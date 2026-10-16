# Stable round-table stage. UI state never changes proof or clock rules.
default r13_meeting_scrolls = {}
default r13_meeting_active = False
default r13_meeting_claim = None
default r13_meeting_intro = False
default r13_meeting_focus = None
default r13_meeting_shot_revision = 0
default r13_meeting_pan_direction = 1
default r13_meeting_pan_started = 0.0
default r13_meeting_interrupting = False
default r13_meeting_replaying = False
default r13_meeting_opinion_baseline = {}
default r13_meeting_findings = {}
default r13_meeting_feedback = None

init 99 python:
    import json as r13_meeting_json
    R13_MEETING_SEATED=r13_meeting_json.load(renpy.file("assets/room13-meeting-seated.json")) if renpy.loadable("assets/room13-meeting-seated.json") else {}
    def r13_meeting_cast(claim,session,speaker=None):
        seats=list(r13_debate_seats(session));present={who for who,stance in seats}
        for who in (["granny","resident_seori"] if session=="trial" else ["mom"])+[st["who"] for st in r13_debate_statements(claim)]+[R13_DEBATE[claim]["chair"]]:
            if who in CAST and who!="dad" and who not in present:
                seats.append((who,None));present.add(who)
        return seats

    def r13_meeting_focus_person(claim):
        people=[p for p,stance in r13_meeting_cast(claim,r13_debate_session(claim))]
        focused=getattr(store,"r13_meeting_focus",None)
        return focused if focused in people else r13_debate_statements(claim)[0]["who"]

    def r13_meeting_neighbors(claim,person):
        people=[p for p,stance in r13_meeting_cast(claim,r13_debate_session(claim))]
        index=people.index(person) if person in people else 0
        return people[index-1],people[(index+1)%len(people)]

    def r13_meeting_focus_change(claim,who):
        if who not in CAST or who=="dad" or who==getattr(store,"r13_meeting_focus",None):return
        people=[p for p,stance in r13_meeting_cast(claim,r13_debate_session(claim))]
        old=getattr(store,"r13_meeting_focus",None)
        if who not in people:return
        a=people.index(old) if old in people else 0;b=people.index(who)
        step=(b-a)%len(people)
        store.r13_meeting_pan_direction=1 if step<=len(people)/2 else -1
        store.r13_meeting_focus=who;store.r13_meeting_shot_revision+=1
        store.r13_meeting_pan_started=renpy.display.core.get_time()

    def r13_meeting_pan_tick(trans,st,at):
        elapsed=renpy.display.core.get_time()-getattr(store,"r13_meeting_pan_started",0.0)
        moving=getattr(persistent,"room13_motion",True) and not renpy.is_skipping() and 0<=elapsed<.24
        trans.xoffset=int(getattr(store,"r13_meeting_pan_direction",1)*64*(1-elapsed/.24)**2) if moving else 0
        return .016 if moving else None

    def r13_meeting_edge(x,session):
        return int((396 if session=="trial" else 474)+(88 if session=="trial" else 110)*((x-640)/640.0)**2)

    def r13_meeting_seat_position(index,count,session="trial"):
        x=int(60+(index+.5)*1160/max(1,count))
        return x,r13_meeting_edge(x,session)

    def r13_meeting_actor(who,focus,cx,seated=False):
        if seated and who in R13_MEETING_SEATED:
            spec=R13_MEETING_SEATED[who]
            art=Crop(tuple(spec["crop"]),spec["file"])
            return Transform(art,xzoom=-1) if cx>640 else art
        pose=getattr(store,"dialogue_expression","neutral") if who==focus and getattr(store,"r13_meeting_active",False) else "neutral"
        spec=CAST[who].get(pose) or CAST[who]["neutral"]
        art=Crop(tuple(spec["crop"]),spec["file"])
        flip=(cx<640 and spec.get("facing")=="left") or (cx>640 and spec.get("facing")=="right")
        return Transform(art,xzoom=-1) if flip else art

    def r13_meeting_neighbor_art(who,is_left,seated=False):
        # Side seats face into the circle rather than towards the viewer.
        spec=R13_MEETING_SEATED.get(who) if seated else None
        spec=spec or CAST[who]["neutral"]
        facing=spec.get("facing","")
        art=Crop(tuple(spec["crop"]),spec["file"])
        flip=(is_left and facing.startswith("left")) or (not is_left and facing.startswith("right"))
        return Transform(art,xzoom=-1) if flip else art

    def r13_meeting_next_statement(claim,current,person=None,step=1):
        ids=[st["id"] for st in r13_debate_statements(claim) if r13_debate_visible(claim,st) and (person is None or st["who"]==person)]
        return ids[(ids.index(current)+step)%len(ids)] if current in ids else ids[0] if ids else current

    def r13_meeting_plate(session,close=False):
        path="assets/room13-pixel-meeting-interview066.webp" if close and session=="trial" else "assets/room13-pixel-meeting-%s056.webp"%("room" if session=="trial" else "altar")
        plate=Transform(path,xysize=(1280,720),nearest=True)
        if close and session=="trial":return plate
        return Crop((160,0,1280,720),Transform(plate,zoom=1.25,nearest=True)) if close else plate

    class R13MeetingForeground(renpy.Displayable):
        def __init__(self,session,close=False,**kwargs):super(R13MeetingForeground,self).__init__(**kwargs);self.session=session;self.close=close
        def render(self,width,height,st,at):
            out=renpy.Render(1280,720);c=out.canvas()
            if self.close and self.session=="trial":
                edge=[(x,int(396+98*((x-640)/640.0)**2)) for x in range(0,1281,32)]
            else:
                edge=[(x,int(r13_meeting_edge((x+160)/1.25,self.session)*1.25) if self.close else r13_meeting_edge(x,self.session)) for x in range(0,1281,32)]
            c.polygon("#ffffff",edge+[(1280,720),(0,720)])
            return out

    class R13MeetingScrollChanged:
        def __init__(self,claim):self.claim=claim
        def __call__(self,value):
            value=max(0,int(value));offsets=dict(getattr(store,"r13_meeting_scrolls",{}))
            if offsets.get(self.claim)!=value:
                offsets[self.claim]=value;store.r13_meeting_scrolls=offsets;renpy.retain_after_load()

    def r13_meeting_adjustment(claim):
        return ui.adjustment(value=getattr(store,"r13_meeting_scrolls",{}).get(claim,0),changed=R13MeetingScrollChanged(claim))

