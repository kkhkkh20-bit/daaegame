# 2026-10-29 엔딩 연출(소유자 「그걸로 적용하자」 — 엔딩 컷씬 제안서 시안 a1~a3 + b1).
#
# 1) 결말 컷: 결말 문구 줄에 {"endcut": "END-04"} 또는 {"endcut": "END-04:blanket"}(배경 판 + 투명 판)을 달면
#    그 줄 앞에서 검게 어두워졌다(0.8초) 컷이 뜨고, 대사창 없이 2초 그림만 보인 뒤 지문이 나온다(누르면 건너뜀).
#    컷이 떠 있는 동안 장소 이름표·날짜판은 감춘다(r13_cg_active, CG 와 같은 규칙). 컷은 그 결말이 끝날 때까지 남는다.
#    추모 소품(MEM-xx·WILD-ENDING-PROPS-xx)은 장면 위에 어둡게 깐 판 가운데 정사각으로 띄우고, 그 대사 묶음이 끝나면 내린다.
#    그림 파일이 없으면 아무것도 하지 않는다 — 요청서(docs/art-requests, END-01~11·MEM-01~08)의 그림이 오는 대로
#    assets/ending/<ID>.webp(투명 판은 <ID>-<판>.webp)에 넣기만 하면 그 줄에서 뜬다. 문구는 바꾸지 않는다.
# 2) 결말 이름 카드: 「이야기를 마쳤습니다」 확인창 대신 수첩 판에 결말 이름·지킨 사람/잃은 사람과
#    「저장하기」「메인 화면으로」를 함께 둔다(눌러야 할 창이 하나 줄고, 마지막 지문 위에 확인창이 덮이지 않는다).
default r13_end_cut_key = None

init 350 python:
    R13_END_CUT_DIR = "assets/ending/"
    # 이미 납품된 그림을 쓰는 컷. END-11 배경은 불타는 밤 배경 WILD-DAWN 이다(같은 그림을 두 번 요청하지 않는다).
    R13_END_CUT_BASE = {"END-11": "assets/wild-night/wild-village-dawn-ash.webp"}

    def r13_end_cut_is_prop(base):
        return base.startswith("MEM-") or base.startswith("WILD-ENDING-PROPS")

    def r13_end_cut_cover(path):
        # 1280x720 를 채우도록 같은 비율로 확대하고 가운데를 쓴다(배경 판과 투명 판이 같은 캔버스면 같은 자리에 겹친다).
        iw, ih = renpy.image_size(path)
        zoom = max(1280.0/iw, 720.0/ih)
        return Crop((int((iw*zoom-1280)/2), int((ih*zoom-720)/2), 1280, 720), Transform(path, zoom=zoom, nearest=True))

    def r13_end_cut_art(key):
        """컷 그림. 파일이 없으면 None — 그림이 오기 전에는 지금 화면 그대로 둔다."""
        base, _, layer = (key or "").partition(":")
        path = R13_END_CUT_BASE.get(base, R13_END_CUT_DIR+base+".webp")
        # 투명 판이 있는 컷은 배경 판을 <ID>-base.webp 로 받았다(2026-10-29 납품).
        if base and not renpy.loadable(path):
            path = R13_END_CUT_DIR+base+"-base.webp"
        if not base or not renpy.loadable(path):
            return None
        if r13_end_cut_is_prop(base):
            side = 480
            return Fixed(Solid("#05080cc8"),
                Transform(path, xysize=(side, side), fit="contain", nearest=True, xalign=.5, ypos=56),
                xysize=(1280, 720))
        parts = [r13_end_cut_cover(path)]
        layer_path = R13_END_CUT_DIR+base+"-"+layer+".webp"
        if layer and renpy.loadable(layer_path):
            parts.append(r13_end_cut_cover(layer_path))
        return Fixed(*parts, xysize=(1280, 720))

    def r13_end_cut_fast():
        return renpy.is_skipping() or getattr(store, "r13_fast_read", False) or getattr(store, "r13_fast_all", False)

    def r13_end_cut_show(key):
        art = r13_end_cut_art(key)
        if art is None:
            return False
        prop = r13_end_cut_is_prop(key.partition(":")[0])
        tag = "r13_end_prop" if prop else "r13_end_cut"
        if not prop:
            store.r13_cg_active = True
            store.r13_end_cut_key = key
            renpy.hide("r13_visitor")
        if r13_end_cut_fast():
            renpy.show(tag, what=art, zorder=(9 if prop else 8))
            return True
        if prop:
            renpy.show(tag, what=art, zorder=9)
            renpy.with_statement(Dissolve(.4))
            return True
        renpy.show("r13_end_black", what=At(Solid("#000"), r13_end_black_in), zorder=10)
        renpy.pause(.8, hard=True)
        renpy.show(tag, what=art, zorder=8)
        renpy.hide("r13_end_black")
        renpy.with_statement(Dissolve(.4))
        renpy.pause(2.0)
        return True

    def r13_end_cut_hide():
        renpy.hide("r13_end_cut")
        renpy.hide("r13_end_prop")
        if store.r13_end_cut_key:
            store.r13_cg_active = False
        store.r13_end_cut_key = None

    _r13_end_cut_line_art = r13_ep_line_art
    def r13_ep_line_art(packet):
        options = packet[2] if len(packet) > 2 and isinstance(packet[2], dict) else {}
        if options.get("endcut"):
            r13_end_cut_show(options["endcut"])
        return _r13_end_cut_line_art(packet)

    # 소품은 그 대사 묶음과 함께 내려간다. 결말 컷은 결말 카드까지 남는다.
    _r13_end_cut_line_clear = r13_ep_line_art_clear
    def r13_ep_line_art_clear():
        renpy.hide("r13_end_prop")
        return _r13_end_cut_line_clear()

    def r13_end_card_lost():
        """잃은 사람 이름. 다람·엄마는 R13_NW_LIVES 밖이라 결말이 따로 말하는 경우만 더한다."""
        names = [r13_display_name(p) for p in r13_nw_dead()]
        ending = r13_v111_value("ending14")
        if ending == "left_name":
            names = [r13_display_name("daram")]+names
        if ending == "wild_night":
            family = r13_v111_value("wild_family")
            if family in ("no_mom", "alone"):
                names = [r13_display_name("mom")]+names
            if family == "alone":
                names = [r13_display_name("daram")]+names
        return names

    def r13_end_card_info():
        ending = r13_v111_value("ending14")
        dead = r13_nw_dead()
        kept = [who for who, key in R13_NW_LIVES if who not in dead]
        lost = r13_end_card_lost()
        return R13_FORK_ENDINGS.get(ending, ""), "지킨 사람 %d · 잃은 사람 %d" % (len(kept), len(lost)), " · ".join(lost)

