# 0.20.7 (play review D23-06 and the full play check): the old campaign's goal line ("의문 · …",
# "10일째 청문까지 N일") read stale in the new story (save cards, the day board). The new story
# has no such single goal, so the line is left out; the save card keeps place and last line.
init 340 python:
    _r13_v111_campaign_goal=r13_campaign_goal
    def r13_campaign_goal():
        if globals().get("r13_v111_active",lambda:False)():return None
        return _r13_v111_campaign_goal()

# 후반 기획서 D (2026-10-23): 장면 단위 의문보다 지금 단계의 목적을 먼저 보인다. 지금까지 확인한
# 사실만 말한다. 단계 문구가 없는 대기에서는 기존 장면 의문을 그대로 쓴다.
init 341 python:
    R13_V111_STEP_GOALS={
        # 2026-10-27 UX 인계서 D05: 지금 할 수 있는 행동 한 문장. 정답 자료·결과는 말하지 않는다.
        "gate_request":"돌목 씨에게 우리 방문 신청 기록을 확인받자.",
        "gate_choice":"돌목 씨에게 우리 방문 신청 기록을 확인받자.",
        "gate_investigate":"서류의 날짜·이름·방문 목적과 초소 규칙을 직접 확인하자.",
        "nubi_children_receipt7":"선생님이 아이 셋을 실제로 맡았는지 확인하자.",
        "bori_witness7":"보리 씨가 창고 앞에서 직접 본 일을 확인하자.",
        "nabi_beds13":"수레에서 내려올 사람들이 누울 자리를 확인하자.",
        "momo_down13":"내려온 사람을 학교에서 실제로 맡았는지 확인하자.",
        "guldol_down13":"내려온 사람을 학교에서 실제로 맡았는지 확인하자.",
        "transport_cleanup13":"다음 명단이 와도 다시 태우지 못하게 하자.",
        "device_lock14":"떼어 낸 부품을 다시 사람에게 쓰지 못하게 보관하자.",
        "hp_meal6":"보급판은 확인했다. 아이들에게 돌아가기 전 식당을 둘러볼 수 있다.",
        "hp_house11":"추위를 막을 준비와 판돌 씨의 동의가 먼저다.",
        "hidden_base_offer14":"아내가 시설에 두고 온 수첩을 찾고 있다.",
        "hidden_base_door14":"종이에 옮긴 자국이 이 문틀과 맞는다.",
        "hidden_base_room14":"안에 남은 기록을 아내와 함께 읽어 보자.",
        "wild_room14":"불길이 학교 쪽으로 온다. 가족과 나갈 채비를 해야 한다.",
        "wild_hall14":"도토 씨가 불붙은 돌을 들고 있다. 뒷문 너머는 광장이다.",
        "wild_square14":"잠긴 집에 아이가 있다. 우리 가족도 광장에 오래 머물 수 없다.",
        "wild_road14":"초소에도 푸른 불이 켜졌다. 폐온실은 산길 첫 굽이에 있다.",
        "supply_inventory14":"오늘 밤 학교에서 쓸 몫과 남은 양을 확인하자.",
        # 2026-10-29 외부 검토 「행동이 질문 목록 안에 있다」: 네로에게 가는 일을 나비의 질문에서 빼고 지도의 숲으로 옮겼다.
        # 숲을 누르면 확인 창 없이 오후가 정해지므로, 누르기 전에 그 뜻을 여기서 알린다(결과·정답은 말하지 않는다).
        "afternoon2":"해 지기 전, 피코 씨의 잠자리를 마련할 수 있다. 숲으로 가면 오늘 오후는 네로 씨를 돕는다.",
    }
    # 2026-10-27 외부 리뷰 R04: 장면 의문은 이동 대기 동안 앞 장면 것이 남는다(r13_v111_thought_hold). 그래서 등록을
    # 마치고 여관으로 가는 길에도 「우리 두 사람 모두 제대로 등록됐을까?」가 보였다. 그 의문에 답이 난 값이 있으면
    # 다음 단계의 할 일로 바꾼다. 정답 자료·결과는 말하지 않는다.
    R13_V111_RESOLVED_QUESTIONS={
        "MS14_D01_S04":("gate_registered",True,"등록은 끝났다. 여관에서 13호 방과 아내의 소식을 확인하자."),
    }
    _r13_step_goal=r13_v111_goal
    def r13_v111_goal():
        v=store.room13.get("v111") or {}
        gate=v.get("gate")
        text=r13_day2_guidance() or R13_V111_STEP_GOALS.get(gate) or _r13_step_goal()
        for scene,(key,expected,resolved) in R13_V111_RESOLVED_QUESTIONS.items():
            if text and text==R13_V111_QUESTIONS.get(scene) and r13_v111_value(key)==expected:return resolved
        # 2026-10-29 피드백 E: R04 와 같은 규칙을 값 하나로 못 가리는 장면까지 넓힌다. 이동 중이면 갈 곳을 붙인다.
        for scene,(answered,resolved) in globals().get("R13_V111_RESOLVED_WHEN",{}).items():
            if text and text==R13_V111_QUESTIONS.get(scene) and answered():
                travel=r13_v111_travel_goal(v.get("travel_to")) if gate=="travel" else ""
                resolved=resolved() if callable(resolved) else resolved
                return (resolved+" "+travel).strip()
        return text

