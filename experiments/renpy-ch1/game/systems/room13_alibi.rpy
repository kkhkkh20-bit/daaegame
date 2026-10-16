# Who was where, and does it add up (owner 0.18.79): "이벤트와 로직이 치밀해야 해. 사람들이 정신없으면서
# 퍼즐을 맞춰 가는 느낌, 관계성." Design: docs/ALIBI_RELATIONS.md.
#   1. Story pins: at moments the script already narrates, the schedule (r13_where) follows the script
#      instead of the weekly routine. Day 1 evening: 토실 is in the forest on granny's errand and 칼바람
#      walks her back. Day 4 evening (the incident): the people the incident scene never shows are
#      elsewhere (부엉이 할아버지 in 13호, 은호·구슬·백 부인 at the store, 우박 at the clinic, 토실 in the back room).
#   2. Alibi questions: after such a moment, the people who were around can be asked where they were.
#      Answers follow the pins; some lie or cover for someone because of who they are to each other.
#   3. Cross-checks: two statements that cannot both be true make Dad notice it, and the notebook keeps
#      the comparison. Flags only: no record, no change to the meeting/trial code (another chat owns it).
init 147 python:
    # (day, period): {person: place}
    R13_STORY_PINS={
        (1,2):{"resident_tosil":"forest","resident_kalbaram":"forest"},
        (4,2):{"resident_owlgp":"hall","resident_eunho":"store","resident_guseul":"store",
            "resident_madam":"store","resident_ubak":"clinic","resident_tosil":"inn"},
    }
    R13_STORY_PIN_REASONS={
        (1,2,"resident_tosil"):("보온병을 안고 눈 위 발자국을 따라 걷는다.","할머니가 부인에게 차를 갖다 드리라며 숲으로 보냈다(엄마를 따라간 발소리)."),
        (1,2,"resident_kalbaram"):("큰 전나무 밑에서 우는 아이를 발견한다.","덫을 보고 돌아오다 토실을 여관까지 데려다준다."),
        (4,2,"resident_owlgp"):("13호실에서 다람이와 함께 있다.","할머니와 약속한 저녁 물건 전달(사건 당사자)."),
        (4,2,"resident_eunho"):("창고에서 구슬과 재고를 센다.","납품 장부 마감 날. 따로 든 외상 장부가 있다."),
        (4,2,"resident_guseul"):("은호 옆에서 재고 수를 받아 적는다.","은호의 알리바이를 대 주는 견습."),
        (4,2,"resident_madam"):("자기 창고에서 뭉치와 보관함을 센다.","저녁마다 여관에 오던 백 부인이 이날은 여관에 없다."),
        (4,2,"resident_ubak"):("진료소에서 서리의 기록을 정리한다.","비명 소식에 서리만 먼저 뛰어간다."),
        (4,2,"resident_tosil"):("여관 뒷방 이불 속에 있다.","할머니가 일찍 자라고 했다. 빨래방 쪽 벽 안 발소리를 듣는다."),
    }

    _r13_alibi_where=r13_where
    def r13_where(person):
        s=store.room13 or {}
        pins=R13_STORY_PINS.get((s.get("day"),min(s.get("period",0),2)))
        if pins and person in pins:return pins[person]
        return _r13_alibi_where(person)

    _r13_alibi_activity=r13_activity_text
    def r13_activity_text(person):
        s=store.room13 or {}
        spec=R13_STORY_PIN_REASONS.get((s.get("day"),min(s.get("period",0),2),person))
        return spec[0] if spec else _r13_alibi_activity(person)

    # ---- alibi statements ----
    # moment: (title, first day it can be asked, need flags)
    R13_ALIBI_MOMENTS={
        "night1":("첫날 밤",2,[]),
        "case":("13호 사건이 난 저녁",5,[]),
    }
    # (moment, person): dict(claim=lines, truth=(flag, lines) shown instead once the flag is set)
    R13_ALIBI={
        ("night1","granny"):dict(claim=[
            ("dad","저희가 도착한 첫날 밤, 할머니는 어디 계셨습니까?"),
            ("granny","접수대를 지켰죠. 손님이 새로 든 날엔 늦게까지 앉아 있어요."),
            ("dad","토실이는요?"),
            ("granny","일찍 재웠어요. 그 애는 해만 지면 졸려 해요.")]),
        ("night1","resident_tosil"):dict(claim=[
            ("dad","토실아, 우리가 온 첫날 밤엔 뭐 했니?"),
            ("resident_tosil","……자고 있었어요. 진짜예요."),
            ("dad","(대답이 너무 빠르다. 눈도 마주치지 않는다.)",{"thought":True})],
            truth=("tosil_errand_seen",[
            ("dad","토실아, 첫날 밤에도 숲에 갔었지?"),
            ("resident_tosil","……네. 할머니가 부인한테 차 갖다 드리라고 해서요. 거짓말해서 죄송해요.")])),
        ("night1","resident_kalbaram"):dict(claim=[
            ("dad","고개 마차가 들어온 날 밤, 어디 계셨습니까?"),
            ("resident_kalbaram","숲 끝 덫을 보고 내려왔소."),
            ("resident_kalbaram","큰 전나무 밑에서 흰 토끼 아이가 보온병을 안고 울고 있었지. 여관까지 데려다줬소."),
            ("dad","왜 아무에게도 말하지 않으셨습니까?"),("resident_kalbaram","묻는 사람이 없었으니까.")]),
        ("night1","resident_hyeoni"):dict(claim=[
            ("dad","저희가 온 첫날 밤에도 식당에서 노래하셨습니까?"),
            ("resident_hyeoni","네. 새 손님이 왔다고 다들 수군거려서 노래가 잘 팔렸죠."),
            ("resident_hyeoni","할머니가 부엌에 와서 보온병에 따뜻한 차를 가득 담아 가셨어요. 손님 방에 가져가시나 했죠.")]),
        ("case","granny"):dict(claim=[
            ("dad","그날 저녁, 할머니는 어디 계셨습니까?"),
            ("granny","식당을 보고 있었어요. 손님들이랑 내내 같이 있었죠. 비명이 나고 나서야 부엌으로 갔고요.")]),
        ("case","resident_hyeoni"):dict(claim=[
            ("dad","그날 저녁 식당에 할머니가 계셨습니까?"),
            ("resident_hyeoni","처음에 국을 떠 주시고는 부엌 쪽으로 가셨어요. 그 뒤로 식당엔 안 오셨고요."),
            ("resident_hyeoni","비명이 들린 다음엔 다들 일어서서 2층만 쳐다봤어요.")]),
        ("case","resident_dalgeurak"):dict(claim=[
            ("dad","사건 날 저녁, 식당에서 할머니를 보셨습니까?"),
            ("resident_dalgeurak","저녁 내내 내 자리에서 장부를 썼소. 할머니는 초저녁에 한 번 지나갔을 뿐이오."),
            ("resident_dalgeurak","비명 뒤에 '공구를 가지러 간다'며 부엌 뒷문으로 나가더구먼. 식당 쪽으론 안 왔소.")]),
        ("case","resident_tok"):dict(claim=[
            ("dad","사건 날 저녁엔 어디 계셨습니까?"),
            ("resident_tok","식당 구석에서 계측기를 뜯어 놓고 있었어요. 낮엔 할머니 핀을 새로 달아 드렸고요."),
            ("resident_tok","할머니요? 식당엔 거의 안 계셨어요. 국 냄새만 나고 사람은 없었죠.")]),
        ("case","resident_tosil"):dict(claim=[
            ("dad","토실아, 사건 난 날 저녁엔 어디 있었니?"),
            ("resident_tosil","할머니가 일찍 자라고 해서 뒷방에 있었어요."),
            ("resident_tosil","비명 소리 조금 뒤에요, 빨래방 쪽 벽 안에서 누가 걷는 소리가 났어요. 쥐인 줄 알았는데 발소리였어요.")]),
        ("case","resident_eunho"):dict(claim=[
            ("dad","사건 날 저녁엔 어디 계셨습니까?"),
            ("resident_eunho","창고에서 구슬이랑 재고를 셌소. 그날이 납품 장부 마감이었으니까. 구슬한테 물어보시오.")]),
        ("case","resident_guseul"):dict(claim=[
            ("dad","사건 날 저녁, 은호 사장과 함께 계셨습니까?"),
            ("resident_guseul","네, 창고에서 같이 재고를 셌어요."),
            ("resident_guseul","……사장님은 우리 장부 말고 다른 장부를 하나 따로 들고 계셨어요. 그건 저도 못 보게 하셨고요.")]),
        ("case","resident_ubak"):dict(claim=[
            ("dad","사건 날 저녁엔 어디 계셨습니까?"),
            ("resident_ubak","진료소에서 스승님 기록을 정리했어요. 소식이 오자 스승님만 먼저 뛰어가셨고 저는 진료소를 지켰어요.")]),
        ("case","resident_madam"):dict(claim=[
            ("dad","사건 날 저녁에는 여관에 오지 않으셨다던데요."),
            ("resident_madam","내 창고에서 뭉치랑 보관함을 셌어요. 매일 가던 여관도 그날은 이상하게 가기 싫더라고요."),
            ("dad","(저녁마다 여관에 오던 사람이 하필 그날만 오지 않았다.)",{"thought":True})]),
    }
    # Two statements that cannot both be true: (needed statements, Dad's thought, flag, notebook line)
    R13_ALIBI_CROSS=[
        ([("night1","granny"),("night1","resident_kalbaram")],
            [("dad","(할머니는 토실이를 일찍 재웠다고 했다. 그런데 칼바람은 그날 밤 숲에서 우는 토실이를 여관까지 데려다줬다.)",{"thought":True}),
             ("dad","(누가 그 밤에 아이를 숲으로 보냈을까.)",{"thought":True})],
            "alibi_x_night1","할머니는 첫날 밤 토실을 재웠다고 했지만, 칼바람은 그 밤 숲에서 토실을 데려왔다."),
        ([("night1","resident_hyeoni"),("night1","resident_kalbaram")],
            [("dad","(첫날 밤 할머니가 보온병에 차를 담아 갔다. 숲에서 발견된 아이도 보온병을 안고 있었다.)",{"thought":True})],
            "alibi_x_thermos","할머니가 담아 간 보온병과, 숲에서 토실이 안고 있던 보온병."),
        ([("case","granny"),("case","resident_hyeoni")],
            [("dad","(할머니는 저녁 내내 식당에 있었다고 했다. 현이는 할머니가 처음에 국만 뜨고 부엌으로 갔다고 한다.)",{"thought":True})],
            "alibi_x_dining","할머니는 사건 저녁 내내 식당에 있었다고 했지만, 식당 사람들은 할머니를 거의 보지 못했다."),
        ([("case","granny"),("case","resident_tok")],
            [("dad","(톡도 그날 저녁 식당에 할머니가 거의 없었다고 한다. 할머니 말과 두 사람 말이 맞지 않는다.)",{"thought":True})],
            "alibi_x_dining2",""),
        ([("case","resident_dalgeurak"),("case","resident_tosil")],
            [("dad","(비명 뒤 할머니는 부엌 뒷문으로 나갔다. 그 조금 뒤, 토실은 빨래방 쪽 벽 안에서 발소리를 들었다.)",{"thought":True}),
             ("dad","(부엌과 빨래방 사이, 벽 안에 길이 있다면…….)",{"thought":True})],
            "alibi_x_wall","비명 뒤 부엌 뒷문으로 나간 할머니, 그리고 빨래방 쪽 벽 안의 발소리."),
        ([("case","resident_eunho"),("case","resident_guseul")],
            [("dad","(은호와 구슬은 서로의 알리바이가 된다. 다만 은호는 그날도 따로 든 장부가 있었다.)",{"thought":True})],
            "alibi_x_store",""),
    ]

    def r13_alibi_heard(moment,person):
        return r13_has("alibi:%s:%s"%(moment,person))

    for (_r13_m,_r13_p),_r13_spec in R13_ALIBI.items():
        _r13_title,_r13_from,_r13_need=R13_ALIBI_MOMENTS[_r13_m]
        ROOM13["topics"]["alibi:%s:%s"%(_r13_m,_r13_p)]=dict(npc=_r13_p,title="%s, 어디 계셨습니까?"%_r13_title,
            day=[_r13_from,14],need=list(_r13_need),give=[],flags=[],lines=list(_r13_spec["claim"]))
        R13_TOPIC_LABELS["alibi:%s:%s"%(_r13_m,_r13_p)]="r13_alibi_topic"

    _r13_alibi_topics=r13_topics
    def r13_topics(person):
        rows=[]
        for key,spec in _r13_alibi_topics(person):
            if key.startswith("alibi:case:") and (store.room13 or {}).get("case_state")!="occurred":continue
            rows.append((key,spec))
        return rows

    def r13_alibi_lines(key):
        _,m,p=key.split(":",2)
        spec=R13_ALIBI[(m,p)]
        truth=spec.get("truth")
        if truth and r13_has(truth[0]):return truth[1]
        return spec["claim"]

    def r13_alibi_new_crosses():
        return [c for c in R13_ALIBI_CROSS if not r13_has(c[2]) and all(r13_alibi_heard(m,p) for m,p in c[0])]

    _r13_alibi_notes=r13_first_mystery_notes
    def r13_first_mystery_notes():
        rows=list(_r13_alibi_notes())
        for m,(title,_d,_n) in R13_ALIBI_MOMENTS.items():
            heard=[p for (mm,p) in R13_ALIBI if mm==m and r13_alibi_heard(m,p)]
            if not heard:continue
            facts=[c[3] for c in R13_ALIBI_CROSS if c[0][0][0]==m and r13_has(c[2]) and c[3]]
            fact="물어본 사람: "+", ".join(R13_NAMES.get(p,p) for p in heard)+"."
            if facts:fact+=" "+" ".join(facts)
            rows.append(dict(title=title+", 누가 어디 있었나",fact=fact,
                question="맞지 않는 말이 있다. 누가 왜 거짓말을 할까?" if facts else "서로의 말이 맞는지, 그 자리에 있던 다른 사람에게도 물어보자.",
                hint="그 시각 같은 장소에 있던 사람은 서로의 증인이 된다.",keys=[]))
        return rows

label r13_alibi_topic:
    $ _ab_key=r13_topic
    call r13_lines(r13_alibi_lines(_ab_key),"alibi:"+_ab_key[6:]+(":truth" if R13_ALIBI[tuple(_ab_key.split(":",2)[1:])].get("truth") and r13_has(R13_ALIBI[tuple(_ab_key.split(":",2)[1:])]["truth"][0]) else ""))
    $ r13_flag(_ab_key)
    $ _ab_new=r13_alibi_new_crosses()
    while _ab_new:
        $ _ab_cross=_ab_new.pop(0)
        call r13_lines(_ab_cross[1],"alibi:cross:"+_ab_cross[2])
        $ r13_flag(_ab_cross[2])
    return
