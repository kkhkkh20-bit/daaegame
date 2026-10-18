"""Unit normalization contract; verify actual slider geometry in native QA."""
import math,textwrap,unittest
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1]
class VolumePercentTest(unittest.TestCase):
 def test_percent_tracks_engine_adjustment(self):
  source=(ROOT/'game/room13_options.rpy').read_text().split('    def r13_mixer_percent(mixer):',1)[1]
  ns={};position=[0];ranges=[60]
  class MixerValue:
   def __init__(self,mixer):self.mixer=mixer
   def get_adjustment(self):return SimpleNamespace(value=position[0],range=ranges[0])
  ns['MixerValue']=MixerValue
  exec('def r13_mixer_percent(mixer):\n'+textwrap.indent(textwrap.dedent(source),'    '),ns)
  for scale in (1,60,80):
   ranges[0]=scale
   for fraction,want in ((0,0),(.25,25),(.5,50),(.75,75),(1,100)):
    position[0]=scale*fraction;self.assertEqual(ns['r13_mixer_percent']('music'),want)
  position[0]=-1;self.assertEqual(ns['r13_mixer_percent']('sfx'),0)
  position[0]=1000;self.assertEqual(ns['r13_mixer_percent']('sfx'),100)
  ranges[0]=0;self.assertEqual(ns['r13_mixer_percent']('sfx'),0)
 def test_both_labels_use_same_source(self):
  s=(ROOT/'game/screens.rpy').read_text()
  for mixer in ('music','sfx'):self.assertIn('r13_mixer_percent("%s")'%mixer,s)
  self.assertIn('bar value Preference("music volume")',s)
  self.assertIn('bar value Preference("sound volume")',s)
  self.assertNotIn('round(_preferences.get_volume(',s)
 def test_mismatch_explanation(self):
  # At standard 60dB slider range, raw amplitude .55 appears at 91.35%.
  position=(20*math.log10(.55)+60)/60
  self.assertGreater(position,.9)
if __name__=='__main__':unittest.main(verbosity=2)
