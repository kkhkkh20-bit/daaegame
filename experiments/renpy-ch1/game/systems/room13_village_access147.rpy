# 공공 방문은 사건 진행과 분리한다. 선택·인계·자료 획득은 기존 본편이 맡는다.
init 382 python:
    R13_VILLAGE147_PUBLIC_PLACES=("inn","hall","room13","dining","square","gate","post","workshop","clinic","school","store")
    R13_VILLAGE147_OBSERVATIONS={
        ("clinic","notes"):"기록철이 꽂혀 있다. 환자의 기록은 담당자 허락 없이 펼치지 않는다.",
        ("store","ledger"):"물자 장부가 놓여 있다. 기록은 담당자에게 물어보고 확인하자.",
        ("school","desks"):"책상마다 높이가 조금씩 다르다. 의자는 책상 아래에 밀어 넣어 두었다.",
        ("school","stove"):"난로 옆에 장작을 모아 두었다. 난로 가까운 바닥의 눈이 녹아 있다.",
        ("school","blankets"):"접어 둔 담요들이 쌓여 있다. 쓴 뒤 다시 덮기 좋게 가장자리를 맞춰 놓았다.",
        ("workshop","plans"):"작업대에 도면을 펼쳐 놓았다. 자와 연필을 종이 위에 얹어 두었다.",
        ("post","notice"):"영업 안내가 붙어 있다. 마을 밖 우편은 고갯길이 열려야 출발한다.",
    }

    def r13_village147_lunch_ready():
        s=store.room13 or {}
        return bool(r13_v111_active() and s.get("day")==2 and s.get("period")==0
                    and (s.get("v111") or {}).get("gate")=="morning_finish2"
                    and not r13_v111_tense_context())

    def r13_village147_move_message(key,target):
        if not r13_v111_active() or store.room13.get("day")!=2:return None
        if key=="afternoon2" and target=="forest":
            return "네로를 만나 일을 마치고 돌아오면 해가 집니다.\n피코를 식당으로 데려오는 일은 아직 마치지 않았습니다.\n네로를 만나러 갈까요?"
        if key=="shelter_enter" and target=="dining":
            return "피코와 식당에 들어가 자리를 안내하고 저녁으로 넘어갑니다.\n함께 들어갈까요?"
        return None

    def r13_village147_move_caption(key,target):
        return "네로 만나러 가기" if key=="afternoon2" and target=="forest" else "피코와 들어가기"

    _r13_village147_ambient=r13_v111_ambient_text
    def r13_v111_ambient_text(key,spec):
        s=store.room13 or {};here=s.get("location")
        if r13_v111_active() and 2<=s.get("day",1)<=7 and here in R13_VILLAGE147_PUBLIC_PLACES:
            key=r13_v111_object_key(key)
            main=any(o.get("object")==key and o.get("location")==here for o in r13_v111_binding().get("options",[]))
            record=R13_V111_RECORD_OBJECTS.get((here,key))
            if not main and record:
                if r13_v111_owned(record):return _r13_village147_ambient(key,spec)
                return R13_VILLAGE147_OBSERVATIONS.get((here,key))
            if not main and key.startswith("v111_"):
                if here=="gate" and key in ("v111_fence","v111_bucket") and s["day"]<4:return None
            if not main and (here,key) in R13_VILLAGE147_OBSERVATIONS:
                if here not in ("school","workshop") or s["day"]==2:
                    return R13_VILLAGE147_OBSERVATIONS[(here,key)]
        return _r13_village147_ambient(key,spec)

    _r13_village147_observation_allowed=r13_observation_chat_allowed
    def r13_observation_chat_allowed(identity):
        if (r13_v111_active() and store.room13.get("day",1)<6
                and r13_observation_key(identity)==("school","desks")):return False
        return _r13_village147_observation_allowed(identity)

    _r13_village147_visible=r13_visible_people
    def r13_visible_people():
        people=_r13_village147_visible()
        if not r13_v111_active() or not 2<=store.room13.get("day",1)<=7:return people
        here=store.room13.get("location");binding=r13_v111_binding();places={}
        # 현재 본편에서 약속한 재실이 평상 시간표보다 우선한다. 같은 배우를 다른 곳에 복제하지 않는다.
        for option in binding.get("options",[]):
            if option.get("person") and option.get("location"):
                places.setdefault(option["person"],set()).add(option["location"])
        for place,members in (binding.get("people_by_location") or {}).items():
            for person in members:places.setdefault(person,set()).add(place)
        if binding.get("location"):
            for person in binding.get("people",[]):places.setdefault(person,set()).add(binding["location"])
        return [person for person in people if (person not in places or here in places[person])
                and not r13_village147_delivery_away(person)]

    def r13_village147_delivery_away(person):
        s=store.room13 or {}
        if (not r13_v111_active() or person!="nabi" or s.get("day")!=2 or s.get("period")!=2):return False
        binding=r13_v111_binding()
        return not (person in binding.get("people",[]) or any(person in members for members in (binding.get("people_by_location") or {}).values())
                    or any(option.get("person")==person for option in binding.get("options",[])))

    _r13_village147_where=r13_where
    def r13_where(person):
        if r13_village147_delivery_away(person):return None
        return _r13_village147_where(person)

    _r13_village147_goal=r13_v111_goal
    def r13_v111_goal():
        if r13_village147_lunch_ready():return "아침 조사를 마쳤다. 더 둘러본 뒤, 원할 때 점심을 먹으러 가자."
        return _r13_village147_goal()
