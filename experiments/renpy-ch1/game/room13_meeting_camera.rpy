# A single world-space camera. Seats never animate from one UI card to another.
# The near table, fixed cast and far architecture share the same continuous yaw.
init 175 python:
    import math as r13_orbit_math
    import json as r13_meeting_art_json
    R13_MEETING_SOURCE_ART=r13_meeting_art_json.load(renpy.file("assets/room13-meeting-source-art.json"))

    def r13_meeting_world_view(claim,focus):
        people=[p for p,_ in r13_meeting_cast(claim,r13_debate_session(claim))]
        target=people.index(focus) if focus in people else 0
        old=getattr(store,"r13_meeting_previous_focus",None)
        if old not in people:return float(target),False
        start=people.index(old);delta=(target-start)%len(people)
        if delta>len(people)/2.0:delta-=len(people)
        enabled=persistent.room13_motion and not renpy.is_skipping()
        if not enabled or not delta or r13_meeting_direct_duration()<=0:return float(start+delta),False
        revision=getattr(store,"r13_meeting_shot_revision",0)
        now=renpy.display.core.get_time()
        if getattr(store,"r13_meeting_pan_painted_revision",-1)!=revision:
            store.r13_meeting_pan_painted_revision=revision
            store.r13_meeting_pan_started=now
        duration=min(.44,r13_meeting_direct_duration()+max(0,abs(delta)-1)*.055)
        u=min(1.0,max(0.0,(now-store.r13_meeting_pan_started)/max(.01,duration)))
        ease=u*u*(3-2*u)
        return start+delta*ease,u<1.0

    def r13_meeting_world_slot(index,view,count):
        # Three visible seats, projected from one fixed circular seat arrangement.
        delta=(index-view+count/2.0)%count-count/2.0
        step=2*r13_orbit_math.pi/max(7,count)
        angle=delta*step
        if abs(angle)>r13_orbit_math.radians(72):return None
        focal=573.0/r13_orbit_math.tan(step)
        x=640+focal*r13_orbit_math.tan(angle)
        if x< -540 or x>1820:return None
        depth=max(.65,1.0-.18*(1-r13_orbit_math.cos(angle))/max(.01,1-r13_orbit_math.cos(step)))
        return x,depth,angle

    def r13_meeting_orbit_height(session):
        return 840 if r13_meeting_kind(session) in ("round","stone") else 740

    def r13_meeting_portrait_x(session,x,width,focused=False):
        return x

    def r13_meeting_world_tiles(out,normal,mirror,position,y=0):
        width=normal.get_size()[0]
        start=-(position%(2*width))
        for index in range(4):
            out.subpixel_blit(normal if index%2==0 else mirror,(start+index*width,y))

    class R13MeetingSurface(renpy.Displayable):
        def __init__(self,session,view,count,shade,**kwargs):
            super(R13MeetingSurface,self).__init__(**kwargs)
            self.view=view;self.count=count
            self.y=476 if r13_meeting_kind(session)=="round" else 440
            plate=r13_meeting_plate(session,True)
            band=(160,490,960,180) if r13_meeting_kind(session)=="stone" else (160,470,960,250)
            self.art=Transform(Crop(band,plate),xysize=(1280,340),nearest=True,
                matrixcolor=BrightnessMatrix(-.025-shade*.35))
            self.flip=Transform(self.art,xzoom=-1)
        def render(self,width,height,st,at):
            out=renpy.Render(1280,720)
            a=renpy.render(self.art,1280,340,st,at);b=renpy.render(self.flip,1280,340,st,at)
            r13_meeting_world_tiles(out,a,b,self.view*5120.0/max(1,self.count),self.y)
            return out
        def visit(self):return [self.art,self.flip]

    def r13_meeting_slot_art(person,height):
        slot=(getattr(store,"r13_meeting_art_slots",{}) or {}).get(person)
        spec=R13_MEETING_SOURCE_ART.get(person,{}).get(slot)
        if not spec or not renpy.loadable(spec["file"]):return None
        ratio=float(height)/840
        # Same canvas and neutral head placement as the approved dialogue source.
        # No automatic mirroring: front-facing art remains front-facing.
        return Fixed(Transform(spec["file"],xpos=int(round(spec["offset"][0]*ratio)),
            ypos=int(round(spec["offset"][1]*ratio)),zoom=spec["scale"]*ratio,nearest=False,subpixel=True),
            xysize=tuple(int(round(v*ratio)) for v in spec["canvas"]))

    def r13_meeting_reaction_phase(reaction,token,claimed,elapsed,disabled=False):
        # A fresh displayable never replays an already claimed token. Elapsed
        # display time is local; only token + phase are saved/rolled back.
        if not reaction or reaction.get("token")!=token or disabled:return "settled"
        phase=reaction.get("phase","settled")
        if phase=="pending":return "settled" if claimed else "playing"
        if phase=="playing" and claimed and elapsed<.35:return "playing"
        return "settled"

    class R13MeetingReaction(renpy.Displayable):
        def __init__(self,token,react,settled,**kwargs):
            super(R13MeetingReaction,self).__init__(**kwargs)
            self.token=token;self.react=react;self.settled=settled
            self.claimed=False;self.started=None
        def visit(self):return [self.react,self.settled]
        def render(self,width,height,st,at):
            if renpy.predicting():return renpy.render(self.settled,width,height,st,at)
            reaction=getattr(store,"r13_meeting_reaction",None)
            elapsed=0.0 if self.started is None else max(0.0,st-self.started)
            phase=r13_meeting_reaction_phase(reaction,self.token,self.claimed,elapsed,
                renpy.is_skipping() or renpy.in_rollback() or not persistent.room13_motion)
            if phase=="playing":
                if not self.claimed:
                    self.claimed=True;self.started=st
                    store.r13_meeting_reaction=dict(reaction,phase="playing")
                renpy.redraw(self,.035)
                return renpy.render(self.react,width,height,st,at)
            if reaction and reaction.get("token")==self.token and reaction.get("phase")!="settled":
                r13_meeting_reaction_settle()
            return renpy.render(self.settled,width,height,st,at)

    def r13_meeting_reaction_art(person,pose,height,settled):
        reaction=getattr(store,"r13_meeting_reaction",None)
        if not reaction or reaction.get("person")!=person or reaction.get("phase")=="settled":return settled
        # Only approved, existing source frames. Missing sixth slots fail closed.
        profile=r13_dialogue_source_profile(person,"surprise",height)
        frame=(profile or {}).get("frames",{}).get("surprise_react")
        if not frame or not renpy.loadable(frame["file"]):return settled
        react=Fixed(Transform(frame["file"],xpos=frame["offset"][0],ypos=frame["offset"][1],
            zoom=frame.get("scale",1.0),nearest=False,subpixel=True),xysize=tuple(profile["canvas"]))
        return R13MeetingReaction(reaction["token"],react,settled)

    class R13MeetingOrbit(renpy.Displayable):
        def __init__(self,claim,focus,revision,beat,poses,line_token=None,listener=None,slots=None,reaction=None,**kwargs):
            super(R13MeetingOrbit,self).__init__(**kwargs)
            self.claim=claim;self.focus=focus
            self.session=r13_debate_session(claim);self.kind=r13_meeting_kind(self.session)
            self.people=[p for p,_ in r13_meeting_cast(claim,self.session)]
            self.poses=dict(poses or {});self.beat=beat
            self.shade=R13_MEETING_BEATS.get(beat,R13_MEETING_BEATS["listen"])[3]
            tint="#e4eeff" if self.kind=="stone" else "#fff3df" if self.kind=="round" else "#eef3ff"
            # Uniform enlargement and centered crop lowers the authored horizon
            # with the close table edge; neither the table nor background is squashed.
            plate=r13_meeting_plate(self.session,True)
            zoom=1.24 if self.kind=="round" else 1.14 if self.kind=="stone" else 1.0
            if zoom!=1.0:plate=Crop((int(1280*(zoom-1)/2),0,1280,720),Transform(plate,zoom=zoom))
            self.plate=Transform(plate,
                matrixcolor=TintMatrix(tint)*SaturationMatrix(.86)*BrightnessMatrix(-.035-self.shade))
            self.flip=Transform(self.plate,xzoom=-1)
            self.art={};self.offsets={}
            base=r13_meeting_orbit_height(self.session)
            # Build/predict each portrait once per shot, never inside the frame loop.
            for person in self.people:
                pose=self.poses.get(person,"neutral")
                art=r13_meeting_slot_art(person,base)
                if art is None:art=r13_fullbody_close_art(person,pose,base)
                if art is None:art=Transform(r13_meeting_actor(person,self.focus,640),ysize=base,fit="contain",nearest=True)
                # 2026-10-26 소유자: 인물 그림에 흰 테두리 스티커를 두르지 않는다. 회의 근접 화면도 같다.
                art=r13_meeting_reaction_art(person,pose,base,art)
                gain=(.065 if self.beat in ("interrupt","explain","shaken","gasp","cornered") else .0) if person==self.focus else (-.01 if person==listener else -.05)-self.shade*.35
                self.art[person]=Transform(art,nearest=not bool(r13_dialogue_source_profile(person,pose,base)),subpixel=True,matrixcolor=BrightnessMatrix(gain))
                self.offsets[person]=(r13_close_x(person,pose,base)-640,r13_fullbody_close_y(person,base,96,pose))
            self.surface=R13MeetingSurface(self.session,0,len(self.people),self.shade) if self.kind in ("round","stone") else None
            self.foreground=AlphaMask(self.surface,R13MeetingForeground(self.session,True)) if self.surface is not None else None
        def render(self,width,height,st,at):
            out=renpy.Render(1280,720)
            if renpy.predicting():view=float(self.people.index(self.focus)) if self.focus in self.people else 0.0;moving=False
            else:view,moving=r13_meeting_world_view(self.claim,self.focus)
            a=renpy.render(self.plate,1280,720,st,at);b=renpy.render(self.flip,1280,720,st,at)
            r13_meeting_world_tiles(out,a,b,view*2560.0/max(1,len(self.people)))
            slots=[]
            for index,person in enumerate(self.people):
                slot=r13_meeting_world_slot(index,view,len(self.people))
                if slot is not None:slots.append((abs(slot[2]),person,slot))
            for _distance,person,(cx,depth,angle) in sorted(slots,reverse=True):
                art=self.art[person]
                scale=r13_orbit_math.cos(angle*.35)
                if art.zoom!=depth or art.xzoom!=scale:
                    art.zoom=depth;art.xzoom=scale;renpy.redraw(art,0)
                rendered=renpy.render(art,1280,1000,st,at)
                dx,dy=self.offsets[person]
                x=cx+dx*depth-rendered.get_size()[0]/2
                x=r13_meeting_portrait_x(self.session,x,rendered.get_size()[0],person==self.focus)
                y=dy*depth+(1-depth)*240
                out.subpixel_blit(rendered,(x,y))
            if self.surface is not None:
                if self.surface.view!=view:
                    self.surface.view=view;renpy.redraw(self.surface,0)
                foreground=renpy.render(self.foreground,1280,720,st,at)
                out.blit(foreground,(0,0))
            if moving:renpy.redraw(self,0)
            return out
        def visit(self):return [self.plate,self.flip]+list(self.art.values())+([self.foreground] if self.foreground is not None else [])
