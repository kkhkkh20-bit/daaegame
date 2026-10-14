# 배경음·효과음 연결 (0.18.5, 2026-10-14)
# - 배경음은 장소(배경)별로 고른다. 장소마다 평온/조사/밤 세 가지, 이야기 장면 몇 곳은 따로 지정.
# - 장소 환경음(바람·난로·시계)은 ambience 채널에서 반복한다.
# - 모든 버튼은 리모컨 버튼 '딸깍'. 증거를 내밀면 오케스트라 히트, 회의 판정 뒤 맞음/틀림 소리.
# 음원 출처·라이선스: assets/music-v6-credits.txt

init -5 python:
    renpy.music.register_channel("ambience", mixer="sfx", loop=True, stop_on_mute=True)
    config.main_menu_stop_channels = list(config.main_menu_stop_channels) + ["ambience"]

init 150 python:
    R13_BGM = {
        "title": "assets/bgm-title.mp3", "family": "assets/bgm-family.mp3", "ending": "assets/bgm-ending.mp3",
        "village": "assets/bgm-village.mp3", "village2": "assets/bgm-village2.mp3",
        "inn": "assets/bgm-inn.mp3", "inn2": "assets/bgm-inn2.mp3",
        "travel": "assets/bgm-travel.mp3", "snow": "assets/bgm-snow.mp3",
        "search": "assets/bgm-search.mp3", "think": "assets/bgm-think.mp3", "night": "assets/bgm-night.mp3",
        "council": "assets/bgm-council.mp3", "pressure": "assets/bgm-pressure.mp3",
        "dark": "assets/bgm-dark.mp3", "altar": "assets/bgm-altar.mp3",
    }
    R13_AMBIENCE = {"wind": "assets/amb-wind.mp3", "fire": "assets/amb-fire.mp3", "clock": "assets/amb-clock.mp3"}

    # 장소(배경 이름) → (평온, 조사, 밤) 배경음, 환경음
    R13_PLACE_SOUND = {
        "winter":          (("snow", "snow", "night"), "wind"),          # 눈에 막힌 입구
        "winter_square":   (("village", "search", "night"), "wind"),     # 광장
        "winter_post":     (("village", "search", "night"), "wind"),     # 우체국
        "winter_workshop": (("village2", "search", "think"), "clock"),   # 수리점
        "r13_store":       (("village2", "search", "night"), None),      # 공동 물품 창고
        "front":           (("inn", "think", "inn2"), "fire"),           # 여관 접수대
        "council":         (("inn", "think", "inn2"), "fire"),           # 여관 식당
        "kitchen":         (("inn", "think", "inn2"), "fire"),           # 여관 주방
        "hall":            (("inn", "search", "night"), None),           # 여관 2층 복도
        "guestroom":       (("inn2", "think", "inn2"), None),            # 임시 객실
        "room":            (("night", "night", "night"), None),          # 13호실
        "winter_passage":  (("dark", "dark", "dark"), None),             # 서비스 통로
        "r13_clinic":      (("think", "think", "think"), None),          # 임시 진료실
        "r13_school":      (("inn2", "inn2", "inn2"), None),             # 마을 학교
        "r13_greenhouse":  (("dark", "dark", "dark"), None),             # 폐온실 지하
        "r13_facility":    (("dark", "dark", "dark"), None),             # 북쪽 보호시설
        "r13_altar":       (("altar", "altar", "altar"), None),          # 숲속 제단
        "winter_carriage": (("travel", "travel", "travel"), None),       # 마차 안
    }
    R13_MOOD_SLOT = {"calm": 0, "search": 1, "night": 2}

    # 이야기 장면 지정: (배경, 제목) → (배경음 또는 None=무음, 환경음 또는 None=끔). 없으면 장소 규칙.
    R13_SCENE_SOUND = {
        ("winter", "초소 안 보호실 · 만남"): ("family", None),
        ("winter_square", "광장 · 끌고 가는 수레"): ("pressure", "wind"),
        ("r13_school", "학교 대피소"): ("inn2", None),
        ("r13_greenhouse", "폐온실 지하 · 합류"): ("family", None),
        ("r13_facility", "아무도 없는 만남의 방"): ("dark", None),
        ("r13_clinic", "금요일 · 진료실 앞"): ("think", None),
        ("r13_altar", "북쪽 산길 끝 · 숲속 제단"): ("altar", None),
        ("r13_altar", "산 아래 다시 켜진 마을"): ("ending", None),
        ("front", "여관 접수대"): ("inn", "fire"),
        ("front", "여관 접수대 · 그 뒤"): ("search", None),
        ("front", "월요일 아침 · 꺼져 가는 난방"): ("night", None),
        ("hall", "여관 2층 · 연기가 새는 문"): (None, None),
        ("room", "여관 2층 · 13호 구조 직후"): (None, None),
    }

    def r13_sound_choice(bg, title, mood):
        """(배경음 키 또는 None, 환경음 키 또는 None)."""
        if (bg, title) in R13_SCENE_SOUND:
            return R13_SCENE_SOUND[(bg, title)]
        tracks, amb = R13_PLACE_SOUND.get(bg, (None, None))
        if mood == "travel":
            return "travel", amb
        if mood == "hearing":
            return "council", None
        if mood == "quiet":
            return None, amb
        if tracks is None:
            return {"calm": "village", "search": "search", "night": "night"}.get(mood), amb
        return tracks[R13_MOOD_SLOT.get(mood, 0)], amb

    def r13_sound_ambience(key):
        path = R13_AMBIENCE.get(key) if key else None
        if path:
            if renpy.music.get_playing(channel="ambience") != path:
                renpy.music.play(path, channel="ambience", loop=True, fadein=1.0, fadeout=.5, relative_volume=.55)
        else:
            renpy.music.stop(channel="ambience", fadeout=.5)

    def r13_sound_scene_music(bg, title, mood):
        """label r13_scene 이 부른다. 재생할 배경음 경로(None=무음)를 돌려주고 환경음을 맞춘다."""
        bgm, amb = r13_sound_choice(bg, title, mood)
        r13_sound_ambience(amb)
        return R13_BGM.get(bgm) if bgm else None

    # 기존 효과음 키 → 새 파일. 없는 키는 예전 파일(assets/source-*.wav)을 그대로 쓴다.
    R13_FX = {
        "tap": "sfx-click", "select": "sfx-click", "page": "sfx-page", "found": "sfx-evidence-get",
        "pop9": "sfx-clue", "impact": "sfx-present", "cut9": "sfx-present", "knock": "sfx-knock",
        "door": "sfx-door-close", "doorOpen": "sfx-door-open", "unlock": "sfx-unlock", "slam": "sfx-slam",
        "steps": "sfx-walk-wood", "steps_snow": "sfx-walk-snow", "bell10": "sfx-bell",
        "present": "sfx-present", "right": "sfx-right", "wrong": "sfx-wrong",
    }

    def r13_fx_path(key):
        name = R13_FX.get(key)
        return "assets/" + name + ".wav" if name else None

    _r13_sound_source_fx = source_fx
    def source_fx(key):
        path = r13_fx_path(key)
        if path and renpy.loadable(path):
            if not renpy.is_skipping():
                store.source_effect_log.append(key)
                renpy.music.play(path, channel="scene_fx", loop=False)
            return
        return _r13_sound_source_fx(key)

    # 증거를 내밀 때(확인 뒤에만 불린다): 오케스트라 히트
    _r13_sound_present = r13_present
    def r13_present(person, key, identity=False):
        source_fx("present")
        return _r13_sound_present(person, key, identity)

    # 회의에서 증거를 내밀 때: 히트 뒤에 판정 소리(반박 성공=맞음, 틀림=틀림, 그 밖=히트만)
    _r13_sound_debate_judge = r13_debate_judge
    def r13_debate_judge(claim, sid, key):
        result = _r13_sound_debate_judge(claim, sid, key)
        if not renpy.is_skipping():
            follow = {"break": "right", "wrong": "wrong"}.get(result[0])
            queue = [r13_fx_path("present")] + ([r13_fx_path(follow)] if follow else [])
            store.source_effect_log.append("present:" + result[0])
            renpy.music.play(queue, channel="scene_fx", loop=False)
        return result


