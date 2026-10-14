"""Exercise actual pure model, including replay, cancellation and insolvency."""
import copy, json, textwrap, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ns={'winter_copy':copy}
exec(textwrap.dedent((ROOT/'game/systems/room13_livelihood_model.rpy').read_text().split('init 91 python:\n')[1]),ns)
class LivelihoodTest(unittest.TestCase):
 def state(self,**extra):
  return dict(day=2,period=0,flags=['livelihood_open'],**extra)
 def test_daily_budget(self):
  s=self.state();s,r=ns['r13_complete_job'](s,'kitchen','finish');self.assertEqual(r['pay'],6)
  s,r=ns['r13_complete_job'](s,'repair','ask');self.assertEqual(r['pay'],8)
  self.assertEqual(s['period'],2);self.assertFalse(ns['r13_job_allowed'](s,'delivery'))
  s=ns['r13_settle_lodging'](s);self.assertEqual(ns['r13_wallet'](s)['cash'],4);self.assertEqual(ns['r13_wallet'](s)['debt'],0)
 def test_once_and_cancel(self):
  s=self.state();before=copy.deepcopy(s)
  self.assertEqual(ns['r13_complete_job'](s,'delivery','cancel'),(s,None));self.assertEqual(s,before)
  n,r=ns['r13_complete_job'](s,'delivery','finish');self.assertEqual(s,before)
  self.assertFalse(ns['r13_job_allowed'](n,'delivery'))
  self.assertEqual(ns['r13_settle_lodging'](ns['r13_settle_lodging'](n)),ns['r13_settle_lodging'](n))
 def test_insolvent_and_first_night(self):
  s=self.state();n=ns['r13_settle_lodging'](s);self.assertEqual(ns['r13_wallet'](n)['debt'],10)
  s['day']=1;n=ns['r13_settle_lodging'](s);self.assertEqual(ns['r13_wallet'](n)['debt'],0)
  self.assertFalse(ns['r13_job_allowed'](s,'delivery'))
 def test_earned_route_and_once_only_bonus(self):
  s=self.state();self.assertIsNone(ns['r13_complete_job'](s,'delivery','combine')[1])
  s,r=ns['r13_complete_job'](s,'delivery','ask');s['day']=3;s['period']=0
  s,r=ns['r13_complete_job'](s,'delivery','combine');self.assertEqual(r['pay'],14)
  s['day']=4;s['period']=0;self.assertIsNone(ns['r13_complete_job'](s,'delivery','combine')[1])
 def test_purchase_and_debt(self):
  s=self.state();self.assertFalse(ns['r13_purchase'](s,'cord')[1])
  s,r=ns['r13_complete_job'](s,'repair','finish');s,ok=ns['r13_purchase'](s,'cord');self.assertTrue(ok)
  self.assertFalse(ns['r13_purchase'](s,'cord')[1]);self.assertEqual(ns['r13_wallet'](s)['cash'],5)
  s=ns['r13_settle_lodging'](s);self.assertEqual(ns['r13_wallet'](s)['debt'],5)
  s['day']=3;s['period']=0;s,r=ns['r13_complete_job'](s,'repair','finish');s=ns['r13_repay'](s)
  self.assertEqual(ns['r13_wallet'](s)['debt'],0);self.assertEqual(ns['r13_wallet'](s)['cash'],3)
 def test_shop_windows_and_debt_limit(self):
  s=self.state(case_state='pending');s['day']=5;s['livelihood']=dict(cash=50)
  self.assertFalse(ns['r13_purchase'](s,'file')[1])      # only after the incident
  s['case_state']='occurred';n,ok=ns['r13_purchase'](s,'file');self.assertTrue(ok)
  s['day']=3;self.assertFalse(ns['r13_purchase'](s,'file')[1])  # not on sale yet
  s['day']=5;s['livelihood']=dict(cash=50,debt=21);self.assertFalse(ns['r13_purchase'](s,'snack')[1])
  s['livelihood']=dict(cash=50,used=['blanket']);self.assertFalse(ns['r13_purchase'](s,'blanket')[1])
  self.assertNotIn('blueprint',ns['R13_SHOP'])
 def test_save_roundtrip_and_legacy(self):
  s=self.state();s,r=ns['r13_complete_job'](s,'delivery','ask');loaded=json.loads(json.dumps(s))
  self.assertEqual(ns['r13_wallet'](loaded),ns['r13_wallet'](s))
  self.assertEqual(ns['r13_wallet']({})['cash'],0)
  self.assertNotIn('livelihood',{})
class ShopIconTest(unittest.TestCase):
 def test_every_item_has_a_16x16_icon(self):
  src=(ROOT/'game/systems/room13_shop_icons.rpy').read_text().split('init 79 python:\n')[1].split('\n    class ')[0]
  icons={};exec(textwrap.dedent(src),icons)
  for key in ns['R13_SHOP']:
   rows=icons['R13_ITEM_ICONS'][key];self.assertEqual(len(rows),16,key)
   for row in rows:
    self.assertEqual(len(row),16,key)
    for ch in row:self.assertTrue(ch=='.' or ch in icons['R13_ICON_PALETTE'],(key,ch))
class ItemUseTest(unittest.TestCase):
 def test_item_uses_point_at_real_objects_and_tools_have_icons(self):
  import re
  src=(ROOT/'game/systems/room13_items.rpy').read_text()
  content=json.loads((ROOT/'game/room13-content.json').read_text())
  pairs=re.findall(r'"use_[a-z_]+": \("([a-z0-9]+)","([a-z_]+)"',src)
  self.assertGreaterEqual(len(pairs),6)
  for place,obj in pairs:self.assertIn(obj,content['objects'][place],(place,obj))
  icons=(ROOT/'game/systems/room13_shop_icons.rpy').read_text()
  for tool in ('knife','lantern'):self.assertIn('"%s":['%tool,icons)
  # The passage is only revealed after the soot trail; opening still needs the old puzzle.
  self.assertIn('["own:knife","soot_trail"],flags=["passage_found"]',src)
  self.assertNotIn('passage_open',src)
if __name__=='__main__':unittest.main()
