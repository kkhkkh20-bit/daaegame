# Scene geometry, conversation ownership and free observations are separate
# from the calendar/evidence rules. All remembered state lives inside winter.
default winter_target_kind = None
default winter_target_id = None

init 46 python:
    WINTER_WORLD=json.load(renpy.file("winter-world.json"))
    WINTER_SPOTS={
        "inn":[("granny",590,180,190,330,"inn_activity"),("nabi",975,285,175,300,"world"),("resident_nubi",155,325,180,250,"inn_activity"),("bami",815,100,150,205,"world")],
        "gate":[("guard",270,240,220,340,"world"),("karo",875,295,210,285,"world"),("neoul",640,285,175,290,"world")],
        "square":[("doto",190,320,180,270,"world"),("resident_tori",925,295,170,280,"activity"),("bami",25,260,150,205,"world")],
        "post":[("seryeon",560,225,230,360,"world"),("doto",1085,320,165,270,"world")],
        "workshop":[("buri",745,315,195,275,"world")],
        "room":[],"passage":[]}

    def winter_seen(s,key):
        n=winter_copy.deepcopy(s)
        n.setdefault("seen",[])
        if key not in n["seen"]:n["seen"].append(key)
        return n

    WINTER_SCHEDULES=json.load(renpy.file("winter-schedules.json"))

    def winter_where(s,person):
        if person not in WINTER_SCHEDULES:return None
        # Case consequences outrank the weekly routine, including next week.
        if person=="resident_nubi":
            if s["day"]<3 or s["witness"] in ("detained","dead"):return None
            if s["witness"]=="safe":return "inn"
        if person=="bami" and s["day"]<4:return None
        if person=="neoul":
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
        positions={"inn":[(365,285),(50,290),(790,285),(230,285)],
            "post":[(40,285),(280,285),(840,285)],
            "square":[(430,285),(665,285),(35,285)],
            "workshop":[(180,285),(410,285),(980,285)],
            "gate":[(40,285),(450,285)]}
        result=[]
        for who in people:
            if who in original:result.append(original[who]);continue
            index=visitors.index(who)
            x,y=positions[place][index]
            result.append((who,x,y,170,290,"world"))
        return result

    def winter_known_at(s,place):
        names=[WINTER_NAMES[who] for who in WINTER_SCHEDULES
            if "routine:"+who in s.get("seen",[]) and winter_where(s,who)==place]
        return " · ".join(names) if names else "알아둔 일정 없음"

    def winter_routine_lines(s,who):
        rows=[(who,WINTER_SCHEDULES[who]["description"])]
        if who=="resident_nubi" and s["witness"]=="safe":
            return [(who,"당분간 여관 밖에는 안 나가려고요. 가족도 여기로 왔어요.")]
        if who=="neoul" and s["witness"]=="detained":
            rows.append((who,"다만 지금은 이송 문제 때문에 입구에 남습니다."))
        return rows

    def winter_greeting_key(s,who):
        variant=""
        if who=="resident_nubi" and s["witness"]=="safe":variant=":protected"
        elif s["day"]>=8:
            if who=="granny":variant=":week2:"+str(s["first_result"])
            elif who=="resident_tori":variant=":week2"
            elif who=="buri" and winter_has(s,"fuel"):variant=":fuel"
            elif who=="nabi" and s["witness"]=="dead":variant=":absence"
        return "hello:"+who+variant

    def winter_greeting(s,who):
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
        if s["day"]==5 and s["witness"]!="available":
            return [("granny","누비 가족은 여기 있어요." if s["witness"]=="safe" else "누비가 안 보여요. 집 앞에는 경비가 있고."),("dad","오늘은 이송 기록을 확인하겠습니다.")]
        if s["day"]==8 and s["witness"]=="safe":
            return [("nabi","오늘은 그릇 더 꺼내자. 누비네도 같이 먹어."),("daram","작은 그릇은 내가 놓을게요.")]
        if s["day"]==9 and "routine:resident_tori" not in s.get("seen",[]):
            return [("daram","우리 여기 온 지 일주일 지났어."),("dad","응. 오늘은 놓친 곳도 다시 보자.")]
        return WINTER["events"].get(str(s["day"]),[])

    def winter_target_options(s,kind,key):
        owned=(WINTER_WORLD["places"][s["location"]]["objects"][key]["actions"] if kind=="object" else
            [k for k,v in WINTER_WORLD["owners"].items() if v==key and
             (WINTER["actions"][k]["cost"]==0 or WINTER["actions"][k]["place"]==s["location"])])
        return [k for k in owned if winter_visible(s,k) or k in s["done"]]

    def winter_goal(s):
        if not winter_has(s,"inn_registered"):return "접수대의 할머니에게 말을 걸어 방을 구하자."
        if winter_period(s)==3:return "오늘 큰 일정은 마쳤다. 더 묻고 살펴보거나 여관에서 밤을 보내자."
        if s["witness"]=="detained" and s["day"]<=7:return "누비의 이송을 막을 근거를 찾아 마을 입구의 너울에게 가자."
        if s["day"]<=3 and s["day"]>=2:return "할머니의 혐의를 확인하자. 방의 침구와 우편실의 난방비 기록이 실마리다."
        if not winter_has(s,"registry"):return "할머니에게 숙박 명부를 부탁하자. 엄마가 머문 흔적이 남아 있을까."
        if not winter_has(s,"sightings"):return "세련에게 엄마를 마지막으로 본 곳을 물어보자. 자리를 비웠다면 일정을 확인하자."
        if not winter_has(s,"route"):return "까로를 만나 눈에 막힌 길과 운송 기록을 물어보자."
        if winter_has(s,"map") and not winter_has(s,"mother"):return "옛 점검 통로를 살펴 두 목격 장소 사이의 길을 확인하자."
        if winter_has(s,"mother") and not winter_has(s,"mother_secure"):return "뒤따르는 경비가 있다. 까로에게 교대를 확인하고 엄마의 거처를 옮기자."
        return "주민의 말과 현장 기록을 비교하자. 수리점·광장에도 다른 흔적이 남아 있다."

    def winter_empty_result():
        x,y=renpy.get_mouse_pos()
        renpy.end_interaction(("empty",(int(x),int(y))))

    def winter_inspection_mark(s,key,point):
        n=winter_copy.deepcopy(s)
        n.setdefault("checks",{})[s["location"]+":"+key]=list(point)
        return n

