# Reviewed pilot: C2 only. Presentation state never changes proof or story outcomes.
default r13_meeting_pressure = {}
default r13_meeting_pressure_events = []
default r13_meeting_collective = None
default r13_meeting_silence_ambience = None
default r13_meeting_quiet_released = []

init 191 python:
    def r13_meeting_pressure_enabled(claim=None):
        return (claim or getattr(store,"r13_meeting_claim",None))=="C2"

    def r13_meeting_pressure_key(claim,person):
        return ((store.room13 or {}).get("run_token","legacy"),claim,person)

    def r13_meeting_pressure_level(person,claim=None):
        claim=claim or getattr(store,"r13_meeting_claim",None)
        return (getattr(store,"r13_meeting_pressure",{}) or {}).get(r13_meeting_pressure_key(claim,person),0) if r13_meeting_pressure_enabled(claim) else 0

    def r13_meeting_pressure_change(claim,sid,event,amount):
        if not r13_meeting_pressure_enabled(claim):return False
        person=r13_debate_statement(claim,sid)["who"]
        token=r13_meeting_pressure_key(claim,person)+(sid,event)
        events=list(getattr(store,"r13_meeting_pressure_events",[]) or [])
        if token in events:return False
        events.append(token);store.r13_meeting_pressure_events=events
        levels=dict(getattr(store,"r13_meeting_pressure",{}) or {})
        key=r13_meeting_pressure_key(claim,person)
        levels[key]=max(0,min(2,levels.get(key,0)+amount))
        store.r13_meeting_pressure=levels
        return True

    def r13_meeting_pressure_pose(person,fallback="neutral"):
        level=r13_meeting_pressure_level(person)
        # Only distinct approved frames: anxious and flustered are the SAME asset.
        return ("neutral","anxious","surprise")[level] if level else fallback

    def r13_meeting_pressure_attendees(claim):
        people=[p for p,_ in r13_meeting_cast(claim,r13_debate_session(claim))]
        return [p for p in people if p!=r13_viewpoint()
            and not (R13_DEATH_FLAGS.get(p) and r13_has(R13_DEATH_FLAGS[p]))
            and not (p=="resident_owlgp" and (store.room13 or {}).get("victim_state")=="dead")
            and not (p=="mom" and r13_mom_absent())]

    def r13_meeting_pressure_proof(claim,sid):
        proof=getattr(store,"r13_meeting_proof_reveal",None)
        if not proof or not proof.get("revealed") or proof.get("claim")!=claim or proof.get("sid")!=sid:return
        if not r13_meeting_pressure_change(claim,sid,"proven_contradiction",1):return
        store.r13_meeting_collective=dict(claim=claim,sid=sid,token=proof["identity"],phase="pending",
            people=r13_meeting_pressure_attendees(claim))
        # The collective reaction replaces the old single-person 0.35-second flash.
        store.r13_meeting_reaction=None
        store.r13_meeting_shock_target=None

    def r13_meeting_pressure_recover(claim,sid):
        # Called only by the actual failed-answer branch of the authored counter.
        r13_meeting_pressure_change(claim,sid,"successful_counter",-1)

    def r13_meeting_collective_pending():
        return bool((getattr(store,"r13_meeting_collective",None) or {}).get("phase")=="pending")

    def r13_meeting_collective_settle():
        reaction=getattr(store,"r13_meeting_collective",None)
        if reaction:store.r13_meeting_collective=dict(reaction,phase="settled")

    def r13_meeting_collective_art(person,height):
        profile=r13_dialogue_source_profile(person,"surprise",height)
        frame=(profile or {}).get("frames",{}).get("surprise_react")
        if frame and renpy.loadable(frame["file"]):
            return Fixed(Transform(frame["file"],xpos=frame["offset"][0],ypos=frame["offset"][1],
                zoom=frame.get("scale",1.0),nearest=False,subpixel=True),xysize=tuple(profile["canvas"]))
        return r13_fullbody_close_art(person,r13_meeting_pressure_pose(person),height)

    _r13_pressure_direct_line=r13_meeting_direct_line
    def r13_meeting_direct_line(identity,index,packet,expression,pose):
        expression,pose=_r13_pressure_direct_line(identity,index,packet,expression,pose)
        if not getattr(store,"r13_meeting_active",False) or not r13_meeting_pressure_enabled():return expression,pose
        people=r13_meeting_pressure_attendees(store.r13_meeting_claim)
        poses=dict(getattr(store,"r13_meeting_direction_poses",{}) or {})
        for who in people:
            if r13_meeting_pressure_level(who):poses[who]=r13_meeting_pressure_pose(who)
        person=packet[0]
        if person in people and r13_meeting_pressure_level(person):
            # Preserve authored non-neutral gestures, never let a neutral slot erase pressure.
            metadata=packet[2] if len(packet)>2 and isinstance(packet[2],dict) else {}
            authored=metadata.get("pose") or metadata.get("expression")
            pose=authored if authored and authored!="neutral" else r13_meeting_pressure_pose(person)
            expression=pose;poses[person]=pose
        store.r13_meeting_direction_poses=poses
        store.r13_meeting_art_slots={p:s for p,s in (getattr(store,"r13_meeting_art_slots",{}) or {}).items() if not r13_meeting_pressure_level(p)}
        return expression,pose

    _r13_pressure_direct_audio=r13_meeting_direct_audio
    def r13_meeting_direct_audio():
        _r13_pressure_direct_audio()
        if not getattr(store,"r13_meeting_active",False) or not r13_meeting_pressure_enabled():return
        proof=getattr(store,"r13_meeting_proof_reveal",None)
        collective=getattr(store,"r13_meeting_collective",None) or {}
        quiet=bool(proof and not proof.get("revealed") and proof["identity"] not in store.r13_meeting_quiet_released)
        if quiet and renpy.get_screen("r13_meeting_quiet_clock") is None:renpy.show_screen("r13_meeting_quiet_clock",token=proof["identity"])
        if not quiet:renpy.hide_screen("r13_meeting_quiet_clock")
        silent=quiet or collective.get("phase") in ("pending","playing")
        if silent:
            if store.r13_meeting_silence_ambience is None:store.r13_meeting_silence_ambience=r13_meeting_channel_gain("ambience")
            # Keep track position and mixer preferences; silence only the authored explanation.
            renpy.music.set_volume(0.0,delay=.10,channel="music")
            renpy.music.set_volume(0.0,delay=.10,channel="ambience")
        elif store.r13_meeting_silence_ambience is not None:
            renpy.music.set_volume(store.r13_meeting_silence_ambience,delay=.20,channel="ambience")
            store.r13_meeting_silence_ambience=None

    def r13_meeting_quiet_release(token):
        if token not in store.r13_meeting_quiet_released:store.r13_meeting_quiet_released=list(store.r13_meeting_quiet_released)+[token]
        renpy.hide_screen("r13_meeting_quiet_clock")
        r13_meeting_direct_audio()

    _r13_pressure_direct_end=r13_meeting_direct_end
    def r13_meeting_direct_end():
        _r13_pressure_direct_end()
        store.r13_meeting_silence_ambience=None
        renpy.hide_screen("r13_meeting_quiet_clock")
        r13_meeting_collective_settle()

    def r13_meeting_pressure_after_load():
        r13_meeting_collective_settle()
        proof=getattr(store,"r13_meeting_proof_reveal",None)
        if proof and proof["identity"] not in store.r13_meeting_quiet_released:store.r13_meeting_quiet_released=list(store.r13_meeting_quiet_released)+[proof["identity"]]
        # Saved levels/events survive; transient shock never restarts on load.
        if getattr(store,"r13_meeting_active",False):r13_meeting_direct_audio()
    config.after_load_callbacks.append(r13_meeting_pressure_after_load)

