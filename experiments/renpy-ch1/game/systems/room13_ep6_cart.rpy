# 에피소드 ⑥ 「끌려가는 수레」 (13일)와 제단 앞 장면(14일). 대본: docs/EPISODE6_FINALE_SCRIPT.md
#   마을은 대대로 죽음을 '보호소'라고 불러 왔다.
#   13일 아침: 광장에 결박 끈을 실은 수레, 게시판의 수레 명단(엄마 이름도), 판돌 영감.
#   13일 세 칸: 장터(은호의 편도 쪽지, 구슬의 다른 장부) · 창고 뒷길(뭉치, 백 부인의 비축품)
#              · 마구간(실룩, 수레를 늦춘다) · 회관(바둑이와 명령서 — 증인으로 세운다).
#   칸을 쓰지 않는 것: 할머니의 차(할머니의 말), 종탑의 설이(종), 여니·토리의 빨래 수레(한 사람을 빼낼 길).
#   13일 밤: 광장 수레 앞 → 회의 Q6(촌장) → 결정(수레를 멈춘다 / 가족만 뺀다 / 명단을 공개한다 / 할머니를 세운다).
#   14일: 기존 제단 결말(r13_finale → F1~F4 → E0~E6) 앞에 그림책·손자국·할머니의 고백을 넣는다.
#   결말 준비(쉴 곳·식량·교대·환자 운반)는 에피소드 결과로도 채운다. 진 엔딩(E6)은 모든 에피소드를 완벽하게 끝낸 판.
#   깃발 접두사 cv_, 장면 r13_cv_*.
init 157 python:
    for _key,_name,_est,_not in (
        ("V00","수레의 결박 끈","광장 수레에 담요 대신 손목 고리가 달린 끈이 실렸다. 그래서 무슨 뜻? 보살피러 가는 수레가 아니다.",""),
        ("V01","수레 명단","'보호소 이송'. 굴돌, 모모, 판돌 옆엔 '잊음', 그 아래 '말썽' 줄에 엄마 이름. 그래서 무슨 뜻? 아픈 사람만이 아니라 마을이 치우고 싶은 사람도 보낸다.",""),
        ("V02","은호의 빌림 쪽지","\"수레 한 대, 하루, 편도.\" 그래서 무슨 뜻? 돌아올 짐이 없다. 올라간 사람은 안 내려온다.",""),
        ("V03","은호의 다른 장부","수레 값을 낸 곳은 회관이 아니라 여관. 지난 네 겨울, 같은 날, 같은 편도 수레. 그래서 무슨 뜻? 해마다 같은 일이고, 돈은 할머니가 냈다.",""),
        ("V04","백 부인의 비축품","창고 쪽문 안쪽, 담요 마흔 장과 곡식 자루. 그래서 무슨 뜻? 마을엔 아직 나눌 것이 있다. 그런데 수레엔 담요 한 장 안 실었다.",""),
        ("V05","실룩의 말","실룩: \"내려올 땐 늘 빈 수레였소. 보호소라는데, 거기 지붕 하나 못 봤소.\" 그래서 무슨 뜻? 사람을 내려놓고 오는 게 아니라, 두고 온다.",""),
        ("V06","명령서","'보호소 이송을 명함.' 촌장의 뿔 도장. 그런데 'ㄹ'의 꼬리가 둥글게 말린 글씨. 그래서 무슨 뜻? 도장은 촌장 것, 손은 다른 사람. 가족을 부른 가짜 편지와 같은 손이다.",""),
        ("V07","할머니의 말","할머니: \"돌이 버티려면 사람이 필요해요. 늘 그래 왔어요.\" 그래서 무슨 뜻? 할머니는 수레가 어디로 가는지 알고 있다.",""),
        ("V08","손 아래의 온기","제단의 작은 손자국에 다람이 손을 얹자 그 자리만 따뜻해졌고, 손을 떼도 다람은 멀쩡했다. 그래서 무슨 뜻? 사람이 죽지 않아도 돌은 데워진다.",""),
    ):
        ROOM13["evidence"][_key]=dict(id=_key,name=_name,kind="기록",establishes=_est,does_not_establish=_not or "이것만으로 다른 사실까지 정할 수는 없다.",scenes=[],current_run_only=True,retained_on_show=True)
    R13_RECORD_SHORT.update(V00="결박 끈",V01="수레 명단",V02="편도 쪽지",V03="은호의 다른 장부",V04="백 부인의 비축품",V05="실룩의 말",V06="명령서",V07="할머니의 말",V08="손 아래의 온기")
    R13_NAMES["npc_pandol"]="판돌 영감"
    R13_CHARS["npc_pandol"]=Character("판돌 영감",cb_who_id="npc_pandol")

    def r13_cv_daram():
        return (store.room13 or {}).get("daram_state") in ("with_dad","rescued")

    # ---- 회의 Q6: 수레 앞 (13일 밤, 광장, 맞서는 사람 촌장) ----
    R13_DEBATE_SEATS["ep6"]=["resident_ppul","neoul","resident_badook","resident_bori","mom","resident_seol"]
    R13_DEBATE_STANCE["ep6"]=("보호소라 믿는다","모르겠다","수레를 막는다")
    R13_EP_MEETING_PLACE["ep6"]="winter_square"
    R13_EP_MEETING_HEADER["ep6"]="광장 회의 · 13일째 밤"
    R13_DEBATE["Q6"]=dict(title="수레는 어디로 가나",session="ep6",chair="resident_ppul",
        statements=[
            dict(id="s1",who="resident_ppul",text="이 수레는 【보호소】로 가는 수레요.",
                accept=["Y05"],soft={"V03":("resident_ppul","편도 수레가 뭘 증명하오."),"V05":("resident_ppul","끄는 사람 말 하나로?")},
                broken_by={"Y05":[("mom","이건 마을의 죽은 사람 명단이에요. 여기 모과 할멈. 작년에 보호소로 간 분이죠. 죽은 사람 칸에 있어요."),
                    ("dad","그리고 여기. 판돌 영감님 이름이 이미 적혀 있습니다. 옆에 '이송'. 아직 떠나지도 않은 사람이, 죽은 사람 명단에 있습니다."),
                    ("npc_pandol","……모과가 거기 있소?"),(None,"……")]},
                hint="보호소에 간 사람들이 적힌 곳.",
                wrong=("resident_ppul","그게 보호소가 없다는 증거요?")),
            dict(id="s2",who="resident_ppul",text="【돌은 희생으로만 버티오】. 보내지 않으면 마을 전체가 얼어 죽소.",
                accept=["Y14"],soft={"Y06":("resident_ppul","손바닥 위의 조각 셋으로 마을을 데우겠다는 거요?")},
                broken_by={"Y14":[("mom","어젯밤, 아무도 바치지 않았어요. 옛 시설에 남은 조각을 모아 큰 돌을 데웠어요. 등이 밝아진 거, 다 보셨죠."),
                    (None,"사람들 틈에서 누군가 말했다. \"……학교 창밖 등이 밝아졌어. 나도 봤어.\"")]},
                hint="어젯밤 광장 등.",
                wrong=("resident_ppul","하루 밝았다고 겨울을 넘기오?")),
            dict(id="s3",who="resident_ppul",text="그래도 이 일은 【내가 명령했소】. 내 도장이오. 책임도 내가 지오.",
                accept=["V06"],
                broken_by={"V06":[("dad","도장은 촌장님 것입니다. 글씨는 아닙니다. 이 'ㄹ' 꼬리를 보십시오. 우리 가족을 이 마을로 부른 가짜 편지와 똑같습니다."),
                    ("resident_badook","순찰대원으로 말합니다. 이 명령서는 여관에서 왔습니다."),(None,"사람들이 웅성거렸다.")]},
                hint="명령서의 글씨.",
                wrong=("resident_ppul","내 도장이 찍혔소.")),
        ],
        conclusion=dict(prompt="이 수레를 어떻게 정리할까?",
            options=[("correct","보호소는 없다. 수레는 제단으로 간다. 명령서는 할머니가 썼다"),
                ("over","촌장이 혼자 다 꾸몄다"),
                ("weak","돌이 식은 건 어쩔 수 없다")],
            correct=[(None,"촌장이 지팡이에 몸을 기댔다. 오래 서 있던 사람처럼."),
                ("resident_ppul","……네 해 전, 첫 겨울이었소. 돌이 처음으로 식었소."),
                ("resident_ppul","내 손녀가 이름을 잊기 시작했소. 내 이름부터. 그다음 제 이름."),
                ("resident_ppul","할멈이 말했소. 돌에 사람을 주면 돌이 버틴다고. 그래서 보냈소. 내 손으로 수레에 태웠소."),
                ("resident_ppul","이제 와서 그게 아니었다고 하면, 나는 그 애를 무엇 때문에 보낸 거요.")]+[("daram","(작게) ……할아버지 손녀 이름 뭐야?"),(None,"촌장은 대답하지 않았다.")],
            over=("resident_badook","글씨가 다릅니다. 촌장님이 감싸는 사람이 따로 있습니다."),
            weak=("mom","어쩔 수 있어요. 어젯밤에 했잖아요.")),
        sway=["resident_badook","resident_bori","resident_seol"])

    R13_EVENT_OFFERS.update({
        "r13_cv_market":("장터에서 은호가 수레 빌린 쪽지를 흔든다",[],""),
        "r13_cv_store":("창고 뒷길 쪽문 앞에서 뭉치가 서성인다",[],""),
        "r13_cv_stable":("마구간에서 실룩이 수레 끌 말을 손질한다",[],""),
        "r13_cv_hall":("회관 문 앞에서 바둑이가 명령서를 들고 서 있다",[],""),
    })
    R13_OFFER_ACTORS.update({"r13_cv_market":("resident_eunho",None),"r13_cv_store":("resident_mungchi",None),"r13_cv_stable":("resident_siluk",None),"r13_cv_hall":("resident_badook",None)})

    # 결말 준비는 에피소드 결과로도 채운다.
    def r13_cv_preparations():
        if r13_has("ws_tents_school") or r13_has("ws_kids_alive") or r13_has("wf_kids_school"):r13_flag("shelter_ready")
        if r13_has("ws_lab"):r13_flag("operators_ready")
        if r13_has("V04"):r13_flag("supplies_ready")
        if r13_has("cart_stopped"):r13_flag("patient_transport")


