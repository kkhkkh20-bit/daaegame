# B notebook interview: shared paper components, original question actions and gates.
init 80 python:
    R13_SIDE_QUESTION_TOP=150

    def r13_side_question_pages(entries):
        """Fit complete measured rows; overflow uses visible pages, never scrolling."""
        rows=[]
        for title,action,read in entries:
            label=r13_question_caption(title,False,mark_unread=False)
            text=Text(label,font=R13_UI_BOLD_FONT,size=r13_read_size(26,28),xsize=506,line_spacing=2)
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

    def r13_notebook_topic_y():
        return 550 if r13_touch_ui() else 574

    def r13_notebook_lineart(title):
        # Decorative scenery only: never encode evidence, importance, or truth.
        kind="market" if "장터" in title else "winter" if any(w in title for w in ("겨울","눈","날씨")) else "village" if "마을" in title else "book_corner"
        return "assets/ui-b-question/b_lineart_"+kind+".png"

    def r13_notebook_button_surface(primary=False,hovered=False):
        return Frame(Crop((16,10,128,32),"assets/ui-b-question/b_button_primary.png" if primary else "assets/ui-b-question/b_button.png"),16,10)

    def r13_original_card_surface(path,width):
        # Uniform scale of the actual artwork; centre within the larger hit area.
        return Fixed(Transform(Crop((16,16,640,84),path),zoom=width/640.0,align=(.5,.5)))

    def r13_notebook_question_surface(read=False,focused=False):
        return Solid("#fff8e940" if focused else "#00000000")

    def r13_notebook_button_icon(icon,color="#503525"):
        boxes={"icon_document":(14,8,36,48),"icon_book_open":(8,18,48,27),"icon_arrow_left_bold":(8,18,48,27),"b_icon_more":(16,20,32,24)}
        return Transform(Crop(boxes[icon],"assets/ui-b-question/"+icon+".png"),xysize=(24,24),fit="contain")

screen r13_notebook_topic_action(x,w,caption,command,ready=True,primary=False,icon=None,control_id=None):
    fixed:
        area (x,r13_notebook_topic_y(),w,88 if r13_touch_ui() else 64)
        $ state_icon=r13_notebook_button_icon(icon) if icon else None
        use r13_state_button(caption,command,w,88 if r13_touch_ui() else 64,family="primary" if primary else "standard",enabled=ready,icon=state_icon,text_size=24 if r13_touch_ui() else 22,control_id=control_id or ("r13_notebook_"+caption))

screen r13_notebook_topic_tools(ready,person,present_action):
    if present_action is not None:
        use r13_notebook_topic_action(572,146,"자료 제시",present_action,ready,True,"icon_document")
    use r13_notebook_topic_action(726,146,"기록",Show("r13_records",target=person,present_action=present_action),ready,icon="icon_book_open")
    use r13_notebook_topic_action(880,146,"더보기",Show("r13_more_tools"),ready,icon="b_icon_more")

