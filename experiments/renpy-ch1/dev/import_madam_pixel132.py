"""백 부인 고해상도 도트 여섯 표정을 준비한다. 기본 실행은 검사만 한다.

백 부인은 기존 player-facing 등록이 없어 작은 source-master를 확대했다.
검수된 원본만 새 일반 프로필로 준비하며, --apply는 메인 통합 담당자가 실행한다.
기존 대화·현장 키에 맞춘 840/질문 높이는 납품 영수증으로 보존한다.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from import_dialogue_gaze116 import SLOTS, build_profiles, normalize_question_layout, read_source

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'art/madam-pixel132-20261108'
REGISTRY = ROOT / 'game/assets/room13-dialogue-player-facing.json'
PERSON = 'resident_madam'
REVISION = 'madam-pixel-consistency-20261108'
RUNTIME_PREFIX = 'assets/dialogue-player-facing/madam20261108/'


def prepare():
    receipt = json.loads((ART / 'manifest.json').read_text())
    if receipt['person'] != PERSON or receipt['art_revision'] != REVISION:
        raise ValueError('이번 백 부인 납품 영수증이 아님')
    frames = receipt['frames']
    if len(frames) != 6 or {row['slot'] for row in frames} != set(SLOTS):
        raise ValueError('여섯 고유 기본 표정이 필요함')
    if len({row['source_sha256'] for row in frames}) != 6:
        raise ValueError('여섯 표정 원본이 서로 같음')
    sources = {}
    for frame in frames:
        row = read_source(ROOT / frame['source_master'])
        if row['source_sha256'] != frame['source_sha256']:
            raise ValueError('원본 해시 불일치: ' + frame['source_master'])
        if not frame['runtime_file'].startswith(RUNTIME_PREFIX):
            raise ValueError('이번 백 부인 경로만 허용: ' + frame['runtime_file'])
        expected = PERSON + '-flustered.webp' if frame['slot'] == 'flustered' else frame['slot'] + '.webp'
        if Path(frame['runtime_file']).name != expected:
            raise ValueError('표정 파일명 불일치: ' + frame['runtime_file'])
        runtime = ROOT / 'game' / frame['runtime_file']
        if hashlib.sha256(runtime.read_bytes()).hexdigest() != frame['runtime_sha256']:
            raise ValueError('런타임 해시 불일치: ' + frame['runtime_file'])
        row['file'] = frame['runtime_file']
        sources[frame['slot']] = row
    profiles = build_profiles(sources, receipt['visible_height_840'], receipt['question_height'])
    front = json.loads(REGISTRY.read_text())
    entry = copy.deepcopy(front['people'].get(PERSON, {}))
    entry.update(status='approved_runtime', stance='standing', gaze='player',
                 art_style='storybook_source', source_kind='source_master',
                 art_revision=REVISION, profiles=profiles,
                 approval='소유자: 0.20.131 제1부 완주 검수의 조연 도트 밀도·확대 품질 교정')
    normalize_question_layout({PERSON: entry})
    return entry


def apply(entry):
    front = json.loads(REGISTRY.read_text())
    front['people'][PERSON] = copy.deepcopy(entry)
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
    print(json.dumps(dict(person=PERSON, frames=6, profiles=list(entry['profiles']),
                          art_revision=REVISION, applied=args.apply), ensure_ascii=False))


if __name__ == '__main__':
    main()
