"""Venue rendering must not invent a table, move an event, or announce future meetings."""
import ast,copy,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Venues(unittest.TestCase):
 def setUp(self):
  self.store=types.SimpleNamespace(room13=dict(day=4,period=0,location='square',offers={},flags=[],propositions=[]))
  self.env=dict(store=self.store,renpy=types.SimpleNamespace(Displayable=object,loadable=lambda p:False),
   Transform=lambda path,**kw:path,Crop=lambda area,child:child)
  code=(ROOT/'game/room13_meeting_seating.rpy').read_text().split('init 99 python:\n',1)[1].split('\ntransform ',1)[0]
  exec(textwrap.dedent(code),self.env)
 def test_venue_is_authored_place_not_current_hub_location(self):
  for session,place,kind in [('trial','dining','round'),('ep4','dining','round'),('ep1','square','field'),('ep2','square','field'),('ep6','square','field'),('ep3','school','room'),('ep5a','school','room'),('ep5','school','room'),('finale','altar','stone')]:
   actual=self.env['R13_MEETING_VENUES'][session]
   self.assertEqual(actual[:2],(place,kind))
  self.assertEqual(self.env['r13_meeting_map_venue']('inn'),self.env['r13_meeting_map_venue']('dining'))
  self.assertIsNone(self.env['r13_meeting_map_venue']('passage'))
 def test_close_table_lowers_edge_without_moving_wide_seat_contacts(self):
  close=self.env['r13_meeting_close_edge'];wide=self.env['r13_meeting_edge']
  self.assertEqual(close(640,'trial'),532);self.assertEqual(wide(640,'trial'),396)
  self.assertEqual(close(0,'trial'),536);self.assertEqual(close(1280,'trial'),536)
  self.assertEqual(close(640,'finale'),532);self.assertEqual(wide(640,'finale'),432)
  for session in ('ep1','ep3'):
   self.assertEqual(close(640,session),wide(640,session))
 def test_existing_episode_plate_wrapper_keeps_round_table_for_ep4(self):
  base=self.env['r13_meeting_plate']
  self.env.update(_r13_e1_plate=base,R13_EP_MEETING_PLACE=dict(ep1='winter_square',ep4='council',ep3='r13_school'),r13_background=lambda key:key)
  src='    def r13_meeting_plate'+(ROOT/'game/systems/room13_ep1_lamp_thief.rpy').read_text().split('    def r13_meeting_plate',1)[1].split('\n    _r13_e1_cast',1)[0]
  fn=next(n for n in ast.parse(textwrap.dedent(src)).body if isinstance(n,ast.FunctionDef) and n.name=='r13_meeting_plate')
  exec(compile(ast.Module(body=[fn],type_ignores=[]),'episode_plate','exec'),self.env)
  plate=self.env['r13_meeting_plate']
  self.assertEqual(plate('ep4',True),base('trial',True))
  self.assertEqual(plate('ep1',True),'winter_square')
  self.assertEqual(plate('ep3',False),'r13_school')
  self.assertIn('altar-standing',plate('finale',True))
 def test_pending_icon_requires_an_actual_current_offer(self):
  pending=self.env['r13_meeting_map_pending'];s=self.store.room13
  self.assertFalse(pending('square'))
  s['offers']={'r13_ep1_meeting':dict(day=4,period=0,location='square')}
  before=copy.deepcopy(s);self.assertTrue(pending('square'));self.assertFalse(pending('school'))
  self.assertEqual(s,before)
  s['period']=1;self.assertFalse(pending('square'))
  s['period']=0;s['day']=5;self.assertFalse(pending('square'))
  s['day']=4;s['offers']={'r13_w1c_portrait':dict(day=4,period=0,location='square')};self.assertFalse(pending('square'))
 def test_standing_feet_do_not_use_tabletop_occlusion_height(self):
  self.env['CAST']={'buri':{'neutral':{'crop':(0,0,200,400)}}}
  for session in ('ep1','ep3','ep5','ep6'):
   edge=self.env['r13_meeting_edge'](640,session)
   w,h,top=self.env['r13_meeting_standing_slot']('buri',6,edge,session)
   self.assertEqual(top+h,edge)
  self.assertEqual(self.env['r13_meeting_edge'](640,'trial'),396)
  self.assertEqual(self.env['r13_meeting_edge'](640,'finale'),432)
