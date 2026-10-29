# 2026-10-29 소유자 승인 설계안 ②(1일 돌목 사건 다시 설계): 「신청서는 저 선반에 날짜별로 꽂혀 있소」 뒤에
# 돌목이 「오늘 날짜는 맨 위 칸이오」라고 칸을 알려 주어 「직접 찾아 보여 달라」가 행동이 되지 못했다.
# 선반 칸은 요일로 나뉘어 있고, 아빠는 명단의 「같은 도착일」(우리가 내린 날 = 오늘)과 날짜판을 보고 칸을 고른다.
# 틀린 칸은 벌칙 없이 그 칸이 무엇인지만 말한다(기회를 쓰지 않는다). 새 자료·사건은 없다 — 맞는 칸에서 원래대로 신청 원본(E03)을 찾는다.
# days123.rpy 는 줄 수 고정이라 r13_v111_gate_original 의 한 줄만 이 label 호출로 바꿨다.
init 360 python:
    def r13_gate_shelf_days():
        today=(store.room13 or {}).get("day",1)
        names=[r13_weekday(today+d)+"요일" for d in (-1,0,1)]
        return names

label r13_v111_gate_shelf_pick:
    $ r13_gate_shelf_names=r13_gate_shelf_days()
    call r13_lines([r13_nw_added_line(dict(kind="thought",text="선반 칸마다 요일 쪽지가 붙어 있다. 명단엔 「같은 도착일」이라고만 적혀 있다."))],'nw:gate_shelf_intro')
label r13_v111_gate_shelf_menu:
    $ r13_gate_shelf_pick=renpy.display_menu([(r13_gate_shelf_names[0]+" 칸을 꺼낸다","before"),(r13_gate_shelf_names[1]+" 칸을 꺼낸다","today"),(r13_gate_shelf_names[2]+" 칸을 꺼낸다","after")])
    if r13_gate_shelf_pick=="today":
        call r13_lines([r13_nw_added_line(dict(kind="thought",text=r13_gate_shelf_names[1]+" 칸. 오늘 내린 사람들 신청서다.\n맨 앞에…… 내 이름이 있다."))],'nw:gate_shelf_today')
        return
    if r13_gate_shelf_pick=="before":
        call r13_lines([r13_nw_added_line(dict(kind="thought",text=r13_gate_shelf_names[0]+" 칸. 어제 들어온 사람들 이름뿐이다.\n우리는 오늘 내렸다."))],'nw:gate_shelf_before')
    else:
        call r13_lines([r13_nw_added_line(dict(kind="thought",text=r13_gate_shelf_names[2]+" 칸은 비어 있다. 아직 오지 않은 날이다."))],'nw:gate_shelf_after')
    jump r13_v111_gate_shelf_menu
