"""Notebook UI memories must be isolated from case state and other recipients."""
import copy,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ReviewContext(unittest.TestCase):
 def setUp(self):
  self.store=types.SimpleNamespace(room13={'evidence':['E01'],'day':4},r13_book_views={},r13_meeting_claim='C2',r13_debate_selected='s2')
  source=(ROOT/'game/room13_notebook.rpy').read_text().split('    def r13_book_context',1)[1].split('    def r13_record_category',1)[0]
  self.env=dict(store=self.store);exec(textwrap.dedent('    def r13_book_context'+source),self.env)
 def test_reopen_retains_selection_without_touching_case_or_other_person(self):
  before=copy.deepcopy(self.store.room13)
  context=self.env['r13_book_context'];remember=self.env['r13_book_remember']
  remember(context('buri',False),'E01',2)
  remember(context('granny',False),'E06',0)
  self.assertEqual(self.store.r13_book_views[context('buri',False)],dict(detail='E01',page=2))
  self.assertEqual(self.store.room13,before)
 def test_hearing_memory_is_per_claim_and_statement_not_fake_target(self):
  context=self.env['r13_book_context'];a=context('resident_seori',True)
  self.assertEqual(a,context('granny',True))
  self.store.r13_debate_selected='s3';self.assertNotEqual(a,context('resident_seori',True))
  self.store.r13_debate_selected='s2';self.store.r13_meeting_claim='F1';self.assertNotEqual(a,context('resident_seori',True))
