# 1부는 7일 화재와 학교 인수 뒤, 13호의 다음 사건이 시작되기 전에 닫는다.
# 이 값을 끈 후속판은 같은 완료 저장에서 원래 free_evening7 흐름으로 돌아간다.
define R13_PART1_PUBLIC = True

default r13_part1_save_failed = False

init 370 python:
    def r13_part1_active():
        return bool(R13_PART1_PUBLIC and r13_v111_active())

    def r13_part1_ready():
        values=(store.room13.get("v111") or {}).get("values",{})
        return (store.room13.get("day")==7 and values.get("meeting:fire") in ("win","partial","lose")
                and values.get("D07_S02_handover_completed") is True and values.get("D07_S02_message_completed") is True)

    def r13_part1_warning_known():
        return (r13_v111_owned("E27") and r13_v111_value("mother_first_contact_read5") is True
                and r13_v111_value("mother_denies_invitation") is True)

    def r13_part1_daram_here():
        # 이전 판의 위치 표식이 낡았어도, 학교에서 실제 마주한 아이와 대화한다.
        if (store.room13.get("location")!="school" or r13_v111_value("DARAM_DETAINED")
                or r13_v111_value("departed:daram") or not r13_v111_person_alive("daram")):return False
        return r13_v111_actor_ready("daram") or "daram" in r13_visible_people()

    def r13_part1_can_explore():
        return (r13_part1_active() and r13_part1_ready() and store.room13.get("period")==1
                and r13_v111_value("route7") in (None,"uncommitted"))

    def r13_part1_resume_exploration():
        if not r13_part1_can_explore():return
        # 사건 결과와 오후 행동은 그대로 두고 다음 마무리에서 완료 저장을 갱신한다.
        r13_v111_set("part1_completed",False)
        r13_v111_set("part1_checkpoint_written",False)
        store.r13_part1_save_failed=False
        store.r13_v111_talk_person=None
        renpy.retain_after_load()

    def r13_part1_records(values):
        """현재 판에서 입증/기록한 범위만 보여 준다. 미래의 생사와 인계 완료를 만들지 않는다."""
        outcome=values.get("meeting:fire")
        rows=[]
        if outcome=="win" and values.get("neoul_promise_proven"):
            rows.append("누비의 방화 자백과, 너울의 약속을 뒷받침하는 배급표를 남겼다.")
        elif outcome=="win":
            action="빈 창고의 불을 끈 것" if values.get("FIRE_EVACUATED") else "아이들을 구하고 불을 끈 것"
            rows.append("누비가 불을 놓은 일과 보리가 %s을 구분해 기록했다."%action)
        elif outcome=="partial":
            rows.append("누비의 방화 자백은 남겼지만, 보리는 감춘 죄로 명단에 올랐다.")
        elif outcome=="lose":
            rows.append("누비의 자백을 얻지 못했다. 보리는 방화자로 기록돼 명단에 올랐다.")
        if values.get("D07_S02_handover_completed"):
            rows.append("학교가 맡은 아이들의 자리와 돌봄 담당자를 확인했다.")
        if values.get("E07_OWL_CONTACT"):
            rows.append("초롱이 건넨 쪽지에는 13과 부엉이의 이름이 있다. 엄마의 현재 위치는 아직 모른다.")
        if values.get("stove13_7")=="ration":
            rows.append("13호 난로에서 검푸른 돌을 꺼내고 배급 돌로 바꿨다.")
        elif values.get("stove13_7")=="empty":
            rows.append("13호 난로에서 검푸른 돌을 꺼냈다.")
        if values.get("doto_promise7"):
            rows.append("도토에게 다람을 맡게 되면 부름을 받아도 자리를 지켜 달라고 부탁했다.")
        return rows

    def r13_part1_save():
        if not r13_part1_active() or not r13_part1_ready() or not r13_v111_value("part1_completed"):
            return
        if r13_v111_value("part1_checkpoint_written"):return
        r13_v111_set("part1_checkpoint_written",True)
        store.r13_part1_save_failed=False
        # 화면 Action 안의 변경도 완료 저장을 복원할 때 유지한다.
        renpy.retain_after_load()
        try:
            renpy.take_screenshot()
            renpy.save("part1-clear",extra_info="1부 완료 · 화재 사건")
        except Exception as error:
            r13_v111_set("part1_checkpoint_written",False)
            store.r13_part1_save_failed=True
            renpy.log("1부 완료 저장 실패: %s"%type(error).__name__)
        renpy.restart_interaction()

    _r13_part1_binding=r13_v111_binding
    def r13_v111_binding():
        result=_r13_part1_binding()
        if r13_part1_active() and (store.room13.get("v111") or {}).get("gate")=="free_day7":
            result=dict(result)
            result["options"]=[dict(o,title="다람아, 오늘 조사는 여기서 마치자.") if o.get("index")==0 else o for o in result.get("options",[])]
        return result

