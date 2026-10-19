# Generated native fixtures. Administrator direct-entry seeds prior M2 and Piko-safe.
# Earlier gameplay is not tested by these fixtures. All episode actions and inference clicks are real.
# Native execution/screenshots are still required; do not present source generation as a passed playtest.

testcase recommended_ep4_structure_and_prevention:
    pause 2.0
    $ r13_rec_admin_harness=True
    run Call("r13_recommended_ep4_admin")
    click pos (640,600) until screen "r13_recommended_actions" timeout 80
    click '식기를 돌려놓으며 아빠와 함께 복도를 지난다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '나비에게 여는 방법을 물어 부리와 즉시 구조한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click "오늘을 마친다"
    click "다음 날로 간다"
    click pos (640,600) until screen "r13_recommended_actions" timeout 80
    click '나비에게 7일의 열기와 닫기를 따로 묻는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '서리에게 구조된 피해자의 회복과 손상을 확인한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '부리와 빈 작업칸의 문·레버를 안전하게 시험한다'
    click pos (640,600) until screen "r13_rec_e4_layout" timeout 80
    screenshot "recommended-e4-layout.png"
    click "P · 작업칸 쪽"
    click pos (640,600) until screen "r13_rec_e4_layout" timeout 80
    assert eval ("e4_card_lever" not in r13_recommended["facts"])
    click "R · 객실 쪽"
    click pos (640,600) until screen "r13_rec_e4_layout" timeout 80
    click "L 올리기"
    click pos (640,600) until screen "r13_rec_e4_layout" timeout 80
    click "L 끝까지 내리기"
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '따닥이 너울 앞에서 설명하는 내일 실측을 듣는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click "오늘을 마친다"
    click "다음 날로 간다"
    click pos (640,600) until screen "r13_recommended_actions" timeout 80
    click '레버를 고정하고 공개 동행·출입 감시까지 배치한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '나비와 작업 시작의 빈 칸·열린 문·출입선을 확인한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '따닥의 실제 실측과 안전 결과를 확인한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    assert eval (r13_recommended["episodes"]["4"]["victim"]=="recovering" and r13_recommended["episodes"]["4"]["day9"]=="prevented")
    click "오늘을 마친다"
    click "다음 날로 간다"
    click pos (640,600) until screen "r13_recommended_actions" timeout 80
    click "공개 회의"
    click pos (640,600) until screen "r13_recommended_cards" timeout 80
    click '사건 1'
    click '인물'
    click '피코'
    click '피코 · 오늘 밤의 계획'
    click pos (640,600) until screen "r13_recommended_cards" timeout 80
    assert eval (r13_recommended["episodes"][str(r13_recommended["episode"])]["hearing"]==0)
    click '사건 4'
    click '인물'
    click '아빠'
    click '아빠 · 동행 또는 기다림 확인'
    assert screen "r13_rec_e456_pick"
    click '아빠가 객실 쪽에서 다람과 함께 있던 때'
    assert screen "r13_rec_e456_pick"
    click '다람은 판자문 바깥 객실에서 도움을 청했다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 4'
    click '인물'
    click '다람'
    click '다람 · 7일 객실 R에서의 구조 요청'
    assert screen "r13_rec_e456_pick"
    click '7일 판자문 너머에서 들은 문을 열어 달라는 말'
    assert screen "r13_rec_e456_pick"
    click '다람이 왔을 때 할아버지는 살아 있었다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 4'
    click '인물'
    click '서리'
    click '서리 · 발견과 진료 경과'
    assert screen "r13_rec_e456_pick"
    click '살아 있던 구조 요청부터 늦게 문을 연 뒤까지'
    assert screen "r13_rec_e456_pick"
    click '다친 채 추운 칸에 갇혀 구조가 늦어졌다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 4'
    click '자료 · 현장'
    click '13호 개폐 장치'
    click '13호 개폐 장치 · R / G / P / K'
    assert screen "r13_rec_e456_pick"
    click '관리 칸 레버를 올리자 판자문이 열린 연결'
    assert screen "r13_rec_e456_pick"
    click '관리 칸에서 안쪽 문을 열고 잠글 수 있다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 4'
    click '인물'
    click '나비'
    click '나비 · 7일의 두 짧은 개폐 관찰'
    assert screen "r13_rec_e456_pick"
    click '7일 업무 인계 때 너울이 직접 열고 닫은 때'
    assert screen "r13_rec_e456_pick"
    click '너울은 그날 직접 레버로 문을 열었다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 4'
    click '인물'
    click '너울'
    click '너울 · 7일 책임을 묻는 대상'
    assert screen "r13_rec_e456_pick"
    click '직접 문을 연 일과 살아 있다는 보고 뒤 못 연다고 한 답'
    assert screen "r13_rec_e456_pick"
    click '열 줄 알면서 살아 있는 사람의 구조를 막았다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    assert eval (r13_recommended["neoul"]=="detained" and "e4_card_nabi9" not in r13_recommended["facts"])
    screenshot "recommended-e4-survival-and-detention.png"

