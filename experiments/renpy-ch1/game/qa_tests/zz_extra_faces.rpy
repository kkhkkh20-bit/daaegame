label qa_extra_faces_lines:
    call r13_lines([r13_nw_added_line(dict(speaker="주민",text="문 닫기 전에 들어가요. 바람 들어와요.",expression="anxious",kind="dialogue")),r13_nw_added_line(dict(speaker="순찰대원",text="명단에 없는 사람은 여기서 기다리시오.",expression="angry",kind="dialogue")),r13_nw_added_line(dict(speaker="다람",text="아빠, 저 사람 표정 봤어? 진짜 화났어.",expression="anxious",kind="dialogue"))],"qa:extra")
    return

testcase extra_faces:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Call("qa_extra_faces_lines")
    pause 1.2
    screenshot "extra-01.png"
    click pos (900,600)
    pause 1.2
    screenshot "extra-02.png"
    click pos (900,600)
    pause 1.2
    screenshot "extra-03.png"
