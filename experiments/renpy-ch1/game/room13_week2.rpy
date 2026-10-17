# Days 8–14: rescue, reunion, disaster response, confrontation and completed endings.
label r13_week2_opening:
    $ r13_upgrade()
    if room13["week2_started"]:
        jump r13_week2_day
    $ r13_edit(day=R13_WEEK2_DAY,period=0,location="inn",week2_started=True)
    show screen r13_hud
    call r13_scene("front","월요일 아침 · 꺼져 가는 난방","night")
    if room13["granny_state"]=="detained":
        call r13_lines([(None,"접수대가 비어 있었다. 할머니 대신 나비가 열쇠를 들고 손님 수를 세었다."),("nabi","할머니는 아직 경비실에 계세요. 그래서 이 문은 제가 잠글게요.")],"week2:granny_held")
    else:
        call r13_lines([(None,"아래층 난방관에서 소리가 멎었다. 할머니는 불 꺼진 방들의 열쇠를 따로 챙겼다.")],"week2:granny_free")
    if room13["daram_state"]=="held":
        call r13_lines([("neoul","보호시설 난방도 약해졌습니다. 환자들을 다른 곳으로 옮긴다는 말이 나오고 있습니다."),("dad","다람이도 옮겨지는 환자에 포함됩니까?"),("neoul","지금 쓰고 있는 명단을 확인해야 합니다. 지난 재판 기록만으로는 이번에 누구를 끌고 갈지 알 수 없습니다."),(None,"판결이 내려졌어도 아이에게 가는 길이 끝난 것은 아니었다. 옮겨질 사람들의 명단부터 찾아야 한다.")],"week2:rescue_route")
    else:
        call r13_lines([("daram","아빠. 저 사람, 어제도 저기서 배관 고쳤잖아."),(None,"배관을 고치던 주민이 자기 이름을 잊었다. 길 건너에서는 빈 식량 자루를 두고 언성이 높아졌다."),("dad","아빠랑 여기서 같이 지켜보자."),("daram","물 가져다줄까? 먼저 물어보고 줄게.")],"week2:family_route")
    # 0.18.90: 초롱이 죽은 판에서는 돌의 바늘을 보는 우박이 말한다.
    call r13_lines([("resident_ubak" if r13_has("chorong_dead") else "resident_lamplighter","등불이 어두워진 건 나중이에요. 며칠 전부터 힘을 재는 바늘이 먼저 흔들렸어요."),(None,"재판에서 누구 편을 들었든, 눈과 추위는 마을 전체를 덮고 있었다. 학교는 교실을 비웠다. 진료소는 복도까지 자리를 깔았다.")],"week2:crisis")
    if r13_has("warning_exposed"):
        $ r13_flag("pursuit_active")
        call r13_lines([(None,"여관에서 편지 이야기가 새어 나갔다. 다음 편지를 누가 가져오는지 묻고 다니는 사람이 있다고 했다.")] if r13_has("chorong_dead") else [("resident_lamplighter","여관에서 편지 이야기가 새어 나갔어요. 다음 편지를 누가 가져오는지 묻고 다니는 사람이 있어요.")],"week2:prior_disclosure")
    jump r13_roam

label r13_week2_day:
    $ r13_upgrade()
    if not room13["week2_started"]:
        jump r13_week2_opening
    if room13["day"]>=14:
        jump r13_finale
    jump r13_roam

