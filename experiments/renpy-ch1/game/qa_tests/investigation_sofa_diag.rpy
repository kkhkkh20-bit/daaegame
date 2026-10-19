# LOCAL CANDIDATE QA. NOT RUN. Depends on existing production placement diagnostic helpers.
init 999 python:
    def r13_sofa_begin(person):
        r13_pd_begin('local-sofa-placement-'+person)
        store.r13_sofa_person=person
        store.r13_sofa_saved_people=R13_PD_MAP_PEOPLE['inn']
        R13_PD_MAP_PEOPLE['inn']=(person,)
        store.r13_sofa_outcome=dict(body='PENDING',dialogue='NOT_VERIFIED',route='PENDING',visual_acceptance=False)

    def r13_sofa_geometry(step):
        assert room13['location']=='inn' and room13['day']==2 and room13['period']==0
        actors={a['person']:a for a in r13_stage_people(False)}
        assert all(p in actors for p in ('resident_tosil','resident_nubi')), 'Do not fabricate joint presence'
        expected={'resident_nubi':('map27_in_1',(420,535),226), 'resident_tosil':('living_thermos',(535,535),215)}
        for person,(pose,foot,height) in expected.items():
            actor=actors[person];row=r13_pd_row(actor,'r13_hub')
            assert actor['pose']==pose and actor['height']==height
            assert all(abs(a-b)<=1.5 for a,b in zip(row['foot_world'],foot))
            assert len(actor.get('map27_occlusion',[]))==4
            assert not actor.get('map27_keepouts')
            # Verify foreground pixels cannot hit the concealed body, not just polygon metadata.
            x,y,w,h=actor['rect']
            rendered=renpy.render(r13_actor_hit_mask(actor),w,h,1.2,1.2)
            rejected=[]
            for polygon in actor['map27_occlusion']:
                furniture=renpy.render(R13FurnitureMask(polygon,size=(w,h),origin=(x,y)),w,h,1.2,1.2)
                for ly in range(2,int(h)-2,3):
                    for lx in range(2,int(w)-2,3):
                        if furniture.is_pixel_opaque(lx,ly):
                            # Diagnose before preserving the strict rejection below.
                            # SDK8.5.3 GL2 returns alpha0..255 here, not full-opacity boolean.
                            if rendered.is_pixel_opaque(lx,ly):
                                offset=r13_world_offset();wx,wy=x+lx,y+ly;sx=wx-offset
                                focus=renpy.display.render.focus_at_point(int(sx),int(wy)) if 0<=sx<1280 else None
                                samples=[]
                                for dy in (-1,0,1):
                                    for dx in (-1,0,1):
                                        samples.append(dict(local=[lx+dx,ly+dy],furniture_alpha=int(furniture.is_pixel_opaque(lx+dx,ly+dy)),hit_alpha=int(rendered.is_pixel_opaque(lx+dx,ly+dy))))
                                r13_pd_flow_log('sofa-mask-strict-failure-detail',dict(step=step,person=person,
                                    actor_rect=actor['rect'],world_point=[wx,wy],screen_point=[sx,wy],polygon=polygon,
                                    mask_samples=samples,renderer=str(renpy.get_renderer_info()),
                                    expected_actor_tooltip=r13_person_caption(person)+' · 말 걸기',
                                    actual_topmost_tooltip=focus.widget._get_tooltip() if focus is not None else None,
                                    actual_topmost_bounds=[focus.x,focus.y,focus.w,focus.h] if focus is not None else None,
                                    strict_rejection_preserved=True,visual_acceptance=False))
                            assert not rendered.is_pixel_opaque(lx,ly), ('Masked furniture remains clickable',person,lx,ly)
                            if len(rejected)<12:rejected.append([x+lx,y+ly])
            assert rejected, ('No foreground overlap tested',person)
            r13_pd_flow_log('sofa-furniture-hit-rejection',dict(person=person,world_points=rejected))
            r13_pd_flow_log('sofa-person-geometry',dict(step=step,person=person,row=row,visual_acceptance=False))
        r13_pd_target_render(r13_sofa_person,expected[r13_sofa_person][0],step)

    def r13_sofa_result():
        r13_sofa_geometry('final')
        r13_pd_flow_log('sofa-result',dict(outcome=dict(r13_sofa_outcome),person=r13_sofa_person))
        R13_PD_MAP_PEOPLE['inn']=r13_sofa_saved_people
        r13_pd_end()

