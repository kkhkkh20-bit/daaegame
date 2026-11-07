import ast,json,textwrap,types,unittest
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
  base=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people'];self.assertEqual(len(base),59);self.assertTrue({'bami:small_relief','resident_lamplighter:guarded_relief','kid_kkomi:resilient_pride','resident_tosil:empathetic_confusion'}.issubset(self.data['entries']))
  for entry in self.data['entries'].values():
   for height,p in entry['profiles'].items():
    self.assertEqual(p['canvas'],base[entry['person']]['profiles'][height]['canvas'])
    for f in p['frames'].values():
     with Image.open(ROOT/'game'/f['file']) as im:
      b=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox()
     x,y=f['offset'];self.assertGreaterEqual(x+b[0],0);self.assertGreaterEqual(y+b[1],0);self.assertLessEqual(x+b[2],p['canvas'][0]);self.assertLessEqual(y+b[3],p['canvas'][1])
 def test_wrong_mother_role_is_not_registered(self):
  self.assertFalse(any(e['person'] in ('mom','chorong_mother') for e in self.data['entries'].values()))

 def rendering_environment(self,plan):
  def function(path,name):
   text=path.read_text().split(' python:',1)[1]
   tree=ast.parse(textwrap.dedent(text))
   return next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name==name)
  fit=function(ROOT/'game/systems/room13_dialogue_beats.rpy','r13_dialogue_fit_profile')
  render=function(ROOT/'game/systems/room13_dialogue_context_art.rpy','r13_dialogue_beat_art')
  fallback=object()
  env=dict(store=types.SimpleNamespace(r13_dialogue_beat=plan),R13_DIALOGUE_CONTEXT_ART=self.data,
           R13DialogueBeat=lambda chosen,profile:(chosen,profile),_r13_context_beat_art=lambda *args:fallback)
  exec(compile(ast.Module(body=[fit,render],type_ignores=[]),'문맥 표정 크기 맞춤','exec'),env)
  return env,fallback

 def test_actual_say_height_keeps_each_authored_context_frame(self):
  # 840 키만 찾던 경로는 1302 대사에서 전용 표정을 버리고 일반 중립 그림으로 돌아갔다.
  for key,entry in self.data['entries'].items():
   plan=dict(person=entry['person'],talk=entry['slot'],react=None,context_key=key)
   env,fallback=self.rendering_environment(plan)
   chosen,profile=env['r13_dialogue_beat_art'](entry['person'],1302)
   original=entry['profiles']['840'];ratio=1302/840
   self.assertIs(chosen,plan)
   self.assertEqual(set(profile['frames']),set(original['frames']))
   self.assertEqual(profile['canvas'],[round(n*ratio) for n in original['canvas']])
   frame=profile['frames'][plan['talk']];source=original['frames'][plan['talk']]
   self.assertEqual(frame['file'],source['file'])
   self.assertEqual(frame['offset'],[round(n*ratio) for n in source['offset']])
   self.assertAlmostEqual(frame['scale'],source.get('scale',1)*ratio)
   self.assertNotEqual((chosen,profile),fallback)

 def test_exact_sizes_and_other_fitted_height_keep_same_emotion(self):
  key='bami:small_relief';entry=self.data['entries'][key]
  plan=dict(person=entry['person'],talk=entry['slot'],react=None,context_key=key)
  env,_=self.rendering_environment(plan);render=env['r13_dialogue_beat_art']
  for h in (560,760,840):
   self.assertIs(render(entry['person'],h)[1],entry['profiles'][str(h)])
  chosen,profile=render(entry['person'],740)
  self.assertEqual(chosen['talk'],'small_relief')
  self.assertEqual(profile['frames']['small_relief']['file'],entry['profiles']['760']['frames']['small_relief']['file'])

 def test_other_speaker_and_missing_context_keep_existing_beat_path(self):
  key='bami:small_relief';entry=self.data['entries'][key]
  plan=dict(person=entry['person'],talk=entry['slot'],react=None,context_key=key)
  env,fallback=self.rendering_environment(plan);render=env['r13_dialogue_beat_art']
  self.assertIs(render('mom',1302),fallback)
  env['store'].r13_dialogue_beat=dict(plan,context_key='미등록 문맥')
  self.assertIs(render(entry['person'],1302),fallback)
  env['store'].r13_dialogue_beat=None
  self.assertIs(render(entry['person'],1302),fallback)
if __name__=='__main__':unittest.main()
