# 생활 동작 중 웅크리거나 앉은 그림의 키 비율(2026-10-27). 기준 키가 없는 장소(광장 등)는 그림을 칸 높이 그대로
# 늘려서, 11일 광장의 솜이(구두 얼음 긁기)가 어른보다 크게 섰다. 다른 생활 동작처럼 stature_ratio 를 준다.
# 값은 머리 크기를 평온 그림과 맞추는 비율((자세 키/머리)÷(평온 키/머리))이다. 그림 표(json)는 해시로 고정돼 있어
# 여기서 덧붙인다.
init 330 python:
    for _r13_ls_who,_r13_ls_pose,_r13_ls_ratio in (("resident_somi","living_bootice",.85),("resident_badook","living_bootlace",.84),
            ("resident_ubak","living_measure",.89),("resident_eunho","living_prices",.94),("resident_seori","living_notes",.95)):
        if _r13_ls_pose in R13_ACTING.get(_r13_ls_who,{}) and R13_ACTING[_r13_ls_who][_r13_ls_pose].get("stature_ratio") is None:
            R13_ACTING[_r13_ls_who][_r13_ls_pose]["stature_ratio"]=_r13_ls_ratio
