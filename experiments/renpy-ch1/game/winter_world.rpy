# Scene geometry, conversation ownership and free observations are separate
# from the calendar/evidence rules. All remembered state lives inside winter.
default winter_target_kind = None
default winter_target_id = None

init 46 python:
    WINTER_WORLD=json.load(renpy.file("winter-world.json"))
    WINTER_SPOTS={
        "inn":[("granny",590,180,190,330,"inn_activity"),("nabi",975,285,175,300,"world"),("resident_nubi",155,325,180,250,"inn_activity"),("bami",815,100,150,205,"world")],
        "gate":[("guard",270,240,220,340,"world"),("karo",875,295,210,285,"world"),("neoul",640,285,175,290,"world"),("resident_bori",55,340,155,235,"world"),("resident_lamplighter",1100,320,150,260,"world")],
        "square":[("doto",190,320,180,270,"world"),("resident_tori",925,295,170,280,"activity"),("bami",25,260,150,205,"world"),("resident_lamplighter",710,235,160,270,"world"),("resident_tok",855,420,170,165,"activity"),("resident_bori",675,330,150,250,"world")],
        "post":[("seryeon",560,225,230,360,"world"),("doto",1085,320,165,270,"world")],
        "workshop":[("buri",745,315,195,275,"world"),("resident_bori",195,330,155,250,"world"),("resident_tok",430,345,200,230,"activity"),("resident_lamplighter",1045,320,150,265,"world")],
        "room":[],"passage":[]}

    def winter_seen(s,key):
        n=winter_copy.deepcopy(s)
        n.setdefault("seen",[])
        if key not in n["seen"]:n["seen"].append(key)
        return n

    WINTER_SCHEDULES=json.load(renpy.file("winter-schedules.json"))

    def winter_where(s,person):
        if person not in WINTER_SCHEDULES:return None
        if person=="guard" and (s["day"]-1)%7==1 and winter_period(s)==2:return "square"
        # Case consequences outrank the weekly routine, including next week.
        if person=="resident_nubi":
            if s["day"]<3 or s["witness"] in ("detained","dead"):return None
            if s["witness"]=="safe":return "inn"
        if person=="bami" and s["day"]<4:return None
        if person=="neoul":
            if winter_has(s,"plaza_plan_shared") and not winter_has(s,"plaza_plan_echo_seen"):return "inn"
            if s["day"]<2:return None
            if s["witness"]=="detained" and s["day"] in (6,7):return "gate"
        return WINTER_SCHEDULES[person]["week"][(s["day"]-1)%7][min(2,winter_period(s))]

    def winter_people(s):
        place=s["location"]
        people=[who for who in WINTER_SCHEDULES if winter_where(s,who)==place]
        original={row[0]:row for row in WINTER_SPOTS[place]}
        # Keep approved counter placement. Visitors stand in the open floor,
        # not behind furniture; each actor has exactly one location.
        visitors=[who for who in people if who not in original]
        positions={"inn":[(365,285),(790,300),(50,290),(230,285)],
            "post":[(40,285),(280,285),(840,285)],
            "square":[(430,285),(665,285),(35,285)],
            "workshop":[(15,285),(960,285)],
            "gate":[(40,285),(450,285)]}
        result=[]
        for who in people:
            if who in original:result.append(original[who]);continue
            index=visitors.index(who)
            x,y=positions[place][index]
            result.append((who,x,y,170,290,"world"))
        return result

    def winter_known_at(s,place):
        names=list(dict.fromkeys(WINTER_NAMES[row["who"]] for row in s.get("encounters",[]) if row["place"]==place and row["day"]==s["day"]))
        return ("오늘 만남 · "+" · ".join(names[:2])+(" 외 %d명"%(len(names)-2) if len(names)>2 else "")) if names else "아직 둘러볼 곳"

    def winter_routine_lines(s,who):
        rows=[(who,WINTER_ROUGH_HINTS.get(who,"지금은 정해 둔 약속이 없어요."))]
        if who=="resident_nubi" and s["witness"]=="safe":
            return [(who,"당분간 여관 밖에는 안 나가려고요. 가족도 여기로 왔어요.")]
        if who=="neoul" and s["witness"]=="detained":
            rows.append((who,"다만 지금은 이송 문제 때문에 입구에 남습니다."))
        return rows

    def winter_greeting_key(s,who):
        variant=""
        if who=="doto" and winter_has(s,"doto_memory") and s["day"]>=2:
            variant=":supported" if winter_has(s,"doto_supported") else ":recanted"
        if who=="resident_nubi" and s["witness"]=="safe":variant=":protected"
        elif s["day"]>=8:
            if who=="granny":variant=":week2:"+str(s["first_result"])
            elif who=="resident_tori":variant=":week2"
            elif who=="buri" and winter_has(s,"fuel"):variant=":fuel"
            elif who=="nabi" and s["witness"]=="dead":variant=":absence"
        variant += ":"+s.get("resident_stance",{}).get(who,"neutral")
        if who=="resident_lamplighter":variant += ":ally" if winter_has(s,"mother_ally") else ""
        if who=="seryeon" and "mother_search" in s.get("known_information",{}).get(who,[]):variant += ":informed"
        return "hello:"+who+variant+winter_exploration_key(s,who)

    def winter_greeting(s,who):
        guarded=winter_private_greeting(s,who)
        if guarded:return guarded
        extra=winter_exploration_greeting(s,who)
        if extra:return extra
        if who=="doto" and winter_has(s,"doto_memory") and s["day"]>=2:
            if winter_has(s,"doto_supported"):
                return [(who,"창고 분들은 잘 잤대요. 그리고 그날 본 분, 사진 속 분 맞아요. 이번엔 제 이름도 같이 적어요.")]
            return [(who,"사진 속 분은 못 봤어요. 다른 사람과 헷갈렸나 봐요."),("daram","어제 기록판까지 보여 줬잖아요."),(who,"……지금은 사람들 있어요. 나중에 이야기해요.")]
        if who=="resident_nubi" and s["witness"]=="safe":
            return [(who,"오늘은 가족이랑 같이 왔어요. 이름을 숨기지 않아도 된다고 하셔서."),("dad","공개할 때까지 함께 있겠습니다.")]
        if s["day"]>=8:
            if who=="granny":
                return [(who,"장부를 내 손으로 지켜도 되겠네. 덕분이에요." if s["first_result"]=="protected" else "오늘도 장부를 가져갔어요. 손님 이름을 옮겨 적더군요."),("dad","새로 적힌 게 있으면 같이 보겠습니다.")]
            if who=="resident_tori":
                return [(who,"지난주 맡긴 수선부터 돌려주러 왔어요. 오늘은 새 도면을 들고 오진 않았어요.")]
            if who=="buri" and winter_has(s,"fuel"):
                return [(who,"연료는 여관 쪽에 모아 뒀어. 이제 밖으로 빼앗기지 않게 지켜야 해.")]
            if who=="nabi" and s["witness"]=="dead":
                return [(who,"누비 몫 그릇을 치우려다가 그냥 뒀어. 아직 아무 말도 못 들었으니까.")]
        return WINTER_WORLD["greetings"][who]

    def winter_morning(s):
        if s["day"]==5 and s["witness"]=="available" and not winter_has(s,"witness"):
            return [("resident_nubi","집 앞에 경비가 서 있어요. 왜 왔는지 물어도 기다리라고만 하고."),("dad","가족은 같이 있습니까?"),("resident_nubi","집에요. 저도 돌아가 봐야겠어요.")]
        if s["day"]==5 and s["witness"]!="available":
            return [("granny","누비 가족은 여기 있어요." if s["witness"]=="safe" else "누비가 안 보여요. 집 앞에는 경비가 있고."),("dad","오늘은 이송 기록을 확인하겠습니다.")]
        if s["day"]==8 and s["witness"]=="safe":
            return [("nabi","오늘은 그릇 더 꺼내자. 누비네도 같이 먹어."),("daram","작은 그릇은 내가 놓을게요.")]
        if s["day"]==9 and "routine:resident_tori" not in s.get("seen",[]):
            return [("daram","우리 여기 온 지 일주일 지났어."),("dad","응. 오늘은 놓친 곳도 다시 보자.")]
        return WINTER["events"].get(str(s["day"]),[])

    def winter_target_options(s,kind,key):
        if kind=="person" and winter_person_closed(s,key):return []
        owned=(WINTER_WORLD["places"][s["location"]]["objects"][key]["actions"] if kind=="object" else
            [k for k,v in WINTER_WORLD["owners"].items() if v==key and
             (WINTER["actions"][k]["cost"]==0 or WINTER["actions"][k]["place"]==s["location"])])
        return [k for k in owned if winter_visible(s,k) or k in s["done"]]

    def winter_goal(s):
        # Legacy observer field only; the HUD gives no next-destination orders.
        return "엄마가 이 마을에서 남긴 흔적을 찾고, 함께 돌아갈 길을 알아본다."

    def winter_empty_result():
        x,y=renpy.get_mouse_pos()
        renpy.end_interaction(("empty",(int(x),int(y))))

    def winter_inspection_mark(s,key,point):
        n=winter_copy.deepcopy(s)
        n.setdefault("checks",{})[s["location"]+":"+key]=list(point)
        return n

    def winter_display_topics(s,kind,key,tab):
        return [k for k in winter_target_options(s,kind,key)
            if bool(WINTER["actions"][k]["cost"])==(tab=="activity")]

    def winter_calendar_notes(s,day):
        notes=[]
        if day==1:notes.append(("겨울잠 여관", "엄마의 편지에 적힌 곳. 난로 옆에서 만나기로 했다."))
        if day==3 and s["day"]>=2:notes.append(("할머니의 심의", "저녁. 여관 보증을 지킬 근거를 가져가야 한다."))
        if day==6 and s["day"]>=6:notes.append(("이송 기록 공개 접수", "저녁. 원본을 여러 사람 앞에서 남길 기회."))
        if "repair" in s["records"] and s["records"]["repair"]["day"] < day <= s["records"]["repair"]["day"]+3:
            notes.append(("엄마의 측정", "밤. 비상 운용을 위해 하루의 출력 변화를 비교한다."))
        if (day-1)%7==1 and winter_has(s,"service_hint"):
            notes.append(("우편실 감압 점검", "저녁. 광장 회수 작업 중에는 손잡이 걸쇠의 압력이 빠진다."))
        if (day-1)%7==1 and winter_has(s,"cart_witnessed"):
            notes.append(("광장의 수레", "저녁에 돌 뒤에서 멈추는 것을 봤다. 다음 화요일에도 오는지 확인하자."))
        elif (day-1)%7==1 and winter_has(s,"cart_trace_seen") and winter_has(s,"service_hint"):
            notes.append(("광장의 바퀴 자국", "점검패에는 화요일 저녁이 회수 작업이라고 적혀 있었다. 이 자국과 관련 있을까?"))
        for row in s.get("encounters",[]):
            if row["day"]==day:
                notes.append((WINTER_NAMES[row["who"]]+" · 직접 만남",("오전","오후","저녁")[row["period"]]+" · "+WINTER["places"][row["place"]]["name"]))
        for who,hint in s.get("heard_routes",{}).items():
            if hint["day"]==day:notes.append((WINTER_NAMES[who]+"에게 들은 말",hint["text"]))
        return notes

    def winter_hearing_opening(s,hearing):
        if hearing=="granny":
            return [("nabi","저 이불 내가 꿰맸다고 몇 번을 말해."),("seryeon","그 말씀도 듣겠습니다. 돈이 비는 문제와 함께요."),("granny","손님 이름을 내놓으면 없던 일로 해 줄 겁니까?"),("seryeon","그런 약속은 못 합니다."),("dad","이름을 넘기기 전에, 혐의 자체부터 확인합시다.")]
        if hearing=="witness":
            return [("seryeon","사본은 모두 반납해 주세요. 주민 이름이 적혀 있습니다."),("dad","돌려주면 이송된 사람이 어디로 갔는지 누가 확인합니까?"),("neoul","여기서 대조한 원본 번호는 남기겠습니다. 실제 목적지를 보죠.")]
        return [("seryeon","돌이 꺼져 가고 있습니다. 명부에 오른 분들은 경비를 따라가 주세요."),("granny","내 손님을 내주지는 않겠어요."),("seryeon","여관 하나의 일이 아닙니다. 마을 전체가 얼어붙게 생겼어요."),("dad","앞서 데려간 사람들은 어디 있습니까? 그 사람들도 마을을 위해 간다고 했겠지요."),("neoul","아직 문 열지 마세요. 어디로 데려가는지부터 확인하겠습니다.")]

    def winter_observation_lines(s,place,key):
        extra=winter_exploration_observation(s,place,key)
        if extra:return extra
        repeats="observed:"+place+":"+key in s.get("seen",[])
        if place=="room" and key=="bed":
            if winter_has(s,"kitchen"):return [("daram","나비 아주머니 수선표랑 똑같아. 빨간 매듭도."),("dad","기록의 침구가 이 물건인지 확인됐어.")]
            return [("daram","여기만 천이 달라. 누가 기웠나 봐."),("dad","끝을 조금만 들어 봐. 뜯지는 말고."),("daram","안쪽은 색이 바랬네. 겉만 새로 덮었나?")]
        if place=="post" and key=="ledger":
            if winter_has(s,"receipt"):return [("dad","유예 도장이 있는 원본. 집계표에는 이 표시가 빠져 있다."),("daram","우리가 본 날짜도 적어 두자.")]
            return [("seryeon","그건 손님들 주소도 있어서요. 찾는 항목을 말씀해 주세요."),("dad","여관에 관한 기록부터 보겠습니다.")]
        if place=="square" and key=="offerings":
            if winter_has(s,"death"):return [("daram","저 끈 달린 열쇠…… 이송 명단에 적힌 물건이야."),("dad","사망 기록의 번호와도 같아."),("daram","돌아오라고 놓는 줄 알았는데."),("dad","여기에 놓은 사람은 어디까지 알고 있었을까.")]
            if winter_has(s,"witness"):return [("daram","누비 씨가 말한 수레에도 이런 작은 보따리가 있었대."),("dad","묶인 번호를 적자. 같은 사람 물건인지는 확인해야 해.")]
            return [("daram","장갑 한 짝이랑 열쇠도 있어. 누가 잃어버렸나?"),("doto","멀리 간 사람 몫이에요. 돌이 이름을 잊지 말라고요."),("daram","돌아오면 찾아가요?"),("doto","……그랬으면 좋겠네요.")]
        if place=="square" and key=="pipe":
            if winter_has(s,"research"):return [("dad","말을 유지하는 회로에서 열까지 끌어다 쓴 관이다."),("daram","엄마가 줄여야 한다던 게 이쪽이구나.")]
            return [("daram","여기만 눈이 없어. 손 대면 따뜻해."),("dad","오래 잡지는 마. 뜨거워질 수도 있어.")]
        if place=="gate" and key=="road" and winter_has(s,"order"):
            return [("dad","지시서의 목적지는 이 고개가 아니었다."),("daram","사람들한텐 밖으로 간다고 했는데.")]
        if place=="workshop" and key=="wheel":
            if winter_has(s,"order"):return [("buri","원본은 네가 가져갔지? 남은 쪽지는 내가 보관할게. 없애라 해도 안 버려.")]
            return [("daram","바퀴에 종이가 끼었어요."),("buri","수리표겠지. 잠깐, 기름 묻으니까 내가 뺄게.")]
        if place=="room" and key=="window":
            if winter_has(s,"surveillance"):return [("daram","또 저 사람이네. 우편실 앞에도 있었어."),("dad","창에서 조금 떨어져 있어. 우리 동선을 보고 있을 수 있어.")]
            return [("daram","문 앞에 발자국이 왔다 갔다 했어. 들어온 건 없고."),("dad","배달 왔다 돌아갔을 수도 있어. 지금은 표시만 해 두자.")]
        text=WINTER_WORLD["places"][place]["objects"][key]["text"]
        return [(None,("다시 살폈다. " if repeats else "")+text)]

