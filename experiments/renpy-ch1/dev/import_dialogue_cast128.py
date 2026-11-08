"""검수한 대화 인물 원본만 연결한다. 그림·이야기·판정은 수정하지 않는다."""
import argparse
import copy
import json
from pathlib import Path

from import_art import encode
from import_dialogue_gaze116 import SLOTS, build_profiles, normalize_question_layout, read_source

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'art/dialogue-cast-unify-20261108'
ASSETS = ROOT / 'game/assets'
REVISION = 'dialogue-cast-pixel-20261108'


def read(path):
    return json.loads(path.read_text())


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def verified(frame):
    row = read_source(ROOT / frame['source_master'])
    if row['source_sha256'] != frame['source_sha256']:
        raise ValueError('검수 원본 해시 불일치: ' + frame['source_master'])
    row['file'] = frame['runtime_file']
    if not row['file'].startswith('assets/dialogue-player-facing/cast20261108/'):
        raise ValueError('이번 납품 경로만 허용: ' + row['file'])
    return row


def prepare():
    targets = read(ART / 'runtime-fit-targets.json')
    prepared = {}
    for who, target in targets.items():
        receipt = read(ART / who / 'manifest.json')
        sources = {frame['slot']: verified(frame) for frame in receipt['frames']}
        if len(receipt['frames']) != 6 or set(sources) != set(SLOTS):
            raise ValueError('여섯 고유 표정이 필요함: ' + who)
        contexts = {frame['slot']: verified(frame) for frame in receipt.get('context_frames', [])}
        poses = {frame['pose']: verified(frame) for frame in receipt.get('pose_frames', [])}
        profiles = build_profiles(dict(sources, **contexts), target['visible_height_840'], target['question_height'])
        prepared[who] = dict(sources=sources, contexts=contexts, poses=poses, profiles=profiles)
    return prepared


def apply(prepared):
    front_path = ASSETS / 'room13-dialogue-player-facing.json'
    context_path = ASSETS / 'room13-dialogue-context-art.json'
    pose_path = ASSETS / 'room13-dialogue-pose-source-art.json'
    front, context, poses = read(front_path), read(context_path), read(pose_path)
    # 원본 압축을 끝낸 다음에만 알파 경계를 읽어 발 선을 맞춘다.
    for row in prepared.values():
        for source in [*row['sources'].values(), *row['contexts'].values(), *row['poses'].values()]:
            target = ROOT / 'game' / source['file']
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(encode(ROOT / source['source_master']))
    for who, row in prepared.items():
        entry = dict(front['people'].get(who, {}), status='approved_runtime', stance='standing',
            gaze='player', art_style='storybook_source', source_kind='source_master', art_revision=REVISION,
            approval='소유자: 대화할 때 나오는 인물 그림의 도트 화풍 차이 교정',
            profiles=copy.deepcopy(row['profiles']))
        for profile in entry['profiles'].values():
            profile['frames'] = {key: frame for key, frame in profile['frames'].items() if key in SLOTS}
        normalize_question_layout({who: entry})
        front['people'][who] = entry
        for slot in row['contexts']:
            key = who + ':' + slot
            old = context['entries'][key]
            profiles = copy.deepcopy(row['profiles'])
            for profile in profiles.values():
                profile['frames'] = {slot: profile['frames'][slot]}
            profiles['560']['question_top'] = entry['profiles']['560']['question_top']
            context['entries'][key] = dict(old, art_revision=REVISION, profiles=profiles)
        for pose, source in row['poses'].items():
            # 앉아서 읽기/듣기의 동작·크기는 기존 authored 프로필에 맞춘다.
            from PIL import Image
            old = poses['people'][who]['pose_profiles'][pose]
            profiles = copy.deepcopy(old['profiles'])
            for profile in profiles.values():
                for slot, frame in profile['frames'].items():
                    with Image.open(ROOT / 'game' / frame['file']) as image:
                        bounds = image.getchannel('A').point(lambda a: 255 if a >= 40 else 0).getbbox()
                    scale = frame.get('scale', 1)
                    visible = (bounds[3] - bounds[1]) * scale
                    center = frame['offset'][0] + (bounds[0] + bounds[2]) * scale / 2
                    foot = frame['offset'][1] + bounds[3] * scale
                    left, top, right, bottom = source['bounds']
                    factor = visible / (bottom - top)
                    new = dict(file=source['file'], scale=factor, nearest=False, native_detail=True,
                        offset=[round(center - (left + right) * factor / 2), round(foot - bottom * factor)],
                        source_master=source['source_master'], source_sha256=source['source_sha256'])
                    if new['offset'][0] + left * factor < 0 or new['offset'][0] + right * factor > profile['canvas'][0]:
                        raise ValueError('앉은 자세의 폭이 기존 공간을 벗어남: ' + who + ':' + pose)
                    profile['frames'][slot] = new
                profile.pop('pixel_grid', None)
                profile.pop('dot_scale', None)
                profile['smooth'] = True
            left, top, right, bottom = source['bounds']
            poses['people'][who]['pose_profiles'][pose] = dict(old, profiles=profiles, art_revision=REVISION,
                source_master=source['source_master'], source_sha256=source['source_sha256'],
                source_crop_xywh=[left, top, right - left, bottom - top], kind='approved_authored_pixel_pose')
    write(front_path, front)
    write(context_path, context)
    write(pose_path, poses)
    from build_dialogue_size_fit import refresh_if_present
    refresh_if_present()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    prepared = prepare()
    if args.apply:
        apply(prepared)
    print(json.dumps(dict(people=len(prepared), frames=sum(len(row[k]) for row in prepared.values()
        for k in ('sources', 'contexts', 'poses')), applied=args.apply), ensure_ascii=False))


if __name__ == '__main__':
    main()
