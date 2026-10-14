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

    _r13_firstday_notes=r13_first_mystery_notes
    def r13_first_mystery_notes():
        rows=_r13_firstday_notes()
        if store.room13.get("life_poc") and store.room13.get("case_state")=="pending":
            if r13_has("M01"):
                rows[0]=dict(title="등불을 돌보는 사람은 엄마를 알고 있을까?",fact="엄마는 메모에 등불을 돌보는 사람에게 소식을 물어보라고 적었다.",question="누구를 말하며, 언제 엄마를 만났을까?",hint="할머니나 식당에서 등불을 돌보는 사람이 누구인지 물어보자.",keys=["M01"])
        return rows

    _r13_life_present=r13_present
    def r13_present(person,key,identity=False):
        if key=="M01" and r13_has("M01"):
            if person in ("granny","nabi"):
                r13_flag("mother_lamplighter_lead")
                return [("dad","여기 적힌, 등불을 돌보는 분이 누구입니까?"),(person,"초롱을 말하는 것 같네요. 마을 등불을 돌보는 분이에요."),("dad","아내를 만났는지 직접 물어보겠습니다.")]
            if person=="resident_lamplighter":
                if store.room13["day"]<3:
                    return [(person,"그분이 남긴 글씨군요. 맡아 둔 것을 찾아볼게요. 내일 다시 와 주시겠어요?")]
                r13_flag("topic:lamplighter_warning")
                return [(person,"가족에게 전해 달라고 맡긴 봉투가 있어요. 여기서 길게 이야기하진 맙시다.")]
        return _r13_life_present(person,key,identity)

label r13_first_day_arrival:
    call r13_lines([("guard","신청 종이 확인했습니다. 다돌 님과 다람이, 두 분이군요. 여관은 광장 안쪽입니다."),("karo","짐은 제가 옮겨 드릴게요. 축은 손을 봐야 하니 내일 다시 말씀드리죠.")],"life:arrival:entry")
    $ r13_flag("entry_corrected")
    $ r13_grant(["E02"],"입구에서 확인받은, 함께 들어왔다는 기록")
    call r13_lines([("daram","아빠, 엄마가 있던 여관부터 가 보자."),("dad","그래. 편지를 보내신 할머니께 여쭤보자.")],"life:arrival:direction")
    return

label r13_first_day_checkin:
    call r13_lines([("dad","보내 주신 편지를 받고 왔습니다. 아내는 여기 있습니까?"),("granny","아직 돌아오지 않았어요. 방에 두고 간 물건도 그대로고요."),("dad","편지를 보내실 때도 없었습니까?"),("granny","네. 소식이 없어서 가족께 알려야겠다고 생각했어요. 기다리게 해서 미안해요."),("daram","엄마가 있던 방을 봐도 돼요?"),("granny","13호실이에요. 오늘 식사와 방값은 받지 않을게요. 내일부터 두 분 숙식은 하루 열 냥이고요."),("dad","우선 방부터 살펴보겠습니다.")],"life:arrival:inn")
    $ r13_flag("lodging")
    $ r13_note_encounter("granny")
    return

label r13_mother_note:
    call r13_lines([("dad","(책상에 접힌 종이가 있다. 다람이 이름 옆에 작은 도토리를 그려 놓았다.)",{"thought":True}),("daram","엄마가 나한테 쓰는 표시야."),(None,"‘먼저 도착했는데 내가 없으면, 저녁에 등불을 돌보는 분에게 내 소식을 물어봐. 방에 남긴 건 그대로 두고.’"),("dad","(언제 쓴 메모일까. 이 사람은 아내를 만났을지도 모른다.)",{"thought":True})],"life:mother:note")
    $ r13_grant(["M01"],"13호실 책상 위의 메모를 읽음")
    return

label r13_life_first_night:
    $ r13_edit(period=2)
    call r13_scene(R13_PLACES["room13"][1],R13_PLACES["room13"][0],"night")
    call r13_lines([("daram","엄마가 여기 있었던 건 맞지? 이불도 엄마가 꿰맨 것 같아."),("dad","응. 메모도 남겨 뒀고. 그런데 지금 어디 있는지는 더 알아봐야겠어."),("daram","내일 등불 돌보는 분부터 찾아보자."),("dad","그래. 까로 아저씨한테 마차도 물어보고. 오늘은 여기서 쉬자.")],"life:night1:plan")
    $ r13_flag("night1_seen")
    return

init 95 python:
    # Keep repeat questions consistent with the new arrival, without rewriting old saves.
    _r13_firstday_topic_lines=r13_conversation_topic_lines
    def r13_conversation_topic_lines(key):
        if store.room13.get("life_poc") and key=="granny_letter":
            return [("dad","소식이 끊겨서 저희에게 편지를 보내셨다고요?"),("granny","네. 물건도 두고 갔는데 돌아오지 않아서요."),("dad","마지막으로 누굴 만났는지 알아보겠습니다.")]
        if store.room13.get("life_poc") and key=="register":
            if store.room13.get("day",1)>1:
                return [("granny","13호실 그대로 쓰세요. 숙식은 하루 열 냥이고, 모자라면 적어 둘게요.")]
            return [("granny","13호실을 쓰세요. 오늘은 무료이고, 내일부터 두 분 숙식은 하루 열 냥이에요.")]
        return _r13_firstday_topic_lines(key)
    _r13_firstday_topics=r13_topics
    def r13_topics(person):
        return [(key,spec) for key,spec in _r13_firstday_topics(person)
            # The old return-carriage question is replaced by life:karo on day 2.
            # Do not blanket-hide eligible resident questions on the first day.
            # Base availability still enforces every clue/day/case condition.
            if not (store.room13.get("life_poc") and key=="karo_road")]
