# 선택 생활 의뢰: 본편의 증거·판정·시간 값과 분리된 저장 상태를 쓴다.
init 362 python:
    from collections.abc import Mapping as R13SidequestMapping
    with renpy.file("v111/sidequests146.json") as _sq_file:
        R13_SIDEQUESTS=json.load(_sq_file)["quests"]
    R13_SIDEQUEST_PUBLIC_PLACES=frozenset(("inn","square","post","workshop","clinic","school","hall","dining"))
    for _sq_id,_sq in R13_SIDEQUESTS.items():
        _sq_label="r13_sq146_"+_sq_id
        R13_EVENT_OFFERS[_sq_label]=(_sq["title"],[],"")
        R13_OFFER_ACTORS[_sq_label]=(_sq["owner"],None)

    def r13_sidequest_problems():
        problems=[];ids=set()
        for key,spec in R13_SIDEQUESTS.items():
            if spec.get("work_place") not in R13_SIDEQUEST_PUBLIC_PLACES:problems.append(key+": 비공개 작업 장소")
            if spec.get("object") not in ROOM13["objects"].get(spec.get("work_place"),{}):problems.append(key+": 없는 조사 물건")
            if spec.get("owner") not in CAST:problems.append(key+": 없는 주민")
            if not spec.get("choices") or len({c.get("result") for c in spec["choices"]})!=len(spec["choices"]):problems.append(key+": 작업 방식 중복")
            needed={"offer","accept","decline","defer","reminder","done","passed"}
            needed.update("work_"+c["result"] for c in spec.get("choices",[]))
            needed.update("report_"+c["result"] for c in spec.get("choices",[]))
            if not needed<=set(spec.get("blocks",{})):problems.append(key+": 대화 단계 누락")
            for phase,rows in spec.get("blocks",{}).items():
                for row in rows:
                    if row.get("id") in ids:problems.append(key+": 중복 대사 ID")
                    ids.add(row.get("id"))
                    if row.get("speaker") not in (None,"아빠",spec.get("owner_name")):problems.append(key+": 부재 인물 발화")
                    if row.get("speaker") is not None and row["speaker"] not in MS14_SPEAKERS:problems.append(key+": 화자 연결 누락")
                    if not row.get("text") or row.get("kind") not in ("dialogue","narration"):problems.append(key+": 대사 형식")
        return problems
    if r13_sidequest_problems():raise Exception("생활 의뢰 등록 오류: "+"; ".join(r13_sidequest_problems()))

    def r13_sidequest_state(key):
        values=(store.room13 or {}).get("v111",{}).get("sidequests",{})
        row=values.get(key,{}) if isinstance(values,R13SidequestMapping) else {}
        return winter_copy.deepcopy(dict(row)) if isinstance(row,R13SidequestMapping) else {}

    def r13_sidequest_status(key):
        return r13_sidequest_state(key).get("status","unseen")

    def r13_sidequest_calm():
        s=store.room13 or {};v=s.get("v111") or {}
        if not r13_v111_active() or not 2<=s.get("day",1)<=7:return False
        group=v.get("sidequests",{})
        if not isinstance(group,R13SidequestMapping) or any(not isinstance(row,R13SidequestMapping) for row in group.values()):return False
        if v.get("gate")=="travel" or s.get("location")=="v111_fire":return False
        if r13_v111_tense_context() or any(getattr(store,k,False) for k in
                ("r13_meeting_active","r13_meeting_live_active","r13_cg_active","r13_aftermath_active","r13_ending_story_active")):return False
        if r13_v111_value("DARAM_DETAINED") or s.get("case_state")=="occurred":return False
        return globals().get("r13_v111_revisit_allowed",lambda:False)()

    def r13_sidequest_person_ready(key):
        spec=R13_SIDEQUESTS.get(key)
        return bool(spec and r13_sidequest_calm() and r13_v111_person_alive(spec["owner"])
                    and not r13_v111_value("departed:"+spec["owner"]) and not r13_v111_value("busy:"+spec["owner"])
                    and r13_v111_actor_ready(spec["owner"]) and spec["owner"] in r13_visible_people())

    def r13_sidequest_person_actions(person):
        rows=[];day=store.room13.get("day",1)
        for key,spec in R13_SIDEQUESTS.items():
            if spec["owner"]!=person or not r13_sidequest_person_ready(key):continue
            state=r13_sidequest_state(key);status=state.get("status","unseen")
            if status in ("unseen","declined","deferred") and spec["offer_days"][0]<=day<=spec["offer_days"][-1]:
                rows.append(dict(quest=key,action="offer",title=spec["offer_title"],read=False))
            elif status=="accepted":rows.append(dict(quest=key,action="status",title=spec.get("status_title","어디부터 손대면 될까요?"),read=bool(state.get("reminder_seen"))))
            elif status=="worked":rows.append(dict(quest=key,action="report",title=spec.get("report_title","부탁하신 일을 마쳤습니다."),read=False))
            elif status=="done":rows.append(dict(quest=key,action="done",title=spec.get("done_title","그 뒤로 좀 괜찮으세요?"),read=True))
            elif status in ("declined","deferred","passed") and day>spec["offer_days"][-1]:
                rows.append(dict(quest=key,action="close",title=spec.get("close_title","그때 부탁하신 일은 어떻게 됐습니까?"),read=status=="passed"))
        return rows

    def r13_sidequest_object_actions(key):
        if not r13_sidequest_calm():return []
        here=store.room13["location"]
        # 수사에서 쓰는 같은 물건은 본편의 원래 선택이 우선한다.
        if any(o.get("object")==key and o.get("location")==here for o in r13_v111_binding().get("options",[])):return []
        rows=[]
        for quest,spec in R13_SIDEQUESTS.items():
            if spec["object"]!=key or spec["work_place"]!=here or r13_sidequest_status(quest)!="accepted":continue
            if not r13_v111_person_alive(spec["owner"]) or r13_v111_value("departed:"+spec["owner"]) or r13_v111_value("busy:"+spec["owner"]):continue
            rows.append(dict(quest=quest,action="work",title=spec["work_title"],message=spec["work_message"]))
        return rows

    def r13_sidequest_allowed(key,action):
        if key not in R13_SIDEQUESTS:return False
        if action=="work":return any(r["quest"]==key for r in r13_sidequest_object_actions(R13_SIDEQUESTS[key]["object"]))
        return any(r["quest"]==key and r["action"]==action for r in r13_sidequest_person_actions(R13_SIDEQUESTS[key]["owner"]))

    def r13_sidequest_update(key,action,result=None):
        if key not in R13_SIDEQUESTS:return False
        check="offer" if action in ("accept","decline","defer") else action
        if not r13_sidequest_allowed(key,check):return False
        if action=="work" and result not in {c["result"] for c in R13_SIDEQUESTS[key]["choices"]}:return False
        states={"accept":"accepted","decline":"declined","defer":"deferred","work":"worked","report":"done","close":"passed"}
        if action not in states and action!="status":return False
        n=winter_copy.deepcopy(store.room13);group=n["v111"].setdefault("sidequests",{})
        row=dict(group.get(key,{}));row["status"]=states.get(action,row.get("status","accepted"))
        if action=="accept":row.update(accepted_day=n["day"],accepted_period=n["period"])
        if action=="work":row.update(result=result,work_day=n["day"],work_period=n["period"])
        if action=="report":row.update(completed_day=n["day"],completed_period=n["period"])
        if action=="status":row["reminder_seen"]=True
        group[key]=row;store.room13=n
        return True

    def r13_sidequest_lines(key,phase):
        spec=R13_SIDEQUESTS.get(key)
        if not spec:return []
        if key=="seam" and phase=="done" and r13_sidequest_state(key).get("result")=="tight":phase="done_tight"
        return [r13_nw_added_line(winter_copy.deepcopy(row)) for row in spec["blocks"].get(phase,[])]

    def r13_sidequest_priority_people():
        # 배치 필터에서 사용한다. 여기서는 일과·표시·물리 재실 조회를 호출하지 않는다.
        return [spec["owner"] for key,spec in R13_SIDEQUESTS.items() if r13_sidequest_status(key) in ("accepted","worked")]

    def r13_sidequest_song_lines():
        return [spec["song"] for key,spec in R13_SIDEQUESTS.items() if r13_sidequest_status(key)=="done"]

    def r13_sidequest_tasks():
        rows=[]
        for key,spec in R13_SIDEQUESTS.items():
            status=r13_sidequest_status(key)
            if status=="unseen":continue
            place=spec["work_place"] if status=="accepted" else r13_where(spec["owner"]) if status=="worked" else None
            objective=spec["objective"] if status=="accepted" else spec["owner_name"]+"에게 한 일을 보여 준다." if status=="worked" else "도움을 마쳤다." if status=="done" else "주민이 직접 마무리했다." if status=="passed" else "다시 말을 걸어 도울 수 있다." if store.room13.get("day",1)<=spec["offer_days"][-1] else "주민에게 그 뒤 일을 물어볼 수 있다."
            rows.append(dict(id=key,title=spec["title"],status=status,objective=objective,place=place))
        return rows

    def r13_sidequest_places():
        if not r13_sidequest_calm():return []
        places=[]
        for key,spec in R13_SIDEQUESTS.items():
            status=r13_sidequest_status(key)
            if status not in ("accepted","worked"):continue
            if not r13_v111_person_alive(spec["owner"]) or r13_v111_value("departed:"+spec["owner"]):continue
            target=spec["work_place"] if status=="accepted" else r13_where(spec["owner"])
            if target in R13_SIDEQUEST_PUBLIC_PLACES:places.append(target)
        return list(dict.fromkeys(places))

    _r13_sidequest_places=r13_places
    def r13_places():
        return list(dict.fromkeys(_r13_sidequest_places()+r13_sidequest_places()))

    _r13_sidequest_questions=r13_v111_questions
    def r13_v111_questions(person):
        formal=[];personal=[]
        for row in _r13_sidequest_questions(person):
            payload=getattr(row[1],"value",None)
            target=personal if isinstance(payload,(tuple,list)) and payload and payload[0]=="resident_chat" else formal
            target.append(row)
        quests=[(row["title"],Return(("sidequest",(row["quest"],row["action"]))),row["read"]) for row in r13_sidequest_person_actions(person)]
        return formal+quests+personal

    _r13_sidequest_business=r13_v111_has_business
    def r13_v111_has_business(person):
        return bool(r13_sidequest_person_actions(person)) or _r13_sidequest_business(person)

