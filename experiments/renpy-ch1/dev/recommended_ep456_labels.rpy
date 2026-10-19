# Shared scene renderer is reused; these screens only add earned object interaction.
screen r13_rec_e456_pick(prompt, choices):
    modal True
    add Solid("#142327ef")
    frame:
        xalign .5 yalign .5 xsize 1100 ysize 590
        vbox:
            spacing 22
            text prompt size 27
            for answer_id, caption, feedback in choices:
                textbutton caption action Return(answer_id) xsize 1010 text_size 24
            textbutton "일단 물러나 현장을 다시 본다" action Return(None) text_size 22

screen r13_rec_e4_layout(prompt, mode="space"):
    modal True
    add Solid("#152328")
    text "13호 · 서로 다른 두 문" xpos 65 ypos 35 size 32
    text prompt xpos 65 ypos 82 size 25 xmaximum 1130
    frame:
        xpos 65 ypos 150 xsize 340 ysize 440 background Solid("#294851")
        vbox:
            text "공개 복도 H" size 28
            text "A: 객실로 들어가는 문\nB: 관리 칸의 유일 출입" size 21
    frame:
        xpos 430 ypos 150 xsize 390 ysize 205 background Solid("#755f42")
        vbox:
            text "객실 R" size 29
            text "A는 열림. 다람과 보호자가 서는 쪽." size 20
            textbutton "R · 객실 쪽" action Return("R") text_size 24
    frame:
        xpos 855 ypos 150 xsize 340 ysize 205 background Solid("#36424c")
        vbox:
            text "작업칸 P" size 29
            text "다른 통행문 없음. 사람이 있는 쪽." size 20
            textbutton "P · 작업칸 쪽" action Return("P") text_size 24
    textbutton "G\n판자문" xpos 791 ypos 211 action Return("G") text_size 22
    frame:
        xpos 430 ypos 390 xsize 765 ysize 200 background Solid("#335c52")
        vbox:
            text "관리 칸 K · L은 위의 G에 기계로 연결" size 26
            text "통행은 B 하나. 확인한 연결부에 끈·예약 장치 없음." size 20
            hbox:
                spacing 25
                textbutton "L 올리기" action Return("up") text_size 25
                textbutton "L 끝까지 내리기" action Return("down") text_size 25
                textbutton "G를 안에서 당기기" action Return("inside") text_size 23
    textbutton "조사로 돌아간다" xpos 65 ypos 635 action Return(None) text_size 23

label r13_rec_e4_inspect_layout:
    call screen r13_rec_e4_layout("다람이 사람을 발견하고 도움을 청한 쪽을 직접 짚어 보자.")
    if _return is None:
        return False
    if _return != "R":
        call r13_lines([("dad","다람이는 잠긴 작업칸 안에 있지 않았어. 열린 객실 입구와 안쪽 판자문을 나눠 보자.")], "recommended:e4:layout:wrong-position")
        jump r13_rec_e4_inspect_layout
    call r13_lines([("daram","나는 여기였어. 저 판자문 밑으로 사람이 움직였어."),("buri","그럼 지금은 아무도 안에 없으니, 제가 관리 칸에서 열어 볼게요.")], "recommended:e4:layout:position")
label r13_rec_e4_inspect_open:
    call screen r13_rec_e4_layout("부리가 밖의 관리 칸에 섰다. 판자문을 여는 동작을 시험하자.")
    if _return is None:
        return False
    if _return != "up":
        call r13_lines([("buri","그 동작으로는 열리지 않아요. 레버의 반대 방향도 안전하게 확인합시다.")], "recommended:e4:layout:wrong-open")
        jump r13_rec_e4_inspect_open
    call r13_lines([(None,"부리가 L을 올리자 연결부가 움직이며 G가 올라갔다. 밖에서 작업칸으로 통하는 길이 열렸다."),("dad","이제 잠기는 조건도 확인하죠.")], "recommended:e4:layout:open")
label r13_rec_e4_inspect_lock:
    call screen r13_rec_e4_layout("문짝이 살짝 움직이는 것과 걸쇠가 잠기는 것을 구별할 동작은?")
    if _return is None:
        return False
    if _return != "down":
        call r13_lines([("buri","문짝을 당기거나 레버를 조금 건드리는 것만으로는 걸쇠가 걸리지 않아요.")], "recommended:e4:layout:wrong-lock")
        jump r13_rec_e4_inspect_lock
    call r13_lines([(None,"L을 끝까지 내리자 G가 내려가 걸쇠에 걸렸다. 부리는 다시 올려 아무도 갇히지 않은 칸을 열어 두었다."),("buri","놓아 두어도 저절로 잠기지 않습니다. 여기 연결부도 함께 보세요. 다른 출입구나 붙인 끈, 예약 장치는 없어요."),("dad","여기서 열고 잠글 수 있다는 사실과, 누가 실제로 썼는지는 따로 물어야겠습니다.")], "recommended:e4:layout:lock")
    return True