# 모든 버튼: 리모컨 버튼 '딸깍'
style button:
    activate_sound "assets/sfx-click.wav"

# 음악 출처 (CC BY 4.0 표기). 옵션 → 소리 → 음악 출처 → 보기
screen r13_music_credits():
    modal True
    zorder 120
    add Solid("#0b151bf4")
    frame:
        area (120,40,1040,640) background Solid("#14272b") padding (40,28)
        vbox:
            spacing 14
            text "음악 · 효과음 출처" size 32 color R13_UI_COLORS["menu_accent"]
            text "배경음" size 22 color "#f2d493"
            text "\"Sleep (Piano Only)\", \"The Long Way Home\", \"Home Was You\", \"Childhood\", \"Midvinter\", \"Snowfall\", \"First Snow\", \"Sanctuary\", \"The Long Dark\", \"Shadows and Dust\" by Scott Buckley – released under CC-BY 4.0. www.scottbuckley.com.au" size 18 color "#e6ece2"
            text "\"Heartwarming\", \"Water Lily\", \"Investigations\", \"Comfortable Mystery 4\", \"Measured Paces\", \"Iron Horse\" Kevin MacLeod (incompetech.com) Licensed under Creative Commons: By Attribution 4.0 License http://creativecommons.org/licenses/by/4.0/" size 18 color "#e6ece2"
            text "앞뒤 무음을 자르고 음량만 맞췄습니다. 작곡가가 이 게임을 보증한다는 뜻은 아닙니다." size 17 color R13_UI_COLORS["menu_secondary"]
            text "효과음" size 22 color "#f2d493"
            text "Kenney (kenney.nl), OpenGameArt.org 작가 1j01 · railkill · pwl · voltiment555 · cough-e · rubberduck · ignasd · pagdev · bart 의 CC0 소리" size 18 color "#e6ece2"
            null height 6
            textbutton "닫기" style "r13opt_button" xsize 170 action Hide("r13_music_credits") text_size 22
