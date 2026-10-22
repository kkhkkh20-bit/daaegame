# 0.19.96 수첩 관계도 — 새 세계관 연결.
# 기존 관계도(room13_relations.rpy)는 예전 이야기의 표식(chorong_dead, N02 …)으로 숨짐·구함·관계를
# 판정했다. 새 세계관(v111)에서는 그 표식이 세워지지 않으므로 아래 값으로 같은 화면을 채운다.
# - 숨짐: 다섯 목숨(R13_NW_LIVES)과 톡·무쇠(R13_V111_LIFE), r13_nw_is_dead 기준.
# - 13번째 수레: 이송 명단(listed:) → '이송 명단', 떠남(departed:) → '수레로 떠남',
#   인계해 데려옴(handed:) → '수레에서 데려옴'(초록).
# - 다람: 붙잡힘(DARAM_DETAINED) / 학교에 있음 / 함께 있음. 엄마: family_reunited 전까지 '아직 못 만남'.
# - 관계 선: 새 세계관 자료(V111:…)를 얻은 뒤에만 생긴다. 이야기 판정에는 쓰지 않는다.
# - 언제: 해당 값이 처음 바뀐 날과 때를 rel_dates["nw:<값>"]에 적는다.
init 330 python:
    # 다섯 목숨(R13_NW_LIVES)에 톡·무쇠까지(R13_V111_LIFE).
    R13_NW_REL_LIFE = dict(R13_V111_LIFE);R13_NW_REL_LIFE.update(dict(R13_NW_LIVES))
    R13_NW_REL_WATCH = set(R13_NW_REL_LIFE.values())|{"DARAM_DETAINED","family_reunited","route12"}
    def r13_nw_rel_watched(key):
        return key in R13_NW_REL_WATCH or key.split(":",1)[0] in ("listed","departed","handed")

    _r13_nw_rel_set=r13_v111_set
    def r13_v111_set(key,value):
        stamp=r13_nw_rel_watched(key) and r13_v111_value(key)!=value
        _r13_nw_rel_set(key,value)
        if stamp:
            n=winter_copy.deepcopy(store.room13);dates=dict(n.get("rel_dates",{}))
            dates.setdefault("nw:"+key,(n.get("day",1),n.get("period",0)))
            n["rel_dates"]=dates;store.room13=n

    def r13_nw_rel_when(key):
        when=(store.room13 or {}).get("rel_dates",{}).get("nw:"+key)
        if not when:return ""
        return "%d일 %s "%(when[0],("아침","낮","저녁","밤")[min(3,when[1])])

    _r13_nw_rel_status=r13_rel_status
    def r13_rel_status(person):
        if not r13_v111_active():return _r13_nw_rel_status(person)
        # r13_v111_set already raises the old death flags (piko_dead, tok_dead, v111:owl_dead …)
        # with their dates, so a death the old chart knows is kept as it is.
        base=_r13_nw_rel_status(person)
        if base[0]=="dead":return base
        lives=R13_NW_REL_LIFE
        if person in lives and r13_nw_is_dead(person,lives[person]):
            key=lives[person] if r13_v111_value(lives[person]) is False else "route12"
            return "dead",r13_nw_rel_when(key)+"숨짐"
        if r13_v111_value("handed:"+person):return "saved",r13_nw_rel_when("handed:"+person)+"수레에서 데려옴"
        if r13_v111_value("departed:"+person):return "gone",r13_nw_rel_when("departed:"+person)+"수레로 떠남"
        if r13_v111_value("listed:"+person):return "missing",r13_nw_rel_when("listed:"+person)+"이송 명단"
        if person=="mom":
            return (None,"") if r13_v111_value("family_reunited") else ("missing","아직 못 만남")
        if person=="daram":
            if r13_v111_value("DARAM_DETAINED"):return "missing",r13_nw_rel_when("DARAM_DETAINED")+"붙잡혀 있음"
            if r13_v111_value("DARAM_location")=="school":return "missing","학교에 있음"
            return "with","함께 있음"
        return None,""

    def _r13_nw_owned_any(*keys):
        return lambda:any(r13_v111_owned(k) for k in keys)
    # (가, 나, 종류, 선 위의 말, 알게 되는 조건) — 모두 새 세계관 자료의 이름과 내용에서 온 사실.
    R13_NW_RELATIONS = [
        ("daram","mom","family","가족",lambda:True),
        ("granny","resident_tosil","family","함께 산다",lambda:True),
        ("resident_badook","guard","work","같은 순찰",lambda:True),
        ("resident_piko","mom","work","엄마의 초상을 그림",_r13_nw_owned_any("E09","NW_PIKO_PAINTING")),
        ("resident_lamplighter","resident_siluk","suspect","3번 등의 돌",_r13_nw_owned_any("E14","E17","E34")),
        ("resident_siluk","resident_madam","suspect","등 조각을 팔고 삼",_r13_nw_owned_any("E16","NW_MADAM_DAY7")),
        ("guard","bami","suspect","밤이를 지목",_r13_nw_owned_any("E20")),
        ("doto","resident_owlgp","suspect","도둑으로 몰림",_r13_nw_owned_any("E08_CHILD_ACCOUNT","E08_ROOM")),
        ("granny","resident_owlgp","suspect","핀과 목도리",_r13_nw_owned_any("E09_SCARF","E09_PIN_OWNER")),
        ("resident_bori","kid_dodam","family","아빠와 아들",_r13_nw_owned_any("E06_RESCUE","E06_EMPTY")),
        ("npc_pandol","resident_teacher","work","학교 물자 인수",_r13_nw_owned_any("E13_HANDOVER","E14_SUPPLY")),
        ("resident_ppul","neoul","work","장부와 규칙",_r13_nw_owned_any("NW_NEOUL_LEDGER")),
        ("resident_ppul","resident_badook","work","회관 창 안",_r13_nw_owned_any("NW_HALL_WINDOW")),
    ]
    _r13_nw_rel_edges=r13_rel_edges
    def r13_rel_edges():
        if not r13_v111_active():return _r13_nw_rel_edges()
        shown=set(r13_rel_people())
        return [(a,b,k,l) for a,b,k,l,ok in R13_NW_RELATIONS if a in shown and b in shown and ok()]
