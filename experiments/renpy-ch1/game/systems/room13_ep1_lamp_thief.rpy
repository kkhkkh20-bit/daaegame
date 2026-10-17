# 에피소드 ① 「등 도둑」 (1~4일). 대본: docs/EPISODE1_SCRIPT.md (v2 · 쉬운 말).
#   우박은 온도만 재고 조각을 돌려놓았다. 실룩이 다시 열어 훔쳐 백 부인에게 팔았다.
#   3번 등 밑에서 피코가, 기록실 난로 앞에서 사서 선생님이 얼어 죽는다(제시로 살릴 수 있다).
#   4일 아침 광장 회의(Q1)로 결판. 옛 사건 4 「톡의 공방」은 이 에피소드로 대신한다.
init 152 python:
    import re
    # ---- 단서 (모두 쉬운 물건, 설명은 '그래서 무슨 뜻'으로) ----
    for _key,_name,_kind,_est in (
        ("L00","등 밑의 피코","기록","3일 새벽, 광장 3번 등이 식고 그 밑에서 자던 그림쟁이 피코가 얼어 쓰러졌다."),
        ("L01","톡의 등 장부","물증","광장 3번 등이 요즘 밤마다 깜빡인다고 적혀 있다. 그 등은 곧 꺼질 수 있다."),
        ("L02","빌려 간 온도계","증언","등 속 온도를 재는 기구를 진료소 검사원이 빌려 갔다. 진료소 사람이 등을 열어 봤을 수 있다."),
        ("L03","등 속의 숫자 쪽지","물증","꺼진 3번 등 안에 온도를 적은 쪽지가 끼어 있었다. 누군가 등을 열고 온도를 쟀다."),
        ("L04","뚜껑에 걸린 노끈","물증","3번 등 뚜껑 틈에 짐 묶는 갈색 노끈이 걸려 있었다. 온도를 잰 사람 말고도 등을 연 사람이 한 명 더 있다."),
        ("L05","우박의 말","증언","우박은 온도만 재고, 새벽이 되기 전에 조각을 제자리에 돌려놨다고 했다."),
        ("L06","초롱의 말","증언","초롱은 새벽에 돌 때 3번 등이 아직 미지근했다고 했다. 우박 다음에 누가 또 열었다."),
        ("L07","실룩의 짐 끈","물증","실룩의 갈색 짐 끈은 한쪽 끝이 뜯겨 있다. 등 뚜껑에 걸린 끈과 같다."),
        ("L08","실룩 아이의 말","증언","실룩의 아이는 아빠가 어젯밤 늦게, 손이 꽁꽁 언 채 들어왔다고 했다."),
        ("L09","이름표 붙은 조각","물증","백 부인 창고의 조각 밑에 톡의 글씨로 '광장 3'이라는 이름표가 붙어 있다. 피코가 잠든 등에서 나온 조각이다."),
        ("L10","빈 난로","물증","기록실 난로 조각도 사라졌다. 같은 사람이 또 훔쳤다."),
        ("L11","사서의 말","증언","사서 선생님은 밤에 허리에 노끈을 감은 사람이 창으로 들어와 난로 조각을 빼 갔다고 했다."),
        ("L12","코 없는 엄마 초상","물증","피코가 그리다 만 엄마 초상. 코만 아직 그려져 있지 않다."),
        ("L13","피코의 스케치","물증","소포를 안고 우는 다람쥐 여인. 눈썹의 흉터가 엄마와 같다. 피코는 엄마를 본 적이 있다."),
        ("L14","나사 탁본","물증","3번 등 나사 둘레를 종이에 떠 둔 것. 등을 닦아 내도 흔적이 남는다."),
    ):
        ROOM13["evidence"][_key]=dict(id=_key,name=_name,kind=_kind,establishes=_est,does_not_establish="",scenes=[],current_run_only=True,retained_on_show=True)
    R13_RECORD_SHORT.update(L00="등 밑의 피코",L01="톡의 등 장부",L02="빌려 간 온도계",L03="숫자 쪽지",L04="뚜껑의 노끈",L05="우박의 말",
        L06="초롱의 말",L07="실룩의 짐 끈",L08="아이의 말",L09="이름표 조각",L10="빈 난로",L11="사서의 말",L12="코 없는 초상",L13="피코의 스케치",L14="나사 탁본")

    # ---- 옛 사건 4(톡의 공방)는 이 에피소드로 대신한다 ----
    ROOM13["activities"].pop("ep4_lamp_look",None)
    R13_CONTEXT_ACTIVITIES[("square","lamp")]=tuple(k for k in R13_CONTEXT_ACTIVITIES.get(("square","lamp"),()) if k!="ep4_lamp_look")
    ROOM13["topics"].pop("ubak_lamp",None)

    # ---- 광장 3번 등 (조사 지점) ----
    ROOM13["objects"]["square"]["lt_lamp3"]=dict(rect=[560,150,110,300],text="광장 3번 등. 피코가 늘 그 밑에서 잤다.",
        need=["lt_dawn"],give=[],flags=[],call_label="r13_ep1_lamp")
    R13_OBJECT_NAMES["lt_lamp3"]="광장 3번 등"

    # ---- 대화 주제 ----
    def _r13_e1_topic(npc,title,day,need=(),not_flags=(),lines=(),give=(),flags=()):
        return dict(npc=npc,title=title,day=list(day),need=list(need),not_flags=list(not_flags),give=list(give),flags=list(flags),lines=list(lines))
    ROOM13["topics"].update({
        "ep1:tok_lamps":_r13_e1_topic("resident_tok","광장 등은 누가 돌봅니까?",(2,3),need=["buri_honest"],not_flags=["lt_tok_lamps"],
            give=["L01","L02"],flags=["lt_tok_lamps"],lines=[
            ("resident_tok","등은 내 자식 같은 거라. 하나라도 식으면 그 밑에서 누가 떨잖아요."),
            ("buri","저기 공구판 빈자리요? 【온도계】 자리예요. 등 안이 얼마나 따뜻한지 재는 거요. 지난주에 진료소 검사원님이 빌려 갔어요."),
            ("resident_tok","(장부를 넘기며) 그나저나 광장 【3번 등】이 요 며칠 밤마다 깜빡여요. 내일 봐야지.")]),
        "ep1:nabi_shelter":_r13_e1_topic("nabi","광장 그림쟁이를 오늘 밤 여기서 재워 줄 수 없을까?",(2,2),need=["lt_piko_convinced"],not_flags=["lt_shelter_asked"]),
        "ep1:ubak":_r13_e1_topic("resident_ubak","광장 3번 등 안의 숫자 쪽지를 묻는다",(3,4),not_flags=["lt_ubak_done"]),
        "ep1:librarian":_r13_e1_topic("resident_librarian","피코가 여기 자주 왔습니까?",(3,3),need=["lt_dawn"],not_flags=["lt_lib_met"]),
    })
    R13_TOPIC_LABELS.update({"ep1:nabi_shelter":"r13_ep1_nabi_shelter","ep1:ubak":"r13_ep1_ubak","ep1:librarian":"r13_ep1_librarian"})

    _r13_e1_topics=r13_topics
    def r13_topics(person):
        rows=_r13_e1_topics(person)
        # 우박에게 물으려면 쪽지나 온도계 이야기를 먼저 알아야 한다.
        if person=="resident_ubak" and not (r13_has("L03") or r13_has("L02")):
            rows=[(k,s) for k,s in rows if k!="ep1:ubak"]
        return rows

    # ---- 제시: 살리기는 선택지가 아니라 증거를 보여 주는 것이다 ----
    _r13_e1_present=r13_present
    def r13_present(person,key,identity=False):
        s=store.room13 or {}
        d=s.get("day",1)
        if person=="resident_piko" and d==2 and not r13_has("lt_piko_convinced"):
            if key=="L01" and r13_has("L01"):
                _r13_e1_present(person,key,identity)
                r13_flag("lt_piko_convinced")
                return [("dad","수리공 톡 씨 장부입니다. 이 3번 등이 요즘 밤마다 깜빡인답니다. 오늘 밤 꺼질지도 몰라요."),
                    ("resident_piko","……3번이면 내가 자는 등인데."),
                    ("resident_piko","그러고 보니 어젯밤 새벽에 손이 시렸어요. 알았어요. 근데 갈 데가 없어요. 방값이 없으니까.")]
        if person=="resident_librarian" and d==3 and r13_has("lt_lib_met") and not r13_has("lt_lib_safe"):
            if key=="L04" and r13_has("L04") and not r13_has("lt_lib_warned"):
                _r13_e1_present(person,key,identity)
                r13_flag("lt_lib_warned")
                return [("dad","3번 등에서 누가 조각을 훔쳐 갔습니다. 이 노끈을 남기고요. 이 난로도 조각으로 돌죠."),
                    ("resident_librarian","……여기도요? 그래도 기록을 두고 갈 수는 없어요. 비우면 젖어 버려요.")]
            if key=="L03" and r13_has("L03") and not r13_has("lt_lib_warned"):
                return [("resident_librarian","검사원 조수 일이라면 들었어요. 돌려놨다던데요. 훔친 사람 이야기는 아니잖아요.")]
            if key=="L00" and r13_has("L00") and r13_has("lt_lib_warned"):
                _r13_e1_present(person,key,identity)
                r13_flag("lt_lib_safe")
                lines=[("resident_librarian","……피코가 그 등 밑에서……. (손을 떤다) 알았어요. 오늘 밤은 창을 잠그고, 조각은 서랍에 넣어 둘게요."),
                    ("resident_librarian","대신 장작이 있어야 해요. 조각 없이 버티려면요.")]
                if r13_has("nabi_helped"):
                    r13_flag("lt_lib_saved")
                    lines+=[(None,"나비에게 장작 한 아름을 얻어 기록실 난로 옆에 쌓아 두었다."),
                        ("resident_librarian","이렇게까지…… 고마워요. 오늘 밤은 버티겠네요.")]
                else:
                    r13_flag("lt_lib_ill")
                    lines+=[("dad","(장작을 나눠 줄 사람이 떠오르지 않는다. 여관 부엌 일을 도왔다면 나비에게 부탁할 수 있었을 텐데.)",{"thought":True})]
                return lines
        return _r13_e1_present(person,key,identity)

    # ---- 회의 Q1 (광장, 4일 아침) ----
    R13_DEBATE_SEATS["ep1"]=["resident_tok","buri","resident_lamplighter","resident_madam","resident_siluk","resident_ubak"]
    R13_DEBATE_STANCE["ep1"]=("톡을 의심","모르겠다","톡을 믿는다")
    R13_EP_MEETING_PLACE={"ep1":"winter_square"}
    R13_EP_MEETING_HEADER={"ep1":"광장 회의 · 4일째"}
    def r13_meeting_header(session):
        if session in R13_EP_MEETING_HEADER:
            # 0.18.91: a meeting convened early shows the day it actually happens.
            head=R13_EP_MEETING_HEADER[session]
            return re.sub(r"\d+일째","%d일째"%store.room13["day"],head) if store.room13 else head
        return "식당 회의 · %d일째"%R13_TRIAL_DAY if session=="trial" else "제단 앞 회의 · 14일째"
    R13_DEBATE["Q1"]=dict(title="3번 등을 열어 피코를 얼어 쓰러지게 한 사람",session="ep1",chair="neoul",
        statements=[
            dict(id="s1",who="neoul",text="3번 등을 연 건 【톡】이오. 등 여는 사람은 톡뿐이니까.",
                accept=["L03","L04","L14"],
                broken_by={
                    "L03":[("dad","등 안에 온도를 적은 쪽지가 있었습니다. 온도계는 지난주부터 진료소에 있었습니다. 톡 씨 손에는 그 도구가 없었어요."),("neoul","……그럼 온도를 잰 자를 데려오시오.")],
                    "L04":[("dad","뚜껑 틈에 짐 묶는 노끈이 걸려 있었습니다. 톡 씨는 노끈을 쓰지 않습니다. 이 등을 연 사람은 두 명입니다."),("neoul","……두 명이라고?")],
                    "L14":[("dad","등을 닦기 전에 나사 둘레를 떠 둔 종이입니다. 톡 씨 공구 자국은 없습니다."),("neoul","……종이 한 장으로 사람을 바꾸라는 거요?")]},
                hint="3번 등에서 찾은 쪽지나 노끈. 톡 씨 물건이 아니다.",
                wrong=("neoul","그게 등을 연 사람과 무슨 상관이오?")),
            dict(id="s2",who="neoul",text="온도계를 빌려 간 【검사원 조수】가 조각을 뺐소.",
                accept=["L06"],soft={"L05":("neoul","본인이 돌려놨다고 하면 그만이오? 증인을 대시오.")},
                broken_by={"L06":[("resident_lamplighter","새벽에 돌 때 등은 아직 미지근했어요. 조각이 그때까지 안에 있었다는 뜻이에요."),("neoul","……그 뒤에 또 누가 열었다는 거요?")]},
                hint="우박이 돌려놓은 뒤에도 등이 따뜻했다는 걸 본 사람이 있다.",
                wrong=("neoul","그게 조수가 손대지 않았다는 증거요?")),
            dict(id="s3",who="resident_madam",text="제 창고 조각은 【정당하게 산 것】이에요.",
                accept=["L09"],
                broken_by={"L09":[("dad","조각 밑에 톡 씨 글씨로 '광장 3'. 피코가 잠든 그 등입니다. 부인은 그 밑에서 잠든 사람 머리 위의 온기를 산 겁니다."),
                    (None,"광장이 웅성거렸다. 백 부인이 숄을 여몄다."),("resident_madam","……판 사람에게 물으세요.")]},
                hint="창고 조각에 붙어 있던 것.",
                wrong=("resident_madam","그게 제가 훔쳤다는 뜻인가요?")),
            dict(id="s4",who="neoul",text="누가 팔았든 【이미 끝난 일】이오. 톡만 풀어 주면 되지 않소.",
                accept=["L10","L11"],
                broken_by={"L10":[("dad","끝나지 않았습니다. 같은 사람이 기록실 난로 조각도 가져갔습니다. 그리고 한 사람이 더 쓰러졌습니다."),("neoul","……")],
                    "L11":[("resident_librarian","어젯밤 허리에 노끈을 감은 사람이 제 기록실 창으로 들어왔어요. 장작이 없었으면 저도 죽었을 거예요."),("neoul","……")]},
                hint="같은 손이 또 조각을 가져간 곳이 있다.",
                wrong=("neoul","그래서 무엇이 아직 안 끝났다는 거요?")),
            dict(id="s5",who="resident_siluk",text="그 노끈…… 【누구나 쓰는 끈】이오.",
                accept=["L07"],soft={"L08":("resident_siluk","애 말을 믿으라는 거요? 끈을 대 보시오.")},
                broken_by={"L07":[("dad","끝이 뜯긴 자리가 똑같습니다. 그리고 어젯밤 늦게, 손이 꽁꽁 언 채 들어오셨다고요. 따님이."),
                    (None,"실룩이 무릎을 꿇었다."),
                    ("resident_siluk","……빚이 열두 냥이었소. 못 갚으면 애들을 일꾼으로 보내야 했소."),
                    ("resident_siluk","등 하나 식는다고 사람이 쓰러질 줄은 몰랐소. 그림쟁이가 거기서 자는 줄은……."),
                    (None,"실룩의 아이가 빵 봉지를 떨어뜨렸다. 빵이 눈 위로 굴렀다."),
                    ("resident_madam","빚은 빚이에요. 저는 아무도 죽이지 않았어요."),
                    ("daram","(작게) ……아빠.")]},
                hint="뜯긴 노끈의 짝.",
                wrong=("resident_siluk","그게 내 끈이라는 증거요?")),
        ],
        conclusion=dict(prompt="이 일을 어떻게 정리할까?",
            options=[("correct","온도를 잰 건 우박, 조각을 훔친 건 실룩, 그 조각을 산 건 백 부인이다"),
                ("over","실룩이 일부러 사람을 죽였다"),
                ("weak","온도를 잰 검사원 탓이다")],
            correct=[("neoul","……좋소. 톡은 풀어 주겠소."),
                ("resident_tok","내가 고친 등 밑에서 잤어요. 내 탓이 아니라고 해도…… 편하진 않네요.")],
            over=("neoul","죽이려던 건 아니라지 않소. 그 말은 증거가 더 있어야 하오."),
            weak=("resident_seori","제가 연 등은 새벽에 따뜻했습니다.")),
        sway=["resident_tok","buri","resident_lamplighter"])

    _r13_e1_session=r13_debate_session
    def r13_debate_session(claim):
        spec=R13_DEBATE.get(claim) or {}
        if spec.get("session"):return spec["session"]
        return _r13_e1_session(claim)

    _r13_e1_seats=r13_debate_seats
    def r13_debate_seats(session):
        if session not in R13_EP_MEETING_PLACE:return _r13_e1_seats(session)
        props=(store.room13 or {}).get("propositions",[]);moved={}
        for claim,spec in R13_DEBATE.items():
            if spec.get("session")!=session:continue
            done,total=r13_debate_progress(claim)
            step=(1 if done*2>=total and done else 0)+(1 if claim in props else 0)
            for who in spec.get("sway",[]):moved[who]=max(moved.get(who,0),step)
        return [(who,min(2,moved.get(who,0))) for who in R13_DEBATE_SEATS[session]]

    _r13_e1_plate=r13_meeting_plate
    def r13_meeting_plate(session,close=False):
        if session in R13_EP_MEETING_PLACE and r13_meeting_kind(session)!="round":
            return Transform(r13_background(R13_EP_MEETING_PLACE[session]),xysize=(1280,720))
        return _r13_e1_plate(session,close)

    _r13_e1_cast=r13_meeting_cast
    def r13_meeting_cast(claim,session,speaker=None):
        if session in R13_EP_MEETING_PLACE:
            seats=list(r13_debate_seats(session));present={who for who,stance in seats}
            for who in [st["who"] for st in r13_debate_statements(claim)]+[R13_DEBATE[claim]["chair"]]:
                if who in CAST and who!=r13_viewpoint() and who not in present:
                    seats.append((who,None));present.add(who)
            return seats
        return _r13_e1_cast(claim,session,speaker)

    # ---- 밤 대화 ----
    for _k,_t,_c,_l in (
        ("night:ep1_promise","다람이가 그림쟁이 이야기를 한다",lambda:r13_has("lt_piko_promise") and store.room13["day"]==2,[
            ("daram","아빠, 그 아저씨가 엄마 그려 준대. 코 찡그리는 것도."),
            ("daram","엄마가 그림 보면 웃겠다. 그치?")]),
        ("night:ep1_cold","다람이가 창밖을 본다",lambda:r13_has("piko_seen") and not r13_has("lt_piko_promise") and store.room13["day"]==2,[
            ("daram","그 아저씨, 오늘도 밖에서 자?"),
            ("dad","……그럴 거야."),
            ("daram","춥겠다.")]),
    ):
        ROOM13["topics"][_k]=dict(npc="daram",title=_t,day=[2,2],need=["lodging"],give=[],flags=[],lines=list(_l))
        R13_NIGHT_TALK_COND[_k]=_c

    R13_EVENT_OFFERS.update({
        "r13_ep1_accused":("수리점 앞에 사람들이 모여 있다",["lt_open"],"수리점 앞에서 너울이 톡을 몰아세웠다는 말을 들었다."),
        "r13_ep1_meeting":("광장 돌 앞에 사람들이 모여 있다. 톡이 묶여 서 있다",[],""),
    })
    R13_OFFER_ACTORS.update({"r13_ep1_accused":("neoul",("angry",)),"r13_ep1_meeting":("neoul",("angry",))})

