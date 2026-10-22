"""Apply the owner-approved 2026-10-22 scarf art; no generation at apply time.

Default: apply cached reviewed outputs. --check: validate installed bytes.
--revert: restore byte-exact originals and remove the two new expressions.
Preflight every file before writing; refuse unrelated edits. Repeated runs are safe.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'art/granny-scarf-20261022'
SHARED_REGISTRIES = ('game/assets/room13-fullbody-dialogue.json',)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def run(check=False, revert=False, root=ROOT, art=ART):
    manifest = json.loads((art / 'manifest.json').read_text())
    rows = manifest['files']
    # Validate the entire transaction first, including archived payloads.
    for row in rows:
        for folder, field in [('originals', 'before_sha256'), ('edited', 'after_sha256')]:
            if row[field] is not None and digest(art / folder / row['path']) != row[field]:
                raise ValueError('Archive hash mismatch: ' + folder + '/' + row['path'])
        actual = digest(root / row['path'])
        expected = row['before_sha256'] if revert else row['after_sha256']
        if check and row['path'] in SHARED_REGISTRIES:
            # Later intakes (e.g. expr-intake-20261022) also edit this registry: check only the
            # granny entries this transaction owns.
            folder = 'originals' if revert else 'edited'
            want = json.loads((art / folder / row['path']).read_text())['people']['granny']['images']
            have = json.loads((root / row['path']).read_text())['people']['granny']['images']
            if any(want.get(e) != have.get(e) for e in ('joy', 'surprise')):
                raise ValueError('Installed granny entries differ: ' + row['path'])
        elif check:
            if actual != expected:
                raise ValueError('Installed hash mismatch: ' + row['path'])
        elif actual not in (row['before_sha256'], row['after_sha256']):
            raise ValueError('Unrelated edits; refusing to overwrite: ' + row['path'])
    if not check:
        for row in rows:
            target = root / row['path']
            expected = row['before_sha256'] if revert else row['after_sha256']
            if digest(target) == expected:
                continue
            if expected is None:
                target.unlink(missing_ok=True)
            else:
                source = art / ('originals' if revert else 'edited') / row['path']
                target.parent.mkdir(parents=True, exist_ok=True)
                temporary = target.with_name(target.name + '.scarf-tmp')
                temporary.write_bytes(source.read_bytes())
                temporary.replace(target)
    return len(rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--revert', action='store_true')
    args = parser.parse_args()
    count = run(args.check, args.revert)
    print(('Checked' if args.check else 'Reverted' if args.revert else 'Applied') + f' {count} files')
