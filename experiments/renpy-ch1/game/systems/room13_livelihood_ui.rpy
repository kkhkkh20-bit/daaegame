screen r13_work_board(start_tab="work"):
    modal True
    zorder 90
    default tab=start_tab
    $ wallet=r13_wallet(room13)
    add Solid("#102725f5")
    text "마을 생활" xpos 48 ypos 30 size 32 color "#efd4a1"
    text ("가진 돈 %d냥 · 갚을 돈 %d냥 · 하루 방값·밥값 10냥"%(wallet["cash"],wallet["debt"])) xpos 310 ypos 41 size 23 color "#fff2cf"
    hbox:
        xpos 48 ypos 95 spacing 16
        for key,title in (("work","일거리"),("shop","상점"),("relations","함께한 일"),("ledger","생활 장부")):
            textbutton title style "r13_action_button" xsize 225 ysize 55 selected tab==key action SetScreenVariable("tab",key)
    if tab=="work":
        text ("오전·오후 한 번씩 · "+r13_learning_settlement_text(compact=True)) xpos 48 ypos 174 size 22 color "#d4dfd8"
        vbox:
            xpos 48 ypos 226 spacing 14
            for key,job in R13_JOBS.items():
                button:
                    style "r13_action_button" xsize 1180 ysize 112 padding (22,10)
                    sensitive r13_work_available(key)
                    action Return((key,"finish"))
                    vbox:
                        spacing 7
                        text (job["title"]+" · "+R13_NAMES.get(job["npc"],job["npc"])+" · %d냥"%job["pay"]) size 25 color "#fff2cf"
                        text (r13_learning_job_context(key)+" · "+r13_work_status(key)) size r13_read_size(20,23) color "#d4dfd8"
                        text (r13_learning_time_text(1)+" · "+r13_learning_settlement_text(additional=job["pay"],compact=True)) size r13_read_size(18,21) color "#eee5d5"
        text ("오늘 일할 시간은 끝났다. 저녁에는 사람들을 만나거나 기록을 살펴보자." if room13["period"]>=2 else "조사·대화는 시간 소모 없음 · 돈이 모자라면 외상으로 남겨도 잘 수 있다.") xpos 48 ypos 598 size 21 color "#efd4a1"
    elif tab=="shop":
        text "물건은 공동 물품 창고의 은호 사장에게서 산다. 여기서도 같은 물건을 볼 수 있다." xpos 48 ypos 174 size 22 color "#d4dfd8"
        textbutton "은호 사장의 물건 보기" style "r13_action_button" xpos 48 ypos 226 xsize 420 ysize 66 action Show("r13_shop",close=Hide("r13_shop"))
    elif tab=="relations":
        text "함께 겪은 일에서 새로운 질문이 생긴다." xpos 48 ypos 174 size 22 color "#d4dfd8"
        viewport:
            area (48,226,1180,370) mousewheel True draggable True scrollbars "vertical"
            vbox:
                spacing 24
                for key in wallet["relations"]:
                    text R13_WORK_RELATIONS.get(key,key) size 25 color "#fff2cf" xsize 1120
                if not wallet["relations"]:
                    text "아직 함께 일하며 알아낸 이야기가 없다." size 24 color "#d4dfd8"
    else:
        text "첫날은 공짜. 잠들 때 가진 돈으로 방값과 밥값을 내고, 모자란 만큼만 나중에 갚을 돈으로 남긴다." xpos 48 ypos 174 size 22 color "#d4dfd8"
        viewport:
            area (48,226,1170,340) mousewheel True draggable True scrollbars "vertical"
            vbox:
                spacing 16
                for row in reversed(wallet["ledger"]):
                    text ("%d일째 · %s · %+d냥"%(row["day"],row["text"],row["amount"])) size 23 color "#fff2cf"
                if not wallet["ledger"]:
                    text "아직 수입·지출이 없다." size 23 color "#d4dfd8"
        textbutton "가진 돈으로 외상 갚기":
            style "r13_action_button" area (48,578,390,58)
            sensitive wallet["cash"]>0 and wallet["debt"]>0 action Function(r13_life_repay)
    textbutton "돌아가기" style "r13_action_button" area (950,646,280,58) action Return(False)
    key "game_menu" action Return(False)
