# New-world meetings on the existing meeting stage (owner, 2026-10-22: "전부 기존 걸 쓰자").
# The authored V1.1.1 meetings ran on the plain field dialogue screen. They now use the
# round-table / field / altar meeting stage of the older meetings: speaker in the middle,
# neighbours at both sides, the camera turning to whoever speaks, the issue strip on top.
# Nothing here decides a meeting: dates, proofs, chances and results stay in the rules file.
# A meeting is the set of generator labels below (dev/test_newworld_text.py keeps it in step).
init 321 python:
    R13_NW_MEETINGS={
        'gate':dict(kind='field',issue='다람이 함께 들어갈 수 있는가',cast=['돌목', '다람'],
            labels=['gate_investigate', 'gate_read_original', 'gate_read_rules', 'gate_reread_list', 'gate_purpose', 'gate_lodging', 'gate_proof', 'gate_proven_dispatch', 'gate_proven', 'gate_early', 'gate_number', 'gate_wrong', 'gate_hint', 'gate_reason']),
        'lamp':dict(kind='field',issue='3번 등의 돌을 꺼낸 사람은 누구인가',cast=['너울', '실룩', '톡', '백 부인', '초롱', '바둑이'],
            labels=['trial_open', 'trial_repair', 'trial_repair_ok', 'trial_sale', 'trial_sale_ok', 'trial_knife', 'trial_knife_records', 'knife_fit', 'knife_wrong', 'trial_latch', 'trial_latch_ok', 'trial_stone', 'trial_stone_ok', 'badugi_arrives', 'trial_piko', 'trial_alive', 'trial_dead', 'trial_choices', 'stone_choice', 'stone_return', 'stone_defer', 'custody_choice', 'silluk_report', 'silluk_transfer', 'trial_wrong', 'trial_hint', 'trial_wrong_sale', 'trial_hint_sale', 'trial_wrong_latch', 'trial_hint_latch', 'trial_wrong_stone', 'trial_hint_stone']),
        'gate_post':dict(kind='field',issue='초소에서 돌목을 문 사람은 밤이인가',cast=['너울', '밤이', '돌목', '네로', '바둑이', '다람', '콩이'],
            labels=['hearing5', 'proof5', 'wrong5', 'hint5', 'bami_clear5']),
        'fire':dict(kind='field',issue='창고 문 앞에 불을 놓은 사람은 누구인가',cast=['누비', '보리', '너울', '나비'],
            labels=['day7', 'children_school7', 'children_here7', 'nubi_children_school7', 'nubi_children_receipt7', 'nubi_children_received7', 'bori_witness7', 'bori_witness_heard7', 'nubi_proof7', 'nubi_wrong7', 'nubi_admission7', 'responsibility7', 'fire_basis_route7', 'empty_fire_basis7', 'rescue_fire_basis7', 'responsibility_wrong7', 'responsibility_answers7']),
        'room13':dict(kind='room',issue='13호실에서 부엉이 어르신에게 무슨 일이 있었나',cast=['할머니', '촌장', '너울', '도토', '나비', '서리', '다람'],
            labels=['hearing10', 'wound_proof10', 'wound_answer10', 'passage_proof10', 'passage_answer10', 'hearing_wrong10', 'passage_wrong10', 'hearing_hint10', 'owner10', 'owner_proof10', 'owner_answer10', 'owner_tok10', 'owner_copy10', 'time10', 'time_proof10', 'time_answer10', 'contact_proof10', 'contact_answer10', 'owner_wrong10', 'time_wrong10', 'contact_wrong10']),
        'records':dict(kind='room',issue='엄마가 맡긴 기록을 누가 받아야 하는가',cast=['부엉이', '할머니', '너울', '다람'],
            labels=['prevent_hearing10', 'authority_proof10', 'authority_answer10', 'writing_proof10', 'writing_answer10', 'pocket10', 'pocket_answer10', 'family_paper10', 'private_handoff10', 'owl_invitation10', 'public_paper10', 'authority_wrong10', 'writing_wrong10', 'writing_partial10']),
        'hypothesis':dict(kind='room',issue='사람이 무너지는 까닭은 무엇인가',cast=['판돌', '백 부인', '선생님', '돌목', '굴돌', '촌장', '초롱'],
            labels=['hypothesis11', 'hyp0_menu11', 'hyp0_sick11', 'hyp0_call11', 'hyp0_old11', 'hyp0_won11', 'hyp1_q11', 'hyp1_badreason11', 'hyp1_reason11', 'hyp1_proof11', 'hyp1_wrong11', 'hyp1_lost11', 'hyp1_won11', 'hyp2_q11', 'hyp2_badreason11', 'hyp2_reason11', 'hyp2_proof11', 'hyp2_wrong11', 'hyp2_lost11', 'hyp2_won11', 'hyp3_q11', 'hyp3_badreason11', 'hyp3_reason11', 'hyp3_proof11', 'hyp3_wrong11', 'hyp3_lost11', 'hyp3_won11', 'hyp4_q11', 'hyp4_badreason11', 'hyp4_reason11', 'hyp4_proof11', 'hyp4_wrong11', 'hyp4_lost11', 'hyp4_won11', 'hyp5_q11', 'hyp5_badreason11', 'hyp5_reason11', 'hyp5_proof11', 'hyp5_wrong11', 'hyp5_lost11', 'hyp5_won11', 'hyp_lost_gate11', 'hyp_end11']),
        'soup':dict(kind='room',issue='아이들이 먹은 수프에 무엇이 들어갔나',cast=['선생님', '나비', '서리', '너울', '돌목', '다람'],
            labels=['soup_hearing12', 'meal_observations12', 'bottle_match12', 'bottle_matched12', 'seal_proof12', 'seal_answer12', 'seal_late12', 'seal_pre12', 'handling12', 'handling_route12', 'handling_late12', 'handling_pre12', 'medical_arrival12', 'soup_final12', 'soup_conclusion12', 'soup_conclusion_route12', 'conclusion_late12', 'conclusion_pre12', 'confessed12', 'list_proof12', 'list_wrong12', 'list_won12', 'soup_after_route12', 'medicine_wrong12', 'fragment_wrong12', 'soup_lost12', 'soup_hint12', 'soup_hint_final12']),
        'blanket':dict(kind='field',issue='모과 씨가 판돌 씨를 기다린다는 말은 사실인가',cast=['촌장', '판돌', '바둑이', '다람'],
            labels=['blanket_lie13', 'mending_proof13', 'mending_answer13', 'badook_proof13', 'badook_wrong13', 'badook_won13', 'mending_rest13', 'mending_wrong13', 'mending_hint13']),
        'piko':dict(kind='field',issue='3번 돌을 빼라고 시킨 사람은 누구인가',cast=['너울', '실룩', '바둑이', '판돌'],
            labels=['stop_cart13', 'rein13', 'rein_ledger13p', 'rein_ledger13', 'rein_painting13p', 'rein_won13', 'rein_wrong13a', 'rein_wrong13b', 'rein_wrong13']),
        'altar':dict(kind='stone',issue='사람을 제단에 보내야 마을이 사는가',cast=['촌장', '엄마', '바둑이', '다람'],
            labels=['altar14', 'mayor_interview14', 'altar1_q14', 'altar1_proof14', 'altar1_wrong14', 'altar1_won14', 'altar2_q14', 'altar2_proof14', 'altar2_wrong14', 'altar2_won14', 'altar3_q14', 'altar3_proof14', 'altar3_wrong14', 'altar3_won14', 'altar4_q14', 'altar4_proof14', 'altar4_wrong14', 'altar4_won14', 'altar_close14', 'altar_lost14']),
    }
    R13_NW_MEETING_OF={("r13_v111_"+l):k for k,m in R13_NW_MEETINGS.items() for l in m["labels"]}
    # Helpers called from inside a meeting that must not close it.
    R13_NW_MEETING_KEEP=("r13_v111_proof","r13_v111_proof_again")
    # Leaving for the map or a wait hides the stage; the next line of the same meeting brings it back.
    R13_NW_MEETING_PAUSE=("r13_v111_travel","r13_v111_wait","r13_v111_wait_again")
    for _nw_key,_nw_m in R13_NW_MEETINGS.items():
        R13_MEETING_VENUES["nw_"+_nw_key]=(None,_nw_m["kind"],None)

    def r13_nw_meeting_claim(claim):
        return isinstance(claim,str) and claim.startswith("NW:") and claim[3:] in R13_NW_MEETINGS
    def r13_nw_meeting_key(claim):
        return claim[3:] if r13_nw_meeting_claim(claim) else None

    def r13_nw_stage_cast_ids(key):
        """The meeting's speakers who are alive and, when the scene lists them, actually there."""
        m=R13_NW_MEETINGS[key]
        ids=[MS14_SPEAKERS.get(n) for n in m["cast"]]
        ids=[p for p in ids if p and p in CAST and p!=r13_viewpoint() and r13_v111_person_alive(p)]
        here=set((store.room13.get("v111",{}) or {}).get("people",[]) or [])
        present=[p for p in ids if p in here]
        return present if len(present)>=2 else ids

    def r13_nw_stage_begin(key):
        store.r13_nw_meeting_cast=r13_nw_stage_cast_ids(key)
        if not store.r13_nw_meeting_cast:return
        r13_meeting_direct_end()
        for name in ("r13_meeting_intro","r13_meeting_interrupting","r13_meeting_replaying","r13_meeting_live_active"):
            setattr(store,name,False)
        store.r13_meeting_claim="NW:"+key
        store.r13_meeting_previous_focus=None
        store.r13_meeting_focus=store.r13_nw_meeting_cast[0]
        store.r13_meeting_shot_revision+=1
        store.r13_meeting_active=True
        renpy.hide("r13_visitor")

    def r13_nw_stage_end():
        if not r13_nw_meeting_claim(getattr(store,"r13_meeting_claim",None)):return
        r13_meeting_direct_end()
        store.r13_meeting_active=False
        store.r13_meeting_claim=None
        store.r13_meeting_focus=None
        store.r13_meeting_previous_focus=None
        renpy.hide_screen("r13_meeting_cut_in")

    def r13_nw_stage_label(name,abnormal=False):
        if name in R13_NW_MEETING_KEEP:return
        if name=="r13_lines":
            pending=getattr(store,"r13_nw_pending",None)
            if pending and getattr(store,"r13_meeting_claim",None)!="NW:"+pending and not (getattr(store,"r13_meeting_active",False) and getattr(store,"r13_meeting_claim",None) in R13_DEBATE):
                r13_nw_stage_begin(pending)
            return
        if name in R13_NW_MEETING_OF:
            key=R13_NW_MEETING_OF[name]
            if getattr(store,"r13_meeting_claim",None) not in (None,"NW:"+key):r13_nw_stage_end()
            store.r13_nw_pending=key
            return
        if name in R13_NW_MEETING_PAUSE:
            r13_nw_stage_end()
            return
        if name.startswith("r13_v111_") or name in ("r13_roam","r13_day"):
            store.r13_nw_pending=None
            r13_nw_stage_end()
    config.label_callbacks.append(r13_nw_stage_label)

    _r13_nw_debate_session=r13_debate_session
    def r13_debate_session(claim):
        key=r13_nw_meeting_key(claim)
        return "nw_"+key if key else _r13_nw_debate_session(claim)

    _r13_nw_meeting_cast=r13_meeting_cast
    def r13_meeting_cast(claim,session,speaker=None):
        if r13_nw_meeting_claim(claim):
            return [(p,None) for p in (getattr(store,"r13_nw_meeting_cast",None) or [])]
        return _r13_nw_meeting_cast(claim,session,speaker)

    _r13_nw_meeting_focus_person=r13_meeting_focus_person
    def r13_meeting_focus_person(claim):
        if r13_nw_meeting_claim(claim):
            people=[p for p,_ in r13_meeting_cast(claim,None)]
            focused=getattr(store,"r13_meeting_focus",None)
            return focused if focused in people else (people[0] if people else None)
        return _r13_nw_meeting_focus_person(claim)

    _r13_nw_meeting_plate=r13_meeting_plate
    def r13_meeting_plate(session,close=False):
        if isinstance(session,str) and session.startswith("nw_") and r13_meeting_kind(session) in ("field","room"):
            # Field and indoor meetings stand in the scene's own place picture.
            location=store.room13["location"]
            return Transform(r13_background(R13_PLACES.get(location,(None,location))[1]),xysize=(1280,720),nearest=True)
        return _r13_nw_meeting_plate(session,close)

    _r13_nw_meeting_header=r13_meeting_header
    def r13_meeting_header(session):
        if isinstance(session,str) and session.startswith("nw_"):
            place=R13_PLACES.get(store.room13["location"],("",))[0]
            return "%s 회의 · %d일째"%(place,store.room13["day"])
        return _r13_nw_meeting_header(session)

    _r13_nw_meeting_direct_line=r13_meeting_direct_line
    def r13_meeting_direct_line(identity,index,packet,expression,pose):
        claim=getattr(store,"r13_meeting_claim",None)
        if getattr(store,"r13_meeting_active",False) and r13_nw_meeting_claim(claim):
            options=packet[2] if len(packet)>2 and isinstance(packet[2],dict) else {}
            beat=options.get("beat") if options.get("beat") in R13_MEETING_BEATS else "listen"
            person=packet[0]
            speaking=person in CAST and person!=r13_viewpoint()
            # Someone who joins mid-meeting (e.g. Badook arriving) takes a seat when first speaking.
            people=list(getattr(store,"r13_nw_meeting_cast",None) or [])
            if speaking and person not in people and r13_v111_person_alive(person):
                store.r13_nw_meeting_cast=people+[person]
            store.r13_meeting_direction=dict(beat=beat,claim=claim)
            # The orbit camera reads the speaker's pose from here (room13_meeting_camera.rpy).
            store.r13_meeting_line_token=(identity,index,person,packet[1])
            store.r13_meeting_direction_poses={person:pose} if speaking else {}
            store.r13_meeting_listener=None
            store.r13_meeting_art_slots={}
            store.r13_meeting_reaction=None
            if beat=="interrupt" and persistent.room13_motion and not renpy.is_skipping():
                renpy.show_screen("r13_meeting_cut_in",caption=R13_MEETING_BEATS[beat][0])
            return expression,pose
        return _r13_nw_meeting_direct_line(identity,index,packet,expression,pose)

default r13_nw_pending = None
default r13_nw_meeting_cast = []

screen r13_nw_meeting_chrome(claim):
    $ key=r13_nw_meeting_key(claim)
    $ left=r13_nw_tries_left(key)
    frame:
        area (24,18,900,66) padding (16,8) background R13PaperFrame()
        add R13AntiqueIcon("meeting_"+r13_meeting_kind(r13_debate_session(claim)),size=30) xpos 0 ypos 8
        vbox:
            xpos 42
            spacing 2
            text (r13_meeting_header(r13_debate_session(claim))+"  ·  남은 기회 %d / %d"%(left,R13_NW_TRIES)) size r13_read_size(15,17) color "#795d40"
            text ("쟁점 · "+R13_NW_MEETINGS[key]["issue"]) size r13_read_size(21,25) color "#493b30"
        add Solid("#d6bf98") xpos 0 ypos 51 xysize (868,3)
        if left<R13_NW_TRIES:
            add Solid("#a88043") xpos 0 ypos 51 xysize (int(868*left/float(R13_NW_TRIES)),3)
