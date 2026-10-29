# 2026-10-24 지시서 01 (docs/codex/지시서_01_결함_기회수_맞물림.md): 회의는 언제나 깰 수 있어야 한다.
# 칼 쟁점 무동의 판 승리, 13호 3번 재제출 승리, 「전부 내기」 뒤 근거 안 남음, 회의별 기회 수, 틀렸을 때 아빠 속말.
# 보고서: docs/reviews/codex-01/적용보고.md
init python:
    def qa_rules_kept(key,correct,given):
        return r13_v111_proof_kept(key,correct,["V111:"+k for k in given])
    def qa_rules_ok(key,correct,given):
        return r13_v111_proof_accepts(key,correct,["V111:"+k for k in given])

testcase v111_rules_tries_table:
    # 회의별 기회 = 쟁점 수 + 2 (최소 3), 11일 가설만 13 (소유자 결정 5). 증명 화면 숫자도 같은 표를 쓴다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval ([r13_nw_tries_max(m) for m in ("gate","gate_post","fire","records","blanket","piko","soup","altar","lamp","room13","hypothesis")]==[3,3,4,4,4,4,5,6,7,7,13])
    assert eval (r13_v111_proof_chances("구리선과 수선 출처를 대조한다")=="회의 기회 7 / 7")
    assert eval (r13_v111_proof_chances("함께 들어갈 근거를 고른다")=="회의 기회 3 / 3")
    run Function(r13_v111_set,"tries:gate",2)
    assert eval (r13_v111_proof_chances("함께 들어갈 근거를 고른다")=="회의 기회 1 / 3 · 이번이 마지막")
    # 13호 3번: 두 정답 세트를 함께 내도 받는다. 남은 근거만 다시 내도 받는다.
    assert eval qa_rules_ok("구리선과 수선 출처를 대조한다",["E08_WOUND_WIRE","E09_PIN_OWNER"],["E08_WOUND_WIRE","E09_PIN_OWNER","E08_CONTACT_ASSEMBLY"])
    assert eval not qa_rules_ok("구리선과 수선 출처를 대조한다",["E08_WOUND_WIRE","E09_PIN_OWNER"],["E08_WOUND_WIRE","E08_CONTACT_ASSEMBLY"])
    assert eval not qa_rules_ok("구리선과 수선 출처를 대조한다",["E08_WOUND_WIRE","E09_PIN_OWNER"],["E08_WOUND_WIRE","E09_PIN_OWNER","E01"])
    # 전부 내기: 정답이 받아 줄 수(덧붙임 제외)보다 많이 낸 오답은 아무것도 남기지 않는다. 그보다 적으면 맞는 것만 남는다.
    assert eval (qa_rules_kept("구리선과 수선 출처를 대조한다",["E08_WOUND_WIRE","E09_PIN_OWNER"],["E08_WOUND_WIRE","E09_PIN_OWNER","E08_CONTACT_ASSEMBLY","E01"])==[])
    assert eval (qa_rules_kept("구리선과 수선 출처를 대조한다",["E08_WOUND_WIRE","E09_PIN_OWNER"],["E08_WOUND_WIRE","E01"])==["V111:E08_WOUND_WIRE"])
    # 덧붙임은 세지 않는다: 초소 정답 셋 + 덧붙임 하나 + 오답 하나는 넷으로 세어 맞는 것만 남기고, 정답 넷 + 오답 둘은 여섯이라 비운다.
    assert eval (qa_rules_kept("밤이 혐의의 근거를 확인한다",["E20","E22","E23","E24"],["E20","E22","E23","E21","E01"])==["V111:E20","V111:E22","V111:E23"])
    assert eval (qa_rules_kept("밤이 혐의의 근거를 확인한다",["E20","E22","E23","E24"],["E20","E22","E23","E24","E01","E02"])==[])

