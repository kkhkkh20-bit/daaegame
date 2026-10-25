"""Actual Python staging and final schedule chains; no claim of renderer/save-engine QA."""
import ast, copy, io, json, pickle, re, textwrap, unittest
from pathlib import Path
from types import SimpleNamespace
import r13_timeline_env  # actual timeline constants
from qa_room13_rules import load_rules
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'game/systems/room13_life_groups.rpy'

def selected(env,filename,names):
    src=(ROOT/'game'/filename).read_text()
    for match in re.finditer(r'^init(?: -?\d+)? python:\n((?:[ \t].*\n|\n|#[^\n]*\n)*)',src,re.M):
        tree=ast.parse(textwrap.dedent(''.join(line for line in match.group(1).splitlines(True) if not line.startswith('#'))))
        tree.body=[n for n in tree.body if
            (isinstance(n,ast.FunctionDef) and n.name in names) or
            (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets))]
        exec(compile(tree,filename,'exec'),env)

def environment(group='workshop_pair',approved=True):
    env=load_rules();s=env['store'];s.r13_life_field_active=True
    env['R13_RESIDENTS']=env['ROOM13']['residents']
    env['R13_GREETING'].update({k:'' for k in env['R13_RESIDENTS']})
    selected(env,'room13_life.rpy',{'R13_WEEKLY_ROUTINES','r13_resident_where','r13_daylight'})
    selected(env,'systems/room13_new_places.rpy',{'R13_NEW_PLACE_DAYS','R13_NEW_PLACE_ROUTINES','R13_RAW_SLOT_PLACE','r13_raw_weekly_slot','r13_new_place_for','_r13_new_places_resident_where','r13_resident_where'})
    for f,alias,extra in [
        ('room13_gate_continuity.rpy','_r13_before_gate_where',[]),
        ('room13_home.rpy','_r13_home_where',['r13_home_with_daram']),
        ('systems/room13_livelihood_flow.rpy','_r13_life_where',[]),
        ('systems/room13_episodes.rpy','_r13_episode_where',[]),
        ('systems/room13_alibi.rpy','_r13_alibi_where',['R13_STORY_PINS']),
        ('systems/room13_ep2_kids.rpy','_r13_kd_where',[]),
        ('systems/room13_ep4_night13.rpy','_r13_nt_where',[]),
        ('systems/room13_story_continuity.rpy','_r13_continuity_where',['R13_DEATH_FLAGS'])]:
        selected(env,f,{alias,'r13_where',*extra})
    selected(env,'room13_acting.rpy',{'r13_visible_people'})
    selected(env,'room13_entry_window.rpy',{'r13_daram_waiting_at_gate','_r13_entry_visible_people','r13_visible_people'})
    selected(env,'systems/room13_event_offers.rpy',{'R13_EVENT_OFFERS','R13_OFFER_ACTORS','r13_offer_for_person','r13_offers_here','r13_person_action'})
    selected(env,'systems/room13_map_action27.rpy',{'r13_map27_geometry'})
    env['Return']=lambda value:value
    acting=json.loads((ROOT/'game/assets/room13-pixel-acting.json').read_text())
    for row in json.loads((ROOT/'game/assets/room13-map-action27.json').read_text())['rows']:
        acting.setdefault(row['person'],{})[row['pose']]=row['spec']
    layouts=json.loads((ROOT/'game/assets/room13-world-layout.json').read_text())
    env.update(R13_ACTING=acting,CAST=copy.deepcopy(acting),Transform=lambda *a,**k:a,Crop=lambda *a:a,R13_WORLD_LAYOUTS=layouts,
        r13_acting_spec=lambda who,pose:acting.get(who,{}).get(pose),
        r13_world_width=lambda:layouts[s.room13['location']]['width'])
    for loc in ('inn','school','workshop'):
        for key,rect in layouts[loc]['objects'].items():env['ROOM13']['objects'][loc][key]['rect']=rect
    env['renpy'].loadable=lambda p:(ROOT/'game'/p).exists()
    env['renpy'].image=lambda *a,**k:None
    actors=[];env['r13_stage_people']=lambda entry=False:actors
    block=SOURCE.read_text().split('init 181 python:\n',1)[1].split('\nscreen ',1)[0]
    exec(textwrap.dedent(block),env)
    row=next(r for r in env['R13_LIFE_GROUPS'] if r['id']==group)
    row['status']='approved' if approved else 'awaiting_live_review'
    s.room13.update(day=row['days'][0],period=row['periods'][0],location=row['location'],flags=['lodging','entry_corrected',*row['need_flags']],offers={})
    if not row.get('conditional_cast'):
        for i,m in enumerate(row['members']):
            actors.append(dict(person=m['person'],pose=m['replace_poses'][0],x=10+100*i,y=300,width=60,height=200,rect=[10+100*i,300,60,200],depth=500,occlusion=[],slot=None,contact='standing'))
    return env,row,actors