# =========================================================
# 장면
# =========================================================
label r13_ep1_events:
    $ _e1d,_e1p,_e1loc=room13["day"],room13["period"],room13["location"]
    # 옛 사건 4의 첫 장면과 기한이 다시 켜지지 않게 한다.
    if not r13_has("ep4_seen"):
        $ r13_flag("ep4_seen")
    if _e1d<=2 and _e1loc=="square" and not r13_has("piko_seen"):
        call r13_ep1_glimpse
    if _e1d==3 and not r13_has("lt_dawn"):
        call r13_ep1_dawn
        return
    if _e1d==3 and _e1p<=1 and _e1loc=="workshop" and not r13_has("lt_open"):
        $ r13_offer("r13_ep1_accused")
    if _e1d==3 and _e1p==2 and _e1loc=="square" and r13_has("piko_dead") and not r13_has("lt_funeral"):
        call r13_ep1_funeral
    if _e1d==4 and not r13_has("lt_lib_dawn"):
        call r13_ep1_library_dawn
    if _e1d==4 and _e1p<=1 and _e1loc=="gate" and not r13_has("lt_siluk_seen"):
        call r13_ep1_siluk
    if _e1d==4 and _e1p<=1 and _e1loc=="store" and not r13_has("lt_store_seen") and (r13_has("L04") or r13_has("L11")):
        call r13_ep1_store
    if _e1d==4 and _e1p<=1 and _e1loc=="square" and not r13_has("lt_done"):
        $ r13_offer("r13_ep1_meeting")
    if (_e1d>4 or (_e1d==4 and _e1p>=2)) and r13_has("lt_dawn") and not r13_has("lt_done"):
        call r13_ep1_deadline
    return

