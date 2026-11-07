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
  self.assertEqual(len(actual),14)
  records=json.loads((ROOT/'game/v111/records.json').read_text())['records']
  for cue in actual:
   if 'line_id' in cue:
    r=records[cue['line_id']]
    self.assertEqual(r['speaker'],'다람' if cue['person']=='daram' else '우박')
    self.assertIn(r['direction']['slot'] or 'neutral',{'neutral','joy','anxious','angry','surprise','flustered'})
 def test_revised_grief_lines_keep_authored_emotion_without_comic_context(self):
  # 실제 개정 대사 층과 문맥 선택기를 함께 통과시켜, 옛 포즈가 다시 덮지 못하게 한다.
  from test_newworld_text import Layer
  env=Layer.load(self)
  for rid,identity,emotion in (
   ('MS14_D01_S03_L0005','v111:gate_read_original:MS14_D01_S03_L0003','angry'),
   ('MS14_D03_S06_L0003','v111:restore3:MS14_D03_S06_L0002','anxious')):
   packet=next(p for p in env['r13_v111_lines']([rid]) if p[2].get('line_id')==rid)
   self.assertEqual(packet[2]['expression'],emotion)
   self.assertIsNone(env['r13_dialogue_context_match'](identity,0,packet,emotion))
  # 울음을 닦는 전용 그림과 갑작스러운 수레 경고는 계속 사용한다.
  for rid,identity,key in (
   ('MS14_D03_S06_L0018','v111:piko_memorial:MS14_D03_S06_L0013','daram:intake21_09_wipe_tears'),
   ('MS14_D03_S04_L0003','v111:silluk3:MS14_D03_S04_L0002','daram:intake21_08_scared_brave')):
   packet=next(p for p in env['r13_v111_lines']([rid]) if p[2].get('line_id')==rid)
   cue=env['r13_dialogue_context_match'](identity,0,packet,packet[2]['expression'])
   self.assertEqual(cue['key'],key)
 def test_fire_survivors_and_witness_keep_tense_expressions(self):
  from test_newworld_text import Layer
  env=Layer.load(self)
  for rid in ('MS14_D06_S04_L0017','MS14_D06_S04_L0033','MS14_D07_S01_L0022'):
   packet=env['r13_v111_line'](rid)
   self.assertEqual(packet[2]['expression'],'anxious')
  added=next(row for section in ('before','after','blocks') for rows in env['R13_NW_TEXT'][section].values() for row in rows if row.get('id')=='NW_MV_D07_03')
  self.assertEqual(env['r13_nw_added_line'](added)[2]['expression'],'anxious')
  import ast,re
  source=(ROOT/'game/room13_v111_days610.rpy').read_text()
  block=source.split('label r13_v111_bori_witness_heard7:',1)[1].split('\nlabel ',1)[0]
  args=re.search(r'call r13_lines\((.*)\)',block).group(1)
  call=ast.parse('f('+args+')',mode='eval').body
  packets=ast.literal_eval(call.args[0]);packet=packets[0]
  self.assertEqual(packet[0],'resident_bori')
  self.assertEqual(packet[2]['expression'],'anxious');self.assertEqual(packet[2]['pose'],'anxious')
 def test_location_refresh_preserves_retired_receipt_rows_and_rejects_text_changes(self):
  import tempfile
  from refresh_intake21_lines import refresh
  from import_resource_intake21 import RETIRED_CONTEXT_LINE_IDS
  receipt=copy.deepcopy(self.receipt)
  retired=[c for c in receipt['bindings'] if c.get('line_id') in RETIRED_CONTEXT_LINE_IDS]
  active=next(c for c in receipt['bindings'] if c.get('line_id') and c['line_id'] not in RETIRED_CONTEXT_LINE_IDS)
  active['source_line']-=12
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'receipt.json';path.write_text(json.dumps(receipt,ensure_ascii=False))
   self.assertEqual(refresh(path,'bindings'),1)
   refreshed=json.loads(path.read_text())
   self.assertEqual([c for c in refreshed['bindings'] if c.get('line_id') in RETIRED_CONTEXT_LINE_IDS],retired)
   active=next(c for c in refreshed['bindings'] if c['key']==active['key'])
   active['text']+=' 바뀐 대사'
   path.write_text(json.dumps(refreshed,ensure_ascii=False))
   with self.assertRaises(AssertionError):refresh(path,'bindings')
 def test_common_daram_scale_and_neutral_foot_canvas(self):
  base=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people']
  front=json.loads((ROOT/'game/assets/room13-dialogue-player-facing.json').read_text())['people']
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
   entry=self.data['entries'][row['person']+':'+row['slot']]
   profile=entry['profiles'][row['height']]
   path=ROOT/'game'/profile['frames'][row['slot']]['file']
   # 48행 영수증과 받은 옛 출력은 새 작화와 별개로 계속 보존·검증한다.
   legacy=ROOT/'game/assets/dialogue-context-master'/row['person']/row['height']/(row['slot']+'.webp')
   self.assertEqual(hashlib.sha256(legacy.read_bytes()).hexdigest(),row['output_sha256'])
   if entry.get('art_revision')=='daram-consistency-20261107':
    from import_daram_consistency import CONTEXT,VISIBLE_HEIGHT_840,QUESTION_VISIBLE_HEIGHT
    self.assertEqual(row['person'],'daram');self.assertIn(row['slot'],CONTEXT)
    self.assertEqual(profile['canvas'],front['daram']['profiles'][row['height']]['canvas'])
    frame=profile['frames'][row['slot']]
    self.assertTrue(frame['file'].startswith('assets/dialogue-player-facing/daram-consistency-20261107/'))
    with Image.open(path) as im:bounds=im.getchannel('A').point(lambda a:255 if a>=40 else 0).getbbox()
    visible=QUESTION_VISIBLE_HEIGHT if row['height']=='560' else VISIBLE_HEIGHT_840*int(row['height'])/840
    self.assertAlmostEqual((bounds[3]-bounds[1])*frame['scale'],visible,delta=.00001)
   else:self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),row['output_sha256'])
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
    refreshed=data[cue['key']].get('art_revision')=='daram-consistency-20261107'
    self.assertEqual(startup_media(path,set()),not refreshed and cue['slot']=='intake21_01_bravado',path)
 def test_held_icons_are_not_registered(self):
  records=json.loads((ROOT/'game/v111/records.json').read_text())['records']
  for asset in self.receipt['held_icons']['assets']:
   for evidence in asset['evidence']:
    self.assertIn(evidence['line_id'],records)
   self.assertNotIn(asset['asset_id'],json.dumps(self.data))
if __name__=='__main__':unittest.main()