# 0.20.10 (4~14일 리뷰): 힌트 라벨이 없는 대조의 되묻기. 비교할 범위만 말하고 정답 자료는 말하지 않는다.
init 342 python:
    R13_PROOF_RANGE={
        "불이 시작된 곳과 진술을 대조한다":"불이 시작된 자리와 그 자리에 무엇이 있었는지만 보자. 장작을 누가 가져갔는지는 다른 이야기다.",
        "불의 원인과 빈 창고 진압을 구분한다":"불을 낸 일, 불을 끈 일, 그때 아이들이 어디 있었는지. 셋을 따로 세워야 한다.",
        "불의 원인과 아이 구조를 구분한다":"불을 낸 일, 아이들을 꺼낸 일, 그 말을 누가 했는지. 셋을 따로 세워야 한다.",
        # 2026-10-27 A01: 되묻기는 할머니의 「흔한 핀」 말에 걸린 것만 짚는다. 무엇과 무엇을 잇는지는 셋째 오답 힌트로 옮겼다.
        "구리선과 수선 출처를 대조한다":"같은 모양이라는 말만으로, 같은 핀이라고 할 수도 다른 핀이라고 할 수도 없다.",
        "첫 비명 뒤 핀을 다시 채운 때":"핀이 언제 다시 채워졌는지. 그 시각을 적은 기록끼리 맞춰 보자.",
        "수신인과 가족 전달 권한을 구분한다":"할머니에게 맡겼다는 기록이 있는지부터 보자. 아내 쪽에서 나간 것마다 받는 사람이 어떻게 적혔는지.",
        # 2026-10-29 논쟁 점검 P08: 옛 글(「반송된 쪽지, 글씨 본보기, 초대장」)은 따로 된 자료가 아닌 둘을 찾게 하고, 꼭 필요한
        # 「누가 그 초대장을 부쳤는지」는 가리키지 않았다. 세울 고리 셋만 말한다. 자료 이름은 말하지 않는다.
        "반송·필사본·초대 발송을 대조한다":"초대장 그 자체, 누가 그것을 부쳤는지, 글씨가 닮게 된 차례. 셋을 따로 세워 보자.",
        "초롱과 피코의 하루를 대조한다":"초롱과 피코가 돌 곁에 얼마나 있었는지, 몸에 무엇이 나타났는지를 나란히 놓자.",
        "창고에서 잠자는 사람을 짚는다":"창고에서 자는 사람이 언제부터 그렇게 됐는지.",
        "요즘 돌이 어디서 오는지 대조한다":"요즘 돌의 값과, 그 돌을 어디서 캐 왔는지.",
        "아르카가 없는 아이들과 대조한다":"돌 곁에 없던 아이들은 어땠는지.",
        "13호 난로의 돌을 내놓는다":"13호 난로에서 나온 것 그 자체를 보이자.",
        "명단과 흰 그릇을 대조한다":"흰 그릇을 받은 아이들과 이송 명단의 이름을 맞춰 보자.",
        "촌장이 어젯밤 있던 곳을 확인한다":"촌장이 어젯밤 어디 있었는지 본 사람이나 남은 것.",
        # 2026-10-29 논쟁 점검 P14: 옛 글은 정답 줄(두 배)을 먼저 말했다. 실룩의 말(「값은 다 같다」)에서 출발한다.
        "장부의 두 배를 실룩에게 보인다":"돌값이 정말 어느 등이든 같았는지. 3일에 그 돌이 거래된 자리를 떠올리자.",
        "인수하지 않은 돌의 약속 값을 보인다":"돌값이 정말 어느 등이든 같았는지. 3일에 그 돌이 거래된 자리를 떠올리자.",
        "피코가 막혀야 했던 까닭을 보인다":"피코가 무엇을 그리고 있었는지.",
        "희생의 숫자와 장부를 대조한다":"한 사람이 열흘을 산다는 숫자가 실제 기록과 맞는지.",
        "아르카가 부른다는 말과 옛 기록을 대조한다":"옛 기록에 무엇이라 적혀 있었는지. 깨진 기록을 이어서 읽자.",
        # 2026-10-29 논쟁 점검 P12: 제출하는 것은 쇠에 남은 것 하나다. 그 내력은 제단에서 「어르신 앞에서 말하겠다」던 사람이 안다.
        "쇠가 언제 붙었는지 보인다":"쇠 자체에 남은 것. 그리고 그것이 무엇인지 아는 사람이 지금 이 자리에 있다.",
        "맨 처음 이름을 짚는다":"맨 처음 새겨진 이름과 그 집의 돌.",
        "두 편지를 나란히 본다":"두 편지에서 같은 말과 다른 말을 찾자.",
        # 2026-10-29 논쟁 점검 P06: 10일 13호 5번은 자료가 다섯 장인데 되묻기가 꺼져 있었다. 할머니 말에서 출발해 견줄 범위만 말한다.
        "접촉면과 아이의 위치를 대조한다":"‘쓰러진 뒤에 집기만 했다’. 그 말이 맞다면 촛대 조각에 붙은 것, 상처에 남은 것, 그때 아이가 있던 자리와 어긋나지 않아야 한다.",
        # 2026-10-29 논쟁 점검 P11: 3일 등 예방판 A·B 도 되묻기가 없었다.
        "수리 뒤 새로 생긴 파손을 가린다":"톡 씨가 고친 뒤, 새벽에 마지막으로 그 안을 본 때. 그때와 지금 그 안이 어떻게 다른지.",
        "남아 있는 돌과 칼의 사용을 연결한다":"‘바깥 걸쇠만 닫았다’. 그 말대로라면 칼끝이 어디까지 닿을 수 있었는지.",
        "두 편지의 초대를 대조한다":"두 편지가 누구를 부르는지, 부르지 않는지.",
    }
    # 그날 할 일을 마친 잠자리 단계와 확인 요청 단계의 '생각'.
    # 2026-10-29: 2일 저녁 lamp_prep2 도 잠자리 단계다. 다람의 「방으로 들어간다」를 빼고 13호 침대로 옮겼으므로 같은 말로 침대를 가리킨다.
    for _gate in ("lamp_prep2","sleep1","sleep2","sleep3","sleep4","sleep5","sleep6_input","free_sleep7_input","detained_bed7",
                  "sleep8_input","sleep9_input","sleep10_input","sleep11_input","sleep12_bed_input","sleep13_input",
                  "sleep13_gate_input","departed_bed13"):
        R13_V111_STEP_GOALS[_gate]="오늘 할 일은 마쳤다. 잠자리를 정리하자."
    R13_V111_STEP_GOALS.update({
        "teacher_relief_check13":"초소로 가기 전, 선생님 곁을 누가 이어 맡는지 확인하자.",
        "altar_guide14":"제단까지 갈 길을 바둑이에게 확인해 달라고 하자.",
        "heat_check11":"벽 그림과 떨어진 돌판에 무엇이 적혀 있는지 보자.",
        "root_note11":"눌러 둔 돌 아래 쪽지를 찾자.",
        # 2026-10-29 피드백 E: 초상화 부탁을 마친 뒤의 등 조사와 네로 일손. 장면 의문(그려 줄 사람·남은 낮 시간)은 이미 답이 났다.
        "lamp_observe":"피코 씨가 자는 등 아래를 직접 살펴보자.",
        "nero_work":"네로 씨가 맡긴 침구 일을 거들자.",
        # 2026-10-29 눈가림 플레이: 3일 광장에는 단계 문구가 하나도 없어 장면 의문 「돌은 언제 사라졌을까?」만 남았다.
        # 톡이 「집게는 공방 판에」라고 한 직후라 플레이어는 잠긴 공방으로 가고, 초롱에게 점검장을 청할 차례인 줄 몰랐다.
        "lamp_inspect3":"톡 씨를 데려가기 전에, 3번 등 안부터 직접 살펴보자.",
        "fragment_request":"안쪽에서 나온 조각이 무엇인지, 등을 고친 톡 씨에게 물어보자.",
        "lamp_log_request":"돌이 언제까지 있었는지가 먼저다. 초롱 씨에게 점검장을 보여 달라고 하자. 공방은 그다음이다.",
        "loan_read":"톡 씨가 말한 집게가 공방 판에 있는지 확인하자.",
        "measurement_read":"우박 씨가 잰 기록을 직접 읽어 보자.",
        "transport_read":"새벽에 톡 씨를 봤다는 짐꾼에게 운반표를 청해 보자.",
        "knife_permission":"짐꾼의 수레 손잡이 옆에 있던 것을 보여 달라고 하자.",
        "store_visit":"수취 창고에 가서 직접 확인하자.",
        "stone_check":"창고에 있는 돌의 번호를 톡 씨에게 봐 달라고 하자.",
        "sale_check":"그 돌이 어떻게 창고에 들어왔는지 기록을 보자.",
        "restore_input":"3번 돌을 등에 되돌려 놓자.",
    })

