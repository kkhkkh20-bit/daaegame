# New residents (owner 0.18.77): "추가 캐릭터들과 시나리오를 많이 만들어야 해. 추가 캐릭터 넣을 것이거든."
# Owner decisions (2026-10-16): all eight; dialogue and scenarios first, art later; the footsteps that
# followed mom to her forest hideout were 토실, granny's granddaughter, sent on an errand she did not
# understand. Plan: docs/NEW_CHARACTERS_PLAN_0171.md. Art request: docs/ART_REQUEST_NEW_CAST_8.md.
#   - Until their art arrives each newcomer borrows another resident's drawings with a shifted hue
#     (R13_NEW_CAST_STAND_IN). Remove an entry once the real art is imported.
#   - Scenarios run in investigation/daily life only. They leave flags, never records, and do not touch
#     the meeting/trial code (another chat develops it).
init 56 python:
    R13_NEW_CAST={
        "resident_tosil":dict(id="tosil",name="토실",work="할머니 손녀. 여관 심부름을 한다.",protects="할머니",
            activity="보온병을 두 손으로 꼭 안고 있다.",unrelated="그건 할머니한테 물어봐야 해요.",
            weekly_locations=[["inn","market","inn"],["inn","market","inn"],["inn","square","inn"],["inn","market","inn"],
                ["inn","market","inn"],["square","market","inn"],["inn","market","inn"]]),
        "resident_mulgyeol":dict(id="mulgyeol",name="물결",work="얼음 위 나루지기. 썰매 배를 끈다.",protects="강가 사람들",
            activity="굵은 밧줄을 어깨에 감아 정리한다.",unrelated="강 얘기면 몰라도 그건 잘 모르겠네요.",
            weekly_locations=[["river","river","home"],["river","river","dining"],["river","river","home"],["river","market","home"],
                ["river","river","dining"],["river","river","home"],["market","river","home"]]),
        "resident_solbang":dict(id="solbang",name="솔방울",work="숲 약초꾼. 진료소에 약초를 댄다.",protects="아픈 사람들",
            activity="바구니 속 마른 약초를 다발로 묶는다.",unrelated="약초 말고는 아는 게 별로 없어서요.",
            weekly_locations=[["forest","clinic","home"],["forest","market","home"],["forest","clinic","home"],["forest","forest","home"],
                ["forest","clinic","home"],["forest","market","home"],["forest","clinic","home"]]),
        "resident_dalgeurak":dict(id="dalgeurak",name="달그락",work="눈에 갇힌 떠돌이 행상.",protects="자기 보따리",
            activity="보따리를 펼쳐 냄비와 방울을 늘어놓는다.",unrelated="에이, 그건 장사 얘기가 아니잖소.",
            weekly_locations=[["market","market","dining"],["market","square","dining"],["market","market","dining"],["market","market","dining"],
                ["market","square","dining"],["market","market","dining"],["market","market","dining"]]),
        "resident_jongjong":dict(id="jongjong",name="종종이",work="어린 배달꾼. 슬링의 조수.",protects="배달 순서",
            activity="편지 묶음을 안고 발을 동동 구른다.",unrelated="그건 슬링 언니한테 물어봐요!",
            weekly_locations=[["post","square","home"],["post","post","home"],["post","square","home"],["post","market","home"],
                ["post","square","home"],["post","post","home"],["post","square","home"]]),
        "resident_guldol":dict(id="guldol",name="굴돌 할아버지",work="옛 돌 일꾼의 마지막 세대.",protects="옛 기억",
            activity="작은 돌을 망치로 톡톡 두드리며 귀를 기울인다.",unrelated="눈이 어두워서 그런 건 잘 못 봤소.",
            weekly_locations=[["workshop","home","home"],["workshop","square","home"],["workshop","home","home"],["workshop","workshop","home"],
                ["workshop","home","home"],["workshop","square","home"],["home","workshop","home"]]),
        "resident_hyeoni":dict(id="hyeoni",name="현이",work="떠돌이 악사. 소문을 노래로 만든다.",protects="노래 값",
            activity="현을 하나씩 튕기며 음을 맞춘다.",unrelated="그런 건 노래가 안 돼요.",
            weekly_locations=[["home","market","dining"],["square","market","dining"],["home","market","dining"],["home","square","dining"],
                ["home","market","dining"],["square","market","dining"],["home","market","dining"]]),
        "resident_kalbaram":dict(id="kalbaram",name="칼바람",work="숲 끝에 혼자 사는 사냥꾼.",protects="숲 끝 길",
            activity="덫의 이빨을 하나씩 손질한다.",unrelated="……모르오.",
            weekly_locations=[["forest","gate","home"],["forest","forest","home"],["forest","gate","home"],["forest","home","home"],
                ["forest","gate","home"],["forest","forest","home"],["forest","home","home"]]),
    }
    # Borrowed drawings until the real art arrives: (resident whose drawings are used, hue shift in degrees).
    # Sources avoid the ten redesigned residents (dev/test_npc_redesign.py) and residents usually in the same place.
    R13_NEW_CAST_STAND_IN={
        "resident_tosil":("resident_kongi",150),
        "resident_mulgyeol":("resident_somi",200),
        "resident_solbang":("resident_mungchi",90),
        "resident_dalgeurak":("resident_ubak",40),
        "resident_jongjong":("resident_tok",250),
        "resident_guldol":("resident_ttadak",300),
        "resident_hyeoni":("resident_piko",120),
        "resident_kalbaram":("resident_musoe",180),
    }
    for _r13_nc_id,_r13_nc in R13_NEW_CAST.items():
        _r13_nc=dict(_r13_nc,runtime_id=_r13_nc_id)
        ROOM13["residents"][_r13_nc_id]=_r13_nc
        # 0.18.89: a resident with real art in cast.json (dev/apply_ep_art.py) keeps it.
        if _r13_nc_id in CAST:continue
        _r13_src,_r13_hue=R13_NEW_CAST_STAND_IN[_r13_nc_id]
        CAST[_r13_nc_id]=dict((st,dict(spec)) for st,spec in CAST[_r13_src].items())
        for _r13_st,_r13_spec in CAST[_r13_nc_id].items():
            renpy.image(_r13_nc_id+" "+_r13_st,Transform(Crop(tuple(_r13_spec["crop"]),_r13_spec["file"]),
                nearest=_r13_spec.get("nearest",True),matrixcolor=HueMatrix(_r13_hue)))
    R13_GREETING_NEW_CAST={
        "resident_tosil":"아저씨가 13호실 손님이죠? 할머니가 얘기했어요.",
        "resident_mulgyeol":"얼음 위로 나오실 거면 제 발자국만 밟으세요.",
        "resident_solbang":"약초 찾으세요? 아니면 길을 잃으셨나?",
        "resident_dalgeurak":"어서 오시오! 눈 때문에 발이 묶였지만 물건은 안 묶였소.",
        "resident_jongjong":"배달 중이에요! 짧게만요!",
        "resident_guldol":"……발소리가 낯설군. 새로 온 사람이오?",
        "resident_hyeoni":"한 곡 들을래요? 오늘 소문으로 만든 거예요.",
        "resident_kalbaram":"숲 끝엔 오지 마시오. 할 말은 그것뿐이오.",
    }