testcase investigation_sofa_tosil:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_sofa_begin,'resident_tosil')
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_flow_log,"sofa-initial-camera",dict(camera_offset=r13_world_offset(),layout_initial_x=r13_layout().get('initial_x',0),world_width=r13_world_width(),state=r13_pd_copy.deepcopy(room13)))
    # inn's authored initial_x is640; reach zero with real pan controls.
    if eval (r13_world_offset()>0):
        $ r13_s2_before_pan=r13_world_offset()
        click "‹"
        pause 0.5
        assert eval (r13_world_offset()<r13_s2_before_pan)
    if eval (r13_world_offset()>0):
        $ r13_s2_before_pan=r13_world_offset()
        click "‹"
        pause 0.5
        assert eval (r13_world_offset()<r13_s2_before_pan)
    assert eval (r13_world_offset()==0)
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Function(r13_pd_check_field,"sofa-camera-zero")
    screenshot "investigation_sofa_tosil-sofa-target-camera-zero-before-assert.png"
    run Function(r13_sofa_geometry,"sofa-target-camera-zero")
    screenshot "sofa-tosil-01-camera-zero.png"
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    assert eval (r13_world_offset()==r13_world_width()-1280)
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Function(r13_pd_check_field,"sofa-camera-right")
    screenshot "investigation_sofa_tosil-sofa-target-camera-right-before-assert.png"
    run Function(r13_sofa_geometry,"sofa-target-camera-right")
    screenshot "sofa-tosil-02-camera-right.png"
    run Function(r13_pd_choose_person,True)
    assert eval (not r13_pd_person_ready)
    # Both candidates are left of camera-right; no phantom offscreen input target.
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person,True)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person,True)
    assert eval (r13_pd_person_ready and r13_pd_person=='resident_tosil')
    screenshot "investigation_sofa_tosil-sofa-actual-body-click-viewport-before-assert.png"
    run Function(r13_sofa_geometry,"sofa-actual-body-click-viewport")
    click pos (r13_pd_person_x,r13_pd_person_y)
    pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None or renpy.get_screen("notify") is not None) timeout 5
    if eval (r13_pd_contact_allowed):
        if screen "say":
            run Function(r13_pd_log_opening,"sofa-actual-notice")
            screenshot "sofa-tosil-03-first-notice.png"
        advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
        assert eval (r13_target==r13_pd_person)
        $ r13_sofa_outcome.update(body='ACTUAL_BODY_DISPATCH',route='NORMAL_CONTACT_MENU')
        pause 0.4
        if screen "r13_resident_approach":
            run Function(r13_pd_approach_yes)
            run Function(r13_pd_flow_log,"sofa-live-approach-caption",dict(source_title=r13_pd_approach_text,display_title=r13_question_summary(r13_pd_approach_text)))
            click expression r13_question_summary(r13_pd_approach_text)
        advance until screen "r13_topics" timeout 40
        pause 0.4
        if eval (bool(r13_pd_plain_topics(r13_pd_person))):
            run Function(r13_pd_choose_topic)
            click expression r13_pd_topic_title
            advance until eval (r13_pd_topic_say_ready()) timeout 40
            pause 0.4
            run Function(r13_pd_assert_topic_say)
            screenshot "sofa-tosil-04-actual-topic-say.png"
            advance until screen "r13_topics" timeout 40
            assert eval (r13_pd_topic in room13['read_topics'])
            $ r13_sofa_outcome['dialogue']='ACTUAL_PLAIN_TOPIC_SAY_COMPLETED'
        else:
            run Function(r13_pd_flow_log,"sofa-normal-menu-no-plain-topic",dict(available=[k for k,_ in r13_topics_in_order(r13_pd_person)],dialogue_verified=False))
            $ r13_sofa_outcome['dialogue']='NO_ELIGIBLE_PLAIN_TOPIC_NORMAL_MENU_VERIFIED'
            screenshot "sofa-tosil-04-normal-menu.png"
        pause 0.3
        click "돌아가기"
        advance until screen "r13_hub" timeout 40
    else:
        assert screen "notify"
        assert eval (renpy.get_screen("notify").scope.get("message")=="지금은 %s에게 더 물어볼 이야기가 없다."%R13_NAMES[r13_pd_person])
        $ r13_sofa_outcome.update(body='ACTUAL_BODY_DISPATCH',route='GENUINE_NO_CONTENT_NOTIFY',dialogue='NOT_AVAILABLE_NOT_VERIFIED')
        run Function(r13_pd_flow_log,"sofa-genuine-no-content",dict(person=r13_pd_person,probe=r13_pd_contact_probe(r13_pd_person),outcome=dict(r13_sofa_outcome)))
        screenshot "sofa-tosil-04-production-no-content.png"
        pause until eval (renpy.get_screen("notify") is None) timeout 5
        assert screen "r13_hub"
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Function(r13_pd_check_field,"sofa-returned-field")
    screenshot "investigation_sofa_tosil-sofa-target-returned-before-assert.png"
    run Function(r13_sofa_geometry,"sofa-target-returned")
    screenshot "sofa-tosil-05-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_sofa_result)


