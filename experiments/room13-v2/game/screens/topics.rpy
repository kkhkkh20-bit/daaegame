# 질문 목록: 인물 왼쪽·질문지 오른쪽. 그 사람에게 하는 말만 둔다(조작은 아래 단추로).
# 긴 목록은 명시적 쪽 넘김(숨은 스크롤 없음). 하단 4버튼은 같은 크기.

define V2_TOPICS_PER_PAGE = 5

screen v2_topics(p):
    default page = 0
    $ rows = v2_topics(p)
    $ pages = max(1, (len(rows) + V2_TOPICS_PER_PAGE - 1) // V2_TOPICS_PER_PAGE)
    $ shown = rows[page * V2_TOPICS_PER_PAGE:(page + 1) * V2_TOPICS_PER_PAGE]
    $ wait = v2_input_wait()

    add Transform("assets/dialogue-dot-v2/%s/760/neutral.webp" % p, zoom=1.0) xanchor 0.5 xpos 250 ypos 50
    frame:
        xpos 92 ypos 588 xysize (196, 60)
        background v2_frame("ui-b-question/nameplate_paper.png", 20)
        hbox:
            xalign 0.5 yalign 0.5 spacing 6
            add Transform("assets/ui-b-question/b_icon_acorn.png", zoom=0.45) yalign 0.5
            text V2_PEOPLE[p]["name"] size v2_type("title") yalign 0.5

    fixed:
        xpos 520 ypos 160 xysize (720, 500)
        add Transform("assets/ui-b-question/b_panel_book.png", xysize=(720, 500))
        frame:
            xpos 40 ypos -10 xysize (360, 52)
            background v2_frame("ui-b-question/b_tab_title.png", 20)
            hbox:
                xpos 18 yalign 0.5 spacing 8
                add Transform("assets/ui-b-question/b_icon_acorn.png", zoom=0.42) yalign 0.5
                text "묻고 싶은 이야기" size v2_type("body") color V2_COLOR["inverse"] yalign 0.5
                text "질문 %d개" % len(rows) size v2_type("small") color V2_COLOR["inverse"] yalign 0.5
        vbox:
            xpos 48 ypos 62 xsize 630 spacing 6
            if not rows:
                text "지금 물어볼 말은 없다. 자료를 보여 줄 수는 있다." size v2_type("body") color V2_COLOR["muted"]
            for n, row in enumerate(shown):
                button:
                    xfill True ysize 58
                    background None
                    hover_background Solid("#e9d6b366")
                    action Return(("topic", row["key"]))
                    hbox:
                        yalign 0.5 spacing 8
                        add Transform("assets/ui-b-question/%s" % ("b_icon_acorn_done.png" if row["read"] else "b_icon_acorn.png"), zoom=0.42) yalign 0.5
                        text "%d" % (page * V2_TOPICS_PER_PAGE + n + 1) size v2_type("body") yalign 0.5 color V2_COLOR["muted"]
                        text row["title"] size v2_type("emphasis") yalign 0.5 color (V2_COLOR["muted"] if row["read"] else V2_COLOR["ink"])
                        if row["new"]:
                            text "새" size v2_type("small") yalign 0.5 color V2_COLOR["accent"]
                add Solid("#d8c4a0") ysize 1
        if pages > 1:
            hbox:
                xpos 48 ypos 388 spacing 14
                textbutton "‹ 앞쪽" style "v2_button" action SetScreenVariable("page", page - 1) sensitive page > 0 text_size v2_type("small")
                text "%d / %d" % (page + 1, pages) size v2_type("small") yalign 0.5
                textbutton "뒤쪽 ›" style "v2_button" action SetScreenVariable("page", page + 1) sensitive page + 1 < pages text_size v2_type("small")
        hbox:
            xpos 40 ypos 422 spacing 10
            for label, act in (("자료 제시", Return(("present",))), ("기록", Show("v2_records")),
                               ("더보기", Show("v2_settings")), ("돌아가기", Return(("back",)))):
                textbutton label style "v2_button" xysize (150, 56) action act text_size v2_type("body")

    if wait > 0:
        button:
            xysize (1280, 720) background None action NullAction()
        timer wait action Function(renpy.restart_interaction)
