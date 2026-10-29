# B 지도: 「여관 안」·「숲·산길」 탭 (2026-10-24 소유자 "지도 에셋도 적용", "여관 에셋지도도 적용").
# 납품 원본: design/resource-intake-20261024/b-ui-map-inn/, b-ui-map-forest/ (manifest·placement 좌표).
# 게임 파일: game/assets/map-b/ (원본 PNG 를 투명 그대로 webp 로 옮김).
#
# - 수첩 틀(1280x720, 가운데 창 x88 y58 1136x570)을 0.86 배로 줄여 아래 고정 조작 줄(y602~712) 위에 둔다.
#   틀의 아래 띠(원래 캡션 자리)에 구역 이름·현재 위치·안내를 쓴다. 그림에는 글자가 없다.
# - 장소 스티커는 납품 좌표(지도 안 좌표)를 그대로 쓰고, 이름표는 게임이 그린다.
# - 무엇을 그릴지는 기존 판정(r13_map_nodes / r13_map_locked_nodes / r13_map_discovered)만 따른다.
#   새 공개 조건을 만들지 않는다. 드러나지 않은 장소는 스티커·이름표·누를 자리·접근성 이름을 모두 뺀다.
#   숲의 폐온실·제단은 그 자리에 가림판만, 여관 숨은 통로는 가림판이 없어 아무것도 그리지 않는다.
# - 고르거나 마우스를 올리면 스티커가 살짝 떠오른다(0.20.11 "아이콘처럼 집이 튀어나오게", r13_map_pop 재사용).
init 64 python:
    R13_BMAP_ART = "assets/map-b/"
    # 수첩 틀 축소 배치. 틀의 아래 띠 바닥(690*0.86+2=595)이 조작 줄(602) 위에서 끝난다.
    R13_BMAP_SCALE = 0.86
    R13_BMAP_FRAME_POS = (90, 2)
    R13_BMAP_WINDOW = (88, 58, 1136, 570)

    # 장소별 스티커·이름표 (지도 안 좌표 = 1136x570 바탕 기준).
    # sticker: (그림, 배치 상자 x,y,w,h — 그림 비율 그대로 상자 안 가운데),
    # label: 이름표 가운데. 여관은 placement_proposal.json 의 x,y,width,height,
    # 숲은 manifest.proposed.json 의 box/label_center 를 옮겼다. 여관 이름표 높이는
    # 실제 그림이 보이는 아래 끝(알파 상자)에 맞췄다 — 제안 좌표는 아래층 그림 위에 걸린다.
    R13_BMAP = {
        "inn": dict(base=r13_asset_path("file:assets/map-b/inn_base.webp"), places={
            "hall": dict(art=r13_asset_path("file:assets/map-b/inn_corridor.webp"), box=(95,68,280,280), label=(235,325), z=10),
            "room13": dict(art=r13_asset_path("file:assets/map-b/inn_room13.webp"), box=(409,56,290,290), label=(554,314), z=10),
            "guestroom": dict(art=r13_asset_path("file:assets/map-b/inn_temporary_guestroom.webp"), box=(770,56,290,290), label=(915,321), z=10),
            "inn": dict(art=r13_asset_path("file:assets/map-b/inn_reception.webp"), box=(95,300,270,270), label=(230,545), z=10),
            "dining": dict(art=r13_asset_path("file:assets/map-b/inn_dining.webp"), box=(430,300,270,270), label=(565,548), z=10),
            "kitchen": dict(art=r13_asset_path("file:assets/map-b/inn_kitchen.webp"), box=(775,300,270,270), label=(910,548), z=10),
            # 숨은 통로: 13호실과 임시 객실 사이, 방들 아래층(z5). 공개 전에는 아무것도 그리지 않는다.
            "passage": dict(art=r13_asset_path("file:assets/map-b/inn_hidden_passage.webp"), box=(652,103,160,160), label=(722,256), z=5),
            # 옛 시설(지하): 납품에 그림이 없다. 공개된 뒤에만 이름표 한 장을 지면 오른쪽 아래에 둔다.
            "ancient": dict(art=None, box=None, label=(1078,548), z=10),
        }, covers={}),
        "mountain": dict(base=r13_asset_path("file:assets/map-b/forest_base.webp"), places={
            "forest": dict(art=r13_asset_path("file:assets/map-b/forest_forest_path.webp"), box=(125,285,225,210), label=(237,516), z=10),
            "facility": dict(art=r13_asset_path("file:assets/map-b/forest_protection_facility.webp"), box=(290,50,260,190), label=(420,257), z=10),
            "greenhouse": dict(art=r13_asset_path("file:assets/map-b/forest_abandoned_greenhouse.webp"), box=(640,290,230,210), label=(755,520), z=10),
            "altar": dict(art=r13_asset_path("file:assets/map-b/forest_mountain_altar.webp"), box=(785,55,220,210), label=(895,284), z=10),
        }, covers={
            "greenhouse": dict(art=r13_asset_path("file:assets/map-b/forest_cover_greenhouse.webp"), box=(610,285,290,220)),
            "altar": dict(art=r13_asset_path("file:assets/map-b/forest_cover_altar.webp"), box=(750,50,290,235)),
        }),
    }
    R13_BMAP_ART_SIZES = {}

    def r13_bmap_regions():
        return tuple(R13_BMAP)

    def r13_bmap_screen(lx, ly):
        """지도 안 좌표 -> 화면 좌표."""
        fx, fy = R13_BMAP_FRAME_POS
        s = R13_BMAP_SCALE
        return fx+(R13_BMAP_WINDOW[0]+lx)*s, fy+(R13_BMAP_WINDOW[1]+ly)*s

    def r13_bmap_art_size(path):
        if path not in R13_BMAP_ART_SIZES:
            R13_BMAP_ART_SIZES[path] = renpy.image_size(path)
        return R13_BMAP_ART_SIZES[path]

    def r13_bmap_fit(path, box):
        """그림 비율을 지키며 상자 안 가운데에 놓은 화면 사각형 (x,y,w,h)."""
        bx, by, bw, bh = box
        iw, ih = r13_bmap_art_size(path)
        k = min(float(bw)/iw, float(bh)/ih)
        w, h = iw*k, ih*k
        x, y = r13_bmap_screen(bx+(bw-w)/2.0, by+(bh-h)/2.0)
        s = R13_BMAP_SCALE
        return int(round(x)), int(round(y)), int(round(w*s)), int(round(h*s))

    def r13_bmap_label_size():
        return 22 if r13_touch_ui() else 20

    def r13_bmap_text_units(text):
        # 한글 한 글자를 1, 띄어쓰기·라틴 문자·문장부호는 좁게 센다.
        return sum(.35 if c == " " else (.55 if ord(c) < 0x1100 else 1.0) for c in text)

    def r13_bmap_label_text(key):
        return ("현재 · " if key == store.room13.get("location") else "")+r13_map_label(key)

    def r13_bmap_label_rect(region, key):
        lx, ly = R13_BMAP[region]["places"][key]["label"]
        cx, cy = r13_bmap_screen(lx, ly)
        size = r13_bmap_label_size()
        w = int(r13_bmap_text_units(r13_bmap_label_text(key))*size)+30
        h = size+16
        x = int(round(cx-w/2.0))
        y = int(round(cy-h/2.0))
        # 수첩 창 밖으로 나가지 않게 (오른쪽 끝 옛 시설 이름표 등).
        left, top = r13_bmap_screen(0, 0)
        right, bottom = r13_bmap_screen(R13_BMAP_WINDOW[2], R13_BMAP_WINDOW[3])
        x = max(int(left)+4, min(int(right)-4-w, x))
        y = max(int(top)+4, min(int(bottom)-4-h, y))
        return x, y, w, h

    def r13_bmap_target(region, key):
        """누를 자리: 스티커 사각형과 이름표 사각형을 합친 상자, 그리고 그 안의 상대 위치."""
        spec = R13_BMAP[region]["places"][key]
        label = r13_bmap_label_rect(region, key)
        sticker = r13_bmap_fit(spec["art"], spec["box"]) if spec.get("art") else None
        rects = [label]+([sticker] if sticker else [])
        x0 = min(r[0] for r in rects); y0 = min(r[1] for r in rects)
        x1 = max(r[0]+r[2] for r in rects); y1 = max(r[1]+r[3] for r in rects)
        return dict(area=(x0, y0, x1-x0, y1-y0), sticker=sticker, label=label)

    def r13_bmap_mask(region, key):
        """그림이 실제로 보이는 곳과 이름표만 누를 수 있게 한다(투명한 귀퉁이는 빠진다)."""
        t = r13_bmap_target(region, key)
        x0, y0, w, h = t["area"]
        children = []
        if t["sticker"]:
            sx, sy, sw, sh = t["sticker"]
            children.append(Transform(R13_BMAP[region]["places"][key]["art"], size=(sw, sh), xpos=sx-x0, ypos=sy-y0))
        lx, ly, lw, lh = t["label"]
        children.append(Transform(Solid("#fff"), xpos=lx-x0, ypos=ly-y0, xysize=(lw, lh)))
        return Fixed(*children, xysize=(w, h))

    def r13_bmap_places(region):
        """[(key, 상태)] 그릴 순서(z) 대로. 상태: open(갈 수 있음) / shown(보이지만 지금은 못 감) / locked(공개된 곳, 눌러도 안내만).
        r13_map_nodes / r13_map_locked_nodes 에 없는 장소(숨은 곳 포함)는 아예 돌려주지 않는다."""
        places = R13_BMAP[region]["places"]
        allowed = set(r13_places())
        rows = []
        for key, point in r13_map_nodes(region):
            if key in places:
                rows.append((key, "open" if key in allowed else "shown"))
        shown = set(k for k, s in rows)
        for key, point in r13_map_locked_nodes(region):
            if key in places and key not in shown:
                rows.append((key, "locked"))
        return sorted(rows, key=lambda row: places[row[0]]["z"])

    def r13_bmap_covers(region):
        """가림판: 숨은 장소가 지도에 드러나지 않았을 때만. 판정은 기존 r13_cart_cover_visible 과 같다."""
        visible = set(key for key, point in r13_map_nodes(region))
        return [(key, spec) for key, spec in R13_BMAP[region]["covers"].items() if key not in visible]

    def r13_bmap_hint(region):
        if region == "mountain" and r13_map_locked_nodes(region):
            return "흐린 곳은 지금 갈 수 없습니다 · 고른 뒤 이동을 누르세요" if r13_touch_ui() else "흐린 곳은 지금 갈 수 없습니다 · 장소를 고른 뒤 이동을 누르세요"
        return "장소를 고른 뒤 이동을 누르세요"

    def r13_bmap_label_bg(w, h, focused=False, locked=False):
        # 여관 이동 칩(room13_inn_navigation_v4)과 같은 크림 판·갈색 테두리.
        return r13_inn_v4_chip_background(w, h, hover=focused, locked=locked)

