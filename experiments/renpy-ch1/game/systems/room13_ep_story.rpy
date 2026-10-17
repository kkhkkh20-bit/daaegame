# 0.18.90 서사 보강 (소유자 2026-10-16: 잃음보다 "그들도 애썼다"는 게 남게)
# - 쌓는 장면: 위기 전에 그 사람이 무엇을 지키며 사는지 짧게 보인다. 모두 선택이다.
# - 구한 뒤: 살린 사람을 나중에 찾아가면 바뀐 행동과 생각이 보인다. 고맙다는 인사는 따로 넣지 않는다.
# 회의·증거·조건은 바꾸지 않는다. 주제 키는 날짜표가 옮기지 않는 에피소드 접두사(ep1: 등)를 쓴다.
init 158 python:
    def r13_st_topic(npc,title,day,need=(),not_flags=(),flags=(),lines=()):
        return dict(npc=npc,title=title,day=list(day),need=list(need),not_flags=list(not_flags),flags=list(flags),give=[],lines=list(lines))

    ROOM13["topics"].update({
        # ---- 쌓는 장면 ----
        "ep1:st_piko_faces":r13_st_topic("resident_piko","판자에 누구를 그리고 있어요?",(1,2),flags=["st_piko_faces"],lines=[
            ("resident_piko","광장에서 자는 사람들 얼굴이요. 돈은 안 받아요."),
            ("resident_piko","겨울을 넘기면 얼굴이 바뀌잖아요. 못 넘기면…… 아무도 그 얼굴을 기억 못 하고요."),
            ("resident_piko","그래서 그려 둬요. 판자 한 장에 한 사람씩. 다 그리기 전엔 저도 못 가요."),
            ("dad","(가진 것 없는 사람이 남의 얼굴을 지키고 있다.)",{"thought":True})]),
        "ep4:st_ttadak_boards":r13_st_topic("resident_ttadak","판자를 많이 사 두셨네요",(2,8),not_flags=["ttadak_dead"],flags=["st_ttadak_boards"],lines=[
            ("resident_ttadak","아랫길 네로 아저씨네 천막에 댈 거예요. 바람이 숭숭 들어와서 애들이 밤새 기침해요."),
            ("resident_ttadak","여관 일은 일당이 두 배라 거절 못 해요. 판자 값은 어떻게든 벌어야죠."),
            ("resident_ttadak","저는 판자를 늘 반 치씩 길게 잘라요. 모자라는 것보다 남는 게 낫거든요."),
            ("dad","(남는 판자는 결국 남의 천막으로 간다.)",{"thought":True})]),
        "ep6:st_momo_glasses":r13_st_topic("resident_momo","늘 안경을 품에 넣고 다니시네요",(2,12),flags=["st_momo_glasses"],lines=[
            ("resident_momo","제 안경이 아니에요. 첫 겨울에 보호소로 간 동생 거예요."),
            ("resident_momo","옛 마을 물건이라면 뭐든 산다고들 흉보죠. 사람은 가도 물건은 남으니까, 그거라도 붙잡아 두는 거예요."),
            ("resident_momo","언젠가 누가 ‘이건 누구 것이었소’ 하고 물어봐 주면 좋겠어요. 그럼 그 이름을 한 번 더 말할 수 있으니까요.")]),
        # ---- 구한 뒤 찾아가면 ----
        "ep1:st_piko_after":r13_st_topic("resident_piko","몸은 좀 괜찮아요?",(4,14),need=["piko_survived"],flags=["st_piko_after"],lines=[
            ("resident_piko","손가락이 아직 좀 굳었어요. 그래도 붓은 쥐어져요."),
            ("resident_piko","이제 등 밑에서 안 자요. 겨울 동안 쉴 자리를 얻었어요."),
            ("resident_piko","요즘은 등 밑에서 자는 사람들 얼굴을 그려서 이름이랑 같이 등지기한테 맡겨요."),
            ("resident_piko","쓰러져 보니까 알겠더라고요. 얼굴만 남기면 안 돼요. 누가 찾아와 줘야 해요.")]),
        "ep1:st_lib_after":r13_st_topic("resident_librarian","기록실은 이제 따뜻해요?",(4,14),need=["lt_lib_saved"],flags=["st_lib_after"],lines=[
            ("resident_librarian","기록을 세 벌로 베끼고 있어요. 한 벌은 학교에, 한 벌은 진료소에 둘 거예요."),
            ("resident_librarian","혼자 지키다 혼자 얼어 죽을 뻔했잖아요. 기록은 나눠 들어야 오래 남는다는 걸 그날 배웠어요.")]),
        "ep4:st_chorong_after":r13_st_topic("resident_lamplighter","요즘 밤길은 괜찮아요?",(9,14),need=["nt_chorong_safe"],not_flags=["badook_dead"],flags=["st_chorong_after"],lines=[
            ("resident_lamplighter","요즘 밤 순회는 바둑이 씨랑 같이 돌아요."),
            ("resident_lamplighter","편지는 여전히 제가 직접 전해요. 그건 안 바꿔요. 다만 이제 혼자 가지는 않아요."),
            ("resident_lamplighter","그날 밤 누가 기다리고 있었다는 걸 알고 나니까 지름길이 다 무서워졌어요. 그래도 등은 켜야죠.")]),
        "ep4:st_ttadak_after":r13_st_topic("resident_ttadak","판자 문은 어떻게 했어요?",(11,14),need=["nt_ttadak_safe"],flags=["st_ttadak_after"],lines=[
            ("resident_ttadak","판자 문 안쪽에 손잡이를 달았어요. 안에서도 열리게요."),
            ("resident_ttadak","누가 또 들어갔다가 갇히면 안 되잖아요. 판자는 반 치 길게 잘랐어요. 늘 그랬듯이."),
            ("resident_ttadak","네로 아저씨네 천막에도 판자를 다 댔어요. 그날 일당 받은 걸로요.")]),
        "ep5:st_nero_after":r13_st_topic("resident_nero","무엇을 그렇게 꿰매고 있어요?",(12,14),need=["nero_alive"],flags=["st_nero_after"],lines=[
            ("resident_nero","학교 아이들 이름표다. 표가 없는 애들 것까지."),
            ("resident_nero","그날 밤 다 못 데려왔지. 그래서 이름이라도 먼저 걸어 두는 거다. 다음엔 이름을 보고 찾아올 수 있게.")]),
        "ep5:st_teacher_after":r13_st_topic("resident_teacher","출석은 요즘 어떻게 불러요?",(13,14),need=["teacher_alive"],flags=["st_teacher_after"],lines=[
            ("resident_teacher","출석을 이제 아이들이 서로 불러요. 제가 부르면…… 제가 세는 숫자가 되더라고요.",{"pose":"write_attendance"}),
            ("resident_teacher","아이들이 서로 이름을 부르면, 한 명이 비어도 금방 알아요. 그게 맞는 거였어요.")]),
        "ep5:st_bori_after":r13_st_topic("resident_bori","도담이는 좀 어때요?",(13,14),need=["ws_kids_alive"],not_flags=["dodam_dead"],flags=["st_bori_after"],lines=[
            ("resident_bori","열 내렸어. 오늘 아침엔 감자 수프를 혼자 다 먹었다."),
            ("resident_bori","장작은 이제 몰래 안 가져가. 학교에서 같이 나눠 쓰기로 했거든.")]),
    })

    R13_EVENT_OFFERS.update({
        "r13_st_dodam":("학교 교실 구석에서 보리가 열 나는 아이 이마를 짚고 있다",[],""),
        "r13_st_kkomi_class":("학교 칠판 앞에서 꼬미가 분필을 쥐고 서 있다",[],""),
        "r13_st_pandol":("광장 이름 판 앞에서 늙은 비버가 판을 닦고 있다",[],""),
    })
    R13_OFFER_ACTORS.update({"r13_st_dodam":("resident_bori",None)})

