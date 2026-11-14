from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from test_results import check, declarations

ROOT = Path(__file__).resolve().parents[2]
(ROOT / ".scratch/tests").mkdir(parents=True, exist_ok=True)


def case(name, result="Passed"):
    return {"nodeType": "Test Case", "nodeIdentifierURL": f"test://com.apple.xcode/App/CoreTests/Suite/{name}()",
            "result": result}


class ExecutionGateTests(unittest.TestCase):
    def setUp(self):
        self.expected = {"CoreTests/Suite/first", "CoreTests/Suite/second"}
        self.summary = {"result": "Passed", "passedTests": 2, "failedTests": 0, "skippedTests": 0,
                        "devicesAndConfigurations": [{"passedTests": 5}]}
        self.tree = [case("first"), case("second")]

    def test_parameter_executions_are_distinct_from_declarations(self):
        report = check(self.expected, self.summary, self.tree)
        self.assertEqual((report["declared_tests"], report["executions"]), (2, 5))

    def test_equal_counts_cannot_hide_a_missing_test_identity(self):
        self.tree[1] = case("unexpected")
        with self.assertRaisesRegex(ValueError, "Missing identities"):
            check(self.expected, self.summary, self.tree)

    def test_success_summary_cannot_hide_crashed_case(self):
        self.tree[1] = case("second", "Failed")
        with self.assertRaises(ValueError):
            check(self.expected, self.summary, self.tree)

    def test_success_with_skips_is_rejected(self):
        self.summary["skippedTests"] = 1
        with self.assertRaises(ValueError):
            check(self.expected, self.summary, self.tree)

    def test_no_execution_is_rejected(self):
        self.summary["devicesAndConfigurations"] = []
        with self.assertRaises(ValueError):
            check(self.expected, self.summary, self.tree)

    def test_missing_case_identity_fails_closed(self):
        self.tree[0].pop("nodeIdentifierURL")
        with self.assertRaisesRegex(ValueError, "lacks"):
            check(self.expected, self.summary, self.tree)

    def test_source_scopes_attributes_and_comments(self):
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch/tests") as folder:
            root = Path(folder)
            target = root / "Packages/AppKit/Tests/CoreTests"
            target.mkdir(parents=True)
            (target / "Tests.swift").write_text(
                '// @Test func fake() {}\nstruct Outer {\n'
                ' @Test(arguments: [1, 2])\n func first(value: Int) {}\n'
                ' struct Nested { @Test func second() { let text = "@Test func fake() {}" } }\n'
                '}\nextension Outer { @Test func third() {} }\n')
            self.assertEqual(declarations(root, "AppTests"), {
                "CoreTests/Outer/first", "CoreTests/Outer/Nested/second", "CoreTests/Outer/third",
            })
