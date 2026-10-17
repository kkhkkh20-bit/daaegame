# Live presentation and public opinions reuse the canonical debate judge.
default r13_meeting_pending_resume = None
default r13_meeting_live_active = False
default r13_meeting_live_sid = None
default r13_meeting_live_command = None
default r13_meeting_resume_listening = False
default r13_meeting_live_lap = 0

init 100 python:
    # Brief public responses add rhythm without revealing gated witness facts,
    # opening hidden statements or claiming that preparations were completed.
    R13_MEETING_REJOINDERS={
        "C1":{"s1":("resident_seori","본 것과 짐작한 것은 구분해서 말해 주십시오."),"s2":("granny","그래서 지금 무슨 말을 하시려는 거예요?")},
        "C2":{"s1":("buri","잠깐요. 무슨 일이었는지부터 차례로 들어요."),"s2":("nabi","직접 본 일과 들은 말을 섞지는 말아요."),"s3":("resident_seori","그때 방에 있던 사람이 누구인지 확인하겠습니다.")},
        "C3":{"s1":("nabi","첫 비명 때는 할머니와 함께 있었어요."),"s2":("nabi","저도 제 차례에, 제가 본 것만 말할게요."),"s3":("resident_seori","그 길은 직접 확인한 자료로 따지겠습니다.")},
        "C4":{"s0":("nabi","그 말은 자료를 보고 확인해요."),"s1":("nabi","제 이름이 나오는 이야기라면 끝까지 듣고 말할게요."),"s2":("buri","촛대 이야기는 대충 넘기지 말아요."),"s3":("resident_seori","그때 무엇을 알고 있었는지 듣겠습니다.")},
        "F1":{"s1":("nabi","가족들이 듣고 있어요. 그 판단은 분명해야 해요."),"s2":("mom","기록에 남은 말도 같이 들어요.")},
        "F2":{"s4":("buri","낮과 저녁은 쓰는 힘이 다르니까요."),"s1":("mom","그날 불이 올라온 건 사실이에요."),"s2":("buri","같은 일을 계속해도 되는지가 문제잖아요."),"s3":("nabi","다른 길이 정말 없는지 끝까지 들어요.")},
        "F3":{"s1":("resident_bori","잘 곳부터 따져야 한다는 데는 동의하오."),"s2":("buri","사람 수에 맞게 세어야 해요."),"s3":("mom","실제로 맡을 사람을 정했는지 확인해요.")},
        "F4":{"s1":("mom","제 이야기를 제 입으로 할 차례도 주세요."),"s2":("nabi","그 요청을 보낸 때부터 차례로 말해요.")},
    }

    def r13_meeting_live_ids(claim,start):
        ids=[st["id"] for st in r13_debate_statements(claim) if r13_debate_visible(claim,st) and not r13_debate_is_broken(claim,st["id"])]
        return ids[ids.index(start):]+ids[:ids.index(start)] if start in ids else ids

    def r13_meeting_live_next(claim,sid,step=1):
        visible=[st["id"] for st in r13_debate_statements(claim) if r13_debate_visible(claim,st)]
        if not visible:return None
        start=visible.index(sid) if sid in visible else -1
        for offset in range(1,len(visible)+1):
            candidate=visible[(start+step*offset)%len(visible)]
            if not r13_debate_is_broken(claim,candidate):return candidate
        return None

    def r13_meeting_statement_text(claim,sid):
        # The player locates the contradiction; authored brackets are not a hint.
        return r13_debate_statement(claim,sid)["text"].replace("【","").replace("】","")

    def r13_meeting_heard(claim,sid):
        return claim+":"+sid in (store.room13 or {}).get("meeting_heard",[])

    def r13_meeting_prepare_live_line(identity):
        if not identity.startswith("meeting:live:"):return
        # A cyclic transcript must always leave an interaction to interrupt.
        store.r13_fast_all=False;store.r13_fast_read=False
        renpy.config.skipping=None

    def r13_meeting_mark_heard(identity,index):
        if not identity.startswith("meeting:live:") or index!=0:return
        key=identity[len("meeting:live:"):]
        heard=list((store.room13 or {}).get("meeting_heard",[]))
        if key not in heard:
            heard.append(key);r13_edit(meeting_heard=heard)

    def r13_meeting_live_rows(claim,sid):
        st=r13_debate_statement(claim,sid)
        rows=[(st["who"],r13_meeting_statement_text(claim,sid))]
        reply=R13_MEETING_REJOINDERS.get(claim,{}).get(sid)
        if not reply and claim.startswith("Q") and sid==r13_debate_statements(claim)[0]["id"]:
            # Only an attendee; no random witness, new fact, or persuasion effect.
            people=[p for p,_ in r13_meeting_cast(claim,r13_debate_session(claim)) if p not in (st["who"],r13_viewpoint())]
            if people:reply=(people[0],"잠깐, 한 사람씩 이야기해요.")
        if reply:rows.append(reply)
        return rows

    def r13_meeting_live_should_stop(identity):
        return bool(identity.startswith("meeting:live:") and getattr(store,"r13_meeting_live_active",False) and getattr(store,"r13_meeting_live_command",None))

    def r13_meeting_can_live_press():
        if not getattr(store,"r13_meeting_live_active",False) or not r13_meeting_can_interrupt():return False
        claim=store.r13_meeting_claim;sid=r13_meeting_live_target()
        packet=getattr(store,"r13_packet",None)
        return bool(packet and packet[0]==r13_debate_statement(claim,sid)["who"] and not r13_debate_is_broken(claim,sid))

    def r13_meeting_request_live_action(kind):
        if not getattr(store,"r13_meeting_live_active",False) or getattr(store,"r13_meeting_interrupting",False):return
        if kind=="press" and not r13_meeting_can_live_press():return
        if kind in ("previous","next"):
            target=r13_meeting_live_next(store.r13_meeting_claim,store.r13_meeting_live_sid,-1 if kind=="previous" else 1)
            if not target:return
            store.r13_meeting_live_command=("seek",target)
        elif kind=="press":store.r13_meeting_live_command=(kind,r13_meeting_live_target())
        elif kind=="review":store.r13_meeting_live_command=("review",)
        else:return
        renpy.end_interaction(True)

    R13_MEETING_ISSUES={
        "C1":"13호에 들어가는 길은 하나뿐이었나?",
        "C2":"다람이가 휘두른 촛대가 사망 원인인가?",
        "C3":"첫 비명 뒤에도 할머니는 식당에 있었나?",
        "C4":"할머니는 도우러 들어갔을 뿐인가?",
        "F1":"환자들은 정말 돌아올 수 없는가?",
        "F2":"사람을 희생하는 것 말고 방법은 없나?",
        "F3":"희생 없이 오늘 밤을 버틸 수 있나?",
        "F4":"가족을 떼어 놓으려 한 이유는 무엇인가?",
    }

    def r13_meeting_begin_opinions(claim):
        baseline=dict(getattr(store,"r13_meeting_opinion_baseline",{}))
        if claim not in baseline:
            baseline[claim]=dict(r13_debate_seats(r13_debate_session(claim)))
            store.r13_meeting_opinion_baseline=baseline

    def r13_meeting_finding(claim,sid):
        # Show only the exact observation already submitted for this statement.
        # No hand-authored summary may turn an account into a stronger claim.
        if not r13_debate_is_broken(claim,sid):return None
        return getattr(store,"r13_meeting_findings",{}).get(claim+":"+sid)

    def r13_meeting_reaction_lines(vote):
        session=vote["session"]
        lines=[]
        for change in vote.get("changed",[]):
            who=change["person"];stance=change["to"]
            if session=="trial":
                text=("아직 그 아이를 의심하고 있어요.","그 아이가 그랬다고 단정할 수는 없겠어요.","이제는 그 아이가 그랬다는 말에 동의하지 않아요.")[stance]
            else:
                text=("아직은 희생을 이어 가야 한다고 생각해요.","희생을 계속하는 게 맞는지 다시 생각해 봐야겠어요.","더는 사람을 희생하는 데 동의하지 않아요.")[stance]
            lines.append((who,text))
        return lines

    R13_MEETING_RESUME_FIELDS=("r13_index","r13_packet","r13_expression","r13_directed_pose","r13_pages","r13_page_i","r13_read_id","r13_thought_active","r13_last_partner","dialogue_speaker","dialogue_expression","r13_conv_skip","r13_current_pose","r13_meeting_focus","r13_meeting_shot_revision","r13_meeting_pan_direction","r13_meeting_pan_started","r13_meeting_previous_focus","r13_meeting_previous_expression","r13_meeting_pan_painted_revision","r13_meeting_live_active","r13_meeting_live_sid","r13_meeting_live_command","r13_meeting_live_lap","r13_meeting_direction","r13_meeting_direction_poses","r13_meeting_direction_music","r13_meeting_shock_target","r13_meeting_shock_at")

    def r13_meeting_resume_after_load():
        # Ren'Py saves the outer interaction while a nested UI context is open.
        # Restore that interaction's cursor rather than a child reply's globals.
        resume=getattr(store,"r13_meeting_pending_resume",None)
        if not isinstance(resume,dict):return
        for name in R13_MEETING_RESUME_FIELDS:
            if name in resume:setattr(store,name,resume[name])
        store.r13_meeting_pending_resume=None
        store.r13_meeting_interrupting=False
        renpy.hide_screen("r13_book")
        renpy.hide_screen("r13_material_corner")
        renpy.hide("r13_visitor")
        renpy.hide_screen("r13_meeting_cut_in")
        renpy.hide_screen("r13_meeting_evidence_hold")
        renpy.hide_screen("r13_meeting_objection")

    config.after_load_callbacks.append(r13_meeting_resume_after_load)

    def r13_meeting_live_target():
        claim=getattr(store,"r13_meeting_claim",None)
        if claim not in R13_DEBATE:return None
        sid=(getattr(store,"r13_meeting_live_sid",None) if getattr(store,"r13_meeting_live_active",False) else None) or getattr(store,"r13_debate_selected",None)
        sts=r13_debate_statements(claim)
        st=next((s for s in sts if s["id"]==sid),sts[0])
        # A question's final authored line may introduce the hidden next claim.
        # This is an exact authored-line match, never a keyword guess.
        packet=getattr(store,"r13_packet",None)
        if st.get("reveals") and st.get("press") and packet and tuple(packet[:2])==tuple(st["press"][-1][:2]):
            return st["reveals"]
        return st["id"]

    def r13_meeting_can_interrupt():
        packet=getattr(store,"r13_packet",None)
        target=r13_meeting_live_target()
        if getattr(store,"r13_meeting_live_active",False) and packet and target:
            if packet[0]!=r13_debate_statement(store.r13_meeting_claim,target)["who"]:return False
        return bool(getattr(store,"r13_meeting_active",False) and not getattr(store,"r13_meeting_interrupting",False) and not getattr(store,"r13_meeting_replaying",False)
            and not getattr(store,"r13_meeting_intro",False) and packet and packet[0] not in (None,"dad") and target)

    def r13_meeting_vote_snapshot(claim,choice):
        session=r13_debate_session(claim)
        rows=[]
        for who,stance in r13_debate_seats(session):
            grounds=[cid for cid,spec in R13_DEBATE.items() if cid.startswith("C" if session=="trial" else "F") and who in spec.get("sway",[]) and (cid in store.room13.get("propositions",[]) or r13_debate_progress(cid)[0])]
            rows.append(dict(person=who,stance=stance,grounds=grounds))
        previous=store.room13.get("meeting_votes",{}).get(claim)
        baseline=({row["person"]:row["stance"] for row in previous["voters"]} if previous else getattr(store,"r13_meeting_opinion_baseline",{}).get(claim,{}))
        changed=[dict(person=row["person"],before=baseline[row["person"]],to=row["stance"]) for row in rows if row["person"] in baseline and baseline[row["person"]]!=row["stance"]]
        return dict(session=session,claim=claim,choice=choice,voters=rows,changed=changed,
            tally=[sum(row["stance"]==i for row in rows) for i in range(3)],
            propositions=list(store.room13.get("propositions",[])))

    def r13_meeting_record_vote(claim,choice):
        # Records opinions; proof, witness consent and ending authority stay with
        # r13_prove / r13_verdict / r13_resolve_ending, never a popularity threshold.
        vote=r13_meeting_vote_snapshot(claim,choice)
        votes=dict(store.room13.get("meeting_votes",{}));votes[claim]=vote
        r13_edit(meeting_votes=votes)
        return vote

