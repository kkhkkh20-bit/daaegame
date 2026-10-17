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
        x,y=tuple(int(round(p * R13_WORLD_V5_SCALE)) for p in R13_WORLD_V5["layers"][key]["label"])
        # Leave separate touch targets for the tight school/clinic/workshop cluster.
        dx,dy={"school":(0,-20),"workshop":(-42,0),"market":(10,0),"post":(0,5)}.get(key,(0,0))
        return x+dx,y+dy

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
            action r13_map_pick(key,selected)
            hovered SetScreenVariable("map_hover",key)
            unhovered SetScreenVariable("map_hover",None)
            sensitive ready
            alt R13_MAP_LABELS[key]
        if key==selected or key==map_hover:
            add r13_v5_outline(key) xpos (30+lx) ypos (150+ly)
    # Compact pictograms leave the geography visible. Names appear on focus,
    # including touch selection; polygon hit areas remain available underneath.
    for key, point in r13_map_nodes("village"):
        $ tx, ty = r13_v5_label(key)
        button:
            id ("v5_label_"+key)
            area (30+tx-32,150+ty-32,64,64)
            padding (0,0)
            background None
            action r13_map_pick(key,selected)
            hovered SetScreenVariable("map_hover",key)
            unhovered SetScreenVariable("map_hover",None)
            sensitive ready
            alt R13_MAP_LABELS[key]
            add R13PaperPanel(key==selected or key==map_hover) xysize (44,44) align (.5,.5)
            add R13AntiqueIcon("place_"+key,size=30) align (.5,.5)
        if key==room13["location"]:
            add Solid("#a15435") xpos (30+tx-5) ypos (150+ty+17) xysize (10,5)
    $ active=map_hover or selected
    if active in dict(r13_map_nodes("village")):
        $ tx,ty=r13_v5_label(active)
        $ name_width=max(96,min(200,28+len(R13_MAP_LABELS[active])*22))
        frame:
            xpos (30+max(0,min(860-name_width,tx-name_width//2))) ypos (150+max(0,ty-61))
            xysize (name_width,34) padding (6,2) background R13InkPanel(focused=True)
            text R13_MAP_LABELS[active] size 20 color "#fff3d5" align (.5,.5)
