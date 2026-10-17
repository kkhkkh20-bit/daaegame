# 에피소드 ③ 「장작 창고의 불」 (4일 오후 ~ 7일 오후). 대본: docs/EPISODE3_SCRIPT.md
#   아이 셋을 먹이려던 엄마가, 남의 아이를 태웠다.
#   4일 오후·저녁: 빨래터에서 너울이 누비에게 한 약속을 엿듣는다. 학교 뒤 장작 창고의 꼬미를 만난다.
#     꼬미를 살리려면 사자 선생님(너울의 약속을 보여 준다 → 출석부)과 꼬미(출석부를 보여 준다)를 둘 다 움직인다.
#     (완벽한 길: ① 회의 뒤 4일 오후 빨래터 → 4일 저녁 학교. 5일은 다람의 하루라 칸이 없다.)
#   5일 밤: 장작 창고에 불(②의 '두 불빛'). 보리가 아이 셋을 끌어낸다. 꼬미는 나오지 못한다(살리지 못했다면).
#   6일: 보리가 붙잡힌다. 나비가 자기 등잔 탓이라 무너진다. 창고 터·학교·빨래터를 살핀다.
#   7일 오전: 나비를 감쌀지, 누비의 말을 들을지(한 칸). 7일 오전·오후: 학교 회의 Q3.
#   깃발 접두사 wf_, 장면 이름 r13_wf_* (옛 큰 사건 3의 r13_ep3_*와 겹치지 않게).
init 154 python:
    for _key,_name,_est,_not in (
        ("F01","너울의 약속","빨래터에서 엿들은 말. 너울: \"그 애들이 줄면, 그 몫은 당신 집으로 가오.\" 그래서 무슨 뜻? 너울이 누비에게 창고 아이들을 치우라고 부추겼다.","너울은 '없애라'고는 말하지 않았다."),
        ("F02","가득 찬 등유 통","4일, 빨래 솥 옆 기름통은 뚜껑까지 꽉 차 있었다. 그래서 무슨 뜻? 나중에 줄었다면 누가 많이 썼다.","언제 줄었는지는 이것만으로 모른다."),
        ("F03","나비의 등잔","뚜껑을 덮으면 꺼지는 여관 등잔. 나비가 창고 아이들에게 빌려주며 \"잘 땐 꼭 뚜껑 닫으라\"고 했다.","그 밤 뚜껑을 닫았는지는 모른다."),
        ("F04","보리의 손바닥","보리는 두 손바닥만 데었고 손등은 멀쩡하다. 그래서 무슨 뜻? 불을 붙인 손이 아니라, 불붙은 판자를 꽉 쥐고 뜯어낸 손이다.","보리가 장작을 훔친 건 맞다."),
        ("F05","뚜껑 닫힌 등잔","창고 안쪽 구석에서 나온 등잔. 뚜껑이 닫혔고 기름이 그대로다. 그래서 무슨 뜻? 불은 등잔에서 나지 않았다.",""),
        ("F06","까만 문틀","문틀은 숯이 됐는데 안쪽 장작은 겉만 그을렸다. 그래서 무슨 뜻? 불은 안이 아니라 문에서 시작됐다. 그래서 아이들이 문으로 못 나왔다.",""),
        ("F07","문 앞 눈의 기름 냄새","창고 문 앞 녹은 눈에 무지개 같은 기름막, 독한 냄새. 그래서 무슨 뜻? 누가 문 앞에 솥에 쓰는 등유를 부었다.","누가 부었는지는 모른다."),
        ("F08","살아남은 아이의 말","\"문 쪽이 먼저 빨갰어. 곰 아저씨가 뒷벽을 부수고 우릴 끌어냈어.\" 그래서 무슨 뜻? 보리는 불을 낸 사람이 아니라 아이들을 꺼낸 사람이다.",""),
        ("F09","반쯤 빈 등유 통","6일, 빨래터 기름통이 반이나 비었다. 솥 밑 불은 거의 안 땠다. 그래서 무슨 뜻? 빨래터 기름이 다른 데 쓰였다.",""),
        ("F10","누비의 손등","누비의 손등에 새로 덴 물집. 솥에 데면 손바닥이나 팔이다. 그래서 무슨 뜻? 확 피어오르는 불 앞에 손을 뻗은 사람이다.",""),
        ("F11","누비 아이의 말","누비의 큰아이: \"엄마가 어젯밤 늦게 왔어. 엄마한테 빨래터 기름 냄새 났어. 손을 계속 씻었어.\"",""),
        ("F12","누비의 말","누비: \"불만 내려고 했어요. 너울 님이 그 애들 몫을 우리 집에 준다고 했어요.\" 그래서 무슨 뜻? 누비가 불을 냈고, 너울의 약속이 그 손을 밀었다.","누비 말뿐이라면 너울은 부인할 수 있다."),
        ("F13","출석부 한 장","사자 선생님이 출석부 맨 아래 빈 줄에 창고 아이들 이름 넷을 적었다. 맨 위에 꼬미. 오늘 밤부터 학교 돌창고에 자리가 있다.",""),
        ("F14","사자 선생님의 말","\"그 밤 아이들은 학교 돌창고에 있었어요. 제가 증인이에요.\" 그래서 무슨 뜻? 창고 안에 아이들은 없었고, 보리는 아이들을 구하려고 뒷벽을 뜯었다.",""),
    ):
        ROOM13["evidence"][_key]=dict(id=_key,name=_name,kind="기록",establishes=_est,does_not_establish=_not or "이것만으로 다른 사실까지 정할 수는 없다.",scenes=[],current_run_only=True,retained_on_show=True)
    R13_RECORD_SHORT.update(F01="너울의 약속",F02="꽉 찬 등유 통",F03="나비의 등잔",F04="보리의 손바닥",F05="뚜껑 닫힌 등잔",F06="까만 문틀",F07="문 앞 기름 냄새",
        F08="살아남은 아이의 말",F09="반쯤 빈 등유 통",F10="누비의 손등",F11="누비 아이의 말",F12="누비의 말",F13="출석부 한 장",F14="선생님의 말")

    # 학교 선생님은 사자다(소유자 2026-10-16). 사자 그림은 0.18.89(dev/apply_ep_art.py).
    R13_NAMES["resident_teacher"]="사자 선생님"
    R13_CHARS["resident_teacher"]=Character("사자 선생님",cb_who_id="resident_teacher")
    # 아이들(0.18.89부터 그림이 있다: cast.json, dev/apply_ep_art.py).
    for _k,_n in (("kid_kkomi","꼬미"),("kid_kkam","깜이"),("kid_mong","몽이"),("kid_bang","방울"),("kid_nubi1","누비의 큰아이"),("kid_nubi2","누비의 둘째")):
        R13_NAMES[_k]=_n
        R13_CHARS[_k]=Character(_n,cb_who_id=_k)

    def r13_wf_topic(npc,title,day,need=(),not_flags=(),flags=(),give=(),lines=()):
        return dict(npc=npc,title=title,day=list(day),need=list(need),not_flags=list(not_flags),flags=list(flags),give=list(give),lines=list(lines))
    ROOM13["topics"].update({
        "ep3:nabi_bowls":r13_wf_topic("nabi","따로 덜어 둔 그릇 넷은 뭐니?",(3,4),not_flags=["wf_kids_known"],flags=["wf_kids_known","know_nabi_debt"],give=["F03"],lines=[
            (None,"나비가 남은 밥을 따로 그릇 넷에 덜고 있었다. 그릇 옆에 작은 등잔 하나."),
            ("nabi","……이건 할머니한텐 비밀이에요."),
            ("nabi","학교 뒤 장작 창고에 애들이 살아요. 【표】가 없어서 밥도 장작도 못 받는 애들이요."),
            (None,"표: 마을 명단에 이름이 올라 밥과 장작을 받는 종이. 표가 없으면 아무것도 못 받는다."),
            ("nabi","밤에 깜깜하면 무섭대서, 여관 등잔 하나 빌려줬어요. 뚜껑을 덮으면 불이 꺼지는 거예요."),
            ("nabi","잘 땐 【꼭 뚜껑 닫으라고】 했어요. 꼬미는 대장이라 말 잘 들어요."),
            ("nabi","……저도 예전엔 표가 없었어요. 할머니가 거둬 주시기 전엔요.")]),
    })

    _r13_wf_present=r13_present
    def r13_present(person,key,identity=False):
        s=store.room13
        if person=="resident_teacher" and s["day"]<=4 and not r13_has("wf_fire"):
            if key=="F01" and not r13_has("F13"):
                r13_flag("wf_teacher_moved","wf_kids_known")
                r13_grant(["F13"],"사자 선생님이 출석부 빈 줄에 적은 이름 넷")
                return [("dad","빨래터에서 들었습니다. 너울이 누비 아주머니에게, 그 애들이 '줄면' 몫을 주겠다고 했습니다. 이번 주 안에."),
                    ("resident_teacher","……줄면, 이라고요."),
                    (None,"선생님이 안경을 벗었다. 한참을 창밖만 보았다."),
                    ("resident_teacher","학교 뒤에 교구 창고가 있어요. 난로는 없지만 벽이 돌이라 불이 안 붙어요. 오늘 밤부터 거기서 재우지요."),
                    ("resident_teacher","그런데 그 애들이 저를 믿을까요. 이름 한 번 불러 준 적이 없는데."),
                    (None,"선생님이 출석부를 펼쳐, 맨 아래 빈 줄에 펜을 댔다."),
                    ("resident_teacher","이름이 뭐래요? 이름을 알아야 부르지요."),
                    (None,"빈 줄에 이름 넷이 적혔다. 맨 위에 꼬미."),
                    ("dad","(이제 꼬미가 이 종이를 믿어야 한다.)",{"thought":True})]
            if key=="F03":
                return [("resident_teacher","등잔은 조심하면 되지요. 그 애들, 생각보다 영리해요.")]
        return _r13_wf_present(person,key,identity)

    # ---- 회의 Q3 (학교, 의장 촌장) ----
    R13_DEBATE_SEATS["ep3"]=["resident_ppul","resident_teacher","resident_bori","nabi","resident_nubi","resident_badook"]
    R13_DEBATE_STANCE["ep3"]=("보리를 의심","모르겠다","보리를 믿는다")
    R13_EP_MEETING_PLACE["ep3"]="r13_school"
    R13_EP_MEETING_HEADER["ep3"]="학교 회의 · 7일째"
    R13_DEBATE["Q3"]=dict(title="장작 창고에 불을 낸 사람",session="ep3",chair="resident_ppul",
        statements=[
            dict(id="s1",who="neoul",text="【보리】가 장작을 훔치다 불을 냈소. 그 밤 창고에 있던 어른은 보리뿐이오.",
                accept=["F04","F08","F14"],
                broken_by={
                    "F04":[("dad","손바닥만 데었습니다. 불을 붙인 손이 아니라, 불붙은 판자를 뜯어낸 손입니다."),("kid_kkam","곰 아저씨가 우리 꺼냈어!"),("neoul","……장작 도둑인 건 변함없소. 그럼 등잔이오.")],
                    "F08":[("dad","살아남은 아이들 말입니다. 문 쪽이 먼저 빨갰고, 보리 씨가 뒷벽을 부숴 아이들을 끌어냈습니다."),("kid_kkam","곰 아저씨가 우리 꺼냈어!"),("neoul","……장작 도둑인 건 변함없소. 그럼 등잔이오.")],
                    "F14":[("resident_teacher","그 밤 아이들은 학교 돌창고에 있었어요. 보리 씨는 빈 창고에 아이들이 있는 줄 알고 맨손으로 벽을 뜯었어요."),("neoul","……장작 도둑인 건 변함없소. 그럼 등잔이오.")]},
                # 0.19.15: 꼬미를 구한 판에는 창고가 비어 있었다. 보리가 아이들을 끌어낸 일은 없다.
                broken_if={"F04":("wf_kkomi_alive",[("dad","손바닥만 데었습니다. 불을 붙인 손이 아니라, 불붙은 판자를 뜯어낸 손입니다."),
                    ("resident_teacher","그 밤 아이들은 학교에 있었어요. 보리 씨는 창고에 아이들이 있는 줄 알고 벽을 뜯은 거예요."),("neoul","……장작 도둑인 건 변함없소. 그럼 등잔이오.")])},
                hint="보리의 손, 또는 그 밤 창고에 있던 아이들.",
                wrong=("neoul","그게 보리가 불을 안 냈다는 증거요?")),
            dict(id="s2",who="neoul",text="불은 【나비의 등잔】에서 났소. 그 애가 스스로 말했소.",
                accept=["F05"],
                broken_by={"F05":[("dad","창고 안쪽 구석에서 나왔습니다. 뚜껑이 닫혔고 기름이 그대로입니다. 꼬미가 약속대로 닫았습니다."),(None,"나비가 두 손으로 입을 막았다.")]},
                hint="그 밤 등잔이 켜져 있었는지.",
                wrong=("neoul","등잔 이야기를 하시오.")),
            dict(id="s3",who="neoul",text="그럼 【저절로】 난 불이오. 장작 창고는 원래 잘 타오.",
                accept=["F06","F07"],
                broken_by={
                    "F06":[("dad","안쪽 장작은 겉만 그을렸고 문틀은 숯이 됐습니다. 불은 문에서 시작됐습니다. 그래서 아이들이 문으로 못 나왔습니다."),(None,"사람들이 웅성거렸다.")],
                    "F07":[("dad","문 앞 눈에서 등유 냄새가 납니다. 솥에 쓰는 독한 기름입니다. 누가 문 앞에 부었습니다."),(None,"사람들이 웅성거렸다.")]},
                hint="불이 어디서 시작됐는지.",
                wrong=("neoul","창고는 원래 잘 타오.")),
            dict(id="s4",who="neoul",text="등유야 【집집마다】 쓰오. 누구라도 부을 수 있소.",
                accept=["F09","F10"],
                broken_by={
                    "F09":[("dad","등유를 통째로 쓰는 곳은 빨래터뿐입니다. 그 통이 반이 비었습니다."+(" 불 나기 전에는 뚜껑까지 꽉 차 있었습니다." if False else "")),(None,"사람들이 누비를 돌아보았다.")],
                    "F10":[("dad","그 밤 손등을 덴 사람이 있습니다. 확 피어오르는 불 앞에 손을 뻗어야 손등이 뎁니다."),(None,"사람들이 누비를 돌아보았다.")]},
                hint="등유를 통째로 쓰는 곳.",
                wrong=("neoul","그게 누구를 가리키오?")),
            dict(id="s5",who="resident_nubi",text="저는 【그 밤 집에】 있었어요. 애들 재우고요.",
                accept=["F11","F12"],
                broken_by={
                    "F11":[("dad","어젯밤 늦게 오셨다고요. 기름 냄새가 나서, 손을 계속 씻으셨다고. ……큰아이가."),
                        (None,"……"),
                        ("kid_nubi1","엄마, 그 기름 냄새…… 그거였어?"),
                        (None,"누비가 무릎을 꿇었다. 업힌 아기가 놀라 울기 시작했다."),
                        ("resident_nubi","……불만 내려고 했어요. 애들이 나가기만 하면 됐어요. 바람이, 바람이 바뀌어서……"),
                        ("resident_nubi","우리 막내가 사흘째 물만 먹었어요. 젖도 안 나와요. 저도 애가 셋이에요. 셋이라고요."),
                        ("resident_nubi","그 애도 누구 애였을 텐데. 그걸 그날 밤엔 생각 못 했어요."),
                        ("resident_nubi","(너울을 본다) 너울 님이 그랬잖아요. 그 애들이 줄면, 우리 집에 준다고."),
                        ("neoul","나는 그런 말 한 적 없소. 저 여자가 지어낸 말이오."),
                        ("kid_kkam","……아기 배고파서 울어?"),
                        ("resident_bori","(묶인 손으로 얼굴을 덮는다) 제길. 제길……."),
                        ("daram","(작게) ……아빠. 마녀야? 저 아줌마가 마녀야?")],
                    "F12":[("dad","오늘 아침 빨래터에서 직접 하신 말씀입니다. 불만 내려고 했다고."),
                        (None,"누비가 무릎을 꿇었다. 업힌 아기가 놀라 울기 시작했다."),
                        ("resident_nubi","우리 막내가 사흘째 물만 먹었어요. 저도 애가 셋이에요. 셋이라고요."),
                        ("resident_nubi","(너울을 본다) 너울 님이 그랬잖아요. 그 애들이 줄면, 우리 집에 준다고."),
                        ("neoul","나는 그런 말 한 적 없소. 저 여자가 지어낸 말이오."),
                        ("daram","(작게) ……아빠. 마녀야? 저 아줌마가 마녀야?")]},
                hint="그 밤 누비가 집에 늦게 왔다는 걸 아는 사람.",
                wrong=("resident_nubi","……그게 뭐요.")),
        ],
        conclusion=dict(prompt="이 불을 어떻게 정리할까?",
            options=[("correct","누비가 문 앞에 등유를 부었다. 쫓아내려던 불이 바람에 번졌다"),
                ("over","누비가 아이들을 죽이려 했다"),
                ("weak","보리가 장작을 훔쳐서 생긴 일이다")],
            correct=[("resident_ppul","……불은 등잔도 보리도 아니구려."),("neoul","보리는 풀어 주겠소. 장작 값은 따로 받겠소. 누비는 내가 데려가오.")],
            over=("resident_teacher","죽이려 했다면 뒷벽에도 부었겠지요. 기름은 문 앞에만 있었어요."),
            weak=("kid_kkam","곰 아저씨 나쁜 사람 아니야!")),
        sway=["resident_teacher","resident_badook","nabi"])

    R13_EVENT_OFFERS.update({
        "r13_wf_laundry":("빨래 줄 너머로 완장 찬 사람이 걸어온다",["wf_laundry_missed"],"빨래터에서 너울이 누비 아주머니와 오래 이야기했다는 말을 들었다."),
        "r13_wf_hideout":("학교 뒤 장작 창고 문틈으로 아이 목소리가 새어 나온다",[],""),
        "r13_wf_nabi_blame":("주방에서 나비가 빈 그릇 넷 앞에 주저앉아 있다",[],"나비가 주방에서 울고 있었다는 말을 들었다."),
        "r13_wf_ruins":("타고 남은 장작 창고 터에 검은 물이 고여 있다",[],""),
        "r13_wf_nubi":("빨래터 솥 밑 불이 꺼져 있다. 누비가 손을 천으로 감고 있다",[],""),
        "r13_wf_choice":("주방에서는 나비가 보따리를 싸고, 빨래터에서는 누비가 운다",[],""),
        "r13_wf_meeting":("학교 교실에 사람들이 모여 있다. 보리가 묶여 서 있다",[],""),
    })
    R13_OFFER_ACTORS.update({"r13_wf_laundry":("resident_nubi",None),"r13_wf_nabi_blame":("nabi",None),"r13_wf_nubi":("resident_nubi",None),"r13_wf_meeting":("neoul",("angry",))})