label r13_week2_events:
    if room13.get("reply_due") is not None and r13_abs_time()>=room13["reply_due"] and not r13_has("E19") and not r13_has("chorong_dead") and not r13_has("mom_reunited"):
        call r13_scene("winter_square","광장 · 등 밑의 답장","search")
        call r13_lines([("resident_lamplighter","답이 왔습니다. 예전 은신처 말고 지금 보내는 신호를 확인하라는군요."),(None,"「폐온실 아래 등 표식을 봐 줘. 주소를 다른 사람에게 말하지 마. 뒤따르는 사람이 있으면 들어오지 말고.」")],"week2:reply")
        $ r13_grant(["E19"],"초롱이 직접 가져온 현재 답장")
        $ r13_edit(mom_state="contacted")
    if r13_has("contact_compromised") and "contact_relocated" not in room13["events"]:
        call r13_lines([(None,"광장 등 밑에 짧은 쪽지가 끼워져 있었다. 「약속 장소에 경비가 먼저 와 있었어. 자리를 바꿨어. 새 표식을 봐 줘.」"),("dad","(아내 글씨다. 살아 있다.)",{"thought":True})] if r13_has("chorong_dead") else [("resident_lamplighter","약속 장소에 경비가 먼저 와 있었어요. 그래서 부인께서 자리를 바꾸셨어요. 새 표식을 확인해야 해요."),("dad","아내가 살아 있다는 거죠?"),("resident_lamplighter","제가 직접 받은 신호로는 그렇습니다. 다음 신호도 같이 확인해 봅시다.")],"week2:relocated")
        $ r13_event("contact_relocated")
    if r13_has("convoy_changed") and "convoy_changed_notice" not in room13["events"]:
        call r13_lines([("neoul","사람을 끌고 가는 경비 조가 바뀌었습니다. 전에 보신 순번과 다를 겁니다."),(None,"갖고 있던 기록은 그대로 남아 있다. 하지만 지금 내려진 명령은 다시 확인해야 한다.")],"week2:convoy_changed")
        $ r13_event("convoy_changed_notice")
    if room13["day"]>=r13_tl(11) and "day11_warning" not in room13["events"]:
        call r13_scene("winter_square","광장 · 꺼진 집들","night")
        call r13_lines([("resident_ppul","불이 들어오지 않는 집은 학교로 모이십시오. 보호시설 환자들은 별도로 옮깁니다."),("resident_bori","왜 보호시설에 계신 분들은 학교로 안 와요?"),("resident_ppul","함께 있으면 서로 다칠 수 있기 때문이오."),(None,"옮길 사람 명단에 붉은 줄이 그어졌다. 치료하러 옮긴다기에는 준비해 둔 장비가 맞지 않았다.")],"week2:day11_warning")
        if room13["daram_state"]=="held":
            call r13_lines([("neoul","아이 이름도 따로 옮길 사람 명단에 올라 있습니다. 명령이 바뀌기 전에 확인할 일이 있으면 지금 하십시오.")],"week2:day11_child")
        $ r13_event("day11_warning")
    # 0.18.83: 13일의 수레는 에피소드 ⑥(systems/room13_ep6_cart.rpy)이 맡는다. 예전 경고 장면 대신 그 아침 장면을 부른다.
    if room13["day"]>=13 and not r13_has("cv_morning"):
        call r13_cv_morning
    return

label r13_special_activity(key):
    if key in R13_GIMMICK_LABELS:
        call expression R13_GIMMICK_LABELS[key]
        return _return
    if key=="map":
        call r13_compare_first_plan
        return _return
    if key=="interview":
        call r13_case_interview
        return _return
    if key=="w2_meet":
        call r13_reunion
        return True
    if key=="w2_measure2":
        call r13_lines(ROOM13["activities"][key]["lines"],"activity:"+key)
        menu:
            "어느 구간을 함께 남길까?"
            "남은 힘·쓰는 양·버티는 시간을 함께 적는다":
                call r13_lines([("resident_seori","쓰는 힘이 모은 힘보다 적은 동안만 버팁니다. 손실량과 멈춘 시점도 적겠습니다."),("mom","장치를 늘린다고 새 힘이 생기는 건 아니에요. 공급할 곳을 줄여서 장작과 식량을 마련할 시간을 버는 거예요.")],"observation:complete:v3")
                return True
            "잘 나온 숫자 하나만 기록한다":
                call r13_lines([("resident_seori","그 숫자만 떼어 놓으면 반대쪽 주장에도 쓰일 수 있습니다. 앞뒤 기록을 함께 보십시오.")],"observation:incomplete")
                return False
            "판단을 미루고 돌아간다":
                return False
    if key.startswith("w2_rescue_"):
        call r13_rescue(key.replace("w2_rescue_",""))
        return _return
    if key=="w2_escape":
        if r13_has("pursuit_active") and not r13_has("pursuit_managed"):
            call r13_lines([("karo","뒤에서 누가 등불을 들고 우리를 따라오고 있어요. 이대로 가면 돌아갈 길까지 알려 주는 셈이에요."),("dad","그럼 출발 지점을 바꿔서 나가죠.")],"escape:pursuit")
            return False
        menu:
            "이 길을 건너면 이번 여정은 끝난다."
            "가족과 떠난다":
                $ r13_ending_id="E2" if r13_has("mom_reunited") else "E0"
                jump r13_ending
            "남아서 더 알아본다":
                return False
    return False

