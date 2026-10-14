"""Observation viewpoint, companion presence, and repeat-budget regressions."""
import copy
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace


class ObservationTests(unittest.TestCase):
    def setUp(self):
        self.state = dict(day=1, period=1, location='square', daram_state='with_dad',
                          case_state='pending', flags=['entry_corrected'], evidence=['E01'])
        self.env = dict(store=SimpleNamespace(room13=self.state),
                        r13_has=lambda flag: flag in self.state['flags'],
                        r13_edit=lambda **changes: self.state.update(changes))
        source = (Path(__file__).resolve().parents[1]/'game/room13_thoughts.rpy').read_text()
        exec(textwrap.dedent(source.split('init 63 python:\n')[1].split('\nlabel ')[0]), self.env)

    def make(self, identity='object:square:cart', entries=None):
        return self.env['r13_make_observation_lines'](
            entries or [(None, '바퀴에 눈이 묻어 있다.')], identity)

    def test_facts_and_other_speaker_preserved_without_state_mutation(self):
        before = copy.deepcopy(self.state)
        lines = self.make('object:case:trace', [(None, '흔적은 두 줄이다.'), ('dad', '문은 잠겼다.'), ('guard', '기다리세요.')])
        self.assertEqual(lines[0][:2], ('dad', '(흔적은 두 줄이다.)'))
        self.assertTrue(lines[0][2]['thought'])
        self.assertEqual(lines[1][1], '(문은 잠겼다.)')
        self.assertEqual(lines[2], ('guard', '기다리세요.'))
        self.assertEqual(self.state, before)

    def test_child_requires_actual_companionship(self):
        for state in ['held', 'separated', 'lost']:
            self.state['daram_state'] = state
            self.assertFalse(any(p[0] == 'daram' for p in self.make()))
        self.state.update(daram_state='with_dad', flags=[])
        self.assertEqual(len(self.make()), 1)
        self.state['flags'] = ['entry_corrected']
        lines = self.make()
        self.assertEqual([p[0] for p in lines], ['dad', 'dad', 'daram'])
        self.assertFalse(lines[1][2].get('thought', False))

    def test_repeat_and_period_budget_do_not_change_clock_or_evidence(self):
        remember = self.env['r13_remember_observation_chat']
        remember('object:square:cart')
        self.assertEqual(len(self.make()), 1)
        remember('object:square:stall')
        self.assertEqual(len(self.make('object:inn:door')), 1)
        self.assertEqual((self.state['day'], self.state['period'], self.state['evidence']), (1, 1, ['E01']))
        self.state['period'] = 2
        self.assertEqual(len(self.make()), 3)

    def test_no_light_banter_at_active_crime_scene(self):
        self.state['case_state'] = 'occurred'
        self.assertEqual(len(self.make('object:room13:bread')), 1)
        self.assertEqual(len(self.make('puzzle:book:locked')), 1)


if __name__ == '__main__':
    unittest.main()
