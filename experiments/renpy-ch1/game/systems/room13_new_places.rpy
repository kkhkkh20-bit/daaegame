# New places (owner, 0.18.61): "광장 외에 4개 더 … 사냥 낚시 … 시장도 좋아", "일거리 조사 다 넣지 뭐",
# "거대 문명 맵도 생겼는데 어떻게 보여줄지, 할머니 비밀장소 대사와 다 만들어 줘".
# Art: art/new-maps-v3-20261015. The places 장터·강가·숲속 are game/room13_new_places.rpy (0.18.63);
#   here the river and the forest each give a day's work and goods are bought at the market's
#   cheese and meat stall (the old 은호 topic moves there).
#   - 돌을 만들던 옛 시설 (ancient): granny's secret place under the inn, reached in week 2 through a
#     cracked wall in the 13호 back passage. Seeing it and hearing granny/mom there is story colour
#     and motive; it grants no record and opens no proof, so trials and endings are unchanged.
# Residents whose week had no place to go ("아랫길", spare home hours, the post visits) now spend
# some of it here, which thins the post office crowd.
init 130 python:
    # 장터·강가·숲속 themselves (places, art, inspection spots) come from game/room13_new_places.rpy
    # (0.18.63). This file adds what happens there, and the old works under the inn.
    R13_PLACES.update(ancient=("돌을 만들던 옛 시설","wide_ancient"))
    R13_MAP_LABELS.update(ancient="옛 시설")

    _r13_new_places=r13_places
    def r13_places():
        result=list(_r13_new_places())
        if r13_ancient_open() and "ancient" not in result:result.append("ancient")
        return result

    def r13_ancient_open():
        s=store.room13 or {}
        return bool(s.get("passage_open")) and r13_has("ancient_found")

    R13_LOCAL_CONNECTIONS["ancient"]=(("passage","계단 위로"),)
    R13_LOCAL_CONNECTIONS["passage"]=tuple(R13_LOCAL_CONNECTIONS.get("passage",()))+(("ancient","돌계단 아래로"),)

    # The cheese and meat stall also sells the village goods (the old 은호 shop topic).
    ROOM13["objects"]["market"]["market_cheese"]["call_label"]="r13_market_stall"

    # ---- inspection spots in the old works (world coordinates of the 2160-wide picture) ----
    def _r13_spot(rect,text,**kw):
        spec=dict(rect=list(rect),text=text,need=[],give=[],flags=[]);spec.update(kw);return spec
    ROOM13["objects"]["ancient"]=dict(
        an_press=_r13_spot((180,230,340,270),"거대한 누르개 아래 각진 돌이 놓여 있다. 돌 표면의 홈무늬가 광장의 돌과 같다. 누르개에는 먼지가 두껍게 쌓였다."),
        an_tube=_r13_spot((955,119,120,358),"유리관 속에 돌 조각이 떠 있다. 빛이 아주 천천히 밝아졌다가 어두워진다. 무엇이 빛을 채우는지는 보이지 않는다."),
        an_small_tube=_r13_spot((1094,278,80,200),"작은 유리관은 반쯤 비어 있다. 바닥에 가라앉은 돌 조각에는 빛이 거의 없다."),
        an_drip=_r13_spot((1730,40,239,298),"천장 장치에서 초록빛 물방울이 하나씩 떨어진다. 떨어지는 간격이 일정하지 않다."),
        an_channel=_r13_spot((119,547,677,70),"바닥 도랑은 오래전에 말랐다. 돌 틈에 남은 희미한 빛의 자국만 계단 쪽 위로 이어진다."),
        an_corridor=_r13_spot((1472,318,120,200),"복도가 어둠 속으로 길게 이어진다. 등불 없이 더 들어가는 건 위험하다."),
    )
    # The way down: a cracked wall in the back passage, noticed only in week 2.
    ROOM13["objects"].setdefault("passage",{})["crack"]=dict(rect=[1870,239,140,160],
        text="회벽이 갈라진 틈으로 따뜻한 바람이 새어 나온다.",need=["week2_started"],give=[],flags=[],call_label="r13_ancient_crack")
    R13_OBJECT_NAMES.update(an_press="누르개 아래의 돌",an_tube="빛나는 유리관",an_small_tube="작은 유리관",an_drip="빛이 떨어지는 장치",an_channel="바닥의 빛 도랑",
        an_corridor="멀리 이어진 복도",crack="갈라진 회벽")

    _r13_new_places_visible=r13_object_visible
    def r13_object_visible(spec):
        if spec is ROOM13["objects"].get("passage",{}).get("crack"):
            s=store.room13 or {}
            return bool(s.get("week2_started")) and s.get("day",1)>=8 and not r13_has("ancient_found")
        return _r13_new_places_visible(spec)

    # ---- residents: who spends spare hours at the new places ----
    # person: [(weekly slots it replaces, new place, periods, days)]. Days default to both weeks
    # except the arrival day and day 8 (2-7, 9-14). A slot moves only when nothing pinned the person
    # elsewhere (a shelter, a clinic, a week-2 post); events placed by r13_where stay authoritative.
    # 0.18.71 (owner): "장사하는 사람들 이제 시장에 많이 넣어 주자. 시장은 사람 많아도 되니."
    #   The market (morning and afternoon; closed in the evening) gathers the traders.
    #   꽥순 fishes and 바둑이 checks traps every afternoon, so their work exists in week 2 too.
    R13_NEW_PLACE_DAYS=tuple(range(2,8))+tuple(range(9,15))
    R13_NEW_PLACE_ROUTINES={
        "resident_kkwak":[(("lowroad",),"river",(1,),None)],
        "resident_nero":[(("lowroad",),"river",(0,),None)],
        "resident_badook":[(("home",),"forest",(1,),None)],
        "resident_bori":[(("home",),"forest",(0,1),None)],
        # Not day 6: 실룩 sells testimony at the gate that morning (r13_w1c_testimony).
        "resident_siluk":[(("gate",),"forest",(0,),(2,3,4,5,9,10,11,12,13))],
        "resident_eunho":[(("post",),"market",(0,),None)],
        "resident_guseul":[(("post",),"market",(1,),None)],
        "resident_kongi":[(("post",),"market",(1,),None),(("square",),"market",(0,),None)],
        "resident_ppul":[(("post",),"market",(0,1),(2,4,6,9,11,13))],
        "resident_yeoni":[(("home",),"market",(0,),None)],
        "resident_madam":[(("home",),"market",(0,),None)],
        "resident_mungchi":[(("home",),"market",(0,),None)],
        "resident_tori":[(("square",),"market",(0,),(2,6,9,13))],
        "resident_nubi":[(("workshop",),"market",(1,),None)],
    }
    R13_RAW_SLOT_PLACE={"home":None,"library":"post","lowroad":"gate","tower":"square"}

    def r13_raw_weekly_slot(person):
        s=store.room13
        weekly=R13_WEEKLY_ROUTINES.get(person,(R13_RESIDENTS.get(person) or {}).get("weekly_locations"))
        if not weekly:return None
        return weekly[(s["day"]-1)%7][min(s["period"],2)]

    def r13_new_place_for(person):
        """The new place this resident spends the current slot at, or None."""
        s=store.room13
        if "lodging" not in s.get("flags",[]):return None
        raw=r13_raw_weekly_slot(person);period=min(s["period"],2)
        for slots,place,periods,days in R13_NEW_PLACE_ROUTINES.get(person,()):
            if raw in slots and period in periods and s["day"] in (days or R13_NEW_PLACE_DAYS):return place
        return None

    def r13_new_place_people(location):
        """Residents whose routine can bring them to this new place."""
        return [x for x,rs in R13_NEW_PLACE_ROUTINES.items() if any(r[1]==location for r in rs)]

    _r13_new_places_resident_where=r13_resident_where
    def r13_resident_where(person):
        where=_r13_new_places_resident_where(person)
        place=r13_new_place_for(person)
        # Only the plain weekly slot moves; a special case above (clinic, shelter) wins.
        if place and where==R13_RAW_SLOT_PLACE.get(r13_raw_weekly_slot(person),r13_raw_weekly_slot(person)):return place
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
            ("dad","걸어서는요?"),("resident_kkwak","해 질 녘엔 걸어서도 위험해요. 그래서 다들 【고개 마차】만 기다리죠."),
            ("resident_kkwak","아, 며칠 전 새벽엔 낯선 아주머니가 여기서 물을 길어 갔어요. 【숲】 쪽으로 가던데요.")],
        hunting=[("dad","숲을 지나 마을 밖으로 나가는 길은 없습니까?"),("resident_badook","숲 끝은 【절벽】이에요. 길은 없어요."),
            ("dad","그럼 순찰은 무엇을 지키는 겁니까?"),("resident_badook","길 잃은 사람이요. 밤에 숲에 들어간 사람은 저희가 찾아 데려와요."),
            ("resident_badook","그러고 보니 며칠 전 밤엔 【큰 전나무 뿌리】 쪽에서 등불이 하나 깜빡였어요. 가 보니 아무도 없었지만요.")])
    for _r13_job_key in ("fishing","hunting"):
        _r13_job=R13_JOBS[_r13_job_key]
        ROOM13["topics"]["job:"+_r13_job_key]=dict(npc=_r13_job["npc"],
            title="일손을 돕겠습니다 · %s (%d냥)"%(_r13_job["title"],_r13_job["pay"]),
            day=[2,14],need=["livelihood_open"],give=[],flags=[],lines=[])
        R13_TOPIC_LABELS["job:"+_r13_job_key]="r13_job_from_talk"

    # ---- mom's first hiding place (owner 0.18.71: "엄마가 숨는 공간도 마련해 줘야 해") ----
    # Week 1 had only the words "예전 은신처" (room13_week2.rpy, E19). It is the hollow under the
    # tangled roots in the forest: she watched the inn road from there, left when she heard someone
    # follow her, and moved to the greenhouse basement. Finding it is colour and motive only: a flag,
    # no record, so trials and endings do not change. 바둑이 mentions a lamp there during the trap work.
    R13_FOREST_ROOTS_TEXT=ROOM13["objects"]["forest"]["forest_roots"]["text"]
    R13_MARKET_CLOTH_TEXT=ROOM13["objects"]["market"]["market_cloth"]["text"]
    ROOM13["objects"]["market"]["market_cloth"]["call_label"]="r13_market_cloth"
    ROOM13["objects"]["forest"]["forest_roots"]["call_label"]="r13_mom_hideout"
    R13_OBJECT_NAMES["forest_roots"]="엉킨 뿌리"
    ROOM13["topics"]["hideout:mom"]=dict(npc="mom",title="숲 뿌리 밑에 숨어 있었어?",day=[8,14],need=["mom_hideout_found"],give=[],flags=["mom_hideout_heard"],lines=[
        ("dad","숲속 큰 뿌리 밑에서 당신이 쓰던 담요를 봤어. 거기 있었지?"),
        ("mom","응. 여관을 나와서 처음 숨은 데가 거기야. 바둑이 순찰길에서 조금 비켜 있어서."),
        ("dad","그 구멍에서 여관 굴뚝이 보이더라."),
        ("mom","그래서 거기 있었어. 마차가 오는 날, 당신이랑 다람이가 내리는 것도 봤어."),
        ("dad","봤으면서 왜 내려오지 않았어?"),
        ("mom","그날 밤부터 누가 내 발자국을 따라왔어. 내가 내려가면 그 사람이 곧장 너희한테 닿았을 거야."),
        ("mom","그래서 【초롱】한테 경고를 맡기고, 책상 메모로 초롱에게 가는 길만 남겼어."),
        ("dad","할머니도 그 방에 드나들었을 텐데, 메모가 들킬 걱정은 안 했어?"),
        ("mom","했지. 그래서 메모엔 초롱 이름만 남겼고, 초롱한테도 내가 어디 있는지는 끝까지 말하지 않았어."),
        ("dad","뿌리 밑 종이에 ‘여기는 들켰다, 옮긴다’고 적혀 있었어."),
        ("mom","발소리가 구멍 앞에서 멈춘 밤이 있었어. 다음 날 새벽에 【폐온실】 아래로 옮겼지.")])

    # ---- goods: bought at the market (owner: "시장에서 클릭해서 상점 이용") ----
    _r13_new_places_topics=r13_topics
    def r13_topics(person):
        rows=[]
        for key,spec in _r13_new_places_topics(person):
            if key=="shop:eunho" and (store.room13 or {}).get("location")!="market":continue
            if key=="ancient:mom" and not r13_has("ancient_found"):continue
            if key=="hideout:mom" and not r13_has("mom_hideout_found"):continue
            rows.append((key,spec))
        return rows

    # ---- mom on the old works (week 2, after the family found it) ----
    ROOM13["topics"]["ancient:mom"]=dict(npc="mom",title="마을 아래의 옛 시설을 알고 있었어?",day=[8,14],need=["ancient_found"],give=[],flags=["ancient_mom_heard"],lines=[
        ("dad","13호 뒤 통로 아래에 옛 시설이 있었어. 알고 있었어?"),
        ("mom","응. 할머니가 처음 나를 데려간 곳이 거기야."),
        ("dad","처음부터 그곳을 보여 줬다고?"),
        ("mom","벽에 새긴 【옛 글자】, 룬을 읽어 달라고 했어. 돌을 다시 채우는 법이 적혀 있을 거라면서."),
        ("dad","그래서 읽었어?"),
        ("mom","일부만. 거기 적힌 건 돌을 새로 채우는 법이 아니었어. 여러 돌에 【남은 힘을 모으는 법】이었지."),
        ("dad","할머니가 바라던 대답은 아니었겠네."),
        ("mom","응. 그 뒤로 할머니는 나를 자꾸 거기로 데려가려 했어. 회복한 사람의 기록을 바로잡으려 하자 나까지 가두려 했고. 그래서 여관을 나온 거야."),
        ("dad","그곳 이야기를 마을 사람들에게 해도 될까?"),
        ("mom","보여 줄 기록이 갖춰지기 전에는 안 돼. 기록 없이 말하면 할머니 말만 남아.")])
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
        ("granny","우리 집안이 대대로 지켜 온 곳이에요. 산속 제단은 촌장도 알지만, 이 아래는 우리 집안만 알아요."),
        ("dad","촌장님도 이곳은 모른다는 말씀입니까?"),
        ("granny","제단 장치를 어떻게 다루는지는 내가 촌장에게 일러 줬어요. 그 장치가 어디서 왔는지는 말하지 않았고요."),
        ("dad","이 빛나는 돌들은 무엇입니까?"),
        ("granny","마을을 데우는 【돌】은 원래 여기서 만들어졌어요. 아주 먼 옛날 사람들이 만들었죠."),
        ("dad","지금도 여기서 돌을 만듭니까?"),
        ("granny","아니요. 만드는 법은 끊겼어요. 벽의 글을 읽는 법도 내 어머니 대에 끊겼고요. 남은 건 사람에게서 빛을 거두는 법뿐이었죠."),
        ("dad","사람에게서 빛을 거둔다는 게, 제단에서 하는 그 일입니까?"),
        ("granny","……돌에 빛이 얼마나 남았는지 사람들이 알면 마을은 겨울을 못 넘겨요. 누군가는 정해야 했어요.",{"expression":"angry"}),
        ("dad","누구를 보낼지 정한 사람이 할머니였군요."),
        ("granny","보내자고 정한 건 회의였어요. 누구를 보낼지는 내가 골랐고요. 나는 맡은 일을 했을 뿐이에요."),
        ("dad","제 아내도 이곳을 알았습니까?"),
        ("granny","그 사람은 벽에 새긴 【옛 글자】, 룬을 읽을 줄 알았어요. 그래서 나는 그 사람이 꼭 필요했어요."),
        ("dad","그래서 아내를 붙잡아 두려 하셨습니까?"),
        ("granny","붙잡은 게 아니에요. 같이 지키자고 했을 뿐이에요. 그 사람은 거절했지만요."),
        ("dad","(같이 지키자고 했을 뿐이라면, 아내는 왜 여관을 나와 숨어야 했을까. 할머니 말과 아내가 한 일이 맞지 않는다.)",{"thought":True}),
        ("dad","책상에 남은 아내의 메모는 왜 그대로 두셨습니까? 할머니도 그 방에 드나드셨을 텐데요."),
        ("granny","초롱에게 가라는 메모였죠. 그냥 뒀어요. 당신들이 그 사람한테 가는 길을 찾아 줄 테니까."),
        ("dad","(메모를 남겨 둔 것도 아내를 찾으려는 미끼였다. 하지만 지금 들은 말만으로는 아무것도 입증되지 않는다.)",{"thought":True}),
        ("granny","이곳 이야기는 마을에 하지 마세요. 사람들이 겁을 먹으면, 그다음은 아무도 책임 못 져요."),
        (None,"할머니는 등불을 들고 계단 쪽으로 사라졌다. 초록빛만 남은 방이 다시 조용해졌다.")],"ancient:granny")
    if r13_ancient_daram:
        call r13_lines([("daram","할머니는 엄마를 여기 데려오고 싶었던 거야?"),
            ("dad","그런 것 같아. 그런데 엄마는 싫다고 했대."),
            ("daram","엄마가 싫다고 한 데는 이유가 있을 거야.")],"ancient:granny:daram")
    $ r13_flag("ancient_granny_met")
    return

