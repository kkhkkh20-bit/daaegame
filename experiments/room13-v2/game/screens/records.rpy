# 기록(수첩): 자료·사람·메모(「지금 할 일」). 수첩 계열은 모두 같은 수첩 판(b_opt_panel) 안에 다 들어간다.
# 자료 목록은 4개씩 명시적 쪽 넘김. v2_ev_list·v2_ev_detail 은 자료 제시·증명 화면도 함께 쓰는 부품이다.

define V2_EV_PER_PAGE = 4

screen v2_notebook(title):
    # 수첩 판 바탕과 제목(부품).
    add "assets/ui-b-options/b_opt_panel.png" xalign 0.5 yalign 0.5 zoom 0.98
    text title xpos 140 ypos 58 size v2_type("display")

screen v2_ev_list(items, sel, pick, checked=(), page_var="page", page=0, xpos=140, ypos=150, width=320, box=False):
    # 자료 카드 목록(부품). pick 은 카드를 누를 때의 동작을 돌려주는 함수.
    $ pages = max(1, (len(items) + V2_EV_PER_PAGE - 1) // V2_EV_PER_PAGE)
    vbox:
        xpos xpos ypos ypos spacing 10 xsize width
        for e in items[page * V2_EV_PER_PAGE:(page + 1) * V2_EV_PER_PAGE]:
            button:
                style "v2_card" xfill True ysize 80
                selected e == sel or e in checked
                action pick(e)
                alt V2_EVIDENCE[e]["name"]
                hbox:
                    spacing 10 yalign 0.5
                    if box:
                        frame:
                            xysize (34, 34) yalign 0.5
                            background v2_frame("ui-b-options/b_opt_choice.png", 8)
                            if e in checked:
                                text "✓" xalign 0.5 yalign 0.5 size v2_type("body") color V2_COLOR["accent"]
                    add Transform("assets/" + V2_EVIDENCE[e]["art"], fit="contain", xysize=(52, 52)) yalign 0.5
                    # 날짜·장소 꼬리표는 두지 않는다(소유자 2026-10-29 「날짜 장소가 전혀 필요가 없을듯」).
                    text V2_EVIDENCE[e]["name"] size v2_type("body") yalign 0.5
        if pages > 1:
            hbox:
                spacing 14
                textbutton "‹" style "v2_button" xysize (60, 52) action SetScreenVariable(page_var, page - 1) sensitive page > 0 text_size v2_type("title")
                text "%d / %d" % (page + 1, pages) size v2_type("body") yalign 0.5
                textbutton "›" style "v2_button" xysize (60, 52) action SetScreenVariable(page_var, page + 1) sensitive page + 1 < pages text_size v2_type("title")

screen v2_ev_detail(e, xpos=490, ypos=140, width=400, origin=False):
    # 자료 하나의 이름·종류·그림·사실(부품). 추론은 넣지 않는다(본 것·들은 말만).
    # origin: 「출처 펼치기」를 누른 상태. 그림 자리에 원문을 보인다(스크롤 없이 칸 안에 들어오게).
    if e:
        vbox:
            xpos xpos ypos ypos xsize width spacing 10
            hbox:
                spacing 12
                text V2_EVIDENCE[e]["name"] size v2_type("title")
                text V2_EVIDENCE[e]["kind"] size v2_type("small") color V2_COLOR["accent"] yalign 0.5
            if origin:
                text ("들은 말" if V2_EVIDENCE[e]["kind"] == "증언" else "확인한 내용") size v2_type("small") color V2_COLOR["accent"]
                text V2_EVIDENCE[e]["text"] size v2_type("small")
            else:
                frame:
                    xalign 0.5 xysize (220, 170)
                    background v2_frame("ui-b-options/b_opt_choice.png", 18)
                    add Transform("assets/" + V2_EVIDENCE[e]["art"], fit="contain", xysize=(190, 140)) xalign 0.5 yalign 0.5
                for f in V2_EVIDENCE[e]["facts"]:
                    text "· " + f size v2_type("body")

screen v2_ev_pair_read(pair, xpos=750, ypos=112, width=380):
    # 나란히 놓기(읽기용, 지금 판 r13_pw_pair): 두 자료를 같은 폭 두 열로. 맞는지 아닌지는 표시하지 않는다.
    $ col = (width - 16) // 2
    vbox:
        xpos xpos ypos ypos xsize width spacing 8
        text "왼쪽 목록에서 함께 볼 자료를 누른다." size v2_type("small") color V2_COLOR["muted"]
        hbox:
            spacing 16
            for e in pair:
                vbox:
                    xsize col spacing 6
                    if e:
                        text V2_EVIDENCE[e]["name"] size v2_type("body")
                        add Transform("assets/" + V2_EVIDENCE[e]["art"], fit="contain", xysize=(col, 100))
                        for f in V2_EVIDENCE[e]["facts"]:
                            text "· " + f size v2_type("small")

screen v2_records():
    modal True
    zorder 60
    default tab = "ev"
    default page = 0
    default sel = (v2_owned_newest() or [None])[0]
    add Solid("#00000088")
    use v2_notebook("기록")
    hbox:
        xpos 300 ypos 54 spacing 12
        for key, label in (("ev", "자료"), ("people", "사람"), ("memo", "메모")):
            textbutton label style "v2_button" action SetScreenVariable("tab", key) selected tab == key text_size v2_type("body") padding (20, 4)
    imagebutton:
        xpos 1110 ypos 42 idle Transform("assets/ui-b-options/b_opt_close.png", zoom=0.6)
        action Hide("v2_records") alt "닫기"
    if tab == "ev":
        if not v2_ev:
            text "아직 모은 자료가 없다." xpos 140 ypos 160 size v2_type("subtitle") color V2_COLOR["muted"]
        else:
            text "자료 %d개" % len(v2_ev) xpos 140 ypos 118 size v2_type("small") color V2_COLOR["muted"]
            use v2_ev_list(v2_owned_newest(), sel, lambda e: SetScreenVariable("sel", e), checked=(), page=page)
            use v2_ev_detail(sel)
            if sel:
                vbox:
                    xpos 910 ypos 150 xsize 240 spacing 8
                    text "적힌 글" size v2_type("small") color V2_COLOR["accent"]
                    text V2_EVIDENCE[sel]["text"] size v2_type("small")
    elif tab == "people":
        text "만난 사람" xpos 140 ypos 118 size v2_type("small") color V2_COLOR["muted"]
        hbox:
            xpos 140 ypos 160 spacing 16 box_wrap True xsize 1040
            for who in ["daram"] + [w for w in v2_met if w != "daram"]:
                frame:
                    xysize (230, 230)
                    background v2_frame("ui-b-options/b_opt_choice.png", 18)
                    vbox:
                        xalign 0.5 yalign 0.5 spacing 6
                        add Transform(Crop((0, 0, 330, 300), "assets/dialogue-dot-v2/%s/760/neutral.webp" % who), fit="contain", xysize=(130, 120)) xalign 0.5
                        text V2_PEOPLE[who]["name"] size v2_type("title") xalign 0.5
                        text V2_PEOPLE[who]["role"] size v2_type("small") color V2_COLOR["muted"] xalign 0.5
    else:
        vbox:
            xpos 140 ypos 140 xsize 1040 spacing 14
            text "지금 할 일" size v2_type("subtitle") color V2_COLOR["accent"]
            text (v2_goal() or "지금은 따로 적어 둔 일이 없다.") size v2_type("emphasis")
            if v2_scene:
                text "지금 장면" size v2_type("small") color V2_COLOR["muted"]
                text V2_SCENES[v2_scene]["title"] size v2_type("body")
