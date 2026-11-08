"""초롱의 평상6표정과 기존 광장 작업1자세를 분리한다. --apply는 메인 담당자만 실행한다."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from import_dialogue_gaze116 import SLOTS, build_profiles, normalize_question_layout, read_source

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'art/chorong-calm132-20261108'
REGISTRY = ROOT / 'game/assets/room13-dialogue-player-facing.json'
POSE_REGISTRY = ROOT / 'game/assets/room13-dialogue-pose-source-art.json'
PERSON = 'resident_lamplighter'
REVISION = 'chorong-everyday-pixel-20261108'
WORK_POSE = 'lamp_work132'


def receipt():
    row = json.loads((ART / 'manifest.json').read_text())
    if row['person'] != PERSON or row['art_revision'] != REVISION:
        raise ValueError('이번 초롱 평상 납품 영수증이 아님')
    return row


def prepare():
    row = receipt()
    if len(row['frames']) != 6 or {f['slot'] for f in row['frames']} != set(SLOTS):
        raise ValueError('서로 다른 여섯 표정이 필요함')
    sources = {}
    for frame in row['frames']:
        source = read_source(ROOT / frame['source_master'])
        if source['source_sha256'] != frame['source_sha256']:
            raise ValueError('생성 원본 해시 불일치: ' + frame['source_master'])
        if not frame['runtime_file'].startswith('assets/dialogue-player-facing/chorong20261108/'):
            raise ValueError('이번 초롱 평상 경로만 허용: ' + frame['runtime_file'])
        runtime = ROOT / 'game' / frame['runtime_file']
        if hashlib.sha256(runtime.read_bytes()).hexdigest() != frame['runtime_sha256']:
            raise ValueError('런타임 해시 불일치: ' + frame['runtime_file'])
        source['file'] = frame['runtime_file']
        sources[frame['slot']] = source
    front = json.loads(REGISTRY.read_text())
    entry = copy.deepcopy(front['people'][PERSON])
    entry.update(status='approved_runtime', stance='standing', gaze='player',
                 art_style='storybook_source', source_kind='source_master',
                 art_revision=REVISION,
                 profiles=build_profiles(sources, row['visible_height_840'], row['question_height']),
                 approval='소유자: 완주 검수의 평상 대화/광장 작업 그림 분리')
    normalize_question_layout({PERSON: entry})
    return entry


def prepare_work_pose():
    # 반드시 영수증의 동결된 작업 프로필을 읽는다. 일반 그림을 교체한 뒤 재실행해도
    # 새 평상 표정을 작업 포즈로 오인해 덮어쓰지 않는다.
    work = copy.deepcopy(receipt()['work_pose'])
    if work['key'] != WORK_POSE or work['record'] != 'MS14_D02_S01_L0011':
        raise ValueError('광장 작업 한 대사 계약 불일치')
    for profile in work['profiles'].values():
        # 작업 자세는 질문용 일반 전신 계약을 빌리지 않는다.
        profile.pop('question_top', None)
        if set(profile['frames']) != {'neutral', 'flustered'}:
            raise ValueError('기존 작업 표정 재사용 계약 불일치')
        for frame in profile['frames'].values():
            if not frame['file'].startswith('assets/dialogue-player-facing/gaze116/resident_lamplighter/'):
                raise ValueError('기존 작업 원화만 허용')
            path = ROOT / frame['source_master']
            if hashlib.sha256(path.read_bytes()).hexdigest() != frame['source_sha256']:
                raise ValueError('기존 작업 원본 변경됨')
            if not (ROOT / 'game' / frame['file']).is_file():
                raise ValueError('기존 작업 런타임 없음')
    return dict(profiles=work['profiles'], kind=work['kind'],
                visible_height_at_840=work['visible_height_at_840'])


def apply(entry, work_pose=None):
    front = json.loads(REGISTRY.read_text())
    front['people'][PERSON] = copy.deepcopy(entry)
    poses = json.loads(POSE_REGISTRY.read_text())
    target = poses['people'].setdefault(PERSON, {}).setdefault('pose_profiles', {})
    target[WORK_POSE] = copy.deepcopy(work_pose if work_pose is not None else prepare_work_pose())
    REGISTRY.write_text(json.dumps(front, ensure_ascii=False, indent=2) + '\n')
    POSE_REGISTRY.write_text(json.dumps(poses, ensure_ascii=False, indent=2) + '\n')
    from build_dialogue_size_fit import refresh_if_present
    refresh_if_present()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    entry = prepare()
    work = prepare_work_pose()
    if args.apply:
        apply(entry, work)
    print(json.dumps(dict(person=PERSON, frames=6, art_revision=REVISION,
                          preserved_work_pose=WORK_POSE, applied=args.apply), ensure_ascii=False))


if __name__ == '__main__':
    main()
