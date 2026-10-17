# 공개 회의(7일째 식당 회의 · 14일째 제단 앞 회의).
# 주장 하나 = 상대의 발언 2~3개. 발언의 【강조된 말】을 맞는 자료로 깨고,
# 모두 깨면 결론을 말한다. 틀린 자료·틀린 결론에는 벌이 없다(기회는 많다).
# 실패는 두 가지뿐이다(스토리보드: 증거가 모자라면 다람이는 끌려간다).
#  - 깰 수 있는 발언이 하나도 없는 논점은 선택지 없이 넘어가고 반론하지 못한 것으로 남는다.
#  - 자료를 찾지 못하고 '반론을 그만둔다'를 고르면 그 회의에서 다시 다룰 수 없다.
# 0.18.35: 일부 발언만 깰 자료가 있어도 회의에 들어간다. 깬 발언은 남고(자리 기울기·기록),
#  남은 발언 때문에 결론은 못 낸다. '여기까지 정리한다'로 닫으면 partial로 남는다.
# 결과는 기존 r13_prove/propositions로만 남기므로 판결·엔딩 규칙은 그대로다.
init 98 python:
    from collections.abc import Mapping as R13DebateMapping
    R13_DEBATE={
        "C1":dict(title="잠긴 방에는 아이만 있었다",
            chair="resident_seori",
            statements=[
                dict(id="s1",who="seryeon",text="복도에 있던 사람들은 【아무도 문으로 들어가지 않았다】고 했습니다.",
                    truth=True,
                    press=[("seryeon","복도에 있던 다섯 명이 똑같은 말을 했어요. 그 사람들이 다 같이 거짓말을 했다는 겁니까?"),
                        ("dad","아니요. 그 다섯 명이 지켜본 게 13호의 어느 문이었는지 묻는 겁니다."),
                        ("seryeon","……복도 쪽 문이죠. 13호에 다른 문이 또 어디 있습니까?")],
                    reveals="s2",
                    hint="그 사람들 말은 맞다. 문제는 그 사람들이 본 것이 '복도 쪽 문' 하나뿐이라는 점이다.",
                    wrong=("seryeon","복도 사람들이 본 것까지 부정하시는 겁니까? 그 사람들 말은 틀리지 않았어요.")),
                dict(id="s2",who="seryeon",text="그 방으로 들어가는 길은 【복도 쪽 문 하나뿐】입니다.",
                    hidden=True,
                    accept=["E05","E37"],
                    soft={"E04":("resident_seori","도면에 그린 선만으로는 그 통로가 지금도 열리는지 알 수 없습니다. 직접 열어 보고 확인한 것이 있습니까?")},
                    hint="도면만으로는 부족하다. 내가 직접 열어 본 길이 있다.",
                    broken=[("dad","주방 레버를 올리고 13호 책장 아래 책을 당기면, 책장 뒤 문이 열립니다. 제가 직접 열어 봤습니다."),
                        ("seryeon","……그 문이 세탁실로 이어진다고요?",{"expression":"surprise"})],
                    wrong=("seryeon","그 자료가 13호에 다른 길이 있다는 증거입니까?")),
            ],
            conclusion=dict(prompt="다른 길이 있다는 걸 어떻게 정리할까?",
                options=[
                    ("correct","'아이만 들어갔다'는 말은 틀렸다"),
                    ("over","길을 아는 할머니가 범인이다"),
                    ("weak","엄마가 그 길로 왔을지도 모른다"),
                ],
                correct=[("resident_seori","13호에는 정문 말고도 들어갈 길이 있었습니다. ‘아이만 들어갈 수 있었다’는 말은 고치십시오."),
                    ("seryeon","그 통로 안에 그 아이 엄마의 물건이 있었다면서요."),
                    ("dad","통로에 남은 오래된 흔적만으로는 그날 누가 지나갔는지까지 알 수 없습니다."),
                    ("resident_seori","그날 누가 그 통로를 썼는지는 따로 따지겠습니다.")],
                over=("resident_seori","통로가 있다는 것과 누가 그 통로를 썼는지는 다른 문제입니다. 아직 그 사람이 누구라고 말할 수는 없습니다."),
                weak=("seryeon","그럼 아버님의 부인을 의심하자는 겁니까? 통로에서 나온 오래된 물건 하나만 가지고요?")),
            sway=["resident_tori","doto"]),

        "C2":dict(title="아이가 친 촛대 때문에 죽었다",
            chair="resident_seori",
            statements=[
                dict(id="s1",who="resident_ppul",text="아이가 촛대로 【어르신의 머리를 내리쳤다】고 했습니다.",
                    accept=["E06","E08"],
                    hint="다람이가 친 곳은 머리가 아니었다. 다람이를 만났을 때 들은 말과 처음 상처를 본 기록이 있다.",
                    broken=[("dad","다람이가 친 건 자기 팔을 붙잡은 손입니다. 처음 상처를 살핀 기록에도 팔의 상처와 머리의 상처가 따로 적혀 있습니다."),
                        ("resident_ppul","팔이든 머리든, 아이가 친 건 사실 아닙니까?")],
                    # 0.18.35: one record, one claim. E06 is the child's own account; E08 only shows two wounds.
                    broken_by={
                        "E06":[("dad","다람이는 할아버지가 붙잡은 자기 팔을 빼려고 촛대로 그 손을 쳤다고 했습니다. 머리를 쳤다고 한 적은 없습니다."),
                            ("resident_ppul","아이 말만 믿으라는 겁니까? 그래도 아이가 친 건 사실 아닙니까?",{"expression":"flustered"})],
                        "E08":[("dad","처음 상처를 살핀 기록입니다. 어르신 팔의 상처와 머리의 상처가 따로 적혀 있습니다. 머리를 한 번 내리쳤다면 팔의 상처는 어디서 생겼습니까?"),
                            ("resident_ppul","……팔이든 머리든, 아이가 친 건 사실 아닙니까?",{"expression":"flustered"})]},
                    wrong=("resident_ppul","그 자료로 아이가 머리를 치지 않았다고 할 수 있습니까?")),
                dict(id="s2",who="resident_ppul",text="촛대는 【한 번 휘둘렸을 뿐】입니다. 그 한 번에 돌아가셨어요.",
                    accept=["E35"],
                    # 0.18.35: the broken candlestick alone cannot order the blows (E07 says so).
                    soft={"E07":("resident_seori","촛대가 둘로 갈라진 건 보입니다. 하지만 조각만 봐서는 언제 갈라졌는지, 머리 상처를 그 조각이 냈는지 알 수 없습니다. 상처와 맞춰 본 기록이 있습니까?")},
                    hint="촛대가 두 동강 난 것만으로는 모자란다. 깨진 면과 머리 상처를 실제로 맞춰 본 기록이 있어야 한다.",
                    broken=[("dad","검사원님과 깨진 면을 상처에 맞춰 본 기록입니다. 머리의 상처는 갈라진 윗부분의 안쪽 날과 모양이 맞습니다."),
                        ("dad","그 안쪽 날은 촛대가 붙어 있을 때는 드러나지 않습니다. 촛대가 부러진 다음에, 누군가 그 윗부분 조각을 다시 들었다는 뜻입니다.")],
                    wrong=("resident_ppul","상처 모양만으로 촛대가 두 번 쓰였다는 걸 어떻게 압니까?")),
                dict(id="s3",who="resident_ppul",text="그 방에는 【아이 혼자】 있었습니다. 다시 휘두를 사람이 누가 있습니까?",
                    accept=["E10","E09"],
                    need_consent={"E10":"bami_consent"},
                    hint="촛대가 부러진 뒤 다람이는 침대 밑에 숨어 있었다. 통로 쪽에서 다가온 발자국도 있었다.",
                    broken=[("dad","촛대가 갈라진 직후 아이는 침대 밑으로 숨었고, 구하러 들어갈 때까지 나오지 않았습니다. 그사이 통로 쪽에서 다가온 발자국이 남아 있습니다."),
                        ("buri","……그럼 할아버지를 친 사람이 따로 있다는 거예요?",{"expression":"surprise"})],
                    # 0.18.41 (owner review): the passage Dad proved in C1 comes back at him.
                    counter=dict(need_prop="C1",
                        lines=[("resident_ppul","잠깐만요. 아까 13호에 다른 길이 있다고 하셨지요."),
                            ("resident_ppul","그럼 그 통로로 아이가 직접 나갔다가 들어왔을 수도 있잖습니까?",{"expression":"angry"})],
                        prompt="통로가 있다는 내 말이 다람이에게 돌아왔다. 어떻게 답할까?",
                        options=[("correct","통로는 주방 레버로만 열린다"),
                            ("over","그 통로는 할머니만 썼다"),
                            ("weak","겁 많은 아이는 그 길로 못 간다")],
                        correct=[("dad","책장 뒤 문은 주방에서 레버를 올려야 열립니다. 아까 이 자리에서 확인한 대로입니다."),
                            ("dad","방 안에 갇힌 아이 혼자서는 열 수 없습니다. 그 문이 열렸다면, 그때 주방에 누군가 있었다는 뜻입니다."),
                            ("resident_ppul","……주방에 누군가요.",{"expression":"flustered"})],
                        wrong=dict(over=("resident_seori","그 길을 누가 썼는지는 아직 아무도 밝히지 못했습니다. 지금 물은 건 아이가 그 길을 쓸 수 있었느냐입니다."),
                            weak=("resident_ppul","겁 많은 아이가 촛대는 휘둘렀다면서요?",{"expression":"angry"}))),
                    broken_by={
                        "E10":[("dad","밤이가 본 것입니다. 촛대가 바닥에서 갈라진 직후 아이는 침대 밑으로 숨었고, 구하러 들어갈 때까지 나오지 않았습니다."),
                            ("buri","……그럼 침대 밑에 있던 애가 어떻게 할아버지를 다시 쳐요?",{"expression":"surprise"})],
                        "E09":[("dad","촛대가 떨어진 뒤에 통로 쪽에서 다가온 발자국이 있습니다. 그 위로 피가 번졌습니다. 촛대가 떨어진 다음에 그 자리로 온 사람이 있었다는 뜻입니다."),
                            ("buri","……그럼 할아버지를 친 사람이 따로 있다는 거예요?",{"expression":"surprise"})]},
                    wrong=("resident_ppul","그 자료가 방 안에 다른 사람이 있었다는 증거입니까?")),
            ],
            conclusion=dict(prompt="촛대와 상처의 순서로 무엇을 말할까?",
                options=[
                    ("correct","머리 상처는 다른 누군가가 냈다"),
                    ("over","통로를 아는 할머니가 죽였다"),
                    ("weak","겁먹은 아이에게는 책임이 없다"),
                ],
                correct=[("resident_seori","아이가 한 일과 어르신을 죽게 한 일을 같은 일로 적을 수는 없습니다."),
                    ("daram","그럼…… 내가 할아버지를 때린 건 어떻게 돼?",{"expression":"anxious"}),
                    ("dad","네가 때린 건 붙잡은 손을 놓게 하려고 한 일이야. 할아버지를 죽게 한 일과는 달라.")],
                over=("resident_seori","확인된 건 누군가 촛대를 다시 들었다는 것까지입니다. 그 사람이 누구인지는 아직 아무도 밝히지 못했습니다."),
                weak=("buri","할아버지도 그때 겁에 질려 있었어요. 그런 말로만 끝내지 마세요.",{"expression":"angry"})),
            sway=["buri","resident_bori","nabi"]),

        "C3":dict(title="할머니는 그때 식당에 있었다",
            chair="resident_seori",
            statements=[
                dict(id="s1",who="granny",text="비명이 들릴 때 나는 【식당에】 있었어요. 다들 봤잖아요.",
                    truth=True,
                    press=[("granny","그때 나비가 내 바로 옆에 있었어요. 직접 물어봐요."),("nabi","네. 첫 비명이 났을 때는 할머니랑 같이 있었어요.")],
                    hint="이 말은 사실이다. 따질 것은 '첫 비명 다음'이다.",
                    wrong=("nabi","제가 할머니랑 같이 있던 것까지 없던 일로 만들지는 마세요.",{"expression":"angry"})),
                dict(id="s2",who="granny",text="그 뒤로도 나는 【계속 사람들 곁에】 있었어요.",
                    accept=["E12"],
                    soft={"E11":("resident_seori","복도 사람들이 지켜본 건 13호 앞문뿐입니다. 그사이 할머니가 어디 있었는지는 그 말만으로 알 수 없습니다.")},
                    hint="공구를 가지러 주방에 간 뒤로는 아무도 할머니를 보지 못했다. 그걸 직접 말할 수 있는 사람은 나비다.",
                    broken=[("nabi","할머니가 공구를 가지러 주방에 가신 뒤로는…… 저도 못 봤어요.",{"expression":"anxious"}),
                        ("granny","내가 잠깐 안 보였다는 게 전부잖아요.",{"expression":"flustered"})],
                    wrong=("granny","그 자료가 내가 혼자 있었다는 증거예요?")),
                dict(id="s3",who="granny",text="주방에서 그 방까지는 【한참 걸려요】. 그 잠깐에 다녀올 수는 없어요.",
                    accept=["E05","E37"],
                    hint="주방과 13호 책장은 통로로 바로 이어져 있다.",
                    broken=[("dad","주방에서 레버를 올리면 13호 책장 뒤로 곧장 이어집니다. 복도로 돌아갈 필요가 없습니다."),
                        ("granny","……그 통로는 세탁물을 나르던 길이에요.",{"expression":"flustered"})],
                    wrong=("granny","그 자료가 주방에서 13호까지 가깝다는 증거예요?")),
            ],
            conclusion=dict(prompt="할머니의 그날 움직임을 어떻게 정리할까?",
                options=[
                    ("correct","주방에 간 뒤로는 아무도 못 봤다"),
                    ("over","그때 할머니가 13호실에서 죽였다"),
                    ("weak","나비는 할머니 편이라 못 믿는다"),
                ],
                correct=[("resident_seori","첫 비명 때 식당에 있었다는 건 사실입니다. 하지만 그것이 그 뒤의 시간까지 설명해 주지는 않습니다."),
                    ("resident_seori","할머니가 13호에 실제로 들어갔는지는 이어서 보겠습니다.")],
                over=("resident_seori","13호에 갈 수 있었다는 것과 실제로 갔다는 것은 다릅니다. 실제로 갔다는 증거는 아직 보여 주지 않으셨습니다."),
                weak=("nabi","저는 본 것만 말했어요. 누구 편을 든 게 아니에요.",{"expression":"angry"})),
            sway=["nabi","resident_kongi"]),

        "C4":dict(title="들어갔다 해도 도우려 했을 뿐이다",
            chair="resident_seori",
            statements=[
                dict(id="s0",who="granny",text="그런 핀은 마을에 흔해요. 【내 것이라는 증거】가 있어요?",
                    accept=["E13"],
                    soft={"E14":("resident_seori","촛대에 핀이 끼어 있었던 건 확인했습니다. 남은 건 그 핀이 누구 것인지입니다.")},
                    hint="그 핀의 덧댄 이음은 톡이 그날 처음 만든 하나뿐인 것이다. 만든 사람이 직접 말해야 한다.",
                    broken=[("resident_tok","이 핀 이음은 내가 목요일에 덧댄 거예요. 맞는 부품이 없어서요. 그래서 이렇게 생긴 핀은 마을에 이것 하나뿐이에요."),
                        ("resident_tok","그날 그 핀을 달고 간 사람은 할머니고요. 누가 그 핀으로 뭘 했는지는 나도 몰라요."),
                        ("granny","……….",{"expression":"anxious"})],
                    wrong=("granny","그 자료가 내 핀이라는 증거예요?")),
                dict(id="s1",who="granny",text="그 핀은 【오후에 그분을 도울 때】 떨어졌을 수도 있잖아요.",
                    accept=["E15"],
                    soft={"E13":("resident_seori","그날 새 핀으로 바꿨다는 건 알겠습니다. 그 핀이 언제까지 할머니 옷에 달려 있었는지가 궁금합니다.")},
                    hint="첫 비명 직후, 나비가 그 핀을 할머니 목도리에 직접 여며 주었다.",
                    # 0.18.41: Nabi's testimony is turned on Nabi.
                    counter=dict(
                        lines=[("granny","그래요. 첫 비명 뒤에도 핀이 내 목도리에 있었다 쳐요."),
                            ("granny","그럼 그 핀을 마지막으로 만진 건 나비네요. 나비가 떨어뜨렸을 수도 있잖아요?",{"expression":"angry"}),
                            ("nabi","네……?",{"expression":"surprise"})],
                        prompt="나비의 증언이 나비에게 돌아왔다. 어떻게 답할까?",
                        options=[("correct","핀은 식당을 나설 때도 달려 있었다"),
                            ("over","나비가 할머니 지시로 말을 바꿨다"),
                            ("weak","흔한 핀이라 누구 것인지 모른다")],
                        correct=[("dad","나비가 핀을 여며 드린 건 첫 비명 때, 식당에서였습니다."),
                            ("dad","그 뒤 공구를 가지러 식당을 나간 건 할머니입니다. 핀도 목도리에 달린 채 함께 나갔습니다."),
                            ("granny","……….",{"expression":"anxious"})],
                        wrong=dict(over=("resident_seori","나비가 거짓말을 한다는 근거는 없습니다. 근거 없이 증인을 몰아세우지 마십시오."),
                            weak=("granny","방금 그 핀은 마을에 하나뿐이라고 하셨잖아요. 말을 바꾸시네요.",{"expression":"angry"}))),
                    broken=[("nabi","첫 비명 바로 뒤에 제가 할머니 핀을 여며 드렸어요. 그때는 핀이 목도리에 달려 있었어요."),
                        ("granny","……그래서 어쨌다는 거예요?",{"expression":"angry"})],
                    wrong=("granny","그 자료가, 핀이 오후에 떨어진 게 아니라는 증거예요?")),
                dict(id="s2",who="granny",text="구하려고 들어갔다가 【촛대를 주웠을 뿐】이에요.",
                    accept=["E35"],
                    soft={"E33":("resident_seori","아이를 구한 직후에 누가 촛대를 거뒀는지는 확인됩니다. 문제는 그 전에 무슨 일이 있었느냐입니다."),
                        # 0.18.35: E14 itself says when the ring was crushed must be matched separately.
                        "E14":("granny","핀이 고리에 끼어 있었다고요? 주워 들다가 끼었을 수도 있잖아요. 그 고리가 언제 찌그러졌는지는 아세요?",{"expression":"angry"})},
                    hint="핀이 끼어 있었다는 것만으로는 모자란다. 고리가 어느 쪽으로 눌렸는지 맞춰 본 기록이 있어야 한다.",
                    broken=[("dad","촛대를 상처와 맞춰 볼 때 함께 적은 기록입니다. 장식 고리는 내려친 방향으로 찌그러졌고, 고리 안에 낀 핀도 같은 쪽으로 휘었습니다."),
                        ("dad","톡 씨 말대로 그 틈은 나중에 핀만 밀어 넣을 수 있는 틈이 아닙니다. 주워 들다가 끼인 게 아니라, 내려친 순간에 고리에 박혀 들어간 겁니다.")],
                    wrong=("granny","핀 하나로 내가 촛대를 휘둘렀다는 거예요?")),
                dict(id="s3",who="granny",text="그분이 그렇게 위험한 줄은 【몰랐어요】.",
                    accept=["E36"],
                    hint="전날 저녁, 할머니가 직접 쓴 진료 요청이 있다.",
                    broken=[("resident_seori","전날 저녁 할머니가 직접 적어 보낸 쪽지입니다. 발작이 심하다는 내용이었고, 저는 ‘혼자 두지 마라’고 답했습니다."),
                        ("granny","……….",{"expression":"anxious"})],
                    wrong=("granny","그 자료가 내가 위험을 알고 있었다는 증거예요?")),
            ],
            conclusion=dict(prompt="핀과 촛대로 무엇을 말할까?",
                options=[
                    ("correct","핀이 내려친 쪽 고리에 끼어 있었다"),
                    ("over","할머니가 처음부터 우리를 노렸다"),
                    ("weak","방에 들어간 적이 있다는 것까지다"),
                ],
                correct=[("resident_seori","위험을 알면서 둘만 남겼고, 촛대에 할머니의 핀이 내려친 방향으로 끼어 있습니다. 구하려다 생긴 흔적이라는 말은 받아들일 수 없습니다."),
                    ("resident_seori","대답하지 않으셔도, 제출된 자료로 판단하겠습니다.")],
                over=("resident_seori","오늘은 그날 그 방에서 있었던 일만 따집니다. 가족을 부른 이유는 따로 밝혀 주셔야 합니다."),
                weak=("dad","(아니다. 여기서 멈추면 ‘도우려 했다’는 할머니의 말이 그대로 남는다.)")),
            sway=["buri","resident_bori","resident_kongi"]),

        "F1":dict(title="저 사람들은 돌아올 수 없다",
            chair="resident_seori",
            statements=[
                dict(id="s1",who="resident_ppul",text="가족도 못 알아봅니다. 【돌아올 수 없는 분들】로 판단됐어요.",
                    accept=["E20"],
                    hint="처음 증상이 나타난 뒤 나아진 사람이 있었다.",
                    broken=[("dad","증상이 시작된 뒤에도 다시 이름을 말하고 가족을 알아본 사람이 있습니다. 그 관찰을 적어 둔 기록이 있습니다."),
                        ("resident_ppul","그건 한 사람이 잠깐 좋아졌을 뿐이겠죠.",{"expression":"flustered"})],
                    wrong=("resident_ppul","그 자료가 저 환자들이 돌아올 수 있다는 증거입니까?")),
                dict(id="s2",who="resident_ppul",text="나아졌다는 기록은 【처음부터 없었습니다】.",
                    accept=["E31"],
                    hint="누군가 지우기 전에 베껴 둔 기록이 남아 있다.",
                    broken=[("dad","지우기 전에 베껴 둔 기록입니다. 나아진 사람을 ‘되돌릴 수 없음’으로 고쳐 적은 건 할머니입니다."),
                        ("resident_ppul","……누가 그 기록을 지웠다는 겁니까?",{"expression":"surprise"})],
                    wrong=("resident_ppul","그 기록이 원래 있었다는 걸 어떻게 압니까?")),
            ],
            conclusion=dict(prompt="회복 기록이 뜻하는 것은?",
                options=[
                    ("correct","아무도 못 돌아온다는 판단은 틀렸다"),
                    ("over","모두 나으니 당장 전부 풀어 준다"),
                    ("weak","다시 나빠졌으니 나은 기록은 뺀다"),
                ],
                correct=[("resident_seori","잠깐이라도 나아졌던 일을 지워서는 안 됐습니다."),
                    (None,"보리가 환자를 누르던 손을 풀었다. 그리고 담요를 덮어 주었다. 장치는 아직 멈추지 않았다.")],
                over=("nabi","환자를 풀어 줬다가 다치면요? 돌아올 수 있다는 것과 지금 괜찮다는 건 달라요.",{"expression":"anxious"}),
                weak=("resident_seori","다시 나빠진 것도 적어야 합니다. 하지만 그 전의 회복을 지우면 ‘돌아온 적 없다’는 거짓말이 됩니다.")),
            sway=["resident_bori","nabi"]),

        "F2":dict(title="희생 말고는 불을 살릴 방법이 없다",
            chair="resident_seori",
            statements=[
                dict(id="s1",who="resident_ppul",text="지난번 희생 뒤에 【불이 돌아왔습니다】. 다들 봤잖아요.",
                    truth=True,
                    press=[("resident_ppul","불은 돌아왔습니다. 그날 밤 우리 집도 따뜻했습니다."),("mom","그날 출력이 올라간 건 사실이에요. 문제는 그다음에 어떻게 됐는지예요.")],
                    reveals="s2",
                    hint="불이 돌아온 건 사실이다. 그 뒤가 어땠는지 봐야 한다.",
                    wrong=("resident_ppul","그날 밤 불이 돌아온 것까지 거짓말이라는 겁니까?")),
                dict(id="s2",who="resident_ppul",text="그러니 【계속 그렇게 하면】 버틸 수 있습니다.",
                    hidden=True,
                    accept=["E21","E22"],
                    hint="희생할 때마다 버틴 날이 줄었다. 오래된 운전 기록에도 그렇게 적혀 있다.",
                    broken=[("buri","희생이 있을 때마다 버틴 날수가 줄었어요. 어르신이 남긴 운전 기록에도 그렇게 적혀 있어요."),
                        ("resident_ppul","그래도 지금은 희생 말고 방법이 없잖소!",{"expression":"angry"})],
                    broken_by={
                        "E21":[("buri","할아버지가 남긴 운전 기록이에요. 사람한테서 힘을 뽑으면 잠깐 올랐다가 다시 떨어졌어요. 그게 되풀이될수록 남은 힘이 줄었고요."),
                            ("resident_ppul","그래도 지금은 희생 말고 방법이 없잖소!",{"expression":"angry"})],
                        "E22":[("mom","시설의 원래 기록이에요. ‘희생’은 사람이 죽는다는 뜻이고, 힘은 잠깐만 오른다고 적혀 있어요. 잠깐 오르는 걸 계속 버틴다고 할 수는 없어요."),
                            ("resident_ppul","잠깐이라도 오르면 그만큼은 버티는 거잖소!",{"expression":"angry"})]},
                    wrong=("resident_ppul","그 자료가 다음엔 희생이 통하지 않는다는 증거입니까?")),
                dict(id="s3",who="resident_ppul",text="사람을 바치는 것 말고는 【다른 방법이 없습니다】.",
                    accept=["E23"],
                    soft={"E30":("resident_seori","옛 글을 읽어 낸 건 알겠습니다. 그 방법을 실제로 해 본 기록이 있습니까?")},
                    hint="남은 힘을 한곳으로 옮겨 본 기록이 두 번 있다.",
                    broken=[("mom","여러 돌에 남은 힘을 한곳으로 모았어요. 작은 집에서 한 번, 저녁에 더 큰 곳에서 한 번 해 봤고요."),
                        ("resident_seori","새로 채우는 방법은 아니지만, 사람을 잇지 않고도 버틸 방법은 있습니다.")],
                    broken_by={
                        "E23":[("mom","여러 돌에 남은 힘을 한 돌로 옮겨 봤어요. 내준 돌은 줄고 받은 돌은 고르게 빛났어요. 힘을 조금 쓸 때 한 번 본 거지만, 사람을 잇지 않고 옮길 수는 있었어요."),
                            ("resident_seori","새로 채우는 방법은 아니군요. 그래도 사람을 잇지 않는 길이 하나는 있습니다.")]},
                    wrong=("resident_ppul","그 자료가 희생 말고 다른 방법이 있다는 증거입니까?")),
                dict(id="s4",who="resident_ppul",text="작은 곳에서 한 번 본 것뿐이잖소. 【저녁에도 버틸지는 확인하지 못했습니다】.",
                    accept=["E24"],require_observations=True,
                    press=[("dad","낮에 해 본 것만으로는 부족하다는 말씀이군요."),("resident_seori","맞습니다. 힘을 더 많이 쓰는 저녁에 얼마나 버텼는지도 확인해야 합니다.")],
                    blocked=[("resident_seori","낮과 저녁에 직접 확인한 두 기록을 함께 대조해야 합니다. 기록지만으로 실험을 대신할 수는 없습니다.")],
                    soft={"E23":("resident_seori","이건 힘을 적게 쓸 때의 첫 관찰입니다. 지금 따지는 건 저녁의 부하입니다.")},
                    hint="힘을 많이 쓰는 저녁에 실제로 다시 지켜본 기록이 필요하다.",
                    broken=[("mom","저녁에 남은 힘을 다시 재고 옮겼어요. 힘을 더 많이 쓸 때 버틴 시간과 새어 나간 양도 적었습니다."),("resident_seori","낮과 저녁에 따로 확인했군요. 공급할 곳을 줄여야 하고, 새 힘이 생긴 건 아니라는 한계도 그대로 남습니다.")],
                    wrong=("resident_ppul","그 자료에 저녁에도 해 봤다는 내용이 있습니까?")),
            ],
            conclusion=dict(prompt="추출 기록과 낮·저녁의 관찰을 이으면?",
                options=[
                    ("correct","반짝 효과는 짧고, 모으면 버틴다"),
                    ("over","힘을 모으면 장치를 영원히 채운다"),
                    ("weak","희생 직후 불이 올랐으니 쓸 만하다"),
                ],
                correct=[("resident_ppul","돌에 남은 힘도 결국 다 쓰잖소!",{"expression":"angry"}),
                    ("mom","맞아요. 그래서 필요한 곳에 모여 지내면서, 그동안 장작과 식량을 마련해야 해요. 다음 사람을 바칠 날만 기다리는 대신에요."),
                    (None,"작업자가 손을 멈췄다. 환자 쪽 관이 내려왔다. 대피소를 맡은 사람들이 얼마나 버틸 수 있을지 시간을 세기 시작했다.")],
                over=("mom","아니에요. 힘을 모아도 언젠가는 다 써요. 그러니 그동안 다른 준비를 해야 해요."),
                weak=("mom","그 뒤로 더 떨어진 걸 보세요. 한 번 오른 것과 계속 버틸 수 있다는 건 달라요.")),
            sway=["resident_bori","buri","nabi"]),

        "F3":dict(title="오늘 밤 희생 없이 살 방법이 없다",
            chair="resident_seori",
            statements=[
                dict(id="s1",who="resident_ppul",text="불을 끄면 오늘 밤 【잘 곳이 없습니다】.",
                    accept=["E25"],required_flags=["shelter_ready"],
                    blocked=[("resident_seori","학교를 대피소로 실제 넘겨받았는지 확인되지 않았습니다. 기록이 있다는 것과 지금 쓸 수 있다는 건 다릅니다.")],
                    hint="학교를 대피소로 쓰기로 넘겨받았다.",
                    broken=[("dad","대피소로 쓸 학교를 넘겨받았습니다. 몇 명이 들어갈 수 있는지도 적어 뒀습니다.")],
                    wrong=("resident_ppul","그게 오늘 밤 사람들이 잘 곳입니까?")),
                dict(id="s2",who="nabi",text="방만 있으면 뭐해요. 【먹을 것과 장작】은요?",
                    accept=["E26"],required_flags=["supplies_ready"],
                    blocked=[("nabi","장작과 곡식을 실제로 학교에 옮겨 둔 게 아니면, 오늘 밤 쓸 수 있다고 할 수는 없어요.")],
                    hint="학교로 옮긴 장작과 곡식의 양을 적어 두었다.",
                    broken=[("nabi","……학교로 옮긴 양이 이만큼이면 오늘 밤은 버틸 수 있어요.")],
                    wrong=("nabi","없는 걸 있다고 할 수는 없잖아요.")),
                dict(id="s3",who="resident_ppul",text="밤새 장치를 손으로 돌리고 환자를 옮길 【사람이 없습니다】.",
                    ready_flags=["operators_ready","patient_transport"],
                    press=[("buri","장치 이쪽은 내가 잡을게요. 다음 교대할 사람도 정했어요."),("resident_bori","환자는 우리가 수레로 학교까지 옮겨요.")],
                    press_missing=[("nabi","환자를 옮길 사람, 밤에 남을 사람부터 정해요. 우리 손에 실제로 있는 것부터 세어 봐요.")],
                    hint="교대할 사람과 환자를 옮길 사람을 실제로 구해 두었는지가 전부다. 되물으면 확인된다.",
                    wrong=("resident_ppul","사람은 종이로 대신할 수 없습니다.")),
            ],
            conclusion=dict(prompt="오늘 밤을 버틸 방법은?",
                options=[
                    ("correct","학교에 모여 식량을 나누고 교대한다"),
                    ("over","장치를 멈추고 각자 집에서 버틴다"),
                    ("weak","집마다 똑같이 나누고 불을 지킨다"),
                ],
                correct=[("nabi","학교로 솥을 옮겼어요. 들어오실 분부터 들어오세요."),
                    ("resident_bori","장작을 집집마다 나누면 모자라요. 그러니 한곳에 모여 있어야 해요."),
                    ("buri","장치 이쪽은 내가 잡을게요.")],
                over=("resident_ppul","장치를 바로 멈추면 대피소로 옮기기도 전에 얼어 죽습니다.",{"expression":"anxious"}),
                weak=("resident_bori","집집마다 불을 살리면 장작이 모자라요. 빈 방까지 데울 몫은 없다고요.")),
            sway=["resident_bori","nabi"]),

        "F4":dict(title="그 가족이 마을의 질서를 깨뜨렸다",
            chair="resident_seori",
            statements=[
                dict(id="s1",who="granny",text="아내분은 【가족에게 연락하려 하지도 않았어요】. 내가 찾게 해 준 거예요.",
                    accept=["E18"],
                    soft={"E17":("resident_seori","어르신이 아내분을 만난 건 확인됩니다. 하지만 가족에게 언제 경고했는지까지 이 기록으로 알 수는 없습니다."),"E01":("granny","그래요, 그 편지는 내가 부쳤어요. 그게 어때서요?",{"expression":"angry"})},
                    hint="아내는 첫 주에 이미 가족에게 경고를 보냈다. 이미 도망친 뒤였다.",
                    broken=[("dad","아내는 첫 주에 이미 저희에게 오지 말라고 경고했습니다. 그 경고가 전해지지 않았을 뿐입니다. 당신에게서 도망친 뒤의 일이었습니다."),
                        ("mom","여관으로 돌아갈 수는 없었어요. 그동안 가족에게 돌아갈 방법을 찾고 있었거든요.")],
                    broken_by={
                        "E18":[("dad","전해지지 못한 봉투입니다. 아내는 첫 주에 이미 저희에게 오지 말라고 경고했습니다. 누가 나서서 아내를 찾아 주기 전부터, 아내는 스스로 저희에게 연락하고 있었습니다."),
                            ("mom","여관으로 돌아갈 수는 없었어요. 그동안 가족에게 돌아갈 방법을 찾고 있었거든요.")],
                        "E17":[("dad","부엉이 어르신이 베껴 둔 기록입니다. 어르신은 아내를 만났고, 사라진 사람들을 따로 조사하고 있었습니다. 아내를 찾게 해 준 건 할머니가 아닙니다."),
                            ("mom","그분이 제 이야기를 들어 주셨어요. 여관으로는 돌아갈 수 없었고요.")]},
                    wrong=("granny","그 자료가 내가 거짓말했다는 증거예요?")),
                dict(id="s2",who="granny",text="아이를 떼어 놓자고 한 건 【사건이 난 뒤의 보호】였어요.",
                    accept=["E16"],
                    skip_if="C4",
                    hint="가족을 떼어 놓자는 요청은 사건 전에 이미 쓰여 있었다.",
                    broken=[("resident_seori","이 요청을 보낸 날짜는 사건 전입니다. 아이를 보호하려 했다는 말과, 요청을 쓴 날이 맞지 않습니다."),
                        ("granny","그 여자가 돌아왔으면 아이는 다치지 않아도 됐어.",{"expression":"angry"})],
                    wrong=("granny","그 자료가 사건 전에 썼다는 증거예요?")),
            ],
            conclusion=dict(prompt="편지와 경고, 떼어 놓자는 요청을 이으면?",
                options=[
                    ("correct","엄마를 붙잡으려 아이를 떼어 놓았다"),
                    ("over","할머니 혼자 모든 희생을 꾸몄다"),
                    ("weak","할머니가 편지를 부친 건 사실이다"),
                ],
                correct=[("dad","아내가 돌아오기를 거절하자, 아내 이름으로 이 편지를 써서 보내셨습니다. 가족을 떼어 놓는 요청도 미리 써 두셨고요."),
                    ("dad","대답하지 않으셔도 오늘 기록은 남습니다."),
                    ("neoul","이후 지시는 받지 않겠습니다. 먼저 증거 자료부터 챙기죠.")],
                over=("resident_ppul","희생을 정한 건 마을 회의였습니다. 그 책임까지 한 사람에게 미룰 수는 없어요."),
                weak=("granny","편지 보낸 게 무슨 죄예요?",{"expression":"angry"})),
            sway=["resident_ppul","neoul"]),
    }

    # 회의 자리. 'doubt'에서 시작해 반박할 때마다 한 칸씩 돌아선다.
    R13_DEBATE_SEATS={
        "trial":["seryeon","resident_ppul","buri","nabi","resident_bori","resident_tori","doto","resident_kongi"],
        "finale":["resident_ppul","resident_bori","nabi","buri","neoul","resident_tori"],
    }
    R13_DEBATE_STANCE={"trial":("아이를 의심","모르겠다","아이를 믿는다"),"finale":("희생을 이어 간다","모르겠다","희생을 멈춘다")}

    def r13_debate_session(claim):
        s=store.room13 or {}
        return "finale" if (claim.startswith("F") or s.get("finale_started")) else "trial"

    def r13_debate_state():
        d=(store.room13 or {}).get("debate")
        if not isinstance(d,dict):
            d=dict(broken={},pressed={},misses={},closed={})
        for k in ("broken","pressed","misses","closed"):
            d.setdefault(k,{})
        return d

    def r13_debate_save(d):
        n=winter_copy.deepcopy(store.room13);n["debate"]=d;store.room13=n

    def r13_debate_statements(claim):
        return R13_DEBATE[claim]["statements"]

    def r13_debate_statement(claim,sid):
        return next(st for st in r13_debate_statements(claim) if st["id"]==sid)

    def r13_debate_skipped(claim,st):
        return bool(st.get("skip_if")) and st["skip_if"] in (store.room13 or {}).get("propositions",[])

    def r13_debate_observations_ready():
        obs=(store.room13 or {}).get("observations",{})
        if not isinstance(obs,R13DebateMapping):return False
        first=obs.get("first",{});second=obs.get("second",{})
        if not isinstance(first,R13DebateMapping) or not isinstance(second,R13DebateMapping):return False
        a=first.get("time");b=second.get("time")
        return (isinstance(a,(int,float)) and isinstance(b,(int,float)) and a<b
            and first.get("load")=="day_low" and second.get("load")=="evening_high"
            and all(row.get("operator")=="buri" and row.get("recorder")=="resident_seori" for row in (first,second)))

    def r13_debate_context_ready(st):
        return (all(r13_has(flag) for flag in st.get("required_flags",[]))
            and (not st.get("require_observations") or r13_debate_observations_ready()))

    def r13_debate_is_broken(claim,sid):
        st=r13_debate_statement(claim,sid)
        if r13_debate_skipped(claim,st):return True
        if not r13_debate_context_ready(st):return False
        if st.get("ready_flags") and all(r13_has(f) for f in st["ready_flags"]) and sid in r13_debate_state()["pressed"].get(claim,[]):
            return True
        return sid in r13_debate_state()["broken"].get(claim,[])

    def r13_debate_is_pressed(claim,sid):
        return sid in r13_debate_state()["pressed"].get(claim,[])

    def r13_debate_visible(claim,st):
        if not st.get("hidden"):return True
        return any(o.get("reveals")==st["id"] and r13_debate_is_pressed(claim,o["id"]) for o in r13_debate_statements(claim))

    def r13_debate_required(claim):
        return [st["id"] for st in r13_debate_statements(claim) if not st.get("truth")]

    def r13_debate_ready(claim):
        return all(r13_debate_is_broken(claim,sid) for sid in r13_debate_required(claim))

    def r13_debate_progress(claim):
        req=r13_debate_required(claim)
        return sum(1 for sid in req if r13_debate_is_broken(claim,sid)),len(req)

    def r13_debate_mark(kind,claim,sid):
        d=r13_debate_state();row=d[kind].setdefault(claim,[])
        if sid not in row:row.append(sid)
        r13_debate_save(d)

    def r13_debate_judge(claim,sid,key):
        """Returns (result, lines). result: break | soft | wrong."""
        st=r13_debate_statement(claim,sid)
        if r13_debate_is_broken(claim,sid):
            return "soft",[(R13_DEBATE[claim]["chair"],"그 말은 이미 반박됐습니다. 남은 말을 보세요.")]
        if st.get("ready_flags"):
            return "soft",list(st.get("press_missing",[(R13_DEBATE[claim]["chair"],"자료와 함께 실제로 준비된 사람과 길도 확인해야 합니다." )]))
        consent=st.get("need_consent",{}).get(key)
        if consent and not r13_has(consent):
            # Witness gates (systems/room13_episodes.rpy) carry their own refusal lines.
            lines=st.get("consent_lines",{}).get(key)
            return "soft",list(lines) if lines else [(R13_DEBATE[claim]["chair"],"본 사람이 이름을 밝히지 않은 기록만으로는 확인이 어렵습니다. 다른 물건이 필요합니다.")]
        if key in st.get("accept",[]) and not r13_debate_context_ready(st):
            return "soft",list(st["blocked"])
        if key in st.get("accept",[]):
            # broken_if: a different rebuttal when a condition holds (e.g. the witness died, 0.18.90).
            alt=st.get("broken_if",{}).get(key)
            if alt and r13_has(alt[0]):return "break",list(alt[1])
            # broken_by: a different rebuttal when another record breaks the same statement.
            return "break",list(st.get("broken_by",{}).get(key,st.get("broken",[])))
        if key in st.get("soft",{}):
            return "soft",[st["soft"][key]]
        # 이 논점의 다른 발언을 깨는 자료라면 깎지 않고 방향만 알려 준다.
        for other in r13_debate_statements(claim):
            if other["id"]!=sid and key in other.get("accept",[]) and r13_debate_visible(claim,other):
                return "soft",[(R13_DEBATE[claim]["chair"],"쓸 만한 자료입니다. 다만 지금 그 말이 아니라 다른 말과 맞닿아 있습니다.")]
        return "wrong",[st["wrong"]]

    def r13_debate_next_target(claim,fallback):
        # Prefer a statement that still needs a rebuttal; a true statement is
        # selected only when nothing else is open (e.g. it must be pressed first).
        open_ids=[st["id"] for st in r13_debate_statements(claim) if r13_debate_visible(claim,st) and not r13_debate_is_broken(claim,st["id"])]
        required=[sid for sid in open_ids if not r13_debate_statement(claim,sid).get("truth")]
        return (required or open_ids or [fallback])[0]

    def r13_debate_miss(claim):
        d=r13_debate_state();d["misses"][claim]=d["misses"].get(claim,0)+1;r13_debate_save(d)

    def r13_debate_hint_due(claim,sid):
        """0.18.91: after the second wrong record on one statement, its hint once (as a thought)."""
        hint=r13_debate_statement(claim,sid).get("hint")
        if not hint:return None
        d=r13_debate_state();key=claim+":"+sid;seen=d.setdefault("hint_misses",{})
        seen[key]=seen.get(key,0)+1;r13_debate_save(d)
        return "("+hint+")" if seen[key]==2 else None

    def r13_debate_answerable(claim,st):
        """Could the player break this statement with what they actually hold?"""
        if r13_debate_is_broken(claim,st["id"]) or st.get("truth"):return True
        if st.get("ready_flags"):return all(r13_has(f) for f in st["ready_flags"])
        if not r13_debate_context_ready(st):return False
        consent=st.get("need_consent",{})
        return any(key in store.room13.get("evidence",[]) and (key not in consent or r13_has(consent[key])) for key in st.get("accept",[]))

    def r13_debate_arguable(claim):
        """Every statement can be broken with what the player holds (a full rebuttal is possible)."""
        return all(r13_debate_answerable(claim,st) for st in r13_debate_statements(claim))

    def r13_debate_engageable(claim):
        """At least one required statement can still be broken, or all already are (0.18.35)."""
        if r13_debate_ready(claim):return True
        return any(r13_debate_answerable(claim,st) for st in r13_debate_statements(claim)
            if not st.get("truth") and not r13_debate_is_broken(claim,st["id"]))

    def r13_debate_stuck(claim):
        """Not ready, and nothing left the player can break: only closing remains."""
        return not r13_debate_ready(claim) and not r13_debate_engageable(claim)

    def r13_debate_dad_broken(claim):
        """Statements Dad actually broke (a skipped one does not count)."""
        return sum(1 for st in r13_debate_statements(claim)
            if not st.get("truth") and not r13_debate_skipped(claim,st) and r13_debate_is_broken(claim,st["id"]))

    def r13_debate_emphasis(st):
        text=st["text"]
        return text.split("【",1)[1].split("】",1)[0] if "【" in text else text

    def r13_debate_partial_lines(claim):
        """Closing with some statements broken: what stands and what is left (no record names)."""
        sts=[st for st in r13_debate_statements(claim) if not st.get("truth") and not r13_debate_skipped(claim,st)]
        done=[st for st in sts if r13_debate_is_broken(claim,st["id"])]
        left=[st for st in sts if not r13_debate_is_broken(claim,st["id"])]
        chair=R13_DEBATE[claim]["chair"]
        # 0.18.50: everything broken but no conclusion said (or nothing actually broken by Dad).
        if not left:
            return [("dad","(말은 모두 뒤집었다. 하지만 결론은 말하지 않았다.)",{"thought":True}),
                (chair,"결론을 듣지 못했으니 오늘은 여기까지 하겠습니다.")]
        if not done:
            return [("dad","(맞는 자료를 찾지 못했다. 저 말은 반박되지 않은 채 그대로 남는다.)",{"thought":True})]
        rows=[("dad","(‘%s’ 부분은 뒤집었다. 하지만 ‘%s’ 부분은 뒤집지 못했다.)"%(r13_debate_emphasis(done[-1]),r13_debate_emphasis(left[0])),{"thought":True})]
        rows+=r13_debate_gap_lines(claim,left[0])
        rows.append((chair,"반박된 말은 기록에서 고치겠습니다. 남은 말은 오늘 그대로 둡니다."))
        return rows

    def r13_debate_closed(claim):
        return bool(r13_debate_state()["closed"].get(r13_debate_session(claim)+":"+claim))

    def r13_debate_close(claim,reason):
        d=r13_debate_state();d["closed"][r13_debate_session(claim)+":"+claim]=reason;r13_debate_save(d)

    def r13_case_available():
        """13호 사건 논점의 이야기 순서: C3은 C2 뒤, C4는 C3 뒤에 열린다."""
        props=store.room13.get("propositions",[])
        return [c for c,need in (("C1",None),("C2",None),("C3","C2"),("C4","C3")) if need is None or need in props]

    def r13_debate_evidence_ready(claim):
        """(statements the player could already answer, statements that need evidence)."""
        need=[st for st in r13_debate_statements(claim) if not st.get("truth") and not st.get("skip_if")]
        return sum(1 for st in need if r13_debate_answerable(claim,st)),len(need)

    def r13_campaign_goal():
        """Goal line after day 2: the next meeting and how ready the player is for it."""
        s=store.room13 or {}
        day=s.get("day",1)
        if s.get("finale_started") or day>=14:return None
        if not s.get("trial_ended"):
            if s.get("case_state")=="occurred":
                have,need=r13_debate_evidence_ready("C2")
                return "식당 회의까지 %d일 · 촛대 논점에 쓸 자료 %d/%d"%(max(0,R13_TRIAL_DAY-day),have,need)
            if s.get("case_state")=="prevented":
                return "%d일째 청문까지 %d일 · 함께 들어온 기록을 지키자"%(R13_TRIAL_DAY,max(0,R13_TRIAL_DAY-day))
            notes=r13_first_mystery_notes()
            return ("의문 · "+notes[-1]["question"]) if notes else None
        ready=sum(1 for name,ok in r13_crisis_preparations() if ok)
        return "제단까지 %d일 · 함께 버틸 준비 %d/4"%(max(0,14-day),ready)

    def r13_debate_open(claim):
        """Still worth offering as a choice: not proven, not closed, and the evidence exists."""
        return claim not in store.room13.get("propositions",[]) and not r13_debate_closed(claim) and r13_debate_engageable(claim)

    def r13_debate_seats(session):
        """Each seat's stance 0..2: half the statements broken moves one step, the proof another."""
        props=(store.room13 or {}).get("propositions",[])
        prefix="C" if session=="trial" else "F"
        moved={}
        for claim,spec in R13_DEBATE.items():
            if not claim.startswith(prefix):continue
            done,total=r13_debate_progress(claim)
            step=(1 if done*2>=total and done else 0)+(1 if claim in props else 0)
            for who in spec.get("sway",[]):
                moved[who]=max(moved.get(who,0),step)
        fixed={"seryeon"} if session=="trial" else set()
        # 0.18.90: someone who died before this meeting is replaced by who carried on their duty.
        seats=[getattr(store,"r13_dead_stand_in",lambda w:w)(who) for who in R13_DEBATE_SEATS[session]]
        seats=[who for i,who in enumerate(seats) if who not in seats[:i]]
        return [(who,0 if who in fixed else min(2,moved.get(who,0))) for who in seats]

    def r13_debate_tally(session):
        counts=[0,0,0]
        for who,stance in r13_debate_seats(session):counts[stance]+=1
        return counts

    def r13_debate_markup(text):
        return text.replace("【","{color=#c4562f}").replace("】","{/color}")

    def r13_debate_counter(claim,sid):
        """A counter the opponent builds from what Dad just proved (0.18.41), or None."""
        c=r13_debate_statement(claim,sid).get("counter")
        if not c:return None
        if c.get("need_prop") and c["need_prop"] not in (store.room13 or {}).get("propositions",[]):return None
        return c

    def r13_debate_counter_options(claim,sid):
        opts=list(r13_debate_statement(claim,sid)["counter"]["options"])
        shift=(sum(ord(ch) for ch in claim+sid)+1)%len(opts)
        return opts[shift:]+opts[:shift]

    def r13_debate_conclusion_options(claim):
        opts=list(R13_DEBATE[claim]["conclusion"]["options"])
        # 매번 같은 자리에 정답이 오지 않게, 주장마다 고정된 순서로 섞는다.
        shift=sum(ord(c) for c in claim)%len(opts)
        return opts[shift:]+opts[:shift]

