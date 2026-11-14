"""Match declared Swift tests to xcresult identities; parameter cases are executions, not declarations."""
from pathlib import Path
import re
from urllib.parse import unquote, urlparse


def declarations(root, app_target):
    expected = set()
    roots = [(root / "AppTests", app_target)]
    roots += [(path, path.name) for path in sorted((root / "Packages/AppKit/Tests").glob("*")) if path.is_dir()]
    for folder, target in roots:
        for path in sorted(folder.rglob("*.swift")):
            text = path.read_text()
            # Blank comments and string literals so example annotations/braces do not become tests.
            text = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/|"""[\s\S]*?"""|"(?:\\.|[^"\\])*"',
                          lambda match: "\n" * match[0].count("\n") + " ", text)
            stack, pending_type, pending_test = [], None, False
            tokens = re.finditer(r"\b(struct|class|enum|extension|func)\s+([A-Za-z_]\w*(?:\.\w+)*)|@Test\b|[{}]", text)
            for token in tokens:
                word = token[0]
                if token[1] in {"struct", "class", "enum", "extension"}:
                    pending_type = token[2]
                elif word == "@Test":
                    pending_test = True
                elif token[1] == "func" and pending_test:
                    scopes = [value for value in stack if value]
                    key = "/".join([target, *scopes, token[2]])
                    if key in expected:
                        raise ValueError(f"Ambiguous test name {key}; use distinct test function names.")
                    expected.add(key)
                    pending_test = False
                elif word == "{":
                    stack.append(pending_type)
                    pending_type = None
                elif word == "}":
                    if stack:
                        stack.pop()
    return expected


def cases(tree):
    if isinstance(tree, dict):
        if tree.get("nodeType") == "Test Case":
            yield tree
        for value in tree.values():
            yield from cases(value)
    elif isinstance(tree, list):
        for value in tree:
            yield from cases(value)


def check(expected, summary, tree):
    observed, failed = set(), []
    for case in cases(tree):
        url = case.get("nodeIdentifierURL")
        if not url:
            raise ValueError("A test case lacks nodeIdentifierURL; inspect this xcresult format.")
        parts = unquote(urlparse(url).path).strip("/").split("/")
        if len(parts) < 3:
            raise ValueError(f"Unsupported test identity: {url}")
        parts[-1] = parts[-1].split("(")[0]
        observed.add("/".join(parts[1:]))  # remove scheme; retain bundle/suite/function
        if case.get("result") != "Passed":
            failed.append(case.get("nodeIdentifier", url))
    executions = sum(row.get("passedTests", 0) for row in summary.get("devicesAndConfigurations", []))
    problems = []
    if not expected:
        problems.append("No declared tests were found.")
    if summary.get("result") != "Passed" or summary.get("failedTests", 0) or summary.get("skippedTests", 0):
        problems.append("The result contains failures/skips or did not pass.")
    if expected != observed:
        problems.append(f"Missing identities: {sorted(expected - observed)}; unexpected: {sorted(observed - expected)}")
    if failed or summary.get("passedTests") != len(expected) or executions < len(expected):
        problems.append(f"Incomplete execution: {len(expected)} declared, {summary.get('passedTests')} passed, "
                        f"{executions} executions, non-passed cases {failed}")
    if problems:
        raise ValueError("\n".join(problems))
    return {"declared_tests": len(expected), "passed_tests": summary["passedTests"], "executions": executions,
            "failures": 0, "skips": 0, "identities": sorted(observed)}
