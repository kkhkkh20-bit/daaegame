# 데이터 조회 전수 검사와 GUI 재생 검사를 분리한다. 이 파일은 공개 빌드에 포함하지 않는다.
init python:
    QA146_PUBLIC=("gate","square","inn","hall","dining","post","workshop","clinic","school")
    QA146_DAILY_SCENES={1:"MS14_D01_S05",2:"MS14_D02_S04",3:"MS14_D03_S06",4:"MS14_D04_S01",
                        5:"MS14_D05_S01",6:"MS14_D06_S01",7:"MS14_D07_S03"}
    QA146_ACTIVE_FIELDS=("r13_life_field_active","r13_v111_talk_person","r13_meeting_active",
        "r13_meeting_live_active","r13_cg_active","r13_aftermath_active","r13_ending_story_active")

    def qa146_save_context():
        return (winter_copy.deepcopy(store.room13),{k:getattr(store,k,None) for k in QA146_ACTIVE_FIELDS})

    def qa146_restore_context(saved):
        store.room13=saved[0]
        for key,value in saved[1].items():setattr(store,key,value)

    def qa146_output(name,data):
        import os
        folder=os.path.join(os.environ.get("ROOM13_QA_OUT","/tmp/room13-qa"),"runtime146")
        os.makedirs(folder,exist_ok=True)
        with open(os.path.join(folder,name),"w",encoding="utf-8") as stream:
            json.dump(data,stream,ensure_ascii=False,indent=2,default=str)

    def qa146_begin():
        renpy.test.runtime146_base=winter_copy.deepcopy(store.room13)
        renpy.test.runtime146_report=dict(
            scope="실제 SDK 초기화 함수를 사용하는 준비 상태 조회. 자연 플레이 도달성 또는 모든 GUI 클릭의 증거가 아님.",
            daily_policy="피코 생존 가능 경로의 일상 행렬. 1~7일×3시간대×9공개 장소. 미방문 장소도 직접 준비했으므로 이동 해금 증거가 아님.",
            semantic_limit="원문과 조건을 기록한다. 인물의 지식·감정·문장 자연스러움은 별도 독립 문안 검토를 따른다.",
            states=[],issues=[],diagnostics=[])

    def qa146_prepare(day,period,place,gate="qa_daily146",scene=None,values=None,flags=None,evidence=None,people=None):
        n=winter_copy.deepcopy(renpy.test.runtime146_base)
        n.update(day=day,period=period,location=place,case_state="pending",daram_state="with_dad")
        n["evidence"]=[]
        n["flags"]=["entry_corrected","lodging"]
        n["arguments"]={}
        n["v111"]=dict(values=winter_copy.deepcopy(R13_V111["initial"]),people=list(people or ()),
                        gate=gate,scene=scene or QA146_DAILY_SCENES[day],visited_places=[place])
        n["v111"]["values"].update(day=day,gate_registered=True,DARAM_DETAINED=False,OWL_ALIVE=True,
                                  piko_alive=True,**{"location:daram":place})
        if day==7:
            n["v111"]["values"].update(FIRE_EVACUATED=True,D06_S03P_empty_fire_completed=True,
                                      warehouse_children_school_handover=4)
            n["evidence"].append("V111:E06_FIRE")
        n["v111"]["values"].update(values or {})
        n["flags"].extend(flags or ())
        n["evidence"].extend("V111:"+k if not k.startswith("V111:") else k for k in (evidence or ()))
        store.room13=n
        store.r13_v111_talk_person=None
        store.r13_life_field_active=True
        for field in ("r13_meeting_active","r13_meeting_live_active","r13_cg_active",
                      "r13_aftermath_active","r13_ending_story_active"):
            setattr(store,field,False)

    def qa146_read_choice(person,entry):
        caption,action,read=entry
        value=getattr(action,"value",None)
        row=dict(title=caption,value=value,read=bool(read),packets=[],mode="ui_or_main_action")
        if isinstance(value,(tuple,list)) and len(value)==2:
            if value[0]=="resident_chat":
                row["mode"]="resident_chat"
                row["packets"]=r13_v111_resident_chat_lines(value[1])
                if value[1]=="hyeoni:song":
                    row["mode"]="existing_song_label"
                    row["packets"]=[("resident_hyeoni",verse) for verse in r13_hyeoni_verses()]
            elif value[0]=="followup":
                row["mode"]="followup_query_without_read_write"
                spec=next((r for r in R13_REACTIONS.get("followups",()) if r["id"]==value[1]),None)
                if spec:row["packets"]=r13_reaction_packets(r13_v111_followup_display(spec)["lines"])
            elif value[0]=="sidequest":
                row["mode"]="sidequest_action_not_executed"
        return row

    def qa146_pan_probe():
        """준비된 카메라 양끝에서 같은 무대 좌표인지 조회한다. 실제 팬 클릭 검사가 아니다."""
        saved=winter_copy.deepcopy(store.r13_world_cameras);place=store.room13["location"];out=[]
        try:
            for offset in (0,r13_camera_range(place)):
                cameras=dict(saved);cameras[place]=offset;store.r13_world_cameras=cameras
                actors=[dict(person=a["person"],rect=list(a.get("rect",()))) for a in r13_stage_people()]
                out.append(dict(offset=offset,visible=list(r13_visible_people()),actors=actors))
            return out
        finally:
            store.r13_world_cameras=saved

    def qa146_capture(tag,kind="daily"):
        report=renpy.test.runtime146_report
        current=store.room13
        row=dict(tag=tag,kind=kind,day=current["day"],period=current["period"],location=current["location"],
                 scene=current["v111"].get("scene"),gate=current["v111"].get("gate"),
                 values=winter_copy.deepcopy(current["v111"]["values"]),people=[],objects=[],issues=[])
        before=winter_copy.deepcopy(current)
        def issue(code,detail,hard=True):
            item=dict(tag=tag,code=code,detail=detail)
            row["issues"].append(item)
            report["issues" if hard else "diagnostics"].append(item)
        try:
            people=list(r13_visible_people())
            row["visible"]=people
            if len(people)!=len(set(people)):issue("duplicate_person",people)
            if tag=="routine_old_cast_location_history":
                row["prepared_camera_endpoints"]=qa146_pan_probe()
                left,right=row["prepared_camera_endpoints"]
                if left["visible"]!=right["visible"] or left["actors"]!=right["actors"]:
                    issue("camera_changed_resident_world_position",row["prepared_camera_endpoints"])
                for end in row["prepared_camera_endpoints"]:
                    ids=[a["person"] for a in end["actors"]]
                    if len(ids)!=len(set(ids)):issue("duplicate_actor_in_stage",end)
            if kind=="daily" and r13_population146_active() and len(people)>R13_POPULATION146_LIMIT:
                protected=[p for p in people if current["location"] in r13_population146_needed_places(p)]
                if len(protected)<=R13_POPULATION146_LIMIT:issue("ordinary_population_over_limit",dict(visible=people,protected=protected))
            for person in people:
                qs=list(r13_v111_questions(person))
                detail=dict(person=person,name=R13_NAMES.get(person,person),where=r13_where(person),
                            alive=r13_v111_person_alive(person),actor_ready=r13_v111_actor_ready(person),
                            resident_topic_keys=[q["key"] for q in r13_v111_resident_topics(person)],
                            choices=[qa146_read_choice(person,q) for q in qs])
                row["people"].append(detail)
                if not detail["alive"]:issue("dead_person_visible",person)
                if r13_v111_value("departed:"+person):issue("departed_person_visible",person)
                if (kind=="daily" or tag.startswith("routine_old_cast")) and not detail["actor_ready"]:
                    issue("ordinary_visible_but_not_ready",person)
                if tag=="routine_old_cast_post_relocated" and person in ("doto","resident_owlgp") and not detail["resident_topic_keys"]:
                    issue("relocated_resident_lost_topics",person)
                if not qs:issue("visible_person_without_choice",person,kind not in ("non_hub_boundary_query","invalid_state_stress"))
                for q in detail["choices"]:
                    if not str(q["title"]).strip():issue("empty_choice_title",dict(person=person,value=q["value"]))
                    if q["mode"] in ("resident_chat","existing_song_label","followup_query_without_read_write") and not q["packets"]:
                        issue("empty_dialogue_packets",dict(person=person,value=q["value"]))
                    for packet in q["packets"]:
                        if len(packet)<2 or not str(packet[1]).strip():issue("empty_dialogue_text",dict(person=person,value=q["value"]))
                        elif packet[0]=="dad" and str(packet[1]).strip().strip("()（）").strip() in set(R13_OBJECT_NAMES.values()):
                            issue("dad_object_name_only",dict(person=person,text=packet[1]))
            binding=r13_v111_binding()
            indices=[o["index"] for o in binding.get("options",())]
            row["main_option_indices"]=indices
            raw=R13_V111_BINDINGS.get(current["v111"].get("gate"),{})
            raw_indices=[o.get("index",i) for i,o in enumerate(raw.get("options",()))]
            from collections import Counter
            if raw and Counter(indices)-Counter(raw_indices):issue("main_index_not_in_source",dict(actual=indices,source=sorted(raw_indices)))
            for key,spec in ROOM13["objects"].get(current["location"],{}).items():
                if not r13_object_visible(spec):continue
                matches=[o["index"] for o in binding.get("options",()) if o.get("object")==r13_v111_object_key(key)
                         and o.get("location")==current["location"]]
                text=r13_v111_ambient_text(key,spec)
                obj=dict(key=key,main_indices=matches,ambient=text)
                row["objects"].append(obj)
                if not matches and text and str(text).strip() in (key,r13_object_name(key)):
                    issue("object_name_only_ambient",obj)
            if store.room13!=before:issue("query_changed_story_state",dict(before_day=before["day"],after_day=store.room13["day"]))
        except Exception as error:
            import traceback
            issue("runtime_exception",dict(type=type(error).__name__,message=str(error),trace=traceback.format_exc()))
        report["states"].append(row)
        return row

    def qa146_sweep_day(day):
        saved=qa146_save_context()
        try:
            for period in (0,1,2):
                for place in QA146_PUBLIC:
                    qa146_prepare(day,period,place)
                    qa146_capture("daily:%d:%d:%s"%(day,period,place))
            qa146_output("engine-sweep.json",renpy.test.runtime146_report)
        finally:
            qa146_restore_context(saved)

    def qa146_sweep_branches():
        saved=qa146_save_context()
        try:
            cases=[
                dict(tag="piko_before_discovery_no_hub",day=3,period=0,place="square",gate="piko_clean",scene="MS14_D03_S01",
                     values=dict(piko_alive=True,piko_sheltered=False)),
                dict(tag="piko_after_actual_commit",day=3,period=0,place="square",gate="piko_clean",scene="MS14_D03_S01",
                     values={"piko_alive":False,"portrait":"unfinished","E09.variant":"unfinished"},
                     evidence=["E09"],flags=["piko_dead","v111:applied:MS14_D03_S01_L0021"]),
                dict(tag="piko_false_without_record_stress_not_normal_path",day=3,period=0,place="square",gate="piko_clean",scene="MS14_D03_S01",
                     values=dict(piko_alive=False)),
                dict(tag="evacuated_before_fire",day=6,period=1,place="school",gate="afternoon6",scene="MS14_D06_S02",
                     values=dict(FIRE_EVACUATED=True,warehouse_children_school_handover=4)),
                dict(tag="fire_in_progress",day=6,period=1,place="v111_fire",gate="fire_rescue6",scene="MS14_D06_S03",
                     values=dict(FIRE_EVACUATED=False),people=["resident_bori","kid_kkomi"]),
                dict(tag="fire_after_saved_children",day=6,period=2,place="dining",gate="sleep6_input",scene="MS14_D06_S04",
                     values=dict(FIRE_EVACUATED=True,D06_S03P_empty_fire_completed=True,warehouse_children_school_handover=4),evidence=["E06_FIRE"]),
                dict(tag="fire_after_failed_rescue",day=6,period=2,place="dining",gate="sleep6_input",scene="MS14_D06_S04",
                     values=dict(FIRE_EVACUATED=False,D06_S03_main_completed=True,KKOMI_ALIVE=False),evidence=["E06_FIRE"]),
                dict(tag="detained_boundary_stress_not_public_part1",day=7,period=2,place="room13",gate="detained_bed7",scene="MS14_D07_S04",
                     values=dict(DARAM_DETAINED=True,OWL_ALIVE=False,route7="murder")),
                dict(tag="routine_old_cast_location_history",day=2,period=0,place="square",gate="qa_daily146",scene="MS14_D02_S04",
                     people=list(R13_POPULATION146_ROUTINES),values={"location:"+p:"square" for p in R13_POPULATION146_ROUTINES}),
                dict(tag="routine_old_cast_post_relocated",day=2,period=0,place="post",gate="chorong_documents2",scene="MS14_D02_S01",
                     people=["doto","resident_owlgp"],values={"location:doto":"square","location:resident_owlgp":"square"}),
            ]
            for case in cases:
                tag=case.pop("tag");qa146_prepare(**case)
                kind="non_hub_boundary_query" if tag=="piko_before_discovery_no_hub" else "invalid_state_stress" if "stress" in tag else "prepared_branch"
                qa146_capture(tag,kind)
            # 실제 생사·부재 경계 입력은 선택 원문을 내놓지 않아야 한다.
            for person in ("resident_seol","resident_hyeoni","resident_yeoni","resident_piko"):
                for blocked in ("dead","departed","away"):
                    qa146_prepare(2,0,"square")
                    if blocked=="dead":r13_v111_set("piko_alive" if person=="resident_piko" else "alive:"+person,False)
                    elif blocked=="departed":r13_v111_set("departed:"+person,True)
                    else:
                        r13_v111_set("location:"+person,"clinic");r13_v111_set("busy:"+person,"medical_call")
                    topics=r13_v111_resident_topics(person)
                    if topics:renpy.test.runtime146_report["issues"].append(dict(tag="blocked:%s:%s"%(person,blocked),code="blocked_person_has_resident_topic",detail=topics))
            qa146_output("engine-sweep.json",renpy.test.runtime146_report)
        finally:
            qa146_restore_context(saved)

    def qa146_quest_projection():
        s=store.room13;v=s["v111"]["values"]
        return winter_copy.deepcopy(dict(day=s["day"],period=s["period"],evidence=s.get("evidence"),
            arguments=s.get("arguments"),wallet=s.get("wallet"),case_state=s.get("case_state"),
            story={k:v.get(k) for k in ("piko_alive","gate_registered","OWL_ALIVE","DARAM_DETAINED",
                                       "portrait","FIRE_EVACUATED")}))

    def qa146_gui_checkpoint(quest,phase):
        rows=getattr(renpy.test,"runtime146_gui",[])
        rows.append(dict(quest=quest,expected=phase,status=r13_sidequest_status(quest),
            state=winter_copy.deepcopy(r13_sidequest_state(quest)),day=room13["day"],
            period=room13["period"],place=room13["location"],
            protected_story_unchanged=qa146_quest_projection()==renpy.test.runtime146_quest_base))
        renpy.test.runtime146_gui=rows
        qa146_output("gui-quests.json",dict(scope="각 시작 상태는 직접 준비. 이후 수락·물건 선택·작업·보고는 실제 GUI 클릭. notice는 왕복 지도 이동도 클릭.",checkpoints=rows))
        return rows[-1]["status"]==phase and rows[-1]["protected_story_unchanged"]

    def qa146_summary():
        report=renpy.test.runtime146_report
        report["counts"]=dict(states=len(report["states"]),npc_visits=sum(len(r.get("people",())) for r in report["states"]),
                              choices=sum(len(p["choices"]) for r in report["states"] for p in r.get("people",())),
                              objects=sum(len(r.get("objects",())) for r in report["states"]),issues=len(report["issues"]),diagnostics=len(report["diagnostics"]))
        qa146_output("engine-sweep.json",report)
        return not report["issues"]

