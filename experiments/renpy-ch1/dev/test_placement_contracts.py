#!/usr/bin/env python3
"""Source-only contract tests. Run from any cwd. This is NOT Ren'Py/native screenshot QA."""
import collections
import copy
import io
import json
from pathlib import Path
import textwrap
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
RPY = ROOT / 'game/systems/room13_placement_contracts.rpy'
REGISTRY = ROOT / 'game/assets/room13-placement-contracts.json'
FIXTURE = Path(__file__).parent / 'fixtures/placement-contract-baseline.json'
SOURCE = RPY.read_text()
CORE = textwrap.dedent(SOURCE.split('init 183 python:\n', 1)[1].split('\ninit 184 python:', 1)[0])
ADAPTER = textwrap.dedent(SOURCE.split('init 184 python:\n', 1)[1])
E = {}; exec(compile(CORE, str(RPY)+':init183', 'exec'), E)
F = json.loads(FIXTURE.read_text())


class Rig:
    def __init__(self, key='2/0/inn'):
        self.registry = json.loads(REGISTRY.read_text())
        self.specs = copy.deepcopy(F['specs'])
        self.actors = copy.deepcopy(F['actors'].get(key, []))
        d,p,loc = key.split('/')
        self.state = dict(copy.deepcopy(F['profile']), day=int(d), period=int(p), location=loc)
        self.variant = next((v for v in self.registry['background_variants'].values() if v['location']==loc and int(p) in v['periods']), None)
        self.context = {} if self.variant is None else dict(world_size=self.registry['geometries'][self.variant['geometry']]['world_size'], background=copy.deepcopy(self.variant['background']))
        self.blobs = {a['spec']['file']:a['git_blob'] for a in self.registry['assets'].values()}
        self.blobs.update({v['background']['file']:v['git_blob'] for v in self.registry['background_variants'].values()})
    def spec(self,p,q): return self.specs.get(p,{}).get(q)
    def resolve(self, enabled=True):
        return E['r13_pc_resolve'](self.actors,self.state,self.registry,self.context,self.spec,lambda f:f in self.blobs,self.blobs.get,enabled)
    def slot(self, name='laundry.floor'):
        return self.registry['geometries'][self.variant['geometry']]['slots'][name]
    def binding(self, id='inn.morning.nubi'):
        return next(b for b in self.registry['bindings'] if b['id']==id)


