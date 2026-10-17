# A single world-space camera. Seats never animate from one UI card to another.
# The near table, fixed cast and far architecture share the same continuous yaw.
init 175 python:
    import math as r13_orbit_math

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
        return int(round(x)),depth,angle

    def r13_meeting_world_tiles(out,normal,mirror,position,y=0):
        width=normal.get_size()[0]
        start=-int(position%(2*width))
        for index in range(4):
            out.blit(normal if index%2==0 else mirror,(start+index*width,y))

    class R13MeetingSurface(renpy.Displayable):
        def __init__(self,session,view,count,shade,**kwargs):
            super(R13MeetingSurface,self).__init__(**kwargs)
            self.view=view;self.count=count
            plate=r13_meeting_plate(session,True)
            band=(160,490,960,180) if r13_meeting_kind(session)=="stone" else (160,470,960,250)
            self.art=Transform(Crop(band,plate),xysize=(1280,340),nearest=True,
                matrixcolor=BrightnessMatrix(-.025-shade*.35))
            self.flip=Transform(self.art,xzoom=-1)
        def render(self,width,height,st,at):
            out=renpy.Render(1280,720)
            a=renpy.render(self.art,1280,340,st,at);b=renpy.render(self.flip,1280,340,st,at)
            r13_meeting_world_tiles(out,a,b,self.view*5120.0/max(1,self.count),380)
            return out
        def visit(self):return [self.art,self.flip]

    class R13MeetingOrbit(renpy.Displayable):
        def __init__(self,claim,focus,revision,beat,poses,**kwargs):
            super(R13MeetingOrbit,self).__init__(**kwargs)
            self.claim=claim;self.focus=focus
            self.session=r13_debate_session(claim);self.kind=r13_meeting_kind(self.session)
            self.people=[p for p,_ in r13_meeting_cast(claim,self.session)]
            self.poses=dict(poses or {});self.beat=beat
            self.shade=R13_MEETING_BEATS.get(beat,R13_MEETING_BEATS["listen"])[3]
            tint="#e4eeff" if self.kind=="stone" else "#fff3df" if self.kind=="round" else "#eef3ff"
            self.plate=Transform(r13_meeting_plate(self.session,True),
                matrixcolor=TintMatrix(tint)*SaturationMatrix(.86)*BrightnessMatrix(-.035-self.shade))
            self.flip=Transform(self.plate,xzoom=-1)
            self.art={}
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
            reacting=False
            for _distance,person,(cx,depth,angle) in sorted(slots,reverse=True):
                pose=self.poses.get(person,"neutral")
                base=840 if self.kind in ("round","stone") else 740
                key=(person,pose)
                if key not in self.art:
                    art=r13_fullbody_close_art(person,pose,base)
                    if art is None:art=Transform(r13_meeting_actor(person,self.focus,cx),ysize=base,fit="contain",nearest=True)
                    self.art[key]=art
                central=person==self.focus
                gain=(.065 if self.beat in ("interrupt","explain","shaken","gasp","cornered") else .0) if central else -.05-self.shade*.35
                art=Transform(self.art[key],zoom=depth,xzoom=r13_orbit_math.cos(angle*.35),nearest=True,
                    matrixcolor=BrightnessMatrix(gain))
                rendered=renpy.render(art,1280,1000,st,at)
                x=int(cx+(r13_close_x(person,pose,base)-640)*depth-rendered.get_size()[0]/2)
                y=int(r13_fullbody_close_y(person,base,96,pose)*depth+(1-depth)*240)
                # A startled body recoils once in its own fixed seat; the camera stays still.
                if person==getattr(store,"r13_meeting_shock_target",None) and persistent.room13_motion:
                    elapsed=renpy.display.core.get_time()-getattr(store,"r13_meeting_shock_at",0.0)
                    if 0<=elapsed<.36:
                        y-=int(34*r13_orbit_math.sin(r13_orbit_math.pi*elapsed/.36));reacting=True
                out.blit(rendered,(x,y))
            if self.kind in ("round","stone"):
                surface=R13MeetingSurface(self.session,view,len(self.people),self.shade)
                foreground=renpy.render(AlphaMask(surface,R13MeetingForeground(self.session,True)),1280,720,st,at)
                out.blit(foreground,(0,0))
            if moving or reacting:renpy.redraw(self,.016)
            return out
        def visit(self):return [self.plate,self.flip]+list(self.art.values())
