# 아랫길 노인 전용 그림. 공유 별지기 장로 원본은 변경하지 않는다.
# 기본 입석·얼굴만 납품됐으며 기존 표정 대체 규칙을 유지한다.
# 새 이야기·표정·장면을 작성하지 않는다.
init 172 python:
    R13_LOWERROAD_ELDER_BODY = "assets/lowerroad-elder/v111_lowerroad_elder_fullbody.webp"
    R13_LOWERROAD_ELDER_FACE = "assets/lowerroad-elder/v111_lowerroad_elder_face.webp"
    R13_FULLBODY["people"]["v111_lowerroad_elder"] = dict(
        name_ko="아랫길 노인", crop=[157,17,716,1487], figure=[173,33,684,1455],
        images={"neutral": dict(file=R13_LOWERROAD_ELDER_BODY, size=[1024,1536],
                                native_detail=True, smooth_source=True)})
    R13_FULLBODY_FILES.add(R13_LOWERROAD_ELDER_BODY)
    # 다른 인물의 얼굴을 빌리지 않고 기존 캐스트·표정 API를 유지한다.
    # 기본 전신을 포함해 각 행은 독립된 사전이다.
    _r13_elder_body = dict(file=R13_LOWERROAD_ELDER_BODY, crop=[173,33,684,1455],
        nearest=False, foot=[339,1437], facing="front", contact="standing",
        head=[62,0,555,542], reviewed=True, posture="standing")
    _r13_elder_face = dict(file=R13_LOWERROAD_ELDER_FACE, crop=[0,0,555,555],
        nearest=False, dedicated_avatar=True, facing="front", gaze="viewer")
    CAST["v111_lowerroad_elder"] = {
        key: dict(_r13_elder_face if key.startswith("avatar_") else _r13_elder_body)
        for key in CAST.get("v111_lowerroad_elder", CAST["elder"])}
    R13_BDIALOGUE_FACES["v111_lowerroad_elder"] = {"neutral": R13_LOWERROAD_ELDER_FACE}
