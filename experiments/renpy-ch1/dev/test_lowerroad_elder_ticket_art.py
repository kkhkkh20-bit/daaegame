"""Dedicated actor art must not change the borrowed elder or evidence identity."""
import copy,json,textwrap,unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]

class ElderTicketArt(unittest.TestCase):
 def test_dedicated_rows_leave_shared_elder_untouched(self):
  elder=json.loads((ROOT/'game/assets/room13-fullbody-dialogue.json').read_text())['people']['elder']
  cast=json.loads((ROOT/'game/assets/cast.json').read_text())['elder']
  saved_body=copy.deepcopy(elder);saved_cast=copy.deepcopy(cast)
  env=dict(R13_FULLBODY={'people':{'elder':elder,'v111_lowerroad_elder':elder}},CAST={'elder':cast,'v111_lowerroad_elder':cast},R13_FULLBODY_FILES=set(),R13_BDIALOGUE_FACES={})
  source=(ROOT/'game/systems/room13_lowerroad_elder_art.rpy').read_text().split('init 172 python:\n',1)[1]
  exec(textwrap.dedent(source),env)
  self.assertEqual(elder,saved_body);self.assertEqual(cast,saved_cast)
  actor=env['R13_FULLBODY']['people']['v111_lowerroad_elder']
  self.assertIsNot(actor,elder);self.assertEqual(set(actor['images']),{'neutral'})
  self.assertEqual(set(env['CAST']['v111_lowerroad_elder']),set(cast))
  self.assertTrue(all(row['file'].startswith('assets/lowerroad-elder/') for row in env['CAST']['v111_lowerroad_elder'].values()))
  self.assertEqual(env['R13_BDIALOGUE_FACES']['v111_lowerroad_elder'],{'neutral':env['R13_LOWERROAD_ELDER_FACE']})
  self.assertIn(actor['images']['neutral']['file'],env['R13_FULLBODY_FILES'])

 def test_elder_original_rgba_and_ticket_runtime_bytes_preserved(self):
  source=REPO/'design/resource-intake-20261025/batch-02'
  for part in ('fullbody','face'):
   with Image.open(source/'2'/('v111_lowerroad_elder_%s_candidate.png'%part)) as png, Image.open(ROOT/'game/assets/lowerroad-elder'/('v111_lowerroad_elder_%s.webp'%part)) as webp:
    self.assertEqual(png.convert('RGBA').tobytes(),webp.convert('RGBA').tobytes())
  self.assertEqual((ROOT/'game/assets/evidence/NW_NUBI_TICKET.webp').read_bytes(),(source/'6/grand-win-evidence-v1/webp/NW_NUBI_TICKET.webp').read_bytes())
  self.assertTrue((ROOT/'art/batch02-elder-ticket-20261025/NW_NUBI_TICKET-before.webp').is_file())
  self.assertFalse((ROOT/'game/assets/evidence/REWARD_DOLMOK_VOID_MARK.webp').exists())
