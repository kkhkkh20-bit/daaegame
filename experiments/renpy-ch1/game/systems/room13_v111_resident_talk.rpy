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

    def r13_v111_resident_companion_ok(person):
        # 다람은 동행 중 현장 그림에서만 숨긴다. 학교·보호·구금 중에는 이 예외가 없다.
        if person!="daram":return False
        here=(store.room13 or {}).get("location")
        if r13_v111_value("DARAM_DETAINED") or r13_v111_value("location:daram") not in (None,here):return False
        if any(r13_v111_value("busy:"+who)=="daram_guard" for who in ("mom","nabi")):return False
        return person in globals().get("r13_v111_roam_companions",lambda:[])()

    def r13_v111_resident_talk_context(person):
        s=store.room13 or {}
        if s.get("location")=="v111_fire":return "fire"
        tense=r13_v111_tense_context()
        if tense:return tense
        if r13_v111_value("busy:"+person):return "busy"
        reactions=(globals().get("R13_V111_RESIDENT_DIALOGUE",{}).get(person) or {}).get("reactions",{})
        if 6<=s.get("day",1)<=7:
            if ("fire_safe" in reactions and r13_v111_value("D06_S03P_empty_fire_completed") is True
                    and r13_v111_value("warehouse_children_school_handover")==4
                    and r13_v111_value("KKOMI_ALIVE") is True):return "fire_safe"
            if ("fire_lost" in reactions and r13_v111_value("D06_S03_main_completed") is True
                    and r13_v111_value("warehouse_children_rescued")==3
                    and r13_v111_value("KKOMI_ALIVE") is False):return "fire_lost"
        if r13_v111_resident_piko_heard(person):return "piko_after"
        return None

    def r13_v111_resident_piko_heard(person):
        s=store.room13 or {}
        return (person in ("nabi","buri") and 3<=s.get("day",1)<=7
                and r13_v111_value("piko_alive") is False
                and "V111:E09" in s.get("evidence",[])
                and bool(r13_v111_value("piko_news3:"+person)))

    def r13_v111_resident_talk_available(person):
        catalogue=globals().get("R13_V111_RESIDENT_DIALOGUE",{})
        new=person in catalogue
        if not r13_v111_active() or (not new and person not in {v[0] for v in R13_V111_RESIDENT_TOPICS.values()}):return False
        s=store.room13 or {};v=s.get("v111") or {};here=s.get("location")
        if not 1<=s.get("day",1)<=7 or v.get("gate")=="travel":return False
        if any(getattr(store,name,False) for name in
                ("r13_meeting_active","r13_meeting_live_active","r13_cg_active","r13_aftermath_active","r13_ending_story_active")):return False
        if not r13_v111_person_alive(person) or r13_v111_value("departed:"+person):return False
        if person=="daram" and r13_v111_value("DARAM_DETAINED"):return False
        companion=r13_v111_resident_companion_ok(person) if new else False
        visible=person in r13_visible_people()
        if not visible and not companion:return False
        busy=r13_v111_value("busy:"+person)
        location=r13_v111_value("location:"+person)
        routine=(person in globals().get("R13_POPULATION146_ROUTINES",{})
                 and globals().get("r13_population146_active",lambda:False)()
                 and not globals().get("r13_population146_guarded",lambda p:True)(person))
        if location not in (None,here) and not routine:return False
        # 현장에 남아 일하는 주민은 짧게 응답할 수 있다. 부재·이송 인물을 다시 소환하지 않는다.
        if not companion and not r13_v111_actor_ready(person):
            if not (new and busy and location==here and visible):return False
        main=any(o.get("person")==person and o.get("location")==here
                 for o in r13_v111_binding().get("options",[]))
        context=r13_v111_resident_talk_context(person)
        # 화재 현장 필수 인물의 즉시 행동은 기존 구조 대화가 맡는다.
        if new:return not (context=="fire" and main)
        return not (context or main)

    def r13_v111_resident_catalogue_topics(person):
        entry=globals().get("R13_V111_RESIDENT_DIALOGUE",{}).get(person)
        if not entry:return []
        context=r13_v111_resident_talk_context(person)
        if context:
            row=(entry.get("reactions") or {}).get(context) or entry.get("urgent") or {}
            if not row:return []
            title=row["title"];lines=winter_copy.deepcopy(row["lines"])
            if context=="busy":
                busy=r13_v111_value("busy:"+person)
                if busy in ("daram_guard","school_transport","family_walk","medical_call"):
                    # 현재 맡은 돌봄·이송을 새 활동으로 대체하지 않는다.
                    replies={"daram_guard":"지금은 아이 곁을 지키고 있어요. 전할 말이 있으면 여기서 들을게요.",
                        "school_transport":"아이들과 함께 가는 중이에요. 잠깐 전할 말은 들을 수 있지만 오래 멈출 수는 없어요.",
                        "family_walk":"함께 이동하는 중이라 오래 멈출 수는 없어요. 전할 말이 있나요?",
                        "medical_call":"진료 때문에 맡은 일이 있어요. 오래 이야기하기는 어렵지만 급한 말은 전해 주세요."}
                    title="잠깐 말씀 나눠도 되겠습니까?";lines=[["dad",title],[person,replies[busy]]]
            out=[dict(key="resident146:%s:urgent_%s"%(person,context),person=person,
                      title=title,lines=lines,context=context)]
            # 다음 날 화재 이야기가 있어도 직접 들은 피코의 소식을 지우지 않는다.
            if (context in ("fire_safe","fire_lost") and store.room13.get("day",1)>6
                    and r13_v111_resident_piko_heard(person)):
                memory=(entry.get("reactions") or {}).get("piko_after")
                if memory:out.append(dict(key="resident146:%s:urgent_piko_after"%person,person=person,
                    title=memory["title"],lines=winter_copy.deepcopy(memory["lines"]),context="piko_after"))
            # 사건 직후에는 짧게 응답한다. 다음 날에는 기억을 남기되 본업도 다시 물을 수 있다.
            if (context=="piko_after" and store.room13.get("day",1)>3
                    or context in ("fire_safe","fire_lost") and store.room13.get("day",1)>6):
                row=next((row for row in entry.get("topics",[]) if row["id"]=="work"),None)
                if row:out.append(dict(key="resident146:%s:work"%person,person=person,
                         title=row["title"],lines=winter_copy.deepcopy(row["lines"]),context="ordinary"))
            return out
        day=store.room13.get("day",1)
        return [dict(key="resident146:%s:%s"%(person,row["id"]),person=person,
                     title=row["title"],lines=winter_copy.deepcopy(row["lines"]),context="ordinary")
                for row in entry.get("topics",[]) if row["days"][0]<=day<=row["days"][-1]]

    def r13_v111_resident_topics(person):
        if not r13_v111_resident_talk_available(person):return []
        day=store.room13.get("day",1);out=r13_v111_resident_catalogue_topics(person)
        # 긴급 상황에는 일상 노래나 구 캠페인의 안부를 섞지 않는다.
        if r13_v111_resident_talk_context(person):return out
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
        if isinstance(key,str) and key.startswith("resident146:"):
            pieces=key.split(":",2)
            return next((row for row in r13_v111_resident_topics(pieces[1]) if row["key"]==key),None) if len(pieces)==3 else None
        entry=R13_V111_RESIDENT_TOPICS.get(key)
        return next((row for row in r13_v111_resident_topics(entry[0]) if row["key"]==key),None) if entry else None

    def r13_v111_resident_chat_lines(key):
        spec=r13_v111_resident_chat_spec(key)
        if not spec:return []
        if spec.get("context") not in (None,"ordinary"):
            slot="thinking" if spec["context"]=="busy" else "anxious"
            return [list(packet[:2])+[dict(expression=slot,pose=slot)] for packet in spec["lines"]]
        return list(spec["lines"])

    def r13_v111_resident_chat_read(key):
        if r13_v111_resident_chat_spec(key):r13_v111_set("resident_chat_read:"+key,True)

    _r13_resident_hyeoni_verses=r13_hyeoni_verses
    def r13_hyeoni_verses():
        if not r13_v111_active():return _r13_resident_hyeoni_verses()
        return [R13_V111_RESIDENT_WINTER_VERSE]+list(globals().get("r13_sidequest_song_lines",lambda:[])())

    _r13_resident_questions=r13_v111_questions
    def r13_v111_questions(person):
        rows=list(_r13_resident_questions(person))
        for topic in r13_v111_resident_topics(person):
            read=bool(r13_v111_value("resident_chat_read:"+topic["key"]))
            rows.append((topic["title"],Return(("resident_chat",topic["key"])),read))
        return rows

    _r13_resident_business=r13_v111_has_business
    def r13_v111_required_business(person):
        # 재독 후속과 선택 자료 반응은 소식을 전할 일을 영구히 막는 필수 업무가 아니다.
        here=store.room13.get("location")
        return any(option.get("person")==person and option.get("location")==here
                   for option in r13_v111_binding().get("options",[]))

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

# 라벨 뒤의 별도 초기화: 순수 조회 함수는 카탈로그가 없으면 기존 허용 목록으로 돌아간다.
init 359 python:
    import json as _r13_resident_json
    with renpy.file("v111/resident-dialogue.json") as _r13_resident_file:
        _r13_resident_source=_r13_resident_json.load(_r13_resident_file)
    if _r13_resident_source.get("schema")!=1:raise ValueError("주민 대화 스키마가 맞지 않습니다")
    R13_V111_RESIDENT_DIALOGUE=_r13_resident_source["people"]
    for _r13_resident_person,_r13_resident_entry in R13_V111_RESIDENT_DIALOGUE.items():
        for _r13_resident_row in _r13_resident_entry["topics"]+[_r13_resident_entry["urgent"]]+list(_r13_resident_entry.get("reactions",{}).values()):
            if not _r13_resident_row.get("title") or not _r13_resident_row.get("lines"):
                raise ValueError("빈 주민 대화: "+_r13_resident_person)
            if any(len(packet)!=2 or packet[0] not in (None,"dad",_r13_resident_person)
                   for packet in _r13_resident_row["lines"]):
                raise ValueError("다른 인물의 발화를 포함한 주민 대화: "+_r13_resident_person)
