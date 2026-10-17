import re,textwrap,types,unittest,json
from pathlib import Path
class SaveUITests(unittest.TestCase):
 def setUp(self):
  self.files={};self.deleted=[]
  self.persistent=types.SimpleNamespace(_file_page='1',room13_read=['kept'],room13_knowledge=['E01'],room13_endings=['A'],room13_large_text=True)
  self.env=dict(store=types.SimpleNamespace(room13_mode=True,room13={'campaign_id':'room13_v1','story_revision':'current','visual_revision':'pixel-b-front-v3','day':1}),ROOM13={'story_revision':'current'},persistent=self.persistent,config=types.SimpleNamespace(save_json_callbacks=[]))
  self.env['renpy']=types.SimpleNamespace(list_saved_games=lambda regexp,fast:[s for s in self.files if re.match(regexp,s)],slot_json=lambda s:self.files.get(s),unlink_save=self.deleted.append,restart_interaction=lambda:None)
  source=(Path(__file__).resolve().parents[1]/'game/room13_save_ui.rpy').read_text().split('init 100 python:\n')[1].split('\nscreen ')[0];exec(textwrap.dedent(source),self.env)
 def test_new_characters_do_not_disable_continue_for_new_saves(self):
  root=Path(__file__).resolve().parents[1]
  portraits=json.loads((root/'game/assets/room13-portraits.json').read_text())
  self.env['store'].R13_PORTRAITS=portraits
  assignment=next(line.strip() for line in (root/'game/room13_week2_rules.rpy').read_text().splitlines() if line.strip().startswith('target_visual_revision='))
  exec(assignment,self.env)
  self.env['store'].room13['visual_revision']=self.env['target_visual_revision']
  self.assertEqual(self.env['r13_save_status'](self.metadata()),'compatible')
 def metadata(self,ctime=10):
  m={'_version':'0.17.1-dev','_ctime':ctime};self.env['r13_save_metadata'](m);return m
 def test_continue_selects_only_compatible_contract(self):
  self.files={'1-1':self.metadata(10),'auto-1':{'_version':'0.15.8-dev','_ctime':999},'2-2':self.metadata(20),'_reload-1':self.metadata(9999)}
  self.assertEqual(self.env['r13_continue_slot'](),'2-2')
 def test_unknown_and_incompatible_are_distinct(self):
  self.assertEqual(self.env['r13_save_status']({'_version':'0.17.0-dev'}),'unknown')
  m=self.metadata();m['r13_story']='previous';self.assertEqual(self.env['r13_save_status'](m),'incompatible')
  self.files={'1-1':m};self.assertIsNone(self.env['r13_continue_slot']())
 def test_no_saves_is_safe(self):self.assertIsNone(self.env['r13_continue_slot']())
 def test_cleanup_excludes_persistent_and_internal_slots(self):
  self.files={'1-1':self.metadata(),'auto-1':{'_version':'0.15'},'quick-1':{'_version':'0.16'},'_reload-1':{'_version':'0.14'},'persistent':{}}
  before=vars(self.persistent).copy();old=self.env['r13_cleanup_slots']('old');self.assertEqual(set(old),{'auto-1','quick-1'})
  self.env['r13_delete_confirmed_saves'](old,{slot:self.files[slot].get('_ctime') for slot in old});self.assertEqual(set(self.deleted),set(old));self.assertEqual(vars(self.persistent),before)
  self.assertNotIn('_reload-1',self.env['r13_cleanup_slots']('all'))
 def test_changed_slot_is_not_deleted(self):
  self.files={'1-1':self.metadata(20)};self.env['r13_delete_confirmed_saves'](('1-1',),{'1-1':10});self.assertEqual(self.deleted,[])
 def test_metadata_does_not_change_progress(self):
  before=self.env['store'].room13.copy();self.metadata();self.assertEqual(self.env['store'].room13,before)
if __name__=='__main__':unittest.main()