label r13_market_cloth:
    if r13_has("mom_hideout_found"):
        call r13_lines([(None,"털실과 천이 색깔별로 쌓인 노점이다. 맨 아래 담요의 가장자리 무늬가 눈에 익다."),
            ("dad","(숲 뿌리 밑에 있던 담요와 같은 무늬다. 아내는 이 노점에서 담요를 샀을까.)",{"thought":True})],"market:cloth:blanket")
    else:
        call r13_observe([(None,R13_MARKET_CLOTH_TEXT)],"market:cloth:plain")
    return

label r13_mom_hideout:
    if room13["day"]<3:
        call r13_observe([(None,R13_FOREST_ROOTS_TEXT)],"forest:roots:plain")
        return
    if r13_has("mom_hideout_found"):
        call r13_lines([(None,"뿌리 밑 구멍은 그대로다. 접힌 담요 위에 눈이 조금 더 쌓였다."),
            ("dad","(아내는 여기서 여관 굴뚝을 보고 있었다.)",{"thought":True})],"forest:hideout:again")
        return
    $ r13_hideout_daram=room13.get("daram_state") in ("with_dad","rescued")
    call r13_lines([(None,"엉킨 뿌리 사이의 눈이 유난히 단단하게 다져져 있다. 누가 여러 번 드나든 자국이다."),
        (None,"몸을 숙이자 뿌리 밑으로 어른 하나가 웅크려 들어갈 만한 구멍이 보였다."),
        (None,"안쪽에는 마른 솔잎이 깔려 있고, 접은 담요와 다 타 버린 초 토막, 이 빠진 찻잔이 놓여 있었다."),
        ("dad","(뿌리 안쪽 껍질에 【도토리】가 새겨져 있다. 우리 가족만 쓰는 표식이다.)",{"thought":True}),
        ("dad","(아내가 여기 숨어 있었다. 초는 꺼진 지 며칠은 됐다.)",{"thought":True}),
        (None,"담요 아래에서 접힌 종이 한 장이 나왔다. 앞면에는 룬을 옮겨 적다 만 연습이 빽빽했다."),
        (None,"뒷면에는 서둘러 쓴 한 줄이 있었다. 「따라오는 발소리. 여기는 들켰다. 옮긴다.」"),
        ("dad","(구멍 입구에서 나무 사이로 여관 굴뚝이 보인다. 아내는 여기서 여관 쪽을 지켜보고 있었다.)",{"thought":True})],"forest:hideout:find")
    if r13_hideout_daram:
        call r13_lines([("daram","이 담요, 엄마 거야. 끝에 내가 꿰맨 실이 있어.",{"expression":"anxious"}),
            ("dad","그래. 엄마는 여기서 우리를 기다렸던 것 같아."),
            ("daram","그런데 왜 내려오지 않았어?"),
            ("dad","누가 엄마를 따라왔대. 엄마가 내려오면 그 사람도 같이 왔을 거야.")],"forest:hideout:daram")
    call r13_lines([("dad","(누가 아내를 따라왔을까. 지금은 알 수 없다. 이 자리는 남에게 말하지 말자.)",{"thought":True})],"forest:hideout:close")
    $ r13_flag("mom_hideout_found")
    return
