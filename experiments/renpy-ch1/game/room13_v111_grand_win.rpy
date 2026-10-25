# 2026-10-24 대승리 두 곳(docs/design/GRAND_WIN_DESIGN.md 추천안, 소유자 결정 DECISIONS_20261024.md 4·7번).
# 7일 불 회의의 보너스 증거 「누비네 배급표의 덧붙인 줄」, 12일 수프 회의의 「돌아온 흰 그릇」.
# 얻는 길은 기존 현장 묶음(v111/field-bindings.json)의 조사 물건·질문으로만 연다. 새 화면·표시·권유는 없다.
# 처음 하는 사람에게는 평범한 생활 행동으로만 보이고, 두 단계 이상이 맞아야 증거가 된다.
# 보고: docs/reviews/grand-win-20261024/적용보고.md
init 321 python:
    # 조사 물건. 글이 빈 물건은 그 단계의 선택이 있을 때만 눌린다(돋보기 표식은 원래 없다).
    # 빨래터는 2048x768 그림을 1920x720으로 그린 자리(room13_v111_later_bindings.rpy), 학교는 1800x720.
    ROOM13["objects"].setdefault("laundry",{})["v111_drum"]=dict(rect=[665,400,110,150],need=[],give=[],flags=[],text="솥 옆의 등유 통. 반쯤 비었다.")
    ROOM13["objects"]["laundry"]["v111_line"]=dict(rect=[640,175,560,225],need=[],give=[],flags=[],text="")
    ROOM13["objects"].setdefault("school",{})["v111_bowl_table"]=dict(rect=[1610,380,185,110],need=[],give=[],flags=[],text="")
    R13_OBJECT_NAMES.update(v111_drum="등유 통",v111_line="빨래 줄",v111_bowl_table="작은 배식대")

    # 5일 저녁 여관으로 가는 길: 지도에서 빨래터로 돌아갈 수 있다(r13_v111_travel 의 이동 대기에 한 자리 더).
    # 표시하지 않는다. 지도에 빨래터가 갈 수 있는 곳으로 보일 뿐이다.
    _r13_gw_binding=r13_v111_binding
    def r13_v111_binding():
        b=_r13_gw_binding()
        v=store.room13.get("v111",{})
        detour=v.get("travel_detour")
        if v.get("gate")=="travel" and detour and detour!=v.get("travel_to") and detour in R13_PLACES:
            options=list(b.get("options",[]))
            options.append(dict(title=R13_PLACES[detour][0],location=detour,move=detour,index=len(options)))
            b=dict(b,options=options)
        return b

    # 12일 수프 대승리·예방판 대체(결정 7)가 이송 예정 칸을 무효로 하면, 13일에 그 칸으로 실린 사람을 내린다.
    # 실룩(3일 처분)과 굴돌(처음 수레 명단)은 다른 까닭으로 실렸으므로 남는다(GRAND_WIN_DESIGN.md 2-4).
    R13_GW_VOID_KEEP=("resident_siluk","resident_guldol")
    def r13_gw_void_people():
        if r13_v111_value("transfer_list_voided") is not True:return []
        return [p for p in r13_nw_listed() if p not in R13_GW_VOID_KEEP and r13_v111_person_alive(p) and not r13_v111_value("handed:"+p) and not r13_v111_value("departed:"+p)]
    def r13_gw_void_down():
        people=r13_gw_void_people()
        for p in people:
            r13_v111_set("handed:"+p,True)
            r13_v111_set("void_down:"+p,True)
        return people

# ---------------------------------------------------------------- 5일 저녁 빨래터 (F1 첫 단계)
label r13_v111_laundry5:
    $ r13_v111_arrive(['daram'] if r13_v111_actor_ready('daram') else [])
label r13_v111_laundry5_wait:
    call r13_v111_wait('laundry5')
    if _return==0:
        call r13_v111_laundry_overhear5
        jump r13_v111_laundry5_wait
    # 지도로 여관을 골랐다(이미 여관에 와 있다). 함께 온 다람만 세운다.
    $ r13_v111_arrive(['daram'] if r13_v111_actor_ready('daram') else [])
    return