transform r13_meeting_pan(revision=0,direction=1):
    subpixel False
    function r13_meeting_pan_tick

screen r13_meeting_stage(claim,focus=None,close=False,ready=False,selected=None,ballot=False):
    $ session=r13_debate_session(claim)
    $ seats=r13_meeting_cast(claim,session)
    add r13_meeting_plate(session,close)
    fixed:
        id "meeting_camera"
        xsize 1280 ysize 720
        if close:
            at r13_meeting_pan(r13_meeting_shot_revision,r13_meeting_pan_direction)
        add r13_meeting_plate(session,close)
        if close:
            $ left,right=r13_meeting_neighbors(claim,focus)
            for neighbor,is_left in ((left,True),(right,False)):
                $ sitting=session=="trial" and neighbor in R13_MEETING_SEATED
                $ side_crop=(R13_MEETING_SEATED[neighbor] if sitting else CAST[neighbor]["neutral"])["crop"]
                $ side_scale=min((950.0 if sitting else 660.0)/side_crop[3],(520.0 if sitting else 440.0)/side_crop[2])
                $ side_width=int(round(side_crop[2]*side_scale))
                $ side_height=int(round(side_crop[3]*side_scale))
                $ side_x=-side_width//3 if is_left else 1280-side_width*2//3
                add r13_pixel_scale(r13_meeting_neighbor_art(neighbor,is_left,sitting),side_width,side_height,R13_CLOSE_PIXEL_GRID) xpos side_x ypos (142 if sitting else 164)
            # Reuse front-facing interview expressions and their stable torso centre.
            $ pose=getattr(store,"dialogue_expression","neutral") if getattr(store,"dialogue_speaker",None)==focus else "neutral"
            $ portrait=r13_fullbody_close_art(focus,pose,840)
            if portrait is not None:
                add portrait xcenter r13_close_x(focus,pose,840) ypos r13_fullbody_close_y(focus,840,96,pose)
            else:
                add Transform(r13_meeting_actor(focus,focus,640),ysize=840,fit="contain",nearest=True) xcenter 640 ypos 108
        else:
            for index,(who,stance) in enumerate(seats):
                $ cx,edge=r13_meeting_seat_position(index,len(seats),session)
                $ height=230 if session=="trial" else 246
                $ top=edge+(95 if session=="trial" else 24)-height
                add Transform(r13_meeting_actor(who,focus,cx,seated=session=="trial"),ysize=height,fit="contain",nearest=True) xcenter cx ypos top
                $ own=[st for st in r13_debate_statements(claim) if st["who"]==who and r13_debate_visible(claim,st)]
                button:
                    area (cx-56,top-28,112,84) padding (0,0) background None hover_background None
                    action Return(("select",r13_meeting_next_statement(claim,selected,who)))
                    sensitive ready and bool(own) and not ballot
                    frame:
                        xsize 112 ysize 24 padding (3,2) background R13InkPanel(focused=who==focus)
                        text R13_NAMES[who] size r13_read_size(14,16) color ("#efd191" if who==focus else "#efe0c3") xalign .5 yalign .5
        add AlphaMask(r13_meeting_plate(session,close),R13MeetingForeground(session,close))
        if ballot:
            for index,(who,stance) in enumerate(seats):
                if stance is not None:
                    $ cx,edge=r13_meeting_seat_position(index,len(seats),session)
                    frame:
                        xpos cx-56 ypos min(edge+8,442) xsize 112 ysize 40 padding (4,4) background R13PaperPanel()
                        text R13_DEBATE_STANCE[session][stance] size 14 color "#493b30" text_align .5 xalign .5 yalign .5

