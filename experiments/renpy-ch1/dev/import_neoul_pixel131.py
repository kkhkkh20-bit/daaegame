"""너울의 검수된 여섯 도트 표정을 연결한다. 기본 실행은 파일·프로필 검사만 한다.

메인 담당자만 --apply를 실행한다. 그때 너울의 일반 대화/질문/단독 회의
프로필과 크기 맞춤표를 갱신하며, 다른 인물·문맥·동작 표는 바꾸지 않는다.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from import_dialogue_gaze116 import SLOTS, build_profiles, normalize_question_layout, read_source

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'art/neoul-pixel-20261108'
REGISTRY = ROOT / 'game/assets/room13-dialogue-player-facing.json'
REVISION = 'neoul-pixel-consistency-20261108'


def prepare():
    receipt = json.loads((ART / 'manifest.json').read_text())
    if receipt['person'] != 'neoul' or receipt['art_revision'] != REVISION:
        raise ValueError('이번 너울 납품 영수증이 아님')
    frames = receipt['frames']
    if len(frames) != 6 or {row['slot'] for row in frames} != set(SLOTS):
        raise ValueError('여섯 고유 기본 표정이 필요함')
    sources = {}
    for frame in frames:
        row = read_source(ROOT / frame['source_master'])
        if row['source_sha256'] != frame['source_sha256']:
            raise ValueError('원본 해시 불일치: ' + frame['source_master'])
        if not frame['runtime_file'].startswith('assets/dialogue-player-facing/neoul20261108/'):
            raise ValueError('이번 너울 경로만 허용: ' + frame['runtime_file'])
        runtime = ROOT / 'game' / frame['runtime_file']
        if hashlib.sha256(runtime.read_bytes()).hexdigest() != frame['runtime_sha256']:
            raise ValueError('런타임 해시 불일치: ' + frame['runtime_file'])
        row['file'] = frame['runtime_file']
        sources[frame['slot']] = row
    profiles = build_profiles(sources, receipt['visible_height_840'], receipt['question_height'])
    front = json.loads(REGISTRY.read_text())
    entry = copy.deepcopy(front['people']['neoul'])
    entry.update(status='approved_runtime', stance='standing', gaze='player',
                 art_style='storybook_source', source_kind='source_master',
                 art_revision=REVISION, profiles=profiles,
                 approval='소유자: 0.20.130 실 플레이 검수의 너울 도트 화풍 교정')
    normalize_question_layout({'neoul': entry})
    return entry


def apply(entry):
    front = json.loads(REGISTRY.read_text())
    front['people']['neoul'] = copy.deepcopy(entry)
    REGISTRY.write_text(json.dumps(front, ensure_ascii=False, indent=2) + '\n')
    from build_dialogue_size_fit import refresh_if_present
    refresh_if_present()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    entry = prepare()
    if args.apply:
        apply(entry)
    print(json.dumps(dict(person='neoul', frames=6, profiles=list(entry['profiles']),
                          art_revision=REVISION, applied=args.apply), ensure_ascii=False))


if __name__ == '__main__':
    main()