# =========================================================
# 장면
# =========================================================
label r13_cv_events:
    $ _cvd,_cvp,_cvloc=room13["day"],room13["period"],room13["location"]
    if _cvd!=13:
        return
    if not r13_has("cv_morning"):
        call r13_cv_morning
        return
    if _cvp<=2 and _cvloc=="market" and not r13_has("cv_market"):
        $ r13_offer("r13_cv_market")
    if _cvp<=2 and _cvloc=="store" and not r13_has("cv_store"):
        $ r13_offer("r13_cv_store")
    if _cvp<=2 and _cvloc=="gate" and not r13_has("cv_stable"):
        $ r13_offer("r13_cv_stable")
    if _cvp<=2 and _cvloc=="square" and not r13_has("cv_hall"):
        $ r13_offer("r13_cv_hall")
    if _cvp==2 and _cvloc in ("inn","dining") and not r13_has("cv_tea"):
        call r13_cv_tea
        # 할머니의 차를 마신 저녁은 곧바로 광장의 밤으로 이어진다.
        call r13_cv_night
        return
    if (_cvp>=3 or (_cvp==2 and _cvloc=="square")) and not r13_has("cv_night"):
        call r13_cv_night
    return

label r13_cv_morning:
    $ r13_flag("cv_morning")
    $ r13_event("day13_warning")
    call r13_scene("winter_square","13일 아침 · 광장, 수레","search")
    call r13_lines([(None,"광장 돌 앞에 수레 한 대가 서 있었다. 장터에서 짐 나르던 은호네 큰 수레다."),
        (None,"짐칸에 담요는 없었다. 굵은 끈이 둘둘 말려 있었다. 사람 손목에 맞을 만한 고리가 달린 끈이었다.")]+
        ([("daram","아빠, 저 끈 뭐야? 짐 묶는 거야?")] if r13_cv_daram() else [])+
        [("dad","(짐 묶는 끈에 손목 고리는 없다.)",{"thought":True}),
        ("neoul","오늘 밤, 북쪽 보호소로 가는 수레요. 몸 약한 이들을 따뜻한 데로 모시는 거요."),
        ("neoul","명단은 게시판에 붙였소. 이름 있는 집은 저녁까지 짐을 싸 두시오."),
        (None,"게시판의 종이 한 장. 맨 위에 '보호소 이송'. 굴돌. 모모. 판돌. 이름 옆에 '잊음'.")]+
        ([(None,"그 아래 줄은 다르다. 실룩. 말썽.")] if r13_has("siluk_handed") else [])+
        ([(None,"사자. 말썽.")] if r13_has("teacher_on_cart") else [])+
        [(None,"맨 끝. 엄마의 이름. 말썽.")]+
        ([("daram","엄마 이름이다. 엄마도 가? 엄마 안 아프잖아.")] if r13_cv_daram() else [])+
        [("dad","(이건 아픈 사람 명단이 아니다. 마을이 치우고 싶은 사람 명단이다.)",{"thought":True}),
        (None,"게시판 앞에 판돌 영감이 지팡이를 짚고 서 있었다. 자기 이름을 손가락으로 몇 번이고 짚었다.",{"show":"npc_pandol","pose":"point_name"}),
        ("npc_pandol","이게…… 나요? 판돌. 판돌이 나 맞지요?"),
        ("npc_pandol","보호소엔 불이 잘 든다더구먼. 거기 가면 우리 할멈도 있으려나. ……모과. 작년 겨울에 먼저 갔소.")],"cv:morning")
    $ r13_grant(["V00","V01"],"13일 아침 광장의 수레와 게시판")
    return

