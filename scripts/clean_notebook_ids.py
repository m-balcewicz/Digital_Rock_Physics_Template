#!/usr/bin/env python3
"""Remove per-cell `id` keys from notebooks. Intended to be used as a pre-commit hook.

This script edits notebooks in-place. It preserves other notebook structure using nbformat.
"""
import sys
from pathlib import Path
import nbformat


def clean_notebook(path: Path) -> bool:
    nb = nbformat.read(str(path), as_version=4)
    changed = False
    for cell in nb.cells:
        # remove top-level cell id if present
        if 'id' in cell:
            cell.pop('id', None)
            changed = True
        # optionally: sanitize empty metadata to a dict (keep key present)
        if 'metadata' in cell and cell['metadata'] is None:
            cell['metadata'] = {}
            changed = True
    if changed:
        nbformat.write(nb, str(path))
    return changed


def main(argv):
    paths = argv[1:]
    if not paths:
        paths = [str(p) for p in Path('.').rglob('*.ipynb')]
    any_changed = False
    for p in paths:
        pth = Path(p)
        try:
            changed = clean_notebook(pth)
            print(f'Processed {p}: changed={changed}')
            any_changed = any_changed or changed
        except Exception as exc:
            print(f'Failed to process {p}: {exc}', file=sys.stderr)
            return 2
    return 1 if any_changed else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
#!/usr/bin/env python3
import nbformat
from pathlib import Path
import sys

def clean_notebook(path: Path):
    nb = nbformat.read(str(path), as_version=4)
    changed = False
    for cell in nb.cells:
        if 'id' in cell:
            cell.pop('id', None)
            changed = True
        # If you want to remove empty metadata dicts:
        # if 'metadata' in cell and not cell['metadata']:
        #     cell['metadata'] = {}
    if changed:
        nbformat.write(nb, str(path))
    return changed

if __name__ == '__main__':
    paths = sys.argv[1:]
    if not paths:
        paths = [str(p) for p in Path('.').rglob('*.ipynb')]
    for p in paths:
        try:
            changed = clean_notebook(Path(p))
            print(f'{p}: changed={changed}')
        except Exception as e:
            print(f'{p}: error {e}')
            raise