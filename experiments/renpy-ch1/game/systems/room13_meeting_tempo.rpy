# Review pilot: meeting milestones, not individual emotional pressure.
default r13_meeting_tempo_milestones = []

init 173 python:
    R13_MEETING_TEMPO_ENABLED = True
    R13_MEETING_TEMPO_RATES = (1.0,1.06,1.12)

    def r13_meeting_tempo_stage(claim=None):
        claim=claim or getattr(store,"r13_meeting_claim",None)
        if not R13_MEETING_TEMPO_ENABLED or claim!="C2":return 0
        run=(store.room13 or {}).get("run_token","legacy")
        return min(2,len(set(tuple(x) for x in store.r13_meeting_tempo_milestones if tuple(x[:2])==(run,claim))))

    def r13_meeting_tempo_mark(claim,sid):
        proof=getattr(store,"r13_meeting_proof_reveal",None) or {}
        if claim!="C2" or not proof.get("revealed") or proof.get("claim")!=claim or proof.get("sid")!=sid:return
        token=((store.room13 or {}).get("run_token","legacy"),claim,sid)
        if token not in store.r13_meeting_tempo_milestones:
            store.r13_meeting_tempo_milestones=list(store.r13_meeting_tempo_milestones)+[token]

    def r13_meeting_tempo_file(path):
        return path.split(">",1)[-1] if path and path.startswith("<") else path

    def r13_meeting_tempo_identity(path):
        path=r13_meeting_tempo_file(path)
        for base in ("council","pressure"):
            if path==R13_BGM[base]:return base,0
            for stage in (1,2):
                if path=="assets/bgm-%s-tempo%d.ogg"%(base,stage):return base,stage
        return None,0

    def r13_meeting_tempo_path(wanted):
        stage=r13_meeting_tempo_stage()
        if not stage or wanted not in ("council","pressure"):return R13_BGM[wanted]
        reaction=getattr(store,"r13_meeting_collective",None) or {}
        # Change only after the silent reveal/collective beat has settled.
        if reaction.get("phase") in ("pending","playing"):
            current=r13_meeting_tempo_file(renpy.music.get_playing(channel="music"))
            base,old_stage=r13_meeting_tempo_identity(current)
            if base==wanted:return current
        return "assets/bgm-%s-tempo%d.ogg"%(wanted,stage)

    def r13_meeting_tempo_play(path):
        current=renpy.music.get_playing(channel="music")
        if r13_meeting_tempo_file(current)==path:return
        old_base,old_stage=r13_meeting_tempo_identity(current)
        new_base,new_stage=r13_meeting_tempo_identity(path)
        position=renpy.music.get_pos(channel="music")
        if old_base and old_base==new_base and position is not None:
            # Map the same musical position; never change playback sample rate/pitch.
            position=max(0.0,position)*R13_MEETING_TEMPO_RATES[old_stage]/R13_MEETING_TEMPO_RATES[new_stage]
            renpy.music.play("<from %.3f>%s"%(position,path),channel="music",loop=False,fadeout=.12,fadein=.20)
            renpy.music.queue(path,channel="music",loop=True)
        else:
            renpy.music.play(path,channel="music",loop=True,fadeout=.12,fadein=.20)

    def r13_meeting_tempo_snapshot():
        if not R13_MEETING_TEMPO_ENABLED or getattr(store,"r13_meeting_claim",None)!="C2":return None
        return dict(path=renpy.music.get_playing(channel="music"),position=renpy.music.get_pos(channel="music"),
            volume=r13_meeting_channel_gain("music"),paused=renpy.music.get_pause(channel="music"))

    def r13_meeting_interrupt_with_tempo(claim,sid):
        # A nested context restores its parent's audio when it returns. Carry the
        # child's actual musical position back, rather than restart its stage.
        audio=renpy.call_in_new_context("r13_meeting_interrupt",claim,sid)
        if not audio:return
        path=r13_meeting_tempo_file(audio.get("path"))
        if not path:return
        position=audio.get("position")
        if position is not None:
            renpy.music.play("<from %.3f>%s"%(max(0.0,position),path),channel="music",loop=False,fadeout=.08,fadein=.12)
            renpy.music.queue(path,channel="music",loop=True)
        else:renpy.music.play(path,channel="music",loop=True,fadeout=.08,fadein=.12)
        renpy.music.set_volume(audio["volume"],channel="music")
        renpy.music.set_pause(audio["paused"],channel="music")

init 192 python:
    _r13_tempo_pressure_proof=r13_meeting_pressure_proof
    def r13_meeting_pressure_proof(claim,sid):
        _r13_tempo_pressure_proof(claim,sid)
        r13_meeting_tempo_mark(claim,sid)