label r13_debate_run(claim):
    # 0.18.91: 회의 직전 자동저장. 회의에서 그만둔 반론은 그 회의 안에서 되돌릴 수 없다.
    $ r13_autosave_now()
    $ r13_meeting_claim=claim
    $ r13_meeting_active=True
    $ r13_meeting_focus_change(claim,r13_debate_statements(claim)[0]["who"])
    call r13_debate_session_run(claim)
    $ r13_meeting_result=_return
    $ r13_meeting_active=False
    hide r13_visitor
    return r13_meeting_result

label r13_debate_session_run(claim):
    $ r13_claim=claim
    if not r13_debate_engageable(claim):
        call r13_debate_unanswerable(claim)
        return False
    $ r13_meeting_begin_opinions(claim)
    $ r13_debate_selected=r13_debate_next_target(claim,r13_debate_statements(claim)[0]["id"])
    $ r13_meeting_resume_listening=False
    $ r13_debate_action=("round",r13_debate_selected)
    jump r13_debate_dispatch
label r13_debate_loop:
    $ r13_meeting_claim=r13_claim
    $ r13_meeting_active=True
    window hide
    hide r13_visitor
    $ r13_meeting_focus_change(r13_claim,r13_debate_statement(r13_claim,r13_debate_selected)["who"])
    call screen r13_debate_board(r13_claim,r13_debate_selected)
    $ r13_meeting_claim=r13_claim
    $ r13_meeting_active=True
    $ r13_debate_action=_return
