# Owner's test tool (0.18.22). Hidden from players.
#   Turn on: open the game with ?admin=1 in the address, or press Shift+A in the field.
#   Then a "관리자" button sits at the top of the field. It offers:
#     - 다음 진행 조건: what the current day needs, what is here, whether sleep is open and why not.
#     - 클릭 영역 보기: draws every pressable object in the room with its name.
#     - jumps: day/period/place, preset starting points, money, items, evidence, flags.
#   Every change goes through the normal state (r13_edit) and then re-enters the field, so the game
#   behaves as if the player had got there. Nothing here is saved across new games.
default persistent.room13_admin=False
default r13_admin_hitboxes=False

init 131 python:
    def r13_admin_url_check():
        try:
            if renpy.emscripten and "admin=1" in renpy.emscripten.run_script_string("window.location.search"):
                persistent.room13_admin=True
        except Exception:
            pass
    config.start_callbacks.append(r13_admin_url_check)

    def r13_admin_toggle():
        persistent.room13_admin=not persistent.room13_admin
        renpy.notify("관리자 도구 "+("켜짐" if persistent.room13_admin else "꺼짐"))
        renpy.restart_interaction()

    R13_ADMIN_PRESETS=[
        ("1일 · 13호 도착 직후",dict(day=1,period=1,location="room13"),["entry_corrected","lodging"],[]),
        ("2일 아침 · 여관",dict(day=2,period=0,location="inn"),["entry_corrected","lodging","livelihood_open"],["E01","E02","M01","E03"]),
        ("3일 아침 · 광장",dict(day=3,period=0,location="square"),["entry_corrected","lodging","livelihood_open"],["E01","E02","M01","E03"]),
        ("%d일 저녁 · 사건 전"%R13_CASE_DAY,dict(day=R13_CASE_DAY,period=2,location="inn"),["entry_corrected","lodging","livelihood_open"],["E01","E02","M01","E03"]),
        ("%d일 아침 · 사건 뒤"%(R13_CASE_DAY+1),dict(day=R13_CASE_DAY+1,period=0,location="inn",case_state="occurred",victim_state="dead",daram_state="held"),["entry_corrected","lodging","livelihood_open"],["E01","E02","M01","E03"]),
        ("%d일 아침 · 둘째 주"%R13_WEEK2_DAY,dict(day=R13_WEEK2_DAY,period=0,location="inn",case_state="occurred",trial_ended=True,week2_started=True),["entry_corrected","lodging","livelihood_open"],["E01","E02","M01","E03"]),
    ]

    def r13_admin_apply(state=None,flags=(),evidence=(),fresh=False):
        n=winter_copy.deepcopy(r13_new() if fresh else store.room13)
        n.update(state or {})
        n["flags"]=list(dict.fromkeys(list(n.get("flags",[]))+list(flags)))
        n["evidence"]=list(dict.fromkeys(list(n.get("evidence",[]))+[e for e in evidence if e in ROOM13["evidence"]]))
        n.setdefault("life_poc",True)
        store.room13=n
        r13_upgrade()

    def r13_admin_preset(index):
        title,state,flags,evidence=R13_ADMIN_PRESETS[index]
        r13_admin_apply(state,flags,evidence,fresh=True)
        store.room13["life_poc"]=True
        renpy.notify("이동: "+title)

    def r13_admin_cash(amount):
        n=winter_copy.deepcopy(store.room13);w=r13_wallet(n);w["cash"]=max(0,w["cash"]+amount);n["livelihood"]=w;store.room13=n

    def r13_admin_give_item(key):
        n=winter_copy.deepcopy(store.room13);w=r13_wallet(n)
        if key not in w["items"]:w["items"].append(key)
        n["livelihood"]=w;store.room13=n

    def r13_admin_items():
        keys=list(R13_SHOP)+list(globals().get("R13_BORROW",{}))
        return [(k,(R13_SHOP.get(k) or R13_BORROW.get(k))["title"]) for k in keys]

    def r13_admin_next():
        """Plain lines: what the current point needs. Read-only."""
        s=store.room13 or {};lines=[]
        place=R13_PLACES.get(s.get("location"),("?",))[0] if s.get("location") in R13_PLACES else s.get("location")
        lines.append("%d일째 · %s · %s"%(s.get("day",1),("아침","오후","저녁","밤")[min(s.get("period",0),3)],place))
        goal=(r13_intro_goal() if s.get("day",1)<=2 else None) or r13_campaign_goal()
        if goal:lines.append("현재 목표 줄 · "+goal)
        if s.get("day")==1:
            for label,ok in (("입구 확인(entry_corrected)",r13_has("entry_corrected")),("여관 숙소(lodging)",r13_has("lodging")),
                    ("엄마의 메모 M01 · 13호 책상 위 접힌 종이",r13_has("M01")),("엄마의 바느질 E03 · 13호 침대",r13_has("E03"))):
                lines.append(("완료 · " if ok else "필요 · ")+label)
        if r13_bed_available("bed"):
            lines.append("잠자기 · 가능 (침대를 누르거나 '자기')")
        elif r13_has("lodging"):
            reason=r13_bed_blocked_reason("bed") if s.get("location") in ("room13","guestroom") else None
            lines.append("잠자기 · "+(reason or "숙소 방(13호 또는 임시 객실)에서만 가능"))
        objs=[k for k,spec in ROOM13["objects"].get(s.get("location"),{}).items() if r13_object_visible(spec)]
        unseen=[r13_object_name(k) for k in objs if not r13_has("observed:%s:%s"%(s.get("location"),k))]
        if objs:lines.append("이곳에서 누를 수 있는 것 %d개 · 아직 안 본 것: %s"%(len(objs),", ".join(unseen) if unseen else "없음"))
        people=[R13_NAMES.get(p,p) for p in r13_people()]
        if people:lines.append("이곳 사람 · "+", ".join(people))
        acts=[spec["title"] for k in objs for a,spec in r13_object_actions(k)]
        if acts:lines.append("이곳 활동 · "+" / ".join(acts))
        offers=[t for k,t in r13_offers_here()]
        if offers:lines.append("일반 사건 표시 · "+" / ".join(offers))
        lines.append("일자리 · "+("열림" if r13_has("livelihood_open") else "아직 (2일째 까로가 제안)"))
        lines.append("가진 돈 %d냥 · 물건 %s"%(r13_wallet(s)["cash"],", ".join(r13_wallet(s)["items"]) or "없음"))
        lines.append("자료 %d개 · %s"%(len(s.get("evidence",[]))," ".join(s.get("evidence",[]))))
        return lines

