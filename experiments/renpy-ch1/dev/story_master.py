"""이야기 총정리표 · 코드에서 자동으로 뽑는 부분 (소유자 2026-10-24: "그래야 다른 채팅이 이어받지").

다른 채팅·Codex가 대사·분기·회의·결말을 코드를 다 읽지 않고 파악하도록, 게임 코드와 데이터를
읽어 docs/design/story_master_auto.md 를 쓴다. 사람이 쓰는 부분은 docs/design/story_master.md.

  python3 dev/story_master.py            표준 출력으로 보여 준다
  python3 dev/story_master.py --write    docs/design/story_master_auto.md 에 쓴다

표준 라이브러리만 쓴다. 게임을 띄우지 않고 글자로 읽으므로 완벽하지 않다. 읽지 못한 자리는
「자동 추출 실패: 파일:줄」로 남긴다(조용히 빼면 빠진 줄 모르고 믿게 된다).
실행할 때마다 같은 결과가 나오게 파일 안 순서 · 이름순으로만 늘어놓는다(시각·난수 없음).
"""
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'game'
OUT = ROOT / 'docs/design/story_master_auto.md'
SRC = ROOT / 'docs/story-ms14/source/다람탐정_제작기준본01_대사연출조건.json'
DAY_FILES = ['room13_v111_days123.rpy', 'room13_v111_days45.rpy', 'room13_v111_days610.rpy', 'room13_v111_days1114.rpy', 'room13_v111_owl_prevent.rpy','room13_hidden_pandol.rpy','room13_hidden_base.rpy']
RULES = GAME / 'room13_v111_newworld_rules.rpy'
TEXT = GAME / 'room13_v111_newworld_text.rpy'
FORK = GAME / 'room13_fork_screen.rpy'

FAIL = []


def fail(path, line, why):
    FAIL.append((Path(path).name, line, why))


def rel(path):
    return Path(path).name


# ---------------------------------------------------------------- 공통 읽기

def balanced(text, start):
    """text[start] 가 여는 괄호일 때 짝이 맞는 닫는 괄호까지(따옴표 안은 건너뜀)."""
    pairs = {'(': ')', '[': ']', '{': '}'}
    stack = []
    quote = None
    i = start
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == '\\':
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in '\'"':
            quote = ch
        elif ch == '#':
            nl = text.find('\n', i)
            i = len(text) if nl < 0 else nl
            continue
        elif ch in pairs:
            stack.append(pairs[ch])
        elif stack and ch == stack[-1]:
            stack.pop()
            if not stack:
                return text[start:i + 1]
        i += 1
    return None


def call_args(line, name):
    """한 줄에서 name(...) 호출의 인자를 파이썬 값으로. 못 읽으면 None."""
    at = line.find(name + '(')
    if at < 0:
        return None
    body = balanced(line, at + len(name))
    if body is None:
        return None
    try:
        node = ast.parse('f' + body, mode='eval').body
    except SyntaxError:
        return None
    out = []
    for a in node.args:
        try:
            out.append(ast.literal_eval(a))
        except ValueError:
            out.append(Expr(ast.get_source_segment('f' + body, a)))
    return out


class Expr(str):
    """리터럴이 아닌 인자(식). 그대로 글자로 보인다."""


def strip_comment(s):
    quote = None
    for i, ch in enumerate(s):
        if quote:
            if ch == quote:
                quote = None
        elif ch in '\'"':
            quote = ch
        elif ch == '#':
            return s[:i].rstrip()
    return s.rstrip()


def literal_after(text, marker, path):
    """`marker` 뒤에 오는 리터럴(dict/tuple) 또는 dict(...) 호출을 값으로."""
    at = text.find(marker)
    if at < 0:
        fail(path, 0, '찾지 못함: ' + marker)
        return None
    i = at + len(marker)
    while text[i] in ' \t':
        i += 1
    if text.startswith('dict(', i):
        body = balanced(text, i + 4)
        node = ast.parse('dict' + body, mode='eval').body
        return {k.arg: ast.literal_eval(k.value) for k in node.keywords}
    body = balanced(text, i)
    try:
        return ast.literal_eval(body)
    except (ValueError, SyntaxError, TypeError):
        fail(path, text[:at].count('\n') + 1, '값을 읽지 못함: ' + marker)
        return None


def func_source(text, name):
    m = re.search(r'^( *)def ' + re.escape(name) + r'\(.*?(?=^\1(?:def |[A-Za-z_]\w*\s*=|#)|\Z)', text, re.S | re.M)
    if not m:
        return None
    lines = m.group(0).rstrip().splitlines()
    pad = len(m.group(1))
    return '\n'.join(l[pad:] for l in lines)