transform r13_end_black_in:
    alpha 0.0
    linear .8 alpha 1.0

screen r13_end_card(name, stat, lost):
    modal True
    zorder 100
    default ready = False
    timer .45 action SetScreenVariable("ready", True)
    add Solid("#05070fa6")
    add r13_asset(R13_NB_PANEL) pos R13_NB_PANEL_POS
    text "열나흘째 · 이야기의 끝" xpos R13_NB_TITLE_X ypos R13_NB_TITLE_Y font R13_UI_BOLD_FONT size r13_type("subtitle") color r13_type_color("muted")
    add Solid("#c9a86a99") xpos R13_NB_LEFT ypos R13_NB_RULE_Y xsize R13_NB_WIDTH ysize 2
    vbox:
        xpos (R13_NB_LEFT+R13_NB_WIDTH//2) xanchor .5 ypos 220 spacing 22
        text "결말" xalign .5 font R13_UI_BOLD_FONT size r13_type("body") color r13_type_color("accent")
        text name id "r13_end_name" xalign .5 font R13_UI_BOLD_FONT size r13_type("display") color r13_type_color("ink")
        add Solid("#bc4134") xalign .5 xsize 220 ysize 4
        text stat xalign .5 font R13_UI_BOLD_FONT size r13_type("subtitle") color r13_type_color("ink")
        if lost:
            text lost xalign .5 xmaximum (R13_NB_WIDTH-80) text_align .5 size r13_type("emphasis") color r13_type_color("muted")
    hbox:
        xpos R13_NB_RIGHT xanchor 1.0 ypos r13_nb_footer_y() spacing R13_NB_GAP
        use r13_control("저장하기", None, Return(False), enabled=ready, width=220, control_id="r13_end_save")
        use r13_control("메인 화면으로", None, Return(True), enabled=ready, primary=True, width=260, control_id="r13_end_main")

label r13_v111_end_card14:
    window hide
    $ r13_end_card_name, r13_end_card_stat, r13_end_card_names = r13_end_card_info()
    call screen r13_end_card(r13_end_card_name, r13_end_card_stat, r13_end_card_names)
    if not _return:
        call screen save
    $ r13_end_cut_hide()
    return
