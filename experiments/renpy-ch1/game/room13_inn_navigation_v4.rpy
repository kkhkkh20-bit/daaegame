# Inn lobby / upstairs hall travel chips and the supplementary inn guide (0.18.5).
# The "안내도" button opens the hand-drawn guide (inn-guide-v4, owner's final
# choice). The older "여관 안내도" tab of the map screen is unchanged.
# Approved layout: inn-navigation-v4-integration.zip (assets/room13-inn-navigation-v4.json).
# - Backgrounds are unchanged (lobby panorama, hall-before/after art). Chip
#   rectangles are converted with exactly the background's transform.
# - Destinations come only from r13_local_connections(): the same access rules,
#   time cost (none) and dispatch (Return(("travel",key)) -> r13_local_destination)
#   as the older button row. "outside" is the existing exit that opens the map.
# - "Edge" chips are screen-edge UI, not doors drawn in the picture.
# - The passage and other unrevealed places are never named here.
init 63 python:
    R13_INN_V4 = json.load(renpy.file("assets/room13-inn-navigation-v4.json")) if renpy.loadable("assets/room13-inn-navigation-v4.json") else {}
    R13_INN_GUIDE = json.load(renpy.file("assets/room13-inn-guide.json")) if renpy.loadable("assets/room13-inn-guide.json") else {}
    R13_INN_GUIDE_SIZE = (960, 640)
    R13_INN_V4_CHIP_HEIGHT = 50
    # Bottom-centre belongs to the toolbar; a centred edge chip sits above it.
    R13_INN_V4_ABOVE_FOOTER = 588

    def r13_inn_v4_scale(location):
        source = R13_INN_V4[location]["source"]
        if location == "inn":
            return 1920.0/source[0], 720.0/source[1]
        return 1280.0/source[0], 720.0/source[1]

    def r13_inn_v4_chips(location, world=False):
        """[(key, label, (x,y,w,h), sensitive)]. world=True: chips drawn on the
        panorama (scroll with it); False: fixed screen UI."""
        spec = R13_INN_V4.get(location)
        if not spec:
            return []
        links = dict(r13_local_connections())
        sx, sy = r13_inn_v4_scale(location)
        panorama = location == "inn"
        result = []
        for chip in spec["chips"]:
            key = chip["to"]
            if key not in links and key != "room13":
                continue  # unavailable rooms (e.g. guest room) are not shown
            on_picture = chip["kind"] == "drawn"
            if panorama and on_picture != world:
                continue
            if not panorama and world:
                continue
            x0, y0, x1, y1 = chip["bounds"]
            cx, cy = (x0+x1)/2.0*sx, (y0+y1)/2.0*sy
            label = chip["label"] if key in links else chip["label"]+" · 잠김"
            w = max(int((x1-x0)*sx)+16, 26*len(label)//2+44)
            h = R13_INN_V4_CHIP_HEIGHT
            if on_picture:
                x, y = int(cx-w/2), int(cy-h/2)
            else:
                width = 1920.0 if panorama else 1280.0
                if abs(cx-width/2) < width*.15:
                    x, y = 640-w//2, R13_INN_V4_ABOVE_FOOTER
                elif cx < width/2:
                    x, y = int(x0*sx), int(cy-h/2)
                else:
                    x, y = int(1280-(spec["source"][0]-x1)*sx-w), int(cy-h/2)
            result.append((key, label, (x, y, w, h), key in links))
        return result

    def r13_inn_v4_handled(location):
        return {chip["to"] for chip in R13_INN_V4.get(location, {}).get("chips", [])}

    def r13_inn_v4_chip_background(w, h, hover=False, locked=False):
        fill = "#3a2c22f2" if locked else "#5a4433f2" if hover else "#2c221bdb"
        border = "#8a7a62d6" if locked else "#f2cf8a" if hover else "#c2a370d6"
        return Fixed(
            Transform(Solid("#00000038"), xpos=0, ypos=3, xysize=(w, h)),
            Transform(Solid(border), xysize=(w, h)),
            Transform(Solid(fill), xpos=1, ypos=1, xysize=(w-2, h-2)),
            xysize=(w, h+3))

    def r13_inn_guide_available():
        return bool(R13_INN_GUIDE) and store.room13.get("location") in ("inn", "hall") and renpy.loadable(R13_INN_GUIDE.get("base", ""))

    def r13_inn_guide_labels():
        """Labels on the guide, gated by the same rules as travel."""
        places = set(r13_places())
        links = dict(r13_local_connections())
        here = store.room13.get("location")
        sx = R13_INN_GUIDE_SIZE[0]/float(R13_INN_GUIDE["width"])
        sy = R13_INN_GUIDE_SIZE[1]/float(R13_INN_GUIDE["height"])
        result = []
        for label in R13_INN_GUIDE.get("labels", []):
            key = label["locationId"]
            text = label["text"]
            target = None
            state = "plain"
            if key == "guestroom" and key not in places:
                continue  # existing rule: only after the family room is unusable
            if key in R13_INN_LOCATIONS:
                if key == here:
                    text, state = "● " + text, "here"
                elif key in links:
                    target, state = key, "link"
                elif key not in places:
                    text, state = text + " · 잠김", "locked"
            elif key == "entrance" and "outside" in links:
                target, state = "outside", "link"
            size = max(17, int(label["fontSize"]*sx))
            result.append(dict(text=text, x=int(label["x"]*sx), y=int(label["y"]*sy), size=size, target=target, state=state, key=key))
        return result

    def r13_inn_guide_close():
        renpy.hide_screen("r13_inn_guide")
        try:
            renpy.set_focus("r13_hub", "r13_inn_guide_button")
        except Exception:
            pass
        renpy.restart_interaction()

screen r13_inn_v4_world_chips(ready=False):
    for key, label, (x, y, w, h), active in r13_inn_v4_chips(room13["location"], world=True):
        button:
            id ("r13_inn_v4_"+key)
            area (x, y, w, h+3) padding (0, 0)
            background r13_inn_v4_chip_background(w, h, locked=not active)
            hover_background r13_inn_v4_chip_background(w, h, True)
            insensitive_background r13_inn_v4_chip_background(w, h, locked=True)
            action Return(("travel", key)) sensitive (ready and active)
            alt label
            text label size 23 color "#f6e8cc" hover_color "#ffffff" insensitive_color "#c9bda8" xalign .5 ypos (h//2) yanchor .5

screen r13_inn_v4_screen_chips(ready=False):
    for key, label, (x, y, w, h), active in r13_inn_v4_chips(room13["location"], world=False):
        button:
            id ("r13_inn_v4_"+key)
            area (x, y, w, h+3) padding (0, 0)
            background r13_inn_v4_chip_background(w, h, locked=not active)
            hover_background r13_inn_v4_chip_background(w, h, True)
            insensitive_background r13_inn_v4_chip_background(w, h, locked=True)
            action Return(("travel", key)) sensitive (ready and active)
            alt label
            text label size 23 color "#f6e8cc" hover_color "#ffffff" insensitive_color "#c9bda8" xalign .5 ypos (h//2) yanchor .5

# Supplementary guest wayfinding drawing: not a scene, not a floor plan.
screen r13_inn_guide():
    modal True
    zorder 70
    style_prefix "r13"
    key "game_menu" action Function(r13_inn_guide_close)
    add Solid("#0b1418d8")
    $ gx, gy = (1280-R13_INN_GUIDE_SIZE[0])//2, 34
    add Transform(R13_INN_GUIDE["base"], size=R13_INN_GUIDE_SIZE) xpos gx ypos gy
    for item in r13_inn_guide_labels():
        if item["target"]:
            textbutton item["text"]:
                id ("r13_inn_guide_"+item["key"])
                xpos (gx+item["x"]) ypos (gy+item["y"]) xanchor .5 yanchor .5
                padding (10, 4)
                background Solid("#f3e6c8d0") hover_background Solid("#ffe7a8")
                text_size item["size"] text_color "#4a2f1c" text_hover_color "#2a160a"
                action [Hide("r13_inn_guide"), Return(("travel", item["target"]))]
                alt (item["text"]+" · 이동")
        else:
            frame:
                xpos (gx+item["x"]) ypos (gy+item["y"]) xanchor .5 yanchor .5
                padding (8, 2)
                background (Solid("#2c221bd0") if item["state"]=="here" else None)
                text item["text"] size item["size"] color ("#f6e8cc" if item["state"]=="here" else "#7d6a55" if item["state"]=="locked" else "#4a2f1c")
    text "보조 안내도 · 이동 조건은 장면의 이동 버튼과 같습니다":
        xalign .5 ypos 712 yanchor 1.0 size 19 color "#e6dcc6"
    textbutton "닫기":
        id "r13_inn_guide_close"
        style "r13_action_button" xpos (gx+R13_INN_GUIDE_SIZE[0]-120) ypos (gy+10) xsize 110 ysize 54 text_size 22
        action Function(r13_inn_guide_close)
