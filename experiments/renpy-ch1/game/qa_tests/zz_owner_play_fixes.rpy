# Owner play test 2026-10-22: first-meeting greeting, Daram's answer to the letter, cancel on 돌목.
testcase owner_play_fixes:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.0
    # 실룩 has not spoken with Dad yet: a stranger's greeting, not "또 만나네요".
    click "실룩"
    pause 0.8
    screenshot "fix-01-siluk-first.png"
    click pos (900,600) until screen "r13_hub" timeout 30
    pause 0.6
    # Daram: show the letter.
    click "다람"
    click pos (900,600) until screen "r13_topics" timeout 20  # 0.20.10: Daram answers once first
    pause 0.5
    screenshot "fix-02-daram-topics.png"
    click "자료 보여주기"
    pause 1.0
    click "QA V111:E01"
    pause 1.0
    screenshot "fix-03-daram-letter.png"
    # 0.20.6: the conversation stays open after the answer; 「돌아가기」 leaves it.
    click pos (200,400) until screen "r13_topics" timeout 30
    click "돌아가기"
    pause 1.0
    pause 0.6
    # 돌목: open the evidence, then cancel.
    click "돌목"
    pause 1.0
    screenshot "fix-04-guard.png"
    click pos (900,600) until screen "r13_hub" timeout 60
    pause 0.8
    screenshot "fix-05-hub-again.png"
    click "돌목"
    pause 1.2
    screenshot "fix-06-guard-topics.png"
    click "자료 보여주기"
    pause 1.2
    screenshot "fix-07-guard-book.png"
    click "QA 닫기"
    pause 1.5
    screenshot "fix-08-after-cancel.png"
    assert eval (renpy.get_screen("r13_hub") or renpy.get_screen("r13_topics"))