screen r13_rec_e5_pots_screen(prompt, swapped=False):
    modal True
    add Solid("#192629")
    text "학교 배식대 · 몸체는 그대로, 뚜껑은 따로" xpos 65 ypos 35 size 31
    text prompt xpos 65 ypos 89 size 25 xmaximum 1140
    frame:
        xpos 80 ypos 170 xsize 510 ysize 360 background Solid("#594d3a")
        vbox:
            spacing 30
            text "왼쪽 A · 원래 순찰대 몫" size 27
            textbutton ("아이 그림 뚜껑" if swapped else "그림 없는 뚜껑") action Return("left_lid") text_size 28
            textbutton "몸체: 깨진 귀" action Return("left_body") text_size 30
            text "음식은 이 몸체 안에 그대로" size 21
    frame:
        xpos 665 ypos 170 xsize 510 ysize 360 background Solid("#365448")
        vbox:
            spacing 30
            text "오른쪽 C · 원래 아이들 몫" size 27
            textbutton ("그림 없는 뚜껑" if swapped else "아이 그림 뚜껑") action Return("right_lid") text_size 28
            textbutton "몸체: 천 감은 손잡이" action Return("right_body") text_size 29
            text "음식은 이 몸체 안에 그대로" size 21
    text "같은 크기의 뚜껑. F 앞문 안쪽에서는 두 냄비가 모두 보인다." xpos 80 ypos 560 size 24
    textbutton "조사로 돌아간다" xpos 80 ypos 625 action Return(None) text_size 23

label r13_rec_e5_inspect_pots:
    call screen r13_rec_e5_pots_screen("뚜껑이 없어져도 같은 냄비인지 알아볼 수 있는 왼쪽의 부분은?")
    if _return is None:
        return False
    if _return != "left_body":
        call r13_lines([("resident_bori","뚜껑은 빼서 식히기도 해요. 냄비 자체는 어느 부분으로 구별할까요?")], "recommended:e5:pots:wrong")
        jump r13_rec_e5_inspect_pots
    call r13_lines([("daram","한쪽 귀가 깨졌어. 뚜껑을 내려도 이건 남아."),("resident_bori","맞아. 오른쪽은 손잡이에 천이 있고. 배식할 땐 아이 그림 뚜껑을 보는 게 우리 습관이야."),("dad","고정된 특징과 옮길 수 있는 표식이 다르구나.")], "recommended:e5:pots:seen")
    return True

label r13_rec_e4_work_scene:
    if r13_recommended["e4_lever_blocked"]:
        call r13_lines([("nabi","관리 칸 출입은 받지 않습니다. 필요한 물품은 부리가 가져다줄 거예요."),(None,"너울은 문 바깥에서 물품을 받았다. 따닥은 열린 작업칸에서 실측을 마치고 무사히 나왔다."),("resident_ttadak","문이 움직이지 않아 일도 빨리 끝났어요.")], "recommended:e4:work:prevented")
    elif "e4_wedge_set" in r13_recommended["done"]:
        call r13_lines([(None,"관리 칸에서 업무 물품을 챙긴 너울이 나온 뒤, G가 버팀목에 닿았다. 부리가 레버를 풀고 따닥을 불렀다."),("resident_ttadak","안전해요. 버팀목이 문을 막았어요."),("dad","다치지 않은 건 다행입니다. 그때의 출입을 실제로 본 사람에게 묻겠습니다.")], "recommended:e4:work:wedge")
    else:
        call r13_lines([(None,"실측 중 G가 내려가 걸렸다. 부리가 밖의 레버를 올려 따닥을 데리고 나왔다. 따닥은 다쳐 진료를 받게 됐다."),("dad","구조부터 합시다. 누가 몇 번 움직였는지 못 본 사실을 덧붙이지 않겠습니다.")], "recommended:e4:work:injured")
    return True

label r13_rec_e6_hold_scene:
    if r13_recommended["episodes"]["6"]["transport"] == "at_altar_waiting":
        call r13_scene("r13_altar", "도착한 수레 · 먼저 사람을 보호한다", "calm")
    call r13_lines(r13_rec_e6_hold_lines(r13_recommended), "recommended:e6:hold:current")
    return True

