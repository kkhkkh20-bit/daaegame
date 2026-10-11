# Condensed chapter-one adaptation. Original public/v2 scripts stay unchanged.
label change_scene(background, music=None):
    window hide
    scene black with Dissolve(0.15)
    if music and renpy.music.get_playing() != music:
        play music music fadeout 0.15 fadein 0.25
    elif music is None:
        stop music fadeout 0.15
    $ renpy.pause(0.3,hard=True)
    scene expression background with Dissolve(0.22)
    return

label start:
    $ inventory, inspected, visited, resolved_topics = [], [], [], []
    $ lamp_ready = somsom_found = archive_permission = archive_open = False
    $ case_resolved = mother_clue = test_complete = False
    $ clock_rotated = clock_demonstrated = False
    $ wrong_attempts = conclusion_attempts = 0
    $ meeting_first = comparison_topic = None
    $ digit_code, code_error = [0,0,0,0], False
    $ typing_allowed, speaker, showdown_issue = True, "seryeon", "place"
    $ stage, place, clock_text = "arrival", "마차 안", "해 질 무렵"
    show screen hud
    call change_scene("bg carriage","assets/travel.mp3")
    daram "아빠, 표정 풀어. 아직 여관 밥도 안 먹었는데."
    dad "네가 내 주머니에 넣은 부스러기부터 먹고 있어."
    daram "비상식량이야. 길 잃으면 둘이 나눠 먹으려고."
    dad "그럼 길은 네가 찾는 거다."
    daram "저기 불 켜진 집! 오늘은 저기서 자자."
    $ place = "마을로 들어가는 길"
    call change_scene("bg approach","assets/travel.mp3")
    karo "우체국 앞에 내려 드릴게요. 돌아가는 차는 내일 정오고요."
    daram "정오까지 밥 세 번 먹을 수 있겠네."
    dad "편지 먼저 확인하고."
    $ place = "우체국 앞"
    call change_scene("bg post","assets/travel.mp3")
    daram "닫혔네. 눈 온다고 먼저 퇴근했나 봐."
    dad "내일 오자. 도장은 이 마을 게 맞으니까."
    daram "응. 편지는 내가 넣을게. 간식 없는 주머니에."
    $ current_location, place = "front", "여관 접수대"
    call change_scene("bg inn","assets/travel.mp3")
    play sound "assets/door.wav" volume 0.45
    call change_scene("bg front","assets/travel.mp3")
    jump roam

label roam:
    $ place = LOCATIONS[current_location][0]
    if current_location not in visited:
        $ visited.append(current_location)
    $ roam_music = "assets/travel.mp3" if stage == "arrival" else "assets/after.mp3" if stage == "aftermath" else "assets/search.mp3"
    call change_scene(LOCATIONS[current_location][1],roam_music)
    call screen explore(current_location)
    $ target = _return
    if target == "map":
        call screen village_map
        $ current_location = _return
        jump roam
    elif target == "rest":
        jump night_scene
    elif target == "meeting":
        if council_ready():
            jump meeting_entry
        elif not somsom_found:
            daram "잠깐. 할머니가 찾던 손님은 아직 못 찾았잖아."
        elif "registry" not in inventory:
            daram "저 애가 왜 여기서 잤는지부터 알고 싶어."
        else:
            dad "목격 시각을 확인하고 모이자. 잘못된 말로 몰아붙일 수는 없어."
        jump roam
    elif target == "finish":
        if mother_clue:
            jump chapter_end
        dad "할머니께 인사는 하고 가자."
        jump roam
    call local_interaction
    jump roam

