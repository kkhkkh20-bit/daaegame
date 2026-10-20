"""Reproducible, lossless D01 extraction from the verified delivery folder.

python3 dev/import_production_basis01.py /path/to/01_스토리기준본 --check
No natural-language condition or branch summary is executed here.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def extract(source):
    path = source / "다람탐정_제작기준본01_대사연출조건.json"
    data = json.loads(path.read_text())
    scenes = {s["scene_id"]: s for s in data["scenes"]}
    selected = [scenes["MS14_D01_" + key] for key in ("S01", "S02", "S03")]
    registration = scenes["MS14_D01_S04"]
    selected.append({**registration, "blocks": [registration["blocks"][0]]})
    return json.dumps(dict(version=data["version"], source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                           scenes=selected), ensure_ascii=False, indent=2) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = extract(args.source)
    target = ROOT / "game/production-basis01-d01.json"
    if args.check:
        if target.read_text() != expected: raise SystemExit("FAIL: source D01 slice differs")
        print("PASS: every exported scene/block/record/option matches the verified source")
    else:
        target.write_text(expected)
