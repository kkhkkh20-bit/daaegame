# Story integration; generic economy rules live in the model module.
init 92 python:
    def r13_life_apply_purchase(key):
        state,ok=r13_purchase(store.room13,key)
        store.room13=state
        renpy.notify("구입했습니다." if ok else "이미 가지고 있거나 돈이 부족합니다.")
    def r13_life_repay():
        store.room13=r13_repay(store.room13)

    _r13_life_next_day=r13_next_day
    def r13_next_day():
        if store.room13.get("life_poc") or r13_has("livelihood_open"):
            store.room13=r13_settle_lodging(store.room13)
        _r13_life_next_day()

    ROOM13["topics"]["life:karo"]=dict(npc="karo",title="마차는 언제 다시 출발합니까?",day=[2,14],need=["lodging"],give=[],flags=["livelihood_open"],lines=[
        ("dad","그럼 마차는 언제 다시 출발합니까?"),
        ("karo","바퀴 축도 고쳐야 하고, 고개를 넘는 정기 마차도 겨울에는 쉬어요. 그래서 제 마차로는 당장 돌아가실 수 없습니다."),
        ("dad","하루 이틀만 머물 생각이었는데……. 고개 말고 다른 길 사정도 아십니까?"),
        ("karo","다른 길은 직접 알아보셔야 해요. 제가 다니던 고개 길과는 사정이 다르거든요."),
        ("karo","여기 계시는 동안 일손을 보태 보실래요? 짐 나르는 일은 한나절에 일곱 냥이에요. 여관이랑 수리점에서도 일할 사람을 구한대요."),
        ("dad","일도 좋지만, 아내 소식도 계속 알아봐야 합니다."),
        ("karo","그럼 배달을 다니면서 마을 사람들을 만나 보세요. 대신 누구네 짐인지는 꼭 짐표와 같이 확인하고요.")])
    ROOM13["topics"]["life:nabi"]=dict(npc="nabi",title="초롱 씨 그릇은 늘 따로 챙기니?",day=[2,14],need=["life:nabi_helped"],give=[],flags=[],lines=[
        ("dad","아까 따로 둔 그릇 말이야, 초롱 씨 몫이라고 했니?"),
        ("nabi","네. 밖에서 등불을 돌보느라 끼니때를 자주 놓치거든요."),
        ("dad","아내가 여기 머물 때도 등불 돌보는 분이 왔었니?"),
        ("nabi","네, 오긴 했죠. 부인이랑 무슨 얘기를 했는지는 초롱한테 직접 물어봐요.")])
    ROOM13["topics"]["life:buri"]=dict(npc="buri",title="장부의 숫자는 언제 옮겨 적습니까?",day=[2,14],need=["life:buri_honest"],give=[],flags=[],lines=[
        ("buri","아까 모자란 부품 알려 줘서 고마워요. 다시 세어 본 수를 장부에 적어 뒀어요."),
        ("dad","장부에 적힌 수와 실제 물건 수가 다를 때도 있구나."),
        ("buri","일이 다 끝난 뒤에 장부에 옮겨 적으니까요. 그래서 적혀 있다고 늘 맞는 건 아니에요.")])

    _r13_life_topics=r13_topics
    def r13_topics(person):
        rows=_r13_life_topics(person)
        # Keep the return-journey question easy to find on day two.
        return sorted(rows,key=lambda row:0 if row[0]=="life:karo" and not r13_has("livelihood_open") else 1)

label r13_livelihood:
    window hide
    call screen r13_work_board
    if not isinstance(_return,(tuple,list)) or len(_return)!=2:
        return
    $ r13_job_key,r13_job_choice=_return
    jump r13_livelihood_start

# 0.18.56 (owner): work is asked for in person (systems/room13_direct_work.rpy).
label r13_livelihood_run(job):
    $ r13_job_key,r13_job_choice=job,"finish"
