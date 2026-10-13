# Days 8–14: rescue, reunion, disaster response, confrontation and completed endings.
label r13_week2_opening:
    $ r13_upgrade()
    if room13["week2_started"]:
        jump r13_week2_day
    $ r13_edit(day=8,period=0,location="inn",week2_started=True)
    show screen r13_hud
    call r13_scene("front","월요일 아침 · 꺼져 가는 난방","night")
    if room13["granny_state"]=="detained":
        call r13_lines([(None,"접수대가 비어 있었다. 나비가 열쇠를 들고 손님 수를 세었다."),("nabi","할머니는 아직 경비실에 계세요. 이 문은 제가 잠글게요.")],"week2:granny_held")
    else:
        call r13_lines([(None,"아래층 난방관에서 소리가 멎었다. 할머니가 불 꺼진 방의 열쇠를 따로 모았다.")],"week2:granny_free")
    if room13["daram_state"]=="held":
        call r13_lines([("neoul","보호시설 난방도 약해졌습니다. 환자를 다른 곳으로 옮긴다는 말이 나옵니다."),("dad","다람이도 포함됩니까?"),("neoul","현행 명단을 확인해야 합니다. 이전 재판 기록만으로 지금 호송 대상을 알 수는 없습니다."),(None,"판결이 끝나도 아이에게 닿는 길은 끝나지 않았다. 이동하는 명단부터 찾아야 한다.")],"week2:rescue_route")
    else:
        call r13_lines([("daram","아빠. 저 사람, 어제도 저기서 일했잖아."),(None,"배관을 고치던 주민이 자기 이름을 잊었다. 길 건너에서는 빈 식량 자루를 두고 언성이 높아졌다."),("dad","여기서 같이 보자."),("daram","물 가져올까? 물어보고 줄게.")],"week2:family_route")
    call r13_lines([("resident_lamplighter","등이 먼저 어두워진 게 아니에요. 며칠 전부터 바늘이 흔들렸어요."),(None,"재판에서 누구 편을 들었든 눈과 추위는 마을 전체를 덮고 있었다. 학교에서는 교실을 비우고, 진료소는 복도까지 자리를 폈다.")],"week2:crisis")
    if r13_has("warning_exposed"):
        $ r13_flag("pursuit_active")
        call r13_lines([("resident_lamplighter","여관에서 편지 이야기가 나왔습니다. 누가 다음 편지를 가져오는지 확인하러 다녀요.")],"week2:prior_disclosure")
    jump r13_roam

label r13_week2_day:
    $ r13_upgrade()
    if not room13["week2_started"]:
        jump r13_week2_opening
    if room13["day"]>=14:
        jump r13_finale
    jump r13_roam