init 343 python:
    # 2026-10-29 피드백 E: 이동 대기 동안 앞 장면 의문을 붙들어 두는 규칙(2026-10-24 행동 검수 4, 소유자 승인)은 그대로 둔다 —
    # 4일 처마→초소처럼 의문이 아직 열려 있는 경우가 있다. 다만 그 의문에 이미 답이 난 장면은 R04 처럼 바꾼다.
    # 2일: 초상화를 맡긴 뒤에도 「그려 줄 사람을 찾을 수 있을까?」, 오후 일을 정한 뒤 저녁 13호에서도 「남은 낮 시간으로…」가 남았다.
    R13_V111_RESOLVED_WHEN={
        "MS14_D02_S03":(lambda:r13_v111_value("portrait_commissioned") is True,"초상화는 피코 씨에게 맡겼다."),
        # 2026-10-29 눈가림 플레이: 오후 일을 마치고 저녁 13호에서 여관 접수대로 가는 대기에서도 「오늘 오후에 할 일은 정했다.」가
        # 떠 시간과 어긋났다. 저녁(period 2)이면 하루가 기울었다는 말만 한다. 결과(피코가 어디서 자는지)는 말하지 않는다.
        "MS14_D02_S04":(lambda:r13_v111_value("D02_afternoon") in ("shelter","nero"),
            lambda:"날이 저물었다." if (store.room13 or {}).get("period",0)>=2 else "오늘 오후에 할 일은 정했다."),
    }
    # 2026-10-29 피드백 E: 받침이 있으면 「으로」, 없거나 ㄹ 받침이면 「로」.
    def r13_ro(word):
        ch=word[-1] if word else ""
        if u"\uac00"<=ch<=u"\ud7a3":
            return word+("로" if (ord(ch)-0xAC00)%28 in (0,8) else "으로")
        return word+"(으)로"
    def r13_v111_travel_goal(target):
        name=R13_PLACES.get(target,(None,))[0] if target else None
        return (r13_ro(name)+" 가자.") if name else ""
    # 2026-10-29 피드백 E: 흐린 장소를 누르면 「지금은 갈 수 없습니다」만 나와 왜 막혔는지 몰랐다. 이동 중이면 가는 곳을,
    # 아니면 지금 화면의 「생각」을 붙인다. 정답·결과는 말하지 않는다(생각 줄과 같은 문장).
    def r13_map_locked_notice(label):
        base=label+" · 지금은 이곳으로 갈 수 없습니다."
        if not globals().get("r13_v111_active",lambda:False)():return base
        v=store.room13.get("v111") or {}
        if v.get("gate")=="travel" and v.get("travel_to") in R13_PLACES:
            return label+" · 지금은 "+r13_ro(R13_PLACES[v["travel_to"]][0])+" 가는 길입니다."
        goal=r13_v111_goal()
        return (label+" · 아직 갈 일이 없습니다. 지금 생각: "+goal) if goal else base

