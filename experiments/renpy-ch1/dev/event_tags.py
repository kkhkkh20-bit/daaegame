"""사건 태그 (2026-10-23 소유자: "각 사건 태그를 걸어서 쉽게 구분하고 정리해 보자").

검수·버그 보고·지시서에서 "어느 사건인지"를 한 이름으로 부르기 위한 표다.
줄 번호는 하루에도 밀리므로 태그는 장면 ID와 라벨에 붙인다.

  사건 태그  D07-OWL 처럼 날짜-이름. 장면(MS14_D07_S03 등) 묶음이다.
  세부 분기  분기 지도 PDF·엑셀(0.20.15)의 ID. 사건 태그 아래에 둔다.

라벨의 사건은 (1) 회의 라벨이면 그 회의, (2) 라벨 안 대사 줄의 장면,
(3) 라벨 안 r13_v111_scene 호출, (4) 같은 파일 바로 앞 라벨 순으로 정한다.

  python3 dev/event_tags.py           표 문서와 JSON 을 다시 쓰고, 태그 없는 라벨을 보고한다
  python3 dev/event_tags.py D07-OWL   그 사건의 장면·회의·라벨
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'game'
OUT_JSON = ROOT / 'docs/design/event_tags.json'
OUT_MD = ROOT / 'docs/design/EVENT_TAGS.md'

# 태그: (이름, 장면들, 회의 키)
EVENTS = {
    'D01-CARRIAGE': ('마차 · 엄마의 편지', ['S01'], None),
    'D01-GATE': ('초소 입장 · 둘이 들어갈 근거', ['S02', 'S03', 'S04'], 'gate'),
    'D01-ROOM13': ('빈 13호 · 기다리지 않는 방', ['S05'], None),
    'D02-BOX': ('광장 · 초롱과 교환함', ['S01'], None),
    'D02-POST': ('우체국 · 누가 부친 편지인가', ['S02'], None),
    'D02-PIKO': ('초상 의뢰 · 피코 숙소 선택', ['S03', 'S04'], None),
    'D02-NIGHT': ('여관 · 설명할 수 없는 빈칸', ['S05'], None),
    'D03-PIKO': ('아침 · 피코 생사 확정', ['S01'], None),
    'D03-LAMP': ('3번 등 사건 · 조사와 회의', ['S02', 'S03', 'S04', 'S05'], 'lamp'),
    'D03-EVENING': ('저녁 · 그려지지 않은 얼굴', ['S06'], None),
    'D04-SOMI': ('솜이네 · 닫힌 뒷문', ['S01'], None),
    'D04-KIDS': ('처마 · 아이들의 증언', ['S02'], None),
    'D04-POST': ('초소 뒤 비명 · 문기둥 사건', ['S03', 'S04'], None),
    'D05-BAMI': ('밤이 혐의 · 초소 회의', ['S01', 'S02', 'S03'], 'gate_post'),
    'D05-WARNING': ('이제 도착한 경고 편지', ['S04'], None),
    'D05-NIGHT': ('저녁 · 맡긴다는 말', ['S05'], None),
    'D06-FIRE': ('창고 아이들 · 오늘 옮길까 내일 데려올까', ['S01', 'S02', 'S03', 'S03P', 'S04', 'P01'], None),
    'D07-FIRE': ('화재 회의 · 누가 불을 놓았나', ['S01', 'S02'], 'fire'),
    'D07-OWL': ('밤의 갈림길 · 부엉이 생사', ['S03', 'S04', 'P01', 'P02'], None),
    'D08-MURDER': ('살인 경로 · 13호 현장 조사', ['S01', 'S02', 'S03'], None),
    'D08-PREVENT': ('예방 경로 · 진료소', ['P01'], None),
    'D08-LETTER': ('등 관리함 · 엄마의 편지', ['S04'], None),
    'D09-PASSAGE': ('숨은 통로 · 주방과 책장', ['S01'], None),
    'D09-PIN': ('핀과 스카프 · 공방과 식당', ['S02', 'S03'], None),
    'D09-POST': ('우체국 · 누가 부쳤는가', ['S04'], None),
    'D09-PREVENT': ('예방 경로 · 침입과 위조', ['P01'], None),
    'D10-ROOM13': ('13호 회의 · 부엉이에게 무슨 일이', ['S01', 'S02', 'S03'], 'room13'),
    'D10-RECORDS': ('기록 회의 · 누가 기록을 받아야 하나', ['P01'], 'records'),
    'D10-AFTER': ('회의 뒤 · 다음에 갈 곳', ['S04', 'S04P'], None),
    'D11-REUNION': ('펌프와 빈 뿌리 집 · 엄마 재회', ['S00', 'S01', 'S02', 'S02A', 'S02B'], None),
    'D11-HYP': ('시설의 열 · 가설 회의', ['S03'], 'hypothesis'),
    'D11-NERO': ('문이 열려 있어야 하는 밤 · 네로 생사', ['S04'], None),
    'D12-SOUP': ('배식 · 아이들이 먹은 수프', ['S01', 'S02', 'S03', 'S04', 'S05', 'A', 'B'], 'soup'),
    'D13-BLANKET': ('판돌의 담요 · 담요 회의', ['S01', 'S02', 'S03'], 'blanket'),
    'D13-FAMILY': ('가족 셋의 하룻밤 · 가족 우선', ['A'], None),
    'D13-CART': ('수레와 인계 · 피코 사건', ['S04', 'B'], 'piko'),
    'D13-CROWD': ('사람을 끌어내리는 손 · 군중 폭력', ['C'], None),
    'D14-ALTAR': ('제단 회의 · 장치', ['S01', 'S02'], 'altar'),
    'D14-GRANNY': ('보미라는 이름 · 할머니 면담', ['S03'], None),
    'D14-NAMES': ('이름판 아래의 그릇', ['S04'], None),
    'D14-ENDING': ('엄마 몫 과자 · 결말', ['S05', 'END_FAMILY', 'END_PARTIAL', 'END_VIOLENCE'], None),
    'COMMON': ('공통 장치 · 대기·증거 제출·이동', [], None),
}

# 분기 지도 PDF(0.20.15, 5f6654e)의 세부 분기 ID -> 사건 태그. 라벨은 그 커밋의 줄 범위에서 한 번 뽑아 고정했다.
BRANCH_PARENT = {
    'D01-GATE': 'D01-GATE', 'D02-PIKO': 'D02-PIKO', 'D03-LAMP': 'D03-LAMP', 'D03-STONE': 'D03-LAMP',
    'D04-SILUK': 'D04-SOMI', 'D05-BAMI': 'D05-BAMI', 'D06-FIRE': 'D06-FIRE', 'D07-FIRE': 'D07-FIRE',
    'D07-OWL': 'D07-OWL', 'D10-MEETINGS': None, 'D11-DAY': 'D11-HYP', 'D11-HYP': 'D11-HYP',
    'D11-NERO': 'D11-NERO', 'D12-SOUP': 'D12-SOUP', 'D13-FAMILY': 'D13-FAMILY', 'D13-BLANKET': 'D13-BLANKET',
    'D13-PIKO': 'D13-CART', 'D13-POSITION': 'D13-CART', 'D13-HANDOVER': 'D13-CART', 'D13-CHAIN': 'D13-CART',
    'D13-CROWD': 'D13-CROWD', 'D14-ENDING': 'D14-ENDING', 'D14-ALTAR': 'D14-ALTAR', 'D14-EPILOGUE': 'D14-ENDING',
}


# 장면보다 분기 목록을 앞세우는 분기. 가족 제안은 담요 장면 안에서, 결말 판정은 14일 아침 장면 안에서
# 이뤄져 장면으로만 보면 다른 사건에 묶인다.
BRANCH_FIRST = ('D13-FAMILY', 'D14-ENDING', 'D14-EPILOGUE')


def scene_tag():
    out = {}
    for tag, (_, scenes, _) in EVENTS.items():
        day = tag[:3]
        if not day.startswith('D'):
            continue
        for s in scenes:
            out[f'MS14_{day}_{s}'] = tag
    return out


def meetings():
    src = (GAME / 'room13_v111_meeting_stage.rpy').read_text()
    block = src.split('R13_NW_MEETINGS={', 1)[1].split('\n    }', 1)[0]
    out = {}
    for key, labels in re.findall(r"'(\w+)':dict\(.*?labels=\[([^\]]*)\]", block, re.S):
        for l in re.findall(r"'(\w+)'", labels):
            out['r13_v111_' + l] = key
    return out


def label_tags():
    s2t = scene_tag()
    m2t = {m: t for t, (_, _, m) in EVENTS.items() if m}
    meet = meetings()
    frozen = json.loads(OUT_JSON.read_text()).get('branches', {}) if OUT_JSON.exists() else {}
    first = {l: BRANCH_PARENT[b] for b in BRANCH_FIRST for l in frozen.get(b, [])}
    out, why, leftovers = {}, {}, {}
    for f in sorted(GAME.glob('room13_v111*.rpy')):
        prev = None
        cur = None
        body = {}
        for line in f.read_text().split('\n'):
            m = re.match(r'label (\w+)', line)
            if m:
                cur = m.group(1)
                body[cur] = ''
                continue
            if cur and (line.startswith(' ') or not line.strip()):
                body[cur] += line + '\n'
            elif line.strip() and not line.startswith(' '):
                cur = None
        pending = []
        for label, text in body.items():
            tag = reason = None
            if label in meet and meet[label] in m2t:
                tag, reason = m2t[meet[label]], '회의'
            if not tag and label in first:
                tag, reason = first[label], '분기 목록'
            if not tag:
                for rid in re.findall(r'MS14_(D\d\d_[A-Z0-9]+?)_L\d{4}', text):
                    t = s2t.get('MS14_' + rid)
                    if t:
                        tag, reason = t, '대사 줄'
                        break
            if not tag:
                m = re.search(r"r13_v111_scene\('(MS14_\w+)'\)", text)
                if m and m.group(1) in s2t:
                    tag, reason = s2t[m.group(1)], '장면 호출'
            day = re.search(r'(\d+)$', label)
            if not tag and prev and not (day and prev.startswith('D') and int(prev[1:3]) != int(day.group(1))):
                tag, reason = prev, '앞 라벨'
            if not tag and f.name == 'room13_v111.rpy':
                tag, reason = 'COMMON', '공통 장치'
            if tag:
                out[label], why[label] = tag, reason
                prev = tag
            else:
                pending.append(label)
                continue
            # 그날 시작 라벨처럼 앞에서 정하지 못한 것은 바로 뒤 라벨을 따른다
            for p in pending:
                out[p], why[p] = tag, '뒤 라벨'
            pending.clear()
        leftovers.update({p: body[p] for p in pending})
    # 파일 끝에서 다른 파일로 넘어가는 라벨(예: morning6 -> day6)은 넘어가는 곳을 따른다
    for label, text in leftovers.items():
        m = re.search(r'jump (\w+)', text)
        if m and m.group(1) in out:
            out[label], why[label] = out[m.group(1)], '이동 대상'
    return out, why


def build():
    labels, why = label_tags()
    old = json.loads(OUT_JSON.read_text()) if OUT_JSON.exists() else {}
    branches = old.get('branches', {})
    data = dict(
        note='dev/event_tags.py 가 만든다. 손으로 고치지 말고 EVENTS 표를 고친 뒤 다시 돌린다.',
        events={t: dict(name=n, scenes=[f'MS14_{t[:3]}_{s}' for s in sc], meeting=m,
                        branches=sorted(b for b, p in BRANCH_PARENT.items() if p == t),
                        labels=sorted(l for l, x in labels.items() if x == t)) for t, (n, sc, m) in EVENTS.items()},
        labels=labels, branches=branches)
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n')
    lines = ['# 사건 태그', '',
             '소유자 지시(2026-10-23): "각 사건 태그를 걸어서 쉽게 구분하고 정리해 보자." 검수·버그 보고·지시서에서 사건을 이 이름으로 부른다.',
             '', '- 사건 태그는 장면 ID 묶음이다. 줄 번호가 바뀌어도 그대로다.',
             '- 세부 분기 ID는 분기 지도 PDF·엑셀(0.20.15)의 ID다. 사건 태그 아래에 묶었다.',
             '- 표는 `python3 dev/event_tags.py`가 만든다(`docs/design/event_tags.json`). 하루치 대본을 사건만 보려면 `python3 dev/dialogue_day.py show 7 --tag D07-OWL`.',
             '', '| 태그 | 사건 | 장면 | 회의 | 세부 분기(PDF·엑셀) | 라벨 수 |', '|---|---|---|---|---|---|']
    for t, e in data['events'].items():
        sc = ', '.join(s.split('_', 2)[2] for s in e['scenes'])
        lines.append(f"| `{t}` | {e['name']} | {sc} | {e['meeting'] or ''} | {', '.join(e['branches'])} | {len(e['labels'])} |")
    lines += ['', '`D10-MEETINGS`(PDF)는 두 회의를 함께 가리킨다. 여기서는 `D10-ROOM13`(살인 경로)과 `D10-RECORDS`(예방 경로)로 나눴다.', '']
    OUT_MD.write_text('\n'.join(lines))
    total = sum(1 for f in GAME.glob('room13_v111*.rpy') for _ in re.finditer(r'^label ', f.read_text(), re.M))
    print(f'사건 {len(EVENTS)}개, 라벨 {len(labels)}/{total}개 태그')
    counts = {}
    for r in why.values():
        counts[r] = counts.get(r, 0) + 1
    print('판정 근거', counts)
    return labels, total


if __name__ == '__main__':
    if len(sys.argv) > 1:
        data = json.loads(OUT_JSON.read_text())
        e = data['events'][sys.argv[1]]
        print(sys.argv[1], e['name'], '| 장면', ' '.join(e['scenes']), '| 회의', e['meeting'], '| 분기', ' '.join(e['branches']))
        print(' '.join(l.replace('r13_v111_', '') for l in e['labels']))
    else:
        build()