label r13_reunion:
    call r13_scene("r13_greenhouse","폐온실 지하 · 합류","quiet")
    if r13_has("mother_intervened"):
        call r13_lines([("dad","진료실에서 헤어진 뒤로는 안전했어?"),("mom","뒤따라온 사람 때문에 숨을 자리를 한 번 옮겼어. 여기 신호는 초롱하고 새로 정했고."),("dad","이번엔 셋이 같이 나갈 방법을 찾자.")],"reunion:after_intervention:v3")
    if room13["daram_state"]=="held":
        call r13_lines([("mom","다람이는 어디 있어?"),("dad","아직 보호시설 안에 있어."),("mom","만나 봤어? 직접 봤어?")],"reunion:held:question")
        if r13_has("E06"):
            call r13_lines([("dad","응. 하지만 네가 올 거라고는 말하지 않았어."),("mom","잘했어. 우선 아이를 데리고 나올 길부터 찾자.")],"reunion:held:visited")
        else:
            call r13_lines([("dad","잡혀갈 때 본 게 마지막이야. 아직 만나서 제대로 얘기를 듣지는 못했어."),("mom","그럼 명단만 믿지 말자. 아이가 지금 어디에 있는지부터 직접 확인해야 해.")],"reunion:held:unvisited")
    else:
        call r13_cinematic("reunion")
        call r13_lines([("daram","……엄마?"),(None,"엄마가 손을 뻗다 말고 아이 눈높이에 맞춰 앉았다. 그러자 다람이가 품으로 달려들었다."),("mom","손 좀 보자. 어디 다쳤어?")],"reunion:free")
        if room13["case_state"]=="prevented":
            call r13_lines([("daram","안 다쳤어. 계속 아빠랑 같이 있었어."),("mom","그래. 잘했어.")],"reunion:prevented")
        else:
            call r13_lines([("daram","이제 하나도 안 아파."),("mom","그래도 손 보여 줘.")],"reunion:injured")
    call r13_lines([("dad","네 편지를 받고 왔어. 13호실에서 기다린다고 했잖아."),(None,"가지고 온 편지를 펼쳤다. 아내는 한 줄을 읽더니 고개를 저었다."),("mom","이건 내가 쓴 게 아니야. 다람이 이름 옆에 도토리도 없잖아."),("mom","나는 할머니에게 다시는 돌아오지 않겠다고 말했어. 너희한테는 오지 말라고 따로 썼고."),("dad","그 편지는 오지 않았어. 이 편지만 왔지."),("mom","내 이름으로 부르면 너희가 올 거고, 그럼 나도 돌아올 수밖에 없으니까. 나한테 직접 오라고 하면 거절할 걸 알았겠지.")],"reunion:lure")
    if room13.get("life_poc"):
        call r13_lines([("dad","방에 남긴 메모에는 우리가 오면 짐을 놓아두라고 했잖아."),("mom","가족에게 연락하겠다는 말은 들었어. 혹시 네가 다람이와 오면 초롱에게 내 소식을 묻게 하려고 남겼지. 내가 어디로 가는지는 쓰지 않았어.")],"reunion:family_note:learning")
    $ r13_flag("mom_reunited")
    $ r13_edit(mom_state="reunited")
    call r13_lines([("mom","연구 원본은 여기 있어. 하지만 내가 적은 것만으로는 사람들이 안 믿을 거야. 장치가 버텼다는 옛 기록과 지금 지켜본 결과도 필요해."),("dad","그렇다고 또 혼자서 나서지는 마."),("mom","혼자는 안 할게. 그렇다고 기다리고만 있지도 않을 거고.")],"reunion:research")
    $ r13_grant(["E30"],"엄마가 보관한 연구 원본 직접 확인")
    return

