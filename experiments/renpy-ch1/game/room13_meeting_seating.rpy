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
default r13_meeting_previous_focus = None
default r13_meeting_previous_expression = "neutral"
default r13_meeting_pan_painted_revision = -1

init 99 python:
    import json as r13_meeting_json
    import functools as r13_meeting_functools
    R13_MEETING_SEATED=r13_meeting_json.load(renpy.file("assets/room13-meeting-seated.json")) if renpy.loadable("assets/room13-meeting-seated.json") else {}
    R13_MEETING_STANDING_FACING={"resident_bori":"right"}
    # Presentation metadata; never supplies a meeting's date, availability or proof.
    R13_MEETING_VENUES={
        "trial":("dining","round","식당 · 원탁 회의"),
        "ep4":("dining","round","식당 · 원탁 회의"),
        "ep1":("square","field","광장 · 현장 회의"),
        "ep2":("square","field","광장 · 현장 회의"),
        "ep6":("square","field","광장 · 현장 회의"),
        "ep3":("school","room","학교 · 실내 입석"),
        "ep5a":("school","room","학교 · 실내 입석"),
        "ep5":("school","room","학교 · 실내 입석"),
        "finale":("altar","stone","제단 · 돌판 회의"),
        "final":("altar","stone","제단 · 돌판 회의"),
    }
    def r13_meeting_kind(session):
        return R13_MEETING_VENUES.get(session,(None,"field",None))[1]

    def r13_meeting_map_venue(place):
        place="dining" if place=="inn" else place
        return next((v for v in R13_MEETING_VENUES.values() if v[0]==place),None)

    def r13_meeting_map_pending(place):
        s=store.room13 or {}
        # Only an offer that is already on screen may mark an active gathering.
        return any(k in ("r13_ep1_meeting","r13_wf_meeting") and
            o.get("location")==place and o.get("day")==s.get("day") and o.get("period")==s.get("period")
            for k,o in s.get("offers",{}).items())
    def r13_meeting_cast(claim,session,speaker=None):
        seats=list(r13_debate_seats(session));present={who for who,stance in seats}
        for who in (["granny","resident_seori"] if session=="trial" else ["mom"])+[st["who"] for st in r13_debate_statements(claim)]+[R13_DEBATE[claim]["chair"]]:
            if who in CAST and who!=((getattr(store,"room13",None) or {}).get("pov") or "dad") and who not in present:
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
        if who not in CAST or who==((getattr(store,"room13",None) or {}).get("pov") or "dad") or who==getattr(store,"r13_meeting_focus",None):return
        people=[p for p,stance in r13_meeting_cast(claim,r13_debate_session(claim))]
        old=getattr(store,"r13_meeting_focus",None)
        if who not in people:return
        a=people.index(old) if old in people else 0;b=people.index(who)
        step=(b-a)%len(people)
        store.r13_meeting_pan_direction=1 if step<=len(people)/2 else -1
        store.r13_meeting_previous_focus=old if old in people else None
        store.r13_meeting_previous_expression=r13_meeting_direct_pose(old,getattr(store,"dialogue_expression","neutral"))
        store.r13_meeting_focus=who;store.r13_meeting_shot_revision+=1
        store.r13_meeting_pan_started=renpy.display.core.get_time()

    def r13_meeting_pan_tick(trans,st,at,outgoing=False):
        if getattr(renpy,"predicting",lambda:False)():
            trans.xoffset=0;trans.alpha=0.0 if outgoing else 1.0
            return None
        now=renpy.display.core.get_time();revision=getattr(store,"r13_meeting_shot_revision",0)
        enabled=getattr(persistent,"room13_motion",True) and not renpy.is_skipping() and r13_meeting_direct_duration()>0
        if getattr(store,"r13_meeting_pan_painted_revision",-1)!=revision:
            # Start when the shot is painted, so image preparation cannot eat
            # the sweep before the first visible frame on slower devices.
            store.r13_meeting_pan_started=now if enabled else now-1
            store.r13_meeting_pan_painted_revision=revision
        elapsed=now-getattr(store,"r13_meeting_pan_started",0.0)
        duration=max(.01,r13_meeting_direct_duration())
        moving=enabled and getattr(store,"r13_meeting_previous_focus",None) is not None and 0<=elapsed<duration
        u=min(1.0,max(0.0,elapsed/duration));ease=u*u*(3-2*u)
        distance=getattr(store,"r13_meeting_pan_direction",1)*280
        trans.xoffset=int(-distance*ease if outgoing else distance*(1-ease)) if moving else 0
        trans.alpha=(1.0-ease if moving else 0.0) if outgoing else (ease if moving else 1.0)
        return .016 if moving else None

    def r13_meeting_edge(x,session):
        kind=r13_meeting_kind(session)
        if kind in ("field","room"):return 520
        return int((396 if kind=="round" else 432)+(88 if kind=="round" else 68)*((x-640)/640.0)**2)

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
        facing=spec.get("facing","") if seated else R13_MEETING_STANDING_FACING.get(who,spec.get("facing",""))
        art=Crop(tuple(spec["crop"]),spec["file"])
        flip=(is_left and facing.startswith("left")) or (not is_left and facing.startswith("right"))
        return Transform(art,xzoom=-1) if flip else art

    def r13_meeting_next_statement(claim,current,person=None,step=1):
        ids=[st["id"] for st in r13_debate_statements(claim) if r13_debate_visible(claim,st) and (person is None or st["who"]==person)]
        return ids[(ids.index(current)+step)%len(ids)] if current in ids else ids[0] if ids else current

    def r13_meeting_standing_slot(who,count,edge,session="finale"):
        crop=CAST[who]["neutral"]["crop"]
        width=min(int(crop[2]*306.0/crop[3]),int(1160.0/max(1,count)*.90))
        height=int(round(width*crop[3]/float(crop[2])))
        return width,height,int(edge-height*(1.0 if r13_meeting_kind(session) in ("field","room") else .60))

    def r13_meeting_plate(session,close=False):
        if r13_meeting_kind(session) in ("field","room"):
            place=R13_EP_MEETING_PLACE.get(session,"winter_square")
            return Transform(r13_background(place),xysize=(1280,720),nearest=True)
        if r13_meeting_kind(session)=="stone":return Transform("assets/room13-pixel-meeting-altar-standing072.webp",xysize=(1280,720),nearest=True)
        path="assets/room13-pixel-meeting-interview066.webp" if close else "assets/room13-pixel-meeting-room056.webp"
        plate=Transform(path,xysize=(1280,720),nearest=True)
        if close:return plate
        return Crop((160,0,1280,720),Transform(plate,zoom=1.25,nearest=True)) if close else plate

    class R13MeetingForeground(renpy.Displayable):
        def __init__(self,session,close=False,**kwargs):super(R13MeetingForeground,self).__init__(**kwargs);self.session=session;self.close=close
        def render(self,width,height,st,at):
            out=renpy.Render(1280,720);c=out.canvas()
            if r13_meeting_kind(self.session)=="stone":
                edge=[(x,r13_meeting_edge(x,self.session)) for x in range(0,1281,16)]
            elif self.close:
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

