# Village map v5 (closed PR #8, ported to 0.18.5). Winter mountain village with
# a shrine and an old quarry, no church. The original picture is drawn once;
# the 8 real destinations (R13_MAP_NODES["village"]) get UI names, a polygon
# pointer area and a highlight. The shrine, quarry and other houses are
# scenery: no node, no label, no click (room13-worldmap-v5.json, node=None).
# Destination layers are pre-cut by dev/make_worldmap_layers.py (polygon
# outlines, not pixel-exact building cut-outs).
init 61 python:
    R13_WORLD_V5 = json.load(renpy.file("room13-worldmap-v5.json"))
    R13_WORLD_V5_ART = "assets/room13-worldmap-v5.webp"
    R13_WORLD_V5_SCALE = 860.0 / 1672
    R13_MAP_NODES["village"] = {key: tuple(int(round(p * R13_WORLD_V5_SCALE)) for p in spec["point"])
        for key, spec in R13_WORLD_V5["layers"].items() if spec["node"]}

    def r13_v5_rect(key):
        x, y, w, h = R13_WORLD_V5["layers"][key]["bounds"]
        x0, y0, x1, y1 = [int(round(v * R13_WORLD_V5_SCALE)) for v in (x, y, x+w, y+h)]
        return (x0, y0, x1-x0, y1-y0)

    def r13_v5_layer(key, highlighted=False):
        art = "assets/room13-worldmap-v5-%s.webp" % key
        if highlighted:
            art = Transform(art, matrixcolor=BrightnessMatrix(.18))
        return Transform(art, size=r13_v5_rect(key)[2:], nearest=True)

    def r13_v5_outline(key):
        return Transform("assets/room13-worldmap-v5-%s-outline.webp" % key, size=r13_v5_rect(key)[2:], nearest=True)

    def r13_v5_label(key):
        return tuple(int(round(p * R13_WORLD_V5_SCALE)) for p in R13_WORLD_V5["layers"][key]["label"])

screen r13_worldmap_v5(selected, ready, map_hover):
    add Transform(R13_WORLD_V5_ART, size=(860,484), nearest=True) xpos 30 ypos 150
    for key, point in r13_map_nodes("village"):
        $ lx, ly, lw, lh = r13_v5_rect(key)
        button:
            id ("v5_building_"+key)
            xpos (30+lx) ypos (150+ly) xysize (lw, lh) padding (0, 0)
            background (r13_v5_layer(key, True) if key==selected or key==map_hover else None)
            hover_background r13_v5_layer(key, True)
            insensitive_background None
            focus_mask r13_v5_layer(key)
            action SetScreenVariable("selected",key)
            hovered SetScreenVariable("map_hover",key)
            unhovered SetScreenVariable("map_hover",None)
            sensitive ready
            alt R13_MAP_LABELS[key]
        if key==selected or key==map_hover:
            add r13_v5_outline(key) xpos (30+lx) ypos (150+ly)
    # 0.18.47 (owner): no bobbing pin; the label's ● marks the current place.
    # Text remains UI text; no painted-in names and no labels for locked nodes.
    for key, point in r13_map_nodes("village"):
        $ tx, ty = r13_v5_label(key)
        textbutton (("● " if key==room13["location"] else "") + R13_MAP_LABELS[key]):
            id ("v5_label_"+key)
            area (30+tx-57,150+ty-18,114,36)
            padding (3,3)
            text_size 20 text_xalign .5 text_yalign .5
            text_color "#fff3d5" text_hover_color "#ffffff"
            background Solid("#325b50f5" if key==selected else "#152e30e8")
            hover_background Solid("#51665af5")
            action SetScreenVariable("selected",key)
            hovered SetScreenVariable("map_hover",key)
            unhovered SetScreenVariable("map_hover",None)
            sensitive ready
            alt R13_MAP_LABELS[key]
