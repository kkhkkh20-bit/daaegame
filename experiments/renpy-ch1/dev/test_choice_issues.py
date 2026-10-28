"""2026-10-27 외부 리뷰: 쟁점 제목 표가 실제 메뉴와 맞고, 처음 한 번 안내가 실제 기능만 말한다."""
from type_stub import r13_type_stub
import re
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT/'game'
SOURCE=(GAME/'systems/room13_choice_issues.rpy').read_text()

def story_menus():
    """새 세계 이야기 파일의 menu 문: {label: [선택지 목록, ...]}."""
    menus={}
    for path in sorted(GAME.glob('room13_v111*.rpy')):
        lines=path.read_text().split('\n');label=None
        for i,line in enumerate(lines):
            m=re.match(r'^label (\w+)',line)
            if m:label=m.group(1);menus.setdefault(label,[])
            m=re.match(r'^(\s*)menu\s*:',line)
            if not m:continue
            indent=len(m.group(1));options=[]
            for row in lines[i+1:]:
                if not row.strip():continue
                depth=len(row)-len(row.lstrip())
                if depth<=indent:break
                o=re.match(r"""^\s*(['"])(.+?)\1(?:\s+if\s+.*)?:\s*$""",row)
                if o and depth==indent+4:options.append(o.group(2))
            menus[label].append(tuple(options))
    return menus

def meeting_labels():
    text=(GAME/'room13_v111_meeting_stage.rpy').read_text()
    return {'r13_v111_'+name for block in re.findall(r"labels=\[([^\]]*)\]",text) for name in re.findall(r"'(\w+)'",block)}

def load(persistent=None,mornings=()):
    shown=[]
    ns=dict(store=SimpleNamespace(r13_meeting_active=False),
            persistent=persistent or SimpleNamespace(r13_proof_guide_done=False,r13_recovery_hint_retry=False,r13_recovery_hint_morning=False),
            renpy=SimpleNamespace(show_screen=lambda *a:shown.append(a)),
            # 2026-10-27 타이포 V2: 단계 표시 색이 스위치를 따른다. 끈 상태의 이전 색을 아래 시험이 확인한다.
            r13_type_color=lambda token:{"accent":"#a63a2e","muted":"#6b5641"}[token],
            r13_morning_days=lambda:list(mornings))
    block=SOURCE.split('init 80 python:\n')[1]
    block=re.split(r'^(?=\S)',block,flags=re.M)[0]
    exec(textwrap.dedent(block),ns)
    return ns,shown

class ChoiceIssueTable(unittest.TestCase):
    def setUp(self):
        self.ns,_=load()
        self.table=self.ns['R13_CHOICE_ISSUES']
        self.menus=story_menus()

    def test_every_issue_matches_one_real_menu(self):
        self.assertGreaterEqual(len(self.table),10)
        self.assertLessEqual(len(self.table),20)
        for menu_id,(issue,options) in self.table.items():
            self.assertIn(menu_id,self.menus,menu_id)
            self.assertIn(tuple(options),self.menus[menu_id],menu_id)

    def test_meeting_menus_are_left_alone(self):
        self.assertFalse(set(self.table)&meeting_labels())

    def test_issue_is_short_and_reveals_nothing(self):
        for menu_id,(issue,options) in self.table.items():
            self.assertLessEqual(len(issue),30,menu_id)
            self.assertNotIn('?',issue)
            for word in ('죽','살리','살아','정답','범인','실패','성공','위험','안전','결과','!'):
                self.assertNotIn(word,issue,menu_id)

    def test_issue_only_when_visible_options_belong_to_the_menu(self):
        f=self.ns['r13_choice_issue_for']
        self.assertEqual(f('r13_v111_offer13',['조건을 더 묻는다']),'가족 셋이 물러날까, 현장에 남을까')
        self.assertEqual(f('r13_v111_offer13',['조건을 더 묻는다','가족 셋이 수락하고 물러난다','거절하고 현장에 남는다']),'가족 셋이 물러날까, 현장에 남을까')
        # 같은 label 의 한 줄짜리 확인 메뉴, 표에 없는 메뉴, 이름 없는 자리에는 붙지 않는다.
        self.assertIsNone(f('r13_v111_heat_seen11',['벽 아래 깨진 돌판을 들여다본다']))
        self.assertIsNone(f('r13_v111_room_compare',['방을 더 둘러본다']))
        self.assertIsNone(f(None,['조건을 더 묻는다']))
        self.assertIsNone(f('r13_v111_offer13',[]))

    def test_meeting_never_takes_an_issue(self):
        self.ns['store'].r13_meeting_active=True
        self.assertIsNone(self.ns['r13_choice_issue']([('조건을 더 묻는다',None,False)]))

    def test_previous_line_stays_small_and_one_line(self):
        f=self.ns['r13_choice_issue_subline']
        self.assertEqual(f('',('까로','그러네.')),'까로 · 그러네.')
        self.assertEqual(f('',('','마차가 멈췄다.')),'마차가 멈췄다.')
        self.assertIsNone(f('',None))
        self.assertEqual(f('메뉴 제목',('까로','그러네.')),'메뉴 제목')
        long=f('',('돌목','가'*80),20)
        self.assertEqual(len(long),20)
        self.assertTrue(long.endswith('…'))

