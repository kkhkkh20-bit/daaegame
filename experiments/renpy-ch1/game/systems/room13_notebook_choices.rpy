# Torn-paper decisions: decorative UI cannot predict a choice's outcome.
# 2026-10-27 타이포 시안(R13_TYPE_V2, systems/room13_type_scale.rpy): 머리 hero · 본문 display · 번호 title ·
#   작은 줄 emphasis · 쪽 넘김 body. 꺼져 있으면 size/color 는 이전 값 그대로다.
default r13_choice_hidden_actor = None

init 81 python:
    # 2026-10-28 소유자: "선택지 글자가 쓸모없이 크다. 질문보다 답변이 훨씬 커서 글씨 줄이고 비율 맞춰".
    # 선택지 본문은 display(36) 에서 emphasis(26) 로 내린다. 머리 글(질문)은 display·작게면 subtitle 그대로라 늘 선택지보다 크다.
    R13_CHOICE_BODY="emphasis"
    R13_CHOICE_TEXT_PAD=116   # 번호 칸(36~90)·사이·오른쪽 여백. 예전 184(번호 60 + 「·」 130 + 글자 160)
    def r13_notebook_choice_pages(entries,width,height,split=False):
        # 2026-10-28 소유자(7일 빨래터 선택 캡처): "왜 이리 두껍고 튀어나와". 가장 긴 선택지(세 줄)에 칸 높이를 모두 맞추던
        # 것을 그만두고, 칸마다 제 글자 높이만큼만 갖는다(최소 64, 터치 80). 글자 폭은 번호 자리를 줄인 width-R13_CHOICE_TEXT_PAD.
        minimum=80 if r13_touch_ui() else 60
        rows=[]
        for entry in entries:
            label=r13_question_caption(entry[0],False,False)
            text=Text(label,font=R13_UI_BOLD_FONT,size=(r13_type(R13_CHOICE_BODY)),xsize=width-R13_CHOICE_TEXT_PAD,line_spacing=4)
            measured=int(renpy.render(text,width-R13_CHOICE_TEXT_PAD,720,0,0).get_size()[1])
            rows.append((entry,max(minimum,measured+28),measured+20))
        def total(rs):
            return sum(h for e,h,m in rs)+16*max(0,len(rs)-1)
        def shrink(rs):
            # 넘치면 칸 위아래 여백만 줄인다. 글자가 든 높이(m) 아래로는 줄이지 않는다.
            over=total(rs)-height
            if over<=0:return [(e,h) for e,h,m in rs]
            out=[]
            for e,h,m in rs:
                cut=min(h-m,-(-over//max(1,len(rs))))
                out.append((e,h-cut))
            return out
        # 2026-10-27 소유자: "선택지 하나짜리 선택지창이 존재하면 안 되지". 쪽을 나눠도 한 쪽에 하나만 남기지 않는다.
        n=len(rows)
        if not rows:return [[]]
        if n<=4:
            one=shrink(rows)
            # 2026-10-28 다른 길 12일: 넷이 바닥 높이로도 안 들어가면 2+2 로 나눈다(셋 이하는 나누면 하나짜리 쪽이 생긴다).
            # 나누기는 호출자가 머리글을 줄여 보고도 안 들어갈 때만 부탁한다(split). 넓은 판의 짧은 넷이 갈리지 않게.
            if n<4 or not split or sum(h for e,h in one)+16*(n-1)<=height:return [one]
            return [shrink(rows[:2]),shrink(rows[2:])]
        tallest=max(h for e,h,m in rows)
        per=max(2,min(9,(height+16)//(tallest+16)))
        count=max(1,-(-n//per))
        base,extra=divmod(n,count)
        if base<2 and count>1:count-=1;base,extra=divmod(n,count)
        pages=[];i=0
        for k in range(count):
            size=base+(1 if k<extra else 0);pages.append(shrink(rows[i:i+size]));i+=size
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
        size=(r13_type("title"))   # 2026-10-28: 머리 글 title(30) · 선택지 emphasis(26)
        text=Text(heading,font=R13_UI_BOLD_FONT,size=size,xsize=width-102,line_spacing=4)
        measured=int(renpy.render(text,width-102,720,0,0).get_size()[1])
        if subline:
            # 2026-10-27 쟁점 제목: 직전 대사는 쟁점 아래 작은 줄로 남고, 머리 칸이 그만큼 자란다.
            small=Text(subline,font=R13_UI_BOLD_FONT,size=(r13_type("emphasis")),xsize=width-102,line_spacing=2)
            measured+=8+int(renpy.render(small,width-102,720,0,0).get_size()[1])
        header=max(72,measured+32)   # 2026-10-28 소유자 「질문이 너무 크게 박혀 있다」: 판을 글자 높이에 맞춘다(예전 최소 112)
        cap=max(120,460-header-28)
        pages=r13_notebook_choice_pages(entries,width,cap)
        if (len(pages)>1 or not r13_notebook_choice_fits(pages,cap)) and subline and _retry:
            # 작은 줄 때문에 선택지가 두 쪽으로 갈리거나 칸이 모자라면(13일 가족 제안, 좁은 판) 작은 줄을 뺀다.
            # 한 쪽에 다 보이는 것이 직전 대사보다 중요하다.
            return r13_notebook_choice_geometry(entries,width,heading,None,False)
        if len(pages)==1 and not r13_notebook_choice_fits(pages,cap):
            # 넷 이하인데 머리글이 커서 칸이 안 들어가면 머리글을 한 단 작게 재고, 그래도 모자라면 칸을 아래로 더 내린다(최대 60).
            small=Text(heading,font=R13_UI_BOLD_FONT,size=r13_type("title"),xsize=width-102,line_spacing=4)
            header=max(72,int(renpy.render(small,width-102,720,0,0).get_size()[1])+32)
            cap=max(120,460-header-28+60)
            pages=r13_notebook_choice_pages(entries,width,cap)
            if not r13_notebook_choice_fits(pages,cap) and len(entries)==4:
                # 작은 머리글로도 넷이 안 들어가면 2+2 로 나눈다(쪽 넘김 버튼 자리만큼 칸이 줄어든다).
                pages=r13_notebook_choice_pages(entries,width,max(120,cap-(100 if r13_touch_ui() else 66)),split=True)
            return header,pages,"__small__"
        if len(pages)>1:
            pages=r13_notebook_choice_pages(entries,width,max(120,cap-(100 if r13_touch_ui() else 66)))
        return header,pages,subline

screen r13_notebook_choice_list(person,pose,title,entries,ready,return_action=None,caption="",carriage=False):
    default page=0
    default focused_choice=None
    # 2026-10-28 소유자: 인물 옆 판이 좁아(560) 선택지가 세 줄로 접혔다. 인물은 오른쪽(약 860~)에 서므로 왼쪽으로 넓힌다.
    $ left=(220 if carriage else 110 if person else 190)
    $ width=(560 if carriage else 680 if person else 900)
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
    # 2026-10-28: 머리글 180 고정은 칸이 640 안에 들어올 때만. 넘치면 위로 올려 자리를 번다.
    # 2026-10-28 소유자: "선택지 질문이 너무 정중앙에 크게 박혀 있어. 좀 더 위로 올리고 배치 맞춰". 질문 판은 위 줄(장소·날짜판) 바로
    # 아래(112)에 두고 선택지는 그 밑으로 이어 붙인다. 아래가 모자랄 때만 위로 당긴다(최소 40).
    $ pager_h=((100 if r13_touch_ui() else 66) if len(pages)>1 else 0)
    $ header_top=max(40,min(112,640-header_height-20-rows_height-pager_h))
    $ rows_top=header_top+header_height+20
    if person and not carriage:
        # 2026-10-26 소유자: 인물 그림은 스티커 없이 간다.
        # 2026-10-28 소유자 「캐릭터도 너무 위로 올라가 있다」: 머리 위 여백을 70 → 150 으로 내린다(위 줄 날짜판과 겹치지 않게).
        add r13_close_art(person,pose,760):
            xpos r13_close_x(person,pose,760)+390 xanchor .5 ypos r13_close_y(person,760,150,pose)
    frame:
        xpos left+20 ypos header_top xsize width-40 ysize header_height padding (32,12,24,12) background r13_notebook_note()
        if subline:
            vbox:
                align (.5,.5) spacing 8
                text heading id "r13_choice_issue" xsize width-106 text_align .5 size (r13_type("subtitle") if heading_small else r13_type("title")) color (r13_type_color("ink")) font R13_UI_BOLD_FONT line_spacing 4
                text subline xsize width-106 text_align .5 size (r13_type("emphasis")) color (r13_type_color("muted")) font R13_UI_BOLD_FONT line_spacing 2
        else:
            text heading xsize width-106 align (.5,.5) text_align .5 size (r13_type("subtitle") if heading_small else r13_type("title")) color (r13_type_color("ink")) font R13_UI_BOLD_FONT line_spacing 4
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
                        xpos 26 yalign .5 xysize (40,40) padding (3,3) background Solid("#fff6e6")
                        fixed:
                            add Solid("#bc4134" if focused_choice==i else "#654129")
                            text str(i+1) align (.5,.5) size (r13_type("emphasis")) color (r13_type_color("inverse")) font R13_UI_BOLD_FONT
                    text r13_question_caption(label,False,False) xpos 88 yalign .5 xsize width-R13_CHOICE_TEXT_PAD size (r13_type(R13_CHOICE_BODY)) font R13_UI_BOLD_FONT color (r13_type_color("ink")) line_spacing 4
                    if focused_choice==i:
                        add Transform(Crop((20,16,23,32),r13_asset_path("file:assets/ui-b-question/b_icon_acorn.png")),zoom=2.0) xpos -40 yalign .5
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

# 2026-10-28 소유자 시안 C 선택: 아빠의 물음(메뉴 머리 글·쟁점)은 아래 대사판에 「아빠」 리본과 함께, 선택지는 그 위 오른쪽 세로 목록.
# 질문 판이 화면 가운데를 차지하지 않고, 대사와 같은 자리에서 읽힌다. 대사창과 선택지는 겹치지 않는다(목록 바닥 = 리본 위).
init 82 python:
    R13_CHOICE_C_LIST_BOTTOM=520    # 목록 바닥 상한. 실제로는 대사판 리본 위 12px 와 더 낮은 쪽
    R13_CHOICE_C_LIST_TOP=104       # 위 줄(장소·날짜판) 아래
    R13_CHOICE_C_WIDTH=640
    R13_CHOICE_TEXT_NUDGE=2
    def r13_choice_c_geometry(entries,width):
        avail=R13_CHOICE_C_LIST_BOTTOM-R13_CHOICE_C_LIST_TOP
        pages=r13_notebook_choice_pages(entries,width,avail)
        if len(pages)>1 or not r13_notebook_choice_fits(pages,avail):
            pager=(100 if r13_touch_ui() else 66)
            pages=r13_notebook_choice_pages(entries,width,avail-pager,split=True)
        # 2026-10-28 소유자: "균일한 폰트에 균일한 상하 폭 맞아? 다 각기 달라 보인다". 한 화면의 칸은 모두 같은 높이(가장 긴 칸)로,
        # 글자는 칸 가운데. 판 폭(R13_CHOICE_C_WIDTH)을 넓혀 대부분 한 줄에 들어가게 해 두꺼워지지 않게 한다.
        tallest=max([h for page in pages for e,h in page] or [0])
        return [[(e,tallest) for e,h in page] for page in pages]

screen r13_choice_c(person,pose,entries,ready,caption=""):
    default page=0
    default focused_choice=None
    $ width=R13_CHOICE_C_WIDTH
    $ left=(600 if person else 320)
    $ context=r13_choice_context()
    $ issue=r13_choice_issue(entries)
    $ heading=issue or caption or (context[1] if context else "어떻게 할까?")
    $ subline=r13_choice_issue_subline(caption,context,34) if issue else None
    $ thought=heading.strip().startswith("(")
    $ pages=r13_choice_c_geometry(entries,width)
    $ page=min(page,len(pages)-1)
    $ visible=pages[page]
    $ pager_h=((100 if r13_touch_ui() else 66) if len(pages)>1 else 0)
    $ rows_height=sum(row[1] for row in visible)+max(0,len(visible)-1)*10
    $ list_bottom=min(R13_CHOICE_C_LIST_BOTTOM,r13_night_panel_top(heading+("\n"+subline if subline else ""))-48)   # 윗변 위로 올라간 리본보다 위
    $ rows_top=list_bottom-pager_h-rows_height
    if person:
        add r13_close_art(person,pose,760):
            xpos 330 xanchor .5 ypos r13_close_y(person,760,150,pose)
    # 대사판: 일반 대사창과 같은 계산(r13_night_panel_top·r13_night_say_top)이라 높이·리본·글자 자리가 같다.
    $ say_text=heading+("\n"+subline if subline else "")
    $ say_top=r13_night_say_top(say_text)
    add Transform(Frame(Crop((16,16,1168,128),r13_asset_path("file:assets/ui-b-dialogue/b_panel_dialogue.png")),48,24,64,24),xysize=(1220,R13_NIGHT_PAPER_BOTTOM-r13_night_panel_top(say_text)),alpha=r13_night_shade_alpha()) xpos 30 ypos r13_night_panel_top(say_text)
    frame:
        xpos 120 ypos (r13_night_panel_top(say_text)-R13_SAY_RIBBON_LIFT) yanchor .5 background Frame(Crop((16,12,168,32),r13_asset_path("file:assets/ui-b-dialogue/b_ribbon_name.png")),16,6,32,6) padding (22,8,36,10)
        text "아빠" color (r13_type_color("inverse")) font R13_UI_BOLD_FONT size (r13_type("title")) outlines []
    vbox:
        xpos 120 ypos say_top spacing 4
        text heading id "r13_choice_issue" xsize 1090 size r13_night_say_size() color ("#2A5FA8" if thought else r13_type_color("ink")) font R13_UI_BOLD_FONT line_spacing 4
        if subline:
            text subline xsize 1090 size (r13_type("small")) color (r13_type_color("muted")) font R13_UI_BOLD_FONT
    vbox:
        pos (left,rows_top) spacing 10
        for i,((label,command,read),height) in enumerate(visible):
            button:
                id ("r13_notebook_choice_"+str(i+1))
                xsize width ysize height padding (0,0)
                background r13_notebook_choice_surface(width)
                hover_background r13_notebook_choice_surface(width,True)
                action r13_safe_question_action(command) sensitive ready
                hovered SetLocalVariable("focused_choice",i)
                unhovered SetLocalVariable("focused_choice",None)
                fixed:
                    frame:
                        xpos 22 yalign .5 xysize (40,40) padding (3,3) background Solid("#fff6e6")
                        fixed:
                            add Solid("#bc4134" if focused_choice==i else "#654129")
                            text str(i+1) align (.5,.5) size (r13_type("emphasis")) color (r13_type_color("inverse")) font R13_UI_BOLD_FONT
                    # 2026-10-28 소유자 「두 줄 선택지가 위로 치우쳐 보인다」: 실측(캡처) 위 여백이 아래보다 3~4px 작았다.
                    # 마지막 줄 뒤에도 붙는 줄 간격(4)과 글꼴의 아래 여백 때문이다. 그만큼 내려 가운데에 맞춘다.
                    text r13_question_caption(label,False,False) xpos 84 yalign .5 yoffset R13_CHOICE_TEXT_NUDGE xsize width-R13_CHOICE_TEXT_PAD size (r13_type(R13_CHOICE_BODY)) font R13_UI_BOLD_FONT color (r13_type_color("ink")) line_spacing 4
    if len(pages)>1:
        hbox:
            pos (left,list_bottom-pager_h+12) spacing 16
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