init 145 python:
    R13_GREETING.update(R13_GREETING_NEW_CAST)

    def _r13_nc_topic(key,npc,title,lines,day=(2,14),need=(),flags=(),not_flags=(),period=None):
        spec=dict(npc=npc,title=title,day=list(day),need=list(need),give=[],flags=list(flags),not_flags=list(not_flags),lines=list(lines))
        if period:spec["period"]=list(period)
        ROOM13["topics"][key]=spec

    # ---- 토실 (granny's granddaughter) ----
    _r13_nc_topic("tosil:hello","resident_tosil","할머니 손녀니?",[
        ("dad","여관 할머니 손녀니?"),("resident_tosil","네. 토실이에요. 할머니가 여관 일 도우라고 해서 같이 살아요."),
        ("dad","부모님은?"),("resident_tosil","겨울엔 산 너머에서 일해요. 봄에 데리러 온대요."),
        ("resident_tosil","다람이는 몇 살이에요? 나랑 비슷해 보이는데.")],flags=["tosil_met"])
    _r13_nc_topic("tosil:granny","resident_tosil","할머니는 어떤 분이야?",[
        ("dad","할머니는 어떤 분이니?"),("resident_tosil","무섭기도 하고 다정하기도 해요. 밤에는 꼭 혼자 아래층으로 내려가세요."),
        ("dad","아래층?"),("resident_tosil","창고 쪽이요. 따라가면 혼나요. 한 번 혼났어요."),
        ("dad","(밤마다 혼자 아래로 내려간다…….)",{"thought":True})],need=["tosil_met"])
    _r13_nc_topic("tosil:forest","resident_tosil","숲에 갔던 밤 이야기",[
        ("dad","토실아, 숲에 심부름 간 게 그날이 처음이 아니었니?"),
        ("resident_tosil","……네. 처음은 아저씨네 마차가 온 날 밤이었어요. 할머니가 부인한테 따뜻한 차 갖다 드리라고, 발자국 따라가면 된다고 했어요."),
        ("dad","부인을 만났니?"),("resident_tosil","아뇨. 큰 나무 밑에서 누가 숨 쉬는 소리가 났는데, 무서워서 그냥 울었어요. 칼바람 아저씨가 여관까지 데려다줬어요."),
        ("resident_tosil","다음 날 다시 가 보니까 담요만 있고 아무도 없었어요."),
        ("resident_tosil","할머니한테 그대로 말했더니, 잘했다고 꿀떡을 줬어요. ……제가 뭘 잘못한 거예요?"),
        ("dad","아니. 토실이는 심부름을 한 것뿐이야.")],need=["tosil_errand_seen"],flags=["tosil_confessed"])

    # ---- 물결 (river ferry) ----
    _r13_nc_topic("mulgyeol:crossing","resident_mulgyeol","강 건너 길",[
        ("dad","썰매 배로 강을 건널 수 있습니까?"),("resident_mulgyeol","가까운 얼음판까지만요. 한가운데는 겨울에도 안 얼어요."),
        ("dad","그럼 강 건너 마을로는?"),("resident_mulgyeol","【봄 해빙】 전엔 못 가요. 해마다 누군가 고집부리다 빠지죠.")])
    _r13_nc_topic("mulgyeol:water","resident_mulgyeol","새벽에 물 길러 온 사람",[
        ("dad","요즘 새벽에 강에 물 길러 오는 사람이 있습니까?"),
        ("resident_mulgyeol","있었어요. 처음 보는 아주머니였는데, 꼭 해 뜨기 전에 왔다가 숲으로 갔어요."),
        ("dad","언제까지 왔습니까?"),("resident_mulgyeol","며칠 전부터 안 와요. 마지막 날엔 뒤를 자꾸 돌아보더라고요."),
        ("resident_mulgyeol","아, 그 아주머니 장갑에 【도토리】 수가 놓여 있었어요. 예뻐서 기억해요.")],need=["mulgyeol_helped"])
    _r13_nc_topic("mulgyeol:water_cold","resident_mulgyeol","새벽에 물 길러 온 사람",[
        ("dad","요즘 새벽에 강에 물 길러 오는 사람이 있습니까?"),
        ("resident_mulgyeol","……얼음에 빠졌을 때 지나가던 분이죠? 그때 좀 잡아 주지 그랬어요."),
        ("resident_mulgyeol","처음 보는 아주머니가 해 뜨기 전에 왔다가 숲으로 가곤 했어요. 그 이상은 몰라요.")],need=["mulgyeol_fell"],not_flags=["mulgyeol_helped"])

    # ---- 솔방울 (herbalist) ----
    _r13_nc_topic("solbang:herbs","resident_solbang","약초 이야기",[
        ("dad","진료소 약초는 전부 숲에서 납니까?"),("resident_solbang","대부분요. 눈 밑에 숨은 걸 찾아야 해서 손이 많이 가요."),
        ("resident_solbang","요즘은 아픈 사람이 늘어서 숲 안쪽까지 들어가야 해요.")])
    _r13_nc_topic("solbang:musoe","resident_solbang","무쇠 할아버지 약",[
        ("dad","무쇠 할아버지 약은 잘 지어졌습니까?"),
        ("resident_solbang","그날 캔 뿌리로 사흘 치는 됐어요. 그다음은 눈이 얼마나 오느냐에 달렸죠."),
        ("resident_solbang","약초가 떨어질 때마다 숲 안쪽까지 가야 해요. 그때마다 길 표식 천이 하나씩 줄어 있어요. 누가 떼 가는 건지.")],need=["solbang_helped"])

    # ---- 달그락 (stranded peddler) ----
    _r13_nc_topic("dalgeurak:who","resident_dalgeurak","어디서 오셨습니까?",[
        ("dad","어디서 오셨습니까?"),("resident_dalgeurak","고개 너머 장터를 도는 행상이오. 첫눈 오던 날 짐수레 바퀴가 부러져서 이 마을에 발이 묶였지."),
        ("dad","고개는 넘을 수 있지 않습니까? 저희는 마차로 왔는데요."),("resident_dalgeurak","빈 마차는 겨우 지나가오. 내 짐을 지고 걸어서는 못 넘어. 까로 양반 마차 고쳐지면 짐을 실어 달라고 해 볼 참이오."),
        ("dad","여관에 묵으십니까?"),("resident_dalgeurak","식당 구석 자리를 얻었소. 할머니가 물건값으로 숙박비를 깎아 줬지.")])
    _r13_nc_topic("dalgeurak:eunho","resident_dalgeurak","은호 사장과의 거래",[
        ("dad","은호 사장과는 거래하십니까?"),("resident_dalgeurak","은호 사장은 내 물건을 반값에 사서 제값에 팔고 싶어 하지."),
        ("resident_dalgeurak","그런데 요즘 은호 사장이 나한테 판 냄비 하나가 진료소 것이더구먼. 바닥에 진료소 표시가 있었소."),
        ("dad","(창고에서 사라진 물건이 행상 손을 거쳐 돌고 있다…….)",{"thought":True})],day=(3,14))

    # ---- 종종이 (young courier) ----
    _r13_nc_topic("jongjong:work","resident_jongjong","배달 일은 힘들지 않니?",[
        ("dad","배달 일은 힘들지 않니?"),("resident_jongjong","하나도요! 슬링 언니가 순서만 정해 주면 저는 뛰기만 하면 돼요."),
        ("resident_jongjong","대신 봉투는 절대 열면 안 돼요. 열면 해고래요.")])
    _r13_nc_topic("jongjong:envelope","resident_jongjong","여관 할머니가 맡긴 봉투",[
        ("dad","혹시 여관 할머니가 맡긴 봉투를 부친 적 있니?"),
        ("resident_jongjong","있어요! 눈 오기 전에요. 할머니가 직접 우체국까지 오시기 힘들다고 저한테 줬어요."),
        ("dad","봉투에 뭐가 그려져 있었니?"),("resident_jongjong","아무것도요. 그냥 하얀 봉투였어요. 받는 사람 이름만 엄청 또박또박 써 있었어요."),
        ("dad","(도토리 표식이 없는 봉투. 우리 집으로 온 그 편지다.)",{"thought":True})],need=["poc:letter_conflict"])

    # ---- 굴돌 (last of the old stone workers) ----
    _r13_nc_topic("guldol:stone","resident_guldol","옛 돌 일",[
        ("dad","예전에 돌 일을 하셨다고 들었습니다."),("resident_guldol","내 아버지 때까지는 마을에 돌 다루는 사람이 여럿 있었소."),
        ("resident_guldol","지금은 나 하나 남았지. 그나마 깨진 돌을 붙이는 정도요. 새로 만드는 법은 나도 모르오.")])
    _r13_nc_topic("guldol:works","resident_guldol","여관 아래 옛 시설",[
        ("dad","여관 아래에 돌을 만들던 시설이 있었습니다."),("resident_guldol","……결국 그걸 봤구먼."),
        ("resident_guldol","거기가 멈춘 건 지금 여관 할머니의 어머니 대요. 그분이 【룬】을 마지막으로 읽던 사람이었소."),
        ("resident_guldol","그분이 돌아가시고 나서 아무도 벽의 글을 못 읽었지. 할머니는 평생 그걸 다시 읽을 사람을 찾았소."),
        ("dad","그래서 아내가 필요했던 거군요.")],need=["ancient_found"],day=(8,14))

    # ---- 현이 (minstrel) ----
    _r13_nc_topic("hyeoni:song","resident_hyeoni","오늘의 노래를 청한다",[],day=(2,14))
    R13_TOPIC_LABELS["hyeoni:song"]="r13_hyeoni_song"

    # ---- 칼바람 (hunter at the forest's end) ----
    _r13_nc_topic("kalbaram:edge","resident_kalbaram","숲 끝에는 무엇이 있습니까?",[
        ("dad","숲 끝에는 무엇이 있습니까?"),("resident_kalbaram","절벽. 그리고 그 아래 옛 길."),
        ("dad","순찰대는 숲 끝엔 길이 없다고 하던데요."),("resident_kalbaram","겨울엔 그 말이 맞소. 눈사태가 길을 덮으니까. 봄이 돼야 다시 드러나지. 가지 마시오.")])
    # 칼바람's account of the first night is his alibi answer (systems/room13_alibi.rpy).

    # ---- mom, after reunion: who the footsteps were ----
    _r13_nc_topic("tosil:mom","mom","숲까지 따라온 발소리의 주인",[
        ("dad","숲까지 따라온 발소리 말이야. 토실이었어. 할머니 손녀."),
        ("mom","……그 아이였구나. 할머니가 차를 보낸 거야?"),
        ("dad","응. 발자국만 따라가면 된다고 했대. 아이는 아무것도 몰랐어."),
        ("mom","나는 그날 밤 무서워서 짐을 쌌는데. 그 아이도 추운 데서 혼자였겠네."),
        ("mom","다람이한테는 토실이를 미워하지 말라고 해 줘. 그 아이 잘못이 아니야.")],day=(8,14),need=["tosil_errand_seen","mom_reunited"])

    # ---- 다람이 and 토실 at night ----
    R13_NIGHT_TALKS_NEW_CAST=[
        ("night:tosil","다람이가 새 친구 이야기를 한다",lambda:r13_has("tosil_friend"),[
            ("daram","아빠, 토실이는 할머니랑 둘이 산대. 엄마 아빠는 봄에 온대."),
            ("dad","그래. 다람이랑 비슷하네. 둘 다 엄마를 기다리고."),
            ("daram","응. 그래서 과자 반의 반을 줬어. 엄마 몫은 안 건드렸어!"),
            ("dad","잘했어. 친구가 생겼네.")]),
        ("night:tosil_hurt","다람이가 토실이 이야기를 꺼낸다",lambda:r13_has("tosil_errand_seen") and r13_has("tosil_friend"),[
            ("daram","아빠. 엄마를 따라간 게 토실이였다며."),
            ("dad","응. 할머니가 시켜서 간 거래. 토실이는 무슨 일인지 몰랐어."),
            ("daram","……그래도 토실이 때문에 엄마가 또 도망간 거잖아. 토실이 미워해야 해?"),
            ("dad","아니. 토실이도 엄마를 기다리는 아이야. 다람이처럼."),
            ("daram","……응. 그럼 내일도 과자 반의 반 줄 거야. 대신 엄마 얘기는 안 할 거야.")]),
    ]
    for _k,_t,_c,_l in R13_NIGHT_TALKS_NEW_CAST:
        ROOM13["topics"][_k]=dict(npc="daram",title=_t,day=[2,14],need=["lodging"],give=[],flags=[],lines=list(_l))
        R13_NIGHT_TALK_COND[_k]=_c

    # ---- scenario offers: press the person to step in; passing by leaves the look-away outcome ----
    R13_EVENT_OFFERS.update({
        "r13_nc_tosil_friend":("장터 구석에서 토실이 다람이 과자 봉지를 힐끔거린다",[],""),
        "r13_nc_mulgyeol_ice":("강가 얼음판에서 썰매 배가 기우뚱한다",["mulgyeol_fell"],"강가에서 나루지기가 얼음에 빠질 뻔했다는 말을 들었다."),
        "r13_nc_solbang_herbs":("숲 입구에서 솔방울이 빈 바구니를 들고 서성인다",[],""),
        "r13_nc_dalgeurak_news":("장터에서 행상이 바깥 소식을 한 냥에 판다며 외친다",[],""),
    })
    R13_OFFER_ACTORS.update({
        "r13_nc_tosil_friend":("resident_tosil",None),
        "r13_nc_mulgyeol_ice":("resident_mulgyeol",None),
        "r13_nc_solbang_herbs":("resident_solbang",None),
        "r13_nc_dalgeurak_news":("resident_dalgeurak",None),
    })

    def r13_hyeoni_verses():
        """Verses from what the village is talking about today (flags only; no new facts)."""
        s=store.room13;verses=[]
        if s.get("case_state")=="occurred":verses.append("「열세 번째 방 문이 부서진 밤, 여관 굴뚝만 연기를 뿜었네」")
        if r13_has("ev_e_done") or r13_has("bori_punished"):verses.append("「빈 수레 끌고 간 보리네, 배급표엔 이름이 없었다네」")
        if r13_has("tools_sold") or r13_has("pages_sold"):verses.append("「은호네 자루는 날마다 불룩, 누구 물건인지 묻지 마오」")
        if r13_has("mom_hideout_found"):verses.append("「숲 깊은 뿌리 밑에 꺼진 초 하나, 누가 두고 갔나」")
        if r13_has("w2_bell_silent") or r13_has("ep3_bell_seen"):verses.append("「종이 울리지 않은 밤, 두 집 불이 꺼졌네」")
        if not verses:verses.append("「눈은 쌓이고 마차는 안 오고, 고개 너머 봄은 아직 멀어라」")
        return verses[-2:]