transform r13_meeting_background_light(shade=0.0,tint="#fff6e8"):
    linear (.18 if persistent.room13_motion else 0) matrixcolor (TintMatrix(tint)*SaturationMatrix(.91)*BrightnessMatrix(-.04-shade))

transform r13_meeting_pan(revision=0,direction=1,outgoing=False):
    subpixel False
    crop (0,0,1280,720)
    function r13_meeting_functools.partial(r13_meeting_pan_tick,outgoing=outgoing)

screen r13_meeting_stage(claim,focus=None,close=False,ready=False,selected=None,ballot=False):
    $ session=r13_debate_session(claim)
    if close:
        add R13MeetingOrbit(claim,focus,r13_meeting_shot_revision,(r13_meeting_direction or {}).get("beat","listen"),r13_meeting_direction_poses)
    else:
        add r13_meeting_plate(session,False)
        use r13_meeting_camera_frame(claim,focus,False,ready,selected,ballot)

screen r13_meeting_camera_frame(claim,focus=None,close=False,ready=False,selected=None,ballot=False,outgoing=False):
    $ session=r13_debate_session(claim)
    $ venue_kind=r13_meeting_kind(session)
    $ seated=venue_kind=="round"
    $ seats=r13_meeting_cast(claim,session)
    fixed:
        id "meeting_camera"
        xsize 1280 ysize 720
        if close:
            at r13_meeting_pan(r13_meeting_shot_revision,r13_meeting_pan_direction,outgoing)
        add r13_meeting_plate(session,close) at r13_meeting_background_light(r13_meeting_direct_shade(),"#eef4ff" if venue_kind=="stone" else "#fff6e8" if seated else "#f3f6ff")
        if close:
            $ left,right=r13_meeting_neighbors(claim,focus)
            for neighbor,is_left in ((left,True),(right,False)):
                $ sitting=seated and neighbor in R13_MEETING_SEATED
                $ side_crop=(R13_MEETING_SEATED[neighbor] if sitting else CAST[neighbor]["neutral"])["crop"]
                $ side_scale=min((950.0 if sitting else 660.0)/side_crop[3],(520.0 if sitting else 440.0)/side_crop[2])
                $ side_width=int(round(side_crop[2]*side_scale))
                $ side_height=int(round(side_crop[3]*side_scale))
                $ side_profile=r13_dialogue_source_profile(neighbor,"neutral",950 if sitting else 660)
                if side_profile:
                    $ side_art=r13_fullbody_close_art(neighbor,"neutral",950 if sitting else 660)
                    $ side_width,side_height=side_profile["canvas"]
                else:
                    $ side_art=r13_pixel_scale(r13_meeting_neighbor_art(neighbor,is_left,sitting),side_width,side_height,R13_CLOSE_PIXEL_GRID)
                $ side_x=-side_width//3 if is_left else 1280-side_width*2//3
                add Transform(side_art,nearest=not bool(side_profile),matrixcolor=BrightnessMatrix(-.08-r13_meeting_direct_shade()*.4)*SaturationMatrix(.90)) xpos side_x ypos (142 if sitting else 164)
            # Reuse front-facing interview expressions and their stable torso centre.
            $ pose=r13_meeting_previous_expression if outgoing else (getattr(store,"dialogue_expression","neutral") if getattr(store,"dialogue_speaker",None)==focus else "neutral")
            $ pose=r13_meeting_previous_expression if outgoing else r13_meeting_direct_pose(focus,pose)
            $ close_height=r13_meeting_direct_close_height(venue_kind,outgoing)
            $ portrait=r13_fullbody_close_art(focus,pose,close_height)
            if portrait is not None:
                add portrait xcenter r13_close_x(focus,pose,close_height) ypos r13_fullbody_close_y(focus,close_height,96,pose)
            else:
                add Transform(r13_meeting_actor(focus,focus,640),ysize=840,fit="contain",nearest=True) xcenter 640 ypos 108
        else:
            for index,(who,stance) in enumerate(seats):
                $ cx,edge=r13_meeting_seat_position(index,len(seats),session)
                if seated:
                    $ height=230
                    $ top=edge+95-height
                    add Transform(r13_meeting_actor(who,focus,cx,seated=True),ysize=height,fit="contain",nearest=True) xcenter cx ypos top
                else:
                    $ stand_width,height,top=r13_meeting_standing_slot(who,len(seats),edge,session)
                    add r13_pixel_scale(r13_meeting_actor(who,focus,cx),stand_width,height,R13_CLOSE_PIXEL_GRID) xcenter cx ypos top
                $ own=[st for st in r13_debate_statements(claim) if st["who"]==who and r13_debate_visible(claim,st)]
                button:
                    area (cx-56,top-28,112,84) padding (0,0) background None hover_background None
                    action Return(("select",r13_meeting_next_statement(claim,selected,who)))
                    sensitive ready and bool(own) and not ballot
                    frame:
                        xsize 112 ysize 24 padding (3,2) background R13InkPanel(focused=who==focus)
                        text R13_NAMES[who] size r13_read_size(14,16) color ("#efd191" if who==focus else "#efe0c3") xalign .5 yalign .5
        # Outdoor/classroom plates contain no table. Masking them hides legs
        # behind an invisible tabletop and paints background over the cast.
        if venue_kind in ("round","stone"):
            add Transform(AlphaMask(r13_meeting_plate(session,close),R13MeetingForeground(session,close)),matrixcolor=BrightnessMatrix(-.025-r13_meeting_direct_shade()*.4))
        if ballot:
            for index,(who,stance) in enumerate(seats):
                if stance is not None:
                    $ cx,edge=r13_meeting_seat_position(index,len(seats),session)
                    frame:
                        xpos cx-56 ypos min(edge+8,442) xsize 112 ysize 40 padding (4,4) background R13PaperPanel()
                        text R13_DEBATE_STANCE[session][stance] size 14 color "#493b30" text_align .5 xalign .5 yalign .5