label r13_cv_market:
    $ r13_flag("cv_market")
    call r13_scene("r13_market","장터 · 은호","calm")
    call r13_lines([("resident_eunho","수레 말이오? 빌려 줬소. 장사꾼이 빈 수레 놀려서 뭐 합니까."),
        ("resident_eunho","하루, 편도. 값은 이미 받았소. 돌아올 때 실을 짐이 없다더이다."),
        ("dad","(사람을 모셔다 드리는 길이면 내려올 때 빈 수레다. 그건 맞다. 그런데 모셔다 드린 사람 소식은 한 번도 내려온 적이 없다.)",{"thought":True}),
        (None,"은호의 견습 구슬이 저울 옆에서 장부를 넘기고 있었다."),
        ("resident_guseul","사장님 장부요? 그건 손님한테 보여 주는 거고요. ……진짜는 따로 있어요.")],"cv:market")
    $ r13_grant(["V02"],"장터에서 은호가 흔든 빌림 쪽지")
    menu:
        "수레 명단의 엄마 이름을 보여 준다":
            call r13_lines([("dad","이 명단 맨 끝이 제 아내입니다. 이 수레가 정말 보호소로 가는지 알아야 합니다."),
                (None,"구슬이 계산대 밑에서 얇은 장부를 꺼내 왔다."),
                ("resident_guseul","수레 값은 회관이 아니라 여관에서 나와요. 할머니가 직접 오세요. 해마다 이맘때요."),
                ("resident_guseul","네 번이에요. 네 겨울. 날짜도 똑같고, 늘 편도예요.")],"cv:guseul")
            $ r13_grant(["V03"],"구슬이 꺼내 온 은호의 다른 장부")
        "빌림 쪽지를 보여 준다":
            call r13_lines([("resident_guseul","그건 저도 봤어요. 그게 다예요.")],"cv:guseul:no")
    $ r13_tick()
    return

