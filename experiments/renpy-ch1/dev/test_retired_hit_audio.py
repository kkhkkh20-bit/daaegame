"""제거한 히트음의 별칭·회의 큐·이전 저장 호환을 실제 함수로 확인한다."""
import ast
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock
import wave
from test_carriage_disembark_audio import python_nodes, load_functions
from test_newworld_text import ROOT


class RetiredHitAudio(TestCase):
    def runtime(self, skipping=False, available=True):
        path=ROOT/'game/systems/room13_sound.rpy'
        music=SimpleNamespace(play=Mock())
        env=dict(renpy=SimpleNamespace(music=music,loadable=lambda p:available,is_skipping=lambda:skipping),
                 store=SimpleNamespace(source_effect_log=[],r13_meeting_active=False),
                 _r13_sound_source_fx=Mock(),r13_fx_cue=Mock(),
                 _r13_sound_debate_judge=Mock(return_value=('break','내용')))
        mapping=next(n for n in python_nodes(path) if isinstance(n,ast.Assign)
                     and any(isinstance(t,ast.Name) and t.id=='R13_FX' for t in n.targets))
        exec(compile(ast.Module(body=[mapping],type_ignores=[]),str(path),'exec'),env)
        load_functions(env,path,{'source_fx','r13_fx_path','r13_debate_judge'})
        return env,music

    def test_retired_aliases_never_play_or_fall_back(self):
        for skipping in (False,True):
            for available in (False,True):
                env,music=self.runtime(skipping,available)
                for key in ('impact','cut9','present'):
                    self.assertIsNone(env['r13_fx_path'](key))
                    env['source_fx'](key)
                music.play.assert_not_called()
                env['_r13_sound_source_fx'].assert_not_called()
                self.assertEqual(env['store'].source_effect_log,[])

    def test_other_sound_and_unknown_fallback_are_preserved(self):
        env,music=self.runtime()
        for key in ('right','wrong','found','tap','steps_snow'):
            env['source_fx'](key)
            music.play.assert_called_with(env['r13_fx_path'](key),channel='scene_fx',loop=False)
        env['source_fx']('legacy_key')
        env['_r13_sound_source_fx'].assert_called_once_with('legacy_key')

    def test_debate_queue_keeps_only_result_sound_and_original_result(self):
        for result,expected in (('break','right'),('wrong','wrong'),('other',None)):
            with self.subTest(result=result):
                env,music=self.runtime()
                original=(result,'내용')
                env['_r13_sound_debate_judge'].return_value=original
                self.assertEqual(env['r13_debate_judge']('C1','S1','E1'),original)
                if expected:
                    music.play.assert_called_once_with(['assets/sfx-'+expected+'.wav'],channel='scene_fx',loop=False)
                else:
                    music.play.assert_not_called()
                self.assertEqual(env['r13_fx_cue'].call_count,1 if result=='break' else 0)

    def test_old_saved_direct_path_is_valid_digital_silence(self):
        with wave.open(str(ROOT/'game/assets/sfx-present.wav'),'rb') as wav:
            self.assertEqual(wav.getcomptype(),'NONE')
            self.assertEqual(wav.getsampwidth(),2)
            self.assertGreater(wav.getnframes(),0)
            self.assertLess(wav.getnframes()/wav.getframerate(),.1)
            self.assertFalse(any(wav.readframes(wav.getnframes())))
