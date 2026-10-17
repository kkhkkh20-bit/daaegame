# 에피소드 ② 「다람 탐정단 — 처마 밑의 이빨 자국」 (4일 밤 ~ 6일 아침). 대본: docs/EPISODE2_SCRIPT.md
#   4일 밤: 입구에서 경비 돌목이 어둠 속에서 물린다. 너울은 처마 밑의 밤이를 지목한다(아빠 시점).
#   5일: 아빠는 하루 종일 엄마 소식을 알아보러 나가고, 플레이어는 다람이 된다(room13["pov"]="daram").
#        다람의 얼굴은 화면에 나오지 않고, 아빠의 얼굴이 보이며, 생각 표시는 다람의 생각이다.
#        해 지기 전까지 걸음 다섯 번. 어디를 먼저 갈지, 무엇을 보여 줄지가 단서를 정한다.
#   5일 저녁: 광장 회의(의장 바둑이). 다람이 직접 말한다. 회의 Q2.
#   5일 밤: 무쇠 할아버지는 솜이를 못 알아보는 날이 오기 전에 스스로 얼음 강으로 간다.
#   예전 큰 사건 1 「처마 밑의 밤이」(systems/room13_episodes.rpy)는 이 에피소드로 바뀐다.
#   깃발 접두사 kd_ (옛 사건 깃발 ep1_*, 등 도둑 lt_*와 겹치지 않게).
init 153 python:
    for _key,_name,_est,_not in (
        ("K01","콩이의 소문","장터에서 콩이가 \"밤이가 물었대\"라고 했다. 그래서 무슨 뜻? 콩이는 직접 본 게 아니라 창고 형들에게 들은 말이다.","누가 처음 그 말을 했는지는 모른다."),
        ("K02","돌목의 말","돌목 아저씨: \"어두웠지만, 키가 내 어깨쯤 되는 사람이었어. 손이 아주 차가웠고.\" 그래서 무슨 뜻? 문 사람은 밤이보다 훨씬 크다.","얼굴은 못 봤다."),
        ("K03","밤이의 말","밤이: \"그날 밤 나는 처마 위에서 별을 봤어. 할아버지 같은 사람이 신발도 안 신고 비틀비틀 입구로 갔어.\" 그래서 무슨 뜻? 밤이는 입구에 없었다.","그 할아버지가 누구인지는 밤이도 모른다."),
        ("K04","큰 맨발 발자국","지붕에서 본 눈밭. 어른 크기의 맨발 발자국이 입구에서 솜이네 집 뒷문으로 이어진다. 그래서 무슨 뜻? 신발 없는 어른이 입구에서 솜이네 집으로 갔다.","발자국만으로 누구인지는 정할 수 없다."),
        ("K05","손바닥의 이름","무쇠 할아버지 손바닥에 '솜이'라는 글자가 빽빽하다. 그래서 무슨 뜻? 할아버지는 손녀 이름을 잊지 않으려고 적어 두었다. 이름을 잊어 가는 중이다.","할아버지가 일부러 사람을 물었다는 뜻은 아니다."),
        ("K06","할아버지의 말","할아버지가 바로 앞의 솜이에게 \"너희, 우리 손녀랑 닮았구나\"라고 했다. 그래서 무슨 뜻? 할아버지는 가족을 못 알아볼 때가 있다.","언제부터 그랬는지는 솜이만 안다."),
        ("K07","강 이야기","할아버지: \"강물 소리가 듣기 좋구나. 할멈이 거기 있단다. 거기서 기다린대.\" 그래서 무슨 뜻? 할아버지가 강으로 갈지도 모른다.","언제 갈지는 모른다."),
        ("K08","네로의 이름표","아랫길 천막의 네로 아저씨가 쥐여 준 낡은 천 조각. 삐뚤한 바느질로 이름이 적혀 있다. \"이름은 잃어버리면 안 된다.\"","누구 이름인지는 아직 모른다."),
        # 0.18.90 동물 특징으로 알리바이 확인: 박쥐는 날 수 있지만, 날아오르면 날개가 눈을 쓴다.
        ("K09","처마 위 눈자리","지붕에서 본 처마 위. 밤이가 앉았던 자리 둘레는 쓸리지 않았고, 발톱 자국은 기둥을 타고 처마 밑으로만 내려간다. 박쥐가 날아오르면 날개 밑의 눈이 부채꼴로 쓸린다. 그날 밤 뒤로 눈은 오지 않았다. 그래서 무슨 뜻? 밤이는 그날 밤 처마에서 날아 입구로 가지 않았다.","밤이가 그 자리에 언제부터 있었는지는 모른다."),
    ):
        ROOM13["evidence"][_key]=dict(id=_key,name=_name,kind="기록",establishes=_est,does_not_establish=_not,scenes=[],current_run_only=True,retained_on_show=True)
    R13_RECORD_SHORT.update(K01="콩이의 소문",K02="어깨 높이",K03="처마 위의 밤이",K04="큰 맨발",K05="손바닥의 이름",K06="손녀랑 닮았구나",K07="강 이야기",K08="네로의 이름표",K09="처마 위 눈자리")

    # 담요는 사건 전에도 밤이에게 건넬 수 있다(②의 지름길).
    R13_SHOP["blanket"]=dict(R13_SHOP["blanket"],day=(2,13),case=False,_tl=True)

    def r13_pov_packet(packet):
        """In Daram's episode the engine's stock "dad" thoughts are Daram's thoughts."""
        if r13_viewpoint()=="daram" and packet and packet[0]=="dad" and len(packet)>2 and isinstance(packet[2],dict) and packet[2].get("thought"):
            return ("daram",)+tuple(packet[1:])
        return packet

    # ---- 회의 Q2 (광장, 의장 바둑이, 다람이 말한다) ----
    R13_DEBATE_SEATS["ep2"]=["resident_badook","guard","resident_kongi","resident_tosil","resident_somi","resident_nero"]
    R13_DEBATE_STANCE["ep2"]=("밤이를 의심","모르겠다","밤이를 믿는다")
    R13_EP_MEETING_PLACE["ep2"]="winter_square"
    R13_EP_MEETING_HEADER["ep2"]="광장 회의 · 5일째"
    R13_DEBATE["Q2"]=dict(title="입구에서 돌목을 문 사람",session="ep2",chair="resident_badook",
        statements=[
            dict(id="s1",who="neoul",text="다들 【밤이가 물었다】고 하오.",
                accept=["K01"],
                broken_by={"K01":[("daram","콩이야, 너 그거 봤어? 탐정단 규칙. 본 것만 말하기."),
                    ("resident_kongi","……저, 본 거 아니에요. 들은 거예요."),(None,"사람들이 웅성거렸다.")]},
                hint="그 말을 처음 한 사람은 직접 봤을까?",
                wrong=("neoul","그게 소문과 무슨 상관이오?")),
            dict(id="s2",who="neoul",text="이빨 자국을 보면 【아이 짓】이오.",
                accept=["K02"],
                broken_by={"K02":[("daram","돌목 아저씨가 그랬어. 키가 자기 어깨쯤이었대."),
                    ("resident_badook","어깨 높이면 밤이 키로는 안 닿습니다."),("neoul","……그럼 날아와서 물었을 거요. 박쥐니까.")]},
                hint="물린 사람이 기억하는 키.",
                wrong=("neoul","그게 아이가 아니라는 증거요?")),
            dict(id="s2f",who="neoul",text="박쥐는 【날 수 있소】. 처마에서 입구까지는 한 번 날면 그만이오.",
                accept=["K09"],
                broken_by={"K09":[("daram","밤이가 날아오르면 날개 밑의 눈이 부채꼴로 쓸려. 근데 그날 밤 밤이 자리는 하나도 안 쓸렸어."),
                    ("daram","발톱 자국도 기둥을 타고 처마 밑으로만 내려갔어. 입구 쪽으로는 안 갔어."),
                    ("resident_badook","그날 밤 뒤로 눈은 오지 않았습니다. 날았다면 자국이 남았을 겁니다."),
                    ("neoul","……")]},
                hint="날아오르면 눈에 무엇이 남을까?",
                wrong=("neoul","그런다고 날 수 있다는 게 없어지오?")),
            dict(id="s3",who="neoul",text="밤이는 밤마다 【입구를 돌아다닌다】.",
                accept=["K03"],
                broken_by={"K03":[("daram","그날 밤 밤이는 처마 위에 있었어. 별 보고 있었대."),
                    (None,"사람들 틈에서 솜이가 떨리는 목소리로 말했다."),
                    ("resident_somi","……나도 봤어. 밤이 그날 처마 위에 있었어.")]},
                hint="그날 밤 밤이가 있던 곳.",
                wrong=("neoul","그날 밤 그 아이가 어디 있었는지 말해 보시오.")),
            dict(id="s4",who="neoul",text="맨발 자국은 신발 없는 【들짐승 아이】 것이오.",
                accept=["K04"],
                broken_by={"K04":[("daram","이건 어른 발이야. 밤이 발은 이만해."),
                    (None,"다람이 두 손으로 작은 발 모양을 만들어 보였다."),
                    ("neoul","……그럼 누구란 말이오.")]},
                hint="눈밭 발자국의 크기.",
                wrong=("neoul","발자국은 발자국이오.")),
        ],
        conclusion=dict(prompt="그럼 밤이는?",
            options=[("correct","밤이는 처마 위에 있었고, 문 사람은 어른이다"),
                ("over","콩이가 밤이에게 누명을 씌웠다"),
                ("weak","밤이가 아닐 수도 있다")],
            correct=[("resident_badook","……밤이는 아닙니다. 의장으로서 그렇게 적겠습니다."),
                ("neoul","그럼 누구란 말이오?")],
            over=("resident_kongi","나 아니야! 나는 들은 걸 판 것뿐이야!"),
            weak=("neoul","‘아닐 수도’로는 못 풀어 주오.")),
        sway=["resident_badook","guard","resident_kongi"])

    # 무쇠 할아버지는 5일 밤 강으로 간다(진료소에 맡기면 7일 새벽). 그 뒤로는 마을에 없다.
    for _k in ("musoe_after_good","musoe_after_bad"):
        if _k in ROOM13["topics"]:
            ROOM13["topics"][_k]["not_flags"]=list(ROOM13["topics"][_k].get("not_flags",[]))+["musoe_gone","kd_seori"]
    _r13_kd_where=r13_where
    def r13_where(person):
        if person=="resident_musoe":
            if r13_has("musoe_gone"):return None
            if r13_has("kd_seori"):return "clinic"
        return _r13_kd_where(person)

    R13_KD_PLACES=[
        # (키, 제목, 안내, 필요한 단서들 중 하나, 그 단서가 이미 있으면 숨김)
        ("market","장터","콩이가 소문을 판다",(),("K01",)),
        ("gate","입구","물린 돌목 아저씨",(),("K02","kd_dolmok_failed")),
        ("eaves","처마 밑","밤이가 숨어 있다",(),("K03","kd_bami_fled")),
        ("lowroad","아랫길","솜이가 자꾸 가자는 곳",(),("kd_lowroad",)),
        ("roof","지붕 위","마을이 한눈에 보인다",("K02","K03"),("K04",)),
        ("somi_home","솜이네 집","발자국이 이어진 곳",("K04",),("K05",)),
    ]

    def r13_kd_steps():
        return (store.room13 or {}).get("kd_steps",0)

    def r13_kd_menu():
        rows=[("어디로 갈까? 해 지기까지 "+"●"*r13_kd_steps()+"○"*(5-r13_kd_steps()),None)]
        for key,title,hint,need,hide in R13_KD_PLACES:
            if any(r13_has(h) for h in hide):continue
            if need and not any(r13_has(n) for n in need):continue
            rows.append((title+" — "+hint,key))
        rows.append(("광장으로 간다 (회의를 기다린다)","meeting"))
        return rows

