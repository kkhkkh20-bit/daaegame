# Torn-paper decisions: decorative UI cannot predict a choice's outcome.
default r13_choice_hidden_actor = None

init 81 python:
    def r13_notebook_choice_pages(entries,width,height):
        rows=[]
        for entry in entries:
            label=r13_question_caption(entry[0],False,False)
            text=Text(label,font=R13_UI_BOLD_FONT,size=r13_read_size(32,34),xsize=width-184,line_spacing=4)
            measured=int(renpy.render(text,width-184,720,0,0).get_size()[1])
            rows.append((entry,max(96,measured+28)))
        # Equal paper cards: the longest option sets the shared row height.
        row_height=max((height for entry,height in rows),default=88 if r13_touch_ui() else 80)
        rows=[(entry,row_height) for entry,height in rows]
        pages=[];page=[];used=0
        for entry,h in rows:
            if page and (used+16+h>height or len(page)>=9):
                pages.append(page);page=[];used=0
            page.append((entry,h));used+=h+(16 if len(page)>1 else 0)
        return pages+([page] if page else []) or [[]]

    def r13_notebook_note():
        # Crop the paper body before nine-slicing; the original large transparent
        # margin above the tape must not consume half of a 92px heading.
        return r13_sticker_button()

    def r13_notebook_choice_surface(width,hovered=False):
        return r13_sticker_button(focused=hovered)

    def r13_notebook_choice_geometry(entries,width,heading,subline=None):
        size=r13_read_size(36,38)
        text=Text(heading,font=R13_UI_BOLD_FONT,size=size,xsize=width-102,line_spacing=4)
        measured=int(renpy.render(text,width-102,720,0,0).get_size()[1])
        if subline:
            # 2026-10-27 쟁점 제목: 직전 대사는 쟁점 아래 작은 줄로 남고, 머리 칸이 그만큼 자란다.
            small=Text(subline,font=R13_UI_BOLD_FONT,size=r13_read_size(22,26),xsize=width-102,line_spacing=2)
            measured+=8+int(renpy.render(small,width-102,720,0,0).get_size()[1])
        header=max(112,measured+44)
        cap=max(120,460-header-28)
        pages=r13_notebook_choice_pages(entries,width,cap)
        if len(pages)>1:
            pages=r13_notebook_choice_pages(entries,width,max(120,cap-(100 if r13_touch_ui() else 66)))
        return header,pages

