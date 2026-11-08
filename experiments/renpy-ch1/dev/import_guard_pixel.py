"""검수한 돌목 도트 여섯 원본만 가져온다. 원본 수정·픽셀 필터는 하지 않는다.

인물 표시 키는 납품 기록의 기존 값으로 유지한다. 기본 실행은 해시 검사,
--apply는 품질95 WebP·정면 연결·크기표를 갱신한다.
"""
import argparse
import json
from pathlib import Path

from import_art import encode
from import_dialogue_gaze116 import SLOTS, build_profiles, normalize_question_layout, read_source

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'art/pixel-consistency-20261108/guard/manifest.json'
REGISTRY = ROOT / 'game/assets/room13-dialogue-player-facing.json'


def prepare():
    receipt = json.loads(MANIFEST.read_text())
    sources = {}
    for frame in receipt['frames']:
        slot = frame['slot']
        if slot in sources:
            raise ValueError('중복 표정: ' + slot)
        row = read_source(ROOT / frame['source_master'])
        if row['source_sha256'] != frame['source_sha256']:
            raise ValueError('검수 원본 해시 불일치: ' + slot)
        row['file'] = frame['runtime_file']
        sources[slot] = row
    if set(sources) != set(SLOTS):
        raise ValueError('돌목 여섯 표정이 모두 필요함')
    return receipt, sources


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    receipt, sources = prepare()
    if args.apply:
        profiles = build_profiles(sources, receipt['visible_height_840'])
        data = json.loads(REGISTRY.read_text())
        entry = dict(data['people']['guard'], profiles=profiles,
                     art_revision='guard-pixel-consistency-20261108',
                     approval='소유자: 기존 도트 화풍과 돌목·누비의 그림체 차이 교정')
        for row in sources.values():
            target = ROOT / 'game' / row['file']
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(encode(ROOT / row['source_master']))
        normalize_question_layout({'guard': entry})
        data['people']['guard'] = entry
        REGISTRY.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        from build_dialogue_size_fit import refresh_if_present
        refresh_if_present()
    print(json.dumps(dict(person='guard', frames=len(sources), applied=args.apply), ensure_ascii=False))


if __name__ == '__main__':
    main()
