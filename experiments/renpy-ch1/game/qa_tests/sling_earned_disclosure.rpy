# Optional NATIVE QA fixture, PREPARED ONLY / NOT EXECUTED.
# Copy into game/qa_tests only in the QA build with the existing r13_qa_roam helper.
# This is a controlled fixture, not a natural campaign replay or production hook.
default r13_qa_sling_done = False

label r13_qa_sling_first_opening:
    hide screen r13_hub
    $ r13_qa_sling_done=False
    # r13_qa_roam suppresses automatic week-one offers; reset only this controlled event.
    $ room13["flags"]=[flag for flag in room13["flags"] if flag!="ev_l_done"]
    call r13_w1c_letters
    $ r13_qa_sling_done=True
    jump r13_field

label r13_qa_sling_show_j06:
    hide screen r13_hub
    $ r13_qa_sling_done=False
    $ r13_qa_sling_rows=r13_present("resident_sling","J06",False)
    call r13_lines(r13_qa_sling_rows,"qa:sling:show:j06")
    $ r13_qa_sling_done=True
    jump r13_field

label r13_qa_sling_confront:
    hide screen r13_hub
    $ r13_qa_sling_done=False
    call r13_sling_earned_confront
    $ r13_qa_sling_done=True
    jump r13_field

testcase sling_earned_disclosure:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="post",life_poc=True,evidence=["J06"]),("entry_corrected","lodging"))
    click pos (640,600) until screen "r13_hub" timeout 40
    run Call("r13_qa_sling_first_opening")
    click pos (640,560) until screen "choice" timeout 30
    pause until eval (renpy.get_screen("choice").scope.get("choice_ready",False)) timeout 10
    screenshot "sling-first-meeting-choice.png"
    click "“편지에서 뭘 보려는 겁니까?”"
    click pos (640,560) until screen "choice" timeout 30
    pause until eval (renpy.get_screen("choice").scope.get("choice_ready",False)) timeout 10
    click "“남의 편지는 열지 마세요.”"
    click pos (640,560) until eval (r13_qa_sling_done) timeout 30
    assert eval (r13_has("sling_nonpaid_trust") and not r13_has("H9") and not r13_has("know_granny_reads"))
    # Possession has not shown J06 to Sling.
    assert eval (not r13_sling_confront_ready() and not r13_sling_papers_shown())
    run Call("r13_qa_sling_show_j06")
    click pos (640,560) until eval (r13_qa_sling_done) timeout 30
    assert eval (r13_sling_confront_ready() and not r13_has("H9"))
    run Call("r13_qa_sling_confront")
    pause until screen "choice" timeout 20
    pause until eval (renpy.get_screen("choice").scope.get("choice_ready",False)) timeout 10
    screenshot "sling-earned-confront-choice.png"
    click "지금은 더 묻지 않는다"
    pause until eval (r13_qa_sling_done) timeout 20
    assert eval (not r13_has("H9") and not r13_has("sling_confront_completed"))
    run Call("r13_qa_sling_confront")
    pause until screen "choice" timeout 20
    pause until eval (renpy.get_screen("choice").scope.get("choice_ready",False)) timeout 10
    click "편지 일을 끝까지 듣는다"
    click pos (640,560) until eval (r13_qa_sling_done) timeout 30
    assert eval (r13_has("H9") and r13_has("know_granny_reads") and room13["evidence"].count("H9")==1)
    assert eval (r13_sling_fake_letter_ready())
    pause until screen "r13_hub" timeout 20
    screenshot "sling-completed-confront-field.png"
    $ r13_qa_note("sling: first opening refuses name; possession not presentation; actual J06 plus free protection; cancel inert; completed confrontation H9 once")
