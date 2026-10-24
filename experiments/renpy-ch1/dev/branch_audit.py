"""분기 대사 대조 점검 (2026-10-24 소유자 핵심 임무: 분기끼리 논리 오류 0, 분기마다 모든 인물 대사 맞춤).

대사 한 줄마다 「이 줄이 나올 수 있는 경로」와 「그 경로에서의 세계 상태」를 맞대어 의심 줄을 뽑는다.
사람이 손으로 적은 경로표를 쓰지 않는다. 대본 rpy(room13_v111_days*.rpy)의 라벨·jump·call·if·menu 를
그래프로 읽고, 값을 바꾸는 호출(r13_v111_set, r13_v111_commit 의 원문 기록 연산, r13_fork_set_fate,
r13_nw_meeting_end, r13_nw_list, r13_nw_acquire)을 따라가며 지점마다 「가능한 값의 집합」을 모은다.
갈림 시점(fate_piko·fate_kkomi·fate_owl·fate_nero·fate_soup·fate_crowd)의 결과는 경로를 나누는 열쇠로
따로 들고 다닌다(같은 줄이라도 fate_owl=lost 경로와 stay 경로의 상태를 섞지 않는다).
회의 결과(meeting:*)·명단(listed:*)·떠남(departed:*)은 그 안에서 값 집합으로 들고 다닌다.

  D 죽었거나 떠난 뒤의 말   화자가 그 경로에서 죽었거나 수레로 떠났다(확실: 그 경로에서 반드시, 의심: 그럴 수 있음).
                            이름이 문장에 나오고 과거형 표지가 없으면(「너울 씨」를 산 사람처럼) 의심.
  E 장면에 없는 화자        원본 장면 등장인물(제작기준본 actors)과 그 지점까지 무대에 오른 사람(arrive·join·
                            travel 동행·현장 인원) 어디에도 없는 화자. 원본 장면 인원 정보가 있는 장면만 본다.
  F 일어나지 않은 일        갈림 결과에 딸린 낱말(FATE_WORDS)이 그 결과가 아닌 경로에서 나온다.
  G 같은 말 두 번           같은 날·같은 경로에서 같은 인물이 거의 같은 말을 두 번 한다(유사도, 의심).

  python3 dev/branch_audit.py --day 7          7일만
  python3 dev/branch_audit.py --all            1~14일
  python3 dev/branch_audit.py --all --json     기계용
  python3 dev/branch_audit.py --all --write    docs/reviews/branch-audit/YYYYMMDD.md 에 표로 쓴다

조건을 해석하지 못하면 추정하지 않는다. 그 조건은 「알 수 없음」으로 두고(그 줄은 양쪽 다 가능한 것으로 본다)
목록에 따로 낸다. 자세한 설명과 한계는 docs/design/BRANCH_AUDIT.md.
"""
import argparse
import ast
import collections
import datetime
import difflib
import heapq
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'game'
SRC_SCENES = ROOT / 'docs/story-ms14/source/다람탐정_제작기준본01_대사연출조건.json'
STORY_FILES = ('room13_v111_days123.rpy', 'room13_v111_days45.rpy', 'room13_v111_days610.rpy', 'room13_v111_days1114.rpy')
ENTRY = 'r13_v111_start'

# 한 조건을 판정할 때 펼쳐 보는 값 조합의 상한. 넘으면 그 조건은 「알 수 없음」.
ENUM_LIMIT = 4000
# 한 값이 가질 수 있는 후보가 이보다 많아지면(횟수 누적 등) 「아무 값」으로 본다.
VALUE_CAP = 12


class _Any:
    """계산할 수 없는 값(밖의 함수가 바꾸거나 식을 못 읽음). 이 값을 읽는 판정은 「알 수 없음」."""
    def __repr__(self):
        return '?'


ANY = _Any()


class Unknown(Exception):
    pass


class NeedKey(Exception):
    """아직 정하지 않은 값. dom 이 있으면 그 값들 중 하나(판정 함수 호출의 가능한 결과)."""
    def __init__(self, key, dom=None):
        super().__init__(key)
        self.key = key
        self.dom = dom


def freeze(v):
    if isinstance(v, list):
        return tuple(freeze(x) for x in v)
    if isinstance(v, dict):
        return tuple(sorted((k, freeze(x)) for k, x in v.items()))
    return v


def norm(values):
    s = frozenset(values)
    if ANY in s or len(s) > VALUE_CAP:
        return frozenset((ANY,))
    return s


# ---------------------------------------------------------------- 갈림 결과 낱말 사전 (F)
# (갈림, 그 일이 일어나는 결과들) -> 그 일을 가리키는 낱말. 작게 둔다. 이름표가 가리키는 사건 자체가
# 모든 경로에 있으면(예: 3번 등은 두 경로 모두 꺼진다) 넣지 않는다 — 결과(죽음·구조)를 가리키는 말만.
FATE_WORDS = [
    ('fate_piko', ('lost',), r'코가 빈 (초상|그림)|(얼어 죽은|죽은) 피코|피코(가|는)? ?(얼어 ?죽|죽었)'),
    ('fate_piko', ('saved',), r'피코가 완성한|완성(된|한) 초상|피코(가|는)? ?(살았|살아 있)'),
    ('fate_kkomi', ('lost',), r'타 버린 창고|꼬미(의)? (그릇|숟가락|빈자리)|꼬미(가|는|도)? ?(죽었|죽은|숨졌)'),
    ('fate_kkomi', ('saved',), r'빈 창고(만)? ?(탔|타|불)|아이 넷(을|이)? ?(다 )?(학교|데려|옮)'),
    ('fate_owl', ('lost',), r'부엉이(는|가)? ?죽었|노인을 죽게 한|부엉이를 친|(죽은|돌아가신) 부엉이'),
    ('fate_owl', ('stay', 'take'), r'부엉이(가|는)? ?(살았|살아 있)|부엉이 어르신은 살아서'),
    ('fate_nero', ('lost',), r'끊긴 등불|눈에 묻혀|네로(가|는|도)? ?(죽었|죽은|묻혔|못 돌아)'),
    ('fate_nero', ('handover', 'rescue'), r'셋 다 들어왔'),
    ('fate_soup', ('lost',), r'도담아[.,]? ?(불 켜졌어)?[.…, ]*일어나|도담(이)?(가|는)? ?(죽었|죽은|숨졌)'),
    ('fate_crowd', ('riot',), r'올라간 주먹|뒤집힌 수레|모모 씨의 손'),
    ('fate_crowd', ('block', 'riot'), r'너울(이|은|도)? ?(맞아 ?죽|죽었|죽은)|(맞아 죽은|죽은) 너울'),
]

# 이름이 나와도 「산 사람처럼」이 아닌 줄의 표지(과거형·죽음·떠남). 이것이 있으면 D 이름 언급을 띄우지 않는다.
PAST_MARKS = r'었|였|았|했|셨|던|더라|더군|더니|죽|숨|묻|잃|떠나|떠난|떠났|실려|끌려|태워|장례|무덤|생전|마지막|그날|기억|남긴|남겨|명단|수레'

# 이름 언급(D)에서 사람 이름으로 보지 않는 호칭.
ROLE_NAMES = {'엄마', '아빠', '할머니', '촌장', '선생님', '사자 선생님', '아이', '주민', '순찰대원', '아랫길 주민'}

# 원본 장면 actors 의 로마자 표기 -> 게임 인물 ID (제작기준본은 로마자·한글이 섞여 있다).
SOURCE_ACTOR_ALIASES = {
    'father': 'dad', 'grandmother': 'granny', 'granny': 'granny', 'owl': 'resident_owlgp', 'chorong': 'resident_lamplighter',
    'dolmok': 'guard', 'badugi': 'resident_badook', 'silluk': 'resident_siluk', 'piko': 'resident_piko', 'nero': 'resident_nero',
    'tok': 'resident_tok', 'kkomi': 'kid_kkomi', 'bori': 'resident_bori', 'seori': 'resident_seori', 'musoe': 'resident_musoe',
    'ttadak': 'resident_ttadak', 'teacher': 'resident_teacher', 'ubak': 'resident_ubak', 'baek': 'resident_madam',
    'nubi': 'resident_nubi', 'sling': 'resident_sling', 'momo': 'resident_momo', 'somi': 'resident_somi',
    'kongi': 'resident_kongi', 'tosil': 'resident_tosil',
}

# 경로 열쇠에 더하는 값(사람이 정함). 13일 수레가 떠났는지에 떠난 사람 전부와 13일 결과가 묶여 있어서,
# 섞으면 「수레가 안 떠난 결말에서도 판돌이 떠났을 수 있음」이 된다.
EXTRA_SPLIT = ('cart_departed',)

# 사망 판정이 생존 값 말고 다른 값에도 걸린 사람(r13_nw_is_dead).
DEATH_KEYS = {'kid_dodam': ('route12',)}

# 이름 없는 단역(주민·순찰대원·종업원 등). 장면 인원으로 따지지 않는다.
EXTRAS = ('v111_', 'ms14_')

# 한 번 정해지면 바뀌지 않는 값. G 에서 두 줄이 같은 판에 함께 나올 수 있는지 가를 때 쓴다.
WRITE_ONCE = ('meeting:', 'fate:', 'choice:', 'route7', 'prevention', 'route12', 'outcome13', 'ending14')

# 대사 안에서 이름 대신 쓰는 다른 꼴(사람이 확인해 넣는다).
NAME_ALIASES = {'부엉이 영감': 'resident_owlgp'}


# ---------------------------------------------------------------- 게임 자료 읽기
class Game:
    """점검에 쓰는 자료 묶음. 시험은 이 모양의 가짜를 직접 만든다."""

    def __init__(self, **kw):
        self.records = {}
        self.options = {}
        self.initial = {}
        self.patches = {}          # day -> dNN.json
        self.reactions = {}
        self.speakers = {}         # 한글 화자 이름 -> 인물 ID
        self.life = {}             # 인물 ID -> 생존 값 이름 (없으면 alive:<ID>)
        self.lives = []            # R13_NW_LIVES (인물, 값)
        self.listable = []
        self.fates = []            # 갈림 키 순서
        self.fate_days = {}        # 갈림 키 -> '2일 저녁'
        self.fate_results = {}     # 갈림 키 -> [(결과, 이름표)]
        self.when_src = {}         # 조건 이름 -> 식 글자
        self.when = {}             # 조건 이름 -> ast 식(못 읽으면 None)
        self.scene_actors = {}     # 장면 -> 원본 등장인물 ID 집합
        self.bindings = {}         # 현장 열쇠 -> 그 자리 인원
        self.story = {}            # 파일 이름 -> 글자
        self.external_keys = set()
        self.external_prefixes = set()
        self.notes = []            # 코드에서 못 뽑아 표로 보충한 것과 그 출처
        self.funcs = {}            # 규칙 파일의 판정 함수 이름 -> ast 함수
        self.consts = {}           # 그 함수가 읽는 상수
        self.part_names = None     # 경로 열쇠 이름(갈림 + 함수로 정해지는 값), Analyzer 가 채운다
        self.__dict__.update(kw)

    def keys(self):
        return self.part_names or self.fates

    def life_key(self, person):
        return self.life.get(person, 'alive:' + person)


