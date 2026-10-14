"""Display-only knowledge markup must never expose unowned evidence or identities."""
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
 def test_current_knowledge_only_and_particles(self):
  text='까로에게 초대 편지를 보여주자. 여관에서 밤이와 비밀 문서를 찾자.'
  out=self.env['r13_semantic_text'](text)
  self.assertEqual(out.count('{b}'),3)
  self.assertIn('밤이와 비밀 문서',out)
  self.assertEqual(re.sub(r'\{[^}]*\}','',out),text)
 def test_no_partial_names_or_nested_tags(self):
  text='까로네 여관방 {color=#fff}까로{/color} [까로] 초대 편지함'
  self.assertEqual(self.env['r13_semantic_text'](text),text)
 def test_single_syllable_person_has_word_boundary(self):
  self.env['R13_NAMES']['karo']='톡'
  out=self.env['r13_semantic_text']('톡에게 말해. 톡톡 톡방')
  self.assertEqual(out.count('{b}'),1)
  self.assertIn('톡톡 톡방',out)
 def test_existing_markup_is_idempotent(self):
  fn=self.env['r13_semantic_text'];self.assertEqual(fn(fn('까로와 여관')),fn('까로와 여관'))
 def test_thought_blue_is_preserved(self):
  self.store.r13_thought_active=True;self.assertEqual(self.env['r13_semantic_text']('까로와 여관'),'까로와 여관')
 def test_skip_only_read_key(self):
  self.env['r13_toggle_read_skip']();self.assertIsNone(self.env['renpy'].config.skipping)
  self.store.r13_read_id='read';self.store.r13_fast_read=False;self.env['r13_toggle_read_skip']();self.assertEqual(self.env['renpy'].config.skipping,'slow')
 def test_fast_all_and_end(self):
  self.env['r13_toggle_fast_all']();self.assertTrue(self.store.r13_fast_all);self.assertEqual(self.env['renpy'].config.skipping,'slow')
  self.env['r13_end_skip_modes']();self.assertFalse(self.store.r13_fast_all or self.store.r13_fast_read)
 def test_palette_contrast(self):
  def lum(h):
   rgb=[int(h[i:i+2],16)/255 for i in (1,3,5)]
   return sum(w*(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4) for w,x in zip((.2126,.7152,.0722),rgb))
  for color in self.env['R13_SEMANTIC_DARK'].values():self.assertGreater((lum(color)+.05)/(lum('#142237')+.05),7)
if __name__=='__main__':unittest.main()
