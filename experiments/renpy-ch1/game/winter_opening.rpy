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

    def winter_nabi_supports(s):
        return winter_has(s,"ration_public") and winter_has(s,"ration_route") and (s["day"]<10 or winter_has(s,"fuel"))

    def winter_hearing_limit(s):
        return 3 + int(winter_has(s,"doto_supported")) + int(winter_has(s,"permission") and s["witness"] in ("available","safe")) + int(winter_has(s,"karo_hearing_ready")) + int(winter_nabi_supports(s))

    def winter_support_lines(s):
        result=[]
        if winter_nabi_supports(s):
            result.append(("nabi","배급 때도 표만 보고 우리 탓이라 했잖아. 이 사람은 인수증까지 맞춰 봤어. 이번에도 원본부터 펼쳐 보자고."))
        elif winter_has(s,"ration_public") and s["day"]>=10:
            result.extend([("nabi","인수증은 내가 쓴 게 맞아. 그 말은 안 바꿔."),("seryeon","그러면 시설을 멈추고도 각자 난방을 버틸 수 있겠군요?"),("nabi","……우리 집엔 애들이 있어. 그 일까지 찬성한 건 아니야.")])
        if winter_has(s,"karo_hearing_ready"):
            result.append(("karo","운행 일지는 내가 확인했어요. 저 수레 안은 못 봤지만, 내 기록을 모르는 사람의 추측이라고 넘기진 마요."))
        if winter_has(s,"doto_supported"):
            result.append(("doto","제가 적은 날짜와 목격담이 맞습니다. 말을 바꾸라고 찾아온 사람도 있었어요. 이분 말씀 끝까지 들어 주세요."))
        if winter_has(s,"permission") and s["witness"] in ("available","safe"):
            result.append(("resident_nubi","이젠 제 이름으로 말하겠습니다. 그날 수레를 민 건 저예요."))
        return result

label winter_arrival:
    $ winter_entry=True
    $ winter=dict(winter,location="gate")
    call winter_scene("winter_carriage","고개 아래 · 마을로 가는 마차","calm")
    call winter_lines([("daram","아빠. 아까부터 같은 쪽만 먹지?"),("dad","어느 쪽?"),("daram","큰 거 있는 쪽. 봉지 돌려 봐."),("dad","들켰네."),("daram","이건 남겨. 엄마 것도 있어야지."),("dad","눅눅해지겠다."),("daram","그래도 가져왔다는 게 중요하지."),(None,"다람이 봉지 입구를 접어 가방 안쪽에 넣었다."),("daram","편지 줘 봐. 여관 이름 또 까먹었어."),("dad","겨울잠 여관."),("daram","그건 기억나. 방 이름이…… 아니, 방은 안 썼네."),("dad","난로 옆에서 기다리라고 했지."),("daram","엄마가 먼저 와 있으면 내가 먼저 볼 거야. 아빠는 짐 들어."),("dad","그럼 네 가방도 내 짐인가?"),("daram","이건 내가 들 거야."),(None,"편지의 접힌 자리를 폈다. 열흘 전 날짜. 그 뒤로 답장은 오지 않았다.")],"carriage")
    $ winter=winter_collect(winter,"invitation")
    call winter_lines([("karo","잠깐, 안에서 기다려요. 바퀴 쪽을 좀 볼게요."),("daram","아까 덜컹한 거요?"),("karo","얼음 턱에 걸렸어. 축에 금이 갔네. 더 굴리면 바퀴가 빠져요."),("dad","여기서 내려야겠군요."),("karo","문 바로 앞이에요. 짐은 내가 옮길게요."),("daram","돌아갈 때도 이 마차 타요?"),("karo","고치고 눈이 녹아야지. 고개엔 또 눈보라가 친대. 지금 다시 올라갈 수는 없어.")],"carriage_stop")
    call winter_scene("winter","마을 입구 · 검문 초소","search")
    call winter_lines([("dad","다람아, 손."),("daram","목도리 꼈어. 잠깐만."),("dad","풀었어. 천천히 내려와."),(None,"눈에 발이 푹 잠겼다. 문 안쪽에서 경비가 책 한 권을 펼쳤다."),("guard","여관 손님 한 분 맞습니까?"),("dad","딸도 함께입니다."),("guard","여긴 한 명만 적혔네요. 아이는 저쪽에서 기다리게 하세요."),("daram","아빠도 같이 가?"),("guard","아버지는 이름부터 확인해야지. 저쪽이 더 따뜻해."),("dad","같이 기다리겠습니다."),("guard","처음 오는 분들은 나눠서 확인합니다. 오래 안 걸려요."),("karo","두 사람 온다고 종이를 받았는데. 어디 넣었더라."),("daram","아빠. 저 아저씨 손 안 잡을래."),("dad","응. 내 옆에 있어.")],"gate")
    jump winter_entry_loop

