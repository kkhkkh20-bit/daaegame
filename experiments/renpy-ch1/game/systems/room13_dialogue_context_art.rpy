# Four approved expressions for exact spoken contexts; general six-slot art stays intact.
init 172 python:
    R13_DIALOGUE_CONTEXT_ART = json.load(renpy.file("assets/room13-dialogue-context-art.json"))

    def r13_dialogue_context_match(identity,index,packet,pose):
        if pose not in R13_FULLBODY_PLAIN or len(packet)<2:
            return None
        for cue in R13_DIALOGUE_CONTEXT_ART["bindings"]:
            if (cue["identity"],cue["index"],cue["person"],cue["text"]) == (identity,index,packet[0],packet[1]):
                return cue
        return None

    _r13_context_beat_begin = r13_dialogue_beat_begin
    def r13_dialogue_beat_begin(identity,index,packet,pose):
        _r13_context_beat_begin(identity,index,packet,pose)
        if getattr(store,"r13_meeting_active",False) or getattr(store,"r13_thought_active",False):
            return
        cue = r13_dialogue_context_match(identity,index,packet,pose)
        if not cue:return
        entry = R13_DIALOGUE_CONTEXT_ART["entries"][cue["key"]]
        if entry.get("status")!="approved_runtime":return
        if not all(renpy.loadable(entry["profiles"][str(h)]["frames"][cue["slot"]]["file"]) for h in (560,760,840)):
            return
        store.r13_dialogue_beat = dict(person=cue["person"],talk=cue["slot"],react=None,
            settled=True,duration=.35,context_key=cue["key"])

    _r13_context_beat_art = r13_dialogue_beat_art
    def r13_dialogue_beat_art(person,height):
        plan = getattr(store,"r13_dialogue_beat",None) or {}
        if plan.get("context_key") and plan.get("person")==person:
            entry = R13_DIALOGUE_CONTEXT_ART["entries"].get(plan["context_key"],{})
            profile = entry.get("profiles",{}).get(str(int(height)))
            if profile:return R13DialogueBeat(plan,profile)
        return _r13_context_beat_art(person,height)
