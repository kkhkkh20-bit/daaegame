# One shared disaster, with remembered observations and optional routes into it.
# Core case evidence and the ending remain independent of these optional tasks.
init 48 python:
    def winter_crisis_stage(s):
        return 0 if s["day"]<4 else 1 if s["day"]<8 else 2 if s["day"]<11 else 3

    def winter_exploration_greeting(s,who):
        if who=="nabi" and s["witness"]=="dead":return None
        if who=="nabi" and winter_has(s,"ration_public"):
            return [(who,"표를 고치고 나니 밥 숨겨 먹는다는 소리는 덜 해. 그래도 남은 곡물이 늘어난 건 아니니, 배급은 같이 지켜봐야지.")]
        if who=="nabi" and winter_has(s,"mill_helped"):
            return [(who,"톡이 빻은 걸 또 보냈어. 어제보다 빵을 더 구울 수 있겠네."),("daram","그릇 가져올게요.")]
        if who=="resident_tok" and winter_has(s,"mill_helped"):
            return [(who,"손잡이는 잘 돌아가요. 집마다 남은 곡물을 조금씩 가져오더군요. 전등이 꺼져도 이건 쓸 수 있어요.")]
        if who=="seryeon" and winter_has(s,"ration_public"):
            return [(who,"배급표는 정정했습니다. 하지만 중앙 보관소 우선 배정은 제 마음대로 취소할 수 없습니다."),("dad","그 결정을 한 사람이 누구인지도 확인하겠습니다.")]
        if who=="resident_bori" and winter_crisis_stage(s)>=2:
            return [(who,"집으로 가져갈 장작을 여관 쪽에 모으고 있어요. 혼자 불 때다 꺼뜨리는 것보다 같이 지키는 게 낫겠지요.")]
        if who=="resident_lamplighter" and winter_crisis_stage(s)>=1:
            return [(who,"골목 등을 더 껐어요. 가로등 고장이라고 써 붙였지만, 고칠 부품을 갈아도 켜지지 않습니다."),("daram","집에 불 보내려고요?"),(who,"응. 그런데 이제 집 안 등도 어두워.")]
        if who=="nabi" and winter_crisis_stage(s)>=1:
            return [(who,"오늘도 수프는 있어. 빵은 나눠 먹자. 모자란다고 남의 그릇부터 세면 같이 앉을 자리가 없어져."),("daram","아빠랑 같이 먹을게요.")]
        return None

    def winter_exploration_key(s,who):
        if who not in ("nabi","seryeon","resident_bori","resident_tok","resident_lamplighter"):return ""
        return ":%d:%d:%d"%(winter_crisis_stage(s),winter_has(s,"mill_helped"),winter_has(s,"ration_public"))

    def winter_action_lines(s,key):
        if key=="room_reason" and key in s["done"]:
            return [("daram","옷을 두고 간 이유는 아직 몰라. 그래도 메모를 쓴 곳은 물어볼 수 있겠지?"),("dad","응. 부리와 등을 점검한 사람을 찾아보자.")]
        if key=="ration_compare" and key in s["done"]:
            return [("daram","여섯에서 넷이 먼저 빠지고, 둘만 여관에 온 거야. 번호도 이어져."),("nabi","표만 보고 우리한테 여섯을 내놓으라던 거네.")]
        if key=="ration_share" and key in s["done"]:
            return [("nabi","표를 바로잡는 데 내 인수증을 써도 된다고 했어. 그 약속은 지킬게." if winter_has(s,"ration_public") else "지금은 원본을 잘 갖고 있어 줘. 공개할 마음이 들면 다시 말하고.")]
        if key=="meal":
            return [("nabi","그릇은 넉넉해. 오늘은 수프부터 나누자."),("daram","아빠는 빵 큰 쪽 줄게."),("dad","네 것부터 먹어."),("daram","나 수프도 먹을 건데."),(None,"손님들이 그릇을 돌렸다. 조각난 빵을 더 꺼낼 수 있었다." if winter_has(s,"mill_helped") else "마지막 빵을 얇게 잘랐다. 나비는 자기 접시에도 같은 크기를 놓았다."),("nabi","내일 걱정은 먹고 하자. 식으면 더 맛없어.")]
        if key=="buri_outage" and not winter_has(s,"mother_note"):
            lines=list(WINTER["actions"][key]["lines"])
            lines[-1]=("buri","연구하러 온 분도 그걸 묻더군. 나는 배관만 아는 사람이야.")
            return lines
        return WINTER["actions"][key]["lines"]

    def winter_exploration_observation(s,place,key):
        stage=winter_crisis_stage(s)
        if place=="room" and key=="under":
            if winter_has(s,"mother_note"):return [("daram","봉투는 우리가 챙겼어. 다른 건 없어."),("dad","눌린 글씨는 수첩에 남겨 뒀지?")]
            return [("daram","아빠, 침대 밑에 하얀 모서리 보여. 봉투 같은데?")]
        if place=="room" and key=="boxes":
            return [("daram","옷은 그대로 뒀어. 엄마가 돌아오면 찾을 수 있게.")] if winter_has(s,"mother_linen") else [("daram","빈 줄 알았는데 천 아래 뭐가 있어. 열어 봐도 돼?"),("dad","천천히. 꺼내면 있던 자리에 다시 두자.")]
        if place=="room" and key=="window" and not winter_has(s,"surveillance"):
            return [("daram","저 골목 등 꺼졌다. 방 안 불도 아까보다 어두워."),("dad","아래에서 고장인지 물어보자.")]
        if place=="gate" and key=="booth":
            if winter_has(s,"ration_public"):return [(None,"배급표에 정정 종이가 붙었다. 여관 인수 둘, 중앙 보관소 전용 넷. 배정 총량 여섯 옆에 실제 목적지가 적혔다.")]
            return [(None,"초소 벽에 통행 중단 공고와 곡물 배급표가 나란히 붙었다. 여관 줄에는 여섯 자루라고 적혔다."),("daram","밥은 여기서 나눠 주나? 아래 작은 글씨도 있어.")]
        if place=="square" and key=="pipe" and not winter_has(s,"research"):
            if stage>=2:return [("daram","여기도 눈 쌓이네. 처음엔 따뜻했는데."),("dad","장갑 끼고 있어. 오래 만져도 돌아오지는 않아.")]
            return [("daram","여기는 눈이 녹았어. 저쪽 관은 하얀데."),("dad","관이 갈라지는 곳부터 보자."),("daram","아래로 가는 게 더 따뜻해. 왜 다르게 데워지지?")]
        if place=="inn" and key=="desk":
            return [(None,"열쇠 옆에 식사 인원표가 있다. 방을 얻지 못한 주민 몫까지 그릇 수에 들어 있다."),("daram","자는 사람보다 밥 먹는 사람이 많네. 나비 아주머니한테 물어보자.")]
        if place=="workshop" and key=="wood":
            return [(None,"마른 장작에는 여관으로 옮길 표시가 붙었다. 젖은 묶음은 따로 펼쳐 놓았다." if stage>=2 else "젖은 장작을 띄워 쌓아 말리고 있다. 검은 곰팡이가 핀 묶음은 따로 골라냈다."),("daram","왜 바로 못 때는지 알겠어. 손도 젖네.")]
        if place=="workshop" and key=="meter" and not winter_has(s,"meter"):
            return [(None,"눈금은 낮은 곳에서 떨린다. 기록지에는 며칠치 가동 시각과 끊긴 선이 남아 있다."),("daram","꼭대기까지 못 가네. 부리 씨한테 물어보자.")]
        if place=="post" and key=="mailbag":
            return [(None,"지난주 날짜의 발송 표가 붙은 짐까지 쌓여 있다. 약과 제분기 부품을 요청한 주문서는 아직 회신이 없다."),("daram","편지만 못 나가는 게 아니구나.")]
        return None

    def winter_local_look(s):
        base=WINTER["places"][s["location"]]["look"]
        if winter_crisis_stage(s)>=2:
            base+=" 골목에서 집기를 옮기는 소리가 들린다. 집마다 버티던 주민들이 난로가 있는 곳으로 모이고 있다."
        return base