label r13_ep1_glimpse:
    $ r13_flag("piko_seen")
    call r13_lines([(None,"광장 둘레에 등이 다섯 개 서 있었다. 등 하나 밑에서 누군가 판자에 그림을 그리고 있었다."),
        ("resident_piko","여기가 마을에서 제일 따뜻해요. 등 안에 따뜻한 돌 조각이 들어 있거든요. 밤새 손을 데워 줘요."),
        ("daram","아저씨 그림 예쁘다!"),
        ("dad","(이 마을에서 등은 불빛이 아니라 난로구나.)",{"thought":True})],"ep1:glimpse")
    return

label r13_ep1_nabi_shelter:
    $ r13_flag("lt_shelter_asked")
    if r13_has("nabi_helped") or r13_has("lt_piko_promise"):
        if r13_has("nabi_helped"):
            call r13_lines([("nabi","그림쟁이 아저씨를 여기서요? 할머니가 아시면 큰일 나요."),
                ("nabi","……손님은 제 일 도와주셨으니까요. 식당 의자라도 괜찮다면요. 불 꺼진 뒤에만, 새벽엔 꼭 나가야 해요.")],"ep1:shelter:helped")
        else:
            call r13_lines([("nabi","그림쟁이 아저씨를 여기서요? 할머니가 아시면 큰일 나요."),
                ("dad","그 사람이 제 아내를 그려 주고 있습니다. 아내를 찾는 데 꼭 필요한 그림이에요."),
                ("nabi","……손님 부인을요? 오늘 하루만이에요.")],"ep1:shelter:portrait")
        $ r13_flag("piko_sheltered")
        $ r13_tick()
    else:
        call r13_lines([("nabi","그림쟁이 아저씨를 여기서요? 할머니가 아시면 큰일 나요."),
            ("nabi","죄송해요. 저도 여기서 쫓겨나면 갈 데가 없어요.")],"ep1:shelter:no")
    return

