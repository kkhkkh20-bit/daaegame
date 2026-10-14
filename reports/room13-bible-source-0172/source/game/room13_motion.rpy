# Small dialogue-only performance. Field artwork and its clickable silhouette
# stay still; a two-pixel portrait idle never substitutes for an authored pose.
default persistent.room13_motion = True
default r13_motion_person = None
image r13_visitor = Null()

init 58 python:
    import math as r13_motion_math

    def r13_appearance_duration():
        return .22 if persistent.room13_motion and not renpy.is_skipping() else 0.0

    class R13PortraitEntrance:
        # One say portrait exists at a time. Screen replacement preserves its
        # timebase; remember the visible identity so a different speaker starts
        # a fresh fade without restarting an unchanged portrait every sentence.
        def __init__(self):
            self.key=None
            self.started=0.0
            self.last_st=-1.0
        def __call__(self,trans,st,at):
            key=(store.dialogue_speaker,store.dialogue_expression)
            if key!=self.key or st<self.last_st:
                self.key=key
                self.started=st
            self.last_st=st
            duration=r13_appearance_duration()
            trans.alpha=min(1.0,max(0.0,(st-self.started)/duration)) if duration else 1.0
            return 1.0/60.0 if trans.alpha<1.0 else None

    r13_portrait_entrance=R13PortraitEntrance()

    # Native artwork pixels/degrees. An interview enlarges these by about 1.5x;
    # exploration reduces them. Distinct periods/phases avoid synchronized actors.
    R13_MOTION_PROFILES = {
        "daram": (4.5, 0.90, 0.45, 0.16),
        "dad": (5.6, 0.65, 0.30, 0.10),
        "mom": (5.4, 0.65, 0.25, 0.09),
        "granny": (6.2, 0.42, 0.18, 0.06),
        "seryeon": (5.8, 0.50, 0.24, 0.09),
        "nabi": (4.8, 0.65, 0.35, 0.13),
        "bami": (6.4, 0.22, 0.60, 0.20),
        "doto": (6.1, 0.40, 0.18, 0.06),
        "buri": (5.7, 0.55, 0.20, 0.06),
        "karo": (5.2, 0.55, 0.30, 0.10),
        "neoul": (6.0, 0.42, 0.20, 0.07),
        "guard": (6.4, 0.35, 0.12, 0.04),
    }

    def r13_motion_profile(person):
        seed=sum((i+1)*ord(c) for i,c in enumerate(person))
        profile=R13_MOTION_PROFILES.get(person,
            (5.0+(seed%17)/10.0,0.38+(seed%6)*0.05,0.18+(seed%5)*0.03,0.05+(seed%4)*0.02))
        return profile, (seed%628)/100.0

    def r13_idle_clock():
        # One immutable timestamp for the complete render frame, including the
        # independently rendered focus mask. Screen st/at can have different
        # origins and must never drive an actor's clickable silhouette.
        return float(renpy.display.interface.frame_time)

    def r13_idle_kind(pose,spec,contact,speaking=False):
        if speaking or contact=="dialogue_bust":return "dialogue"
        if contact in ("background_chair","portable_stool","self_seated","floor_sit"):
            return "seated"
        if contact=="hanging":return "hanging"
        description=(pose+" "+spec.get("action_ko",spec.get("action",""))).lower()
        if contact in ("held_ledger","clipboard") or any(word in description for word in ("read","book","map","책","편지","지도","장부")):
            return "reading"
        if pose.startswith(("living_","action_")) or contact in ("surface","tool","kneeling","squatting","crouching"):
            return "working"
        return "standing"

    def r13_idle_geometry(spec,width,height,kind):
        # A whole horizontal region below the earliest contact stays EXACTLY
        # unchanged. This protects both the anchor and surrounding tool/chair
        # pixels, rather than merely pinning one point in a stretched picture.
        native_height=float(spec.get("crop",[0,0,width,height])[3] or height)
        sy=float(height)/native_height
        anchors=spec.get("anchor",{})
        limits=[]
        for key in ("hand","seat","foot"):
            point=spec.get(key,anchors.get(key))
            if point:limits.append(float(point[1])*sy-8.0)
        if kind=="dialogue":lock=height*.78
        elif kind=="standing":lock=min(limits+[height*.80])
        elif kind=="seated":lock=min(limits+[height*.49])
        elif kind in ("reading","working"):lock=min(limits+[height*.42])
        else:lock=height*.30
        # Hanging feet are at the top: keep that entire attachment still and
        # use only a tiny chest pulse below it, with no pendulum translation.
        top=height*.34 if kind=="hanging" else 0.0
        if kind=="hanging":lock=height*.69
        lock=max(top+4.0,min(height-4.0,lock))
        return int(top)//2*2,int(lock)//2*2

    def r13_idle_values(person,pose,kind,t):
        profile,phase=r13_motion_profile(person)
        period=profile[0]
        angle=t*2.0*r13_motion_math.pi/period+phase
        # A small finite set of held pixel positions avoids continuous jitter.
        # The patterns intentionally differ: reading is an occasional nod;
        # work is a slow head adjustment; standing has a longer weight shift.
        if kind=="reading":
            shift=.70*r13_motion_math.sin(angle*.43+phase)
            breath=2.0*max(0.0,r13_motion_math.sin(angle*.71))**3
        elif kind=="working":
            shift=2.0*r13_motion_math.sin(angle*.58+phase)
            breath=.80*r13_motion_math.sin(angle)
        elif kind=="seated":
            shift=1.30*r13_motion_math.sin(angle*.47+phase)
            breath=1.65*r13_motion_math.sin(angle*.81)
        elif kind=="hanging":
            shift=0.0
            breath=1.55*r13_motion_math.sin(angle*.83)
        else:
            shift=(1.55 if kind=="dialogue" else 1.90)*r13_motion_math.sin(angle*.53+phase)
            breath=1.80*r13_motion_math.sin(angle)
        if "distressed" in pose:
            shift*=.72
        # Hold a complete two-pixel state for part of the breathing cycle;
        # don't march a deformation boundary through the face every 125 ms.
        return (int(round(shift/2.0))*2,int(round(breath/2.0))*2)

    def r13_idle_bands(width,height,top,lock,values):
        shift,breath=values
        runs=[]
        last=None
        # Inverse-map two-pixel rows, so a vertical breath cannot open a seam
        # between a moving head and stationary hands. Consecutive identical
        # maps become one blit; no hundreds-of-row-blits-per-actor render loop.
        for y in range(0,height,2):
            row_height=min(2,height-y)
            if y<=top or y>=lock:
                dx=dy=0
            else:
                u=(y-top)/float(lock-top)
                neck=max(0.0,(u-.55)/.45)
                taper=1.0-neck*neck*(3.0-2.0*neck)
                bell=4.0*u*(1.0-u)
                dx=int(round(shift*taper/2.0))*2
                dy=int(round(breath*bell/2.0))*2
            source_y=max(0,min(height-row_height,y+dy))
            delta=source_y-y
            # The fixed lower region must have the same render/subsurface
            # boundary in every state, including the completely still state.
            if last is not None and y!=lock and last[2:]==[dx,delta]:
                last[1]+=row_height
            else:
                last=[y,row_height,dx,delta]
                runs.append(last)
        return tuple(tuple(run) for run in runs)

    class R13AuthoredIdle(renpy.Displayable):
        def __init__(self,art,person,pose,spec,width,height,contact=None,speaking=False,**kwargs):
            super(R13AuthoredIdle,self).__init__(**kwargs)
            self.child=renpy.displayable(art)
            # Render the final-size pixel grid once before slicing it. Slicing
            # an unflattened scaled atlas can change texture sampling at the
            # scale's internal seams even in an otherwise unmoving body part.
            self.flat=Flatten(self.child)
            self.person=person
            self.pose=pose
            self.width=max(1,int(round(width)))
            self.height=max(1,int(round(height)))
            spec=spec or {}
            self.kind=r13_idle_kind(pose,spec,contact or spec.get("contact","standing"),speaking)
            self.top,self.lock=r13_idle_geometry(spec,self.width,self.height,self.kind)
            self.layouts={}

        def visit(self):return [self.child,self.flat]

        def render(self,width,height,st,at):
            # Return the identical render, rather than a zero-offset resample.
            # OFF screenshots therefore remain byte/pixel stable.
            if self.kind!="dialogue":
                # Compatibility for field displayables retained by older saves.
                # No redraw, raster warp, or mask-only movement in exploration.
                return renpy.render(self.child,self.width,self.height,st,at)
            if not persistent.room13_motion or renpy.is_skipping():
                # A retained say portrait also notices ON after the settings
                # screen closes; no scene/pose replacement is required.
                renpy.redraw(self,.20)
                return renpy.render(self.child,self.width,self.height,st,at)
            child=renpy.render(self.flat,self.width,self.height,st,at)
            clock=r13_idle_clock()
            frame=int(clock*8.0)/8.0
            values=r13_idle_values(self.person,self.pose,self.kind,frame)
            runs=self.layouts.get(values)
            if runs is None:
                runs=r13_idle_bands(self.width,self.height,self.top,self.lock,values)
                if len(self.layouts)>=32:self.layouts.clear()
                self.layouts[values]=runs
            result=renpy.Render(self.width,self.height)
            for y,row_height,dx,dy in runs:
                # Clip within the original bounds on both sides. Geometry,
                # stage placement and the mask's coordinate space never grow.
                sx=max(0,-dx)
                target_x=max(0,dx)
                row_width=self.width-abs(dx)
                result.blit(child.subsurface((sx,y+dy,row_width,row_height)),(target_x,y))
            # All actor/mask instances wake at the same global 8 Hz boundary,
            # even if a focus mask was first requested later than the picture.
            renpy.redraw(self,max(.005,.125-(clock-frame)))
            return result

    def r13_idle_art(art,person,pose,spec,width,height,contact=None,speaking=False):
        # Both visible world art and its alpha hit mask use this exact path.
        # Dialogue/topic portraits explicitly pass dialogue_bust even between lines.
        if not speaking and contact!="dialogue_bust":
            return renpy.displayable(art)
        return renpy.displayable(art)

    class R13CharacterMotion:
        def __init__(self,person,pose,speaking=False,entrance=False):
            self.person=person
            self.pose=pose
            self.profile,self.phase=r13_motion_profile(person)
            self.speaking=speaking
            self.entrance=entrance

        def __call__(self,trans,st,at):
            if not self.speaking or not persistent.room13_motion or renpy.is_skipping():
                trans.xoffset=0.0
                trans.yoffset=0.0
                trans.rotate=0.0
                trans.alpha=1.0
                return 0.20
            trans.xoffset=0
            trans.yoffset=0
            trans.rotate=0
            trans.alpha=1.0
            return None

    R13_PIXEL_MOTION=json.load(renpy.file("assets/room13-pixel-motion.json"))

    class R13TailMotion:
        # Pickle compatibility for pre-pixel saves. after_load replaces the
        # old composed actor before rendering; this shim never loads old art.
        def __init__(self,pose):
            self.tense="distressed" in pose
        def __call__(self,trans,st,at):
            trans.rotate=0
            return .2

    class R13PixelTailMotion:
        def __init__(self,pose):
            self.tense="distressed" in pose
        def __call__(self,trans,st,at):
            enabled=persistent.room13_motion and not renpy.is_skipping()
            # The attachment stays behind the separately authored body. One
            # native-pixel step avoids blurred rotation or a painted tail layer.
            trans.xoffset=0
            trans.yoffset=0
            return .125 if enabled else .2

    def r13_pixel_daram_layers(pose):
        expression=next((key for key in ("thinking","distressed","expressive") if key in pose),"neutral")
        data=R13_PIXEL_MOTION
        spec=data["poses"][expression]
        body=Crop(tuple(spec["body"]),data["file"])
        if spec.get("body_size"):
            body=Transform(body,size=tuple(spec["body_size"]),nearest=True)
        tail=Crop(tuple(spec["tail"]),data["file"])
        kwargs=dict(subpixel=False,nearest=True,function=R13PixelTailMotion(pose))
        if spec.get("tail_size"):kwargs["size"]=tuple(spec["tail_size"])
        tail=Transform(tail,**kwargs)
        return Composite(tuple(data["canvas"]),tuple(spec["tail_pos"]),tail,tuple(spec.get("body_pos",[0,0])),body)

    def r13_motion_art(image_name,person,pose,speaking=False,entrance=False):
        spec=r13_acting_spec(person,pose)
        if spec:
            # Living poses have authored prop/floor contacts: idle translation
            # would make hands float away from tools and feet leave the floor.
            # Redesigned Daram never inherits the old body/tail composite.
            return Transform(Crop(tuple(spec["crop"]),spec["file"]),nearest=True,subpixel=False)
        # Pre-redesign fallback remains static in the field as well.
        if not speaking:
            return Transform(image_name,subpixel=False,nearest=True)
        # Only old dialogue art may use independently authored tail layers.
        art=r13_pixel_daram_layers(pose) if person=="daram" else image_name
        return Transform(art,subpixel=False,nearest=True,rotate_pad=False,
            function=R13CharacterMotion(person,pose,speaking,entrance))

screen r13_motion_settings():
    textbutton ("인물 전환 효과: 켜짐" if persistent.room13_motion else "인물 전환 효과: 정지"):
        action ToggleField(persistent,"room13_motion")
        xfill True

# Only the art receives opacity. Coordinates, background and dialogue panels
# remain fixed, and stable screen IDs retain this timeline on reevaluation.
transform r13_actor_appear(duration=.22):
    subpixel False
    nearest True
    alpha 0.0
    linear duration alpha 1.0

# Master-layer tags deliberately retain ATL state when replaced. Restart the
# entrance for an actual new speaker; unchanged speakers are not re-shown.
transform r13_actor_enter(duration=.22):
    subpixel False
    nearest True
    on show:
        alpha 0.0
        linear duration alpha 1.0
    on replace:
        # No authored motion frames: swap the expression once and hold it.
        alpha 1.0
        yoffset 0
