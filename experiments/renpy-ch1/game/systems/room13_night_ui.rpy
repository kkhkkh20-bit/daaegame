# B notebook dialogue (2026-10-24 owner approval). Historical function names
# preserve geometry and save compatibility; controls retain their existing actions.
init 150 python:
    R13_NIGHT_UI="assets/ui-night/"
    R13_NIGHT_TEXT_COLOR="#4b3420"
    # 대사판 종이(b_panel_dialogue) 는 screens.rpy 에서 아래끝 714 에 맞춰 늘인다. 그 종이의 아래 테두리(남색 선)는
    # 그림 아래끝에서 16px 안쪽까지 그려진다(crop 128 줄 중 112~125). 조작 리본은 그 선보다 위에서 끝나야 한다.
    # 2026-10-28 소유자 「건너뛰기·더보기를 우측 하단에 놓고, 대사창 박스 하단을 더 줄여 두 줄 들어가게」:
    # 스티커가 종이 아래 테두리에 걸쳐도 화면(720) 안에 들어오도록 종이 아래끝을 694 로 올린다.
    R13_NIGHT_PAPER_BOTTOM=690
    R13_NIGHT_PAPER_EDGE=16
    R13_NIGHT_CONTROL_GAP=10         # 리본 아래끝과 종이 테두리 선 사이
    # 2026-10-28 소유자 「선택지 대화창이랑 일반 대화창 높이가 너무 다르다, 둘의 중간으로 통일」(178) 뒤에
    # 「아빠라는 이름과 대사가 너무 붙어 있다, 위로 붙어 있다」「높이 그대로에 아래를 줄여서 올려」
    # 「건너뛰기·더보기는 스티커 에셋이라 대화창 안에 들어갈 필요는 없다」:
    #   - 종이 높이는 그대로(PC 178). 대사는 이름 리본 아래부터 종이 아래 테두리까지의 가운데에 둔다.
    #   - 이름 리본은 종이 윗변 왼쪽에, 건너뛰기·더보기 스티커는 종이 아래 테두리 오른쪽에 걸친다(종이 안 빈칸 없음).
    #   - 세 줄 이상이면 종이가 위로 자란다(리본·스티커가 같이 올라간다).
    R13_SAY_RIBBON_IN=14      # 윗변에 걸친 이름 리본이 종이 안으로 들어오는 깊이(리본 가운데 = 윗변 - 12)
    R13_SAY_RIBBON_LIFT=12
    R13_SAY_MARGIN=10         # 리본 아래 여백 = 종이 아래 테두리 위 여백
    _R13_SAY_BLOCK={}
    def r13_night_say_block(lines=2,size=None):
        # 2026-10-28 실측: 한 줄 높이를 글자 크기(30)로 잡아 두 줄 칸이 64 로 계산됐는데, 실제로 그린 두 줄은 88 이었다
        # (Pretendard 줄 높이 + 줄 간격 4). 그래서 대사가 종이 아래로 치우쳤다. 실제로 그려서 잰다.
        size=size or r13_night_say_size()
        key=(size,lines)
        if key not in _R13_SAY_BLOCK:
            t=Text("\n".join(["가나다"]*lines),font=R13_UI_BOLD_FONT,size=size,line_spacing=4)
            _R13_SAY_BLOCK[key]=int(renpy.render(t,1280,720,0,0).get_size()[1])
        return _R13_SAY_BLOCK[key]
    def r13_night_panel_top(what=None,size=None):
        size=size or r13_night_say_size()
        lines=r13_night_say_lines(what) if what is not None else 2
        block=r13_night_say_block(max(2,lines),size)
        return R13_NIGHT_PAPER_BOTTOM-(R13_NIGHT_PAPER_EDGE+R13_SAY_RIBBON_IN+block+2*R13_SAY_MARGIN)
    def r13_night_control_y():
        # 스티커 가운데 = 종이 아래 테두리 선(아래끝 - 테두리 두께의 절반). 오른쪽 아래에 걸친다.
        return R13_NIGHT_PAPER_BOTTOM-R13_NIGHT_PAPER_EDGE//2
    R13_NIGHT_CONTROL_Y=R13_NIGHT_PAPER_BOTTOM-R13_NIGHT_PAPER_EDGE//2   # 더보기 판이 참조
    R13_NIGHT_TEXT_BOTTOM=R13_NIGHT_PAPER_BOTTOM-R13_NIGHT_PAPER_EDGE-R13_SAY_MARGIN

    def r13_night_say_size():
        # The mockup's line is a step larger than the boxed window's (same size setting).
        # 2026-10-27 타이포 시안: 켜지면 display 단계. 줄 수·위치 계산이 모두 이 함수를 쓰므로 여기서 바꾼다.
        return r13_type("display")

    def r13_night_say_lines(what):
        if not isinstance(what,str):return 1
        size=r13_night_say_size()
        packet=getattr(store,"r13_packet",None)
        face=None if getattr(store,"r13_thought_active",False) or "r13_visitor" in renpy.get_showing_tags() else r13_bdialogue_face(packet[0] if packet else None,r13_fullbody_emotion(getattr(store,"r13_directed_pose","neutral")))
        return max(1,_r13_say_lines(what,size,988 if face else 1090))

    def r13_night_say_top(what=None):
        """대사 첫 줄 윗선. 두 줄 칸의 첫 줄 자리에서 시작한다.
        2026-10-28 소유자 「한 줄일 때 가운데 정렬이 아니라 위 칸에 써야 할 듯」: 한 줄도 첫 줄 자리에 둔다. 대사가 바뀔 때
        첫 글자 자리가 줄 수에 따라 오르내리면 눈이 따라가야 한다(역전재판·페르소나·Ren'Py 기본 대사창 모두 첫 줄 고정)."""
        return r13_night_panel_top(what)+R13_SAY_RIBBON_IN+R13_SAY_MARGIN

    def r13_night_text_color():
        # B dialogue uses paper-role colours on the cream notebook.
        if getattr(store,"r13_thought_active",False):return r13_role_color("thought","paper")
        packet=getattr(store,"r13_packet",None)
        if packet and packet[0] is None:return r13_role_color("narration","paper")
        # 2026-10-27 타이포 시안: 말은 ink 토큰(값은 지금과 같다). 생각·서술의 역할색은 그대로 둔다.
        return r13_type_color("ink")

    def r13_night_shade_alpha():
        # The approved "대사창 진하기" setting still decides how dark the shade gets.
        return {"99":.88,"d4":.985,"f5":1.0}.get(persistent.room13_window_alpha or "d4",1.0)

    def r13_night_shade_top(what=None):
        top=r13_night_say_top(what)-150
        if (persistent.room13_window_alpha or "d4") in ("f0","f5","fa","ff"):top-=60
        return max(240,top)

    def r13_night_ribbon():
        return Frame(r13_asset_path("file:"+(R13_NIGHT_UI+"name_ribbon.png")),44,0,44,0)