label r13_ep1_dawn:
    $ r13_flag("lt_dawn")
    $ r13_edit(location="square")
    call r13_scene("winter_square","광장 · 꺼진 3번 등","night")
    if r13_has("piko_sheltered"):
        $ r13_flag("piko_survived")
        call r13_lines([(None,"3번 등이 꺼져 있었다. 그 밑에 피코가 쓰러져 있었다. 식당에서 자고, 새벽에 그림을 챙기러 나왔다가."),
            ("nabi","제가 문을 너무 일찍 열었어요……. 숨은 쉬어요! 진료소로!"),
            (None,"사람들이 피코를 들어 옮겼다. 손에서 붓이 떨어지지 않았다.")],"ep1:dawn:survived")
        if r13_has("lt_piko_promise"):
            call r13_lines([(None,"피코의 품에서 판자 하나가 나왔다. 엄마의 얼굴. 코를 찡그린 모양까지 다 그려져 있었다."),
                ("daram","엄마다! 아저씨가 약속 지켰어!")],"ep1:dawn:portrait_done")
            $ r13_flag("mom_portrait")
            $ r13_grant(["P01"],"피코가 끝까지 그린 엄마 초상")
        $ r13_grant(["L00","L06"],"꺼진 3번 등 밑에서 쓰러진 피코")
    else:
        $ r13_flag("piko_dead")
        call r13_lines([(None,"광장이 이상하게 조용했다. 3번 등이 꺼져 있었다. 그 밑에 담요를 덮은 작은 몸이 웅크려 있었다. 손에는 붓이 쥐여 있었다."),
            ("resident_lamplighter","새벽에 돌 때만 해도…… 미지근했어요. 분명히."),
            ("daram","아빠, 아저씨 왜 안 일어나?")],"ep1:dawn:dead")
        call r13_lines([(None,"……눈 내리는 소리만 들렸다.")],"ep1:dawn:silence")
        if r13_has("lt_piko_promise"):
            call r13_lines([(None,"붓 옆에 판자 하나. 엄마의 얼굴이었다. 코만 아직 그려져 있지 않았다."),
                ("daram","……엄마다. 코를 아직 안 그렸어.")],"ep1:dawn:portrait")
            $ r13_grant(["L12"],"피코가 그리다 만 엄마 초상")
        else:
            call r13_lines([(None,"판자 사이에서 오래된 스케치가 나왔다. 다람쥐 여인이 소포를 안고 울고 있었다."),
                ("dad","(눈썹의 흉터. 아내다. 피코는 아내를 본 적이 있다.)",{"thought":True})],"ep1:dawn:sketch")
            $ r13_grant(["L13"],"피코의 판자 사이에서 나온 스케치")
        $ r13_grant(["L00","L06"],"3일 새벽 광장")
    call r13_lines([("dad","(등이 꺼진 밤에, 등 밑에서 잔 사람이 쓰러졌다.)",{"thought":True})],"ep1:dawn:thought")
    return

