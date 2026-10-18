# C2 presentation only. Authored dialogue, speakers, evidence and branches are untouched.
default r13_c2_edit = {}
default r13_c2_pair_poses = {}

init 195 python:
    R13_MEETING_RESUME_FIELDS=R13_MEETING_RESUME_FIELDS+("r13_c2_edit","r13_c2_pair_poses")
    def r13_c2_pair_for(identity,person):
        # A sustained authored exchange, not a keyword or a one-line interruption.
        sustained=("debate:counter:C2:s3","debate:counter_ok:C2:s3",
            "debate:counter_wrong:C2:s3:weak")
        return ("resident_ppul","dad") if identity in sustained and person in ("resident_ppul","dad") else None

    _r13_c2_direct_line=r13_meeting_direct_line
    def r13_meeting_direct_line(identity,index,packet,expression,pose):
        expression,pose=_r13_c2_direct_line(identity,index,packet,expression,pose)
        if not store.r13_meeting_active or store.r13_meeting_claim!="C2":
            store.r13_c2_edit={};store.r13_c2_pair_poses={}
            return expression,pose
        token=(identity,index,packet[0],packet[1])
        old=store.r13_c2_edit or {}
        if old.get("token")==token:
            if old.get("pair"):
                kept=dict(store.r13_meeting_direction_poses or {});kept.update(store.r13_c2_pair_poses or {})
                store.r13_meeting_direction_poses=kept
            return expression,pose
        person=packet[0];pair=r13_c2_pair_for(identity,person)
        poses=dict(store.r13_meeting_direction_poses or {})
        if pair:
            kept=dict(store.r13_c2_pair_poses or {}) if old.get("pair")==pair else {}
            for who in pair:
                if who==person or who not in kept:kept[who]=poses.get(who,pose if who==person else "neutral")
            store.r13_c2_pair_poses=kept
            poses.update(kept);store.r13_meeting_direction_poses=poses
        else:store.r13_c2_pair_poses={}
        listener=store.r13_meeting_listener
        if not listener and old.get("speaker") in CAST and old.get("speaker")!=person:listener=old["speaker"]
        if listener==person:listener=None
        if person not in CAST:listener=None
        store.r13_c2_edit=dict(token=token,speaker=person,pair=pair,listener=listener,
            phase="pending" if listener and not pair else "settled",
            cue="enter" if pair and old.get("pair")!=pair else "hold" if pair else "exit" if old.get("pair") else "reaction")
        return expression,pose

    _r13_c2_direct_end=r13_meeting_direct_end
    def r13_meeting_direct_end():
        _r13_c2_direct_end()
        store.r13_c2_edit={};store.r13_c2_pair_poses={}

    def r13_c2_edit_after_load():
        # Pair/left-right/pressure survive; a brief reaction never replays on load.
        if store.r13_c2_edit:store.r13_c2_edit=dict(store.r13_c2_edit,phase="settled")
    config.after_load_callbacks.append(r13_c2_edit_after_load)

    class R13C2Editorial(renpy.Displayable):
        def __init__(self,focus,**kwargs):
            super(R13C2Editorial,self).__init__(**kwargs)
            state=dict(store.r13_c2_edit or {})
            self.token=state.get("token");self.pair=state.get("pair")
            self.focus=state.get("speaker") if state.get("speaker") in CAST else focus
            self.listener=state.get("listener")
            self.started=None;self.claimed=False
            self.shots={}
            for who in set([self.focus,self.listener]+list(self.pair or ())):
                if who not in CAST:continue
                shot=R13MeetingOrbit("C2",who,store.r13_meeting_shot_revision,
                    (store.r13_meeting_direction or {}).get("beat","listen"),
                    store.r13_meeting_direction_poses,store.r13_meeting_line_token,
                    store.r13_meeting_listener,store.r13_meeting_art_slots,
                    store.r13_meeting_reaction,portrait_focus=True)
                shot.review_fixed_view=True
                self.shots[who]=shot
            self.panel=None
            if self.pair:
                pieces=[r13_meeting_plate("trial",False)]
                for i,who in enumerate(self.pair):
                    active=who==self.focus;x=20+i*630
                    # One crop transform for the entire room/person/table composition.
                    art=Transform(Crop((310,70,660,430),self.shots[who]),xsize=600,ysize=391,
                        matrixcolor=BrightnessMatrix(0 if active else -.10))
                    pieces.extend([Transform(R13PaperFrame() if active else R13InkPanel(),xpos=x,ypos=90,xsize=610,ysize=400),
                        Transform(art,xpos=x+5,ypos=98),
                        Transform(R13InkPanel(slim=True),xpos=x+14,ypos=108,xsize=210,ysize=36),
                        Text(R13_NAMES[who]+(" · 발언" if active else ""),xpos=x+24,ypos=114,size=21,color="#f5e6cb")])
                self.panel=Fixed(*pieces,xysize=(1280,720))
        def render(self,width,height,st,at):
            if self.panel is not None:return renpy.render(self.panel,width,height,st,at)
            shot=self.shots.get(self.focus)
            if shot is None:return renpy.render(r13_meeting_plate("trial",False),width,height,st,at)
            state=store.r13_c2_edit or {}
            enabled=persistent.room13_motion and not renpy.is_skipping() and not store.r13_fast_all and not renpy.in_rollback()
            current=state.get("token")==self.token
            if not renpy.predicting() and current and state.get("phase") in ("pending","playing"):
                if not enabled or (state.get("phase")=="playing" and not self.claimed):
                    store.r13_c2_edit=dict(state,phase="settled")
                else:
                    if not self.claimed:
                        self.claimed=True;self.started=st
                        store.r13_c2_edit=dict(state,phase="playing")
                    elapsed=max(0,st-self.started)
                    if elapsed<1.1:renpy.redraw(self,1.1-elapsed)
                    elif elapsed<1.8:
                        shot=self.shots.get(self.listener,shot);renpy.redraw(self,1.8-elapsed)
                    else:store.r13_c2_edit=dict(state,phase="settled")
            return renpy.render(shot,width,height,st,at)
        def visit(self):return list(self.shots.values())+([self.panel] if self.panel is not None else [])

init 196 python:
    def r13_ppul_v2_art(slot,height):
        # Source canvas matches approved neutral. Keep its uniform scale and align
        # alpha32 foot baseline: neutral 1498, shock 1497, panic 1490.
        ratio=float(height)/840
        dy=1 if slot=="shockburst" else 8
        scale=594.0/1029
        return Fixed(Transform("assets/ppul-comic-v2/resident_ppul--"+slot+".webp",
            xpos=int(round(8*ratio)),ypos=int(round((33+dy*scale)*ratio)),zoom=scale*ratio,
            nearest=False,subpixel=True),xysize=(int(round(611*ratio)),int(round(906*ratio))))

    _r13_c2_slot_art=r13_meeting_slot_art
    def r13_meeting_slot_art(person,height):
        if store.r13_meeting_claim=="C2" and person=="resident_ppul" and r13_meeting_pressure_level(person)>0:
            pose=(store.r13_meeting_direction_poses or {}).get(person,"neutral")
            # Authored anger is the attempted recovery; do not turn it into panic.
            if pose in ("neutral","anxious","flustered","surprise"):
                return r13_ppul_v2_art("ongoingpanic",height)
        return _r13_c2_slot_art(person,height)

    _r13_c2_collective_art=r13_meeting_collective_art
    def r13_meeting_collective_art(person,height):
        if store.r13_meeting_claim=="C2" and person=="resident_ppul":
            return r13_ppul_v2_art("shockburst",height)
        return _r13_c2_collective_art(person,height)