label r13_cv_store:
    $ r13_flag("cv_store")
    call r13_scene("r13_store","창고 뒷길","quiet")
    call r13_lines([("resident_mungchi","……뒷길 있어요. 장작 넣는 쪽문이요. 마님은 몰라요.")],"cv:store")
    menu:
        "수레의 결박 끈 이야기를 한다":
            call r13_lines([("dad","저 수레엔 담요가 한 장도 없습니다. 끈만 있어요."),
                ("resident_mungchi","……보호소 가는데 담요도 없어요? 거기 추운 데예요?"),
                (None,"쪽문 안쪽, 천장까지 쌓인 담요. 곡식 자루."),
                ("resident_mungchi","마흔 장이요. 제가 셌어요. 마님 식구는 넷이에요.")],"cv:store:open")
            $ r13_grant(["V04"],"뭉치가 보여 준 창고 쪽문 안쪽")
        "그냥 돌아간다":
            pass
    $ r13_tick()
    return

label r13_cv_stable:
    $ r13_flag("cv_stable")
    call r13_scene("ep_stable","마구간","quiet")
    if r13_has("siluk_handed"):
        call r13_lines([(None,"실룩은 마구간 기둥에 묶여 있었다. 수레가 떠날 때 같이 실린다."),
            ("resident_siluk","빚 대신 일꾼이랬는데, 일꾼은 보호소에 안 가지 않소?"),
            ("resident_siluk","작년에도 그 수레를 봤소. 내려올 땐 늘 빈 수레였소.")],"cv:stable:tied")
    else:
        call r13_lines([("resident_siluk","나더러 몰라고 했소. 안 몰면 애들 배급표를 뺀다고 너울이 그러더이다."),
            ("resident_siluk","작년에도 몰았소. 산길 끝까지 올라가서, 사람을 내려놓고, 끈만 다시 감아서 내려왔소."),
            ("resident_siluk","내려올 땐 늘 빈 수레였소. 보호소라는데, 거기 지붕 하나 못 봤소."),
            ("resident_siluk","나는 끄는 사람이오. 끄는 사람은 뒤를 안 보오.")],"cv:stable:driver")
    $ r13_grant(["V05"],"마구간에서 실룩에게 들은 말")
    if r13_has("siluk_debt_cleared"):
        menu:
            "“오늘은 늦게 끌어 주십시오.”":
                call r13_lines([("resident_siluk","……말이 발을 다쳤다고 하겠소. 동트기 전까진.")],"cv:stable:delay")
                $ r13_flag("cv_cart_delayed")
            "그냥 돌아간다":
                pass
    if not r13_has("cv_cart_delayed"):
        $ r13_tick()
    return