def _literal_after(src, name):
    """`NAME = <literal>` 의 오른쪽을 ast 로 읽는다."""
    m = re.search(r'\b' + re.escape(name) + r'\s*=\s*', src)
    if not m:
        return None
    rest = src[m.end():]
    for end in range(len(rest), 0, -1):
        # 가장 긴 식부터 줄여 가며 읽는다(한 줄짜리 정의가 대부분이라 금방 끝난다).
        if rest[end - 1] not in ')]}':
            continue
        try:
            return ast.parse(rest[:end].strip(), mode='eval').body
        except SyntaxError:
            continue
    return None


def _block_after(src, start_pat):
    """`start_pat{` 로 시작하는 사전 글자를 짝 맞는 `}` 까지 꺼낸다(문자열 안의 괄호는 건너뛴다)."""
    m = re.search(start_pat, src)
    if not m:
        return None
    i = src.index('{', m.start())
    depth, j, quote = 0, i, None
    while j < len(src):
        ch = src[j]
        if quote:
            if ch == '\\':
                j += 2
                continue
            if ch == quote:
                quote = None
        elif ch in '"\'':
            quote = ch
        elif ch == '#':
            j = src.index('\n', j)
            continue
        elif ch in '{([':
            depth += 1
        elif ch in '})]':
            depth -= 1
            if depth == 0:
                return src[i:j + 1]
        j += 1
    return None


def parse_when(src):
    """R13_NW_WHEN 사전을 읽어 조건 이름 -> (식 글자, ast) 로. 반복문으로 더하는 dead:/listed: 도 만든다."""
    text = _block_after(src, r'R13_NW_WHEN\s*=\s*\{')
    out_src, out_ast = {}, {}
    if text:
        tree = ast.parse(text, mode='eval').body
        for k, v in zip(tree.keys, tree.values):
            if isinstance(k, ast.Constant) and isinstance(v, ast.Lambda):
                out_src[k.value] = ast.get_source_segment(text, v.body) or ''
                out_ast[k.value] = v.body if not v.args.args else None
    # for _nw_who in (...): R13_NW_WHEN["dead:"+_nw_who]=lambda w=_nw_who: w in r13_nw_dead()
    m = re.search(r'for _nw_who in \(([^)]*)\):\s*\n\s*R13_NW_WHEN\["dead:"', src)
    if m:
        for who in re.findall(r'"([^"]+)"', m.group(1)):
            expr = '"%s" in r13_nw_dead()' % who
            out_src['dead:' + who] = expr
            out_ast['dead:' + who] = ast.parse(expr, mode='eval').body
    m = re.search(r'R13_NW_LIST_NAMES\s*=\s*\(([^)]*)\)', src)
    if m and 'R13_NW_WHEN["listed:"' in src:
        for who in re.findall(r'"([^"]+)"', m.group(1)):
            expr = 'r13_v111_value("listed:%s") is True' % who
            out_src['listed:' + who] = expr
            out_ast['listed:' + who] = ast.parse(expr, mode='eval').body
    return out_src, out_ast


# 규칙 파일에서 본문 그대로 계산하는 판정 함수. 값을 바꾸지 않고 읽기만 하는 것만 넣는다.
# r13_nw_retry 는 기회를 하나 쓰는 부수 효과가 있지만 판정에는 「회의가 이미 끝났으면 거짓」만 쓴다(부수 효과는 무시).
FUNC_NAMES = ('r13_nw_is_dead', 'r13_nw_dead', 'r13_nw_loss_count', 'r13_nw_ending14', 'r13_nw_true_ending_ready', 'r13_nw_listed',
              'r13_nw_retry')


def parse_funcs(src, names):
    out = {}
    lines = src.split('\n')
    for i, line in enumerate(lines):
        m = re.match(r'^(\s*)def (\w+)\(', line)
        if not m or m.group(2) not in names:
            continue
        ind = len(m.group(1))
        body = [line[ind:]]
        for nxt in lines[i + 1:]:
            if nxt.strip() and _indent(nxt) <= ind:
                break
            body.append(nxt[ind:] if len(nxt) >= ind else nxt)
        try:
            fn = ast.parse('\n'.join(body)).body[0]
            out[m.group(2)] = fn
        except SyntaxError:
            continue
    return out


SET_RE = re.compile(r'r13_v111_set\(\s*(["\'])([^"\'%]+)\1\s*([,+%])')


def external_writes(game_dir, story_files):
    """대본 밖(엔진·화면·다른 층)에서 값을 바꾸는 키. 대본 그래프로는 못 따라가므로 처음부터 「아무 값」."""
    keys, prefixes = set(), set()
    # 이 함수들 안의 쓰기는 대본에서 그 함수 호출로 따로 흉내 낸다.
    modeled = ('def r13_nw_list', 'def r13_nw_meeting_end', 'def r13_fork_set_fate', 'def r13_v111_set', 'def r13_v111_apply')
    for f in sorted(game_dir.rglob('*.rpy')):
        if f.name in story_files or 'qa_tests' in f.parts:
            continue
        text = f.read_text(encoding='utf-8')
        cur = None
        for line in text.split('\n'):
            s = line.strip()
            if s.startswith('def '):
                cur = s
            for m in SET_RE.finditer(line):
                if cur and cur.startswith(modeled):
                    continue
                if m.group(3) == ',':
                    keys.add(m.group(2))
                else:
                    prefixes.add(m.group(2))
    return keys, prefixes


def load_game():
    g = Game()
    data = json.loads((GAME / 'v111/records.json').read_text(encoding='utf-8'))
    g.records, g.options = data['records'], data.get('options', {})
    g.initial = {k: freeze(v) for k, v in data['initial'].items()}
    for day in range(1, 15):
        p = GAME / f'v111/newworld/d{day:02d}.json'
        if p.exists():
            g.patches[day] = json.loads(p.read_text(encoding='utf-8'))
    p = GAME / 'v111/newworld/reactions.json'
    g.reactions = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
    src = (GAME / 'ms14_story.rpy').read_text(encoding='utf-8')
    g.speakers = dict(re.findall(r'"([^"]+)"\s*:\s*"([a-z_0-9]+)"', src.split('MS14_SPEAKERS', 1)[1].split('}', 1)[0]))
    later = (GAME / 'room13_v111_later_bindings.rpy').read_text(encoding='utf-8')
    for block in re.findall(r'MS14_SPEAKERS\.update\(\{(.*?)\}\)', later, re.S):
        g.speakers.update(re.findall(r'"([^"]+)"\s*:\s*"([a-z_0-9]+)"', block))
    main = (GAME / 'room13_v111.rpy').read_text(encoding='utf-8')
    body = main.split('def r13_v111_person_alive', 1)[1].split('return', 1)[0]
    g.life = dict(re.findall(r'"([a-z_0-9]+)":"([A-Za-z_:0-9]+)"', body))
    rules = (GAME / 'room13_v111_newworld_rules.rpy').read_text(encoding='utf-8')
    for m in re.finditer(r'R13_NW_LIVES\s*=\s*(?:R13_NW_LIVES\s*\+\s*)?\((.*)\)\s*$', rules, re.M):
        g.lives += re.findall(r'\("([a-z_0-9]+)","([A-Za-z_:0-9]+)"\)', m.group(1))
    m = re.search(r'R13_NW_LISTABLE\s*=\s*\(([^)]*)\)', rules)
    g.listable = re.findall(r'"([^"]+)"', m.group(1)) if m else []
    g.funcs = parse_funcs(rules, FUNC_NAMES)
    g.consts = dict(R13_NW_LIVES=tuple(g.lives), R13_NW_LISTABLE=tuple(g.listable))
    for name in ('R13_NW_FROZEN_AT', 'R13_NW_TRIES'):
        m = re.search(r'^\s*%s\s*=\s*(\d+)' % name, rules, re.M)
        if m:
            g.consts[name] = int(m.group(1))
    fork = (GAME / 'room13_fork_screen.rpy').read_text(encoding='utf-8')
    points = _literal_after(fork, 'R13_FORK_FATE_POINTS')
    for p in ast.literal_eval(points) if points is not None else ():
        g.fates.append(p[0])
        g.fate_days[p[0]] = p[2]
    res = _literal_after(fork, 'R13_FORK_FATE_RESULTS')
    if isinstance(res, ast.Call):
        for kw in res.keywords:
            g.fate_results[kw.arg] = list(ast.literal_eval(kw.value))
    text = (GAME / 'room13_v111_newworld_text.rpy').read_text(encoding='utf-8')
    g.when_src, g.when = parse_when(text)
    try:
        for s in json.loads(SRC_SCENES.read_text(encoding='utf-8'))['scenes']:
            ids = set()
            for a in s.get('actors') or []:
                aid = a.get('actor_id') if isinstance(a, dict) else a
                ids.add(SOURCE_ACTOR_ALIASES.get(aid) or g.speakers.get(aid) or aid)
            g.scene_actors[s['scene_id']] = ids
    except (OSError, KeyError, ValueError):
        pass
    try:
        for key, b in json.loads((GAME / 'v111/field-bindings.json').read_text(encoding='utf-8')).items():
            people = set(b.get('people') or [])
            for o in b.get('options', []):
                if o.get('person'):
                    people.add(o['person'])
            g.bindings[key] = people
    except (OSError, ValueError):
        pass
    for f in STORY_FILES:
        g.story[f] = (GAME / f).read_text(encoding='utf-8')
    g.external_keys, g.external_prefixes = external_writes(GAME, STORY_FILES)
    g.notes = [
        ('kid_dodam 사망', '12일 늦은 폭로(route12=late_exposure)도 사망으로 센다', 'room13_v111_newworld_rules.rpy r13_nw_is_dead'),
        ('수레로 떠남', '13일 담요 회의 패배 때 python 블록이 탑승자마다 departed:<인물>을 켠다. 누가 타는지는 명단·cart_roster 로 정해져 '
         '이 도구는 「명단에 오를 수 있는 사람 모두가 떠났을 수 있음」으로 본다', 'room13_v111_days1114.rpy r13_v111_mending_wrong13'),
        ('생존 값 이름', '인물 ID -> 생존 값은 r13_v111_person_alive 의 표, 없으면 alive:<인물>', 'room13_v111.rpy'),
    ]
    return g


# ---------------------------------------------------------------- 대본 읽기 (라벨 그래프)
LABEL_RE = re.compile(r'^label\s+([A-Za-z_][\w.]*)\s*(\(.*\))?\s*:\s*$')