label r13_debate_dispatch:
    if r13_debate_action[0]=="round":
        call r13_meeting_live_round(r13_claim)
        $ r13_debate_action=_return
        $ r13_meeting_resume_listening=r13_debate_action[0]=="press"
        jump r13_debate_dispatch
    if r13_debate_action[0]=="select":
        $ r13_meeting_feedback=None
        $ r13_debate_selected=r13_debate_action[1]
    elif r13_debate_action[0]=="leave":
        if r13_debate_dad_broken(r13_claim):
            call screen r13_confirm("여기까지 정리하면 이 회의에서는 이 주장을 다시 다룰 수 없다. 반박한 말은 기록에 남고, 남은 말은 그대로 남는다.","여기까지 정리한다","더 찾아본다")
        else:
            call screen r13_confirm("반론을 그만두면 이 회의에서는 이 주장을 다시 다룰 수 없다. 상대의 말이 그대로 남는다.","반론을 그만둔다","더 찾아본다")
        if _return:
            if r13_debate_dad_broken(r13_claim):
                $ r13_debate_close(r13_claim,"partial")
                call r13_lines(r13_debate_partial_lines(r13_claim),"debate:partial:"+r13_claim)
                return False
            $ r13_debate_close(r13_claim,"gave_up")
            call r13_lines([("dad","(맞는 자료를 찾지 못했다. 저 말은 반박되지 않은 채 그대로 남는다.)",{"thought":True})],"debate:gave_up:"+r13_claim)
            return False
    elif r13_debate_action[0]=="listen":
        $ r13_meeting_feedback=None
        $ r13_meeting_replaying=True
        $ r13_debate_st=r13_debate_statement(r13_claim,r13_debate_action[1])
        call r13_lines([(r13_debate_st["who"],r13_debate_st["text"].replace("【","").replace("】",""))]+r13_debate_st.get("press",[]),"meeting:replay:"+r13_claim+":"+r13_debate_st["id"])
        $ r13_meeting_replaying=False
    elif r13_debate_action[0]=="press":
        $ r13_meeting_feedback=None
        show screen r13_meeting_cut_in("잠깐만요.")
        $ r13_debate_st=r13_debate_statement(r13_claim,r13_debate_action[1])
        if r13_debate_st.get("ready_flags") and not all(r13_has(f) for f in r13_debate_st["ready_flags"]):
            call r13_lines(r13_debate_st.get("press_missing",[(r13_debate_st["who"],"그래서, 있습니까?")]),"debate:press_missing:"+r13_claim+":"+r13_debate_st["id"])
        else:
            call r13_lines(r13_debate_st.get("press",[(r13_debate_st["who"],"말한 그대로입니다."),("dad","(저 말을 반박할 자료가 있는지 다시 살펴보자.)",{"thought":True})]),"debate:press:"+r13_claim+":"+r13_debate_st["id"])
        if not r13_debate_st.get("ready_flags") or all(r13_has(f) for f in r13_debate_st["ready_flags"]):
            $ r13_debate_mark("pressed",r13_claim,r13_debate_st["id"])
        if r13_debate_st.get("ready_flags") and r13_debate_is_broken(r13_claim,r13_debate_st["id"]):
            python:
                observation=r13_debate_st["press"][0][1]
                findings=dict(r13_meeting_findings);findings[r13_claim+":"+r13_debate_st["id"]]=observation
                r13_meeting_findings=findings
                r13_meeting_feedback=dict(claim=r13_claim,sid=r13_debate_st["id"],text=observation)
        if r13_debate_st.get("reveals"):
            $ r13_debate_selected=r13_debate_st["reveals"]
    elif r13_debate_action[0]=="present":
        call screen r13_book("resident_seori",present=True,hearing=True)
        $ r13_item=_return
        if r13_item:
            call r13_debate_present_record(r13_claim,r13_debate_action[1],r13_item)
    elif r13_debate_action[0]=="conclude":
        call r13_debate_conclude(r13_claim)
        if _return:
            # Episode 3: without the chief's promise the culprit verdict is not enforced.
            # Week-1 case T: a bought false witness ruins the hearing even with the promise.
            if r13_claim=="C4" and r13_has("fake_testimony"):
                call r13_lines(R13_FAKE_TESTIMONY_LINES,"debate:c4:fake_testimony")
                $ r13_flag("c4_unenforced","fake_testimony_exposed")
                $ r13_debate_close(r13_claim,"unenforced")
                call r13_meeting_public_vote(r13_claim,r13_debate_pick)
                return True
            if r13_claim=="C4" and not r13_has("fair_hearing"):
                call r13_lines(R13_C4_UNENFORCED,"debate:c4:unenforced")
                $ r13_flag("c4_unenforced")
                $ r13_debate_close(r13_claim,"unenforced")
                call r13_meeting_public_vote(r13_claim,r13_debate_pick)
                return True
            $ r13_prove(r13_claim)
            call r13_meeting_public_vote(r13_claim,r13_debate_pick)
            return True
    if r13_meeting_resume_listening and not r13_debate_ready(r13_claim):
        $ r13_meeting_resume_listening=False
        $ r13_debate_action=("round",r13_debate_selected)
        jump r13_debate_dispatch
    $ r13_meeting_resume_listening=False
    jump r13_debate_loop

