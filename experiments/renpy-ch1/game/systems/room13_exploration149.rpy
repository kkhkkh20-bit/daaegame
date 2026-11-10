# 시장에서 구한 물건과 현장에서 배운 방법을 다른 조사에 쓴다.
# 원래 사건 정답·생사 판정은 기존 본편 라벨이 처리한다.
default r13_ex149_held = None
default r13_ex149_scale_on_pan = False

init 390 python:
    with renpy.file("v111/exploration149.json") as _ex149_file:
        R13_EX149_BLOCKS=json.load(_ex149_file)["blocks"]
    R13_EX149_REQUIRED={"market_intro","delivery_intro","delivery_large_tag","delivery_small_tag","delivery_box","delivery_need_read","delivery_tie","delivery_taught","delivery_repeat","delivery_unbound","delivery_separate","scale_intro","scale_reference","scale_place","scale_pivot","scale_need_check","scale_eunho","scale_repeat","scale_pack","lamp_method","lamp_need_method","wrong_target","need_item","receive_cord","receive_weight","return_weight"}
    if not R13_EX149_REQUIRED<=set(R13_EX149_BLOCKS):raise Exception("선택 탐색 대화 단계 누락")
    _ex149_ids=set()
    for _ex149_key,_ex149_rows in R13_EX149_BLOCKS.items():
        _ex149_cast={None,"아빠"}
        if _ex149_key.startswith("delivery_"):_ex149_cast.add("까로")
        if _ex149_key in ("market_intro","scale_eunho","scale_repeat","receive_cord","receive_weight","return_weight"):_ex149_cast.add("은호")
        for _ex149_row in _ex149_rows:
            if not _ex149_row.get("id") or _ex149_row["id"] in _ex149_ids:raise Exception("선택 탐색 대사 ID 중복/누락")
            _ex149_ids.add(_ex149_row["id"])
            if _ex149_row.get("speaker") not in _ex149_cast or _ex149_row.get("kind") not in ("narration","dialogue") or not _ex149_row.get("text"):raise Exception("선택 탐색의 화자/대사 형식 오류: "+_ex149_key)
    R13_EX149_ITEMS=("cord","weight")
    R13_EX149_PARTS={
        "delivery":(("large_tag","큰 상자의 짐표"),("small_tag","작은 상자의 짐표"),("box","작은 상자의 바닥")),
        "scale":(("reference","오른쪽 접시의 가게 추"),("pivot","저울의 축")),
    }

    def r13_ex149_lines(key):
        return [r13_nw_added_line(row) for row in R13_EX149_BLOCKS[key]]

    def r13_ex149_topics(person):
        if not r13_ex149_person_ready(person):return []
        state=r13_ex149_state();here=store.room13.get("location")
        if person=="karo" and here=="gate":
            return [("수레 옆의 두 짐을 살펴봐도 될까요?","delivery",bool(state.get("knot_method")))]
        if person=="resident_eunho" and here in ("store","market"):
            rows=[("묶음끈과 표준추를 쓸 수 있을까요?","shop",bool(state.get("intro_seen")))]
            if r13_ex149_weight_borrowed():
                rows.append(("빌린 표준추를 돌려드리겠습니다.","return_weight",False))
            if here=="store" and state.get("scale_placed") and state.get("scale_pivot") and (r13_ex149_owned("weight") or state.get("scale_corrected")):
                rows.append(("표준추를 올려 봤는데, 함께 다시 재 주시겠어요?","scale_report",bool(state.get("scale_corrected"))))
            return rows
        return []

    _r13_ex149_questions=r13_v111_questions
    def r13_v111_questions(person):
        rows=list(_r13_ex149_questions(person))
        extra=[(title,Return(("exploration149",action)),read) for title,action,read in r13_ex149_topics(person)]
        split=next((i for i,row in enumerate(rows) if isinstance(getattr(row[1],"value",None),(tuple,list))),len(rows))
        return rows[:split]+extra+rows[split:]

    _r13_ex149_business=r13_v111_has_business
    def r13_v111_has_business(person):
        return bool(r13_ex149_topics(person)) or _r13_ex149_business(person)

    _r13_ex149_places=r13_v111_public_revisit_places
    def r13_v111_public_revisit_places():
        places=list(_r13_ex149_places())
        if r13_ex149_available() and "market" not in places:places.append("market")
        return places

    def r13_ex149_object(key):
        return r13_ex149_available() and (store.room13.get("location"),key) in (("store","scale"),("market","market_cloth"))

    def r13_ex149_picture(scene):
        state=r13_ex149_state()
        if scene=="delivery":return R13_LIFE_SCENES["delivery"]["after" if state.get("delivery_tied") else "before"]
        return R13_LIFE_SCENES["scale_loaded" if store.r13_ex149_scale_on_pan else "scale_base"]["before"]

    def r13_ex149_notes():
        state=r13_ex149_state();out=[]
        if state.get("delivery_large_tag"):out.append("큰 짐표: 광장 뒤 세 번째 집, 솔 씨 댁.")
        if state.get("delivery_small_tag"):out.append("작은 짐표: 광장 뒤 세 번째 집, 솔 씨 댁.")
        if state.get("delivery_box"):out.append("작은 상자의 밑면은 매끄러워, 큰 상자 위에서 미끄러진다.")
        if state.get("knot_method"):out.append("까로와 짐을 묶어 보았다. 움직이는 부분을 누른 채 끈을 감는 법을 배웠다.")
        if state.get("scale_placed"):out.append("가게 저울에 표준추를 올려 양쪽 접시를 살폈다. 추는 다시 챙겼다.")
        if state.get("scale_pivot"):out.append("저울 축에 조절 나사가 있다. 이것만으로 누가 손댔는지는 알 수 없다.")
        if state.get("scale_corrected"):out.append("은호와 빈 접시부터 확인하고 저울 눈금을 맞췄다. 물건을 올리기 전에 수평인지 먼저 본다.")
        return out