label r13_ep1_accused:
    $ r13_flag("lt_open")
    call r13_ev_here("search")
    call r13_lines([(None,"수리점 앞에 사람들이 모여 있었다. 너울이 톡의 작업대를 손바닥으로 내리쳤다."),
        ("neoul","3번 등 안의 돌 조각이 없어졌소. 그래서 그 밑에서 사람이 쓰러졌소."),
        ("neoul","그 등을 열 줄 아는 사람은 이 마을에 당신뿐이오."),
        ("resident_tok","나는 안 가져갔어요! 조각이 없으면 등이 식는다는 걸 제일 잘 아는 게 나라고요!"),
        ("neoul","내일 아침까지 범인이 안 나오면, 당신을 광장에 세우겠소.")],"ep1:accused")
    menu:
        "“증거도 없이 사람을 세울 겁니까?”":
            call r13_lines([("neoul","그럼 내일 아침까지 증거를 가져오시오.")],"ep1:accused:defend")
        "“톡 씨 말고 누가 열겠습니까.”":
            call r13_lines([(None,"너울이 톡의 손목을 묶었다."),("resident_tok","……당신도 똑같군요.")],"ep1:accused:side")
            $ r13_flag("tok_hostile")
        "끼어들지 않는다":
            pass
    return None

label r13_ep1_lamp:
    $ _e1_loop=True
    while _e1_loop:
        $ _e1_loop=False
        $ _e1_menu=[("꺼진 3번 등을 살핀다",None)]
        if not r13_has("L03"):
            $ _e1_menu.append(("등 안을 본다","inside"))
        if not r13_has("L04"):
            $ _e1_menu.append(("뚜껑 틈을 본다","gap"))
        if r13_has("own:rubbing") and not r13_has("L14"):
            $ _e1_menu.append(("탁본 종이로 나사 둘레를 떠 둔다","rub"))
        $ _e1_menu.append(("그만 본다","stop"))
        $ _e1_pick=renpy.display_menu(_e1_menu)
        if _e1_pick=="inside":
            call r13_lines([(None,"조각이 있던 자리에 작은 쪽지가 끼어 있었다. 숫자가 몇 개 적혀 있다. 온도를 잰 숫자 같다."),
                ("dad","(누군가 등을 열고 온도를 쟀다.)",{"thought":True})],"ep1:lamp:inside")
            $ r13_grant(["L03"],"꺼진 3번 등 안")
            $ _e1_loop=True
        elif _e1_pick=="gap":
            call r13_lines([(None,"뚜껑 틈에 갈색 노끈 한 가닥이 걸려 있었다. 짐을 묶을 때 쓰는 거친 끈이다."),
                ("dad","(온도를 잰 사람이 노끈을 쓸 리는 없다. 이 등을 연 사람이 한 명 더 있다.)",{"thought":True})],"ep1:lamp:gap")
            $ r13_grant(["L04"],"꺼진 3번 등 뚜껑")
            $ _e1_loop=True
        elif _e1_pick=="rub":
            call r13_lines([(None,"숯으로 문지르자 나사 둘레의 흔적이 종이 위에 고스란히 떠올랐다."),
                ("dad","(너울이 등을 닦아도, 이건 남는다.)",{"thought":True})],"ep1:lamp:rub")
            $ r13_use_item("rubbing")
            $ r13_grant(["L14"],"나사 둘레를 뜬 탁본")
            $ _e1_loop=True
    if r13_has("L03") and r13_has("L04") and r13_ep_first("lt_two_people"):
        call r13_lines([("dad","(정리하면, 이 등을 연 사람은 두 명이다. 온도를 잰 사람, 그리고 노끈을 남긴 사람.)",{"thought":True})],"ep1:lamp:summary")
    return