testcase v111_rules_knife_no_consent:
    # 3일 칼 쟁점: 칼 대조에 동의하지 않은 판에도 정답 보기가 있어 이길 수 있다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day3_meeting_ready)
    run Function(r13_v111_set,"silluk_knife_comparison_consent",False)
    run Jump("r13_v111_trial_knife")
    pause 1.5
    click "깨진 칼끝을 안쪽 조각에 맞대 본다"
    click pos (900,600) until screen "r13_crisis_proof" timeout 90
    assert eval (v111_claim=="v111:바깥 걸쇠 주장과 발견 위치를 대조한다" and not r13_v111_value("tries:lamp") and r13_v111_value("meeting:lamp") is None)
    assert eval qa_nw_seen("이 칼끝입니다")

testcase v111_rules_copper_resubmit:
    # 13호 3번: 틀린 뒤 남겨 둔 근거를 그대로 다시 내면 이긴다. 틀린 뒤 증명 화면 앞에 아빠 속말이 나온다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run Function(r13_edit,location="school")
    run Function(r13_grant,["V111:E08_WOUND_WIRE","V111:E09_PIN_OWNER","V111:E01"],"qa")
    run Jump("r13_v111_owner_proof10")
    pause 1.5
    assert screen "r13_crisis_proof"
    click "자료 고르기"
    pause 0.5
    click "QA V111:E08_WOUND_WIRE"
    pause 0.8
    click "QA V111:E09_PIN_OWNER"
    pause 0.8
    click "QA V111:E01"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until screen "r13_crisis_proof" timeout 90
    assert eval (r13_v111_value("tries:room13")==1 and sorted(room13["arguments"]["v111:구리선과 수선 출처를 대조한다"])==["V111:E08_WOUND_WIRE","V111:E09_PIN_OWNER"])
    assert eval qa_nw_seen(R13_NW_WRONG_THOUGHTS["구리선과 수선 출처를 대조한다"][1])
    click "선택한 근거 제출"
    click pos (900,600) until screen "r13_crisis_proof" timeout 90
    assert eval (r13_v111_value("proof_given:구리선과 수선 출처를 대조한다")==["V111:E08_WOUND_WIRE","V111:E09_PIN_OWNER"] and r13_v111_value("tries:room13")==1)

testcase v111_rules_dump_all:
    # 가진 자료를 다 내면 오답이 되고, 탁자에 아무것도 남지 않는다(다음 제출로 풀리지 않는다).
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run Function(r13_edit,location="school")
    run Function(r13_grant,["V111:E08_WOUND_WIRE","V111:E09_PIN_OWNER","V111:E08_CONTACT_ASSEMBLY","V111:E01"],"qa")
    run Jump("r13_v111_owner_proof10")
    pause 1.5
    click "자료 고르기"
    pause 0.5
    click "QA V111:E08_WOUND_WIRE"
    pause 0.8
    click "QA V111:E09_PIN_OWNER"
    pause 0.8
    click "QA V111:E08_CONTACT_ASSEMBLY"
    pause 0.8
    click "QA V111:E01"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until screen "r13_crisis_proof" timeout 90
    assert eval (r13_v111_value("tries:room13")==1 and room13["arguments"]["v111:구리선과 수선 출처를 대조한다"]==[] and not r13_v111_value("proof_given:구리선과 수선 출처를 대조한다"))

testcase v111_rules_final_line:
    # 기회를 다 쓴 오답 뒤 한 번: 「다 있었다. 그런데 이어 붙이지 못했다.」 (입구 회의는 기회 3)
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_commit,"MS14_D01_S02_L0019")
    run Function(r13_v111_set,"tries:gate",r13_nw_tries_max("gate")-1)
    run Jump("r13_v111_gate_wrong")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (r13_v111_value("meeting:gate")=="lose" and r13_v111_value("gate_daram_unlisted") is True)
    assert eval (qa_nw_seen("다 있었다. 그런데 이어 붙이지 못했다.") and r13_nw_wrong_pending is None and r13_v111_value("wrong_final:gate") is True)