label local_interaction:
    if current_location == "room":
        call room_interaction
        return
    if current_location == "hall" and target == "clock":
        call clock_inspection
        return
    if current_location == "doto" and target == "notebook":
        $ target = "talk"
    $ person = LOCATIONS[current_location][2]
    show expression person + " neutral" as visitor at portrait_close
    if stage == "arrival":
        if person == "granny":
            if "granny_arrival" not in inspected:
                granny "어서 와요. 둘이 묵을 방 찾으세요?"
                dad "네. 내일 우체국에 들르려고요."
                granny "언덕을 또 내려가려면 든든히 먹어 둬야겠네요."
                daram "아빠, 들었지? 이건 할머니 지시야."
                granny "지시는 아니고, 수프는 남았지."
                granny "방은 계단 위예요. 둘이 쓸 열쇠 여기 있어요."
                dad "감사합니다. 이 사진도 한번 봐 주시겠습니까?"
                granny "…우체국에서 찾는 분이 이분인가요?"
                dad "제 아내입니다."
                granny "사진은 넣어 둬요. 아가 손이 얼었네요."
                daram "난 괜찮아요. 아빠 손이 더 차가워."
                $ mark_seen("granny_arrival")
            else:
                granny "수프는 부엌에 있어요. 방은 계단 바로 위고요."
        elif person == "nabi":
            if "nabi_arrival" not in inspected:
                nabi "수프? 그릇은 딱 두 개 남았네."
                daram "큰 거 아빠 줘요. 아빠 건 내가 조금씩 먹게."
                nabi "그건 큰 거 네가 달라는 말이지?"
                daram "들켰네."
                nabi "창가 쥐들은 깨우지 마. 첫눈 오면 자러 오는 손님들이야."
                dad "몸이 차갑군요."
                nabi "겨울잠 들면 그래. 수건만 덮어 줘."
                $ mark_seen("nabi_arrival")
            else:
                nabi "수프는 더 줄 수 있어. 그릇은 네가 씻어."
                daram "아빠, 우리 이제 일자리도 생겼어."
        elif person == "karo":
            karo "여관은 찾았어요? 나는 내일 정오까지 여기 있어요."
            daram "밥을 얻었어요. 이제 방만 얻으면 돼요."
            karo "그 순서면 이 마을에서 굶지는 않겠네."
    elif stage == "aftermath":
        call aftermath_talk
    elif person == "granny":
        if not archive_permission:
            daram "할머니, 주머니보다 베개 구석을 먼저 찾으셨죠?"
            granny "거기 자던 손님이 없어졌어."
            dad "누군지 알아야 찾을 수 있습니다."
            granny "이름을 적지 말아 달랬어. 돈 없는 손님을 재운 벌금은 내가 내면 돼."
            daram "그럼 이름 빼고 찾아요. 어디서 자는지만 알려 주세요."
            granny "…침대 밑 상자에 옛 장부가 있어. 첫 손님 날짜로 잠갔지."
            granny "오늘은 봐도 돼. 남의 이름을 밖에 옮기지만 마."
            $ archive_permission = True
        else:
            granny "상자는 열어도 돼. 그 아이가 어디 갔는지부터 봐 줘."
    elif person == "nabi":
        if "kitchen" not in inventory:
            daram "이불 손자국, 밀가루 맞죠?"
            nabi "내 손이야. 밤 열한 시에 반죽하다 이불을 펴 드렸어."
            dad "안 쓰는 방이라고 들었습니다만."
            nabi "안 쓴다는 말과 아무도 안 잔다는 말은 다르더라."
            nabi "그다음엔 부엌에 있었어. 손님 깨울까 봐 뒤 계단으로 다녔고."
            daram "깨우면 안 되는 손님… 창가 쥐들처럼?"
            nabi "할머니한테 물어봐. 이 등잔은 가져가도 돼. 손 조심하고."
            $ acquire("kitchen")
            $ lamp_ready = True
        else:
            nabi "등잔 가져갔지? 어두운 데 손부터 넣지 마."
    elif person == "bami":
        if "bami" not in inventory:
            bami "나 자는 시간인데. 목소리 조금만 낮춰."
            daram "밤에 여기서 잤어?"
            bami "밤엔 깨어 있어. 다섯 시 종 치면 자고."
            dad "주머니를 들고 지나간 사람을 봤습니까?"
            bami "세련. 여섯 시 반쯤 끝방으로 갔다가 빈손으로 왔어."
            daram "다섯 시에 잤다면서 여섯 시 반엔 어떻게 봤어?"
            bami "그러게… 그 시계만 봤는데. 숫자가 없어서."
            $ acquire("bami")
        else:
            bami "그 손님이 끝방으로 간 건 확실해. 시각은… 같이 다시 봐 줘."
    elif person == "doto":
        if "snow" not in inventory:
            doto "공책은 손 말리고 만져요. 한 해를 다 적었으니까."
            daram "첫눈 기다리느라 안 잤어요?"
            doto "그 칸은 하루 지나서 채울 수 없어요. 자정, 종 열두 번."
            dad "복도에도 나왔습니까?"
            doto "네. 밤이가 창문 좀 닫으라더군요. 자기는 늘 거꾸로면서."
            daram "그럼 첫눈 때 밤이는 깨어 있었네."
            $ acquire("snow")
        else:
            doto "고치려면 이유가 있어야 해요. 공책도, 사람 말도."
    elif person == "karo":
        if "karo" not in inventory:
            karo "세련 씨를 기다려요? 어제는 나도 기다렸는데."
            dad "어디서요?"
            karo "아랫마을 주막. 노름판을 못 떠나서 차를 놓쳤지."
            daram "얼마나 잃었어요?"
            karo "남의 주머니까지 세지는 않아. 앉아 있던 것만 봤어."
            $ acquire("karo")
        else:
            karo "차는 기다려 줄게요. 먼저 판정 내리고 보내면 안 되잖아."
    hide visitor
    return

