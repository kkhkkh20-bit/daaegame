# 아랫길 노인 전용 그림. 공유 별지기 장로 원본은 변경하지 않는다.
# 2026-10-26 테두리 없는 6감정 후보를 받아 흰 테두리 입석을 대신한다(인물 스티커 없음 결정).
# 받은 그대로는 반투명 가장자리와 발 높이가 달라 알파를 이진화하고 발 밑줄을 1503 에 맞췄다.
# 원본은 art/lowerroad-elder-20261026/originals 에 둔다. 새 이야기·장면은 작성하지 않는다.
init 172 python:
    R13_LOWERROAD_ELDER_EMOTIONS = ("neutral","joy","flustered","angry","anxious","surprise")
    R13_LOWERROAD_ELDER_BODY = "assets/lowerroad-elder/v111_lowerroad_elder-neutral.webp"
    R13_LOWERROAD_ELDER_FACE = "assets/lowerroad-elder/v111_lowerroad_elder_face-noborder.webp"  # 새 평온 그림에서 잘라 냄
    R13_FULLBODY["people"]["v111_lowerroad_elder"] = dict(
        name_ko="아랫길 노인", crop=[157,33,713,1474], figure=[161,37,705,1466],
        images={e: dict(file="assets/lowerroad-elder/v111_lowerroad_elder-%s.webp" % e, size=[1024,1536],
                        native_detail=True, smooth_source=True) for e in R13_LOWERROAD_ELDER_EMOTIONS})
    for _r13_e in R13_LOWERROAD_ELDER_EMOTIONS:
        R13_FULLBODY_FILES.add(R13_FULLBODY["people"]["v111_lowerroad_elder"]["images"][_r13_e]["file"])
    # 다른 인물의 얼굴을 빌리지 않고 기존 캐스트·표정 API를 유지한다.
    # 기본 전신을 포함해 각 행은 독립된 사전이다.
    _r13_elder_body = dict(file=R13_LOWERROAD_ELDER_BODY, crop=[161,37,705,1466],
        nearest=False, foot=[352,1448], facing="front", contact="standing",
        head=[62,0,555,542], reviewed=True, posture="standing")
    _r13_elder_face = dict(file=R13_LOWERROAD_ELDER_FACE, crop=[0,0,555,555],
        nearest=False, dedicated_avatar=True, facing="front", gaze="viewer")
    CAST["v111_lowerroad_elder"] = {
        key: dict(_r13_elder_face if key.startswith("avatar_") else _r13_elder_body)
        for key in CAST.get("v111_lowerroad_elder", CAST["elder"])}
    R13_BDIALOGUE_FACES["v111_lowerroad_elder"] = {"neutral": R13_LOWERROAD_ELDER_FACE}
