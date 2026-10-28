# The crisis is a field confrontation, not a second formal trial.
screen r13_crisis():
    style_prefix "r13"
    modal True
    zorder 35
    default ready=False
    default preparations_open=False
    timer .15 action SetScreenVariable("ready",True)
    use r13_meeting_stage("F1")
    frame:
        area (24,18,900,66) padding (16,8) background R13PaperFrame()
        add R13AntiqueIcon("meeting_stone",size=30) xpos 0 ypos 8
        vbox:
            xpos 42
            text "제단 앞 회의 · 14일째" size r13_type("small") color "#795d40"
            text "연결을 멈춰야 한다" size r13_type("body") color "#493b30"
    $ preparations=r13_crisis_preparations()
    textbutton ("대피 준비 · %d / %d"%(sum(ok for name,ok in preparations),len(preparations))):
        style "r13_action_button" xpos 942 ypos 18 xsize 314 ysize 64 text_size r13_type("small")
        action ToggleScreenVariable("preparations_open") sensitive ready
    for index,key in enumerate(("F1","F2","F3","F4")):
        $ proved=key in room13["propositions"]
        $ open_claim=r13_debate_open(key)
        button:
            area (48+(index%2)*598,482+(index//2)*82,586,72) padding (14,9)
            background R13PaperPanel(proved) hover_background R13PaperPanel(True)
            action Return(key) sensitive ready and open_claim
            fixed:
                xsize 554 ysize 54
                text ("{s}"+R13_CLAIMS[key]["assertion"]+"{/s}" if proved else R13_CLAIMS[key]["assertion"]) size r13_type("small") color ("#82745d" if not open_claim else "#493b30") xsize (432 if not open_claim else 554) yalign .5
                if not open_claim:
                    text ("입증함" if proved else "이번 회의 정리됨" if r13_debate_closed(key) else "반론 자료 부족") xpos 446 xsize 108 size r13_type("small") color "#795d40" yalign .5
    hbox:
        xpos 48 ypos 650 spacing 16
        textbutton "수첩을 다시 본다" style "r13_action_button" xsize 312 ysize 60 text_size r13_type("body") action Show("r13_book") sensitive ready
        textbutton "모은 근거와 해 둔 준비로 움직인다" style "r13_action_button" xsize 620 ysize 60 text_size r13_type("body") action Return("finish") sensitive ready
    if preparations_open:
        frame:
            area (838,94,418,370) padding (20,16) background R13PaperFrame()
            vbox:
                spacing 12
                text "함께 움직일 준비" size r13_type("emphasis") color "#493b30"
                for name,prepared in preparations:
                    text (name+" · "+("모아 둠" if prepared else "마련하지 못함")) size r13_type("small") color ("#3d7058" if prepared else "#795d40")
                if room13["case_state"]=="occurred" and any(r13_debate_open(c) for c in r13_case_available()):
                    textbutton "13호 사건에서 남은 문제" style "r13_action_button" xsize 370 ysize 54 text_size r13_type("small") action Return("case") sensitive ready
                if r13_has("E29"):
                    textbutton "가족과 빠져나갈 길" style "r13_action_button" xsize 370 ysize 54 text_size r13_type("small") action Return("escape") sensitive ready

# 2026-10-27 자료 대조 패널 정리(소유자 "총체적 난국, 너무 안 이뻐"). 같은 기능, 배치만 다시 했다.
#   위계는 셋뿐이다 — 제목(주장) title · 본문(고른 자료) body · 보조(남은 기회·단계·안내) small.
#   위에서 아래로: 제목 + 남은 기회 칩 → 단계 칩 셋(첫 제출 성공 전까지) → 자료 카드 목록 → 안내 한 줄 → 버튼 넷.
#   카드는 내용만큼 자라고, 한 열로 안 들어가면 두 열로 나눈다 — 스크롤 상자는 두지 않는다(휴대폰 큰 글씨에서
#   자료 둘에도 스크롤이 생겼다). 동작·화면 id(r13_proof_steps, r13_proof_pick …)는 그대로다.
init 112 python:
    R13_PROOF_PANEL=(50,100,1180,570)
    R13_PROOF_PAD=(48,32,28,24)
    R13_PROOF_INNER_W=R13_PROOF_PANEL[2]-R13_PROOF_PAD[0]-R13_PROOF_PAD[2]   # 1104
    R13_PROOF_INNER_H=R13_PROOF_PANEL[3]-R13_PROOF_PAD[1]-R13_PROOF_PAD[3]   # 514
    R13_PROOF_GAP=10          # 머리·단계·목록·안내 사이
    R13_PROOF_CARD_GAP=8      # 카드 사이(세로·가로 같다)
    R13_PROOF_REMOVE_W=104    # 카드 안 「빼기」 폭
    # 2026-10-28 소유자 시안 B 승인: 빈 칸 셋을 미리 보이고, 판은 내용만큼만 높여 아래에 붙인다(위로 회의 장면이 보이게).
    R13_PROOF_EMPTY_SLOTS=3
    R13_PROOF_COMPACT=True

    def r13_proof_text_size(text,size,width=None,heavy=True):
        t=Text(text,font=(R13_UI_BOLD_FONT if heavy else R13_UI_FONT),size=size,xsize=width)
        w,h=renpy.render(t,width or 1280,720,0,0).get_size()
        return int(w),int(h)

    def r13_proof_card_height():
        # 썸네일 + 이름 두 줄(body)이 들어가는 높이. 휴대폰은 「빼기」 터치 영역 때문에 가장 높다.
        #   PC 보통 64(안 56, body 24 두 줄 55) · PC 크게 72(안 64, 28 두 줄 64) · 휴대폰 80(안 72, 30 두 줄 69).
        return 80 if r13_touch_ui() else (72 if persistent.room13_large_text else 64)

    def r13_proof_layout(claim,count,chances,steps_shown,help_text,note=None):
        """(열 수, 카드 높이, 제목 폭). 다섯 장까지 휴대폰 큰 글씨에서도 스크롤 없이 들어가게 남은 높이로 열을 정한다.
        휴대폰 크게: 514 − 머리 48 − 단계 42 − 안내 39 − 버튼 88 − 사이 40 = 257 ≥ 두 열 세 줄 3×80+2×8 = 256.
        note(2026-10-27 B02: 시작 비용 안내)는 안내 아래 small 한 줄이라, 있을 때만 그 높이와 사이 하나를 더 뺀다."""
        title_size=(r13_type("title") if R13_TYPE_V2 else r13_type("display"))
        small=(r13_type("small") if R13_TYPE_V2 else 22)
        chip_w=(r13_proof_text_size(chances,small)[0]+28) if chances else 0
        title_w=R13_PROOF_INNER_W-(chip_w+16 if chances else 0)
        header=max(r13_proof_text_size(R13_CLAIMS[claim]["assertion"],title_size,title_w)[1],small+12)
        steps=(small+14) if steps_shown else 0
        help_h=r13_proof_text_size(help_text,small,R13_PROOF_INNER_W,heavy=False)[1]
        note_h=(r13_proof_text_size(note,small,R13_PROOF_INNER_W,heavy=False)[1]+R13_PROOF_GAP) if note else 0
        gaps=R13_PROOF_GAP*(4 if steps_shown else 3)
        avail=R13_PROOF_INNER_H-header-steps-help_h-note_h-r13_control_height()-gaps
        card=r13_proof_card_height()
        n=max(1,count)
        cols=1 if n*card+R13_PROOF_CARD_GAP*(n-1)<=avail else 2
        return cols,card,title_w

    def r13_proof_shown(chosen,cols,card,avail):
        """(보일 카드, 숨긴 개수). 2026-10-28 꼼수 길 자동 주행: 가진 자료를 전부 고르면(20~70개) 카드가 패널 아래로
        넘쳐 버튼과 겹치고 틀 밖에 찍혔다. 들어가는 줄 수만 그리고, 넘치면 마지막 칸을 「그 밖에 N개」로 바꾼다."""
        chosen=list(chosen or ())
        rows=max(1,(avail+R13_PROOF_CARD_GAP)//(card+R13_PROOF_CARD_GAP))
        cap=rows*cols
        if len(chosen)<=cap:return chosen,0
        shown=chosen[:max(0,cap-1)]
        return shown,len(chosen)-len(shown)

    def r13_proof_avail(claim,chances,steps_shown,help_text,note=None):
        title_size=(r13_type("title") if R13_TYPE_V2 else r13_type("display"))
        small=(r13_type("small") if R13_TYPE_V2 else 22)
        chip_w=(r13_proof_text_size(chances,small)[0]+28) if chances else 0
        title_w=R13_PROOF_INNER_W-(chip_w+16 if chances else 0)
        header=max(r13_proof_text_size(R13_CLAIMS[claim]["assertion"],title_size,title_w)[1],small+12)
        steps=(small+14) if steps_shown else 0
        help_h=r13_proof_text_size(help_text,small,R13_PROOF_INNER_W,heavy=False)[1]
        note_h=(r13_proof_text_size(note,small,R13_PROOF_INNER_W,heavy=False)[1]+R13_PROOF_GAP) if note else 0
        gaps=R13_PROOF_GAP*(4 if steps_shown else 3)
        return R13_PROOF_INNER_H-header-steps-help_h-note_h-r13_control_height()-gaps

# 작은 꼬리표. 테두리만 있는 칩은 빨강 판 안에 크림 판을 넣어 그린다 — 새 재질을 만들지 않는다.
screen r13_proof_chip(label,filled=False):
    frame:
        padding (2,2) background Solid(r13_type_color("accent") if R13_TYPE_V2 else "#bc4134")
        frame:
            padding (12,3) background Solid((r13_type_color("accent") if R13_TYPE_V2 else "#bc4134") if filled else "#f5ecd9")
            text label font R13_UI_BOLD_FONT size (r13_type("small") if R13_TYPE_V2 else 22) color ((r13_type_color("inverse") if R13_TYPE_V2 else "#fff3df") if filled else (r13_type_color("accent") if R13_TYPE_V2 else "#bc4134"))

screen r13_crisis_proof(claim,heading="제단 앞 · 맞서야 할 주장",can_press=True,need_evidence=False,leave_label="다른 주장부터",chances=None,investigate=False):
    style_prefix "r13"
    modal True
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    $ chosen=list(room13["arguments"].get(claim,[]))
    $ steps_shown=bool(need_evidence and r13_proof_guide_active())
    $ help_text=(r13_proof_guide_help(len(chosen),chances) if steps_shown else r13_proof_edit_help(chances))
    $ start_note=(r13_v111_proof_start_note(claim) if chances else None)
    $ cols,card_h,title_w=r13_proof_layout(claim,len(chosen),chances,steps_shown,help_text,start_note)
    $ shown,hidden_n=r13_proof_shown(chosen,cols,card_h,r13_proof_avail(claim,chances,steps_shown,help_text,start_note))
    $ card_w=(R13_PROOF_INNER_W-R13_PROOF_CARD_GAP*(cols-1))//cols
    $ thumb=card_h-8
    $ name_w=card_w-20-thumb-14-((R13_PROOF_REMOVE_W+12) if need_evidence else 0)
    $ body_size=(r13_type("body") if R13_TYPE_V2 else r13_type("body"))
    # 2026-10-28 시안: 판을 내용만큼만 높여 아래에 붙인다(위로 회의 무대가 보이게). 남는 높이 = 쓸 수 있는 높이 − 카드 줄.
    $ used_rows=((len(shown)+(1 if hidden_n else 0)+cols-1)//cols) if chosen else 1
    $ spare=max(0,r13_proof_avail(claim,chances,steps_shown,help_text,start_note)-(used_rows*card_h+max(0,used_rows-1)*R13_PROOF_CARD_GAP)) if R13_PROOF_COMPACT else 0
    $ panel=(R13_PROOF_PANEL[0],R13_PROOF_PANEL[1]+spare,R13_PROOF_PANEL[2],R13_PROOF_PANEL[3]-spare)
    frame:
        area panel padding R13_PROOF_PAD background R13DiaryPanel()
        fixed:
            vbox:
                spacing R13_PROOF_GAP
                # 머리: 주장 제목 왼쪽, 같은 줄 오른쪽에 남은 기회 칩. 「기록 · 자료 대조」 글자는 뺐다 — 패널 자체가 그것이다.
                # fixed+yalign 으로 짜면 높이가 정해지지 않아 패널 전체로 늘어난다(첫 캡처에서 가운데가 비었다). hbox 로 둔다.
                hbox:
                    xsize R13_PROOF_INNER_W spacing 16
                    text R13_CLAIMS[claim]["assertion"] font R13_UI_BOLD_FONT size (r13_type("title") if R13_TYPE_V2 else r13_type("display")) color (r13_type_color("ink") if R13_TYPE_V2 else "#4b3420") xsize title_w yalign .5
                    if chances:
                        frame:
                            padding (0,0) background None yalign .5 xalign 1.0
                            use r13_proof_chip(chances)
                # 단계: 세 칩, 지금 단계만 빨강 채움. 첫 제출 성공 뒤에는 그대로 사라진다(r13_proof_guide_finish).
                if steps_shown:
                    hbox:
                        id "r13_proof_steps" spacing 8
                        for label,current in r13_proof_guide_chips(len(chosen)):
                            use r13_proof_chip(label,current)
                # 고른 자료: 빈 상자가 아니라 카드 목록. 썸네일은 기록 화면과 같은 그림(r13_evidence_picture).
                if chosen:
                    vbox:
                        spacing R13_PROOF_CARD_GAP
                        for row in range(0,len(shown)+(1 if hidden_n else 0),cols):
                            hbox:
                                spacing R13_PROOF_CARD_GAP
                                for key in (shown+(["__more__"] if hidden_n else []))[row:row+cols]:
                                  if key=="__more__":
                                    # 넘친 자료는 한 칸으로 묶는다. 하나씩 빼는 것은 「자료 고르기」에서 같은 자료를 다시 누르면 된다.
                                    frame:
                                        id "r13_proof_more" xysize (card_w,card_h) padding (16,4) background r13_sticker_button()
                                        text ("그 밖에 %d개 · 「자료 고르기」에서 빼거나 더합니다"%hidden_n) yalign .5 xsize card_w-32 font R13_UI_BOLD_FONT size (r13_type("small") if R13_TYPE_V2 else 22) color (r13_type_color("muted") if R13_TYPE_V2 else "#6b5641")
                                  else:
                                    frame:
                                        xysize (card_w,card_h) padding (10,4) background r13_sticker_button()
                                        add r13_evidence_picture(key,thumb) xpos 0 yalign .5
                                        text r13_ev_two_lines(ROOM13["evidence"][key]["name"],name_w,body_size,2) xpos (thumb+14) yalign .5 xsize name_w font R13_UI_BOLD_FONT size (r13_type("body") if R13_TYPE_V2 else r13_type("body")) color (r13_type_color("ink") if R13_TYPE_V2 else "#4b3420") line_spacing -1
                                        if need_evidence:
                                            fixed:
                                                xalign 1.0 yalign .5 xysize (R13_PROOF_REMOVE_W,card_h-12)
                                                use r13_control("빼기",None,Return(("remove",key)),enabled=ready,width=R13_PROOF_REMOVE_W,height=card_h-12,label_size=(r13_type("small") if R13_TYPE_V2 else 22))
                elif R13_PROOF_EMPTY_SLOTS:
                    # 2026-10-28 소유자 「폰트나 공간이 안 예쁘다, 자료 고르기 쪽 디자인 예쁘게」: 빈 판 가운데 한 줄이 떠 있었다.
                    # 자료가 놓일 자리를 빈 칸(점선 테두리)으로 미리 보여 준다. 칸 크기는 담긴 카드와 같다.
                    hbox:
                        spacing R13_PROOF_CARD_GAP
                        for i in range(R13_PROOF_EMPTY_SLOTS):
                            # 빈 칸은 가벼운 선과 옅은 바탕만(시안의 회색 판은 탁해 보였다).
                            $ slot_w=(R13_PROOF_INNER_W-R13_PROOF_CARD_GAP*(R13_PROOF_EMPTY_SLOTS-1))//R13_PROOF_EMPTY_SLOTS
                            fixed:
                                xysize (slot_w,card_h)
                                add Solid("#f3e6c9") xysize (slot_w,card_h)
                                for bx,by,bw,bh in ((0,0,slot_w,2),(0,card_h-2,slot_w,2),(0,0,2,card_h),(slot_w-2,0,2,card_h)):
                                    add Solid("#c9ae7e") xpos bx ypos by xysize (bw,bh)
                                text ("자료를 여기에 담는다" if i==0 else "빈 칸") align (.5,.5) size (r13_type("small")) color (r13_type_color("disabled") if i else r13_type_color("muted")) font R13_UI_BOLD_FONT
                else:
                    fixed:
                        xysize (R13_PROOF_INNER_W,card_h)
                        text "「자료 고르기」로 담습니다." align (.5,.5) size (r13_type("body") if R13_TYPE_V2 else r13_type("body")) color (r13_type_color("muted") if R13_TYPE_V2 else "#6b5641")
                # 안내 한 줄.
                text help_text size (r13_type("small") if R13_TYPE_V2 else 22) color (r13_type_color("muted") if R13_TYPE_V2 else "#6b5641") xsize R13_PROOF_INNER_W
                # 2026-10-27 B02: 시작 비용이 적용된 회의(5일 밤이, bami_cold4)에서만 까닭 한 줄. 조건 없는 판은 아무것도 없다.
                if start_note:
                    text start_note size (r13_type("small") if R13_TYPE_V2 else 22) color (r13_type_color("muted") if R13_TYPE_V2 else "#6b5641") xsize R13_PROOF_INNER_W
            # 버튼 넷은 공통 부품 규격 한 줄. 주 버튼은 「선택한 근거 제출」 하나.
            hbox:
                yalign 1.0 spacing R13_CONTROL["gap"]
                use r13_control("자료 고르기",None,Return("present"),enabled=ready,width=264,control_id="r13_proof_pick")
                use r13_control("되묻는다",None,Return("press"),enabled=(ready and can_press),width=264,control_id="r13_proof_hint")
                use r13_control("선택한 근거 제출",None,Return("argue"),enabled=(ready and (bool(chosen) or not need_evidence)),primary=True,width=264,control_id="r13_proof_submit")
                # 2026-10-27 UX 인계서 D04: 조사 복귀가 열린 쟁점은 넷째 칸이 「조사 계속」. 기회를 쓰지 않고 현장 라벨로 돌아간다.
                if investigate:
                    use r13_control("조사 계속",None,Return("investigate"),enabled=ready,width=264,control_id="r13_proof_back")
                else:
                    use r13_control(leave_label,None,Return("leave"),enabled=ready,width=264,control_id="r13_proof_back")

screen r13_rescue_notes():
    style_prefix "r13"
    modal True
    zorder 60
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    add Solid("#172a2aa6")
    frame:
        area (165,145,950,475) padding (30,26)
        vbox:
            spacing 20
            text "아이에게 닿을 방법" size r13_type("display") color "#765426"
            if room13["scout_revision"]!=room13["convoy_revision"]:
                text "지금 따르고 있는, 끌고 가라는 명령과 지킴 순서를 확인하지 못했다." size r13_type("emphasis") xsize 875
            for route in r13_rescue_routes():
                text {"order":"너울과 맞춰 본 명령으로 옮기는 것을 멈출 수 있다.","laundry":"누비와, 물건이 들어오며 지키는 사람이 바뀌는 때에 맞춰 아이를 넘겨받기로 했다.","maintenance":"부리와 점검문을 확인해 두었다."}[route] size r13_type("emphasis") xsize 875
            if r13_has("operators_ready") and r13_has("patient_transport"):
                text "장치를 다룰 사람들과 나를 사람들이 있다. 엄마와 함께 사람 쪽 연결을 막을 수 있다." size r13_type("emphasis") xsize 875
            elif not r13_rescue_routes():
                text "함께 연결을 막고 아이를 옮길 준비도 갖추지 못했다. 혼자 끌고 가는 걸 막으면 경비를 넘어서기 어렵다." size r13_type("emphasis") xsize 875
            textbutton "돌아간다" action Return(False) sensitive ready text_size r13_type("emphasis")

screen r13_ending_screen(key):
    style_prefix "r13"
    modal True
    zorder 70
    default ready=False
    timer .5 action SetScreenVariable("ready",True)
    add Solid("#111b2266")
    text "이번 여정의 끝" xpos 76 ypos 84 size r13_type("body") color "#dfbd7e"
    text R13_ENDINGS[key]["title"] xpos 72 ypos 126 xsize 568 size r13_type("display") color "#fff0d0" outlines [(2,"#1d262b",0,1)]
    text r13_ending_story_frame(key,3)["caption"] xpos 76 ypos 218 xsize 540 size r13_type("emphasis") color "#fff0d0" line_spacing 7 outlines [(1,"#1d262b",0,1)]
    textbutton "후일담 다시 보기":
        style "r13_action_button" area (76,584,340,62) text_size r13_type("emphasis") action Return("replay") sensitive ready
    textbutton "이름 판":
        style "r13_action_button" area (430,584,200,62) text_size r13_type("emphasis") action Return("board") sensitive ready
    frame:
        area (680,54,548,612) padding (26,24) background R13PaperFrame()
        vbox:
            spacing 12
            text "남은 기록" size r13_type("title") color "#765426"
            viewport:
                xsize 496 ysize 230 draggable True mousewheel True scrollbars "vertical" vscrollbar_unscrollable "hide"
                vbox:
                    spacing 12
                    for line in r13_ending_notes():
                        text line size r13_type("body") xsize 464 color "#493b30"
            text "새 여정은 첫날부터 시작해요. 이번 기록과 물건은 이어지지 않아요." size r13_type("small") xsize 490 color "#795d40"
            textbutton "새 여정 시작" style "r13_action_button" xsize 490 ysize 54 text_size r13_type("emphasis") action Return("restart") sensitive ready
            hbox:
                spacing 12
                textbutton "진행 불러오기" style "r13_action_button" xsize 239 ysize 52 text_size r13_type("body") action ShowMenu("load") sensitive ready
                textbutton "메인화면으로" style "r13_action_button" xsize 239 ysize 52 text_size r13_type("body") action Confirm("메인화면으로 돌아가시겠습니까?",MainMenu(confirm=False)) sensitive ready

screen r13_nearby():
    style_prefix "r13"
    modal True
    zorder 45
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    add Solid("#172a2aa6")
    frame:
        area (220,150,840,515) padding (24,20)
        vbox:
            spacing 15
            text "주변 사람들" size r13_type("display") color "#765426"
            viewport:
                xsize 780 ysize 350 draggable True mousewheel True scrollbars "vertical"
                vbox:
                    spacing 10
                    for person in r13_people():
                        button:
                            xsize 730 ysize 85 padding (10,8)
                            background R13PaperPanel() hover_background R13PaperPanel()
                            action Return(person) sensitive ready
                            hbox:
                                spacing 20
                                add Transform(r13_art(person,"avatar_neutral"),size=(66,66),fit="contain")
                                text R13_NAMES[person] size r13_type("emphasis") yalign .5
            textbutton "돌아가기" action Return(False) sensitive ready
