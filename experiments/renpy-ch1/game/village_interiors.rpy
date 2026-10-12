# A building is a parent destination; its public rooms are local, saveable places.
# Bedrooms and case locations remain in the existing lodging/investigation flow.
default arrival_inn_room = "reception"
default village_interiors_seen = []

init 35 python:
    VILLAGE_INTERIORS = json.load(renpy.file("village-interiors.json"))

    def village_inn_spec():
        room=VILLAGE_INTERIORS["inn"]["rooms"][store.arrival_inn_room]
        return dict(sid="V_INN_"+store.arrival_inn_room.upper(),
            title="겨울잠 여관 · "+room["name"],sub=village_clock(),
            camera="stage",bg=room["background"],music="village_bright")

    def village_inn_guests():
        present={entry["id"] for entry in village_people_here("inn")}
        return [entry for entry in VILLAGE_INTERIORS["inn"]["rooms"]["lounge"]["people"] if entry["id"] in present]

    def village_interior_room(person,parent):
        for key,room in VILLAGE_INTERIORS.get(parent,{}).get("rooms",{}).items():
            if any(entry["id"]==person for entry in room.get("people",[])):
                return key
        return None

screen inn_room_navigation(ready):
    add Solid("#172225f2",xsize=1280,ysize=118) ypos 602
    add Solid("#bca579",xsize=1232,ysize=1) xpos 24 ypos 602
    for i,(key,room) in enumerate(VILLAGE_INTERIORS["inn"]["rooms"].items()):
        textbutton room["name"]:
            xpos (40+i*225) ypos 614 xsize 205 ysize 62 text_size 23
            background Solid("#dfd2af" if key==arrival_inn_room else "#293e38")
            text_color ("#21302e" if key==arrival_inn_room else "#f3e8cd")
            hover_background Solid("#647967")
            sensitive ready
            action (NullAction() if key==arrival_inn_room else Return("room:"+key))
    textbutton "살펴보기":
        xpos 510 ypos 614 xsize 185 ysize 62 text_size 23
        background None hover_background Solid("#344743") action Return("look") sensitive ready
    textbutton "여관 앞":
        xpos 730 ypos 614 xsize 165 ysize 62 text_size 23
        background None hover_background Solid("#344743") action Return("outside") sensitive ready
    textbutton "마을 지도":
        xpos 910 ypos 614 xsize 230 ysize 62 text_size 23
        background None hover_background Solid("#344743") action Return("map") sensitive ready
    text "마을  /  겨울잠 여관  /  [VILLAGE_INTERIORS['inn']['rooms'][arrival_inn_room]['name']]" xpos 58 ypos 687 size 16 color "#bfcac0"
