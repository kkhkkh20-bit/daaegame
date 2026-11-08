# 현장에서 본 바깥 판과 돌 아래 안쪽 받침을, 해당 성공 설명에서만 함께 보여 준다.
# 기존 E17/E32/E33의 관계를 읽는 그림이다. 자료·정답·기회·생사에는 쓰지 않는다.
init 365 python:
    R13_LATCH132_ART="assets/room13-latch-diagram132.webp"
    R13_LATCH132_CUTS=("latch132_outer","latch132_inner")

    def r13_latch132_layout():
        # 일반/큰 글씨 대사판과 이름 리본 위, 단독 회의 인물 얼굴 오른쪽.
        return dict(x=790,y=124,w=470,h=376,art_x=12,art_y=38,art_w=446,art_h=297)

    def r13_latch132_focus(kind):
        # 생성 원화의 해당 위치만 테두리로 짚는다. 화살표로 새 운동 경로를 만들지 않는다.
        return (114,66,44,256) if kind=="latch132_outer" else (278,234,60,42)

    R13_LATCH132_LEGACY_LINES={
        "MS14_D03_S05_L0021":"latch132_outer",
        "MS14_D03_S05_L0022":"latch132_outer",
        "MS14_D03_S05_L0023":"latch132_inner",
        "MS14_D03_S05_L0024":"latch132_inner",
    }

    def r13_latch132_resume_kind(packet,current_cut,active,scene,say_visible):
        if not active or scene!="MS14_D03_S05" or not say_visible:return None
        options=packet[2] if packet and len(packet)>2 and isinstance(packet[2],dict) else {}
        rid=options.get("line_id")
        if rid=="MS14_D03_S05_L0025":return None
        return R13_LATCH132_LEGACY_LINES.get(rid) or (current_cut if current_cut in R13_LATCH132_CUTS else None)

    def r13_latch132_packet(packet,active,scene):
        # 옛 저장에 이미 계산된 다음 대사들도 같은 위치 강조를 얻는다. 원 packet은 그대로 둔다.
        if not active or scene!="MS14_D03_S05":return packet
        options=packet[2] if packet and len(packet)>2 and isinstance(packet[2],dict) else {}
        rid=options.get("line_id")
        if rid not in R13_LATCH132_LEGACY_LINES and rid!="MS14_D03_S05_L0025":return packet
        cut=R13_LATCH132_LEGACY_LINES.get(rid)
        if "cut" in options and options["cut"]==cut:return packet
        return tuple(packet[:2])+(dict(options,cut=cut),)+tuple(packet[3:])

    def r13_latch132_after_load():
        packet=getattr(store,"r13_packet",None)
        current_cut=getattr(store,"r13_ep_cut_current",None)
        scene=(getattr(store,"room13",None) or {}).get("v111",{}).get("scene")
        kind=r13_latch132_resume_kind(packet,current_cut,r13_v111_active(),scene,bool(renpy.get_screen("say")))
        if kind:
            # 옛 저장의 packet은 그대로 둔다. 서사 값이나 효과음을 재실행하지 않고 UI만 복원한다.
            store.r13_ep_cut_current=kind
            renpy.show("r13_ep_cut",what=Null(),zorder=5)
            renpy.show_screen("r13_latch_diagram132",kind=kind)
        else:
            renpy.hide_screen("r13_latch_diagram132")
            if current_cut in R13_LATCH132_CUTS:
                store.r13_ep_cut_current=None
                renpy.hide("r13_ep_cut")

    config.after_load_callbacks.append(r13_latch132_after_load)

    _r13_latch132_cut_art=r13_ep_cut_art
    def r13_ep_cut_art(name):
        # 회의 무대가 main 컷보다 위에 있으므로 도식은 아래의 비모달 screen이 맡는다.
        if name in R13_LATCH132_CUTS:return Null()
        return _r13_latch132_cut_art(name)

    _r13_latch132_line_art=r13_ep_line_art
    def r13_ep_line_art(packet):
        scene=(getattr(store,"room13",None) or {}).get("v111",{}).get("scene")
        display_packet=r13_latch132_packet(packet,r13_v111_active(),scene)
        result=_r13_latch132_line_art(display_packet)
        cut=getattr(store,"r13_ep_cut_current",None)
        if cut in R13_LATCH132_CUTS:
            renpy.show_screen("r13_latch_diagram132",kind=cut)
        else:
            renpy.hide_screen("r13_latch_diagram132")
        return result

    _r13_latch132_line_clear=r13_ep_line_art_clear
    def r13_ep_line_art_clear():
        renpy.hide_screen("r13_latch_diagram132")
        return _r13_latch132_line_clear()

screen r13_latch_diagram132(kind):
    # 버튼/입력 가로채기 없이 대사와 함께 읽는 관찰 그림.
    zorder 6
    $ L=r13_latch132_layout()
    $ fx,fy,fw,fh=r13_latch132_focus(kind)
    $ ink=r13_type_color("ink")
    $ accent=r13_type_color("accent")
    $ muted=r13_type_color("muted")
    fixed:
        xpos L["x"] ypos L["y"] xysize (L["w"],L["h"])
        add r13_ev_pixel_panel(L["w"],L["h"])
        add Solid("#fff3df") pos (12,12) xysize (L["w"]-24,L["h"]-24)
        add Transform(R13_LATCH132_ART,xysize=(L["art_w"],L["art_h"]),nearest=True) pos (L["art_x"],L["art_y"])
        text "3번 등 · 현장 스케치" xpos 22 ypos 14 xsize 426 size r13_type("body") color ink font R13_UI_BOLD_FONT
        text "바깥 판" xpos 20 ypos 78 xsize 104 size r13_type("small") color (accent if kind=="latch132_outer" else muted) font R13_UI_BOLD_FONT
        text "돌이 있던 자리" xpos 240 ypos 88 xsize 210 size r13_type("small") color muted font R13_UI_BOLD_FONT
        text "안쪽 받침" xpos 232 ypos 322 xsize 208 size r13_type("small") color (accent if kind=="latch132_inner" else muted) font R13_UI_BOLD_FONT
        text "파편" xpos 340 ypos 218 xsize 94 size r13_type("small") color (accent if kind=="latch132_inner" else muted) font R13_UI_BOLD_FONT
        add Solid("#a63a2e") pos (fx,fy) xysize (fw,3)
        add Solid("#a63a2e") pos (fx,fy+fh-3) xysize (fw,3)
        add Solid("#a63a2e") pos (fx,fy) xysize (3,fh)
        add Solid("#a63a2e") pos (fx+fw-3,fy) xysize (3,fh)
