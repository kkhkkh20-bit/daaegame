"""Resource bindings cannot silently survive a changed story or change game state."""
import copy
import hashlib
import json
import textwrap
import types
import unittest
from pathlib import Path
from PIL import Image
from import_resource_intake21 import reviewed_bindings, BATCH
ROOT=Path(__file__).resolve().parents[1]

class ResourceIntake(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=json.loads((ROOT/'game/assets/room13-dialogue-context-art.json').read_text())
  cls.receipt=json.loads((ROOT/'docs/reviews'/BATCH/'receipt.json').read_text())
 def test_exact_existing_packets(self):
  actual=[c for c in self.data['bindings'] if c.get('batch')==BATCH]
  self.assertEqual(actual,reviewed_bindings())
  self.assertEqual(len(actual),16)
  records=json.loads((ROOT/'game/v111/records.json').read_text())['records']
  for cue in actual:
   if 'line_id' in cue:
    r=records[cue['line_id']]
    self.assertEqual(r['speaker'],'다람' if cue['person']=='daram' else '우박')
    self.assertIn(r['direction']['slot'] or 'neutral',{'neutral','joy','anxious','angry','surprise','flustered'})
 def test_common_daram_scale_and_neutral_foot_canvas(self):
  base=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people']
  rows=self.receipt['profiles'];self.assertEqual(len(rows),48)
  for height in ('560','760','840'):
   daram=[r for r in rows if r['person']=='daram' and r['height']==height]
   self.assertEqual(len(daram),10)
   self.assertEqual(len({r['scale'] for r in daram}),1)
   self.assertEqual(len({tuple(r['image_size']) for r in daram}),1)
   self.assertLess(next(r for r in daram if 'reproach' in r['slot'])['visible_box'][3]-next(r for r in daram if 'reproach' in r['slot'])['visible_box'][1],next(r for r in daram if 'bravado' in r['slot'])['visible_box'][3]-next(r for r in daram if 'bravado' in r['slot'])['visible_box'][1])
  for row in rows:
   p=base[row['person']]['profiles'][row['height']];f=p['frames']['neutral']
   with Image.open(ROOT/'game'/f['file']) as im:bb=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox()
   self.assertEqual(row['foot'],f['offset'][1]+bb[3])
   self.assertEqual(row['canvas'],p['canvas'])
   profile=self.data['entries'][row['person']+':'+row['slot']]['profiles'][row['height']]
   path=ROOT/'game'/profile['frames'][row['slot']]['file']
   self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),row['output_sha256'])
 def test_context_application_does_not_touch_story_state(self):
  source=(ROOT/'game/systems/room13_dialogue_context_art.rpy').read_text().split('init 172 python:\n',1)[1]
  source=source[source.index('    def r13_dialogue_context_match'):]
  state=types.SimpleNamespace(room13={'time':3,'evidence':['x'],'v111':{'piko_alive':False}},r13_meeting_active=False,r13_thought_active=False,r13_dialogue_beat=None)
  def begin(*args):state.r13_dialogue_beat=None
  env=dict(store=state,R13_DIALOGUE_CONTEXT_ART=self.data,R13_FULLBODY_PLAIN={'neutral','joy','anxious','angry','surprise','flustered'},r13_dialogue_beat_begin=begin,r13_dialogue_beat_art=lambda *a:None,renpy=types.SimpleNamespace(loadable=lambda p:(ROOT/'game'/p).is_file()))
  exec(textwrap.dedent(source),env);before=copy.deepcopy(state.room13)
  for c in self.data['bindings']:
   args=(c['identity'],c['index'],(c['person'],c['text']))
   env['r13_dialogue_beat_begin'](*args,'neutral')
   self.assertEqual(state.r13_dialogue_beat['context_key'],c['key'])
   self.assertTrue(state.r13_dialogue_beat['settled'])
   env['r13_dialogue_beat_begin'](*args,'hold_storybook')
   self.assertIsNone(state.r13_dialogue_beat)
   state.r13_meeting_active=True;env['r13_dialogue_beat_begin'](*args,'neutral');self.assertIsNone(state.r13_dialogue_beat);state.r13_meeting_active=False
  self.assertEqual(state.room13,before)
 def test_later_daram_poses_do_not_block_the_opening(self):
  from build_web import startup_media
  data=self.data['entries']
  for cue in self.data['bindings']:
   if cue.get('batch')!=BATCH or cue['person']!='daram':continue
   for profile in data[cue['key']]['profiles'].values():
    path=profile['frames'][cue['slot']]['file']
    self.assertEqual(startup_media(path,set()),cue['slot']=='intake21_01_bravado',path)
 def test_held_icons_are_not_registered(self):
  records=json.loads((ROOT/'game/v111/records.json').read_text())['records']
  for asset in self.receipt['held_icons']['assets']:
   for evidence in asset['evidence']:
    self.assertIn(evidence['line_id'],records)
   self.assertNotIn(asset['asset_id'],json.dumps(self.data))
if __name__=='__main__':unittest.main()
