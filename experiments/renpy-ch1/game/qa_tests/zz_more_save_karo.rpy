testcase more_save_karo:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.0
    click "까로"
    pause 1.5
    click pos (900,600) until screen "r13_topics" timeout 30
    pause 1.0
    screenshot "karo-01-topics.png"
    click "더보기"
    pause 1.0
    screenshot "karo-02-more.png"
    click "저장 · 불러오기"
    pause 1.5
    screenshot "karo-03-save.png"
    assert screen "save"