style r13_night_link_text is text:
    font r13_ui_font() size r13_type("small") color "#4b3420" hover_color "#b03730" insensitive_color "#8f8778"
    outlines []

screen r13_night_link(caption,glyph,icon,command,enabled=True,link_id=None):
    $ on_paper=not r13_black_card
    $ label_width=(208 if r13_touch_ui() else 184) if caption in ("건너뛰기","더보기") else (370 if r13_touch_ui() else 300)
    button:
        id (link_id or ("r13_night_"+caption))
        xsize label_width ysize (88 if r13_touch_ui() else 56) yalign .5 padding (0,0)
        background None hover_background None
        action command sensitive enabled alt caption
        fixed:
            xysize (label_width,88 if r13_touch_ui() else 56)
            if on_paper:
                add Transform(Frame(Crop((16,12,168,32),r13_asset_path("file:assets/ui-b-dialogue/b_ribbon_name.png")),16,6,32,6),xysize=(label_width,52 if r13_touch_ui() else 44),alpha=1.0 if enabled else .55) align (.5,.5)
            # 2026-10-27 타이포 시안: body 단계(값은 지금 24/28 과 같다). 리본 위라 inverse. 비활성 색은 어두운 면용이 없어 그대로.
            text caption align (.5,.5) xoffset -6 font R13_UI_BOLD_FONT size (r13_type("body")) color ((r13_type_color("inverse")) if enabled else "#c0b6a5")

screen r13_night_controls(ready=True):
    $ line_active=renpy.get_screen("say") is not None and not any(renpy.get_screen(n) for n in ("choice","r13_topics","r13_resident_approach","r13_entry_karo_topics"))
    $ skip_action=([SetVariable("r13_carriage_skip",True),Function(renpy.end_interaction,True)] if place=="마차 안" else [SetVariable("r13_conv_skip",True),Function(renpy.end_interaction,True)])
    hbox:
        xanchor 1.0 xpos (R13_CONCEPT_RIGHT-30) yanchor .5 ypos r13_night_control_y() spacing 12
        if _preferences.afm_enable and line_active:
            use r13_night_link("자동 읽기 중 · 정지","■",None,Preference("auto-forward","disable"),enabled=ready,link_id="r13_night_auto_stop")
        if line_active:
            use r13_night_link("건너뛰기","▸▸",None,skip_action,enabled=ready)
        use r13_night_link("더보기",None,"settings",Show("r13_more_tools"),enabled=ready)
