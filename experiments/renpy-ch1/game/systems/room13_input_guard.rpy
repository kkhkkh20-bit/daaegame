# Keep a rapid second tap on a question from dismissing its first reply.
# Transient engine state: no wall-clock deadline is stored in game saves.
init 147 python:
    import time as r13_input_clock
    renpy._r13_question_deadline=0.0
    _r13_before_question_dismiss=config.say_allow_dismiss

    def r13_mark_question_input():
        renpy._r13_question_deadline=r13_input_clock.monotonic()+.35

    def r13_safe_question_action(action):
        return [Function(r13_mark_question_input),action]

    def r13_question_allow_dismiss():
        if getattr(store,"room13_mode",False) and r13_input_clock.monotonic()<renpy._r13_question_deadline:
            return False
        allowed=_r13_before_question_dismiss() if _r13_before_question_dismiss else True
        if allowed and getattr(store,"room13_mode",False):
            renpy._r13_last_advance=r13_input_clock.monotonic()
        return allowed

    # 2026-10-29 눈가림 플레이: 대사를 넘기던 손이 대사가 끝난 줄 모르고 한 번 더 누르면, 막 다시 뜬 조사 화면의
    # 인물·물건이 그 누름을 받아 다른 대화가 열렸다(3일 톡·초롱 뒤 「바쁜 사람을 자꾸 붙잡지 말자」가 이어짐).
    # 같은 누름이 두 번 먹는 것은 아니다(대사가 mouseup 을 먹는다). 대사를 넘긴 시각을 적어 두고, 조사 화면과
    # 질문 목록은 그 뒤 잠깐(.6초) 동안 현장·질문을 받지 않는다. 화면이 늦게 떴으면 남은 만큼만 기다린다.
    renpy._r13_last_advance=0.0
    def r13_field_ready_delay(base=.15,after_line=.6):
        left=after_line-(r13_input_clock.monotonic()-getattr(renpy,"_r13_last_advance",0.0))
        return max(base,left)

    config.say_allow_dismiss=r13_question_allow_dismiss
