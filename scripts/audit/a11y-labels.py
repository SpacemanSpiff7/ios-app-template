#!/usr/bin/env python3
"""Static check of icon-only trailing labels; device VoiceOver review remains required."""
from pathlib import Path
import re
import sys
files = [Path(p) for p in sys.argv[1:]] or [p for root in ('App', 'Packages/AppKit/Sources') for p in Path(root).rglob('*.swift')]
failed = False
checked = 0
for path in files:
    text = path.read_text()
    for match in re.finditer(r'\blabel:\s*\{', text):
        start = match.end()
        depth, end = 1, start
        while end < len(text) and depth:
            depth += (text[end] == '{') - (text[end] == '}')
            end += 1
        label = text[start:end-1]
        if 'Image(systemName:' not in label or re.search(r'\b(?:Text|Label)\s*\(', label):
            continue
        checked += 1
        # Include chained modifiers, stopping before the next statement/control.
        tail = text[end:]
        modifiers = re.match(r'(?:\s*\.[^\n]+(?:\n|$))*', tail).group()
        if '.accessibilityLabel(' not in label + modifiers:
            line = text.count('\n', 0, match.start()) + 1
            print(f'{path}:{line}: icon-only label needs accessibilityLabel')
            failed = True
print(f'Checked {checked} icon-only trailing labels (static subset; VoiceOver still required).')
sys.exit(failed)
