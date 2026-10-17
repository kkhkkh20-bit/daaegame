# Shared council direction: only presentation state, never proof, suspicion or clock.
# Every C/F/Q hearing uses these beats. Authored counter questions retain authority.
default r13_meeting_direction = {}
default r13_meeting_direction_seen = []
default r13_meeting_direction_poses = {}
default r13_meeting_direction_music = None
default r13_meeting_direction_return_audio = {}
default r13_meeting_shock_target = None
default r13_meeting_shock_at = 0.0

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
    # Performance styles, not guilt. A composed opponent can gather themselves
    # between statements; others retain pressure from already-proved contradictions.
    R13_MEETING_COMPOSED = {"resident_ppul","resident_seori","neoul"}

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

    def r13_meeting_direct_line(identity,index,packet,expression,pose):
        if not getattr(store,"r13_meeting_active",False):return expression,pose
        claim=getattr(store,"r13_meeting_claim",None)
        if claim not in R13_DEBATE:return expression,pose
        person=packet[0]
        beat=r13_meeting_direct_phase(identity,index,person)
        r13_meeting_direct_beat(beat,claim)
        # Keep explicit writer/art direction. Neutral fallbacks can use the beat.
        explicit=(len(packet)>2 and bool(packet[2])) or pose not in ("neutral","interview_neutral")
        if person in CAST and person!=r13_viewpoint():
            if not explicit:
                group=R13_DEBATE[claim].get("session","trial" if claim.startswith("C") else "finale")
                count=sum(1 for cid,spec in R13_DEBATE.items()
                    if spec.get("session","trial" if cid.startswith("C") else "finale")==group
                    for st in spec["statements"] if st["who"]==person and not st.get("truth")
                    and not r13_debate_skipped(cid,st) and r13_debate_is_broken(cid,st["id"]))
                if beat=="listen" and count and person not in R13_MEETING_COMPOSED:
                    pose="flustered" if count==1 else "anxious"
                elif beat=="shaken":
                    # Escalate only already-established contradictions by this speaker.
                    pose="surprise" if count==0 else "flustered" if count==1 else "anxious"
                elif beat=="cornered":pose="angry"
                elif beat=="recover":pose="neutral"
                elif beat=="reversal":pose="angry"
                elif beat=="loss":pose="neutral"
            if beat=="shaken" and person==getattr(store,"r13_meeting_shock_target",None) and index<=1:
                pose="surprise"
            poses=dict(getattr(store,"r13_meeting_direction_poses",{}) or {})
            poses[person]=pose;store.r13_meeting_direction_poses=poses
        return expression,pose

    def r13_meeting_direct_shock(claim,sid):
        target=r13_debate_statement(claim,sid)["who"]
        store.r13_meeting_shock_target=target
        poses=dict(getattr(store,"r13_meeting_direction_poses",{}) or {})
        people=[p for p,_ in r13_meeting_cast(claim,r13_debate_session(claim))]
        for who in people:
            if who in CAST and who!=r13_viewpoint():poses[who]="surprise"
        store.r13_meeting_direction_poses=poses
        store.r13_meeting_shock_at=renpy.display.core.get_time()

    def r13_meeting_direct_gasps(claim,sid):
        token=claim+":"+sid+":gasp"
        seen=list(getattr(store,"r13_meeting_direction_seen",[]) or [])
        if token in seen:return []
        seen.append(token);store.r13_meeting_direction_seen=seen
        target=r13_debate_statement(claim,sid)["who"]
        people=list(r13_meeting_neighbors(claim,target))
        people=list(dict.fromkeys(p for p in people if p in CAST and p not in (target,r13_viewpoint())))
        return [(who,text,{"pose":"surprise"}) for who,text in zip(people,("정말요?","그렇다고요?"))]

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
    $ r13_meeting_direct_shock(claim,sid)
    $ r13_meeting_direct_beat("interrupt",claim,sid,key)
    if not renpy.is_skipping() and not r13_fast_all:
        show screen r13_meeting_objection(claim,sid)
        $ renpy.music.set_pause(True,channel="music")
        $ source_fx("impact")
        $ renpy.pause(.68 if persistent.room13_motion else .42)
        hide screen r13_meeting_objection
    $ r13_meeting_shock_at=renpy.display.core.get_time()
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
        call r13_lines(r13_meeting_gasp_rows,"meeting:gasp:"+claim+":"+sid)
    return
