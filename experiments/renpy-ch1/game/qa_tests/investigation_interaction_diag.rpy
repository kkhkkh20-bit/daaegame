# Separate controlled input cases. Uses actual production r13_roam / r13_field routing.
# No test bypass of resident dispatch, object observation, or return routing.
init 999 python:
    R13_PD_MAP_PEOPLE={'post':('seryeon','resident_sling','resident_jongjong'),'workshop':('resident_tok','buri','resident_lamplighter','resident_musoe'),'inn':('granny','resident_ttadak')}
    R13_PD_MAP_OBJECTS={'post':('scarf','twine','parcels'),'workshop':('plans','bolts','rag'),'inn':('keys','register')}

    def r13_pd_flow_log(step,extra=None):
        out=dict(step=step,variant=r13_pd_variant,day=room13['day'],period=room13['period'],location=room13['location'],motion_enabled=bool(persistent.room13_motion),appearance_duration=r13_appearance_duration(),flags=list(room13.get('flags',[])))
        if extra:out.update(extra)
        with open(r13_pd_os.path.join(r13_pd_out(),'interaction-'+room13['location']+'.jsonl'),'a') as f:
            f.write(r13_pd_json.dumps(out,ensure_ascii=False)+'\n')

    def r13_pd_check_field(step):
        hub=renpy.get_screen('r13_hub')
        assert hub and hub.scope.get('ready',False),'Real hub not ready'
        offset=r13_world_offset();rows=[]
        for actor in r13_stage_people(False):
            row=r13_pd_row(actor,'r13_hub')
            row['on_screen']=actor['x']+actor['width']>offset and actor['x']<offset+1280
            if row['on_screen']:
                assert row['widget_present'] and row['ancestor_alphas'] and all(a>=.99 for a in row['ancestor_alphas']),('Incomplete entrance render',row)
                assert min(row['render_bounds'])>0,row
            rows.append(row)
        r13_pd_flow_log(step,dict(actors=rows,ready=True))

    def r13_pd_choose_person():
        location=room13['location'];offset=r13_world_offset()
        actors=r13_stage_people(False);plates=r13_actor_nameplates(actors)
        for person in R13_PD_MAP_PEOPLE[location]:
            plate=next((p for p in plates if p['person']==person),None)
            if not plate or r13_offer_for_person(person):continue
            x,y,w,h=plate['rect'];sx=x+w/2-offset;sy=y+h/2
            if not (16<sx<1000 and 100<sy<690):continue
            store.r13_pd_person=person;store.r13_pd_person_name=R13_NAMES[person]
            store.r13_pd_person_x=int(sx);store.r13_pd_person_y=int(sy)
            r13_pd_flow_log('resident-click-target',dict(person=person,name=R13_NAMES[person],nameplate_rect=plate['rect'],screen_click=[sx,sy],method='actual visible nameplate; not guessed body rectangle'))
            return
        raise AssertionError(('No preferred scheduled resident nameplate in viewport',location,[a['person'] for a in actors]))

    def r13_pd_choose_object():
        location=room13['location'];offset=r13_world_offset();actors=r13_stage_people(False)
        objects=ROOM13['objects'][location]
        occupied=[a['rect'] for a in actors]+[p['rect'] for p in r13_actor_nameplates(actors)]
        def inside(px,py,rect):
            x,y,w,h=rect;return x<=px<x+w and y<=py<y+h
        for key in R13_PD_MAP_OBJECTS[location]:
            spec=objects.get(key)
            if not spec or not r13_object_visible(spec):continue
            # Avoid contexts requiring a choice for this minimal click-return case.
            if r13_tool_available(key) or r13_object_actions(key) or r13_context_wait(key) or r13_bed_available(key) or r13_bed_blocked_reason(key):continue
            x,y,w,h=spec['rect']
            for fy in (.5,.25,.75,.1,.9):
                for fx in (.5,.25,.75,.1,.9):
                    px,py=int(x+w*fx),int(y+h*fy);sx=px-offset
                    if not (24<sx<1000 and 110<py<590):continue
                    if any(inside(px,py,r) for r in occupied):continue
                    if any(other!=key and r13_object_visible(ospec) and inside(px,py,ospec['rect']) for other,ospec in objects.items()):continue
                    flag='observed:'+location+':'+key
                    assert not r13_has(flag),('Object already observed in fresh fixture',flag)
                    store.r13_pd_object=key;store.r13_pd_observed_flag=flag
                    store.r13_pd_object_x=int(sx);store.r13_pd_object_y=py
                    r13_pd_flow_log('object-click-target',dict(key=key,source_rect=spec['rect'],screen_click=[sx,py],method='runtime object rectangle; exclude actor/nameplate/other object rectangles'))
                    return
        raise AssertionError(('No unobstructed context-free object point',location))

