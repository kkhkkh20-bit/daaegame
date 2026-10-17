default r13_present_priority = None
default r13_book_views = {}

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
        "E36":"전날 진료요청","E37":"잠금 작동기록","G1":"예약 원본","G2":"아이 보호 규칙","G3":"옮겨 쓴 목록",
    }
    R13_RECORD_PAGE_SIZE=12
    def r13_book_context(target,hearing):
        if hearing:
            return ("meeting",getattr(store,"r13_meeting_claim",None),getattr(store,"r13_debate_selected",None))
        return ("person",target)

    def r13_book_remember(context,detail,page):
        views=dict(getattr(store,"r13_book_views",{}))
        views[context]=dict(detail=detail,page=page)
        store.r13_book_views=views

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
    def r13_record_page_size():return 8 if getattr(persistent,"room13_large_text",False) else R13_RECORD_PAGE_SIZE
    def r13_record_pages(entries):return max(1,(len(entries)+r13_record_page_size()-1)//r13_record_page_size())
    def r13_record_page(entries,page):return max(0,min(page,r13_record_pages(entries)-1))
    def r13_record_selected(entries,detail,page):
        visible=entries[r13_record_page(entries,page)*r13_record_page_size():][:r13_record_page_size()]
        return detail if detail in visible else (visible[0] if visible else None)
    def r13_record_select(owner,variable,value,mark_seen=True):
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
        selected_background R13InkPanel(focused=True)
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
        for key,title in (("all","자료"),("people","인물"),("relations","관계도"),("dialogue","대화")):
            if not present or key=="all":
                button:
                    style "r13_paper_tab_button" xsize 176 ysize 56
                    selected current==key alt title
                    action [Function(r13_record_select,owner,"category" if owner=="r13_book" else "tab",key),Function(r13_record_select,owner,"detail",None),Function(r13_record_select,owner,"page",0)]
                    hbox:
                        xalign .5 yalign .5 spacing 10
                        add R13AntiqueIcon("record" if key=="all" else ("people" if key=="relations" else key),size=24) yalign .5
                        text title size r13_read_size(20,24) font r13_ui_font() color ("#fff0ce" if current==key else "#493b30") yalign .5
    if not present:
        vbox:
            xpos 66 ypos 382 spacing 12
            textbutton "조사 메모" style "r13_paper_tab_button" xsize 176 ysize 48 text_size 18 selected current=="notes" action (Function(r13_record_select,owner,"tab","notes") if not isinstance(owner,str) else Show("r13_learning_notes"))
            textbutton "달력" style "r13_paper_tab_button" xsize 176 ysize 48 text_size 18 selected current=="calendar" action (Function(r13_record_select,owner,"tab","calendar") if not isinstance(owner,str) else Show("r13_calendar"))

screen r13_record_filters(owner,order,archive=False):
    hbox:
        xpos 280 ypos 76 spacing 10
        textbutton ("최근 획득순" if order=="recent" else "발견 순서"):
            style "r13_compact_button" xsize 246 ysize 42 text_size 19
            action [Function(r13_record_select,owner,"order","acquired" if order=="recent" else "recent"),Function(r13_record_select,owner,"page",0)]

screen r13_material_grid(entries,detail,page,owner,archive=False):
    $ actual_page=r13_record_page(entries,page)
    $ page_size=r13_record_page_size()
    $ columns=3 if persistent.room13_large_text else 4
    $ cell=166 if persistent.room13_large_text else 124
    $ visible=entries[actual_page*page_size:][:page_size]
    add R13PaperFrame() xpos 278 ypos 132 xsize 520 ysize 440
    for index in range(page_size):
        $ key=visible[index] if index<len(visible) else None
        button:
            area (290+(index%columns)*cell,146+(index//columns)*140,cell-5,136)
            padding (6,6) background R13PaperPanel(key is not None and detail==key,transferable=bool(key and not archive and r13_catalog_transferable(key)))
            action (Function(r13_record_select,owner,"detail",key,not archive) if key else NullAction())
            sensitive key is not None
            if key:
                vbox:
                    xalign .5 yalign .5 spacing 6
                    add Transform(r13_record_icon(key),xysize=(52,52),fit="contain",nearest=True) xalign .5
                    text (("● " if not archive and r13_record_unread(key) else "")+R13_RECORD_SHORT.get(key,r13_catalog_title(key)[:8])):
                        size r13_read_size(16,21) color "#493b30" xsize cell-20 text_align .5
                    if not archive and r13_catalog_transferable(key):
                        text "전달 가능" size 14 color "#795714" xalign .5
    hbox:
        xpos 302 ypos 584 spacing 12
        textbutton "‹ 이전" style "r13_compact_button" xsize 132 ysize 82 text_size 19 sensitive actual_page>0 action Function(r13_record_select,owner,"page",actual_page-1)
        text ("%d / %d"%(actual_page+1,r13_record_pages(entries))) size 19 color "#65503b" yalign .5 xsize 124 text_align .5
        textbutton "다음 ›" style "r13_compact_button" xsize 132 ysize 82 text_size 19 sensitive actual_page+1<r13_record_pages(entries) action Function(r13_record_select,owner,"page",actual_page+1)
    if not entries:
        text "아직 모은 자료가 없습니다." xpos 300 ypos 540 size 18 color "#625738" xsize 470 text_align .5

screen r13_material_detail(detail,archive=False):
    add R13PaperFrame() xpos 820 ypos 58 xsize 406 ysize 512
    if detail:
        if not archive and r13_record_unread(detail):
            timer .7 action Function(r13_record_mark_seen,detail)
        $ ev=r13_catalog_record(detail)
        add Transform(r13_record_icon(detail),xysize=(132,128),fit="contain",nearest=True) xpos 954 ypos 78
        text ev["name"] xpos 842 ypos 218 xsize 362 text_align .5 size r13_read_size(23,28) color "#6c512a"
        viewport:
            area (844,266,358,274) mousewheel True draggable True scrollbars "vertical"
            vbox:
                spacing 12
                if not archive and r13_catalog_transferable(detail):
                    text "전달 가능 · 보여준 뒤 결정" size 17 color "#795714" xsize 332
                text ev["establishes"] size r13_read_size(21,26) color "#493b30" xsize 332
                text ("지난 플레이에서 찾은 것 · 지금은 보여줄 수 없음" if archive else r13_catalog_origin(detail)) size 17 color "#625738" xsize 332
                if not archive and detail in ROOM13["evidence"]:
                    text r13_learning_record_status(detail) size 17 color "#555943" xsize 332
                if not archive and detail in room13.get("records",{}):
                    text ("얻은 곳: "+room13["records"][detail]["source"]) size 17 color "#625738" xsize 332
    else:
        text "자료를 선택하세요." xpos 846 ypos 278 xsize 354 text_align .5 size 21 color "#625738"

screen r13_person_record_detail(person):
    add R13PaperFrame() xpos 820 ypos 58 xsize 406 ysize 512
    if person:
        add Transform(r13_art(person,"avatar_neutral"),xysize=(132,128),fit="contain",nearest=True) xpos 954 ypos 78
        text r13_person_caption(person) xpos 840 ypos 218 xsize 366 text_align .5 size r13_read_size(23,28) color "#6c512a"
        viewport:
            area (844,266,358,278) mousewheel True draggable True scrollbars "vertical"
            vbox:
                spacing 12
                for meeting in room13.get("encounters",[]):
                    if isinstance(meeting,dict) and meeting.get("person")==person:
                        text ("%d일 · %s · %s"%(meeting["day"],("오전","오후","저녁","늦은 저녁")[meeting["period"]],R13_PLACES.get(meeting["place"],(meeting["place"],))[0])) size 18 color "#493b30" xsize 332
                for title in r13_note_topics(person):
                    text ("들은 이야기 · "+title) size 18 color "#493b30" xsize 332
                for entry in room13.get("resident_knowledge",{}).get(person,[]):
                    $ record_id=entry.split(":")[0]
                    if record_id in ROOM13["evidence"]:
                        text ("보여 준 자료 · "+ROOM13["evidence"][record_id]["name"]+(" (이름 공개)" if entry.endswith(":named") else " (이름 숨김)" if record_id=="E10" else "")) size 18 color "#625738" xsize 332
    else:
        text "직접 만난 사람부터 기록합니다." xpos 844 ypos 278 xsize 354 text_align .5 size 21 color "#625738"

screen r13_records(initial_tab="all",note_focus=None,close_action=None,target=None,present_action=None):
    style_prefix "r13"
    modal True
    zorder 50
    on "show" action Function(source_fx,"note_open")
    on "hide" action Function(source_fx,"note_close")
    default tab=initial_tab
    $ tab="all" if tab in ("evidence","testimony","items","compare") else tab
    default detail=None
    default person=None
    default page=0
    default archive=False
    default order="recent"
    default rel_sel=None
    default rel_filter="all"
    use r13_reference_record_shell("기록")
    use r13_reference_record_categories(_scope,tab,archive=archive)
    if tab=="all":
        if r13_learning_archive_keys():
            textbutton ("이번 여정" if not archive else "지난 플레이"):
                style "r13_paper_tab_button" xpos 66 ypos 326 xsize 176 ysize 40 text_size 18
                action [SetScreenVariable("archive",not archive),SetScreenVariable("detail",None),SetScreenVariable("page",0)]
        $ entries=r13_catalog_entries(archive)
        $ selected_record=r13_record_selected(entries,detail,page)
        text ("모은 자료 %d개"%len(entries)) xpos 284 ypos 78 size 22 color "#65503b"
        use r13_material_grid(entries,selected_record,page,_scope,archive)
        use r13_material_detail(selected_record,archive)
    elif tab=="people":
        $ people=r13_met_people()
        $ selected_person=r13_record_selected(people,person,page)
        $ actual_page=r13_record_page(people,page)
        $ visible=people[actual_page*r13_record_page_size():][:r13_record_page_size()]
        text "직접 만난 사람들" xpos 292 ypos 88 size 23 color "#65503b"
        add R13PaperFrame() xpos 278 ypos 132 xsize 520 ysize 440
        for index,who in enumerate(visible):
            button:
                area (292+(index%3)*164,146+(index//3)*104,158,98) padding (6,5) background R13PaperPanel(selected_person==who)
                action Function(r13_record_select,_scope,"person",who)
                vbox:
                    xalign .5 spacing 3
                    add Transform(r13_art(who,"avatar_neutral"),xysize=(58,58),fit="contain",nearest=True) xalign .5
                    text R13_NAMES[who] size 18 color "#493b30" xalign .5
        use r13_person_record_detail(selected_person)
        hbox:
            xpos 302 ypos 596 spacing 12
            textbutton "‹ 이전" style "r13_compact_button" xsize 132 ysize 82 text_size 19 sensitive actual_page>0 action SetScreenVariable("page",actual_page-1)
            text ("%d / %d"%(actual_page+1,r13_record_pages(people))) size 19 color "#65503b" yalign .5 xsize 124 text_align .5
            textbutton "다음 ›" style "r13_compact_button" xsize 132 ysize 82 text_size 19 sensitive actual_page+1<r13_record_pages(people) action SetScreenVariable("page",actual_page+1)
    elif tab=="relations":
        use r13_relations_content(_scope,rel_sel,rel_filter)
    elif tab=="notes":
        use r13_learning_notes_content(note_focus)
    elif tab=="calendar":
        use r13_calendar_content()
    elif tab=="items":
        use r13_item_bag_content()
    elif tab=="compare":
        use r13_compare_content(target,present_action)
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
    textbutton "닫기" style "r13_compact_button" xpos 66 ypos 594 xsize 176 ysize 44 text_size 20 action (close_action or Hide("r13_records"))
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
                        add Transform(r13_art(person,"avatar_neutral"),size=(60,62),fit="contain")
                        text R13_NAMES[person] size 23 yalign .5
            if not r13_met_people():
                text "직접 이야기한 사람부터 기록한다." size 23 xsize 410
    if selected:
        text r13_person_caption(selected) xpos 565 ypos 120 size 32 color "#765426"
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