# =========================================================
# 장면
# =========================================================
label r13_wf_events:
    $ _wfd,_wfp,_wfloc=room13["day"],room13["period"],room13["location"]
    # 옛 묶음 3의 O 「학교 장작」(보리의 장작 도둑, 8~9일 저녁)은 이 에피소드가 대신한다.
    if r13_has("wf_fire") and not r13_has("ev_o_done"):
        $ r13_flag("ev_o_done")
    if _wfd==4 and _wfp>=1 and _wfloc=="kitchen" and not r13_has("wf_overheard") and not r13_has("wf_laundry_tried"):
        $ r13_offer("r13_wf_laundry")
    if _wfd==4 and _wfp>=1 and _wfloc=="school" and (r13_has("wf_kids_known") or r13_has("F13")) and not r13_has("wf_kkomi_saved") and not r13_has("wf_hideout_today"):
        $ r13_offer("r13_wf_hideout")
    if _wfd==6 and not r13_has("wf_morning"):
        call r13_wf_morning
        return
    if _wfd==6 and _wfp<=1 and _wfloc=="kitchen" and not r13_has("wf_nabi_blame"):
        $ r13_offer("r13_wf_nabi_blame")
    if _wfd==6 and _wfloc=="school" and not r13_has("wf_ruins"):
        $ r13_offer("r13_wf_ruins")
    if _wfd==6 and _wfp>=1 and _wfloc=="kitchen" and not r13_has("wf_nubi_seen"):
        $ r13_offer("r13_wf_nubi")
    # 0.18.91 조기 소집: 6일 저녁, 반박할 자료가 다 모였으면 학교에서 회의를 미리 연다. 7일이 빈다.
    if _wfd==6 and _wfp>=2 and _wfloc=="school" and r13_has("wf_fire") and not r13_has("wf_done") and r13_debate_arguable("Q3"):
        $ r13_offer("r13_wf_meeting")
    if _wfd==7 and _wfp==0 and _wfloc=="kitchen" and not r13_has("wf_choice_done") and not r13_has("wf_done"):
        $ r13_offer("r13_wf_choice")
    if _wfd==7 and _wfp<=1 and _wfloc=="school" and r13_has("wf_fire") and not r13_has("wf_done"):
        $ r13_offer("r13_wf_meeting")
    if (_wfd>7 or (_wfd==7 and _wfp>=2)) and r13_has("wf_fire") and not r13_has("wf_done"):
        call r13_wf_missed
    return

