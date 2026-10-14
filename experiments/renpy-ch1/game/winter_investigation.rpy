# Discovery, testimony and leads share the existing save state. NPC schedules are
# simulation data; the player notebook only contains encounters and things heard.
init 49 python:
    def winter_entry_empty_result():
        x,y=renpy.get_mouse_pos()
        renpy.end_interaction((int(x),int(y)))

    def winter_open_questions(s):
        rows=[]
        if winter_has(s,"mother_linen") and not winter_has(s,"mother"):
            rows.append(("엄마가 남긴 짐","옷과 단추는 두고 갔다. 돌아올 생각이었을까, 가져갈 수 없었던 걸까?"))
        if winter_has(s,"mother_note") and not winter_has(s,"mother_repair"):
            rows.append(("메모의 이름","등은 꺼졌는데 아래는 따뜻했다. 그리고 부리에게 물어볼 일이 있었다."))
        if winter_has(s,"sightings") and not winter_has(s,"passage_known"):
            rows.append(("같은 종소리, 다른 장소","엄마를 우편실 뒤와 광장에서 봤다는 두 사람. 둘 다 맞을 수도 있을까?"))
        if winter_has(s,"ration_notice") and not winter_has(s,"ration_route"):
            rows.append(("배급표의 여섯 자루","표에 적힌 숫자는 실제로 받은 양과 같을까?"))
        if winter_has(s,"ration_route"):
            rows.append(("중앙 보관소","여관으로 오던 곡물이 먼저 그쪽으로 갔다. 안에는 누가 있고 무엇에 쓰일까?"))
        if winter_has(s,"carriage_checked"):
            rows.append(("돌아갈 길","마차도 고쳐야 하고 눈보라도 잦아들어야 한다. 엄마가 떠났는지는 아직 별도로 확인해야 한다."))
        return rows or [("엄마가 보낸 편지","여관 난로 옆에서 기다리라고 했다. 엄마에게 무슨 일이 있었을까?")]
    WINTER_WORK_LINES={
        "granny":[("granny","빈방을 세는 게 아니에요. 오늘 밤 누가 안 돌아왔는지 보는 거지."),("daram","안 오면 찾으러 가요?"),("granny","밤엔 못 나가. 그래서 이름을 지우지 않는 거야.")],
        "nabi":[("nabi","그릇 수를 세고 있어. 손님 말고 밥 먹으러 오는 사람도 있거든."),("daram","우리도 놓을까요?"),("nabi","잠깐만. 거긴 뜨거운 솥 내려놓을 자리야. 저쪽부터 부탁해.")],
        "guard":[("guard","문이 얼어붙기 전에 눈을 치웁니다. 조금만 물러서세요."),("dad","여길 나간 사람이 있습니까?"),("guard","차로 나간 사람은 없어요. 다른 일은 담당자에게 물으세요.")],
        "karo":[("karo","바퀴 축에 감긴 얼음을 떼는 중이에요. 이대로 움직이면 더 부러져요."),("daram","말도 쉬어야겠네요."),("karo","그렇지. 아까 놀랐으니까 조용히 다녀오자.")],
        "seryeon":[("seryeon","못 보낸 짐을 다시 세고 있습니다. 찾는 게 있으면 이름부터 말씀해 주세요."),("daram","눈 녹으면 한꺼번에 보내요?"),("seryeon","그러고 싶죠. 그때까지 여기 있어야 하는 짐도 있고요.")],
        "doto":[("doto","돌 앞에 놓인 물건을 옮기고 있어요. 눈에 묻히면 주인이 못 찾으니까."),("daram","같이 들어도 돼요?"),("doto","번호 달린 건 손대지 말고요. 저 빈 바구니만 부탁해요.")],
        "buri":[("buri","고장 난 걸 고치는 것보다 쓸 만한 부품 찾는 게 오래 걸려."),("daram","여기 있는 건 다 못 쓰는 거예요?"),("buri","아직 몰라. 그래서 버리지 못하는 거야.")],
        "bami":[("bami","자려고. 낮에 자야 해."),("daram","밤에는 안 자요?"),("bami","전엔 그랬지. 요즘은 밤에도 안 나가. 시끄러워서.")],
        "neoul":[("neoul","문이 열리는지 집마다 보는 중입니다."),("dad","왜요?"),("neoul","눈에 막혀 갇히면 불러도 안 들립니다. 누구를 잡으러 다니는 건 아니에요.")],
        "resident_nubi":[("resident_nubi","젖은 이불을 걷어요. 다들 불을 줄이니 마르질 않아서."),("daram","여관에 널면 안 돼요?"),("resident_nubi","손님들 지나갈 자리는 남겨야지. 할머니께 한번 여쭤볼게요.")],
        "resident_tori":[("resident_tori","수선 맡긴 순서대로 하고 있어요. 급하다고 먼저 달라는 분이 많아서요."),("dad","물어볼 것만 잠깐 있습니다."),("resident_tori","손은 움직여도 괜찮죠? 듣고 있어요.")],
        "resident_bori":[("resident_bori","잘 마른 것과 젖은 걸 나눠요. 겉만 보고 때면 연기 때문에 못 있어요."),("daram","이건 무거우니까 젖은 거?"),("resident_bori","잘 봤네. 하지만 무거운 나무도 있으니 끝을 한번 만져 봐.")],
        "resident_tok":[("resident_tok","작은 시계는 잠깐 미뤘어요. 먼저 움직여야 하는 게 생겨서."),("daram","손잡이 돌리는 거요?"),("resident_tok","응. 톱니 끝은 만지지 말고 구경해.")],
        "resident_lamplighter":[("resident_lamplighter","깨진 등인지 전기가 안 오는 건지 가리는 중이야."),("daram","어떻게 알아요?"),("resident_lamplighter","불 들어오는 쪽에 한번 달아 보지. 여기선 멀쩡한 것도 고장 난 것처럼 보이거든.")],
    }
    WINTER_ROUGH_HINTS={
        "granny":"돌아와서 접수대가 비었으면 종을 울려요. 멀리는 못 가니까.",
        "nabi":"밥때쯤 여관에 와. 솥 앞에 없으면 그릇 걷으러 간 거야.",
        "guard":"문 근처에 있습니다. 일을 보러 안쪽에 갈 때도 있으니 다른 경비에게 물어보세요.",
        "karo":"대개 마차 옆에 있을 거예요. 짐 찾으러 우편실에 가기도 하고. 먼저 고쳐야 하니까.",
        "seryeon":"창구가 열렸을 때 오세요. 배급 날은 자리를 비울 수도 있습니다.",
        "doto":"짐이 오는 쪽에 있어요. 광장에서 안 보이면 우편실로 납품 갔을 거예요.",
        "buri":"고칠 게 쌓여서 여기 오래 있을 거야. 가끔 밥 먹으러 나갈 테니 없으면 다시 와.",
        "bami":"따뜻한 처마 밑. 아래만 보지 말고 위도 봐.",
        "neoul":"순찰을 돌아야 해서 한곳에 있진 않습니다. 입구와 광장 쪽을 먼저 찾아보세요.",
        "resident_nubi":"세탁물을 받아 주는 데부터 가요. 여관이나 수리점 쪽에서 마주칠 거예요.",
        "resident_tori":"광장에서 수선거리를 받을 때 와요. 요즘엔 오래 못 앉아 있어. 납품 때문에 수리점에 들르기도 하고요.",
        "resident_bori":"해 있을 때는 장작을 만져야지요. 입구에 없으면 수리점에서 말리고 있을 겁니다.",
        "resident_tok":"요즘은 수리점에 자주 가요. 장치를 끝내야 해서. 맡긴 시계 돌려줄 때는 광장에 나가고요.",
        "resident_lamplighter":"아직 밝을 때 길을 돌아. 해 지면 수리할 등을 들고 들어가야지.",
    }

    def winter_remember_person(s,who):
        n=winter_copy.deepcopy(s)
        entry=dict(who=who,place=s["location"],day=s["day"],period=min(2,winter_period(s)))
        if entry not in n.setdefault("encounters",[]):n["encounters"].append(entry)
        return n

    def winter_can_ask_hint(s,who):
        if who not in WINTER_ROUGH_HINTS:return False
        return "work:"+who in s.get("seen",[]) and any(WINTER_WORLD["owners"].get(k)==who for k in s["done"])

    def winter_remember_hint(s,who):
        n=winter_seen(s,"routine:"+who)
        n.setdefault("heard_routes",{})[who]=dict(day=s["day"],text=WINTER_ROUGH_HINTS[who])
        return n

    def winter_topic_entries(s,kind,target,tab):
        rows=[]
        if kind=="person" and tab=="talk":
            rows.append(("hello","안부를 묻는다",winter_greeting_key(s,target) in s.get("seen",[])))
            if target in WINTER_WORK_LINES and not winter_person_closed(s,target):rows.append(("work","지금 하시는 일", "work:"+target in s.get("seen",[])))
        rows += [(key,("새 이야기 · " if key in s.get("new_topics",{}).get(target,[]) else "")+WINTER["actions"][key]["name"],key in s["done"]) for key in winter_display_topics(s,kind,target,tab)]
        if kind=="person" and tab=="talk" and not winter_person_closed(s,target) and winter_can_ask_hint(s,target):
            rows.append(("routine","다음에는 어디서 뵐까요?","routine:"+target in s.get("seen",[])))
        return rows

    def winter_evidence_kind(key):
        if key in ("karo_account","witness","karo_memory","doto_memory","sightings","symptoms","kitchen","lamp_log"):return "들은 말"
        if key in ("bed","mother_linen","tracks","transfer_seal"):return "발견한 흔적"
        if key in ("ration_route","research","repair","escape"):return "맞춰 본 단서"
        return "찾아낸 기록"

    def winter_evidence_picture(key):
        faces={"karo_account":"karo","witness":"resident_nubi","karo_memory":"karo","doto_memory":"doto","symptoms":"bami","kitchen":"nabi","lamp_log":"resident_lamplighter"}
        if key in faces:return faces[key]+" avatar_neutral"
        if key=="bed":return Crop((535,280,490,190),winter_background("room"))
        if key=="mother_linen":return Crop((90,305,245,255),winter_background("room"))
        if key in ("route","escape"):return "assets/carriage.png"
        if key in ("map","sightings"):return "assets/map.png"
        if key in ("meter","repair","mill_note"):return Crop((390,70,260,260),winter_background("winter_workshop"))
        if key in ("transfer_seal","ritual"):return "assets/seal.png"
        if key=="tracks":return Crop((780,400,450,200),winter_background("winter_square"))
        if key in ("ration_notice","kitchen_receipt","ration_order","ration_route"):return "assets/record.png"
        if key in ("invitation","entry_permit","entry_copy","entry_rule","mother_note"):return "assets/contract.png"
        return "assets/notebook.png"

    def winter_entry_hint(s):
        if not winter_has(s,"entry_rule"):return "문 옆에 접힌 종이가 있어. 기다리는 사람도 읽으라고 붙인 걸까?"
        if not winter_has(s,"entry_permit"):return "까로 아저씨가 우리 둘 이름을 받았댔지? 어떤 종이였는지 물어보자."
        if not winter_has(s,"entry_copy"):return "경비 아저씨가 보는 이름도 같이 확인해야겠어. 번호가 같은지."
        return "우리가 갖고 온 종이랑 저쪽 책을 같이 보여 주면 어때? 내 이름이 빠진 데를."