label r13_meeting_live_round(claim):
    $ r13_meeting_live_active=True
    $ r13_meeting_live_command=None
    $ r13_meeting_live_lap=0
    while not r13_meeting_live_command and not r13_debate_ready(claim):
        # Recompute after questions reveal statements or a live rebuttal resolves one.
        $ r13_meeting_round_ids=r13_meeting_live_ids(claim,r13_debate_selected)
        if not r13_meeting_round_ids:
            $ r13_meeting_live_command=("review",)
        else:
            $ r13_meeting_live_sid=r13_meeting_round_ids[0]
            $ r13_debate_selected=r13_meeting_live_sid
            call r13_lines(r13_meeting_live_rows(claim,r13_meeting_live_sid),"meeting:live:"+claim+":"+r13_meeting_live_sid)
            if r13_meeting_live_command and r13_meeting_live_command[0]=="seek":
                $ r13_debate_selected=r13_meeting_live_command[1]
                $ r13_meeting_live_command=None
            elif not r13_meeting_live_command:
                $ r13_meeting_round_next=r13_meeting_live_next(claim,r13_meeting_live_sid)
                if r13_meeting_round_next:
                    if r13_debate_statements(claim).index(r13_debate_statement(claim,r13_meeting_round_next))<=r13_debate_statements(claim).index(r13_debate_statement(claim,r13_meeting_live_sid)):
                        $ r13_meeting_live_lap+=1
                    $ r13_debate_selected=r13_meeting_round_next
    $ r13_meeting_round_result=r13_meeting_live_command or ("review",)
    $ r13_meeting_live_active=False
    $ r13_meeting_live_sid=None
    $ r13_meeting_live_command=None
    $ r13_meeting_live_lap=0
    return r13_meeting_round_result