label r13_hyeoni_song:
    $ _hy_verses=r13_hyeoni_verses()
    call r13_lines([("resident_hyeoni","그럼 오늘 소문으로 한 곡.")]+[("resident_hyeoni",v) for v in _hy_verses]+[
        ("dad","(노래는 오늘 마을에 퍼진 말을 그대로 따라간다.)",{"thought":True})],"hyeoni:song:%d:%d"%(room13["day"],room13["period"]))
    return

label r13_new_cast_events:
    $ _nc_d,_nc_p,_nc_loc=room13["day"],min(room13["period"],2),room13["location"]
    # Event plan: docs/EVENT_DESIGN_NEW_CAST.md (N1-N5).
    if (2<=_nc_d<=R13_CASE_DAY or r13_tl(9)<=_nc_d<=r13_tl(12)) and _nc_p==1 and _nc_loc=="market" and not r13_has("tosil_friend") and room13.get("daram_state") in ("with_dad","rescued"):
        $ r13_offer("r13_nc_tosil_friend")
    if r13_tl(9)<=_nc_d<=r13_tl(11) and _nc_p==2 and _nc_loc=="inn" and not r13_has("tosil_errand_done") and room13.get("granny_state")!="detained" and not r13_has("mom_reunited"):
        call r13_nc_tosil_errand
    if 2<=_nc_d<=R13_TRIAL_DAY and _nc_p==0 and _nc_loc=="river" and not r13_has("mulgyeol_helped") and not r13_has("mulgyeol_fell"):
        $ r13_offer("r13_nc_mulgyeol_ice")
    if _nc_d in (4,6) and _nc_p==0 and _nc_loc=="forest" and not r13_has("solbang_helped"):
        $ r13_offer("r13_nc_solbang_herbs")
    if _nc_d in (3,r13_tl(9),r13_tl(11)+1) and _nc_p==0 and _nc_loc=="market" and not r13_has("outside_news_bought"):
        $ r13_offer("r13_nc_dalgeurak_news")
    return