# =========================================================
# 장면
# =========================================================
label r13_ep2_events:
    $ _kdd,_kdp=room13["day"],room13["period"]
    # 옛 큰 사건 1(밤이)의 장면과 새벽 결말은 이 에피소드로 바뀌었다.
    if not r13_has("ep1_done"):
        $ r13_flag("ep1_patrol_seen","ep1_eaves_seen","ep1_done")
    if _kdd==4 and _kdp>=2 and not r13_has("kd_bite"):
        call r13_ep2_bite
    if _kdd==5 and not r13_has("kd_done"):
        call r13_ep2_day
        return "day"
    if _kdd==7 and _kdp==0 and r13_has("kd_seori") and not r13_has("kd_clinic_note"):
        call r13_ep2_clinic_note
    return None

label r13_ep2_bite(late=False):
    # late: 4일 밤 장면을 지나쳐 5일이 되었을 때. 다람이 하루 앞에서 지난밤 일로 보여 준다.
    $ r13_flag("kd_bite")
    if not late and room13["location"] in ("room13","guestroom"):
        call r13_scene(R13_PLACES[room13["location"]][1],R13_PLACES[room13["location"]][0],"night")
        call r13_lines([("daram","아빠, 오늘은 내가 읽어 줄게."),
            (None,"(그림책) 남매는 숲에 들어가며 빵 부스러기를 떨어뜨렸어요.",{"book":"U02-opening"}),
            (None,"(그림책) 그런데 새들이 부스러기를 다 먹어 버렸어요."),
            (None,"(그림책) 남매는 별을 보고 길을 찾아 집에 돌아갔어요."),
            ("daram","나는 길 안 잃어버려. 아빠가 있으니까.")],"ep2:book")
    call r13_scene("winter","입구 · 지난밤의 비명" if late else "입구 · 어둠 속의 비명","night")
    call r13_lines([(None,("지난밤, " if late else "")+"입구 쪽에서 비명이 들렸다. 경비 돌목이 어깨를 감싸 쥐고 눈밭에 주저앉아 있었다."),
        ("guard","뭔가가…… 어둠 속에서 물었소!"),
        ("neoul","처마 밑의 그 들짐승 아이 짓이오. 날이 밝으면 찾아서 보호소로 보내겠소."),
        ("dad","보호소에서 돌아온 사람은 있습니까?"),
        ("neoul","……그건 보호소에서 알아서 할 일이오."),
        (None,"너울이 돌아서자 바둑이가 낮게 말했다."),
        ("resident_badook","저는 돌아온 사람을 본 적이 없습니다. 아직 한 번도요.")],"ep2:bite")
    if not r13_has("W1"):
        $ r13_grant(["W1"],"입구에서 너울·바둑이와 나눈 말")
    $ r13_flag("badook_doubt")
    return