label r13_cv_hall:
    $ r13_flag("cv_hall")
    call r13_scene("ep_hall_front","회관 앞","quiet")
    call r13_lines([("resident_badook","너울 반장님이 수레 호송을 저더러 맡으라고 하셨습니다. 이게 명령서고요."),
        ("resident_badook","그런데 손님, 이상합니다. 보호소 가는 길에 결박 끈이 왜 필요합니까."),
        (None,"명령서. '보호소 이송을 명함.' 아래에 촌장의 뿔 도장. 'ㄹ'의 꼬리가 둥글게 한 바퀴 말려 있다."),
        (None,"가방에서 이 마을로 우리를 부른 초대 편지를 꺼냈다. 'ㄹ'의 꼬리가 똑같이 말려 있었다."),
        ("dad","(편지를 쓴 손이 명령서도 썼다. 그 손은 할머니다.)",{"thought":True}),
        ("resident_badook","저는 오늘 밤 이 명령을 못 따르겠습니다. 수레 앞에 서 있을 겁니다. 혼자라도요.")],"cv:hall")
    $ r13_grant(["V06"],"바둑이가 보여 준 명령서")
    menu:
        "명령서와 초대 편지를 나란히 보여 준다" if r13_has("E01"):
            call r13_lines([("dad","이 명령서는 촌장이 쓴 게 아닙니다. 도장만 촌장 것이고, 손은 여관 할머니입니다."),
                ("dad","몸으로 막지 마십시오. 오늘 밤 회의에서 '이 명령서는 가짜'라고 말해 주십시오. 순찰대원이 말하면 사람들이 듣습니다."),
                ("resident_badook","……막는 사람이 아니라, 말하는 사람이 되라는 거군요.")],"cv:hall:witness")
            $ r13_flag("cv_badook_witness")
            if r13_has("K02"):
                call r13_lines([("guard","같이 서겠소. 그 꼬마가 약 갖다 준 날부터 빚진 기분이었소.")],"cv:hall:dolmok")
                $ r13_flag("cv_badook_safe")
        "수레 명단을 보여 준다":
            call r13_lines([("resident_badook","명단이 이상한 건 저도 압니다. 그래서 막겠다는 겁니다.")],"cv:hall:list")
    $ r13_tick()
    return

label r13_cv_tea:
    $ r13_flag("cv_tea")
    call r13_scene("ep_hall_cell" if room13.get("granny_state")=="detained" else "council","13일 저녁 · 회관 아래 방" if room13.get("granny_state")=="detained" else "13일 저녁 · 여관 식당","quiet")
    call r13_lines(([(None,"회관 아래 방. 창살 너머로 할머니가 찻주전자를 들었다.")] if room13.get("granny_state")=="detained" else [(None,"여관 식당. 할머니가 찻잔 둘에 차를 따랐다. 손이 하나도 떨리지 않았다.")])+
        [("granny","앉아요. 식기 전에 마셔요. 오늘 밤은 길 테니까."),
        ("dad","명령서를 쓰셨죠."),
        ("granny","촌장 어른은 글씨가 떨려서요. 내가 대신 써 드린 지 오래예요. 해마다 그날 써요.")]+
        ([("mom","저 명단에 제 이름이 있어요."),("granny","그럼요. 아가가 말썽이니까. 옛 시설 조각을 함부로 꺼내면, 남은 것도 금방 동나요.")] if r13_has("mom_reunited") else [])+
        [(None,"……"),
        ("granny","돌이 버티려면 사람이 필요해요. 늘 그래 왔어요.")]+
        ([("daram","할머니, 보호소 따뜻해?"),("granny","그럼. 아주 따뜻해.")] if r13_cv_daram() else [])+
        [(None,"할머니의 찻잔에서 김이 났다. 할머니는 한 모금도 마시지 않았다."),
        (None,"수선집 앞에서 여니와 토리가 빨래 수레를 손보고 있었다. \"새벽마다 빨래 수레가 마을 입구로 나가요. 사람 하나는 들어가요.\""),
        (None,"종탑 위, 흰 부엉이 설이가 종 줄 옆에 앉아 있었다.")],"cv:tea")
    $ r13_grant(["V07"],"할머니에게 직접 들은 말")
    $ r13_flag("cv_laundry_cart")
    if r13_has("V03") or r13_has("V05"):
        menu:
            "설이에게 네 겨울의 수레 이야기를 한다":
                call r13_lines([("dad","이 수레는 네 해 동안 사람을 싣고 올라가서 빈 수레로 내려왔습니다. 오늘 밤은 사람들이 봐야 합니다."),
                    ("resident_seol","……네 해. 내가 이 종을 지킨 게 네 해예요."),
                    ("resident_seol","수레가 움직이면 칠게요. 딱 한 번만.")],"cv:bell")
                $ r13_flag("cv_bell")
            "종탑을 지나친다":
                pass
    $ r13_edit(period=3)
    return