testcase runtime146_prepared_query_sweep:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa146_begin)
    run Function(qa146_sweep_day,1)
    run Function(qa146_sweep_day,2)
    run Function(qa146_sweep_day,3)
    run Function(qa146_sweep_day,4)
    run Function(qa146_sweep_day,5)
    run Function(qa146_sweep_day,6)
    run Function(qa146_sweep_day,7)
    run Function(qa146_sweep_branches)
    assert eval (qa146_summary())


label qa146_quest_start(quest):
    $ qa146_begin()
    $ qa146_place={'seam':'inn','notice':'square','parts':'workshop'}[quest]
    $ qa146_prepare(2,1,qa146_place,gate='afternoon2',scene='MS14_D02_S04')
    $ r13_v111_arrive(['daram'])
    $ renpy.test.runtime146_quest_base=qa146_quest_projection()
    call r13_scene(R13_PLACES[room13['location']][1],R13_PLACES[room13['location']][0],'calm')
    call r13_v111_wait('afternoon2')
    return

# 준비된 2일차 오후에서 시작. 수락·작업·보고는 실제 화면 버튼을 누른다.
testcase runtime146_gui_quest_seam:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa146_quest_start','seam')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    if eval (r13_world_offset()>0):
        click '왼쪽 구역' until eval (r13_world_offset()==0) timeout 20
    pause .7
    click '여니'
    pause until screen 'r13_topics' timeout 15
    pause .7
    screenshot '146-seam-offer.png'
    if not '바느질을 조금 도와드릴까요?':
        click id 'r13_topics_next' until '바느질을 조금 도와드릴까요?' timeout 15
    click '바느질을 조금 도와드릴까요?'
    click pos (900,600) until '제가 해 볼게요.' timeout 35
    pause .7
    click '제가 해 볼게요.'
    click pos (900,600) until screen 'r13_topics' timeout 35
    assert eval (qa146_gui_checkpoint('seam','accepted'))
    pause .7
    click '돌아가기'
    pause until screen 'r13_hub' timeout 15
    pause .7
    if not '털실 바구니':
        click '오른쪽 구역' until '털실 바구니' timeout 20
    pause .7
    click '털실 바구니'
    pause until screen 'r13_confirm' timeout 15
    pause .7
    screenshot '146-seam-work-confirm.png'
    click '천을 받치고 한 땀 뜬다'
    pause until '움직일 틈을 두고 꿰맨다' timeout 15
    pause .7
    click '움직일 틈을 두고 꿰맨다'
    click pos (900,600) until screen 'r13_hub' timeout 25
    assert eval (qa146_gui_checkpoint('seam','worked'))
    assert eval (r13_sidequest_state('seam').get('result')=='room')
    if eval (r13_world_offset()>0):
        click '왼쪽 구역' until eval (r13_world_offset()==0) timeout 20
    pause .7
    click '여니'
    pause until screen 'r13_topics' timeout 15
    pause .7
    if not '부탁하신 일을 마쳤습니다.':
        click id 'r13_topics_next' until '부탁하신 일을 마쳤습니다.' timeout 15
    click '부탁하신 일을 마쳤습니다.'
    click pos (900,600) until screen 'r13_topics' timeout 35
    assert eval (qa146_gui_checkpoint('seam','done'))
    pause .7
    screenshot '146-seam-reported.png'