label r13_rescue(route, at_altar=False):
    if room13["daram_state"]!="held":
        return False
    if route not in r13_rescue_routes():
        call r13_lines([("dad","전에 확인한 교대 순서와 지금 경비들 움직임이 다르다. 그러니 지금 기록을 다시 확인해야 한다.")],"rescue:stale")
        return False
    if at_altar:
        if route=="order":
            call r13_lines([("dad","너울 씨. 제가 대조해 본 명령서에는 이 아이 이름이 없었습니다. 지금도 같은 명령입니까?"),("neoul","예. 이 수레를 멈추십시오. 아이는 제가 넘겨받겠습니다."),(None,"너울이 끌고 가라는 명령서의 서명 칸을 경비에게 들이밀었다. 경비가 다른 서류를 뒤지는 사이, 나는 아이를 수레에서 안아 내렸다.")],"rescue:altar:order")
        elif route=="laundry":
            call r13_lines([("resident_nubi","담요 받으러 오면 안쪽 매듭부터 보세요. 제가 수레를 가리겠습니다."),(None,"아이를 넘겨받기로 미리 약속해 둔 사람들이 담요를 내렸다. 누비가 반대편을 붙드는 동안, 나는 아이 손을 묶은 끈을 풀었다."),("mom","여기로 와. 엄마가 잡았어.")],"rescue:altar:laundry")
        else:
            call r13_lines([("buri","점검하는 문은 제가 열어 뒀어요. 끌고 가는 수레 뒤쪽으로 나오세요."),(None,"부리가 확인한 점검문으로 들어가 연결대 앞을 막았다. 수레가 멈춘 틈에 아이를 끌어안았다.")],"rescue:altar:maintenance")
    else:
        call r13_scene("r13_facility","북쪽 보호시설","night")
    if not at_altar and route=="order":
        call r13_lines([("resident_seori","옮길 사람을 적는 칸과 실제로 태운 사람 명단이 다릅니다. 원본 명령대로 하고 있지 않습니다."),("neoul","이 명령에는 오늘 이 아이를 옮기라는 내용이 없습니다."),("dad","그럼 이 문을 열어 주십시오."),("neoul","나가는 데까지는 제가 함께 가겠습니다. 그 뒤는 약속드릴 수 없습니다.")],"rescue:order")
    elif not at_altar and route=="laundry":
        call r13_lines([("resident_nubi","수레는 여기에 두겠습니다. 안에서 오래 기다리면 들켜요."),(None,"오늘 확인한 교대 시간에 맞춰, 지키는 사람이 없는 문으로 들어갔다. 누비는 다음 운반자가 올 때까지 그 자리를 지켰다."),("dad","다람아. 아빠야. 같이 나가자.")],"rescue:laundry")
    elif not at_altar:
        call r13_lines([("buri","점검문은 확인했어요. 제가 잡고 있을 테니 아이부터 데려와 주세요."),(None,"지금 자물쇠가 어느 쪽으로 걸렸는지, 걸쇠는 어떤지 먼저 확인했다. 그런 뒤 점검문을 열었다. 도면에만 있던 길을 믿고 무작정 뛰어들지는 않았다.")],"rescue:maintenance")
    call r13_lines([("daram","이번엔 같이 가는 거지?"),("dad","응. 여기서부터는 같이 가.")],"rescue:child")
    if at_altar:
        call r13_lines([("mom","여기 있어. 둘 다 손 줘."),(None,"다람이가 양손으로 엄마와 나를 하나씩 붙잡았다.")],"rescue:mother_here")
    elif r13_has("mom_reunited"):
        call r13_lines([("daram","엄마도 같이 와?"),("dad","엄마 만나러 가자.")],"rescue:mother_waits")
    else:
        call r13_lines([("daram","엄마는 어디 있어?"),("dad","엄마는 아직 찾고 있어. 엄마가 네가 어디 있는지도 모른 채 찾게 하지는 않을게.")],"rescue:mother_unknown")
    $ r13_edit(daram_state="rescued",location="altar" if at_altar else "inn")
    $ r13_flag("daram_rescued")
    return True

