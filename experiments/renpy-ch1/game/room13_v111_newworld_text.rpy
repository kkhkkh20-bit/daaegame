# New-world dialogue layer (2026-10-21 rework plan, "새 세계관 대사판").
# The authored V1.1.1 records stay exactly as imported (test_v111 checks them).
# Owner-reviewed revisions live in game/v111/newworld/dNN.json and are applied
# here, by record ID only:
#   replace  {rid: {"text": ..., "when"?: name, "expression"?: slot}}   new sentence for an authored line (only while when holds)
#            or {rid: [variant, ...]}: one sentence per branch, the first variant whose when holds is shown
#   before / after  {rid: [line, ...]}             new lines around an authored line
#   drop     [rid | {"id": rid, "when": name}, ...]  authored line not shown (while when holds)
#   evidence {key: {"name": ..., "variants": {variant: text}, "add_variants": {new: text}}}
#   new_evidence {"NW_...": {"name": ..., "kind": "물증|기록|관찰기록|증언", "variants": {variant: text}}}
#            a record that only the new world has; the generators acquire it with r13_nw_acquire
#   titles   {binding: {option index: title}}        new wording for a field choice (v111/field-bindings.json)
#   blocks   {name: [line, ...]}                     new-world lines with no authored record
#            (new meetings); the generators show them with r13_nw_block(name)
# A new line: {"id": "NW_...", "speaker": name|null, "text": ..., "kind"?: dialogue|narration|thought, "expression"?,
#              (thought: the father's unspoken line; text without brackets, the engine adds them)
#              "fx"?: jolt|shake|slam|flash, a one-off hit, shake or flash as the line appears
#              "beat"?: a meeting-stage beat (interrupt, shaken, cornered, ...) for lines inside a meeting
#              "when"?: condition name in R13_NW_WHEN, "cut"?: existing ep art name}
# Conditions are named Python predicates, never evaluated strings.
# With every file empty the game shows the same lines in the same order as before.
init 319 python:
    R13_NW_TEXT_DAYS=["d%02d"%n for n in range(1,15)]
    R13_NW_TEXT=dict(replace={},before={},after={},drop=[],evidence={},new_evidence={},blocks={},titles={})
    for _nw_day in R13_NW_TEXT_DAYS:
        _nw_path="v111/newworld/%s.json"%_nw_day
        if not renpy.loadable(_nw_path):continue
        with renpy.file(_nw_path) as _nw_file:_nw_part=json.load(_nw_file)
        for _nw_key in ("replace","before","after","evidence","new_evidence","blocks","titles"):
            for _nw_rid,_nw_value in _nw_part.get(_nw_key,{}).items():
                if _nw_rid in R13_NW_TEXT[_nw_key]:raise Exception("Duplicate new-world entry: %s %s"%(_nw_key,_nw_rid))
                R13_NW_TEXT[_nw_key][_nw_rid]=_nw_value
        R13_NW_TEXT["drop"]+=list(_nw_part.get("drop",[]))
    # New-world records join the V1.1.1 catalog before anything checks references.
    for _nw_key,_nw_spec in R13_NW_TEXT["new_evidence"].items():
        if not _nw_key.startswith("NW_") or _nw_key in R13_V111["evidence"]:raise Exception("Bad new-world evidence key: "+_nw_key)
        if _nw_spec.get("kind") not in R13_RECORD_CATEGORIES or not _nw_spec.get("name") or not _nw_spec.get("variants"):raise Exception("Incomplete new-world evidence: "+_nw_key)
        R13_V111["evidence"][_nw_key]=dict(name=_nw_spec["name"],kind=_nw_spec["kind"],variants=dict(_nw_spec["variants"]))
        ROOM13["evidence"]["V111:"+_nw_key]=dict(id="V111:"+_nw_key,name=_nw_spec["name"],kind=_nw_spec["kind"],establishes=next(iter(_nw_spec["variants"].values())),does_not_establish="",current_run_only=True,retained_on_show=True,scenes=[])
        R13_RECORD_SHORT["V111:"+_nw_key]=_nw_spec["name"]
    def r13_nw_acquire(key,variant="observed"):
        """Give a new-world record once (same path as an authored 'acquire')."""
        if key not in R13_NW_TEXT["new_evidence"]:raise Exception("Unknown new-world evidence: "+str(key))
        if variant not in R13_V111["evidence"][key]["variants"]:raise Exception("Unknown new-world evidence variant: %s %s"%(key,variant))
        r13_v111_apply("nw:acquire:"+key,[dict(op="acquire",key=key,variant=variant)])
    # Named conditions for added lines. Add one line here when an event needs it.
    R13_NW_WHEN={
        "always":lambda:True,
        "owl_alive":lambda:r13_v111_value("OWL_ALIVE") is not False,
        "owl_dead":lambda:r13_v111_value("OWL_ALIVE") is False,
        "piko_alive":lambda:r13_v111_value("piko_alive") is not False,
        # 0.20.7 (ending review 4·5·6·13·15): one last act per path, after the shared snack scene.
        "end_portrait_child":lambda:r13_v111_value("piko_alive") is False and r13_v111_value("portrait")=="child_completed" and not r13_nw_true_ending_ready(),
        "end_family":lambda:r13_v111_value("ending14")=="family",
        "end_partial_departed":lambda:r13_v111_value("ending14")=="partial" and bool(r13_v111_value("cart_departed")),
        "end_partial_waiting":lambda:r13_v111_value("ending14")=="partial" and not r13_v111_value("cart_departed") and not r13_v111_value("pending_handover_completed"),
        "end_partial_done":lambda:r13_v111_value("ending14")=="partial" and not r13_v111_value("cart_departed") and bool(r13_v111_value("pending_handover_completed")),
        "end_injury":lambda:bool(r13_v111_value("crowd_injury")),
        "end_morning_won":lambda:r13_v111_value("ending14")=="morning" and r13_v111_value("meeting:altar")=="win" and not r13_nw_true_ending_ready(),
        "end_morning_partial":lambda:r13_v111_value("ending14")=="morning" and r13_v111_value("meeting:altar")=="partial",
        "end_morning_lost":lambda:r13_v111_value("ending14")=="morning" and r13_v111_value("meeting:altar")=="lose",
        "piko_dead":lambda:r13_v111_value("piko_alive") is False,
        "kkomi_alive":lambda:r13_v111_value("KKOMI_ALIVE") is not False,
        "kkomi_dead":lambda:r13_v111_value("KKOMI_ALIVE") is False,
        # Event 01: lost gate proof, Daram entered as '외 한 명' (owner plan A, 2026-10-21).
        "gate_daram_unlisted":lambda:r13_v111_value("gate_daram_unlisted") is True,
        "gate_daram_listed":lambda:r13_v111_value("gate_daram_unlisted") is not True,
        # Review 0.20.1 #1: the gate's "entry allowed" lines only on the last wrong answer.
        # 0.20.6 (play review P02): after the room is looked over, Granny stops sending us back up.
        "room13_checked_d1":lambda:r13_v111_owned("E06"),
        "room13_unchecked_d1":lambda:not r13_v111_owned("E06"),
        "d06_bowl_together":lambda:r13_v111_value("choice:MS14_D06_S01")=="together",  # 0.20.7
        "gate_last_try":lambda:(r13_v111_value("tries:gate") or 0)+1>=r13_nw_tries_max("gate"),
        "gate_retry":lambda:(r13_v111_value("tries:gate") or 0)+1<r13_nw_tries_max("gate"),
        # 0.20.5 (Codex C03): a wrong answer that held only some of the gate records says so,
        # without naming the missing ones; a set with none of them gets the plain refusal.
        "gate_partial_retry":lambda:(r13_v111_value("tries:gate") or 0)+1<r13_nw_tries_max("gate") and bool(set(getattr(store,"v111_last_presented",None) or [])&{"V111:E02","V111:E03","V111:E04"}),
        # Review 0.20.1 4-5: the day-12 prep line names only what is really ready.
        "prep12_others_missing":lambda:not all(r13_v111_value(k) for k in ("warm_seat_ready","carrier_arrived","warm_support_arrived")),
        # 0.20.6 (owner review): one of the two ready -> name only what is still missing.
        "prep12_seat_only":lambda:bool(r13_v111_value("warm_seat_ready")) and not r13_v111_value("carrier_arrived"),
        "prep12_carrier_only":lambda:bool(r13_v111_value("carrier_arrived")) and not r13_v111_value("warm_seat_ready"),
        "prep12_seat_and_carrier":lambda:bool(r13_v111_value("warm_seat_ready")) and bool(r13_v111_value("carrier_arrived")),
        # Event 03: the day-3 lamp meeting (win / partial / lose).
        "lamp_win":lambda:r13_v111_value("meeting:lamp")=="win",
        "lamp_partial":lambda:r13_v111_value("meeting:lamp")=="partial",
        "lamp_lose":lambda:r13_v111_value("meeting:lamp")=="lose",
        "lamp_not_win":lambda:r13_v111_value("meeting:lamp") in ("partial","lose"),
        # Audit d01-05 #1/#6: which stage of the lamp meeting was reached (sale -> knife -> latch -> stone).
        "lamp_stage_sale":lambda:r13_v111_value("repair_opening_separated") is True,
        "lamp_stage_latch":lambda:r13_v111_owned("E33"),
        "lamp_stage_stone":lambda:r13_v111_value("outer_latch_claim_refuted") is True,
        "lamp_partial_sale":lambda:r13_v111_value("meeting:lamp")=="partial" and not r13_v111_owned("E33"),
        "lamp_partial_latch":lambda:r13_v111_value("meeting:lamp")=="partial" and r13_v111_owned("E33") and r13_v111_value("outer_latch_claim_refuted") is not True,
        "lamp_partial_stone":lambda:r13_v111_value("meeting:lamp")=="partial" and r13_v111_value("outer_latch_claim_refuted") is True,
        # Event 04: the day-5 gate-post meeting.
        "gate_post_lose":lambda:r13_v111_value("meeting:gate_post")=="lose",
        "gate_post_half":lambda:(r13_v111_value("tries:gate_post") or 0)>0 and r13_v111_value("meeting:gate_post") is None,
        # Proof scope (owner 2026-10-22): a won proof that carried an allowed extra record
        # (R13_PROOF_EXTRAS / R13_PROOF_ALTERNATES in room13_v111_newworld_rules.rpy).
        "gate_won_with_e01":lambda:"V111:E01" in (r13_v111_value("proof_given:함께 들어갈 근거를 고른다") or []),
        "repair_won_with_e10":lambda:"V111:E10" in (r13_v111_value("proof_given:수리와 반출을 가릴 자료를 낸다") or []),
        "gate_post_won_with_e21":lambda:"V111:E21" in (r13_v111_value("proof_given:밤이 혐의의 근거를 확인한다") or []),
        # 0.20.18 연쇄 P1: 살아 있는 피코의 4일 밤 그림을 회의에 냈는가. _only 는 겉옷·귀가 진술 없이 그림으로 이긴 경우.
        "gate_post_won_with_sketch":lambda:"V111:NW_PIKO_SKETCH4" in (r13_v111_value("proof_given:밤이 혐의의 근거를 확인한다") or []),
        "gate_post_won_with_sketch_only":lambda:"V111:NW_PIKO_SKETCH4" in (r13_v111_value("proof_given:밤이 혐의의 근거를 확인한다") or []) and not {"V111:E23","V111:E24"}&set(r13_v111_value("proof_given:밤이 혐의의 근거를 확인한다") or []),
        # 0.20.18 (열쇠표 K1): 2일 오후 피코의 자리를 위해 실제로 한 일.
        "piko_sacks2":lambda:r13_v111_value("piko_sacks2") is True,
        # 0.20.18 (열쇠표 K2): 6일 선생님께 아이들 자리를 받아 두었는가.
        "kkomi_seat6":lambda:r13_v111_value("kkomi_seat6") is True,
        # 2026-10-23 연결오류: 아이들을 먼저 옮긴 판에서는 도토를 이미 만났다(P01·빈 창고 불). 소개를 되풀이하지 않는다.
        "fire_evacuated":lambda:r13_v111_value("FIRE_EVACUATED") is True,
        # 2026-10-24 지시서 02 감정선: 불을 끄다 보리가 손을 덴 판(bori_burned6), 7일 도담 숟가락·12일 다람이 숟가락을 돌려주는가,
        # 10일 꼬미와 도토리를 나눴는가.
        "fire_not_evacuated":lambda:r13_v111_value("FIRE_EVACUATED") is not True,
        "dodam_spoon_lent":lambda:r13_v111_value("dodam_spoon7") is True and r13_v111_actor_ready("daram"),
        "dodam_spoon12":lambda:r13_v111_value("dodam_spoon12") is True,
        "kkomi_acorn_shared":lambda:r13_v111_value("kkomi_acorn10") is True and r13_v111_actor_ready("daram"),
        # 0.20.18 (CRUEL_CHOICES.md C1): 13일 공개 때 엄마와 다람이 광장에 있는가.
        # 0.20.18 (CRUEL_CHOICES.md C3 A안): 3일 실룩을 풀어 준 판, 5번 등이 비어 밤이가 처마에서 내려왔다.
        "bami_cold4":lambda:r13_v111_value("bami_cold4") is True,
        "bami_warm4":lambda:r13_v111_value("bami_cold4") is not True,
        # 0.20.19 (CRUEL_CHOICES.md D1·D3): 폭동 때 수레에 남아 있던 모모, 12일 다람이 말할 수 있는가.
        "riot_momo13":lambda:r13_v111_value("riot_momo13") is True,
        "daram_ready":lambda:r13_v111_actor_ready("daram"),
        # 0.20.20 (aftermath 시안): 막아섰다가 실패한 판, 수레로 떠난 사람이 있는 판.
        "crowd_block_failed13":lambda:r13_v111_value("crowd_intervention")=="failed" and r13_v111_value("crowd_blocked_by_dad") is True,
        "departed_any":lambda:any(p!="daram" for p in (r13_v111_value("departed_names") or [])),
        "family_on_square":lambda:r13_v111_value("family_location")=="square" and r13_v111_actor_ready("daram"),
        # 2026-10-24 자료 재사용(EVIDENCE_CLUTTER_PLAN.md 2부): 정답 위에 덧붙인 자료를 상대가 한 줄로 짚는다.
        "hyp1_won_with_e28":lambda:"V111:E28" in (r13_v111_value("proof_given:초롱과 피코의 하루를 대조한다") or []),
        "hyp3_won_with_e14":lambda:"V111:E14" in (r13_v111_value("proof_given:요즘 돌이 어디서 오는지 대조한다") or []),
        "writing_won_with_e27":lambda:"V111:E27" in (r13_v111_value("proof_given:반송·필사본·초대 발송을 대조한다") or []),
        "writing_won_with_e09":lambda:"V111:E09" in (r13_v111_value("proof_given:반송·필사본·초대 발송을 대조한다") or []),
        "blanket_won_with_e35":lambda:"V111:E35" in (r13_v111_value("proof_given:아내가 봤다는 담요의 시점을 확인한다") or []),
        "badook_won_with_e29":lambda:"V111:E29" in (r13_v111_value("proof_given:촌장이 어젯밤 있던 곳을 확인한다") or []),
        "piko_ledger_with_e34":lambda:"V111:E34" in (r13_v111_value("proof_given:장부의 두 배를 실룩에게 보인다") or []),
        "altar4_won_with_ledger":lambda:"V111:NW_NEOUL_LEDGER" in (r13_v111_value("proof_given:맨 처음 이름을 짚는다") or []),
        "altar4_won_with_rations":lambda:"V111:NW_OLD_RATIONS" in (r13_v111_value("proof_given:맨 처음 이름을 짚는다") or []) and "V111:NW_NEOUL_LEDGER" not in (r13_v111_value("proof_given:맨 처음 이름을 짚는다") or []),
        "altar4_won_with_burnt_page":lambda:"V111:NW_BURNT_PAGE" in (r13_v111_value("proof_given:맨 처음 이름을 짚는다") or []),
        "hyp1_won_without_e08":lambda:bool(r13_v111_value("proof_given:초롱과 피코의 하루를 대조한다")) and "V111:E08" not in r13_v111_value("proof_given:초롱과 피코의 하루를 대조한다"),
        # Event 05: the day-7 fire meeting.
        "fire_win":lambda:r13_v111_value("meeting:fire")=="win",
        "fire_partial":lambda:r13_v111_value("meeting:fire")=="partial",
        "fire_lose":lambda:r13_v111_value("meeting:fire")=="lose",
        # Events 06-07: the day-7 room 13 night and the day-10 meetings.
        # 2026-10-25 부엉이 예방 1단계(OWL_PREVENTION_DESIGN.md 9장): 7일 A/B/C 메뉴를 걷고, 7일 낮 13호 난로의 돌(stone)
        # 또는 도토의 다짐(promise)으로만 막는다. 다짐만 받은 판은 예전 B 판처럼 부엉이가 무너진 채 살아 8일 서리가 돌을 꺼낸다.
        "prevention_b":lambda:r13_v111_value("prevention") in ("B","promise"),
        "prevention_stone":lambda:r13_v111_value("prevention")=="stone",
        "owl_fell7":lambda:r13_v111_value("OWL_ALIVE") is not False and r13_v111_value("prevention")!="stone",
        "stove_untouched7":lambda:r13_v111_value("stove13_7") is None,
        "stove_blue7":lambda:r13_v111_value("stove13_7") not in ("ration","empty"),
        "stove_fixed7":lambda:r13_v111_value("stove13_7") in ("ration","empty"),
        "stove_ration7":lambda:r13_v111_value("stove13_7")=="ration",
        "stove_emptied7":lambda:r13_v111_value("stove13_7")=="empty",
        # 결정 11(2026-10-25): 5일 밤 접시의 과자 봉지를 다람의 가방에 넣은 판. 아니면 과자는 첫날처럼 외투 안에 있다.
        "snack_bagged5":lambda:r13_v111_value("snack_bagged5") is True,
        "snack_unbagged5":lambda:r13_v111_value("snack_bagged5") is not True,
        "room13_win":lambda:r13_v111_value("meeting:room13")=="win",
        "room13_lose":lambda:r13_v111_value("meeting:room13")=="lose",
        "room13_not_win":lambda:r13_v111_value("meeting:room13") in ("partial","lose"),
        "room13_partial_unknown":lambda:r13_v111_value("meeting:room13")=="partial" and r13_v111_value("room13_partial_kind")=="unknown",
        "room13_partial_accident":lambda:r13_v111_value("meeting:room13")=="partial" and r13_v111_value("room13_partial_kind")=="accident",
        "records_partial":lambda:r13_v111_value("meeting:records")=="partial",
        "records_lose":lambda:r13_v111_value("meeting:records")=="lose",
        "records_lose_prev_b":lambda:r13_v111_value("meeting:records")=="lose" and r13_v111_value("prevention")!="stone",
        "records_partial_prev_b":lambda:r13_v111_value("meeting:records")=="partial" and r13_v111_value("prevention")!="stone",
        # 돌을 바꿔 부엉이가 무너지지 않은 판: 할머니가 너울에게 「같은 말을 두 번 묻는다」고 일러 명단 얘기가 나온다.
        "records_lose_prev_stone":lambda:r13_v111_value("meeting:records")=="lose" and r13_v111_value("prevention")=="stone",
        "records_partial_prev_stone":lambda:r13_v111_value("meeting:records")=="partial" and r13_v111_value("prevention")=="stone",
        "records_lose_fell7":lambda:r13_v111_value("meeting:records")=="lose" and r13_v111_value("prevention")!="stone",
        # Event 08: the day-11 facility and the hypothesis meeting.
        "guldol_ready":lambda:r13_v111_actor_ready("resident_guldol"),
        "karo_ready":lambda:r13_v111_actor_ready("karo"),  # 0.20.9
        "karo_absent":lambda:not r13_v111_actor_ready("karo"),  # 2026-10-23 연결오류: 까로가 없는 숲의 대체 지문
        "route12_late":lambda:r13_v111_value("route12")=="late_exposure",  # 0.20.10 D12-03 학교 밖에 다녀온 경로
        "route12_stayed":lambda:r13_v111_value("route12")!="late_exposure",
        "tosil_inside":lambda:r13_v111_value("tosil_listen")=="inside",  # 0.20.9 엔딩 검토 9
        "tosil_outside":lambda:r13_v111_value("tosil_listen")=="outside",
        "tok_round_asked":lambda:bool(r13_v111_value("followup_read:NW_RX_F007")),  # 0.20.9 D23-04 먼저 물어본 경우
        "heard_inn_order1":lambda:r13_v111_value("heard_inn_order1") is True,  # 0.20.9 1일 문간 지시를 들은 경로
        "guldol_absent":lambda:not r13_v111_actor_ready("resident_guldol"),
        # 2026-10-24 자가 검수 12: 11일 판돌이 아빠 말을 들어 주는 까닭. 앞 회의(3·5·7·10일) 중 하나라도 이겼는가.
        "town_won_before11":lambda:any(r13_v111_value("meeting:"+m)=="win" for m in ("lamp","gate_post","fire","room13","records")),
        "town_won_none_before11":lambda:not any(r13_v111_value("meeting:"+m)=="win" for m in ("lamp","gate_post","fire","room13","records")),
        "hyp_win":lambda:r13_v111_value("meeting:hypothesis")=="win",
        "hyp_partial":lambda:r13_v111_value("meeting:hypothesis")=="partial",
        "hyp_lose":lambda:r13_v111_value("meeting:hypothesis")=="lose",
        "hyp_not_lose":lambda:r13_v111_value("meeting:hypothesis") in ("win","partial"),
        "hyp_lost1":lambda:r13_v111_value("hyp_issue:1")=="lost",
        "hyp_lost2":lambda:r13_v111_value("hyp_issue:2")=="lost",
        "hyp_lost3":lambda:r13_v111_value("hyp_issue:3")=="lost",
        "hyp_lost4":lambda:r13_v111_value("hyp_issue:4")=="lost",
        # Event 09: the day-12 soup.
        "soup_lose_stolen":lambda:r13_v111_value("meeting:soup")=="lose" and r13_v111_value("soup_lose_kind")=="stolen",
        "soup_lose_nabi":lambda:r13_v111_value("meeting:soup")=="lose" and r13_v111_value("soup_lose_kind")=="nabi",
        # Event 10: the day-13 cart.
        "daram_deal_freed":lambda:r13_v111_value("daram_deal_freed") is True,
        # Audit d11-14 #2: a hypothesis wrong answer that may be retried holds judgment.
        "hyp_retry":lambda:r13_v111_value("meeting:hypothesis") is None and (r13_v111_value("tries:hypothesis") or 0)<r13_nw_tries_max("hypothesis"),
        "hyp_final":lambda:not (r13_v111_value("meeting:hypothesis") is None and (r13_v111_value("tries:hypothesis") or 0)<r13_nw_tries_max("hypothesis")),
        # Audit d11-14 #3: a lost hypothesis meeting after some issues were won.
        "hyp_lose_some_won":lambda:r13_v111_value("meeting:hypothesis")=="lose" and any(r13_v111_value("hyp_issue:%d"%i)=="won" for i in (1,2,3,4)),
        "hyp_lose_none_won":lambda:not (r13_v111_value("meeting:hypothesis")=="lose" and any(r13_v111_value("hyp_issue:%d"%i)=="won" for i in (1,2,3,4))),
        # Audit d11-14 #8: Nabi changed her room 13 testimony only on the murder route.
        "soup_lose_nabi_murder":lambda:r13_v111_value("meeting:soup")=="lose" and r13_v111_value("soup_lose_kind")=="nabi" and r13_v111_value("route7")=="murder",
        "soup_lose_nabi_prevented":lambda:r13_v111_value("meeting:soup")=="lose" and r13_v111_value("soup_lose_kind")=="nabi" and r13_v111_value("route7")!="murder",
        # Audit d11-14 #12: firewood is really at the school (carrier received or box picked up).
        "wood12_missing":lambda:not (r13_v111_value("warm_support_arrived") or r13_v111_value("heat_box_received")),
        # Audit d11-14 #10, #13, #6, #7.
        "blanket_undecided":lambda:r13_v111_value("meeting:blanket") is None,
        "blanket_partial":lambda:r13_v111_value("meeting:blanket")=="partial",
        "siluk_not_listed":lambda:r13_v111_value("listed:resident_siluk") is not True,
        "daram_listed_unhanded":lambda:r13_v111_value("listed:daram") is True and not r13_v111_value("handed:daram"),
        # Event 11: the altar, Bomi, and the endings.
        "has_ledger":lambda:r13_v111_owned("NW_NEOUL_LEDGER"),
        "no_ledger":lambda:not r13_v111_owned("NW_NEOUL_LEDGER"),
        "has_burnt_page":lambda:r13_v111_owned("NW_BURNT_PAGE"),
        "altar_win":lambda:r13_v111_value("meeting:altar")=="win",
        "altar_partial":lambda:r13_v111_value("meeting:altar")=="partial",
        "altar_lose":lambda:r13_v111_value("meeting:altar")=="lose",
        "medicine_locked":lambda:r13_v111_value("medicine_locked") is True,
        "medicine_unchecked":lambda:not r13_v111_value("medicine_locked"),
        "daram_not_deal_freed":lambda:r13_v111_value("daram_deal_freed") is not True,
        "warm_support_pending":lambda:not r13_v111_value("warm_support_arrived"),
        "warm_support_ready":lambda:r13_v111_value("warm_support_arrived") is True,
        "family_priority":lambda:r13_v111_value("outcome13")=="family_priority",
        "reader_nabi":lambda:not (r13_v111_value("departed:nabi") or not r13_v111_person_alive("nabi")),
        "reader_tosil":lambda:bool(r13_v111_value("departed:nabi") or not r13_v111_person_alive("nabi")),
        "granny_held_win":lambda:r13_v111_value("OWL_ALIVE") is False and r13_v111_value("meeting:room13")=="win",
        "granny_room13_partial":lambda:r13_v111_value("OWL_ALIVE") is False and r13_v111_value("meeting:room13")=="partial",
        "granny_room13_lose":lambda:r13_v111_value("OWL_ALIVE") is False and r13_v111_value("meeting:room13")=="lose",
        # 2026-10-24 동기 줄 4차(문구시안.md): 3일 회의에서 톡이 풀려난 판(이김·부분). 짐은 listed:resident_tok 이 받는다.
        "tok_freed3":lambda:r13_v111_value("meeting:lamp") in ("win","partial") and r13_v111_value("listed:resident_tok") is not True,
        # 13일 수레 앞: 다람이 곁에 있고, 방금까지 수레에 묶여 있던 판(listed:daram)이 아닐 때만 빈 칸을 묻는다.
        "daram_watching13":lambda:r13_v111_actor_ready("daram") and r13_v111_value("listed:daram") is not True,
        # 14일 아침: 엄마와 다람이 함께 학교에 있을 때만 셋이 말한다.
        "mom_daram_ready14":lambda:r13_v111_actor_ready("mom") and r13_v111_actor_ready("daram"),
        # 2026-10-24 행동 검수(action-review-20261024/적용보고.md). 이미 있는 값만 읽는다.
        # 대안 1: 회의에서 틀린 뒤 기회가 한 번만 남았을 때 결정하는 사람이 참을성이 바닥났음을 말한다.
        "lamp_last_try":lambda:r13_v111_value("meeting:lamp") is None and r13_nw_tries_left("lamp")==1,
        "gate_post_last_try":lambda:r13_v111_value("meeting:gate_post") is None and r13_nw_tries_left("gate_post")==1,
        # 4-1: 3일 회의를 진 판은 보호시설 설명을 이미 들었다. 5-1: 밤이를 풀어 준 판.
        "lamp_not_lose":lambda:r13_v111_value("meeting:lamp")!="lose",
        "gate_post_win":lambda:r13_v111_value("meeting:gate_post")=="win",
        # 소유자 결정 4(탈출 축): 3일에 톡에게 「쇠 토막을 구해 와야 해요」를 들은 판에서, 5일 식당에 까로가 있을 때.
        "karo_heard_iron5":lambda:r13_v111_value("meeting:lamp") in ("win","partial") and r13_v111_value("listed:resident_tok") is not True and r13_v111_actor_ready("karo"),
        # 11-11: 학교 물자를 아직 넘기지 않아 「학교 물자 인계를 먼저」가 메뉴에 남는 판.
        "school_supply_pending":lambda:not r13_v111_value("school_supply_handed"),
        # 12-1·13-3: 돌목이 그 자리에 있을 때(원래 줄도 같은 확인을 한다).
        "guard_ready":lambda:r13_v111_actor_ready("guard"),
        # 13-4: 다람이 수레를 보지 못하는 판은 엄마가 같은 말을 한다.
        "daram_not_watching13":lambda:not (r13_v111_actor_ready("daram") and r13_v111_value("listed:daram") is not True),
        # 13-10: 까로와 돌목이 둘 다 곁에 있으면 셋이 주고받고, 아니면 아빠의 속말 한 줄.
        "karo_guard_ready13":lambda:r13_v111_actor_ready("karo") and r13_v111_actor_ready("guard"),
        "karo_guard_not_ready13":lambda:not (r13_v111_actor_ready("karo") and r13_v111_actor_ready("guard")),
        # 14-5: 부리가 공구를 챙긴 판에서 촌장 동행을 아직 묻기 전.
        "buri_site_ask14":lambda:bool(r13_v111_value("buri_device_consent")) and not r13_v111_value("mayor_site_decided") and r13_v111_person_alive("buri"),
        # 대안 9: 마을의 아침인데 이 아침을 함께 못 맞은 사람이 있는 판(진엔딩을 막는 까닭 하나).
        "morning_with_loss14":lambda:r13_v111_value("ending14")=="morning" and r13_nw_loss_count()>0 and r13_v111_actor_ready("mom") and r13_v111_actor_ready("daram"),
        # 2026-10-24 대승리(GRAND_WIN_DESIGN.md 1·2장, 결정 4·7): 5일 빨래터에서 엿들은 판, 7일 막내에게서 숨긴 자리를 들은 판.
        "laundry_overheard5":lambda:r13_v111_value("grand_laundry_seen5") is True,
        "ticket_spot_kid7":lambda:r13_v111_value("grand_ticket_spot_kid") is True and r13_v111_value("grand_laundry_seen5") is not True,
        # 7일 불 회의를 배급표로 이긴 판(대승리)과 보통으로 이긴 판.
        "fire_grand":lambda:r13_v111_value("grand:fire") is True,
        "fire_win_plain":lambda:r13_v111_value("meeting:fire")=="win" and r13_v111_value("grand:fire") is not True,
        "karo_ready11":lambda:r13_v111_actor_ready("karo"),
        # 12일 수프 회의를 돌아온 그릇으로 이긴 판. 돌목이 그 자리에 있으면 그가 칸을 무효로 적는다.
        "grand_soup":lambda:r13_v111_value("grand:soup") is True,
        "grand_soup_guard":lambda:r13_v111_value("grand:soup") is True and r13_v111_actor_ready("guard"),
        "grand_soup_noguard":lambda:r13_v111_value("grand:soup") is True and not r13_v111_actor_ready("guard"),
        # 이송 예정 칸이 무효가 된 판(수프 대승리, 또는 국을 미리 막은 판에서 돌목에게 그릇을 보인 판).
        "list_voided":lambda:r13_v111_value("transfer_list_voided") is True,
        "list_not_voided":lambda:r13_v111_value("transfer_list_voided") is not True,
        "daram_listed_voided13":lambda:r13_v111_value("listed:daram") is True and r13_v111_value("transfer_list_voided") is True and r13_v111_actor_ready("guard"),
        "daram_listed_unvoided13":lambda:r13_v111_value("listed:daram") is True and not (r13_v111_value("transfer_list_voided") is True and r13_v111_actor_ready("guard")),
        "daram_departs13":lambda:r13_v111_value("listed:daram") is True and r13_v111_value("transfer_list_voided") is not True,
    }
    for _nw_who in ("resident_piko","kid_kkomi","resident_owlgp","resident_nero","kid_dodam","neoul","resident_momo","v111_lowerroad_elder"):
        R13_NW_WHEN["dead:"+_nw_who]=(lambda w=_nw_who:w in r13_nw_dead())
    # One condition per person who can be on the transfer list (same names as R13_NW_LISTABLE).
    R13_NW_LIST_NAMES=("resident_tok","bami","resident_bori","nabi","daram","resident_owlgp","resident_piko","resident_siluk","resident_guldol","resident_teacher","mom","dad")
    for _nw_person in R13_NW_LIST_NAMES:
        R13_NW_WHEN["listed:"+_nw_person]=(lambda p=_nw_person:r13_v111_value("listed:"+p) is True)
    # Impact direction names (systems/room13_impact_fx.rpy; that file loads later, so the names live here).
    R13_NW_FX=("jolt","shake","slam","flash")
    R13_NW_CUT_SPECIAL=("bell","v111_blanket_before","v111_blanket_after","v111_reunion_far","v111_reunion_close")
    def r13_nw_replace_variants(rid):
        """A replace entry is one variant or a list of variants (first whose condition holds wins)."""
        entry=R13_NW_TEXT["replace"].get(rid)
        if entry is None:return []
        # Ren'Py rebinds list/dict in the store; JSON gives the plain types, so test by shape.
        return [entry] if hasattr(entry,"get") else entry
    def r13_nw_replacement(rid):
        for variant in r13_nw_replace_variants(rid):
            if R13_NW_WHEN[variant.get("when","always")]():return variant
        return None
    def r13_nw_drop_item(item):
        return (item,"always") if isinstance(item,str) else (item.get("id"),item.get("when","always"))
    def r13_nw_dropped(rid):
        return any(r==rid and R13_NW_WHEN[w]() for r,w in (r13_nw_drop_item(i) for i in R13_NW_TEXT["drop"]))
    def r13_nw_text_problems():
        """Every broken reference in the loaded files, as readable strings."""
        out=[];records=R13_V111["records"];seen=set()
        for rid in R13_NW_TEXT["replace"]:
            if rid not in records:out.append("replace: unknown record "+rid);continue
            for variant in r13_nw_replace_variants(rid):
                if not variant.get("text"):out.append("replace: empty text "+rid)
                elif variant.get("when","always") not in R13_NW_WHEN:out.append("replace: unknown condition "+rid)
                elif variant.get("fx") and variant["fx"] not in R13_NW_FX:out.append("replace: unknown fx "+rid)
        for item in R13_NW_TEXT["drop"]:
            rid,when=r13_nw_drop_item(item)
            if rid not in records:out.append("drop: unknown record "+str(rid))
            if when not in R13_NW_WHEN:out.append("drop: unknown condition "+str(rid))
        for where in ("before","after","blocks"):
            for rid,rows in R13_NW_TEXT[where].items():
                if where!="blocks" and rid not in records:out.append(where+": unknown record "+rid)
                if where=="blocks" and not rows:out.append("blocks: empty block "+rid)
                for row in rows:
                    nid=row.get("id","")
                    if not nid.startswith("NW_") or nid in seen or nid in records:out.append(where+": bad or repeated id "+repr(nid))
                    seen.add(nid)
                    if not row.get("text"):out.append(where+": empty text "+nid)
                    if row.get("kind","dialogue") not in ("dialogue","narration","thought"):out.append(where+": unknown kind %s %s"%(nid,row.get("kind")))
                    if row.get("kind")=="thought" and (row.get("speaker")!="아빠" or row["text"].startswith("(")):out.append(where+": thought must be the father's, without brackets "+nid)
                    if row.get("speaker") is not None and row["speaker"] not in MS14_SPEAKERS:out.append(where+": unknown speaker %s %s"%(nid,row["speaker"]))
                    if row.get("when","always") not in R13_NW_WHEN:out.append(where+": unknown condition %s %s"%(nid,row.get("when")))
                    if row.get("beat") and row["beat"] not in R13_MEETING_BEATS:out.append(where+": unknown meeting beat %s %s"%(nid,row["beat"]))
                    if row.get("fx") and row["fx"] not in R13_NW_FX:out.append(where+": unknown fx %s %s"%(nid,row["fx"]))
                    cut=row.get("cut")
                    if cut and cut not in R13_NW_CUT_SPECIAL and not (cut.startswith("ev:") and renpy.loadable("assets/evidence/%s.webp"%cut[3:])) and not renpy.loadable("assets/room13-ep-%s.webp"%cut):out.append(where+": missing cut art %s %s"%(nid,cut))
        for key in R13_NW_TEXT["evidence"]:
            if key not in R13_V111["evidence"]:out.append("evidence: unknown key "+key)
        return out
    for _nw_binding,_nw_titles in R13_NW_TEXT["titles"].items():
        for _nw_index,_nw_title in _nw_titles.items():
            R13_V111_BINDINGS[_nw_binding]["options"][int(_nw_index)]["title"]=_nw_title
    _nw_problems=r13_nw_text_problems()
    if _nw_problems:raise Exception("New-world text files are inconsistent: "+"; ".join(_nw_problems[:8]))

    _r13_nw_authored_line=r13_v111_line
    def r13_v111_line(rid):
        packet=_r13_nw_authored_line(rid)
        revised=r13_nw_replacement(rid)
        if revised:
            packet=(packet[0],revised["text"])+tuple(packet[2:])
            # 0.19.98: a revised line may carry its own expression (owner: "대사에 맞는 표정").
            if revised.get("expression") and len(packet)>2 and isinstance(packet[2],dict):
                packet=(packet[0],packet[1],dict(packet[2],expression=revised["expression"],pose=revised["expression"]))+tuple(packet[3:])
            # 0.20.7: a revised authored line may also raise or clear a picture cut ("ev:<record>" = the
            # record's picture held up in the scene, owner "편지·그림·과자 봉지를 직접 들여다보게").
            if "cut" in revised and len(packet)>2 and isinstance(packet[2],dict):
                packet=(packet[0],packet[1],dict(packet[2],cut=revised["cut"]))+tuple(packet[3:])
            # 0.19.99: impact direction for the line (systems/room13_impact_fx.rpy).
            if revised.get("fx") and len(packet)>2 and isinstance(packet[2],dict):
                packet=(packet[0],packet[1],dict(packet[2],fx=revised["fx"]))+tuple(packet[3:])
        return packet
    def r13_nw_added_line(row):
        if row.get("kind")=="thought":
            # The father's unspoken thought, shown like the authored thought lines.
            return ("dad","("+row["text"]+")",dict(no_lead=True,thought=True,expression="thinking",pose="thinking"))
        who=MS14_SPEAKERS.get(row.get("speaker")) if row.get("speaker") is not None else None
        if who and not r13_v111_person_alive(who):raise Exception("Absent/dead new-world speaker: "+row["id"])
        slot=row.get("expression") or "neutral"
        options=dict(no_lead=True,expression=slot,pose=slot)
        if row.get("cut"):options["cut"]=row["cut"]
        # Meeting stage beat (systems/room13_meeting_direction.rpy), used only inside a meeting.
        if row.get("beat"):options["beat"]=row["beat"]
        if row.get("fx"):options["fx"]=row["fx"]
        return (who,row["text"],options)
    def r13_nw_wrong_final_lines():
        # 2026-10-24 지시서 01 4번: 회의 기회를 다 쓴 오답 뒤 처음 나오는 대사 묶음 끝에 아빠 속말 한 줄
        # (r13_nw_wrong_queue 가 남겨 둔 것, room13_v111_newworld_rules.rpy). 한 번 보이면 지운다.
        pending=globals().get("r13_nw_wrong_pending")
        if not pending or pending[0]!="final":return []
        globals()["r13_nw_wrong_pending"]=None
        return [r13_nw_added_line(dict(kind="thought",text=pending[1]))]
    def r13_v111_lines(rids):
        """Authored lines with the reviewed new-world revisions around them."""
        out=[]
        for rid in rids:
            for row in R13_NW_TEXT["before"].get(rid,()):
                if R13_NW_WHEN[row.get("when","always")]():out.append(r13_nw_added_line(row))
            if not r13_nw_dropped(rid):
                packet=r13_v111_line(rid)
                # The authored record rides with its line, so approved per-line art
                # still finds it after lines are added before it or its text changes.
                out.append((packet[0],packet[1],dict(packet[2],line_id=rid))+tuple(packet[3:]))
            for row in R13_NW_TEXT["after"].get(rid,()):
                if R13_NW_WHEN[row.get("when","always")]():out.append(r13_nw_added_line(row))
        return out+r13_nw_wrong_final_lines()
    def r13_nw_block(name):
        """Lines of a new-world block (a new meeting) whose conditions hold."""
        if name not in R13_NW_TEXT["blocks"]:raise Exception("Unknown new-world block: "+str(name))
        return [r13_nw_added_line(row) for row in R13_NW_TEXT["blocks"][name] if R13_NW_WHEN[row.get("when","always")]()]+r13_nw_wrong_final_lines()
    _r13_nw_context_match=r13_dialogue_context_match
    def r13_dialogue_context_match(identity,index,packet,pose):
        rid=packet[2].get("line_id") if len(packet)>2 and isinstance(packet[2],dict) else None
        if not rid:return _r13_nw_context_match(identity,index,packet,pose)
        if pose not in R13_FULLBODY_PLAIN:return None
        for cue in R13_DIALOGUE_CONTEXT_ART["bindings"]:
            if cue.get("line_id")==rid and cue["identity"]==identity and cue["person"]==packet[0]:
                return cue
        return None
    for _nw_key,_nw_spec in R13_NW_TEXT["evidence"].items():
        _nw_rid="V111:"+_nw_key
        if _nw_spec.get("name"):
            ROOM13["evidence"][_nw_rid]["name"]=_nw_spec["name"]
            R13_RECORD_SHORT[_nw_rid]=_nw_spec["name"]
        for _nw_variant,_nw_text in _nw_spec.get("variants",{}).items():
            if _nw_variant not in R13_V111["evidence"][_nw_key]["variants"]:raise Exception("Unknown evidence variant: %s %s"%(_nw_key,_nw_variant))
            R13_V111["evidence"][_nw_key]["variants"][_nw_variant]=_nw_text
        for _nw_variant,_nw_text in _nw_spec.get("add_variants",{}).items():
            if _nw_variant in R13_V111["evidence"][_nw_key]["variants"]:raise Exception("Evidence variant already exists: %s %s"%(_nw_key,_nw_variant))
            R13_V111["evidence"][_nw_key]["variants"][_nw_variant]=_nw_text
        ROOM13["evidence"][_nw_rid]["establishes"]=next(iter(R13_V111["evidence"][_nw_key]["variants"].values()))
