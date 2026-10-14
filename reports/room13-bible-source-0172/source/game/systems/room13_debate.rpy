# 공개 회의(7일째 식당 회의 · 14일째 제단 앞 회의).
# 주장 하나 = 상대의 발언 2~3개. 발언의 【강조된 말】을 맞는 자료로 깨고,
# 모두 깨면 결론을 말한다. 틀린 자료·틀린 결론에는 벌이 없다(기회는 많다).
# 실패는 두 가지뿐이다(스토리보드: 증거가 모자라면 다람이는 끌려간다).
#  - 필수 자료를 모으지 못한 논점은 선택지 없이 넘어가고 반론하지 못한 것으로 남는다.
#  - 자료를 찾지 못하고 '반론을 그만둔다'를 고르면 그 회의에서 다시 다룰 수 없다.
# 결과는 기존 r13_prove/propositions로만 남기므로 판결·엔딩 규칙은 그대로다.
init 98 python:
    R13_DEBATE={
        "C1":dict(title="잠긴 방에는 아이만 있었다",
            chair="resident_seori",
            statements=[
                dict(id="s1",who="seryeon",text="복도에 있던 사람들은 【아무도 문으로 들어가지 않았다】고 했습니다.",
                    truth=True,
                    press=[("seryeon","다섯 명이 같은 말을 했어요. 다 같이 거짓말을 했다는 겁니까?"),
                        ("dad","아니요. 그분들이 지켜본 게 어느 문이었는지 묻는 겁니다."),
                        ("seryeon","……복도 쪽 문이죠. 그 방에 다른 문이 어디 있습니까?")],
                    reveals="s2",
                    hint="그 사람들 말은 맞다. 문제는 그 사람들이 본 것이 '복도 쪽 문' 하나뿐이라는 점이다.",
                    wrong=("seryeon","그 사람들이 본 것까지 부정하시는 겁니까? 그건 틀린 말이 아니에요.")),
                dict(id="s2",who="seryeon",text="그 방으로 들어가는 길은 【복도 쪽 문 하나뿐】입니다.",
                    hidden=True,
                    accept=["E05","E37"],
                    soft={"E04":("resident_seori","종이에 그린 선만으로는 지금도 그 길이 열리는지 알 수 없습니다. 직접 확인한 것이 있습니까?")},
                    hint="도면만으로는 부족하다. 내가 직접 열어 본 길이 있다.",
                    broken=[("dad","주방 레버를 올리고 책장 아래 책을 당기면, 책장 뒤 문이 열립니다. 제가 직접 열었습니다."),
                        ("seryeon","……세탁실로 이어진다고요?")],
                    wrong=("seryeon","그게 이 방에 다른 길이 있다는 증거입니까?")),
            ],
            conclusion=dict(prompt="다른 길이 있다는 걸 어떻게 정리할까?",
                options=[
                    ("correct","복도에서 본 건 앞문뿐이다. 다른 길이 있으니 '아이만 들어갈 수 있었다'는 말은 틀렸다."),
                    ("over","책장 뒤 길이 있으니, 그 길을 아는 할머니가 범인이다."),
                    ("weak","통로 안에 엄마 물건이 있었으니, 그날 엄마가 그 길로 왔을지도 모른다."),
                ],
                correct=[("resident_seori","정문 말고도 들어갈 길이 있었습니다. '아이만 들어갈 수 있었다'는 말은 고치십시오."),
                    ("seryeon","통로 안에 그 아이 엄마 물건이 있었다면서요."),
                    ("dad","오래전 흔적이 그날 누가 지나갔는지 말해 주지는 않습니다."),
                    ("resident_seori","그날 누가 그 길을 썼는지는 따로 따지겠습니다.")],
                over=("resident_seori","길이 있다는 것과 누가 그 길을 썼는지는 다른 문제입니다. 아직 그 사람을 말할 수는 없습니다."),
                weak=("seryeon","그럼 아버님 부인을 의심하자는 겁니까? 오래된 물건 하나로요?")),
            sway=["resident_tori","doto"]),

        "C2":dict(title="아이가 친 촛대 때문에 죽었다",
            chair="resident_seori",
            statements=[
                dict(id="s1",who="resident_ppul",text="아이가 촛대로 【어르신의 머리를 내리쳤다】고 했습니다.",
                    accept=["E06","E08"],
                    hint="다람이가 친 곳은 머리가 아니었다. 다람이를 만났을 때 들은 말과 처음 상처를 본 기록이 있다.",
                    broken=[("dad","다람이가 친 건 자기 팔을 붙잡은 손입니다. 처음 상처를 본 기록에도 팔의 상처와 머리의 상처가 따로 적혀 있습니다."),
                        ("resident_ppul","팔이든 머리든, 아이가 친 건 사실 아닙니까?")],
                    wrong=("resident_ppul","그게 아이가 머리를 치지 않았다는 말이 됩니까?")),
                dict(id="s2",who="resident_ppul",text="촛대는 【한 번 휘둘렸을 뿐】입니다. 그 한 번에 돌아가셨어요.",
                    accept=["E07","E35"],
                    hint="촛대는 바닥에 떨어져 두 동강이 났다. 머리 상처는 부러진 윗부분의 날과 맞는다.",
                    broken=[("dad","촛대는 바닥에 떨어져 둘로 갈라졌습니다. 머리의 상처는 갈라진 윗부분의 날카로운 안쪽과 맞습니다."),
                        ("dad","촛대가 부러진 다음에, 누군가 그 조각을 다시 들었다는 뜻입니다.")],
                    wrong=("resident_ppul","그걸로 촛대가 두 번 쓰였다는 걸 어떻게 압니까?")),
                dict(id="s3",who="resident_ppul",text="그 방에는 【아이 혼자】 있었습니다. 다시 휘두를 사람이 누가 있습니까?",
                    accept=["E10","E09"],
                    need_consent={"E10":"bami_consent"},
                    hint="촛대가 부러진 뒤 다람이는 침대 밑에 숨어 있었다. 통로 쪽에서 다가온 발자국도 있었다.",
                    broken=[("dad","촛대가 갈라진 직후 아이는 침대 밑으로 숨었고, 구하러 들어갈 때까지 나오지 않았습니다. 그사이 통로 쪽에서 다가온 발자국이 있습니다."),
                        ("buri","……그럼 할아버지를 친 사람이 따로 있다는 거예요?")],
                    wrong=("resident_ppul","그 자료가 방 안에 다른 사람이 있었다는 증거입니까?")),
            ],
            conclusion=dict(prompt="촛대와 상처의 순서로 무엇을 말할까?",
                options=[
                    ("correct","아이는 팔을 쳤다. 머리의 상처는 촛대가 부러진 뒤, 침대 밑에 숨은 아이가 아닌 누군가가 냈다."),
                    ("over","그러니 통로를 아는 할머니가 어르신을 죽였다."),
                    ("weak","아이는 겁에 질려 있었으니 무슨 일을 했든 책임이 없다."),
                ],
                correct=[("resident_seori","아이가 한 일과, 어르신을 죽게 한 일을 같은 것으로 적을 수 없습니다."),
                    ("daram","그럼…… 내가 때린 건?"),
                    ("dad","그건 네가 손을 놓게 하려고 한 일이야. 죽게 한 일과는 달라.")],
                over=("resident_seori","누군가 다시 촛대를 들었다는 것까지입니다. 그 사람이 누구인지는 아직 아무도 보여 주지 않았습니다."),
                weak=("buri","할아버지도 겁에 질려 있었어요. 그런 말로 끝내지 말아요.")),
            sway=["buri","resident_bori","nabi"]),

        "C3":dict(title="할머니는 그때 식당에 있었다",
            chair="resident_seori",
            statements=[
                dict(id="s1",who="granny",text="비명이 들릴 때 나는 【식당에】 있었어요. 다들 봤잖아요.",
                    truth=True,
                    press=[("granny","나비가 바로 옆에 있었어요. 물어봐요."),("nabi","네. 첫 비명 때는 같이 있었어요.")],
                    hint="이 말은 사실이다. 따질 것은 '첫 비명 다음'이다.",
                    wrong=("nabi","제가 같이 있던 것까지 없던 일로 만들지는 마세요.")),
                dict(id="s2",who="granny",text="그 뒤로도 나는 【계속 사람들 곁에】 있었어요.",
                    accept=["E12","E11"],
                    hint="공구를 가지러 주방에 간 뒤로는 아무도 할머니를 보지 못했다.",
                    broken=[("nabi","공구를 가지러 주방에 가신 뒤로는…… 저도 못 봤어요."),
                        ("granny","잠깐 안 보였다는 게 전부잖아요.")],
                    wrong=("granny","그게 내가 혼자 있었다는 증거예요?")),
                dict(id="s3",who="granny",text="주방에서 그 방까지는 【한참 걸려요】. 그 잠깐에 다녀올 수는 없어요.",
                    accept=["E05","E37"],
                    hint="주방과 13호 책장은 통로로 바로 이어져 있다.",
                    broken=[("dad","주방에서 레버를 올리면 13호 책장 뒤로 바로 이어집니다. 복도를 돌아갈 필요가 없습니다."),
                        ("granny","……그 길은 세탁물을 나르던 길이에요.")],
                    wrong=("granny","그게 주방에서 그 방까지 가까웠다는 거예요?")),
            ],
            conclusion=dict(prompt="할머니의 그날 움직임을 어떻게 정리할까?",
                options=[
                    ("correct","첫 비명 때 식당에 있었던 건 맞다. 하지만 주방에 간 뒤로는 아무도 못 봤고, 주방에서 그 방까지 바로 가는 길이 있다."),
                    ("over","그 시간에 할머니가 13호실에 가서 어르신을 죽였다."),
                    ("weak","나비는 할머니 편이니 그 말은 믿을 수 없다."),
                ],
                correct=[("resident_seori","첫 비명 때 식당에 있었다는 건 사실입니다. 하지만 그 뒤 시간까지 설명해 주지는 않습니다."),
                    ("resident_seori","할머니가 그 방에 실제로 들어갔는지는 이어서 보겠습니다.")],
                over=("resident_seori","갈 수 있었다는 것과 갔다는 것은 다릅니다. 그건 아직 보여 주지 않았습니다."),
                weak=("nabi","저는 본 것만 말했어요. 편을 든 게 아니에요.")),
            sway=["nabi","resident_kongi"]),

        "C4":dict(title="들어갔다 해도 도우려 했을 뿐이다",
            chair="resident_seori",
            statements=[
                dict(id="s1",who="granny",text="그 핀은 【오후에 그분을 도울 때】 떨어졌을 수도 있잖아요.",
                    accept=["E15"],
                    soft={"E13":("resident_seori","그날 새 핀으로 바꿨다는 건 알겠습니다. 언제까지 할머니 옷에 있었는지가 궁금합니다.")},
                    hint="첫 비명 직후, 나비가 그 핀을 할머니 목도리에 직접 여며 주었다.",
                    broken=[("nabi","첫 비명 바로 뒤에 제가 그 핀을 여며 드렸어요. 그때는 목도리에 있었어요."),
                        ("granny","……그래서요?")],
                    wrong=("granny","그게 오후에 떨어진 게 아니라는 증거예요?")),
                dict(id="s2",who="granny",text="구하려고 들어갔다가 【촛대를 주웠을 뿐】이에요.",
                    accept=["E14","E35"],
                    soft={"E33":("resident_seori","구한 직후 누가 촛대를 거뒀는지는 확인됩니다. 그 전에 무슨 일이 있었는지가 문제입니다.")},
                    hint="핀은 촛대 장식 고리 안에, 내려친 방향으로 눌려 끼어 있었다.",
                    broken=[("dad","핀은 촛대 장식 고리 안에 끼어 있었습니다. 고리는 내려친 방향으로 찌그러졌고, 핀도 같이 휘었습니다."),
                        ("dad","주워 들다가 들어간 게 아닙니다. 내려친 순간에 끼어 들어간 겁니다.")],
                    wrong=("granny","그걸로 내가 촛대를 휘둘렀다는 거예요?")),
                dict(id="s3",who="granny",text="그분이 그렇게 위험한 줄은 【몰랐어요】.",
                    accept=["E36"],
                    hint="전날 저녁, 할머니가 직접 쓴 진료 요청이 있다.",
                    broken=[("resident_seori","전날 저녁 할머니가 직접 적어 보낸 쪽지입니다. 발작이 심하다고, 그리고 제가 '혼자 두지 마라'고 답했습니다."),
                        ("granny","……….")],
                    wrong=("granny","그게 내가 알았다는 증거예요?")),
            ],
            conclusion=dict(prompt="핀과 촛대로 무엇을 말할까?",
                options=[
                    ("correct","첫 비명 뒤에도 핀은 할머니 옷에 있었다. 그 핀이 내려친 방향으로 눌린 고리에 끼었다. 구하다 주운 게 아니라 내려친 것이다."),
                    ("over","할머니는 처음부터 우리 가족을 노리고 이 모든 걸 꾸몄다."),
                    ("weak","할머니가 그 방에 들어간 적이 있다는 것까지만 말할 수 있다."),
                ],
                correct=[("resident_seori","위험을 알면서 둘만 남겼고, 촛대에 할머니의 핀이 내려친 방향으로 끼어 있습니다. 구하려다 생긴 흔적이라는 말은 받아들일 수 없습니다."),
                    ("resident_seori","대답하지 않으셔도, 내놓은 자료로 판단하겠습니다.")],
                over=("resident_seori","오늘은 그날 그 방에서 있었던 일만 따집니다. 가족을 부른 이유는 따로 보여 주셔야 합니다."),
                weak=("dad","(아니다. 거기서 멈추면 '도우려 했다'는 말이 그대로 남는다.)")),
            sway=["buri","resident_bori","resident_kongi"]),

        "F1":dict(title="저 사람들은 돌아올 수 없다",
            chair="resident_seori",
            statements=[
                dict(id="s1",who="resident_ppul",text="가족도 못 알아봅니다. 【돌아올 수 없는 분들】로 판단됐어요.",
                    accept=["E20"],
                    hint="처음 증상이 나타난 뒤 나아진 사람이 있었다.",
                    broken=[("dad","증상이 시작된 뒤 다시 이름을 말하고 가족을 알아본 사람이 있습니다. 적어 둔 관찰이 있습니다."),
                        ("resident_ppul","한 사람이 잠깐 좋아졌을 뿐이겠죠.")],
                    wrong=("resident_ppul","그게 저분들이 돌아올 수 있다는 증거입니까?")),
                dict(id="s2",who="resident_ppul",text="나아졌다는 기록은 【처음부터 없었습니다】.",
                    accept=["E31"],
                    hint="누군가 지우기 전에 베껴 둔 기록이 남아 있다.",
                    broken=[("dad","지우기 전에 베껴 둔 기록입니다. 나아진 사람을 '되돌릴 수 없음'으로 다시 적은 건 할머니입니다."),
                        ("resident_ppul","……누가 그걸 지웠다는 겁니까?")],
                    wrong=("resident_ppul","그 기록이 원래 있었다는 걸 어떻게 압니까?")),
            ],
            conclusion=dict(prompt="회복 기록이 뜻하는 것은?",
                options=[
                    ("correct","모두 낫는다는 뜻은 아니다. 하지만 '아무도 돌아올 수 없다'는 판단은 틀렸다."),
                    ("over","모두 나을 수 있으니, 지금 당장 전부 풀어 줘야 한다."),
                    ("weak","나중에 다시 나빠졌으니 나아졌던 기록은 빼고 생각하자."),
                ],
                correct=[("resident_seori","잠깐이라도 나아졌던 일을 지워서는 안 됐습니다."),
                    (None,"보리가 환자를 누르던 손을 풀고 담요를 덮었다. 장치는 아직 멈추지 않았다.")],
                over=("nabi","풀었다가 다치면요? 돌아올 수 있다는 것과 지금 괜찮다는 건 달라요."),
                weak=("resident_seori","다시 나빠진 것도 적어야 합니다. 하지만 그 전의 회복을 지우면 '돌아온 적 없다'는 거짓말이 됩니다.")),
            sway=["resident_bori","nabi"]),

        "F2":dict(title="희생 말고는 불을 살릴 방법이 없다",
            chair="resident_seori",
            statements=[
                dict(id="s1",who="resident_ppul",text="지난번 희생 뒤에 【불이 돌아왔습니다】. 다들 봤잖아요.",
                    truth=True,
                    press=[("resident_ppul","돌아왔어요. 그날 밤 우리 집도 따뜻했습니다."),("mom","올라간 건 사실이에요. 그다음에 어떻게 됐는지가 문제예요.")],
                    reveals="s2",
                    hint="불이 돌아온 건 사실이다. 그 뒤가 어땠는지 봐야 한다.",
                    wrong=("resident_ppul","그날 밤 불이 돌아온 것까지 거짓말이라는 겁니까?")),
                dict(id="s2",who="resident_ppul",text="그러니 【계속 그렇게 하면】 버틸 수 있습니다.",
                    hidden=True,
                    accept=["E21","E22"],
                    hint="희생할 때마다 버틴 날이 줄었다. 오래된 운전 기록에도 그렇게 적혀 있다.",
                    broken=[("buri","희생할 때마다 버틴 날이 줄었어요. 어르신이 남긴 운전 기록에도 그렇게 적혀 있어요."),
                        ("resident_ppul","그래도 지금은 그 방법밖에 없잖소!")],
                    wrong=("resident_ppul","그게 다음엔 안 된다는 증거입니까?")),
                dict(id="s3",who="resident_ppul",text="사람을 바치는 것 말고는 【다른 방법이 없습니다】.",
                    accept=["E23","E24"],
                    soft={"E30":("resident_seori","옛 글을 읽어 낸 건 알겠습니다. 실제로 해 본 기록이 있습니까?")},
                    hint="남은 힘을 한곳으로 옮겨 본 기록이 두 번 있다.",
                    broken=[("mom","여러 돌에 남은 힘을 한곳으로 모았어요. 작은 집에서 한 번, 저녁에 더 큰 곳에서 한 번 해 봤고요."),
                        ("resident_seori","새로 채우는 건 아니지만, 사람을 잇지 않고 버틸 방법은 있습니다.")],
                    wrong=("resident_ppul","그게 다른 방법이 있다는 증거입니까?")),
            ],
            conclusion=dict(prompt="두 번 지켜본 결과로 무엇을 말할까?",
                options=[
                    ("correct","희생 뒤 반짝 올라간 힘은 갈수록 짧아졌다. 남은 힘을 모으면 사람을 잇지 않고 필요한 곳부터 버틸 수 있다."),
                    ("over","남은 힘을 모으면 장치를 영원히 다시 채울 수 있다."),
                    ("weak","희생 직후엔 불이 올랐으니, 아직은 쓸 만한 방법이다."),
                ],
                correct=[("resident_ppul","그것도 결국 다 쓰잖소!"),
                    ("mom","맞아요. 그래서 필요한 곳에 모이고, 그동안 장작과 식량을 마련해야 해요. 다음 사람을 바칠 날을 기다리는 대신요."),
                    (None,"작업자가 손을 멈췄다. 환자 쪽 관이 내려왔다. 대피소를 맡은 사람들이 버틸 시간을 세기 시작했다.")],
                over=("mom","아니에요. 모아도 언젠가는 다 써요. 그동안 다른 준비를 해야 해요."),
                weak=("mom","그 뒤로 더 떨어진 걸 봐요. 한 번 오른 것과 계속 버틸 수 있다는 건 달라요.")),
            sway=["resident_bori","buri","nabi"]),

        "F3":dict(title="오늘 밤 희생 없이 살 방법이 없다",
            chair="resident_seori",
            statements=[
                dict(id="s1",who="resident_ppul",text="불을 끄면 오늘 밤 【잘 곳이 없습니다】.",
                    accept=["E25"],
                    hint="학교를 대피소로 쓰기로 넘겨받았다.",
                    broken=[("dad","학교를 넘겨받았습니다. 몇 명이 들어갈 수 있는지도 적어 뒀습니다.")],
                    wrong=("resident_ppul","그게 오늘 밤 잘 곳입니까?")),
                dict(id="s2",who="nabi",text="방만 있으면 뭐해요. 【먹을 것과 장작】은요?",
                    accept=["E26"],
                    hint="학교로 옮긴 장작과 곡식의 양을 적어 두었다.",
                    broken=[("nabi","……학교에 옮긴 양이 이만큼이면, 오늘 밤은 돼요.")],
                    wrong=("nabi","없는 걸 있다고 할 수는 없잖아요.")),
                dict(id="s3",who="resident_ppul",text="밤새 장치를 손으로 돌리고 환자를 옮길 【사람이 없습니다】.",
                    ready_flags=["operators_ready","patient_transport"],
                    press=[("buri","이쪽은 내가 잡을게요. 다음 교대도 정했어요."),("resident_bori","환자는 우리가 수레로 옮겨요.")],
                    press_missing=[("nabi","옮길 사람, 밤에 남을 사람요. 우리 손에 실제로 있는 것부터 세 봐요.")],
                    hint="교대할 사람과 환자를 옮길 사람을 실제로 구해 두었는지가 전부다. 되물으면 확인된다.",
                    wrong=("resident_ppul","사람은 종이로 대신할 수 없습니다.")),
            ],
            conclusion=dict(prompt="오늘 밤을 버틸 방법은?",
                options=[
                    ("correct","학교로 모여 실제 식량을 나누고, 장치는 손으로 교대하며 돌린다."),
                    ("over","장치를 바로 멈추고 각자 집에서 버틴다."),
                    ("weak","집마다 같은 양을 나누고 각자 불을 지킨다."),
                ],
                correct=[("nabi","학교에 솥 옮겼어요. 들어오실 분부터 들어오세요."),
                    ("resident_bori","집집마다 나누면 모자라요. 모여 있어야 해요."),
                    ("buri","이쪽은 내가 잡을게요.")],
                over=("resident_ppul","장치를 바로 멈추면 대피소로 옮기기도 전에 얼어 죽습니다."),
                weak=("resident_bori","집집마다 불을 살리면 장작이 모자라요. 빈 방까지 데울 몫은 없다고요.")),
            sway=["resident_bori","nabi"]),

        "F4":dict(title="그 가족이 마을의 질서를 깨뜨렸다",
            chair="resident_seori",
            statements=[
                dict(id="s1",who="granny",text="나는 그 사람들한테 【아내를 찾게 해 줬어요】.",
                    accept=["E18","E17"],
                    soft={"E01":("granny","그래요, 내가 보낸 편지예요. 그게 어때서요?")},
                    hint="아내는 첫 주에 이미 가족에게 경고를 보냈다. 이미 도망친 뒤였다.",
                    broken=[("dad","아내는 첫 주에 이미 저희에게 오지 말라고 경고했습니다. 전해지지 않았을 뿐이죠. 당신에게서 도망친 뒤였습니다."),
                        ("mom","돌아갈 수는 없었어요. 가족에게 돌아갈 방법을 찾고 있었지.")],
                    wrong=("granny","그게 내가 거짓말했다는 거예요?")),
                dict(id="s2",who="granny",text="아이를 떼어 놓자고 한 건 【사건이 난 뒤의 보호】였어요.",
                    accept=["E16"],
                    skip_if="C4",
                    hint="가족을 떼어 놓자는 요청은 사건 전에 이미 쓰여 있었다.",
                    broken=[("resident_seori","보낸 날짜는 사건 전입니다. 보호라는 말과 그 요청을 쓴 날이 맞지 않습니다."),
                        ("granny","그 여자가 돌아왔으면 아이는 다치지 않아도 됐어.")],
                    wrong=("granny","그게 사건 전이라는 증거예요?")),
            ],
            conclusion=dict(prompt="편지와 경고, 떼어 놓자는 요청을 이으면?",
                options=[
                    ("correct","엄마를 다시 붙잡으려고 가족을 불렀고, 아이를 떼어 놓아 엄마를 움직이려 했다."),
                    ("over","할머니 혼자 마을의 모든 희생을 꾸몄다."),
                    ("weak","할머니가 편지를 보낸 건 사실이다."),
                ],
                correct=[("dad","아내가 돌아오기를 거절한 뒤 이 편지를 보냈습니다. 가족을 떼어 놓는 요청도 먼저 써 두었고요."),
                    ("dad","대답하지 않으셔도 기록은 남습니다."),
                    ("neoul","이후 지시는 받지 않겠습니다. 자료부터 챙기죠.")],
                over=("resident_ppul","희생을 정한 건 마을 회의였습니다. 그 책임까지 한 사람에게 미룰 수는 없어요."),
                weak=("granny","편지 보낸 게 죄예요?")),
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

    def r13_debate_is_broken(claim,sid):
        st=r13_debate_statement(claim,sid)
        if r13_debate_skipped(claim,st):return True
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
        consent=st.get("need_consent",{}).get(key)
        if consent and not r13_has(consent):
            return "soft",[(R13_DEBATE[claim]["chair"],"본 사람이 이름을 밝히지 않은 기록만으로는 확인이 어렵습니다. 다른 물건이 필요합니다.")]
        if key in st.get("accept",[]):
            return "break",list(st.get("broken",[]))
        if key in st.get("soft",{}):
            return "soft",[st["soft"][key]]
        # 이 논점의 다른 발언을 깨는 자료라면 깎지 않고 방향만 알려 준다.
        for other in r13_debate_statements(claim):
            if other["id"]!=sid and key in other.get("accept",[]) and r13_debate_visible(claim,other):
                return "soft",[(R13_DEBATE[claim]["chair"],"쓸 만한 자료입니다. 다만 지금 그 말이 아니라 다른 말과 맞닿아 있습니다.")]
        return "wrong",[st["wrong"]]

    def r13_debate_miss(claim):
        d=r13_debate_state();d["misses"][claim]=d["misses"].get(claim,0)+1;r13_debate_save(d)

    def r13_debate_answerable(claim,st):
        """Could the player break this statement with what they actually hold?"""
        if r13_debate_is_broken(claim,st["id"]) or st.get("truth"):return True
        if st.get("ready_flags"):return all(r13_has(f) for f in st["ready_flags"])
        consent=st.get("need_consent",{})
        return any(key in store.room13.get("evidence",[]) and (key not in consent or r13_has(consent[key])) for key in st.get("accept",[]))

    def r13_debate_arguable(claim):
        return all(r13_debate_answerable(claim,st) for st in r13_debate_statements(claim))

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
                return "식당 회의까지 %d일 · 촛대 논점에 쓸 자료 %d/%d"%(max(0,7-day),have,need)
            if s.get("case_state")=="prevented":
                return "7일째 청문까지 %d일 · 함께 들어온 기록을 지키자"%max(0,7-day)
            notes=r13_first_mystery_notes()
            return ("의문 · "+notes[-1]["question"]) if notes else None
        ready=sum(1 for name,ok in r13_crisis_preparations() if ok)
        return "제단까지 %d일 · 함께 버틸 준비 %d/4"%(max(0,14-day),ready)

    def r13_debate_open(claim):
        """Still worth offering as a choice: not proven, not closed, and the evidence exists."""
        return claim not in store.room13.get("propositions",[]) and not r13_debate_closed(claim) and r13_debate_arguable(claim)

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
        return [(who,0 if who in fixed else min(2,moved.get(who,0))) for who in R13_DEBATE_SEATS[session]]

    def r13_debate_tally(session):
        counts=[0,0,0]
        for who,stance in r13_debate_seats(session):counts[stance]+=1
        return counts

    def r13_debate_markup(text):
        return text.replace("【","{color=#c4562f}").replace("】","{/color}")

    def r13_debate_conclusion_options(claim):
        opts=list(R13_DEBATE[claim]["conclusion"]["options"])
        # 매번 같은 자리에 정답이 오지 않게, 주장마다 고정된 순서로 섞는다.
        shift=sum(ord(c) for c in claim)%len(opts)
        return opts[shift:]+opts[:shift]

label r13_debate_run(claim):
    $ r13_claim=claim
    if not r13_debate_arguable(claim):
        call r13_debate_unanswerable(claim)
        return False
    $ r13_debate_selected=next((st["id"] for st in r13_debate_statements(claim) if r13_debate_visible(claim,st) and not r13_debate_is_broken(claim,st["id"])),r13_debate_statements(claim)[0]["id"])
label r13_debate_loop:
    window hide
    hide r13_visitor
    call screen r13_debate_board(r13_claim,r13_debate_selected)
    $ r13_debate_action=_return
    if r13_debate_action[0]=="select":
        $ r13_debate_selected=r13_debate_action[1]
    elif r13_debate_action[0]=="leave":
        call screen r13_confirm("반론을 그만두면 이 회의에서는 이 주장을 다시 다룰 수 없다. 상대의 말이 그대로 남는다.","반론을 그만둔다","더 찾아본다")
        if _return:
            $ r13_debate_close(r13_claim,"gave_up")
            call r13_lines([("dad","(맞는 자료를 찾지 못했다. 이 말은 그대로 남는다.)",{"thought":True})],"debate:gave_up:"+r13_claim)
            return False
    elif r13_debate_action[0]=="press":
        $ r13_debate_st=r13_debate_statement(r13_claim,r13_debate_action[1])
        if r13_debate_st.get("ready_flags") and not all(r13_has(f) for f in r13_debate_st["ready_flags"]):
            call r13_lines(r13_debate_st.get("press_missing",[(r13_debate_st["who"],"그래서, 있습니까?")]),"debate:press_missing:"+r13_claim+":"+r13_debate_st["id"])
        else:
            call r13_lines(r13_debate_st.get("press",[(r13_debate_st["who"],"말한 그대로입니다."),("dad","(이 말을 깰 자료가 있는지 다시 보자.)",{"thought":True})]),"debate:press:"+r13_claim+":"+r13_debate_st["id"])
        $ r13_debate_mark("pressed",r13_claim,r13_debate_st["id"])
        if r13_debate_st.get("reveals"):
            $ r13_debate_selected=r13_debate_st["reveals"]
    elif r13_debate_action[0]=="present":
        call screen r13_book("resident_seori",present=True,hearing=True)
        $ r13_item=_return
        if r13_item:
            $ r13_debate_result,r13_debate_rows=r13_debate_judge(r13_claim,r13_debate_action[1],r13_item)
            show screen r13_material_corner(r13_item)
            call r13_lines(r13_debate_rows,"debate:"+r13_debate_result+":"+r13_claim+":"+r13_debate_action[1]+":"+r13_item)
            hide screen r13_material_corner
            if r13_debate_result=="break":
                $ r13_debate_mark("broken",r13_claim,r13_debate_action[1])
                $ r13_submit(r13_claim,r13_item)
                $ r13_debate_selected=next((st["id"] for st in r13_debate_statements(r13_claim) if r13_debate_visible(r13_claim,st) and not r13_debate_is_broken(r13_claim,st["id"])),r13_debate_selected)
            elif r13_debate_result=="wrong":
                $ r13_debate_miss(r13_claim)
    elif r13_debate_action[0]=="conclude":
        call r13_debate_conclude(r13_claim)
        if _return:
            $ r13_prove(r13_claim)
            return True
    jump r13_debate_loop

label r13_debate_unanswerable(claim):
    # 필수 자료가 없으면 선택지 없이 넘어간다. 상대의 말이 반박되지 않은 채 남는다.
    $ r13_debate_gap=next(st for st in r13_debate_statements(claim) if not r13_debate_answerable(claim,st))
    call r13_lines([(r13_debate_gap["who"],r13_debate_gap["text"].replace("【","").replace("】","")),
        ("dad","(이 말을 뒤집을 자료가 내게 없다.)",{"thought":True}),
        (None,"아무도 그 말을 막지 못했다.")],"debate:unanswerable:"+claim)
    $ r13_debate_close(claim,"no_evidence")
    return

label r13_debate_conclude(claim):
    $ r13_debate_spec=R13_DEBATE[claim]["conclusion"]
    $ r13_debate_menu=[(text,kind) for kind,text in r13_debate_conclusion_options(claim)]
    $ r13_debate_pick=renpy.display_menu([(r13_debate_spec["prompt"],None)]+r13_debate_menu)
    if r13_debate_pick=="correct":
        call r13_lines(r13_debate_spec["correct"],"debate:conclusion:"+claim)
        return True
    call r13_lines([r13_debate_spec[r13_debate_pick]],"debate:conclusion_wrong:"+claim+":"+r13_debate_pick)
    $ r13_debate_miss(claim)
    return False

screen r13_debate_board(claim,selected):
    style_prefix "r13"
    modal True
    zorder 35
    default ready=False
    timer .3 action SetScreenVariable("ready",True)
    $ session=r13_debate_session(claim)
    $ done,total=r13_debate_progress(claim)
    $ visible=[st for st in r13_debate_statements(claim) if r13_debate_visible(claim,st)]
    $ sel=r13_debate_statement(claim,selected)
    add Solid("#0d1a1fd8")
    # 머리줄: 장소 · 주장 · 신뢰
    frame:
        area (40,22,1200,86) padding (22,10) background Solid("#14272bf0")
        vbox:
            spacing 4
            text ("식당 회의 · 7일째" if session=="trial" else "제단 앞 회의 · 14일째") size r13_read_size(19,22) color "#9fcbd9"
            text ("상대의 주장 · "+R13_DEBATE[claim]["title"]) size r13_read_size(28,32) color "#f6d18a"
    # 자리와 여론
    $ tally=r13_debate_tally(session)
    $ names=R13_DEBATE_STANCE[session]
    frame:
        area (40,116,1200,46) padding (16,6) background Solid("#14272bc0")
        hbox:
            spacing 10 yalign .5
            for who,stance in r13_debate_seats(session):
                frame:
                    padding (8,3) background Solid(("#7d3b2c","#4e5552","#2f6b55")[stance])
                    text (("▶ " if who==sel["who"] else "")+R13_NAMES.get(who,who)) size r13_read_size(17,20) color ("#ffe4a1" if who==sel["who"] else "#f3eee2") bold (who==sel["who"])
        text ("%s %d · %s %d · %s %d"%(names[0],tally[0],names[1],tally[1],names[2],tally[2])) xalign 1.0 yalign .5 size r13_read_size(17,20) color "#d4dfd8"
    # 발언 카드
    viewport:
        area (40,172,820,452) mousewheel True draggable True scrollbars "vertical" vscrollbar_unscrollable "hide"
        vbox:
            spacing 12
            for st in visible:
                $ broken=r13_debate_is_broken(claim,st["id"])
                button:
                    xsize 796 padding (18,12)
                    background Solid("#f1e7d0" if st["id"]==selected else "#d9cdb2" if not broken else "#a9a493")
                    hover_background Solid("#f6edd9")
                    action Return(("select",st["id"])) sensitive ready
                    vbox:
                        spacing 6
                        hbox:
                            spacing 12
                            text R13_NAMES.get(st["who"],st["who"]) size r13_read_size(19,22) color "#6b4a22"
                            if broken:
                                text "반박함" size r13_read_size(19,22) color "#2f6b55"
                            elif st.get("truth") and r13_debate_is_pressed(claim,st["id"]):
                                text "사실인 말" size r13_read_size(19,22) color "#5d6a66"
                            elif r13_debate_is_pressed(claim,st["id"]):
                                text "되물음" size r13_read_size(19,22) color "#5d6a66"
                        text (r13_debate_markup(st["text"]) if not broken else "{s}"+st["text"].replace("【","").replace("】","")+"{/s}"):
                            size r13_read_size(23,27) color "#2c2a24" xsize 756
    # 오른쪽: 선택한 말에 대한 행동
    frame:
        area (876,172,364,452) padding (20,18) background Solid("#14272bf0")
        vbox:
            spacing 14
            text ("반박한 말 %d / %d"%(done,total)) size r13_read_size(20,24) color "#9fcbd9"
            hbox:
                spacing 12
                if sel["who"] in CAST:
                    add Transform(r13_art(sel["who"],"avatar_neutral"),xysize=(68,76),fit="contain",nearest=True)
                text (R13_NAMES.get(sel["who"],sel["who"])+"의 말") size r13_read_size(22,26) color "#f6d18a" xsize 240 yalign .5
            if r13_debate_is_pressed(claim,selected) or claim in (room13.get("debate") or {}).get("misses",{}) and (room13.get("debate") or {})["misses"][claim]>=2:
                text ("("+sel["hint"]+")") size r13_read_size(20,24) color "#a8cdec" xsize 324
            else:
                text "되물으면 더 들을 수 있다." size r13_read_size(20,24) color "#7d8f8c" xsize 324
            null height 4
            textbutton "되묻기" style "r13_action_button" xsize 324 ysize 56 text_size r13_read_size(22,26):
                action Return(("press",selected)) sensitive ready and not r13_debate_is_broken(claim,selected)
            textbutton "자료로 반박" style "r13_action_button" xsize 324 ysize 56 text_size r13_read_size(22,26):
                action Return(("present",selected)) sensitive ready and not r13_debate_is_broken(claim,selected) and not sel.get("ready_flags")
    hbox:
        xpos 40 ypos 640 spacing 16
        textbutton "결론을 말한다" style "r13_action_button" xsize 320 ysize 60 text_size r13_read_size(23,27):
            action Return(("conclude",)) sensitive ready and r13_debate_ready(claim)
        textbutton "반론을 그만둔다" style "r13_action_button" xsize 260 ysize 60 text_size r13_read_size(21,25):
            action Return(("leave",)) sensitive ready
    if not r13_debate_ready(claim):
        text "강조된 말을 모두 반박하면 결론을 말할 수 있다. 틀려도 다시 낼 수 있다. 그만두면 이 회의에서는 다시 다룰 수 없다." xpos 640 ypos 646 xsize 600 size r13_read_size(18,21) color "#b7ccd0"
    key "game_menu" action Return(("leave",))