label r13_finale:
    $ r13_upgrade()
    $ r13_edit(day=14,period=0,location="altar",finale_started=True)
    show screen r13_hud
    call r13_scene("r13_altar","북쪽 산길 끝 · 숲속 제단","hearing")
    call r13_lines([(None,"광장의 불빛이 발아래로 멀어졌다. 산길은 수레가 다닐 만큼 넓게 다져져 있었다. 그 끝, 소나무 사이로 연결 장치가 드러났다. 산 아래로 내려가는 관을 따라 사람들이 모여 있었다.")],"finale:mountain_approach")
    call r13_lines([(None,"솟은 돌 주변에서 묶인 환자들과 담요를 든 가족들이 뒤섞였다. 쓰러진 난간을 일으켜 세울 사람도 없었다."),("resident_ppul","지금 연결해야 합니다. 이러다 대피소 쪽도 버티지 못하오!"),("resident_bori","우리 식구가 아직 저 안에 있어요! 먼저 나오게 해 주세요!")],"finale:arrival")
    if room13["granny_state"]=="detained":
        call r13_lines([(None,"할머니는 너울에게 감시받고 있었다. 장치에 손이 닿을 거리는 아니었다."),("resident_ppul","할머니는 장치 다루는 법을 들으려고 데려온 겁니다. 결정은 내가 합니다."),("dad","그 결정의 책임도 직접 지십시오.")],"finale:granny_detained")
    else:
        call r13_lines([("granny","다들 가까이 오지 마요. 지금 끈을 풀면 또 다칠 수 있어요."),(None,"어제 밥그릇을 건네던 때와 똑같은 말투였다. 할머니는 결박 끈의 매듭을 다시 확인했다.")],"finale:granny_free")
    if not r13_has("mom_reunited"):
        call r13_lines([(None,"장치 뒤에서 누군가 연결 손잡이를 붙들었다."),("mom","사람 쪽을 먼저 연결하지 마세요!"),("dad","……너, 여기 있었어?"),("mom","끌려가는 사람들을 따라왔어. 지금은 이 손잡이부터 잡아 줘."),(None,"엄마는 스스로 여기까지 왔다. 하지만 연구 원본이나 주민의 동의까지 손에 쥐여 주지는 못했다.")],"finale:mother_arrives")
        $ r13_flag("mom_reunited","mother_late_arrival")
        $ r13_edit(mom_state="reunited")
    if room13["daram_state"]=="held":
        call r13_lines([("daram","아빠!"),("mom","말만 하다가 아이를 저기 그대로 두지는 말자.")],"finale:child_on_convoy")
        call r13_final_rescue
        if not _return:
            $ r13_edit(daram_state="lost")
            $ r13_ending_id="E1"
            jump r13_ending
    else:
        call r13_lines([("daram","저 아저씨도 이름 있어. 아까 나랑 이야기했어."),("mom","알아. 그래서 엄마가 멈추러 온 거야.")],"finale:child_with_family")
    # 제단 앞: 그림책, 손자국, 할머니의 고백, 촌장과 작은 손자국 (systems/room13_ep6_cart.rpy).
    call r13_cv_altar
    call r13_cinematic("mountain")
label r13_final_hub:
    window hide
    hide r13_visitor
    call screen r13_crisis
    $ r13_choice=_return
    if r13_choice in ("F1","F2","F3","F4"):
        call r13_crisis_argument(r13_choice)
    elif r13_choice=="case":
        menu:
            "13호 사건에서 아직 따질 문제"
            "첫 방어와 사망 원인을 구분한다" if r13_debate_open("C2") and "C2" in r13_case_available():
                call r13_argument("C2")
            "할머니의 실제 목격 구간을 확인한다" if r13_debate_open("C3") and "C3" in r13_case_available():
                call r13_argument("C3")
            "손대고 숨긴 일의 마지막 모순을 짚는다" if r13_debate_open("C4") and "C4" in r13_case_available():
                call r13_argument("C4")
                if "C4" in room13["propositions"]:
                    $ r13_edit(granny_state="detained")
            "지금의 제단 문제로 돌아간다":
                pass
    elif r13_choice=="escape":
        if r13_has("pursuit_active") and not r13_has("pursuit_managed"):
            call r13_lines([("karo","뒤를 밟는 사람을 떼어 내지 못했어요. 이대로 나가면 약속한 안전한 길이 아니게 돼요.")],"finale:escape_blocked")
        else:
            call screen r13_confirm("가족과 낮은 고갯길을 건넙니다. 여기 남은 주민들의 문제는 해결되지 않을 수 있습니다.","함께 떠난다","남는다")
            if _return:
                $ r13_ending_id="E2"
                jump r13_ending
    elif r13_choice=="finish":
        call screen r13_confirm("지금 모은 증거와 실제로 해 둔 준비로 움직입니다. 준비하지 않은 식량이나 도움은 없는 것으로 칩니다.","사람들과 움직인다","더 이야기한다")
        if _return:
            $ r13_ending_id=r13_resolve_ending()
            jump r13_ending
    jump r13_final_hub

label r13_final_rescue:
    menu:
        "아이에게 먼저 닿아야 한다."
        "너울에게 명령의 모순을 보여 준다" if "order" in r13_rescue_routes():
            call r13_rescue("order",at_altar=True)
            return _return
        "누비와 미리 짠 넘겨받기로 아이를 빼낸다" if "laundry" in r13_rescue_routes():
            call r13_rescue("laundry",at_altar=True)
            return _return
        "부리와 확인한 점검문으로 연결을 막는다" if "maintenance" in r13_rescue_routes():
            call r13_rescue("maintenance",at_altar=True)
            return _return
        "나르는 사람들과 엄마에게 관을 끊게 한다" if r13_has("operators_ready") and r13_has("patient_transport"):
            call r13_lines([("mom","난방을 끊는 게 아니야. 사람에게 가는 이 관만 잡아 줘."),("buri","보리, 이쪽을 받쳐요!"),(None,"엄마와 장치를 다루는 사람들이 관을 떼어 냈다. 그사이 보리가 아이를 수레에서 내렸다."),("daram","아빠, 놓지 마."),("dad","아빠가 꼭 잡고 있어.")],"finale:emergency_rescue")
            $ r13_edit(daram_state="rescued")
            return True
        "확인해 둔 준비를 다시 살핀다":
            call screen r13_rescue_notes
            jump r13_final_rescue
        "혼자서라도 몸으로 끌려가는 걸 막는다":
            call r13_lines([(None,"엄마가 연결을 늦추는 동안 수레를 붙들었다. 경비는 바깥 명령만 되풀이했다. 문을 열 사람도, 다른 명령을 확인해 줄 사람도 구하지 못했다."),("dad","다람아!"),(None,"그때 눈발 사이로 다음 수레가 들어왔다. 붙잡고 있던 끈이 손에서 빠져나갔다.")],"finale:last_rescue_failed")
            return False

