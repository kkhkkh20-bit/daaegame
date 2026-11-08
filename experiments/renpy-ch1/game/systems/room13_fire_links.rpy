# 화재의 관찰·질문·책임을 직접 연결한다. 제출 판정과 기회는 기존 proof 라벨이 맡는다.
default r13_fire_link_views = {}
default r13_fire_recheck_focus = None

init 352 python:
    R13_FIRE_LINK_FIRST="불이 시작된 곳과 진술을 대조한다"
    R13_FIRE_LINK_KEYS=(R13_FIRE_LINK_FIRST,"불의 원인과 빈 창고 진압을 구분한다","불의 원인과 아이 구조를 구분한다")
    R13_FIRE_LINK_QUESTIONS=(
        ("door","문 앞에서 무엇을 하셨습니까?"),
        ("lamp_keeper","창고 등잔은 누가 관리합니까?"),
        ("wood_owner","뒤창 장작은 누구 것입니까?"),
    )
    R13_FIRE_SITE_ART="assets/room13-fire-site-observations.webp"
    R13_FIRE_SITE_PANELS=(
        ("뒷벽 물통 옆","뚜껑이 닫혀 있다.\n안에 기름이 남아 있다.",(0,0,879,887)),
        ("문 쪽","탄 자국 곁에 천이 있다.\n천에서 기름 냄새가 났다.",(895,0,879,887)),
    )

    def r13_fire_site_available(key,owned):
        # 조사로 얻은 기록을 다시 보는 화면. 미조사 저장에 관찰을 먼저 보여 주지 않는다.
        return key=="V111:E06_FIRE" and key in owned

    def r13_fire_site_panel(index,size):
        return Transform(Crop(R13_FIRE_SITE_PANELS[index][2],R13_FIRE_SITE_ART),xysize=(size,size),fit="contain",nearest=True)

    def r13_fire_link_clone(row):
        result=dict(row or {})
        for field in ("materials","roles","extra","observations"):
            if field in result:result[field]=list(result[field])
        return result

    def r13_fire_link_observations(owned,witness=False):
        """기존 자료와 실제 청취로만 만드는 관찰. 조회는 상태를 바꾸지 않는다."""
        rows=[]
        if "V111:E06_FIRE" in owned:
            rows.extend([
                ("lamp","등잔은 뒷벽 물통 옆에 있었고, 뚜껑이 닫힌 채 기름이 남아 있었다.","V111:E06_FIRE"),
                ("door","문 쪽에서 탄 자국과 기름 냄새 나는 천을 확인했다.","V111:E06_FIRE"),
            ])
        if witness:
            rows.append(("witness","보리는 불이 번지기 전 누비가 창고 문 앞에 서 있는 것을 봤다.",None))
        if "V111:E06_EMPTY" in owned:
            rows.append(("bori","아이들은 학교로 옮겨졌고, 보리는 빈 창고의 불 확산을 막았다.","V111:E06_EMPTY"))
        elif "V111:E06_RESCUE" in owned:
            rows.append(("bori","보리는 아이 하나를 안고 나왔고, 두 아이가 뒤따라 나왔다.","V111:E06_RESCUE"))
        return rows

    def r13_fire_link_union(state,owned,first):
        """연결판의 제출 묶음. 순서를 보존하고 미보유·중복만 제외한다."""
        values=list(state.get("materials",())) if first else list(state.get("roles",()))+list(state.get("extra",()))
        result=[]
        for value in values:
            if value in owned and value not in result:result.append(value)
        return result

    def r13_fire_link_sources(state,owned,observations):
        """고른 사실의 실제 출처 제안. 명시적으로 바꾼 자료·구 저장의 선택은 그대로 둔다.
        이 함수는 arguments에 쓰지 않는다. 출처 확인 화면의 명시적 제출에서만 실제 묶음이 된다.
        """
        if state.get("source_manual",bool(state.get("materials"))):
            return r13_fire_link_union(state,owned,True)
        sources=dict((fact,source) for fact,text,source in observations)
        result=[]
        for fact in state.get("observations",()):
            source=sources.get(fact)
            if source in owned and source not in result:result.append(source)
        return result

    def r13_fire_link_check(key,state,owned,observations):
        """연결 문법만 검사한다. 틀린 자료는 원래 판정으로 보내며 정답 함수를 호출하지 않는다."""
        first=key==R13_FIRE_LINK_FIRST
        chosen=r13_fire_link_union(state,owned,first)
        if not chosen:return "empty"
        if first:
            facts=tuple(state.get("observations",(None,None)))
            available={r[0] for r in observations}
            if len(facts)!=2 or any(f not in available for f in facts) or facts[0]==facts[1]:return "incomplete"
            # 화면은 선택의 문법만 검사한다. 질문의 타당성은 실제 누비의 답변으로 확인한다.
            if state.get("question") not in dict(R13_FIRE_LINK_QUESTIONS):return "incomplete"
            return "ready"
        roles=list(state.get("roles",(None,None,None)))
        if len(roles)!=3:return "incomplete"
        action="V111:E06_EMPTY" if key==R13_FIRE_LINK_KEYS[1] else "V111:E06_RESCUE"
        who={"V111:E07_NUBI","V111:NW_NUBI_TICKET"}
        # 기존 R13_PROOF_EXTRAS의 화재 덧붙임도 역할 배치를 건너뛰게 하지 않는다.
        allowed={"V111:E06_FIRE",action,"V111:NW_LAUNDRY_TALK","V111:E02"}|who
        # 맞는 자료가 자리만 뒤바뀐 경우 연결만 다시 본다. 다른 자료·부족한 묶음은 기존 오답 처리를 받는다.
        if set(chosen)<=allowed and "V111:E06_FIRE" in chosen and action in chosen and set(chosen)&who:
            if roles[0]!="V111:E06_FIRE" or roles[1] not in who or roles[2]!=action:return "roles"
        return "ready"

    def r13_fire_question_route(payload,observations):
        """상대가 답할 대목. UI 정답 표시나 자료 판정을 하지 않는다."""
        if not isinstance(payload,dict):return "incomplete"
        facts=payload.get("observations")
        if not isinstance(facts,(list,tuple)) or len(facts)!=2:return "incomplete"
        available={row[0] for row in observations}
        if any(not isinstance(fact,str) or fact not in available for fact in facts) or facts[0]==facts[1]:return "incomplete"
        question=payload.get("question")
        if not isinstance(question,str) or question not in dict(R13_FIRE_LINK_QUESTIONS):return "incomplete"
        if question!="door":return question
        if set(facts) in ({"lamp","door"},{"door","witness"}):return "challenge"
        return "action" if "bori" in facts else "presence"

    def r13_fire_recheck_options(owned,pot_heard=False):
        """자백 전 실제로 읽을 수 있는 기록·청취만. 둘 다 합리적인 되물음이다."""
        options=[]
        if "V111:E06_FIRE" in owned:options.append("trace")
        if pot_heard:options.append("pot")
        return tuple(options)

