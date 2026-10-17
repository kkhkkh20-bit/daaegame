# 0.19.17 선택지 검수 뒤 조정자 정리 (init 201, 검수 파일 room13_ask_review_*.rpy 뒤)
init 201 python:
    # 부리의 답은 장치를 "돌리는" 동안 붙잡을 사람 이야기다(검수 2 판단 필요 1).
    if "w2_buri_ops" in ROOM13["topics"]:
        _fa_was=ROOM13["topics"]["w2_buri_ops"]["title"]
        ROOM13["topics"]["w2_buri_ops"]["title"]="장치를 돌리려면 누가 있어야 하니?"
        R13_QUESTION_SUMMARIES["장치를 돌리려면 누가 있어야 하니?"]="장치를 돌리는 동안 누가 있어야 하는지 묻는다"

    # 사건 뒤(8~10일) 사자 선생님: 대피소 이야기(11일~) 전이라 아빠가 "환자를 받을 수 있느냐"를 먼저 꺼낼 근거가 없다.
    #   선생님이 먼저 환자 이야기를 꺼내므로, 아빠는 걱정을 묻기만 한다(검수 2 판단 필요 2).
    if "life:resident_teacher:after" in ROOM13["topics"]:
        ROOM13["topics"]["life:resident_teacher:after"]["title"]="요즘 걱정되는 일이 있으십니까?"
        R13_QUESTION_SUMMARIES.setdefault("요즘 걱정되는 일이 있으십니까?","요즘 걱정되는 일이 있는지 묻는다")
