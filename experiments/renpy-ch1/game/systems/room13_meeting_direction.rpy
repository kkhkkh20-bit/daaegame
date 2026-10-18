# Shared council direction: only presentation state, never proof, suspicion or clock.
# Every C/F/Q hearing uses these beats. Authored counter questions retain authority.
default r13_meeting_direction = {}
default r13_meeting_direction_seen = []
default r13_meeting_direction_poses = {}
default r13_meeting_direction_music = None
default r13_meeting_direction_return_audio = {}
default r13_meeting_shock_target = None
default r13_meeting_shock_at = 0.0
default r13_meeting_proof_reveal = None
# Presentation-only state. Older saves receive these defaults; no story flags.
default r13_meeting_line_token = None
default r13_meeting_listener = None
default r13_meeting_art_slots = {}
default r13_meeting_reaction = None
default r13_meeting_reaction_tokens = []

init 174 python:
    R13_MEETING_BEATS = {
        "listen": ("토론 중", 1.0, .22, .00),
        "gasp": ("주민의 놀람", .42, .00, .30),
        "reaction": ("주민의 반응", .88, .12, .12),
        "press": ("되묻기", .90, .12, .10),
        "select": ("자료 확인", .50, .00, .22),
        "interrupt": ("잠깐만요!", .20, .00, .38),
        "explain": ("근거 제시", .58, .00, .28),
        "shaken": ("상대의 답변", .64, .16, .32),
        "recover": ("상대의 반문", 1.0, .12, .18),
        "reversal": ("남은 반론", 1.0, .12, .22),
        "half": ("남은 근거", .86, .18, .12),
        "resolve": ("반박 성립", .88, .18, .18),
        "settle": ("의견 정리", .78, .26, .00),
        "cornered": ("마지막 항변", .82, .16, .36),
        "loss": ("남겨진 주장", .68, .26, .18),
    }
    def r13_meeting_startle_pose(person):
        # Every approved dialogue source now has a real surprise talk frame.
        return "surprise"

    def r13_meeting_direct_beat(beat,claim=None,sid=None,key=None):
        if beat not in R13_MEETING_BEATS:return
        old=getattr(store,"r13_meeting_direction",{}) or {}
        claim=claim or getattr(store,"r13_meeting_claim",None)
        if claim not in R13_DEBATE:return
        if old.get("claim")!=claim:
            store.r13_meeting_direction_poses={}
            store.r13_meeting_direction_music=None
        store.r13_meeting_direction=dict(claim=claim,beat=beat,
            sid=sid if sid is not None else old.get("sid"),
            key=key if key is not None else old.get("key"))
        r13_meeting_direct_audio()

    def r13_meeting_channel_gain(channel):
        # SDK 8.5.3 set_volume writes this rollback-aware channel context.
        # There is no renpy.music.get_volume API.
        return renpy.audio.audio.get_channel(channel).context.secondary_volume

    def r13_meeting_direct_audio():
        state=getattr(store,"r13_meeting_direction",{}) or {}
        if not getattr(store,"r13_meeting_active",False):return
        if not getattr(store,"r13_meeting_direction_return_audio",{}):
            store.r13_meeting_direction_return_audio={channel:dict(path=renpy.music.get_playing(channel=channel),
                volume=r13_meeting_channel_gain(channel),paused=renpy.music.get_pause(channel=channel))
                for channel in ("music","ambience")}
        beat=state.get("beat","listen");claim=state.get("claim")
        if claim not in R13_DEBATE:return
        venue=r13_meeting_kind(r13_debate_session(claim))
        base="altar" if venue=="stone" else "council"
        wanted="pressure" if beat in ("recover","reversal","cornered") else base
        # Quiet beats retain the current track/position; no restart per sentence.
        if beat in ("listen","press","select","interrupt","explain","shaken","half","resolve","reaction","gasp"):
            wanted=getattr(store,"r13_meeting_direction_music",None) or base
        path=R13_BGM[wanted]
        renpy.music.set_pause(False,channel="music")
        if renpy.music.get_playing(channel="music")!=path:
            renpy.music.play(path,channel="music",loop=True,fadeout=.28,fadein=.35)
        store.r13_meeting_direction_music=wanted
        renpy.music.set_volume(R13_MEETING_BEATS[beat][1],delay=.16,channel="music")
        r13_sound_ambience("wind" if venue in ("stone","field") else "fire")

    def r13_meeting_direct_end():
        store.r13_meeting_proof_reveal=None
        store.r13_meeting_line_token=None
        store.r13_meeting_art_slots={}
        store.r13_meeting_listener=None
        store.r13_meeting_reaction=None
        store.r13_meeting_direction={}
        store.r13_meeting_direction_poses={}
        store.r13_meeting_direction_music=None
        store.r13_meeting_shock_target=None
        saved=getattr(store,"r13_meeting_direction_return_audio",{}) or {}
        for channel,state in saved.items():
            path=state.get("path")
            if renpy.music.get_playing(channel=channel)!=path:
                if path:renpy.music.play(path,channel=channel,loop=True,fadeout=.2,fadein=.2)
                else:renpy.music.stop(channel=channel,fadeout=.2)
            renpy.music.set_volume(state.get("volume",1.0),delay=.2,channel=channel)
            renpy.music.set_pause(state.get("paused",False),channel=channel)
        store.r13_meeting_direction_return_audio={}
        renpy.hide_screen("r13_meeting_objection")
        renpy.hide_screen("r13_meeting_evidence_hold")

    def r13_meeting_direct_phase(identity,index,person):
        proof=getattr(store,"r13_meeting_proof_reveal",None)
        if proof and identity==proof["identity"] and index<proof["boundary"]:
            return "explain"
        # Exact structural identities, never keywords in dialogue or hidden culprit data.
        if identity.startswith("meeting:live:"):return "listen" if index==0 else "reaction"
        if identity.startswith("meeting:replay:"):return "listen"
        if identity.startswith("meeting:opinions:"):return "settle"
        if identity.startswith("meeting:murmur:"):return "reaction"
        if identity.startswith("meeting:gasp:"):return "gasp"
        if identity.startswith("debate:counter_wrong:"):return "reversal"
        if identity.startswith("debate:counter_ok:"):return "resolve"
        if identity.startswith("debate:counter:"):return "recover"
        if identity.startswith(("debate:unanswerable:","debate:gave_up:","debate:partial:","debate:c4:unenforced","debate:c4:fake_testimony")):return "loss"
        if identity.startswith(("debate:conclusion_wrong:","debate:point_wrong:","debate:point_key_wrong:")):return "reversal"
        if identity.startswith("debate:conclusion:"):
            claim=getattr(store,"r13_meeting_claim",None)
            point=R13_DEBATE.get(claim,{}).get("conclusion",{}).get("point",{})
            return "cornered" if person==point.get("who") else "settle"
        if identity.startswith("debate:break:"):
            return "explain" if person in (None,r13_viewpoint()) else "shaken"
        if identity.startswith("debate:half:"):return "half"
        if identity.startswith("debate:soft:"):return "press"
        if identity.startswith("debate:wrong:"):return "reversal"
        if identity.startswith(("debate:press:","debate:press_missing:")):return "press"
        return "listen"

    # Exact public lines, not emotion keywords, allegiance or hidden case state.
    # Art slots are separate from authored emotions and never infer allegiance.
    # Their source files/placement live in room13-meeting-source-art.json.
    R13_MEETING_LINE_CUES = {
        ("meeting:live:C1:s1",0,"seryeon","복도에 있던 사람들은 아무도 문으로 들어가지 않았다고 했습니다."):
            dict(slot="confident_report",pose="neutral"),
        ("meeting:live:C3:s1",0,"granny","비명이 들릴 때 나는 식당에 있었어요. 다들 봤잖아요."):
            dict(slot="composed_answer",pose="neutral"),
        ("debate:soft:C2:s2:E07",0,"resident_seori","촛대가 둘로 갈라진 건 보입니다. 하지만 조각만 봐서는 언제 갈라졌는지, 머리 상처를 그 조각이 냈는지 알 수 없습니다. 상처와 맞춰 본 기록이 있습니까?"):
            dict(slot="evidence_check",pose="neutral"),
        ("meeting:live:F1:s1",0,"resident_ppul","가족도 못 알아봅니다. 돌아올 수 없는 분들로 판단됐어요."):
            dict(slot="stern_statement",pose="neutral"),
        ("meeting:live:Q4:s1",0,"resident_ppul","목수는 혼자 통로에 들어갔다가 문이 저절로 닫혀 갇혔소. 딱한 사고요."):
            dict(slot="stern_statement",pose="neutral"),
        ("meeting:live:Q6:s1",0,"resident_ppul","이 수레는 보호소로 가는 수레요."):
            dict(slot="stern_statement",pose="neutral"),
        ("meeting:live:C2:s1",0,"resident_ppul","아이의 말과 상처 기록 모두 아이가 머리를 쳤다는 증거요."):
            dict(slot="stern_statement",pose="neutral",listener=("buri","neutral")),
        ("meeting:live:C2:s1",1,"buri","잠깐요. 무슨 일이었는지부터 차례로 들어요."):
            dict(slot="measured_interject",pose="neutral",listener=("resident_ppul","neutral")),
        ("meeting:live:C2:s2",1,"nabi","직접 본 일과 들은 말을 섞지는 말아요."):
            dict(pose="neutral",listener=("resident_ppul","neutral")),
        ("meeting:live:C2:s3",0,"resident_ppul","그 방에는 아이 혼자 있었소. 다시 휘두를 사람이 누가 있소?"):
            dict(slot="stern_statement",pose="neutral"),
        ("meeting:live:C2:s3",1,"resident_seori","그때 방에 있던 사람이 누구인지 확인하겠습니다."):
            dict(pose="neutral",listener=("resident_ppul","neutral")),
        ("meeting:live:C3:s1",1,"nabi","첫 비명 때는 할머니와 함께 있었어요."):
            dict(pose="neutral",listener=("granny","neutral")),
        ("debate:press:C3:s1",1,"nabi","네. 첫 비명이 났을 때는 할머니랑 같이 있었어요."):
            dict(pose="neutral",listener=("granny","neutral")),
        ("debate:break:C3:s2:E12",0,"nabi","할머니가 공구를 가지러 주방에 가신 뒤로는…… 저도 못 봤어요."):
            dict(slot="witness_hesitate",expression="anxious",pose="anxious",listener=("granny","neutral")),
    }

    def r13_meeting_reaction_settle():
        reaction=getattr(store,"r13_meeting_reaction",None)
        if reaction:
            store.r13_meeting_reaction=dict(reaction,phase="settled")
        store.r13_meeting_shock_target=None

    def r13_meeting_direct_line(identity,index,packet,expression,pose):
        if not getattr(store,"r13_meeting_active",False):return expression,pose
        claim=getattr(store,"r13_meeting_claim",None)
        if claim not in R13_DEBATE:return expression,pose
        person=packet[0]
        token=(identity,index,person,packet[1])
        proof=getattr(store,"r13_meeting_proof_reveal",None)
        reaction=getattr(store,"r13_meeting_reaction",None)
        carry=bool(proof and proof.get("at_end") and proof.get("revealed") and reaction
            and reaction.get("phase")=="pending" and index==0
            and identity=="meeting:gasp:"+proof["claim"]+":"+proof["sid"])
        if token!=getattr(store,"r13_meeting_line_token",None):
            if not carry:
                r13_meeting_reaction_settle()
                store.r13_meeting_reaction=None
            store.r13_meeting_direction_poses={}
            store.r13_meeting_listener=None
            store.r13_meeting_line_token=token
        proof=getattr(store,"r13_meeting_proof_reveal",None)
        if proof and identity==proof["identity"] and index==proof["boundary"] and not proof["revealed"]:
            r13_meeting_direct_reveal(proof["claim"],proof["sid"])
        beat=r13_meeting_direct_phase(identity,index,person)
        r13_meeting_direct_beat(beat,claim)
        metadata=packet[2] if len(packet)>2 and isinstance(packet[2],dict) else {}
        explicit=bool(metadata.get("pose") or metadata.get("expression")) or pose not in ("neutral","interview_neutral") or expression not in (None,"neutral")
        cue=R13_MEETING_LINE_CUES.get(token,{})
        if not explicit:pose=cue.get("pose",pose)
        # An authored pose always wins. A matching authored emotion may use a
        # reviewed variant of that same emotion (Nabi's anxious witness account).
        use_slot=cue.get("slot") and not metadata.get("pose") and (not explicit or cue.get("expression")==metadata.get("expression",expression))
        store.r13_meeting_art_slots={person:cue["slot"]} if use_slot else {}
        poses={}
        listener=cue.get("listener")
        attendees={p for p,_ in r13_meeting_cast(claim,r13_debate_session(claim))}
        if listener and listener[0] in attendees and listener[0] not in (person,r13_viewpoint()):
            store.r13_meeting_listener=listener[0]
            poses[listener[0]]=listener[1]
        else:store.r13_meeting_listener=None
        if person in CAST and person!=r13_viewpoint():
            if pose=="surprise":pose=r13_meeting_startle_pose(person)
            poses[person]=pose
        reaction=getattr(store,"r13_meeting_reaction",None)
        if reaction and reaction["token"]==(getattr(store,"r13_meeting_proof_reveal",None) or {}).get("identity"):
            target=reaction["person"]
            if target==person:
                if not explicit and not cue:
                    pose=r13_meeting_startle_pose(person)
                    poses[person]=pose
                # The authored final face wins, including angry and special poses.
                store.r13_meeting_reaction=dict(reaction,pose=pose)
                if explicit and pose not in ("neutral","surprise","flustered","anxious"):
                    r13_meeting_reaction_settle()
            elif target in attendees:
                # A proof reaction replaces (never adds to) the one listener cue.
                poses={p:v for p,v in poses.items() if p==person}
                poses[target]=reaction["pose"]
                store.r13_meeting_listener=target
        store.r13_meeting_direction_poses=poses
        return expression,pose

    def r13_meeting_proof_boundary(claim,sid,rows):
        # Witnesses may explain the observation before the challenged speaker replies.
        # A self-contained reply with no preceding explanation reacts only at its end.
        target=r13_debate_statement(claim,sid)["who"]
        first=next((i for i,row in enumerate(rows) if row[0]==target),len(rows))
        return first if first>0 else len(rows)

    def r13_meeting_prepare_proof(claim,sid,key,rows):
        store.r13_meeting_shock_target=None
        boundary=r13_meeting_proof_boundary(claim,sid,rows)
        store.r13_meeting_proof_reveal=dict(claim=claim,sid=sid,
            identity="debate:break:"+claim+":"+sid+":"+key,
            boundary=boundary,at_end=boundary==len(rows),revealed=False)

    def r13_meeting_direct_reveal(claim,sid):
        proof=getattr(store,"r13_meeting_proof_reveal",None)
        if proof and proof["revealed"]:return
        if proof:store.r13_meeting_proof_reveal=dict(proof,revealed=True)
        r13_meeting_direct_beat("shaken",claim,sid)
        r13_meeting_direct_shock(claim,sid)

    def r13_meeting_direct_shock(claim,sid):
        proof=getattr(store,"r13_meeting_proof_reveal",None)
        # A call without a completed explanation is not an animation trigger.
        if not proof or not proof.get("revealed") or proof["claim"]!=claim or proof["sid"]!=sid:return
        token=proof["identity"]
        tokens=list(getattr(store,"r13_meeting_reaction_tokens",[]) or [])
        if token in tokens:return
        tokens.append(token);store.r13_meeting_reaction_tokens=tokens
        target=r13_debate_statement(claim,sid)["who"]
        store.r13_meeting_reaction=dict(token=token,person=target,phase="pending",pose="surprise")
        store.r13_meeting_shock_target=target
        # Only the person whose statement was challenged reacts. No group flinch.
        store.r13_meeting_direction_poses={target:r13_meeting_startle_pose(target)}

    def r13_meeting_direct_gasps(claim,sid):
        # Q1 already ends each proof with an authored reply or a child's reaction.
        # Generic surprise after those lines interrupts their meaning and pacing.
        if claim=="Q1":return []
        token=claim+":"+sid+":gasp"
        seen=list(getattr(store,"r13_meeting_direction_seen",[]) or [])
        if token in seen:return []
        seen.append(token);store.r13_meeting_direction_seen=seen
        target=r13_debate_statement(claim,sid)["who"]
        people=list(r13_meeting_neighbors(claim,target))
        people=list(dict.fromkeys(p for p in people if p in CAST and p not in (target,r13_viewpoint())))
        return [(who,text,{"pose":r13_meeting_startle_pose(who)}) for who,text in zip(people,("정말요?","그렇다고요?"))]

    def r13_meeting_direct_pose(person,fallback="neutral"):
        return (getattr(store,"r13_meeting_direction_poses",{}) or {}).get(person,fallback)

    def r13_meeting_direct_duration():
        beat=(getattr(store,"r13_meeting_direction",{}) or {}).get("beat","listen")
        return R13_MEETING_BEATS.get(beat,R13_MEETING_BEATS["listen"])[2]

    def r13_meeting_direct_shade():
        beat=(getattr(store,"r13_meeting_direction",{}) or {}).get("beat","listen")
        return R13_MEETING_BEATS.get(beat,R13_MEETING_BEATS["listen"])[3]

    def r13_meeting_direct_close_height(kind,outgoing=False):
        beat=(getattr(store,"r13_meeting_direction",{}) or {}).get("beat","listen")
        base=840 if kind in ("round","stone") else 740
        return base+(36 if beat in ("shaken","recover","reversal","cornered") and not outgoing else 0)

    def r13_meeting_direct_murmurs(claim,sid,result):
        if claim=="Q1":return []
        # One short response per first outcome, from someone actually at this meeting.
        token=claim+":"+sid+":"+result
        seen=list(getattr(store,"r13_meeting_direction_seen",[]) or [])
        if token in seen or result not in ("break","half","countered"):return []
        target=r13_debate_statement(claim,sid)["who"]
        people=[p for p,_stance in r13_meeting_cast(claim,r13_debate_session(claim))
            if p not in (target,r13_viewpoint()) and p in CAST]
        if not people:return []
        seen.append(token);store.r13_meeting_direction_seen=seen
        texts={"break":("……앞의 말과 맞춰 봅시다.","잠깐, 끝까지 들어봐요."),
            "half":("아직 확인할 게 남았군요.","그것만으로는 정리하기 어렵겠어요."),
            "countered":("그 질문에는 아직 답하지 못했어요.","그렇다고 의심이 풀린 건 아니잖아요.")}
        offset=sum(ord(c) for c in token)
        return [(people[offset%len(people)],texts[result][offset%2])]

    def r13_meeting_direct_after_load():
        r13_meeting_reaction_settle()
        if getattr(store,"r13_meeting_active",False):
            r13_meeting_direct_audio()
        else:
            r13_meeting_direct_end()

    config.after_load_callbacks.append(r13_meeting_direct_after_load)

