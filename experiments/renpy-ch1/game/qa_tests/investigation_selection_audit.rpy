# QA-only controlled final-selector sweep, not a natural campaign replay.
default r13_selection_audit_done = False
default r13_selection_audit_page = []
default r13_selection_audit_page_number = 0

init 999 python:
    def r13_selection_audit_collect():
        out=r13_pd_os.path.join(r13_pd_os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'),'investigation-selection-audit')
        r13_pd_os.makedirs(out,exist_ok=True)
        def checkpoint(step, **details):
            with open(r13_pd_os.path.join(out,'checkpoints.jsonl'),'a') as f:
                f.write(r13_pd_json.dumps(dict(step=step,**details),ensure_ascii=False)+'\n');f.flush()
        checkpoint('collect-start')
        original=r13_pd_copy.deepcopy(room13)
        unique={};failures=[];states=0
        locations=sorted(R13_PLACES)
        try:
            for day in range(1,15):
                for period in range(3):
                    for location in locations:
                        state=r13_pd_copy.deepcopy(original)
                        state.update(day=day,period=period,location=location)
                        store.room13=state;R13_STAGE_CACHE.clear();states+=1
                        checkpoint('state-start',day=day,period=period,location=location,state_count=states)
                        try:
                            actors=r13_stage_people(False)
                            for actor in actors:
                                who,pose=actor['person'],actor['pose']
                                assert actor['width']>0 and actor['height']>0, ('Nonpositive selected size',actor)
                                spec=r13_acting_spec(who,pose) or {}
                                source_file=spec.get('file')
                                if source_file and not renpy.loadable(source_file):
                                    failures.append(dict(day=day,period=period,location=location,person=who,pose=pose,error='Selected authored source is not loadable',file=source_file))
                                    continue
                                key=(who,pose,source_file or '<runtime-fallback-displayable>')
                                if key not in unique:
                                    # Missing authored metadata is not proof that a CAST fallback image is missing.
                                    rendered=renpy.render(r13_staged_visible_art(actor,still=True),1280,720,1.0,1.0).get_size()
                                    assert min(rendered)>0, ('Selected displayable has no rendered bounds',who,pose)
                                    unique[key]=dict(person=who,pose=pose,file=source_file,native_detail=bool(spec.get('native_detail')),
                                        source_kind='authored-spec' if source_file else 'runtime-fallback-metadata-unresolved',rendered_bounds=list(rendered),
                                        source_crop=spec.get('crop'),source_size=list(renpy.image_size(source_file)) if source_file else None,contexts=[])
                                unique[key]['contexts'].append(dict(day=day,period=period,location=location,
                                    rect=list(actor['rect']),size=[actor['width'],actor['height']],contact=actor.get('contact'),
                                    occlusion=actor.get('occlusion',[]),map27_occlusion=actor.get('map27_occlusion',[])))
                        except Exception as error:
                            failures.append(dict(day=day,period=period,location=location,error=repr(error)))
        finally:
            store.room13=original;R13_STAGE_CACHE.clear() # Derived cache invalidation, not cache-content restoration.
            checkpoint('collect-restored',state_count=states,failures=len(failures))
        rows=[unique[key] for key in sorted(unique)]
        report=dict(kind='controlled actual final-selector sweep; no natural campaign completion claim',
            original_state=original,locations=locations,days=list(range(1,15)),periods=[0,1,2],state_count=states,
            unique_selected_pose_count=len(rows),rows=rows,failures=failures,
            limits=['Existing QA roam suppression flags are held fixed and recorded.',
                'Story-exclusive states not selected by this profile remain unverified.',
                'Comparison-board size200 is not a production size proposal.',
                'World placement/click proof is limited to separately executed cases.'])
        out=r13_pd_os.path.join(r13_pd_os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'),'investigation-selection-audit')
        r13_pd_os.makedirs(out,exist_ok=True)
        with open(r13_pd_os.path.join(out,'selection-report.json'),'w') as f:
            r13_pd_json.dump(report,f,ensure_ascii=False,indent=2)
        assert not failures, failures[:5]
        return rows,out

    def r13_selection_audit_board_actors(rows):
        result=[]
        for i,row in enumerate(rows):
            who,pose=row['person'],row['pose']
            cw,ch=r13_actor_geometry(who,pose)
            scale=min(200.0/ch,390.0/cw)
            w=int(round(cw*scale));h=int(round(ch*scale))
            result.append(dict(person=who,pose=pose,x=(i%3)*426+(426-w)//2,y=(i//3)*240+24,
                width=w,height=h,rect=[0,0,w,h],depth=h,occlusion=[],map27_occlusion=[],contact='standing'))
        return result

screen r13_selection_audit_board():
    modal True
    zorder 300
    add Solid('#243039')
    for index,actor in enumerate(r13_selection_audit_board_actors(r13_selection_audit_page)):
        add r13_staged_visible_art(actor,still=True) xpos actor['x'] ypos actor['y']
        text (actor['person']+' / '+actor['pose']) xpos (index%3)*426+6 ypos (index//3)*240+4 size 12
    text ('CONTROLLED SELECTED POSES / page '+str(r13_selection_audit_page_number)) xpos 6 ypos 704 size 12

label r13_selection_audit_run:
    $ r13_selection_audit_done=False
    $ r13_selection_rows,r13_selection_out=r13_selection_audit_collect()
    hide screen say
    hide screen r13_hub
    python:
        for start in range(0,len(r13_selection_rows),9):
            store.r13_selection_audit_page=r13_selection_rows[start:start+9]
            store.r13_selection_audit_page_number=start//9+1
            r13_pd_checkpoint('selection-board-%03d-before-show'%store.r13_selection_audit_page_number,capture=False)
            renpy.show_screen('r13_selection_audit_board')
            renpy.pause(.25,hard=True,modal=False)
            assert renpy.screenshot(r13_pd_os.path.join(r13_selection_out,'selected-poses-%03d.png'%store.r13_selection_audit_page_number))
            r13_pd_checkpoint('selection-board-%03d-captured'%store.r13_selection_audit_page_number,capture=False)
            renpy.hide_screen('r13_selection_audit_board')
        store.r13_selection_audit_done=True
    return

testcase investigation_selection_audit:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    run Call("r13_selection_audit_run")
    pause until eval (r13_selection_audit_done) timeout 120
