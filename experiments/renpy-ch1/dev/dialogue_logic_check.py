"""대사 논리 자동 검사 (2026-10-23 소유자: 개선할 것을 싸게 찾는 방법).

1~14일 대사 다듬기에서 사람이 읽고서야 찾은 유형을 기계로 먼저 거른다.
결과는 후보 목록이다. 분기 때문에 실제로는 문제가 아닐 수 있으므로 show 로 확인한다.

  A 이름 소개 전 사용   어떤 이름이 처음 나온 줄이 아빠의 말·지문·생각이다(누가 알려 준 적 없음).
  B 죽은 사람이 말함    죽을 수 있는 인물의 더한 줄에 when 도, 호출 쪽 생존 확인 if 도 없다.
                        r13_nw_added_line 은 죽은 화자를 만나면 예외로 멈추므로 진행 막힘이 된다.
  C 결과 지문 중복      같은 날 같은 결과 조건(partial/lose/win/fail)의 지문이 서로 다른 줄에 붙었다.

  python3 dev/dialogue_logic_check.py
"""
import collections
import contextlib
import io
import json
import re
from pathlib import Path

import dialogue_day as dd

GAME = dd.GAME
NW = GAME / 'v111/newworld'


def speakers():
    src = (GAME / 'room13_v111_source_cast.rpy').read_text()
    names = dict(re.findall(r'"([^"]+)"\s*:\s*"([a-z_0-9]+)"', src.split('MS14_SPEAKERS', 1)[1].split('}', 1)[0]))
    later = (GAME / 'room13_v111_later_bindings.rpy').read_text()
    for block in re.findall(r'MS14_SPEAKERS\.update\(\{(.*?)\}\)', later, re.S):
        names.update(re.findall(r'"([^"]+)"\s*:\s*"([a-z_0-9]+)"', block))
    return names


def life_flags():
    src = (GAME / 'room13_v111.rpy').read_text()
    return dict(re.findall(r'"([a-z_0-9]+)":"([A-Za-z_:0-9]+)"', src.split('def r13_v111_person_alive', 1)[1].split('return', 1)[0]))


def day_lines(day):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        dd.show(day)
    out = []
    for line in buf.getvalue().splitlines():
        m = re.match(r'\s*\+?(\S+?)(?: \((앞|뒤|블록)\))?(?:\{([^}]*)\})? ([^:]{1,14}): (.*)', line)
        if m:
            out.append(dict(id=m.group(1), when=m.group(3), who=m.group(4), text=m.group(5)))
        elif out and line.strip() and not line.startswith('#'):
            # 대사 안 줄바꿈(\n, 2026-10-28 템포 손질)은 다음 줄로 찍힌다. 앞 줄에 이어 붙여야 둘째 줄의 이름도 센다
            out[-1]['text'] += ' ' + line.strip()
    return out


# 사람이 확인한 이름 첫 언급(2026-10-23): 같은 줄에서 누군가 알려 주거나 명단에서 읽는다.
NAME_REVIEWED = {
    (11, 'NW_DLG_D11_01', '굴돌'),   # 엄마가 같은 줄에서 일러 준다
    (12, 'NW_D12_S01_A01', '새미'),  # 대피 명단에 적힌 이름을 읽는다
}


def check_names(names):
    told = {}
    first_by_dad = []
    # 엄마·할머니·촌장·선생님은 호칭이라 소개 없이 불러도 된다
    roles = {'엄마', '아빠', '할머니', '촌장', '선생님', '사자 선생님', '부엉이'}
    plain = [n for n in names if len(n) >= 2 and n not in roles and not re.search(r'[0-9 ]|아이|주민|대원|담당|종업원', n)]
    for day in range(1, 15):
        for row in day_lines(day):
            for n in plain:
                if n in told:
                    continue
                # 부르는 꼴(솜이→솜아, 도담→도담아)도 이름을 알려 준 것으로 본다
                stem = n[:-1] if n.endswith('이') else n
                pat = r'(?<![가-힣])(' + re.escape(n) + r'|' + re.escape(stem) + r'아(?=[ ,.…!?]))'  # 뒤 조사는 가리지 않는다(네로한테, 도토예요)
                if re.search(pat, row['text']):
                    if (day, row['id'], n) in NAME_REVIEWED:
                        told[n] = (day, row['id'], row['who'])
                        continue
                    told[n] = (day, row['id'], row['who'])
                    if row['who'] in ('아빠', '지문', '아빠(생각)'):
                        first_by_dad.append((day, row['id'], n, row['who'], row['text'][:50]))
    return first_by_dad


def call_guards():
    """원문 ID -> 그 호출을 감싼 if 조건들의 글자."""
    guards = collections.defaultdict(str)
    for f in GAME.glob('room13_v111*.rpy'):
        lines = f.read_text().split('\n')
        for i, line in enumerate(lines):
            if 'r13_v111_lines(' not in line:
                continue
            ind = len(line) - len(line.lstrip())
            ctx = []
            for j in range(i - 1, -1, -1):
                prev = lines[j]
                if not prev.strip():
                    continue
                pind = len(prev) - len(prev.lstrip())
                if pind < ind:
                    ctx.append(prev.strip())
                    ind = pind
                    if prev.startswith('label'):
                        break
            for rid in re.findall(r"MS14_\w+", line):
                guards[rid] += ' '.join(ctx)
    return guards