def names_table():
    """인물 id → 한글 이름. R13_NAMES 를 만드는 dict(...)/update(...) 를 글자로 모은다."""
    names = {}
    for f in sorted(GAME.rglob('*.rpy')):
        if 'qa_tests' in f.parts:
            continue
        t = f.read_text(errors='replace')
        for marker in ('NAMES=dict(', 'NAMES = dict(', 'NAMES = {', 'R13_NAMES.update(', 'MS14_NAMES.update('):
            for m in re.finditer(re.escape(marker), t):
                body = balanced(t, m.end() - 1)
                if body:
                    for k, v in re.findall(r'(\w+)\s*=\s*"([^"]+)"', body):
                        names.setdefault(k, v)
                    for k, v in re.findall(r'"(\w+)"\s*:\s*"([^"]+)"', body):
                        names.setdefault(k, v)
        # 화자표(한글 → id)로 남은 사람을 채운다. 같은 id 가 여럿이면 처음 것.
        for marker in ('MS14_SPEAKERS = {', 'MS14_SPEAKERS.update({'):
            for m in re.finditer(re.escape(marker), t):
                body = balanced(t, m.end() - 1)
                if body:
                    for v, k in re.findall(r'"([^"]+)"\s*:\s*"(\w+)"', body):
                        if k not in names:
                            names[k] = v
    for k, v in EXTRA_NAMES.items():
        names.setdefault(k, v)
    return names


# 코드에 이름표가 없는 id(죽음 판정에만 나온다). 이름은 대사(d11·d12)에서 부르는 말을 따랐다.
EXTRA_NAMES = {'v111_lowerroad_elder': '아랫길 노인'}


def places_table():
    places = {}
    for f in sorted(GAME.rglob('*.rpy')):
        if 'qa_tests' in f.parts:
            continue
        t = f.read_text(errors='replace')
        for marker in ('R13_PLACES = {', 'R13_PLACES={', 'R13_PLACES.update({'):
            for m in re.finditer(re.escape(marker), t):
                body = balanced(t, m.end() - 1)
                if body:
                    for k, v in re.findall(r'"(\w+)"\s*:\s*\(\s*"([^"]+)"', body):
                        places.setdefault(k, v)
        for k, v in re.findall(r'R13_PLACES\[["\'](\w+)["\']\]\s*=\s*\(\s*["\']([^"\']+)', t):
            places.setdefault(k, v)
    return places


def scene_titles():
    try:
        return {s['scene_id']: (s.get('title', ''), s.get('location', '')) for s in json.loads(SRC.read_text())['scenes']}
    except (OSError, KeyError, ValueError):
        fail(SRC, 0, '장면 원본을 읽지 못함')
        return {}


def binding_titles():
    """현장 대기(r13_v111_wait('키'))의 보기 번호 → 문구. 새 세계 패치의 titles 가 덮어쓴다."""
    try:
        b = json.loads((GAME / 'v111/field-bindings.json').read_text())
    except (OSError, ValueError):
        fail(GAME / 'v111/field-bindings.json', 0, '현장 보기 파일을 읽지 못함')
        return {}
    over = {}
    for f in sorted((GAME / 'v111/newworld').glob('d*.json')):
        for key, rows in json.loads(f.read_text()).get('titles', {}).items():
            for idx, title in rows.items():
                over[(key, int(idx))] = title
    out = {}
    for key, spec in b.items():
        rows = {}
        for ordinal, opt in enumerate(spec.get('options', [])):
            i=opt.get('index',ordinal)
            rows[opt.get('index', i)] = over.get((key, i), opt.get('title', ''))
        out[key] = rows
    return out


BINDINGS = {}


# ---------------------------------------------------------------- 날짜 파일 읽기

OP_PATTERNS = [
    ('set', 'r13_v111_set'), ('fate', 'r13_fork_set_fate'), ('list', 'r13_nw_list'),
    ('end', 'r13_nw_meeting_end'), ('retry', 'r13_nw_retry'), ('proof', 'r13_v111_proof'),
    ('block', 'r13_nw_block'), ('acquire', 'r13_nw_acquire'),
]


