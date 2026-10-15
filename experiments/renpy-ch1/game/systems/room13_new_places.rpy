# New places (owner, 0.18.61): "광장 외에 4개 더 … 사냥 낚시 … 시장도 좋아", "일거리 조사 다 넣지 뭐",
# "거대 문명 맵도 생겼는데 어떻게 보여줄지, 할머니 비밀장소 대사와 다 만들어 줘".
# Art: art/new-maps-v3-20261015 (river, forest, market, ancient stone works), one picture each.
#   - 장터 (market), 강가 (river), 숲속 (forest): village places from day 2 (after lodging). Each has
#     investigation spots; the river and the forest each give a day's work; goods are bought at
#     the market stall (the old 은호 topic moves here).
#   - 돌을 만들던 옛 시설 (ancient): granny's secret place under the inn, reached in week 2 through a
#     cracked wall in the 13호 back passage. Seeing it and hearing granny/mom there is story colour
#     and motive; it grants no record and opens no proof, so trials and endings are unchanged.
# Residents whose week had no place to go ("아랫길", spare home hours, the post visits) now spend
# some of it here, which thins the post office crowd.
init 130 python:
    R13_PLACES.update(
        market=("장터","wide_market"),
        river=("강가","wide_river"),
        forest=("숲속 사냥터","wide_forest"),
        ancient=("돌을 만들던 옛 시설","wide_ancient"),
    )
    R13_MAP_LABELS.update(market="장터",river="강가",forest="숲속",ancient="옛 시설")
    R13_NEW_VILLAGE_PLACES=("market","river","forest")

    _r13_new_places=r13_places
    def r13_places():
        result=list(_r13_new_places())
        if r13_has("lodging"):result += [p for p in R13_NEW_VILLAGE_PLACES if p not in result]
        if r13_ancient_open() and "ancient" not in result:result.append("ancient")
        return result

    def r13_ancient_open():
        s=store.room13 or {}
        return bool(s.get("passage_open")) and r13_has("ancient_found")

    R13_LOCAL_CONNECTIONS["ancient"]=(("passage","계단 위로"),)
    R13_LOCAL_CONNECTIONS["passage"]=tuple(R13_LOCAL_CONNECTIONS.get("passage",()))+(("ancient","돌계단 아래로"),)

    # ---- investigation spots (world coordinates of the 2160-wide pictures) ----
    def _r13_spot(rect,text,**kw):
        spec=dict(rect=list(rect),text=text,need=["lodging"],give=[],flags=[]);spec.update(kw);return spec
    ROOM13["objects"]["market"]=dict(
        mk_stall=_r13_spot((1213,318,338,180),"말린 고기와 치즈를 늘어놓은 노점이다. 마을 사람들이 쓰는 물건도 이 노점에서 판다.",call_label="r13_market_stall"),
        mk_oven=_r13_spot((428,318,120,130),"화덕 옆 판에 빵이 식어 간다. 빵 위에 집마다 다른 무늬를 찍어 두었다."),
        mk_vegetables=_r13_spot((597,378,288,120),"채소 상자마다 값을 새긴 나무판이 꽂혀 있다. 어디서 기른 채소인지는 적혀 있지 않다."),
        mk_cloth=_r13_spot((1720,408,248,90),"두꺼운 옷감이 색깔별로 접혀 있다. 담요로 쓸 만큼 두툼하다."),
        mk_jars=_r13_spot((2009,378,151,140),"항아리 입구를 천으로 단단히 묶었다. 안에 든 것은 열어 봐야 알 수 있다."),
        mk_firewood=_r13_spot((328,477,100,120),"장작이 높이 쌓여 있다. 추위가 길어지면 이 더미부터 줄어들 것이다."),
    )
    ROOM13["objects"]["river"]=dict(
        rv_ice_edge=_r13_spot((1432,626,728,94),"물가의 얼음은 가장자리부터 얇아진다. 밟으면 갈라지는 소리가 날 것 같다."),
        rv_ice_slabs=_r13_spot((80,388,398,90),"깨진 얼음판이 물가에 밀려와 쌓였다. 누군가 얼음 구멍을 뚫은 자리일 수 있다."),
        rv_rocks=_r13_spot((398,527,437,110),"강가 바위는 눈이 녹아 미끄럽다. 그물을 말린 자국처럼 젖은 줄무늬가 남아 있다."),
        rv_reeds=_r13_spot((0,338,160,200),"마른 풀이 눈 위로 삐죽 나와 있다. 바람이 강 쪽에서 분다."),
        rv_cliffs=_r13_spot((1711,149,449,120),"건너편은 깎아지른 절벽이다. 저쪽으로 건너가는 다리는 보이지 않는다."),
        rv_water=_r13_spot((895,298,696,220),"강 한가운데는 얼지 않고 흐른다. 마차가 건널 수 있는 길은 아니다."),
    )
    ROOM13["objects"]["forest"]=dict(
        fr_roots=_r13_spot((0,400,620,200),"굵은 뿌리가 눈 위로 엉켜 있다. 발을 잘못 디디면 넘어지기 쉽다."),
        fr_bush=_r13_spot((835,278,160,120),"눈 덮인 덤불 아래로 작은 짐승이 드나든 구멍이 보인다."),
        fr_deep=_r13_spot((1114,80,200,320),"숲 안쪽은 낮에도 어둡다. 길을 표시한 천이 없으면 돌아 나오기 어렵겠다."),
        fr_branch=_r13_spot((1671,457,318,140),"눈 무게에 꺾인 가지가 쓰러져 있다. 땔감으로 쓰기엔 아직 젖어 있다."),
    )
    ROOM13["objects"]["ancient"]=dict(
        an_press=_r13_spot((180,230,340,270),"거대한 누르개 아래 각진 돌이 놓여 있다. 돌 표면의 홈무늬가 광장의 돌과 같다. 누르개에는 먼지가 두껍게 쌓였다.",need=[]),
        an_tube=_r13_spot((955,119,120,358),"유리관 속에 돌 조각이 떠 있다. 빛이 아주 천천히 밝아졌다가 어두워진다. 무엇이 빛을 채우는지는 보이지 않는다.",need=[]),
        an_small_tube=_r13_spot((1094,278,80,200),"작은 유리관은 반쯤 비어 있다. 바닥에 가라앉은 돌 조각에는 빛이 거의 없다.",need=[]),
        an_drip=_r13_spot((1730,40,239,298),"천장 장치에서 초록빛 물방울이 하나씩 떨어진다. 떨어지는 간격이 일정하지 않다.",need=[]),
        an_channel=_r13_spot((119,547,677,70),"바닥 도랑을 따라 희미한 빛이 흐른다. 빛은 계단 쪽, 마을이 있는 위쪽으로 흘러간다.",need=[]),
        an_corridor=_r13_spot((1472,318,120,200),"복도가 어둠 속으로 길게 이어진다. 등불 없이 더 들어가는 건 위험하다.",need=[]),
    )
    # The way down: a cracked wall in the back passage, noticed only in week 2.
    ROOM13["objects"].setdefault("passage",{})["crack"]=dict(rect=[1870,239,140,160],
        text="회벽이 갈라진 틈으로 따뜻한 바람이 새어 나온다.",need=["week2_started"],give=[],flags=[],call_label="r13_ancient_crack")
    R13_OBJECT_NAMES.update(mk_stall="노점",mk_oven="화덕과 빵",mk_vegetables="채소 상자",mk_cloth="옷감 더미",mk_jars="항아리",
        mk_firewood="장작 더미",rv_ice_edge="얼음 가장자리",rv_ice_slabs="물가의 얼음판",rv_rocks="강가 바위",rv_reeds="마른 풀",
        rv_cliffs="건너편 절벽",rv_water="흐르는 강물",fr_roots="얽힌 뿌리",fr_bush="눈 덮인 덤불",fr_deep="숲 안쪽",fr_branch="쓰러진 가지",
        an_press="누르개 아래의 돌",an_tube="빛나는 유리관",an_small_tube="작은 유리관",an_drip="빛이 떨어지는 장치",an_channel="바닥의 빛 도랑",
        an_corridor="멀리 이어진 복도",crack="갈라진 회벽")

    _r13_new_places_visible=r13_object_visible
    def r13_object_visible(spec):
        if spec is ROOM13["objects"].get("passage",{}).get("crack"):
            s=store.room13 or {}
            return bool(s.get("week2_started")) and s.get("day",1)>=8 and not r13_has("ancient_found")
        return _r13_new_places_visible(spec)

    # ---- residents: who spends spare hours at the new places (week 1 schedule) ----
    # (person, weekly slot it replaces, new place, periods); the story-critical slots stay.
    R13_NEW_PLACE_ROUTINES={
        "resident_kkwak":(("lowroad","home"),"river",(0,1)),
        "resident_nero":(("lowroad",),"river",(0,1,2)),
        "resident_badook":(("home",),"forest",(0,1)),
        "resident_bori":(("home",),"forest",(0,1)),
        "resident_siluk":(("home",),"forest",(0,1)),
        "resident_eunho":(("post",),"market",(0,1,2)),
        "resident_guseul":(("post",),"market",(0,1,2)),
        "resident_kongi":(("post",),"market",(0,1)),
        "resident_ppul":(("post",),"market",(0,1)),
        "resident_yeoni":(("home",),"market",(0,1)),
    }

    def r13_raw_weekly_slot(person):
        s=store.room13
        weekly=R13_WEEKLY_ROUTINES.get(person,(R13_RESIDENTS.get(person) or {}).get("weekly_locations"))
        if not weekly:return None
        return weekly[(s["day"]-1)%7][min(s["period"],2)]

    _r13_new_places_resident_where=r13_resident_where
    def r13_resident_where(person):
        where=_r13_new_places_resident_where(person)
        rule=R13_NEW_PLACE_ROUTINES.get(person)
        s=store.room13
        if not rule or s["day"]<2 or s["day"]>=8 or "lodging" not in s.get("flags",[]):return where
        slots,place,periods=rule
        if min(s["period"],2) not in periods:return where
        raw=r13_raw_weekly_slot(person)
        # Only spare hours move; anything an event pinned (a school shelter, a clinic) stays.
        if raw in slots and where in (None,"post","gate"):return place
        return where

    # ---- work at the river and in the forest ----
    R13_JOBS.update(
        fishing=dict(title="강가 얼음낚시",npc="resident_kkwak",place="river",pay=7,
            detail="얼음 구멍이 다시 얼지 않게 깨고, 꽥순과 그물을 걷는다.",choice="강 건너 길에 관해 묻는다"),
        hunting=dict(title="숲속 덫 살피기",npc="resident_badook",place="forest",pay=8,
            detail="바둑이와 덫 세 곳을 돌며 걸린 짐승을 거둔다.",choice="숲 밖으로 나가는 길을 묻는다"),
    )
    R13_JOB_MARKS.update(fishing=["kkwak_ice"],hunting=["badook_trail"])
    R13_WORK_RELATIONS.update(
        kkwak_ice="꽥순에게 강 건너 길은 얼음이 얇아 겨울에는 막힌다는 것을 들었다.",
        badook_trail="바둑이에게 숲 끝은 절벽이라 마을 밖으로 나가는 길이 없다는 것을 들었다.")
    R13_JOB_CONTEXT.update(fishing="꽥순과 얼음 구멍을 지키며 그물을 걷는다.",hunting="바둑이와 숲속 덫을 돌아본다.")
    R13_JOB_START_LINES=dict(
        fishing=[("resident_kkwak","얼음 구멍이 다시 얼지 않게 가장자리만 깨 주세요. 그물은 제가 걷을게요."),
            ("dad","가장자리만 깨면 됩니까?"),("resident_kkwak","네. 너무 넓히면 발밑이 꺼져요.")],
        hunting=[("resident_badook","덫은 세 군데예요. 걸린 게 있으면 제가 거둘게요."),
            ("dad","저는 무엇을 하면 됩니까?"),("resident_badook","길을 표시한 【천】만 따라오세요. 숲 안쪽은 길이 없어요.")])
    R13_JOB_ASK_LINES=dict(
        fishing=[("dad","강을 건너 마을 밖으로 나갈 수 있습니까?"),("resident_kkwak","겨울엔 안 돼요. 얼음이 얇아서 마차는 못 건너요."),
            ("dad","걸어서는요?"),("resident_kkwak","해 질 녘엔 걸어서도 위험해요. 그래서 다들 【고개 마차】만 기다리죠.")],
        hunting=[("dad","숲을 지나 마을 밖으로 나가는 길은 없습니까?"),("resident_badook","숲 끝은 【절벽】이에요. 길은 없어요."),
            ("dad","그럼 순찰은 무엇을 지키는 겁니까?"),("resident_badook","길 잃은 사람이요. 밤에 숲에 들어간 사람은 저희가 찾아 데려와요.")])
    for _r13_job_key in ("fishing","hunting"):
        _r13_job=R13_JOBS[_r13_job_key]
        ROOM13["topics"]["job:"+_r13_job_key]=dict(npc=_r13_job["npc"],
            title="일손을 돕겠습니다 · %s (%d냥)"%(_r13_job["title"],_r13_job["pay"]),
            day=[2,14],need=["livelihood_open"],give=[],flags=[],lines=[])
        R13_TOPIC_LABELS["job:"+_r13_job_key]="r13_job_from_talk"

    # ---- goods: bought at the market (owner: "시장에서 클릭해서 상점 이용") ----
    _r13_new_places_topics=r13_topics
    def r13_topics(person):
        rows=[]
        for key,spec in _r13_new_places_topics(person):
            if key=="shop:eunho" and (store.room13 or {}).get("location")!="market":continue
            if key=="ancient:mom" and not r13_has("ancient_found"):continue
            rows.append((key,spec))
        return rows

    # ---- mom on the old works (week 2, after the family found it) ----
    ROOM13["topics"]["ancient:mom"]=dict(npc="mom",title="마을 아래의 옛 시설을 알고 있었어?",day=[8,14],need=["ancient_found"],give=[],flags=["ancient_mom_heard"],lines=[
        ("dad","13호 뒤 통로 아래에 옛 시설이 있었어. 알고 있었어?"),
        ("mom","응. 할머니가 처음 나를 데려간 곳이 거기야."),
        ("dad","처음부터 그곳을 보여 줬다고?"),
        ("mom","벽에 새긴 【옛 글자】를 읽어 달라고 했어. 돌을 다시 채우는 법이 적혀 있을 거라면서."),
        ("dad","그래서 읽었어?"),
        ("mom","일부만. 거기 적힌 건 돌을 새로 채우는 법이 아니었어. 여러 돌에 【남은 힘을 모으는 법】이었지."),
        ("dad","할머니가 바라던 대답은 아니었겠네."),
        ("mom","응. 그 뒤로 할머니는 나를 자꾸 거기로 데려가려 했어. 그래서 여관을 나온 거야."),
        ("dad","그곳 이야기를 마을 사람들에게 해도 될까?"),
        ("mom","보여 줄 기록이 갖춰지기 전에는 안 돼. 지금 말하면 사람들은 겁부터 낼 거야.")])
    R13_NAMES.setdefault("mom","엄마")

