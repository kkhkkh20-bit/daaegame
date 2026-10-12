# Scene geometry, conversation ownership and free observations are separate
# from the calendar/evidence rules. All remembered state lives inside winter.
default winter_target_kind = None
default winter_target_id = None

init 46 python:
    WINTER_WORLD=json.load(renpy.file("winter-world.json"))
    WINTER_SPOTS={
        "inn":[("granny",590,180,190,330,"inn_activity"),("nabi",975,285,175,300,"world"),("resident_nubi",155,325,180,250,"inn_activity"),("bami",815,100,150,205,"world")],
        "gate":[("guard",270,240,220,340,"world"),("karo",875,295,210,285,"world"),("neoul",640,285,175,290,"world")],
        "square":[("doto",190,320,180,270,"world"),("resident_tori",925,295,170,280,"activity")],
        "post":[("seryeon",560,225,230,360,"world"),("doto",1085,320,165,270,"world")],
        "workshop":[("buri",745,315,195,275,"world")],
        "room":[],"passage":[]}

    def winter_seen(s,key):
        n=winter_copy.deepcopy(s)
        n.setdefault("seen",[])
        if key not in n["seen"]:n["seen"].append(key)
        return n

    def winter_people(s):
        result=[]
        for row in WINTER_SPOTS[s["location"]]:
            person=row[0]
            if person=="resident_tori" and s["day"]!=2:continue
            if person=="resident_nubi" and (s["day"]<3 or s["witness"] in ("detained","dead")):continue
            if person=="bami" and s["day"]<4:continue
            if person=="neoul" and not (s["witness"]=="detained" and s["day"] in (6,7)):continue
            if person=="doto" and s["location"]=="post" and s["day"]<5:continue
            result.append(row)
        # Mom is reached by physically opening the passage door, never a spoiler
        # actor on the map. Until her own approved sprite exists, her presence
        # is represented by the lit inner doorway, not another person's art.
        return result

    def winter_target_options(s,kind,key):
        owned=(WINTER_WORLD["places"][s["location"]]["objects"][key]["actions"] if kind=="object" else
            [k for k,v in WINTER_WORLD["owners"].items() if v==key and WINTER["actions"][k]["place"]==s["location"]])
        return [k for k in owned if winter_visible(s,k) or k in s["done"]]

    def winter_goal(s):
        if not winter_has(s,"inn_registered"):return "접수대의 할머니에게 말을 걸어 방을 구하자."
        if s["ap"]==0:return "오늘 조사는 마쳤다. 수첩을 확인하고 여관에서 밤을 보내자."
        if s["witness"]=="detained" and s["day"]<=7:return "누비의 이송을 막을 근거를 찾아 마을 입구의 너울에게 가자."
        if s["day"]<=3 and s["day"]>=2:return "할머니의 혐의를 확인하자. 방의 침구와 우편실의 난방비 기록이 실마리다."
        if not winter_has(s,"registry"):return "할머니에게 숙박 명부를 부탁하자. 엄마가 머문 흔적이 남아 있을까."
        if not winter_has(s,"sightings"):return "우편실의 세련에게 엄마를 마지막으로 본 곳을 물어보자."
        if not winter_has(s,"route"):return "마을 입구의 까로에게 눈에 막힌 길과 운송 기록을 물어보자."
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
        call winter_lines([("granny","어서 와요. 마차에서 온 두 분이죠?"),("dad","네. 방 하나 부탁드립니다."),("daram","장갑도 말려도 돼요?"),("granny","난로 옆에 걸어 둬요. 손부터 녹이고."),("dad","그리고… 이 사진 속 사람을 찾습니다."),("granny","……이분이 쓰던 방이 비어 있어요."),("daram","엄마가 여기서 잤어요?"),("granny","그랬어요. 지금은 없지만."),("dad","그 방으로 주십시오."),("granny","복도 끝이에요. 열세 번째 침대. 짐부터 두고 와요."),("seryeon","늦게 확인해서 죄송합니다. 두 분 체류는 제가 맡겠습니다."),("dad","아이를 또 따로 부르는 일은 없겠죠?"),("granny","숙박 보증은 내가 해요. 물을 일이 있으면 여기로 와요."),("seryeon","알겠습니다. 열흘 뒤 체류 심의까지는요."),("dad","할머니. 엄마가 남긴 연락처는 없었습니까?"),("granny","편지는 우편실의 세련 씨가 맡아요. 명부는 내가 찾아 놓을게요.")],"registration")
        $ winter=winter_flag(winter,"inn_registered")
    if "hello:"+winter_target_id not in winter.get("seen",[]):
        call winter_lines(WINTER_WORLD["greetings"][winter_target_id],"hello:"+winter_target_id)
        $ winter=winter_seen(winter,"hello:"+winter_target_id)
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
        call winter_lines(WINTER_WORLD["greetings"][winter_target_id],"hello:"+winter_target_id)
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
    if winter_mode and winter and winter.get("version",1)<2:
        $ winter=winter_flag(winter,"inn_registered")
        $ winter=dict(winter,version=2)
    return