init 353 python:
    def r13_fire_links_active(key):
        if not r13_v111_active() or key not in R13_FIRE_LINK_KEYS:return False
        # 옛 판에서 가설을 마친 저장은 기존 자료 대조를 그대로 이어 간다.
        return key!=R13_FIRE_LINK_FIRST or r13_v111_value("fire_origin_hypothesis") is not True

    def r13_fire_links_state(claim):
        row=r13_fire_link_clone((r13_fire_link_views or {}).get(claim,{}) or {})
        row.setdefault("view","board");row.setdefault("field",None);row.setdefault("page",0)
        row.setdefault("tab","now")
        row.setdefault("observations",[None,None]);row.setdefault("question",None)
        row.setdefault("roles",[None,None,None]);row.setdefault("extra",[])
        row.setdefault("materials",list((room13.get("arguments") or {}).get(claim,())))
        # 이 값이 없는 구 저장의 직접 선택을 출처 제안으로 덮어쓰지 않는다.
        row.setdefault("source_manual",bool(row["materials"]))
        row.setdefault("source_pending",False)
        row.setdefault("library_return","board");row.setdefault("read_return","library")
        row.setdefault("detail",None);row.setdefault("origin",False);row.setdefault("notice",None)
        return row

    def r13_fire_links_write(claim,row):
        views=dict(r13_fire_link_views or {});views[claim]=r13_fire_link_clone(row);store.r13_fire_link_views=views
        # call screen 안에서 고친 연결도 저장에 남긴다. 불러오기가 문장 시작으로 되돌리지 않게 한다.
        renpy.retain_after_load()

    def r13_fire_links_change(claim,**changes):
        row=r13_fire_links_state(claim);row.update(changes);r13_fire_links_write(claim,row)
        renpy.restart_interaction()

    def r13_fire_links_enter(claim,key):
        row=r13_fire_links_state(claim);owned=r13_pw_entries()
        args=[k for k in (room13.get("arguments") or {}).get(claim,()) if k in owned]
        if key==R13_FIRE_LINK_FIRST:
            if not row["source_pending"]:row["materials"]=args
        else:
            row["roles"]=[k if k in args else None for k in row["roles"]]
            row["extra"]=[k for k in args if k not in row["roles"]]
        if row.get("detail") not in owned:row["detail"]=None
        row["notice"]=None;r13_fire_links_write(claim,row)
        renpy.restart_interaction()

    def r13_fire_links_sync(claim,key,row):
        r13_fire_links_write(claim,row)
        # 첫 쟁점은 출처 확인의 제출 전까지 후보만 저장한다. 둘째 쟁점의 역할 배치는 기존처럼 동기화한다.
        if key!=R13_FIRE_LINK_FIRST:
            r13_pw_set_arguments(claim,r13_fire_link_union(row,r13_pw_entries(),False))
        renpy.restart_interaction()

    def r13_fire_links_pick(claim,key,field,value):
        row=r13_fire_links_state(claim);owned=r13_pw_entries()
        if field in ("obs0","obs1"):
            valid=[x[0] for x in r13_fire_link_observations(owned,r13_v111_value("bori_nubi_door_witness_heard") is True)]
            if value not in valid:return
            facts=list(row["observations"]);facts[int(field[-1])]=value;row["observations"]=facts
        elif field=="question":
            if value not in dict(R13_FIRE_LINK_QUESTIONS):return
            row["question"]=value
        elif field in ("role0","role1","role2"):
            if value not in owned:return
            roles=list(row["roles"]);roles[int(field[-1])]=value;row["roles"]=roles
            row["extra"]=[k for k in row["extra"] if k!=value]
        elif field in ("materials","extra"):
            if value not in owned:return
            chosen=list(row[field]);row[field]=[k for k in chosen if k!=value] if value in chosen else chosen+[value]
            if field=="materials":row.update(source_manual=True,source_pending=True)
            row["notice"]=None;r13_fire_links_sync(claim,key,row);return
        else:return
        row.update(view="board",notice=None);r13_fire_links_sync(claim,key,row)

    def r13_fire_links_submit(claim,key):
        row=r13_fire_links_state(claim);owned=r13_pw_entries()
        observations=r13_fire_link_observations(owned,r13_v111_value("bori_nubi_door_witness_heard") is True)
        if key==R13_FIRE_LINK_FIRST:
            # 관찰을 고르는 동안에는 제안만 보인다. 출처 확인의 제출이 자료 묶음을 확정한다.
            row["materials"]=r13_fire_link_sources(row,owned,observations)
        check=r13_fire_link_check(key,row,owned,observations)
        if check!="ready":
            messages={"empty":"제시할 자료를 먼저 고르세요.","incomplete":"빈 연결 자리를 채운 뒤 함께 읽어 보세요.",
                "roles":"고른 자료가 각 자리에서 무엇을 설명하는지 다시 읽어 보자."}
            r13_fire_links_change(claim,notice=messages[check]);return
        if key==R13_FIRE_LINK_FIRST:
            # 문답이 끝나기 전에는 기존 제출 자료를 바꾸거나 성공을 기록하지 않는다.
            row["source_pending"]=True
            r13_fire_links_write(claim,row)
            payload=dict(question=row["question"],observations=list(row["observations"]),materials=list(row["materials"]))
            renpy.end_interaction(("fire_question",payload));return
        else:r13_fire_links_sync(claim,key,row)
        renpy.end_interaction("argue")

    def r13_fire_question_validate(payload):
        """저장·재진입 때도 현재 소유/선택과 일치하는 문답만 실행한다. 조회는 무변경."""
        if not isinstance(payload,dict):return "incomplete"
        claim="v111:"+R13_FIRE_LINK_FIRST
        row=r13_fire_links_state(claim);owned=r13_pw_entries()
        observations=r13_fire_link_observations(owned,r13_v111_value("bori_nubi_door_witness_heard") is True)
        route=r13_fire_question_route(payload,observations)
        materials=payload.get("materials")
        if route=="incomplete" or not isinstance(materials,(list,tuple)) or not materials:return "incomplete"
        if any(not isinstance(material,str) or material not in owned for material in materials):return "incomplete"
        if list(payload["observations"])!=row["observations"] or payload["question"]!=row["question"]:return "incomplete"
        if list(materials)!=r13_fire_link_sources(row,owned,observations):return "incomplete"
        return route

    def r13_fire_question_finish(payload,argue=False):
        claim="v111:"+R13_FIRE_LINK_FIRST
        route=r13_fire_question_validate(payload)
        if route=="incomplete" or (argue and route!="challenge"):return False
        row=r13_fire_links_state(claim);row.update(view="board",notice=None)
        if argue:
            row["source_pending"]=False
            r13_pw_set_arguments(claim,list(payload["materials"]))
        r13_fire_links_write(claim,row)
        return True

    def r13_fire_admission_ready():
        # 이미 마친 저장은 다시 묻지 않는다. 자료 소유만으로 성공한 것으로 간주하지 않는다.
        if r13_v111_value("NUBI_admitted_setting_fire"):return True
        given=r13_v111_value("proof_given:"+R13_FIRE_LINK_FIRST) or []
        return r13_v111_owned("E06_FIRE") and r13_v111_proof_accepts(R13_FIRE_LINK_FIRST,["E06_FIRE"],given)

    def r13_fire_links_edit_sources(claim):
        row=r13_fire_links_state(claim);owned=r13_pw_entries()
        observations=r13_fire_link_observations(owned,r13_v111_value("bori_nubi_door_witness_heard") is True)
        row["materials"]=r13_fire_link_sources(row,owned,observations)
        row.update(source_manual=True,source_pending=True,view="library",field="materials",page=0,library_return="sources",notice=None)
        # 바꾸기 창을 연 것만으로 제출할 자료나 기회를 바꾸지 않는다.
        r13_fire_links_write(claim,row);renpy.restart_interaction()

    def r13_fire_links_clear(claim,key,field):
        if field not in ("role0","role1","role2"):return
        row=r13_fire_links_state(claim)
        row["roles"][int(field[-1])]=None
        row.update(view="board",notice=None)
        r13_fire_links_sync(claim,key,row)

    def r13_fire_links_text(row,index,first,observations):
        if first:
            if index<2:return dict((k,t) for k,t,source in observations).get(row["observations"][index],"관찰을 고른다")
            return dict(R13_FIRE_LINK_QUESTIONS).get(row["question"],"이어 물을 질문을 고른다")
        value=row["roles"][index]
        return r13_catalog_title(value) if value in r13_pw_entries() else "자료를 놓는다"

