"""Coverage must retain the full roster and separate fallbacks from verified art."""
import json
import unittest
from pathlib import Path
import art_coverage
import art_display_metrics
import ast

ROOT=Path(__file__).resolve().parents[1]


class ArtCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=art_coverage.build()
        cls.rows={r['id']:r for r in cls.data['items']}

    def test_roster_and_stable_unique_ids(self):
        self.assertEqual(len(self.data['canonical_roster']),48)
        self.assertEqual(set(self.data['runtime_roster']),set(json.loads((ROOT/'game/assets/cast.json').read_text())))
        self.assertEqual(len(self.rows),len(self.data['items']))
        for person in self.data['canonical_roster']:
            self.assertIn(f'character/{person}/dialogue/neutral',self.rows)

    def test_fallback_is_not_finished_expression(self):
        doto=self.rows['character/resident_teacher/dialogue/joy']
        self.assertEqual(doto['production_status'],'not_produced')
        self.assertEqual(doto['connection_status'],'neutral_fallback')
        self.assertEqual(self.rows['character/guard/dialogue/angry']['production_status'],'available_unreviewed')
        self.assertEqual(self.rows['character/dad/dialogue/neutral']['production_status'],'not_required_viewpoint')

    def test_links_and_review_evidence(self):
        for row in self.rows.values():
            self.assertNotEqual(row['connection_status'],'broken_path',row['id'])
            if row['screen_review']['status']=='passed':
                self.assertTrue(row['screen_review']['evidence'])
        self.assertEqual(self.rows['map/hall/after/evening']['event_condition'],'case_state == occurred')
        candidate=next(r for r in self.data['registry_audit'] if r['pose']=='living_wheelsnow')
        self.assertEqual(candidate['status'],'held')

    def test_packet_uses_real_sources_and_unique_targets(self):
        packet=json.loads((ROOT/'docs/art-coverage/batch-01.json').read_text())
        outputs=[o for job in packet['jobs'] for o in job['outputs']]
        self.assertEqual(len(outputs),packet['output_count'])
        self.assertEqual(len({o['id'] for o in outputs}),len(outputs))
        for job in packet['jobs']:
            self.assertTrue((ROOT/job['approved_reference']).is_file())
            for output in job['outputs']:
                self.assertIn(output['id'],self.rows)

    def test_display_scale_matches_runtime_function(self):
        path=ROOT/'game/room13_fullbody_dialogue.rpy'
        functions=[node for tree,_ in art_coverage.init_trees(path) for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='r13_fullbody_scale']
        env={'R13_FULLBODY':json.loads((ROOT/'game/assets/room13-fullbody-dialogue.json').read_text()),
             'R13_FULLBODY_FIGURE':1.05,'R13_FULLBODY_TUNING':{'bami':.88,'doto':.92}}
        exec(compile(ast.Module(body=functions,type_ignores=[]),'runtime-scale','exec'),env)
        for row in art_display_metrics.build():
            self.assertAlmostEqual(row['scale_in_reference_coordinates'],env['r13_fullbody_scale'](row['character'],row['dialogue_height']))


if __name__=='__main__':unittest.main()
