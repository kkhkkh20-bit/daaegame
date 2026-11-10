# 자료 대조 통합 화면. 2026-11-06 소유자 지시로 읽기 시안을 본편에 적용했다.
#   같은 수첩 틀에서 목록·한 장 읽기·두 장 읽기를 바꾼다. 체크한 제출 묶음은 읽는 자료와 별개다.
#   발언은 위에서 펼치고, 기존 사실은 본문 앞에 두며 긴 원문·출처는 펼쳐서 읽는다.
#   본편 1~14일의 등록된 쟁점에 쓴다. 화재는 원래 관찰 연결판과 함께 쓰며,
#   미등록 쟁점·옛 캠페인은 기존 r13_crisis_proof / r13_book 으로 간다.
#
#   바꾸지 않는 것(인계서 13장): v111_claim="v111:"+key 와 room13["arguments"][v111_claim], 정답 판정
#   (r13_v111_proof_accepts·R13_PROOF_ALTERNATES·R13_PROOF_EXTRAS·r13_v111_proof_kept), 기회(r13_v111_proof_chances·
#   r13_nw_retry). 이 파일은 정답 함수를 부르지 않는다 — 목록은 이번 회차 보유 자료(room13["evidence"])에서 기존
#   catalog 적격성으로만 뽑고, 획득 순서(최신 먼저)로 놓는다. 정답 ID·미획득 자료·정답 개수는 어디에도 내지 않는다.
#   읽기·체크·탭·비교·복귀·빈 제출은 기회를 쓰지 않는다 — 제출(「근거 제시」/「비교 마치기」)만 "argue" 를 돌려 주고,
#   판정은 호출한 라벨이 기존 그대로 한다.
#
#   첫 블록(init 350)은 표시 문맥 표와 순수 선택 계산이다. store·renpy 를 쓰지 않아 dev/test_proof_workspace.py 가
#   Ren'Py 없이 그대로 실행한다. store 에 기대는 것은 다음 블록(init 351)에 둔다.
init 350 python:
    # 쟁점 key → 표시 문맥. quote_when: ("flag", 플래그) 는 r13_has, ("value", 값 키) 는 r13_v111_value 가 True 일 때만
    # 발언을 보인다. None 은 늘 보인다. 정답 ID·미획득 자료·미래 대사는 여기 넣지 않는다.
    R13_PW_CONTEXT={
        "함께 들어갈 근거를 고른다":dict(mode="proof",speaker="돌목",
            quote="명단에는 다돌 씨 이름만 있습니다. 다람 이름이 없으니 아이는 들여보낼 수 없습니다.",
            quote_when=("flag","v111:entered:MS14_D01_S02")),
        # 2026-11-05 소유자 시안 승인: 3일도 이미 익힌 같은 화면에서 직접 읽고 고른다.
        # 인용은 각 쟁점 직전에 실제로 들은 발언뿐이며, 진료소에는 질문 제목만 둔다.
        "측정 종료와 점검 기록을 대조한다":dict(mode="proof",speaker=None,quote=None,quote_when=None),
        "수리와 반출을 가릴 자료를 낸다":dict(mode="proof",speaker="너울",
            quote="어제 3번 등을 연 사람은 톡 하나입니다. 장부에 그렇게 적혀 있습니다. 그런데 아침에는 돌이 없었습니다.",
            quote_when=("flag","v111:entered:MS14_D03_S05")),
        "돌과 매입 기록을 낸다":dict(mode="proof",speaker="너울",
            quote="아침에 없던 그 돌은 지금 어디 있습니까? 누구 손을 거쳐 갔습니까?",
            quote_when=("flag","v111:entered:MS14_D03_S05")),
        "바깥 걸쇠 주장과 발견 위치를 대조한다":dict(mode="proof",speaker="실룩",
            quote="새벽에 간 건 맞아요. 걸쇠가 벌어졌길래 칼로 밀어 닫아 줬죠.",
            quote_when=("flag","v111:entered:MS14_D03_S05")),
        "마지막 점검과 인수한 돌을 연결한다":dict(mode="proof",speaker="실룩",
            quote="그 돌을 판 건 맞아요. 그래도 길에서 주운 거예요.",
            quote_when=("flag","v111:entered:MS14_D03_S05")),
        # 두 편지: 인물의 해설 없이 문서 둘을 직접 읽는다. 의문 한 줄만.
        "두 편지를 나란히 본다":dict(mode="compare",speaker=None,
            quote="초대 편지와 방의 메모를 직접 읽고 견준다. 무엇이 같고, 무엇이 다른가.",
            quote_when=None),
        # 방어 진술을 실제 문답에서 먼저 듣고, 발화 위치를 자료로 검증한다.
        "불이 시작된 곳과 진술을 대조한다":dict(mode="proof",speaker="누비",
            quote="창고 안에 등잔 있었잖아요. 거기서 불이 번졌을 수도 있죠. 제가 거기 있었다고 불을 놓은 건 아니에요.",
            quote_when=("value","fire_lamp_defense_heard")),
        # 1부의 나머지 경로. 인용을 새로 만들거나 자료 이름으로 정답을 알려 주지 않는다.
        "수리 뒤 새로 생긴 파손을 가린다":dict(mode="proof",speaker=None,quote=None,quote_when=None),
        "남아 있는 돌과 칼의 사용을 연결한다":dict(mode="proof",speaker=None,quote=None,quote_when=None),
        "밤이 혐의의 근거를 확인한다":dict(mode="proof",speaker=None,quote=None,quote_when=None),
        "두 편지의 초대를 대조한다":dict(mode="compare",speaker=None,quote=None,quote_when=None),
        "불의 원인과 빈 창고 진압을 구분한다":dict(mode="proof",speaker=None,quote=None,quote_when=None),
        "불의 원인과 아이 구조를 구분한다":dict(mode="proof",speaker=None,quote=None,quote_when=None),
    }
    R13_PW_TABS=(("all","전체"),("now","이번 사건"),("past","지난 사건"),("person","사람별"))
    R13_PW_COMPARE_LIMIT=2
    # 저장된 호출의 review_return이 없던 판도 같은 현장으로 돌아갈 수 있게 한다.
    R13_PW_REVIEW_RETURNS={"두 편지를 나란히 본다":"r13_v111_letter_compare_review"}

    def r13_pw_initial_view(mode,hearing_count,remembered=None,pair=None,detail=None,hearing_only=False):
        # 한 발언뿐이면 곧바로 자료를 읽는다. 직접 바꿔 둔 화면과 두 문서 읽기는 보존한다.
        if hearing_only:return "statements"
        if remembered:return remembered
        if mode!="compare" and hearing_count>1:return "statements"
        if mode!="compare" and hearing_count==1:return "list"
        return "pair" if pair else "single" if detail else "list"

    def r13_pw_hearing_geometry(touch):
        # 두 줄 제목에도 상하 여백을 둔다. 한 쪽의 발언 수는 PC4/터치3을 유지한다.
        return dict(per_page=3 if touch else 4,height=88 if touch else 72,gap=8)

    def r13_pw_review_target(key,declared=None):
        return declared or R13_PW_REVIEW_RETURNS.get(key)

    def r13_pw_pair_submission(pair,owned,mode):
        """현재 직접 읽는 쌍을 명시적으로 제출할 때만 사용한다. 정답 자료를 고르지 않는다."""
        values=list(pair or ())
        if mode!="compare" or len(values)!=2 or values[0]==values[1]:return None
        return values if all(k in owned for k in values) else None

    R13_GATE_APPLICATION_QUOTE="신청서에는 다람 이름도 있군요. 받은 명단과 다릅니다."

    def r13_pw_context(key,gate_application_acknowledged=False):
        """시범 쟁점이면 문맥 dict, 아니면 None(호출자가 기존 화면으로 폴백)."""
        spec=R13_PW_CONTEXT.get(key)
        if spec and key=="함께 들어갈 근거를 고른다" and gate_application_acknowledged:
            return dict(spec,quote=R13_GATE_APPLICATION_QUOTE)
        return spec

    def r13_pw_quote_visible(spec,has,value):
        """발언을 보일지. has(flag)·value(key) 는 호출자가 넘기는 조회 함수라 시험에서 바꿔 끼울 수 있다."""
        when=(spec or {}).get("quote_when")
        if not when:return True
        kind,name=when
        if kind=="flag":return bool(has(name))
        return value(name) is True

    def r13_pw_order(keys,days):
        """보유 목록을 획득한 날(최신 먼저)로 놓는다. 같은 날은 원래 목록 순서(획득 순서)를 지킨다.
        날을 모르는 자료는 가장 오래된 것으로 본다. 정답 함수로 정렬하지 않는다."""
        indexed=list(enumerate(keys))
        def day_of(key):
            day=days.get(key) if days else None
            return day if isinstance(day,int) else -1
        indexed.sort(key=lambda pair:(-day_of(pair[1]),pair[0]))
        return [key for _,key in indexed]

    def r13_pw_toggle(chosen,key,owned,mode):
        """체크 켜기·끄기. (새 선택 목록, 교체 대기 자료).
        보유하지 않은 자료는 무시한다. compare 는 둘까지만 — 셋째를 고르면 선택은 그대로 두고 교체 대기로 돌려 준다
        (처음 것을 자동으로 버리지 않는다). 일반 proof 에는 개수 제한이 없다."""
        chosen=list(chosen or ())
        if key not in (owned or ()):return chosen,None
        if key in chosen:
            return [k for k in chosen if k!=key],None
        if mode=="compare" and len(chosen)>=R13_PW_COMPARE_LIMIT:
            return chosen,key
        return chosen+[key],None

    def r13_pw_replace(chosen,old,new,owned):
        """교체 대기 자료를 고른 자리에 넣는다. 자리가 없거나 보유하지 않은 자료면 그대로."""
        chosen=list(chosen or ())
        if old not in chosen or new not in (owned or ()) or new in chosen:return chosen
        return [new if k==old else k for k in chosen]

    def r13_pw_remove(chosen,key):
        return [k for k in (chosen or ()) if k!=key]

    def r13_pw_submit_ok(chosen,mode):
        """주 행동이 눌리는가. 빈 제출은 막는다(기회를 쓰지 않는다). compare 는 정확히 둘."""
        n=len(chosen or ())
        if mode=="compare":return n==R13_PW_COMPARE_LIMIT
        return n>0

    def r13_pw_pair_from_chosen(chosen,mode):
        """compare 에서 「나란히 보기」가 펼칠 두 자료. 둘이 아니면 None."""
        if mode=="compare" and len(chosen or ())==R13_PW_COMPARE_LIMIT:return (chosen[0],chosen[1])
        return None

    def r13_pw_pair_fill(pair,key):
        """읽기용 쌍의 빈 자리를 채운다. 제출 묶음과는 별개다."""
        a,b=(tuple(pair or ())+(None,None))[:2]
        if key is None or key in (a,b):return (a,b)
        if a is None:return (key,b)
        if b is None:return (a,key)
        return (a,b)

    def r13_pw_pair_live(pair,owned):
        """없는 자료가 든 쌍은 정리한다. 둘 다 있을 때만 나란히 읽는다."""
        if not pair:return None
        a,b=(tuple(pair)+(None,None))[:2]
        a=a if a in (owned or ()) else None
        b=b if b in (owned or ()) else None
        if a is None and b is None:return None
        return (a,b)

    def r13_pw_pair_on_open(chosen,pair,detail,owned):
        """직접 체크한 두 장을 펼친다. 읽기만 바꾸며 제출 묶음은 건드리지 않는다."""
        selected=tuple(chosen or ())
        if len(selected)==2 and selected[0]!=selected[1] and all(k in owned for k in selected):
            return selected
        live=r13_pw_pair_live(pair,owned)
        return live or (detail if detail in owned else None,None)

    def r13_pw_initial_tab(mode,use_drawer,entries,current):
        # 비교는 지난 자료와도 견주므로 처음부터 보유 목록 전체를 연다.
        return "now" if mode!="compare" and use_drawer and len(entries)>=13 and current else "all"

    def r13_pw_read_pair(pair,key,slot):
        """읽을 자리만 바꾼다. 중복 자료는 다른 자리에서 비우며 제출 선택은 받지 않는다."""
        items=list((tuple(pair or ())+(None,None))[:2])
        if slot not in (0,1):return tuple(items)
        items[slot]=key
        if items[1-slot]==key:items[1-slot]=None
        return tuple(items)

    def r13_pw_main_label(mode):
        return "비교 마치기" if mode=="compare" else "근거 제시"

    def r13_pw_room_letters_copy(key,pair,discovery_needed,observed,inquiry=False):
        """첫 방의 실제 읽는 두 글만, 관찰 전후에 맞는 조작 설명을 쓴다."""
        values=tuple(pair or ())
        if key not in ("두 편지를 나란히 본다","v111:두 편지를 나란히 본다") or len(values)!=2 or set(values)!={"V111:E01","V111:E06"}:
            return None
        if inquiry:
            return ("다람과 이야기","두 글을 읽고, 다람과 함께 확인합니다.")
        if observed:
            return ("발견한 차이 확인","「발견한 차이 확인」을 눌러 다람과 이야기를 이어 가세요.")
        if not discovery_needed:
            # 이미 비교를 끝낸 옛 저장에는 새 관찰을 요구하지 않는다.
            return ("비교 내용 확인","「비교 내용 확인」을 눌러 이야기를 이어 가세요.")
        return ("차이 살펴보기","두 글의 다른 부분을 직접 짚어 보세요. 기회는 줄어들지 않습니다.")

    def r13_pw_pages(sections,cols,cap,card_h,header_h,gap=8,pager_h=0):
        """목록을 눈에 보이는 쪽으로 나눈다(소유자: 긴 목록은 명시적 쪽 넘김, 숨은 스크롤 없음).
        2026-10-27 14일 자동 플레이: 1일 13호 「두 편지를 나란히 본다」에서 자료 7개 중 4개만 보이고 「방의 메모」가
        숨은 스크롤 아래에 있어 제출이 막혔다. 줄 단위(묶음 제목 한 줄, 카드 한 줄)로 높이를 재서 한 쪽에 들어가는 만큼만
        담는다. 한 쪽을 넘으면 쪽 넘김 줄 높이(pager_h)만큼 줄여 다시 나눈다. 반환: [[("header",글)|("cards",[키…]),…],…]."""
        rows=[]
        for header,keys in sections:
            if header:rows.append(("header",header,header_h))
            for i in range(0,len(keys),cols):rows.append(("cards",list(keys[i:i+cols]),card_h))
        def pack(limit):
            pages=[];page=[];used=0
            for kind,value,height in rows:
                need=height+(gap if page else 0)
                if page and used+need>limit:
                    pages.append(page);page=[];used=0;need=height
                page.append((kind,value));used+=need
            return pages+([page] if page else []) or [[]]
        pages=pack(cap)
        if len(pages)>1 and pager_h:pages=pack(cap-pager_h-gap)
        return pages

