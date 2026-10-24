default r13_present_priority = None
default r13_book_views = {}
default r13_record_scrolls = {}
default r13_records_view = {}

# Record categories are explicit: a testimony is not inferred from its title.
init 68 python:
    R13_RECORD_CATEGORIES={"물증":"evidence","기록":"evidence","관찰기록":"evidence","증언":"testimony"}
    assert set(ev["kind"] for ev in ROOM13["evidence"].values())<=set(R13_RECORD_CATEGORIES)
    R13_RECORD_SHORT={
        "E01":"초대 편지","E02":"고친 입장기록","E03":"바느질 흔적","E04":"옛 도면","E05":"통로 작동",
        "E06":"다람이 만남","E07":"촛대 두 부분","E08":"진료·죽음 기록","E09":"촛농·발자국","E10":"밤이의 목격",
        "E11":"복도 구조순서","E12":"공구 운반공백","E13":"핀 수리 쪽지","E14":"촛대 속 핀","E15":"여민 브로치",
        "E16":"떼어놓기 요청","E17":"어르신 사본","E18":"미전달 봉투","E19":"초롱의 답장","E20":"회복 관찰",
        "E21":"힘 다한 기록","E22":"힘 뽑기 원본","E23":"첫 옮김 관찰","E24":"저녁 관찰","E25":"대피소 받음",
        "E26":"땔감·식량","E27":"끌고 갈 명령","E28":"교대 관찰","E29":"낮은 통로","E30":"엄마의 연구",
        "E31":"지우기 전 기록","E32":"밖으로 간 도면","E33":"촛대 보관 기록","E34":"되돌아온 짐","E35":"파단면·상처",
        "E36":"전날 진료요청","E37":"잠금 작동기록","G1":"방문 신청 원본","G2":"겨울철 입장 규칙","G3":"초소 처리 명단",
    }
    R13_RECORD_PAGE_SIZE=12
    def r13_book_context(target,hearing):
        if hearing:
            return ("meeting",getattr(store,"r13_meeting_claim",None),getattr(store,"r13_debate_selected",None))
        return ("person",target)

    def r13_book_remember(context,detail,page,material_filter="all"):
        views=dict(getattr(store,"r13_book_views",{}))
        views[context]=dict(detail=detail,page=page,material_filter=material_filter)
        store.r13_book_views=views

    def r13_records_remember(tab,detail,person,page,archive,rel_sel=None,rel_filter="all",rel_focus=True,material_filter="all",drawer="now",drawer_case=None):
        store.r13_records_view=dict(tab=tab,detail=detail,person=person,page=page,archive=archive,rel_sel=rel_sel,rel_filter=rel_filter,rel_focus=rel_focus,material_filter=material_filter,drawer=drawer,drawer_case=drawer_case)

    class R13RecordScrollChanged:
        def __init__(self,key):
            self.key=key
        def __call__(self,value):
            # Store numbers only, never viewports or adjustments in a save.
            value=max(0,int(value))
            offsets=dict(getattr(store,"r13_record_scrolls",{}))
            if offsets.get(self.key,0)!=value:
                offsets[self.key]=value
                store.r13_record_scrolls=offsets
                renpy.retain_after_load()

    def r13_record_scroll_key(context,detail,archive=False):
        return (context,detail,bool(archive),bool(getattr(persistent,"room13_large_text",False)))

    def r13_record_scroll_adjustment(context,detail,archive=False):
        key=r13_record_scroll_key(context,detail,archive)
        # The viewport replaces this provisional range with measured text height.
        # A range of 1 would clamp the saved offset before first layout.
        return ui.adjustment(range=100000,value=getattr(store,"r13_record_scrolls",{}).get(key,0),
            changed=R13RecordScrollChanged(key))

    def r13_book_statement():
        claim=getattr(store,"r13_meeting_claim",None)
        sid=getattr(store,"r13_debate_selected",None)
        if not claim or not sid:return None
        st=r13_debate_statement(claim,sid)
        return (R13_NAMES.get(st["who"],"발언자"),r13_meeting_statement_text(claim,sid))

    def r13_record_category(key):
        return R13_RECORD_CATEGORIES[ROOM13["evidence"][key]["kind"]]
    def r13_record_entries(category="evidence",archive=False,present=False,order="acquired",favorite_only=False):
        raw=(getattr(persistent,"room13_knowledge",[]) or []) if archive and not present else ((store.room13 or {}).get("evidence",[]))
        entries=list(dict.fromkeys(key for key in raw if key in ROOM13["evidence"] and r13_record_category(key)==category))
        if order=="recent":entries.reverse()
        # The legacy favorite_only argument is ignored so old saved filters cannot hide records.
        return entries
    def r13_material_subset(entries,kind="all"):
        # A lens over one collection, not a second evidence/inventory split.
        if kind=="testimony":
            return [key for key in entries if key in ROOM13["evidence"] and ROOM13["evidence"][key]["kind"]=="증언"]
        if kind=="transfer":return [key for key in entries if r13_catalog_transferable(key)]
        # 0.19.8: a record read while this filter is on stays listed until the filter changes; dropping it
        # at once auto-selected the next one and marked the whole list read, or disabled presenting.
        if kind=="unread":return [key for key in entries if r13_record_unread(key) or key in r13_unread_hold]
        return entries

    # Keep every record footer inside the sheet (bottom 676), with a 16px inset.
    def r13_record_footer_height():
        return r13_control_height()

    def r13_record_footer_y():
        return 660-r13_record_footer_height()

    def r13_material_filter_choices(current,allow_transfer=True):
        owned=r13_catalog_entries(False,False)
        choices=[(key,title) for key,title in (("all","전체"),("testimony","증언"),("transfer","전달 가능"))
            if (key!="transfer" or allow_transfer) and (key in ("all",current) or bool(r13_material_subset(owned,key)))]
        # All has no action to offer when there is no other material category.
        return choices if len(choices)>1 else []

    def r13_material_filters_visible(current,allow_transfer=True,shelf=None,shelf_count=0):
        return bool(r13_material_filter_choices(current,allow_transfer) or (shelf is not None and (shelf_count or shelf)))

    def r13_material_body(ev):
        # Presentation only: never rewrite evidence facts or the catalogue.
        import re
        body=ev.get("establishes","")
        title=ev.get("name","")
        for separator in (" / ",": ","：", "\n"):
            prefix=title+separator
            if title and body.startswith(prefix):
                body=body[len(prefix):].lstrip()
                break
        # Only spaced list separators before words; keep dates, fractions and URLs.
        return re.sub(r"\s+/\s+(?=[가-힣A-Za-z「‘“])","\n",body)

    def r13_material_source_person(key):
        # Only explicit source metadata and people already encountered.
        who=ROOM13["evidence_sources"].get(key)
        return who if key in (store.room13 or {}).get("evidence",[]) and who in r13_met_people() else None

    def r13_person_materials(person):
        return [key for key in r13_catalog_entries(hearing=True) if key in ROOM13["evidence"]
            and ROOM13["evidence"][key]["kind"]=="증언"
            and ROOM13["evidence_sources"].get(key)==person]

    def r13_open_record_relation(owner,person):
        if person not in r13_met_people():return
        owner.update(tab="relations",rel_sel=person,rel_focus=True)
        renpy.restart_interaction()

    def r13_open_person_material(owner,key):
        entries=r13_catalog_entries()
        if key not in entries:return
        owner.update(tab="all",archive=False,material_filter="all",detail=key,
            page=entries.index(key)//r13_record_page_size())
        r13_record_mark_seen(key)

    def r13_record_page_size():return 5
    def r13_record_pages(entries):return max(1,(len(entries)+r13_record_page_size()-1)//r13_record_page_size())
    def r13_record_page(entries,page):return max(0,min(page,r13_record_pages(entries)-1))
    def r13_record_restore_page(entries,detail,page):
        # The remembered record survives page-size/order changes in old saves.
        return entries.index(detail)//r13_record_page_size() if detail in entries else r13_record_page(entries,page)
    def r13_record_selected(entries,detail,page):
        visible=entries[r13_record_page(entries,page)*r13_record_page_size():][:r13_record_page_size()]
        return detail if detail in visible else (visible[0] if visible else None)
    r13_unread_hold=set()
    def r13_record_select(owner,variable,value,mark_seen=True):
        if variable=="material_filter":r13_unread_hold.clear()
        if not isinstance(owner,str):owner[variable]=value
        else:renpy.set_screen_variable(variable,value,screen=owner)
        if mark_seen and variable=="detail" and value in (store.room13 or {}).get("evidence",[]):
            r13_record_update_ui("seen",value,True)
        renpy.restart_interaction()
    def r13_prepare_present(target,keys):
        owned=(store.room13 or {}).get("evidence",[])
        store.r13_present_priority=(target,tuple(k for k in keys if k in owned))
    def r13_present_entries(entries,target):
        pending=getattr(store,"r13_present_priority",None)
        keys=pending[1] if pending and pending[0]==target else ()
        return [k for k in keys if k in entries]+[k for k in entries if k not in keys]
    def r13_present_selection(entries,detail,page):
        return detail if detail in entries[r13_record_page(entries,page)*r13_record_page_size():][:r13_record_page_size()] else None
    def r13_record_unread(key):
        return key in (store.room13 or {}).get("evidence",[]) and key not in (store.room13 or {}).get("record_ui",{}).get("seen",[])
    def r13_record_update_ui(field,key,add):
        if field!="seen" or key not in (store.room13 or {}).get("evidence",[]):return False
        ui_state=winter_copy.deepcopy(store.room13.get("record_ui",{}))
        values=list(ui_state.get(field,[]))
        if add:r13_unread_hold.add(key)
        if add and key not in values:values.append(key)
        elif not add and key in values:values.remove(key)
        else:return False
        ui_state[field]=values
        r13_edit(record_ui=ui_state)
        renpy.retain_after_load()
        return True
    def r13_record_mark_seen(key):
        # UI actions must not return the boolean state-change result: Ren'Py
        # would treat it as the return value of the active call screen.
        r13_record_update_ui("seen",key,True)
        renpy.restart_interaction()
    def r13_record_toggle_favorite(key):
        # Retired UI action name retained for already-saved screen actions.
        pass

    R13_RECORD_ICON_SHEET=json.load(renpy.file("assets/room13-evidence-icons.json")) if renpy.loadable("assets/room13-evidence-icons.json") else {}
    def r13_record_icon(key):
        if isinstance(key,str) and key.startswith(("bag:","tool:")):return r13_catalog_object_icon(key)
        # Testimony portraits come only from authored evidence_sources.
        who=ROOM13["evidence_sources"].get(key) if r13_record_category(key)=="testimony" else None
        if who:return r13_art(who,"avatar_neutral")
        # Use the same authored object in every picker, not just the large detail view.
        evidence_path=globals().get("r13_evidence_art_path",lambda key:None)(key)
        if evidence_path:return evidence_path
        art=r13_material_art(key)
        if art is not None:return art
        if key in R13_RECORD_ICON_SHEET:
            spec=R13_RECORD_ICON_SHEET[key]
            return Crop(tuple(spec["crop"]),spec["file"])
        return r13_evidence_art(key) or ("assets/evidence.png" if ROOM13["evidence"][key]["kind"]=="물증" else "assets/record.png")
    def r13_record_origin(key):
        rec=(store.room13 or {}).get("records",{}).get(key)
        if not rec:return "이번 여정에서 얻은 자료"
        return "%d일 · %s · %s"%(rec["day"],("오전","오후","저녁","늦은 저녁")[min(rec.get("period",0),3)],R13_PLACES.get(rec.get("place"),(rec.get("place",""),))[0])
    def r13_calendar_promises():
        state=store.room13 or {}
        day=state.get("day",1)
        flags=state.get("flags",[])
        promises=[]
        if day<=R13_CASE_DAY and "elder_appointment" in flags:
            promises.append("%d일째 · %s요일 저녁 — 어르신과 만나기로 했다."%(R13_CASE_DAY,r13_weekday(R13_CASE_DAY)))
        if day<=R13_TRIAL_DAY and "trial_notice" in flags:
            promises.append("%d일째 · %s요일 — 다람이의 사건을 주민 앞에서 다룬다."%(R13_TRIAL_DAY,r13_weekday(R13_TRIAL_DAY)))
        if day==13 and "day13_warning" in state.get("events",[]):
            promises.append("14일째 · "+r13_weekday(14)+"요일 동틀 무렵 — 제단으로 끌고 간다는 말을 전해 받았다.")
        return promises

    def r13_met_people():
        # Old saves may lack encounter rows. Infer only actual conversations or
        # direct presentations from this save, never persistent reads from a run.
        state=store.room13 or {}
        people=[e.get("person") for e in state.get("encounters",[]) if isinstance(e,dict)]
        people.extend(ROOM13["topics"][key]["npc"] for key in state.get("read_topics",[]) if key in ROOM13["topics"])
        people.extend(who for who,items in state.get("resident_knowledge",{}).items() if items)
        return list(dict.fromkeys(who for who in people if who in R13_NAMES))
    def r13_history_stamp(entry):
        if not getattr(store,"room13_mode",False) or not store.room13:return
        entry.r13_recorded=True
        entry.r13_thought=bool(getattr(store,"r13_thought_active",False))
        entry.r13_person=getattr(store,"dialogue_speaker",None)
        entry.r13_day=store.room13.get("day")
        # The opening carriage has no map location; room13 already says "gate".
        entry.r13_place="carriage" if getattr(store,"place",None)=="마차 안" else store.room13.get("location")
    config.history_length=max(config.history_length or 0,250)
    config.history_callbacks.append(r13_history_stamp)
    def r13_history_rows():
        rows=[]
        for entry in reversed(getattr(store,"_history_list",[]) or []):
            if not getattr(entry,"what",None):continue
            who=getattr(entry,"who",None)
            thought=getattr(entry,"r13_thought",False)
            kind="독백" if thought else ("발언" if who else "서술")
            place=getattr(entry,"r13_place",None)
            day=getattr(entry,"r13_day",None)
            place_name="마차 안" if place=="carriage" else R13_PLACES.get(place,(place or "",))[0]
            stamp=("%d일 · %s"%(day,place_name)) if day is not None else "이전 저장의 대화"
            rows.append(dict(who=who or "서술",kind=kind,stamp=stamp,
                what=renpy.filter_text_tags(entry.what,allow=["b","i","u","s","color"])))
        return rows

init 71:
    style r13_paper_tab_button is r13_compact_button:
        background R13PaperPanel(False)
        hover_background R13PaperPanel(True)
        selected_background R13ControlSurface(chosen=True)
    style r13_paper_tab_button_text is r13_compact_button_text:
        color "#303d38"
        hover_color "#724b39"
        selected_color "#fff0ce"
        insensitive_color "#72786a"


screen r13_reference_record_shell(title):
    add Solid("#211b1899")
    add R13TravelSheet() xpos 36 ypos 36 xsize 1208 ysize 640
    add Solid("#d6bd96") xpos 54 ypos 54 xsize 200 ysize 596
    text title xpos 76 ypos 72 size 24 color "#493b30" font r13_ui_font()

screen r13_reference_record_categories(owner,current,present=False,archive=False):
    vbox:
        xpos 66 ypos 128 spacing 10
        # 0.19.2 빼기 정리: 탭 6 → 4. 인물은 「사람」(관계도)에, 달력은 「메모」 안으로 합쳤다.
        for key,title,icon in (("all","자료","record"),("relations","사람","people"),("dialogue","대화","dialogue"),("notes","메모","investigate")):
            if not present or key=="all":
                button:
                    style "r13_paper_tab_button" xsize 176 ysize (80 if r13_touch_ui() else 56)
                    selected (current==key or (key=="notes" and current=="calendar") or (key=="relations" and current=="people")) alt title
                    action ((Show("r13_learning_notes") if key=="notes" and isinstance(owner,str) else
                        [Function(r13_record_select,owner,"category" if owner=="r13_book" else "tab",key),Function(r13_record_select,owner,"detail",None),Function(r13_record_select,owner,"page",0)]))
                    hbox:
                        xalign .5 yalign .5 spacing 10
                        add R13AntiqueIcon(icon,size=24) yalign .5
                        text title size r13_read_size(20,24) font r13_ui_font() color ("#fff0ce" if current==key else "#493b30") yalign .5

    if r13_v111_active() and not present:
        textbutton "갈림길":
            style "r13_paper_tab_button" xpos 66 ypos (488 if r13_touch_ui() else 392)
            xsize 176 ysize (80 if r13_touch_ui() else 56) text_size r13_read_size(20,24)
            action Show("r13_fork_screen")

screen r13_record_filters(owner,order,archive=False):
    hbox:
        xpos 280 ypos 76 spacing 10
        textbutton ("최근 획득순" if order=="recent" else "발견 순서"):
            style "r13_compact_button" xsize 246 ysize 42 text_size 19
            action [Function(r13_record_select,owner,"order","acquired" if order=="recent" else "recent"),Function(r13_record_select,owner,"page",0)]

# 0.20.x: the 자료 tab's filters, picture grid and detail (r13_material_filters / r13_material_grid /
# r13_material_detail) moved to systems/room13_evidence_view.rpy (증거 비교 창, plan5 m2a/m2b).
# They were only ever `use`d inside r13_records / r13_book, never shown on their own.

# 0.19.2: 「인물」 탭을 「사람」(관계도)에 합치며, 인물 기록은 관계도 오른쪽 상세 아래에 붙는다.
screen r13_person_brief(person):
    vbox:
        spacing 8
        $ topics=r13_note_topics(person)
        $ shown=[e.split(":")[0] for e in room13.get("resident_knowledge",{}).get(person,[]) if e.split(":")[0] in ROOM13["evidence"]]
        if topics:
            text ("들은 이야기 · %d"%len(topics)) size r13_read_size(17,20) color "#765426"
            for title in topics:
                text ("· "+title) size r13_read_size(16,19) color "#493b30" xsize 286
        if shown:
            text ("보여 준 자료 · %d"%len(shown)) size r13_read_size(17,20) color "#765426"
            for record_id in shown:
                text ("· "+ROOM13["evidence"][record_id]["name"]) size r13_read_size(16,19) color "#625738" xsize 286

screen r13_records(initial_tab="all",note_focus=None,close_action=None,target=None,present_action=None):
    style_prefix "r13"
    on "show" action Function(r13_unread_hold.clear)
    modal True
    zorder 50
    on "show" action Function(source_fx,"note_open")
    default tab=(initial_tab if initial_tab!="all" else r13_records_view.get("tab","all"))
    $ tab="all" if tab in ("evidence","testimony","items","compare") else tab
    $ tab="relations" if tab=="people" else tab
    default detail=r13_records_view.get("detail")
    default person=r13_records_view.get("person")
    default page=r13_records_view.get("page",0)
    default page_restored=False
    default archive=r13_records_view.get("archive",False)
    default order="recent"
    default shelf=False
    default material_filter=r13_records_view.get("material_filter","all")
    default rel_sel=r13_records_view.get("rel_sel")
    default rel_filter="all"
    $ rel_filter="all" # Retired status filter must not survive an old saved screen.
    default rel_focus=r13_records_view.get("rel_focus",True)
    # 2026-10-24 증거 서랍(v111): 이번 사건 / 지난 사건 / 사람별. 옛 저장의 화면 기억에는 없으므로 이번 사건부터.
    default drawer=r13_records_view.get("drawer","now")
    default drawer_case=r13_records_view.get("drawer_case")
    default drawer_gpage=0
    default drawer_ipage=0
    on "hide" action [Function(source_fx,"note_close"),Function(r13_records_remember,tab,detail,person,page,archive,rel_sel,rel_filter,rel_focus,material_filter,drawer,drawer_case)]
    # 0.20.x 증거 비교 창: a comparison pair is never restored from an older save's screen.
    default pair=None
    default pair_slot=1
    if r13_meeting_active and r13_meeting_claim in R13_DEBATE:
        use r13_meeting_stage(r13_meeting_claim,r13_meeting_focus_person(r13_meeting_claim),True)
    if tab=="all":
        # 0.20.x 증거 비교 창 (owner-approved plan5 m2a/m2b, 2026-10-22): brown sheet with top tabs,
        # one big picture with a few observed facts, 「나란히 놓기」 for two records side by side.
        # systems/room13_evidence_view.rpy. The other tabs keep the paper folio below.
        $ material_filter="all" if material_filter=="unread" or (archive and material_filter=="transfer") else material_filter
        if r13_drawer_active(archive):
            # 2026-10-24 증거 서랍 (시안 docs/reviews/evidence-drawer-20261024/, systems/room13_evidence_drawer.rpy).
            $ drawer_all=r13_catalog_entries()
            $ drawer_view=r13_drawer_view(drawer,drawer_all,detail,drawer_case)
            $ header=r13_drawer_header(drawer,drawer_all,drawer_view,drawer_case)
            use r13_ink_record_shell("기록",r13_ev_record_tabs(_scope),"all",(close_action or Hide("r13_records")))
            $ drawer_chips=r13_drawer_chips(_scope,drawer,(False if r13_learning_archive_keys() else None))
            use r13_ink_chips(drawer_chips)
            if drawer_view[0]=="groups":
                use r13_drawer_groups_view(drawer,drawer_all,drawer_case,drawer_gpage,drawer_ipage,_scope,header)
            else:
                $ entries=drawer_view[1]
                if not page_restored:
                    $ page=r13_record_restore_page(entries,detail,page)
                    $ page_restored=True
                $ selected_record=r13_drawer_selected(entries,detail,page)
                use r13_evidence_browser(entries,selected_record,page,_scope,pair,pair_slot,False,("records",),header)
            # 2026-10-24 수첩 목표 칸(systems/room13_goal_strip.rpy): 탭 줄과 칩 사이 빈자리. 펼친 판이 위에 오도록 맨 끝에 둔다.
            use r13_goal_strip(r13_ev_tab_x("기록")+(len(r13_ev_record_tabs(_scope))-1)*R13_EV_TAB_PITCH+88,r13_ev_chip_boxes(drawer_chips)[0][0])
        else:
            $ entries=r13_material_subset(r13_catalog_entries(archive,shelf=shelf and not archive),material_filter)
            if not page_restored:
                $ page=r13_record_restore_page(entries,detail,page)
                $ page_restored=True
            $ selected_record=r13_record_selected(entries,detail,page)
            $ day_span=r13_evidence_day_span(entries)
            $ header=(("지난 사건 %d개" if shelf and not archive else "자료 %d개")%len(entries))+((" · "+day_span) if day_span else "")
            use r13_ink_record_shell("기록",r13_ev_record_tabs(_scope),"all",(close_action or Hide("r13_records")))
            use r13_ink_chips(r13_ev_filter_chips(_scope,material_filter,not archive,(None if archive else shelf),len(r13_catalog_entries(shelf=True)),(archive if archive or r13_learning_archive_keys() else None)))
            use r13_evidence_browser(entries,selected_record,page,_scope,pair,pair_slot,archive,("records",),header)
    else:
        use r13_reference_record_shell("기록")
        use r13_reference_record_categories(_scope,tab,archive=archive)
        if tab=="relations":
            use r13_relations_content(_scope,rel_sel,rel_filter,rel_focus)
        elif tab=="notes":
            use r13_learning_notes_content(note_focus)
            textbutton "달력 ›" style "r13_paper_tab_button" xpos 1090 ypos 70 xsize 120 ysize (56 if r13_touch_ui() else 40) text_size (22 if r13_touch_ui() else 18) action Function(r13_record_select,_scope,"tab","calendar")
        elif tab=="calendar":
            use r13_calendar_content()
            textbutton "‹ 메모" style "r13_paper_tab_button" xpos 400 ypos 70 xsize 120 ysize (56 if r13_touch_ui() else 40) text_size (22 if r13_touch_ui() else 18) action Function(r13_record_select,_scope,"tab","notes")
        elif tab=="items":
            use r13_item_bag_content()
        else:
            text "실제로 지나간 대화" xpos 292 ypos 88 size 23 color "#65503b"
            viewport:
                area (280,134,930,472) mousewheel True draggable True scrollbars "vertical"
                vbox:
                    spacing 12
                    for row in r13_history_rows():
                        frame:
                            xsize 900 padding (16,12) background R13PaperPanel()
                            vbox:
                                spacing 6
                                text (row["who"]+" · "+row["stamp"]) size 17 color "#625738" xsize 864
                                text row["what"] size r13_read_size(21,26) color (r13_role_color("thought","paper") if row["kind"]=="독백" else r13_role_color("narration","paper") if row["kind"]=="서술" else r13_role_color("speech","paper")) xsize 864
        textbutton "닫기" style "r13_compact_button" xpos 66 ypos r13_record_footer_y() xsize 176 ysize r13_record_footer_height() text_size r13_read_size(20,23) action (close_action or Hide("r13_records"))
    key "game_menu" action (close_action or Hide("r13_records"))

screen r13_resident_notes():
    style_prefix "r13"
    modal True
    zorder 60
    default selected=None
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    add Solid("#eee7d6")
    text "다람이의 수첩 · 만난 사람들" xpos 55 ypos 35 size 32 color "#765426"
    viewport:
        area (55,115,455,495) mousewheel True draggable True scrollbars "vertical"
        vbox:
            spacing 10
            for person in r13_met_people():
                button:
                    xsize 420 ysize 82 padding (8,8)
                    background R13PaperPanel(selected==person)
                    action SetScreenVariable("selected",person) sensitive ready
                    hbox:
                        spacing 16
                        add Transform(r13_art(person,"avatar_neutral"),size=(60,62),fit="contain",nearest=r13_profile_nearest(person))
                        text r13_display_name(person) size 23 yalign .5
            if not r13_met_people():
                text "직접 이야기한 사람부터 기록한다." size 23 xsize 410
    if selected:
        text r13_display_name(selected) xpos 565 ypos 112 size 32 color "#765426"
        text r13_display_role(selected) xpos 565 ypos 156 size 20 color "#625738"
        viewport:
            area (565,185,650,420) mousewheel True draggable True scrollbars "vertical"
            vbox:
                spacing 14
                text "직접 만난 때와 장소" size 24 color "#496450"
                for meeting in room13["encounters"]:
                    if isinstance(meeting,dict) and meeting["person"]==selected:
                        text ("%d일 · %s · %s"%(meeting["day"],("오전","오후","저녁","늦은 저녁")[meeting["period"]],R13_PLACES[meeting["place"]][0])) size 21
                text "들은 이야기" size 24 color "#496450"
                for title in r13_note_topics(selected):
                    text ("· "+title) size 21 xsize 600
                $ disclosed=room13["resident_knowledge"].get(selected,[])
                if disclosed:
                    text "내가 보여 준 자료" size 24 color "#765426"
                    for item in disclosed:
                        $ eid=item.split(":")[0]
                        text (ROOM13["evidence"][eid]["name"]+(" · 이름도 공개함" if item.endswith(":named") else " · 이름은 숨김" if eid=="E10" else "")) size 21 xsize 600
    text "앞으로의 일정은 쓰여 있지 않다. 직접 만난 기록으로 짐작해 보자." xpos 55 ypos 625 size 20 color "#717367"
    textbutton "닫기" xpos 55 ypos 670 action Hide("r13_resident_notes") sensitive ready text_size 23