label r13_part1_finish:
    if not r13_part1_active() or not r13_part1_ready():
        return
    if not r13_v111_value("part1_completed"):
        # free_day7의 첫 선택은 학교의 다람에게 하는 말이다. 구 저장의 다른 위치 진입만 실제 이동으로 맞춘다.
        if room13.get("location")!="school":
            call r13_v111_travel('school','part1_finish',[])
        if r13_v111_value("meeting:fire")=="lose":
            call r13_lines(r13_nw_block('part1_fire_lost'),'nw:part1_fire_lost')
        elif r13_v111_value("meeting:fire")=="partial":
            call r13_lines(r13_nw_block('part1_fire_partial'),'nw:part1_fire_partial')
        elif r13_v111_value("neoul_promise_proven"):
            call r13_lines(r13_nw_block('part1_fire_grand'),'nw:part1_fire_grand')
        else:
            call r13_lines(r13_nw_block('part1_fire_won'),'nw:part1_fire_won')
        if r13_part1_daram_here():
            if r13_v111_value("KKOMI_ALIVE") is False:
                call r13_lines(r13_nw_block('part1_child_lost'),'nw:part1_child_lost')
            elif r13_v111_value("KKOMI_ALIVE") is True:
                call r13_lines(r13_nw_block('part1_child_saved'),'nw:part1_child_saved')
            if r13_v111_value("meeting:fire")=="partial":
                call r13_lines(r13_nw_block('part1_family_partial'),'nw:part1_family_partial')
            elif r13_v111_value("meeting:fire")=="lose":
                call r13_lines(r13_nw_block('part1_family_lost'),'nw:part1_family_lost')
            if r13_part1_warning_known():
                call r13_lines(r13_nw_block('part1_family_plan'),'nw:part1_family_plan')
            else:
                call r13_lines(r13_nw_block('part1_family_contact'),'nw:part1_family_contact')
            call r13_lines(r13_nw_block('part1_family_close'),'nw:part1_family_close')
        $ r13_v111_set("part1_completed",True)
    call screen r13_part1_end
    if _return=="explore":
        $ r13_part1_resume_exploration()
        return "explore"
    return

screen r13_part1_finish_choice():
    modal True
    zorder 150
    default ready=False
    timer .2 action SetScreenVariable("ready",True)
    use r13_notebook_shell("오늘의 조사",stamp="일곱째 날")
    text "오늘의 조사를 마칠까요?" xpos R13_NB_LEFT ypos 220 size r13_type("display") color r13_nb_ink() font R13_UI_BOLD_FONT
    text "마치면 제1부의 마지막 대화로 이어집니다.\n아직 둘러볼 곳이 있으면 조사를 계속할 수 있습니다." xpos R13_NB_LEFT ypos 324 xsize R13_NB_WIDTH size r13_type("emphasis") color r13_nb_ink() font R13_UI_FONT
    hbox:
        xpos R13_NB_LEFT ypos r13_nb_footer_y() spacing 18
        use r13_control("탐색 계속",None,Return(False),enabled=ready,width=528,control_id="r13_part1_keep_exploring")
        use r13_control("1부 마무리",None,Return(True),enabled=ready,primary=True,width=528,control_id="r13_part1_finish_now")
    key "game_menu" action Return(False)

screen r13_part1_end():
    modal True
    zorder 150
    default expanded=False
    default ready=False
    timer .2 action SetScreenVariable("ready",True)
    # 실제 종료 화면이 열린 뒤 저장한다. 1~7일 자료·선택과 다음 라벨의 호출 스택이 함께 남는다.
    timer .35 action Function(r13_part1_save)
    if not r13_part1_active():
        timer .05 action Return("continue")
    use r13_notebook_shell("제1부 · 화재 사건",stamp="일곱째 날")
    text "불이 꺼진 뒤" xpos R13_NB_LEFT ypos 184 size r13_type("display") color r13_nb_ink() font R13_UI_BOLD_FONT
    if expanded:
        viewport:
            area (R13_NB_LEFT,248,R13_NB_WIDTH,244) mousewheel True draggable True scrollbars "vertical"
            vbox:
                xsize (R13_NB_WIDTH-24) spacing 20
                for line in r13_part1_records((room13.get("v111") or {}).get("values",{})):
                    text line size r13_type("emphasis") color r13_nb_ink() font R13_UI_FONT xsize (R13_NB_WIDTH-24)
    else:
        vbox:
            xpos R13_NB_LEFT ypos 264 xsize (R13_NB_WIDTH-32) spacing 24
            text "창고의 불은 꺼졌다.\n기록에 남은 이름들은 수첩 안에 있다." size r13_type("emphasis") color r13_nb_ink() font R13_UI_FONT xsize (R13_NB_WIDTH-32)
            text "엄마를 찾아온 길은 아직 계속된다." size r13_type("emphasis") color r13_nb_ink() font R13_UI_FONT xsize (R13_NB_WIDTH-32)
            text "제1부를 마쳤습니다." size r13_type("body") color r13_nb_accent() font R13_UI_BOLD_FONT
    text ("자동 저장을 마치지 못했습니다. 진행 저장으로 남겨 주세요." if r13_part1_save_failed else "이어가기용 완료 저장을 남겼습니다." if r13_v111_value("part1_checkpoint_written") else "완료 저장을 남기는 중입니다.") xpos R13_NB_LEFT ypos 506 size r13_type("small") color r13_nb_muted() font R13_UI_FONT xsize R13_NB_WIDTH
    hbox:
        xpos R13_NB_LEFT ypos r13_nb_footer_y() spacing 18
        use r13_control("탐색 계속",None,Return("explore"),enabled=ready and r13_part1_can_explore(),width=255,control_id="r13_part1_explore")
        use r13_control("기록 접기" if expanded else "기록 펼치기",None,ToggleScreenVariable("expanded"),enabled=ready,width=255,control_id="r13_part1_records")
        use r13_control("진행 저장",None,ShowMenu("save"),enabled=ready,width=255,control_id="r13_part1_save")
        use r13_control("메인화면",None,MainMenu(confirm=False),enabled=ready,primary=True,width=255,control_id="r13_part1_main")
    key "game_menu" action ShowMenu("pause_menu")
