"""완주 검수의 진료 담당자·누비 큰아이 도트 원화를 검사하고 연결한다.

기본 실행은 검사만 한다. --apply는 메인 통합 담당자만 사용하며, 신규
player-facing 두 엔트리만 추가/교체한다. 공유 주민 원화는 변경하지 않는다.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from import_dialogue_gaze116 import SLOTS, build_profiles, normalize_question_layout, read_source

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'art/support-pixel132-20261108'
REGISTRY = ROOT / 'game/assets/room13-dialogue-player-facing.json'
REVISION = 'support-pixel-consistency-20261108'
TARGETS = {
    'ms14_clinician': (630, 560),
    'kid_nubi1': (495, 373.3333333333333),
}


def prepare():
    entries = {}
    for person, (visible_height, question_height) in TARGETS.items():
        receipt = json.loads((ART / person / 'manifest.json').read_text())
        if receipt['person'] != person or receipt['art_revision'] != REVISION:
            raise ValueError('이번 조연 납품 영수증이 아님: ' + person)
        if receipt['visible_height_840'] != visible_height or receipt['question_height'] != question_height:
            raise ValueError('기존 표시 키 계약과 다름: ' + person)
        frames = receipt['frames']
        if len(frames) != 6 or {row['slot'] for row in frames} != set(SLOTS):
            raise ValueError('여섯 고유 기본 표정이 필요함: ' + person)
        sources = {}
        for frame in frames:
            row = read_source(ROOT / frame['source_master'])
            if row['source_sha256'] != frame['source_sha256']:
                raise ValueError('원본 해시 불일치: ' + frame['source_master'])
            if not frame['runtime_file'].startswith('assets/dialogue-player-facing/support132-20261108/' + person + '/'):
                raise ValueError('이번 조연 경로만 허용: ' + frame['runtime_file'])
            runtime = ROOT / 'game' / frame['runtime_file']
            if hashlib.sha256(runtime.read_bytes()).hexdigest() != frame['runtime_sha256']:
                raise ValueError('런타임 해시 불일치: ' + frame['runtime_file'])
            row['file'] = frame['runtime_file']
            sources[frame['slot']] = row
        profiles = build_profiles(sources, visible_height, question_height)
        entries[person] = dict(
            status='approved_runtime', stance='standing', gaze='player',
            art_style='storybook_source', source_kind='source_master',
            art_revision=REVISION, profiles=profiles,
            approval='소유자: 0.20.131 완주 검수의 조연 도트 품질 교정',
        )
    normalize_question_layout(entries)
    return entries


def apply(entries):
    if set(entries) != set(TARGETS):
        raise ValueError('이번 조연 두 엔트리만 적용할 수 있음')
    front = json.loads(REGISTRY.read_text())
    front['people'].update(copy.deepcopy(entries))
    REGISTRY.write_text(json.dumps(front, ensure_ascii=False, indent=2) + '\n')
    from build_dialogue_size_fit import refresh_if_present
    refresh_if_present()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    entries = prepare()
    if args.apply:
        apply(entries)
    print(json.dumps(dict(people=list(entries), frames=12, art_revision=REVISION,
                          applied=args.apply), ensure_ascii=False))


if __name__ == '__main__':
    main()
