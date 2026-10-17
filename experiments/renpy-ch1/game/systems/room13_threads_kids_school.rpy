# 0.19.17 단서 줄기 데이터: 아이들·학교·아랫길 묶음 (g5_kids_school)
#   밤이, 솜이, 무쇠, 네로, 보리, 누비, 사자 선생님, 종종이, 칼바람, 굴돌, 뿔이 촌장, 너울, 설이.
#   틀: systems/room13_threads.rpy (steps / variants / again / recap / timeless, R13_REACTIONS).
#   원래 대사는 고치지 않는다. 지금 상태와 맞지 않는 첫 대사만 variants로 덮는다.
#   라벨로 도는 주제(약상자·원한 풀기·재판 요구·보증인)는 variants가 쓰이지 않으므로 steps와 recap만 단다.
init 186 python:
    def _g5(key,**kw):
        if key in ROOM13["topics"]:
            ROOM13["topics"][key].update(kw)

    def _g5_daram_held(s):
        return s.get("daram_state")=="held"

    def _g5_before_trial_end(s):
        return s.get("day",1)<=R13_TRIAL_DAY

    def _g5_after_trial(s):
        return s.get("day",1)>R13_TRIAL_DAY

    _G5_MUSOE_HERE={"not":["musoe_gone"]}
    _G5_BORI_MUTE=[(None,"보리는 도담의 작은 신발 한 짝을 쥔 채 고개를 들지 않았다."),
        ("dad","(지금은 아무것도 묻지 않는 게 맞다.)",{"thought":True})]

    # =====================================================================
    # 밤이 (아이, 아빠는 부드러운 반말 / 밤이는 존댓말)
    # =====================================================================
    _g5("life:bami:work",steps={"not":["bami_taken"]},
        variants=[
            ({"has":["bami_watched"]},[
                ("dad","밤에 여기서 자니?"),
                ("bami","잘 수 있을 때만요. 광장 일 뒤로 너울 아저씨가 저를 눈여겨본대요. 그래서 자는 자리를 날마다 바꿔요."),
                ("dad","빈방이 있는지 여관에 물어봐 줄까?"),
                ("bami","제가 어디 있는지는 말하지 마세요. 빈방이 있는지만 물어봐 주세요."),
                ("dad","네가 어디 있는지는 말하지 않을게.")]),
            ({"has":["bami_safe"]},[
                ("dad","밤에 여기서 자니?"),
                ("bami","네. 광장 일 뒤로는 경비 아저씨들이 저를 끌고 가지 않아요. 그래도 문이 닫히면 잘 데를 다시 찾아야 해요."),
                ("dad","빈방이 있는지 여관에 물어봐 줄까?"),
                ("bami","제가 어디 있는지는 말하지 마세요. 빈방이 있는지만 물어봐 주세요."),
                ("dad","네가 어디 있는지는 말하지 않을게.")]),
        ],
        again=[(None,[("bami","아직은 처마 밑이에요. 제가 어디 있는지는 아무한테도 말 안 하셨죠?"),("dad","응. 말하지 않았어.")])])
    _g5("life:bami:after",steps={"not":["bami_taken"]},
        again=[(None,[("bami","아직은 괜찮아요. 탐정님이 안 계실 때도 문으로 누가 드나드는지는 제가 볼게요.")])])
    _g5("life:bami:crisis",steps={"not":["bami_taken"]},
        again=[(None,[("bami","문으로 누가 드나드는지부터요. 따뜻한지는 그다음이에요.")])])
    # 옛 큰 사건 1의 길(네로의 헛간). "그날 13호"는 사건 뒤에만 뜻이 있다.
    _g5("bami_away",steps={"case":"occurred"},
        again=[(None,[("bami","그날은 네로 아저씨네 헛간에 있었어요. 13호 일은 정말 못 봤어요.")])])
    # 13호 목격은 재판(10일)까지의 질문이다. 재판이 끝나면 지나간 질문이 된다.
    _g5("bami_boundary",steps={"all":[{"case":"occurred"},_g5_before_trial_end]},
        variants=[({"has":["bami_friend"]},[
            (None,"내가 수첩을 꺼내자 밤이가 뒤로 물러났다. 이야기를 들으려면 내가 먼저 수첩을 접어야 했다."),
            ("bami","수첩에 적지 마세요. 저 아직 아무 말도 안 했단 말이에요."),
            ("dad","알았어, 적지 않고 듣기만 할게. 밖에서 방 안이 어디까지 보였니?"),
            ("bami","문 쪽은 안 보여요. 제 자리에서 보이는 건 침대 밑하고 그 앞 바닥뿐이에요."),
            ("dad","어디에 숨어서 방 안을 들여다본 거니?"),
            ("bami","처마 밑 틈으로요. 낮게 달린 쇠살 사이로 봤어요. 그래서 방 안 사람 얼굴은 안 보여요."),
            ("dad","방금 말한 건 적어도 될까?"),
            ("bami","제 이름은 빼 주세요. 이름이 적히면 또 저를 검사하러 와요."),
            ("dad","약속할게. 네 이름은 빼고 네가 봤다고 말한 사실까지만 적을게."),
            ("bami","……다람이는 광장에서 저 대신 말해 줬어요. 그러니까 이번 약속은 믿어 볼게요.")])],
        again=[(None,[("bami","말했잖아요. 제 자리에서는 침대 밑하고 그 앞 바닥만 보여요. 문 쪽은 몰라요.")])])
    _g5("bami_saw",steps={"all":[{"case":"occurred"},_g5_before_trial_end]},
        again=[(None,[("bami","소리가 난 뒤로 다람이는 침대 밑에 있었어요. 손에는 아무것도 없었고요."),
            ("bami","소리 나기 전은 못 봤어요. 그건 몇 번을 물으셔도 같아요.")])])
    _g5("item:blanket",timeless=True,
        again=[(None,[("bami","담요는 덮고 자요. 제 이름은 아직 아무한테도 말 안 하셨죠?"),("dad","응. 약속했잖아.")])])

    # =====================================================================
    # 솜이 (아이) · 무쇠 할아버지 (5일 밤 얼음 강으로 간다: musoe_gone)
    # =====================================================================
    _g5("life:resident_somi:work",
        variants=[({"has":["musoe_gone"]},[
            ("dad","어디 다녀왔니?"),
            ("resident_somi","강가요."),
            (None,"솜이는 손바닥을 주먹 쥐었다가 천천히 폈다."),
            ("resident_somi","……이제는 할아버지한테 먼저 갔다고 말할 사람도 없어요."),
            ("dad","그럼 신발은 괜찮니?"),
            ("resident_somi","그건 봐 주셔도 돼요.")])],
        again=[({"has":["musoe_gone"]},[("resident_somi","강가에 또 다녀왔어요. 그냥요.")]),
            (None,[("resident_somi","어디 다녀왔는지는 말 안 해요. 신발은 멀쩡해요.")])])
    _g5("life:resident_somi:after",
        variants=[({"has":["musoe_gone"]},[
            ("resident_somi","어른들은 시키는 대로만 하라면서, 못 하면 왜 못 했냐고 하세요."),
            ("dad","네가 갈 수 있는 길이 어딘지부터 물을게."),
            ("resident_somi","……할아버지도 늘 그렇게 먼저 물어봤어요. 그럼 제가 말할 차례도 있는 거죠?")])],
        again=[(None,[("resident_somi","제가 갈 수 있는 길은 제가 말한다고 했잖아요. 물어봐 주시면 돼요.")])])
    _g5("life:resident_somi:crisis",
        again=[(None,[("resident_somi","내려앉을 데가 있는 길만 갈게요. 그건 제가 정해요.")])])
    _g5("somi_worry",steps=_G5_MUSOE_HERE,
        again=[(None,[("resident_somi","할아버지 기침은 그대로예요. 집에는 오시지 마세요.")])])
    _g5("somi_after_trust",steps=_G5_MUSOE_HERE,
        variants=[({"has":["kd_seori"]},[
            ("resident_somi","할아버지는 진료소에 계세요. 서리 선생님이 보호소 말고 거기 두신대요."),
            ("resident_somi","아까는 저보고 누구냐고 한 번 물으셨어요. ……그래도 손바닥에는 제 이름이 그대로 있어요.")])],
        again=[({"has":["kd_seori"]},[("resident_somi","할아버지는 오늘도 진료소에 계세요. 제 이름은 아직 기억하세요.")]),
            (None,[("resident_somi","할아버지는 오늘도 수프를 조금 드셨어요.")])])
    _g5("somi_after_roof",timeless=True,
        again=[(None,[("resident_somi","굴뚝 옆 판자요. 밤엔 처마 쪽으로 디디세요. 더 알려 드릴 건 없어요.")])])
    _g5("somi_after_hostile",
        variants=[({"has":["musoe_gone"]},[
            (None,"솜이는 내 얼굴을 보자마자 휙 지붕 쪽으로 돌아섰다."),
            ("resident_somi","할아버지 이제 집에 없어요. ……아저씨한테는 할 말 없어요.")])],
        again=[(None,[(None,"솜이는 이번에도 대답하지 않고 지붕 쪽만 보았다.")])])
    # 원한 풀기는 라벨(r13_grudge_fix)이 대사를 맡는다. 할아버지가 떠난 뒤 "약값"은 지나간 말이다.
    _g5("grudge_fix:somi",steps=_G5_MUSOE_HERE,recap="솜이에게 할아버지 약값을 보탰다. 그날 일을 잊어 달라는 뜻은 아니었다")

    _g5("life:resident_musoe:work",steps=_G5_MUSOE_HERE,
        again=[(None,[("resident_musoe","옛날 길이라 했지, 열려 있다고는 안 했소. 솜이를 앞세우지만 마시오.")])])
    _g5("life:resident_musoe:after",steps=_G5_MUSOE_HERE,
        again=[(None,[("resident_musoe","오늘 밤 버틸 방법부터 보시오. 손녀 손이 언다는 말은 했소.")])])
    _g5("life:resident_musoe:crisis",steps=_G5_MUSOE_HERE,
        again=[(None,[("resident_musoe","솜이 날개를 보고 일부터 떠올리지 마시오. 그 말이면 됐소.")])])
    _g5("medkit_musoe",steps=_G5_MUSOE_HERE,recap="무쇠 할아버지에게 약상자를 건넸다. 할아버지는 빚 대신 폐광 지도를 내밀었다")
    _g5("musoe_after_good",steps=_G5_MUSOE_HERE,
        again=[(None,[("resident_musoe","열은 내렸소. 그 지도는 갖고 계시오.")])])
    _g5("musoe_after_bad",steps=_G5_MUSOE_HERE,
        again=[(None,[(None,"무쇠 할아버지는 기침을 참으며 고개를 돌렸다."),("resident_musoe","약 이야기는 그만하시오.")])])

    # =====================================================================
    # 네로 (아랫길)
    # =====================================================================
    _g5("life:resident_nero:work",
        again=[(None,[("resident_nero","표 주인이 찾으러 올 때까지는 안 버려요. 누구한테 알려 줄지는 그때 정하고요.")])])
    _g5("smalltalk:nero_tag",timeless=True,
        again=[(None,[("resident_nero","짐이랑 짐표는 같이 외워 둬요. 이름은 큰 소리로 부르지 마시고요.")])])
    _g5("life:resident_nero:after",
        again=[(None,[("resident_nero","이름 없는 그릇은 오늘도 하나 놔뒀어요. 누구 몫인지는 묻지 마세요.")])])
    _g5("life:resident_nero:crisis",
        variants=[
            ({"has":["nero_alive"]},[
                ("resident_nero","그날 밤 다 못 데려왔어요. 이름표만 남은 사람이 있어요."),
                ("dad","명단만 보고 사람을 가르지는 않겠습니다."),
                ("resident_nero","그 말, 이번엔 문 앞에서도 지켜 주세요.")]),
            ({"has":["ws_tents_school"]},[
                ("resident_nero","선생님이 이름표를 보고 뒷문을 열어 줬어요. 이름부터 대라는 말은 안 하더군요."),
                ("dad","명단에 없는 사람도 그렇게 들어갈 수 있어야 합니다."),
                ("resident_nero","오늘 밤만이 아니라 내일도요. 그걸 지켜보겠습니다.")]),
        ],
        again=[(None,[("resident_nero","명단만 보고 가르지 않겠다고 하셨죠. 문 앞에서 확인하겠습니다.")])])
    _g5("life:resident_nero:privacy",
        again=[(None,[("resident_nero","그 종이는 다른 사람 앞에 펼치지 마세요. 길은 아는데, 입은 따로 다뭅니다.")])])
    _g5("ep5:st_nero_after",steps={"has":["nero_alive"]},
        again=[(None,[("resident_nero","오늘도 이름표를 꿰맨다. 다음엔 이름을 보고 찾아올 수 있게.")])])

    # =====================================================================
    # 보리 (어른, 존댓말 / 사건 뒤 거친 반말이 섞인다)
    # =====================================================================
    _g5("life:resident_bori:work",
        variants=[({"has":["wf_fire"]},[
            (None,"보리는 붕대 감은 손으로 장작 지게 끈을 붙들고 있었다."),
            ("dad","그 손으로 짐을 지시려고요?"),
            ("resident_bori","데인 건 손바닥이에요. 등은 멀쩡하고요."),
            ("resident_bori","장작 나르는 일 말고는 할 줄 아는 게 없어요. 대피소에 맡긴 우리 애 몫도 벌어야 하고요.")])],
        again=[({"has":["wf_fire"]},[("resident_bori","손은 아물고 있어요. 짐은 나눠서 질게요.")]),
            (None,[("resident_bori","나눠서 실으면 언덕을 두 번 올라야 해요. 그동안 우리 집 불은 누가 보는데요.")])])
    _g5("smalltalk:bori_bundle",timeless=True,
        again=[(None,[("resident_bori","길이가 비슷한 것끼리요. 한쪽으로 쏠리면 매듭부터 다시 봐요.")])])
    _g5("smalltalk:bori_home",timeless=True,
        again=[(None,[("resident_bori","부탁하실 일이 있으면 제가 언제 돌아가야 하는지부터 물어봐 주세요.")])])
    _g5("life:resident_bori:after",
        variants=[({"has":["bori_adopts"]},[
            ("resident_bori","우리 집에 애가 셋 늘었어요. 대피소를 만든다고 그 집 난로 불부터 끄라는 말씀이시라면 전 안 들을래요."),
            ("dad","불을 끄라는 부탁은 드리지 않았습니다."),
            ("resident_bori","알아요. 그래도 다들 부탁하기 전에 짐을 질 제 어깨부터 쳐다보시거든요.")])],
        again=[(None,[("resident_bori","불 끄라는 말은 아직 안 하셨죠. 그럼 됐어요.")])])
    _g5("life:resident_bori:crisis",
        variants=[({"has":["bori_mute"]},list(_G5_BORI_MUTE)),
            ({"has":["dodam_dead"]},[
                ("resident_bori","짐이요? 들 수 있어요. 대신 우리 집 애들 누울 자리부터요."),
                ("dad","댁의 가족이 머물 자리부터 확인하겠습니다."),
                ("resident_bori","……하나 잃었어요. 남은 애들까지 문 앞에 세워 두진 않을 거예요.")])],
        again=[({"has":["bori_mute"]},[(None,"보리는 이번에도 대답하지 않았다.")]),
            (None,[("resident_bori","식구들 누울 자리부터 확인해 주시면 어깨는 빌려드려요.")])])
    _g5("life:resident_bori:changed",
        variants=[({"has":["bori_mute"]},[
            (None,"보리는 말없이 수레 손잡이를 쥐었다. 수레 바닥에 작은 신발 한 짝이 놓여 있었다."),
            ("dad","오늘 밤까지 맡아 달라는 뜻은 아닙니다."),
            (None,"보리가 아주 작게 고개를 끄덕였다.")])],
        again=[({"has":["bori_mute"]},[(None,"보리는 대답 대신 수레 손잡이를 다시 쥐었다.")]),
            (None,[("resident_bori","수레는 가져올게요. 오늘 밤까지라는 말만 안 하시면요.")])])
    # 둘째 주 진행 주제(transport_terms). 대사만 지금 상태에 맞춘다.
    _g5("w2_bori",
        variants=[({"has":["bori_mute"]},[
            (None,"보리는 대답 대신 수레 손잡이를 쥐었다. 도담의 신발 한 짝이 수레 바닥에 놓여 있었다."),
            ("dad","댁의 가족이 누울 자리부터 먼저 확인하겠습니다."),
            (None,"보리가 아주 작게 고개를 끄덕였다.")])],
        again=[({"has":["bori_mute"]},[(None,"보리는 고개만 끄덕였다.")]),
            (None,[("resident_bori","누울 자리부터 확인해 주세요. 우리 식구를 문 앞에 세워 두면 안 해요.")])])
    # 배급 일(ev_e) 뒤 안부. 아이를 잃은 뒤에는 묻지 않는다.
    _g5("bori_after",steps={"not":["dodam_dead"]},
        again=[(None,[("resident_bori","그날 누가 나서 줬으니 장작 수레는 지켰어요. 그거면 됐어요.")])])
    _g5("ep5:st_bori_after",steps={"has":["ws_kids_alive"],"not":["dodam_dead"]},
        again=[(None,[("resident_bori","도담이? 오늘도 수프 한 그릇 다 먹었다.")])])
    _g5("medkit_bori",steps={"not":["dodam_dead","bori_child_cured"]},recap="보리네 아이에게 약상자를 썼다")

    # =====================================================================
    # 누비 (빨래터, ③의 불)
    # =====================================================================
    _g5("life:resident_nubi:work",
        variants=[({"all":[{"has":["wf_fire"]},{"not":["wf_done"]}]},[
            (None,"누비 아주머니는 젖은 천으로 손을 감은 채 빨래 표를 고르고 있었다."),
            ("dad","빨래 묶음마다 달린 표가 다르네요."),
            ("resident_nubi","한 가족은 같은 표를 써요. 돌려줄 때 헤매지 않으려고요."),
            ("resident_nubi","……오늘은 빨래를 많이 못 받아요. 손을 좀 다쳐서요.")])],
        again=[(None,[("resident_nubi","한 가족은 같은 표예요. 이름은 안 적어요. 밖에 널면 다 읽으니까요.")])])
    _g5("life:resident_nubi:after",
        variants=[({"all":[{"has":["wf_solved"]},{"not":["nubi_taken"]}]},[
            (None,"누비는 손등의 물집을 소매로 가렸다."),
            ("resident_nubi","용기 내라는 말은 많이 들었어요. 이제 저한테는 그 말도 안 하더군요."),
            ("dad","그럼 아주머니 식구들이 머물 곳부터 보겠습니다."),
            ("resident_nubi","저만 말고요. 집에 남을 애들 자리도요.")])],
        again=[(None,[("resident_nubi","저만 말고 집에 남을 식구들 자리도요. 그 말은 했어요.")])])
    _g5("life:resident_nubi:crisis",
        again=[(None,[("resident_nubi","가족이 같이 머물 자리가 먼저 보이면 움직일 수 있어요.")])])
    _g5("item:firewood",timeless=True,
        variants=[({"has":["F12"]},[
            ("dad","장작 묶음입니다. 아이들 있는 방부터 데우세요."),
            ("resident_nubi","……장작이요."),
            (None,"누비는 장작을 받아 들고 한참 내려다보았다."),
            ("resident_nubi","이게 그때 있었으면…… 아니에요. 아이들 방부터 데울게요.")])],
        again=[(None,[("resident_nubi","주신 장작으로 아이들 방은 데웠어요.")])])
    _g5("nubi_after",steps={"not":["nubi_taken"]},
        variants=[({"any":[{"has":["F12"]},{"has":["wf_solved"]}]},[
            ("resident_nubi","너울 님 부탁이요? ……장작 얘기만이 아니었다는 건 이제 아시잖아요."),
            ("resident_nubi","그 애들 몫을 준다는 말까지 들었어요. 다시는 그 사람 말 안 들어요."),
            ("resident_nubi","제 이름은 이제 숨길 수도 없네요.")])],
        again=[({"any":[{"has":["F12"]},{"has":["wf_solved"]}]},[("resident_nubi","그 사람 약속은 이제 안 들어요. 더 할 말은 없어요.")]),
            (None,[("resident_nubi","이젠 그런 일 안 해요. 그 사람 앞에서 제 이름만 꺼내지 말아 줘요.")])])
    # 엄마 소문: 엄마가 맡긴 봉투를 읽기 전까지만 묻는 질문이다.
    _g5("rumor_mom:nubi",steps={"thread":"mom","max":4},
        again=[(None,[("resident_nubi","식당에서 흘려들은 게 다예요. 누가 한 말인지는 정말 몰라요.")])])
    _g5("grudge_cold:nubi",steps={"not":["nubi_taken"]},
        again=[(None,[("resident_nubi","장작은 아직 끊긴 그대로예요.")])])
    _g5("grudge_fix:nubi",steps={"not":["nubi_taken"]},recap="누비네 끊긴 장작 값을 대신 냈다")
    _g5("w2_nubi",
        again=[(None,[("resident_nubi","집에 남은 식구들 자리부터요. 그게 되면 제가 지키는 문도 말씀드릴게요.")])])
    _g5("w2_laundry",
        again=[(None,[("resident_nubi","약속한 사람이 안 나오면 그냥 돌아서요. 안에서 오래 기다리면 들켜요.")])])

    # =====================================================================
    # 사자 선생님 (학교·대피소)
    # =====================================================================
    _g5("life:resident_teacher:work",
        variants=[
            ({"all":[{"has":["kkomi_dead"]},{"has":["F13"]}]},[
                ("dad","이 추위에도 수업은 계속합니까?"),
                ("resident_teacher","해요. 오늘은 출석부 맨 위 이름을 부르지 못했어요."),
                ("resident_teacher","이름을 적어 두기만 하면 지켜 줄 수 있다고 생각했나 봐요.")]),
            ({"has":["kkomi_dead"]},[
                ("dad","이 추위에도 수업은 계속합니까?"),
                ("resident_teacher","해요. 학교 뒤 창고에서 아이가 죽었다는데, 저는 그 아이 이름도 몰랐어요."),
                ("resident_teacher","그래서 오늘은 출석을 더 천천히 불렀어요.")]),
            ({"all":[{"has":["wf_fire"]},{"has":["kids_school"]}]},[
                ("dad","이 추위에도 수업은 계속합니까?"),
                ("resident_teacher","해요. 창고에서 나온 아이들이 이제 학교 돌창고에서 자요. 수업도 같이 듣고요."),
                ("resident_teacher","아침마다 이름을 부르면 다들 대답해요. 그게 요즘 제일 좋은 일이에요.")]),
        ],
        again=[(None,[("resident_teacher","교실이 따뜻할 때까지는 해요. 손이 굳으면 다 같이 일어나 걷고요.")])])
    _g5("life:resident_teacher:after",
        again=[(None,[("resident_teacher","아이들 자리를 지키면서 환자 자리를 찾는 거라면 같이 보지요.")])])
    # 대피소 준비 질문은 수프(12일 저녁) 전까지. 그 뒤는 지나간 질문이다.
    _g5("life:resident_teacher:crisis",steps={"not":["ws_soup","teacher_on_cart"]},
        again=[(None,[("resident_teacher","자리가 비기 전에는 약속하지 않겠다고 하셨죠. 그 약속이면 돼요.")])])
    _g5("life:resident_teacher:changed",steps={"not":["ws_soup","teacher_on_cart"]},
        again=[(None,[("resident_teacher","이름을 못 쓰시는 분은 제가 대신 적어요. 그걸로 못 들어오는 분은 없어요.")])])
    _g5("w2_school",
        again=[(None,[("resident_teacher","책상만 옮긴다고 끝나지 않아요. 밥과 밤에 남을 사람까지 같이 정해요.")])])
    _g5("w2_school_vouch",recap="선생님에게 보증해 줄 사람을 데려갔다")
    # 표 없는 아이들: 출석부(F13)가 이미 있으면 같은 장면을 되풀이하지 않는다.
    #   불이 난 뒤에는 "이름 넷"을 쓰지 않는다(꼬미가 죽은 판이 있다). 기록 F13의 글은 고치지 않았다(보고서).
    _g5("teacher_kids",steps={"not":["F13"]},
        variants=[({"has":["wf_fire"]},[
            ("resident_teacher","표가 없는 아이들이요? ……창고가 타고 나서야 그 아이들 얘기를 하게 되네요. 저도 늦었고요."),
            ("resident_teacher","남은 아이들 이름은 학생 명부에 올리겠어요. 그러면 촌장님도 함부로 못 뺍니다."),
            (None,"선생님이 출석부 맨 아래 빈 줄에 이름을 적어 내려갔다."),
            ("dad","(이 종이를 그 아이들이 믿어 줄까?)",{"thought":True})])],
        again=[({"has":["kkomi_dead"]},[("resident_teacher","명부에 올린 이름은 그대로예요. 맨 위 줄은 비워 두었어요.")]),
            (None,[("resident_teacher","명부에 올린 이름은 그대로예요. 오늘 아침에도 불렀어요.")])])
    _g5("ep5:st_teacher_after",steps={"has":["teacher_alive"]},
        again=[(None,[("resident_teacher","오늘도 아이들이 서로 이름을 불렀어요. 빈자리가 없었어요.")])])

    # =====================================================================
    # 뿔이 촌장 (하오체)
    # =====================================================================
    _g5("life:resident_ppul:work",
        again=[(None,[("resident_ppul","확인 안 된 숫자는 말하지 않겠소. 자기 몫을 지키면 버틴다는 말까지만 하오.")])])
    _g5("life:resident_ppul:after",
        again=[(None,[("resident_ppul","마련하러 왔다는 것과 마련했다는 것은 다르오. 잘 곳을 보여 주시오.")])])
    _g5("life:resident_ppul:crisis",
        again=[(None,[("resident_ppul","잠자리와 먹을 것을 보여 주시오. 그 뒤에 이야기하겠소.")])])
    # "재판"은 13호 사건(7일) 뒤에야 있다.
    _g5("ppul_hearing",steps={"case":"occurred"},recap="촌장에게 재판을 증거대로 열고 판결대로 집행해 달라고 했다")
    _g5("ppul_names",timeless=True,
        again=[(None,[("resident_ppul","그 종이는 거두어 두시오. 맨 아래 이름은 내가 차마 못 지운 이름이오.")])])
    _g5("grudge_cold:ppul",
        variants=[(_g5_after_trial,[("resident_ppul","재판은 끝났소. 장부 일은 나도 아직 잊지 않았소.")])],
        again=[(None,[("resident_ppul","할 말은 했소. 그 이상은 기대하지 마시오.")])])
    _g5("grudge_fix:ppul",timeless=True,recap="장부로 촌장을 몰아세운 일을 사과했다")

    # =====================================================================
    # 너울 (하오체·합쇼체)
    # =====================================================================
    _g5("life:neoul:work",
        again=[(None,[("neoul","기다리라고 할 때는 있소. 그 말에 책임이 없다고 하진 않겠소.")])])
    _g5("life:neoul:after",
        variants=[(lambda s:s.get("case_state")=="occurred" and s.get("daram_state") in ("with_dad","rescued") and s.get("day",1)>R13_CASE_DAY,[
            ("neoul","기록은 남아 있습니다. 아이를 보호실에 둔 기록도, 아이가 나간 날도 제 글씨입니다."),
            ("dad","위에서 시킨 일이라고만 적을 수도 있었을 텐데요."),
            ("neoul","시킨 사람이 있어도 보호실 문을 잠근 건 저입니다. 명령만 있었다고 적지는 마십시오.")])],
        again=[(None,[("neoul","보호실 기록은 제 글씨요. 명령만 있었다고 적지 마시오.")])])
    _g5("life:neoul:crisis",
        again=[(None,[("neoul","확인한 사실을 남기는 거라 하셨소. 내 이름도 지우지 마시오.")])])
    # 아이가 보호실에 있는 동안만 묻는 질문이다.
    _g5("neoul_custody",steps={"all":[{"case":"occurred"},_g5_daram_held]},
        again=[(None,[("neoul","만남에는 내가 같이 있겠소. 아이가 한 말은 고친 것까지 그대로 적소.")])])
    _g5("w2_stay_order",
        again=[(None,[("neoul","이 명령은 어른 환자 셋에 대한 거요. 아이 명령은 다음 장에 따로 있소.")])])

    # =====================================================================
    # 설이 (종탑)
    # =====================================================================
    _g5("life:resident_seol:work",
        again=[(None,[("resident_seol","종소리 뜻은 말로도 알려야 해요. 다들 안다고 치면 안 돼요.")])])
    _g5("life:resident_seol:after",
        again=[(None,[("resident_seol","한 번 치면 통행, 길게 치면 대피. 오늘은 틀리면 안 돼요.")])])
    _g5("life:resident_seol:crisis",
        again=[(None,[("resident_seol","크게 치는 건 쉬워요. 헷갈리지 않게 치는 게 어렵지요.")])])
    # 초롱이 살아 있는 동안의 새벽 이야기(현재형).
    _g5("smalltalk:seol_rope",steps={"not":["chorong_dead"]},
        again=[(None,[("resident_seol","새벽엔 끈부터 다시 매요. 초롱 씨는 오늘도 북쪽 길 끝 등 하나만 보고 갔어요.")])])

    # =====================================================================
    # 굴돌 · 종종이 · 칼바람 (새 인물)
    # =====================================================================
    _g5("guldol:stone",timeless=True,
        again=[(None,[("resident_guldol","깨진 돌을 붙이는 정도요. 새로 만드는 법은 나도 모르오.")])])
    # 아빠가 할머니의 속을 먼저 단정하지 않는다: 물음으로 바꾸고, 굴돌은 본 것까지만 말한다.
    _g5("guldol:works",steps={"has":["ancient_found"]},
        variants=[(None,[
            ("dad","여관 아래에 돌을 만들던 시설이 있었습니다."),
            ("resident_guldol","……결국 그걸 봤구먼."),
            ("resident_guldol","거기가 멈춘 건 지금 여관 할머니의 어머니 대요. 그분이 【룬】을 마지막으로 읽던 사람이었소."),
            ("resident_guldol","그분이 돌아가시고 나서 아무도 벽의 글을 못 읽었지. 할머니는 평생 그걸 다시 읽을 사람을 찾았소."),
            ("dad","그래서 할머니가 아내를 이 마을에 붙잡아 두려 한 겁니까?"),
            ("resident_guldol","그건 할머니한테 물으시오. 나는 내가 본 것까지만 말했소.")])],
        again=[(None,[("resident_guldol","그 시설이 멈춘 건 할머니 어머니 대요. 그 이상은 할머니가 답할 일이오.")])])
    _g5("jongjong:work",timeless=True,
        again=[(None,[("resident_jongjong","오늘도 뛰어요! 봉투는 절대 안 열어요.")])])
    _g5("jongjong:envelope",steps={"has":["poc:letter_conflict"]},
        variants=[
            ({"has":["poc:granny_explained"]},[
                ("dad","혹시 여관 할머니가 맡긴 봉투를 부친 적 있니?"),
                ("resident_jongjong","있어요! 눈 오기 전에요. 할머니가 직접 우체국까지 오시기 힘들다고 저한테 줬어요."),
                ("dad","봉투에 뭐가 그려져 있었니?"),
                ("resident_jongjong","아무것도요. 그냥 하얀 봉투였어요. 받는 사람 이름만 엄청 또박또박 써 있었어요."),
                ("dad","(할머니는 아내 말을 받아 적어 부쳤다고 했다. 아내가 정말 부탁했다면, 왜 도토리 표식 하나 없었을까?)",{"thought":True})]),
            (None,[
                ("dad","혹시 여관 할머니가 맡긴 봉투를 부친 적 있니?"),
                ("resident_jongjong","있어요! 눈 오기 전에요. 할머니가 직접 우체국까지 오시기 힘들다고 저한테 줬어요."),
                ("dad","봉투에 뭐가 그려져 있었니?"),
                ("resident_jongjong","아무것도요. 그냥 하얀 봉투였어요. 받는 사람 이름만 엄청 또박또박 써 있었어요."),
                ("dad","(도토리 표식이 없는 하얀 봉투. 우리 집으로 온 그 편지도 그 봉투였을까?)",{"thought":True})]),
        ],
        again=[(None,[("resident_jongjong","하얀 봉투였어요. 이름만 또박또박. 그것밖에 기억 안 나요.")])])
    _g5("kalbaram:edge",timeless=True,
        again=[(None,[("resident_kalbaram","봄 전엔 길이 없소. 가지 마시오.")])])
    _g5("alibi:night1:resident_kalbaram",timeless=True,
        again=[(None,[("resident_kalbaram","말하지 않았소. 덫을 보고 내려오다 토끼 아이를 여관까지 데려다줬소. 그게 다요.")])])

    # =====================================================================
    # 증거 반응: 그 인물 자리에서 확인되는 것과 확인되지 않는 것
    # =====================================================================
    R13_REACTIONS.update({
        # 밤이: 자기가 한 말, 자기를 둘러싼 소문과 자국
        ("bami","E10"):[(None,[("bami","제가 말한 그대로네요. 소리 난 뒤에 다람이가 침대 밑에 있었던 거요."),
            ("bami","처음에 누가 촛대를 들었는지는 거기 없어요. 저는 그걸 못 봤으니까요.")])],
        ("bami","K01"):[(None,[("bami","콩이가 그랬어요? ……콩이도 본 게 아니라 들은 거잖아요."),
            ("bami","누가 처음 그 말을 했는지는 저도 몰라요.")])],
        ("bami","K02"):[(None,[("bami","어깨쯤이요? 저는 돌목 아저씨 허리에도 안 닿아요."),
            ("bami","그래도 누가 물었는지는 저도 못 봤어요.")])],
        ("bami","K03"):[(None,[("bami","제가 한 말이에요. 그날 밤엔 처마 위에서 별을 봤어요."),
            ("bami","비틀비틀 가던 할아버지가 누구인지는 몰라요. 얼굴은 안 보였어요.")])],
        ("bami","K09"):[(None,[("bami","제 자리 눈이 안 쓸렸어요? ……날아오르면 날개가 눈을 쓸어요. 그날은 안 날았어요."),
            ("bami","기둥 타고 처마 밑으로만 내려갔어요.")])],
        # 너울: 자기 말과 명단. 인정할 수 있는 데까지만.
        ("neoul","F01"):[(None,[("neoul","엿들으셨소? ……'줄면'이라고 했지, 없애라고 한 적은 없소."),
            ("neoul","그 말을 누가 어떻게 들었는지까지 내가 책임질 일은 아니오.")])],
        ("neoul","F12"):[(None,[("neoul","저 여자 말뿐이오."),
            ("neoul","내가 무엇을 약속했는지 적힌 종이가 있다면 그때 다시 오시오.")])],
        ("neoul","N02"):[(None,[("neoul","회관 뒤에서 엿들으셨소?"),
            ("neoul","내가 받은 부탁을 외지 사람에게 하나하나 풀어 줄 까닭은 없소.")])],
        ("neoul","Y10"):[(None,[("neoul","명단은 위에서 내려온 대로 적었소."),
            ("neoul","수레가 어디로 가는지는 내가 정하는 일이 아니오.")])],
        # 보리: 자기 손, 자기를 두고 나온 말들, 자기 집
        ("resident_bori","F04"):[(None,[("resident_bori","불붙은 판자를 붙잡고 뜯었어요. 그래서 손바닥만 데었고요."),
            ("resident_bori","장작 훔친 건 맞아요. 그건 이 손으로도 못 지워요.")])],
        ("resident_bori","F08"):[({"has":["kkomi_dead"]},[("resident_bori","애들이 그렇게 말했어요? ……뒷벽 부순 건 맞아요."),
                ("resident_bori","셋은 꺼냈어요. 하나는 못 꺼냈고요. 문 쪽이 왜 먼저 탔는지는 저도 몰라요.")]),
            (None,[("resident_bori","뒷벽 부순 건 저예요. 문 쪽이 먼저 빨갰던 건 맞아요."),
                ("resident_bori","누가 문 쪽에 불을 냈는지는 저도 못 봤어요.")])],
        ("resident_bori","F14"):[(None,[("resident_bori","선생님이 그렇게 말해 줬어요? ……저는 안에 애들이 있는 줄 알았어요."),
            ("resident_bori","그래서 뒷벽을 뜯은 거예요. 장작 훔치러 간 길이긴 했어도요.")])],
        ("resident_bori","W8"):[(None,[("resident_bori","장작은 나르는 사람이 먼저 지는데, 우리 집 몫은 장부대로예요. 그래서 난로가 꺼져 있었죠."),
            ("resident_bori","어머니 기침이 추위 탓인지는 서리 선생님한테 물어보세요. 저는 몰라요.")])],
        # 굴돌: 엄마와 함께 적은 실험 기록
        ("resident_guldol","Y07"):[(None,[("resident_guldol","부인과 내가 같이 적은 종이요. 조각을 모아 두고 밤마다 손을 대 봤지. 식지 않았소."),
            ("resident_guldol","그걸로 마을 돌을 얼마 동안 데울 수 있는지는 나도 모르오. 그건 부인이 셈한 거요.")])],
        # 무쇠: 자기가 건넨 지도, 자기 손바닥
        ("resident_musoe","H5"):[(None,[("resident_musoe","내가 드린 폐광 지도요. 옛날에 쓰던 굴이지."),
            ("resident_musoe","지금도 막히지 않았는지는 나도 모르오. 솜이를 앞세워 들어가지만 마시오.")])],
        ("resident_musoe","K05"):[(None,[(None,"무쇠 할아버지는 종이를 한참 보다가 자기 손바닥을 폈다."),
            ("resident_musoe","……솜이. 솜이 이름이오. 잊기 전에 적어 둔 거요.")])],
        # 네로: 자기가 준 이름표, 자기가 꿰맨 꾸러미
        ("resident_nero","K08"):[(None,[("resident_nero","제가 그 꼬마한테 쥐여 준 거예요. 이름은 잃어버리면 안 되니까요."),
            ("resident_nero","누구 이름인지는 묻지 마세요. 주인이 찾으러 오면 그때 말할게요.")])],
        ("resident_nero","Y09"):[({"has":["nero_alive"]},[("resident_nero","그날 밤 천막에 있던 사람들 이름이에요. 못 데려온 사람 것도 있어요."),
                ("resident_nero","이름이 있으니까 아무도 '이름 모름'이 아니에요.")])],
        # 누비: 자기가 들은 소문
        ("resident_nubi","J12"):[(None,[("resident_nubi","제가 식당에서 흘려들은 말이에요. 누가 했는지는 정말 기억이 안 나요."),
            ("resident_nubi","부인을 직접 본 건 아니에요. 그것만은 분명히 해 주세요.")])],
        # 솜이: 할아버지의 자국
        ("resident_somi","K04"):[({"has":["kd_named"]},[("resident_somi","그거 보고 할아버지 이름 말한 거잖아요. ……이제 됐어요?")]),
            (None,[("resident_somi","할아버지 발이에요. 신발도 안 신고 나가셨어요."),
                ("resident_somi","……저는 알고 있었어요. 그래서 숨긴 거예요.")])],
        ("resident_somi","K05"):[(None,[("resident_somi","할아버지가 제 이름 잊지 않으려고 쓴 거예요. 손바닥이 새까매질 때까지요.")])],
        ("resident_somi","K06"):[(None,[("resident_somi","제가 바로 앞에 있는데, 손녀랑 닮았대요."),
            ("resident_somi","언제부터 그랬는지는…… 꽤 됐어요. 말하면 할아버지를 데려갈까 봐 못 했어요.")])],
        # 사자 선생님: 자기가 적은 출석부, 자기가 한 말
        ("resident_teacher","F13"):[({"has":["kkomi_dead"]},[("resident_teacher","제가 적은 출석부예요. 맨 위 이름은…… 이제 제가 부를 수가 없네요."),
                ("resident_teacher","이름을 적은 것과 지켜 준 것은 달랐어요.")]),
            (None,[("resident_teacher","제가 적은 출석부예요. 이름이 올라 있으면 우리 학교 아이예요."),
                ("resident_teacher","아이들이 실제로 오는지는 아이들이 정해요. 저는 자리를 비워 둘 뿐이에요.")])],
        ("resident_teacher","F14"):[(None,[("resident_teacher","제가 한 말 그대로예요. 그 밤 아이들은 학교 돌창고에 있었어요. 제가 증인이에요."),
            ("resident_teacher","창고 문 앞에서 무슨 일이 있었는지는 저도 보지 못했어요.")])],
        # 아이들: 자기 이름, 자기 말
        ("kid_bang","Y12"):[(None,[("kid_bang","약장은 어른만 열 수 있어. 나는 몰라.")])],
        ("kid_kkomi","F13"):[({"not":["kkomi_dead"]},[("kid_kkomi","맨 위가 내 이름이야? ……대장이니까 맨 위지."),
                ("kid_kkomi","그래도 학교에서 자도 되는지는 동생들한테 먼저 물어볼 거야.")])],
        ("kid_nubi1","F11"):[(None,[("kid_nubi1","내가 한 말이야. ……엄마 혼나?"),
            ("dad","네가 본 대로 말해 준 거야. 그건 잘못이 아니란다.")])],
        ("kid_saemi","Y13"):[(None,[("kid_saemi","응, 내가 그랬어. 쓴맛이 나서 남겼어."),
            ("kid_saemi","왜 쓴맛이 났는지는 몰라.")])],
    })
