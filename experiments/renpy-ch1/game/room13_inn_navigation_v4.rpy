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
    R13_INN_V4_CHIP_HEIGHT = 58
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
        # 0.18.58: a wide hall scrolls like the lobby. Its drawn chips take the wide
        # picture's own centres (world layout "chips"); edge chips stay screen UI.
        wide = location != "inn" and r13_world_width(location) > 1280
        centres = r13_layout(location).get("chips", {}) if wide else {}
        panorama = location == "inn" or wide
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
            w = max(int((x1-x0)*sx)+16, 26*len(label)//2+68)
            h = R13_INN_V4_CHIP_HEIGHT
            if on_picture:
                if wide:
                    cx, cy = centres[key]
                x, y = int(cx-w/2), int(cy-h/2)
            else:
                width = 1920.0 if location == "inn" else 1280.0
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
        fill = "#cdbd9e" if locked else "#f4e3bf" if hover else "#ead4a9"
        border = "#a38e6e" if locked else "#8e6635" if hover else "#92764e"
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

    def r13_inn_guide_rooms():
        """Room areas on the guide (screen coords) with the same state as their label (0.18.22)."""
        sx = R13_INN_GUIDE_SIZE[0]/float(R13_INN_GUIDE["width"])
        sy = R13_INN_GUIDE_SIZE[1]/float(R13_INN_GUIDE["height"])
        rooms = R13_INN_GUIDE.get("rooms", {})
        result = []
        for item in r13_inn_guide_labels():
            rect = rooms.get(item["key"])
            if not rect:
                continue
            x, y, w, h = rect
            result.append(dict(item, rect=(int(x*sx), int(y*sy), int(w*sx), int(h*sy))))
        return result

    class R13GuideRoomMark(renpy.Displayable):
        """Room overlay on the guide: hover glow for a destination, outline for 'here', shade for locked."""
        def __init__(self, w, h, state, hover=False, **kwargs):
            super(R13GuideRoomMark, self).__init__(**kwargs)
            self.w, self.h, self.state, self.hover = int(w), int(h), state, hover
        def render(self, width, height, st, at):
            w, h = self.w, self.h
            r = renpy.Render(w, h); c = r.canvas()
            if self.state == "locked":
                c.rect("#3a2c2266", (0, 0, w, h))
                for x in range(-h, w, 14):
                    c.line("#3a2c2240", (x, 0), (x+h, h), 2)
                return r
            if self.state == "here":
                c.rect("#c2502e", (0, 0, w, h), 4)
                return r
            if self.hover:
                c.rect("#ffe2904d", (0, 0, w, h))
                c.rect("#e0902e", (0, 0, w, h), 5)
            else:
                # Idle destinations show a thin dashed edge so they read as places to press.
                c.rect("#ffd27a2e", (0, 0, w, h))
                for x in range(0, w, 20):
                    c.rect("#b8641e", (x, 0, 11, 4)); c.rect("#b8641e", (x, h-4, 11, 4))
                for y in range(0, h, 20):
                    c.rect("#b8641e", (0, y, 4, 11)); c.rect("#b8641e", (w-4, y, 4, 11))
            return r

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
            text ("› "+label) size 23 color "#65503b" hover_color "#493b30" insensitive_color "#82745e" xalign .5 ypos (h//2) yanchor .5

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
            text ("› "+label) size 23 color "#65503b" hover_color "#493b30" insensitive_color "#82745e" xalign .5 ypos (h//2) yanchor .5

# Supplementary guest wayfinding drawing: not a scene, not a floor plan.
screen r13_inn_guide():
    modal True
    zorder 70
    style_prefix "r13"
    key "game_menu" action Function(r13_inn_guide_close)
    add Solid("#0b1418d8")
    $ gx, gy = (1280-R13_INN_GUIDE_SIZE[0])//2, 34
    add Transform(R13_INN_GUIDE["base"], size=R13_INN_GUIDE_SIZE) xpos gx ypos gy
    # The rooms themselves are the buttons (0.18.22, owner: text labels did not read as places).
    for room in r13_inn_guide_rooms():
        $ rx, ry, rw, rh = room["rect"]
        if room["target"]:
            button:
                id ("r13_inn_guide_room_"+room["key"])
                area (gx+rx, gy+ry, rw, rh) padding (0, 0)
                background R13GuideRoomMark(rw, rh, "link") hover_background R13GuideRoomMark(rw, rh, "link", True)
                action [Hide("r13_inn_guide"), Return(("travel", room["target"]))]
                tooltip (room["text"]+"(으)로 이동") alt (room["text"]+" · 이동")
        else:
            add R13GuideRoomMark(rw, rh, room["state"]) xpos (gx+rx) ypos (gy+ry)
            if room["state"]=="here":
                frame:
                    xpos (gx+rx+8) ypos (gy+ry+8) padding (8, 3) background Solid("#c2502e")
                    text "현재 위치" size 16 color "#fff4e0"
    for item in r13_inn_guide_labels():
        if item["target"] and item["key"] not in R13_INN_GUIDE.get("rooms", {}):
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
                background (Solid("#2c221bd0") if item["state"]=="here" else Solid("#f3e6c8b0") if item["state"]=="link" else None)
                text item["text"] size item["size"] color ("#f6e8cc" if item["state"]=="here" else "#7d6a55" if item["state"]=="locked" else "#4a2f1c")
    $ guide_hint=GetTooltip()
    text (guide_hint or "가고 싶은 방을 누르세요 · 이동 조건은 장면의 이동 버튼과 같습니다"):
        xalign .5 ypos 712 yanchor 1.0 size 19 color "#e6dcc6"
    textbutton "닫기":
        id "r13_inn_guide_close"
        style "r13_action_button" xpos (gx+R13_INN_GUIDE_SIZE[0]-120) ypos (gy+10) xsize 110 ysize 54 text_size 22
        action Function(r13_inn_guide_close)
