# The arrival is an investigation with persistent observations, not an automatic pardon.
default winter_entry = False
default winter_entry_selection = []
default winter_topic_tab = "talk"

init 47 python:
    def winter_collect(s, key, source="entry"):
        n=winter_copy.deepcopy(s)
        if key not in n["evidence"]:
            n["evidence"].append(key)
            n["records"][key]=dict(day=n["day"],period=winter_period(n),source=source,place=n["location"])
        return n

    def winter_entry_proof(s, selected):
        held=set(selected)
        return held.issubset(set(s["evidence"])) and (
            {"entry_permit","entry_copy"}.issubset(held) or
            {"entry_permit","entry_rule"}.issubset(held))

    def winter_reason_feedback(s, claim, selected):
        relevant=set(k for path in claim["paths"] for k in path)
        if relevant.intersection(selected):return claim["partial"]
        return "그 기록이 틀렸다는 뜻은 아닙니다. 지금 이 주장과 어떻게 이어지는지는 아직 확인되지 않았습니다."

    def winter_hearing_limit(s):
        return 3 + int(winter_has(s,"doto_supported")) + int(winter_has(s,"permission") and s["witness"] in ("available","safe")) + int("meal" in s["done"])

    def winter_support_lines(s):
        result=[]
        if winter_has(s,"doto_supported"):
            result.append(("doto","제가 적은 날짜와 목격담이 맞습니다. 말을 바꾸라고 찾아온 사람도 있었어요. 이분 말씀 끝까지 들어 주세요."))
        if winter_has(s,"permission") and s["witness"] in ("available","safe"):
            result.append(("resident_nubi","이젠 제 이름으로 말하겠습니다. 그날 수레를 민 건 저예요."))
        if "meal" in s["done"]:
            result.append(("nabi","며칠 같이 지내 봤어. 말만 던지고 도망갈 사람은 아니야. 자료부터 보자고."))
        return result

label winter_arrival:
    $ winter_entry=True
    $ winter=dict(winter,location="gate")
    call winter_scene("winter_carriage","고개 아래 · 마을로 가는 마차","calm")
    call winter_lines([("daram","아빠. 아까부터 같은 쪽만 먹지?"),("dad","어느 쪽?"),("daram","큰 거 있는 쪽. 봉지 돌려 봐."),("dad","들켰네."),("daram","이건 남겨. 엄마 것도 있어야지."),("dad","눅눅해지겠다."),("daram","그래도 가져왔다는 게 중요하지."),(None,"다람이 봉지 입구를 접어 가방 안쪽에 넣었다."),("daram","편지 줘 봐. 여관 이름 또 까먹었어."),("dad","겨울잠 여관."),("daram","그건 기억나. 방 이름이…… 아니, 방은 안 썼네."),("dad","난로 옆에서 기다리라고 했지."),("daram","엄마가 먼저 와 있으면 내가 먼저 볼 거야. 아빠는 짐 들어."),("dad","그럼 네 가방도 내 짐인가?"),("daram","이건 내가 들 거야."),(None,"편지의 접힌 자리를 폈다. 열흘 전 날짜. 그 뒤로 답장은 오지 않았다.")],"carriage")
    $ winter=winter_collect(winter,"invitation")
    call winter_lines([("karo","앞에서 멈춥니다. 짐은 두고 먼저 내려오세요."),("daram","여관 앞 아니에요?"),("karo","문에서 손님부터 확인한대. 어제 묵은 대피소보다 따뜻할 거야."),("dad","돌아가는 차편은요?"),("karo","우리가 넘은 고개가 밤에 무너졌어요. 오늘 내려온 길은 대피소까지만 이어져요."),("daram","그럼 아저씨도 여기 있어요?"),("karo","응. 내 짐도 같이 내려야지.")],"carriage_stop")
    call winter_scene("winter","마을 입구 · 검문 초소","search")
    call winter_lines([("dad","다람아, 손."),("daram","잠깐. 목도리 꼈어."),("dad","풀었어. 이제 내려와."),(None,"눈에 발이 푹 잠겼다. 초소 안에서 장부를 든 경비가 나왔다."),("guard","성인 한 분. 접수번호 73-2 맞습니까?"),("dad","딸도 함께입니다."),("guard","아이 등록은 없네요. 얘야, 왼쪽 초소 난로가 따뜻해. 거기서 기다리자."),("daram","아빠도?"),("guard","아버지는 여기서 서류를 보시고요. 아이는 안 춥게 해 줄 겁니다."),("dad","따로 보내지는 않겠습니다."),("guard","명부에 없는 사람은 분리 대기입니다. 문 닫기 전에는 처리해야 합니다."),("karo","잠깐요. 출발할 때 두 분 서류를 받았는데."),("guard","그럼 원본을 보여 주세요. 여기 적힌 건 한 명입니다."),("daram","아빠. 내 가방 잡아 줘."),("dad","응. 넌 내 옆에 있어.")],"gate")
    jump winter_entry_loop