label winter_entry_loop:
    window hide
    hide winter_visitor
    call screen winter_entry_hub
    $ winter_entry_choice=_return
    if isinstance(winter_entry_choice,tuple):
        $ winter=winter_inspection_mark(winter,"entry_empty:%d:%d"%(winter_entry_choice[0]//80,winter_entry_choice[1]//80),winter_entry_choice)
        call winter_lines([(None,"눈에 덮인 바닥과 문턱을 살폈다. 떨어진 물건은 보이지 않는다.")],"entry_empty")
    elif winter_entry_choice=="permit":
        menu:
            "까로는 옷 안주머니를 뒤지고 있다."
            "여관에서 받은 종이를 함께 찾는다":
                call winter_lines([("dad","두 사람 온다고 적힌 종이, 아직 있습니까?"),("karo","네. 젖을까 봐 안주머니에 넣었어요. 여기."),("daram","내 이름도 있네. 아빠 옆에."),(None,"겨울잠 여관. 손님 두 사람. 번호 73-2. 할머니의 이름 아래 도장이 찍혔다."),("karo","경비가 보는 것과 같은 번호인지 봐요. 내가 내밀면 잘 안 읽더라고.")],"entry_permit")
                call winter_discovery("entry_permit")
            "마차를 고칠 수 있는지 묻는다":
                call winter_lines([("karo","수리점에 맡겨야죠. 그래도 눈보라가 그쳐야 길을 봐요."),("dad","그동안 여관에 있겠습니다."),("karo","나도 멀리 못 가요. 먼저 둘이 같이 들어가요.")],"entry_carriage")
            "잠깐 더 둘러본다":
                pass
    elif winter_entry_choice=="ledger":
        menu:
            "경비는 펼친 책을 손으로 누르고 있다."
            "우리 이름이 적힌 줄을 보여 달라고 한다":
                call winter_lines([("dad","다른 사람 이름은 안 보겠습니다. 우리 줄만 보여 주세요."),("guard","73-2. 성인 한 명. 아이 칸은 비었어요."),("daram","누가 내 이름 지웠어요?"),("guard","난 이대로 받았어. 네 이름은 방금 처음 들었고."),("dad","번호와 적힌 인원만 옮겨 적겠습니다."),("guard","그 줄만요.")],"entry_copy")
                call winter_discovery("entry_copy")
            "아이도 여기서 기다리면 안 되나요?":
                call winter_lines([("guard","처음 오는 사람들은 저쪽부터 확인해요."),("dad","함께 온 가족도요?"),("guard","문 옆에 붙인 안내 보셨습니까? 난 늘 하던 대로 하는 겁니다.")],"entry_advice")
            "다른 곳을 살펴본다":
                pass
    elif winter_entry_choice=="rule":
        call winter_lines([("daram","아래가 접혔어. 여기 글씨도 있네."),("dad","종이 젖었으니 살살 펴 봐."),(None,"「이름이 서로 다르면 처음 받은 종이와 맞춰 볼 것. 함께 온 가족은 확인이 끝날 때까지 함께 기다릴 것.」"),("daram","같이 기다리라고 써 있는데."),("dad","이 문장도 남겨 두자.")],"entry_rule")
        call winter_discovery("entry_rule")
    elif winter_entry_choice=="road":
        call winter_lines([(None,"바퀴 축에 갈라진 선이 보였다. 까로가 천으로 표시해 두었다. 문 너머에서는 눈이 다시 옆으로 몰아쳤다."),("daram","저거 고쳐도 산은 못 넘는 거네."),("dad","눈보라가 그쳐야 길도 볼 수 있어. 우선 둘이 같이 들어가자.")],"entry_road")
    elif winter_entry_choice=="look":
        call winter_lines([(None,"문 옆 종이의 아래쪽이 접혔다. 경비는 책을 펼친 채 기다리고, 까로는 주머니에서 무언가를 찾는다.")],"entry_look")
    elif winter_entry_choice=="daram":
        call winter_lines([("daram",winter_entry_hint(winter))],"entry_hint")
    elif winter_entry_choice=="present":
        $ winter_selected=[]
        call screen winter_evidence(True)
        if _return:
            if winter_entry_proof(winter,winter_selected):
                jump winter_entry_reason
            elif "invitation" in winter_selected:
                call winter_lines([("guard","가족이 보낸 편지인 건 알겠습니다. 하지만 여관에서 두 분을 기다린다는 확인도 있어야 해요."),("karo","여관에서 준 종이도 봐 주세요. 도장 있는 쪽이요.")],"entry_letter_reply")
            else:
                call winter_lines([("guard","같은 손님인지, 몇 명인지 확인해야 해요. 지금 보여 주신 것만으론 이름을 고치기 어렵습니다.")],"entry_other_reply")
    jump winter_entry_loop

label winter_entry_reason:
    call winter_lines([("guard","번호는 같네요. 여긴 두 사람, 내 책엔 한 사람."),("karo","출발할 때도 둘이었어요. 중간에 태운 아이가 아니고."),("guard","그래서 어느 쪽을 고쳐 달라는 겁니까?")],"entry_counter")
    menu:
        "어떤 점을 바로잡아야 할까?"
        "아이를 새 손님으로 다시 적어 달라고 한다":
            call winter_lines([("guard","그럼 새로 온 손님부터 확인해야 합니다."),("daram","근데 내 이름 이미 있잖아."),("dad","잠깐만요. 처음 적힌 이름을 다시 보겠습니다.")],"entry_new_wrong")
            jump winter_entry_loop
        "함께 온 두 사람이다. 이름을 돌려놓는다":
            pass
        "경비가 일부러 이름을 지웠다고 몰아붙인다":
            call winter_lines([("guard","내가 쓴 책이 아닙니다. 누가 지웠다고요?"),("dad","그건 아직 모릅니다. 확인할 수 있는 것부터 보죠.")],"entry_blame_wrong")
            jump winter_entry_loop
    call winter_lines([("dad","새 손님이 아닙니다. 처음 종이에 있던 아이 이름이 이 책에만 빠졌어요."),("guard","……두 사람으로 고치겠습니다."),("daram","그럼 이제 아빠랑 가도 돼요?"),("guard","그래. 여관 주인한테 이 종이 보여 줘."),("dad","함께 기다리라는 안내도 확인해 주세요. 다른 가족이 와도요."),("guard","알겠습니다. 해 지기 전에는 여관에 들어가세요."),("karo","짐은 내가 옮겨요. 마차도 맡겨야 하니."),("daram","이제 손 놔도 돼?"),("dad","문 나갈 때까진 잡고 있자.")],"entry_won")
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
    button:
        xpos 0 ypos 140 xsize 1280 ysize 450 padding (0,0) background None
        action Function(winter_entry_empty_result) sensitive ready
    add Transform("guard world",size=(240,360),fit="contain") xpos 330 ypos 215
    add Transform("karo world",size=(235,330),fit="contain") xpos 865 ypos 255
    add Transform("assets/contract.png",size=(68,86),fit="contain") xpos 146 ypos 240
    button:
        xpos 330 ypos 215 xsize 240 ysize 360 padding (0,0) background None
        action Return("ledger") sensitive ready
    button:
        xpos 865 ypos 255 xsize 235 ysize 330 padding (0,0) background None
        action Return("permit") sensitive ready
    button:
        xpos 115 ypos 205 xsize 140 ysize 175 padding (0,0) background None
        action Return("rule") sensitive ready
    button:
        xpos 585 ypos 300 xsize 230 ysize 270 padding (0,0) background None
        action Return("road") sensitive ready
    for key,x,y in (("entry_permit",965,440),("entry_copy",445,405),("entry_rule",180,282)):
        if winter_has(winter,key):
            add TopicTick() xpos x ypos y
    for key,point in winter.get("checks",{}).items():
        if key.startswith("gate:entry_empty:"):
            add TopicTick() xpos point[0]-13 ypos point[1]-13
    frame:
        xpos 24 ypos 624 xsize 1232 ysize 88 background Solid("#142526ef") padding (18,14)
        hbox:
            spacing 16
            textbutton "주변 살펴보기" style "winter_button" xsize 330 text_size 22 action Return("look") sensitive ready
            textbutton "다람과 이야기" style "winter_button" xsize 330 text_size 22 action Return("daram") sensitive ready
            textbutton "증거 수첩 · 보여 주기" style "winter_button" xsize 480 text_size 22 action Return("present") sensitive ready
