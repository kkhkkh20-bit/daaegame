# New-world systems (2026-10-21 plan, chapters 7, 8 and 11).
# Data and rules only: one-shot meetings, issue results, the transfer list,
# money (nyang), the thief rule, deaths and the ending order.
# Every value lives in room13["v111"]["values"] through r13_v111_set, so saves,
# rollback and the existing V1.1.1 story keep one state.
# No screen is added here. The notebook purse line and the branch screen wait
# for approved image drafts (CLAUDE.md design review rule).
init 318 python:
    # Issues in authored order. True marks a gate issue.
    # partial_min: fewest non-gate wins that still count as partial (else lose).
    # needs: an issue that stays closed when a listed earlier issue was lost.
    R13_NW_MEETINGS={
        "gate":dict(day=1,issues=[("applicants",True),("lodging",True),("correction",True)]),
        "lamp":dict(day=3,issues=[("tok_innocent",True),("knife_shard",False),("closed_words",False),("culprit_words",False)]),
        "gate_post":dict(day=5,issues=[("height",True),("kongi_time",True),("grey_cloth",False),("shoes",False),("musoe",False)]),
        "fire":dict(day=7,issues=[("lamp_not_cause",True),("wood_location",True),("nubi_water",True),("three_faults",False)]),
        "room13":dict(day=10,issues=[("self_defense",True),("doto_door",True),("passage",True),("doto_staging",True),("nabi_alibi",True),("kitchen_alibi",False),("notebook_blow",False),("pin",False),("accident",False)]),
        "records":dict(day=10,issues=[("recipient",True),("old_mandate",True),("last_page",False)]),
        "hypothesis":dict(day=11,issues=[("pick",True),("chorong",False),("madam",False),("recent_years",False),("children",False),("witness",True)]),
        "soup":dict(day=12,issues=[("same_pot",True),("spoiled",True),("bottle",True),("sealed_words",True),("list_bowl",False)]),
        "blanket":dict(day=13,issues=[("chief_addendum",False),("blanket_time",True),("date_badook",False)]),
        "reinvestigation":dict(day=13,issues=[("double_and_painting",True)]),
        "altar":dict(day=14,issues=[("all_die",True),("altar_origin",False),("iron_when",False),("dallae",False)],partial_min=2),
    }
    R13_NW_RESULTS=("win","partial","lose")
    # People who can be written on the school transfer list (plan 7-6, 8-7).
    R13_NW_LISTABLE=("resident_tok","bami","resident_bori","nabi","daram","resident_owlgp","resident_piko","resident_siluk","resident_guldol","resident_teacher","mom","dad")
    # The five lives the frozen-village ending counts (plan 11-1).
    R13_NW_LIVES=(("resident_piko","piko_alive"),("kid_kkomi","KKOMI_ALIVE"),("resident_owlgp","OWL_ALIVE"),("resident_nero","nero_alive"),("kid_dodam","alive:kid_dodam"))
    R13_NW_FROZEN_AT=4
    R13_NW_THIEF_LIMIT=2

    def r13_nw_split(issue):
        meeting,name=issue.split(":",1)
        spec=R13_NW_MEETINGS.get(meeting)
        if spec is None or name not in [n for n,_ in spec["issues"]]:raise Exception("Unknown meeting issue: "+issue)
        return meeting,name
    def r13_nw_is_gate(issue):
        meeting,name=r13_nw_split(issue)
        return dict(R13_NW_MEETINGS[meeting]["issues"])[name]
    def r13_nw_issue(issue):
        r13_nw_split(issue)
        return r13_v111_value("issue:"+issue)
    def r13_nw_meeting(meeting):
        if meeting not in R13_NW_MEETINGS:raise Exception("Unknown meeting: "+meeting)
        return r13_v111_value("meeting:"+meeting)
    def r13_nw_issue_open(issue):
        meeting,name=r13_nw_split(issue)
        if r13_nw_meeting(meeting) is not None:return False
        if r13_nw_issue(issue) in ("won","lost"):return False
        needs=R13_NW_MEETINGS[meeting].get("needs",{}).get(name,())
        return not any(r13_nw_issue(meeting+":"+n)=="lost" for n in needs)
    def r13_nw_settle(issue,state):
        meeting,name=r13_nw_split(issue)
        if not r13_nw_issue_open(issue):
            raise Exception("Settled or closed issue cannot change: "+issue)
        r13_v111_set("issue:"+issue,state)
        # A lost gate ends the meeting on the spot (plan 7-3).
        if state=="lost" and r13_nw_is_gate(issue):r13_nw_meeting_close(meeting)
        return state
    def r13_nw_judge(issue,correct,given,partial=None):
        """One evidence presentation for one issue. Returns won, hardened, lost or empty.
        A wrong presentation settles the issue (plan 7-1). A listed half presentation
        hardens the opponent once and the issue stays open (plan 7-2)."""
        if not r13_nw_issue_open(issue):raise Exception("Issue is not open: "+issue)
        got=set(given or [])
        if not got:return "empty"
        if got==set("V111:"+k for k in correct):return r13_nw_settle(issue,"won")
        if r13_nw_issue(issue)!="hardened" and any(got==set("V111:"+k for k in p) for p in (partial or [])):
            r13_v111_set("issue:"+issue,"hardened")
            return "hardened"
        return r13_nw_settle(issue,"lost")
    def r13_nw_choose(issue,picked,correct):
        """Choice-only issue (hypothesis pick, the 'why' sentence). Also one shot."""
        if not r13_nw_issue_open(issue):raise Exception("Issue is not open: "+issue)
        return r13_nw_settle(issue,"won" if picked==correct else "lost")
    def r13_nw_result(meeting):
        spec=R13_NW_MEETINGS[meeting]
        states=[(gate,r13_nw_issue(meeting+":"+name)) for name,gate in spec["issues"]]
        if any(gate and state!="won" for gate,state in states):return "lose"
        if all(state=="won" for _,state in states):return "win"
        wins=sum(1 for gate,state in states if not gate and state=="won")
        if wins<spec.get("partial_min",0):return "lose"
        return "partial"
    def r13_nw_meeting_close(meeting):
        """Close once. Issues never reached are recorded as locked (not won)."""
        if r13_nw_meeting(meeting) is not None:return r13_nw_meeting(meeting)
        for name,_ in R13_NW_MEETINGS[meeting]["issues"]:
            if r13_nw_issue(meeting+":"+name) in (None,"hardened"):r13_v111_set("issue:"+meeting+":"+name,"locked")
        result=r13_nw_result(meeting)
        r13_v111_set("meeting:"+meeting,result)
        return result
    def r13_nw_first_lost(meeting):
        for name,_ in R13_NW_MEETINGS[meeting]["issues"]:
            if r13_nw_issue(meeting+":"+name)=="lost":return name
        return None

    # Transfer list (plan 7-6). Listed people still live their days; the 13th cart takes them.
    def r13_nw_list(person,reason):
        if person not in R13_NW_LISTABLE:raise Exception("Person cannot be listed: "+str(person))
        if r13_v111_value("listed:"+person):return False
        r13_v111_set("listed:"+person,True)
        r13_v111_set("listed_reason:"+person,reason)
        r13_v111_set("listed_order",list(r13_v111_value("listed_order") or [])+[person])
        if person=="daram":r13_v111_set("daram_wristband",True)
        return True
    def r13_nw_unlist(person):
        if not r13_v111_value("listed:"+person):return False
        if r13_v111_value("departed:"+person):raise Exception("Departed person cannot be unlisted: "+person)
        r13_v111_set("listed:"+person,False)
        r13_v111_set("listed_order",[p for p in (r13_v111_value("listed_order") or []) if p!=person])
        if person=="daram":r13_v111_set("daram_wristband",False)
        return True
    def r13_nw_listed():
        return [p for p in (r13_v111_value("listed_order") or []) if r13_v111_value("listed:"+p) and not r13_v111_value("departed:"+p) and r13_nw_alive(p)]
    def r13_nw_cart_departs(stopped):
        """The 13th cart leaves. Listed people not taken down go with it."""
        if r13_v111_value("cart13_departed"):return list(r13_v111_value("departed_order") or [])
        gone=[p for p in r13_nw_listed() if p not in stopped]
        for p in gone:r13_v111_set("departed:"+p,True)
        r13_v111_set("departed_order",gone)
        r13_v111_set("cart13_departed",True)
        return gone

    # Lives (plan 11-1, 8-2).
    def r13_nw_alive(person):
        for who,key in R13_NW_LIVES:
            if who==person:return not r13_nw_is_dead(who,key)
        return r13_v111_value("alive:"+person) is not False
    def r13_nw_is_dead(who,key):
        if r13_v111_value(key) is False:return True
        return who=="kid_dodam" and r13_v111_value("route12")=="late_exposure"
    def r13_nw_dead():
        return [who for who,key in R13_NW_LIVES if r13_nw_is_dead(who,key)]
    def r13_nw_loss_count():
        return len(r13_nw_dead())

    # Money (plan 8-3 to 8-9). Each event pays or costs once, so reloads and
    # repeated visits cannot farm wages.
    def r13_nw_nyang():
        return r13_v111_value("nyang") or 0
    def r13_nw_earn(event,amount):
        if amount<=0:raise Exception("Earn amount must be positive: "+event)
        marker="v111:nyang:earn:"+event
        if r13_has(marker):return False
        r13_v111_set("nyang",r13_nw_nyang()+amount)
        r13_flag(marker)
        return True
    def r13_nw_paid(event):
        return r13_has("v111:nyang:spend:"+event)
    def r13_nw_spend(event,amount):
        if amount<=0:raise Exception("Spend amount must be positive: "+event)
        marker="v111:nyang:spend:"+event
        if r13_has(marker):return True
        if r13_nw_nyang()<amount:return False
        r13_v111_set("nyang",r13_nw_nyang()-amount)
        r13_flag(marker)
        return True

    # The golden rule: a thief goes to the Arka (plan 8-7).
    def r13_nw_thief_mark():
        return r13_v111_value("thief_mark") or 0
    def r13_nw_steal(event):
        marker="v111:thief:"+event
        if r13_has(marker):return r13_nw_thief_mark()
        mark=min(R13_NW_THIEF_LIMIT,r13_nw_thief_mark()+1)
        r13_v111_set("thief_mark",mark)
        r13_flag(marker)
        if mark>=R13_NW_THIEF_LIMIT:r13_nw_list("dad","thief")
        return mark

    # Ending order (plan 11-1). Checked on the 14th morning, before the old dispatch.
    def r13_nw_ending14():
        if r13_v111_value("departed:daram"):return "left_name"
        if r13_v111_value("departed:dad"):return "left_name_dad"
        if r13_nw_loss_count()>=R13_NW_FROZEN_AT:return "frozen"
        outcome=r13_v111_value("outcome13")
        if outcome=="family_priority":return "family"
        if outcome in ("partial_rescue","departed"):return "partial"
        if r13_v111_value("crowd_injury"):return "violence"
        return "morning"
    def r13_nw_true_ending_ready():
        if r13_v111_value("ending14")!="morning" or r13_nw_loss_count():return False
        if not r13_v111_value("neoul_ledger_secured"):return False
        return all(r13_nw_meeting(m)=="win" for m in ("records","hypothesis","blanket","altar"))

    # Draft ending text (plan 11-2). Narration only, in the father's voice.
    # Owner review pending; art E01-E04 is requested in the 2026-10-21 resource request.
    R13_NW_ENDING_TEXT={
        "left_name":[
            "수레가 산길 굽이에서 보이지 않게 되었다. 다람은 끝까지 뒤를 보지 않았다. 손목의 명단 끈만 눈에 남았다.",
            "열나흘째 아침. 학교 교실에는 아내와 나뿐이었다. 누구도 먼저 말을 꺼내지 않았다.",
            "광장 이름판 앞에서 붓을 들었다. 확인된 이름만 적는다. 이 마을의 규칙이었다. 다람의 이름은 확인되지 않았다. 손이 빈칸 앞에서 멈췄다.",
            "밤. 접시에 과자가 하나 남았다. 다람 몫이었다. 부스러기도 없었다.",
            "아내가 말했다. \"치우지 마.\"",
            "첫 길이 열린 날, 까로의 마차에 둘이 탔다. 다람이 앉던 자리에는 짐을 두지 않았다.",
        ],
        "left_name_dad":[
            "수레가 움직였다. 학교 창가에 작은 빨간 모자가 보였다. 손을 들지 못했다. 손목에 묶인 끈이 무거웠다.",
            "도둑은 아르카 곁으로. 이 마을이 믿는 규칙이었고, 나는 그 규칙을 두 번 어겼다.",
            "다람은 아내의 손을 잡고 서 있었다. 울지 않았다. 대신 수첩에 무언가를 적었다.",
            "산길 굽이에서 마을이 보이지 않게 되었다. 수레 위 누구도 어디로 가는지 묻지 않았다.",
        ],
        "frozen":[
            "'돌 불을 끄자'는 말을 들어 줄 사람이 남지 않았다.",
            "광산 안쪽에서 마지막으로 캔 돌까지 등과 난로에 들어갔다. 광장의 아르카등은 하루에 하나씩 꺼졌다.",
            "열나흘째 아침, 이름판 앞. 이름을 읽던 {reader}가 읽다 말고 멈췄다. 자기가 무엇을 읽고 있었는지 잊은 얼굴이었다.",
            "주민들은 더 이상 날짜를 묻지 않았다. 묻는 법을 잊은 것이다.",
            "첫 길이 열린 날, 마을 입구. 돌목이 우리를 보았다. 알아보지 못했다. \"허가… 몇 명이오?\"",
            "다람이 또박또박 말했다. \"다람. 제 이름은 다람이에요.\"",
            "돌목은 붓을 쥔 채 오래 서 있었다. 끝내 받아 적지 못했다.",
            "다음 겨울에도 수레는 갈 것이다.",
        ],
        "frozen_family":"우리는 입구 옆 자리에서 멀리 그 모습을 바라보았다.",
        "true":[
            "그해 겨울, 마을은 학교에 모여 장작으로 지냈다. 광장 등에는 덮개를 씌웠다. 춥고 어두운 겨울이었다. 장작이 모자란 밤도 있었다.",
            "돌 불을 끄고 몇 주가 지났을 때, 날짜를 되묻던 이웃 하나가 오늘 날짜를 맞혔다. 이름을 잊은 사람은 돌아오지 않았다.",
            "돌등이 꺼진 골목에 기름등과 장작불이 드문드문 켜졌다. 광장 큰 돌 앞에서 기도하는 사람은 줄었다. 광산 입구에는 '닫음' 팻말이 걸렸다.",
            "첫 길이 열린 날, 까로의 마차. 짐 위에 피코가 완성한 초상이 실려 있었다.",
            "마차 안에서 아내가 지도를 펼쳤다. 이 마을 말고도 산골 마을 몇 곳에 표시가 있었다. 그 옆에는 옛 시설과 광산이, 몇 곳에는 '태움'이라는 글자가 적혀 있었다.",
            "다람이 물었다. \"저기도 돌로 불 켜?\"",
            "아내는 지도를 접지 않은 채 대답했다. \"여기만이 아닐지도 몰라.\"",
        ],
    }
    R13_NW_ENDING_TITLE={"left_name":"남겨진 이름","left_name_dad":"남겨진 이름","frozen":"얼어붙은 마을","true":"말을 위한 돌"}
    def r13_nw_ending_rows(kind):
        if kind=="frozen":
            reader="토실" if (r13_v111_value("departed:nabi") or not r13_nw_alive("nabi")) else "나비"
            rows=[t.replace("{reader}",reader) for t in R13_NW_ENDING_TEXT["frozen"]]
            if r13_v111_value("outcome13")=="family_priority":rows.insert(3,R13_NW_ENDING_TEXT["frozen_family"])
        else:
            rows=list(R13_NW_ENDING_TEXT[kind])
        return [(None,t) for t in rows]