# Brief impact, followed by a patient, user-paced evidence explanation.
transform r13_meeting_objection_appear(motion=True):
    alpha (0.0 if motion else 1.0)
    xoffset (-24 if motion else 0)
    linear (.07 if motion else 0) alpha 1.0 xoffset 0

screen r13_meeting_objection(claim,sid):
    zorder 150
    # A nested record context has no say screen between the picker and explanation.
    # Paint the frozen council here too, not the unrelated exploration backdrop.
    use r13_meeting_stage(claim,r13_meeting_focus_person(claim),True)
    use r13_meeting_chrome(claim)
    add Solid("#11182066")
    # Owner-approved fixed typography image: no live text or button panel.
    add Transform("assets/room13-ui-objection01917.webp",xysize=(1120,420),fit="contain",nearest=True) xpos 80 ypos 132
    frame:
        area (160,548,960,96) padding (20,14) background R13PaperFrame()
        text r13_meeting_statement_text(claim,sid) size r13_read_size(23,26) color "#493b30" xmaximum 920

screen r13_meeting_evidence_hold(claim,sid,key):
    zorder 35
    # Keep the disputed sentence visible while the player explains the record.
    frame:
        area (80,400,910,88) padding (16,10) background R13PaperFrame()
        vbox:
            spacing 2
            text "붙잡은 발언" size 14 color "#795d40"
            text r13_meeting_statement_text(claim,sid) size r13_read_size(19,22) color "#493b30" xmaximum 878

