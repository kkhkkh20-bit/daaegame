# Uses the existing Ren'Py test runner. No scene setup/evidence grants are
# injected: all story progress below comes from the shipped new-game inputs.
default pb01_qa_awards = []

testcase pb01_input_save_skip:
    pause 2.0
    $ _preferences.text_cps = 1
    click "처음부터"
    pause until screen "say" timeout 30
    $ pb01_qa_first_record = r13_basis01_state["record"]
    click pos (640,600)
    pause 0.1
    assert eval (r13_basis01_state["record"] == pb01_qa_first_record)
    screenshot "pb01_01_first_click_completes_line.png"
    $ _preferences.text_cps = 0
    click "더보기"
    pause 0.5
    click "읽은 대사 빠르게"
    pause 0.5
    # Exercise the existing fast-all action as well; it must stop at the
    # mandatory input and cannot acquire the letter on behalf of the player.
    run Function(r13_toggle_fast_all)
    pause until screen "choice" timeout 40
    pause 0.6
    assert eval (r13_basis01_state["evidence"] == [] and not r13_fast_all and not r13_fast_read)
    screenshot "pb01_02_mandatory_letter_input.png"
    $ renpy.save("qa-pb01-before-letter","qa")
    click "편지를 펼친다"
    click pos (640,600) until "마지막 줄을 본다" timeout 40
    pause 0.6
    assert eval (r13_basis01_state["evidence"] == ["E01"] and room13["evidence"].count("PB01:E01") == 1)
    $ renpy.save("qa-pb01-after-letter","qa")
    run Function(renpy.load,"qa-pb01-before-letter")
    pause 1.0
    assert eval (r13_basis01_state["evidence"] == [] and "PB01:E01" not in room13["evidence"])
    click "편지를 펼친다"
    click pos (640,600) until "마지막 줄을 본다" timeout 40
    pause 0.6
    assert eval (room13["evidence"].count("PB01:E01") == 1)
    run Function(renpy.load,"qa-pb01-after-letter")
    pause 1.0
    assert eval (r13_basis01_state["evidence"] == ["E01"] and room13["evidence"].count("PB01:E01") == 1)
    screenshot "pb01_03_letter_after_load.png"
    click "마지막 줄을 본다"
    click pos (640,600) until "편지를 접는다" timeout 30
    pause 0.6
    assert eval (r13_basis01_state["K01a"] and not r13_basis01_state["K01b"])
    click "편지를 접는다"
    click pos (640,600) until "마차에서 내린다" timeout 40
    pause 0.6
    click "마차에서 내린다"
    click pos (640,600) until "가족 방문 신청서를 찾아 달라고 한다" timeout 50
    pause 0.6
    click "가족 방문 신청서를 찾아 달라고 한다"
    click pos (640,600) until "자료를 확인한다" timeout 30
    pause 0.6
    click "자료를 확인한다"
    pause 0.6
    assert eval (r13_basis01_state["evidence"] == ["E01","E02"])
    screenshot "pb01_04_gate_before_document_clicks.png"
    click "신청 원본을 살펴본다"
    click pos (640,600) until "겨울철 입장 규칙을 살펴본다" timeout 40
    pause 0.6
    assert eval ("E03" in r13_basis01_state["evidence"] and "E04" not in r13_basis01_state["evidence"])
    click "겨울철 입장 규칙을 살펴본다"
    click pos (640,600) until "신청 원본을 살펴본다" timeout 30
    pause 0.6
    assert eval (r13_basis01_state["elapsed_minutes"] == 35)
    $ renpy.save("qa-pb01-documents","qa")
    click "신청 원본을 살펴본다"
    click pos (640,600) until "겨울철 입장 규칙을 살펴본다" timeout 40
    pause 0.6
    assert eval (r13_basis01_state["elapsed_minutes"] == 35 and room13["evidence"].count("PB01:E03") == 1)
    run Function(renpy.load,"qa-pb01-documents")
    pause 1.0
    click "자료를 살펴보고 함께 들어갈 이유를 제시한다"
    pause 0.6
    click "자료를 함께 제시한다"
    pause 0.6
    keysym "K_1"
    pause 0.6
    keysym "K_7"
    click pos (640,600) until eval (r13_basis01_state["record"] == "MS14_D01_S03_L0024" and renpy.get_screen("choice") is not None) timeout 30
    pause 0.6
    assert eval (not r13_basis01_state["gate_basis_proven"] and not r13_basis01_state["gate_registered"])
    screenshot "pb01_05_wrong_returns_to_argument.png"
    keysym "K_4"
    click pos (640,600) until eval (r13_basis01_state["record"] == "MS14_D01_S03_L0027" and renpy.get_screen("choice") is not None) timeout 30
    pause 0.6
    assert eval (not r13_basis01_state["gate_basis_proven"] and r13_basis01_state["elapsed_minutes"] == 35)
    keysym "K_3"
    pause 0.6
    keysym "K_2"
    pause 0.6
    keysym "K_3"
    pause 0.6
    keysym "K_4"
    pause 0.6
    screenshot "pb01_06_player_selected_grounds.png"
    keysym "K_7"
    # Rapid repeated taps cannot resubmit a result or duplicate an award.
    click pos (640,600)
    click pos (640,600)
    click pos (640,600) until eval (r13_basis01_state["gate_registered"]) timeout 50
    pause 0.3
    assert eval (r13_basis01_state["gate_basis_proven"] and not r13_basis01_state["reason_heard"])
    assert eval (room13["evidence"].count("PB01:E05") == 1 and r13_basis01_state["evidence"].count("E05") == 1)
    $ renpy.store.pb01_qa_awards = list(r13_basis01_state["applied"])
    $ renpy.save("qa-pb01-registered","qa")
    run Function(renpy.load,"qa-pb01-registered")
    pause 1.0
    assert eval (r13_basis01_state["gate_registered"] and r13_basis01_state["applied"] == renpy.store.pb01_qa_awards)
    screenshot "pb01_07_registration_after_load.png"
    $ open("qa_result.txt","w").write(json.dumps(dict(test="pb01_input_save_skip",state=r13_basis01_state,notebook=room13["evidence"]),ensure_ascii=False,indent=2))