label r13_st_events:
    $ _std,_stp,_stloc=room13["day"],room13["period"],room13["location"]
    if 3<=_std<=4 and _stp<=1 and _stloc=="school" and not r13_has("st_dodam_seen"):
        $ r13_offer("r13_st_dodam")
    if 6<=_std<=9 and _stp<=1 and _stloc=="school" and r13_has("wf_kkomi_saved") and not r13_has("st_kkomi_class_seen"):
        $ r13_offer("r13_st_kkomi_class")
    if _std==R13_WEEK2_DAY and _stp==2 and _stloc=="square" and not r13_has("st_pandol_seen"):
        $ r13_offer("r13_st_pandol")
    return

label r13_st_dodam:
    $ r13_flag("st_dodam_seen")
    call r13_scene("r13_school","학교 교실 · 열 나는 아이","quiet")
    call r13_lines([(None,"교실 구석 담요 위에 아주 작은 아기 곰이 누워 있었다. 벙어리장갑이 손보다 컸다.",{"show":"kid_dodam"}),
        ("resident_bori","열이 안 내려. 장작 한 짐을 더 날라야 약을 바꿔 준대."),
        ("kid_dodam","아빠, 나 안 아파. 노래 불러 줄까?"),
        ("kid_dodam","(작게) 휘휘 저어라 겨울 수프, 감자 하나 당근 하나……",{"expression":"joy"}),
        ("resident_bori","……그래. 다 나으면 진짜 수프 끓여 줄게. 감자 두 개 넣어서."),
        ("dad","(아이 하나를 위해서라면 저 큰 곰은 무엇이든 할 것 같았다.)",{"thought":True})],"st:dodam")
    return