label r13_meeting_direct_interrupt(claim,sid,key):
    $ r13_meeting_direct_beat("interrupt",claim,sid,key)
    if not renpy.is_skipping() and not r13_fast_all:
        show screen r13_meeting_objection(claim,sid)
        $ renpy.music.set_pause(True,channel="music")
        $ source_fx("impact")
        $ renpy.pause(.68 if persistent.room13_motion else .42)
        hide screen r13_meeting_objection
    $ r13_meeting_direct_beat("explain",claim,sid,key)
    show screen r13_meeting_evidence_hold(claim,sid,key)
    return

label r13_meeting_direct_reactions(claim,sid,result):
    $ r13_meeting_murmurs=r13_meeting_direct_murmurs(claim,sid,result)
    if r13_meeting_murmurs:
        call r13_lines(r13_meeting_murmurs,"meeting:murmur:"+claim+":"+sid+":"+result)
    return

label r13_meeting_direct_gasp_lines(claim,sid):
    $ r13_meeting_gasp_rows=r13_meeting_direct_gasps(claim,sid)
    if r13_meeting_gasp_rows:
        $ r13_meeting_focus_change(claim,r13_debate_statement(claim,sid)["who"])
        call r13_lines(r13_meeting_gasp_rows,"meeting:gasp:"+claim+":"+sid)
    return