label r13_ep2_day:
    # 0.19.10: 5일 아침 대사는 지난밤 물림 사건을 전제로 한다. 그 장면을 보지 못했으면 먼저 보여 준다.
    if not r13_has("kd_bite"):
        call r13_ep2_bite(late=True)
    $ r13_flag("kd_started")
    $ r13_edit(period=0,kd_steps=5)
    call r13_scene(R13_PLACES["room13"][1],"5일 아침 · 13호","calm")
    call r13_lines([("dad","오늘은 하루 종일 엄마 소식을 알아보러 다녀야 해. 나비 언니 말 잘 듣고."),
        ("daram","아빠. 밤이 잡혀가?"),
        ("dad","……모르겠다."),
        (None,"아빠가 내 탐정 모자를 고쳐 씌워 주었다."),
        ("dad","오늘은 탐정님이 마을을 맡아 줘. 위험한 데는 가지 말고."),
        (None,"문이 닫혔다.")],"ep2:morning")
    # 여기서부터 플레이어는 다람이다.
    $ r13_edit(pov="daram")
    call r13_lines([("daram","(밤이는 그런 애 아니야. 내가 알아낼 거야.)",{"thought":True})],"ep2:morning:thought")
    $ r13_edit(location="square")
    call r13_scene("winter_square","광장 · 다람 탐정단","calm")
    call r13_lines([(None,"광장 돌 앞에 토실, 콩이, 솜이가 모여 있었다."),
        ("daram","다들 들어 봐. 밤이가 잡혀갈지도 몰라. 우리가 진짜 범인을 찾자."),
        ("resident_kongi","우리가? 애들이?"),
        ("daram","응. 오늘부터 우리는 【다람 탐정단】이야."),
        (None,"주머니에서 도토리를 꺼내 하나씩 나눠 주었다."),
        ("daram","이게 탐정단 표시. 그리고 규칙이 하나 있어."),
        ("daram","【본 것만 말하기. 들은 건 '들었어'라고 말하기.】"),
        ("resident_kongi","그럼 내 장사는 어떡해."),
        ("resident_tosil","(작게) ……나도 할래."),
        (None,"솜이는 아무 말 없이 도토리를 꼭 쥐었다.")],"ep2:club")
    $ r13_flag("kids_club")
    while r13_kd_steps()>0 and not r13_has("kd_to_meeting"):
        $ _kd_pick=renpy.display_menu(r13_kd_menu())
        if _kd_pick=="meeting":
            $ r13_flag("kd_to_meeting")
        else:
            call expression "r13_ep2_at_"+_kd_pick
            $ r13_edit(period=0 if r13_kd_steps()>=3 else 1)
    $ r13_edit(period=2)
    call r13_ep2_meeting
    call r13_ep2_night
    # 같은 밤, 학교 뒤 장작 창고에 불(에피소드 ③, systems/room13_ep3_woodfire.rpy).
    call r13_wf_fire
    $ r13_flag("kd_done")
    $ r13_next_day()
    call r13_ep2_book_after
    return

