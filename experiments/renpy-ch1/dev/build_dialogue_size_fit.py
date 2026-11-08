"""승인 대화 원화는 그대로 두고 현장 키에 맞는 표시 프로필만 만든다."""
import argparse
import ast
import copy
import json
import math
from functools import lru_cache
from pathlib import Path
import textwrap

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'game'
OUT = GAME / 'assets/room13-dialogue-size-fit.json'
REVISION = 'dialogue-size-20261107'
CONTEXTS = {
    'bami:small_relief', 'resident_lamplighter:guarded_relief',
    'kid_kkomi:resilient_pride', 'resident_tosil:empathetic_confusion',
    'kid_kkomi:intake21_kkomi_anxious', 'kid_kkomi:intake21_kkomi_joy',
    'kid_dodam:intake21_dodam_joy', 'kid_saemi:intake21_saemi_anxious',
    'resident_ubak:intake21_ubak_anxious', 'resident_ubak:intake21_ubak_angry',
}


def read(name):
    return json.loads((GAME / 'assets' / name).read_text())


@lru_cache(None)
def alpha_bounds(path):
    with Image.open(GAME / path) as image:
        return image.convert('RGBA').getchannel('A').point(lambda a: 255 if a >= 40 else 0).getbbox()


def signature(profiles):
    return {h: dict(canvas=p['canvas'], frames={k: [f['file'], f['offset'], f.get('scale', 1.0)]
        for k, f in p['frames'].items()}) for h, p in profiles.items()}


def visible(frame):
    b = alpha_bounds(frame['file'])
    return (b[3] - b[1]) * frame.get('scale', 1.0)


def reshape(profile, heights, question=False):
    """원본 비율을 유지한다. 반응 컷의 웅크림은 talk 대비 원래 비율을 유지한다."""
    result = copy.deepcopy(profile)
    result.pop('dot_scale', None)
    result.pop('question_top', None)
    result['smooth'] = True  # fit_profile의 도트 정수배 분기가 최종 scale을 덮지 않게 한다.
    result['size_fit_revision'] = REVISION
    frames = result['frames']
    for slot, frame in frames.items():
        target = heights.get(slot, heights.get('neutral', next(iter(heights.values()))))
        b = alpha_bounds(frame['file'])
        frame['scale'] = target / (b[3] - b[1])
        # anchor는 원래 dot_scale 경로 전용이다. 새 최종 source fitting에서는 쓰지 않는다.
        frame.pop('anchor', None)
    widths = [(alpha_bounds(f['file'])[2] - alpha_bounds(f['file'])[0]) * f['scale'] for f in frames.values()]
    body_heights = [visible(f) for f in frames.values()]
    canvas = [math.ceil(max(widths)) + 48, math.ceil(max(body_heights)) + 48]
    if not question:
        canvas = [max(a, b) for a, b in zip(canvas, profile['canvas'])]
    result['canvas'] = canvas
    feet = []
    for frame in frames.values():
        b = alpha_bounds(frame['file']); scale = frame['scale']
        frame['offset'] = [round(canvas[0] / 2 - (b[0] + b[2]) * scale / 2), round(24 - b[1] * scale)]
        feet.append(frame['offset'][1] + b[3] * scale)
    if question:
        result['question_top'] = math.floor(708 - max(feet))
    return result


def runtime_smooth():
    source = (GAME / 'systems/room13_dialogue_beats.rpy').read_text().split('init 170 python:', 1)[1]
    tree = ast.parse(textwrap.dedent(source))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'r13_closeup_smooth_profiles')
    env = dict(R13_CLOSEUP_SMOOTH_TABLE=read('room13-closeup-smooth.json'), _r13_closeup_smooth_cache={},
               renpy=type('Files', (), {'loadable': staticmethod(lambda path: (GAME / path).is_file())}))
    exec(compile(ast.Module(body=[node], type_ignores=[]), '기존 원본 연결', 'exec'), env)
    return env['r13_closeup_smooth_profiles']


