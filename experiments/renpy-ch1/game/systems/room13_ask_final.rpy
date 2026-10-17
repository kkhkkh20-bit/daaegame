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

    # 모모 그림에는 초록 숄이 있다(어깨에 두르고 여미고 있다). 검수 1의 "의자에 개켜 둔 숄"은 그림과 어긋나 되돌린다.
    if "ep6:st_momo_glasses" in ROOM13["topics"]:
        _fa_t=ROOM13["topics"]["ep6:st_momo_glasses"]
        _fa_t["title"]="그 초록 숄을 늘 여미고 계시네요"
        R13_QUESTION_SUMMARIES["그 초록 숄을 늘 여미고 계시네요"]="늘 여미는 초록 숄이 누구 것인지 묻는다"
        _fa_t["variants"]=[(None,[
            ("resident_momo","제 숄이 아니에요. 첫 겨울에 보호소로 간 동생 거예요."),
            ("resident_momo","옛 마을 물건이라면 뭐든 산다고들 흉보죠. 사람은 가도 물건은 남으니까, 그거라도 붙잡아 두는 거예요."),
            ("resident_momo","언젠가 누가 ‘이건 누구 것이었소’ 하고 물어봐 주면 좋겠어요. 그럼 그 이름을 한 번 더 말할 수 있으니까요.")])]