label r13_ep1_ubak:
    $ r13_flag("lt_ubak_done")
    call r13_lines([("dad","꺼진 3번 등 안에 온도를 적은 쪽지가 있었습니다."),
        ("resident_ubak","……! 제가 했어요. 스승님이 돌이 얼마나 식었는지 몰래 재 오라고 해서요."),
        ("resident_ubak","근데 온도만 재고, 새벽 되기 전에 조각을 【제자리에 돌려놨어요】. 진짜예요."),
        ("resident_ubak","그 아저씨가…… 저 때문이에요?"),
        ("resident_seori","제 심부름이었습니다. 그리고 이 아이가 돌려놨다면, 새벽엔 조각이 등 안에 있었어야 합니다.")],"ep1:ubak")
    $ r13_grant(["L05"],"우박의 말")
    menu:
        "“재 본 숫자는 어땠지?”":
            call r13_lines([("resident_ubak","가을보다 훨씬 낮아요. 밤마다 더 떨어져요."),
                ("resident_seori","마을의 돌 자체가 식고 있습니다.")],"ep1:ubak:numbers")
            $ r13_grant(["W4"],"우박이 잰 돌의 온도")
            $ r13_flag("know_stone_failing")
        "“울지 마. 같이 밝히자.”":
            call r13_lines([("resident_ubak","……네."),("resident_seori","고맙습니다. 저도 도울 일이 있으면 말씀하십시오.")],"ep1:ubak:trust")
            $ r13_flag("seori_trust","ubak_ally")
        "“우박이를 너울에게 데려가겠습니다.”":
            call r13_lines([("resident_seori","진짜 범인을 놓칠 겁니다. 이 아이는 돌려놨다고 했습니다.")],"ep1:ubak:blame")
            $ r13_flag("ubak_suspected","seori_cold")
    return

label r13_ep1_librarian:
    $ r13_flag("lt_lib_met")
    call r13_lines([("resident_librarian","따뜻한 차 한 잔은 늘 있어요."),
        ("resident_librarian","피코는 여기서 옛 그림을 자주 베껴 갔어요. 지난달엔 우체국 앞에서 소포를 안고 울던 다람쥐 여인을 그리고 싶다더군요."),
        ("dad","(아내다.)",{"thought":True}),
        ("resident_librarian","(난로를 보며) 요즘 이 난로 조각이 금방 식어요.")],"ep1:librarian")
    return