label r13_crisis_argument(claim):
    $ r13_meeting_claim=claim
    $ r13_meeting_active=True
    $ r13_meeting_focus_change(claim,r13_debate_statements(claim)[0]["who"])
    $ r13_claim=claim
    if claim=="F1":
        call r13_lines([("resident_ppul","저분들은 가족도 알아보지 못합니다. 회복할 수 없는 분들로 판단됐소."),("dad","그 판단부터 다시 확인해야 합니다.")],"final:F1:start")
    elif claim=="F2":
        call r13_lines([("resident_ppul","지난번에는 불이 돌아왔습니다. 그건 다들 직접 봤잖소."),("mom","힘이 올라간 건 사실이에요. 그다음에 더 떨어진 것도 보세요.")],"final:F2:start")
        if r13_has("research_disclosed"):
            call r13_lines([("resident_ppul","이미 보여 주신 연구 아니오. 본인이 맞다고 쓴 기록 말고 다른 사람이 확인한 것도 있습니까?")],"final:F2:prepared")
    elif claim=="F3":
        call r13_lines([("resident_ppul","그럼 오늘 밤은 어디서 잡니까? 불 끄고 서로 껴안으면 삽니까?"),("nabi","먹을 것도 같이 답해야 해요. 없는 걸 있다고 할 수는 없잖아요.")],"final:F3:start")
    else:
        call r13_lines([("dad","우리를 부른 편지부터 확인하겠습니다."),("granny","내가 부인을 찾게 해 줬잖아요."),("dad","아내는 이미 할머니에게서 도망친 뒤였습니다.")],"final:F4:start")
label r13_crisis_argument_menu:
    call r13_debate_run(r13_claim) from r13_crisis_debate_return
    $ r13_meeting_active=False
    return _return