label r13_wf_laundry:
    $ r13_flag("wf_laundry_tried")
    call r13_scene("ep_laundry","여관 뒤 빨래터","quiet")
    call r13_lines([(None,"여관 뒤 빨래터. 큰 솥 밑에서 등유 불이 약하게 탔다. 솥 옆에 기름통 하나. 뚜껑까지 꽉 차 있었다."),
        (None,"등유: 등잔과 빨래 솥에 쓰는 기름. 냄새가 독하다."),
        (None,"누비 아주머니가 등에 아기를 업은 채 젖은 이불을 짜고 있었다. 손이 빨갛게 터 있었다."),
        ("resident_nubi","아이고, 손님. 빨래 맡기시게요? ……오늘은 솥이 덜 데워져서요. 기름도 아껴 써야 하고요."),
        (None,"빨래 줄 너머로 완장 찬 사람이 걸어왔다. 너울이다.")],"wf:laundry")
    $ r13_grant(["F02"],"빨래 솥 옆 기름통을 직접 봄")
    menu:
        "빨래 줄 뒤에 선다":
            call r13_lines([("neoul","이번 주 배급이 또 줄었소. 알고 있소?"),
                ("resident_nubi","……애들이 셋이에요. 막내는 사흘째 물만 먹었어요."),
                ("neoul","학교 뒤 장작 창고에 표 없는 애들이 산다는 건 아시오?"),
                ("neoul","그 애들이 먹는 밥, 그 애들이 때는 장작. 다 누구 몫이겠소."),
                ("neoul","그 애들이 【줄면】, 그 몫은 당신 집으로 가오. 명단은 내가 손보겠소."),
                ("resident_nubi","줄면……요? 어떻게 줄어요?"),
                ("neoul","그건 내 알 바 아니오. 이번 주 안이오."),
                (None,"너울이 가 버렸다. 누비는 한참 동안 솥 옆 기름통을 내려다보았다."),
                (None,"등에 업힌 아기가 칭얼댔다. 누비가 기계처럼 몸을 흔들었다."),
                ("dad","('줄면'. 누구도 '없애라'고는 말하지 않았다. 그래서 더 무섭다.)",{"thought":True})],"wf:laundry:overhear")
            $ r13_grant(["F01"],"빨래터에서 엿들은 너울의 말")
            $ r13_flag("wf_overheard","wf_kids_known")
        "인사한다":
            call r13_lines([("neoul","아, 여관 손님이오. 빨래 얘기나 하고 있었소."),
                (None,"너울은 말을 돌리고 가 버렸다.")],"wf:laundry:greet")
        "그냥 간다":
            pass
    $ r13_tick()
    return

