# 2026-10-29 피드백 J(0.20.86 외부 플레이): 3일 오전 공방에서 부리가 「집게를 빌려 간 우박은 진료소에 있다」고
# 하는데, 같은 공방 조사 화면에 우박이 서 있었다(뒤이어 진료소에서도 만난다).
# 원인: 장면 묶음(field-bindings)에 없는 주민은 옛 주간 일과대로 세운다(room13_v111.rpy r13_visible_people 가 부르는
# _r13_v111_visible_people → r13_where → r13_resident_where). 우박의 일과(room13-content.json weekly_locations)는
# 날마다 오전=공방·오후=진료소·저녁=여관이라, 3일 오전(period 0) 공방에 그대로 섰다.
# 대사가 「그 사람은 다른 곳에 있다」고 말한 장면에서는 그 사람을 다른 장소에 세우지 않는다. 대사가 가리키는 곳에서는
# 장면 묶음대로 보인다. days123 은 줄 수를 바꾸면 안 되므로 여기서 덮어쓴다.
init 342 python:
    # 장면 ID: {사람: 대사가 그 사람이 있다고 말한 장소}
    R13_V111_SCENE_ELSEWHERE={
        # D03 S03: 부리 「진료소요. 거기서 돌 재요.」(NW_AR_D03_03), 우박 「나 지금 못 나가요. 돌이 식는 중이라.」(NW_AR_D03_04).
        # 집게를 돌려주러 공방에 다시 가는 owl_tongs3 도 이 장면 안이라 같이 걸린다.
        "MS14_D03_S03":{"resident_ubak":"clinic"},
    }
    _r13_elsewhere_visible_people=r13_visible_people
    def r13_visible_people():
        people=_r13_elsewhere_visible_people()
        if not r13_v111_active():return people
        away=R13_V111_SCENE_ELSEWHERE.get(store.room13["v111"].get("scene"),{})
        if not away:return people
        here=store.room13.get("location")
        return [p for p in people if away.get(p,here)==here]