def _indent(line):
    return len(line) - len(line.lstrip(' '))


def _strip_comment(s):
    # 문자열 밖의 # 부터 지운다.
    quote = None
    for i, ch in enumerate(s):
        if quote:
            if ch == quote:
                quote = None
        elif ch in '"\'':
            quote = ch
        elif ch == '#':
            return s[:i].rstrip()
    return s


class Story:
    """대본 rpy 의 라벨과 문장 나무."""

    def __init__(self, texts):
        self.labels = {}       # 이름 -> dict(file, line, body, next)
        self.order = []
        self._ids = 0
        for fname, text in texts.items():
            self._parse_file(fname, text)

    def _parse_file(self, fname, text):
        lines = text.split('\n')
        starts = [(i, LABEL_RE.match(l)) for i, l in enumerate(lines)]
        starts = [(i, m) for i, m in starts if m]
        prev = None
        for n, (i, m) in enumerate(starts):
            end = starts[n + 1][0] if n + 1 < len(starts) else len(lines)
            body_lines = [(j + 1, lines[j]) for j in range(i + 1, end)]
            body, _ = self._block(fname, body_lines, 0, None)
            name = m.group(1)
            self.labels[name] = dict(name=name, file=fname, line=i + 1, body=body, next=None)
            if prev:
                self.labels[prev]['next'] = name
            prev = name
            self.order.append(name)

    def _new_id(self):
        self._ids += 1
        return self._ids

    def _block(self, fname, lines, i, indent):
        """같은 들여쓰기의 문장들. (문장 목록, 다음 위치)."""
        out = []
        while i < len(lines):
            no, raw = lines[i]
            s = _strip_comment(raw).strip()
            if not s:
                i += 1
                continue
            ind = _indent(raw)
            if indent is None:
                indent = ind
            if ind < indent:
                break
            if ind > indent:
                # 예상하지 못한 더 깊은 줄(이어지는 식 등)은 건너뛴다.
                i += 1
                continue
            i += 1
            where = (fname, no)
            if s.endswith(':') and (s.startswith(('if ', 'elif ', 'while ')) or s in ('else:', 'python:', 'menu:', 'init python:')
                                    or s.startswith(('menu ', 'python '))):
                kids, i = self._children(lines, i, ind)
                if s.startswith('if '):
                    out.append(dict(t='if', id=self._new_id(), at=where,
                                    branches=[(s[3:-1].strip(), self._block(fname, kids, 0, None)[0])]))
                elif s.startswith('elif ') and out and out[-1]['t'] == 'if':
                    out[-1]['branches'].append((s[5:-1].strip(), self._block(fname, kids, 0, None)[0]))
                elif s == 'else:' and out and out[-1]['t'] == 'if':
                    out[-1]['branches'].append((None, self._block(fname, kids, 0, None)[0]))
                elif s.startswith('while '):
                    out.append(dict(t='if', id=self._new_id(), at=where, loop=True,
                                    branches=[(s[6:-1].strip(), self._block(fname, kids, 0, None)[0])]))
                elif s.startswith('python'):
                    base = min((_indent(r) for _, r in kids if r.strip()), default=0)
                    out.append(dict(t='py', at=where, code='\n'.join(r[base:] for _, r in kids)))
                else:
                    out.append(self._menu(fname, kids, where))
                continue
            out.append(self._simple(s, where))
        return [x for x in out if x], i

    def _children(self, lines, i, ind):
        kids = []
        while i < len(lines):
            no, raw = lines[i]
            if raw.strip() and _indent(raw) <= ind and not raw.strip().startswith('#'):
                break
            kids.append((no, raw))
            i += 1
        return kids, i

    def _menu(self, fname, kids, where):
        choices = []
        base = min((_indent(r) for _, r in kids if r.strip() and not r.strip().startswith('#')), default=0)
        j = 0
        while j < len(kids):
            no, raw = kids[j]
            s = _strip_comment(raw).strip()
            j += 1
            if not s or _indent(raw) != base:
                continue
            m = re.match(r'^(["\'])(.*?)\1\s*(?:if\s+(.*))?:$', s)
            if not m:
                continue
            sub = []
            while j < len(kids) and (not kids[j][1].strip() or _indent(kids[j][1]) > base):
                sub.append(kids[j])
                j += 1
            choices.append((m.group(3), m.group(2), self._block(fname, sub, 0, None)[0]))
        return dict(t='menu', id=self._new_id(), at=where, choices=choices)

    def _simple(self, s, where):
        lines_ids = []
        for call in re.findall(r'r13_v111_lines\(\[([^\]]*)\]', s):
            lines_ids += re.findall(r'MS14_\w+', call)
        blocks = re.findall(r'r13_nw_block\(\s*["\']([^"\']+)["\']', s)
        if lines_ids or blocks:
            return dict(t='lines', at=where, rids=lines_ids, blocks=blocks)
        if s.startswith('$'):
            return dict(t='py', at=where, code=s[1:].strip())
        if s.startswith('jump '):
            target = s[5:].strip()
            return dict(t='jump', at=where, target=None if target.startswith('expression') else target)
        if s.startswith('call '):
            rest = s[5:].strip()
            if rest.startswith(('screen ', 'expression ')):
                return None
            m = re.match(r'([A-Za-z_][\w.]*)\s*(\((.*)\))?', rest)
            if not m:
                return None
            return dict(t='call', at=where, target=m.group(1), args=m.group(3) or '')
        if s == 'return' or s.startswith('return '):
            return dict(t='return', at=where)
        return None


# ---------------------------------------------------------------- 값 판정
class Evaluator:
    """한 가지 값 조합(assign)으로 식을 계산한다. 없는 키는 NeedKey, 모르는 것은 Unknown."""

    CONSTS = {'True': True, 'False': False, 'None': None, 'R13_NW_TRIES': 5, 'R13_NW_FROZEN_AT': 4}

    def __init__(self, game, assign):
        self.g = game
        self.a = assign
        self.local = {}
        self.stack = []

    def get(self, key):
        if key not in self.a:
            raise NeedKey(key)
        v = self.a[key]
        if v is ANY:
            raise Unknown(key)
        return v

    def dead(self):
        out = [w for w, k in self.g.lives
               if self.get(k) is False or (w == 'kid_dodam' and self.get('route12') == 'late_exposure')]
        names = self.get('departed_names') or ()
        return out + [p for p in names if p != 'daram' and p not in out]

    def call(self, name, args):
        if name == 'r13_v111_value':
            return self.get(args[0])
        if name == 'r13_v111_owned':
            return self.get('owned:' + args[0])
        if name == 'r13_v111_person_alive':
            return self.get(self.g.life_key(args[0])) is not False
        if name == 'r13_v111_actor_ready':
            p = args[0]
            if p == 'dad':
                return True
            if self.get(self.g.life_key(p)) is False:
                return False
            if self.get('departed:' + p) is True:
                return False
            raise Unknown('actor_ready')
        if name == 'r13_nw_dead':
            return self.dead()
        if name == 'r13_nw_loss_count':
            return len(self.dead())
        if name == 'r13_nw_listed':
            return [p for p in self.g.listable if self.get('listed:' + p)]
        if name in self.g.funcs:
            return self.user(name, args)
        simple = {'len': len, 'bool': bool, 'set': set, 'list': list, 'tuple': tuple, 'sorted': sorted,
                  'str': str, 'int': int, 'any': any, 'all': all, 'max': max, 'min': min}
        if name in simple:
            return simple[name](*args)
        raise Unknown(name)

    def user(self, name, args):
        """규칙 파일의 판정 함수(r13_nw_dead·r13_nw_ending14 등)를 본문 그대로 계산한다. 모르는 값에서 갈리는
        if 는 양쪽을 다 따라가 가능한 결과를 모은다. 결과가 여럿이면 그 호출을 하나의 값처럼 펼쳐 본다."""
        key = ('call', name, freeze(list(args)))
        if key in self.a:
            v = self.a[key]
            if v is ANY:
                raise Unknown(name)
            return v
        fn = self.g.funcs[name]
        if len(self.stack) > 8:
            raise Unknown('depth')
        params = [a.arg for a in fn.args.args]
        if len(args) != len(params):
            raise Unknown('args')
        saved = self.local
        self.stack.append(name)
        try:
            results = self.fork(fn.body, dict(zip(params, args)))
        finally:
            self.stack.pop()
            self.local = saved
        if len(results) == 1:
            v = next(iter(results))
            if v is ANY:
                raise Unknown(name)
            return v
        raise NeedKey(key, frozenset(results))

    def fork(self, body, local):
        self.local = local
        for idx, st in enumerate(body):
            rest = body[idx + 1:]
            if isinstance(st, ast.Return):
                try:
                    return {freeze(self.ev(st.value)) if st.value is not None else None}
                except Unknown:
                    return {ANY}
            if isinstance(st, ast.If):
                try:
                    t = self.ev(st.test)
                except Unknown:
                    return self.fork(st.body + rest, dict(local)) | self.fork(st.orelse + rest, dict(local))
                return self.fork((st.body if t else st.orelse) + rest, local)
            try:
                if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
                    local[st.targets[0].id] = self.ev(st.value)
                elif isinstance(st, ast.AugAssign) and isinstance(st.target, ast.Name) and isinstance(st.op, ast.Add):
                    cur = local.get(st.target.id)
                    if cur is ANY:
                        raise Unknown('local')
                    val = self.ev(st.value)
                    local[st.target.id] = tuple(cur) + tuple(val) if isinstance(cur, (list, tuple)) else cur + val
                elif isinstance(st, ast.Expr):
                    continue  # 설명 글·알림 같은 부수 효과는 판정과 무관하다
                else:
                    return {ANY}
            except Unknown:
                if isinstance(st, ast.Assign):
                    local[st.targets[0].id] = ANY
                elif isinstance(st, ast.AugAssign):
                    local[st.target.id] = ANY
        return {None}

    def ev(self, n):
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.Name):
            if n.id in self.local:
                if self.local[n.id] is ANY:
                    raise Unknown(n.id)
                return self.local[n.id]
            if n.id in self.CONSTS:
                return self.CONSTS[n.id]
            if n.id in self.g.consts:
                return self.g.consts[n.id]
            raise Unknown(n.id)
        if isinstance(n, (ast.Tuple, ast.List)):
            return tuple(self.ev(e) for e in n.elts)
        if isinstance(n, ast.Set):
            return {self.ev(e) for e in n.elts}
        if isinstance(n, ast.BoolOp):
            return self.boolop(n)
        if isinstance(n, ast.UnaryOp):
            v = self.ev(n.operand)
            if isinstance(n.op, ast.Not):
                return not v
            if isinstance(n.op, ast.USub):
                return -v
            raise Unknown('unary')
        if isinstance(n, ast.BinOp):
            a, b = self.ev(n.left), self.ev(n.right)
            try:
                if isinstance(n.op, ast.Add):
                    return a + b
                if isinstance(n.op, ast.Sub):
                    return a - b
                if isinstance(n.op, ast.Mult):
                    return a * b
                if isinstance(n.op, ast.Mod):
                    return a % b
                if isinstance(n.op, ast.BitAnd):
                    return set(a) & set(b)
                if isinstance(n.op, ast.BitOr):
                    return set(a) | set(b)
            except TypeError:
                raise Unknown('binop')
            raise Unknown('binop')
        if isinstance(n, ast.Compare):
            left = self.ev(n.left)
            for op, right_n in zip(n.ops, n.comparators):
                right = self.ev(right_n)
                try:
                    ok = {ast.Eq: lambda: left == right, ast.NotEq: lambda: left != right,
                          ast.Is: lambda: left is right, ast.IsNot: lambda: left is not right,
                          ast.In: lambda: left in right, ast.NotIn: lambda: left not in right,
                          ast.Lt: lambda: left < right, ast.LtE: lambda: left <= right,
                          ast.Gt: lambda: left > right, ast.GtE: lambda: left >= right}[type(op)]()
                except (TypeError, KeyError):
                    raise Unknown('compare')
                if not ok:
                    return False
                left = right
            return True
        if isinstance(n, ast.IfExp):
            return self.ev(n.body) if self.ev(n.test) else self.ev(n.orelse)
        if isinstance(n, ast.Call):
            if not isinstance(n.func, ast.Name) or n.keywords:
                raise Unknown('call')
            if n.func.id in ('any', 'all') and len(n.args) == 1 and isinstance(n.args[0], ast.GeneratorExp):
                vals = self.comp(n.args[0])
                return any(vals) if n.func.id == 'any' else all(vals)
            return self.call(n.func.id, [self.ev(a) for a in n.args])
        if isinstance(n, (ast.ListComp, ast.GeneratorExp)):
            return tuple(self.comp(n))
        raise Unknown(type(n).__name__)

    def boolop(self, n):
        # 하나라도 확실히 거짓(and)·참(or)이면 나머지를 몰라도 답이 정해진다.
        is_and = isinstance(n.op, ast.And)
        unknown = None
        last = None
        for v_n in n.values:
            try:
                v = self.ev(v_n)
            except Unknown as e:
                unknown = e
                continue
            last = v
            if is_and and not v:
                return v
            if not is_and and v:
                return v
        if unknown is not None:
            raise unknown
        return last

    def comp(self, n):
        if len(n.generators) != 1:
            raise Unknown('comp')
        gen = n.generators[0]
        tgt = gen.target
        names = [tgt.id] if isinstance(tgt, ast.Name) else [e.id for e in getattr(tgt, 'elts', []) if isinstance(e, ast.Name)]
        if not names or (not isinstance(tgt, ast.Name) and len(names) != len(tgt.elts)):
            raise Unknown('comp')
        out = []
        for item in self.ev(gen.iter):
            vals = [item] if isinstance(tgt, ast.Name) else list(item)
            for k, v in zip(names, vals):
                self.local[k] = v
            if all(self.ev(c) for c in gen.ifs):
                out.append(self.ev(n.elt))
        return out