label night_scene:
    $ place, clock_text = "2층 복도", "첫눈이 오기 전"
    call change_scene("bg hall","assets/night.mp3")
    show bami world:
        xpos 840 ypos 100 zoom 0.65
    daram "아빠, 거꾸로 매달린 손님 있어."
    bami "바닥에 선 손님이 둘 있네."
    daram "내일은 나도 거꾸로 인사해 줄게."
    dad "꼬리로 매달릴 생각은 하지 마."
    bami "끝방은 건드리지 마. 할머니가 잠자리를 펴 놨어."
    daram "안 쓰는 방이라더니."
    dad "우리 방으로 가자. 남의 잠자리까지 볼 이유는 없어."
    hide bami
    $ mark_seen("night_bami")
    $ stage, place, clock_text = "conflict", "열세 번째 침대", "다음 날 아침"
    call change_scene("bg room","assets/search.mp3")
    show seryeon neutral at portrait_close
    seryeon "제 돈이 여기서 나왔는데 왜 아직도 확인만 합니까?"
    neoul "봉인은 그대로였고, 제가 잘라 열었습니다. 안에는 백 냥입니다."
    nabi "나도 옆에서 봤어요. 끊어진 데 없는 띠를 잘라서 열었죠."
    seryeon "삼백 냥을 넣었습니다. 이백 냥은 이 방 주인이 물어내야죠."
    granny "난 네 돈에 손댄 적 없어."
    seryeon "그럼 이 방을 못 보게 한 이유부터 말씀하세요."
    granny "그건… 네게 할 말이 아니야."
    daram "아빠, 할머니 계속 베개 옆만 봐. 주머니 말고."
    dad "알아. 그래서 아직 떠날 수 없어."
    dad "방을 살펴봐도 되겠습니까?"
    neoul "돈은 제가 보관하죠. 빈 주머니와 봉인띠는 이 방에서 살펴보셔도 됩니다."
    $ acquire("seal")
    hide seryeon
    $ stage, current_location = "investigation", "room"
    jump roam

label clock_inspection:
    if "clock" not in inventory:
        daram "여기도 숫자가 없네. 윗쪽 표시는 어디야?"
        dad "벽에 걸린 방향으로 읽는 거지."
        daram "그럼 밤이는 이걸 어떻게 봤을까."
        $ acquire("clock")
    else:
        dad "이 시계는 바늘 방향으로 읽는다. 보는 방향도 기록해 두자."
    return