label r13_ep1_funeral:
    $ r13_flag("lt_funeral")
    call r13_scene("winter_square","광장 · 피코의 장례","night")
    call r13_lines([(None,"톡이 꺼진 등 옆에 피코의 판자 그림들을 하나씩 세웠다. 부리가 등잔을 들었다."),
        ("resident_tok","내가 고친 등 밑에서 잤어요. 내 탓이 아니라고 해도…… 편하진 않네요."),
        ("resident_momo","……세 냥이면 하룻밤 방값은 됐을 거요."),
        (None,"아무도 대답하지 않았다.")],"ep1:funeral")
    if r13_has("L12"):
        call r13_lines([(None,"다람이 크레용을 꺼내 엄마 초상 앞에 쪼그려 앉았다."),
            ("daram","아저씨. 약속 내가 지킬게."),
            (None,"다람이 삐뚤빼뚤, 엄마의 코를 찡그린 모양으로 그려 넣었다."),
            (None,"……눈 내리는 소리만 들렸다."),
            ("daram","……이제 엄마 웃는다.")],"ep1:funeral:nose")
        $ r13_flag("portrait_finished_by_daram","mom_portrait")
        $ r13_grant(["P01"],"다람이 코를 그려 넣은 엄마 초상")
    else:
        call r13_lines([(None,"다람이 피코의 판자 하나에 꽃을 올렸다."),("daram","아저씨 그림 예뻤어요.")],"ep1:funeral:flower")
    $ r13_flag("piko_mourned")
    $ r13_tick()
    return

label r13_ep1_library_dawn:
    $ r13_flag("lt_lib_dawn")
    if r13_has("lt_lib_saved"):
        call r13_lines([("resident_librarian","밤에 누가 창으로 들어왔어요. 장작이 있어서 버텼어요."),
            ("resident_librarian","얼굴은 못 봤지만, 허리에 【노끈】을 감고 있었어요.")],"ep1:library:saved")
        $ r13_grant(["L11","L10"],"기록실 사서의 말")
    elif r13_has("lt_lib_ill"):
        call r13_lines([(None,"기록실 사서 선생님이 밤새 앓다가 진료소로 옮겨졌다는 말을 들었다. 난로 조각은 사라졌다고 했다.")],"ep1:library:ill")
        $ r13_grant(["L10"],"기록실의 빈 난로")
    else:
        $ r13_flag("librarian_dead")
        call r13_scene("winter_post","우체국 안쪽 · 기록실","night")
        call r13_lines([(None,"난로가 꺼져 있었다. 조각이 있던 자리가 비어 있었다."),
            (None,"사서 선생님은 의자에 앉아 있었다. 무릎 위 기록 묶음에 자기 숄을 덮어 둔 채였다."),
            (None,"……눈 내리는 소리만 들렸다."),
            ("dad","(기록이 젖지 않게. 마지막까지.)",{"thought":True}),
            (None,"묶음 맨 위 대출 카드에 아내의 이름이 있었다."),
            ("dad","(여기 난로 조각도 사라졌다. 같은 사람이다.)",{"thought":True})],"ep1:library:dead")
        $ r13_grant(["L10"],"기록실의 빈 난로")
    return

label r13_ep1_siluk:
    $ r13_flag("lt_siluk_seen")
    call r13_lines([(None,"짐꾼 실룩이 짐을 묶고 있었다. 갈색 노끈, 한쪽 끝이 뜯겨 있었다."),
        ("resident_siluk","……무슨 일이오. 바쁘오."),
        (None,"실룩의 아이 둘이 따끈한 빵을 나눠 먹고 있었다. \"아빠가 빵 사 왔어요! 진짜 빵이에요!\"",{"show":"kid_siluk2","expression":"joy"})],"ep1:siluk")
    $ _e1_loop=True
    while _e1_loop:
        $ _e1_loop=False
        $ _e1_menu=[("무엇을 할까?",None)]
        if not r13_has("L07"):
            $ _e1_menu.append(("노끈을 본다","rope"))
        if not r13_has("L08"):
            $ _e1_menu.append(("아이에게 묻는다","kid"))
        if not r13_has("siluk_debt_known"):
            $ _e1_menu.append(("실룩에게 빚을 묻는다","debt"))
        $ _e1_menu.append(("그만 간다","stop"))
        $ _e1_pick=renpy.display_menu(_e1_menu)
        if _e1_pick=="rope":
            call r13_lines([("dad","(등 뚜껑에 걸려 있던 것과 같은 끈이다. 끝이 뜯긴 자리도.)",{"thought":True})],"ep1:siluk:rope")
            $ r13_grant(["L07"],"실룩의 짐 끈")
            $ _e1_loop=True
        elif _e1_pick=="kid":
            call r13_lines([(None,"실룩의 아이가 빵을 꼭 쥔 채 말했다. \"아빠가 어젯밤 늦게, 손이 꽁꽁 언 채 들어왔어요.\"",{"show":"kid_siluk1"})],"ep1:siluk:kid")
            $ r13_grant(["L08"],"실룩 아이의 말")
            $ _e1_loop=True
        elif _e1_pick=="debt":
            call r13_lines([("resident_siluk","……백 부인한테 진 빚, 다음 달까지 못 갚으면 애들을 그 집 일꾼으로 보내야 하오.")],"ep1:siluk:debt")
            $ r13_flag("siluk_debt_known")
            $ _e1_loop=True
    return

