import hashlib,json,textwrap,types,unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class ProfileIcons(unittest.TestCase):
 def test_exact_scope_provenance_and_uniform_padding(self):
  data=json.loads((ROOT/'game/assets/room13-profile-source-art.json').read_text())['people'];base=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people'];specs={r['character_id']:r for r in json.loads((ROOT/'docs/reviews/profile-icons/approved-crops.json').read_text())}
  self.assertEqual(set(data),set(base)-{'resident_solbang'});self.assertEqual(len(data),58)
  for who,e in data.items():
   self.assertEqual(e['source_sha256'],specs[who]['source_sha256']);self.assertEqual(e['source_size'],specs[who]['source_size'])
   path=ROOT/'game'/e['file'];self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),e['sha256'])
   with Image.open(path) as im:
    self.assertEqual(im.size,(256,256));box=im.getchannel('A').getbbox();self.assertGreaterEqual(min(box[:2]),12);self.assertLessEqual(max(box[2:]),244)
 def test_missing_mother_stays_hidden(self):
  text=(ROOT/'game/systems/room13_relations.rpy').read_text();body=text.split('    def r13_rel_face(person):',1)[1].split('    def r13_rel_layout',1)[0]
  missing=[True];calls=[]
  env=dict(r13_rel_status=lambda p:('missing' if missing[0] else None,''),Fixed=lambda *a,**k:'hidden',Solid=lambda *a:None,Text=lambda *a,**k:None,r13_ui_font=lambda:'font',r13_art=lambda *args:calls.append(args) or 'face')
  exec('def r13_rel_face(person):\n'+textwrap.indent(textwrap.dedent(body),'    '),env)
  self.assertEqual(env['r13_rel_face']('mom'),'hidden');self.assertEqual(calls,[])
  missing[0]=False;self.assertEqual(env['r13_rel_face']('mom'),'face');self.assertEqual(calls,[('mom','avatar_neutral')])
 def test_profile_registration_never_registers_world_poses(self):
  source=(ROOT/'game/systems/room13_profile_source_art.rpy').read_text();self.assertIn('+" avatar_neutral"',source);self.assertNotIn('R13_ACTING',source);self.assertNotIn('R13_FULLBODY',source)
if __name__=='__main__':unittest.main()
