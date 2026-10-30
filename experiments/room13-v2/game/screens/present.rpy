# 자료 제시: 고른 자료를 그 사람에게 직접 내민다(대신 내미는 대화 주제는 만들지 않는다).

screen v2_present(p):
    modal True
    zorder 20
    default page = 0
    default sel = (v2_owned_newest() or [None])[0]
    add Solid("#00000066")
    use v2_notebook("자료 제시 · %s에게" % V2_PEOPLE[p]["name"])
    if not v2_ev:
        text "보여 줄 자료가 없다." xpos 140 ypos 160 size v2_type("subtitle") color V2_COLOR["muted"]
    else:
        use v2_ev_list(v2_owned_newest(), sel, lambda e: SetScreenVariable("sel", e), checked=(), page=page)
        use v2_ev_detail(sel)
    hbox:
        xpos 760 ypos 600 spacing 14
        textbutton "돌아가기" style "v2_button" xysize (180, 60) action Return(("back_topics",)) text_size v2_type("body")
        textbutton "보여 준다" style "v2_primary" xysize (200, 60) action Return(("show", sel)) sensitive bool(sel) text_size v2_type("body")
