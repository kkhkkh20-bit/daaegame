# 시간 규칙과 저녁 미션 (소유자 지시, 0.18.5)
#   - 시간은 일(오전·오후 한 번씩)과 13호에서 자는 것으로만 흐른다.
#     조사·대화·이동·활동·사건 선택은 시간을 쓰지 않는다.
#   - 저녁에는 일이 없다. 그날 저녁에만 할 수 있는 "저녁 미션"이 열린다.
#     자면 그날 미션은 사라진다(다시 열리지 않는다).
#   - 사건의 결과로 하룻밤을 잃는 것(감금·격리)은 그대로 둔다. 플레이어가 고른 행동의 대가다.
init 106 python:
    # Activities and context waits no longer spend time.
    for _a in ROOM13["activities"].values():
        _a["cost"]=0
    R13_CONTEXT_WAIT.clear()

    for _key,_name,_est,_not in (
        ("W6","식어 가는 등","광장 등 열두 개 가운데 넷이 한 달 사이 반나절 일찍 꺼진다. 초롱은 이번 겨울 조각을 두 번 갈았다.","등이 식는 것과 돌이 식는 것이 같은 일인지는 초롱도 모른다."),
        ("W7","보호실의 밤","재판까지 아이는 입구 옆 보호실에서 지낸다. 밤에는 경비 한 사람만 남고, 담요와 먹을 것은 그 경비 마음이다.","보호실 규칙을 누가 정했는지는 경비들도 모른다."),
    ):
        ROOM13["evidence"][_key]=dict(id=_key,name=_name,kind="기록",establishes=_est,does_not_establish=_not,scenes=[],current_run_only=True,retained_on_show=True)
    R13_RECORD_SHORT.update(W6="식어 가는 등",W7="보호실의 밤")

    R13_EVENING_PLACE=dict(inn="여관",dining="식당",kitchen="주방",square="광장",store="창고",gate="입구")
    # key, days, place, title, hint, open(state)
    R13_EVENING_MISSIONS=[
        ("ep1_patrol",(2,2),"inn","여관 순찰 지켜보기","경비가 여관에 등록 검사를 온다는 말이 돈다.",
            lambda:not r13_has("ep1_patrol_seen")),
        ("ep2_kitchen",(2,3),"kitchen","주방 뒷문의 불빛","밤마다 주방 뒷문에 작은 불이 켜진다.",
            lambda:not r13_has("ep2_seen")),
        ("lamp_round",(2,3),"square","초롱과 등불 돌기","등불지기 초롱이 저녁 순회를 돈다.",
            lambda:not r13_has("ev_lamp_done")),
        ("ev_c",(3,3),"inn","백 부인의 밤일","백 부인이 저녁에 일손을 구한다고 한다.",
            lambda:not r13_has("ev_c_done") and not r13_has("madam_hostile")),
        ("ev_b",(3,3),"store","창고 앞 소동","공동 창고 쪽이 소란스럽다.",
            lambda:not r13_has("ev_b_done")),
        ("night_visit",(5,6),"gate","보호실 밤 면회","밤에는 보호실에 경비가 한 사람만 남는다.",
            lambda:store.room13.get("daram_state")=="held" and not r13_has("ev_visit:%d"%store.room13["day"]) and not r13_has("visit_banned")),
        ("ep3_bell",(5,6),"square","광장 종 아래 모임","광장 돌이 흐려졌다고 사람들이 모인다.",
            lambda:not r13_has("ep3_bell_seen")),
        ("eve_trial",(6,6),"dining","재판 전날 밤 식당","내일 재판에 나올 사람들이 식당에 모였다.",
            lambda:not r13_has("ev_eve_done")),
    ]

    def r13_evening_open():
        s=store.room13
        return bool(s) and s.get("period")==2 and s.get("day") in (2,3,5,6)

    def r13_evening_missions():
        if not r13_evening_open():return []
        day=store.room13["day"]
        return [(k,place,title,hint) for k,days,place,title,hint,ok in R13_EVENING_MISSIONS
            if days[0]<=day<=days[1] and ok()]

label r13_evening_auto:
    # Once per evening: the work day is over, show what tonight allows.
    if not r13_evening_missions() or r13_has("evening_brief:%d"%room13["day"]):
        return None
    $ r13_flag("evening_brief:%d"%room13["day"])
    call r13_ev_here("night")
    call r13_lines([(None,"하루 일이 끝났다. 저녁에는 일이 없지만, 오늘 밤에만 할 수 있는 일이 있다. 자기 전까지는 시간이 흐르지 않는다.")],"evening:brief")
    call r13_evening_board
    return _return

