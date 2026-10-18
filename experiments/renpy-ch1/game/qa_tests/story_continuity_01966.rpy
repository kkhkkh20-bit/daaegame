# PREPARED ONLY: controlled native fixtures, not a natural campaign replay.
# Requires the existing CI tests.rpy helpers (r13_qa_roam and QA r13_book override).
# No production replacement, no mocked progression, no local SDK execution.
# Clock/location changes below are explicit fixture inputs, NOT evidence of travel/sleep.
# Final .66 menu wording follows the source-audit 24-character correction.
default r13_qa066_done = False
default r13_qa066_talk_history = []

label r13_qa066_talk(person, day=None, period=None):
    hide screen r13_hub
    $ r13_qa066_done=False
    if day is not None:
        $ room13.update(day=day,period=period)
    $ r13_target=person
    $ r13_qa066_history_before=list(_history_list)
    call r13_talk
    $ r13_qa066_talk_history=[entry.what for entry in _history_list if entry not in r13_qa066_history_before]
    $ r13_qa066_done=True
    jump r13_field

label r13_qa066_dispatch(person, topic):
    hide screen r13_hub
    $ r13_qa066_done=False
    $ r13_target=person
    $ r13_topic=topic
    $ r13_present_origin="topics"
    call r13_talk_dispatch
    $ r13_qa066_done=True
    jump r13_field

label r13_qa066_siluk_offer:
    hide screen r13_hub
    $ r13_qa066_done=False
    # Only this event's fixture suppression is removed; other helper flags stay.
    $ room13["flags"]=[f for f in room13["flags"] if f!="ev_a_done"]
    call r13_ev_a_siluk
    $ r13_qa066_done=True
    jump r13_field

label r13_qa066_siluk_notice(day, period):
    hide screen r13_hub
    $ r13_qa066_done=False
    $ room13.update(day=day,period=period,location="stable")
    call r13_siluk_advance_events
    $ r13_qa066_done=True
    jump r13_field

label r13_qa066_siluk_followup:
    hide screen r13_hub
    $ r13_qa066_done=False
    call r13_siluk_advance_followup
    $ r13_qa066_done=True
    jump r13_field

label r13_qa066_lamp_pickup:
    hide screen r13_hub
    $ r13_qa066_done=False
    $ room13["location"]="square"
    call r13_object_options("lamp")
    $ r13_qa066_done=True
    jump r13_field

# Real first encounter then same-day and next-day conversation routing.
# No greeting/encounter flags are fabricated to bypass the first meeting.
testcase controlled_066_siluk_reunion:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=1,period=0,location="stable",life_poc=True,case_state="pending"),("entry_corrected","lodging"))
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval ("resident_siluk" not in r13_met_people())
    run Call("r13_qa066_talk","resident_siluk")
    click pos (640,560) until screen "r13_resident_approach" timeout 30
    pause until eval (renpy.get_screen("r13_resident_approach").scope.get("ready",False)) timeout 10
    # Actual side-question caption is summarized by R13_QUESTION_SUMMARIES.
    click "수레를 세우면 길을 묻겠다고 한다"
    click pos (640,560) until screen "r13_topics" timeout 40
    pause until eval (renpy.get_screen("r13_topics").scope.get("ready",False)) timeout 10
    screenshot "controlled-066-siluk-first-topics.png"
    click "돌아가기"
    pause until eval (r13_qa066_done) timeout 15
    assert eval ("resident_siluk" in r13_met_people() and r13_first_encounter)
    run Call("r13_qa066_talk","resident_siluk")
    click pos (640,560) until screen "r13_topics" timeout 30
    pause until eval (renpy.get_screen("r13_topics").scope.get("ready",False)) timeout 10
    screenshot "controlled-066-siluk-same-day-topics.png"
    click "돌아가기"
    pause until eval (r13_qa066_done) timeout 15
    assert eval (not r13_first_encounter and room13["day"]==1)
    assert eval (not any("이 마을에 처음 왔습니다" in text for text in r13_qa066_talk_history))
    run Call("r13_qa066_talk","resident_siluk",2,0)
    click pos (640,560) until screen "r13_topics" timeout 40
    pause until eval (renpy.get_screen("r13_topics").scope.get("ready",False)) timeout 10
    screenshot "controlled-066-siluk-next-day-topics.png"
    click "돌아가기"
    pause until eval (r13_qa066_done) timeout 15
    assert eval (not r13_first_encounter and room13["day"]==2 and r13_has(r13_calendar_key("resident_siluk")))
    assert eval (not any("실룩입니다" in text or "이 마을에 처음 왔습니다" in text for text in r13_qa066_talk_history))
    assert eval (any(e["person"]=="resident_siluk" and e["day"]==1 for e in room13["encounters"]) and any(e["person"]=="resident_siluk" and e["day"]==2 for e in room13["encounters"]))

