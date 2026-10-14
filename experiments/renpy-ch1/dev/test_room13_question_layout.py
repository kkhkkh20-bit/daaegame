"""Pixel coordinates must stay integers when RenPy returns float render sizes."""
import textwrap,types,unittest
from pathlib import Path
root=Path(__file__).resolve().parents[1]
class Render:
 def __init__(self,height):self.height=height
 def get_size(self):return (423.0,self.height)
ns=dict(renpy=types.SimpleNamespace(Displayable=object,render=lambda text,*args:Render(52.0 if text=='wrapped' else 26.0)),Text=lambda caption,**kw:caption,r13_read_size=lambda a,b:a,r13_ui_font=lambda:'font')
source=(root/'game/systems/room13_reference_ui.rpy').read_text().split('init 79 python:\n')[1].split('\ninit 80:')[0]
exec(textwrap.dedent(source),ns)
class QuestionLayoutTest(unittest.TestCase):
 def test_wrapped_caption_uses_absolute_pixel_coordinates(self):
  height=ns['r13_reference_list_height']([('wrapped',None,False),('short',None,False)],470)
  self.assertIs(type(height),int);self.assertLess(height,540);self.assertIs(type((680-height)//2),int)
 def test_scroll_cap_and_empty_list_stay_integral(self):
  self.assertIs(type(ns['r13_reference_list_height']([],470)),int)
  height=ns['r13_reference_list_height']([('wrapped',None,False)]*20,470)
  self.assertEqual(height,540);self.assertIs(type(height),int)
if __name__=='__main__':unittest.main()
