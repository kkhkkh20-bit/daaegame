# Real-engine UI regression. Run only in disposable CI HOME/XDG/save directories.
# This fixture is not campaign progression; Replay is entered by its actual UI action.
default r13_qa_admin_before = None
default r13_qa_admin_history = None
default r13_qa_admin_slots = None
default r13_qa_admin_enabled_before = False

init 190 python:
    def r13_qa_admin_persistent_snapshot():
        names=("room13_read","room13_knowledge","room13_knowledge_revision",
            "room13_previous_knowledge","room13_endings","room13_ending_notes",
            "room13_opening_seen","room13_cinematics_seen")
        return {name:winter_copy.deepcopy(getattr(persistent,name,None)) for name in names}

    def r13_qa_admin_save_snapshot():
        return {slot:winter_copy.deepcopy(renpy.slot_json(slot))
            for slot in renpy.list_slots()}

testcase admin_meeting_replay:
    pause 2.0
    click "처음부터"
    pause 3.0
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
    screenshot "admin-meeting-02-c2-live.png"
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
