"""0.20.5 (Codex S03): Daram's place reads the newer location key before the older one."""
import re,textwrap,unittest
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1]
class DaramWhere(unittest.TestCase):
    def setUp(self):
        src=(ROOT/'game/systems/room13_v111_relations.rpy').read_text()
        body=re.search(r'(    def r13_v111_daram_where\(\):.*?\n)(?=    \S)',src,re.S).group(1)
        self.values={};self.store=SimpleNamespace(room13={'location':'square'})
        self.env=dict(store=self.store,r13_v111_value=lambda k:self.values.get(k))
        exec(textwrap.dedent(body),self.env)
    def where(self):return self.env['r13_v111_daram_where']()
    def test_default_and_twelfth_day_choice(self):
        self.assertEqual(self.where(),'with')
        self.values['DARAM_location']='with_father';self.assertEqual(self.where(),'with')
        self.values['DARAM_location']='school';self.assertEqual(self.where(),'school')
    def test_escort_to_school_overrides_the_older_choice(self):
        self.values.update({'DARAM_location':'with_father','location:daram':'school'})
        self.assertEqual(self.where(),'school')
        self.store.room13['location']='school';self.assertEqual(self.where(),'with')
if __name__=='__main__':unittest.main()