label r13_ep2_step(free=False):
    if not free:
        $ r13_edit(kd_steps=max(0,r13_kd_steps()-1))
    return

label r13_ep2_at_market:
    $ r13_edit(location="market")
    call r13_scene("r13_market","장터 · 콩이의 소문","calm")
    call r13_lines([("resident_kongi","밤이가 물었다는 거? 다들 그러던데. 한 냥이면 더 알려 줄게.")],"ep2:kongi")
    menu:
        "구운 밤을 나눠 준다" if r13_has("own:snack"):
            $ r13_use_item("snack")
            call r13_lines([("resident_kongi","……공짜로 말해 줄게. 나 사실 못 봤어. 들은 거야. 창고 형들이 그러던데.")],"ep2:kongi:snack")
            $ r13_grant(["K01"],"구운 밤을 나눠 먹으며 콩이에게 들은 말")
            call r13_ep2_step(True)
        "“너 그거 봤어?”":
            call r13_lines([("resident_kongi","……아니. 들었어. 창고 형들이 그러던데."),
                ("daram","그럼 '들었어'라고 해야지. 규칙이야."),
                ("resident_kongi","치…… 알았어. 들었어.")],"ep2:kongi:ask")
            $ r13_grant(["K01"],"장터에서 콩이에게 들은 말")
            call r13_ep2_step
    return

