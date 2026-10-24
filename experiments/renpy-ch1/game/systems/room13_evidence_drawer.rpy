# 증거 서랍 (2026-10-24 소유자 "추천안대로", 디자인 적용 승인).
# 시안: docs/reviews/evidence-drawer-20261024/01_비교.png, 02_이번사건.png, 03_지난사건.png
# 설계: docs/design/EVIDENCE_CLUTTER_PLAN.md 1부. 적용 기록: docs/reviews/evidence-drawer-20261024/적용보고.md
#   - 지금 이야기(v111)의 자료를 사건(회의)별로 묶는다. 회의가 끝나면 그 사건 자료는 「지난 사건」으로 간다.
#     옛 이야기의 「지난 사건」 묶음(systems/room13_shelf.rpy)은 그대로 두고, v111 에서만 이 서랍을 쓴다.
#   - 어느 사건에 묶일지는 "얻은 자리에서 가장 가까운 다음 회의"다. 자리는 이야기 원본에서 뽑은
#     game/v111/evidence-drawer.json(dev/build_evidence_drawer.py)을 쓰고, 이번 판의 획득 기록(날·출처)이
#     있으면 그것을 먼저 본다. 옛 저장 파일은 기록에 있는 날만으로도 같은 표에서 자리를 찾는다.
#   - 정정·결과 기록은 원래 카드 귀퉁이의 「쪽지」로 접어 목록에서 뺀다. 회의 정답·대체 세트·덧붙임과
#     대화에서 꺼내는 자료는 접지 않는다(다른 작업자가 늘리는 R13_PROOF_ALTERNATES/EXTRAS 는 실행 중에 읽는다).
#   - 어느 자료가 다시 쓰이는지는 어디에도 표시하지 않는다(정답 힌트 금지). 서랍을 여는 것이 추리다.
# 화면에서만 묶고 접는다. 자료 보유·이야기 조건·회의 판정은 그대로다.
init 336 python:
    import json as _r13_dr_json
    R13_DRAWER=(_r13_dr_json.load(renpy.file("v111/evidence-drawer.json")) if renpy.loadable("v111/evidence-drawer.json")
        else dict(meetings=[],sites={},fixed=[]))
    R13_DRAWER_SCENE_INDEX=dict((scene,i) for i,scene in enumerate(R13_V111.get("scene_days",{})))
    # 사건 이름: 회의가 다룬 일을 물건·자리로 짧게(갈림길 화면의 회의 이름과 겹치지 않게). 번호는 회의 순서.
    R13_DRAWER_NAMES=dict(gate="초소의 입장",lamp="3번 등의 돌",gate_post="밤이의 혐의",fire="장작 창고의 불",
        room13="13호의 밤",records="맡긴 기록",hypothesis="무너지는 까닭",soup="학교의 수프",
        blanket="담요의 새",piko="두 배의 장부",altar="제단의 이름")
    R13_DRAWER_NUMBERS="①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"
    # 갱신은 쪽지로(설계 1부 2번·2부 끝 문단): (쪽지가 될 기록, 붙을 원래 카드).
    # E13_HANDOVER·E14_SUPPLY·E13_ORDER 는 대화·회의에서 직접 꺼내는 자료라 접지 않는다(적용보고.md).
    R13_DRAWER_NOTES=(("E26","E21"),("E19","E21"),("E05","E02"),("E30","E06"),("E10_PUMP","E06_CONTACT"),("E08_RECENT_LETTER","E27"))
    R13_DRAWER_BACK=("drawer:back:past","drawer:back:person")
    # 꼬리표는 짧게: 긴 장소 이름은 끝 낱말로 줄이되(「눈에 막힌 입구」→「입구」), 그게 어색한 곳만 적는다.
    R13_DRAWER_PLACE_SHORT=dict(v111_custody="보호실",v111_supervised="감독 자리")
    R13_DRAWER_PERSON_SKIP=("아이","주민","아빠","순찰대원")
    R13_DRAWER_GRID_ROWS=3
    R13_DRAWER_GRID_COLS=3

    def r13_drawer_active(archive=False):
        return not archive and r13_v111_active() and bool(R13_DRAWER.get("meetings"))

    def r13_drawer_meetings():
        return [m["key"] for m in R13_DRAWER.get("meetings",[])]

    def _r13_dr_scene(scene):
        return R13_DRAWER_SCENE_INDEX.get(scene,len(R13_DRAWER_SCENE_INDEX))

    def _r13_dr_before(site,meeting):
        """이 획득 자리가 이 회의 전(같은 장면이면 마지막 증명 줄까지)인가."""
        a,b=_r13_dr_scene(site[0]),_r13_dr_scene(meeting["scene"])
        if a!=b:return a<b
        return site[2]<0 or (site[1]==meeting["file"] and site[2]<=meeting["line"])

    def r13_drawer_record(key):
        return ((store.room13 or {}).get("records",{}) or {}).get(key) or {}

    def r13_drawer_site(key):
        """이번 판에서 이 자료를 얻은 자리. 출처가 이야기 기록이면 그 장면, 아니면 얻은 날의 자리, 없으면 처음 자리."""
        base=r13_evidence_base_key(key)
        sites=R13_DRAWER.get("sites",{}).get(base) or [] if base else []
        rec=r13_drawer_record(key)
        source=str(rec.get("source") or "")
        for site in sites:
            if site[2]<0 and source.startswith(site[0]+"_"):return site
        day=rec.get("day")
        same=[site for site in sites if R13_V111["scene_days"].get(site[0])==day]
        if same:return same[0]
        return sites[0] if sites else None

    def r13_drawer_case_of(key):
        """이 자료가 묶이는 사건(회의 키). 사건이 없는 물건·옛 기록은 None."""
        meetings=R13_DRAWER.get("meetings",[])
        if not meetings or not r13_evidence_base_key(key):return None
        site=r13_drawer_site(key)
        if site:
            for meeting in meetings:
                if _r13_dr_before(site,meeting):return meeting["key"]
            return meetings[-1]["key"]
        day=r13_drawer_record(key).get("day")
        if day is None:return None
        for meeting in meetings:
            if meeting["day"]>=day:return meeting["key"]
        return meetings[-1]["key"]

    def r13_drawer_closed(meeting):
        """회의가 끝났다(결과가 있다). 이 판에 열리지 않은 회의는 뒤 회의가 끝나면 닫힌 것으로 본다."""
        keys=r13_drawer_meetings()
        if meeting not in keys:return False
        return any(r13_v111_value("meeting:"+k) is not None for k in keys[keys.index(meeting):])

    def r13_drawer_case_day(meeting):
        for m in R13_DRAWER.get("meetings",[]):
            if m["key"]==meeting:return m["day"]
        return None

    def r13_drawer_case_title(meeting,with_day=True):
        keys=r13_drawer_meetings()
        number=R13_DRAWER_NUMBERS[keys.index(meeting)] if meeting in keys and keys.index(meeting)<len(R13_DRAWER_NUMBERS) else ""
        title=(number+" " if number else "")+R13_DRAWER_NAMES.get(meeting,meeting)
        return title+(" · %d일"%r13_drawer_case_day(meeting) if with_day and r13_drawer_case_day(meeting) else "")

    # 쪽지 ---------------------------------------------------------------
    def r13_drawer_note_pairs():
        """(쪽지, 원래 카드) 전체 키. 회의 제시에 쓰이는 자료는 이 자리에서 빠진다."""
        used=set(R13_DRAWER.get("fixed",[]))
        for sets in globals().get("R13_PROOF_ALTERNATES",{}).values():
            for one in sets:used.update(one)
        for one in globals().get("R13_PROOF_EXTRAS",{}).values():used.update(one)
        return [("V111:"+note,"V111:"+base) for note,base in R13_DRAWER_NOTES if note not in used]

    def r13_drawer_folded(owned=None):
        owned=set((store.room13 or {}).get("evidence",[]) if owned is None else owned)
        if not r13_drawer_active():return {}
        return dict((note,base) for note,base in r13_drawer_note_pairs() if note in owned and base in owned)

    def r13_drawer_notes(key):
        return [note for note,base in r13_drawer_folded().items() if base==key]

    # 목록 ---------------------------------------------------------------
    def r13_drawer_visible(entries):
        folded=r13_drawer_folded()
        return [k for k in entries if k not in folded]

    def r13_drawer_now(entries):
        out=[]
        for key in r13_drawer_visible(entries):
            case=r13_drawer_case_of(key)
            if not (case and r13_drawer_closed(case)):out.append(key)
        return out

    def r13_drawer_cases(entries):
        """끝난 사건 묶음, 최근 사건부터: [(회의, [자료])]."""
        groups={}
        for key in r13_drawer_visible(entries):
            case=r13_drawer_case_of(key)
            if case and r13_drawer_closed(case):groups.setdefault(case,[]).append(key)
        return [(m,groups[m]) for m in reversed(r13_drawer_meetings()) if m in groups]

    def r13_drawer_mentions(key,person):
        if ROOM13["evidence_sources"].get(key)==person:return True
        name=R13_NAMES.get(person)
        record=r13_catalog_record(key) or {}
        return bool(name) and name in (record.get("name","")+" "+record.get("establishes",""))

    def r13_drawer_people(entries):
        """사람별: 그 사람이 출처이거나 이름·내용에 나오는 자료. 많이 나오는 사람부터."""
        visible=r13_drawer_visible(entries)
        met=r13_met_people()
        seen_names=set();rows=[]
        people=list(dict.fromkeys(list(met)+list(R13_NAMES)))
        for person in people:
            name=R13_NAMES.get(person)
            # 이름 없는 배역(순찰대원·주민·아이 등)은 흔한 낱말이라 아무 자료에나 걸린다. 이름 있는 사람만.
            if person=="dad" or person.startswith("v111_") or not name or name in R13_DRAWER_PERSON_SKIP or name in seen_names or person not in CAST:continue
            keys=[k for k in visible if r13_drawer_mentions(k,person)]
            if keys:
                seen_names.add(name);rows.append((person,keys))
        rows.sort(key=lambda row:-len(row[1]))
        return rows

    def r13_drawer_groups(mode,entries):
        return r13_drawer_cases(entries) if mode=="past" else r13_drawer_people(entries)

    def r13_drawer_group_keys(mode,entries,chosen):
        for key,keys in r13_drawer_groups(mode,entries):
            if key==chosen:return keys
        return []

    def r13_drawer_group_choice(mode,entries,chosen):
        groups=r13_drawer_groups(mode,entries)
        keys=[key for key,_ in groups]
        return chosen if chosen in keys else (keys[0] if keys else None)

    def r13_drawer_group_title(mode,key,with_day=True):
        return r13_drawer_case_title(key,with_day) if mode=="past" else R13_NAMES.get(key,key)

    def r13_drawer_now_day():
        return (store.room13 or {}).get("day",1)

    # 카드 꼬리표 「N일 · 장소」 ------------------------------------------
    def r13_drawer_tag(key):
        if not r13_drawer_active() or not r13_evidence_base_key(key):return ""
        rec=r13_drawer_record(key)
        day=rec.get("day")
        place=None
        if day is not None:
            # 「여관 1층 · 주방」처럼 긴 장소 이름은 마지막 자리만(시안 「13일 밤 · 주방」).
            place=(R13_PLACES.get(rec.get("place")) or (None,))[0]
            place=R13_DRAWER_PLACE_SHORT.get(rec.get("place")) or (place.split(" · ")[-1] if place else None)
            if place and len(place)>6:place=place.split(" ")[-1]
        else:
            site=r13_drawer_site(key)
            day=R13_V111["scene_days"].get(site[0]) if site else None
        if day is None:return ""
        text="%d일"%day+(" 밤" if rec.get("period")==3 else "")
        return text+(" · "+place if place else "")

    def r13_drawer_unread(key):
        return r13_record_unread(key) or any(r13_record_unread(note) for note in r13_drawer_notes(key))

    def r13_drawer_mark_notes(key):
        for note in r13_drawer_notes(key):r13_record_update_ui("seen",note,True)
        renpy.restart_interaction()

    # 화면 상태 ------------------------------------------------------------
    def r13_drawer_reset(owner):
        return [Function(r13_record_select,owner,name,value,False) for name,value in
            (("detail",None),("page",0),("pair",None),("drawer_gpage",0),("drawer_ipage",0))]

    def r13_drawer_chips(owner,mode,archive=None):
        chips=[(title,mode==key,[Function(r13_record_select,owner,"drawer",key,False)]+r13_drawer_reset(owner))
            for key,title in (("now","이번 사건"),("past","지난 사건"),("person","사람별"))]
        if archive is not None:
            chips.append(("지난 플레이",bool(archive),[Function(r13_record_select,owner,"archive",not archive,False)]+r13_drawer_reset(owner)))
        return chips

    def r13_drawer_open(owner,key,keys):
        """묶음 오른쪽 격자에서 고른 자료를 기존 상세로 연다(왼쪽 첫 줄은 묶음 목록으로 돌아가기)."""
        index=(keys.index(key)+1) if key in keys else 0
        return [Function(r13_record_select,owner,"detail",key,True),Function(r13_record_select,owner,"pair",None,False),
            Function(r13_record_select,owner,"page",index//r13_record_page_size(),False)]

    def r13_drawer_back(owner):
        return [Function(r13_record_select,owner,"detail",None,False),Function(r13_record_select,owner,"pair",None,False),
            Function(r13_record_select,owner,"page",0,False)]

    def r13_drawer_selected(entries,detail,page,present=False):
        visible=[k for k in entries[r13_record_page(entries,page)*r13_record_page_size():][:r13_record_page_size()] if k not in R13_DRAWER_BACK]
        if detail in visible or present:return detail if detail in visible else None
        return visible[0] if visible else None

    def r13_drawer_view(mode,entries,detail,chosen):
        """지금 보는 서랍: ("list", 목록) 이번 사건 · ("groups", None) 묶음 고르기 · ("group", [뒤로]+목록) 묶음 안 상세."""
        if mode not in ("past","person"):return ("list",r13_drawer_now(entries))
        keys=r13_drawer_group_keys(mode,entries,r13_drawer_group_choice(mode,entries,chosen))
        if detail is not None and detail in keys:
            return ("group",[R13_DRAWER_BACK[0 if mode=="past" else 1]]+keys)
        return ("groups",None)

    def r13_drawer_header(mode,entries,view,chosen):
        if view[0]=="list":return "이번 사건 · %d일  %d개"%(r13_drawer_now_day(),len(view[1]))
        choice=r13_drawer_group_choice(mode,entries,chosen)
        if view[0]=="group":
            return r13_drawer_group_title(mode,choice)+"  %d개"%(len(view[1])-1)
        groups=r13_drawer_groups(mode,entries)
        if mode=="past":return "지난 사건 · %d건  %d개"%(len(groups),sum(len(k) for _,k in groups))
        return "사람별 · %d명"%len(groups)

    def r13_drawer_where(key,entries):
        """기록의 다른 칸(관계도 등)에서 자료로 넘어올 때 그 자료가 있는 서랍."""
        if key in r13_drawer_now(entries):return ("now",None)
        for case,keys in r13_drawer_cases(entries):
            if key in keys:return ("past",case)
        return ("now",None)

    _r13_drawer_open_person_material=r13_open_person_material
    def r13_open_person_material(owner,key):
        _r13_drawer_open_person_material(owner,key)
        entries=r13_catalog_entries()
        if not r13_drawer_active() or key not in entries:return
        folded=r13_drawer_folded()
        key=folded.get(key,key)
        mode,case=r13_drawer_where(key,entries)
        if mode=="past":
            keys=r13_drawer_group_keys("past",entries,case)
            owner.update(drawer="past",drawer_case=case,detail=key,page=(keys.index(key)+1)//r13_record_page_size())
        else:
            now=r13_drawer_now(entries)
            owner.update(drawer="now",detail=key,page=(now.index(key)//r13_record_page_size()) if key in now else 0)

# 한 장 카드: 그림 · 이름 · 꼬리표 「N일 · 장소」 · 귀퉁이 쪽지. 왼쪽 목록과 묶음 격자가 같이 쓴다.
screen r13_drawer_card_body(key,w,h,label_size,chosen=False,thumb=60,name_width=174):
    $ tag=r13_drawer_tag(key)
    $ notes=len(r13_drawer_notes(key)) if r13_drawer_active() else 0
    $ small=r13_ev_small_size()
    fixed:
        xysize (w,h)
        add r13_evidence_picture(key,thumb) xpos 7 ypos (h//2) yanchor .5
        vbox:
            xpos (thumb+16) ypos (h//2) yanchor .5 spacing 2
            text r13_ev_two_lines(r13_catalog_title(key),name_width,label_size,(2 if tag else 3)):
                xsize name_width text_align 0 size label_size color "#e3d6bd" font r13_ui_font() line_spacing -1
            if tag:
                text tag size small color ("#f0c66a" if chosen else "#beaa8c") font r13_ui_font() xsize name_width
        if notes:
            # 갱신 기록은 새 카드가 아니라 원래 카드 귀퉁이의 쪽지로 붙는다(시안 그대로의 베이지 꼬리표).
            frame:
                xpos (w-6) xanchor 1.0 ypos -8 padding (8,1) background Solid("#ecdebe")
                text ("쪽지 %d"%notes) size max(13,small-4) color "#50321e" font r13_ui_font()

# 왼쪽: 사건 묶음(지난 사건) 또는 사람(사람별) 카드, 다섯 줄씩.
screen r13_drawer_group_list(mode,entries,chosen,gpage,owner,header):
    $ touch=r13_touch_ui()
    $ label_size=(r13_read_size(22,24) if touch else r13_read_size(18,22))
    $ groups=r13_drawer_groups(mode,entries)
    $ size=r13_record_page_size()
    $ pages=max(1,(len(groups)+size-1)//size)
    $ gpage=max(0,min(gpage,pages-1))
    text header xpos 64 ypos 112 size label_size color "#d9c9a8" font r13_ui_font()
    for index,(group_key,group_items) in enumerate(groups[gpage*size:][:size]):
        $ is_chosen=group_key==chosen
        button:
            xpos 60 ypos (140+index*88) xysize (256,88) padding (0,0)
            background R13ControlSurface(chosen=is_chosen) hover_background R13ControlSurface(chosen=is_chosen,hovered=True)
            alt r13_drawer_group_title(mode,group_key)
            action [Function(r13_record_select,owner,"drawer_case",group_key,False),Function(r13_record_select,owner,"drawer_ipage",0,False)]
            fixed:
                xysize (256,88)
                if mode=="past":
                    # 사건의 자료 그림 세 장을 겹쳐 놓는다(시안).
                    for j,icon_key in enumerate(group_items[:3]):
                        add r13_evidence_picture(icon_key,40) xpos (6+j*20) ypos (44+(j%2)*6) yanchor .5
                else:
                    add Transform(r13_art(group_key,"avatar_neutral"),xysize=(56,56),fit="contain") xpos 10 ypos 44 yanchor .5
                # 시안은 셋째 그림과 이름 첫 글자가 겹친다. 번호가 그림에 묻히지 않게 이름을 몇 px 오른쪽에 둔다.
                vbox:
                    xpos 92 ypos 44 yanchor .5 spacing 2
                    text r13_ev_two_lines(r13_drawer_group_title(mode,group_key,False),156,label_size,2):
                        xsize 156 size label_size color "#e3d6bd" font r13_ui_font() line_spacing -1
                    text ((("%d일 · "%r13_drawer_case_day(group_key)) if mode=="past" and r13_drawer_case_day(group_key) else "")+"자료 %d"%len(group_items)):
                        size r13_ev_small_size() color ("#f0c66a" if is_chosen else "#beaa8c") font r13_ui_font()
    if pages>1:
        $ ph=r13_ev_button_height()
        $ pw=88 if touch else 72
        fixed:
            xpos 60 ypos (R13_EV_BOTTOM-ph) xysize (pw,ph)
            use r13_control("‹",None,Function(r13_record_select,owner,"drawer_gpage",gpage-1,False),enabled=gpage>0,width=pw,height=ph,control_id="r13_dr_gprev")
        text ("%d / %d"%(gpage+1,pages)) xpos 188 xanchor .5 ypos (R13_EV_BOTTOM-ph//2) yanchor .5 size label_size color "#d9c9a8" font r13_ui_font()
        fixed:
            xpos (316-pw) ypos (R13_EV_BOTTOM-ph) xysize (pw,ph)
            use r13_control("›",None,Function(r13_record_select,owner,"drawer_gpage",gpage+1,False),enabled=gpage+1<pages,width=pw,height=ph,control_id="r13_dr_gnext")
    if not groups:
        text ("끝난 사건이 아직 없습니다. 회의가 끝나면 그 사건 자료가 여기로 옵니다." if mode=="past" else "자료에 나오는 사람이 아직 없습니다."):
            xpos 64 ypos 160 xsize 252 size label_size color "#b8b0a2" font r13_ui_font()
    add Solid("#c9a86a66") xpos 330 ypos 116 xsize 1 ysize 564

# 오른쪽: 고른 묶음의 자료 카드 격자. 누르면 기존 상세(왼쪽 목록 + 큰 그림)로 간다.
screen r13_drawer_group_grid(mode,entries,chosen,ipage,owner):
    $ touch=r13_touch_ui()
    $ keys=r13_drawer_group_keys(mode,entries,chosen)
    $ label_size=(r13_read_size(22,24) if touch else r13_read_size(18,22))
    $ per=R13_DRAWER_GRID_ROWS*R13_DRAWER_GRID_COLS
    $ pages=max(1,(len(keys)+per-1)//per)
    $ ipage=max(0,min(ipage,pages-1))
    $ card_h=88 if touch else 82
    if chosen:
        text r13_drawer_group_title(mode,chosen) xpos 370 ypos 116 size (r13_read_size(30,32) if touch else r13_read_size(28,30)) color "#f6ecd8" font r13_ui_font()
        text ("회의가 끝난 사건의 자료입니다. 다른 회의에서도 낼 수 있습니다." if mode=="past" else "이 사람이 나오는 자료입니다."):
            xpos 370 ypos (164 if touch else 160) xsize 840 size r13_ev_small_size() color "#beaa8c" font r13_ui_font()
        for index,key in enumerate(keys[ipage*per:][:per]):
            button:
                xpos (370+(index%R13_DRAWER_GRID_COLS)*280) ypos (206+(index//R13_DRAWER_GRID_COLS)*110) xysize (250,card_h) padding (0,0)
                background R13ControlSurface() hover_background R13ControlSurface(hovered=True)
                alt r13_catalog_title(key) action r13_drawer_open(owner,key,keys)
                fixed:
                    xysize (250,card_h)
                    use r13_drawer_card_body(key,250,card_h,label_size,False,56,166)
                    if r13_drawer_unread(key):
                        text "●" xpos 63 xanchor 1.0 ypos 3 size 13 color "#f0c66a" font r13_ui_font()
        if pages>1:
            $ ph=r13_ev_button_height()
            $ pw=88 if touch else 72
            fixed:
                xpos 370 ypos (R13_EV_BOTTOM-ph) xysize (pw,ph)
                use r13_control("‹",None,Function(r13_record_select,owner,"drawer_ipage",ipage-1,False),enabled=ipage>0,width=pw,height=ph,control_id="r13_dr_iprev")
            text ("%d / %d"%(ipage+1,pages)) xpos (370+pw+64) xanchor .5 ypos (R13_EV_BOTTOM-ph//2) yanchor .5 size label_size color "#d9c9a8" font r13_ui_font()
            fixed:
                xpos (370+pw+128) ypos (R13_EV_BOTTOM-ph) xysize (pw,ph)
                use r13_control("›",None,Function(r13_record_select,owner,"drawer_ipage",ipage+1,False),enabled=ipage+1<pages,width=pw,height=ph,control_id="r13_dr_inext")

# 묶음 고르기 한 화면(왼쪽 묶음 목록 + 오른쪽 격자).
screen r13_drawer_groups_view(mode,entries,chosen,gpage,ipage,owner,header):
    $ chosen=r13_drawer_group_choice(mode,entries,chosen)
    use r13_drawer_group_list(mode,entries,chosen,gpage,owner,header)
    use r13_drawer_group_grid(mode,entries,chosen,ipage,owner)

# 상세 아래에 붙는 쪽지: 원래 카드 내용 다음에 그 쪽지의 이름 · 꼬리표와 관찰 사실.
screen r13_drawer_note_blocks(key,width):
    for note in r13_drawer_notes(key):
        frame:
            xsize width padding (14,10) background Frame(R13_NIGHT_UI+"preview_box.png",8,8)
            vbox:
                spacing 6
                text ("쪽지 · "+r13_catalog_title(note)+((" · "+r13_drawer_tag(note)) if r13_drawer_tag(note) else "")):
                    size r13_ev_small_size() color "#d9b46c" font r13_ui_font() xsize (width-28)
                use r13_evidence_fact_list(note,width-28)