# 준비된 2일차 오후에서 시작. 수락·작업·보고는 실제 화면 버튼을 누른다.
testcase runtime146_gui_quest_notice:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa146_quest_start','notice')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    if eval (r13_world_offset()>0):
        click '왼쪽 구역' until eval (r13_world_offset()==0) timeout 20
    pause .7
    click '설이'
    pause until screen 'r13_topics' timeout 15
    pause .7
    screenshot '146-notice-offer.png'
    if not '종소리 안내를 도와드릴까요?':
        click id 'r13_topics_next' until '종소리 안내를 도와드릴까요?' timeout 15
    click '종소리 안내를 도와드릴까요?'
    click pos (900,600) until '제가 해 볼게요.' timeout 35
    pause .7
    click '제가 해 볼게요.'
    click pos (900,600) until screen 'r13_topics' timeout 35
    assert eval (qa146_gui_checkpoint('notice','accepted'))
    pause .7
    click '돌아가기'
    pause until screen 'r13_hub' timeout 15
    pause .7
    click '지도'
    pause until screen 'r13_map' timeout 15
    pause .7
    click id 'map_name_post'
    pause .4
    click id 'r13_map_travel'
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    assert eval (room13['location']=='post')
    pause .7
    if not '게시된 공고':
        click '오른쪽 구역' until '게시된 공고' timeout 20
    pause .7
    click '게시된 공고'
    pause until screen 'r13_confirm' timeout 15
    pause .7
    screenshot '146-notice-work-confirm.png'
    click '접힌 종소리 안내를 편다'
    pause until '종소리 수가 먼저 보이게 편다' timeout 15
    pause .7
    click '종소리 수가 먼저 보이게 편다'
    click pos (900,600) until screen 'r13_hub' timeout 25
    assert eval (qa146_gui_checkpoint('notice','worked'))
    assert eval (r13_sidequest_state('notice').get('result')=='count')
    pause .7
    click '지도'
    pause until screen 'r13_map' timeout 15
    pause .7
    click id 'map_name_square'
    pause .4
    click id 'r13_map_travel'
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    assert eval (room13['location']=='square')
    if eval (r13_world_offset()>0):
        click '왼쪽 구역' until eval (r13_world_offset()==0) timeout 20
    pause .7
    click '설이'
    pause until screen 'r13_topics' timeout 15
    pause .7
    if not '부탁하신 일을 마쳤습니다.':
        click id 'r13_topics_next' until '부탁하신 일을 마쳤습니다.' timeout 15
    click '부탁하신 일을 마쳤습니다.'
    click pos (900,600) until screen 'r13_topics' timeout 35
    assert eval (qa146_gui_checkpoint('notice','done'))
    pause .7
    screenshot '146-notice-reported.png'