label r13_ep2_at_gate:
    $ r13_edit(location="gate")
    call r13_scene("winter","입구 · 돌목 아저씨","calm")
    call r13_lines([("guard","애들은 저리 가시오.")],"ep2:dolmok")
    menu:
        "토실이와 같이 간다":
            call r13_lines([(None,"토실이가 할머니 심부름으로 받아 온 약병을 두 손으로 내밀었다."),
                ("resident_tosil","할머니가…… 아저씨 어깨에 바르래요."),
                ("guard","……고맙소."),
                ("guard","어두워서 얼굴은 못 봤소. 키가…… 내 어깨쯤이었나. 손이 아주 차가웠소.")],"ep2:dolmok:tosil")
            $ r13_grant(["K02"],"입구에서 돌목 아저씨에게 들은 말")
        "혼자 간다":
            call r13_lines([("guard","애들 놀이할 데가 아니오."),
                ("daram","(혼자 오면 안 되는 거였어.)",{"thought":True})],"ep2:dolmok:alone")
            $ r13_flag("kd_dolmok_failed")
    call r13_ep2_step
    return

label r13_ep2_at_eaves:
    $ r13_edit(location="inn")
    call r13_scene("ep_eaves","여관 처마 밑 · 밤이","quiet")
    if r13_has("own:blanket"):
        $ r13_use_item("blanket")
        call r13_lines([(None,"처마 밑에 아빠가 사 둔 담요를 놓자, 낡은 망토가 먼저 고개를 내밀었다."),
            ("bami","……이거 너네 아빠 거지? 따뜻하다."),
            ("bami","나 아니야. 그날 밤 나는 【처마 위】에 있었어. 별 보고 있었어."),
            ("bami","할아버지 같은 사람이 비틀비틀 입구 쪽으로 걸어갔어. 신발도 안 신고.")],"ep2:bami:blanket")
        $ r13_grant(["K03"],"처마 밑에서 밤이에게 들은 말")
        $ r13_flag("bami_club")
        call r13_ep2_step(True)
        return
    call r13_lines([(None,"여관 처마 밑에 낡은 망토가 웅크려 있었다. 다가가자 망토가 움찔했다."),
        ("bami","오지 마. 너도 나 잡으러 왔지.")],"ep2:bami")
    menu:
        "도토리를 내민다":
            call r13_lines([("daram","아니야. 이거, 탐정단 표시야. 너도 하자."),
                (None,"밤이가 한참 보다가 도토리를 받았다."),
                ("bami","나 아니야. 그날 밤 나는 【처마 위】에 있었어. 별 보고 있었어."),
                ("bami","할아버지 같은 사람이 비틀비틀 입구 쪽으로 걸어갔어. 신발도 안 신고.")],"ep2:bami:acorn")
            $ r13_grant(["K03"],"처마 밑에서 밤이에게 들은 말")
            $ r13_flag("bami_club")
        "“너 진짜 안 물었어?”":
            call r13_lines([("bami","……거봐. 너도 똑같아."),
                (None,"망토가 펄럭 하더니 지붕 너머로 사라졌다."),
                ("daram","(묻는 게 아니라 믿어 줬어야 했어.)",{"thought":True})],"ep2:bami:fled")
            $ r13_flag("kd_bami_fled")
    call r13_ep2_step
    return