# 0.16.2 이전 저장의 복귀 지점을 위해 남겨 둔다. 새 흐름은 쓰지 않는다.
label r13_final_reason(claim):
    if claim=="F1":
        menu:
            "회복 관찰과 삭제 전 기록이 뜻하는 것은?"
            "모두 낫진 않지만, 못 돌아온다는 건 틀렸다":
                call r13_lines([("resident_seori","일시적으로라도 나아졌다는 사실을 지워서는 안 됐습니다."),(None,"보리가 환자를 누르던 손을 풀고 담요를 덮었다. 장치 연결은 아직 멈추지 않았다.")],"final:F1:proved")
                return True
            "다시 나빠졌으니 나아진 기록도 뺀다":
                call r13_lines([("resident_seori","다시 나빠진 것도 적어야 합니다. 하지만 그 전의 반응을 없애면 회복한 적이 없다는 결론을 만들게 됩니다.")],"final:F1:wrong")
    elif claim=="F2":
        menu:
            "옛 기록과 두 번 지켜본 결과를 어떻게 이을까?"
            "희생 효과는 점점 짧았다. 힘을 모아 지킨다":
                call r13_lines([("buri","힘을 뽑아낼수록 버틴 기간이 줄었어요. 할아버지가 남긴 운전 기록에도 그렇게 적혀 있어요."),("resident_seori","힘을 다르게 쓸 때도 남은 힘이 옮겨 가는 걸 확인했습니다. 새로 힘을 채우는 건 아니지만, 사람을 잇지 않고 버틸 방법은 있습니다."),("resident_ppul","그것도 결국 다 쓰면 끝이잖소!"),("mom","맞아요. 그러니까 필요한 곳에 모여서, 그동안 장작과 식량을 마련해야 해요. 다음에 바칠 사람을 정할 날을 기다리는 대신에요."),(None,"작업자가 손을 멈췄다. 환자 쪽 관이 내려왔다. 대피소를 맡은 사람들이 실제로 얼마나 버틸 수 있을지 따져 보기 시작했다.")],"final:F2:proved:v3")
                return True
            "희생 직후 힘이 올랐으니 성공한 방법이다":
                call r13_lines([("mom","그 뒤에 힘이 떨어진 걸 별개의 사고로 떼어 보려면 근거가 있어야 해. 옛 기록도 같은 순서잖아."),("resident_seori","한 번 올랐다는 것과 계속 버틸 수 있다는 주장은 다릅니다. 다음 관측까지 함께 보겠습니다.")],"final:F2:wrong")
    elif claim=="F3":
        menu:
            "오늘 밤을 버틸 방법은?"
            "학교에 모여 식량을 나누고 일을 교대한다":
                call r13_lines([("nabi","학교로 솥 옮겼어요. 오실 분들은 먼저 안으로 들어오세요."),("resident_bori","장작을 집집마다 나누면 모자라요. 한곳에 모여 있어야 해요."),("buri","이쪽은 내가 잡을게요. 다음 교대도 정했어요.")],"final:F3:proved")
                return True
            "집마다 똑같이 나누고 각자 난방한다":
                call r13_lines([("resident_bori","집집마다 불을 살리면 장작이 모자라요. 빈 방까지 덥힐 몫은 없다고요."),("nabi","나누는 양이 같다고 오늘 밤을 버틸 조건까지 같은 건 아니에요.")],"final:F3:wrong")
    else:
        menu:
            "편지와 경고, 분리 지시를 연결하면?"
            "가족을 불러 아이를 떼어 통제하려 했다":
                call r13_lines([("dad","아내가 돌아오기를 거절한 뒤에, 아내 이름으로 이 편지를 써서 보내셨습니다. 가족을 떼어 놓을 지시도 미리 준비해 두셨고요."),("granny","그 여자가 돌아왔으면 아이는 다치지 않아도 됐어요."),("mom","할머니를 만나러 돌아갈 수는 없었어요. 가족에게 돌아갈 방법을 찾고 있었으니까요."),("dad","대답하지 않으셔도 기록은 남습니다."),("neoul","이제부터 그 지시는 따르지 않겠습니다. 자료부터 챙깁시다.")],"final:F4:proved")
                return True
            "분리 지시는 아이를 지키려던 것이었다":
                call r13_lines([("resident_seori","보낸 원본의 날짜는 사건 이전입니다. 지키려 했다는 설명은 그 지시를 내린 시점과 함께 대조해 봐야 합니다.")],"final:F4:wrong")
    return False