screen r13_notebook_choice_list(person,pose,title,entries,ready,return_action=None,caption="",carriage=False):
    default page=0
    default focused_choice=None
    $ left=220 if person or carriage else 190
    $ width=560 if person or carriage else 900
    $ context=r13_choice_context() if title=="선택" else None
    # 2026-10-27: 표(room13_choice_issues.rpy)에 있는 무거운 선택만 쟁점을 제목으로 쓴다. 나머지는 예전 그대로.
    $ issue=r13_choice_issue(entries) if title=="선택" else None
    $ heading=issue or caption or (context[1] if context else "어떻게 할까?" if title=="선택" else title)
    $ subline=r13_choice_issue_subline(caption,context,20 if width<900 else 34) if issue else None
    $ header_height,pages=r13_notebook_choice_geometry(entries,width,heading,subline)
    $ page=min(page,len(pages)-1)
    $ visible=pages[page]
    $ rows_height=sum(row[1] for row in visible)+max(0,len(visible)-1)*16
    $ header_top=180 if header_height<=112 and len(pages)==1 else max(40,640-header_height-28-rows_height-((100 if r13_touch_ui() else 66) if len(pages)>1 else 0))
    $ rows_top=header_top+header_height+28
    if person and not carriage:
        # 2026-10-26 소유자: 인물 그림은 스티커 없이 간다.
        add r13_close_art(person,pose,760):
            xpos r13_close_x(person,pose,760)+390 xanchor .5 ypos r13_close_y(person,760,70,pose)
    frame:
        xpos left+20 ypos header_top xsize width-40 ysize header_height padding (42,22,24,22) background r13_notebook_note()
        if subline:
            vbox:
                align (.5,.5) spacing 8
                text heading id "r13_choice_issue" xsize width-106 text_align .5 size r13_read_size(36,38) color "#4b3022" font R13_UI_BOLD_FONT line_spacing 4
                text subline xsize width-106 text_align .5 size r13_read_size(22,26) color "#7a5a40" font R13_UI_BOLD_FONT line_spacing 2
        else:
            text heading xsize width-106 align (.5,.5) text_align .5 size r13_read_size(36,38) color "#4b3022" font R13_UI_BOLD_FONT line_spacing 4
    add Transform(r13_asset_path("file:assets/ui-b-question/b_tape_red.png"),xysize=(64,22),rotate=-16) xpos left+8 ypos header_top-24
    vbox:
        pos (left,rows_top) spacing 16
        for i,((label,command,read),height) in enumerate(visible):
            button:
                id (("r13_carriage_choice_" if carriage else "r13_notebook_choice_")+str(i+1))
                xsize width ysize height padding (0,0)
                background r13_notebook_choice_surface(width)
                hover_background r13_notebook_choice_surface(width,True)
                action r13_safe_question_action(command) sensitive ready
                hovered SetLocalVariable("focused_choice",i)
                unhovered SetLocalVariable("focused_choice",None)
                fixed:
                    # Selection uses ink/acorn emphasis; no repeated tape.
                    frame:
                        xpos 60 yalign .5 xysize (54,54) padding (3,3) background Solid("#fff6e6")
                        fixed:
                            add Solid("#bc4134" if focused_choice==i else "#654129")
                            text str(i+1) align (.5,.5) size r13_read_size(30,34) color "#fff7e8" font R13_UI_BOLD_FONT
                    text "·" xpos 130 yalign .5 size 28 color "#654129" font R13_UI_BOLD_FONT
                    text r13_question_caption(label,False,False) xpos 160 yalign .5 xsize width-184 size r13_read_size(32,34) font R13_UI_BOLD_FONT color "#4b3420" line_spacing 4
                    if focused_choice==i:
                        add Transform(Crop((20,16,23,32),r13_asset_path("file:assets/ui-b-question/b_icon_acorn.png")),zoom=2.0) xpos -26 yalign .5
        if not entries:
            frame:
                xsize width padding (26,22) background r13_notebook_note()
                text "지금 더 물을 이야기는 없다.\n가지고 온 자료를 보여줄 수도 있다." xsize width-52 size r13_read_size(24,28) color "#6b5641" font R13_UI_BOLD_FONT
    if len(pages)>1:
        hbox:
            pos (left,rows_top+rows_height+12) spacing 16
            textbutton "← 이전":
                xsize (width-16)//2 ysize (88 if r13_touch_ui() else 54) padding (12,4)
                background r13_notebook_button_surface()
                hover_background r13_notebook_button_surface(False,True)
                text_font R13_UI_BOLD_FONT text_color "#6b4932" text_hover_color "#6b4932" text_insensitive_color "#a99b86" text_size r13_read_size(22,26)
                action SetLocalVariable("page",page-1) sensitive ready and page>0
            textbutton "다음 →":
                xsize (width-16)//2 ysize (88 if r13_touch_ui() else 54) padding (12,4)
                background r13_notebook_button_surface()
                hover_background r13_notebook_button_surface(False,True)
                text_font R13_UI_BOLD_FONT text_color "#6b4932" text_hover_color "#6b4932" text_insensitive_color "#a99b86" text_size r13_read_size(22,26)
                action SetLocalVariable("page",page+1) sensitive ready and page<len(pages)-1
    if ready:
        for i,((label,command,read),height) in enumerate(visible):
            key ("K_%d"%(i+1)) action r13_safe_question_action(command)
            key ("K_KP%d"%(i+1)) action r13_safe_question_action(command)
    if return_action is not None:
        use r13_notebook_topic_action(1044,152,"돌아가기",return_action,ready,icon="icon_arrow_left_bold")
