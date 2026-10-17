# Bind only evaluated packets from an explicitly audited call site.
# No resource is enabled by this module; HOLD assets stay outside the registry.
default r13_dialogue_binding = None

init 169 python:
    R13_DIALOGUE_BINDINGS = json.load(renpy.file("assets/room13-dialogue-bindings.json"))

    def r13_bind_dialogue_rows(entries, identity, route, registry):
        """Snapshot evaluated branch output. Never cache by text or current day."""
        if route is None:
            return None
        spec=registry["routes"].get(route)
        result={"identity":identity,"route":route,"rows":{},"unresolved":[]}
        if spec is None:
            return result
        candidates=[registry["cues"][key] for key in spec["cues"]]
        sequence_cues=None
        if spec["group"]=="topics":
            for sequence in registry.get("sequences",[]):
                key=sequence["topic"]
                if identity not in ("topic:"+key,"topic:record_full:"+key,"topic:review:"+key,"material:accepted:"+key,"medkit:"+key):continue
                if [list(p[:2]) for p in entries]==sequence["packets"]:
                    sequence_cues=sequence["cues"]
                    break
        for index,packet in enumerate(entries):
            if len(packet)<2 or packet[0] in (None,"dad"):
                continue
            if len(packet)>2 and isinstance(packet[2],dict) and packet[2].get("thought"):
                continue
            matches=[]
            for cue in ([sequence_cues[str(index)]] if str(index) in (sequence_cues or {}) else [] if sequence_cues is not None else candidates):
                if cue["person"] not in (None,packet[0]):
                    continue
                if sequence_cues is None and cue.get("path") and cue["path"][0]=="with_daram":continue
                text=cue["text"]
                if spec["group"]=="debate":
                    text=text.replace("【", "").replace("】", "")
                if text!=packet[1]:
                    continue
                # Static topic records may only be reused for their actual topic.
                context=cue.get("context_identity")
                if context and context.startswith("topic:") and spec["group"]=="topics":
                    key=context[len("topic:"):]
                    if identity not in (context,"topic:review:"+key,"topic:record_full:"+key,"material:accepted:"+key,"medkit:"+key) and not identity.startswith(("b3:pages:","b3:buy:","w1c:karo:","negotiation:")):
                        continue
                matches.append(cue)
            # Conflicting decisions require a source/branch-specific correction.
            decisions={(c["emotion"],bool(c.get("reaction"))) for c in matches}
            if len(decisions)!=1:
                result["unresolved"].append({"index":index,"person":packet[0],"text":packet[1],"reason":"conflicting_context" if matches else "unreviewed_output"})
                continue
            emotion,reaction=next(iter(decisions))
            if identity.startswith(("topic:record_full:","topic:review:")):
                reaction=False
            result["rows"][str(index)]={"person":packet[0],"text":packet[1],"emotion":emotion,"reaction":reaction,"reviewed":True,"review_refs":sorted(set(c["review_ref"] for c in matches))}
        return result
