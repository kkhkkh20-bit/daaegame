"""하차 대사의 일회성 소리만 없애고 일반 충격·주행·타이핑 소리를 보존한다."""
import ast
import re
import textwrap
from types import SimpleNamespace
from unittest.mock import Mock
from test_newworld_text import Layer, ROOT

class CarriageArrivalAudio(Layer):
    def impact_runtime(self, *, skipping=False, motion=True):
        env=self.load()
        env['store'].r13_impact_log=[]
        music=SimpleNamespace(play=Mock())
        env.update(
            renpy=SimpleNamespace(music=music,is_skipping=lambda:skipping,
                in_rollback=lambda:False,loadable=lambda path:True,
                show_layer_at=Mock(),show_screen=Mock()),
            persistent=SimpleNamespace(room13_motion=motion),
            Transform=lambda **kw:kw,r13_ep_line_art=lambda packet:None)
        source=(ROOT/'game/systems/room13_impact_fx.rpy').read_text()
        block=re.search(r'^init 345 python:\n((?:[ \t].*\n|\n)*)',source,re.M).group(1)
        exec(textwrap.dedent(block),env)
        return env,music

    def test_actual_disembarkation_packets_are_silent_in_every_mode(self):
        # 일반 진행/설정 동작 끄기/건너뛰기의 출력 packet을 실제 충격 dispatcher에 전달한다.
        for skipping,motion in ((False,True),(False,False),(True,True),(True,False)):
            with self.subTest(skipping=skipping,motion=motion):
                env,music=self.impact_runtime(skipping=skipping,motion=motion)
                packets=env['r13_v111_lines'](['MS14_D01_S02_L0002','MS14_D01_S02_L0003','MS14_D01_S02_L0005'])
                self.assertTrue(any('혼자 내려갈' in p[1] for p in packets),'하차 대사 자체는 보존한다')
                for packet in packets:
                    self.assertIsNone(env['r13_packet_impact'](packet))
                    env['r13_ep_line_art'](packet)
                music.play.assert_not_called()
                self.assertEqual(env['store'].r13_impact_log,[])

    def test_other_impacts_keep_their_sound_even_when_motion_is_off(self):
        # 전역 음소거나 공통 임팩트 제거로 하차 소리를 감추지 않는다.
        for motion in (True,False):
            with self.subTest(motion=motion):
                env,music=self.impact_runtime(motion=motion)
                env['r13_ep_line_art'](('daram','다른 장면의 반응',{'fx':'jolt'}))
                music.play.assert_called_once_with('assets/sfx-present.wav',channel='scene_fx',loop=False)
                self.assertEqual(env['store'].r13_impact_log,['jolt'])

    def test_carriage_exit_adds_no_movement_sound(self):
        # 하차 대사를 무음으로 바꾼 뒤 장면 이동 효과음으로 우회하지 않는다.
        source=(ROOT/'game/systems/room13_sound.rpy').read_text()
        block=re.search(r'^    def r13_sound_move\(prev, bg\):\n((?:[ \t].*\n|\n)*)',source,re.M).group(0)
        env={}
        tree=ast.parse(textwrap.dedent(block))
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='r13_sound_move')
        exec(compile(ast.Module(body=[node],type_ignores=[]),'movement','exec'),env)
        self.assertIsNone(env['r13_sound_move']('winter_carriage','winter'))
        self.assertIsNone(env['r13_sound_move']('winter','winter_carriage'))

    def test_finishing_carriage_preserves_typing_and_does_not_stop_bgm(self):
        # 실제 종료 함수는 주행 채널을 끝내며, 타이핑을 복구하고 BGM을 끄지 않는다.
        source=(ROOT/'game/room13_carriage_direction.rpy').read_text()
        block=re.search(r'^    def r13_carriage_finish\(\):\n((?:[ \t].*\n|\n)*)',source,re.M).group(0)
        music=SimpleNamespace(stop=Mock(),play=Mock())
        state=SimpleNamespace(r13_carriage_narrow=True,typing_allowed=False)
        env=dict(store=state,renpy=SimpleNamespace(music=music,hide_screen=Mock(),show_layer_at=Mock()))
        exec(textwrap.dedent(block),env)
        env['r13_carriage_finish']()
        self.assertTrue(state.typing_allowed)
        self.assertFalse(state.r13_carriage_narrow)
        stopped={c.kwargs['channel'] for c in music.stop.call_args_list}
        self.assertTrue({'carriage_ride','carriage_hooves'}<=stopped)
        self.assertFalse(stopped & {'music','ambience','typing'})
        music.play.assert_not_called()