label r13_nc_tosil_friend:
    call r13_ev_here("calm")
    call r13_lines([(None,"장터 구석, 토실이 다람이 손에 든 과자 봉지를 힐끔힐끔 본다."),
        ("resident_tosil","……그거 맛있어?"),
        ("daram","응. 근데 반은 엄마 거야. 엄마 만나면 줄 거야.",{"expression":"flustered"}),
        ("resident_tosil","너희 엄마도 없어? 우리 엄마도 봄에 와."),
        (None,"다람이가 잠깐 망설이더니 자기 몫에서 반을 뚝 떼어 내밀었다."),
        ("daram","그럼 이건 내 몫에서 반. 엄마 몫은 안 돼.",{"expression":"joy"}),
        ("resident_tosil","……고마워. 나는 토실이야. 할머니 손녀."),
        ("daram","나는 다람이! 13호실에 있어.",{"expression":"joy"}),
        ("dad","(다람이에게 이 마을에서 처음 생긴 친구다.)",{"thought":True})],"newcast:tosil:friend")
    $ r13_flag("tosil_friend","tosil_met")
    return

label r13_nc_tosil_errand:
    $ r13_flag("tosil_errand_done")
    call r13_lines([(None,"해가 진 뒤, 접수대 뒤에서 할머니가 토실에게 보온병을 쥐여 주었다."),
        ("granny","큰 나무 밑에 다시 가 보렴. 부인이 돌아왔으면 이거 드리고, 아무 말 말고 바로 와."),
        (None,"토실이 여관 뒷문으로 빠져나가 숲 쪽으로 걸어갔다.")],"newcast:tosil:errand:open")
    menu:
        "몰래 따라가 본다":
            call r13_lines([(None,"토실은 큰 전나무 뿌리 앞에서 멈춰 서서 구멍 안을 들여다보았다. 안은 비어 있었다."),
                ("resident_tosil","……오늘도 없네. 저번처럼."),
                ("dad","토실아, 이 밤에 여기서 뭐 하니?"),
                ("resident_tosil","아, 아저씨! 할머니가 부인이 돌아왔나 보고 오래요. 처음 왔을 땐 발자국만 따라가면 된다고 했는데."),
                ("dad","(할머니는 아이를 시켜 아내를 쫓게 했다. 할머니는 지금도 아내를 찾고 있다.)",{"thought":True}),
                ("dad","오늘은 너무 깜깜해. 같이 돌아가자. 할머니한테는 아무도 없었다고만 하렴.")],"newcast:tosil:errand:follow")
            $ r13_flag("tosil_errand_seen")
        "그냥 둔다":
            call r13_lines([("dad","(아이 혼자 숲에……. 하지만 지금 따라가면 할머니 눈에 띌 수도 있다.)",{"thought":True})],"newcast:tosil:errand:stay")
    return