label r13_week2_events:
    if room13.get("reply_due") is not None and r13_abs_time()>=room13["reply_due"] and not r13_has("E19"):
        call r13_scene("winter_square","광장 · 등 밑의 답장","search")
        call r13_lines([("resident_lamplighter","답이 왔습니다. 예전 은신처가 아니라 현재 신호를 확인하라는군요."),(None,"「폐온실 아래 등 표식을 봐 줘. 주소를 다른 사람에게 말하지 마. 뒤따르는 사람이 있으면 들어오지 말고.」")],"week2:reply")
        $ r13_grant(["E19"],"초롱이 직접 가져온 현재 답장")
        $ r13_edit(mom_state="contacted")
    if r13_has("contact_compromised") and "contact_relocated" not in room13["events"]:
        call r13_lines([("resident_lamplighter","약속 장소에 경비가 먼저 왔어요. 어머니는 자리를 바꿨습니다. 새 표식을 확인해야 해요."),("dad","살아 있다는 거죠?"),("resident_lamplighter","제가 직접 받은 신호는 그렇습니다. 그다음 것을 확인합시다.")],"week2:relocated")
        $ r13_event("contact_relocated")
    if r13_has("convoy_changed") and "convoy_changed_notice" not in room13["events"]:
        call r13_lines([("neoul","호송 조가 바뀌었습니다. 이전에 보신 교대와 다를 겁니다."),(None,"가지고 있는 기록은 남아 있다. 하지만 지금 시행되는 명령을 다시 확인해야 한다.")],"week2:convoy_changed")
        $ r13_event("convoy_changed_notice")
    if room13["day"]>=11 and "day11_warning" not in room13["events"]:
        call r13_scene("winter_square","광장 · 꺼진 집들","night")
        call r13_lines([("resident_ppul","불이 들어오지 않는 집은 학교로 모이십시오. 보호시설 환자들은 별도로 옮깁니다."),("resident_bori","왜 거기 계신 분들은 학교로 안 와요?"),("resident_ppul","서로 다칠 수 있으니까요."),(None,"이송 명부에 붉은 줄이 그어졌다. 치료를 위한 이동이라기에는 준비된 장비가 달랐다.")],"week2:day11_warning")
        if room13["daram_state"]=="held":
            call r13_lines([("neoul","아이 이름도 별도 대상에 올라 있습니다. 명령이 바뀌기 전에 확인할 일이 있으면 지금 하십시오.")],"week2:day11_child")
        $ r13_event("day11_warning")
    if room13["day"]>=13 and "day13_warning" not in room13["events"]:
        call r13_scene("winter_square","광장 · 호송 수레","night")
        call r13_lines([(None,"담요만 실어야 할 수레에 결박 끈이 함께 올라갔다. 저녁 작업을 마친 사람들이 광장 북쪽의 산길 입구에 모였다."),("neoul","내일 동이 트면 산 위 제단으로 옮긴답니다. 연결 전에 멈출 근거와 사람을 확보해야 합니다.")],"week2:day13_warning:mountain")
        if room13["daram_state"] in ("with_dad","rescued"):
            if room13["case_state"]=="prevented":
                call r13_lines([("daram","저 아저씨한테 물 가져다줘도 돼? 급하게 주면 쏟으니까, 천천히."),("dad","같이 물어보자.")],"week2:daram_prevented")
            else:
                call r13_lines([("daram","내가 물 가져다줘도 돼? 이번엔 안 잡아당겨."),("dad","같이 물어보자."),(None,"다람이는 컵을 내려놓고 상대가 고개를 끄덕일 때까지 기다렸다.")],"week2:daram_recovery")
        $ r13_event("day13_warning")
    return

