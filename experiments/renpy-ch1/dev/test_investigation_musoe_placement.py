"""Pure source/geometry regression. No RenPy import or game execution."""
from pathlib import Path
import ast,textwrap,types,copy,unittest,hashlib
ROOT=Path(__file__).resolve().parents[1]
# Pure extraction of the checked-in init block; no RenPy import or SDK execution.
src=(ROOT/'game/systems/room13_spatial_contacts.rpy').read_text(encoding='utf-8')
# The inverse delta is independently pinned to exact b029ac21 source bytes below.
# This avoids a second checkout/base folder while retaining an exact scope guard.
DELTA='                elif location=="workshop" and r13_world_width()==1800 and person=="resident_musoe" and actor["pose"]=="job_inspect_old_tool":\n                    # Candidate visitor floor position; preserve approved source, pose and current stature.\n                    actor=r13_contact_geometry(actor,actor["pose"],"foot",(130,690),actor["height"],690)\n'
BASE_SHA256='e94811069937cc2a59849ceb3e3afda83cccca12acdfe7662ae0a85b4b1eae73'
old=src.replace(DELTA,'')
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
if __name__=='__main__':unittest.main()