label winter_entry_loop:
    window hide
    hide winter_visitor
    call screen winter_entry_hub
    $ winter_entry_choice=_return
    if winter_entry_choice=="permit":
        call winter_lines([("karo","짐칸 말고 안주머니에 넣었죠. 여기 있어요."),("dad","숙박 보증 전달증이군요."),("karo","겨울잠 여관에서 보내온 거예요. 접수 도장까지 받고 출발했어요."),("daram","여기 내 이름 있다."),(None,"73-2. 성인 한 명, 아동 한 명. 아래에는 숙박 보증인의 서명이 있었다.")],"entry_permit")
        $ winter=winter_collect(winter,"entry_permit")
    elif winter_entry_choice=="ledger":
        call winter_lines([("dad","같은 접수번호인지 보겠습니다. 그 줄만 보여 주세요."),("guard","73-2. 성인 한 명. 아이 칸은 비었습니다."),("dad","언제 옮겨 쓴 겁니까?"),("guard","오늘 새벽 인계받았습니다. 제가 아이 이름을 빼지는 않았어요."),(None,"번호 아래 한 줄이 비어 있다. 다람의 이름을 묻기도 전에 만들어진 명부다.")],"entry_copy")
        $ winter=winter_collect(winter,"entry_copy")
    elif winter_entry_choice=="rule":
        call winter_lines([("daram","문 옆에도 종이 있어. 아래가 접혔네."),("dad","손 베이지 않게. 내가 펼칠게."),(None,"보증번호가 있는 동반 가족은 보증인에게 함께 인계한다. 분리 대기는 원본 대조 후 집행한다."),("guard","규정은 맞습니다. 하지만 보증이 확인돼야 합니다.")],"entry_rule")
        $ winter=winter_collect(winter,"entry_rule")
    elif winter_entry_choice=="road":
        call winter_lines([("daram","아빠. 그냥 다른 마을로 가면 안 돼?"),("dad","고개가 열리면 갈 수 있어."),("daram","그때까지 여기 있어야 해?"),("dad","우선 같이 있을 방부터 구하자. 엄마가 기다리라고 한 곳으로.")],"entry_road")
    elif winter_entry_choice=="present":
        $ winter_selected=[]
        call screen winter_evidence(True)
        if _return:
            if winter_entry_proof(winter,winter_selected):
                jump winter_entry_reason
            elif "invitation" in winter_selected:
                call winter_lines([("guard","가족이 보낸 편지인 건 알겠습니다. 그래도 숙박 보증 접수와 같은 서류는 아닙니다."),("karo","제가 가져온 전달증도 같이 봐 주세요. 도장이 있는 쪽이요.")],"entry_letter_reply")
            else:
                call winter_lines([("guard","제가 대조할 것은 접수번호와 동반 인원입니다. 다른 기록만으로 명부를 고칠 수는 없습니다.")],"entry_other_reply")
    jump winter_entry_loop

