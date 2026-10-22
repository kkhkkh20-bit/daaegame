# 0.20.7 (play review D23-06 and the full play check): the old campaign's goal line ("의문 · …",
# "10일째 청문까지 N일") read stale in the new story (save cards, the day board). The new story
# has no such single goal, so the line is left out; the save card keeps place and last line.
init 340 python:
    _r13_v111_campaign_goal=r13_campaign_goal
    def r13_campaign_goal():
        if globals().get("r13_v111_active",lambda:False)():return None
        return _r13_v111_campaign_goal()
