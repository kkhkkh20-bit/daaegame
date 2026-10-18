# Isolated SDK comparison fixture. No production caller or default effect change.
default r13_effect_review_enabled = False
default r13_effect_review_mode = "A"
default r13_effect_review_manual = False
default r13_effect_review_phase = 0
default r13_effect_review_started = 0.0

transform r13_effect_review_slide():
    subpixel True
    zoom 1.10
    xalign .5 yalign .5
    xoffset -56
    easeout .28 xoffset 0

transform r13_effect_review_zoom():
    subpixel True
    xalign .5 yalign .5
    zoom 1.04
    easeout .22 zoom 1.0

# Our proposal: current image plus two trailing positions, not reference footage.
transform r13_effect_review_trail_fade(opacity=1.0):
    alpha opacity
    pause .06
    linear .28 alpha 0.0

init 193 python:
    def r13_review_route(people,old,new):
        start=people.index(old);end=people.index(new)
        delta=(end-start)%len(people)
        if delta>len(people)/2.0:delta-=len(people)
        direction=1 if delta>0 else -1
        passing=[people[(start+direction*n)%len(people)] for n in range(1,abs(delta))]
        return start,delta,passing

    class R13ReviewOrbitLayer(R13MeetingOrbit):
        def __init__(self,focus,start,delta,components,people=None,lag=0,**kwargs):
            super(R13ReviewOrbitLayer,self).__init__("C2",focus,0,"listen",{},**kwargs)
            self.review_fixed_view=True
            self.review_components=components
            self.review_actor_ids=self.people if people is None else people
            self.start=start;self.delta=delta;self.lag=lag
        def render(self,width,height,st,at):
            p=max(0.0,min(1.0,(st-self.lag)/.34))
            self.review_view_override=self.start+self.delta*(1-(1-p)**3)
            if st<.34+self.lag:renpy.redraw(self,0)
            return super(R13ReviewOrbitLayer,self).render(width,height,st,at)

    class R13DirectionalTrailReview(renpy.Displayable):
        def __init__(self,art,settled,old_focus,**kwargs):
            super(R13DirectionalTrailReview,self).__init__(**kwargs)
            self.settled=settled;self.arrival=art.focus
            start,delta,self.passing=r13_review_route(art.people,old_focus,art.focus)
            assert self.arrival not in self.passing
            regular=[p for p in art.people if p not in self.passing and p!=self.arrival]
            layers=[R13ReviewOrbitLayer(art.focus,start,delta,("background","actors"),regular),
                R13ReviewOrbitLayer(art.focus,start,delta,("actors",),self.passing)]
            # Transparent character layers only; arrival/background/UI never enter echoes.
            for lag,alpha,blur in ((.055,.26,3),(.11,.15,6)):
                source=R13ReviewOrbitLayer(art.focus,start,delta,("actors",),self.passing,lag)
                layers.append(At(Transform(Flatten(source),blur=blur),r13_effect_review_trail_fade(alpha)))
            # Draw arrival exactly once, sharp, in front of echoes; table occlusion stays last.
            layers.append(R13ReviewOrbitLayer(art.focus,start,delta,("actors",),[self.arrival]))
            layers.append(R13ReviewOrbitLayer(art.focus,start,delta,("foreground",),[]))
            self.moving=Fixed(*layers,xysize=(1280,720))
        def render(self,width,height,st,at):
            if st>=.34 or not persistent.room13_motion or renpy.is_skipping() or renpy.in_rollback():
                return renpy.render(self.settled,width,height,st,at)
            renpy.redraw(self,0)
            return renpy.render(self.moving,width,height,st,st)
        def visit(self):return [self.moving,self.settled]

    def r13_effect_review_advance():
        store.r13_effect_review_phase=(store.r13_effect_review_phase+1)%3
        store.r13_effect_review_started=renpy.display.core.get_time()

    class R13EffectReview(renpy.Displayable):
        """Same approved C2 artwork and authored lines; only stage transition differs."""
        def __init__(self,mode,**kwargs):
            super(R13EffectReview,self).__init__(**kwargs)
            self.mode=mode
            rows=R13_DEBATE["C2"]["statements"][0]
            self.rows=[(rows["who"],rows["text"])]+list(rows["broken"])
            if mode=="D":
                # Reuse reviewed source text directly; no duplicate dialogue registration.
                opening=R13_DIALOGUE_BEATS["lines"]["trial:opening"]
                self.rows=[(opening[str(i)]["person"],opening[str(i)]["text"]) for i in (0,1,0)]
            self.scenes=[];self.effects=[];self.dialogues=[];self.arts=[]
            for who,text in self.rows:
                art=R13MeetingOrbit("C2",who,0,"listen",{})
                art.review_fixed_view=True
                self.arts.append(art)
                # A needs symmetric overscan to avoid exposed frame edges.
                scene=Fixed(Transform(art,zoom=1.10,xalign=.5,yalign=.5),xysize=(1280,720)) if mode=="A" else art
                self.scenes.append(scene)
                self.dialogues.append(Fixed(
                    Transform(R13InkPanel(),xpos=100,ypos=548,xsize=1080,ysize=150),
                    Text(R13_NAMES.get(who,who),xpos=128,ypos=565,size=24,color="#f5e6cb"),
                    Text(text,xpos=128,ypos=603,xmaximum=1024,size=23,color="#f5e6cb"),xysize=(1280,720)))
            for i,scene in enumerate(self.scenes):
                if i==0:self.effects.append(scene)
                elif mode=="A":self.effects.append(Fixed(At(self.arts[i],r13_effect_review_slide),xysize=(1280,720)))
                elif mode=="B":self.effects.append(renpy.display.transition.Dissolve(.38,old_widget=self.scenes[i-1],new_widget=scene))
                elif mode=="D":self.effects.append(R13DirectionalTrailReview(self.arts[i],scene,self.rows[i-1][0]))
                else:self.effects.append(Fixed(At(scene,r13_effect_review_zoom),xysize=(1280,720)))
        def render(self,width,height,st,at):
            phase=0 if st<2.0 else 1 if st<5.5 else 2
            elapsed=st-(0,2.0,5.5)[phase]
            if store.r13_effect_review_manual:
                phase=store.r13_effect_review_phase
                elapsed=max(0.0,renpy.display.core.get_time()-store.r13_effect_review_started)
            out=renpy.Render(1280,720)
            out.blit(renpy.render(self.effects[phase],1280,720,elapsed,elapsed),(0,0))
            out.blit(renpy.render(self.dialogues[phase],1280,720,st,at),(0,0))
            renpy.redraw(self,0 if phase and elapsed<.42 else max(.01,(2.0 if phase==0 else 5.5 if phase==1 else st+1)-st))
            return out
        def visit(self):return self.scenes+self.effects+self.dialogues

screen r13_effect_review_screen(mode):
    modal True
    zorder 300
    add R13EffectReview(mode) id "effect_review"
    if r13_effect_review_manual:
        key "mouseup_1" action Function(r13_effect_review_advance)
    frame:
        xpos 24 ypos 20 padding (14,8) background Solid("#17202bed")
        text (mode+" · "+{"A":"짧은 가로 이동","B":"짧은 디졸브","C":"작은 줌 정착","D":"통과 인물만 잔상 · 도착 인물 선명"}[mode]+"   |   비교용 · 미적용") size 25 color "#ffffff"

label r13_effect_review:
    if not r13_effect_review_enabled:
        return
    $ renpy.music.stop(channel="ambience")
    $ renpy.music.play(R13_BGM["council"],channel="music",loop=True)
    $ renpy.music.set_volume(.65,channel="music")
    call screen r13_effect_review_screen(r13_effect_review_mode)
    return
