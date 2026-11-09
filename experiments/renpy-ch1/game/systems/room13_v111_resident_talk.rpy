# 기존 일반 주민 대화 중 일상 내용만 본편에 연결한다. 사건·보상·옛 진행 라벨은 실행하지 않는다.
init 358 python:
    MS14_SPEAKERS.update({"설이":"resident_seol","현이":"resident_hyeoni","여니":"resident_yeoni"})
    R13_V111_RESIDENT_TOPICS={
        "life:resident_badook:work":("resident_badook",1,4),
        "life:resident_owlgp:work":("resident_owlgp",1,4),
        "life:resident_seol:work":("resident_seol",1,4),
        "life:resident_seol:after":("resident_seol",5,7),
        "smalltalk:yeoni_seam":("resident_yeoni",1,4),
        "life:resident_yeoni:after":("resident_yeoni",5,7),
        "hyeoni:song":("resident_hyeoni",2,7),
    }
    R13_V111_RESIDENT_QUESTION_TITLES={
        "hyeoni:song":"한 곡 들려주시겠어요?",
        "life:resident_badook:work":"밤 순찰도 혼자 다닙니까?",
        "life:resident_owlgp:work":"지금도 직접 기록을 하십니까?",
    }
    # systems/room13_new_cast.rpy의 기본 겨울 노래 원문. 본편에서는 구 캠페인의 사건 플래그로 가사를 만들지 않는다.
    R13_V111_RESIDENT_WINTER_VERSE="「눈은 쌓이고 마차는 안 오고, 고개 너머 봄은 아직 멀어라」"

    def r13_v111_resident_talk_available(person):
        if not r13_v111_active() or person not in {v[0] for v in R13_V111_RESIDENT_TOPICS.values()}:return False
        s=store.room13 or {};v=s.get("v111") or {}
        if not 1<=s.get("day",1)<=7 or v.get("gate")=="travel" or s.get("location")=="v111_fire":return False
        if r13_v111_tense_context() or any(getattr(store,name,False) for name in
                ("r13_meeting_active","r13_meeting_live_active","r13_cg_active","r13_aftermath_active","r13_ending_story_active")):return False
        if not r13_v111_person_alive(person) or r13_v111_value("departed:"+person) or r13_v111_value("busy:"+person):return False
        if not r13_v111_actor_ready(person) or person not in r13_visible_people():return False
        # 현재 사건에서 그 사람에게 할 정식 질문이 있으면 먼저 그 대화에 응한다.
        return not any(o.get("person")==person and o.get("location")==s.get("location")
                       for o in r13_v111_binding().get("options",[]))

    def r13_v111_resident_topics(person):
        if not r13_v111_resident_talk_available(person):return []
        day=store.room13.get("day",1);out=[]
        for key,(who,first,last) in R13_V111_RESIDENT_TOPICS.items():
            if who!=person or not first<=day<=last:continue
            spec=ROOM13.get("topics",{}).get(key)
            if not spec or spec.get("npc")!=person:continue
            # 같은 이름의 옛 사건이 보상·조건을 얻게 되어도 여기서 조용히 활성화하지 않는다.
            if any(spec.get(field) for field in ("give","flags","need","not_flags","state","case","read_after","special","cost")):continue
            days=spec.get("day",(1,14))
            if not days[0]<=day<=days[-1]:continue
            if spec.get("period") is not None and store.room13.get("period") not in spec["period"]:continue
            lines=spec.get("lines") or []
            if key!="hyeoni:song" and (not lines or any(packet[0] not in (None,"dad",person) for packet in lines)):continue
            if not spec.get("title"):continue
            out.append(dict(key=key,person=person,title=R13_V111_RESIDENT_QUESTION_TITLES.get(key,spec["title"]),lines=winter_copy.deepcopy(lines)))
        return out

    def r13_v111_resident_chat_spec(key):
        entry=R13_V111_RESIDENT_TOPICS.get(key)
        return next((row for row in r13_v111_resident_topics(entry[0]) if row["key"]==key),None) if entry else None

    def r13_v111_resident_chat_lines(key):
        spec=r13_v111_resident_chat_spec(key)
        return list(spec["lines"]) if spec else []

    def r13_v111_resident_chat_read(key):
        if r13_v111_resident_chat_spec(key):r13_v111_set("resident_chat_read:"+key,True)

    _r13_resident_hyeoni_verses=r13_hyeoni_verses
    def r13_hyeoni_verses():
        return [R13_V111_RESIDENT_WINTER_VERSE] if r13_v111_active() else _r13_resident_hyeoni_verses()

    _r13_resident_questions=r13_v111_questions
    def r13_v111_questions(person):
        rows=list(_r13_resident_questions(person))
        for topic in r13_v111_resident_topics(person):
            read=bool(r13_v111_value("resident_chat_read:"+topic["key"]))
            rows.append((topic["title"],Return(("resident_chat",topic["key"])),read))
        return rows

    _r13_resident_business=r13_v111_has_business
    def r13_v111_has_business(person):
        return bool(r13_v111_resident_topics(person)) or _r13_resident_business(person)

label r13_v111_resident_chat(key):
    $ v111_resident_spec=r13_v111_resident_chat_spec(key)
    if v111_resident_spec:
        if key=="hyeoni:song":
            call r13_hyeoni_song
        else:
            call r13_lines(r13_v111_resident_chat_lines(key),"topic:"+key)
        $ r13_v111_resident_chat_read(key)
    return