testcase recommended_ep5_prevention:
    pause 2.0
    $ r13_rec_admin_harness=True
    run Call("r13_recommended_ep5_admin")
    click pos (640,600) until screen "r13_recommended_actions" timeout 80
    click '학교의 점검 공지와 실제 남는 난방 공간을 확인한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click "오늘을 마친다"
    click "다음 날로 간다"
    click pos (640,600) until screen "r13_recommended_actions" timeout 80
    click '배식 전 두 냄비의 몸체·뚜껑·원래 몫을 살펴본다'
    click pos (640,600) until screen "r13_rec_e5_pots_screen" timeout 80
    screenshot "recommended-e5-pots-original.png"
    click "몸체: 깨진 귀"
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '서리에게 보관약과 선생님의 요청을 묻는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '서리와 약장을 잠그고 선생님에게 실제 학교 자리를 보여 준다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '정상 냄비를 확인하고 아이들과 저녁을 먹는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click "오늘을 마친다"
    click "다음 날로 간다"
    click pos (640,600) until screen "r13_recommended_actions" timeout 80
    click "공개 회의"
    click pos (640,600) until screen "r13_recommended_cards" timeout 80
    click '사건 1'
    click '인물'
    click '피코'
    click '피코 · 오늘 밤의 계획'
    click pos (640,600) until screen "r13_recommended_cards" timeout 80
    assert eval (r13_recommended["episodes"][str(r13_recommended["episode"])]["hearing"]==0)
    click '사건 5'
    click '인물'
    click '서리'
    click '서리 · 약장 안의 보관약'
    assert screen "r13_rec_e456_pick"
    click '안의 용기를 확인한 뒤 잠근 약장'
    assert screen "r13_rec_e456_pick"
    click '약이 나가기 전에 계획을 멈췄다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 5'
    click '자료 · 현장'
    click '학교의 실제 자리'
    click '학교 점검 · 실제 계속 쓸 자리'
    assert screen "r13_rec_e456_pick"
    click '난로 한 대 점검과 지금 쓸 수 있는 교실'
    assert screen "r13_rec_e456_pick"
    click '현재 쓰는 교실에서 계속 아이들을 돌볼 수 있다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    assert eval (r13_recommended["episodes"]["5"]["event"]=='prevented')
    assert eval (r13_recommended["neoul"]=="detained")
    screenshot "recommended-e5-prevented.png"

