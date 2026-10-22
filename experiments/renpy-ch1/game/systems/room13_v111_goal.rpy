# 0.20.7 (play review D23-06 and the full play check): the old campaign's goal line ("의문 · …",
# "10일째 청문까지 N일") read stale in the new story (save cards, the day board). The new story
# has no such single goal, so the line is left out; the save card keeps place and last line.
init 340 python:
    _r13_v111_campaign_goal=r13_campaign_goal
    def r13_campaign_goal():
        if globals().get("r13_v111_active",lambda:False)():return None
        return _r13_v111_campaign_goal()

# 후반 기획서 D (2026-10-23): 장면 단위 의문보다 지금 단계의 목적을 먼저 보인다. 지금까지 확인한
# 사실만 말한다. 단계 문구가 없는 대기에서는 기존 장면 의문을 그대로 쓴다.
init 341 python:
    R13_V111_STEP_GOALS={
        "nabi_beds13":"수레에서 내려올 사람들이 누울 자리를 확인하자.",
        "momo_down13":"내려온 사람을 학교에서 실제로 맡았는지 확인하자.",
        "guldol_down13":"내려온 사람을 학교에서 실제로 맡았는지 확인하자.",
        "transport_cleanup13":"다음 명단이 와도 다시 태우지 못하게 하자.",
        "device_lock14":"떼어 낸 부품을 다시 사람에게 쓰지 못하게 보관하자.",
        "supply_inventory14":"오늘 밤 학교에서 쓸 몫과 남은 양을 확인하자.",
    }
    _r13_step_goal=r13_v111_goal
    def r13_v111_goal():
        gate=(store.room13.get("v111") or {}).get("gate")
        return R13_V111_STEP_GOALS.get(gate) or _r13_step_goal()
