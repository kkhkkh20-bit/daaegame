# 0.20.4 (owner 2026-10-22: "대사 타이핑속도 디폴트를 빠르게"): the default is now 빠르게(55).
# A browser that still holds the old default 보통(34) moves once; a speed chosen by hand stays.
default persistent.r13_text_speed_default_v2 = False
init 999 python:
    def r13_text_speed_migrate():
        if not persistent.r13_text_speed_default_v2:
            if preferences.text_cps==34:preferences.text_cps=config.default_text_cps
            persistent.r13_text_speed_default_v2=True
    config.start_callbacks.append(r13_text_speed_migrate)
