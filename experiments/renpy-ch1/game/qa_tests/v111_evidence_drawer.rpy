# 2026-10-24 증거 서랍(소유자 "추천안대로", 시안 docs/reviews/evidence-drawer-20261024/).
# 14일 상태: 자료 81장을 원래 얻는 날·자리에서 받고, 제단 회의 앞 열 회의가 끝났다.
# 기록 화면의 이번 사건 / 지난 사건 / 사람별, 쪽지 카드, 회의 근거 고르기에서 지난 사건 열기를 본다(PC·휴대폰).
init python:
    import os
    # 회의가 열리는 자리(갈림길 화면의 장소)를 그 사건 자료를 얻은 곳으로 쓴다. 꼬리표 모양만 보는 시험이다.
    QA_DRAWER_PLACE=dict(gate="gate",lamp="square",gate_post="gate",fire="v111_fire",room13="room13",records="room13",
        hypothesis="school",soup="dining",blanket="square",piko="square",altar="altar")
    def qa_drawer_site_key(base):
        site=R13_DRAWER["sites"][base][0]
        return (R13_DRAWER_SCENE_INDEX.get(site[0],999),site[2])
    def qa_drawer_day14():
        bases=sorted(R13_DRAWER["sites"],key=qa_drawer_site_key)
        for base in bases:
            site=R13_DRAWER["sites"][base][0]
            day=R13_V111["scene_days"][site[0]]
            r13_edit(day=day,period=(3 if base=="NW_BURNT_PAGE" else 1),location=("kitchen" if base=="NW_BURNT_PAGE" else "school"))
            # 사건 자리는 받은 날·출처로 다시 찾는다. 장소는 그 사건 회의 자리로 둔다.
            source=(site[0]+"_L0000") if site[2]<0 else ("nw:acquire:"+base)
            r13_grant(["V111:"+base],source)
            case=r13_drawer_case_of("V111:"+base)
            if base!="NW_BURNT_PAGE":
                n=winter_copy.deepcopy(store.room13);n["records"]["V111:"+base]["place"]=QA_DRAWER_PLACE.get(case,"school");store.room13=n
        for meeting in r13_drawer_meetings():
            if meeting!="altar":r13_v111_set("meeting:"+meeting,"win")
        r13_v111_set("day",14)
        r13_edit(day=14,location="school",period=1)
    def qa_drawer_scope(name="r13_records"):
        return renpy.get_screen(name).scope
    def qa_drawer_log(text):
        with open(os.path.join(config.basedir,"qa_result.txt"),"a",encoding="utf-8") as out:out.write(text+"\n")
    def qa_drawer_legacy_ok():
        """v111 이 꺼진 판: 서랍·꼬리표·쪽지가 모두 꺼지고 옛 「지난 사건」 묶음 경로가 그대로 쓰인다."""
        global r13_v111_active
        real=r13_v111_active
        r13_v111_active=lambda:False
        try:
            return (not r13_drawer_active() and r13_drawer_tag("V111:E01")=="" and r13_drawer_folded()=={}
                and r13_catalog_entries(shelf=True)==[])
        finally:
            r13_v111_active=real
    def qa_drawer_dump():
        entries=r13_catalog_entries()
        qa_drawer_log("이번 사건 %d개: %s"%(len(r13_drawer_now(entries)),", ".join(r13_catalog_title(k) for k in r13_drawer_now(entries))))
        for case,keys in r13_drawer_cases(entries):
            qa_drawer_log("%s  %d개: %s"%(r13_drawer_case_title(case),len(keys),", ".join(r13_catalog_title(k) for k in keys)))
        qa_drawer_log("쪽지: %s"%", ".join("%s→%s"%(r13_catalog_title(n),r13_catalog_title(b)) for n,b in sorted(r13_drawer_folded().items())))
        qa_drawer_log("사람별: %s"%", ".join("%s %d"%(R13_NAMES[p],len(k)) for p,k in r13_drawer_people(entries)))