label winter_discovery(key):
    if not winter_has(winter,key):
        $ winter=winter_collect(winter,key,"field")
        call winter_found_card(key)
    return

label winter_found_card(key):
    window hide
    $ renpy.music.play("assets/source-found.wav",channel="scene_fx",loop=False,relative_volume=.25)
    call screen winter_found(key)
    return

screen winter_found(key):
    modal True
    zorder 72
    default ready=False
    timer .3 action SetScreenVariable("ready",True)
    add Solid("#07171bbc")
    frame:
        xpos 210 ypos 140 xsize 860 ysize 440 padding (24,24) background Solid("#233b3ef8")
        fixed:
            text "다람의 증거 수첩" size 24 color "#d4e1d7"
            add Transform(winter_evidence_picture(key),size=(250,225),fit="contain") xpos 8 ypos 85
            text winter_evidence_kind(key) xpos 300 ypos 53 size 18 color "#b0cdc4"
            text WINTER["evidence"][key]["name"] xpos 300 ypos 85 size 28 xsize 470 color "#ffe0a1"
            text WINTER["evidence"][key]["text"] xpos 300 ypos 136 size 21 xsize 470
            textbutton "수첩에 끼워 둔다" xpos 290 ypos 330 xsize 360 ysize 52 style "winter_button" action Return() sensitive ready