screen r13_ex149_bag():
    modal True
    zorder 45
    use r13_notebook_shell("물품",close_action=Return(None))
    text "물건을 고른 뒤 현장에서 사용할 곳을 누르세요." xpos 132 ypos 148 size r13_type("small") color r13_nb_muted()
    for index,item in enumerate(R13_EX149_ITEMS):
        $ owned=r13_ex149_owned(item)
        fixed:
            area (132,190+index*158,1074,146)
            if r13_material_art("bag:"+item):
                add r13_material_art("bag:"+item) xpos 0 ypos 8 xysize (160,100)
            text R13_SHOP[item]["title"] xpos 180 ypos 6 size r13_type("subtitle") color r13_nb_ink() font R13_UI_BOLD_FONT
            text ("짐이나 헐거운 덮개를 묶는 데 쓸 수 있다." if item=="cord" else "가게 저울에 올려 볼 수 있다. 사용해도 없어지지 않는다.") xpos 180 ypos 55 xsize 590 size r13_type("body") color r13_nb_ink()
            fixed:
                area (830,22,232,r13_control_height())
                use r13_control("사용할 물품 선택" if owned else "가지고 있지 않음",None,Return(item),enabled=owned,width=232,control_id="ex149_select_"+item)
    use r13_nb_footer_button(0,"현장으로",Return(None),control_id="ex149_bag_back")
    use r13_nb_footer_button(1,"사용 취소",Return("cancel"),enabled=r13_ex149_held is not None,control_id="ex149_cancel")
    use r13_nb_footer_button(3,"알게 된 방법",Return("notes"),width=232,control_id="ex149_notes")

screen r13_ex149_shop():
    modal True
    zorder 45
    use r13_notebook_shell("은호의 생활 도구",close_action=Return(None))
    text "남은 끈을 받거나, 필요한 표준추를 빌릴 수 있습니다." xpos 132 ypos 148 size r13_type("small") color r13_nb_muted()
    for index,item in enumerate(R13_EX149_ITEMS):
        $ owned=r13_ex149_owned(item)
        $ spent=item in r13_wallet(room13)["used"]
        fixed:
            area (132,190+index*158,1074,146)
            if r13_material_art("bag:"+item):
                add r13_material_art("bag:"+item) xpos 0 ypos 8 xysize (160,100)
            text R13_SHOP[item]["title"] xpos 180 ypos 6 size r13_type("subtitle") color r13_nb_ink() font R13_UI_BOLD_FONT
            text R13_SHOP[item]["detail"] xpos 180 ypos 55 xsize 590 size r13_type("body") color r13_nb_ink()
            fixed:
                area (830,22,232,r13_control_height())
                use r13_control("가지고 있음" if owned else "이미 사용함" if spent else "남은 끈 받기" if item=="cord" else "표준추 빌리기",None,Return(item),enabled=not owned and not spent,width=232,control_id="ex149_receive_"+item)
    use r13_nb_footer_button(0,"돌아가기",Return(None),control_id="ex149_shop_back")

