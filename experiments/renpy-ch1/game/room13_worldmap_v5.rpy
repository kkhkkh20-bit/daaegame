# Legacy filename retained for saves; cartography v6 uses buildings as targets.
init 61 python:
    R13_CARTOGRAPHY = json.load(renpy.file("room13-cartography.json"))
    R13_MAP_SCALE = 1248.0 / 1672
    for _region, _spec in R13_CARTOGRAPHY["regions"].items():
        R13_MAP_NODES[_region] = {key: tuple(int(round(p * R13_MAP_SCALE)) for p in node["point"])
            for key, node in _spec["nodes"].items()}

    def r13_cart_rect(region,key):
        x,y,w,h=R13_CARTOGRAPHY["regions"][region]["nodes"][key]["bounds"]
        a,b,c,d=[int(round(v*R13_MAP_SCALE)) for v in (x,y,x+w,y+h)]
        return a,b,c-a,d-b

    def r13_cart_layer(region,key,highlight=False,outline=False):
        path="assets/room13-map-%s-%s%s.webp" % (region,key,"-outline" if outline else "")
        art=Transform(path,size=r13_cart_rect(region,key)[2:],nearest=True)
        return Transform(art,matrixcolor=BrightnessMatrix(.09)) if highlight else art

    def r13_cart_point(region,key):
        x,y=R13_MAP_NODES[region][key]
        return 16+x,9+y

    def r13_cart_label_point(key):
        x,y=R13_CARTOGRAPHY["regions"]["village"]["nodes"][key]["label_point"]
        return 16+int(round(x*R13_MAP_SCALE)),9+int(round(y*R13_MAP_SCALE))

    def r13_cart_cover_visible(key):
        # Image discovery uses the same authored knowledge gate as the names.
        # The base image contains ordinary forest, not future-place silhouettes.
        return key in dict(r13_map_nodes("mountain"))

screen r13_cartography(region,selected,ready,map_hover):
    $ art=R13_CARTOGRAPHY["regions"][region]["art"]
    add Transform(art,size=(1248,702),nearest=True) xpos 16 ypos 9
    if region=="mountain":
        for secret in ("greenhouse","altar"):
            if r13_cart_cover_visible(secret):
                $ cx,cy,cw,ch=R13_CARTOGRAPHY["reveals"][secret]["bounds"]
                add Transform(R13_CARTOGRAPHY["reveals"][secret]["art"],size=(int(round(cw*R13_MAP_SCALE)),int(round(ch*R13_MAP_SCALE))),nearest=True) xpos (16+int(round(cx*R13_MAP_SCALE))) ypos (9+int(round(cy*R13_MAP_SCALE)))
    for key,point in r13_map_nodes(region):
        $ lx,ly,lw,lh=r13_cart_rect(region,key)
        button:
            id ("map_building_"+key)
            area (16+lx,9+ly,lw,lh) padding (0,0)
            background (r13_cart_layer(region,key,True) if region!="village" and key==selected else None)
            hover_background (r13_cart_layer(region,key,True) if region!="village" else None)
            insensitive_background None
            focus_mask r13_cart_layer(region,key)
            action SetScreenVariable("selected",key)
            hovered SetScreenVariable("map_hover",key)
            unhovered SetScreenVariable("map_hover",None)
            sensitive ready
            alt R13_MAP_LABELS[key]
        if region!="village" and (key==selected or key==map_hover):
            add r13_cart_layer(region,key,outline=True) xpos (16+lx) ypos (9+ly)
    # The drawing is the destination; real game-font labels share its selection.
    # These use the same knowledge gates as the building masks, never future names.
    if region=="village":
        for key,point in r13_map_nodes(region):
            $ hx,hy=r13_cart_label_point(key)
            $ title="여관" if key=="inn" else R13_MAP_LABELS[key]
            $ active=key==selected or key==map_hover
            $ nw=max(100,24+len(title)*21)
            button:
                id ("map_name_"+key)
                xpos (hx-nw//2) ypos (hy-21) xysize (nw,42) padding (8,5)
                background (R13InkPanel(focused=True) if active else Solid("#f0dfbd88"))
                hover_background R13InkPanel(focused=True)
                action SetScreenVariable("selected",key)
                hovered SetScreenVariable("map_hover",key)
                unhovered SetScreenVariable("map_hover",None)
                sensitive ready
                alt R13_MAP_LABELS[key]
                text title size 21 color ("#fff0d2" if active else "#493b30") align (.5,.5)
            if key==room13["location"]:
                text "현재 위치" xpos hx ypos (hy+24 if hy<565 else hy-42) xanchor .5 size 14 color "#765b3e"
    elif map_hover in dict(r13_map_nodes(region)):
        $ hx,hy=r13_cart_point(region,map_hover)
        $ nw=max(118,min(230,32+len(R13_MAP_LABELS[map_hover])*22))
        frame:
            xpos (max(24,min(1256-nw,hx-nw//2))) ypos (max(101,min(568,hy-62)))
            xysize (nw,38) padding (8,3) background R13InkPanel(focused=True)
            text R13_MAP_LABELS[map_hover] size 21 color "#fff0d2" align (.5,.5)
