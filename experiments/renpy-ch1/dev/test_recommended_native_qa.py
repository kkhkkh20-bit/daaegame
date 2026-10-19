import unittest
from test_recommended_integration import G,f,ep1
class NativeQaIsolation(unittest.TestCase):
 def test_per_state_qa_switch_never_promotes_production_flags(self):
  s=ep1();self.assertFalse(f('piko_geometry_ready',s));self.assertFalse(f('e3_geometry_ready',s))
  s['qa_native_gates']={'piko':True,'e3':True}
  self.assertFalse(f('piko_geometry_ready',s));self.assertFalse(f('e3_geometry_ready',s))
  s['qa_fixture']='native_geometry_probe_v1'
  self.assertTrue(f('piko_geometry_ready',s));self.assertTrue(f('e3_geometry_ready',s))
  self.assertFalse(G['r13_rec_piko_contact_art_verified']);self.assertFalse(G['r13_rec_e3_geometry_art_verified'])
  self.assertFalse(f('piko_geometry_ready',f('new_state')))
 def test_isolated_qa_allows_actual_final_piko_input(self):
  s=ep1();s.update(qa_fixture='native_geometry_probe_v1',qa_native_gates={'piko':True,'e3':True})
  s=f('piko_hear_defense',s);s=f('apply',s,'contact_match')
  s,_,ok=f('present',s,'container')
  self.assertTrue(ok);self.assertEqual(s['verdict'],'direct_removal')
 def test_qa_save_reload_is_confirmed_but_excluded_from_continue(self):
  import types
  from pathlib import Path
  p=Path(__file__).resolve().parents[1]/'game/systems/room13_recommended_story.rpy'
  lines=p.read_text().split('init 920 python:\n',1)[1].split('\nscreen ',1)[0].splitlines()
  body='\n'.join(line[4:] if line.startswith('    ') else line for line in lines)
  data={'qa':dict(r13_campaign='room13_recommended_qa_v1',r13_recommended_revision=G['r13_rec_revision'],_ctime=20),'normal':dict(r13_campaign='room13_recommended_v1',r13_recommended_revision=G['r13_rec_revision'],_ctime=10)}
  st=types.SimpleNamespace(r13_recommended=dict(revision=G['r13_rec_revision'],episode=1),room13=dict(campaign_id='room13_recommended_qa_v1'))
  ns=dict(store=st,config=types.SimpleNamespace(save_json_callbacks=[]),r13_rec_revision=G['r13_rec_revision'],r13_save_status=lambda d:'incompatible',r13_save_caption=lambda d:'legacy',r13_load_action=lambda slot:('legacy',slot),r13_save_slots=lambda:list(data),renpy=types.SimpleNamespace(slot_json=lambda slot:data[slot]),Confirm=lambda text,action:('confirm',text,action),FileLoad=lambda *a,**k:('load',a,k))
  import textwrap
  legacy=(p.parents[1]/'room13_save_ui.rpy').read_text()
  legacy_continue=legacy.split('    def r13_continue_slot():',1)[1].split('\n    def ',1)[0]
  exec('def r13_continue_slot():\n'+textwrap.indent(textwrap.dedent(legacy_continue).strip(),'    '),ns)
  exec(body,ns)
  self.assertEqual(ns['r13_save_status'](data['qa']),'compatible')
  self.assertEqual(ns['r13_continue_slot'](),'normal')
  saved_normal=data.pop('normal')
  self.assertIsNone(ns['r13_continue_slot']())
  data['normal']=saved_normal
  data['normal']['_ctime']=30
  self.assertEqual(ns['r13_continue_slot'](),'normal')
  self.assertEqual(ns['r13_load_action']('qa')[0],'confirm')
  self.assertEqual(ns['r13_load_action']('normal'),('legacy','normal'))
  metadata={};ns['r13_rec_save_metadata'](metadata)
  self.assertEqual(metadata['r13_recommended_revision'],G['r13_rec_revision'])
 def test_fresh_qa_clock_and_cues_reset_but_reentry_does_not(self):
  from pathlib import Path
  root=Path(__file__).resolve().parents[1]
  source=(root/'game/systems/room13_recommended_native_qa.rpy').read_text()
  self.assertIn("room13['day'] = r13_recommended['day']",source)
  self.assertIn('r13_rec_stage_memory = {}',source)
  ui=(root/'dev/recommended_ep23_ui.rpy').read_text()
  at=ui.index('r13_rec_e3_privacy(r13_recommended, True)')
  self.assertLess(at,ui.index("'recommended:e3:child-testimony'"))
 def test_shortcut_cannot_open_legacy_records_in_recommended_campaign(self):
  import types
  from test_recommended_art import init_body,R
  calls=[];screens=set()
  st=types.SimpleNamespace(room13={'campaign_id':'room13_recommended_v1'},r13_recommended={'day':1})
  ns=dict(store=st,r13_shortcut_records=lambda:calls.append('legacy'),renpy=types.SimpleNamespace(get_screen=lambda n:n in screens,call_in_new_context=lambda label:calls.append(label)))
  exec(init_body(R/'game/systems/room13_recommended_shortcuts.rpy'),ns)
  ns['r13_shortcut_records']();self.assertEqual(calls,['r13_rec_stage_notebook'])
  screens.add('r13_rec_stage_choice');ns['r13_shortcut_records']();self.assertEqual(len(calls),1)
  st.room13['campaign_id']='room13_v1';ns['r13_shortcut_records']();self.assertEqual(calls[-1],'legacy')