testcase pb01_regular:
    pause 2.0
    $ _preferences.text_cps = 0
    click "처음부터"
    click pos (640,600) until "편지를 펼친다" timeout 40
    pause 0.6
    click "편지를 펼친다"
    click pos (640,600) until "편지를 접는다" timeout 40
    pause 0.6
    click "편지를 접는다"
    click pos (640,600) until "마차에서 내린다" timeout 40
    pause 0.6
    click "마차에서 내린다"
    click pos (640,600) until "초대 편지를 보여 준다" timeout 50
    pause 0.6
    click "초대 편지를 보여 준다"
    click pos (640,600) until "자료를 확인한다" timeout 30
    pause 0.6
    click "자료를 확인한다"
    pause 0.6
    click "겨울철 입장 규칙을 살펴본다"
    click pos (640,600) until "신청 원본을 살펴본다" timeout 30
    pause 0.6
    click "신청 원본을 살펴본다"
    click pos (640,600) until "겨울철 입장 규칙을 살펴본다" timeout 40
    pause 0.6
    click "자료를 살펴보고 함께 들어갈 이유를 제시한다"
    pause 0.6
    click "두 종이의 항목을 비교한다"
    click pos (640,600) until eval (r13_basis01_state["purpose_difference_known"] and renpy.get_screen("choice") is not None) timeout 40
    pause 0.6
    assert eval (r13_basis01_state["purpose_difference_known"] and not r13_basis01_state["gate_registered"])
    screenshot "pb01_regular_purpose_compared.png"
    keysym "K_5"
    click pos (640,600) until eval (r13_basis01_state["reason_heard"] and renpy.get_screen("choice") is not None) timeout 40
    pause 0.6
    assert eval (r13_basis01_state["reason_heard"] and r13_basis01_state["K05"])
    keysym "K_3"
    pause 0.6
    keysym "K_2"
    pause 0.6
    keysym "K_3"
    pause 0.6
    keysym "K_4"
    pause 0.6
    keysym "K_7"
    click pos (640,600) until eval (r13_basis01_state["gate_registered"]) timeout 50
    pause 0.3
    assert eval (r13_basis01_state["gate_basis_proven"] and r13_basis01_state["reason_heard"] and r13_basis01_state["elapsed_minutes"] == 35)
    assert eval (room13["evidence"].count("PB01:E05") == 1)
    screenshot "pb01_regular_registered.png"
    $ open("qa_result.txt","w").write(json.dumps(dict(test="pb01_regular",state=r13_basis01_state,notebook=room13["evidence"]),ensure_ascii=False,indent=2))
