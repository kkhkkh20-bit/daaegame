# 버튼 이름을 직접 활성화하지 않고, 현재 그림 속 장부의 중앙을 마우스로 누른다.
init python:
    def qa_gate_ledger_pointer(key):
        x,y,w,h=r13_object_target_rect(key,ROOM13["objects"]["gate"][key])
        return r13_world_to_screen((x+w/2.0,y+h/2.0))

testcase gate_ledger_pointer_handoff:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.0
    assert eval (room13["v111"]["gate"]=="gate_request" and not r13_v111_owned("E02"))
    $ qa_gate_ledger_before=r13_v111_value("elapsed_minutes") or 0
    $ qa_gate_ledger_center=qa_gate_ledger_pointer("ledger")
    assert eval (0<qa_gate_ledger_center[0]<1280 and 200<qa_gate_ledger_center[1]<650)
    click pos (qa_gate_ledger_center[0],qa_gate_ledger_center[1])
    pause until screen "say" timeout 20
    assert eval (r13_packet and "명단을 보여 주십시오" in r13_packet[1] and not r13_v111_owned("E02"))
    screenshot "장부중앙_명단요청.png"
    click pos (900,600) until eval (renpy.get_screen("r13_hub") and room13["v111"]["gate"]=="gate_choice") timeout 50
    assert eval (r13_v111_owned("E02") and not r13_v111_owned("E03") and r13_v111_value("elapsed_minutes")==qa_gate_ledger_before+15)
    pause .8
    $ qa_gate_shelf_center=qa_gate_ledger_pointer("booth")
    click pos (qa_gate_shelf_center[0],qa_gate_shelf_center[1])
    click pos (900,600) until screen "choice" timeout 30
    click "금요일 칸을 꺼낸다"
    click pos (900,600) until eval (renpy.get_screen("r13_hub") and room13["v111"]["gate"]=="gate_investigate") timeout 30
    pause .8
    $ qa_gate_document_center=qa_gate_ledger_pointer("gate_documents")
    click pos (qa_gate_document_center[0],qa_gate_document_center[1])
    click pos (900,600) until eval (renpy.get_screen("r13_hub") and r13_v111_owned("E03")) timeout 40
    pause .8
    $ qa_gate_reread_before=r13_v111_value("elapsed_minutes")
    $ qa_gate_ledger_center=qa_gate_ledger_pointer("ledger")
    click pos (qa_gate_ledger_center[0],qa_gate_ledger_center[1])
    pause until screen "say" timeout 20
    assert eval (r13_packet and "초소 처리 명단" in r13_packet[1])
    click pos (900,600) until screen "r13_hub" timeout 30
    assert eval (r13_v111_owned("E02") and r13_v111_owned("E03") and r13_v111_value("elapsed_minutes")==qa_gate_reread_before)
    screenshot "장부와신청서_각각조사.png"