label room_interaction:
    if target == "pouch":
        $ place = "발견 당시 주머니"
        call change_scene("cg pouch","assets/search.mp3")
        if "pouch" not in inventory:
            daram "도장 잉크가 아직 묻네. 별 끝이 말렸어."
            dad "찾을 때 봉인은 끊어지지 않았다고 했지."
            daram "이 계약서, 할머니 이름 칸이 비어 있어."
            dad "팔기로 한 여관은 아니라는 거다."
            $ acquire("pouch")
        else:
            dad "백 냥과 빈 서명 칸. 봉인은 너울 씨가 열었다."
    elif target == "flour":
        if "flour" not in inventory:
            daram "하얀 손자국이야. 빵 냄새도 나."
            dad "씻어 내기 전에 누가 이불을 폈는지 물어보자."
            $ acquire("flour")
        else:
            daram "이 손은 주머니보다 이불 끝을 잡았네."
    elif target == "head":
        $ mark_seen("head_date")
        daram "빛 받으니까 읽힌다. 첫 손님, 열한 번째 달 둘째 날."
        dad "처음 받은 손님 날짜를 새겼군."
    elif target == "chest":
        if not archive_permission:
            daram "자물쇠네. 열어 볼까?"
            dad "방 주인에게 먼저 묻자."
        elif not archive_open:
            call screen chest_lock
            if _return == "opened":
                $ archive_open = True
                daram "열렸어. 첫 손님을 잊지 않으려고 잠근 거네."
                dad "뒤의 이름들은 건드리지 말자."
                daram "첫눈마다 작은 손님, 베개 구석… 여기도, 여기도."
                $ acquire("registry")
        else:
            daram "첫눈마다 베개 구석. 그런데 오늘은 비어 있었어."
    elif target == "under":
        if somsom_found:
            dad "작은 손님은 수건에 싸서 나비에게 맡겼다. 자리는 그대로 두자."
        elif not search_ready():
            daram "상자 뒤는 안 보여. 아빠 손도 안 들어갈 것 같은데."
            if not lamp_ready:
                dad "잡아당기지 마. 부엌에서 등잔을 빌려오자."
            elif not archive_permission:
                dad "상자를 움직여도 되는지 주인에게 먼저 묻자."
            else:
                dad "장부에서 원래 잠자리를 확인하고 움직이자. 흔적을 섞으면 안 돼."
        else:
            $ typing_allowed = False
            call change_scene("bg room",None)
            daram "등잔 조금만 낮춰 줘. 저 틈에… 털이 있어."
            dad "뒤로 물러서. 아빠가 꺼낼게."
            call change_scene("cg somsom",None)
            daram "…쥐야? 왜 이렇게 차가워?"
            dad "아직 몰라. 수건부터 가져와 줘."
            daram "같이 가면 안 돼? 혼자 두기 싫어."
            dad "그래. 둘이 받쳐 들자."
            neoul "무슨 일입니까?"
            dad "작은 손님을 찾았습니다. 상태부터 확인해 주십시오."
            neoul "장소는 따로 듣겠습니다. 지금은 발견한 방만 알리죠."
            $ somsom_found = True
            $ acquire("record")
            $ acquire("fur")
            $ typing_allowed = True
            daram "털에 빨간 글씨도 묻었어. 거꾸로 된 별. 닦지 말까?"
            dad "응. 수건으로 덮기 전에 모양을 남기자."
            nabi "내 바구니에 눕혀. 따뜻한 수건 더 가져올게."
            buri "차갑고 안 움직여요? 그럼… 늦은 건가."
            daram "잠깐만요. 아직 아무도 확인 안 했잖아요."
            neoul "돈 이야기는 뒤로. 다들 식당으로 모여 주십시오."
    return

label meeting_entry:
    $ stage, place, clock_text = "meeting", "여관 원탁", "정오가 되기 전"
    call change_scene("bg council","assets/meeting.mp3")
    show screen round_table
    granny "솜솜이야. 첫눈마다 여기로 오는 손님."
    buri "겨울잠이면 이렇게 차가워집니까?"
    granny "네가 시계에 귀 대듯, 그 아이 숨부터 들어 봐."
    menu:
        "지금 먼저 확인할 것은?"
        "작은 손님의 숨":
            pass
        "누가 죽였는지":
            $ conclusion_attempts += 1
            dad "죽었다는 것도 아직 확인하지 못했습니다."
    $ typing_allowed = False
    daram "…수염 움직였어. 아빠, 봤지?"
    dad "봤어. 숨도 있다."
    nabi "다행이다. 내 수건은 좀 더 덮어 둘게."
    $ typing_allowed = True
    seryeon "그렇다면 이제 제 돈 얘기를 하죠."
    daram "살아 있다고 그 자리에 혼자 들어간 건 아니잖아요."
    dad "각자 본 것을 들어 봅시다."
    jump council_loop

label council_loop:
    window hide
    call screen council
    $ action_kind, action_value = _return
    if action_kind == "speaker":
        $ speaker = action_value
        $ meeting_first = comparison_topic = None
        jump council_loop
    elif action_kind == "duel":
        jump showdown_entry
    elif action_kind == "press":
        call resident_press
        jump council_loop
    call screen evidence_book(present=True)
    $ evidence_choice = _return
    if evidence_choice != "cancel":
        call council_evidence
    jump council_loop

