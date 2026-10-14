"""Option resets must preserve the campaign and persistent discovery records."""
import copy,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Options(unittest.TestCase):
 def setUp(self):
  self.played=[];self.stopped=[];self.notices=[];self.saved=[]
  self.state={'day':7,'period':2,'evidence':['E01'],'flags':['entry_corrected'],'money':25}
  self.p=types.SimpleNamespace(room13_read=['line1'],room13_knowledge=['E01'],room13_endings=['end1'],room13_typing_sound=True,room13_motion=False,room13_large_text=True,room13_text_small=True,room13_large_text_auto=True,room13_window_alpha='f5',r13_save_page=3)
  self.store=types.SimpleNamespace(room13=self.state,r13_fast_read=True)
  self.vol={'music':.1,'sfx':.2};self.mute={'music':True,'sfx':True}
  prefs=types.SimpleNamespace(get_mute=lambda k:self.mute[k],get_volume=lambda k:self.vol[k],set_mute=lambda k,v:self.mute.update({k:v}),set_volume=lambda k,v:self.vol.update({k:v}),text_cps=55,afm_time=3)
  self.small=False
  renpy=types.SimpleNamespace(music=types.SimpleNamespace(stop=lambda **k:self.stopped.append(k),play=lambda *a,**k:self.played.append((a,k))),save_persistent=lambda:self.saved.append(True),restart_interaction=lambda:None,notify=self.notices.append,stop_skipping=lambda:None,variant=lambda k:self.small)
  self.env=dict(persistent=self.p,store=self.store,preferences=prefs,config=types.SimpleNamespace(default_music_volume=.75,default_sfx_volume=.7,default_text_cps=34),renpy=renpy)
  exec(textwrap.dedent((ROOT/'game/room13_options.rpy').read_text().split('init 70 python:\n')[1]),self.env)
 def test_typing_off_stops_only_typing(self):
  self.env['r13_set_option']('room13_typing_sound',False)
  self.assertEqual(self.stopped,[{'channel':'typing'}]);self.assertFalse(self.p.room13_typing_sound);self.assertEqual(self.vol,{'music':.1,'sfx':.2})
 def test_typing_tick_disable_does_not_queue_old_glyphs(self):
  text=types.SimpleNamespace(slow=True,r13_revealed=5,r13_audio_seen=0)
  self.store.typing_allowed=True
  self.env['renpy'].get_screen=lambda name:name=='say'
  self.env['renpy'].get_displayable=lambda *args:text
  self.env['renpy'].is_skipping=lambda:False
  body=(ROOT/'game/room13_dialogue_rhythm.rpy').read_text().split('    def r13_typing_tick():',1)[1]
  exec('def r13_typing_tick():\n'+textwrap.indent(textwrap.dedent(body).lstrip('\n'),'    '),self.env)
  self.p.room13_typing_sound=False;self.env['r13_typing_tick']()
  self.assertEqual(text.r13_audio_seen,5);self.assertFalse(self.played)
  self.p.room13_typing_sound=True;self.env['r13_typing_tick']();self.assertFalse(self.played)
  text.r13_revealed=6;self.env['r13_typing_tick']();self.assertEqual(len(self.played),1)
 def test_invalid_option_cannot_write_campaign_or_discovery(self):
  before=copy.deepcopy(vars(self.p));self.env['r13_set_option']('room13_read',[]);self.assertEqual(vars(self.p),before)
 def test_reset_preserves_progress_history_and_save_page(self):
  state=copy.deepcopy(self.state)
  self.env['r13_reset_options']()
  self.assertEqual(self.state,state);self.assertEqual(self.p.room13_read,['line1']);self.assertEqual(self.p.room13_knowledge,['E01']);self.assertEqual(self.p.room13_endings,['end1']);self.assertEqual(self.p.r13_save_page,3)
  self.assertEqual(self.vol,{'music':.75,'sfx':.7});self.assertEqual(self.mute,{'music':False,'sfx':False});self.assertEqual(self.env['preferences'].text_cps,34);self.assertFalse(self.p.room13_large_text);self.assertFalse(self.store.r13_fast_read)
 def test_reset_retains_large_text_on_small_device(self):
  self.small=True;self.env['r13_reset_options']();self.assertTrue(self.p.room13_large_text)
 def test_test_sound_respects_mute_and_zero_and_plays_once(self):
  self.env['r13_test_option_sound']();self.assertFalse(self.played);self.assertTrue(self.notices)
  self.mute['sfx']=False;self.vol['sfx']=0;self.env['r13_test_option_sound']();self.assertFalse(self.played)
  self.vol['sfx']=.7;self.env['r13_test_option_sound']();self.assertEqual(len(self.played),1);self.assertEqual(self.played[0][1]['channel'],'sound')
if __name__=='__main__':unittest.main()