label r13_nw_left_name_ending14:
    $ v111_nw_kind=r13_v111_value('ending14')
    $ r13_edit(period=0,location='school' if v111_nw_kind=='left_name' else 'square')
    $ room13["v111"]["people"]=[]
    call r13_scene(R13_PLACES[room13["location"]][1],R13_NW_ENDING_TITLE[v111_nw_kind],"quiet")
    call r13_lines(r13_nw_ending_rows(v111_nw_kind),'v111:nw:ending:'+v111_nw_kind)
    jump r13_nw_story_end14

label r13_nw_frozen_ending14:
    $ r13_edit(period=0,location='gate')
    $ room13["v111"]["people"]=[]
    call r13_scene(R13_PLACES['gate'][1],R13_NW_ENDING_TITLE['frozen'],"night")
    call r13_lines(r13_nw_ending_rows('frozen'),'v111:nw:ending:frozen')
    jump r13_nw_story_end14

label r13_nw_true_epilogue14:
    $ r13_v111_set('ending14','true')
    $ r13_edit(location='gate')
    $ room13["v111"]["people"]=[]
    call r13_scene(R13_PLACES['gate'][1],R13_NW_ENDING_TITLE['true'],"quiet")
    call r13_lines(r13_nw_ending_rows('true'),'v111:nw:ending:true')
    return

label r13_nw_story_end14:
    $ r13_v111_set('story14_completed',True)
    call screen r13_confirm("이야기를 마쳤습니다. 현재 진행을 저장할 수 있습니다.",yes="메인 화면으로",no="저장하기")
    if not _return:
        call screen save
    return
