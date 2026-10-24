# New-world event rules that need more than text (owner-approved per event).
# Text for these paths lives in game/v111/newworld/dNN.json.
init 318 python:
    # Event 01 gate (plan A, 2026-10-21): one presentation. A half presentation
    # (application only) gets one more try; any other wrong answer is final and
    # Daram enters as '외 한 명' with no name on the record.
    R13_V111_ENTRY["MS14_D01_S04"]=([],{"gate_registered":False})
    def r13_nw_gate_entry_decided(previous=globals().get("R13_V111_SCENE_CHECKS",{}).get("MS14_D01_S04")):
        decided=r13_v111_value("gate_basis_proven") is True or r13_v111_value("gate_daram_unlisted") is True
        return decided and (previous is None or previous())
    if "R13_V111_SCENE_CHECKS" not in globals():R13_V111_SCENE_CHECKS={}
    R13_V111_SCENE_CHECKS["MS14_D01_S04"]=r13_nw_gate_entry_decided
    _r13_nw_rules_catalog_record=r13_catalog_record
    def r13_catalog_record(key):
        record=_r13_nw_rules_catalog_record(key)
        if record and r13_v111_active() and key=="V111:E05" and r13_v111_value("gate_daram_unlisted") is True:
            record=dict(record);record["establishes"]=R13_V111["evidence"]["E05"]["variants"]["unlisted"]
        return record

    # Meetings and the transfer list (plan 7). A meeting is decided once.
    R13_NW_MEETING_RESULTS=("win","partial","lose")
    def r13_nw_meeting_end(meeting,result):
        if result not in R13_NW_MEETING_RESULTS:raise Exception("Unknown meeting result: "+str(result))
        if r13_v111_value("meeting:"+meeting) is None:
            r13_v111_set("meeting:"+meeting,result)
            if "r13_fork_record" in globals():r13_fork_record(meeting,result)
        return r13_v111_value("meeting:"+meeting)
    R13_NW_LISTABLE=("resident_tok","bami","resident_bori","nabi","daram","resident_owlgp","resident_piko","resident_siluk","resident_guldol","resident_teacher","mom","dad")
    def r13_nw_list(person,reason):
        """Write a name on the school transfer list (the 13th cart takes them)."""
        if person not in R13_NW_LISTABLE:raise Exception("Person cannot be listed: "+str(person))
        if r13_v111_value("listed:"+person):return False
        r13_v111_set("listed:"+person,True)
        r13_v111_set("listed_reason:"+person,reason)
        r13_v111_set("listed_order",list(r13_v111_value("listed_order") or [])+[person])
        return True
    def r13_nw_listed():
        return [p for p in (r13_v111_value("listed_order") or []) if r13_v111_value("listed:"+p)]
    def r13_nw_roster_lines():
        """0.20.7 (ending review 10): before the 13th's last argument, the list as already known.
        Facts only (no outcome, no hint): each name ever written and where it stands now."""
        rows=[]
        for p in (r13_v111_value("listed_order") or []):
            if r13_v111_value("handed:"+p):state="데려옴"
            elif r13_v111_value("departed:"+p):state="수레로 떠남"
            elif r13_v111_value("listed:"+p):state="아직 명단에 있음"
            else:state="명단에서 빠짐"
            rows.append(R13_NAMES.get(p,p)+": "+state)
        if not rows:return []
        return [(None,"명단을 다시 펼쳤다. "+" · ".join(rows)+".")]

    # Event 03 lamp meeting: evening scene opens after a partial or lost meeting too.
    R13_V111_ENTRY["MS14_D03_S06"]=([],{"stone_choice_completed":True})
    def r13_nw_lamp_evening_ready(previous=R13_V111_SCENE_CHECKS.get("MS14_D03_S06")):
        decided=r13_v111_value("lamp_theft_supported") is True or r13_v111_value("meeting:lamp") in ("partial","lose")
        return decided and (previous is None or previous())
    R13_V111_SCENE_CHECKS["MS14_D03_S06"]=r13_nw_lamp_evening_ready

    # Proof scope (owner 2026-10-22, "다 추천안대로"): a proof passes when every needed
    # record is there. Related records on top are allowed (R13_PROOF_EXTRAS), and a
    # proof may have another complete set (R13_PROOF_ALTERNATES). The answers themselves
    # do not change; what was presented is kept as proof_given:<key> so the other side
    # can name the extra record in one line (conditions in room13_v111_newworld_text.rpy).
    R13_PROOF_EXTRAS={
        "함께 들어갈 근거를 고른다":("E01",),
        "수리와 반출을 가릴 자료를 낸다":("E10",),
        "밤이 혐의의 근거를 확인한다":("E21","NW_PIKO_SKETCH4"),
        # 2026-10-24 자료 재사용(EVIDENCE_CLUTTER_PLAN.md 2부, 소유자 "추천안대로"): 받을 때 쓸모없어 보이던
        # 자료를 정답 세트 위에 덧붙여도 받아 준다. 정답 세트는 그대로이고, 덧붙인 자료는 상대가 한 줄로 짚는다.
        "초롱과 피코의 하루를 대조한다":("E08","E28"),
        "요즘 돌이 어디서 오는지 대조한다":("E14",),
        # 2026-10-24 새 사실(새사실_시안.md 1번, 소유자 "추천안대로"): 초상 속 엄마는 바늘을 쥐고 있다. 2일에 다람이
        # 「손이 놀면 잠 온다」며 그렇게 주문했다. 피코는 엄마를 앞에 두고 그리지 않았으므로(2일 설명으로 그림)
        # 그날 손이 멀쩡했다는 증거는 못 된다. 그래서 대체 세트가 아니라 덧붙임으로만 받는다.
        "반송·필사본·초대 발송을 대조한다":("E07","E27","E09"),
        "아내가 봤다는 담요의 시점을 확인한다":("E35",),
        "촌장이 어젯밤 있던 곳을 확인한다":("E29",),
        "장부의 두 배를 실룩에게 보인다":("E34",),
        "맨 처음 이름을 짚는다":("NW_BURNT_PAGE",),
    }
    R13_PROOF_ALTERNATES={
        "구리선과 수선 출처를 대조한다":(("E08_CONTACT_ASSEMBLY","E09_PIN_OWNER"),),
        "초롱과 피코의 하루를 대조한다":(("E11","NW_PIKO_TREMOR"),),
        # 0.20.18 연쇄 P1 (소유자 2026-10-23 "전 사건에서 살린 애가 나중에 활용되어"): 2일에 살린 피코의
        # 그림이 겉옷 대조·귀가 진술을 대신한다. 그림은 얼굴이 아니라 키·소매·맨발만 보이므로 밤이를 벗길 뿐
        # 누가 물었는지는 정하지 않는다(회의 결론 불변).
        "밤이 혐의의 근거를 확인한다":(("E20","E22","NW_PIKO_SKETCH4"),("E20","E22","E23","NW_PIKO_SKETCH4"),("E20","E22","E24","NW_PIKO_SKETCH4")),
        # 2026-10-24 자료 재사용: 할머니의 「부인이 부탁했으면 대신 써 줄 수도」는 부탁이 있었느냐는 물음이다.
        # 5일 엄마의 경고 편지(E27, "그 편지는 내가 쓴 게 아니야")가 접수 묶음(E07)보다 그 물음에 직접 답한다.
        # 초대장(E01)과 발송 순서(E09_MAIL)는 그대로 있어야 한다. 회의 결론 불변.
        "반송·필사본·초대 발송을 대조한다":(("E01","E27","E09_MAIL"),),
    }
    # Shown title only; the proof key (and the saved argument slot) keeps the old name.
    R13_PROOF_TITLES={"첫 비명 뒤 핀을 다시 채운 때":"핀이 언제 떨어졌는가",
        # 0.20.6 (full play check: the old title pointed at 실룩's records): the claim is "only Tok opened it".
        "수리와 반출을 가릴 자료를 낸다":"톡이 고친 뒤에 등을 본 기록을 낸다"}
    # 0.20.6: which meeting's chances a proof uses (dev/test_proof_meetings.py re-derives this from the
    # wrong-answer labels). The proof screen shows them; a proof without a meeting shows none.
    R13_PROOF_MEETING={
        "함께 들어갈 근거를 고른다":"gate",
        "수리와 반출을 가릴 자료를 낸다":"lamp","돌과 매입 기록을 낸다":"lamp","바깥 걸쇠 주장과 발견 위치를 대조한다":"lamp","마지막 점검과 인수한 돌을 연결한다":"lamp",
        "밤이 혐의의 근거를 확인한다":"gate_post",
        "불이 시작된 곳과 진술을 대조한다":"fire","불의 원인과 빈 창고 진압을 구분한다":"fire","불의 원인과 아이 구조를 구분한다":"fire",
        "두 상처와 촛대 파손을 대조한다":"room13","두 번째 길을 실제 기록으로 보인다":"room13","구리선과 수선 출처를 대조한다":"room13",
        "첫 비명 뒤 핀을 다시 채운 때":"room13","접촉면과 아이의 위치를 대조한다":"room13",
        "수신인과 가족 전달 권한을 구분한다":"records","반송·필사본·초대 발송을 대조한다":"records",
        "초롱과 피코의 하루를 대조한다":"hypothesis","창고에서 잠자는 사람을 짚는다":"hypothesis","요즘 돌이 어디서 오는지 대조한다":"hypothesis",
        "아르카가 없는 아이들과 대조한다":"hypothesis","13호 난로의 돌을 내놓는다":"hypothesis",
        "재사용 설명과 개봉 봉인을 대조한다":"soup","파편·봉인·취급 구간을 함께 제시한다":"soup","명단과 흰 그릇을 대조한다":"soup",
        "아내가 봤다는 담요의 시점을 확인한다":"blanket","촌장이 어젯밤 있던 곳을 확인한다":"blanket",
        "장부의 두 배를 실룩에게 보인다":"piko","피코가 막혀야 했던 까닭을 보인다":"piko",
        "희생의 숫자와 장부를 대조한다":"altar","아르카가 부른다는 말과 옛 기록을 대조한다":"altar","쇠가 언제 붙었는지 보인다":"altar","맨 처음 이름을 짚는다":"altar"}
    def r13_v111_proof_chances(key):
        meeting=R13_PROOF_MEETING.get(key)
        if not meeting or r13_v111_value("meeting:"+meeting) is not None:return None
        most=r13_nw_tries_max(meeting)
        left=max(0,most-(r13_v111_value("tries:"+meeting) or 0))
        # 0.20.7 (play review days 2-3): a wrong answer now settles the meeting; say so.
        return "남은 기회 %d / %d"%(left,most)+(" · 이번이 마지막" if left==1 else "")
    def r13_v111_proof_sets(key,correct):
        return [set("V111:"+k for k in need) for need in [tuple(correct)]+list(R13_PROOF_ALTERNATES.get(key,()))]
    def r13_v111_proof_accepts(key,correct,given):
        # 2026-10-24 지시서 01: 정답 세트 하나를 다 갖추고, 나머지가 다른 정답 세트나 덧붙임에 든 자료뿐이면 받는다.
        # 예전에는 세트마다 따로 견줘서 13호 3번(구리선)의 두 세트를 함께 내면 틀렸고, 「맞는 근거는 남겨 두었다」를
        # 믿고 그대로 다시 내도 또 틀렸다. 두 세트는 같은 사실(핀 수선 출처)을 다른 쪽에서 짚을 뿐이라 함께 내도 맞다.
        given=set(given or ())
        sets=r13_v111_proof_sets(key,correct)
        allowed=set().union(*sets)|set("V111:"+k for k in R13_PROOF_EXTRAS.get(key,()))
        return any(need<=given for need in sets) and given<=allowed

    # 0.20.6 (owner day-1 play: "인정받은 부분을 남겨 두기"): after a wrong answer the records that
    # belong to an accepted set stay on the table; only the others are taken back. Chances and the
    # accepted sets do not change.
    def r13_v111_proof_kept(key,correct,given):
        sets=[set(correct)]+[set(a) for a in R13_PROOF_ALTERNATES.get(key,())]
        keep=set().union(*sets)
        # 2026-10-24 지시서 01 (소유자 결정 6 「전부 내기」 막기): 가진 자료를 다 내면 정답 쪽만 남아 다음 제출로
        # 풀렸다(회의 11개 중 8개). 덧붙임을 빼고 센 자료 수가 정답이 받아 줄 수 있는 수(모든 정답 세트의 합)보다
        # 많으면 아무것도 남기지 않는다. 상한은 화면에 보이지 않는다 — 보이면 정답 개수가 드러난다.
        extra=set(R13_PROOF_EXTRAS.get(key,()))
        counted=[k for k in (given or ()) if not (isinstance(k,str) and k.startswith("V111:") and k[5:] in extra)]
        if len(counted)>len(keep-extra):return []
        return [k for k in (given or ()) if isinstance(k,str) and k.startswith("V111:") and k[5:] in keep]

    # Half presentation (plan 7-2): some of the right records, none wrong.
    def r13_nw_half(correct):
        given=set(getattr(store,"v111_last_presented",None) or [])
        want=set("V111:"+k for k in correct)
        return bool(given) and given<want

    # Event 04 gate-post meeting: day 5 afternoon also follows a lost meeting.
    R13_V111_ENTRY["MS14_D05_S04"]=([],{})
    def r13_nw_gate_post_after(previous=R13_V111_SCENE_CHECKS.get("MS14_D05_S04")):
        return r13_v111_value("bami_status") in ("cleared","listed") and (previous is None or previous())
    R13_V111_SCENE_CHECKS["MS14_D05_S04"]=r13_nw_gate_post_after

    # Event 05 fire meeting: the school scene also follows a lost meeting (Bori blamed).
    def r13_nw_fire_school_ready(previous=R13_V111_SCENE_CHECKS.get("MS14_D07_S02")):
        return (previous is not None and previous()) or r13_v111_value("meeting:fire")=="lose"
    R13_V111_SCENE_CHECKS["MS14_D07_S02"]=r13_nw_fire_school_ready

    # Endings (plan 11-1). Checked on the 14th morning before the kept endings.
    # The five lives the frozen-village ending counts.
    R13_NW_LIVES=(("resident_piko","piko_alive"),("kid_kkomi","KKOMI_ALIVE"),("resident_owlgp","OWL_ALIVE"),("resident_nero","nero_alive"),("kid_dodam","alive:kid_dodam"))
    # 0.20.19 (소유자 2026-10-23 "나는 많이 죽었으면 해. 개입 안 하면 폭동이든", CRUEL_CHOICES.md D1~D4):
    # 폭동(너울·수레의 모모), 늦은 구조에 함께 묻힌 아랫길 노인도 죽음으로 센다.
    R13_NW_LIVES=R13_NW_LIVES+(("neoul","alive:neoul"),("resident_momo","alive:resident_momo"),("v111_lowerroad_elder","alive:v111_lowerroad_elder"))
    R13_NW_FROZEN_AT=4
    def r13_nw_is_dead(who,key):
        if r13_v111_value(key) is False:return True
        return who=="kid_dodam" and r13_v111_value("route12")=="late_exposure"
    def r13_nw_dead():
        dead=[who for who,key in R13_NW_LIVES if r13_nw_is_dead(who,key)]
        # D2: 13일 수레로 실려 간 사람은 돌아오지 못한다. 다람은 「남겨진 이름」이 따로 받는다.
        dead+=[p for p in (r13_v111_value("departed_names") or []) if p!="daram" and p not in dead]
        return dead
    def r13_nw_loss_count():
        return len(r13_nw_dead())
    def r13_nw_ending14():
        if r13_v111_value("departed:daram"):return "left_name"
        if r13_nw_loss_count()>=R13_NW_FROZEN_AT:return "frozen"
        outcome=r13_v111_value("outcome13")
        if outcome=="family_priority":return "family"
        if outcome=="partial_rescue":return "partial"
        if r13_v111_value("crowd_injury"):return "violence"
        return "morning"
    def r13_nw_true_ending_ready():
        """Plan 11-1 #6: all five alive, records/hypothesis/blanket/altar won, Neoul's ledger held."""
        if r13_v111_value("ending14")!="morning" or r13_nw_loss_count():return False
        if not r13_v111_owned("NW_NEOUL_LEDGER"):return False
        return all(r13_v111_value("meeting:"+m)=="win" for m in ("records","hypothesis","blanket","altar"))

    # Chances per meeting (owner 2026-10-22: three, then five "so the player can keep deducing").
    # A wrong answer shows the rebuttal and costs a chance; the wrong answer that uses the last chance stands.
    # 2026-10-24 소유자 결정 5 (docs/reviews/meeting-balance-20261024/기회수_분석.md 5장 B안): 같은 다섯 번이
    # 쟁점 하나짜리 회의는 너무 쉽게, 11일 가설(결정점 11자리)은 너무 어렵게 만들었다. 회의별 기회 = 쟁점 수 + 2
    # (최소 3), 11일 가설만 결정점 수 + 2 = 13. 표에 없는 회의는 예전 값 R13_NW_TRIES 를 쓴다.
    R13_NW_TRIES=5
    R13_NW_TRIES_BY_MEETING=dict(gate=3,gate_post=3,fire=4,records=4,blanket=4,piko=4,soup=5,altar=6,lamp=7,room13=7,hypothesis=13)
    def r13_nw_tries_max(meeting):
        return R13_NW_TRIES_BY_MEETING.get(meeting,R13_NW_TRIES)
    def r13_nw_tries_left(meeting):
        return max(0,r13_nw_tries_max(meeting)-(r13_v111_value("tries:"+meeting) or 0))
    def r13_nw_retry(meeting,correct=None,note=None):
        """True (and one chance used) when this wrong answer may be tried again."""
        if r13_v111_value("meeting:"+meeting) is not None:return False
        used=(r13_v111_value("tries:"+meeting) or 0)+1
        r13_v111_set("tries:"+meeting,used)
        left=r13_nw_tries_max(meeting)-used
        if left<=0:
            renpy.notify("잘못된 제출로 기회 1회 사용 · 남은 기회 0번.")
            r13_nw_wrong_queue(meeting,True)
            return False
        kept=bool((store.room13.get("arguments") or {}).get(getattr(store,"v111_claim",None) or ""))
        hint=note if (note and correct and r13_nw_half(correct)) else ("맞는 근거는 남겨 두었다." if kept else "맞지 않는다.")
        renpy.notify("기회 1회 사용 · 남은 기회 %d번. %s"%(left,hint))
        r13_nw_wrong_queue(meeting,False)
        return True

    # 2026-10-24 지시서 01 4번 (MEETING_RULES_V2.md 6장 1·2번, 소유자 「증거는 모였다는 걸 알려 주면 좋고」):
    # 틀린 뒤 반박을 듣고 나서 아빠 속말 한 줄. 같은 쟁점에서 틀린 횟수 1 / 2 / 3번째부터 문구가 다르다.
    # 쟁점별 문구는 아직 비어 있다(다음 지시서에서 채운다). 비어 있으면 기본 문구를 쓴다.
    # 자료 이름·정답은 넣지 않는다. 2번째는 상대 주장의 한 구절, 3번째부터는 자료의 종류까지만.
    #   형식: R13_NW_WRONG_THOUGHTS["<쟁점 키>"]={1:"...",2:"...",3:"..."}
    #   쟁점 키 = 증명 키(r13_v111_proof 의 첫 인자), 선택지 쟁점은 "menu:<이름>"(3일 칼 trial_knife, 11일 hyp0~hyp5).
    # 기회를 다 쓴 오답 뒤에는 회의마다 한 번 「다 있었다」 줄을 보인다.
    # 보이는 자리: 증명 화면에 다시 들어갈 때, 선택지 쟁점의 질문 앞(label r13_nw_wrong_thought),
    # 기회를 다 쓴 줄은 그 뒤 처음 나오는 대사 묶음 끝(r13_v111_lines·r13_nw_block 이 덧붙인다).
    R13_NW_WRONG_DEFAULT="근거는 다 손에 있다. 내가 엉뚱한 것끼리 묶었다."
    R13_NW_WRONG_FINAL="다 있었다. 그런데 이어 붙이지 못했다."
    R13_NW_WRONG_THOUGHTS={}
    def r13_nw_wrong_issue():
        claim=getattr(store,"v111_claim",None) or ""
        return claim[5:] if claim.startswith("v111:") else claim
    def r13_nw_wrong_text(issue,count):
        rows=R13_NW_WRONG_THOUGHTS.get(issue) or {}
        for n in range(min(max(1,count),3),0,-1):
            if rows.get(n):return rows[n]
        return R13_NW_WRONG_DEFAULT
    def r13_nw_wrong_queue(meeting,final):
        issue=r13_nw_wrong_issue()
        count=(r13_v111_value("wrong:"+issue) or 0)+1 if issue else 1
        if issue:r13_v111_set("wrong:"+issue,count)
        if final:
            if r13_v111_value("wrong_final:"+meeting):
                store.r13_nw_wrong_pending=None
                return
            r13_v111_set("wrong_final:"+meeting,True)
            store.r13_nw_wrong_pending=("final",R13_NW_WRONG_FINAL)
        else:
            store.r13_nw_wrong_pending=("try",r13_nw_wrong_text(issue,count))

    # Review 2026-10-22: a person who left on the cart (departed:<p>) is never placed again.
    _r13_nw_arrive=r13_v111_arrive
    def r13_v111_arrive(people):
        return _r13_nw_arrive([p for p in people if not r13_v111_value("departed:"+p)])
    def r13_v111_join(people):
        """Someone who speaks walks into the scene already on stage (same filters as arrive)."""
        r13_v111_arrive(list(store.room13["v111"].get("people") or [])+list(people))
    _r13_nw_binding=r13_v111_binding
    def r13_v111_binding():
        b=_r13_nw_binding()
        if b.get("people"):b=dict(b,people=[p for p in b["people"] if not r13_v111_value("departed:"+p)])
        return b
