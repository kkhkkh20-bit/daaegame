# Torn-paper decisions: decorative UI cannot predict a choice's outcome.
# 2026-10-27 타이포 시안(R13_TYPE_V2, systems/room13_type_scale.rpy): 머리 hero · 본문 display · 번호 title ·
#   작은 줄 emphasis · 쪽 넘김 body. 꺼져 있으면 size/color 는 이전 값 그대로다.
default r13_choice_hidden_actor = None

init 81 python:
    def r13_notebook_choice_pages(entries,width,height):
        rows=[]
        for entry in entries:
            label=r13_question_caption(entry[0],False,False)
            text=Text(label,font=R13_UI_BOLD_FONT,size=(r13_type("display")),xsize=width-184,line_spacing=4)
            measured=int(renpy.render(text,width-184,720,0,0).get_size()[1])
            rows.append((entry,max(96,measured+28),measured+20))
        # Equal paper cards: the longest option sets the shared row height.
        row_height=max((h for entry,h,m in rows),default=88 if r13_touch_ui() else 80)
        floor=max((m for entry,h,m in rows),default=64)
        # 2026-10-27 소유자: "선택지 하나짜리 선택지창이 존재하면 안 되지". 쪽을 나눠도 한 쪽에 하나만 남기지 않는다.
        # 넷 이하는 늘 한 쪽에 둔다. 칸은 글자가 든 높이(floor) 아래로는 줄이지 않는다 — 그보다 모자라면 호출한 쪽이 머리글을 줄인다.
        n=len(rows)
        if n<=4:
            if n*row_height+16*(n-1)>height:row_height=max(floor,(height-16*(n-1))//max(1,n))
            return [[(entry,row_height) for entry,h,m in rows]] if rows else [[]]
        per=max(2,min(9,(height+16)//(row_height+16)))
        count=max(1,-(-n//per))
        base,extra=divmod(n,count)
        if base<2 and count>1:count-=1;base,extra=divmod(n,count)
        pages=[];i=0
        for k in range(count):
            size=base+(1 if k<extra else 0);pages.append([(entry,row_height) for entry,h,m in rows[i:i+size]]);i+=size
        return pages or [[]]

    def r13_notebook_choice_fits(pages,height):
        return all(sum(h for e,h in page)+16*(len(page)-1)<=height for page in pages)

    def r13_notebook_note():
        # Crop the paper body before nine-slicing; the original large transparent
        # margin above the tape must not consume half of a 92px heading.
        return r13_sticker_button()

    def r13_notebook_choice_surface(width,hovered=False):
        return r13_sticker_button(focused=hovered)

    def r13_notebook_choice_geometry(entries,width,heading,subline=None,_retry=True):
        size=(r13_type("display"))
        text=Text(heading,font=R13_UI_BOLD_FONT,size=size,xsize=width-102,line_spacing=4)
        measured=int(renpy.render(text,width-102,720,0,0).get_size()[1])
        if subline:
            # 2026-10-27 쟁점 제목: 직전 대사는 쟁점 아래 작은 줄로 남고, 머리 칸이 그만큼 자란다.
            small=Text(subline,font=R13_UI_BOLD_FONT,size=(r13_type("emphasis")),xsize=width-102,line_spacing=2)
            measured+=8+int(renpy.render(small,width-102,720,0,0).get_size()[1])
        header=max(112,measured+44)
        cap=max(120,460-header-28)
        pages=r13_notebook_choice_pages(entries,width,cap)
        if (len(pages)>1 or not r13_notebook_choice_fits(pages,cap)) and subline and _retry:
            # 작은 줄 때문에 선택지가 두 쪽으로 갈리거나 칸이 모자라면(13일 가족 제안, 좁은 판) 작은 줄을 뺀다.
            # 한 쪽에 다 보이는 것이 직전 대사보다 중요하다.
            return r13_notebook_choice_geometry(entries,width,heading,None,False)
        if len(pages)==1 and not r13_notebook_choice_fits(pages,cap):
            # 넷 이하인데 머리글이 커서 칸이 안 들어가면 머리글을 한 단 작게 재고, 그래도 모자라면 칸을 아래로 더 내린다(최대 60).
            small=Text(heading,font=R13_UI_BOLD_FONT,size=r13_read_size(28,30),xsize=width-102,line_spacing=4)
            header=max(112,int(renpy.render(small,width-102,720,0,0).get_size()[1])+44)
            cap=max(120,460-header-28+60)
            pages=r13_notebook_choice_pages(entries,width,cap)
            return header,pages,"__small__"
        if len(pages)>1:
            pages=r13_notebook_choice_pages(entries,width,max(120,cap-(100 if r13_touch_ui() else 66)))
        return header,pages,subline

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
    $ header_height,pages,subline=r13_notebook_choice_geometry(entries,width,heading,subline)
    $ heading_small=(subline=="__small__")
    $ subline=None if heading_small else subline
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
                text heading id "r13_choice_issue" xsize width-106 text_align .5 size (r13_type("subtitle") if heading_small else r13_type("display")) color (r13_type_color("ink")) font R13_UI_BOLD_FONT line_spacing 4
                text subline xsize width-106 text_align .5 size (r13_type("emphasis")) color (r13_type_color("muted")) font R13_UI_BOLD_FONT line_spacing 2
        else:
            text heading xsize width-106 align (.5,.5) text_align .5 size (r13_type("subtitle") if heading_small else r13_type("display")) color (r13_type_color("ink")) font R13_UI_BOLD_FONT line_spacing 4
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
                            text str(i+1) align (.5,.5) size (r13_type("title")) color (r13_type_color("inverse")) font R13_UI_BOLD_FONT
                    text "·" xpos 130 yalign .5 size r13_type("subtitle") color "#654129" font R13_UI_BOLD_FONT
                    text r13_question_caption(label,False,False) xpos 160 yalign .5 xsize width-184 size (r13_type("display")) font R13_UI_BOLD_FONT color (r13_type_color("ink")) line_spacing 4
                    if focused_choice==i:
                        add Transform(Crop((20,16,23,32),r13_asset_path("file:assets/ui-b-question/b_icon_acorn.png")),zoom=2.0) xpos -26 yalign .5
        if not entries:
            frame:
                xsize width padding (26,22) background r13_notebook_note()
                text "지금 더 물을 이야기는 없다.\n가지고 온 자료를 보여줄 수도 있다." xsize width-52 size (r13_type("subtitle")) color (r13_type_color("muted")) font R13_UI_BOLD_FONT
    if len(pages)>1:
        hbox:
            pos (left,rows_top+rows_height+12) spacing 16
            textbutton "← 이전":
                xsize (width-16)//2 ysize (88 if r13_touch_ui() else 54) padding (12,4)
                background r13_notebook_button_surface()
                hover_background r13_notebook_button_surface(False,True)
                text_font R13_UI_BOLD_FONT text_color (r13_type_color("muted")) text_hover_color (r13_type_color("muted")) text_insensitive_color (r13_type_color("disabled")) text_size (r13_type("body"))
                action SetLocalVariable("page",page-1) sensitive ready and page>0
            textbutton "다음 →":
                xsize (width-16)//2 ysize (88 if r13_touch_ui() else 54) padding (12,4)
                background r13_notebook_button_surface()
                hover_background r13_notebook_button_surface(False,True)
                text_font R13_UI_BOLD_FONT text_color (r13_type_color("muted")) text_hover_color (r13_type_color("muted")) text_insensitive_color (r13_type_color("disabled")) text_size (r13_type("body"))
                action SetLocalVariable("page",page+1) sensitive ready and page<len(pages)-1
    if ready:
        for i,((label,command,read),height) in enumerate(visible):
            key ("K_%d"%(i+1)) action r13_safe_question_action(command)
            key ("K_KP%d"%(i+1)) action r13_safe_question_action(command)
    if return_action is not None:
        use r13_notebook_topic_action(1044,152,"돌아가기",return_action,ready,icon=None)