label r13_wf_hideout:
    $ r13_flag("wf_hideout_today")
    call r13_scene("ep_hideout","학교 뒤 · 장작 창고","calm")
    if not r13_has("wf_kkomi_met"):
        call r13_lines([(None,"학교 뒷마당 끝, 지붕이 내려앉은 장작 창고. 문틈으로 아이 목소리가 새어 나왔다."),
            ("kid_kkomi","누구야! ……나비 누나 그릇이네. 누나 심부름이야?",{"pose":"door_peek"}),
            ("daram","나 다람이야. 탐정이야."),
            ("kid_kkomi","탐정? 나는 꼬미. 여기 대장."),
            (None,"안은 생각보다 아늑했다. 장작을 쌓아 벽을 만들고, 그 안쪽에 담요 넷이 깔려 있었다. 구석에 나비의 등잔."),
            ("kid_kkomi","여긴 비밀 아지트야. 【여긴 우리만 아는 데야.】 어른들은 몰라.",{"pose":"hideout_proud"}),
            ("kid_kkomi","아, 곰 아저씨는 알아. 밤마다 장작 몇 개씩 몰래 가져가. 우리도 못 본 척해 줘. 아저씨도 우리 못 본 척해 주니까."),
            ("daram","이거 줄게. 도토리. 내 탐정 표시야."),
            ("kid_kkomi","우리 탐정단 같은 거네. 아지트 대장 표시."),
            ("kid_kkomi","다음엔 너도 와. 밤에 오면 등잔 켜고 무서운 얘기 해 줄게."),
            ("daram","응! 약속!"),
            ("dad","(장작더미 속에 아이 넷. 불씨 하나면 끝이다.)",{"thought":True})],"wf:hideout")
        $ r13_flag("wf_kkomi_met","wf_kids_known")
    call r13_lines([("kid_kkomi","학교? 싫어. 여긴 우리만 아는 데라니까."),
        ("kid_kkomi","학교는 표 있는 애들 데잖아. 거기 가면 어른들이 이름 물어보고, 그러다 보호소 보내.")],"wf:hideout:refuse")
    menu:
        "출석부를 보여 준다" if r13_has("F13"):
            call r13_lines([("dad","학교 선생님이 너희 이름을 적었어. 오늘 밤부터 너희 자리가 있대."),
                ("kid_kkomi","(종이를 받아 든다) ……이거 내 이름이야? 꼬, 미."),
                ("kid_kkomi","나 내 이름 이렇게 생긴 거 처음 봐."),
                ("kid_bang","대장, 내 것도 있어? 어디?",{"pose":"cling_leg"}),
                ("kid_kkomi","(한참 종이를 보다가) ……딱 오늘만이야. 담요 챙겨. 등잔은 뚜껑 닫고 두고 가. 대장이 맨 뒤에 간다.")],"wf:hideout:saved")
            $ r13_flag("wf_kkomi_saved","kids_school")
        "너울의 말을 전한다" if r13_has("F01"):
            call r13_lines([("kid_kkomi","어른이 우리 없애려 한다고? 그럼 더 꼭꼭 숨어야지."),
                (None,"아이들이 장작더미 더 안쪽으로 숨었다."),
                ("dad","(겁만 줬다. 숨을 곳을 보여 줘야 했다.)",{"thought":True})],"wf:hideout:scared")
        "오늘은 돌아간다":
            pass
    $ r13_tick()
    return