testcase recommended_ep5_body_lid_target:
    pause 2.0
    $ r13_rec_admin_harness=True
    run Call("r13_recommended_ep5_admin")
    click pos (640,600) until screen "r13_recommended_actions" timeout 80
    click "오늘을 마친다"
    click "다음 날로 간다"
    click pos (640,600) until screen "r13_recommended_actions" timeout 80
    click '배식 전 두 냄비의 몸체·뚜껑·원래 몫을 살펴본다'
    click pos (640,600) until screen "r13_rec_e5_pots_screen" timeout 80
    screenshot "recommended-e5-pots-original.png"
    click "몸체: 깨진 귀"
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '서리에게 보관약과 선생님의 요청을 묻는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '배식 자리로 돌아가 이상을 확인하고 즉시 돌봄을 인계한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '치료실에서 보리에게 순서와 위치를 묻는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '새미에게 약이 아니라 두 뚜껑을 덮은 사람을 묻는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '서리·보리와 실제 반출 용기와 인계 구간을 대조한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click "오늘을 마친다"
    click "다음 날로 간다"
    click pos (640,600) until screen "r13_recommended_actions" timeout 80
    click '서리에게 아이 돌봄을 인계하고 보리와 회의에 간다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click "공개 회의"
    click pos (640,600) until screen "r13_recommended_cards" timeout 80
    click '사건 1'
    click '인물'
    click '피코'
    click '피코 · 오늘 밤의 계획'
    click pos (640,600) until screen "r13_recommended_cards" timeout 80
    assert eval (r13_recommended["episodes"][str(r13_recommended["episode"])]["hearing"]==0)
    click '사건 5'
    click '자료 · 현장'
    click '두 냄비와 뚜껑'
    click '두 냄비 · 고정 몸체와 이동 뚜껑'
    assert screen "r13_rec_e5_pots_screen"
    screenshot "recommended-e5-pots-swapped.png"
    click "몸체: 깨진 귀"
    assert screen "r13_rec_e456_pick"
    click '뚜껑을 내려도 남는 깨진 귀'
    assert screen "r13_rec_e456_pick"
    click '아침에 순찰대에게 남겨 달랬던 몸체다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 5'
    click '인물'
    click '보리'
    click '보리 · 원래 요청·혼입 위치·배식'
    assert screen "r13_rec_e456_pick"
    click '같은 깨진 귀 냄비에 붓는 모습과 앞선 순찰대 몫 요청'
    assert screen "r13_rec_e456_pick"
    click '선생님이 약을 넣은 몸체는 원래 순찰대 몫이었다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 5'
    click '자료 · 현장'
    click '두 냄비와 뚜껑'
    click '두 냄비 · 고정 몸체와 이동 뚜껑'
    assert screen "r13_rec_e456_pick"
    click '몸체는 두고 두 뚜껑만 아침 자리로 돌린다'
    assert screen "r13_rec_e456_pick"
    click '바뀐 그림을 따라 원래 순찰대 냄비에서 아이들에게 떴다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 5'
    click '인물'
    click '새미'
    click '새미 · 두 뚜껑과 앞문'
    assert screen "r13_rec_e456_pick"
    click '선생님이 두 뚜껑을 덮을 때 앞문에서 물을 주던 보리'
    assert screen "r13_rec_e456_pick"
    click '마지막으로 두 뚜껑을 덮은 사람은 선생님이다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 5'
    click '자료 · 현장'
    click '반출 약통'
    click '반출 약통 · 동일 용기의 인계'
    assert screen "r13_rec_e456_pick"
    click '목테 흠집과 진료실 앞부터 학교까지 함께 온 인계'
    assert screen "r13_rec_e456_pick"
    click '서리가 알던 내용물과 보리가 본 붓는 행동이 같은 통으로 이어진다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 5'
    click '인물'
    click '선생님'
    click '선생님 · 요청과 행동의 책임'
    assert screen "r13_rec_e456_pick"
    click '순찰대 몫에 넣은 약과 마지막으로 덮은 두 뚜껑'
    assert screen "r13_rec_e456_pick"
    click '선생님의 약 넣기와 뚜껑 바꾸기가 아이들 배식으로 이어졌다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    assert eval (r13_recommended["episodes"]["5"]["event"]=='contaminated')
    assert eval (r13_recommended["neoul"]=="detained")
    screenshot "recommended-e5-responsibility.png"