def parse_day_file(path):
    """라벨마다 장면·이동·인물·갈림·판정 값을 줄 순서대로 모은다."""
    lines = path.read_text(errors='replace').splitlines()
    labels = []
    cur = None
    scene = None
    i = 0
    while i < len(lines):
        raw = lines[i]
        ln = i + 1
        s = raw.strip()
        ind = len(raw) - len(raw.lstrip())
        if not s or s.startswith('#'):
            i += 1
            continue
        m = re.match(r'label (\w+)', s)
        if m and ind == 0:
            cur = dict(name=m.group(1), line=ln, scene=scene, items=[], file=rel(path), choices=None)
            labels.append(cur)
            i += 1
            continue
        if cur is None:
            i += 1
            continue
        m = re.search(r"r13_v111_scene\((['\"])(\w+)\1\)", s)
        if m:
            scene = m.group(2)
            cur['scene'] = scene
            cur['items'].append(('scene', scene, ln))
        elif 'r13_v111_scene(' in s:
            fail(path, ln, '장면 이름이 글자가 아님: ' + s)
        if 'r13_v111_travel(' in s:
            a = call_args(s, 'r13_v111_travel')
            if a and isinstance(a[0], str) and not isinstance(a[0], Expr):
                cur['items'].append(('travel', a[0], ln))
            else:
                fail(path, ln, '이동 장소를 읽지 못함')
        for kind in ('arrive', 'join'):
            if 'r13_v111_%s(' % kind in s and 'def ' not in s:
                a = call_args(s, 'r13_v111_' + kind)
                if a and isinstance(a[0], list) and not isinstance(a[0], Expr):
                    cur['items'].append((kind, a[0], ln))
                elif a and isinstance(a[0], Expr) and re.findall(r'\[([^\]]*)\]', a[0]):
                    # 목록 + 식(그날 값에 따라 한 사람 더). 글자로 적힌 사람만 넣고 식은 표시만 한다.
                    ids = re.findall(r'["\'](\w+)["\']', re.findall(r'\[([^\]]*)\]', a[0])[0])
                    ids = [x for x in ids if x not in ('guard_relief_person',)]
                    cur['items'].append((kind, ids + ['(+식)'], ln))
                else:
                    fail(path, ln, '세우는 인물을 읽지 못함(변수)')
        m = re.search(r"r13_v111_wait\((['\"])(\w+)\1\)", s)
        if m:
            cur['choices'] = BINDINGS.get(m.group(2))
            if cur['choices'] is None:
                fail(path, ln, '현장 보기 키를 찾지 못함: ' + m.group(2))
        if s.startswith('$ v111_menu=['):
            cur['choices'] = {int(n): t for t, n in re.findall(r"'([^']*)'\)?,(\d+)\)", s)}
            cur['items'].append(('vmenu', None, ln))
        m = re.search(r"v111_claim\s*=\s*['\"](menu:\w+)['\"]", s)
        if m:
            cur['items'].append(('claim', m.group(1), ln))
        for kind, name in OP_PATTERNS:
            if name + '(' in s and 'def ' + name not in s:
                a = call_args(s, name)
                if a is None:
                    fail(path, ln, '%s 인자를 읽지 못함' % name)
                else:
                    cur['items'].append((kind, a, ln))
        if re.search(r"r13_v111_set\(\s*['\"]departed_names['\"]", s) or ('departed:' in s and 'r13_v111_set' in s and 'r13_v111_set(' not in s.split('departed:')[0][-20:]):
            pass
        if re.match(r'for _p in .*departed:', s):
            cur['items'].append(('departed_loop', s, ln))
        if s == 'menu:':
            opts, _ = parse_menu(lines, i, ind, path)
            cur['items'].append(('menu', opts, ln))
            # 보기 블록 안의 값 바꾸기(생사 판정 등)도 읽도록 다음 줄부터 그대로 이어 읽는다
            i += 1
            continue
        m = re.match(r'(if|elif)\s+(.+):$', s)
        if m and not s.startswith(('"', "'")):
            cond = m.group(2)
            if cur['choices'] is not None:
                cond = re.sub(r'\b(?:v111_answer|_return)\s*==\s*(\d+)', lambda mm: '「%s」' % cur['choices'].get(int(mm.group(1)), '보기 ' + mm.group(1)), cond)
            target = block_target(lines, i, ind)
            if target is not None:
                cur['items'].append(('if', (m.group(1), cond, target), ln))
        elif s == 'else:':
            target = block_target(lines, i, ind)
            if target is not None:
                cur['items'].append(('if', ('else', '', target), ln))
        m = re.match(r'jump (\w+)$', s)
        if m:
            cur['items'].append(('jump', m.group(1), ln))
        i += 1
    return labels


def block_target(lines, i, ind):
    """if/else 블록 안 첫 jump 대상(없으면 블록의 첫 줄 요약)."""
    first = None
    j = i + 1
    while j < len(lines):
        raw = lines[j]
        if raw.strip() and (len(raw) - len(raw.lstrip())) <= ind:
            break
        st = raw.strip()
        if st and not st.startswith('#'):
            m = re.match(r'jump (\w+)', st)
            if m:
                return '→ ' + m.group(1)
            if first is None and re.search(r'r13_v111_set\(|r13_nw_list\(|r13_fork_set_fate\(|r13_nw_meeting_end\(|r13_nw_acquire\(|r13_v111_join\(', st):
                first = st
        j += 1
    # 대사 한 줄만 감싸는 if(사람이 있을 때만 말함 등)는 갈림이 아니라서 빼고(None), 값을 바꾸는 if 만 남긴다.
    return first


