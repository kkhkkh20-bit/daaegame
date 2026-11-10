# 소설의 생활 장면을 현장 관찰 → 질문 → 선택 행동 → 기억으로 잇는다.
init 387 python:
    from collections.abc import Mapping as R13World148Mapping
    with renpy.file("v111/world-inquiries148.json") as _world148_file:
        R13_WORLD148=json.load(_world148_file)["threads"]

    def r13_world148_problems():
        problems=[];ids=set()
        for key,spec in R13_WORLD148.items():
            if spec.get("owner") not in CAST:problems.append(key+": 없는 주민")
            if set(c.get("result") for c in spec.get("choices",[]))!={"help","listen","later"}:problems.append(key+": 선택 결과 누락")
            for point in spec.get("sources",[])+[spec.get("task",{})]:
                if point.get("object") not in ROOM13["objects"].get(point.get("location"),{}):problems.append(key+": 없는 조사 물건")
            phases={"intro","help","listen","action","memory_help","memory_listen","reinspect_help","reinspect_listen"}
            if not phases<=set(spec.get("blocks",{})):problems.append(key+": 대화 단계 누락")
            blocks=list(spec.get("blocks",{}).values())+[s.get("observation",[]) for s in spec.get("sources",[])]
            blocks += [rows for variant in spec.get("variants",{}).values() for rows in variant.values()]
            for rows in blocks:
                for row in rows:
                    if not row.get("id") or row["id"] in ids:problems.append(key+": 대사 ID 중복 또는 누락")
                    ids.add(row.get("id"))
                    if not row.get("text") or row.get("kind") not in ("dialogue","narration"):problems.append(key+": 대사 형식")
                    if row.get("speaker") not in (None,"아빠","다람",spec["owner_name"]):problems.append(key+": 부재 인물 발화")
                    if row.get("speaker")=="다람" and not row.get("companion"):problems.append(key+": 동행 조건 누락")
            if any(row.get("speaker") not in {None,"아빠","다람"} for row in spec["blocks"].get("action",[])):problems.append(key+": 현장에 없는 주민의 작업 발화")
        return problems
    if r13_world148_problems():raise Exception("마을 조사 등록 오류: "+"; ".join(r13_world148_problems()))

    def r13_world148_state(key):
        group=((store.room13 or {}).get("v111") or {}).get("world148",{})
        row=group.get(key,{}) if isinstance(group,R13World148Mapping) else {}
        return winter_copy.deepcopy(dict(row)) if isinstance(row,R13World148Mapping) else {}

    def r13_world148_variants(key):
        variants=[]
        owner=R13_WORLD148[key]["owner"]
        if r13_v111_owned("E09"):
            if r13_v111_value("piko_alive") is False and r13_v111_value("piko_news3:"+owner):variants.append("piko_dead")
            elif r13_v111_value("piko_alive") is True:variants.append("piko_safe")
        meeting=r13_v111_value("meeting:lamp")
        if meeting in ("win","partial","lose"):
            # 혐의를 벗겼다는 말은 실제 명단 처리까지 일치할 때만 쓴다.
            if meeting=="lose" or r13_v111_value("listed:resident_tok") is not True:variants.append("lamp_"+meeting)
        if (r13_v111_value("D06_S03P_empty_fire_completed") is True
                and r13_v111_value("warehouse_children_school_handover")==4
                and r13_v111_value("KKOMI_ALIVE") is True):variants.append("fire_safe")
        elif (r13_v111_value("D06_S03_main_completed") is True
                and r13_v111_value("warehouse_children_rescued")==3
                and r13_v111_value("KKOMI_ALIVE") is False):variants.append("fire_lost")
        return variants

    def r13_world148_calm():
        group=((store.room13 or {}).get("v111") or {}).get("world148",{})
        return bool(isinstance(group,R13World148Mapping)
                    and all(isinstance(row,R13World148Mapping) for row in group.values())
                    and r13_sidequest_calm())

    def r13_world148_window(key):
        spec=R13_WORLD148.get(key);s=store.room13 or {}
        if not spec or not spec["days"][0]<=s.get("day",1)<=spec["days"][-1] or not r13_world148_calm():return False
        return key!="aftermath" or any(v in r13_world148_variants(key) for v in ("fire_safe","fire_lost"))

    def r13_world148_object_free(obj):
        here=store.room13.get("location")
        return not any(o.get("object")==obj and o.get("location")==here for o in r13_v111_binding().get("options",[]))

    def r13_world148_source_allowed(key,obj):
        if not r13_world148_window(key) or not r13_world148_object_free(obj):return False
        return any(source["location"]==store.room13.get("location") and source["object"]==obj for source in R13_WORLD148[key]["sources"])

    def r13_world148_ready(key):
        spec=R13_WORLD148.get(key)
        if not spec or not r13_world148_window(key):return False
        person=spec["owner"]
        # 일과 이동에는 지난 장면의 location 값보다 현행 배치 계약을 따른다.
        return bool(person in r13_visible_people() and r13_v111_actor_ready(person)
                    and r13_v111_person_alive(person) and not r13_v111_value("busy:"+person)
                    and not r13_v111_value("departed:"+person))

    def r13_world148_known(key):
        needed={"postal":"E07","seat":"E09","tools":"E12"}.get(key)
        if needed and not r13_v111_owned(needed):return False
        # 초상 보유만으로 사망 소식을 이미 나눈 것으로 취급하지 않는다.
        if key=="seat" and r13_v111_value("piko_alive") not in (True,False):return False
        if key=="seat" and r13_v111_value("piko_alive") is False:
            return bool(r13_v111_value("piko_news3:"+R13_WORLD148[key]["owner"]))
        return True

    def r13_world148_person_actions(person):
        rows=[];s=store.room13 or {}
        for key,spec in R13_WORLD148.items():
            if spec["owner"]!=person or not r13_world148_ready(key) or not r13_world148_known(key):continue
            state=r13_world148_state(key)
            if not state.get("observed"):continue
            if not state.get("result"):
                rows.append(dict(thread=key,action="ask",title=spec["question"],read=False))
            elif state.get("result")=="help" and not state.get("worked"):
                rows.append(dict(thread=key,action="reminder",title=spec["question"],read=True))
            elif (state.get("worked") and not state.get("report_seen")) or (s.get("day",1),s.get("period",0))>tuple(state.get("last_time",[0,0])):
                stamp="%s:%s:%s"%(s.get("day"),s.get("period"),",".join(r13_world148_variants(key)))
                rows.append(dict(thread=key,action="memory",title=spec["question"],read=state.get("memory_stamp")==stamp))
        return rows

    def r13_world148_object_actions(obj):
        rows=[];here=store.room13.get("location")
        for key,spec in R13_WORLD148.items():
            if not r13_world148_window(key) or not r13_world148_object_free(obj):continue
            state=r13_world148_state(key);task=spec["task"]
            if (state.get("result")=="help" and not state.get("worked")
                    and task["location"]==here and task["object"]==obj):
                # 수락으로 완료하지 않고 현장 물건을 다시 선택했을 때 확인한다.
                rows.append(dict(thread=key,action="work",title=task["title"]))
            elif r13_world148_source_allowed(key,obj):
                rows.append(dict(thread=key,action="observe",title=spec["title"]))
        return rows

    def r13_world148_allowed(key,action):
        if key not in R13_WORLD148:return False
        if action in ("observe","work"):
            return any(row["thread"]==key and row["action"]==action for row in r13_world148_object_actions_current())
        return any(row["thread"]==key and row["action"]==action for row in r13_world148_person_actions(R13_WORLD148[key]["owner"]))

    def r13_world148_object_actions_current():
        return [row for obj in ROOM13["objects"].get(store.room13.get("location"),{}) for row in r13_world148_object_actions(obj)]

    def r13_world148_record(key,action,result=None):
        check="ask" if action=="choose" else action
        if not r13_world148_allowed(key,check):return False
        if action=="choose" and result not in ("help","listen"):return False
        if action not in ("observe","choose","work","memory"):return False
        n=winter_copy.deepcopy(store.room13);group=n["v111"].setdefault("world148",{});row=dict(group.get(key,{}))
        now=[n["day"],n["period"]]
        if action=="observe":
            if not row.get("observed"):
                source=next(source for source in R13_WORLD148[key]["sources"] if source["location"]==n["location"])
                row.update(observed=True,observed_time=now,source_place=n["location"],observed_fact=source["fact"])
        elif action=="choose":row.update(result=result,asked_time=now,last_time=now,heard_variants=r13_world148_variants(key))
        elif action=="work":row.update(worked=True,worked_time=now,last_time=now)
        else:
            row["memory_stamp"]="%s:%s:%s"%(n["day"],n["period"],",".join(r13_world148_variants(key)))
            if row.get("worked"):row["report_seen"]=True
        group[key]=row;store.room13=n
        return True

    def r13_world148_block(key,phase):
        spec=R13_WORLD148[key];rows=spec["blocks"].get(phase,[])
        for variant in r13_world148_variants(key):rows=spec.get("variants",{}).get(variant,{}).get(phase,rows)
        return rows

    def r13_world148_lines(key,phase):
        if phase=="observation":
            rows=next((source["observation"] for source in R13_WORLD148[key]["sources"] if source["location"]==store.room13.get("location")),[])
        else:rows=r13_world148_block(key,phase)
        companion=r13_v111_resident_companion_ok("daram")
        return [r13_nw_added_line({k:v for k,v in row.items() if k!="companion"}) for row in rows if not row.get("companion") or companion]

    def r13_world148_journal():
        rows=[]
        for key,spec in R13_WORLD148.items():
            state=r13_world148_state(key)
            if not state.get("observed"):continue
            result=state.get("result");task=spec["task"]
            status="현장에서 본 것" if not result else ("도울 차례" if result=="help" and not state.get("worked") else "들은 이야기")
            fact=state.get("observed_fact","")
            if state.get("worked"):fact=spec["facts"]["helped"]
            elif result=="listen":fact=spec["facts"]["learned"]
            when=state.get("worked_time",state.get("asked_time",state["observed_time"]))
            source=(spec["owner_name"]+"에게 들음") if result=="listen" else (R13_PLACES.get(state.get("source_place"),(state.get("source_place"),))[0]+"에서 관찰")
            if state.get("worked"):status="직접 해본 일";source="직접 확인 · "+spec["owner_name"]
            next_step=("이 이야기를 기록해 두었습니다." if store.room13.get("day")==7 else "다음에 "+spec["owner_name"]+"에게 안부를 물을 수 있습니다.") if result else (spec["owner_name"]+"에게 물어볼 수 있습니다.")
            if not result and not r13_world148_known(key):next_step="관찰한 내용을 남겨 두었습니다."
            if state.get("worked") and not state.get("report_seen"):next_step=spec["owner_name"]+"에게 한 일을 알려줄 수 있습니다."
            if result=="help" and not state.get("worked"):next_step=R13_PLACES.get(task["location"],(task["location"],))[0]+" · "+task["title"]
            rows.append(dict(title=spec["title"],status=status,fact=fact,source="%d일 · %s"%(when[0],source),objective=next_step))
        return rows

    _r13_world148_questions=r13_v111_questions
    def r13_v111_questions(person):
        rows=list(_r13_world148_questions(person));split=next((i for i,row in enumerate(rows)
            if isinstance(getattr(row[1],"value",None),(tuple,list)) and getattr(row[1],"value",None)
            and getattr(row[1],"value",None)[0] in ("resident_chat","sidequest","village_visit")),len(rows))
        topics=[(row["title"],Return(("world148",(row["thread"],row["action"]))),row["read"]) for row in r13_world148_person_actions(person)]
        return rows[:split]+topics+rows[split:]

    _r13_world148_business=r13_v111_has_business
    def r13_v111_has_business(person):
        return bool(r13_world148_person_actions(person)) or _r13_world148_business(person)

    _r13_world148_priority=r13_population146_side_people
    def r13_population146_side_people():
        # 배치 함수에서 재실 조회를 부르면 재귀하므로 저장된 관찰만 조회한다.
        s=store.room13 or {};day=s.get("day",1)
        return set(_r13_world148_priority())|{spec["owner"] for key,spec in R13_WORLD148.items()
            if spec["days"][0]<=day<=spec["days"][-1] and r13_world148_state(key).get("observed")}

