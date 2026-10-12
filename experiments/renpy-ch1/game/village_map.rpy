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

init 35 python:
    VILLAGE_PLACE_LOOK = {
        "gate": [["det1","아빠, 우리가 지나가니까 말하다가 멈췄어."],["det0","처음 보는 얼굴이라 그런가 보다."],["det1","…나도 처음 보는데."]],
        "fountain": [["det1","돌에는 손 안 대는데, 옆에서는 다들 놀고 있네."],["det0","여기서는 익숙한 모양이지."],["det1","얼마나 오래 있었을까?"]],
        "post": [["det1","봉투 모서리가 접혔어. 주머니에 넣어서 그런가?"],["det0","내 가방에 넣을까?"],["det1","아니, 내가 조심해서 들게."]],
        "lane": [["det1","여기 냄새 좋아. 나무 타는 냄새."],["det0","발밑 봐. 장작이 굴러 나왔다."],["det1","누가 걸리겠다. 옆으로 옮겨 놓을까?"]],
        "inn": [["det1","창문에 김 서렸어. 안은 따뜻한가 봐."],["det0","발 시리니?"],["det1","조금. 아빠 손도 차갑네."]]}
    VILLAGE_PLACE_MOOD = {
        "gate": ("고개를 넘으면", "짐 푸는 사람들. 돌아오는 마차."),
        "fountain": ("등불이 켜지는 광장", "그림을 그리고, 간식을 나누는 자리."),
        "post": ("편지가 모이는 곳", "봉투를 정리하는 소리, 작은 수리대."),
        "lane": ("처마 아래 골목", "장작 냄새가 남은 조용한 샛길."),
        "inn": ("불 켜진 큰 창문", "하루 일을 마친 사람들이 모인다.")}

screen arrival_map():
    modal True
    default ready=False
    default hover_place=None
    timer .35 action SetScreenVariable("ready",True)
    add Transform("assets/village-overview.png",size=(1280,720))
    frame:
        xpos 24 ypos 22 xsize 420 padding (20,15) background Solid("#172225ee")
        vbox:
            spacing 8
            text "낯선 마을의 첫 저녁" size 28 color "#f3e8cd"
            text (village_clock()+"  /  "+str(sum(village_map_visited(k) for k in ARRIVAL_PLACES))+"곳을 걸었다") size 17 color "#bfcac0"
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
        frame:
            xpos plaque[0] ypos (min(plaque[1],555)) padding (10,6)
            background Solid("#172225de")
            text (("● " if current else "")+spec[0]) size 20 color "#f3e8cd"
    add Solid("#172225f5",xsize=1280,ysize=116) ypos 604
    add Solid("#bca579",xsize=1232,ysize=1) xpos 24 ypos 604
    for i,(location,spec) in enumerate(ARRIVAL_PLACES.items()):
        $ current=location==arrival_location
        button:
            xpos (24+i*248) ypos 615 xsize 238 ysize 94 padding (14,10)
            background Solid("#dfd2af" if current else "#263835") hover_background Solid("#475e55")
            sensitive ready action Return(location)
            id ("map_label_"+location)
            vbox:
                spacing 7
                text spec[0] size 23 color ("#20332f" if current else "#f3e8cd")
                text ("현재 위치" if current else "문 닫힘 · 내일 다시" if location=="post" and arrival_post_closed else "다녀간 곳" if village_map_visited(location) else "아직 가 보지 않은 곳") size 15 color ("#4c6559" if current else "#bfcac0")
    if village_interiors_seen:
        frame:
            xpos 934 ypos 421 padding (10,6) background Solid("#172225de")
            text "접수대 · 손님 홀" size 17 color "#d9c18c"
    $ focus=hover_place or arrival_location or "gate"
    frame:
        xpos 24 ypos 147 xsize 310 padding (18,15) background Solid("#172225e5")
        vbox:
            spacing 8
            text VILLAGE_PLACE_MOOD[focus][0] size 22 color "#e4cc96"
            text VILLAGE_PLACE_MOOD[focus][1] size 18 color "#d5dfd4" xsize 270
    textbutton "거리로 돌아가기":
        xpos 1030 ypos 94 xsize 225 text_size 20
        background Solid("#172225ed") hover_background Solid("#475e55")
        sensitive ready action Return(arrival_location or "gate")
