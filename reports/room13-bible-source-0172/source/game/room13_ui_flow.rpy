# Display-only helpers. No persistent discovery, story, evidence, or clock writes.
init 99 python:
    import re as r13_ui_re

    R13_SEMANTIC_DARK = {"person":"#ebcd8a", "place":"#a9ded4", "evidence":"#ffb3a3"}

    def r13_dialogue_profile(who):
        packet=getattr(store,"r13_packet",None)
        person=packet[0] if packet else None
        # Use the actual named speaker, not an inferred identity or a new crop.
        return person if who and person in CAST and R13_NAMES.get(person)==who else None

    def r13_known_terms():
        state=store.room13 or {}
        terms={}
        people=r13_met_people()
        packet=getattr(store,"r13_packet",None)
        if packet and packet[0] in R13_NAMES:people=people+[packet[0]]
        for person in people:
            name=R13_NAMES.get(person,"")
            if name:terms[name]="person"
        places={state.get("location")}
        places.update(e.get("place") for e in state.get("encounters",[]) if isinstance(e,dict))
        places.update(r.get("place") for r in state.get("records",{}).values())
        for place_id in places:
            name=R13_PLACES.get(place_id,("",))[0]
            if len(name)>=2:terms[name]="place"
        for key in state.get("evidence",[]):
            if key in ROOM13["evidence"]:
                for name in (ROOM13["evidence"][key]["name"],R13_RECORD_SHORT.get(key,"")):
                    if len(name)>=2:terms[name]="evidence"
        return terms

    def r13_semantic_text(text):
        if not isinstance(text,str) or not getattr(store,"room13_mode",False) or getattr(store,"r13_thought_active",False):return text
        terms=r13_known_terms()
        if not terms:return text
        # Longest complete names first. Korean particles are allowed only when
        # followed by a word boundary; e.g. 톡 never highlights 톡톡/톡방.
        boundary=r"(?=$|[^가-힣A-Za-z0-9_]|(?:은|는|이|가|을|를|의|에|에서|에게|께|와|과|도|만|으로|로|부터|까지)(?=$|[^가-힣A-Za-z0-9_]))"
        pattern=r13_ui_re.compile(r"(?<![가-힣A-Za-z0-9_])("+"|".join(r13_ui_re.escape(x) for x in sorted(terms,key=len,reverse=True))+")"+boundary)
        result=[]
        protected=[]
        for part in r13_ui_re.split(r"(\{[^{}]*\}|\[[^\[\]]*\])",text):
            if part.startswith("{"):
                tag=part[1:-1].split("=",1)[0]
                if tag in ("color","b","a"):protected.append(tag)
                elif tag.startswith("/") and tag[1:] in protected:protected.remove(tag[1:])
                result.append(part)
            elif part.startswith("[") or protected:
                result.append(part)
            else:
                result.append(pattern.sub(lambda m:"{color="+R13_SEMANTIC_DARK[terms[m.group(0)]]+"}{b}"+m.group(0)+"{/b}{/color}",part))
        return "".join(result)

    def r13_toggle_read_skip():
        store.r13_fast_read=not store.r13_fast_read
        renpy.stop_skipping()
        if store.r13_fast_read and getattr(store,"r13_read_id",None) in persistent.room13_read:
            renpy.config.skipping="slow"
        renpy.restart_interaction()

    def r13_stop_skip_at_choices():
        if not getattr(store,"room13_mode",False):return
        if any(renpy.get_screen(name) for name in ("choice","r13_topics","r13_entry_topics","r13_entry_karo_topics","r13_resident_approach","r13_book","r13_debate_board","r13_confirm")):
            renpy.stop_skipping()
    config.interact_callbacks.append(r13_stop_skip_at_choices)
