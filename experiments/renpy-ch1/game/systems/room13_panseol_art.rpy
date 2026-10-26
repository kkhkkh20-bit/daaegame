# 판돌의 누나 판설(이름: 2026-10-26 소유자 "판설"). 그림은 HIDDEN-P3 세 장(중립·경계·피곤).
# 경계는 불안(anxious) 자리에, 피곤은 자기 이름(tired)으로 둔다. 다른 감정은 기존 규칙대로 중립을 쓴다.
# 대본에서는 7일 판돌이 이름을 말한 뒤부터 이름표로 말한다(그 전에는 「안쪽 여자」 지문).
init 326 python:
    R13_PANSEOL_FILES={e:"assets/panseol/panseol-%s.webp"%e for e in ("neutral","anxious","tired")}
    R13_PANSEOL_FACE="assets/panseol/panseol-face.webp"
    R13_FULLBODY["people"]["npc_panseol"]=dict(name_ko="판설",crop=[139,19,850,1471],figure=[143,23,842,1463],
        images={e:dict(file=f,size=[1024,1536],native_detail=True,smooth_source=True) for e,f in R13_PANSEOL_FILES.items()})
    for _ps_file in R13_PANSEOL_FILES.values():R13_FULLBODY_FILES.add(_ps_file)
    _r13_ps_body=dict(file=R13_PANSEOL_FILES["neutral"],crop=[143,23,842,1463],nearest=False,foot=[420,1462],
        facing="front",contact="standing",head=[30,0,470,470],reviewed=True,posture="standing")
    _r13_ps_face=dict(file=R13_PANSEOL_FACE,crop=[0,0,470,470],nearest=False,dedicated_avatar=True,facing="front",gaze="viewer")
    CAST["npc_panseol"]={key:dict(_r13_ps_face if key.startswith("avatar_") else _r13_ps_body) for key in CAST["elder"]}
    # 이름표(MS14_SPEAKERS·R13_NAMES)는 대본 검사보다 먼저 서야 해서 room13_v111_later_bindings.rpy 에 있다.
