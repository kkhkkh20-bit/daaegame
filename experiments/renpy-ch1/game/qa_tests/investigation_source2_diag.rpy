# QA-only proposed source2 specimens, NOT approval of all investigation art or a 2x2 pipeline.
init 999 python:
    R13_S2_EXPECTED = {'resident_ttadak': {'file': 'assets/investigation-source2/ttadak-doorframe-v1.webp', 'crop': [30, 82, 967, 1391], 'nearest': True, 'foot': [517.75, 1390], 'head': [300, 0, 430, 450], 'contact': 'standing', 'reviewed': False, 'map_action': True, 'stature_ratio': 1.0, 'source_sha256': 'c8f2b481ff3a4d4fb8e3231b586541f649a912455ccea25cad81b1d32145f89b', 'native_detail': True}, 'resident_tosil': {'file': 'assets/investigation-source2/tosil-thermos-v1.webp', 'crop': [153, 17, 733, 1483], 'nearest': True, 'foot': [418.0, 1482], 'head': [0, 0, 733, 630], 'contact': 'standing', 'reviewed': False, 'map_action': True, 'stature_ratio': 1.0, 'source_sha256': '7c4ac82394064772fc0d1db6176fd467391d9cbf20f9a30eea29f03294b763ff', 'native_detail': True}}

    def r13_s2_begin(person,pose,period,height,foot):
        r13_pd_begin('proposed-source2-'+person)
        store.r13_s2_person=person;store.r13_s2_pose=pose;store.r13_s2_period=period
        store.r13_s2_height=height;store.r13_s2_foot=foot
        store.r13_s2_saved_people=R13_PD_MAP_PEOPLE['inn']
        R13_PD_MAP_PEOPLE['inn']=(person,)
        store.r13_s2_outcome=dict(body='PENDING',dialogue='NOT_VERIFIED',route='PENDING',visual_acceptance=False,full_2x2_approval=False)

    def r13_s2_geometry(step):
        assert room13['location']=='inn' and room13['day']==2 and room13['period']==r13_s2_period
        actor=next(a for a in r13_stage_people(False) if a['person']==r13_s2_person)
        assert actor['pose']==r13_s2_pose,(actor['pose'],r13_s2_pose)
        spec=r13_acting_spec(r13_s2_person,r13_s2_pose)
        expected=R13_S2_EXPECTED[r13_s2_person]
        for key in ('file','crop','foot','head','source_sha256','native_detail','stature_ratio'):
            assert spec.get(key)==expected[key],('Wrong source2 registry',key,spec.get(key),expected[key])
        row=r13_pd_row(actor,'r13_hub')
        assert actor['height']==r13_s2_height,('Unexpected stature change',actor['height'],r13_s2_height)
        assert all(abs(a-b)<=1.5 for a,b in zip(row['foot_world'],r13_s2_foot)),('World foot moved',row['foot_world'],r13_s2_foot)
        r13_pd_target_render(r13_s2_person,r13_s2_pose,step)
        r13_pd_flow_log('source2-contact-review',dict(target=row,door_rect=ROOM13['objects']['inn']['door']['rect'],
            other_actors=[dict(person=a['person'],pose=a['pose'],rect=a['rect'],depth=a['depth']) for a in r13_stage_people(False) if a['person']!=r13_s2_person],
            review=('doorframe hand-to-frame contact and feet' if r13_s2_person=='resident_ttadak' else 'child scale relative to scene depth; thermos and hand integrity'),
            no_production_geometry_override=True,visual_acceptance=False,full_2x2_approval=False))

    def r13_s2_result():
        assert room13['location']=='inn' and room13['day']==2 and room13['period']==r13_s2_period
        r13_pd_flow_log('source2-result',dict(outcome=dict(r13_s2_outcome),person=r13_s2_person,pose=r13_s2_pose))
        R13_PD_MAP_PEOPLE['inn']=r13_s2_saved_people
        r13_pd_end()

