# Native fixtures only. No native execution or screenshots claimed by generation.
# The field test clicks actual locations, NPC/object subjects, questions and hearings.
# Direct-entry boot seeds M2/Piko-safe/Nabi supervised; it does not claim earlier gameplay.
testcase recommended_ep2_field_and_hearing:
    pause 2.0
    $ r13_rec_admin_harness=False
    run Call("r13_recommended_ep2_admin")
    click pos (640,600) until screen "r13_recommended_field" timeout 40
    click "지도 · 이동"
    click "눈에 막힌 입구"
    pause 0.5
    click '돌목'
    assert screen "r13_recommended_subject"
    click '돌목의 보고를 듣고 밤이의 상황을 확인한다'
    click pos (640,600) until screen 'r13_recommended_field' timeout 100
    screenshot "recommended-e2-01-reported.png"
    click "오늘을 마친다"
    click "다음 날로 간다"
    click pos (640,600) until screen "r13_recommended_field" timeout 50
    click '수레 난간과 소매천'
    assert screen "r13_recommended_subject"
    click '수레 난간과 소매가 걸린 자리를 살펴본다'
    click pos (640,600) until screen 'r13_recommended_field' timeout 100
    click '담요와 짧은 두 고리'
    assert screen "r13_recommended_subject"
    click '담요를 펼쳐 두 짧은 고정끈을 확인한다'
    click pos (640,600) until screen 'r13_recommended_field' timeout 100
    click '솜이'
    assert screen "r13_recommended_subject"
    click '솜이에게 담요 주인과 귀가 약속을 묻는다'
    click pos (640,600) until screen 'r13_recommended_field' timeout 100
    click '밤이'
    assert screen "r13_recommended_subject"
    click '밤이에게 수레에서 누구를 보고 있었는지 묻는다'
    click pos (640,600) until screen 'r13_recommended_field' timeout 100
    click '바둑이'
    assert screen "r13_recommended_subject"
    click '수레 담당 바둑이에게 요구 전후를 처음부터 듣는다'
    click pos (640,600) until screen 'r13_recommended_field' timeout 100
    assert eval ("e2_card_badook" in r13_recommended["facts"] and not r13_recommended["episodes"]["2"]["bite_admitted"])
    screenshot "recommended-e2-02-before-hearing.png"
    click "약속한 회의에 간다"
    click pos (640,600) until screen "r13_rec_stage_choice" timeout 80
    click "이름·거처 비공개를 회의 규칙으로 정하고, 밤이가 답할지 고르게 한다"
    click pos (640,600) until screen "r13_recommended_cards" timeout 80
    assert eval (r13_recommended["episodes"]["2"]["bite_admitted"])
    click '사건 2'
    click '인물'
    click '솜이'
    click '솜이 · 돌아오기로 한 약속'
    click pos (640,600) until screen "r13_recommended_cards" timeout 80
    assert eval (r13_recommended["episodes"]["2"]["stage"]==0)
    screenshot "recommended-e2-03-wrong-card.png"
    click '사건 2'
    click '자료 · 현장'
    click '수레와 고정끈'
    click '수레 난간 · 소매가 닿은 자리'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 2'
    click '인물'
    click '바둑이'
    click '바둑이 · 비명보다 먼저 본 손'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 2'
    click '자료 · 현장'
    click '수레와 고정끈'
    click '담요와 두 짧은 고정끈'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 2'
    click '인물'
    click '돌목'
    click '돌목 · 보고와 실제 행위'
    click pos (640,600) until screen 'r13_rec_stage_choice' timeout 100
    click "결박 → 풀라는 요구 → 수레 안으로 뻗은 팔 → 밤이의 물림"
    click pos (640,600) until screen "r13_recommended_field" timeout 100
    assert eval (r13_recommended["episodes"]["2"]["verdict"]=="bite_and_prior_coercion")
    assert eval (r13_recommended["mother"]=="M2" and r13_recommended["piko"]=="safe")
    screenshot "recommended-e2-04-consequence.png"
    $ r13_qa_note("recommended_ep2_field_and_hearing: real map, actor/object, question, anonymity, wrong/correct card and order clicks. Initial M2/Piko-safe state is a disclosed fixture.")

