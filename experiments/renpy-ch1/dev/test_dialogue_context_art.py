import json,textwrap,types,unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class ContextArt(unittest.TestCase):
 def setUp(self):
  self.data=json.loads((ROOT/'game/assets/room13-dialogue-context-art.json').read_text())
 def test_exact_context_and_authored_pose_gate(self):
  source=(ROOT/'game/systems/room13_dialogue_context_art.rpy').read_text();block=source.split('    def r13_dialogue_context_match',1)[1].split('    _r13_context_beat_begin',1)[0]
  env=dict(R13_DIALOGUE_CONTEXT_ART=self.data,R13_FULLBODY_PLAIN={'neutral','joy','anxious','angry','surprise'})
  exec('def r13_dialogue_context_match'+textwrap.dedent(block),env)
  match=env['r13_dialogue_context_match']
  for cue in self.data['bindings']:
   args=(cue['identity'],cue['index'],(cue['person'],cue['text']))
   self.assertEqual(match(*args,'neutral'),cue)
   self.assertIsNone(match(*args,'hold_storybook'))
   self.assertIsNone(match(cue['identity']+'other',*args[1:],'neutral'))
   self.assertIsNone(match(cue['identity'],cue['index'],('mom',cue['text']),'neutral'))
 def test_profiles_preserve_normal_canvas_and_have_files(self):
  base=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people'];self.assertEqual(len(base),59);self.assertEqual(len(self.data['entries']),4)
  for entry in self.data['entries'].values():
   for height,p in entry['profiles'].items():
    self.assertEqual(p['canvas'],base[entry['person']]['profiles'][height]['canvas'])
    for f in p['frames'].values():
     with Image.open(ROOT/'game'/f['file']) as im:
      b=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox()
     x,y=f['offset'];self.assertGreaterEqual(x+b[0],0);self.assertGreaterEqual(y+b[1],0);self.assertLessEqual(x+b[2],p['canvas'][0]);self.assertLessEqual(y+b[3],p['canvas'][1])
 def test_wrong_mother_role_is_not_registered(self):
  self.assertFalse(any(e['person'] in ('mom','chorong_mother') for e in self.data['entries'].values()))
if __name__=='__main__':unittest.main()
