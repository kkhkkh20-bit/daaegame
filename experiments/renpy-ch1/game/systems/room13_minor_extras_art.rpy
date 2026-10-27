# 단역 공용 전신 3벌(2026-10-27 요청서): 순찰대원·주민(어른)·아이, 각 6감정.
# 대화 그림은 room13-dialogue-talk-art-extra.json 에 같은 도트 크기(어른 210, 아이 165)로 들어 있다.
# 여기서는 현장 입석과 얼굴 칸도 같은 그림으로 바꾼다. 그동안은 대사 없는 주민(뭉치·칼바람·깜 등)의
# 그림을 빌려 썼는데(room13_extra_faces.rpy), 대화창에서는 새 그림이 나오고 현장에서는 다른 인물이
# 서 있으면 같은 사람으로 읽히지 않는다. 빌려 주던 원래 인물의 행은 바꾸지 않는다.
# 그림은 도트 760(3배) 파일을 그대로 쓰고 최근접으로 그린다. 좌표는 그 파일의 픽셀 기준이다.
# 아랫길 주민·진료 담당자·종업원은 주민 그림을, 실룩의 아이·누비의 막내는 아이 그림을 같이 쓴다(요청서 표).
# 대사·사실·분기·조건은 바꾸지 않는다.
init 327 python:
    R13_MINOR_ART_EMOTIONS = ("neutral","joy","flustered","angry","anxious","surprise")
    R13_MINOR_ART = {
        # 그림 id: (이미지 크기, 전신 crop, figure, 발, 머리, 얼굴 칸)
        "v111_patrol": ([447,672],[17,17,380,644],[21,21,372,636],[177,633],[0,0,372,252],[72,18,252,252]),
        "v111_resident": ([438,657],[44,5,350,647],[48,9,342,639],[165,639],[0,0,342,252],[87,12,252,252]),
        "v111_child": ([351,528],[17,11,302,512],[21,15,294,504],[148,504],[0,0,294,228],[55,18,228,228]),
    }
    R13_MINOR_ART_USERS = {
        # 화자 id: (그림 id, 이름). 이름은 빌려 준 인물의 이름이 남지 않게 직접 적는다.
        "v111_patrol":("v111_patrol","순찰대원"),
        "v111_resident":("v111_resident","주민"),
        "v111_lower_resident":("v111_resident","아랫길 주민"),
        "ms14_clinician":("v111_resident","진료 담당자"),
        "ms14_attendant":("v111_resident","종업원"),
        "v111_child":("v111_child","아이"),
        "v111_siluk_child":("v111_child","실룩의 아이"),
        "kid_nubi3":("v111_child","누비의 막내"),
    }
    def r13_minor_art_file(art,emotion):
        return "assets/dialogue-dot-v2/%s/760/%s.webp" % (art,"surprise_talk" if emotion=="surprise" else emotion)
    for _mn_user,(_mn_art,_mn_name) in R13_MINOR_ART_USERS.items():
        _mn_size,_mn_crop,_mn_fig,_mn_foot,_mn_head,_mn_face=R13_MINOR_ART[_mn_art]
        R13_FULLBODY["people"][_mn_user]=dict(name_ko=_mn_name,crop=list(_mn_crop),figure=list(_mn_fig),
            images={e:dict(file=r13_minor_art_file(_mn_art,e),size=list(_mn_size),native_detail=True) for e in R13_MINOR_ART_EMOTIONS})
        for _mn_e in R13_MINOR_ART_EMOTIONS:R13_FULLBODY_FILES.add(r13_minor_art_file(_mn_art,_mn_e))
        _mn_body=dict(file=r13_minor_art_file(_mn_art,"neutral"),crop=list(_mn_fig),nearest=True,foot=list(_mn_foot),
            facing="front",contact="standing",head=list(_mn_head),reviewed=True,posture="standing")
        _mn_avatar=dict(file=r13_minor_art_file(_mn_art,"neutral"),crop=list(_mn_face),nearest=True,
            dedicated_avatar=True,facing="front",gaze="viewer")
        # 빌려 쓴 행과 같은 열쇠를 유지한다. 각 행은 따로 만든 사전이라 빌려 준 인물의 행은 그대로 남는다.
        CAST[_mn_user]={key:dict(_mn_avatar if key.startswith("avatar_") else _mn_body) for key in CAST.get(_mn_user,CAST["elder"])}
        # 2026-10-27 14일 자동 플레이 7일 학교: 「누비의 막내」가 현장에 서는 순간 Image 'kid_nubi3 neutral' not found 가 글자로 찍혔다.
        # 「인물 자세」 이름의 그림은 options.rpy 가 cast.json 을 읽을 때(이 층보다 앞) 한 번만 등록하므로, 여기서 빌려 만든 행은
        # 그림 이름이 없다. 빌려 온 행마다 같은 이름으로 등록한다.
        for _mn_key,_mn_spec in CAST[_mn_user].items():
            renpy.image(_mn_user+" "+_mn_key,Transform(Crop(tuple(_mn_spec["crop"]),_mn_spec["file"]),nearest=True))
