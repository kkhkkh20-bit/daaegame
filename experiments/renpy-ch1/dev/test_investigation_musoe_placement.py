"""Pure source/geometry regression. No RenPy import or game execution."""
from pathlib import Path
import ast,textwrap,types,copy,unittest,hashlib
ROOT=Path(__file__).resolve().parents[1]
# Pure extraction of the checked-in init block; no RenPy import or SDK execution.
src=(ROOT/'game/systems/room13_spatial_contacts.rpy').read_text(encoding='utf-8')
# The inverse delta is independently pinned to exact b029ac21 source bytes below.
# This avoids a second checkout/base folder while retaining an exact scope guard.
DELTA='                elif location=="workshop" and r13_world_width()==1800 and person=="resident_musoe" and actor["pose"]=="job_inspect_old_tool":\n                    # Candidate visitor floor position; preserve approved source, pose and current stature.\n                    actor=r13_contact_geometry(actor,actor["pose"],"foot",(130,690),actor["height"],690)\n'
BASE_SHA256='1d67bba39d261be24cddc63f947f632a1e189e1034b9115f3c92c5e9a42f22c6'
# PR17's independently reviewed sofa block is a separate, byte-exact delta.
# Never update BASE_SHA256 to accept unrelated production changes.
SOFA_DELTA='                elif location=="inn" and r13_world_width()==1920 and (person,actor["pose"]) in (("resident_nubi","map27_in_1"),("resident_tosil","living_thermos")):\n                    # LOCAL CANDIDATE: inner lounge floor, in front of rear bench.\n                    # Preserve presence, approved sources, pose and ordinary event priority.\n                    target,height=((420,535),226) if person=="resident_nubi" else ((535,535),215)\n                    actor=r13_contact_geometry(actor,actor["pose"],"foot",target,height,target[1])\n                    # Foreground furniture also masks the native alpha hit silhouette.\n                    actor["map27_occlusion"]=[\n                        [(475,446),(502,446),(503,450),(512,450),(516,456),(515,469),(508,474),(501,473),(501,482),(480,482),(475,477)],\n                        [(385,445),(400,439),(405,433),(414,432),(414,426),(424,426),(426,433),(443,438),(449,450),(449,470),(438,480),(413,480),(402,473),(398,458),(385,457)],\n                        [(336,477),(409,456),(502,467),(546,477),(546,498),(529,510),(529,591),(491,594),(489,523),(430,519),(430,564),(413,564),(413,513),(338,500)],\n                        [(552,461),(619,482),(655,413),(687,381),(756,374),(783,393),(778,557),(749,580),(748,612),(717,620),(714,585),(588,552),(588,591),(563,590)],\n                    ]\n                    actor["map27_keepouts"]=[]\n'
SOFA_SHA256='ea4c06ea86e989c8960f47f1e739ba8535ce1d8f873d1db5b620677d61766c58'
def restore_known_deltas(source):
 if len(SOFA_DELTA.splitlines())!=13 or hashlib.sha256(SOFA_DELTA.encode('utf-8')).hexdigest()!=SOFA_SHA256:
  raise ValueError('Approved sofa block constant changed; review required')
 if source.count(SOFA_DELTA)!=1:
  raise ValueError('Expected exactly one byte-exact approved sofa block')
 without_sofa=source.replace(SOFA_DELTA,'',1)
 if without_sofa.count(DELTA)!=1:
  raise ValueError('Expected exactly one unchanged Musoe delta')
 baseline=without_sofa.replace(DELTA,'',1)
 if hashlib.sha256(baseline.encode('utf-8')).hexdigest()!=BASE_SHA256:
  raise ValueError('Unreviewed source remains outside exact sofa and Musoe deltas')
 return baseline
