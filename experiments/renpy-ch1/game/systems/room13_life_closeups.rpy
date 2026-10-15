# Life close-ups with visible results (owner's map-assets brief, 0.18.21).
#   One shared screen: look at a thing, pick a tool, use it on a thing. The background swaps
#   to the "after" picture only when the existing model says the action happened.
#   A delivery: the two-parcel scene of r13_delivery_inspect, drawn. Pay/bonus/time unchanged.
#   B door:     the inn front door lets in a draft; with leave, the inn's old cloth goes under it.
#               Optional, free, no evidence or money. Stays fixed for this run.
#   C meal:     the first kitchen job of a run serves the set kept aside (초롱's), then the
#               existing finish/ask choice. Later kitchen jobs skip the close-up.
# Assets: assets/room13-pixel-life-{delivery,door,meal}-{before,after}.webp (1672x941, lossless).
init 126 python:
    R13_LIFE_SCENES={
        "delivery":dict(title="까로의 수레 · 배달 짐",before="assets/room13-pixel-life-delivery-before.webp",after="assets/room13-pixel-life-delivery-after.webp",
            targets=dict(large_tag=([0.407,0.475,0.055,0.13],"큰 상자의 짐표"),small_tag=([0.642,0.56,0.045,0.13],"작은 상자의 짐표"),
                large_box=([0.225,0.295,0.425,0.48],"큰 나무 상자"),small_box=([0.585,0.46,0.195,0.3],"작은 상자"),rope=([0.73,0.68,0.18,0.23],"굵은 짐 끈"))),
        "door":dict(title="여관 현관 · 출입문",before="assets/room13-pixel-life-door-before.webp",after="assets/room13-pixel-life-door-after.webp",
            targets=dict(draft_gap=([0.19,0.6,0.48,0.07],"문 아래 틈"),door=([0.19,0.01,0.48,0.59],"출입문"),cloth=([0.69,0.655,0.3,0.25],"낡은 천"))),
        "meal":dict(title="식당 · 배식대",before="assets/room13-pixel-life-meal-before.webp",after="assets/room13-pixel-life-meal-after.webp",
            targets=dict(soup_pot=([0.12,0.245,0.29,0.235],"국 냄비"),bread_source=([0.64,0.29,0.24,0.16],"빵 쟁반"),
                fourth_bowl=([0.715,0.47,0.16,0.15],"파란 잎 무늬 그릇"),fourth_plate=([0.71,0.625,0.17,0.14],"빈 접시"))),
    }
    R13_LIFE_TOOL_NAMES={"cloth":"여관의 낡은 천"}

    def r13_life_tool_name(key):
        return R13_LIFE_TOOL_NAMES.get(key) or R13_SHOP.get(key,{}).get("title",key)

    def r13_life_rect(norm):
        x,y,w,h=norm
        return (int(x*1280),int(y*720),int(w*1280),int(h*720))

    def r13_life_door_available():
        s=store.room13 or {}
        # The leave comes from Granny at her counter; without her the door is just looked at.
        return s.get("location")=="inn" and s.get("day",1)>=2 and s.get("period",0)<3 and "granny" in r13_people()

screen r13_life_closeup(scene,after=False,tools=(),actions=(),message=""):
    modal True
    zorder 40
    style_prefix "r13"
    default selected=None
    default ready=False
    timer .25 action SetScreenVariable("ready",True)
    $ spec=R13_LIFE_SCENES[scene]
    add Transform(spec["after"] if after else spec["before"],xysize=(1280,720),nearest=True)
    for key,(norm,name) in spec["targets"].items():
        button:
            area r13_life_rect(norm) padding (0,0) background None hover_background R13HoverCorners()
            action Return(("use",selected,key) if selected else ("look",key)) sensitive ready
            tooltip name alt name
    frame:
        area (16,14,1248,68) padding (18,10) background R13ActionPanel()
        hbox:
            spacing 20
            text spec["title"] size 27 color "#fff2cf" yalign .5 xsize 420
            text ("사용 중: "+r13_life_tool_name(selected) if selected else "물건을 눌러 살펴보기") size 21 color "#d9bc80" yalign .5 xsize 380
            if selected:
                textbutton "선택 해제" style "r13_action_button" text_size 19 xsize 155 ysize 46 action SetScreenVariable("selected",None)
    $ hint=GetTooltip()
    if hint:
        frame:
            xpos 24 ypos 518 padding (12,7) background R13ActionPanel()
            text hint size 20 color "#fff2cf"
    frame:
        area (16,564,1248,80) padding (18,12) background R13ActionPanel()
        text message size 22 color "#fff2cf" xsize 1200
    frame:
        area (16,652,1248,60) padding (14,4) background R13ActionPanel()
        hbox:
            spacing 12
            text "쓸 물건" size 21 color "#d9bc80" yalign .5 xsize 100
            for key in tools:
                textbutton r13_life_tool_name(key):
                    style "r13_action_button" text_size 21 xsize 222 ysize 52
                    background (Solid("#675635") if selected==key else R13ActionPanel())
                    action SetScreenVariable("selected",None if selected==key else key) sensitive ready
            if not tools:
                text "지금 쓸 수 있는 물건이 없다." size 21 color "#c1c9c2" yalign .5
    vbox:
        xpos 1250 xanchor 1.0 ypos 96 spacing 8
        for value,title in actions:
            textbutton title:
                style "r13_action_button" text_size 21 xmaximum 560 padding (16,10)
                action Return(("action",value)) sensitive ready
    if selected:
        key "game_menu" action SetScreenVariable("selected",None)

