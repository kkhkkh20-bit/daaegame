# 2026-10-25 종이 소리 후보를 개발본 UI에 낮은 음량으로 연결한다.
# CC0 출처는 assets/diary-sounds/SOURCES.txt. 최대 피크0dB인01후보는 채택하지 않는다.
init 154 python:
    R13_DIARY_FX = {
        "note_open":("assets/diary-sounds/notebook-open.ogg",.45),
        "page":("assets/diary-sounds/evidence-paper.mp3",.8),
    }
    _r13_diary_before_source_fx=source_fx
    def source_fx(key):
        if key in R13_DIARY_FX:
            path,volume=R13_DIARY_FX[key]
            path=r13_asset_path("file:"+path)
            if renpy.loadable(path):
                if not renpy.is_skipping():
                    store.source_effect_log.append(key)
                    renpy.music.play("<volume %s>%s"%(volume,path),channel="scene_fx",loop=False)
                return
        return _r13_diary_before_source_fx(key)
