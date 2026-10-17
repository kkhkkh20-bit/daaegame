"""Dormant map-placement adapter: guard conditions, anchors and shared draw/pick masks."""
import io,json,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def environment(rows=None):
    actor=dict(person='resident_sling',pose='activity',x=5,y=6,width=30,height=40,rect=[5,6,30,40],depth=46,occlusion=[])
    env=dict(json=json,renpy=types.SimpleNamespace(file=lambda p:io.StringIO((ROOT/'game'/p).read_text()),loadable=lambda p:True),
        r13_stage_people=lambda entry=False:[actor],r13_staged_visible_art=lambda a,still=False:('original',a['person'],still),
        store=types.SimpleNamespace(room13=dict(location='post',period=0,day=2,flags=['lodging'])),
        r13_world_width=lambda:2160,r13_daylight=lambda:'morning',r13_offer_for_person=lambda who:None,
        R13_ACTING={},R13FurnitureMask=lambda poly,**kw:('mask',poly,kw),AlphaMask=lambda a,m,**kw:('alpha',a,m,kw))
    src=(ROOT/'game/systems/room13_map_action27.rpy').read_text().split('init 178 python:\n',1)[1]
    exec(textwrap.dedent(src),env)
    if rows is not None:env['R13_MAP_ACTION27']['rows']=rows
    return env,actor

def approved():
    return dict(status='approved',person='resident_sling',location='post',periods=[0,1,2],replace_poses=['activity'],pose='new_map_pose',
        variants={'morning':dict(world_width=2160,render_height=200,anchor='parcel',target=[1450,548],occlusion=[[[1100,560],[2160,470],[2160,720],[1100,720]]])})

class MapAction27(unittest.TestCase):
    def test_registry_is_dormant_and_keeps_actor_identity(self):
        env,actor=environment();self.assertEqual(env['R13_MAP_ACTION27']['rows'],[])
        self.assertIs(env['r13_stage_people']()[0],actor)
        self.assertEqual(env['r13_staged_visible_art'](actor,True),('original','resident_sling',True))
    def test_missing_art_and_missing_variant_do_not_fallback(self):
        row=approved();env,actor=environment([row]);self.assertIs(env['r13_stage_people']()[0],actor)
        select=env['r13_map27_variant'];state=env['store'].room13
        self.assertIsNone(select(row,actor,state,'afternoon',1280,False))
        self.assertIsNone(select(row,actor,state,'morning',1280,False))
        row['status']='awaiting_art';self.assertIsNone(select(row,actor,state,'morning',2160,False))
    def test_event_map9_solbang_and_state_guards(self):
        row=approved();env,actor=environment();select=env['r13_map27_variant'];s=env['store'].room13
        self.assertIsNone(select(row,actor,s,'morning',2160,True))
        for pose in ['event_steam','map9_letters_waiting','work_herb_bundle']:
            self.assertIsNone(select(row,dict(actor,pose=pose),s,'morning',2160,False))
        row.update(need_flags=['allowed'],not_flags=['dead'],min_day=3,max_day=10)
        self.assertIsNone(select(row,actor,s,'morning',2160,False))
        self.assertIsNone(select(row,actor,dict(s,day=4,flags=['allowed','dead']),'morning',2160,False))
        self.assertIsNotNone(select(row,actor,dict(s,day=4,flags=['allowed']),'morning',2160,False))
        # The wrapper cannot reintroduce dead/detained/off-schedule people removed upstream.
        env['_r13_map27_stage']=lambda entry=False:[];env['R13_MAP_ACTION27']['rows']=[row]
        self.assertEqual(env['r13_stage_people'](),[])
    def test_uniform_contact_geometry_and_no_second_perspective(self):
        env,actor=environment();v=approved()['variants']['morning']
        spec=dict(crop=[10,20,300,768],anchors={'parcel':[150,384],'hand':[100,384]},foreground_parts=[[[100,300],[200,300],[200,384],[100,384]]])
        out=env['r13_map27_geometry'](actor,spec,v,2160)
        self.assertEqual(out['height'],200);self.assertEqual(out['width'],78)
        self.assertAlmostEqual(out['x']+150*200/768,1450,delta=.5)
        self.assertAlmostEqual(out['y']+384*200/768,548,delta=.5)
        self.assertEqual(out['occlusion'],[]);self.assertEqual(len(out['map27_keepouts']),1)
        with self.assertRaises(ValueError):env['r13_map27_geometry'](actor,spec,dict(v,secondary_targets={'hand':[0,0]}),2160)
        self.assertEqual(actor['height'],40)
    def test_drawing_and_picker_use_same_composed_mask(self):
        env,actor=environment();actor.update(map27_occlusion=[[[0,0],[20,0],[20,30]]],map27_keepouts=[[[5,5],[10,5],[10,10]]])
        visible=env['r13_staged_visible_art'](actor,True)
        self.assertEqual(visible[0],'alpha');self.assertEqual(visible[2][0],'alpha')
        self.assertTrue(visible[2][3]['invert'])
        # Execute the real picker, not a duplicate implementation.
        src=(ROOT/'game/room13_acting.rpy').read_text();start=src.index('    def r13_actor_hit_mask(actor):');end=src.index('    def r13_actor_face',start)
        env['Crop']=lambda rect,art:(rect,art);exec(textwrap.dedent(src[start:end]),env)
        self.assertEqual(env['r13_actor_hit_mask'](actor)[1],visible)
    def test_runtime_has_no_schedule_or_dialogue_mutation(self):
        src=(ROOT/'game/systems/room13_map_action27.rpy').read_text()
        for name in ['def r13_where','def r13_resident_where','def r13_speaker','renpy.image(']:self.assertNotIn(name,src)

if __name__=='__main__':unittest.main()
