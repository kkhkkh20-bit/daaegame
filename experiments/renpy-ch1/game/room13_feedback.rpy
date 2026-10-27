# Feedback never awards evidence or advances narrative time.
init 69 python:
    def r13_evidence_acquired(keys):
        if keys:
            renpy.hide_screen("r13_evidence_found")
            renpy.show_screen("r13_evidence_found", keys=list(keys),conversation=r13_feedback_in_conversation())

    def r13_click_feedback(key):
        spec=ROOM13["objects"].get(store.room13["location"],{}).get(key)
        if not spec:return
        x,y,w,h=spec["rect"]
        wx,wy=r13_screen_to_world(renpy.get_mouse_pos())
        target=(wx,wy) if x<=wx<=x+w and y<=wy<=y+h else (x+w/2.0,y+h/2.0)
        point=r13_world_to_screen(target)
        renpy.show_screen("r13_click_glint", point=point)

    class R13ClickGlint(renpy.Displayable):
        def render(self,width,height,st,at):
            out=renpy.Render(60,60)
            c=out.canvas()
            c.lines("#f5dfa0",True,[(30,4),(56,30),(30,56),(4,30)],2)
            c.lines("#fff9de",False,[(18,30),(27,39),(42,22)],3)
            return out

transform r13_click_pulse:
    alpha 1.0 zoom .55
    easeout .2 zoom 1.05
    linear .4 alpha 0.0 zoom 1.3

transform r13_evidence_reveal:
    alpha 0.0 xoffset -14
    # 0.18.47 storybook tone: a slower, softer arrival and no hop.
    easeout .35 alpha 1.0 xoffset 0

screen r13_click_glint(point):
    zorder 90
    add R13ClickGlint() xpos point[0] ypos point[1] xanchor .5 yanchor .5 at r13_click_pulse
    timer .65 action Hide("r13_click_glint")

# 0.18.33 (owner): top right, clear of the person and the questions.
# 0.18.46 (owner): only the icon and the record's name, the frame hugging them, a little larger
# and moved in from the edge toward the person, as if held out to them. No caption.
define R13_EVIDENCE_CARD_CENTER = (1010, 112)
define R13_EVIDENCE_ICON_SIZE = 104
define R13_EVIDENCE_NAME_WIDTH = 190
define R13_EVIDENCE_CARD_PAD = 10

screen r13_evidence_card(key,caption="",conversation=False,notice=False,compact=False):
    # 2026-10-27: 왼쪽 위 획득 알림이 현장 상단 지도·기록 버튼(y 40~75)을 덮었다. 그 아래로 내린다.
    # 2026-10-27: 알림 카드는 오른쪽 위(날짜판 아래). 왼쪽 위에 두니 자료 대조 화면의 발언 글과 겹쳤다.
    # 2026-10-27 14일 자동 플레이 2일(등 살펴보기 선택창): 선택창 틀(195~1085)의 오른쪽 가장자리를 카드(1030~1170)가 덮었다.
    # 선택창이 떠 있으면 틀 바깥(1110~1250)으로 비켜 둔다.
    $ card_center=((1180,190) if renpy.get_screen("choice") else (1100,190)) if notice else R13_EVIDENCE_CARD_CENTER
    style_prefix "r13"
    if compact:
        # 2026-10-27: 자료 대조 패널(50,100)-(1230,670)이 떠 있는 동안은 왼쪽 위 카드가 주장 제목을 덮는다.
        # 패널 아래 띠(670~720)의 오른쪽 끝에 한 줄짜리로 내린다 — 그림 36 + 이름, 높이 44 로 패널에 닿지 않는다.
        frame:
            xanchor 1.0 xpos 1230 yanchor 1.0 ypos 718 padding (10,4,12,4)
            background R13ActionPanel()
            at r13_evidence_reveal
            hbox:
                spacing 10
                add Transform(r13_record_icon(key),size=(36,36),fit="contain",nearest=True) yalign .5
                text r13_catalog_title(key) size r13_type("small") color "#fff4df" yalign .5 xmaximum 360
    else:
        frame:
            xanchor .5 xpos card_center[0] ypos card_center[1] padding (R13_EVIDENCE_CARD_PAD,8,R13_EVIDENCE_CARD_PAD,8)
            background R13ActionPanel()
            at r13_evidence_reveal
            vbox:
                spacing 3
                add Transform(r13_record_icon(key),size=(R13_EVIDENCE_ICON_SIZE,R13_EVIDENCE_ICON_SIZE),fit="contain",nearest=True) xalign .5
                text r13_catalog_title(key) size r13_type("small") color "#fff4df" xalign .5 text_align .5 xmaximum R13_EVIDENCE_NAME_WIDTH

screen r13_evidence_found(keys,conversation=False):
    # 0.18.48: above the desk close-up (90) and the item bag (95), which reopen right after a
    # find and used to cover the card. It has no buttons, so it never blocks input.
    zorder 98
    default item_index=0
    # Navigation and full record panes own their surface. Desk/item finds still show above the close-up.
    # 2026-10-27: 자료 대조 통합 화면 위에서도 띄우지 않는다(발언·상세 글과 겹쳤다).
    if not any(renpy.get_screen(name) for name in ("r13_map","r13_records","r13_learning_notes","r13_record_compare","r13_calendar","r13_work_board","r13_proof_workspace")):
        if renpy.get_screen("r13_crisis_proof") or renpy.get_screen("r13_topics"):
            # 자료 대조 패널 위에서는 제목과 겹치지 않게 패널 아래로 보낸다(위 compact).
            # 2026-10-27 검수(p08c 캡처): 질문 수첩(488~1180, 줄은 y 228 부터) 위에서도 오른쪽 위 카드(1012~1190, 190~)가
            # 첫 질문의 끝 글자를 덮어 「묻는ㄷ」로 보였다. 질문 목록이 떠 있으면 같은 한 줄 카드로 수첩 아래 띠에 둔다.
            use r13_evidence_card(keys[item_index],conversation=conversation,notice=True,compact=True)
        else:
            if r13_fx_active():
                add R13_STORYBOOK.get("card_glow", Null()) xpos 120 ypos (92+8+R13_EVIDENCE_ICON_SIZE//2+20) anchor (.5,.5) at r13_card_glow
            use r13_evidence_card(keys[item_index],conversation=conversation,notice=True)
    if item_index+1<len(keys):
        timer 2.4 action SetScreenVariable("item_index",item_index+1)
    else:
        timer 2.4 action Hide("r13_evidence_found")

# A quiet acknowledgement for empty taps; no observation, journal or clock writes.
init 69 python:
    def r13_empty_tap_feedback():
        renpy.show_screen("r13_empty_tap",point=renpy.get_mouse_pos())

    class R13EmptyTap(renpy.Displayable):
        def render(self,width,height,st,at):
            r=renpy.Render(32,32)
            r.canvas().circle("#fff4df99",(16,16),10,2)
            return r

transform r13_empty_tap_fade:
    alpha .7
    linear .35 alpha 0.0

screen r13_empty_tap(point):
    zorder 90
    add R13EmptyTap() pos point anchor (.5,.5) at r13_empty_tap_fade
    timer .4 action Hide("r13_empty_tap")