label r13_ep2_at_lowroad:
    $ r13_edit(location="river")
    $ r13_flag("kd_lowroad")
    call r13_scene("r13_river","아랫길 · 천막들","quiet")
    call r13_lines([("resident_somi","비틀거리던 할아버지면…… 아랫길 천막 사람들일 거야. 거기 이상한 사람 많아."),
        (None,"솜이가 앞장서서 아랫길로 갔다. 천막 앞에서 네로 아저씨가 막아섰다."),
        ("resident_nero","애들이 올 데가 아니다."),
        (None,"네로 아저씨가 솜이를 한 번 보았다. 솜이가 눈을 피했다."),
        ("daram","(솜이가 이상해. 아까부터 자꾸 여기로만 가자고 해.)",{"thought":True}),
        (None,"돌아서는 내 손에 네로 아저씨가 낡은 천 조각 하나를 쥐여 주었다. 삐뚤한 바느질로 이름이 적혀 있었다."),
        ("resident_nero","가져가라. 이름은 잃어버리면 안 된다.")],"ep2:lowroad")
    $ r13_grant(["K08"],"아랫길 천막에서 네로 아저씨가 쥐여 준 천 조각")
    $ r13_flag("somi_misled")
    call r13_ep2_step
    return

label r13_ep2_at_roof:
    $ r13_edit(location="inn")
    call r13_scene("ep_roof_evening","여관 지붕 위","search")
    call r13_lines([("resident_somi","(머뭇거리다) ……지붕에서 보면 잘 보여."),
        (None,"솜이를 따라 여관 지붕에 올랐다. 마을이 한눈에 보였다.")]+
        ([("bami","저기. 입구에서부터 발자국.")] if r13_has("bami_club") else [(None,"입구 쪽 눈밭에 무언가 길게 이어져 있었다.")])+
        [(None,"눈밭에 맨발 발자국이 이어져 있었다. 어른 발 크기였다. 발자국은 아랫길이 아니라, 반대쪽 골목으로 꺾여 있었다."),
        ("daram","저기…… 솜이네 집 뒷문이잖아."),
        ("resident_somi","……거기 아니야."),
        (None,"발밑 처마 위 눈에 작은 자리가 하나 눌려 있었다. 거꾸로 매달린 작은 발톱 자국이 기둥을 타고 처마 밑으로 내려가 있었다. 밤이가 별을 보던 자리다.")]+
        ([("bami","나 날아오를 땐 날개가 눈을 다 쓸어. 봐."),(None,"밤이가 처마 끝을 박차자 날개 밑의 눈이 부채꼴로 쓸려 나갔다.")] if r13_has("bami_club") else
         [(None,"조금 떨어진 처마 끝에는 눈이 부채꼴로 쓸려 있었다. 아까 밤이가 날아간 자리다.")] if r13_has("kd_bami_fled") else
         [(None,"지붕 끝에서 참새들이 날아올랐다. 날개 밑의 눈이 부채꼴로 쓸려 나갔다.")])+
        [(None,"밤이가 앉았던 자리 둘레는 쓸리지 않았다. 그날 밤 뒤로 눈은 오지 않았다. 저 아래 발자국이 그대로 남은 것처럼."),
        ("daram","(그날 밤 밤이는 여기서 날아오르지 않았어.)",{"thought":True})],"ep2:roof")
    $ r13_grant(["K04","K09"],"여관 지붕에서 내려다본 눈밭과 처마")
    call r13_ep2_step
    return

label r13_ep2_at_somi_home:
    $ r13_edit(location="square")
    call r13_scene("ep_somi_home","솜이네 집","quiet")
    call r13_lines([(None,"솜이네 집은 따뜻하지 않았다. 창가에 무쇠 할아버지가 앉아 있었다. 손바닥에 잉크로 무언가가 빽빽이 적혀 있었다. 솜이. 솜이. 솜이."),
        ("resident_musoe","어이구, 꼬마 손님들이구나."),
        ("resident_musoe","(나와 솜이를 번갈아 보며) 너희, 우리 손녀랑 닮았구나."),
        (None,"아무도 말하지 않았다."),
        ("resident_somi","……할아버지. 나야. 솜이야."),
        ("resident_musoe","솜이? (손바닥을 내려다본다) 솜이…… 그래, 솜이. 우리 솜이는 어디 갔지?"),
        (None,"솜이가 울음을 터뜨렸다.")]+
        ([("resident_somi","열은 내렸어. 약도 먹었어. 근데 그 뒤로 자꾸…… 나를 몰라봐.")] if r13_has("musoe_recovering") or r13_has("musoe_herbs") else []),"ep2:home")
    $ r13_grant(["K05","K06"],"솜이네 집에서 본 것과 들은 말")
    call r13_lines([("resident_somi","말하지 마. 아무한테도. 할아버지 보호소 가면…… 보호소 간 사람은 아무도 안 돌아와."),
        ("resident_somi","그래서 네로 아저씨한테 부탁해서 밤에 천막에 숨겼어. 근데 할아버지가 자꾸 집에 오려고 해. 집을 찾다가…… 경비 아저씨가 붙잡으니까 무서워서……."),
        ("resident_tosil","(작게) ……솜이야."),
        ("daram","(밤이를 구하려면 할아버지를 말해야 해. 할아버지를 지키려면 밤이가 잡혀가.)",{"thought":True}),
        (None,"나가려는데 할아버지가 창밖을 보며 말했다."),
        ("resident_musoe","강물 소리가 듣기 좋구나. 할멈이 거기 있단다. 거기서 기다린대.")],"ep2:home:secret")
    $ r13_grant(["K07"],"무쇠 할아버지가 창밖을 보며 한 말")
    $ r13_flag("somi_secret","know_musoe_sick")
    call r13_ep2_step
    return

