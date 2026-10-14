# 활동 방향 제작 인계 · 최신 main bc0359b 기준

시간표·장소를 새로 만들지 않는다. `pose-location-review.csv`는 기존 주간 시간표와 기존 사건/보호 분기의 인물·장소 조합이다. 중립 대체나 우체국/식당의 강제 중립 처리가 있는 행을 먼저 검토한다. `pose-source-inventory.json`에 현재 pose_id·방향·접촉점과 기존 calendar action 원문을 넣었다. 원문은 요구 근거이며 모든 문장마다 새 그림을 만들라는 뜻은 아니다.

## 우선 제작/대조할 pose_id

아래 신규 이름은 **제안 ID**이며 아직 게임에 구현되거나 새 자산으로 승인된 상태가 아니다. 현재 ID와 혼동하지 않는다. 한 활동 자세에서 말 걸면 플레이어를 보는 자세로 1회 전환하고 정지한다. 기존 정면 대화 전신/프로필 43종을 우선 재사용한다.

| 인물/장소 | 현재 ID | 필요한 활동 방향/대상 | 신규 제안 ID |
|---|---|---|---|
| 까로/입구 | action_1(left, sorting), action_2(left, portable_crate) | 마차 축 점검·바퀴 옆 공구·짐 묶기. 현재 정리 자세가 축 수리까지 나타낸다고 간주하지 않음 | world_gate_axle_check_left, world_gate_tie_luggage_left, world_gate_sort_tools_left |
| 문지기/입구 | action_1(right, held_ledger), check_records_low | 초소 서류를 내려다보기 → 플레이어 정면 | world_gate_records_down, world_gate_records_listen_front |
| 할머니/접수대 | world_counter_wipe(front-right-threequarter) | 이미 있는 접수대 앞판 접촉을 유지. 손/행주가 실제 앞판에 닿아야 함 | 기존 world_counter_wipe 우선 재사용; 필요 시 world_inn_counter_listen_front |
| 부리/공방 | action_1(right, tool), action_2(right, kneeling) | 기존 작업대/도면/부품 방향. 달력의 도면 검토와 무릎 작업을 구분 | world_workshop_plan_read_right, world_workshop_parts_kneel_right |
| 세련/우체국 | chair_read(rear_left), chair_listen(rear_left), action_1(right, clipboard) | 새 배경의 실제 창가 의자·책상 방향에 맞춘 읽기. chair_listen은 메타데이터상 rear_left이므로 정면 시선 보장 안 됨 | world_post_letter_read_seated, world_post_letter_listen_front |
| 도토/광장·복도 | world_bulletin_back(back-right), action_1/2 | 광장 게시판을 보는 뒤태 유지. 복도에서 문/메모를 확인하는 활동과 분리 | 기존 world_bulletin_back; world_hall_notes_read, world_hall_listen_front |
| 나비/식당·접수대·학교 | action_1(rear, bucket), action_2(left, tray) | 식당의 실제 식탁 닦기/쟁반 나르기. 학교에서는 기존 피난 활동만 | world_dining_table_wipe, world_dining_tray_carry_left |
| 밤이/복도·접수대 | action_1(front, hanging), action_2(left, floor_sit) | 실제 들보 발 접촉, 바닥에 앉기, 기존 보호 분기의 문 살피기. 숨는 상태를 드러내지 않음 | world_hall_beam_hang, world_inn_seated_listen_front |
| 엄마/온실 | action_1(right, kneeling), action_2(right, floor_sit) | 기존 식물/도구 위치와 무릎 작업 방향 일치 | world_greenhouse_plant_check_right |
| 너울/입구·보호시설 | action_1(rear, notebook), action_2(left, stool) | 기존 명부/교대 메모를 보는 자세, 말 걸 때 정면 | world_facility_register_read, world_facility_listen_front |
| 피코/광장·진료실 | living_paint(right-profile); 진료실은 distressed | 작은 그림판으로 시선/붓끝 정렬. 진료실에서 그림 작업으로 대체하지 않음 | 기존 living_paint 우선; world_square_paint_listen_front |
| 토리/광장·여관·학교 | world_bench_left, activity | 실제 벤치 위치를 쓰는 광장 자세와 실내 대기 자세 구분 | 기존 world_bench_left; world_inn_wait_seated_front |

## 전 주민 공통 납품 정보

- 투명 RGBA, 전신 발끝 포함, 몸·얼굴·부속품을 임의로 분리하지 않은 정지 원본. 단순 좌우 반전 금지.
- person_id, pose_id, 대응 location, 기존 활동/분기 근거, facing, crop, head, foot, hand/seat/hook 필요 지점, 의도한 접촉 대상, 가림 앞뒤.
- 소품이 그림에 포함되는지 명시. 그림 속 의자·탁자와 배경 의자·탁자가 이중으로 생기지 않아야 한다.
- 장소마다 등장하는 실제 시간표는 그대로 유지. CSV에서 중립 대체로 표시된 방문 주민도 기존 행동 원문에 맞는 자세가 필요하지만 새로운 직무/일정은 추가하지 않는다.
- 세로 화면의 작은 글씨/터치 영역은 UI 배치 문제다. 추가 아트가 필요한 문제가 아니다.

입구 첫 가로 배경은 2048×768을 동일 비율 1920×720의 월드로 사용한다. 마차는 왼쪽, 규칙 게시판은 중앙 왼쪽, 서류 초소는 오른쪽이다. 다른 장소의 정확한 방향·발/손 위치는 배경별 대조 이후 확정하며 전체 이미지를 임의 반전해 맞추지 않는다.
