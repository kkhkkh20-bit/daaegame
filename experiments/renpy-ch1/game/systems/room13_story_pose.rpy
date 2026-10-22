# 0.20.7 (owner suggestion 1: "현장 화면의 다람도 방금 있었던 일을 기억하기"). Outside dialogue the
# field figure in room 13 follows the first day's story instead of the fixed reading pose: she
# looks around the empty room, then sits with the family drawing spread out, and at night sits by
# the folded snack bag. Existing poses and the room's own home positions only.
init 50 python:
    # Room 13 floor in front of the bed, inside the opening view (the home stage's own coordinates).
    R13_DARAM_STORY_SPOTS={"inspect_floor":(700,555,195),"action_2":(715,565,210)}
    # The wide room's contact layer (systems/room13_spatial_contacts.rpy) places the figure last;
    # same tuple shape as R13_HOME_CONTACTS: (anchor, x, y, height, depth).
    R13_DARAM_STORY_CONTACTS={"inspect_floor":("foot",920,560,189,560),"action_2":("foot",940,570,253,570)}
    def r13_stage_story_key():
        state=getattr(store,"room13",None) or {}
        v=state.get("v111") or {}
        return (v.get("scene"),v.get("gate"),tuple(sorted(k for k in state.get("evidence",[]) if k in ("V111:E06","V111:E30"))))

    def r13_daram_story_activity(state):
        """(pose, activity) for Daram at home on the new story's first day, or None."""
        if not state.get("v111") or state.get("day")!=1:return None
        if min(state.get("period",0),2)>=2:return ("action_2","과자 봉지 곁에서 그림을 그리며 기다리는 중")
        if "V111:E30" in state.get("evidence",[]):return ("action_2","가족 그림을 따라 그리는 중")
        return ("inspect_floor","빈방을 둘러보는 중")

init 182 python:
    # After the home contact layer (systems/room13_spatial_contacts.rpy, init 179, pinned source):
    # on the first day the figure stands/sits in front of the bed, inside the opening view.
    _r13_story_pose_stage=r13_stage_people
    def r13_stage_people(entry=False):
        actors=_r13_story_pose_stage(entry)
        state=store.room13 or {}
        if state.get("location")!="room13" or not r13_daram_story_activity(state):return actors
        out=[]
        for actor in actors:
            if actor.get("person")=="daram" and actor.get("pose") in R13_DARAM_STORY_CONTACTS:
                anchor,x,y,height,depth=R13_DARAM_STORY_CONTACTS[actor["pose"]]
                actor=r13_contact_geometry(actor,actor["pose"],anchor,(x,y),height,depth)
            out.append(actor)
        return sorted(out,key=lambda a:a.get("depth",0))