screen r13_ex149_closeup(scene):
    modal True
    zorder 45
    $ state=r13_ex149_state()
    use r13_notebook_shell("까로의 배달 짐" if scene=="delivery" else "가게 저울",close_action=Return(None))
    add Transform(r13_ex149_picture(scene),xysize=(620,349),nearest=True) xpos 132 ypos 152
    text "그림 오른쪽에서 살펴볼 곳을 고르세요." xpos 132 ypos 512 xsize 620 size r13_type("small") color r13_nb_muted()
    viewport:
        area (776,150,430,r13_nb_body_bottom()-150)
        mousewheel True draggable True scrollbars "vertical"
        vbox:
            spacing 12
            for part,title in R13_EX149_PARTS[scene]:
                use r13_control(title,None,Return(("look",part)),chosen=bool(state.get(scene+"_"+part)),width=408,height=r13_control_height(),control_id="ex149_look_"+part)
    use r13_nb_footer_button(0,"현장으로",Return(None),control_id="ex149_closeup_back")
    if scene=="delivery":
        if state.get("delivery_tied"):
            use r13_nb_footer_button(2,"까로와 묶은 짐 확인",Return(("report","delivery")),width=280,control_id="ex149_report_delivery")
        else:
            use r13_nb_footer_button(2,"함께 옮길 방법 정하기",Return(("use","cord")),enabled=r13_ex149_owned("cord"),width=280,control_id="ex149_tie")
    else:
        use r13_nb_footer_button(2,"표준추 올려 비교",Return(("use","weight")),enabled=r13_ex149_owned("weight"),width=280,control_id="ex149_place_weight")

screen r13_ex149_notes():
    modal True
    zorder 45
    use r13_notebook_shell("직접 확인한 것",close_action=Return(None))
    viewport:
        area (132,150,1074,r13_nb_body_bottom()-150)
        mousewheel True draggable True scrollbars "vertical"
        vbox:
            spacing 20
            for note in r13_ex149_notes() or ["아직 이곳에서 직접 확인한 것이 없습니다."]:
                text note size r13_type("body") color r13_nb_ink() xmaximum 1032
    use r13_nb_footer_button(0,"돌아가기",Return(None),control_id="ex149_notes_back")

label r13_ex149_inventory:
    if not r13_ex149_available():
        return
    call screen r13_ex149_bag
    if _return=="notes":
        call screen r13_ex149_notes
        jump r13_ex149_inventory
    elif _return=="cancel":
        $ r13_ex149_held=None
    elif _return in R13_EX149_ITEMS and r13_ex149_owned(_return):
        $ r13_ex149_held=_return
        $ renpy.notify(R13_SHOP[r13_ex149_held]["title"]+" 선택 · 현장에서 사용할 곳을 누르세요.")
    return

label r13_ex149_person(person,action):
    if not any(row[1]==action for row in r13_ex149_topics(person)):
        return
    if action=="shop":
        if not r13_ex149_state().get("intro_seen") and r13_ex149_mark("intro_seen"):
            call r13_lines(r13_ex149_lines("market_intro"),"exploration149:market_intro")
        label r13_ex149_shop_again:
        call screen r13_ex149_shop
        if _return in R13_EX149_ITEMS:
            if r13_ex149_receive(_return):
                $ ex149_receive_key="receive_"+_return
                call r13_lines(r13_ex149_lines(ex149_receive_key),"exploration149:"+ex149_receive_key)
            jump r13_ex149_shop_again
    elif action=="return_weight":
        if r13_ex149_return_weight():
            call r13_lines(r13_ex149_lines("return_weight"),"exploration149:return_weight")
    elif action=="delivery":
        if r13_ex149_state().get("knot_method"):
            call r13_lines(r13_ex149_lines("delivery_repeat"),"exploration149:delivery_repeat")
        else:
            if not r13_ex149_state().get("delivery_tied"):
                call r13_lines(r13_ex149_lines("delivery_intro"),"exploration149:delivery_intro")
            call r13_ex149_inspect("delivery")
    elif action=="scale_report":
        if r13_ex149_state().get("scale_corrected"):
            call r13_lines(r13_ex149_lines("scale_repeat"),"exploration149:scale_repeat")
        elif r13_ex149_scale_correct():
            call r13_lines(r13_ex149_lines("scale_eunho"),"exploration149:scale_eunho")
    return