label r13_cv_night:
    $ r13_flag("cv_night")
    $ r13_edit(location="square")
    call r13_scene("winter_square","13일 밤 · 광장, 수레 앞","night")
    call r13_lines([(None,"횃불이 다섯. 수레 짐칸에 굴돌 할아버지, 모모 관장, 판돌 영감이 앉아 있었다. 손목에 고리가 채워져 있었다.")]+
        ([(None,"짐칸 끝에 실룩. 고개를 숙이고 있었다.")] if r13_has("siluk_handed") else [])+
        ([(None,"사자 선생님이 출석부를 품에 안고 앉아 있었다.",{"show":"resident_teacher","pose":"collapse_attendance"})] if r13_has("teacher_on_cart") else [])+
        [("resident_guldol","보호소에도 돌이 있으려나. 손이 심심해서."),
        ("neoul","출발하오."),
        (None,"수레 앞에, 바둑이가 서 있었다.",{"show":"resident_badook","pose":"block_cart"}),
        ("resident_badook","못 갑니다. 명령서를 봤습니다. 이 수레는 보호소에 안 갑니다.",{"pose":"block_cart"})],"cv:night:open")
    if r13_has("cv_bell"):
        call r13_lines([(None,"쿵.",{"cut":"bell","music":None,"sfx":"bell10"}),(None,"종소리였다. 낮고 길게, 눈 덮인 지붕들 위로 퍼져 나갔다."),
            (None,"창문이 하나둘 열렸다. 사람들이 숄을 걸치고 광장으로 나왔다.",{"cut":None})]+([("daram","……종이 울렸어. 아빠, 종이 울렸어.")] if r13_cv_daram() else []),"cv:night:bell")
    if r13_has("cv_badook_safe"):
        call r13_lines([("resident_badook","명령서를 들고 있습니다. 이 명령서는 촌장님 글씨가 아닙니다. 회의를 엽시다."),
            ("guard","이 친구를 밀려면 나도 밀어야 할 거요."),
            (None,"순찰대원들이 서로를 보았다. 아무도 먼저 손을 뻗지 않았다.")],"cv:night:badook_safe")
    elif r13_has("cv_badook_witness"):
        call r13_lines([("neoul","밀어라."),(None,"순찰대원들이 바둑이를 밀었다. 바둑이가 얼어붙은 돌바닥에 쓰러졌다. 숨은 있다."),
            ("resident_badook","……명령서는, 가짜입니다.")],"cv:night:badook_hurt")
        $ r13_flag("badook_hurt")
    else:
        call r13_lines([("neoul","밀어라."),
            (None,"순찰대원 셋이 바둑이를 밀었다. 바둑이는 팔을 벌린 채 버텼다. 끝까지 길을 비키지 않았다."),
            (None,"누군가 세게 밀쳤다. 바둑이가 얼어붙은 돌바닥에 쓰러졌다. 다시 일어나지 않았다."),
            (None,"……"),
            (None,"눈 위에 순찰 완장이 떨어져 있었다. 한쪽 끈이 뜯겨 있었다."),
            ("guard","……이 바보. 정직한 거 말고도 재주 많았잖소.")],"cv:night:badook_dead")
        $ r13_flag("badook_dead")
    if r13_has("ws_cart_truth"):
        call r13_lines([(None,"대피소에 있던 얼굴들이 수레를 빙 둘러섰다. 보리가 맨 앞이었다. 화상 자국이 남은 손으로 수레 바퀴를 붙잡았다."),
            ("resident_bori","이 수레 어디 가는지, 오늘은 여기서 말하시오.")],"cv:night:crowd")
    call r13_lines([(None,"회관 쪽에서 뿔이 촌장이 지팡이를 짚고 걸어왔다. 사람들이 길을 열어 주었다."),
        ("resident_ppul","소란 피울 일이 아니오. 아픈 이들을 보호소에 모시는 길이오."),
        ("resident_ppul","말할 게 있으면 지금 하시오. 여기, 다 보는 앞에서.")],"cv:night:ppul")
    call r13_debate_run("Q6")
    if _return:
        call r13_cv_decision
    else:
        call r13_lines([("resident_ppul","말은 다 들었소. 수레는 떠나오."),(None,"새벽, 수레가 산길로 올라갔다.")],"cv:night:fail")
        call r13_cv_cart_left
    $ r13_cv_preparations()
    call r13_lines([(None,"(그림책) 그 사람들은 다시 돌아오지 않았어요.",{"book":"U06-opening"})]+
        ([(None,"(그림책) 이번엔 마을 사람들이 피리를 꺾었어요.",{"book":"U06-ending"})] if r13_has("cart_stopped") else [(None,"(그림책) 한 아이만 늦게 걸어서, 문이 닫히기 전에 돌아왔어요.")] if r13_has("cv_family_only") else [])+
        ([("daram","……아빠. 피리 부는 아저씨는 누가 불라고 해서 분 거야?")] if r13_cv_daram() else []),"cv:night:book")
    $ r13_flag("cv_done")
    return

