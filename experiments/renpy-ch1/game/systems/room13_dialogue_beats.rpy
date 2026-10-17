# Resource-gated dialogue direction. No held art is registered here.
default r13_dialogue_beat = None

init 170 python:
    R13_DIALOGUE_BEATS = json.load(renpy.file("assets/room13-dialogue-beats.json"))
    R13_DIALOGUE_TALK_ART = json.load(renpy.file("assets/room13-dialogue-talk-art.json"))

    def r13_dialogue_plan(identity, index, packet, pose, cues, people, binding=None):
        """Exact text/speaker/scene binding; never infer emotion from keywords."""
        if pose not in R13_FULLBODY_PLAIN or len(packet) < 2:
            return None
        cue = (binding.get("rows", {}).get(str(index)) if binding.get("identity")==identity else None) if binding is not None else cues.get(identity, {}).get(str(index))
        if not cue or not cue.get("reviewed") or (cue.get("person"), cue.get("text")) != tuple(packet[:2]):
            return None
        person = packet[0]
        entry = people.get(person, {})
        if entry.get("status") != "approved_runtime" or entry.get("stance") != "standing" or entry.get("gaze") != "player" or entry.get("art_style") != "storybook_source" or entry.get("source_kind") != "source_master":
            return None
        emotion = cue["emotion"]
        if emotion not in ("neutral","joy","angry","anxious","surprise"):
            return None
        talk = "surprise_talk" if emotion == "surprise" else emotion
        profiles = entry.get("profiles", {})
        if not all(talk in profiles.get(str(h), {}).get("frames", {}) for h in (560,760,840)):
            return None
        react = "surprise_react" if emotion == "surprise" and cue.get("reaction") else None
        if react and not all(react in profiles[str(h)]["frames"] for h in (560,760,840)):
            react = None
        return dict(person=person, talk=talk, react=react, settled=not bool(react), duration=.35)

    def r13_dialogue_beat_begin(identity, index, packet, pose):
        # New lines (including narration and POV replies) invalidate the old reaction.
        store.r13_dialogue_beat = None
        if getattr(store,"r13_meeting_active",False) or getattr(store,"r13_thought_active",False):
            return
        plan = r13_dialogue_plan(identity,index,packet,pose,R13_DIALOGUE_BEATS["lines"],R13_DIALOGUE_TALK_ART["people"],getattr(store,"r13_dialogue_binding",None))
        if plan:
            entry=R13_DIALOGUE_TALK_ART["people"][plan["person"]]
            if not all(frame["file"].startswith("assets/dialogue-source-master/") and renpy.loadable(frame["file"]) for profile in entry["profiles"].values() for frame in profile["frames"].values()):
                return
            if renpy.is_skipping() or renpy.in_rollback() or not persistent.room13_motion:
                plan["settled"]=True
            store.r13_dialogue_beat=plan

    def r13_dialogue_beat_settle():
        if store.r13_dialogue_beat:
            store.r13_dialogue_beat=dict(store.r13_dialogue_beat,settled=True)

    def r13_dialogue_beat_after_load():
        # Loading must never replay a saved flinch, including a restored say interaction.
        r13_dialogue_beat_settle()

    def r13_dialogue_beat_ready(person):
        return bool(store.r13_dialogue_beat and store.r13_dialogue_beat["person"]==person)

    def r13_dialogue_phase(plan, elapsed, skipping=False, motion=True):
        return plan["talk"] if plan["settled"] or skipping or not motion or elapsed>=plan["duration"] else plan["react"]

    class R13DialogueBeat(renpy.Displayable):
        def __init__(self,plan,profile,**kwargs):
            super(R13DialogueBeat,self).__init__(**kwargs)
            self.plan=plan
            self.finished=False
            self.started_st=None
            self.frames={}
            for key in (plan["talk"],plan["react"]):
                if key and key not in self.frames:
                    frame=profile["frames"][key]
                    self.frames[key]=Fixed(Transform(frame["file"],xpos=frame["offset"][0],ypos=frame["offset"][1],zoom=frame.get("scale",1.0),nearest=False,subpixel=True),xysize=tuple(profile["canvas"]))
        def visit(self):
            return list(self.frames.values())
        def render(self,width,height,st,at):
            if self.started_st is None:self.started_st=st
            elapsed=max(0.0,st-self.started_st)
            active=store.r13_dialogue_beat
            # An old retained portrait always resolves to its calm talk frame.
            plan=self.plan if active is self.plan else dict(self.plan,settled=True)
            key=plan["talk"] if self.finished else r13_dialogue_phase(plan,elapsed,renpy.is_skipping() or renpy.in_rollback(),persistent.room13_motion)
            if key==plan["talk"]:
                self.finished=True
                # Persist completion across screen reconstruction (settings, resize).
                if active is self.plan and not active["settled"]:r13_dialogue_beat_settle()
            if key!=plan["talk"]:
                renpy.redraw(self,min(.05,max(.001,plan["duration"]-elapsed)))
            return renpy.render(self.frames[key],width,height,st,at)

    R13_DIALOGUE_POSE_SOURCE = json.load(renpy.file("assets/room13-dialogue-pose-source-art.json"))

    def r13_dialogue_fit_profile(profiles,height):
        exact=profiles.get(str(int(height)))
        if exact:return exact
        if not profiles:return None
        base=min(profiles,key=lambda h:abs(int(h)-int(height)))
        ratio=float(height)/int(base);profile=profiles[base]
        frames={key:dict(frame,offset=[int(round(v*ratio)) for v in frame["offset"]],scale=frame.get("scale",1.0)*ratio) for key,frame in profile["frames"].items()}
        return dict(canvas=[max(1,int(round(v*ratio))) for v in profile["canvas"]],frames=frames)

    def r13_dialogue_source_profile(person,pose,height):
        # An unreviewed line uses the approved neutral, never an older design.
        # Meeting close-ups use approved sources; distant seated ensembles remain separate.
        if getattr(store,"r13_thought_active",False):return None
        key=r13_fullbody_key(pose)
        posed=R13_DIALOGUE_POSE_SOURCE["people"].get(person,{})
        if key in posed.get("poses",[]):return r13_dialogue_fit_profile(posed["profiles"],height)
        if key not in R13_FULLBODY_PLAIN:return None
        entry=R13_DIALOGUE_TALK_ART["people"].get(person,{})
        if entry.get("status")!="approved_runtime":return None
        return r13_dialogue_fit_profile(entry.get("profiles",{}),height)

    def r13_dialogue_source_neutral(person,pose,height):
        profile=r13_dialogue_source_profile(person,pose,height)
        if not profile:return None
        emotion=r13_fullbody_emotion(pose) if getattr(store,"r13_meeting_active",False) else "neutral"
        emotion={"surprise":"surprise_talk","flustered":"anxious"}.get(emotion,emotion)
        frame=profile["frames"].get(emotion,profile["frames"]["neutral"])
        if renpy.loadable(frame["file"]):
            return Fixed(Transform(frame["file"],xpos=frame["offset"][0],ypos=frame["offset"][1],zoom=frame.get("scale",1.0),nearest=False,subpixel=True),xysize=tuple(profile["canvas"]))
        # An approved character must never silently revert to the old pixel design.
        # A second shipped size is the same approved neutral, with its whole canvas scaled.
        posed=R13_DIALOGUE_POSE_SOURCE["people"].get(person,{})
        entry=posed if r13_fullbody_key(pose) in posed.get("poses",[]) else R13_DIALOGUE_TALK_ART["people"][person]
        for alternate in sorted(entry["profiles"],key=lambda h:abs(int(h)-int(height))):
            other=entry["profiles"][alternate]
            fallback=other["frames"]["neutral"]
            if renpy.loadable(fallback["file"]):
                art=Fixed(Transform(fallback["file"],xpos=fallback["offset"][0],ypos=fallback["offset"][1],zoom=fallback.get("scale",1.0),nearest=False,subpixel=True),xysize=tuple(other["canvas"]))
                renpy.log("Approved dialogue size fallback: %s %s -> %s" % (person,height,alternate))
                return Transform(art,xysize=tuple(profile["canvas"]),nearest=False,subpixel=True)
        renpy.log("Approved dialogue art unavailable: %s %s" % (person,frame["file"]))
        return Fixed(Text("인물 그림을 불러오지 못했습니다.\n연결을 확인한 뒤 게임을 다시 열어 주세요.",size=22,color="#fff4df",xalign=.5,ypos=100),xysize=tuple(profile["canvas"]))

    def r13_dialogue_beat_art(person,height):
        if not r13_dialogue_beat_ready(person):return None
        profile=r13_dialogue_fit_profile(R13_DIALOGUE_TALK_ART["people"][person]["profiles"],height)
        return R13DialogueBeat(store.r13_dialogue_beat,profile) if profile else None

    config.after_load_callbacks.append(r13_dialogue_beat_after_load)