label r13_ep1_store:
    $ r13_flag("lt_store_seen")
    call r13_lines([(None,"창고 안쪽 상자에서 초록빛이 새어 나왔다. 손을 대니 사람 손처럼 따뜻했다. 등 조각들이다."),
        ("resident_madam","사고판 것뿐이에요. 요즘 온기가 얼마나 귀한지 아세요?"),
        (None,"조각 하나를 뒤집어 보니 밑에 작은 이름표. 톡의 글씨로 '광장 3'."),
        ("dad","(톡은 고친 조각마다 이름표를 붙인다. 이건 피코가 잠든 그 등의 조각이다.)",{"thought":True})],"ep1:store")
    $ r13_grant(["L09"],"백 부인 창고의 조각")
    return

label r13_ep1_meeting:
    call r13_scene("winter_square","광장 · 등 도둑 회의","hearing")
    call r13_lines([(None,"톡이 묶인 채 돌 앞에 서 있었다. 사람들 틈에 실룩의 아이 둘이 빵 봉지를 쥐고 서 있었다. 백 부인은 맨 앞줄에 앉았다."),
        ("neoul","그림쟁이가 쓰러졌소."+(" 기록실 선생도 죽었소." if r13_has("librarian_dead") else "")+" 오늘 끝냅시다.")],"ep1:meeting:open")
    call r13_debate_run("Q1")
    if _return:
        call r13_ep1_decision
    else:
        call r13_lines([("neoul","증거가 모자라오. 톡은 광장에 세우겠소."),(None,"톡이 끌려가며 수리점 쪽을 돌아보았다.")],"ep1:meeting:fail")
        $ r13_flag("tok_detained","lt_done")
    call r13_ep1_aftermath
    return None

label r13_ep1_decision:
    $ r13_flag("tok_cleared","lt_done","lt_solved")
    call r13_lines([("neoul","톡은 풀어 주겠소. 실룩은 내가 데려가오.")],"ep1:decision:open")
    $ _e1_menu=[("어떻게 할까?",None),("실룩을 데려가게 둔다","hand"),("백 부인 창고를 열어 조각을 돌려놓게 한다","store"),("둘 다 요구한다","both")]
    if r13_has("siluk_debt_known"):
        $ _e1_menu.append(("“실룩의 빚은 훔친 조각 값으로 없던 걸로 하시죠.”","debt"))
    $ _e1_pick=renpy.display_menu(_e1_menu)
    if _e1_pick in ("hand","both"):
        call r13_lines([(None,"너울이 실룩의 팔을 잡아끌었다. 실룩의 아이들이 따라가려다 넘어졌다.",{"show":"kid_siluk2","expression":"anxious"}),
            ("resident_siluk","애들은…… 애들은 건드리지 마시오!")],"ep1:decision:hand")
        $ r13_flag("siluk_handed")
    if _e1_pick in ("store","both"):
        call r13_lines([("resident_madam","내 돈으로 산 거예요!"),(None,"사람들이 창고 쪽으로 움직였다."),
            ("resident_madam","이 마을에서 오래 살 생각은 없으신가 보군요.")],"ep1:decision:store")
        $ r13_flag("madam_store_opened","madam_hostile")
    if _e1_pick=="debt":
        call r13_lines([("resident_madam","……뭐라고요?"),
            ("dad","부인이 산 조각은 훔친 물건입니다. 돌려주시든지, 그 값으로 빚을 지우시든지."),
            (None,"사람들의 눈이 백 부인에게 쏠렸다. 백 부인이 입술을 깨물었다."),
            ("resident_madam","……좋아요. 빚은 없던 걸로 하죠. 조각은 돌려주겠어요."),
            (None,"실룩이 아이들을 끌어안았다.")],"ep1:decision:debt")
        $ r13_flag("siluk_debt_cleared","madam_store_opened")
    return

label r13_ep1_aftermath:
    call r13_lines([(None,"톡이 '광장 3' 조각을 등에 다시 넣었다. 등이 데워졌다. 그런데 숨 몇 번 사이에 온기가 옅어졌다."),
        ("resident_tok","이 조각, 가을엔 밤새 따뜻했어요. 지금은…….")],"ep1:after:lamp")
    if r13_has("know_stone_failing"):
        call r13_lines([("resident_ubak","조각 탓이 아니에요. 【돌이 식고 있어요】.")],"ep1:after:ubak")
    call r13_lines([("dad","(실룩이 훔친 건 조각이지만, 피코를 쓰러뜨린 건 이 겨울이다.)",{"thought":True})],"ep1:after:thought")
    if r13_has("piko_dead"):
        call r13_lines([(None,"그날 밤, 다람이 그림책을 펼쳤다.",{"book":"U01-opening"}),
            (None,"「아침이 되자, 아저씨는 엄마 코를 다 못 그린 채 잠들어 있었어요.」",{"book":"U01-ending"}),
            ("daram","……아빠. 이 책, 이제 안 읽을래.")],"ep1:after:book")
    else:
        call r13_lines([(None,"그날 밤, 다람이 그림책을 펼쳤다.",{"book":"U01-opening"}),
            (None,"「아침이 되자, 누군가 아저씨에게 담요를 덮어 주었어요.」",{"book":"U01-ending"}),
            ("daram","아빠, 이번엔 끝이 바뀌었어.")],"ep1:after:book_saved")
    return

label r13_ep1_deadline:
    $ r13_flag("lt_done","tok_detained")
    call r13_lines([(None,"광장에 판자가 덧대진 기둥이 섰다. 톡이 그 앞에 묶여 있었다. 회의는 열리지 않았다."),
        ("dad","(진짜 범인은 아직 마을 어딘가에 있다.)",{"thought":True})],"ep1:deadline")
    return
