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
            if r13_v111_value("handed:"+p) and r13_v111_value("void_down:"+p):state="무효 칸에서 내림"
            elif r13_v111_value("handed:"+p):state="데려옴"
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
        # 2026-10-24 대승리(GRAND_WIN_DESIGN.md 1-4·2-3, 결정 4): 엿들은 말(NW_LAUNDRY_TALK)과 1일 초소 명단(E02, 같은
        # 「처리 너울」)은 덧붙임으로만 받는다. 엿들은 말 혼자로는 약속을 입증하지 못한다(너울: 담 뒤에서 들은 말).
        "불의 원인과 빈 창고 진압을 구분한다":("NW_LAUNDRY_TALK","E02"),
        "불의 원인과 아이 구조를 구분한다":("NW_LAUNDRY_TALK","E02"),
        "명단과 흰 그릇을 대조한다":("NW_RETURNED_BOWL","NW_SICK_BEDS"),
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
        # 2026-10-24 대승리(GRAND_WIN_DESIGN.md 1-4, 결정 4): 누비의 진술(E07_NUBI)은 스스로 「약속은 입증 못 한다」고
        # 적혀 있다. 배급표의 덧붙인 줄(「창고가 비면 빨래터 누비네로. 처리 너울」)이 그 자리를 물건으로 메운다.
        # 기본 정답은 그대로이고, 이 표로 이기면(덧붙여 내도) 대승리 grand:fire 를 적는다(room13_v111_days610.rpy).
        "불의 원인과 빈 창고 진압을 구분한다":(("E06_FIRE","E06_EMPTY","NW_NUBI_TICKET"),),
        "불의 원인과 아이 구조를 구분한다":(("E06_FIRE","E06_RESCUE","NW_NUBI_TICKET"),),
        # 2026-10-24 대승리(GRAND_WIN_DESIGN.md 2-3, 결정 4): 빈 수레가 시설에서 돌려보낸 흰 그릇이 배식대의 흰 그릇과
        # 같다는 것이 「흰 그릇 = 실려 갈 사람 몫」을 명단 없이 보인다. 이 그릇으로 이기면 grand:soup.
        "명단과 흰 그릇을 대조한다":(("NW_WHITE_BOWLS","NW_RETURNED_BOWL"),),
        # 2026-10-25 결정 10(DECISIONS_20261024.md): 13일 피코 회의를 진 판에는 너울의 장부가 없다. 「회의는 언제나 깰 수
        # 있다」에 맞춰, 그 판에서도 늘 얻는 자료로 촌장의 「한 사람이 열흘을 산다」를 꺾는다 — 학교 장작 인수(E14_SUPPLY),
        # 돌 없이 등잔으로 지낸 창고 아이들(NW_KKOMI_NOSTONE), 꽃 표시가 큰 집 아이들에게만 붙은 침상 목록(NW_SICK_BEDS).
        # 장작 기록만 내면 지금처럼 반쪽 답(altar1_half14)이다. 결론(1번 쟁점 이김)은 바뀌지 않는다.
        "희생의 숫자와 장부를 대조한다":(("E14_SUPPLY","NW_KKOMI_NOSTONE","NW_SICK_BEDS"),),
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

    # 2026-10-24 대승리 판정(GRAND_WIN_DESIGN.md 0장): 쟁점을 이긴 제출(proof_given)에 보너스 증거가 있으면 대승리다.
    # 회의 결과가 이김일 때만 부른다. 보너스 증거는 어디에도 「새」나 이름으로 표시하지 않는다.
    def r13_nw_grand(keys,bonus):
        return any("V111:"+bonus in (r13_v111_value("proof_given:"+k) or []) for k in keys)

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
        """Morning ending with no one lost (R13_NW_LIVES), Neoul's ledger held, records/hypothesis/blanket/altar
        won, and both grand wins (2026-10-24 MEETING_RULES_V2.md 3장, GRAND_WIN_DESIGN.md 2-5): 7일 불 회의를
        배급표로, 12일 수프 회의를 돌아온 그릇으로 이긴 판. 12일 국을 미리 막은 판은 돌목에게 그릇을 보인
        대화가 수프 대승리를 대신한다(결정 7)."""
        if r13_v111_value("ending14")!="morning" or r13_nw_loss_count():return False
        if not r13_v111_owned("NW_NEOUL_LEDGER"):return False
        if not (r13_v111_value("grand:fire") is True and r13_v111_value("grand:soup") is True):return False
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
            r13_meeting_exhausted(meeting)
            return False
        kept=bool((store.room13.get("arguments") or {}).get(getattr(store,"v111_claim",None) or ""))
        hint=note if (note and correct and r13_nw_half(correct)) else ("맞는 근거는 남겨 두었다." if kept else "맞지 않는다.")
        renpy.notify("기회 1회 사용 · 남은 기회 %d번. %s"%(left,hint))
        r13_nw_wrong_queue(meeting,False)
        return True

    # 2026-10-24 지시서 01 4번 (MEETING_RULES_V2.md 6장 1·2번, 소유자 「증거는 모였다는 걸 알려 주면 좋고」):
    # 틀린 뒤 반박을 듣고 나서 아빠 속말 한 줄. 같은 쟁점에서 틀린 횟수 1 / 2 / 3번째부터 문구가 다르다.
    # 2026-10-24: 회의 11개의 쟁점 39곳(증명 32·선택지 7)을 모두 채웠다. 표에 없는 쟁점만 기본 문구를 쓴다.
    # 1번째는 「근거는 손에 있다」를 쟁점마다 달리 말하고, 2번째는 정답이 겨누는 상대 주장의 구절을 옮기며,
    # 3번째는 자료의 종류와 대략의 때·곳까지. 대체 정답이 있는 쟁점은 어느 길로도 맞게 쓴다.
    # 14일 제단 1번은 장부가 없는 판(반쪽 대답)도 있어 「손에 있다」를 쓰지 않는다. 쟁점별 점검은
    # docs/reviews/wrong-thoughts-20261024/적용보고.md.
    # 자료 이름·정답은 넣지 않는다. 2번째는 상대 주장의 한 구절, 3번째부터는 자료의 종류까지만.
    #   형식: R13_NW_WRONG_THOUGHTS["<쟁점 키>"]={1:"...",2:"...",3:"..."}
    #   쟁점 키 = 증명 키(r13_v111_proof 의 첫 인자), 선택지 쟁점은 "menu:<이름>"(3일 칼 trial_knife, 11일 hyp0~hyp5).
    # 기회를 다 쓴 오답 뒤에는 회의마다 한 번 「다 있었다」 줄을 보인다.
    # 보이는 자리: 증명 화면에 다시 들어갈 때, 선택지 쟁점의 질문 앞(label r13_nw_wrong_thought),
    # 기회를 다 쓴 줄은 그 뒤 처음 나오는 대사 묶음 끝(r13_v111_lines·r13_nw_block 이 덧붙인다).
    R13_NW_WRONG_DEFAULT="근거는 다 손에 있다. 내가 엉뚱한 것끼리 묶었다."
    R13_NW_WRONG_FINAL="다 있었다. 그런데 이어 붙이지 못했다."
    R13_NW_WRONG_THOUGHTS={
        '함께 들어갈 근거를 고른다':{1:'들어갈 근거는 오늘 받은 종이에 다 있다. 내가 엉뚱한 걸 내밀었다.',2:'돌목 씨는 아이를 일꾼으로는 못 받는다고 한다. ……우리가 일꾼으로 왔다는 그 부분, 내가 가진 것과 맞나?',3:'오늘 이 창구에서 본 적힌 것들이다. 우리가 무엇으로 왔는지, 규칙은 무엇이라 하는지.'},
        '수리와 반출을 가릴 자료를 낸다':{1:'톡 씨를 풀어 줄 근거는 이미 모아 두었다. 묶는 법이 틀렸다.',2:'너울 씨는 등을 연 사람이 톡 씨 ‘하나’라고 한다. ……그 부분이 내가 가진 것과 맞나?',3:'그날 새벽 등에 손댄 사람들이 남긴 적힌 것들. 빌린 것, 잰 것, 마지막으로 본 것.'},
        '돌과 매입 기록을 낸다':{1:'돌이 간 길은 오늘 낮에 다 따라가 봤다. 꺼낼 걸 잘못 골랐다.',2:'너울 씨는 마지막으로 연 사람을 대 보라고 한다. ……그 물음에 답할 것이 내 손에 없나?',3:'오늘 낮 창고에서 본 물건, 그리고 그것을 누가 팔았는지 적힌 것.'},
        'menu:trial_knife':{1:'칼은 이미 탁자 위에 있다. 내가 보는 자리가 틀렸다.',2:'실룩 씨는 같은 칼이야 얼마든지 있다는 투다. ……모양만 보면 그 말이 맞지 않나?',3:'등 안쪽에서 나온 물건이 있었다. 그것이 어느 칼에서 왔는지는 모양 말고 다른 데서 드러난다.'},
        '바깥 걸쇠 주장과 발견 위치를 대조한다':{1:'실룩 씨 말을 깰 자료는 다 손에 있다. 내가 엮은 순서가 어긋났다.',2:'실룩 씨는 ‘바깥 걸쇠만’ 칼로 밀어 닫았다고 한다. ……그 부분이 내가 가진 것과 맞나?',3:'실룩 씨가 직접 한 말, 그리고 조각이 나온 자리와 칼을 맞대 본 것. 다 오늘 이 공방에서다.'},
        '마지막 점검과 인수한 돌을 연결한다':{1:'돌 하나의 길은 처음부터 끝까지 수첩에 있다. 이어 붙이는 데서 틀렸다.',2:'실룩 씨는 자기가 판 돌이 ‘그 돌’인지는 모른다고 한다. ……정말 그 부분이 비어 있나?',3:'새벽에 등을 마지막으로 본 사람의 기록, 그리고 창고에 있던 돌과 그 돌을 판 줄.'},
        '밤이 혐의의 근거를 확인한다':{1:'밤이를 지킬 근거는 이미 모았다. 내가 엉뚱한 것끼리 묶었다.',2:'너울 씨는 키가 맞으면 밤이일 수도 있다고 한다. ……‘키가 맞으면’이라는 그 부분, 내가 가진 것과 맞나?',3:'그날 밤 그 사람의 키나 차림을 보여 줄 것. 울타리에 남은 것이든, 그 사람을 본 눈이든.'},
        '불이 시작된 곳과 진술을 대조한다':{1:'불이 난 자리에서 본 건 다 적어 두었다. 내가 꺼낸 게 틀렸다.',2:'누비 씨는 어제 저녁 그 통으로 물을 데웠다고 한다. ……그 등유가 간 곳, 내가 본 것과 맞나?',3:'어젯밤 불탄 창고에서 내 눈으로 본 것. 불이 어디서 시작됐고, 그 자리에 무엇이 남았는지.'},
        '불의 원인과 빈 창고 진압을 구분한다':{1:'누구 몫의 잘못인지 가를 근거는 다 모였다. 내가 한데 섞어 냈다.',2:'너울 씨는 셋 다 책임이 있다고 한 줄로 묶는다. ……그 묶음이 내가 가진 것과 맞나?',3:'오늘 아침 빨래터에서 들은 말, 어젯밤 불난 자리, 그리고 그때 보리 씨가 한 일을 내가 본 것.'},
        '불의 원인과 아이 구조를 구분한다':{1:'불을 낸 일과 아이를 꺼낸 일. 근거는 따로따로 손에 있다. 내가 뒤섞었다.',2:'너울 씨는 ‘다들 책임이 있소’로 끝내려 한다. ……그 말이 내가 본 어젯밤과 맞나?',3:'누비 씨가 오늘 스스로 한 말, 불이 시작된 자리, 그리고 창고 앞에서 내 눈으로 본 보리 씨.'},
        '두 상처와 촛대 파손을 대조한다':{1:'다람이 편에 설 근거는 이미 손에 있다. 이어 붙이는 법이 틀렸다.',2:'너울 씨는 손목을 쳤으면 머리도 쳤을 수 있다고 한다. ……그 부분이 내가 가진 것과 맞나?',3:'다람이 본인이 한 말, 그리고 두 상처와 부러진 촛대를 따로따로 본 사람의 기록.'},
        '두 번째 길을 실제 기록으로 보인다':{1:'그 방에 드나든 길은 내가 이미 확인했다. 내놓을 걸 잘못 골랐다.',2:'너울 씨는 그 문으로 들어간 사람이 없었다고 한다. ……‘그 문’만 있었다는 그 부분, 맞나?',3:'내 발로 직접 걸어 본 것, 그리고 13호 방 안을 둘러보며 적은 것. 둘 다 내가 남겼다.'},
        '구리선과 수선 출처를 대조한다':{1:'이 핀이 누구 것인지 가릴 근거는 다 있다. 내가 맞대 본 게 틀렸다.',2:'할머니는 시장에서 한 줌씩 파는 흔한 핀이라고 한다. ……‘흔한’ 핀이라는 그 부분, 맞나?',3:'이 핀을 고친 흔적이 남은 것, 그리고 그 수선을 적어 둔 공방 쪽 기록.'},
        '첫 비명 뒤 핀을 다시 채운 때':{1:'핀이 언제 어디 있었는지, 들은 말은 다 적어 두었다. 내가 고른 게 틀렸다.',2:'할머니는 낮에 방을 치울 때 떨어졌을 거라고 한다. ……‘낮에’라는 그 부분, 내가 가진 것과 맞나?',3:'그날 밤 그 핀을 직접 본 사람의 말. 첫 비명 뒤와, 다람이 손을 잡고 있던 때.'},
        '접촉면과 아이의 위치를 대조한다':{1:'여기까지 온 근거로 다 말할 수 있다. 하나를 빠뜨렸거나 잘못 끼웠다.',2:'할머니는 아이가 먼저 그걸 쓰고 내려놨을 수도 있다고 한다. ……그 부분이 내가 가진 것과 맞나?',3:'촛대 조각에 무엇이 어떻게 붙었는지와 그 천의 주인, 상처에 남은 것, 다람이 손을 지켜본 사람.'},
        '수신인과 가족 전달 권한을 구분한다':{1:'아내가 누구에게 무엇을 맡겼는지, 근거는 모았다. 내가 잘못 짚었다.',2:'할머니는 아내가 가족에게 전할 것을 늘 자기에게 맡겼다고 한다. ……그 부분이 내가 가진 것과 맞나?',3:'아내 쪽에서 나온 것이 누구 앞으로 왔는지 적힌 것. 학교 뒤와 우체국에서 본 것이다.'},
        '반송·필사본·초대 발송을 대조한다':{1:'그 초대장이 어디서 왔는지, 손에 든 것만으로 말할 수 있다. 엮는 법이 틀렸다.',2:'할머니는 나도 ‘부인 글씨’라고 했다고 한다. ……글씨가 닮았다는 그 부분, 내가 가진 것과 맞나?',3:'1일부터 품에 있던 종이, 그것이 어디서 왔는지 말해 줄 것, 그리고 우체국에 남은 날짜.'},
        'menu:hyp0':{1:'이 마을에서 본 것만으로 말할 수 있다. 내가 고른 말이 빗나갔다.',2:'마을은 아르카가 사람을 ‘부른다’고, 불려 간 건 복이라고 한다. ……그 말이 내가 본 것과 맞나?',3:'무너진 사람들이 무엇 곁에서 얼마나 지냈는지. 2일 광장부터 내가 본 사람들을 떠올리자.'},
        'menu:hyp1':{1:'초롱 씨가 멀쩡한 까닭도 내가 본 것 안에 있다. 내가 짚은 이유가 틀렸다.',2:'돌목 씨는 아르카를 ‘날마다 만지는’ 초롱 씨가 멀쩡하다고 한다. ……‘만진다’가 맞는 잣대인가?',3:'초롱 씨가 하루에 등을 어떻게 도는지, 그리고 등 바로 아래서 지낸 사람이 어땠는지.'},
        '초롱과 피코의 하루를 대조한다':{1:'초롱 씨와 피코 씨의 하루, 둘 다 수첩에 있다. 내가 엉뚱한 쪽을 냈다.',2:'돌목 씨는 날마다 만지는 초롱 씨가 멀쩡하다고 한다. ……그 ‘날마다’가 어떤 하루인지, 내가 가진 것과 맞나?',3:'초롱 씨의 하루가 적힌 것, 그리고 2일 광장에서 등 아래 피코 씨를 내 눈으로 본 것.'},
        'menu:hyp2':{1:'백 부인 창고 일도 내가 직접 보고 들었다. 짚은 이유가 빗나갔다.',2:'백 부인은 돌이 산더미인 창고의 주인인데 멀쩡하다고 한다. ……‘주인이 멀쩡하다’는 그 부분, 맞나?',3:'3일 백 부인 창고에서 보고 들은 것. 누가 어디서 지내는지.'},
        '창고에서 잠자는 사람을 짚는다':{1:'창고에서 누가 지내는지, 나는 이미 봤다. 내놓을 걸 잘못 골랐다.',2:'백 부인은 그 창고 곁에서 멀쩡한 사람으로 자기만 든다. ……그 창고에 부인만 있었나?',3:'3일 창고 구석에서 내가 본 사람, 그리고 그 사람이 내게 한 말.'},
        'menu:hyp3':{1:'왜 요즘 늘었는지, 내가 들은 말 안에 답이 있다. 고른 말이 틀렸다.',2:'판돌 씨는 옛날부터 아르카를 써 왔다고 한다. ……‘옛날부터’라는 그 말, 내가 들은 것과 맞나?',3:'요즘 돌값을 들은 곳, 그리고 광산에서 일한 사람 집에서 들은 말.'},
        '요즘 돌이 어디서 오는지 대조한다':{1:'요즘 돌이 어디서 오는지, 들은 말은 다 적어 두었다. 묶는 법이 틀렸다.',2:'판돌 씨 말로는 옛날부터 같은 아르카를 써 왔다. ……그 ‘같은’이 내 수첩과 맞나?',3:'3일 창고에서 들은 돌값, 그리고 5일 솜이네에서 들은, 돌을 캐던 사람 이야기.'},
        'menu:hyp4':{1:'아이들이 왜 앓는지도 내가 본 것 안에 있다. 짚은 이유가 빗나갔다.',2:'주민은 아이가 무슨 죄냐고 묻는다. 아이와 아르카는 상관없다는 투다. ……그 부분이 내가 본 것과 맞나?',3:'오늘 학교 입구에서 본 적힌 것, 그리고 창고 아이들이 밤에 무엇을 켜는지 들은 말.'},
        '아르카가 없는 아이들과 대조한다':{1:'견줄 아이들은 둘 다 손에 있다. 내가 엉뚱하게 견주었다.',2:'주민은 ‘우리 애가 무슨 죄냐’고 한다. 아이 몸이 약해서라는 투다. ……그 부분이 내가 가진 것과 맞나?',3:'오늘 학교 입구의 적힌 것, 그리고 6일 창고 아이에게 들은, 그 방의 불 이야기.'},
        'menu:hyp5':{1:'직접 본 일은 있다. 내가 고른 말이 그 일을 비껴갔다.',2:'선생님은 아르카가 사람을 무너뜨리는 걸 ‘직접 본 사람’이 있느냐고 묻는다. ……없다고 할 수 있나?',3:'13호, 한 방 안에서 한 저녁 사이에 일어난 일. 그 방 난로를 떠올리자.'},
        '13호 난로의 돌을 내놓는다':{1:'답할 것은 이미 손에 있다. 내가 엉뚱한 걸 집었다.',2:'선생님은 ‘직접 본 사람’을 찾는다. ……그 물음에 말 말고 손에 쥔 것으로 답할 수 없나?',3:'13호 난로에 들어 있던 것. 들은 말이 아니라 물건이다.'},
        '재사용 설명과 개봉 봉인을 대조한다':{1:'선생님 말을 가를 근거는 다 손에 있다. 내가 엉뚱한 것끼리 맞댔다.',2:'선생님은 약을 ‘다 쓴 병’에 물을 담았다고 한다. ……그 부분이 내가 본 것과 맞나?',3:'아이들 냄비에서 나온 것, 그리고 배식 준비 때 그 병을 내 눈으로 함께 본 것.'},
        '파편·봉인·취급 구간을 함께 제시한다':{1:'선생님 말이 어디서 어긋나는지, 근거는 다 들었다. 묶는 법이 틀렸다.',2:'선생님은 병을 비우고 ‘씻는 데서’ 물을 받았다고 한다. ……그 부분이 내가 들은 것과 맞나?',3:'냄비 쪽 두 가지에 더해, 냄비를 건넨 짧은 동안을 곁에서 지켜본 사람의 말.'},
        '명단과 흰 그릇을 대조한다':{1:'선생님 말을 가를 것은 오늘 하루 내가 본 것 안에 있다. 내가 엉뚱하게 맞댔다.',2:'선생님은 작은 냄비가 아이들 ‘모두’를 위한 것이었다고 한다. ……그 ‘모두’가 내가 본 것과 맞나?',3:'오늘 아침 학교 문 옆에 붙은 적힌 것, 그리고 배식 때 누구 앞에 무엇이 놓였는지 본 것.'},
        '아내가 봤다는 담요의 시점을 확인한다':{1:'이 담요의 일은 내가 제일 잘 안다. 내놓을 걸 잘못 골랐다.',2:'촌장은 ‘어젯밤’ 모과 씨가 이 담요의 새를 보고 웃었다고 한다. ……그 부분이 내가 아는 것과 맞나?',3:'오늘 아침 학교에서 내 손으로 한 일. 다람이도 곁에 있었다.'},
        '촌장이 어젯밤 있던 곳을 확인한다':{1:'촌장 말을 가를 근거는 이미 손에 있다. 내가 맞대 본 게 틀렸다.',2:'촌장은 학교 종이 울릴 무렵 모과 씨를 보러 나가 있었다고 한다. ……그 시각, 내가 본 것과 맞나?',3:'어젯밤 종이 울릴 무렵 내 눈으로 본 것. 그때 나는 어디를 지나고 있었나.'},
        '장부의 두 배를 실룩에게 보인다':{1:'실룩 씨 입을 열 근거는 이미 손에 있다. 내가 엉뚱한 걸 내밀었다.',2:'너울 씨는 ‘그게 증거냐’고 흘려 넘긴다. ……‘두 배’라는 내 말, 가진 것으로 받칠 수 있지 않나?',3:'3일 백 부인 쪽에서 받아 둔 적힌 것. 누가 무엇을 얼마에 팔았는지.'},
        '피코가 막혀야 했던 까닭을 보인다':{1:'너울 씨가 피코 씨를 막은 까닭, 근거는 손에 있다. 내가 고른 게 틀렸다.',2:'너울 씨는 ‘도둑의 말’이라고 덮는다. ……피코 씨가 품던 판자, 그 부분을 받쳐 줄 것이 없나?',3:'피코 씨가 그린 그림 속에 무엇이 있었는지. 겉에 보이는 것 말고, 그 밑까지.'},
        '희생의 숫자와 장부를 대조한다':{1:'숫자에는 숫자로 맞서야 한다. 내가 엉뚱한 것을 들이밀었다.',2:'촌장은 ‘한 사람이 열흘을 산다’고 한다. ……그 숫자가 내가 가진 숫자와 맞나?',3:'돌과 장작, 그리고 누가 무너졌는지가 적힌 것. 그런 숫자라야 열흘과 견줄 수 있다.'},
        '아르카가 부른다는 말과 옛 기록을 대조한다':{1:'옛사람들이 남긴 말은 이미 손에 있다. 내가 맞대는 법이 틀렸다.',2:'촌장은 아르카가 ‘부른’ 사람이라고 한다. ……그 ‘부른다’는 말이 옛 기록과 맞나?',3:'옛 시설과 제단에서 본, 돌에 새긴 글. 깨진 두 쪽을 이어 읽자.'},
        '쇠가 언제 붙었는지 보인다':{1:'그 쇠의 일은 오늘 제단에서 내 눈으로 봤다. 내놓을 걸 잘못 골랐다.',2:'촌장은 쇠가 ‘할아버지 때부터’ 있었다고 한다. ……그 부분이 내가 본 것과 맞나?',3:'오늘 제단의 쇠에서 내 눈으로 본 것. 쇠 안쪽을 떠올리자.'},
        '맨 처음 이름을 짚는다':{1:'처음이 누구였는지, 근거는 손에 있다. 내가 엉뚱한 것끼리 겹쳤다.',2:'촌장은 ‘처음부터’ 그렇게 해 왔다고 한다. ……그 ‘처음’이 언제 누구였는지, 내가 가진 것과 맞나?',3:'옛 시설 벽에 새겨진 것, 그리고 그해 집집이 받은 돌이 적힌 것. 둘을 겹쳐 보자.'},
    }
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
