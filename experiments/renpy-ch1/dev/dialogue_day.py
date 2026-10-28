"""하루치 대본 뽑기·대사 수정 반영 (2026-10-23 소유자: "하루씩 대사 체크하고 수정해줘").

대사 검수는 원문(records.json)과 날짜별 패치(newworld/dNN.json)를 머릿속에서 합쳐
읽어야 해서 비싸고 틀리기 쉬웠다. 실제 재생 순서대로 한 줄씩 합쳐 보여 주고,
고칠 때는 "ID -> 새 문장"만 적으면 패치의 알맞은 자리에 넣는다.

  python3 dev/dialogue_day.py show 7            7일 대본(장면 제목, 화자, 조건 포함)
  python3 dev/dialogue_day.py show 7 --tag D07-OWL   그 사건(docs/design/EVENT_TAGS.md)만
  python3 dev/dialogue_day.py apply 7 EDITS.json [--dry]

EDITS.json 은 [{"ref": "...", "text": "..."}] 목록이다.
  ref = MS14_D07_S01_L0047          원문 줄의 기본 문장(조건 없는 교체)
  ref = MS14_D07_S01_L0047{fire_lose} 그 조건의 교체 변형
  ref = NW_D07_OR01                 패치가 더한 줄(before/after/blocks)
  ref = S01_L0047                   그 날의 짧은 ID(show 출력 그대로)도 된다
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'game'
SRC = ROOT / 'docs/story-ms14/source/다람탐정_제작기준본01_대사연출조건.json'


def load(day):
    recs = json.loads((GAME / 'v111/records.json').read_text())['records']
    path = GAME / f'v111/newworld/d{day:02d}.json'
    patch = json.loads(path.read_text())
    return recs, path, patch


def shown_ids():
    # 화면에 나오는 줄은 r13_v111_lines([...]) 안에 있는 ID 뿐이다. commit 만 되는 줄은
    # 진행 기록용 연출 메모("조작: ...")라 읽거나 고칠 대상이 아니다.
    ids = set()
    for f in GAME.glob('*.rpy'):
        for call in re.findall(r"r13_v111_lines\(\[([^\]]*)\]", f.read_text()):
            ids.update(re.findall(r"MS14_\w+", call))
    return ids


def carriage_text():
    m = re.search(r"R13_V111_CARRIAGE_TEXT = \{(.*?)\n    \}", (GAME / 'room13_v111.rpy').read_text(), re.S)
    return dict(re.findall(r'"(MS14_\w+)": "([^"]*)"', m.group(1))) if m else {}


def scenes():
    out = {}
    try:
        for s in json.loads(SRC.read_text())['scenes']:
            out[s['scene_id']] = f"{s.get('title','')} ({s.get('location','')})"
    except (OSError, KeyError, ValueError):
        pass
    return out


def variants(entry):
    if entry is None:
        return []
    return [entry] if isinstance(entry, dict) else entry


def who(row, base_speaker=None):
    kind = row.get('kind')
    if kind in ('action', 'narration') or (kind is None and not (row.get('speaker') or base_speaker)):
        return '지문'
    if kind == 'thought':
        return f"{row.get('speaker') or base_speaker or '아빠'}(생각)"
    if kind in ('system', 'evidence', 'choice'):
        return {'system': '안내', 'evidence': '자료', 'choice': '선택'}[kind]
    return row.get('speaker') or base_speaker or '?'


def show(day, tag=None):
    recs, _, patch = load(day)
    only = None
    if tag:
        # 사건 태그(docs/design/event_tags.json)의 장면만 보인다
        only = set(json.loads((ROOT / 'docs/design/event_tags.json').read_text())['events'][tag]['scenes'])
    titles = scenes()
    prefix = f'MS14_D{day:02d}_'
    drops = {}
    for item in patch.get('drop', []):
        rid, when = (item, 'always') if isinstance(item, str) else (item.get('id'), item.get('when', 'always'))
        drops[rid] = when
    added = lambda rows, where, rid: [
        f"  +{r.get('id','?')} ({where}){'{'+r['when']+'}' if r.get('when') else ''} {who(r)}: {r.get('text','')}"
        for r in rows]
    shown, carriage = shown_ids(), carriage_text()
    scene = None
    lines = []
    for rid, rec in recs.items():
        if not rid.startswith(prefix) or rid not in shown:
            continue
        if only is not None and rid.rsplit('_', 1)[0] not in only:
            continue
        if rid in carriage:
            rec = dict(rec, text=carriage[rid])
        sid = rid.rsplit('_', 1)[0]
        if sid != scene:
            scene = sid
            lines.append(f"\n## {sid[5:]} {titles.get(sid,'')}")
        lines += added(patch['before'].get(rid, []), '앞', rid)
        short = rid[len(prefix):]
        vs = variants(patch['replace'].get(rid))
        default = next((v for v in vs if not v.get('when')), None)
        text = (default or rec).get('text', '')
        mark = ''
        if rid in drops:
            mark = ' [삭제]' if drops[rid] == 'always' else f" [삭제{{{drops[rid]}}}]"
        if drops.get(rid) != 'always':
            lines.append(f"{short} {who(rec)}: {text}{mark}")
        for v in vs:
            if v.get('when'):
                lines.append(f"{short}{{{v['when']}}} {who(rec)}: {v.get('text','')}")
        lines += added(patch['after'].get(rid, []), '뒤', rid)
    for name, rows in patch.get('blocks', {}).items():
        lines.append(f"\n## 블록 {name}")
        lines += added(rows, '블록', name)
    print('\n'.join(lines).strip())


def apply(day, edits_path, dry=False):
    recs, path, patch = load(day)
    edits = json.loads(Path(edits_path).read_text())
    shown = shown_ids()
    rows_by_id = {}
    for where in ('before', 'after', 'blocks'):
        for rows in patch.get(where, {}).values():
            for r in rows:
                if r.get('id'):
                    rows_by_id[r['id']] = r
    done, problems = 0, []
    for e in edits:
        ref, text = e['ref'], e['text'].strip()
        if re.match(r'[A-Z]\w*?_L\d{4}', ref) and not ref.startswith(('MS14_', 'NW_')):
            ref = f'MS14_D{day:02d}_' + ref
        if not text:
            problems.append(f'{ref}: 빈 문장')
            continue
        if re.search(r'(?<!…)…(?!…)', text) or '...' in text:
            problems.append(f'{ref}: 말줄임표는 …… 하나로 쓴다(VOICE_GUIDE 1)')
            continue
        m = re.fullmatch(r'(MS14_\w+?)(?:\{(\w[\w:]*)\})?', ref)
        if ref in rows_by_id:
            # 엔진이 생각 줄에 괄호를 붙인다. 괄호째 넣으면 게임 시작 때 새 세계 글 검사가 멈춘다(2026-10-28)
            if rows_by_id[ref].get('kind') == 'thought' and text.startswith('('):
                problems.append(f'{ref}: 생각 줄은 괄호 없이 쓴다')
                continue
            rows_by_id[ref]['text'] = text
            if e.get('speaker'):
                rows_by_id[ref]['speaker'] = e['speaker']
        elif m and m.group(1) in recs and m.group(1) not in shown:
            problems.append(f'{ref}: 화면에 나오지 않는 줄(연출 메모)')
            continue
        elif m and m.group(1) in recs:
            rid, when = m.group(1), m.group(2)
            vs = variants(patch['replace'].get(rid))
            target = next((v for v in vs if v.get('when') == when), None)
            if target is not None:
                target['text'] = text
            elif when:
                problems.append(f'{ref}: 그 조건의 변형이 없음')
                continue
            else:
                # 조건 변형은 앞에서 먼저 맞으면 이긴다. 조건 없는 기본은 맨 뒤에 둔다.
                new = {'text': text}
                if not vs:
                    patch['replace'][rid] = new
                else:
                    patch['replace'][rid] = vs + [new]
        else:
            problems.append(f'{ref}: 찾을 수 없는 ID')
            continue
        done += 1
    print(f'반영 {done}건, 문제 {len(problems)}건')
    for p in problems:
        print('  ', p)
    if not dry and not problems:
        path.write_text(json.dumps(patch, ensure_ascii=False, indent=2) + '\n')
    elif problems:
        print('문제가 있어 파일을 바꾸지 않았다.')
        sys.exit(1)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'show':
        show(int(sys.argv[2]), sys.argv[sys.argv.index('--tag') + 1] if '--tag' in sys.argv else None)
    elif cmd == 'apply':
        apply(int(sys.argv[2]), sys.argv[3], '--dry' in sys.argv)
    else:
        print(__doc__)
