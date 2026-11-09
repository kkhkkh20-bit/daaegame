# 실물의 위치를 직접 짚는 읽기 화면. 이 화면은 자료·기회·시간·이야기 값을 쓰지 않는다.
# 칼의 맞물림을 확인한 반환 값의 적용과 다음 대사는 호출한 사건이 소유한다.
init 353 python:
    R13_CASE_INSPECT_ART={
        "knife":"assets/room13-meeting-knife-tip-match.webp",
        "latch":"assets/room13-latch-diagram132.webp",
    }
    R13_CASE_INSPECT_CROP={"knife":(40,180,2100,370),"latch":(0,0,1536,1024)}
    # 원본 그림의 좌표다. 사전 표시나 강조선에는 쓰지 않고 투명 입력 영역에만 쓴다.
    R13_CASE_INSPECT_TARGETS={
        "knife":(("handle",(80,200,830,340)),("blade",(910,250,770,270)),
                 ("tip",(1830,300,300,220)),("fit",(1680,270,160,240))),
        "latch":(("outer",(250,90,280,860)),("inner",(900,650,230,220))),
    }
    R13_CASE_INSPECT_TEXT={
        ("knife","handle"):"나무 손잡이에 끈이 감겨 있다.",
        ("knife","blade"):"손잡이에서 끝으로 이어지는 칼날의 넓은 면이다.",
        ("knife","tip"):"따로 떨어진 금속 조각이다. 한쪽은 뾰족하고 반대쪽은 울퉁불퉁하다.",
        ("knife","fit"):"칼끝의 깨진 선과 파편의 깨진 선이 서로 맞물린다.",
        ("knife","other"):"두 물건이 놓인 자리의 빈 부분이다. 그림의 다른 곳도 살펴볼 수 있다.",
        ("latch","outer"):"등의 바깥쪽 판과 걸쇠다. 실룩은 바깥 걸쇠를 칼로 밀어 닫았다고 말했다.",
        ("latch","inner"):"돌이 놓였던 안쪽 받침이다. 금속 파편이 발견된 자리가 여기다.",
        ("latch","other"):"현장의 위치를 옮겨 그린 종이다. 물건이 놓인 부분을 다시 살펴볼 수 있다.",
    }

    def r13_case_inspect_layout(kind,footer_y=572):
        if kind not in R13_CASE_INSPECT_ART:
            raise ValueError("지원하지 않는 실물 조사: "+str(kind))
        if kind=="knife":
            return dict(art=(146,226,1050,185),text=(148,444,1048,100))
        height=min(372,max(280,footer_y-200))
        return dict(art=(148,188,height*3//2,height),text=(760,222,420,270))

    def r13_case_inspect_target_rect(kind,target,layout,minimum=72):
        source=next((rect for key,rect in R13_CASE_INSPECT_TARGETS[kind] if key==target),None)
        if source is None:
            raise ValueError("없는 관찰 지점: "+str(target))
        cx,cy,cw,ch=R13_CASE_INSPECT_CROP[kind]
        ax,ay,aw,ah=layout["art"]
        sx,sy,sw,sh=source
        width=max(minimum,int(round(sw*float(aw)/cw)))
        height=max(minimum,int(round(sh*float(ah)/ch)))
        width=min(aw,width);height=min(ah,height)
        center_x=ax+(sx+sw*.5-cx)*float(aw)/cw
        center_y=ay+(sy+sh*.5-cy)*float(ah)/ch
        x=max(ax,min(ax+aw-width,int(round(center_x-width*.5))))
        y=max(ay,min(ay+ah-height,int(round(center_y-height*.5))))
        return (x,y,width,height)

    def r13_case_inspect_observation(kind,selected):
        return R13_CASE_INSPECT_TEXT.get((kind,selected),"그림에서 살펴볼 곳을 누르세요.")

    def r13_case_inspect_result(kind,selected):
        # 선택은 화면 안의 관찰일 뿐이다. 정답 적용·소모·획득은 여기서 하지 않는다.
        return "knife_fit" if kind=="knife" and selected=="fit" else None


screen r13_case_inspect(kind):
    modal True
    zorder 205
    default selected=None
    $ L=r13_case_inspect_layout(kind,r13_nb_footer_y())
    $ ax,ay,aw,ah=L["art"]
    $ tx,ty,tw,th=L["text"]
    $ crop=R13_CASE_INSPECT_CROP[kind]
    $ result=r13_case_inspect_result(kind,selected)
    # 그림 밖을 누른 동작으로 대사나 호출한 화면까지 닫지 않는다.
    key "dismiss" action NullAction()
    key "game_menu" action Return(None)
    use r13_notebook_shell("칼과 파편 조사" if kind=="knife" else "걸쇠와 파편의 위치",close_action=Return(None))
    text "그림에서 살펴볼 곳을 누르세요." xpos 148 ypos 148 xsize 1048 size r13_type("body") color r13_nb_muted() font R13_UI_FONT
    add Transform(Crop(crop,R13_CASE_INSPECT_ART[kind]),xysize=(aw,ah),nearest=True) pos (ax,ay)
    button:
        id "r13_case_inspect_picture"
        area (ax,ay,aw,ah) background None hover_background None
        action SetScreenVariable("selected","other") alt "그림 조사"
    for target,source_rect in R13_CASE_INSPECT_TARGETS[kind]:
        $ rect=r13_case_inspect_target_rect(kind,target,L)
        button:
            id ("r13_case_inspect_"+target)
            area rect background None hover_background None
            action SetScreenVariable("selected",target) alt "그림 조사"
    viewport:
        area (tx,ty,tw,th) mousewheel True draggable True scrollbars "vertical"
        text r13_case_inspect_observation(kind,selected) xsize (tw-20) size r13_type("body") color r13_nb_ink() font R13_UI_FONT
    fixed:
        xpos R13_NB_LEFT ypos r13_nb_footer_y() xysize (220,r13_control_height())
        use r13_control("닫기",None,Return(None),width=220,control_id="r13_case_inspect_close")
    fixed:
        xpos (R13_NB_RIGHT-280) ypos r13_nb_footer_y() xysize (280,r13_control_height())
        use r13_control("이 부분으로 확인" if result else "다른 곳 살펴보기",None,Return(result) if result else SetScreenVariable("selected",None),enabled=selected is not None,primary=bool(result),width=280,control_id="r13_case_inspect_confirm")