testcase recommended_ep6_actual_protection:
    pause 2.0
    $ r13_rec_admin_harness=True
    run Call("r13_recommended_ep6_admin")
    click pos (640,600) until screen "r13_recommended_actions" timeout 80
    click '현재 학교 배분판의 판돌 제외 칸과 적용일을 읽는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '현재 출발 명단의 날짜와 다음 인계 항목을 읽는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '학교에 남은 판돌에게 현재 보호와 실제 출발을 묻는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '나비에게 7일 요청과 12일 수령을 구분해 묻는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '뭉치에게 같은 자리의 지시와 실제 포장을 묻는다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '촌장·바둑이·실룩과 현재 승객을 보호하며 출발을 멈춘다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '바둑이·촌장과 제단의 실제 돌봄 인계를 확인한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '엄마 연구 원본을 실제 조각·공동 난로·공간과 대조한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '검증한 난로를 점검하고 오늘의 공동 공간을 가동한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '학교 책상을 옮기고 승객 세 사람의 실제 자리를 편다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '나비·뭉치와 실제 남은 재료로 세 사람의 식사를 준비한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '서리와 나비의 실제 돌봄 교대와 연락을 맞춘다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '실룩·바둑이와 환자가 탈 실제 이동길을 점검한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click "오늘을 마친다"
    click "다음 날로 간다"
    click pos (640,600) until screen "r13_recommended_actions" timeout 80
    click "공개 회의"
    click pos (640,600) until screen "r13_recommended_cards" timeout 80
    click '사건 1'
    click '인물'
    click '피코'
    click '피코 · 오늘 밤의 계획'
    click pos (640,600) until screen "r13_recommended_cards" timeout 80
    assert eval (r13_recommended["episodes"][str(r13_recommended["episode"])]["hearing"]==0)
    click '사건 6'
    click '자료 · 현장'
    click '학교 배분판'
    click '학교 배분판 · 7일 결정 / 12일 적용'
    assert screen "r13_rec_e456_pick"
    click '판돌의 외부 보호 완료 칸과 12일 적용일'
    assert screen "r13_rec_e456_pick"
    click '이미 다른 곳에서 보호받는 사람처럼 학교 몫에서 빠졌다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 6'
    click '자료 · 현장'
    click '출발 명단'
    click '출발 명단 · 판돌 13일 저녁 / 제단 인계'
    assert screen "r13_rec_e456_pick"
    click '13일 저녁 출발과 12일부터 빠진 학교 몫'
    assert screen "r13_rec_e456_pick"
    click '학교에 남아 먹어야 할 동안 몫이 먼저 끊겼다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 6'
    click '인물'
    click '나비'
    click '나비 · 7일 요청 / 12일 실제 수령'
    assert screen "r13_rec_e456_pick"
    click '7일 인계 자리에서 13일 저녁까지의 식사를 부탁한 때'
    assert screen "r13_rec_e456_pick"
    click '제외가 적용되기 전에 남을 기간과 식사 필요를 들었다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 6'
    click '인물'
    click '뭉치'
    click '뭉치 · 직접 지시와 실제 적용'
    assert screen "r13_rec_e456_pick"
    click '같은 자리에서 받은 제외 지시와 그 기준대로 한 포장'
    assert screen "r13_rec_e456_pick"
    click '할머니가 빼라고 했고 뭉치가 그 말대로 포장했다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 6'
    click '자료 · 현장'
    click '출발 명단'
    click '출발 명단 · 판돌 13일 저녁 / 제단 인계'
    assert screen "r13_rec_e456_pick"
    click '제단 목적지와 식사·숙소를 다시 맡기는 항목'
    assert screen "r13_rec_e456_pick"
    click '제단이라는 이름만으로 생활 보호가 이어졌다고 할 수 없다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 6'
    click '인물'
    click '바둑이'
    click '바둑이 · 제단의 실제 인계 확인'
    assert screen "r13_rec_e456_pick"
    click '돌 앞에 사람을 두는 자리와 돌봄·식사·잠자리 인계의 부재'
    assert screen "r13_rec_e456_pick"
    click '확인한 인계는 사람을 먹이고 재우는 보호소 인계가 아니다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '메인'
    click '자료 · 현장'
    click '엄마 연구 원본'
    click '엄마 연구 원본'
    assert screen "r13_rec_e456_pick"
    click '새 희생 없이 현재 난로와 교실에서 확인한 시간'
    assert screen "r13_rec_e456_pick"
    click '확인하고 준비한 이 공간에서는 오늘을 버틸 다른 길이 있다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 6'
    click '자료 · 현장'
    click '학교의 실제 자리'
    click '학교 · 오늘 보호할 실제 준비'
    assert screen "r13_rec_e456_pick"
    click '펴 놓은 세 자리·준비한 세 식사·두 담당자·확인한 이동길'
    assert screen "r13_rec_e456_pick"
    click '확인한 세 사람의 식사와 잠자리와 돌봄을 오늘 넘길 수 있다'
    click pos (640,600) until screen 'r13_recommended_cards' timeout 100
    click '사건 6'
    click '인물'
    click '할머니'
    click '할머니 · 7일 식사 요청을 들은 사람'
    assert screen "r13_rec_e456_pick"
    click '판돌이 남는다는 부탁 뒤에도 몫을 빼라는 지시'
    assert screen "r13_rec_e456_pick"
    click '남아 있는 줄 알면서 끊은 몫을 돌려놓아야 한다'
    click pos (640,600) until screen 'r13_recommended_actions' timeout 100
    assert eval (not r13_recommended["episodes"]["6"]["today_sacrifice_stopped"])
    screenshot "recommended-e6-proof-not-yet-handoff.png"
    click '촌장의 철회와 바둑이의 강행 준비 해제를 직접 확인한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '배분판을 바로잡고 실제 식사·잠자리·돌봄을 인계한다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '다음 보호 인계 전 지원을 끊지 못하도록 업무를 나눠 맡긴다'
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    click '가족의 현재 상태를 확인하고 학교의 첫 밤을 함께 보낸다'
    click pos (640,600) until screen "choice" timeout 80
    click "오늘은 학교에 함께 남는다"
    click pos (640,600) until screen "r13_recommended_actions" timeout 100
    assert eval (r13_recommended["episodes"]["6"]["verdict"]=="complete_today" and r13_recommended["episodes"]["6"]["today_sacrifice_stopped"])
    assert eval (r13_recommended["mother"]=="M2" and r13_recommended["neoul"]=="detained")
    screenshot "recommended-e6-first-night.png"
    $ r13_qa_note("recommended_ep456: direct-entry fixture seeds prior history; episode actions, layout/pot clicks, card/part/conclusion, survival prevention and actual cancellation/handoff are native UI-tested only if this testcase has passed.")