label r13_cv_decision:
    $ _cv_menu=[("수레를 어떻게 할까?",None),("수레를 멈춘다","stop"),("명단을 광장에 공개한다","publish")]
    if r13_has("cv_laundry_cart"):
        $ _cv_menu.append(("가족만 빨래 수레로 뺀다","family"))
    if room13.get("trial_result")=="culprit_proven":
        $ _cv_menu.append(("명령서를 쓴 사람을 세운다","granny"))
    $ _cv_pick=renpy.display_menu(_cv_menu)
    if _cv_pick in ("stop","granny"):
        call r13_lines([(None,"촌장이 지팡이로 수레 바퀴를 두드렸다."),("resident_ppul","……내리시오."),
            (None,"고리가 하나씩 풀렸다. 굴돌 할아버지가 끌을 주머니에 넣었다. 판돌 영감이 손목을 문질렀다.")],"cv:decision:stop")
        $ r13_flag("cart_stopped")
        if _cv_pick=="granny":
            call r13_lines([("resident_ppul","……그건 내일, 산에서 하시오. 할멈도 올라갈 거요.")],"cv:decision:granny")
            $ r13_flag("cv_granny_tomorrow")
    elif _cv_pick=="publish":
        call r13_lines([("mom","……모과. 판돌의 아내. 보낸 사람, 너울."),
            (None,"엄마는 읽기를 멈추지 않았다. 이름이 하나씩 불릴 때마다 사람들이 한 걸음씩 다가왔다."),
            ("resident_bori","너울. 네가 실었구나. 다 네가."),
            ("neoul","나는 명령서대로 했소! 명령서대로!"),
            (None,"누가 먼저 손을 뻗었는지는 아무도 몰랐다. 너울이 사람들 사이로 끌려 들어갔다. 횃불이 흔들렸다."),
            ("mom","그만해요! 그만…….")]+([("daram","아빠, 우리가 이긴 거야?"),("dad","…….")] if r13_cv_daram() else []),"cv:decision:publish")
        $ r13_flag("cart_stopped","neoul_gone")
    else:
        call r13_lines([(None,"빨래 수레 덮개 아래로 엄마가 몸을 숨겼다.")]+
            ([(None,"여니가 판돌 영감의 손을 끌었다. \"한 사람 말고, 이분도요. 제 단골이에요.\"")] if r13_has("ws_cart_truth") else [])+
            [(None,"새벽, 수레가 산길로 올라갔다.")]+([("daram","아빠, 할아버지들은?"),("dad","…….")] if r13_cv_daram() else []),"cv:decision:family")
        $ r13_flag("cv_family_only")
        call r13_cv_cart_left
    return

label r13_cv_cart_left:
    $ r13_flag("cart_left","guldol_dead","momo_dead")
    if not (r13_has("cv_family_only") and r13_has("ws_cart_truth")):
        $ r13_flag("pandol_dead")
    if r13_has("siluk_handed"):
        $ r13_flag("siluk_dead")
    if r13_has("teacher_on_cart"):
        $ r13_flag("teacher_dead")
    return

