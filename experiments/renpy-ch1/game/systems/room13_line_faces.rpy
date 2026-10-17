# 0.19.17 대사별 표정과 "순간 반응 → 대화 자세" (소유자 2026-10-17)
#   "각 대사별 표정 연출이 지금 잘 안 나와서 매칭해서 적용시켜 줘야 함."
#   "놀람은 오래 유지하는 대화 표정이 아니라 짧은 리액션 컷이다. 순간 움찔한 뒤 플레이어를 다시 보면서
#    '놀란 감정이 남은 대화 자세'로 바꾸고, 그 상태에서 대사를 이어 가게. 이미지도 순간 리액션용과 대화 유지용을 구분."
#
# 1) 표정: assets/room13-line-faces.json {인물:{대사 글자:표정}}. 대사 전체를 장면 문맥과 함께 읽고 정했다.
#    대사 안에 직접 쓴 expression/pose와 room13-fullbody-line-emotions.json(손으로 정한 줄)이 먼저다.
# 2) 그림: 전신 표정 묶음이 두 벌인 인물(-acting 동작 컷 + 정면 그림)은
#    놀람·화남·당황(R13_FACE_REACT)에서 동작 컷을 순간 반응(R13_FACE_REACT_TIME초)으로만 쓰고, 곧 정면 그림(대화 유지)으로 바뀐다.
#    같은 사람이 같은 표정을 이어 말하면 정면 그림만 쓴다.
default r13_face_last = {}
default r13_face_react = None

transform r13_react_then_hold(react,hold):
    react
    pause R13_FACE_REACT_TIME
    hold

init 192 python:
    R13_LINE_FACES=(json.load(renpy.file("assets/room13-line-faces.json")) if renpy.loadable("assets/room13-line-faces.json") else {}).get("faces",{})
    R13_FACE_REACT=("surprise","angry","flustered")
    R13_FACE_REACT_TIME=.45

    def r13_face_hold_file(person,emotion):
        entry=R13_FULLBODY.get("people",{}).get(person) or {}
        image=entry.get("images",{}).get(emotion) or {}
        f=image.get("file","")
        if "-acting" not in f:return None
        plain=f.replace("-acting","")
        return plain if renpy.loadable(plain) else None

    _r13_lf_performance=r13_line_performance
    def r13_line_performance(identity,index,packet):
        expression,pose=_r13_lf_performance(identity,index,packet)
        person,text=packet[0],packet[1]
        if index==0:store.r13_face_last={}
        explicit=len(packet)>2 and packet[2] and (not isinstance(packet[2],dict) or "expression" in packet[2] or "pose" in packet[2])
        cue=R13_FULLBODY_LINES.get("lines",{}).get(identity,{}).get(str(index))
        authored=explicit or (cue and cue.get("person")==person and cue.get("text")==text) or pose not in ("neutral","thinking")+R13_FULLBODY_EMOTIONS
        if not authored:
            face=R13_LINE_FACES.get(person,{}).get(text)
            if face:expression,pose=R13_FULLBODY_TO_LEGACY.get(face,expression),face
        emotion=r13_fullbody_key(pose)
        last=dict(store.r13_face_last or {})
        store.r13_face_react=(person,emotion) if emotion in R13_FACE_REACT and last.get(person)!=emotion else None
        last[person]=emotion;store.r13_face_last=last
        return expression,pose

    R13_FACE_HOLD_CACHE={}
    def r13_face_hold_art(person,emotion,height,speaking=False):
        plain=r13_face_hold_file(person,emotion)
        if not plain:return None
        key=(person,emotion,int(height))
        art=R13_FACE_HOLD_CACHE.get(key)
        if art is None:
            entry=R13_FULLBODY["people"][person]
            scale=r13_fullbody_scale(person,height)
            width=entry["crop"][2]*scale;native_height=entry["crop"][3]*scale
            art=r13_pixel_scale(Crop(tuple(entry["crop"]),plain),width,native_height,R13_CLOSE_PIXEL_GRID)
            art=r13_idle_art(art,person,emotion,None,int(round(width)),int(round(native_height)),contact="dialogue_bust",speaking=speaking)
            if len(R13_FACE_HOLD_CACHE)>=24:R13_FACE_HOLD_CACHE.clear()
            R13_FACE_HOLD_CACHE[key]=art
        return art

    _r13_lf_close=r13_fullbody_close_art
    def r13_fullbody_close_art(person,pose,height,speaking=False,entrance=False):
        emotion=r13_fullbody_key(pose)
        if emotion not in R13_FACE_REACT:return _r13_lf_close(person,pose,height,speaking,entrance)
        hold=r13_face_hold_art(person,emotion,height,speaking)
        if hold is None:return _r13_lf_close(person,pose,height,speaking,entrance)
        if store.r13_face_react==(person,emotion):
            result=r13_react_then_hold(_r13_lf_close(person,pose,height,speaking,False),hold)
        else:
            result=hold
        return At(result,r13_actor_enter(r13_appearance_duration())) if entrance else result