label r13_st_kkomi_class:
    $ r13_flag("st_kkomi_class_seen")
    call r13_scene("r13_school","학교 교실 · 칠판 앞","quiet")
    call r13_lines([(None,"교실 칠판 앞에 꼬미가 서 있었다. 분필을 쥐고, 깜이·몽이·방울 앞에서.",{"show":"kid_kkomi","expression":"joy"}),
        ("kid_kkomi","이게 꼬, 이게 미. 대장 이름부터 외워."),
        ("kid_kkam","대장, 내 이름은?"),
        ("kid_kkomi","그건 선생님한테 배워. 나도 아직 거기까지밖에 몰라."),
        ("resident_teacher","꼬미가 반장을 하겠대요. 출석은 이제 꼬미가 불러요."),
        ("dad","(아지트 대장이 교실 대장이 되었다.)",{"thought":True})],"st:kkomi_class")
    return

label r13_st_pandol:
    $ r13_flag("st_pandol_seen")
    call r13_scene("winter_square","광장 · 이름 판 앞","quiet")
    call r13_lines([(None,"광장 이름 판 앞. 늙은 비버가 소매로 눈을 털어 내고 있었다. 앞니 하나가 빠져 있었다.",{"show":"npc_pandol"}),
        ("npc_pandol","할멈 이름이 여기 있소. 모과. 지난겨울에 보호소로 갔지."),
        ("npc_pandol","요즘 자꾸 잊어버려서. 아침에 뭘 먹었는지, 집에 가는 길이 어느 쪽인지."),
        ("npc_pandol","그래서 매일 와서 이름을 손가락으로 짚어 보오. 이것까지 잊으면, 할멈은 정말 없는 사람이 되니까.",{"pose":"point_name"}),
        ("npc_pandol","손목에 털실 감은 것도 할멈이 감아 준 거요. 풀리면 다시 감는 법은…… 그것도 가끔 잊소.")]+
        ([("daram","할아버지, 내가 내일도 같이 짚어 줄게."),("npc_pandol","……허허. 그럼 둘이 짚으면 안 잊겠구먼.")] if room13.get("daram_state") in ("with_dad","rescued") else []),"st:pandol", binding_route="dynamic:475")
    return
