"""하차 효과음은 없애고 다른 장면의 배경음·타이핑·연출음은 보존한다."""
import ast
import copy
import re
import textwrap
import types
import unittest

from test_newworld_text import Layer, ROOT


def python_nodes(path):
    source = path.read_text()
    nodes = []
    for match in re.finditer(r'^init(?: -?\d+)? python:\n((?:[ \t].*\n|\n)*)', source, re.M):
        nodes.extend(ast.parse(textwrap.dedent(match.group(1))).body)
    return nodes


def load_functions(env, path, names):
    nodes = [node for node in python_nodes(path) if isinstance(node, ast.FunctionDef) and node.name in names]
    assert {node.name for node in nodes} == set(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), env)


class CarriageDisembarkAudio(Layer):
    def audio_environment(self):
        env = self.load()
        self.played, self.stopped = [], []
        env.update(
            renpy=types.SimpleNamespace(
                music=types.SimpleNamespace(
                    play=lambda *args, **kw: self.played.append((args, kw)),
                    stop=lambda *args, **kw: self.stopped.append((args, kw))),
                loadable=lambda path: True,
                is_skipping=lambda: False,
                in_rollback=lambda: False,
                hide_screen=lambda *args: None,
                show_layer_at=lambda *args, **kw: None),
            persistent=types.SimpleNamespace(room13_motion=False),
            source_fx=lambda key: self.played.append(('source_fx', key)))
        self.state.place = '눈에 막힌 입구'
        self.state.r13_impact_log = []
        return env

    def test_handoff_stops_all_carriage_and_prior_effect_channels_immediately(self):
        env = self.audio_environment()
        load_functions(env, ROOT / 'game/room13_carriage_direction.rpy', {'r13_carriage_finish'})
        self.state.r13_carriage_narrow = True
        self.state.typing_allowed = True
        env['r13_carriage_finish']()
        self.assertEqual({kw['channel'] for _, kw in self.stopped},
                         {'carriage_ride', 'carriage_hooves', 'scene_fx', 'sound'})
        self.assertTrue(all(kw['fadeout'] == 0 for _, kw in self.stopped))
        self.assertFalse(self.played)
        self.assertFalse(self.state.r13_carriage_narrow)
        self.assertTrue(self.state.typing_allowed)
        self.assertFalse({'music', 'typing'} & {kw['channel'] for _, kw in self.stopped})

    def test_actual_arrival_rows_have_no_direct_or_impact_sound(self):
        env = self.audio_environment()
        path = ROOT / 'game/systems/room13_ep_art.rpy'
        lower = copy.deepcopy(next(node for node in python_nodes(path)
                                   if isinstance(node, ast.FunctionDef) and node.name == 'r13_ep_line_art'))
        lower.name = '_r13_impact_line_art'
        exec(compile(ast.Module(body=[lower], type_ignores=[]), str(path), 'exec'), env)
        impact = ROOT / 'game/systems/room13_impact_fx.rpy'
        spec = next(node for node in python_nodes(impact) if isinstance(node, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == 'R13_IMPACT_FX' for t in node.targets))
        exec(compile(ast.Module(body=[spec], type_ignores=[]), str(impact), 'exec'), env)
        load_functions(env, impact, {'r13_ep_line_art', 'r13_packet_impact', 'r13_impact'})
        source = (ROOT / 'game/room13_v111_days123.rpy').read_text()
        rids = []
        for label in ('r13_v111_carriage_end', 'r13_v111_gate_arrival'):
            scene = re.search(r'^label ' + label + r':\n(.*?)(?=^label )', source, re.M | re.S).group(1)
            rids += ast.literal_eval(re.search(r'r13_v111_lines\((\[[^\]]*\])\)', scene).group(1))
        before = copy.deepcopy(self.state.room13)
        for packet in env['r13_v111_lines'](rids):
            env['r13_ep_line_art'](packet)
        self.assertFalse(self.played)
        self.assertEqual(before, self.state.room13)
        # 같은 효과음을 쓰던 다른 장면도 무음, 별개로 쓰는 강한 충격음은 보존한다.
        env['r13_impact']('jolt')
        self.assertFalse(self.played)
        env['r13_impact']('shake')
        self.assertEqual(self.played[-1][1]['channel'], 'scene_fx')

    def test_no_carriage_transition_steps_but_other_place_steps_remain(self):
        env = self.audio_environment()
        path = ROOT / 'game/systems/room13_sound.rpy'
        sets = [node for node in python_nodes(path) if isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id in {'R13_INDOOR', 'R13_OUTDOOR'} for t in node.targets)]
        exec(compile(ast.Module(body=sets, type_ignores=[]), str(path), 'exec'), env)
        load_functions(env, path, {'r13_sound_move'})
        self.assertIsNone(env['r13_sound_move']('winter_carriage', 'winter'))
        self.assertIsNone(env['r13_sound_move']('winter', 'winter'))
        self.assertEqual(env['r13_sound_move']('winter', 'winter_square'), 'steps_snow')
        self.assertEqual(env['r13_sound_move']('winter', 'front'), 'doorOpen')


if __name__ == '__main__':
    unittest.main()