label r13_sidequest_dispatch(quest,action):
    if not r13_sidequest_allowed(quest,action):
        return False
    if action=="offer":
        call r13_lines(r13_sidequest_lines(quest,'offer'),'sidequest:'+quest+':offer')
        $ sq146_spec=R13_SIDEQUESTS[quest]
        $ sq146_choice=renpy.display_menu([(sq146_spec['accept_title'],'accept'),(sq146_spec['decline_title'],'decline'),(sq146_spec['defer_title'],'defer')])
        $ sq146_choice=sq146_choice if sq146_choice in ('accept','decline','defer') else 'defer'
        if r13_sidequest_update(quest,sq146_choice):
            call r13_lines(r13_sidequest_lines(quest,sq146_choice),'sidequest:'+quest+':'+sq146_choice)
    elif action=="report":
        $ sq146_phase='report_'+r13_sidequest_state(quest).get('result','')
        call r13_lines(r13_sidequest_lines(quest,sq146_phase),'sidequest:'+quest+':'+sq146_phase)
        $ r13_sidequest_update(quest,'report')
    elif action=="status":
        call r13_lines(r13_sidequest_lines(quest,'reminder'),'sidequest:'+quest+':reminder')
        $ r13_sidequest_update(quest,'status')
    elif action=="done":
        call r13_lines(r13_sidequest_lines(quest,'done'),'sidequest:'+quest+':done')
    elif action=="close":
        call r13_lines(r13_sidequest_lines(quest,'passed'),'sidequest:'+quest+':passed')
        if r13_sidequest_status(quest)!='passed':
            $ r13_sidequest_update(quest,'close')
    return True

label r13_sidequest_object_menu(key):
    $ sq146_options=r13_sidequest_object_actions(key)
    if not sq146_options:
        return False
    $ sq146_action=sq146_options[0]
    call screen r13_confirm(sq146_action['message'],sq146_action['title'],'그냥 살펴본다')
    if not _return:
        return False
    $ sq146_quest=sq146_action['quest']
    if not r13_sidequest_allowed(sq146_quest,'work'):
        return False
    $ sq146_choices=[(choice['title'],choice['result']) for choice in R13_SIDEQUESTS[sq146_quest]['choices']]
    $ sq146_method=renpy.display_menu(sq146_choices)
    if r13_sidequest_update(sq146_quest,'work',sq146_method):
        call r13_lines(r13_sidequest_lines(sq146_quest,'work_'+sq146_method),'sidequest:'+sq146_quest+':work:'+sq146_method)
        return True
    return False

label r13_sq146_seam:
    call r13_sidequest_dispatch('seam','offer')
    return

label r13_sq146_notice:
    call r13_sidequest_dispatch('notice','offer')
    return

label r13_sq146_parts:
    call r13_sidequest_dispatch('parts','offer')
    return
