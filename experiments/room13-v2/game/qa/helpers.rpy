# 화면 시험 도우미(게임에는 쓰지 않는다). 시험은 대사 글자가 아니라 장면 ID·상태 값·화면 이름을 본다.

init python:
    def qa_jump(node, ev=(), vals=None, place=None):
        """시험을 짧게: 앞 단계를 이미 지난 상태로 만들고 그 노드로 간다."""
        if place:
            store.v2_loc = place
            v2_show_bg()
        for e in ev:
            v2_get(e)
        for k, v in (vals or {}).items():
            store.v2_vals[k] = v
        store.v2_ui = None
        store.v2_gate = None
        v2_goto(node)
        renpy.jump("v2_run")

    def qa_poke(key, value):
        store.v2_vals[key] = value

    def qa_write(name, value):
        with open(renpy.config.basedir + "/tests/" + name, "w") as f:
            f.write(repr(value))

    def qa_boot_mark():
        import time
        qa_write("boot.txt", time.time())

    def qa_measure():
        qa_write("measure.txt", dict(field_ms=v2_measure_field(200), gate=v2_gate, loc=v2_loc))
