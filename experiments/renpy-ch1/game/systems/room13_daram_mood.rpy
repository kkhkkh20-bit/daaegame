# 다람이's face follows what she says (owner 0.18.71): "다람의 태도도 확실히 어리니까 엄마를 못 만나는
# 실망감과 이런 것들을 대사에 잘 넣고 표정에도 넣어야 할 것 같아. 지금 다람에 대한 표정들이 대사와 함께
# 적용이 잘 안 되어 있는 것 같아."
#   Of about 300 다람이 lines only ~50 had a face chosen (inline or room13-fullbody-line-emotions.json);
#   the rest showed the neutral face. A line with no chosen face now gets one from its words:
#   missing mom / fear -> anxious, delight -> joy, a sudden "어?" -> surprise, sulking -> angry,
#   embarrassment -> flustered. Faces chosen by hand (inline, per-line cue, scene direction) always win.
#   Full-body faces available: neutral, joy, anxious, surprise, angry, flustered.
init 141 python:
    import re as _r13_mood_re
    R13_DARAM_MOOD_RULES=(
        ("surprise",_r13_mood_re.compile(r"^(어[?!.…]|앗|엇|어어|깜짝|헉)|진짜\?|정말\?|벌써\?")),
        ("angry",_r13_mood_re.compile(r"치사|나빠|미워|흥[.!]|거짓말쟁이|왜 맨날|싫다니까|화났")),
        ("flustered",_r13_mood_re.compile(r"아니야, 그게|그게 아니라|부끄|몰라, 몰라|안 울어|울면 안 돼|들켰")),
        ("anxious",_r13_mood_re.compile(r"엄마.*(없|어디|안 와|못 만|보고 싶|언제|왜)|보고 싶|무서|무섭|괜찮을까|괜찮아\?|(?<!안 )아파|싫어|어떡해|어떻게 해|가지 마|놓지 마|혼자|안 오면|……$|^……|훌쩍|울었|……!$")),
        ("joy",_r13_mood_re.compile(r"헤헤|와아|우와|와!|좋아!|좋다|신난|맛있|예쁘|찾았다|찾았어!|됐다|최고|고마워|약속!|^응!|야호|따뜻하겠다")),
        # A lively exclamation of more than a word, without trailing-off dots, reads as delight.
        ("joy",_r13_mood_re.compile(r"^(?!.*……)(?=.{5,}).*[^?]!( |$)")),
    )

    def r13_daram_mood(text):
        plain=_r13_mood_re.sub(r"\{[^}]*\}|【|】","",text or "").strip()
        for emotion,rule in R13_DARAM_MOOD_RULES:
            if rule.search(plain):return emotion
        return None

    _r13_mood_line_performance=r13_line_performance
    def r13_line_performance(identity,index,packet):
        expression,pose=_r13_mood_line_performance(identity,index,packet)
        if packet[0]!="daram" or (len(packet)>2 and packet[2]):return expression,pose
        if pose not in ("neutral","thinking"):return expression,pose
        cue=R13_FULLBODY_LINES.get("lines",{}).get(identity,{}).get(str(index))
        if cue and cue.get("person")=="daram" and cue.get("text")==packet[1]:return expression,pose
        mood=r13_daram_mood(packet[1])
        if not mood:return expression,pose
        return R13_FULLBODY_TO_LEGACY.get(mood,expression),mood

    # 다람이 misses mom: two night talks in 13호 while the family has not met her yet.
    # She brings it up herself; Dad only answers. Nothing is recorded.
    R13_DARAM_MISS_TALKS=[
        ("night:miss_mom","다람이가 엄마 이야기를 꺼낸다",lambda:not r13_has("mom_reunited") and store.room13["day"]<=7,[
            (None,"다람이가 이불 끝을 코까지 끌어 올렸다."),
            ("daram","아빠. 이불에서 엄마 냄새 나.",{"expression":"anxious"}),
            ("dad","그래? 엄마가 이 이불을 덮고 잤나 보다."),
            ("daram","나 마차에서 엄마한테 줄 과자 반 남겨 놨다? 아직 안 먹었어.",{"expression":"joy"}),
            ("dad","잘했네. 엄마 만나면 그때 같이 먹자."),
            ("daram","……엄마는 우리가 온 거 알까?",{"expression":"anxious"}),
            ("dad","알게 될 거야. 아빠가 꼭 알릴게."),
            ("daram","엄마가 우리 보기 싫어서 나간 건 아니지?",{"expression":"anxious"}),
            ("dad","절대 아니야. 엄마는 다람이를 제일 보고 싶어 했어."),
            ("daram","……응. 그럼 엄마 만나면 과자부터 줄 거야. 내가 먼저.",{"expression":"joy"})]),
        ("night:miss_mom2","다람이가 엄마에게 서운한 마음을 말한다",lambda:not r13_has("mom_reunited") and store.room13["day"]>=4 and "night:miss_mom" in store.room13.get("read_topics",[]),[
            ("daram","아빠, 엄마는 왜 편지도 안 해? 우리가 여기 있는데.",{"expression":"angry"}),
            ("dad","편지를 보내면 누가 엄마를 찾아낼까 봐 조심하는 걸 거야."),
            ("daram","그래도……. 나 같으면 몰래라도 했을 거야.",{"expression":"angry"}),
            ("dad","엄마도 그러고 싶을 거야. 지금은 그게 더 위험해서 참고 있는 거고."),
            ("daram","……과자 반은 그래도 엄마 거야. 화났어도.",{"expression":"flustered"}),
            ("dad","그래. 엄마 몫은 엄마 거지."),
            ("daram","만나면 제일 먼저 꽉 안아 줄 거야. 그다음에 화낼 거야.",{"expression":"joy"})]),
    ]
    for _k,_t,_c,_l in R13_DARAM_MISS_TALKS:
        ROOM13["topics"][_k]=dict(npc="daram",title=_t,day=[2,14],need=["lodging"],give=[],flags=[],lines=list(_l))
        R13_NIGHT_TALK_COND[_k]=_c

label r13_daram_arrival_miss:
    # After granny says mom has not been seen for days: a child's disappointment, before the room.
    call r13_lines([(None,"계단 앞에서 다람이가 걸음을 멈췄다."),
        ("daram","엄마가 13호실에서 기다린다고 했잖아. 내가 먼저 문 두드리기로 했는데.",{"expression":"anxious"}),
        ("dad","그랬지. 아빠도 엄마가 문을 열어 줄 줄 알았어."),
        ("daram","과자도 반 남겨 놨는데……. 엄마 주려고.",{"expression":"anxious"}),
        ("dad","잘 갖고 있어. 엄마 만나면 그때 주자."),
        ("daram","……응. 울면 안 돼. 엄마 찾으려면 눈 크게 떠야 하니까.",{"expression":"flustered"})],"life:arrival:daram_miss")
    return
