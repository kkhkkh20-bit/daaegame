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
            return "(편지는 이 여관에서 왔고, 방에는 아내의 바느질과 닮은 매듭이 있다. 여기 머물렀을 가능성은 있지만, 지금도 있는지는 모른다.)" + ("\n다람이: 엄마가 언제 여기 있었는지 물어보자." if r13_home_with_daram() else "")
        if pair=={"G1","G3"}:
            r13_gate_record_comparison()
            return "(예약은 다돌과 한 사람 더, 두 명이다. 초소 이름 목록에만 한 명으로 적혀 있다. 원본을 보여 주고 확인해 봐야겠다.)"
        if pair in ({"E04","E37"},{"E04","E05"}):
            return "(도면의 연결선과 실제로 움직인 장치가 맞는다. 종이에만 남은 길이 아니었다.)"
        return "(지금 적힌 내용만으로 두 기록이 어떻게 이어지는지는 아직 모르겠다.)"

    def r13_compare_selected(selected):
        renpy.set_screen_variable("feedback",r13_compare_result(selected),screen="r13_record_compare")
        renpy.restart_interaction()

screen r13_record_compare(called=False):
    style_prefix "r13"
    modal True
    zorder 80
    default selected=()
    default feedback=""
    $ materials=[key for key in room13["evidence"] if key in ROOM13["evidence"]]
    add Solid("#eee7d6")
    text "기록 비교" xpos 40 ypos 28 size 32 color "#765426"
    text "함께 살펴볼 기록을 두 개 골라 주세요." xpos 254 ypos 36 size 23 color "#526158"
    for column in range(2):
        frame:
            area (40+column*610,100,590,205) padding (22,18)
            background R13PaperPanel(False)
            vbox:
                spacing 18
                if len(selected)>column:
                    $ key=selected[column]
                    text ROOM13["evidence"][key]["name"] size r13_read_size(27,30) color "#765426"
                    viewport:
                        xsize 546 ysize 125 mousewheel True draggable True scrollbars "vertical"
                        text ROOM13["evidence"][key]["establishes"] xsize 518 size r13_read_size(24,28) color "#342a23" line_spacing 6
                else:
                    text "기록 선택" size 27 color "#69746a"
    viewport:
        area (40,326,1200,174) mousewheel True draggable True scrollbars "vertical"
        vpgrid:
            cols 3 spacing 10
            for key in materials:
                textbutton R13_RECORD_SHORT.get(key,ROOM13["evidence"][key]["name"]):
                    style "r13_paper_tab_button" xsize 382 ysize 66
                    selected key in selected
                    action [SetScreenVariable("selected",r13_compare_pair(selected,key)),SetScreenVariable("feedback","")]
    text feedback xpos 54 ypos 527 xsize 1158 size r13_read_size(24,28) color "#285779" line_spacing 6
    textbutton "기록으로 돌아가기":
        style "r13_action_button" area (40,636,290,58) action (Return() if called else Hide("r13_record_compare"))
    textbutton "비교하기":
        style "r13_action_button" area (978,636,260,58)
        action Function(r13_compare_selected,selected)
        sensitive len(selected)==2
    key "game_menu" action (Return() if called else Hide("r13_record_compare"))
