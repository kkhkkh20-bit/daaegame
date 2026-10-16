# 에피소드 중심 날짜표 (2026-10-16 소유자 결정, docs/STORY_EPISODES_FULL.md).
#   예전: 13호 사건 4일 저녁 → 식당 재판 7일 → 둘째 주 8~14일.
#   지금: 에피소드 ①②③이 1~7일을 쓰고, 13호 사건은 7일 저녁, 재판은 10일, 둘째 주는 11~14일.
# 예전 날짜로 쓴 데이터(주제·활동·상점·날짜별 한마디)는 여기서 한꺼번에 새 날짜로 옮긴다.
# 코드 안의 날짜 조건은 R13_CASE_DAY / R13_TRIAL_DAY / R13_WEEK2_DAY와 r13_tl()을 쓴다.
# 새 에피소드 데이터(키가 "ep숫자:" 또는 "night:ep"로 시작)는 처음부터 새 날짜로 쓰므로 옮기지 않는다.
# 요일: 1일을 금요일로 둔다. 그래서 사건 7일=목요일, 재판 10일=일요일, 둘째 주 11일=월요일로
# 예전 대사의 요일("목요일 저녁", "일요일에 주민들을 모아", "월요일 아침")이 그대로 맞는다.
init -200 python:
    R13_CASE_DAY=7
    R13_TRIAL_DAY=10
    R13_WEEK2_DAY=11
    R13_WEEKDAY_SHIFT=4
    # 예전 날짜 → 새 날짜 (구간 끝, 정확한 날). 둘째 주 7일은 4일로 줄어든다.
    R13_TL_MAP={1:1,2:2,3:3,4:7,5:8,6:9,7:10,8:11,9:11,10:12,11:12,12:13,13:13,14:14}
    R13_TL_NATIVE_PREFIXES=("ep1:","ep2:","ep3:","ep4:","ep5:","ep6:","night:ep","altar:")

    def r13_tl(day):
        """예전 날짜 하나를 새 날짜로."""
        return R13_TL_MAP.get(day,day)

    def r13_tl_start(day):
        """예전 구간의 시작. 4일 이전에 열리던 것은 그대로 열린다(사건 전 날들이 늘었으므로)."""
        return day if day<=4 else r13_tl(day)

    def r13_tl_window(a,b):
        return r13_tl_start(a),r13_tl(b)

    def r13_weekday(day):
        return ("월","화","수","목","금","토","일")[(day-1+R13_WEEKDAY_SHIFT)%7]

init 990 python:
    def _r13_tl_native(key):
        return any(str(key).startswith(p) for p in R13_TL_NATIVE_PREFIXES)

    def _r13_tl_remap_specs(table):
        for key,spec in list(table.items()):
            if not isinstance(spec,dict) or _r13_tl_native(key) or spec.get("_tl"):continue
            if "day" in spec and isinstance(spec["day"],(list,tuple)) and len(spec["day"])==2:
                a,b=r13_tl_window(*spec["day"])
                spec["day"]=[a,b] if isinstance(spec["day"],list) else (a,b)
            spec["_tl"]=True

    _r13_tl_remap_specs(ROOM13["topics"])
    _r13_tl_remap_specs(ROOM13["activities"])
    for _r13_tl_loc in ROOM13.get("objects",{}).values():
        _r13_tl_remap_specs(_r13_tl_loc)
    _r13_tl_remap_specs(R13_SHOP)

    # 날짜별 한마디(calendar_daily): 예전 날짜 칸을 새 날짜 칸으로. 둘째 주에서 두 날이 겹치면 앞날 것을 쓴다.
    for _r13_tl_person,_r13_tl_daily in list(R13_OPENING_SCENES["calendar_daily"].items()):
        _r13_tl_new={}
        for _r13_tl_k in sorted(_r13_tl_daily,key=lambda k:int(k)):
            _r13_tl_new.setdefault(str(r13_tl(int(_r13_tl_k))),_r13_tl_daily[_r13_tl_k])
        R13_OPENING_SCENES["calendar_daily"][_r13_tl_person]=_r13_tl_new

    # 저녁 미션: (키, (첫날, 끝날), 장소, 제목, 안내, 조건)
    R13_EVENING_MISSIONS[:]=[(k,r13_tl_window(*days),place,title,hint,ok) if not _r13_tl_native(k) else (k,days,place,title,hint,ok)
        for k,days,place,title,hint,ok in R13_EVENING_MISSIONS]
