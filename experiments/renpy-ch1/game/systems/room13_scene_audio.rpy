# 장면 효과음·심장박동·생각 화자. 2026-10-27 옛 1장 해석기(source.rpy)를 지우면서 새 게임이 계속 쓰는
# 부분만 여기로 옮겼다. 이름(source_fx·source_pulse·source_thought·winter_copy)은 40여 파일이 부르고
# 저장 파일에도 들어가므로 바꾸지 않는다.
default source_effect_log = []

# 생각·지문 줄의 화자(이름 없음). r13_lines 가 화자 없는 줄에 쓴다.
define source_thought = Character(None,cb_who_id=None)

init -5 python:
    # 옛 겨울 판이 쓰던 별칭. 상태 사전을 복사하는 모든 곳(r13_edit 등)이 이 이름으로 부른다.
    import copy as winter_copy

    renpy.music.register_channel("scene_fx",mixer="sfx",loop=False)
    renpy.music.register_channel("pulse",mixer="sfx",loop=True)

    def source_fx(key):
        if key in ("roll","carStop","carDepart","letter","tick2"):
            return # 보관 중인 말 소리는 소유자 요청으로 끈 채 둔다.
        path=("assets/door.wav" if key=="doorOpen" else
              "assets/source-wood-door-close.wav" if key=="door" else
              "assets/source-"+key+".wav")
        if renpy.loadable(path) and not renpy.is_skipping():
            store.source_effect_log.append(key)
            renpy.music.play(path,channel="scene_fx",loop=False)

    def source_pulse(enabled):
        store.typing_allowed=not enabled
        renpy.music.stop(channel="typing")
        if enabled:
            if renpy.music.get_playing(channel="pulse"):
                return # 긴장 줄이 이어지면 심장박동 하나를 계속 쓴다.
            store.source_effect_log.append("heartbeat")
            renpy.music.stop(fadeout=0)
            renpy.music.play("assets/source-silence.wav",channel="pulse",loop=False)
            renpy.music.queue("assets/source-heartbeat.wav",channel="pulse",loop=True,clear_queue=True)
        else: renpy.music.stop(channel="pulse",fadeout=0)