# 라벨 이름으로 생존이 보장되는 경로. 7일 예방(prevent) 경로에서는 부엉이가 산다(route7).
SAFE_ROUTE = {'OWL_ALIVE': ('prevent', 'alive')}


# 사람이 경로를 따라가 확인한 줄(2026-10-23). 새로 생긴 후보만 보이게 한다.
REVIEWED = {
    'NW_D10_P01_L08': '10일 예방 경로 회의(prevent_hearing10) 안의 오답 줄. 부엉이 생존 경로',
    'NW_D10_P01_P03': '10일 예방 경로 회의 안의 오답 줄. 부엉이 생존 경로',
    'NW_D10_P01_V02': '10일 예방 경로 회의 안의 답변 줄. 부엉이 생존 경로',
    'NW_D10_P01_T21': '10일 예방 경로 회의 안의 맞장구 줄. 부엉이 생존 경로',
    'NW_D10_P01_T29': '10일 예방 경로 회의 안의 맞장구 줄. 부엉이 생존 경로',
}


def death_points():
    """사망 값 -> (날, 장면) 중 가장 이른 것. 원문 기록의 set ... false 에서 읽는다."""
    recs = json.loads((GAME / 'v111/records.json').read_text())['records']
    out = {}
    for rid, rec in recs.items():
        for op in rec.get('operations', []) + rec.get('effects', []):
            if isinstance(op, dict) and op.get('op') == 'set' and op.get('value') is False:
                m = re.match(r'MS14_D(\d\d)_(\w+?)_L', rid)
                key = (int(m.group(1)), m.group(2))
                if op['field'] not in out or key < out[op['field']]:
                    out[op['field']] = key
    return out


def check_dead_speakers(names, life):
    guards = call_guards()
    deaths = death_points()
    when_src = (GAME / 'room13_v111_newworld_text.rpy').read_text()
    out = []
    for path in sorted(NW.glob('d*.json')):
        day = int(path.stem[1:])
        part = json.loads(path.read_text())
        for where in ('before', 'after'):
            for rid, rows in part[where].items():
                for row in rows:
                    person = names.get(row.get('speaker') or '')
                    if person not in life:
                        continue
                    flag = life[person]
                    cond = row.get('when', '')
                    cond_src = re.search(r'"%s":lambda:([^\n]*)' % re.escape(cond), when_src) if cond else None
                    texts = (cond_src.group(1) if cond_src else '') + guards.get(rid, '')
                    if flag in texts or person in texts or 'alive' in cond or 'alive' in guards.get(rid, '') \
                            or any(w in guards.get(rid, '') for w in SAFE_ROUTE.get(flag, ())):
                        continue
                    # 사망이 설정되는 장면보다 앞이면 아직 살아 있다
                    death = deaths.get(flag)
                    scene = re.match(r'MS14_D\d\d_(\w+?)_L', rid)
                    if death is None or (day, scene.group(1) if scene else '') < death:
                        continue
                    if row.get('id') in REVIEWED:
                        continue
                    out.append((day, row.get('id'), row['speaker'], cond or '-', row['text'][:40]))
    return out


# 사람이 경로를 따라가 확인한 결과 지문 묶음(2026-10-23). 각 오답 라벨은 마지막 기회일 때만 회의를
# 끝내고 곧장 마무리 선택으로 넘어가므로, 같은 조건 지문은 한 판에 한 번만 나온다.
OUTCOME_REVIEWED = {
    ('d03', 'lamp_lose'): '회의 결과(S05)와 다음 장면(S06)의 뒷모습',
    ('d03', 'lamp_partial'): 'knife_wrong 과 trial_wrong 은 서로 다른 마지막 기회',
    ('d10', 'records_lose'): '오답 라벨마다 마지막 기회일 때 한 번',
    ('d10', 'room13_lose'): 'H/P 는 다른 경로, S04 는 다음 장면의 뒷모습',
    ('d10', 'room13_partial_unknown'): 'O/T 는 다른 경로',
    ('d11', 'room13_lose'): '아침(S00)과 뒤 장면(S02)의 뒷모습',
}


def check_outcomes():
    out = []
    for path in sorted(NW.glob('d*.json')):
        part = json.loads(path.read_text())
        seen = collections.defaultdict(list)
        for where in ('before', 'after'):
            for rid, rows in part[where].items():
                for row in rows:
                    cond = row.get('when', '')
                    if row.get('speaker') is None and re.search(r'partial|lose|win|fail', cond):
                        seen[cond].append((rid, row.get('id')))
        for cond, items in seen.items():
            anchors = {r for r, _ in items}
            if len(anchors) > 1 and (path.stem, cond) not in OUTCOME_REVIEWED:
                out.append((path.stem, cond, sorted(i for _, i in items)))
    return out


if __name__ == '__main__':
    names = speakers()
    life = life_flags()
    a = check_names(names)
    b = check_dead_speakers(names, life)
    c = check_outcomes()
    print(f'A 이름 소개 전 사용 {len(a)}건')
    for day, rid, n, who, text in a:
        print(f'  {day}일 {rid} {n} ({who}): {text}')
    print(f'B 죽을 수 있는 인물의 무조건 대사 {len(b)}건')
    for day, rid, who, cond, text in b:
        print(f'  {day}일 {rid} {who} when={cond}: {text}')
    print(f'C 같은 결과 조건 지문이 여러 줄에 {len(c)}건')
    for day, cond, ids in c:
        print(f'  {day} {cond}: {", ".join(ids)}')