label r13_ep2_meeting:
    $ r13_edit(location="square")
    call r13_scene("winter_square","5일 저녁 · 광장 회의","hearing")
    call r13_lines([(None,"광장에 사람들이 모였다. 너울이 밤이의 팔을 붙들고 있었다. 바둑이가 그 옆에 서 있었다."),
        ("neoul","들짐승 아이가 경비를 물었소. 오늘 밤 보호소로 보내겠소."),
        ("daram","잠깐! 그거 이상해!"),
        ("neoul","……애들 놀이에 끼어들지 마시오."),
        ("resident_badook","들어나 보죠. 아이 말이라도.")],"ep2:meeting:open")
    call r13_debate_run("Q2")
    if _return:
        call r13_ep2_decision
    else:
        call r13_lines([("neoul","놀이는 끝났소."),
            (None,"너울이 밤이를 끌고 갔다. 밤이가 한 번 돌아보았다. 도토리를 쥔 손이 보였다."),
            ("daram","(내가 모자랐어. 밤이는 아무것도 안 했는데.)",{"thought":True})],"ep2:meeting:fail")
        $ r13_flag("bami_taken","kd_failed")
    call r13_ep2_tell_somi
    return

label r13_ep2_decision:
    $ r13_flag("bami_safe","bami_at_eaves","bami_friend","kd_solved")
    call r13_lines([(None,"모두가 나를 보았다. 사람들 틈에서 솜이가 고개를 저었다."),
        ("daram","(말하면 밤이는 살아. 말하지 않으면…….)",{"thought":True})],"ep2:decision:open")
    if r13_has("K05"):
        $ _kd_menu=[("누구라고 말할까?",None),("“……무쇠 할아버지야. 아파서 그래.”","name"),("“누군지는 몰라. 근데 밤이는 아니야.”","cover")]
        if r13_has("seori_trust"):
            $ _kd_menu.append(("“서리 선생님한테 데려가 줘.”","seori"))
    else:
        $ _kd_menu=[("누구라고 말할까?",None),("“누군지는 몰라. 근데 밤이는 아니야.”","cover")]
    $ _kd_pick=renpy.display_menu(_kd_menu)
    if _kd_pick=="name":
        call r13_lines([("daram","……무쇠 할아버지야. 아파서 그래. 일부러 그런 거 아니야."),
            ("neoul","내일 아침 그 노인을 데려가겠소."),
            (None,"밤이의 팔이 풀렸다. 솜이가 나를 노려보더니 뛰어갔다.")],"ep2:decision:name")
        $ r13_flag("kd_named","somi_angry")
    elif _kd_pick=="seori":
        call r13_lines([("daram","서리 선생님한테 데려가 줘. 보호소 말고."),
            (None,"나는 손바닥에 이름이 빽빽하던 할아버지 이야기를 했다."),
            ("resident_seori","제가 돌보겠습니다. 보호소가 아니라 진료소에서."),
            ("neoul","……검사원이 책임진다면."),
            (None,"솜이가 내 손을 잡았다. 손이 차가웠다.")],"ep2:decision:seori")
        $ r13_flag("kd_seori","somi_trust")
    else:
        call r13_lines([("daram","누군지는 몰라. 근데 밤이는 아니야."),
            ("neoul","풀어 주겠소. 앞으로 눈여겨보겠소."),
            (None,"솜이가 내 손을 꼭 잡았다.")],"ep2:decision:cover")
        $ r13_flag("kd_covered","somi_trust","bami_watched")
    call r13_lines([("bami","……너, 내 친구 해도 돼.")],"ep2:decision:friend")
    return

label r13_ep2_tell_somi:
    # 강 이야기를 솜이에게 전해야 그 밤의 작별을 볼 수 있다.
    if r13_has("K07") and not r13_has("kd_seori"):
        call r13_lines([(None,"사람들이 흩어졌다. 솜이가 광장 끝에 혼자 서 있었다.")],"ep2:after:somi")
        menu:
            "강 이야기를 솜이에게 전한다":
                call r13_lines([("daram","솜이야. 할아버지가 아까 그랬어. 강물 소리가 좋다고. 할머니가 거기서 기다린대."),
                    ("resident_somi","……할아버지가?"),
                    (None,"솜이의 얼굴이 하얘졌다.")],"ep2:after:river")
                $ r13_flag("kd_somi_warned")
            "오늘은 그냥 돌아간다":
                pass
    return