# ---- 14일 제단: 기존 r13_finale의 제단 결판 앞에 들어간다 ----
label r13_cv_altar:
    if r13_has("cv_altar"):
        return
    $ r13_flag("cv_altar")
    # 13일 밤 광장에 가지 않고 잠들었다면 수레는 새벽에 떠났다.
    if not r13_has("cv_night"):
        $ r13_flag("cv_night","cv_skipped")
        call r13_cv_cart_left
    $ r13_cv_preparations()
    call r13_lines([(None,"(그림책) 마을 한가운데 금으로 덮인 왕자 동상이 서 있었어요.",{"book":"U07-opening"}),
        (None,"(그림책) 다 내주고 잿빛이 된 왕자 발밑에서, 제비는 잠들었어요.")]+
        ([("resident_tosil","……이거. 할머니가 맨날 읽어 주던 거야. 너 줄라고 가져왔어.",{"pose":"hold_storybook"}),
          ("daram","제비 왜 남쪽에 안 갔어? 추운데."),
          ("resident_tosil","……왕자가 혼자 있을까 봐.")] if r13_cv_daram() else []),"cv:altar:book")
    if r13_has("cart_left"):
        call r13_lines([(None,"돌 앞에 사람들이 앉아 있었다. 손목 끈은 풀리지 않은 채였다. 모두 돌 쪽을 보고 있었다."),
            (None,"굴돌 할아버지의 끌이 눈 위에 떨어져 있었다. 돌에 새 손자국 하나가 아주 얕게 파여 있었다.")]+
            ([("daram","……할아버지 손이 심심하댔잖아.")] if r13_cv_daram() else []),"cv:altar:cart")
    call r13_lines([(None,"돌 표면을 보았다. 손자국이었다. 위에서 아래까지, 겹겹이. 어른 손. 굽은 노인 손. 그리고 아주 작은 손.")]+
        ([("daram","이거 내 손이랑 똑같아."),
          (None,"다람이 작은 자국 위에 손을 얹었다. 손바닥 아래에서 돌이 아주 조금 따뜻해졌다.",{"cut":"U23-small-handprint"}),
          ("daram","어? 따뜻해졌어. 내 손 있는 데만."),
          (None,"다람이 손을 뗐다. 손바닥이 조금 차가웠다. 그뿐이었다.",{"cut":None}),
          ("daram","차가워. 근데 괜찮아.")] if r13_cv_daram() else [])+
        [("mom","……사람 온기였어. 돌을 데우는 건."),
        ("mom","옛날 사람들은 여기 와서 손을 얹었던 거야. 다 같이. 데워지면 손을 떼고 내려갔어."),
        ("mom","그래서 손자국이 이렇게 많은 거야. 죽은 사람 손이 아니라, 왔다가 내려간 사람들 손이야.",{"book":"U07-ending"})],"cv:altar:hands")
    $ r13_grant(["V08"],"제단의 작은 손자국 위에서 직접 본 것")
    if r13_has("cv_granny_tomorrow") or room13.get("granny_state")!="detained":
        call r13_lines([(None,"할머니가 돌에 손을 얹었다. 금방 뗐다. 데인 것처럼.",{"show":"granny","pose":"withdraw_hand"}),
            ("granny","손을 얹고…… 내려가면 됐다고요?"),
            ("granny","내 딸, 보미도 이름을 잊기 시작했어요. 처음엔 장 보러 가는 길을. 다음엔 토실이 이름을요."),
            ("granny","내가 여기로 데려왔어요. 이 손으로. 그 애 목도리를 여며 주고."),
            ("granny","그게 마을을 살린다고 믿어야 살 수 있었어요. 그래서 아가를 붙잡으려 했어요. 편지도 내가 썼어요."),
            ("granny","아가 방법이 맞다면, 내 딸은 죽지 않아도 됐다는 거예요."),
            (None,"……"),
            ("resident_tosil","……할머니. 여기가 산 너머야?")]+
            ([("daram","토실아. 엄마 손자국, 같이 찾자. 탐정단이잖아.")] if r13_has("ws_tosil_kept") and r13_cv_daram() else []),"cv:altar:granny")
    call r13_lines([(None,"촌장이 지팡이를 내려놓았다. 돌 아래쪽, 손가락을 쫙 벌린 작은 손자국 앞에 무릎을 꿇었다."),
        ("resident_ppul","그 애는 손을 대면 꼭 손가락을 쫙 벌렸소. 이렇게."),
        ("resident_ppul","손을 얹고 내려왔으면 됐다니. 나는 그 애를 두고 내려왔소.",{"pose":"kneel_stone"})]+
        ([("daram","할아버지, 손녀 이름 뭐야? 어젯밤엔 안 알려 줬잖아."),
          ("resident_ppul","……달래. 달래였소."),
          ("daram","그럼 내려가서 판에 적자. 여기 두고 가면 또 아무도 몰라.")] if r13_cv_daram() and r13_has("cart_stopped") else []),"cv:altar:ppul")
    if r13_cv_daram() and r13_has("cart_stopped"):
        $ r13_flag("ppul_lives","dallae_named")
    return