# ---- A: delivery (replaces the menu of r13_delivery_inspect; same outcomes) ----
label r13_delivery_inspect:
    $ _dv_tied=False
    $ _dv_msg="까로가 수레 옆에 짐 두 개를 내려 두었다."
    while True:
        $ _w=r13_wallet(room13)
        $ _dv_cord=("cord" in _w["items"]) or ("karo_trusted" in _w["relations"])
        # Every owned item can be tried (as before); 까로's cord joins once he offered it.
        $ _dv_tools=() if _dv_tied else tuple(dict.fromkeys(list(_w["items"])+(["cord"] if _dv_cord else [])))
        call screen r13_life_closeup("delivery",after=_dv_tied,tools=_dv_tools,
            actions=[("ask",r13_job_question),("go","짐을 나르러 간다")],message=_dv_msg)
        $ _kind=_return[0];_a=_return[1];_b=_return[2] if len(_return)>2 else None
        if _kind=="action":
            if _a=="ask":
                $ r13_job_choice="ask"
            else:
                $ r13_job_choice="finish"
                if _dv_tied and not r13_wallet(room13)["combined_paid"]:
                    # Tying the two boxes is what shows they go to the same house in one trip.
                    python:
                        _w=r13_wallet(room13);_w["relations"]=list(dict.fromkeys(_w["relations"]+["same_lane"]))
                        if "cord" not in _w["items"]:_w["relations"]=list(dict.fromkeys(_w["relations"]+["karo_trusted"]))
                        r13_edit(livelihood=_w)
                    $ r13_job_choice="combine"
            return
        if _kind=="look":
            if _a=="large_tag":
                $ _dv_msg="큰 상자 짐표 · 받는 곳: 광장 뒤 세 번째 집, 솔 씨 댁. 큰 나무 상자."
            elif _a=="small_tag":
                $ _dv_msg="작은 상자 짐표 · 받는 곳: 광장 뒤 세 번째 집, 솔 씨 댁. 작은 상자. 바닥이 매끈하다."
            elif _a=="small_box" and not _dv_tied:
                $ _dv_msg="큰 상자 위에 작은 상자를 얹어 보았다. 수레가 기울 때마다 작은 상자가 미끄러졌다. 까로: “위에 올리면 작은 게 자꾸 떨어져요.”"
            elif _a=="rope":
                $ _dv_msg=("굵은 짐 끈이다. 아래쪽 쓸 물건에서 고른 뒤 상자를 누르면 쓸 수 있다." if _dv_cord and not _dv_tied else "까로의 수레에 걸려 있던 굵은 끈이다. 까로가 허락하기 전에는 함부로 쓰지 않는다." if not _dv_tied else "끈은 두 상자를 감고 있다.")
            elif _dv_tied:
                $ _dv_msg="두 상자가 끈으로 함께 묶여 있다. 수레가 기울어도 움직이지 않는다."
            else:
                $ _dv_msg="큰 나무 상자다. 바닥이 넓고 무겁다."
        elif _kind=="use":
            if _a=="cord" and _b in ("small_box","large_box") and not _dv_tied:
                $ source_fx("impact")
                $ _dv_tied=True
                $ _dv_msg="작은 상자를 큰 상자 위에 올리고 굵은 끈으로 함께 묶었다. 까로: “이렇게 실으면 한 번에 되겠네요.”"
            elif _b in ("small_box","large_box") and not _dv_tied:
                $ _dv_msg="상자를 고정할 수 없다. 물건은 그대로 두었다."
            else:
                $ _dv_msg="여기에는 쓸 데가 없다. 물건은 그대로 두었다."
    return