# store 에 기대는 도우미와 화면.
default r13_pw_views = {}   # 쟁점(claim)별 UI 기억: 탭·열어 본 자료·발언 접힘. 구 저장에는 없어도 기본값으로 연다.
default persistent.room13_pw_controls_seen = False

init 351 python:
    def r13_pw_reveal_gate_statement():
        # 방금 들은 발언만 펼친다. 제출 자료·획득·기회는 손대지 않는다.
        claim="v111:함께 들어갈 근거를 고른다"
        views=dict(store.r13_pw_views or {})
        remembered=dict(views.get(claim,{}) or {})
        remembered["quote_open"]=True
        views[claim]=remembered
        store.r13_pw_views=views

    def r13_pw_active(key):
        return r13_v111_active() and (r13_pw_context(key) is not None or r13_case_hearing_spec(key) is not None)

    def r13_pw_quote_visible_now(key):
        spec=r13_pw_context(key)
        return r13_pw_quote_visible(spec,r13_has,r13_v111_value)

    def r13_pw_entries():
        """이번 회차에 보유한, 제시 적격인 자료. 물건(bag:/tool:)은 근거가 아니라 뺀다(hearing=True 와 같은 기준).
        서랍이 켜진 이야기(v111)는 결과 쪽지 접기를 그대로 따른다(접히는 쪽지는 제시에 쓰이지 않는 것만이다)."""
        keys=[k for k in r13_catalog_entries(False,True) if r13_catalog_can_present(k,True)]
        if r13_drawer_active():keys=r13_drawer_visible(keys)
        records=(store.room13 or {}).get("records",{}) or {}
        days=dict((k,(records.get(k) or {}).get("day")) for k in keys)
        return r13_pw_order(keys,days)

    def r13_pw_sections(tab,entries):
        """[(묶음 제목 또는 None, 자료 목록)]. 전체는 한 묶음, 보조 탭은 기존 서랍의 분류(새 사실을 더하지 않는다)."""
        if tab=="now" and r13_drawer_active():return [(None,r13_drawer_now(entries))]
        if tab=="past" and r13_drawer_active():
            return [(r13_drawer_case_title(case),keys) for case,keys in r13_drawer_cases(entries)]
        if tab=="person" and r13_drawer_active():
            return [(R13_NAMES.get(person,person),keys) for person,keys in r13_drawer_people(entries)]
        return [(None,list(entries))]

    def r13_pw_set_arguments(claim,chosen):
        # 기존 방식 그대로: room13 을 복사해 arguments 만 바꾼다. 보유 사실·기회·판정은 손대지 않는다.
        copy=winter_copy.deepcopy(store.room13)
        copy["arguments"][claim]=list(chosen)
        store.room13=copy
        # 호출 화면 안에서 체크한 묶음도 저장 직후 불러오기에 남긴다.
        renpy.retain_after_load()

    def r13_pw_submit_pair(claim,pair,mode):
        chosen=r13_pw_pair_submission(pair,r13_pw_entries(),mode)
        if chosen is None:return
        if r13_room_letters_begin_discovery(claim,chosen):return
        r13_pw_set_arguments(claim,chosen)
        renpy.end_interaction("argue")

    def r13_pw_submit_selected(claim):
        chosen=list((store.room13.get("arguments") or {}).get(claim,[]))
        if r13_room_letters_begin_discovery(claim,chosen):return
        renpy.end_interaction("argue")

    def r13_pw_toggle_action(claim,key,mode):
        persistent.room13_pw_controls_seen=True
        owned=r13_pw_entries()
        chosen=list((store.room13.get("arguments") or {}).get(claim,[]))
        new,pending=r13_pw_toggle(chosen,key,owned,mode)
        if pending:
            renpy.set_screen_variable("replace_pending",pending,screen="r13_proof_workspace")
        elif new!=chosen:
            r13_pw_set_arguments(claim,new)
        renpy.restart_interaction()

    def r13_pw_replace_action(claim,old,new):
        owned=r13_pw_entries()
        chosen=list((store.room13.get("arguments") or {}).get(claim,[]))
        r13_pw_set_arguments(claim,r13_pw_replace(chosen,old,new,owned))
        renpy.set_screen_variable("replace_pending",None,screen="r13_proof_workspace")
        renpy.restart_interaction()

    def r13_pw_remove_action(claim,key):
        chosen=list((store.room13.get("arguments") or {}).get(claim,[]))
        r13_pw_set_arguments(claim,r13_pw_remove(chosen,key))
        renpy.restart_interaction()

    def r13_pw_remember_pair(claim,pair):
        # D08: 관찰 뒤 대사를 보이고 돌아오면 같은 쌍이 펼쳐져 있어야 한다. 「목록으로」가 지운다.
        views=dict(store.r13_pw_views or {});row=dict(views.get(claim,{}));row["pair"]=tuple(pair) if pair else None;views[claim]=row;store.r13_pw_views=views
    def r13_pw_remember(claim,tab,detail,quote_open,view=None,pair=None,origin_open=False,hearing_target=None):
        views=dict(store.r13_pw_views or {})
        row=dict(views.get(claim,{}));row.update(tab=tab,detail=detail,quote_open=quote_open,view=view,pair=tuple(pair) if pair else None,origin_open=origin_open,hearing_target=hearing_target);views[claim]=row
        store.r13_pw_views=views

    def r13_pw_capture_view():
        # 화면을 닫기 전에 저장해도 읽던 방식과 발언이 이어지게 한다.
        screen=renpy.get_screen("r13_proof_workspace")
        if not screen or not screen.scope.get("ready"):return
        scope=screen.scope;claim=scope.get("claim")
        if not claim:return
        row=dict(tab=scope.get("tab"),detail=scope.get("detail"),quote_open=scope.get("quote_open",False),
                 view=scope.get("view"),pair=tuple(scope["pair"]) if scope.get("pair") else None,
                 origin_open=scope.get("origin_open",False),hearing_target=scope.get("hearing_target"))
        previous=(store.r13_pw_views or {}).get(claim,{})
        if all(previous.get(k)==v for k,v in row.items()):return
        r13_pw_remember(claim,**row)
        renpy.retain_after_load()

    config.interact_callbacks.append(r13_pw_capture_view)

    def r13_pw_open_detail(key):
        """이름은 읽기만 연다. 비교 자리 선택 중에는 그 자리만 채운다."""
        if key not in r13_pw_entries():return
        persistent.room13_pw_controls_seen=True
        screen=renpy.get_screen("r13_proof_workspace")
        if not screen:return
        slot=screen.scope.get("pick_slot")
        if slot in (0,1):
            pair=r13_pw_read_pair(screen.scope.get("pair"),key,slot)
            renpy.set_screen_variable("pair",pair,screen="r13_proof_workspace")
            renpy.set_screen_variable("view","pair",screen="r13_proof_workspace")
            renpy.set_screen_variable("pick_slot",None,screen="r13_proof_workspace")
        else:
            renpy.set_screen_variable("view","single",screen="r13_proof_workspace")
        renpy.set_screen_variable("detail",key,screen="r13_proof_workspace")
        renpy.set_screen_variable("origin_open",False,screen="r13_proof_workspace")
        if key in (store.room13 or {}).get("evidence",[]):r13_record_update_ui("seen",key,True)
        renpy.restart_interaction()

    def r13_pw_read_groups(key):
        """일반 기록과 같은 현재 변형의 사실을 읽는다. 기존 저장·호출 이름은 유지한다."""
        return r13_evidence_read_groups(key)

    def r13_pw_read_layout(title,quote_open,quote_text,compact=False):
        """수첩 종이 안의 제목·본문·하단을 계산한다. 긴 발언은 펼쳤을 때만 자리를 쓴다."""
        touch=r13_touch_ui();left=R13_NB_LEFT;width=R13_NB_WIDTH
        footer=r13_nb_footer_y();context_y=156 if touch else 144
        title_w=width
        title_h=r13_proof_text_size(title,r13_type("small" if compact else "emphasis"),title_w)[1]
        quote_h=(r13_pw_quote_height(quote_text,width-32)+24) if quote_open and quote_text else 0
        quote_y=context_y+max(36,title_h)+8
        top=quote_y+(quote_h+8 if quote_h else 0)
        return dict(touch=touch,left=left,right=R13_NB_RIGHT,width=width,top=R13_NB_TOP,
                    footer_y=footer,footer_h=r13_control_height(),context_y=context_y,title_w=title_w,
                    quote_y=quote_y,quote_h=quote_h,body_top=top,body_h=max(80,footer-12-top),
                    tab_h=88 if touch else 40,card_h=88 if touch else 80,cols=2 if touch else 3)

    def r13_pw_id(prefix,key):
        return prefix+str(key).replace("V111:","").replace(":","_")

    def r13_pw_card_height():
        # 72 는 「N일 · 장소」 꼬리표가 있던 때의 높이다. 꼬리표는 2026-10-29 소유자 「날짜 장소가 전혀 필요가 없을 듯」으로 뺐고,
        # 아래 붙임 판(dock)은 64 로 줄여 쓴다(r13_pw_layout).
        return 88 if r13_touch_ui() else (80 if persistent.room13_large_text else 72)

    def r13_pw_chip_height():
        return 64 if r13_touch_ui() else 40

    def r13_pw_tab_height():
        return 88 if r13_touch_ui() else 40

    def r13_pw_chip_fit(widths,label_w,more_w,width,gap=8):
        """(보일 칩 수). 순수 계산 — 칩 너비 목록과 앞 글자·「+N」 칩 너비로 한 줄에 들어갈 수를 센다.
        2026-10-28 꼼수 길 자동 주행: 자료를 일곱 개 넘게 고르면 칩이 오른쪽 틀 밖으로 잘렸다(숨은 가로 끌기).
        다 들어가면 전부, 아니면 「+N개」 칩 자리를 남기고 들어가는 만큼."""
        used=label_w
        if used+sum(w+gap for w in widths)<=width:return len(widths)
        n=0
        for w in widths:
            if used+gap+w+gap+more_w>width:break
            used+=gap+w;n+=1
        return n

    def r13_pw_chip_widths(chosen,short,small):
        def tw(t,size):
            return int(renpy.render(Text(t,font=R13_UI_BOLD_FONT,size=size),1280,100,0,0).get_size()[0])
        return [24+tw(r13_evidence_short(k,short),small)+10+tw("×",small+4) for k in chosen]

    def r13_pw_small():
        return r13_nb_small_size()

    def r13_pw_body():
        return r13_nb_body_size()

    def r13_pw_quote_height(text,width):
        return r13_proof_text_size(text,r13_nb_emphasis_size(),width)[1]

    # 2026-10-29 소유자 「자료 제시할 때 최대 상하 2줄이라 불편」 → B안 승인: 판을 위로 넓히고 세 줄 · 한 쪽에 12장.
    R13_PW_DOCK_PANEL=(50,96,1180,600)
    def r13_pw_layout(quote_open,quote_text,dock=False):
        """자리 계산. PC: 왼쪽 발언 열 · 가운데 목록 · 오른쪽 상세, 위에 탭 줄, 아래에 칩 줄과 버튼 줄.
        휴대폰: 위 한 줄(발언 접기 버튼 + 탭), 본문 한 영역(목록 또는 상세), 아래 칩 줄과 버튼 줄.
        전체 화면은 스크롤하지 않는다 — 목록·상세만 뷰포트다."""
        touch=r13_touch_ui()
        dock=dock and not touch
        L=dict(touch=touch,dock=dock,left=R13_NB_LEFT,right=R13_NB_RIGHT,width=R13_NB_WIDTH,top=R13_NB_TOP)
        L["footer_y"]=r13_nb_footer_y()
        L["chip_h"]=r13_pw_chip_height()
        L["chips_y"]=L["footer_y"]-(8 if touch else 12)-L["chip_h"]
        L["body_bottom"]=L["chips_y"]-8
        L["tab_h"]=r13_pw_tab_height()
        if touch:
            L["fold_w"]=372
            L["tab_x"]=L["left"]+L["fold_w"]+16
            L["tab_w"]=(L["right"]-L["tab_x"]-24)//4
            L["tab_gap"]=8
            qh=(r13_pw_quote_height(quote_text,L["width"]-32)+24) if (quote_open and quote_text) else 0
            L["quote_y"]=L["top"]+L["tab_h"]+8
            L["quote_h"]=qh
            L["body_top"]=L["quote_y"]+(qh+8 if qh else 0)
            L["list_x"]=L["left"];L["list_w"]=L["width"]
            L["detail_x"]=L["left"];L["detail_w"]=L["width"]
            L["cols"]=1 if persistent.room13_large_text else 2
        elif dock:
            # 2026-10-28 소유자 2안 승인: B안 판(아래 붙임)과 같은 자리·같은 모양. 머리(쟁점·발언 한 줄) 아래에 탭·목록·읽는 칸.
            P=R13_PW_DOCK_PANEL
            L["panel"]=P
            L["left"]=P[0]+48;L["right"]=P[0]+P[2]-28;L["width"]=L["right"]-L["left"];L["top"]=P[1]+22
            L["footer_y"]=P[1]+P[3]-20-r13_control_height()
            L["chips_y"]=L["footer_y"];L["body_bottom"]=L["footer_y"]-10
            L["quote_y"]=L["top"]+46;L["rule_y"]=L["top"]+84
            L["tab_y"]=L["top"]+96
            L["list_x"]=L["left"];L["list_w"]=640
            L["detail_x"]=L["left"]+664;L["detail_w"]=L["right"]-L["detail_x"]
            L["tab_x"]=L["list_x"];L["tab_w"]=0;L["tab_gap"]=6
            L["body_top"]=L["tab_y"]+L["tab_h"]+8
            L["cols"]=2
        else:
            L["quote_x"]=L["left"];L["quote_w"]=268
            L["list_x"]=424;L["list_w"]=340
            L["detail_x"]=788;L["detail_w"]=L["right"]-788
            L["tab_x"]=L["list_x"];L["tab_w"]=0;L["tab_gap"]=6
            L["body_top"]=L["top"]+L["tab_h"]+12
            L["cols"]=1
        L["body_h"]=max(60,L["body_bottom"]-L["body_top"])
        L["card_h"]=r13_pw_card_height()
        if dock:
            L["card_h"]=64   # 꼬리표를 뺐으니 이름 두 줄만 들어가면 된다. 64 면 한 쪽에 네 줄.
        return L

    def r13_pw_tab_boxes(L):
        """탭 칩의 (x, 폭). PC 는 글자 길이대로, 휴대폰은 네 칸 균등."""
        small=r13_pw_small()
        out=[];x=L["tab_x"]
        for key,title in R13_PW_TABS:
            w=L["tab_w"] or (len(title)*small+22)
            out.append((key,title,x,w));x+=w+L["tab_gap"]
        return out

    def r13_pw_help(mode,chances,count):
        if mode=="compare":
            return "「나란히 읽기」에서 두 자료를 고른 뒤 「이 두 장 비교」를 누른다. 돌아가려면 「조사 계속」."
        # 2026-10-29 눈가림 플레이: 1일 돌목 회의에서 한 장씩만 내다 다 틀렸고, 여러 장을 함께 낼 수 있다는 것은
        # 기록의 「나란히 놓기」를 보고서야 짐작했다. 몇 장인지는 말하지 않고, 함께 고를 수 있다는 것만 알린다.
        if not count:
            return "체크로 근거를 고르세요. 여러 장을 함께 고를 수 있습니다. 이름을 누르면 오른쪽에서 읽습니다."
        if chances:
            return "더 고를 수도 있습니다. 다 골랐으면 「근거 제시」(틀리면 기회 1회)."
        return "더 고를 수도 있습니다. 다 골랐으면 「근거 제시」를 누릅니다."