label r13_debate_unanswerable(claim):
    # 필수 자료가 없으면 선택지 없이 넘어간다. 상대의 말이 반박되지 않은 채 남는다.
    $ r13_debate_gap=next(st for st in r13_debate_statements(claim) if not r13_debate_answerable(claim,st))
    call r13_lines([(r13_debate_gap["who"],r13_debate_gap["text"].replace("【","").replace("】","")),
        ("dad","(저 말을 뒤집을 자료가 지금 내게는 없다.)",{"thought":True})]+r13_debate_gap_lines(claim,r13_debate_gap)+[
        (None,"아무도 그 말을 막지 못했다.")],"debate:unanswerable:"+claim)
    $ r13_debate_close(claim,"no_evidence")
    return

label r13_debate_answer_counter(claim,sid):
    $ r13_debate_c=r13_debate_counter(claim,sid)
    call r13_lines(r13_debate_c["lines"],"debate:counter:"+claim+":"+sid)
    $ r13_debate_pick=renpy.display_menu([(r13_debate_c["prompt"],None)]+[(text,kind) for kind,text in r13_debate_counter_options(claim,sid)])
    if r13_debate_pick=="correct":
        call r13_lines(r13_debate_c["correct"],"debate:counter_ok:"+claim+":"+sid)
        return True
    call r13_lines([r13_debate_c["wrong"][r13_debate_pick],
        ("dad","(내 말이 그대로 되돌아왔다. 자료는 맞다. 답을 다시 생각해 보자.)",{"thought":True})],"debate:counter_wrong:"+claim+":"+sid+":"+r13_debate_pick)
    return False