screen r13_admin_key():
    # Used inside r13_hub (a modal screen): Shift+A toggles the tool in the field.
    if room13:
        key "shift_K_a" action Function(r13_admin_toggle)
        if persistent.room13_admin:
            textbutton "관리자":
                style "r13_action_button" xpos 620 ypos 96 xanchor .5 padding (14,6) text_size 18
                background Solid("#7a2a1ee6") hover_background Solid("#a83a28")
                action Show("r13_admin")

screen r13_admin_hitboxes():
    if r13_admin_hitboxes and persistent.room13_admin:
        for key,spec in ROOM13["objects"].get(room13["location"],{}).items():
            if r13_object_visible(spec):
                $ x,y,w,h=spec["rect"]
                add Solid("#ff3b3b30",xsize=w,ysize=h) xpos x ypos y
                add R13HoverCorners(w,h,"#ff5a3c",3) xpos x ypos y
                text r13_object_name(key) xpos x+4 ypos y+2 size 16 color "#fff" outlines [(2,"#000",0,0)]

screen r13_admin():
    modal True
    zorder 120
    style_prefix "r13"
    default tab="next"
    add Solid("#071015ee")
    text "관리자 도구 · 테스트 전용" xpos 40 ypos 24 size 30 color "#ff9a7a"
    hbox:
        xpos 40 ypos 72 spacing 10
        for key,title in (("next","다음 진행 조건"),("jump","이동·시점"),("give","돈·물건·자료")):
            textbutton title style "r13_action_button" xsize 230 ysize 46 text_size 20 selected tab==key action SetScreenVariable("tab",key)
        textbutton ("클릭 영역 보기: "+("켬" if r13_admin_hitboxes else "끔")) style "r13_action_button" xsize 260 ysize 46 text_size 20 action ToggleVariable("r13_admin_hitboxes")
    viewport:
        area (40,134,1200,500) mousewheel True draggable True scrollbars "vertical"
        vbox:
            spacing 10
            if tab=="next":
                textbutton "회의 바로 테스트 (진행 보존)" style "r13_action_button" text_size 21 padding (16,10) action Show("r13_admin_meeting_picker")
                for line in r13_admin_next():
                    text line size 21 color ("#ffd27a" if line.startswith("필요 ·") else "#e8efe8") xsize 1150
            elif tab=="jump":
                text "시작 지점 (새 회차 상태로 바꿈)" size 21 color "#f6d18a"
                hbox:
                    box_wrap True spacing 8 xsize 1150
                    for i,(title,_s,_f,_e) in enumerate(R13_ADMIN_PRESETS):
                        textbutton title style "r13_action_button" text_size 18 padding (12,8) action [Function(r13_admin_preset,i),Hide("r13_admin"),Jump("r13_field")]
                text "날짜·시간 (지금 상태에서)" size 21 color "#f6d18a"
                hbox:
                    spacing 8
                    textbutton "하루 앞으로" style "r13_action_button" text_size 18 padding (12,8) action [Function(r13_admin_apply,dict(day=min(14,room13["day"]+1),period=0)),Hide("r13_admin"),Jump("r13_field")]
                    textbutton "하루 뒤로" style "r13_action_button" text_size 18 padding (12,8) action [Function(r13_admin_apply,dict(day=max(1,room13["day"]-1),period=0)),Hide("r13_admin"),Jump("r13_field")]
                    for p,title in ((0,"아침"),(1,"오후"),(2,"저녁")):
                        textbutton title style "r13_action_button" text_size 18 padding (12,8) action [Function(r13_admin_apply,dict(period=p)),Hide("r13_admin"),Jump("r13_field")]
                text "장소 (조건 무시하고 바로 이동)" size 21 color "#f6d18a"
                hbox:
                    box_wrap True spacing 8 xsize 1150
                    for key in R13_PLACES:
                        textbutton R13_PLACES[key][0] style "r13_action_button" text_size 18 padding (12,8) action [Function(r13_admin_apply,dict(location=key)),Hide("r13_admin"),Jump("r13_field")]
            else:
                hbox:
                    spacing 8
                    textbutton "+10냥" style "r13_action_button" text_size 18 padding (12,8) action Function(r13_admin_cash,10)
                    textbutton "+50냥" style "r13_action_button" text_size 18 padding (12,8) action Function(r13_admin_cash,50)
                    textbutton "일자리 열기" style "r13_action_button" text_size 18 padding (12,8) action Function(r13_flag,"livelihood_open")
                text "물건 받기" size 21 color "#f6d18a"
                hbox:
                    box_wrap True spacing 8 xsize 1150
                    for key,title in r13_admin_items():
                        textbutton title style "r13_action_button" text_size 17 padding (10,6) action Function(r13_admin_give_item,key) selected key in r13_wallet(room13)["items"]
                text "자료 받기 (누르면 바로 기록됨)" size 21 color "#f6d18a"
                hbox:
                    box_wrap True spacing 6 xsize 1150
                    for key in sorted(ROOM13["evidence"]):
                        textbutton (key+" "+ROOM13["evidence"][key]["name"]):
                            style "r13_action_button" text_size 15 padding (8,5)
                            selected key in room13["evidence"]
                            action Function(r13_admin_apply,None,(),(key,))
    textbutton "닫기" style "r13_action_button" area (1040,650,200,54) text_size 22 action Hide("r13_admin")
    textbutton "관리자 끄기" style "r13_action_button" area (40,650,200,54) text_size 20 action [Function(r13_admin_toggle),Hide("r13_admin")]
    key "game_menu" action Hide("r13_admin")

