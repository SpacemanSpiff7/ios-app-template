"""Source and artifact fingerprints used by verification helpers."""
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".scratch", ".build", "DerivedData", "__pycache__", ".swiftpm"}


def tree_digest(root, source=False):
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if source and (any(part in SKIP or part.endswith(".xcodeproj") for part in relative.parts)
                       or path.name == "Info.plist" or path.suffix == ".entitlements"):
            continue
        if path.is_symlink():
            payload = str(path.readlink()).encode()
        elif path.is_file():
            payload = path.read_bytes()
        else:
            continue
        digest.update(str(relative).encode() + b"\0")
        digest.update(str(path.lstat().st_mode & 0o777).encode() + b"\0")
        digest.update(hashlib.sha256(payload).digest())
    return digest.hexdigest()


def source_identity(root=ROOT):
    commit, dirty = None, None
    if (root / ".git").exists():
        commit_result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True)
        if commit_result.returncode == 0:
            commit = commit_result.stdout.strip()
        status = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=all"], cwd=root, text=True)
        dirty = status.splitlines()
    return {"commit": commit, "dirty_paths": dirty, "tree_sha256": tree_digest(root, source=True)}