label r13_v111_laundry_overhear5:
    call r13_lines(r13_nw_block('laundry_line5'),'nw:laundry_line5')
    $ r13_v111_join(['neoul','resident_nubi'])
    call r13_lines(r13_nw_block('laundry_overhear5'),'nw:laundry_overhear5')
    $ r13_nw_acquire("NW_LAUNDRY_TALK")
    $ r13_v111_set('grand_laundry_seen5',True)
    $ r13_v111_set('grand_ticket_spot_known',True)
    # 둘은 각자 자리를 떴다. 무대에는 다람만 남긴다.
    $ r13_v111_arrive(['daram'] if r13_v111_actor_ready('daram') else [])
    return

# ---------------------------------------------------------------- 7일 (F1 둘째 단계, F3 둘째 길)
label r13_v111_nubi_snack7:
    call r13_lines(r13_nw_block('nubi_snack7'),'nw:nubi_snack7')
    $ r13_v111_set('grand_snack_ready7',False)
    $ r13_v111_set('grand_snack_given7',True)
    $ r13_v111_set('grand_ticket_spot_kid',True)
    $ r13_v111_set('grand_ticket_spot_known',True)
    return

label r13_v111_nubi_ticket7:
    call r13_lines(r13_nw_block('nubi_ticket7'),'nw:nubi_ticket7')
    $ r13_nw_acquire("NW_NUBI_TICKET")
    return

# ---------------------------------------------------------------- 11일 까로의 빈 수레 (S1 첫 단계)
label r13_v111_bowl_cart11:
    call r13_lines(r13_nw_block('bowl_cart11'),'nw:bowl_cart11')
    $ r13_v111_set('grand_bowl_seen11',True)
    return

label r13_v111_bowl_pocket11:
    call r13_lines(r13_nw_block('bowl_pocket11'),'nw:bowl_pocket11')
    $ r13_v111_set('grand_bowl_pocket',True)
    return

# ---------------------------------------------------------------- 12일 작은 배식대 (S1 둘째 단계)
label r13_v111_bowl_compare12:
    call r13_lines(r13_nw_block('bowl_compare12'),'nw:bowl_compare12')
    $ r13_nw_acquire("NW_RETURNED_BOWL")
    return

# 12일 국을 미리 막은 판(수프 회의가 없다): 돌목이 문간에 있고, 같은 그릇을 그에게 보이는 대화가
# 수프 대승리를 대신한다(결정 7). 주머니에 그릇이 없는 판은 이 자리를 지나지 않는다.
label r13_v111_early_bowl12:
    $ r13_v111_join(['guard'])
    call r13_lines(r13_nw_block('early_door12'),'nw:early_door12')
label r13_v111_early_bowl12_wait:
    call r13_v111_wait('early_bowl12')
    if _return==1:
        call r13_v111_bowl_compare12
        jump r13_v111_early_bowl12_wait
    if _return==2:
        call r13_v111_early_guard_bowl12
        jump r13_v111_early_bowl12_wait
    return

label r13_v111_early_guard_bowl12:
    call r13_lines(r13_nw_block('early_guard_bowl12'),'nw:early_guard_bowl12')
    $ r13_v111_set('transfer_list_voided',True)
    $ r13_v111_set('grand:soup',True)
    return

# ---------------------------------------------------------------- 13일
label r13_v111_listed_void13:
    # 수레가 선 순간, 무효 칸으로 실린 사람을 모두 내린다(수프 대승리의 보상).
    if r13_gw_void_people():
        call r13_lines(r13_nw_block('listed_void13'),'nw:listed_void13')
        $ r13_gw_void_down()
    return

label r13_v111_crowd_record13:
    # 7일 불 대승리의 보상: 회의 기록(배급표)을 함께 읽어 주먹을 내리게 하고, 너울이 장부를 넘긴다.
    # 갈림길 화면의 광장 칸에는 이 결과의 이름이 없다(화면 변경은 시안 먼저). 운명 값은 적지 않는다.
    call r13_lines(r13_nw_block('crowd_record_read13'),'nw:crowd_record_read13')
    if not r13_v111_owned("NW_NEOUL_LEDGER"):
        $ r13_nw_acquire("NW_NEOUL_LEDGER","surrendered")
    if r13_v111_value('crowd_preparation_schema13'):
        $ r13_crowd_release13()
    $ r13_v111_set('crowd_record_read',True)
    $ r13_v111_set('crowd_resolution_done',True)
    $ r13_v111_set('crowd_injury',False)
    $ r13_v111_set('crowd_intervention','success')
    $ r13_v111_set('outcome13','all_rescued')
    jump r13_v111_handover_plan13
