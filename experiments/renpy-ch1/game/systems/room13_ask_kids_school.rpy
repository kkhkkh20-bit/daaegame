# 0.19.17 질문이 앞서 나가지 않게 (소유자 2026-10-17): 아이들·학교·아랫길 묶음 (g5_kids_school)
#   "배달 일을 하는지 어떻게 알고 '배달 일은 힘들지 않니?'야?"
#   질문 제목은 아빠가 지금 아는 것(눈에 보이는 일, 들은 말, 첫 만남 장면)만 전제한다.
#   - 첫 만남 장면에서 자기 일을 말하거나 하는 일이 그대로 보이는 사람(보리, 누비, 선생님, 촌장, 너울, 설이)과
#     일정한 일이 없는 밤이는 새 질문을 두지 않는다. 그 사람과 대화를 여는 순간 그 장면을 본 것이다.
#   - 첫 만남 장면이 일을 말하지 않는 사람(솜이, 무쇠, 네로)과 첫 만남 장면이 없는 사람(종종이, 칼바람, 굴돌)은
#     ask:job:<id> 질문 하나로 일을 묻는다. 읽으면 knows_job:<id> 깃발이 선다.
#   틀: systems/room13_threads.rpy (steps / variants / again). 기존 steps는 덮지 않고 {"all":[old,new]}로 합친다.
#   원래 줄기 파일(room13_threads_kids_school.rpy, init 186)은 고치지 않는다.
init 197 python:
    def _ak5_steps(key,cond):
        t=ROOM13["topics"].get(key)
        if t is None:return
        old=t.get("steps")
        t["steps"]={"all":[old,cond]} if old else cond

    def _ak5_retitle(key,title,summary):
        t=ROOM13["topics"].get(key)
        if t is None:return
        t["title"]=title
        R13_QUESTION_SUMMARIES[title]=summary

    def _ak5_job(person,title,lines,again,summary):
        key="ask:job:"+person
        ROOM13["topics"][key]=dict(npc=person,title=title,day=[1,14],need=[],not_flags=[],give=[],
            flags=["knows_job:"+person],lines=list(lines),again=[(None,list(again))])
        R13_QUESTION_SUMMARIES[title]=summary

    def _ak5_heard_bori_fire(s):
        # 보리의 첫날 첫 만남(early)은 "저희 집은 불부터 지펴야 해서요"로 끝나고,
        # 수요일(6일) 인사도 "불은 기다려 주질 않네요"다. 그날 보리와 말한 기록이 있으면 들은 것이다.
        for e in s.get("encounters",[]):
            if isinstance(e,dict) and e.get("person")=="resident_bori" and e.get("day") in (1,6):
                return True
        return False

    def _ak5_nero_at_store(s):
        # 창고에서는 네로가 짐에 붙은 낡은 이름표를 떼는 모습이 화면 활동 문구로 보인다.
        return s.get("location")=="store"

    # =====================================================================
    # 새 질문: 무슨 일을 하는지 (보이는 것에서 출발)
    # =====================================================================
    # 종종이: 우체국·광장·장터에서 편지 묶음을 안고 다닌다.
    _ak5_job("resident_jongjong","편지 꾸러미가 많네. 여기서 일하니?",[
        ("dad","편지 꾸러미가 많네. 여기서 일하니?"),
        ("resident_jongjong","네! 종종이예요. 우체국에서 편지 돌리는 배달꾼이에요!"),
        ("resident_jongjong","아침엔 우체국에서 순서 받고요, 오후엔 광장 집집을 다 돌아요. 장터 송장도 제가 돌려요.")],
        [("resident_jongjong","저는 우체국 배달꾼이에요! 오늘도 광장 집집을 다 돌 거예요.")],
        "무슨 일을 하는지 묻는다")
    # 솜이: 광장에서 구두 밑창 얼음을 긁는다. 심부름 가방을 멨다.
    _ak5_job("resident_somi","가방이 무거워 보이네. 일하는 중이니?",[
        ("dad","가방이 무거워 보이네. 일하는 중이니?"),
        ("resident_somi","심부름이요. 지붕으로 다니면 아래 길보다 훨씬 빨라요."),
        ("resident_somi","누가 시켰는지는 묻지 마세요. 그건 심부름 시킨 사람 일이에요.")],
        [("resident_somi","심부름 중이라고 했잖아요. 누가 시켰는지는 말 안 해요.")],
        "무슨 일을 하는지 묻는다")
    # 무쇠: 수리점 난로 곁에서 낡은 지도를 접어 넣는다. 첫 만남에서는 이름과 길 이야기만 했다.
    _ak5_job("resident_musoe","지금은 무슨 일을 하십니까?",[
        ("dad","지금은 무슨 일을 하십니까?"),
        ("resident_musoe","옛날엔 광산에서 굴을 팠소. 광산이 닫힌 뒤로는 손을 놓았지."),
        ("resident_musoe","지금은 손녀 솜이 하나 돌보는 게 일이오. 그 애가 날래서 나보다 바쁘오.")],
        [("resident_musoe","옛날엔 굴을 팠고, 지금은 솜이를 돌보오. 그게 다요.")],
        "무슨 일을 하는지 묻는다")
    # 네로: 강가에서 그물을 손질하거나 창고·입구에서 짐을 나른다. 첫 만남에서는 이름만 알려 줬다.
    _ak5_job("resident_nero","여기서 무슨 일을 하십니까?",[
        ("dad","여기서 무슨 일을 하십니까?"),
        ("resident_nero","아침엔 강가 일이고, 오후엔 창고 짐을 날라요. 일 있는 데면 어디든 가요."),
        ("resident_nero","아랫길 오두막에서 몇 사람이랑 같이 살아요. 누군지는 묻지 마시고요.")],
        [("resident_nero","강가 일하고 짐 나르는 일이요. 같이 사는 사람들 이야기는 거기까지예요.")],
        "무슨 일을 하는지 묻는다")
    # 칼바람: 숲에서 덫을 손질하거나 입구에 가죽 꾸러미를 내려놓는다.
    _ak5_job("resident_kalbaram","여기서 무슨 일을 하십니까?",[
        ("dad","여기서 무슨 일을 하십니까?"),
        ("resident_kalbaram","사냥."),
        ("resident_kalbaram","숲 끝에 사오. 가죽은 입구까지만 가져오고, 마을 안엔 잘 안 들어가오.")],
        [("resident_kalbaram","사냥하오. 숲 끝에 사오.")],
        "무슨 일을 하는지 묻는다")
    # 굴돌: 수리점에서 작은 돌을 두드리며, 광장에서는 돌 앞에 서서 귀를 댄다.
    _ak5_job("resident_guldol","돌 소리를 듣고 계십니까?",[
        ("dad","돌 소리를 듣고 계십니까?"),
        ("resident_guldol","그렇소. 두드려 보면 어디가 금 갔는지 소리가 알려 주오."),
        ("resident_guldol","나는 돌 일을 하오. 깨진 돌을 붙이는 일이지.")],
        [("resident_guldol","돌 일을 하오. 소리를 들으면 금 간 데를 아오.")],
        "돌 소리를 듣는지 묻는다")

    # =====================================================================
    # 직업·사정을 전제한 질문: 그 사실을 알게 된 뒤에만
    # =====================================================================
    # 종종이: 배달 일을 하는지 알아야 묻는다. 봉투 질문도 종종이가 우편을 부치는 줄 알아야 나온다.
    _ak5_steps("jongjong:work",{"has":["knows_job:resident_jongjong"]})
    _ak5_steps("jongjong:envelope",{"has":["knows_job:resident_jongjong"]})

    # 굴돌: "예전에 돌 일을 하셨다고 들었습니다"는 들은 데가 있어야 한다. 일을 직접 들은 뒤로 첫 줄을 바꾼다.
    _ak5_steps("guldol:stone",{"has":["knows_job:resident_guldol"]})
    if "guldol:stone" in ROOM13["topics"]:
        ROOM13["topics"]["guldol:stone"]["variants"]=list(ROOM13["topics"]["guldol:stone"].get("variants") or [])+[(None,[
            ("dad","돌 일은 오래 하셨습니까?"),
            ("resident_guldol","내 아버지 때까지는 마을에 돌 다루는 사람이 여럿 있었소."),
            ("resident_guldol","지금은 나 하나 남았지. 그나마 깨진 돌을 붙이는 정도요. 새로 만드는 법은 나도 모르오.")])]

    # 솜이: 심부름을 하는지 알아야 "요즘도 어른들이 심부름을 시키니?"가 나온다.
    _AK5_SOMI_JOB={"any":[{"has":["knows_job:resident_somi"]},{"has":["roof_path"]},{"has":["somi_secret"]},
        {"has":["somi_trust"]},{"has":["somi_hostile"]},{"has":["ev_b_done"]}]}
    _ak5_steps("life:resident_somi:after",_AK5_SOMI_JOB)

    # 무쇠: 솜이가 손녀라는 걸 알아야 "솜이에게 일을 부탁할 때"를 묻는다.
    _AK5_MUSOE_SOMI={"any":[{"has":["knows_job:resident_musoe"]},{"has":["life:resident_musoe:work"]},
        {"has":["life:resident_musoe:after"]},{"has":["medkit_musoe"]},{"has":["know_musoe_sick"]},{"has":["somi_secret"]},
        {"has":["somi_trust"]},{"has":["somi_hostile"]},{"has":["ev_b_done"]}]}
    _ak5_steps("life:resident_musoe:crisis",_AK5_MUSOE_SOMI)
    # 약상자: 할아버지가 아프다는 걸 들은 뒤에 건넨다(솜이의 걱정, 솔방울의 약 이야기, 약초 사건).
    _ak5_steps("medkit_musoe",{"any":[{"has":["know_musoe_sick"]},{"has":["somi_worry"]},{"has":["solbang:musoe"]},
        {"has":["somi_secret"]},{"has":["ev_b_done"]},{"has":["musoe_worse"]},{"has":["somi_trust"]},{"has":["somi_hostile"]}]})

    # 네로: 배식 일을 하지 않는다. 같이 사는 사람들이 있다는 걸 들은 뒤에 끼니를 묻는다.
    _ak5_retitle("life:resident_nero:after","같이 지내는 분들 끼니는 괜찮습니까?","같이 지내는 사람들 끼니를 묻는다")
    _ak5_steps("life:resident_nero:after",{"any":[{"has":["knows_job:resident_nero"]},{"has":["bami_away"]},{"has":["bami_hidden_away"]}]})
    # 짐표를 떼는 모습은 창고에서만 보인다. 한 번 물은 뒤로는 어디서든 남는다.
    _ak5_steps("smalltalk:nero_tag",{"any":[_ak5_nero_at_store,{"has":["smalltalk:nero_tag"]}]})

    # 보리: "집의 불도 보러 가셔야 한다고 했죠?"는 보리에게 그 말을 들은 뒤에만.
    _ak5_steps("smalltalk:bori_home",{"any":[_ak5_heard_bori_fire,{"has":["life:resident_bori:work"]},{"has":["smalltalk:bori_home"]}]})

    # 누비: 첫 만남에서는 가족 이야기를 하지 않는다. 제목은 지내는 곳만 묻고, 식구 이야기는 누비가 꺼낸다.
    _ak5_retitle("life:resident_nubi:after","요즘 지내시는 곳은 괜찮습니까?","지내는 곳이 괜찮은지 묻는다")
    # 장작: 집에 아이들이 있다는 걸 모를 때는 "아이들 있는 방부터"라고 하지 않는다.
    _AK5_NUBI_FAMILY={"any":[{"has":["nubi_hostile"]},{"has":["nubi_ally"]},{"has":["grudge_cold:nubi"]},{"has":["nubi_after"]},
        {"has":["wf_fire"]},{"has":["wf_solved"]},{"has":["F12"]},{"has":["life:resident_nubi:after"]},
        {"has":["life:resident_nubi:crisis"]},{"has":["w2_nubi"]}]}
    if "item:firewood" in ROOM13["topics"]:
        _ak5_fw=ROOM13["topics"]["item:firewood"]
        _ak5_fw["variants"]=list(_ak5_fw.get("variants") or [])+[({"not":[]} if False else {"all":[{"any":[_AK5_NUBI_FAMILY]},{"not":["__never__"]}],"__ak5_neg":True},[])][:0]+[
            (lambda_free_cond,[]) for lambda_free_cond in []]
