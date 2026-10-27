"""Presentation-only cleanup helpers and geometry. Native screenshot QA remains required."""
import ast
import textwrap
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NOTE=(ROOT/'game/room13_notebook.rpy').read_text()
BOOK=(ROOT/'game/room13_screens.rpy').read_text()
VIEW=(ROOT/'game/systems/room13_evidence_view.rpy').read_text()
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
  # 2026-10-27 수첩 공통 틀: 하단 버튼 줄은 갈림길과 같은 684 에서 끝나고, 모든 탭의 닫기는
  # systems/room13_notebook_shell.rpy 의 r13_nb_footer_button(0,...) 으로 오른쪽 아래 한 줄에 선다.
  for height in (64,80):
   env=self.env(height=height);y=env['r13_record_footer_y']()
   self.assertEqual(y+env['r13_record_footer_height'](),684)
  self.assertIn('use r13_nb_footer_button(0,"닫기",(close_action or Hide("r13_records")),control_id="r13_nb_close")',NOTE)
  self.assertNotIn('screen r13_reference_record_shell',NOTE)
  self.assertNotIn('screen r13_reference_record_categories',NOTE)
 def test_source_expand_is_one_way_and_scroll_is_retained(self):
  # 0.20.x: the fold lives in systems/room13_evidence_view.rpy (right column of the 자료 view).
  # 0.20.7: one toggle button (출처 펼치기 / 출처 접기) in the same place.
  self.assertIn('("출처 접기" if origin_open else "출처 펼치기")',VIEW)
  self.assertIn('SetLocalVariable("origin_open",not origin_open)',VIEW)
  self.assertIn('yadjustment detail_scroll',VIEW)
  self.assertIn('area (rx,R13_EV_TOP,R13_EV_RIGHT_W+8,max(60,reading_bottom-R13_EV_TOP)) mousewheel True draggable True scrollbars ("vertical" if (detail or present) else None)',VIEW)  # 0.20.6: no empty scrollbar
  self.assertIn('$ reading_bottom=R13_EV_BOTTOM-buttons*bh-max(0,buttons-1)*12-16',VIEW)
 def test_old_relationship_filters_are_neutralized(self):
  self.assertIn('$ rel_filter="all"',NOTE)
  self.assertIn('$ filt="all"',REL)
  self.assertNotIn('selected filt==key',REL)
  self.assertNotIn('살아 있음 %d',REL)
  self.assertIn('xpos R13_NB_LEFT ypos (R13_NB_TOP+44) xsize 588 ysize 436',REL)  # 2026-10-27 수첩 공통 틀 안쪽
 def test_admin_exit_does_not_cover_header_arrows(self):
  self.assertIn('xpos 942 ypos 92 xsize 314 ysize (80 if r13_touch_ui() else 56)',ADMIN)
  self.assertGreaterEqual(92-84,8)
  self.assertIn('action EndReplay(confirm=False)',ADMIN)
  self.assertNotIn('xpos 900 ypos 8',ADMIN)
 def test_filters_moved_out_of_the_grid(self):
  # 0.20.x: the filter chips sit in the top bar (r13_ink_chips), so the grid no longer reserves a row.
  self.assertIn('use r13_ink_chips(r13_ev_filter_chips(',NOTE)
  self.assertIn('use r13_ink_chips(r13_ev_filter_chips(',BOOK)
  self.assertNotIn('screen r13_material_filters(',NOTE)

if __name__=='__main__':unittest.main()
