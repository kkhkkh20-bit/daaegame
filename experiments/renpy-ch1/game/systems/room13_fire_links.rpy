# 화재의 관찰·질문·책임을 직접 연결한다. 제출 판정과 기회는 기존 proof 라벨이 맡는다.
default r13_fire_link_views = {}

init 352 python:
    R13_FIRE_LINK_FIRST="불이 시작된 곳과 진술을 대조한다"
    R13_FIRE_LINK_KEYS=(R13_FIRE_LINK_FIRST,"불의 원인과 빈 창고 진압을 구분한다","불의 원인과 아이 구조를 구분한다")
    R13_FIRE_LINK_QUESTIONS=(
        ("door","문 앞에서 무엇을 하셨습니까?"),
        ("lamp_keeper","창고 등잔은 누가 관리합니까?"),
        ("wood_owner","뒤창 장작은 누구 것입니까?"),
    )

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

    def r13_fire_link_check(key,state,owned,observations):
        """연결 문법만 검사한다. 틀린 자료는 원래 판정으로 보내며 정답 함수를 호출하지 않는다."""
        first=key==R13_FIRE_LINK_FIRST
        chosen=r13_fire_link_union(state,owned,first)
        if not chosen:return "empty"
        if first:
            facts=tuple(state.get("observations",(None,None)))
            available={r[0] for r in observations}
            if len(facts)!=2 or any(f not in available for f in facts) or facts[0]==facts[1]:return "incomplete"
            # 문 앞 흔적은 등잔 상태와도, 실제 목격과도 연결할 수 있다. 범인은 아직 확정하지 않는다.
            if set(facts) not in ({"lamp","door"},{"door","witness"}) or state.get("question")!="door":return "links"
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
        if key==R13_FIRE_LINK_FIRST:row["materials"]=args
        else:
            row["roles"]=[k if k in args else None for k in row["roles"]]
            row["extra"]=[k for k in args if k not in row["roles"]]
        if row.get("detail") not in owned:row["detail"]=None
        row["notice"]=None;r13_fire_links_write(claim,row)
        renpy.restart_interaction()

    def r13_fire_links_sync(claim,key,row):
        r13_fire_links_write(claim,row)
        r13_pw_set_arguments(claim,r13_fire_link_union(row,r13_pw_entries(),key==R13_FIRE_LINK_FIRST))
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
            row["notice"]=None;r13_fire_links_sync(claim,key,row);return
        else:return
        row.update(view="board",notice=None);r13_fire_links_sync(claim,key,row)

    def r13_fire_links_submit(claim,key):
        row=r13_fire_links_state(claim);owned=r13_pw_entries()
        observations=r13_fire_link_observations(owned,r13_v111_value("bori_nubi_door_witness_heard") is True)
        check=r13_fire_link_check(key,row,owned,observations)
        if check!="ready":
            messages={"empty":"제시할 자료를 먼저 고르세요.","incomplete":"빈 연결 자리를 채운 뒤 함께 읽어 보세요.",
                "links":"고른 관찰에서 그 질문이 이어지는지 다시 읽어 보자.","roles":"고른 자료가 각 자리에서 무엇을 설명하는지 다시 읽어 보자."}
            r13_fire_links_change(claim,notice=messages[check]);return
        r13_fire_links_sync(claim,key,row)
        renpy.end_interaction("argue")

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
    $ chosen=r13_fire_link_union(row,owned,first)
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
        text (("제출 자료 %d장"%len(chosen)) if first else ("덧붙인 자료 %d장"%len(row["extra"]))) xpos 142 ypos 474 size small color muted font R13_UI_FONT
        if row["notice"]:
            text row["notice"] xpos 142 ypos 508 xsize 1040 size small color r13_nb_accent() font R13_UI_FONT
        elif chances:
            text chances.replace("회의 기회","기회") xpos 142 ypos 508 xsize 1040 size small color muted font R13_UI_FONT
        fixed:
            xpos 142 ypos footer_y xysize (230,footer_h)
            use r13_control("들은 말 읽기",None,Function(r13_fire_links_change,claim,view="words"),enabled=ready,width=230,height=footer_h,label_size=small,control_id="r13_fire_words")
        fixed:
            xpos 386 ypos footer_y xysize (230,footer_h)
            use r13_control("조사 계속" if investigate else "자료 읽기",None,Return("investigate") if investigate else Function(r13_fire_links_change,claim,view="library",field=None,page=0),enabled=ready,width=230,height=footer_h,label_size=small,control_id="r13_fire_investigate")
        fixed:
            xpos 630 ypos footer_y xysize (240,footer_h)
            use r13_control("자료 고르기" if first else "덧붙일 자료",None,Function(r13_fire_links_change,claim,view="library",field="materials" if first else "extra",page=0),enabled=ready,width=240,height=footer_h,label_size=small,control_id="r13_fire_materials")
        fixed:
            xpos 884 ypos footer_y xysize (298,footer_h)
            use r13_control("연결한 근거 제시",None,Function(r13_fire_links_submit,claim,key),enabled=ready and bool(chosen),primary=True,width=298,height=footer_h,label_size=small,control_id="r13_fire_submit")
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
                use r13_control(r13_ev_two_lines(r13_catalog_title(material),706,small,2),None,Function(r13_fire_links_change,claim,view="read",detail=material,origin=False),enabled=ready,width=766,height=76,label_size=small,control_id=r13_pw_id("r13_fire_read_",material))
            if row["field"]:
                $ is_chosen=(material in row.get(row["field"],[]) if row["field"] in ("materials","extra") else material in chosen)
                fixed:
                    xpos 920 ypos yy xysize (262,76)
                    use r13_control("선택 해제" if is_chosen and row["field"] in ("materials","extra") else "이 자료 선택",None,Function(r13_fire_links_pick,claim,key,row["field"],material),enabled=ready,chosen=is_chosen,width=262,height=76,label_size=small,control_id=r13_pw_id("r13_fire_pick_",material))
        text ("%d / %d쪽"%(page+1,max(1,(len(listed)+2)//3))) xpos 876 ypos 514 size small color muted font R13_UI_FONT
        fixed:
            xpos 142 ypos footer_y xysize (284,footer_h)
            use r13_control("연결판으로",None,Function(r13_fire_links_change,claim,view="board"),enabled=ready,width=284,height=footer_h,label_size=small,control_id="r13_fire_back")
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
            use r13_control("자료 목록으로",None,Function(r13_fire_links_change,claim,view="library"),enabled=ready,width=284,height=footer_h,label_size=small,control_id="r13_fire_back")
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
