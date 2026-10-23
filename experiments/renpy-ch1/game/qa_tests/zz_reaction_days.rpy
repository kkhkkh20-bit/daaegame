# 0.20.6 (Codex R01): the 6th-day answer does not hide the different 7th-day answer.
testcase reaction_days:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    $ r13_grant(["V111:E06_CONTACT"],"qa")
    $ r13_edit(day=6)
    $ qa_r6=r13_v111_present_reaction("nabi","V111:E06_CONTACT")
    assert eval (qa_r6 and "이름이 없군요" in qa_r6[0][1])
    $ r13_edit(day=7)
    assert eval (not r13_reaction_seen([s for s in R13_REACTIONS["present"] if s["person"]=="nabi" and s["evidence"]=="E06_CONTACT" and r13_reaction_day_ok(s)][0]))
    $ qa_r7=r13_v111_present_reaction("nabi","V111:E06_CONTACT")
    assert eval (qa_r7 and "여전히" in qa_r7[0][1])
