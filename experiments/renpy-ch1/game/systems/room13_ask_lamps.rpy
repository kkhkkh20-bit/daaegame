# 0.19.x 질문이 앞서 나가지 않게 · g3_lamps (소유자 2026-10-17)
#   "배달 일을 하는지 어떻게 알고 '배달 일은 힘들지 않니?'야?"
#   질문 제목은 아빠가 지금 아는 것(눈에 보이는 일, 들은 말, 첫 만남 장면)만 전제한다.
#
# 첫 만남 판단 (room13-dialogue-openings.json first_meetings)
#   - 첫날(1일=금요일)의 첫 만남(early)에서는 열 사람 모두 자기 일을 말한다.
#   - 둘째 날부터의 첫 만남(late)에서도 일을 말하는 사람: 사서("저는 사서입니다"),
#     슬링(아빠가 "우편 일로" 묻고 "예"), 바둑이("순찰 나가기 전까지는"), 피코(그림이 눈앞에 있고 "그림 보러 오신 거면").
#     이 넷은 만나면 곧 아는 셈이라 ask:job을 두지 않는다(질문 목록은 만난 뒤에만 열린다).
#   - late에서 일을 말하지 않는 사람: 초롱, 톡, 우박, 서리, 따닥, 모모. 이 여섯에게 ask:job을 둔다.
#     첫날 만났으면(early를 봤으면) ask:job은 나오지 않고, 그 장면을 본 것을 아는 조건으로 쓴다.
#   조건 함수는 이름 있는 함수로 쓴다(람다 금지). 기존 steps는 {"all":[기존, 새 조건]}으로 합친다.
init 195 python:
    def _ga3_met_day1(s,person):
        # 첫날(arrival)의 첫 만남에서는 early 장면이 나온다. 그날 만난 기록이 있으면 그 장면을 본 것이다.
        for e in s.get("encounters",[]) or []:
            if isinstance(e,dict) and e.get("person")==person and e.get("day")==1:
                return True
        return False

    def _ga3_d1_lamplighter(s):return _ga3_met_day1(s,"resident_lamplighter")
    def _ga3_d1_tok(s):return _ga3_met_day1(s,"resident_tok")
    def _ga3_d1_ubak(s):return _ga3_met_day1(s,"resident_ubak")
    def _ga3_d1_seori(s):return _ga3_met_day1(s,"resident_seori")
    def _ga3_d1_ttadak(s):return _ga3_met_day1(s,"resident_ttadak")
    def _ga3_d1_momo(s):return _ga3_met_day1(s,"resident_momo")

    def _ga3_job_open_lamplighter(s):return not _ga3_d1_lamplighter(s)
    def _ga3_job_open_tok(s):return not _ga3_d1_tok(s)
    def _ga3_job_open_ubak(s):return not _ga3_d1_ubak(s)
    def _ga3_job_open_seori(s):return not _ga3_d1_seori(s)
    def _ga3_job_open_ttadak(s):return not _ga3_d1_ttadak(s)
    def _ga3_job_open_momo(s):return not _ga3_d1_momo(s)

    # ---- 적용 도구 ----
    def _ga3_add_steps(key,cond):
        t=ROOM13["topics"].get(key)
        if t is None:return False
        old=t.get("steps")
        t["steps"]={"all":[old,cond]} if old is not None else cond
        return True

    def _ga3_knows(key,d1,person,extra):
        # 이 질문 자체를 이미 읽었으면(옛 저장) 감추지 않는다.
        rows=[{"has":["knows_job:"+person]},d1,{"has":[key]}]
        rows+=[{"has":[k]} for k in extra]
        return {"any":rows}

    def _ga3_retitle(key,title,summary=None):
        t=ROOM13["topics"].get(key)
        if t is None:return False
        was=t["title"]
        t["title"]=title
        if summary:R13_QUESTION_SUMMARIES[title]=summary
        elif was in R13_QUESTION_SUMMARIES:R13_QUESTION_SUMMARIES[title]=R13_QUESTION_SUMMARIES[was]
        return True

    def _ga3_put_first(person,key):
        # 질문 번호는 처음 보인 순서대로 매겨진다. 새 첫 질문이 그 사람 목록 맨 앞에 오게 사전 순서를 바꾼다.
        T=ROOM13["topics"]
        if key not in T:return
        rows=list(T.items())
        spec=T[key]
        rows=[(k,v) for k,v in rows if k!=key]
        at=next((i for i,(k,v) in enumerate(rows) if v.get("npc")==person),len(rows))
        rows.insert(at,(key,spec))
        T.clear()
        T.update(rows)

    def _ga3_job(person,title,summary,lines,again,steps):
        key="ask:job:"+person
        ROOM13["topics"][key]=dict(npc=person,title=title,day=[1,14],need=[],not_flags=[],give=[],
            flags=["knows_job:"+person],lines=list(lines),again=[(None,list(again))],steps=steps)
        R13_QUESTION_SUMMARIES[title]=summary
        _ga3_put_first(person,key)

    # =================================================================
    # 첫 질문 ask:job (late 첫 만남에서 일을 말하지 않는 여섯)
    # =================================================================
    # 초롱: 등 아래에서 점검함을 열고 등을 올려다본다(보이는 것).
    _ga3_job("resident_lamplighter","등을 돌보는 일을 하십니까?","등을 돌보는 일을 하는지 묻는다",
        [("dad","등을 돌보는 일을 하십니까?"),
         ("resident_lamplighter","네, 등불지기예요. 해가 지면 광장이랑 입구 쪽 등을 돌면서 켜졌는지, 흔들리지 않는지 봐요."),
         ("resident_lamplighter","고장 난 데는 수리점 톡 씨한테 맡기고요.")],
        [("resident_lamplighter","등불지기예요. 해가 지면 등을 한 바퀴씩 돌아요.")],
        _ga3_job_open_lamplighter)

    # 톡: 작업대에서 핀을 집게로 물고 살핀다.
    _ga3_job("resident_tok","여기서 무엇을 고치십니까?","무엇을 고치는지 묻는다",
        [("dad","여기서 무엇을 고치십니까?"),
         ("resident_tok","시계도 보고, 등도 보고, 쇠붙이로 된 건 웬만하면 다 봐요. 여기가 제 수리점이에요."),
         ("resident_tok","작은 부품이 많으니까 발밑만 조심해 주세요.")],
        [("resident_tok","시계, 등, 쇠붙이요. 고칠 게 생기면 가져오세요.")],
        _ga3_job_open_tok)

    # 우박: 계측기 바늘과 종이 눈금을 맞춘다. 청소년이라 아빠는 반말.
    _ga3_job("resident_ubak","무엇을 재고 있니?","무엇을 재는지 묻는다",
        [("dad","무엇을 재고 있니?"),
         ("resident_ubak","등이랑 돌에서 나오는 힘이요! 아, 저는 검사원 보조예요. 서리 검사원님 밑에서 배우고 있어요."),
         ("resident_ubak","아침엔 수리점에서, 오후엔 진료소에서 재요. 잰 숫자는 검사원님께 먼저 보여 드려야 하고요.")],
        [("resident_ubak","검사원 보조예요. 서리 검사원님 밑에서 재는 일을 배워요.")],
        _ga3_job_open_ubak)

    # 서리: 메모 옆에 확인한 사람 이름을 적는다.
    _ga3_job("resident_seori","무슨 서류를 보고 계십니까?","무슨 서류를 보는지 묻는다",
        [("dad","무슨 서류를 보고 계십니까?"),
         ("resident_seori","외부 관리국에서 나온 검사원입니다. 이 마을 진료소와 우체국 기록을 확인하고 있습니다."),
         ("resident_seori","누가 무엇을 직접 봤는지, 언제 확인했는지를 맞춰 두는 일입니다.")],
        [("resident_seori","관리국 검사원입니다. 진료소와 우체국 기록을 확인합니다.")],
        _ga3_job_open_seori)

    # 따닥: 벽의 벌어진 이음에 나무 조각을 대 본다.
    _ga3_job("resident_ttadak","벽을 고치시는 겁니까?","벽을 고치는 중인지 묻는다",
        [("dad","벽을 고치시는 겁니까?"),
         ("resident_ttadak","네, 목수예요. 집이든 벽이든 낡은 데를 손봐요. 아침엔 수리점, 오후엔 여관 공사요."),
         ("resident_ttadak","두드려 보면 속이 빈 데를 알아요. 그러니 아무 데나 두드리시면 안 돼요.")],
        [("resident_ttadak","목수예요. 낡은 데를 손보는 일이요.")],
        _ga3_job_open_ttadak)

    # 모모: 우체국 구석에서 낡은 등잔 바닥의 번호를 읽는다(place_reasons: 박물관 물건을 맡겨 두고 정리).
    _ga3_job("resident_momo","이 옛 물건들을 정리하십니까?","옛 물건을 정리하는지 묻는다",
        [("dad","이 옛 물건들을 정리하십니까?"),
         ("resident_momo","네, 박물관 관장이에요. 박물관 물건 일부를 여기 우체국 구석에 맡겨 두고 정리하는 중이에요."),
         ("resident_momo","보시는 건 얼마든지 좋아요. 손은 대지 마시고요.")],
        [("resident_momo","박물관 관장이에요. 보시는 건 언제든 좋아요.")],
        _ga3_job_open_momo)

    # =================================================================
    # 직업·사정을 전제한 질문에 조건 걸기
    # =================================================================
    # 톡: "고쳐 달라는 부탁", "수리를 맡기면"은 수리점 주인이라는 걸 알아야 한다.
    _GA3_TOK_EXTRA=["tok_repair","tok_pin","item:file","cross:tok_pin_job","heard_pin_job","ep1:tok_lamps","tok_cleared","tok_hostile"]
    for _ga3_k in ("life:resident_tok:after","life:resident_tok:crisis"):
        _ga3_add_steps(_ga3_k,_ga3_knows(_ga3_k,_ga3_d1_tok,"resident_tok",_GA3_TOK_EXTRA))

    # 서리: 기록을 맡은 검사원이라는 것, 진료소 환자를 본다는 것.
    _GA3_SEORI_EXTRA=["ask:job:resident_ubak","seori_case","seori_previous","seal_look","w2_erased"]
    for _ga3_k in ("life:resident_seori:work","life:resident_seori:after","life:resident_seori:crisis","w2_doctor"):
        _ga3_add_steps(_ga3_k,_ga3_knows(_ga3_k,_ga3_d1_seori,"resident_seori",_GA3_SEORI_EXTRA))

    # 따닥: 마을 집들을 고치는 목수라는 것.
    _GA3_TTADAK_EXTRA=["life:resident_ttadak:work","smalltalk:ttadak_wood","ep4:st_ttadak_boards","ttadak_hostile","nt_ttadak_safe","nt_ttadak_half"]
    for _ga3_k in ("life:resident_ttadak:after","life:resident_ttadak:crisis"):
        _ga3_add_steps(_ga3_k,_ga3_knows(_ga3_k,_ga3_d1_ttadak,"resident_ttadak",_GA3_TTADAK_EXTRA))
    # "말씀하신 대로 도면부터"는 따닥이 도면 이야기를 한 뒤에만(life:resident_ttadak:work 답).
    _ga3_add_steps("smalltalk:ttadak_plan",{"any":[{"has":["life:resident_ttadak:work"]},{"has":["smalltalk:ttadak_plan"]}]})

    # 초롱: "연락을 맡긴 분들"은 초롱이 연락을 맡고 있다는 걸 안 뒤에만.
    _ga3_add_steps("life:resident_lamplighter:crisis",{"any":[{"has":[k]} for k in
        ("E18","E19","reply_agreed","warning_location","mother_intervened","topic:w2_contact","w2_contact",
         "lamplighter_warning","warning_open_with","mom_reunited","life:resident_lamplighter:crisis")]})

    # =================================================================
    # 모르는 것을 전제한 제목을 관찰형으로 (첫 대사는 그 인물이 하므로 variants 불필요)
    # =================================================================
    # 우박은 청소년: 아빠는 반말(본문 첫 줄이 이미 "잴 때마다 숫자가 다르게 나오니?").
    _ga3_retitle("life:resident_ubak:work","잴 때마다 숫자가 다르니?")
    _ga3_retitle("life:resident_ubak:measurement","다시 잴 때는 무엇을 비교해야 하니?")
    # 누가 따라온다는 건 초롱이 말해 줘야 안다.
    _ga3_retitle("w2_lamps","등을 점검할 때 별일은 없습니까?","등 점검에 별일이 없는지 묻는다")
    # "그 그림"은 아빠가 들은 적 없는 물건이다. 눈앞의 그림으로 묻는다.
    _ga3_retitle("life:resident_momo:after","이 그림을 좀 봐도 되겠습니까?","그림을 봐도 되는지 묻는다")
    _ga3_retitle("life:resident_momo:crisis","그림 속 장치는 지금도 쓸 수 있습니까?","그림 속 장치를 지금 쓸 수 있는지 묻는다")
    # "대피할 때도"는 아직 듣지 못한 사정이다. 바둑이 첫 대사("명령이라면 이름을 적어 주십시오")에 맞춘다.
    _ga3_retitle("life:resident_badook:after","명령을 받으면 어떻게 확인합니까?","명령을 어떻게 확인하는지 묻는다")
