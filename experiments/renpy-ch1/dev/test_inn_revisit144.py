"""여관 재방문은 현재 수사 선택과 날짜를 바꾸지 않는다."""
import copy
import json
import unittest
from types import SimpleNamespace

from test_play_review_field import ROOT, load_function


class InnRevisit144(unittest.TestCase):
    def setUp(self):
        self.values=dict(ui_room_arrival_seen=True,gate_registered=True,OWL_ALIVE=True)
        self.state=SimpleNamespace(room13=dict(day=1,period=2,location='room13',case_state='pending',
                                              evidence=['V111:E06'],flags=[],v111=dict(gate='sleep1',values=self.values)))
        self.binding=json.loads((ROOT/'game/v111/field-bindings.json').read_text())['sleep1']
        self.env=dict(store=self.state,r13_v111_active=lambda:True,
                      r13_v111_value=lambda key:self.values.get(key),
                      r13_v111_owned=lambda key:'V111:'+key in self.state.room13['evidence'],
                      r13_has=lambda key:key in self.state.room13['flags'],
                      r13_v111_binding=lambda:self.binding,_r13_v111_places=lambda:['legacy'])
        for key in ('r13_v111_free7_ready','r13_v111_revisit_allowed','r13_v111_known_public_visits','r13_v111_public_revisit_places','r13_v111_inn_revisit_places'):
            load_function('game/room13_v111.rpy',key,self.env)
        load_function('game/room13_v111.rpy','r13_places',self.env)
        navigation=(ROOT/'game/room13_navigation.rpy').read_text()
        start=navigation.index('    R13_LOCAL_CONNECTIONS=')
        end=navigation.index('\n\n    def r13_local_connections',start)
        import ast,textwrap
        exec(compile(ast.parse(textwrap.dedent(navigation[start:end])),'여관 연결','exec'),self.env)
        for key in ('r13_local_connections','r13_local_destination'):
            load_function('game/room13_navigation.rpy',key,self.env)

    def test_sleep_keeps_a_real_route_to_reception_and_back(self):
        before=copy.deepcopy(self.state.room13)
        places=self.env['r13_places']
        self.assertEqual(places(),['room13','inn','hall'])
        self.assertEqual(self.env['r13_local_destination']('hall'),'hall')
        self.state.room13['location']='hall'
        self.assertEqual(self.env['r13_local_destination']('inn'),'inn')
        self.state.room13['location']='inn'
        self.assertEqual(self.env['r13_local_destination']('hall'),'hall')
        self.state.room13['location']='hall'
        self.assertEqual(self.env['r13_local_destination']('room13'),'room13')
        self.state.room13['location']='room13'
        self.assertEqual(self.state.room13,before)
        self.assertEqual(self.binding['options'][0]['object'],'bed')

    def test_reading_places_never_advances_day_or_changes_the_pending_choices(self):
        before=copy.deepcopy((self.state.room13,self.binding))
        for _ in range(3):
            self.env['r13_places']();self.env['r13_v111_inn_revisit_places']()
        self.assertEqual((self.state.room13,self.binding),before)

    def test_room_is_not_known_before_first_arrival(self):
        self.values['ui_room_arrival_seen']=False
        self.state.room13['evidence']=[]
        self.state.room13['location']='inn'
        self.binding=dict(location='inn',options=[])
        self.assertEqual(self.env['r13_places'](),['inn'])

    def test_saved_night_without_the_new_first_arrival_flag_uses_existing_evidence(self):
        self.values.pop('ui_room_arrival_seen')
        self.assertEqual(self.env['r13_v111_inn_revisit_places'](),['inn','hall','room13'])
        self.state.room13['evidence']=[];self.state.room13['day']=2
        self.assertEqual(self.env['r13_v111_inn_revisit_places'](),['inn','hall','room13'])

    def test_dining_reopens_after_actual_story_visit_and_other_rooms_stay_hidden(self):
        self.assertNotIn('dining',self.env['r13_places']())
        self.state.room13['day']=2
        self.assertNotIn('dining',self.env['r13_places']())
        self.state.room13['flags'].append('v111:entered:MS14_D02_S04')
        self.assertIn('dining',self.env['r13_places']())
        for key in ('kitchen','guestroom','passage','ancient','school','facility'):
            self.assertNotIn(key,self.env['r13_places']())

    def test_detention_and_incident_only_keep_authored_access(self):
        for field,value in (('DARAM_DETAINED',True),('OWL_ALIVE',False),('route7','murder')):
            with self.subTest(field=field):
                self.values[field]=value
                self.assertEqual(self.env['r13_places'](),['room13'])
                self.values.pop(field)
        self.state.room13['case_state']='occurred'
        self.assertEqual(self.env['r13_places'](),['room13'])
        self.binding=dict(options=[dict(location='hall',move='hall',index=41)])
        self.assertEqual(self.env['r13_places'](),['room13','hall'])
        self.assertEqual(self.binding['options'][0]['index'],41)

    def test_other_days_and_non_inn_waits_keep_their_existing_routes(self):
        self.state.room13['day']=8
        self.assertEqual(self.env['r13_places'](),['room13'])
        self.state.room13['day']=2;self.state.room13['location']='forest';self.state.room13['v111']['gate']='travel'
        self.binding=dict(options=[dict(location='post',move='post',index=17)])
        self.assertEqual(self.env['r13_places'](),['forest','post'])
        self.env['r13_v111_active']=lambda:False
        self.assertEqual(self.env['r13_places'](),['legacy'])


if __name__=='__main__':unittest.main()