class LifeGroups(unittest.TestCase):
    def test_real_staging_chain_keeps_every_scheduled_actor_for_all_review_slots(self):
        from review_life_groups import stage_environment
        for key in ('workshop_pair','inn_mending','school_play'):
            e,row=stage_environment(key)
            e['r13_touch_ui']=lambda:False
            for day in row['days']:
                for period in row['periods']:
                    e['store'].room13.update(day=day,period=period)
                    before=copy.deepcopy(e['store'].room13)
                    solo=e['_r13_life_groups_stage']();result=e['r13_stage_people']()
                    self.assertTrue(e['r13_life_groups_here'](),(key,day,period))
                    self.assertEqual(len(result),len({a['person'] for a in result}))
                    self.assertTrue({a['person'] for a in solo}<={a['person'] for a in result})
                    self.assertEqual(before,e['store'].room13)
    def test_approved_child_source_hash_and_export_alpha_are_preserved(self):
        import hashlib
        from PIL import Image,ImageChops
        e,row,_=environment('school_play')
        for member in row['members']:
            spec=member['spec'];source=ROOT/'art/resident-life-groups-20261018/originals'/(member['person']+'-play-source.png')
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),spec['source_sha256'])
            with Image.open(source) as a,Image.open(ROOT/'game'/spec['file']) as b:
                self.assertEqual(a.size,b.size)
                self.assertIsNone(ImageChops.difference(a.getchannel('A'),b.getchannel('A')).getbbox())
    def test_cooperative_originals_and_shared_component_contact(self):
        import hashlib
        from PIL import Image
        from map27_pixel_derivative import validate_map_image
        source=ROOT/'art/cooperative-work-three-20261018'
        manifest=json.loads((source/'manifest.json').read_text())
        for row in manifest:
            original=source/row['file']
            self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(),row['sha256'])
            with Image.open(ROOT/'game/assets'/('room13-group-'+row['person_id']+'-cooperative.webp')) as image:
                validate_map_image(image.convert('RGBA'))
        e,row,_=environment('workshop_pair');actors=e['r13_stage_people']();contacts=[]
        for member in row['members']:
            actor=next(a for a in actors if a['person']==member['person']);spec=member['spec'];anchor=spec['anchors'][member['anchor']];scale=actor['height']/spec['crop'][3]
            contacts.append([actor['x']+anchor[0]*scale,actor['y']+anchor[1]*scale])
        self.assertLess(max(abs(a-b) for a,b in zip(*contacts)),1)
        e,row,_=environment('inn_mending');actor=next(a for a in e['r13_stage_people']() if a['person']=='resident_tori')
        self.assertTrue(actor['map27_occlusion'])
    def test_stale_child_and_invalid_choice_never_enter_adult_dialogue(self):
        e,row,_=environment('school_play');e['store'].room13['day']=10
        self.assertEqual(e['r13_person_action']('kid_kkam'),('life_child','kid_kkam'))
        self.assertEqual(e['r13_life_group_lines']('school_play','kid_kkam'),[])
        for value in (None,False,1,{},'life_group',('life_group',)):
            self.assertFalse(e['r13_life_choice_is_group'](value))
        self.assertTrue(e['r13_life_choice_is_group'](('life_group','school_play')))
        for tag in ('r13_ep_cut','r13_ep_book'):
            e,row,_=environment('school_play');e['renpy'].get_showing_tags=lambda:[tag]
            self.assertEqual(e['r13_stage_people'](),[])
    def test_pending_rows_remain_disabled(self):
        for key in ('workshop_pair','inn_mending','school_play'):
            e,row,a=environment(key,False)
            self.assertEqual(e['r13_stage_people'](),a)
            self.assertEqual(e['r13_life_groups_here'](),[])
            self.assertEqual(e['r13_life_group_lines'](key),[])
    def test_final_schedule_workshop_day2_day3_and_inn_day2_day3_day6(self):
        for key in ('workshop_pair','inn_mending'):
            e,row,a=environment(key)
            for day in row['days']:
                for period in row['periods']:
                    e['store'].room13.update(day=day,period=period)
                    for m in row['members']:
                        self.assertEqual(e['r13_where'](m['person']),row['location'])
                        self.assertIn(m['person'],e['r13_visible_people']())
                    self.assertEqual(len(e['r13_life_groups_here']()),1)
    def test_square_plan_is_rejected_by_actual_final_wrapper(self):
        e,_,_=environment('inn_mending')
        for day in (2,9):
            e['store'].room13.update(day=day,period=0,location='square')
            self.assertEqual(e['r13_where']('resident_tori'),'market')
            self.assertNotEqual(e['r13_where']('resident_tori'),e['r13_where']('resident_yeoni'))
            self.assertEqual(e['r13_life_groups_here'](),[])
    def test_missing_member_detention_event_pose_offer_and_final_visibility(self):
        for kind in ('absent','detained','offer','pose','visibility','where','missing_art','evening','entry','cut','meeting','forced'):
            with self.subTest(kind=kind):
                e,row,a=environment();s=e['store'];before=copy.deepcopy(a)
                if kind=='absent':a.pop()
                if kind=='detained':s.room13['flags'].append('tok_detained')
                if kind=='offer':s.room13['offers']['r13_ep4_accused']=dict(day=2,period=0,location='workshop')
                if kind=='pose':a[0]['pose']='event_toolbox'
                if kind=='visibility':e['r13_visible_people']=lambda:['buri']
                if kind=='where':e['r13_where']=lambda person:None
                if kind=='missing_art':e['renpy'].loadable=lambda p:False
                if kind=='evening':s.room13['period']=2
                if kind=='cut':s.r13_cg_active=True
                if kind=='meeting':s.r13_meeting_active=True
                if kind=='forced':s.r13_life_field_active=False
                expected=copy.deepcopy(a)
                self.assertEqual(e['r13_stage_people'](kind=='entry'),expected)
                self.assertEqual(a,expected)
                if kind!='entry':self.assertEqual(e['r13_life_group_lines'](row['id']),[])
        e,row,a=environment();e['store'].room13['flags']+=['tok_detained','tok_cleared']
        self.assertEqual(len(e['r13_life_groups_here']()),1)
    def test_geometry_contacts_masks_and_old_cache_are_not_mutated(self):
        e,row,a=environment();before=copy.deepcopy(a)
        out=e['r13_stage_people']();self.assertEqual(a,before)
        for member in row['members']:
            actor=next(x for x in out if x['person']==member['person'])
            spec=e['r13_acting_spec'](member['person'],member['pose'])
            point=spec.get(member['anchor'],spec.get('anchors',{}).get(member['anchor']))
            scale=member['height']/spec['crop'][3]
            for axis,name in enumerate(('x','y')):self.assertAlmostEqual(actor[name]+point[axis]*scale,member['target'][axis],delta=.51)
            self.assertEqual(actor['map27_occlusion'],[e['R13_WORLD_LAYOUTS']['workshop']['occlusion']])
        self.assertTrue(next(x for x in out if x['person']=='resident_tok')['map27_keepouts'])
        e['store'].room13['flags'].append('tok_detained')
        self.assertEqual(e['r13_stage_people'](),before)
        e['store'].room13['flags'].remove('tok_detained')
        self.assertEqual(e['r13_stage_people'](),out)
    def test_children_narrow_presence_and_all_negative_states(self):
        e,row,a=environment('school_play')
        self.assertEqual({x['person'] for x in e['r13_stage_people']()},{m['person'] for m in row['members']})
        self.assertTrue(all(m['person'] not in e['R13_RESIDENTS'] and m['person'] not in e['R13_WEEKLY_ROUTINES'] for m in row['members']))
        for flag in row['need_flags']:
            e,row,a=environment('school_play');e['store'].room13['flags'].remove(flag)
            self.assertEqual(e['r13_stage_people'](),[])
        for flag in row['not_flags']:
            e,row,a=environment('school_play');e['store'].room13['flags'].append(flag)
            self.assertEqual(e['r13_stage_people'](),[])
        for day in (1,7,10,11,14):
            e,row,a=environment('school_play');e['store'].room13['day']=day
            self.assertEqual(e['r13_stage_people'](),[])
        for day in (8,9):
            for period in (0,1):
                e,row,a=environment('school_play');e['store'].room13.update(day=day,period=period)
                self.assertEqual(len(e['r13_stage_people']()),3)
        for attr in ('r13_cg_active','r13_meeting_active','r13_aftermath_active','r13_ending_story_active'):
            e,_,_=environment('school_play');setattr(e['store'],attr,True)
            self.assertEqual(e['r13_stage_people'](),[])
    def test_children_fallback_keeps_resident_and_stove_clicks_clear(self):
        e,row,a=environment('school_play');child=e['r13_stage_people']()[0]
        for person in ('resident_nubi','kid_kkam'):
            a[:]=[dict(child,person=person)];before=copy.deepcopy(a)
            self.assertEqual(e['r13_stage_people'](),before)
        a.clear()
        row['members'][0]['target']=[920,550]
        self.assertEqual(e['r13_stage_people'](),[])
    def test_repeated_individual_group_cancel_move_and_serialized_state_reads(self):
        for key in ('workshop_pair','inn_mending','school_play'):
            e,row,a=environment(key);s=e['store'];before=copy.deepcopy(s.room13)
            for repeat in range(3):
                self.assertEqual(e['r13_life_group_lines'](key),row['lines'])
                for m in row['members']:
                    p=m['person'];action=e['r13_person_action'](p)
                    if row.get('conditional_cast'):
                        self.assertEqual(action,('life_child',p));self.assertEqual(e['r13_life_group_lines'](key,p),[(p,row['individual_lines'][p])]+row['lines'])
                    else:self.assertEqual(action,('person',p))
                self.assertEqual(e['r13_person_action']('buri',True),('person','buri'))
                s.room13=pickle.loads(pickle.dumps(s.room13))  # Python data only, not engine save QA
                self.assertEqual(s.room13,before)
            s.room13['location']='square';self.assertEqual(e['r13_life_group_lines'](key),[])
            s.room13=copy.deepcopy(before);self.assertEqual(e['r13_life_group_lines'](key),row['lines'])
    def test_child_event_dispatch_wins_outside_active_play_group(self):
        e,row,_=environment('school_play')
        p=row['members'][0]['person'];before=copy.deepcopy(e['store'].room13)
        self.assertEqual(e['r13_person_action'](p),('life_child',p))
        self.assertEqual(e['r13_life_group_lines']('school_play',p)[0][0],p)
        self.assertEqual(len(e['r13_life_group_lines']('school_play',p)),5)
        e['_r13_life_groups_person_action']=lambda person,entry=False:('authored_event',person)
        e['store'].r13_life_field_active=False
        self.assertEqual(e['r13_person_action'](p),('authored_event',p))
        self.assertEqual(e['r13_life_group_lines']('school_play',p),[])
        self.assertEqual(e['store'].room13,before)
        e['store'].r13_life_field_active=True
        e['_r13_life_groups_stage']=lambda entry=False:[dict(person=p)]
        self.assertEqual(e['r13_person_action'](p),('authored_event',p))

    def test_no_story_api_or_event_reentry_and_explicit_return_sites(self):
        src=SOURCE.read_text();label=src.split('label r13_life_group_talk',1)[1].split('label r13_life_field_person_dispatch',1)[0]
        for token in ('call r13_lines','call r13_talk','r13_flag(','r13_tick(','r13_grant(','r13_note_encounter(','r13_st_kkomi_class','r13_wf_ruins'):self.assertNotIn(token,label)
        flow=(ROOT/'game/room13.rpy').read_text()
        self.assertIn('from r13_life_group_field_return',src)
        self.assertIn('from r13_life_child_field_return',src)
        self.assertIn('focus_mask r13_actor_hit_mask(actor)',(ROOT/'game/room13_screens.rpy').read_text())

if __name__=='__main__':unittest.main()
