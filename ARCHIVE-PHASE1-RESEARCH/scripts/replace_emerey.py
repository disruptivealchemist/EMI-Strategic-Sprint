import os
import re
import sys
from pathlib import Path
from difflib import unified_diff

ROOT = Path(__file__).resolve().parents[1]  # repo root
EXCLUDE_DIRS = {'.git', '.venv', 'node_modules', '__pycache__'}

# mapping of regex -> replacement (covers common forms)
REPLACEMENTS = [
    (re.compile(r'\bEmerey\s+Industries\b', re.IGNORECASE), 'Emery Industries'),
    (re.compile(r'\bemereyindustries\b', re.IGNORECASE), 'emeryindustries'),
    (re.compile(r'\bEmerey\b', re.IGNORECASE), 'Emery'),
    (re.compile(r'\bemerey\b', re.IGNORECASE), 'emery'),
]

TEXT_FILE_EXTS = {'.py', '.md', '.txt', '.csv', '.html', '.htm', '.vtt', '.json', '.yaml', '.yml', '.ini', '.cfg', '.rst', '.toml', '.js', '.css'}

def is_text_file(path: Path) -> bool:
    if path.suffix.lower() in TEXT_FILE_EXTS:
        return True
    try:
        with open(path, 'rb') as f:
            chunk = f.read(4096)
            if b'\0' in chunk:
                return False
    except Exception:
        return False
    return True

def apply_replacements(text: str):
    new = text
    for pattern, repl in REPLACEMENTS:
        new = pattern.sub(repl, new)
    return new

def main():
    changed = []
    for p in ROOT.rglob('*'):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if not p.is_file():
            continue
        if not is_text_file(p):
            continue
        try:
            s = p.read_text(encoding='utf-8')
        except Exception:
            continue
        new_s = apply_replacements(s)
        if new_s != s:
            bak = p.with_suffix(p.suffix + '.bak')
            p.rename(bak)  # keep original as backup
            p.write_text(new_s, encoding='utf-8')
            changed.append((p, bak, s.splitlines(keepends=True), new_s.splitlines(keepends=True)))
    if not changed:
        print("No occurrences found.")
        return
    for p, bak, old_lines, new_lines in changed:
        print(f"Modified: {p}")
        diff = unified_diff(old_lines, new_lines, fromfile=str(bak), tofile=str(p))
        for line in diff:
            sys.stdout.write(line)
    print(f"\nTotal files modified: {len(changed)}")
    print("Backups saved with .bak extension next to each modified file.")
    print("Review changes, then run: git add -A && git commit -m 'Replace Emery -> Emery'")

if __name__ == '__main__':
    main()