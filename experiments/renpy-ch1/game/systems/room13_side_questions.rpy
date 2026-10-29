# B notebook interview: shared paper components, original question actions and gates.
init 80 python:
    R13_SIDE_QUESTION_TOP=150

    def r13_side_question_pages(entries):
        """Fit complete measured rows; overflow uses visible pages, never scrolling."""
        rows=[]
        for title,action,read in entries:
            label=r13_question_caption(title,False,mark_unread=False)
            # 2026-10-27 타이포 시안: 질문 항목은 emphasis. 줄 수 측정과 화면 글자 크기가 같은 식이어야 한다.
            text=Text(label,font=R13_UI_BOLD_FONT,size=(r13_type("emphasis")),xsize=506,line_spacing=2)
            height=int(renpy.render(text,506,720,0,0).get_size()[1])
            rows.append(((title,action,read),max(88 if r13_touch_ui() else 84,height+20)))
        def pack(cap):
            pages=[];page=[];used=0
            for entry,height in rows:
                if page and (used+8+height>cap or len(page)>=8):
                    pages.append(page);page=[];used=0
                page.append((entry,height));used+=height+(8 if len(page)>1 else 0)
            return pages+([page] if page else []) or [[]]
        cap=r13_notebook_topic_y()-(R13_SIDE_QUESTION_TOP+78)-12
        pages=pack(cap)
        return pack(cap-(96 if r13_touch_ui() else 60)) if len(pages)>1 else pages

    # 2026-10-29 눈가림 플레이: 3일 톡의 첫 질문(이야기를 잇는 질문)에는 「새」가 없고 뒤에 열린 후속 질문에만 있었다.
    # 「새」는 후속 질문(room13_v111_reactions.rpy)만 붙였기 때문이다. 플레이어에게 「새」는 아직 안 물은 말이므로,
    # 목록에 그리는 자리에서만 안 읽은 줄 모두에 같은 표시를 붙인다. 제목 자체(r13_v111_questions)는 바꾸지 않는다 —
    # 다른 코드와 화면 시험이 제목을 그대로 비교한다.
    R13_NEW_MARK="{color=#e0707a}새{/color}  "
    def r13_mark_new_questions(rows):
        out=[]
        for row in rows:
            title,action,read=row
            if not read and not title.startswith(R13_NEW_MARK):title=R13_NEW_MARK+title
            out.append((title,action,read))
        return out

    def r13_notebook_topic_y():
        return 550 if r13_touch_ui() else 574

    def r13_notebook_lineart(title):
        # Decorative scenery only: never encode evidence, importance, or truth.
        kind="market" if "장터" in title else "winter" if any(w in title for w in ("겨울","눈","날씨")) else "village" if "마을" in title else "book_corner"
        return r13_asset_path("file:"+("assets/ui-b-question/b_lineart_"+kind+".png"))

    def r13_notebook_button_surface(primary=False,hovered=False):
        return r13_sticker_button(primary=primary,focused=hovered)

    def r13_original_card_surface(path,width):
        # Uniform scale of the actual artwork; centre within the larger hit area.
        return Fixed(Transform(Crop((16,16,640,84),path),zoom=width/640.0,align=(.5,.5)))

    def r13_notebook_question_surface(read=False,focused=False):
        # 2026-10-26 소유자: 「클릭하는 임팩트가 없고 버튼인지 헷갈려」. 올리면 따뜻한 바탕과 왼쪽 빨간 줄이 생긴다.
        if not focused:return Solid("#00000000")
        return Fixed(Solid("#f3dcb0d9"),Transform(Solid("#b83b32"),xsize=6))

    def r13_notebook_button_icon(icon,color="#503525"):
        boxes={"icon_document":(14,8,36,48),"icon_book_open":(8,18,48,27),"icon_arrow_left_bold":(8,18,48,27),"b_icon_more":(16,20,32,24)}
        return Transform(Crop(boxes[icon],r13_asset_path("file:"+("assets/ui-b-question/"+icon+".png"))),xysize=(24,24),fit="contain")