label r13_livelihood_start:
    if not r13_work_available(r13_job_key):
        return
    $ r13_job_spec=R13_JOBS[r13_job_key]
    call screen r13_confirm(r13_job_spec["title"]+" · 일당 %d냥\n"%r13_job_spec["pay"]+r13_learning_time_text(1)+"\n"+r13_learning_settlement_text(additional=r13_job_spec["pay"]),"시작하기","돌아가기")
    if not _return:
        return
    $ r13_edit(location=r13_job_spec["place"])
    call r13_scene(R13_PLACES[room13["location"]][1],R13_PLACES[room13["location"]][0],"calm")
    if r13_job_key=="delivery":
        call r13_lines([("karo","이 두 짐은 받는 사람 이름과 목적지부터 확인하고 옮깁시다.")],"life:delivery:start:v2")
    elif r13_job_key in R13_JOB_START_LINES:
        call r13_lines(R13_JOB_START_LINES[r13_job_key],"life:"+r13_job_key+":start")
    elif r13_job_key=="kitchen":
        call r13_lines([("nabi","닦은 그릇은 여기에 두고요. 이 한 벌은 따로 놓아 줘요."),("dad","응. 나머지 그릇은 식당으로 내가면 되니?")],"life:kitchen:start")
    else:
        call r13_lines([("buri","부품은 같은 크기끼리 나눠 주세요. 다 세고 나면 장부에 표시하고요."),("dad","세어 보니 장부에 적힌 것보다 한 개 적구나.")],"life:repair:start")
    $ r13_job_question=r13_job_spec["choice"]
    $ r13_combined_pay=R13_JOBS["delivery"]["pay"]*2
    if r13_job_key=="delivery":
        call r13_delivery_inspect
    elif r13_job_key=="kitchen" and not r13_has("life_meal_served"):
        call r13_life_meal
    else:
        menu:
            "맡은 일만 마친다":
                $ r13_job_choice="finish"
            "[r13_job_question]":
                $ r13_job_choice="ask"
    $ r13_life_state,r13_life_result=r13_complete_job(room13,r13_job_key,r13_job_choice)
    if not r13_life_result:
        return
    $ room13=r13_life_state
    $ r13_time_consequences(room13)
    if r13_life_result["observed"]:
        if r13_job_key=="delivery":
            call r13_lines([("dad","받는 집은 잘 아십니까?"),("karo","광장 뒤는 제가 매일 다니는 길이에요. 짐 끈은 수레에 걸어 뒀으니 필요하면 쓰세요.")],"life:delivery:route:v2")
        elif r13_job_key in R13_JOB_ASK_LINES:
            call r13_lines(R13_JOB_ASK_LINES[r13_job_key],"life:"+r13_job_key+":ask")
        elif r13_job_key=="kitchen":
            call r13_lines([("dad","따로 놓은 이 그릇은 누구 몫이니?"),("nabi","초롱 몫이요. 돌아오면 드려야 해요. 다른 이야기는 손님 식사를 내간 다음에 해요.")],"life:kitchen:notice")
        else:
            call r13_lines([("dad","부품 하나가 모자라. 그래서 장부에는 아직 표시하지 않았어."),("buri","잘했어요. 장부에 적힌 수에 억지로 맞추지 마세요. 모자란 하나는 제가 어디 썼는지 찾아볼게요.")],"life:repair:honest")
        $ r13_flag(*["life:"+mark for mark in r13_wallet(room13)["relations"]])
    elif r13_life_result["combined"]:
        call r13_lines([("karo","한 번 나간 길에 두 건을 다 마쳤네요. 약속대로 두 건 값입니다.")],"life:delivery:combined")
    $ renpy.notify("일당 %d냥 · 현재 %d냥"%(r13_life_result["pay"],r13_wallet(room13)["cash"]))
    return

# Two parcels, one address (owner's knowledge-run plan D-1, 0.18.16). No "earn double" choice:
# the labels can be read, the load tried, and an owned item (or 까로's cord, once he offered it)
# used on the boxes. Pay, the once-only bonus and time stay as in r13_complete_job.
# r13_delivery_inspect now lives in systems/room13_life_closeups.rpy (drawn close-up, 0.18.22).

init 93 python:
    _r13_life_where=r13_where
    def r13_where(person):
        if person=="karo" and store.room13.get("day")==2 and not r13_has("livelihood_open"):
            return "gate"
        return _r13_life_where(person)

    ROOM13["topics"]["life:snack"]=dict(npc="daram",title="구운 밤, 같이 먹을까?",day=[2,14],need=[],give=[],flags=[],lines=[("daram","이거 반씩 나눠 먹자. 엄마 몫도 남겨 둘까?"),("dad","오늘은 따뜻할 때 다 먹자. 다시 만나면 그때 셋이 같이 사러 가고."),("daram","응. 그때는 내가 골라 줄 거야.")])
    _r13_life_snack_topics=r13_topics
    def r13_topics(person):
        return [(key,spec) for key,spec in _r13_life_snack_topics(person)
            if key!="life:snack" or (r13_home_with_daram() and "snack" in r13_wallet(store.room13)["items"])]
    _r13_life_finish_topic=r13_finish_topic
    def r13_finish_topic(key):
        _r13_life_finish_topic(key)
        if key=="life:snack":
            n=winter_copy.deepcopy(store.room13);wallet=r13_wallet(n)
            if "snack" in wallet["items"]:wallet["items"].remove("snack")
            n["livelihood"]=wallet;store.room13=n