label winter_talk:
    $ winter_topic_tab="talk"
    $ winter=winter_remember_person(winter,winter_target_id)
    if winter_target_id=="granny" and not winter_has(winter,"inn_registered"):
        call winter_lines([("granny","어서 와요. 문부터 닫고. 손이 꽁꽁 얼었겠네."),("dad","방을 부탁드립니다. 보내 주신 종이를 받고 왔습니다."),("granny","두 분 다 왔네요. 장갑은 난로 옆에 걸어요."),("daram","여기서 기다리던 분은요? 이 사진……"),("granny","……그분 딸이구나."),("dad","아내가 여기서 만나자고 편지를 보냈습니다."),("granny","방은 비워 두었어요. 일주일 전 나간 뒤로는 못 봤고요."),("daram","짐도 가져갔어요?"),("granny","아니. 못 가져간 것이 있어요."),("dad","그 방을 볼 수 있을까요?"),("granny","복도 끝이에요. 열세 번째 침대. 다른 사람 앞에서는 그분 이름부터 꺼내지 마요."),("dad","이유는 듣고 싶습니다."),("granny","찾는 사람이 또 와요. 숙박 명부를 보여 달라고."),("dad","어디서 온 사람들입니까?"),("granny","초소요. 내가 아는 건 거기까지예요."),("daram","아빠. 우리 짐도 거기 놓자."),("dad","그래. 방을 보고, 편지 보낸 곳부터 찾아보자.")],"registration")
        $ winter=winter_flag(winter,"inn_registered")
        call winter_lines([("daram","수첩 첫 장은 달력으로 쓸래. 엄마 만나면 날짜에 동그라미 치게."),("dad","약속도 적어 둬. 다시 찾을 수 있게.")],"calendar_intro")
    if winter_greeting_key(winter,winter_target_id) not in winter.get("seen",[]):
        call winter_lines(winter_greeting(winter,winter_target_id),"hello:"+winter_target_id)
        $ winter=winter_seen(winter,winter_greeting_key(winter,winter_target_id))
    if winter_target_id=="doto" and winter_has(winter,"doto_memory") and winter["day"]>=2 and not winter_has(winter,"doto_supported"):
        $ winter=winter_flag(winter,"doto_recanted")
    jump winter_questions