label resident_press:
    if speaker == "granny":
        granny "이름을 안 묻겠다고 재웠어. 그 약속까지 팔면 다음 겨울엔 어디서 자니."
        daram "그래서 돈 이야기에도 입 다물었어요?"
        granny "난 벌금을 내면 돼. 그 아이는 잠자리를 잃잖아."
    elif speaker == "nabi":
        nabi "할머니 없으면 밤에 빵 굽는 나도 나가야 해. 그래서 도와드린 거야."
    elif speaker == "bami":
        bami "가면서 주머니를 들었고 돌아올 땐 없었어. 그건 안 뒤집어 봤어."
    elif speaker == "doto":
        doto "내가 종 열두 번을 적을 때 밤이는 창문을 닫으랬어요. 잠들어 있지 않았죠."
    elif speaker == "buri":
        buri "다 식으면 끝이라 생각했어요. 장치만 만지다 보니… 함부로 말했군요."
    elif speaker == "karo":
        karo "노름판은 봤어. 이백 냥을 잃었다고 말하면 그건 내가 지어내는 거지."
    elif speaker == "neoul":
        neoul "장부 밖 손님 벌금과 도난은 다른 일입니다. 둘을 묶어 판정하지 않겠습니다."
    else:
        seryeon "돈을 받고 돌아가야 해요. 삼백 냥을 제가 직접 세고 봉했습니다."
    return

label council_evidence:
    if speaker == "nabi" and evidence_choice in ("flour","kitchen"):
        nabi "내가 편 이불이야. 손자국을 보고 날 의심하는 건 이해해."
        nabi "하지만 할머니 도우러 간 일을 도둑질로 바꾸진 마."
        if "quilt" not in resolved_topics:
            $ resolved_topics.append("quilt")
    elif speaker in ("bami","doto") and evidence_choice in ("clock","snow","bami"):
        if "clock" in resolved_topics:
            bami "맞아. 자정이었어. 주머니를 든 그 손님을 봤어."
            return
        if comparison_topic != "clock":
            $ comparison_topic, meeting_first = "clock", evidence_choice
            if evidence_choice == "snow":
                doto "첫눈은 자정. 하지만 이 기록만으론 왜 여섯 시 반이라 했는지 모르죠."
            else:
                bami "시계는 거꾸로 봤어. 그래도 그때 눈 뜨고 있었던 건 맞아."
            daram "본 시각하고 깨어 있던 시간을 같이 맞춰 보자."
        elif evidence_choice == meeting_first:
            dad "같은 기록만 다시 볼 수는 없다. 다른 쪽을 비교하자."
        else:
            call screen clock_compare
            menu:
                "밤이가 본 것은 언제인가?"
                "첫눈이 내린 자정":
                    pass
                "아침 여섯 시 반":
                    $ conclusion_attempts += 1
                    daram "그때는 밤이가 이미 자고 있었어. 다시 보자."
                    return
            bami "…위아래를 반대로 읽었네. 자정이야. 미안."
            seryeon "남의 말이 바뀌었다고 제 말까지 거짓은 아니죠."
            neoul "다른 기록과 맞는 정정입니다. 자정으로 남기겠습니다."
            $ resolved_topics.append("clock")
            $ meeting_first = comparison_topic = None
    elif speaker == "seryeon" and evidence_choice in ("pouch","fur","seal"):
        if "contact" in resolved_topics:
            seryeon "닿았다는 얘기는 들었습니다. 그 이상을 보여 주세요."
            return
        $ compared_key = "pouch" if evidence_choice == "seal" else evidence_choice
        if comparison_topic != "contact":
            $ comparison_topic, meeting_first = "contact", compared_key
            if compared_key == "fur":
                dad "털의 붉은 자국입니다. 뒤집힌 글씨와 말린 별 끝."
                seryeon "붉은 얼룩이 다 제 것입니까?"
            else:
                dad "봉인띠의 도장입니다. 잉크가 덜 말랐고 별 끝이 말렸습니다."
                seryeon "제 주머니에 제 도장이 있는 게 이상합니까?"
            daram "다른 쪽도 봐야겠네."
        elif compared_key == meeting_first:
            daram "아빠, 다른 데 남은 자국하고 비교해야지."
        else:
            menu:
                "두 자국으로 알 수 있는 것은?"
                "주머니의 도장이 솜솜에게 닿았다":
                    pass
                "세련이 이백 냥을 훔쳤다":
                    $ conclusion_attempts += 1
                    dad "접촉한 흔적만으로 돈의 행방까지 알 수는 없습니다."
                    return
            seryeon "…닿았더라도 누가 닿게 했는지는 모르잖아요."
            neoul "그렇죠. 그래서 시각과 움직임도 함께 봅니다."
            $ resolved_topics.append("contact")
            $ meeting_first = comparison_topic = None
    else:
        $ wrong_attempts += 1
        if evidence_choice == "karo":
            karo "노름을 했다고 여기서 도둑질한 건 아니야. 주머니부터 봐요."
        elif evidence_choice == "registry":
            granny "이 장부는 손님을 재운 기록이야. 돈을 가져간 기록은 아니고."
        elif evidence_choice == "flour":
            nabi "그건 내 이불 손자국이야. 지금 발언과는 다른 일이네."
        else:
            dad "이 기록은 다른 질문에 쓰는 편이 맞겠군요. 지금 발언을 확인하지는 못합니다."
    return

