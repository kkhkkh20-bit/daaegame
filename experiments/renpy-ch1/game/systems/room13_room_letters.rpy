# 첫 방에서 대사로 함께 펼친 두 글의 읽기 자리. 제시 묶음·판정은 바꾸지 않는다.
init 355 python:
    R13_V111_STEP_GOALS.update({
        "note_pick":"책상 위 접힌 메모를 펼쳐 보자.",
        "bundle_open":"메모 밑 접힌 그림도 함께 살펴보자.",
        "letter_compare_review":"초롱 씨는 어디 있을까. 두 글은 같은 사람이 쓴 걸까.",
        "chorong_inquiry1":"메모에 적힌 초롱 씨는 지금 어디 계실까. 아래층 할머니에게 물어볼 수 있다.",
    })
    R13_V111_RECORD_LATER[("room13","family_bundle")]="책상 위 접힌 종이. 먼저 그 위의 메모부터 읽어 보자."

    R13_ROOM_LETTERS_KEY="두 편지를 나란히 본다"
    R13_ROOM_LETTERS_PAIR=("V111:E01","V111:E06")

    def r13_room_letters_discovery_needed(key):
        if key not in (R13_ROOM_LETTERS_KEY,"v111:"+R13_ROOM_LETTERS_KEY):
            return False
        if r13_v111_value("letter_tail_observed") is True:
            return False
        # 이미 비교를 마친 판에는 새 조사 단계를 소급하지 않는다.
        given=r13_v111_value("proof_given:"+R13_ROOM_LETTERS_KEY)
        if given and set(given)==set(R13_ROOM_LETTERS_PAIR):
            return False
        return not r13_has("v111:applied:MS14_D01_S05_L0031")

    def r13_room_letters_discovery_pending(key,pair):
        values=tuple(pair or ())
        return (len(values)==2 and set(values)==set(R13_ROOM_LETTERS_PAIR)
                and r13_room_letters_discovery_needed(key))

    def r13_room_letters_begin_discovery(claim,pair):
        # 자료를 읽는 편의는 유지하되, 차이를 짚기 전에는 제출하지 않는다.
        # 이 동작은 UI 기억만 바꾸며 보유 자료·선택·기회·시간은 그대로다.
        if not r13_room_letters_discovery_pending(claim,pair):
            return False
        views=dict(getattr(store,"r13_pw_views",{}) or {})
        remembered=dict(views.get(claim,{}) or {})
        remembered.update(view="pair",pair=tuple(pair),quote_open=False,
                          origin_open=False,room_letters_discovery=True)
        views[claim]=remembered
        store.r13_pw_views=views
        screen=renpy.get_screen("r13_proof_workspace")
        if screen:
            for field,value in (("view","pair"),("pair",tuple(pair)),("observe",True),
                                ("quote_open",False),("origin_open",False),("pick_slot",None)):
                screen.scope[field]=value
            renpy.restart_interaction()
        return True

    def r13_room_letters_open():
        keys=("V111:E01","V111:E06")
        if not all(key in store.room13.get("evidence",[]) for key in keys):
            return False
        claim="v111:두 편지를 나란히 본다"
        views=dict(getattr(store,"r13_pw_views",{}) or {})
        remembered=dict(views.get(claim,{}) or {})
        if remembered.get("room_letters_130"):
            return False
        # 구 저장의 한 장 읽기 상태도 첫 방문에 한 번만 두 글 읽기로 맞춘다.
        # 체크/arguments는 그대로 두며 완료 버튼은 현재 읽는 쌍을 명시 제출한다.
        remembered.update(tab="all",detail="V111:E06",view="pair",pair=keys,
                          quote_open=False,origin_open=False,room_letters_130=True)
        views[claim]=remembered
        store.r13_pw_views=views
        return True

    def r13_room_letters_after_load():
        screen=renpy.get_screen("r13_proof_workspace")
        if not screen or screen.scope.get("key")!="두 편지를 나란히 본다":
            return
        if not r13_room_letters_open():
            return
        remembered=store.r13_pw_views["v111:두 편지를 나란히 본다"]
        for field in ("tab","detail","view","pair","quote_open","origin_open"):
            screen.scope[field]=remembered[field]

    config.after_load_callbacks.append(r13_room_letters_after_load)