label r13_rec_e6_night_scene:
    call r13_lines([(None,"세 사람은 준비한 식사를 먹었다. 먼저 맡은 서리가 상태를 살핀 뒤, 나비가 학교의 첫 교대를 시작했다."),("daram","오늘은 아무도 돌 앞에 두고 오지 않은 거지?"),("dad","응. 여기에 자리가 있고, 먹을 것과 돌볼 사람도 있어.")], "recommended:e6:night:community")
    if r13_recommended["mother"] == "M2":
        menu:
            "오늘의 보호는 이어진다. 가족의 다음 계획은?"
            "오늘은 학교에 함께 남는다":
                $ r13_recommended = r13_rec_e6_choose_future(r13_recommended, "stay")
            "떠날 길이 확인될 때까지 함께 쉰다":
                $ r13_recommended = r13_rec_e6_choose_future(r13_recommended, "departure_pending")
        call r13_lines([("mom","내일 이후 일은 또 정해야 해. 오늘은 같이 있을 수 있어."),("daram","그럼 오늘은 여기서 같이 자자."),(None,"가족은 확인한 공동 공간에서 이불을 폈다. 다음 교대가 도착하는 것을 보고 불을 낮췄다.")], "recommended:e6:night:family")
    else:
        call r13_lines([("dad","학교의 오늘 밤은 지켰지만 엄마와 다시 만나는 일은 아직 남았어. 확인된 연락 길을 계속 따라가자.")], "recommended:e6:night:family-unfinished")
    return True

label r13_recommended_ep4_hearing:
    call r13_scene("council", "10일 · 7일과 9일을 나누는 심리", "calm")
    $ r13_rec_stage_enter(4)
    jump r13_rec_e456_hearing_loop
label r13_recommended_ep5_hearing:
    call r13_scene("r13_school", "13일 · 배식과 책임을 구별하는 회의", "calm")
    $ r13_rec_stage_enter(5)
    jump r13_rec_e456_hearing_loop
label r13_recommended_ep6_hearing:
    call r13_scene("r13_school", "14일 · 남을 수 있는 오늘", "calm")
    $ r13_rec_stage_enter(6)
    jump r13_rec_e456_hearing_loop

label r13_rec_e456_hearing_loop:
    $ r13_rec_late_reason = r13_rec_e456_ready(r13_recommended)
    if r13_rec_late_reason:
        call r13_lines([("dad",r13_rec_late_reason)], "recommended:late:hearing:missing")
        jump r13_recommended_hub
    $ r13_rec_late_steps = r13_rec_e456_hearing(r13_recommended)
    $ r13_rec_late_index = r13_recommended["episodes"][str(r13_recommended["episode"])]["hearing"]
    if r13_rec_late_index >= len(r13_rec_late_steps):
        jump r13_rec_e456_result
    $ r13_rec_late_step = r13_rec_late_steps[r13_rec_late_index]
    call r13_lines(r13_rec_e456_challenge(r13_recommended), "recommended:late:hearing:challenge")
    $ r13_rec_stage_prompt(r13_rec_late_step["id"])
    call screen r13_recommended_cards(r13_rec_late_step["question"])
    if _return is None:
        jump r13_recommended_hub
    $ r13_rec_late_card = _return
    if r13_rec_late_card != r13_rec_late_step["card"]:
        $ r13_rec_stage_answer(r13_rec_late_step["id"],False)
        call r13_lines([("dad","그 자료만으로는 지금 방어를 깨뜨릴 수 없습니다. 상대가 주장한 날짜와 행위를 다시 봅시다.")], "recommended:late:hearing:wrong-card")
        jump r13_rec_e456_hearing_loop
    if r13_recommended["episode"] == 5 and not r13_recommended["e5_poison_blocked"] and r13_rec_late_index == 0:
        call screen r13_rec_e5_pots_screen("아이들이 배식받은 쪽이다. 원래 몫을 알려 주는 고정 부위를 짚어 보자.", True)
        if _return is None:
            jump r13_recommended_hub
        if _return != "left_body":
            $ r13_rec_stage_answer(r13_rec_late_step["id"],False)
            call r13_lines([("dad","뚜껑의 그림은 옮길 수 있습니다. 같은 냄비를 끝까지 따라갈 기준은 몸체에 있습니다.")], "recommended:e5:hearing:body")
            jump r13_rec_e456_hearing_loop
    call screen r13_rec_e456_pick("그 자료의 어느 부분을 근거로 삼을까?", r13_rec_late_step["details"])
    if _return is None:
        jump r13_recommended_hub
    $ r13_rec_late_detail = _return
    call screen r13_rec_e456_pick("그 부분으로 말할 수 있는 결론은 어디까지일까?", r13_rec_late_step["claims"])
    if _return is None:
        jump r13_recommended_hub
    $ r13_rec_late_claim = _return
    $ r13_recommended, r13_rec_late_feedback, r13_rec_late_correct = r13_rec_e456_present(r13_recommended, r13_rec_late_card, r13_rec_late_detail, r13_rec_late_claim)
    $ r13_rec_stage_answer(r13_rec_late_step["id"],r13_rec_late_correct)
    call r13_lines([("dad",r13_rec_late_feedback)], "recommended:late:hearing:answer")
    if r13_recommended["episodes"][str(r13_recommended["episode"])]["hearing"] >= len(r13_rec_late_steps):
        jump r13_rec_e456_result
    jump r13_rec_e456_hearing_loop

