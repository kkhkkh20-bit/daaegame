# 대사 장면 인물 크기·위치(2026-10-28 소유자 「역전재판처럼 상당히 가까이, 머리끝이 화면 끝처럼」 → 1.55배).
# room13_rules.rpy 의 r13_speaker 가 부른다. 마차(앉은 다람)는 예전 크기(840) 그대로.
init 40 python:
    R13_SAY_ACTOR_H=int(840*1.55)   # 대사 장면 인물 높이(예전 840)
    R13_SAY_ACTOR_DY=-552           # 키운 만큼 올려 어른 머리끝이 화면 위(약 20)에 오게
    # 2026-10-28 소유자 「다람이는 좀 내려야겠다. 아이니까」「캐릭터마다 키를 생각해서 배치하는 듯」(역전재판 캡처):
    # 머리 높이를 인물 키로 정한다. 키는 현장 도트 서 있는 높이(room13-field-dot-v2.json, 어른 210)를 쓴다 —
    # 아이 165, 할머니·부엉이 195, 선생님·까로·보리 230. 210 보다 작으면 그만큼 내리고, 크면 올려 머리끝이 화면 위에서 살짝 잘린다.
    # 다람은 0.82(아래 주석). 거리 520 은 어른 머리끝(약 20)~대사판 위(약 540).
    R13_SAY_STATURE_REF=210.0
    def r13_say_stature(who):
        # 2026-10-28 소유자 「다람이 몸이 좀 더 가운데로 오고 높아야 하지 않을까」: 2/3 → 다른 아이들(165/210)보다 조금 큰 0.82.
        if who=="daram":return 0.82
        dot=(globals().get("R13_FIELD_DOT",{}).get(who) or {}).get("poses",{})
        entry=dot.get("neutral") or next(iter(dot.values()),None)
        return (entry["size"][1]/R13_SAY_STATURE_REF) if entry else 1.0
    def r13_say_child_drop(who):
        return int(round(520*(1-min(1.0,r13_say_stature(who)))))

    # 그림마다 캔버스 안 머리 위치가 달라(같은 발 선이어도 선생님·까로는 얼굴이 잘리고 할머니는 낮았다) 실제 그림의
    # 불투명 영역 윗변을 재서 머리끝을 목표 높이에 맞춘다. 재지 못하면 예전 계산(발 선 + 키 보정)으로 둔다.
    R13_SAY_HEAD_TOP=20          # 어른(키 210) 머리끝 화면 높이
    R13_SAY_TALL_CUT=36          # 210 보다 큰 인물은 키 차이만큼(최대 이만큼) 화면 위로 잘린다
    _R13_SAY_HEADTOP={}
    def _r13_say_headtop(who,pose,h):
        profile=r13_dialogue_source_profile(who,pose,h)
        if not profile:return None
        # 그리는 쪽(room13_dialogue_beats.rpy)과 같은 그림을 재야 한다. 놀람은 surprise_talk, 당황 그림이 없으면 불안을 그린다.
        # 2026-10-28 캡처 검수(11일 엄마 「이거…… 아직 갖고 다녔어?」): 이 대응이 없어 보통 표정 그림의 머리를 재고 놀람 그림을 그려
        # 머리가 화면 위로 잘리고 다리만 보였다.
        emotion={"surprise":"surprise_talk"}.get(r13_fullbody_emotion(pose),r13_fullbody_emotion(pose))
        if emotion=="flustered" and "flustered" not in profile["frames"]:emotion="anxious"
        frame=profile["frames"].get(emotion) or profile["frames"].get("neutral")
        if not frame:return None
        key=(frame["file"],h)
        if key not in _R13_SAY_HEADTOP:
            try:
                surf=renpy.display.im.Image(frame["file"]).load()
                top=surf.get_bounding_rect(min_alpha=40).top
                _R13_SAY_HEADTOP[key]=frame["offset"][1]+top*frame.get("scale",1.0)
            except Exception:
                _R13_SAY_HEADTOP[key]=None
        return _R13_SAY_HEADTOP[key]
    # 2026-10-28 캡처 검수(11일 엄마 놀람): 그림 묶음 표로 잰 머리 높이가 실제 그림과 66px 달랐다(표에 없는 표정은 다른 그림이
    # 그려진다). 실제로 그릴 그림(말하는 그림)을 한 번 그려 맨 위 불투명 줄을 잰다. 인물·자세·키마다 한 번만 잰다.
    _R13_SAY_DRAWN_TOP={}
    def _r13_say_drawn_headtop(who,pose,h):
        key=(who,pose,h)
        if key not in _R13_SAY_DRAWN_TOP:
            try:
                rect=renpy.render_to_surface(r13_close_art(who,pose,h,True)).get_bounding_rect(min_alpha=40)
                _R13_SAY_DRAWN_TOP[key]=rect.top if rect.height else None
            except Exception:
                _R13_SAY_DRAWN_TOP[key]=None
        return _R13_SAY_DRAWN_TOP[key]
    def r13_say_head_target(who):
        st=r13_say_stature(who)
        if st>1.0:return R13_SAY_HEAD_TOP-min(R13_SAY_TALL_CUT,int(round((st-1.0)*R13_SAY_STATURE_REF*1.55*0.4)))
        return R13_SAY_HEAD_TOP+r13_say_child_drop(who)
    # 그림 캔버스 가운데가 몸 가운데가 아닌 인물(다람은 왼쪽 꼬리 때문에 얼굴이 오른쪽에 섰다)은 그만큼 옮긴다.
    R13_SAY_X_NUDGE={"daram":-64}
    def r13_say_actor_x(who,pose,carriage=False):
        return r13_close_x(who,pose,r13_say_actor_h(carriage))+(0 if carriage else R13_SAY_X_NUDGE.get(who,0))
    def r13_say_actor_h(carriage=False):
        return 840 if carriage else R13_SAY_ACTOR_H
    def r13_say_actor_y(who,pose,carriage=False):
        h=r13_say_actor_h(carriage)
        if carriage:return r13_close_y(who,h,110,pose)
        head=_r13_say_drawn_headtop(who,pose,h)
        if head is None:head=_r13_say_headtop(who,pose,h)
        if head is not None:return int(round(r13_say_head_target(who)-head))
        return r13_close_y(who,h,110,pose)+R13_SAY_ACTOR_DY+r13_say_child_drop(who)
