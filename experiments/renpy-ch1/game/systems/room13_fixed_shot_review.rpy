# Owner-requested visual comparison only. No production caller or story mutation.
default r13_shot_review_enabled = False
default r13_shot_review_mode = "1"
default r13_shot_review_manual_phase = None

init 194 python:
    class R13FixedShotReview(renpy.Displayable):
        def __init__(self,mode,**kwargs):
            super(R13FixedShotReview,self).__init__(**kwargs)
            self.mode=mode
            self.focuses=("resident_ppul","buri","seryeon")
            self.shots={}
            for who in self.focuses:
                shot=R13MeetingOrbit("C2",who,0,"listen",{})
                if who not in shot.people:raise ValueError("Review focus must have a real seat: "+who)
                shot.review_fixed_view=True
                self.shots[who]=shot
            statement=R13_DEBATE["C2"]["statements"][0]["text"].replace("【","").replace("】","")
            reply=R13_DIALOGUE_BEATS["lines"]["trial:C2:done"]["0"]["text"]
            self.dialogues=[]
            for who,text in (("resident_ppul",statement),("resident_ppul",statement),("seryeon",reply)):
                self.dialogues.append(Fixed(
                    Transform(R13InkPanel(),xpos=80,ypos=548,xsize=1120,ysize=150),
                    Text(R13_NAMES[who],xpos=108,ypos=565,size=24,color="#f5e6cb"),
                    Text(text,xpos=108,ypos=603,xmaximum=1060,size=23,color="#f5e6cb"),xysize=(1280,720)))
            # Keep the room visible behind two wood-framed crops of approved fixed shots.
            left=Transform(Crop((285,70,710,470),self.shots["resident_ppul"]),xsize=672,ysize=444)
            right=Transform(Crop((340,70,600,470),self.shots["seryeon"]),xsize=528,ysize=414)
            self.panel=Fixed(
                Transform(r13_meeting_plate("trial",False),matrixcolor=BrightnessMatrix(-.12)),
                Transform(R13InkPanel(),xpos=16,ypos=82,xsize=700,ysize=460),
                Transform(left,xpos=30,ypos=90),
                Transform(R13PaperFrame(),xpos=706,ypos=102,xsize=558,ysize=444),
                Transform(right,xpos=720,ypos=116),
                Transform(R13InkPanel(slim=True),xpos=40,ypos=98,xsize=186,ysize=38),
                Text(R13_NAMES["resident_ppul"],xpos=52,ypos=104,size=21,color="#f5e6cb"),
                Transform(R13InkPanel(slim=True),xpos=736,ypos=124,xsize=170,ysize=38),
                Text(R13_NAMES["seryeon"]+" · 반문",xpos=748,ypos=130,size=21,color="#f5e6cb"),
                xysize=(1280,720))
        def render(self,width,height,st,at):
            boundaries=(6.0,7.2,9.5,10.4)
            phase=sum(st>=t for t in boundaries)
            if store.r13_shot_review_manual_phase is not None:phase=store.r13_shot_review_manual_phase
            dialogue=0 if phase<2 else 2
            who="resident_ppul" if phase<2 else "seryeon"
            reaction=self.mode=="2" and phase in (1,3)
            if reaction:who="buri" if phase==1 else "resident_ppul"
            split=self.mode=="3" and phase in (2,3)
            scene=self.panel if split else self.shots[who]
            out=renpy.Render(1280,720)
            out.blit(renpy.render(scene,1280,720,st,at),(0,0))
            out.blit(renpy.render(self.dialogues[dialogue],1280,720,st,at),(0,0))
            titles={"1":"전체 화면 고정샷","2":"짧은 청자 반응 편집","3":"중요한 반문에만 2인 분할"}
            caption=(R13_NAMES[who]+" · 듣는 반응") if reaction else ("뿔이 · 발언" if dialogue==0 else "세련 · 반문")
            badge=Fixed(Transform(R13InkPanel(slim=True),xpos=24,ypos=20,xsize=1232,ysize=44),
                Text(self.mode+" · "+titles.get(self.mode,self.mode)+"   |   "+caption,
                    xpos=40,ypos=28,size=24,color="#f5e6cb"),xysize=(1280,720))
            out.blit(renpy.render(badge,1280,720,st,at),(0,0))
            if store.r13_shot_review_manual_phase is None and phase<4:renpy.redraw(self,max(.01,boundaries[phase]-st))
            return out
        def visit(self):return list(self.shots.values())+[self.panel]+self.dialogues

screen r13_shot_review_screen(mode):
    modal True
    zorder 300
    add R13FixedShotReview(mode)

label r13_shot_review:
    if not r13_shot_review_enabled:
        return
    $ renpy.music.stop(channel="ambience")
    $ renpy.music.play(R13_BGM["council"],channel="music",loop=True)
    $ renpy.music.set_volume(.65,channel="music")
    call screen r13_shot_review_screen(r13_shot_review_mode)
    return