label winter_object:
    $ winter_topic_tab="talk"
    $ winter_object_spec=WINTER_WORLD["places"][winter["location"]]["objects"][winter_target_id]
    $ winter_rect=winter_object_spec["rect"]
    $ winter=winter_inspection_mark(winter,winter_target_id,(winter_rect[0]+winter_rect[2]//2,winter_rect[1]+winter_rect[3]//2))
    if winter["location"]=="square" and winter_target_id=="tracks":
        call winter_timed_cart
    elif winter["location"]=="post" and winter_target_id=="latch":
        call winter_secret_latch
        if winter["location"]=="passage":
            jump winter_roam
    else:
        call winter_lines(winter_present_observation(winter,winter["location"],winter_target_id),"object:"+winter_target_id)
    $ winter=winter_seen(winter,"observed:"+winter["location"]+":"+winter_target_id)
    if any(WINTER["actions"][k]["cost"] for k in winter_target_options(winter,"object",winter_target_id)) and not any(not WINTER["actions"][k]["cost"] for k in winter_target_options(winter,"object",winter_target_id)):
        $ winter_topic_tab="activity"
    if winter_target_id=="door" and winter["location"]=="passage" and winter_has(winter,"mother"):
        $ winter_target_kind="person"
        $ winter_target_id="mom"
        jump winter_talk
    if winter_target_options(winter,winter_target_kind,winter_target_id):
        jump winter_questions
    jump winter_field

label winter_questions:
    window hide
    if winter_target_kind=="person":
        $ winter_speaker(winter_target_id)
        if winter_target_id in CAST:
            $ renpy.show(winter_target_id+" interview_neutral",tag="winter_visitor",at_list=[winter_portrait_question])
    call screen winter_topics(winter_target_kind,winter_target_id)
    $ winter_topic_choice=_return
    if winter_topic_choice=="back":
        hide winter_visitor
        jump winter_field
    if winter_topic_choice=="present":
        $ winter_selected=[]
        call screen winter_evidence(True,winter_target_id)
        if isinstance(_return,dict) and _return.get("target")==winter_target_id:
            $ winter_selected=_return["selection"]
            $ winter_disclosure_named=_return["named"]
            call screen winter_disclosure_review(winter_target_id,winter_selected,winter_disclosure_named)
            if _return:
                call winter_present_to_resident
        jump winter_questions
    if winter_topic_choice=="hello":
        call winter_lines(winter_greeting(winter,winter_target_id),"hello:"+winter_target_id)
        $ winter=winter_seen(winter,winter_greeting_key(winter,winter_target_id))
        jump winter_questions
    if winter_topic_choice=="routine":
        call winter_lines(winter_routine_lines(winter,winter_target_id),"routine:"+winter_target_id)
        $ winter=winter_remember_hint(winter,winter_target_id)
        jump winter_questions
    if winter_topic_choice=="work":
        call winter_lines(WINTER_WORK_LINES[winter_target_id],"work:"+winter_target_id)
        $ winter=winter_seen(winter,"work:"+winter_target_id)
        jump winter_questions
    $ winter_action_id=winter_topic_choice
    $ winter=winter_finish_topic(winter,winter_target_id,winter_action_id)
    if winter_action_id in winter["done"]:
        if winter_action_id=="ration_share" and not winter_has(winter,"ration_public"):
            call winter_exploration_decision
        else:
            call winter_lines(winter_action_lines(winter,winter_action_id),"recall:"+winter_action_id)
        jump winter_questions
    call winter_action_run
    if winter_target_kind=="person" and winter_target_id!="mom" and winter_target_id not in [p[0] for p in winter_people(winter)]:
        hide winter_visitor
        jump winter_field
    jump winter_questions

# Version-one saves already saw automatic inn registration. Preserve their
# knowledge when they resume at a saved exploration screen.
label after_load:
    if room13_mode and room13:
        $ r13_upgrade()
        if room13.get("revision_restart_required"):
            jump r13_revision_resume
        $ r13_fullbody_refresh_after_load()
    if winter_mode and winter:
        $ winter=winter_upgrade(winter)
        $ clock_text=winter_clock(winter)
    return