screen r13_meeting_chrome(claim):
    $ session=r13_debate_session(claim)
    frame:
        area (24,18,900,66) padding (16,8) background R13PaperFrame()
        vbox:
            spacing 2
            text ("식당 회의 · 7일째" if session=="trial" else "제단 앞 회의 · 14일째") size r13_read_size(15,17) color "#795d40"
            text ("참석자들의 이야기" if r13_meeting_intro else "쟁점 · "+R13_MEETING_ISSUES.get(claim,R13_DEBATE[claim]["title"])) size r13_read_size(21,25) color "#493b30"

screen r13_meeting_tools(claim,sid=None,board=False,ready=True):
    $ completed=bool(sid and r13_debate_is_broken(claim,sid))
    hbox:
        xpos 80 ypos 646 spacing 12
        textbutton ("다시 듣기" if completed else "되묻기"):
            style "r13_action_button" xsize 188 ysize 64 text_size 24
            action Return(("listen" if completed else "press",sid)) sensitive ready and board
        textbutton "보여주기":
            style "r13_action_button" xsize 188 ysize 64 text_size 24
            action (Return(("present",sid)) if board else Function(renpy.call_in_new_context,"r13_meeting_interrupt",claim,r13_meeting_live_target()))
            sensitive ready and not completed and (board or r13_meeting_can_interrupt())
    if board:
        text ("결론을 말할 수 있다" if r13_debate_ready(claim) else "아직 살펴볼 말이 있다") xpos 496 ypos 668 size r13_read_size(19,22) color "#f1dfba" outlines [(1,"#30251e",0,0)]
        textbutton "결론을 말한다":
            style "r13_action_button" xpos 952 ypos 646 xsize 248 ysize 64 text_size 24
            action Return(("conclude",)) sensitive ready and r13_debate_ready(claim)
    else:
        textbutton "백로그":
            style "r13_action_button" xpos 952 ypos 646 xsize 120 ysize 64 text_size 21 action Show("r13_backlog")
        textbutton "더보기":
            style "r13_action_button" xpos 1080 ypos 646 xsize 120 ysize 64 text_size 21 action Show("r13_more_tools")

screen r13_meeting_rebuttal_hold(claim):
    zorder 35
    use r13_meeting_stage(claim,r13_meeting_focus_person(claim),True)
    use r13_meeting_chrome(claim)

screen r13_meeting_choices(items,ready):
    use r13_meeting_stage(r13_meeting_claim,r13_meeting_focus_person(r13_meeting_claim),True)
    use r13_meeting_chrome(r13_meeting_claim)
    $ caption=" ".join(item.caption for item in items if item.action is None)
    if caption:
        frame:
            area (160,402,960,42) padding (14,7) background R13PaperPanel()
            text caption size r13_read_size(20,24) color "#493b30"
    vbox:
        xpos 160 ypos 452 spacing 10
        for index,item in enumerate([item for item in items if item.action is not None]):
            textbutton (str(index+1)+"  "+item.caption):
                style "r13_action_button" xsize 960 ysize 64 text_size r13_read_size(23,27)
                action r13_safe_question_action(item.action) sensitive ready
            if index<9 and ready:
                key ("K_%d"%(index+1)) action r13_safe_question_action(item.action)