testcase investigation_source2_ttadak:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_s2_begin,'resident_ttadak','living_doorframe',1,196,(1043, 472))
    run Call("r13_qa_roam",dict(day=2,period=1,location="inn",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    # Normal day2 afternoon arrival: resolve Nubi's actual offer through its UI.
    # Never seed ev_q_done, change the date, or jump past the production event.
    advance until screen "choice" timeout 40
    pause until eval (renpy.get_screen("choice").scope.get("choice_ready",False)) timeout 5
    assert eval (room13['day']==2 and room13['period']==1 and room13['location']=='inn' and r13_has('ev_q_done'))
    assert eval ('거절한다' in [item.caption for item in renpy.get_screen('choice').scope['items']])
    run Function(r13_pd_flow_log,"source2-real-arrival-offer",dict(choices=[item.caption for item in renpy.get_screen('choice').scope['items']],state=r13_pd_copy.deepcopy(room13),camera_offset=r13_world_offset()))
    screenshot "source2-ttadak-00-real-arrival-offer.png"
    click "거절한다"
    advance until screen "r13_hub" timeout 40
    assert eval (room13['day']==2 and room13['period']==1 and room13['location']=='inn')
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_flow_log,"source2-initial-camera",dict(camera_offset=r13_world_offset(),layout_initial_x=r13_layout().get('initial_x',0),world_width=r13_world_width(),state=r13_pd_copy.deepcopy(room13)))
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
    run Function(r13_pd_check_field,"source2-camera-zero")
    run Function(r13_s2_geometry,"source2-target-camera-zero")
    screenshot "source2-ttadak-01-camera-zero.png"
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
    run Function(r13_pd_check_field,"source2-camera-right")
    run Function(r13_s2_geometry,"source2-target-camera-right")
    screenshot "source2-ttadak-02-camera-right.png"
    run Function(r13_pd_choose_person,True)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person,True)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person,True)
    assert eval (r13_pd_person_ready and r13_pd_person=='resident_ttadak')
    run Function(r13_s2_geometry,"source2-actual-body-click-viewport")
    click pos (r13_pd_person_x,r13_pd_person_y)
    pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None or renpy.get_screen("notify") is not None) timeout 5
    if eval (r13_pd_contact_allowed):
        if screen "say":
            run Function(r13_pd_log_opening,"source2-actual-notice")
            screenshot "source2-ttadak-03-first-notice.png"
        advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
        assert eval (r13_target==r13_pd_person)
        $ r13_s2_outcome.update(body='ACTUAL_BODY_DISPATCH',route='NORMAL_CONTACT_MENU')
        pause 0.4
        if screen "r13_resident_approach":
            run Function(r13_pd_approach_yes)
            click expression r13_pd_approach_text
        advance until screen "r13_topics" timeout 40
        pause 0.4
        if eval (bool(r13_pd_plain_topics(r13_pd_person))):
            run Function(r13_pd_choose_topic)
            click expression r13_pd_topic_title
            advance until eval (r13_pd_topic_say_ready()) timeout 40
            pause 0.4
            run Function(r13_pd_assert_topic_say)
            screenshot "source2-ttadak-04-actual-topic-say.png"
            advance until screen "r13_topics" timeout 40
            assert eval (r13_pd_topic in room13['read_topics'])
            $ r13_s2_outcome['dialogue']='ACTUAL_PLAIN_TOPIC_SAY_COMPLETED'
        else:
            run Function(r13_pd_flow_log,"source2-normal-menu-no-plain-topic",dict(available=[k for k,_ in r13_topics_in_order(r13_pd_person)],dialogue_verified=False))
            $ r13_s2_outcome['dialogue']='NO_ELIGIBLE_PLAIN_TOPIC_NORMAL_MENU_VERIFIED'
            screenshot "source2-ttadak-04-normal-menu.png"
        pause 0.3
        click "돌아가기"
        advance until screen "r13_hub" timeout 40
    else:
        assert screen "notify"
        assert eval (renpy.get_screen("notify").scope.get("message")=="지금은 %s에게 더 물어볼 이야기가 없다."%R13_NAMES[r13_pd_person])
        $ r13_s2_outcome.update(body='ACTUAL_BODY_DISPATCH',route='GENUINE_NO_CONTENT_NOTIFY',dialogue='NOT_AVAILABLE_NOT_VERIFIED')
        run Function(r13_pd_flow_log,"source2-genuine-no-content",dict(person=r13_pd_person,probe=r13_pd_contact_probe(r13_pd_person),outcome=dict(r13_s2_outcome)))
        screenshot "source2-ttadak-04-production-no-content.png"
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
    run Function(r13_pd_check_field,"source2-returned-field")
    run Function(r13_s2_geometry,"source2-target-returned")
    screenshot "source2-ttadak-05-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_s2_result)