class NotebookHeaderWithIssue(unittest.TestCase):
    def test_issue_header_grows_and_keeps_every_choice(self):
        import sys;sys.path.insert(0,str(Path(__file__).resolve().parent))
        from test_notebook_choices import function
        for touch in (False,True):
            ns=dict(r13_question_caption=lambda title,*args,**kw:title,R13_UI_BOLD_FONT='bold',r13_type=r13_type_stub(touch=touch),
                    r13_read_size=lambda a,b:b if touch else a,r13_touch_ui=lambda:touch,R13_CHOICE_TEXT_PAD=116,R13_CHOICE_BODY="emphasis",Text=lambda text,**kw:text,
                    renpy=SimpleNamespace(render=lambda text,*args:SimpleNamespace(get_size=lambda:(600,72 if len(text)>20 else 30))))
            function('systems/room13_notebook_choices.rpy','r13_notebook_choice_pages',ns)
            function('systems/room13_notebook_choices.rpy','r13_notebook_choice_fits',ns)
            geometry=function('systems/room13_notebook_choices.rpy','r13_notebook_choice_geometry',ns)
            entries=[('가족 셋이 수락하고 물러난다',object(),False),('거절하고 현장에 남는다',object(),False),('조건을 더 묻는다',object(),False)]
            issue='가족 셋이 물러날까, 현장에 남을까 하는 자리'
            plain,_,_=geometry(entries,560,issue)
            header,pages,sub=geometry(entries,560,issue,'까로 · 그러네. 조건이 하나 더 있소')
            # 작은 줄이 남았으면 머리 칸이 자라고, 쪽이 갈려서 작은 줄을 뺐으면 머리 칸은 쟁점만의 높이다.
            if sub:self.assertGreater(header,plain)
            else:self.assertEqual(header,plain)
            self.assertEqual([e for page in pages for e,h in page],entries)
            for page in pages:
                content=sum(h for e,h in page)+16*(len(page)-1)
                # 쪽이 하나면 쪽 넘김 줄이 없다. 2026-10-27: 넷 이하는 늘 한 쪽에 둔다.
                self.assertLessEqual(header+24+content+((100 if touch else 66) if len(pages)>1 else 0),540)