old=restore_known_deltas(src)
def tree(s):return ast.parse(textwrap.dedent(s.split('init 179 python:\n')[1]))
def stage(source,actor,location='workshop',width=1800,offer=False):
 t=tree(source);defs=[n for n in t.body if isinstance(n,ast.FunctionDef)]
 env=dict(store=types.SimpleNamespace(room13={'location':location}),_r13_contact_stage=lambda entry:[copy.deepcopy(actor)],r13_offer_for_person=lambda person:offer,r13_world_width=lambda:width,R13_HOME_CONTACTS={},R13_SQUARE_LEVELS={},r13_acting_spec=lambda *a:dict(foot=[437.9,1517],contact='self-contained'),r13_actor_geometry=lambda *a:(805,1518))
 exec(compile(ast.Module(body=defs,type_ignores=[]),'contacts','exec'),env)
 return env['r13_stage_people']()[0]
def actor(**kw):
 a=dict(person='resident_musoe',pose='job_inspect_old_tool',x=1619,y=425,width=148,height=280,rect=[1619,425,148,280],depth=705,slot=None,occlusion=[],map27_occlusion=[],map27_keepouts=[],contact='self-contained',activity='authored activity');a.update(kw);return a
class Tests(unittest.TestCase):
 def test_exact_job_geometry(self):
  a=stage(src,actor());self.assertEqual(a['rect'],[49,410,148,280]);self.assertEqual(a['depth'],690);self.assertEqual(a['height'],280);self.assertEqual(a['activity'],'authored activity')
 def test_offer_unchanged(self):self.assertEqual(stage(src,actor(),offer=True),stage(old,actor(),offer=True))
 def test_other_location_unchanged(self):self.assertEqual(stage(src,actor(),location='post'),stage(old,actor(),location='post'))
 def test_other_width_unchanged(self):self.assertEqual(stage(src,actor(),width=1280),stage(old,actor(),width=1280))
 def test_other_person_unchanged(self):self.assertEqual(stage(src,actor(person='resident_tok')),stage(old,actor(person='resident_tok')))
 def test_neutral_unchanged(self):self.assertEqual(stage(src,actor(pose='neutral')),stage(old,actor(pose='neutral')))
 def test_other_pose_unchanged(self):self.assertEqual(stage(src,actor(pose='living_foldmap')),stage(old,actor(pose='living_foldmap')))
 def test_function_map_unchanged(self):
  sig=lambda s:[(n.name,n.lineno) for n in tree(s).body if isinstance(n,ast.FunctionDef)]
  self.assertEqual(sig(src),sig(old))
 def test_only_one_branch_added(self):
  self.assertEqual(src.count(DELTA),1)
  self.assertEqual(hashlib.sha256(old.encode('utf-8')).hexdigest(),BASE_SHA256,
                   'Non-Musoe source changed from b029ac21; review and update scope guard explicitly.')
 def test_sofa_delta_is_exactly_pinned(self):
  self.assertEqual(len(SOFA_DELTA.splitlines()),13)
  self.assertEqual(hashlib.sha256(SOFA_DELTA.encode('utf-8')).hexdigest(),SOFA_SHA256)
  self.assertEqual(src.count(SOFA_DELTA),1)
 def test_scope_rejects_changed_sofa_geometry(self):
  for before,after in [('((535,535),215)','((536,535),215)'),('(475,446)','(476,446)'),('resident_tosil','resident_other')]:
   changed=SOFA_DELTA.replace(before,after,1)
   self.assertNotEqual(changed,SOFA_DELTA)
   with self.assertRaises(ValueError):restore_known_deltas(src.replace(SOFA_DELTA,changed,1))
 def test_scope_rejects_missing_or_duplicate_sofa(self):
  for replacement in ('',SOFA_DELTA+SOFA_DELTA):
   with self.assertRaises(ValueError):restore_known_deltas(src.replace(SOFA_DELTA,replacement,1))
 def test_scope_rejects_changed_musoe(self):
  with self.assertRaises(ValueError):restore_known_deltas(src.replace('(130,690)','(131,690)',1))
 def test_scope_rejects_unrelated_source(self):
  with self.assertRaises(ValueError):restore_known_deltas(src+'# unreviewed addition\n')
if __name__=='__main__':unittest.main()
