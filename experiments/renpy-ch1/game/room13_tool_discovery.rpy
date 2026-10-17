# Optional magnifier observations reuse existing facts. They never grant forensic
# evidence, open passages, spend/skip time, or replace an existing activity.
init 73 python:
    R13_TOOL_DISCOVERIES = {
        "seam":dict(place="room13",object="bed",evidence_id="E03",person="daram",topic="tool:seam",
            title="붉은 바느질",summary="이불 안쪽의 붉은 실과 매듭을 확대해 살폈다.",
            followup="다람이에게 엄마의 바느질과 닮았다고 한 부분을 물어볼 수 있다."),
        "plans":dict(place="workshop",object="plans",evidence_id="E04",person="buri",topic="tool:plans",
            title="도면의 겹친 선",summary="옛 구조의 선 위로 덧그린 선이 겹쳐 있음을 확대해 살폈다.",
            followup="부리에게 옛 선과 덧그린 선을 어떻게 비교할지 물어볼 수 있다."),
    }
    def r13_tool_target(key,state=None):
        state=store.room13 if state is None else state
        if not state or "magnifier" not in state.get("inspection_items",{}).get("inventory",[]):return None
        place=state.get("location")
        if "observed:"+str(place)+":"+key not in state.get("flags",[]):return None
        for name,spec in R13_TOOL_DISCOVERIES.items():
            if (place,key)!=(spec["place"],spec["object"]):continue
            if name=="seam" and "E03" not in state.get("evidence",[]):return None
            return name
        return None

    def r13_tool_available(key):
        if not r13_tool_target(key):return False
        spec=ROOM13["objects"].get(store.room13["location"],{}).get(key)
        return bool(spec and r13_object_visible(spec))

    def r13_tool_can_ask_child(key,state=None):
        state=store.room13 if state is None else state
        return bool(state and r13_tool_target(key,state)=="seam"
            and "seam" in state.get("tool_discoveries",{})
            and state.get("daram_state") in ("with_dad","rescued"))

    def r13_tool_transition(state,key):
        result=winter_copy.deepcopy(state)
        target=r13_tool_target(key,state)
        if not target:return result,False
        notes=result.setdefault("tool_discoveries",{})
        if target in notes:return result,False
        spec=R13_TOOL_DISCOVERIES[target]
        notes[target]=dict(day=state["day"],period=state["period"],place=state["location"],evidence_id=spec["evidence_id"])
        return result,True

    def r13_tool_record(key):
        if not r13_tool_available(key):return False
        next_state,changed=r13_tool_transition(store.room13,key)
        if changed:store.room13=next_state
        return changed

    def r13_tool_notes():
        # Old saves have no field; opening this list never migrates or writes.
        notes=(store.room13 or {}).get("tool_discoveries",{})
        return [dict(R13_TOOL_DISCOVERIES[key],id=key,day=value["day"],period=value["period"],place=value["place"])
            for key,value in notes.items() if key in R13_TOOL_DISCOVERIES]

    def r13_tool_art(key):
        target=r13_tool_target(key)
        if target=="seam":
            art=r13_evidence_art("E03")
            if art:return Transform(art,xysize=(690,400),fit="contain",nearest=True)
        location=store.room13["location"]
        rect=tuple(ROOM13["objects"][location][key]["rect"])
        background=r13_world_background(location) if r13_layout(location) else r13_background(R13_PLACES[location][1])
        return Transform(Crop(rect,background),xysize=(690,400),fit="contain",nearest=True)

    ROOM13["topics"]["tool:seam"]=dict(npc="daram",title="이 바느질이 엄마 것과 닮았다고 했지?",day=[1,13],need=["E03"],give=[],flags=[],lines=[
        ("dad","붉은 매듭이 잘 보이네. 엄마 바느질하고 닮았다고 했지?"),
        ("daram","응. 그래서 엄마 생각이 났어."),
        ("dad","네가 엄마 바느질하고 닮았다고 한 부분도 같이 적어 둘게."),
        ("daram","아빠, 실은 잡아당기지 마.")])
    ROOM13["topics"]["tool:plans"]=dict(npc="buri",title="도면에서 겹친 선은 어떻게 비교하면 됩니까?",day=[1,13],need=[],give=[],flags=[],lines=[
        ("dad","돋보기로 보니 옛 선 위로 다른 선이 겹쳐 있더구나."),
        ("buri","덧칠한 선만 따라가면 원래 벽을 놓쳐요. 옛 선과 덧선을 따로 짚어 보세요.")])
    r13_tool_base_topics=r13_topics
    def r13_topics(person):
        notes=(store.room13 or {}).get("tool_discoveries",{})
        locked={spec["topic"] for name,spec in R13_TOOL_DISCOVERIES.items() if name not in notes}
        return [(key,spec) for key,spec in r13_tool_base_topics(person) if key not in locked]

    r13_tool_base_present=r13_present
    def r13_present(person,key,identity=False):
        # Always retain the original consent/disclosure/unlock behavior first.
        response=r13_tool_base_present(person,key,identity)
        if key not in store.room13.get("evidence",[]):return response
        notes=store.room13.get("tool_discoveries",{})
        read=store.room13.get("read_topics",[])
        if person=="daram" and key=="E03" and "seam" in notes and "tool:seam" in read and store.room13.get("daram_state") in ("with_dad","rescued"):
            return [("daram","돋보기로 같이 봤던 거네. 내가 엄마 생각났다고 한 것도 적었어?"),
                ("dad","응. 네가 한 말 그대로 적었어.")]
        if person=="buri" and key=="E04" and "plans" in notes and "tool:plans" in read and store.room13["day"]<=R13_TRIAL_DAY:
            return [("buri","돋보기로 봤던 선도 표시했군요. 외벽과 비교한 길이는 여기 적혀 있고요."),
                ("dad","응. 옛 선과 덧그린 선을 섞지 않고 따로 적어 뒀어.")]
        return response