# Payment, actual displayed notices, and requests commit through production labels.
# This proves boundary behavior, not an uninterrupted elapsed-day campaign.
testcase controlled_066_siluk_advance_handoff:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=0,location="stable",life_poc=True,case_state="pending"),("entry_corrected","lodging","ev_a_done"),(),12)
    click pos (640,600) until screen "r13_hub" timeout 40
    run Call("r13_qa066_siluk_offer")
    click pos (640,560) until screen "choice" timeout 30
    pause until eval (renpy.get_screen("choice").scope.get("choice_ready",False)) timeout 10
    screenshot "controlled-066-siluk-payment-choice.png"
    click "선금 다섯 냥을 준다"
    click pos (640,560) until eval (r13_qa066_done) timeout 30
    assert eval (r13_cash_now()==7 and r13_siluk_advance_record()["branch"]=="paid" and r13_siluk_advance_phase()=="pending")
    assert eval (not r13_has("siluk_scammed") and not r13_has("know_siluk_debt") and not r13_siluk_advance_record()["overdue_seen"])
    run Call("r13_qa066_siluk_followup")
    pause until screen "choice" timeout 15
    pause until eval (renpy.get_screen("choice").scope.get("choice_ready",False)) timeout 10
    click "맡긴 짐은 어디까지 확인하셨습니까?"
    click pos (640,560) until eval (r13_qa066_done) timeout 30
    assert eval (r13_siluk_advance_record()["last_request"]=="progress" and r13_siluk_advance_record()["status"]=="pending" and r13_cash_now()==7)
    run Call("r13_qa066_siluk_notice",3,2)
    click pos (640,560) until eval (r13_qa066_done) timeout 30
    assert eval (r13_has("siluk_scammed") and r13_siluk_advance_record()["overdue_seen"] and not r13_siluk_advance_record()["next_day_seen"])
    run Call("r13_qa066_siluk_followup")
    pause until screen "choice" timeout 15
    pause until eval (renpy.get_screen("choice").scope.get("choice_ready",False)) timeout 10
    screenshot "controlled-066-siluk-overdue-choice.png"
    click "선금은 드렸으니 부탁한 짐을 가져와 주세요"
    click pos (640,560) until eval (r13_qa066_done) timeout 30
    assert eval (r13_siluk_advance_record()["last_request"]=="deliver" and r13_siluk_advance_record()["status"]=="confronted" and r13_cash_now()==7)
    run Call("r13_qa066_siluk_notice",4,0)
    click pos (640,560) until eval (r13_qa066_done) timeout 30
    assert eval (r13_siluk_advance_record()["next_day_seen"] and r13_siluk_advance_record()["status"]=="confronted" and r13_siluk_advance_notice() is None)
    assert eval (len([row for row in r13_wallet(room13)["ledger"] if row["text"]=="실룩에게 선금"])==1)
    screenshot "controlled-066-siluk-next-day-unresolved.png"