screen r13_meeting_chrome(claim):
    $ session=r13_debate_session(claim)
    $ proved,proof_total=r13_debate_progress(claim)
    frame:
        area (24,18,900,66) padding (16,8) background R13PaperFrame()
        add R13AntiqueIcon("meeting_"+r13_meeting_kind(session),size=30) xpos 0 ypos 8
        vbox:
            xpos 42
            spacing 2
            text (r13_meeting_header(session)+("" if r13_meeting_intro else "  ·  반박 %d / %d"%(proved,proof_total))) size r13_read_size(15,17) color "#795d40"
            text ("참석자들의 이야기" if r13_meeting_intro else "쟁점 · "+R13_MEETING_ISSUES.get(claim,R13_DEBATE[claim]["title"])) size r13_read_size(21,25) color "#493b30"
        if not r13_meeting_intro:
            add Solid("#d6bf98") xpos 0 ypos 51 xysize (868,3)
            if proved:
                add Solid("#a88043") xpos 0 ypos 51 xysize (int(868*proved/max(1,proof_total)),3)

screen r13_meeting_tools(claim,sid=None,board=False,ready=True):
    $ completed=bool(sid and r13_debate_is_broken(claim,sid))
    $ live_controls=r13_meeting_live_active and not r13_meeting_interrupting
    hbox:
        xpos 80 ypos 646 spacing 12
        textbutton ("다시 듣기" if completed else "되묻기"):
            style "r13_action_button" xsize 188 ysize 64 text_size 24
            action (Return(("listen" if completed else "press",sid)) if board else Function(r13_meeting_request_live_action,"press"))
            sensitive ready and (board or (live_controls and r13_meeting_can_live_press()))
        textbutton "보여주기":
            style "r13_action_button" xsize 188 ysize 64 text_size 24
            action (Return(("present",sid)) if board else Function(renpy.call_in_new_context,"r13_meeting_interrupt",claim,r13_meeting_live_target()))
            sensitive ready and not completed and (board or r13_meeting_can_interrupt())
    if board:
        if r13_debate_ready(claim):
            text "결론을 말할 수 있다" xpos 496 ypos 668 size r13_read_size(19,22) color "#f1dfba" outlines [(1,"#30251e",0,0)]
        else:
            textbutton "토론 듣기":
                style "r13_action_button" xpos 496 ypos 646 xsize 224 ysize 64 text_size 23
                action Return(("round",sid)) sensitive ready
        textbutton "결론을 말한다":
            style "r13_action_button" xpos 952 ypos 646 xsize 248 ysize 64 text_size 24
            action Return(("conclude",)) sensitive ready and r13_debate_ready(claim)
    else:
        if live_controls:
            $ live_ids=r13_meeting_live_ids(claim,r13_meeting_live_sid)
            $ visible_ids=[st["id"] for st in r13_debate_statements(claim) if r13_debate_visible(claim,st)]
            frame:
                area (942,18,314,64) padding (12,8) background R13PaperFrame()
                text ("발언 %d / %d · %s"%(visible_ids.index(r13_meeting_live_sid)+1,len(visible_ids),"새 발언" if r13_debate_statement(claim,r13_meeting_live_sid).get("hidden") and not r13_meeting_heard(claim,r13_meeting_live_sid) else "반복 듣기" if r13_meeting_live_lap else "토론 중")) align (.5,.5) size r13_read_size(20,23) color "#493b30"
            hbox:
                xpos 736 ypos 646 spacing 12
                textbutton "‹":
                    style "r13_action_button" xsize 72 ysize 64 text_size 32 alt "이전 발언"
                    action Function(r13_meeting_request_live_action,"previous") sensitive ready and len(live_ids)>1
                textbutton "›":
                    style "r13_action_button" xsize 72 ysize 64 text_size 32 alt "다음 발언"
                    action Function(r13_meeting_request_live_action,"next") sensitive ready and len(live_ids)>1
            if ready and len(live_ids)>1:
                key "K_LEFT" action Function(r13_meeting_request_live_action,"previous")
                key "K_RIGHT" action Function(r13_meeting_request_live_action,"next")
            textbutton "발언 고르기":
                style "r13_action_button" xpos 496 ypos 646 xsize 224 ysize 64 text_size 23
                action Function(r13_meeting_request_live_action,"review") sensitive ready
            # 0.18.88: after a full lap, say what to do next (players kept clicking through the loop).
            if r13_meeting_live_lap>=1:
                frame:
                    area (160,440,960,44) padding (14,7) background R13PaperPanel()
                    text "이상한 말엔 「보여주기」, 하나씩 따지려면 「발언 고르기」" size r13_read_size(20,23) color "#493b30" xalign .5
        textbutton "백로그":
            style "r13_action_button" xpos 952 ypos 646 xsize 120 ysize 64 text_size 21 action Show("r13_backlog")
        textbutton "더보기":
            style "r13_action_button" xpos 1080 ypos 646 xsize 120 ysize 64 text_size 21 action Show("r13_more_tools")