testcase v111_evidence_drawer:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_drawer_day14)
    pause 0.5
    $ qa_drawer_entries=r13_catalog_entries()
    run Function(qa_drawer_dump)
    # 81장 전부 받았고, 쪽지 여섯 장은 목록에서 빠지며, 나머지는 이번 사건이나 지난 사건 한 곳에만 있다.
    assert eval (len([k for k in room13["evidence"] if k.startswith("V111:")])==81)
    assert eval (sorted(r13_drawer_folded())==sorted("V111:"+k for k in ("E26","E19","E05","E30","E10_PUMP","E08_RECENT_LETTER")))
    assert eval (sorted(r13_drawer_notes("V111:E21"))==["V111:E19","V111:E26"])
    # 두 배 장부(⑩)와 맡긴 기록(⑥) 회의는 자기 사건에서 새로 얻는 자료가 없어(뒤 자료는 다음 사건으로) 묶음이 비고, 목록에 나오지 않는다.
    assert eval ([c for c,_ in r13_drawer_cases(qa_drawer_entries)]==["blanket","soup","hypothesis","room13","fire","gate_post","lamp","gate"])
    assert eval (len(r13_drawer_now(qa_drawer_entries))+sum(len(k) for _,k in r13_drawer_cases(qa_drawer_entries))==len(qa_drawer_entries)-6)
    # 제단 회의 정답과 쓰일 자료는 이번 사건에 있다(얻은 자리가 두 배 장부 회의 뒤인 너울의 장부 포함).
    assert eval (all("V111:"+k in r13_drawer_now(qa_drawer_entries) for k in ("NW_NEOUL_LEDGER","NW_TABLET_B","NW_IRON_MARK","NW_BURNT_PAGE","NW_MADAM_DAY7")))
    # 대화·회의에서 꺼내는 자료는 접지 않는다.
    assert eval (all("V111:"+k in r13_drawer_visible(qa_drawer_entries) for k in ("E13_HANDOVER","E14_SUPPLY","E13_ORDER")))
    # 옛 저장(출처·장소 기록이 없고 날만 있음)에서도 같은 사건에 묶인다.
    $ qa_drawer_cases_before=dict((k,r13_drawer_case_of(k)) for k in qa_drawer_entries)
    $ qa_drawer_saved=winter_copy.deepcopy(room13)
    $ room13["records"]=dict((k,dict(day=v.get("day"))) for k,v in room13["records"].items())
    assert eval (all(r13_drawer_case_of(k)==qa_drawer_cases_before[k] for k in qa_drawer_entries))
    assert eval (r13_drawer_tag("V111:E21")=="4일")
    $ room13["records"]={}
    assert eval (r13_drawer_case_of("V111:E01")=="gate" and r13_drawer_tag("V111:E01")=="1일")
    $ room13=qa_drawer_saved
    run Function(qa_drawer_dump)
    # PC: 기록 · 이번 사건
    $ r13_touch_ui=lambda: False
    $ r13_records_view={"tab":"all","detail":"V111:NW_BURNT_PAGE","page":0}
    run Show("r13_records")
    pause 1.2
    screenshot "drawer-01-now-pc.png"
    # 지난 사건: 칩을 눌러 연다. 가장 최근에 끝난 사건이 먼저 고른 상태다.
    click "지난 사건"
    pause 0.8
    assert eval (qa_drawer_scope()["drawer"]=="past" and qa_drawer_scope()["detail"] is None)
    click "⑨ 담요의 새 · 13일"
    pause 0.8
    screenshot "drawer-02-past-pc.png"
    # 고른 사건의 카드를 누르면 기존 상세로. 왼쪽 첫 줄은 사건 목록으로 돌아가는 칸.
    click "회관 창 안의 촌장과 바둑이"
    pause 1.0
    assert eval (qa_drawer_scope()["detail"]=="V111:NW_HALL_WINDOW")
    screenshot "drawer-03-past-detail-pc.png"
    click "‹ 지난 사건 목록"
    pause 0.6
    assert eval (qa_drawer_scope()["detail"] is None and qa_drawer_scope()["drawer_case"]=="blanket")
    # 쪽지 카드: 밤이의 그날 밤 목격(③ 밤이의 혐의)에 정정 기록과 제한된 목격이 쪽지로 붙는다.
    # ③은 둘째 쪽에 있다(최근 사건부터 다섯 장씩).
    click id "r13_dr_gnext"
    pause 0.4
    click "③ 밤이의 혐의 · 5일"
    pause 0.6
    screenshot "drawer-04-past-gatepost-pc.png"
    click "밤이의 그날 밤 목격"
    pause 1.0
    screenshot "drawer-05-note-detail-pc.png"
    # 사람별
    click "사람별"
    pause 0.8
    screenshot "drawer-06-person-pc.png"
    run Hide("r13_records")
    pause 0.4
    # 회의 근거 고르기(실제 보여주기 화면): 이번 사건이 먼저, 지난 사건을 열어 고를 수 있다.
    $ renpy.display.screen.screens[("r13_book",None)] = MS14_QA_REAL_BOOK
    run Show("r13_book",target="dad",present=True,purpose="proof",chosen=[])
    pause 1.2
    screenshot "drawer-07-proof-now-pc.png"
    click "지난 사건"
    pause 0.8
    screenshot "drawer-08-proof-past-pc.png"
    click "⑩ 두 배의 장부 · 13일"
    pause 0.6
    click "너울의 장부"
    pause 1.0
    assert eval (qa_drawer_scope("r13_book")["drawer"]=="past")
    click "백 부인의 매입 장부"
    pause 1.0
    screenshot "drawer-09-proof-past-pick-pc.png"
    run Hide("r13_book")
    pause 0.4
    # 휴대폰(터치 영역 88px 줄)
    $ r13_touch_ui=lambda: True
    $ r13_records_view={"tab":"all","detail":"V111:NW_BURNT_PAGE","page":0,"drawer":"now"}
    run Show("r13_records")
    pause 1.2
    screenshot "drawer-11-now-touch.png"
    $ qa_drawer_scope()["drawer"]="past"
    $ qa_drawer_scope()["detail"]=None
    pause 0.8
    screenshot "drawer-12-past-touch.png"
    $ qa_drawer_scope()["drawer_case"]="gate_post"
    $ qa_drawer_scope()["detail"]="V111:E21"
    $ qa_drawer_scope()["page"]=0
    pause 1.0
    screenshot "drawer-13-note-detail-touch.png"
    $ qa_drawer_scope()["drawer"]="person"
    $ qa_drawer_scope()["detail"]=None
    pause 0.8
    screenshot "drawer-14-person-touch.png"
    run Hide("r13_records")
    pause 0.4
    run Show("r13_book",target="dad",present=True,purpose="proof",chosen=[])
    pause 1.0
    $ qa_drawer_scope("r13_book")["drawer"]="past"
    pause 0.8
    screenshot "drawer-15-proof-past-touch.png"
    run Hide("r13_book")
    $ r13_touch_ui=lambda: False
    pause 0.4
    run Function(qa_drawer_log,"PASS v111_evidence_drawer")

# 옛 이야기(v111 아님)는 예전 「지난 사건」 묶음 그대로: 서랍이 켜지지 않는다.
testcase v111_evidence_drawer_legacy:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval qa_drawer_legacy_ok()
    assert eval r13_drawer_active()
    run Function(qa_drawer_log,"PASS v111_evidence_drawer_legacy")