def parse_menu(lines, i, ind, path):
    """menu: 아래 보기들. (문구, 조건, 대상 라벨) 목록과 다음 줄 번호."""
    opts = []
    j = i + 1
    opt_ind = None
    while j < len(lines):
        raw = lines[j]
        st = raw.strip()
        cind = len(raw) - len(raw.lstrip())
        if st and cind <= ind:
            break
        if not st or st.startswith('#'):
            j += 1
            continue
        if opt_ind is None:
            opt_ind = cind
        if cind == opt_ind:
            m = re.match(r'''(['"])(.*?)\1(?:\s+if\s+(.+))?:$''', strip_comment(st))
            if m:
                opts.append([m.group(2), m.group(3) or '', '', j + 1])
            else:
                fail(path, j + 1, '메뉴 보기를 읽지 못함: ' + st[:60])
        elif opts and not opts[-1][2]:
            mm = re.match(r'jump (\w+)', st)
            if mm:
                opts[-1][2] = mm.group(1)
            elif st.startswith('$ ') and not opts[-1][2]:
                opts[-1][2] = st
        j += 1
    return opts, j


# ---------------------------------------------------------------- 그리기

def fmt_people(ids, names):
    return ', '.join(names.get(p, p) for p in ids) if ids else '—'


def fmt_val(v):
    if isinstance(v, Expr):
        return '`%s`' % v
    return '`%s`' % json.dumps(v, ensure_ascii=False)


def day_of(scene):
    m = re.match(r'MS14_D(\d+)', scene or '')
    return int(m.group(1)) if m else None


def op_text(kind, a, names):
    if kind == 'set' and len(a) >= 2:
        key = a[0] if isinstance(a[0], str) else str(a[0])
        return '`%s` = %s' % (key, fmt_val(a[1]))
    if kind == 'fate' and len(a) >= 2:
        return '생사 판정 `%s` = `%s`' % (a[0], a[1])
    if kind == 'list' and len(a) >= 2:
        return '명단 올림 %s (까닭 `%s`)' % (names.get(a[0], a[0]), a[1])
    if kind == 'end' and len(a) >= 2:
        return '회의 끝 `%s` → %s' % (a[0], fmt_val(a[1]))
    if kind == 'acquire':
        return '자료 얻음 `%s`' % a[0]
    return None


def render_days(all_labels, names, places, titles):
    out = ['## 1. 날짜별 장면 순서', '',
           '파일 안 순서대로 장면을 늘어놓았다(실제 재생 순서와 대체로 같고, 갈래가 나뉘는 날은 갈래마다 따로 나온다).',
           '「인물」은 그 장면 안에서 `r13_v111_arrive`/`r13_v111_join` 으로 세운 사람 전부(갈래에 따라 일부만 선다).',
           '「갈림」은 메뉴 보기(조건)와 `if` 조건, 「값」은 그 장면에서 바뀌는 판정 값이다.', '']
    scenes = {}
    order = []
    for lab in all_labels:
        sc = None
        for kind, a, ln in lab['items']:
            if kind == 'scene':
                sc = a
                if sc not in scenes:
                    scenes[sc] = dict(labels=[], travel=[], people=[], branch=[], ops=[], file=lab['file'], line=ln)
                    order.append(sc)
        key = lab['scene'] or ('(장면 전) ' + lab['file'])
        if key not in scenes:
            scenes[key] = dict(labels=[], travel=[], people=[], branch=[], ops=[], file=lab['file'], line=lab['line'])
            order.append(key)
        cur = scenes[key] if sc is None else None
        for kind, a, ln in lab['items']:
            if kind == 'scene':
                cur = scenes[a]
                if lab['name'] not in cur['labels']:
                    cur['labels'].append(lab['name'])
                continue
            if cur is None:
                cur = scenes[key]
            if lab['name'] not in cur['labels']:
                cur['labels'].append(lab['name'])
            if kind == 'travel' and a not in cur['travel']:
                cur['travel'].append(a)
            elif kind in ('arrive', 'join'):
                for p in a:
                    if p not in cur['people']:
                        cur['people'].append(p)
            elif kind == 'menu':
                cur['branch'].append(('menu', lab['name'], a, ln))
            elif kind == 'if' and a[0] != 'else':
                cur['branch'].append(('if', lab['name'], a, ln))
            else:
                t = op_text(kind, a, names)
                if t:
                    cur['ops'].append((lab['name'], t, ln))
    by_day = {}
    for sc in order:
        d = day_of(sc)
        by_day.setdefault(d, []).append(sc)
    for d in sorted(by_day, key=lambda x: (x is None, x or 0)):
        out += ['### %s' % ('%d일' % d if d else '날짜 없음'), '',
                '| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |', '|---|---|---|---|---|']
        for sc in by_day[d]:
            info = scenes[sc]
            t = titles.get(sc)
            if t is None and sc.startswith('MS14_'):
                fail(info['file'], info['line'], '장면 제목 없음: ' + sc)
            title = ('%s · %s' % t) if t else '—'
            trav = ', '.join('%s(%s)' % (places.get(p, p), p) if places.get(p) else p for p in info['travel']) or '—'
            labs = ', '.join('`%s`' % l for l in info['labels'][:6]) + (' 외 %d' % (len(info['labels']) - 6) if len(info['labels']) > 6 else '')
            out.append('| `%s` | %s | %s | %s | %s |' % (sc, title.replace('|', '/'), trav, fmt_people(info['people'], names), labs))
        out.append('')
        for sc in by_day[d]:
            info = scenes[sc]
            if not info['branch'] and not info['ops']:
                continue
            out += ['#### `%s` 갈림 · 값 (%s:%d)' % (sc, info['file'], info['line']), '']
            for kind, lab, a, ln in info['branch']:
                if kind == 'menu':
                    out.append('- 메뉴 `%s` (%d줄)' % (lab, ln))
                    for text, cond, target, oln in a:
                        out.append('  - 「%s」%s%s' % (text, (' — 조건 `%s`' % cond) if cond else '', (' → `%s`' % target) if target and not target.startswith('$') else ((' `%s`' % target) if target else '')))
                else:
                    word, cond, target = a
                    shown = cond if re.fullmatch(r'「[^」]*」', cond) else '`%s`' % cond
                    out.append('- `%s` %s %s %s' % (lab, word, shown, ('`%s`' % target) if target else ''))
            if info['ops']:
                out.append('- 값')
                seen = set()
                for lab, t, ln in info['ops']:
                    if (lab, t) in seen:
                        continue
                    seen.add((lab, t))
                    out.append('  - %s (`%s`)' % (t, lab))
            out.append('')
    return out


