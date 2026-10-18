# QA-only actual selection, body click and truthful work-pose checks.


testcase investigation_job_chorong:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_pd_begin,"proposed-job-chorong")
    $ r13_pd_saved_preference=R13_PD_MAP_PEOPLE["workshop"]
    $ R13_PD_MAP_PEOPLE["workshop"]=("resident_lamplighter",)
    run Call("r13_qa_roam",dict(day=2,period=0,location="workshop",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    screenshot "job-chorong-00-entry-hint.png"
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    assert eval (r13_world_offset()==0)
    run Function(r13_pd_target_render,"resident_lamplighter","job_replace_lightstone","target-camera-zero")
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "job-chorong-01-field.png"
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
    assert eval (r13_pd_person_ready and r13_pd_person=="resident_lamplighter")
    assert eval (any(a["person"]=="resident_lamplighter" and a["pose"]=="job_replace_lightstone" and a.get("activity")=="가져온 등을 손에 들고 빛돌을 갈아 끼운다." for a in r13_stage_people(False)))
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "job-chorong-01b-selected-visible.png"
    click pos (r13_pd_person_x,r13_pd_person_y)
    pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 5
    if screen "say":
        run Function(r13_pd_log_opening,"actual-first-contact-notice")
        screenshot "job-chorong-01c-first-notice.png"
    advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
    assert eval (r13_target==r13_pd_person)
    pause 0.4
    if screen "r13_resident_approach":
        run Function(r13_pd_approach_yes)
        screenshot "job-chorong-01d-approach.png"
        click expression r13_pd_approach_text
        pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_topics") is not None) timeout 5
        if screen "say":
            run Function(r13_pd_log_opening,"actual-first-contact-opening")
            screenshot "job-chorong-01e-opening.png"
    advance until screen "r13_topics" timeout 40
    pause 0.4
    run Function(r13_pd_choose_topic)
    run Function(r13_pd_checkpoint,"topics-before-click-"+room13["location"])
    click expression r13_pd_topic_title
    advance until eval (r13_pd_topic_say_ready()) timeout 40
    pause 0.4
    run Function(r13_pd_assert_topic_say)
    screenshot "job-chorong-02-resident-topic-say.png"
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
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "job-chorong-03-returned.png"
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    assert eval (r13_world_offset()==(r13_world_width()-1280 if room13["location"]=="workshop" else 0))
    run Function(r13_pd_check_field,"job-right-camera-end")
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Function(r13_pd_target_render,"resident_lamplighter","job_replace_lightstone","target-camera-right-end")
    screenshot "job-chorong-04-right-camera-end.png"
    $ R13_PD_MAP_PEOPLE["workshop"]=r13_pd_saved_preference
    run Hide("r13_qa_pixel_variant")
    run Function(r13_pd_end)


testcase investigation_job_musoe:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_pd_begin,"proposed-job-musoe")
    $ r13_pd_saved_preference=R13_PD_MAP_PEOPLE["workshop"]
    $ R13_PD_MAP_PEOPLE["workshop"]=("resident_musoe",)
    run Call("r13_qa_roam",dict(day=2,period=0,location="workshop",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    screenshot "job-musoe-00-entry-hint.png"
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    assert eval (r13_world_offset()==0)
    run Function(r13_pd_target_render,"resident_musoe","job_inspect_old_tool","target-camera-zero")
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "job-musoe-01-field.png"
    run Function(r13_pd_choose_person,True)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person,True)
    if eval (not r13_pd_person_ready and r13_world_offset()>0):
        click "‹"
        pause 0.5
        run Function(r13_pd_choose_person,True)
    if eval (not r13_pd_person_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_person,True)
    if eval (not r13_pd_person_ready and r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
        run Function(r13_pd_choose_person,True)
    assert eval (r13_pd_person_ready and r13_pd_person=="resident_musoe")
    assert eval (any(a["person"]=="resident_musoe" and a["pose"]=="job_inspect_old_tool" and a.get("activity")=="오래 쓰던 손도구의 머리를 손끝으로 살핀다." for a in r13_stage_people(False)))
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "job-musoe-01b-selected-visible.png"
    click pos (r13_pd_person_x,r13_pd_person_y)
    pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None or renpy.get_screen("notify") is not None) timeout 5
    if eval (r13_pd_contact_allowed):
        if screen "say":
            run Function(r13_pd_log_opening,"actual-first-contact-notice")
            screenshot "job-musoe-01c-first-notice.png"
        advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
        assert eval (r13_target==r13_pd_person)
        pause 0.4
        if screen "r13_resident_approach":
            run Function(r13_pd_approach_yes)
            screenshot "job-musoe-01d-approach.png"
            click expression r13_pd_approach_text
            pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_topics") is not None) timeout 5
            if screen "say":
                run Function(r13_pd_log_opening,"actual-first-contact-opening")
                screenshot "job-musoe-01e-opening.png"
        advance until screen "r13_topics" timeout 40
        pause 0.4
        run Function(r13_pd_choose_topic)
        run Function(r13_pd_checkpoint,"topics-before-click-"+room13["location"])
        click expression r13_pd_topic_title
        advance until eval (r13_pd_topic_say_ready()) timeout 40
        pause 0.4
        run Function(r13_pd_assert_topic_say)
        screenshot "job-musoe-02-resident-topic-say.png"
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
        move pos (640,20)
        pause 0.2
        pause until eval (r13_pd_hover_clear()) timeout 3
        screenshot "job-musoe-03-returned.png"
    else:
        assert screen "notify"
        assert eval (renpy.get_screen("notify").scope.get("message")=="지금은 %s에게 더 물어볼 이야기가 없다."%R13_NAMES[r13_pd_person])
        run Function(r13_pd_flow_log,"actual-body-click-no-conversation",dict(person=r13_pd_person,contact_probe=r13_pd_contact_probe(r13_pd_person),dialogue_verified=False,visual_acceptance=False))
        screenshot "job-musoe-02-production-no-conversation.png"
        pause until eval (renpy.get_screen("notify") is None) timeout 5
        assert screen "r13_hub"
        assert eval (room13["location"]=="workshop" and room13["day"]==2 and room13["period"]==0)
        run Function(r13_pd_check_field,"body-click-denial-stayed-in-field")
    # Wood has a real contextual wait option; inspect then physically decline it, never advance time.
    if eval (r13_world_offset()>0):
        click "‹"
        pause 0.5
    if eval (r13_world_offset()>0):
        click "‹"
        pause 0.5
    assert eval (r13_world_offset()==0)
    $ r13_pd_saved_object_preference=R13_PD_MAP_OBJECTS["workshop"]
    $ R13_PD_MAP_OBJECTS["workshop"]=("wood",)
    assert eval (r13_context_wait("wood") and not r13_tool_available("wood") and not r13_object_actions("wood"))
    run Function(r13_pd_choose_object,True)
    assert eval (r13_pd_object_ready and r13_pd_object=="wood")
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has("observed:workshop:wood")) timeout 10
    assert screen "say"
    run Function(r13_pd_flow_log,"actual-wood-observed",dict(key=r13_pd_object,flag=r13_pd_observed_flag))
    screenshot "job-musoe-03b-wood-observed.png"
    advance until screen "r13_object_context" timeout 40
    pause until eval (renpy.get_screen("r13_object_context").scope.get("ready",False)) timeout 5
    assert eval (renpy.get_screen("r13_object_context").scope.get("key")=="wood")
    screenshot "job-musoe-03c-wood-context.png"
    click "그만 살펴본다"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    assert eval (room13["location"]=="workshop" and room13["day"]==2 and room13["period"]==0)
    run Function(r13_pd_check_field,"returned-from-wood-without-waiting")
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "job-musoe-03d-wood-returned.png"
    $ R13_PD_MAP_OBJECTS["workshop"]=r13_pd_saved_object_preference
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    assert eval (r13_world_offset()==(r13_world_width()-1280 if room13["location"]=="workshop" else 0))
    run Function(r13_pd_check_field,"job-right-camera-end")
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Function(r13_pd_target_render,"resident_musoe","job_inspect_old_tool","target-camera-right-end")
    screenshot "job-musoe-04-right-camera-end.png"
    $ R13_PD_MAP_PEOPLE["workshop"]=r13_pd_saved_preference
    run Hide("r13_qa_pixel_variant")
    run Function(r13_pd_end)