label r13_special_activity(key):
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
            "보내는 돌과 받는 돌의 잔량, 부하와 유지 시간을 함께 기록한다":
                call r13_lines([("resident_seori","모은 힘보다 쓴 힘이 적은 동안만 버팁니다. 손실과 멈춘 시점도 적겠습니다."),("mom","장치를 늘리면 새 힘이 생기는 게 아니에요. 공급할 곳을 줄이고 장작과 식량을 마련할 시간을 얻는 거예요.")],"observation:complete:v3")
                return True
            "잘 나온 숫자 하나만 기록한다":
                call r13_lines([("resident_seori","그것만 떼어 놓으면 반대 주장에도 쓸 수 있습니다. 전후 기록을 함께 보십시오.")],"observation:incomplete")
                $ r13_tick()
                return False
            "판단을 보류하고 돌아간다":
                $ r13_tick()
                return False
    if key.startswith("w2_rescue_"):
        call r13_rescue(key.replace("w2_rescue_",""))
        return _return
    if key=="w2_escape":
        if r13_has("pursuit_active") and not r13_has("pursuit_managed"):
            call r13_lines([("karo","뒤의 등불이 우리를 따라오고 있어요. 이대로는 돌아갈 길까지 알려 주게 됩니다."),("dad","출발 지점을 바꾼 뒤 나가죠.")],"escape:pursuit")
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
        call r13_lines([("dad","진료실에서 헤어진 뒤로는 안전했어?"),("mom","뒤따라온 사람 때문에 자리를 한 번 옮겼어. 여기 신호는 초롱하고 새로 정했고."),("dad","이번엔 같이 나갈 방법을 찾자.")],"reunion:after_intervention:v3")
    if room13["daram_state"]=="held":
        call r13_lines([("mom","다람이는?"),("dad","아직 안에 있어."),("mom","면회는 했어? 직접 봤어?")],"reunion:held:question")
        if r13_has("E06"):
            call r13_lines([("dad","응. 네가 올 거라고는 말하지 않았어."),("mom","잘했어. 먼저 데리고 나올 길부터 보자.")],"reunion:held:visited")
        else:
            call r13_lines([("dad","잡혀갈 때 보고, 아직 면회에서 제대로 듣지는 못했어."),("mom","그럼 명단만 믿지 말자. 지금 어디에 있는지부터 직접 확인해야 해.")],"reunion:held:unvisited")
    else:
        call r13_cinematic("reunion")
        call r13_lines([("daram","……엄마?"),(None,"엄마가 손을 뻗다가 아이의 눈높이로 앉았다. 다람이가 달려들었다."),("mom","손 좀 보자. 어디 다쳤어?")],"reunion:free")
        if room13["case_state"]=="prevented":
            call r13_lines([("daram","안 다쳤어. 아빠랑 같이 있었어."),("mom","그래. 잘했어.")],"reunion:prevented")
        else:
            call r13_lines([("daram","이제 안 아파."),("mom","그래도 보여 줘.")],"reunion:injured")
    call r13_lines([("dad","편지를 받고 왔어."),("mom","무슨 편지?"),(None,"가지고 온 편지를 펼쳤다."),("mom","나는 그 사람에게 돌아오지 않겠다고 말했어."),("dad","그 말은 편지에 없었네."),("mom","내가 사라졌다고 가족이 찾아오면 따라올 수 있으니까. 나한테 직접 오라고 하면 거절할 걸 알았겠지.")],"reunion:lure")
    $ r13_flag("mom_reunited")
    $ r13_edit(mom_state="reunited")
    call r13_lines([("mom","연구 원본은 여기 있어. 하지만 내가 적은 것만으로는 사람들이 안 믿을 거야. 장치가 버텼다는 옛 기록과 지금의 관측도 필요해."),("dad","그렇다고 네가 혼자 다시 나서지는 마."),("mom","혼자는 안 할게. 기다리고만 있지도 않을 거고.")],"reunion:research")
    $ r13_grant(["E30"],"엄마가 보관한 연구 원본 직접 확인")
    return

label r13_rescue(route, at_altar=False):
    if room13["daram_state"]!="held":
        return False
    if route not in r13_rescue_routes():
        call r13_lines([("dad","이전에 확인한 교대와 지금 움직임이 다르다. 현재 기록을 다시 확인해야겠어.")],"rescue:stale")
        return False
    if at_altar:
        if route=="order":
            call r13_lines([("dad","너울 씨. 대조한 명령에는 이 아이가 없었습니다. 지금도 같은 명령입니까?"),("neoul","예. 이 수레를 멈추십시오. 제가 인계받겠습니다."),(None,"너울이 호송 명령의 서명란을 내밀었다. 경비가 다른 서류를 찾는 사이 아이를 안아 내렸다.")],"rescue:altar:order")
        elif route=="laundry":
            call r13_lines([("resident_nubi","담요 받으러 오면 안쪽 매듭부터 보세요. 제가 수레를 가리겠습니다."),(None,"확인했던 인계조가 담요를 내렸다. 누비가 반대편을 붙드는 동안 아이의 손을 풀었다."),("mom","여기로. 잡았어.")],"rescue:altar:laundry")
        else:
            call r13_lines([("buri","점검문은 열어 뒀어요. 호송 수레 뒤로 나오세요."),(None,"부리가 확인한 문으로 들어가 연결대 앞을 막았다. 수레가 멈춘 틈에 아이를 끌어안았다.")],"rescue:altar:maintenance")
    else:
        call r13_scene("r13_facility","북쪽 보호시설","night")
    if not at_altar and route=="order":
        call r13_lines([("resident_seori","이송 대상을 쓰는 난과 실제 태운 사람의 명단이 다릅니다. 원본대로 시행되지 않고 있어요."),("neoul","이 명령에는 오늘 이 아이를 옮기라는 내용이 없습니다."),("dad","그럼 문을 열어 주십시오."),("neoul","나가는 데까지는 제가 갑니다. 그다음은 제가 약속할 수 없습니다.")],"rescue:order")
    elif not at_altar and route=="laundry":
        call r13_lines([("resident_nubi","수레는 여기에 두겠습니다. 안에서 오래 기다리면 들켜요."),(None,"오늘 확인한 교대에 맞춰 비는 문으로 들어갔다. 누비는 다음 운반자가 올 때까지 그 자리를 지켰다."),("dad","다람아. 아빠야. 같이 나가자.")],"rescue:laundry")
    elif not at_altar:
        call r13_lines([("buri","문은 확인했어요. 제가 잡고 있을 테니 아이부터 데려와 주세요."),(None,"현재 자물쇠의 방향과 걸쇠를 확인하고 점검문을 열었다. 도면에만 있던 길을 믿고 뛰어들지는 않았다.")],"rescue:maintenance")
    call r13_lines([("daram","이번엔 같이 가는 거지?"),("dad","응. 여기서부터 같이.")],"rescue:child")
    if at_altar:
        call r13_lines([("mom","여기 있어. 둘 다 손 줘."),(None,"다람이가 한 손씩 우리를 붙들었다.")],"rescue:mother_here")
    elif r13_has("mom_reunited"):
        call r13_lines([("daram","엄마도 와?"),("dad","만나러 가자.")],"rescue:mother_waits")
    else:
        call r13_lines([("daram","엄마는?"),("dad","아직 찾고 있어. 네가 어디 있는지도 모른 채 찾게 하지는 않을게.")],"rescue:mother_unknown")
    $ r13_edit(daram_state="rescued",location="altar" if at_altar else "inn")
    $ r13_flag("daram_rescued")
    return True

