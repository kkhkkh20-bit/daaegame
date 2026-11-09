# Feedback never awards evidence or advances narrative time.
init 69 python:
    class R13FieldPointerGate(renpy.Displayable):
        def render(self,width,height,st,at):
            return renpy.Render(0,0)
        def event(self,ev,x,y,st):
            # 터치도 새 지점의 down/motion에서 먼저 열어 같은 탭의 up이
            # 원래 물건 버튼으로 간다. 이 감시자는 클릭을 소비하지 않는다.
            if hasattr(ev,"pos"):r13_wake_field_pointer()
            return None

    class R13ObjectHover(renpy.Displayable):
        # 조사할 물건의 모서리만 짧게 표시한다. 이름 팝업·새 클릭 단계는 없다.
        def __init__(self,size,**kwargs):
            super(R13ObjectHover,self).__init__(**kwargs)
            self.size=tuple(max(1,int(value)) for value in size)
        def render(self,width,height,st,at):
            w,h=self.size
            out=renpy.Render(w,h)
            c=out.canvas()
            p=2;n=max(1,min(8,(w-4)//3,(h-4)//3))
            for x,y,dx,dy in ((p,p,1,1),(w-p-1,p,-1,1),(p,h-p-1,1,-1),(w-p-1,h-p-1,-1,-1)):
                c.lines("#6c4e36aa",False,[(x,y+dy*n),(x,y),(x+dx*n,y)],1)
            return out

    def r13_evidence_notice_keys(current,new_keys):
        # 한 번의 화면 안에서 이미 보여 준 자료도 다시 줄 세우지 않는다.
        result=list(dict.fromkeys(current or []))
        for key in new_keys or []:
            if key not in result:result.append(key)
        return result

    def r13_evidence_notice_visible():
        blocked=("main_menu","pause_menu","save","load","confirm","r13_latch_diagram132","r13_piko_scene",
            "r13_pw_picture","r13_map","r13_records","r13_learning_notes","r13_record_compare",
            "r13_calendar","r13_work_board","r13_proof_workspace")
        # 가족 그림은 내용 자체가 단서다. 큰 첫 발견 컷을 읽는 동안 알림과 만료 시계를
        # 함께 기다리게 하고, 컷을 접은 뒤 원래 자리에서 획득 사실을 알려 준다.
        family_focus=getattr(store,"r13_ep_cut_current",None) in ("focus:E06","focus:D01_FAMILY_DRAWING") and renpy.showing("r13_ep_cut")
        return not family_focus and not getattr(store,"r13_nw_comparison",None) and not any(renpy.get_screen(name) for name in blocked)

    def r13_evidence_acquired(keys):
        if not keys:return
        current=renpy.get_screen("r13_evidence_found")
        # show 직후에는 화면 매개변수가 아직 scope에 바인딩되지 않아 _kwargs에만 있다.
        existing=list(current.scope.get("notice_keys",current.scope.get("keys",current.scope.get("_kwargs",{}).get("keys",[])))) if current else []
        queued=r13_evidence_notice_keys(existing,keys)
        if current and queued==existing:return
        if current:
            # 기존 화면의 default 목록만 늘린다. 다시 show하면 현재 index가 0으로 돌아간다.
            renpy.set_screen_variable("notice_keys",queued,screen="r13_evidence_found")
            renpy.restart_interaction()
        else:
            renpy.show_screen("r13_evidence_found",keys=queued,conversation=r13_feedback_in_conversation())

    def r13_click_feedback(key):
        spec=ROOM13["objects"].get(store.room13["location"],{}).get(key)
        if not spec:return
        # 메모처럼 터치 범위를 넓힌 물건도 실제로 누른 지점에서 반응한다.
        # 키보드로 고른 경우에만 물건 가운데를 쓴다.
        target_rect=globals().get("r13_object_target_rect",lambda key,spec:tuple(spec["rect"]))
        x,y,w,h=target_rect(key,spec)
        wx,wy=r13_screen_to_world(renpy.get_mouse_pos())
        target=(wx,wy) if x<=wx<=x+w and y<=wy<=y+h else (x+w/2.0,y+h/2.0)
        point=r13_world_to_screen(target)
        renpy.show_screen("r13_click_glint", point=point)

    class R13ClickGlint(renpy.Displayable):
        def render(self,width,height,st,at):
            out=renpy.Render(32,32)
            c=out.canvas()
            c.circle("#fff4df99",(16,16),8,1)
            return out

transform r13_click_pulse:
    alpha .7 zoom .9
    linear .2 alpha 0.0 zoom 1.0

transform r13_evidence_reveal:
    alpha 0.0 xoffset -14
    # 0.18.47 storybook tone: a slower, softer arrival and no hop.
    easeout .35 alpha 1.0 xoffset 0

screen r13_click_glint(point):
    zorder 90
    add R13ClickGlint() xpos point[0] ypos point[1] xanchor .5 yanchor .5 at r13_click_pulse
    timer .25 action Hide("r13_click_glint")

# 0.18.33 (owner): top right, clear of the person and the questions.
# 0.18.46 (owner): only the icon and the record's name, the frame hugging them, a little larger
# and moved in from the edge toward the person, as if held out to them. No caption.
define R13_EVIDENCE_CARD_CENTER = (1010, 112)
define R13_EVIDENCE_ICON_SIZE = 104
define R13_EVIDENCE_NAME_WIDTH = 190
define R13_EVIDENCE_NOTICE_SIZE = (360, 136)
define R13_EVIDENCE_HELD_SIZE = (300, 100)
define R13_EVIDENCE_NOTICE_TOP = 104
define R13_EVIDENCE_CARD_PAD = 10

screen r13_evidence_card(key,caption="",conversation=False,notice=False,compact=False):
    # 2026-10-27: 왼쪽 위 획득 알림이 현장 상단 지도·기록 버튼(y 40~75)을 덮었다. 그 아래로 내린다.
    # 2026-10-27: 알림 카드는 오른쪽 위(날짜판 아래). 왼쪽 위에 두니 자료 대조 화면의 발언 글과 겹쳤다.
    style_prefix "r13"
    if compact:
        # 2026-10-27: 자료 대조 패널(50,100)-(1230,670)이 떠 있는 동안은 왼쪽 위 카드가 주장 제목을 덮는다.
        # 패널 아래 띠(670~720)의 오른쪽 끝에 한 줄짜리로 내린다 — 그림 36 + 이름, 높이 44 로 패널에 닿지 않는다.
        frame:
            xanchor 1.0 xpos 1230 yanchor 1.0 ypos 718 padding (10,4,12,4)
            background r13_ev_pixel_panel()
            at r13_evidence_reveal
            hbox:
                spacing 10
                add Transform(r13_record_icon(key),size=(36,36),fit="contain",nearest=True) yalign .5
                text r13_catalog_title(key) size r13_type("small") color "#493b30" yalign .5 xmaximum 360
    else:
        # 2026-10-28 분기 주행 캡처: 알림 카드가 이름 길이마다 폭이 달랐고(이름에 맞춰 틀이 줄었다), 자리도 화면마다
        # 셋으로 갈렸다(대화 1010·조사 1100·선택 1180). 선택창 목록(오른쪽 600~1236, y 240~)과 조사 화면 오른쪽 화살표를 덮었다.
        # 증거 칸(R13_EV_CUT_BOX)과 같은 납품 종이 틀의 고정 크기 카드로, 날짜판 아래 한 자리에 둔다.
        # 증거 칸이 떠 있으면 그 아래로 내린다(둘이 겹치지 않게).
        $ card_w,card_h=R13_EVIDENCE_NOTICE_SIZE if notice else R13_EVIDENCE_HELD_SIZE
        $ card_y=(R13_EV_CUT_BOX[1]+R13_EV_CUT_BOX[2]+8) if renpy.showing("r13_ep_cut") else R13_EVIDENCE_NOTICE_TOP
        fixed:
            xanchor 1.0 xpos 1252 ypos card_y xysize (card_w,card_h)
            at r13_evidence_reveal
            add r13_ev_pixel_panel(card_w,card_h)
            hbox:
                xpos 20 ypos 20 spacing 14 ysize card_h-40
                add Transform(r13_record_icon(key),xysize=(card_h-40,card_h-40),fit="contain",nearest=True) yalign .5
                if notice:
                    vbox:
                        spacing 2 yalign .5
                        text "증거 획득" size r13_type("small") color "#8a3d2b" font R13_UI_BOLD_FONT
                        text r13_catalog_title(key) size r13_type("small") color "#493b30" xmaximum card_w-card_h-20 layout "subtitle"
                else:
                    text r13_catalog_title(key) size r13_type("small") color "#493b30" yalign .5 xmaximum card_w-card_h-20 layout "subtitle"

screen r13_evidence_found(keys,conversation=False):
    # 0.18.48: above the desk close-up (90) and the item bag (95), which reopen right after a
    # find and used to cover the card. It has no buttons, so it never blocks input.
    zorder 98
    default item_index=0
    default notice_keys=keys
    # Navigation and full record panes own their surface. Desk/item finds still show above the close-up.
    # 2026-10-27: 자료 대조 통합 화면 위에서도 띄우지 않는다(발언·상세 글과 겹쳤다).
    if r13_evidence_notice_visible():
        if renpy.get_screen("r13_crisis_proof") or renpy.get_screen("r13_topics"):
            # 자료 대조 패널 위에서는 제목과 겹치지 않게 패널 아래로 보낸다(위 compact).
            # 2026-10-27 검수(p08c 캡처): 질문 수첩(488~1180, 줄은 y 228 부터) 위에서도 오른쪽 위 카드(1012~1190, 190~)가
            # 첫 질문의 끝 글자를 덮어 「묻는ㄷ」로 보였다. 질문 목록이 떠 있으면 같은 한 줄 카드로 수첩 아래 띠에 둔다.
            use r13_evidence_card(notice_keys[item_index],conversation=conversation,notice=True,compact=True)
        else:
            if r13_fx_active():
                add R13_STORYBOOK.get("card_glow", Null()) xpos (1252-R13_EVIDENCE_NOTICE_SIZE[0]//2) ypos (R13_EVIDENCE_NOTICE_TOP+R13_EVIDENCE_NOTICE_SIZE[1]//2) anchor (.5,.5) at r13_card_glow
            use r13_evidence_card(notice_keys[item_index],conversation=conversation,notice=True)
        # 카드를 넘길 때만 새 시계를 만든다. 같은 timer를 재사용하면 두 번째 카드에서 멈춘다.
        # 현재 카드에 다음 자료가 추가되어도 같은 key·timer라 보던 순서와 시간은 이어진다.
        for notice_index index notice_index in [item_index]:
            timer 3.2 action (SetScreenVariable("item_index",notice_index+1) if notice_index+1<len(notice_keys) else Hide("r13_evidence_found"))

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
