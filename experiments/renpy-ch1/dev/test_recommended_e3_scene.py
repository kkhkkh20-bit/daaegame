import hashlib,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class ActualSceneTests(unittest.TestCase):
 def test_source_hash_and_single_transform(self):
  contract=json.loads((R/'docs/e3_coordinate_interaction_contract.json').read_text())
  art=R/'game/assets/recommended-story-icons/fire_lmw_night_geometry_v3.png'
  self.assertEqual(hashlib.sha256(art.read_bytes()).hexdigest(),contract['night_source_sha256'])
  s=(R/'game/systems/room13_recommended_ep23.rpy').read_text()
  self.assertIn('R13_REC_E3_CROP = (80,150,1500,650)',s)
  self.assertIn('xysize=(1140,494)',s)
  self.assertIn('focus_mask True',s)
  self.assertNotIn('r13_rec_e3_geometry_art_verified = True',s)
 def test_m_anchor_is_on_overlap_and_not_stone_pillar(self):
  c=json.loads((R/'docs/e3_coordinate_interaction_contract.json').read_text())
  m=c['candidate_native_anchors']['M']
  self.assertGreater(m[0]-18,c['reviewed_geometry']['pillar_max_x'])
  scale=.76
  screen=(70+(m[0]-80)*scale,116+(m[1]-150)*scale)
  self.assertEqual(tuple(round(v/2)*2 for v in screen),(656,428))
  self.assertAlmostEqual(80+(screen[0]-70)/scale,m[0])
  self.assertAlmostEqual(150+(screen[1]-116)/scale,m[1])
 def test_cancel_and_answers_preserve_existing_semantic_values(self):
  s=(R/'game/systems/room13_recommended_ep23.rpy').read_text()
  for value in ('L-M','M-W','overlap','outside','unknown'):
   self.assertIn("Return('%s')"%value,s)
  self.assertIn("key 'game_menu' action Return(None)",s)