class PlacementContractTests(unittest.TestCase):
    def fallback(self,rig,code):
        before=copy.deepcopy(rig.actors);out,report=rig.resolve()
        self.assertIs(out,rig.actors);self.assertEqual(before,rig.actors)
        self.assertEqual(report['bypass'],'transaction_fallback');self.assertTrue(any(code in x for x in report['errors']),report)
    def test_default_off_882_states_no_dependencies_or_mutation(self):
        def denied(*args): raise AssertionError('disabled adapter touched dependency')
        seen=0;occurrences=0
        for state in F['states']:
            key='{day}/{period}/{location}'.format(**state);a=F['actors'].get(key,[]);before=copy.deepcopy(a)
            out,report=E['r13_pc_resolve'](a,state,{}, {},denied,denied,denied,False)
            self.assertIs(out,a);self.assertEqual(a,before);self.assertEqual(report['bypass'],'disabled');seen+=1;occurrences+=len(a)
        self.assertEqual((seen,occurrences),(882,1520))
    def test_enabled_882_states_replays_geometry_contact_and_masks(self):
        counts=collections.Counter();bindings=collections.Counter();changes=[]
        fields=('person','pose','x','y','width','height','rect','depth','contact','slot','occlusion','map27_occlusion','map27_keepouts')
        for state in F['states']:
            key='{day}/{period}/{location}'.format(**state);r=Rig(key);before=copy.deepcopy(r.actors);out,report=r.resolve()
            self.assertFalse(report['errors'],(key,report));self.assertEqual(before,r.actors)
            counts[report['bypass'] or 'applied']+=1;bindings.update(report['applied'])
            self.assertEqual([a['person'] for a in before],[a['person'] for a in out])
            for a,b in zip(before,out):
                for k in fields:
                    self.assertEqual(E['r13_pc_normalized'](a.get(k,[])),E['r13_pc_normalized'](b.get(k,[])),(key,a['person'],k))
        self.assertEqual(dict(counts),{'unmigrated_location':798,'applied':52,'no_eligible_binding':32})
        self.assertEqual(set(bindings),{b['id'] for b in Rig().registry['bindings']})
    def test_pose_swap_changes_one_binding_not_coordinates(self):
        r=Rig('2/1/post');geometry=copy.deepcopy(r.registry['geometries']);r.binding('post.afternoon.seryeon')['asset']='seryeon.chair_listen'
        out,report=r.resolve();self.assertFalse(report['errors'],report);a=next(a for a in out if a['person']=='seryeon')
        self.assertEqual(a['pose'],'chair_listen');self.assertEqual(geometry,r.registry['geometries'])
        spec=r.spec('seryeon','chair_listen');scale=108/(spec['foot'][1]-spec['seat'][1])
        self.assertLess(abs(a['x']+spec['seat'][0]*scale-175),1);self.assertLess(abs(a['y']+spec['seat'][1]*scale-562),1)
        self.assertLess(abs(a['y']+spec['foot'][1]*scale-670),1);self.assertEqual(a['depth'],674)
        self.assertEqual(a['activity'],spec['action_ko'])
    def test_new_actor_binding_only_uses_present_roster(self):
        r=Rig();r.binding()['actor']='resident_sling';r.binding()['asset']='sling.parcel'
        out,report=r.resolve();self.assertIs(out,r.actors);self.assertEqual(report['bypass'],'no_eligible_binding')
    def test_missing_exact_pose_no_neutral_fallback(self):
        r=Rig();r.registry['assets']['nubi.legacy_laundry']['pose']='missing';self.fallback(r,'MISSING_EXACT_POSE')
    def test_missing_asset(self):
        r=Rig();del r.blobs[r.registry['assets']['nubi.legacy_laundry']['spec']['file']];self.fallback(r,'MISSING_ASSET')
    def test_asset_digest(self):
        r=Rig();r.blobs[r.registry['assets']['nubi.legacy_laundry']['spec']['file']]='bad';self.fallback(r,'ASSET_DIGEST_MISMATCH')
    def test_background_digest(self):
        r=Rig();r.blobs[r.variant['background']['file']]='bad';self.fallback(r,'BACKGROUND_DIGEST_MISMATCH')
    def test_native_detail_render_path_is_guarded(self):
        r=Rig();r.specs['resident_nubi']['map27_in_1']['native_detail']=True;self.fallback(r,'STALE_POSE_CONTRACT')
    def test_crop_drift(self):
        r=Rig();r.specs['resident_nubi']['map27_in_1']['crop'][2]-=1;self.fallback(r,'STALE_POSE_CONTRACT')
    def test_invalid_padding(self):
        r=Rig();r.registry['assets']['nubi.legacy_laundry']['alpha_bounds']=[0,0,1000,1000];self.fallback(r,'INVALID_INTRINSIC_BOUNDS')
    def test_source_canvas_bounds(self):
        r=Rig();r.registry['assets']['nubi.legacy_laundry']['source_size']=[100,100];self.fallback(r,'INVALID_INTRINSIC_BOUNDS')
    def test_missing_contact_anchor(self):
        r=Rig();r.registry['assets']['nubi.legacy_laundry']['anchor_map']['floor']='seat';self.fallback(r,'MISSING_CONTACT_ANCHOR')
    def test_contact_mismatch_not_squashed(self):
        r=Rig();r.slot()['contacts']=['background_chair'];self.fallback(r,'INCOMPATIBLE_CONTACT')
    def test_facing_mismatch_not_mirrored(self):
        r=Rig();r.slot()['facing']=['right'];self.fallback(r,'INCOMPATIBLE_FACING')
    def test_negative_scale(self):
        r=Rig();r.slot()['scale']['pixels']=-1;self.fallback(r,'INVALID_SCALE')
    def test_no_nonuniform_stretch_mode(self):
        r=Rig();r.slot()['scale']={'kind':'width_and_height','pixels':250};self.fallback(r,'UNSUPPORTED_SCALE_METRIC')
    def test_size_range(self):
        r=Rig();r.slot()['size_limits']=[1,5];self.fallback(r,'SIZE_OUT_OF_RANGE')
    def test_invalid_head_shape_rolls_back(self):
        r=Rig();r.slot()['scale']['kind']='head_height';r.registry['assets']['nubi.legacy_laundry']['spec']['head']=[];r.specs['resident_nubi']['map27_in_1']['head']=[];self.fallback(r,'INVALID_HEAD_BOUNDS')
    def test_secondary_foot_contact_is_required(self):
        r=Rig('2/1/post');r.slot('staff.window_chair')['secondary_contacts'][0]['target'][1]=500;self.fallback(r,'SECONDARY_CONTACT_MISMATCH')
    def test_outside_world(self):
        r=Rig();r.slot()['target']=[-10000,-10000];self.fallback(r,'OUTSIDE_WORLD')
    def test_partial_world_clip_is_not_stretched(self):
        r=Rig();r.slot()['target']=[25,655];a=next(a for a in r.actors if a['person']=='resident_nubi')
        b=E['r13_pc_place'](a,r.registry['assets']['nubi.legacy_laundry'],r.slot(),[1920,720]);self.assertEqual(b['rect'][0],0);self.assertGreater(b['width'],b['rect'][2]);self.assertEqual(b['height'],a['height'])
    def test_viewport_offscreen_is_not_clickable_box(self):
        a={'rect':[1450,300,180,260]};self.assertIsNone(E['r13_pc_viewport_rect'](a,0));self.assertEqual(E['r13_pc_viewport_rect'](a,880),[570,300,180,260]);self.assertEqual(E['r13_pc_viewport_rect']({'rect':[1200,300,180,260]},0),[1200,300,80,260])
    def test_all_narrative_paths_bypass(self):
        for key in ('entry','locked_scene','offers'):
            r=Rig();r.context[key]=True;r.registry=None;out,report=r.resolve();self.assertIs(out,r.actors);self.assertEqual(report['bypass'],'narrative_priority')
    def test_existing_life_group_wins(self):
        r=Rig();next(a for a in r.actors if a['person']=='resident_nubi')['life_group']='existing_group';out,report=r.resolve();self.assertIs(out,r.actors);self.assertEqual(report['bypass'],'no_eligible_binding')
    def test_wrong_time_and_required_flag_no_spawn(self):
        for field,value in [('days',[]),('periods',[]),('need_flags',['not_present'])]:
            r=Rig();r.binding()[field]=value;out,report=r.resolve();self.assertIs(out,r.actors);self.assertEqual(report['bypass'],'no_eligible_binding')
    def test_wrong_identity(self):
        r=Rig();r.binding()['asset']='sling.parcel';self.fallback(r,'IDENTITY_MISMATCH')
    def test_role_slot_incompatible(self):
        r=Rig();r.binding()['role']='postal_staff';self.fallback(r,'INCOMPATIBLE_ROLE_SLOT')
    def test_unapproved_candidate_cannot_bind(self):
        r=Rig();r.registry['assets']['nubi.legacy_laundry']['status']='candidate';self.fallback(r,'UNAPPROVED_ASSET')
    def test_duplicate_binding(self):
        r=Rig();r.registry['bindings'].append(copy.deepcopy(r.binding()));self.fallback(r,'AMBIGUOUS_BINDING')
    def test_wrong_2160_vs_1280_variant(self):
        r=Rig('1/0/post');r.context['world_size']=[1280,720];self.fallback(r,'BACKGROUND_VARIANT_MISMATCH')
    def test_wrong_background_crop(self):
        r=Rig('1/0/post');r.context['background']['crop']=[0,0,2160,728];self.fallback(r,'BACKGROUND_VARIANT_MISMATCH')
    def test_upstream_mask_only_fix_cannot_be_reverted(self):
        for key,val in [('occlusion',[[1,2],[3,4],[5,6]]),('map27_occlusion',[[[1,2],[3,4],[5,6]]]),('map27_keepouts',[[[1,2],[3,4],[5,6]]]),('contact','new_contact'),('slot',[1,2,3,'floor']),('ground_depth',600),('elevation',10)]:
            r=Rig();next(a for a in r.actors if a['person']=='resident_nubi')[key]=val;self.fallback(r,'UPSTREAM_PLACEMENT_CHANGED')
    def test_stale_main067_coordinates_cannot_be_reverted(self):
        r=Rig();a=next(a for a in r.actors if a['person']=='resident_nubi');a['rect']=[206,414,165,248];a['depth']=662;self.fallback(r,'UPSTREAM_PLACEMENT_CHANGED')
    def test_old_source_warning_is_not_render_grid_fix(self):
        r=Rig();out,report=r.resolve();self.assertIn('SOURCE_COARSE_NOT_FIXED_BY_GRID',[w['code'] for w in report['warnings']]);self.assertFalse(r.registry['assets']['nubi.legacy_laundry']['source_quality']['render_grid_changes_asset_quality'])
    def test_face_collision_rejects_regression(self):
        r=Rig();a=next(a for a in r.actors if a['person']=='resident_nubi');others=[a for a in r.actors if a['person']!='resident_nubi'];self.assertTrue(others)
        target=E['r13_pc_face'](others[0],r.spec(others[0]['person'],others[0]['pose']));source=E['r13_pc_face'](a,r.spec(a['person'],a['pose']));r.slot()['target'][0]+=target[0]-source[0];r.slot()['target'][1]+=target[1]-source[1];self.fallback(r,'FACE_COLLISION')
    def test_critical_object_collision_rejects_regression(self):
        r=Rig();a=next(a for a in r.actors if a['person']=='resident_nubi');r.slot()['target'][0]-=100
        placed=E['r13_pc_place'](a,r.registry['assets']['nubi.legacy_laundry'],r.slot(),[1920,720]);face=E['r13_pc_face'](placed,r.spec(a['person'],a['pose']));r.registry['geometries'][r.variant['geometry']]['critical_rects']=[face];self.fallback(r,'CRITICAL_OBJECT_COLLISION')
    def test_no_coordinate_authoring_in_scenario_bindings(self):
        for b in Rig().registry['bindings']:
            self.assertFalse(set(b).intersection(('x','y','height','width','target','depth','occlusion')));self.assertIsInstance(b['upstream_guard'],str)
    def test_adapter_safe_missing_and_corrupt_registry_while_off(self):
        for payload in (None,b'{broken'):
            class Renpy:
                def file(self,p):
                    if payload is None: raise IOError('missing')
                    return io.BytesIO(payload)
                def log(self,m): pass
            env=dict(E,renpy=Renpy(),r13_stage_people=lambda entry=False:['upstream'])
            exec(compile(ADAPTER,'adapter','exec'),env)
            self.assertFalse(env['R13_PLACEMENT_CONTRACTS_ENABLED']);self.assertEqual(env['r13_stage_people'](),['upstream'])
    def test_adapter_disabled_does_not_touch_context_or_aliases(self):
        registry=REGISTRY.read_bytes()
        class Renpy:
            def file(self,p): return io.BytesIO(registry)
            def image(self,*a): raise AssertionError('default off registered image')
        actors=[{'original':True}];env=dict(E,renpy=Renpy(),r13_stage_people=lambda entry=False:actors)
        exec(compile(ADAPTER,'adapter','exec'),env);self.assertIs(env['r13_stage_people'](),actors)
    def test_adapter_contains_no_runtime_image_registration(self):
        runtime=ADAPTER.split('def r13_stage_people(entry=False):',1)[1]
        self.assertNotIn('register_aliases',runtime);self.assertNotIn('renpy.image',runtime)
    def test_malformed_registry_shape_is_atomic_fallback(self):
        for key,value in [('assets',None),('bindings',[None]),('background_variants',[])]:
            r=Rig();r.registry[key]=value;self.fallback(r,'INVALID_REGISTRY_SHAPE')
    def test_invalid_mask_polygons_never_reach_renderer(self):
        for value in (None, [[[1,2],[3],[4,5]]], [[[1,2],[3,4]]]):
            r=Rig();r.slot()['occlusion']=value;self.fallback(r,'INVALID_MASK_POLYGON' if value is None or len(value[0])<3 else 'INVALID_ANCHOR')
    def test_nonfinite_mask_never_reaches_renderer(self):
        r=Rig();r.slot()['occlusion']=[[[1,2],[3,float('nan')],[4,5]]];self.fallback(r,'INVALID_ANCHOR')
    def test_invalid_depth_and_mask_layer(self):
        r=Rig();r.slot()['depth']={'mode':'fixed','value':'bad'};self.fallback(r,'INVALID_NUMERIC_GEOMETRY')
        r=Rig();r.slot()['mask_layer']='unrecognized';self.fallback(r,'INVALID_MASK_LAYER')
    def test_whole_scene_rolls_back_if_second_binding_fails(self):
        r=Rig('3/1/post');r.slot('staff.window_chair')['contacts']=['standing'];self.fallback(r,'INCOMPATIBLE_CONTACT')
    def alias_env(self):
        r=Rig();asset=r.registry['assets']['nubi.legacy_laundry'];asset['registration']='isolated_alias';asset['pose']='pc_test_existing_source';asset['source_quality']['status']='reference_reviewed'
        logs=[];images=[];registered=set()
        class Renpy:
            def file(self,path): return io.BytesIO(json.dumps(r.registry).encode())
            def log(self,message): logs.append(message)
            def loadable(self,path): return True
            def has_image(self,name,exact=False): self.exact=exact;return name in registered
            def image(self,name,displayable): images.append(name)
        env=dict(E,renpy=Renpy(),r13_stage_people=lambda entry=False:[],R13_ACTING={},CAST={'resident_nubi':{}},Transform=lambda a,**kw:a,Crop=lambda c,f:(c,f))
        exec(compile(ADAPTER,'adapter','exec'),env);env['r13_pc_blob']=r.blobs.get
        return r,env,images,registered
    def test_new_alias_prevalidated_and_expected_spec_not_shared(self):
        r,e,images,registered=self.alias_env();e['r13_pc_register_aliases_at_init']();self.assertEqual(images,['resident_nubi pc_test_existing_source'])
        e['R13_ACTING']['resident_nubi']['pc_test_existing_source']['native_detail']=True
        self.assertNotIn('native_detail',e['R13_PLACEMENT_CONTRACTS']['assets']['nubi.legacy_laundry']['spec'])
    def test_alias_existing_engine_image_not_overwritten(self):
        r,e,images,registered=self.alias_env();registered.add('resident_nubi pc_test_existing_source')
        with self.assertRaisesRegex(E['R13PlacementContractError'],'ALIAS_ALREADY_REGISTERED'):e['r13_pc_register_aliases_at_init']()
        self.assertEqual(images,[]);self.assertEqual(e['R13_ACTING'],{});self.assertTrue(e['renpy'].exact)
    def test_alias_bad_contract_is_rejected_before_registration(self):
        r,e,images,registered=self.alias_env();e['R13_PLACEMENT_CONTRACTS']['assets']['nubi.legacy_laundry']['alpha_bounds']=[0,0,10000,10000]
        with self.assertRaisesRegex(E['R13PlacementContractError'],'INVALID_INTRINSIC_BOUNDS'):e['r13_pc_register_aliases_at_init']()
        self.assertEqual(images,[]);self.assertEqual(e['R13_ACTING'],{})
    def test_reuse_existing_map27_geometry_and_contact_assertions(self):
        old={};path=Path(__file__).parent/'fixtures/upstream_map27_geometry.py';exec(compile(path.read_text(),str(path),'exec'),old)
        cases=json.loads((path.parent/'upstream_map27_geometry_cases.json').read_text())
        for row in cases:
            for period,name in enumerate(('morning','afternoon','evening')):
                if row['location']=='inn' and period!=0:continue
                r=Rig('1/%d/%s'%(period,row['location']));actor=next(a for a in r.actors if a['person']==row['person']);variant=row['variants'][name]
                legacy=old['r13_map27_geometry'](actor,row['spec'],variant,variant['world_width']);out,report=r.resolve();current=next(a for a in out if a['person']==actor['person'])
                for key in ('x','y','width','height','rect','depth','contact','occlusion','map27_occlusion','map27_keepouts'):
                    self.assertEqual(E['r13_pc_normalized'](legacy[key]),E['r13_pc_normalized'](current[key]))
                invalid=copy.deepcopy(variant);invalid['secondary_targets']={next(iter(row['spec']['anchors'])):[-999,-999]}
                with self.assertRaisesRegex(ValueError,'secondary contact mismatch'):old['r13_map27_geometry'](actor,row['spec'],invalid,variant['world_width'])
    def test_json_schema_accepts_actual_registry(self):
        try:import jsonschema
        except ImportError:self.skipTest('jsonschema authoring validator not installed; runtime has no dependency')
        schema=json.loads((REGISTRY.parent/'room13-placement-contracts.schema.json').read_text());jsonschema.Draft202012Validator.check_schema(schema);jsonschema.validate(json.loads(REGISTRY.read_text()),schema)
    def test_preimage_guard_rejects_stale_source_and_existing_addition(self):
        import importlib.util,tempfile
        spec=importlib.util.spec_from_file_location('guard',Path(__file__).with_name('verify_placement_contract_preimages.py'));guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'old').write_text('old');manifest={'preimages':{'old':guard.git_blob(root/'old')},'additions':{'new':'not-used-before'}}
            self.assertEqual(guard.verify(root,manifest),[]);(root/'old').write_text('drift');self.assertEqual(guard.verify(root,manifest)[0]['reason'],'PREIMAGE_MISMATCH')
            (root/'old').write_text('old');(root/'new').write_text('do not overwrite');self.assertEqual(guard.verify(root,manifest)[0]['reason'],'ADDED_PATH_ALREADY_EXISTS')
    def test_incomplete_upstream_guard_rejected(self):
        r=Rig();r.registry['upstream_guards'][r.binding()['upstream_guard']]={};self.fallback(r,'INCOMPLETE_UPSTREAM_GUARD')
    def test_new_alias_needs_reference_review(self):
        r,e,images,registered=self.alias_env();e['R13_PLACEMENT_CONTRACTS']['assets']['nubi.legacy_laundry']['source_quality']['status']='legacy_coarse'
        with self.assertRaisesRegex(E['R13PlacementContractError'],'UNREVIEWED_NEW_VARIANT'):e['r13_pc_register_aliases_at_init']()
        self.assertEqual(images,[])
    def test_reuse_existing_pr18c_inn_contact_geometry(self):
        r=Rig();actor=next(a for a in r.actors if a['person']=='resident_nubi')
        old=dict(r13_acting_spec=r.spec,r13_actor_geometry=lambda person,pose:tuple(r.spec(person,pose)['crop'][2:]))
        path=Path(__file__).parent/'fixtures/upstream_spatial_contact_geometry.py';exec(compile(path.read_text(),str(path),'exec'),old)
        legacy=old['r13_contact_geometry'](actor,actor['pose'],'foot',(420,535),226,535);out,report=r.resolve();current=next(a for a in out if a['person']==actor['person'])
        for key in ('x','y','width','height','rect','depth','contact','occlusion','map27_occlusion','map27_keepouts'):
            self.assertEqual(E['r13_pc_normalized'](legacy[key]),E['r13_pc_normalized'](current[key]))
    def test_pr18c_post_morning_source_is_untouched(self):
        for day in (2,3,6):
            r=Rig('%d/0/post'%day);before=next(a for a in r.actors if a['person']=='seryeon');out,report=r.resolve();after=next(a for a in out if a['person']=='seryeon')
            self.assertEqual(before,after);self.assertEqual(after['rect'],[1403,340,195,234]);self.assertEqual(after['depth'],560);self.assertEqual(len(after['map27_occlusion']),1)
        self.assertFalse(any(b['actor']=='seryeon' and 'post.morning' in b['variants'] for b in Rig().registry['bindings']))
    def test_candidate_is_two_new_init_blocks_only(self):
        self.assertEqual(SOURCE.count('init 183 python:'),1);self.assertEqual(SOURCE.count('init 184 python:'),1)
        compile(CORE,'core','exec');compile(ADAPTER,'adapter','exec')


if __name__ == '__main__': unittest.main(verbosity=2)