screen r13_notebook_topic_action(x,w,caption,command,ready=True,primary=False,icon=None,control_id=None):
    fixed:
        area (x,r13_notebook_topic_y(),w,88 if r13_touch_ui() else 64)
        $ state_icon=r13_notebook_button_icon(icon) if icon else None
        # 2026-10-27 소유자: 네 버튼 크기 통일. 주 버튼도 같은 바탕(standard)을 쓰고 글자색으로만 구분한다(primary 바탕은 크기가 달랐다).
        use r13_state_button(caption,command,w,88 if r13_touch_ui() else 64,family="question_flat_standard",enabled=ready,icon=state_icon,text_size=(r13_type("body")),control_id=control_id or ("r13_notebook_"+caption))

screen r13_notebook_topic_tools(ready,person,present_action):
    if present_action is not None:
        use r13_notebook_topic_action(572,146,"자료 제시",present_action,ready,True,None)
    use r13_notebook_topic_action(726,146,"기록",Show("r13_records",target=person,present_action=present_action),ready,icon=None)
    use r13_notebook_topic_action(880,146,"더보기",Show("r13_more_tools"),ready,icon=None)

screen r13_side_question_list(person,pose,entries,ready,return_action=None,caption=""):
    default page=0
    $ pages=r13_side_question_pages(entries)
    $ page=min(page,len(pages)-1)
    $ visible=pages[page]
    add Solid("#29232625")
    add r13_close_art(person,pose,840):
        xpos r13_close_x(person,pose,840)-340 xanchor .5 ypos r13_question_close_y(person,840,110,pose)   # 2026-10-27 외부 리뷰 R07: 발이 화면 안에 들어오는 발 선(room13_fullbody_dialogue.rpy)
    add r13_asset("file:assets/ui-b-question/b_panel_book.png") xpos 488 ypos 144
    add Transform(Frame(Crop((16,12,288,40),r13_asset_path("file:assets/ui-b-question/b_tab_title.png")),32,12),xysize=(420,52)) xpos 560 ypos 166
    add Transform(Crop((20,16,23,32),r13_asset_path("file:assets/ui-b-question/b_icon_acorn.png")),xysize=(29,40)) xpos 578 ypos 174
    # 2026-10-27 타이포 시안: 제목과 인물 이름은 같은 subtitle 단계(2026-10-17 같은 크기 정렬 유지).
    text (caption or "묻고 싶은 이야기") xpos 618 ypos 176 xsize 340 size (r13_type("subtitle")) color (r13_type_color("inverse")) font R13_UI_BOLD_FONT
    # 2026-10-27 소유자: 「질문 N개」가 오른쪽 위 테이프·모서리 그림과 겹쳤다. 모서리 그림은 빼고 개수는 제목 띠 오른쪽 끝에 둔다.
    text ("질문 %d개"%len(entries) if len(pages)==1 else "%d / %d쪽"%(page+1,len(pages))) xpos 966 xanchor 1.0 ypos 184 size (r13_type("small")) color (r13_type_color("inverse")) font R13_UI_BOLD_FONT
    # Name stays next to the speaker, clear of the notebook and their face.
    add Transform(r13_asset_path("file:assets/ui-b-question/nameplate_paper.png"),xysize=(246,94)) xpos 78 ypos 566
    add Transform(Crop((20,16,23,32),r13_asset_path("file:assets/ui-b-question/b_icon_acorn.png")),xysize=(25,34)) xpos 112 ypos 595
    # 2026-10-28 캡처 검수: 「부엉이 할아버지」(부제목 크기 163px)가 글자 칸 160px 를 넘어 둘째 줄이 판 밖으로 잘렸다. 여덟 자 이상은 한 단 내린다.
    text R13_NAMES[person] xpos 150 ypos 594 size (r13_type("subtitle") if len(R13_NAMES[person])<8 else r13_type("body")) color (r13_type_color("ink")) font R13_UI_BOLD_FONT xmaximum 160
    vbox:
        pos (572,R13_SIDE_QUESTION_TOP+78) spacing 8
        for i,((label,command,read),height) in enumerate(visible):
            button:
                id ("r13_side_topic_"+str(i+1))
                xsize 608 ysize height padding (0,0)
                background r13_notebook_question_surface(read)
                hover_background r13_notebook_question_surface(read,True)
                action r13_safe_question_action(command) sensitive ready
                activate_sound R13_MAP_TICK
                at r13_question_row_motion
                fixed:
                    add Solid("#8c71552b",xsize=576,ysize=1) xpos 16 ypos (height-1)
                    if len(r13_question_summary(label))<15:
                        add Transform(r13_notebook_lineart(label),xysize=(204,78),alpha=.22) xalign 1.0 yalign .5
                    add Transform(Crop((20,16,24,32),r13_asset_path("file:assets/ui-b-question/b_icon_acorn_done.png") if read else r13_asset_path("file:assets/ui-b-question/b_icon_acorn.png")),xysize=(27,36)) xpos 20 yalign .5
                    text str(i+1) xpos 53 yalign .5 size (r13_type("small")) color (r13_type_color("muted")) font R13_UI_BOLD_FONT
                    text r13_question_caption(label,False,mark_unread=False) xpos 82 yalign .5 xsize 506 size (r13_type("emphasis")) line_spacing 2 color ((r13_type_color("muted")) if read else (r13_type_color("ink"))) hover_color (r13_type_color("accent")) font R13_UI_BOLD_FONT
                    if read:
                        text "✓" xpos 30 yalign .74 size r13_type("small") color "#6c765a" font "assets/Room13Sans.ttf"
        if not entries:
            frame:
                xsize 608 padding (22,20) background Frame(Crop((16,16,640,84),r13_asset_path("file:assets/ui-b-question/b_panel_card.png")),80,24)
                text "지금 더 물을 이야기는 없다.\n가지고 온 자료를 보여줄 수도 있다." xsize 592 size (r13_type("subtitle")) color (r13_type_color("muted")) font R13_UI_BOLD_FONT
    if len(pages)>1:
        textbutton "← 이전 질문":
            id "r13_topics_previous"
            area (572,r13_notebook_topic_y()-(96 if r13_touch_ui() else 60),296,(88 if r13_touch_ui() else 48))
            background None hover_background None text_color (r13_type_color("muted")) text_hover_color (r13_type_color("accent")) text_insensitive_color (r13_type_color("disabled")) text_font R13_UI_BOLD_FONT text_size (r13_type("body")) padding (12,4) text_yalign .5
            action SetLocalVariable("page",page-1) sensitive ready and page>0
        textbutton "다음 질문 →":
            id "r13_topics_next"
            area (884,r13_notebook_topic_y()-(96 if r13_touch_ui() else 60),296,(88 if r13_touch_ui() else 48))
            background None hover_background None text_color (r13_type_color("muted")) text_hover_color (r13_type_color("accent")) text_insensitive_color (r13_type_color("disabled")) text_font R13_UI_BOLD_FONT text_size (r13_type("body")) padding (12,4) text_yalign .5
            action SetLocalVariable("page",page+1) sensitive ready and page<len(pages)-1
    if ready:
        for i,((label,command,read),height) in enumerate(visible):
            key ("K_%d"%(i+1)) action r13_safe_question_action(command)
            key ("K_KP%d"%(i+1)) action r13_safe_question_action(command)
    if return_action is not None:
        use r13_notebook_topic_action(1034,146,"돌아가기",return_action,ready,icon=None)


# 질문 한 줄: 올리면 살짝 오른쪽으로 나와 「누를 수 있다」를 보이고, 내리면 제자리.
transform r13_question_row_motion:
    on idle:
        ease .08 xoffset 0
    on hover:
        ease .08 xoffset 6
