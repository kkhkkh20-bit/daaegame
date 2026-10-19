testcase character_grid2_field_dialogue_profiles:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Function(r13_g2_prepare_physical_window)
    pause 1.0
    run Function(r13_g2_runtime_probe)
    run Function(r13_c4_begin)
    $ persistent.room13_motion=False
    run Function(r13_pd_begin,"proposed")
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    screenshot "grid2-context-field-00-entry-hint.png"
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    run Show("r13_qa_pixel_variant")
    run Function(r13_pd_check_field,"entered-real-field")
    run Function(r13_c4_field,"entered")
    screenshot "grid2-context-field-01-field.png"
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
    run Function(r13_c4_capture,"dialogue","topic")
    screenshot "grid2-context-field-02-resident-topic-say.png"
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
    run Function(r13_c4_field,"returned")
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
    screenshot "grid2-context-field-03-object.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    pause 0.2
    assert eval (room13["location"]=="inn" and room13["day"]==2 and room13["period"]==0)
    run Function(r13_pd_check_field,"returned-from-object")
    screenshot "grid2-context-field-04-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_pd_end)
    click "기록"
    pause 0.4
    run Function(r13_c4_clear_profiles)
    click "사람"
    pause 0.4
    assert screen "r13_records"
    run Function(r13_c4_capture,"profile","relations")
    screenshot "grid2-context-profiles-relations.png"
    click "닫기"
    pause 0.3
    # Legacy notes screen is explicitly fixture-opened, not a claimed UI route.
    run Function(r13_c4_clear_profiles)
    run Show("r13_resident_notes")
    pause 0.4
    assert screen "r13_resident_notes"
    run Function(r13_c4_require_profile_size,(60,62))
    run Function(r13_c4_capture,"profile","notes-60x62")
    screenshot "grid2-context-profiles-notes.png"
    click "닫기"
    run Function(r13_c4_end)


testcase character_grid2_meeting_replay:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Function(r13_g2_prepare_physical_window)
    pause 1.0
    run Function(r13_g2_runtime_probe)
    run Function(r13_c4_begin)
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",case_state="pending",victim_state="alive",evidence=["E01"],propositions=[]),("entry_corrected","lodging"))
    click pos (640,600) until screen "r13_hub" timeout 40
    pause 1.0
    # Deliberate save in the isolated CI profile, to detect overwrites or new slots.
    $ renpy.save("qa-admin-before")
    $ r13_qa_admin_before=winter_copy.deepcopy(room13)
    $ r13_qa_admin_history=r13_qa_admin_persistent_snapshot()
    $ r13_qa_admin_slots=r13_qa_admin_save_snapshot()
    $ r13_qa_admin_enabled_before=persistent.room13_admin
    $ persistent.room13_admin=True
    run Function(renpy.restart_interaction)
    pause 1.0
    click "관리자"
    pause 0.5
    assert screen "r13_admin"
    click "다음 진행 조건"
    click "회의 바로 테스트 (진행 보존)"
    pause 0.5
    assert screen "r13_admin_meeting_picker"
    screenshot "admin-meeting-01-picker.png"
    click "C2 · 아이가 친 촛대 때문에 죽었다"
    pause 3.0
    assert eval (_in_replay=="r13_admin_meeting_replay" and r13_admin_meeting_test)
    assert eval (room13["location"]=="dining" and room13["day"]==R13_TRIAL_DAY and room13["propositions"]==["C1"])
    assert eval ("E08" in room13["evidence"] and "E35" in room13["evidence"] and "bami_consent" in room13["flags"])
    assert eval (r13_meeting_active and r13_meeting_claim=="C2" and not r13_debate_is_broken("C2","s1"))
    assert eval (not _autosave and not FileSave("qa-admin-before",slot=True).get_sensitive())
    assert screen "r13_admin_meeting_controls"
    run Function(r13_c4_capture,"meeting","entry")
    screenshot "grid2-context-meeting-entry.png"
    advance
    pause 0.2
    run Function(r13_c4_capture,"meeting","next-line-early")
    screenshot "grid2-context-meeting-next-line-early.png"
    pause 0.7
    run Function(r13_c4_capture,"meeting","next-line-settled")
    screenshot "grid2-context-meeting-next-line-settled.png"
    run Function(r13_c4_clear_profiles)
    run Show("r13_c4_choices_fixture")
    pause 0.4
    run Function(r13_c4_require_profile_size,(48,48))
    run Function(r13_c4_capture,"profile","choices-48x48")
    screenshot "grid2-context-profiles-choices.png"
    run Hide("r13_c4_choices_fixture")
    pause 0.2
    # Prove isolation even after canonical debate state changes. This is NOT a played rebuttal.
    $ r13_debate_mark("broken","C2","s1")
    $ r13_submit("C2","E08")
    assert eval (r13_debate_is_broken("C2","s1") and "E08" in room13["arguments"]["C2"])
    click "테스트 종료 · 다시 선택"
    pause 0.5
    assert screen "r13_admin_meeting_picker"
    assert eval (not _in_replay and not r13_admin_meeting_test and room13==r13_qa_admin_before)
    assert eval (r13_qa_admin_persistent_snapshot()==r13_qa_admin_history)
    assert eval (r13_qa_admin_save_snapshot()==r13_qa_admin_slots)
    screenshot "admin-meeting-03-returned-picker.png"
    click "C2 · 아이가 친 촛대 때문에 죽었다"
    pause 3.0
    assert eval (_in_replay=="r13_admin_meeting_replay" and r13_admin_meeting_test)
    assert eval (room13["propositions"]==["C1"] and not room13["arguments"] and not r13_debate_is_broken("C2","s1"))
    assert eval (r13_meeting_active and r13_meeting_claim=="C2")
    screenshot "admin-meeting-04-c2-clean-reentry.png"
    click "테스트 종료 · 다시 선택"
    pause 0.5
    assert eval (not _in_replay and room13==r13_qa_admin_before)
    assert eval (r13_qa_admin_persistent_snapshot()==r13_qa_admin_history and r13_qa_admin_save_snapshot()==r13_qa_admin_slots)
    click "닫기"
    pause 0.3
    assert screen "r13_admin"
    click "닫기"
    pause 0.3
    assert screen "r13_hub"
    assert eval (not renpy.get_screen("r13_admin_meeting_picker") and not renpy.get_screen("r13_admin_meeting_controls"))
    assert eval (room13==r13_qa_admin_before)
    screenshot "admin-meeting-05-original-hub.png"
    $ persistent.room13_admin=r13_qa_admin_enabled_before
    $ r13_qa_note("admin_meeting_replay: actual selector/Replay C2 entry, exit, clean reentry, original room13 and authored persistent histories and save-slot metadata preserved; 5 native screenshots. Rebuttal state mutation was a fixture, not played evidence UI.")

    run Function(r13_c4_end)