# 준비된 2일차 오후에서 시작. 수락·작업·보고는 실제 화면 버튼을 누른다.
testcase runtime146_gui_quest_parts:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa146_quest_start','parts')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    if eval (r13_world_offset()>0):
        click '왼쪽 구역' until eval (r13_world_offset()==0) timeout 20
    pause .7
    click '부리'
    pause until screen 'r13_topics' timeout 15
    pause .7
    screenshot '146-parts-offer.png'
    if not '부품 정리를 좀 도와줄까?':
        click id 'r13_topics_next' until '부품 정리를 좀 도와줄까?' timeout 15
    click '부품 정리를 좀 도와줄까?'
    click pos (900,600) until '내가 해 볼게.' timeout 35
    pause .7
    click '내가 해 볼게.'
    click pos (900,600) until screen 'r13_topics' timeout 35
    assert eval (qa146_gui_checkpoint('parts','accepted'))
    pause .7
    click '돌아가기'
    pause until screen 'r13_hub' timeout 15
    pause .7
    if not '부품 접시':
        click '오른쪽 구역' until '부품 접시' timeout 20
    pause .7
    click '부품 접시'
    pause until screen 'r13_confirm' timeout 15
    pause .7
    screenshot '146-parts-work-confirm.png'
    click '여분 부품을 천 위에 정리한다'
    pause until '길이가 비슷한 것끼리 놓는다' timeout 15
    pause .7
    click '길이가 비슷한 것끼리 놓는다'
    click pos (900,600) until screen 'r13_hub' timeout 25
    assert eval (qa146_gui_checkpoint('parts','worked'))
    assert eval (r13_sidequest_state('parts').get('result')=='length')
    if eval (r13_world_offset()>0):
        click '왼쪽 구역' until eval (r13_world_offset()==0) timeout 20
    pause .7
    click '부리'
    pause until screen 'r13_topics' timeout 15
    pause .7
    if not '부탁한 일을 마쳤어.':
        click id 'r13_topics_next' until '부탁한 일을 마쳤어.' timeout 15
    click '부탁한 일을 마쳤어.'
    click pos (900,600) until screen 'r13_topics' timeout 35
    assert eval (qa146_gui_checkpoint('parts','done'))
    pause .7
    screenshot '146-parts-reported.png'