class Values:
    """경로별 상태: 갈림 결과 묶음(열쇠) -> {값 이름: 가능한 값 집합}. 없는 이름은 처음 값."""

    def __init__(self, game):
        self.g = game

    def init_dom(self, key):
        if key == '_stage':
            return frozenset()
        if key in self.g.external_keys or any(key.startswith(p) for p in self.g.external_prefixes):
            return frozenset((ANY,))
        if key in self.g.initial:
            return frozenset((self.g.initial[key],))
        if key.startswith('owned:'):
            return frozenset((False,))
        return frozenset((None,))

    def dom(self, vs, key):
        return vs[key] if key in vs else self.init_dom(key)

    def join_vs(self, a, b):
        if a is b:
            return a
        out = dict(a)
        for k, v in b.items():
            av = a.get(k)
            if av is None:
                av = self.init_dom(k)
            if av is v or av == v:
                continue
            out[k] = av | v if k == '_stage' else norm(av | v)
        for k, av in a.items():
            if k not in b and k != '_stage':
                init = self.init_dom(k)
                if av != init:
                    out[k] = norm(av | init)
        return out

    def join(self, s1, s2):
        if s1 is None:
            return s2
        if s2 is None:
            return s1
        out = dict(s1)
        for k, vs in s2.items():
            out[k] = self.join_vs(s1[k], vs) if k in s1 else vs
        return out

    # 조건 판정 ---------------------------------------------------------------
    def enumerate(self, node, vs):
        """식을 값 조합마다 계산한다. [(조합, 결과 또는 Unknown)]. 조합이 너무 많으면 None."""
        results, stack, count = [], [{}], 0
        while stack:
            a = stack.pop()
            count += 1
            if count > ENUM_LIMIT:
                return None
            try:
                results.append((a, Evaluator(self.g, a).ev(node)))
            except NeedKey as e:
                for v in (e.dom if e.dom is not None else self.dom(vs, e.key)):
                    b = dict(a)
                    b[e.key] = v
                    stack.append(b)
            except Unknown:
                results.append((a, Unknown))
            except Exception:
                results.append((a, Unknown))
        return results

    def refine_vs(self, node, vs, want):
        """조건이 want 일 수 있는 조합만 남긴 상태. 불가능하면 None. 판정 못 하면 그대로."""
        res = self.enumerate(node, vs)
        if res is None:
            return vs
        kept = [a for a, out in res if out is Unknown or bool(out) == want]
        if not kept:
            return None
        if all(out is Unknown for _, out in res):
            return vs
        out = dict(vs)
        keys = set().union(*[set(a) for a in kept])
        for k in keys:
            if isinstance(k, str) and all(k in a for a in kept):
                out[k] = frozenset(a[k] for a in kept)
        return out

    def split_vs(self, node, vs):
        """값 식의 결과마다 (값, 그 결과를 내는 조합만 남긴 상태). 계산 못 한 조합은 ANY 로 묶는다."""
        res = self.enumerate(node, vs)
        if res is None:
            return [(ANY, vs)]
        groups = collections.defaultdict(list)
        for a, out in res:
            groups[ANY if out is Unknown else freeze(out)].append(a)
        out = []
        for v, kept in groups.items():
            sub = dict(vs)
            for k in set().union(*[set(a) for a in kept]):
                if isinstance(k, str) and all(k in a for a in kept):
                    sub[k] = frozenset(a[k] for a in kept)
            out.append((v, sub))
        return out

    def refine(self, state, node, want):
        if node is None:
            return state
        out = {}
        for key, vs in state.items():
            r = self.refine_vs(node, vs, want)
            if r is not None:
                out[key] = r
        return out

    def values_of(self, node, vs):
        """값 식이 가질 수 있는 값들(모르면 ANY)."""
        res = self.enumerate(node, vs)
        if res is None:
            return frozenset((ANY,))
        return norm(ANY if out is Unknown else freeze(out if not isinstance(out, set) else sorted(out)) for _, out in res)

    def certainty(self, node, state):
        """조건이 어떻게 될 수 있는가: {True, False} 의 부분집합, 판정 못 하면 None."""
        seen = set()
        for vs in state.values():
            res = self.enumerate(node, vs)
            if res is None or any(out is Unknown for _, out in res):
                return None
            seen |= {bool(out) for _, out in res}
        return seen


def parse_expr(src):
    try:
        return ast.parse(src, mode='eval').body
    except SyntaxError:
        return None


