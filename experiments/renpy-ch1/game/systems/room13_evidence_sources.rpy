# 0.20.14: New-world testimony shows its actual speaker rather than a generic paper.
# These are authorship metadata only. No record is granted and no proof rule is changed.
# Registered after the authored/new-world catalog (init 300/319).
init 329 python:
    R13_V111_TESTIMONY_SOURCES={
        "E19":"bami",                    # 밤이: 전에 강 쪽에서 엄마를 봤다.
        "E20":"guard",                   # 돌목의 첫 말.
        "E24":"resident_nero",           # 네로: 어젯밤 나갔다가 돌아왔다.
        "E25":"guard",                   # 돌목의 재확인 진술.
        "E21":"bami",                    # 밤이: 양동이가 넘어졌을 때 처마에 있었다.
        "E07_NUBI":"resident_nubi",       # 누비의 직접 진술.
        "NW_INNER_PRICE":"resident_madam",# 백 부인의 돌값 설명.
        "NW_MUSOE_DEEP":"resident_somi",  # 무쇠에 관해 말한 사람은 솜이.
        "NW_KKOMI_NOSTONE":"kid_kkomi",   # 꼬미: 우린 표도 없고 돌도 없어.
    }
    for _r13_ev_key,_r13_ev_person in R13_V111_TESTIMONY_SOURCES.items():
        ROOM13["evidence_sources"]["V111:"+_r13_ev_key]=_r13_ev_person
