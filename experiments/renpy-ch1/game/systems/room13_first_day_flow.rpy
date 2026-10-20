# Guided first evening. Later campaign plot remains in its existing modules.
init 94 python:
    _r13_life_new=r13_new
    def r13_new():
        state=_r13_life_new()
        state["life_poc"]=True
        return state

    ROOM13["evidence"]["M01"]=dict(id="M01",name="엄마가 남긴 짧은 메모",kind="물증",
        establishes="엄마는 가족이 도착하면 등불을 돌보는 사람에게 자신의 소식을 물어보라고 적었다.",
        does_not_establish="",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["objects"]["room13"]["mother_note"]=dict(rect=[150,385,94,32],
        text="엄마의 메모",need=["lodging"],give=[],flags=[],life_note=True)
    _r13_firstday_visible=r13_object_visible
    def r13_object_visible(spec):
        if spec.get("life_note") and not store.room13.get("life_poc"):return False
        return _r13_firstday_visible(spec)
    _r13_firstday_places=r13_places
    def r13_places():
        if store.room13.get("life_poc") and store.room13.get("day")==1:
            if not r13_has("entry_corrected"):return ["gate"]
            return ["gate","square","inn","hall","room13"] if r13_has("lodging") else ["gate","square","inn"]
        return _r13_firstday_places()
    _r13_firstday_connections=r13_local_connections
    def r13_local_connections():
        if store.room13.get("life_poc") and store.room13.get("day")==1:
            if store.room13.get("location")=="gate":return [("square","광장으로"),("inn","여관으로")]
            if store.room13.get("location")=="square":return [("inn","여관으로"),("gate","마을 입구로")]
        return _r13_firstday_connections()
    _r13_firstday_bed=r13_bed_available
    def r13_bed_available(key):
        if store.room13.get("life_poc") and store.room13.get("day")==1:
            return key=="bed" and store.room13.get("location")=="room13" and r13_has("M01") and r13_has("E03")
        return _r13_firstday_bed(key)

    def r13_bed_blocked_reason(key):
        # Day 1: sleep waits until the room is read, but the bed still says so (owner, 0.18.22).
        s=store.room13 or {}
        if key!="bed" or not r13_has("lodging") or r13_bed_available(key):return None
        if not (s.get("life_poc") and s.get("day")==1 and s.get("location")=="room13"):return None
        if not r13_has("M01"):return "아직은 아니다. 책상 위를 먼저 살펴보자"
        if not r13_has("E03"):return "아직은 아니다. 이불부터 살펴보자"
        return None

    _r13_firstday_notes=r13_first_mystery_notes
    def r13_first_mystery_notes():
        rows=_r13_firstday_notes()
        if store.room13.get("life_poc") and store.room13.get("case_state")=="pending":
            if r13_has("M01"):
                rows[0]=dict(title="등불을 돌보는 사람은 엄마를 알고 있을까?",fact="엄마는 메모에 등불을 돌보는 사람에게 소식을 물어보라고 적었다.",question="누구를 말하며, 언제 엄마를 만났을까?",hint="이 마을에 오래 산 사람이라면 누구를 말하는지 알 것이다. 메모를 읽은 사람은 아직 아빠와 다람이뿐이다.",keys=["M01"])
        return rows

    _r13_life_present=r13_present
    def r13_present(person,key,identity=False):
        if key=="M01" and r13_has("M01"):
            if person in ("granny","nabi"):
                r13_flag("mother_lamplighter_lead")
                return [("dad","여기 적힌 ‘등불을 돌보는 분’이 누구입니까?"),(person,"초롱을 말하는 것 같네요. 마을 등불을 돌보는 분이에요."),("dad","등불을 돌보는 분께 아내를 만났는지 직접 물어보겠습니다.")]
            if person=="resident_lamplighter":
                if store.room13["day"]<3:
                    return [(person,"그분이 남긴 글씨군요. 맡아 둔 것을 찾아볼게요. "+("모레" if store.room13["day"]==1 else "내일")+" 다시 와 주시겠어요?")]
                r13_flag("topic:lamplighter_warning")
                return [(person,"가족에게 전해 달라고 맡긴 봉투가 있어요. 여기서 길게 이야기하진 맙시다.")]
        return _r13_life_present(person,key,identity)

label r13_first_day_arrival:
    call r13_lines([("guard","신청서를 확인했습니다. 다돌 님과 다람이, 두 분이구려. 여관은 광장 안쪽에 있습니다."),("karo","짐은 제가 옮겨 드릴게요. 바퀴 축은 손을 봐야 하니 내일 다시 말씀드리죠.")],"life:arrival:entry")
    $ r13_flag("entry_corrected")
    $ r13_grant(["E02"],"입구에서 확인받은, 함께 들어왔다는 기록")
    call r13_lines([("daram","아빠, 빨리 여관 가자. 엄마가 기다릴 거야."),("dad","그래. 13호실이라고 했지.")],"life:arrival:direction")
    return

label r13_first_day_checkin:
    call r13_lines([('granny', '다돌 씨죠? 아이구, 손이 빨갛네. 난로부터 쬐어요.'), ('granny', '손 바로 대면 아파. 이걸로 감싸고 천천히.'), ('daram', '고맙습니다.'), ('dad', '아내는 어디 있습니까?'), ('granny', '며칠째 안 보여요. 조사하러 나가면 밤낮이 없던 사람이라.'), ('daram', '기다린댔는데.'), ('granny', '방은 그대로 뒀지. 올라가 봐요.'), ('dad', '마지막으로 어디 간다고 했습니까?'), ('granny', '내게 일일이 말하진 않았어요. 밥도 식혀 놓고 들어오던걸.'), ('dad', '마지막으로 돌아온 날은 기억하십니까?'), ('granny', '밥상은 매일 차렸죠. 어느 날부터 안 왔더라…… 방부터 보세요. 아이가 떨고 있잖아요.')],"life:arrival:inn")
    # 0.18.75 (owner): 다람이's disappointment that mom is not here (systems/room13_daram_mood.rpy).
    call r13_daram_arrival_miss
    $ r13_flag("lodging")
    $ r13_note_encounter("granny")
    return

label r13_mother_note:
    call r13_lines([(None, '메모: “내가 자리를 비웠으면 광장 등의 초롱에게 소식을 물어봐. 물건은 책상 아래에 두었어.” 끝에 작은 도토리.'), ('daram', '이건 엄마 거다. 도토리 삐뚤어.'), ('dad', '책상 아래라고 했지.')],"life:mother:note:v2")
    $ r13_grant(["M01"],"13호실 책상 위의 메모를 읽음"); r13_flag("mother_lamplighter_lead")
    return

label r13_life_first_night:
    $ r13_edit(period=2)
    call r13_scene(R13_PLACES["room13"][1],R13_PLACES["room13"][0],"night")
    call r13_lines([("daram","엄마가 여기 있었던 건 맞지? 이불도 엄마가 꿰맨 것 같아."),("dad","응. 메모도 남겨 뒀고. 그런데 엄마가 지금 어디 있는지는 더 알아봐야겠어.")],"life:night1:plan:v2")
    if r13_has("mother_expected_family"):
        call r13_lines([('dad', '편지에는 도토리가 없네.'), ('daram', '엄마가 잊었나?'), ('dad', '그럴 수도 있고, 누가 대신 써 줬을 수도 있어.'), ('daram', '그럼 초롱한테 물어보자.')],"life:night1:comparison")
    if r13_mother_knowledge()["promised"] and not r13_mother_knowledge()["received"]:
        call r13_lines([("daram","초롱 아저씨가 엄마 봉투를 맡고 있대."),("dad","응. 어디서 받을 수 있는지 바로 물어볼 수 있어. 엄마가 어떤 글을 남겼을까?")],"life:night1:promised")
    elif r13_mother_knowledge()["recognized"]:
        call r13_lines([("daram","초롱 아저씨가 엄마를 알아봤지."),("dad","응. 엄마와 언제 어디서 만났는지도 더 들어 보고 싶어.")],"life:night1:recognized")
    elif r13_mother_knowledge()["named"]:
        call r13_lines([("daram","메모에 적힌 분은 초롱 아저씨지?"),("dad","응. 그분도 엄마를 기억할까?")],"life:night1:known_lead")
    else:
        call r13_lines([("daram","등불 돌보는 분이 누구인지는 아직 모르지?"),("dad","응. 이 마을 사람이라면 누구 말인지 알 텐데.")],"life:night1:unknown_lead")
    call r13_lines([('daram', '엄마가 내일도 안 오면?'), (None, '나는 방금 펴 놓은 침구를 다시 눌렀다. 마차에서 가운데 자리를 달라던 아이였다.'), ('dad', '아침에 초롱 만나고, 돌아갈 차도 알아볼게. 여기 앉아 기다리기만 하진 않을 거야.'), ('daram', '차도 없으면?'), ('dad', '그다음 방법을 알아봐야지. 너 혼자 남겨 두지는 않아.'), (None, '다람이가 과자 봉지 끝을 두 번 접었다.'), ('daram', '눅눅해지겠다.'), ('dad', '잘 싸 두자.'), ('daram', '여기 놓을래. 엄마가 먼저 올 수도 있잖아.'), ('dad', '그래.'), ('daram', '엄마 오면 깨워 줘.'), ('dad', '응.'), (None, '문밖에서 발소리가 멈췄다. 노크하고 들어온 사람은 침구를 가져온 종업원이었다. 나는 한참 문손잡이를 놓지 못했다.')],"life:night1:rest")
    $ r13_flag("night1_seen")
    return

init 95 python:
    # Keep repeat questions consistent with the new arrival, without rewriting old saves.
    _r13_firstday_topic_lines=r13_conversation_topic_lines
    def r13_conversation_topic_lines(key):
        if store.room13.get("life_poc") and key=="granny_letter":
            return [('dad', '아내는 어디 있습니까?'), ('granny', '며칠째 안 보여요. 조사하러 나가면 밤낮이 없던 사람이라.'), ('daram', '기다린댔는데.'), ('granny', '방은 그대로 뒀지. 올라가 봐요.'), ('dad', '마지막으로 어디 간다고 했습니까?'), ('granny', '내게 일일이 말하진 않았어요. 밥도 식혀 놓고 들어오던걸.'), ('dad', '마지막으로 돌아온 날은 기억하십니까?'), ('granny', '밥상은 매일 차렸죠. 어느 날부터 안 왔더라…… 방부터 보세요. 아이가 떨고 있잖아요.')]
        if store.room13.get("life_poc") and key=="register":
            if store.room13.get("day",1)>1:
                return [("granny","13호실 그대로 쓰세요. 부인이 잡아 둔 방이에요.")]
            return [('granny', '다돌 씨죠? 아이구, 손이 빨갛네. 난로부터 쬐어요.'), ('granny', '손 바로 대면 아파. 이걸로 감싸고 천천히.'), ('daram', '고맙습니다.'), ('dad', '아내는 어디 있습니까?'), ('granny', '며칠째 안 보여요. 조사하러 나가면 밤낮이 없던 사람이라.'), ('daram', '기다린댔는데.'), ('granny', '방은 그대로 뒀지. 올라가 봐요.'), ('dad', '마지막으로 어디 간다고 했습니까?'), ('granny', '내게 일일이 말하진 않았어요. 밥도 식혀 놓고 들어오던걸.'), ('dad', '마지막으로 돌아온 날은 기억하십니까?'), ('granny', '밥상은 매일 차렸죠. 어느 날부터 안 왔더라…… 방부터 보세요. 아이가 떨고 있잖아요.')]
        return _r13_firstday_topic_lines(key)
    _r13_firstday_topics=r13_topics
    def r13_topics(person):
        return [(key,spec) for key,spec in _r13_firstday_topics(person)
            # The old return-carriage question is replaced by life:karo on day 2.
            # Do not blanket-hide eligible resident questions on the first day.
            # Base availability still enforces every clue/day/case condition.
            if not (store.room13.get("life_poc") and key=="karo_road")]