# ---------------------------------------------------------------- 흐름 따라가기
class Analyzer:
    def __init__(self, game, story=None):
        self.g = game
        self.story = story or Story(game.story)
        self.V = Values(game)
        self.entry = {}          # 라벨 -> 들어올 때 상태
        self.sites = {}          # 위치 -> dict(stmt, label, path, state)
        self.unknown_guards = collections.Counter()
        self.persons = set(game.speakers.values()) | set(game.listable) | {p for p, _ in game.lives}
        self.read_keys, self.read_prefixes = self.reads()
        # 판정 함수의 결과로 정해지는 값(예: ending14 = r13_nw_ending14())은 경로 열쇠에 넣는다. 그 값으로
        # 갈라 가는 라벨(결말마다)에서 그 값을 만든 상태(떠난 사람·죽은 사람)와의 짝이 섞이지 않게.
        split = set()
        for text in game.story.values():
            for key, fn in re.findall(r"r13_v111_set\(\s*['\"]([^'\"]+)['\"]\s*,\s*(\w+)\(\)\s*\)", text):
                if fn in game.funcs:
                    split.add(key)
        self.split = sorted(split) + [k for k in EXTRA_SPLIT if k not in split and self.tracked(k)]
        self.part_names = ['fate:' + f for f in game.fates] + self.split
        game.part_names = [f for f in game.fates] + self.split
        self.edges = collections.defaultdict(set)
        self._reach = {}
        self.rets = {}           # 라벨 -> 그 라벨의 return 지점 상태
        self.static_calls()

    def reads(self):
        """조건(when·if·menu·값 식)에서 읽는 값 이름. 읽히지 않는 값은 들고 다니지 않는다(속도)."""
        texts = list(self.g.when_src.values())

        def walk(body):
            for s in body:
                if s['t'] == 'if':
                    for c, sub in s['branches']:
                        texts.append(c or '')
                        walk(sub)
                elif s['t'] == 'menu':
                    for c, _t, sub in s['choices']:
                        texts.append(c or '')
                        walk(sub)
                elif s['t'] == 'py':
                    # 대본 코드에서는 읽는 호출의 인자만(쓰는 키까지 넣으면 모든 값을 들고 다니게 된다).
                    texts.extend(m.group(0) for m in re.finditer(
                        r'r13_v111_(?:value|owned|person_alive|actor_ready)\(\s*["\'][^"\']+["\']\s*\+?', s['code']))
        for lab in self.story.labels.values():
            walk(lab['body'])
        keys, prefixes = set(), set()
        for t in texts:
            keys.update(re.findall(r'["\']([^"\'%]+)["\']', t))
            prefixes.update(re.findall(r'["\']([a-z_]+:)(?:%|["\']\s*\+)', t))
        keys |= {k for _, k in self.g.lives} | set(self.g.life.values()) | {'day', 'route12', 'departed_names'}
        prefixes |= {'fate:', 'meeting:', 'listed:', 'departed:', 'alive:'}
        return keys, prefixes

    def tracked(self, key):
        if key.startswith('_') or key in self.read_keys:
            return True
        if key.startswith('owned:'):
            return key[6:] in self.read_keys
        i = key.find(':')
        return i > 0 and key[:i + 1] in self.read_prefixes

    def initial_state(self):
        vs = {k: frozenset((None,)) for k in self.part_names}
        return {tuple(None for _ in self.part_names): vs}

    def key_of(self, vs):
        return tuple(next(iter(vs.get(k, frozenset((None,))))) for k in self.part_names)

    def static_calls(self):
        """call 대상마다 return 이 나올 수 있는 라벨(jump·이어짐으로 닿는 곳)과, 그 return 을 기다리는 호출 라벨."""
        labels = self.story.labels
        jumps = collections.defaultdict(set)
        self.call_sites = collections.Counter()
        callers = collections.defaultdict(set)
        has_return = set()

        def walk(name, body):
            for st in body:
                if st['t'] == 'jump' and st['target']:
                    jumps[name].add(st['target'])
                elif st['t'] == 'return':
                    has_return.add(name)
                elif st['t'] == 'call':
                    if st['target'] in labels:
                        self.call_sites[st['target']] += 1
                        callers[st['target']].add(name)
                    else:
                        jumps[name].update(n for n in re.findall(r'["\']([A-Za-z_]\w*)["\']', st['args']) if n in labels)
                for _c, sub in st.get('branches', ()):
                    walk(name, sub)
                for _c, _t, sub in st.get('choices', ()):
                    walk(name, sub)
        for name, lab in labels.items():
            walk(name, lab['body'])
            if lab['next']:
                jumps[name].add(lab['next'])
        preds = collections.defaultdict(set)
        for x, ys in jumps.items():
            for y in ys:
                preds[y].add(x)
        for t, cs in callers.items():
            for c in cs:
                preds[t].add(c)
        self.closure = {}
        for target in callers:
            # 그 호출 라벨에서만 들어갈 수 있는 라벨까지만 본다. 본편 흐름으로 빠져나가는 jump 를 따라가면
            # 다른 날의 return 까지 모여 상태가 섞인다.
            seen = {target}
            grew = True
            while grew:
                grew = False
                for x in list(seen):
                    for y in jumps.get(x, ()):
                        if y not in seen and y in labels and preds[y] <= seen:
                            seen.add(y)
                            grew = True
            self.closure[target] = seen
        self.has_return = has_return
        self.ret_waiters = collections.defaultdict(set)
        for target, seen in self.closure.items():
            for y in seen:
                self.ret_waiters[y] |= callers[target]

    def after_call(self, target, state):
        """call 이 돌아온 뒤의 상태. 호출된 라벨이 바꾼 값(탑승자 목록 등)을 이어받는다."""
        seen = self.closure.get(target, ())
        if not any(y in self.has_return for y in seen):
            return state
        ret = None
        for y in seen:
            ret = self.V.join(ret, self.rets.get(y))
        if ret is None:
            return None
        if self.call_sites[target] == 1:
            return ret
        # 여러 곳에서 부르면 같은 경로 열쇠의 return 만 잇는다(다른 호출 지점의 상태가 섞이지 않게).
        return {k: ret.get(k, vs) for k, vs in state.items()}

    def reach(self, a, b):
        """라벨 a 에서 b 로 갈 수 있는가(jump·call·이어짐)."""
        if a not in self._reach:
            seen, todo = set(), [a]
            while todo:
                x = todo.pop()
                for y in self.edges.get(x, ()):
                    if y not in seen:
                        seen.add(y)
                        todo.append(y)
            self._reach[a] = seen
        return b in self._reach[a]

    def run(self, entry=ENTRY):
        labels = self.story.labels
        if entry not in labels:
            entry = self.story.order[0]
        self.entry = {entry: self.initial_state()}
        # 대본 순서가 앞선 라벨부터 처리한다(날이 흐르는 순서라 다시 처리하는 일이 적다).
        rank = {n: i for i, n in enumerate(self.story.order)}
        work = [(rank[entry], entry)]
        queued = {entry}
        self.passes = 0
        while work:
            self.passes += 1
            if self.passes > 200000:
                raise RuntimeError('흐름 따라가기가 끝나지 않는다')
            _, name = heapq.heappop(work)
            queued.discard(name)
            lab = labels[name]
            outs = []
            self._ret_changed = False
            end = self.block(lab['body'], self.entry[name], name, (), outs)
            if self._ret_changed:
                for w in self.ret_waiters.get(name, ()):
                    if w not in queued and w in self.entry:
                        heapq.heappush(work, (rank[w], w))
                        queued.add(w)
            if end is not None and lab['next']:
                outs.append((lab['next'], end))
            for target, st in outs:
                if target in labels:
                    self.edges[name].add(target)
                if target not in labels or not st:
                    continue
                old = self.entry.get(target)
                new = self.V.join(old, st)
                if new != old:
                    self.entry[target] = new
                    if target not in queued:
                        heapq.heappush(work, (rank[target], target))
                        queued.add(target)
        return self

    def block(self, body, state, label, path, outs):
        for stmt in body:
            if not state:
                return None
            t = stmt['t']
            if t == 'py':
                state = self.py(stmt['code'], state)
            elif t == 'lines':
                at = stmt['at']
                old = self.sites.get(at)
                self.sites[at] = dict(stmt=stmt, label=label, path=path,
                                      state=self.V.join(old['state'], state) if old else state)
            elif t == 'jump':
                if stmt['target']:
                    outs.append((stmt['target'], state))
                return None
            elif t == 'return':
                old = self.rets.get(label)
                new = self.V.join(old, state)
                if new != old:
                    self.rets[label] = new
                    self._ret_changed = True
                return None
            elif t == 'call':
                state = self.call(stmt, state, outs)
                if stmt['target'] in self.story.labels:
                    state = self.after_call(stmt['target'], state)
            elif t == 'if':
                state = self.branch(stmt, state, label, path, outs)
            elif t == 'menu':
                res = None
                for i, (cond, _text, sub) in enumerate(stmt['choices']):
                    st = self.guard(cond, state, True)
                    res = self.V.join(res, self.block(sub, st, label, path + ((stmt['id'], i),), outs))
                state = res
        return state

    def guard(self, cond, state, want):
        if cond is None:
            return state
        node = parse_expr(cond)
        if node is None:
            self.unknown_guards[cond] += 1
            return state
        if self.V.certainty(node, state) is None:
            self.unknown_guards[cond] += 1
        return self.V.refine(state, node, want)

    def branch(self, stmt, state, label, path, outs):
        res, rest = None, state
        has_else = False
        for i, (cond, sub) in enumerate(stmt['branches']):
            if cond is None:
                has_else = True
                st, rest = rest, {}
            else:
                st = self.guard(cond, rest, True)
                rest = self.guard(cond, rest, False)
            res = self.V.join(res, self.block(sub, st, label, path + ((stmt['id'], i),), outs))
        if not has_else:
            res = self.V.join(res, rest)
        if stmt.get('loop'):
            res = self.V.join(res, state)
        return res

    def call(self, stmt, state, outs):
        target, args = stmt['target'], stmt['args']
        if target in self.story.labels:
            outs.append((target, state))
        # 증명 화면이 돌려줄 라벨 이름(성공·오답·힌트)은 그 라벨로 가는 길이다.
        for name in re.findall(r'["\']([A-Za-z_]\w*)["\']', args):
            if name in self.story.labels and name != target:
                outs.append((name, state))
        if target == 'r13_v111_travel':
            m = re.search(r'\[([^\]]*)\]', args)
            if m:
                state = self.stage(state, re.findall(r'["\']([\w]+)["\']', m.group(1)))
        if target == 'r13_v111_wait':
            m = re.match(r'\s*["\']([^"\']+)["\']', args)
            if m and m.group(1) in self.g.bindings:
                state = self.stage(state, self.g.bindings[m.group(1)])
        return state

    # 값 바꾸기 ----------------------------------------------------------------
    def stage(self, state, people, reset=False):
        out = {}
        for k, vs in state.items():
            vs = dict(vs)
            vs['_stage'] = (frozenset() if reset else self.V.dom(vs, '_stage')) | frozenset(people)
            out[k] = vs
        return out

    def py(self, code, state):
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return state
        consts = {n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
        local = {'_consts': consts}
        for node in tree.body:
            state = self.exec_node(node, state, may=False, local=local)
        return state

    def exec_node(self, node, state, may, local):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            return self.effect(node.value, state, may, local)
        if isinstance(node, ast.Assign):
            tgt = node.targets[0]
            if isinstance(tgt, ast.Name):
                local[tgt.id] = node.value
            elif ast.unparse(tgt).replace("'", '"') == 'room13["v111"]["people"]':
                people = []
                if isinstance(node.value, (ast.List, ast.Tuple)):
                    people = [e.value for e in node.value.elts if isinstance(e, ast.Constant)]
                return self.stage(state, people, reset=True)
            for sub in ast.walk(node.value):
                if isinstance(sub, ast.Call):
                    state = self.effect(sub, state, may, local)
            return state
        if isinstance(node, (ast.If, ast.For, ast.While)):
            for sub in node.body + getattr(node, 'orelse', []):
                state = self.exec_node(sub, state, True, local)
            return state
        return state

    def put(self, state, key, vals, may):
        if not self.tracked(key):
            return state
        out = {}
        for k, vs in state.items():
            vs = dict(vs)
            vs[key] = norm(self.V.dom(vs, key) | vals) if may else norm(vals)
            out[k] = vs
        return self.rekey(out) if key in self.part_names else out

    def rekey(self, state):
        out = {}
        for vs in state.values():
            k = self.key_of(vs)
            out[k] = self.V.join_vs(out[k], vs) if k in out else vs
        return out

    def apply_ops(self, state, ops, may):
        for op in ops:
            if op.get('op') == 'set':
                state = self.put(state, op['field'], frozenset((freeze(op['value']),)), may)
            elif op.get('op') == 'acquire':
                state = self.put(state, 'owned:' + op['key'], frozenset((True,)), may)
        return state

    def effect(self, call, state, may, local):
        if not isinstance(call.func, ast.Name):
            return state
        name, args = call.func.id, call.args

        def const(i):
            return args[i].value if len(args) > i and isinstance(args[i], ast.Constant) else None

        if name == 'r13_v111_set' and len(args) >= 2:
            key = const(0)
            if key is None:
                # 동적 키("departed:"+_p): 그 앞머리를 가진 모든 사람이 이 값일 수 있다.
                prefix = None
                k = args[0]
                if isinstance(k, ast.BinOp) and isinstance(k.left, ast.Constant) and isinstance(k.left.value, str):
                    prefix = k.left.value
                if prefix:
                    # 누가 해당되는지는 코드가 정한다. 같은 코드 안에 적힌 인물과 그 경로에서 명단에 오를 수 있는
                    # 사람만 후보로 둔다(모든 사람을 후보로 두면 할머니·촌장까지 떠난 것으로 잡힌다).
                    named = set(local.get('_consts', ())) & self.persons
                    vals = self.values_any(args[1], state)
                    out = {}
                    for kk, vs in state.items():
                        vs = dict(vs)
                        cands = named | {p for p in self.g.listable if True in self.V.dom(vs, 'listed:' + p)}
                        for p in sorted(cands):
                            if self.tracked(prefix + p):
                                vs[prefix + p] = norm(self.V.dom(vs, prefix + p) | vals)
                        out[kk] = vs
                    return out
                return state
            if not self.tracked(key):
                return state
            if isinstance(args[1], ast.Name) and args[1].id in local:
                return self.put(state, key, frozenset((ANY,)), may)
            if key in self.split and not may:
                # 값마다 그 값을 만든 조합만 남겨 따로 들고 간다.
                out = {}
                for k, vs in state.items():
                    for v, sub in self.V.split_vs(args[1], vs):
                        sub = dict(sub)
                        sub[key] = frozenset((v,))
                        nk = self.key_of(sub)
                        out[nk] = self.V.join_vs(out[nk], sub) if nk in out else sub
                return out
            out = {}
            for k, vs in state.items():
                vals = self.literal_or_eval(args[1], vs)
                vs = dict(vs)
                vs[key] = norm(self.V.dom(vs, key) | vals) if may else vals
                out[k] = vs
            return self.rekey(out) if key in self.part_names else out
        if name == 'r13_v111_commit' and const(0) in self.g.records:
            return self.apply_ops(state, self.g.records[const(0)].get('operations', []), may)
        if name == 'r13_v111_option' and const(0) in self.g.options:
            return self.apply_ops(state, self.g.options[const(0)].get('operations', []), may)
        if name == 'r13_v111_apply' and len(args) >= 2:
            return self.apply_ops(state, self.ops_literal(args[1]), may)
        if name == 'r13_fork_set_fate' and const(0) and const(1):
            out = {}
            for k, vs in state.items():
                vs = dict(vs)
                cur = self.V.dom(vs, 'fate:' + const(0))
                if None in cur:
                    vs['fate:' + const(0)] = frozenset((const(1),)) if cur == {None} or not may else cur | {const(1)}
                out[k] = vs
            return self.rekey(out)
        if name == 'r13_nw_meeting_end' and const(0) and const(1):
            out = {}
            for k, vs in state.items():
                vs = dict(vs)
                key = 'meeting:' + const(0)
                cur = self.V.dom(vs, key)
                new = (cur - {None}) | ({const(1)} if None in cur else set())
                vs[key] = norm(cur | new if may else new)
                out[k] = vs
            return out
        if name == 'r13_nw_list' and const(0):
            return self.put(state, 'listed:' + const(0), frozenset((True,)), may)
        if name == 'r13_nw_acquire' and const(0):
            return self.put(state, 'owned:' + const(0), frozenset((True,)), may)
        if name in ('r13_v111_arrive', 'r13_v111_join') and args and isinstance(args[0], (ast.List, ast.Tuple)):
            return self.stage(state, [e.value for e in args[0].elts if isinstance(e, ast.Constant)])
        if name == 'r13_v111_scene' and const(0):
            return self.put(state, '_scene', frozenset((const(0),)), may)
        return state

    def values_any(self, node, state):
        out = frozenset()
        for vs in state.values():
            out |= self.literal_or_eval(node, vs)
        return norm(out)

    def literal_or_eval(self, node, vs):
        try:
            return frozenset((freeze(ast.literal_eval(node)),))
        except (ValueError, SyntaxError, TypeError):
            return self.V.values_of(node, vs)

    def ops_literal(self, node):
        out = []
        if not isinstance(node, (ast.List, ast.Tuple)):
            return out
        for e in node.elts:
            try:
                if isinstance(e, ast.Dict):
                    out.append({ast.literal_eval(k): ast.literal_eval(v) for k, v in zip(e.keys, e.values)})
                elif isinstance(e, ast.Call) and getattr(e.func, 'id', '') == 'dict':
                    out.append({kw.arg: ast.literal_eval(kw.value) for kw in e.keywords})
            except (ValueError, SyntaxError):
                continue
        return out


# ---------------------------------------------------------------- 줄 모으기
class Row:
    __slots__ = ('id', 'rid', 'day', 'speaker', 'person', 'text', 'conds', 'when', 'site', 'label', 'path',
                 'scene', 'state', 'source', 'variant')

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


def who_of(game, row, base=None):
    kind = row.get('kind')
    if kind == 'thought':
        return '아빠'
    if kind in ('action', 'narration', 'system', 'evidence', 'choice'):
        return None
    return row.get('speaker') or base


def collect_rows(game, an):
    """지점마다 실제로 나올 수 있는 줄(원문·교체 변형·앞뒤 덧줄·블록 줄)과 그 줄의 조건."""
    patch_of = {}
    for day, patch in game.patches.items():
        for key in ('replace', 'before', 'after', 'blocks'):
            for rid, v in patch.get(key, {}).items():
                patch_of[(key, rid)] = v
    drops = collections.defaultdict(list)
    for patch in game.patches.values():
        for item in patch.get('drop', []):
            rid, when = (item, 'always') if isinstance(item, str) else (item.get('id'), item.get('when', 'always'))
            drops[rid].append(when)
    rows = []
    for at, site in sorted(an.sites.items()):
        st = site['state']
        days = {v for vs in st.values() for v in an.V.dom(vs, 'day') if isinstance(v, int)}
        site_day = min(days) if len(days) == 1 else None
        scenes = {v for vs in st.values() for v in an.V.dom(vs, '_scene') if isinstance(v, str)}

        def add(row, rid, conds, scene, day, source, variant=None):
            text = row.get('text', '')
            spk = who_of(game, row)
            rows.append(Row(id=row.get('id') or rid, rid=rid, day=day, speaker=spk, person=game.speakers.get(spk) if spk else None,
                            text=text, conds=conds, when=[w for w, _ in conds], site=at, label=site['label'], path=site['path'],
                            scene=scene, state=st, source=source, variant=variant))

        for rid in site['stmt']['rids']:
            m = re.match(r'MS14_D(\d\d)_', rid)
            day = int(m.group(1)) if m else site_day
            scene = rid.rsplit('_', 1)[0]
            for row in patch_of.get(('before', rid), []):
                add(row, rid, [(row.get('when', 'always'), True)], scene, day, 'before')
            rec = game.records.get(rid)
            drop_conds = [(w, False) for w in drops.get(rid, [])]
            if rec and rec.get('player_visible', True) and 'always' not in drops.get(rid, []):
                entry = patch_of.get(('replace', rid))
                variants = [] if entry is None else ([entry] if isinstance(entry, dict) else entry)
                base = dict(kind=rec.get('kind'), speaker=rec.get('speaker'))
                earlier = []
                default_seen = False
                for v in variants:
                    w = v.get('when', 'always')
                    row = dict(base, text=v.get('text', ''), id=rid + ('{%s}' % w if w != 'always' else ''))
                    add(row, rid, earlier + [(w, True)] + drop_conds, scene, day, 'replace', w)
                    if w == 'always':
                        default_seen = True
                        break
                    earlier.append((w, False))
                if not default_seen:
                    add(dict(base, text=rec.get('text', ''), id=rid), rid, earlier + drop_conds, scene, day, 'record')
            for row in patch_of.get(('after', rid), []):
                add(row, rid, [(row.get('when', 'always'), True)], scene, day, 'after')
        for name in site['stmt']['blocks']:
            m = re.search(r'(\d+)$', name)
            day = site_day or (int(m.group(1)) if m and 1 <= int(m.group(1)) <= 14 else None)
            scene = next(iter(scenes)) if len(scenes) == 1 else None
            for row in patch_of.get(('blocks', name), []):
                add(row, 'block:' + name, [(row.get('when', 'always'), True)], scene, day, 'block')
    return rows


def row_state(game, an, row):
    """줄의 조건을 걸러 낸 상태와, 해석 못 한 조건 이름들."""
    st = row.state
    unknown = []
    for w, want in row.conds:
        if w == 'always':
            if not want:
                return {}, unknown
            continue
        node = game.when.get(w)
        if node is None:
            unknown.append(w)
            continue
        if an.V.certainty(node, st) is None:
            unknown.append(w)
        st = an.V.refine(st, node, want)
    return st, unknown


# ---------------------------------------------------------------- 검사
def fmt_key(game, key):
    parts = ['%s=%s' % (f, v) for f, v in zip(game.keys(), key) if v is not None]
    return ', '.join(parts) or '갈림 전'


def summarize_keys(game, keys):
    keys = sorted(keys, key=lambda k: tuple('' if v is None else v for v in k))
    if not keys:
        return ''
    common = []
    for i, f in enumerate(game.keys()):
        vals = {k[i] for k in keys}
        if len(vals) == 1 and None not in vals:
            common.append('%s=%s' % (f, next(iter(vals))))
    text = ', '.join(common) or fmt_key(game, keys[0])
    return text + (' 외 %d개 경로' % (len(keys) - 1) if len(keys) > 1 and not common else
                   (' (%d개 경로)' % len(keys) if len(keys) > 1 else ''))


def finding(check, grade, row, conflict, keys, game, extra=None):
    return dict(check=check, grade=grade, id=row.id, day=row.day, speaker=row.speaker or '지문',
                when=' & '.join(('' if want else 'not ') + w for w, want in row.conds if w != 'always') or '-',
                label=row.label, site='%s:%d' % row.site, conflict=conflict, paths=summarize_keys(game, keys),
                text=row.text[:80], **(extra or {}))


def life_state(an, vs, person):
    """(죽음 확실, 죽음 가능, 떠남 확실, 떠남 가능)"""
    life = an.V.dom(vs, an.g.life_key(person))
    route12 = an.V.dom(vs, 'route12') if person == 'kid_dodam' else frozenset()
    dep = an.V.dom(vs, 'departed:' + person)
    dead_sure = (life == {False}) or (route12 == {'late_exposure'})
    dead_may = False in life or 'late_exposure' in route12
    return dead_sure, dead_may, dep == {True}, True in dep


def name_patterns(game):
    out = []
    for name, pid in list(game.speakers.items()) + list(NAME_ALIASES.items()):
        if len(name) < 2 or name in ROLE_NAMES or re.search(r'[0-9]', name):
            continue
        out.append((name, pid, re.compile(r'(?<![가-힣])' + re.escape(name) + r'(?!(차|밭|빛|꽃|떡))')))
    # 긴 이름부터(「부엉이 영감」이 「부엉이」보다 먼저)
    return sorted(out, key=lambda x: -len(x[0]))


def check_rows(game, an, rows, days=None):
    found, unknown_conds = [], collections.Counter()
    names = name_patterns(game)
    mortal = {p for p, _ in game.lives} | set(game.life) | set(game.listable)
    fate_words = [(f, set(rs), re.compile(p)) for f, rs, p in FATE_WORDS if f in game.fates]
    refined = []
    first_gone = gone_days(an, rows)
    for row in rows:
        if days and row.day not in days:
            continue
        if row.source == 'reaction':
            st, unk = row.state, []
        else:
            st, unk = row_state(game, an, row)
        for w in unk:
            unknown_conds[w] += 1
        if not st:
            continue
        refined.append((row, st))
        # D 화자 (반응 대사는 그 사람이 눈앞에 있을 때만 나오므로 화자는 보지 않는다)
        if row.person and row.person != 'dad' and row.source != 'reaction':
            sure, may = [], []
            for key, vs in st.items():
                ds, dm, ps, pm = life_state(an, vs, row.person)
                if ds or ps:
                    sure.append((key, '사망' if ds else '수레로 떠남'))
                elif dm or pm:
                    may.append((key, '사망' if dm else '수레로 떠남'))
            if sure:
                found.append(finding('D', '확실', row, '화자 %s: 그 경로에서 이미 %s' % (row.speaker, sure[0][1]), [k for k, _ in sure], game))
            elif may:
                found.append(finding('D', '의심', row, '화자 %s: 그 경로에서 %s일 수 있음' % (row.speaker, may[0][1]), [k for k, _ in may], game))
        # D 이름 언급
        if row.text and not re.search(PAST_MARKS, row.text):
            seen = set()
            masked = row.text
            for name, pid, pat in names:
                if pid in seen or pid not in mortal or pid == row.person or not pat.search(masked):
                    continue
                seen.add(pid)
                masked = pat.sub(' ', masked)
                # 이 줄의 조건이 그 사람의 생사를 이미 따진다면 쓴 사람이 경로를 알고 쓴 것이다.
                keys = (game.life_key(pid), pid) + DEATH_KEYS.get(pid, ())
                if any(k in game.when_src.get(w, '') for w, _ in row.conds for k in keys) or any(w.endswith(pid) for w, _ in row.conds):
                    continue
                # 죽은 날(떠난 날) 그 장면의 묘사는 현재형이 자연스럽다. 그 다음 날부터만 본다.
                hit = [(k, '사망' if life_state(an, vs, pid)[0] else '수레로 떠남') for k, vs in st.items()
                       if (life_state(an, vs, pid)[0] or life_state(an, vs, pid)[2])
                       and row.day is not None and gone_before(first_gone, pid, k, row.day)]
                if hit:
                    found.append(finding('D', '의심', row, '「%s」를 현재형으로 다룸: 그 경로에서 %s' % (name, hit[0][1]),
                                         [k for k, _ in hit], game, dict(mention=name)))
        # E 장면 등장인물
        actors = game.scene_actors.get(row.scene) if row.scene else None
        if actors and row.person and row.person not in ('dad', 'daram', 'mom') and not row.person.startswith(EXTRAS):
            stage = set().union(*[an.V.dom(vs, '_stage') for vs in st.values()])
            if row.person not in actors and row.person not in stage:
                # 말하는 사람은 화면에 걸어 들어오게 되어 있어(room13_v111_idle.rpy) 진행은 막히지 않는다. 의심.
                found.append(finding('E', '의심', row, '%s 장면 등장인물·무대 인원에 %s 없음' % (row.scene, row.person), list(st), game))
        # F 일어나지 않은 일
        for f, results, pat in fate_words:
            m = pat.search(row.text or '')
            if not m:
                continue
            i = game.fates.index(f)
            bad = [k for k in st if k[i] is not None and k[i] not in results]
            if bad:
                found.append(finding('F', '의심', row, '「%s」(%s=%s 의 일)인데 %s 경로에서도 나옴' % (
                    m.group(0), f, '/'.join(sorted(results)), '/'.join(sorted({k[i] for k in bad}))), bad, game,
                    dict(word=m.group(0))))
    found += check_repeats(game, an, refined)
    return found, unknown_conds


def gone_days(an, rows):
    """인물 -> [(경로 열쇠, 그 경로에서 죽음·떠남이 처음 확실해진 날)]. 줄이 나오는 지점의 상태로 센다."""
    out = collections.defaultdict(dict)
    people = {p for p, _ in an.g.lives} | set(an.g.life) | set(an.g.listable)
    seen = set()
    for row in sorted(rows, key=lambda r: r.day or 99):
        if row.day is None or row.site in seen:
            continue
        seen.add(row.site)
        for key, vs in row.state.items():
            for p in people:
                if key not in out[p]:
                    ls = life_state(an, vs, p)
                    if ls[0] or ls[2]:
                        out[p][key] = row.day
    return out


def gone_before(first_gone, pid, key, day):
    """그 경로(뒤에 갈림이 더 정해진 열쇠 포함)에서 day 보다 앞선 날에 이미 죽었거나 떠났는가."""
    for k1, d1 in first_gone.get(pid, {}).items():
        if d1 < day and all(a is None or a == b for a, b in zip(k1, key)):
            return True
    return False


def reaction_rows(game, an, rows):
    """주민 반응 대사(reactions.json). 그 날들의 대사 지점 상태를 모아 쓰고, 말하는 사람은 살아서 그 자리에 있다고 본다."""
    by_day = collections.defaultdict(dict)
    for row in rows:
        if row.day is None:
            continue
        cur = by_day[row.day]
        for key, vs in row.state.items():
            cur[key] = an.V.join_vs(cur[key], vs) if key in cur else vs
    out = []
    for kind in ('present', 'followups'):
        for i, item in enumerate(game.reactions.get(kind, [])):
            lo, hi = (item.get('days') or [1, 14])[:2]
            for day in range(lo, hi + 1):
                st = by_day.get(day)
                if not st:
                    continue
                person = item.get('person')
                life = ast.parse('r13_v111_person_alive(%r)' % person, mode='eval').body
                st = an.V.refine(st, life, True)
                for line in item.get('lines', []):
                    spk = who_of(game, line)
                    out.append(Row(id=line.get('id') or '%s#%d' % (kind, i), rid='reaction:%s:%d' % (kind, i), day=day, speaker=spk,
                                   person=game.speakers.get(spk) if spk else None, text=line.get('text', ''), conds=[], when=[],
                                   site=('reactions.json', i), label='reactions:' + kind, path=(), scene=None, state=st,
                                   source='reaction'))
    return out


def _plain(text):
    return re.sub(r'[\s.,!?…~·「」『』“”"\'()\-—]+', '', text or '')


def _exclusive_paths(p1, p2):
    a = dict(p1)
    return any(k in a and a[k] != v for k, v in p2)


def _write_once_conflict(an, vs1, vs2):
    for k in set(vs1) & set(vs2):
        if not k.startswith(WRITE_ONCE):
            continue
        a, b = vs1[k] - {None}, vs2[k] - {None}
        if a and b and ANY not in a and ANY not in b and None not in vs1[k] and None not in vs2[k] and not (a & b):
            return True
    return False


def _can_follow(an, ra, sa, rb, key):
    """줄 a 가 나온 뒤 줄 b 의 라벨에 들어갈 수 있는가. a 지점에서 정해진 한 번뿐인 값(회의 결과 등)을
    b 라벨의 들어오는 상태가 받아들이지 못하면 같은 판에 둘 다 나오지 않는다."""
    entry = an.entry.get(rb.label, {}).get(key)
    if entry is None:
        return False
    va = sa[key]
    for k, vals in va.items():
        if not isinstance(k, str) or not k.startswith(WRITE_ONCE) or None in vals or ANY in vals:
            continue
        vb = an.V.dom(entry, k)
        if ANY not in vb and not (vals & vb):
            return False
    return True


G_RATIO = 0.82
G_MIN_LEN = 10


def check_repeats(game, an, refined):
    """G: 같은 날·같은 경로에서 같은 인물이 거의 같은 말을 두 번."""
    out = []
    groups = collections.defaultdict(list)
    for row, st in refined:
        if row.person and row.person != 'dad' and row.day and len(_plain(row.text)) >= G_MIN_LEN:
            groups[(row.day, row.person)].append((row, st))
    reported = set()
    for items in groups.values():
        for i in range(len(items)):
            r1, s1 = items[i]
            for j in range(i + 1, len(items)):
                r2, s2 = items[j]
                if r1.id == r2.id or r1.rid == r2.rid and r1.source == r2.source == 'replace' or (r1.rid == r2.rid and r1.variant != r2.variant):
                    continue
                if r1.label == r2.label:
                    if _exclusive_paths(r1.path, r2.path):
                        continue
                elif not (an.reach(r1.label, r2.label) or an.reach(r2.label, r1.label)):
                    # 서로 갈 수 없는 라벨(같은 회의의 다른 경로 등)은 한 판에 함께 나오지 않는다.
                    continue
                ratio = difflib.SequenceMatcher(None, _plain(r1.text), _plain(r2.text)).ratio()
                if ratio < G_RATIO:
                    continue
                common = [k for k in s1 if k in s2 and not _write_once_conflict(an, s1[k], s2[k])]
                if r1.label != r2.label:
                    common = [k for k in common if _can_follow(an, r1, s1, r2, k) or _can_follow(an, r2, s2, r1, k)]
                if not common:
                    continue
                pair = tuple(sorted((r1.id, r2.id)))
                if pair in reported:
                    continue
                reported.add(pair)
                out.append(finding('G', '의심', r2, '같은 날 %s 의 말과 %.0f%% 같음: %s' % (r1.id, ratio * 100, r1.text[:40]),
                                   common, game, dict(other=r1.id)))
    return out


def world_table(game, an, rows):
    """날짜 x 갈림 결과별 생존·명단·떠남(그 날 대사 지점들의 상태를 모은 것)."""
    by_day = collections.defaultdict(dict)
    seen_sites = set()
    for row in rows:
        if row.day is None or row.site in seen_sites:
            continue
        seen_sites.add(row.site)
        cur = by_day[row.day]
        for key, vs in row.state.items():
            cur[key] = an.V.join_vs(cur[key], vs) if key in cur else vs
    people = sorted({p for p, _ in game.lives} | set(game.listable))
    names = game.keys()
    table = []
    for day in sorted(by_day):
        parts = by_day[day]
        facts = {}
        for key, vs in parts.items():
            ls = {p: life_state(an, vs, p) for p in people}
            facts[key] = dict(
                dead={p for p in people if ls[p][0]}, dead_may={p for p in people if ls[p][1]},
                listed={p for p in game.listable if an.V.dom(vs, 'listed:' + p) == {True}},
                listed_may={p for p in game.listable if True in an.V.dom(vs, 'listed:' + p)},
                gone={p for p in people if ls[p][3]})
        groups = [('모든 경로', list(parts))]
        for i, n in enumerate(names):
            for r in sorted({k[i] for k in parts if k[i] is not None}, key=str):
                groups.append(('%s=%s' % (n, r), [k for k in parts if k[i] == r]))
        for title, keys in groups:
            fs = [facts[k] for k in keys]
            sure = set.intersection(*[f['dead'] for f in fs])
            lsure = set.intersection(*[f['listed'] for f in fs])
            table.append(dict(day=day, paths=title, n=len(keys), dead=sorted(sure),
                              dead_may=sorted(set.union(*[f['dead_may'] for f in fs]) - sure),
                              listed=sorted(lsure), listed_may=sorted(set.union(*[f['listed_may'] for f in fs]) - lsure),
                              departed_may=sorted(set.union(*[f['gone'] for f in fs]))))
    return table


def death_points(game, story):
    """생존 값이 거짓이 되는 곳(원문 기록 연산과 대본의 r13_v111_set)."""
    life_keys = {k for _, k in game.lives} | set(game.life.values())
    out = []
    for rid, rec in game.records.items():
        for op in rec.get('operations', []):
            if op.get('op') == 'set' and op.get('field') in life_keys and op.get('value') is False:
                out.append((op['field'], rid))
    for fname, text in game.story.items():
        for n, line in enumerate(text.split('\n'), 1):
            for k in life_keys:
                if re.search(r"r13_v111_set\(\s*['\"]%s['\"]\s*,\s*False" % re.escape(k), line):
                    out.append((k, '%s:%d' % (fname, n)))
    return sorted(set(out))


# ---------------------------------------------------------------- 실행·출력
def audit(game=None, days=None):
    game = game or load_game()
    an = Analyzer(game).run()
    rows = collect_rows(game, an)
    found, unknown_conds = check_rows(game, an, rows + reaction_rows(game, an, rows), days)
    reached = set(an.entry)
    unreached = [n for n in an.story.order if n not in reached]
    return dict(game=game, analyzer=an, rows=rows, findings=found, unknown_conds=unknown_conds,
                unknown_guards=an.unknown_guards, unreached=unreached)


def counts(found):
    c = collections.Counter((f['check'], f['grade']) for f in found)
    return {'%s %s' % k: v for k, v in sorted(c.items())}


# 거짓 양성을 줄이려고 바꾼 기준(2026-10-24 첫 실행 때 건수 변화). 보고서 끝에 그대로 싣는다.
ADJUSTMENTS = [
    ('D 화자', '13일 수레 탑승자를 「모든 인물」에서 「그 python 블록에 적힌 인물 + 그 경로에서 명단에 오를 수 있는 사람」으로 좁힘', '149 -> 54'),
    ('D 화자', '규칙 파일의 판정 함수(r13_nw_ending14 등)를 본문대로 계산하고, 결말 값(ending14)을 경로 열쇠로 둠', '54 -> 28'),
    ('D 화자', '13일 수레 출발(cart_departed)을 경로 열쇠로 둠. 수레가 안 떠난 결말에서 판돌·나비·부엉이가 「떠났을 수 있음」으로 잡히던 것 제거', '28 -> 8'),
    ('D 이름', '과거·회상 표지(었·였·셨·던·더라 등)가 있는 줄, 죽은 날 당일 장면 묘사, 줄 조건이 그 사람 생사를 이미 따지는 줄은 뺌', '15 -> 6'),
    ('E', '말하는 사람은 화면에 걸어 들어오게 되어 있어(room13_v111_idle.rpy) 등급을 의심으로 내리고, 이름 없는 단역(v111_·ms14_)은 뺌', '27 -> 18'),
    ('F', '모든 경로에 있는 일을 가리키는 이름표(꺼진 등·닫힌 문·작은 냄비)는 사전에서 빼고, 실제 대사 문구로 사전을 다시 씀', '0 -> 1'),
    ('G', '같은 라벨의 배타 갈래, 서로 갈 수 없는 라벨, 한 번뿐인 값(회의 결과)이 어긋나는 짝은 뺌. r13_nw_retry 를 본문대로 읽어 재시도 갈래에 결과 덧줄이 붙지 않게 함', '8 -> 3'),
]

CHECK_TITLES = dict(D='죽었거나 떠난 뒤의 말', E='장면에 없는 화자', F='일어나지 않은 일', G='같은 말 두 번')


def print_text(res, days):
    found = res['findings']
    print('분기 대사 대조 — %s' % ('%s일' % ','.join(map(str, days)) if days else '1~14일'))
    print('대사 지점 %d곳, 줄 %d개, 도달 못 한 라벨 %d개(옛 저장용 등)' % (
        len(res['analyzer'].sites), len(res['rows']), len(res['unreached'])))
    for k, v in counts(found).items():
        print('  %s %s: %d건' % (k, CHECK_TITLES[k[0]], v))
    for check in 'DEFG':
        items = [f for f in found if f['check'] == check]
        if not items:
            continue
        print('\n## %s %s (%d)' % (check, CHECK_TITLES[check], len(items)))
        for f in sorted(items, key=lambda f: (f['grade'] != '확실', f['day'] or 0, f['id'])):
            print('  [%s] %s일 %s %s (조건 %s) — %s | 경로 %s | %s' % (
                f['grade'], f['day'], f['id'], f['speaker'], f['when'], f['conflict'], f['paths'], f['text'][:50]))
    if res['unknown_conds']:
        print('\n## 해석 못 한 조건(이 조건이 붙은 줄은 양쪽 다 가능한 것으로 봤다)')
        for w, n in res['unknown_conds'].most_common():
            print('  %s (%d줄): %s' % (w, n, res['game'].when_src.get(w, '?')[:90]))


def md_escape(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')


def write_md(res, days, path):
    g, an = res['game'], res['analyzer']
    found = res['findings']
    today = datetime.date.today().isoformat()
    out = ['# 분기 대사 대조 결과 (%s)' % today, '',
           '`python3 dev/branch_audit.py %s --write` 로 만든 표다. 설명·한계는 `docs/design/BRANCH_AUDIT.md`.' % (
               '--day ' + ','.join(map(str, days)) if days else '--all'),
           '결과는 후보 목록이다. 「확실」은 그 경로에서 반드시 어긋나는 것, 「의심」은 사람이 확인할 것.', '',
           '- 대사 지점 %d곳, 줄 %d개' % (len(an.sites), len(res['rows'])),
           '- 도달 못 한 라벨 %d개(옛 저장용으로 남긴 라벨 등, 그 안의 줄은 검사하지 않음)' % len(res['unreached']), '',
           '## 건수', '', '| 검사 | 등급 | 건수 |', '|---|---|---|']
    for k, v in counts(found).items():
        out.append('| %s %s | %s | %d |' % (k[0], CHECK_TITLES[k[0]], k.split()[1], v))
    for check in 'DEFG':
        items = [f for f in found if f['check'] == check]
        out += ['', '## %s %s (%d건)' % (check, CHECK_TITLES[check], len(items)), '']
        if not items:
            out.append('없음.')
            continue
        out += ['| 등급 | 날 | 줄 ID | 화자 | 조건 | 충돌한 상태 | 경로 | 위치 | 대사 |', '|---|---|---|---|---|---|---|---|---|']
        for f in sorted(items, key=lambda f: (f['grade'] != '확실', f['day'] or 0, f['id'])):
            out.append('| %s |' % ' | '.join(md_escape(x) for x in (
                f['grade'], f['day'], f['id'], f['speaker'], f['when'], f['conflict'], f['paths'], f['site'], f['text'])))
    out += ['', '## 거짓 양성 조정', '', '| 검사 | 바꾼 기준 | 건수 |', '|---|---|---|']
    out += ['| %s | %s | %s |' % (md_escape(a), md_escape(b), c) for a, b, c in ADJUSTMENTS]
    out += ['', '## 세계 상태 표 (날짜 x 갈림 결과)', '',
            '그 날 대사 지점들의 상태를 모았다. 「확정」은 그 결과의 모든 판에서, 「가능」은 일부 판에서. 경로 수는 '
            '그 결과를 지난 갈림 조합의 수.', '',
            '| 날 | 경로 | 경로 수 | 사망 확정 | 사망 가능 | 명단 확정 | 명단 가능 | 떠났을 수 있음 |', '|---|---|---|---|---|---|---|---|']
    for t in world_table(g, an, res['rows']):
        if days and t['day'] not in days:
            continue
        out.append('| %s |' % ' | '.join(md_escape(x) for x in (
            t['day'], t['paths'], t['n'], ', '.join(t['dead']) or '-', ', '.join(t['dead_may']) or '-', ', '.join(t['listed']) or '-',
            ', '.join(t['listed_may']) or '-', ', '.join(t['departed_may']) or '-')))
    out += ['', '### 사망이 설정되는 곳(코드에서 뽑음)', '']
    for k, where in death_points(g, an.story):
        out.append('- `%s` = False: `%s`' % (k, where))
    out += ['', '### 코드에서 못 뽑아 보충한 것', '']
    for what, how, src in g.notes:
        out.append('- %s: %s (출처 `%s`)' % (what, how, src))
    out += ['', '## 해석 못 한 조건', '', '이 조건이 붙은 줄은 참·거짓 양쪽 다 가능한 것으로 두고 검사했다(추정하지 않음).', '']
    for w, n in res['unknown_conds'].most_common():
        out.append('- `%s` (%d줄): `%s`' % (w, n, md_escape(g.when_src.get(w, '?'))[:120]))
    out += ['', '### 해석 못 한 대본 분기(if·menu 조건, 상위 30)', '']
    for c, n in res['unknown_guards'].most_common(30):
        out.append('- `%s` (%d번)' % (md_escape(c)[:120], n))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(out) + '\n', encoding='utf-8')
    return path


def main(argv=None):
    ap = argparse.ArgumentParser(description='분기 대사 대조 점검')
    ap.add_argument('--day', help='날(쉼표로 여러 날)')
    ap.add_argument('--all', action='store_true', help='1~14일 전부')
    ap.add_argument('--json', action='store_true', help='기계용 출력')
    ap.add_argument('--write', action='store_true', help='docs/reviews/branch-audit/YYYYMMDD.md 에 쓴다')
    a = ap.parse_args(argv)
    if not a.day and not a.all:
        ap.print_help()
        return 2
    days = [int(x) for x in a.day.split(',')] if a.day else None
    res = audit(days=days)
    if a.write:
        # 출력을 head 등으로 잘라 보더라도 보고서는 남게 먼저 쓴다.
        p = write_md(res, days, ROOT / 'docs/reviews/branch-audit' / (datetime.date.today().strftime('%Y%m%d') + '.md'))
        print('썼다: %s' % p.relative_to(ROOT), file=sys.stderr)
    if a.json:
        print(json.dumps(dict(counts=counts(res['findings']), findings=res['findings'],
                              unknown_conditions=dict(res['unknown_conds']),
                              unreached_labels=res['unreached']), ensure_ascii=False, indent=1))
    else:
        print_text(res, days)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)  # head 등으로 잘라 볼 때
