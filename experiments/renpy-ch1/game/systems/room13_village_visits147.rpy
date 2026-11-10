# 선택 방문은 현장에 있는 사람과만 진행하며 본편 대기와 별도 기억을 남긴다.
init 384 python:
    from collections.abc import Mapping as R13Visit147Mapping
    MS14_SPEAKERS.update({"토리":"resident_tori"})
    with renpy.file("v111/village-visits147.json") as _r13_visit147_file:
        R13_VISITS147=json.load(_r13_visit147_file)["events"]

    def r13_visit147_problems():
        problems=[];ids=set()
        for key,spec in R13_VISITS147.items():
            if spec.get("owner") not in spec.get("members",[]):problems.append(key+": 주인공 누락")
            if any(person not in CAST for person in spec.get("members",[])):problems.append(key+": 없는 주민")
            if spec.get("source_place") not in ROOM13.get("objects",{}):problems.append(key+": 없는 장소")
            results=[choice.get("result") for choice in spec.get("choices",[])]
            if set(results)!={"help","watch","decline"} or len(results)!=3:problems.append(key+": 선택 결과 누락")
            phases={"intro","passed","noticed"}|set(results)|{"memory_"+result for result in results}
            if not phases<=set(spec.get("blocks",{})):problems.append(key+": 대화 단계 누락")
            for phase,lines in spec.get("blocks",{}).items():
                for line in lines:
                    lid=line.get("id")
                    if not lid or lid in ids:problems.append(key+": 대사 ID 중복 또는 누락")
                    ids.add(lid)
                    speaker=line.get("speaker");person=MS14_SPEAKERS.get(speaker)
                    if speaker is not None and person not in set(spec["members"])|{"dad","daram"}:problems.append(key+": 부재 인물 대사")
                    if person=="daram" and not line.get("companion"):problems.append(key+": 다람 동행 조건 누락")
                    if not line.get("text") or line.get("kind") not in ("narration","dialogue"):problems.append(key+": 대사 형식")
        return problems
    if r13_visit147_problems():raise Exception("방문 장면 등록 오류: "+"; ".join(r13_visit147_problems()))

    def r13_visit147_state(key):
        group=((store.room13 or {}).get("v111") or {}).get("village_visits",{})
        row=group.get(key,{}) if isinstance(group,R13Visit147Mapping) else {}
        return winter_copy.deepcopy(dict(row)) if isinstance(row,R13Visit147Mapping) else {}

    def r13_visit147_calm():
        s=store.room13 or {};v=s.get("v111") or {};group=v.get("village_visits",{})
        if not isinstance(group,R13Visit147Mapping) or any(not isinstance(row,R13Visit147Mapping) for row in group.values()):return False
        if not globals().get("r13_sidequest_calm",lambda:False)():return False
        # 확인한 상실 당일에는 생활의 반가운 회상보다 현재 사건에 반응한다.
        if s.get("day")==3 and r13_v111_value("piko_alive") is False and "V111:E09" in s.get("evidence",[]):return False
        if s.get("day")==6 and (r13_v111_value("D06_S03P_empty_fire_completed") is True or r13_v111_value("D06_S03_main_completed") is True):return False
        return True

    def r13_visit147_ready(people):
        if not r13_visit147_calm():return False
        here=store.room13.get("location")
        required=[option for option in r13_v111_binding().get("options",[]) if option.get("location")==here]
        if any(option.get("person") in people for option in required):return False
        visible=set(r13_visible_people())
        return all(person in visible and r13_v111_actor_ready(person) and r13_v111_person_alive(person)
                   and not r13_v111_value("busy:"+person) and not r13_v111_value("departed:"+person) for person in people)

    def r13_visit147_source_window(key):
        spec=R13_VISITS147.get(key);s=store.room13 or {}
        return bool(spec and s.get("day")==spec["source_day"] and s.get("period") in spec["source_periods"])

    def r13_visit147_source_allowed(key):
        spec=R13_VISITS147.get(key)
        if not spec or not r13_visit147_source_window(key):return False
        if store.room13.get("location")!=spec["source_place"]:return False
        if r13_visit147_state(key).get("status","unseen") not in ("unseen","noticed"):return False
        if key=="sleeve" and r13_sidequest_status("seam")!="unseen":return False
        return r13_visit147_ready(spec["members"])

    def r13_visit147_memory_allowed(key):
        spec=R13_VISITS147.get(key);s=store.room13 or {}
        if not spec or not 2<=s.get("day",1)<=7:return False
        if s.get("day")==2 and s.get("period",0)<2:return False
        # 이미 맡은 수선은 기존 작업·보고·결과 대화가 맡는다. 손 빼기와 재봉 완료를 섞지 않는다.
        if key=="sleeve" and r13_sidequest_status("seam")!="unseen":return False
        return r13_visit147_ready([spec["owner"]])

    def r13_visit147_person_actions(person):
        rows=[]
        for key,spec in R13_VISITS147.items():
            if person!=spec["owner"]:continue
            state=r13_visit147_state(key)
            if r13_visit147_source_allowed(key):rows.append(dict(event=key,action="visit",title=spec["source_title"],read=False))
            elif r13_visit147_memory_allowed(key):
                known=state.get("result") in ("help","watch","decline") or state.get("intro_seen") is True or state.get("status")=="noticed"
                rows.append(dict(event=key,action="memory",title=spec["memory_title"] if known else spec["passed_title"],read=bool(state.get("memory_seen"))))
        return rows

    def r13_visit147_allowed(key,action):
        spec=R13_VISITS147.get(key)
        return bool(spec and any(row["event"]==key and row["action"]==action for row in r13_visit147_person_actions(spec["owner"])))

    def r13_visit147_record(key,action,result=None):
        check="visit" if action in ("noticed","complete") else action
        if not r13_visit147_allowed(key,check):return False
        if action=="complete" and result not in {choice["result"] for choice in R13_VISITS147[key]["choices"]}:return False
        if action not in ("noticed","complete","memory"):return False
        n=winter_copy.deepcopy(store.room13);group=n["v111"].setdefault("village_visits",{})
        row=dict(group.get(key,{}))
        if action=="noticed":row.update(status="noticed",intro_seen=True)
        elif action=="complete":row.update(status="completed",intro_seen=True,result=result,completed_day=n["day"],completed_period=n["period"])
        else:
            if row.get("status") not in ("completed","passed"):row["status"]="passed"
            row["memory_seen"]=True
        group[key]=row;store.room13=n
        return True

    def r13_visit147_memory_phase(key):
        state=r13_visit147_state(key);result=state.get("result")
        if result in ("help","watch","decline"):return "memory_"+result
        return "noticed" if state.get("intro_seen") is True or state.get("status")=="noticed" else "passed"

    def r13_visit147_lines(key,phase):
        spec=R13_VISITS147.get(key)
        if not spec:return []
        companion=globals().get("r13_v111_resident_companion_ok",lambda person:False)("daram")
        rows=[]
        for original in spec["blocks"].get(phase,[]):
            if original.get("companion") and not companion:continue
            row=winter_copy.deepcopy(original);row.pop("companion",None)
            rows.append(r13_nw_added_line(row))
        return rows

    def r13_visit147_pending_here():
        return [dict(event=key,title=spec["title"],person=spec["owner"],notice=spec["notice"])
                for key,spec in R13_VISITS147.items() if r13_visit147_source_allowed(key)]

    def r13_visit147_notice():
        pending=r13_visit147_pending_here()
        return pending[0]["notice"] if pending else None

    def r13_visit147_priority_people():
        # 일과·현재 표시를 조회하지 않아 배치 선택과 서로 재귀하지 않는다.
        s=store.room13 or {};day=s.get("day",1);period=s.get("period",0)
        if not 2<=day<=7:return []
        people=[]
        for key,spec in R13_VISITS147.items():
            if key=="sleeve" and r13_sidequest_status("seam")!="unseen":continue
            if day==2 and period in spec["source_periods"] and r13_visit147_state(key).get("status","unseen") in ("unseen","noticed"):
                people.extend(spec["members"])
            elif day>2 or period>=2:people.append(spec["owner"])
        return list(dict.fromkeys(people))

    _r13_visit147_population=r13_population146_side_people
    def r13_population146_side_people():
        return set(_r13_visit147_population())|set(r13_visit147_priority_people())

    _r13_visit147_quest_actions=r13_sidequest_person_actions
    def r13_sidequest_person_actions(person):
        rows=_r13_visit147_quest_actions(person)
        if person=="resident_yeoni" and r13_visit147_source_allowed("sleeve"):
            return [row for row in rows if not (row["quest"]=="seam" and row["action"]=="offer")]
        return rows

    _r13_visit147_quest_lines=r13_sidequest_lines
    def r13_sidequest_lines(key,phase):
        if key=="seam" and phase=="offer" and r13_visit147_state("sleeve").get("status")=="completed":
            return r13_visit147_lines("sleeve","quest_offer")
        return _r13_visit147_quest_lines(key,phase)

    _r13_visit147_questions=r13_v111_questions
    def r13_v111_questions(person):
        rows=list(_r13_visit147_questions(person));split=next((i for i,row in enumerate(rows)
            if isinstance(getattr(row[1],"value",None),(tuple,list)) and bool(getattr(row[1],"value",None)) and getattr(row[1],"value",None)[0] in ("resident_chat","sidequest")),len(rows))
        visits=[(row["title"],Return(("village_visit",(row["event"],row["action"]))),row["read"]) for row in r13_visit147_person_actions(person)]
        return rows[:split]+visits+rows[split:]

    _r13_visit147_business=r13_v111_has_business
    def r13_v111_has_business(person):
        return bool(r13_visit147_person_actions(person)) or _r13_visit147_business(person)

label r13_visit147_dispatch(event,action):
    if not r13_visit147_allowed(event,action):
        return False
    if action=="visit":
        call r13_lines(r13_visit147_lines(event,'intro'),'village147:'+event+':intro')
        $ r13_visit147_record(event,'noticed')
        if not r13_visit147_allowed(event,'visit'):
            return False
        $ visit147_choices=[(choice['title'],choice['result']) for choice in R13_VISITS147[event]['choices']]
        $ visit147_result=renpy.display_menu(visit147_choices)
        if visit147_result not in ('help','watch','decline') or not r13_visit147_allowed(event,'visit'):
            return False
        call r13_lines(r13_visit147_lines(event,visit147_result),'village147:'+event+':'+visit147_result)
        $ r13_visit147_record(event,'complete',visit147_result)
    elif action=="memory":
        $ visit147_phase=r13_visit147_memory_phase(event)
        call r13_lines(r13_visit147_lines(event,visit147_phase),'village147:'+event+':'+visit147_phase)
        $ r13_visit147_record(event,'memory')
    return True
