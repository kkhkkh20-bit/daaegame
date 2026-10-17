# Explicit presentation fixture, not a natural campaign replay.
default r13_qa_direction_done = False
default r13_qa_direction_result = None

label r13_qa_direction_present(claim,sid,key):
    hide screen r13_hub
    $ r13_meeting_claim=claim
    $ r13_meeting_active=True
    $ r13_meeting_direction_seen=[]
    $ r13_qa_direction_done=False
    $ r13_qa_direction_sound_begin=len(source_effect_log)
    call r13_debate_present_record(claim,sid,key)
    $ r13_qa_direction_result=_return
    $ r13_meeting_active=False
    $ r13_meeting_direct_end()
    $ r13_qa_direction_done=True
    return

testcase meeting_direction:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=10,period=0,location="dining",case_state="occurred",victim_state="dead",evidence=["E09","E06"],propositions=["C1"]),("entry_corrected","lodging"))
    click pos (640,600) until screen "r13_hub" timeout 40
    run Call("r13_qa_direction_present","C2","s3","E09")
    click pos (640,600) until screen "choice" timeout 40
    assert eval (r13_meeting_direction["beat"]=="recover" and not r13_debate_is_broken("C2","s3"))
    assert eval ("right" not in source_effect_log[r13_qa_direction_sound_begin:])
    screenshot "direction-recovered.png"
    click "겁 많은 아이는 그 길로 못 간다"
    click pos (640,600) until eval (r13_qa_direction_done) timeout 40
    assert eval ("right" not in source_effect_log[r13_qa_direction_sound_begin:])
    assert eval (not r13_qa_direction_result and not r13_debate_is_broken("C2","s3") and "C2" not in room13["propositions"])
    assert eval (not r13_meeting_direction and not renpy.get_screen("r13_meeting_evidence_hold") and not renpy.music.get_pause(channel="music"))
    $ r13_qa_direction_done=False
    run Call("r13_qa_direction_present","C2","s3","E09")
    click pos (640,600) until screen "choice" timeout 40
    click "통로는 주방 레버로만 열린다"
    click pos (640,600) until eval (r13_qa_direction_done) timeout 40
    assert eval ("right" in source_effect_log[r13_qa_direction_sound_begin:])
    assert eval (r13_qa_direction_result and r13_debate_is_broken("C2","s3") and "C2" not in room13["propositions"])
    assert eval (not r13_meeting_direction and not renpy.music.get_pause(channel="music"))
    $ r13_qa_note("direction: opponent recovery, wrong counter keeps statement, success only after correct counter, cleanup ok")