label r13_nc_mulgyeol_ice:
    call r13_ev_here("calm")
    call r13_lines([(None,"쩍, 하는 소리와 함께 썰매 배 앞의 얼음이 갈라졌다. 물결이 밧줄을 붙잡은 채 미끄러진다."),
        ("resident_mulgyeol","밧줄! 밧줄 끝 좀 잡아 줘요!")],"newcast:mulgyeol:ice:open")
    menu:
        "밧줄을 잡아당긴다":
            call r13_lines([(None,"밧줄을 힘껏 당기자 썰매 배가 단단한 얼음 위로 끌려 올라왔다."),
                ("resident_mulgyeol","……휴. 살았다. 고마워요. 이 은혜는 강가 일로 갚을게요."),
                ("resident_mulgyeol","궁금한 거 있으면 물어봐요. 강가에서 본 건 다 말해 줄게요.")],"newcast:mulgyeol:ice:pull")
            $ r13_flag("mulgyeol_helped")
        "사람을 부르러 간다":
            call r13_lines([(None,"꽥순을 데리고 돌아왔을 때 물결은 혼자 기어 올라와 젖은 몸을 떨고 있었다."),
                ("resident_mulgyeol","……다음엔 그냥 밧줄을 잡아 줘요. 그래도 와 줘서 고마워요.")],"newcast:mulgyeol:ice:call")
            $ r13_flag("mulgyeol_helped","mulgyeol_cold")
    return