def render_meetings(all_labels, rules_text, fork_text, names, when):
    out = ['## 2. 회의', '']
    meetings = literal_after(fork_text, 'R13_FORK_MEETINGS =', FORK) or ()
    proof_meeting = literal_after(rules_text, 'R13_PROOF_MEETING=', RULES) or {}
    alts = literal_after(rules_text, 'R13_PROOF_ALTERNATES=', RULES) or {}
    extras = literal_after(rules_text, 'R13_PROOF_EXTRAS=', RULES) or {}
    ptitles = literal_after(rules_text, 'R13_PROOF_TITLES=', RULES) or {}
    tries = literal_after(rules_text, 'R13_NW_TRIES_BY_MEETING=', RULES) or {}
    m = re.search(r'R13_NW_TRIES=(\d+)', rules_text)
    default_tries = int(m.group(1)) if m else None
    # 증명 호출과 회의 끝 · 메뉴 쟁점
    proofs = {}
    ends = {}
    label_by = {l['name']: l for l in all_labels}
    retry_of = {}
    for lab in all_labels:
        for kind, a, ln in lab['items']:
            if kind == 'retry' and a:
                retry_of.setdefault(lab['name'], a[0])
    menu_issues = {}
    for lab in all_labels:
        claim = None
        for kind, a, ln in lab['items']:
            if kind == 'proof':
                if len(a) < 3 or not isinstance(a[0], str) or not isinstance(a[1], list):
                    fail(lab['file'], ln, '증명 호출을 읽지 못함')
                    continue
                key = a[0]
                proofs.setdefault(key, dict(correct=a[1], where=[], first=(lab['file'], ln)))
                proofs[key]['where'].append('%s:%d' % (lab['file'], ln))

            elif kind == 'end':
                if len(a) < 2 or isinstance(a[0], Expr):
                    fail(lab['file'], ln, '회의 끝 호출을 읽지 못함')
                    continue
                ops = [op_text(k, b, names) for k, b, l2 in lab['items'] if k in ('set', 'list', 'fate', 'acquire')]
                ends.setdefault(a[0], []).append((a[1], lab['name'], '%s:%d' % (lab['file'], ln), [o for o in ops if o]))
            elif kind == 'claim':
                claim = a
            elif kind == 'vmenu' and claim:
                # display_menu 꼴: 보기 번호마다 뒤따르는 if 가 대상 라벨로 보낸다
                rows = []
                meeting = None
                for k2, b2, l2 in lab['items']:
                    if k2 == 'if' and b2[2].startswith('→ ') and b2[1].startswith('「'):
                        target = b2[2][2:]
                        r = retry_of.get(target)
                        tl = label_by.get(target)
                        if r is None and tl:
                            for k3, b3, l3 in tl['items']:
                                if k3 == 'jump' and retry_of.get(b3):
                                    r = retry_of[b3]
                                    break
                                if k3 == 'end':
                                    r = b3[0]
                                    break
                        meeting = meeting or r
                        rows.append((b2[1].strip('「」'), '', target, '틀림(기회 사용 또는 회의 끝)' if r else '통과'))
                if not rows:
                    fail(lab['file'], ln, '선택지 쟁점의 보기를 읽지 못함: ' + claim)
                menu_issues.setdefault(claim, dict(meeting=meeting, rows=rows, where='%s:%d' % (lab['file'], ln)))
                claim = None
            elif kind == 'menu' and claim:
                meeting = None
                rows = []
                for text, cond, target, oln in a:
                    tl = label_by.get(target)
                    r = retry_of.get(target)
                    if r is None and tl:
                        # 오답 라벨이 바로 다른 라벨로 넘기는 경우 한 번 따라간다
                        for k2, b2, l2 in tl['items']:
                            if k2 == 'jump' and retry_of.get(b2):
                                r = retry_of[b2]
                                break
                    meeting = meeting or r
                    rows.append((text, cond, target, '틀림(기회 사용)' if r else '통과'))
                menu_issues.setdefault(claim, dict(meeting=meeting, rows=rows, where='%s:%d' % (lab['file'], ln)))
                claim = None
    out += ['기회 수는 `R13_NW_TRIES_BY_MEETING`(표에 없으면 `R13_NW_TRIES`=%s). 정답 판정은 `r13_v111_proof_accepts` — 정답 세트 하나를 다 갖추고, 나머지가 다른 정답 세트나 덧붙임에 든 자료뿐이면 받는다.' % default_tries, '',
            '| 회의 | 이름 | 날 | 기회 | 결과(코드에 있는 것) |', '|---|---|---|---|---|']
    for row in meetings:
        key, title, day = row[0], row[1], row[2]
        res = sorted(set(('win·partial(쟁점 모두 이기면 win)' if isinstance(r[0], Expr) else str(r[0])) for r in ends.get(key, [])))
        out.append('| `%s` | %s | %s | %s | %s |' % (key, title, day, tries.get(key, default_tries), ', '.join(res) or '—'))
    out.append('')
    loose = [(k, v) for k, v in proofs.items() if k not in proof_meeting]
    if loose:
        out += ['회의 밖 대조(기회를 쓰지 않는 자료 맞추기 · `R13_PROOF_MEETING` 에 없음)', '']
        for k, v in loose:
            out.append('- %s — 정답 %s (%s)' % (k, '+'.join(v['correct']), ', '.join(v['where'])))
        out.append('')
    known = set(r[0] for r in meetings)
    for key in sorted(set(proof_meeting.values()) - known):
        fail(RULES, 0, '회의 목록(R13_FORK_MEETINGS)에 없는 회의: ' + key)
    for row in meetings:
        key, title, day = row[0], row[1], row[2]
        out += ['### %s `%s` · %s · 기회 %s' % (title, key, day, tries.get(key, default_tries)), '']
        issues = [(k, v) for k, v in proofs.items() if proof_meeting.get(k) == key]
        mis = [(k, v) for k, v in menu_issues.items() if v['meeting'] == key]
        if mis:
            out.append('선택지 쟁점')
            out.append('')
            for k, v in mis:
                out.append('- `%s` (%s)' % (k, v['where']))
                for text, cond, target, verdict in v['rows']:
                    out.append('  - 「%s」 — %s%s' % (text, verdict, (' · 조건 `%s`' % cond) if cond else ''))
            out.append('')
        if issues:
            out += ['| 증명 키(쟁점) | 화면 제목 | 정답 | 대체 정답 | 덧붙여도 받음 | 자리 |', '|---|---|---|---|---|---|']
            for k, v in issues:
                alt = ' / '.join('+'.join(s) for s in alts.get(k, ())) or '—'
                ex = ', '.join(extras.get(k, ())) or '—'
                out.append('| %s | %s | %s | %s | %s | %s |' % (k, ptitles.get(k, '—'), '+'.join(v['correct']), alt, ex, ', '.join(v['where'])))
            out.append('')
        if not issues and not mis:
            out += ['(쟁점을 코드에서 찾지 못함)', '']
            fail(FORK, 0, '쟁점을 찾지 못한 회의: ' + key)
        if ends.get(key):
            out.append('결과마다 바뀌는 값')
            out.append('')
            for res, lab, where, ops in ends[key]:
                out.append('- %s · `%s` (%s)%s' % (fmt_val(res), lab, where, (': ' + '; '.join(ops)) if ops else ''))
            out.append('')
        conds = sorted(n for n, e in when.items() if ('"meeting:%s"' % key) in e or ("'meeting:%s'" % key) in e or ('tries:%s' % key) in e or ('"%s"' % key) in e and 'tries' in e)
        if conds:
            out += ['이 회의를 읽는 조건: ' + ', '.join('`%s`' % c for c in conds), '']
    return out