# 체크 상자: 선택은 체크 + 테두리로 보인다(색만으로 구별하지 않는다). 새 재질 없이 잉크 선과 크림 면.
screen r13_pw_checkbox(on,size=30):
    frame:
        xysize (size,size) padding (2,2) background Solid(r13_nb_accent() if on else r13_nb_ink()) align (.5,.5)
        frame:
            xysize (size-4,size-4) padding (0,0) background Solid("#f5ecd9")
            if on:
                text "✓" align (.5,.5) size (size-8) color r13_nb_accent() font R13_UI_BOLD_FONT

# 자료 한 장: 왼쪽 체크 영역(선택), 나머지(그림·이름)는 상세를 읽는 영역. 둘은 시각적으로 갈라져 있다.
screen r13_pw_card(claim,key,mode,w,h,chosen,is_detail,ready,close_on_open=None):
    $ check_w=88 if r13_touch_ui() else 56
    $ thumb=h-28
    $ name_w=w-check_w-thumb-30
    # 64 칸(세 줄 목록)에서는 이름 두 줄이 테두리에 붙지 않게 한 단계 작게.
    $ label_size=r13_type("body")
    frame:
        xysize (w,h) padding (0,0) background (Solid(r13_nb_accent()) if chosen else (Solid("#c9a86a99") if is_detail else None))
        frame:
            xpos 3 ypos 3 xysize (w-6,h-6) padding (0,0) background r13_field_paper()
            button:
                id r13_pw_id("r13_pw_check_",key)
                xpos 0 ypos 0 xysize (check_w,h-6) padding (0,0) background None hover_background Solid("#8d4b2d14")
                action Function(r13_pw_toggle_action,claim,key,mode) sensitive ready
                alt (("선택 해제 · " if chosen else "선택 · ")+r13_catalog_title(key))
                use r13_pw_checkbox(chosen,40 if r13_touch_ui() else 30)
            add Solid("#c9a86a66") xpos check_w ypos 8 xsize 1 ysize (h-22)
            button:
                id r13_pw_id("r13_pw_open_",key)
                xpos (check_w+1) ypos 0 xysize (w-6-check_w-1,h-6) padding (0,0) background None hover_background Solid("#8d4b2d14")
                action ([Hide(close_on_open),Function(r13_pw_open_detail,key)] if close_on_open else Function(r13_pw_open_detail,key)) sensitive ready
                alt ("읽기 · "+r13_catalog_title(key))
                fixed:
                    xysize (w-6-check_w-1,h-6)
                    add r13_evidence_picture(key,thumb) xpos 8 yalign .5
                    $ name=r13_ev_two_lines(r13_catalog_title(key),name_w,label_size,2)
                    vbox:
                        xpos (thumb+18) yalign .5 spacing 1
                        text name xsize name_w size label_size color r13_nb_ink() font R13_UI_BOLD_FONT line_spacing -1