screen r13_side_question_list(person,pose,entries,ready,return_action=None,caption=""):
    default page=0
    $ pages=r13_side_question_pages(entries)
    $ page=min(page,len(pages)-1)
    $ visible=pages[page]
    add Solid("#29232625")
    add r13_close_art(person,pose,840):
        xpos r13_close_x(person,pose,840)-340 xanchor .5 ypos r13_close_y(person,840,110,pose)
    add "assets/ui-b-question/b_panel_book.png" xpos 488 ypos 144
    add Transform(Frame(Crop((16,12,288,40),"assets/ui-b-question/b_tab_title.png"),32,12),xysize=(420,52)) xpos 560 ypos 166
    add Transform(Crop((20,16,23,32),"assets/ui-b-question/b_icon_acorn.png"),xysize=(29,40)) xpos 578 ypos 174
    text (caption or "묻고 싶은 이야기") xpos 618 ypos 176 xsize 340 size 30 color "#fff4df" font R13_UI_BOLD_FONT
    add Transform("assets/ui-b-question/b_lineart_book_corner.png",xysize=(174,67),alpha=.45) xpos 1024 ypos 156
    text ("질문 %d개"%len(entries) if len(pages)==1 else "%d / %d쪽"%(page+1,len(pages))) xpos 1100 ypos 204 size 17 color "#816b53" font R13_UI_BOLD_FONT
    # Name stays next to the speaker, clear of the notebook and their face.
    add Transform("assets/ui-b-question/nameplate_paper.png",xysize=(246,94)) xpos 78 ypos 566
    add Transform(Crop((20,16,23,32),"assets/ui-b-question/b_icon_acorn.png"),xysize=(25,34)) xpos 112 ypos 595
    text R13_NAMES[person] xpos 150 ypos 594 size 30 color "#503525" font R13_UI_BOLD_FONT xmaximum 160
    vbox:
        pos (572,R13_SIDE_QUESTION_TOP+78) spacing 8
        for i,((label,command,read),height) in enumerate(visible):
            button:
                id ("r13_side_topic_"+str(i+1))
                xsize 608 ysize height padding (0,0)
                background r13_notebook_question_surface(read)
                hover_background r13_notebook_question_surface(read,True)
                action r13_safe_question_action(command) sensitive ready
                fixed:
                    add Solid("#8c71552b",xsize=576,ysize=1) xpos 16 ypos (height-1)
                    if len(r13_question_summary(label))<15:
                        add Transform(r13_notebook_lineart(label),xysize=(204,78),alpha=.22) xalign 1.0 yalign .5
                    add Transform(Crop((20,16,24,32),"assets/ui-b-question/b_icon_acorn_done.png" if read else "assets/ui-b-question/b_icon_acorn.png"),xysize=(27,36)) xpos 20 yalign .5
                    text str(i+1) xpos 53 yalign .5 size 18 color "#9b7b5b" font R13_UI_BOLD_FONT
                    text r13_question_caption(label,False,mark_unread=False) xpos 82 yalign .5 xsize 506 size r13_read_size(26,28) line_spacing 2 color ("#786650" if read else "#4b3420") font R13_UI_BOLD_FONT
                    if read:
                        text "✓" xpos 30 yalign .74 size 17 color "#6c765a" font "assets/Room13Sans.ttf"
        if not entries:
            frame:
                xsize 608 padding (22,20) background Frame(Crop((16,16,640,84),"assets/ui-b-question/b_panel_card.png"),80,24)
                text "지금 더 물을 이야기는 없다.\n가지고 온 자료를 보여줄 수도 있다." xsize 592 size r13_read_size(24,28) color "#6b5641" font R13_UI_BOLD_FONT
    if len(pages)>1:
        textbutton "← 이전 질문":
            id "r13_topics_previous"
            area (572,r13_notebook_topic_y()-(96 if r13_touch_ui() else 60),296,(88 if r13_touch_ui() else 48))
            background None hover_background None text_color "#72563e" text_hover_color "#b83b32" text_insensitive_color "#b6a58d" text_font R13_UI_BOLD_FONT text_size r13_read_size(22,26) padding (12,4) text_yalign .5
            action SetLocalVariable("page",page-1) sensitive ready and page>0
        textbutton "다음 질문 →":
            id "r13_topics_next"
            area (884,r13_notebook_topic_y()-(96 if r13_touch_ui() else 60),296,(88 if r13_touch_ui() else 48))
            background None hover_background None text_color "#72563e" text_hover_color "#b83b32" text_insensitive_color "#b6a58d" text_font R13_UI_BOLD_FONT text_size r13_read_size(22,26) padding (12,4) text_yalign .5
            action SetLocalVariable("page",page+1) sensitive ready and page<len(pages)-1
    if ready:
        for i,((label,command,read),height) in enumerate(visible):
            key ("K_%d"%(i+1)) action r13_safe_question_action(command)
            key ("K_KP%d"%(i+1)) action r13_safe_question_action(command)
    if return_action is not None:
        use r13_notebook_topic_action(1034,146,"돌아가기",return_action,ready,icon="icon_arrow_left_bold")