# 2026-10-29 외부 검토 2 N4: 6일 창고. 선생님 자리를 받은 뒤에도 「생각」이 P01 의문(이미 답이 난 것)에 머물렀고,
# 꼬미가 「깡통은 아직 여기 있어」로 멈춰도 어디를 눌러야 하는지 말이 없었다. 지금 할 일 한 문장만. 결과는 말하지 않는다.
init 344 python:
    _r13_goal_before_can6=r13_v111_goal
    def r13_v111_goal():
        v=store.room13.get("v111") or {}
        if v.get("gate")=="afternoon6" and r13_v111_value("kkomi_seat6") is True:
            if r13_v111_value("kkomi_can_wait6") and not r13_v111_value("acorn_recovered"):
                return "꼬미는 문에 단 깡통을 두고는 못 간다고 한다. 문 옆 천장에 매단 그 줄부터 살피자."
            return "선생님 자리는 받아 두었다. 창고로 돌아가 꼬미에게 알리자."
        # 2026-10-29 눈가림 플레이: 2일 식당에서 나비를 돕기로 한 뒤 무엇을 눌러야 할지 몰라 물건을 이것저것 누르다
        # 지도에서 숲을 골라 오후가 네로 쪽으로 넘어갔다. 「생각」은 처음 문장(잠자리를 마련할 수 있다)에 멈춰 있었다.
        # 한 일에 따라 다음 행동 한 문장만 바꾼다. 숲으로 가면 오후가 정해진다는 경고는 늘 붙인다. 결과는 말하지 않는다.
        if v.get("gate")=="afternoon2":
            tail=" 숲으로 가면 오늘 오후는 네로 씨를 돕는다."
            if r13_v111_value("piko_bench_clean2"):
                return "벤치는 깨끗해졌다. 광장의 피코 씨에게 자리가 있다고 알리자."+tail
            if r13_v111_value("piko_bench_seen2") and r13_v111_value("piko_cloth2"):
                return "빌린 천으로 벤치의 물감 자국을 닦자."+tail
            if r13_v111_value("piko_bench_seen2"):
                return "벤치의 물감 가루를 닦을 마른 천이 있어야 한다. 여관 접수대 할머니께 여쭤 보자."+tail
            if r13_v111_value("piko_sacks2"):
                return "포대는 옮겼다. 비워 둔 벤치 자리를 살펴보자."+tail
        return _r13_goal_before_can6()