label r13_wf_fire:
    # ②의 5일 밤 뒤에 이어진다(systems/room13_ep2_kids.rpy).
    $ r13_flag("wf_fire")
    call r13_scene("ep_woodshed_fire","5일 밤 · 학교 뒤 장작 창고","night")
    if r13_has("wf_kkomi_saved") or r13_has("kids_school"):
        call r13_lines([(None,"창고 문 쪽이 통째로 타고 있었다."),
            (None,"뒤쪽에서 판자 부서지는 소리. 커다란 곰이 맨손으로 불붙은 판자를 뜯어내고 있었다. 보리다."),
            ("resident_bori","애들은! 애들 어디 있어!"),
            (None,"창고 안은 비어 있었다. 학교 돌창고 창문에 작은 얼굴 넷이 붙어 있었다."),
            (None,"꼬미가 다람에게 손을 흔들었다. 손에 도토리가 쥐여 있었다.")],"wf:fire:saved")
        $ r13_flag("wf_kkomi_alive")
        return
    call r13_lines([(None,"창고 문 쪽이 통째로 타고 있었다. 문으로는 아무도 나올 수 없었다."),
        (None,"뒤쪽에서 판자 부서지는 소리. 커다란 곰이 맨손으로 불붙은 판자를 뜯어내고 있었다. 보리다."),
        ("resident_bori","나와! 이쪽으로! 기어서 나와!"),
        (None,"보리가 아이 하나, 또 하나, 또 하나를 끌어냈다. 아이들은 기침을 하며 눈밭에 굴렀다."),
        ("resident_bori","몇이야! 몇 명이야, 여기!"),
        ("kid_kkam","넷…… 꼬미가 아직……! 꼬미가 우리 깨우고, 대장은 맨 나중에 나온다고……",{"expression":"anxious"}),
        ("resident_bori","하나가 안 나왔어! 하나가!"),
        (None,"보리가 다시 불 속으로 손을 뻗었다. 그때 지붕이 내려앉았다."),
        (None,"……"),
        (None,"눈 내리는 소리. 보리는 데인 손으로 아이 셋을 한꺼번에 끌어안고 있었다. 아이들보다 보리가 더 크게 떨고 있었다."),
        ("daram","……아빠. 꼬미 아직 안 나왔어. 대장은 맨 나중에 나온댔어.")],"wf:fire:dead")
    $ r13_flag("kkomi_dead")
    return

label r13_wf_morning:
    $ r13_flag("wf_morning")
    if not r13_has("wf_fire"):
        return
    call r13_scene("ep_woodshed_ruin","6일 아침 · 장작 창고 터","quiet")
    if r13_has("kkomi_dead"):
        call r13_lines([(None,"창고는 검은 기둥 몇 개만 남았다. 눈이 녹아 시커먼 물이 고였다."),
            (None,"다람이 담요 넷이 깔려 있던 자리 앞에 쪼그려 앉았다. 재 사이에서 작고 둥근 것을 집어 들었다."),
            (None,"도토리였다. 한쪽이 까맣게 그을려 있었다."),
            ("daram","……꼬미야."),
            (None,"……"),
            ("daram","아빠. 이거 대장 표시야. 내가 준 거야. 꼬미가 끝까지 갖고 있었어."),
            ("daram","다음엔 나도 오기로 했는데.")],"wf:morning:acorn")
    else:
        call r13_lines([(None,"창고는 검은 기둥 몇 개만 남았다."),
            ("kid_kkomi","우리 집 다 탔어. ……근데 대장은 표시 안 잃어버렸다."),
            (None,"꼬미가 그을리지 않은 도토리를 내밀었다.")],"wf:morning:alive")
    $ r13_edit(location="square")
    call r13_scene("winter_square","6일 아침 · 광장","search")
    call r13_lines([(None,"보리가 손이 묶인 채 광장 돌 앞에 앉아 있었다. 등에는 아직 장작 지게. 손에는 아무렇게나 감은 천."),
        ("neoul","이 자가 밤마다 학교 장작 창고에서 장작을 훔쳤소. 어젯밤에도 거기 있었소."),
        ("resident_ppul","도둑이 불까지 냈구려."+(" 표 없는 애 하나가 죽었다지." if r13_has("kkomi_dead") else "")),
        ("resident_ppul","회의는 내일 학교에서 하겠소. 그때까지 범인이 바뀌지 않으면 보리를 내보내겠소."),
        ("resident_bori","장작 훔친 건 맞다! 대피소 우리 애가 열이 나서, 몇 개씩…… 그래도 불은 내가 안 냈어!")]+
        ([("resident_bori","애 셋 꺼낸 게 나라고! 하나는…… 하나는 못 꺼냈어.")] if r13_has("kkomi_dead") else []),"wf:morning:square")
    menu:
        "보리의 손을 본다":
            call r13_lines([(None,"천을 걷어 보니 두 손바닥이 벌겋게 데어 있었다. 손등은 멀쩡했다."),
                ("dad","(두 손바닥만 데었고 손등은 멀쩡하다. 불씨를 놓다 덴 손일까, 뜨거운 것을 꽉 쥐었던 손일까?)",{"thought":True})],"wf:morning:hands")
            $ r13_grant(["F04"],"광장에서 직접 본 보리의 손")
            $ r13_flag("wf_bori_trusted")
        "“증거도 없이 내보낼 겁니까?”":
            call r13_lines([("neoul","그럼 내일까지 증거를 가져오시오.")],"wf:morning:demand")
            $ r13_flag("wf_bori_trusted")
        "“불을 냈을 수도 있겠군요.”":
            call r13_lines([("resident_bori","……당신도 똑같구먼."),(None,"보리가 고개를 돌렸다.")],"wf:morning:doubt")
            $ r13_flag("wf_bori_closed")
    return