# Separate admin-action harness: tests dialogue/actions + evidence/map, not physical hotspot navigation.
testcase recommended_ep3_prevention_map:
    pause 2.0
    $ r13_rec_admin_harness=True
    run Call("r13_recommended_ep3_admin")
    click pos (640,600) until screen "r13_recommended_actions" timeout 40
    click '나비에게 따로 덜어 둔 네 그릇을 묻는다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    click '창고에서 네 아이에게 오늘 밤 계획을 듣는다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    click '학교의 난로·네 자리·야간 돌봄을 확인한다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    click '네 아이를 데리고 학교에 들어가 실제 인계한다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    assert eval (r13_recommended["e3_school_handoff"] and r13_recommended["episodes"]["3"]["children"]=="school")
    screenshot "recommended-e3-01-actual-school-handoff.png"
    click "오늘을 마친다"
    click "다음 날로 간다"
    click pos (640,600) until screen "r13_recommended_actions" timeout 50
    click '학교에서 네 아이가 무사한 아침을 확인한다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    click '안전 확인 뒤 뜯긴 벽의 폭과 방향을 본다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    click '보리에게 불난 뒤 벽을 뜯은 이유를 묻는다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    click '등잔 자리·문밖 통·뜯긴 벽의 배치를 확인한다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    click '선생님에게 창문에서 본 순서와 시야 끝을 묻는다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    click '창고 문앞 W의 통과 바로 옆 주둥이 조각을 맞춘다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    click '누비에게 현장에 남은 통을 보여 주고 인계를 묻는다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    click '큰아이에게 귀가를 기다린 자리와 걱정을 묻는다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    click '큰아이의 학교 돌봄과 비공개 면담 범위를 실제 마련한다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    assert eval (r13_recommended["episodes"]["3"]["kkomi"]=="alive")
    assert eval ("e3_card_child" not in r13_recommended["facts"])
    click "공개 회의"
    click pos (640,600) until screen "r13_rec_stage_choice" timeout 80
    click "보호자 동석·이름 비공개로, 아이가 동의한 관찰만 듣는다"
    click pos (640,600) until screen "r13_recommended_cards" timeout 100
    click '사건 3'
    click '자료 · 현장'
    click '장작창고 현장'
    click '사람이 지나는 뜯긴 벽'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 3'
    click '인물'
    click '선생님'
    click '선생님 · M–W 한 차례 왕복'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 3'
    click '자료 · 현장'
    click '빨래터 통과 주둥이'
    click 'W에 남은 통과 맞는 주둥이 조각'
    click pos (640,600) until screen 'r13_rec_e3_route_map' timeout 100
    screenshot "recommended-e3-02-proposed-sightline-map.png"
    click "L"
    click pos (640,600) until screen "r13_rec_e3_route_map" timeout 60
    assert eval (r13_recommended["episodes"]["3"]["map_step"]==0)
    click 'W'
    click pos (640,600) until screen 'r13_rec_e3_route_map' timeout 100
    click 'L'
    click pos (640,600) until screen 'r13_rec_e3_route_map' timeout 100
    click '큰아이 · L–M'
    click pos (640,600) until screen 'r13_rec_e3_route_map' timeout 100
    click '선생님 · M–W'
    click pos (640,600) until screen 'r13_rec_e3_route_map' timeout 100
    click pos (656,428)
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 3'
    click '인물'
    click '누비'
    click '누비 · 통 소유와 대여 주장'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    assert eval (r13_recommended["episodes"]["3"]["verdict"]=="partial_geometry_unverified")
    assert eval (r13_recommended["episodes"]["3"]["kkomi"]=="alive" and r13_recommended["e3_school_handoff"])
    screenshot "recommended-e3-03-honest-partial-result.png"
    $ r13_qa_note("recommended_ep3_prevention_map: admin action harness for actual school handoff and safe branch; native evidence and map clicks, wrong can endpoint rejected; default production geometry gate remains closed. This is not proof of actual sightline art.")
