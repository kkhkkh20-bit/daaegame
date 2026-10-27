"""2일차 단계 안내는 저장된 현재 단계에서 계산하며 게임 진행을 변경하지 않는다."""
import ast
import copy
from pathlib import Path
import textwrap
from types import SimpleNamespace
import unittest

ROOT=Path(__file__).resolve().parents[1]
GUIDE=(ROOT/'game/systems/room13_day2_guidance.rpy').read_text()
GOAL=(ROOT/'game/systems/room13_v111_goal.rpy').read_text()
IDLE=(ROOT/'game/room13_v111_idle.rpy').read_text()

class Day2Guidance(unittest.TestCase):
 def make(self,gate='lamp_rope',location='square',day=2,scene='MS14_D02_S01',destination=None):
  state=dict(day=day,location=location,evidence=['V111:E01','V111:E06'],records={},arguments={},flags=[],
      v111=dict(gate=gate,scene=scene,travel_to=destination,people=['resident_lamplighter','daram'],values={'elapsed_minutes':20}))
  calls=[]
  env=dict(store=SimpleNamespace(room13=state),r13_object_name=lambda k:'원래 이름:'+k,
      r13_nw_added_line=lambda row:dict(row),r13_v111_goal=lambda:'원래 장면의 생각',
      r13_v111_idle_lines=lambda p:calls.append(p) or [('old',p)],r13_met_people=lambda:[],
      R13_V111_QUESTIONS={},r13_v111_value=lambda key:None)   # 2026-10-27 R04: 답이 난 장면 의문 치환(room13_v111_goal.rpy)이 읽는 값
  exec(textwrap.dedent(GUIDE.split('init 353 python:\n')[1]),env)
  goal_block=GOAL.split('init 341 python:\n')[1].split('\n# ',1)[0]
  exec(textwrap.dedent(goal_block),env)
  idle_block=IDLE.split('init 351 python:\n')[1]
  exec(textwrap.dedent(idle_block),env)
  return env,state,calls

 def test_required_action_replaces_long_term_question(self):
  env,_,_=self.make()
  text=env['r13_v111_goal']()
  self.assertIn('메모를 초롱에게',text)
  self.assertIn('덮개 지지 끈',text)
  self.assertNotIn('떠날 길',text)
  self.assertEqual(env['r13_object_name']('lamp'),'등불 · 덮개 지지 끈')

 def test_each_wait_stage_describes_current_action(self):
  for gate,place,words in (
      ('lamp_rope','square',('지지 끈','점검')),
      ('go_box','square',('깊은 숲','교환함')),
      ('box_inspect','forest',('교환함과 주변','직접')),
      ('box_note','forest',('쪽지','직접 넣자')),
      ('envelope_show','post',('봉투','서련')),
      ('post_menu','post',('돌려받기','남은 질문'))):
   env,state,_=self.make(gate,place);before=copy.deepcopy(state)
   text=env['r13_v111_goal']()
   for word in words:self.assertIn(word,text)
   self.assertEqual(state,before)

 def test_travel_phase_uses_destination_without_inventing_a_discovery(self):
  for scene,destination,word in (
      ('MS14_D02_S01','gate','마차'),('MS14_D02_S01','square','광장'),
      ('MS14_D02_S01','forest','교환함'),('MS14_D02_S02','post','발신인')):
   env,state,_=self.make('travel',scene=scene,destination=destination)
   self.assertIn(word,env['r13_v111_goal']())
  env,_,_=self.make('travel',scene='MS14_D02_S04',destination='post')
  self.assertEqual(env['r13_v111_goal'](),'원래 장면의 생각')

 def test_repeated_lamplighter_taps_only_explain_the_action(self):
  env,state,calls=self.make();before=copy.deepcopy(state)
  for _ in range(3):
   lines=env['r13_v111_idle_lines']('resident_lamplighter')
   self.assertEqual(lines[0]['speaker'],'초롱')
   self.assertIn('지지 끈',lines[0]['text'])
   self.assertNotIn('물어볼 게 없',lines[0]['text'])
  self.assertEqual(calls,[])
  self.assertEqual(state,before)

 def test_finished_action_changes_reminder_and_removes_old_lamp_name(self):
  env,state,_=self.make()
  state['v111']['gate']='go_box'
  text=env['r13_v111_idle_lines']('resident_lamplighter')[0]['text']
  self.assertIn('교환함',text);self.assertNotIn('지지 끈',text)
  self.assertEqual(env['r13_object_name']('lamp'),'원래 이름:lamp')
  state['v111']['gate']='box_note';state['location']='forest'
  self.assertIn('쪽지',env['r13_v111_idle_lines']('resident_lamplighter')[0]['text'])

 def test_other_people_days_places_and_legacy_calls_keep_existing_behavior(self):
  for day,place,gate,person in ((3,'square','lamp_rope','resident_lamplighter'),
      (2,'forest','lamp_rope','resident_lamplighter'),(2,'square','lamp_rope','daram'),
      (2,'square','sleep2','resident_lamplighter')):
   env,_,calls=self.make(gate,place,day)
   self.assertEqual(env['r13_v111_idle_lines'](person),[('old',person)])
   self.assertEqual(calls,[person])
  env,state,_=self.make();state['v111']={}
  self.assertIsNone(env['r13_day2_guidance']())

 def test_restored_state_restores_guidance_without_remembered_ui_progress(self):
  env,state,_=self.make('travel','room13',scene='MS14_D02_S01',destination='gate')
  morning=copy.deepcopy(state);first=env['r13_v111_goal']()
  state['location']='forest';state['v111'].update(gate='box_note',travel_to='forest')
  state['v111']['values'].update(mother_box_checked_day2=True,arrival_note_sent=True)
  self.assertIn('쪽지',env['r13_v111_goal']())
  env['store'].room13=copy.deepcopy(morning)
  self.assertEqual(env['r13_v111_goal'](),first)
  self.assertEqual(env['store'].room13,morning)

if __name__=='__main__':unittest.main()
