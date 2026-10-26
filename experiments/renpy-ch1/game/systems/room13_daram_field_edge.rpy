# 현장 다람의 가장자리(2026-10-27). 다람 현장 그림 두 장은 원본에 옅은 번짐(반투명 테두리)이 넓게 깔려 있어,
# 다른 인물과 같은 격자로 줄여도 다람만 흐릿한 테를 두르고 보였다(반투명 비율 0.97~1.16, 다른 인물 0.27 이하).
# 반투명을 끊은 사본(알파 128 기준)을 만들어 다람 현장 자세만 그 사본을 쓴다. 원본 파일은 해시로 고정돼 그대로 둔다.
init 330 python:
    R13_DARAM_HARD_EDGE={"assets/room13-pixel-world-daram-gray-gutter.webp":"assets/room13-pixel-acting-daram-world-hard.webp",
        "assets/room13-pixel-world-family-extra-gray.webp":"assets/room13-pixel-acting-daram-extra-hard.webp"}
    for _r13_de_spec in R13_ACTING.get("daram",{}).values():
        if isinstance(_r13_de_spec,dict) and _r13_de_spec.get("file") in R13_DARAM_HARD_EDGE:
            _r13_de_spec["file"]=R13_DARAM_HARD_EDGE[_r13_de_spec["file"]]
