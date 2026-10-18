# Owner-only quick test. Native Replay isolates the current game and disables saves.
# Based on dev/qa_meeting_review_cards.py's day-7 fixture, not a campaign shortcut.
default r13_admin_meeting_test = False
default r13_admin_meeting_claim = "C2"

init 180 python:
    R13_ADMIN_MEETINGS=("C2","C1","C3","C4")

    def r13_admin_meeting_fixture(claim):
        if claim not in R13_ADMIN_MEETINGS:
            raise ValueError("Unknown admin meeting: "+str(claim))
        n=r13_new()
        n.update(day=R13_TRIAL_DAY,period=2,location="dining",case_state="occurred",
            victim_state="dead",daram_state="held",life_poc=True,
            evidence=list(ROOM13["evidence"]),
            propositions=list(("C1","C2","C3","C4")[:int(claim[1])-1]),arguments={})
        n["flags"]=list(dict.fromkeys(n.get("flags",[])+["entry_corrected","lodging","bami_consent"]))
        # Evidence is supplied for testing, never granted to normal or persistent history.
        n["records"]={key:dict(day=R13_TRIAL_DAY,period=2,source="관리자 회의 테스트 자료",place="dining") for key in n["evidence"]}
        return n

screen r13_admin_meeting_picker():
    modal True
    zorder 130
    add Solid("#071015ee")
    frame:
        xalign .5 yalign .5 xsize 900 padding (28,24) background R13ActionPanel()
        vbox:
            spacing 14
            text "회의 바로 테스트" size 30 color "#f6d18a"
            text "실제 회의 로직 · 앞 논점 완료 · 테스트 자료/밤이 동의 포함" size 21 color "#fff4df"
            text "현재 진행과 저장은 유지됩니다. 나가서 같은 회의를 고르면 처음부터 다시 시작합니다." size 21 color "#ced9d4" xsize 840
            if persistent.room13_admin:
                for claim in R13_ADMIN_MEETINGS:
                    textbutton (claim+" · "+R13_DEBATE[claim]["title"]):
                        style "r13_action_button" text_size 22 padding (16,10)
                        action Replay("r13_admin_meeting_replay",scope={"r13_admin_meeting_claim":claim},locked=False)
            textbutton "닫기" style "r13_action_button" text_size 22 action Hide("r13_admin_meeting_picker")
    key "game_menu" action Hide("r13_admin_meeting_picker")

label r13_admin_meeting_replay:
    if not _in_replay or not persistent.room13_admin or r13_admin_meeting_claim not in R13_ADMIN_MEETINGS:
        $ renpy.end_replay()
        return
    $ r13_admin_meeting_test=True
    $ _autosave=False
    $ _game_menu_screen=None
    $ room13_mode=True
    $ room13=r13_admin_meeting_fixture(r13_admin_meeting_claim)
    $ r13_upgrade()
    show screen r13_admin_meeting_controls
    call r13_scene("council","관리자 · 회의 테스트","hearing")
    # No verdict, cinematic or campaign continuation: only the selected canonical debate.
    call r13_debate_run(r13_admin_meeting_claim)
    call screen r13_admin_meeting_finished
    $ renpy.end_replay()
    return

screen r13_admin_meeting_controls():
    zorder 200
    textbutton "테스트 종료 · 다시 선택":
        style "r13_action_button" xpos 900 ypos 8 xsize 360 ysize 42 text_size 19
        action EndReplay(confirm=False)
    key "game_menu" action EndReplay(confirm=False)
    key "quick_save" action NullAction()
    key "quick_load" action NullAction()

screen r13_admin_meeting_finished():
    modal True
    zorder 210
    add Solid("#071015cc")
    frame:
        xalign .5 yalign .5 xsize 720 padding (28,24) background R13ActionPanel()
        vbox:
            spacing 18
            text "회의 테스트가 끝났습니다" size 28 color "#f6d18a"
            text "결과는 본편 진행에 반영되지 않습니다." size 22 color "#fff4df"
            textbutton "회의 다시 선택 / 나가기" style "r13_action_button" text_size 23 action EndReplay(confirm=False)
    key "game_menu" action EndReplay(confirm=False)
