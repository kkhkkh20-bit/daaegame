# Targeted placement-only native cases. Reuse verified physical click/topic/return helpers.
# Official CI only; no actor/schedule/story flag injection.

testcase investigation_placement_ubak:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_pd_begin,"proposed-placement-ubak")
    $ r13_pd_saved_preference=R13_PD_MAP_PEOPLE["workshop"]
    $ R13_PD_MAP_PEOPLE["workshop"]=("resident_ubak",)
    run Call("r13_qa_roam",dict(day=2,period=0,location="workshop",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    screenshot "placement-ubak-00-entry-hint.png"
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    assert eval (r13_world_offset()==0)
    run Function(r13_pd_target_render,"resident_ubak","living_measure","target-camera-zero")
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "placement-ubak-01-field.png"
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
    assert eval (r13_pd_person_ready and r13_pd_person=="resident_ubak")
    click pos (r13_pd_person_x,r13_pd_person_y)
    pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 5
    if screen "say":
        run Function(r13_pd_log_opening,"actual-first-contact-notice")
        screenshot "placement-ubak-01c-first-notice.png"
    advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
    assert eval (r13_target==r13_pd_person)
    pause 0.4
    if screen "r13_resident_approach":
        run Function(r13_pd_approach_yes)
        screenshot "placement-ubak-01d-approach.png"
        click expression r13_pd_approach_text
        pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_topics") is not None) timeout 5
        if screen "say":
            run Function(r13_pd_log_opening,"actual-first-contact-opening")
            screenshot "placement-ubak-01e-opening.png"
    advance until screen "r13_topics" timeout 40
    pause 0.4
    run Function(r13_pd_choose_topic)
    run Function(r13_pd_checkpoint,"topics-before-click-"+room13["location"])
    click expression r13_pd_topic_title
    advance until eval (r13_pd_topic_say_ready()) timeout 40
    pause 0.4
    run Function(r13_pd_assert_topic_say)
    screenshot "placement-ubak-02-resident-topic-say.png"
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
    screenshot "placement-ubak-03-returned.png"
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    assert eval (r13_world_offset()==(r13_world_width()-1280 if room13["location"]=="workshop" else 0))
    run Function(r13_pd_check_field,"placement-opposite-camera-end")
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Function(r13_pd_target_render,"resident_ubak","living_measure","target-camera-right-end")
    screenshot "placement-ubak-04-opposite-camera-end.png"
    $ R13_PD_MAP_PEOPLE["workshop"]=r13_pd_saved_preference
    run Hide("r13_qa_pixel_variant")
    run Function(r13_pd_end)


testcase investigation_placement_granny:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_pd_begin,"proposed-placement-granny")
    $ r13_pd_saved_preference=R13_PD_MAP_PEOPLE["inn"]
    $ R13_PD_MAP_PEOPLE["inn"]=("granny",)
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    screenshot "placement-granny-00-entry-hint.png"
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "placement-granny-01-field.png"
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
    assert eval (r13_pd_person_ready and r13_pd_person=="granny")
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
    screenshot "placement-granny-02-resident-topic-say.png"
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
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "placement-granny-03-returned.png"
    $ r13_pd_saved_object_preference=R13_PD_MAP_OBJECTS["inn"]
    $ R13_PD_MAP_OBJECTS["inn"]=("register",)
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
    assert eval (r13_pd_object_ready and r13_pd_object=="register")
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    run Function(r13_pd_flow_log,"actual-object-observed",dict(key=r13_pd_object,flag=r13_pd_observed_flag))
    screenshot "placement-granny-04-register.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    assert eval (room13["location"]=="inn" and room13["day"]==2 and room13["period"]==0)
    run Function(r13_pd_check_field,"returned-from-object")
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "placement-granny-05-register-returned.png"
    $ R13_PD_MAP_OBJECTS["inn"]=r13_pd_saved_object_preference
    if eval (r13_world_offset()>0):
        click "‹"
        pause 0.5
    if eval (r13_world_offset()>0):
        click "‹"
        pause 0.5
    assert eval (r13_world_offset()==(r13_world_width()-1280 if room13["location"]=="workshop" else 0))
    run Function(r13_pd_check_field,"placement-opposite-camera-end")
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "placement-granny-06-opposite-camera-end.png"
    $ R13_PD_MAP_PEOPLE["inn"]=r13_pd_saved_preference
    run Hide("r13_qa_pixel_variant")
    run Function(r13_pd_end)