label r13_nc_solbang_herbs:
    call r13_ev_here("calm")
    call r13_lines([("resident_solbang","진료소 약초가 다 떨어졌어요. 숲 안쪽까지 가야 하는데, 혼자는 길 표식 천을 다 못 봐서요."),
        ("dad","같이 가 드리겠습니다.")],"newcast:solbang:open")
    call r13_lines([(None,"붉은 표식 천을 따라 숲 안쪽으로 들어갔다. 솔방울이 눈을 헤치고 마른 뿌리를 캐낸다."),
        (None,"돌아오는 길, 큰 전나무 뿌리 쪽 눈이 유난히 단단하게 다져져 있었다."),
        ("resident_solbang","저기는 요즘 누가 자꾸 드나드나 봐요. 동물 자국은 아니고요."),
        ("resident_solbang","덕분에 약초를 넉넉히 캤어요. 무쇠 할아버지 약도 이걸로 지을 수 있어요.")],"newcast:solbang:walk")
    $ r13_flag("solbang_helped")
    return

label r13_nc_dalgeurak_news:
    call r13_ev_here("calm")
    call r13_lines([("resident_dalgeurak","바깥 소식이오, 바깥 소식! 한 냥이면 고개 너머 이야기를 들려드리지!")],"newcast:dalgeurak:open")
    menu:
        "한 냥을 내고 듣는다" if r13_cash_now()>=1:
            $ r13_cash(-1,"행상에게 바깥 소식 값")
            call r13_lines([("resident_dalgeurak","고개 마차는 눈이 녹아야 와. 내 짐작엔 【보름째】나 돼야 할 거요."),
                ("resident_dalgeurak","그리고 고개 아래 마을에선 이 마을 이름만 나와도 고개를 돌리더이다. 해마다 사람이 줄어든다고."),
                ("dad","(바깥에서도 이 마을이 이상하다는 걸 알고 있었다.)",{"thought":True})],"newcast:dalgeurak:paid")
            $ r13_flag("outside_news_bought")
        "지금은 됐다":
            call r13_lines([("resident_dalgeurak","에이, 소식은 상하지도 않는데. 다음에 또 오시오.")],"newcast:dalgeurak:pass")
    return