label showdown_entry:
    $ stage, place, showdown_issue = "showdown", "여관 원탁", "place"
    play music "assets/pressure.mp3" fadeout 0.2 fadein 0.25
    seryeon "침대 밑 상자 뒤에 처박혀 있던 쥐 때문에 제 돈을 잊으셨군요."
    daram "…상자 뒤?"
    jump showdown_loop

label showdown_loop:
    window hide
    call screen duel
    if _return == "press":
        if showdown_issue == "place":
            seryeon "누군가 말했겠죠. 여기 온 손님이 저만은 아니잖아요."
        elif showdown_issue == "movement":
            seryeon "복도를 걸었다고 주머니를 숨긴 사람이 되는 건 아닙니다."
        else:
            seryeon "이백 냥은 사라졌어요. 누군가는 내야 합니다."
        jump showdown_loop
    call screen evidence_book(present=True)
    $ evidence_choice = _return
    if evidence_choice == "cancel":
        jump showdown_loop
    if showdown_issue == "place" and evidence_choice == "record":
        neoul "저는 방만 발표했습니다. 처음 자리는 발견한 두 분과 따로 들었고요."
        dad "우린 그 뒤 내내 같이 다녔습니다. 누구에게 들었습니까?"
        seryeon "…그 방에 가기는 했어요. 쓰러져 있길래 치운 겁니다."
        daram "치웠다고? 아까는 처음 보는 쥐라며."
        $ showdown_issue, meeting_first = "movement", None
    elif showdown_issue == "movement" and evidence_choice in ("bami","fur","pouch"):
        $ movement_key = "fur" if evidence_choice == "pouch" else evidence_choice
        if meeting_first is None:
            $ meeting_first = movement_key
            if movement_key == "bami":
                bami "자정에 주머니를 들고 끝방으로 갔어. 돌아올 땐 빈손."
                seryeon "들고만 간 겁니다."
            else:
                daram "그냥 들고만 있었다면 솜솜 털에 왜 도장이 눌려 찍혀?"
                seryeon "다른 사람이 주머니를 만졌을 수도 있잖아요."
        elif movement_key == meeting_first:
            dad "움직임과 닿은 흔적. 양쪽을 함께 확인하자."
        else:
            dad "당신이 든 주머니가 그 방에 남았고, 도장이 손님의 털에 닿았습니다."
            daram "손님도 옮겼다고 했죠. 그런데 주머니는 못 봤다는 거예요?"
            seryeon "그래도 돈이 없어진 건 사실입니다."
            $ showdown_issue, meeting_first = "money", None
    elif showdown_issue == "money" and evidence_choice in ("seal","pouch"):
        neoul "당신이 봉한 뒤 제가 열 때까지 봉인은 끊어지지 않았습니다."
        dad "누가 돈을 꺼냈다는 주장부터 맞지 않습니다."
        menu:
            "봉인과 백 냥이 입증하는 것은?"
            "봉한 뒤에는 이백 냥이 빠져나가지 않았다":
                pass
            "까로가 이백 냥을 훔쳤다":
                $ conclusion_attempts += 1
                karo "내가 본 건 노름판이지, 이 주머니 속이 아니에요."
                jump showdown_loop
        dad "봉하기 전 삼백 냥이었다는 근거는 당신 말뿐입니다. 할머니가 갚을 빚은 입증되지 않았어요."
        jump case_verdict
    else:
        $ wrong_attempts += 1
        if evidence_choice == "karo":
            karo "잃은 액수는 안 봤어요. 그 말로 없는 증거를 채우진 맙시다."
        elif evidence_choice == "registry":
            granny "그 아이를 숨긴 이유는 내게 물어. 돈이 줄어든 이유는 그 장부에 없어."
        else:
            dad "그 기록만으로 지금 주장을 반박할 수는 없습니다. 다른 사실과 맞춰 보죠."
    jump showdown_loop

