# 13호 난로 그림(2026-10-26 v2 납품). 13호 배경에는 난로가 없어 빈 벽에 조사 자리만 있었다.
# 받은 세 장(inner·ration·empty)은 오후 배경 위에 그린 통그림이라, 난로 부분만 떼어
# 사건 전후 x 아침·오후·저녁 여섯 배경의 조명에 맞춰 둔 조각을 그림 좌표로 겹친다
# (만드는 법: game/assets/room13-stove/manifest.json, 원본은 art/room13-stove-20261026/).
# 어떤 돌을 보여 줄지는 대본을 따른다. 대사·진행 조건은 바꾸지 않는다.
#   7일 전: 도토가 갈아 넣은 배급 돌(ration 그림, 보통 불빛). 재받이에 돌 없음.
#   7·8일: 할머니가 7일 아침 배급 돌을 재받이에 묻고 안쪽 돌을 넣었다(owl_prevent 머리말).
#          stove13_7 이 없으면 inner, 바꿔 넣었으면 ration, 꺼내기만 했으면 empty.
#          재받이 돌은 주머니에 넣었거나 난로에 바꿔 넣기 전까지 보인다.
#   9일부터: 8일에 서리가 난로의 돌을 꺼냈고(D08_P01) 재받이 돌도 나왔다(D08_S02) → 빈 난로, 재받이 돌 없음.
#            7일에 바꿔 넣은 판(ration)은 그대로 둔다.
init 330 python:
    R13_STOVE_ART=json.load(renpy.file("assets/room13-stove/manifest.json"))
    ROOM13["objects"]["room13"]["v111_stove"]["rect"]=[1885,310,122,185]
    ROOM13["objects"]["room13"]["v111_ashbin"]["rect"]=[1872,474,104,44]

    def r13_stove_state():
        if not r13_v111_active():return "ration",False
        day=store.room13.get("day",1)
        if day<7:return "ration",False
        stove=r13_v111_value("stove13_7")
        if day>=9:return ("ration" if stove=="ration" else "empty"),False
        state=stove if stove in ("ration","empty") else "inner"
        return state,(stove!="ration" and not r13_v111_value("pocket_ration7"))

    _r13_stove_treatment=r13_scene_treatment
    def r13_scene_treatment(location,period,source):
        if location=="room13" and period in ("morning","afternoon","evening"):
            state,stone=r13_stove_state()
            case=r13_world_state("room13") or "before"
            x,y,w,h=R13_STOVE_ART["patch_rect"]
            parts=[(0,0),source,(x,y),R13_STOVE_ART["files"]["%s/%s/%s"%(state,case,period)]]
            if stone:
                parts+=[tuple(R13_STOVE_ART["ashbin"]["rect"][:2]),R13_STOVE_ART["ashbin"]["file"]]
            source=Composite((2172,724),*parts)
        return _r13_stove_treatment(location,period,source)