label r13_debate_present_record(claim,sid,key,allow_hidden=False,presentation_result=None,presentation_rows=None,was_interrupting=False):
    if key not in room13.get("evidence",[]) or key not in ROOM13["evidence"]:
        return False
    if not r13_debate_visible(claim,r13_debate_statement(claim,sid)) and not allow_hidden:
        return False
    $ was_interrupting=r13_meeting_interrupting
    $ r13_meeting_interrupting=True
    $ r13_meeting_focus_change(claim,r13_debate_statement(claim,sid)["who"])
    $ presentation_result,presentation_rows=r13_debate_judge(claim,sid,key)
    # An accepted record earns an interruption, not a premature victory.
    # The opponent can recover in the canonical counter question below.
    if presentation_result=="break":
        call r13_meeting_direct_interrupt(claim,sid,key)
        call r13_meeting_direct_gasp_lines(claim,sid)
    else:
        $ r13_meeting_direct_beat("half" if presentation_result=="half" else "reversal",claim,sid,key)
        $ source_fx("present" if presentation_result in ("half","soft") else "wrong")
    show screen r13_material_corner(key)
    call r13_lines(presentation_rows,"debate:"+presentation_result+":"+claim+":"+sid+":"+key)
    hide screen r13_material_corner
    hide screen r13_meeting_evidence_hold
    if presentation_result=="break" and r13_debate_counter(claim,sid):
        call r13_debate_answer_counter(claim,sid)
        if not _return:
            $ presentation_result="countered"
            $ r13_debate_miss(claim)
    if presentation_result=="break":
        if allow_hidden:
            python:
                for source in r13_debate_statements(claim):
                    if source.get("reveals")==sid:r13_debate_mark("pressed",claim,source["id"])
        $ r13_debate_mark("broken",claim,sid)
        $ r13_meeting_direct_beat("resolve",claim,sid,key)
        $ source_fx("right")
        $ r13_submit(claim,key)
        python:
            observation=next((row[1] for row in presentation_rows if row[0] is not None),None)
            if observation:
                findings=dict(r13_meeting_findings);findings[claim+":"+sid]=observation
                r13_meeting_findings=findings
                r13_meeting_feedback=dict(claim=claim,sid=sid,text=observation)
        $ r13_debate_selected=r13_debate_next_target(claim,sid)
        if persistent.room13_motion and not renpy.is_skipping():
            show screen r13_meeting_rebuttal_hold(claim)
            pause .22
            hide screen r13_meeting_rebuttal_hold
    elif presentation_result=="half":
        $ r13_debate_half(claim,sid,key)
        $ r13_meeting_feedback=dict(claim=claim,sid=sid,text="반쯤 무너졌다. 하나가 더 필요하다.")
    elif presentation_result=="wrong":
        $ r13_debate_miss(claim)
        $ presentation_rows=r13_debate_hint_due(claim,sid)
        if presentation_rows:
            call r13_lines([("dad",presentation_rows,{"thought":True})],"debate:hint:"+claim+":"+sid)
    call r13_meeting_direct_reactions(claim,sid,presentation_result)
    $ r13_meeting_interrupting=was_interrupting
    $ r13_meeting_direct_beat("listen",claim)
    return presentation_result=="break"