label r13_world148_dispatch(thread,action):
    if not r13_world148_allowed(thread,action):
        return False
    if action=="ask":
        call r13_lines(r13_world148_lines(thread,'intro'),'world148:'+thread+':intro')
        $ world148_result=renpy.display_menu([(choice['title'],choice['result']) for choice in R13_WORLD148[thread]['choices']])
        if world148_result not in ('help','listen') or not r13_world148_allowed(thread,'ask'):
            return False
        call r13_lines(r13_world148_lines(thread,world148_result),'world148:'+thread+':'+world148_result)
        $ r13_world148_record(thread,'choose',world148_result)
    elif action=="reminder":
        $ renpy.notify(R13_WORLD148[thread]['task']['message'])
    elif action=="memory":
        $ world148_phase='memory_help' if r13_world148_state(thread).get('worked') else 'memory_listen'
        call r13_lines(r13_world148_lines(thread,world148_phase),'world148:'+thread+':'+world148_phase)
        $ r13_world148_record(thread,'memory')
    return True

label r13_world148_object(key):
    $ world148_actions=r13_world148_object_actions(key)
    if not world148_actions:
        return False
    if len(world148_actions)>1:
        $ world148_selected=renpy.display_menu([(row['title'],row['thread']) for row in world148_actions]+[('현장으로 돌아간다',None)])
    else:
        $ world148_selected=world148_actions[0]['thread']
    $ world148_entry=next((row for row in world148_actions if row['thread']==world148_selected),None)
    if not world148_entry or not r13_world148_allowed(world148_selected,world148_entry['action']):
        return True
    if world148_entry['action']=='work':
        call screen r13_confirm(R13_WORLD148[world148_selected]['task']['message'],R13_WORLD148[world148_selected]['task']['title'],'나중에 하기')
        if _return and r13_world148_allowed(world148_selected,'work'):
            call r13_lines(r13_world148_lines(world148_selected,'action'),'world148:'+world148_selected+':action')
            $ r13_world148_record(world148_selected,'work')
    else:
        $ world148_state=r13_world148_state(world148_selected)
        $ world148_phase=('reinspect_help' if world148_state.get('worked') else 'reinspect_listen') if world148_state.get('result') else 'observation'
        $ r13_field_reading=True
        call r13_lines(r13_world148_lines(world148_selected,world148_phase),'world148:'+world148_selected+':'+world148_phase)
        $ r13_field_reading=False
        $ r13_world148_record(world148_selected,'observe')
        if not world148_state.get('observed'):
            $ renpy.notify((R13_WORLD148[world148_selected]['owner_name']+'에게 물어볼 말이 생겼습니다.' if r13_world148_known(world148_selected) else '관찰한 내용을 기록했습니다.')+' 상단 마을일에서 다시 볼 수 있습니다.')
    return True
