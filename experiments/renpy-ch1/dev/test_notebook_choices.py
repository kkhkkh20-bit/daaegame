"""Paper menus retain action identity, touch targets and the suspended stage."""
from type_stub import r13_type_stub
import ast
from pathlib import Path
import re
import textwrap
from types import SimpleNamespace
import unittest

ROOT=Path(__file__).resolve().parents[1]

def function(path,name,ns):
    source=(ROOT/'game'/path).read_text()
    for block in re.split(r'^init(?: -?\d+)? python:\n',source,flags=re.M)[1:]:
        block=re.split(r'^(?=\S)',block,flags=re.M)[0]
        for node in ast.parse(textwrap.dedent(block)).body:
            if isinstance(node,ast.FunctionDef) and node.name==name:
                exec(compile(ast.Module(body=[node],type_ignores=[]),path,'exec'),ns)
                return ns[name]
    raise AssertionError(name)

class NotebookChoices(unittest.TestCase):
    def test_paged_choices_keep_every_original_action_and_fit_with_the_header(self):
        for touch in (False,True):
            ns=dict(r13_question_caption=lambda title,*args,**kw:title,
                    r13_ui_font=lambda:'font',R13_UI_BOLD_FONT='bold-font',r13_read_size=lambda a,b:b if touch else a,
                    r13_touch_ui=lambda:touch,r13_type=r13_type_stub(touch=touch),
                    Text=lambda text,**kw:text,
                    renpy=SimpleNamespace(render=lambda text,*args:SimpleNamespace(get_size=lambda:(600,72 if len(text)>20 else 30))))
            function('systems/room13_notebook_choices.rpy','r13_notebook_choice_pages',ns)
            function('systems/room13_notebook_choices.rpy','r13_notebook_choice_fits',ns)
            geometry=function('systems/room13_notebook_choices.rpy','r13_notebook_choice_geometry',ns)
            entries=[('이미 들은 말을 다시 확인하는 긴 선택지 '+str(i),object(),i%2==0) for i in range(17)]
            header,pages,_=geometry(entries,650,'방금 들은 이야기에 대해 어떻게 대답할까?')
            self.assertGreater(len(pages),1)
            self.assertEqual([entry for page in pages for entry,height in page],entries)
            self.assertEqual(len({height for page in pages for entry,height in page}),1)
            for page in pages:
                content=sum(height for entry,height in page)+16*(len(page)-1)
                self.assertLessEqual(header+24+content+((100 if touch else 66) if len(pages)>1 else 0),600)
                if touch:self.assertTrue(all(height>=88 for entry,height in page))

    def test_four_choices_that_overflow_a_narrow_panel_split_two_and_two(self):
        # 2026-10-28 다른 길 12일(학교, 나비 옆 560 판): 셋째가 두 줄이라 넷째 칸이 화면 아래(y 716)로 나갔다.
        ns=dict(r13_question_caption=lambda title,*args,**kw:title,
                r13_ui_font=lambda:'font',R13_UI_BOLD_FONT='bold-font',r13_read_size=lambda a,b:a,
                r13_touch_ui=lambda:False,r13_type=r13_type_stub(touch=False),
                Text=lambda text,**kw:text,
                renpy=SimpleNamespace(render=lambda text,*args:SimpleNamespace(get_size=lambda:(500,88 if len(text)>14 else 44))))
        function('systems/room13_notebook_choices.rpy','r13_notebook_choice_pages',ns)
        function('systems/room13_notebook_choices.rpy','r13_notebook_choice_fits',ns)
        geometry=function('systems/room13_notebook_choices.rpy','r13_notebook_choice_geometry',ns)
        entries=[('배식 전에 더 살핀다',object(),False),('다람과 장작을 받으러 간다',object(),False),
                 ('다람은 나비 곁에 두고 다녀온다',object(),False),('아침에 부탁한 일들을 확인한다',object(),False)]
        header,pages,_=geometry(entries,560,'배식 전에 더 살필까, 장작을 받으러 갈까')
        self.assertEqual([len(page) for page in pages],[2,2])
        self.assertEqual([entry for page in pages for entry,height in page],entries)
        for page in pages:
            content=sum(height for entry,height in page)+16*(len(page)-1)
            self.assertLessEqual(header+28+content+66,600)
            self.assertTrue(all(height>=88+20 for entry,height in page))
        # 셋이면 나누지 않는다(하나짜리 쪽 금지).
        header,pages,_=geometry(entries[:3],560,'배식 전에 더 살필까, 장작을 받으러 갈까')
        self.assertEqual(len(pages),1)

    def test_stage_displayable_is_restored_without_rebuilding_its_pose(self):
        actor=object();current={'actor':actor};events=[]
        state=SimpleNamespace(place='여관',r13_meeting_active=False,r13_choice_hidden_actor=None)
        def hide(tag):events.append(('hide',tag));current['actor']=None
        def show(tag,what):events.append(('show',tag));current['actor']=what
        scene_lists=SimpleNamespace(get_displayable_by_tag=lambda layer,tag:current['actor'])
        ns=dict(store=state,renpy=SimpleNamespace(game=SimpleNamespace(context=lambda:SimpleNamespace(scene_lists=scene_lists)),hide=hide,show=show))
        layout=function('room13_interaction.rpy','r13_choice_layout',ns)
        layout('granny','joy',True)
        self.assertIs(state.r13_choice_hidden_actor,actor)
        self.assertIsNone(current['actor'])
        layout('granny','joy',True)
        layout('granny','joy',False)
        self.assertIs(current['actor'],actor)
        self.assertIsNone(state.r13_choice_hidden_actor)
        self.assertEqual(events,[('hide','r13_visitor'),('show','r13_visitor')])

    def test_carriage_and_meeting_stages_keep_their_authored_positions(self):
        for place,meeting in (('마차 안',False),('광장',True)):
            ns=dict(store=SimpleNamespace(place=place,r13_meeting_active=meeting),renpy=SimpleNamespace())
            layout=function('room13_interaction.rpy','r13_choice_layout',ns)
            layout('daram','neutral',True)
            layout('daram','neutral',False)

if __name__=='__main__':unittest.main()