label winter_entry_reason:
    call winter_lines([("guard","번호가 같은데 인원이 다르군요. 그렇다고 전달증만 보고 들일 수는……"),("karo","도장도 보세요. 같은 접수처잖아요."),("guard","원본은 확인했습니다. 무엇을 정정해 달라는 겁니까?")],"entry_counter")
    menu:
        "어떤 점을 바로잡아야 할까?"
        "새로 아이 등록을 신청한다":
            call winter_lines([("guard","신규 신청이면 분리 대기 절차부터입니다."),("daram","근데 내 이름 이미 있잖아. 또 적어야 해?"),("dad","잠깐만요. 원래 접수 내용을 다시 보겠습니다.")],"entry_new_wrong")
            jump winter_entry_loop
        "원본에 있는 동반 가족과 보증번호를 명부에 복원한다":
            pass
        "명부를 쓴 사람이 범인이라고 단정한다":
            call winter_lines([("guard","누가 왜 틀렸는지는 아직 모릅니다. 저도 전달받은 명부예요."),("dad","그렇군요. 지금 바로 확인할 수 있는 내용부터 정정합시다.")],"entry_blame_wrong")
            jump winter_entry_loop
    call winter_lines([("dad","미등록이 아닙니다. 원본의 동반 가족을 옮겨 적지 않은 겁니다."),("guard","……인원 두 명. 보증번호 유지. 정정 사유는 원본 대조."),("dad","가족은 보증인에게 함께 인계하는 규정도 적용해 주세요."),("guard","여관으로 함께 가십시오. 정정 사본도 드리겠습니다."),("karo","제가 짐까지 같이 옮길게요."),("guard","보증은 열나흘째 공동 심의까지입니다. 그 전에 갱신하지 못하면 다시 확인합니다."),("daram","이제 손 놔도 돼?"),("dad","문 나갈 때까진 잡고 있자.")],"entry_won")
    $ winter=winter_flag(winter,"entry_corrected")
    $ winter_entry=False
    call winter_scene("front","겨울잠 여관 · 접수대","calm")
    play sound "assets/door.wav" volume .35
    call winter_lines([("daram","아빠. 난로 옆에 아무도 없어."),("dad","먼저 할머니께 물어보자."),("karo","짐은 문 옆에 놓을게요. 난 마구간에 있으니 필요하면 불러요.")],"inn_arrive")
    $ winter=dict(winter,location="inn")
    jump winter_day

screen winter_entry_hub():
    modal True
    default ready=False
    timer .4 action SetScreenVariable("ready",True)
    add Transform("guard world",size=(240,360),fit="contain") xpos 330 ypos 215
    add Transform("karo world",size=(235,330),fit="contain") xpos 865 ypos 255
    button:
        xpos 330 ypos 215 xsize 240 ysize 360 background None
        action Return("ledger") sensitive ready
    button:
        xpos 865 ypos 255 xsize 235 ysize 330 background None
        action Return("permit") sensitive ready
    button:
        xpos 55 ypos 190 xsize 230 ysize 255 background None
        action Return("rule") sensitive ready
    button:
        xpos 585 ypos 300 xsize 230 ysize 270 background None
        action Return("road") sensitive ready
    frame:
        xpos 24 ypos 568 xsize 1232 ysize 144 background Solid("#142526ef") padding (18,14)
        vbox:
            spacing 12
            text "다람과 떨어지지 않고 들어갈 근거를 찾자." size 24 color "#edcf94"
            hbox:
                spacing 12
                textbutton ("까로의 서류 ✓" if winter_has(winter,"entry_permit") else "까로의 서류") style "winter_button" xsize 270 text_size 20 action Return("permit") sensitive ready
                textbutton ("경비의 명부 ✓" if winter_has(winter,"entry_copy") else "경비의 명부") style "winter_button" xsize 270 text_size 20 action Return("ledger") sensitive ready
                textbutton ("문 옆 규정 ✓" if winter_has(winter,"entry_rule") else "문 옆 규정") style "winter_button" xsize 270 text_size 20 action Return("rule") sensitive ready
                textbutton "기록을 대조해 말한다" style "winter_button" xsize 270 text_size 20 action Return("present") sensitive ready
