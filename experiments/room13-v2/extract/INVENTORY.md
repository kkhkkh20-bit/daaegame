# 다람탐정 v111 전체 지도 (1~14일) — 추출 1단계

2026-10-30. 지금 게임(`experiments/renpy-ch1/game`)을 **실행하지 않고** 파일만 읽어 만든 지도다. 기계가 읽는 같은 내용은 `inventory.json`.

## 읽는 법

- 흐름 시작: `start` → `room13_start` → `r13_v111_start` → 마차(`r13_carriage_departure`) → `r13_v111_start_block`. 시작에서 닿는 label 856개(정적 분석). 닿지 않는 v111 label: `r13_v111_crowd_block_old13`, `r13_v111_crowd_failed13`, `r13_v111_shelter_choice`, `r13_v111_shelter_work`, `r13_v111_today6`, `r13_v111_permission_today6`, `r13_v111_acorn_recover6`, `r13_v111_acorn_recovered6`.
- 장면 순서: 원본 장면표(`docs/story-ms14/source/다람탐정_제작기준본01_대사연출조건.json`) 순서. `P`·`A`·`B`·`C`·`END` 는 같은 날의 대체 갈래(예방판·다른 결과)다. label 의 장면은 그 label 안 마지막 `r13_v111_scene`, 없으면 데려온 label 의 장면(실행 중 실제와 다를 수 있다).
- 대사 세 곳의 합: 원문 `v111/records.json` → 날짜 패치 `v111/newworld/dNN.json`(replace/before/after/drop/blocks/titles/evidence) → rpy 안 직접 쓴 줄. 「펼친 줄」은 before/after 를 더하고 늘 삭제되는 줄을 뺀 수(조건 줄 포함).
- 대기 관문 = `r13_v111_wait(key)`: 조사 화면(`r13_hub`)에서 인물·물건·지도를 눌러 고르는 자리. 선택지는 `v111/field-bindings.json`(제목은 dNN `titles` 로 덮임), guard 가 맞을 때만 보인다. 「간다」 = 고르면 실행되는 것.
- 「1일 입구(gate)」 회의는 기회 무제한(`R13_NW_UNLIMITED`)이라 짐(lose) 갈래와 `gate_last_try` 줄은 실제로 닿지 않는다.
- `MS14_D07_P01`·`MS14_D07_P02` 는 원본 장면표에만 있고 rpy 에서 쓰지 않는다.

## 날짜별 장면 한눈에

| 날 | 장면 | 제목 | 원본 시간·장소 | 실제 장소(이동) | 화자 | 대기 관문 | 회의 | 얻는 자료 | 음악 / 환경음 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `D01_S01` | 1. 마차 / 엄마 몫 | 1일 낮 / 움직이는 마차 | gate | 다람, 아빠, 까로, 돌목 |  |  | E01 | bgm-travel.mp3 / wind |
| 1 | `D01_S02` | 2. 초소 / 한 사람의 허가 | 1일 도착 / 초소 입구→내부 | gate | 다람, 아빠, 까로, 돌목 | gate_request, gate_choice, gate_investigate | 함께 들어갈 근거를 고른다 | E02 | bgm-snow.mp3 / wind |
| 1 | `D01_S03` | 3. 초소 / 둘이 들어갈 근거 | 1일 / 초소 첫 추리 |  | 다람, 아빠, 돌목 |  |  | E03, E04 | bgm-snow.mp3 / wind |
| 1 | `D01_S04` | 4. 문이 열릴 때 / 이름 | 1일 / 초소 등록 후 입장 | gate | 다람, 돌목, 아빠, 너울 | registered_menu |  | E05 | bgm-snow.mp3 / wind |
| 1 | `D01_S05` | 5. 여관 13호 / 기다리지 않는 방 | 1일 저녁 / 로비→빈13호→밤 | inn, room13 | 할머니, 다람, 아빠 | note_pick, bundle_open, sleep1 | 두 편지를 나란히 본다 | E06, E30 | bgm-inn.mp3 / fire |
| 2 | `D02_S01` | 1. 광장 / 초롱의 손 | 2일 아침 / 마구간→등→북쪽 교환함 | gate, square, forest | 아빠, 까로, 촌장, 다람, 초롱 | lamp_rope, go_box, box_inspect, box_note |  |  | bgm-snow.mp3 / wind |
| 2 | `D02_S02` | 2. 우체국 / 내 편지부터 | 2일 낮 / 우체국 | post | 세련, 아빠, 다람, 모모 | envelope_show, post_menu |  | E07 | bgm-village.mp3 / wind |
| 2 | `D02_S03` | 3. 3번 등 / 초상 의뢰 | 2일 오후 / 3번등 화가 자리 | square | 모모, 피코, 아빠, 다람, 초롱 | portrait_ask, lamp_observe |  | NW_PIKO_TREMOR, E08 | bgm-village2.mp3 / wind |
| 2 | `D02_S04` | 4. 식당 / 부탁은 자리가 되기까지 | 2일 해지기 전 한 번의 기회 / 식당↔북쪽길 | dining, square, forest, inn, room13 | 아빠, 나비, 다람, 초롱, 피코, 네로, 할머니 | afternoon2, shelter_enter, nero_work |  | E31, E35 | bgm-inn.mp3 / fire |
| 2 | `D02_S05` | 5. 여관 / 설명할 수 없는 빈칸 | 2일 밤 / 여관 로비→13호 | inn, room13 | 할머니, 아빠, 다람, 초롱 | sleep2, lamp_prep2 |  |  | bgm-inn2.mp3 / wind |
| 3 | `D03_S01` | 1. 아침 / 두 가지 약속의 끝 | 3일 새벽~아침 / 광장 사망 또는 식당 생존 | square, dining | 피코, 다람, 아빠, 초롱, 나비, 톡, 실룩, 백 부인 | lamp_attempt_field3, piko_clean |  | E09, NW_LA_CHECK, NW_LA_FIELD, NW_LA_KNIFE, NW_LA_OFFER, NW_INNER_PRICE, NW_KEEPER_DATE, E09 | bgm-night.mp3 / wind |
| 3 | `D03_S02` | 2. 광장 / 먼저 묶인 손 | 3일 아침 / 3번등 공개 조사 | square | 아빠, 까로, 다람, 실룩, 너울, 톡, 초롱 | lamp_inspect3, fragment_request, lamp_log_request |  | E10, E32, E11 | bgm-search.mp3 / wind |
| 3 | `D03_S03` | 3. 공방과 진료소 / 돌려놓았다는 말 | 3일 오전 / 공방→진료소 | workshop, clinic | 부리, 아빠, 우박, 다람, 부엉이 | loan_read, measurement_read | 측정 종료와 점검 기록을 대조한다 | E12, E13 | bgm-think.mp3 / clock |
| 3 | `D03_S04` | 4. 짐 내리는 골목 / 식구의 빵 | 3일 낮 / 골목→허락된 창고→공개확인 | square, store, workshop | 실룩, 다람, 실룩의 아이, 아빠, 백 부인, 톡, 부리 | transport_read, knife_permission, store_visit, stone_check, sale_check |  | E14, E15, E16, NW_INNER_PRICE, NW_KEEPER_DATE | bgm-search.mp3 / wind |
| 3 | `D03_S05` | 5. 광장 공방 / 무엇을 증명했는가 | 3일 오후 / 등 앞 공방 | workshop, square | 아빠, 너울, 바둑이, 실룩, 초롱, 톡, 백 부인, 부엉이, 다람 | restore_input | 수리 뒤 새로 생긴 파손을 가린다 / 남아 있는 돌과 칼의 사용을 연결한다 / 수리와 반출을 가릴 자료를 낸다 / 돌과 매입 기록을 낸다 / 바깥 걸쇠 주장과 발견 위치를 대조한다 / 마지막 점검과 인수한 돌을 연결한다 | E33, E17 | bgm-council.mp3 /  |
| 3 | `D03_S06` | 6. 저녁 / 그려지지 않은 얼굴 | 3일 저녁 / 등 복구·초상·물자인수 | square, room13, clinic | 초롱, 아빠, 다람, 네로, 톡, 피코 | blankets_receive, sleep3 |  |  | bgm-village.mp3 / wind |
| 4 | `D04_S01` | 1. 솜이네 골목 / 닫힌 뒷문 | 4일 아침 / 조건부노동현장→솜이네문 | v111_labor, ms14_somi | 아빠, 너울, 실룩, 네로, 솜이, 다람, 아랫길 노인 | labor_sheet4, portrait_show4, nero_help4 |  | E34, E18, E31 | bgm-village2.mp3 / wind |
| 4 | `D04_S02` | 2. 처마 / 도토리 세 개 | 4일 낮 / 광장처마→오후방문후퇴 | square, ms14_somi | 콩이, 다람, 토실, 아빠, 밤이, 네로, 초롱 | portrait_place4 |  | E19 | bgm-village.mp3 / wind |
| 4 | `D04_S03` | 3. 저녁 초소 뒤 / 비명 | 4일 저녁 / 초소뒷길 | gate | 돌목, 아빠, 너울, 밤이, 바둑이 | look_gate4 |  | E20 | bgm-pressure.mp3 / wind |
| 4 | `D04_S04` | 4. 같은 밤 / 잘못 적은 키 | 4일 밤 / 밝은초소→문앞울타리→식당 | ms14_guardroom, gate, dining, square, room13 | 아빠, 다람, 밤이, 콩이, 바둑이, 나비, 초롱, 꼬미, 피코 | bami_ask4, inspect_gate4, collect4, sleep4 |  | E21, E22, NW_PIKO_SKETCH4 | bgm-think.mp3 / wind |
| 5 | `D05_S01` | 1. 솜이네 / 손바닥 | 5일 아침 / 솜이네안 | ms14_somi, ms14_somi_inside | 아빠, 네로, 무쇠, 솜이, 다람 |  |  | NW_MUSOE_DEEP | bgm-think.mp3 / wind |
| 5 | `D05_S02` | 2. 문턱 / 숨긴 것과 일어난 것 | 5일 오전 / 솜이네→진료소문→초소 | ms14_somi_inside, clinic | 무쇠, 솜이, 아빠, 네로, 다람, 바둑이, 진료 담당자 | compare_cloth5 |  | E23, E24 | bgm-think.mp3 / wind |
| 5 | `D05_S03` | 3. 초소 / 사라지지 않는 상처 | 5일 낮 / 초소밤이혐의검증 | gate | 콩이, 너울, 다람, 아빠, 돌목, 나비, 네로, 바둑이, 밤이 |  | 밤이 혐의의 근거를 확인한다 | E25, E26 | bgm-council.mp3 /  |
| 5 | `D05_S04` | 4. 점심 무렵 / 이제 도착한 경고 | 5일 점심무렵 / 초소앞바람막힌곳 | gate | 초롱, 아빠, 다람 | envelope5, reply_handoff5 | 두 편지의 초대를 대조한다 | E27, E28 | bgm-think.mp3 / wind |
| 5 | `D05_S05` | 5. 저녁 / 맡긴다는 말의 무게 | 5일 저녁 / 솜이네→식당→같은복도→13호 | ms14_somi_inside, dining, inn, hall, room13 | 솜이, 다람, 아빠, 무쇠, 네로, 바둑이, 까로, 나비, 너울, 할머니, 종업원, 부엉이, 누비 | laundry5, lock_check5, sleep5 |  | E29, NW_LAUNDRY_TALK | bgm-inn2.mp3 / fire |
| 6 | `D06_S01` | 6-1. 오전 / 학교 뒤문 — 엄마에게 갈 물건 | ["SCHOOL_REAR", "INN_REAR"] | school, dining | 다람, 할머니, 아빠, 초롱, 사자 선생님, 꼬미, 나비, 밤이, 콩이, 판돌 | board6, hp_meal6 |  | E06_CONTACT | bgm-inn2.mp3 / fire |
| 6 | `D06_S02` | 6-2. 오후 / 장작 창고 — 안전한 곳이라는 말 | ["WOODSHED", "SCHOOL_REAR"] | v111_woodshed, school | 꼬미, 다람, 아빠, 보리, 도담, 도토, 창고 아이 1, 창고 아이 2, 창고 아이 3, 사자 선생님 | woodshed_check6, afternoon6, handoff6 |  | NW_KKOMI_NOSTONE | bgm-search.mp3 / wind |
| 6 | `D06_S03` | 6-3. 해 질 무렵 / 창고 바깥 — 먼저 꺼낼 것 | ["WOODSHED"] | v111_fire, school | 다람, 보리, 아빠, 꼬미 | wet_cloth6, clear_wood6 |  |  | bgm-pressure.mp3 / fire |
| 6 | `D06_S04` | 6-4. 밤 / 학교 난로 곁 — 세 가지 잘못 | ["SCHOOL_ROOM", "WOODSHED"] | school, v111_ruin | 나비, 아빠, 너울, 보리, 도담, 도토, 꼬미, 다람 | fire_evidence6, sleep6_input |  | E06_EMPTY, E06_RESCUE, E06_FIRE | bgm-night.mp3 / wind |
| 6 | `D06_P01` | D06_P01 — 오늘 옮기는 경로 | ["SCHOOL_ROOM"] |  | 아빠, 사자 선생님 |  |  |  | bgm-inn2.mp3 / fire |
| 6 | `D06_S03P` | D06_S03P — 빈 창고의 불 | ["WOODSHED", "SCHOOL_ROOM"] | v111_fire | 보리, 아빠 |  |  |  | bgm-pressure.mp3 / fire |
| 7 | `D07_S01` | 7-1. 오전 / 빨래터 — 내 아이들 몫 | ["LAUNDRY"] | laundry, school | 누비, 아빠, 보리, 아이, 나비, 너울, 다람, 누비의 막내 | nubi_children_receipt7, bori_witness7 | 불이 시작된 곳과 진술을 대조한다 | E07_NUBI, NW_NUBI_TICKET | bgm-think.mp3 / wind |
| 7 | `D07_S02` | 7-2. 낮 / 회관에서 학교까지 — 남은 사람의 자리 | ["HALL", "SCHOOL_ROOM"] | school | 너울, 아빠, 누비, 보리, 나비, 사자 선생님, 창고 아이 1, 창고 아이 2, 창고 아이 3, 누비의 큰아이, 누비의 둘째, 누비의 막내, 도토, 다람, 초롱, 꼬미, 도담, 부리, 톡, 판돌, 판설 | school_names7, free_day7 | 불의 원인과 빈 창고 진압을 구분한다 / 불의 원인과 아이 구조를 구분한다 | NW_STONE | bgm-inn2.mp3 / fire |
| 7 | `D07_S03` | 7-3. 저녁 / 여관 13호 — 잠깐이라는 약속 | ["ROOM13", "INN_CORRIDOR"] | room13, school, clinic | 도토, 다람, 아빠, 할머니, 부엉이, 까로, 서리, 톡 | detained_bed7, free_sleep7_input |  |  | bgm-think.mp3 / clock |
| 7 | `D07_S04` | 7-4. 밤 / 초소에서 13호까지 — 열리지 않는 문 | ["SNOW_DETOUR", "OUTPOST", "INN_CORRIDOR", "ROOM13"] | clinic, hall, room13 | 까로, 도토, 아빠, 나비, 다람, 할머니, 너울 |  |  |  | bgm-pressure.mp3 / wind |
| 8 | `D08_S01` | 8-1. 아침 / 보호실 — 듣기 싫은 말 | ["HOLDING_ROOM"] | v111_custody | 서리, 너울, 아빠, 다람 |  |  | E08_CHILD_ACCOUNT | bgm-night.mp3 / wind |
| 8 | `D08_S02` | 8-2. 오전 / 13호 — 없어진 조각의 자리 | ["INN_CORRIDOR", "ROOM13"] | room13 | 부리, 아빠, 할머니, 도토 | room_check8 |  | E08_ROOM, E08_CHILD_POSITION, E08_ROOM_REACH, NW_STONE | bgm-search.mp3 / clock |
| 8 | `D08_S03` | 8-3. 오후 / 진료실 — 부러진 다음 | ["CLINIC"] | clinic | 서리, 아빠, 부리 | tool_faces8, wire_curve8 |  | E08_TOOL, E08_CONTACT_ASSEMBLY, E08_WOUND_WIRE | bgm-think.mp3 / clock |
| 8 | `D08_S04` | 8-4. 해 질 무렵 / 등 관리함 — 혼자 가지 않는 길 | ["LAMP_PATH"] | square, school | 초롱, 아빠, 순찰대원, 바둑이 | escort8, sleep8_input |  | E08_RECENT_LETTER | bgm-snow.mp3 / wind |
| 8 | `D08_P01` | 8-P. 생존 대체 / 다람과 함께 듣는 진료 | ["SCHOOL_ROOM", "CLINIC", "ROOM13"] | room13 | 부엉이, 아빠, 도토, 서리, 다람, 너울 |  |  | NW_STONE | bgm-think.mp3 / clock |
| 9 | `D09_S01` | 9-1. 오전 / 주방과 책장 — 길 하나를 더 세다 | ["INN_KITCHEN", "ROOM13", "PASSAGE"] | kitchen | 따닥, 아빠, 할머니, 부리, 도토, 다람 | safe_passage9, passage_after9 |  | E09_PASSAGE | bgm-dark.mp3 / wind |
| 9 | `D09_S02` | 9-2. 낮 / 공방 — 같은 핀이 아니다 | ["WORKSHOP", "POST_OFFICE"] | workshop | 아빠, 톡, 부리, 세련 |  |  | E09_PIN_OWNER | bgm-search.mp3 / clock |
| 9 | `D09_S03` | 9-3. 오후 / 식당 — 나비가 여민 것 | ["INN_DINING"] | dining | 나비, 아빠, 할머니 | pin_question9, scarf_compare9 |  | E09_PIN_TIME, E09_PIN_HANDOVER_TIME, E09_SCARF | bgm-think.mp3 / fire |
| 9 | `D09_S04` | 9-4. 저녁 / 우체국 — 누가 부쳤는지, 누가 썼는지 | ["POST_OFFICE", "HOLDING_ROOM", "SCHOOL_ROOM"] | post, v111_custody, school | 세련, 아빠, 슬링, 다람 | sleep9_input |  | E09_MAIL | bgm-village.mp3 / wind |
| 9 | `D09_P01` | 9-P. 생존 대체 / 침입과 위조의 갈림길 | ["INN_KITCHEN", "PASSAGE", "ROOM13"] | kitchen, room13 | 따닥, 아빠, 도토, 할머니, 나비, 부엉이 | safe_prevent9, papers_check9 |  | E09_PASSAGE | bgm-dark.mp3 / wind |
| 10 | `D10_S01` | 10-1. 아침 / 회관 대기실 — 아빠 말부터 고치기 | ["HALL_WAITING"] | school | 다람, 아빠, 부리 |  |  |  | bgm-think.mp3 /  |
| 10 | `D10_S02` | 10-2. 오전 / 회관 — 문 하나의 증언 | ["HALL"] | school | 촌장, 아빠, 너울, 다람, 서리, 도토, 나비, 따닥, 할머니, 순찰대원 |  | 두 상처와 촛대 파손을 대조한다 / 두 번째 길을 실제 기록으로 보인다 |  | bgm-council.mp3 /  |
| 10 | `D10_S03` | 10-3. 정오 / 회관 — 세 번의 변명 | ["HALL", "HALL_WAITING"] | school | 아빠, 할머니, 톡, 촌장, 너울, 나비, 도토, 서리, 다람, 부리, 슬링 |  | 구리선과 수선 출처를 대조한다 / 첫 비명 뒤 핀을 다시 채운 때 / 접촉면과 아이의 위치를 대조한다 |  | bgm-council.mp3 /  |
| 10 | `D10_S04` | 10-4. 오후 / 우체국 옆 벤치 — 다음에 갈 곳 | ["POST_BENCH", "SCHOOL_ROOM"] | post, school | 아빠, 다람, 세련, 부리, 나비, 꼬미 | sleep10_input |  | E10_PUMP | bgm-snow.mp3 / wind |
| 10 | `D10_P01` | 10-P. 예방 대체 / 그 종이를 넘기기 전에 | ["HALL", "POST_BENCH"] | school | 부엉이, 할머니, 아빠, 다람, 슬링, 세련, 너울, 서리 | pocket10, private_handoff10 | 수신인과 가족 전달 권한을 구분한다 / 반송·필사본·초대 발송을 대조한다 | E10_PUMP | bgm-council.mp3 /  |
| 10 | `D10_S04P` | 반드시 실장할 짧은 대체 대사 | ["SCHOOL_ROOM"] | school | 다람, 아빠 |  |  |  | bgm-inn2.mp3 / fire |
| 11 | `D11_S00` | 장면 11-0. 셋째 말뚝 아래 | 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 | school, forest | 까로, 아빠, 다람 | pump_open11 |  |  | bgm-snow.mp3 / wind |
| 11 | `D11_S01` | 장면 11-1. 빈 뿌리 집 | 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 | forest, school | 다람, 아빠, 토실, 나비 | root_note11, nabi_wait11, tosil_handoff11 |  |  | bgm-snow.mp3 / wind |
| 11 | `D11_S02` | 장면 11-2. 폐온실의 낮은 문 | 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 | greenhouse | 엄마, 다람, 아빠 |  |  |  | bgm-family.mp3 / wind |
| 11 | `D11_S02A` | 장면 11-2A. 마를 때까지 | 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 | greenhouse | 엄마, 다람, 아빠 |  |  |  | bgm-family.mp3 / wind |
| 11 | `D11_S02B` | 장면 11-2B. 단추 하나 | 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 | greenhouse | 아빠, 엄마, 다람 | mother_questions11 |  |  | bgm-family.mp3 / wind |
| 11 | `D11_S03` | 장면 11-3. 열이 있는 물건 | 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 | facility, school, square, forest | 굴돌, 엄마, 아빠, 다람, 초롱, 나비, 토실, 네로, 아랫길 주민, 선생님, 백 부인, 판돌, 주민, 촌장, 돌목, 부엉이, 까로, 사자 선생님 | heat_check11, family_place_check11, family_space_after_supply11, rescue_cart11, day_rescue_door11 | 초롱과 피코의 하루를 대조한다 / 아르카가 없는 아이들과 대조한다 / 13호 난로의 돌을 내놓는다 / 요즘 돌이 어디서 오는지 대조한다 / 창고에서 잠자는 사람을 짚는다 | NW_TABLET_A, NW_NAMES, NW_SICK_BEDS, E14_SUPPLY | bgm-dark.mp3 / clock |
| 11 | `D11_S04` | 장면 11-4. 문이 열려 있어야 하는 밤 | 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 | school, hidden_pandol, forest | 다람, 엄마, 아빠, 네로, 선생님, 까로, 아랫길 주민, 판돌 | rescue_handoff11, sleep11_input, hp_house11, night_rescue_prepare11, late_supply_handoff11, snow_door11 |  | E14_SUPPLY | bgm-snow.mp3 / wind |
| 12 | `D12_S01` | 장면 12-1. 불러야 할 이름 | 학교 배식실/진료 공간/시설 인수 지점 | school, forest, square | 아빠, 다람, 선생님, 돌목, 서리, 나비, 까로, 네로, 엄마, 사자 선생님 | morning_prep12, carrier_receipt12 |  | NW_TRANSFER_LIST, E14_SUPPLY | bgm-inn2.mp3 / fire |
| 12 | `D12_S02` | 장면 12-2. 배식 전의 손 | 학교 배식실/진료 공간/시설 인수 지점 | school, facility | 도담, 보리, 다람, 나비, 선생님, 새미, 아빠 | meal_inspect12, pickup_box12 |  | NW_WHITE_BOWLS | bgm-inn2.mp3 / fire |
| 12 | `D12_S03` | 장면 12-3. 돌아온 냄비 | 학교 배식실/진료 공간/시설 인수 지점 | school | 보리, 아빠, 나비, 새미, 선생님, 다람 | soup_fragment12 |  |  | bgm-think.mp3 /  |
| 12 | `D12_S04` | 장면 12-4. 같은 것을 먹었다는 말 | 학교 배식실/진료 공간/시설 인수 지점 | school | 백 부인, 아빠, 선생님, 새미, 나비, 서리, 돌목, 너울, 엄마, 다람, 보리 | bottle_match12 | 재사용 설명과 개봉 봉인을 대조한다 / 파편·봉인·취급 구간을 함께 제시한다 / 명단과 흰 그릇을 대조한다 | E12_FRAGMENT, E12_SEAL, E12_HANDLING, NW_RETURNED_BOWL | bgm-think.mp3 /  |
| 12 | `D12_S05` | 장면 12-5. 너무 밝은 창문 | 학교 배식실/진료 공간/시설 인수 지점 | school | 아빠, 선생님, 나비, 새미, 돌목, 너울, 엄마, 보리, 다람 | sleep12_bed_input |  | NW_HALL_WINDOW, NW_PIKO_PAINTING | bgm-night.mp3 /  |
| 12 | `D12_A` | 대체 장면 12-A. 배식 직전 발견 | 학교 배식실/진료 공간/시설 인수 지점 | school | 아빠, 나비, 다람, 선생님 |  |  |  | bgm-think.mp3 /  |
| 12 | `D12_B` | 대체 장면 12-B. 수프 사건이 일어나지 않은 저녁 | 학교 배식실/진료 공간/시설 인수 지점 | school | 선생님, 아빠, 엄마, 아이, 다람, 돌목 | early_bowl12 |  |  | bgm-family.mp3 / fire |
| 13 | `D13_S01` | 장면 13-1. 판돌의 어깨 | 학교/입구 경비실/광장 수레 | school | 판돌, 다람, 아빠, 까로, 엄마, 새미, 나비, 돌목 | blanket_mend13, teacher_relief_check13 |  | E13_MENDING | bgm-inn2.mp3 / fire |
| 13 | `D13_S02` | 장면 13-2. 벤치 한 칸 | 학교/입구 경비실/광장 수레 | gate, square | 돌목, 엄마, 아빠, 다람, 너울, 촌장 |  |  |  | bgm-snow.mp3 / wind |
| 13 | `D13_S03` | 장면 13-3. 아내가 불렀다는 말 | 학교/입구 경비실/광장 수레 | square, school | 아빠, 판돌, 다람, 촌장, 너울, 바둑이, 나비, 피코 | cart_inspect13, departed_bed13 | 아내가 봤다는 담요의 시점을 확인한다 / 촌장이 어젯밤 있던 곳을 확인한다 | NW_PIKO_PAINTING | bgm-pressure.mp3 / wind |
| 13 | `D13_S04` | 장면 13-4. 바퀴가 멎어도 | 학교/입구 경비실/광장 수레 | square, school, v111_supervised, v111_labor | 바둑이, 너울, 아빠, 돌목, 엄마, 판돌, 나비, 모모, 굴돌, 다람, 선생님, 실룩, 촌장, 까로, 은호, 네로, 부리 | nabi_beds13, momo_down13, guldol_down13, teacher_down13, teacher_receipt13, silluk_supervision13, silluk_receipt13, transport_cleanup13, crowd_prepare13 | 인수하지 않은 돌의 약속 값을 보인다 / 장부의 두 배를 실룩에게 보인다 / 피코가 막혀야 했던 까닭을 보인다 | NW_NEOUL_LEDGER, E13_HANDOVER, E13_ORDER |  / wind |
| 13 | `D13_A` | 대체 장면 13-A. 가족 셋의 하룻밤 | 학교/입구 경비실/광장 수레 | square, gate, school | 아빠, 촌장, 다람, 엄마, 주민, 돌목 | sleep13_gate_input, sleep13_input |  |  | bgm-family.mp3 / fire |
| 13 | `D13_B` | 대체 장면 13-B. 멈췄지만 끝내지 못한 밤 | 학교/입구 경비실/광장 수레 | square | 까로, 돌목, 아빠, 판돌, 바둑이 |  |  |  | bgm-night.mp3 / wind |
| 13 | `D13_C` | 대체 장면 13-C. 사람을 끌어내리는 손 | 학교/입구 경비실/광장 수레 | square | 주민, 너울, 다람, 아빠, 돌목, 누비 |  |  | NW_NEOUL_LEDGER | bgm-pressure.mp3 / wind |
| 14 | `D14_S01` | 장면 14-1. 아침에도 살아 있는 사람 | 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 | school | 나비, 아이, 토실, 백 부인, 판돌, 아빠, 다람, 엄마, 바둑이 | altar_guide14 |  | NW_BURNT_PAGE, NW_MADAM_DAY7, NW_OLD_RATIONS | bgm-inn2.mp3 / fire |
| 14 | `D14_S02` | 장면 14-2. 아무도 묶여 있지 않은 제단 | 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 | altar, gate, v111_labor, school | 다람, 아빠, 엄마, 바둑이, 촌장, 부리, 백 부인, 까로, 나비, 돌목 | mayor_site_request14, device_detach14, guard_relief_check14, device_lock14, device_pause14 | 희생의 숫자와 장부를 대조한다 / 아르카가 부른다는 말과 옛 기록을 대조한다 / 쇠가 언제 붙었는지 보인다 / 맨 처음 이름을 짚는다 | NW_TABLET_B, NW_IRON_MARK | bgm-altar.mp3 / wind |
| 14 | `D14_S03` | 장면 14-3. 보미라는 이름 | 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 | gate | 아빠, 할머니, 엄마, 부엉이, 토실 |  |  |  | bgm-think.mp3 /  |
| 14 | `D14_S04` | 장면 14-4. 이름판 아래의 그릇 | 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 | square, school | 토실, 다람, 아빠, 판돌, 엄마, 나비, 돌목, 백 부인, 초롱, 부엉이 | supply_inventory14 |  |  | bgm-village.mp3 / wind |
| 14 | `D14_S05` | 장면 14-5. 엄마 몫 과자 | 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 |  | 다람, 엄마, 아빠, 나비, 도토, 바둑이, 돌목 | wild_room14, wild_hall14, wild_square14, wild_road14, hidden_base_offer14, hidden_base_room14, hidden_base_door14 |  |  | bgm-ending.mp3 /  |
| 14 | `D14_END_FAMILY` | 가족 철수 결말 — 열지 않은 문 | 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 | gate | 돌목, 아빠, 다람, 엄마 |  |  |  | bgm-family.mp3 / fire |
| 14 | `D14_END_PARTIAL` | 부분 구조 결말 — 남은 인계표 | 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 | square, school | 까로, 아빠, 돌목, 다람 | partial_handoff14, partial_receipt14 |  |  | bgm-snow.mp3 / wind |
| 14 | `D14_END_VIOLENCE` | 군중 폭력 결말 — 한 명의 자리가 더 필요하다 | 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 | clinic | 서리, 주민, 다람, 아빠 |  |  |  | bgm-think.mp3 / clock |

## 1일

### MS14_D01_S01 1. 마차 / 엄마 몫

- 원본 시간·장소: 1일 낮 / 움직이는 마차 · 생각(목표 문구): 편지에 적힌 여관까지 무사히 갈 수 있을까?
- label: `r13_v111_start_block`, `r13_v111_letter_open`, `r13_v111_letter_read`, `r13_v111_gate_ledger_hand`, `r13_v111_letter_menu`, `r13_v111_letter_last`, `r13_v111_letter_hand`, `r13_v111_letter_none`, `r13_v111_carriage_end`, `r13_v111_leave_carriage`, `r13_v111_letter_close`, `r13_v111_letter_any`, `r13_v111_letter_close_b`
- 장소: gate · 원본 등장: daram, karo, father · 무대 세우기: 
- 대사: 원문 ID 21개, 묶음 gate_ledger_hand, 펼친 줄 27, rpy 직접 줄 12
- 그림: 배경 gate=room13-pixel-ready-gate0173-afternoon.webp, room13-pixel-ready-gate0173-evening.webp, room13-pixel-ready-gate0173-morning.webp
- 자료: E01 초대 편지(observed)
- 상태 값 쓰기: `letter_close_selected`, `K01a`, `K01b`, `carriage_stopped`
- 메뉴(`r13_v111_letter_menu`, display_menu): v111_menu

### MS14_D01_S02 2. 초소 / 한 사람의 허가

- 원본 시간·장소: 1일 도착 / 초소 입구→내부 · 생각(목표 문구): 마을에 들어가려면 무엇을 확인받아야 할까?
- 진입 조건(어기면 예외로 멈춤): 자료 ["E01"], 값 {"carriage_stopped": true}
- label: `r13_v111_gate_arrival`, `r13_v111_gate_request`, `r13_v111_gate_list`, `r13_v111_gate_choice`, `r13_v111_gate_letter`, `r13_v111_gate_original_out`, `r13_v111_gate_investigate`, `r13_v111_gate_reread_list`, `r13_v111_gate_proof`, `r13_v111_letter_observe`, `r13_v111_gate_proven_dispatch`, `r13_v111_gate_original`, `r13_v111_gate_shelf_pick`, `r13_v111_gate_shelf_menu`
- 장소: gate · 원본 등장: daram, karo, dolmok, father · 무대 세우기: 
- 대사: 원문 ID 21개, 묶음 letter_observe_tail, letter_observe_head, letter_observe_body, letter_observe_margin, letter_observe_nudge, 펼친 줄 37, rpy 직접 줄 5
- 그림: 배경 gate=room13-pixel-ready-gate0173-afternoon.webp, room13-pixel-ready-gate0173-evening.webp, room13-pixel-ready-gate0173-morning.webp · r13_scene ["winter", "눈에 막힌 입구"]
- 자료: E02 초소 처리 명단(observed)
- 상태 값 쓰기: `letter_tail_observed`, `letter_observe_miss`
- 메뉴(`r13_v111_gate_shelf_menu`, display_menu): [(r13_gate_shelf_names[0] + ' 칸을 꺼낸다', 'before'), (r13_gate_shelf_names[1] + ' 칸을 꺼낸다', 'today'), (r13_gate_shelf_names[2] + ' 칸을 꺼낸다', 'after')]
- 대기 관문 `gate_request` (장소 gate, 인물 ["guard", "daram"])
    - [0] 초소 처리 명단을 읽는다 — 물건 ledger@gate → jump r13_v111_gate_list
- 대기 관문 `gate_choice` (장소 gate, 인물 ["guard", "daram"])
    - [0] 초대 편지를 보여 준다 — 사람 guard · 자료 제시 V111:E01 (제시 버튼만)@gate → option MS14_D01_S02_L0022_O1; jump r13_v111_gate_letter
    - [1] 신청서를 찾으러 선반으로 간다 — 물건 booth@gate → option MS14_D01_S02_L0022_O2; jump r13_v111_gate_original
- 대기 관문 `gate_investigate` (장소 gate, 인물 ["guard", "daram"])
    - [0] 신청 원본을 읽는다 — 물건 gate_documents@gate → jump r13_v111_gate_read_original
    - [1] 겨울철 입장 규칙을 읽는다 — 물건 rules@gate → jump r13_v111_gate_read_rules
    - [2] 초소 처리 명단을 다시 본다 — 물건 ledger@gate → jump r13_v111_gate_reread_list
    - [3] 명단과 신청서, 적힌 게 다릅니다. — 사람 guard@gate · 조건 자료 E03 == true → option MS14_D01_S03_L0008_O1; jump r13_v111_gate_purpose
    - [4] 13호에 두 사람, 여관 확인도 여기 있습니다. — 사람 guard@gate · 조건 자료 E03 == true; 값 gate_lodging_retired == true → option MS14_D01_S03_L0008_O2; jump r13_v111_gate_lodging
    - [5] 근거를 대겠습니다. 둘 다 들여보내 주십시오. — 사람 guard@gate → option MS14_D01_S03_L0008_O3; jump r13_v111_gate_proof
    - [7] 명단은 어떻게 옮겨 적으신 겁니까? — 사람 guard@gate · 조건 값 purpose_difference_known == true; 값 reason_heard == false → option MS14_D01_S03_L0008_O5; jump r13_v111_gate_reason
    - [6] (선택지표에 없음) → option MS14_D01_S03_L0008_O4; jump r13_v111_gate_hint
- 회의/대조 「다람의 이름까지 등록하고 함께 들어갈 근거를 고른다」 (키 `함께 들어갈 근거를 고른다`, 회의 gate, 기회 무제한(R13_NW_UNLIMITED), 화면 r13_proof_workspace(통합 화면, mode=proof))
    - 정답 ["E02", "E03"] · 대체 없음 · 덧붙임 허용 ["E01", "E04"]
    - 상대 주장(화면 인용): 지금 이 명단에는 다돌 한 명만 적혀 있소. 일꾼으로. 그래서 다돌만 들어갈 수 있소.
    - 이김 → `r13_v111_gate_proven_dispatch` {"jumps": [["r13_v111_gate_proven", "if r13_v111_value('purpose_difference_known')==True"], ["r13_v111_gate_early", null]]}
    - 틀림 → `r13_v111_gate_wrong` {"meeting_end": [{"meeting": "gate", "result": "lose", "when": null}], "sets": [["gate_daram_unlisted", true, null]], "jumps": [["r13_v111_gate_investigate", "if r13_nw_retry('gate')"], ["r13_v111_registered", null]], "retry": ["r13_nw_retry('gate')"]}
    - 되묻기 → `r13_v111_gate_hint` {"jumps": [["r13_v111_gate_investigate", null]]}

### MS14_D01_S03 3. 초소 / 둘이 들어갈 근거

- 원본 시간·장소: 1일 / 초소 첫 추리 · 생각(목표 문구): 우리가 낸 신청서와 문지기의 원본은 같은 내용일까?
- 진입 조건(어기면 예외로 멈춤): 자료 ["E02"], 값 {"gate_registered": false}
- label: `r13_v111_gate_read_original`, `r13_v111_gate_read_rules`, `r13_v111_gate_purpose`, `r13_v111_gate_lodging`, `r13_v111_gate_number`, `r13_v111_gate_proven`, `r13_v111_gate_early`, `r13_v111_gate_wrong`, `r13_v111_gate_hint`, `r13_v111_gate_reason`
- 장소:  · 원본 등장: daram, dolmok, father · 무대 세우기: 
- 대사: 원문 ID 27개, 묶음 없음, 펼친 줄 39, rpy 직접 줄 0
- 그림: 배경 (이동 없음 — 앞 장면 배경 유지)
- 자료: E03 방문 신청 원본(observed), E04 겨울철 입장 규칙(observed)
- 상태 값 쓰기: `purpose_difference_known`, `gate_hardened`, `gate_daram_unlisted`, `gate_basis_proven`, `reason_heard`, `K05`
- 회의 결과: `gate` → lose (`r13_v111_gate_number`)
- 회의 결과: `gate` → win (`r13_v111_gate_proven`)
- 회의 결과: `gate` → win (`r13_v111_gate_early`)
- 회의 결과: `gate` → lose (`r13_v111_gate_wrong`)

### MS14_D01_S04 4. 문이 열릴 때 / 이름

- 원본 시간·장소: 1일 / 초소 등록 후 입장 · 생각(목표 문구): 우리 두 사람 모두 제대로 등록됐을까?
- 진입 조건(어기면 예외로 멈춤): 자료 [], 값 {"gate_registered": false} · 검사 `r13_v111_value("gate_basis_proven") is True or r13_v111_value("gate_daram_unlisted") is True`
- label: `r13_v111_registered`, `r13_v111_registered_menu`, `r13_v111_registered_reason`, `r13_v111_registered_depart`
- 장소: gate · 원본 등장: dolmok, daram, neoul, karo, father · 무대 세우기: 
- 대사: 원문 ID 19개, 묶음 없음, 펼친 줄 36, rpy 직접 줄 0
- 그림: 배경 gate=room13-pixel-ready-gate0173-afternoon.webp, room13-pixel-ready-gate0173-evening.webp, room13-pixel-ready-gate0173-morning.webp · 컷 ev:E05
- 자료: E05 정정된 입장 기록(observed)
- 상태 값 쓰기: `gate_registered`, `E05.variant`, `reason_heard`, `K05`, `gate_mother_report_instruction_heard`, `heard_inn_order1`
- 대기 관문 `registered_menu` (장소 gate, 인물 ["guard", "daram", "karo"])
    - [0] 명단은 어떻게 옮겨 적으신 겁니까? — 사람 guard@gate · 조건 값 reason_heard == false → option MS14_D01_S04_L0012_O1; jump r13_v111_registered_reason
    - [1] 짐을 찾아 여관으로 간다 — 이동 inn@inn → option MS14_D01_S04_L0012_O2; jump r13_v111_registered_depart

### MS14_D01_S05 5. 여관 13호 / 기다리지 않는 방

- 원본 시간·장소: 1일 저녁 / 로비→빈13호→밤 · 생각(목표 문구): 편지를 보낸 여관에서 아내를 만날 수 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 [], 값 {"gate_registered": true}
- label: `r13_v111_inn`, `r13_v111_room_observe`, `r13_v111_room_empty`, `r13_v111_note_pick`, `r13_v111_room_note`, `r13_v111_bundle_open`, `r13_hidden_base_paper1`, `r13_v111_bundle`, `r13_v111_letter_compare`, `r13_v111_room_compare`, `r13_v111_sleep1`, `r13_v111_letter_retry`
- 장소: inn, room13 · 원본 등장: granny, daram, inn_worker, father · 무대 세우기: 
- 대사: 원문 ID 46개, 묶음 hands_wrapped1, hidden_base_paper1, compare_retry, 펼친 줄 68, rpy 직접 줄 1
- 그림: 배경 inn=room13-pixel-panorama-inn-afternoon.webp, room13-pixel-panorama-inn-evening.webp, room13-pixel-panorama-inn-morning.webp; room13=(상태별) after,before · 컷 ev:HIDDEN_A3_paper, ev:D01_FAMILY_DRAWING, ev:D01_SNACK_BAG
- 자료: E06 방의 메모(observed), E30 책상 아래 보따리(observed)
- 상태 값 쓰기: `ui_room_arrival_seen`, `hidden_base:paper`, `under_desk_checked`, `K01a`, `K01b`, `cookie.location`, `day`
- 메뉴(`r13_v111_inn`, display_menu): 다람의 손을 천으로 감싸 준다
- 메뉴(`r13_v111_room_compare`, display_menu): 할머니에게 초롱의 행방을 묻는다 / 방을 더 둘러본다
- 메뉴(`r13_v111_room_compare`, display_menu): 다람의 이불을 여민다
- 대기 관문 `note_pick` (장소 room13, 인물 ["daram"])
    - [0] 책상 메모를 집는다 — 물건 mother_note@room13 → jump r13_v111_room_note
- 대기 관문 `bundle_open` (장소 room13, 인물 ["daram"])
    - [0] 책상 아래 보따리를 연다 — 물건 family_bundle@room13 → jump r13_v111_bundle
    - [100] 서랍 밑 종이를 빼낸다 — 물건 family_bundle@room13 · 조건 값 hidden_base:paper == null → call r13_hidden_base_paper1; jump r13_v111_bundle_open
- 대기 관문 `sleep1` (장소 room13, 인물 ["daram"])
    - [0] 과자를 두고 잠든다 — 물건 bed@room13 → apply option:sleep1:0 [{"op": "set", "field": "day", "value": 2}]; jump r13_v111_day2
- 회의/대조 「두 편지를 나란히 본다」 (키 `두 편지를 나란히 본다`, 회의 , 기회 회의 아님(기회 없음), 화면 r13_proof_workspace(통합 화면, mode=compare))
    - 정답 ["E01", "E06"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(화면 인용): 두 편지를 직접 읽고 견준다. 무엇이 같고, 무엇이 다른가.
    - 이김 → `r13_v111_room_compare` {"sets": [["K01a", true, null], ["K01b", true, null], ["cookie.location", "room13_plate", null]], "jumps": [["r13_v111_sleep1", null]]}
    - 틀림 → `r13_v111_letter_retry` {"jumps": [["r13_v111_letter_compare", null]]}

## 2일

### MS14_D02_S01 1. 광장 / 초롱의 손

- 원본 시간·장소: 2일 아침 / 마구간→등→북쪽 교환함 · 생각(목표 문구): 오늘 마을을 떠날 길이 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 [], 값 {"day": 2}
- label: `r13_v111_day2`, `r13_v111_square2`, `r13_v111_lamp_rope`, `r13_v111_chorong`, `r13_v111_go_box`, `r13_v111_box_path`, `r13_v111_box_inspect`, `r13_v111_box_empty`, `r13_v111_box_note`, `r13_v111_box_written`
- 장소: gate, square, forest · 원본 등장: karo, chorong, daram, father · 무대 세우기: 
- 대사: 원문 ID 38개, 묶음 없음, 펼친 줄 59, rpy 직접 줄 0
- 그림: 배경 gate=room13-pixel-ready-gate0173-afternoon.webp, room13-pixel-ready-gate0173-evening.webp, room13-pixel-ready-gate0173-morning.webp; square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp; forest=room13-pixel-wide-forest-afternoon.webp, room13-pixel-wide-forest-evening.webp, room13-pixel-wide-forest-morning.webp
- 상태 값 쓰기: `return_transport_inquiry_pending`, `mother_box_checked_day2`, `arrival_note_sent`
- 대기 관문 `lamp_rope` (장소 square, 인물 ["resident_lamplighter", "daram"])
    - [0] 덮개 지지 끈을 잡는다 — 물건 lamp@square → jump r13_v111_chorong
- 대기 관문 `go_box` (장소 square, 인물 ["resident_lamplighter", "daram"])
    - [0] 초롱과 교환함으로 간다 — 이동 forest@forest → jump r13_v111_box_path
- 대기 관문 `box_inspect` (장소 forest, 인물 ["resident_lamplighter", "daram"])
    - [0] 함과 주변을 직접 확인한다 — 물건 v111_box@forest → jump r13_v111_box_empty
- 대기 관문 `box_note` (장소 forest, 인물 ["resident_lamplighter", "daram"])
    - [0] 도착 쪽지를 직접 넣는다 — 물건 v111_box@forest → jump r13_v111_box_written

### MS14_D02_S02 2. 우체국 / 내 편지부터

- 원본 시간·장소: 2일 낮 / 우체국 · 생각(목표 문구): 편지를 부친 사람은 정말 아내일까?
- 진입 조건(어기면 예외로 멈춤): 자료 [], 값 {"mother_box_checked_day2": true, "arrival_note_sent": true}
- label: `r13_v111_post`, `r13_v111_envelope_show`, `r13_v111_post_checked`, `r13_v111_post_menu`, `r13_v111_post_scribe`, `r13_v111_post_return`
- 장소: post · 원본 등장: seryeon, daram, father · 무대 세우기: ["resident_momo"]
- 대사: 원문 ID 26개, 묶음 momo_post2, 펼친 줄 43, rpy 직접 줄 0
- 그림: 배경 post=room13-pixel-wide-post-morning.webp
- 자료: E07 초대 봉투 접수 기록(observed)
- 상태 값 쓰기: `pending_post_search`
- 대기 관문 `envelope_show` (장소 post, 인물 ["seryeon", "daram"])
    - [0] 초대 편지의 봉투를 보여 준다 — 사람 seryeon · 자료 제시 V111:E01 (제시 버튼만)@post → jump r13_v111_post_checked
- 대기 관문 `post_menu` (장소 post, 인물 ["seryeon", "daram"])
    - [0] 대필도 합니까? — 사람 seryeon@post → option MS14_D02_S02_L0015_O1; jump r13_v111_post_scribe
    - [1] 제 편지, 돌려주시겠습니까? — 사람 seryeon@post → option MS14_D02_S02_L0015_O2; jump r13_v111_post_return

### MS14_D02_S03 3. 3번 등 / 초상 의뢰

- 원본 시간·장소: 2일 오후 / 3번등 화가 자리 · 생각(목표 문구): 아내의 얼굴을 그려 줄 사람을 찾을 수 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 ["E07"], 값 {}
- label: `r13_v111_piko2`, `r13_v111_portrait_ask`, `r13_v111_portrait_commission`, `r13_v111_lamp_observe`, `r13_v111_lamp_details`, `r13_v111_lamp_seen_0`, `r13_v111_lamp_seen_1`, `r13_v111_lamp_seen_2`, `r13_v111_lamp_seen_3`
- 장소: square · 원본 등장: momo, piko, daram, chorong, father · 무대 세우기: 
- 대사: 원문 ID 42개, 묶음 없음, 펼친 줄 58, rpy 직접 줄 4
- 그림: 배경 square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp
- 자료: NW_PIKO_TREMOR 피코의 손 떨림(observed), E08 3번 등의 상태(observed)
- 상태 값 쓰기: `portrait_commissioned`, `nero_contact_lead`, `lamp_part_0`, `lamp_part_1`, `lamp_part_2`, `lamp_part_3`
- 대기 관문 `portrait_ask` (장소 square, 인물 ["resident_piko", "daram"])
    - [0] 제가 그려 본 건데, 아내를 그려 주실 수 있습니까? — 사람 resident_piko@square → jump r13_v111_portrait_commission
- 대기 관문 `lamp_observe` (장소 square, 인물 ["resident_piko", "daram"])
    - [0] 번호판을 본다 — 물건 lamp@square → jump r13_v111_lamp_seen_0
    - [1] 덮개를 본다 — 물건 lamp@square → jump r13_v111_lamp_seen_1
    - [2] 담요를 본다 — 물건 lamp@square → jump r13_v111_lamp_seen_2
    - [3] 받침과 바닥을 본다 — 물건 lamp@square → jump r13_v111_lamp_seen_3
    - [4] 살펴보기를 마친다 — 물건 lamp@square · 조건 값 lamp_part_0 == true; 값 lamp_part_1 == true; 값 lamp_part_2 == true; 값 lamp_part_3 == true → jump r13_v111_lamp_details

### MS14_D02_S04 4. 식당 / 부탁은 자리가 되기까지

- 원본 시간·장소: 2일 해지기 전 한 번의 기회 / 식당↔북쪽길 · 생각(목표 문구): 남은 낮 시간으로 누구를 먼저 도울 수 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 ["E08"], 값 {"portrait_commissioned": true, "nero_contact_lead": true}
- label: `r13_v111_diner_offer`, `r13_v111_afternoon`, `r13_v111_shelter_prepare`, `r13_v111_shelter_enter`, `r13_v111_shelter_done`, `r13_v111_nero_choice`, `r13_v111_nero_work`, `r13_v111_nero_done`
- 장소: dining, square, forest, inn, room13 · 원본 등장: nabi, chorong, piko, nero, granny, daram, father · 무대 세우기: 
- 대사: 원문 ID 66개, 묶음 shelter_work_done2, shelter_cloth_done2, bench_look2, bench_clean2, 펼친 줄 89, rpy 직접 줄 0
- 그림: 배경 dining=room13-pixel-wide-dining-afternoon.webp, room13-pixel-wide-dining-evening.webp, room13-pixel-wide-dining-morning.webp; square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp; forest=room13-pixel-wide-forest-afternoon.webp, room13-pixel-wide-forest-evening.webp, room13-pixel-wide-forest-morning.webp; inn=room13-pixel-panorama-inn-afternoon.webp, room13-pixel-panorama-inn-evening.webp, room13-pixel-panorama-inn-morning.webp; room13=(상태별) after,before
- 자료: E31 네로의 공급 경로(observed), E35 가족 침구 예약(reserved)
- 상태 값 쓰기: `piko_sacks2`, `piko_cloth2`, `piko_bench_seen2`, `piko_bench_clean2`, `D02_afternoon`, `piko_sheltered`, `nero_met_day2`, `box_rechecked_day2`, `selected_afternoon_work_completed`, `nero_supply_route_known`, `nero_bedding_reserved`, `carried_dry_blankets`
- 갈림길 운명: ["fate_piko", "saved"] (`r13_v111_shelter_done`)
- 대기 관문 `afternoon2` (장소 dining, 인물 ["nabi", "daram"])
    - [0] 포대 옮기는 거, 제가 돕겠습니다. — 사람 nabi@dining · 조건 값 piko_sacks2 == null → set piko_sacks2=True; 대사 shelter_work_done2
    - [1] 마른 천을 좀 빌릴 수 있을까요? — 사람 granny@inn · 조건 값 piko_cloth2 == null → set piko_cloth2=True; 대사 shelter_cloth_done2
    - [2] 오늘 밤은 식당에 앉을 자리가 있습니다. — 사람 resident_piko@square · 조건 값 piko_sacks2 == true; 값 piko_cloth2 == true; 값 piko_bench_clean2 == true → option MS14_D02_S04_L0020_O1; apply option:afternoon:0 [{"op": "set", "field": "D02_afternoon", "value": "shelter"}]; jump r13_v111_shelter_prepare
    - [3] 숲으로 가서 네로를 돕는다 — 이동 forest@forest → option MS14_D02_S04_L0020_O2; apply option:afternoon:1 [{"op": "set", "field": "D02_afternoon", "value": "nero"}]; jump r13_v111_nero_choice
    - [80] 벤치 표면을 살핀다 — 물건 table@dining · 조건 값 piko_sacks2 == true; 값 piko_bench_seen2 == null → 대사 bench_look2; set piko_bench_seen2=True
    - [81] 천으로 벤치의 물감을 닦는다 — 물건 table@dining · 조건 값 piko_bench_seen2 == true; 값 piko_cloth2 == true; 값 piko_bench_clean2 == null → 대사 bench_clean2; set piko_bench_clean2=True
- 대기 관문 `shelter_enter` (장소 square, 인물 ["resident_piko", "daram"])
    - [0] 피코와 식당에 들어간다 — 이동 dining@dining → jump r13_v111_shelter_done
- 대기 관문 `nero_work` (장소 forest, 인물 ["resident_nero", "daram"])
    - [0] 침구를 옮겨 묶고 이름을 적는다 — @forest → jump r13_v111_nero_done

### MS14_D02_S05 5. 여관 / 설명할 수 없는 빈칸

- 원본 시간·장소: 2일 밤 / 여관 로비→13호 · 생각(목표 문구): 아내를 마지막으로 본 날 이후는 누가 알까?
- 진입 조건(어기면 예외로 멈춤): 자료 [], 값 {"selected_afternoon_work_completed": true}
- label: `r13_v111_evening2`, `r13_v111_evening2_route`, `r13_v111_evening2_alive`, `r13_v111_evening2_end`, `r13_v111_sleep2`, `r13_lamp_prep2`, `r13_v111_day3`, `r13_v111_evening2_outside`
- 장소: inn, room13 · 원본 등장: granny, daram, father · 무대 세우기: 
- 대사: 원문 ID 12개, 묶음 la_cord2, la_latch2, la_bind2, 펼친 줄 23, rpy 직접 줄 0
- 그림: 배경 inn=room13-pixel-panorama-inn-afternoon.webp, room13-pixel-panorama-inn-evening.webp, room13-pixel-panorama-inn-morning.webp; room13=(상태별) after,before
- 상태 값 쓰기: `day`, `lamp_prep_done2`, `lamp_cord2`, `lamp_latch_seen2`, `lamp_bound2`
- 갈림길 운명: ["fate_piko", "saved"] (`r13_v111_day3`)
- 갈림길 운명: ["fate_piko", "lost"] (`r13_v111_day3`)
- 대기 관문 `sleep2` (장소 room13, 인물 ["daram"])
    - [0] 아침 약속을 적고 잠든다 — 물건 bed@room13 → apply option:sleep2:0 [{"op": "set", "field": "day", "value": 3}]; jump r13_v111_day3
- 대기 관문 `lamp_prep2` (장소 room13, 인물 ["daram"])
    - [0] 아침 약속을 적고 잠든다 — 물건 bed@room13 → set lamp_prep_done2=True
    - [1] 남은 끈 좀 써도 될까요? — 사람 resident_lamplighter@square · 조건 값 lamp_cord2 == null → 대사 la_cord2; set lamp_cord2=True
    - [2] 덮개의 걸쇠를 살핀다 — 물건 lamp@square · 조건 값 lamp_latch_seen2 == null → 대사 la_latch2; set lamp_latch_seen2=True
    - [3] 걸쇠에 끈을 감아 고정한다 — 물건 lamp@square · 조건 값 lamp_cord2 == true; 값 lamp_latch_seen2 == true; 값 lamp_bound2 == null → 대사 la_bind2; set lamp_bound2=True

## 3일

### MS14_D03_S01 1. 아침 / 두 가지 약속의 끝

- 원본 시간·장소: 3일 새벽~아침 / 광장 사망 또는 식당 생존 · 생각(목표 문구): 그림 속 얼굴이 아내와 닮았을까?
- 진입 조건(어기면 예외로 멈춤): 자료 [], 값 {"day": 3}
- label: `r13_lamp_attempt3`, `r13_lamp_attempt_field3`, `r13_v111_piko_alive3`, `r13_v111_piko_clean`, `r13_v111_piko_receive`, `r13_v111_piko_dead3`
- 장소: square, dining · 원본 등장: chorong, daram, piko, nabi, father · 무대 세우기: ["resident_piko", "resident_lamplighter", "resident_tok", "daram"]
- 대사: 원문 ID 33개, 묶음 la_morning3, la_field3, la_knife3, la_store3, 펼친 줄 65, rpy 직접 줄 0
- 그림: 배경 square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp; dining=room13-pixel-wide-dining-afternoon.webp, room13-pixel-wide-dining-evening.webp, room13-pixel-wide-dining-morning.webp
- 자료: E09 엄마의 초상(complete), NW_LA_CHECK 3번 등 마지막 점검(observed), NW_LA_FIELD 남아 있는 3번 돌과 안쪽 조각(observed), NW_LA_KNIFE 동의받아 맞춘 실룩의 칼(observed), NW_LA_OFFER 인수되지 않은 3번 돌의 두 배 값(observed), NW_INNER_PRICE 안쪽 돌의 값(observed), NW_KEEPER_DATE 날짜를 두 번 물은 창고지기(observed), E09 엄마의 초상(unfinished)
- 상태 값 쓰기: `piko_alive`, `piko.location`, `portrait`, `lamp_field_done3`, `lamp_knife_done3`, `lamp_store_done3`
- 대기 관문 `lamp_attempt_field3` (장소 square, 인물 ["resident_lamplighter", "resident_tok", "resident_piko", "daram"])
    - [0] 톡 씨, 공방에서 같이 확인해 주시겠습니까? — 사람 resident_tok@square · 조건 값 lamp_field_done3 == true; 값 lamp_knife_done3 == true; 값 lamp_store_done3 == true → jump r13_lamp_attempt_open3
    - [1] 돌받침 안쪽을 살피고 조각을 담는다 — 물건 lamp@square · 조건 값 lamp_field_done3 == null → 대사 la_field3; r13_nw_acquire ['NW_LA_CHECK']; r13_nw_acquire ['NW_LA_FIELD']; set lamp_field_done3=True
    - [2] 칼과 조각을 나란히 놓고 봐도 되겠습니까? — 사람 resident_siluk@square · 조건 값 lamp_field_done3 == true; 값 lamp_knife_done3 == null → 대사 la_knife3; r13_nw_acquire ['NW_LA_KNIFE']; set lamp_knife_done3=True
    - [3] 매입 장부와 약속하신 값을 보여 주시겠습니까? — 사람 resident_madam@store · 조건 값 lamp_store_done3 == null → 대사 la_store3; r13_nw_acquire ['NW_LA_OFFER']; r13_nw_acquire ['NW_INNER_PRICE']; r13_nw_acquire ['NW_KEEPER_DATE']; set lamp_store_done3=True
- 대기 관문 `piko_clean` (장소 dining, 인물 ["resident_piko", "nabi", "daram"])
    - [0] 약속한 자리를 치운다 — 물건 table@dining → jump r13_v111_piko_receive

### MS14_D03_S02 2. 광장 / 먼저 묶인 손

- 원본 시간·장소: 3일 아침 / 3번등 공개 조사 · 생각(목표 문구): 광장 등의 돌은 언제 사라졌을까?
- 진입 조건(어기면 예외로 멈춤): 자료 ["E09"], 값 {}
- label: `r13_v111_lamp3`, `r13_v111_lamp_inspect3`, `r13_v111_lamp_interior3`, `r13_v111_fragment_request`, `r13_v111_lamp_fragment3`, `r13_v111_lamp_log_request`, `r13_v111_lamp_log3`
- 장소: square · 원본 등장: tok, neoul, chorong, daram, father · 무대 세우기: 
- 대사: 원문 ID 25개, 묶음 없음, 펼친 줄 52, rpy 직접 줄 0
- 그림: 배경 square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp
- 자료: E10 빈 받침과 자국(observed), E32 안쪽 받침의 칼끝 파편(observed), E11 초롱의 점검장(observed)
- 대기 관문 `lamp_inspect3` (장소 square, 인물 ["resident_tok", "neoul", "resident_lamplighter", "daram"])
    - [0] 번호판·받침·자국을 살핀다 — 물건 lamp@square → jump r13_v111_lamp_interior3
- 대기 관문 `fragment_request` (장소 square, 인물 ["resident_tok", "resident_lamplighter", "daram"])
    - [0] 톡 씨, 안쪽 조각 좀 봐 주시겠습니까? — 사람 resident_tok@square → jump r13_v111_lamp_fragment3
- 대기 관문 `lamp_log_request` (장소 square, 인물 ["resident_lamplighter", "daram"])
    - [0] 점검장을 보여 주시겠어요? — 사람 resident_lamplighter@square → jump r13_v111_lamp_log3

### MS14_D03_S03 3. 공방과 진료소 / 돌려놓았다는 말

- 원본 시간·장소: 3일 오전 / 공방→진료소 · 생각(목표 문구): 톡의 집게는 지금 어디에 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 ["E10", "E11", "E32"], 값 {}
- label: `r13_v111_workshop3`, `r13_v111_loan_read`, `r13_v111_loan3`, `r13_v111_clinic3`, `r13_v111_measurement_read`, `r13_v111_measurement3`, `r13_v111_measurement_proof`, `r13_v111_measurement_correct`, `r13_v111_measurement_after`, `r13_v111_owl_tongs3`, `r13_v111_measurement_wrong`, `r13_v111_measurement_hint`
- 장소: workshop, clinic · 원본 등장: buri, ubak, daram, father · 무대 세우기: ["buri", "resident_owlgp"]
- 대사: 원문 ID 38개, 묶음 clinic_returned3, owl_tongs3, 펼친 줄 63, rpy 직접 줄 0
- 그림: 배경 workshop=room13-pixel-panorama-workshop-afternoon.webp, room13-pixel-panorama-workshop-evening.webp, room13-pixel-panorama-workshop-morning.webp; clinic=room13-pixel-ready-clinic0177-afternoon.webp, room13-pixel-ready-clinic0177-evening.webp, room13-pixel-ready-clinic0177-morning.webp
- 자료: E12 공구 대여 쪽지(observed), E13 우박의 측정지(observed)
- 상태 값 쓰기: `measurement_separated_from_theft`
- 메뉴(`r13_v111_clinic3`, display_menu): (무엇부터 물을까?) / 꺼낸 시각부터 묻는다 / 다시 넣은 게 확실한지 묻는다
- 대기 관문 `loan_read` (장소 workshop, 인물 ["buri", "daram"])
    - [0] 대여 쪽지를 읽는다 — 물건 tools@workshop → jump r13_v111_loan3
- 대기 관문 `measurement_read` (장소 clinic, 인물 ["resident_ubak", "daram"])
    - [0] 측정지를 읽는다 — 물건 notes@clinic → jump r13_v111_measurement3
- 회의/대조 「우박 씨가 잰 뒤에도 3번 등 안에 돌이 있었는가」 (키 `측정 종료와 점검 기록을 대조한다`, 회의 , 기회 회의 아님(기회 없음), 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E13", "E11"] · 대체 없음 · 덧붙임 허용 없음
    - 이김 → `r13_v111_measurement_correct` {"sets": [["measurement_separated_from_theft", true, null]], "jumps": [["r13_v111_measurement_after", null]]}
    - 틀림 → `r13_v111_measurement_wrong` {"jumps": [["r13_v111_measurement_proof", null]]}
    - 되묻기 → `r13_v111_measurement_hint` {"jumps": [["r13_v111_measurement_proof", null]]}

### MS14_D03_S04 4. 짐 내리는 골목 / 식구의 빵

- 원본 시간·장소: 3일 낮 / 골목→허락된 창고→공개확인 · 생각(목표 문구): 집게를 돌려주기 전에 무엇을 더 확인해야 할까?
- 진입 조건(어기면 예외로 멈춤): 자료 [], 값 {"measurement_separated_from_theft": true}
- label: `r13_v111_silluk3`, `r13_v111_transport_read`, `r13_v111_transport3`, `r13_v111_knife_permission`, `r13_v111_knife_observed`, `r13_v111_store_visit`, `r13_v111_store3`, `r13_v111_stone_check`, `r13_v111_stone3`, `r13_v111_sale_check`, `r13_v111_sale3`
- 장소: square, store, workshop · 원본 등장: silluk, silluk_children, baek, tok, buri, daram, father · 무대 세우기: 
- 대사: 원문 ID 33개, 묶음 없음, 펼친 줄 50, rpy 직접 줄 0
- 그림: 배경 square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp; store=room13-bg-store-2-afternoon.webp, room13-bg-store-2-evening.webp, room13-bg-store-2-morning.webp; workshop=room13-pixel-panorama-workshop-afternoon.webp, room13-pixel-panorama-workshop-evening.webp, room13-pixel-panorama-workshop-morning.webp
- 자료: E14 실룩의 운반표(observed), E15 창고의 3번 돌(observed), E16 백 부인의 매입 장부(observed), NW_INNER_PRICE 안쪽 돌의 값(observed), NW_KEEPER_DATE 날짜를 두 번 물은 창고지기(observed)
- 상태 값 쓰기: `silluk_knife_comparison_consent`, `silluk.children.location`
- 대기 관문 `transport_read` (장소 square, 인물 ["resident_siluk", "daram"])
    - [0] 운반표를 보여 주시겠습니까? — 사람 resident_siluk@square → jump r13_v111_transport3
- 대기 관문 `knife_permission` (장소 square, 인물 ["resident_siluk", "daram"])
    - [0] 그 칼, 잠깐 보여 주시겠습니까? — 사람 resident_siluk@square → jump r13_v111_knife_observed
- 대기 관문 `store_visit` (장소 square, 인물 ["resident_siluk", "daram"])
    - [0] 수취 창고에서 확인한다 — 이동 store@store → jump r13_v111_store3
- 대기 관문 `stone_check` (장소 store, 인물 ["resident_madam", "resident_tok", "daram"])
    - [0] 톡 씨, 이 돌 번호 좀 봐 주십시오. — 사람 resident_tok@store → jump r13_v111_stone3
- 대기 관문 `sale_check` (장소 store, 인물 ["resident_madam", "daram"])
    - [0] 매입 기록을 본다 — 물건 ledger@store → jump r13_v111_sale3

### MS14_D03_S05 5. 광장 공방 / 무엇을 증명했는가

- 원본 시간·장소: 3일 오후 / 등 앞 공방 · 생각(목표 문구): 등을 연 사람과 돌을 가져간 사람은 같을까?
- 진입 조건(어기면 예외로 멈춤): 자료 ["E11", "E12", "E13", "E14", "E15", "E16", "E32"], 값 {"silluk.children.location": "workshop_with_buri"}
- label: `r13_lamp_attempt_open3`, `r13_lamp_attempt_repair3`, `r13_lamp_attempt_repair_ok3`, `r13_lamp_attempt_final3`, `r13_lamp_attempt_win3`, `r13_v111_custody_choice`, `r13_v111_restore_route`, `r13_lamp_attempt_after3`, `r13_v111_restore_input`, `r13_v111_silluk_report`, `r13_v111_silluk_transfer`, `r13_lamp_attempt_partial3`, `r13_lamp_attempt_wrong3`, `r13_v111_trial_open`, `r13_v111_trial_repair`, `r13_v111_trial_repair_ok`, `r13_v111_trial_sale`, `r13_v111_trial_sale_ok`, `r13_v111_trial_knife`, `r13_v111_knife_fit`, `r13_v111_trial_latch`, `r13_v111_trial_latch_ok`, `r13_v111_trial_stone`, `r13_v111_trial_stone_ok`, `r13_v111_badugi_arrives`, `r13_v111_trial_piko`, `r13_v111_trial_alive`, `r13_v111_trial_choices`, `r13_v111_stone_choice`, `r13_v111_stone_return`, `r13_v111_stone_defer`, `r13_v111_trial_dead`, `r13_v111_trial_wrong_stone`, `r13_v111_trial_hint_stone`, `r13_v111_trial_wrong_latch`, `r13_v111_trial_hint_latch`, `r13_v111_knife_wrong`, `r13_v111_trial_knife_records`, `r13_v111_trial_wrong_sale`, `r13_v111_trial_hint_sale`, `r13_v111_trial_wrong`, `r13_v111_trial_hint`
- 장소: workshop, square · 원본 등장: neoul, tok, chorong, ubak, silluk, baek, badugi, daram, father · 무대 세우기: ["resident_tok", "resident_lamplighter", "resident_siluk", "neoul", "daram"] ["resident_owlgp"] ["resident_lamplighter", "resident_piko", "daram"]
- 대사: 원문 ID 58개, 묶음 la_open3, la_repair_ok3, la_final3, tok_axle3, owl_workshop3a, la_after3, la_wrong3, la_partial3, la_lose3, 펼친 줄 157, rpy 직접 줄 0
- 그림: 배경 workshop=room13-pixel-panorama-workshop-afternoon.webp, room13-pixel-panorama-workshop-evening.webp, room13-pixel-panorama-workshop-morning.webp; square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp
- 자료: E33 동의받고 대조한 칼(observed), E17 실룩의 걸쇠 진술(observed)
- 상태 값 쓰기: `silluk.children.location`, `repair_opening_separated`, `outer_latch_claim_refuted`, `silluk_status`, `lamp_theft_supported`, `stone_choice_completed`, `stone_warm_felt3`, `piko.location`, `public_stones`, `unverified_stones_status`
- 회의 결과: `lamp` → win (`r13_lamp_attempt_win3`)
- 회의 결과: `lamp` → partial (`r13_lamp_attempt_partial3`)
- 회의 결과: `lamp` → lose (`r13_lamp_attempt_wrong3`)
- 회의 결과: `lamp` → win (`r13_v111_badugi_arrives`)
- 회의 결과: `lamp` → partial (`r13_v111_trial_wrong_stone`)
- 회의 결과: `lamp` → partial (`r13_v111_trial_wrong_latch`)
- 회의 결과: `lamp` → partial (`r13_v111_knife_wrong`)
- 회의 결과: `lamp` → partial (`r13_v111_trial_wrong_sale`)
- 회의 결과: `lamp` → lose (`r13_v111_trial_wrong`)
- 이송 명단에 적음: resident_siluk (lamp_transfer, `r13_v111_silluk_transfer`)
- 이송 명단에 적음: resident_tok (lamp_lose, `r13_lamp_attempt_wrong3`)
- 이송 명단에 적음: resident_tok (lamp_lose, `r13_v111_trial_wrong`)
- 메뉴(`r13_v111_custody_choice`, display_menu): v111_menu
- 메뉴(`r13_v111_trial_knife`, display_menu): v111_menu
- 메뉴(`r13_v111_stone_choice`, display_menu): v111_menu
- 대기 관문 `restore_input` (장소 square, 인물 ["resident_tok", "resident_lamplighter", "daram"])
    - [0] 톡·초롱과 3번 돌을 복구한다 — 물건 lamp@square → jump r13_v111_restore3
- 회의/대조 「등 안의 칼끝 조각은 톡이 고친 뒤에 생긴 것인가」 (키 `수리 뒤 새로 생긴 파손을 가린다`, 회의 lamp, 기회 7, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["NW_LA_CHECK", "NW_LA_FIELD"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 너울 씨는 그 등 안을 마지막으로 만진 게 톡 씨라고 한다. ……정말 톡 씨가 마지막이었나?
    - 이김 → `r13_lamp_attempt_repair_ok3` {"sets": [["repair_opening_separated", true, null]], "jumps": [["r13_lamp_attempt_final3", null]]}
    - 틀림 → `r13_lamp_attempt_wrong3` {"meeting_end": [{"meeting": "lamp", "result": "lose", "when": null}], "listed": [{"person": "resident_tok", "reason": "lamp_lose", "when": null}], "jumps": [["r13_lamp_attempt_repair3", "if r13_nw_retry('lamp',['NW_LA_CHECK','NW_LA_FIELD'],'half_la_repair3')"], ["r13_v111_custody_choice", null]], "retry": ["r13_nw_retry('lamp',['NW_LA_CHECK','NW_LA_FIELD'],'half_la_repair3')"]}
- 회의/대조 「실룩이 한 말이, 칼끝이 부러진 자리와 맞는가」 (키 `남아 있는 돌과 칼의 사용을 연결한다`, 회의 lamp, 기회 7, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["NW_LA_CHECK", "NW_LA_FIELD", "NW_LA_KNIFE"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 실룩 씨는 바깥 걸쇠만 밀어 닫다가 칼이 부러졌다고 한다. ……그 부분이 내가 본 것과 맞나?
    - 이김 → `r13_lamp_attempt_win3` {"meeting_end": [{"meeting": "lamp", "result": "win", "when": null}], "sets": [["outer_latch_claim_refuted", true, null]], "jumps": [["r13_v111_custody_choice", null]]}
    - 틀림 → `r13_lamp_attempt_partial3` {"meeting_end": [{"meeting": "lamp", "result": "partial", "when": null}], "jumps": [["r13_lamp_attempt_final3", "if r13_nw_retry('lamp',['NW_LA_CHECK','NW_LA_FIELD','NW_LA_KNIFE'],'half_la_final3')"], ["r13_v111_custody_choice", null]], "retry": ["r13_nw_retry('lamp',['NW_LA_CHECK','NW_LA_FIELD','NW_LA_KNIFE'],'half_la_final3')"]}
- 회의/대조 「톡이 고친 뒤로, 3번 등이 열린 때를 차례로 잇는다」 (키 `수리와 반출을 가릴 자료를 낸다`, 회의 lamp, 기회 7, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E11", "E12", "E13"] · 대체 없음 · 덧붙임 허용 ["E10"]
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 너울 씨 장부에선 톡 씨 다음이 곧 돌 없는 아침이다. ……그 사이에 정말 아무 일도 없었나?
    - 이김 → `r13_v111_trial_repair_ok` {"sets": [["repair_opening_separated", true, null]], "jumps": [["r13_v111_trial_sale", null]]}
    - 틀림 → `r13_v111_trial_wrong` {"meeting_end": [{"meeting": "lamp", "result": "lose", "when": null}], "listed": [{"person": "resident_tok", "reason": "lamp_lose", "when": null}], "jumps": [["r13_v111_trial_repair", "if r13_nw_retry('lamp')"], ["r13_v111_trial_choices", null]], "retry": ["r13_nw_retry('lamp')"]}
    - 되묻기 → `r13_v111_trial_hint` {"jumps": [["r13_v111_trial_repair", null]]}
- 회의/대조 「사라진 3번 등의 돌은 어디로, 누구 손을 거쳐 갔는가」 (키 `돌과 매입 기록을 낸다`, 회의 lamp, 기회 7, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E15", "E16"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 너울 씨는 아침에 없던 그 돌이 지금 어디 있고, 누구 손을 거쳐 갔느냐고 묻는다. ……그 물음에 답할 것이 내 손에 없나?
    - 이김 → `r13_v111_trial_sale_ok` {"jumps": [["r13_v111_trial_knife", null]]}
    - 틀림 → `r13_v111_trial_wrong_sale` {"meeting_end": [{"meeting": "lamp", "result": "partial", "when": null}], "jumps": [["r13_v111_trial_sale", "if r13_nw_retry('lamp')"], ["r13_v111_trial_choices", null]], "retry": ["r13_nw_retry('lamp')"]}
    - 되묻기 → `r13_v111_trial_hint_sale` {"jumps": [["r13_v111_trial_sale", null]]}
- 회의/대조 「실룩이 한 말이, 칼끝이 부러진 자리와 맞는가」 (키 `바깥 걸쇠 주장과 발견 위치를 대조한다`, 회의 lamp, 기회 7, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E17", "E32", "E33"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 실룩 씨는 ‘바깥 걸쇠만’ 칼로 밀어 닫았다고 한다. ……그 부분이 내가 가진 것과 맞나?
    - 이김 → `r13_v111_trial_latch_ok` {"sets": [["outer_latch_claim_refuted", true, null]], "jumps": [["r13_v111_trial_stone", null]]}
    - 틀림 → `r13_v111_trial_wrong_latch` {"meeting_end": [{"meeting": "lamp", "result": "partial", "when": null}], "jumps": [["r13_v111_trial_latch", "if r13_nw_retry('lamp')"], ["r13_v111_trial_choices", null]], "retry": ["r13_nw_retry('lamp')"]}
    - 되묻기 → `r13_v111_trial_hint_latch` {"jumps": [["r13_v111_trial_latch", null]]}
- 회의/대조 「실룩이 판 돌은 새벽까지 등 안에 있던 바로 그 돌인가」 (키 `마지막 점검과 인수한 돌을 연결한다`, 회의 lamp, 기회 7, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E11", "E15", "E16"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 실룩 씨는 자기가 판 돌이 ‘그 돌’인지는 모른다고 한다. ……정말 그 부분이 비어 있나?
    - 이김 → `r13_v111_trial_stone_ok` {"sets": [["lamp_theft_supported", true, null]], "jumps": [["r13_v111_badugi_arrives", null]]}
    - 틀림 → `r13_v111_trial_wrong_stone` {"meeting_end": [{"meeting": "lamp", "result": "partial", "when": null}], "jumps": [["r13_v111_trial_stone", "if r13_nw_retry('lamp')"], ["r13_v111_trial_choices", null]], "retry": ["r13_nw_retry('lamp')"]}
    - 되묻기 → `r13_v111_trial_hint_stone` {"jumps": [["r13_v111_trial_stone", null]]}

### MS14_D03_S06 6. 저녁 / 그려지지 않은 얼굴

- 원본 시간·장소: 3일 저녁 / 등 복구·초상·물자인수 · 생각(목표 문구): 돌을 되돌린 뒤 아내를 찾는 길은 어디로 이어질까?
- 진입 조건(어기면 예외로 멈춤): 자료 [], 값 {"stone_choice_completed": true} · 검사 `r13_v111_value("lamp_theft_supported") is True or r13_v111_value("meeting:lamp") in ("partial","lose")`
- label: `r13_v111_somi_lead`, `r13_v111_blankets_route`, `r13_v111_blankets_receive`, `r13_v111_blankets3`, `r13_v111_stairs3`, `r13_v111_sleep3`, `r13_v111_day4`, `r13_v111_restore3`, `r13_v111_box_news3`, `r13_v111_memorial_route`, `r13_v111_piko_evening`, `r13_v111_piko_memorial`, `r13_v111_restore_defer`
- 장소: square, room13, clinic · 원본 등장: chorong, tok, piko, nero, daram, father · 무대 세우기: 
- 대사: 원문 ID 32개, 묶음 없음, 펼친 줄 51, rpy 직접 줄 0
- 그림: 배경 square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp; room13=(상태별) after,before; clinic=room13-pixel-ready-clinic0177-afternoon.webp, room13-pixel-ready-clinic0177-evening.webp, room13-pixel-ready-clinic0177-morning.webp
- 상태 값 쓰기: `nero_bedding_reserved`, `carried_dry_blankets`, `E35.status`, `day`, `public_stones`, `stone_warm_felt3`, `portrait`
- 대기 관문 `blankets_receive` (장소 square, 인물 ["resident_nero", "daram"])
    - [0] 어제 이름 적어 둔 침구, 받으러 왔습니다. — 사람 resident_nero@square → jump r13_v111_blankets3
- 대기 관문 `sleep3` (장소 room13, 인물 ["daram"])
    - [0] 그림을 세워 두고 잠든다 — 물건 bed@room13 → apply option:sleep3:0 [{"op": "set", "field": "day", "value": 4}]; jump r13_v111_day4

## 4일

### MS14_D04_S01 1. 솜이네 골목 / 닫힌 뒷문

- 원본 시간·장소: 4일 아침 / 조건부노동현장→솜이네문 · 생각(목표 문구): 아내의 초상으로 만날 수 있는 사람은 누구일까?
- 진입 조건(어기면 예외로 멈춤): 자료 [], 값 {"day": 4}
- label: `r13_v111_labor4`, `r13_v111_labor_sheet4`, `r13_v111_labor_confirm4`, `r13_v111_somi4`, `r13_v111_nero_route4`, `r13_v111_nero_known4`, `r13_v111_portrait_show4`, `r13_v111_somi_talk4`, `r13_v111_elder_cane4`, `r13_v111_nero_new4`, `r13_v111_nero_help4`, `r13_v111_nero_help_done4`
- 장소: v111_labor, ms14_somi · 원본 등장: silluk, neoul, nero, somi, musoe, daram, father · 무대 세우기: ["daram", "resident_siluk", "neoul"] ["daram", "resident_nero", "resident_somi"] ["v111_lowerroad_elder"]
- 대사: 원문 ID 50개, 묶음 elder_cane4, 펼친 줄 69, rpy 직접 줄 0
- 그림: 배경 v111_labor=room13-pixel-panorama-woodshed-intact.webp; ms14_somi=room13-bg-somi-alley-afternoon.webp, room13-bg-somi-alley-evening.webp, room13-bg-somi-alley-morning.webp
- 자료: E34 실룩의 작업표(observed), E18 솜이의 이야기(observed), E31 네로의 공급 경로(observed)
- 상태 값 쓰기: `silluk_status`, `silluk_labor_transfer_known`, `nero_supply_route_known`, `carried_dry_blankets`
- 대기 관문 `labor_sheet4` (장소 v111_labor, 인물 ["daram", "resident_siluk", "neoul"])
    - [0] 작업표를 보여 주십시오. — 사람 neoul@v111_labor → jump r13_v111_labor_confirm4
- 대기 관문 `portrait_show4` (장소 ms14_somi, 인물 ["daram", "resident_nero", "resident_somi"])
    - [0] 이분을 보셨습니까? — 사람 resident_nero · 자료 제시 V111:E09@ms14_somi → jump r13_v111_somi_talk4
- 대기 관문 `nero_help4` (장소 ms14_somi, 인물 ["daram", "resident_nero"])
    - [0] 침구와 물통을 돕는다 — 물건 v111_bedding@ms14_somi → jump r13_v111_nero_help_done4

### MS14_D04_S02 2. 처마 / 도토리 세 개

- 원본 시간·장소: 4일 낮 / 광장처마→오후방문후퇴 · 생각(목표 문구): 밤이가 직접 본 것은 어디까지일까?
- 진입 조건(어기면 예외로 멈춤): 자료 ["E18"], 값 {}
- label: `r13_v111_eaves4`, `r13_v111_portrait_place4`, `r13_v111_bami_mother4`
- 장소: square, ms14_somi · 원본 등장: kongi, tosil, daram, bami, nero, father · 무대 세우기: ["daram", "resident_kongi", "resident_tosil", "bami"] ["resident_lamplighter"]
- 대사: 원문 ID 26개, 묶음 silluk_lamp4, 펼친 줄 45, rpy 직접 줄 0
- 그림: 배경 square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp; ms14_somi=room13-bg-somi-alley-afternoon.webp, room13-bg-somi-alley-evening.webp, room13-bg-somi-alley-morning.webp
- 자료: E19 밤이의 제한된 목격(observed)
- 상태 값 쓰기: `bami_cold4`, `afternoon_visit_declined`
- 대기 관문 `portrait_place4` (장소 square, 인물 ["daram", "resident_kongi", "resident_tosil", "bami"])
    - [0] 여기 두고 물러날게. — 사람 bami · 자료 제시 V111:E09@square → jump r13_v111_bami_mother4

### MS14_D04_S03 3. 저녁 초소 뒤 / 비명

- 원본 시간·장소: 4일 저녁 / 초소뒷길 · 생각(목표 문구): 초소 뒤에서 누가 다친 걸까?
- 진입 조건(어기면 예외로 멈춤): 자료 ["E19"], 값 {"afternoon_visit_declined": true}
- label: `r13_v111_cry4`, `r13_v111_look_gate4`, `r13_v111_bite4`
- 장소: gate · 원본 등장: dolmok, neoul, bami, badugi, passerby, daram, father · 무대 세우기: ["daram", "guard", "neoul", "resident_badook"]
- 대사: 원문 ID 22개, 묶음 없음, 펼친 줄 28, rpy 직접 줄 0
- 그림: 배경 gate=room13-pixel-ready-gate0173-afternoon.webp, room13-pixel-ready-gate0173-evening.webp, room13-pixel-ready-gate0173-morning.webp
- 자료: E20 돌목의 최초 진술(observed)
- 상태 값 쓰기: `bami_status`, `dolmok.location`
- 대기 관문 `look_gate4` (장소 gate, 인물 ["daram", "guard", "neoul", "resident_badook"])
    - [0] 밝은 쪽에서 살핀다 — 물건 gate_documents@gate → jump r13_v111_bite4

### MS14_D04_S04 4. 같은 밤 / 잘못 적은 키

- 원본 시간·장소: 4일 밤 / 밝은초소→문앞울타리→식당 · 생각(목표 문구): 불빛 안에 남은 흔적이 그날 밤의 말과 맞을까?
- 진입 조건(어기면 예외로 멈춤): 자료 ["E20"], 값 {"bami_status": "temporarily_with_badugi", "dolmok.location": "clinic"}
- label: `r13_v111_testimony4`, `r13_v111_bami_ask4`, `r13_v111_bami_night4`, `r13_v111_inspect_gate4`, `r13_v111_fence_seen4`, `r13_v111_inspection_ready4`, `r13_v111_tracks_talk4`, `r13_v111_collect4`, `r13_v111_cloth4`, `r13_v111_kkomi_backdoor4`, `r13_v111_piko_sketch4`, `r13_v111_sleep4`, `r13_v111_morning5`, `r13_v111_tracks_seen4`, `r13_v111_bucket_seen4`
- 장소: ms14_guardroom, gate, dining, square, room13 · 원본 등장: badugi, bami, daram, kongi, nabi, chorong, father · 무대 세우기: ["daram", "resident_badook", "bami"] ["kid_kkomi"] ["daram"] ["resident_piko"]
- 대사: 원문 ID 54개, 묶음 kkomi_backdoor4, piko_sketch4, 펼친 줄 86, rpy 직접 줄 3
- 그림: 배경 ms14_guardroom=room13-bg-guardroom-afternoon.webp, room13-bg-guardroom-evening.webp, room13-bg-guardroom-morning.webp; gate=room13-pixel-ready-gate0173-afternoon.webp, room13-pixel-ready-gate0173-evening.webp, room13-pixel-ready-gate0173-morning.webp; dining=room13-pixel-wide-dining-afternoon.webp, room13-pixel-wide-dining-evening.webp, room13-pixel-wide-dining-morning.webp; square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp; room13=(상태별) after,before · 컷 ev:NW_PIKO_SKETCH4
- 자료: E21 밤이의 그날 밤 목격(observed), E22 울타리에서 수거한 천(observed), NW_PIKO_SKETCH4 피코의 처마 옆 그림(observed)
- 상태 값 쓰기: `rumor_not_eyewitness`, `d4_fence_seen`, `bami_status`, `piko.location`, `day`, `d4_tracks_seen`, `d4_bucket_seen`
- 대기 관문 `bami_ask4` (장소 ms14_guardroom, 인물 ["daram", "resident_badook", "bami"])
    - [0] 어디서 봤니? — 사람 bami@ms14_guardroom → jump r13_v111_bami_night4
- 대기 관문 `inspect_gate4` (장소 gate, 인물 ["daram"])
    - [0] 울타리 천 — 물건 v111_fence@gate → jump r13_v111_fence_seen4
    - [1] 겹친 발자국 — 물건 road@gate → jump r13_v111_tracks_seen4
    - [2] 엎어진 양동이 — 물건 v111_bucket@gate → jump r13_v111_bucket_seen4
- 대기 관문 `collect4` (장소 gate, 인물 ["daram", "resident_badook", "bami"])
    - [0] 같이 천을 수거해 주십시오. — 사람 resident_badook@gate → jump r13_v111_cloth4
- 대기 관문 `sleep4` (장소 room13, 인물 ["daram"])
    - [0] 관찰과 추측을 나눠 적고 잔다 — 물건 bed@room13 → jump r13_v111_morning5

## 5일

### MS14_D05_S01 1. 솜이네 / 손바닥

- 원본 시간·장소: 5일 아침 / 솜이네안 · 생각(목표 문구): 그날 밤 돌아온 모습을 직접 본 사람은 누구일까?
- 진입 조건(어기면 예외로 멈춤): 자료 ["E21", "E22"], 값 {}
- label: `r13_v111_somi5`
- 장소: ms14_somi, ms14_somi_inside · 원본 등장: nero, somi, musoe, daram, father · 무대 세우기: ["daram", "resident_nero", "resident_somi", "resident_musoe"]
- 대사: 원문 ID 21개, 묶음 없음, 펼친 줄 32, rpy 직접 줄 0
- 그림: 배경 ms14_somi=room13-bg-somi-alley-afternoon.webp, room13-bg-somi-alley-evening.webp, room13-bg-somi-alley-morning.webp; ms14_somi_inside=ms14/somi_inside 계열(MS14_ART["somi_inside"])
- 자료: NW_MUSOE_DEEP 갱도 맨 아래까지 간 무쇠(observed)
- 상태 값 쓰기: `somi_entry_consent`, `E24.status`

### MS14_D05_S02 2. 문턱 / 숨긴 것과 일어난 것

- 원본 시간·장소: 5일 오전 / 솜이네→진료소문→초소 · 생각(목표 문구): 허락받은 옷의 찢어진 끝과 울타리 천이 이어질까?
- 진입 조건(어기면 예외로 멈춤): 자료 [], 값 {"somi_entry_consent": true, "E24.status": "partial"}
- label: `r13_v111_wait_cloth5`, `r13_v111_compare_cloth5`, `r13_v111_cloth_match5`
- 장소: ms14_somi_inside, clinic · 원본 등장: musoe, somi, nero, daram, badugi, clinic_worker, father · 무대 세우기: ["daram", "resident_nero", "resident_somi", "resident_musoe"]
- 대사: 원문 ID 25개, 묶음 clinic_next5, 펼친 줄 32, rpy 직접 줄 0
- 그림: 배경 ms14_somi_inside=ms14/somi_inside 계열(MS14_ART["somi_inside"]); clinic=room13-pixel-ready-clinic0177-afternoon.webp, room13-pixel-ready-clinic0177-evening.webp, room13-pixel-ready-clinic0177-morning.webp
- 자료: E23 허락받고 대조한 겉옷(observed), E24 네로의 귀가 관찰(observed)
- 상태 값 쓰기: `E24.status`, `musoe.location`, `somi.location`
- 대기 관문 `compare_cloth5` (장소 ms14_somi_inside, 인물 ["daram", "resident_nero", "resident_somi", "resident_musoe"])
    - [0] 허락받은 옷과 천을 대조한다 — 물건 v111_coat@ms14_somi_inside → jump r13_v111_cloth_match5

### MS14_D05_S03 3. 초소 / 사라지지 않는 상처

- 원본 시간·장소: 5일 낮 / 초소밤이혐의검증 · 생각(목표 문구): 밤이를 붙잡아 둘 근거가 실제로 남아 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 ["E20", "E22", "E23", "E24"], 값 {"musoe.location": "clinic", "somi.location": "clinic"}
- label: `r13_v111_hearing5`, `r13_v111_proof5`, `r13_v111_bami_clear5`, `r13_v111_wrong5`, `r13_v111_hint5`
- 장소: gate · 원본 등장: dolmok, neoul, nero, badugi, kongi, bami, daram, father · 무대 세우기: ["daram", "guard", "neoul", "resident_nero", "resident_badook", "resident_kongi"]
- 대사: 원문 ID 30개, 묶음 없음, 펼친 줄 60, rpy 직접 줄 0
- 그림: 배경 gate=room13-pixel-ready-gate0173-afternoon.webp, room13-pixel-ready-gate0173-evening.webp, room13-pixel-ready-gate0173-morning.webp
- 자료: E25 돌목의 재확인 진술(observed), E26 밤이 혐의 정정 기록(observed)
- 상태 값 쓰기: `gate_post_cold_cost`, `tries:gate_post`, `bami_status`, `musoe_care`
- 회의 결과: `gate_post` → win (`r13_v111_bami_clear5`)
- 회의 결과: `gate_post` → lose (`r13_v111_wrong5`)
- 이송 명단에 적음: bami (gate_post_lose, `r13_v111_wrong5`)
- 회의/대조 「돌목이 붙잡은 사람을, 울타리 천에서부터 거슬러 잇는다」 (키 `밤이 혐의의 근거를 확인한다`, 회의 gate_post, 기회 3, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E20", "E22", "E23", "E24"] · 대체 [["E20", "E22", "NW_PIKO_SKETCH4"], ["E20", "E22", "E23", "NW_PIKO_SKETCH4"], ["E20", "E22", "E24", "NW_PIKO_SKETCH4"]] · 덧붙임 허용 ["E21", "NW_PIKO_SKETCH4"]
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 너울 씨는 키가 맞으면 밤이일 수도 있다고 한다. ……‘키가 맞으면’이라는 그 부분, 내가 가진 것과 맞나?
    - 이김 → `r13_v111_bami_clear5` {"meeting_end": [{"meeting": "gate_post", "result": "win", "when": null}], "sets": [["bami_status", "cleared", null], ["musoe_care", "nero_badugi_night_rotation", null]], "acquires": ["E25", "E26"], "jumps": [["r13_v111_warning5", null]]}
    - 틀림 → `r13_v111_wrong5` {"meeting_end": [{"meeting": "gate_post", "result": "lose", "when": null}], "listed": [{"person": "bami", "reason": "gate_post_lose", "when": null}], "sets": [["bami_status", "listed", null]], "jumps": [["r13_v111_proof5", "if r13_nw_retry(\"gate_post\",[\"E20\",\"E22\",\"E23\",\"E24\"],None)"], ["r13_v111_warning5", null]], "retry": ["r13_nw_retry(\"gate_post\",[\"E20\",\"E22\",\"E23\",\"E24\"],None)"]}
    - 되묻기 → `r13_v111_hint5` {"jumps": [["r13_v111_proof5", null]]}

### MS14_D05_S04 4. 점심 무렵 / 이제 도착한 경고

- 원본 시간·장소: 5일 점심무렵 / 초소앞바람막힌곳 · 생각(목표 문구): 아내의 답은 처음 편지와 같은 말을 하고 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 [], 값 {} · 검사 `r13_v111_value("bami_status") in ("cleared","listed")`
- label: `r13_v111_warning5`, `r13_v111_envelope5`, `r13_v111_warning_read5`, `r13_v111_warning_compare5`, `r13_v111_warning_compared5`, `r13_v111_review5`, `r13_v111_reply_handoff5`, `r13_v111_reply_done5`, `r13_v111_warning_retry5`
- 장소: gate · 원본 등장: chorong, daram, father · 무대 세우기: ["daram", "resident_lamplighter"]
- 대사: 원문 ID 25개, 묶음 compare_retry, 펼친 줄 36, rpy 직접 줄 2
- 그림: 배경 gate=room13-pixel-ready-gate0173-afternoon.webp, room13-pixel-ready-gate0173-evening.webp, room13-pixel-ready-gate0173-morning.webp
- 자료: E27 엄마의 경고 편지(observed), E28 엄마에게 쓰는 답장(observed)
- 상태 값 쓰기: `mother_warning_received`, `mother_denies_invitation`, `supply_contact_pending`, `inn_information_hub_risk_known`, `E28.handed_to`
- 메뉴(`r13_v111_warning_compared5`, menu): 첫날 기록을 다시 본다 / 답장을 쓴다
- 대기 관문 `envelope5` (장소 gate, 인물 ["daram", "resident_lamplighter"])
    - [0] 봉투를 받겠습니다. — 사람 resident_lamplighter@gate → jump r13_v111_warning_read5
- 대기 관문 `reply_handoff5` (장소 gate, 인물 ["daram", "resident_lamplighter"])
    - [0] 답장을 맡기겠습니다. — 사람 resident_lamplighter · 자료 제시 V111:E28@gate → jump r13_v111_reply_done5
- 회의/대조 「두 편지의 초대를 대조한다」 (키 `두 편지의 초대를 대조한다`, 회의 , 기회 회의 아님(기회 없음), 화면 r13_crisis_proof + r13_book(compare))
    - 정답 ["E01", "E27"] · 대체 없음 · 덧붙임 허용 없음
    - 이김 → `r13_v111_warning_compared5` {"sets": [["mother_denies_invitation", true, null], ["supply_contact_pending", true, null], ["inn_information_hub_risk_known", true, null]], "acquires": ["E28"], "jumps": [["r13_v111_reply_handoff5", null]]}
    - 틀림 → `r13_v111_warning_retry5` {"jumps": [["r13_v111_warning_compare5", null]]}

### MS14_D05_S05 5. 저녁 / 맡긴다는 말의 무게

- 원본 시간·장소: 5일 저녁 / 솜이네→식당→같은복도→13호 · 생각(목표 문구): 우리가 이 문을 스스로 열고 닫을 수 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 [], 값 {"mother_warning_received": true, "supply_contact_pending": true}
- label: `r13_v111_night5`, `r13_v111_owl_glove5`, `r13_v111_laundry5`, `r13_v111_laundry5_wait`, `r13_v111_laundry_overhear5`, `r13_v111_lock_check5`, `r13_v111_safety5`, `r13_v111_blankets5`, `r13_v111_packed5`, `r13_v111_last5`, `r13_v111_sleep5`, `r13_v111_morning6`, `r13_v111_empty_bag5`, `r13_v111_snack_plate5`
- 장소: ms14_somi_inside, dining, inn, hall, room13 · 원본 등장: somi, musoe, nero, badugi, nabi, granny, inn_worker, daram, father · 무대 세우기: ["daram", "resident_somi", "resident_musoe", "resident_nero", "resident_badook"] ["karo"] ["resident_owlgp"] ["neoul", "resident_nubi"]
- 대사: 원문 ID 52개, 묶음 owl_glove5, laundry_line5, laundry_overhear5, snack_plate5, 펼친 줄 103, rpy 직접 줄 0
- 그림: 배경 ms14_somi_inside=ms14/somi_inside 계열(MS14_ART["somi_inside"]); dining=room13-pixel-wide-dining-afternoon.webp, room13-pixel-wide-dining-evening.webp, room13-pixel-wide-dining-morning.webp; inn=room13-pixel-panorama-inn-afternoon.webp, room13-pixel-panorama-inn-evening.webp, room13-pixel-panorama-inn-morning.webp; hall=(상태별) after,before; room13=(상태별) after,before
- 자료: E29 다음 날 아침 보호 약속(observed), NW_LAUNDRY_TALK 빨래터에서 들은 너울의 말(observed)
- 상태 값 쓰기: `nero.location`, `musoe.location`, `somi.location`, `badugi.location`, `daram_next_morning_guard`, `grand_laundry_seen5`, `grand_ticket_spot_known`, `family_safety_changed`, `day`, `snack_bagged5`, `cookie.location`
- 대기 관문 `laundry5` (장소 laundry, 인물 ["daram"])
    - [0] 빨래 줄에 젖은 장갑을 건다 — 물건 v111_line@laundry · 조건 값 grand_laundry_seen5 == null → call r13_v111_laundry_overhear5; jump r13_v111_laundry5_wait
    - [1] 여관 접수대 — 이동 inn@inn → (이 label 에서 따로 처리 없음)
- 대기 관문 `lock_check5` (장소 room13, 인물 ["daram"])
    - [0] 문과 창문 잠금을 확인한다 — 물건 window@room13 → jump r13_v111_safety5
    - [1] 책상 접시를 본다 — 물건 bread@room13 · 조건 값 snack_bagged5 == null → call r13_v111_snack_plate5
- 대기 관문 `sleep5` (장소 room13, 인물 ["daram"])
    - [0] 아침 일정을 정하고 잔다 — 물건 bed@room13 → jump r13_v111_morning6

## 6일

### MS14_D06_S01 6-1. 오전 / 학교 뒤문 — 엄마에게 갈 물건

- 원본 시간·장소: ["SCHOOL_REAR", "INN_REAR"] · 생각(목표 문구): 다람의 자리만 마련하면 다른 아이들은 어디에 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("mother_warning_received") is True`
- label: `r13_v111_day6`, `r13_v111_blankets6`, `r13_v111_bowl_together6`, `r13_v111_nabi_supply6`, `r13_v111_board6`, `r13_v111_board_done6`, `r13_hp_meal6`, `r13_hp_meal6_wait`, `r13_v111_bowl_eat6`
- 장소: school, dining · 원본 등장: kkomi, nabi, daram, teacher, father, chorong · 무대 세우기: ["daram", "granny", "resident_lamplighter"] ["daram", "resident_teacher", "resident_lamplighter", "kid_kkomi"] ["npc_pandol", "daram", "nabi"]
- 대사: 원문 ID 36개, 묶음 bami_after5_6, kongi_after4_6, hp_spoon6, hp_meet6, 펼친 줄 85, rpy 직접 줄 1
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp; dining=room13-pixel-wide-dining-afternoon.webp, room13-pixel-wide-dining-evening.webp, room13-pixel-wide-dining-morning.webp · r13_scene [{"expr": "R13_PLACES['inn'][1]"}, {"expr": "R13_PLACES['inn'][0]"}] · 컷 ev:HIDDEN_P4_before, ev:PROP_D06_cloth_empty_borrowed_bowl, ev:PROP_D06_two_towels_salt_parcel
- 자료: E06_CONTACT 학교 뒤 공개 물자 수량(observed)
- 상태 값 쓰기: `cookie.location`, `D06_S01_opening_completed`, `D06_S01_children_completed`, `choice:MS14_D06_S01`, `D06_S01_bowl_choice_completed`, `family_blankets_not_donated`, `D06_S01_blankets_completed`, `D06_S01_bowl_together_completed`, `E06_CONTACT`, `school_day_seat`, `mother_route_shared`, `D06_S01_supply_completed`, `D06_S01_bowl_eat_completed`
- 메뉴(`r13_v111_day6`, menu): 그릇을 돌려주러 같이 가자. / 오늘은 먹었니? 먹을 것부터 알아보자.
- 대기 관문 `board6` (장소 dining, 인물 ["daram", "nabi"])
    - [0] 공개 보급판을 확인한다 — 물건 table@dining → jump r13_v111_board_done6
- 대기 관문 `hp_meal6` (장소 dining, 인물 ["npc_pandol", "daram", "nabi"])
    - [0] 다람아, 애들한테 가자. — 사람 daram@dining → (이 label 에서 따로 처리 없음)
    - [1] 식기 보따리를 살핀다 — 물건 table@dining · 조건 값 hidden_pandol:spoon_seen == null → 대사 hp_spoon6
    - [2] 숟가락 손잡이가 헐겁네요. — 사람 npc_pandol@dining · 조건 값 hidden_pandol:spoon_seen == true; 값 hidden_pandol:met == null → 대사 hp_meet6

### MS14_D06_S02 6-2. 오후 / 장작 창고 — 안전한 곳이라는 말

- 원본 시간·장소: ["WOODSHED", "SCHOOL_REAR"] · 생각(목표 문구): 아이들이 안에서 스스로 나올 수 있는 곳일까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("school_day_seat")=="confirmed"`
- label: `r13_v111_woodshed6`, `r13_v111_woodshed_check6`, `r13_v111_woodshed_seen6`, `r13_v111_afternoon6`, `r13_v111_fetch6`, `r13_v111_children_ready6`, `r13_v111_handoff6`, `r13_v111_handoff_done6`, `r13_v111_permission6`
- 장소: v111_woodshed, school · 원본 등장: kkomi, daram, kid_dodam, bori, father · 무대 세우기: ["daram", "kid_kkomi", "resident_bori"]
- 대사: 원문 ID 39개, 묶음 can_look6, can_pack6, can_wait6, fetch_now6, 펼친 줄 76, rpy 직접 줄 0
- 그림: 배경 v111_woodshed=room13-pixel-wide-woodshed-inside-afternoon.webp, room13-pixel-wide-woodshed-inside-evening.webp; school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 자료: NW_KKOMI_NOSTONE 창고 아이들의 기름 등잔(observed)
- 상태 값 쓰기: `D06_S02_inspect_completed`, `kkomi_can_seen6`, `acorn_recovered`, `kkomi_can_wait6`, `choice:MS14_D06_S02`, `D06_S02_evacuation_completed`, `evacuation_requested`, `D06_S02_today_completed`, `FIRE_EVACUATED`, `KKOMI_ALIVE`, `warehouse_children_school_handover`, `D06_P01_handover_completed`, `D06_S02_permission_completed`
- 갈림길 운명: ["fate_kkomi", "lost"] (`r13_v111_afternoon6`)
- 갈림길 운명: ["fate_kkomi", "saved"] (`r13_v111_handoff_done6`)
- 대기 관문 `woodshed_check6` (장소 v111_woodshed, 인물 ["daram", "kid_kkomi", "resident_bori"])
    - [0] 문 앞과 뒤창을 살핀다 — 물건 v111_wood@v111_woodshed → jump r13_v111_woodshed_seen6
- 대기 관문 `afternoon6` (장소 v111_woodshed, 인물 ["daram", "kid_kkomi", "resident_bori"])
    - [0] 선생님, 학교에 아이 자리가 있겠습니까? — 사람 resident_teacher@school · 조건 값 kkomi_seat6 == null → jump r13_v111_seat6
    - [1] 학교에 자리가 났어. 같이 갈래? — 사람 kid_kkomi@v111_woodshed · 조건 값 kkomi_seat6 == true → set choice:MS14_D06_S02='today'; jump r13_v111_fetch6
    - [2] 내일 아침에 데리러 올게 — 사람 kid_kkomi@v111_woodshed → set choice:MS14_D06_S02='permission'; r13_fork_set_fate ['fate_kkomi', 'lost']; jump r13_v111_permission6
    - [80] 깡통 줄을 살핀다 — 물건 v111_can@v111_woodshed · 조건 값 kkomi_can_seen6 == null → 대사 can_look6; set kkomi_can_seen6=True; jump r13_v111_afternoon6
    - [81] 줄을 풀고 도토리를 챙긴다 — 물건 v111_can@v111_woodshed · 조건 값 kkomi_can_seen6 == true; 값 acorn_recovered == null → 대사 can_pack6; set acorn_recovered=True; jump r13_v111_afternoon6
- 대기 관문 `handoff6` (장소 school, 인물 ["daram", "resident_teacher", "doto", "kid_kkomi"])
    - [0] 네 아이와 물자를 확인한다 — 물건 blankets@school → jump r13_v111_handoff_done6

### MS14_D06_S03 6-3. 해 질 무렵 / 창고 바깥 — 먼저 꺼낼 것

- 원본 시간·장소: ["WOODSHED"] · 생각(목표 문구): 아이들이 지나갈 수 있는 길이 남아 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("FIRE_EVACUATED") is False`
- label: `r13_v111_fire6`, `r13_v111_wet_cloth6`, `r13_v111_wet_done6`, `r13_v111_clear_wood6`, `r13_v111_rescue_done6`
- 장소: v111_fire, school · 원본 등장: kkomi, daram, bori, father · 무대 세우기: ["daram", "resident_bori"]
- 대사: 원문 ID 17개, 묶음 없음, 펼친 줄 20, rpy 직접 줄 0
- 그림: 배경 v111_fire=room13-pixel-panorama-woodshed-fire.webp; school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 상태 값 쓰기: `KKOMI_ALIVE`, `warehouse_children_rescued`, `DARAM_location`, `BORI_hands`, `D06_S03_main_completed`
- 대기 관문 `wet_cloth6` (장소 v111_fire, 인물 ["resident_bori"])
    - [0] 물에 적신 천을 건넨다 — 물건 v111_water@v111_fire → jump r13_v111_wet_done6
- 대기 관문 `clear_wood6` (장소 v111_fire, 인물 ["resident_bori"])
    - [0] 옆문 장작을 치운다 — 물건 v111_wood@v111_fire → jump r13_v111_rescue_done6

### MS14_D06_S04 6-4. 밤 / 학교 난로 곁 — 세 가지 잘못

- 원본 시간·장소: ["SCHOOL_ROOM", "WOODSHED"] · 생각(목표 문구): 불이 시작된 자리와 따로 보관할 흔적은 무엇일까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:bool(r13_v111_value("D06_S03_main_completed") or r13_v111_value("D06_S03P_empty_fire_completed"))`
- label: `r13_v111_after_fire6`, `r13_v111_bori_unhurt6`, `r13_v111_bori_burned6`, `r13_v111_empty_testimony6`, `r13_v111_rescue_testimony6`, `r13_v111_fire_evidence6`, `r13_v111_fire_record6`, `r13_v111_bowl_result6`, `r13_v111_four_bowls6`, `r13_v111_sleep6`, `r13_v111_sleep6_input`, `r13_v111_sleep6_done`, `r13_v111_morning7`, `r13_v111_empty_bowl6`
- 장소: school, v111_ruin · 원본 등장: kkomi, nabi, neoul, daram, kid_dodam, doto, bori, father · 무대 세우기: ["daram", "nabi", "resident_bori", "neoul", "doto"]
- 대사: 원문 ID 37개, 묶음 wood_morning7, 펼친 줄 59, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp; v111_ruin=room13-pixel-panorama-woodshed-ruin.webp
- 자료: E06_EMPTY 빈 창고 진압과 네 아이 인수(observed), E06_RESCUE 보리의 세 아이 구조 목격(observed), E06_FIRE 등잔·천·발화 지점(observed)
- 상태 값 쓰기: `D06_S04_supplies_completed`, `D06_S04_nabi_lamp_completed`, `D06_S04_accusation_completed`, `BORI_hands`, `D06_S04_no_burns_completed`, `KKOMI_ALIVE`, `D06_S04_burns_completed`, `D06_S04_empty_testimony_completed`, `D06_S04_rescue_testimony_completed`, `E06_FIRE`, `D06_S04_fire_evidence_completed`, `D06_S04_full_bowls_completed`, `day`, `D06_S04_empty_bowl_completed`
- 대기 관문 `fire_evidence6` (장소 v111_ruin, 인물 ["doto"])
    - [0] 등잔과 천을 따로 확인한다 — 물건 v111_lamp@v111_ruin → jump r13_v111_fire_record6
- 대기 관문 `sleep6_input` (장소 school, 인물 ["daram"])
    - [0] 잠자리를 정리한다 — 물건 blankets@school → jump r13_v111_sleep6_done

### MS14_D06_P01 D06_P01 — 오늘 옮기는 경로

- 원본 시간·장소: ["SCHOOL_ROOM"] · 생각(목표 문구): 허락과 함께 네 아이의 실제 자리도 확보됐을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("evacuation_requested") is True`
- label: `r13_v111_seat6`
- 장소:  · 원본 등장: kkomi, daram, doto, teacher, father, 창고 아이 1, 창고 아이 2, 창고 아이 3 · 무대 세우기: ["daram", "resident_teacher"]
- 대사: 원문 ID 3개, 묶음 seat_done6, 펼친 줄 5, rpy 직접 줄 0
- 그림: 배경 (이동 없음 — 앞 장면 배경 유지)
- 상태 값 쓰기: `evacuation_requested`, `D06_P01_permission_completed`, `school_permission`, `teacher_agrees`, `kkomi_seat6`

### MS14_D06_S03P D06_S03P — 빈 창고의 불

- 원본 시간·장소: ["WOODSHED", "SCHOOL_ROOM"] · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("FIRE_EVACUATED") is True and r13_v111_value("warehouse_children_school_handover")==4`
- label: `r13_v111_empty_fire6`
- 장소: v111_fire · 원본 등장: bori, father · 무대 세우기: ["resident_bori", "doto"]
- 대사: 원문 ID 7개, 묶음 없음, 펼친 줄 7, rpy 직접 줄 0
- 그림: 배경 v111_fire=room13-pixel-panorama-woodshed-fire.webp
- 상태 값 쓰기: `fire_result`, `warehouse_children_location`, `D06_S03P_empty_fire_completed`

## 7일

### MS14_D07_S01 7-1. 오전 / 빨래터 — 내 아이들 몫

- 원본 시간·장소: ["LAUNDRY"] · 생각(목표 문구): 기름 천과 등유 통만으로 그날 일을 알 수 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_owned("E06_FIRE")`
- label: `r13_v111_day7`, `r13_v111_children_school7`, `r13_v111_nubi_children_school7`, `r13_v111_nubi_children_receipt7`, `r13_v111_nubi_children_received7`, `r13_v111_bori_witness7`, `r13_v111_bori_witness_heard7`, `r13_v111_nubi_proof7`, `r13_v111_nubi_first_question7`, `r13_v111_nubi_admission7`, `r13_v111_nubi_wrong7`, `r13_v111_nubi_ticket7`, `r13_v111_nubi_snack7`, `r13_v111_children_here7`
- 장소: laundry, school · 원본 등장: nabi, nubi, bori, father, 아이 · 무대 세우기: ["resident_nubi", "resident_bori", "nabi"] ["nabi", "resident_teacher", "kid_nubi1", "kid_nubi2", "kid_nubi3"] ["resident_nubi", "resident_bori"] ["neoul"]
- 대사: 원문 ID 38개, 묶음 nubi_children_received7, drum_look7, nubi_ask_oil, nubi_ask_lamp, nubi_ask_door, fire_lose_neoul7, nubi_ticket7, nubi_snack7, 펼친 줄 76, rpy 직접 줄 1
- 그림: 배경 laundry=room13-pixel-panorama-laundry-afternoon.webp, room13-pixel-panorama-laundry-evening.webp; school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 자료: E07_NUBI 누비의 직접 진술(observed), NW_NUBI_TICKET 누비네 배급표의 덧붙인 줄(observed)
- 상태 값 쓰기: `D07_S01_questions_completed`, `choice:MS14_D07_S01`, `D07_S01_child_place_completed`, `grand_snack_ready7`, `NUBI_CHILDREN_location`, `D07_S01_school_completed`, `bori_nubi_door_witness_heard`, `fire_first_question`, `NUBI_admitted_setting_fire`, `NUBI_intent_to_kill`, `D07_S01_admission_completed`, `grand_snack_given7`, `grand_ticket_spot_kid`, `grand_ticket_spot_known`, `D07_S01_here_completed`
- 회의 결과: `fire` → lose (`r13_v111_nubi_wrong7`)
- 이송 명단에 적음: resident_bori (fire_lose, `r13_v111_nubi_wrong7`)
- 메뉴(`r13_v111_day7`, menu): 아이들은 학교에서 기다리게 하자. / 여기서 계속 묻는다.
- 메뉴(`r13_v111_nubi_first_question7`, menu): 문 앞의 기름 흔적을 설명해 주십시오. / 등잔은 뒷벽 물통 옆에 있었습니다. 뚜껑도 닫혀 있었고요. / 창고 문 앞에 서 계신 걸 보리 씨가 봤습니다.
- 대기 관문 `nubi_children_receipt7` (장소 school, 인물 ["nabi", "resident_teacher", "kid_nubi1", "kid_nubi2", "kid_nubi3", "daram"])
    - [0] 선생님, 누비 씨 아이 셋을 맡아 주셨습니까? — 사람 resident_teacher@school → jump r13_v111_nubi_children_received7
    - [1] 막내가 네 가방만 보고 있네. — 사람 daram@school · 조건 값 grand_snack_ready7 == true → call r13_v111_nubi_snack7
- 대기 관문 `bori_witness7` (장소 laundry, 인물 ["resident_nubi", "resident_bori"])
    - [0] 창고 문 앞에서 무엇을 보셨습니까? — 사람 resident_bori@laundry → jump r13_v111_bori_witness_heard7
    - [1] 기름통을 살핀다 — 물건 v111_drum@laundry · 조건 값 grand_ticket_spot_known == true; 자료 NW_NUBI_TICKET == false → 대사 drum_look7
    - [2] 통 밑 홈을 들춘다 — 물건 v111_drum@laundry · 조건 값 grand_ticket_spot_known == true; 자료 NW_NUBI_TICKET == false → call r13_v111_nubi_ticket7
- 회의/대조 「불이 시작된 곳과 진술을 대조한다」 (키 `불이 시작된 곳과 진술을 대조한다`, 회의 fire, 기회 4, 화면 r13_proof_workspace(통합 화면, mode=proof))
    - 정답 ["E06_FIRE"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(화면 인용): 등유 통은 내가 써요. 애들도 물 데울 때 쓰고요. …… 어제 저녁에도 데웠죠.
    - 이김 → `r13_v111_nubi_first_question7` {"sets": [["fire_first_question", "oil", "menu \"문 앞의 기름 흔적을 설명해 주십시오.\""], ["fire_first_question", "lamp", "menu \"등잔은 뒷벽 물통 옆에 있었습니다. 뚜껑도 닫혀 있었고요.\""], ["fire_first_question", "door", "menu \"창고 문 앞에 서 계신 걸 보리 씨가 봤습니다.\""]], "jumps": [["r13_v111_bori_witness7", "if not r13_v111_value(\"bori_nubi_door_witness_heard\")"], ["r13_v111_nubi_admission7", null]]}
    - 틀림 → `r13_v111_nubi_wrong7` {"meeting_end": [{"meeting": "fire", "result": "lose", "when": null}], "listed": [{"person": "resident_bori", "reason": "fire_lose", "when": null}], "jumps": [["r13_v111_nubi_proof7", "if r13_nw_retry(\"fire\")"], ["r13_v111_responsibility7", null]], "retry": ["r13_nw_retry(\"fire\")"]}

### MS14_D07_S02 7-2. 낮 / 회관에서 학교까지 — 남은 사람의 자리

- 원본 시간·장소: ["HALL", "SCHOOL_ROOM"] · 생각(목표 문구): 아이들의 오늘 밤 자리와 보호자는 정해졌을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `(lambda:r13_v111_value("NUBI_admitted_setting_fire") is True) or r13_v111_value("meeting:fire")=="lose"`
- label: `r13_v111_responsibility7`, `r13_v111_responsibility_answers7`, `r13_v111_school_names7`, `r13_v111_school_names_done7`, `r13_v111_living_child7`, `r13_v111_lost_child7`, `r13_v111_dodam_spoon7`, `r13_v111_free_day7`, `r13_v111_free_day7_wait`, `r13_v111_free_evening7`, `r13_v111_free_day7_pick`, `r13_v111_owl_repair_pick7`, `r13_hidden_base_pick7`, `r13_hp_pick7`, `r13_v111_fire_basis_route7`, `r13_v111_empty_fire_basis7`, `r13_v111_responsibility_wrong7`, `r13_v111_rescue_fire_basis7`
- 장소: school · 원본 등장: kkomi, nabi, neoul, nubi, 누비의 둘째, 누비의 막내, 누비의 큰아이, daram, doto, bori, teacher, father, 창고 아이 1, 창고 아이 2, 창고 아이 3, chorong · 무대 세우기: ["nabi", "resident_bori", "resident_nubi", "neoul"] ["nabi", "resident_bori", "resident_teacher"] ["doto", "daram"] ["resident_lamplighter"] ["daram", "kid_dodam"] ["nabi", "resident_teacher", "daram"]
- 대사: 원문 ID 41개, 묶음 dodam_spoon7, free_open7, free_evening7, doto_basket7, doto_promise7, stove_look7, ashbin7, stove_swap7, buri_tongs7, stove_hide7, owl_latch_look7, owl_latch_request7, owl_latch_work7, hidden_base_plate_seen7, hidden_base_plate7, hp_pin7, hp_fit7, hp_permit7, hp_discover7, hp_house7, laundry_talk_rebut7, 펼친 줄 158, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp · 컷 ev:HIDDEN_A3_plate_front, ev:HIDDEN_P4_pin, ev:HIDDEN_P4_after
- 자료: NW_STONE 각인 없는 검푸른 돌(swapped)
- 상태 값 쓰기: `fire_neoul_promise_recorded`, `grand:fire`, `neoul_promise_proven`, `D07_S02_responsibility_completed`, `FAMILY_BASE`, `NUBI_CHILDREN_school_care`, `warehouse_survivors_school_care`, `D07_S02_handover_completed`, `E07_OWL_CONTACT`, `D07_S02_message_completed`, `D07_S02_living_child_completed`, `D07_S02_fourth_child_completed`, `D07_S02_lost_child_completed`, `dodam_spoon7`, `doto_promise7`, `pocket_ration7`, `stove13_7`, `tongs7`, `owl_latch_seen7`, `owl_tok_agreed7`, `owl_tok_work7`, `busy:resident_tok`, `hidden_base:plate_seen`, `hidden_base:plate`
- 회의 결과: `fire` → win (`r13_v111_responsibility_answers7`)
- 회의 결과: `fire` → partial (`r13_v111_responsibility_wrong7`)
- 이송 명단에 적음: resident_bori (fire_partial, `r13_v111_responsibility_wrong7`)
- 대기 관문 `school_names7` (장소 school, 인물 ["nabi", "resident_teacher"])
    - [0] 명부와 실제 침구를 확인한다 — 물건 desks@school → jump r13_v111_school_names_done7
- 대기 관문 `free_day7` (장소 school, 인물 ["nabi", "resident_teacher", "daram"]) — 동적: r13_owl_tok_available7() 가 거짓이면 index 111·112 를 뺀다.
    - [0] 다람아, 이제 13호에 가 보자. — 사람 daram@school → jump r13_v111_free_evening7
    - [1] 돌 바구니가 무거워 보입니다. — 사람 doto@hall → 대사 doto_basket7
    - [2] 아래서 누가 부르면 어떻게 하십니까? — 사람 doto@hall · 조건 값 doto_promise7 == null → 대사 doto_promise7; set doto_promise7=True
    - [3] 난로를 살핀다 — 물건 v111_stove@room13 → 대사 stove_look7
    - [4] 재받이를 들여다본다 — 물건 v111_ashbin@room13 · 조건 값 pocket_ration7 == null; 값 stove13_7 == null → 대사 ashbin7; set pocket_ration7=True
    - [5] 집게로 돌을 꺼내고, 주머니의 배급 돌을 넣는다 — 물건 v111_stove@room13 · 조건 값 tongs7 == true; 값 pocket_ration7 == true; 값 stove13_7 == null → 대사 stove_swap7; set pocket_ration7=False; set stove13_7='ration'; r13_nw_acquire ['NW_STONE', 'swapped']
    - [6] 집게 하나만 빌릴 수 있을까? — 사람 buri@workshop · 조건 값 tongs7 == null → 대사 buri_tongs7; set tongs7=True
    - [7] 집게로 돌을 꺼낸다 — 물건 v111_stove@room13 · 조건 값 tongs7 == true; 값 pocket_ration7 == null; 값 stove13_7 == null → 대사 stove_hide7; set stove13_7='empty'; r13_nw_acquire ['NW_STONE', 'swapped']
    - [80] 문고리 부품을 살핀다 — 물건 bolts@workshop · 조건 값 hidden_pandol:spoon_seen == true; 값 hidden_pandol:pin_seen == null → 대사 hp_pin7
    - [81] 숟가락에 맞는 핀일까? — 사람 buri@workshop · 조건 값 hidden_pandol:met == true; 값 hidden_pandol:pin_seen == true; 값 hidden_pandol:pin_fitted == null → 대사 hp_fit7
    - [82] 숟가락을 가져오셨습니까? — 사람 npc_pandol@dining · 조건 값 hidden_pandol:pin_fitted == true; 값 hidden_pandol:visit_allowed == null → 대사 hp_permit7
    - [83] 손잡이를 고쳐 쟁반에 놓는다 — 물건 hp_table@hidden_pandol · 조건 값 hidden_pandol:visit_allowed == true; 값 hidden_pandol:family_seen == null → 대사 hp_discover7
    - [84] 안쪽 난로를 살핀다 — 물건 hp_stove@hidden_pandol · 조건 값 hidden_pandol:family_seen == true → 대사 hp_house7
    - [100] 버리는 문고리 부품을 살핀다 — 물건 bolts@workshop · 조건 값 hidden_base:plate_seen == null → 대사 hidden_base_plate_seen7; set hidden_base:plate_seen=True
    - [101] 이 작은 판은 가져가도 될까? — 사람 buri@workshop · 조건 값 hidden_base:plate_seen == true; 값 hidden_base:plate == null → 대사 hidden_base_plate7; set hidden_base:plate=True
    - [110] 13호 빗장 받이를 살핀다 — 물건 v111_latch7@room13 · 조건 값 owl_latch_seen7 == null → 대사 owl_latch_look7; set owl_latch_seen7=True
    - [111] 빗장 받이를 봐 주실 수 있습니까? — 사람 resident_tok@workshop · 조건 값 owl_latch_seen7 == true; 값 owl_tok_agreed7 == null; 값 TOK_ALIVE == true → 대사 owl_latch_request7; set owl_tok_agreed7=True
    - [112] 빗장 받이 작업을 함께 확인한다 — 물건 v111_latch7@room13 · 조건 값 owl_tok_agreed7 == true; 값 owl_tok_work7 == null → 대사 owl_latch_work7; set owl_tok_work7=True; set busy:resident_tok='owl_repair7'
- 회의/대조 「‘다들 책임이 있소’. 셋이 정말 같은 책임인가」 (키 `불의 원인과 빈 창고 진압을 구분한다`, 회의 fire, 기회 4, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E06_FIRE", "E06_EMPTY", "E07_NUBI"] · 대체 [["E06_FIRE", "E06_EMPTY", "NW_NUBI_TICKET"]] · 덧붙임 허용 ["NW_LAUNDRY_TALK", "E02"]
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 너울 씨는 셋 다 책임이 있다고 한 줄로 묶는다. ……그 묶음이 내가 가진 것과 맞나?
    - 이김 → `r13_v111_responsibility_answers7` {"meeting_end": [{"meeting": "fire", "result": "win", "when": null}], "sets": [["fire_neoul_promise_recorded", true, "if r13_v111_value(\"meeting:fire\")==\"win\""], ["grand:fire", true, "if r13_v111_value(\"meeting:fire\")==\"win\" / if r13_nw_grand([\"불의 원인과 빈 창고 진압을 구분한다\",\"불의 원인과 아이 구조를 구분한다\"],\"NW_NUBI_TICKET\")"], ["neoul_promise_proven", true, "if r13_v111_value(\"meeting:fire\")==\"win\" / if r13_nw_grand([\"불의 원인과 빈 창고 진압을 구분한다\",\"불의 원인과 아이 구조를 구분한다\"],\"NW_NUBI_TICKET\")"], ["D07_S02_responsibility_completed", true, null]], "jumps": [["r13_v111_school_names7", null]]}
    - 틀림 → `r13_v111_responsibility_wrong7` {"meeting_end": [{"meeting": "fire", "result": "partial", "when": null}], "listed": [{"person": "resident_bori", "reason": "fire_partial", "when": null}], "jumps": [["r13_v111_fire_basis_route7", "if r13_nw_retry(\"fire\",[\"E06_FIRE\",\"E06_EMPTY\",\"E07_NUBI\"] if r13_v111_value(\"FIRE_EVACUATED\") else [\"E06_FIRE\",\"E06_RESCUE\",\"E07_NUBI\"],\"half_fire_split7\")"], ["r13_v111_responsibility_answers7", null]], "retry": ["r13_nw_retry(\"fire\",[\"E06_FIRE\",\"E06_EMPTY\",\"E07_NUBI\"] if r13_v111_value(\"FIRE_EVACUATED\") else [\"E06_FIRE\",\"E06_RESCUE\",\"E07_NUBI\"],\"half_fire_split7\")"]}
- 회의/대조 「‘다들 책임이 있소’. 셋이 정말 같은 책임인가」 (키 `불의 원인과 아이 구조를 구분한다`, 회의 fire, 기회 4, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E06_FIRE", "E06_RESCUE", "E07_NUBI"] · 대체 [["E06_FIRE", "E06_RESCUE", "NW_NUBI_TICKET"]] · 덧붙임 허용 ["NW_LAUNDRY_TALK", "E02"]
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 너울 씨는 ‘다들 책임이 있소’로 끝내려 한다. ……그 말이 내가 본 어젯밤과 맞나?
    - 이김 → `r13_v111_responsibility_answers7` {"meeting_end": [{"meeting": "fire", "result": "win", "when": null}], "sets": [["fire_neoul_promise_recorded", true, "if r13_v111_value(\"meeting:fire\")==\"win\""], ["grand:fire", true, "if r13_v111_value(\"meeting:fire\")==\"win\" / if r13_nw_grand([\"불의 원인과 빈 창고 진압을 구분한다\",\"불의 원인과 아이 구조를 구분한다\"],\"NW_NUBI_TICKET\")"], ["neoul_promise_proven", true, "if r13_v111_value(\"meeting:fire\")==\"win\" / if r13_nw_grand([\"불의 원인과 빈 창고 진압을 구분한다\",\"불의 원인과 아이 구조를 구분한다\"],\"NW_NUBI_TICKET\")"], ["D07_S02_responsibility_completed", true, null]], "jumps": [["r13_v111_school_names7", null]]}
    - 틀림 → `r13_v111_responsibility_wrong7` {"meeting_end": [{"meeting": "fire", "result": "partial", "when": null}], "listed": [{"person": "resident_bori", "reason": "fire_partial", "when": null}], "jumps": [["r13_v111_fire_basis_route7", "if r13_nw_retry(\"fire\",[\"E06_FIRE\",\"E06_EMPTY\",\"E07_NUBI\"] if r13_v111_value(\"FIRE_EVACUATED\") else [\"E06_FIRE\",\"E06_RESCUE\",\"E07_NUBI\"],\"half_fire_split7\")"], ["r13_v111_responsibility_answers7", null]], "retry": ["r13_nw_retry(\"fire\",[\"E06_FIRE\",\"E06_EMPTY\",\"E07_NUBI\"] if r13_v111_value(\"FIRE_EVACUATED\") else [\"E06_FIRE\",\"E06_RESCUE\",\"E07_NUBI\"],\"half_fire_split7\")"]}

### MS14_D07_S03 7-3. 저녁 / 여관 13호 — 잠깐이라는 약속

- 원본 시간·장소: ["ROOM13", "INN_CORRIDOR"] · 생각(목표 문구): 아픈 어르신과 다람 곁에 지금 누가 남을 수 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("D07_S02_handover_completed") is True`
- label: `r13_v111_room_visit7`, `r13_v111_owl_well7`, `r13_v111_sleep7`, `r13_v111_detained_sleep7`, `r13_v111_detained_bed7`, `r13_v111_detained_morning8`, `r13_v111_day8`, `r13_v111_free_sleep7`, `r13_v111_free_sleep7_input`, `r13_v111_free_sleep7_done`, `r13_v111_handover7`, `r13_v111_promise_night7`, `r13_v111_tok_night7`
- 장소: room13, school, clinic · 원본 등장: karo, daram, doto, owl, father · 무대 세우기: ["daram", "granny", "resident_owlgp", "doto", "karo"] ["karo", "resident_seori"] ["daram", "doto", "resident_owlgp", "resident_seori", "karo"] ["resident_tok"] ["daram", "doto", "resident_owlgp", "resident_seori", "karo", "resident_tok"]
- 대사: 원문 ID 20개, 묶음 owl_well7, promise_clinic7, promise_room7, owl_tok_stays7, owl_tok_return7, 펼친 줄 89, rpy 직접 줄 0
- 그림: 배경 room13=(상태별) after,before; school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp; clinic=room13-pixel-ready-clinic0177-afternoon.webp, room13-pixel-ready-clinic0177-evening.webp, room13-pixel-ready-clinic0177-morning.webp
- 상태 값 쓰기: `D07_S03_medical_request_completed`, `D07_S03_protection_completed`, `route7`, `prevention`, `choice:MS14_D07_S03`, `OWL_ALIVE`, `DARAM_DETAINED`, `D07_medical_care`, `day`, `DOTO_location`, `DARAM_guardian`, `father_location`, `D07_S03_C_completed`
- 갈림길 운명: ["fate_owl", "stone"] (`r13_v111_owl_well7`)
- 갈림길 운명: ["fate_owl", "lost"] (`r13_v111_handover7`)
- 갈림길 운명: ["fate_owl", "promise"] (`r13_v111_promise_night7`)
- 갈림길 운명: ["fate_owl", "repair"] (`r13_v111_tok_night7`)
- 대기 관문 `detained_bed7` (장소 room13, 인물 [])
    - [0] 다음 날 면회를 준비한다 — 물건 bed@room13 → jump r13_v111_detained_morning8
- 대기 관문 `free_sleep7_input` (장소 school, 인물 ["daram"])
    - [0] 잠자리를 정리한다 — 물건 blankets@school → jump r13_v111_free_sleep7_done

### MS14_D07_S04 7-4. 밤 / 초소에서 13호까지 — 열리지 않는 문

- 원본 시간·장소: ["SNOW_DETOUR", "OUTPOST", "INN_CORRIDOR", "ROOM13"] · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("route7")=="murder" and r13_v111_value("D07_S03_C_completed") is True`
- label: `r13_v111_incident7`
- 장소: clinic, hall, room13 · 원본 등장: karo, nabi, neoul, daram, doto, father, grandmother · 무대 세우기: ["karo", "resident_seori"] ["karo", "resident_seori", "doto", "nabi"] ["granny"] ["neoul"] ["daram"]
- 대사: 원문 ID 31개, 묶음 없음, 펼친 줄 41, rpy 직접 줄 0
- 그림: 배경 clinic=room13-pixel-ready-clinic0177-afternoon.webp, room13-pixel-ready-clinic0177-evening.webp, room13-pixel-ready-clinic0177-morning.webp; hall=(상태별) after,before; room13=(상태별) after,before
- 상태 값 쓰기: `OWL_ALIVE`, `DARAM_DETAINED`, `DARAM_location`, `father_knows_attack_scene`, `D07_S04_main_completed`

## 8일

### MS14_D08_S01 8-1. 아침 / 보호실 — 듣기 싫은 말

- 원본 시간·장소: ["HOLDING_ROOM"] · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("route7")=="murder" and r13_v111_value("DARAM_DETAINED") is True`
- label: `r13_v111_custody8`
- 장소: v111_custody · 원본 등장: neoul, daram, seori, father · 무대 세우기: ["daram", "resident_seori", "neoul"]
- 대사: 원문 ID 23개, 묶음 없음, 펼친 줄 44, rpy 직접 줄 0
- 그림: 배경 v111_custody=room13-pixel-panorama-holding-morning.webp
- 자료: E08_CHILD_ACCOUNT 다람의 진술과 손목 기록(observed)
- 상태 값 쓰기: `E08_CHILD_ACCOUNT`, `D08_S01_main_completed`

### MS14_D08_S02 8-2. 오전 / 13호 — 없어진 조각의 자리

- 원본 시간·장소: ["INN_CORRIDOR", "ROOM13"] · 생각(목표 문구): 도토는 문틈에서 무엇을 계속 확인했을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("route7")=="murder" and r13_v111_value("OWL_ALIVE") is False`
- label: `r13_v111_room_evidence8`, `r13_v111_room_check8`, `r13_v111_room_checked8`
- 장소: room13 · 원본 등장: doto, buri, father · 무대 세우기: ["doto", "buri"]
- 대사: 원문 ID 30개, 묶음 없음, 펼친 줄 64, rpy 직접 줄 0
- 그림: 배경 room13=(상태별) after,before
- 자료: E08_ROOM 13호 현장과 도토의 관찰(observed), E08_CHILD_POSITION 도토가 확인한 다람의 두 손(observed), E08_ROOM_REACH 문틈과 책상 사이 거리(observed), NW_STONE 각인 없는 검푸른 돌(observed)
- 상태 값 쓰기: `E08_ROOM`, `postcry_alive_testimony`, `D08_S02_main_completed`, `E08_CHILD_POSITION`, `DOTO_view_scope`, `E08_ROOM_REACH`, `new_v1_evidence_seeded`
- 대기 관문 `room_check8` (장소 room13, 인물 ["doto", "buri"])
    - [0] 문틈과 발견 자리를 살핀다 — 물건 floor@room13 → jump r13_v111_room_checked8

### MS14_D08_S03 8-3. 오후 / 진료실 — 부러진 다음

- 원본 시간·장소: ["CLINIC"] · 생각(목표 문구): 두 조각과 상처는 어떤 접촉을 남겼을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("route7")=="murder" and r13_v111_owned("E08_ROOM")`
- label: `r13_v111_wounds8`, `r13_v111_tool_faces8`, `r13_v111_tool_faces_seen8`, `r13_v111_wire_curve8`, `r13_v111_wire_curve_seen8`
- 장소: clinic · 원본 등장: buri, seori, father · 무대 세우기: ["resident_seori", "buri"]
- 대사: 원문 ID 24개, 묶음 없음, 펼친 줄 38, rpy 직접 줄 0
- 그림: 배경 clinic=room13-pixel-ready-clinic0177-afternoon.webp, room13-pixel-ready-clinic0177-evening.webp, room13-pixel-ready-clinic0177-morning.webp
- 자료: E08_TOOL 촛대 파손·상처 대조 자료(observed), E08_CONTACT_ASSEMBLY 접힌 천·닫힌 핀·고리(observed), E08_WOUND_WIRE 상처 가장자리의 구리 파편(observed)
- 상태 값 쓰기: `E08_TOOL`, `D08_S03_main_completed`, `E08_CONTACT_ASSEMBLY`, `E08_WOUND_WIRE`, `pin_owner`
- 대기 관문 `tool_faces8` (장소 clinic, 인물 ["resident_seori", "buri"])
    - [0] 손잡이·파단면·고리를 확인한다 — 물건 notes@clinic → jump r13_v111_tool_faces_seen8
- 대기 관문 `wire_curve8` (장소 clinic, 인물 ["resident_seori", "buri"])
    - [0] 구리 조각과 핀 끝을 대조한다 — 물건 notes@clinic → jump r13_v111_wire_curve_seen8

### MS14_D08_S04 8-4. 해 질 무렵 / 등 관리함 — 혼자 가지 않는 길

- 원본 시간·장소: ["LAMP_PATH"] · 생각(목표 문구): 답장을 안전하게 받으려면 무엇이 필요할까?
- label: `r13_v111_mother_letter8`, `r13_v111_letter_route8`, `r13_v111_letter_murder8`, `r13_v111_escort8`, `r13_v111_escort_done8`, `r13_v111_sleep8`, `r13_v111_sleep8_input`, `r13_v111_sleep8_done`, `r13_v111_day9`, `r13_v111_letter_prevent8`
- 장소: square, school · 원본 등장: 순찰대원, father, chorong · 무대 세우기: ["resident_lamplighter", "doto", "resident_badook"]
- 대사: 원문 ID 25개, 묶음 daram_school8, 펼친 줄 33, rpy 직접 줄 0
- 그림: 배경 square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp; school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 자료: E08_RECENT_LETTER 6일에 쓴 엄마의 편지(observed)
- 상태 값 쓰기: `D08_S04_escort_completed`, `D08_S04_escort_murder_completed`, `D08_S04_late_completed`, `public_road_escort_completed`, `E08_RECENT_LETTER`, `CHORONG_ALIVE`, `mother_location`, `mother_secret_shared`, `D08_S04_keep_private_completed`, `day`, `D08_S04_escort_prevent_completed`, `D08_S04_safe_completed`
- 대기 관문 `escort8` (장소 square, 인물 ["resident_lamplighter", "doto", "resident_badook"])
    - [0] 공개 길 동행을 부탁합니다. — 사람 resident_badook@square → jump r13_v111_escort_done8
- 대기 관문 `sleep8_input` (장소 school, 인물 ["daram"])
    - [0] 잠자리를 정리한다 — 물건 blankets@school → jump r13_v111_sleep8_done

### MS14_D08_P01 8-P. 생존 대체 / 다람과 함께 듣는 진료

- 원본 시간·장소: ["SCHOOL_ROOM", "CLINIC", "ROOM13"] · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("route7")=="prevented" and r13_v111_value("OWL_ALIVE") is True`
- label: `r13_v111_prevent_clinic8`, `r13_v111_prevention_story8`, `r13_v111_owl_well8`, `r13_v111_missing_pages8`, `r13_v111_owl_reading8`, `r13_v111_care8`
- 장소: room13 · 원본 등장: daram, doto, owl, seori, father · 무대 세우기: ["daram", "resident_owlgp", "doto"] ["daram", "resident_owlgp", "resident_seori", "doto"] ["neoul", "granny"]
- 대사: 원문 ID 12개, 묶음 owl_well8, neoul_list8, owl_reading8, 펼친 줄 40, rpy 직접 줄 0
- 그림: 배경 room13=(상태별) after,before
- 자료: NW_STONE 각인 없는 검푸른 돌(clinic)
- 상태 값 쓰기: `living_owl_records_question`, `murder_evidence_available`, `D08_P01_missing_pages_completed`, `owl_reading8_done`, `E08_prevention_experience`, `D08_P01_care_B_completed`

## 9일

### MS14_D09_S01 9-1. 오전 / 주방과 책장 — 길 하나를 더 세다

- 원본 시간·장소: ["INN_KITCHEN", "ROOM13", "PASSAGE"] · 생각(목표 문구): 문이 닫혀도 밖으로 돌아올 수 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("route7")=="murder"`
- label: `r13_v111_passage9`, `r13_v111_safe_passage9`, `r13_v111_passage_walk9`, `r13_v111_passage_after9`, `r13_v111_passage_measured_hint9`, `r13_v111_passage_safety_hint9`
- 장소: kitchen · 원본 등장: doto, ttadak, father, grandmother · 무대 세우기: ["doto", "resident_ttadak", "granny", "buri"]
- 대사: 원문 ID 14개, 묶음 daram_door9, 펼친 줄 30, rpy 직접 줄 0
- 그림: 배경 kitchen=room13-pixel-wide-kitchen-afternoon.webp, room13-pixel-wide-kitchen-evening.webp, room13-pixel-wide-kitchen-morning.webp · 컷 O47-handprints
- 자료: E09_PASSAGE 직접 왕복한 통로(observed)
- 상태 값 쓰기: `daram_door_asked9`, `E09_PASSAGE`, `TTADAK_ALIVE`, `D09_S01_main_completed`, `time_cost`
- 대기 관문 `safe_passage9` (장소 kitchen, 인물 ["doto", "resident_ttadak"])
    - [0] 쐐기·안전줄·문지기를 확인한다 — 물건 rear@kitchen → jump r13_v111_passage_walk9
    - [1] 들어가기 전에 확인할 것은요? — 사람 resident_ttadak@kitchen → jump r13_v111_passage_safety_hint9
- 대기 관문 `passage_after9` (장소 kitchen, 인물 ["doto", "resident_ttadak"])
    - [0] 작업장으로 간다 — 이동 workshop@workshop → jump r13_v111_workshop9
    - [1] 실측한 길을 다시 확인합니다. — 사람 resident_ttadak@kitchen → jump r13_v111_passage_measured_hint9

### MS14_D09_S02 9-2. 낮 / 공방 — 같은 핀이 아니다

- 원본 시간·장소: ["WORKSHOP", "POST_OFFICE"] · 생각(목표 문구): 수선된 핀의 모양과 인수인은 누구일까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("route7")=="murder" and r13_v111_owned("E09_PASSAGE")`
- label: `r13_v111_workshop9`, `r13_v111_tok_route9`, `r13_v111_tok9`, `r13_v111_repair_copy9`
- 장소: workshop · 원본 등장: seryeon, father, tok · 무대 세우기: ["buri"] ["buri", "resident_tok"] ["seryeon"]
- 대사: 원문 ID 21개, 묶음 없음, 펼친 줄 33, rpy 직접 줄 0
- 그림: 배경 workshop=room13-pixel-panorama-workshop-afternoon.webp, room13-pixel-panorama-workshop-evening.webp, room13-pixel-panorama-workshop-morning.webp
- 자료: E09_PIN_OWNER 핀 수선과 인수 기록(observed)
- 상태 값 쓰기: `E09_PIN_OWNER`, `D09_S02_tok_completed`, `tok_repair_copy_owned`, `D09_S02_receipt_completed`

### MS14_D09_S03 9-3. 오후 / 식당 — 나비가 여민 것

- 원본 시간·장소: ["INN_DINING"] · 생각(목표 문구): 비명이 났을 때 할머니는 어디 있었을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_owned("E09_PIN_OWNER")`
- label: `r13_v111_scarf9`, `r13_v111_repair_trust9`, `r13_v111_pin_question9`, `r13_v111_pin_time9`, `r13_v111_scarf_compare9`, `r13_v111_scarf_done9`
- 장소: dining · 원본 등장: nabi, father, grandmother · 무대 세우기: ["nabi"] ["granny"]
- 대사: 원문 ID 36개, 묶음 없음, 펼친 줄 48, rpy 직접 줄 0
- 그림: 배경 dining=room13-pixel-wide-dining-afternoon.webp, room13-pixel-wide-dining-evening.webp, room13-pixel-wide-dining-morning.webp
- 자료: E09_PIN_TIME 첫 비명 뒤 핀을 다시 채운 때(observed), E09_PIN_HANDOVER_TIME 양손 확인 뒤 계단참의 핀(observed), E09_SCARF 목도리 찢어진 끝(observed)
- 상태 값 쓰기: `D09_S03_repair_trust_completed`, `E09_PIN_TIME`, `D09_S03_testimony_completed`, `E09_PIN_HANDOVER_TIME`, `grandmother_leaves_for_kitchen_after_child_guard_started`, `new_v1_evidence_seeded`, `E09_SCARF`, `grandmother_wrapped_upper_piece`, `D09_S03_scarf_completed`
- 대기 관문 `pin_question9` (장소 dining, 인물 ["nabi"])
    - [0] 그날 밤 할머니 곁에서 본 것을 묻겠습니다. — 사람 nabi@dining → jump r13_v111_pin_time9
- 대기 관문 `scarf_compare9` (장소 dining, 인물 ["nabi"])
    - [0] 목도리 끝과 핀을 대조한다 — 물건 mittens@dining → jump r13_v111_scarf_done9

### MS14_D09_S04 9-4. 저녁 / 우체국 — 누가 부쳤는지, 누가 썼는지

- 원본 시간·장소: ["POST_OFFICE", "HOLDING_ROOM", "SCHOOL_ROOM"] · 생각(목표 문구): 맡긴 사람과 쓴 사람을 같은 사람이라 할 수 있을까?
- label: `r13_v111_postal9`, `r13_v111_night_route9`, `r13_v111_custody_night9`, `r13_v111_sleep9`, `r13_v111_sleep9_input`, `r13_v111_sleep9_done`, `r13_v111_day10`, `r13_v111_school_night9`
- 장소: post, v111_custody, school · 원본 등장: daram, seryeon, sling, father · 무대 세우기: ["seryeon", "resident_sling"]
- 대사: 원문 ID 28개, 묶음 없음, 펼친 줄 53, rpy 직접 줄 0
- 그림: 배경 post=room13-pixel-wide-post-morning.webp; v111_custody=room13-pixel-panorama-holding-morning.webp; school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 자료: E09_MAIL 발송·필사본·반송의 출처(observed)
- 상태 값 쓰기: `pending_post_search`, `post_search_status`, `E09_MAIL`, `D09_S04_postal_completed`, `D09_S04_custody_night_completed`, `day`, `D09_S04_school_night_completed`
- 대기 관문 `sleep9_input` (장소 school, 인물 ["daram"])
    - [0] 잠자리를 정리한다 — 물건 blankets@school → jump r13_v111_sleep9_done

### MS14_D09_P01 9-P. 생존 대체 / 침입과 위조의 갈림길

- 원본 시간·장소: ["INN_KITCHEN", "PASSAGE", "ROOM13"] · 생각(목표 문구): 돌려받은 종이의 번호와 빈 자리는 맞을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("route7")=="prevented" and r13_v111_value("OWL_ALIVE") is True`
- label: `r13_v111_prevent_passage9`, `r13_v111_safe_prevent9`, `r13_v111_prevent_walk9`, `r13_v111_papers_check9`, `r13_v111_papers_done9`
- 장소: kitchen, room13 · 원본 등장: nabi, doto, ttadak, owl, father, grandmother · 무대 세우기: ["doto", "resident_ttadak", "granny", "nabi"]
- 대사: 원문 ID 21개, 묶음 없음, 펼친 줄 23, rpy 직접 줄 0
- 그림: 배경 kitchen=room13-pixel-wide-kitchen-afternoon.webp, room13-pixel-wide-kitchen-evening.webp, room13-pixel-wide-kitchen-morning.webp; room13=(상태별) after,before
- 자료: E09_PASSAGE 직접 왕복한 통로(observed)
- 상태 값 쓰기: `E09_PASSAGE`, `TTADAK_ALIVE`, `D09_P01_passage_completed`, `returned_pages_count`, `OWL_claim_no_separate_page`, `hidden_page_known`, `D09_P01_records_completed`
- 대기 관문 `safe_prevent9` (장소 kitchen, 인물 ["doto", "resident_ttadak"])
    - [0] 쐐기·안전줄·문지기를 확인한다 — 물건 rear@kitchen → jump r13_v111_prevent_walk9
- 대기 관문 `papers_check9` (장소 room13, 인물 ["resident_owlgp", "granny"])
    - [0] 반환 장수와 빈 자리를 확인한다 — 물건 books@room13 → jump r13_v111_papers_done9

## 10일

### MS14_D10_S01 10-1. 아침 / 회관 대기실 — 아빠 말부터 고치기

- 원본 시간·장소: ["HALL_WAITING"] · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("route7")=="murder" and all(r13_v111_owned(k) for k in ("E08_CHILD_POSITION","E08_ROOM_REACH","E08_CONTACT_ASSEMBLY","E08_WOUND_WIRE","E09_PIN_HANDOVER_TIME","E09_SCARF"))`
- label: `r13_v111_waiting10`
- 장소: school · 원본 등장: daram, buri, father · 무대 세우기: ["daram", "resident_seori", "buri"]
- 대사: 원문 ID 14개, 묶음 없음, 펼친 줄 18, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 상태 값 쓰기: `BURI_notebook`, `D10_S01_main_completed`

### MS14_D10_S02 10-2. 오전 / 회관 — 문 하나의 증언

- 원본 시간·장소: ["HALL"] · 생각(목표 문구): 그 문 말고 들어갈 길이 실제로 있었을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("D10_S01_main_completed") is True`
- label: `r13_v111_hearing10`, `r13_v111_wound_proof10`, `r13_v111_wound_answer10`, `r13_v111_passage_proof10`, `r13_v111_passage_answer10`, `r13_v111_passage_wrong10`, `r13_v111_hearing_hint10`, `r13_v111_hearing_wrong10`
- 장소: school · 원본 등장: nabi, neoul, doto, ttadak, seori, father, 촌장, grandmother · 무대 세우기: ["daram", "doto", "nabi", "granny", "neoul", "resident_ppul", "resident_seori"]
- 대사: 원문 ID 42개, 묶음 없음, 펼친 줄 93, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 상태 값 쓰기: `D10_S02_opening_completed`, `wounds_distinct`, `two_attackers_proven`, `postcry_alive_testimony`, `postcry_head_uninjured`, `D10_S02_two_wounds_completed`, `child_upper_reuse_after_pin_refasten`, `sole_access_assumption`, `D10_S02_second_door_completed`, `time_cost`
- 회의 결과: `room13` → lose (`r13_v111_passage_wrong10`)
- 회의 결과: `room13` → lose (`r13_v111_hearing_wrong10`)
- 이송 명단에 적음: daram (room13_lose, `r13_v111_passage_wrong10`)
- 이송 명단에 적음: daram (room13_lose, `r13_v111_hearing_wrong10`)
- 회의/대조 「두 상처와 촛대 파손을 대조한다」 (키 `두 상처와 촛대 파손을 대조한다`, 회의 room13, 기회 7, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E08_CHILD_ACCOUNT", "E08_TOOL"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 너울 씨는 손목을 쳤으면 머리도 쳤을 수 있다고 한다. ……그 부분이 내가 가진 것과 맞나?
    - 이김 → `r13_v111_wound_answer10` {"sets": [["wounds_distinct", true, null], ["two_attackers_proven", false, null], ["postcry_alive_testimony", true, null], ["postcry_head_uninjured", "unproven", null], ["D10_S02_two_wounds_completed", true, null], ["child_upper_reuse_after_pin_refasten", "refuted_by_continuous_hands_and_position", null], ["D10_S02_two_wounds_completed", true, null]], "jumps": [["r13_v111_passage_proof10", null]]}
    - 틀림 → `r13_v111_hearing_wrong10` {"meeting_end": [{"meeting": "room13", "result": "lose", "when": null}], "listed": [{"person": "daram", "reason": "room13_lose", "when": null}], "jumps": [["r13_v111_wound_proof10", "if r13_nw_retry(\"room13\",['E08_CHILD_ACCOUNT', 'E08_TOOL'],'half_room13_wound10')"], ["r13_v111_bench10", null]], "retry": ["r13_nw_retry(\"room13\",['E08_CHILD_ACCOUNT', 'E08_TOOL'],'half_room13_wound10')"]}
    - 되묻기 → `r13_v111_hearing_hint10` {"sets": [["time_cost", 0, null]], "jumps": [["r13_v111_passage_proof10", "if r13_v111_value(\"D10_S02_two_wounds_completed\")"], ["r13_v111_wound_proof10", null]]}
- 회의/대조 「정말 그 문 말고는 책상까지 갈 길이 없었는가」 (키 `두 번째 길을 실제 기록으로 보인다`, 회의 room13, 기회 7, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E09_PASSAGE", "E08_ROOM"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 너울 씨는 그 문으로 들어간 사람이 없었다고 한다. ……‘그 문’만 있었다는 그 부분, 맞나?
    - 이김 → `r13_v111_passage_answer10` {"sets": [["sole_access_assumption", "refuted", null], ["D10_S02_second_door_completed", true, null]], "jumps": [["r13_v111_owner10", null]]}
    - 틀림 → `r13_v111_passage_wrong10` {"meeting_end": [{"meeting": "room13", "result": "lose", "when": null}], "listed": [{"person": "daram", "reason": "room13_lose", "when": null}], "jumps": [["r13_v111_passage_proof10", "if r13_nw_retry(\"room13\",['E09_PASSAGE', 'E08_ROOM'],'half_room13_passage10')"], ["r13_v111_bench10", null]], "retry": ["r13_nw_retry(\"room13\",['E09_PASSAGE', 'E08_ROOM'],'half_room13_passage10')"]}
    - 되묻기 → `r13_v111_hearing_hint10` {"sets": [["time_cost", 0, null]], "jumps": [["r13_v111_passage_proof10", "if r13_v111_value(\"D10_S02_two_wounds_completed\")"], ["r13_v111_wound_proof10", null]]}

### MS14_D10_S03 10-3. 정오 / 회관 — 세 번의 변명

- 원본 시간·장소: ["HALL", "HALL_WAITING"] · 생각(목표 문구): 상처에 남은 조각과 계단참의 핀은 어떻게 이어질까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("D10_S02_second_door_completed") is True`
- label: `r13_v111_owner10`, `r13_v111_owner_proof10`, `r13_v111_owner_answer10`, `r13_v111_owner_tok10`, `r13_v111_time10`, `r13_v111_time_proof10`, `r13_v111_time_answer10`, `r13_v111_contact_proof10`, `r13_v111_contact_answer10`, `r13_v111_contact_wrong10`, `r13_v111_time_wrong10`, `r13_v111_owner_copy10`, `r13_v111_owner_wrong10`
- 장소: school · 원본 등장: nabi, neoul, daram, doto, buri, seori, father, 촌장, tok, grandmother · 무대 세우기: ["daram", "granny", "resident_ppul", "neoul", "nabi", "resident_seori", "buri", "doto"] ["daram", "granny", "resident_ppul", "neoul", "nabi", "resident_seori", "resident_tok", "buri", "doto"]
- 대사: 원문 ID 70개, 묶음 없음, 펼친 줄 131, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 상태 값 쓰기: `D10_S03_owner_question_completed`, `pin_owner`, `D10_S03_owner_tok_completed`, `D10_S03_time_question_completed`, `pin_after_cry`, `grandmother_kitchen_move`, `D10_S03_time_answer_completed`, `grandmother_passage_entry`, `D10_S03_entry_admission_completed`, `pin_transfer`, `fatal_contact_assembly`, `same_moment_fatal_contact`, `child_upper_reuse`, `D10_contact_limit_completed`, `D10_S03_contact_limit_completed`, `grandmother_records_confrontation`, `fatal_contact_responsibility`, `premeditation`, `interpretation.intentional_strike_vs_struggle_collision`, `DARAM_DETAINED`, `daram_release_basis`, `D10_confrontation_release_completed`, `DARAM_location`, `grandmother_custody`, `forgery_confirmed`, `room13_partial_kind`, `D10_S03_owner_copy_completed`
- 회의 결과: `room13` → win (`r13_v111_contact_answer10`)
- 회의 결과: `room13` → partial (`r13_v111_contact_wrong10`)
- 회의 결과: `room13` → partial (`r13_v111_time_wrong10`)
- 회의 결과: `room13` → partial (`r13_v111_owner_wrong10`)
- 회의/대조 「이 핀을 구별할 수 있는가」 (키 `구리선과 수선 출처를 대조한다`, 회의 room13, 기회 7, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E08_WOUND_WIRE", "E09_PIN_OWNER"] · 대체 [["E08_CONTACT_ASSEMBLY", "E09_PIN_OWNER"]] · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 할머니는 시장에서 한 줌씩 파는 흔한 핀이라고 한다. ……‘흔한’ 핀이라는 그 부분, 맞나?
    - 이김 → `r13_v111_owner_answer10` {"jumps": [["r13_v111_owner_tok10", "if r13_v111_tok_attends(\"hearing\")"], ["r13_v111_owner_copy10", null]]}
    - 틀림 → `r13_v111_owner_wrong10` {"meeting_end": [{"meeting": "room13", "result": "partial", "when": null}], "sets": [["room13_partial_kind", "unknown", null]], "jumps": [["r13_v111_owner_proof10", "if r13_nw_retry(\"room13\",['E08_WOUND_WIRE', 'E09_PIN_OWNER'],'half_room13_owner10')"], ["r13_v111_bench10", null]], "retry": ["r13_nw_retry(\"room13\",['E08_WOUND_WIRE', 'E09_PIN_OWNER'],'half_room13_owner10')"]}
- 회의/대조 「핀이 언제 떨어졌는가」 (키 `첫 비명 뒤 핀을 다시 채운 때`, 회의 room13, 기회 7, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E09_PIN_TIME", "E09_PIN_HANDOVER_TIME"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 할머니는 낮에 방을 치울 때 떨어졌을 거라고 한다. ……‘낮에’라는 그 부분, 내가 가진 것과 맞나?
    - 이김 → `r13_v111_time_answer10` {"sets": [["pin_after_cry", "grandmother_scarf_testimony", null], ["grandmother_kitchen_move", "admitted", null], ["D10_S03_time_answer_completed", true, null], ["grandmother_passage_entry", "admitted", null], ["D10_S03_entry_admission_completed", true, null]], "jumps": [["r13_v111_contact_proof10", null]]}
    - 틀림 → `r13_v111_time_wrong10` {"meeting_end": [{"meeting": "room13", "result": "partial", "when": null}], "sets": [["room13_partial_kind", "unknown", null]], "jumps": [["r13_v111_time_proof10", "if r13_nw_retry(\"room13\",['E09_PIN_TIME', 'E09_PIN_HANDOVER_TIME'],'half_room13_time10')"], ["r13_v111_bench10", null]], "retry": ["r13_nw_retry(\"room13\",['E09_PIN_TIME', 'E09_PIN_HANDOVER_TIME'],'half_room13_time10')"]}
- 회의/대조 「방금 설명은 물증과 맞는가」 (키 `접촉면과 아이의 위치를 대조한다`, 회의 room13, 기회 7, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E08_CONTACT_ASSEMBLY", "E08_WOUND_WIRE", "E08_CHILD_POSITION", "E08_ROOM_REACH", "E09_SCARF"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 할머니는 핀이 ‘그때 걸렸나 보다’고 한다. 촛대를 집다가 저절로 걸렸다는 투다. ……그 부분이 내가 가진 것과 맞나?
    - 이김 → `r13_v111_contact_answer10` {"meeting_end": [{"meeting": "room13", "result": "win", "when": null}], "sets": [["pin_transfer", "intentional_refastening_through_cloth_ring_admitted", null], ["fatal_contact_assembly", "matched_break_and_wound_edge", null], ["same_moment_fatal_contact", "authored_material_chain", null], ["child_upper_reuse", "refuted", null], ["D10_contact_limit_completed", true, null], ["D10_S03_contact_limit_completed", true, null], ["grandmother_records_confrontation", "admitted", null], ["fatal_contact_responsibility", "grandmother", null]], "jumps": [["r13_v111_bench10", null]]}
    - 틀림 → `r13_v111_contact_wrong10` {"meeting_end": [{"meeting": "room13", "result": "partial", "when": null}], "sets": [["room13_partial_kind", "accident", null]], "jumps": [["r13_v111_contact_proof10", "if r13_nw_retry(\"room13\",['E08_CONTACT_ASSEMBLY', 'E08_WOUND_WIRE', 'E08_CHILD_POSITION', 'E08_ROOM_REACH', 'E09_SCARF'],'half_room13_contact10')"], ["r13_v111_bench10", null]], "retry": ["r13_nw_retry(\"room13\",['E08_CONTACT_ASSEMBLY', 'E08_WOUND_WIRE', 'E08_CHILD_POSITION', 'E08_ROOM_REACH', 'E09_SCARF'],'half_room13_contact10')"]}

### MS14_D10_S04 10-4. 오후 / 우체국 옆 벤치 — 다음에 갈 곳

- 원본 시간·장소: ["POST_BENCH", "SCHOOL_ROOM"] · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("D10_confrontation_release_completed") is True and r13_v111_value("DARAM_DETAINED") is False`
- label: `r13_v111_bench10`, `r13_v111_sleep10`, `r13_v111_kkomi_acorn10`, `r13_v111_sleep10_input`, `r13_v111_sleep10_done`
- 장소: post, school · 원본 등장: nabi, daram, buri, seryeon, father · 무대 세우기: ["daram", "seryeon", "buri", "nabi"] ["kid_kkomi"]
- 대사: 원문 ID 24개, 묶음 kkomi_acorn10, 펼친 줄 51, rpy 직접 줄 0
- 그림: 배경 post=room13-pixel-wide-post-morning.webp; school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 자료: E10_PUMP 6일에 마지막 쓴 연락함(observed)
- 상태 값 쓰기: `E10_PUMP`, `FAMILY_BASE`, `mother_location`, `D10_S04_main_completed`, `kkomi_acorn10`, `day`
- 대기 관문 `sleep10_input` (장소 school, 인물 ["daram"])
    - [0] 잠자리를 정리한다 — 물건 blankets@school → jump r13_v111_sleep10_done

### MS14_D10_P01 10-P. 예방 대체 / 그 종이를 넘기기 전에

- 원본 시간·장소: ["HALL", "POST_BENCH"] · 생각(목표 문구): 가족이라는 말만으로 이 종이를 받을 권리가 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("route7")=="prevented" and r13_v111_value("OWL_ALIVE") is True`
- label: `r13_v111_prevent_hearing10`, `r13_v111_authority_proof10`, `r13_v111_authority_answer10`, `r13_v111_writing_proof10`, `r13_v111_writing_answer10`, `r13_v111_pocket10`, `r13_v111_pocket_answer10`, `r13_v111_family_paper10`, `r13_v111_private_handoff10`, `r13_v111_owl_invitation10`, `r13_v111_public_paper10`, `r13_v111_writing_wrong10`, `r13_v111_writing_partial10`, `r13_v111_authority_wrong10`
- 장소: school · 원본 등장: daram, owl, seryeon, sling, father, grandmother · 무대 세우기: ["daram", "resident_owlgp", "granny", "resident_ppul", "neoul", "resident_sling", "seryeon"] ["daram", "resident_owlgp", "granny", "seryeon"]
- 대사: 원문 ID 63개, 묶음 없음, 펼친 줄 99, rpy 직접 줄 1
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 자료: E10_PUMP 6일에 마지막 쓴 연락함(observed)
- 상태 값 쓰기: `D10_P01_stop_handover_completed`, `D10_P01_authority_question_completed`, `proxy_receipt_authority`, `last_page_holder`, `D10_P01_authority_answer_completed`, `D10_P01_writing_question_completed`, `invitation_current_authorization`, `D10_P01_writing_answer_completed`, `D10_P01_pocket_question_completed`, `D10_P01_pocket_challenge_completed`, `separate_page_observed`, `public_board_count_match`, `route_face_visible_to_crowd`, `D10_P01_private_count_completed`, `owl_invitation_testimony`, `E10_PUMP`, `mother_secret_shared`, `OWL_ALIVE`, `DARAM_DETAINED`, `D10_P01_family_delivery_completed`
- 회의 결과: `records` → win (`r13_v111_writing_answer10`)
- 회의 결과: `records` → partial (`r13_v111_writing_wrong10`)
- 회의 결과: `records` → lose (`r13_v111_authority_wrong10`)
- 이송 명단에 적음: resident_owlgp (records_lose, `r13_v111_authority_wrong10`)
- 메뉴(`r13_v111_pocket_answer10`, menu): 가족끼리 확인하고, 왜 숨겼는지 묻는다 / 공개된 수량만 대조하고 기록을 받는다
- 대기 관문 `pocket10` (장소 school, 인물 ["resident_owlgp"])
    - [0] 어제는 전부라고 하셨습니다. — 사람 resident_owlgp@school → jump r13_v111_pocket_answer10
- 대기 관문 `private_handoff10` (장소 school, 인물 ["daram", "resident_owlgp", "granny"])
    - [0] 아내가 직접 편지를 건넸습니까? — 사람 resident_owlgp@school → jump r13_v111_owl_invitation10
    - [1] 공개 수치만 대조하고 인계해 주십시오. — 사람 resident_owlgp@school → jump r13_v111_public_paper10
- 회의/대조 「수신인과 가족 전달 권한을 구분한다」 (키 `수신인과 가족 전달 권한을 구분한다`, 회의 records, 기회 4, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E06_CONTACT", "E09_MAIL"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 할머니는 아내가 가족에게 전할 것을 늘 자기에게 맡겼다고 한다. ……그 부분이 내가 가진 것과 맞나?
    - 이김 → `r13_v111_authority_answer10` {"sets": [["proxy_receipt_authority", "unconfirmed", null], ["last_page_holder", "OWL", null], ["D10_P01_authority_answer_completed", true, null], ["D10_P01_writing_question_completed", true, null]], "jumps": [["r13_v111_writing_proof10", null]]}
    - 틀림 → `r13_v111_authority_wrong10` {"meeting_end": [{"meeting": "records", "result": "lose", "when": null}], "listed": [{"person": "resident_owlgp", "reason": "records_lose", "when": null}], "sets": [["E10_PUMP", "private_contact_box_last_used_day6", null], ["last_page_holder", "family", null], ["mother_secret_shared", false, null], ["OWL_ALIVE", true, null], ["DARAM_DETAINED", false, null], ["D10_P01_family_delivery_completed", true, null]], "acquires": ["E10_PUMP"], "jumps": [["r13_v111_authority_proof10", "if r13_nw_retry(\"records\",['E06_CONTACT', 'E09_MAIL'],'half_records_authority10')"], ["r13_v111_prevent_return10", null]], "retry": ["r13_nw_retry(\"records\",['E06_CONTACT', 'E09_MAIL'],'half_records_authority10')"]}
- 회의/대조 「그 초대장을 아내가 보냈다고 할 수 있는가」 (키 `반송·필사본·초대 발송을 대조한다`, 회의 records, 기회 4, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E01", "E07", "E09_MAIL"] · 대체 [["E01", "E27", "E09_MAIL"]] · 덧붙임 허용 ["E07", "E27", "E09"]
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 할머니는 나도 ‘부인 글씨’라고 했다고 한다. ……글씨가 닮았다는 그 부분, 내가 가진 것과 맞나?
    - 이김 → `r13_v111_writing_answer10` {"meeting_end": [{"meeting": "records", "result": "win", "when": null}], "sets": [["invitation_current_authorization", "unproven", null], ["D10_P01_writing_answer_completed", true, null], ["D10_P01_pocket_question_completed", true, null]], "jumps": [["r13_v111_pocket10", null]]}
    - 틀림 → `r13_v111_writing_wrong10` {"meeting_end": [{"meeting": "records", "result": "partial", "when": null}], "jumps": [["r13_v111_writing_proof10", "if r13_nw_retry(\"records\",['E01', 'E07', 'E09_MAIL'],'half_records_writing10')"], ["r13_v111_writing_partial10", null]], "retry": ["r13_nw_retry(\"records\",['E01', 'E07', 'E09_MAIL'],'half_records_writing10')"]}

### MS14_D10_S04P 반드시 실장할 짧은 대체 대사

- 원본 시간·장소: ["SCHOOL_ROOM"] · 생각(목표 문구): 
- label: `r13_v111_prevent_return10`
- 장소: school · 원본 등장: daram, father · 무대 세우기: ["daram"]
- 대사: 원문 ID 4개, 묶음 없음, 펼친 줄 7, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 상태 값 쓰기: `FAMILY_BASE`, `OWL_ALIVE`, `DARAM_DETAINED`, `D10_S04P_main_completed`

## 11일

### MS14_D11_S00 장면 11-0. 셋째 말뚝 아래

- 원본 시간·장소: 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 · 생각(목표 문구): 마지막으로 사용한 연락함에 지금 답이 남아 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_owned("E10_PUMP")`
- label: `r13_v111_day11`, `r13_v111_pump_open11`, `r13_v111_pump_reply11`
- 장소: school, forest · 원본 등장: 까로, 다람, 아빠 · 무대 세우기: ["daram", "karo"]
- 대사: 원문 ID 10개, 묶음 없음, 펼친 줄 23, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp; forest=room13-pixel-wide-forest-afternoon.webp, room13-pixel-wide-forest-evening.webp, room13-pixel-wide-forest-morning.webp
- 상태 값 쓰기: `root_address_known`
- 대기 관문 `pump_open11` (장소 forest, 인물 ["daram", "karo"])
    - [0] 셋째 말뚝 아래 통을 연다 — 물건 v111_box@forest → jump r13_v111_pump_reply11

### MS14_D11_S01 장면 11-1. 빈 뿌리 집

- 원본 시간·장소: 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 · 생각(목표 문구): 토실이 안전하게 기다릴 곳은 정해졌을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("root_address_known") is True`
- label: `r13_v111_root11`, `r13_v111_root_note11`, `r13_v111_root_read11`, `r13_v111_tosil_detained11`, `r13_v111_tosil_free11`, `r13_v111_nabi_waiting11`, `r13_v111_nabi_wait11`, `r13_v111_nabi_arrival11`, `r13_v111_tosil_handoff11`, `r13_v111_tosil_safe11`
- 장소: forest, school · 원본 등장: 나비, 다람, 아빠, 토실 · 무대 세우기: ["daram", "resident_tosil"] ["daram", "resident_tosil", "nabi"]
- 대사: 원문 ID 41개, 묶음 없음, 펼친 줄 47, rpy 직접 줄 0
- 그림: 배경 forest=room13-pixel-wide-forest-afternoon.webp, room13-pixel-wide-forest-evening.webp, room13-pixel-wide-forest-morning.webp; school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 상태 값 쓰기: `greenhouse_address_known`, `tosil_safe_handoff_confirmed`, `tosil_location`, `tosil_knows_greenhouse`
- 대기 관문 `root_note11` (장소 forest, 인물 ["daram", "resident_tosil"])
    - [0] 눌러 둔 돌 아래 쪽지를 본다 — 물건 forest_roots@forest → jump r13_v111_root_read11
- 대기 관문 `nabi_wait11` (장소 school, 인물 ["daram", "resident_tosil"])
    - [0] 나비가 올 때까지 토실과 기다린다 — 물건 desks@school → jump r13_v111_nabi_arrival11
- 대기 관문 `tosil_handoff11` (장소 school, 인물 ["daram", "resident_tosil", "nabi"])
    - [0] 토실의 보호를 부탁합니다. — 사람 nabi@school → jump r13_v111_tosil_safe11

### MS14_D11_S02 장면 11-2. 폐온실의 낮은 문

- 원본 시간·장소: 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("tosil_safe_handoff_confirmed") is True and r13_v111_value("greenhouse_address_known") is True`
- label: `r13_v111_reunion11`
- 장소: greenhouse · 원본 등장: 다람, 아빠, 엄마 · 무대 세우기: ["daram", "mom"]
- 대사: 원문 ID 14개, 묶음 없음, 펼친 줄 19, rpy 직접 줄 0
- 그림: 배경 greenhouse=room13-pixel-ready-greenhouse0177-afternoon.webp, room13-pixel-ready-greenhouse0177-evening.webp, room13-pixel-ready-greenhouse0177-morning.webp · 컷 v111_reunion_far, v111_reunion_close
- 상태 값 쓰기: `family_reunited`

### MS14_D11_S02A 장면 11-2A. 마를 때까지

- 원본 시간·장소: 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("family_reunited") is True`
- label: `r13_v111_dry11`, `r13_v111_coat_use11`, `r13_v111_dry_done11`, `r13_v111_blanket_use11`, `r13_v111_blanket_one11`, `r13_v111_blanket_keep11`
- 장소: greenhouse · 원본 등장: 다람, 아빠, 엄마 · 무대 세우기: ["daram", "mom"]
- 대사: 원문 ID 27개, 묶음 없음, 펼친 줄 28, rpy 직접 줄 0
- 그림: 배경 greenhouse=room13-pixel-ready-greenhouse0177-afternoon.webp, room13-pixel-ready-greenhouse0177-evening.webp, room13-pixel-ready-greenhouse0177-morning.webp · 컷 ev:PROP_D11_child_wet_socks
- 메뉴(`r13_v111_dry11`, menu): 두 장을 꺼내 덮는다 / 한 장을 함께 덮는다 / 짐 안에 둔다 / 외투 안쪽을 함께 덮는다

### MS14_D11_S02B 장면 11-2B. 단추 하나

- 원본 시간·장소: 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 · 생각(목표 문구): 아내가 돌아오지 못한 이유는 무엇일까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("family_reunited") is True`
- label: `r13_v111_button11`, `r13_v111_mother_questions11`, `r13_v111_mother_life11`, `r13_v111_mother_ready11`, `r13_v111_mother_last11`, `r13_v111_forgery_question11`, `r13_v111_owl_question11`, `r13_v111_mother_invitation11`, `r13_v111_mother_return11`
- 장소: greenhouse · 원본 등장: 다람, 아빠, 엄마 · 무대 세우기: ["daram", "mom"]
- 대사: 원문 ID 49개, 묶음 없음, 펼친 줄 68, rpy 직접 줄 0
- 그림: 배경 greenhouse=room13-pixel-ready-greenhouse0177-afternoon.webp, room13-pixel-ready-greenhouse0177-evening.webp, room13-pixel-ready-greenhouse0177-morning.webp · 컷 ev:PROP_D11_sewing_needle_thread
- 상태 값 쓰기: `mother_q_life`, `mother_q_invitation`, `mother_q_return`
- 대기 관문 `mother_questions11` (장소 greenhouse, 인물 ["daram", "mom"])
    - [0] 어떻게 지냈어? — 사람 mom@greenhouse → jump r13_v111_mother_life11
    - [1] 왜 우리를 부르지 않았어? — 사람 mom@greenhouse → jump r13_v111_mother_invitation11
    - [2] 왜 돌아오지 못했어? — 사람 mom@greenhouse → jump r13_v111_mother_return11

### MS14_D11_S03 장면 11-3. 열이 있는 물건

- 원본 시간·장소: 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 · 생각(목표 문구): 지금 가진 열과 운반 인력으로 누구의 자리를 먼저 마련할 수 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("family_reunited") is True`
- label: `r13_v111_facility11`, `r13_v111_guldol_heat11`, `r13_v111_mother_heat11`, `r13_v111_heat_check11`, `r13_hidden_base_marks11`, `r13_v111_heat_seen11`, `r13_v111_family_blankets11`, `r13_v111_no_blankets11`, `r13_v111_family_place11`, `r13_v111_family_place_check11`, `r13_v111_family_place_done11`, `r13_v111_school_visit11`, `r13_v111_family_space_after_supply11`, `r13_v111_family_space_checked11`, `r13_v111_family_space_ready11`, `r13_v111_blanket_choice11`, `r13_v111_blanket_store11`, `r13_v111_hypothesis11`, `r13_v111_hyp0_menu11`, `r13_v111_hyp0_sick11`, `r13_v111_hyp_lost_gate11`, `r13_v111_hyp_end11`, `r13_v111_hyp0_call11`, `r13_v111_hyp0_won11`, `r13_v111_hyp1_q11`, `r13_v111_hyp1_reason11`, `r13_v111_hyp1_proof11`, `r13_v111_hyp1_won11`, `r13_v111_hyp2_q11`, `r13_v111_hyp2_badreason11`, `r13_v111_hyp2_lost11`, `r13_v111_hyp3_q11`, `r13_v111_hyp3_badreason11`, `r13_v111_hyp3_lost11`, `r13_v111_hyp4_q11`, `r13_v111_hyp4_reason11`, `r13_v111_hyp4_proof11`, `r13_v111_hyp4_won11`, `r13_v111_hyp5_q11`, `r13_v111_hyp5_reason11`, `r13_v111_hyp5_proof11`, `r13_v111_hyp5_won11`, `r13_v111_hyp5_wrong11`, `r13_v111_hyp5_lost11`, `r13_v111_hyp5_after_lost11`, `r13_v111_hyp5_badreason11`, `r13_v111_hyp4_wrong11`, `r13_v111_hyp4_lost11`, `r13_v111_hyp4_badreason11`, `r13_v111_hyp3_reason11`, `r13_v111_hyp3_proof11`, `r13_v111_hyp3_won11`, `r13_v111_hyp3_wrong11`, `r13_v111_hyp2_reason11`, `r13_v111_hyp2_proof11`, `r13_v111_hyp2_won11`, `r13_v111_hyp2_wrong11`, `r13_v111_hyp1_wrong11`, `r13_v111_hyp1_lost11`, `r13_v111_hyp1_badreason11`, `r13_v111_hyp0_old11`, `r13_v111_tosil_blanket11`, `r13_v111_tosil_blanket_remaining11`, `r13_v111_tosil_blanket_last11`, `r13_v111_rescue_prepare11`, `r13_v111_rescue_cart11`, `r13_v111_rescue_ready11`, `r13_v111_day_rescue11`, `r13_v111_day_rescue_door11`, `r13_v111_day_rescue_school11`, `r13_v111_supply_school11`, `r13_v111_bowl_cart11`, `r13_v111_bowl_pocket11`
- 장소: facility, school, square, forest · 원본 등장: 굴돌, 나비, 네로, 다람, 선생님, 아랫길 주민, 아빠, 엄마, 초롱, 토실 · 무대 세우기: ["daram", "mom", "resident_guldol", "resident_lamplighter"] ["mom", "daram", "nabi", "resident_teacher"] ["mom", "daram", "nabi", "resident_teacher", "resident_tosil"] ["daram", "resident_teacher", "guard", "resident_madam", "npc_pandol", "resident_lamplighter", "resident_owlgp"] ["mom", "daram", "karo", "resident_nero", "resident_lamplighter"] ["mom", "daram", "resident_teacher", "nabi"]
- 대사: 원문 ID 42개, 묶음 warm_recall11, hidden_base_marks11, mural_tablet11, mural_names11, hyp_open11, hyp0_sick11, hyp_lose11, hyp_result11, hyp0_call11, hyp0_won11, hyp1_q11, hyp1_reason11, hyp1_won11, hyp2_q11, hyp2_lost11, hyp3_q11, hyp3_lost11, hyp4_q11, hyp4_reason11, hyp4_won11, hyp5_q11, hyp5_reason11, hyp5_won11, hyp_chief11, hyp5_lost11, hyp4_lost11, hyp3_reason11, hyp3_won11, hyp2_reason11, hyp2_won11, hyp1_lost11, hyp0_old11, nr_cart11, nr_cover11, nr_driver11, nr_lights11, nr_seat11, nr_seat_nabi11, bowl_cart_again11, nr_missing11, bowl_cart11, bowl_pocket11, 펼친 줄 213, rpy 직접 줄 0
- 그림: 배경 facility=room13-pixel-ready-facility0177-afternoon.webp, room13-pixel-ready-facility0177-evening.webp, room13-pixel-ready-facility0177-morning.webp; school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp; square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp; forest=room13-pixel-wide-forest-afternoon.webp, room13-pixel-wide-forest-evening.webp, room13-pixel-wide-forest-morning.webp · 컷 ev:HIDDEN_A3_paper_marked, ev:NW_TABLET_A, ev:NW_NAMES
- 자료: NW_TABLET_A 깨진 돌판(observed), NW_NAMES 벽에 새긴 이름들(observed), NW_SICK_BEDS 학교 침상 목록의 꽃 표시(observed), E14_SUPPLY 학교 장작 인수 기록(observed)
- 상태 값 쓰기: `guldol_facility_seen`, `hidden_base:marks_copied`, `heat_inventory_observed`, `family_school_place`, `hyp_issue:1`, `hyp_issue:2`, `hyp_issue:3`, `hyp_issue:4`, `rescue_preparation_schema11`, `rescue_cart_ready`, `rescue_cover_ready`, `rescue_driver_ready`, `rescue_lights_ready`, `rescue_school_ready11`, `lower_road_arrived11`, `rescue_handoff_period11`, `school_supply_handed`, `school_heat_connected`, `grand_bowl_seen11`, `grand_bowl_pocket`
- 회의 결과: `hypothesis` → lose (`r13_v111_hyp_lost_gate11`)
- 회의 결과: `hypothesis` → {"expr": "'win' if all((r13_v111_value('hyp_issue:%d' % i) == 'won' for i in (1, 2, 3, 4))) else 'partial'"} (`r13_v111_hyp5_won11`)
- 회의 결과: `hypothesis` → partial (`r13_v111_hyp5_after_lost11`)
- 이송 명단에 적음: resident_guldol (facility, `r13_v111_hyp_end11`)
- 메뉴(`r13_v111_heat_seen11`, display_menu): 벽 아래 깨진 돌판을 들여다본다
- 메뉴(`r13_v111_heat_seen11`, display_menu): 그림 옆 벽에 새긴 글씨를 본다
- 메뉴(`r13_v111_heat_seen11`, menu): 가족 자리부터 본다 / 아랫길 대피 준비를 확인한다 / 준비된 물자를 학교로 옮긴다
- 메뉴(`r13_v111_blanket_choice11`, menu): 가족 짐에 보관한다 / 토실에게 한 장을 건넨다
- 메뉴(`r13_v111_hyp0_menu11`, menu): 야생화는 옮는 병이다 / 아르카가 사람을 부른다 / 꺼낸 아르카 곁에 오래 있던 사람부터 무너진다 / 늙으면 누구나 그렇게 된다
- 메뉴(`r13_v111_hyp1_q11`, menu): 두 사람이 아르카 곁에 머문 시간을 비교한다 / 두 사람의 나이와 몸 상태를 비교한다 / 두 사람이 아르카를 만진 방식을 비교한다
- 메뉴(`r13_v111_hyp2_q11`, menu): 켜지 않고 쌓아 둔 돌은 아무 해가 없다 / 백 부인은 그 돌 곁에서 잠을 자지 않는다 / 백 부인은 돌을 팔기만 한다
- 메뉴(`r13_v111_hyp3_q11`, menu): 요즘 사람들이 약해졌다 / 외지 사람이 병을 들여왔다 / 요즘 태우는 돌이 더 독하다
- 메뉴(`r13_v111_hyp4_q11`, menu): 아이들이 밤을 어디서 보내는지 본다 / 아이와 어른의 몸을 비교한다 / 아이들이 아르카를 어떻게 다루는지 본다
- 메뉴(`r13_v111_hyp5_q11`, menu): 한 방의 돌이 바뀌자 한 사람이 한 저녁 사이에 무너졌다 / 한 방의 돌을 치우자 무너지던 사람이 돌아왔다 / 한 방의 돌을 꺼내자 그 앞에서 흐려지던 머리가 맑아졌다 / 부엉이 어르신은 원래 아팠다 / 13호가 추워서 그렇다
- 대기 관문 `heat_check11` (장소 facility, 인물 ["daram", "mom", "resident_guldol", "resident_lamplighter", "guard", "karo"])
    - [0] 벽 그림과 돌판을 확인한다 — 물건 v111_mural@facility → jump r13_v111_heat_seen11
    - [100] 종이와 벽의 자국을 맞춰 본다 — 물건 v111_mural@facility · 조건 값 hidden_base:paper == true; 값 hidden_base:plate == true; 값 hidden_base:marks_copied == null → call r13_hidden_base_marks11; jump r13_v111_heat_check11
- 대기 관문 `family_place_check11` (장소 school, 인물 ["mom", "daram", "nabi", "resident_teacher"])
    - [0] 가족 세 사람이 쓸 자리를 확인한다 — 물건 blankets@school → jump r13_v111_family_place_done11
- 대기 관문 `family_space_after_supply11` (장소 school, 인물 ["mom", "daram", "nabi", "resident_teacher"])
    - [0] 가족 세 사람의 실제 자리를 확인한다 — 물건 blankets@school → jump r13_v111_family_space_checked11
- 대기 관문 `rescue_cart11` (장소 square, 인물 ["mom", "daram", "karo", "resident_nero", "resident_lamplighter"])
    - [0] 수레를 끌고 아랫길로 간다 — 물건 cart@square → jump r13_v111_rescue_ready11
    - [1] 수레 짐칸을 살핀다 — 물건 cart@square · 조건 값 grand_bowl_seen11 == null → call r13_v111_bowl_cart11
    - [2] 그릇 하나를 집는다 — 물건 cart@square · 조건 값 grand_bowl_seen11 == true; 값 grand_bowl_pocket == null → call r13_v111_bowl_pocket11
    - [3] 짐칸을 다시 본다 — 물건 cart@square · 조건 값 grand_bowl_seen11 == true; 값 grand_bowl_pocket == null → 대사 bowl_cart_again11
    - [80] 수레 짐을 내려 자리를 비운다 — 물건 cart@square · 조건 값 rescue_cart_ready == null → 대사 nr_cart11; set rescue_cart_ready=True
    - [81] 덮개를 접어 빈 짐칸에 싣는다 — 물건 cart@square · 조건 값 rescue_cart_ready == true; 값 rescue_cover_ready == null → 대사 nr_cover11; set rescue_cover_ready=True
    - [82] 까로 씨, 수레를 끌어 주시겠습니까? — 사람 karo@square · 조건 값 rescue_cart_ready == true; 값 rescue_driver_ready == null → 대사 nr_driver11; set rescue_driver_ready=True
    - [83] 아랫길을 비추는 등을 점검한다 — 물건 lamp@square · 조건 값 rescue_lights_ready == null → 대사 nr_lights11; set rescue_lights_ready=True
    - [84] 아랫길 세 사람의 받을 자리를 비운다 — 물건 blankets@school · 조건 값 rescue_school_ready11 == null → set rescue_school_ready11=True
    - [85] 먼저 학교 물자를 인계한다 — 물건 cart@square → jump r13_v111_supply_school11
- 대기 관문 `day_rescue_door11` (장소 forest, 인물 ["karo", "resident_nero"])
    - [0] 아랫길 사람들의 문을 연다 — 물건 v111_lower_door@forest → jump r13_v111_day_rescue_school11
- 회의/대조 「초롱과 피코의 하루를 대조한다」 (키 `초롱과 피코의 하루를 대조한다`, 회의 hypothesis, 기회 13, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E11", "E08", "NW_PIKO_TREMOR"] · 대체 [["E11", "NW_PIKO_TREMOR"], ["NW_LA_CHECK", "E08", "NW_PIKO_TREMOR"], ["NW_LA_CHECK", "NW_PIKO_TREMOR"]] · 덧붙임 허용 ["E08", "E28"]
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 돌목 씨는 날마다 만지는 초롱 씨가 멀쩡하다고 한다. ……그 ‘날마다’가 어떤 하루인지, 내가 가진 것과 맞나?
    - 이김 → `r13_v111_hyp1_won11` {"sets": [["hyp_issue:1", "won", null]], "jumps": [["r13_v111_hyp2_q11", null]]}
    - 틀림 → `r13_v111_hyp1_wrong11` {"jumps": [["r13_v111_hyp1_proof11", "if r13_nw_retry(\"hypothesis\",['E11', 'E08', 'NW_PIKO_TREMOR'],'half_hyp1_11')"], ["r13_v111_hyp1_lost11", null]], "retry": ["r13_nw_retry(\"hypothesis\",['E11', 'E08', 'NW_PIKO_TREMOR'],'half_hyp1_11')"]}
- 회의/대조 「아르카가 없는 아이들과 대조한다」 (키 `아르카가 없는 아이들과 대조한다`, 회의 hypothesis, 기회 13, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["NW_KKOMI_NOSTONE", "NW_SICK_BEDS"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 주민은 ‘우리 애가 무슨 죄냐’고 한다. 아이 몸이 약해서라는 투다. ……그 부분이 내가 가진 것과 맞나?
    - 이김 → `r13_v111_hyp4_won11` {"sets": [["hyp_issue:4", "won", null]], "jumps": [["r13_v111_hyp5_q11", null]]}
    - 틀림 → `r13_v111_hyp4_wrong11` {"jumps": [["r13_v111_hyp4_proof11", "if r13_nw_retry(\"hypothesis\",['NW_KKOMI_NOSTONE', 'NW_SICK_BEDS'],'half_hyp4_11')"], ["r13_v111_hyp4_lost11", null]], "retry": ["r13_nw_retry(\"hypothesis\",['NW_KKOMI_NOSTONE', 'NW_SICK_BEDS'],'half_hyp4_11')"]}
- 회의/대조 「아르카가 사람을 무너뜨리는 것을 직접 본 일이 있는가」 (키 `13호 난로의 돌을 내놓는다`, 회의 hypothesis, 기회 13, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["NW_STONE"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 선생님은 ‘직접 본 사람’을 찾는다. ……그 물음에 말 말고 손에 쥔 것으로 답할 수 없나?
    - 이김 → `r13_v111_hyp5_won11` {"meeting_end": [{"meeting": "hypothesis", "result": {"expr": "'win' if all((r13_v111_value('hyp_issue:%d' % i) == 'won' for i in (1, 2, 3, 4))) else 'partial'"}, "when": null}], "jumps": [["r13_v111_hyp_end11", null]]}
    - 틀림 → `r13_v111_hyp5_wrong11` {"jumps": [["r13_v111_hyp5_proof11", "if r13_nw_retry(\"hypothesis\")"], ["r13_v111_hyp5_lost11", null]], "retry": ["r13_nw_retry(\"hypothesis\")"]}
- 회의/대조 「요즘 돌이 어디서 오는지 대조한다」 (키 `요즘 돌이 어디서 오는지 대조한다`, 회의 hypothesis, 기회 13, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["NW_INNER_PRICE", "NW_MUSOE_DEEP"] · 대체 없음 · 덧붙임 허용 ["E14"]
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 판돌 씨 말로는 옛날부터 같은 아르카를 써 왔다. ……그 ‘같은’이 내 수첩과 맞나?
    - 이김 → `r13_v111_hyp3_won11` {"sets": [["hyp_issue:3", "won", null]], "jumps": [["r13_v111_hyp4_q11", null]]}
    - 틀림 → `r13_v111_hyp3_wrong11` {"jumps": [["r13_v111_hyp3_proof11", "if r13_nw_retry(\"hypothesis\",['NW_INNER_PRICE', 'NW_MUSOE_DEEP'],'half_hyp3_11')"], ["r13_v111_hyp3_lost11", null]], "retry": ["r13_nw_retry(\"hypothesis\",['NW_INNER_PRICE', 'NW_MUSOE_DEEP'],'half_hyp3_11')"]}
- 회의/대조 「돌이 산더미인 그 창고 곁에서는 정말 아무도 무너지지 않았는가」 (키 `창고에서 잠자는 사람을 짚는다`, 회의 hypothesis, 기회 13, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["NW_KEEPER_DATE"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 백 부인은 그 창고 곁에서 멀쩡한 사람으로 자기만 든다. ……그 창고에 부인만 있었나?
    - 이김 → `r13_v111_hyp2_won11` {"sets": [["hyp_issue:2", "won", null]], "jumps": [["r13_v111_hyp3_q11", null]]}
    - 틀림 → `r13_v111_hyp2_wrong11` {"jumps": [["r13_v111_hyp2_proof11", "if r13_nw_retry(\"hypothesis\",['NW_KEEPER_DATE'],None)"], ["r13_v111_hyp2_lost11", null]], "retry": ["r13_nw_retry(\"hypothesis\",['NW_KEEPER_DATE'],None)"]}

### MS14_D11_S04 장면 11-4. 문이 열려 있어야 하는 밤

- 원본 시간·장소: 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 · 생각(목표 문구): 아랫길 사람들은 스스로 올라올 수 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("family_school_place") is True`
- label: `r13_v111_night11`, `r13_v111_rest_blanket11`, `r13_v111_night_rescue_route11`, `r13_v111_rescue_handoff11`, `r13_v111_sleep11`, `r13_v111_sleep11_input`, `r13_hp_visit11`, `r13_hp_house11_wait`, `r13_hp_house11_pick`, `r13_hp_wood11`, `r13_v111_sleep11_done`, `r13_v111_lower_safe11`, `r13_v111_request_rescue11`, `r13_v111_night_rescue_prepare11`, `r13_v111_late_supply11`, `r13_v111_late_supply_handoff11`, `r13_v111_late_supply_done11`, `r13_v111_late_road11`, `r13_v111_night_rescue_choices11`, `r13_v111_night_rescue11`, `r13_v111_snow_door11`, `r13_v111_night_rescue_done11`, `r13_v111_late_cart11`
- 장소: school, hidden_pandol, forest · 원본 등장: 까로, 네로, 다람, 선생님, 아랫길 주민, 아빠, 엄마 · 무대 세우기: ["mom", "daram", "resident_teacher", "karo", "resident_nero"] ["mom", "daram", "resident_teacher", "nabi", "karo", "resident_nero"] ["npc_pandol"] ["resident_teacher"] ["karo"] ["karo", "resident_nero"]
- 대사: 원문 ID 25개, 묶음 night_lights11, nr_handoff11, nr_pending11, hp_visit11, hp_look11, hp_consent11, hp_place11, hp_replace11, hp_tongs11, hp_no_wood11, hp_wood11, lower_elder11, 펼친 줄 71, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp; hidden_pandol=배경 키 ms14_somi_inside 의 파일은 옛 r13_background 경로(room13_life.rpy 등)로 정해짐 — 미확인; forest=room13-pixel-wide-forest-afternoon.webp, room13-pixel-wide-forest-evening.webp, room13-pixel-wide-forest-morning.webp · r13_scene [{"expr": "R13_PLACES[room13['location']][1]"}, {"expr": "R13_PLACES[room13['location']][0]"}] · 컷 ev:PROP_D11_blank_name_tag_bundle
- 자료: E14_SUPPLY 학교 장작 인수 기록(observed)
- 상태 값 쓰기: `lower_lights_cut`, `rescue_handoff_period11`, `lower_road_handover`, `nero_alive`, `alive:v111_lowerroad_elder`, `day`, `school_supply_handed`, `school_heat_connected`, `lower_road_lost`, `location:resident_nero`, `lower_road_arrived11`
- 갈림길 운명: ["fate_nero", "handover"] (`r13_v111_rescue_handoff11`)
- 갈림길 운명: ["fate_nero", "rescue"] (`r13_v111_rescue_handoff11`)
- 갈림길 운명: ["fate_nero", "handover"] (`r13_v111_lower_safe11`)
- 갈림길 운명: ["fate_nero", "lost"] (`r13_v111_late_road11`)
- 대기 관문 `rescue_handoff11` (장소 school, 인물 ["mom", "daram", "resident_teacher", "karo", "resident_nero", "nabi"])
    - [0] 세 사람을 맞은 자리와 명단을 확인한다 — 물건 blankets@school → 대사 nr_handoff11; set lower_road_handover=3; set nero_alive=True; set alive:v111_lowerroad_elder=True; r13_fork_set_fate ['fate_nero', 'rescue']; jump r13_v111_sleep11
    - [1] 학교 안에서 받을 사람을 기다린다 — 물건 blankets@school → 대사 nr_pending11; jump r13_v111_sleep11
- 대기 관문 `sleep11_input` (장소 school, 인물 ["daram"])
    - [0] 잠자리를 정리한다 — 물건 blankets@school → jump r13_v111_sleep11_done
    - [80] 판돌 씨 집에 들렀다 온다 — 물건 blankets@school · 조건 값 hidden_pandol:family_seen == true; 값 meeting:hypothesis == "win"; 값 hidden_pandol:heat_replaced == null → call r13_hp_visit11; jump r13_v111_sleep11_input
    - [81] 남은 장작 몫을 확인한다 — 물건 blankets@school · 조건 값 hidden_pandol:family_seen == true; 값 meeting:hypothesis == "win"; 값 hidden_pandol:wood_reserved == null → call r13_hp_wood11; jump r13_v111_sleep11_input
- 대기 관문 `hp_house11` (장소 hidden_pandol, 인물 ["npc_pandol"])
    - [0] 학교로 돌아가겠습니다. — 사람 npc_pandol@hidden_pandol → call r13_scene
    - [1] 난로와 재통을 살핀다 — 물건 hp_stove@hidden_pandol · 조건 값 hidden_pandol:stove_seen == null → 대사 hp_look11
    - [2] 장작으로 바꿔도 되겠습니까? — 사람 npc_pandol@hidden_pandol · 조건 값 hidden_pandol:stove_seen == true; 값 hidden_pandol:wood_reserved == true; 값 hidden_pandol:consent == null → 대사 hp_consent11
    - [3] 장작 상자에 가져온 몫을 놓는다 — 물건 hp_wood@hidden_pandol · 조건 값 hidden_pandol:consent == true; 값 hidden_pandol:wood_delivered == null → 대사 hp_place11
    - [4] 집게로 돌을 꺼내 장작을 땐다 — 물건 hp_stove@hidden_pandol · 조건 값 hidden_pandol:consent == true; 값 hidden_pandol:wood_delivered == true; 값 hidden_pandol:tongs == true; 값 hidden_pandol:heat_replaced == null → 대사 hp_replace11
    - [5] 벽의 집게를 빌린다 — 물건 hp_tongs@hidden_pandol · 조건 값 hidden_pandol:stove_seen == true; 값 hidden_pandol:tongs == null → 대사 hp_tongs11
- 대기 관문 `night_rescue_prepare11` (장소 school, 인물 ["mom", "daram", "resident_teacher", "karo", "resident_nero"])
    - [0] 낮에 챙긴 운반 준비를 확인한다 — 물건 blankets@school → jump r13_v111_night_rescue_choices11
    - [1] 오늘은 출발을 미룬다 — 물건 blankets@school → jump r13_v111_late_road11
- 대기 관문 `late_supply_handoff11` (장소 school, 인물 ["mom", "daram", "resident_teacher", "karo"])
    - [0] 온기 상자 인수를 확인한다 — 물건 blankets@school → jump r13_v111_late_supply_done11
- 대기 관문 `snow_door11` (장소 forest, 인물 ["karo", "resident_nero"])
    - [0] 눈에 막힌 문을 연다 — 물건 v111_lower_door@forest → jump r13_v111_night_rescue_done11

## 12일

### MS14_D12_S01 장면 12-1. 불러야 할 이름

- 원본 시간·장소: 학교 배식실/진료 공간/시설 인수 지점 · 생각(목표 문구): 몸을 녹일 자리와 물자는 같은 곳에 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("lower_road_handover")==3 or r13_v111_value("lower_road_lost") is True`
- label: `r13_v111_day12`, `r13_v111_loss_route12`, `r13_v111_loss_names12`, `r13_v111_morning_notice12`, `r13_v111_morning_prep12_entry`, `r13_v111_morning_prep12`, `r13_v111_medicine12`, `r13_v111_warm_place12`, `r13_v111_carrier12`, `r13_v111_carrier_receipt12`, `r13_v111_carrier_received12`, `r13_v111_madam_invite12`, `r13_v111_living_names12`
- 장소: school, forest, square · 원본 등장: 까로, 나비, 네로, 다람, 돌목, 서리, 선생님, 아빠 · 무대 세우기: ["mom", "daram", "karo", "guard", "resident_teacher", "resident_nero"] ["karo"] ["daram", "karo"] ["mom", "daram", "guard", "resident_teacher"] ["resident_seori"] ["mom", "daram", "resident_teacher"]
- 대사: 원문 ID 23개, 묶음 elder_name12, daram_fever12, fever_seat12, 펼친 줄 68, rpy 직접 줄 1
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp; forest=room13-pixel-wide-forest-afternoon.webp, room13-pixel-wide-forest-evening.webp, room13-pixel-wide-forest-morning.webp; square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp
- 자료: NW_TRANSFER_LIST 학교 문 옆 이송 예정 칸(observed), E14_SUPPLY 학교 장작 인수 기록(observed)
- 상태 값 쓰기: `daram_fever12`, `medicine_locked`, `warm_seat_taken12`, `warm_seat_ready`, `carrier_arrived`, `busy:karo`, `warm_support_arrived`, `school_supply_handed`, `madam_observer_consent`
- 대기 관문 `morning_prep12` (장소 school, 인물 ["mom", "daram", "guard", "resident_teacher"])
    - [0] 약장 관리를 확인합니다. — 사람 resident_seori@clinic → jump r13_v111_medicine12
    - [1] 불 땔 자리를 부탁드립니다. — 사람 resident_teacher@school · 조건 값 warm_seat_taken12 == null → jump r13_v111_warm_place12
    - [2] 까로 씨, 학교까지 운반 좀 부탁합니다. — 사람 karo@square → jump r13_v111_carrier12
    - [3] 배식 준비를 살핀다 — 물건 desks@school → jump r13_v111_meal12
    - [4] 학교 물자를 함께 확인하시겠습니까? — 사람 resident_madam@store → jump r13_v111_madam_invite12
- 대기 관문 `carrier_receipt12` (장소 school, 인물 ["karo", "mom", "daram", "resident_teacher"])
    - [0] 선생님, 장작은 다 받으셨습니까? — 사람 resident_teacher@school → jump r13_v111_carrier_received12

### MS14_D12_S02 장면 12-2. 배식 전의 손

- 원본 시간·장소: 학교 배식실/진료 공간/시설 인수 지점 · 생각(목표 문구): 배식 준비와 아이들 자리는 안전하게 확인됐을까?
- label: `r13_v111_meal12`, `r13_v111_meal_choice12`, `r13_v111_stay_meal12`, `r13_v111_meal_inspect12`, `r13_v111_take_daram12`, `r13_v111_pickup12`, `r13_v111_pickup_box12`, `r13_v111_pickup_done12`, `r13_v111_leave_daram12`, `r13_v111_prevent_check12`, `r13_v111_prevent_ready12`, `r13_v111_medicine_missing12`, `r13_v111_seat_missing12`, `r13_v111_carrier_missing12`
- 장소: school, facility · 원본 등장: 나비, 다람, 도담, 보리, 새미, 선생님, 아빠 · 무대 세우기: ["daram", "nabi", "resident_teacher", "resident_bori", "kid_dodam", "kid_saemi"] ["mom"] ["mom", "daram"]
- 대사: 원문 ID 35개, 묶음 meal12_return, bowls_carried12, sp_smallpot12, sp_bowls12, sp_bottle12, sp_separate12, 펼친 줄 66, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp; facility=room13-pixel-ready-facility0177-afternoon.webp, room13-pixel-ready-facility0177-evening.webp, room13-pixel-ready-facility0177-morning.webp · 컷 ev:PROP_D12_large_small_ladles, ev:PROP_D12_teacher_large_red_bowl
- 자료: NW_WHITE_BOWLS 흰 그릇을 받은 아이들({'expr': "'daram' if r13_v111_value('meeting:room13') == 'lose' else 'observed'"})
- 상태 값 쓰기: `location:mom`, `route12`, `dodam_spoon12`, `bowls_carried12`, `bottle_original_seal_seen`, `meal12_intro_seen`, `soup_smallpot_seen12`, `soup_bowls_seen12`, `soup_bottle_seen12`, `soup_serving_separated12`, `DARAM_location`, `heat_box_received`, `busy:nabi`
- 갈림길 운명: ["fate_soup", "lost"] (`r13_v111_take_daram12`)
- 갈림길 운명: ["fate_soup", "lost"] (`r13_v111_leave_daram12`)
- 메뉴(`r13_v111_meal12`, display_menu): 흰 그릇을 작은 배식대로 나른다
- 메뉴(`r13_v111_meal_choice12`, menu): 배식 전에 더 살핀다 / 다람과 장작을 받으러 간다 / 다람은 나비 곁에 두고 다녀온다 / 아침에 부탁한 일들을 확인한다
- 대기 관문 `meal_inspect12` (장소 school, 인물 ["daram", "nabi", "resident_teacher", "resident_bori", "kid_dodam", "kid_saemi"])
    - [0] 작은 냄비와 국자 자리를 살핀다 — 물건 desks@school · 조건 값 soup_smallpot_seen12 == null → 대사 sp_smallpot12; set soup_smallpot_seen12=True
    - [1] 흰 그릇이 놓인 자리를 살핀다 — 물건 v111_bowl_table@school · 조건 값 soup_bowls_seen12 == null → 대사 sp_bowls12; set soup_bowls_seen12=True
    - [2] 선반에 놓인 병의 봉인을 살핀다 — 물건 desks@school · 조건 값 soup_bottle_seen12 == null → 대사 sp_bottle12; set soup_bottle_seen12=True
    - [3] 흰 그릇을 옆으로 옮기고 작은 냄비를 연다 — 물건 v111_bowl_table@school · 조건 값 soup_smallpot_seen12 == true; 값 soup_bowls_seen12 == true; 값 soup_bottle_seen12 == true → 대사 sp_separate12; set soup_serving_separated12=True; set route12='premeal_stopped'; jump r13_v111_premeal12
    - [4] 장작을 받을 일을 다시 살핀다 — 물건 desks@school → jump r13_v111_meal_choice12
- 대기 관문 `pickup_box12` (장소 facility, 인물 ["mom"])
    - [0] 준비된 장작 묶음을 인수한다 — 물건 blankets@facility → jump r13_v111_pickup_done12

### MS14_D12_S03 장면 12-3. 돌아온 냄비

- 원본 시간·장소: 학교 배식실/진료 공간/시설 인수 지점 · 생각(목표 문구): 남은 수프에서 무엇이 발견됐을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("route12")=="late_exposure"`
- label: `r13_v111_late_meal12`, `r13_v111_soup_fragment12`, `r13_v111_fragment_seen12`
- 장소: school · 원본 등장: 나비, 보리, 새미, 선생님, 아빠 · 무대 세우기: ["daram", "nabi", "resident_bori", "resident_teacher", "kid_saemi"]
- 대사: 원문 ID 15개, 묶음 kkomi_soup12, 펼친 줄 20, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp · 컷 ev:PROP_D12_white_bowl_crosswise_spoon
- 상태 값 쓰기: `busy:nabi`, `KKOMI_ALIVE`, `kkomi_soup_dead`, `medical_called`, `busy:resident_bori`, `soup_fragment_observed`
- 대기 관문 `soup_fragment12` (장소 school, 인물 ["nabi", "resident_teacher"])
    - [0] 작은 냄비의 남은 수프를 보존한다 — 물건 stove@school → jump r13_v111_fragment_seen12

### MS14_D12_S04 장면 12-4. 같은 것을 먹었다는 말

- 원본 시간·장소: 학교 배식실/진료 공간/시설 인수 지점 · 생각(목표 문구): 온전했던 봉인과 확인한 동선은 어떻게 이어질까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("route12") in ("late_exposure","premeal_stopped") and r13_v111_value("soup_fragment_observed") is True`
- label: `r13_v111_soup_hearing12`, `r13_v111_meal_observations12`, `r13_v111_bottle_match12`, `r13_v111_bottle_matched12`, `r13_v111_seal_proof12`, `r13_v111_seal_answer12`, `r13_v111_seal_late12`, `r13_v111_handling12`, `r13_v111_handling_route12`, `r13_v111_handling_late12`, `r13_v111_medical_arrival12`, `r13_v111_soup_final12`, `r13_v111_soup_conclusion12`, `r13_v111_soup_conclusion_route12`, `r13_v111_conclusion_late12`, `r13_v111_confessed12`, `r13_v111_list_proof12`, `r13_v111_list_won12`, `r13_v111_soup_after_route12`, `r13_v111_aftermath_pre12`, `r13_v111_teacher_guard_pre12`, `r13_v111_soup_pre_close12`, `r13_v111_pre_lights12`, `r13_v111_pre_no_lights12`, `r13_v111_teacher_neoul_pre12`, `r13_v111_list_wrong12`, `r13_v111_conclusion_pre12`, `r13_v111_fragment_wrong12`, `r13_v111_soup_lost12`, `r13_v111_soup_hint_final12`, `r13_v111_handling_pre12`, `r13_v111_seal_pre12`, `r13_v111_medicine_wrong12`, `r13_v111_soup_hint12`, `r13_v111_bowl_compare12`
- 장소: school · 원본 등장: 나비, 너울, 돌목, 백 부인, 새미, 서리, 선생님, 아빠 · 무대 세우기: ["daram", "nabi", "resident_teacher", "resident_madam"] ["daram", "nabi", "resident_teacher", "resident_seori", "resident_bori", "guard", "neoul"] ["mom", "daram", "nabi", "resident_teacher", "guard", "neoul"]
- 대사: 원문 ID 98개, 묶음 bowls_recall12, seori_ask12, seori_ledger12, seori_confess12, soup_list_q12, soup_list_won12, soup_list_lost12, soup_lost12, bowl_compare12, 펼친 줄 161, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 자료: E12_FRAGMENT 냄비 파편과 병 입구(observed), E12_SEAL 준비 때 온전했던 개봉 봉인(observed), E12_HANDLING 작은 냄비의 인계·관찰 구간(observed), NW_RETURNED_BOWL 돌아온 흰 그릇(observed)
- 상태 값 쓰기: `busy:resident_bori`, `medical_arrived`, `teacher_confessed`, `transfer_list_secured`, `grand:soup`, `transfer_list_voided`, `book_promise12`, `teacher_custody`, `teacher_transfer`, `soup_lose_kind`, `seori_disciplined`
- 회의 결과: `soup` → win (`r13_v111_list_won12`)
- 회의 결과: `soup` → partial (`r13_v111_list_wrong12`)
- 회의 결과: `soup` → lose (`r13_v111_fragment_wrong12`)
- 회의 결과: `soup` → lose (`r13_v111_medicine_wrong12`)
- 이송 명단에 적음: nabi (soup_lose, `r13_v111_fragment_wrong12`)
- 메뉴(`r13_v111_medical_arrival12`, menu): 약장 밖에 맡긴 약도 있는지 묻는다 / 장부를 다시 보여 달라고 한다
- 메뉴(`r13_v111_aftermath_pre12`, menu): 돌목에게 감독을 맡긴다 / 너울에게 신병을 넘긴다
- 대기 관문 `bottle_match12` (장소 school, 인물 ["nabi", "resident_teacher"])
    - [0] 병과 파편의 경계를 대조한다 — 물건 desks@school → jump r13_v111_bottle_matched12
    - [1] 주머니의 그릇을 배식대 옆에 놓아 본다 — 물건 v111_bowl_table@school · 조건 값 grand_bowl_pocket == true; 자료 NW_RETURNED_BOWL == false; 값 bowls_carried12 == true → call r13_v111_bowl_compare12
- 회의/대조 「그 병은 정말 약을 다 쓴 빈 병이었는가」 (키 `재사용 설명과 개봉 봉인을 대조한다`, 회의 soup, 기회 5, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E12_FRAGMENT", "E12_SEAL"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 선생님은 약을 ‘다 쓴 병’에 물을 담았다고 한다. ……그 부분이 내가 본 것과 맞나?
    - 이김 → `r13_v111_seal_answer12` {"jumps": [["r13_v111_seal_late12", "if r13_v111_value('route12')=='late_exposure'"], ["r13_v111_seal_pre12", null]]}
    - 틀림 → `r13_v111_medicine_wrong12` {"meeting_end": [{"meeting": "soup", "result": "lose", "when": null}], "sets": [["soup_lose_kind", "stolen", null], ["seori_disciplined", true, null]], "jumps": [["r13_v111_seal_proof12", "if r13_nw_retry(\"soup\",['E12_FRAGMENT', 'E12_SEAL'],'half_soup_seal12')"], ["r13_v111_soup_lost12", null]], "retry": ["r13_nw_retry(\"soup\",['E12_FRAGMENT', 'E12_SEAL'],'half_soup_seal12')"]}
    - 되묻기 → `r13_v111_soup_hint12` {"jumps": [["r13_v111_seal_proof12", null]]}
- 회의/대조 「선생님은 정말 씻는 데서 물을 받았는가」 (키 `파편·봉인·취급 구간을 함께 제시한다`, 회의 soup, 기회 5, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E12_FRAGMENT", "E12_SEAL", "E12_HANDLING"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 선생님은 병을 비우고 ‘씻는 데서’ 물을 받았다고 한다. ……그 부분이 내가 들은 것과 맞나?
    - 이김 → `r13_v111_soup_conclusion12` {}
    - 틀림 → `r13_v111_fragment_wrong12` {"meeting_end": [{"meeting": "soup", "result": "lose", "when": null}], "listed": [{"person": "nabi", "reason": "soup_lose", "when": null}], "sets": [["soup_lose_kind", "nabi", null]], "jumps": [["r13_v111_soup_final12", "if r13_nw_retry(\"soup\",['E12_FRAGMENT', 'E12_SEAL', 'E12_HANDLING'],'half_soup_final12')"], ["r13_v111_soup_lost12", null]], "retry": ["r13_nw_retry(\"soup\",['E12_FRAGMENT', 'E12_SEAL', 'E12_HANDLING'],'half_soup_final12')"]}
    - 되묻기 → `r13_v111_soup_hint_final12` {"jumps": [["r13_v111_soup_final12", null]]}
- 회의/대조 「작은 냄비는 정말 아이들 모두를 위한 것이었는가」 (키 `명단과 흰 그릇을 대조한다`, 회의 soup, 기회 5, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["NW_TRANSFER_LIST", "NW_WHITE_BOWLS"] · 대체 [["NW_WHITE_BOWLS", "NW_RETURNED_BOWL"]] · 덧붙임 허용 ["NW_RETURNED_BOWL", "NW_SICK_BEDS"]
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 선생님은 작은 냄비가 아이들 ‘모두’를 위한 것이었다고 한다. ……그 ‘모두’가 내가 본 것과 맞나?
    - 이김 → `r13_v111_list_won12` {"meeting_end": [{"meeting": "soup", "result": "win", "when": null}], "sets": [["transfer_list_secured", true, null], ["grand:soup", true, "if r13_v111_value(\"meeting:soup\")==\"win\" and r13_nw_grand([\"명단과 흰 그릇을 대조한다\"],\"NW_RETURNED_BOWL\")"], ["transfer_list_voided", true, "if r13_v111_value(\"meeting:soup\")==\"win\" and r13_nw_grand([\"명단과 흰 그릇을 대조한다\"],\"NW_RETURNED_BOWL\")"]], "jumps": [["r13_v111_soup_after_route12", null]]}
    - 틀림 → `r13_v111_list_wrong12` {"meeting_end": [{"meeting": "soup", "result": "partial", "when": null}], "jumps": [["r13_v111_list_proof12", "if r13_nw_retry(\"soup\",[\"NW_TRANSFER_LIST\",\"NW_WHITE_BOWLS\"],\"half_soup_list12\")"], ["r13_v111_soup_after_route12", null]], "retry": ["r13_nw_retry(\"soup\",[\"NW_TRANSFER_LIST\",\"NW_WHITE_BOWLS\"],\"half_soup_list12\")"]}

### MS14_D12_S05 장면 12-5. 너무 밝은 창문

- 원본 시간·장소: 학교 배식실/진료 공간/시설 인수 지점 · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("route12")=="late_exposure" and r13_v111_value("teacher_confessed") is True and r13_v111_value("medical_arrived") is True`
- label: `r13_v111_aftermath_late12`, `r13_v111_lights12`, `r13_v111_no_lights12`, `r13_v111_child_light12`, `r13_v111_child_dark12`, `r13_v111_teacher_guard_late12`, `r13_v111_sleep12`, `r13_v111_sleep12_bed`, `r13_v111_sleep12_bed_input`, `r13_v111_sleep12_bed_done`, `r13_v111_teacher_neoul_late12`
- 장소: school · 원본 등장: 나비, 너울, 다람, 돌목, 보리, 새미, 선생님, 아빠, 엄마 · 무대 세우기: ["daram", "nabi", "resident_teacher", "resident_seori", "resident_bori", "guard", "neoul"] ["daram", "mom", "nabi", "resident_teacher", "resident_seori", "resident_bori", "guard", "neoul"]
- 대사: 원문 ID 31개, 묶음 portrait12, 펼친 줄 38, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 자료: NW_HALL_WINDOW 회관 창 안의 촌장과 바둑이(observed), NW_PIKO_PAINTING 초상 밑의 그림(observed)
- 상태 값 쓰기: `alive:kid_dodam`, `alive:kid_saemi`, `teacher_custody`, `teacher_transfer`, `day`
- 메뉴(`r13_v111_aftermath_late12`, menu): 돌목에게 감독을 맡긴다 / 너울에게 신병을 넘긴다
- 대기 관문 `sleep12_bed_input` (장소 school, 인물 ["daram"])
    - [0] 잠자리를 정리한다 — 물건 blankets@school → jump r13_v111_sleep12_bed_done

### MS14_D12_A 대체 장면 12-A. 배식 직전 발견

- 원본 시간·장소: 학교 배식실/진료 공간/시설 인수 지점 · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("route12")=="premeal_stopped"`
- label: `r13_v111_premeal12`
- 장소: school · 원본 등장: 나비, 다람, 새미, 선생님, 아빠 · 무대 세우기: ["daram", "nabi", "resident_teacher", "resident_bori", "kid_dodam", "kid_saemi"]
- 대사: 원문 ID 7개, 묶음 없음, 펼친 줄 10, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 상태 값 쓰기: `route12`, `medical_called`, `busy:resident_bori`, `soup_fragment_observed`
- 갈림길 운명: ["fate_soup", "premeal"] (`r13_v111_premeal12`)

### MS14_D12_B 대체 장면 12-B. 수프 사건이 일어나지 않은 저녁

- 원본 시간·장소: 학교 배식실/진료 공간/시설 인수 지점 · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("route12")=="early_prevented"`
- label: `r13_v111_early12`, `r13_v111_early_bowl12`, `r13_v111_early_bowl12_wait`, `r13_v111_early_guard_bowl12`
- 장소: school · 원본 등장: 다람, 선생님, 아빠, 아이, 엄마 · 무대 세우기: ["daram", "mom", "nabi", "resident_teacher", "karo", "kid_dodam", "kid_saemi"] ["guard"]
- 대사: 원문 ID 10개, 묶음 early_ordinary12, early_door12, early_guard_bowl12, 펼친 줄 24, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 상태 값 쓰기: `route12`, `school_heat_connected`, `busy:karo`, `transfer_list_voided`, `grand:soup`
- 갈림길 운명: ["fate_soup", "early"] (`r13_v111_early12`)
- 대기 관문 `early_bowl12` (장소 school, 인물 ["daram", "mom", "nabi", "resident_teacher", "karo", "kid_dodam", "kid_saemi", "guard"])
    - [0] 저녁 배식을 돕는다 — 물건 stove@school → (이 label 에서 따로 처리 없음)
    - [1] 주머니의 그릇을 배식대 옆에 놓아 본다 — 물건 v111_bowl_table@school · 조건 값 grand_bowl_pocket == true; 자료 NW_RETURNED_BOWL == false → call r13_v111_bowl_compare12; jump r13_v111_early_bowl12_wait
    - [2] 이 그릇 바닥의 표시는 무엇입니까? — 사람 guard@school · 조건 자료 NW_RETURNED_BOWL == true; 값 grand:soup == null → call r13_v111_early_guard_bowl12; jump r13_v111_early_bowl12_wait

## 13일

### MS14_D13_S01 장면 13-1. 판돌의 어깨

- 원본 시간·장소: 학교/입구 경비실/광장 수레 · 생각(목표 문구): 판돌에게 둘러 줄 담요의 터진 곳은 어디일까?
- label: `r13_v111_day13`, `r13_v111_blanket_mend13`, `r13_hp_handoff13`, `r13_v111_blanket_mended13`, `r13_v111_teacher_relief13`, `r13_v111_teacher_relief_check13`, `r13_v111_teacher_relief_done13`
- 장소: school · 원본 등장: 까로, 다람, 아빠, 엄마, 판돌 · 무대 세우기: ["mom", "daram", "npc_pandol", "karo"] ["npc_pandol"] ["nabi"] ["mom", "daram", "guard", "resident_teacher", "v111_patrol"]
- 대사: 원문 ID 18개, 묶음 kkomi_gone13, fever13, book_promise13, hp_handoff_open13, hp_handoff_missing13, hp_handoff13, relief_done13, 펼친 줄 54, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp · 컷 v111_blanket_before, v111_blanket_after
- 자료: E13_MENDING 오늘 아침 회색 담요 수선(observed)
- 상태 값 쓰기: `busy:karo`, `pandol_blanket_mended`, `busy:v111_patrol`, `teacher_supervisor`, `busy:guard`
- 이송 명단에 적음: resident_piko (street, `r13_v111_day13`)
- 대기 관문 `blanket_mend13` (장소 school, 인물 ["mom", "daram", "npc_pandol", "karo"])
    - [0] 회색 담요를 실제로 수선한다 — 물건 blankets@school → jump r13_v111_blanket_mended13
    - [80] 누나의 돌봄 인계를 확인한다 — 물건 desks@school · 조건 값 hidden_pandol:heat_replaced == true; 값 hidden_pandol:care_handed == null → call r13_hp_handoff13; jump r13_v111_blanket_mend13
- 대기 관문 `teacher_relief_check13` (장소 school, 인물 ["mom", "daram", "guard", "resident_teacher", "v111_patrol"])
    - [0] 초소로 가시기 전에, 선생님 곁은 누가 맡습니까? — 사람 guard@school → jump r13_v111_teacher_relief_done13

### MS14_D13_S02 장면 13-2. 벤치 한 칸

- 원본 시간·장소: 학교/입구 경비실/광장 수레 · 생각(목표 문구): 가족의 자리와 다른 사람의 이송을 함께 약속할 수 있을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("family_reunited") is True and r13_v111_value("DARAM_DETAINED") is not True`
- label: `r13_v111_gate_bench13`, `r13_v111_offer13`, `r13_v111_offer_question13`, `r13_v111_offer_accept13`, `r13_v111_offer_refuse13`
- 장소: gate, square · 원본 등장: 너울, 다람, 돌목, 실룩, 아빠, 엄마, 촌장 · 무대 세우기: ["mom", "daram", "guard"] ["mom", "daram", "npc_pandol", "resident_ppul", "neoul", "karo", "guard"]
- 대사: 원문 ID 31개, 묶음 없음, 펼친 줄 64, rpy 직접 줄 0
- 그림: 배경 gate=room13-pixel-ready-gate0173-afternoon.webp, room13-pixel-ready-gate0173-evening.webp, room13-pixel-ready-gate0173-morning.webp; square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp
- 상태 값 쓰기: `family_offer_terms_seen`, `family_deal`, `listed:daram`, `daram_deal_freed`
- 메뉴(`r13_v111_offer13`, menu): 조건을 더 묻는다 / 가족 셋이 수락하고 물러난다 / 거절하고 현장에 남는다

### MS14_D13_S03 장면 13-3. 아내가 불렀다는 말

- 원본 시간·장소: 학교/입구 경비실/광장 수레 · 생각(목표 문구): 촌장이 전한 시점과 우리가 직접 한 일은 맞을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("family_deal") is False and r13_v111_owned("E13_MENDING")`
- label: `r13_v111_blanket_lie13`, `r13_v111_mending_proof13`, `r13_v111_mending_answer13`, `r13_v111_badook_proof13`, `r13_v111_badook_won13`, `r13_v111_mending_rest13`, `r13_v111_cart_inspect13`, `r13_v111_cart_observed13`, `r13_v111_silluk_board_observation13`, `r13_v111_teacher_board_observation13`, `r13_v111_badook_wrong13`, `r13_v111_mending_wrong13`, `r13_v111_departed_night13`, `r13_v111_departed_bed13`, `r13_v111_mending_hint13`
- 장소: square, school · 원본 등장: 너울, 다람, 아빠, 촌장, 판돌 · 무대 세우기: ["mom", "daram", "npc_pandol", "resident_ppul", "guard", "karo", "resident_badook"] ["mom", "nabi"]
- 대사: 원문 ID 36개, 묶음 badook_q13, badook_won13, cart_names13, badook_retry13, badook_lost13, blanket_lost13, 펼친 줄 84, rpy 직접 줄 2
- 그림: 배경 square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp; school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 자료: NW_PIKO_PAINTING 초상 밑의 그림(told)
- 상태 값 쓰기: `false_message_admitted`, `cart_roster`, `location:resident_siluk`, `silluk_transfer`, `location:resident_teacher`, `teacher_transfer`, `cart_departed`, `outcome13`
- 회의 결과: `blanket` → win (`r13_v111_badook_won13`)
- 회의 결과: `blanket` → partial (`r13_v111_badook_wrong13`)
- 회의 결과: `blanket` → lose (`r13_v111_mending_wrong13`)
- 대기 관문 `cart_inspect13` (장소 square, 인물 ["mom", "daram", "karo", "guard"])
    - [0] 실제 탑승자와 하차 준비를 확인한다 — 물건 cart@square → jump r13_v111_cart_observed13
- 대기 관문 `departed_bed13` (장소 school, 인물 ["mom", "nabi"])
    - [0] 오늘 밤 자리를 확인한다 — 물건 blankets@school → jump r13_v111_morning14
- 회의/대조 「아내가 봤다는 담요의 시점을 확인한다」 (키 `아내가 봤다는 담요의 시점을 확인한다`, 회의 blanket, 기회 4, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E13_MENDING"] · 대체 없음 · 덧붙임 허용 ["E35"]
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 촌장은 ‘어젯밤’ 모과 씨가 이 담요의 새를 보고 웃었다고 한다. ……그 부분이 내가 아는 것과 맞나?
    - 이김 → `r13_v111_mending_answer13` {"jumps": [["r13_v111_badook_proof13", null]]}
    - 틀림 → `r13_v111_mending_wrong13` {"meeting_end": [{"meeting": "blanket", "result": "lose", "when": null}], "sets": [["cart_departed", true, null], ["outcome13", "partial_rescue", null]], "jumps": [["r13_v111_mending_proof13", "if r13_nw_retry(\"blanket\")"], ["r13_v111_departed_night13", null]], "retry": ["r13_nw_retry(\"blanket\")"]}
    - 되묻기 → `r13_v111_mending_hint13` {"jumps": [["r13_v111_mending_proof13", null]]}
- 회의/대조 「촌장이 어젯밤 있던 곳을 확인한다」 (키 `촌장이 어젯밤 있던 곳을 확인한다`, 회의 blanket, 기회 4, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["NW_HALL_WINDOW"] · 대체 없음 · 덧붙임 허용 ["E29"]
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 촌장은 학교 종이 울릴 무렵 모과 씨를 보러 나가 있었다고 한다. ……그 시각, 내가 본 것과 맞나?
    - 이김 → `r13_v111_badook_won13` {"meeting_end": [{"meeting": "blanket", "result": "win", "when": null}], "jumps": [["r13_v111_mending_rest13", null]]}
    - 틀림 → `r13_v111_badook_wrong13` {"meeting_end": [{"meeting": "blanket", "result": "partial", "when": null}], "jumps": [["r13_v111_badook_proof13", "if r13_nw_retry(\"blanket\")"], ["r13_v111_mending_rest13", null]], "retry": ["r13_nw_retry(\"blanket\")"]}

### MS14_D13_S04 장면 13-4. 바퀴가 멎어도

- 원본 시간·장소: 학교/입구 경비실/광장 수레 · 생각(목표 문구): 수레가 멎은 뒤 실제로 인수된 사람은 누구일까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("false_message_admitted") is True`
- label: `r13_v111_stop_cart13`, `r13_v111_listed_void13`, `r13_v111_rein13`, `r13_v111_rein_ledger13p`, `r13_v111_rein_ledger13`, `r13_v111_rein_painting13p`, `r13_v111_rein_won13`, `r13_v111_after_rein13`, `r13_v111_partial_listed13`, `r13_v111_family_position13`, `r13_v111_family_stay13`, `r13_v111_handover_plan13`, `r13_v111_school_handover_prep13`, `r13_v111_nabi_beds13`, `r13_v111_beds_ready13`, `r13_v111_pandol_down13`, `r13_v111_momo_transport13`, `r13_v111_momo_down13`, `r13_v111_momo_school13`, `r13_v111_guldol_transport13`, `r13_v111_guldol_down13`, `r13_v111_guldol_school13`, `r13_v111_last_cart13`, `r13_v111_teacher_transport13`, `r13_v111_teacher_down13`, `r13_v111_teacher_supervised13`, `r13_v111_teacher_receipt13`, `r13_v111_teacher_received13`, `r13_v111_silluk_transport13`, `r13_v111_silluk_supervision13`, `r13_v111_silluk_down13`, `r13_v111_silluk_family13`, `r13_v111_silluk_receipt13`, `r13_v111_silluk_received13`, `r13_v111_family_still_here13`, `r13_v111_family_already_school13`, `r13_v111_transport_cleanup13`, `r13_v111_escort_refuse13`, `r13_v111_order_stop13`, `r13_v111_relay_stop13`, `r13_v111_relay_supervised13`, `r13_v111_relay_present13`, `r13_v111_relay_confirmed13`, `r13_v111_driver_refuse13`, `r13_v111_cart_return13`, `r13_v111_night_finish13`, `r13_v111_buri_tools13`, `r13_v111_crowd_prepare13`, `r13_v111_crowd_prepare_wait13`, `r13_v111_family_karo13`, `r13_v111_family_walk_karo13`, `r13_v111_family_nero13`, `r13_v111_rein_wrong13b`, `r13_v111_rein_wrong13`, `r13_v111_rein_wrong13a`
- 장소: square, school, v111_supervised, v111_labor · 원본 등장: 굴돌, 까로, 나비, 너울, 네로, 다람, 돌목, 모모, 바둑이, 선생님, 실룩, 아빠, 엄마, 은호, 촌장, 판돌 · 무대 세우기: ["mom", "daram", "karo", "guard", "resident_badook", "npc_pandol", "resident_momo", "resident_guldol", "resident_ppul", "neoul"] ["mom", "daram", "karo", "guard", "resident_badook", "npc_pandol", "resident_momo", "resident_guldol", "resident_ppul", "neoul", "resident_siluk"] ["guard", "karo", "nabi"] ["nabi", "karo"] ["guard", "karo", "resident_badook"] ["guard", "karo", "resident_badook", "npc_pandol"]
- 대사: 원문 ID 59개, 묶음 listed_down_daram13, listed_void13, rein_open13, rein_ledger13, rein_won13, handover_wait13, nabi_down13, beds_ready13, momo_walk13, back_square13, guldol_walk13, listed_down13, order_relay_next13, relay_confirmed13, karo_cart_next13, buri_tools13, crowd_space_records13, crowd_space_cart13, crowd_place_guard13, karo_report13, rein_retry13, rein_lost13, 펼친 줄 143, rpy 직접 줄 2 · 계산 줄 ["r13_nw_roster_lines()"]
- 그림: 배경 square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp; school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp; v111_supervised=room13-pixel-panorama-holding-morning.webp; v111_labor=room13-pixel-panorama-woodshed-intact.webp
- 자료: NW_NEOUL_LEDGER 너울의 장부({'expr': "'full' if r13_v111_value('meeting:hypothesis') == 'win' else 'some' if r13_v111_value('meeting:hypothesis') == 'partial' else 'observed'"}), E13_HANDOVER 판돌의 학교 인수 기록(observed), E13_ORDER 중지된 이송 명령 사본(observed)
- 상태 값 쓰기: `cart_stopped`, `stop_actor`, `handed:daram`, `busy:resident_badook`, `cart_roster`, `roster_shown13`, `neoul_held`, `family_location`, `location:daram`, `busy:mom`, `handed:nabi`, `handover_prepared13`, `busy:karo`, `handed:npc_pandol`, `handed:resident_momo`, `handed:resident_guldol`, `all_cart_handed`, `outcome13`, `handed:resident_teacher`, `teacher_transfer`, `busy:neoul`, `handed:resident_siluk`, `silluk_transfer`, `busy:guard`, `actual_stop_actor_refuses_transport`, `current_order_execution_stopped`, `relay_stopped`, `Kkaro_forced_transport_refused`, `cart_returned`, `escort_gear_returned`, `current_transport_chain_stopped`, `buri_device_consent`, `crowd_preparation_schema13`, `crowd_records_spaced13`, `crowd_cart_spaced13`, `location:guard`, `crowd_supervisor_placed13`, `location:mom`, `location:karo`, `location:resident_nero` …(41개)
- 회의 결과: `piko` → win (`r13_v111_rein_won13`)
- 회의 결과: `piko` → lose (`r13_v111_rein_wrong13`)
- 메뉴(`r13_v111_family_position13`, menu): 엄마와 다람이 곁에 남게 한다 / 엄마와 다람을 까로와 학교로 보낸다 / 엄마와 다람을 네로와 학교로 보낸다
- 메뉴(`r13_v111_handover_plan13`, menu): 학교 침상과 인수를 먼저 확인한다 / 하차한 사람부터 부축한다 / 보온·감독 아래 인계를 기다린다 / 검증한 기록을 공개한다
- 대기 관문 `nabi_beds13` (장소 school, 인물 ["nabi", "karo"])
    - [0] 침상과 인수를 부탁합니다. — 사람 nabi@school → jump r13_v111_beds_ready13
- 대기 관문 `momo_down13` (장소 square, 인물 ["karo", "guard", "resident_badook", "resident_momo"])
    - [0] 모모를 부축해 학교로 모신다 — 물건 cart@square → jump r13_v111_momo_school13
- 대기 관문 `guldol_down13` (장소 square, 인물 ["karo", "guard", "resident_badook", "resident_guldol"])
    - [0] 굴돌을 부축해 학교로 모신다 — 물건 cart@square → jump r13_v111_guldol_school13
- 대기 관문 `teacher_down13` (장소 square, 인물 ["karo", "guard", "resident_badook", "resident_teacher", "neoul"])
    - [0] 교사를 분리된 감독 자리로 옮긴다 — 물건 cart@square → jump r13_v111_teacher_supervised13
- 대기 관문 `teacher_receipt13` (장소 v111_supervised, 인물 ["karo", "resident_teacher", "neoul"])
    - [0] 선생님을 여기서 따로 맡으셨습니까? — 사람 neoul@v111_supervised → jump r13_v111_teacher_received13
- 대기 관문 `silluk_supervision13` (장소 square, 인물 ["karo", "guard", "resident_badook", "resident_siluk"])
    - [0] 하차 전 감독 교대를 확인합니다. — 사람 guard@square → jump r13_v111_silluk_down13
- 대기 관문 `silluk_receipt13` (장소 v111_labor, 인물 ["karo", "guard", "resident_siluk"])
    - [0] 실룩 씨를 여기서 맡으셨습니까? — 사람 guard@v111_labor → jump r13_v111_silluk_received13
- 대기 관문 `transport_cleanup13` (장소 square, 인물 ["karo", "guard", "resident_badook"]) — 동적: 돌목 위치·마친 확인(_done)에 따라 선택지를 빼고 장소별 인물표(people_by_location)를 다시 만든다.
    - [0] 내일 새 명단이 오면, 또 태울 겁니까? — 사람 resident_badook@square → jump r13_v111_escort_refuse13
    - [1] 명령 전체를 중지하고, 사본을 직접 전하겠습니다. — 사람 guard@square → jump r13_v111_order_stop13
    - [2] 강제 운반은 맡지 말고, 빈 수레를 돌려주자. — 사람 karo@square → jump r13_v111_driver_refuse13
    - [3] 빈 수레 반환을 요청한다. — 사람 karo@square → jump r13_v111_cart_return13
    - [4] 중지 명령 사본을 너울에게 보인다 — 사람 neoul · 자료 제시 V111:E13_ORDER (제시 버튼만)@square → jump r13_v111_relay_confirmed13
    - [5] 학교로 돌아간다 — 이동 school@school → jump r13_v111_night_finish13
    - [6] 내일 쓸 공구를 부탁합니다. — 사람 buri@workshop → jump r13_v111_buri_tools13
- 대기 관문 `crowd_prepare13` (장소 square, 인물 ["guard", "karo", "resident_badook", "neoul"]) — 동적: 돌목이 군중 감독에 못 오면(r13_crowd_guard_available13) 돌목과 그 선택지를 뺀다.
    - [0] 기록 읽을 자리를 수레에서 떼어 놓는다 — 물건 cart@square · 조건 값 crowd_records_spaced13 == null → 대사 crowd_space_records13; set crowd_records_spaced13=True
    - [1] 수레 옆 짐을 옮겨 통로를 나눈다 — 물건 cart@square · 조건 값 crowd_cart_spaced13 == null → 대사 crowd_space_cart13; set crowd_cart_spaced13=True
    - [2] 기록을 읽는 동안 너울 씨 곁을 맡아 주시겠습니까? — 사람 guard@square · 조건 값 crowd_records_spaced13 == true; 값 crowd_cart_spaced13 == true; 값 crowd_supervisor_placed13 == null → 대사 crowd_place_guard13; set busy:guard='crowd_supervision'; set location:guard='square'; set crowd_supervisor_placed13=True
    - [3] 검증한 기록을 소리 내어 읽는다 — 물건 cart@square → jump r13_v111_crowd13
    - [4] 공개를 미루고 인계부터 확인한다 — 물건 cart@square → jump r13_v111_handover_plan13
- 회의/대조 「실룩이 말한 ‘아무 등이나, 값은 다 같다’가 맞는가」 (키 `인수하지 않은 돌의 약속 값을 보인다`, 회의 piko, 기회 4, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["NW_LA_OFFER"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 실룩 씨는 아무 등이나 골랐고 돌값은 어느 등이든 같다고 한다. ……그 ‘같은 값’이 내가 본 것과 맞나?
    - 이김 → `r13_v111_rein_ledger13` {"jumps": [["r13_v111_rein_painting13p", null]]}
    - 틀림 → `r13_v111_rein_wrong13a` {"jumps": [["r13_v111_rein_ledger13p", "if r13_nw_retry(\"piko\")"], ["r13_v111_rein_wrong13", null]], "retry": ["r13_nw_retry(\"piko\")"]}
- 회의/대조 「실룩이 말한 ‘아무 등이나, 값은 다 같다’가 맞는가」 (키 `장부의 두 배를 실룩에게 보인다`, 회의 piko, 기회 4, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["E16"] · 대체 없음 · 덧붙임 허용 ["E34"]
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 실룩 씨는 아무 등이나 골랐고 돌값은 어느 등이든 같다고 한다. ……그 ‘같은 값’이 내가 본 것과 맞나?
    - 이김 → `r13_v111_rein_ledger13` {"jumps": [["r13_v111_rein_painting13p", null]]}
    - 틀림 → `r13_v111_rein_wrong13a` {"jumps": [["r13_v111_rein_ledger13p", "if r13_nw_retry(\"piko\")"], ["r13_v111_rein_wrong13", null]], "retry": ["r13_nw_retry(\"piko\")"]}
- 회의/대조 「피코가 막혀야 했던 까닭을 보인다」 (키 `피코가 막혀야 했던 까닭을 보인다`, 회의 piko, 기회 4, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["NW_PIKO_PAINTING"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 너울 씨는 ‘도둑의 말’이라고 덮는다. ……피코 씨가 품던 판자, 그 부분을 받쳐 줄 것이 없나?
    - 이김 → `r13_v111_rein_won13` {"meeting_end": [{"meeting": "piko", "result": "win", "when": null}], "sets": [["neoul_held", true, null]], "acquires": ["NW_NEOUL_LEDGER"], "jumps": [["r13_v111_after_rein13", null]]}
    - 틀림 → `r13_v111_rein_wrong13b` {"jumps": [["r13_v111_rein_painting13p", "if r13_nw_retry(\"piko\")"], ["r13_v111_rein_wrong13", null]], "retry": ["r13_nw_retry(\"piko\")"]}

### MS14_D13_A 대체 장면 13-A. 가족 셋의 하룻밤

- 원본 시간·장소: 학교/입구 경비실/광장 수레 · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("family_deal") is True`
- label: `r13_v111_family_exit13`, `r13_v111_sleep13`, `r13_v111_sleep13_gate`, `r13_v111_sleep13_gate_input`, `r13_v111_morning14`, `r13_v111_day14`, `r13_v111_ending_dispatch14`, `r13_v111_left_name_ending14`, `r13_v111_memorial14`, `r13_v111_story_end14`, `r13_v111_end_card14`, `r13_v111_frozen_ending14`, `r13_v111_collect_family13`, `r13_v111_sleep13_input`
- 장소: square, gate, school · 원본 등장: 다람, 아빠, 엄마, 촌장 · 무대 세우기: ["mom", "daram", "guard", "karo"] ["mom", "daram", "nabi"] ["mom", "daram", "guard"] ["mom", "daram"]
- 대사: 원문 ID 13개, 묶음 end_left_name14, end_memorial14, end_frozen14, 펼친 줄 47, rpy 직접 줄 0
- 그림: 배경 square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp; gate=room13-pixel-ready-gate0173-afternoon.webp, room13-pixel-ready-gate0173-evening.webp, room13-pixel-ready-gate0173-morning.webp; school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp · r13_scene [{"expr": "R13_PLACES['school'][1]"}, "남겨진 이름"], [{"expr": "R13_PLACES['gate'][1]"}, "얼어붙은 마을"]
- 상태 값 쓰기: `family_benefits_received`, `night14_lodging`, `outcome13`, `departed_unrescued`, `family_location`, `location:daram`, `busy:mom`, `day`, `ending14`, `story14_completed`
- 대기 관문 `sleep13_gate_input` (장소 gate, 인물 ["mom", "daram", "guard"])
    - [0] 오늘 밤 우리 가족 세 사람, 어디서 자면 됩니까? — 사람 guard@gate → jump r13_v111_morning14
- 대기 관문 `sleep13_input` (장소 school, 인물 ["mom", "daram", "nabi"])
    - [0] 오늘 밤 자리를 확인한다 — 물건 blankets@school → jump r13_v111_morning14

### MS14_D13_B 대체 장면 13-B. 멈췄지만 끝내지 못한 밤

- 원본 시간·장소: 학교/입구 경비실/광장 수레 · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("cart_stopped") is True and not r13_v111_value("all_cart_handed")`
- label: `r13_v111_partial13`
- 장소: square · 원본 등장: 까로, 너울, 돌목, 바둑이, 아빠, 판돌 · 무대 세우기: ["karo", "guard", "resident_badook"]
- 대사: 원문 ID 7개, 묶음 없음, 펼친 줄 7, rpy 직접 줄 0
- 그림: 배경 square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp
- 상태 값 쓰기: `outcome13`, `cart_stopped`, `pending_handover_supervised`

### MS14_D13_C 대체 장면 13-C. 사람을 끌어내리는 손

- 원본 시간·장소: 학교/입구 경비실/광장 수레 · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("false_message_admitted") is True and r13_v111_value("cart_stopped") is True`
- label: `r13_v111_crowd13`, `r13_v111_daram_crowd13`, `r13_v111_crowd_record13`, `r13_v111_crowd_guard13`, `r13_v111_crowd_watch13`, `r13_v111_crowd_legacy_menu13`, `r13_v111_crowd_block13`
- 장소: square · 원본 등장: 너울, 다람, 돌목, 아빠, 주민 · 무대 세우기: ["resident_nubi"]
- 대사: 원문 ID 9개, 묶음 crowd_record13, crowd_record_read13, riot13, crowd_block_fail13, 펼친 줄 35, rpy 직접 줄 0
- 그림: 배경 square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp
- 자료: NW_NEOUL_LEDGER 너울의 장부(surrendered)
- 상태 값 쓰기: `crowd_witnessed`, `crowd_record_read`, `crowd_resolution_done`, `crowd_injury`, `crowd_intervention`, `outcome13`, `riot_momo13`, `alive:neoul`, `alive:resident_momo`, `crowd_blocked_by_dad`
- 갈림길 운명: ["fate_crowd", "supervisor"] (`r13_v111_crowd_guard13`)
- 갈림길 운명: ["fate_crowd", "riot"] (`r13_v111_crowd_watch13`)
- 갈림길 운명: ["fate_crowd", "block"] (`r13_v111_crowd_block13`)
- 메뉴(`r13_v111_crowd_legacy_menu13`, menu): 7일 회의 기록을 함께 읽는다 / 너울을 몸으로 감싼다 / 돌목에게 너울을 맡긴다 / 주민들을 말리지 않는다

## 14일

### MS14_D14_S01 장면 14-1. 아침에도 살아 있는 사람

- 원본 시간·장소: 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("all_cart_handed") is True`
- label: `r13_v111_morning_safe14`, `r13_v111_old_rations14`, `r13_v111_altar_guide14`, `r13_v111_altar_ready14`
- 장소: school · 원본 등장: 나비, 아빠, 아이, 판돌 · 무대 세우기: ["mom", "daram", "npc_pandol", "nabi", "resident_tosil", "resident_madam"]
- 대사: 원문 ID 14개, 묶음 old_rations14, altar_guide14, 펼친 줄 32, rpy 직접 줄 0
- 그림: 배경 school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 자료: NW_BURNT_PAGE 반쯤 탄 수첩 장(observed), NW_MADAM_DAY7 백 부인 장부의 7일 줄(observed), NW_OLD_RATIONS 4년 전 집별 배급 기록(observed)
- 상태 값 쓰기: `altar_guide_confirmed`, `busy:resident_badook`
- 대기 관문 `altar_guide14` (장소 school, 인물 ["mom", "daram", "resident_badook"])
    - [0] 제단 접근로를 확인해 주십시오. — 사람 resident_badook@school → jump r13_v111_altar_ready14

### MS14_D14_S02 장면 14-2. 아무도 묶여 있지 않은 제단

- 원본 시간·장소: 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 · 생각(목표 문구): 사람을 묶는 장치와 남은 열의 쓰임은 같은 것일까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("all_cart_handed") is True and r13_v111_value("altar_guide_confirmed") is True`
- label: `r13_v111_altar14`, `r13_v111_mayor_interview14`, `r13_v111_altar1_q14`, `r13_v111_altar1_proof14`, `r13_v111_altar1_won14`, `r13_v111_altar2_q14`, `r13_v111_altar2_proof14`, `r13_v111_altar3_q14`, `r13_v111_altar3_proof14`, `r13_v111_altar4_q14`, `r13_v111_altar4_proof14`, `r13_v111_altar_close14`, `r13_v111_dallae14`, `r13_v111_device14`, `r13_v111_mayor_site_request14`, `r13_v111_mayor_site_yes14`, `r13_v111_mayor_site_no14`, `r13_v111_buri_work_start14`, `r13_v111_madam_device_question14`, `r13_v111_device_record14`, `r13_v111_device_rescue14`, `r13_v111_device_worker14`, `r13_v111_buri_record_answer14`, `r13_v111_buri_supply_answer14`, `r13_v111_buri_no_transport_answer14`, `r13_v111_madam_device_close14`, `r13_v111_device_detach14`, `r13_v111_device_detached14`, `r13_v111_guard_relief14`, `r13_v111_guard_relief_check14`, `r13_v111_guard_relieved14`, `r13_v111_device_school14`, `r13_v111_device_lock14`, `r13_v111_device_locked14`, `r13_v111_device_order14`, `r13_v111_device_supply14`, `r13_v111_device_pause14`, `r13_v111_altar4_won14`, `r13_v111_altar4_wrong14`, `r13_v111_altar3_won14`, `r13_v111_altar3_wrong14`, `r13_v111_altar2_won14`, `r13_v111_altar2_wrong14`, `r13_v111_altar1_wrong14`, `r13_v111_altar_lost14`
- 장소: altar, gate, v111_labor, school · 원본 등장: 까로, 나비, 다람, 돌목, 바둑이, 백 부인, 부리, 아빠, 엄마, 촌장 · 무대 세우기: ["mom", "daram", "resident_badook", "karo"] ["mom", "resident_ppul", "resident_badook", "karo"] ["mom", "daram", "karo", "resident_badook"] ["mom", "daram", "buri", "resident_ppul", "resident_badook", "karo"] ["mom", "daram", "karo", "nabi", "guard"]
- 대사: 원문 ID 54개, 묶음 altar1_q14, altar1_won_alt14, altar1_won14, altar2_q14, altar2_cannot14, altar2_lost14, altar3_q14, altar3_cannot14, altar3_lost14, altar4_q14, altar4_cannot14, altar4_lost14, altar_result14, buri_held14, record_question14, altar4_won14, altar3_won14, altar2_won14, altar1_lost14, altar1_half14, altar_lost14, 펼친 줄 140, rpy 직접 줄 1
- 그림: 배경 altar=room13-pixel-ready-altar0177-afternoon.webp, room13-pixel-ready-altar0177-evening.webp, room13-pixel-ready-altar0177-morning.webp; gate=room13-pixel-ready-gate0173-afternoon.webp, room13-pixel-ready-gate0173-evening.webp, room13-pixel-ready-gate0173-morning.webp; v111_labor=room13-pixel-panorama-woodshed-intact.webp; school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 자료: NW_TABLET_B 제단 밑돌의 글자(observed), NW_IRON_MARK 제단 쇠의 공방 표식(observed)
- 상태 값 쓰기: `altar_heat_structure_observed`, `mayor_false_invitation_admitted`, `altar_issue:1`, `altar_issue:2`, `altar_issue:3`, `altar_issue:4`, `mayor_site_decided`, `mayor_site_joined`, `buri_device_present`, `device_record_kind`, `device_record_shown`, `busy:karo`, `device_support_ready`, `command_confrontation_done`, `busy:buri`, `device_detached`, `guard_relief_person`, `{'expr': "'busy:' + r13_v111_value('guard_relief_person')"}`, `busy:guard`, `device_joint_control`, `dallae_first_victim_known`, `altar_half1`
- 회의 결과: `altar` → {"expr": "'win' if all((r13_v111_value('altar_issue:%d' % i) == 'won' for i in (1, 2, 3, 4))) else 'partial'"} (`r13_v111_altar_close14`)
- 회의 결과: `altar` → lose (`r13_v111_altar_lost14`)
- 대기 관문 `mayor_site_request14` (장소 gate, 인물 ["mom", "daram", "resident_ppul", "resident_badook", "karo"])
    - [0] 감독 아래 현장 확인에 동행해 주십시오. — 사람 resident_ppul@gate → jump r13_v111_mayor_site_yes14
    - [1] 이 자리에서만 확인하겠습니다. — 사람 resident_ppul@gate → jump r13_v111_mayor_site_no14
- 대기 관문 `device_detach14` (장소 altar, 인물 ["mom", "daram", "karo", "resident_badook"]) — 동적: buri_device_present 면 people 을 6명으로 바꾼다.
    - [0] 기록한 고정부를 안전하게 분리한다 — 물건 valve@altar → jump r13_v111_device_detached14
- 대기 관문 `guard_relief_check14` (장소 v111_labor, 인물 ["guard", "resident_siluk", "v111_patrol"]) — 동적: people = 돌목·실룩·(guard_relief_person 또는 순찰대원).
    - [0] 학교 인수 동안의 감독 교대를 확인합니다. — 사람 guard@v111_labor → jump r13_v111_guard_relieved14
- 대기 관문 `device_lock14` (장소 school, 인물 ["mom", "daram", "karo", "nabi", "guard"])
    - [0] 부품·기록판·열쇠 인수를 확인한다 — 물건 desks@school → jump r13_v111_device_locked14
- 대기 관문 `device_pause14` (장소 altar, 인물 ["mom", "daram", "karo", "resident_badook"])
    - [0] 장치를 살피며 기록을 다시 확인한다 — 물건 valve@altar → jump r13_v111_device_record14
- 회의/대조 「한 사람이 열흘을 산다는 숫자를 실제 기록과 견준다」 (키 `희생의 숫자와 장부를 대조한다`, 회의 altar, 기회 6, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["NW_NEOUL_LEDGER"] · 대체 [["E14_SUPPLY", "NW_KKOMI_NOSTONE", "NW_SICK_BEDS"]] · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 촌장은 ‘한 사람이 열흘을 산다’고 한다. ……그 숫자가 내가 가진 숫자와 맞나?
    - 이김 → `r13_v111_altar1_won14` {"sets": [["altar_issue:1", "won", null]], "jumps": [["r13_v111_altar2_q14", null]]}
    - 틀림 → `r13_v111_altar1_wrong14` {"sets": [["altar_half1", true, "if v111_altar_half"], ["altar_issue:1", "half", "if v111_altar_half"]], "jumps": [["r13_v111_altar1_proof14", "if (v111_altar_half and r13_nw_altar_half_ask()) or (not v111_altar_half and r13_nw_retry(\"altar\",['NW_NEOUL_LEDGER'],'half_altar1_14'))"], ["r13_v111_altar2_q14", "if v111_altar_half"], ["r13_v111_altar_lost14", null]], "retry": ["(v111_altar_half and r13_nw_altar_half_ask()) or (not v111_altar_half and r13_nw_retry(\"altar\",['NW_NEOUL_LEDGER'],'half_altar1_14'))"]}
- 회의/대조 「옛 사람들은 정말 아르카가 사람을 부른다고 적었는가」 (키 `아르카가 부른다는 말과 옛 기록을 대조한다`, 회의 altar, 기회 6, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["NW_TABLET_A", "NW_TABLET_B"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 촌장은 아르카가 ‘부른’ 사람이라고 한다. ……그 ‘부른다’는 말이 옛 기록과 맞나?
    - 이김 → `r13_v111_altar2_won14` {"sets": [["altar_issue:2", "won", null]], "jumps": [["r13_v111_altar3_q14", null]]}
    - 틀림 → `r13_v111_altar2_wrong14` {"sets": [["altar_issue:2", "lost", null]], "jumps": [["r13_v111_altar2_proof14", "if r13_nw_retry(\"altar\",['NW_TABLET_A', 'NW_TABLET_B'],'half_altar2_14')"], ["r13_v111_altar3_q14", null]], "retry": ["r13_nw_retry(\"altar\",['NW_TABLET_A', 'NW_TABLET_B'],'half_altar2_14')"]}
- 회의/대조 「그 쇠는 정말 할아버지 때부터 제단에 있었는가」 (키 `쇠가 언제 붙었는지 보인다`, 회의 altar, 기회 6, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["NW_IRON_MARK"] · 대체 없음 · 덧붙임 허용 없음
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 촌장은 쇠가 ‘할아버지 때부터’ 있었다고 한다. ……그 부분이 내가 본 것과 맞나?
    - 이김 → `r13_v111_altar3_won14` {"sets": [["altar_issue:3", "won", null]], "jumps": [["r13_v111_altar4_q14", null]]}
    - 틀림 → `r13_v111_altar3_wrong14` {"sets": [["altar_issue:3", "lost", null]], "jumps": [["r13_v111_altar3_proof14", "if r13_nw_retry(\"altar\",['NW_IRON_MARK'],None)"], ["r13_v111_altar4_q14", null]], "retry": ["r13_nw_retry(\"altar\",['NW_IRON_MARK'],None)"]}
- 회의/대조 「맨 처음 이름을 짚는다」 (키 `맨 처음 이름을 짚는다`, 회의 altar, 기회 6, 화면 r13_crisis_proof + r13_book(proof))
    - 정답 ["NW_NAMES", "NW_NEOUL_LEDGER"] · 대체 [["NW_NAMES", "NW_OLD_RATIONS"]] · 덧붙임 허용 ["NW_BURNT_PAGE"]
    - 상대 주장(두 번째 오답 속말이 옮긴 구절): 촌장은 ‘처음부터’ 그렇게 해 왔다고 한다. ……그 ‘처음’이 언제 누구였는지, 내가 가진 것과 맞나?
    - 이김 → `r13_v111_altar4_won14` {"sets": [["altar_issue:4", "won", null], ["dallae_first_victim_known", true, null]], "jumps": [["r13_v111_altar_close14", null]]}
    - 틀림 → `r13_v111_altar4_wrong14` {"sets": [["altar_issue:4", "lost", null]], "jumps": [["r13_v111_altar4_proof14", "if r13_nw_retry(\"altar\",['NW_NAMES', 'NW_NEOUL_LEDGER'],'half_altar4_14')"], ["r13_v111_altar_close14", null]], "retry": ["r13_nw_retry(\"altar\",['NW_NAMES', 'NW_NEOUL_LEDGER'],'half_altar4_14')"]}

### MS14_D14_S03 장면 14-3. 보미라는 이름

- 원본 시간·장소: 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 · 생각(목표 문구): 
- label: `r13_v111_granny_interview14`, `r13_v111_tosil_listen14`, `r13_v111_tosil_inside14`, `r13_v111_tosil_outside14`
- 장소: gate · 원본 등장: 아빠, 엄마, 토실, 할머니 · 무대 세우기: ["mom", "daram", "granny", "guard", "resident_tosil", "resident_owlgp"]
- 대사: 원문 ID 29개, 묶음 없음, 펼친 줄 58, rpy 직접 줄 0
- 그림: 배경 gate=room13-pixel-ready-gate0173-afternoon.webp, room13-pixel-ready-gate0173-evening.webp, room13-pixel-ready-gate0173-morning.webp
- 상태 값 쓰기: `tosil_listen`, `bomi_death_confirmed`, `adult_interview_done`, `location:resident_tosil`
- 메뉴(`r13_v111_tosil_listen14`, menu): 토실에게 함께 듣겠냐고 묻는다 / 밖에서 기다리고, 확인한 일을 나중에 말해 주겠다고 한다

### MS14_D14_S04 장면 14-4. 이름판 아래의 그릇

- 원본 시간·장소: 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 · 생각(목표 문구): 실제로 남은 물자는 누구에게 인수됐을까?
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("bomi_death_confirmed") is True`
- label: `r13_v111_name_board14`, `r13_v111_tosil_name14`, `r13_v111_pandol_news14`, `r13_v111_supply_inventory14`, `r13_v111_supply_inventory_done14`, `r13_v111_madam_inventory14`, `r13_v111_lamp_assignment14`, `r13_v111_chorong_lamps14`, `r13_v111_mother_lamps14`, `r13_v111_owl_alive14`, `r13_v111_unfinished_operation14`, `r13_v111_tosil_no_name14`
- 장소: square, school · 원본 등장: 나비, 다람, 돌목, 백 부인, 부엉이, 아빠, 엄마, 초롱, 토실, 판돌 · 무대 세우기: ["mom", "daram", "resident_tosil", "npc_pandol"] ["mom", "daram", "nabi", "guard"] ["mom", "daram", "nabi", "guard", "resident_lamplighter"] ["mom", "daram", "nabi", "guard", "resident_owlgp"]
- 대사: 원문 ID 26개, 묶음 name_board_intro14, 펼친 줄 37, rpy 직접 줄 0
- 그림: 배경 square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp; school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 상태 값 쓰기: `school_inventory_checked`, `school_supply_handed`, `school_heat_connected`, `current_sacrifice_operation_closed`, `lamp_manager`
- 메뉴(`r13_v111_name_board14`, menu): 토실이 이름을 쓰겠다면 기다린다 / 지금 쓰지 않아도 된다고 말한다
- 대기 관문 `supply_inventory14` (장소 school, 인물 ["mom", "daram", "nabi", "guard"])
    - [0] 실물·사용처·남은 양을 함께 확인한다 — 물건 stove@school → jump r13_v111_supply_inventory_done14

### MS14_D14_S05 장면 14-5. 엄마 몫 과자

- 원본 시간·장소: 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("family_reunited") is True and r13_v111_value("night14_lodging") in ("gate","school")`
- label: `r13_v111_cookie_scene14`, `r13_v111_cookie_distance14`, `r13_v111_wild_night14`, `r13_v111_wild_room14`, `r13_v111_wild_hall14`, `r13_v111_wild_square14`, `r13_v111_wild_road14`, `r13_v111_wild_climb14`, `r13_v111_wild_ending14`, `r13_v111_true_epilogue14`, `r13_hidden_base14`, `r13_hidden_base_room14`, `r13_hidden_base_return14`, `r13_hidden_base_door14`
- 장소:  · 원본 등장: 다람, 돌목, 아빠, 엄마 · 무대 세우기: ["mom", "daram", "nabi"] ["mom", "daram", "doto"] ["mom", "daram", "resident_badook"] ["mom", "daram", "guard"] ["mom", "daram"] ["daram"]
- 대사: 원문 ID 19개, 묶음 ending_last14, wild_wake14, wild_hall14, wild_hall_help14, wild_square14, wild_square_help14, wild_road14, wild_road_help14, wild_climb14, end_wild_night14, end_true14, hidden_base_offer14, hidden_base_arrival14, hidden_base_section14, hidden_base_incident14, hidden_base_notebook14, hidden_base_notebook_kept14, hidden_base_return14, hidden_base_frame14, hidden_base_paper_set14, hidden_base_plate_right14, hidden_base_plate_wrong14, hidden_base_open14, hidden_base_stuck14, 펼친 줄 180, rpy 직접 줄 0
- 그림: 배경 (이동 없음 — 앞 장면 배경 유지) · r13_scene [{"expr": "R13_PLACES[room13['location']][1]"}, {"expr": "R13_PLACES[room13['location']][0]"}], [{"expr": "R13_PLACES['school'][1]"}, "불타는 밤"], [{"expr": "R13_PLACES['square'][1]"}, "불타는 밤"], [{"expr": "R13_PLACES['forest'][1]"}, "불타는 밤"], [{"expr": "R13_PLACES['greenhouse'][1]"}, "불타는 밤"], [{"expr": "R13_PLACES['gate'][1]"}, "말을 위한 돌"], [{"expr": "R13_PLACES['hidden_base14'][1]"}, "옛 시설 정비실"] · 컷 ev:HIDDEN_A4_section, ev:HIDDEN_A4_checklist, ev:HIDDEN_A5_notebook, ev:HIDDEN_A3_paper_marked, ev:HIDDEN_A3_plate_front, ev:HIDDEN_A3_plate_back
- 상태 값 쓰기: `story14_completed`, `ending14`, `wild_night14`, `wild_late`, `wild_family`, `hidden_base:finished`, `hidden_base:entered`, `hidden_base:read_section`, `hidden_base:read_incident`, `hidden_base:notebook_taken`, `hidden_base:returned`, `hidden_base:frame_seen`, `hidden_base:paper_set`, `hidden_base:aligned`, `hidden_base:opened`
- 대기 관문 `wild_room14` (장소 school, 인물 ["mom", "daram", "nabi"])
    - [0] 담요와 외투를 챙긴다 — 물건 blankets@school → (이 label 에서 따로 처리 없음)
- 대기 관문 `wild_hall14` (장소 school, 인물 ["mom", "daram", "doto"])
    - [0] 도토 씨, 바구니 내려놓으세요. — 사람 doto@school → set wild_late={'expr': "(r13_v111_value('wild_late') or 0) + 1"}; 대사 wild_hall_help14
    - [1] 뒷문으로 돌아 광장으로 간다 — 이동 square@square → (이 label 에서 따로 처리 없음)
- 대기 관문 `wild_square14` (장소 square, 인물 ["mom", "daram", "resident_badook"])
    - [0] 바둑이 씨, 같이 문을 밉시다. — 사람 resident_badook@square → set wild_late={'expr': "(r13_v111_value('wild_late') or 0) + 1"}; 대사 wild_square_help14
    - [1] 다람과 산길 쪽으로 간다 — 이동 forest@forest → (이 label 에서 따로 처리 없음)
- 대기 관문 `wild_road14` (장소 forest, 인물 ["mom", "daram", "guard"])
    - [0] 돌목 씨, 같이 가요. 여기 있으면 안 돼요. — 사람 guard@forest → set wild_late={'expr': "(r13_v111_value('wild_late') or 0) + 1"}; 대사 wild_road_help14
    - [1] 초소를 등지고 첫 굽이로 오른다 — 물건 forest_roots@forest → (이 label 에서 따로 처리 없음)
- 대기 관문 `hidden_base_offer14` (장소 school, 인물 ["mom", "daram"])
    - [0] 수첩을 챙기러 같이 가자. — 사람 mom@school → (이 label 에서 따로 처리 없음)
    - [1] 오늘은 여기서 쉰다 — 물건 blankets@school → (이 label 에서 따로 처리 없음)
- 대기 관문 `hidden_base_room14` (장소 hidden_base14, 인물 ["mom", "daram"])
    - [0] 정비 단면판을 읽는다 — 물건 hb_section@hidden_base14 → 대사 hidden_base_section14; set hidden_base:read_section=True
    - [1] 고장 점검표를 읽는다 — 물건 hb_incident@hidden_base14 → 대사 hidden_base_incident14; set hidden_base:read_incident=True
    - [2] 엄마의 현장 수첩을 챙긴다 — 물건 hb_notebook@hidden_base14 → (이 label 에서 따로 처리 없음)
    - [3] 학교로 돌아간다 — 물건 hb_door@hidden_base14 → jump r13_hidden_base_return14
- 대기 관문 `hidden_base_door14` (장소 hidden_base14, 인물 ["mom", "daram"])
    - [0] 문틀의 홈을 살핀다 — 물건 hb_door@hidden_base14 · 조건 값 hidden_base:frame_seen == null → 대사 hidden_base_frame14; set hidden_base:frame_seen=True
    - [1] 홈 위에 종이를 댄다 — 물건 hb_door@hidden_base14 · 조건 값 hidden_base:frame_seen == true; 값 hidden_base:paper_set == null → 대사 hidden_base_paper_set14; set hidden_base:paper_set=True
    - [2] 표시한 면을 바깥으로 끼운다 — 물건 hb_door@hidden_base14 · 조건 값 hidden_base:paper_set == true → 대사 hidden_base_plate_right14; set hidden_base:aligned=True
    - [3] 표시한 면을 안으로 끼운다 — 물건 hb_door@hidden_base14 · 조건 값 hidden_base:paper_set == true → 대사 hidden_base_plate_wrong14; set hidden_base:aligned=False
    - [4] 문을 연다 — 물건 hb_door@hidden_base14 → 대사 hidden_base_stuck14
    - [5] 학교로 돌아가자. — 사람 mom@hidden_base14 → jump r13_hidden_base_return14

### MS14_D14_END_FAMILY 가족 철수 결말 — 열지 않은 문

- 원본 시간·장소: 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("outcome13")=="family_priority"`
- label: `r13_v111_family_ending14`, `r13_v111_family_lodging14`, `r13_v111_cookie_gate14`
- 장소: gate · 원본 등장: 다람, 돌목, 아빠, 엄마 · 무대 세우기: ["mom", "daram", "guard"] ["mom", "daram"]
- 대사: 원문 ID 9개, 묶음 없음, 펼친 줄 11, rpy 직접 줄 0
- 그림: 배경 gate=room13-pixel-ready-gate0173-afternoon.webp, room13-pixel-ready-gate0173-evening.webp, room13-pixel-ready-gate0173-morning.webp
- 상태 값 쓰기: `night14_lodging`

### MS14_D14_END_PARTIAL 부분 구조 결말 — 남은 인계표

- 원본 시간·장소: 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("outcome13")=="partial_rescue"`
- label: `r13_v111_partial_ending14`, `r13_v111_partial_departed14`, `r13_v111_cookie14`, `r13_v111_partial_handoff14`, `r13_v111_partial_work14`, `r13_v111_partial_patient14`, `r13_v111_partial_receipt14`, `r13_v111_partial_received14`, `r13_v111_partial_wait14`
- 장소: square, school · 원본 등장: 까로, 다람, 돌목, 아빠 · 무대 세우기: ["karo", "guard", "resident_badook", "daram"] ["mom", "daram"] ["karo", "guard", "resident_badook"]
- 대사: 원문 ID 10개, 묶음 partial_departed14, 펼친 줄 18, rpy 직접 줄 0
- 그림: 배경 square=room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp; school=room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp
- 상태 값 쓰기: `night14_lodging`, `{'expr': "'handed:' + v111_pending_patient"}`, `pending_handover_completed`, `pending_handover_supervised`
- 대기 관문 `partial_handoff14` (장소 square, 인물 ["karo", "guard", "resident_badook"])
    - [0] 남은 인계에 직접 참여한다 — 물건 cart@square → jump r13_v111_partial_work14
- 대기 관문 `partial_receipt14` (장소 school, 인물 ["mom", "daram", "nabi", "karo", "guard"]) — 동적: v111_pending_patient 를 people 에 더한다.
    - [0] 새로 난 침상에 이분을 받아 주시겠습니까? — 사람 nabi@school → jump r13_v111_partial_received14

### MS14_D14_END_VIOLENCE 군중 폭력 결말 — 한 명의 자리가 더 필요하다

- 원본 시간·장소: 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 · 생각(목표 문구): 
- 진입 조건(어기면 예외로 멈춤): 자료 , 값  · 검사 `lambda:r13_v111_value("crowd_injury") is True`
- label: `r13_v111_violence_ending14`, `r13_v111_crowd_child_saw14`, `r13_v111_crowd_child_away14`, `r13_v111_crowd_failed14`, `r13_v111_crowd_no_action14`
- 장소: clinic · 원본 등장: 다람, 서리, 아빠, 주민 · 무대 세우기: ["mom", "daram", "guard", "resident_seori"]
- 대사: 원문 ID 12개, 묶음 없음, 펼친 줄 14, rpy 직접 줄 0
- 그림: 배경 clinic=room13-pixel-ready-clinic0177-afternoon.webp, room13-pixel-ready-clinic0177-evening.webp, room13-pixel-ready-clinic0177-morning.webp

## 회의 11개

기회 = 회의마다 함께 쓰는 수(`R13_NW_TRIES_BY_MEETING`). 틀리면 기회 1 사용, 마지막 기회의 오답이 그대로 결과가 된다(`r13_nw_retry`). 결과는 한 번만 적힌다(`r13_nw_meeting_end`).

| 회의 | 기회 | 쟁점(증명 키) | 이김 label | 반쪽 label | 짐 label |
|---|---|---|---|---|---|
| `gate` | 무제한 | 함께 들어갈 근거를 고른다 | r13_v111_gate_proven, r13_v111_gate_early |  | r13_v111_gate_number, r13_v111_gate_wrong |
| `lamp` | 7 | 수리 뒤 새로 생긴 파손을 가린다 / 남아 있는 돌과 칼의 사용을 연결한다 / 수리와 반출을 가릴 자료를 낸다 / 돌과 매입 기록을 낸다 / 바깥 걸쇠 주장과 발견 위치를 대조한다 / 마지막 점검과 인수한 돌을 연결한다 | r13_lamp_attempt_win3, r13_v111_badugi_arrives | r13_lamp_attempt_partial3, r13_v111_trial_wrong_stone, r13_v111_trial_wrong_latch, r13_v111_knife_wrong, r13_v111_trial_wrong_sale | r13_lamp_attempt_wrong3, r13_v111_trial_wrong |
| `gate_post` | 3 | 밤이 혐의의 근거를 확인한다 | r13_v111_bami_clear5 |  | r13_v111_wrong5 |
| `fire` | 4 | 불이 시작된 곳과 진술을 대조한다 / 불의 원인과 빈 창고 진압을 구분한다 / 불의 원인과 아이 구조를 구분한다 | r13_v111_responsibility_answers7 | r13_v111_responsibility_wrong7 | r13_v111_nubi_wrong7 |
| `room13` | 7 | 두 상처와 촛대 파손을 대조한다 / 두 번째 길을 실제 기록으로 보인다 / 구리선과 수선 출처를 대조한다 / 첫 비명 뒤 핀을 다시 채운 때 / 접촉면과 아이의 위치를 대조한다 | r13_v111_contact_answer10 | r13_v111_contact_wrong10, r13_v111_time_wrong10, r13_v111_owner_wrong10 | r13_v111_passage_wrong10, r13_v111_hearing_wrong10 |
| `hypothesis` | 13 | 초롱과 피코의 하루를 대조한다 / 아르카가 없는 아이들과 대조한다 / 13호 난로의 돌을 내놓는다 / 요즘 돌이 어디서 오는지 대조한다 / 창고에서 잠자는 사람을 짚는다 |  | r13_v111_hyp5_after_lost11 | r13_v111_hyp_lost_gate11 |
| `soup` | 5 | 재사용 설명과 개봉 봉인을 대조한다 / 파편·봉인·취급 구간을 함께 제시한다 / 명단과 흰 그릇을 대조한다 | r13_v111_list_won12 | r13_v111_list_wrong12 | r13_v111_fragment_wrong12, r13_v111_medicine_wrong12 |
| `altar` | 6 | 희생의 숫자와 장부를 대조한다 / 아르카가 부른다는 말과 옛 기록을 대조한다 / 쇠가 언제 붙었는지 보인다 / 맨 처음 이름을 짚는다 |  |  | r13_v111_altar_lost14 |
| `blanket` | 4 | 아내가 봤다는 담요의 시점을 확인한다 / 촌장이 어젯밤 있던 곳을 확인한다 | r13_v111_badook_won13 | r13_v111_badook_wrong13 | r13_v111_mending_wrong13 |
| `piko` | 4 | 인수하지 않은 돌의 약속 값을 보인다 / 장부의 두 배를 실룩에게 보인다 / 피코가 막혀야 했던 까닭을 보인다 | r13_v111_rein_won13 |  | r13_v111_rein_wrong13 |
| `records` | 4 | 수신인과 가족 전달 권한을 구분한다 / 반송·필사본·초대 발송을 대조한다 | r13_v111_writing_answer10 | r13_v111_writing_wrong10 | r13_v111_authority_wrong10 |

전체 증명 38곳은 `inventory.json` 의 `proofs`(정답·대체·덧붙임·성공/오답/되묻기 label·되돌아갈 현장).

| 날 | 보이는 제목 | 키 | 회의 | 정답 | 대체 정답 | 덧붙임 |
|---|---|---|---|---|---|---|
| 1 | 다람의 이름까지 등록하고 함께 들어갈 근거를 고른다 | `함께 들어갈 근거를 고른다` | gate | ["E02", "E03"] | [] | ["E01", "E04"] |
| 1 | 두 편지를 나란히 본다 | `두 편지를 나란히 본다` |  | ["E01", "E06"] | [] | [] |
| 3 | 등 안의 칼끝 조각은 톡이 고친 뒤에 생긴 것인가 | `수리 뒤 새로 생긴 파손을 가린다` | lamp | ["NW_LA_CHECK", "NW_LA_FIELD"] | [] | [] |
| 3 | 실룩이 한 말이, 칼끝이 부러진 자리와 맞는가 | `남아 있는 돌과 칼의 사용을 연결한다` | lamp | ["NW_LA_CHECK", "NW_LA_FIELD", "NW_LA_KNIFE"] | [] | [] |
| 5 | 돌목이 붙잡은 사람을, 울타리 천에서부터 거슬러 잇는다 | `밤이 혐의의 근거를 확인한다` | gate_post | ["E20", "E22", "E23", "E24"] | [["E20", "E22", "NW_PIKO_SKETCH4"], ["E20", "E22", "E23", "NW_PIKO_SKETCH4"], ["E20", "E22", "E24", "NW_PIKO_SKETCH4"]] | ["E21", "NW_PIKO_SKETCH4"] |
| 5 | 두 편지의 초대를 대조한다 | `두 편지의 초대를 대조한다` |  | ["E01", "E27"] | [] | [] |
| 7 | 불이 시작된 곳과 진술을 대조한다 | `불이 시작된 곳과 진술을 대조한다` | fire | ["E06_FIRE"] | [] | [] |
| 10 | 두 상처와 촛대 파손을 대조한다 | `두 상처와 촛대 파손을 대조한다` | room13 | ["E08_CHILD_ACCOUNT", "E08_TOOL"] | [] | [] |
| 10 | 정말 그 문 말고는 책상까지 갈 길이 없었는가 | `두 번째 길을 실제 기록으로 보인다` | room13 | ["E09_PASSAGE", "E08_ROOM"] | [] | [] |
| 10 | 이 핀을 구별할 수 있는가 | `구리선과 수선 출처를 대조한다` | room13 | ["E08_WOUND_WIRE", "E09_PIN_OWNER"] | [["E08_CONTACT_ASSEMBLY", "E09_PIN_OWNER"]] | [] |
| 10 | 핀이 언제 떨어졌는가 | `첫 비명 뒤 핀을 다시 채운 때` | room13 | ["E09_PIN_TIME", "E09_PIN_HANDOVER_TIME"] | [] | [] |
| 10 | 방금 설명은 물증과 맞는가 | `접촉면과 아이의 위치를 대조한다` | room13 | ["E08_CONTACT_ASSEMBLY", "E08_WOUND_WIRE", "E08_CHILD_POSITION", "E08_ROOM_REACH", "E09_SCARF"] | [] | [] |
| 12 | 그 병은 정말 약을 다 쓴 빈 병이었는가 | `재사용 설명과 개봉 봉인을 대조한다` | soup | ["E12_FRAGMENT", "E12_SEAL"] | [] | [] |
| 12 | 선생님은 정말 씻는 데서 물을 받았는가 | `파편·봉인·취급 구간을 함께 제시한다` | soup | ["E12_FRAGMENT", "E12_SEAL", "E12_HANDLING"] | [] | [] |
| 12 | 작은 냄비는 정말 아이들 모두를 위한 것이었는가 | `명단과 흰 그릇을 대조한다` | soup | ["NW_TRANSFER_LIST", "NW_WHITE_BOWLS"] | [["NW_WHITE_BOWLS", "NW_RETURNED_BOWL"]] | ["NW_RETURNED_BOWL", "NW_SICK_BEDS"] |
| 14 | 한 사람이 열흘을 산다는 숫자를 실제 기록과 견준다 | `희생의 숫자와 장부를 대조한다` | altar | ["NW_NEOUL_LEDGER"] | [["E14_SUPPLY", "NW_KKOMI_NOSTONE", "NW_SICK_BEDS"]] | [] |
| 14 | 옛 사람들은 정말 아르카가 사람을 부른다고 적었는가 | `아르카가 부른다는 말과 옛 기록을 대조한다` | altar | ["NW_TABLET_A", "NW_TABLET_B"] | [] | [] |
| 14 | 그 쇠는 정말 할아버지 때부터 제단에 있었는가 | `쇠가 언제 붙었는지 보인다` | altar | ["NW_IRON_MARK"] | [] | [] |
| 14 | 맨 처음 이름을 짚는다 | `맨 처음 이름을 짚는다` | altar | ["NW_NAMES", "NW_NEOUL_LEDGER"] | [["NW_NAMES", "NW_OLD_RATIONS"]] | ["NW_BURNT_PAGE"] |
| 13 | 아내가 봤다는 담요의 시점을 확인한다 | `아내가 봤다는 담요의 시점을 확인한다` | blanket | ["E13_MENDING"] | [] | ["E35"] |
| 13 | 촌장이 어젯밤 있던 곳을 확인한다 | `촌장이 어젯밤 있던 곳을 확인한다` | blanket | ["NW_HALL_WINDOW"] | [] | ["E29"] |
| 13 | 실룩이 말한 ‘아무 등이나, 값은 다 같다’가 맞는가 | `인수하지 않은 돌의 약속 값을 보인다` | piko | ["NW_LA_OFFER"] | [] | [] |
| 13 | 실룩이 말한 ‘아무 등이나, 값은 다 같다’가 맞는가 | `장부의 두 배를 실룩에게 보인다` | piko | ["E16"] | [] | ["E34"] |
| 13 | 피코가 막혀야 했던 까닭을 보인다 | `피코가 막혀야 했던 까닭을 보인다` | piko | ["NW_PIKO_PAINTING"] | [] | [] |
| 11 | 초롱과 피코의 하루를 대조한다 | `초롱과 피코의 하루를 대조한다` | hypothesis | ["E11", "E08", "NW_PIKO_TREMOR"] | [["E11", "NW_PIKO_TREMOR"], ["NW_LA_CHECK", "E08", "NW_PIKO_TREMOR"], ["NW_LA_CHECK", "NW_PIKO_TREMOR"]] | ["E08", "E28"] |
| 11 | 아르카가 없는 아이들과 대조한다 | `아르카가 없는 아이들과 대조한다` | hypothesis | ["NW_KKOMI_NOSTONE", "NW_SICK_BEDS"] | [] | [] |
| 11 | 아르카가 사람을 무너뜨리는 것을 직접 본 일이 있는가 | `13호 난로의 돌을 내놓는다` | hypothesis | ["NW_STONE"] | [] | [] |
| 11 | 요즘 돌이 어디서 오는지 대조한다 | `요즘 돌이 어디서 오는지 대조한다` | hypothesis | ["NW_INNER_PRICE", "NW_MUSOE_DEEP"] | [] | ["E14"] |
| 11 | 돌이 산더미인 그 창고 곁에서는 정말 아무도 무너지지 않았는가 | `창고에서 잠자는 사람을 짚는다` | hypothesis | ["NW_KEEPER_DATE"] | [] | [] |
| 10 | 수신인과 가족 전달 권한을 구분한다 | `수신인과 가족 전달 권한을 구분한다` | records | ["E06_CONTACT", "E09_MAIL"] | [] | [] |
| 10 | 그 초대장을 아내가 보냈다고 할 수 있는가 | `반송·필사본·초대 발송을 대조한다` | records | ["E01", "E07", "E09_MAIL"] | [["E01", "E27", "E09_MAIL"]] | ["E07", "E27", "E09"] |
| 7 | ‘다들 책임이 있소’. 셋이 정말 같은 책임인가 | `불의 원인과 빈 창고 진압을 구분한다` | fire | ["E06_FIRE", "E06_EMPTY", "E07_NUBI"] | [["E06_FIRE", "E06_EMPTY", "NW_NUBI_TICKET"]] | ["NW_LAUNDRY_TALK", "E02"] |
| 7 | ‘다들 책임이 있소’. 셋이 정말 같은 책임인가 | `불의 원인과 아이 구조를 구분한다` | fire | ["E06_FIRE", "E06_RESCUE", "E07_NUBI"] | [["E06_FIRE", "E06_RESCUE", "NW_NUBI_TICKET"]] | ["NW_LAUNDRY_TALK", "E02"] |
| 3 | 우박 씨가 잰 뒤에도 3번 등 안에 돌이 있었는가 | `측정 종료와 점검 기록을 대조한다` |  | ["E13", "E11"] | [] | [] |
| 3 | 톡이 고친 뒤로, 3번 등이 열린 때를 차례로 잇는다 | `수리와 반출을 가릴 자료를 낸다` | lamp | ["E11", "E12", "E13"] | [] | ["E10"] |
| 3 | 사라진 3번 등의 돌은 어디로, 누구 손을 거쳐 갔는가 | `돌과 매입 기록을 낸다` | lamp | ["E15", "E16"] | [] | [] |
| 3 | 실룩이 한 말이, 칼끝이 부러진 자리와 맞는가 | `바깥 걸쇠 주장과 발견 위치를 대조한다` | lamp | ["E17", "E32", "E33"] | [] | [] |
| 3 | 실룩이 판 돌은 새벽까지 등 안에 있던 바로 그 돌인가 | `마지막 점검과 인수한 돌을 연결한다` | lamp | ["E11", "E15", "E16"] | [] | [] |

## 메뉴 선택지(menu: / display_menu) 37곳

| 날 | 장면 | label | 종류 | 선택지 → 결과 |
|---|---|---|---|---|
| None |  | `r13_v111_wait_again` | display_menu | (계산) v111_object_options |
| 1 | D01_S01 | `r13_v111_letter_menu` | display_menu | (계산) v111_menu |
| 1 | D01_S05 | `r13_v111_inn` | display_menu | 다람의 손을 천으로 감싸 준다(=0) |
| 1 | D01_S05 | `r13_v111_room_compare` | display_menu | 할머니에게 초롱의 행방을 묻는다(=0) / 방을 더 둘러본다(=1) |
| 1 | D01_S05 | `r13_v111_room_compare` | display_menu | 다람의 이불을 여민다(=0) |
| 3 | D03_S05 | `r13_v111_custody_choice` | display_menu | (계산) v111_menu |
| 5 | D05_S04 | `r13_v111_warning_compared5` | menu | 첫날 기록을 다시 본다 → r13_v111_review5 / 답장을 쓴다 → (이어감) |
| 6 | D06_S01 | `r13_v111_day6` | menu | 그릇을 돌려주러 같이 가자. → r13_v111_bowl_together6 · set choice:MS14_D06_S01=together / 오늘은 먹었니? 먹을 것부터 알아보자. → r13_v111_bowl_eat6 · set choice:MS14_D06_S01=eat_first |
| 7 | D07_S01 | `r13_v111_day7` | menu | 아이들은 학교에서 기다리게 하자. → r13_v111_children_school7 · set choice:MS14_D07_S01=school / 여기서 계속 묻는다. → r13_v111_children_here7 · set choice:MS14_D07_S01=here |
| 7 | D07_S01 | `r13_v111_nubi_first_question7` | menu | 문 앞의 기름 흔적을 설명해 주십시오. → (이어감) · set fire_first_question=oil / 등잔은 뒷벽 물통 옆에 있었습니다. 뚜껑도 닫혀 있었고요. → (이어감) · set fire_first_question=lamp / 창고 문 앞에 서 계신 걸 보리 씨가 봤습니다. → (이어감) · set fire_first_question=door |
| 11 | D11_S02A | `r13_v111_dry11` | menu | 두 장을 꺼내 덮는다 [if r13_v111_value('carried_dry_blankets')==2] → r13_v111_blanket_use11 / 한 장을 함께 덮는다 [if r13_v111_value('carried_dry_blankets')==1] → r13_v111_blanket_one11 / 짐 안에 둔다 [if r13_v111_value('carried_dry_blankets')>0] → r13_v111_blanket_keep11 / 외투 안쪽을 함께 덮는다 [if r13_v111_value('carried_dry_blankets')==0] → r13_v111_coat_use11 |
| 11 | D11_S03 | `r13_v111_heat_seen11` | display_menu | 벽 아래 깨진 돌판을 들여다본다(=0) |
| 11 | D11_S03 | `r13_v111_heat_seen11` | display_menu | 그림 옆 벽에 새긴 글씨를 본다(=0) |
| 11 | D11_S03 | `r13_v111_heat_seen11` | menu | 가족 자리부터 본다 → r13_v111_family_place11 / 아랫길 대피 준비를 확인한다 → r13_v111_rescue_prepare11 / 준비된 물자를 학교로 옮긴다 → r13_v111_supply_school11 |
| 11 | D11_S03 | `r13_v111_blanket_choice11` | menu | 가족 짐에 보관한다 → r13_v111_blanket_store11 / 토실에게 한 장을 건넨다 → r13_v111_tosil_blanket11 |
| 11 | D11_S03 | `r13_v111_hyp0_menu11` | menu | 야생화는 옮는 병이다 → r13_v111_hyp0_sick11 / 아르카가 사람을 부른다 → r13_v111_hyp0_call11 / 꺼낸 아르카 곁에 오래 있던 사람부터 무너진다 → r13_v111_hyp0_won11 / 늙으면 누구나 그렇게 된다 → r13_v111_hyp0_old11 |
| 12 | D12_S02 | `r13_v111_meal12` | display_menu | 흰 그릇을 작은 배식대로 나른다(=0) |
| 12 | D12_S02 | `r13_v111_meal_choice12` | menu | 배식 전에 더 살핀다 → r13_v111_stay_meal12 / 다람과 장작을 받으러 간다 → r13_v111_take_daram12 / 다람은 나비 곁에 두고 다녀온다 → r13_v111_leave_daram12 / 아침에 부탁한 일들을 확인한다 → r13_v111_prevent_check12 |
| 12 | D12_S04 | `r13_v111_medical_arrival12` | menu | 약장 밖에 맡긴 약도 있는지 묻는다 → (이어감) / 장부를 다시 보여 달라고 한다 → (이어감) |
| 12 | D12_S05 | `r13_v111_aftermath_late12` | menu | 돌목에게 감독을 맡긴다 → r13_v111_teacher_guard_late12 / 너울에게 신병을 넘긴다 → r13_v111_teacher_neoul_late12 |
| 13 | D13_S02 | `r13_v111_offer13` | menu | 조건을 더 묻는다 → r13_v111_offer_question13 / 가족 셋이 수락하고 물러난다 [if r13_v111_value('family_offer_terms_seen')] → r13_v111_offer_accept13 / 거절하고 현장에 남는다 [if r13_v111_value('family_school_place')] → r13_v111_offer_refuse13 |
| 14 | D14_S03 | `r13_v111_tosil_listen14` | menu | 토실에게 함께 듣겠냐고 묻는다 → r13_v111_tosil_inside14 / 밖에서 기다리고, 확인한 일을 나중에 말해 주겠다고 한다 → r13_v111_tosil_outside14 |
| 14 | D14_S04 | `r13_v111_name_board14` | menu | 토실이 이름을 쓰겠다면 기다린다 → r13_v111_tosil_name14 / 지금 쓰지 않아도 된다고 말한다 → r13_v111_tosil_no_name14 |
| 13 | D13_S04 | `r13_v111_family_position13` | menu | 엄마와 다람이 곁에 남게 한다 → r13_v111_family_stay13 / 엄마와 다람을 까로와 학교로 보낸다 [if not r13_v111_value('busy:karo')] → r13_v111_family_karo13 / 엄마와 다람을 네로와 학교로 보낸다 [if r13_v111_value('nero_alive') and not r13_v111_value('busy:resident_nero') and r13_v111_actor_ready("resident_nero")] → r13_v111_family_nero13 |
| 13 | D13_S04 | `r13_v111_handover_plan13` | menu | 학교 침상과 인수를 먼저 확인한다 → r13_v111_school_handover_prep13 / 하차한 사람부터 부축한다 [if r13_v111_value('handover_prepared13')] → r13_v111_pandol_down13 / 보온·감독 아래 인계를 기다린다 → r13_v111_partial13 / 검증한 기록을 공개한다 [if r13_v111_value('false_message_admitted') and not r13_v111_value('crowd_resolution_done')] → r13_v111_crowd_prepare13 |
| 13 | D13_C | `r13_v111_crowd_legacy_menu13` | menu | 7일 회의 기록을 함께 읽는다 [if r13_v111_value('neoul_promise_proven') and r13_v111_person_alive('resident_nubi') and r13_v111_person_alive('neoul')] → r13_v111_crowd_record13 / 너울을 몸으로 감싼다 → r13_v111_crowd_block13 / 돌목에게 너울을 맡긴다 [if not r13_v111_value('busy:guard')] → r13_v111_crowd_guard13 / 주민들을 말리지 않는다 → r13_v111_crowd_watch13 |
| 12 | D12_S04 | `r13_v111_aftermath_pre12` | menu | 돌목에게 감독을 맡긴다 → r13_v111_teacher_guard_pre12 / 너울에게 신병을 넘긴다 → r13_v111_teacher_neoul_pre12 |
| 11 | D11_S03 | `r13_v111_hyp1_q11` | menu | 두 사람이 아르카 곁에 머문 시간을 비교한다 → r13_v111_hyp1_reason11 / 두 사람의 나이와 몸 상태를 비교한다 → r13_v111_hyp1_badreason11 / 두 사람이 아르카를 만진 방식을 비교한다 → r13_v111_hyp1_badreason11 |
| 11 | D11_S03 | `r13_v111_hyp2_q11` | menu | 켜지 않고 쌓아 둔 돌은 아무 해가 없다 → r13_v111_hyp2_badreason11 / 백 부인은 그 돌 곁에서 잠을 자지 않는다 → r13_v111_hyp2_reason11 / 백 부인은 돌을 팔기만 한다 → r13_v111_hyp2_badreason11 |
| 11 | D11_S03 | `r13_v111_hyp3_q11` | menu | 요즘 사람들이 약해졌다 → r13_v111_hyp3_badreason11 / 외지 사람이 병을 들여왔다 → r13_v111_hyp3_badreason11 / 요즘 태우는 돌이 더 독하다 → r13_v111_hyp3_reason11 |
| 11 | D11_S03 | `r13_v111_hyp4_q11` | menu | 아이들이 밤을 어디서 보내는지 본다 → r13_v111_hyp4_reason11 / 아이와 어른의 몸을 비교한다 → r13_v111_hyp4_badreason11 / 아이들이 아르카를 어떻게 다루는지 본다 → r13_v111_hyp4_badreason11 |
| 11 | D11_S03 | `r13_v111_hyp5_q11` | menu | 한 방의 돌이 바뀌자 한 사람이 한 저녁 사이에 무너졌다 [if r13_v111_value('OWL_ALIVE') is False] → r13_v111_hyp5_reason11 / 한 방의 돌을 치우자 무너지던 사람이 돌아왔다 [if r13_v111_value('OWL_ALIVE') is not False and r13_v111_value('prevention')!='stone'] → r13_v111_hyp5_reason11 / 한 방의 돌을 꺼내자 그 앞에서 흐려지던 머리가 맑아졌다 [if r13_v111_value('prevention')=='stone'] → r13_v111_hyp5_reason11 / 부엉이 어르신은 원래 아팠다 → r13_v111_hyp5_badreason11 / 13호가 추워서 그렇다 → r13_v111_hyp5_badreason11 |
| 10 | D10_P01 | `r13_v111_pocket_answer10` | menu | 가족끼리 확인하고, 왜 숨겼는지 묻는다 → r13_v111_family_paper10 / 공개된 수량만 대조하고 기록을 받는다 → r13_v111_public_paper10 |
| 3 | D03_S03 | `r13_v111_clinic3` | display_menu | (무엇부터 물을까?)(=None) / 꺼낸 시각부터 묻는다(=0) / 다시 넣은 게 확실한지 묻는다(=1) |
| 3 | D03_S05 | `r13_v111_trial_knife` | display_menu | (계산) v111_menu |
| 3 | D03_S05 | `r13_v111_stone_choice` | display_menu | (계산) v111_menu |
| 1 | D01_S02 | `r13_v111_gate_shelf_menu` | display_menu | (계산) [(r13_gate_shelf_names[0] + ' 칸을 꺼낸다', 'before'), (r13_gate_shelf_names[1] + ' 칸을 꺼낸다', 'today'), (r13_gate_shelf_names[2] + ' 칸을 꺼낸다', 'after')] |

## 분기 조건 (R13_NW_WHEN 308개 + 장면 진입 검사)

「뜻」은 코드 곁 주석이 있으면 그것, 없으면 코드를 풀어 쓴 것(`[키]` = r13_v111_value). 대사 패치(dNN)의 when 에 이름으로 쓰인다.

| 이름 | 뜻 | 코드 풀이 | 쓰인 수 |
|---|---|---|---|
| `always` |  | True | 0 |
| `lamp_attempt_sheltered` |  | bool([lamp_bound2]) 그리고 bool([piko_sheltered]) | 1 |
| `lamp_attempt_outside` |  | bool([lamp_bound2]) 그리고 아님 [piko_sheltered] | 1 |
| `lamp_stolen_silluk_listed` |  | 아님 [lamp_bound2] 그리고 bool([listed:resident_siluk]) | 1 |
| `lamp_attempt_silluk_listed` |  | bool([lamp_bound2]) 그리고 bool([listed:resident_siluk]) | 1 |
| `lamp_attempt` |  | bool([lamp_bound2]) | 8 |
| `piko_alive_lamp_stolen` |  | [piko_alive] ≠거짓 그리고 아님 [lamp_bound2] | 3 |
| `lamp_stolen` |  | 아님 [lamp_bound2] | 6 |
| `hp_known_trusted` |  | bool([hidden_pandol:met]) 그리고 R13_NW_WHEN["town_won_before11"]() | 1 |
| `hp_known_untrusted` |  | bool([hidden_pandol:met]) 그리고 R13_NW_WHEN["town_won_none_before11"]() | 1 |
| `hp_unknown_trusted` |  | 아님 [hidden_pandol:met] 그리고 R13_NW_WHEN["town_won_before11"]() | 1 |
| `hp_unknown_untrusted` |  | 아님 [hidden_pandol:met] 그리고 R13_NW_WHEN["town_won_none_before11"]() | 1 |
| `owl_alive` |  | [OWL_ALIVE] ≠거짓 | 2 |
| `owl_dead` |  | [OWL_ALIVE] =거짓 | 9 |
| `piko_alive` |  | [piko_alive] ≠거짓 | 6 |
| `end_portrait_child` | 0.20.7 (ending review 4·5·6·13·15): one last act per path, after the shared snack scene. | [piko_alive] =거짓 그리고 [portrait]=="child_completed" 그리고 아님 r13_nw_true_ending_ready() | 1 |
| `end_family` |  | [ending14]=="family" | 1 |
| `end_partial_departed` |  | [ending14]=="partial" 그리고 bool([cart_departed]) | 1 |
| `end_partial_waiting` |  | [ending14]=="partial" 그리고 아님 [cart_departed] 그리고 아님 [pending_handover_completed] | 3 |
| `end_partial_done` |  | [ending14]=="partial" 그리고 아님 [cart_departed] 그리고 bool([pending_handover_completed]) | 1 |
| `end_injury` |  | bool([crowd_injury]) | 1 |
| `end_morning_won` |  | [ending14]=="morning" 그리고 [meeting:altar]=="win" 그리고 아님 r13_nw_true_ending_ready() | 1 |
| `end_morning_partial` |  | [ending14]=="morning" 그리고 [meeting:altar]=="partial" | 2 |
| `end_morning_lost` |  | [ending14]=="morning" 그리고 [meeting:altar]=="lose" | 2 |
| `piko_dead` |  | [piko_alive] =거짓 | 12 |
| `kkomi_alive` |  | [KKOMI_ALIVE] ≠거짓 | 4 |
| `kkomi_dead` |  | [KKOMI_ALIVE] =거짓 | 3 |
| `gate_daram_unlisted` | Event 01: lost gate proof, Daram entered as '외 한 명' (owner plan A, 2026-10-21). | [gate_daram_unlisted] =참 | 10 |
| `gate_daram_listed` |  | [gate_daram_unlisted] ≠참 | 4 |
| `room13_checked_d1` | Review 0.20.1 #1: the gate's "entry allowed" lines only on the last wrong answer. 0.20.6 (play review P02): after the room is looked over, Granny stops sending  | 자료 E06 보유 | 1 |
| `room13_unchecked_d1` |  | 아님 자료 E06 보유 | 1 |
| `d06_bowl_together` | 0.20.7 | [choice:MS14_D06_S01]=="together" | 1 |
| `gate_last_try` |  | ([tries:gate] 또는 0)+1>=r13_nw_tries_max("gate") | 2 |
| `gate_retry` |  | ([tries:gate] 또는 0)+1<r13_nw_tries_max("gate") | 2 |
| `gate_partial_retry` | 0.20.5 (Codex C03): a wrong answer that held only some of the gate records says so, without naming the missing ones; a set with none of them gets the plain refu | ([tries:gate] 또는 0)+1<r13_nw_tries_max("gate") 그리고 "V111:E03" in (getattr(store,"v111_last_presented",None) 또는 []) 그리고 "V111:E02" 아님 in (getattr(store,"v111_last_presented",None) 또는 []) | 1 |
| `gate_both_given` |  | {"V111:E02","V111:E03"}<=set(getattr(store,"v111_last_presented",None) 또는 []) | 1 |
| `gate_has_original` |  | 자료 E03 보유 | 1 |
| `prep12_others_missing` | Review 0.20.1 4-5: the day-12 prep line names only what is really ready. | 아님 all(r13_v111_value(k) for k in ("warm_seat_ready","carrier_arrived","warm_support_arrived")) | 1 |
| `prep12_seat_only` | 0.20.6 (owner review): one of the two ready -> name only what is still missing. | bool([warm_seat_ready]) 그리고 아님 [carrier_arrived] | 1 |
| `prep12_carrier_only` |  | bool([carrier_arrived]) 그리고 아님 [warm_seat_ready] | 1 |
| `prep12_seat_and_carrier` |  | bool([warm_seat_ready]) 그리고 bool([carrier_arrived]) | 1 |
| `lamp_win` | Event 03: the day-3 lamp meeting (win / partial / lose). | [meeting:lamp]=="win" | 4 |
| `lamp_partial` |  | [meeting:lamp]=="partial" | 6 |
| `lamp_lose` |  | [meeting:lamp]=="lose" | 16 |
| `lamp_not_win` |  | [meeting:lamp] in ("partial","lose") | 2 |
| `lamp_stage_sale` | Audit d01-05 #1/#6: which stage of the lamp meeting was reached (sale -> knife -> latch -> stone). | [repair_opening_separated] =참 | 2 |
| `lamp_stage_latch` |  | 자료 E33 보유 | 2 |
| `lamp_stage_stone` |  | [outer_latch_claim_refuted] =참 | 2 |
| `lamp_partial_sale` |  | [meeting:lamp]=="partial" 그리고 아님 자료 E33 보유 | 2 |
| `lamp_partial_latch` |  | [meeting:lamp]=="partial" 그리고 자료 E33 보유 그리고 [outer_latch_claim_refuted] ≠참 | 2 |
| `lamp_partial_stone` |  | [meeting:lamp]=="partial" 그리고 [outer_latch_claim_refuted] =참 | 2 |
| `lamp_repair_half_owl` | 2026-10-29 외부 검토 0.20.86 B: 첫 쟁점(톡 다음에 등이 열린 때)에서 맞는 자료만 일부 낸 오답이면, 너울의 되묻기가 맞게 짚은 쪽은 인정하고 빈 칸만 묻는다. 틀린 자료가 섞였거나 회의가 이미 끝났으면(lose) 기본 되묻기를 쓴다 — 끝난 판에서 「알겠소」라고 해 | [meeting:lamp] 없음 그리고 [repair_opening_separated] ≠참 그리고 "V111:E13" in set(getattr(store,"v111_last_presented",None) 또는 []) 그리고 "V111:E11" 아님 in set(getattr(store,"v111_last_presented",None) 또는 []) 그리고 | 1 |
| `lamp_repair_half_check` |  | [meeting:lamp] 없음 그리고 [repair_opening_separated] ≠참 그리고 "V111:E11" in set(getattr(store,"v111_last_presented",None) 또는 []) 그리고 set(getattr(store,"v111_last_presented",None) 또는 [])<={"V111:E10","V111:E | 1 |
| `gate_post_lose` | Event 04: the day-5 gate-post meeting. | [meeting:gate_post]=="lose" | 16 |
| `gate_post_half` |  | ([tries:gate_post] 또는 0)>0 그리고 [meeting:gate_post] 없음 | 1 |
| `gate_won_with_e01` | Proof scope (owner 2026-10-22): a won proof that carried an allowed extra record (R13_PROOF_EXTRAS / R13_PROOF_ALTERNATES in room13_v111_newworld_rules.rpy). | "V111:E01" in ([proof_given:함께 들어갈 근거를 고른다] 또는 []) | 2 |
| `repair_won_with_e10` |  | "V111:E10" in ([proof_given:수리와 반출을 가릴 자료를 낸다] 또는 []) | 1 |
| `gate_post_won_with_e21` |  | "V111:E21" in ([proof_given:밤이 혐의의 근거를 확인한다] 또는 []) | 1 |
| `gate_post_won_with_sketch` | 0.20.18 연쇄 P1: 살아 있는 피코의 4일 밤 그림을 회의에 냈는가. _only 는 겉옷·귀가 진술 없이 그림으로 이긴 경우. | "V111:NW_PIKO_SKETCH4" in ([proof_given:밤이 혐의의 근거를 확인한다] 또는 []) | 1 |
| `gate_post_won_with_sketch_only` |  | "V111:NW_PIKO_SKETCH4" in ([proof_given:밤이 혐의의 근거를 확인한다] 또는 []) 그리고 아님 {"V111:E23","V111:E24"}&set([proof_given:밤이 혐의의 근거를 확인한다] 또는 []) | 2 |
| `piko_sacks2` | 0.20.18 (열쇠표 K1): 2일 오후 피코의 자리를 위해 실제로 한 일. | [piko_sacks2] =참 | 1 |
| `kkomi_seat6` | 0.20.18 (열쇠표 K2): 6일 선생님께 아이들 자리를 받아 두었는가. | [kkomi_seat6] =참 | 1 |
| `fire_evacuated` | 2026-10-23 연결오류: 아이들을 먼저 옮긴 판에서는 도토를 이미 만났다(P01·빈 창고 불). 소개를 되풀이하지 않는다. | [FIRE_EVACUATED] =참 | 5 |
| `fire_not_evacuated` | 2026-10-24 지시서 02 감정선: 불을 끄다 보리가 손을 덴 판(bori_burned6), 7일 도담 숟가락·12일 다람이 숟가락을 돌려주는가, 10일 꼬미와 도토리를 나눴는가. | [FIRE_EVACUATED] ≠참 | 2 |
| `dodam_spoon_lent` |  | [dodam_spoon7] =참 그리고 daram 이(가) 그 자리에 있음 | 3 |
| `dodam_spoon12` |  | [dodam_spoon12] =참 | 2 |
| `lower_elder_received12` |  | [lower_road_handover]==3 그리고 [alive:v111_lowerroad_elder] ≠거짓 | 1 |
| `owl_listed_cart13` |  | [OWL_ALIVE] ≠거짓 그리고 [listed:resident_owlgp] =참 그리고 아님 [departed:resident_owlgp] | 3 |
| `kkomi_can_carried6` |  | bool([kkomi_can_seen6] 그리고 [acorn_recovered]) | 5 |
| `kkomi_can_left6` |  | 아님 ([kkomi_can_seen6] 그리고 [acorn_recovered]) | 2 |
| `kkomi_acorn_shared` |  | [kkomi_acorn10] =참 그리고 daram 이(가) 그 자리에 있음 | 1 |
| `bami_cold4` | 0.20.18 (CRUEL_CHOICES.md C1): 13일 공개 때 엄마와 다람이 광장에 있는가. 0.20.18 (CRUEL_CHOICES.md C3 A안): 3일 실룩을 풀어 준 판, 5번 등이 비어 밤이가 처마에서 내려왔다. | [bami_cold4] =참 | 5 |
| `bami_warm4` |  | [bami_cold4] ≠참 | 1 |
| `riot_momo13` | 0.20.19 (CRUEL_CHOICES.md D1·D3): 폭동 때 수레에 남아 있던 모모, 12일 다람이 말할 수 있는가. | [riot_momo13] =참 | 2 |
| `daram_ready` |  | daram 이(가) 그 자리에 있음 | 70 |
| `crowd_block_failed13` | 0.20.20 (aftermath 시안): 막아섰다가 실패한 판, 수레로 떠난 사람이 있는 판. | [crowd_intervention]=="failed" 그리고 [crowd_blocked_by_dad] =참 | 1 |
| `departed_any` |  | any(p!="daram" for p in ([departed_names] 또는 [])) | 1 |
| `family_on_square` |  | [family_location]=="square" 그리고 daram 이(가) 그 자리에 있음 | 3 |
| `hyp1_won_with_e28` | 2026-10-24 자료 재사용(EVIDENCE_CLUTTER_PLAN.md 2부): 정답 위에 덧붙인 자료를 상대가 한 줄로 짚는다. | "V111:E28" in ([proof_given:초롱과 피코의 하루를 대조한다] 또는 []) | 1 |
| `hyp3_won_with_e14` |  | "V111:E14" in ([proof_given:요즘 돌이 어디서 오는지 대조한다] 또는 []) | 1 |
| `writing_won_with_e27` |  | "V111:E27" in ([proof_given:반송·필사본·초대 발송을 대조한다] 또는 []) | 2 |
| `writing_won_with_e09` |  | "V111:E09" in ([proof_given:반송·필사본·초대 발송을 대조한다] 또는 []) | 3 |
| `blanket_won_with_e35` |  | "V111:E35" in ([proof_given:아내가 봤다는 담요의 시점을 확인한다] 또는 []) | 1 |
| `badook_won_with_e29` |  | "V111:E29" in ([proof_given:촌장이 어젯밤 있던 곳을 확인한다] 또는 []) | 2 |
| `piko_ledger_with_e34` |  | "V111:E34" in ([proof_given:장부의 두 배를 실룩에게 보인다] 또는 []) | 1 |
| `altar4_won_with_ledger` |  | "V111:NW_NEOUL_LEDGER" in ([proof_given:맨 처음 이름을 짚는다] 또는 []) | 1 |
| `altar4_won_with_rations` |  | "V111:NW_OLD_RATIONS" in ([proof_given:맨 처음 이름을 짚는다] 또는 []) 그리고 "V111:NW_NEOUL_LEDGER" 아님 in ([proof_given:맨 처음 이름을 짚는다] 또는 []) | 1 |
| `altar4_won_with_burnt_page` |  | "V111:NW_BURNT_PAGE" in ([proof_given:맨 처음 이름을 짚는다] 또는 []) | 1 |
| `hyp1_won_without_e08` |  | bool([proof_given:초롱과 피코의 하루를 대조한다]) 그리고 "V111:E08" 아님 in [proof_given:초롱과 피코의 하루를 대조한다] | 1 |
| `fire_win` | Event 05: the day-7 fire meeting. | [meeting:fire]=="win" | 4 |
| `fire_partial` |  | [meeting:fire]=="partial" | 4 |
| `fire_lose` |  | [meeting:fire]=="lose" | 11 |
| `prevention_b` | Events 06-07: the day-7 room 13 night and the day-10 meetings. 2026-10-25 부엉이 예방 1단계(OWL_PREVENTION_DESIGN.md 9장): 7일 A/B/C 메뉴를 걷고, 7일 낮 13호 난로의 돌(stone) 또는 도토의 | [prevention] in ("B","promise","repair") | 4 |
| `prevention_stone` |  | [prevention]=="stone" | 7 |
| `owl_fell7` |  | [OWL_ALIVE] ≠거짓 그리고 [prevention]!="stone" | 3 |
| `stove_untouched7` |  | [stove13_7] 없음 | 2 |
| `stove_blue7` |  | [stove13_7] 아님 in ("ration","empty") | 4 |
| `stove_fixed7` |  | [stove13_7] in ("ration","empty") | 2 |
| `stove_ration7` |  | [stove13_7]=="ration" | 1 |
| `stove_emptied7` |  | [stove13_7]=="empty" | 2 |
| `snack_bagged5` | 결정 11(2026-10-25): 5일 밤 접시의 과자 봉지를 다람의 가방에 넣은 판. 아니면 과자는 첫날처럼 외투 안에 있다. | [snack_bagged5] =참 | 2 |
| `snack_unbagged5` |  | [snack_bagged5] ≠참 | 7 |
| `room13_win` |  | [meeting:room13]=="win" | 7 |
| `room13_lose` |  | [meeting:room13]=="lose" | 28 |
| `room13_not_win` |  | [meeting:room13] in ("partial","lose") | 15 |
| `room13_partial_unknown` |  | [meeting:room13]=="partial" 그리고 [room13_partial_kind]=="unknown" | 12 |
| `room13_partial_accident` |  | [meeting:room13]=="partial" 그리고 [room13_partial_kind]=="accident" | 9 |
| `records_partial` |  | [meeting:records]=="partial" | 2 |
| `records_lose` |  | [meeting:records]=="lose" | 10 |
| `records_lose_prev_b` |  | [meeting:records]=="lose" 그리고 [prevention]!="stone" | 1 |
| `records_partial_prev_b` |  | [meeting:records]=="partial" 그리고 [prevention]!="stone" | 1 |
| `records_lose_prev_stone` | 돌을 바꿔 부엉이가 무너지지 않은 판: 할머니가 너울에게 「같은 말을 두 번 묻는다」고 일러 명단 얘기가 나온다. | [meeting:records]=="lose" 그리고 [prevention]=="stone" | 2 |
| `records_partial_prev_stone` |  | [meeting:records]=="partial" 그리고 [prevention]=="stone" | 1 |
| `records_lose_fell7` |  | [meeting:records]=="lose" 그리고 [prevention]!="stone" | 1 |
| `guldol_ready` | Event 08: the day-11 facility and the hypothesis meeting. | resident_guldol 이(가) 그 자리에 있음 | 4 |
| `karo_ready` | 0.20.9 | karo 이(가) 그 자리에 있음 | 6 |
| `karo_absent` | 2026-10-23 연결오류: 까로가 없는 숲의 대체 지문 | 아님 karo 이(가) 그 자리에 있음 | 2 |
| `route12_late` | 0.20.10 D12-03 학교 밖에 다녀온 경로 | [route12]=="late_exposure" | 6 |
| `route12_stayed` |  | [route12]!="late_exposure" | 1 |
| `route12_premeal` | 2026-10-27 외부 검토 B03: 먹기 전에 막은 판의 수프 회의. 조기 예방 판(early_prevented)은 회의가 없다. | [route12]=="premeal_stopped" | 3 |
| `letter_tail_unobserved` | 2026-10-27 D08: 두 편지 관찰에서 플레이어가 끝부분을 직접 짚었으면 비교 뒤 같은 세 줄을 되풀이하지 않는다. | 아님 [letter_tail_observed] | 3 |
| `tosil_inside` | 0.20.9 엔딩 검토 9 | [tosil_listen]=="inside" | 2 |
| `tosil_outside` |  | [tosil_listen]=="outside" | 2 |
| `tok_round_asked` | 0.20.9 D23-04 먼저 물어본 경우 | bool([followup_read:NW_RX_F007]) | 1 |
| `heard_inn_order1` | 0.20.9 1일 문간 지시를 들은 경로 | [heard_inn_order1] =참 | 2 |
| `guldol_absent` |  | 아님 resident_guldol 이(가) 그 자리에 있음 | 2 |
| `town_won_before11` | 2026-10-24 자가 검수 12: 11일 판돌이 아빠 말을 들어 주는 까닭. 앞 회의(3·5·7·10일) 중 하나라도 이겼는가. | any([meeting:m]=="win" for m in ("lamp","gate_post","fire","room13","records")) | 0 |
| `town_won_none_before11` |  | 아님 any([meeting:m]=="win" for m in ("lamp","gate_post","fire","room13","records")) | 0 |
| `hyp_win` |  | [meeting:hypothesis]=="win" | 6 |
| `hyp_partial` |  | [meeting:hypothesis]=="partial" | 5 |
| `hyp_lose` |  | [meeting:hypothesis]=="lose" | 4 |
| `hyp_not_lose` |  | [meeting:hypothesis] in ("win","partial") | 8 |
| `hyp_lost1` |  | [hyp_issue:1]=="lost" | 1 |
| `hyp_lost2` |  | [hyp_issue:2]=="lost" | 1 |
| `hyp_lost3` |  | [hyp_issue:3]=="lost" | 1 |
| `hyp_lost4` |  | [hyp_issue:4]=="lost" | 1 |
| `soup_lose_stolen` | Event 09: the day-12 soup. | [meeting:soup]=="lose" 그리고 [soup_lose_kind]=="stolen" | 3 |
| `soup_lose_nabi` |  | [meeting:soup]=="lose" 그리고 [soup_lose_kind]=="nabi" | 3 |
| `daram_deal_freed` | Event 10: the day-13 cart. | [daram_deal_freed] =참 | 2 |
| `hyp_retry` | Audit d11-14 #2: a hypothesis wrong answer that may be retried holds judgment. | [meeting:hypothesis] 없음 그리고 ([tries:hypothesis] 또는 0)<r13_nw_tries_max("hypothesis") | 5 |
| `hyp_final` |  | 아님 ([meeting:hypothesis] 없음 그리고 ([tries:hypothesis] 또는 0)<r13_nw_tries_max("hypothesis")) | 5 |
| `hyp_lose_some_won` | Audit d11-14 #3: a lost hypothesis meeting after some issues were won. | [meeting:hypothesis]=="lose" 그리고 any(r13_v111_value("hyp_issue:%d"%i)=="won" for i in (1,2,3,4)) | 1 |
| `hyp_lose_none_won` |  | 아님 ([meeting:hypothesis]=="lose" 그리고 any(r13_v111_value("hyp_issue:%d"%i)=="won" for i in (1,2,3,4))) | 1 |
| `soup_lose_nabi_murder` | Audit d11-14 #8: Nabi changed her room 13 testimony only on the murder route. | [meeting:soup]=="lose" 그리고 [soup_lose_kind]=="nabi" 그리고 [route7]=="murder" | 1 |
| `soup_lose_nabi_prevented` |  | [meeting:soup]=="lose" 그리고 [soup_lose_kind]=="nabi" 그리고 [route7]!="murder" | 1 |
| `wood12_missing` | Audit d11-14 #12: firewood is really at the school (carrier received or box picked up). | 아님 ([warm_support_arrived] 또는 [heat_box_received]) | 1 |
| `blanket_undecided` | Audit d11-14 #10, #13, #6, #7. | [meeting:blanket] 없음 | 2 |
| `blanket_partial` |  | [meeting:blanket]=="partial" | 1 |
| `siluk_not_listed` |  | [listed:resident_siluk] ≠참 | 1 |
| `daram_listed_unhanded` |  | [listed:daram] =참 그리고 아님 [handed:daram] | 1 |
| `has_ledger` | Event 11: the altar, Bomi, and the endings. | 자료 NW_NEOUL_LEDGER 보유 | 4 |
| `no_ledger` |  | 아님 자료 NW_NEOUL_LEDGER 보유 | 3 |
| `has_burnt_page` |  | 자료 NW_BURNT_PAGE 보유 | 1 |
| `altar_win` |  | [meeting:altar]=="win" | 5 |
| `altar_partial` |  | [meeting:altar]=="partial" | 2 |
| `altar_lose` |  | [meeting:altar]=="lose" | 1 |
| `medicine_locked` |  | [medicine_locked] =참 | 2 |
| `medicine_unchecked` |  | 아님 [medicine_locked] | 2 |
| `daram_not_deal_freed` |  | [daram_deal_freed] ≠참 | 1 |
| `warm_support_pending` |  | 아님 [warm_support_arrived] | 2 |
| `warm_support_ready` |  | [warm_support_arrived] =참 | 4 |
| `family_priority` |  | [outcome13]=="family_priority" | 1 |
| `reader_nabi` |  | 아님 ([departed:nabi] 또는 아님 nabi 생존) | 2 |
| `reader_tosil` |  | bool([departed:nabi] 또는 아님 nabi 생존) | 2 |
| `granny_held_win` |  | [OWL_ALIVE] =거짓 그리고 [meeting:room13]=="win" | 8 |
| `granny_room13_partial` |  | [OWL_ALIVE] =거짓 그리고 [meeting:room13]=="partial" | 1 |
| `granny_room13_lose` |  | [OWL_ALIVE] =거짓 그리고 [meeting:room13]=="lose" | 1 |
| `tok_freed3` | 2026-10-24 동기 줄 4차(문구시안.md): 3일 회의에서 톡이 풀려난 판(이김·부분). 짐은 listed:resident_tok 이 받는다. | [meeting:lamp] in ("win","partial") 그리고 [listed:resident_tok] ≠참 | 7 |
| `daram_watching13` | 13일 수레 앞: 다람이 곁에 있고, 방금까지 수레에 묶여 있던 판(listed:daram)이 아닐 때만 빈 칸을 묻는다. | daram 이(가) 그 자리에 있음 그리고 [listed:daram] ≠참 | 6 |
| `wild_omen12` | 14일 아침: 엄마와 다람이 함께 학교에 있을 때만 셋이 말한다. 2026-10-24 불타는 밤: 11일 가설 회의를 진 판의 12~13일 전조와 14일 밤. | [meeting:hypothesis]=="lose" 그리고 resident_teacher 이(가) 그 자리에 있음 | 6 |
| `wild_omen13_karo` |  | [meeting:hypothesis]=="lose" 그리고 karo 이(가) 그 자리에 있음 | 8 |
| `wild_omen13_gate_kept` | 11일 1번 쟁점을 이긴 판은 돌목이 「초소 불은 오늘 끄겠소」(NW_H1_W_04)라고 했다가 다시 켰다. | [meeting:hypothesis]=="lose" 그리고 [hyp_issue:1]!="won" 그리고 guard 이(가) 그 자리에 있음 | 2 |
| `wild_omen13_gate_relit` |  | [meeting:hypothesis]=="lose" 그리고 [hyp_issue:1]=="won" 그리고 guard 이(가) 그 자리에 있음 | 2 |
| `wild_daram_fever` |  | bool([daram_fever12]) | 2 |
| `wild_daram_well` |  | 아님 [daram_fever12] | 3 |
| `wild_three` |  | [wild_family]=="three" | 6 |
| `wild_no_mom` |  | [wild_family]=="no_mom" | 9 |
| `wild_alone` |  | [wild_family]=="alone" | 8 |
| `wild_omen13_gate` |  | [meeting:hypothesis]=="lose" 그리고 guard 이(가) 그 자리에 있음 그리고 daram 이(가) 그 자리에 있음 | 5 |
| `mom_daram_ready14` |  | mom 이(가) 그 자리에 있음 그리고 daram 이(가) 그 자리에 있음 | 5 |
| `lamp_last_try` | 2026-10-24 행동 검수(action-review-20261024/적용보고.md). 이미 있는 값만 읽는다. 대안 1: 회의에서 틀린 뒤 기회가 한 번만 남았을 때 결정하는 사람이 참을성이 바닥났음을 말한다. | [meeting:lamp] 없음 그리고 r13_nw_tries_left("lamp")==1 | 2 |
| `gate_post_last_try` |  | [meeting:gate_post] 없음 그리고 r13_nw_tries_left("gate_post")==1 | 1 |
| `lamp_not_lose` | 4-1: 3일 회의를 진 판은 보호시설 설명을 이미 들었다. 5-1: 밤이를 풀어 준 판. | [meeting:lamp]!="lose" | 2 |
| `gate_post_win` |  | [meeting:gate_post]=="win" | 3 |
| `gate_post_half_height` | 2026-10-29 외부 검토 2 N3: 5일 회의에서 맞는 자료만 일부 낸 오답(틀린 자료 없음, 회의 진행 중)이면 너울의 되묻기가 짚은 고리는 인정하고 빈 고리만 묻는다. 3일 lamp_repair_half_* 와 같은 방식. 정답 묶음은 그대로다. | r13_gp_half() 그리고 "V111:E22" in r13_gp_given() 그리고 "V111:E20" 아님 in r13_gp_given() 그리고 ({"V111:E23","V111:E24"}<=r13_gp_given() 또는 "V111:NW_PIKO_SKETCH4" in r13_gp_given()) | 1 |
| `gate_post_half_wearer` |  | r13_gp_half() 그리고 {"V111:E22","V111:E23"}<=r13_gp_given() 그리고 아님 {"V111:E24","V111:NW_PIKO_SKETCH4"}&r13_gp_given() | 1 |
| `gate_post_half_match` |  | r13_gp_half() 그리고 {"V111:E22","V111:E24"}<=r13_gp_given() 그리고 아님 {"V111:E23","V111:NW_PIKO_SKETCH4"}&r13_gp_given() | 1 |
| `gate_post_half_cloth` |  | r13_gp_half() 그리고 "V111:E22" in r13_gp_given() 그리고 아님 {"V111:E23","V111:E24","V111:NW_PIKO_SKETCH4"}&r13_gp_given() | 1 |
| `gate_post_half_fence` |  | r13_gp_half() 그리고 "V111:E22" 아님 in r13_gp_given() 그리고 bool({"V111:E23","V111:E24","V111:NW_PIKO_SKETCH4"}&r13_gp_given()) | 1 |
| `karo_heard_iron5` | 소유자 결정 4(탈출 축): 3일에 톡에게 「쇠 토막을 구해 와야 해요」를 들은 판에서, 5일 식당에 까로가 있을 때. | [meeting:lamp] in ("win","partial") 그리고 [listed:resident_tok] ≠참 그리고 karo 이(가) 그 자리에 있음 | 4 |
| `school_supply_pending` | 11-11: 학교 물자를 아직 넘기지 않아 「학교 물자 인계를 먼저」가 메뉴에 남는 판. | 아님 [school_supply_handed] | 3 |
| `guard_ready` | 12-1·13-3: 돌목이 그 자리에 있을 때(원래 줄도 같은 확인을 한다). | guard 이(가) 그 자리에 있음 | 6 |
| `daram_not_watching13` | 13-4: 다람이 수레를 보지 못하는 판은 엄마가 같은 말을 한다. | 아님 (daram 이(가) 그 자리에 있음 그리고 [listed:daram] ≠참) | 1 |
| `karo_guard_ready13` | 13-10: 까로와 돌목이 둘 다 곁에 있으면 셋이 주고받고, 아니면 아빠의 속말 한 줄. | karo 이(가) 그 자리에 있음 그리고 guard 이(가) 그 자리에 있음 | 3 |
| `karo_guard_not_ready13` |  | 아님 (karo 이(가) 그 자리에 있음 그리고 guard 이(가) 그 자리에 있음) | 1 |
| `buri_site_ask14` | 14-5: 부리가 공구를 챙긴 판에서 촌장 동행을 아직 묻기 전. | bool([buri_device_consent]) 그리고 아님 [mayor_site_decided] 그리고 buri 생존 | 2 |
| `morning_with_loss14` | 대안 9: 마을의 아침인데 이 아침을 함께 못 맞은 사람이 있는 판(진엔딩을 막는 까닭 하나). | [ending14]=="morning" 그리고 r13_nw_loss_count()>0 그리고 mom 이(가) 그 자리에 있음 그리고 daram 이(가) 그 자리에 있음 | 2 |
| `laundry_overheard5` | 2026-10-24 대승리(GRAND_WIN_DESIGN.md 1·2장, 결정 4·7): 5일 빨래터에서 엿들은 판, 7일 막내에게서 숨긴 자리를 들은 판. | [grand_laundry_seen5] =참 | 4 |
| `ticket_spot_kid7` |  | [grand_ticket_spot_kid] =참 그리고 [grand_laundry_seen5] ≠참 | 1 |
| `fire_grand` | 7일 불 회의를 배급표로 이긴 판(대승리)과 보통으로 이긴 판. | [grand:fire] =참 | 4 |
| `fire_win_plain` |  | [meeting:fire]=="win" 그리고 [grand:fire] ≠참 | 1 |
| `karo_ready11` |  | karo 이(가) 그 자리에 있음 | 2 |
| `grand_soup` | 12일 수프 회의를 돌아온 그릇으로 이긴 판. 돌목이 그 자리에 있으면 그가 칸을 무효로 적는다. | [grand:soup] =참 | 3 |
| `grand_soup_guard` |  | [grand:soup] =참 그리고 guard 이(가) 그 자리에 있음 | 4 |
| `grand_soup_noguard` |  | [grand:soup] =참 그리고 아님 guard 이(가) 그 자리에 있음 | 1 |
| `list_voided` | 이송 예정 칸이 무효가 된 판(수프 대승리, 또는 국을 미리 막은 판에서 돌목에게 그릇을 보인 판). | [transfer_list_voided] =참 | 2 |
| `list_not_voided` |  | [transfer_list_voided] ≠참 | 2 |
| `daram_listed_voided13` |  | [listed:daram] =참 그리고 [transfer_list_voided] =참 그리고 guard 이(가) 그 자리에 있음 | 1 |
| `daram_listed_unvoided13` |  | [listed:daram] =참 그리고 아님 ([transfer_list_voided] =참 그리고 guard 이(가) 그 자리에 있음) | 2 |
| `daram_departs13` |  | [listed:daram] =참 그리고 [transfer_list_voided] ≠참 | 3 |
| `mom03_piko_alive` | 2026-10-27 엄마 줄기 짚기(외부 리뷰 1순위): 사건이 끝난 저녁, 부녀가 엄마에 대해 안 것과 모르는 것을 주고받는다. 다람이 곁에 있을 때만. 갈래는 그날 장면을 가르는 값과 같게 읽는다(3일 r13_v111_memorial_route, 7일 KKOMI_ALIVE). 피코· | daram 이(가) 그 자리에 있음 그리고 [piko_alive] =참 | 4 |
| `mom03_piko_dead` |  | daram 이(가) 그 자리에 있음 그리고 [piko_alive] ≠참 | 4 |
| `mom07_kkomi_alive` |  | daram 이(가) 그 자리에 있음 그리고 bool([KKOMI_ALIVE]) | 1 |
| `nw_rebut_pending` | 2026-10-29 논쟁 점검 P02 (소유자 승인 방향): 맞는 자료를 일부만 낸 오답이면 상대가 짚은 고리는 인정하고 빈 고리를 자료 이름 없이 묻는다. 3일 lamp_repair_half_*·5일 gate_post_half_* 와 같은 방식을 나머지 회의에 넓힌 것이다. 0.19. | bool(getattr(store,"r13_nw_rebut_pending",None)) | 14 |
| `nw_no_rebut` |  | 아님 getattr(store,"r13_nw_rebut_pending",None) | 4 |
| `fire1_no_fire_record` | 7일 불 1번(P01): 누비의 「천」 반박은 불탄 자리 기록(천이 들어 있다)을 냈을 때만 맞는다. | r13_nw_wrong_issue()=="불이 시작된 곳과 진술을 대조한다" 그리고 아님 이번 제출에 E06_FIRE 중 하나 | 2 |
| `half_fire_who7` | 7일 불 2번: 불이 붙은 자리 · 보리가 그 밤에 한 일 · 불을 낸 손. | 이번 제출에 E06_FIRE 중 하나 그리고 이번 제출에 E06_EMPTY,E06_RESCUE 중 하나 그리고 아님 이번 제출에 E07_NUBI,NW_NUBI_TICKET 중 하나 | 1 |
| `half_fire_bori7` |  | 이번 제출에 E06_FIRE 중 하나 그리고 이번 제출에 E07_NUBI,NW_NUBI_TICKET 중 하나 그리고 아님 이번 제출에 E06_EMPTY,E06_RESCUE 중 하나 | 1 |
| `half_fire_start7` |  | 아님 이번 제출에 E06_FIRE 중 하나 그리고 이번 제출에 E06_EMPTY,E06_RESCUE 중 하나 그리고 이번 제출에 E07_NUBI,NW_NUBI_TICKET 중 하나 | 1 |
| `half_fire_only_start7` |  | 이번 제출에 E06_FIRE 중 하나 | 1 |
| `half_fire_only_bori7` |  | 이번 제출에 E06_EMPTY,E06_RESCUE 중 하나 | 1 |
| `half_fire_only_who7` |  | 이번 제출에 E07_NUBI,NW_NUBI_TICKET 중 하나 | 1 |
| `half_r13_account10` | 10일 13호 1~5번. | 이번 제출에 E08_CHILD_ACCOUNT 중 하나 그리고 아님 이번 제출에 E08_TOOL 중 하나 | 1 |
| `half_r13_tool10` |  | 이번 제출에 E08_TOOL 중 하나 그리고 아님 이번 제출에 E08_CHILD_ACCOUNT 중 하나 | 1 |
| `half_r13_walked10` |  | 이번 제출에 E09_PASSAGE 중 하나 그리고 아님 이번 제출에 E08_ROOM 중 하나 | 1 |
| `half_r13_room10` |  | 이번 제출에 E08_ROOM 중 하나 그리고 아님 이번 제출에 E09_PASSAGE 중 하나 | 1 |
| `half_r13_record10` |  | 이번 제출에 E09_PIN_OWNER 중 하나 그리고 아님 이번 제출에 E08_WOUND_WIRE,E08_CONTACT_ASSEMBLY 중 하나 | 1 |
| `half_r13_wire10` |  | 이번 제출에 E08_WOUND_WIRE 중 하나 그리고 아님 이번 제출에 E09_PIN_OWNER 중 하나 | 1 |
| `half_r13_hook10` |  | 이번 제출에 E08_CONTACT_ASSEMBLY 중 하나 그리고 아님 이번 제출에 E09_PIN_OWNER 중 하나 | 1 |
| `half_r13_first10` |  | 이번 제출에 E09_PIN_TIME 중 하나 그리고 아님 이번 제출에 E09_PIN_HANDOVER_TIME 중 하나 | 1 |
| `half_r13_stair10` |  | 이번 제출에 E09_PIN_HANDOVER_TIME 중 하나 그리고 아님 이번 제출에 E09_PIN_TIME 중 하나 | 1 |
| `half_r13_c_object10` |  | 아님 이번 제출에 E08_CONTACT_ASSEMBLY,E08_WOUND_WIRE 중 하나 | 1 |
| `half_r13_c_child10` |  | 아님 (이번 제출에 E08_CHILD_POSITION 중 하나 그리고 이번 제출에 E08_ROOM_REACH 중 하나) | 1 |
| `half_r13_c_hook10` |  | 아님 이번 제출에 E08_CONTACT_ASSEMBLY 중 하나 | 1 |
| `half_r13_c_wound10` |  | 아님 이번 제출에 E08_WOUND_WIRE 중 하나 | 1 |
| `half_r13_c_scarf10` |  | 아님 이번 제출에 E09_SCARF 중 하나 | 1 |
| `half_rec_contact10` | 10일 기록 1·2번. | 이번 제출에 E06_CONTACT 중 하나 그리고 아님 이번 제출에 E09_MAIL 중 하나 | 1 |
| `half_rec_mail10` |  | 이번 제출에 E09_MAIL 중 하나 그리고 아님 이번 제출에 E06_CONTACT 중 하나 | 1 |
| `half_rec_invite10` |  | 아님 이번 제출에 E01 중 하나 | 1 |
| `half_rec_origin10` |  | 아님 이번 제출에 E07,E27 중 하나 | 1 |
| `half_rec_order10` |  | 아님 이번 제출에 E09_MAIL 중 하나 | 1 |
| `half_hyp1_night11` | 11일 가설 1·3·4번(2·5번은 자료 한 장이라 일부 정답이 없다). | 이번 제출에 E11,NW_LA_CHECK 중 하나 그리고 아님 이번 제출에 NW_PIKO_TREMOR 중 하나 | 1 |
| `half_hyp1_day11` |  | 이번 제출에 NW_PIKO_TREMOR 중 하나 그리고 아님 이번 제출에 E11,NW_LA_CHECK 중 하나 | 1 |
| `half_hyp1_lamp11` |  | 이번 제출에 E08 중 하나 그리고 아님 이번 제출에 E11,NW_LA_CHECK,NW_PIKO_TREMOR 중 하나 | 1 |
| `half_hyp3_price11` |  | 이번 제출에 NW_INNER_PRICE 중 하나 그리고 아님 이번 제출에 NW_MUSOE_DEEP 중 하나 | 1 |
| `half_hyp3_deep11` |  | 이번 제출에 NW_MUSOE_DEEP 중 하나 그리고 아님 이번 제출에 NW_INNER_PRICE 중 하나 | 1 |
| `half_hyp4_nostone11` |  | 이번 제출에 NW_KKOMI_NOSTONE 중 하나 그리고 아님 이번 제출에 NW_SICK_BEDS 중 하나 | 1 |
| `half_hyp4_beds11` |  | 이번 제출에 NW_SICK_BEDS 중 하나 그리고 아님 이번 제출에 NW_KKOMI_NOSTONE 중 하나 | 1 |
| `half_soup_fragment12` | 12일 수프 1~3번. | 이번 제출에 E12_FRAGMENT 중 하나 그리고 아님 이번 제출에 E12_SEAL 중 하나 | 1 |
| `half_soup_seal12` |  | 이번 제출에 E12_SEAL 중 하나 그리고 아님 이번 제출에 E12_FRAGMENT 중 하나 | 1 |
| `half_soup_hand12` |  | 아님 이번 제출에 E12_HANDLING 중 하나 | 1 |
| `half_soup_bottle12` |  | 아님 (이번 제출에 E12_FRAGMENT 중 하나 그리고 이번 제출에 E12_SEAL 중 하나) | 1 |
| `half_list_returned12` |  | 이번 제출에 NW_RETURNED_BOWL 중 하나 그리고 아님 이번 제출에 NW_WHITE_BOWLS,NW_TRANSFER_LIST 중 하나 | 1 |
| `half_list_nobowls12` |  | 아님 이번 제출에 NW_WHITE_BOWLS 중 하나 | 1 |
| `half_list_bowls12` |  | 이번 제출에 NW_WHITE_BOWLS 중 하나 | 1 |
| `half_altar1_wood14` | 14일 제단 1·2·4번(3번은 자료 한 장). | 이번 제출에 E14_SUPPLY 중 하나 그리고 아님 이번 제출에 NW_KKOMI_NOSTONE,NW_SICK_BEDS 중 하나 | 1 |
| `half_altar1_kids14` |  | 아님 이번 제출에 E14_SUPPLY 중 하나 그리고 이번 제출에 NW_KKOMI_NOSTONE,NW_SICK_BEDS 중 하나 | 1 |
| `half_altar1_mixed14` |  | 이번 제출에 E14_SUPPLY 중 하나 그리고 이번 제출에 NW_KKOMI_NOSTONE,NW_SICK_BEDS 중 하나 | 1 |
| `half_altar2_front14` |  | 이번 제출에 NW_TABLET_A 중 하나 그리고 아님 이번 제출에 NW_TABLET_B 중 하나 | 1 |
| `half_altar2_back14` |  | 이번 제출에 NW_TABLET_B 중 하나 그리고 아님 이번 제출에 NW_TABLET_A 중 하나 | 1 |
| `half_altar4_names14` |  | 이번 제출에 NW_NAMES 중 하나 그리고 아님 이번 제출에 NW_NEOUL_LEDGER,NW_OLD_RATIONS 중 하나 | 1 |
| `half_altar4_year14` |  | 아님 이번 제출에 NW_NAMES 중 하나 | 1 |
| `lamp_sale_half_stone` | 2026-10-29 논쟁 점검 P04·P05: 3일 등 회의 2번(돌의 행방)과 4번(그 돌이 새벽까지 등 안에 있던 돌인가)은 같은 자료를 쓰지만 묻는 것이 다르다. 맞는 자료만 일부 낸 오답이면 너울이 그 쟁점의 빈 고리만 묻는다(MS14_D03_S05_L0071 변형). 3일 회의 | [meeting:lamp] 없음 그리고 r13_nw_wrong_issue()=="돌과 매입 기록을 낸다" 그리고 r13_gp_given()=={"V111:E15"} | 1 |
| `lamp_sale_half_ledger` |  | [meeting:lamp] 없음 그리고 r13_nw_wrong_issue()=="돌과 매입 기록을 낸다" 그리고 r13_gp_given()=={"V111:E16"} | 1 |
| `lamp_stone_half_check` |  | [meeting:lamp] 없음 그리고 r13_nw_wrong_issue()=="마지막 점검과 인수한 돌을 연결한다" 그리고 bool(r13_gp_given()) 그리고 r13_gp_given()<={"V111:E15","V111:E16"} | 1 |
| `lamp_stone_half_mark` |  | [meeting:lamp] 없음 그리고 r13_nw_wrong_issue()=="마지막 점검과 인수한 돌을 연결한다" 그리고 r13_gp_given() in ({"V111:E11"},{"V111:E11","V111:E16"}) | 1 |
| `lamp_stone_half_sale` |  | [meeting:lamp] 없음 그리고 r13_nw_wrong_issue()=="마지막 점검과 인수한 돌을 연결한다" 그리고 r13_gp_given()=={"V111:E11","V111:E15"} | 1 |
| `half_la_check3` | 2026-10-29 논쟁 점검 P11: 3일 등 예방판(lamp_bound2) A·B 의 일부 정답 반박(half_la_repair3·half_la_final3). | 이번 제출에 NW_LA_CHECK 중 하나 그리고 아님 이번 제출에 NW_LA_FIELD 중 하나 | 1 |
| `half_la_field3` |  | 이번 제출에 NW_LA_FIELD 중 하나 그리고 아님 이번 제출에 NW_LA_CHECK 중 하나 | 1 |
| `half_la_noknife3` |  | 아님 이번 제출에 NW_LA_KNIFE 중 하나 | 1 |
| `half_la_nofield3` |  | 이번 제출에 NW_LA_KNIFE 중 하나 그리고 아님 이번 제출에 NW_LA_FIELD 중 하나 | 1 |
| `half_la_nocheck3` |  | 이번 제출에 NW_LA_KNIFE 중 하나 그리고 이번 제출에 NW_LA_FIELD 중 하나 그리고 아님 이번 제출에 NW_LA_CHECK 중 하나 | 1 |
| `room13_stage_wound10` | 2026-10-29 논쟁 점검 P07: 10일 13호 되묻기 줄(MS14_D10_S02_L0051)은 1번·2번이 함께 쓴다. 1번(두 상처)일 때만 그 쟁점을 짚는다. | r13_nw_wrong_issue()=="두 상처와 촛대 파손을 대조한다" | 1 |
| `fire_win_empty` | 2026-10-30 논쟁 점검 낮음 P15: 7일 불 2번을 이긴 뒤 아빠가 「불은 누비, 보리는 진압/구조」로 갈라 정리한다(대피 여부로 갈림). | [meeting:fire]=="win" 그리고 [FIRE_EVACUATED] =참 | 1 |
| `fire_win_rescue` |  | [meeting:fire]=="win" 그리고 [FIRE_EVACUATED] ≠참 | 1 |
| `soup_stage_seal12` | P22: 12일 되묻기 줄(MS14_D12_S04_L0093)은 1번·2번이 함께 쓴다. 1번(병이 정말 빈 병이었나)일 때는 1번 고리만 짚는다. | r13_nw_wrong_issue()=="재사용 설명과 개봉 봉인을 대조한다" | 1 |
| `compare_letter1` | P23: 두 편지 자기 대조의 오답 한 줄을 1일·5일로 가른다(같은 compare_retry 묶음). | r13_nw_wrong_issue()!="두 편지의 초대를 대조한다" | 1 |
| `compare_warning5` |  | r13_nw_wrong_issue()=="두 편지의 초대를 대조한다" | 1 |
| `gate_post_won_with_e24` | P26: 5일 초소를 이긴 뒤 「그럼 네로요」에 답할 때, 네로의 귀가 관찰을 냈으면 그 자료에서 출발한다. | "V111:E24" in ([proof_given:밤이 혐의의 근거를 확인한다] 또는 []) | 1 |
| `gate_post_won_without_e24` |  | "V111:E24" 아님 in ([proof_given:밤이 혐의의 근거를 확인한다] 또는 []) | 1 |
| `guldol_daram` |  | _r13_bd_with_daram(lambda:resident_guldol 이(가) 그 자리에 있음) | 3 |
| `guldol_daram13` |  | _r13_bd_with_daram(lambda:resident_guldol 이(가) 그 자리에 있음) | 1 |
| `tok_listed_daram` |  | _r13_bd_with_daram(lambda:[listed:resident_tok] =참) | 1 |
| `bami_listed_daram` |  | _r13_bd_with_daram(lambda:[listed:bami] =참) | 1 |
| `bori_listed_daram` |  | _r13_bd_with_daram(lambda:[listed:resident_bori] =참) | 1 |
| `nabi_listed_daram` |  | _r13_bd_with_daram(lambda:[listed:nabi] =참) | 2 |
| `nabi_list12_daram` |  | _r13_bd_with_daram(lambda:R13_NW_WHEN["soup_lose_nabi"]()) | 2 |
| `teacher_hides13` | 12일 국을 막은 판(early/premeal)에도 선생님의 목적(이송 칸 아이를 보내지 않으려는 것)은 남는다. 이송 칸이 무효가 된 판(수프 대승리)에는 숨길 까닭이 없다. | [fate:fate_soup] in ("early","premeal") 그리고 [transfer_list_voided] ≠참 그리고 resident_teacher 이(가) 그 자리에 있음 | 2 |
| `dead:resident_piko` |  | resident_piko 이(가) 죽었거나 수레로 떠남(r13_nw_dead) | 1 |
| `dead:kid_kkomi` |  | kid_kkomi 이(가) 죽었거나 수레로 떠남(r13_nw_dead) | 1 |
| `dead:resident_owlgp` |  | resident_owlgp 이(가) 죽었거나 수레로 떠남(r13_nw_dead) | 1 |
| `dead:resident_nero` |  | resident_nero 이(가) 죽었거나 수레로 떠남(r13_nw_dead) | 1 |
| `dead:kid_dodam` |  | kid_dodam 이(가) 죽었거나 수레로 떠남(r13_nw_dead) | 1 |
| `dead:neoul` |  | neoul 이(가) 죽었거나 수레로 떠남(r13_nw_dead) | 3 |
| `dead:resident_momo` |  | resident_momo 이(가) 죽었거나 수레로 떠남(r13_nw_dead) | 1 |
| `dead:v111_lowerroad_elder` |  | v111_lowerroad_elder 이(가) 죽었거나 수레로 떠남(r13_nw_dead) | 1 |
| `listed:resident_tok` |  | resident_tok 이(가) 이송 명단에 적힘 | 15 |
| `listed:bami` |  | bami 이(가) 이송 명단에 적힘 | 2 |
| `listed:resident_bori` |  | resident_bori 이(가) 이송 명단에 적힘 | 2 |
| `listed:nabi` |  | nabi 이(가) 이송 명단에 적힘 | 2 |
| `listed:daram` |  | daram 이(가) 이송 명단에 적힘 | 4 |
| `listed:resident_owlgp` |  | resident_owlgp 이(가) 이송 명단에 적힘 | 1 |
| `listed:resident_piko` |  | resident_piko 이(가) 이송 명단에 적힘 | 2 |
| `listed:resident_siluk` |  | resident_siluk 이(가) 이송 명단에 적힘 | 2 |
| `listed:resident_guldol` |  | resident_guldol 이(가) 이송 명단에 적힘 | 3 |
| `listed:resident_teacher` |  | resident_teacher 이(가) 이송 명단에 적힘 | 0 |
| `listed:mom` |  | mom 이(가) 이송 명단에 적힘 | 0 |
| `listed:dad` |  | dad 이(가) 이송 명단에 적힘 | 0 |

### 장면 진입 검사(`R13_V111_SCENE_CHECKS`, 최종 합성)

- `MS14_D06_S01`: `lambda:r13_v111_value("mother_warning_received") is True`
- `MS14_D06_S02`: `lambda:r13_v111_value("school_day_seat")=="confirmed"`
- `MS14_D06_S03`: `lambda:r13_v111_value("FIRE_EVACUATED") is False`
- `MS14_D06_P01`: `lambda:r13_v111_value("evacuation_requested") is True`
- `MS14_D06_S03P`: `lambda:r13_v111_value("FIRE_EVACUATED") is True and r13_v111_value("warehouse_children_school_handover")==4`
- `MS14_D06_S04`: `lambda:bool(r13_v111_value("D06_S03_main_completed") or r13_v111_value("D06_S03P_empty_fire_completed"))`
- `MS14_D07_S01`: `lambda:r13_v111_owned("E06_FIRE")`
- `MS14_D07_S02`: `(lambda:r13_v111_value("NUBI_admitted_setting_fire") is True) or r13_v111_value("meeting:fire")=="lose"`
- `MS14_D07_S03`: `lambda:r13_v111_value("D07_S02_handover_completed") is True`
- `MS14_D07_S04`: `lambda:r13_v111_value("route7")=="murder" and r13_v111_value("D07_S03_C_completed") is True`
- `MS14_D08_S01`: `lambda:r13_v111_value("route7")=="murder" and r13_v111_value("DARAM_DETAINED") is True`
- `MS14_D08_S02`: `lambda:r13_v111_value("route7")=="murder" and r13_v111_value("OWL_ALIVE") is False`
- `MS14_D08_S03`: `lambda:r13_v111_value("route7")=="murder" and r13_v111_owned("E08_ROOM")`
- `MS14_D08_P01`: `lambda:r13_v111_value("route7")=="prevented" and r13_v111_value("OWL_ALIVE") is True`
- `MS14_D09_S01`: `lambda:r13_v111_value("route7")=="murder"`
- `MS14_D09_S02`: `lambda:r13_v111_value("route7")=="murder" and r13_v111_owned("E09_PASSAGE")`
- `MS14_D09_S03`: `lambda:r13_v111_owned("E09_PIN_OWNER")`
- `MS14_D09_P01`: `lambda:r13_v111_value("route7")=="prevented" and r13_v111_value("OWL_ALIVE") is True`
- `MS14_D10_S01`: `lambda:r13_v111_value("route7")=="murder" and all(r13_v111_owned(k) for k in ("E08_CHILD_POSITION","E08_ROOM_REACH","E08_CONTACT_ASSEMBLY","E08_WOUND_WIRE","E09_PIN_HANDOVER_TIME","E09_SCARF"))`
- `MS14_D10_S02`: `lambda:r13_v111_value("D10_S01_main_completed") is True`
- `MS14_D10_S03`: `lambda:r13_v111_value("D10_S02_second_door_completed") is True`
- `MS14_D10_S04`: `lambda:r13_v111_value("D10_confrontation_release_completed") is True and r13_v111_value("DARAM_DETAINED") is False`
- `MS14_D10_P01`: `lambda:r13_v111_value("route7")=="prevented" and r13_v111_value("OWL_ALIVE") is True`
- `MS14_D11_S00`: `lambda:r13_v111_owned("E10_PUMP")`
- `MS14_D11_S01`: `lambda:r13_v111_value("root_address_known") is True`
- `MS14_D11_S02`: `lambda:r13_v111_value("tosil_safe_handoff_confirmed") is True and r13_v111_value("greenhouse_address_known") is True`
- `MS14_D11_S02A`: `lambda:r13_v111_value("family_reunited") is True`
- `MS14_D11_S02B`: `lambda:r13_v111_value("family_reunited") is True`
- `MS14_D11_S03`: `lambda:r13_v111_value("family_reunited") is True`
- `MS14_D11_S04`: `lambda:r13_v111_value("family_school_place") is True`
- `MS14_D12_S01`: `lambda:r13_v111_value("lower_road_handover")==3 or r13_v111_value("lower_road_lost") is True`
- `MS14_D12_S03`: `lambda:r13_v111_value("route12")=="late_exposure"`
- `MS14_D12_S04`: `lambda:r13_v111_value("route12") in ("late_exposure","premeal_stopped") and r13_v111_value("soup_fragment_observed") is True`
- `MS14_D12_S05`: `lambda:r13_v111_value("route12")=="late_exposure" and r13_v111_value("teacher_confessed") is True and r13_v111_value("medical_arrived") is True`
- `MS14_D12_A`: `lambda:r13_v111_value("route12")=="premeal_stopped"`
- `MS14_D12_B`: `lambda:r13_v111_value("route12")=="early_prevented"`
- `MS14_D13_S02`: `lambda:r13_v111_value("family_reunited") is True and r13_v111_value("DARAM_DETAINED") is not True`
- `MS14_D13_S03`: `lambda:r13_v111_value("family_deal") is False and r13_v111_owned("E13_MENDING")`
- `MS14_D13_S04`: `lambda:r13_v111_value("false_message_admitted") is True`
- `MS14_D13_A`: `lambda:r13_v111_value("family_deal") is True`
- `MS14_D13_B`: `lambda:r13_v111_value("cart_stopped") is True and not r13_v111_value("all_cart_handed")`
- `MS14_D13_C`: `lambda:r13_v111_value("false_message_admitted") is True and r13_v111_value("cart_stopped") is True`
- `MS14_D14_S01`: `lambda:r13_v111_value("all_cart_handed") is True`
- `MS14_D14_S02`: `lambda:r13_v111_value("all_cart_handed") is True and r13_v111_value("altar_guide_confirmed") is True`
- `MS14_D14_S04`: `lambda:r13_v111_value("bomi_death_confirmed") is True`
- `MS14_D14_S05`: `lambda:r13_v111_value("family_reunited") is True and r13_v111_value("night14_lodging") in ("gate","school")`
- `MS14_D14_END_FAMILY`: `lambda:r13_v111_value("outcome13")=="family_priority"`
- `MS14_D14_END_PARTIAL`: `lambda:r13_v111_value("outcome13")=="partial_rescue"`
- `MS14_D14_END_VIOLENCE`: `lambda:r13_v111_value("crowd_injury") is True`
- `MS14_D01_S04`: `r13_v111_value("gate_basis_proven") is True or r13_v111_value("gate_daram_unlisted") is True`
- `MS14_D03_S06`: `r13_v111_value("lamp_theft_supported") is True or r13_v111_value("meeting:lamp") in ("partial","lose")`
- `MS14_D05_S04`: `r13_v111_value("bami_status") in ("cleared","listed")`

## 자료(증거) 89개

| ID | 이름 | 종류 | 얻는 곳(장면 · 경로) | 회의 쓰임 | facts(첫 변형) |
|---|---|---|---|---|---|
| E01 | 초대 편지 | 기록 | D01_S01 commit MS14_D01_S01_L0010 | 덧붙임: 함께 들어갈 근거를 고른다; 정답: 두 편지를 나란히 본다; 정답: 두 편지의 초대를 대조한다; 정답: 반송·필사본·초대 발송을 대조한다; 대체: 반송·필사본·초대 발송을 대조한다 | 다람이를 데리고 와 달라는 편지다. / 여관 13호실에서 기다린다고 적혔다. |
| E02 | 초소 처리 명단 | 기록 | D01_S02 commit MS14_D01_S02_L0019 | 정답: 함께 들어갈 근거를 고른다; 덧붙임: 불의 원인과 빈 창고 진압을 구분한다; 덧붙임: 불의 원인과 아이 구조를 구분한다 | 다돌은 신규 일꾼 1명으로 적혔다. / 동행 아동은 모집에서 제외됐다. / 뒤에 여관에 먼저 연락하라는 쪽지가 있다. |
| E03 | 방문 신청 원본 | 기록 | D01_S03 commit MS14_D01_S03_L0002 | 정답: 함께 들어갈 근거를 고른다 | 다돌이 아내를 만나러 낸 신청서다. / 동행인 다람까지 총 2명으로 적혔다. / 여관 13호에 2명 숙박이 확인됐다. |
| E04 | 겨울철 입장 규칙 | 기록 |  commit MS14_D01_S03_L0007; D01_S03 commit MS14_D01_S03_L0007 | 덧붙임: 함께 들어갈 근거를 고른다 | 방문객은 숙소 확인 뒤 동행인도 등록한다. / 초소에서 인원과 숙소를 확인해 고친다. / 새 일꾼은 작업 명단의 본인만 등록한다. |
| E05 | 정정된 입장 기록 | 기록 | D01_S04 commit MS14_D01_S04_L0008 |  | 신청 원본과 숙박 확인으로 기록을 고쳤다. / 방문객 다돌, 동행인 다람으로 적혔다. / 확인자는 돌목이다. |
| E06 | 방의 메모 | 기록 | D01_S05 commit MS14_D01_S05_L0019 | 정답: 두 편지를 나란히 본다 | 자리를 비우면 초롱에게 물으라고 적혔다. / 물건은 책상 아래에 두었다고 적혔다. |
| E30 | 책상 아래 보따리 | 기록 | D01_S05 commit MS14_D01_S05_L0022 |  | 여벌 목도리와 연필 두 자루가 있다. / 다람의 가족 그림도 들어 있다. / 밑바닥에도 주소나 다른 봉투는 없다. |
| E07 | 초대 봉투 접수 기록 | 기록 | D02_S02 commit MS14_D02_S02_L0005 | 정답: 반송·필사본·초대 발송을 대조한다; 덧붙임: 반송·필사본·초대 발송을 대조한다 | 초대 봉투의 접수 묶음은 여관이다. / 봉투에 소인 날짜와 접수번호가 있다. / 작성자와 전달자 이름은 기록되지 않았다. |
| E08 | 3번 등의 상태 | 기록 | D02_S03 commit MS14_D02_S03_L0025 | 정답: 초롱과 피코의 하루를 대조한다; 덧붙임: 초롱과 피코의 하루를 대조한다; 대체: 초롱과 피코의 하루를 대조한다 | 3번 등 덮개가 덜 맞물려 있다. / 피코의 담요는 얇다. / 받침에서 멀어지면 바닥이 차갑다. |
| E31 | 네로의 공급 경로 | 기록 | D04_S01 commit MS14_D04_S01_L0033; D02_S04 commit MS14_D02_S04_L0083 |  | 네로는 교환함 옆에서 엄마에게 식량을 줬다. / 네로 말로는 엄마가 혼자 빵을 먹었다. / 물자는 학교 옆 공동 창고에서 받는다. |
| E35 | 가족 침구 예약 | 기록 | D02_S04 commit MS14_D02_S04_L0083 | 덧붙임: 아내가 봤다는 담요의 시점을 확인한다 | 다돌 가족 몫으로 침구가 예약됐다. / 예약한 침구는 마른 담요 두 장이다. |
| E09 | 엄마의 초상 | 기록 | D03_S01 apply lamp_attempt:portrait3; D03_S01 commit MS14_D03_S01_L0039; D03_S01 commit MS14_D03_S01_L0021 | 덧붙임: 반송·필사본·초대 발송을 대조한다 | 엄마를 그린 초상이다. / 코가 있어야 할 자리가 비어 있다. / 무릎에 천을 펴고 바늘을 쥔 손이 그려져 있다. |
| E10 | 빈 받침과 자국 | 기록 | D03_S02 commit MS14_D03_S02_L0012 | 덧붙임: 수리와 반출을 가릴 자료를 낸다 | 3번 등은 비어 있다. / 테두리에는 둥근 눌린 자국이 있다. / 안쪽에는 새로 난 곧은 긁힘이 있다. |
| E32 | 안쪽 받침의 칼끝 파편 | 기록 | D03_S02 commit MS14_D03_S02_L0016 | 정답: 바깥 걸쇠 주장과 발견 위치를 대조한다 | 돌받침 안쪽 틈에서 칼끝 파편이 나왔다. / 현장에서 위치와 들어 올리는 방향을 봤다. |
| E11 | 초롱의 점검장 | 기록 | D03_S02 commit MS14_D03_S02_L0027 | 정답: 초롱과 피코의 하루를 대조한다; 대체: 초롱과 피코의 하루를 대조한다; 정답: 측정 종료와 점검 기록을 대조한다; 정답: 수리와 반출을 가릴 자료를 낸다; 정답: 마지막 점검과 인수한 돌을 연결한다 | 점검장에 3번 등, 돌 3으로 적혔다. / 새벽 종 직전에 점검을 마쳤다고 적혔다. |
| E12 | 공구 대여 쪽지 | 기록 | D03_S03 commit MS14_D03_S03_L0008 | 정답: 수리와 반출을 가릴 자료를 낸다 | 빌린 공구는 계측 집게다. / 빌린 사람은 우박이다. / 대여 시점은 전날 저녁이다. |
| E13 | 우박의 측정지 | 기록 | D03_S03 commit MS14_D03_S03_L0027 | 정답: 측정 종료와 점검 기록을 대조한다; 정답: 수리와 반출을 가릴 자료를 낸다 | 등번호 3, 돌표식 3으로 적혔다. / 측정 시작과 종료 기록이 있다. / 우박은 새벽 종 한참 전에 끝났다고 했다. |
| E14 | 실룩의 운반표 | 기록 | D03_S04 commit MS14_D03_S04_L0009 | 덧붙임: 요즘 돌이 어디서 오는지 대조한다 | 운반표의 수취인은 백 부인이다. / 품목은 돌로 적혀 있다. |
| E15 | 창고의 3번 돌 | 기록 | D03_S04 commit MS14_D03_S04_L0028 | 정답: 돌과 매입 기록을 낸다; 정답: 마지막 점검과 인수한 돌을 연결한다 | 백 부인 창고에서 3번 돌을 확인했다. / 톡이 각인과 금 방향 표시를 확인했다. / 같은 상자에 든 나머지 두 돌의 출처는 확인되지 않았다. |
| E16 | 백 부인의 매입 장부 | 기록 | D03_S04 commit MS14_D03_S04_L0032 | 정답: 장부의 두 배를 실룩에게 보인다; 정답: 돌과 매입 기록을 낸다; 정답: 마지막 점검과 인수한 돌을 연결한다 | 판매자 실룩의 이름과 서명이 있다. / 돌 3개와 지급 내역이 적혀 있다. / 장부는 백 부인이 보관한다. |
| E33 | 동의받고 대조한 칼 | 기록 | D03_S05 commit MS14_D03_S05_L0018 | 정답: 바깥 걸쇠 주장과 발견 위치를 대조한다 | 실룩의 동의를 받고 칼과 파편을 맞췄다. / 깨진 단면과 날의 연마선을 살폈다. |
| E17 | 실룩의 걸쇠 진술 | 기록 | D03_S05 commit MS14_D03_S05_L0018 | 정답: 바깥 걸쇠 주장과 발견 위치를 대조한다 | 실룩은 순회 뒤 바깥 걸쇠를 닫았다고 했다. / 안의 돌은 건드리지 않았다고 했다. / 돌은 길에서 주웠다고 했다. |
| E34 | 실룩의 작업표 | 기록 | D04_S01 commit MS14_D04_S01_L0015 | 덧붙임: 장부의 두 배를 실룩에게 보인다 | 실룩은 조사 대기에서 공동작업으로 바뀌었다. / 작업표의 종료일은 비어 있다. / 너울은 저녁 배식 때 아이들을 만난다고 했다. |
| E18 | 솜이의 이야기 | 기록 | D04_S01 commit MS14_D04_S01_L0050 |  | 솜이는 엄마가 할아버지께 책을 읽어 줬다고 했다. / 같은 것을 두 번 읽어도 기다려 줬다고 했다. |
| E19 | 밤이의 제한된 목격 | 증언 | D04_S02 commit MS14_D04_S02_L0025 |  | 밤이는 전에 강 쪽에서 엄마를 봤다고 했다. / 언제 어디로 갔는지는 모른다고 했다. |
| E20 | 돌목의 최초 진술 | 증언 | D04_S03 commit MS14_D04_S03_L0003 | 정답: 밤이 혐의의 근거를 확인한다; 대체: 밤이 혐의의 근거를 확인한다 | 돌목은 얼굴을 못 봤다고 했다. / 검은 것이 털인지 옷인지 모른다고 했다. / 붙잡고 허리를 숙였다가 물렸다고 했다. |
| E22 | 울타리에서 수거한 천 | 기록 | D04_S04 commit MS14_D04_S04_L0044 | 정답: 밤이 혐의의 근거를 확인한다; 대체: 밤이 혐의의 근거를 확인한다 | 초소 문 앞 울타리에 회색 천이 걸려 있었다. / 위치와 방향을 그린 뒤 바둑이와 수거했다. / 발자국은 겹쳐 있다. |
| E23 | 허락받고 대조한 겉옷 | 기록 | D05_S02 commit MS14_D05_S02_L0016 | 정답: 밤이 혐의의 근거를 확인한다; 대체: 밤이 혐의의 근거를 확인한다 | 울타리 천과 벗은 겉옷을 대조했다. / 찢어진 선과 두 줄 수선실을 살폈다. |
| E24 | 네로의 귀가 관찰 | 증언 | D05_S02 commit MS14_D05_S02_L0025 | 정답: 밤이 혐의의 근거를 확인한다; 대체: 밤이 혐의의 근거를 확인한다 | 네로는 소매가 찢어진 채 돌아왔다고 했다. / 네로는 입에 피가 조금 있었다고 했다. / 공격 장면은 보지 못했다고 했다. |
| E25 | 돌목의 재확인 진술 | 증언 | D05_S03 commit MS14_D05_S03_L0037 |  | 돌목은 뒤에서 팔을 잡았다고 했다. / 멈추지 않아 계속 붙잡았다고 했다. / 돌아서다가 물렸다고 했다. |
| E26 | 밤이 혐의 정정 기록 | 기록 | D05_S03 commit MS14_D05_S03_L0037 |  | 밤이가 무는 모습을 본 사람은 없다. / 기록에는 울타리 천과 옷의 대조가 담겼다. / 밤이를 붙잡아 두지 않기로 했다. |
| E27 | 엄마의 경고 편지 | 기록 | D05_S04 commit MS14_D05_S04_L0005 | 정답: 두 편지의 초대를 대조한다; 덧붙임: 반송·필사본·초대 발송을 대조한다; 대체: 반송·필사본·초대 발송을 대조한다 | 엄마는 두 사람을 부른 적 없다고 적었다. / 편지 이야기를 여관에 말하지 말라고 했다. / 먹을 것과 마른 천이 필요하다고 적었다. |
| E28 | 엄마에게 쓰는 답장 | 기록 | D05_S04 commit MS14_D05_S04_L0027 | 덧붙임: 초롱과 피코의 하루를 대조한다 | 다람이는 함께 있다고 적었다. / 다람이 엄지 옆이 텄다고 적었다. / 먹을 것과 천을 준비하겠다고 적었다. / 만날 방법과 있는 곳을 알려 달라고 적었다. |
| E29 | 다음 날 아침 보호 약속 | 기록 | D05_S05 commit MS14_D05_S05_L0027 | 덧붙임: 촌장이 어젯밤 있던 곳을 확인한다 | 내일 아침 바둑이와 다람이 식당 앞에 있다. / 순찰 전까지 아빠가 안 오면 초소로 간다. / 종일 보호하는 약속은 아니다. |
| E21 | 밤이의 그날 밤 목격 | 증언 | D04_S04 commit MS14_D04_S04_L0018 | 덧붙임: 밤이 혐의의 근거를 확인한다 | 밤이는 양동이가 넘어질 때 처마에 있었다고 했다. / 맨발로 울타리 쪽에 가는 사람을 봤다고 했다. / 그 사람의 얼굴과 키는 모른다고 했다. |
| E06_CONTACT | 학교 뒤 공개 물자 수량 | 기록 | D06_S01 commit MS14_D06_S01_L0048 | 정답: 수신인과 가족 전달 권한을 구분한다 | 학교 뒤 공개 보급판에 인수 표시가 있다. / 오늘 수건 두 장과 소금 한 꾸러미다. / 수령인과 거처는 적혀 있지 않다. |
| E06_FIRE | 등잔·천·발화 지점 | 기록 | D06_S04 commit MS14_D06_S04_L0037 | 정답: 불이 시작된 곳과 진술을 대조한다; 정답: 불의 원인과 빈 창고 진압을 구분한다; 대체: 불의 원인과 빈 창고 진압을 구분한다; 정답: 불의 원인과 아이 구조를 구분한다; 대체: 불의 원인과 아이 구조를 구분한다 | 등잔은 뒷벽 물통 옆에 있었다. / 뚜껑이 닫혀 있고 기름이 남아 있었다. / 문 쪽 탄 자국과 기름 냄새 나는 천을 봤다. |
| E08_CHILD_ACCOUNT | 다람의 진술과 손목 기록 | 기록 | D08_S01 commit MS14_D08_S01_L0025 | 정답: 두 상처와 촛대 파손을 대조한다 | 다람은 손목을 놓아 달라고 했다고 말했다. / 그 뒤 촛대로 손을 쳤다고 말했다. / 서리가 손목의 멍을 기록했다. |
| E08_ROOM | 13호 현장과 도토의 관찰 | 기록 | D08_S02 commit MS14_D08_S02_L0037 | 정답: 두 번째 길을 실제 기록으로 보인다 | 문 아래에 벌어진 틈이 있다. / 침대 끝은 문 가까이에 있다. / 발견 자리는 책상 옆으로 표시됐다. |
| E08_CHILD_POSITION | 도토가 확인한 다람의 두 손 | 기록 | D08_S02 commit MS14_D08_S02_L0037 | 정답: 접촉면과 아이의 위치를 대조한다 | 도토는 문틈에서 왼손을 잡았다고 했다. / 오른손의 아랫조각도 보았다고 했다. / 충격음 뒤 문이 열릴 때까지 두 손을 봤다고 했다. |
| E08_ROOM_REACH | 문틈과 책상 사이 거리 | 기록 | D08_S02 commit MS14_D08_S02_L0037 | 정답: 접촉면과 아이의 위치를 대조한다 | 도토가 다람의 손을 잡은 곳은 문틈이다. / 책상 옆 발견 자리까지 거리를 확인했다. |
| E08_TOOL | 촛대 파손·상처 대조 자료 | 기록 | D08_S03 commit MS14_D08_S03_L0028 | 정답: 두 상처와 촛대 파손을 대조한다 | 촛대의 윗조각과 손잡이 아래조각이 나뉘었다. / 윗조각의 장식 고리에 천과 핀이 남아 있다. / 서리가 손목과 머리의 상처를 살폈다. |
| E08_CONTACT_ASSEMBLY | 접힌 천·닫힌 핀·고리 | 기록 | D08_S03 commit MS14_D08_S03_L0028 | 대체: 구리선과 수선 출처를 대조한다; 정답: 접촉면과 아이의 위치를 대조한다 | 닫힌 핀이 접힌 천과 장식 고리를 통과한다. / 뒤쪽은 천으로 감겨 있다. / 앞의 깨진 면과 구리 끝은 드러나 있다. |
| E08_WOUND_WIRE | 상처 가장자리의 구리 파편 | 기록 | D08_S03 commit MS14_D08_S03_L0028 | 정답: 구리선과 수선 출처를 대조한다; 정답: 접촉면과 아이의 위치를 대조한다 | 머리 상처 가장자리에서 구리선이 나왔다. / 짧은 구리선 조각을 따로 보관했다. / 핀의 구리 수리 끝에는 빈 부분이 있다. |
| E08_RECENT_LETTER | 6일에 쓴 엄마의 편지 | 기록 | D08_S04 commit MS14_D08_S04_L0033 |  | 편지에 적힌 날짜: 6일 · 받은 날: 8일(초롱이 건넴) / “아이를 여관으로 데려오지 마요.” / “물자 답은 부엉이 씨에게 남겼어요.” |
| E09_PASSAGE | 직접 왕복한 통로 | 기록 | D09_S01 commit MS14_D09_S01_L0014; D09_P01 commit MS14_D09_P01_L0012 | 정답: 두 번째 길을 실제 기록으로 보인다 | 쐐기와 안전줄, 바깥 문지기를 확인했다. / 직접 왕복한 통로는 13호 뒤로 이어진다. / 문은 주방에서 열고 안쪽 손잡이는 없다. |
| E09_PIN_OWNER | 핀 수선과 인수 기록 | 기록 | D09_S02 commit MS14_D09_S02_L0018; D09_S02 commit MS14_D09_S02_L0026 | 정답: 구리선과 수선 출처를 대조한다; 대체: 구리선과 수선 출처를 대조한다 | 공방 수선장과 인수 기록 사본이다. / 핀 뒤의 구리 수리 끝을 확인했다. / 핀의 수령인도 확인했다. |
| E09_PIN_TIME | 첫 비명 뒤 핀을 다시 채운 때 | 기록 | D09_S03 commit MS14_D09_S03_L0034 | 정답: 첫 비명 뒤 핀을 다시 채운 때 | 나비는 첫 비명 뒤 할머니 목도리가 걸렸다고 했다. / 그때 나비가 핀을 다시 채웠다고 했다. / 핀 끝에 손가락을 찔렸다고 했다. |
| E09_PIN_HANDOVER_TIME | 양손 확인 뒤 계단참의 핀 | 기록 | D09_S03 commit MS14_D09_S03_L0034 | 정답: 첫 비명 뒤 핀을 다시 채운 때 | 나비는 핀이 할머니 목도리에 있었다고 했다. / 그때 도토가 다람의 손을 잡고 있었다고 했다. / 주방으로 이동한 것은 그 뒤라고 했다. |
| E09_SCARF | 목도리 찢어진 끝 | 기록 | D09_S03 commit MS14_D09_S03_L0049 | 정답: 접촉면과 아이의 위치를 대조한다 | 할머니 목도리의 한 귀퉁이가 뜯겨 있다. / 할머니는 그 천을 주워 감쌌다고 말했다. |
| E09_MAIL | 발송·필사본·반송의 출처 | 기록 | D09_S04 commit MS14_D09_S04_L0024 | 정답: 수신인과 가족 전달 권한을 구분한다; 정답: 반송·필사본·초대 발송을 대조한다; 대체: 반송·필사본·초대 발송을 대조한다 | 본보기 아래에 작업 날짜가 있다. / 반송 접수 날짜와 초대 발송 날짜가 있다. / 날짜는 반송 접수, 본보기 작업, 초대 발송 순서다. |
| E10_PUMP | 6일에 마지막 쓴 연락함 | 기록 | D10_S04 commit MS14_D10_S04_L0027; D10_P01 commit MS14_D10_P01_L0083; D10_P01 commit MS14_D10_P01_L0083 |  | 물자 인수 날짜와 소금·수건 수량이 있다. / “옛 펌프집 아래 통, 셋째 말뚝” / “옮길 때만 답을 둔다.” |
| E12_FRAGMENT | 냄비 파편과 병 입구 | 기록 | D12_S04 apply fragment_comparison12 | 정답: 재사용 설명과 개봉 봉인을 대조한다; 정답: 파편·봉인·취급 구간을 함께 제시한다 | 작은 냄비에 남은 파편을 살폈다. / 병 입구의 경계 두 곳과 이음선을 대조했다. |
| E12_SEAL | 준비 때 온전했던 개봉 봉인 | 기록 | D12_S04 apply original_seal_recalled12 | 정답: 재사용 설명과 개봉 봉인을 대조한다; 정답: 파편·봉인·취급 구간을 함께 제시한다 | 배식 준비 때 선생님이 받은 병이다. / 마개와 목을 잇는 봉인은 끊어지지 않았다. |
| E12_HANDLING | 작은 냄비의 인계·관찰 구간 | 기록 | D12_S04 apply handling_observed12 | 정답: 파편·봉인·취급 구간을 함께 제시한다 | 나비가 큰 냄비에서 덜어 직접 건넸다. / 교사의 손은 가림판 뒤에 있었다. / 지켜본 동안 세척대로 오가지는 않았다. |
| E13_MENDING | 오늘 아침 회색 담요 수선 | 기록 | D13_S01 apply actual_blanket_mending13 | 정답: 아내가 봤다는 담요의 시점을 확인한다 | 아빠가 회색 담요에 새 무늬 천을 꿰맸다. / 다람이 천을 잡았다. / 까로가 판돌에게 담요를 둘러 주었다. |
| E13_HANDOVER | 판돌의 학교 인수 기록 | 기록 | D13_S04 apply pandol_actual_school_handover |  | 판돌을 발판으로 내려 부축했다. / 나비가 학교 침상에서 판돌을 인수했다. |
| E14_SUPPLY | 학교 장작 인수 기록 | 기록 | D12_S01 apply actual_school_supply12; D11_S04 apply actual_late_school_supply11; D11_S03 apply actual_school_supply11 | 대체: 희생의 숫자와 장부를 대조한다 | 아빠와 까로가 장작 묶음을 운반했다. / 선생님이 그 장작을 인수했다. / 오늘 밤 쓸 양은 따로 확인한다. |
| E06_EMPTY | 빈 창고 진압과 네 아이 인수 | 관찰기록 | D06_S04 commit MS14_D06_S04_L0030 | 정답: 불의 원인과 빈 창고 진압을 구분한다; 대체: 불의 원인과 빈 창고 진압을 구분한다 | 네 아이를 학교에 인계했다. / 그 뒤 창고에는 아이들이 없었다. / 아빠는 보리가 불 확산을 막는 모습을 봤다. |
| E06_RESCUE | 보리의 세 아이 구조 목격 | 관찰기록 | D06_S04 commit MS14_D06_S04_L0027 | 정답: 불의 원인과 아이 구조를 구분한다; 대체: 불의 원인과 아이 구조를 구분한다 | 보리는 아이 하나를 안고 나왔다. / 두 아이가 뒤따라 나오는 것을 아빠가 봤다. / 꼬미는 구조하지 못했다. |
| E07_NUBI | 누비의 직접 진술 | 증언 | D07_S01 commit MS14_D07_S01_L0045 | 정답: 불의 원인과 빈 창고 진압을 구분한다; 정답: 불의 원인과 아이 구조를 구분한다 | 누비가 직접 진술했다. / 자신이 불을 놓았다고 말했다. |
| E13_ORDER | 중지된 이송 명령 사본 | 기록 | D13_S04 apply actual_stopped_order13 |  | 돌목이 현재 이송 명령 전체를 중지했다. / 입구에서 인수하는 일도 중지한다. / 기존 감독 기록은 보존한다. |
| NW_PIKO_TREMOR | 피코의 손 떨림 | 관찰기록 | D02_S03 r13_nw_acquire | 정답: 초롱과 피코의 하루를 대조한다; 대체: 초롱과 피코의 하루를 대조한다 | 2일 광장, 피코의 손끝이 가늘게 떨렸다. / 피코는 이 불 아래서 손이 덜 떨린다고 했다. / 피코는 3번 등 바로 아래에서 지낸다. |
| NW_INNER_PRICE | 안쪽 돌의 값 | 증언 | D03_S01 r13_nw_acquire; D03_S04 r13_nw_acquire | 정답: 요즘 돌이 어디서 오는지 대조한다 | 백 부인은 센 돌을 찾는 집이 많다고 했다. / 안쪽 돌은 값이 세 배라고 말했다. |
| NW_KEEPER_DATE | 날짜를 두 번 물은 창고지기 | 관찰기록 | D03_S01 r13_nw_acquire; D03_S04 r13_nw_acquire | 정답: 창고에서 잠자는 사람을 짚는다 | 3일, 창고 침상의 노인이 날짜를 두 번 물었다. / 백 부인은 자신이 식당 위층에 산다고 했다. / 노인은 여기서 잔다고 백 부인이 말했다. |
| NW_PIKO_SKETCH4 | 피코의 처마 옆 그림 | 관찰기록 | D04_S04 r13_nw_acquire | 덧붙임: 밤이 혐의의 근거를 확인한다; 대체: 밤이 혐의의 근거를 확인한다 |  |
| NW_MUSOE_DEEP | 갱도 맨 아래까지 간 무쇠 | 증언 | D05_S01 r13_nw_acquire | 정답: 요즘 돌이 어디서 오는지 대조한다 | 솜이는 할아버지가 갱도 맨 아래까지 갔다고 했다. / 안쪽 돌을 제일 많이 캤다고 전했다. |
| NW_LAUNDRY_TALK | 빨래터에서 들은 너울의 말 | 관찰기록 | D05_S05 r13_nw_acquire | 덧붙임: 불의 원인과 빈 창고 진압을 구분한다; 덧붙임: 불의 원인과 아이 구조를 구분한다 |  |
| NW_KKOMI_NOSTONE | 창고 아이들의 기름 등잔 | 증언 | D06_S02 r13_nw_acquire | 대체: 희생의 숫자와 장부를 대조한다; 정답: 아르카가 없는 아이들과 대조한다 | 꼬미는 “우린 표도 없고 돌도 없어.”라고 했다. / 창고 아이들은 나비가 준 기름 등잔을 쓴다. |
| NW_NUBI_TICKET | 누비네 배급표의 덧붙인 줄 | 물증 | D07_S01 r13_nw_acquire | 대체: 불의 원인과 빈 창고 진압을 구분한다; 대체: 불의 원인과 아이 구조를 구분한다 |  |
| NW_STONE | 각인 없는 검푸른 돌 | 물증 | D08_S02 r13_nw_acquire; D08_P01 r13_nw_acquire; D07_S02 r13_nw_acquire; D07_S02 r13_nw_acquire | 정답: 13호 난로의 돌을 내놓는다 | 13호 난로 속에서 나온 검푸르게 탄 돌이다. / 돌에 배급 각인이 없다. / 도토는 그날 배급 돌을 넣었다고 말했다. |
| NW_SICK_BEDS | 학교 침상 목록의 꽃 표시 | 기록 | D11_S03 r13_nw_acquire | 덧붙임: 명단과 흰 그릇을 대조한다; 대체: 희생의 숫자와 장부를 대조한다; 정답: 아르카가 없는 아이들과 대조한다 | 11일 학교 입구의 선생님 침상 목록이다. / 큰 집 아이들에게 야생화 아이 표시가 있다. / 창고에서 온 아이들 이름 옆에는 표시가 없다. |
| NW_TABLET_A | 깨진 돌판 | 물증 | D11_S03 r13_nw_acquire | 정답: 아르카가 부른다는 말과 옛 기록을 대조한다 | 옛 시설 벽에서 떨어져 반이 깨진 돌판이다. / “아르카는 장치 안에서만 쓰라.” / “꺼내어……” 뒤의 글은 없다. |
| NW_NAMES | 벽에 새긴 이름들 | 기록 | D11_S03 r13_nw_acquire | 정답: 맨 처음 이름을 짚는다; 대체: 맨 처음 이름을 짚는다 | 옛 시설 벽에 칼끝으로 이름들이 새겨졌다. / 맨 위는 달래, 중간은 보미, 끝은 모과다. / 아빠가 수첩에 이름을 옮겨 적었다. |
| NW_TRANSFER_LIST | 학교 문 옆 이송 예정 칸 | 기록 | D12_S01 r13_nw_acquire | 정답: 명단과 흰 그릇을 대조한다 | 12일 아침 학교 문 옆의 대피 명단이다. / 이송 예정 칸의 이름은 침상과 배급에서 빠져 있다. / 정식 인계가 안 된 아이들과 회의 패자들이다. |
| NW_WHITE_BOWLS | 흰 그릇을 받은 아이들 | 관찰기록 | D12_S02 r13_nw_acquire | 정답: 명단과 흰 그릇을 대조한다; 대체: 명단과 흰 그릇을 대조한다 | 12일 배식의 흰 그릇은 작은 냄비 몫이다. / 흰 그릇은 의자를 끌어다 앉은 아이들 앞에 놓였다. / 도담은 자리가 없어 새미 옆에 앉았다. |
| NW_HALL_WINDOW | 회관 창 안의 촌장과 바둑이 | 관찰기록 | D12_S05 r13_nw_acquire | 정답: 촌장이 어젯밤 있던 곳을 확인한다 | 12일 밤 학교 종이 울릴 무렵이다. / 회관 창 안에 촌장이 앉아 있었다. / 문 옆에는 바둑이가 서 있었다. |
| NW_PIKO_PAINTING | 초상 밑의 그림 | 물증 | D12_S05 r13_nw_acquire; D13_S03 r13_nw_acquire | 정답: 피코가 막혀야 했던 까닭을 보인다 | 12일 밤 난로 곁에서 초상의 덧칠이 들떴다. / 아래로 수레와 묶인 손, 붉은 목도리가 보인다. / 피코가 그 위에 엄마를 덧그렸다. |
| NW_RETURNED_BOWL | 돌아온 흰 그릇 | 관찰기록 | D12_S04 r13_nw_acquire | 덧붙임: 명단과 흰 그릇을 대조한다; 대체: 명단과 흰 그릇을 대조한다 |  |
| NW_NEOUL_LEDGER | 너울의 장부 | 기록 | D13_S04 r13_nw_acquire; D13_C r13_nw_acquire | 정답: 희생의 숫자와 장부를 대조한다; 정답: 맨 처음 이름을 짚는다 | 11일 아랫길 등을 끊었다고 적혀 있다. / 집별 돌 배급량과 돌·장작 창고의 잔량이 날짜별로 있고, 맨 아래에 4년 전 공방 인수장과 그해 배급 줄이 따로 묶여 있다. / 수레마다 실은 이름과 날짜, 뒤쪽에 보미의 이름이 있다. |
| NW_TABLET_B | 제단 밑돌의 글자 | 물증 | D14_S02 r13_nw_acquire | 정답: 아르카가 부른다는 말과 옛 기록을 대조한다 | 제단 장치 밑돌에 글자가 새겨져 있다. / “……불을 켜지 말라.” / “곁의 말이 무너진다.” |
| NW_IRON_MARK | 제단 쇠의 공방 표식 | 물증 | D14_S02 r13_nw_acquire | 정답: 쇠가 언제 붙었는지 보인다 | 제단의 고리 달린 쇠 안쪽에 공방 표식이 있다. / 무슨 표식이냐고 묻자 바둑이는 나중에 말하겠다고만 했다. |
| NW_BURNT_PAGE | 반쯤 탄 수첩 장 | 물증 | D14_S01 r13_nw_acquire | 덧붙임: 맨 처음 이름을 짚는다 | 13일 밤 주방 아궁이 재에서 찾았다. / 나비와 토실이 찾은 부엉이의 수첩 장이다. / “보미 — 어머니가 데려갔다.” |
| NW_MADAM_DAY7 | 백 부인 장부의 7일 줄 | 기록 | D14_S01 r13_nw_acquire |  | 백 부인 창고 장부의 7일 기록이다. / “7일, 여관, 안쪽 돌 하나” |
| NW_OLD_RATIONS | 4년 전 집별 배급 기록 | 기록 | D14_S01 r13_nw_acquire | 대체: 맨 처음 이름을 짚는다 | 학교에서 확인한 4년 전 집별 배급표 사본이다. / 돌을 가장 많이 받은 집은 촌장 댁이다. / 같은 해 장작 창고 잔량은 한 달 치다. |
| NW_LA_CHECK | 3번 등 마지막 점검 | 관찰기록 | D03_S01 r13_nw_acquire | 정답: 수리 뒤 새로 생긴 파손을 가린다; 정답: 남아 있는 돌과 칼의 사용을 연결한다; 대체: 초롱과 피코의 하루를 대조한다 |  |
| NW_LA_FIELD | 남아 있는 3번 돌과 안쪽 조각 | 관찰기록 | D03_S01 r13_nw_acquire | 정답: 수리 뒤 새로 생긴 파손을 가린다; 정답: 남아 있는 돌과 칼의 사용을 연결한다 |  |
| NW_LA_KNIFE | 동의받아 맞춘 실룩의 칼 | 관찰기록 | D03_S01 r13_nw_acquire | 정답: 남아 있는 돌과 칼의 사용을 연결한다 |  |
| NW_LA_OFFER | 인수되지 않은 3번 돌의 두 배 값 | 관찰기록 | D03_S01 r13_nw_acquire | 정답: 인수하지 않은 돌의 약속 값을 보인다 |  |

## 상태 값 656개

쓰기·읽기 위치는 `inventory.json` 의 `state_keys`(각 12곳까지). `*` 는 사람·장면 이름이 붙는 묶음 키, `(식)` 은 키를 계산으로 만드는 곳.

| 키 | 처음 값 | 쓰기 | 읽기 | 첫 쓰기 위치 | 첫 읽기 위치 |
|---|---|---|---|---|---|
| `BORI_hands` | (없음) | 3 | 0 | records.json:MS14_D06_S03_L0022 |  |
| `BURI_notebook` | (없음) | 1 | 0 | records.json:MS14_D10_S01_L0019 |  |
| `CHORONG_ALIVE` | (없음) | 1 | 0 | records.json:MS14_D08_S04_L0033 |  |
| `D02_afternoon` | (없음) | 2 | 3 | records.json options:MS14_D02_S04_L0020_O1 | room13_v111.rpy:550 |
| `D06_P01_handover_completed` | (없음) | 1 | 0 | records.json:MS14_D06_P01_L0024 |  |
| `D06_P01_permission_completed` | (없음) | 1 | 0 | records.json:MS14_D06_P01_L0008 |  |
| `D06_S01_blankets_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S01_L0016 |  |
| `D06_S01_bowl_choice_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S01_L0025 |  |
| `D06_S01_bowl_eat_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S01_L0033 |  |
| `D06_S01_bowl_together_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S01_L0029 |  |
| `D06_S01_children_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S01_L0023 |  |
| `D06_S01_opening_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S01_L0012 |  |
| `D06_S01_supply_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S01_L0048 |  |
| `D06_S02_evacuation_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S02_L0026 |  |
| `D06_S02_inspect_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S02_L0024 |  |
| `D06_S02_permission_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S02_L0033 |  |
| `D06_S02_today_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S02_L0029 |  |
| `D06_S03P_empty_fire_completed` | (없음) | 1 | 1 | records.json:MS14_D06_S03P_L0008 | room13_v111_later_bindings.rpy:122 |
| `D06_S03_main_completed` | (없음) | 1 | 1 | records.json:MS14_D06_S03_L0022 | room13_v111_later_bindings.rpy:122 |
| `D06_S04_accusation_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S04_L0024 |  |
| `D06_S04_burns_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S04_L0014 |  |
| `D06_S04_empty_bowl_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S04_L0043 |  |
| `D06_S04_empty_testimony_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S04_L0030 |  |
| `D06_S04_fire_evidence_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S04_L0037 |  |
| `D06_S04_full_bowls_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S04_L0049 |  |
| `D06_S04_nabi_lamp_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S04_L0010 |  |
| `D06_S04_no_burns_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S04_L0018 |  |
| `D06_S04_rescue_testimony_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S04_L0027 |  |
| `D06_S04_supplies_completed` | (없음) | 1 | 0 | records.json:MS14_D06_S04_L0005 |  |
| `D07_P01_main_completed` | (없음) | 1 | 0 | records.json:MS14_D07_P01_L0014 |  |
| `D07_P02_main_completed` | (없음) | 1 | 0 | records.json:MS14_D07_P02_L0021 |  |
| `D07_S01_admission_completed` | (없음) | 1 | 0 | records.json:MS14_D07_S01_L0045 |  |
| `D07_S01_child_place_completed` | (없음) | 1 | 0 | records.json:MS14_D07_S01_L0019 |  |
| `D07_S01_here_completed` | (없음) | 1 | 0 | records.json:MS14_D07_S01_L0029 |  |
| `D07_S01_questions_completed` | (없음) | 1 | 0 | records.json:MS14_D07_S01_L0017 |  |
| `D07_S01_school_completed` | (없음) | 1 | 0 | records.json:MS14_D07_S01_L0024 |  |
| `D07_S02_fourth_child_completed` | (없음) | 1 | 0 | records.json:MS14_D07_S02_L0052 |  |
| `D07_S02_handover_completed` | (없음) | 1 | 1 | records.json:MS14_D07_S02_L0029 | room13_v111_later_bindings.rpy:125 |
| `D07_S02_living_child_completed` | (없음) | 1 | 0 | records.json:MS14_D07_S02_L0037 |  |
| `D07_S02_lost_child_completed` | (없음) | 1 | 0 | records.json:MS14_D07_S02_L0033 |  |
| `D07_S02_message_completed` | (없음) | 1 | 0 | records.json:MS14_D07_S02_L0046 |  |
| `D07_S02_responsibility_completed` | (없음) | 1 | 0 | records.json:MS14_D07_S02_L0014 |  |
| `D07_S03_A_completed` | (없음) | 1 | 0 | records.json:MS14_D07_S03_L0019 |  |
| `D07_S03_B_completed` | (없음) | 1 | 0 | records.json:MS14_D07_S03_L0022 |  |
| `D07_S03_C_completed` | (없음) | 1 | 1 | records.json:MS14_D07_S03_L0031 | room13_v111_later_bindings.rpy:126 |
| `D07_S03_medical_request_completed` | (없음) | 1 | 0 | records.json:MS14_D07_S03_L0014 |  |
| `D07_S03_protection_completed` | (없음) | 1 | 0 | records.json:MS14_D07_S03_L0016 |  |
| `D07_S04_main_completed` | (없음) | 1 | 0 | records.json:MS14_D07_S04_L0036 |  |
| `D07_medical_care` | (없음) | 5 | 0 | room13_v111_owl_prevent.rpy:94 |  |
| `D08_P01_care_B_completed` | (없음) | 1 | 0 | records.json:MS14_D08_P01_L0017 |  |
| `D08_P01_fear_A_completed` | (없음) | 1 | 0 | records.json:MS14_D08_P01_L0010 |  |
| `D08_P01_missing_pages_completed` | (없음) | 1 | 0 | records.json:MS14_D08_P01_L0026 |  |
| `D08_S01_main_completed` | (없음) | 1 | 0 | records.json:MS14_D08_S01_L0025 |  |
| `D08_S02_main_completed` | (없음) | 1 | 0 | records.json:MS14_D08_S02_L0037 |  |
| `D08_S03_main_completed` | (없음) | 1 | 0 | records.json:MS14_D08_S03_L0028 |  |
| `D08_S04_escort_completed` | (없음) | 1 | 0 | records.json:MS14_D08_S04_L0005 |  |
| `D08_S04_escort_murder_completed` | (없음) | 1 | 0 | records.json:MS14_D08_S04_L0013 |  |
| `D08_S04_escort_prevent_completed` | (없음) | 1 | 0 | records.json:MS14_D08_S04_L0021 |  |
| `D08_S04_keep_private_completed` | (없음) | 1 | 0 | records.json:MS14_D08_S04_L0033 |  |
| `D08_S04_late_completed` | (없음) | 1 | 0 | records.json:MS14_D08_S04_L0026 |  |
| `D08_S04_safe_completed` | (없음) | 1 | 0 | records.json:MS14_D08_S04_L0030 |  |
| `D09_P01_passage_completed` | (없음) | 1 | 0 | records.json:MS14_D09_P01_L0012 |  |
| `D09_P01_records_completed` | (없음) | 1 | 0 | records.json:MS14_D09_P01_L0027 |  |
| `D09_S01_main_completed` | (없음) | 1 | 0 | records.json:MS14_D09_S01_L0014 |  |
| `D09_S02_receipt_completed` | (없음) | 1 | 0 | records.json:MS14_D09_S02_L0026 |  |
| `D09_S02_tok_completed` | (없음) | 1 | 0 | records.json:MS14_D09_S02_L0018 |  |
| `D09_S03_repair_trust_completed` | (없음) | 1 | 0 | records.json:MS14_D09_S03_L0005 |  |
| `D09_S03_scarf_completed` | (없음) | 1 | 0 | records.json:MS14_D09_S03_L0049 |  |
| `D09_S03_testimony_completed` | (없음) | 1 | 0 | records.json:MS14_D09_S03_L0034 |  |
| `D09_S04_custody_night_completed` | (없음) | 1 | 0 | records.json:MS14_D09_S04_L0030 |  |
| `D09_S04_postal_completed` | (없음) | 1 | 0 | records.json:MS14_D09_S04_L0024 |  |
| `D09_S04_school_night_completed` | (없음) | 1 | 0 | records.json:MS14_D09_S04_L0036 |  |
| `D10_P01_authority_answer_completed` | (없음) | 1 | 0 | records.json:MS14_D10_P01_L0025 |  |
| `D10_P01_authority_question_completed` | (없음) | 1 | 0 | records.json:MS14_D10_P01_L0018 |  |
| `D10_P01_family_delivery_completed` | (없음) | 1 | 0 | records.json:MS14_D10_P01_L0083 |  |
| `D10_P01_pocket_challenge_completed` | (없음) | 1 | 0 | records.json:MS14_D10_P01_L0055 |  |
| `D10_P01_pocket_question_completed` | (없음) | 1 | 0 | records.json:MS14_D10_P01_L0048 |  |
| `D10_P01_private_count_completed` | (없음) | 1 | 0 | records.json:MS14_D10_P01_L0069 |  |
| `D10_P01_stop_handover_completed` | (없음) | 1 | 0 | records.json:MS14_D10_P01_L0014 |  |
| `D10_P01_writing_answer_completed` | (없음) | 1 | 0 | records.json:MS14_D10_P01_L0042 |  |
| `D10_P01_writing_question_completed` | (없음) | 1 | 0 | records.json:MS14_D10_P01_L0030 |  |
| `D10_S01_main_completed` | (없음) | 1 | 1 | records.json:MS14_D10_S01_L0019 | room13_v111_later_bindings.rpy:136 |
| `D10_S02_opening_completed` | (없음) | 1 | 0 | records.json:MS14_D10_S02_L0010 |  |
| `D10_S02_second_door_completed` | (없음) | 1 | 1 | records.json:MS14_D10_S02_L0046 | room13_v111_later_bindings.rpy:137 |
| `D10_S02_two_wounds_completed` | (없음) | 1 | 1 | records.json:MS14_D10_S02_L0033 | room13_v111_days610.rpy:1522 |
| `D10_S03_contact_limit_completed` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0059 |  |
| `D10_S03_entry_admission_completed` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0044 |  |
| `D10_S03_owner_copy_completed` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0017 |  |
| `D10_S03_owner_question_completed` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0004 |  |
| `D10_S03_owner_tok_completed` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0013 |  |
| `D10_S03_time_answer_completed` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0036 |  |
| `D10_S03_time_question_completed` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0022 |  |
| `D10_S04P_main_completed` | (없음) | 1 | 0 | records.json:MS14_D10_S04P_L0005 |  |
| `D10_S04_main_completed` | (없음) | 1 | 0 | records.json:MS14_D10_S04_L0027 |  |
| `D10_confrontation_release_completed` | (없음) | 1 | 1 | records.json:MS14_D10_S03_L0088 | room13_v111_later_bindings.rpy:138 |
| `D10_contact_limit_completed` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0059 |  |
| `DARAM_DETAINED` | false | 9 | 13 | room13_v111_owl_prevent.rpy:93 | room13_v111.rpy:111 |
| `DARAM_guardian` | (없음) | 1 | 0 | records.json:MS14_D07_S03_L0031 |  |
| `DARAM_location` | (없음) | 6 | 5 | room13_v111_days1114.rpy:1270 | room13_v111.rpy:184 |
| `DOTO_location` | (없음) | 1 | 0 | records.json:MS14_D07_S03_L0031 |  |
| `DOTO_view_scope` | (없음) | 1 | 0 | records.json:MS14_D08_S02_L0037 |  |
| `E01.variant` | (없음) | 1 | 0 | records.json:MS14_D01_S01_L0010 |  |
| `E02.variant` | (없음) | 1 | 0 | records.json:MS14_D01_S02_L0019 |  |
| `E03.variant` | (없음) | 1 | 0 | records.json:MS14_D01_S03_L0002 |  |
| `E04.variant` | (없음) | 1 | 0 | records.json:MS14_D01_S03_L0007 |  |
| `E05.variant` | (없음) | 2 | 0 | room13_v111_days123.rpy:296 |  |
| `E06.variant` | (없음) | 1 | 0 | records.json:MS14_D01_S05_L0019 |  |
| `E06_CONTACT` | (없음) | 1 | 0 | records.json:MS14_D06_S01_L0048 |  |
| `E06_CONTACT.variant` | (없음) | 1 | 0 | records.json:MS14_D06_S01_L0048 |  |
| `E06_EMPTY.variant` | (없음) | 1 | 0 | records.json:MS14_D06_S04_L0030 |  |
| `E06_FIRE` | (없음) | 1 | 0 | records.json:MS14_D06_S04_L0037 |  |
| `E06_FIRE.variant` | (없음) | 1 | 0 | records.json:MS14_D06_S04_L0037 |  |
| `E06_RESCUE.variant` | (없음) | 1 | 0 | records.json:MS14_D06_S04_L0027 |  |
| `E07.variant` | (없음) | 1 | 0 | records.json:MS14_D02_S02_L0005 |  |
| `E07_NUBI.variant` | (없음) | 1 | 0 | records.json:MS14_D07_S01_L0045 |  |
| `E07_OWL_CONTACT` | (없음) | 1 | 0 | records.json:MS14_D07_S02_L0046 |  |
| `E08.variant` | (없음) | 1 | 0 | records.json:MS14_D02_S03_L0025 |  |
| `E08_CHILD_ACCOUNT` | (없음) | 1 | 0 | records.json:MS14_D08_S01_L0025 |  |
| `E08_CHILD_ACCOUNT.variant` | (없음) | 1 | 0 | records.json:MS14_D08_S01_L0025 |  |
| `E08_CHILD_POSITION` | (없음) | 1 | 0 | records.json:MS14_D08_S02_L0037 |  |
| `E08_CHILD_POSITION.variant` | (없음) | 1 | 0 | records.json:MS14_D08_S02_L0037 |  |
| `E08_CONTACT_ASSEMBLY` | (없음) | 1 | 0 | records.json:MS14_D08_S03_L0028 |  |
| `E08_CONTACT_ASSEMBLY.variant` | (없음) | 1 | 0 | records.json:MS14_D08_S03_L0028 |  |
| `E08_RECENT_LETTER` | (없음) | 1 | 0 | records.json:MS14_D08_S04_L0033 |  |
| `E08_RECENT_LETTER.variant` | (없음) | 1 | 0 | records.json:MS14_D08_S04_L0033 |  |
| `E08_ROOM` | (없음) | 1 | 0 | records.json:MS14_D08_S02_L0037 |  |
| `E08_ROOM.variant` | (없음) | 1 | 0 | records.json:MS14_D08_S02_L0037 |  |
| `E08_ROOM_REACH` | (없음) | 1 | 0 | records.json:MS14_D08_S02_L0037 |  |
| `E08_ROOM_REACH.variant` | (없음) | 1 | 0 | records.json:MS14_D08_S02_L0037 |  |
| `E08_TOOL` | (없음) | 1 | 0 | records.json:MS14_D08_S03_L0028 |  |
| `E08_TOOL.variant` | (없음) | 1 | 0 | records.json:MS14_D08_S03_L0028 |  |
| `E08_WOUND_WIRE` | (없음) | 1 | 0 | records.json:MS14_D08_S03_L0028 |  |
| `E08_WOUND_WIRE.variant` | (없음) | 1 | 0 | records.json:MS14_D08_S03_L0028 |  |
| `E08_prevention_experience` | (없음) | 2 | 0 | records.json:MS14_D08_P01_L0010 |  |
| `E09.variant` | (없음) | 2 | 1 | records.json:MS14_D03_S01_L0021 | room13_v111.rpy:589 |
| `E09_MAIL` | (없음) | 1 | 0 | records.json:MS14_D09_S04_L0024 |  |
| `E09_MAIL.variant` | (없음) | 1 | 0 | records.json:MS14_D09_S04_L0024 |  |
| `E09_PASSAGE` | (없음) | 2 | 1 | records.json:MS14_D09_S01_L0014 | room13_navigation.rpy:102 |
| `E09_PASSAGE.variant` | (없음) | 2 | 0 | records.json:MS14_D09_S01_L0014 |  |
| `E09_PIN_HANDOVER_TIME` | (없음) | 1 | 0 | records.json:MS14_D09_S03_L0034 |  |
| `E09_PIN_HANDOVER_TIME.variant` | (없음) | 1 | 0 | records.json:MS14_D09_S03_L0034 |  |
| `E09_PIN_OWNER` | (없음) | 2 | 0 | records.json:MS14_D09_S02_L0018 |  |
| `E09_PIN_OWNER.variant` | (없음) | 2 | 0 | records.json:MS14_D09_S02_L0018 |  |
| `E09_PIN_TIME` | (없음) | 1 | 0 | records.json:MS14_D09_S03_L0034 |  |
| `E09_PIN_TIME.variant` | (없음) | 1 | 0 | records.json:MS14_D09_S03_L0034 |  |
| `E09_SCARF` | (없음) | 1 | 0 | records.json:MS14_D09_S03_L0049 |  |
| `E09_SCARF.variant` | (없음) | 1 | 0 | records.json:MS14_D09_S03_L0049 |  |
| `E10.variant` | (없음) | 1 | 0 | records.json:MS14_D03_S02_L0012 |  |
| `E10_PUMP` | (없음) | 2 | 0 | records.json:MS14_D10_S04_L0027 |  |
| `E10_PUMP.variant` | (없음) | 2 | 0 | records.json:MS14_D10_S04_L0027 |  |
| `E11.variant` | (없음) | 1 | 0 | records.json:MS14_D03_S02_L0027 |  |
| `E12.variant` | (없음) | 1 | 0 | records.json:MS14_D03_S03_L0008 |  |
| `E13.variant` | (없음) | 1 | 0 | records.json:MS14_D03_S03_L0027 |  |
| `E14.variant` | (없음) | 1 | 0 | records.json:MS14_D03_S04_L0009 |  |
| `E15.variant` | (없음) | 1 | 0 | records.json:MS14_D03_S04_L0028 |  |
| `E16.variant` | (없음) | 1 | 0 | records.json:MS14_D03_S04_L0032 |  |
| `E17.variant` | (없음) | 1 | 0 | records.json:MS14_D03_S05_L0018 |  |
| `E18.variant` | (없음) | 1 | 0 | records.json:MS14_D04_S01_L0050 |  |
| `E19.variant` | (없음) | 1 | 0 | records.json:MS14_D04_S02_L0025 |  |
| `E20.variant` | (없음) | 1 | 0 | records.json:MS14_D04_S03_L0003 |  |
| `E21.variant` | (없음) | 1 | 0 | records.json:MS14_D04_S04_L0018 |  |
| `E22.variant` | (없음) | 1 | 0 | records.json:MS14_D04_S04_L0044 |  |
| `E23.variant` | (없음) | 1 | 0 | records.json:MS14_D05_S02_L0016 |  |
| `E24.status` | (없음) | 2 | 0 | records.json:MS14_D05_S01_L0024 |  |
| `E24.variant` | (없음) | 1 | 0 | records.json:MS14_D05_S02_L0025 |  |
| `E25.variant` | (없음) | 1 | 0 | records.json:MS14_D05_S03_L0037 |  |
| `E26.variant` | (없음) | 1 | 0 | records.json:MS14_D05_S03_L0037 |  |
| `E27.variant` | (없음) | 1 | 0 | records.json:MS14_D05_S04_L0005 |  |
| `E28.handed_to` | (없음) | 1 | 0 | records.json:MS14_D05_S04_L9501 |  |
| `E28.variant` | (없음) | 1 | 0 | records.json:MS14_D05_S04_L0027 |  |
| `E29.variant` | (없음) | 1 | 0 | records.json:MS14_D05_S05_L0027 |  |
| `E30.variant` | (없음) | 1 | 0 | records.json:MS14_D01_S05_L0022 |  |
| `E31.variant` | (없음) | 2 | 0 | records.json:MS14_D02_S04_L0083 |  |
| `E32.variant` | (없음) | 1 | 0 | records.json:MS14_D03_S02_L0016 |  |
| `E33.variant` | (없음) | 1 | 0 | records.json:MS14_D03_S05_L0018 |  |
| `E34.variant` | (없음) | 1 | 0 | records.json:MS14_D04_S01_L0015 |  |
| `E35.status` | (없음) | 1 | 1 | records.json:MS14_D03_S06_L0041 | room13_v111.rpy:605 |
| `E35.variant` | (없음) | 1 | 0 | records.json:MS14_D02_S04_L0083 |  |
| `FAMILY_BASE` | (없음) | 3 | 0 | records.json:MS14_D07_S02_L0029 |  |
| `FIRE_EVACUATED` | (없음) | 3 | 10 | records.json:MS14_D06_S02_L0033 | room13_v111_days610.rpy:345 |
| `K01a` | false | 2 | 2 | records.json:MS14_D01_S01_L0015 | room13_v111_days123.rpy:35 |
| `K01b` | false | 2 | 2 | records.json:MS14_D01_S01_L0016 | room13_v111_days123.rpy:35 |
| `K05` | false | 2 | 0 | records.json:MS14_D01_S03_L0031 |  |
| `KKOMI_ALIVE` | true | 4 | 8 | room13_v111_days1114.rpy:1316 | room13_v111_days1114.rpy:1314 |
| `Kkaro_forced_transport_refused` | (없음) | 2 | 2 | room13_v111_days1114.rpy:2504 | room13_v111.rpy:90 |
| `NABI_relationship` | (없음) | 0 | 1 |  | room13_v111_days610.rpy:1222 |
| `NUBI_CHILDREN_location` | (없음) | 2 | 0 | records.json:MS14_D07_S01_L0024 |  |
| `NUBI_CHILDREN_school_care` | (없음) | 1 | 0 | records.json:MS14_D07_S02_L0029 |  |
| `NUBI_admitted_setting_fire` | (없음) | 1 | 1 | records.json:MS14_D07_S01_L0045 | room13_v111_later_bindings.rpy:124 |
| `NUBI_intent_to_kill` | (없음) | 1 | 0 | records.json:MS14_D07_S01_L0045 |  |
| `OWL_ALIVE` | true | 8 | 18 | room13_v111_owl_prevent.rpy:92 | room13_v111_days1114.rpy:331 |
| `OWL_claim_no_separate_page` | (없음) | 1 | 0 | records.json:MS14_D09_P01_L0027 |  |
| `TOK_ALIVE` | true | 0 | 3 |  | room13_v111_later_bindings.rpy:63 |
| `TTADAK_ALIVE` | (없음) | 2 | 0 | records.json:MS14_D09_S01_L0014 |  |
| `acorn_recovered` | (없음) | 2 | 5 | room13_v111_days610.rpy:154 | room13_v111_days610.rpy:159 |
| `actual_stop_actor_refuses_transport` | (없음) | 2 | 1 | room13_v111_days1114.rpy:2485 | room13_v111.rpy:88 |
| `adult_interview_done` | (없음) | 2 | 2 | room13_v111_days1114.rpy:3312 | room13_v111_days1114.rpy:3329 |
| `afternoon_visit_declined` | false | 1 | 0 | records.json:MS14_D04_S02_L0031 |  |
| `alive:kid_dodam` | (없음) | 1 | 0 | records.json:MS14_D12_S05_L0043 |  |
| `alive:kid_saemi` | (없음) | 1 | 0 | records.json:MS14_D12_S05_L0043 |  |
| `alive:nabi` | (없음) | 0 | 2 |  | room13_hidden_pandol.rpy:13 |
| `alive:neoul` | (없음) | 2 | 0 | room13_v111_days1114.rpy:2687 |  |
| `alive:resident_kongi` | (없음) | 0 | 1 |  | room13_v111_days610.rpy:40 |
| `alive:resident_momo` | (없음) | 1 | 0 | room13_v111_days1114.rpy:2729 |  |
| `alive:v111_lowerroad_elder` | (없음) | 2 | 2 | room13_v111_days1114.rpy:950 | room13_v111_days1114.rpy:1046 |
| `all_cart_handed` | (없음) | 1 | 3 | room13_v111_days1114.rpy:2364 | room13_v111_later_bindings.rpy:157 |
| `altar1_half_asked` | (없음) | 1 | 1 | room13_v111_newworld_rules.rpy:342 | room13_v111_newworld_rules.rpy:339 |
| `altar_guide_confirmed` | (없음) | 1 | 2 | room13_v111_days1114.rpy:2874 | room13_navigation.rpy:101 |
| `altar_half1` | (없음) | 1 | 0 | room13_v111_days1114.rpy:2931 |  |
| `altar_heat_structure_observed` | (없음) | 1 | 0 | room13_v111_days1114.rpy:2895 |  |
| `altar_issue:*` | (없음) | 0 | 1 |  | room13_v111_days1114.rpy:3033 |
| `altar_issue:1` | (없음) | 2 | 0 | room13_v111_days1114.rpy:2932 |  |
| `altar_issue:2` | (없음) | 3 | 0 | room13_v111_days1114.rpy:2957 |  |
| `altar_issue:3` | (없음) | 3 | 0 | room13_v111_days1114.rpy:2985 |  |
| `altar_issue:4` | (없음) | 3 | 0 | room13_v111_days1114.rpy:3013 |  |
| `arrival_note_sent` | (없음) | 1 | 0 | records.json:MS14_D02_S01_L0039 |  |
| `badugi.location` | (없음) | 1 | 0 | records.json:MS14_D05_S05_L9502 |  |
| `bami_cold4` | (없음) | 1 | 4 | room13_v111_days45.rpy:134 | room13_v111_days45.rpy:133 |
| `bami_status` | free | 4 | 2 | room13_v111_days45.rpy:499 | room13_v111_days610.rpy:38 |
| `bomi_death_confirmed` | (없음) | 2 | 1 | room13_v111_days1114.rpy:3311 | room13_v111_later_bindings.rpy:161 |
| `book_promise12` | (없음) | 1 | 1 | room13_v111_days1114.rpy:1611 | room13_v111_days1114.rpy:1803 |
| `bori_nubi_door_witness_heard` | (없음) | 1 | 2 | room13_v111_days610.rpy:532 | room13_v111_days610.rpy:556 |
| `bottle_original_seal_seen` | (없음) | 1 | 0 | room13_v111_days1114.rpy:1193 |  |
| `bowls_carried12` | (없음) | 1 | 2 | room13_v111_days1114.rpy:1184 | room13_v111_days1114.rpy:1387 |
| `box_rechecked_day2` | false | 2 | 0 | records.json:MS14_D02_S04_L0038 |  |
| `buri_device_consent` | (없음) | 1 | 3 | room13_v111_days1114.rpy:2550 | room13_v111_days1114.rpy:3051 |
| `buri_device_present` | (없음) | 1 | 3 | room13_v111_days1114.rpy:3089 | room13_v111.rpy:102 |
| `buri_supply_participated` | (없음) | 0 | 1 |  | room13_v111_days1114.rpy:3230 |
| `busy:*` | (없음) | 1 | 2 | room13_v111_days1114.rpy:3206 | room13_v111.rpy:169 |
| `busy:buri` | (없음) | 2 | 0 | room13_v111_days1114.rpy:3188 |  |
| `busy:guard` | (없음) | 5 | 7 | room13_v111_days1114.rpy:10 | room13_v111.rpy:82 |
| `busy:karo` | (없음) | 11 | 1 | room13_v111_days1114.rpy:1135 | room13_v111_days1114.rpy:2168 |
| `busy:mom` | (없음) | 4 | 3 | room13_v111_days1114.rpy:2180 | room13_v111.rpy:183 |
| `busy:nabi` | (없음) | 2 | 2 | room13_v111_days1114.rpy:1280 | room13_v111.rpy:184 |
| `busy:neoul` | (없음) | 1 | 2 | room13_v111_days1114.rpy:2410 | room13_v111.rpy:97 |
| `busy:resident_badook` | (없음) | 3 | 0 | room13_v111_days1114.rpy:2091 |  |
| `busy:resident_bori` | (없음) | 3 | 0 | room13_v111_days1114.rpy:1324 |  |
| `busy:resident_nero` | (없음) | 1 | 1 | room13_v111_days1114.rpy:2211 | room13_v111_days1114.rpy:2170 |
| `busy:resident_tok` | (없음) | 2 | 2 | room13_v111_owl_prevent.rpy:14 | room13_v111_owl_prevent.rpy:11 |
| `busy:v111_patrol` | (없음) | 1 | 1 | room13_v111_days1114.rpy:1848 | room13_v111_days1114.rpy:3195 |
| `carried_dry_blankets` | 0 | 3 | 13 | records.json:MS14_D02_S04_L0083 | room13_v111_days1114.rpy:203 |
| `carrier_arrived` | (없음) | 1 | 3 | room13_v111_days1114.rpy:1134 | room13_v111_newworld_text.rpy:112 |
| `cart_departed` | (없음) | 1 | 4 | room13_v111_days1114.rpy:2018 | room13_v111_days1114.rpy:3466 |
| `cart_returned` | (없음) | 1 | 1 | room13_v111_days1114.rpy:2516 | room13_v111.rpy:91 |
| `cart_roster` | (없음) | 5 | 10 | room13_v111_days1114.rpy:2044 | room13_v111_days1114.rpy:2009 |
| `cart_stopped` | (없음) | 2 | 2 | room13_v111_days1114.rpy:2083 | room13_v111_later_bindings.rpy:157 |
| `child_upper_reuse` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0059 |  |
| `child_upper_reuse_after_pin_refasten` | (없음) | 1 | 0 | records.json:MS14_D10_S02_L0033 |  |
| `choice:MS14_D06_S01` | (없음) | 2 | 1 | room13_v111_days610.rpy:46 | room13_v111_newworld_text.rpy:100 |
| `choice:MS14_D06_S02` | (없음) | 2 | 0 | room13_v111_days610.rpy:165 |  |
| `choice:MS14_D07_S01` | (없음) | 2 | 0 | room13_v111_days610.rpy:470 |  |
| `choice:MS14_D07_S03` | (없음) | 4 | 0 | room13_v111_days610.rpy:762 |  |
| `command_confrontation_done` | (없음) | 2 | 0 | room13_v111_days1114.rpy:3171 |  |
| `cookie.location` | (없음) | 3 | 0 | room13_v111_days610.rpy:14 |  |
| `crowd_blocked_by_dad` | (없음) | 1 | 1 | room13_v111_days1114.rpy:2686 | room13_v111_newworld_text.rpy:167 |
| `crowd_cart_spaced13` | (없음) | 1 | 1 | room13_v111_days1114.rpy:2620 | field-bindings.json:crowd_prepare13 |
| `crowd_injury` | (없음) | 6 | 6 | room13_v111_days1114.rpy:2689 | room13_v111_days1114.rpy:3604 |
| `crowd_intervention` | (없음) | 5 | 2 | room13_v111_days1114.rpy:2690 | room13_v111_days1114.rpy:3542 |
| `crowd_preparation_schema13` | (없음) | 1 | 7 | room13_v111_days1114.rpy:2610 | room13_v111_days1114.rpy:2639 |
| `crowd_record_read` | (없음) | 1 | 0 | room13_v111_grand_win.rpy:131 |  |
| `crowd_records_spaced13` | (없음) | 1 | 1 | room13_v111_days1114.rpy:2617 | field-bindings.json:crowd_prepare13 |
| `crowd_resolution_done` | (없음) | 6 | 1 | room13_v111_days1114.rpy:2688 | room13_v111_days1114.rpy:2247 |
| `crowd_supervisor_placed13` | (없음) | 2 | 1 | room13_v111_days1114.rpy:11 | field-bindings.json:crowd_prepare13 |
| `crowd_witnessed` | (없음) | 1 | 1 | room13_v111_days1114.rpy:2675 | room13_v111_days1114.rpy:3538 |
| `current_order_execution_stopped` | (없음) | 2 | 2 | room13_v111_days1114.rpy:2493 | room13_v111.rpy:89 |
| `current_sacrifice_operation_closed` | (없음) | 2 | 0 | room13_v111_days1114.rpy:3390 |  |
| `current_transport_chain_stopped` | (없음) | 1 | 2 | room13_v111_days1114.rpy:2554 | room13_v111_days1114.rpy:3390 |
| `d4_bucket_seen` | false | 1 | 0 | room13_v111_days45.rpy:298 |  |
| `d4_fence_seen` | false | 1 | 0 | room13_v111_days45.rpy:282 |  |
| `d4_tracks_seen` | false | 1 | 0 | room13_v111_days45.rpy:290 |  |
| `dallae_first_victim_known` | (없음) | 1 | 1 | room13_v111_days1114.rpy:3029 | room13_v111_days1114.rpy:3035 |
| `daram_deal_freed` | (없음) | 1 | 2 | room13_v111_days1114.rpy:1917 | room13_v111_newworld_text.rpy:243 |
| `daram_door_asked9` | (없음) | 1 | 1 | room13_v111_days610.rpy:1121 | room13_v111_days610.rpy:1120 |
| `daram_fever12` | (없음) | 1 | 6 | room13_v111_days1114.rpy:1067 | room13_v111_days1114.rpy:1066 |
| `daram_hello:*` | (없음) | 1 | 1 | room13_v111_idle.rpy:203 | room13_v111_idle.rpy:199 |
| `daram_hello_count` | (없음) | 1 | 1 | room13_v111_idle.rpy:205 | room13_v111_idle.rpy:204 |
| `daram_next_morning_guard` | (없음) | 1 | 0 | records.json:MS14_D05_S05_L0027 |  |
| `daram_release_basis` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0088 |  |
| `day` | 1 | 11 | 0 | room13_v111_days1114.rpy:1019 |  |
| `departed:*` | (없음) | 1 | 6 | room13_v111_days1114.rpy:2016 | room13_v111_days1114.rpy:20 |
| `departed:daram` | (없음) | 0 | 1 |  | room13_v111_newworld_rules.rpy:267 |
| `departed:guard` | (없음) | 0 | 2 |  | room13_v111_days1114.rpy:4 |
| `departed:karo` | (없음) | 0 | 1 |  | room13_v111_days1114.rpy:18 |
| `departed:nabi` | (없음) | 0 | 3 |  | room13_hidden_pandol.rpy:13 |
| `departed:npc_pandol` | (없음) | 0 | 2 |  | room13_hidden_pandol.rpy:13 |
| `departed:resident_owlgp` | (없음) | 0 | 1 |  | room13_v111_newworld_text.rpy:155 |
| `departed:resident_teacher` | (없음) | 0 | 1 |  | room13_v111_days1114.rpy:472 |
| `departed:resident_tok` | (없음) | 0 | 1 |  | room13_v111_owl_prevent.rpy:11 |
| `departed_names` | (없음) | 1 | 2 | room13_v111_days1114.rpy:2015 | room13_v111_newworld_rules.rpy:262 |
| `departed_unrescued` | (없음) | 1 | 0 | room13_v111_days1114.rpy:2583 |  |
| `device_detached` | (없음) | 1 | 0 | room13_v111_days1114.rpy:3186 |  |
| `device_joint_control` | (없음) | 1 | 2 | room13_v111_days1114.rpy:3225 | room13_v111_days1114.rpy:3390 |
| `device_record_kind` | (없음) | 2 | 1 | room13_v111_days1114.rpy:3131 | room13_v111_days1114.rpy:3230 |
| `device_record_shown` | (없음) | 2 | 0 | room13_v111_days1114.rpy:3136 |  |
| `device_support_ready` | (없음) | 2 | 0 | room13_v111_days1114.rpy:3156 |  |
| `dodam_spoon12` | (없음) | 1 | 1 | room13_v111_days1114.rpy:1171 | room13_v111_newworld_text.rpy:153 |
| `dodam_spoon7` | (없음) | 1 | 2 | room13_v111_days610.rpy:696 | room13_v111_days1114.rpy:1171 |
| `dolmok.location` | (없음) | 1 | 0 | records.json:MS14_D04_S03_L0020 |  |
| `doto_promise7` | (없음) | 1 | 2 | room13_v111_owl_prevent.rpy:58 | room13_v111_days610.rpy:756 |
| `elapsed_minutes` | (없음) | 2 | 2 | room13_hidden_base.rpy:24 | room13_hidden_base.rpy:18 |
| `ending14` | (없음) | 3 | 20 | room13_v111_days1114.rpy:2797 | room13_hidden_base.rpy:11 |
| `escort_gear_returned` | (없음) | 1 | 0 | room13_v111_days1114.rpy:2517 |  |
| `evacuation_requested` | (없음) | 2 | 1 | room13_v111_days610.rpy:178 | room13_v111_later_bindings.rpy:120 |
| `false_message_admitted` | (없음) | 1 | 3 | room13_v111_days1114.rpy:1997 | room13_v111_days1114.rpy:2247 |
| `family_benefits_received` | (없음) | 1 | 0 | room13_v111_days1114.rpy:2580 |  |
| `family_blankets_not_donated` | (없음) | 1 | 0 | records.json:MS14_D06_S01_L0016 |  |
| `family_deal` | (없음) | 2 | 2 | room13_v111_days1114.rpy:1914 | room13_v111_later_bindings.rpy:154 |
| `family_location` | (없음) | 5 | 7 | room13_v111_days1114.rpy:2177 | room13_v111_days1114.rpy:2277 |
| `family_offer_terms_seen` | (없음) | 1 | 1 | room13_v111_days1114.rpy:1908 | room13_v111_days1114.rpy:1897 |
| `family_reunited` | (없음) | 1 | 8 | room13_v111_days1114.rpy:179 | room13_v111.rpy:476 |
| `family_safety_changed` | false | 1 | 0 | records.json:MS14_D05_S05_L0038 |  |
| `family_school_place` | (없음) | 2 | 3 | room13_v111_days1114.rpy:444 | room13_v111_days1114.rpy:536 |
| `fatal_contact_assembly` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0059 |  |
| `fatal_contact_responsibility` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0088 |  |
| `fate:*` | (없음) | 1 | 1 | room13_fork_screen.rpy:63 | room13_fork_screen.rpy:62 |
| `fate:fate_soup` | (없음) | 0 | 1 |  | room13_v111_newworld_text.rpy:460 |
| `father_and_daram_together` | (없음) | 1 | 0 | records.json:MS14_D07_S03_L0022 |  |
| `father_knows_attack_scene` | (없음) | 1 | 0 | records.json:MS14_D07_S04_L0036 |  |
| `father_location` | (없음) | 2 | 0 | records.json:MS14_D07_S03_L0019 |  |
| `fire_first_question` | (없음) | 3 | 0 | room13_v111_days610.rpy:560 |  |
| `fire_neoul_promise_recorded` | (없음) | 1 | 0 | room13_v111_days610.rpy:629 |  |
| `fire_result` | (없음) | 1 | 0 | records.json:MS14_D06_S03P_L0008 |  |
| `followup_heard:*` | (없음) | 1 | 2 | room13_v111_reactions.rpy:112 | room13_v111_reactions.rpy:74 |
| `followup_read:*` | (없음) | 1 | 1 | room13_v111_reactions.rpy:92 | room13_v111_reactions.rpy:74 |
| `followup_read:NW_RX_F007` | (없음) | 0 | 1 |  | room13_v111_newworld_text.rpy:225 |
| `forgery_confirmed` | (없음) | 1 | 2 | room13_v111_days610.rpy:1642 | room13_v111_days1114.rpy:329 |
| `gate_basis_proven` | false | 2 | 1 | records.json:MS14_D01_S03_L0019 | room13_v111_newworld_rules.rpy:9 |
| `gate_daram_unlisted` | (없음) | 2 | 5 | room13_v111_days123.rpy:260 | room13_v111_days123.rpy:295 |
| `gate_hardened` | (없음) | 1 | 1 | room13_v111_days123.rpy:257 | room13_v111.rpy:441 |
| `gate_lodging_retired` | (없음) | 0 | 1 |  | field-bindings.json:gate_investigate |
| `gate_mother_report_instruction_heard` | (없음) | 1 | 0 | records.json:MS14_D01_S04_L0020 |  |
| `gate_post_cold_cost` | (없음) | 1 | 1 | room13_v111_days45.rpy:488 | room13_v111_days45.rpy:487 |
| `gate_registered` | false | 1 | 0 | records.json:MS14_D01_S04_L0008 |  |
| `grand:*` | (없음) | 0 | 2 |  | room13_fork_screen.rpy:56 |
| `grand:fire` | (없음) | 1 | 3 | room13_v111_days610.rpy:632 | room13_v111_newworld_rules.rpy:281 |
| `grand:soup` | (없음) | 2 | 5 | room13_v111_days1114.rpy:1561 | room13_v111_newworld_rules.rpy:281 |
| `grand_bowl_pocket` | (없음) | 1 | 4 | room13_v111_grand_win.rpy:85 | room13_v111_days1114.rpy:1751 |
| `grand_bowl_seen11` | (없음) | 1 | 1 | room13_v111_grand_win.rpy:80 | field-bindings.json:rescue_cart11 |
| `grand_laundry_seen5` | (없음) | 1 | 3 | room13_v111_grand_win.rpy:57 | room13_v111_newworld_text.rpy:326 |
| `grand_snack_given7` | (없음) | 1 | 1 | room13_v111_grand_win.rpy:67 | room13_v111_days610.rpy:501 |
| `grand_snack_ready7` | (없음) | 2 | 1 | room13_v111_days610.rpy:501 | field-bindings.json:nubi_children_receipt7 |
| `grand_ticket_spot_kid` | (없음) | 1 | 1 | room13_v111_grand_win.rpy:68 | room13_v111_newworld_text.rpy:327 |
| `grand_ticket_spot_known` | (없음) | 2 | 2 | room13_v111_grand_win.rpy:58 | room13_v111_days610.rpy:501 |
| `grandmother_custody` | free | 1 | 2 | room13_v111_days610.rpy:1641 | room13_v111.rpy:174 |
| `grandmother_kitchen_move` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0036 |  |
| `grandmother_leaves_for_kitchen_after_child_guard_started` | (없음) | 1 | 0 | records.json:MS14_D09_S03_L0034 |  |
| `grandmother_passage_entry` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0044 |  |
| `grandmother_records_confrontation` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0088 |  |
| `grandmother_wrapped_upper_piece` | (없음) | 1 | 0 | records.json:MS14_D09_S03_L0049 |  |
| `greenhouse_address_known` | (없음) | 1 | 2 | room13_v111_days1114.rpy:87 | room13_navigation.rpy:100 |
| `greeted:*:*` | (없음) | 4 | 3 | room13_v111_idle.rpy:60 | room13_v111_idle.rpy:59 |
| `greeted_count:*` | (없음) | 1 | 1 | room13_v111_idle.rpy:62 | room13_v111_idle.rpy:61 |
| `guard_relief_person` | (없음) | 1 | 3 | room13_v111_days1114.rpy:3195 | room13_v111.rpy:103 |
| `guldol_facility_seen` | (없음) | 1 | 1 | room13_v111_days1114.rpy:364 | room13_v111_days1114.rpy:844 |
| `handed:*` | (없음) | 3 | 9 | room13_v111_days1114.rpy:2358 | room13_v111_days1114.rpy:2014 |
| `handed:daram` | (없음) | 2 | 3 | room13_v111_days1114.rpy:2090 | room13_v111_days1114.rpy:2088 |
| `handed:nabi` | (없음) | 1 | 1 | room13_v111_days1114.rpy:2255 | room13_v111_days1114.rpy:2252 |
| `handed:npc_pandol` | (없음) | 1 | 0 | room13_v111_days1114.rpy:2288 |  |
| `handed:resident_guldol` | (없음) | 1 | 0 | room13_v111_days1114.rpy:2338 |  |
| `handed:resident_momo` | (없음) | 1 | 1 | room13_v111_days1114.rpy:2313 | room13_v111_days1114.rpy:2725 |
| `handed:resident_siluk` | (없음) | 1 | 1 | room13_v111_days1114.rpy:2458 | room13_v111_days1114.rpy:2348 |
| `handed:resident_teacher` | (없음) | 1 | 1 | room13_v111_days1114.rpy:2408 | room13_v111_days1114.rpy:2346 |
| `handover_prepared13` | (없음) | 1 | 1 | room13_v111_days1114.rpy:2269 | room13_v111_days1114.rpy:2243 |
| `heard_inn_order1` | (없음) | 1 | 1 | room13_v111_days123.rpy:323 | room13_v111_newworld_text.rpy:226 |
| `heat_box_received` | (없음) | 1 | 1 | room13_v111_days1114.rpy:1297 | room13_v111_newworld_text.rpy:254 |
| `heat_inventory_observed` | (없음) | 1 | 0 | room13_v111_days1114.rpy:409 |  |
| `hidden_base:*` | (없음) | 0 | 1 |  | room13_hidden_base.rpy:5 |
| `hidden_base:aligned` | (없음) | 2 | 0 | room13_hidden_base.rpy:105 |  |
| `hidden_base:entered` | (없음) | 1 | 0 | room13_hidden_base.rpy:86 |  |
| `hidden_base:finished` | (없음) | 2 | 0 | room13_hidden_base.rpy:83 |  |
| `hidden_base:frame_seen` | (없음) | 1 | 1 | room13_hidden_base.rpy:99 | field-bindings.json:hidden_base_door14 |
| `hidden_base:marks_copied` | (없음) | 1 | 1 | room13_hidden_base.rpy:70 | field-bindings.json:heat_check11 |
| `hidden_base:notebook_taken` | (없음) | 2 | 0 | room13_hidden_base.rpy:131 |  |
| `hidden_base:opened` | (없음) | 1 | 0 | room13_hidden_base.rpy:112 |  |
| `hidden_base:paper` | (없음) | 1 | 2 | room13_hidden_base.rpy:54 | field-bindings.json:bundle_open |
| `hidden_base:paper_set` | (없음) | 1 | 1 | room13_hidden_base.rpy:102 | field-bindings.json:hidden_base_door14 |
| `hidden_base:plate` | (없음) | 1 | 2 | room13_hidden_base.rpy:63 | field-bindings.json:heat_check11 |
| `hidden_base:plate_seen` | (없음) | 1 | 1 | room13_hidden_base.rpy:60 | field-bindings.json:free_day7 |
| `hidden_base:read_incident` | (없음) | 1 | 0 | room13_hidden_base.rpy:127 |  |
| `hidden_base:read_section` | (없음) | 1 | 0 | room13_hidden_base.rpy:124 |  |
| `hidden_base:return_context` | (없음) | 2 | 0 | room13_hidden_base.rpy:16 |  |
| `hidden_base:returned` | (없음) | 1 | 0 | room13_hidden_base.rpy:143 |  |
| `hidden_page_known` | (없음) | 1 | 0 | records.json:MS14_D09_P01_L0027 |  |
| `hidden_pandol:*` | (없음) | 1 | 1 | room13_hidden_pandol.rpy:7 | room13_hidden_pandol.rpy:5 |
| `hidden_pandol:care_handed` | (없음) | 0 | 1 |  | field-bindings.json:blanket_mend13 |
| `hidden_pandol:consent` | (없음) | 0 | 1 |  | field-bindings.json:hp_house11 |
| `hidden_pandol:family_seen` | (없음) | 0 | 2 |  | field-bindings.json:sleep11_input |
| `hidden_pandol:heat_replaced` | (없음) | 0 | 3 |  | field-bindings.json:blanket_mend13 |
| `hidden_pandol:met` | (없음) | 0 | 6 |  | room13_v111_newworld_text.rpy:73 |
| `hidden_pandol:pin_fitted` | (없음) | 0 | 1 |  | field-bindings.json:free_day7 |
| `hidden_pandol:pin_seen` | (없음) | 0 | 1 |  | field-bindings.json:free_day7 |
| `hidden_pandol:spoon_seen` | (없음) | 0 | 2 |  | field-bindings.json:free_day7 |
| `hidden_pandol:stove_seen` | (없음) | 0 | 1 |  | field-bindings.json:hp_house11 |
| `hidden_pandol:tongs` | (없음) | 0 | 1 |  | field-bindings.json:hp_house11 |
| `hidden_pandol:visit_allowed` | (없음) | 0 | 2 |  | room13_navigation.rpy:99 |
| `hidden_pandol:wood_delivered` | (없음) | 0 | 1 |  | field-bindings.json:hp_house11 |
| `hidden_pandol:wood_reserved` | (없음) | 0 | 2 |  | field-bindings.json:sleep11_input |
| `hyp_issue:*` | (없음) | 0 | 4 |  | room13_v111_days1114.rpy:834 |
| `hyp_issue:1` | (없음) | 2 | 3 | room13_v111_days1114.rpy:661 | room13_v111_newworld_text.rpy:235 |
| `hyp_issue:2` | (없음) | 2 | 1 | room13_v111_days1114.rpy:702 | room13_v111_newworld_text.rpy:236 |
| `hyp_issue:3` | (없음) | 2 | 1 | room13_v111_days1114.rpy:743 | room13_v111_newworld_text.rpy:237 |
| `hyp_issue:4` | (없음) | 2 | 1 | room13_v111_days1114.rpy:784 | room13_v111_newworld_text.rpy:238 |
| `idle_count` | (없음) | 1 | 1 | room13_v111_idle.rpy:72 | room13_v111_idle.rpy:71 |
| `inn_information_hub_risk_known` | false | 1 | 0 | records.json:MS14_D05_S04_L0027 |  |
| `interpretation.intentional_strike_vs_struggle_collision` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0088 |  |
| `invitation_current_authorization` | (없음) | 1 | 0 | records.json:MS14_D10_P01_L0042 |  |
| `kkomi_acorn10` | (없음) | 1 | 2 | room13_v111_days610.rpy:1890 | room13_v111_days610.rpy:1886 |
| `kkomi_can_seen6` | (없음) | 1 | 3 | room13_v111_days610.rpy:150 | room13_v111_newworld_text.rpy:156 |
| `kkomi_can_wait6` | (없음) | 1 | 1 | room13_v111_days610.rpy:162 | systems/room13_v111_goal.rpy:168 |
| `kkomi_seat6` | (없음) | 1 | 4 | room13_v111_days610.rpy:184 | room13_v111_days610.rpy:255 |
| `kkomi_soup_dead` | (없음) | 1 | 1 | room13_v111_days1114.rpy:1317 | room13_v111_days1114.rpy:1790 |
| `lamp_bound2` | (없음) | 1 | 13 | room13_lamp_attempt.rpy:15 | room13_v111.rpy:556 |
| `lamp_cord2` | (없음) | 1 | 2 | room13_lamp_attempt.rpy:9 | room13_lamp_attempt.rpy:13 |
| `lamp_field_done3` | (없음) | 1 | 1 | room13_lamp_attempt.rpy:35 | field-bindings.json:lamp_attempt_field3 |
| `lamp_knife_done3` | (없음) | 1 | 1 | room13_lamp_attempt.rpy:39 | field-bindings.json:lamp_attempt_field3 |
| `lamp_latch_seen2` | (없음) | 1 | 2 | room13_lamp_attempt.rpy:12 | room13_lamp_attempt.rpy:13 |
| `lamp_manager` | (없음) | 2 | 0 | room13_v111_days1114.rpy:3417 |  |
| `lamp_part_*` | (없음) | 0 | 1 |  | room13_v111_days123.rpy:603 |
| `lamp_part_0` | false | 0 | 1 |  | field-bindings.json:lamp_observe |
| `lamp_part_1` | false | 0 | 1 |  | field-bindings.json:lamp_observe |
| `lamp_part_2` | false | 0 | 1 |  | field-bindings.json:lamp_observe |
| `lamp_part_3` | false | 0 | 1 |  | field-bindings.json:lamp_observe |
| `lamp_prep_done2` | (없음) | 1 | 1 | room13_lamp_attempt.rpy:5 | room13_v111_days123.rpy:812 |
| `lamp_store_done3` | (없음) | 1 | 1 | room13_lamp_attempt.rpy:45 | field-bindings.json:lamp_attempt_field3 |
| `lamp_theft_supported` | false | 2 | 1 | room13_lamp_attempt.rpy:97 | room13_v111_newworld_rules.rpy:56 |
| `last_page_holder` | (없음) | 2 | 0 | records.json:MS14_D10_P01_L0025 |  |
| `letter_close_selected` | (없음) | 1 | 0 | records.json options:MS14_D01_S01_L0014_O3 |  |
| `letter_observe_miss` | (없음) | 1 | 2 | room13_v111_days123.rpy:408 | room13_v111_days123.rpy:408 |
| `letter_tail_observed` | (없음) | 1 | 3 | room13_v111_days123.rpy:405 | room13_v111_days123.rpy:415 |
| `listed:*` | (없음) | 1 | 6 | room13_v111_newworld_rules.rpy:33 | room13_v111_days1114.rpy:20 |
| `listed:bami` | (없음) | 0 | 2 |  | room13_v111_days610.rpy:38 |
| `listed:daram` | (없음) | 1 | 9 | room13_v111_days1114.rpy:1916 | room13_v111_days1114.rpy:1915 |
| `listed:guard` | (없음) | 0 | 1 |  | room13_v111_days1114.rpy:4 |
| `listed:nabi` | (없음) | 0 | 4 |  | room13_hidden_pandol.rpy:13 |
| `listed:resident_bori` | (없음) | 0 | 1 |  | room13_v111_newworld_text.rpy:455 |
| `listed:resident_kongi` | (없음) | 0 | 1 |  | room13_v111_days610.rpy:40 |
| `listed:resident_owlgp` | (없음) | 0 | 1 |  | room13_v111_newworld_text.rpy:155 |
| `listed:resident_piko` | (없음) | 0 | 1 |  | room13_v111_days1114.rpy:2046 |
| `listed:resident_siluk` | (없음) | 0 | 3 |  | room13_v111_newworld_text.rpy:68 |
| `listed:resident_teacher` | (없음) | 0 | 1 |  | room13_v111_days1114.rpy:472 |
| `listed:resident_tok` | (없음) | 0 | 4 |  | room13_v111_newworld_text.rpy:279 |
| `listed_order` | (없음) | 1 | 3 | room13_v111_newworld_rules.rpy:35 | room13_v111_newworld_rules.rpy:35 |
| `listed_reason:*` | (없음) | 1 | 0 | room13_v111_newworld_rules.rpy:34 |  |
| `living_owl_records_question` | (없음) | 1 | 0 | records.json:MS14_D08_P01_L0026 |  |
| `location:*` | (없음) | 1 | 2 | room13_v111_later_bindings.rpy:84 | room13_v111.rpy:169 |
| `location:daram` | (없음) | 6 | 5 | room13_v111_days1114.rpy:2017 | room13_v111.rpy:182 |
| `location:guard` | (없음) | 1 | 2 | room13_v111_days1114.rpy:2624 | room13_v111.rpy:82 |
| `location:karo` | (없음) | 1 | 0 | room13_v111_days1114.rpy:2193 |  |
| `location:mom` | (없음) | 5 | 1 | room13_v111_days1114.rpy:1162 | room13_v111.rpy:476 |
| `location:nabi` | (없음) | 0 | 1 |  | room13_v111_days1114.rpy:107 |
| `location:resident_madam` | (없음) | 0 | 1 |  | room13_v111.rpy:105 |
| `location:resident_nero` | (없음) | 2 | 0 | room13_v111_days1114.rpy:995 |  |
| `location:resident_siluk` | (없음) | 1 | 0 | room13_v111_days1114.rpy:2062 |  |
| `location:resident_teacher` | (없음) | 1 | 0 | room13_v111_days1114.rpy:2055 |  |
| `location:resident_tok` | (없음) | 1 | 0 | room13_v111_owl_prevent.rpy:15 |  |
| `location:resident_tosil` | (없음) | 1 | 0 | room13_v111_days1114.rpy:3317 |  |
| `lower_lights_cut` | (없음) | 1 | 0 | room13_v111_days1114.rpy:858 |  |
| `lower_road_arrived11` | (없음) | 2 | 1 | room13_v111_days1114.rpy:513 | room13_v111_days1114.rpy:863 |
| `lower_road_handover` | (없음) | 1 | 4 | room13_v111_days1114.rpy:948 | room13_v111_days1114.rpy:863 |
| `lower_road_lost` | (없음) | 1 | 2 | room13_v111_days1114.rpy:994 | room13_v111_days1114.rpy:1032 |
| `madam_observer_consent` | (없음) | 1 | 5 | room13_v111_days1114.rpy:1100 | room13_v111.rpy:105 |
| `mayor_false_invitation_admitted` | (없음) | 1 | 0 | room13_v111_days1114.rpy:2911 |  |
| `mayor_site_decided` | (없음) | 2 | 2 | room13_v111_days1114.rpy:3071 | room13_v111_days1114.rpy:3051 |
| `mayor_site_joined` | (없음) | 2 | 2 | room13_v111_days1114.rpy:3072 | room13_v111_days1114.rpy:3054 |
| `meal12_intro_seen` | (없음) | 1 | 1 | room13_v111_days1114.rpy:1195 | room13_v111_days1114.rpy:1161 |
| `measurement_separated_from_theft` | (없음) | 1 | 0 | records.json:MS14_D03_S03_L0035 |  |
| `medical_arrived` | (없음) | 1 | 1 | room13_v111_days1114.rpy:1496 | room13_v111_later_bindings.rpy:150 |
| `medical_called` | (없음) | 2 | 0 | room13_v111_days1114.rpy:1323 |  |
| `medicine_locked` | (없음) | 1 | 3 | room13_v111_days1114.rpy:1109 | room13_v111_days1114.rpy:1212 |
| `meeting:*` | (없음) | 1 | 12 | room13_v111_newworld_rules.rpy:25 | room13_fork_screen.rpy:143 |
| `meeting:altar` | (없음) | 0 | 8 |  | room13_v111_days1114.rpy:3614 |
| `meeting:blanket` | (없음) | 0 | 3 |  | room13_v111_days1114.rpy:2145 |
| `meeting:fire` | (없음) | 0 | 9 |  | room13_v111_days610.rpy:600 |
| `meeting:gate_post` | (없음) | 0 | 6 |  | room13_v111_idle.rpy:185 |
| `meeting:hypothesis` | (없음) | 0 | 20 |  | room13_hidden_pandol.rpy:9 |
| `meeting:lamp` | (없음) | 0 | 23 |  | room13_lamp_attempt.rpy:96 |
| `meeting:records` | (없음) | 0 | 7 |  | room13_v111_newworld_text.rpy:205 |
| `meeting:room13` | (없음) | 0 | 9 |  | room13_v111_days1114.rpy:1192 |
| `meeting:soup` | (없음) | 0 | 5 |  | room13_v111_days1114.rpy:1560 |
| `mother_box_checked_day2` | false | 1 | 0 | records.json:MS14_D02_S01_L0033 |  |
| `mother_denies_invitation` | false | 1 | 0 | records.json:MS14_D05_S04_L0014 |  |
| `mother_location` | (없음) | 2 | 0 | records.json:MS14_D08_S04_L0033 |  |
| `mother_q_invitation` | (없음) | 1 | 0 | room13_v111_days1114.rpy:305 |  |
| `mother_q_life` | (없음) | 1 | 0 | room13_v111_days1114.rpy:296 |  |
| `mother_q_return` | (없음) | 1 | 1 | room13_v111_days1114.rpy:315 | room13_v111_idle.rpy:145 |
| `mother_route_shared` | (없음) | 1 | 0 | records.json:MS14_D06_S01_L0048 |  |
| `mother_secret_shared` | (없음) | 2 | 0 | records.json:MS14_D08_S04_L0033 |  |
| `mother_warning_received` | false | 1 | 1 | records.json:MS14_D05_S04_L0005 | room13_v111_later_bindings.rpy:117 |
| `murder_evidence_available` | (없음) | 1 | 0 | records.json:MS14_D08_P01_L0026 |  |
| `musoe.location` | (없음) | 2 | 0 | records.json:MS14_D05_S02_L0031 |  |
| `musoe_alive` | true | 0 | 1 |  | room13_v111.rpy:196 |
| `musoe_care` | (없음) | 1 | 0 | records.json:MS14_D05_S03_L0037 |  |
| `neoul_held` | (없음) | 1 | 0 | room13_v111_days1114.rpy:2123 |  |
| `neoul_promise_proven` | (없음) | 1 | 3 | room13_v111_days610.rpy:633 | room13_v111_days1114.rpy:2647 |
| `nero.location` | (없음) | 1 | 0 | records.json:MS14_D05_S05_L0014 |  |
| `nero_alive` | (없음) | 3 | 1 | room13_v111_days1114.rpy:884 | room13_v111_days1114.rpy:2170 |
| `nero_bedding_reserved` | false | 2 | 1 | records.json:MS14_D02_S04_L0083 | room13_v111_days123.rpy:1433 |
| `nero_contact_lead` | false | 1 | 0 | records.json:MS14_D02_S03_L0047 |  |
| `nero_met_day2` | false | 2 | 1 | records.json:MS14_D02_S04_L0038 | room13_v111_days45.rpy:47 |
| `nero_supply_route_known` | false | 2 | 0 | records.json:MS14_D02_S04_L0083 |  |
| `new_v1_evidence_seeded` | (없음) | 2 | 0 | records.json:MS14_D08_S02_L0037 |  |
| `night14_lodging` | (없음) | 4 | 1 | room13_v111_days1114.rpy:2581 | room13_v111_later_bindings.rpy:162 |
| `outcome13` | (없음) | 10 | 5 | room13_v111_days1114.rpy:2019 | room13_v111_days1114.rpy:2749 |
| `outer_latch_claim_refuted` | (없음) | 2 | 3 | room13_lamp_attempt.rpy:88 | room13_v111_newworld_text.rpy:123 |
| `owl_invitation_testimony` | (없음) | 1 | 1 | room13_v111_days610.rpy:1820 | room13_v111_days1114.rpy:331 |
| `owl_latch_seen7` | (없음) | 1 | 2 | room13_v111_owl_prevent.rpy:133 | room13_v111_owl_prevent.rpy:134 |
| `owl_reading8_done` | (없음) | 1 | 1 | room13_v111_owl_prevent.rpy:127 | room13_v111_owl_prevent.rpy:124 |
| `owl_tok_agreed7` | (없음) | 1 | 2 | room13_v111_owl_prevent.rpy:136 | room13_v111_owl_prevent.rpy:137 |
| `owl_tok_work7` | (없음) | 1 | 2 | room13_v111_owl_prevent.rpy:140 | room13_v111_days610.rpy:758 |
| `pandol_blanket_mended` | (없음) | 1 | 0 | room13_v111_days1114.rpy:1829 |  |
| `pending_handover_completed` | (없음) | 2 | 2 | room13_v111_days1114.rpy:3513 | room13_v111_newworld_text.rpy:84 |
| `pending_handover_supervised` | (없음) | 2 | 0 | room13_v111_days1114.rpy:2606 |  |
| `pending_post_search` | (없음) | 2 | 0 | records.json:MS14_D02_S02_L0025 |  |
| `piko.location` | (없음) | 5 | 1 | room13_lamp_attempt.rpy:21 | room13_v111.rpy:170 |
| `piko_alive` | true | 3 | 13 | room13_lamp_attempt.rpy:20 | room13_v111.rpy:63 |
| `piko_bench_clean2` | (없음) | 1 | 2 | room13_v111_days123.rpy:686 | systems/room13_v111_goal.rpy:176 |
| `piko_bench_seen2` | (없음) | 1 | 3 | room13_v111_days123.rpy:683 | systems/room13_v111_goal.rpy:178 |
| `piko_cloth2` | (없음) | 1 | 2 | room13_v111_days123.rpy:679 | systems/room13_v111_goal.rpy:178 |
| `piko_sacks2` | (없음) | 1 | 3 | room13_v111_days123.rpy:676 | room13_v111_newworld_text.rpy:144 |
| `piko_sheltered` | false | 2 | 5 | records.json:MS14_D02_S04_L0038 | room13_v111_days123.rpy:788 |
| `pin_after_cry` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0036 |  |
| `pin_owner` | (없음) | 3 | 0 | records.json:MS14_D08_S03_L0028 |  |
| `pin_transfer` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0059 |  |
| `pocket_ration7` | (없음) | 2 | 2 | room13_v111_owl_prevent.rpy:63 | systems/room13_stove_art.rpy:24 |
| `portrait` | none | 3 | 4 | records.json:MS14_D03_S01_L0021 | room13_v111.rpy:504 |
| `portrait_commissioned` | (없음) | 1 | 1 | records.json:MS14_D02_S03_L0020 | systems/room13_v111_goal.rpy:132 |
| `post_search_status` | (없음) | 1 | 0 | records.json:MS14_D09_S04_L0024 |  |
| `postcry_alive_testimony` | (없음) | 2 | 0 | records.json:MS14_D08_S02_L0037 |  |
| `postcry_head_uninjured` | (없음) | 1 | 0 | records.json:MS14_D10_S02_L0033 |  |
| `premeditation` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0088 |  |
| `prevention` |  | 3 | 12 | room13_v111_owl_prevent.rpy:89 | room13_v111_days1114.rpy:799 |
| `proof_given:*` | (없음) | 1 | 1 | room13_v111.rpy:437 | room13_v111_newworld_rules.rpy:230 |
| `proof_given:맨 처음 이름을 짚는다` | (없음) | 0 | 3 |  | room13_v111_newworld_text.rpy:178 |
| `proof_given:반송·필사본·초대 발송을 대조한다` | (없음) | 0 | 2 |  | room13_v111_newworld_text.rpy:173 |
| `proof_given:밤이 혐의의 근거를 확인한다` | (없음) | 0 | 5 |  | room13_v111_newworld_text.rpy:139 |
| `proof_given:수리와 반출을 가릴 자료를 낸다` | (없음) | 0 | 1 |  | room13_v111_newworld_text.rpy:138 |
| `proof_given:아내가 봤다는 담요의 시점을 확인한다` | (없음) | 0 | 1 |  | room13_v111_newworld_text.rpy:175 |
| `proof_given:요즘 돌이 어디서 오는지 대조한다` | (없음) | 0 | 1 |  | room13_v111_newworld_text.rpy:172 |
| `proof_given:장부의 두 배를 실룩에게 보인다` | (없음) | 0 | 1 |  | room13_v111_newworld_text.rpy:177 |
| `proof_given:초롱과 피코의 하루를 대조한다` | (없음) | 0 | 2 |  | room13_v111_newworld_text.rpy:171 |
| `proof_given:촌장이 어젯밤 있던 곳을 확인한다` | (없음) | 0 | 1 |  | room13_v111_newworld_text.rpy:176 |
| `proof_given:함께 들어갈 근거를 고른다` | (없음) | 0 | 1 |  | room13_v111_newworld_text.rpy:137 |
| `proof_given:희생의 숫자와 장부를 대조한다` | (없음) | 0 | 1 |  | room13_v111_days1114.rpy:2940 |
| `proxy_receipt_authority` | (없음) | 1 | 0 | records.json:MS14_D10_P01_L0025 |  |
| `public_board_count_match` | (없음) | 1 | 0 | records.json:MS14_D10_P01_L0069 |  |
| `public_road_escort_completed` | (없음) | 1 | 0 | room13_v111_days610.rpy:1091 |  |
| `public_stones` | with_baek | 3 | 1 | records.json:MS14_D03_S05_L0052 | room13_v111_days123.rpy:1362 |
| `purpose_difference_known` | false | 2 | 2 | records.json:MS14_D01_S03_L0012 | room13_v111_days123.rpy:231 |
| `reacted:*` | (없음) | 1 | 1 | room13_v111_idle.rpy:51 | room13_v111_idle.rpy:36 |
| `reacted:*:*` | (없음) | 0 | 1 |  | room13_v111_idle.rpy:37 |
| `reason_heard` | false | 2 | 2 | records.json:MS14_D01_S03_L0031 | field-bindings.json:gate_investigate |
| `relay_stopped` | (없음) | 1 | 1 | room13_v111_days1114.rpy:2540 | room13_v111.rpy:92 |
| `repair_opening_separated` | (없음) | 2 | 3 | room13_lamp_attempt.rpy:62 | room13_v111_newworld_text.rpy:121 |
| `rescue_cart_ready` | (없음) | 1 | 1 | room13_v111_days1114.rpy:459 | field-bindings.json:rescue_cart11 |
| `rescue_cover_ready` | (없음) | 1 | 1 | room13_v111_days1114.rpy:462 | field-bindings.json:rescue_cart11 |
| `rescue_driver_ready` | (없음) | 1 | 1 | room13_v111_days1114.rpy:465 | field-bindings.json:rescue_cart11 |
| `rescue_handoff_period11` | (없음) | 3 | 2 | room13_v111_days1114.rpy:514 | room13_v111_days1114.rpy:951 |
| `rescue_lights_ready` | (없음) | 1 | 1 | room13_v111_days1114.rpy:468 | field-bindings.json:rescue_cart11 |
| `rescue_preparation_schema11` | (없음) | 1 | 1 | room13_v111_days1114.rpy:448 | room13_v111_days1114.rpy:17 |
| `rescue_school_ready11` | (없음) | 1 | 2 | room13_v111_days1114.rpy:476 | room13_v111_days1114.rpy:17 |
| `return_transport_inquiry_pending` | (없음) | 1 | 0 | records.json:MS14_D02_S01_L0008 |  |
| `returned_pages_count` | (없음) | 1 | 0 | records.json:MS14_D09_P01_L0027 |  |
| `riot_momo13` | (없음) | 1 | 2 | room13_v111_days1114.rpy:2725 | room13_v111_days1114.rpy:2728 |
| `room13_partial_kind` | (없음) | 3 | 2 | room13_v111_days610.rpy:1650 | room13_v111_newworld_text.rpy:203 |
| `root_address_known` | (없음) | 1 | 1 | room13_v111_days1114.rpy:55 | room13_v111_later_bindings.rpy:141 |
| `roster_shown13` | (없음) | 1 | 1 | room13_v111_days1114.rpy:2104 | room13_v111_days1114.rpy:2103 |
| `route12` | (없음) | 8 | 17 | room13_v111_days1114.rpy:1165 | room13_v111_days1114.rpy:1373 |
| `route7` | uncommitted | 4 | 17 | room13_v111_days610.rpy:761 | room13_v111_days610.rpy:852 |
| `route_face_visible_to_crowd` | (없음) | 1 | 0 | records.json:MS14_D10_P01_L0069 |  |
| `rumor_not_eyewitness` | false | 1 | 0 | records.json:MS14_D04_S04_L0032 |  |
| `same_moment_fatal_contact` | (없음) | 1 | 0 | records.json:MS14_D10_S03_L0059 |  |
| `school_day_seat` | (없음) | 1 | 1 | records.json:MS14_D06_S01_L0048 | room13_v111_later_bindings.rpy:118 |
| `school_heat_connected` | (없음) | 4 | 5 | room13_v111_days1114.rpy:524 | room13_v111.rpy:602 |
| `school_inventory_checked` | (없음) | 1 | 0 | room13_v111_days1114.rpy:3387 |  |
| `school_permission` | (없음) | 1 | 0 | records.json:MS14_D06_P01_L0008 |  |
| `school_supply_handed` | (없음) | 4 | 5 | room13_v111_days1114.rpy:523 | room13_hidden_pandol.rpy:11 |
| `selected_afternoon_work_completed` | (없음) | 2 | 0 | records.json:MS14_D02_S04_L0038 |  |
| `seori_disciplined` | (없음) | 1 | 0 | room13_v111_days1114.rpy:1577 |  |
| `separate_page_observed` | (없음) | 1 | 0 | records.json:MS14_D10_P01_L0069 |  |
| `silluk.children.location` | (없음) | 2 | 0 | room13_lamp_attempt.rpy:50 |  |
| `silluk_knife_comparison_consent` | (없음) | 1 | 0 | records.json:MS14_D03_S04_L0016 |  |
| `silluk_labor_transfer_known` | false | 1 | 0 | records.json:MS14_D04_S01_L0015 |  |
| `silluk_status` | free | 4 | 6 | room13_v111_days123.rpy:1259 | room13_v111.rpy:172 |
| `silluk_transfer` | (없음) | 2 | 0 | room13_v111_days1114.rpy:2064 |  |
| `snack_bagged5` | (없음) | 1 | 5 | room13_v111_owl_prevent.rpy:28 | room13_v111_days610.rpy:14 |
| `sole_access_assumption` | (없음) | 1 | 0 | records.json:MS14_D10_S02_L0046 |  |
| `somi.location` | (없음) | 2 | 0 | records.json:MS14_D05_S02_L0031 |  |
| `somi_entry_consent` | false | 1 | 0 | records.json:MS14_D05_S01_L0008 |  |
| `soup_bottle_seen12` | (없음) | 1 | 1 | room13_v111_days1114.rpy:1254 | field-bindings.json:meal_inspect12 |
| `soup_bowls_seen12` | (없음) | 1 | 1 | room13_v111_days1114.rpy:1251 | field-bindings.json:meal_inspect12 |
| `soup_fragment_observed` | (없음) | 2 | 1 | room13_v111_days1114.rpy:1340 | room13_v111_later_bindings.rpy:149 |
| `soup_lose_kind` | (없음) | 2 | 4 | room13_v111_days1114.rpy:1576 | room13_v111_newworld_text.rpy:240 |
| `soup_serving_separated12` | (없음) | 1 | 0 | room13_v111_days1114.rpy:1257 |  |
| `soup_smallpot_seen12` | (없음) | 1 | 1 | room13_v111_days1114.rpy:1248 | field-bindings.json:meal_inspect12 |
| `stone_choice_completed` | (없음) | 3 | 0 | room13_lamp_attempt.rpy:98 |  |
| `stone_warm_felt3` | (없음) | 2 | 1 | room13_lamp_attempt.rpy:108 | room13_v111_days1114.rpy:359 |
| `stop_actor` | (없음) | 1 | 0 | room13_v111_days1114.rpy:2084 |  |
| `story14_completed` | (없음) | 2 | 0 | room13_v111_days1114.rpy:2827 |  |
| `stove13_7` | (없음) | 2 | 8 | room13_v111_owl_prevent.rpy:67 | room13_v111_days610.rpy:728 |
| `supply_contact_pending` | false | 1 | 0 | records.json:MS14_D05_S04_L0027 |  |
| `talked:*:*` | (없음) | 1 | 2 | room13_v111.rpy:333 | room13_v111_idle.rpy:99 |
| `teacher_agrees` | (없음) | 1 | 0 | records.json:MS14_D06_P01_L0008 |  |
| `teacher_confessed` | (없음) | 1 | 1 | room13_v111_days1114.rpy:1541 | room13_v111_later_bindings.rpy:150 |
| `teacher_custody` | (없음) | 4 | 2 | records.json:MS14_D12_S04_L0104 | room13_v111.rpy:175 |
| `teacher_supervisor` | (없음) | 1 | 0 | room13_v111_days1114.rpy:1849 |  |
| `teacher_transfer` | (없음) | 6 | 2 | room13_v111_days1114.rpy:2057 | room13_v111_days1114.rpy:2010 |
| `time_cost` | (없음) | 25 | 0 | records.json:MS14_D08_S02_L0039 |  |
| `tok_*` | (없음) | 0 | 1 |  | room13_v111_later_bindings.rpy:63 |
| `tok_repair_copy_owned` | (없음) | 2 | 0 | records.json:MS14_D09_S02_L0018 |  |
| `tongs7` | (없음) | 1 | 1 | room13_v111_owl_prevent.rpy:71 | field-bindings.json:free_day7 |
| `tosil_blanket_given` | (없음) | 0 | 1 |  | room13_v111_days1114.rpy:551 |
| `tosil_knows_greenhouse` | (없음) | 1 | 0 | records.json:MS14_D11_S01_L0052 |  |
| `tosil_listen` | (없음) | 2 | 18 | room13_v111_days1114.rpy:3286 | room13_v111_days1114.rpy:3288 |
| `tosil_location` | (없음) | 1 | 0 | records.json:MS14_D11_S01_L0052 |  |
| `tosil_safe_handoff_confirmed` | (없음) | 1 | 2 | records.json:MS14_D11_S01_L0052 | room13_navigation.rpy:100 |
| `transfer_list_secured` | (없음) | 1 | 0 | room13_v111_days1114.rpy:1558 |  |
| `transfer_list_voided` | (없음) | 2 | 7 | room13_v111_days1114.rpy:1562 | room13_v111_grand_win.rpy:31 |
| `tries:*` | (없음) | 1 | 3 | room13_v111_newworld_rules.rpy:319 | room13_v111_newworld_rules.rpy:198 |
| `tries:gate` | (없음) | 0 | 3 |  | room13_v111_newworld_text.rpy:101 |
| `tries:gate_post` | (없음) | 1 | 2 | room13_v111_days45.rpy:489 | room13_v111_days45.rpy:489 |
| `tries:hypothesis` | (없음) | 0 | 2 |  | room13_v111_newworld_text.rpy:245 |
| `two_attackers_proven` | (없음) | 1 | 0 | records.json:MS14_D10_S02_L0033 |  |
| `ui_room_arrival_seen` | (없음) | 1 | 1 | room13_v111_days123.rpy:342 | room13_v111_days123.rpy:340 |
| `ui_topic_read:*:*` | (없음) | 1 | 1 | room13_v111.rpy:343 | room13_v111.rpy:133 |
| `under_desk_checked` | false | 1 | 0 | records.json:MS14_D01_S05_L0022 |  |
| `unverified_stones_status` | with_baek | 2 | 0 | records.json:MS14_D03_S05_L0052 |  |
| `void_down:*` | (없음) | 1 | 1 | room13_v111_grand_win.rpy:37 | room13_v111_newworld_rules.rpy:44 |
| `warehouse_children_location` | (없음) | 1 | 0 | records.json:MS14_D06_S03P_L0008 |  |
| `warehouse_children_rescued` | (없음) | 1 | 0 | records.json:MS14_D06_S03_L0022 |  |
| `warehouse_children_school_handover` | (없음) | 1 | 1 | records.json:MS14_D06_P01_L0024 | room13_v111_later_bindings.rpy:121 |
| `warehouse_survivors_school_care` | (없음) | 1 | 0 | records.json:MS14_D07_S02_L0029 |  |
| `warm_seat_ready` | (없음) | 1 | 4 | room13_v111_days1114.rpy:1122 | room13_v111_days1114.rpy:1214 |
| `warm_seat_taken12` | (없음) | 1 | 1 | room13_v111_days1114.rpy:1118 | field-bindings.json:morning_prep12 |
| `warm_support_arrived` | (없음) | 1 | 3 | room13_v111_days1114.rpy:1145 | room13_v111_newworld_text.rpy:254 |
| `wild_family` | (없음) | 1 | 6 | room13_v111_days1114.rpy:3705 | room13_v111_days1114.rpy:3712 |
| `wild_late` | (없음) | 4 | 4 | room13_v111_days1114.rpy:3649 | room13_v111_days1114.rpy:3671 |
| `wild_night14` | (없음) | 1 | 4 | room13_v111_days1114.rpy:3648 | room13_v111.rpy:167 |
| `wounds_distinct` | (없음) | 1 | 0 | records.json:MS14_D10_S02_L0033 |  |
| `wrong:*` | (없음) | 1 | 1 | room13_v111_newworld_rules.rpy:435 | room13_v111_newworld_rules.rpy:434 |
| `wrong_final:*` | (없음) | 1 | 1 | room13_v111_newworld_rules.rpy:440 | room13_v111_newworld_rules.rpy:437 |
| `(식) ('fate:' if r13_fork_is_fate_point(key) else 'meeting:')+key` | (없음) | 0 | 1 |  | room13_fork_screen.rpy:55 |
| `(식) fixed[0]` | (없음) | 0 | 1 |  | systems/room13_v111_goal.rpy:201 |
| `(식) flag` | (없음) | 0 | 1 |  | room13_v111_newworld_rules.rpy:173 |
| `(식) k` | (없음) | 0 | 10 |  | room13_v111.rpy:78 |
| `(식) key` | (없음) | 4 | 6 | room13_fork_screen.rpy:370 | room13_fork_screen.rpy:371 |
| `(식) life.get(person,"alive:"+person)` | (없음) | 0 | 1 |  | room13_v111.rpy:57 |
| `(식) op["field"]` | (없음) | 1 | 0 | room13_v111.rpy:34 |  |
| `(식) op["key"]+".variant"` | (없음) | 1 | 0 | room13_v111.rpy:38 |  |

v111 파일에서 쓰거나 읽지 않는 키(옛 판 코드에만 있음) 8개: `carriage_stopped`, `father_with_daram`, `invitation_author`, `tok_hearing_present`, `tok_workshop_present`, `(식) base+".status"`, `(식) base+".variant"`, `(식) lives[person]`

## 장소와 배경 그림

| 장소 키 | 이름 | 배경 키 | 조사 화면 그림 | 출처 |
|---|---|---|---|---|
| altar | 북쪽 산길 · 숲속 제단 | r13_altar | room13-pixel-ready-altar0177-afternoon.webp, room13-pixel-ready-altar0177-evening.webp, room13-pixel-ready-altar0177-morning.webp | assets/room13-world-layout.json |
| clinic | 임시 진료실 | r13_clinic | room13-pixel-ready-clinic0177-afternoon.webp, room13-pixel-ready-clinic0177-evening.webp, room13-pixel-ready-clinic0177-morning.webp | assets/room13-world-layout.json |
| dining | 여관 식당 | council | room13-pixel-wide-dining-afternoon.webp, room13-pixel-wide-dining-evening.webp, room13-pixel-wide-dining-morning.webp | assets/room13-world-layout.json |
| facility | 북쪽 옛 시설 | r13_facility | room13-pixel-ready-facility0177-afternoon.webp, room13-pixel-ready-facility0177-evening.webp, room13-pixel-ready-facility0177-morning.webp | assets/room13-world-layout.json |
| forest | 마을 서쪽 · 길 없는 숲 | r13_forest | room13-pixel-wide-forest-afternoon.webp, room13-pixel-wide-forest-evening.webp, room13-pixel-wide-forest-morning.webp | assets/room13-world-layout.json |
| gate | 눈에 막힌 입구 | winter | room13-pixel-ready-gate0173-afternoon.webp, room13-pixel-ready-gate0173-evening.webp, room13-pixel-ready-gate0173-morning.webp | assets/room13-world-layout.json |
| greenhouse | 폐온실의 지하 작업실 | r13_greenhouse | room13-pixel-ready-greenhouse0177-afternoon.webp, room13-pixel-ready-greenhouse0177-evening.webp, room13-pixel-ready-greenhouse0177-morning.webp | assets/room13-world-layout.json |
| hall | 여관 2층 복도 | hall |  (상태별: after, before) | assets/room13-world-layout.json |
| hidden_pandol | 판돌 집 | ms14_somi_inside | 배경 키 ms14_somi_inside 의 파일은 옛 r13_background 경로(room13_life.rpy 등)로 정해짐 — 미확인 |  |
| inn | 여관 접수대 | front | room13-pixel-panorama-inn-afternoon.webp, room13-pixel-panorama-inn-evening.webp, room13-pixel-panorama-inn-morning.webp | assets/room13-world-layout.json |
| kitchen | 여관 1층 · 주방 | kitchen | room13-pixel-wide-kitchen-afternoon.webp, room13-pixel-wide-kitchen-evening.webp, room13-pixel-wide-kitchen-morning.webp | assets/room13-world-layout.json |
| laundry | 마을 빨래터 | ep_laundry | room13-pixel-panorama-laundry-afternoon.webp, room13-pixel-panorama-laundry-evening.webp | R13_WORLD_LAYOUTS(later_bindings, EP 배경으로 등록) |
| ms14_guardroom | 밝은 초소 안 | winter | room13-bg-guardroom-afternoon.webp, room13-bg-guardroom-evening.webp, room13-bg-guardroom-morning.webp | assets/room13-world-layout.json |
| ms14_somi | 솜이네 골목 | winter | room13-bg-somi-alley-afternoon.webp, room13-bg-somi-alley-evening.webp, room13-bg-somi-alley-morning.webp | assets/room13-world-layout.json |
| ms14_somi_inside | 솜이네 방 | ep_somi_home | ms14/somi_inside 계열(MS14_ART["somi_inside"]) | later_bindings |
| post | 우체국 입구 | winter_post | room13-pixel-wide-post-morning.webp | assets/room13-world-layout.json |
| room13 | 여관 2층 · 13호실 | room |  (상태별: after, before) | assets/room13-world-layout.json |
| school | 마을 학교 | r13_school | room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-evening.webp, room13-pixel-panorama-school-morning.webp | assets/room13-world-layout.json |
| square | 돌이 있는 광장 | winter_square | room13-pixel-panorama-square-afternoon.webp, room13-pixel-panorama-square-evening.webp, room13-pixel-panorama-square-morning.webp | assets/room13-world-layout.json |
| store | 공동 물품 창고 | r13_store | room13-bg-store-2-afternoon.webp, room13-bg-store-2-evening.webp, room13-bg-store-2-morning.webp | assets/room13-world-layout.json |
| v111_custody | 보호실 면회 자리 | ep_holding_morning | room13-pixel-panorama-holding-morning.webp | R13_EP_BACKGROUNDS |
| v111_fire | 장작 창고 바깥 | ep_woodshed_fire | room13-pixel-panorama-woodshed-fire.webp | R13_WORLD_LAYOUTS(later_bindings, EP 배경으로 등록) |
| v111_labor | 공동 장작 하역장 | ep_woodshed_intact | room13-pixel-panorama-woodshed-intact.webp | R13_WORLD_LAYOUTS(later_bindings, EP 배경으로 등록) |
| v111_ruin | 식은 장작 창고 터 | ep_woodshed_ruin | room13-pixel-panorama-woodshed-ruin.webp | R13_WORLD_LAYOUTS(later_bindings, EP 배경으로 등록) |
| v111_supervised | 분리된 감독 자리 | ep_holding_morning | room13-pixel-panorama-holding-morning.webp | R13_EP_BACKGROUNDS |
| v111_woodshed | 학교 뒤 장작 창고 | ep_woodshed_inside | room13-pixel-wide-woodshed-inside-afternoon.webp, room13-pixel-wide-woodshed-inside-evening.webp | R13_WORLD_LAYOUTS(later_bindings, EP 배경으로 등록) |
| workshop | 수리점 | winter_workshop | room13-pixel-panorama-workshop-afternoon.webp, room13-pixel-panorama-workshop-evening.webp, room13-pixel-panorama-workshop-morning.webp | assets/room13-world-layout.json |

## 덮어쓰기 최종 동작(v111 이 실제로 쓰는 함수)

| 함수 | 마지막 층 → 그 아래 v111 층 | 최종 동작 |
|---|---|---|
| `r13_v111_lines(rids)` | room13_v111_reactions.rpy:107 → room13_v111_newworld_text.rpy:580 | id 마다 before(조건 맞는 것) → 원문(drop 조건이면 뺌; replace 변형 중 먼저 맞는 것, 없으면 원문 글; 변형의 expression·cut·fx 적용; 1일 마차 8줄은 R13_V111_CARRIAGE_TEXT) → after(조건). 끝에 「기회를 다 쓴」 마지막 속말이 기다리면 붙인다. 바깥 층은 그 id 를 heard_in 으로 가진 후속 질문을 「들었다」로 표시. |
| `r13_v111_line(rid)` | room13_v111_newworld_text.rpy:542 → room13_v111.rpy:58 | 원문 줄 → (인물 키, 글, {expression=direction.slot, pose, no_lead}). 화자가 죽었거나 조건(requires)이 안 맞으면 예외. 13일 담요 컷 특례. |
| `r13_nw_block(name)` | room13_v111_newworld_text.rpy | dNN blocks 의 줄 중 조건 맞는 것 + 마지막 속말. |
| `r13_v111_binding()` | room13_v111_grand_win.rpy:17 → newworld_rules.rpy:453 → room13_v111.rpy:72 | 대기 묶음 = field-bindings[gate] 에서 guard(자료 보유·값)가 맞는 선택지만. 대기별 특례(free_day7·transport_cleanup13·device_detach14·guard_relief_check14·partial_receipt14·crowd_prepare13·daram_if_free·people_by_location). 떠난 사람(departed:*) 제외. 이동 대기에는 5일 빨래터 우회 자리. |
| `r13_v111_questions(person)` | room13_v111_reactions.rpy:81 → room13_v111.rpy:126 | 이 사람·이 장소 선택지(present_only 제외; 가진 자료를 내미는 선택지는 「present」로) + 후속 질문(안 들었으면 「새」). |
| `r13_v111_idle_lines(person)` | room13_v111_idle.rpy:214(5층) | 2일 안내 → 긴장 장면이면 아빠 속말 → 돌목 6~10일 특례 → 맡은 일 지문 → 방금 대화 → 처음 만남(아빠 인사+첫 인사) → 그날 첫 인사(아빠 한마디+일하는 줄) → 아빠 속말 3종 돌림. |
| `r13_v111_present_reaction(person,shown)` | room13_v111_idle.rpy:139(3층) | reactions.json present(날짜·회의 뒤 조건) → generic → 다람 답 → 아빠 속말. 본 반응은 reacted:* 로 기록. |
| `r13_v111_arrive(people)` | newworld_rules.rpy:447 → later_bindings.rpy:76 | 떠난 사람 빼고, 살아 있는 사람만 지금 장소에 location:* 로 적고 무대 인물로 둔다(14일 백 부인 특례). |
| `r13_visible_people()` | room13_v111_scene_elsewhere.rpy:16 → room13_v111.rpy:153(5층) | 묶음 people + 옛 일과표 주민(필터: busy·위치·생사·구금·떠남) − 다람(동행이면). 장면 묶음 장소가 지금 장소와 다르면 선택지가 가리키는 사람만. |
| `r13_object_visible(spec)` | room13_v111.rpy:237(11층) | v111 이면: 선택지가 가리키거나 관찰 글이 있으면 보임. 그 앞 10층은 v111 에서 관찰 글 계산에만 쓰인다. |
| `r13_places()` | room13_v111.rpy:262(6층) | 지금 장소 + 대기 선택지 장소. |
| `r13_v111_set(key,value)` | room13_fork_screen.rpy:370 (3층) | 값 쓰기 + day/DARAM_DETAINED/OWL_ALIVE/grandmother_custody/family_reunited 는 옛 상태 칸도 갱신, 죽음 깃발, story14_completed 면 결말 기록. 바깥 층은 갈림길 기록. |
| `r13_v111_goal()` | systems/room13_v111_goal.rpy:213(4층) | 대기별 할 일(STEP_GOALS) → 장면 의문(QUESTIONS), 이동 중엔 직전 장면 문구 + 목적지. |
| `r13_v111_context(key)` | systems/room13_camera_follow.rpy:10 → room13_v111.rpy:120 | 대기 이름 기록, 이동 아닌 대기면 생각 유지를 놓고, 카메라를 대상 쪽으로. |
| `r13_catalog_record(key)` | room13_v111_newworld_rules.rpy:14(3층) | 자료 카드: E09 초상·E14_SUPPLY·E35 침구·E05(외 한 명) 동적 이름·설명. |
| `r13_material_art(key)` | room13_v111.rpy:500 | E13_MENDING·E09·E30 특수 그림, 그 밖 R13_V111_MATERIAL_ART 로 옛 그림 대응. |
| `r13_background(key)` | systems/room13_wild_night_art.rpy:21(3층) | 불타는 밤 그림 → v111 이면 장소 배치표 카메라 배경 → EP 배경 → 옛 배경. |
| `r13_speaker(who,…)` | room13_carriage_direction.rpy:99(3층) | 마차 안 다람은 앉은 그림, 그 밖은 공통 화자 처리. v111 층은 만난 사람 기록. |
| `r13_sound_scene_music(bg,title,mood)` | room13_v111.rpy:613(3층) | v111 장면 환경음 + 장면 음악(덮어쓰기·멈춤 포함), 장면표에 없으면 장소별 기본. |
| `r13_topics / r13_present` | 24층 / 22층 | v111 에서는 쓰지 않는다: 화면 r13_topics 가 v111 이면 r13_mark_new_questions(r13_v111_questions(person)) 를 쓰고(room13_screens.rpy:259), 제시는 r13_v111_present_index·r13_v111_present_reaction 이 받는다. |

### 전체 덮어쓰기 표(docs/OVERRIDE_MAP.md 요약: 함수 · 층 수 · 게임이 부르는 바깥 층)

| 함수 | 층 | 바깥 층 |
|---|---|---|
| `r13_topics` | 24 | `systems/room13_sling_confidence.rpy:65` |
| `r13_present` | 22 | `systems/room13_sling_confidence.rpy:74` |
| `r13_stage_people` | 18 | `systems/room13_stage_cache.rpy:17` |
| `r13_object_visible` | 11 | `room13_v111.rpy:237` |
| `r13_conversation_topic_lines` | 10 | `systems/room13_question_discovery.rpy:186` |
| `r13_first_mystery_notes` | 10 | `systems/room13_v111_goal.rpy:192` |
| `r13_where` | 10 | `room13_v111_field_layout.rpy:106` |
| `r13_compare_result` | 6 | `systems/room13_testimony.rpy:42` |
| `r13_places` | 6 | `room13_v111.rpy:262` |
| `r13_finish_topic` | 5 | `systems/room13_daram_home.rpy:127` |
| `r13_intro_goal` | 5 | `systems/room13_review_knowledge.rpy:119` |
| `r13_v111_idle_lines` | 5 | `room13_v111_idle.rpy:214` |
| `r13_visible_people` | 5 | `room13_v111_scene_elsewhere.rpy:16` |
| `r13_calendar_topic_seen` | 4 | `systems/room13_piko_causality.rpy:103` |
| `r13_campaign_goal` | 4 | `systems/room13_v111_goal.rpy:6` |
| `r13_debate_judge` | 4 | `systems/room13_q1_difficulty.rpy:188` |
| `r13_debate_seats` | 4 | `systems/room13_q1_arguments.rpy:198` |
| `r13_ep_line_art` | 4 | `systems/room13_end_cut.rpy:83` |
| `r13_next_day` | 4 | `systems/room13_no_livelihood.rpy:27` |
| `r13_person_action` | 4 | `room13_v111.rpy:202` |
| `r13_v111_goal` | 4 | `systems/room13_v111_goal.rpy:213` |
| `r13_activity_text` | 3 | `systems/room13_alibi.rpy:37` |
| `r13_available` | 3 | `room13_route_knowledge.rpy:16` |
| `r13_background` | 3 | `systems/room13_wild_night_art.rpy:21` |
| `r13_bed_available` | 3 | `room13_v111.rpy:266` |
| `r13_before_line` | 3 | `systems/room13_goal_strip.rpy:80` |
| `r13_calendar_promises` | 3 | `systems/room13_goal_strip.rpy:269` |
| `r13_catalog_record` | 3 | `room13_v111_newworld_rules.rpy:14` |
| `r13_conversation_opening` | 3 | `systems/room13_q1_review.rpy:141` |
| `r13_debate_required` | 3 | `systems/room13_q1_difficulty.rpy:194` |
| `r13_debate_session` | 3 | `room13_v111_meeting_stage.rpy:108` |
| `r13_debate_statements` | 3 | `systems/room13_q1_difficulty.rpy:173` |
| `r13_finish_action` | 3 | `systems/room13_items.rpy:140` |
| `r13_flag` | 3 | `systems/room13_shelf.rpy:28` |
| `r13_line_performance` | 3 | `room13_carriage_direction.rpy:93` |
| `r13_meeting_cast` | 3 | `room13_v111_meeting_stage.rpy:113` |
| `r13_meeting_plate` | 3 | `room13_v111_meeting_stage.rpy:146` |
| `r13_new` | 3 | `systems/room13_no_carryover.rpy:6` |
| `r13_object_name` | 3 | `systems/room13_day2_guidance.rpy:40` |
| `r13_q1_notes` | 3 | `systems/room13_piko_causality.rpy:42` |
| `r13_q1_summary` | 3 | `systems/room13_q1_difficulty.rpy:253` |
| `r13_sound_scene_music` | 3 | `room13_v111.rpy:613` |
| `r13_speaker` | 3 | `room13_carriage_direction.rpy:99` |
| `r13_v111_binding` | 3 | `room13_v111_grand_win.rpy:17` |
| `r13_v111_present_reaction` | 3 | `room13_v111_idle.rpy:139` |
| `r13_v111_set` | 3 | `room13_fork_screen.rpy:370` |
| `r13_world_background` | 3 | `systems/room13_ep_art.rpy:247` |
| `r13_acting_spec` | 2 | `systems/room13_asset_domains.rpy:18` |
| `r13_actor_nameplates` | 2 | `systems/room13_stage_cache.rpy:35` |
| `r13_bdialogue_face` | 2 | `systems/room13_asset_domains.rpy:22` |
| `r13_click_feedback` | 2 | `systems/room13_sound.rpy:210` |
| `r13_close_spec` | 2 | `systems/room13_asset_domains.rpy:14` |
| `r13_contact_presentations` | 2 | `systems/room13_q1_arguments.rpy:29` |
| `r13_debate_answerable` | 2 | `systems/room13_q1_arguments.rpy:179` |
| `r13_debate_engageable` | 2 | `systems/room13_q1_arguments.rpy:186` |
| `r13_debate_hint_due` | 2 | `systems/room13_q1_arguments.rpy:190` |
| `r13_debate_partial_lines` | 2 | `systems/room13_q1_arguments.rpy:194` |
| `r13_debate_ready` | 2 | `systems/room13_q1_arguments.rpy:157` |
| `r13_debate_visible` | 2 | `systems/room13_q1_arguments.rpy:149` |
| `r13_dialogue_beat_art` | 2 | `systems/room13_dialogue_context_art.rpy:28` |
| `r13_dialogue_beat_begin` | 2 | `systems/room13_dialogue_context_art.rpy:14` |
| `r13_dialogue_context_match` | 2 | `room13_v111_newworld_text.rpy:599` |
| `r13_ending_notes` | 2 | `systems/room13_week2_events.rpy:42` |
| `r13_ep_background` | 2 | `systems/room13_ep_art.rpy:237` |
| `r13_ep_cut_art` | 2 | `systems/room13_special_scenes.rpy:33` |
| `r13_ep_line_art_clear` | 2 | `systems/room13_end_cut.rpy:91` |
| `r13_evidence_acquired` | 2 | `systems/room13_sound.rpy:196` |
| `r13_evidence_art_path` | 2 | `systems/room13_asset_domains.rpy:27` |
| `r13_fullbody_spec` | 2 | `systems/room13_asset_domains.rpy:10` |
| `r13_grant` | 2 | `systems/room13_grant_timing.rpy:10` |
| `r13_has` | 2 | `systems/room13_items.rpy:95` |
| `r13_intro_direction_lines` | 2 | `systems/room13_review_knowledge.rpy:98` |
| `r13_learning_job_context` | 2 | `systems/room13_poc_route.rpy:131` |
| `r13_learning_sleep_text` | 2 | `systems/room13_convenience.rpy:24` |
| `r13_life_apply_purchase` | 2 | `systems/room13_sound.rpy:216` |
| `r13_life_tool_name` | 2 | `systems/room13_gimmicks.rpy:45` |
| `r13_living_pose` | 2 | `systems/room13_solbang_chinchilla.rpy:4` |
| `r13_local_connections` | 2 | `systems/room13_first_day_flow.rpy:25` |
| `r13_material_art` | 2 | `room13_v111.rpy:500` |
| `r13_meeting_direct_line` | 2 | `room13_v111_meeting_stage.rpy:161` |
| `r13_meeting_focus_person` | 2 | `room13_v111_meeting_stage.rpy:119` |
| `r13_meeting_header` | 2 | `room13_v111_meeting_stage.rpy:154` |
| `r13_meeting_orbit_height` | 2 | `room13_v111_meeting_stage.rpy:130` |
| `r13_meeting_portrait_x` | 2 | `room13_v111_meeting_stage.rpy:137` |
| `r13_open_person_material` | 2 | `systems/room13_evidence_drawer.rpy:251` |
| `r13_prove` | 2 | `systems/room13_no_livelihood.rpy:49` |
| `r13_q1_node_open` | 2 | `systems/room13_q1_difficulty.rpy:177` |
| `r13_q1_press_done` | 2 | `systems/room13_q1_difficulty.rpy:199` |
| `r13_q1_removal_proved` | 2 | `systems/room13_q1_difficulty.rpy:43` |
| `r13_q1_review_lines` | 2 | `systems/room13_q1_arguments.rpy:231` |
| `r13_q1_review_rows` | 2 | `systems/room13_q1_arguments.rpy:210` |
| `r13_record_entries` | 2 | `systems/room13_learning.rpy:107` |
| `r13_rel_edges` | 2 | `systems/room13_v111_relations.rpy:88` |
| `r13_rel_status` | 2 | `systems/room13_v111_relations.rpy:42` |
| `r13_remember_line` | 2 | `systems/room13_question_discovery.rpy:176` |
| `r13_resident_where` | 2 | `systems/room13_new_places.rpy:105` |
| `r13_scene_treatment` | 2 | `systems/room13_stove_art.rpy:27` |
| `r13_secret_route_available` | 2 | `systems/room13_items.rpy:101` |
| `r13_semantic_text` | 2 | `systems/room13_name_accent.rpy:46` |
| `r13_shop_price` | 2 | `systems/room13_bundle3.rpy:50` |
| `r13_staged_visible_art` | 2 | `systems/room13_map_action27.rpy:87` |
| `r13_topic_current_context` | 2 | `systems/room13_piko_causality.rpy:62` |
| `r13_topic_current_lines` | 2 | `systems/room13_piko_causality.rpy:97` |
| `r13_v111_arrive` | 2 | `room13_v111_newworld_rules.rpy:447` |
| `r13_v111_context` | 2 | `systems/room13_camera_follow.rpy:10` |
| `r13_v111_line` | 2 | `room13_v111_newworld_text.rpy:542` |
| `r13_v111_lines` | 2 | `room13_v111_reactions.rpy:107` |
| `r13_v111_questions` | 2 | `room13_v111_reactions.rpy:81` |
| `r13_w2_action_done` | 2 | `systems/room13_week1_cases.rpy:50` |
| `r13_w2_present` | 2 | `systems/room13_present_flow.rpy:69` |
| `r13_world_edge_label` | 2 | `systems/room13_event_offers.rpy:94` |
| `r13_world_file` | 2 | `systems/room13_hidden_art.rpy:52` |
| `r13_world_props` | 2 | `room13_v111.rpy:252` |
| `r13_world_scene_location` | 2 | `systems/room13_hidden_art.rpy:59` |