label r13_finale:
    $ r13_upgrade()
    $ r13_edit(day=14,period=0,location="altar",finale_started=True)
    show screen r13_hud
    call r13_scene("r13_altar","북쪽 산길 끝 · 숲속 제단","hearing")
    call r13_lines([(None,"광장의 불빛이 발아래로 멀어졌다. 수레가 다닐 만큼 넓게 다져진 산길 끝, 소나무 사이로 연결 장치가 드러났다. 산 아래로 내려가는 관을 따라 사람들이 모여 있었다.")],"finale:mountain_approach")
    call r13_lines([(None,"솟은 돌 주변에 결박한 환자와 담요를 든 가족들이 뒤섞였다. 쓰러진 난간을 다시 세울 사람도 없었다."),("resident_ppul","지금 연결해야 합니다. 대피소 쪽도 버티지 못해요!"),("resident_bori","우리 식구 아직 저 안에 있어요! 먼저 나오게 해 주세요!")],"finale:arrival")
    if room13["granny_state"]=="detained":
        call r13_lines([(None,"할머니는 너울의 감시 아래 있었다. 장치에 손댈 수 있는 거리는 아니었다."),("resident_ppul","운용 설명을 들으려고 데려온 겁니다. 결정은 내가 합니다."),("dad","그 결정의 책임도 직접 지십시오.")],"finale:granny_detained")
    else:
        call r13_lines([("granny","가까이 오지 마요. 지금 풀면 또 다칠 수 있어."),(None,"어제 밥그릇을 건네던 말투였다. 할머니는 결박 끈의 매듭을 다시 확인했다.")],"finale:granny_free")
    if not r13_has("mom_reunited"):
        call r13_lines([(None,"장치 뒤에서 누군가 연결 손잡이를 붙들었다."),("mom","사람 쪽을 먼저 연결하지 마세요!"),("dad","……여기에 있었어?"),("mom","호송을 따라왔어. 지금은 이 손잡이부터 잡아 줘."),(None,"엄마는 스스로 여기까지 왔다. 연구 원본이나 주민의 동의까지 손에 쥐여 주지는 못했다.")],"finale:mother_arrives")
        $ r13_flag("mom_reunited","mother_late_arrival")
        $ r13_edit(mom_state="reunited")
    if room13["daram_state"]=="held":
        call r13_lines([("daram","아빠!"),("mom","말부터 하느라 아이를 저기에 두지는 말자.")],"finale:child_on_convoy")
        call r13_final_rescue
        if not _return:
            $ r13_edit(daram_state="lost")
            $ r13_ending_id="E1"
            jump r13_ending
    else:
        call r13_lines([("daram","저 아저씨도 이름 있어. 아까 이야기했어."),("mom","알아. 그래서 멈추러 온 거야.")],"finale:child_with_family")
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
            "아직 다투는 13호 사건의 논점"
            "첫 방어와 사망 원인을 구분한다" if "C2" not in room13["propositions"]:
                call r13_argument("C2")
            "할머니의 실제 목격 구간을 확인한다" if "C2" in room13["propositions"] and "C3" not in room13["propositions"]:
                call r13_argument("C3")
            "접촉과 은폐의 마지막 모순을 제시한다" if "C3" in room13["propositions"] and "C4" not in room13["propositions"]:
                call r13_argument("C4")
                if "C4" in room13["propositions"]:
                    $ r13_edit(granny_state="detained")
            "지금의 제단 문제로 돌아간다":
                pass
    elif r13_choice=="escape":
        if r13_has("pursuit_active") and not r13_has("pursuit_managed"):
            call r13_lines([("karo","뒤를 밟는 사람을 떼지 못했어요. 이대로 나가는 건 약속한 안전한 길이 아닙니다.")],"finale:escape_blocked")
        else:
            call screen r13_confirm("가족과 낮은 고갯길을 건넙니다. 여기 남은 주민들의 문제는 해결되지 않을 수 있습니다.","함께 떠난다","남는다")
            if _return:
                $ r13_ending_id="E2"
                jump r13_ending
    elif r13_choice=="finish":
        call screen r13_confirm("지금 확보한 증거와 실제 준비로 행동합니다. 준비하지 않은 식량이나 지원은 있는 것으로 처리되지 않습니다.","사람들과 움직인다","더 이야기한다")
        if _return:
            $ r13_ending_id=r13_resolve_ending()
            jump r13_ending
    jump r13_final_hub

