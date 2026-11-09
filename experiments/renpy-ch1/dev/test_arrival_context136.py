"""첫 만남의 지식과 첫 방의 실제 대기 상태를 대조한다."""
import ast
import copy
import json
import textwrap
import unittest
from types import SimpleNamespace

from test_newworld_text import Layer, ROOT, SPEAKERS
from test_play_review_field import load_function


class ArrivalContext136(unittest.TestCase):
    def greeting(self, person, day, location, registered):
        layer=Layer(); env=layer.load(); state=layer.state
        state.room13.update(day=day,location=location)
        state.room13['v111'].update(scene='MS14_D01_S04',gate='registered_menu')
        env['r13_v111_set']('gate_registered',registered)
        before=copy.deepcopy(state.room13)
        env.update(r13_ep_line_art=lambda packet:None,
                   r13_v111_idle_lines=lambda person:[('old',person)],
                   r13_met_people=lambda:[], R13_GREETINGS=json.loads((ROOT/'game/v111/newworld/greetings.json').read_text()),
                   R13_IDLE_KIDS=('bami','resident_kongi','resident_tosil','resident_somi','v111_siluk_child','v111_child'))
        load_function('game/room13_v111_idle.rpy','r13_v111_is_kid',env)
        source=(ROOT/'game/room13_v111_idle.rpy').read_text().split('init 346 python:\n',1)[1].split('\n# Evidence with',1)[0]
        exec(compile(ast.parse(textwrap.dedent(source)),'첫 만남','exec'),env)
        lines=env['r13_v111_idle_lines'](person)
        self.assertEqual(lines[0][0],'dad')
        self.assertIn('다돌',lines[0][1])
        self.assertNotIn('여관',lines[0][1])
        self.assertNotIn('13호',lines[0][1])
        self.assertNotIn('오늘',lines[0][1])
        self.assertEqual(state.room13['evidence'],before['evidence'])
        self.assertEqual(env['r13_v111_value']('gate_registered'),registered)
        self.assertEqual(state.room13['day'],day)
        self.assertEqual(state.room13['location'],location)
        return lines

    def test_first_adult_meeting_never_claims_unconfirmed_lodging(self):
        for day,location,registered in ((1,'gate',False),(1,'gate',True),(1,'room13',True),(2,'square',True)):
            with self.subTest(day=day,location=location,registered=registered):
                self.greeting('resident_siluk',day,location,registered)

    def test_first_child_meeting_does_not_claim_lodging_either(self):
        self.greeting('bami',1,'gate',False)

    def test_inactive_bed_names_the_available_action_without_resolving_the_puzzle(self):
        values={};state=SimpleNamespace(room13=dict(day=1,location='room13',v111=dict(gate='note_pick')))
        spec=dict(special='sleep',text='침대',flags=['old-campaign'])
        env=dict(store=state,ROOM13=dict(objects=dict(room13=dict(bed=spec))),
                 r13_v111_value=lambda key:values.get(key),r13_v111_object_key=lambda key:key)
        ambient=load_function('game/room13_v111.rpy','r13_v111_ambient_text',env)
        self.assertIn('메모',ambient('bed',spec))
        state.room13['v111']['gate']='letter_compare_review'
        before=copy.deepcopy(state.room13)
        self.assertNotIn('도토리',ambient('bed',spec))
        values['letter_tail_observed']=True
        self.assertIn('발견한 차이',ambient('bed',spec))
        self.assertEqual(state.room13,before)
        state.room13['v111']['gate']='sleep1'
        self.assertIsNone(ambient('bed',spec),'잠자기는 실제 선택지가 처리한다')


if __name__=='__main__':unittest.main()