label r13_evening_board:
    $ _ev_items=[(title+" · "+R13_EVENING_PLACE.get(place,place),place) for key,place,title,hint in r13_evening_missions()]
    if not _ev_items:
        call r13_lines([(None,"오늘 저녁에는 따로 남은 일이 없다. 사람들을 만나거나 13호에서 쉬자.")],"evening:none")
        return None
    call r13_lines([(None,"  ".join("· "+hint for key,place,title,hint in r13_evening_missions()))],"evening:hints:%d"%room13["day"])
    $ _ev_pick=renpy.display_menu(_ev_items+[("혼자 마을을 둘러본다",None)])
    return _ev_pick

# Arrival scenes for the three new missions (called from r13_town_events).
label r13_evening_events:
    if room13["period"]!=2:
        return None
    $ _d,_loc=room13["day"],room13["location"]
    if _d in (2,3) and _loc=="square" and not r13_has("ev_lamp_done"):
        call r13_ev_lamp_round
    if _d in (5,6) and _loc=="gate" and room13.get("daram_state")=="held" and not r13_has("ev_visit:%d"%_d) and not r13_has("visit_banned"):
        call r13_ev_night_visit
    if _d==6 and _loc=="dining" and not r13_has("ev_eve_done"):
        call r13_ev_eve_trial
    return None

# ---- 초롱과 등불 돌기 (2~3일 저녁, 광장) ----
label r13_ev_lamp_round:
    $ r13_flag("ev_lamp_done")
    call r13_ev_here("night")
    call r13_lines([(None,"광장 가장자리에서 초롱이 긴 장대로 등 뚜껑을 하나씩 열고 있었다."),
        ("resident_lamplighter","저녁 순회예요. 따라오셔도 돼요. 대신 등 바로 아래에는 서지 마세요."),
        ("daram","아빠, 등마다 이름표가 붙어 있어!")],"ev:lamp:open")
    $ _ep_loop=True
    while _ep_loop:
        $ _ep_loop=False
        menu:
            "식은 등을 함께 센다" if "W6" not in room13["evidence"]:
                call r13_lines([("resident_lamplighter","식은 등은 열둘 중에 넷이요. 한 달 전보다 반나절 일찍 꺼져요. 이번 겨울에만 조각을 두 번 갈았어요."),
                    ("dad","등이 식는 겁니까, 돌이 식는 겁니까?"),
                    ("resident_lamplighter","……돌이 식는지 재 본 사람은 우박뿐이에요. 저는 장대만 들고 다니고요.")],"ev:lamp:count")
                $ r13_grant(["W6"],"초롱과 센 광장 등")
                $ r13_flag("know_stone_failing","lamplighter_trust")
                $ _ep_loop=True
            "꺼진 등을 직접 켜 본다" if "W5" not in room13["evidence"]:
                call r13_lines([(None,"초롱이 손톱만 한 조각을 집게로 건넸다. 장갑을 꼈는데도 사람 손처럼 따뜻했다."),
                    (None,"조각을 등에 끼우자 차가운 유리가 천천히 데워졌다."),
                    ("resident_lamplighter","이 조각은 돌에서 떼어 낸 거예요. 이게 없으면 등은 그냥 유리병이에요.")],"ev:lamp:light")
                $ r13_grant(["W5"],"초롱과 켠 광장 등")
                $ _ep_loop=True
            "다람이와 등에 이름을 붙인다" if room13.get("daram_state") in ("with_dad","rescued") and not r13_has("daram_lamp_named"):
                call r13_lines([("daram","이 등은 ‘도토리’! 제일 작은데 제일 밝아."),
                    ("resident_lamplighter","……그 등은 원래 이름이 없었어요. 이제 생겼네요."),
                    ("dad","(오랜만에 다람이가 웃었다.)",{"thought":True})],"ev:lamp:name")
                $ r13_flag("daram_lamp_named","lamplighter_trust")
                $ _ep_loop=True
            "등 하나를 꺼 두자고 한다" if not r13_has("lamps_saved"):
                call r13_lines([("resident_lamplighter","하나쯤은 괜찮아요. 등을 끄면 돌이 덜 지친다고들 해요."),
                    ("neoul","누가 등을 끄라고 했소? 불 꺼진 길에서 사람이 넘어지면 당신 탓이오."),
                    ("resident_lamplighter","……다시 켤게요.")],"ev:lamp:off")
                $ r13_flag("neoul_annoyed")
                $ _ep_loop=True
            "순회를 마치고 돌아간다":
                call r13_lines([("resident_lamplighter","내일도 이 시간에 돌아요. 등은 밤마다 조금씩 달라요.")],"ev:lamp:end")
    return

