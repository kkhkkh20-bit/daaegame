"""현장 이름표가 대사가 되거나 부재 동행이 호출되지 않는지 검사한다."""
import copy
import unittest
from types import SimpleNamespace
from test_play_review_field import load_function,ROOT

class FieldClick146(unittest.TestCase):
    def test_legacy_special_only_has_an_explicit_plain_observation(self):
        for visible in (True,False):
            objects={'books':dict(special='book_latch',text='붉은 책 뒤의 장치'),
                     'old_reward':dict(give=['OLD_REWARD'],text='옛 사건 보상')}
            state=SimpleNamespace(room13=dict(day=2,location='room13',v111=dict(gate='sleep2')))
            env=dict(store=state,ROOM13=dict(objects=dict(room13=objects)),
                r13_v111_value=lambda key:False,r13_v111_object_key=lambda key:key,
                R13_V111_RECORD_OBJECTS={},R13_V111_RECORD_LATER={},
                _r13_v111_object_visible=lambda spec:visible,
                R13_FIELD_PLAIN_OBSERVATIONS146={('room13','books'):'크기가 다른 책들이 책장에 나란히 꽂혀 있다.'})
            fn=load_function('game/room13_v111.rpy','r13_v111_ambient_text',env)
            before=copy.deepcopy(state.room13)
            text=fn('books',objects['books'])
            self.assertEqual(text is None,not visible)
            if text:
                self.assertNotEqual(text,'책장');self.assertNotIn('장치',text);self.assertNotIn('붉은',text)
            self.assertIsNone(fn('old_reward',objects['old_reward']))
            self.assertEqual(state.room13,before)

    def test_hidden_companion_only_accepts_physical_same_place(self):
        values={};state=SimpleNamespace(room13=dict(day=2,location='square',daram_state='with_dad',v111=dict(scene='MS14_D02_S01')))
        env=dict(store=state,r13_v111_active=lambda:True,r13_visible_people=lambda:[],
                 r13_v111_value=lambda key:values.get(key))
        load_function('game/room13_v111.rpy','r13_v111_roam_companions',env)
        here=load_function('game/systems/room13_field_click146.rpy','r13_v111_dialogue_here146',env)
        self.assertTrue(here('daram'));self.assertFalse(here('mom'))
        for patch in ({'DARAM_DETAINED':True},{'location:daram':'school'},
                      {'busy:mom':'daram_guard'},{'DARAM_location':'school','busy:nabi':'daram_guard'}):
            values.clear();values.update(patch)
            before=copy.deepcopy(state.room13)
            self.assertFalse(here('daram'),patch);self.assertEqual(state.room13,before)

    def test_optional_object_banter_requires_present_child_and_calm_moment(self):
        values={};owned=set();tense=[None]
        state=SimpleNamespace(room13=dict(day=3,location='workshop',daram_state='with_dad',v111=dict(scene='MS14_D03_S03')))
        env=dict(store=state,r13_v111_active=lambda:True,r13_v111_value=lambda key:values.get(key),
                 r13_v111_owned=lambda key:key in owned,r13_v111_tense_context=lambda:tense[0],
                 _r13_field146_observation_chat_allowed=lambda identity:True)
        load_function('game/room13_v111.rpy','r13_v111_roam_companions',env)
        allowed=load_function('game/systems/room13_field_click146.rpy','r13_observation_chat_allowed',env)
        self.assertTrue(allowed('object:workshop:bolts'))
        values.update({'DARAM_location':'school','busy:nabi':'daram_guard'})
        self.assertFalse(allowed('object:workshop:bolts'))
        values.clear();values['piko_alive']=False;owned.add('E09')
        self.assertFalse(allowed('object:workshop:bolts'))
        state.room13['day']=4
        self.assertTrue(allowed('object:workshop:bolts'))
        state.room13['day']=6;values['FIRE_EVACUATED']=True
        self.assertTrue(allowed('object:workshop:bolts'),'사전 대피만으로 화재 사후를 만들지 않는다')
        values['D06_S03P_empty_fire_completed']=True
        self.assertFalse(allowed('object:workshop:bolts'))
        state.room13['day']=7;tense[0]='event'
        self.assertFalse(allowed('object:workshop:bolts'))

if __name__=='__main__':unittest.main()
