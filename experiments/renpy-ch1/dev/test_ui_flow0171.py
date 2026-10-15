"""Footer skip modes (the automatic name markup was retired in 0.18.24: dev/test_typography_roles.py)."""
import re,textwrap,types,unittest
from pathlib import Path
class UIFlowTests(unittest.TestCase):
 def setUp(self):
  self.state=dict(location='inn',evidence=['E01'],records={},encounters=[])
  self.store=types.SimpleNamespace(room13=self.state,room13_mode=True,r13_thought_active=False,r13_packet=('karo',''),r13_fast_read=False,r13_fast_all=False,r13_read_id='new')
  self.persistent=types.SimpleNamespace(room13_read=['read'])
  renpy=types.SimpleNamespace(notify=lambda m:None,stop_skipping=lambda:None,restart_interaction=lambda:None,config=types.SimpleNamespace(skipping=None))
  self.env=dict(store=self.store,CAST={'karo':{}},R13_NAMES={'karo':'까로','bami':'밤이'},R13_PLACES={'inn':('여관',),'secret':('숨은 통로',)},ROOM13={'evidence':{'E01':{'name':'초대 편지'},'E99':{'name':'비밀 문서'}}},R13_RECORD_SHORT={'E01':'초대 편지'},r13_met_people=lambda:[],persistent=self.persistent,renpy=renpy)
  source=(Path(__file__).resolve().parents[1]/'game/room13_ui_flow.rpy').read_text().split('init 99 python:\n')[1].split('    config.interact_callbacks')[0]
  exec(textwrap.dedent(source),self.env)
 def test_skip_only_read_key(self):
  self.env['r13_toggle_read_skip']();self.assertIsNone(self.env['renpy'].config.skipping)
  self.store.r13_read_id='read';self.store.r13_fast_read=False;self.env['r13_toggle_read_skip']();self.assertEqual(self.env['renpy'].config.skipping,'slow')
 def test_fast_all_and_end(self):
  self.env['r13_toggle_fast_all']();self.assertTrue(self.store.r13_fast_all);self.assertEqual(self.env['renpy'].config.skipping,'slow')
  self.env['r13_end_skip_modes']();self.assertFalse(self.store.r13_fast_all or self.store.r13_fast_read)
if __name__=='__main__':unittest.main()