label case_verdict:
    $ case_resolved = True
    neoul "할머니에게 도난 책임을 묻지 않겠습니다. 강제로 계약서를 쓰게 할 근거도 없습니다."
    seryeon "…회사에는 빈손으로 돌아갈 수 없었어요."
    karo "노름판에서 나왔으면 어제 차에 탈 수 있었죠."
    seryeon "남은 백 냥만이라도 돌려놓고, 부족한 돈을 받아 내려 했어요."
    granny "그래서 자는 손님까지 상자 뒤로 밀었니."
    seryeon "죽은 줄 알았습니다. 내가 들어온 걸 알면… 나를 잡을까 봐."
    daram "그럼 사람을 불렀어야죠."
    neoul "허위 신고와 손님을 옮긴 일은 별도로 조사하겠습니다. 돈 쓴 곳도 확인하고요."
    $ stage, clock_text, current_location = "aftermath", "사건 이후", "front"
    hide screen round_table
    jump roam

label aftermath_talk:
    if person == "granny":
        if not mother_clue:
            granny "장부 밖 손님 벌금은 내가 내야지. 그런데 이 여관까지 넘길 생각은 없어."
            dad "아침에 사진을 보고 멈추셨죠."
            granny "지난겨울에 왔어. 네 아내. 열세 번째 침대 곁에서 누굴 기다렸지."
            daram "…사진 다시 꺼내 줘, 아빠."
            granny "이름을 묻지 않겠다고 약속한 사람을 찾고 있었어."
            dad "그 사람이 누굽니까?"
            granny "나도 이름은 몰라. 네 아내는 우체국 뒤 창고에 편지를 맡기고 갔어."
            daram "내일 우체국부터 가자. 오늘은 할머니 손님 자게 두고."
            $ mother_clue = True
        else:
            granny "방은 오늘도 비워 둘게. 솜솜도, 너희도 편히 자."
    elif person == "nabi":
        nabi "수프 두 그릇 남겨 놨어. 오늘은 큰 그릇 네 거야."
        daram "아빠 것도 조금씩 먹을 건데."
        nabi "그건 알고 남겼어."
    elif person == "bami":
        bami "앞으로 시각 물으면 종 소리도 같이 말할게."
        daram "난 네가 거꾸로 자는 게 좋아. 틀려도 멋있잖아."
        bami "틀리는 건 빼고 좋아해 줘."
    elif person == "doto":
        doto "오늘 기록은 한 줄 더 써야겠네요. 첫눈, 작은 손님 생존."
        dad "고친 이유도 남겨 두십시오."
        doto "그래야 다음 해의 내가 믿죠."
    elif person == "karo":
        karo "오늘 차는 떠나도 내일 다시 와요. 돌아갈 자리까지 없어지는 건 아니고."
        daram "내일은 우체국 먼저예요. 좌석은 아직 안 잡을게요."
    return

label chapter_end:
    $ stage, place = "ending", "열세 번째 침대"
    call change_scene("bg room","assets/after.mp3")
    daram "아빠, 수첩에 오늘 일 적어도 돼? 이름은 빼고."
    dad "그래. 틀렸던 것도 적고."
    daram "그건 작은 글씨로 적을게."
    dad "작아도 읽히게 써라."
    daram "…내일 창고에 갈 땐 나도 같이야."
    dad "같이 가자. 오늘처럼 앞서 뛰지만 마."
    $ typing_allowed = False
    daram "방금 창문 두드렸어?"
    stop music fadeout 0.6
    dad "아니."
    daram "그럼 밖에서 누가…"
    $ stage, test_complete = "complete", True
    window hide
    call screen trial_complete
    return
