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
        return _r13_before_question_dismiss() if _r13_before_question_dismiss else True

    config.say_allow_dismiss=r13_question_allow_dismiss
