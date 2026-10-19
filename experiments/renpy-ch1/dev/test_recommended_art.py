import hashlib,json,re,struct,types,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def init_body(path):
 lines=path.read_text().splitlines();start=next(i for i,l in enumerate(lines) if re.match(r'init \d+ python:',l))+1;body=[]
 for line in lines[start:]:
  if line and not line.startswith('    '):break
  body.append(line[4:])
 return '\n'.join(body)
class ArtTests(unittest.TestCase):
 def test_exports_match_artist_hashes_and_native_sizes(self):
  for item in json.loads((R/'docs/art_source_exports.json').read_text()):
   for size in ('64','240'):
    export=item['exports'].get(size)
    if not export:continue
    file=R/'game/assets/recommended-story-icons'/Path(export['file']).name
    if not file.exists():continue
    data=file.read_bytes();self.assertEqual(hashlib.sha256(data).hexdigest(),export['sha256'])
    self.assertEqual(struct.unpack('>II',data[16:24]),(int(size),int(size)))
 def test_every_registry_asset_exists(self):
  s=(R/'game/systems/room13_recommended_evidence_art.rpy').read_text()
  for path in re.findall(r"'((?:assets/)[^']+)'",s):self.assertTrue((R/'game'/path).exists(),path)
  self.assertNotIn("'e2_card_dolmok': 'dolmok'",s)
 def test_pots_never_show_future_swap_before_event_or_after_prevention(self):
  g={'store':types.SimpleNamespace(r13_recommended={})}
  exec(init_body(R/'game/systems/room13_recommended_field.rpy'),g)
  exec(init_body(R/'game/systems/room13_recommended_evidence_art.rpy'),g)
  for state,expected in [({},'original'),({'episodes':{'5':{'event':'contaminated'}}},'swapped'),({'episodes':{'5':{'event':'contaminated'}},'e5_poison_blocked':True},'original')]:
   g['store'].r13_recommended=state
   self.assertIn(expected,g['r13_rec_art_spec']('e5_card_pots')['icon'])
 def test_cloth_comparison_does_not_approve_removal_geometry(self):
  s=(R/'game/systems/room13_recommended_cloth_compare.rpy').read_text()
  self.assertNotIn('r13_rec_piko_contact_art_verified = True',s)
  source=(R/'game/systems/room13_recommended_story.rpy').read_text()
  self.assertIn('if not r13_rec_piko_geometry_ready(r13_recommended):',source)
 def test_renpy_masks_have_complementary_real_alpha(self):
  from PIL import Image, ImageChops
  root=R/'game/assets/recommended-story-icons/cloth-mask-v1'
  masks=[]
  for part in ('parent','fragment'):
   image=Image.open(root/(part+'_mask_rgba.png'))
   self.assertEqual(image.mode,'RGBA')
   alpha=image.getchannel('A');self.assertEqual(set(alpha.getdata()),{0,255})
   self.assertIsNone(ImageChops.difference(alpha,Image.open(root/(part+'_mask.png')).convert('L')).getbbox())
   masks.append(alpha)
  self.assertIsNone(ImageChops.difference(masks[0],ImageChops.invert(masks[1])).getbbox())
  source=(R/'game/systems/room13_recommended_cloth_compare.rpy').read_text()
  self.assertIn('%s_mask_rgba.png',source)
  self.assertNotIn('%s_mask.png',source)
 def test_loan_reconstruction_uses_same_source_and_torn_mask(self):
  text=(R/'game/systems/room13_recommended_story.rpy').read_text()
  self.assertIn('Crop(R13_REC_CLOTH_SOURCE_RECT,R13_REC_CLOTH_TEXTURE)',text)
  self.assertIn('add r13_rec_cloth_part("parent")',text)
  self.assertIn('sensitive (as_overlay or after_delivery)',text)
  self.assertNotIn('r13_rec_piko_record_admission',text)
 def test_portrait_recognition_never_invents_approved_face_scar(self):
  text=(R/'dev/recommended_model.py').read_text()
  self.assertNotIn('흉터',text)
  self.assertIn('얼굴 생김새를 설명',text)
 def test_exact_reviewed_contact_panels_installed(self):
  spec=json.loads((R/'docs/piko_contact_interaction_contract.json').read_text())
  for filename,expected in spec['approved_panels'].items():
   if filename=='inner_fitting_section.png':expected=spec['runtime_asset_overrides']['inner_fitting_section']['sha256']
   p=R/'game/assets/recommended-story-icons/piko-native-v4'/filename
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),expected,filename)
 def test_contact_hotspot_is_fixed_at_reviewed_fitting(self):
  spec=json.loads((R/'docs/piko_contact_interaction_contract.json').read_text())
  x,y,w,h=spec['rim_inspection_hitbox_display']
  self.assertEqual((150+584,30+232,54,54),(320+x,140+y,w,h))
  text=(R/'game/systems/room13_recommended_story.rpy').read_text()
  self.assertIn('area (584,232,54,54)',text)
  self.assertIn('frame_index==len(frames)-1 and fitting_seen',text)
 def test_complete_physical_group_delta_has_exact_files(self):
  manifest=json.loads((R/'docs/art_identity_manifest_v2.json').read_text())
  self.assertEqual(manifest['physical_group_count'],16)
  self.assertEqual(len(manifest['coverage']),16)
  self.assertTrue(all(entry['resolved'] for entry in manifest['coverage'].values()))
  for path,expected in manifest['files'].items():
   self.assertEqual(hashlib.sha256((R/path).read_bytes()).hexdigest(),expected,path)
  ns={'store':types.SimpleNamespace(r13_recommended={})}
  exec(init_body(R/'game/systems/room13_recommended_field.rpy'),ns)
  exec(init_body(R/'game/systems/room13_recommended_evidence_art.rpy'),ns)
  exec(init_body(R/'game/systems/room13_recommended_evidence_art_v2.rpy'),ns)
  self.assertIn('piko_portrait_reuse',ns['r13_rec_art_spec']('piko_portrait')['icon'])
  self.assertIn('empty_before',ns['r13_rec_art_spec']('empty_heat')['examination'])
  self.assertIn('empty_after',ns['r13_rec_art_spec']('pedestal')['examination'])