label r13_wf_nabi_blame:
    $ r13_flag("wf_nabi_blame")
    call r13_scene("kitchen","여관 1층 · 주방","quiet")
    call r13_lines([(None,"주방은 불이 꺼져 있었다. 나비가 빈 그릇 넷 앞에 주저앉아 있었다."),
        ("nabi","제 등잔이에요. 제가 켜 두고 왔어요. 깜깜하면 무섭다고 해서……")]+
        ([("nabi","제가 꼬미를 죽였어요.")] if r13_has("kkomi_dead") else [])+
        [("granny","(들어오며) 여관 등잔을 표 없는 애들한테 갖다줬다고? 그 불이 그 등잔에서 났다면, 여관이 물어내야 할 거다."),
        ("granny","내일 아침까지 짐 싸거라. 아니면 이번 달 품삯은 없다."),
        ("nabi","……네, 할머니.")],"wf:nabi")
    menu:
        "“잘 때 뚜껑을 닫으라고 했니?”":
            call r13_lines([("nabi","……네. 꼬미는 꼭 닫았어요. 맨날요. 근데 어젯밤엔 모르잖아요.")],"wf:nabi:lid")
            if not r13_has("F03"):
                $ r13_grant(["F03"],"나비에게 들은 등잔 이야기")
        "“나비 잘못이 아닐 수도 있습니다.”":
            call r13_lines([("granny","그럼 증거를 가져오세요. 내일 아침까지요.")],"wf:nabi:defend")
    $ r13_tick()
    return

label r13_wf_ruins:
    $ r13_flag("wf_ruins")
    call r13_scene("ep_woodshed_ruin","6일 · 장작 창고 터","search")
    call r13_lines([(None,"타고 남은 창고 터. 어디부터 볼까.")],"wf:ruins")
    $ _wf_left=["inside","door","snow"]
    while _wf_left:
        $ _wf_menu=[("어디를 볼까?",None)]+[(t,k) for k,t in (("inside","안쪽 구석을 본다"),("door","문을 본다"),("snow","문 앞 눈을 본다")) if k in _wf_left]+[("이제 학교로 간다","done")]
        $ _wf_pick=renpy.display_menu(_wf_menu)
        if _wf_pick=="done":
            $ _wf_left=[]
        else:
            $ _wf_left.remove(_wf_pick)
            if _wf_pick=="inside":
                call r13_lines([(None,"담요 자리보다 더 안쪽, 쓰러진 장작 밑에서 작은 등잔이 나왔다. 그을렸지만 깨지지 않았다."),
                    (None,"뚜껑이 꼭 닫혀 있었다. 흔들어 보니 안에 기름이 그대로 찰랑였다."),
                    ("dad","(뚜껑은 닫혔고 기름은 그대로다. 그 밤 이 등잔이 켜져 있었을까?)",{"thought":True})],"wf:ruins:inside")
                $ r13_grant(["F05"],"창고 터 안쪽 구석에서 찾은 등잔")
            elif _wf_pick=="door":
                call r13_lines([(None,"문틀이 숯처럼 새까맸다. 그런데 안쪽 장작더미는 겉만 그을렸다."),
                    ("dad","(안에서 불이 났다면 안쪽이 제일 많이 탔을 텐데, 숯이 된 건 문틀이다. 불은 어디서 시작됐을까?)",{"thought":True})],"wf:ruins:door")
                $ r13_grant(["F06"],"창고 터 문틀을 직접 봄")
            else:
                call r13_lines([(None,"문 앞 눈이 녹아 웅덩이가 져 있었다. 물 위에 무지개 같은 기름막. 코를 대자 독한 냄새가 났다."),
                    ("dad","(등잔 기름 냄새가 아니다. 솥에 쓰는 독한 등유 냄새다. 왜 창고 문 앞 눈에 등유가 고여 있을까?)",{"thought":True})],"wf:ruins:snow")
                $ r13_grant(["F07"],"창고 문 앞 눈을 직접 봄")
    if r13_has("F07") and r13_has("F02"):
        call r13_lines([("dad","(빨래터 솥 옆 기름통도 등유였다. 그 통은 지금도 뚜껑까지 꽉 차 있을까?)",{"thought":True})],"wf:ruins:sum")
    elif r13_has("F07"):
        call r13_lines([("dad","(문 앞의 등유는 어디서 왔을까? 이 마을에서 등유를 통째로 쓰는 곳이 있을까?)",{"thought":True})],"wf:ruins:sum")
    elif r13_has("F06"):
        call r13_lines([("dad","(불이 문 쪽에서 났다면, 무엇이 문 앞에서 불을 키웠을까? 문 앞 눈도 봐야 할까?)",{"thought":True})],"wf:ruins:sum")
    call r13_scene("r13_school","학교 교실 · 난로 옆","quiet")
    if r13_has("wf_kkomi_alive"):
        call r13_lines([("kid_kkomi","우린 학교 돌창고에 있었어. 선생님이 우리 이름 불렀어. 넷 다."),
            ("resident_teacher","그 밤 아이들은 여기 있었어요. 제가 증인이에요.")],"wf:school:alive")
        $ r13_grant(["F14"],"사자 선생님의 말")
    else:
        call r13_lines([(None,"교실 난로 옆. 살아남은 아이 셋이 선생님 외투 하나를 같이 덮고 있었다."),
            (None,"사자 선생님이 낮은 목소리로 노래를 불렀다. 냄비를 젓는 시늉을 하는 노래였다. 아이들은 따라 부르지 않았다."),
            ("resident_teacher","수프 노래예요. 대피소에서 늘 부르는 거죠."),
            ("resident_teacher","이 애들 이름을 부르는 건 이제 나밖에 없어요. 깜이, 몽이, 방울."),
            ("kid_kkam","……곰 아저씨가 우리 살렸어. 문 쪽이 먼저 빨갰어. 문으로 못 나가서, 아저씨가 뒤에 벽을 부쉈어."),
            ("kid_mong","꼬미가 우리 다 깨웠어. 대장은 맨 나중에 나온다고 했어."),
            ("kid_bang","곰 아저씨 손 다 데었어. 아저씨 잡혀갔어?",{"expression":"anxious"})],"wf:school:kids")
        $ r13_grant(["F08"],"학교에서 살아남은 아이들에게 들은 말")
    $ r13_tick()
    return

