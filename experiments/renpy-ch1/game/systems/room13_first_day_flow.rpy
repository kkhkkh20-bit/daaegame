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
    call r13_lines([("guard","신청서를 확인했습니다. 다돌 님과 다람이, 두 분이군요. 여관은 광장 안쪽에 있습니다."),("karo","짐은 제가 옮겨 드릴게요. 바퀴 축은 손을 봐야 하니 내일 다시 말씀드리죠.")],"life:arrival:entry")
    $ r13_flag("entry_corrected")
    $ r13_grant(["E02"],"입구에서 확인받은, 함께 들어왔다는 기록")
    call r13_lines([("daram","아빠, 빨리 여관 가자. 엄마가 기다릴 거야."),("dad","그래. 13호실이라고 했지.")],"life:arrival:direction")
    return

label r13_first_day_checkin:
    call r13_lines([("dad","아내 편지를 받고 왔습니다. 13호실에 묵고 있다고 하던데요."),("granny","부인이요? 며칠째 안 보여요. 방에 두고 간 물건은 그대로인데."),("daram","……엄마 여기 없어요?",{"expression":"anxious"}),(None,"다람이가 내 소매를 꼭 쥐었다. 마차에서 내내 들고 있던 과자 봉지가 구겨졌다."),("dad","편지에는 여기서 기다린다고 했습니다."),("granny","가족을 부른다는 말은 저도 들었어요. 그런데 며칠 전에 나가서는 돌아오지 않았어요."),("daram","엄마가 있던 방을 봐도 돼요? 엄마 물건이라도 보고 싶어요."),("granny","13호실이에요. 오늘 식사와 방값은 받지 않을게요. 내일부터 두 분 숙식은 하루 열 냥이고요."),("dad","우선 13호실부터 살펴보겠습니다.")],"life:arrival:inn")
    # 0.18.70 (owner): 다람이's disappointment that mom is not here (systems/room13_daram_mood.rpy).
    call r13_daram_arrival_miss
    $ r13_flag("lodging")
    $ r13_note_encounter("granny")
    return

label r13_mother_note:
    call r13_lines([("dad","(책상에 접힌 종이가 있다. 다람이 이름 옆에 작은 도토리가 그려져 있다.)",{"thought":True}),("daram","이 그림은 엄마가 나한테 쓰는 표시야."),(None,"‘다람아, 아빠랑 도착하면 이 방에 짐을 놓아. 내가 없으면 등불을 돌보는 분에게 내 소식을 물어봐. 방에 남긴 건 그대로 두고.’"),("daram","아빠랑 나한테 쓴 메모네. 엄마가 언제 적어 놓은 걸까?"),("dad","글씨 모양도 적어 두자. 아까 받은 편지하고 같이 다시 읽어 봐야겠어.")],"life:mother:note:v2")
    $ r13_grant(["M01"],"13호실 책상 위의 메모를 읽음")
    return

label r13_life_first_night:
    $ r13_edit(period=2)
    call r13_scene(R13_PLACES["room13"][1],R13_PLACES["room13"][0],"night")
    call r13_lines([("daram","엄마가 여기 있었던 건 맞지? 이불도 엄마가 꿰맨 것 같아."),("dad","응. 메모도 남겨 뒀고. 그런데 엄마가 지금 어디 있는지는 더 알아봐야겠어.")],"life:night1:plan:v2")
    if r13_has("mother_expected_family"):
        call r13_lines([("daram","메모에 아빠랑 내가 도착하면 이 방으로 오라고 했지."),("dad","응. 엄마도 우리가 올 걸 알고 있었어. 그런데 기다리던 방에는 없네.")],"life:night1:comparison")
    if r13_has("mother_lamplighter_lead"):
        call r13_lines([("daram","초롱 아저씨는 엄마를 기억할까?"),("dad","엄마를 마지막으로 언제 봤는지가 궁금하구나. 그런데 이름만 대면 알아볼까?")],"life:night1:known_lead")
    else:
        call r13_lines([("daram","등불 돌보는 분이 누구인지는 아직 모르지?"),("dad","응. 이 마을 사람이라면 누구 말인지 알 텐데.")],"life:night1:unknown_lead")
    call r13_lines([("dad","까로 아저씨한테 마차 일도 물어보고. 오늘은 여기서 쉬자."),("daram","응. 엄마 소식 찾으면 나한테도 꼭 말해 줘.")],"life:night1:rest")
    $ r13_flag("night1_seen")
    return

init 95 python:
    # Keep repeat questions consistent with the new arrival, without rewriting old saves.
    _r13_firstday_topic_lines=r13_conversation_topic_lines
    def r13_conversation_topic_lines(key):
        if store.room13.get("life_poc") and key=="granny_letter":
            return [("dad","아내가 저희를 부른다는 말을 직접 하던가요?"),("granny","네. 가족이 오면 13호실을 그대로 내주라고 했어요."),("dad","아내가 여관을 나간 건 언제입니까?"),("granny","며칠 됐어요. 날짜는 숙박 장부에 있고요."),("dad","아내가 마지막으로 누구를 만났는지 알아보겠습니다.")]
        if store.room13.get("life_poc") and key=="register":
            if store.room13.get("day",1)>1:
                return [("granny","13호실 그대로 쓰세요. 숙식은 하루 열 냥이고, 모자라면 적어 둘게요.")]
            return [("dad","아내 편지를 받고 왔습니다. 아내가 묵는 방을 볼 수 있습니까?"),("granny","13호실을 쓰세요. 두고 간 물건도 그대로예요."),("daram","엄마는 지금 어디 있어요?"),("granny","며칠째 안 보여요. 나간 뒤로 돌아오지 않았어요."),("dad","13호실부터 살펴보고, 아내가 언제 나갔는지도 여쭤보겠습니다."),("granny","오늘 식사와 방값은 받지 않을게요. 내일부터 두 분 숙식은 하루 열 냥이에요. 모자란 것은 장부에 적고 나중에 주세요."),("daram","아빠, 엄마가 남긴 것도 찾아보자.")]
        return _r13_firstday_topic_lines(key)
    _r13_firstday_topics=r13_topics
    def r13_topics(person):
        return [(key,spec) for key,spec in _r13_firstday_topics(person)
            # The old return-carriage question is replaced by life:karo on day 2.
            # Do not blanket-hide eligible resident questions on the first day.
            # Base availability still enforces every clue/day/case condition.
            if not (store.room13.get("life_poc") and key=="karo_road")]
