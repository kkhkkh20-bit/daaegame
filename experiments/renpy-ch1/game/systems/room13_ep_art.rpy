# 0.18.89 에피소드 그림 연결 (그림 원본: art/ep-art-20261016, 변환: dev/apply_ep_art.py)
#
# - 장면 배경: 에피소드 장소의 새 배경 키(ep_*). 지금까지 비슷한 장소 그림을 빌려 쓰던 곳이다.
# - 현장 겹침: 학교·진료소·숲·옛 시설·제단·광장 그림 위에, 그 일이 일어난 뒤에만 물건을 얹는다.
# - 그림책과 장면 컷: 대사 줄의 {"book": ...} / {"cut": ...}로 띄운다. 그 대사 묶음이 끝나면 내려간다.
# 이야기·조건·대사는 바꾸지 않는다. 그림만 고른다.
init 160 python:
    # key: file, or {daylight: file}. 2048x768 panorama -> 1920x720, 2172x724 wide -> 2160x720,
    # shown through a 1280 window at the x below (default: centre).
    R13_EP_BACKGROUNDS = {
        "ep_roof_evening":"room13-pixel-panorama-roof-evening.webp",
        "ep_roof_night":"room13-pixel-panorama-roof-night.webp",
        "ep_somi_home":"room13-pixel-wide-somi-home-afternoon.webp",
        "ep_woodshed_intact":"room13-pixel-panorama-woodshed-intact.webp",
        "ep_woodshed_fire":"room13-pixel-panorama-woodshed-fire.webp",
        "ep_woodshed_ruin":"room13-pixel-panorama-woodshed-ruin.webp",
        "ep_hideout":"room13-pixel-wide-hideout-afternoon.webp",
        "ep_laundry":{"morning":"room13-pixel-panorama-laundry-afternoon.webp","afternoon":"room13-pixel-panorama-laundry-afternoon.webp","evening":"room13-pixel-panorama-laundry-evening.webp"},
        "ep_belltower_night":"room13-pixel-panorama-belltower-night.webp",
        "ep_eaves":"room13-pixel-panorama-eaves-afternoon.webp",
        "ep_hall_front":"room13-pixel-panorama-hall-front-afternoon.webp",
        "ep_holding_morning":"room13-pixel-panorama-holding-morning.webp",
        "ep_holding_night":"room13-pixel-panorama-holding-night.webp",
        "ep_stable":"room13-pixel-wide-stable-afternoon.webp",
        "ep_hall_cell":"room13-pixel-wide-hall-cell-evening.webp",
        "ep_square_spring":"room13-pixel-panorama-square-spring.webp",
    }
    # Window x on the scaled picture where the centre would cut the subject.
    R13_EP_BACKGROUND_X = {"ep_woodshed_intact":560,"ep_woodshed_fire":560,"ep_woodshed_ruin":560,"ep_holding_morning":200,"ep_holding_night":200}

    def r13_ep_background_file(key):
        value=R13_EP_BACKGROUNDS[key]
        if isinstance(value,dict):
            value=value.get(r13_daylight()) or value["afternoon"]
        return "assets/"+value

    def r13_ep_background(key):
        path=r13_ep_background_file(key)
        width=2160 if "-wide-" in path else 1920
        x=R13_EP_BACKGROUND_X.get(key,(width-1280)//2)
        return Crop((x,0,1280,720),Transform(path,size=(width,720),nearest=True,subpixel=False))

    _r13_ep_art_background=r13_background
    def r13_background(key):
        if key in R13_EP_BACKGROUNDS:return r13_ep_background(key)
        return _r13_ep_art_background(key)

    # Scene overlays: same size as the place's picture, drawn only in these states.
    def _r13_ep_day():
        return (store.room13 or {}).get("day",0)

    def _r13_ep_soup_evening():
        return r13_has("ws_soup") and _r13_ep_day()==R13_WEEK2_DAY+1

    R13_EP_OVERLAYS = {
        "school":(
            ("room13-ep-O38-shelter-full.webp",lambda:(r13_has("ws_long_night") or r13_has("ws_tents_school") or r13_has("shelter_ready")) and not _r13_ep_soup_evening() and not r13_has("soup_kids_dead")),
            ("room13-ep-O42-evac-list.webp",lambda:r13_has("ws_long_night") and not r13_has("cv_done")),
            ("room13-ep-O39-two-pots.webp",lambda:_r13_ep_soup_evening() and not r13_has("dodam_sick") and not r13_has("soup_kids_dead")),
            ("room13-ep-O40-spilled.webp",lambda:r13_has("dodam_sick") and _r13_ep_day()==R13_WEEK2_DAY+1),
            ("room13-ep-O41-four-blankets.webp",lambda:r13_has("soup_kids_dead") and _r13_ep_day()<=R13_WEEK2_DAY+2),
        ),
        "clinic":(("room13-ep-O43-cabinet-gap.webp",lambda:_r13_ep_day()>=R13_WEEK2_DAY+1 and r13_has("ws_teacher_talked") and not r13_has("ws_cabinet_locked")),),
        "forest":(("room13-ep-O44-hideout-empty.webp",lambda:r13_has("Y02")),),
        "ancient":(("room13-ep-O45-ancient-shelf.webp",lambda:r13_has("ws_lab")),),
        "altar":(
            ("room13-ep-O47-handprints.webp",lambda:True),
            ("room13-ep-O46-mountain-ropes.webp",lambda:r13_has("cart_left")),
            ("room13-ep-O48-chisel.webp",lambda:r13_has("cart_left")),
        ),
        "square":(
            ("room13-ep-O49-cart.webp",lambda:_r13_ep_day()==R13_WEEK2_DAY+2 and not r13_has("cart_left")),
            ("room13-ep-O50-cart-list.webp",lambda:_r13_ep_day()>=R13_WEEK2_DAY+2),
        ),
    }

    def r13_ep_overlays(location):
        if not store.room13:return []
        return ["assets/"+file for file,shown in R13_EP_OVERLAYS.get(location,()) if shown()]

    _r13_ep_art_world_background=r13_world_background
    def r13_world_background(location=None,daylight=None):
        base=_r13_ep_art_world_background(location,daylight)
        location=location or store.room13["location"]
        files=r13_ep_overlays(location)
        if not files:return base
        spec=R13_WORLD_LAYOUTS[location]
        crop=spec.get("crops",{}).get(daylight or r13_daylight())
        width=int(spec["width"])
        layers=[Transform(Crop(tuple(crop),f) if crop else f,size=(width,720),nearest=True,subpixel=False) for f in files]
        return Fixed(base,*layers,xysize=(width,720))

    # Picture books (U00 frame + a 3:2 panel on the left page) and full-screen cuts.
    R13_EP_BOOK_PANEL = (133,60,480,320)

    def r13_ep_book_art(name):
        x,y,w,h=R13_EP_BOOK_PANEL
        return Fixed(Transform("assets/room13-ep-U00-open-book.webp",size=(1280,720),nearest=True),
            Transform("assets/room13-ep-%s.webp"%name,size=(w,h),xpos=x,ypos=y,nearest=True),xysize=(1280,720))

    def r13_ep_cut_art(name):
        if name=="bell":return r13_ep_bell_art()
        return Transform("assets/room13-ep-%s.webp"%name,size=(1280,720),nearest=True)

    def r13_ep_line_art(packet):
        options=packet[2] if len(packet)>2 and isinstance(packet[2],dict) else {}
        if "book" in options:
            if options["book"]:renpy.show("r13_ep_book",what=At(r13_ep_book_art(options["book"]),r13_ep_art_fade),zorder=0)
            else:renpy.hide("r13_ep_book")
        if "cut" in options:
            if options["cut"]:renpy.show("r13_ep_cut",what=At(r13_ep_cut_art(options["cut"]),r13_ep_art_fade),zorder=5)
            else:renpy.hide("r13_ep_cut")
        # 0.18.91 연출: 줄마다 음악 끄기/바꾸기, 효과음, 화면 어둡게(그 대화가 끝날 때까지).
        if "music" in options:
            if options["music"]:renpy.music.play(R13_BGM[options["music"]],fadeout=1.0,fadein=1.0)
            else:renpy.music.stop(fadeout=1.5)
        if options.get("sfx"):source_fx(options["sfx"])
        if "dim" in options:
            if options["dim"]:renpy.show("r13_ep_dim",what=At(Solid("#05080cb0"),r13_ep_art_fade),zorder=4)
            else:renpy.hide("r13_ep_dim")

    def r13_ep_line_art_clear():
        renpy.hide("r13_ep_book")
        renpy.hide("r13_ep_cut")
        renpy.hide("r13_ep_dim")

transform r13_ep_art_fade:
    alpha 0.0
    linear .25 alpha 1.0

# The bell over the roofs (⑥ 13일 밤): three swing frames and sound waves over the night roofs
# (the belltower picture has its own bell, so it is not the backdrop here).
image r13_ep_bell_swing:
    "assets/room13-ep-U21-bell-01.webp"
    pause .22
    "assets/room13-ep-U21-bell-02.webp"
    pause .22
    "assets/room13-ep-U21-bell-01.webp"
    pause .22
    "assets/room13-ep-U21-bell-03.webp"
    pause .22
    repeat

transform r13_ep_wave_pulse:
    alpha 0.0
    linear .5 alpha .9
    linear .9 alpha 0.0
    repeat

init 161 python:
    def r13_ep_bell_art():
        return Fixed(r13_ep_background("ep_roof_night"),
            Transform("r13_ep_bell_swing",size=(256,384),xpos=512,ypos=40,nearest=True),
            At(Transform("assets/room13-ep-U21-soundwaves.webp",size=(1280,480),xpos=0,ypos=0,nearest=True),r13_ep_wave_pulse),
            xysize=(1280,720))
