# 현장 조작과 인물의 발화를 분리하고, 주민 부탁은 기존 수첩으로 다시 확인한다.
init 379 python:
    R13_FIELD_PLAIN_OBSERVATIONS146={
        ("room13","books"):"크기가 다른 책들이 책장에 나란히 꽂혀 있다.",
        ("kitchen","shelf"):"찬장에 그릇들이 놓여 있다.",
        ("passage","handle"):"문 안쪽에 손잡이가 달려 있다.",
        ("ms14_somi_inside","v111_coat"):"회색 겉옷이 놓여 있다.",
        ("ms14_somi","v111_bedding"):"처마 아래에 침구와 물통이 놓여 있다.",
    }
    R13_SIDEQUEST_STATUS146={"accepted":"진행 중","worked":"보고할 차례","done":"마침",
        "deferred":"보류","declined":"거절","passed":"기회가 지남"}

    def r13_v111_dialogue_here146(person):
        if person in r13_visible_people():return True
        return bool(r13_v111_active() and person=="daram" and 1<=store.room13.get("day",1)<=7
                    and person in r13_v111_roam_companions())

    def r13_field_companion_button146():
        return bool(r13_v111_active() and r13_v111_dialogue_here146("daram") and "daram" not in r13_visible_people()
                    and r13_v111_resident_topics("daram"))

    def r13_sidequest_tasks146():
        return globals().get("r13_sidequest_tasks",lambda:[])()

    _r13_field146_observation_chat_allowed=r13_observation_chat_allowed
    def r13_observation_chat_allowed(identity):
        if r13_v111_active():
            # 현장 그림에서 숨긴 동행과, 다른 장소에서 보호 중인 아이를 구별한다.
            if "daram" not in r13_v111_roam_companions():return False
            s=store.room13
            if s.get("location")=="v111_fire" or r13_v111_tense_context():return False
            if s.get("day")==3 and r13_v111_value("piko_alive") is False and r13_v111_owned("E09"):return False
            if s.get("day")==6 and (r13_v111_value("D06_S03P_empty_fire_completed")
                    or r13_v111_value("D06_S03_main_completed")):return False
        return _r13_field146_observation_chat_allowed(identity)

    _r13_field146_conversation_pose=r13_conversation_pose
    def r13_conversation_pose(person,pose=None):
        if pose is None and r13_v111_active() and person in CAST:
            if r13_v111_resident_talk_context(person) in ("piko_after","fire","fire_safe","fire_lost"):
                pose="anxious"
        return _r13_field146_conversation_pose(person,pose)

screen r13_v111_object_choices146(key,options):
    modal True
    zorder 40
    default ready=False
    timer .2 action SetScreenVariable("ready",True)
    add Solid("#172a2a80")
    $ entries=[(o["title"],Return(o["position"]),False) for o in options]
    use r13_question_list(None,"neutral",r13_object_name(key),entries,ready,return_action=Return("back"))
    key "game_menu" action Return("back")

screen r13_sidequest_journal146():
    modal True
    zorder 45
    default ready=False
    timer .2 action SetScreenVariable("ready",True)
    add Solid("#172a2aa6")
    add r13_asset_path(R13_NB_PANEL) xpos R13_NB_PANEL_POS[0] ypos R13_NB_PANEL_POS[1]
    text "주민의 부탁" xpos R13_NB_TITLE_X ypos R13_NB_TITLE_Y size r13_nb_title_size() color r13_nb_ink() font R13_UI_BOLD_FONT
    default page=0
    $ tasks=r13_sidequest_tasks146()
    $ pages=max(1,(len(tasks)+1)//2)
    $ page=min(page,pages-1)
    text ("%d / %d쪽"%(page+1,pages)) xpos 1120 ypos R13_NB_TITLE_Y xanchor 1.0 size r13_type("small") color r13_type_color("muted")
    vbox:
        pos (156,142) xsize 996 spacing 18
        if not tasks:
            text "아직 들은 부탁이 없습니다." size r13_type("body") color r13_nb_ink()
        for task in tasks[page*2:page*2+2]:
            vbox:
                spacing 5
                text (task["title"]+" · "+R13_SIDEQUEST_STATUS146.get(task["status"],task["status"])) size r13_type("body") color r13_nb_ink() font R13_UI_BOLD_FONT
                text task["objective"] size r13_type("small") color r13_type_color("muted") xmaximum 980
                if task.get("place"):
                    text ("장소: "+R13_PLACES.get(task["place"],(task["place"],))[0]) size r13_type("small") color r13_type_color("muted")
    use r13_nb_footer_button(0,"현장으로",Return(False),primary=True,control_id="r13_quest_journal_close")
    if pages>1:
        use r13_nb_footer_button(2,"이전",SetScreenVariable("page",page-1),enabled=ready and page>0,control_id="r13_quest_journal_prev")
        use r13_nb_footer_button(1,"다음",SetScreenVariable("page",page+1),enabled=ready and page<pages-1,control_id="r13_quest_journal_next")
    key "game_menu" action Return(False)