label r13_rec_e456_result:
    if r13_recommended["episode"] == 4:
        if r13_recommended["episodes"]["4"]["victim"] == "recovering":
            call r13_lines([("resident_seori","피해자는 회복 중입니다. 구조가 빨라졌다고 감금과 구조 방해가 없었던 일은 아닙니다.")], "recommended:e4:result:alive")
        else:
            call r13_lines([("dad","처음부터 흉기 때문에 끝난 죽음이 아니었습니다. 살아 있는 사람을 가두고, 열 수 있는 문을 못 연다고 속여 구조를 막은 책임입니다.")], "recommended:e4:result:dead")
        if r13_recommended["e4_lever_blocked"]:
            call r13_lines([("dad","9일은 우리가 막았습니다. 그날 일어나지 않은 잠금 범죄를 더하지 않겠습니다.")], "recommended:e4:result:prevention")
        elif "e4_card_nabi9" not in r13_recommended["facts"]:
            call r13_lines([("dad","9일 그때 누가 드나들었는지는 아직 못 알아냈어요. 그날 일을 너울 씨에게 더하진 않겠습니다. 오늘 확인한 7일 일부터 책임져 주세요.")], "recommended:e4:result:limited9")
        call r13_lines([("resident_ppul","앞서 정한 절차대로, 감금과 구조 방해 책임을 확인한 너울을 추가 위험 방지를 위해 구금하겠소. 다람의 보호자 동반 대기는 끝냅니다."),(None,"너울은 현장 업무에서 분리됐다. 다람은 아빠의 손을 잡고 회의장을 나왔다.")], "recommended:e4:result:detained")
    elif r13_recommended["episode"] == 5:
        if r13_recommended["e5_poison_blocked"]:
            call r13_lines([("resident_teacher","학교를 지킬 다른 길을 먼저 확인했어야 했어요."),("resident_bori","아이들 저녁은 무사히 끝났어요. 다음 배식도 몸체와 표식을 함께 보겠습니다.")], "recommended:e5:result:prevented")
        else:
            call r13_lines([("resident_teacher","내가 넣은 건 맞아요. 하지만 아이들에게 먹이려던 건 아니었어요."),("dad","아이들을 노렸다고 몰아가지는 않겠어요. 그래도 약을 넣고 뚜껑을 바꾼 일까지 보리에게 떠넘기진 마세요."),("resident_ppul","선생님의 배식 업무를 분리하고 돌봄은 다른 담당자에게 맡기겠소. 아이들의 치료를 계속하십시오.")], "recommended:e5:result:responsibility")
        call r13_lines([("resident_badook","이제 오늘 저녁 출발 명단과 학교 배분을 맞춰야 합니다. 아직 학교에 남은 사람부터 함께 확인해 주세요.")], "recommended:e5:next:invitation")
    else:
        call r13_lines([("dad","배제 책임을 밝힌 것으로 사람의 밤이 저절로 바뀌지는 않습니다. 이제 강행 준비를 풀고, 실제 식사와 잠자리로 인계합시다."),("resident_ppul","내가 현재 운행 철회를 확인하겠소.")], "recommended:e6:result:execution")
    jump r13_recommended_hub

label r13_recommended_ep4_admin:
    call r13_rec_e456_admin_boot
    $ r13_recommended = r13_rec_e456_admin_seed(4)
    $ room13["day"] = 7
    jump r13_recommended_hub
label r13_recommended_ep5_admin:
    call r13_rec_e456_admin_boot
    $ r13_recommended = r13_rec_e456_admin_seed(5)
    $ room13["day"] = 11
    jump r13_recommended_hub
label r13_recommended_ep6_admin:
    call r13_rec_e456_admin_boot
    $ r13_recommended = r13_rec_e456_admin_seed(6)
    $ room13["day"] = 13
    jump r13_recommended_hub
label r13_rec_e456_admin_boot:
    $ room13_mode = True
    $ winter_mode = True
    $ winter = winter_new()
    $ source_mode = False
    $ room13 = r13_new()
    $ room13['campaign_id'] = 'room13_recommended_v1'
    $ r13_scene_key = None
    $ r13_world_cameras = {}
    $ r13_inspection_location = None
    $ room13['learning_archive'] = r13_learning_archive_seed()
    $ typing_allowed = True
    hide screen r13_hud
    hide screen winter_hud
    hide screen hud
    return
