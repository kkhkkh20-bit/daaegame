# 대화와 질문 화면의 인물 그림은 동시에 남지 않아야 한다.
# 질문 화면으로 돌아올 때 큰 그림을 지우고, 다음 대화에서는 다시 보여 준다.

testcase v2_daram_detail:
    # 신청서를 함께 보는 다람의 표정: 승인 원본 연결 뒤 실제 근접 화면을 캡처한다.
    pause until screen "main_menu" timeout 60
    click "처음부터"
    pause 1.0
    run Function(qa_jump, "gate_investigate", ev=["E01", "E02"], place="gate")
    pause until screen "v2_field" timeout 30
    pause 0.7
    click "초소 서류"
    click pos (600, 600) until eval ("MS14_D01_S03_L0005" in v2_trace) timeout 60
    pause 1.0
    assert eval (v2_fig == "daram" and "v2fig" in renpy.get_showing_tags(layer="master"))
    screenshot "daram_approved_closeup.png"

testcase v2_topic_portrait:
    pause until screen "main_menu" timeout 60
    click "처음부터"
    pause 1.0
    run Function(qa_jump, "gate_investigate", ev=["E01", "E02", "E03"], place="gate")
    pause until screen "v2_field" timeout 30
    pause 0.7
    click "돌목"
    pause until screen "v2_topics" timeout 10
    assert eval ("v2fig" not in renpy.get_showing_tags(layer="master") and v2_fig is None)
    pause 0.7
    click "명단과 신청서"
    pause until screen "say" timeout 10
    assert eval ("v2fig" in renpy.get_showing_tags(layer="master") and v2_fig == "guard")
    click pos (600, 600) until screen "v2_topics" timeout 60
    assert eval (v2_vals.get("purpose_difference_known") is True)
    assert eval ("v2fig" not in renpy.get_showing_tags(layer="master") and v2_fig is None and v2_stage is None)
    assert eval ("v2cut" not in renpy.get_showing_tags(layer="master"))
    screenshot "topic_return_single_portrait.png"
    pause 0.7
    click "명단은 어떻게"
    pause until screen "say" timeout 10
    assert eval ("v2fig" in renpy.get_showing_tags(layer="master") and v2_fig == "guard")
    screenshot "topic_next_dialogue_portrait.png"
    click pos (600, 600) until screen "v2_topics" timeout 60
    assert eval (v2_vals.get("reason_heard") is True)
    assert eval ("v2fig" not in renpy.get_showing_tags(layer="master") and v2_fig is None)


testcase v2_old_topic_portrait:
    # 큰 그림이 남은 지난 판 질문 저장도 불러올 때 한 명만 보여야 한다.
    pause until screen "main_menu" timeout 60
    click "처음부터"
    pause 1.0
    run Function(qa_jump, "gate_investigate", ev=["E01", "E02", "E03"], place="gate")
    pause until screen "v2_field" timeout 30
    pause 0.7
    click "돌목"
    pause until screen "v2_topics" timeout 10
    run Function(qa_old_ui_portrait, "guard")
    assert eval ("v2fig" in renpy.get_showing_tags(layer="master"))
    click "더보기"
    pause until screen "v2_settings" timeout 10
    click "저장 · 불러오기"
    pause until screen "v2_files" timeout 10
    click "1쪽 1번"
    pause 1.0
    click "불러오기로"
    click "1쪽 1번"
    pause until screen "v2_topics" timeout 30
    assert eval ("v2fig" not in renpy.get_showing_tags(layer="master") and v2_fig is None)
    screenshot "old_topic_save_single_portrait.png"

testcase v2_present_portrait:
    pause until screen "main_menu" timeout 60
    click "처음부터"
    pause 1.0
    run Function(qa_jump, "gate_investigate", ev=["E01", "E02", "E03"], place="gate")
    pause until screen "v2_field" timeout 30
    pause 0.7
    click "돌목"
    pause until screen "v2_topics" timeout 10
    pause 0.7
    click "자료 제시"
    pause until screen "v2_present" timeout 10
    click "초대 편지"
    click "보여 준다"
    pause until screen "say" timeout 10
    assert eval ("v2fig" in renpy.get_showing_tags(layer="master") and v2_fig == "guard")
    click pos (600, 600) until screen "v2_topics" timeout 60
    assert eval (v2_vals.get("reacted:guard:E01") is True)
    assert eval ("v2fig" not in renpy.get_showing_tags(layer="master") and v2_fig is None and v2_stage is None)
    screenshot "present_return_single_portrait.png"
    pause 0.7
    click "자료 제시"
    pause until screen "v2_present" timeout 10
    assert eval ("v2fig" not in renpy.get_showing_tags(layer="master"))
    click "초소 처리 명단"
    click "보여 준다"
    pause until screen "say" timeout 10
    assert eval ("v2fig" in renpy.get_showing_tags(layer="master") and v2_fig == "guard")
    screenshot "present_next_dialogue_portrait.png"
    click pos (600, 600) until screen "v2_topics" timeout 60
    assert eval (v2_vals.get("reacted:guard:E02") is True)
    assert eval ("v2fig" not in renpy.get_showing_tags(layer="master") and v2_fig is None)
