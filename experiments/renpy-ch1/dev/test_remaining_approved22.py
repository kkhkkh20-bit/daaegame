import hashlib,json,unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class RemainingApproved22(unittest.TestCase):
 def test_all_originals_and_derivatives_are_present(self):
  receipt=json.loads((ROOT/'art/approved-remaining22/receipt.json').read_text());self.assertEqual(receipt['verified_count'],22)
  for r in receipt['rows']:
   p=ROOT/r['source'];self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),r['source_sha256'])
   with Image.open(p) as im:self.assertEqual(list(im.size),r['source_size'])
  data=json.loads((ROOT/'game/assets/room13-dialogue-pose-source-art.json').read_text());poses=[(who,key,e) for who,row in data['people'].items() for key,e in row['pose_profiles'].items()];self.assertEqual(sum(e['profiles']['840']['frames']['neutral']['source_master'].startswith('art/approved-remaining22/') for _,_,e in poses),15)
  for who,key,e in poses:
   for height,p in e['profiles'].items():
    f=p['frames']['neutral'];self.assertTrue((ROOT/'game'/f['file']).is_file());self.assertIn('/'+who+'/'+key+'/',f['file']);self.assertEqual(f['source_sha256'],e['source_sha256'])
  self.assertLess(data['people']['kid_saemi']['pose_profiles']['hide_bowl']['visible_height_at_840'],data['people']['kid_dodam']['pose_profiles']['lick_ladle']['visible_height_at_840'])
  self.assertLess(data['people']['resident_teacher']['pose_profiles']['collapse_attendance']['visible_height_at_840'],data['people']['resident_teacher']['pose_profiles']['write_attendance']['visible_height_at_840'])
 def test_solbang_canonical_identity_in_every_live_registry(self):
  for name in ('cast.json','room13-pixel-acting.json','room13-portraits.json'):
   row=json.loads((ROOT/'game/assets'/name).read_text())['resident_solbang']
   for e in row.values():self.assertTrue(e['file'].startswith(('assets/solbang-chinchilla-','assets/profile-source-master/resident_solbang')),e['file'])
  talk=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people']['resident_solbang'];r=json.loads((ROOT/'art/approved-remaining22/receipt.json').read_text());sources={x['pose']:x['source_sha256'] for x in r['rows'] if x['person']=='resident_solbang'}
  for p in talk['profiles'].values():
   self.assertEqual(set(p['frames']),set(sources)-{'work_herb_bundle'})
   for key,f in p['frames'].items():self.assertEqual(f['source_sha256'],sources[key])
  icon=json.loads((ROOT/'game/assets/room13-profile-source-art.json').read_text())['people']['resident_solbang'];self.assertEqual(icon['crop'],[220,60,540,540]);self.assertEqual(icon['source_sha256'],sources['neutral'])

class StorybookVisibility(unittest.TestCase):
 def test_tosil_pose_closes_only_previous_book_overlay(self):
  import ast,textwrap,types
  source=(ROOT/'game/systems/room13_ep_art.rpy').read_text();start=source.index('    def r13_ep_line_art(packet):');end=source.index('    def r13_ep_line_art_clear',start);code=textwrap.dedent(source[start:end]);calls=[]
  env=dict(renpy=types.SimpleNamespace(hide=lambda tag:calls.append(('hide',tag)),show=lambda tag,**kw:calls.append(('show',tag))),At=lambda *a:a,r13_ep_book_art=lambda x:x,r13_ep_art_fade=None)
  exec(code,env);f=env['r13_ep_line_art'];f(('resident_tosil','unchanged line',{'pose':'hold_storybook'}));self.assertEqual(calls,[('hide','r13_ep_book')]);calls.clear();f((None,'ending',{'book':'U07-ending'}));self.assertEqual(calls,[('show','r13_ep_book')])

if __name__=='__main__':unittest.main()