def parse_when(text):
    """R13_NW_WHEN 사전의 이름 → 식(글자)."""
    when = {}
    at = text.find('R13_NW_WHEN={')
    if at < 0:
        fail(TEXT, 0, 'R13_NW_WHEN 을 찾지 못함')
        return when
    start = text[:at].count('\n') + 1
    body = balanced(text, at + len('R13_NW_WHEN='))
    for k, line in enumerate(body.splitlines()[1:-1]):
        st = line.strip()
        if not st or st.startswith('#'):
            continue
        m = re.match(r'"([^"]+)"\s*:\s*lambda\s*:(.*)$', st)
        if not m:
            fail(TEXT, start + k + 1, '조건 줄을 읽지 못함: ' + st[:60])
            continue
        expr = strip_comment(m.group(2)).rstrip(',').strip()
        when[m.group(1)] = expr
    for m in re.finditer(r'for _nw_who in \(([^)]*)\):\s*\n\s*R13_NW_WHEN\["dead:"\+_nw_who\]', text):
        for w in re.findall(r'"(\w+)"', m.group(1)):
            when['dead:' + w] = '"%s" in r13_nw_dead()' % w
    m = re.search(r'R13_NW_LIST_NAMES=\(([^)]*)\)', text)
    if m:
        for p in re.findall(r'"(\w+)"', m.group(1)):
            when['listed:' + p] = 'r13_v111_value("listed:%s") is True' % p
    return when


