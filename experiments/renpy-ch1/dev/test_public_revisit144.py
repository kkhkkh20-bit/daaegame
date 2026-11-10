"""이미 방문한 일상 장소의 재탐색과 잠긴 사건 동선을 구별한다."""
import copy
import json
import unittest
from types import SimpleNamespace

from test_play_review_field import ROOT, load_function


class PublicRevisit144(unittest.TestCase):
    def setUp(self):
        self.state=SimpleNamespace(room13=dict(day=2,period=0,location='square',case_state='pending',
            evidence=['V111:E06'],flags=[],v111=dict(gate='chorong_documents2',scene='MS14_D02_S01',
            values=dict(OWL_ALIVE=True,location_daram='square'),visited_places=['gate','inn','room13','square'])))
        self.binding=dict(location='square',options=[dict(location='square',person='resident_lamplighter',index=0)])
        self.env=dict(store=self.state,winter_copy=SimpleNamespace(deepcopy=copy.deepcopy),
            r13_v111_active=lambda:True,r13_v111_value=lambda key:self.state.room13['v111']['values'].get(key),
            r13_v111_owned=lambda key:'V111:'+key in self.state.room13['evidence'],
            r13_has=lambda key:key in self.state.room13['flags'],r13_v111_binding=lambda:self.binding,
            _r13_v111_places=lambda:['legacy'],
            R13_VILLAGE147_PUBLIC_PLACES=("inn","hall","room13","dining","square","gate","post","workshop","clinic","school","store"))
        for key in ('r13_v111_free7_ready','r13_v111_revisit_allowed','r13_v111_known_public_visits','r13_v111_public_revisit_places','r13_v111_inn_revisit_places','r13_places'):
            load_function('game/room13_v111.rpy',key,self.env)
        load_function('game/room13_rules.rpy','r13_edit',self.env)

    def test_square_can_revisit_inn_and_return_to_the_original_question(self):
        before=copy.deepcopy(self.state.room13)
        self.assertEqual(set(self.env['r13_places']()),set(self.env['R13_VILLAGE147_PUBLIC_PLACES']))
        self.env['r13_edit'](location='inn')
        self.assertEqual(set(self.env['r13_places']()),set(self.env['R13_VILLAGE147_PUBLIC_PLACES']))
        self.env['r13_edit'](location='square')
        after=self.state.room13
        self.assertEqual(after['day'],before['day']);self.assertEqual(after['period'],before['period'])
        self.assertEqual(after['v111']['gate'],before['v111']['gate'])
        self.assertEqual(after['v111']['values'],before['v111']['values'])
        self.assertEqual(after['evidence'],before['evidence']);self.assertEqual(after['flags'],before['flags'])
        self.assertEqual(self.binding['options'][0]['index'],0)

    def test_only_actual_location_edits_record_new_visits(self):
        old=self.state.room13;before=copy.deepcopy(old)
        self.env['r13_edit'](period=1)
        self.assertEqual(self.state.room13['v111']['visited_places'],before['v111']['visited_places'])
        self.env['r13_edit'](location='post')
        self.assertEqual(old,before)
        self.assertIn('post',self.state.room13['v111']['visited_places'])
        self.assertNotIn('workshop',self.state.room13['v111']['visited_places'])
        self.env['r13_edit'](location='post')
        self.assertEqual(self.state.room13['v111']['visited_places'].count('post'),1)
        saved=json.loads(json.dumps(self.state.room13));self.state.room13=saved
        self.assertIn('post',self.env['r13_places']())

    def test_public_first_visits_open_but_private_and_future_places_remain_closed(self):
        self.state.room13['v111']['visited_places']+=['store','passage','ancient','facility','greenhouse','altar']
        for key in ('post','workshop','clinic','school','store'):
            self.assertIn(key,self.env['r13_places']())
        for key in ('passage','ancient','facility','greenhouse','altar'):
            self.assertNotIn(key,self.env['r13_places']())

    def test_old_saves_restore_only_certain_completed_visits(self):
        self.state.room13['v111'].pop('visited_places')
        self.state.room13['day']=5
        self.assertEqual(self.env['r13_v111_known_public_visits'](),['inn','square'])
        completed=['MS14_D02_S02_L0005','MS14_D03_S03_L0008','MS14_D03_S03_L0027','MS14_D06_S01_L0012']
        self.state.room13['flags']=['v111:applied:'+rid for rid in completed]
        self.assertEqual(self.env['r13_v111_known_public_visits'](),['inn','square','post','workshop','clinic','school'])
        # 장면에 들어갔다는 표지만으로는 도착 전 목적지를 방문한 것으로 보지 않는다.
        self.state.room13['flags']=['v111:entered:MS14_D03_S03']
        self.assertNotIn('clinic',self.env['r13_v111_known_public_visits']())

    def test_travel_meetings_emergencies_and_detention_keep_authored_places(self):
        self.state.room13['v111']['visited_places']+=['post','workshop','clinic','school']
        for gate in ('travel','wet_cloth6','clear_wood6','fire_evidence6','bori_witness7','detained_bed7','unregistered_future_gate'):
            with self.subTest(gate=gate):
                self.state.room13['v111']['gate']=gate
                self.assertEqual(self.env['r13_places'](),['square'])
        self.state.room13['v111']['gate']='lamp_attempt_field3'
        self.state.room13['v111']['scene']='MS14_D03_S05'
        self.assertEqual(self.env['r13_places'](),['square'])
        self.state.room13['v111']['scene']='MS14_D02_S01';self.state.r13_meeting_active=True
        self.assertEqual(self.env['r13_places'](),['square'])

    def test_separately_guarded_family_does_not_gain_detours(self):
        values=self.state.room13['v111']['values']
        for field,value in (('busy:mom','daram_guard'),('busy:nabi','daram_guard'),('location:daram','school'),('DARAM_DETAINED',True)):
            with self.subTest(field=field):
                values[field]=value
                self.assertEqual(self.env['r13_places'](),['square'])
                values.pop(field)

    def test_afternoon_forest_story_choice_is_unchanged_and_store_public_space_opens(self):
        self.state.room13['v111'].update(gate='afternoon2',scene='MS14_D02_S04')
        self.state.room13['v111']['visited_places'].append('store')
        self.binding=json.loads((ROOT/'game/v111/field-bindings.json').read_text())['afternoon2']
        original=copy.deepcopy(self.binding)
        self.assertIn('inn',self.env['r13_places']())
        self.assertIn('store',self.env['r13_places']())
        self.assertEqual(self.binding,original)
        forest=next(o for o in self.binding['options'] if o.get('move')=='forest')
        self.assertTrue(forest['move_by_story'])

    def test_new_run_and_legacy_campaign_do_not_inherit_visits(self):
        self.state.room13['v111']=dict(values={},gate='gate_request')
        self.state.room13['location']='gate';self.state.room13['evidence']=[]
        self.binding=dict(options=[dict(location='gate',object='ledger',index=0)])
        self.assertEqual(self.env['r13_places'](),['gate'])
        self.state.room13.pop('v111')
        self.env['r13_v111_active']=lambda:False
        self.env['r13_edit'](location='inn')
        self.assertNotIn('v111',self.state.room13)
        self.assertEqual(self.env['r13_places'](),['legacy'])


if __name__=='__main__':unittest.main()