label r13_final_rescue:
    menu:
        "아이에게 먼저 닿아야 한다."
        "너울에게 현행 명령의 모순을 제시한다" if "order" in r13_rescue_routes():
            call r13_rescue("order",at_altar=True)
            return _return
        "누비와 준비한 인계로 아이를 빼낸다" if "laundry" in r13_rescue_routes():
            call r13_rescue("laundry",at_altar=True)
            return _return
        "부리와 확인한 점검문으로 연결을 막는다" if "maintenance" in r13_rescue_routes():
            call r13_rescue("maintenance",at_altar=True)
            return _return
        "운반조와 엄마에게 사람 쪽 연결 차단을 부탁한다" if r13_has("operators_ready") and r13_has("patient_transport"):
            call r13_lines([("mom","난방을 끊는 게 아니야. 사람에게 가는 이 관만 잡아 줘."),("buri","보리, 이쪽을 받쳐요!"),(None,"엄마와 운용조가 관을 분리하는 동안 보리가 아이를 수레에서 내렸다."),("daram","놓지 마."),("dad","잡고 있어.")],"finale:emergency_rescue")
            $ r13_edit(daram_state="rescued")
            return True
        "확인해 둔 준비를 다시 살핀다":
            call screen r13_rescue_notes
            jump r13_final_rescue
        "혼자라도 호송을 몸으로 막는다":
            call r13_lines([(None,"엄마가 연결을 지연시키는 동안 수레를 붙들었다. 경비는 바깥 명령만 반복했다. 문을 열 사람도, 다른 명령을 확인해 줄 사람도 확보하지 못했다."),("dad","다람아!"),(None,"눈발 사이로 다음 수레가 들어왔다. 손에서 잡고 있던 끈이 빠져나갔다.")],"finale:last_rescue_failed")
            return False

