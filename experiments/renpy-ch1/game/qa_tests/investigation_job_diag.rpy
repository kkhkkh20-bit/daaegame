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
    screenshot "job-chorong-01b-selected-visible.png"
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
    screenshot "job-chorong-03-returned.png"
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    assert eval (r13_world_offset()==(r13_world_width()-1280 if room13["location"]=="workshop" else 0))
    run Function(r13_pd_check_field,"job-right-camera-end")
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
    screenshot "job-musoe-01-field.png"
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
    assert eval (r13_pd_person_ready and r13_pd_person=="resident_musoe")
    assert eval (any(a["person"]=="resident_musoe" and a["pose"]=="job_inspect_old_tool" and a.get("activity")=="오래 쓰던 손도구의 머리를 손끝으로 살핀다." for a in r13_stage_people(False)))
    screenshot "job-musoe-01b-selected-visible.png"
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
    screenshot "job-musoe-03-returned.png"
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    assert eval (r13_world_offset()==(r13_world_width()-1280 if room13["location"]=="workshop" else 0))
    run Function(r13_pd_check_field,"job-right-camera-end")
    screenshot "job-musoe-04-right-camera-end.png"
    $ R13_PD_MAP_PEOPLE["workshop"]=r13_pd_saved_preference
    run Hide("r13_qa_pixel_variant")
    run Function(r13_pd_end)

