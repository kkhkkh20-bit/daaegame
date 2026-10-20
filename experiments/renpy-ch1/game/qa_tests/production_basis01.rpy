# Existing-engine D01 checks; native results are recorded by CI.
# No evidence/world state injection. Positions are the production object rects.
# Notebook selection uses the existing qa_tests/helpers.rpy stub; it does not
# establish production notebook visual quality. Actual native run is pending.
init 999 python:
    def pb01_qa_object_point(key):
        x,y,w,h=ROOM13["objects"]["gate"][key]["rect"]
        return (x+w//2-r13_world_offset(),y+h//2)

# Save/skip proof uses actual room13, with no shadow state or expected-state ledger.
testcase pb01_input_save_skip:
    pause 2.0
    $ _preferences.text_cps=1
    click "처음부터"
    pause until screen "say" timeout 30
    $ pb01_qa_read_id=r13_read_id
    click pos (640,600)
    pause 0.1
    assert eval (r13_read_id==pb01_qa_read_id)
    screenshot "pb01_first_click.png"
    $ _preferences.text_cps=0
    click "더보기"
    pause 0.5
    click "읽은 대사 빠르게"
    pause 0.5
    run Function(r13_toggle_fast_all)
    pause until screen "choice" timeout 40
    pause 0.6
    assert eval ("PB01:E01" not in room13["evidence"] and not r13_fast_all)
    $ renpy.save("qa-pb01-before-letter","qa")
    click "편지를 펼친다"
    advance until "편지를 접는다" timeout 40
    pause 0.6
    assert eval (room13["evidence"].count("PB01:E01")==1)
    run Function(renpy.load,"qa-pb01-before-letter")
    pause 1.0
    assert eval ("PB01:E01" not in room13["evidence"])
    click "편지를 펼친다"
    advance until "편지를 접는다" timeout 40
    pause 0.6
    click "마지막 줄을 본다"
    advance until "편지를 접는다" timeout 30
    pause 0.6
    click "글씨를 살핀다"
    advance until "편지를 접는다" timeout 30
    pause 0.6
    assert eval (r13_has("pb01:K01a") and r13_has("pb01:K01b"))
    click "편지를 접는다"
    advance until "마차에서 내린다" timeout 40
    pause 0.6
    click "마차에서 내린다"
    advance until "가족 방문 신청서를 찾아 달라고 한다" timeout 40
    pause 0.6
    click "가족 방문 신청서를 찾아 달라고 한다"
    advance until "자료를 확인한다" timeout 30
    pause 0.6
    click "자료를 확인한다"
    pause until screen "r13_hub" timeout 10
    pause 0.6
    assert eval (room13["evidence"]==["PB01:E01","PB01:E02"])
    screenshot "pb01_existing_gate_before_inspection.png"
    $ pb01_qa_point=pb01_qa_object_point("gate_documents")
    click pos (pb01_qa_point[0],pb01_qa_point[1])
    advance until screen "r13_hub" timeout 40
    pause 0.6
    assert eval (r13_has("PB01:E03") and not r13_has("PB01:E04"))
    $ pb01_qa_point=pb01_qa_object_point("rules")
    click pos (pb01_qa_point[0],pb01_qa_point[1])
    advance until screen "r13_hub" timeout 30
    pause 0.6
    assert eval (r13_has("PB01:E04"))
    $ renpy.save("qa-pb01-documents","qa")
    run Function(renpy.load,"qa-pb01-documents")
    pause 1.0
    assert eval (room13["evidence"].count("PB01:E03")==1 and room13["day"]==1)
    click "돌목"
    pause until screen "r13_entry_topics" timeout 10
    pause 0.6
    click "자료를 함께 제시한다"
    pause until screen "r13_book" timeout 10
    pause 0.6
    click "QA PB01:E03"
    pause 0.6
    click "QA PB01:E03"
    advance until screen "r13_entry_topics" timeout 30
    pause 0.6
    assert eval (not r13_has("pb01:gate_basis_proven"))
    click "힌트를 생각한다"
    advance until screen "r13_entry_topics" timeout 30
    pause 0.6
    click "자료를 함께 제시한다"
    pause until screen "r13_book" timeout 10
    pause 0.6
    click "QA PB01:E03"
    pause 0.6
    click "QA PB01:E04"
    advance until eval (r13_has("entry_corrected")) timeout 40
    pause 0.5
    assert eval (r13_has("pb01:gate_registered") and not r13_has("pb01:reason_heard"))
    $ renpy.save("qa-pb01-registered","qa")
    run Function(renpy.load,"qa-pb01-registered")
    pause 1.0
    assert eval (r13_has("entry_corrected") and r13_has("pb01:gate_registered") and room13["evidence"].count("PB01:E05")==1)
    assert eval (len(room13["flags"])==len(set(room13["flags"])) and room13["day"]==1)
    screenshot "pb01_registration_after_load.png"
    $ open("qa_result.txt","w").write(json.dumps(room13,ensure_ascii=False,indent=2))

testcase pb01_regular:
    pause 2.0
    $ _preferences.text_cps=0
    click "처음부터"
    advance until "편지를 펼친다" timeout 40
    pause 0.6
    click "편지를 펼친다"
    advance until "편지를 접는다" timeout 40
    pause 0.6
    click "편지를 접는다"
    advance until "마차에서 내린다" timeout 40
    pause 0.6
    click "마차에서 내린다"
    advance until "초대 편지를 보여 준다" timeout 40
    pause 0.6
    click "초대 편지를 보여 준다"
    advance until "자료를 확인한다" timeout 30
    pause 0.6
    click "자료를 확인한다"
    pause until screen "r13_hub" timeout 10
    pause 0.6
    $ pb01_qa_point=pb01_qa_object_point("rules")
    click pos (pb01_qa_point[0],pb01_qa_point[1])
    advance until screen "r13_hub" timeout 30
    pause 0.6
    $ pb01_qa_point=pb01_qa_object_point("gate_documents")
    click pos (pb01_qa_point[0],pb01_qa_point[1])
    advance until screen "r13_hub" timeout 40
    pause 0.6
    click "돌목"
    pause until screen "r13_entry_topics" timeout 10
    pause 0.6
    click "두 종이의 항목을 비교한다"
    advance until screen "r13_entry_topics" timeout 30
    pause 0.6
    assert eval (r13_has("pb01:purpose_difference_known") and not r13_has("entry_corrected"))
    click "왜 일꾼으로 적혔는지 묻는다"
    advance until screen "r13_entry_topics" timeout 30
    pause 0.6
    assert eval (r13_has("pb01:reason_heard") and r13_has("pb01:K05"))
    click "자료를 함께 제시한다"
    pause until screen "r13_book" timeout 10
    pause 0.6
    click "QA PB01:E03"
    pause 0.6
    click "QA PB01:E04"
    advance until eval (r13_has("entry_corrected")) timeout 40
    pause 0.5
    assert eval (r13_has("pb01:gate_registered") and room13["evidence"].count("PB01:E05")==1)
    screenshot "pb01_regular_registered.png"
    $ open("qa_result.txt","w").write(json.dumps(room13,ensure_ascii=False,indent=2))
