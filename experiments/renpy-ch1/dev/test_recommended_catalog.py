import unittest
from pathlib import Path
G={}
for name in ('recommended_model.py','recommended_opening_model.py','recommended_ep23_model.py','recommended_ep456_model.py'):
 exec((Path(__file__).parent/name).read_text(),G)
class CatalogTests(unittest.TestCase):
 def test_every_fact_has_exactly_one_identity(self):
  keys=[k for _,_,ks in G['r13_rec_identity_groups'].values() for k in ks]
  self.assertEqual(len(keys),len(set(keys)))
  self.assertEqual(set(keys),set(G['r13_rec_cards']))
 def test_person_profile_accumulates_without_duplicate_people(self):
  s=G['r13_rec_new_state']();s['facts']=['e4_card_nabi7','e4_card_nabi9','e6_card_nabi']
  for folder in (4,6):
   rows=G['r13_rec_catalog_entries'](s,folder,'person')
   self.assertEqual([x[0] for x in rows],['nabi'])
   self.assertEqual(len(rows[0][2]),3)
 def test_reused_lamp_keeps_identity_and_observations(self):
  s=G['r13_rec_new_state']();s['facts']=['empty_heat','pedestal']
  rows=G['r13_rec_catalog_entries'](s,1,'material')
  self.assertEqual([x[0] for x in rows],['lamp'])
  self.assertEqual(len(rows[0][2]),2)
 def test_only_acquired_facts_but_not_only_correct_answers(self):
  s=G['r13_rec_new_state']();s['facts']=['e5_card_bori','e3_card_bori','e5_card_teacher']
  rows=G['r13_rec_catalog_entries'](s,5,'person')
  self.assertEqual({r[0] for r in rows},{'bori','teacher'})
  self.assertEqual(G['r13_rec_identity_facts'](s,'bori'),['e3_card_bori','e5_card_bori'])
