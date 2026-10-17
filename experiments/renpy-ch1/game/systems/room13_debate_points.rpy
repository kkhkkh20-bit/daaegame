# 0.18.91 A안 · 증거로만 싸우는 회의 (소유자 2026-10-17)
# - pair: 자료 둘을 엮어야 깨지는 발언. 하나만 내밀면 상대가 되받는다(반쯤 무너짐).
#   두 자료는 같은 장면에서 함께 얻는 것만 고른다. 그래야 회의에 필요한 장면 수가 늘지 않는다.
# - point: 결론은 문장 고르기 대신 "범인 지목 → 결정적 증거". 틀린 사람은 over, 틀린 증거는 weak와 같다.
#   ②(다람이 할아버지를 말할지 고르는 이야기)와 ⑤A(설득 회의)는 문장 결론을 그대로 둔다.
init 167 python:
    def _r13_dp_statement(claim,sid):
        return next(st for st in R13_DEBATE[claim]["statements"] if st["id"]==sid)

    # ④ 할머니 "주방엔 아무도 없었다" ← 부리 자국(N09) + 내려진 레버(N07): 9일 아침 통로에서 함께 얻는다.
    _st=_r13_dp_statement("Q4","s3")
    _st["accept"]=["N09","N07"]
    _st["pair"]=dict(keys=["N09","N07"],
        half={"N09":[("dad","따닥 씨는 판자 문 옆 벽을 부리로 오래 쪼았습니다. 그 벽 너머가 주방입니다."),
                ("granny","두드렸다 해도, 그 소리를 누가 들었다는 거예요? 주방엔 아무도 없었어요.")],
              "N07":[("dad","9일 아침, 주방 레버가 내려져 있었습니다."),
                ("granny","레버야 누가 지나가다 건드렸겠지요. 안에서 두드렸으면 누구라도 열어 줬을 거예요.")]},
        broken=[("dad","레버는 주방에서만 내립니다. 그리고 그 레버 바로 옆 벽을, 따닥 씨는 날개도 못 편 채 부리로 오래 두드렸습니다.")]+list(_st["broken_by"]["N09"]))

    # ⑤ 선생님 "아이들과 같은 냄비에서 먹었다" ← 아이 그릇만(Y11) + 새미의 말(Y13): 대피소에서 함께 얻는다.
    _st=_r13_dp_statement("Q5","s3")
    _st["accept"]=["Y11","Y13"]
    _st["pair"]=dict(keys=["Y11","Y13"],
        half={"Y11":[("dad","큰 냄비를 먹은 어른은 모두 멀쩡합니다. 아픈 건 아이 냄비를 먹은 아이들뿐입니다."),
                ("resident_teacher","그러니까요. 저도 그 아이 냄비에서 같이 먹었다니까요.")],
              "Y13":[("kid_saemi","쓴맛이 나서 반만 먹고 남겼어요."),
                ("resident_teacher","아이 하나가 남겼다고, 제가 안 먹었다는 뜻은 아니지요.")]},
        broken=list(_st["broken_by"]["Y13"])+[("dad","아이 냄비만 아이들을 재웠습니다. 그 냄비에서 먹지 않은 어른은 선생님 한 분입니다.")])

    # ⑤A 선생님 "다시 식겠지요. 왜 아무도 몰랐습니까" ← 실험 기록(Y07) + 벽의 옛 편지(Y08): 옛 시설에서 함께 얻는다.
    # 앞 물음(다시 식는다)은 Y07이, 뒤 물음(왜 몰랐나)은 Y08이 답한다. 둘 다 있어야 선생님이 말을 잃는다.
    _st=_r13_dp_statement("Q5A","s2")
    _st["pair"]=dict(keys=["Y07","Y08"],
        half={"Y07":[("dad","조각을 모아 둔 뒤로 지금까지 지켜봤습니다. 한 번도 식지 않았어요."),
                ("resident_teacher","잠깐이야 그럴 수 있지요. 그런 방법이 있었다면 왜 지금까지 아무도 몰랐습니까.")],
              "Y08":[("dad","옛 시설 벽에 이렇게 적혀 있었습니다. '나눠서 데웠다.'"),
                ("resident_teacher","옛날 얘기지요. 지금 그 돌이 식지 않고 버틴다는 걸 누가 봤습니까.")]},
        broken=[("dad","모아 둔 뒤로 지켜봤고, 식지 않았습니다. 옛사람들도 사람을 바치지 않고 나눠서 데웠습니다. 모르게 된 것뿐입니다."),
            ("resident_teacher","…….")])
    _st["hint"]="모아 두고 지켜본 것과, 옛사람들이 남긴 말."

    # ---- 결론: 지목 + 결정적 증거 ----
    R13_DEBATE["Q1"]["conclusion"]["point"]=dict(prompt="3번 등을 다시 열어 조각을 가져간 사람은?",
        candidates=["resident_tok","resident_seori","resident_madam","resident_siluk"],who="resident_siluk",
        keys=["L07","L08"],ask="그 사람이 등을 열었다는 증거는—.",
        decisive={"L07":[("dad","뚜껑에 남은 노끈과 실룩 씨 짐 끈은 끝이 뜯긴 자리가 똑같습니다.")],
                  "L08":[("dad","그날 밤 늦게, 손이 꽁꽁 언 채 들어왔다고 실룩 씨 아이가 말했습니다.")]},
        wrong_who={"resident_tok":("resident_tok","내가 연 등이면 조각을 왜 남의 창고에 팔겠어요."),
                   "resident_seori":R13_DEBATE["Q1"]["conclusion"]["weak"],
                   "resident_madam":("resident_madam","저는 산 것뿐이에요. 등을 연 손은 제 손이 아니에요.")},
        wrong_key=("resident_siluk","그게 내가 등을 열었다는 증거요?"))
    R13_DEBATE["Q3"]["conclusion"]["point"]=dict(prompt="창고 문 앞에 등유를 부은 사람은?",
        candidates=["resident_bori","nabi","neoul","resident_nubi"],who="resident_nubi",
        keys=["F11","F10","F12"],ask="그 사람이 그 밤 불을 냈다는 증거는—.",
        decisive={"F11":[("dad","누비 씨 큰아이가 말했습니다. 엄마가 그 밤 늦게 빨래터 기름 냄새를 묻히고 와서, 손을 계속 씻었다고.")],
                  "F10":[("dad","누비 씨 손등의 새 물집. 솥에 데면 손바닥이나 팔입니다. 손등은 불을 붙이다 덴 자리입니다.")],
                  "F12":[("dad","누비 씨가 직접 말했습니다. 불만 내려고 했다고.")]},
        wrong_who={"resident_bori":R13_DEBATE["Q3"]["conclusion"]["weak"],
                   "nabi":("nabi","제 등잔은 뚜껑이 닫힌 채 나왔어요."),
                   "neoul":("neoul","내가 불을 놓을 까닭이 어디 있소.")},
        wrong_key=("resident_nubi","……그게 제가 불을 냈다는 뜻이에요?"))
    R13_DEBATE["Q4"]["conclusion"]["point"]=dict(prompt="안에 따닥이 있는 걸 알고 통로 문을 닫은 사람은?",
        candidates=["resident_tosil","nabi","resident_ppul","granny"],who="granny",
        keys=["N03"],ask="그 새벽 안에 사람이 있다는 걸 미리 안 사람은—.",
        decisive={"N03":[("dad","따닥 씨가 전날 말했습니다. '내일 새벽에 통로를 잰다. 할머니께도 말씀드렸다.'")]},
        wrong_who={"resident_tosil":R13_DEBATE["Q4"]["conclusion"]["over"],
                   "nabi":("nabi","저는 새벽에 빨래터로 먼저 보내졌어요. 할머니가 보내셨어요."),
                   "resident_ppul":("resident_ppul","나는 그 새벽 회관에 있었소.")},
        wrong_key=("granny","그게 내가 문을 닫았다는 뜻이에요?"))
    R13_DEBATE["Q5"]["conclusion"]["point"]=dict(prompt="아이 냄비에 약을 넣은 사람은?",
        candidates=["resident_bori","resident_seori","resident_madam","resident_teacher"],who="resident_teacher",
        keys=["Y13","Y12"],ask="그 사람이 약을 넣었다는 증거는—.",
        decisive={"Y13":[("dad","아이들은 하얀 그릇, 선생님만 빨간 그릇. 그 안엔 큰 냄비 건더기였습니다. 선생님은 아이 냄비를 먹지 않았습니다.")],
                  "Y12":[("dad","잠드는 약이 사라진 날, 아이 기침약을 찾으러 진료소에 온 사람은 선생님입니다.")]},
        wrong_who={"resident_seori":R13_DEBATE["Q5"]["conclusion"]["weak"],
                   "resident_bori":("resident_bori","내 아들도 그 냄비를 먹었어!"),
                   "resident_madam":("resident_madam","저는 진료소 근처에도 안 갔어요.")},
        wrong_key=("resident_teacher","……그걸로 제가 넣었다는 건가요?"))
    R13_DEBATE["Q6"]["conclusion"]["point"]=dict(prompt="수레 명령서를 실제로 쓴 손은?",
        candidates=["resident_ppul","neoul","resident_badook","granny"],who="granny",
        keys=["V06"],ask="그 손이 누구 것인지 보여 주는 증거는—.",
        decisive={"V06":[("dad","도장은 촌장님 것입니다. 하지만 'ㄹ'의 꼬리가 둥글게 말렸습니다. 우리 가족을 이 마을로 부른 가짜 편지와 같은 손입니다.")]},
        wrong_who={"resident_ppul":R13_DEBATE["Q6"]["conclusion"]["over"],
                   "neoul":("neoul","나는 받은 명령을 옮겼을 뿐이오."),
                   "resident_badook":("resident_badook","저는 그 명령서를 오늘 처음 봤습니다.")},
        wrong_key=("resident_ppul","그게 내가 쓰지 않았다는 증거요?"))

    # ---- 흔들기: 되물으면 숨긴 한 줄이 나온다. 두 사람이 맞붙는 자리도 여기서 연다. 이미 있는 press는 두고 없을 때만. ----
    for _claim,_sid,_lines in (
        ("Q1","s3",[("resident_madam","판 사람이요? 얼굴은 못 봤어요. 해 질 녘에 왔고, 허리에 노끈을 감고 있더군요."),
            ("resident_siluk","……"),
            ("dad","(허리에 노끈. 그 노끈이 등 뚜껑의 노끈과 같은지 보면 된다.)",{"thought":True})]),
        ("Q3","s2",[("nabi","제 등잔은 뚜껑을 덮으면 꺼져요. 꼬미한테 꼭 덮으라고 했어요……. 꼬미가 안 덮었으면 제 탓이에요."),
            ("dad","(그 등잔이 어떤 모습으로 나왔는지부터 보자.)",{"thought":True})]),
        ("Q4","s2",[("granny","새벽 주방엔 늘 토실이가 불을 넣어요. 그 어린 손이 레버에 닿았을지도 모르지요."),
            ("resident_tosil","(작게) ……나, 그날은……"),
            ("granny","토실아, 어른들 얘기란다."),
            ("dad","(토실이가 무언가 말하려다 멈췄다. 할머니는 그날 토실이가 주방에 왔는지 묻지 않았다. 이미 알고 있는 것처럼.)",{"thought":True})]),
        ("Q5","s1",[("resident_bori","감자가 아니면 뭐요! 애들이 저렇게 됐는데!"),
            ("resident_madam","어른들도 같은 감자를 먹었어요. 저도 먹었고요."),
            ("dad","(같은 감자. 그런데 아픈 건 아이들뿐이다. 냄비를 나눠 보자.)",{"thought":True})]),
    ):
        _st=_r13_dp_statement(_claim,_sid)
        if not _st.get("press"):_st["press"]=_lines