def when_usage():
    use = {}
    for f in sorted((GAME / 'v111/newworld').glob('d*.json')):
        for name in re.findall(r'"when"\s*:\s*"([^"]+)"', f.read_text()):
            use.setdefault(name, set()).add(f.stem)
    for f in sorted(GAME.glob('room13_v111*.rpy')):
        for name in re.findall(r'R13_NW_WHEN\["([^"]+)"\]\(\)', f.read_text()):
            use.setdefault(name, set()).add(f.stem.replace('room13_v111_', ''))
    return use


def render_conditions(when):
    use = when_usage()
    out = ['## 4. 조건 이름(`R13_NW_WHEN`)', '',
           '대사 패치(`game/v111/newworld/dNN.json`)의 `"when"` 과 코드의 `R13_NW_WHEN["이름"]()` 이 쓰는 이름. 「쓰는 곳」은 그 이름이 나오는 날짜 패치·코드 파일.', '',
           '| 이름 | 식 | 쓰는 곳 |', '|---|---|---|']
    for name in sorted(when):
        out.append('| `%s` | `%s` | %s |' % (name, when[name].replace('|', '/'), ', '.join(sorted(use.get(name, ()))) or '—'))
    unknown = sorted(n for n in use if n not in when)
    for n in unknown:
        fail(TEXT, 0, '정의를 찾지 못한 조건 이름: ' + n)
    out.append('')
    return out


