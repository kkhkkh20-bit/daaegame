# Text-compatible screen statement: Character injects substitute/scope/slow
# properties into id "what", which must reach Text directly, never an Add wrapper.
python early:
    def r13_dialogue_displayable(*args,**kwargs):
        return renpy.store.R13DialogueText(*args,**kwargs)
    renpy.register_sl_displayable("r13_dialogue_text",r13_dialogue_displayable,"text",scope=True,replaces=True).copy_properties("text")

# Display-only timing. Original dialogue/history/read keys remain unchanged.
init 62 python:
    import re as r13_rhythm_re

    def r13_rhythmic_text(text):
        cps=float(preferences.text_cps or 0)
        if not isinstance(text,str) or cps<=0 or renpy.is_skipping():
            return text
        # Respect any explicitly authored speed rather than nesting overrides.
        if "{cps=" in text:return text
        result=[]
        pending=0.0
        budget=1.2
        for part in r13_rhythm_re.split(r"(\{[^{}]*\}|\[[^\[\]]*\])",text):
            if part.startswith(("{","[")):
                result.append(part)
                continue
            i=0
            while i<len(part):
                punctuation=r13_rhythm_re.match(r"[,，.。!?！？…]+",part[i:])
                if punctuation:
                    run=punctuation.group(0)
                    end=i+len(run)
                    numeric=(run in (".",",") and i>0 and end<len(part) and part[i-1].isdigit() and part[end].isdigit())
                    result.append(run)
                    if not numeric:
                        pending=.30 if "…" in run or ".." in run else .26 if any(c in run for c in ".。!?！？") else .12
                    i=end
                    continue
                char=part[i]
                if pending and char not in "\n\r\t\"'’”)]»" and budget>0:
                    pause=min(pending,budget)
                    # Ren'Py assigns the delay BEFORE each glyph. Slow the
                    # following space/letter, so punctuation itself stays prompt.
                    rate=1.0/(1.0/cps+pause)
                    result.append("{cps=%.6f}"%rate+char+"{/cps}")
                    budget-=pause
                    pending=0.0
                else:
                    result.append(char)
                i+=1
        # A final punctuation mark already waits for player input; no invisible
        # trailing glyph or extra interaction is added to a completed line.
        return "".join(result)

    class R13DialogueText(renpy.text.text.Text):
        # Character owns the original self.text and installs slow/slow_done by
        # comparing it with the original say string. Only the layout token
        # stream receives punctuation timing, after that contract is preserved.
        def tokenize(self,text):
            # 2026-10-29 소유자 캡처 「(말이 명부를 닮았다.)( 짧고, 고쳐 쓸 칸이 없다.)」: {w} 가 든 줄은 여기에 조각으로 온다.
            # 생각 줄 괄호를 조각마다 씌우면 중간에서 「)(」가 생긴다. 괄호는 첫 조각 앞과 끝 조각 뒤에만 둔다.
            strs=[i for i,part in enumerate(text) if isinstance(part,str)]
            display_text=[r13_rhythmic_text(r13_semantic_text(part,i==strs[0],i==strs[-1])) if isinstance(part,str) else part for i,part in enumerate(text)]
            return super(R13DialogueText,self).tokenize(display_text)

        def __init__(self,*args,**kwargs):
            previous=kwargs.get("replaces")
            super(R13DialogueText,self).__init__(*args,**kwargs)
            same=previous is not None and previous.text==self.text
            self.r13_audio_seen=getattr(previous,"r13_audio_seen",0) if same else 0
            self.r13_revealed=getattr(previous,"r13_revealed",0) if same else 0

        def render(self,width,height,st,at):
            result=super(R13DialogueText,self).render(width,height,st,at)
            layout=self.get_layout()
            if layout is not None:
                # Observe the same glyph timestamps the renderer uses, including
                # punctuation pauses. Audio runs from the screen timer, not render.
                self.r13_revealed=sum(1 for paragraph in layout.paragraph_glyphs for g in paragraph if 0 < g.time <= st)
            return result

    def r13_typing_tick():
        blocked=any(renpy.get_screen(name) for name in ("pause_menu","save","load","r13_records","r13_book","r13_backlog","r13_mystery_notebook","r13_cinematic_view","confirm"))
        text=renpy.get_displayable("say","what") if renpy.get_screen("say") else None
        if blocked or text is None or not text.slow or not preferences.text_cps or renpy.is_skipping() or not store.typing_allowed or not persistent.room13_typing_sound:
            renpy.music.stop(channel="typing")
            if text is not None:
                text.r13_audio_seen=getattr(text,"r13_revealed",0)
            return
        count=getattr(text,"r13_revealed",0)
        previous=getattr(text,"r13_audio_seen",0)
        text.r13_audio_seen=count
        if count>previous:
            # A short non-looping click per newly revealed glyph group; lag never
            # queues a backlog after the displayed text has finished.
            renpy.music.play("<from 0 to 0.025>assets/type.wav",channel="typing",loop=False)
