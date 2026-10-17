"""Consequences must agree across independent outcome axes, including old/mixed saves."""
import copy,itertools,json,textwrap,unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'game/assets/room13-episode-aftermath.json').read_text())['frames']
SRC=(ROOT/'game/systems/room13_episode_aftermath.rpy').read_text()
ENV={'R13_AFTERMATH':DATA}
exec(textwrap.dedent('    def r13_episode_aftermath_frames'+SRC.split('    def r13_episode_aftermath_frames',1)[1].split('    def r13_aftermath_actor',1)[0]),ENV)
def select(ep,*flags,child='with_dad'):
 return ENV['r13_episode_aftermath_frames'](ep,dict(flags=list(flags),daram_state=child))
def ids(frames):return [f['id'] for f in frames]
def people(frames):return set(p for f in frames for p in f['subjects'])
class EpisodeAftermath(unittest.TestCase):
 def test_ep1_verdict_and_artist_are_independent(self):
  for dead,detained in itertools.product((False,True),repeat=2):
   f=select('ep1',*(['piko_dead'] if dead else []),*(['tok_detained'] if detained else []))
   self.assertEqual(ids(f),['piko_dead' if dead else 'piko_saved','tok_detained' if detained else 'tok_free'])
  self.assertIn('siluk_debt',ids(select('ep1','siluk_debt_cleared','madam_store_opened')))
  both=ids(select('ep1','siluk_handed','madam_store_opened'));self.assertIn('siluk_handed',both);self.assertIn('madam_open',both)
 def test_river_and_clinic_do_not_resurrect_musoe(self):
  self.assertIn('musoe_clinic',ids(select('ep2','kd_seori')))
  f=select('ep2','kd_seori','musoe_gone');self.assertNotIn('resident_musoe',people(f));self.assertIn('clinic_empty',ids(f))
  self.assertEqual(ids(select('ep2_clinic','musoe_gone')),['clinic_empty'])
  self.assertNotIn('bami',people(select('ep2','bami_taken','bami_safe','kd_shoes_only')))
  self.assertIn('somi_silent',ids(select('ep2','kd_named','kd_shoes_only')))
 def test_fire_loss_and_care_are_distinct(self):
  f=select('ep3','kkomi_dead','bori_adopts');self.assertNotIn('kid_kkomi',people(f));self.assertIn('bori_adopts',ids(f))
  f=select('ep3','wf_missed','bori_taken');self.assertEqual(ids(f),['shed_empty','bori_taken'])
  f=select('ep3','bori_taken','bori_adopts','kkomi_dead');self.assertNotIn('resident_bori',people(f))
  f=select('ep3','kkomi_dead',child='held');self.assertNotIn('daram',people(f))
 def test_night_deaths_override_previous_saves(self):
  f=select('ep4','chorong_dead','nt_chorong_safe','ttadak_dead','nt_ttadak_safe','owl_hat',child='held')
  self.assertEqual(ids(f),['chorong_dead','ttadak_dead']);self.assertNotIn('resident_lamplighter',people(f));self.assertNotIn('resident_ttadak',people(f))
  self.assertEqual(ids(select('ep4','nt_ttadak_safe')),['ttadak_safe'])
  self.assertEqual(ids(select('ep4','nt_ttadak_half')),['ttadak_hurt'])
 def test_soup_counts_and_portrait_presence(self):
  f=select('ep5','soup_kids_dead','ws_kids_alive','bori_adopts');self.assertEqual(ids(f),['soup_empty','bori_shoe']);self.assertFalse(any(p.startswith('kid_') for p in people(f)))
  f=select('ep5','ws_some_alive');self.assertEqual(len([p for p in people(f) if p.startswith('kid_')]),3);self.assertNotIn('kid_dodam',people(f))
  self.assertEqual(ids(select('ep5','ws_kids_alive','dodam_sick')),['dodam_sick'])
  self.assertIn('mom_portrait',ids(select('ep5','ws_kids_alive','mom_reunited','portrait_finished_by_daram')))
  for flag in ('mom_reunited','portrait_finished_by_daram'):
   self.assertNotIn('mom_portrait',ids(select('ep5',flag)))
  self.assertNotIn('mom_portrait',ids(select('ep5','mom_reunited','portrait_finished_by_daram',child='held')))
 def test_cart_stopping_does_not_erase_badook_death(self):
  f=select('ep6','cart_stopped','badook_dead','cv_badook_safe');self.assertEqual(ids(f),['guldol_free','badook_dead']);self.assertNotIn('resident_badook',people(f))
  self.assertEqual(ids(select('ep6','cart_stopped','badook_hurt')),['guldol_free','badook_hurt'])
  self.assertEqual(ids(select('ep6','cart_stopped','cv_badook_safe')),['cart_safe'])
  self.assertEqual(ids(select('ep6','cart_stopped','neoul_gone')),['cart_unrest'])
  f=select('ep6','cv_family_only','cart_left','ws_cart_truth','guldol_dead','momo_dead');self.assertNotIn('resident_guldol',people(f));self.assertIn('pandol_family',ids(f))
  self.assertNotIn('pandol_family',ids(select('ep6','cv_family_only','ws_cart_truth','pandol_dead')))
  self.assertEqual(ids(select('ep6','cv_skipped','cart_left')),['cart_skipped'])
 def test_selection_is_read_only_and_all_frames_are_reachable(self):
  fixtures=[('ep1',[]),('ep1',['piko_dead','tok_detained','siluk_handed','madam_store_opened']),('ep1',['siluk_debt_cleared']),('ep2',['kd_shoes_only','bami_taken','kd_named']),('ep2',['kd_farewell_seen','bami_safe']),('ep2',['kd_seori']),('ep2_clinic',[]),('ep3',[]),('ep3',['kkomi_dead','bori_adopts','nubi_kids_with_nabi']),('ep3',['wf_missed','bori_taken']),('ep4',['chorong_dead','ttadak_dead','nt_ttadak_proven','owl_hat']),('ep4',['nt_chorong_safe','nt_ttadak_half']),('ep4',['nt_ttadak_safe']),('ep4',['nt_chorong_half']),('ep5',['soup_kids_dead']),('ep5',['ws_some_alive']),('ep5',['ws_kids_alive','bori_adopts','mom_reunited','portrait_finished_by_daram']),('ep5',['ws_kids_alive','dodam_sick']),('ep6',['cart_stopped','cv_badook_safe','cv_granny_tomorrow']),('ep6',['cart_left','badook_dead']),('ep6',['cart_stopped','badook_hurt']),('ep6',['cart_stopped','neoul_gone']),('ep6',['cv_family_only','cart_left','ws_cart_truth']),('ep6',['cv_skipped','cart_left'])]
  seen=set();original=copy.deepcopy(DATA)
  for child in ('with_dad','held','rescued'):
   for ep,flags in fixtures:
    state=dict(flags=flags[:],daram_state=child,day=7,period=2,evidence=['E01']);before=copy.deepcopy(state)
    frames=ENV['r13_episode_aftermath_frames'](ep,state);seen.update(ids(frames));self.assertEqual(state,before)
    if child=='held':self.assertNotIn('daram',people(frames))
  self.assertEqual(DATA,original);self.assertEqual(seen,set(DATA))
 def test_art_bounds_approved_faces_and_caption_lengths(self):
  approved=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people']
  for key,f in DATA.items():
   self.assertLessEqual(len(f['caption']),98,key);self.assertNotIn('dad',f['subjects'])
   for a in f.get('actors',[]):
    self.assertIn(a['person'],approved,key)
    p=approved[a['person']]['profiles']['760'];self.assertTrue((ROOT/'game'/p['frames']['neutral']['file']).exists())
   if 'file' in f:
    with Image.open(ROOT/'game'/f['file']) as im:
     if 'rect' in f:
      x,y,w,h=f['rect'];self.assertGreater(w,0);self.assertGreater(h,0);self.assertAlmostEqual(w/h,16/9,delta=.025);self.assertGreaterEqual(x,0);self.assertGreaterEqual(y,0);self.assertLessEqual(x+w,im.width);self.assertLessEqual(y+h,im.height)
 def test_all_authored_exit_paths_are_hooked(self):
  targets={'room13_ep1_lamp_thief.rpy':2,'room13_ep2_kids.rpy':2,'room13_ep3_woodfire.rpy':2,'room13_ep4_night13.rpy':1,'room13_ep5_soup.rpy':1,'room13_ep6_cart.rpy':2}
  for file,count in targets.items():self.assertEqual((ROOT/'game/systems'/file).read_text().count('call r13_episode_aftermath('),count,file)
if __name__=='__main__':unittest.main()
