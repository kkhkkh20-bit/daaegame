"""Production question-discovery gates; no Ren'Py visual/playthrough claim."""
import ast
import re
import textwrap
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def function(ns, source, name):
    lines = source.splitlines(True)
    start = next(i for i, line in enumerate(lines) if line.startswith('    def '+name+'('))
    end = start+1
    while end < len(lines) and (not lines[end].strip() or lines[end].startswith('        ')):
        end += 1
    exec(compile(textwrap.dedent(''.join(lines[start:end])), name, 'exec'), ns)

class GroundedQuestions(unittest.TestCase):
    def setUp(self):
        self.s = dict(flags=[], evidence=[], read_topics=[], question_cues={})
        source = (ROOT/'game/systems/room13_question_discovery.rpy').read_text()
        literal = re.search(r'    R13_QUESTION_LEADS = (\{.*?\n    \})', source, re.S).group(1)
        self.n = dict(store=types.SimpleNamespace(room13=self.s), R13_QUESTION_LEADS=ast.literal_eval(literal), r13_has=lambda k:k in self.s['flags']+self.s['evidence'])
        for name in ('r13_question_lead_known','r13_question_discovered'):
            function(self.n, source, name)
    def known(self, key):
        return self.n['r13_question_discovered'](key,{})
    def test_named_meal_needs_actual_named_meal_not_day_or_name(self):
        self.s['day']=2
        self.assertFalse(self.known('life:nabi'))
        self.s['flags']=['mother_lamplighter_lead','nabi_helped']
        self.assertFalse(self.known('life:nabi'))
        self.s['read_topics']=['help:nabi']
        self.assertTrue(self.known('life:nabi'))
    def test_legacy_completed_help_and_heard_topic_are_preserved(self):
        self.s['flags']=['life:nabi_helped']
        self.assertTrue(self.known('life:nabi'))
        self.s['flags']=[];self.s['read_topics']=['life:nabi']
        self.assertTrue(self.known('life:nabi'))
    def test_light_challenge_follows_denial_and_keeps_old_heard_topic(self):
        self.s['flags']=['heard_kitchen_light']
        self.assertFalse(self.known('cross:nabi_light'))
        self.s['flags'].append('asked_nabi_door')
        self.assertTrue(self.known('cross:nabi_light'))
        self.s['flags']=[];self.s['read_topics']=['cross:nabi_light']
        self.assertTrue(self.known('cross:nabi_light'))
    def test_night_door_cannot_precede_witness_and_old_deadlock_removed(self):
        source=(ROOT/'game/room13_conversations.rpy').read_text()
        self.assertIn('("cross:nabi_door","nabi","밤에 주방에는 누가 들어가?",["heard_kitchen_light"],[',source)
        self.assertIn('ROOM13["topics"]["cross:nabi_door"]["not_flags"]=["nabi_light_asked"]',source)
        self.assertNotIn('ROOM13["topics"]["cross:nabi_door"]["not_flags"]=["heard_kitchen_light"]',source)
    def test_first_contact_and_crime_evidence_gates_untouched(self):
        self.assertTrue(self.known('help:nabi'))
        for key in ('nabi_alibi','nabi_gap','poc:nabi_packet'):
            self.assertTrue(self.known(key)) # underlying day/evidence need gates still apply
    def test_tosil_flavor_does_not_supply_solution_but_witness_route_remains(self):
        source=(ROOT/'game/systems/room13_new_cast.rpy').read_text()
        flavor=source.split('_r13_nc_topic("tosil:granny"',1)[1].split('_r13_nc_topic("tosil:forest"',1)[0]
        for spoiler in ('밤에는','아래층','창고','밤마다','thought'):
            self.assertNotIn(spoiler,flavor)
        self.assertIn('무섭기도 하고 다정하기도 해요.',flavor)
        forest=source.split('_r13_nc_topic("tosil:forest"',1)[1].split('_r13_nc_topic(',1)[0]
        self.assertIn('need=["tosil_errand_seen"]',forest)
        self.assertIn('flags=["tosil_confessed"]',forest)

if __name__=='__main__':unittest.main()
