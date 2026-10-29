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
        if globals().get("r13_v111_active",lambda:False)():
            location=store.room13["location"]
            if r13_layout(location) and R13_PLACES.get(location,(None,None))[1]==key:
                return DynamicDisplayable(r13_camera_background,location,r13_daylight())
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

    R13_EV_CUT_BOX=(1032,104,220)
    # 2026-10-28 소유자 「어두운 바탕에 다른 테두리, 도트 느낌이 없어져서 어색」: 매끈한 사각 테두리 대신 도트 한 칸(4px) 단위의
    # 띠를 겹치고 모서리를 계단으로 깎는다. 띠는 바깥부터 차례로 그린다.
    R13_EV_CUT_PX=4
    R13_EV_CUT_FRAMES=dict(
        cream=("#14171d","#EFE3C6","#14171d","#2E3138"),
        brass=("#14171d","#E3C072","#9A7432","#2E3138"),
    )
    R13_EV_CUT_FRAME="brass"   # 소유자 10-28 「놋쇠선 좋다」
    def r13_ev_pixel_frame(x,y,side,frame):
        u=R13_EV_CUT_PX;parts=[]
        for n,color in enumerate(R13_EV_CUT_FRAMES[frame]):
            o=n*u;w=side-2*o
            # 가로 띠는 양 끝 한 칸, 세로 띠는 위아래 한 칸을 비워 모서리가 계단처럼 깎인다
            parts.append(Solid(color,xysize=(w-2*u,w),xpos=x+o+u,ypos=y+o))
            parts.append(Solid(color,xysize=(w,w-2*u),xpos=x+o,ypos=y+o+u))
        return Fixed(*parts,xysize=(1280,720))
    def r13_ev_pixel_panel(w,h,frame=None):
        """증거 칸과 같은 놋쇠 도트 틀을 (0,0)부터 w x h 로. 자료 알림 카드가 쓴다."""
        u=R13_EV_CUT_PX;parts=[]
        for n,color in enumerate(R13_EV_CUT_FRAMES[frame or R13_EV_CUT_FRAME]):
            o=n*u;ww=w-2*o;hh=h-2*o
            parts.append(Solid(color,xysize=(ww-2*u,hh),xpos=o+u,ypos=o))
            parts.append(Solid(color,xysize=(ww,hh-2*u),xpos=o,ypos=o+u))
        return Fixed(*parts,xysize=(w,h))
    def r13_ep_cut_art(name):
        if name=="bell":return r13_ep_bell_art()
        if name in ("v111_reunion_far","v111_reunion_close"):
            # 0.20.7 (owner days 2-14 #4): the reunion is the distance between the two, so both stand
            # in one frame: apart at the doorway, then together when Daram takes the coat.
            far=name.endswith("far")
            mom=r13_fullbody_close_art("mom","anxious",620) or Null()
            daram=r13_fullbody_close_art("daram","distressed",470) or Null()
            # Mom first, Daram in front of her coat when they are together.
            return Fixed(Transform(mom,xanchor=.5,xpos=(1010 if far else 760),yanchor=1.0,ypos=730),
                Transform(daram,xanchor=.5,xpos=(250 if far else 590),yanchor=1.0,ypos=730),xysize=(1280,720))
        if name.startswith("ev:"):
            # 0.20.7: a record's own picture held up above the dialogue (same art as the 자료 view).
            # To the right of the speaker's face, above the dialogue.
            # 2026-10-28 소유자 「증거 네모칸이 좌우 길이가 달라서 사이즈를 고정, 정사각형으로, 이미지만 떠도 된다, 겹치면 안 된다」
            # (역전재판 증거 칸) → 시안 B(오른쪽 위), 「테두리가 확실히 있어야 해」. 판은 늘 같은 정사각형이고 그림은 그 안에
            # 비율대로 들어간다. 날짜판 아래 오른쪽 구석이라 1.55배 인물과 겹치지 않는다. 바탕은 어둡게, 테두리는 도트 띠(r13_ev_pixel_frame).
            x,y,side=R13_EV_CUT_BOX
            u=R13_EV_CUT_PX;inner=side-2*5*u
            return Fixed(r13_ev_pixel_frame(x,y,side,R13_EV_CUT_FRAME),
                Transform("assets/evidence/%s.webp"%name[3:],xysize=(inner,inner),fit="contain",nearest=True,xpos=x+side//2,xanchor=.5,ypos=y+side//2,yanchor=.5),xysize=(1280,720))
        if name in ("v111_blanket_before","v111_blanket_after"):
            # Existing cut layer/clear lifecycle, preserving the actual school
            # background and the same prop position across the repair beat.
            state="before" if name.endswith("before") else "after"
            # 2026-10-28 캡처 검수(13일 담요 수선): 370x310 그림이 (770,150)에 떠서 1.55배 인물 머리 옆 공중에 걸렸다.
            # 증거 칸과 같은 자리·같은 놋쇠 도트 틀에 넣는다(소유자 「이미지가 겹치면 안 된다」).
            x,y,side=R13_EV_CUT_BOX
            u=R13_EV_CUT_PX;inner=side-2*5*u
            return Fixed(r13_ev_pixel_frame(x,y,side,R13_EV_CUT_FRAME),
                Transform("assets/room13-v111-blanket-%s.webp"%state,xysize=(inner,inner),fit="contain",nearest=True,xpos=x+side//2,xanchor=.5,ypos=y+side//2,yanchor=.5),xysize=(1280,720))
        return Transform("assets/room13-ep-%s.webp"%name,size=(1280,720),nearest=True)

    def r13_ep_line_art(packet):
        options=packet[2] if len(packet)>2 and isinstance(packet[2],dict) else {}
        # 선택창 동안 감춘 증거 칸은 다음 대사에서 되살린다(선택창이 닫힐 때 hide 알림이 늘 오지는 않는다).
        if globals().get("r13_ep_cut_suspended") and "cut" not in options:r13_ep_cut_resume()
        # The illustrated opening ends when Tosil speaks holding the physical book.
        # A later explicit book cue still opens its own illustration normally.
        if packet[0]=="resident_tosil" and options.get("pose")=="hold_storybook" and "book" not in options:
            renpy.hide("r13_ep_book")
        if "book" in options:
            if options["book"]:renpy.show("r13_ep_book",what=At(r13_ep_book_art(options["book"]),r13_ep_art_fade),zorder=0)
            else:renpy.hide("r13_ep_book")
        if "cut" in options:
            globals()["r13_ep_cut_current"]=options["cut"] or None
            if options["cut"]:
                renpy.show("r13_ep_cut",what=At(r13_ep_cut_art(options["cut"]),r13_ep_art_fade),zorder=5)
                # 2026-10-28 소유자 「증거 나올 때 효과음, 휘익이든 따단이든」: 증거 칸이 뜰 때 자료를 얻을 때와 같은 「따단」.
                # 그 줄에 따로 효과음이 적혀 있으면(아래 sfx) 그쪽이 이긴다.
                if str(options["cut"]).startswith("ev:") and not options.get("sfx"):source_fx("found")
            else:renpy.hide("r13_ep_cut")
        # 0.18.91 연출: 줄마다 음악 끄기/바꾸기, 효과음, 화면 어둡게(그 대화가 끝날 때까지).
        if "music" in options:
            if options["music"]:renpy.music.play(R13_BGM[options["music"]],fadeout=1.0,fadein=1.0)
            else:renpy.music.stop(fadeout=1.5)
        if options.get("sfx"):source_fx(options["sfx"])
        if options.get("carriage_jolt") and store.place=="마차 안":r13_carriage_jolt()
        if "carriage_letter" in options and store.place=="마차 안":
            if options["carriage_letter"]:renpy.show_screen("r13_evidence_card", "E01", "가져온 편지", conversation=True, _zorder=85)
            else:renpy.hide_screen("r13_evidence_card")
        if options.get("carriage_reveal") and store.place=="마차 안":
            store.r13_carriage_narrow=False; renpy.show("r13_carriage_background", what=r13_background("winter_carriage"), zorder=-10)
        if "dim" in options:
            if options["dim"]:renpy.show("r13_ep_dim",what=At(Solid("#05080cb0"),r13_ep_art_fade),zorder=4)
            else:renpy.hide("r13_ep_dim")

    def r13_ep_line_art_clear():
        renpy.hide("r13_ep_book")
        renpy.hide("r13_ep_cut")
        store.r13_ep_cut_current=None;store.r13_ep_cut_suspended=None
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

# 0.20.10 (4~14일 리뷰 6일): 식은 창고 터 그림은 예전 이야기의 아침용이다. 새 이야기에서는 같은 날 저녁이라
# 밤빛 화재 뒤 하늘이 다시 밝아 보였다. 저녁·밤에는 그림을 저녁빛으로 물들인다.
init 162 python:
    _r13_v111_ruin_bg=r13_ep_background
    def r13_ep_background(key):
        image=_r13_v111_ruin_bg(key)
        state=getattr(store,"room13",None) or {}
        if key=="ep_woodshed_ruin" and state.get("v111") and state.get("period",0)>=2:
            return Transform(image,matrixcolor=TintMatrix("#9a8cb0")*BrightnessMatrix(-0.12))
        return image
    # 2026-10-28 캡처 검수(진엔딩 길 6일 저녁): 위 물들임은 장면 그림(r13_scene) 경로에만 걸려, 현장 화면(지도에서 들어가는
    # 「식은 장작 창고 터」)은 날짜판이 저녁인데 한낮 그림으로 나왔다. 바로 앞 「장작 창고 바깥」이 저녁 그림이라 시간이
    # 거꾸로 간 것처럼 보였다. 현장 배경에도 같은 저녁빛을 입힌다.
    _r13_v111_ruin_world=r13_world_background
    def r13_world_background(location=None,daylight=None):
        image=_r13_v111_ruin_world(location,daylight)
        state=getattr(store,"room13",None) or {}
        if (location or state.get("location"))=="v111_ruin" and state.get("v111") and state.get("period",0)>=2:
            return Transform(image,matrixcolor=TintMatrix("#9a8cb0")*BrightnessMatrix(-0.12))
        return image

    # 2026-10-28 캡처 검수(12일 배식 선택): 오른쪽 위 증거 칸이 선택지 목록과 겹쳤다(소유자 「이미지가 겹치면 안 된다」).
    # 증거 칸은 선택창이 열려 있는 동안만 감추고, 닫히면 같은 그림을 다시 띄운다(효과음 없이).
    def r13_ep_cut_suspend():
        cut=getattr(store,"r13_ep_cut_current",None)
        if cut and str(cut).startswith("ev:") and renpy.showing("r13_ep_cut"):
            store.r13_ep_cut_suspended=cut
            renpy.hide("r13_ep_cut")
    def r13_ep_cut_resume():
        cut=getattr(store,"r13_ep_cut_suspended",None)
        store.r13_ep_cut_suspended=None
        if cut and getattr(store,"r13_ep_cut_current",None)==cut:
            renpy.show("r13_ep_cut",what=r13_ep_cut_art(cut),zorder=5)

default r13_ep_cut_current = None
default r13_ep_cut_suspended = None