label r13_meeting_interrupt(claim,sid,resume=None):
    $ resume={name:getattr(store,name,None) for name in R13_MEETING_RESUME_FIELDS}
    $ r13_meeting_pending_resume=resume
    $ r13_meeting_interrupting=True
    $ r13_meeting_direct_beat("select",claim,sid)
    call screen r13_book("resident_seori",present=True,hearing=True)
    if _return:
        call r13_debate_present_record(claim,sid,_return,allow_hidden=True)
    python:
        for name,value in resume.items():setattr(store,name,value)
        store.r13_meeting_interrupting=False
        store.r13_meeting_pending_resume=None
        r13_meeting_direct_audio()
    return

label r13_meeting_public_vote(claim,choice):
    $ r13_meeting_vote=r13_meeting_record_vote(claim,choice)
    $ r13_meeting_opinion_lines=r13_meeting_reaction_lines(r13_meeting_vote)
    if r13_meeting_opinion_lines:
        call r13_lines(r13_meeting_opinion_lines,"meeting:opinions:"+claim+":"+choice)
    call screen r13_meeting_ballot(claim,r13_meeting_vote)
    return

screen r13_meeting_ballot(claim,vote):
    style_prefix "r13"
    modal True
    zorder 40
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    use r13_meeting_stage(claim,ballot=True)
    use r13_meeting_chrome(claim)
    frame:
        area (48,488,1184,146) padding (20,14) background R13PaperFrame()
        vbox:
            spacing 10
            text "공개 의견 확인" size r13_read_size(24,28) color "#493b30"
            $ my_choice=next((text for kind,text in R13_DEBATE[claim]["conclusion"]["options"] if kind==vote["choice"]),"")
            text ("내가 밝힌 의견 · "+my_choice) size r13_read_size(19,23) color "#795d40"
            hbox:
                spacing 24
                for index,name in enumerate(R13_DEBATE_STANCE[vote["session"]]):
                    text (name+"  "+str(vote["tally"][index])+"명") size r13_read_size(19,23) color "#493b30"
    textbutton "회의를 계속한다":
        style "r13_action_button" xpos 920 ypos 646 xsize 312 ysize 64 text_size 24
        action Return(True) sensitive ready
    text "입증한 내용에 따른 주민들의 현재 입장" xpos 48 ypos 662 size r13_read_size(18,21) color "#f1dfba" outlines [(1,"#30251e",0,0)]
    key "game_menu" action Return(True)