label r13_market_stall:
    if room13.get("period",0)>=2:
        call r13_lines([(None,"노점은 천을 덮고 문을 닫았다. 내일 낮에 다시 와야겠다.")],"market:stall:closed")
        return
    call r13_lines([(None,"노점 주인이 진열대 위 물건을 하나씩 가리켰다. 값은 공동 창고와 같다고 했다.")],"market:stall:open")
    call screen r13_shop
    return

label r13_ancient_crack:
    if r13_has("ancient_found") or not room13.get("week2_started"):
        return
    call r13_lines([(None,"갈라진 회벽에 손을 대자 판자 한 장이 안쪽으로 밀렸다. 그 뒤로 좁은 【돌계단】이 아래로 이어졌다."),
        ("dad","(위층 통로보다 훨씬 오래된 계단이다. 아래에서 따뜻한 바람이 올라온다.)",{"thought":True})],"ancient:crack")
    menu:
        "계단을 내려가 본다":
            $ r13_flag("ancient_found")
            $ r13_edit(location="ancient")
            call r13_ancient_first_visit
        "지금은 표시만 해 둔다":
            call r13_lines([("dad","(갈라진 자리를 기억해 두자. 다시 오면 판자를 밀면 된다.)",{"thought":True})],"ancient:crack:later")
    return

