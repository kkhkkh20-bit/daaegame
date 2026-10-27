# Inn lobby / upstairs hall travel chips and the supplementary inn guide (0.18.5).
# The legacy guide name now opens the shared floor-by-floor text navigation.
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
        # 0.18.59: a wide hall scrolls like the lobby. Its drawn chips take the wide
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
        return store.room13.get("location") in R13_INN_LOCATIONS

    def r13_inn_guide_labels():
        links=dict(r13_local_connections())
        return [dict(key=key,text=R13_MAP_LABELS[key],target=key if key in links else None)
            for key,point in r13_map_nodes("inn")]

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
            text ("› "+label) size r13_type("small") color "#65503b" hover_color "#493b30" insensitive_color "#82745e" xalign .5 ypos (h//2) yanchor .5

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
            text ("› "+label) size r13_type("small") color "#65503b" hover_color "#493b30" insensitive_color "#82745e" xalign .5 ypos (h//2) yanchor .5

# Saved actions keep this screen name and the local travel tuple contract.
screen r13_inn_guide():
    modal True
    zorder 70
    use r13_map(initial_region="inn",local_guide=True)
