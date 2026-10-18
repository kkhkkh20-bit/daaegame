# Official RenPy 8.5.3 testcase. Unrun locally; no claim of native success.
# Disposable CI profile only. Actual title button, actions and card UI.
testcase recommended_story_first_slice:
    pause 2.0
    click "추천 스토리 검증판 · 엄마 B / 피코 C"
    click "새 추천 이야기 시작"
    $ r13_rec_admin_harness=True
    click pos (640,600) until screen "r13_recommended_actions" timeout 80
    click '돌목에게 두 사람의 입장 확인을 부탁한다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 90
    click '초소 선반에서 오늘 날짜의 신청 원본을 찾는다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 90
    click '돌목에게 원본과 방문 목록을 나란히 보여 준다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 90
    click '메인'
    click '자료 · 현장'
    click '초소 선반의 신청서'
    click "방문 신청 원본"
    click '메인'
    click '자료 · 현장'
    click '입구 방문 목록'
    click "돌목이 옮겨 쓴 방문 목록"
    click pos (640,600) until screen 'r13_recommended_actions' timeout 90
    assert eval ("entry_cleared" in r13_recommended["done"])
    click '까로와 짐을 옮겨 여관에서 엄마를 찾는다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 90
    assert eval (r13_recommended["day"]==1 and "entry_inn_arrived" in r13_recommended["done"])
    click "오늘을 마친다"
    click "다음 날로 간다"
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    assert eval (r13_recommended["mother"]=="M0" and r13_recommended["day"]==2)
    screenshot "recommended-01-entry.png"
    click '그림을 그리는 피코에게 오늘 밤을 묻는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    click '초롱의 낮 점검에 함께한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    click '피코와 여관의 실제 잠자리를 확인하고 함께 옮긴다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    click '부리에게 엄마가 맡긴 물건을 묻는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    click '엄마가 읽은 기록과 마지막 방문을 확인한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    click '초롱에게 가족이 도착했다고 알린다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    assert eval (r13_recommended["mother"]=='M0')
    screenshot "recommended-contact.png"
    click '초롱이 다녀오는 동안 장화를 말리며 쉰다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    click '돌아온 초롱에게 엄마의 답을 받는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    assert eval (r13_recommended["mother"]=='M1')
    screenshot "recommended-reply.png"
    click '열린 수리점 앞길을 확인하고 엄마를 만난다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    assert eval (r13_recommended["mother"]=='M2')
    screenshot "recommended-meet.png"
    click "저녁까지 기다린다"
    click pos (640,600) until screen "r13_recommended_actions" timeout 40
    click '장부에 나온 방을 저녁에 직접 살펴본다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    click '나비와 가족의 방·식사·출입을 실제 확인한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    assert eval (r13_recommended["mother"]=='M2')
    screenshot "recommended-shelter.png"
    assert eval ("family_shelter" in r13_recommended["done"] and r13_recommended["verdict"] is None)
    click "오늘을 마친다"
    click "다음 날로 간다"
    click pos (640,600) until screen "r13_recommended_actions" timeout 40
    assert eval (r13_recommended["piko"]=="safe" and r13_recommended["mother"]=="M2")
    click '빈 3번 등 안쪽을 살펴본다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    click '초롱에게 어제 만진 곳을 정확히 묻는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    click '나비에게 광장 돌과 배식길을 묻는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    click '나비의 배식길을 따라 아이 거처에서 실제 인계를 묻는다'
    click pos (640,600) until screen "r13_rec_piko_intact_cloth" timeout 90
    screenshot "recommended-intact-cloth-loan.png"
    click "돌을 내려놓을 때 모습"
    screenshot "recommended-torn-cloth-delivery.png"
    click "꼬미의 이야기로 돌아간다"
    click pos (640,600) until screen "r13_recommended_actions" timeout 90
    click "오늘을 마친다"
    click "다음 날로 간다"
    pause 0.5
    click "공개 회의"
    click pos (640,600) until screen "r13_rec_stage_choice" timeout 90
    click "우선 들은 말과 돌의 이동부터 정리한다"
    assert screen "r13_recommended_cards"
    click '사건 1'
    click '인물'
    click '꼬미'
    click "꼬미 · 용기의 전후 인계"
    click pos (640,600) until screen "r13_recommended_cards" timeout 40
    assert eval (r13_recommended["hearing"]==0)
    screenshot "recommended-hearing-wrong.png"
    click '사건 1'
    click '자료 · 현장'
    click '광장 3번 등'
    click '아빠와 다람 · 짧은 잔열'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 90
    click '사건 1'
    click '자료 · 현장'
    click '17번 돌'
    click '아이 거처의 17번 돌'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 90
    click '사건 1'
    click '인물'
    click '꼬미'
    click '꼬미 · 용기의 전후 인계'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 90
    assert eval (r13_recommended["verdict"]=="handoff_responsibility")
    assert eval (r13_recommended["piko"]=="safe" and r13_recommended["mother"]=="M2" and r13_recommended["nabi"]=="supervised_relief")
    assert eval (not room13["evidence"] and not room13["flags"])
    screenshot "recommended-09-partial-verdict.png"
    $ renpy.save("qa-recommended-slice")
    $ r13_qa_note("recommended_story_first_slice: actual title, family contact/reunion/shelter, Piko escort, field cards, wrong/correct presentation. Partial handoff finding only; direct-removal art gate remains closed.")

# No fixture state grants: real navigation -> person -> shared questions -> fact.
testcase recommended_story_field_entry:
    pause 2.0
    click "추천 스토리 검증판 · 엄마 B / 피코 C"
    click "새 추천 이야기 시작"
    click pos (640,600) until screen "r13_recommended_field" timeout 80
    assert eval (not r13_rec_admin_harness)
    screenshot "recommended-field-01-entry.png"
    click '돌목'
    click '돌목에게 두 사람의 입장 확인을 부탁한다'
    click pos (640,600) until screen 'r13_recommended_field' timeout 90
    click '초소 서류 선반'
    click '초소 선반에서 오늘 날짜의 신청 원본을 찾는다'
    click pos (640,600) until screen 'r13_recommended_field' timeout 90
    click '돌목'
    click '돌목에게 원본과 방문 목록을 나란히 보여 준다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 90
    click '메인'
    click '자료 · 현장'
    click '초소 선반의 신청서'
    click "방문 신청 원본"
    click '메인'
    click '자료 · 현장'
    click '입구 방문 목록'
    click "돌목이 옮겨 쓴 방문 목록"
    click pos (640,600) until screen 'r13_recommended_field' timeout 90
    assert eval ("entry_cleared" in r13_recommended["done"])
    click "지도 · 이동"
    click "여관 접수대"
    click '나비'
    click '까로와 짐을 옮겨 여관에서 엄마를 찾는다'
    click pos (640,600) until screen 'r13_recommended_field' timeout 90
    assert eval (r13_recommended["day"]==1 and "entry_inn_arrived" in r13_recommended["done"])
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