# Starts a fresh actual roam state; no natural-campaign completion claim.
testcase investigation_flow_baseline_post:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_pd_begin,"baseline")
    run Call("r13_qa_roam",dict(day=2,period=0,location="post",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    screenshot "flow-baseline_post-01-field.png"
    run Function(r13_pd_choose_person)
    click pos (r13_pd_person_x,r13_pd_person_y)
    advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
    assert eval (r13_target==r13_pd_person)
    pause 0.4
    run Function(r13_pd_flow_log,"resident-approach-or-topics",dict(person=r13_target))
    screenshot "flow-baseline_post-02-resident.png"
    click "돌아가기"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    assert eval (room13["location"]=="post")
    run Function(r13_pd_check_field,"returned-from-resident")
    run Function(r13_pd_choose_object)
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    run Function(r13_pd_flow_log,"actual-object-observed",dict(key=r13_pd_object,flag=r13_pd_observed_flag))
    screenshot "flow-baseline_post-03-object.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    assert eval (room13["location"]=="post" and room13["day"]==2 and room13["period"]==0)
    run Function(r13_pd_check_field,"returned-from-object")
    screenshot "flow-baseline_post-04-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_pd_end)

# Starts a fresh actual roam state; no natural-campaign completion claim.
testcase investigation_flow_baseline_workshop:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_pd_begin,"baseline")
    run Call("r13_qa_roam",dict(day=2,period=0,location="workshop",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    screenshot "flow-baseline_workshop-01-field.png"
    run Function(r13_pd_choose_person)
    click pos (r13_pd_person_x,r13_pd_person_y)
    advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
    assert eval (r13_target==r13_pd_person)
    pause 0.4
    run Function(r13_pd_flow_log,"resident-approach-or-topics",dict(person=r13_target))
    screenshot "flow-baseline_workshop-02-resident.png"
    click "돌아가기"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    assert eval (room13["location"]=="workshop")
    run Function(r13_pd_check_field,"returned-from-resident")
    run Function(r13_pd_choose_object)
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    run Function(r13_pd_flow_log,"actual-object-observed",dict(key=r13_pd_object,flag=r13_pd_observed_flag))
    screenshot "flow-baseline_workshop-03-object.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    assert eval (room13["location"]=="workshop" and room13["day"]==2 and room13["period"]==0)
    run Function(r13_pd_check_field,"returned-from-object")
    screenshot "flow-baseline_workshop-04-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_pd_end)

# Starts a fresh actual roam state; no natural-campaign completion claim.
testcase investigation_flow_baseline_inn:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_pd_begin,"baseline")
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    screenshot "flow-baseline_inn-01-field.png"
    run Function(r13_pd_choose_person)
    click pos (r13_pd_person_x,r13_pd_person_y)
    advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
    assert eval (r13_target==r13_pd_person)
    pause 0.4
    run Function(r13_pd_flow_log,"resident-approach-or-topics",dict(person=r13_target))
    screenshot "flow-baseline_inn-02-resident.png"
    click "돌아가기"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    assert eval (room13["location"]=="inn")
    run Function(r13_pd_check_field,"returned-from-resident")
    run Function(r13_pd_choose_object)
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    run Function(r13_pd_flow_log,"actual-object-observed",dict(key=r13_pd_object,flag=r13_pd_observed_flag))
    screenshot "flow-baseline_inn-03-object.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    assert eval (room13["location"]=="inn" and room13["day"]==2 and room13["period"]==0)
    run Function(r13_pd_check_field,"returned-from-object")
    screenshot "flow-baseline_inn-04-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_pd_end)

# Starts a fresh actual roam state; no natural-campaign completion claim.
testcase investigation_flow_proposed_post:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_pd_begin,"proposed")
    run Call("r13_qa_roam",dict(day=2,period=0,location="post",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    screenshot "flow-proposed_post-01-field.png"
    run Function(r13_pd_choose_person)
    click pos (r13_pd_person_x,r13_pd_person_y)
    advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
    assert eval (r13_target==r13_pd_person)
    pause 0.4
    run Function(r13_pd_flow_log,"resident-approach-or-topics",dict(person=r13_target))
    screenshot "flow-proposed_post-02-resident.png"
    click "돌아가기"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    assert eval (room13["location"]=="post")
    run Function(r13_pd_check_field,"returned-from-resident")
    run Function(r13_pd_choose_object)
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    run Function(r13_pd_flow_log,"actual-object-observed",dict(key=r13_pd_object,flag=r13_pd_observed_flag))
    screenshot "flow-proposed_post-03-object.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    assert eval (room13["location"]=="post" and room13["day"]==2 and room13["period"]==0)
    run Function(r13_pd_check_field,"returned-from-object")
    screenshot "flow-proposed_post-04-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_pd_end)

# Starts a fresh actual roam state; no natural-campaign completion claim.
testcase investigation_flow_proposed_workshop:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_pd_begin,"proposed")
    run Call("r13_qa_roam",dict(day=2,period=0,location="workshop",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    screenshot "flow-proposed_workshop-01-field.png"
    run Function(r13_pd_choose_person)
    click pos (r13_pd_person_x,r13_pd_person_y)
    advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
    assert eval (r13_target==r13_pd_person)
    pause 0.4
    run Function(r13_pd_flow_log,"resident-approach-or-topics",dict(person=r13_target))
    screenshot "flow-proposed_workshop-02-resident.png"
    click "돌아가기"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    assert eval (room13["location"]=="workshop")
    run Function(r13_pd_check_field,"returned-from-resident")
    run Function(r13_pd_choose_object)
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    run Function(r13_pd_flow_log,"actual-object-observed",dict(key=r13_pd_object,flag=r13_pd_observed_flag))
    screenshot "flow-proposed_workshop-03-object.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    assert eval (room13["location"]=="workshop" and room13["day"]==2 and room13["period"]==0)
    run Function(r13_pd_check_field,"returned-from-object")
    screenshot "flow-proposed_workshop-04-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_pd_end)

# Starts a fresh actual roam state; no natural-campaign completion claim.
testcase investigation_flow_proposed_inn:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_pd_begin,"proposed")
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    screenshot "flow-proposed_inn-01-field.png"
    run Function(r13_pd_choose_person)
    click pos (r13_pd_person_x,r13_pd_person_y)
    advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
    assert eval (r13_target==r13_pd_person)
    pause 0.4
    run Function(r13_pd_flow_log,"resident-approach-or-topics",dict(person=r13_target))
    screenshot "flow-proposed_inn-02-resident.png"
    click "돌아가기"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    assert eval (room13["location"]=="inn")
    run Function(r13_pd_check_field,"returned-from-resident")
    run Function(r13_pd_choose_object)
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    run Function(r13_pd_flow_log,"actual-object-observed",dict(key=r13_pd_object,flag=r13_pd_observed_flag))
    screenshot "flow-proposed_inn-03-object.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    assert eval (room13["location"]=="inn" and room13["day"]==2 and room13["period"]==0)
    run Function(r13_pd_check_field,"returned-from-object")
    screenshot "flow-proposed_inn-04-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_pd_end)