label winter_exploration_decision:
    if winter_action_id=="room_reason":
        menu:
            "남은 짐으로 어디까지 짐작할 수 있을까?"
            "잠깐 외출했다가 돌아오지 못했을 수 있다":
                $ winter=winter_flag(winter,"mother_short_errand")
                call winter_lines([("dad","그럴 가능성은 있어. 식사 약속을 했는지도 물어보자."),("daram","메모에 이름 쓴 분은 어디 있는지 알겠지?")],"room_hypothesis")
            "누군가 억지로 데려갔을지도 모른다":
                $ winter=winter_flag(winter,"mother_forced_hypothesis")
                call winter_lines([("dad","그럴 수도 있지. 다만 이 짐만으로 단정할 수는 없어."),("daram","마지막에 본 사람부터 찾자. 엄마가 혼자였는지도.")],"room_hypothesis")
            "짐만으로는 모르니 메모에 적힌 일을 따라간다":
                $ winter=winter_flag(winter,"mother_note_hypothesis")
                call winter_lines([("daram","부리한테 물어볼 게 있었다는 건 알겠어."),("dad","그래. 무엇을 확인하려 했는지부터 찾아보자.")],"room_hypothesis")
    elif winter_action_id=="ration_compare":
        menu:
            "세 문서로 확인할 수 있는 것은?"
            "배정 여섯, 인수 둘. 전용 넷이 빠졌다":
                call winter_lines([("daram","번호 41, 42는 여관, 그 뒤 넷은 보관소야. 여섯을 받았다가 숨긴 게 아니네."),("nabi","우리 인수증도 같이 남겨 줘. 내가 서명한 건 거기까지니까.")],"ration_deduction")
            "중앙 보관소가 넉 자루를 받도록 지시했다":
                call winter_lines([("dad","여관 도착 전의 변경입니다. 원본 세 장을 함께 봐야 합니다."),("nabi","그러니 여관에서 사라진 돈이나 먹을 것처럼 쓰면 안 되지.")],"ration_deduction")
            "중앙 보관소 직원이 몰래 넉 자루를 먹었다":
                call winter_lines([("nabi","어디로 보냈는지와 누가 먹었는지는 다르지. 나도 억울하지만 없는 말로 갚지는 말아 줘."),("daram","안에 뭐가 있는지는 아직 못 봤어.")],"ration_unsupported")
                return False
    elif winter_action_id=="ration_share":
        menu:
            "확인한 내용을 어떻게 알릴까?"
            "나비의 동의를 받고 세 기록을 함께 공개한다":
                $ winter=winter_flag(winter,"ration_public")
                call winter_lines([("nabi","내 서명이 있는 인수증은 써도 돼. 밥 먹던 손님 이름은 가려 줘."),("dad","예. 배급 경로만 대조하겠습니다."),(None,"배급표 담당자에게 원본 번호와 인수증을 함께 전달했다. 정정 접수 도장을 받았다."),("nabi","회의에서 또 네 탓이라고 하면, 나도 이 기록을 들고 말할게.")],"ration_published")
            "사본을 두고 우선 공급의 이유를 찾는다":
                $ winter=winter_flag(winter,"ration_private")
                call winter_lines([("dad","원본은 보관하고 왜 보관소가 우선인지 더 보겠습니다."),("nabi","알겠어. 마음 바뀌면 말해. 내 인수증을 공개하는 건 괜찮아.")],"ration_withheld")
    elif winter_action_id=="mother_reply_reason":
        menu:
            "엄마의 답장과 점검 기록은 어느 곳을 가리킬까?"
            "우편실 뒤 꺼진 등 아래의 폐쇄된 배관 길":
                call winter_lines([("daram","부리 씨한테도 그 관을 물었어. 등불지기는 거길 점검했고."),("dad","불빛 말고 열이 남은 곳. 답장과 맞아. 입구를 찾아보자.")],"reply_reasoned")
                $ winter=winter_flag(winter,"passage_known")
            "불을 끈 곳이면 어디든 엄마가 있을 것이다":
                call winter_lines([("daram","꺼진 등은 여러 갠데…… 엄마는 눈이 녹는다고도 썼어."),("dad","그래. 점검한 곳과 함께 보자.")],"reply_incomplete")
                return False
            "단정하지 말고 기록을 다시 읽는다":
                return False
    elif winter_action_id=="plaza_plans":
        menu:
            "토리는 짐을 묶으며 대답을 기다린다."
            "내일 우편실에 가려고 한다고 말한다":
                $ winter=winter_flag(winter,"plaza_plan_shared")
                $ winter=winter_share_fact(winter,["resident_tori"],"post_visit_tomorrow","dad")
                call winter_lines([("dad","내일 가 보려고요."),("resident_tori","그럼 길만 알아 두세요. 큰 돌 왼쪽이에요."),("daram","응. 왼쪽.")],"plaza_plan_shared")
            "길만 알아 두겠다고 한다":
                call winter_lines([("dad","언제 갈지는 아직 모르겠습니다. 길만 알아 두려고요."),("resident_tori","알겠어요. 이 짐 떨어지기 전에 좀 묶어야 해서.")],"plaza_plan_private")
    return True
