# 2026-10-24 자가 검수 15건(docs/reviews/self-review-20261024/적용보고.md): 넣거나 고친 줄이 그 경로에서 실제로 나오는지 본다.

testcase v111_sr_d02_note:
    # 2일 교환함: 「도착 쪽지를 직접 넣는다」를 고른 뒤 쪽지에 무엇을 적었는지가 화면에 나온다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_flag,"v111:applied:option:sleep1:0")
    run Function(r13_v111_set,"day",2)
    run Function(r13_edit,day=2,location="forest",period=0)
    run Jump("r13_v111_box_written")
    click pos (900,600) until "이제 우체국 가" timeout 90
    assert eval (qa_nw_seen("13호실도 꼭 써") and qa_nw_seen("수첩 한 장을 찢어 적는다") and qa_nw_seen("여관 13호실.” 쪽지를 함 안쪽") and qa_nw_seen("오후에 다시 오겠습니다"))

testcase v111_sr_d10_hands:
    # 10일 13호 회의: 도토가 「왼손」으로 고쳐 말한 뒤 아빠도 두 손을 따로 짚는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run Jump("r13_v111_wound_answer10")
    click pos (900,600) until screen "r13_crisis_proof" timeout 120
    assert eval (qa_nw_seen("왼손은 제가 잡았어요") and qa_nw_seen("오른손은 아랫조각을 쥔 채 문틈 앞에") and not qa_nw_seen("두 손이 잡힌"))

testcase v111_sr_d11_cane_no_karo:
    # 11일 늦은 구조, 까로가 없는 판: 지팡이에 이름이 없다(12일 「이름 없는 표」와 맞춤).
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",11)
    run Function(r13_v111_set,"alive:karo",False)
    run Function(r13_edit,location="forest",period=2)
    run Jump("r13_v111_late_road11")
    click pos (900,600) until eval (qa_nw_seen("이름은 어디에도 없다")) timeout 90
    assert eval (qa_nw_seen("누군가 오래 짚던 것이다") and not qa_nw_seen("이름이 새겨져") and not qa_nw_seen("판잣집 할아버지 거예요"))

testcase v111_sr_d14_memorial:
    # 14일 결말 이름 부르기: 꼬미 자리에는 도토리 한 알(깡통은 6일 불에 탔다).
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14)
    run Function(r13_v111_set,"piko_alive",False)
    run Function(r13_v111_set,"KKOMI_ALIVE",False)
    run Function(r13_v111_set,"nero_alive",False)
    run Function(r13_v111_set,"alive:neoul",False)
    run Function(r13_v111_set,"crowd_intervention","failed")
    run Function(r13_v111_set,"crowd_blocked_by_dad",True)
    run Jump("r13_v111_ending_dispatch14")
    click pos (900,600) until screen "r13_end_card" timeout 120
    assert eval (qa_nw_seen("학교 창가 자리에는 도토리 한 알이 놓여 있었다") and not qa_nw_seen("도토리 깡통"))
