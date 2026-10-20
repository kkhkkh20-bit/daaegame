# Comparisons use only materials acquired in this run; never grant source items.
init 78 python:
    def r13_compare_pair(selected,key):
        if key not in (store.room13 or {}).get("evidence",[]):return tuple(selected)
        if key in selected:return tuple(k for k in selected if k!=key)
        return tuple((list(selected)+[key])[-2:])

    def r13_compare_result(selected):
        owned=set((store.room13 or {}).get("evidence",[]))
        if len(set(selected))!=2 or not set(selected)<=owned:
            return "이번 여정에서 모은 기록 두 개를 골라 주세요."
        pair=set(selected)
        if pair=={"E01","E03"}:
            return "(아내 이름으로 온 편지는 이 여관에서 부쳐졌고, 방에는 아내의 바느질과 닮은 매듭이 있다. 여기 머물렀을 가능성은 있지만, 지금도 있는지는 모른다.)" + ("\n다람이: 엄마가 언제 여기 있었는지 물어보자." if r13_home_with_daram() else "")
        if pair=={"G1","G3"}:
            r13_gate_record_comparison()
            return "(신청 원본은 가족 방문 두 명인데, 초소 명단은 신규 일꾼 본인 한 명으로 옮겨져 있다. 숙소 확인과 겨울철 입장 규칙을 함께 확인해 보여 주자.)"
        if pair in ({"E04","E37"},{"E04","E05"}):
            return "(도면의 연결선과 실제로 움직인 장치가 맞는다. 종이에만 남은 길이 아니었다.)"
        return "(지금 적힌 내용만으로 두 기록이 어떻게 이어지는지는 아직 모르겠다.)"

    def r13_compare_selected(selected,scope=None):
        result=r13_compare_result(selected)
        if scope is not None:scope["feedback"]=result
        else:renpy.set_screen_variable("feedback",result,screen="r13_record_compare")
        renpy.restart_interaction()

screen r13_record_compare(called=False):
    modal True
    zorder 80
    use r13_records(initial_tab="all",close_action=(Return() if called else Hide("r13_record_compare")))

screen r13_compare_content(target=None,present_action=None):
    default selected=()
    default feedback=""
    $ materials=[key for key in room13["evidence"] if key in ROOM13["evidence"]]
    text "기록 비교" xpos 284 ypos 76 size 26 color "#765426"
    text "함께 살펴볼 기록 두 개를 고르세요." xpos 440 ypos 82 size 19 color "#65503b"
    for column in range(2):
        frame:
            area (284+column*464,128,450,206) padding (16,14)
            background R13PaperFrame()
            vbox:
                spacing 10
                if len(selected)>column:
                    $ key=selected[column]
                    hbox:
                        spacing 8
                        add R13AntiqueIcon("evidence",size=24) yalign .5
                        text ROOM13["evidence"][key]["name"] size r13_read_size(21,25) color "#765426" xsize 382
                    viewport:
                        xsize 414 ysize 130 mousewheel True draggable True scrollbars "vertical"
                        text r13_catalog_observed(key)["establishes"] xsize 388 size r13_read_size(20,24) color "#493b30" line_spacing 5
                else:
                    text "기록 선택" size 23 color "#796044"
    viewport:
        area (284,350,916,122) mousewheel True draggable True scrollbars "vertical"
        vpgrid:
            cols 3 spacing 8
            for key in materials:
                textbutton R13_RECORD_SHORT.get(key,ROOM13["evidence"][key]["name"]):
                    style "r13_paper_tab_button" xsize 292 ysize 52 text_size r13_read_size(18,21)
                    selected key in selected
                    action [Function(r13_record_select,_scope,"selected",r13_compare_pair(selected,key)),Function(r13_record_select,_scope,"feedback","")]
    viewport:
        area (284,486,914,96) mousewheel True draggable True scrollbars "vertical"
        text feedback xsize 886 size r13_read_size(20,24) color "#285779" line_spacing 5
    textbutton "비교하기":
        style "r13_compact_button" area (954,596,244,44) text_size 21
        action Function(r13_compare_selected,selected,_scope)
        sensitive len(selected)==2

    if target is not None and present_action is not None:
        textbutton (R13_NAMES.get(target,"상대")+"에게 보여주기"):
            style "r13_compact_button" area (284,596,406,44) text_size r13_read_size(20,24)
            sensitive bool(selected)
            action [Function(r13_prepare_present,target,selected),Hide("r13_records"),present_action]
