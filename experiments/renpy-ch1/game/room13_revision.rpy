# Father-perspective revision. Puzzle state belongs to the current saved run.
label r13_revision_resume:
    $ renpy.config.skipping=None
    window show
    $ dialogue_speaker=None
    source_thought "이 저장은 사건의 내용이 다른 이전 초안에서 만들어졌습니다. 이미 본 범행과 모은 증거를 새 사건의 사실로 바꾸어 이어갈 수는 없습니다. 기존 저장 파일은 그대로 남습니다."
    menu:
        "개정된 사건을 1일차부터 시작한다":
            $ renpy.full_restart(label="room13_start")
        "메인 메뉴로 돌아간다":
            $ renpy.full_restart()

label r13_object_mechanism(kind):
    if not r13_secret_route_available():
        return
    if kind=="passage_exit":
        call r13_observe([(None,"손잡이를 당기자 안쪽에서 걸쇠가 풀렸다. 책장 뒤판을 밀면 우리 객실로 나갈 수 있다.")],"puzzle:inside:release")
        menu:
            "2층 객실로 나간다":
                $ r13_edit(location="room13")
            "통로를 더 살핀다":
                pass
        return
    if kind=="kitchen_switch":
        if not r13_has("switch_found"):
            call r13_observe([(None,"선반 아래 덮개를 옆으로 밀었다. 안에 작은 레버가 있고, 금속 줄이 벽 안으로 이어진다. 전선은 없다.")],"puzzle:switch:find")
            $ r13_flag("switch_found")
        if r13_has("E04"):
            call r13_observe([(None,"도면에 덧그린 걸쇠 표시와 모양이 같다. 붉은 선의 반대쪽 끝은 2층으로 이어진다.")],"puzzle:switch:plan")
        window hide
        call screen r13_lever_actions(room13["kitchen_switch"])
        if _return == "raise":
            $ r13_edit(kitchen_switch=True)
            $ source_fx("tap")
            call r13_observe([(None,"손을 떼도 레버는 올라간 채 그대로다. 벽 속 금속 줄이 팽팽하게 당겨졌다.")],"puzzle:switch:on")
        elif _return == "lower":
            $ r13_edit(kitchen_switch=False,passage_open=False)
            $ source_fx("tap")
            call r13_observe([(None,"금속 줄이 느슨해졌다. 곧 위층에서 작은 걸쇠 소리가 났다.")],"puzzle:switch:off")
        return
    if kind=="book_latch":
        if room13["passage_open"]:
            call r13_observe([(None,"책장 아래쪽 판이 안으로 밀린다. 틈 너머 좁은 계단에서 찬 공기가 올라온다.")],"puzzle:book:open")
            menu:
                "통로로 들어간다":
                    $ r13_edit(location="passage")
                "일단 방에 남는다":
                    pass
            return
        call r13_observe([(None,"책장 오른쪽 아래의 붉은 책. 다른 책보다 깊이 박혀 있다. 당겨도 빠지지 않는다.")],"puzzle:book:look:v2")
        menu:
            "책의 아래쪽을 누르고 옆으로 젖힌다":
                if room13["kitchen_switch"]:
                    $ source_fx("door")
                    $ r13_edit(passage_open=True)
                    $ r13_flag("passage_known")
                    call r13_observe([(None,"책등이 움직이자 벽 안쪽에서 금속 소리가 났다. 책장 아래쪽 판이 벽 안으로 밀렸다. 어둠 속으로 내려가는 계단이 보인다. 안쪽에도 손잡이가 있다. 그 손잡이를 당기면 주방 쪽 걸쇠와 상관없이 문을 밀어 열 수 있다."),("dad","안에서 나오는 쪽에서는 갇히지 않게 만들어 뒀군."),(None,"손을 떼자 판이 다시 닫혔다. 하지만 걸쇠는 풀린 그대로라 다시 밀 수 있다.")],"puzzle:book:unlocked")
                    $ r13_grant(["E37"],"주방 레버와 2층 책장 손잡이의 실제 작동")
                    menu:
                        "통로로 들어간다":
                            $ r13_edit(location="passage")
                        "지금은 방에 남는다":
                            pass
                else:
                    call r13_observe([(None,"책이 조금 흔들린다. 그 이상은 움직이지 않는다.")],"puzzle:book:locked:v2")
            "다른 곳을 살핀다":
                pass
        return
    return

