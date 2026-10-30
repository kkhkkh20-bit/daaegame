# 2026-10-30 소유자 지적「표정이 바뀔 때 인물이 잠깐 사라졌다 나타난다」(웹).
#
# 원인: 웹판은 대화 인물 그림을 처음부터 받지 않고(dev/build_web.py 의 진행 내려받기), 받기 전에는 투명한
# 대체 그림을 그린다(renpy/webloader.py). 대사 줄마다 r13_speaker 가 그림을 직접 만들어 보여 주므로 Ren'Py 의
# 미리 읽기가 그 그림을 알 수 없고, 처음 나오는 표정은 그 줄에서야 받기 시작해 첫 화면이 비었다.
# 받은 파일도 60초 뒤 메모리에서 지워지므로 같은 표정이 다시 나와도 또 빌 수 있었다.
#
# 고친 방법(셋 다 웹에서만 동작, 데스크톱은 그대로):
#   1. 미리 받기 — r13_lines 가 한 줄을 그릴 때 뒤 세 줄에 나올 인물 그림 파일을 미리 받기 시작한다.
#   2. 지우지 않기 — 지금 줄과 뒤 세 줄 그림은 60초 지움을 미룬다(webloader.extend).
#   3. 마지막 보장 — 그래도 아직 못 받은 그림이면, 새 그림을 보이기 전에 받을 때까지(최대 3초) 기다린다.
#      기다리는 동안 화면은 바로 앞 줄 그대로 멈춰 있다(앞 그림이 남아 있다). 빈 인물은 한 번도 보이지 않는다.
#      투명한 대체 그림으로 머리 높이를 재서 자리가 틀어지던 것(room13_say_actor.rpy)도 이 순서로 함께 막힌다.
# 3만으로도 빈 화면은 막히지만 그러면 처음 나오는 표정마다 앞 줄이 잠깐 멈춘다. 1·2가 그 멈춤을 거의 없앤다.
init 30 python:
    import os as _r13_wa_os, time as _r13_wa_time

    R13_WEB_ART_READY=True    # 끄면 예전과 같다(전후 비교 측정용 스위치)
    R13_WEB_ART_WAIT=3.0      # 이보다 오래 걸리면(연결 끊김) 기다리지 않고 예전처럼 진행한다
    R13_WEB_ART_AHEAD=3       # 미리 받는 줄 수

    def r13_say_actor_pose(who,expression="neutral",pose=None):
        """대사 줄의 (표정, 지금 자세, 그릴 자세). r13_speaker(room13_rules.rpy)와 아래 미리 받기가 같은 계산을 쓴다."""
        expression=expression if who in CAST and "avatar_"+str(expression) in CAST[who] else "neutral"
        current=r13_conversation_pose(who,pose or expression)
        actor=current if r13_acting_spec(who,current) or r13_fullbody_authored_pose(who,current) or current in R13_FULLBODY_NEW else "interview_"+expression
        return expression,current,actor

    def r13_art_files(d):
        """그릴 그림(displayable) 안의 이미지 파일 이름. 표정·자세·깜빡임 조각까지 실제로 그릴 파일을 그대로 모은다."""
        out=[];seen=set();stack=[d]
        while stack:
            x=stack.pop()
            if x is None or id(x) in seen:continue
            seen.add(id(x))
            fn=getattr(x,"filename",None)
            if isinstance(fn,str) and fn not in out:out.append(fn)
            try:stack.extend(x.visit() or [])
            except Exception:pass
        return out

    def r13_web_art_present(f):
        return _r13_wa_os.path.exists(_r13_wa_os.path.join(config.gamedir,f))

    def r13_web_art_ready(files):
        """웹에서 이 파일들을 지금 그려도 대체 그림이 아닌가. 데스크톱은 늘 참."""
        if not renpy.emscripten or not R13_WEB_ART_READY:return True
        import renpy.webloader as wl
        pending={rr.data for rr in list(wl.queue)}
        return all(r13_web_art_present(f) and f not in pending for f in files if f in renpy.loader.remote_files)

    def r13_web_art_fetch(files):
        """받지 않은 파일은 받기 시작하고, 받아 둔 파일은 60초 지움을 미룬다. 못 받은 파일 목록을 돌려준다."""
        if not renpy.emscripten or not R13_WEB_ART_READY:return []
        import renpy.webloader as wl
        missing=[]
        for f in files:
            if f not in renpy.loader.remote_files:continue
            if r13_web_art_present(f):
                wl.extend(f)
            else:
                wl.enqueue(f,"image",f)
                missing.append(f)
        return missing

    def r13_web_art_wait(what):
        """새 인물 그림을 보이기 직전에 부른다. 웹에서 아직 못 받은 그림이면 받을 때까지 기다린다."""
        if not renpy.emscripten or not R13_WEB_ART_READY:return True
        files=r13_art_files(what)
        r13_web_art_fetch(files)
        if r13_web_art_ready(files):return True
        import emscripten, renpy.webloader as wl
        deadline=_r13_wa_time.time()+R13_WEB_ART_WAIT
        while _r13_wa_time.time()<deadline:
            # 받기는 브라우저가 한다. 잠깐 넘겨 주면 받은 파일이 게임 파일 칸에 들어온다.
            emscripten.sleep(16)
            if all(r13_web_art_present(f) for f in files if f in renpy.loader.remote_files):break
        try:
            # 받은 파일로 대체 그림 캐시를 비운다(보통은 다음 화면 갱신 때 엔진이 한다).
            wl.process_downloaded_resources()
        except Exception:
            pass
        return r13_web_art_ready(files)

    def r13_say_lookahead_art(who,expression,pose):
        """뒤 줄에서 r13_speaker 가 보일 그림(미리 받기용). 보일 사람이 없으면 None."""
        vp=r13_viewpoint()
        carriage=store.place=="마차 안"
        if who not in CAST or who==vp or store.r13_camera!="stage":return None
        if carriage:
            if who!="daram":return None
            return r13_carriage_daram_seat_art(r13_carriage_seat(pose or expression))
        _expr,_current,actor_pose=r13_say_actor_pose(who,expression,pose)
        # 지금 줄의 반응 계획(r13_dialogue_beat)이 다른 줄 그림에 섞이지 않게 잠깐 비운다.
        beat=store.r13_dialogue_beat
        store.r13_dialogue_beat=None
        try:
            return r13_close_art(who,actor_pose,r13_say_actor_h(False),True,False)
        finally:
            store.r13_dialogue_beat=beat

    def r13_say_prefetch(entries,index,identity):
        """r13_lines 가 한 줄을 그린 뒤 부른다. 뒤 몇 줄의 인물 그림을 웹에서 미리 받는다."""
        if not renpy.emscripten or not R13_WEB_ART_READY or getattr(store,"r13_meeting_active",False):return
        for i in range(index+1,min(len(entries),index+1+R13_WEB_ART_AHEAD)):
            try:
                packet=r13_dead_stand_in_packet(r13_pov_packet(entries[i]),identity)
                meta=packet[2] if len(packet)>2 and isinstance(packet[2],dict) else {}
                if meta.get("thought"):continue
                who=packet[0]
                if who is None and meta.get("show") in CAST:
                    art=r13_say_lookahead_art(meta["show"],meta.get("expression","neutral"),meta.get("pose") or meta.get("expression","neutral"))
                else:
                    expression,pose=r13_line_performance(identity,i,packet)
                    art=r13_say_lookahead_art(who,expression,pose)
                if art is not None:r13_web_art_fetch(r13_art_files(art))
            except Exception:
                # 미리 받기는 덤이다. 실패해도 줄 진행을 막지 않는다(보일 때 r13_web_art_wait 가 받는다).
                pass
