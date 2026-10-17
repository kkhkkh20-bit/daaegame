# 0.18.95 끝난 에피소드의 기록 정리 (소유자 2026-10-17: "자연스럽게 이제 이것들은 안 쓰겠지 하는 느낌으로")
# - 에피소드가 끝나면 그 에피소드에서만 쓰던 기록은 수첩의 「지난 사건」 묶음으로 옮긴다.
#   지금 쓰는 자료 목록과 보여주기 목록에서 빠지고, 「지난 사건」 버튼으로 언제든 다시 읽을 수 있다.
# - 기록 자체는 그대로 가지고 있다(관계도·이야기 조건은 계속 본다). 화면에서만 옮긴다.
# - 뒤 에피소드에서 다시 쓰는 기록은 남긴다: K02(⑥), K08(⑤), N05·N06(엄마의 편지), Y05·Y06·Y14(⑥).
init 170 python:
    R13_SHELF = [
        # (끝난 표식 또는 함수, 이름, 옮길 기록)
        ("lt_done","① 등 도둑",["L%02d"%i for i in range(0,15)]),
        ("kd_done","② 처마 밑의 이빨 자국",["K01","K03","K04","K05","K06","K07","K09"]),
        ("wf_done","③ 장작 창고의 불",["F%02d"%i for i in range(1,15)]),
        (lambda:bool((store.room13 or {}).get("week2_started")),"④ 13호의 밤",["N01","N02","N03","N07","N08","N09"]),
        ("ws_done","⑤ 긴 밤과 겨울 수프",["Y01","Y02","Y03","Y04","Y07","Y08","Y09","Y10","Y11","Y12","Y13"]),
    ]

    def r13_shelf_closed(done):
        return done() if callable(done) else r13_has(done)

    def r13_shelved_keys():
        if not store.room13:return set()
        out=set()
        for done,name,keys in R13_SHELF:
            if r13_shelf_closed(done):out|=set(keys)
        return out

    # 에피소드가 끝나는 순간 한 줄로 알려 준다. 기록을 버리는 게 아니라 묶어 두는 느낌으로.
    _r13_shelf_flag=r13_flag
    def r13_flag(*keys):
        closing=[name for done,name,k in R13_SHELF if isinstance(done,str) and done in keys and not r13_has(done)]
        _r13_shelf_flag(*keys)
        for name in closing:
            renpy.notify("%s의 기록을 수첩 「지난 사건」에 묶어 두었다."%name)
