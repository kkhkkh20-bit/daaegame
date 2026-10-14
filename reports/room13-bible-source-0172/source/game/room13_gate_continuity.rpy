# The checkpoint remains staffed after a family is admitted. Keep this small
# extension separate from all other residents' existing routines and custody.
init 67 python:
    R13_GREETING.setdefault("guard", "등록은 확인했습니다. 저는 여기서 출입하는 분들을 계속 확인하겠습니다.")
    R13_CORE_PEOPLE.add("guard")

    _r13_before_gate_where = r13_where

    def r13_where(person):
        if person == "guard":
            # All playable time periods show the same staffed checkpoint.
            # Neither entry_corrected nor the family's case state ends duty.
            return "gate"
        return _r13_before_gate_where(person)

    ROOM13["topics"].setdefault("gate_guard_duty", dict(
        npc="guard", title="아직 초소를 지키고 있습니까?", day=[1,14],
        need=["entry_corrected"], give=[], flags=[],
        lines=[("guard", "등록이 끝나도 초소는 비울 수 없습니다. 들어오고 나가는 사람을 확인하고 있습니다.")]))
    ROOM13["topics"].setdefault("gate_guard_record", dict(
        npc="guard", title="바로잡은 입장 기록을 다시 확인한다", day=[1,14],
        need=["entry_corrected"], give=[], flags=[],
        lines=[("guard", "원본과 맞춰 보고 바로잡은 기록은 남겨 두었습니다. 두 분이 함께 들어오신 것으로 적혀 있습니다.")]))
