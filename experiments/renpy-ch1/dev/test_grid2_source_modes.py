"""Actual source functions under both modes; structural, not native visual proof."""
import ast,textwrap,unittest
from pathlib import Path
from types import SimpleNamespace
from grid2_test_env import load_grid2
ROOT=Path(__file__).resolve().parents[1]
class Node:
 def __init__(self,kind,*args,**kw):self.kind=kind;self.args=args;self.kw=kw

def nodes(art):
 if isinstance(art,Node):
  yield art
  for child in art.args:yield from nodes(child)

def constructors(env):
 for kind in ('Transform','Fixed','Flatten','At'):
  env[kind]=lambda *a,_kind=kind,**kw:Node(_kind,*a,**kw)

def function(env,path,name):
 source=(ROOT/'game'/path).read_text();start=source.index('    def '+name+'(')
 end=source.find('\n    def ',start+1)
 block=source[start:end if end>=0 else len(source)]
 tree=ast.parse(textwrap.dedent(block));exec(compile(ast.Module(body=[tree.body[0]],type_ignores=[]),str(path),'exec'),env)

def assert_final(test,env,raw):
 final=env['r13_g2_final'](raw)
 test.assertEqual(final.kw['xysize'],(1280,720))
 chain=list(nodes(final));test.assertEqual(sum(n.kind=='Flatten' for n in chain),1)
 low=final.args[0].args[0]
 test.assertEqual(low.kw['xysize'],(640,360));test.assertTrue(low.kw['nearest'])
 test.assertFalse(low.kw['subpixel']);test.assertTrue(final.kw['nearest'])
 test.assertTrue(any(n is raw for n in chain))

def assert_dialogue_source_modes(test):
 frame=dict(file='approved-source/neutral.webp',offset=[20,30])
 profile=dict(canvas=[400,840],frames={'neutral':frame})
 env=dict(store=SimpleNamespace(r13_meeting_active=False),renpy=SimpleNamespace(loadable=lambda _:True),r13_dialogue_source_profile=lambda *a:profile)
 constructors(env);load_grid2(env)
 function(env,'systems/room13_dialogue_beats.rpy','r13_dialogue_source_neutral')
 for mode in (False,True):
  env['R13_CHARACTER_GRID2_ENABLED']=mode
  raw=env['r13_dialogue_source_neutral']('guard','neutral',840)
  transforms=[n for n in nodes(raw) if n.kind=='Transform'];test.assertEqual(len(transforms),1)
  t=transforms[0];test.assertEqual(t.args[0],frame['file']);test.assertEqual((t.kw['xpos'],t.kw['ypos']),(20,30))
  test.assertIs(t.kw['nearest'],mode);test.assertIs(t.kw['subpixel'],not mode)
  if mode:assert_final(test,env,raw)
  else:test.assertIs(env['r13_g2_final'](raw),raw)

class SourceModes(unittest.TestCase):
 def test_source_off_is_smooth_on_is_raw_then_exactly_one_final_pass(self):assert_dialogue_source_modes(self)
 def test_enabled_portrait_refresh_preserves_partner_without_reentry(self):
  from test_dialogue_line_refresh import PortraitRefresh
  fixture=PortraitRefresh();fixture.setUp();env=fixture.speaker.__globals__;constructors(env)
  env['R13_CHARACTER_GRID2_ENABLED']=True
  fixture.store.r13_dialogue_beat={'talk':'joy'};fixture.speaker('daram')
  fixture.store.r13_dialogue_beat=None;fixture.speaker('daram');fixture.speaker('dad');fixture.speaker(None)
  self.assertEqual(len(fixture.shown),2);self.assertEqual(fixture.entrances,[False,False]);self.assertEqual(fixture.reactions,[])
  for shown in fixture.shown:
   self.assertEqual(shown['what'].kw['xysize'],(1280,720))
   self.assertEqual(sum(n.kind=='Flatten' for n in nodes(shown['what'])),1)
 def test_enabled_pov_keeps_carriage_daram_only(self):
  from test_room13_pov import ViewpointSpeaker
  fixture=ViewpointSpeaker();fixture.setUp();env=fixture.speak.__globals__;constructors(env);env['R13_CHARACTER_GRID2_ENABLED']=True
  fixture.store.place='마차 안';fixture.speak('dad','thinking');fixture.speak('karo','neutral');fixture.speak('daram','joy')
  self.assertEqual(fixture.store.r13_motion_person,'daram');count=len(fixture.calls)
  fixture.speak('dad','thinking');fixture.speak('karo','neutral');self.assertEqual(len(fixture.calls),count)
  art=fixture.calls[-1][2]['what'];self.assertEqual(sum(n.kind=='Flatten' for n in nodes(art)),1)
  self.assertTrue(any(n.kind=='At' and 'pop' in n.args for n in nodes(art)))
 def test_enabled_beat_retains_reaction_clock_and_nearest_source(self):
  from test_dialogue_beats import functions
  env=functions();plan=dict(person='guard',talk='surprise_talk',react='surprise_react',settled=False,duration=.35)
  transforms=[]
  env.update(store=SimpleNamespace(r13_dialogue_beat=plan),persistent=SimpleNamespace(room13_motion=True),Fixed=lambda child,**kw:child,Transform=lambda path,**kw:transforms.append(kw) or path,renpy=SimpleNamespace(Displayable=object,is_skipping=lambda:False,in_rollback=lambda:False,redraw=lambda *a:None,render=lambda frame,*a:frame))
  load_grid2(env);env['R13_CHARACTER_GRID2_ENABLED']=True
  source=(ROOT/'game/systems/room13_dialogue_beats.rpy').read_text().split('init 170 python:\n',1)[1]
  cls=next(n for n in ast.parse(textwrap.dedent(source)).body if isinstance(n,ast.ClassDef))
  exec(compile(ast.Module(body=[cls],type_ignores=[]),'actual-beat-class','exec'),env)
  profile=dict(canvas=[100,200],frames={k:dict(file=k,offset=[0,0]) for k in ('surprise_talk','surprise_react')})
  art=env['R13DialogueBeat'](plan,profile)
  self.assertEqual(art.render(100,200,100,100),'surprise_react')
  self.assertEqual(art.render(100,200,100.36,100.36),'surprise_talk')
  rebuilt=env['R13DialogueBeat'](env['store'].r13_dialogue_beat,profile)
  self.assertEqual(rebuilt.render(100,200,200,200),'surprise_talk')
  self.assertTrue(transforms);self.assertTrue(all(t['nearest'] and not t['subpixel'] for t in transforms))
 def test_meeting_offsets_and_sampling_both_modes(self):
  spec=dict(file='approved-meeting.webp',canvas=[400,840],offset=[20,30],scale=1.0)
  env=dict(store=SimpleNamespace(r13_meeting_art_slots={'guard':'listen'}),R13_MEETING_SOURCE_ART={'guard':{'listen':spec}},renpy=SimpleNamespace(loadable=lambda _:True))
  constructors(env);load_grid2(env);function(env,'room13_meeting_camera.rpy','r13_meeting_slot_art')
  for mode in (False,True):
   env['R13_CHARACTER_GRID2_ENABLED']=mode;raw=env['r13_meeting_slot_art']('guard',740)
   transforms=[n for n in nodes(raw) if n.kind=='Transform'];self.assertEqual(len(transforms),1)
   t=transforms[0];self.assertIs(t.kw['nearest'],mode);self.assertIs(t.kw['subpixel'],not mode)
   self.assertIs(type(t.kw['xpos']),int);self.assertIs(type(t.kw['ypos']),int)
if __name__=='__main__':unittest.main()