label r13_wf_nubi:
    $ r13_flag("wf_nubi_seen")
    call r13_scene("ep_laundry","여관 뒤 빨래터","quiet")
    call r13_lines([(None,"솥 밑 불은 꺼져 있었다. 누비 아주머니가 손을 젖은 천으로 감은 채 빨래를 개고 있었다. 등에는 막내, 옆에는 아이 둘."),
        ("resident_nubi","손님…… 오늘은 빨래 못 받아요. 손을 좀 다쳐서요.")],"wf:nubi")
    $ _wf_left=["can","hand","kid"]
    while _wf_left:
        $ _wf_menu=[("무엇을 볼까?",None)]+[(t,k) for k,t in (("can","기름통을 본다"),("hand","손을 본다"),("kid","아이에게 묻는다")) if k in _wf_left]+[("이제 돌아간다","done")]
        $ _wf_pick=renpy.display_menu(_wf_menu)
        if _wf_pick=="done":
            $ _wf_left=[]
        else:
            $ _wf_left.remove(_wf_pick)
            if _wf_pick=="can":
                call r13_lines([(None,"솥 옆 기름통. 반쯤 비어 있었다.")]+
                    ([("dad","(엿들을 때는 뚜껑까지 꽉 차 있었다. 솥 밑 불은 그 뒤로 거의 안 땠다.)",{"thought":True})] if r13_has("F02") else [])+
                    [("resident_nubi","요즘 솥을 많이 데워서요……")],"wf:nubi:can")
                $ r13_grant(["F09"],"빨래터 기름통을 직접 봄")
            elif _wf_pick=="hand":
                call r13_lines([(None,"천 밑으로 손등이 보였다. 새로 덴 자리가 물집이 잡혀 있었다."),
                    ("resident_nubi","솥에 데었어요. 빨래하다 보면 늘 그래요."),
                    ("dad","(솥에 데었다면 손바닥이나 팔일 텐데, 물집은 손등에 있다. 무엇 앞에 손을 뻗다 데었을까?)",{"thought":True})],"wf:nubi:hand")
                $ r13_grant(["F10"],"누비의 손을 직접 봄")
            else:
                call r13_lines([("kid_nubi1","엄마가 어젯밤에 늦게 왔어. 우리 다 잘 때."),
                    ("kid_nubi1","엄마한테 빨래터 기름 냄새 났어. 엄마가 막 손 씻었어. 계속 씻었어."),
                    ("kid_nubi2","엄마, 이제 밥 많이 먹을 수 있어? 너울 아저씨가 그랬잖아."),
                    ("resident_nubi","(아이 입을 막는다) ……쉿.")],"wf:nubi:kid")
                $ r13_grant(["F11"],"빨래터에서 누비의 아이에게 들은 말")
    $ r13_tick()
    return

label r13_wf_choice:
    $ r13_flag("wf_choice_done")
    call r13_lines([("dad","(시간이 한 칸뿐이다. 나비를 감쌀지, 누비의 말을 들을지.)",{"thought":True})],"wf:choice")
    menu:
        "주방의 나비에게 간다":
            call r13_scene("kitchen","7일 아침 · 여관 주방","quiet")
            call r13_lines([(None,"나비가 작은 보따리를 싸고 있었다. 할머니가 팔짱을 끼고 서 있었다."),
                ("granny","그 등잔 값은 누가 물어요? 불은 그 등잔에서 났다면서요.")],"wf:choice:nabi")
            menu:
                "뚜껑 닫힌 등잔을 보여 준다" if r13_has("F05"):
                    call r13_lines([("dad","창고 안쪽 구석에서 나왔습니다. 뚜껑이 닫혀 있고, 기름도 그대로입니다. 불은 이 등잔에서 나지 않았습니다."),
                        ("nabi","……꼬미가 닫았어요. 약속대로."),
                        (None,"나비가 등잔을 두 손으로 감싸 쥐고 울었다. 처음으로 소리를 내서."),
                        ("granny","……등잔은 돌아왔으니 됐어요. 이번만은 넘어가지요. 품삯도 그대로 주고.")],"wf:choice:nabi:saved")
                    $ r13_flag("wf_nabi_defended","witness:nabi")
                "“그 아이 잘못이 아닙니다.”":
                    call r13_lines([("granny","증거도 없이 우리 집 일에 끼지 마세요."),
                        (None,"나비는 품삯을 잃고 주방 열쇠를 빼앗겼다.")],"wf:choice:nabi:lost")
                    $ r13_flag("wf_nabi_lost")
        "빨래터의 누비에게 간다":
            call r13_scene("ep_laundry","7일 아침 · 여관 뒤 빨래터","quiet")
            if sum(1 for k in ("F09","F10","F11") if r13_has(k))>=2:
                call r13_lines([("dad"," ".join([t for k,t in (("F07","창고 문 앞 눈에서 등유 냄새가 났습니다."),("F09","이 통은 반이나 줄었고요."),("F10","손등의 물집은 솥에 덴 자리가 아닌 것 같습니다."),("F11","아이가 그 밤 늦게 오셨다고 하더군요.")) if r13_has(k)])),
                    ("resident_nubi","(오래 말이 없다) ……불만 내려고 했어요."),
                    ("resident_nubi","문 앞에 조금만. 애들이 놀라서 나가면, 창고가 비면, 그럼 그 애들이 다른 데로 가면…… 그 몫이 우리 애들한테 온다고 했어요."),
                    ("resident_nubi","너울 님이 그랬어요. 그 애들 몫을 우리 집에 준다고."),
                    ("resident_nubi","그런데 바람이 바뀌었어요. 문 쪽으로 확, 불이 안으로……")]+
                    ([("resident_nubi","저는 도망쳤어요. 애가 안에 있다는 소리를 듣고도요.")] if r13_has("kkomi_dead") else []),"wf:choice:nubi")
                $ r13_grant(["F12"],"빨래터에서 누비에게 직접 들은 말")
            else:
                call r13_lines([("resident_nubi","……무슨 말씀이신지 모르겠어요. 빨래 일이 바빠서요."),
                    ("dad","(내가 본 것만으로는 누비 씨에게 아무것도 물을 수 없었다. 이 빨래터에서 무엇을 더 봐야 했을까?)",{"thought":True})],"wf:choice:nubi:closed")
    $ r13_tick()
    return

label r13_wf_meeting:
    call r13_scene("r13_school","학교 · 장작 창고의 불 회의","hearing")
    call r13_lines([(None,"교실 책상을 벽으로 밀어 두었다. 보리는 손이 묶인 채 앞에 서 있었다. 살아남은 아이들이 사자 선생님 뒤에 숨어 있었다."),
        (None,"사람들 틈에 누비 아주머니. 막내를 업고, 두 아이 손을 잡고 있었다. 나비는 문가에 서 있었다.")]+
        ([("neoul","표 없는 아이 하나가 불에 타 죽었소. 오늘 끝냅시다."),("daram","(작게) 이름 있어. 꼬미야.")] if r13_has("kkomi_dead") else
        [("neoul","장작 창고가 탔소. 오늘 끝냅시다.")]),"wf:meeting:open")
    call r13_debate_run("Q3")
    if _return:
        call r13_wf_decision
    else:
        call r13_lines([("neoul","증거가 모자라오. 보리는 내보내겠소."),
            (None,"보리가 끌려가며 학교 쪽을 돌아보았다. 아이들이 창문에 붙어 있었다.")],"wf:meeting:fail")
        $ r13_flag("bori_taken","wf_done","wf_second_fire")
    call r13_wf_aftermath
    $ r13_tick()
    return None

