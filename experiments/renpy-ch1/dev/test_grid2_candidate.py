import unittest,ast,math
from pathlib import Path
R=Path(__file__).parents[1];G=R/'game'
class Node:
 def __init__(self,kind,*args,**kwargs):self.kind=kind;self.args=args;self.kwargs=kwargs
 def __repr__(self):return repr((self.kind,self.args,self.kwargs))
def construct(name):return lambda *a,**k:Node(name,*a,**k)
def block(path):
 text=path.read_text();b=text.split('init 57 python:\n',1)[1].split('\n# Wrap the final')[0];return '\n'.join(x[4:] if x.startswith('    ') else x for x in b.splitlines())
class GridTests(unittest.TestCase):
 def setUp(self):
  self.g={k:construct(k) for k in ['Transform','Flatten','Fixed','At']};exec(block(G/'room13_character_grid2_v1.rpy'),self.g)
 def enable(self):self.g['R13_CHARACTER_GRID2_ENABLED']=True
 def test_default_off_and_noop(self):
  a=Node('source');self.assertIs(self.g['r13_g2_final'](a),a);self.assertFalse(self.g['r13_g2_enabled']())
 def test_exact_one_final_pass(self):
  self.enable();n=self.g['r13_g2_final'](Node('source'));self.assertEqual(n.kind,'Transform');self.assertEqual(n.kwargs['xysize'],(1280,720));self.assertEqual(n.args[0].kind,'Flatten');low=n.args[0].args[0];self.assertEqual(low.kwargs['xysize'],(640,360));self.assertTrue(low.kwargs['nearest']);self.assertEqual(repr(n).count("'Flatten'"),1)
 def test_invalid_extents_fail(self):
  self.enable()
  for size in [(1279,720),(1280,719),(0,720)]:
   with self.assertRaises(AssertionError):self.g['r13_g2_final']('art',size)
 def test_snap_and_pad(self):
  for n in range(-2001,2002):
   v=n/4.;q=self.g['r13_g2_snap'](v);self.assertEqual(q%2,0);self.assertLessEqual(abs(q-v),1)
   if v>0:self.assertGreaterEqual(self.g['r13_g2_extent'](v),v)
 def test_profiles_actual_sizes_and_text_exclusion(self):
  self.enable()
  for size in [(48,48),(60,62),(44,44),(54,54),(76,76)]:
   x=self.g['r13_g2_profile_transform']('nabi avatar_neutral',xysize=size,fit='contain',nearest=False);self.assertEqual(x.kwargs['xysize'],size);self.assertEqual(x.args[0].kind,'Flatten')
  text=Node('Text','?');n=self.g['r13_g2_profile_transform'](text,xysize=(48,48));self.assertEqual(n.args[0],text)
 def test_actor_copy_clip_even_feet_and_source_preserved(self):
  self.enable();a=dict(x=13,y=41,width=151,height=201,rect=[13,41,151,201],depth=242,person='nabi',pose='work');saved=dict(a)
  b=self.g['r13_g2_actor_geometry'](a,2160);self.assertEqual(a,saved);self.assertIsNot(a,b)
  for k in ['x','y','width','height']:self.assertEqual(b[k]%2,0)
  self.assertEqual(b['grid2_source_size'],(151,201));self.assertLessEqual(abs(b['y']+b['height']-(a['y']+a['height'])),1)
  self.assertEqual(b['rect'],[b['x'],b['y'],b['width'],b['height']])
 def test_raw_scale_once_and_same_visible_mask(self):
  t=(G/'room13_acting.rpy').read_text();self.assertIn('if r13_g2_enabled():grid=1',t);self.assertIn('r13_staged_visible_art(actor,still=True)',t)
  t=(G/'room13_character_grid2_v1.rpy').read_text();self.assertIn('art=_r13_g2_visible_art(actor,still)',t);self.assertIn('return r13_g2_final(art,(actor["width"],actor["height"]))',t)
 def test_meeting_background_excluded(self):
  t=(G/'room13_meeting_camera.rpy').read_text();method=t.split('def r13_g2_render_actors',1)[1].split('def visit',1)[0]
  self.assertNotIn('self.plate',method);self.assertNotIn('self.foreground',method);self.assertIn('r13_g2_snap(x)',method)
  self.assertIn('self.r13_g2_output=r13_g2_final(self.r13_g2_actors)',t);self.assertNotIn('r13_g2_final(self.plate)',t)
 def test_dialogue_wrap_after_reaction(self):
  t=(G/'room13_rules.rpy').read_text();self.assertLess(t.index('what,at_list=r13_react'),t.index('what=r13_g2_final(Fixed(At(what,*at_list)'))
 def test_no_global_activation(self):
  for p in G.rglob('*.rpy'):
   if 'qa_tests' in p.relative_to(G).parts:continue
   self.assertNotRegex(p.read_text(),r'R13_CHARACTER_GRID2_ENABLED\s*=\s*True')
if __name__=='__main__':unittest.main(verbosity=2)