# PIN entry from the settings screen (0.18.50, owner). Big buttons so it works on a phone.
define R13_ADMIN_PIN = "4861"

screen r13_admin_pin():
    modal True
    zorder 120
    default typed=""
    default wrong=False
    add Solid("#000000c8")
    frame:
        xalign .5 yalign .5 xsize 420 padding (24,20) background R13InkPanel()
        vbox:
            spacing 12 xalign .5
            text "관리자 핀 번호" size 26 color "#f6d18a" xalign .5
            text (("●"*len(typed)+"○"*(4-len(typed))) if len(typed)<=4 else "●●●●") size 34 color "#fff4df" xalign .5
            if wrong:
                text "번호가 맞지 않아요" size 19 color "#ff9a7a" xalign .5
            grid 3 4:
                spacing 8 xalign .5
                for k in ("1","2","3","4","5","6","7","8","9","지우기","0","확인"):
                    textbutton k:
                        xsize 110 ysize 64 text_size (28 if len(k)==1 else 20) text_xalign .5
                        action (SetScreenVariable("typed",typed[:-1]) if k=="지우기"
                            else Function(r13_admin_pin_check,typed) if k=="확인"
                            else [SetScreenVariable("typed",(typed+k)[:4]),SetScreenVariable("wrong",False)])
            textbutton "닫기" xalign .5 xsize 200 ysize 52 text_size 21 action Hide("r13_admin_pin")
    key "game_menu" action Hide("r13_admin_pin")

init 132 python:
    def r13_admin_pin_check(typed):
        screen=renpy.get_screen("r13_admin_pin")
        if typed==R13_ADMIN_PIN:
            persistent.room13_admin=True
            renpy.hide_screen("r13_admin_pin")
            renpy.notify("관리자 도구가 켜졌어요. 마을 화면 위쪽 ‘관리자’ 버튼을 누르세요.")
        else:
            if screen:
                screen.scope["typed"]=""
                screen.scope["wrong"]=True
        renpy.restart_interaction()