label r13_case_interview:
    call r13_scene("winter","초소 안 보호실 · 만남","quiet")
    call r13_lines([("daram","아빠가 내 탓이 아니라고 말하면…… 그럼 아닌 거야?"),("dad","아빠가 우긴다고 사실이 바뀌는 건 아니야."),("daram","그런데 왜 자꾸 내 탓이 아니라고 해?"),("dad","네가 한 일하고, 사람들이 네가 했다고 말하는 일이 같은지 알아보려는 거야."),("daram","내가 할아버지 때린 건 맞아.")],"case:interview:opening:v3")
    menu:
        "무엇부터 확인할까?"
        "어디를 어떻게 때렸는지 묻는다":
            call r13_lines([("dad","할아버지 어디를 때렸어?"),("daram","여기, 나 잡은 팔. 할아버지가 안 놔줘서 때렸어. 촛대가 무거워서 두 손으로 들었어."),("dad","할아버지한테 놔 달라고는 했어?"),("daram","했어. 놔 달라고 계속 말했어.")],"case:interview:arm:v3")
        "침대 아래로 들어간 뒤의 일을 묻는다":
            call r13_lines([("dad","침대 밑에 숨은 다음에 밖으로 나온 적 있어?"),("daram","아빠가 부르기 전엔 한 번도 없어."),("dad","그동안 누가 방에 들어오는 건 봤어?"),("daram","침대 밑이라 이불밖에 안 보였어. 바닥은 연기 때문에 매웠고. 누가 문 두드릴 때마다 눈 감았어.")],"case:interview:bed:v3")
    call r13_lines([("dad","할아버지 손이 풀린 뒤에는?"),("daram","촛대 놓쳤어. 바닥에 떨어져서 쨍 했고. 또 잡힐까 봐 침대 밑으로 들어갔어."),("dad","방문은 누가 잠갔어?"),("daram","할아버지가 잠갔어. 종이를 꺼내다가 밖에서 발소리가 나니까 문에 빗장을 걸었어."),("dad","할아버지가 넘어지는 걸 직접 봤어?"),("daram","……모르겠어. 내가 때렸잖아. 그다음에 할아버지가 안 일어났잖아."),("dad","모르는 건 모른다고 적을게. 억지로 더 기억해 내야만 여기서 나갈 수 있는 건 아니야."),(None,"면회 기록에는 다람이의 말과, 확인하지 못한 부분을 나누어 적었다. 아이의 말만으로는 어르신이 죽음에 이른 순서를 정할 수 없다.")],"case:interview:record:v3")
    return True

label r13_mother_intervention:
    if r13_has("mother_intervened"):
        return
    # First daily relay after the incident. A scene shows her action, not a rescue deus ex machina.
    call r13_scene("r13_clinic","금요일 · 진료실 앞","quiet")
    call r13_lines([("resident_lamplighter","오늘 아침에 사건 소식을 전했습니다. 그랬더니 여기서 보자고 하셨어요."),("dad","누가 보자고 했다는 겁니까?"),("mom","나야."),(None,"엄마는 젖은 장갑도 벗지 않은 채였다. 나를 보고 한 걸음 다가오다가, 이내 너울 쪽으로 돌아섰다."),("mom","아이부터 만나게 해 주세요. 저를 찾던 거라면 이렇게 제가 직접 왔어요."),("neoul","부엉이 어르신 사망 사건입니다. 어머니가 오셨다는 이유로 아이를 내보낼 수는 없습니다."),("dad","사건 소식은 언제 들었어?"),("mom","오늘 아침. 어제 받은 편지는 사건 전에 온 거였어. 다람이, 많이 다쳤어?"),("dad","할아버지한테 팔을 붙잡혔었어. 지금은 움직일 수 있어."),("granny","연구한 원본을 가져오면 아이 일도 이야기해 볼 수는 있겠지."),("mom","그 연구를 내놓으면 아이에게 걸린 의심이 풀리나요?"),("granny","사람이 죽었는데 그걸 없던 일로 할 수는 없잖아."),("mom","그럼 기록부터 다시 봐 주세요. 제가 왔다는 사실 말고, 아이가 실제로 한 일을 보고요."),("resident_seori","어머니 부탁과는 별개로 범행 도구는 다시 대조하겠습니다. 원본을 가져오십시오.")],"mother:day5:intervention:v3")
    call r13_lines([(None,"너울이 면회 시간을 적었다. 경비가 엄마에게 연구 원본을 내놓으라고 했다. 그러자 초롱이 앞을 가로막았다."),("resident_lamplighter","저는 두 분의 만남을 주선했을 뿐입니다. 여기는 서류를 넘기는 자리가 아닙니다."),("mom","오늘 만남이 끝나면 다시 연락할게. 따라붙은 사람이 없는지 확인하기 전엔 나를 따라오지 마."),("dad","또 네가 어디 있는지도 모른 채 기다리라는 거야?"),("mom","표식은 초롱에게 남길게. 아이 기록은 네가 챙겨 줘. 나는 이 사람들이 아이를 붙잡아 둘 이유를 없앨 방법을 찾아올게.")],"mother:day5:contact:v3")
    $ r13_flag("mother_intervened","examination_agreed")
    $ r13_edit(mom_state="intervened")
    return

screen r13_lever_actions(raised):
    modal True
    zorder 70
    default ready=False
    timer .25 action SetScreenVariable("ready",True)
    $ lever_options=[("레버를 내린다" if raised else "레버를 올려 걸림턱에 건다",Return("lower" if raised else "raise"),False),("그대로 둔다",Return("leave"),False)]
    use r13_question_list(None,"neutral","올라간 레버가 걸림턱에 고정돼 있다." if raised else "선반 아래 레버는 내려가 있다.",lever_options,ready,list_left=280,list_width=720,animate=False)
    key "game_menu" action Return("leave")
