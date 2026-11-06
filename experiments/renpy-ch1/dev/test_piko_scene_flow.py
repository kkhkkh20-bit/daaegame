"""피코 곁의 선택은 사망 확인 뒤에만 열리고 관찰·청취·자료 소유를 바꾸지 않는다."""
import copy
import textwrap
from test_newworld_text import Layer, ROOT


class PikoSceneFlow(Layer):
    def ready(self):
        env=self.load()
        self.state.room13.update(day=3,location="square")
        env['r13_v111_commit']('MS14_D03_S01_L0021')
        self.state.r13_piko_scene_near=True
        source=(ROOT/'game/systems/room13_piko_scene.rpy').read_text()
        code=source.split('init 320 python:\n',1)[1].split('\nscreen ',1)[0]
        exec(compile(textwrap.dedent(code),'피코 곁의 관찰','exec'),env)
        return env

    def test_only_confirmed_dead_stolen_scene_with_owned_portrait_is_available(self):
        env=self.ready()
        self.assertTrue(env['r13_piko_scene_available']())
        before=copy.deepcopy(self.state.room13)
        self.assertTrue(env['r13_piko_scene_available']())
        self.assertEqual(before,self.state.room13)
        for key,value in [('piko_alive',True),('piko_alive',None),('lamp_bound2',True)]:
            env=self.ready();env['r13_v111_set'](key,value)
            self.assertFalse(env['r13_piko_scene_available']())
        for field,value in [('day',4),('location','dining')]:
            env=self.ready();self.state.room13[field]=value
            self.assertFalse(env['r13_piko_scene_available']())
        env=self.ready();self.state.room13['evidence'].clear()
        self.assertFalse(env['r13_piko_scene_available']())

    def test_question_order_and_repetition_do_not_grant_or_change_gameplay_state(self):
        env=self.ready();before=copy.deepcopy(self.state.room13)
        for near in (True,False):
            self.state.r13_piko_scene_near=near
            for key in ('daram','posture','portrait','posture','daram'):
                rows=env['r13_piko_scene_lines'](env['r13_nw_block']('piko_scene_'+key),key=='portrait')
                self.assertTrue(rows)
                self.assertNotIn('resident_piko',[r[0] for r in rows])
                self.assertEqual(rows[0][2]['cut'],'piko-death3' if near and key!='portrait' else None)
                self.assertEqual(before,self.state.room13)
        self.assertIn('언제 숨졌는지는 저도 몰라요',' '.join(r[1] for r in env['r13_piko_scene_lines'](env['r13_nw_block']('piko_scene_posture'))))

    def test_handover_precedes_optional_scene_and_existing_investigation_remains_exit(self):
        source=(ROOT/'game/room13_v111_days123.rpy').read_text()
        dead=source.split('label r13_v111_piko_dead3:',1)[1].split('\nlabel ',1)[0]
        self.assertLess(dead.index("r13_v111_commit('MS14_D03_S01_L0021')"),dead.index('call r13_piko_scene3'))
        self.assertIn('jump r13_v111_lamp3',dead)
        flow=source.split('label r13_piko_scene3:',1)[1].split('label r13_v111_lamp3:',1)[0]
        self.assertNotIn('r13_v111_commit',flow)
        self.assertNotIn('r13_v111_time',flow)
        self.assertIn('call screen r13_pw_picture("V111:E09",called=True)',flow)
        self.assertLess(flow.index('call r13_lines('),flow.index('r13_v111_set("piko_scene_read:'))