# ---- 보호실 밤 면회 (5~6일 저녁, 입구) ----
label r13_ev_night_visit:
    $ r13_flag("ev_visit:%d"%room13["day"])
    call r13_ev_here("night")
    call r13_lines([(None,"입구 옆 보호실 창에 작은 등 하나가 켜져 있었다. 창살 너머에서 다람이가 웅크리고 있었다. 담요도 없었다."),
        ("daram","아빠!"),
        ("resident_badook" if r13_has("badook_doubt") or r13_has("badook_ally") else "neoul","면회는 잠깐이오. 물건은 내가 먼저 보오.")],"ev:visit:open")
    if "W7" not in room13["evidence"]:
        $ r13_grant(["W7"],"보호실 앞에서 들은 밤 규칙")
    $ _visit_turns=2
    while _visit_turns>0:
        $ _visit_turns-=1
        menu:
            "구운 밤을 넣어 준다" if r13_has("own:snack"):
                $ r13_use_item("snack")
                call r13_lines([("daram","따뜻해……. 아빠, 구운 밤 반은 아빠 거야."),
                    ("dad","다 먹어. 아빠 내일 또 올게.")],"ev:visit:snack")
                $ r13_flag("daram_fed")
            "담요를 넣어 달라고 부탁한다" if not r13_has("visit_blanket_asked"):
                $ r13_flag("visit_blanket_asked")
                if r13_has("badook_doubt") or r13_has("badook_ally"):
                    call r13_lines([("resident_badook","……규칙에 없다고 다 금지된 건 아니지. 내 담요요. 아침에는 돌려받겠소."),
                        ("daram","담요에서 바둑이 아저씨 냄새 나.")],"ev:visit:blanket")
                    $ r13_flag("daram_warm","badook_ally")
                else:
                    call r13_lines([("neoul","보호실은 여관이 아니오."),
                        ("dad","(바둑이였다면 달랐을까. 경비도 사람마다 다르다.)",{"thought":True})],"ev:visit:blanket_no")
            "창살 너머로 이야기를 해 준다":
                call r13_lines([("dad","옛날에 도토리 하나가 겨울 숲에서 길을 잃었는데……"),
                    ("daram","……그 도토리, 결국 집에 가?"),
                    ("dad","응. 아빠 도토리가 찾으러 갔거든."),
                    (None,"다람이는 이야기가 끝날 때까지 창살을 잡고 있다가 잠들었다.")],"ev:visit:story")
                $ r13_flag("daram_story")
            "내일 재판이 어떻게 되는지 알려 준다" if room13["day"]==6:
                call r13_lines([("dad","내일 마을 사람들 앞에서 그날 밤 일을 하나씩 다시 짚어 볼 거야. 넌 네가 본 것만 말하면 돼."),
                    ("daram","모르는 건 어떻게 해?"),
                    ("dad","모른다고 하면 돼. 그게 제일 정직한 거야.")],"ev:visit:trial")
                $ r13_flag("daram_prepared")
            "창 걸쇠를 몰래 살핀다":
                call r13_lines([(None,"창 걸쇠에 손을 대자 등 뒤에서 장대 끝이 땅을 쳤다."),
                    ("neoul","지금 뭘 하는 거요. 오늘 면회는 끝이오. 재판 전까지 밤 면회는 없소."),
                    ("daram","아빠……!")],"ev:visit:caught")
                $ r13_flag("visit_banned","neoul_annoyed","rumor:troublemaker")
                $ _visit_turns=0
    if not r13_has("visit_banned"):
        call r13_lines([("resident_badook" if r13_has("badook_ally") else "neoul","시간 됐소.")],"ev:visit:end")
    return

