"""The basic day-14 ration copy answers altar 4 but never substitutes for the ending ledger."""
import ast
import json
from pathlib import Path
import textwrap
import unittest

GAME = Path(__file__).resolve().parents[1] / 'game'

class AltarRations(unittest.TestCase):
    def setUp(self):
        source = (GAME / 'room13_v111_newworld_rules.rpy').read_text().split('init 318 python:', 1)[-1]
        # Load only the pure proof tables/functions and ending predicate.
        tree = ast.parse(textwrap.dedent(source))
        names = {'R13_PROOF_ALTERNATES', 'R13_PROOF_EXTRAS', 'r13_v111_proof_sets', 'r13_v111_proof_accepts', 'r13_nw_true_ending_ready'}
        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names or isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in n.targets)]
        self.env = {}
        exec(compile(ast.Module(body=nodes, type_ignores=[]), '<rules>', 'exec'), self.env)

    def test_complete_sources_only(self):
        accept = lambda keys: self.env['r13_v111_proof_accepts']('맨 처음 이름을 짚는다', ['NW_NAMES', 'NW_NEOUL_LEDGER'], ['V111:'+k for k in keys])
        for record in ('NW_NEOUL_LEDGER', 'NW_OLD_RATIONS'):
            self.assertTrue(accept(['NW_NAMES', record]))
            self.assertFalse(accept([record]))
        self.assertFalse(accept(['NW_NAMES']))
        self.assertTrue(accept(['NW_NAMES', 'NW_NEOUL_LEDGER', 'NW_OLD_RATIONS']))

    def test_ending_still_requires_actual_ledger(self):
        values = {'ending14':'morning','grand:fire':True,'grand:soup':True, **{'meeting:'+m:'win' for m in ('records','hypothesis','blanket','altar')}}
        owned = {'NW_OLD_RATIONS', 'NW_NAMES'}
        self.env.update(r13_v111_value=values.get,r13_nw_loss_count=lambda:0,r13_v111_owned=lambda k:k in owned)
        self.assertFalse(self.env['r13_nw_true_ending_ready']())
        owned.add('NW_NEOUL_LEDGER')
        self.assertTrue(self.env['r13_nw_true_ending_ready']())

    def test_dialogue_uses_submitted_source_even_when_both_are_owned(self):
        source = (GAME/'room13_v111_newworld_text.rpy').read_text()
        given = []
        conditions = {}
        for key in ('altar4_won_with_ledger', 'altar4_won_with_rations'):
            line = next(line.strip() for line in source.splitlines() if line.strip().startswith('"'+key+'":'))
            conditions[key] = eval(line.split(':',1)[1].rstrip(','), {'r13_v111_value':lambda key:given})
        for submitted, expected in ((['NW_NAMES','NW_OLD_RATIONS'], (False,True)), (['NW_NAMES','NW_NEOUL_LEDGER'], (True,False)), (['NW_NAMES','NW_NEOUL_LEDGER','NW_OLD_RATIONS'], (True,False))):
            given[:] = ['V111:'+k for k in submitted]
            self.assertEqual(tuple(f() for f in conditions.values()), expected)

    def test_mandatory_morning_acquires_separate_record(self):
        source = (GAME/'room13_v111_days1114.rpy').read_text()
        morning = source.split('label r13_v111_morning_safe14:',1)[1].split('label r13_v111_altar_guide14:',1)[0]
        self.assertIn('call r13_v111_old_rations14\n    jump r13_v111_altar_guide14', morning)
        self.assertIn('r13_nw_acquire("NW_OLD_RATIONS")', morning)
        self.assertNotIn('r13_nw_acquire("NW_NEOUL_LEDGER")', morning)
        rows = json.loads((GAME/'v111/newworld/d14.json').read_text())['blocks']['altar4_won14']
        sources = {r.get('when'): r['text'] for r in rows}
        self.assertIn('너울 씨 장부', sources['altar4_won_with_ledger'])
        self.assertIn('학교에서 확인한', sources['altar4_won_with_rations'])

if __name__ == '__main__': unittest.main()
