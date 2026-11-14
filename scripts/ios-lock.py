#!/usr/bin/env python3
"""Hold an OS-released lock for the entire command; nested helpers share ownership."""
import fcntl
import os
from pathlib import Path
import sys
import tempfile

if len(sys.argv) < 2:
    sys.exit("Usage: with-ios-lock.sh command [arguments...]")
path = str(Path(tempfile.gettempdir()) / f"ios-app-template-ios-{os.getuid()}.lock")
if os.environ.get("IOS_LOCK_HELD") != path:
    handle = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        sys.exit("Another iOS build/simulator/device command owns the lock. Wait for it to finish.")
    os.set_inheritable(handle, True)
    os.environ["IOS_LOCK_HELD"] = path
os.execvp(sys.argv[1], sys.argv[1:])
