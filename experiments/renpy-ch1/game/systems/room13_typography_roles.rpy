# Name / speech / thought / item typography (owner's typography handoff, 0.18.24).
#   Spec: assets/room13-typography-tokens.json (TYPOGRAPHY_HANDOFF.md).
#   - Roles, not people, pick colours: speech cream, Dad's thought blue with its parentheses
#     exactly once, narration grey. One speaker-label colour for everyone.
#   - Item names are marked by the author with 「…」; only that span takes the entity colour.
#     The old automatic name/place/evidence regex and its fake {b} are retired.
#   - Use the approved Pretendard Regular: no synthetic bold or italic.
#   - Dark windows and light paper use different colours for the same role.
#   - Warm paper for records and compact HUD labels; translucent ink-brown for speech/actions (solid in explicit dark mode).
#     Shared code-drawn materials live in room13_ui_art.rpy; semantic roles stay independent.
# The typing click already counts rendered glyphs (R13DialogueText), never tag characters.
init 140 python:
    import json as _r13_tj, re as _r13_tre
    R13_TYPE=_r13_tj.load(renpy.file("assets/room13-typography-tokens.json")) if renpy.loadable("assets/room13-typography-tokens.json") else {}

    def r13_role_color(role,surface="dark"):
        return R13_TYPE.get("roles",{}).get(role,{}).get(surface,"#F4E7C4")

    R13_SPEAKER_COLOR=R13_TYPE.get("speaker_color","#F6DFAC")
    # Shared colour tokens used across the existing screens: point them at the roles.
    R13_UI_COLORS.update(
        dark_text=r13_role_color("speech"), dark_secondary=r13_role_color("metadata"),
        menu_secondary=r13_role_color("metadata"), menu_disabled=r13_role_color("subdued"),
        person=r13_role_color("entity"), thought=r13_role_color("thought"),
        paper_text=r13_role_color("speech","paper"), paper_secondary=r13_role_color("metadata","paper"),
        evidence=r13_role_color("entity","paper"), testimony=r13_role_color("thought","paper"))

    def r13_say_color():
        """What colour the current line uses: thought, narration or speech."""
        surface="paper" if getattr(store,"r13_meeting_active",False) else "dark"
        if getattr(store,"r13_thought_active",False):return r13_role_color("thought",surface)
        packet=getattr(store,"r13_packet",None)
        if packet and packet[0] is None:return r13_role_color("narration",surface)
        return r13_role_color("speech",surface)

    _R13_ITEM_SPAN=_r13_tre.compile(r"「[^「」{}\[\]]{1,16}」")  # names only; long quoted letters stay body text

    def r13_semantic_text(text):
        """Display-only. Thought: parentheses exactly once, one colour. Otherwise: only authored
        「item」 spans take the entity colour. No automatic names, no bold."""
        if not isinstance(text,str) or not getattr(store,"room13_mode",False):return text
        if getattr(store,"r13_thought_active",False):
            s=text.strip()
            if s and not s.startswith("("):text="("+text
            if s and not s.endswith(")"):text=text+")"
            return text
        if "「" not in text:return text
        color=r13_role_color("entity","paper" if getattr(store,"r13_meeting_active",False) else "dark")
        parts=_r13_tre.split(r"(\{[^{}]*\}|\[[^\[\]]*\])",text)
        return "".join(p if p.startswith(("{","[")) else _R13_ITEM_SPAN.sub(lambda m:"{color="+color+"}"+m.group(0)+"{/color}",p) for p in parts)

    def r13_frame(kind):
        """Shared material; semantic colour roles remain independent of the rim."""
        return R13PaperFrame() if kind=="aged-paper" else R13InkPanel()

    def r13_dialogue_frame():
        # Approved translucent standard; explicit dark mode keeps its solid face.
        alpha=persistent.room13_window_alpha or "d4"
        dark=alpha in ("f0","f5","fa","ff")
        return R13InkPanel(alpha="ff" if dark else "c9" if alpha=="99" else "d9",dark=dark,slim=True)

init 141:
    # Keep the approved regular weight in labels.
    style say_label:
        bold False