label r13_ancient_first_visit:
    call r13_scene(R13_PLACES["ancient"][1],R13_PLACES["ancient"][0],"quiet")
    $ r13_ancient_daram=room13.get("daram_state") in ("with_dad","rescued")
    call r13_lines([(None,"계단을 내려갈수록 공기가 따뜻해졌다. 마지막 계단을 내려서자 넓은 방이 나타났다."),
        (None,"돌기둥이 끝없이 늘어서 있고, 유리관 속 돌 조각들이 초록빛으로 숨 쉬듯 빛났다.")],"ancient:first:arrive")
    if r13_ancient_daram:
        call r13_lines([("daram","아빠… 마을 아래에 이런 데가 있었어?",{"expression":"anxious"}),
            ("dad","아빠도 처음 봐. 손 놓지 말고 아빠 옆에 있어."),
            ("daram","응. 그런데 여기, 이상하게 따뜻해.")],"ancient:first:daram")
    call r13_lines([("dad","(유리관 속 돌에 광장의 【돌】과 같은 홈무늬가 있다. 마을을 데우는 돌이 여기서 만들어졌던 걸까.)",{"thought":True}),
        (None,"바닥 먼지 위로 발자국 한 줄이 나 있었다. 작고 끝이 둥근 신발 자국. 여관 접수대 앞에서 날마다 보던 신발이다."),
        ("dad","(【할머니】가 이곳을 드나든다.)",{"thought":True})],"ancient:first:footprints")
    if room13.get("granny_state")!="detained" and not room13.get("finale_started"):
        call r13_ancient_granny
    else:
        call r13_lines([("dad","(할머니는 지금 붙잡혀 있다. 이곳을 지키던 사람이 자리를 비운 셈이다.)",{"thought":True}),
            ("dad","(보이는 것만 적어 두자. 이것만으로는 아무것도 입증되지 않는다.)",{"thought":True})],"ancient:first:alone")
    return

