# No fixture state grants: real navigation -> person -> shared questions -> fact.
testcase recommended_story_field_entry:
    pause 2.0
    click "추천 스토리 검증판 · 엄마 B / 피코 C"
    click "새 추천 이야기 시작"
    click pos (640,600) until screen "r13_recommended_field" timeout 80
    assert eval (not r13_rec_admin_harness)
    screenshot "recommended-field-01-entry.png"
    click "지도 · 이동"
    assert screen "r13_recommended_map"
    click "수리점"
    pause 1.0
    assert screen "r13_recommended_field"
    assert eval (r13_recommended["location"]=="workshop")
    click "부리"
    assert screen "r13_recommended_subject"
    screenshot "recommended-field-02-earned-question.png"
    click "부리에게 엄마가 맡긴 물건을 묻는다"
    click pos (640,600) until screen "r13_recommended_field" timeout 70
    assert eval ("repair" in r13_recommended["facts"])
    click "지도 · 이동"
    click "우체국 기록실"
    pause 1.0
    click "사서 선생님"
    click "엄마가 읽은 기록과 마지막 방문을 확인한다"
    click pos (640,600) until screen "r13_recommended_field" timeout 80
    assert eval ("ledger" in r13_recommended["facts"] and r13_recommended["mother"]=="M0")
    screenshot "recommended-field-03-records.png"
    $ r13_qa_note("recommended_story_field_entry: actual title/setup/map/place/person/shared-question clicks; no state grants. Native result pending until CI runs.")
