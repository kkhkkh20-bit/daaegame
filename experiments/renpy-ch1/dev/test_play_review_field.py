"""First-play review: touch geometry, repeatable reading and field hit targets."""
from type_stub import r13_type_stub
import ast
import copy
import re
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]


def load_function(path, name, namespace):
    source = (ROOT / path).read_text()
    for block in re.split(r'^init(?: -?\d+)? python:\n', source, flags=re.M)[1:]:
        block = re.split(r'^(?=\S)', block, flags=re.M)[0]
        for node in ast.parse(textwrap.dedent(block)).body:
            if isinstance(node, ast.FunctionDef) and node.name == name:
                exec(compile(ast.Module(body=[node], type_ignores=[]), path, 'exec'), namespace)
                return namespace[name]
    raise AssertionError(name)


class PlayReviewField(unittest.TestCase):
    def test_crowded_zoomed_gate_keeps_karo_label_near_its_head(self):
        # Captured actual 0.75 gate geometry: a 676 world-y clamp wrongly sent
        # Karo's label two rows above everyone instead of beside his own head.
        screen_faces=dict(resident_siluk=[377.25,406.5,47.25,33.75],guard=[493.5,430.5,56.25,45.75],
                          karo=[416.25,497.25,51.75,28.5],resident_bori=[903.75,474,64.5,52.5],daram=[186.75,524.25,75,15.75])
        faces={k:[853+x/.75,y/.75,w/.75,h/.75] for k,(x,y,w,h) in screen_faces.items()}
        names=dict(resident_siluk='실룩',guard='돌목',karo='까로',resident_bori='보리',daram='다람')
        ns=dict(r13_touch_ui=lambda:True,r13_actor_face_target=lambda a:faces[a['person']],
                r13_actor_nameplate=lambda a:(faces[a['person']][0]+faces[a['person']][2]/2,faces[a['person']][1]-36),
                r13_world_width=lambda:2560,r13_world_offset=lambda:853,r13_view_width=lambda:1707,
                r13_field_zoom=lambda:.75,R13_NAMES=names,R13_CONTROL=dict(width=232),
                r13_control_height=lambda:88,store=SimpleNamespace(R13_LIFE_GROUPS=[]),
                r13_field_ui_rects=lambda offset:[(772,616,480,88),(1020,512,232,88),(940,20,314,68),(24,20,400,54),(8,236,80,80),(1192,236,80,80)])
        labels=load_function('game/room13_interaction.rpy','r13_actor_nameplates',ns)([dict(person=k,rect=v) for k,v in faces.items()])
        label=next(row['rect'] for row in labels if row['person']=='karo')
        face=faces['karo']
        distance=((label[0]+label[2]/2-face[0]-face[2]/2)**2+(label[1]+label[3]/2-face[1]-face[3]/2)**2)**.5*.75
        self.assertLess(distance,120)

    def test_night_dialogue_and_touch_actions_have_separate_vertical_space(self):
        night=(ROOT/'game/systems/room13_night_ui.rpy').read_text()
        screens=(ROOT/'game/screens.rpy').read_text()
        spacing=int(re.search(r'size r13_night_say_size\(\) line_spacing (\d+)',screens).group(1))
        link=night.split('screen r13_night_link(',1)[1].split('\nscreen ',1)[0]
        target_height=re.search(r'xsize label_width ysize (\([^\n]+?\)) yalign',link).group(1)
        ribbon_height=re.search(r'xysize=\(label_width,(\d+ if r13_touch_ui\(\) else \d+)\)',link).group(1)
        # 2026-10-28 소유자 「건너뛰기·더보기는 대화창 안에 들어갈 필요 없다」: 조작 스티커는 이름 리본처럼 종이 윗변에 걸친다.
        # 누르는 칸 아래끝은 대사 첫 줄보다 위, 대사 끝줄은 종이 아래 테두리 선 위, 두 줄까지 종이 윗변은 화면 안 넉넉히.
        paper_bottom=int(re.search(r'R13_NIGHT_PAPER_BOTTOM=(\d+)',night).group(1))
        paper_edge=int(re.search(r'R13_NIGHT_PAPER_EDGE=(\d+)',night).group(1))
        self.assertIn('xysize=(1220,%d-r13_night_panel_top(what))'%paper_bottom,screens)
        for touch in (False,True):
            for large in (False,True):
                for lines in (1,2,3,4):
                    with self.subTest(touch=touch,large=large,lines=lines):
                        store=SimpleNamespace()
                        ns=dict(r13_touch_ui=lambda:touch,r13_read_size=lambda normal,big:big if large else normal,
                                r13_night_say_lines=lambda what:lines,r13_type=r13_type_stub(touch=touch,large=large),store=store,
                                R13_NIGHT_PAPER_BOTTOM=paper_bottom,R13_NIGHT_PAPER_EDGE=paper_edge,
                                R13_SAY_RIBBON_IN=int(re.search(r'R13_SAY_RIBBON_IN=(\d+)',night).group(1)),
                                R13_SAY_MARGIN=int(re.search(r'R13_SAY_MARGIN=(\d+)',night).group(1)))
                        size=load_function('game/systems/room13_night_ui.rpy','r13_night_say_size',ns)()
                        panel=load_function('game/systems/room13_night_ui.rpy','r13_night_panel_top',ns)
                        top=load_function('game/systems/room13_night_ui.rpy','r13_night_say_top',ns)('긴 대사')
                        center=load_function('game/systems/room13_night_ui.rpy','r13_night_control_y',ns)()
                        height=eval(target_height,ns)
                        self.assertEqual(center,panel('긴 대사'))              # 스티커 가운데 = 종이 윗변
                        self.assertGreaterEqual(top-(center+height/2),2 if touch else 8)   # 누르는 칸은 첫 줄보다 위
                        text_bottom=top+lines*size+(lines-1)*spacing
                        self.assertLessEqual(text_bottom,paper_bottom-paper_edge)      # 끝줄은 테두리 선 위
                        if lines<=2:self.assertGreaterEqual(center,440)
                        if touch:self.assertGreaterEqual(height*360/720,44)

    def test_shared_touch_footer_keeps_bottom_and_desktop_sizes(self):
        for touch,large,expected in ((False,False,64),(False,True,80),(True,False,88),(True,True,88)):
            ns=dict(r13_touch_ui=lambda:touch,persistent=SimpleNamespace(room13_large_text=large),
                    R13_CONTROL=dict(height=64,large_height=80,bottom=16,gap=16))
            height=load_function('game/room13_typography.rpy','r13_control_height',ns)
            y=load_function('game/room13_typography.rpy','r13_control_y',ns)
            self.assertEqual(height(),expected)
            self.assertEqual(y()+height(),704)
            if touch:self.assertGreaterEqual(height()*360/720,44)

    def test_long_question_pages_keep_every_row_above_the_pager(self):
        for touch in (False, True):
            for large in (False, True):
                # 2026-10-27 타이포 시안: 줄 수 측정이 단계표를 참조한다. 꺼진 값으로 재야 기대값이 같다.
                ns = dict(R13_SIDE_QUESTION_TOP=150, r13_type=lambda level: 26,
                          r13_question_caption=lambda title, *a, **kw: title,
                          r13_ui_font=lambda: 'font', R13_UI_BOLD_FONT='bold-font', r13_read_size=lambda a,b: b if large else a,
                          r13_touch_ui=lambda: touch,
                          Text=lambda text, **kw: text,
                          renpy=SimpleNamespace(render=lambda text,*a: SimpleNamespace(get_size=lambda: (506, 60 if len(text)>20 else 28))))
                upper=load_function('game/systems/room13_side_questions.rpy','r13_notebook_topic_y',ns)()
                pages = load_function('game/systems/room13_side_questions.rpy', 'r13_side_question_pages', ns)
                entries = [('반복 확인하는 긴 질문입니다. '+str(i), i, False) for i in range(30)]
                result = pages(entries)
                self.assertEqual([entry for page in result for entry,height in page], entries)
                for page in result:
                    height=sum(h for _,h in page)+8*(len(page)-1)
                    self.assertLessEqual(228+height,upper-(96 if touch else 60)-12)
                    if touch:
                        self.assertTrue(all(h*360/720>=44 for _,h in page))

    def test_memo_touch_area_keeps_art_center_and_other_objects_unchanged(self):
        for zoom in (1.0, .75):
            ns=dict(r13_touch_ui=lambda: True,r13_field_zoom=lambda:zoom)
            target=load_function('game/systems/room13_mother_note_spot.rpy','r13_object_target_rect',ns)
            spec=dict(rect=[138,378,104,36],give=[])
            before=copy.deepcopy(spec)
            x,y,w,h=target('mother_note',spec)
            self.assertEqual((x+w/2,y+h/2),(190,396))
            self.assertGreaterEqual(min(w,h)*zoom*360/720,44)
            self.assertEqual(target('desk',spec),tuple(spec['rect']))
            self.assertEqual(spec,before)

    def test_read_mark_does_not_mark_submission_or_hidden_questions(self):
        state=SimpleNamespace(room13=dict(location='gate',evidence=[],v111=dict(gate='gate_investigate')))
        options=[dict(title='비교',person='guard',location='gate',index=3,remember_read=True),
                 dict(title='제출',person='guard',location='gate',index=5),
                 dict(title='다른 곳',person='guard',location='inn',index=6,remember_read=True)]
        ns=dict(store=state,r13_v111_binding=lambda:dict(options=options),Return=lambda x:x,
                r13_v111_value=lambda key:True)
        questions=load_function('game/room13_v111.rpy','r13_v111_questions',ns)
        self.assertEqual(questions('guard'),[('비교',3,True),('제출',5,False)])
        self.assertEqual(questions('daram'),[])

    def test_phone_settings_buttons_match_vertical_alignment(self):
        for touch in (False,True):
            ns=dict(r13_touch_ui=lambda:touch)
            height=load_function('game/screens.rpy','r13_opt_button_height',ns)()
            self.assertLessEqual(height,92)
            if touch:self.assertGreaterEqual(height*360/720,44)
        source=(ROOT/'game/screens.rpy').read_text()
        self.assertIn('ysize r13_opt_button_height()',source)
        self.assertNotIn('ysize r13_opt_button_height()\n                    xsize 230 ysize',source)


if __name__ == '__main__':
    unittest.main()