transform r13_bmap_lift:
    subpixel True
    yoffset 0
    easein .12 yoffset -5

screen r13_map_b(region, selected, ready, map_hover, map_notice=None):
    $ spec = R13_BMAP[region]
    $ s = R13_BMAP_SCALE
    $ fx, fy = R13_BMAP_FRAME_POS
    $ wx, wy = r13_bmap_screen(0, 0)
    # 빈 바탕 → 수첩 틀 → 가림판·스티커 → 이름표 순. 틀을 스티커 아래에 두어 떠오른 스티커가 틀에 잘리지 않는다.
    add Transform(spec["base"], size=(int(round(R13_BMAP_WINDOW[2]*s))+2, int(round(R13_BMAP_WINDOW[3]*s))+2)) xpos (int(wx)-1) ypos (int(wy)-1)
    # The shared outer notebook and footer are owned by r13_map.
    for key, cover in r13_bmap_covers(region):
        $ cx, cy, cw, ch = r13_bmap_fit(cover["art"], cover["box"])
        add Transform(cover["art"], size=(cw, ch)) xpos cx ypos cy
    $ rows = r13_bmap_places(region)
    $ current = room13["location"]
    # 떠오른 스티커는 이웃 스티커(숨은 통로 위의 방 등)에 가리지 않게 맨 나중에 그린다.
    $ draw_rows = [r for r in rows if r[0] not in (selected, map_hover)]+[r for r in rows if r[0] in (selected, map_hover)]
    for key, state in draw_rows:
        $ place = spec["places"][key]
        $ t = r13_bmap_target(region, key)
        $ focused = state != "locked" and (key == selected or key == map_hover)
        $ lifts = focused and state == "open"
        if t["sticker"]:
            $ sx, sy, sw, sh = t["sticker"]
            $ art = Transform(place["art"], size=(sw, sh))
            if lifts:
                # 원래 자리에 옅은 그림자를 남기고 그림 자체가 떠오른다.
                add Transform(art, matrixcolor=TintMatrix("#3b2414")*OpacityMatrix(.22)) xpos sx ypos (sy+2)
                add At(art, r13_map_pop) xanchor .5 yanchor 1.0 xpos (sx+sw//2) ypos (sy+sh)
            elif state == "open":
                add art xpos sx ypos sy
            else:
                # 공개된 곳이지만 지금은 갈 수 없는 곳: 색을 빼고 조금 어둡게.
                add Transform(art, matrixcolor=SaturationMatrix(.3)*BrightnessMatrix(-.05), alpha=.9) xpos sx ypos sy
    for key, state in rows:
        $ lx, ly, lw, lh = r13_bmap_label_rect(region, key)
        $ focused = state != "locked" and (key == selected or key == map_hover)
        $ plate = Fixed(r13_bmap_label_bg(lw, lh, focused=focused, locked=state != "open"), Text(r13_bmap_label_text(key), size=r13_bmap_label_size(), font=R13_UI_BOLD_FONT, color=("#7a2a22" if key == selected else "#65503b" if state == "open" else "#82745e"), xalign=.5, yalign=.5), xysize=(lw, lh+3))
        if focused and state == "open":
            add At(plate, r13_bmap_lift) xpos lx ypos ly
        else:
            add plate xpos lx ypos ly
    for key,state in rows:
        use r13_map_status_badges(key,state,selected,r13_bmap_label_rect(region,key))
    # 누를 자리는 그림 위에 따로 둔다. 숨은 장소는 rows 에 없으므로 버튼·접근성 이름도 없다.
    for key, state in rows:
        $ t = r13_bmap_target(region, key)
        if state == "locked":
            button:
                id ("map_locked_"+key)
                area t["area"] padding (0, 0)
                background None hover_background None insensitive_background None
                focus_mask r13_bmap_mask(region, key)
                action SetScreenVariable("map_notice", r13_map_locked_notice(R13_MAP_LABELS[key]))
                sensitive ready
                alt (R13_MAP_LABELS[key]+" · 지금은 이동할 수 없음")
        else:
            button:
                id (("map_room_" if region == "inn" else "map_building_")+key)
                area t["area"] padding (0, 0)
                background None hover_background None insensitive_background None
                focus_mask r13_bmap_mask(region, key)
                action [SetScreenVariable("selected", key), SetScreenVariable("map_notice", None)]
                activate_sound R13_MAP_TICK
                # 터치에는 올림 단계가 없다: 여기서 다시 그리면 첫 탭을 먹을 수 있다.
                hovered (None if r13_touch_ui() else SetScreenVariable("map_hover", key))
                unhovered (None if r13_touch_ui() else SetScreenVariable("map_hover", None))
                sensitive ready
                alt r13_map_label(key)