label r13_ep2_night:
    $ r13_edit(location="room13")
    call r13_scene(R13_PLACES["room13"][1],"5일 밤 · 13호","night")
    call r13_lines([("daram","아빠, 나 오늘 탐정이었어."),
        ("dad","들었어. 광장에서."),
        ("daram","근데 아빠…… 탐정은 왜 이렇게 슬퍼?"),
        (None,"아빠가 대답 대신 나를 안았다.")],"ep2:night")
    if r13_has("kd_somi_warned"):
        call r13_scene("ep_roof_night","지붕 위 · 두 불빛","night")
        call r13_lines([(None,"잠이 오지 않아 지붕으로 올라갔다. 솜이가 먼저 와 있었다."),
            ("resident_somi","할아버지가…… 집에 없어."),
            (None,"멀리 강 쪽에 작은 등불 하나가 흔들렸다. 그리고 반대쪽, 학교 뒤에서 붉은 빛이 피어올랐다.")]+
            ([("bami","(뒤에서) 저기, 불이야.")] if r13_has("bami_friend") else [])+
            [("daram","……솜이야, 강으로 가자.")],"ep2:roof:lights")
        call r13_scene("r13_river","강가 · 작별","night")
        call r13_lines([(None,"얼음 위에 할아버지가 서 있었다. 맨발이었다."),
            ("resident_somi","할아버지!"),
            (None,"할아버지가 돌아보았다. 그 눈이, 아주 잠깐, 맑았다."),
            ("resident_musoe","……솜이야. 내 손녀 솜이."),
            ("resident_musoe","솜이를 못 알아보는 날이 오기 전에, 할멈한테 가려고."),
            ("resident_somi","가지 마……."),
            ("resident_musoe","(손바닥을 펴 보이며) 봐라. 할아버지는 끝까지 우리 솜이 이름 안 잊었다."),
            (None,"할아버지가 얼음 위로 걸어갔다. 얼음이 낮게 울었다."),
            (None,"……"),
            (None,"솜이가 내 손바닥을 펴더니, 손가락으로 자기 이름을 꾹꾹 눌러 적었다."),
            ("resident_somi","너는…… 잊지 마.")],"ep2:river:farewell")
        $ r13_flag("kd_farewell_seen","musoe_gone")
    elif not r13_has("kd_seori"):
        $ r13_flag("musoe_gone","kd_shoes_only")
    # 조작이 아빠로 돌아온다.
    $ r13_edit(pov=None)
    return

label r13_ep2_book_after:
    call r13_scene(R13_PLACES["room13"][1],"6일 아침 · 13호","calm")
    if r13_has("kd_shoes_only"):
        call r13_lines([(None,"아침, 강가에 신발 한 켤레와 '솜이'가 빽빽한 종이만 남아 있었다는 말이 돌았다."),
            ("daram","……아빠. 솜이가 오늘 탐정단 안 온대.")],"ep2:after:shoes")
    elif r13_has("kd_farewell_seen"):
        call r13_lines([(None,"(그림책) 남매는 숲에 들어가며 빵 부스러기를 떨어뜨렸어요.",{"book":"U02-opening"}),
            (None,"(그림책) 그런데 새들이 부스러기를 다 먹어 버렸어요."),
            (None,"(그림책) 할아버지는 길을 잊지 않으려고, 강으로 갔어요.",{"book":"U02-ending"}),
            ("daram","……아빠. 나 손바닥에 솜이 이름 있어. 안 지울 거야.")],"ep2:after:book")
    if r13_has("kd_named"):
        call r13_lines([("daram","솜이가 나랑 말 안 해. ……그래도 내 말이 틀린 건 아니잖아."),
            ("dad","틀리지 않았어. 그래서 더 아픈 거야.")],"ep2:after:named")
    return

label r13_ep2_clinic_note:
    $ r13_flag("kd_clinic_note","musoe_gone")
    call r13_lines([(None,"진료소에서 이틀을 보낸 무쇠 할아버지가 새벽에 강으로 걸어갔다는 말이 돌았다."),
        (None,"빈 침상 위에 삐뚤한 글씨로 '고마웠소'라고 적힌 종이가 놓여 있었다.")],"ep2:clinic_note")
    return
