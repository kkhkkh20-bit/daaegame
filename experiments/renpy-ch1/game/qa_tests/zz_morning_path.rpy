# 0.20.6 (Codex R06): a morning save belongs to the path that made it.
testcase morning_path:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.0
    $ persistent.r13_mornings={}
    $ r13_edit(morning_ids={})
    $ r13_morning_snapshot()
    assert eval (1 in r13_morning_days() and not r13_morning_due())
    # Back on another path: the run's ids no longer match the stored morning.
    $ r13_edit(morning_ids={"1":"other"})
    assert eval (1 not in r13_morning_days() and r13_morning_due())
    $ r13_morning_snapshot()
    assert eval (1 in r13_morning_days() and room13["morning_ids"]["1"]!="other")