screen r13_tool_closeup(key):
    modal True
    zorder 94
    $ target=r13_tool_target(key)
    $ spec=R13_TOOL_DISCOVERIES[target]
    $ noted=target in room13.get("tool_discoveries",{})
    add Solid("#0c1d25f5")
    text ("돋보기 · "+spec["title"]) style "r13_title_text" color "#efd4a1" xpos 40 ypos 35
    frame:
        area (40,103,720,490) padding (15,18) background R13ActionPanel()
        add r13_tool_art(key) xalign .5 yalign .5
    frame:
        area (782,103,458,490) padding R13_UI_PADDING["panel"] background R13ActionPanel()
        vbox:
            spacing 18
            viewport:
                xsize 408 ysize 340 mousewheel True draggable True scrollbars "vertical"
                vbox:
                    spacing 14
                    text spec["summary"] size 24 color "#fff2cf" xsize 386
                    if noted:
                        text "관찰 메모를 남겼다" size 23 color "#efd4a1"
                        text ("새 질문 · "+R13_NAMES[spec["person"]]) size 22 color "#efd4a1"
                        text ROOM13["topics"][spec["topic"]]["title"] size 23 color "#fff2cf" xsize 386
                        text "관찰 메모에서 다시 읽고, 상대를 만나 물어보자." size 20 color "#ced9d4" xsize 386
                    else:
                        text "살핀 부분을 적어 두고, 아는 사람에게 물어보자." size 23 color "#ced9d4" xsize 386
            textbutton ("메모 남김" if noted else "관찰 메모 남기기"):
                style "r13_action_button" xsize 408 ysize 64 text_size 22
                sensitive not noted action Return("record")
    if r13_tool_can_ask_child(key):
        $ child_read="tool:seam" in room13.get("read_topics",[])
        textbutton ("읽음 · 다람이에게 물어보기" if child_read else "다람이에게 물어보기"):
            style "r13_action_button" xpos 40 ypos 630 xsize 720 ysize 62
            sensitive not child_read action Return("ask_child")
    textbutton "현장으로 돌아가기" style "r13_action_button" xpos 790 ypos 630 xsize 450 ysize 62 action Return()
    key "game_menu" action Return()

label r13_tool_inspect(key):
    if not r13_tool_available(key):
        return
    window hide
    hide r13_visitor
    while r13_tool_available(key):
        call screen r13_tool_closeup(key)
        if _return=="ask_child" and r13_tool_can_ask_child(key) and "tool:seam" not in room13.get("read_topics",[]):
            $ r13_note_encounter("daram")
            call r13_lines(r13_conversation_topic_lines("tool:seam"),"topic:tool:seam") from r13_tool_seam_question_return
            $ r13_finish_topic("tool:seam")
        elif _return=="record":
            $ r13_tool_recorded=r13_tool_record(key)
            if r13_tool_recorded:
                $ source_fx("found")
        else:
            return
    return

screen r13_tool_notebook():
    modal True
    zorder 96
    add Solid("#0b1b24fa")
    text "돋보기 관찰 메모" style "r13_title_text" color "#efd4a1" xpos 56 ypos 35
    viewport:
        area (56,104,1168,490) mousewheel True draggable True scrollbars "vertical"
        vbox:
            spacing 20
            for note in r13_tool_notes():
                frame:
                    xsize 1130 padding R13_UI_PADDING["panel"] background R13ActionPanel()
                    vbox:
                        spacing 14
                        text note["title"] size 28 color "#efd4a1"
                        text ("%d일 · %s · %s"%(note["day"],("오전","오후","저녁","늦은 저녁")[note["period"]],R13_PLACES[note["place"]][0])) size 21 color "#ced9d4"
                        text note["summary"] size 24 color "#fff2cf" xsize 1060
                        if note["topic"] in room13.get("read_topics",[]):
                            text ("질문 완료 · "+R13_NAMES[note["person"]]) size 22 color "#efd4a1"
                            text "들은 내용은 기록의 대화에서 다시 읽을 수 있다." size 22 color "#ced9d4" xsize 1060
                        else:
                            text note["followup"] size 22 color "#ced9d4" xsize 1060
            if not r13_tool_notes():
                text "현장에서 돋보기로 살피고 메모를 남기면 여기에 모입니다." size 24 color "#ced9d4"
    textbutton "닫기" style "r13_action_button" xpos 790 ypos 630 xsize 434 ysize 62 action Hide("r13_tool_notebook")
    key "game_menu" action Hide("r13_tool_notebook")

# The calendar dialogue module replaces r13_conversation_topic_lines at init 75,
# so Buri's plan follow-up must wrap it afterwards or it is silently dropped.
init 77 python:
    r13_tool_base_topic_lines=r13_conversation_topic_lines
    def r13_conversation_topic_lines(key):
        lines=r13_tool_base_topic_lines(key)
        if key!="tool:plans":return lines
        if "E04" in store.room13["evidence"]:
            return lines+[("buri","이건 빌려드린 옛 도면에, 할머니가 집을 보수하면서 선을 덧그린 거예요."),
                ("dad","외벽과 비교해 적은 길이 옆에, 어느 선을 봤는지도 표시해 둘게.")]
        if store.room13["period"]<3 and any(name=="map" for name,unused in r13_actions()):
            return lines+[("buri","밖에서 창과 창 사이 길이도 재 보세요. 그 길이를 이 도면이랑 대조해 보면 돼요."),
                ("dad","그럼 도면을 다시 펼쳐서 외벽과 비교해 볼게.")]
        return lines
