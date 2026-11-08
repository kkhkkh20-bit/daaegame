# 첫 방에서 대사로 함께 펼친 두 글의 읽기 자리. 제시 묶음·판정은 바꾸지 않는다.
init 355 python:
    R13_V111_STEP_GOALS.update({
        "note_pick":"책상 위 접힌 메모를 펼쳐 보자.",
        "bundle_open":"메모 밑 접힌 그림도 함께 살펴보자.",
        "letter_compare_review":"책상에서 초대 편지와 방의 메모를 다시 펼쳐 보자.",
    })
    R13_V111_RECORD_LATER[("room13","family_bundle")]="책상 위 접힌 종이. 먼저 그 위의 메모부터 읽어 보자."

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
