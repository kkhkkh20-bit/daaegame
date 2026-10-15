default persistent.room13_map_list = False

# Spatial navigation: selecting a pin never travels or spends time.
init 60 python:
    R13_MAP_REGIONS = (("village", "마을"), ("inn", "여관 안"), ("mountain", "북쪽 산길"))
    R13_MAP_NODES = {
        "village": {"gate":(132,354), "square":(336,250), "inn":(715,299),
            "post":(466,172), "workshop":(585,425), "clinic":(407,370),
            "school":(95,143), "store":(553,292)},
        "inn": {"inn":(435,420), "dining":(434,307), "kitchen":(170,307),
            "hall":(340,120), "room13":(685,120), "passage":(685,40), "guestroom":(245,65)},
        "mountain": {"facility":(110,135), "greenhouse":(382,108), "altar":(644,100)},
    }
    R13_MAP_LABELS = {"gate":"마을 입구", "square":"광장", "inn":"여관 접수대",
        "post":"우체국", "workshop":"수리점", "clinic":"진료실", "school":"학교",
        "store":"공동 창고", "dining":"식당", "kitchen":"주방", "hall":"2층 복도",
        "room13":"13호실", "guestroom":"임시 객실", "passage":"숨은 통로", "facility":"보호시설",
        "greenhouse":"폐온실", "altar":"산속 제단"}

    R13_INN_LOCATIONS=("inn","dining","kitchen","hall","room13","passage","guestroom")
    R13_LOCAL_CONNECTIONS={
        "inn":(("dining","식당"),("kitchen","주방"),("hall","2층 복도"),("outside","여관 밖으로")),
        "dining":(("inn","접수대"),("kitchen","주방")),
        "kitchen":(("dining","식당"),("inn","접수대")),
        "hall":(("inn","1층 접수대"),("room13","13호실"),("guestroom","임시 객실")),
        "room13":(("hall","복도로"),("passage","숨은 통로")),
        "guestroom":(("hall","복도로"),),
        "passage":(("room13","13호실로"),),
    }

    def r13_local_connections():
        allowed=set(r13_places())
        return [(key,title) for key,title in R13_LOCAL_CONNECTIONS.get(store.room13["location"],())
            if key=="outside" or key in allowed]

    def r13_local_destination(key):
        # Validate again at dispatch, including after a saved interaction resumes.
        return key if key in dict(r13_local_connections()) else None

    def r13_map_region(location):
        if location in R13_INN_LOCATIONS:return "inn"
        if location in ("facility","greenhouse","altar"):return "mountain"
        return "village"

    def r13_map_nodes(region):
        allowed=set(r13_places())|{store.room13["location"]}
        return [(key,point) for key,point in R13_MAP_NODES[region].items()
            if key in allowed and r13_map_discovered(key)]

    def r13_map_discovered(key):
        # Do not expose secret names through stale/legacy current-location saves.
        if key=="passage":return bool(store.room13.get("passage_open") and r13_secret_route_available())
        if key=="greenhouse":return bool(store.room13["day"]>=8 and r13_has("E19"))
        if key=="altar":return bool(store.room13.get("finale_started"))
        return True

    def r13_map_selection(region,selected):
        keys=[key for key,point in r13_map_nodes(region)]
        if selected in keys:return selected
        current=store.room13["location"]
        if current in keys:return current
        return next((key for key in keys if key in r13_places()),keys[0] if keys else None)

    def r13_location_path(location=None):
        location=location or store.room13["location"]
        if not r13_map_discovered(location):return "마을"
        title=R13_MAP_LABELS.get(location,R13_PLACES[location][0])
        if location in R13_INN_LOCATIONS:
            return "마을 › 여관 › "+("접수대" if location=="inn" else title)
        if location in ("facility","greenhouse","altar"):
            return "마을 › 북쪽 산길 › "+title
        return "마을 › "+title

    class R13VillageMap(renpy.Displayable):
        def __init__(self,region,**kwargs):
            super(R13VillageMap,self).__init__(**kwargs)
            self.region=region
        def render(self,width,height,st,at):
            rv=renpy.Render(860,490); c=rv.canvas()
            c.rect("#c6d5ce",(0,0,860,490))
            if self.region=="inn":
                c.rect("#d9d3bb",(30,22,800,450))
                c.rect("#786b53",(58,25,744,179),5)
                c.rect("#b9ad91",(83,98,637,45))
                for x in (98,205,440,545):
                    c.rect("#d3c6a3",(x,33,82,61));c.rect("#8c8063",(x,33,82,61),3)
                c.rect("#e6d6ae",(614,71,163,109));c.rect("#7b6849",(614,71,163,109),4)
                c.rect("#786b53",(58,242,744,217),5)
                c.line("#786b53",(288,245),(288,400),4)
                c.line("#786b53",(59,380),(800,380),4)
                for y in range(179,263,12):c.line("#877a5f",(331,y),(379,y),4)
            else:
                # Purposefully schematic pixel geometry; no ambiguous card grid.
                for x,y in ((20,25),(70,63),(760,50),(807,114),(30,420),(782,427),(58,145),(804,270)):
                    c.rect("#526e61",(x+9,y+24,8,21));c.polygon("#6a8976",((x,y+29),(x+13,y),(x+26,y+29)))
                    c.polygon("#edf0dc",((x+5,y+13),(x+13,y),(x+21,y+13)))
                if self.region=="village":
                    paths=[((430,455),(430,285)),((430,285),(430,85)),((430,200),(195,170)),
                        ((430,220),(677,180)),((430,350),(133,329)),((430,395),(702,404)),((677,180),(688,62))]
                    c.polygon("#8faea9",((755,0),(784,0),(604,490),(568,490)))
                else:
                    paths=[((80,460),(267,304)),((267,304),(415,202)),((415,202),(567,72)),((415,202),(635,377))]
                    for x,y in ((190,35),(310,12),(690,24)):
                        c.polygon("#99b0a7",((x-90,y+130),(x,y),(x+108,y+130)))
                        c.polygon("#f1efda",((x-29,y+44),(x,y),(x+35,y+44)))
                for a,b in paths:
                    c.line("#b9b197",a,b,27);c.line("#eae4c9",a,b,19)
                for key,(x,y) in r13_map_nodes(self.region):
                    if key=="square":
                        c.rect("#91a09a",(x-43,y-33,86,60),4)
                        c.rect("#63776d",(x-9,y-25,18,29))
                    else:
                        c.rect("#87978b",(x-38,y-28,76,49))
                        c.rect("#e5d9b6",(x-32,y-27,64,41))
                        c.polygon("#81615d",((x-43,y-27),(x,y-51),(x+43,y-27)))
                        c.rect("#65584b",(x-6,y-5,12,19))
                        c.rect("#d4aa58",(x-23,y-14,10,10))
            return rv

