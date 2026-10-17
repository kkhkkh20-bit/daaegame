# 0.19.x 전체 선택지 검수 2 (소유자 2026-10-17): "미리 뭘 안다는 게 불가해. 말이 되게끔."
#   범위: 무쇠·물결·뭉치·바둑이·밤이·백 부인·보리·부리·부엉이 할아버지·뿔이 촌장·사서·사자 선생님·
#         서리·설이·세련·솔방울·솜이·슬링의 질문.
#   기준: 선택지가 처음 목록에 나올 수 있는 가장 이른 순간에 아빠가 아는 것만 전제한다.
#   틀: systems/room13_threads.rpy (steps / variants / again). 기존 steps는 {"all":[기존, 새 조건]}으로 합친다.
#   조건 함수는 이름 있는 함수로 쓴다.
init 199 python:
    def _rv2_steps(key,cond):
        t=ROOM13["topics"].get(key)
        if t is None:return False
        old=t.get("steps")
        t["steps"]={"all":[old,cond]} if old else cond
        return True

    def _rv2_retitle(key,title,summary):
        t=ROOM13["topics"].get(key)
        if t is None:return False
        t["title"]=title
        R13_QUESTION_SUMMARIES[title]=summary
        return True

    def _rv2_first(key,lines):
        # 제목에 맞춘 첫 대사. 조건 갈래가 이미 있으면 그 뒤(기본 대사 앞)에 붙인다.
        t=ROOM13["topics"].get(key)
        if t is None:return False
        rows=[r for r in (t.get("variants") or []) if r[0] is not None]
        t["variants"]=rows+[(None,list(lines))]
        return True

    def _rv2_prepend(key,cond,lines):
        t=ROOM13["topics"].get(key)
        if t is None:return False
        t["variants"]=[(cond,list(lines))]+list(t.get("variants") or [])
        return True

    # =====================================================================
    # 무쇠 할아버지
    # =====================================================================
    # "밖으로 나가는 길입니까?"는 지도가 바깥길이라는 걸 안다는 전제다. 보이는 건 낡은 지도를 접어 넣는 모습뿐이다.
    # 솜이가 손녀라는 것도 이 자리에서 처음 듣는다.
    _rv2_retitle("life:resident_musoe:work","그 지도는 어디로 가는 길입니까?","무쇠 할아버지의 지도가 어디로 가는 길인지 묻는다")
    _rv2_first("life:resident_musoe:work",[
        ("dad","접어 넣으시는 그 지도는 어디로 가는 길입니까?"),
        ("resident_musoe","마을 밖으로 이어지던 옛날 길이오. 지금도 막히지 않고 열려 있다고는 안 했소."),
        ("dad","그 길을 한번 직접 확인해 보고 싶습니다."),
        ("resident_musoe","내 손녀 솜이를 혼자 보내지만 마시오. 몸이 작다고 틈 사이로 먼저 밀어 넣지도 말고.")])

    # 약상자: 솔방울에게서만 할아버지 약 이야기를 들었으면 솜이가 손녀라는 걸 아직 모른다.
    _RV2_MUSOE_SOMI={"any":[{"has":["knows_job:resident_musoe"]},{"has":["life:resident_musoe:work"]},
        {"has":["life:resident_musoe:after"]},{"has":["somi_worry"]},{"has":["know_musoe_sick"]},{"has":["somi_secret"]},
        {"has":["somi_trust"]},{"has":["somi_hostile"]},{"has":["ev_b_done"]},{"has":["roof_path"]}]}
    def _rv2_musoe_somi_unknown(s):
        return not r13_cond(_RV2_MUSOE_SOMI,s)
    _rv2_prepend("medkit_musoe",_rv2_musoe_somi_unknown,[
        ("resident_musoe","……도시에서 온 약이오? 이 비싼 값을 내가 어떻게 갚소."),
        ("dad","값은 나중 일입니다. 기침부터 잡으십시오."),
        ("resident_musoe","……빚지고는 못 사는 성미요. 이건 폐광 지도요. 빚은 이걸로 먼저 갚겠소.")])

    # =====================================================================
    # 물결
    # =====================================================================
    # "새벽에 물 길러 온 사람"은 아빠가 모르는 사실(새벽에 물 길러 오는 아주머니)을 먼저 꺼낸다.
    # 아빠가 아는 것: 물결이 "강가에서 본 건 다 말해 줄게요"라고 했다. 아빠는 아내를 찾는 중이다.
    _rv2_retitle("mulgyeol:water","강가에서 낯선 사람을 보셨습니까?","강가에서 낯선 사람을 봤는지 묻는다")
    _rv2_first("mulgyeol:water",[
        ("dad","요즘 강가에서 낯선 사람을 보셨습니까?"),
        ("resident_mulgyeol","있었어요. 처음 보는 아주머니였는데, 꼭 해 뜨기 전에 물 길러 왔다가 숲으로 갔어요."),
        ("dad","언제까지 왔습니까?"),
        ("resident_mulgyeol","며칠 전부터 안 와요. 마지막 날엔 뒤를 자꾸 돌아보더라고요."),
        ("resident_mulgyeol","아, 그 아주머니 장갑에 【도토리】 수가 놓여 있었어요. 예뻐서 기억해요.")])
    _rv2_retitle("mulgyeol:water_cold","강가에서 낯선 사람을 보셨습니까?","강가에서 낯선 사람을 봤는지 묻는다")
    _rv2_first("mulgyeol:water_cold",[
        ("dad","요즘 강가에서 낯선 사람을 보셨습니까?"),
        ("resident_mulgyeol","……얼음에 빠졌을 때 지나가던 분이죠? 그때 좀 잡아 주지 그랬어요."),
        ("resident_mulgyeol","처음 보는 아주머니가 해 뜨기 전에 물 길러 왔다가 숲으로 가곤 했어요. 그 이상은 몰라요.")])

    # "그동안 아내 이야기를 들려주셔서 고마웠습니다"는 물결에게 아주머니 이야기를 들은 뒤에만 맞는다.
    _rv2_steps("aft:mulgyeol_met",{"any":[{"has":["mulgyeol:water"]},{"has":["mulgyeol:water_cold"]},{"has":["aft:mulgyeol_met"]}]})

    # =====================================================================
    # 부리 (청소년: 아빠는 부드러운 반말)
    # =====================================================================
    # 제목만 존댓말("없습니다")이고 실제 대사는 "없어."다.
    _rv2_retitle("buri_assert","“다람이가 그랬을 리 없어.”","다람이가 그랬을 리 없다고 말한다")
    # 작업칼 빌리기·돌려주기: 공통 틀의 존댓말 대사를 부리에게 맞춘다.
    _rv2_first("borrow:knife",[
        ("dad","작업칼 좀 잠시 빌려줄 수 있니? 보증금으로 5냥 맡길게."),
        ("buri","조심해서 쓰고 꼭 돌려줘요. 보증금은 그때 돌려드릴게요.")])
    _rv2_first("return:knife",[
        ("dad","덕분에 잘 썼어. 이제 돌려줄게."),
        ("buri","멀쩡하네요. 보증금 여기 있어요.")])

    # =====================================================================
    # 사서 선생님
    # =====================================================================
    # "광장 돌의 옛 기록을 보여 달라"는 기록실에 그 장부가 있다는 걸 안다는 전제다(2일부터, 조건 없음).
    # 있는지부터 묻는다. 장부를 꺼내는 건 사서다.
    _rv2_retitle("librarian_stone","광장 돌에 관한 기록도 있습니까?","광장 돌에 관한 기록이 있는지 묻는다")

    # =====================================================================
    # 슬링
    # =====================================================================
    # 제목("돼요?")과 첫 대사("됩니까?")를 맞춘다.
    _rv2_retitle("aft:sling_out","우체국 일은 어떻게 됩니까?","우체국 일이 어떻게 되는지 묻는다")

    # 너울에게 사정을 전하기: 슬링을 너울에게 알린 길에서는 누가 시켰는지 듣지 못했다.
    # 슬링이 "할머니도 더는 일을 안 주시고요"라고 한 말(말을 걸어 본다)을 들은 뒤에야 짐작할 수 있다.
    # 대사도 단정이 아니라 짐작으로 바꾼다. 이 주제는 라벨(r13_grudge_fix)이 R13_GRUDGES 대사를 쓴다.
    _rv2_steps("grudge_fix:sling",{"any":[{"has":["grudge_cold:sling"]},{"has":["H9"]}]})
    if "sling" in R13_GRUDGES and R13_GRUDGES["sling"].get("fix"):
        _rv2_fx=R13_GRUDGES["sling"]["fix"]
        R13_GRUDGES["sling"]["fix"]=(_rv2_fx[0],_rv2_fx[1],[
            ("dad","슬링 씨 혼자 꾸민 일 같지 않습니다. 일자리를 쥔 사람이 편지를 열게 시켰을 수 있습니다."),
            ("neoul","……시킨 사람이 따로 있다면 이야기가 다르오. 내일부터 다시 나오라 하시오."),
            ("resident_sling","고마워요. 그래도 그날 너울 앞에 저를 세운 건 안 잊을 거예요.")])