class FirstTimeGuides(unittest.TestCase):
    def test_proof_steps_follow_the_chosen_count_and_stop_after_first_success(self):
        ns,_=load()
        self.assertTrue(ns['r13_proof_guide_active']())
        steps0=ns['r13_proof_guide_steps'](0);steps2=ns['r13_proof_guide_steps'](2)
        for name in ('1 자료 고르기','2 확인','3 선택한 근거 제출'):
            self.assertIn(name,re.sub(r'\{/?color[^}]*\}','',steps0))
        self.assertIn('{color=#a63a2e}1 자료 고르기',steps0)
        self.assertIn('{color=#a63a2e}2 확인',steps2)
        # 스위치를 켜면 지금 단계는 accent, 나머지는 muted 로 바뀐다.
        self.assertIn('{color=#a63a2e}1 자료 고르기',ns['r13_proof_guide_steps'](0))
        self.assertIn('{color=#6b5641}2 확인',ns['r13_proof_guide_steps'](0))
        self.assertIn('자료 고르기',ns['r13_proof_guide_help'](0,'남은 기회 3 / 3'))
        self.assertIn('기회를 쓰지 않습니다',ns['r13_proof_guide_help'](0))
        self.assertIn('기회를 1회',ns['r13_proof_guide_help'](1,'남은 기회 3 / 3'))
        self.assertNotIn('기회',ns['r13_proof_guide_help'](1))
        ns['r13_proof_guide_finish']()
        self.assertFalse(ns['r13_proof_guide_active']())

    def test_retry_note_names_only_features_that_exist(self):
        # 2026-10-27: 저장·불러오기는 「설정」의 「저장」 탭, 「다시 시작할 아침」은 메뉴에서 뺐다. 안내도 그것만 말한다.
        ns,_=load(mornings=())
        note=ns['r13_recovery_retry_note']()
        self.assertIn('「설정」의 「저장」 탭',note);self.assertNotIn('다시 시작할 아침',note);self.assertNotIn('더보기',note)
        ns,_=load(mornings=(1,2))
        self.assertNotIn('다시 시작할 아침',ns['r13_recovery_retry_note']())
        ns['r13_recovery_retry_seen']()
        self.assertIsNone(ns['r13_recovery_retry_note']())
        # 이름이 실제 화면과 같다: 설정 탭 「저장」, 밤 조작 줄의 「더보기」. 메뉴에서 뺀 이름은 남아 있으면 안 된다.
        screens=(GAME/'screens.rpy').read_text()
        self.assertIn('("save","불러오기" if main_menu else "저장")',screens)
        self.assertIn('"더보기"',(GAME/'systems/room13_night_ui.rpy').read_text())
        tools=(GAME/'systems/room13_playback.rpy').read_text()+(GAME/'systems/room13_footer_concept.rpy').read_text()
        for gone in ('"다시 시작할 아침"','"저장 · 불러오기"','"메인화면"'):
            self.assertNotIn(gone,tools)
        self.assertIn('"회의를 처음부터 다시"',(GAME/'room13_meeting_retry_ui.rpy').read_text())

    def test_morning_note_once_and_only_for_a_saved_later_morning(self):
        ns,shown=load(mornings=(1,2))
        ns['r13_morning_days']=lambda:[1]
        ns['r13_recovery_morning_note'](1)
        self.assertEqual(shown,[])
        ns['r13_morning_days']=lambda:[1]
        ns['r13_recovery_morning_note'](2)  # 아침 저장이 실패한 날은 말하지 않는다
        self.assertEqual(shown,[])
        ns['r13_morning_days']=lambda:[1,2]
        ns['r13_recovery_morning_note'](2)
        ns['r13_recovery_morning_note'](3)
        self.assertEqual(len(shown),1)
        self.assertEqual(shown[0][0],'r13_recovery_note')
        self.assertIn('2일 아침',shown[0][1])

    def test_hooks_are_wired(self):
        self.assertIn('r13_proof_guide_finish()',(GAME/'room13_v111.rpy').read_text())
        self.assertIn('r13_recovery_retry_seen()',(GAME/'room13_meeting_retry_logic.rpy').read_text())
        self.assertIn('r13_recovery_morning_note(day)',(GAME/'systems/room13_polish3.rpy').read_text())
        screens=(GAME/'room13_week2_screens.rpy').read_text()
        # 2026-10-27 패널 정리: 단계는 글줄(r13_proof_guide_steps)이 아니라 칩 셋(r13_proof_guide_chips)으로 그린다.
        # 글줄 함수는 남아 있고 위 시험이 그 색·순서를 본다. 여기서는 화면이 칩과 안내를 실제로 쓰는지만 본다.
        self.assertIn('r13_proof_guide_chips(',screens)
        self.assertIn('id "r13_proof_steps"',screens)
        self.assertIn('r13_proof_guide_help(',screens)

if __name__=='__main__':unittest.main()
