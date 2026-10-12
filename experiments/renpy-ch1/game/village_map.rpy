# One illustrated village. Houses remain visible behind small location plaques.
init 35 python:
    VILLAGE_MAP_REGIONS={
        "gate":(55,305,310,220),"fountain":(375,235,220,160),
        "post":(530,80,270,180),"lane":(555,385,300,220),
        "inn":(855,215,355,295)}
    VILLAGE_MAP_PLAQUES={
        "gate":(108,501),"fountain":(393,371),"post":(612,260),
        "lane":(626,610),"inn":(941,501)}

    def village_map_people(location):
        result=[]
        original=village_arrival_resident(location)
        if original:
            person=SOURCE_ALIAS.get(original,original)
            result.append(dict(id=person,public_name=NAMES[person] if original in store.arrival_met else "주민",met=original in store.arrival_met))
        result.extend(village_outdoor_people(location))
        return result

    def village_map_visited(location):
        return location in store.village_places_seen or location==store.arrival_location or location=="post" and store.arrival_post_closed or any(
            observation["place"]==ARRIVAL_PLACES[location][0] for observation in store.village_observations)

screen arrival_map():
    modal True
    default ready=False
    default hover_place=None
    timer .35 action SetScreenVariable("ready",True)
    add Transform("assets/village-overview.png",size=(1280,720))
    frame:
        xpos 26 ypos 94 padding (15,10) background Solid("#201b18e5")
        vbox:
            spacing 5
            text "골짜기 마을" size 29 color "#ffdc91"
            text village_clock() size 18 color "#eadcc0"
    for location,spec in ARRIVAL_PLACES.items():
        $ region=VILLAGE_MAP_REGIONS[location]
        $ plaque=VILLAGE_MAP_PLAQUES[location]
        $ current=location==arrival_location
        button:
            xpos region[0] ypos region[1] xsize region[2] ysize region[3]
            padding (0,0) background None hover_background Solid("#ffe1a019")
            sensitive ready action Return(location)
            hovered SetScreenVariable("hover_place",location)
            unhovered SetScreenVariable("hover_place",None)
            id ("map_building_"+location)
        button:
            xpos plaque[0] ypos plaque[1] xsize 202 ysize 60
            padding (10,6)
            background Solid("#f5e8cfed" if current else "#261d19ef")
            hover_background Solid("#f5e8cffa")
            sensitive ready action Return(location)
            fixed:
                text spec[0] size 22 color ("#473127" if current else "#f5e8cf") xalign .5
                text ("현재 위치" if current else "문 닫힘" if location=="post" and arrival_post_closed else "다녀간 곳" if village_map_visited(location) else "") size 15 color ("#735540" if current else "#c6ad84") xalign .5 ypos 28
            id ("map_label_"+location)
        $ residents=village_map_people(location)
        if residents:
            hbox:
                xpos plaque[0]+8 ypos plaque[1]-40 spacing 4
                for resident in residents:
                    frame:
                        padding (3,3) background Solid("#201b18de")
                        add Transform(resident["id"]+" avatar_neutral",size=(31,31),fit="contain")
    if hover_place:
        $ present=village_map_people(hover_place)
        frame:
            xpos 320 ypos 22 xsize 590 padding (12,9) background Solid("#201b18e8")
            text (ARRIVAL_PLACES[hover_place][0]+(" · "+" / ".join(p["public_name"] for p in present) if present else " · 지금은 조용하다")) size 19 color "#f3e7ce" xalign .5
    textbutton "산길 · 해 진 뒤":
        xpos 936 ypos 116 text_size 16 text_color "#c6ad84"
        background Solid("#201b18cc") hover_background Solid("#47382ddd")
        sensitive ready action Notify("길이 낯설다. 오늘은 마을 안에서 묵을 곳부터 찾자.")
    frame:
        xpos 30 ypos 682 padding (13,6) background Solid("#201b18e5")
        text ("우체국은 내일 열린다 · 오늘은 여관에서 쉬자" if arrival_post_closed else "건물을 눌러 이동 · 작은 얼굴은 지금 그곳에 있는 주민") size 18 color "#eadcc0"