testcase investigation_sofa_nubi:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_sofa_begin,'resident_nubi')
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_flow_log,"sofa-initial-camera",dict(camera_offset=r13_world_offset(),layout_initial_x=r13_layout().get('initial_x',0),world_width=r13_world_width(),state=r13_pd_copy.deepcopy(room13)))
    # inn's authored initial_x is640; reach zero with real pan controls.
    if eval (r13_world_offset()>0):
        $ r13_s2_before_pan=r13_world_offset()
        click "‹"
        pause 0.5
        assert eval (r13_world_offset()<r13_s2_before_pan)
    if eval (r13_world_offset()>0):
        $ r13_s2_before_pan=r13_world_offset()
        click "‹"
        pause 0.5
        assert eval (r13_world_offset()<r13_s2_before_pan)
    assert eval (r13_world_offset()==0)
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Function(r13_pd_check_field,"sofa-camera-zero")
    screenshot "investigation_sofa_nubi-sofa-target-camera-zero-before-assert.png"
    run Function(r13_sofa_geometry,"sofa-target-camera-zero")
    screenshot "sofa-nubi-01-camera-zero.png"
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    assert eval (r13_world_offset()==r13_world_width()-1280)
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Function(r13_pd_check_field,"sofa-camera-right")
    screenshot "investigation_sofa_nubi-sofa-target-camera-right-before-assert.png"
    run Function(r13_sofa_geometry,"sofa-target-camera-right")
    screenshot "sofa-nubi-02-camera-right.png"
    run Function(r13_pd_choose_person,True)
    assert eval (not r13_pd_person_ready)
    # Both candidates are left of camera-right; no phantom offscreen input target.
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person,True)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person,True)
    assert eval (r13_pd_person_ready and r13_pd_person=='resident_nubi')
    screenshot "investigation_sofa_nubi-sofa-actual-body-click-viewport-before-assert.png"
    run Function(r13_sofa_geometry,"sofa-actual-body-click-viewport")
    click pos (r13_pd_person_x,r13_pd_person_y)
    pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None or renpy.get_screen("notify") is not None) timeout 5
    if eval (r13_pd_contact_allowed):
        if screen "say":
            run Function(r13_pd_log_opening,"sofa-actual-notice")
            screenshot "sofa-nubi-03-first-notice.png"
        advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
        assert eval (r13_target==r13_pd_person)
        $ r13_sofa_outcome.update(body='ACTUAL_BODY_DISPATCH',route='NORMAL_CONTACT_MENU')
        pause 0.4
        if screen "r13_resident_approach":
            run Function(r13_pd_approach_yes)
            run Function(r13_pd_flow_log,"sofa-live-approach-caption",dict(source_title=r13_pd_approach_text,display_title=r13_question_summary(r13_pd_approach_text)))
            click expression r13_question_summary(r13_pd_approach_text)
        advance until screen "r13_topics" timeout 40
        pause 0.4
        if eval (bool(r13_pd_plain_topics(r13_pd_person))):
            run Function(r13_pd_choose_topic)
            click expression r13_pd_topic_title
            advance until eval (r13_pd_topic_say_ready()) timeout 40
            pause 0.4
            run Function(r13_pd_assert_topic_say)
            screenshot "sofa-nubi-04-actual-topic-say.png"
            advance until screen "r13_topics" timeout 40
            assert eval (r13_pd_topic in room13['read_topics'])
            $ r13_sofa_outcome['dialogue']='ACTUAL_PLAIN_TOPIC_SAY_COMPLETED'
        else:
            run Function(r13_pd_flow_log,"sofa-normal-menu-no-plain-topic",dict(available=[k for k,_ in r13_topics_in_order(r13_pd_person)],dialogue_verified=False))
            $ r13_sofa_outcome['dialogue']='NO_ELIGIBLE_PLAIN_TOPIC_NORMAL_MENU_VERIFIED'
            screenshot "sofa-nubi-04-normal-menu.png"
        pause 0.3
        click "돌아가기"
        advance until screen "r13_hub" timeout 40
    else:
        assert screen "notify"
        assert eval (renpy.get_screen("notify").scope.get("message")=="지금은 %s에게 더 물어볼 이야기가 없다."%R13_NAMES[r13_pd_person])
        $ r13_sofa_outcome.update(body='ACTUAL_BODY_DISPATCH',route='GENUINE_NO_CONTENT_NOTIFY',dialogue='NOT_AVAILABLE_NOT_VERIFIED')
        run Function(r13_pd_flow_log,"sofa-genuine-no-content",dict(person=r13_pd_person,probe=r13_pd_contact_probe(r13_pd_person),outcome=dict(r13_sofa_outcome)))
        screenshot "sofa-nubi-04-production-no-content.png"
        pause until eval (renpy.get_screen("notify") is None) timeout 5
        assert screen "r13_hub"
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Function(r13_pd_check_field,"sofa-returned-field")
    screenshot "investigation_sofa_nubi-sofa-target-returned-before-assert.png"
    run Function(r13_sofa_geometry,"sofa-target-returned")
    screenshot "sofa-nubi-05-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_sofa_result)