# ---- B: the inn front door ----
label r13_life_door:
    $ _dr_sealed=r13_has("inn_draft_sealed")
    $ _dr_msg=("문 밑에 천이 덧대어 있다. 문은 그대로 여닫을 수 있다." if _dr_sealed else "여관 현관이다. 난로 쪽은 따뜻한데 문 근처만 유난히 춥다.")
    while True:
        $ _dr_tools=("cloth",) if r13_has("inn_cloth_leave") and not _dr_sealed else ()
        call screen r13_life_closeup("door",after=_dr_sealed,tools=_dr_tools,actions=[("back","돌아간다")],message=_dr_msg)
        if _return[0]=="action":
            return
        if _return[0]=="look":
            $ _t=_return[1]
            if _t=="draft_gap":
                $ _dr_msg=("틈이 천으로 덮였다. 들어오던 바람이 줄었다." if _dr_sealed else "문 아래 틈으로 푸르스름한 바깥빛이 보인다. 찬 바람에 작은 눈 알갱이가 안으로 굴러 들어온다.")
            elif _t=="door":
                $ _dr_msg="두꺼운 나무문이다. 문짝은 맞게 닫히는데, 아래쪽만 바닥에서 한 뼘쯤 떠 있다."
            elif _t=="cloth" and not _dr_sealed:
                if r13_has("inn_cloth_leave"):
                    $ _dr_msg="여관의 낡은 천이다. 문 폭만큼 길고 두툼하다. 아래쪽 쓸 물건에서 고를 수 있다."
                else:
                    call r13_lines([("dad","현관 바닥에 둔 이 낡은 천, 잠깐 써도 되겠습니까?"),
                        ("granny","그거요? 버리려던 거예요. 쓰세요.")],"life:door:leave")
                    $ r13_flag("inn_cloth_leave")
                    $ _dr_msg="허락을 받았다. 문 폭만큼 길고 두툼한 천이다."
            else:
                $ _dr_msg="천이 문 밑에 덧대어 있다."
        else:
            if _return[1]=="cloth" and _return[2] in ("draft_gap","door") and not _dr_sealed:
                $ r13_flag("inn_draft_sealed")
                $ _dr_sealed=True
                call r13_lines([(None,"천을 길게 말아 문 아래 틈에 대었다. 문을 열어 보니 천이 함께 밀렸다가 제자리로 돌아왔다."),
                    ("granny","어머, 발밑이 덜 시리네요. 고마워요.")],"life:door:sealed")
                $ _dr_msg="문 밑 틈이 천으로 덮였다. 들어오던 바람이 줄었다."
            else:
                $ _dr_msg="거기에는 쓸 데가 없다. 천은 그대로 두었다."
    return

# ---- C: the first kitchen job of the run ----
label r13_life_meal:
    $ _ml_served=False
    $ _ml_msg="나비: “이 한 벌은 따로 놓아 줘요.” 세 자리는 차려졌고, 오른쪽 파란 잎 무늬 자리만 비어 있다."
    while True:
        call screen r13_life_closeup("meal",after=_ml_served,actions=([("finish","맡은 일만 마친다"),("ask",r13_job_question)] if _ml_served else []),message=_ml_msg)
        if _return[0]=="action":
            $ r13_job_choice=_return[1]
            $ r13_flag("life_meal_served")
            return
        $ _t=_return[1]
        if _t in ("fourth_bowl","fourth_plate") and not _ml_served:
            $ _ml_served=True
            $ _ml_msg="파란 잎 무늬 그릇에 국을 뜨고, 쟁반의 빵 하나를 옆 접시에 옮겼다. 쟁반에는 빵이 하나 남았다."
        elif _t=="soup_pot":
            $ _ml_msg="국 냄비다. 한 그릇 분량이 남아 있다." if not _ml_served else "국 냄비다. 바닥이 보인다."
        elif _t=="bread_source":
            $ _ml_msg=("쟁반에 빵이 두 개 있다." if not _ml_served else "쟁반에 빵이 하나 남았다.")
        else:
            $ _ml_msg="이 자리는 차려졌다."
    return
