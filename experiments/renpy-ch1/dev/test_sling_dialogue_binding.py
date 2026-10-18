"""Actual earned Sling provider and generated cue integration; no native visual claim."""
import copy
import json
import unittest
from pathlib import Path
from test_sling_choice_flow import load_function
ROOT=Path(__file__).resolve().parents[1]
class SlingDialogueBinding(unittest.TestCase):
    def setUp(self):
        self.queue=json.loads((ROOT/'docs/reviews/dialogue-beats/runtime-binding-queue.json').read_text())
        self.registry=json.loads((ROOT/'game/assets/room13-dialogue-bindings.json').read_text())
    def test_sling_actual_providers_all_earned_routes_bind_without_state_changes(self):
        from test_sling_earned_disclosure import EarnedDisclosure
        matches=[q for q in self.queue if q.get('provider_scope',{}).get('function')=='r13_sling_confront_lines']
        self.assertEqual(1,len(matches))
        spec=matches[0]
        self.assertEqual('game/systems/room13_sling_confidence.rpy',spec['provider_scope']['source'])
        for branch in ('legacy','J06','E18_J08'):
            fixture=EarnedDisclosure();fixture.setUp()
            if branch=='legacy':fixture.flag('know_granny_reads')
            else:
                fixture.flag('sling_job_pressure_heard')
                fixture.ready(('J06',) if branch=='J06' else ('E18','J08'))
            load_function(fixture.n,'systems/room13_dialogue_bindings.rpy','r13_bind_dialogue_rows')
            before=copy.deepcopy(fixture.s)
            rows=fixture.n['r13_sling_confront_lines']()
            self.assertEqual(4,len(rows))
            result=fixture.n['r13_bind_dialogue_rows'](rows,'sling:confidence:confront',spec['binding_route'],self.registry)
            self.assertEqual([],result['unresolved'])
            self.assertEqual({'1','3'},set(result['rows']))
            self.assertEqual('anxious',result['rows']['1']['emotion'])
            self.assertEqual('neutral',result['rows']['3']['emotion'])
            self.assertEqual(before,fixture.s)


if __name__=='__main__':unittest.main(verbosity=2)