screen r13_meeting_rebuttal_hold(claim):
    zorder 35
    use r13_meeting_stage(claim,r13_meeting_focus_person(claim),True)
    use r13_meeting_chrome(claim)

transform r13_meeting_cut_in_fade:
    alpha 0.0
    linear .07 alpha 1.0
    pause .22
    linear .09 alpha 0.0

screen r13_meeting_cut_in(caption):
    zorder 140
    frame:
        area (432,430,416,48) padding (12,6) background R13PaperFrame()
        if persistent.room13_motion:
            at r13_meeting_cut_in_fade
        text caption size 26 color "#8b4932" xalign .5 yalign .5
    timer .38 action Hide("r13_meeting_cut_in")

screen r13_meeting_choices(items,ready):
    use r13_meeting_stage(r13_meeting_claim,r13_meeting_focus_person(r13_meeting_claim),True)
    use r13_meeting_chrome(r13_meeting_claim)
    $ caption=" ".join(item.caption for item in items if item.action is None)
    if caption:
        frame:
            area (160,402,960,42) padding (14,7) background R13PaperPanel()
            text caption size r13_read_size(20,24) color "#493b30"
    $ choices=[item for item in items if item.action is not None]
    # Four suspects plus cancel must fit above the dialogue tools on mobile too.
    for index,item in enumerate(choices):
        $ columns=2 if len(choices)>3 else 1
        $ who=next((p for p,name in R13_NAMES.items() if name==item.caption and p!="dad"),None)
        button:
            style "r13_action_button"
            xpos 160+(index%columns)*486 ypos 452+(index//columns)*74
            xsize (474 if columns==2 else 960) ysize 64
            action r13_safe_question_action(item.action) sensitive ready
            hbox:
                align (.5,.5) spacing 14
                if who and columns==2:
                    add Transform(r13_art(who,"avatar_neutral"),xysize=(48,48),fit="contain",nearest=r13_profile_nearest(who)) yalign .5
                text (str(index+1)+"  "+item.caption) size r13_read_size(23,27) color "#fff0ce" yalign .5
        if index<9 and ready:
            key ("K_%d"%(index+1)) action r13_safe_question_action(item.action)