label r13_ending:
    $ r13_finish_ending(r13_ending_id)
    if r13_ending_id in ("E0","E2"):
        call r13_scene("winter","낮은 고갯길","quiet")
        if r13_ending_id=="E0":
            call r13_lines([("daram","엄마한테 우리가 이 마을에 왔다 갔다고 전해질까?"),("dad","엄마한테 연락은 남겨 뒀어."),("daram","그럼 못 찾은 건 아니라고 적어 줘. 아직 못 만난 거라고.")],"ending:E0")
        else:
            call r13_lines([("daram","뒤에 마을 불이 꺼졌어."),("mom","지금은 앞만 보자. 발 디딜 곳이 좁아."),("dad","아빠 손 놓지 마."),(None,"세 사람은 함께 고개를 넘었다. 가족은 돌아왔지만, 마을에서 끊긴 이름들은 아직 그대로 남아 있었다.")],"ending:E2")
    elif r13_ending_id=="E1":
        call r13_scene("r13_facility","아무도 없는 만남의 방","quiet")
        call r13_lines([("dad","어디로 옮겼습니까?"),("guard","여기 남은 기록은 거기까지입니다."),(None,"돌려받은 장갑은 한 짝뿐이었다. 수첩에는 마지막으로 확인한, 끌고 간 시각과 바뀐 경비 순서가 남아 있었다.")],"ending:E1")
    elif r13_ending_id=="E3":
        call r13_scene("r13_altar","산 아래 다시 켜진 마을","quiet")
        call r13_lines([(None,"불이 돌아오자 사람들이 안도의 숨을 내쉬었다. 그 뒤편에서 누군가 한 사람 몫의 그릇을 치웠다."),("resident_eunho","오늘은 따뜻하겠구려."),(None,"며칠 뒤 힘을 재는 바늘이 다시 흔들렸다. 이번에 장치에 이어 붙인 사람의 이름은 돌아오지 않았다.")],"ending:E3")
    elif r13_ending_id=="E4":
        call r13_scene("r13_school","학교 대피소","quiet")
        call r13_lines([("nabi","이쪽 방은 닫아야 해요. 다들 한 곳으로 모여요."),("buri","고칠 수 있는 건 내일 다시 볼게요."),("mom","이름부터 적어요. 누구를 어디로 옮겼는지 남겨야 해요."),(None,"억지로 힘을 뽑아내는 일은 멈췄다. 그래도 모두가 안전하게 지낼 조건을 끝내 갖추지는 못했다.")],"ending:E4")
        if not r13_has("supplies_ready"):
            call r13_lines([(None,"가장 먼저 식량이 모자랐다. 창고에서 실제로 꺼내 오지 못한 곡물은 수첩에만 적혀 있었다. 그 곡물로는 아무의 배도 채우지 못했다.")],"ending:E4:no_food")
        if not r13_has("patient_transport"):
            call r13_lines([(None,"스스로 걷지 못하는 사람을 옮길 손이 부족했다. 낮은 길이 열린 뒤에도 빈 집들을 다시 돌아야 했다.")],"ending:E4:no_transport")
    else:
        if room13["granny_state"]!="detained":
            $ r13_edit(granny_state="removed_from_authority")
        call r13_scene("front","여관 접수대 · 그 뒤","travel")
        call r13_lines([(None,"할머니의 자리는 비어 있었다. 나비가 장부를 펼쳤고 주민들이 제 몫을 적었다. 불은 일부만 켜져 있었다."),("daram","여기에도 내 이름 적어?"),("nabi","오늘 밥 먹을 사람 이름. 안 적으면 또 모자라."),("daram","엄마 이름도 적을게."),("mom","내 이름은 내가 쓸까?"),("daram","응. 이번엔 직접 써.")],"ending:E5:meal")
        if room13["victim_state"]=="dead":
            call r13_lines([(None,"부리는 어르신의 수첩을 덮었다. 아무도 그 빈 의자를 다른 사람의 자리라고 하지 않았다."),("buri","그날 기록은 돌려받을게요. 함께 보관할 사본은 남겨 두고요.")],"ending:elder_dead")
        else:
            call r13_lines([("resident_owlgp","옛 조사에서 내가 놓친 것도 적겠소. 살아 있다고 해서 잘못까지 없어지는 건 아니오.")],"ending:elder_survived")
        call r13_lines([("dad","길이 열리면 집으로 돌아가자."),("daram","길 열리기 전에는?"),("mom","아직 할 일이 조금 남았어."),("daram","조금이면 나도 같이 해도 되지?")],"ending:family")
        if r13_ending_id=="E6":
            call r13_scene("room","열세 번째 창","travel")
            call r13_lines(([("mom","초롱 씨가 남긴 짐에 이 도면이 있었어. 마을 밖으로 보낸 적이 있대. 원본은 여기 남겼고.")] if r13_has("chorong_dead") else [("resident_lamplighter","이 도면은 마을 밖으로 보낸 적이 있습니다. 원본은 여기 남겼고요.")])+[("mom","이 부분이 달라. 고대 장치에 있던 선이 아니야."),("dad","그 선은 나중에 덧붙였다는 거야?"),("mom","누군가 같은 방법으로 다른 곳도 바꿨을 수 있어."),(None,"자료를 여러 부 복사해 나눠 보관했다. 이 마을에서 벌어진 일의 책임은 지워지지 않았다."),("daram","이제 천 걷어도 돼?"),("mom","응."),(None,"다람이가 창에 친 두꺼운 천을 걷었다. 이번에는 누군가를 숨기려는 게 아니었다.")],"ending:E6")
            $ r13_grant(["E32"],"초롱이 간직한, 마을 밖으로 간 장치 도면")
    hide screen r13_hud
    hide r13_visitor
    window hide
    call r13_cinematic(r13_ending_id, leave=True)
    $ renpy.force_autosave()
    # 0.18.99: the winter's name board comes first (systems/room13_polish3.rpy).
    call screen r13_winter_board(r13_ending_id)
    if _return=="restart":
        $ renpy.full_restart(label="room13_start")
    while True:
        call screen r13_ending_screen(r13_ending_id)
        if _return=="replay":
            call r13_cinematic(r13_ending_id,leave=True)
        elif _return=="restart":
            $ renpy.full_restart(label="room13_start")
        elif _return=="board":
            call screen r13_winter_board(r13_ending_id)
            if _return=="restart":
                $ renpy.full_restart(label="room13_start")
        else:
            return