label r13_debate_conclude(claim):
    if not r13_debate_ready(claim):
        return False
    $ r13_debate_spec=R13_DEBATE[claim]["conclusion"]
    $ r13_debate_menu=[(text,kind) for kind,text in r13_debate_conclusion_options(claim)]
    $ r13_debate_pick=renpy.display_menu([(r13_debate_spec["prompt"],None)]+r13_debate_menu)
    if r13_debate_pick=="correct":
        call r13_lines(r13_debate_spec["correct"],"debate:conclusion:"+claim)
        return True
    call r13_lines([r13_debate_spec[r13_debate_pick]],"debate:conclusion_wrong:"+claim+":"+r13_debate_pick)
    $ r13_debate_miss(claim)
    call r13_meeting_public_vote(claim,r13_debate_pick)
    return False

screen r13_meeting_agenda(claims):
    style_prefix "r13"
    modal True
    zorder 35
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    use r13_meeting_stage(claims[0] if claims else "C1")
    frame:
        area (24,18,900,66) padding (16,8) background R13PaperFrame()
        vbox:
            text "식당 회의 · %d일째"%R13_TRIAL_DAY size 17 color "#795d40"
            text "어느 주장을 다룰까?" size r13_read_size(23,27) color "#493b30"
    $ captions={"C1":"정문이 잠겼으니 아이뿐이라는 주장","C2":"다람이의 방어가 죽음의 원인이라는 주장","C3":"할머니는 그때 식당에 있었다는 말","C4":"할머니가 도우러 들어갔을 뿐이라는 변명"}
    frame:
        area (80,490,1120,210) padding (18,14) background R13PaperFrame()
        viewport:
            mousewheel True draggable True scrollbars "vertical" vscrollbar_unscrollable "hide"
            vbox:
                spacing 12
                for claim in claims:
                    textbutton captions.get(claim,R13_DEBATE[claim]["title"]):
                        style "r13_action_button" xsize 1056 ysize 72 text_size r13_read_size(23,27)
                        action Return(claim) sensitive ready

