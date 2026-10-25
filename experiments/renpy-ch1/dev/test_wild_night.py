"""불타는 밤 진입 경계와 가족 결과의 모든 조합."""
import ast
import itertools
from pathlib import Path
import textwrap
import unittest

ROOT=Path(__file__).resolve().parents[1]
class WildNight(unittest.TestCase):
    def setUp(self):
        source=(ROOT/'game/room13_v111_newworld_rules.rpy').read_text().split('init 318 python:',1)[1]
        tree=ast.parse(textwrap.dedent(source))
        names={'r13_nw_wild_night_ready','r13_nw_wild_family','R13_NW_WILD_LATE_OK'}
        nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names or isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets)]
        self.values={}; self.env={'r13_v111_value':self.values.get}
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'<wild>','exec'),self.env)
    def test_entry_all_endings_and_meeting_results(self):
        for ending,hyp,altar in itertools.product(('morning','family','partial','violence','left_name','frozen','true','wild_night'),('win','partial','lose',None),('win','partial','lose',None)):
            self.values.update(ending14=ending,**{'meeting:hypothesis':hyp,'meeting:altar':altar})
            self.assertEqual(self.env['r13_nw_wild_night_ready'](),(ending,hyp,altar)==('morning','lose','lose'))
    def test_family_boundaries(self):
        for fever in (False,True):
            for late in range(4):
                self.values.update(daram_fever12=fever,wild_late=late)
                expected=('no_mom' if fever else 'three') if late<=1 else ('alone' if fever else 'no_mom')
                self.assertEqual(self.env['r13_nw_wild_family'](),expected)
    def test_omens_require_loss_and_the_present_speaker(self):
        source=(ROOT/'game/room13_v111_newworld_text.rpy').read_text()
        present={'resident_teacher','karo','guard','daram'}
        env=dict(self.env,r13_v111_actor_ready=lambda who:who in present)
        conditions={}
        for key in ('wild_omen12','wild_omen13_karo','wild_omen13_gate','wild_omen13_gate_kept','wild_omen13_gate_relit'):
            row=next(line.strip() for line in source.splitlines() if line.strip().startswith('"'+key+'":'))
            conditions[key]=eval(row.split(':',1)[1].rstrip(','),env)
        for result in ('win','partial',None):
            self.values['meeting:hypothesis']=result
            self.assertFalse(any(check() for check in conditions.values()))
        self.values['meeting:hypothesis']='lose'
        self.assertTrue(conditions['wild_omen12']())
        self.assertTrue(conditions['wild_omen13_karo']())
        for issue in (None,'lost','won'):
            self.values['hyp_issue:1']=issue
            self.assertEqual(conditions['wild_omen13_gate_relit'](),issue=='won')
            self.assertEqual(conditions['wild_omen13_gate_kept'](),issue!='won')
        present.clear()
        self.assertFalse(any(check() for check in conditions.values()))
    def test_default_delay_is_zero(self):
        self.assertEqual(self.env['r13_nw_wild_family'](),'three')
if __name__=='__main__':unittest.main()
