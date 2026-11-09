# 같은 조사에서 선반까지 이어갈지 저장하는 UI 의도다. 옛 저장은 기존 명단 경로를 따른다.
default r13_gate_continue_to_shelf=False

# 0.20.138: 날짜별 서류 검색을 별도 요일 퀴즈로 묻지 않는다. 명단과 원본을 읽고
# 플레이어가 차이를 입증하는 데 집중한다. 원본 획득은 호출한 기존 조사 라벨에서만 한다.
# 예전 선택창 안에서 저장한 판을 위해 menu 라벨·선택 값·오답 복귀는 아래에 보존한다.
init 360 python:
    def r13_gate_shelf_days():
        today=(store.room13 or {}).get("day",1)
        names=[r13_weekday(today+d)+"요일" for d in (-1,0,1)]
        return names

label r13_v111_gate_shelf_pick:
    $ r13_gate_shelf_names=r13_gate_shelf_days()
    call r13_lines([r13_nw_added_line(dict(kind="narration",text="선반에서 오늘 날짜의 신청서 묶음을 꺼낸다. 다돌이라고 적힌 종이가 있다."))],'nw:gate_shelf_lookup')
    return

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