screen r13_pw_selected_materials(claim,mode):
    modal True
    zorder 70
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    default selected_page=0
    $ owned=r13_pw_entries()
    $ selected=[k for k in room13.get("arguments",{}).get(claim,[]) if k in owned]
    $ selected_page=min(selected_page,max(0,(len(selected)-1)//3))
    $ small=r13_type("small")
    $ footer=r13_nb_footer_y()
    use r13_notebook_shell("선택한 자료",close_action=Hide("r13_pw_selected_materials"),rule_y=132)
    text "체크는 선택 해제 · 이름은 내용 읽기" xpos R13_NB_LEFT ypos 150 size small color r13_nb_muted() font R13_UI_FONT
    for index,item in enumerate(selected[selected_page*3:selected_page*3+3]):
        fixed:
            xpos R13_NB_LEFT ypos (196+index*100) xysize (R13_NB_WIDTH,88)
            use r13_pw_card(claim,item,mode,R13_NB_WIDTH,88,True,False,ready,close_on_open="r13_pw_selected_materials")
    if not selected:
        text "선택한 자료가 없습니다." xpos R13_NB_LEFT ypos 212 size r13_type("emphasis") color r13_nb_ink() font R13_UI_FONT
    if len(selected)>3:
        for index,(caption,target,enabled) in enumerate((("‹",selected_page-1,selected_page>0),("›",selected_page+1,(selected_page+1)*3<len(selected)))):
            fixed:
                xpos (R13_NB_LEFT+index*94) ypos footer xysize (82,r13_control_height())
                use r13_control(caption,None,SetScreenVariable("selected_page",target),enabled=ready and enabled,width=82,control_id=("r13_pw_selected_prev" if index==0 else "r13_pw_selected_next"))
    text ("%d장 선택 · %d / %d쪽"%(len(selected),selected_page+1,max(1,(len(selected)+2)//3))) xpos 340 ypos (footer+14) size small color r13_nb_muted() font R13_UI_FONT
    fixed:
        xpos 966 ypos footer xysize (240,r13_control_height())
        use r13_control("돌아가기",None,Hide("r13_pw_selected_materials"),enabled=ready,width=240,control_id="r13_pw_selected_close")
    key "game_menu" action Hide("r13_pw_selected_materials")

# 열어 본 자료 상세: 기존 부품(제목 꼬리표·그림 상자·관찰 사실·쪽지)을 다시 쓴다. 긴 원문은 「출처 펼치기」 안.
screen r13_pw_detail(claim,key,mode,x,y,w,h,origin_open,can_pair,ready):
    $ small=r13_pw_small()
    $ bh=r13_ev_button_height()
    $ inner=w-24
    $ pic=min(inner,64 if not r13_touch_ui() else 32)
    # 읽기 조작(출처 펼치기·나란히 놓기)은 뷰포트 밖 아래 한 줄에 고정한다 — 긴 상세에서 스크롤 끝까지 내려가야 보이면 안 된다.
    $ buttons=[("출처 접기" if origin_open else "출처 펼치기",SetScreenVariable("origin_open",not origin_open),"r13_pw_origin")]
    if can_pair:
        # 일반 proof 의 읽기용 나란히 놓기. 제출 묶음은 그대로다(D03·T09).
        $ buttons.append(("⇆ 나란히 놓기",[SetScreenVariable("pair",(key,None)),SetScreenVariable("detail",None)],"r13_pw_pair"))
    if r13_touch_ui():
        $ buttons.append(("그림 확대",Show("r13_pw_picture",key=key),"r13_pw_enlarge"))
    $ bw=(w-8*(len(buttons)-1))//len(buttons)
    for index,(caption,action,control_id) in enumerate(buttons):
        fixed:
            xpos (x+index*(bw+8)) ypos (y+h-bh) xysize (bw,bh)
            use r13_control(caption,None,action,enabled=ready,width=bw,height=bh,label_size=r13_ev_label_size(caption,bw),control_id=control_id)
    viewport:
        id "r13_pw_detail"
        area (x,y,w,h-bh-8) mousewheel True draggable True scrollbars "vertical"
        vscrollbar_unscrollable "hide"
        vbox:
            xsize inner spacing 10
            # 그림과 제목은 작은 머리글, 관찰 사실은 그 아래 전체 폭으로 읽는다.
            hbox:
                spacing 14
                if r13_touch_ui():
                    fixed:
                        xysize (pic,pic)
                        use r13_evidence_picture_box(key,pic)
                else:
                    button:
                        xysize (pic,pic) padding (0,0) background None
                        action Show("r13_pw_picture",key=key) alt "자료 그림 확대"
                        use r13_evidence_picture_box(key,pic)
                use r13_evidence_heading(key,inner-pic-14,(r13_nb_heading_size()))
            use r13_evidence_fact_list(key,inner)
            if r13_drawer_active():
                use r13_drawer_note_blocks(key,inner)
            if origin_open:
                $ ev=r13_catalog_record(key)
                text ("들은 말" if ev.get("kind")=="증언" else "확인한 내용") size small color r13_nb_accent() font R13_UI_BOLD_FONT
                text r13_material_body(ev) size r13_ev_fact_size() color r13_nb_ink() font R13_UI_BOLD_FONT xsize inner
                text r13_catalog_origin(key) size small color r13_nb_muted() font R13_UI_BOLD_FONT xsize inner
                if key in room13.get("records",{}):
                    text ("얻은 곳: "+r13_record_source_label(key)) size small color r13_nb_muted() font R13_UI_BOLD_FONT xsize inner

# 두 자료를 나란히: 같은 폭 두 열, 각 열만 스크롤. 맞는지 아닌지는 표시하지 않는다.
# 두 편지 관찰: 작은 그림 위에 글자를 겹치지 않고, 두 편지가 공유하는 한 줄의 네 버튼으로 부분을 고른다.
# 하나를 고르면 기존 ("observe",구역)을 돌려준다. 정답 구역을 미리 강조하지 않고 기회를 쓰지 않는다.
init 350 python:
    R13_PW_OBSERVE_KEY="두 편지를 나란히 본다"
    def r13_pw_observe_spots(width,height=64):
        names=(("head","머리글"),("body","본문"),("tail","끝부분"),("margin","여백"))
        return [(key,name,(i*(width+8)//4,0,(i+1)*(width+8)//4-i*(width+8)//4-8,height))
                for i,(key,name) in enumerate(names)]
    # 2026-10-29 피드백 M: 나란히 보기에서 편지 두 장이 종이 그림과 요약(「…라고 적혔다」)으로만 보여, 「직접 읽고 견준다」는
    # 안내와 달리 원문이 앞에 없었다. 편지·메모처럼 글 자체가 자료인 것은 원문을 제목 바로 아래 먼저 보이고 그림은 그 아래에 둔다.
    # 맞는지 아닌지는 여전히 표시하지 않는다.
    R13_PW_ORIGINAL_FIRST=("V111:E01","V111:E06","V111:E27")
    def r13_pw_observe_available(key,pair):
        return key==R13_PW_OBSERVE_KEY and bool(pair) and len(pair)==2 and set(pair)=={"V111:E01","V111:E06"}

screen r13_pw_document_original(key,width,inspect=False,ready=True):
    $ document=r13_room_document_original(key)
    vbox:
        xsize width spacing 6
        text "원문" size r13_pw_small() color r13_nb_accent() font R13_UI_BOLD_FONT
        text document["text"] size r13_ev_fact_size() color r13_nb_ink() font R13_UI_BOLD_FONT xsize width
        if key in ("V111:E01","V111:E06"):
            $ tail_h=88 if inspect and r13_touch_ui() else 52
            if inspect:
                button:
                    id r13_pw_id("r13_pw_document_tail_",key)
                    xysize (width,tail_h) padding (0,0)
                    background None hover_background Solid("#c9a86a22")
                    action Return(("observe","tail")) sensitive ready
                    alt (r13_catalog_title(key)+" · 끝부분 살펴보기")
                    if document["mark"]:
                        add Transform(document["mark"],xysize=(48,48),nearest=True) xpos 8 ypos ((tail_h-48)//2)
            else:
                fixed:
                    xsize width ysize tail_h
                    if document["mark"]:
                        add Transform(document["mark"],xysize=(48,48),nearest=True) xpos 8 ypos 0

screen r13_pw_pair(pair,x,y,w,h,observe=False,ready=True):
    $ small=r13_pw_small()
    $ col_w=(w-16)//2
    $ inner=col_w-24
    $ pic=min(inner,160 if not r13_touch_ui() else 110)
    $ title_size=r13_nb_heading_size()
    $ observe_h=88 if r13_touch_ui() else 64
    $ observe_panel_h=observe_h if observe else 0
    $ observe_gap=12 if observe else 0
    text ("두 편지에서 함께 살펴볼 부분을 고르세요." if observe else "나란히 놓기 · 두 자료를 함께 봅니다. 맞는지 아닌지는 표시하지 않습니다.") xpos x ypos y xsize w size small color r13_nb_muted() font R13_UI_BOLD_FONT
    $ top=y+small+10
    add Solid("#c9a86a66") xpos (x+col_w+8) ypos top xsize 1 ysize (h-(top-y)-observe_panel_h-observe_gap)
    for column,key in enumerate((tuple(pair)+(None,None))[:2]):
        viewport:
            id ("r13_pw_pair_%d"%column)
            area ((x if column==0 else x+col_w+16),top,col_w,h-(top-y)-observe_panel_h-observe_gap)
            mousewheel True draggable True scrollbars "vertical"
            vscrollbar_unscrollable "hide"
            vbox:
                xsize inner spacing 8
                if key is not None:
                    use r13_evidence_heading(key,inner,title_size)
                    if key in R13_PW_ORIGINAL_FIRST:
                        use r13_pw_document_original(key,inner,inspect=observe,ready=ready)
                    fixed:
                        xsize inner ysize pic
                        fixed:
                            xpos ((inner-pic)//2) xysize (pic,pic)
                            use r13_evidence_picture_box(key,pic)
                    use r13_evidence_fact_list(key,inner)
                else:
                    text ("%d번 자리"%(column+1)) size title_size color r13_nb_muted() font R13_UI_BOLD_FONT
                    text "목록에서 함께 볼 자료의 이름을 누르세요." size r13_ev_fact_size() color r13_nb_muted() font R13_UI_BOLD_FONT xsize inner
    if observe:
        fixed:
            xpos x ypos (y+h-observe_panel_h) xysize (w,observe_panel_h)
            for spot_id,spot_name,(sx,sy,sw,sh) in r13_pw_observe_spots(w,observe_h):
                fixed:
                    area (sx,sy,sw,sh)
                    use r13_control(spot_name,None,Return(("observe",spot_id)),enabled=ready,width=sw,height=sh,label_size=r13_type("emphasis" if r13_touch_ui() else "body"),control_id=r13_pw_id("r13_pw_spot_0_",spot_id))

# 고른 자료 칩 줄. × 로 그 선택만 해제한다. compare 에서 셋째를 고르면 여기서 바꿀 자리를 고른다.
screen r13_pw_chips(claim,chosen,mode,L,replace_pending,ready):
    $ small=r13_pw_small()
    $ ch=L["chip_h"]
    $ short=10 if L["touch"] else 12
    $ label=(("고른 자료 %d"%len(chosen)) if chosen else ("고른 자료 없음 · 체크로 여러 장 고릅니다" if not L["touch"] else "고른 자료 없음"))
    $ fit=(len(chosen) if replace_pending else r13_pw_chip_fit(r13_pw_chip_widths(chosen,short,small),r13_proof_text_size(label,small)[0],24+r13_proof_text_size("+%d개"%len(chosen),small)[0],L["width"]))
    fixed:
        area (L["left"],L["chips_y"],L["width"],ch)
        hbox:
            spacing 8 ysize ch
            if replace_pending:
                text ("「"+r13_evidence_short(replace_pending,short)+"」와 바꿀 자료:") size small color r13_nb_accent() font R13_UI_BOLD_FONT yalign .5
                for key in chosen:
                    button:
                        id r13_pw_id("r13_pw_swap_",key)
                        ysize ch padding (12,0) background r13_field_paper() hover_background r13_field_paper(hover=True)
                        action Function(r13_pw_replace_action,claim,key,replace_pending) sensitive ready alt ("바꾸기 · "+r13_catalog_title(key))
                        text (r13_evidence_short(key,short)+"  ⇆") size small color r13_nb_ink() font R13_UI_BOLD_FONT yalign .5
                button:
                    id "r13_pw_swap_cancel"
                    ysize ch padding (12,0) background r13_field_paper() hover_background r13_field_paper(hover=True)
                    action SetScreenVariable("replace_pending",None) sensitive ready alt "취소"
                    text "취소" size small color r13_nb_muted() font R13_UI_BOLD_FONT yalign .5
            else:
                text label size small color r13_nb_muted() font R13_UI_BOLD_FONT yalign .5
                for key in chosen[:fit]:
                    button:
                        id r13_pw_id("r13_pw_chip_",key)
                        ysize ch padding (12,0) background r13_field_paper() hover_background r13_field_paper(hover=True)
                        action Function(r13_pw_remove_action,claim,key) sensitive ready alt ("선택 해제 · "+r13_catalog_title(key))
                        hbox:
                            spacing 10 yalign .5
                            text r13_evidence_short(key,short) size small color r13_nb_ink() font R13_UI_BOLD_FONT yalign .5
                            text "×" size (small+4) color r13_nb_accent() font R13_UI_BOLD_FONT yalign .5
                if fit<len(chosen):
                    # 넘친 칩은 「+N개」 하나로. 빼려면 목록의 체크를 다시 누른다.
                    frame:
                        id "r13_pw_chip_more" ysize ch padding (12,0) background r13_field_paper()
                        text ("+%d개"%(len(chosen)-fit)) size small color r13_nb_muted() font R13_UI_BOLD_FONT yalign .5

# 읽는 화면과 제출할 묶음은 독립이다. 문서는 원문, 물증은 관찰 사실을 먼저 읽으며 판단 함수는 호출하지 않는다.
screen r13_pw_read_card(key,x,y,w,h,origin_open,ready,slot=None,inspect=False):
    $ inner=w-32
    frame:
        area (x,y,w,h) padding (1,1) background Solid("#c9a86a")
        frame:
            xfill True yfill True padding (15,12) background Solid("#f5ecd9")
            viewport:
                id ("r13_pw_read_"+str(slot) if slot is not None else "r13_pw_detail")
                xysize (inner,h-26) mousewheel True draggable True scrollbars "vertical"
                vscrollbar_unscrollable "hide"
                vbox:
                    xsize (inner-12) spacing 8
                    if key:
                        button:
                            id ("r13_pw_change_%d"%slot if slot is not None else "r13_pw_single_picture")
                            xsize (inner-12) yminimum 48 padding (0,0) background None hover_background Solid("#c9a86a22")
                            action ([SetScreenVariable("pick_slot",slot),SetScreenVariable("view","list")] if slot is not None else Show("r13_pw_picture",key=key)) sensitive ready
                            alt (("%d번 자료 변경 · "%(slot+1)) if slot is not None else "자료 그림 확대 · ")+r13_catalog_title(key)
                            hbox:
                                spacing 12
                                text r13_catalog_title(key) size r13_type("title") color r13_nb_ink() font R13_UI_BOLD_FONT xsize (inner-112 if slot is not None else inner-64)
                                if slot is not None:
                                    text "변경" size r13_type("small") color r13_nb_accent() font R13_UI_FONT yalign .5
                                else:
                                    add r13_evidence_picture(key,32) yalign .5
                        if key in R13_PW_ORIGINAL_FIRST:
                            use r13_pw_document_original(key,inner-12,inspect=inspect,ready=ready)
                        else:
                            use r13_evidence_read_facts(key,inner-12)
                        if r13_drawer_active():
                            use r13_drawer_note_blocks(key,inner-12)
                        if origin_open:
                            add Solid("#c9a86a99") xsize (inner-12) ysize 1
                            text "출처와 전체 내용" size r13_type("small") color r13_nb_accent() font R13_UI_BOLD_FONT
                            if key in R13_PW_ORIGINAL_FIRST:
                                # 같은 글을 다시 풀어 쓴 요약 때문에 원문·표식이 밀리지 않게 한다.
                                use r13_evidence_read_facts(key,inner-12)
                            else:
                                text r13_material_body(r13_catalog_record(key)) size r13_ev_fact_size() color r13_nb_ink() font R13_UI_FONT xsize (inner-12)
                            text r13_catalog_origin(key) size r13_type("small") color r13_nb_muted() font R13_UI_FONT xsize (inner-12)
                            if key in room13.get("records",{}):
                                text ("얻은 곳: "+r13_record_source_label(key)) size r13_type("small") color r13_nb_muted() font R13_UI_FONT xsize (inner-12)
                    else:
                        text ("%d번 자료"%(slot+1)) size r13_type("title") color r13_nb_muted() font R13_UI_BOLD_FONT
                        text "함께 읽을 자료를 목록에서 고르세요." size r13_type("emphasis") color r13_nb_ink() font R13_UI_FONT xsize (inner-12)
    if slot is not None and key is None:
        fixed:
            xpos (x+16) ypos (y+140) xysize (240,88)
            use r13_control("자료 고르기",None,[SetScreenVariable("pick_slot",slot),SetScreenVariable("view","list")],enabled=ready,width=240,height=88,control_id=("r13_pw_pick_%d"%slot))

screen r13_proof_workspace(claim,key,can_press=False,investigate=False,chances=None,hearing_only=False):
    style_prefix "r13"
    modal True
    zorder 50
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    $ ctx=r13_pw_context(key,gate_application_acknowledged=bool(r13_v111_value("gate_application_acknowledged"))) or dict(mode="proof",speaker=None,quote=None,quote_when=None)
    $ mode=ctx["mode"]
    $ hearing_rows=r13_case_hearing_rows(key)
    # 현재 발언을 건너뛴 구간은 기존 제시 조작으로 풀 수 있어야 한다.
    $ hearing_rows=hearing_rows if any(r["key"]==key for r in hearing_rows) else []
    $ remembered=(r13_pw_views or {}).get(claim,{})
    default tab=remembered.get("tab",("now" if hearing_rows and r13_drawer_now(r13_pw_entries()) else r13_pw_initial_tab(mode,r13_drawer_active(),r13_pw_entries(),r13_drawer_now(r13_pw_entries()))))
    default detail=remembered.get("detail")
    default pair=remembered.get("pair")
    default view=r13_pw_initial_view(mode,len(hearing_rows),remembered.get("view"),pair,detail,hearing_only)
    default hearing_target=remembered.get("hearing_target") if any(r["target"]==remembered.get("hearing_target") for r in hearing_rows) else next((r["target"] for r in hearing_rows if r["key"]==key),None)
    $ view="list" if view=="statements" and not hearing_rows else view
    default quote_open=remembered.get("quote_open",bool(hearing_rows) and mode!="compare")
    default origin_open=remembered.get("origin_open",False)
    default page=0
    default hearing_page=next((i//r13_pw_hearing_geometry(r13_touch_ui())["per_page"] for i,r in enumerate(hearing_rows) if r["target"]==hearing_target),0)
    default pick_slot=None
    default observe=bool(remembered.get("room_letters_discovery")) and r13_room_letters_discovery_needed(key)
    default replace_pending=None
    on "hide" action Function(r13_pw_remember,claim,tab,detail,quote_open,view,pair,origin_open,hearing_target)
    $ owned=r13_pw_entries()
    $ stored=list(room13["arguments"].get(claim,[]))
    $ chosen=[k for k in stored if k in owned]
    $ detail=detail if detail in owned else None
    $ pair=r13_pw_pair_live(pair,owned)
    $ live_pair=(tuple(pair or ())+(None,None))[:2]
    $ pair_open=view=="pair" and None not in live_pair
    $ replace_pending=replace_pending if replace_pending in owned and mode=="compare" else None
    $ hearing_row=next((r for r in hearing_rows if r["target"]==hearing_target),None)
    $ hearing_kind=(hearing_row or {}).get("kind","statement")
    $ quote_text=hearing_row["text"] if hearing_row else ctx["quote"] if not r13_case_hearing_spec(key) and ctx["quote"] and r13_pw_quote_visible_now(key) else None
    $ quote_speaker=R13_NAMES.get(hearing_row["speaker"],hearing_row["speaker"]) if hearing_row else ctx["speaker"]
    $ layout_quote=(((quote_speaker+"  ") if quote_speaker else "")+quote_text) if quote_text else None
    $ title=R13_PROOF_TITLES.get(key,key)
    $ small=r13_type("small")
    $ ink=r13_nb_ink()
    $ muted=r13_nb_muted()
    $ accent=r13_nb_accent()
    $ can_review=bool(r13_pw_review_target(key,"investigate" if investigate else None))
    $ review_action=Return("investigate") if can_review else None
    $ pair_submission=r13_pw_pair_submission(live_pair,owned,mode) if view=="pair" else None
    $ discovery_pending=r13_room_letters_discovery_pending(key,pair_submission or chosen)
    $ room_letters_copy=r13_pw_room_letters_copy(key,pair_submission or chosen,r13_room_letters_discovery_needed(key),r13_v111_value("letter_tail_observed") is True,inquiry=bool(r13_v111_value("letter_inquiry_mode138")))
    # 첫 방은 두 문서의 제목이 이미 각 열에 있다. 쟁점·조작 안내를 두 줄로 반복하지 않는다.
    $ compact_context=bool(room_letters_copy and not quote_open)
    $ context_text=room_letters_copy[1] if compact_context else (hearing_row["title"] if hearing_row else title)
    $ L=r13_pw_read_layout(context_text,quote_open and view!="statements",layout_quote,compact=compact_context)
    $ touch=L["touch"]
    $ hearing_geometry=r13_pw_hearing_geometry(touch)
    use r13_notebook_shell("자료 대조" if mode=="compare" else "질문 검토" if hearing_rows and hearing_kind=="question" else "발언 검증" if hearing_rows else "자료 대조",close_action=(Return("hearing_resume") if hearing_only else review_action),rule_y=(148 if touch else 128))
    if can_review:
        key "game_menu" action review_action
    if chances:
        text chances.replace("회의 기회","기회") xpos R13_NB_TITLE_X ypos (108 if touch else 104) xsize 370 size small color muted font R13_UI_BOLD_FONT
    fixed:
        xpos 500 ypos 54 xysize (208,88 if touch else 64)
        use r13_control((("질문 다시 읽기" if hearing_kind=="question" else "발언 다시 읽기") if len(hearing_rows)==1 else ("확인할 질문" if hearing_kind=="question" else "발언 목록")) if hearing_rows else "한 장만 보기",None,[SetScreenVariable("view","statements")] if hearing_rows else [SetScreenVariable("detail",detail or (live_pair[0] if live_pair[0] else (owned[0] if owned else None))),SetScreenVariable("view","single"),SetScreenVariable("pick_slot",None),SetScreenVariable("observe",False)],enabled=ready and bool(owned),chosen=view==("statements" if hearing_rows else "single"),width=208,height=(88 if touch else 64),label_size=r13_type("body"),control_id="r13_pw_single")
    if not hearing_only:
        fixed:
            xpos 724 ypos 54 xysize (240,88 if touch else 64)
            use r13_control("자료 목록" if view=="statements" else "나란히 읽기",None,[SetScreenVariable("view","list")] if view=="statements" else [SetScreenVariable("pair",r13_pw_pair_on_open(chosen,pair,detail,owned)),SetScreenVariable("view","pair"),SetScreenVariable("pick_slot",None)],enabled=ready and len(owned)>1,chosen=view=="pair",width=240,height=(88 if touch else 64),label_size=r13_type("body"),control_id="r13_pw_pair")
    text context_text xpos L["left"] ypos L["context_y"] xsize L["title_w"] size (small if compact_context else r13_type("emphasis")) color (accent if compact_context else ink) font R13_UI_BOLD_FONT
    if quote_text and view!="statements":
        fixed:
            xpos 982 ypos 54 xysize (176,64 if not touch else 88)
            use r13_control(("안내 접기" if quote_open else "비교 안내") if mode=="compare" else (("질문 접기" if quote_open else "질문 보기") if hearing_kind=="question" else ("발언 접기" if quote_open else "발언 보기")),None,ToggleScreenVariable("quote_open"),enabled=ready,width=176,height=(64 if not touch else 88),label_size=small,control_id="r13_pw_fold")
    if quote_open and layout_quote and view!="statements":
        frame:
            area (L["left"],L["quote_y"],L["width"],L["quote_h"]) padding (16,10) background r13_field_paper()
            text layout_quote id "r13_pw_quote_text" size r13_type("emphasis") color ink font R13_UI_FONT xsize (L["width"]-32)
    if room_letters_copy and not compact_context:
        text room_letters_copy[1] xpos L["left"] ypos L["body_top"] xsize L["width"] size small color accent font R13_UI_BOLD_FONT
        # 안내 한 줄의 높이를 본문에서 빼서 문서·관찰 버튼과 겹치지 않게 한다.
        $ L=dict(L,body_top=L["body_top"]+small+10,body_h=max(60,L["body_h"]-small-10))
    $ sections=r13_pw_sections(tab,owned)
    $ pages=[[]]
    if view=="statements":
        text (("질문을 다시 읽거나 더 확인할 수 있습니다." if hearing_kind=="question" else "발언을 다시 읽거나 되물을 수 있습니다.") if len(hearing_rows)==1 else ("자료로 답할 질문을 고르세요." if hearing_kind=="question" else "누구의 어떤 말을 확인할까요?")) xpos L["left"] ypos L["body_top"] size small color muted font R13_UI_FONT
        $ hearing_page=min(hearing_page,max(0,(len(hearing_rows)-1)//hearing_geometry["per_page"]))
        $ hearing_per_page=hearing_geometry["per_page"]
        $ hearing_visible=hearing_rows[hearing_page*hearing_per_page:(hearing_page+1)*hearing_per_page]
        for hi,row in enumerate(hearing_visible):
            fixed:
                xpos L["left"] ypos (L["body_top"]+40+hi*(hearing_geometry["height"]+hearing_geometry["gap"])) xysize (420,hearing_geometry["height"])
                use r13_control(R13_NAMES.get(row["speaker"],row["speaker"])+" · "+row["title"],None,[SetScreenVariable("hearing_target",row["target"]),SetScreenVariable("quote_open",True)],enabled=ready,chosen=hearing_target==row["target"],width=420,height=hearing_geometry["height"],label_size=small,control_id=("r13_hearing_target_"+row["target"]))
        if hearing_row:
            frame:
                area (L["left"]+440,L["body_top"]+40,L["width"]-440,L["body_h"]-40) padding (20,18) background r13_field_paper()
                vbox:
                    spacing 16
                    text quote_speaker size r13_type("emphasis") color accent font R13_UI_BOLD_FONT
                    text quote_text id "r13_hearing_quote" size r13_type("body") color ink font R13_UI_FONT xsize (L["width"]-480)
    elif view=="list":
        $ tab_w=170 if touch else 140
        for ti,(tab_key,tab_title) in enumerate(R13_PW_TABS):
            fixed:
                xpos (L["left"]+ti*(tab_w+8)) ypos L["body_top"] xysize (tab_w,L["tab_h"])
                use r13_control(tab_title,None,[SetScreenVariable("tab",tab_key),SetScreenVariable("page",0)],enabled=ready,chosen=tab==tab_key,width=tab_w,height=L["tab_h"],label_size=small,control_id=("r13_pw_tab_"+tab_key))
        $ tip_h=(small+12) if pick_slot is not None or not persistent.room13_pw_controls_seen else 0
        if tip_h:
            text ((("왼쪽" if pick_slot==0 else "오른쪽")+"에 읽을 자료의 이름을 누르세요.") if pick_slot is not None else "체크는 선택 · 이름은 내용 읽기") xpos L["left"] ypos (L["body_top"]+L["tab_h"]+8) size small color muted font R13_UI_FONT
        $ list_y=L["body_top"]+L["tab_h"]+8+tip_h
        $ list_h=L["body_h"]-L["tab_h"]-8-tip_h
        $ card_w=(L["width"]-8*(L["cols"]-1))//L["cols"]
        $ pages=r13_pw_pages(sections,L["cols"],list_h,L["card_h"],small+6,8,0)
        $ page=min(page,len(pages)-1)
        text ("%d / %d쪽"%(page+1,len(pages))) xpos L["right"] xanchor 1.0 ypos (L["body_top"]+12) size small color muted font R13_UI_BOLD_FONT
        fixed:
            id "r13_pw_list"
            area (L["left"],list_y,L["width"],list_h)
            vbox:
                spacing 8 xsize L["width"]
                for kind,value in pages[page]:
                    if kind=="header":
                        text value size small color accent font R13_UI_BOLD_FONT xsize L["width"]
                    else:
                        hbox:
                            spacing 8
                            for k in value:
                                use r13_pw_card(claim,k,mode,card_w,L["card_h"],k in chosen,k==detail,ready)
                if not any(keys for _,keys in sections):
                    text ("아직 모은 자료가 없습니다." if not owned else "이 분류에는 자료가 없습니다.") size small color muted font R13_UI_FONT xsize L["width"]
    elif view=="pair":
        if observe and r13_pw_observe_available(key,live_pair):
            use r13_pw_pair(live_pair,L["left"],L["body_top"],L["width"],L["body_h"],True,ready)
        else:
            $ col=(L["width"]-24)//2
            for slot,k in enumerate(live_pair):
                use r13_pw_read_card(k,L["left"]+slot*(col+24),L["body_top"],col,L["body_h"],origin_open,ready,slot,inspect=r13_pw_observe_available(key,live_pair))
    elif detail:
        use r13_pw_read_card(detail,L["left"],L["body_top"],L["width"],L["body_h"],origin_open,ready)
    else:
        text "목록에서 읽을 자료의 이름을 누르세요." xpos L["left"] ypos L["body_top"] size r13_type("emphasis") color muted font R13_UI_FONT
    # 목록 쪽 넘김은 아래 고정한다. 이름으로 읽은 뒤에도 체크한 묶음은 그대로다.
    if view=="statements":
        if len(hearing_rows)>(3 if touch else 4):
            for bi,(caption,target,cid,enabled) in enumerate((("‹",hearing_page-1,"r13_hearing_prev",hearing_page>0),("›",hearing_page+1,"r13_hearing_next",(hearing_page+1)*(3 if touch else 4)<len(hearing_rows)))):
                fixed:
                    xpos (L["left"]+bi*94) ypos L["footer_y"] xysize (82,L["footer_h"])
                    use r13_control(caption,None,SetScreenVariable("hearing_page",target),enabled=ready and enabled,width=82,control_id=cid)
    elif view=="list":
        for bi,(caption,target,cid,enabled) in enumerate((("‹",page-1,"r13_pw_prev",page>0),("›",page+1,"r13_pw_next",page<len(pages)-1))):
            fixed:
                xpos (L["left"]+bi*94) ypos L["footer_y"] xysize (82,L["footer_h"])
                use r13_control(caption,None,SetScreenVariable("page",target),enabled=ready and enabled,width=82,control_id=cid)
    else:
        fixed:
            xpos L["left"] ypos L["footer_y"] xysize (176,L["footer_h"])
            use r13_control("목록",None,[SetScreenVariable("view","list"),SetScreenVariable("observe",False),SetScreenVariable("pick_slot",None)],enabled=ready,width=176,control_id="r13_pw_back_list")
    if view!="statements" and chosen and not pair_submission and not hearing_only:
        fixed:
            xpos 324 ypos L["footer_y"] xysize (144,L["footer_h"])
            use r13_control("%d장 선택\n모아보기"%len(chosen),None,Show("r13_pw_selected_materials",claim=claim,mode=mode),enabled=ready,width=144,label_size=small,control_id="r13_pw_selected")
    else:
        vbox:
            xpos 324 ypos (L["footer_y"]+6) xsize 144 spacing 2
            text (("질문 읽기" if hearing_kind=="question" else "발언 읽기") if view=="statements" and len(hearing_rows)==1 else ("질문 선택" if hearing_kind=="question" else "발언 선택") if view=="statements" else "2장 읽기" if pair_submission else "%d장 선택"%len(chosen)) size small color ink font R13_UI_BOLD_FONT
            text (("%d / %d쪽"%(hearing_page+1,(len(hearing_rows)+(3 if touch else 4)-1)//(3 if touch else 4))) if view=="statements" and len(hearing_rows)>(3 if touch else 4) else "되묻기 · 대조" if view=="statements" else "현재 두 장" if pair_submission else "체크로 두 장" if mode=="compare" and len(chosen)<2 else "제출 자료" if persistent.room13_pw_controls_seen else "체크로 선택") size small color muted font R13_UI_FONT
    $ secondary=[]
    if can_review:
        $ secondary.append(("현장으로",review_action,"r13_pw_investigate"))
    if view=="pair" and r13_pw_observe_available(key,live_pair):
        $ secondary.append(("짚기 그만" if observe else "문서 짚기",[Function(r13_pw_remember_pair,claim,pair),SetScreenVariable("quote_open",False),ToggleScreenVariable("observe")],"r13_pw_observe"))
    if hearing_row:
        $ secondary.append(("더 확인한다" if hearing_kind=="question" else "되묻는다",Return(("hearing_press",hearing_target)),"r13_pw_press"))
        if key=="바깥 걸쇠 주장과 발견 위치를 대조한다":
            $ secondary.append(("등 구조 보기",Return(("hearing_inspect","latch")),"r13_hearing_inspect"))
    elif can_press:
        $ secondary.append(("되묻는다",Return("press"),"r13_pw_press"))
    for si,(caption,action,cid) in enumerate(secondary[:2]):
        fixed:
            xpos (480+si*164) ypos L["footer_y"] xysize (156,L["footer_h"])
            use r13_control(caption,None,action,enabled=ready,width=156,label_size=small,control_id=cid)
    fixed:
        xpos 822 ypos L["footer_y"] xysize (128,L["footer_h"])
        use r13_control("접기" if origin_open else "출처",None,ToggleScreenVariable("origin_open"),enabled=ready and view not in ("list","statements"),width=128,label_size=small,control_id="r13_pw_origin")
    fixed:
        xpos 966 ypos L["footer_y"] xysize (240,L["footer_h"])
        use r13_control("연결판으로" if hearing_only else "자료 대조" if view=="statements" else ("질문에 답하기" if hearing_kind=="question" else "이 발언에 제시") if hearing_row and mode!="compare" else room_letters_copy[0] if room_letters_copy else "다른 부분 짚기" if discovery_pending else "이 두 장 비교" if pair_submission else r13_pw_main_label(mode),None,Return("hearing_resume") if hearing_only else [SetScreenVariable("view","list"),SetScreenVariable("quote_open",True)] if view=="statements" else Return(("hearing_argue",hearing_target)) if hearing_row and mode!="compare" else Function(r13_pw_submit_pair,claim,live_pair,mode) if pair_submission else Function(r13_pw_submit_selected,claim),enabled=ready and (True if hearing_only else bool(hearing_row) if view=="statements" else bool(chosen) if hearing_row and mode!="compare" else bool(pair_submission) or (r13_pw_submit_ok(stored,mode) and r13_pw_submit_ok(chosen,mode))),primary=True,width=240,control_id="r13_pw_submit")
    if replace_pending:
        button:
            xysize (1280,720) background Solid("#05070f88") action NullAction()
        frame:
            area (240,210,800,300) padding (24,24) background R13ConfirmPaper()
            vbox:
                spacing 20
                text ("「"+r13_catalog_title(replace_pending)+"」와 바꿀 자료") xsize 748 size r13_type("emphasis") color ink font R13_UI_BOLD_FONT
                hbox:
                    spacing 16
                    for old in chosen:
                        use r13_control(r13_ev_two_lines(r13_catalog_title(old),320,small,2),None,Function(r13_pw_replace_action,claim,old,replace_pending),width=352,label_size=small,control_id=r13_pw_id("r13_pw_swap_",old))
                use r13_control("취소",None,SetScreenVariable("replace_pending",None),width=144,control_id="r13_pw_swap_cancel")

# 작은 머리글 그림은 필요할 때 기존 수첩 판에서 확대해 본다.
screen r13_pw_picture(key,called=False):
    modal True
    zorder 90
    default fire_focus=None
    $ close_action=Return() if called else Hide("r13_pw_picture")
    use r13_notebook_shell(r13_catalog_title(key),close_action=close_action)
    if r13_fire_site_available(key,r13_pw_entries()):
        text "그림을 누르면 크게 봅니다." xpos 1128 xanchor 1.0 ypos 82 size r13_type("emphasis" if r13_touch_ui() else "small") color r13_nb_muted() font R13_UI_FONT
        use r13_fire_site_picture(fire_focus)
        fixed:
            xpos 1006 ypos r13_nb_footer_y() xysize (200,r13_control_height())
            use r13_control("닫기",None,close_action,primary=True,width=200,height=r13_control_height(),label_size=r13_type("emphasis"),control_id="r13_fire_picture_close")
    else:
        $ box=min(420,r13_nb_footer_y()-R13_NB_TOP-28)
        fixed:
            xcenter 640 ypos (R13_NB_TOP+12) xysize (box,box)
            use r13_evidence_picture_box(key,box)
        use r13_nb_footer_button(0,"닫기",close_action,primary=True)
    key "game_menu" action close_action
