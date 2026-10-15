import copy,json,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class HomeTest(unittest.TestCase):
 def setUp(self):
  self.state=dict(day=2,period=0,location='room13',daram_state='with_dad',mom_state='hidden',case_state='pending',trial_result='pending',flags=['lodging'],evidence=[],read_topics=[])
  store=types.SimpleNamespace(room13=self.state);data={'topics':{}}
  def finish(key):store.room13['read_topics']=list(dict.fromkeys(store.room13['read_topics']+[key]))
  self.ns=dict(store=store,ROOM13=data,winter_copy=copy,r13_topics=lambda p:[(k,s) for k,s in data['topics'].items() if s['npc']==p],r13_stage_people=lambda entry=False:[dict(person='daram',pose='neutral',x=0,y=0)],r13_home_with_daram=lambda:store.room13['location'] in ('room13','guestroom') and store.room13['daram_state'] in ('with_dad','rescued') and 'lodging' in store.room13['flags'],r13_acting_spec=lambda p,pose:dict(foot=[50,100],seat=[50,80],contact='floor_sit'),r13_actor_geometry=lambda p,pose:(100,100),r13_layout=lambda location=None:{},r13_conversation_topic_lines=lambda k:['original'],r13_calendar_topic_seen=lambda k,s:k in store.room13['read_topics'],r13_finish_topic=finish,r13_intro_goal=lambda:'original goal',r13_compare_result=lambda selected:'original comparison',r13_present=lambda person,key,identity=False:[(person,'original response')])
  exec(textwrap.dedent((ROOT/'game/systems/room13_daram_home.rpy').read_text().split('init 101 python:\n')[1]),self.ns)
 def keys(self):return {k for k,s in self.ns['r13_topics']('daram')}
 def test_only_owned_information_opens_questions(self):
  self.assertEqual(self.keys(),{'home:daram:rest'});self.state['evidence']=['M01'];self.assertIn('home:daram:mother',self.keys());self.assertNotIn('home:daram:letters',self.keys());self.state['evidence']+=['E01','E18','J04'];self.assertTrue({'home:daram:letters','home:daram:packet'}<=self.keys())
 def test_held_and_other_places_never_create_home_daram(self):
  for changes in ({'daram_state':'held'},{'daram_state':'with_dad','location':'square'},{'location':'room13','flags':[]}):
   self.state.update(changes);self.assertEqual(self.keys(),set())
 def test_reunion_not_unlocked_by_day_or_first_week_intervention(self):
  self.state.update(day=5,mom_state='intervened',evidence=['E19']);self.assertNotIn('home:daram:reunion',self.keys());self.state.update(day=10,mom_state='hidden');self.assertNotIn('home:daram:reunion',self.keys());self.state['mom_state']='reunited';self.assertIn('home:daram:reunion',self.keys())
 def test_case_verdict_and_crisis_are_separate(self):
  self.state.update(case_state='occurred');self.assertIn('home:daram:case',self.keys());self.assertNotIn('home:daram:verdict',self.keys());self.state.update(trial_ended=True,day=8,week2_started=True);self.assertTrue({'home:daram:verdict','home:daram:cold'}<=self.keys())
 def test_read_mark_refreshes_and_survives_json_save(self):
  self.ns['r13_finish_topic']('home:daram:rest');self.assertTrue(self.ns['r13_daram_home_seen']('home:daram:rest'));self.ns['store'].room13=json.loads(json.dumps(self.ns['store'].room13));self.assertTrue(self.ns['r13_daram_home_seen']('home:daram:rest'));self.ns['store'].room13['evidence'].append('M01');self.assertFalse(self.ns['r13_daram_home_seen']('home:daram:rest'))
 def test_lines_and_queries_do_not_grant_time_money_or_evidence(self):
  self.state.update(evidence=['M01','E01','E18','J04','J05']);before=copy.deepcopy(self.state)
  for k in self.keys():
   self.assertTrue(self.ns['r13_conversation_topic_lines'](k));self.assertEqual(self.ns['ROOM13']['topics'][k]['give'],[])
  self.ns['r13_stage_people']();self.ns['r13_intro_goal']();self.assertEqual(self.state,before)
 def test_activity_uses_time_without_mutating_cached_actor(self):
  original=dict(person='daram',pose='neutral',x=0,y=0);self.ns['_r13_daram_home_stage']=lambda e=False:[original]
  for period,pose in [(0,'action_1'),(1,'action_2'),(2,'inspect_floor')]:
   self.state['period']=period;actor=self.ns['r13_stage_people']()[0];self.assertEqual(actor['pose'],pose);self.assertEqual(original['pose'],'neutral');self.assertTrue(0<=actor['y']<720)
  self.state['case_state']='occurred';self.assertEqual(self.ns['r13_stage_people']()[0]['pose'],'neutral')
 def test_wide_room13_uses_its_own_home_positions(self):
  # 0.18.55: the wide 13호 places each activity on its own bed/rug; guestroom keeps the old spot.
  original=dict(person='daram',pose='neutral',x=0,y=0);self.ns['_r13_daram_home_stage']=lambda e=False:[original]
  spots={'action_1':[1010,445,125],'action_2':[1300,655,185],'inspect_floor':[1530,650,138],'neutral':[1420,662,185]}
  self.ns['r13_layout']=lambda location=None:{'home_positions':spots} if location=='room13' else {}
  for period,pose in [(0,'action_1'),(1,'action_2'),(2,'inspect_floor')]:
   self.state['period']=period;actor=self.ns['r13_stage_people']()[0];cx,feet,height=spots[pose]
   self.assertEqual(actor['height'],height);self.assertEqual(actor['y'],int(feet-(80 if pose=='action_1' else 100)*height/100.0))
  self.state['location']='guestroom';actor=self.ns['r13_stage_people']()[0];self.assertEqual(actor['height'],210)
 def test_home_comparison_keeps_original_progress_without_action_instructions(self):
  self.state['evidence']=['E01','E18']
  def original(selected):
   self.state['flags'].append('poc:letter_conflict');return 'original comparison'
  self.ns['_r13_daram_home_compare']=original
  result=self.ns['r13_compare_result'](['E01','E18']);self.assertIn('poc:letter_conflict',self.state['flags']);self.assertNotIn('보여',result);self.assertNotIn('물어보',result)
 def test_mother_discussion_changes_after_actual_reunion(self):
  self.state.update(day=10,mom_state='reunited',evidence=['M01']);text=' '.join(line for who,line in self.ns['r13_conversation_topic_lines']('home:daram:mother'));self.assertIn('이제 엄마 얼굴을 봤으니까',text);self.assertNotIn('엄마만 없는',text)
 def test_present_keeps_original_side_effects_and_authored_tool_reply(self):
  self.state['evidence']=['E01','E18','E03']
  calls=[]
  def original(person,key,identity=False):calls.append((person,key));return [('daram','authored tool reply')]
  self.ns['_r13_daram_home_present']=original
  before=copy.deepcopy(self.state);response=self.ns['r13_present']('daram','E18');self.assertEqual(calls,[('daram','E18')]);self.assertTrue(any(who=='daram' for who,line in response));self.assertEqual(self.state,before)
  self.state.update(tool_discoveries={'seam':{}},read_topics=['tool:seam']);self.assertEqual(self.ns['r13_present']('daram','E03'),[('daram','authored tool reply')])
if __name__=='__main__':unittest.main()
