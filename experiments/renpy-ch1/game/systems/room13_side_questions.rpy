# Owner-approved side-by-side conversation layout (0.19.36).
init 80 python:
    def r13_side_question_pages(entries):
        """Fit complete measured rows; overflow uses visible pages, never scrolling."""
        rows=[]
        for title,action,read in entries:
            label=r13_question_caption(title,read,mark_unread=True)
            text=Text(label,font=r13_ui_font(),size=r13_read_size(26,28),xsize=506,line_spacing=2)
            height=int(renpy.render(text,506,720,0,0).get_size()[1])
            rows.append(((title,action,read),max(54,height+16)))
        def pack(cap):
            pages=[];page=[];used=0
            for entry,height in rows:
                if page and (used+8+height>cap or len(page)>=8):
                    pages.append(page);page=[];used=0
                page.append((entry,height));used+=height+(8 if len(page)>1 else 0)
            return pages+([page] if page else []) or [[]]
        cap=r13_control_upper_y()-112-12
        pages=pack(cap)
        return pack(cap-60) if len(pages)>1 else pages

screen r13_side_question_list(person,pose,entries,ready,return_action=None,caption=""):
    default page=0
    $ pages=r13_side_question_pages(entries)
    $ page=min(page,len(pages)-1)
    $ visible=pages[page]
    add Solid("#00000088")
    add r13_close_art(person,pose,840):
        xpos r13_close_x(person,pose,840)-340 xanchor .5 ypos r13_close_y(person,840,110,pose)
    text R13_NAMES[person] xpos 80 ypos 70 size 30 color "#f6d18a" font r13_ui_font() outlines [(1,"#101515",0,0)]
    text (caption or "묻고 싶은 이야기") xpos 640 ypos 70 xsize 360 size 30 color "#fff4df" font r13_ui_font()
    text ("질문 %d개 · 모두 표시"%len(entries) if len(pages)==1 else "질문 %d개 · %d / %d쪽"%(len(entries),page+1,len(pages))) xpos 1000 ypos 92 size 17 color "#d4c8b4" font r13_ui_font()
    vbox:
        pos (640,112) spacing 8
        for i,((label,command,read),height) in enumerate(visible):
            button:
                id ("r13_side_topic_"+str(i+1))
                xsize 592 ysize height padding (20,8)
                background R13ControlSurface()
                hover_background R13ControlSurface(hovered=True)
                action r13_safe_question_action(command) sensitive ready
                hbox:
                    yalign .5 spacing 12
                    text str(i+1) yalign .5 xsize 34 size r13_read_size(26,28) color "#f6dfac" font r13_ui_font()
                    text r13_question_caption(label,read,mark_unread=True) yalign .5 xsize 506 size r13_read_size(26,28) line_spacing 2 color (r13_role_color("subdued") if read else "#fff4df") font r13_ui_font()
        if not entries:
            frame:
                xsize 592 padding (20,20) background R13ControlSurface()
                text "지금 더 물을 이야기는 없다.\n가지고 온 자료를 보여줄 수도 있다." xsize 552 size r13_read_size(24,28) color "#fff4df" font r13_ui_font()
    if len(pages)>1:
        textbutton "← 이전 질문":
            id "r13_topics_previous"
            area (640,r13_control_upper_y()-60,288,48) style "r13_action_button" text_size r13_read_size(22,26) padding (12,4) text_yalign .5
            action SetLocalVariable("page",page-1) sensitive ready and page>0
        textbutton "다음 질문 →":
            id "r13_topics_next"
            area (944,r13_control_upper_y()-60,288,48) style "r13_action_button" text_size r13_read_size(22,26) padding (12,4) text_yalign .5
            action SetLocalVariable("page",page+1) sensitive ready and page<len(pages)-1
    if ready:
        for i,((label,command,read),height) in enumerate(visible):
            key ("K_%d"%(i+1)) action r13_safe_question_action(command)
            key ("K_KP%d"%(i+1)) action r13_safe_question_action(command)
    if return_action is not None:
        use r13_footer_control(0,"돌아가기","dialogue",return_action,enabled=ready)
