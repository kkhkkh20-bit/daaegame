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
        art_key=R13_CARTOGRAPHY["regions"][region]["nodes"][key].get("art_key",key)
        path="assets/room13-map-%s-%s%s.webp" % (region,art_key,"-outline" if outline else "")
        art=Transform(path,size=r13_cart_rect(region,key)[2:],nearest=True)
        return Transform(art,matrixcolor=BrightnessMatrix(.09)) if highlight else art

    def r13_cart_point(region,key):
        x,y=R13_MAP_NODES[region][key]
        ox,oy=R13_CARTOGRAPHY["regions"][region].get("offset",(16,9))
        return ox+x,oy+y

    def r13_cart_label_point(key):
        x,y=R13_CARTOGRAPHY["regions"]["village"]["nodes"][key]["label_point"]
        ox,oy=R13_CARTOGRAPHY["regions"]["village"].get("offset",(16,9))
        return ox+int(round(x*R13_MAP_SCALE)),oy+int(round(y*R13_MAP_SCALE))

    def r13_cart_name_rect(key):
        x,y,w,h=R13_CARTOGRAPHY["regions"]["village"]["nodes"][key]["label_bounds"]
        ox,oy=R13_CARTOGRAPHY["regions"]["village"].get("offset",(16,9))
        width=max(90,int(round(w*R13_MAP_SCALE))+16)
        height=max(42,int(round(h*R13_MAP_SCALE))+8)
        hx,hy=r13_cart_label_point(key)
        return hx-width//2,hy-height//2,width,height

    class R13MapInkUnderline(renpy.Displayable):
        def __init__(self,hovered=False,**kwargs):
            super(R13MapInkUnderline,self).__init__(**kwargs)
            self.hovered=hovered
        def render(self,width,height,st,at):
            w=max(1,int(width));r=renpy.Render(w,6);c=r.canvas()
            ink="#4b2817" if self.hovered else "#75482b"
            c.line(ink,(1,3),(w//2,2),3 if self.hovered else 2)
            c.line(ink,(w//2,2),(w-2,3),3 if self.hovered else 2)
            return r

    # 0.20.11 (owner 2026-10-23 "맵 자체를 좀 더 크게" → widened village map, same scale).
    # A region may carry its own drawing size; the village map is larger than the screen and
    # is shown in a draggable view that opens on the current or selected place.
    def r13_cart_canvas(region):
        w,h=R13_CARTOGRAPHY["regions"][region].get("size",R13_CARTOGRAPHY["size"])
        return int(round(w*R13_MAP_SCALE)),int(round(h*R13_MAP_SCALE))

    R13_MAP_VIEW=(1248,720)
    def r13_cart_focus(region,key):
        vw,vh=r13_cart_canvas(region)
        nodes=R13_MAP_NODES.get(region,{})
        x,y=nodes.get(key) or nodes.get(store.room13.get("location")) or (vw//2,vh//2)
        fx=max(0,min(vw-R13_MAP_VIEW[0],x-R13_MAP_VIEW[0]//2))
        fy=max(0,min(vh-R13_MAP_VIEW[1],y-R13_MAP_VIEW[1]//2+40))
        return int(fx),int(fy)

    # 0.20.11: light "tick" when choosing a place (shortened, quieter sfx-click), and which places lift on hover.
    R13_MAP_TICK="assets/sfx-map-tick.wav"
    def r13_cart_pops(region,key):
        node=R13_CARTOGRAPHY["regions"][region]["nodes"][key]
        return node.get("art_key",key) not in ("river","forest") and node["bounds"][2]*node["bounds"][3]<200000

    def r13_cart_cover_visible(key):
        # Image discovery uses the same authored knowledge gate as the names.
        # The base image contains ordinary forest, not future-place silhouettes.
        return key in dict(r13_map_nodes("mountain"))

screen r13_cartography(region,selected,ready,map_hover):
    if "size" in R13_CARTOGRAPHY["regions"][region]:
        $ vw,vh=r13_cart_canvas(region)
        $ fx,fy=r13_cart_focus(region,selected)
        viewport id "r13_map_view":
            xpos 16 ypos 0 xysize R13_MAP_VIEW
            draggable True mousewheel True
            xinitial fx yinitial fy
            fixed:
                xysize (vw,vh)
                use r13_cartography_layer(region,selected,ready,map_hover)
    else:
        use r13_cartography_layer(region,selected,ready,map_hover)

screen r13_cartography_layer(region,selected,ready,map_hover):
    $ art=R13_CARTOGRAPHY["regions"][region]["art"]
    $ ox,oy=R13_CARTOGRAPHY["regions"][region].get("offset",(16,9))
    add Transform(art,size=r13_cart_canvas(region),nearest=True) xpos ox ypos oy
    if region=="mountain":
        for secret in ("greenhouse","altar"):
            if r13_cart_cover_visible(secret):
                $ cx,cy,cw,ch=R13_CARTOGRAPHY["reveals"][secret]["bounds"]
                add Transform(R13_CARTOGRAPHY["reveals"][secret]["art"],size=(int(round(cw*R13_MAP_SCALE)),int(round(ch*R13_MAP_SCALE))),nearest=True) xpos (16+int(round(cx*R13_MAP_SCALE))) ypos (9+int(round(cy*R13_MAP_SCALE)))
    for key,point in r13_map_nodes(region):
        $ lx,ly,lw,lh=r13_cart_rect(region,key)
        # Reuse the authored contour: available destinations are visible before
        # hover, while undiscovered/unavailable places receive no travel outline.
        if key in r13_places():
            $ outlined_focus=key==selected or key==map_hover
            add Transform(r13_cart_layer(region,key,outline=True),matrixcolor=TintMatrix("#694425" if outlined_focus else "#a18b6c"),alpha=(1.0 if outlined_focus else .85)) xpos (ox+lx) ypos (oy+ly)
            # 0.20.11 (owner 2026-10-23 "마우스오버하면 아이콘처럼 집이 튀어나오게"): the place's own
            # drawing lifts a little on hover/selection. Wide terrain (river, forest) keeps the outline only.
            if outlined_focus and r13_cart_pops(region,key):
                add Transform(r13_cart_layer(region,key),matrixcolor=TintMatrix("#3b2414")*OpacityMatrix(.28)) xanchor .5 yanchor 1.0 xpos (ox+lx+lw//2) ypos (oy+ly+lh+3)
                add At(r13_cart_layer(region,key,highlight=True),r13_map_pop) xanchor .5 yanchor 1.0 xpos (ox+lx+lw//2) ypos (oy+ly+lh)
        button:
            id ("map_building_"+key)
            area (ox+lx,oy+ly,lw,lh) padding (0,0)
            background None
            hover_background None
            insensitive_background None
            focus_mask r13_cart_layer(region,key)
            action SetScreenVariable("selected",key)
            activate_sound R13_MAP_TICK
            hovered SetScreenVariable("map_hover",key)
            unhovered SetScreenVariable("map_hover",None)
            sensitive ready
            alt R13_MAP_LABELS[key]
    # Village names are ink in the approved drawing, not separate button plates.
    # Only existing eligible places receive interactive targets and underlines.
    # Building contours above persist independently of the supplementary underline.
    if region=="village":
        for key,point in r13_map_nodes(region):
            $ hx,hy=r13_cart_label_point(key)
            $ nx,ny,nw,nh=r13_cart_name_rect(key)
            button:
                id ("map_name_"+key)
                area (nx,ny,nw,nh) padding (0,0)
                background None hover_background None insensitive_background None
                action SetScreenVariable("selected",key)
                activate_sound R13_MAP_TICK
                hovered SetScreenVariable("map_hover",key)
                unhovered SetScreenVariable("map_hover",None)
                sensitive ready
                alt R13_MAP_LABELS[key]
            if key==selected or key==map_hover:
                $ underline_width=max(36,int(round(R13_CARTOGRAPHY["regions"]["village"]["nodes"][key]["label_bounds"][2]*R13_MAP_SCALE)))
                add R13MapInkUnderline(hovered=(key==map_hover)) xpos (hx-underline_width//2) ypos (hy+18) xysize (underline_width,6)
            if key==("inn" if room13["location"] in R13_INN_LOCATIONS else room13["location"]):
                text "현재 위치" xpos hx ypos (hy+24 if hy<565 else hy-42) xanchor .5 size 14 color "#765b3e"
    elif map_hover in dict(r13_map_nodes(region)):
        $ hx,hy=r13_cart_point(region,map_hover)
        $ nw=max(118,min(230,32+len(R13_MAP_LABELS[map_hover])*22))
        frame:
            xpos (max(24,min(1256-nw,hx-nw//2))) ypos (max(101,min(568,hy-62)))
            xysize (nw,38) padding (8,3) background R13InkPanel(focused=True)
            text R13_MAP_LABELS[map_hover] size 21 color "#fff0d2" align (.5,.5)

transform r13_map_pop:
    subpixel True
    zoom 1.0 yoffset 0
    easein .12 zoom 1.08 yoffset -6