# ---- 재판 전날 밤 식당 (6일 저녁) ----
label r13_ev_eve_trial:
    $ r13_flag("ev_eve_done")
    call r13_ev_here("night")
    call r13_lines([(None,"식당에는 내일 재판에 나올 사람들이 흩어져 앉아 있었다. 누구도 크게 말하지 않았다."),
        ("dad","(내일 재판에서 누가 무엇을 말해 줄지, 오늘 밤 확인해 두자.)",{"thought":True})],"ev:eve:open")
    $ _eve_left=3
    while _eve_left>0:
        $ _eve_left-=1
        menu:
            "나비 옆에 앉는다" if not r13_has("eve:nabi"):
                $ r13_flag("eve:nabi")
                if r13_has("witness:nabi"):
                    call r13_lines([("nabi","내일 재판에서 본 대로 말할게요. 아이들 밥은 이제 걱정 안 해도 되니까요.")],"ev:eve:nabi:yes")
                elif r13_has("kids_fed"):
                    call r13_lines([("nabi","아이들은 이제 괜찮아요. ……그래도 할머니 앞에서 말하는 건 무서워요."),
                        ("dad","(나비가 무서워하는 것은 할머니일까, 아이들 끼니일까.)",{"thought":True})],"ev:eve:nabi:ask")
                else:
                    call r13_lines([("nabi","……내일은 할머니랑 계속 같이 있었다고만 할 거예요. 아이들 밥이 할머니한테 걸려 있거든요."),
                        ("dad","(나비의 입을 막고 있는 건 할머니가 아니라 아이들 끼니다.)",{"thought":True})],"ev:eve:nabi:no")
            "톡을 찾는다" if not r13_has("eve:tok"):
                $ r13_flag("eve:tok")
                if r13_has("witness:tok"):
                    call r13_lines([("resident_tok","핀은 내가 고친 거요. 그 핀이 누구 것인지도 재판에서 내가 말하겠소.")],"ev:eve:tok:yes")
                elif r13_has("tok_detained"):
                    call r13_lines([(None,"톡의 자리는 비어 있었다. 아직 수리점 문에 판자가 덧대져 있다고 했다."),
                        ("dad","(톡이 갇혀 있으면 재판에서 핀 이야기를 해 줄 사람이 없다.)",{"thought":True})],"ev:eve:tok:held")
                else:
                    call r13_lines([("resident_tok","재판? 나는 일만 하오. 내 일이 아니면 끼지 않소."),
                        ("dad","(톡에게 이 재판은 아직 남의 일이다.)",{"thought":True})],"ev:eve:tok:no")
            "밤이를 찾는다" if not r13_has("eve:bami"):
                $ r13_flag("eve:bami")
                if r13_has("bami_taken"):
                    call r13_lines([(None,"처마 밑은 비어 있었다. 검사를 받으러 끌려간 뒤로 밤이를 본 사람은 없었다."),
                        ("dad","(밤이가 그날 본 것은 이제 아무도 말해 줄 수 없다.)",{"thought":True})],"ev:eve:bami:gone")
                elif r13_has("bami_consent"):
                    call r13_lines([("bami","내가 그날 본 거, 내일 재판에서 말할게. 대신 아저씨가 옆에 있어 줘.")],"ev:eve:bami:yes")
                else:
                    call r13_lines([("bami","……사람 많은 데는 싫어. 내가 나서서 말하면 경비들이 나도 데려갈 거잖아."),
                        ("dad","(밤이는 말하기 싫은 게 아니다. 끌려갈까 봐 무서운 것이다.)",{"thought":True})],"ev:eve:bami:no")
            "뿔이 촌장과 마주 앉는다" if not r13_has("eve:ppul"):
                $ r13_flag("eve:ppul")
                if r13_has("fair_hearing"):
                    call r13_lines([("resident_ppul","약속은 지키오. 재판은 증거대로, 집행은 판결대로.")],"ev:eve:ppul:yes")
                else:
                    call r13_lines([("resident_ppul","내일은 마을 법대로 하오. 누가 옳든, 겨울을 넘길 방법이 먼저요."),
                        ("dad","(재판에서 이겨도 촌장이 판결을 따르지 않을 수 있다.)",{"thought":True})],"ev:eve:ppul:no")
            "그만 일어선다":
                $ _eve_left=0
    call r13_lines([("dad","(남은 건 오늘 밤뿐이다. 자기 전에 할 수 있는 일을 하자.)",{"thought":True})],"ev:eve:end")
    return