def build():
    people = read('room13-dialogue-talk-art.json')['people']
    people.update(read('room13-dialogue-talk-art-extra.json')['people'])
    front = read('room13-dialogue-player-facing.json')['people']
    field = read('room13-field-dot-v2.json')['people']
    source = (GAME / 'systems/room13_minor_extras_art.rpy').read_text().split('init 327 python:', 1)[1]
    tree = ast.parse(textwrap.dedent(source))
    aliases = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == 'R13_MINOR_ART_USERS' for t in n.targets)))
    smooth = runtime_smooth()
    output = dict(revision=REVISION, alpha_threshold=40, contract='840=field_height*3; 760 proportional; question feet<=708', people={}, contexts={}, question_poses={})
    for who, entry in people.items():
        field_person = who if who in field else aliases.get(who, (who,))[0]
        poses = field[field_person]['poses']
        fd = poses.get('neutral') or next(iter(poses.values()))
        field_h = fd['size'][1]
        # 공용 아이의 v111_* 별칭도 그림과 같은 키를 쓴다. 이야기의 아동 분류는 바꾸지 않는다.
        child = who == 'daram' or who.startswith('kid_') or field_h <= 166
        raw = front[who]['profiles'] if who in front else smooth(who, entry['profiles'])
        baseline = raw['840']; target = field_h * 3.0
        neutral = visible(baseline['frames']['neutral'])
        preserve = abs(neutral / target - 1) <= .02
        # 표정의 굽힘·귀·머리 모양 차이는 보존하고, neutral 기준 공통 배율만 바꾼다.
        factor = 1.0 if preserve else target / neutral
        heights = {k: visible(f) * factor for k, f in baseline['frames'].items()}
        qheight = field_h / (165.0 if child else 210.0) * (560 * 2 / 3 if child else 560)
        qfactor = qheight / visible(raw['560']['frames']['neutral'])
        profiles = {'840': copy.deepcopy(baseline) if preserve else reshape(baseline, heights),
                    '760': reshape(raw['760'], {k: v * 760 / 840 for k, v in heights.items()}),
                    '560': reshape(raw['560'], {k: visible(f) * qfactor for k, f in raw['560']['frames'].items()}, True)}
        profiles['840'].pop('dot_scale', None)
        profiles['840']['smooth'] = True
        profiles['840']['size_fit_revision'] = REVISION
        output['people'][who] = dict(field_person=field_person, field_height=field_h, child=child,
            stature_source='room13-field-dot-v2.json; R13_MINOR_ART_USERS aliases', target_height_840=target,
            preserved_840=preserve, question_visible_height=qheight, input_profiles=signature(raw), profiles=profiles)
    contexts = read('room13-dialogue-context-art.json')['entries']
    for key in sorted(CONTEXTS):
        entry = contexts[key]; who = entry['person']; raw = entry['profiles']
        ref = output['people'][who]
        target = visible(ref['profiles']['840']['frames']['neutral'])
        profiles = {h: reshape(p, {k: (ref['question_visible_height'] if h == '560' else target * int(h) / 840)
                    for k in p['frames']}, h == '560') for h, p in raw.items()}
        # 질문을 열 때 마지막 문맥이 남아도, 일반 질문 y와 같은 발 선을 쓴다.
        question = ref['profiles']['560']
        foot = max(f['offset'][1] + alpha_bounds(f['file'])[3] * f.get('scale', 1.0) for f in question['frames'].values())
        for frame in profiles['560']['frames'].values():
            frame['offset'][1] = math.floor(foot - alpha_bounds(frame['file'])[3] * frame['scale'])
        profiles['560']['canvas'][1] = question['canvas'][1]
        profiles['560']['question_top'] = question['question_top']
        output['contexts'][key] = dict(person=who, input_profiles=signature(raw), profiles=profiles)
    authored = read('room13-dialogue-pose-source-art.json')['people']['seryeon']['pose_profiles']
    for pose in ('chair_listen', 'chair_read'):
        p = authored[pose]['profiles']['840']
        feet = [f['offset'][1] + alpha_bounds(f['file'])[3] * f.get('scale', 1.0) for f in p['frames'].values()]
        output['question_poses']['seryeon:' + pose] = dict(height=840, profile=signature({'840': p})['840'], top=math.floor(708 - max(feet)))
    # 웹판은 이미지의 pygame Surface에 직접 접근하지 못할 수 있다. 원본 픽셀
    # 기준 경계를 함께 싣고, preserved_840도 같은 메타데이터로 배치한다.
    for section in ('people', 'contexts'):
        for entry in output[section].values():
            for profile in entry['profiles'].values():
                for frame in profile['frames'].values():
                    frame['source_alpha_bounds'] = list(alpha_bounds(frame['file']))
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = json.dumps(build(), ensure_ascii=False, indent=2) + '\n'
    if args.check:
        if not OUT.exists() or OUT.read_text() != result:
            raise SystemExit('대화 크기표가 현재 승인 원본·프로필과 다릅니다. build_dialogue_size_fit.py로 갱신하세요.')
    else:
        OUT.write_text(result)
    print('대화69명·문맥10종 크기표 검증 완료' if args.check else str(OUT))


def refresh_if_present():
    """정면/다람 원본 재납품 도구가 크기표도 함께 갱신하게 한다. 준비만 할 때는 호출하지 않는다."""
    if OUT.exists():
        alpha_bounds.cache_clear()
        OUT.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
