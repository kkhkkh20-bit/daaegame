# TEST ONLY · branch claude/rev13-appearance-test · board revision13 appearance test.
# Not part of the public game. The art data is changed by dev/apply_rev13_test.py (rollback:
# --revert). This file only adds a review gallery on the title screen: every changed person
# and the three new designs side by side on one floor line, feet on the line, the same
# standing height for adults (다람이 at her usual 0.83 share). The new designs have no gameId,
# schedule, event or story; they appear nowhere else.
init 990 python:
    import json as _r13_rev13_json
    R13_REV13 = _r13_rev13_json.load(renpy.file("assets/room13-rev13-gallery.json")) if renpy.loadable("assets/room13-rev13-gallery.json") else {"applied": [], "designs": []}
    R13_REV13_MODES = {"incoming": "외형 교체(옛 동작 제외)", "selected": "대표 선택(기존 동작 유지)", "gallery": "신규 디자인(배치 없음)", "reference": "기준"}

    def r13_rev13_gallery_rows():
        rows = [dict(kind="reference", person="daram", name=R13_NAMES.get("daram", "다람"), share=.83),
                dict(kind="reference", person="dad", name=R13_NAMES.get("dad", "아빠"), share=1.0)]
        for e in R13_REV13.get("applied", []):
            rows.append(dict(kind=e["mode"], person=e["npc"], name=R13_NAMES.get(e["npc"], e["name_ko"]), share=1.0))
        for g in R13_REV13.get("designs", []):
            rows.append(dict(kind="gallery", person=None, name=g["name_ko"].split(" (")[0] + " (가칭)", share=1.0, spec=g))
        return rows

    def r13_rev13_figure(row, height):
        """(displayable, foot_x, foot_y) at the given standing height."""
        spec = row.get("spec") or r13_acting_spec(row["person"], "neutral") or {}
        if not spec.get("file"):
            return None
        x, y, w, h = spec["crop"]
        fx, fy = spec.get("foot", [w / 2.0, h])
        scale = float(height) * row["share"] / fy
        art = Transform(Crop((x, y, w, h), spec["file"]), zoom=scale, nearest=True)
        return art, int(fx * scale), int(fy * scale)

screen r13_rev13_gallery():
    modal True
    zorder 300
    default page = 0
    $ rows = r13_rev13_gallery_rows()
    $ per = 8
    $ pages = (len(rows) + per - 1) // per
    $ shown = rows[page * per:(page + 1) * per]
    add Transform(Crop((300, 0, 1280, 720), "assets/room13-pixel-panorama-square-morning.webp"), size=(1280, 720), nearest=True)
    add Solid("#00000040")
    add Solid("#e0505088", xsize=1280, ysize=2) ypos 600
    text "rev13 외형 시험 적용 · 테스트 전용 (공개판 아님)" xpos 24 ypos 16 font r13_ui_font() size 22 color "#fff3d6" outlines [(2, "#2a1f17", 0, 0)]
    text "발은 붉은 선, 어른은 같은 선 키(300), 다람이는 0.83. %d / %d쪽" % (page + 1, pages) xpos 24 ypos 46 font r13_ui_font() size 16 color "#f0e4c8" outlines [(2, "#2a1f17", 0, 0)]
    for i, row in enumerate(shown):
        $ fig = r13_rev13_figure(row, 300)
        $ cx = 90 + i * 155
        if fig:
            add fig[0] xpos cx - fig[1] ypos 600 - fig[2]
        frame:
            xpos cx - 74 ypos 612 xsize 148 padding (4, 3) background Solid("#211a16d8")
            vbox:
                text row["name"] font r13_ui_font() size 17 color "#fff0ce" xalign .5
                text R13_REV13_MODES.get(row["kind"], row["kind"]) font r13_ui_font() size 11 color "#d9c9a5" xalign .5
    hbox:
        xalign 1.0 ypos 14 xoffset -20 spacing 8
        textbutton "이전" action SetScreenVariable("page", max(0, page - 1)) sensitive page > 0 text_font r13_ui_font() text_size 18
        textbutton "다음" action SetScreenVariable("page", min(pages - 1, page + 1)) sensitive page < pages - 1 text_font r13_ui_font() text_size 18
        textbutton "닫기" action Hide("r13_rev13_gallery") text_font r13_ui_font() text_size 18
    key "game_menu" action Hide("r13_rev13_gallery")
