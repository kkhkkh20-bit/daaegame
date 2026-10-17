# 0.19.17 질문이 앞서 나가지 않게 · g2 여관·13호 사건 쪽 인물 (소유자 2026-10-17)
#   "배달 일을 하는지 어떻게 알고 '배달 일은 힘들지 않니?'야?" — 질문 제목은 아빠가 지금 아는 것만 전제한다.
#   맡은 인물: 까로(karo), 돌목(guard), 도토(doto), 세련(seryeon), 부엉이 할아버지(resident_owlgp), 부리(buri)
#   일을 아는 근거
#   - 까로: 도착 장면에서 마차를 몰고 왔고 바퀴 축에 금이 간 것을 직접 봤다(entry:karo:arrival). 새 질문 없음.
#   - 돌목: 입구 초소에서 방문 등록을 받았다(life:arrival:entry). 새 질문 없음.
#   - 세련: 첫 만남에서 "저는 여기서 우편 접수를 맡고 있습니다"라고 한다. 새 질문 없음.
#   - 부리: 첫 만남에서 부품 작업대를 보여 주고 "고칠 물건 있으세요?"라고 한다(늦은 첫 만남도 공구 놓인 작업대가 보인다). 새 질문 없음.
#   - 도토: 첫 만남에서 아빠가 무슨 일을 하는지 물었지만 길 얘기로 넘어갔다 → ask:job:doto.
#   - 부엉이 할아버지: 첫 만남은 등을 보는 모습뿐이고 예전 일(은퇴 탐정)은 말하지 않는다 → ask:job:resident_owlgp.
init 194 python:
    def _ak2_steps(key,new):
        t=ROOM13["topics"].get(key)
        if not t:return
        old=t.get("steps")
        t["steps"]={"all":[old,new]} if old else new

    def _ak2_retitle(key,title,summary=None):
        t=ROOM13["topics"].get(key)
        if not t:return
        was=t.get("title")
        t["title"]=title
        if was in R13_QUESTION_SUMMARIES:R13_QUESTION_SUMMARIES[title]=R13_QUESTION_SUMMARIES[was]
        if summary:R13_QUESTION_SUMMARIES[title]=summary

    # ================= 첫 질문: 하는 일 =================
    ROOM13["topics"]["ask:job:doto"]=dict(npc="doto",title="광장에서 무슨 일을 맡고 있니?",day=[1,14],need=[],not_flags=[],give=[],
        flags=["knows_job:doto"],
        lines=[
            ("doto","어른들 장부를 옮겨 적어요. 배급하는 날엔 광장에서 이름하고 몫을 맞추는 것도 돕고요."),
            ("doto","틀리게 적으면 누가 밥을 못 받으니까, 한 줄 쓰고 한 번 더 봐요.")],
        again=[(None,[("doto","장부 옮겨 적는 일이요. 배급하는 날엔 이름하고 몫도 맞춰요.")])])
    R13_QUESTION_SUMMARIES["광장에서 무슨 일을 맡고 있니?"]="도토가 광장에서 하는 일을 묻는다"

    ROOM13["topics"]["ask:job:resident_owlgp"]=dict(npc="resident_owlgp",title="등을 살피는 일을 맡고 계십니까?",day=[1,14],need=[],not_flags=[],give=[],
        flags=["knows_job:resident_owlgp"],
        lines=[
            ("resident_owlgp","맡았다기보다 버릇이오. 아침마다 등 번호를 맞춰 보고 초롱에게 알려 주오."),
            ("resident_owlgp","본래 하던 일은 따로 있었소. 사라진 사람이나 다툰 일을 캐어 묻고 적는 일이었소. 손 뗀 지 오래요.")],
        again=[(None,[("resident_owlgp","아침엔 등 번호를 보오. 남의 일 캐던 버릇은 이제 수첩에만 남았소.")])])
    R13_QUESTION_SUMMARIES["등을 살피는 일을 맡고 계십니까?"]="등을 살피는 일을 맡았는지 묻는다"

    # ================= 도토: 장부 일을 안 뒤에만 =================
    #   life:doto:work(옮겨 적는 장부)나 ask:job:doto를 들은 뒤에야 장부를 고치는 일·기록 이야기를 꺼낸다.
    _ak2_doto_job={"any":[{"has":["knows_job:doto"]},{"has":["life:doto:work"]}]}
    _ak2_steps("life:doto:after",_ak2_doto_job)
    _ak2_steps("life:doto:crisis",_ak2_doto_job)

    # ================= 부엉이 할아버지 =================
    # "아직도 기록을 하십니까?"는 예전에 기록하던 사람이라는 걸 전제한다. 보이는 것은 수첩이다.
    _ak2_retitle("life:resident_owlgp:work","수첩에 무엇을 적고 계십니까?","수첩에 무엇을 적는지 묻는다")
    if "life:resident_owlgp:work" in ROOM13["topics"]:
        ROOM13["topics"]["life:resident_owlgp:work"]["variants"]=[
            (None,[
                ("dad","수첩에 무엇을 그렇게 적고 계십니까?"),
                ("resident_owlgp","다 기억한다고 생각하는 일이 제일 위험하오. 그래서 적는 거요."),
                ("dad","적어 둔 걸 다시 읽으면 달라집니까?"),
                ("resident_owlgp","다시 읽어 보면, 내가 본 일보다 남에게 들은 일이 더 많더구려.")])]+list(ROOM13["topics"]["life:resident_owlgp:work"].get("variants") or [])

    # "예전 조사 이야기"는 은퇴 탐정이라는 걸 전제한다. 열리는 근거는 문턱 장면의 "내 쪽에서 이야기하리다"이다.
    _ak2_retitle("owl_old_case","하시겠다던 이야기를 들려주시겠습니까?","하시겠다던 이야기를 청한다")
    if "owl_old_case" in ROOM13["topics"]:
        _ak2_t=ROOM13["topics"]["owl_old_case"]
        _ak2_t["variants"]=[
            ({"has":["knows_job:resident_owlgp"]},[
                ("dad","문턱을 고치시던 날 이야기를 해 주시겠다고 하셨지요. 예전에 하시던 조사 이야기입니까?"),
                ("resident_owlgp","그렇소. 그때는 나도 충분히 확인했다고 생각했소."),
                ("dad","지금은 다르게 생각하십니까?"),
                ("resident_owlgp","확인한 것과 믿은 것을…… 같은 칸에 적어 놓았더구려.")]),
            (None,[
                ("dad","문턱을 고치시던 날 이야기를 해 주시겠다고 하셨지요."),
                ("resident_owlgp","그랬소. 나는 오래 남의 일을 캐어 묻고 적는 일을 했소. 예전 조사 이야기요."),
                ("resident_owlgp","그때는 나도 충분히 확인했다고 생각했소."),
                ("dad","지금은 다르게 생각하십니까?"),
                ("resident_owlgp","확인한 것과 믿은 것을…… 같은 칸에 적어 놓았더구려.")]),
        ]+list(_ak2_t.get("variants") or [])
        if "knows_job:resident_owlgp" not in _ak2_t.get("flags",[]):
            _ak2_t["flags"]=list(_ak2_t.get("flags",[]))+["knows_job:resident_owlgp"]

    # ================= 까로 =================
    # "제 앞으로 되돌아온 물건이 있다고요?"는 누군가에게 들었다는 전제다. 짐표 소식은 까로가 처음 꺼낸다.
    #   아빠가 아는 것: 까로가 짐을 실어 오고 내려 주는 사람이다("내려 드린 짐은 빠진 것 없고요?").
    _ak2_retitle("karo_parcel","저희 앞으로 온 짐은 없습니까?","따로 온 짐이 있는지 묻는다")

    # "초롱 씨는 맡은 편지를 어디에 둡니까?"는 초롱이 편지를 맡는다는 걸 전제한다(메모에는 "소식을 물어보라"뿐).
    _ak2_retitle("poc:karo_box","초롱 씨가 편지를 맡아 두는 곳이 있습니까?")

    # ================= 부리 =================
    # 아빠는 청소년(부리)에게 부드러운 반말을 쓴다. 이 제목만 존댓말로 남아 있었다.
    _ak2_retitle("w2_buri_ops","장치를 멈추면 누가 남아야 하니?")