label r13_wf_decision:
    $ r13_flag("wf_bori_freed","bori_ally","wf_done","wf_solved")
    $ _wf_menu=[("누비를 어떻게 할까?",None),("누비를 데려가게 둔다","hand")]
    if r13_has("F01") or r13_has("F12"):
        $ _wf_menu.append(("너울의 약속을 내놓는다","expose"))
    $ _wf_menu.append(("누비를 감싸고 아이들을 학교에","shelter"))
    if r13_has("wf_overheard") and r13_has("wf_nabi_defended"):
        $ _wf_menu.append(("“약속은 여기서 끝냅니다.”","perfect"))
    $ _wf_pick=renpy.display_menu(_wf_menu)
    if _wf_pick=="hand":
        call r13_lines([(None,"너울이 누비의 팔을 잡았다. 누비의 큰아이가 업힌 막내를 받아 안았다. 아이 셋이 빈 빨래터 쪽으로 걸어갔다."),
            ("dad","(저 아이들은 누가 먹이나.)",{"thought":True})],"wf:decision:hand")
        $ r13_flag("nubi_taken","wf_nubi_kids_alone")
    elif _wf_pick=="expose":
        if r13_has("F01"):
            call r13_lines([("dad","누비 씨를 민 건 '그 애들이 줄면 몫을 주겠다'는 말입니다. 빨래터에서 제가 직접 들었습니다."),
                (None,"사람들이 너울을 보았다. 너울의 얼굴이 굳었다."),
                ("neoul","……외지 사람이 오래 머물 생각이 없나 보오.")],"wf:decision:expose")
            $ r13_flag("neoul_exposed","neoul_enemy")
        else:
            call r13_lines([("dad","누비 씨는 너울 님의 약속 때문이라고 했습니다."),
                ("neoul","저 여자 말뿐이오."),
                (None,"사람들 절반은 너울을 보고, 절반은 누비를 보았다.")],"wf:decision:expose_half")
            $ r13_flag("neoul_half","neoul_enemy","wf_second_fire")
        $ r13_flag("nubi_taken","wf_nubi_kids_alone")
    elif _wf_pick=="shelter":
        call r13_lines([("dad","누비네 아이도, 창고 아이들도 학교에서 겨울을 나게 해 주십시오."),
            ("resident_teacher","제가 모두 맡지요. 이름은 제가 부르겠어요."),
            (None,"누비는 집으로 돌아갔다. 너울은 아무 말도 하지 않았다.")],"wf:decision:shelter")
        $ r13_flag("wf_kids_school","kids_school","wf_second_fire")
    else:
        call r13_lines([("dad","약속은 여기서 끝냅니다. 누비 씨는 창고를 다시 짓는 일로 갚고, 그 집 아이 셋은 나비가 부엌에서 맡습니다."),
            (None,"사람들의 눈이 너울에게 쏠렸다. 너울이 한 걸음 물러섰다."),
            ("nabi","제가 할게요. 할머니한텐 제가 말해요."),
            (None,"누비가 막내를 끌어안고 고개를 숙였다.")],"wf:decision:perfect")
        $ r13_flag("wf_perfect","nubi_kids_with_nabi","neoul_exposed")
    return

label r13_wf_aftermath:
    call r13_scene("ep_woodshed_ruin","%d일 %s · 아지트 터"%(room13["day"],("아침","오후","저녁","밤")[min(3,room13["period"])]),"quiet")
    if r13_has("kkomi_dead"):
        call r13_lines([(None,"타고 남은 창고 터. 다람이 장갑 낀 손으로 언 땅을 팠다. 잘 안 파졌다.")]+
            ([(None,"보리가 붕대 감은 손으로 옆에서 같이 팠다.")] if r13_has("wf_bori_freed") else [])+
            [("daram","여기 꼬미 아지트야. 비밀이었는데, 이제 다 알아."),
            ("daram","(그을린 도토리를 넣는다) 대장 표시는 아지트에 있어야 돼."),
            ("daram","꼬미야. 나 왔어. 다음엔 온다고 했잖아."),
            (None,"……")]+
            ([("resident_bori","……봄 되면 싹 나겠다."),("daram","진짜?"),("resident_bori","몰라. 그냥 그랬으면 좋겠다고.")] if r13_has("wf_bori_freed") else []),"wf:after:bury")
        $ r13_flag("acorn_buried")
    else:
        call r13_lines([("kid_kkomi","대장 표시는 탐정단 단장이 갖고 있어. 아지트 새로 지으면 돌려줘."),
            (None,"꼬미가 도토리를 다람 손에 다시 쥐여 주었다.")],"wf:after:return")
    if r13_has("wf_bori_freed") and r13_has("wf_bori_trusted") and r13_has("kkomi_dead"):
        call r13_lines([(None,"살아남은 아이 셋이 보리 다리에 붙어 있었다. 보리는 데인 손을 어디 둘지 몰라 했다."),
            ("resident_bori","우리 집 좁다. 시끄럽고, 장작도 모자라. ……그래도 오든가."),
            ("kid_kkam","아저씨네 애도 있어?"),
            ("resident_bori","있어. 대피소에 맡겨 놨어. 열이 나서. 낫으면 같이 살자.")],"wf:after:bori")
        $ r13_flag("bori_adopts")
    call r13_lines([(None,"(그림책) 그레텔이 마녀를 힘껏 밀었고,",{"book":"U03-opening"}),
        (None,"(그림책) 마녀도 집에 배고픈 아이가 셋 있었어요.",{"book":"U03-ending"})]+
        ([(None,"(그림책) 그날 밤 화덕은 비어 있었어요.")] if not r13_has("kkomi_dead") else [])+
        [("daram","……아빠. 그럼 그레텔이 나쁜 거야? 마녀가 나쁜 거야?"),
        ("daram","마녀네 애들은 이제 누가 밥 줘?")]+
        ([("dad","나비 언니가."),("daram","……그럼 다행이다.")] if r13_has("nubi_kids_with_nabi") else [("dad","……")]),"wf:after:book")
    return

label r13_wf_missed:
    $ r13_flag("wf_done","bori_taken","wf_second_fire","wf_missed")
    call r13_lines([(None,"학교 회의는 끝났다고 했다. 보리가 장작 도둑이자 불을 낸 사람으로 끌려갔다."),
        ("dad","(그 회의에 갔어야 했다.)",{"thought":True})],"wf:missed")
    return