label r13_crisis_argument(claim):
    $ r13_claim=claim
    if claim=="F1":
        call r13_lines([("resident_ppul","가족도 알아보지 못합니다. 회복할 수 없는 분들로 판단됐어요."),("dad","그 판단부터 다시 확인해야 합니다.")],"final:F1:start")
    elif claim=="F2":
        call r13_lines([("resident_ppul","지난번에는 불이 돌아왔습니다. 그건 다들 봤잖아요."),("mom","올라간 것도 사실이에요. 그다음에 더 내려간 것도 보세요.")],"final:F2:start")
        if r13_has("research_disclosed"):
            call r13_lines([("resident_ppul","이미 보여 주신 연구죠. 본인이 맞다고 쓴 기록 말고 다른 사람이 확인한 것도 있습니까?")],"final:F2:prepared")
    elif claim=="F3":
        call r13_lines([("resident_ppul","그럼 오늘 밤은 어디서 잡니까? 불 끄고 서로 껴안으면 삽니까?"),("nabi","먹을 것도 같이 답해야 해요. 없는 걸 있다고 할 수는 없잖아요.")],"final:F3:start")
    else:
        call r13_lines([("dad","우리를 부른 편지부터 확인하겠습니다."),("granny","아내를 찾게 해줬잖아요."),("dad","아내는 이미 당신에게서 도망친 뒤였습니다.")],"final:F4:start")
label r13_crisis_argument_menu:
    window hide
    hide r13_visitor
    call screen r13_crisis_proof(r13_claim)
    $ r13_choice=_return
    if r13_choice=="leave":
        return
    if r13_choice=="present":
        call screen r13_book("resident_seori",present=True,hearing=True)
        $ r13_item=_return
        if r13_item:
            $ r13_submit(r13_claim,r13_item)
            show screen r13_material_corner(r13_item)
            call r13_lines([("resident_seori",r13_evidence_feedback(r13_claim,r13_item))],"final:proof:"+r13_claim+":"+r13_item)
            hide screen r13_material_corner
    elif r13_choice=="press":
        call r13_lines([("resident_ppul",R13_PRESS[r13_claim])],"final:press:"+r13_claim)
    elif r13_choice=="argue":
        if not r13_argument_ready(r13_claim):
            call r13_lines([("resident_seori","설명되지 않은 부분이 남았습니다. 지금 낸 자료로 확인할 수 있는 데까지만 말해야 합니다.")],"final:insufficient:"+r13_claim)
            if r13_claim=="F3" and not r13_survival_ready():
                call r13_lines([("nabi","장소, 먹을 것, 옮길 사람, 밤에 남을 사람요. 우리 손에 실제로 있는 것부터 세 봐요.")],"final:F3:logistics_missing")
        else:
            call r13_final_reason(r13_claim)
            if _return:
                $ r13_prove(r13_claim)
                return
    jump r13_crisis_argument_menu