screen r13_debate_board(claim,selected):
    style_prefix "r13"
    modal True
    zorder 35
    default ready=False
    default statements_open=False
    timer .15 action SetScreenVariable("ready",True)
    $ sel=r13_debate_statement(claim,selected)
    $ done,total=r13_debate_progress(claim)
    $ visible=[st for st in r13_debate_statements(claim) if r13_debate_visible(claim,st)]
    use r13_meeting_stage(claim,sel["who"],True,ready,selected)
    use r13_meeting_chrome(claim)
    textbutton "발언 기록":
        style "r13_action_button" xpos 942 ypos 18 xsize 144 ysize 64 text_size 20
        action ToggleScreenVariable("statements_open") sensitive ready
    textbutton "회의 중단":
        style "r13_action_button" xpos 1096 ypos 18 xsize 160 ysize 64 text_size 20
        action Return(("leave",)) sensitive ready
    if r13_meeting_feedback and r13_meeting_feedback.get("claim")==claim:
        frame:
            area (80,420,1120,68) padding (14,8) background R13PaperPanel()
            vbox:
                spacing 3
                text "방금 확인한 말" size 15 color "#795d40"
                viewport:
                    xsize 1092 ysize 38 mousewheel True draggable True scrollbars "vertical" vscrollbar_unscrollable "hide"
                    text r13_meeting_feedback["text"] size r13_read_size(18,21) color "#493b30" xsize 1068
    frame:
        area (80,500,1120,132) padding (0,0) background R13PaperFrame()
        textbutton "‹":
            style "r13_compact_button" area (20,6,52,44) text_size 32 alt "이전 발언"
            action Return(("select",r13_meeting_next_statement(claim,selected,step=-1))) sensitive ready and len(visible)>1
        text (R13_NAMES[sel["who"]]+(" · 들음" if r13_meeting_heard(claim,selected) else "")+(" · 새 발언" if sel.get("hidden") and not r13_meeting_heard(claim,selected) else "")) xpos 88 ypos 12 size r13_read_size(18,22) color "#795d40"
        text ("발언 %d / %d"%(visible.index(sel)+1,len(visible))) xcenter 560 ypos 12 size r13_read_size(18,22) color "#795d40"
        textbutton "›":
            style "r13_compact_button" area (1048,6,52,44) text_size 32 alt "다음 발언"
            action Return(("select",r13_meeting_next_statement(claim,selected))) sensitive ready and len(visible)>1
        if r13_debate_is_broken(claim,selected):
            add R13AntiqueIcon("check",size=24) xpos 24 ypos 54
        viewport:
            area (56 if r13_debate_is_broken(claim,selected) else 24,50,1040 if r13_debate_is_broken(claim,selected) else 1072,72) mousewheel True draggable True scrollbars "vertical" vscrollbar_unscrollable "hide"
            text (r13_meeting_statement_text(claim,selected) if not r13_debate_is_broken(claim,selected) else "{s}"+sel["text"].replace("【","").replace("】","")+"{/s}") size r13_read_size(23,29) color ("#82725b" if r13_debate_is_broken(claim,selected) else "#79654e" if r13_meeting_heard(claim,selected) else "#493b30") xsize (1018 if r13_debate_is_broken(claim,selected) else 1050)
    use r13_meeting_tools(claim,selected,True,ready)
    if ready and len(visible)>1:
        key "K_LEFT" action Return(("select",r13_meeting_next_statement(claim,selected,step=-1)))
        key "K_RIGHT" action Return(("select",r13_meeting_next_statement(claim,selected)))
    if statements_open:
        frame:
            area (736,94,520,394) padding (16,14) background R13PaperFrame()
            vbox:
                spacing 10
                hbox:
                    spacing 24
                    text ("발언 기록 · %d/%d 반박"%(done,total)) size 21 color "#493b30"
                    textbutton "닫기" style "r13_compact_button" xsize 112 ysize 44 action SetScreenVariable("statements_open",False)
                viewport:
                    xsize 484 ysize 300 mousewheel True draggable True scrollbars "vertical" vscrollbar_unscrollable "hide"
                    vbox:
                        spacing 8
                        for st in visible:
                            button:
                                style "r13_paper_tab_button" xsize 462 padding (12,12)
                                selected st["id"]==selected
                                action Return(("select",st["id"])) sensitive ready
                                vbox:
                                    spacing 5
                                    text (R13_NAMES[st["who"]]+(" · 반박함" if r13_debate_is_broken(claim,st["id"]) else " · 들음" if r13_meeting_heard(claim,st["id"]) else " · 새로 확인" if st.get("hidden") else "")) size 18 color ("#efd191" if st["id"]==selected else "#795d40")
                                    text st["text"].replace("【","").replace("】","") size r13_read_size(20,24) color ("#fff0ce" if st["id"]==selected else "#493b30") xsize 430
                                    if r13_meeting_finding(claim,st["id"]):
                                        text ("확인한 말 · "+r13_meeting_finding(claim,st["id"])) size r13_read_size(17,20) color ("#e1c993" if st["id"]==selected else "#795d40") xsize 430
    key "game_menu" action (SetScreenVariable("statements_open",False) if statements_open else Return(("leave",)))
