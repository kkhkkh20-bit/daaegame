# Isolated SDK comparison fixture. No production caller or default effect change.
default r13_effect_review_enabled = False
default r13_effect_review_mode = "A"

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

init 193 python:
    class R13EffectReview(renpy.Displayable):
        """Same approved C2 artwork and authored lines; only stage transition differs."""
        def __init__(self,mode,**kwargs):
            super(R13EffectReview,self).__init__(**kwargs)
            self.mode=mode
            rows=R13_DEBATE["C2"]["statements"][0]
            self.rows=[(rows["who"],rows["text"])]+list(rows["broken"])
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
                elif mode=="B":self.effects.append(renpy.display.transition.Dissolve(.24,old_widget=self.scenes[i-1],new_widget=scene))
                else:self.effects.append(Fixed(At(scene,r13_effect_review_zoom),xysize=(1280,720)))
        def render(self,width,height,st,at):
            phase=0 if st<2.0 else 1 if st<5.5 else 2
            elapsed=st-(0,2.0,5.5)[phase]
            out=renpy.Render(1280,720)
            out.blit(renpy.render(self.effects[phase],1280,720,elapsed,elapsed),(0,0))
            out.blit(renpy.render(self.dialogues[phase],1280,720,st,at),(0,0))
            renpy.redraw(self,0 if phase and elapsed<.32 else max(.01,(2.0 if phase==0 else 5.5 if phase==1 else st+1)-st))
            return out
        def visit(self):return self.scenes+self.effects+self.dialogues

screen r13_effect_review_screen(mode):
    modal True
    zorder 300
    add R13EffectReview(mode)
    frame:
        xpos 24 ypos 20 padding (14,8) background Solid("#17202bed")
        text (mode+" · "+{"A":"짧은 가로 이동","B":"짧은 디졸브","C":"작은 줌 정착"}[mode]+"   |   비교용 · 미적용") size 25 color "#ffffff"

label r13_effect_review:
    if not r13_effect_review_enabled:
        return
    $ renpy.music.stop(channel="ambience")
    $ renpy.music.play(R13_BGM["council"],channel="music",loop=True)
    $ renpy.music.set_volume(.65,channel="music")
    call screen r13_effect_review_screen(r13_effect_review_mode)
    return
