# 0.19.17 단서 줄기 · g3_lamps (등·수리점·진료소 줄기: 초롱, 톡, 우박, 서리, 피코, 따닥, 사서, 모모, 슬링, 바둑이)
#   틀: systems/room13_threads.rpy (steps / variants / again / recap / timeless, R13_REACTIONS).
#   원칙: 이야기가 지나가 전제가 틀린 질문만 steps로 감춘다. 여전히 물을 수 있는 질문은 timeless로 두고
#   variants(첫 대사)와 again(다시 묻기)으로 지금 시점에 맞춘다. 결론은 대신 말하지 않는다.
#   조건 함수는 저장에 담기지 않도록 이름 있는 함수로 쓴다(람다 금지).
#   라벨로 도는 주제(ep1:ubak, ep1:librarian, seal_look, w2_expose_numbers, tok_after_doubt, grudge_fix:*)는
#   variants/again이 쓰이지 않는다. steps만 붙인다.
init 184 python:
    # ---- 조건 함수 ----
    def _g3_day(s):
        return s.get("day",1)

    def _g3_known(s):
        return set(s.get("flags",[]))|set(s.get("evidence",[]))|set(s.get("read_topics",[]))

    def _g3_child_away(s):
        return s.get("daram_state") not in ("with_dad","rescued")

    def _g3_after_case_day(s):
        return _g3_day(s)>R13_CASE_DAY

    def _g3_before_case_day(s):
        return _g3_day(s)<R13_CASE_DAY

    def _g3_from_case_day(s):
        return _g3_day(s)>=R13_CASE_DAY

    def _g3_mk(s):
        return r13_mother_knowledge(s)

    def _g3_mom_received(s):
        return _g3_mk(s)["received"]

    def _g3_mom_promised_open(s):
        k=_g3_mk(s)
        return k["promised"] and not k["received"]

    def _g3_mom_promised_early(s):
        return _g3_mom_promised_open(s) and _g3_day(s)<3

    def _g3_mom_promised_due(s):
        return _g3_mom_promised_open(s) and _g3_day(s)>=3

    def _g3_mom_recognized(s):
        k=_g3_mk(s)
        return k["recognized"] or k["promised"] or k["received"]

    def _g3_ask_mom_lamp_open(s):
        # 이름으로 묻는 질문은 초롱이 엄마를 알아보기 전까지만 뜻이 있다.
        return not _g3_mom_recognized(s)

    def _g3_testify_open(s):
        # 재판이 있는 판(13호 사건이 일어남)에서, 재판이 끝나기 전에만.
        return s.get("case_state")=="occurred" and not s.get("trial_result")

    def _g3_lt_dawn_open(s):
        k=_g3_known(s)
        return "lt_dawn" in k and "lt_done" not in k

    def _g3_before_dawn(s):
        return _g3_day(s)<3 and "lt_dawn" not in _g3_known(s)

    def _g3_lt_solved(s):
        return "lt_solved" in _g3_known(s)

    def _g3_sling_working(s):
        k=_g3_known(s)
        return "sling_hostile" not in k or "sling_reconciled" in k

    def _g3_sling_cold(s):
        return not _g3_sling_working(s)

    # ---- 적용 도구 ----
    def _g3_set(key,**spec):
        if key in ROOM13["topics"]:
            ROOM13["topics"][key].update(spec)

    def _g3_thought(text):
        return ("dad",text,{"thought":True})

    # =================================================================
    # 초롱 (resident_lamplighter)
    # =================================================================
    _g3_set("lamplighter_guarded",timeless=True,
        variants=[
            (_g3_lt_solved,[("dad","등에 문제가 있습니까?"),
                ("resident_lamplighter","3번 등엔 조각을 다시 넣었어요. 그런데 가을만큼 오래 데워지지 않아요."),
                ("dad","조각을 되찾았는데도 그렇습니까?"),
                ("resident_lamplighter","네. 조각 탓인지 다른 탓인지는 저도 아직 몰라요. 계속 흔들리는지 지켜보는 중이에요.")]),
            (_g3_lt_dawn_open,[("dad","등에 문제가 있습니까?"),
                ("resident_lamplighter","광장 3번 등이 꺼졌어요. 새벽에 제가 돌 때만 해도 미지근했는데요."),
                ("dad","연결선이 끊어진 겁니까?"),
                ("resident_lamplighter","아니요. 안에 있어야 할 조각이 없어졌대요. 누가 언제 열었는지는 저도 못 봤어요.")]),
            (_g3_child_away,[("dad","등에 문제가 있습니까?"),
                ("resident_lamplighter","위험하니 조금 떨어져서 보세요. 등불 안의 【연결선】이 끊어졌는지 살펴보는 중이에요."),
                ("dad","연결선이 끊어졌으면 고장 난 겁니까?"),
                ("resident_lamplighter","고장이라고 말하면 당장 제가 고쳐야 하거든요. 아직은 지켜보는 중이에요.")]),
        ],
        again=[
            (_g3_lt_solved,[("resident_lamplighter","3번 등은 다시 켜졌어요. 다만 금방 식어서 자주 들여다봐요.")]),
            ({"has":["lt_dawn"]},[("resident_lamplighter","3번 등은 조각이 없어서 꺼진 거였어요. 연결선 탓은 아니었어요.")]),
            (None,[("resident_lamplighter","아직 지켜보는 중이에요. 흔들림이 심해지면 그때 고칠 거예요.")]),
        ])

    _g3_set("life:resident_lamplighter:work",
        variants=[
            ({"has":["lt_dawn"]},[("dad","등불 밝기가 고르지 않군요."),
                ("resident_lamplighter","집마다 돌의 힘을 끌어 쓰는 양이 달라서요. 불이 세다고 다 좋은 건 아닙니다."),
                ("dad","그럼 무엇을 봐야 합니까?"),
                ("resident_lamplighter","계속 【흔들리는지】를 보세요. 한 번 켜졌다고 돌아서면, 다음에 꺼지는 걸 놓치거든요."),
                ("resident_lamplighter","……3번 등이 그랬어요. 미지근한 것만 보고 다음 등으로 갔으니까요.")]),
        ],
        again=[(None,[("resident_lamplighter","켜졌는지보다 계속 흔들리는지를 봐요. 그게 제 일이에요.")])])

    _g3_set("life:resident_lamplighter:after",
        variants=[
            ({"has":["nt_chorong_half"]},[("resident_lamplighter","이마는 괜찮아요. 편지를 지키지 못한 게 더 아파요."),
                ("dad","빼앗긴 편지는 초롱 씨 탓이 아닙니다."),
                ("resident_lamplighter","그래도 그분 글씨였어요. 어머니께도 아직 말을 못 했어요.")]),
            ({"has":["nt_chorong_safe"]},[("resident_lamplighter","그날 밤 길에서 기다린 사람들이 아직 눈앞에 있어요."),
                ("dad","혼자 다니지 않으시는 게 좋겠습니다."),
                ("resident_lamplighter","네. 바둑이 씨가 같이 돌아 줘요. 어머니께는 아직 말씀 못 드렸지만요.")]),
        ],
        again=[
            ({"has":["nt_chorong_half"]},[("resident_lamplighter","다친 데는 나아요. 편지 일은 아직 마음에 걸려요.")]),
            (None,[("resident_lamplighter","어머니께 드릴 말은 아직 다 못 했어요. 불 켜는 일보다 어렵네요.")]),
        ])

    _g3_set("life:resident_lamplighter:crisis",
        again=[(None,[("resident_lamplighter","주소는 지금도 못 드려요. 연락을 맡긴 분이 위험해지니까요.")])])

    _g3_set("smalltalk:lamplighter_check",timeless=True,
        variants=[
            ({"has":["lt_dawn"]},[("dad","점검을 마치면 바로 자리를 옮기십니까?"),
                ("resident_lamplighter","네. 해 지고 한 바퀴, 새벽에 한 바퀴 돌아요."),
                ("resident_lamplighter","새벽에 도는 건 이제 다들 아시잖아요. 3번 등 일 때문에요.")]),
        ],
        again=[({"has":["lt_dawn"]},[("resident_lamplighter","저녁에 한 바퀴, 새벽에 한 바퀴예요. 그사이엔 집에 있어요.")])],
        recap="초롱은 해 진 뒤 한 바퀴만 돈다고 했다. 새벽에 북쪽 길에서 봤다는 말은 무엇일까?")

    _g3_set("cross:lamp_dawn",timeless=True,
        variants=[
            ({"has":["lt_dawn"]},[("dad","새벽에도 북쪽 길 등을 보신다고요?"),
                ("resident_lamplighter","……새벽에 도는 건 맞아요. 광장 등도 그때 봐요."),
                (None,"초롱은 대답하면서 장대를 다른 쪽 어깨로 옮겼다."),
                ("resident_lamplighter","북쪽 길 이야기는 순회할 때 해요. 길 한가운데서 말고요.")]),
        ],
        recap="초롱은 북쪽 길 이야기를 피했다. 새벽에 그 길에서 무엇을 하는 걸까?")

    _g3_set("ask_mom:lamplighter",steps=_g3_ask_mom_lamp_open,
        again=[(None,[("resident_lamplighter","이름만으로는 어느 분인지 모르겠어요. 얼굴이나 그분이 남긴 표시가 있으면 알아볼 수 있을 거예요.")])])

    _g3_set("intro:lamplighter_mother",timeless=True,
        variants=[
            ({"has":["J03"]},[("dad","아내를 마지막으로 어디에서 보셨습니까?"),
                ("resident_lamplighter","【여관 앞】에서요. 등을 손질하다가 잠깐 이야기를 나눴어요."),
                ("dad","무슨 이야기를 하셨습니까?"),
                ("resident_lamplighter","가족이 올지도 모른다고 걱정했어요. 아이한테는 【도토리】 모양을 그려 준다는 이야기도 했고요."),
                ("resident_lamplighter","그래서 메모를 보고 그분 가족인 줄 알았어요."),
                ("dad","그 뒤에 아내는 어디로 갔습니까?"),
                ("resident_lamplighter","【우체국】 쪽 길로 갔어요. 안으로 들어가는 것까지는 보지 못했어요."),
                ("dad","우체국에 들른 건 확인했습니다. 그다음에 어디로 갔는지가 남았군요.")]),
        ],
        again=[
            (_g3_mom_received,[("resident_lamplighter","여관 앞에서 뵌 게 제가 직접 본 마지막이에요. 그 뒤 소식은 맡아 둔 봉투가 전부였어요.")]),
            (None,[("resident_lamplighter","여관 앞에서 이야기하고, 우체국 쪽 길로 가시는 것까지 봤어요. 그다음은 저도 몰라요.")]),
        ])

    _g3_set("lamplighter_warning",timeless=True,
        variants=[
            (_g3_mom_received,[("dad","아내가 맡긴 편지가 있습니까?"),
                ("resident_lamplighter","제가 맡아 둔 건 점검함에서 가져가신 그 봉투예요."),
                ("resident_lamplighter","읽은 이야기는 여기서 하지 맙시다. 누가 들을지 몰라요.")]),
        ],
        again=[
            (_g3_mom_received,[("resident_lamplighter","봉투는 이미 가져가셨지요. 안에 적힌 이야기는 여기서 하지 맙시다.")]),
            (None,[("resident_lamplighter","등 밑 점검함에 그대로 있어요. 꺼내서 다른 곳에서 읽어 주세요.")]),
        ])

    _g3_set("item:lamp_oil",timeless=True,
        variants=[
            (_g3_mom_promised_early,[("dad","등잔 기름입니다. 밤마다 등을 돌보시니 기름이 모자라실 것 같아서요."),
                ("resident_lamplighter","……고맙습니다. 요즘은 기름도 아껴 써야 해서요."),
                ("resident_lamplighter","부인도 전에 이렇게 기름을 챙겨 주셨어요. 말씀드린 봉투는 약속한 날에 찾아 둘게요.")]),
            (_g3_mom_promised_due,[("dad","등잔 기름입니다. 밤마다 등을 돌보시니 기름이 모자라실 것 같아서요."),
                ("resident_lamplighter","……고맙습니다. 요즘은 기름도 아껴 써야 해서요."),
                ("resident_lamplighter","부인도 전에 이렇게 기름을 챙겨 주셨어요. 말씀드린 봉투 이야기는 따로 할게요.")]),
        ],
        recap="초롱에게 기름을 건넸다. 엄마도 초롱에게 기름을 챙겨 주었다고 했다.")

    _g3_set("warning_open_with",steps={"not":["E18"]},
        recap="초롱이 보는 앞에서 봉투를 열었다. 엄마는 왜 오라는 편지를 쓴 적 없다고 했을까?")

    _g3_set("ep4:st_chorong_after",timeless=True,
        again=[(None,[("resident_lamplighter","오늘 밤도 바둑이 씨랑 같이 돌아요. 편지는 여전히 제가 들고요.")])])

    _g3_set("w2_contact",steps={"not":["mom_reunited"]},
        again=[
            ({"has":["E19"]},[("resident_lamplighter","답은 전해 드렸지요. 표식만 보시고, 주소는 누구에게도 말하지 마세요.")]),
            (None,[("resident_lamplighter","말씀은 전했어요. 답이 오면 제가 직접 가져올게요. 장소는 묻지 마시고요.")]),
        ])

    _g3_set("w2_lamps",timeless=True,
        again=[(None,[("resident_lamplighter","경비는 아직도 제가 들른 등마다 따라와요. 만날 곳은 먼저 확인하고 정합시다.")])])

    # =================================================================
    # 톡 (resident_tok)
    # =================================================================
    _g3_set("ep1:tok_lamps",timeless=True,
        again=[
            (_g3_lt_solved,[("resident_tok","3번 등엔 '광장 3' 조각을 다시 넣었어요. 그래도 가을만큼 오래 데워지진 않네요.")]),
            ({"has":["lt_dawn","piko_dead"]},[("resident_tok","깜빡인다고 적어만 두고 먼저 열어 보지 못했어요. 그 밑에서 피코가……."),
                ("resident_tok","그래도 조각은 내가 안 뺐어요.")]),
            ({"has":["lt_dawn"]},[("resident_tok","깜빡인다고 적어만 두고 먼저 열어 보지 못했어요. 피코가 숨이 붙어 있어서 다행이에요."),
                ("resident_tok","그래도 조각은 내가 안 뺐어요.")]),
            (_g3_before_dawn,[("resident_tok","3번 등은 장부에 적어 뒀어요. 내일 들여다볼 거예요.")]),
        ],
        recap="톡의 장부에는 3번 등이 밤마다 깜빡인다고 적혀 있었다. 그 등은 왜 식었을까?")

    _g3_set("cross:tok_pin_job",timeless=True,
        again=[
            (_g3_before_case_day,[("resident_tok","핀은 목요일까지 맞춰 놓을게요. 맞는 부품이 없어서 덧대는 중이에요.")]),
            (None,[("resident_tok","그 핀은 목요일에 할머니께 달아 드렸어요. 그 뒤 일은 나도 몰라요.")]),
        ])

    _g3_set("smalltalk:tok_parts",timeless=True,
        again=[({"has":["tok_repair"]},[_g3_thought("(톡이 천으로 덮어 두던 작은 상자. 할머니 핀을 고치던 자리였을까?)")])],
        recap="톡은 천을 덮은 작은 상자를 슬쩍 밀어 두었다. 그 안에는 무엇이 있을까?")

    _g3_set("tok_repair",timeless=True,
        variants=[
            (_g3_child_away,[("resident_tok","잠깐, 손은 그쪽으로 뻗지 마세요. 방금 땜질한 금속이 아직 뜨거워요."),
                ("dad","무엇을 고치고 계십니까?"),
                ("resident_tok","할머니 목도리 핀이에요. 오늘 새것으로 바꿔 드렸어요. 억지로 잡아당기지만 않으면 안 빠져요."),
                ("dad","핀의 연결 부위 모양이 꽤 특이하군요."),
                ("resident_tok","딱 맞는 부품이 없어서 덧댔어요. 그래서 납품 기록은 따로 남겨 둬야죠.")]),
        ],
        again=[
            (_g3_after_case_day,[("resident_tok","그 핀은 목요일에 할머니 목도리에 달아 드린 거예요. 덧댄 이음이라 보면 알아요.")]),
            (None,[("resident_tok","땜질한 데는 식으면 단단해져요. 억지로 잡아당기지만 않으면요.")]),
        ])

    _g3_set("tok_pin",timeless=True,
        again=[(None,[("resident_tok","같은 이음이에요. 할머니가 달고 가신 뒤에 누가 뭘 했는지는 나도 몰라요.")])])

    _g3_set("tok_testify",steps=_g3_testify_open,
        again=[(None,[("resident_tok","재판에서 그대로 말할게요. 내가 만든 이음이라는 것, 그리고 그 뒤는 모른다는 것까지요.")])])

    _g3_set("tok_after_doubt",steps={"not":["tok_after_doubt"]})

    _g3_set("item:file",steps=_g3_from_case_day,
        recap="톡에게 줄칼을 건네고 새 핀의 수리 쪽지를 받았다.")

    _g3_set("alibi:case:resident_tok",steps={"case":"occurred"},
        again=[(None,[("resident_tok","식당 구석에서 계측기를 보고 있었어요. 할머니는 비명 날 때까진 식당에 계셨고요.")])])

    _g3_set("life:resident_tok:work",
        again=[(None,[("resident_tok","비슷해 보여도 달라요. 맞대 볼 나머지 한쪽이 있어야 같다고 하죠.")])])
    _g3_set("life:resident_tok:after",
        again=[(None,[("resident_tok","안 맞는 부품은 오늘도 안 맞아요. 딸깍 소리만으로 고쳤다고는 안 해요.")])])
    _g3_set("life:resident_tok:crisis",
        again=[(None,[("resident_tok","끼우는 것보다 확인이 오래 걸려요. 조금만 기다려 주세요.")])])

    # =================================================================
    # 우박 (resident_ubak) · 아빠는 반말
    # =================================================================
    _g3_set("ep1:ubak",steps={"not":["lt_done"]})

    _g3_set("alibi:case:resident_ubak",steps={"case":"occurred"},
        again=[(None,[("resident_ubak","진료소를 지키고 있었어요. 스승님만 먼저 뛰어가셨고요.")])])

    _g3_set("life:resident_ubak:work",
        again=[(None,[("resident_ubak","어떤 조건에서 쟀는지 같이 적어야 해요. 숫자만 있으면 맞는지도 몰라요.")])])
    _g3_set("life:resident_ubak:after",
        again=[(None,[("resident_ubak","다시 재고 있어요. 이번엔 잴 때 켜 둔 등도 같이 적었어요.")])])
    _g3_set("life:resident_ubak:crisis",
        again=[(None,[("resident_ubak","다르게 나온 숫자도 지우지 않고 남겨 뒀어요. 그대로 보여 드릴게요.")])])
    _g3_set("life:resident_ubak:measurement",
        recap="같은 조건에서, 옮기기 전과 후에 남은 힘과 버틴 시간을 비교해야 한다.")

    # =================================================================
    # 서리 (resident_seori)
    # =================================================================
    _g3_set("seori_case",steps={"case":"occurred"},
        variants=[
            ({"has":["H15"]},[("resident_seori","처음에는 불부터 끄고 사람을 옮겼습니다. 그 종이는 그때 사망을 확인하고, 눈에 보이는 상처만 적어 둔 것입니다."),
                ("dad","봉해 둔 촛대는 검사원님 앞에서 이미 봤습니다."),
                ("resident_seori","그렇지요. 장식 고리에 끼인 조각을 본 것까지는 함께 적었습니다. 상처 기록과 맞춰 보는 일은 아직 남았습니다.")]),
        ],
        again=[
            ({"has":["H15"]},[("resident_seori","고리 조각을 본 것까지 적어 두었습니다. 상처 기록과 맞춰 볼 일이 남았습니다.")]),
            (None,[("resident_seori","그날 종이는 사망과 눈에 보이는 상처만 적은 겁니다. 촛대는 봉한 채 두었습니다.")]),
        ])

    _g3_set("seori_previous",steps={"case":"occurred"},
        again=[(None,[("resident_seori","회신에는 혼자 두지 말라고만 썼습니다. 아이와 함께 두어도 된다는 말은 없습니다.")])])

    _g3_set("seal_look",steps={"case":"occurred"})
    _g3_set("w2_expose_numbers",steps={"not":["forgery_exposed"]})

    _g3_set("w2_doctor",timeless=True,
        again=[(None,[("resident_seori","돌아오는 환자는 지금도 있습니다. 누가 그 줄을 지웠는지도 기록에서 감추지 않겠습니다.")])])

    _g3_set("item:herbs",timeless=True,
        recap="서리와 함께 열이 내린 환자를 지켜봤다. 환자는 가족의 이름을 불렀다.")

    _g3_set("life:resident_seori:work",
        again=[(None,[("resident_seori","다시 확인할 수 있게 이름을 남깁니다. 책임도 함께 남고요.")])])
    _g3_set("life:resident_seori:after",
        again=[(None,[("resident_seori","제 서명이 있는 줄도 가리지 않겠습니다. 보셔도 됩니다.")])])
    _g3_set("life:resident_seori:crisis",
        again=[(None,[("resident_seori","원본은 남겨 둡니다. 하기 싫은 날에도요.")])])

    # =================================================================
    # 피코 (resident_piko)
    # =================================================================
    _g3_set("ep1:st_piko_faces",timeless=True,
        again=[({"has":["piko_survived"]},[("resident_piko","이제는 얼굴만 그리지 않아요. 이름도 같이 적어 둬요.")])],
        recap="피코는 등 밑에서 자는 사람들 얼굴을 지키고 있다. 피코 자신은 누가 지켜 줄까?")

    _g3_set("ep1:st_piko_after",timeless=True,
        variants=[
            ({"has":["chorong_dead"]},[("resident_piko","손가락이 아직 좀 굳었어요. 그래도 붓은 쥐어져요."),
                ("resident_piko","이제 등 밑에서 안 자요. 겨울 동안 쉴 자리를 얻었어요."),
                ("resident_piko","등 밑에서 자는 사람들 얼굴은 이름이랑 같이 그려 둬요. 등지기 아저씨가 맡아 주던 판자는 이제 제가 들고 다녀요."),
                ("resident_piko","쓰러져 보니까 알겠더라고요. 얼굴만 남기면 안 돼요. 누가 찾아와 줘야 해요.")]),
        ],
        again=[(None,[("resident_piko","붓은 쥐어져요. 오늘도 한 사람 그렸어요. 이름까지요.")])])

    _g3_set("smalltalk:piko_cloth",timeless=True,
        again=[(None,[("resident_piko","천은 아직 덮어 둘게요. 다 그리면 제가 먼저 걷을게요.")])])

    _g3_set("grudge_cold:piko",steps={"not":["piko_reconciled"]},
        recap="피코는 모모 관장에게 일러바친 일을 아직 잊지 않았다. 그날 받은 사례금은 누구의 몫이었을까?")
    _g3_set("grudge_fix:piko",steps={"not":["piko_reconciled"]})

    _g3_set("life:resident_piko:work",
        again=[(None,[("resident_piko","그림 속 본인이 먼저 봐야 해요. 이름도 지우지 않을 거고요.")])])
    _g3_set("life:resident_piko:after",
        again=[(None,[("resident_piko","색은 천천히 고르고 있어요. 제 얼굴 말고 그림을 봐 주세요.")])])
    _g3_set("life:resident_piko:crisis",
        again=[(None,[("resident_piko","지금 마음에 드는 색으로 할게요. 고를 때까지만 기다려 주세요.")])])

    # =================================================================
    # 따닥 (resident_ttadak)
    # =================================================================
    _g3_set("ep4:st_ttadak_boards",timeless=True,
        again=[
            ({"has":["nt_ttadak_half"]},[("resident_ttadak","손이 펴지면 천막에 판자를 마저 댈 거예요. 판자는 이미 다 잘라 놨어요.")]),
            ({"has":["st_ttadak_after"]},[("resident_ttadak","천막엔 판자를 다 댔어요. 남은 판자는 또 다른 집으로 가요.")]),
            (None,[("resident_ttadak","판자는 오늘도 반 치씩 길게 잘라 둬요. 모자라는 것보다 남는 게 나으니까요.")]),
        ])

    _g3_set("ep4:st_ttadak_after",timeless=True,
        again=[(None,[("resident_ttadak","판자 문 안쪽 손잡이는 오늘도 돌려 봤어요. 안에서도 잘 열려요.")])])

    _g3_set("smalltalk:ttadak_plan",timeless=True,
        again=[(None,[("resident_ttadak","도면이랑 고친 자리를 같이 들고 오세요. 그래야 안 뜯고도 알아요.")])])
    _g3_set("smalltalk:ttadak_wood",timeless=True,
        again=[(None,[("resident_ttadak","판은 들어갈 자리에 먼저 대 봐요. 대 보기 전엔 다 됐다고 못 해요.")])])

    _g3_set("grudge_cold:ttadak",steps={"not":["ttadak_reconciled"]},
        recap="따닥은 벽 일을 신고한 사례금을 아직 묻고 있다. 그 돈은 받을 일이었을까?")
    _g3_set("grudge_fix:ttadak",steps={"not":["ttadak_reconciled"]})

    _g3_set("life:resident_ttadak:work",
        again=[(None,[("resident_ttadak","재기 전에 도면부터요. 괜히 뜯으면 다 제 탓이 돼요.")])])
    _g3_set("life:resident_ttadak:after",
        variants=[
            ({"has":["nt_ttadak_half"]},[("resident_ttadak","손이 아직 안 펴져요. 망치를 못 쥐니까 지붕 걱정만 늘어요."),
                ("dad","고칠 자리는 제가 대신 적어 두겠습니다."),
                ("resident_ttadak","치수로 적어 주세요. 손이 펴지면 그 치수대로 바로 박을게요.")]),
        ],
        again=[
            ({"has":["nt_ttadak_half"]},[("resident_ttadak","손은 조금씩 펴져요. 치수 적어 둔 건 잘 갖고 있어요.")]),
            (None,[("resident_ttadak","칭찬 말고 치수로 적어 주세요. 그래야 못을 박죠.")]),
        ])
    _g3_set("life:resident_ttadak:crisis",
        again=[(None,[("resident_ttadak","무너질 데부터 봐요. 조용한 집도 빼먹지 않고요.")])])

    # =================================================================
    # 사서 선생님 (resident_librarian)
    # =================================================================
    _g3_set("ep1:librarian",steps={"not":["lt_done"]})

    _g3_set("ep1:st_lib_after",timeless=True,
        again=[(None,[("resident_librarian","베끼는 일은 아직 끝나지 않았어요. 그래도 한 벌씩 늘고 있어요.")])])

    _g3_set("librarian_stone",timeless=True,
        again=[(None,[("resident_librarian","장부는 여기 그대로 있어요. 네 해 전부터 늘어난 이름 줄도요.")])])
    _g3_set("librarian_copy",timeless=True,
        again=[(None,[("resident_librarian","베낀 장부도 숫자는 원본 그대로예요. 필요하면 언제든 다시 펼쳐 드릴게요.")])])

    _g3_set("life:resident_librarian:work",
        again=[(None,[("resident_librarian","여기서 펼쳐 보는 건 돼요. 베낄 때 빠뜨린 줄은 표시해 두시고요.")])])
    _g3_set("life:resident_librarian:after",
        again=[(None,[("resident_librarian","포장지는 드릴게요. 이름이 적힌 서류는 태우지 않아요.")])])
    _g3_set("life:resident_librarian:crisis",
        again=[(None,[("resident_librarian","원본과 베낀 것은 따로 둘 곳을 찾고 있어요. 한꺼번에 잃으면 안 되니까요.")])])
    _g3_set("life:resident_librarian:dated",
        recap="기록은 날짜가 끊기지 않아야 하고, 날짜마다 누가 확인했는지 남아야 한다.")

    # =================================================================
    # 모모 관장 (resident_momo)
    # =================================================================
    _g3_set("ep6:st_momo_glasses",timeless=True,
        again=[(None,[("resident_momo","동생 숄은 오늘도 여기 있어요. 물어봐 주셔서 고마워요.")])])

    _g3_set("life:resident_momo:work",
        again=[(None,[("resident_momo","쓰는 법을 잊으면 다 장식이 돼요. 그래도 버리지는 않아요.")])])
    _g3_set("life:resident_momo:after",
        again=[(None,[("resident_momo","여기 앉아서 보시는 건 언제든 좋아요. 가져가시는 건 안 되고요.")])])
    _g3_set("life:resident_momo:crisis",
        again=[(None,[("resident_momo","그림만 믿고 장치를 켜지는 마세요. 저도 자꾸 예쁜 쪽부터 보네요.")])])

    # =================================================================
    # 슬링 (resident_sling)
    # =================================================================
    _g3_set("ask_mom:sling",steps={"not":["J08"]},
        again=[(None,[("resident_sling","이름만으로는 어려워요. 얼굴을 보면 기억날지도 모르겠어요.")])])

    _g3_set("grudge_cold:sling",steps={"not":["sling_reconciled"]},
        recap="슬링은 우체국에 나가지 못하게 됐다. 슬링에게 편지를 열게 시킨 사람은 따로 있지 않았을까?")
    _g3_set("grudge_fix:sling",steps={"not":["sling_reconciled"]})

    _g3_set("life:resident_sling:work",
        again=[(None,[("resident_sling","받을 사람이 없으면 보낸 곳으로 돌려놔요. 누구에게 전할지는 쓴 사람이 정하니까요.")])])
    _g3_set("life:resident_sling:after",steps=_g3_sling_working,
        again=[(None,[("resident_sling","못 전한 편지는 받는 쪽이 문을 닫았다고 적어 둬요. 핑계라고 해도요.")])])
    _g3_set("life:resident_sling:crisis",steps=_g3_sling_working,
        again=[(None,[("resident_sling","봉투 여는 일만 아니면 도와드릴게요. 못 전한 이유는 제가 전해요.")])])

    # =================================================================
    # 바둑이 (resident_badook)
    # =================================================================
    _g3_set("life:resident_badook:work",
        again=[(None,[("resident_badook","밤 순찰은 둘씩이에요. 찾으러 갈 때도 둘이 갑니다.")])])
    _g3_set("life:resident_badook:after",
        again=[(None,[("resident_badook","삐익! 명령은 이름이 적힌 글로 확인합니다. 지금도요.")])])
    _g3_set("life:resident_badook:crisis",
        again=[(None,[("resident_badook","불 꺼진 집도 다시 두드려 봐요. 빈집인 줄 알았다는 말은 나중에 못 하니까요.")])])

    # =================================================================
    # 증거 반응 (그 인물이 일반 답만 하던 조합)
    # =================================================================
    def _g3_react(person,key,rows):
        R13_REACTIONS[(person,key)]=rows

    _g3_react("resident_badook","W1",[(None,[
        ("resident_badook","제가 드린 말 그대로예요. 검사받고 북쪽 보호소로 간 사람이 돌아오는 건 못 봤습니다."),
        ("resident_badook","보호소 안에서 무슨 일이 있는지는 저도 몰라요. 안에 들어가 본 적이 없어서요.")])])

    # 초롱
    _g3_react("resident_lamplighter","E18",[
        ({"has":["J18"]},[("resident_lamplighter","같이 연 그 봉투예요. 봉인이 온전했던 것까지는 제가 확인해 드릴 수 있어요."),
            ("resident_lamplighter","안에 적힌 말은 부인과 아버님 사이의 일이에요. 제가 보탤 말은 없어요.")]),
        (None,[("resident_lamplighter","제가 점검함에 맡아 둔 봉투가 맞아요."),
            ("resident_lamplighter","부인께 받은 건 맞지만, 지금 어디 계신지는 저도 몰라요.")]),
    ])
    _g3_react("resident_lamplighter","E19",[
        ({"has":["mom_reunited"]},[("resident_lamplighter","이제 직접 만나셨으니 그 답장은 아버님이 간직하세요."),
            ("resident_lamplighter","그래도 표식 이야기는 남들 앞에서 하지 맙시다.")]),
        (None,[("resident_lamplighter","제가 가져다 드린 답장이에요. 예전 은신처 말고 지금 신호를 보라는 말까지는 저도 들었어요."),
            ("resident_lamplighter","주소는 저도 몰라요. 표식을 보러 가실 때 뒤에 누가 따라오는지만 꼭 살피세요.")]),
    ])
    _g3_react("resident_lamplighter","J02",[
        ({"has":["J03"]},[("resident_lamplighter","제가 말씀드린 그대로예요. 우체국에 들르신 건 확인하셨군요."),
            ("resident_lamplighter","그 뒤로 어디 가셨는지는 저도 못 봤어요.")]),
        (None,[("resident_lamplighter","제가 말씀드린 그대로예요. 여관 앞에서 이야기하고, 부인은 우체국 쪽 길로 가셨어요."),
            ("resident_lamplighter","안으로 들어가셨는지는 제가 보지 못했어요.")]),
    ])
    _g3_mail_rows=[
        (_g3_mom_received,[("resident_lamplighter","부인께 봉투를 받은 건 맞아요. 그 봉투는 이미 아버님 손에 있지요."),
            ("resident_lamplighter","제가 맡은 일은 거기까지였어요.")]),
        (_g3_mom_promised_open,[("resident_lamplighter","그 봉투를 제가 맡고 있어요. 말씀드린 대로 꺼내 드릴게요."),
            ("resident_lamplighter","안에 무엇이 적혔는지는 저도 몰라요. 열어 보지 않았으니까요.")]),
        (None,[("resident_lamplighter","부인께 봉투를 받은 건 맞아요."),
            ("resident_lamplighter","다만 받을 분이 맞는지 확인하기 전에는 내드릴 수 없어요. 부인의 표시를 아는 분이어야 해요.")]),
    ]
    _g3_react("resident_lamplighter","J04",[(c,[("resident_lamplighter","나비가 그걸 봤군요.")]+l) for c,l in _g3_mail_rows])
    _g3_react("resident_lamplighter","J05",[(c,[("resident_lamplighter","까로 씨가 점검함을 봤군요.")]+l) for c,l in _g3_mail_rows])
    _g3_react("resident_lamplighter","J07",[
        ({"has":["E19"]},[("resident_lamplighter","초상 속 분이 부인이 맞아요. 답장을 전할 때도 헷갈릴 일은 없어요."),
            ("resident_lamplighter","얼굴은 알아도 계신 곳은 몰라요. 그게 서로 안전해요.")]),
        (None,[("resident_lamplighter","초상 속 분이 부인이 맞아요. 제가 직접 확인했잖아요."),
            ("resident_lamplighter","얼굴은 알아도 지금 어디 계신지는 몰라요.")]),
    ])
    _g3_react("resident_lamplighter","J08",[
        (_g3_mom_recognized,[("resident_lamplighter","슬링 씨가 그렇게 말했군요. 받는 사람 칸이 빈 편지는 제가 받아 갔어요."),
            ("resident_lamplighter","어디로 갔는지는 여기서 말하지 않을게요. 부인이 그렇게 부탁했어요.")]),
        (None,[("resident_lamplighter","우체국에서 편지를 받아 가는 건 제 일이에요."),
            ("resident_lamplighter","누구 편지인지는 받을 분이 맞는지 확인한 다음에 말씀드릴게요.")]),
    ])
    _g3_react("resident_lamplighter","J18",[(None,[
        ("resident_lamplighter","같이 열었지요. 제가 맡아 둔 봉투였고, 봉인도 그대로였어요."),
        ("resident_lamplighter","안에 적힌 말을 어떻게 볼지는 아버님이 판단하실 일이에요.")])])
    _g3_react("resident_lamplighter","L06",[
        (_g3_lt_solved,[("resident_lamplighter","회의에서 말한 그대로예요. 새벽에 돌 때 3번 등은 미지근했어요."),
            ("resident_lamplighter","제가 본 건 그 시각까지예요.")]),
        (None,[("resident_lamplighter","제가 새벽에 돌 때 3번 등은 미지근했어요. 그건 분명해요."),
            ("resident_lamplighter","그 뒤에 누가 열었는지는 못 봤어요. 저는 바로 다음 등으로 갔으니까요.")]),
    ])
    _g3_react("resident_lamplighter","N06",[(None,[
        ("resident_lamplighter","제가 직접 전해 드린 그 편지예요. 그분 글씨가 맞아요."),
        ("resident_lamplighter","편지에 적힌 일을 제가 확인해 드릴 수는 없어요. 저는 전하는 사람이니까요.")])])
    _g3_react("resident_lamplighter","W6",[(None,[
        ("resident_lamplighter","제가 센 그대로예요. 광장 등 넷이 한 달 사이 반나절씩 일찍 꺼져요. 조각도 이번 겨울에 두 번 갈았고요."),
        ("resident_lamplighter","등이 식는 건지 돌이 식는 건지는 저도 몰라요. 저는 켜고 끄는 것만 보니까요.")])])

    # 사서
    _g3_react("resident_librarian","L11",[
        (_g3_lt_solved,[("resident_librarian","회의에서 끈 이야기가 맞춰졌지요. 제가 본 건 창으로 들어온 사람의 허리에 감긴 노끈까지예요."),
            ("resident_librarian","얼굴은 끝내 못 봤어요.")]),
        (None,[("resident_librarian","제가 본 그대로예요. 허리에 노끈을 감은 사람이 창으로 들어와 난로 조각을 빼 갔어요."),
            ("resident_librarian","얼굴은 못 봤어요. 그러니 누구라고는 말씀드릴 수 없어요.")]),
    ])

    # 모모
    _g3_react("resident_momo","V01",[(None,[
        ("resident_momo","제 이름이 저기 있네요. ‘잊음’ 칸에요."),
        ("resident_momo","저는 아직 동생 이름도 기억하는데요. 누가 이 칸을 채웠는지는 저도 몰라요.")])])
    _g3_react("resident_momo","W9",[
        ({"has":["ep6:st_momo_glasses"]},[("resident_momo","흉보는 말 그대로 적으셨네요. 네, 옛 마을 물건이면 사요."),
            ("resident_momo","어디에 쓰느냐고 물으시면, 아무 데도 안 써요. 동생 숄처럼 남겨 두는 거예요.")]),
        (None,[("resident_momo","흉보는 말 그대로 적으셨네요. 네, 옛 마을 물건이면 사요."),
            ("resident_momo","어디에 쓰느냐고 물으시면…… 아무 데도 안 써요. 남겨 두는 거예요. 이유까지 다 말씀드릴 생각은 없어요.")]),
    ])

    # 피코 (L12·L13은 피코가 죽은 판에만 생기므로 반응을 두지 않는다)
    _g3_react("resident_piko","L00",[(None,[
        ("resident_piko","그날 새벽 일이요. 식당에서 자고, 그림 챙기러 나왔다가 그렇게 됐어요."),
        ("resident_piko","등이 왜 식었는지는 저도 몰라요. 눈을 떴을 땐 진료소였어요.")])])
    _g3_react("resident_piko","L09",[(None,[
        ("resident_piko","‘광장 3’이면 제가 자던 등이에요."),
        ("resident_piko","그 조각이 어떻게 백 부인 창고까지 갔는지는 저도 몰라요. 저는 그 밑에서 자기만 했으니까요.")])])
    _g3_react("resident_piko","P01",[(None,[
        ("resident_piko","제가 끝까지 그린 그 그림이에요. 코 찡그린 것까지요."),
        ("resident_piko","그분을 본 건 우체국 앞에서 소포를 안고 계실 때였어요. 그다음에 어디 가셨는지는 몰라요.")])])

    # 서리
    _g3_react("resident_seori","H10",[(None,[
        ("resident_seori","제가 직접 센 것입니다. 장부에 적힌 자루와 상자 수가 창고에 그대로 있었습니다."),
        ("resident_seori","누가 쌓아 두라고 시켰는지는 그 대조로 알 수 없습니다. 거기까지가 제 기록입니다.")])])
    _g3_react("resident_seori","H2",[(None,[
        ("resident_seori","제가 세어 적은 약초입니다. 마을에 약이 없다던 날이었지요."),
        ("resident_seori","왜 쌓아 두었는지는 제 기록에 없습니다. 제가 확인한 건 수량입니다.")])])
    _g3_react("resident_seori","H4",[(None,[
        ("resident_seori","제가 그 자리에서 확인한 일입니다. 빗장은 밖에서 질러져 있었습니다."),
        ("resident_seori","왜 가두려 했는지는 백 부인이 말하지 않았습니다. 짐작으로 적지는 않겠습니다.")])])
    _g3_react("resident_seori","W8",[(None,[
        ("resident_seori","보리 어머니의 기침 말이군요."),
        ("resident_seori","진료하지 않고 추위 탓이라고 적을 수는 없습니다. 직접 보기 전에는 답하지 않겠습니다.")])])

    # 슬링
    _g3_react("resident_sling","H9",[
        (_g3_sling_cold,[("resident_sling","그 일로 우체국에 못 나가게 됐어요. 다시 꺼내실 필요는 없잖아요."),
            ("resident_sling","어떤 편지를 왜 보려 하셨는지는 저도 몰라요. 그건 할머니께 있는 답이에요.")]),
        (None,[("resident_sling","……네. 일자리를 주시는 대신 여관 손님 편지를 열어 보라고 하셨어요."),
            ("resident_sling","어떤 편지를 왜 보려 하셨는지는 저도 몰라요. 저는 열어서 보여 드리기만 했어요.")]),
    ])
    _g3_react("resident_sling","J08",[(None,[
        ("resident_sling","제가 말씀드린 그대로예요. 그분은 밤마다 받는 사람 칸이 빈 편지를 부치러 오셨어요."),
        ("resident_sling","그 편지는 초롱 씨가 받아 갔어요. 그다음 어디로 갔는지는 저도 몰라요.")])])

    # 톡
    _g3_react("resident_tok","L01",[
        (_g3_lt_solved,[("resident_tok","제 장부예요. 적어 둔 덕에 3번 등 이야기가 맞춰졌지요."),
            ("resident_tok","그래도 적기만 하고 먼저 열어 보지 못한 건 마음에 남아요.")]),
        ({"has":["lt_dawn"]},[("resident_tok","제 장부예요. 3번 등이 깜빡인다고 적어 놓고도 먼저 열어 보지 못했어요."),
            ("resident_tok","그 등을 누가 열었는지는 장부에 없어요. 조각은 내가 안 뺐어요.")]),
        (None,[("resident_tok","제 장부예요. 3번 등이 요즘 밤마다 깜빡인다고 적어 뒀지요."),
            ("resident_tok","왜 깜빡이는지는 열어 봐야 알아요. 장부만으로는 몰라요.")]),
    ])
    _g3_react("resident_tok","L09",[(None,[
        ("resident_tok","제 글씨예요. ‘광장 3’. 제가 고친 조각마다 붙여 두는 이름표예요."),
        ("resident_tok","그게 왜 백 부인 창고에 있었는지는 저도 몰라요. 저는 판 적이 없어요.")])])
    _g3_react("resident_tok","W5",[(None,[
        ("resident_tok","맞아요. 등은 그 조각으로 데워져요. 빼면 금방 식고요."),
        ("resident_tok","조각이 왜 사람 손처럼 따뜻한지는 저도 설명 못 해요. 고칠 줄만 알지요.")])])

    # 따닥
    _g3_react("resident_ttadak","H7",[
        ({"case":"occurred"},[("resident_ttadak","제 기록이에요. 벽 안에 옛 통로가 있는 건 공사 때 직접 봤어요."),
            ("resident_ttadak","그날 밤 누가 그 길로 다녔는지는 몰라요. 저는 길이랑 폭만 쟀어요.")]),
        (None,[("resident_ttadak","제 기록 맞아요. 근데 크게 말하진 마세요. 허락 없이 덧지은 벽이라서요."),
            ("resident_ttadak","통로가 13호 책장 뒤로 이어지는 건 봤어요. 거기를 누가 쓰는지는 몰라요.")]),
    ])
    _g3_react("resident_ttadak","N03",[
        ({"any":[{"has":["nt_ttadak_safe"]},{"has":["nt_ttadak_half"]}]},[("resident_ttadak","제가 그렇게 말했죠. 제가 들어간다는 건 손님이랑 톡 씨, 할머니만 알았어요."),
            ("resident_ttadak","누가 손잡이를 당겼는지는 못 봤어요. 쇠 소리만 들었어요.")]),
        (None,[("resident_ttadak","제가 한 말 맞아요. 새벽에 통로 길이를 한 번 더 재요. 할머니께도 말씀드렸고요."),
            ("resident_ttadak","레버는 올려 두신다고 했어요. 왜요, 뭐가 걸리세요?")]),
    ])
    _g3_react("resident_ttadak","N07",[
        ({"has":["nt_ttadak_safe"]},[("resident_ttadak","쐐기에 걸려 멈춘 그 손잡이요. 새벽에 누가 두 번이나 당겼어요."),
            ("resident_ttadak","주방에 누가 있었는지는 판자 문 안에서 볼 수가 없었어요.")]),
        (None,[("resident_ttadak","그 손잡이가 내려가서 갇혔어요. 쇠 소리는 들었는데, 당긴 사람은 못 봤어요."),
            ("resident_ttadak","손이 아직 안 펴져요. 그것만 확실해요.")]),
    ])
    _g3_react("resident_ttadak","N09",[(None,[
        ("resident_ttadak","제가 쫀 자국이에요. 날개를 못 펴서 부리로 쪼았어요. 주방까지 들리라고요."),
        ("resident_ttadak","들은 사람이 있었는지는 저는 몰라요. 아무도 안 열어 줬어요.")])])

    # 우박
    _g3_react("resident_ubak","L05",[
        (_g3_lt_solved,[("resident_ubak","회의에서 제 말이 맞다고 해 주셔서…… 고마워요."),
            ("resident_ubak","그래도 제가 연 등 밑에서 일어난 일이라 잊히지 않아요.")]),
        (None,[("resident_ubak","제가 한 말 그대로예요. 온도만 재고, 새벽 되기 전에 조각을 돌려놨어요."),
            ("resident_ubak","그 뒤에 누가 열었는지는 몰라요. 제가 돌려놓은 뒤를 본 사람이 있으면 좋겠어요.")]),
    ])
    _g3_react("resident_ubak","W4",[(None,[
        ("resident_ubak","제가 잰 숫자예요. 가을보다 훨씬 낮고, 밤마다 조금씩 더 떨어져요."),
        ("resident_ubak","언제 완전히 멈출지는 몰라요. 재기만 해서는 그건 알 수 없어요.")])])