screen r13_fire_recheck(options):
    modal True
    zorder 50
    $ focus=r13_fire_recheck_focus if r13_fire_recheck_focus in options else options[0]
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    $ ink=r13_nb_ink()
    $ muted=r13_nb_muted()
    $ small=r13_type("small")
    $ footer_y=r13_nb_footer_y()
    $ footer_h=r13_control_height()
    use r13_notebook_shell("누비의 말과 대조한다",rule_y=132)
    text "누비: “나가라고…… 하려고 했어요.”" xpos 142 ypos 150 xsize 1040 size r13_type("emphasis") color ink font R13_UI_BOLD_FONT
    text "확인한 기록이나 앞서 들은 말을 펴고, 그 대목을 직접 묻는다." xpos 142 ypos 202 xsize 1040 size small color muted font R13_UI_FONT
    for index,option in enumerate(options):
        fixed:
            xpos (142+index*530) ypos 252 xysize (510,64)
            use r13_control("문 앞에서 확인한 것" if option=="trace" else "물을 데웠다는 말",None,[SetVariable("r13_fire_recheck_focus",option),Function(renpy.retain_after_load)],enabled=ready,chosen=focus==option,width=510,height=64,label_size=small,control_id="r13_fire_recheck_"+option)
    viewport:
        area (142,334,1040,r13_nb_body_bottom()-334) mousewheel True draggable True scrollbars "vertical"
        vscrollbar_unscrollable "hide"
        vbox:
            xsize 1016 spacing 16
            if focus=="trace":
                text r13_catalog_title("V111:E06_FIRE") size r13_type("subtitle") color ink font R13_UI_BOLD_FONT xsize 1000
                text "문 쪽에서 탄 자국과 기름 냄새 나는 천을 확인했다." size r13_type("emphasis") color ink font R13_UI_FONT xsize 1000
                text ("출처: "+r13_catalog_origin("V111:E06_FIRE")) size small color muted font R13_UI_FONT xsize 1000
                use r13_control("현장 그림",None,Show("r13_pw_picture",key="V111:E06_FIRE"),enabled=ready,width=286,height=64,label_size=small,control_id="r13_fire_recheck_picture")
            else:
                text "오늘 빨래터에서 직접 들은 말" size r13_type("subtitle") color ink font R13_UI_BOLD_FONT xsize 1000
                text "누비: “데웠죠. 왜요?”" size r13_type("emphasis") color ink font R13_UI_FONT xsize 1000
                text "보리: “어제 솥은 차가웠소. 해 지기 전에 내가 물 한 바가지 달라고 했잖소.”" size r13_type("emphasis") color ink font R13_UI_FONT xsize 1000
    fixed:
        xpos 742 ypos footer_y xysize (440,footer_h)
        use r13_control("이 대목으로 되묻는다",None,Return(focus),enabled=ready,primary=True,width=440,height=footer_h,label_size=small,control_id="r13_fire_recheck_ask")

