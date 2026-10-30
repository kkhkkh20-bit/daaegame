# 증명 화면(1일 입구 통합 화면): 상대 주장을 보이고, 가진 자료를 체크로 여러 장 고른다.
# 일부만 맞으면 맞는 자료를 남겨 두고 상대가 반박한다(엔진). 되묻기·조사 계속은 기회를 쓰지 않는다.
# 대조(compare) 모드는 정확히 두 장을 고르고, 두 편지를 나란히 놓아 눈에 띄는 곳을 짚어 볼 수 있다.

screen v2_proof(pid):
    modal True
    zorder 20
    default focus = (v2_pick[-1] if v2_pick else (v2_owned_newest() or [None])[0])
    default page = 0
    $ proof = V2_PROOFS[pid]
    $ compare = proof["mode"] == "compare"
    $ items = v2_owned_newest()
    add Solid("#00000066")
    use v2_notebook("자료 대조" if not compare else "두 편지를 나란히 본다")

    if v2_pair and compare:
        # 나란히 보기: 두 원문을 먼저 보이고, 짚어 볼 곳을 고른다.
        hbox:
            xpos 140 ypos 120 spacing 24
            for e in proof["observe"]["pair"]:
                frame:
                    xysize (480, 380)
                    background v2_frame("ui-b-options/b_opt_choice.png", 18)
                    padding (20, 16)
                    vbox:
                        spacing 8
                        text V2_EVIDENCE[e]["name"] size v2_type("title")
                        add Transform("assets/" + V2_EVIDENCE[e]["art"], fit="contain", xysize=(440, 150)) xalign 0.5
                        text V2_EVIDENCE[e]["text"] size v2_type("body")
        text "눈에 띄는 부분을 짚어 본다" xpos 140 ypos 520 size v2_type("small") color V2_COLOR["accent"]
        hbox:
            xpos 140 ypos 556 spacing 12
            for spot in proof["observe"]["spots"]:
                textbutton spot["label"] style "v2_button" xysize (140, 56) action Return(("observe", spot["id"])) text_size v2_type("body")
            textbutton "돌아가기" style "v2_button" xysize (150, 56) action SetVariable("v2_pair", False) text_size v2_type("body")
    else:
        # 왼쪽: 쟁점과 상대의 실제 발언
        vbox:
            xpos 140 ypos 120 xsize 230 spacing 10
            text proof["title"] size v2_type("subtitle")
            add Solid("#d8c4a0") ysize 1
            if proof["quote"]["who"] in V2_PEOPLE:
                text "%s의 말" % V2_PEOPLE[proof["quote"]["who"]]["name"] size v2_type("small") color V2_COLOR["accent"]
            text proof["quote"]["t"] size v2_type("body")
            text ("두 장을 골라 견준다." if compare else "고른 근거가 맞으면 「근거 제시」.") size v2_type("small") color V2_COLOR["muted"]
        # 가운데: 가진 자료(얻은 순서 최신부터), 체크로 고른다
        use v2_ev_list(items, None, lambda e: [SetScreenVariable("focus", e), Function(v2_toggle_pick, e)], checked=v2_pick, page=page, xpos=390, ypos=120, width=330, box=True)
        # 오른쪽: 자료 상세
        use v2_ev_detail(focus, xpos=750, ypos=112, width=380)
        if compare and v2_pair_ready(pid):
            textbutton "⇆ 나란히 놓기" style "v2_primary" xpos 820 ypos 500 xysize (240, 56) action SetVariable("v2_pair", True) text_size v2_type("body")
        # 아래: 고른 자료 칩과 단추
        hbox:
            xpos 140 ypos 556 spacing 10
            text "고른 자료 %d" % len(v2_pick) size v2_type("small") color V2_COLOR["muted"] yalign 0.5
            for e in v2_pick:
                textbutton V2_EVIDENCE[e]["name"] + " ×" style "v2_button" action Function(v2_toggle_pick, e) text_size v2_type("small") padding (10, 2)
        hbox:
            xpos 520 ypos 610 spacing 14
            if compare:
                textbutton "생각해 본다" style "v2_button" xysize (210, 60) action Return(("press",)) text_size v2_type("body")
                textbutton "견주어 본다" style "v2_primary" xysize (230, 60) action Return(("submit", list(v2_pick))) sensitive len(v2_pick) == 2 text_size v2_type("body")
            else:
                textbutton "되묻는다" style "v2_button" xysize (190, 60) action Return(("press",)) text_size v2_type("body")
                textbutton "조사 계속" style "v2_button" xysize (190, 60) action Return(("investigate",)) text_size v2_type("body")
                textbutton "근거 제시" style "v2_primary" xysize (190, 60) action Return(("submit", list(v2_pick))) sensitive bool(v2_pick) text_size v2_type("body")