label r13_ancient_granny:
    call r13_lines([(None,"그때 기둥 뒤에서 등불 하나가 흔들렸다."),
        ("granny","……결국 여기까지 내려오셨군요."),
        ("dad","할머니. 여기가 어디입니까?"),
        ("granny","우리 집안이 대대로 지켜 온 곳이에요. 마을 사람들은 아무도 몰라요."),
        ("dad","촌장님도 모른다는 말씀입니까?"),
        ("granny","그래요. 촌장도, 경비도 몰라요. 알면 겁부터 낼 테니까."),
        ("dad","이 빛나는 돌들은 무엇입니까?"),
        ("granny","마을을 데우는 【돌】은 원래 여기서 만들어졌어요. 아주 먼 옛날 사람들이 만들었죠."),
        ("dad","지금도 여기서 돌을 만듭니까?"),
        ("granny","아니요. 만드는 법은 끊긴 지 오래예요. 지금은 남은 빛을 아껴 쓰는 것뿐이에요."),
        ("dad","남은 빛을 아낀다는 게, 사람에게서 힘을 뽑는 일입니까?"),
        ("granny","……빛이 줄어드는 걸 사람들이 알면 마을은 겨울을 못 넘겨요. 누군가는 정해야 했어요.",{"expression":"angry"}),
        ("dad","그 ‘누군가’가 할머니였군요."),
        ("granny","나는 맡은 일을 했을 뿐이에요."),
        ("dad","제 아내도 이곳을 알았습니까?"),
        ("granny","그 사람은 벽에 새긴 【옛 글자】를 읽을 줄 알았어요. 그래서 나는 그 사람이 꼭 필요했어요."),
        ("dad","그래서 아내를 붙잡아 두려 하셨습니까?"),
        ("granny","붙잡은 게 아니에요. 같이 지키자고 했을 뿐이에요. 그 사람은 거절했지만요."),
        ("dad","(할머니가 아내에게 매달린 이유가 이곳에 있었다. 하지만 지금 들은 말만으로는 아무것도 입증되지 않는다.)",{"thought":True}),
        ("granny","이곳 이야기는 마을에 하지 마세요. 사람들이 겁을 먹으면, 그다음은 아무도 책임 못 져요."),
        (None,"할머니는 등불을 들고 계단 쪽으로 사라졌다. 초록빛만 남은 방이 다시 조용해졌다.")],"ancient:granny")
    if r13_ancient_daram:
        call r13_lines([("daram","할머니는 엄마를 여기 데려오고 싶었던 거야?"),
            ("dad","그런 것 같아. 그런데 엄마는 싫다고 했대."),
            ("daram","엄마가 싫다고 한 데는 이유가 있을 거야.")],"ancient:granny:daram")
    $ r13_flag("ancient_granny_met")
    return
