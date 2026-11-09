# 1부 일상 장면의 인원을 분산한다. 사건 인물과 실제 진행 위치는 기존 이야기가 우선한다.
init 374 python:
    R13_POPULATION146_LIMIT=5
    R13_POPULATION146_PUBLIC=frozenset(("gate","square","inn","hall","dining","post","workshop","clinic","school","store"))
    R13_POPULATION146_ROUTINES={
        "doto":("post","hall","inn"),
        "resident_owlgp":("post","inn","dining"),
        "resident_ppul":("gate","square","inn"),
        "resident_badook":("gate","square","school"),
        "resident_yeoni":("inn","inn","dining"),
        "resident_tori":("inn","inn","dining"),
        "resident_seol":("square","square","inn"),
        "resident_hyeoni":("square","inn",None),
        "resident_ttadak":("workshop","workshop",None),
    }
    # 초반에는 독립 역할이 없는 배경 배역을 한꺼번에 세우지 않는다. 사건·수락 의뢰의 표시 대상은 보존한다.
    R13_POPULATION146_QUIET_EXTRAS=frozenset(("resident_kkwak","resident_sling","resident_mungchi","resident_guseul"))
    R13_POPULATION146_HOSTS={"gate":("guard","karo"),"square":("resident_seol",),"inn":("granny",),
        "dining":("nabi",),"hall":("doto",),"post":("seryeon",),"workshop":("buri",),
        "clinic":("resident_seori",),"school":("resident_teacher",),"store":("resident_eunho",)}
    R13_POPULATION146_PRIORITY=("resident_yeoni","resident_tori","resident_seol","buri","resident_hyeoni",
        "resident_owlgp","doto","resident_lamplighter","resident_badook","resident_ppul")

    def r13_population146_active():
        s=getattr(store,"room13",None) or {}
        if not r13_v111_active() or not 1<=s.get("day",1)<=7:return False
        if (s.get("v111") or {}).get("gate")=="travel":return False
        if s.get("case_state")=="occurred" or r13_v111_value("DARAM_DETAINED"):return False
        if globals().get("r13_v111_tense_context",lambda:None)():return False
        return not any(getattr(store,name,False) for name in ("r13_meeting_active","r13_meeting_live_active",
            "r13_cg_active","r13_aftermath_active","r13_ending_story_active"))

    def r13_population146_needed_places(person):
        s=store.room13;v=s.get("v111") or {};b=r13_v111_binding();here=s.get("location")
        places={o.get("location") or b.get("location") or here for o in b.get("options",[]) if o.get("person")==person}
        by_place=b.get("people_by_location")
        if by_place is not None:
            places.update(place for place,people in by_place.items() if person in people)
        elif person in b.get("people",[]):places.add(b.get("location") or here)
        if person in b.get("approach",{}):places.add(b.get("location") or here)
        physical=r13_v111_value("location:"+person)
        # 이 아홉 주민의 지난 선택 대화가 people에 남아 있다고 현장 필수 배우로 고정하지 않는다.
        # 현재 정식 선택·명시 업무가 있으면 위의 계약과 busy 조건이 계속 우선한다.
        if (physical and person in v.get("people",[])
                and (person not in R13_POPULATION146_ROUTINES or r13_v111_value("busy:"+person))):
            places.add(physical)
        return places

    def r13_population146_side_people():
        # 상태만 읽는 의뢰 소유자 목록이다. where/visible을 부르는 함수를 넣으면 재귀가 생긴다.
        return set(globals().get("r13_sidequest_priority_people",lambda:[])() or [])

    def r13_population146_guarded(person):
        return bool(r13_population146_needed_places(person) or r13_v111_value("busy:"+person)
                    or r13_v111_value("departed:"+person) or not r13_v111_person_alive(person))

    _r13_population146_where=r13_where
    def r13_where(person):
        original=_r13_population146_where(person)
        if not r13_population146_active() or person not in R13_POPULATION146_ROUTINES:return original
        if r13_population146_guarded(person):return original
        s=store.room13;day=s.get("day",1);period=min(s.get("period",0),2)
        if person=="resident_hyeoni":
            if day==1:return original
            if day==3 and period==0:return None
            if period==0 and day in (5,7):return "inn"
        return R13_POPULATION146_ROUTINES[person][period]

    _r13_population146_actor_ready=r13_v111_actor_ready
    def r13_v111_actor_ready(person):
        # 구 저장의 지난 대화 위치는 일상 일과를 재배치한 뒤의 현재 재실을 막지 않는다.
        # 정식 사건 인물·명시 업무·부재·사망·위기에서는 기존 실제 위치 계약을 유지한다.
        if (r13_population146_active() and person in R13_POPULATION146_ROUTINES
                and not r13_population146_guarded(person)):
            return r13_where(person)==store.room13.get("location")
        return _r13_population146_actor_ready(person)

    def r13_population146_select(people,place,protected,side_people=()):
        people=list(dict.fromkeys(people));protected=set(protected);side_people=set(side_people)
        required=protected|side_people
        visible=[p for p in people if p not in R13_POPULATION146_QUIET_EXTRAS or p in required]
        kept=[p for p in visible if p in required]
        rank={}
        for person in R13_POPULATION146_HOSTS.get(place,())+R13_POPULATION146_PRIORITY:
            if person not in rank:rank[person]=len(rank)
        optional=[p for p in visible if p not in required]
        optional=sorted(enumerate(optional),key=lambda row:(rank.get(row[1],100),row[0]))
        kept += [person for _,person in optional[:max(0,R13_POPULATION146_LIMIT-len(kept))]]
        chosen=set(kept)
        # 기존 무대 순서·깊이 순서는 보존한다. 현재 필수 배우가 다섯 이상이면 그 배우를 숨기지 않는다.
        return [p for p in visible if p in chosen]

    _r13_population146_visible=r13_visible_people
    def r13_visible_people():
        people=_r13_population146_visible()
        s=getattr(store,"room13",None) or {};here=s.get("location")
        if not r13_population146_active() or here not in R13_POPULATION146_PUBLIC:return people
        protected={p for p in people if here in r13_population146_needed_places(p)}
        return r13_population146_select(people,here,protected,r13_population146_side_people())