screen r13_fire_links(claim,key,can_press=False,investigate=False,chances=None):
    modal True
    zorder 50
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    on "show" action Function(r13_fire_links_enter,claim,key)
    $ row=r13_fire_links_state(claim)
    $ first=key==R13_FIRE_LINK_FIRST
    $ owned=r13_pw_entries()
    $ observations=r13_fire_link_observations(owned,r13_v111_value("bori_nubi_door_witness_heard") is True)
    $ chosen=r13_fire_link_sources(row,owned,observations) if first else r13_fire_link_union(row,owned,False)
    $ ink=r13_nb_ink()
    $ muted=r13_nb_muted()
    $ small=r13_type("small")
    $ footer_y=r13_nb_footer_y()
    $ footer_h=r13_control_height()
    use r13_notebook_shell("화재의 연결",rule_y=132)
    text key xpos 142 ypos 145 xsize 1040 size r13_type("emphasis") color ink font R13_UI_BOLD_FONT
    if row["view"]=="board":
        $ labels=("관찰 하나","다른 관찰","이어 물을 질문") if first else ("불이 남긴 흔적","누비 쪽 근거","보리가 한 일")
        for index in range(3):
            $ yy=190+index*94
            text labels[index] xpos 142 ypos (yy+24) xsize 184 size small color muted font R13_UI_BOLD_FONT
            $ field=("obs"+str(index) if index<2 else "question") if first else "role"+str(index)
            $ next_view="choices" if first else "library"
            fixed:
                xpos 340 ypos yy xysize (842,86)
                use r13_control(r13_ev_two_lines(r13_fire_links_text(row,index,first,observations),782,small,2),None,Function(r13_fire_links_change,claim,view=next_view,field=field,page=0,notice=None),enabled=ready,width=842,height=86,label_size=small,control_id=("r13_fire_slot_%d"%index))
        text (("관찰의 출처 %d장"%len(chosen)) if first else ("덧붙인 자료 %d장"%len(row["extra"]))) xpos 142 ypos 474 size small color muted font R13_UI_FONT
        if row["notice"]:
            text row["notice"] xpos 142 ypos 508 xsize 730 size small color r13_nb_accent() font R13_UI_FONT
        elif chances:
            text chances.replace("회의 기회","기회") xpos 142 ypos 508 xsize 1040 size small color muted font R13_UI_FONT
        if r13_fire_site_available("V111:E06_FIRE",owned):
            fixed:
                xpos 896 ypos 474 xysize (286,56)
                use r13_control("현장 그림",None,Show("r13_pw_picture",key="V111:E06_FIRE"),enabled=ready,width=286,height=56,label_size=small,control_id="r13_fire_site")
        fixed:
            xpos 142 ypos footer_y xysize (230,footer_h)
            use r13_control("들은 말 읽기",None,Function(r13_fire_links_change,claim,view="words"),enabled=ready,width=230,height=footer_h,label_size=small,control_id="r13_fire_words")
        fixed:
            xpos 386 ypos footer_y xysize (230,footer_h)
            use r13_control("현장으로" if investigate else "자료 읽기",None,Return("investigate") if investigate else Function(r13_fire_links_change,claim,view="library",field=None,page=0),enabled=ready,width=230,height=footer_h,label_size=small,control_id="r13_fire_investigate")
        fixed:
            xpos 630 ypos footer_y xysize (240,footer_h)
            use r13_control("자료 읽기" if first else "덧붙일 자료",None,Function(r13_fire_links_change,claim,view="library",field=None if first else "extra",page=0,library_return="board"),enabled=ready,width=240,height=footer_h,label_size=small,control_id="r13_fire_materials")
        fixed:
            xpos 884 ypos footer_y xysize (298,footer_h)
            use r13_control("출처 확인" if first else "연결한 근거 제시",None,Function(r13_fire_links_change,claim,view="sources",notice=None) if first else Function(r13_fire_links_submit,claim,key),enabled=ready and (first or bool(chosen)),primary=True,width=298,height=footer_h,label_size=small,control_id="r13_fire_submit")
    elif row["view"]=="sources" and first:
        viewport:
            id "r13_fire_sources_view"
            area (142,194,1040,r13_nb_body_bottom()-194-50) mousewheel True draggable True scrollbars "vertical"
            vscrollbar_unscrollable "hide"
            vbox:
                xsize 1016 spacing 14
                for material in chosen:
                    button:
                        id r13_pw_id("r13_fire_source_read_",material)
                        xsize 1016 padding (0,4) background None hover_background Solid("#c9a86a22")
                        action Function(r13_fire_links_change,claim,view="read",detail=material,origin=True,read_return="sources") sensitive ready
                        alt ("자료 전체 읽기 · "+r13_catalog_title(material))
                        text r13_catalog_title(material) size r13_type("title") color ink font R13_UI_BOLD_FONT xsize 996
                    use r13_evidence_read_facts(material,1000)
                    text ("출처: "+r13_catalog_origin(material)) size small color muted font R13_UI_FONT xsize 1000
                    if material in room13.get("records",{}):
                        text ("얻은 곳: "+r13_record_source_label(material)) size small color muted font R13_UI_FONT xsize 1000
                    add Solid("#c9a86a99") xsize 1000 ysize 1
                if "witness" in row["observations"] and r13_v111_value("bori_nubi_door_witness_heard") is True:
                    text "보리에게 들은 말" size r13_type("subtitle") color ink font R13_UI_BOLD_FONT
                    text "불이 번지기 전에 누비 씨가 창고 문 앞에 서 있는 건 봤소." size r13_type("emphasis") color ink font R13_UI_FONT xsize 1000
                if not chosen:
                    text "제출할 자료가 없습니다. 연결한 관찰과 출처를 다시 확인하세요." size r13_type("emphasis") color ink font R13_UI_FONT xsize 1000
        if row["notice"]:
            text row["notice"] xpos 142 ypos (r13_nb_body_bottom()-44) xsize 1040 size small color r13_nb_accent() font R13_UI_FONT
        fixed:
            xpos 142 ypos footer_y xysize (284,footer_h)
            use r13_control("연결판으로",None,Function(r13_fire_links_change,claim,view="board"),enabled=ready,width=284,height=footer_h,label_size=small,control_id="r13_fire_back")
        fixed:
            xpos 440 ypos footer_y xysize (274,footer_h)
            use r13_control("자료 바꾸기",None,Function(r13_fire_links_edit_sources,claim),enabled=ready,width=274,height=footer_h,label_size=small,control_id="r13_fire_sources_change")
        fixed:
            xpos 884 ypos footer_y xysize (298,footer_h)
            use r13_control("이 내용으로 묻는다",None,Function(r13_fire_links_submit,claim,key),enabled=ready and bool(chosen),primary=True,width=298,height=footer_h,label_size=small,control_id="r13_fire_sources_submit")
    elif row["view"]=="choices":
        $ choices=R13_FIRE_LINK_QUESTIONS if row["field"]=="question" else [(k,t) for k,t,source in observations]
        for index,(value,caption) in enumerate(choices):
            fixed:
                xpos 142 ypos (194+index*84) xysize (1040,80)
                use r13_control(r13_ev_two_lines(caption,980,small,2),None,Function(r13_fire_links_pick,claim,key,row["field"],value),enabled=ready,width=1040,height=80,label_size=small,control_id=("r13_fire_choice_"+value))
        fixed:
            xpos 142 ypos footer_y xysize (264,footer_h)
            use r13_control("연결판으로",None,Function(r13_fire_links_change,claim,view="board"),enabled=ready,width=264,height=footer_h,label_size=small,control_id="r13_fire_back")
    elif row["view"]=="library":
        $ current=r13_drawer_now(owned) if r13_drawer_active() else owned
        $ listed=current if row["tab"]=="now" else owned
        $ page=max(0,min(row["page"],max(0,(len(listed)-1)//3)))
        for ti,(tab,title) in enumerate((("now","이번 사건"),("all","전체 자료"))):
            fixed:
                xpos (142+ti*238) ypos 190 xysize (224,60)
                use r13_control(title,None,Function(r13_fire_links_change,claim,tab=tab,page=0),enabled=ready,chosen=row["tab"]==tab,width=224,height=60,label_size=small,control_id=("r13_fire_tab_"+tab))
        text "이름은 읽기 · 오른쪽은 선택" xpos 636 ypos 204 xsize 546 size small color muted font R13_UI_FONT
        for index,material in enumerate(listed[page*3:page*3+3]):
            $ yy=254+index*84
            fixed:
                xpos 142 ypos yy xysize (766,76)
                use r13_control(r13_ev_two_lines(r13_catalog_title(material),706,small,2),None,Function(r13_fire_links_change,claim,view="read",detail=material,origin=False,read_return="library"),enabled=ready,width=766,height=76,label_size=small,control_id=r13_pw_id("r13_fire_read_",material))
            if row["field"]:
                $ is_chosen=(material in row.get(row["field"],[]) if row["field"] in ("materials","extra") else material in chosen)
                fixed:
                    xpos 920 ypos yy xysize (262,76)
                    use r13_control("선택 해제" if is_chosen and row["field"] in ("materials","extra") else "이 자료 선택",None,Function(r13_fire_links_pick,claim,key,row["field"],material),enabled=ready,chosen=is_chosen,width=262,height=76,label_size=small,control_id=r13_pw_id("r13_fire_pick_",material))
        text ("%d / %d쪽"%(page+1,max(1,(len(listed)+2)//3))) xpos 876 ypos 514 size small color muted font R13_UI_FONT
        fixed:
            xpos 142 ypos footer_y xysize (284,footer_h)
            use r13_control("출처 확인으로" if row["library_return"]=="sources" else "연결판으로",None,Function(r13_fire_links_change,claim,view=row["library_return"]),enabled=ready,width=284,height=footer_h,label_size=small,control_id="r13_fire_back")
        if row["field"] in ("role0","role1","role2"):
            fixed:
                xpos 440 ypos footer_y xysize (274,footer_h)
                use r13_control("이 연결 지우기",None,Function(r13_fire_links_clear,claim,key,row["field"]),enabled=ready,width=274,height=footer_h,label_size=small,control_id="r13_fire_clear")
        fixed:
            xpos 740 ypos footer_y xysize (212,footer_h)
            use r13_control("이전 쪽",None,Function(r13_fire_links_change,claim,page=page-1),enabled=ready and page>0,width=212,height=footer_h,label_size=small,control_id="r13_fire_prev")
        fixed:
            xpos 968 ypos footer_y xysize (214,footer_h)
            use r13_control("다음 쪽",None,Function(r13_fire_links_change,claim,page=page+1),enabled=ready and (page+1)*3<len(listed),width=214,height=footer_h,label_size=small,control_id="r13_fire_next")
    elif row["view"]=="read":
        $ detail=row["detail"] if row["detail"] in owned else None
        use r13_pw_read_card(detail,142,194,1040,r13_nb_body_bottom()-194,row["origin"],ready)
        fixed:
            xpos 142 ypos footer_y xysize (284,footer_h)
            use r13_control("출처 확인으로" if row["read_return"]=="sources" else "자료 목록으로",None,Function(r13_fire_links_change,claim,view=row["read_return"]),enabled=ready,width=284,height=footer_h,label_size=small,control_id="r13_fire_back")
        fixed:
            xpos 842 ypos footer_y xysize (340,footer_h)
            use r13_control("출처 접기" if row["origin"] else "출처와 전체 내용",None,Function(r13_fire_links_change,claim,origin=not row["origin"]),enabled=ready and bool(detail),width=340,height=footer_h,label_size=small,control_id="r13_fire_origin")
    elif row["view"]=="words":
        viewport:
            area (142,194,1040,r13_nb_body_bottom()-194) mousewheel True draggable True scrollbars "vertical"
            vscrollbar_unscrollable "hide"
            vbox:
                xsize 1020 spacing 26
                if r13_v111_value("bori_nubi_door_witness_heard") is True:
                    text "보리에게 들은 말" size r13_type("subtitle") color ink font R13_UI_BOLD_FONT
                    text "불이 번지기 전에 누비 씨가 창고 문 앞에 서 있는 건 봤소." size r13_type("emphasis") color ink font R13_UI_FONT xsize 1020
                if r13_v111_value("fire_lamp_defense_heard") is True:
                    text "누비에게 들은 말" size r13_type("subtitle") color ink font R13_UI_BOLD_FONT
                    text "창고 안에 등잔 있었잖아요. 거기서 불이 번졌을 수도 있죠. 제가 거기 있었다고 불을 놓은 건 아니에요." size r13_type("emphasis") color ink font R13_UI_FONT xsize 1020
        fixed:
            xpos 142 ypos footer_y xysize (284,footer_h)
            use r13_control("연결판으로",None,Function(r13_fire_links_change,claim,view="board"),enabled=ready,width=284,height=footer_h,label_size=small,control_id="r13_fire_back")
        if can_press:
            fixed:
                xpos 842 ypos footer_y xysize (340,footer_h)
                use r13_control("상대에게 되묻는다",None,Return("press"),enabled=ready,width=340,height=footer_h,label_size=small,control_id="r13_fire_press")

# 같은 자료의 두 위치를 직접 확대한다. 새 자료·정답·기회·사건 상태는 만들지 않는다.
screen r13_fire_site_picture(focus=None):
    $ top=R13_NB_TOP+58
    $ small=r13_type("emphasis" if r13_touch_ui() else "small")
    $ box=min(300,r13_nb_body_bottom()-top-small*2-18)
    if focus is None:
        for index,(title,facts,crop) in enumerate(R13_FIRE_SITE_PANELS):
            $ center=398+index*524
            text title xcenter center ypos R13_NB_TOP size r13_type("emphasis") color r13_nb_ink() font R13_UI_BOLD_FONT
            button:
                id ("r13_fire_site_panel_%d"%index)
                xcenter center ypos top xysize (box,box) padding (0,0) background None
                action SetScreenVariable("fire_focus",index) alt (title+" 확대")
                add r13_fire_site_panel(index,box)
            text facts xcenter center ypos (top+box+10) xmaximum 496 size small color r13_nb_ink() font R13_UI_FONT text_align .5
    else:
        $ title,facts,crop=R13_FIRE_SITE_PANELS[focus]
        $ big=r13_nb_body_bottom()-top
        add r13_fire_site_panel(focus,big) xpos 158 ypos top
        vbox:
            xpos (182+big) ypos (top+18) xsize (1000-big) spacing 24
            text title size r13_type("subtitle") color r13_nb_ink() font R13_UI_BOLD_FONT
            text facts size r13_type("emphasis") color r13_nb_ink() font R13_UI_FONT
    fixed:
        xpos 142 ypos r13_nb_footer_y() xysize (276,r13_control_height())
        use r13_control("두 곳 나란히",None,SetScreenVariable("fire_focus",None),chosen=focus is None,width=276,height=r13_control_height(),label_size=small,control_id="r13_fire_site_pair")