label r13_ex149_inspect(ex149_scene):
    if not r13_ex149_available() or (ex149_scene=="delivery" and (room13["location"]!="gate" or not r13_ex149_person_ready("karo"))) or (ex149_scene=="scale" and room13["location"]!="store"):
        return
    label r13_ex149_inspect_again:
    call screen r13_ex149_closeup(ex149_scene)
    $ ex149_pick=_return
    if not isinstance(ex149_pick,tuple):
        if ex149_scene=="scale" and r13_ex149_scale_on_pan:
            call r13_lines(r13_ex149_lines("scale_pack"),"exploration149:scale_pack")
            $ r13_ex149_scale_on_pan=False
        return
    if ex149_pick[0]=="look":
        if r13_ex149_state().get(ex149_scene+"_"+ex149_pick[1]) or r13_ex149_observe(ex149_scene+"_"+ex149_pick[1]):
            $ ex149_block=ex149_scene+"_"+ex149_pick[1]
        else:
            $ ex149_block="scale_need_check" if ex149_scene=="scale" else "delivery_need_read"
        call r13_lines(r13_ex149_lines(ex149_block),"exploration149:"+ex149_block)
    elif ex149_pick==("use","cord"):
        if not r13_ex149_delivery_ready():
            call r13_lines(r13_ex149_lines("delivery_need_read"),"exploration149:delivery_need_read")
        else:
            $ ex149_loading=renpy.display_menu([("작은 상자를 큰 상자 위에 그냥 얹는다","unbound"),("두 상자를 겹쳐 끈으로 묶는다","tie"),("다시 살펴본다",None)])
            if ex149_loading in ("unbound","separate"):
                call r13_lines(r13_ex149_lines("delivery_"+ex149_loading),"exploration149:delivery_"+ex149_loading)
            elif ex149_loading=="tie":
                call screen r13_confirm("가진 끈으로 두 상자를 묶을까요?","두 짐 묶기","더 살펴보기")
                if _return and r13_ex149_delivery_tie():
                    call r13_lines(r13_ex149_lines("delivery_tie"),"exploration149:delivery_tie")
    elif ex149_pick==("report","delivery"):
        if r13_ex149_state().get("knot_method"):
            call r13_lines(r13_ex149_lines("delivery_repeat"),"exploration149:delivery_repeat")
        elif r13_ex149_delivery_report():
            call r13_lines(r13_ex149_lines("delivery_taught"),"exploration149:delivery_taught")
    elif ex149_pick==("use","weight"):
        if r13_ex149_owned("weight") and (r13_ex149_state().get("scale_placed") or r13_ex149_scale_place()):
            $ r13_ex149_scale_on_pan=True
            call r13_lines(r13_ex149_lines("scale_place"),"exploration149:scale_place")
    jump r13_ex149_inspect_again

label r13_ex149_object_dispatch(obj):
    if not r13_ex149_object(obj):
        return False
    if room13["location"]=="store":
        $ r13_ex149_scale_on_pan=False
        call r13_lines(r13_ex149_lines("scale_intro"),"exploration149:scale_intro")
        call r13_ex149_inspect("scale")
    else:
        $ renpy.notify("은호의 생활 도구입니다. 남은 끈이나 빌릴 추는 은호에게 물어보세요.")
    return True

label r13_ex149_use(obj):
    if not r13_ex149_available() or not r13_ex149_owned(r13_ex149_held):
        $ r13_ex149_held=None
        return None
    if r13_ex149_held=="cord" and r13_ex149_lamp_ready(obj):
        call screen r13_confirm("가진 끈으로 3번 등 덮개의 걸쇠를 고정할까요?","걸쇠 고정하기","더 살펴보기")
        if _return and r13_ex149_lamp_supply(obj):
            $ r13_ex149_held=None
            call r13_lines(r13_ex149_lines("lamp_method"),"exploration149:lamp_method")
            return 3
    elif r13_ex149_held=="cord" and r13_ex149_lamp_needs_method(obj):
        call r13_lines(r13_ex149_lines("lamp_need_method"),"exploration149:lamp_need_method")
    elif r13_ex149_held=="weight" and room13["location"]=="store" and obj=="scale":
        $ r13_ex149_held=None
        if r13_ex149_owned("weight") and (r13_ex149_state().get("scale_placed") or r13_ex149_scale_place()):
            $ r13_ex149_scale_on_pan=True
            call r13_lines(r13_ex149_lines("scale_place"),"exploration149:scale_place")
            call r13_ex149_inspect("scale")
    else:
        call r13_lines(r13_ex149_lines("wrong_target"),"exploration149:wrong_target")
    return None