# M01 ownership is seeded. Presentation, pickup, opening and grants are real.
# QA book is explicitly the helper override, NOT production book UI coverage.
testcase controlled_066_chorong_same_day_envelope:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=1,period=1,location="square",life_poc=True,case_state="pending",evidence=["M01","E01"]),("entry_corrected","lodging"))
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval (not r13_has("E18") and not r13_has("warning_location"))
    run Call("r13_qa066_dispatch","resident_lamplighter","present")
    pause until screen "r13_book" timeout 15
    click "QA M01"
    click pos (640,560) until screen "r13_topics" timeout 40
    pause until eval (renpy.get_screen("r13_topics").scope.get("ready",False)) timeout 10
    click "돌아가기"
    pause until eval (r13_qa066_done) timeout 15
    assert eval (r13_has("mother_letter_promised") and r13_has("warning_location") and not r13_has("E18") and room13["day"]==1)
    run Call("r13_qa066_lamp_pickup")
    pause until screen "r13_object_context" timeout 15
    pause until eval (renpy.get_screen("r13_object_context").scope.get("ready",False)) timeout 10
    click "점검함의 봉투를 봉한 채 챙긴다\n시간 소모 없음"
    pause until screen "r13_confirm" timeout 15
    pause until eval (renpy.get_screen("r13_confirm").scope.get("ready",False)) timeout 10
    click "진행한다"
    click pos (640,560) until eval (r13_qa066_done) timeout 30
    assert eval ("warning_keep" in room13["done"] and r13_has("warning_sealed_held") and not r13_has("E18"))
    run Call("r13_qa066_dispatch","resident_lamplighter","warning_open_with")
    click pos (640,560) until screen "r13_topics" timeout 40
    pause until eval (renpy.get_screen("r13_topics").scope.get("ready",False)) timeout 10
    click "돌아가기"
    pause until eval (r13_qa066_done) timeout 15
    assert eval (r13_has("E18") and r13_has("J18") and "warning_open_with" in room13["read_topics"] and room13["day"]==1 and room13["period"]==1)
    assert eval (r13_granny_warning_source_known() and not r13_has("warning_source_exposed"))
    screenshot "controlled-066-chorong-envelope-completed.png"
    run Call("r13_qa066_dispatch","granny","present")
    pause until screen "r13_book" timeout 15
    click "QA E18"
    click pos (640,560) until screen "choice" timeout 40
    pause until eval (renpy.get_screen("choice").scope.get("choice_ready",False)) timeout 10
    screenshot "controlled-066-granny-real-pickup-reply-choice.png"
    assert eval (not r13_has("warning_source_exposed"))
    click "광장 등 밑 점검함에서 꺼냈다고 말한다"
    click pos (640,560) until screen "r13_topics" timeout 30
    pause until eval (renpy.get_screen("r13_topics").scope.get("ready",False)) timeout 10
    click "돌아가기"
    pause until eval (r13_qa066_done) timeout 15
    assert eval (r13_has("warning_source_exposed") and room13["evidence"].count("E18")==1)

# Possession-only fixture: no fabricated pickup, no implied source knowledge.
testcase controlled_066_granny_explicit_reply:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True,case_state="pending",evidence=["E01","E18"]),("entry_corrected","lodging"))
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval (not r13_granny_warning_source_known() and not r13_has("warning_source_exposed") and not r13_has("J06"))
    run Call("r13_qa066_dispatch","granny","present")
    pause until screen "r13_book" timeout 15
    click "QA E18"
    click pos (640,560) until screen "choice" timeout 40
    pause until eval (renpy.get_screen("choice").scope.get("choice_ready",False)) timeout 10
    screenshot "controlled-066-granny-possession-only-reply-choice.png"
    assert eval (not r13_has("warning_source_exposed") and not r13_has("J06"))
    click "어디서 받았는지 왜 궁금한지 되묻는다"
    click pos (640,560) until screen "r13_topics" timeout 30
    pause until eval (renpy.get_screen("r13_topics").scope.get("ready",False)) timeout 10
    click "돌아가기"
    pause until eval (r13_qa066_done) timeout 15
    assert eval (not r13_has("warning_source_exposed") and not r13_has("J06"))
    run Call("r13_qa066_dispatch","granny","present")
    pause until screen "r13_book" timeout 15
    click "QA E18"
    click pos (640,560) until screen "choice" timeout 40
    pause until eval (renpy.get_screen("choice").scope.get("choice_ready",False)) timeout 10
    click "봉투를 거두고 대화를 마친다"
    pause until eval (r13_qa066_done) timeout 15
    assert eval (not r13_has("warning_source_exposed") and not r13_has("J06") and r13_has("E18"))
    screenshot "controlled-066-granny-withdraw-no-source.png"
