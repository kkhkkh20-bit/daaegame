# Native tests use the production renderer. Setup jumps are not full continuous play.
testcase ms14_45_continue:
    pause 1.0
    click "처음부터"
    pause 0.6
    run Jump("ms14_qa_old_checkpoint")
    pause 0.8
    assert eval (ms14["node"]=="d4_depart" and ms14["schema"]==2)
    assert eval (ms14["values"]["carried_dry_blankets"]==2 and ms14["values"]["silluk_status"]=="supervised_compulsory_labor")
    click "광장으로 돌아간다"
    click pos (640,600) until eval (ms14["node"]=="d4_portrait_offer") timeout 35
    pause 0.5
    assert eval ("E19" not in ms14["evidence"])
    click "초상을 기대 놓고 물러난다"
    click pos (640,600) until eval (ms14["node"]=="d4_afternoon_visit") timeout 35
    assert eval ("E19" in ms14["evidence"])
    screenshot "ms14_45_witness.png"

label ms14_qa_old_checkpoint:
    $ ms14=ms14_qa_reach("d4_depart","nero",0,1)
    $ ms14.pop("schema")
    $ ms14.pop("presentation")
    $ ms14["node"]="review_end"
    $ ms14["values"].pop("d4_fence_seen")
    jump ms14_review_end

testcase ms14_45_warning:
    pause 1.0
    click "처음부터"
    pause 0.6
    run Jump("ms14_qa_warning_slow")
    pause 0.2
    assert eval (not ms14["presentation"]["music_silent"])
    click pos (640,600)
    pause 0.3
    assert eval (ms14["presentation"]["music_silent"] and len(ms14["presentation"]["cues"])==1)
    assert eval (r13_packet[2].get("ms14_silence_after",False))
    pause 0.2
    assert eval (renpy.music.get_playing(channel="music") is None)
    screenshot "ms14_45_warning.png"
    $ renpy.save("qa-ms14-warning-silent","ms14")
    $ renpy.music.play(config.main_menu_music,channel="music")
    run Function(renpy.load,"qa-ms14-warning-silent")
    pause 0.6
    assert eval (renpy.music.get_playing(channel="music") is None and len(ms14["presentation"]["cues"])==1)
    $ _preferences.text_cps=30

label ms14_qa_warning_slow:
    $ ms14=ms14_qa_reach("d5_warning")
    $ _preferences.text_cps=1
    $ renpy.music.play(config.main_menu_music,channel="music")
    jump ms14_run

testcase ms14_45_privacy:
    pause 1.0
    click "처음부터"
    pause 0.6
    run Jump("ms14_qa_private_public_view")
    pause 0.8
    assert screen "r13_book"
    assert eval ("MS14:E27" not in r13_present_entries(r13_catalog_entries(),None))
    assert eval ("MS14:E28" not in r13_present_entries(r13_catalog_entries(),None))
    assert eval ("E27" in ms14["evidence"] and "E28" in ms14["evidence"])
    screenshot "ms14_45_private_filtered.png"

label ms14_qa_private_public_view:
    $ ms14=ms14_qa_reach("d5_night_visit")
    $ ms14=ms14_rt.enter(ms14,"d5_proof")
    $ ms14_sync()
    $ renpy.display.screen.screens[("r13_book",None)] = MS14_QA_REAL_BOOK
    call screen r13_book(target=None,present=True)
    return

testcase ms14_45_rebuttal:
    pause 1.0
    click "처음부터"
    pause 0.6
    run Jump("ms14_qa_rebuttal_setup")
    pause 0.7
    assert eval (ms14["values"]["bami_status"]!="cleared")
    $ ms14=ms14_rt.select(ms14,"E23")
    click "선택한 자료를 제시한다"
    click pos (640,600) until eval (ms14["node"]=="d5_rebuttal_menu") timeout 30
    pause 0.6
    assert eval (ms14["values"]["bami_status"]!="cleared")
    click "자료를 함께 제시한다"
    pause 0.5
    $ ms14=ms14_rt.select(ms14,"E20")
    $ ms14=ms14_rt.select(ms14,"E22")
    $ ms14=ms14_rt.select(ms14,"E23")
    $ ms14=ms14_rt.select(ms14,"E24")
    click "선택한 자료를 제시한다"
    pause 0.5
    click "현재 대화 건너뛰기"
    pause 0.3
    click "건너뛰기"
    pause 0.5
    assert eval (ms14["values"]["bami_status"]=="cleared" and "E25" in ms14["evidence"] and "E26" in ms14["evidence"])
    screenshot "ms14_45_record_corrected.png"

label ms14_qa_rebuttal_setup:
    call ms14_qa_at("d5_proof")
    return

testcase ms14_45_night:
    pause 1.0
    click "처음부터"
    pause 0.6
    run Jump("ms14_qa_night_setup")
    pause 0.6
    assert eval (ms14["values"]["carried_dry_blankets"]==2)
    assert eval (ms14["values"]["daram_next_morning_guard"]=="badugi_diner_limited")
    click "현재 대화 건너뛰기"
    pause 0.3
    click "건너뛰기"
    pause 0.5
    assert eval (ms14["node"]=="sleep5" and ms14["values"]["cookie.location"]=="daram_bag")
    assert eval (ms14["values"]["carried_dry_blankets"]==2 and ms14["values"]["badugi.location"]=="somi_house")
    screenshot "ms14_45_night.png"

label ms14_qa_night_setup:
    call ms14_qa_at("d5_cookie","nero",0,1)
    return
