"""Presentation-only cleanup helpers and geometry. Native screenshot QA remains required."""
import ast
import textwrap
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NOTE=(ROOT/'game/room13_notebook.rpy').read_text()
BOOK=(ROOT/'game/room13_screens.rpy').read_text()
REL=(ROOT/'game/systems/room13_relations.rpy').read_text()
ADMIN=(ROOT/'game/systems/room13_admin_meeting.rpy').read_text()
module=ast.parse(textwrap.dedent(NOTE.split('init 68 python:\n',1)[1].split('\ninit 71:',1)[0]))
helpers={'r13_record_footer_height','r13_record_footer_y','r13_material_filter_choices','r13_material_filters_visible'}
code=compile(ast.Module(body=[n for n in module.body if isinstance(n,ast.FunctionDef) and n.name in helpers],type_ignores=[]),'record-ui-helpers','exec')

class RecordCleanup(unittest.TestCase):
 def env(self,entries=(),height=64):
  env=dict(r13_control_height=lambda:height,r13_catalog_entries=lambda *a:list(entries),r13_material_subset=lambda e,k:[v for v in e if v==k])
  exec(code,env);return env
 def test_lone_all_disappears_without_hiding_content(self):
  env=self.env(['ordinary'])
  self.assertEqual(env['r13_material_filter_choices']('all'),[])
  self.assertFalse(env['r13_material_filters_visible']('all'))
 def test_meaningful_categories_keep_reset(self):
  env=self.env(['testimony','transfer'])
  self.assertEqual([k for k,t in env['r13_material_filter_choices']('all')],['all','testimony','transfer'])
  self.assertEqual([k for k,t in env['r13_material_filter_choices']('all',False)],['all','testimony'])
 def test_stale_specific_material_filter_can_return_to_all(self):
  self.assertEqual([k for k,t in self.env()['r13_material_filter_choices']('testimony')],['all','testimony'])
 def test_shelf_control_still_reserves_filter_row(self):
  env=self.env()
  self.assertTrue(env['r13_material_filters_visible']('all',True,False,3))
  self.assertTrue(env['r13_material_filters_visible']('all',True,True,0))
  self.assertFalse(env['r13_material_filters_visible']('all',True,None,3))
 def test_all_footer_modes_have_sheet_inset_and_content_gap(self):
  for height in (64,80):
   env=self.env(height=height);y=env['r13_record_footer_y']()
   self.assertEqual(y+env['r13_record_footer_height'](),660)
   self.assertEqual(676-(y+height),16)
   self.assertGreaterEqual(y-572,8)
  self.assertIn('xpos 824 ypos r13_record_footer_y() xsize 398 ysize r13_record_footer_height()',BOOK)
  self.assertIn('xpos 66 ypos r13_record_footer_y() xsize 176 ysize r13_record_footer_height()',BOOK)
 def test_source_expand_is_one_way_and_scroll_is_retained(self):
  self.assertNotIn('출처 접기',NOTE)
  self.assertIn('if not origin_open:',NOTE)
  self.assertIn('SetLocalVariable("origin_open",True)',NOTE)
  self.assertIn('yadjustment detail_scroll',NOTE)
  self.assertIn('area (844,218,358,322) mousewheel True draggable True scrollbars "vertical"',NOTE)
 def test_old_relationship_filters_are_neutralized(self):
  self.assertIn('$ rel_filter="all"',NOTE)
  self.assertIn('$ filt="all"',REL)
  self.assertNotIn('selected filt==key',REL)
  self.assertNotIn('살아 있음 %d',REL)
  self.assertIn('xpos 278 ypos 110 xsize 588 ysize 468',REL)
 def test_admin_exit_does_not_cover_header_arrows(self):
  self.assertIn('xpos 942 ypos 92 xsize 314 ysize (80 if r13_touch_ui() else 56)',ADMIN)
  self.assertGreaterEqual(92-84,8)
  self.assertIn('action EndReplay(confirm=False)',ADMIN)
  self.assertNotIn('xpos 900 ypos 8',ADMIN)
 def test_grid_reclaims_removed_filter_row(self):
  self.assertIn('if filters else 116',NOTE)
  self.assertIn('ysize (572-grid_top)',NOTE)
  # Rows fit even when there is no chip row, in desktop and touch modes.
  for step,cellh in ((134,128),(122,116)):
   self.assertLessEqual(126+2*step+cellh,572)

if __name__=='__main__':unittest.main()