label r13_final_reason(claim):
    if claim=="F1":
        menu:
            "회복 관찰과 삭제 전 기록이 뜻하는 것은?"
            "모두 낫는다는 뜻은 아니다. 누구도 돌아오지 못한다는 판단은 틀렸다":
                call r13_lines([("resident_seori","일시적으로라도 나아졌다는 사실을 지워서는 안 됐습니다."),(None,"보리가 환자를 누르던 손을 풀고 담요를 덮었다. 아직 장치의 연결은 멈추지 않았다.")],"final:F1:proved")
                return True
            "나중에 다시 악화했으니 첫 회복 기록도 판단에서 제외한다":
                call r13_lines([("resident_seori","다시 나빠진 것도 적어야 합니다. 하지만 그 전의 반응을 없애면 회복한 적이 없다는 결론을 만들게 됩니다.")],"final:F1:wrong")
    elif claim=="F2":
        menu:
            "과거 기록과 두 번의 관측을 어떻게 연결할까?"
            "희생의 반등은 짧아졌다. 잔량을 모아 제한된 곳부터 유지할 수 있다":
                call r13_lines([("buri","추출을 반복할수록 버틴 기간이 줄었어요. 어르신이 남긴 운전일에도 그렇게 적혔습니다."),("resident_seori","다른 부하에서도 잔량 이전을 확인했습니다. 새 충전은 아니지만 사람을 연결하지 않고 버틸 방법은 있습니다."),("resident_ppul","그것도 결국 다 쓰잖소!"),("mom","맞아요. 그래서 필요한 곳에 모이고 그동안 장작과 식량을 마련해야 해요. 다음 사람을 바칠 날짜를 기다리는 대신요."),(None,"작업자가 손을 멈췄다. 환자 쪽 관이 내려왔다. 대피소를 맡은 사람들이 실제로 버틸 시간을 따지기 시작했다.")],"final:F2:proved:v3")
                return True
            "희생 직후 출력이 올랐으니, 새 사고가 생기기 전까지는 성공한 방법이었다":
                call r13_lines([("mom","그 뒤 하락을 새 사고라고 나누려면 그 근거가 필요해. 과거 기록도 같은 순서잖아."),("resident_seori","한 번의 상승과 계속 버틸 수 있다는 주장은 다릅니다. 다음 관측까지 함께 보겠습니다.")],"final:F2:wrong")
    elif claim=="F3":
        menu:
            "오늘 밤을 버틸 방법은?"
            "확보한 학교로 모여 실제 식량을 나누고 수동 운용과 운반을 교대한다":
                call r13_lines([("nabi","학교에 솥 옮겼어요. 들어오실 분부터 들어오세요."),("resident_bori","집집마다 나누면 모자라요. 모여 있어야 해요."),("buri","이쪽은 내가 잡을게요. 다음 교대도 정했어요.")],"final:F3:proved")
                return True
            "집마다 같은 양을 나누고 각자 난방을 유지하도록 한다":
                call r13_lines([("resident_bori","집집마다 불을 살리면 장작이 모자라요. 빈 방까지 덥힐 몫은 없다고요."),("nabi","나누는 양만 같다고 오늘 밤을 버티는 조건까지 같은 건 아니에요.")],"final:F3:wrong")
    else:
        menu:
            "편지와 경고, 분리 지시를 연결하면?"
            "엄마를 따라잡으려고 가족을 불렀고, 아이를 떨어뜨려 통제하려 했다":
                call r13_lines([("dad","엄마가 돌아오기를 거절한 뒤 이 편지를 보냈습니다. 가족을 분리하는 지시도 먼저 준비했고요."),("granny","그 여자가 돌아왔으면 아이는 다치지 않아도 됐어."),("mom","당신을 만나러 돌아갈 수는 없었어요. 가족에게 돌아갈 방법을 찾고 있었지."),("dad","답하지 않으셔도 기록은 남습니다."),("neoul","이후 지시는 받지 않겠습니다. 자료부터 확보하죠.")],"final:F4:proved")
                return True
            "아이를 분리하려는 초안은 사건을 안 뒤 만든 보호 조치였다":
                call r13_lines([("resident_seori","발신 원본의 날짜는 사건 전입니다. 보호라는 설명과 그 지시를 내린 시점을 함께 대조해야 합니다.")],"final:F4:wrong")
    return False

