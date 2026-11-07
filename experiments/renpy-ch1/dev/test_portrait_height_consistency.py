"""질문 전신·일반 근접·몸반응·문맥별 머리 기준의 크기 경계를 검증한다."""
import ast
import copy
import json
from pathlib import Path
import textwrap
import types
import unittest

from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def functions(path,names):
    tree=ast.parse(textwrap.dedent((ROOT/path).read_text().split(' python:',1)[1]))
    return [n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]


class PortraitHeightConsistency(unittest.TestCase):
    def test_question_profile_is_only_an_exact_560_request(self):
        node=functions('game/systems/room13_dialogue_beats.rpy',{'r13_dialogue_fit_profile'})
        env={};exec(compile(ast.Module(body=node,type_ignores=[]),'프로필 크기','exec'),env)
        profiles={str(h):dict(canvas=[h,h],frames=dict(neutral=dict(file=str(h),offset=[10,20],scale=h/1000))) for h in (560,760,840)}
        profiles['560']['question_top']=118
        fit=env['r13_dialogue_fit_profile']
        self.assertIs(fit(profiles,560),profiles['560'])
        for h in (470,559.9,560.1,620,740,1302):
            result=fit(profiles,h);frame=result['frames']['neutral']
            self.assertNotEqual(frame['file'],'560')
            self.assertAlmostEqual(frame['scale'],h/1000)

    def test_body_reaction_uses_actual_source_canvas_instead_of_legacy_crop(self):
        text=(ROOT/'game/systems/room13_dot_fx.rpy').read_text()
        body=text.split('    def r13_body_size',1)[1].split('\n#',1)[0]
        env=dict(r13_dialogue_source_profile=lambda *a:dict(canvas=[493,984]),r13_say_actor_h=lambda:1302,
                 r13_fullbody_spec=lambda *a:self.fail('승인 근접이 있는데 옛 전신 크기를 사용함'))
        exec(textwrap.dedent('    def r13_body_size'+body),env)
        self.assertEqual(env['r13_body_size']('granny','joy'),(493,984))
        env.update(r13_dialogue_source_profile=lambda *a:None,r13_fullbody_spec=lambda *a:dict(crop=[0,0,400,800]),r13_fullbody_scale=lambda *a:1.5)
        self.assertEqual(env['r13_body_size']('granny','withdraw_hand'),(600,1200))

    def test_head_cache_separates_context_frames_with_the_same_person_pose_and_height(self):
        nodes=functions('game/systems/room13_say_actor.rpy',{'_r13_say_drawn_headtop'})
        state=types.SimpleNamespace(r13_dialogue_beat=dict(person='daram',context_key='one',talk='gesture'))
        def profile(path):return dict(canvas=[300,800],frames=dict(gesture=dict(file=path,offset=[10,20],scale=1)))
        data=dict(entries=dict(one=dict(profiles={'840':profile('one.png')}),two=dict(profiles={'840':profile('two.png')})))
        calls=[]
        def surface(*args):
            calls.append(state.r13_dialogue_beat['context_key'])
            return types.SimpleNamespace(get_bounding_rect=lambda **kw:types.SimpleNamespace(top=50 if calls[-1]=='one' else 150,height=700))
        env=dict(store=state,R13_DIALOGUE_CONTEXT_ART=data,_R13_SAY_DRAWN_TOP={},r13_dialogue_fit_profile=lambda profiles,h:profiles['840'],r13_dialogue_source_profile=lambda *a:None,
                 r13_close_art=lambda *a:None,renpy=types.SimpleNamespace(render_to_surface=surface))
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'머리 기준 캐시','exec'),env)
        get=env['_r13_say_drawn_headtop']
        self.assertEqual(get('daram','neutral',840),50)
        self.assertEqual(get('daram','neutral',840),50)
        state.r13_dialogue_beat=dict(person='daram',context_key='two',talk='gesture')
        self.assertEqual(get('daram','neutral',840),150)
        self.assertEqual(calls,['one','two'])

    def test_daram_stage_head_is_raised_without_changing_other_people(self):
        nodes=functions('game/systems/room13_say_actor.rpy',{'r13_say_head_target'})
        env=dict(r13_say_stature=lambda who:.82 if who=='daram' else 1,R13_SAY_HEAD_TOP=20,R13_SAY_HEAD_NUDGE={'daram':-32},r13_say_child_drop=lambda who:94 if who=='daram' else 0)
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'대사 머리 높이','exec'),env)
        self.assertEqual(env['r13_say_head_target']('daram'),82)
        self.assertEqual(env['r13_say_head_target']('granny'),20)

    def test_karo_and_bori_use_tall_adult_size_and_keep_question_geometry(self):
        people=json.loads((ROOT/'game/assets/room13-dialogue-player-facing.json').read_text())['people']
        for who in ('karo','resident_bori'):
            e=people[who]
            self.assertEqual(e['dialogue_visible_height_840'],690)
            for height in ('760','840'):
                for frame in e['profiles'][height]['frames'].values():
                    with Image.open(ROOT/'game'/frame['file']) as image:
                        b=image.getchannel('A').point(lambda a:255 if a>=40 else 0).getbbox()
                    self.assertAlmostEqual((b[3]-b[1])*frame['scale'],690*int(height)/840,delta=.00001)
            self.assertIn('question_top',e['profiles']['560'])
            self.assertNotIn('question_top',e['profiles']['840'])

    def test_future_gaze_import_preserves_two_adults_and_darams_lower_question_alignment(self):
        from import_dialogue_gaze116 import ART,normalize_question_layout
        targets=json.loads((ART/'runtime-fit-targets.json').read_text())
        self.assertFalse({'karo','resident_bori','daram'}&set(targets))
        people=json.loads((ROOT/'game/assets/room13-dialogue-player-facing.json').read_text())['people']
        selected={who:copy.deepcopy(people[who]) for who in ('karo','resident_bori','daram')}
        before=copy.deepcopy(selected)
        normalize_question_layout(selected)
        self.assertEqual(selected,before)


if __name__=='__main__':unittest.main()
