"""검수된 누비 6표정만 다시 가져온다. 원본 그림은 수정하지 않는다.

python3 dev/import_nubi_consistency.py          # 원본·해시 확인만
python3 dev/import_nubi_consistency.py --apply  # WebP·정면 연결·크기표 갱신

새 납품은 art/dialogue-consistency-20261108/resident_nubi/manifest.json으로
추적한다. 예전 gaze116 전체 가져오기는 이 새 리비전을 덮지 않는다.
"""
import argparse
import json
from pathlib import Path

from import_art import encode
from import_dialogue_gaze116 import SLOTS, build_profiles, normalize_question_layout, read_source

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'art/dialogue-consistency-20261108/resident_nubi'
REGISTRY = ROOT / 'game/assets/room13-dialogue-player-facing.json'


def prepare():
    manifest = json.loads((ART / 'manifest.json').read_text())
    sources = {}
    for receipt in manifest['frames']:
        slot = receipt['slot']
        row = read_source(ROOT / receipt['source_master'])
        if row['source_sha256'] != receipt['source_sha256']:
            raise ValueError('검수한 원본과 다름: ' + slot)
        row['file'] = receipt['runtime_file']
        sources[slot] = row
    if set(sources) != set(SLOTS):
        raise ValueError('누비 6표정 원본 필요')
    return manifest, sources


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    manifest, sources = prepare()
    if args.apply:
        profiles = build_profiles(sources, manifest['visible_height_840'])
        for row in sources.values():
            target = ROOT / 'game' / row['file']
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(encode(ROOT / row['source_master']))
        data = json.loads(REGISTRY.read_text())
        entry = dict(data['people']['resident_nubi'],
                     art_revision=manifest['art_revision'],
                     approval='소유자: 화질·작화 일관성 리뷰 개선 승인', profiles=profiles)
        normalize_question_layout({'resident_nubi': entry})
        data['people']['resident_nubi'] = entry
        REGISTRY.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        from build_dialogue_size_fit import refresh_if_present
        refresh_if_present()
    print(json.dumps(dict(person='resident_nubi', frames=len(sources),
                          revision=manifest['art_revision'], applied=args.apply), ensure_ascii=False))


if __name__ == '__main__':
    main()
