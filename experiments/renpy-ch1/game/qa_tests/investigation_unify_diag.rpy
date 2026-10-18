# Diagnostic-only overlay. Install only in the official native QA checkout.
# Uses final runtime functions and never overrides production rendering/staging.
default r13_qa_pixel_diag_done = False

init 999 python:
    import os as r13_pd_os
    import json as r13_pd_json
    import copy as r13_pd_copy
    R13_PD_PEOPLE = ('resident_kkwak','daram','resident_kalbaram','karo','resident_piko','doto','resident_jongjong','resident_lamplighter','resident_musoe')

    def r13_pd_out():
        path=r13_pd_os.path.join(r13_pd_os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'),'investigation-pixel-diag',getattr(store,'r13_pd_variant','proposed'))
        r13_pd_os.makedirs(path,exist_ok=True)
        return path

    def r13_pd_row(actor, screen_name=None):
        person,pose=actor['person'],actor['pose']
        spec=r13_acting_spec(person,pose) or {}
        cw,ch=r13_actor_geometry(person,pose)
        art=r13_staged_visible_art(actor,still=True)
        size=renpy.render(art,1280,720,1.0,1.0).get_size()
        widget=renpy.get_displayable(screen_name,'r13_world_'+person) if screen_name else None
        alpha_path=r13_pd_alpha_path(screen_name,widget) if widget is not None else None
        alpha=min(alpha_path) if alpha_path else None
        foot=spec.get('foot',spec.get('anchor',{}).get('foot',[cw/2.0,ch]))
        return dict(person=person,pose=pose,file=spec.get('file'),native_detail=bool(spec.get('native_detail')),
            crop=spec.get('crop'),source_size=list(renpy.image_size(spec['file'])) if spec.get('file') else None,
            source_crop_size=[cw,ch],display_size=[actor['width'],actor['height']],render_bounds=list(size),
            scale_xy=[float(actor['width'])/cw,float(actor['height'])/ch],foot_anchor=foot,
            world_xy=[actor['x'],actor['y']],foot_world=[actor['x']+foot[0]*float(actor['height'])/ch,actor['y']+foot[1]*float(actor['height'])/ch],
            contact=actor.get('contact'),slot=actor.get('slot'),widget_present=widget is not None,widget_alpha=alpha,ancestor_alphas=alpha_path,motion_enabled=bool(persistent.room13_motion),appearance_duration=r13_appearance_duration(),
            camera_offset=r13_world_offset(),occlusion=actor.get('occlusion',[]),map27_occlusion=actor.get('map27_occlusion',[]))

    def r13_pd_alpha_path(screen_name,target):
        screen=renpy.get_screen(screen_name)
        def walk(node,alphas,seen):
            if node is None or id(node) in seen:return None
            seen=seen|{id(node)}
            state=getattr(node,'state',None)
            alpha=getattr(state,'alpha',None)
            if isinstance(node,renpy.display.transform.Transform) and alpha is not None:
                alphas=alphas+[float(alpha)]
            if node is target:return alphas
            for child in node.visit():
                found=walk(child,alphas,seen)
                if found is not None:return found
            return None
        return walk(screen.child,[],set()) if screen else None

    def r13_pd_begin(variant):
        store.r13_pd_variant=variant
        store.r13_pd_saved_acting=r13_pd_copy.deepcopy(R13_ACTING)
        store.r13_pd_saved_map27=r13_pd_copy.deepcopy(R13_MAP_ACTION27)
        if variant=='baseline':
            baseline_acting=r13_pd_json.load(renpy.file('qa_tests/baseline-room13-pixel-acting.json'))
            baseline_map27=r13_pd_json.load(renpy.file('qa_tests/baseline-room13-map-action27.json'))
            # Preserve unrelated runtime injections; replace all baseline keys and map27 rows.
            for person,poses in baseline_acting.items():
                R13_ACTING.setdefault(person,{}).update(r13_pd_copy.deepcopy(poses))
            store.R13_MAP_ACTION27=baseline_map27
            for row in baseline_map27['rows']:
                if row.get('status')=='approved' and renpy.loadable(row['spec']['file']):
                    R13_ACTING.setdefault(row['person'],{})[row['pose']]=r13_pd_copy.deepcopy(row['spec'])
        R13_STAGE_CACHE.clear()

    def r13_pd_end():
        store.R13_ACTING=store.r13_pd_saved_acting
        store.R13_MAP_ACTION27=store.r13_pd_saved_map27
        R13_STAGE_CACHE.clear()

    def r13_pd_baseline():
        actors=[]
        for i,person in enumerate(R13_PD_PEOPLE):
            cw,ch=r13_actor_geometry(person,'neutral');h=200;w=int(round(cw*float(h)/ch))
            actors.append(dict(person=person,pose='neutral',x=(i%3)*426+(426-w)//2,y=(i//3)*240+30,width=w,height=h,
                rect=[0,0,w,h],depth=h,occlusion=[],contact='standing'))
        return actors

    def r13_pd_state(base,day,period,location):
        assert location in R13_PLACES
        state=r13_pd_copy.deepcopy(base);state.update(day=day,period=period,location=location)
        store.room13=state
        R13_STAGE_CACHE.clear()
        return state

screen r13_qa_pixel_baseline():
    modal True
    zorder 300
    add Solid('#243039')
    text ('NATIVE CONTROLLED BOARD / '+r13_pd_variant) xpos 8 ypos 704 size 13
    for actor in r13_pd_baseline():
        add r13_staged_visible_art(actor,still=True) xpos actor['x'] ypos actor['y']
        text actor['person'] xpos (R13_PD_PEOPLE.index(actor['person'])%3)*426+8 ypos (R13_PD_PEOPLE.index(actor['person'])//3)*240+5 size 16

screen r13_qa_pixel_variant():
    zorder 400
    text ('NATIVE FIELD FIXTURE / '+r13_pd_variant) xpos 8 ypos 704 size 13 color '#ffffff' outlines [(1,'#000000',0,0)]

label r13_qa_pixel_diag(variant="proposed"):
    $ r13_qa_pixel_diag_done=False
    python:
        r13_pd_begin(variant)
    $ persistent.room13_motion=False
    hide screen say
    hide screen r13_hub
    show screen r13_qa_pixel_baseline
    $ renpy.pause(1.0, hard=True)
    python:
        report={'variant':variant,'source_commit':'24ce3b6037093a562f0bd9b1c35c64a9b690a13d','kind':'bounded three-map native presentation fixture; not campaign replay; equal-height board is not an age/size target','baseline':[r13_pd_row(a) for a in r13_pd_baseline()],'fields':[],'missing':[]}
        renpy.screenshot(r13_pd_os.path.join(r13_pd_out(),'00-neutral-equal-height.png'))
    hide screen r13_qa_pixel_baseline
    python:
        base=r13_pd_copy.deepcopy(room13)
        # Bounded presentation fixtures only: three morning maps, one initial viewport.
        cases=[(2,0,location,0) for location in ('post','workshop','inn')]
        report['schedule_inventory']=[]
        report['missing']=[]
        for index,(day,period,location,offset) in enumerate(cases):
            r13_pd_state(base,day,period,location)
            store.r13_world_cameras={location:offset}
            store.r13_field_location=location;store.r13_field_view='people';store.r13_field_pick=None
            renpy.scene()
            renpy.show('r13_pd_background',what=r13_background(R13_PLACES[location][1]))
            renpy.show_screen('r13_hub',entry=False)
            renpy.show_screen('r13_qa_pixel_variant')
            renpy.pause(1.2,hard=True)
            hub=renpy.get_screen('r13_hub')
            assert hub and hub.scope.get('ready',False), 'Field is not ready'
            actors=r13_stage_people(False)
            rows=[r13_pd_row(a,'r13_hub') for a in actors]
            for row in rows:
                row['on_screen']=row['world_xy'][0]+row['display_size'][0]>offset and row['world_xy'][0]<offset+1280
                assert min(row['render_bounds'])>0, row
                assert not row['on_screen'] or (row['widget_present'] and row['widget_alpha'] is not None and row['widget_alpha']>=.99), ('Unverified visible actor',row)
            shot='%02d-d%02d-p%d-%s-x%d.png'%(index+1,day,period,location,offset)
            report['fields'].append(dict(day=day,period=period,location=location,shot=shot,ready=True,actors=rows,flags=list(room13.get('flags',[]))))
            renpy.screenshot(r13_pd_os.path.join(r13_pd_out(),shot))
            with open(r13_pd_os.path.join(r13_pd_out(),'report.json'),'w') as output:r13_pd_json.dump(report,output,ensure_ascii=False,indent=2)
            renpy.hide_screen('r13_hub')
            renpy.hide_screen('r13_qa_pixel_variant')
        store.room13=base
        R13_STAGE_CACHE.clear()
        with open(r13_pd_os.path.join(r13_pd_out(),'report.json'),'w') as output:r13_pd_json.dump(report,output,ensure_ascii=False,indent=2)
        r13_pd_end()
        store.r13_qa_pixel_diag_done=True
    return

testcase investigation_unify_diag:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    click pos (640,600) until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    run Call("r13_qa_pixel_diag","baseline")
    pause until eval (r13_qa_pixel_diag_done) timeout 240
    $ r13_qa_pixel_diag_done=False
    run Call("r13_qa_pixel_diag","proposed")
    pause until eval (r13_qa_pixel_diag_done) timeout 240