def render_lives(all_labels, rules_text, fork_text, names):
    out = ['## 3. 생사 · 명단 · 결말', '']
    m = re.search(r'R13_NW_LIVES=\(\((.*?)\)\)\n', rules_text, re.S)
    lives = re.findall(r'\("(\w+)","([^"]+)"\)', rules_text[rules_text.find('R13_NW_LIVES='):rules_text.find('R13_NW_FROZEN_AT')])
    if not lives:
        fail(RULES, 0, 'R13_NW_LIVES 를 읽지 못함')
    frozen = re.search(r'R13_NW_FROZEN_AT=(\d+)', rules_text)
    out += ['### 죽음으로 세는 사람(`R13_NW_LIVES`)', '', '| 인물 | 살아 있음을 적는 값 (False 면 죽음) |', '|---|---|']
    for who, key in lives:
        out.append('| %s (`%s`) | `%s` |' % (names.get(who, who), who, key))
    out += ['', '그 밖에 `r13_nw_is_dead`: 도담은 `route12 == "late_exposure"` 이면 죽음. `r13_nw_dead`: 13일 수레로 떠난 사람(`departed_names`, 다람 빼고)도 죽음으로 센다. 「얼어붙은 마을」 기준 `R13_NW_FROZEN_AT` = %s.' % (frozen.group(1) if frozen else '?'), '']
    for fn in ('r13_nw_is_dead', 'r13_nw_dead', 'r13_nw_ending14', 'r13_nw_true_ending_ready'):
        src = func_source(rules_text, fn)
        if src:
            out += ['```python', src, '```', '']
        else:
            fail(RULES, 0, '함수를 찾지 못함: ' + fn)
    endings = literal_after(fork_text, 'R13_FORK_ENDINGS =', FORK) if 'R13_FORK_ENDINGS =' in fork_text else None
    if endings is None:
        m = re.search(r'R13_FORK_ENDINGS = dict\((.*?)\)\n', fork_text)
        endings = dict(re.findall(r"(\w+)='([^']+)'", m.group(1))) if m else {}
    order = re.findall(r'return "(\w+)"', func_source(rules_text, 'r13_nw_ending14') or '')
    out += ['### 결말 이름과 판정 순서', '', '| 순서 | 값 | 이름 |', '|---|---|---|']
    for k, v in enumerate(order, 1):
        out.append('| %d | `%s` | %s |' % (k, v, endings.get(v, '?')))
    if 'true' in endings:
        out.append('| 승격 | `true` | %s — `ending14 == "morning"` 에서 `r13_nw_true_ending_ready()` 가 참일 때 |' % endings['true'])
    out.append('')
    # 생사 판정 시점
    fates = literal_after(fork_text, 'R13_FORK_FATE_RESULTS =', FORK) or {}
    out += ['### 생사 판정 시점(`r13_fork_set_fate`)', '', '| 판정 | 결과 | 적는 자리 |', '|---|---|---|']
    calls = {}
    for lab in all_labels:
        for kind, a, ln in lab['items']:
            if kind == 'fate' and len(a) >= 2:
                calls.setdefault((a[0], a[1]), []).append('`%s` (%s:%d)' % (lab['name'], lab['file'], ln))
    for key in fates:
        for res, title in fates[key]:
            out.append('| `%s` | `%s` %s | %s |' % (key, res, title, ', '.join(calls.get((key, res), [])) or '코드에서 호출 못 찾음'))
    out.append('')
    # 명단
    listable = re.search(r'R13_NW_LISTABLE=\(([^)]*)\)', rules_text)
    out += ['### 이송 명단(`r13_nw_list`)', '', '올릴 수 있는 사람: ' + (', '.join(names.get(p, p) for p in re.findall(r'"(\w+)"', listable.group(1))) if listable else '?'), '',
            '| 인물 | 까닭 | 자리 |', '|---|---|---|']
    for lab in all_labels:
        for kind, a, ln in lab['items']:
            if kind == 'list':
                if len(a) < 2:
                    fail(lab['file'], ln, '명단 호출을 읽지 못함')
                    continue
                out.append('| %s | `%s` | `%s` (%s:%d) |' % (names.get(a[0], a[0]), a[1], lab['name'], lab['file'], ln))
    out += ['', '### 수레로 떠남(`departed:`)', '']
    for lab in all_labels:
        for kind, a, ln in lab['items']:
            if kind == 'departed_loop' or (kind == 'set' and a and isinstance(a[0], str) and a[0].startswith('departed')):
                out.append('- `%s` (%s:%d): %s' % (lab['name'], lab['file'], ln, a if isinstance(a, str) else op_text('set', a, names)))
    out.append('')
    return out


def build():
    del FAIL[:]
    names = names_table()
    places = places_table()
    titles = scene_titles()
    BINDINGS.clear()
    BINDINGS.update(binding_titles())
    all_labels = []
    for f in DAY_FILES:
        all_labels += parse_day_file(GAME / f)
    rules_text = RULES.read_text()
    fork_text = FORK.read_text()
    when = parse_when(TEXT.read_text())
    body = []
    body += render_days(all_labels, names, places, titles)
    body += render_meetings(all_labels, rules_text, fork_text, names, when)
    body += render_lives(all_labels, rules_text, fork_text, names)
    body += render_conditions(when)
    head = ['# 이야기 총정리 · 자동 부분', '',
            '> 이 파일은 손으로 고치지 않는다. 다시 만들기: `python3 dev/story_master.py --write` (`experiments/renpy-ch1` 에서).',
            '> 사람이 쓰는 부분(사건 여섯 칸 · 감정선 · 퍼즐 · 현행/설계)은 `docs/design/story_master.md`.',
            '> 읽은 곳: `game/%s`, `game/room13_v111_newworld_rules.rpy`, `game/room13_v111_newworld_text.rpy`, `game/room13_fork_screen.rpy`, 장면 제목은 `docs/story-ms14/source/` 원본.' % '`, `game/'.join(DAY_FILES),
            '> 글자로 읽은 것이라 갈래 순서·조건이 실제 재생과 다를 수 있다. 의심스러우면 표에 적힌 파일:줄을 연다.', '',
            '자동 추출 실패: %d곳 (맨 아래 목록)' % len(FAIL), '',
            '## 차례', '', '1. 날짜별 장면 순서', '2. 회의', '3. 생사 · 명단 · 결말', '4. 조건 이름', '5. 자동 추출 실패', '']
    tail = ['## 5. 자동 추출 실패', '']
    if FAIL:
        for f, ln, why in sorted(set(FAIL)):
            tail.append('- 자동 추출 실패: %s:%d — %s' % (f, ln, why))
    else:
        tail.append('없음.')
    tail.append('')
    return '\n'.join(head + body + tail)


def main(argv):
    text = build()
    if '--write' in argv:
        OUT.write_text(text)
        print('%s 를 썼다 (%d줄, 자동 추출 실패 %d곳)' % (OUT.relative_to(ROOT), text.count('\n'), len(set(FAIL))))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