label r13_ending:
    $ r13_finish_ending(r13_ending_id)
    if r13_ending_id in ("E0","E2"):
        call r13_scene("winter","낮은 고갯길","quiet")
        if r13_ending_id=="E0":
            call r13_lines([("daram","엄마한테 우리가 왔다 갔다고 전해질까?"),("dad","남긴 연락은 있어."),("daram","그럼 못 찾은 건 아니라고 적어 줘. 아직 못 만난 거라고.")],"ending:E0")
        else:
            call r13_lines([("daram","뒤에 불 꺼졌어."),("mom","지금은 앞을 보자. 발 디딜 곳이 좁아."),("dad","손 놓지 마."),(None,"세 사람은 함께 고개를 넘었다. 가족은 돌아왔다. 마을에서 끊겼던 이름들은 아직 남아 있었다.")],"ending:E2")
    elif r13_ending_id=="E1":
        call r13_scene("r13_facility","빈 면회실","quiet")
        call r13_lines([("dad","어디로 옮겼습니까?"),("guard","여기 기록은 끝났습니다."),(None,"돌려받은 장갑은 한 짝이었다. 마지막으로 확인한 호송 시각과 바뀐 교대가 수첩에 남았다.")],"ending:E1")
    elif r13_ending_id=="E3":
        call r13_scene("r13_altar","산 아래 다시 켜진 마을","quiet")
        call r13_lines([(None,"불이 돌아오자 사람들이 숨을 내쉬었다. 그 뒤에서 누군가 한 사람 몫의 그릇을 치웠다."),("resident_eunho","오늘은 따뜻하겠네요."),(None,"며칠 뒤 출력계가 다시 흔들렸다. 이번에 연결한 사람의 이름은 돌아오지 않았다.")],"ending:E3")
    elif r13_ending_id=="E4":
        call r13_scene("r13_school","학교 대피소","quiet")
        call r13_lines([("nabi","이쪽 방은 닫아야 해요. 한 곳으로 모여요."),("buri","수리할 수 있는 건 내일 다시 볼게요."),("mom","이름부터 적어요. 어디로 옮겼는지 남겨야 해요."),(None,"강제 추출은 멈췄다. 하지만 밝힌 진실만큼의 잠자리와 밥을 모두 준비하지는 못했다.")],"ending:E4")
        if not r13_has("supplies_ready"):
            call r13_lines([(None,"가장 먼저 식량이 모자랐다. 창고에서 실제로 꺼내 오지 못한 곡물은 수첩 안에서 배를 채우지 못했다.")],"ending:E4:no_food")
        if not r13_has("patient_transport"):
            call r13_lines([(None,"스스로 걷지 못하는 사람을 옮길 손이 부족했다. 낮은 길이 열린 뒤에도 빈 집들을 다시 돌아야 했다.")],"ending:E4:no_transport")
    else:
        if room13["granny_state"]!="detained":
            $ r13_edit(granny_state="removed_from_authority")
        call r13_scene("front","여관 접수대 · 그 뒤","travel")
        call r13_lines([(None,"할머니의 자리는 비어 있었다. 나비가 장부를 펼쳤고 주민들이 제 몫을 적었다. 불은 일부만 켜져 있었다."),("daram","여기에도 이름 적어?"),("nabi","오늘 밥 먹을 사람. 안 적으면 또 모자라."),("daram","엄마 것도 적을게."),("mom","내 것은 내가 쓸까?"),("daram","응. 이번엔 직접 써.")],"ending:E5:meal")
        if room13["victim_state"]=="dead":
            call r13_lines([(None,"부리는 어르신의 수첩을 덮었다. 누구도 빈 의자를 다른 사람 자리라고 부르지 않았다."),("buri","그날 기록은 돌려받을게요. 같이 보관할 사본은 남겨 두고요.")],"ending:elder_dead")
        else:
            call r13_lines([("resident_owlgp","옛 조사에서 내가 놓친 것도 적겠소. 살아 있다고 잘못까지 없어지지는 않으니까.")],"ending:elder_survived")
        call r13_lines([("dad","길이 열리면 돌아가자."),("daram","그전에는?"),("mom","할 일이 조금 남았어."),("daram","조금이면 같이 해도 되지?")],"ending:family")
        if r13_ending_id=="E6":
            call r13_scene("room","열세 번째 창","travel")
            call r13_lines([("resident_lamplighter","이 도면은 마을 밖으로 보낸 적이 있습니다. 원본은 여기 남겼고요."),("mom","이 부분이 달라요. 고대 장치에 있던 선이 아니에요."),("dad","나중에 붙였다는 거야?"),("mom","누군가 같은 방법으로 다른 곳도 바꿨을 수 있어요."),(None,"자료를 여러 부 복사해 나눠 보관했다. 이 마을에서 벌어진 일의 책임은 지워지지 않았다."),("daram","이제 열어도 돼?"),("mom","응."),(None,"다람이가 창의 두꺼운 천을 걷었다. 이번에는 누군가를 숨기기 위해서가 아니었다.")],"ending:E6")
            $ r13_grant(["E32"],"초롱이 보관한 외부 반출 개조 도면")
    hide screen r13_hud
    hide r13_visitor
    window hide
    call r13_cinematic(r13_ending_id, leave=True)
    $ renpy.force_autosave()
    call screen r13_ending_screen(r13_ending_id)
    if _return=="restart":
        $ renpy.full_restart(label="room13_start")
    return
