# 현장 도트 통일 캡처 초안(2026-10-27). game/qa_tests/ 에 옮겨 dev/run_renpy_tests.sh 로 돌린다.
# 1일 입구는 처음부터 실제 진행, 3일 광장·10일 우체국은 design_restore.rpy 의 fixture 와 같은 방식으로 상태를 만든다.
init 999 python:
    def qa_field_dot_check():
        # 한 장면의 모든 인물이 표에 있고(예전 경로로 떨어진 인물 없음), 화면 도트 한 칸이 같은지 확인한다.
        zoom=r13_field_zoom()
        rows=[(a["person"],a["pose"],a.get("dot",{}).get("scale")) for a in r13_stage_people()]
        missing=[r for r in rows if r[2] is None]
        if missing:raise AssertionError("도트 표에 없는 인물: %r"%missing)
        px={round(r[2]*zoom,3) for r in rows}
        if len(px)!=1:raise AssertionError("화면 도트 px 가 제각각: %r"%rows)
        return rows

label r13_qa_field_dot_square3:
    call r13_scene("winter_square","광장","calm")
    call screen r13_hub
    return

label r13_qa_field_dot_post10:
    call r13_scene("winter_post","우체국 입구","calm")
    call screen r13_hub
    return

testcase field_dot_gate_day1:
    pause 1.0
    $ _preferences.text_cps=0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.0
    assert eval (qa_field_dot_check())
    screenshot "field-dot-gate-day1.png"

testcase field_dot_square_day3:
    pause 1.0
    $ _preferences.text_cps=0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day3_meeting_ready)
    run Function(r13_edit,location="square",period=0)
    run Jump("r13_qa_field_dot_square3")
    pause until screen "r13_hub" timeout 60
    pause 1.0
    assert eval (qa_field_dot_check())
    screenshot "field-dot-square-day3.png"

testcase field_dot_post_day10:
    pause 1.0
    $ _preferences.text_cps=0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(lambda: qa_nw_day(10,"murder"))
    run Function(r13_edit,location="post",period=0)
    run Jump("r13_qa_field_dot_post10")
    pause until screen "r13_hub" timeout 60
    pause 1.0
    assert eval (qa_field_dot_check())
    screenshot "field-dot-post-day10.png"
