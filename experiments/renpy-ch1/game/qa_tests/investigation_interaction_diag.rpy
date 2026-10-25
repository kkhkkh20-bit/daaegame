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
        assert r13_pd_scene_ready(),r13_pd_scene_status()
        offset=r13_world_offset();rows=[]
        for actor in r13_stage_people(False):
            row=r13_pd_row(actor,'r13_hub')
            row['on_screen']=actor['x']+actor['width']>offset and actor['x']<offset+1280
            if row['on_screen']:
                assert row['widget_present'] and row['ancestor_alphas'] and all(a>=.99 for a in row['ancestor_alphas']),('Incomplete entrance render',row)
                assert min(row['render_bounds'])>0,row
            rows.append(row)
        r13_pd_flow_log(step,dict(actors=rows,ready=True,scene_status=r13_pd_scene_status()))

    def r13_pd_plain_topics(person):
        result=[]
        for key,spec in r13_topics_in_order(person):
            if key not in ROOM13['topics'] or key in R13_TOPIC_LABELS or key in ('buri_consent','home:records','shop:eunho') or spec.get('special') or key in room13.get('read_topics',[]):continue
            if spec.get('npc')!=person or spec.get('cost') or spec.get('consume'):continue
            rows=r13_topic_current_lines(key) if r13_topic_current_context(key) is not None else r13_conversation_topic_lines(key)
            speech=[row[1] for row in rows if row[0]==person]
            if speech:result.append((key,spec,speech))
        return result

    def r13_pd_contact_probe(person):
        eligible=r13_pd_plain_topics(person)
        contact=bool(r13_contact_has_content(person))
        rows=[]
        if person not in r13_met_people():
            rows=list(r13_conversation_opening(person,True))
            if person in R13_OPENING_SCENES['first_meetings']:rows+=list(r13_resident_notice(person))
        predicted=[]
        for who,line in rows:
            predicted.extend(r13_question_line_cues('notice:resident:'+person,who,line))
        return dict(person=person,contact_has_content=contact,plain_keys=[k for k,_,_ in eligible],
            available_keys=[k for k,_ in r13_topics_in_order(person)],predicted_first_contact_cues=sorted(set(predicted)),
            known_cues=sorted(room13.get('question_cues',{})),already_met=person in r13_met_people())

    def r13_pd_target_render(person,pose,step):
        actor=next(a for a in r13_stage_people(False) if a['person']==person)
        assert actor['pose']==pose,(person,actor['pose'],pose)
        row=r13_pd_row(actor,'r13_hub');offset=r13_world_offset()
        row['on_screen']=actor['x']+actor['width']>offset and actor['x']<offset+1280
        assert min(row['render_bounds'])>0,row
        if row['on_screen']:
            assert row['widget_present'] and row['ancestor_alphas'] and all(a>=.99 for a in row['ancestor_alphas']),row
        r13_pd_flow_log(step,dict(target=row,contact_probe=r13_pd_contact_probe(person),
            ordinary_place_access=room13['location'] in r13_places(),visual_acceptance=False))

    def r13_pd_log_opening(step):
        screen=renpy.get_screen('say')
        assert screen is not None
        r13_pd_flow_log(step,dict(packet=list(r13_packet),who=screen.scope.get('who'),what=screen.scope.get('what'),
            person=r13_pd_person,contact_probe=r13_pd_contact_probe(r13_pd_person)))

    def r13_pd_hover_clear():
        hub=renpy.get_screen('r13_hub')
        mouse=renpy.get_mouse_pos()
        focus=renpy.display.render.focus_at_point(int(mouse[0]),int(mouse[1]))
        state=dict(mouse=list(mouse),tooltip=GetTooltip(),hub_hint=hub.scope.get('hint') if hub else None,
            hub_present=hub is not None,focus_tooltip=focus.widget._get_tooltip() if focus is not None else None,
            focus_bounds=[focus.x,focus.y,focus.w,focus.h] if focus is not None else None)
        if state!=getattr(store,'r13_pd_last_hover_probe',None):
            store.r13_pd_last_hover_probe=state
            r13_pd_flow_log('actual-hover-state',state)
        # Keep both existing checks: a real displayed hint must not become a false PASS.
        return bool(hub and not state['tooltip'] and not state['hub_hint'])

    def r13_pd_choose_person(allow_no_content=False):
        # Use the same rendered Crop/AlphaMask that the production button uses.
        store.r13_pd_person_ready=False
        location=room13['location'];offset=r13_world_offset()
        actors=r13_stage_people(False);plates=r13_actor_nameplates(actors)
        # Actual current screen-space input regions, including UI overlays.
        regions=[]
        for f in renpy.display.focus.focus_list:
            if f.x is not None:
                regions.append(dict(bounds=[f.x,f.y,f.w,f.h],tooltip=f.widget._get_tooltip(),text=f.widget._tts_all(False)))
        r13_pd_flow_log('rendered-input-regions',dict(camera_offset=offset,regions=regions))
        def inside(px,py,rect):
            x,y,w,h=rect;return x<=px<x+w and y<=py<y+h
        for person in R13_PD_MAP_PEOPLE[location]:
            actor=next((a for a in actors if a['person']==person),None)
            if actor is None or r13_offer_for_person(person):continue
            probe=r13_pd_contact_probe(person)
            if not probe['plain_keys'] and not probe['contact_has_content'] and not allow_no_content:
                r13_pd_flow_log('resident-skipped-no-production-contact',probe)
                continue
            store.r13_pd_contact_allowed=probe['contact_has_content']
            r13_pd_flow_log('resident-contact-preflight',probe)
            x,y,w,h=actor['rect']
            mask=renpy.render(r13_actor_hit_mask(actor),w,h,1.2,1.2)
            blocked=[p['rect'] for p in plates]+[a['rect'] for a in actors if a['person']!=person]
            # Interior 3x3 mask acceptance avoids a single translucent crop-edge pixel.
            for ly in range(3,max(3,int(h)-3),4):
                for lx in range(3,max(3,int(w)-3),4):
                    px,py=x+lx,y+ly;sx=px-offset
                    if not (24<sx<1256 and 110<py<704):continue
                    if any(inside(px,py,r) for r in blocked):continue
                    if not all(mask.is_pixel_opaque(lx+dx,ly+dy) for dx in (-1,0,1) for dy in (-1,0,1)):continue
                    # Same rendered focus test used by Ren'Py 8.5.3 testfocus.find_position.
                    # This rejects actual HUD, object and nameplate interception, not a guessed UI band.
                    focus=renpy.display.render.focus_at_point(int(sx),int(py))
                    tooltip=focus.widget._get_tooltip() if focus is not None else None
                    expected=r13_person_caption(person)+' · 말 걸기'
                    if tooltip!=expected:continue
                    store.r13_pd_person=person;store.r13_pd_person_name=R13_NAMES[person]
                    store.r13_pd_person_x=int(sx);store.r13_pd_person_y=int(py)
                    store.r13_pd_person_ready=True
                    r13_pd_flow_log('resident-body-mask-click-target',dict(person=person,pose=actor['pose'],spec_file=(r13_acting_spec(person,actor['pose']) or {}).get('file'),actor_rect=actor['rect'],mask_local=[lx,ly],screen_click=[sx,py],mask_3x3_opaque=True,camera_offset=offset,focus_bounds=[focus.x,focus.y,focus.w,focus.h],focus_tooltip=tooltip,contact_probe=probe,method='production opaque hit mask plus actual topmost render.focus_at_point body-button tooltip; other actor/nameplate bounds excluded; no UI band bypass'))
                    return
        r13_pd_flow_log('resident-not-yet-clickable',dict(camera_offset=offset,people=[a['person'] for a in actors]))

    def r13_pd_approach_yes():
        screen=renpy.get_screen('r13_resident_approach')
        assert screen and screen.scope.get('ready',False)
        choices=screen.scope.get('choices')
        assert choices and choices[0][0], 'Actual approach positive choice missing'
        store.r13_pd_approach_text=choices[0][0]

    def r13_pd_choose_topic():
        assert renpy.get_screen('r13_topics') and r13_target==r13_pd_person
        available=r13_topics_in_order(r13_target)
        for key,spec,speech in r13_pd_plain_topics(r13_target):
            store.r13_pd_topic=key
            store.r13_pd_topic_source_title=r13_calendar_topic_title(key,spec)
            # Production side question buttons display the summarized caption, not this source title.
            store.r13_pd_topic_title=r13_question_summary(store.r13_pd_topic_source_title)
            store.r13_pd_expected_speech=speech
            r13_pd_flow_log('live-topic-ui-target',dict(person=r13_target,topic=key,source_title=store.r13_pd_topic_source_title,title=store.r13_pd_topic_title,expected_resident_lines=speech,available_keys=[k for k,_ in available]))
            return
        raise AssertionError(('MISSING_DIALOGUE_COVERAGE: no available unread plain topic with resident speech',r13_target,[k for k,_ in available]))

    def r13_pd_topic_say_ready():
        screen=renpy.get_screen('say')
        packet=getattr(store,'r13_packet',None)
        return bool(screen and getattr(store,'r13_topic',None)==getattr(store,'r13_pd_topic',None) and packet and packet[0]==r13_pd_person and packet[1] in r13_pd_expected_speech)

    def r13_pd_assert_topic_say():
        assert r13_pd_topic_say_ready(), 'Selected topic resident speech not reached'
        screen=renpy.get_screen('say');scope=screen.scope
        what=renpy.get_displayable('say','what');who=renpy.get_displayable('say','who')
        expected_name=r13_speaker_label(R13_NAMES[r13_pd_person])
        assert scope.get('who')==expected_name,(scope.get('who'),expected_name)
        assert scope.get('what') and what is not None and who is not None, dict(packet=list(r13_packet),who=scope.get('who'),what=scope.get('what'),what_widget=type(what).__name__,who_widget=type(who).__name__,widget_ids=sorted(screen.widgets))
        assert min(renpy.render(what,1280,720,1.2,1.2).get_size())>0
        assert 'r13_visitor' in renpy.get_showing_tags() and r13_motion_person==r13_pd_person
        bounds=renpy.get_image_bounds('r13_visitor')
        assert bounds and min(bounds[2:])>0
        r13_pd_flow_log('actual-topic-say-verified',dict(topic=r13_pd_topic,packet=list(r13_packet),who=scope.get('who'),what=scope.get('what'),page_index=r13_page_i,portrait_tag='r13_visitor',portrait_bounds=list(bounds),portrait_person=r13_motion_person,portrait_pose=r13_current_pose))

    def r13_pd_choose_object(allow_wait=False):
        store.r13_pd_object_ready=False
        location=room13['location'];offset=r13_world_offset();actors=r13_stage_people(False)
        objects=ROOM13['objects'][location]
        occupied=[p['rect'] for p in r13_actor_nameplates(actors)]
        actor_masks=[(a['rect'],renpy.render(r13_actor_hit_mask(a),a['rect'][2],a['rect'][3],1.2,1.2)) for a in actors]
        def inside(px,py,rect):
            x,y,w,h=rect;return x<=px<x+w and y<=py<y+h
        for key in R13_PD_MAP_OBJECTS[location]:
            spec=objects.get(key)
            if not spec or not r13_object_visible(spec):continue
            # Avoid contexts requiring a choice for this minimal click-return case.
            if r13_tool_available(key) or r13_object_actions(key) or (r13_context_wait(key) and not allow_wait) or r13_bed_available(key) or r13_bed_blocked_reason(key):continue
            x,y,w,h=spec['rect']
            for fy in (.5,.25,.75,.1,.9):
                for fx in (.5,.25,.75,.1,.9):
                    px,py=int(x+w*fx),int(y+h*fy);sx=px-offset
                    if not (24<sx<1256 and 110<py<590):continue
                    # Right-side menu/bed bands are excluded; key rack at y210 is not UI.
                    if sx>=1000 and (py<200 or 250<py<350):continue
                    if any(inside(px,py,r) for r in occupied):continue
                    if any(inside(px,py,r) and mask.is_pixel_opaque(px-r[0],py-r[1]) for r,mask in actor_masks):continue
                    if any(other!=key and r13_object_visible(ospec) and inside(px,py,ospec['rect']) for other,ospec in objects.items()):continue
                    flag='observed:'+location+':'+key
                    assert not r13_has(flag),('Object already observed in fresh fixture',flag)
                    store.r13_pd_object=key;store.r13_pd_observed_flag=flag
                    store.r13_pd_object_x=int(sx);store.r13_pd_object_y=py;store.r13_pd_object_ready=True
                    r13_pd_flow_log('object-click-target',dict(key=key,source_rect=spec['rect'],screen_click=[sx,py],method='runtime object rectangle; exclude rendered actor hit-mask pixels, nameplates, other object rectangles and UI bands'))
                    return
        r13_pd_flow_log('object-not-yet-clickable',dict(camera_offset=offset))

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
    screenshot "flow-baseline_post-00-entry-hint.png"
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    screenshot "flow-baseline_post-01-field.png"
    run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_person)
    assert eval (r13_pd_person_ready)
    click pos (r13_pd_person_x,r13_pd_person_y)
    advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
    assert eval (r13_target==r13_pd_person)
    pause 0.4
    if screen "r13_resident_approach":
        run Function(r13_pd_approach_yes)
        click expression r13_pd_approach_text
    advance until screen "r13_topics" timeout 40
    pause 0.4
    run Function(r13_pd_choose_topic)
    run Function(r13_pd_checkpoint,"topics-before-click-"+room13["location"])
    click expression r13_pd_topic_title
    advance until eval (r13_pd_topic_say_ready()) timeout 40
    pause 0.4
    run Function(r13_pd_assert_topic_say)
    screenshot "flow-baseline_post-02-resident-topic-say.png"
    advance until screen "r13_topics" timeout 40
    assert eval (r13_pd_topic in room13["read_topics"])
    pause 0.3
    click "돌아가기"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    assert eval (room13["location"]=="post")
    run Function(r13_pd_check_field,"returned-from-resident")
    run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_object)
    assert eval (r13_pd_object_ready)
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    run Function(r13_pd_flow_log,"actual-object-observed",dict(key=r13_pd_object,flag=r13_pd_observed_flag))
    screenshot "flow-baseline_post-03-object.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
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
    screenshot "flow-baseline_workshop-00-entry-hint.png"
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    screenshot "flow-baseline_workshop-01-field.png"
    run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_person)
    assert eval (r13_pd_person_ready)
    click pos (r13_pd_person_x,r13_pd_person_y)
    advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
    assert eval (r13_target==r13_pd_person)
    pause 0.4
    if screen "r13_resident_approach":
        run Function(r13_pd_approach_yes)
        click expression r13_pd_approach_text
    advance until screen "r13_topics" timeout 40
    pause 0.4
    run Function(r13_pd_choose_topic)
    run Function(r13_pd_checkpoint,"topics-before-click-"+room13["location"])
    click expression r13_pd_topic_title
    advance until eval (r13_pd_topic_say_ready()) timeout 40
    pause 0.4
    run Function(r13_pd_assert_topic_say)
    screenshot "flow-baseline_workshop-02-resident-topic-say.png"
    advance until screen "r13_topics" timeout 40
    assert eval (r13_pd_topic in room13["read_topics"])
    pause 0.3
    click "돌아가기"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    assert eval (room13["location"]=="workshop")
    run Function(r13_pd_check_field,"returned-from-resident")
    run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_object)
    assert eval (r13_pd_object_ready)
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    run Function(r13_pd_flow_log,"actual-object-observed",dict(key=r13_pd_object,flag=r13_pd_observed_flag))
    screenshot "flow-baseline_workshop-03-object.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
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
    screenshot "flow-baseline_inn-00-entry-hint.png"
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    screenshot "flow-baseline_inn-01-field.png"
    run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_person)
    assert eval (r13_pd_person_ready)
    click pos (r13_pd_person_x,r13_pd_person_y)
    advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
    assert eval (r13_target==r13_pd_person)
    pause 0.4
    if screen "r13_resident_approach":
        run Function(r13_pd_approach_yes)
        click expression r13_pd_approach_text
    advance until screen "r13_topics" timeout 40
    pause 0.4
    run Function(r13_pd_choose_topic)
    run Function(r13_pd_checkpoint,"topics-before-click-"+room13["location"])
    click expression r13_pd_topic_title
    advance until eval (r13_pd_topic_say_ready()) timeout 40
    pause 0.4
    run Function(r13_pd_assert_topic_say)
    screenshot "flow-baseline_inn-02-resident-topic-say.png"
    advance until screen "r13_topics" timeout 40
    assert eval (r13_pd_topic in room13["read_topics"])
    pause 0.3
    click "돌아가기"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    assert eval (room13["location"]=="inn")
    run Function(r13_pd_check_field,"returned-from-resident")
    run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_object)
    assert eval (r13_pd_object_ready)
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    run Function(r13_pd_flow_log,"actual-object-observed",dict(key=r13_pd_object,flag=r13_pd_observed_flag))
    screenshot "flow-baseline_inn-03-object.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
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
    screenshot "flow-proposed_post-00-entry-hint.png"
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    screenshot "flow-proposed_post-01-field.png"
    run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_person)
    assert eval (r13_pd_person_ready)
    click pos (r13_pd_person_x,r13_pd_person_y)
    advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
    assert eval (r13_target==r13_pd_person)
    pause 0.4
    if screen "r13_resident_approach":
        run Function(r13_pd_approach_yes)
        click expression r13_pd_approach_text
    advance until screen "r13_topics" timeout 40
    pause 0.4
    run Function(r13_pd_choose_topic)
    run Function(r13_pd_checkpoint,"topics-before-click-"+room13["location"])
    click expression r13_pd_topic_title
    advance until eval (r13_pd_topic_say_ready()) timeout 40
    pause 0.4
    run Function(r13_pd_assert_topic_say)
    screenshot "flow-proposed_post-02-resident-topic-say.png"
    advance until screen "r13_topics" timeout 40
    assert eval (r13_pd_topic in room13["read_topics"])
    pause 0.3
    click "돌아가기"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    assert eval (room13["location"]=="post")
    run Function(r13_pd_check_field,"returned-from-resident")
    run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_object)
    assert eval (r13_pd_object_ready)
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    run Function(r13_pd_flow_log,"actual-object-observed",dict(key=r13_pd_object,flag=r13_pd_observed_flag))
    screenshot "flow-proposed_post-03-object.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
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
    screenshot "flow-proposed_workshop-00-entry-hint.png"
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    screenshot "flow-proposed_workshop-01-field.png"
    run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_person)
    assert eval (r13_pd_person_ready)
    click pos (r13_pd_person_x,r13_pd_person_y)
    advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
    assert eval (r13_target==r13_pd_person)
    pause 0.4
    if screen "r13_resident_approach":
        run Function(r13_pd_approach_yes)
        click expression r13_pd_approach_text
    advance until screen "r13_topics" timeout 40
    pause 0.4
    run Function(r13_pd_choose_topic)
    run Function(r13_pd_checkpoint,"topics-before-click-"+room13["location"])
    click expression r13_pd_topic_title
    advance until eval (r13_pd_topic_say_ready()) timeout 40
    pause 0.4
    run Function(r13_pd_assert_topic_say)
    screenshot "flow-proposed_workshop-02-resident-topic-say.png"
    advance until screen "r13_topics" timeout 40
    assert eval (r13_pd_topic in room13["read_topics"])
    pause 0.3
    click "돌아가기"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    assert eval (room13["location"]=="workshop")
    run Function(r13_pd_check_field,"returned-from-resident")
    run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_object)
    assert eval (r13_pd_object_ready)
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    run Function(r13_pd_flow_log,"actual-object-observed",dict(key=r13_pd_object,flag=r13_pd_observed_flag))
    screenshot "flow-proposed_workshop-03-object.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
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
    screenshot "flow-proposed_inn-00-entry-hint.png"
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    screenshot "flow-proposed_inn-01-field.png"
    run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_person)
    if eval (not r13_pd_person_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_person)
    assert eval (r13_pd_person_ready)
    click pos (r13_pd_person_x,r13_pd_person_y)
    advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
    assert eval (r13_target==r13_pd_person)
    pause 0.4
    if screen "r13_resident_approach":
        run Function(r13_pd_approach_yes)
        click expression r13_pd_approach_text
    advance until screen "r13_topics" timeout 40
    pause 0.4
    run Function(r13_pd_choose_topic)
    run Function(r13_pd_checkpoint,"topics-before-click-"+room13["location"])
    click expression r13_pd_topic_title
    advance until eval (r13_pd_topic_say_ready()) timeout 40
    pause 0.4
    run Function(r13_pd_assert_topic_say)
    screenshot "flow-proposed_inn-02-resident-topic-say.png"
    advance until screen "r13_topics" timeout 40
    assert eval (r13_pd_topic in room13["read_topics"])
    pause 0.3
    click "돌아가기"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    assert eval (room13["location"]=="inn")
    run Function(r13_pd_check_field,"returned-from-resident")
    run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_object)
    if eval (not r13_pd_object_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_object)
    assert eval (r13_pd_object_ready)
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    run Function(r13_pd_flow_log,"actual-object-observed",dict(key=r13_pd_object,flag=r13_pd_observed_flag))
    screenshot "flow-proposed_inn-03-object.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    assert eval (room13["location"]=="inn" and room13["day"]==2 and room13["period"]==0)
    run Function(r13_pd_check_field,"returned-from-object")
    screenshot "flow-proposed_inn-04-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_pd_end)