# 2026-10-29 눈가림 플레이: 3일 기록의 메모 탭에 1일에 이미 풀린 옛 이야기 의문(「둘이 예약했는데 왜 한 명으로 적혔을까?」)과
# 그 「막혔다면 생각 정리」(선반의 서류…)가 그대로 남았다. 옛 층(room13_learning.rpy)은 옛 깃발 entry_corrected 가 없으면 이 카드를
# 만드는데, 새 이야기는 그 깃발을 세우지 않는다. 새 이야기에서는 지금 장면의 의문 하나만 두고, 「막혔다면」 칸은 지금의 「생각」과
# 같은 문장(지금 할 행동)을 보인다. 의문에 이미 답이 났으면(R04·피드백 E 규칙) 의문 대신 「지금 할 일」로 둔다.
init 345 python:
    _r13_v111_notes_before=r13_first_mystery_notes
    def r13_first_mystery_notes():
        if not globals().get("r13_v111_active",lambda:False)():return _r13_v111_notes_before()
        v=store.room13.get("v111") or {}
        scene=v.get("thought_scene") if v.get("gate")=="travel" and v.get("thought_pending") else v.get("scene")
        question=R13_V111_QUESTIONS.get(scene,"")
        goal=r13_v111_goal() or ""
        if not question and not goal:return []
        answered=False
        fixed=R13_V111_RESOLVED_QUESTIONS.get(scene)
        if fixed and r13_v111_value(fixed[0])==fixed[1]:answered=True
        when=R13_V111_RESOLVED_WHEN.get(scene)
        if when and when[0]():answered=True
        title=question if question and not answered else "지금 할 일"
        return [dict(title=title,fact="",question="",hint=(goal if goal!=title else ""),keys=[])]

