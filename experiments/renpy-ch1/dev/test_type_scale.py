"""2026-10-27 타이포그래피 시안(R13_TYPE_V2): 단계표 값과 「꺼짐 동등성」.

꺼진 동안 화면이 이전과 같아야 하므로, r13_type/r13_type_color 는 반드시
`... if R13_TYPE_V2 else <이전 값>` 꼴 안에서만 쓰이거나, 함수 머리의
`if R13_TYPE_V2:return ...` 한 줄 뒤에 이전 반환이 남아 있어야 한다."""
import re,unittest
from pathlib import Path
GAME=Path(__file__).resolve().parents[1]/'game'
SCALE=GAME/'systems'/'room13_type_scale.rpy'
# 시안이 손대는 파일. 다른 파일에서 r13_type 를 쓰면 범위를 벗어난 것이다.
TOUCHED=['screens.rpy','systems/room13_night_ui.rpy','systems/room13_notebook_choices.rpy',
         'room13_notebook.rpy','systems/room13_evidence_view.rpy',
         # 2026-10-27 2차: 현장·지도·설정·질문·단축키·더보기 판(더보기 판 화면은 footer_concept 에 있다).
         'room13_screens.rpy','room13_map_village_b.rpy','systems/room13_side_questions.rpy',
         'systems/room13_shortcuts.rpy','systems/room13_footer_concept.rpy',
         # 2026-10-27 회의 쪽: 머리띠·이름표·발언 듣는 중·발언 검토·공개 의견·결과 판·자료 대조 패널·쪽지.
         'room13_meeting_seating.rpy','room13_v111_meeting_stage.rpy','systems/room13_meeting_direction.rpy',
         'systems/room13_meeting_flow.rpy','systems/room13_debate.rpy','room13_meeting_retry_ui.rpy',
         'room13_week2_screens.rpy','systems/room13_choice_issues.rpy',
         # 2026-10-27 수첩 공통 틀: 틀·사람·메모·달력·소지품 탭과 서랍(기록 화면 안의 조각들).
         'systems/room13_notebook_shell.rpy','systems/room13_relations.rpy','systems/room13_learning.rpy',
         'room13_inspection.rpy','systems/room13_evidence_drawer.rpy',
         # 2026-10-27 UX 인계서 D01~D03·D06: 자료 대조 통합 화면(수첩 틀의 r13_nb_* 도우미를 쓴다).
         'systems/room13_proof_workspace.rpy']
# 옛 모드 파일(2026-10-27 제거 중)은 검사에서 뺀다.
LEGACY=('winter','source','arrival','council','village_','story.rpy','ms14','timeline','room13_week2','room13_ep','episodes','town_events','scene_runtime','room13_opening')
GUARDED=re.compile(r'r13_type(?:_color)?\("[a-z]+"\)\s+if R13_TYPE_V2 else ')
HEAD=re.compile(r'^\s+if R13_TYPE_V2:\s*return r13_type(?:_color)?\("[a-z]+"\)')

def load_scale(touch=False,large=False,small=False):
    """init python 블록을 Ren'Py 없이 실행한다. r13_read_size 는 room13_readability.rpy 와 같은 식."""
    src=SCALE.read_text(encoding='utf-8')
    body=src.split('init 59 python:',1)[1]
    code='\n'.join(line[4:] if line.startswith('    ') else line for line in body.splitlines())
    def r13_read_size(base,large_=None):
        if not large:
            return int(max(base-3,round(base*.9))) if small else int(base)
        return int(large_ if large_ is not None else max(base+4,round(base*1.25)))
    ns={'r13_touch_ui':lambda:touch,'r13_read_size':r13_read_size}
    exec(code,ns)
    return ns

class TypeScale(unittest.TestCase):
    def test_switch_is_on(self):
        # 2026-10-27 소유자 "적용". 끄면 이전 값으로 돌아가는 구조는 그대로다.
        self.assertIn('define R13_TYPE_V2 = True',SCALE.read_text(encoding='utf-8'))

    def test_levels_rise_in_every_setting(self):
        for touch in (False,True):
            for large,small in ((False,False),(True,False),(False,True)):
                ns=load_scale(touch,large,small)
                sizes=[ns['r13_type'](l) for l in ns['R13_TYPE_LEVELS']]
                self.assertEqual(sizes,sorted(sizes),(touch,large,small,sizes))
                self.assertEqual(len(set(sizes)),len(sizes),(touch,large,small,sizes))
                self.assertGreaterEqual(min(sizes),16)

    def test_scale_values(self):
        ns=load_scale()
        self.assertEqual([ns['r13_type'](l) for l in ns['R13_TYPE_LEVELS']],[20,22,24,26,28,30])
        ns=load_scale(large=True)
        self.assertEqual([ns['r13_type'](l) for l in ns['R13_TYPE_LEVELS']],[24,26,28,30,32,34])
        ns=load_scale(touch=True)
        self.assertEqual([ns['r13_type'](l) for l in ns['R13_TYPE_LEVELS']],[26,28,30,32,34,36])
        ns=load_scale(small=True)
        self.assertEqual(ns['r13_type']('body'),20)   # 2026-10-28 시안 2: 작게 설정은 보통보다 한 칸(2) 작다

    def test_colors_are_hex(self):
        ns=load_scale()
        for token in ('ink','muted','disabled','accent','inverse'):
            self.assertRegex(ns['r13_type_color'](token),r'^#[0-9a-f]{6}$')

    def test_six_levels_and_no_hardcoded_sizes(self):
        # 2026-10-27 소유자 "전체적으로 폰트 사이즈 6단계 이하로 통일해": 단계는 여섯, 화면의 글자 크기는 단계 이름으로만 쓴다.
        ns=load_scale()
        self.assertEqual(len(ns['R13_TYPE_LEVELS']),6)
        literal=[];switch=[]
        for f in sorted(GAME.rglob('*.rpy')):
            rel=f.relative_to(GAME).as_posix()
            # 결말·후일담 화면(ending_story, episode_aftermath)은 지금도 쓰이므로 옛 모드 목록과 무관하게 본다.
            if 'qa_tests' in f.parts or f==SCALE or (any(k in rel for k in LEGACY) and not any(k in rel for k in ('ending_story','episode_aftermath'))):continue
            for n,line in enumerate(f.read_text(encoding='utf-8').splitlines(),1):
                if line.lstrip().startswith('#'):continue
                if re.search(r'(?<![xy_])(?:text_)?size (?:\d{2}\b|\(?r13_read_size\()',line):literal.append('%s:%d'%(rel,n))
                # 2026-10-28: 식 안의 r13_read_size(숫자,숫자) 도 단계 밖이다(목표 띠·자료 서랍·결말 화면에 남아 있었다).
                elif re.search(r'r13_read_size\(\d',line) and 'room13_admin' not in rel:literal.append('%s:%d'%(rel,n))
                if 'if R13_TYPE_V2' in line:switch.append('%s:%d'%(rel,n))
        self.assertEqual(literal,[],'글자 크기는 r13_type("단계") 로만 적는다')
        self.assertEqual(switch,[],'R13_TYPE_V2 이중 경로는 2026-10-27 에 걷어냈다')

if __name__=='__main__':unittest.main()