screen r13_map(initial_region=None):
    style_prefix "r13"
    modal True
    zorder 45
    default region=initial_region or r13_map_region(room13["location"])
    default selected=r13_map_selection(initial_region or r13_map_region(room13["location"]),"square" if initial_region=="village" and room13["location"] in R13_INN_LOCATIONS else room13["location"])
    default map_hover=None
    default ready=False
    # Revalidate restored selection before labels, previews or travel controls render.
    $ region = "village" if region=="mountain" and room13["day"]<8 else region
    $ selected = r13_map_selection(region,selected)
    key "game_menu" action Return(False)
    timer .25 action SetScreenVariable("ready",True)
    add r13_background(R13_PLACES[room13["location"]][1])
    add Solid("#211b1899")
    add R13TravelSheet() xpos 12 ypos 8 xsize 1256 ysize 704
    text ("여관 안내도" if region=="inn" else "북쪽 산길" if region=="mountain" else "마을 지도") xpos 30 ypos 22 size 32 color "#493b30"
    text ("현재 위치 · "+r13_location_path()) xpos 280 ypos 30 size 23 color "#765426"
    hbox:
        xpos 30 ypos 78 spacing 12
        for key,title in R13_MAP_REGIONS:
            textbutton ("‹ 마을 보기" if key=="village" and region!="village" else title):
                style "r13_action_button" xsize 190 ysize 58 text_size 23
                action [SetScreenVariable("region",key),SetScreenVariable("selected",r13_map_selection(key,selected))] selected region==key
                sensitive ready and (key!="mountain" or room13["day"]>=8)
    textbutton ("지도로 보기" if persistent.room13_map_list else "큰 목록 보기"):
        style "r13_action_button" xpos 1010 ypos 78 xsize 240 ysize 58 text_size 24
        action ToggleField(persistent,"room13_map_list") sensitive ready
    if persistent.room13_map_list:
        viewport:
            area (30,150,860,490)
            draggable True mousewheel True scrollbars "vertical"
            vbox:
                spacing 12
                for key,point in r13_map_nodes(region):
                    button:
                        xsize 830 ysize 136 padding (24,18)
                        background R13InkPanel(focused=(key==selected))
                        hover_background R13InkPanel(focused=True)
                        action SetScreenVariable("selected",key) sensitive ready
                        vbox:
                            spacing 12
                            text R13_MAP_LABELS[key] size 36 color "#fff0cb"
                            text ("● 현재 위치" if key==room13["location"] else "선택됨 · 오른쪽에서 이동 확정" if key==selected else "눌러서 장소 확인") size 25 color ("#f3ca73" if key==room13["location"] else "#d7e0d7")
    elif region=="village":
        use r13_worldmap_v5(selected,ready,map_hover)
    else:
        if region=="inn":
            add R13VillageMap(region) xpos 30 ypos 150
        else:
            add Transform("assets/room13-pixel-navigation-village.webp",size=(860,490),nearest=True) xpos 30 ypos 150
        for key,(px,py) in r13_map_nodes(region):
            button:
                area (30+px-82,150+py-30,164,64)
                padding (6,4)
                background R13InkPanel(focused=(key==selected))
                hover_background R13InkPanel(focused=True)
                action SetScreenVariable("selected",key) sensitive ready
                vbox:
                    xalign .5 yalign .5 spacing 3
                    text R13_MAP_LABELS[key] size 22 color "#fff0cb" xalign .5
                    if key==room13["location"]:
                        text "● 현재 위치" size 17 color "#f3ca73" xalign .5
    if selected is not None:
        frame:
            area (916,150,334,490) padding (22,18) background R13PaperFrame()
            fixed:
                xsize 290 ysize 454
                text R13_PLACES[selected][0] ypos 0 size 27 color "#765426" xsize 286
                add Transform(r13_background(R13_PLACES[selected][1]),size=(286,161),nearest=True) ypos 70
                if region=="village" and selected=="inn":
                    textbutton "여관 내부 보기 ›":
                        style "r13_action_button" ypos 243 xsize 286 ysize 64 text_size 24
                        action [SetScreenVariable("region","inn"),SetScreenVariable("selected","inn")] sensitive ready
                if selected==room13["location"]:
                    text "● 지금 머무는 곳" ypos 325 size 24 color "#89532e"
                elif selected in r13_places():
                    text "이동 비용 · 시간 소모 없음" ypos 325 size 21 color "#65503b" xsize 286
                    textbutton "이곳으로 이동":
                        style "r13_action_button" ypos 382 xsize 286 ysize 72 text_size 25
                        action Return(selected) sensitive ready
                else:
                    text "지금은 이동할 수 없습니다." ypos 325 size 22 color "#796044" xsize 286
    else:
        text "아직 확인한 장소가 없습니다." xpos 932 ypos 180 size 22 color "#65503b"
    text "장소 선택 → 이동 확정 · 지도 열람은 시간 소모 없음" xpos 30 ypos 673 size 20 color "#65503b"
    textbutton "현장으로 돌아가기":
        action Return(False) style "r13_action_button" xpos 950 ypos 650 xsize 300 ysize 60 text_size 24