screen r13_meeting_quiet_clock(token):
    timer 2.4 action Function(r13_meeting_quiet_release,token)

screen r13_meeting_collective_view(claim):
    zorder 170
    modal True
    timer (.01 if (r13_meeting_collective or {}).get("phase")=="settled" else .52) action Return()
    if (r13_meeting_collective or {}).get("phase")=="settled":
        use r13_meeting_stage(claim,r13_meeting_focus,True)
    else:
        add r13_meeting_plate(r13_debate_session(claim),False)
        $ participants=(r13_meeting_collective or {}).get("people",[])
        for index,who in enumerate(participants):
            $ cx,edge=r13_meeting_seat_position(index,len(participants),r13_debate_session(claim))
            add Transform(r13_meeting_collective_art(who,840),ysize=300,fit="contain",nearest=False) xcenter cx ypos (edge+95-300)
        add AlphaMask(r13_meeting_plate(r13_debate_session(claim),False),R13MeetingForeground(r13_debate_session(claim),False))

label r13_meeting_collective_beat:
    if r13_meeting_collective_pending():
        $ r13_meeting_direct_audio()
        if persistent.room13_motion and not renpy.is_skipping() and not r13_fast_all and not renpy.in_rollback():
            # Impact breath → all present faces together → return to persistent pressure.
            pause .08
            $ r13_meeting_collective=dict(r13_meeting_collective,phase="playing")
            call screen r13_meeting_collective_view(r13_meeting_collective["claim"])
        $ r13_meeting_collective_settle()
        $ r13_meeting_direct_audio()
    return
