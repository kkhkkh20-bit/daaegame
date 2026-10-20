"""Pure placement regressions; no Ren'Py dependency, no claim of rendered QA.
Run: python dev/test_inn_sofa_placement.py [--game path/to/game]
The default game path is adjacent to this dev directory.
"""
import argparse
import copy
import json
from pathlib import Path
import textwrap
from types import SimpleNamespace
import unittest

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--game', type=Path, default=Path(__file__).resolve().parents[1] / 'game')
ARGS, REST = PARSER.parse_known_args()
GAME = ARGS.game


class InnSofaPlacementTests(unittest.TestCase):
    def setUp(self):
        rows = json.loads((GAME / 'assets/room13-map-action27.json').read_text())['rows']
        acting = json.loads((GAME / 'assets/room13-pixel-acting.json').read_text())
        self.specs = {
            ('resident_nubi', 'map27_in_1'): next(row['spec'] for row in rows if row['person'] == 'resident_nubi' and row['location'] == 'inn'),
            ('resident_tosil', 'living_thermos'): acting['resident_tosil']['living_thermos'],
        }
        self.actors = [dict(person=p, pose=pose, x=0, y=0, width=100, height=248,
                            rect=[0, 0, 100, 248], depth=655, activity='original activity')
                       for p, pose in self.specs]
        self.store = SimpleNamespace(room13=dict(location='inn', day=2, period=0,
            flags=['sentinel_flag'], read_topics=['sentinel_topic'], case_state='before'))
        self.offers = set()
        self.width = 1920
        self.entry_calls = []
        def stage(entry=False):
            self.entry_calls.append(entry)
            return copy.deepcopy(self.actors)
        env = dict(store=self.store, r13_stage_people=stage,
            r13_offer_for_person=lambda person: person in self.offers,
            r13_world_width=lambda: self.width,
            r13_acting_spec=lambda person, pose: self.specs[person, pose],
            r13_actor_geometry=lambda person, pose: self.specs[person, pose]['crop'][2:],
            r13_home_with_daram=lambda: False)
        path = GAME / 'systems/room13_spatial_contacts.rpy'
        code = path.read_text().split('init 179 python:\n', 1)[1]
        exec(compile(textwrap.dedent(code), str(path), 'exec'), env)
        self.stage = env['r13_stage_people']

    def call_immutable(self, entry=False):
        before = copy.deepcopy((self.store.room13, self.actors, self.specs, self.offers))
        result = self.stage(entry)
        self.assertEqual(before, (self.store.room13, self.actors, self.specs, self.offers))
        self.assertEqual(self.entry_calls[-1], entry)
        return result

    def test_exact_geometry_and_proportional_dimensions(self):
        for actor in self.call_immutable():
            is_nubi = actor['person'] == 'resident_nubi'
            foot, height = ((420, 535), 226) if is_nubi else ((535, 535), 215)
            spec = self.specs[actor['person'], actor['pose']]
            scale = height / float(spec['crop'][3])
            self.assertEqual(actor['height'], height)
            self.assertEqual(actor['depth'], 535)
            self.assertEqual(len(actor['map27_occlusion']), 4)
            self.assertEqual(actor['map27_keepouts'], [])
            self.assertEqual(actor['activity'], 'original activity')
            self.assertLessEqual(abs(actor['width'] - spec['crop'][2] * scale), .5)
            for index, key in enumerate(('x', 'y')):
                self.assertLessEqual(abs(actor[key] + spec['foot'][index] * scale - foot[index]), .5)

    def test_schedule_state_is_not_modified_or_used_to_spawn(self):
        original = copy.deepcopy(self.actors)
        for day in (1, 2, 5, 14):
            for period in (0, 1, 2, 3):
                self.store.room13.update(day=day, period=period)
                for selection in ([], original[:1], original[1:], original):
                    self.actors = copy.deepcopy(selection)
                    for entry in (False, True):
                        result = self.call_immutable(entry)
                        self.assertCountEqual([a['person'] for a in result], [a['person'] for a in selection])

    def test_each_offer_bypasses_placement_without_changing_other_actor(self):
        for actor in self.actors:
            self.offers = {actor['person']}
            result = self.call_immutable()
            self.assertEqual(next(a for a in result if a['person'] == actor['person']), actor)
            other = next(a for a in result if a['person'] != actor['person'])
            self.assertEqual(other['depth'], 535)
        self.offers = {a['person'] for a in self.actors}
        self.assertEqual(self.call_immutable(), self.actors)

    def test_other_locations_and_world_width_are_unchanged(self):
        for location in ('hall', 'school', 'forest'):
            self.store.room13['location'] = location
            self.assertEqual(self.call_immutable(), self.actors)
        self.store.room13['location'] = 'inn'
        for width in (1280, 1800, 2160):
            self.width = width
            self.assertEqual(self.call_immutable(), self.actors)

    def test_nonordinary_poses_are_not_replaced(self):
        for actor in self.actors:
            actor['pose'] = 'authored_event_pose'
        self.assertEqual(self.call_immutable(), self.actors)

    def test_other_identity_is_not_changed(self):
        self.actors = [dict(person='resident_unrelated', pose='neutral', depth=600,
                            activity='original', x=10, y=10, width=10, height=10, rect=[10,10,10,10])]
        self.assertEqual(self.call_immutable(), self.actors)


if __name__ == '__main__':
    unittest.main(argv=[__file__] + REST)