label winter_talk:
    if winter_target_id=="granny" and not winter_has(winter,"inn_registered"):
        call winter_lines([("granny","어서 와요. 마차에서 온 두 분이죠?"),("dad","네. 방 하나 부탁드립니다."),("daram","장갑도 말려도 돼요?"),("granny","난로 옆에 걸어 둬요. 손부터 녹이고."),("dad","그리고… 이 사진 속 사람을 찾습니다."),("granny","……이분이 쓰던 방이 비어 있어요."),("daram","엄마가 여기서 잤어요?"),("granny","그랬어요. 지금은 없지만."),("dad","그 방으로 주십시오."),("granny","복도 끝이에요. 열세 번째 침대. 짐부터 두고 와요."),("seryeon","늦게 확인해서 죄송합니다. 두 분 체류는 제가 맡겠습니다."),("dad","아이를 또 따로 부르는 일은 없겠죠?"),("granny","숙박 보증은 내가 해요. 물을 일이 있으면 여기로 와요."),("seryeon","알겠습니다. 두 주 뒤 체류 심의까지는요."),("dad","할머니. 엄마가 남긴 연락처는 없었습니까?"),("granny","편지는 우편실의 세련 씨가 맡아요. 명부는 내가 찾아 놓을게요.")],"registration")
        $ winter=winter_flag(winter,"inn_registered")
    if winter_greeting_key(winter,winter_target_id) not in winter.get("seen",[]):
        call winter_lines(winter_greeting(winter,winter_target_id),"hello:"+winter_target_id)
        $ winter=winter_seen(winter,winter_greeting_key(winter,winter_target_id))
    jump winter_questions

label winter_object:
    $ winter_object_spec=WINTER_WORLD["places"][winter["location"]]["objects"][winter_target_id]
    $ winter_rect=winter_object_spec["rect"]
    $ winter=winter_inspection_mark(winter,winter_target_id,(winter_rect[0]+winter_rect[2]//2,winter_rect[1]+winter_rect[3]//2))
    call winter_lines([(None,winter_object_spec["text"])],"object:"+winter_target_id)
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
            $ renpy.show(winter_target_id+" interview_neutral",tag="winter_visitor",at_list=[portrait_question])
    call screen winter_topics(winter_target_kind,winter_target_id)
    $ winter_topic_choice=_return
    if winter_topic_choice=="back":
        hide winter_visitor
        jump winter_field
    if winter_topic_choice=="hello":
        call winter_lines(winter_greeting(winter,winter_target_id),"hello:"+winter_target_id)
        $ winter=winter_seen(winter,winter_greeting_key(winter,winter_target_id))
        jump winter_questions
    if winter_topic_choice=="routine":
        call winter_lines(winter_routine_lines(winter,winter_target_id),"routine:"+winter_target_id)
        $ winter=winter_seen(winter,"routine:"+winter_target_id)
        jump winter_questions
    $ winter_action_id=winter_topic_choice
    if winter_action_id in winter["done"]:
        call winter_lines(WINTER["actions"][winter_action_id]["lines"],"recall:"+winter_action_id)
        jump winter_questions
    call winter_action_run
    if winter_target_kind=="person" and winter_target_id!="mom" and winter_target_id not in [p[0] for p in winter_people(winter)]:
        hide winter_visitor
        jump winter_field
    jump winter_questions

# Version-one saves already saw automatic inn registration. Preserve their
# knowledge when they resume at a saved exploration screen.
label after_load:
    if winter_mode and winter:
        $ winter=winter_upgrade(winter)
        $ clock_text=winter_clock(winter)
    return
