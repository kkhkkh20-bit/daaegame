def r13_meeting_motion_profile(beat,steps=1):
    extra=max(0,abs(steps)-1)
    if beat=="interrupt":return 0.0,min(.30,.18+extra*.035)
    if beat in ("gasp","reversal"):return .08,min(.48,.32+extra*.045)
    if beat in ("cornered","resolve"):return .05,min(.44,.30+extra*.04)
    if beat in ("press","reaction","explain"):return 0.0,min(.40,.26+extra*.04)
    return 0.0,min(.48,.32+extra*.045)

def r13_meeting_motion_ease(u):
    # Brief acceleration followed by a longer, smooth deceleration to rest.
    u=max(0.0,min(1.0,u));a=.18;area=a/2+(1-a)/3
    if u<a:return u*u/(2*a*area)
    v=(u-a)/(1-a)
    return (a/2+(1-a)*(v-v*v+v*v*v/3))/area

def r13_meeting_world_view(claim,focus):
    people=[p for p,_ in r13_meeting_cast(claim,r13_debate_session(claim))]
    target=people.index(focus) if focus in people else 0
    old=getattr(store,"r13_meeting_previous_focus",None)
    if old not in people:return float(target),False
    start=people.index(old);delta=(target-start)%len(people)
    if delta>len(people)/2.0:delta-=len(people)
    enabled=persistent.room13_motion and not renpy.is_skipping()
    if not enabled or not delta:return float(start+delta),False
    revision=getattr(store,"r13_meeting_shot_revision",0)
    now=renpy.display.core.get_time()
    if getattr(store,"r13_meeting_pan_painted_revision",-1)!=revision:
        store.r13_meeting_pan_painted_revision=revision
        store.r13_meeting_pan_started=now
        beat=(getattr(store,"r13_meeting_direction",{}) or {}).get("beat","listen")
        store.r13_meeting_pan_profile=r13_meeting_motion_profile(beat,delta)
    hold,duration=getattr(store,"r13_meeting_pan_profile",r13_meeting_motion_profile("listen",delta))
    elapsed=max(0.0,now-store.r13_meeting_pan_started)
    u=min(1.0,max(0.0,(elapsed-hold)/duration))
    return start+delta*r13_meeting_motion_ease(u),elapsed<hold+duration