testcase investigation_source2_tosil:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_s2_begin,'resident_tosil','living_thermos',0,265,(485, 706))
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
    run Function(r13_pd_flow_log,"source2-initial-camera",dict(camera_offset=r13_world_offset(),layout_initial_x=r13_layout().get('initial_x',0),world_width=r13_world_width(),state=r13_pd_copy.deepcopy(room13)))
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
    run Function(r13_pd_check_field,"source2-camera-zero")
    run Function(r13_s2_geometry,"source2-target-camera-zero")
    screenshot "source2-tosil-01-camera-zero.png"
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
    run Function(r13_pd_check_field,"source2-camera-right")
    run Function(r13_s2_geometry,"source2-target-camera-right")
    screenshot "source2-tosil-02-camera-right.png"
    run Function(r13_pd_choose_person,True)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person,True)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person,True)
    assert eval (r13_pd_person_ready and r13_pd_person=='resident_tosil')
    run Function(r13_s2_geometry,"source2-actual-body-click-viewport")
    click pos (r13_pd_person_x,r13_pd_person_y)
    pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None or renpy.get_screen("notify") is not None) timeout 5
    if eval (r13_pd_contact_allowed):
        if screen "say":
            run Function(r13_pd_log_opening,"source2-actual-notice")
            screenshot "source2-tosil-03-first-notice.png"
        advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
        assert eval (r13_target==r13_pd_person)
        $ r13_s2_outcome.update(body='ACTUAL_BODY_DISPATCH',route='NORMAL_CONTACT_MENU')
        pause 0.4
        if screen "r13_resident_approach":
            run Function(r13_pd_approach_yes)
            click expression r13_pd_approach_text
        advance until screen "r13_topics" timeout 40
        pause 0.4
        if eval (bool(r13_pd_plain_topics(r13_pd_person))):
            run Function(r13_pd_choose_topic)
            click expression r13_pd_topic_title
            advance until eval (r13_pd_topic_say_ready()) timeout 40
            pause 0.4
            run Function(r13_pd_assert_topic_say)
            screenshot "source2-tosil-04-actual-topic-say.png"
            advance until screen "r13_topics" timeout 40
            assert eval (r13_pd_topic in room13['read_topics'])
            $ r13_s2_outcome['dialogue']='ACTUAL_PLAIN_TOPIC_SAY_COMPLETED'
        else:
            run Function(r13_pd_flow_log,"source2-normal-menu-no-plain-topic",dict(available=[k for k,_ in r13_topics_in_order(r13_pd_person)],dialogue_verified=False))
            $ r13_s2_outcome['dialogue']='NO_ELIGIBLE_PLAIN_TOPIC_NORMAL_MENU_VERIFIED'
            screenshot "source2-tosil-04-normal-menu.png"
        pause 0.3
        click "돌아가기"
        advance until screen "r13_hub" timeout 40
    else:
        assert screen "notify"
        assert eval (renpy.get_screen("notify").scope.get("message")=="지금은 %s에게 더 물어볼 이야기가 없다."%R13_NAMES[r13_pd_person])
        $ r13_s2_outcome.update(body='ACTUAL_BODY_DISPATCH',route='GENUINE_NO_CONTENT_NOTIFY',dialogue='NOT_AVAILABLE_NOT_VERIFIED')
        run Function(r13_pd_flow_log,"source2-genuine-no-content",dict(person=r13_pd_person,probe=r13_pd_contact_probe(r13_pd_person),outcome=dict(r13_s2_outcome)))
        screenshot "source2-tosil-04-production-no-content.png"
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
    run Function(r13_pd_check_field,"source2-returned-field")
    run Function(r13_s2_geometry,"source2-target-returned")
    screenshot "source2-tosil-05-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_s2_result)

