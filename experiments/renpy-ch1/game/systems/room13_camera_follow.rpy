# 2026-10-29 피드백 M: 넓은 장소(우체국·솜이네 앞 등)에서 자동 대화가 끝나 조사 화면으로 돌아오면 카메라는 도착할 때의
# 구역에 그대로 있고, 방금 말하던 사람(세련·네로 등)은 다른 구역에 서 있어 찾기 어려웠다. 가장자리 이름표가 있긴 하지만
# 대화를 이어 갈 사람을 화면 밖에 두는 것은 길 찾기를 플레이어에게 넘기는 것이다.
# 대기에 들어서는 순간, 그 사이에 새 대사가 있었고 마지막 상대가 이 장소에 서 있는데 지금 화면 밖이면 그 사람이 있는 구역으로
# 카메라를 옮긴다. 이동 대기(travel)는 건드리지 않는다. 카메라는 화면 표시일 뿐 시간·자료·상태를 바꾸지 않는다.
default r13_follow_token = None

init 345 python:
    _r13_follow_context=r13_v111_context
    def r13_v111_context(key):
        _r13_follow_context(key)
        try:r13_follow_last_partner(key)
        except Exception:pass  # 표시 보조다. 실패해도 진행을 막지 않는다.

    def r13_follow_last_partner(key):
        if key=="travel":return
        token=getattr(store,"r13_read_id",None)
        if token is None or token==store.r13_follow_token:return
        store.r13_follow_token=token
        person=getattr(store,"r13_last_partner",None)
        location=(store.room13 or {}).get("location")
        end=r13_camera_range(location)
        if not person or end<=0 or person not in r13_visible_people():return
        actor=next((a for a in r13_stage_people() if a.get("person")==person),None)
        if not actor:return
        fx,fy,fw,fh=r13_actor_face(actor,0)
        center=fx+fw/2.0
        left=r13_world_offset(location);view=r13_view_width(location)
        if left+30<=center<=left+view-30:return
        # 조사 화면의 카메라는 양 끝 두 구역뿐이다(r13_world_zone_offset).
        R13WorldCameraChanged(location)(0 if center<view-30 else end)
