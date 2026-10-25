# 이야기 총정리 · 자동 부분

> 이 파일은 손으로 고치지 않는다. 다시 만들기: `python3 dev/story_master.py --write` (`experiments/renpy-ch1` 에서).
> 사람이 쓰는 부분(사건 여섯 칸 · 감정선 · 퍼즐 · 현행/설계)은 `docs/design/story_master.md`.
> 읽은 곳: `game/room13_v111_days123.rpy`, `game/room13_v111_days45.rpy`, `game/room13_v111_days610.rpy`, `game/room13_v111_days1114.rpy`, `game/room13_v111_owl_prevent.rpy`, `game/room13_hidden_pandol.rpy`, `game/room13_hidden_base.rpy`, `game/room13_lamp_attempt.rpy`, `game/room13_v111_newworld_rules.rpy`, `game/room13_v111_newworld_text.rpy`, `game/room13_fork_screen.rpy`, 장면 제목은 `docs/story-ms14/source/` 원본.
> 글자로 읽은 것이라 갈래 순서·조건이 실제 재생과 다를 수 있다. 의심스러우면 표에 적힌 파일:줄을 연다.

자동 추출 실패: 1곳 (맨 아래 목록)

## 차례

1. 날짜별 장면 순서
2. 회의
3. 생사 · 명단 · 결말
4. 조건 이름
5. 자동 추출 실패

## 1. 날짜별 장면 순서

파일 안 순서대로 장면을 늘어놓았다(실제 재생 순서와 대체로 같고, 갈래가 나뉘는 날은 갈래마다 따로 나온다).
「인물」은 그 장면 안에서 `r13_v111_arrive`/`r13_v111_join` 으로 세운 사람 전부(갈래에 따라 일부만 선다).
「갈림」은 메뉴 보기(조건)와 `if` 조건, 「값」은 그 장면에서 바뀌는 판정 값이다.

### 1일

| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |
|---|---|---|---|---|
| `MS14_D01_S01` | 1. 마차 / 엄마 몫 · 1일 낮 / 움직이는 마차 | 눈에 막힌 입구(gate) | — | `r13_v111_start_block`, `r13_v111_letter_open`, `r13_v111_letter_read`, `r13_v111_letter_menu`, `r13_v111_letter_last`, `r13_v111_letter_hand` 외 6 |
| `MS14_D01_S02` | 2. 초소 / 한 사람의 허가 · 1일 도착 / 초소 입구→내부 | 눈에 막힌 입구(gate) | — | `r13_v111_gate_arrival`, `r13_v111_gate_request`, `r13_v111_gate_list`, `r13_v111_gate_choice`, `r13_v111_gate_letter`, `r13_v111_gate_original` 외 2 |
| `MS14_D01_S03` | 3. 초소 / 둘이 들어갈 근거 · 1일 / 초소 첫 추리 | — | — | `r13_v111_gate_read_original`, `r13_v111_gate_read_rules`, `r13_v111_gate_reread_list`, `r13_v111_gate_purpose`, `r13_v111_gate_lodging`, `r13_v111_gate_proof` 외 7 |
| `MS14_D01_S04` | 4. 문이 열릴 때 / 이름 · 1일 / 초소 등록 후 입장 | 눈에 막힌 입구(gate) | — | `r13_v111_registered`, `r13_v111_registered_menu`, `r13_v111_registered_reason`, `r13_v111_registered_depart` |
| `MS14_D01_S05` | 5. 여관 13호 / 기다리지 않는 방 · 1일 저녁 / 로비→빈13호→밤 | 여관 접수대(inn), 여관 2층 · 13호실(room13) | — | `r13_v111_inn`, `r13_v111_room_observe`, `r13_v111_room_empty`, `r13_v111_note_pick`, `r13_v111_room_note`, `r13_v111_bundle_open` 외 5 |

#### `MS14_D01_S01` 갈림 · 값 (room13_v111_days123.rpy:9)

- `r13_v111_letter_open` if `v111_answer==0` `→ r13_v111_letter_read`
- `r13_v111_letter_menu` if 「마지막 줄을 본다」 `→ r13_v111_letter_last`
- `r13_v111_letter_menu` if 「글씨를 살핀다」 `→ r13_v111_letter_hand`
- `r13_v111_letter_menu` if 「편지를 접는다」 `→ r13_v111_letter_close`
- `r13_v111_letter_close` if `r13_v111_value('K01a')==True` `→ r13_v111_letter_any`
- `r13_v111_letter_close_b` if `r13_v111_value('K01b')==True` `→ r13_v111_letter_any`
- `r13_v111_leave_carriage` if `v111_answer==0` `→ r13_v111_gate_arrival`

#### `MS14_D01_S02` 갈림 · 값 (room13_v111_days123.rpy:99)

- `r13_v111_gate_request` if 「초소 처리 명단을 읽는다」 `→ r13_v111_gate_list`
- `r13_v111_gate_choice` if 「초대 편지를 보여 준다」 `→ r13_v111_gate_letter`
- `r13_v111_gate_choice` if 「방문 신청서를 찾아 달라고 한다」 `→ r13_v111_gate_original`
- `r13_v111_gate_investigate` if 「신청 원본을 읽는다」 `→ r13_v111_gate_read_original`
- `r13_v111_gate_investigate` if 「겨울철 입장 규칙을 읽는다」 `→ r13_v111_gate_read_rules`
- `r13_v111_gate_investigate` if 「초소 처리 명단을 다시 본다」 `→ r13_v111_gate_reread_list`
- `r13_v111_gate_investigate` if 「두 종이의 항목을 비교한다」 `→ r13_v111_gate_purpose`
- `r13_v111_gate_investigate` if 「숙소 확인 칸을 본다」 `→ r13_v111_gate_lodging`
- `r13_v111_gate_investigate` if 「자료를 함께 제시한다」 `→ r13_v111_gate_proof`
- `r13_v111_gate_investigate` if 「힌트를 생각한다」 `→ r13_v111_gate_hint`
- `r13_v111_gate_investigate` if 「명단을 옮겨 적은 경위를 묻는다」 `→ r13_v111_gate_reason`

#### `MS14_D01_S03` 갈림 · 값 (room13_v111_days123.rpy:181)

- `r13_v111_gate_proven_dispatch` if `r13_v111_value('purpose_difference_known')==True` `→ r13_v111_gate_proven`
- `r13_v111_gate_number` if `r13_nw_retry('gate')` `→ r13_v111_gate_investigate`
- `r13_v111_gate_wrong` if `r13_nw_retry('gate')` `→ r13_v111_gate_investigate`
- 값
  - 회의 끝 `gate` → `"win"` (`r13_v111_gate_proven`)
  - 회의 끝 `gate` → `"win"` (`r13_v111_gate_early`)
  - `gate_hardened` = `true` (`r13_v111_gate_number`)
  - `gate_daram_unlisted` = `true` (`r13_v111_gate_number`)
  - 회의 끝 `gate` → `"lose"` (`r13_v111_gate_number`)
  - `gate_daram_unlisted` = `true` (`r13_v111_gate_wrong`)
  - 회의 끝 `gate` → `"lose"` (`r13_v111_gate_wrong`)

#### `MS14_D01_S04` 갈림 · 값 (room13_v111_days123.rpy:279)

- `r13_v111_registered` if `r13_v111_value('gate_daram_unlisted')` `$ r13_v111_set('E05.variant','unlisted')`
- `r13_v111_registered_menu` if 「명단을 옮겨 적은 경위를 묻는다」 `→ r13_v111_registered_reason`
- `r13_v111_registered_menu` if 「짐을 찾아 여관으로 간다」 `→ r13_v111_registered_depart`
- 값
  - `E05.variant` = `"unlisted"` (`r13_v111_registered`)
  - `heard_inn_order1` = `true` (`r13_v111_registered_depart`)

#### `MS14_D01_S05` 갈림 · 값 (room13_v111_days123.rpy:317)

- `r13_v111_room_observe` if `not r13_v111_value('ui_room_arrival_seen')` `$ r13_v111_set('ui_room_arrival_seen',True)`
- `r13_v111_room_observe` if 「빈방을 살핀다」 `→ r13_v111_room_empty`
- `r13_v111_note_pick` if 「책상 메모를 집는다」 `→ r13_v111_room_note`
- `r13_v111_bundle_open` if 「서랍 밑 종이를 빼낸다」 `→ r13_v111_bundle_open`
- `r13_v111_bundle_open` if 「책상 아래 보따리를 연다」 `→ r13_v111_bundle`
- `r13_v111_sleep1` if 「과자를 두고 잠든다」 `→ r13_v111_day2`
- 값
  - `ui_room_arrival_seen` = `true` (`r13_v111_room_observe`)

### 2일

| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |
|---|---|---|---|---|
| `MS14_D02_S01` | 1. 광장 / 초롱의 손 · 2일 아침 / 마구간→등→북쪽 교환함 | 눈에 막힌 입구(gate), 돌이 있는 광장(square), 마을 서쪽 · 길 없는 숲(forest) | — | `r13_v111_day2`, `r13_v111_square2`, `r13_v111_lamp_rope`, `r13_v111_chorong`, `r13_v111_go_box`, `r13_v111_box_path` 외 4 |
| `MS14_D02_S02` | 2. 우체국 / 내 편지부터 · 2일 낮 / 우체국 | 우체국 입구(post) | 모모 | `r13_v111_post`, `r13_v111_envelope_show`, `r13_v111_post_checked`, `r13_v111_post_menu`, `r13_v111_post_scribe`, `r13_v111_post_return` |
| `MS14_D02_S03` | 3. 3번 등 / 초상 의뢰 · 2일 오후 / 3번등 화가 자리 | 돌이 있는 광장(square) | — | `r13_v111_piko2`, `r13_v111_portrait_ask`, `r13_v111_portrait_commission`, `r13_v111_lamp_observe`, `r13_v111_lamp_seen_0`, `r13_v111_lamp_seen_1` 외 3 |
| `MS14_D02_S04` | 4. 식당 / 부탁은 자리가 되기까지 · 2일 해지기 전 한 번의 기회 / 식당↔북쪽길 | 여관 식당(dining), 여관 접수대(inn), 돌이 있는 광장(square), 마을 서쪽 · 길 없는 숲(forest), 여관 2층 · 13호실(room13) | — | `r13_v111_diner_offer`, `r13_v111_afternoon`, `r13_v111_shelter_choice`, `r13_v111_shelter_work`, `r13_v111_shelter_prepare`, `r13_v111_shelter_enter` 외 4 |
| `MS14_D02_S05` | 5. 여관 / 설명할 수 없는 빈칸 · 2일 밤 / 여관 로비→13호 | 여관 접수대(inn), 여관 2층 · 13호실(room13) | — | `r13_v111_evening2`, `r13_v111_evening2_route`, `r13_v111_evening2_alive`, `r13_v111_evening2_outside`, `r13_v111_evening2_end`, `r13_v111_sleep2` 외 1 |

#### `MS14_D02_S01` 갈림 · 값 (room13_v111_days123.rpy:421)

- `r13_v111_lamp_rope` if 「덮개 지지 끈을 잡는다」 `→ r13_v111_chorong`
- `r13_v111_go_box` if 「초롱과 교환함으로 간다」 `→ r13_v111_box_path`
- `r13_v111_box_inspect` if 「함과 주변을 직접 확인한다」 `→ r13_v111_box_empty`
- `r13_v111_box_note` if 「도착 쪽지를 직접 넣는다」 `→ r13_v111_box_written`

#### `MS14_D02_S02` 갈림 · 값 (room13_v111_days123.rpy:497)

- `r13_v111_envelope_show` if 「초대 편지의 봉투를 보여 준다」 `→ r13_v111_post_checked`
- `r13_v111_post_menu` if 「대필도 합니까?」 `→ r13_v111_post_scribe`
- `r13_v111_post_menu` if 「내 편지를 돌려받는다」 `→ r13_v111_post_return`

#### `MS14_D02_S03` 갈림 · 값 (room13_v111_days123.rpy:549)

- `r13_v111_portrait_ask` if 「스케치를 보여 주고 부탁한다」 `→ r13_v111_portrait_commission`
- `r13_v111_lamp_observe` if `all(r13_v111_value("lamp_part_%d"%i) for i in range(4))` `→ r13_v111_lamp_details`
- `r13_v111_lamp_observe` if 「번호판을 본다」 `→ r13_v111_lamp_seen_0`
- `r13_v111_lamp_observe` if 「덮개를 본다」 `→ r13_v111_lamp_seen_1`
- `r13_v111_lamp_observe` if 「담요를 본다」 `→ r13_v111_lamp_seen_2`
- `r13_v111_lamp_observe` if 「받침과 바닥을 본다」 `→ r13_v111_lamp_seen_3`
- `r13_v111_lamp_observe` if 「살펴보기를 마친다」 `→ r13_v111_lamp_details`
- 값
  - 자료 얻음 `NW_PIKO_TREMOR` (`r13_v111_portrait_commission`)

#### `MS14_D02_S04` 갈림 · 값 (room13_v111_days123.rpy:634)

- `r13_v111_afternoon` if 「포대를 옮긴다」 `$ r13_v111_set('piko_sacks2',True)`
- `r13_v111_afternoon` elif 「마른 천을 빌린다」 `$ r13_v111_set('piko_cloth2',True)`
- `r13_v111_afternoon` elif 「벤치 표면을 살핀다」 `$ r13_v111_set('piko_bench_seen2',True)`
- `r13_v111_afternoon` elif 「천으로 벤치의 물감을 닦는다」 `$ r13_v111_set('piko_bench_clean2',True)`
- `r13_v111_afternoon` elif 「식당에 앉을 자리를 전한다」 `→ r13_v111_shelter_prepare`
- `r13_v111_afternoon` elif 「네로를 만나러 간다」 `→ r13_v111_nero_choice`
- `r13_v111_shelter_work` if 「비운 벤치와 조건을 전한다」 `→ r13_v111_shelter_prepare`
- `r13_v111_shelter_enter` if 「피코와 식당에 들어간다」 `→ r13_v111_shelter_done`
- `r13_v111_nero_work` if 「침구를 옮겨 묶고 이름을 적는다」 `→ r13_v111_nero_done`
- 값
  - `piko_sacks2` = `true` (`r13_v111_afternoon`)
  - `piko_cloth2` = `true` (`r13_v111_afternoon`)
  - `piko_bench_seen2` = `true` (`r13_v111_afternoon`)
  - `piko_bench_clean2` = `true` (`r13_v111_afternoon`)
  - 생사 판정 `fate_piko` = `saved` (`r13_v111_shelter_done`)

#### `MS14_D02_S05` 갈림 · 값 (room13_v111_days123.rpy:750)

- `r13_v111_evening2_route` if `r13_v111_value('piko_sheltered')==True` `→ r13_v111_evening2_alive`
- `r13_v111_sleep2` if 「아침 약속을 적고 잠든다」 `→ r13_v111_day3`
- `r13_v111_day3` if `r13_v111_value('lamp_bound2')` `→ r13_lamp_attempt3`
- `r13_v111_day3` if `not r13_v111_value('piko_sheltered')` `$ r13_fork_set_fate('fate_piko','lost')`
- `r13_v111_day3` if `r13_v111_value('piko_sheltered')==True` `→ r13_v111_piko_alive3`
- 값
  - 생사 판정 `fate_piko` = `saved` (`r13_v111_day3`)
  - 생사 판정 `fate_piko` = `lost` (`r13_v111_day3`)

### 3일

| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |
|---|---|---|---|---|
| `MS14_D03_S01` | 1. 아침 / 두 가지 약속의 끝 · 3일 새벽~아침 / 광장 사망 또는 식당 생존 | 여관 식당(dining), 돌이 있는 광장(square) | 피코, 초롱, 톡, 다람 | `r13_v111_piko_alive3`, `r13_v111_piko_clean`, `r13_v111_piko_receive`, `r13_v111_piko_dead3`, `r13_lamp_attempt3`, `r13_lamp_attempt_field3` |
| `MS14_D03_S02` | 2. 광장 / 먼저 묶인 손 · 3일 아침 / 3번등 공개 조사 | 돌이 있는 광장(square) | — | `r13_v111_lamp3`, `r13_v111_lamp_inspect3`, `r13_v111_lamp_interior3`, `r13_v111_fragment_request`, `r13_v111_lamp_fragment3`, `r13_v111_lamp_log_request` 외 1 |
| `MS14_D03_S03` | 3. 공방과 진료소 / 돌려놓았다는 말 · 3일 오전 / 공방→진료소 | 수리점(workshop), 임시 진료실(clinic) | 부리, 부엉이 할아버지 | `r13_v111_workshop3`, `r13_v111_loan_read`, `r13_v111_loan3`, `r13_v111_clinic3`, `r13_v111_measurement_read`, `r13_v111_measurement3` 외 6 |
| `MS14_D03_S04` | 4. 짐 내리는 골목 / 식구의 빵 · 3일 낮 / 골목→허락된 창고→공개확인 | 돌이 있는 광장(square), 공동 물품 창고(store), 수리점(workshop) | — | `r13_v111_silluk3`, `r13_v111_transport_read`, `r13_v111_transport3`, `r13_v111_knife_permission`, `r13_v111_knife_observed`, `r13_v111_store_visit` 외 5 |
| `MS14_D03_S05` | 5. 광장 공방 / 무엇을 증명했는가 · 3일 오후 / 등 앞 공방 | 수리점(workshop), 돌이 있는 광장(square) | 톡, 초롱, 실룩, 너울, 다람, 피코 | `r13_v111_trial_open`, `r13_v111_trial_repair`, `r13_v111_trial_repair_ok`, `r13_v111_trial_sale`, `r13_v111_trial_sale_ok`, `r13_v111_trial_knife` 외 36 |
| `MS14_D03_S06` | 6. 저녁 / 그려지지 않은 얼굴 · 3일 저녁 / 등 복구·초상·물자인수 | 돌이 있는 광장(square), 임시 진료실(clinic), 여관 2층 · 13호실(room13) | — | `r13_v111_restore3`, `r13_v111_restore_defer`, `r13_v111_box_news3`, `r13_v111_memorial_route`, `r13_v111_piko_evening`, `r13_v111_piko_memorial` 외 6 |

#### `MS14_D03_S01` 갈림 · 값 (room13_v111_days123.rpy:805)

- `r13_v111_piko_clean` if 「약속한 자리를 치운다」 `→ r13_v111_piko_receive`
- `r13_lamp_attempt_field3` if 「공방에서 함께 확인한다」 `→ r13_lamp_attempt_open3`
- `r13_lamp_attempt_field3` elif 「돌받침 안쪽을 살피고 조각을 담는다」 `$ r13_nw_acquire("NW_LA_CHECK")`
- `r13_lamp_attempt_field3` elif 「칼과 조각의 대조를 부탁한다」 `$ r13_nw_acquire("NW_LA_KNIFE")`
- `r13_lamp_attempt_field3` elif 「매입 장부와 약속한 값을 확인한다」 `$ r13_nw_acquire("NW_LA_OFFER")`
- 값
  - `piko_alive` = `true` (`r13_lamp_attempt3`)
  - `piko.location` = `"square"` (`r13_lamp_attempt3`)
  - 자료 얻음 `NW_LA_CHECK` (`r13_lamp_attempt_field3`)
  - 자료 얻음 `NW_LA_FIELD` (`r13_lamp_attempt_field3`)
  - `lamp_field_done3` = `true` (`r13_lamp_attempt_field3`)
  - 자료 얻음 `NW_LA_KNIFE` (`r13_lamp_attempt_field3`)
  - `lamp_knife_done3` = `true` (`r13_lamp_attempt_field3`)
  - 자료 얻음 `NW_LA_OFFER` (`r13_lamp_attempt_field3`)
  - 자료 얻음 `NW_INNER_PRICE` (`r13_lamp_attempt_field3`)
  - 자료 얻음 `NW_KEEPER_DATE` (`r13_lamp_attempt_field3`)
  - `lamp_store_done3` = `true` (`r13_lamp_attempt_field3`)

#### `MS14_D03_S02` 갈림 · 값 (room13_v111_days123.rpy:838)

- `r13_v111_lamp_inspect3` if 「번호판·받침·자국을 살핀다」 `→ r13_v111_lamp_interior3`
- `r13_v111_fragment_request` if 「톡에게 안쪽 파편을 확인받는다」 `→ r13_v111_lamp_fragment3`
- `r13_v111_lamp_log_request` if 「초롱의 점검장을 확인한다」 `→ r13_v111_lamp_log3`

#### `MS14_D03_S03` 갈림 · 값 (room13_v111_days123.rpy:893)

- `r13_v111_loan_read` if 「대여 쪽지를 읽는다」 `→ r13_v111_loan3`
- `r13_v111_measurement_read` if 「측정지를 읽는다」 `→ r13_v111_measurement3`

#### `MS14_D03_S04` 갈림 · 값 (room13_v111_days123.rpy:985)

- `r13_v111_transport_read` if 「운반표를 본다」 `→ r13_v111_transport3`
- `r13_v111_knife_permission` if 「칼을 보여 달라고 요청한다」 `→ r13_v111_knife_observed`
- `r13_v111_store_visit` if 「수취 창고에서 확인한다」 `→ r13_v111_store3`
- `r13_v111_stone_check` if 「톡에게 각인 확인을 부탁한다」 `→ r13_v111_stone3`
- `r13_v111_sale_check` if 「매입 기록을 본다」 `→ r13_v111_sale3`
- 값
  - 자료 얻음 `NW_INNER_PRICE` (`r13_v111_sale3`)
  - 자료 얻음 `NW_KEEPER_DATE` (`r13_v111_sale3`)

#### `MS14_D03_S05` 갈림 · 값 (room13_v111_days123.rpy:1079)

- `r13_v111_trial_repair` if `r13_v111_value('lamp_bound2')` `→ r13_lamp_attempt_repair3`
- `r13_v111_trial_knife` if 「안쪽 파편과 칼끝을 대조한다」 `→ r13_v111_knife_fit`
- `r13_v111_trial_knife` if 「칼 모양만으로 지목한다」 `→ r13_v111_knife_wrong`
- `r13_v111_trial_knife` if 「자료를 다시 본다」 `→ r13_v111_trial_knife_records`
- `r13_v111_knife_wrong` if `r13_nw_retry('lamp')` `→ r13_v111_trial_knife`
- `r13_v111_trial_piko` if `r13_v111_value('piko_alive')==True` `→ r13_v111_trial_alive`
- `r13_v111_stone_choice` if 「확인된 3번 돌을 돌려 달라고 한다」 `→ r13_v111_stone_return`
- `r13_v111_stone_choice` if 「오늘은 반환 요구를 보류한다」 `→ r13_v111_stone_defer`
- `r13_v111_custody_choice` if `r13_v111_value('meeting:lamp')!='win'` `→ r13_v111_restore_route`
- `r13_v111_custody_choice` if 「지금 데려가지 못하게 하고 내일 다시 나오게 한다」 `→ r13_v111_silluk_report`
- `r13_v111_custody_choice` if 「증거를 넘기고 너울이 실룩을 데려가게 한다」 `→ r13_v111_silluk_transfer`
- `r13_v111_trial_wrong` if `r13_nw_retry('lamp')` `→ r13_v111_trial_repair`
- `r13_v111_trial_wrong_sale` if `r13_nw_retry('lamp')` `→ r13_v111_trial_sale`
- `r13_v111_trial_wrong_latch` if `r13_nw_retry('lamp')` `→ r13_v111_trial_latch`
- `r13_v111_trial_wrong_stone` if `r13_nw_retry('lamp')` `→ r13_v111_trial_stone`
- `r13_v111_restore_route` if `r13_v111_value('lamp_bound2')` `→ r13_lamp_attempt_after3`
- `r13_v111_restore_route` if `r13_v111_value('public_stones')=='returned_uninstalled'` `→ r13_v111_restore_input`
- `r13_v111_restore_input` if `r13_v111_value('meeting:lamp')=='lose'` `→ r13_v111_restore3`
- `r13_v111_restore_input` if 「톡·초롱과 3번 돌을 복구한다」 `→ r13_v111_restore3`
- `r13_lamp_attempt_wrong3` if `r13_nw_retry('lamp')` `→ r13_lamp_attempt_repair3`
- `r13_lamp_attempt_partial3` if `r13_nw_retry('lamp')` `→ r13_lamp_attempt_final3`
- 값
  - 회의 끝 `lamp` → `"partial"` (`r13_v111_knife_wrong`)
  - 회의 끝 `lamp` → `"win"` (`r13_v111_badugi_arrives`)
  - `silluk_status` = `"released"` (`r13_v111_custody_choice`)
  - 명단 올림 실룩 (까닭 `lamp_transfer`) (`r13_v111_silluk_transfer`)
  - 회의 끝 `lamp` → `"lose"` (`r13_v111_trial_wrong`)
  - 명단 올림 톡 (까닭 `lamp_lose`) (`r13_v111_trial_wrong`)
  - 회의 끝 `lamp` → `"partial"` (`r13_v111_trial_wrong_sale`)
  - 회의 끝 `lamp` → `"partial"` (`r13_v111_trial_wrong_latch`)
  - 회의 끝 `lamp` → `"partial"` (`r13_v111_trial_wrong_stone`)
  - `silluk.children.location` = `"workshop_with_buri"` (`r13_lamp_attempt_open3`)
  - `repair_opening_separated` = `true` (`r13_lamp_attempt_repair_ok3`)
  - 회의 끝 `lamp` → `"lose"` (`r13_lamp_attempt_wrong3`)
  - 명단 올림 톡 (까닭 `lamp_lose`) (`r13_lamp_attempt_wrong3`)
  - 회의 끝 `lamp` → `"partial"` (`r13_lamp_attempt_partial3`)
  - `outer_latch_claim_refuted` = `true` (`r13_lamp_attempt_win3`)
  - 회의 끝 `lamp` → `"win"` (`r13_lamp_attempt_win3`)
  - `stone_warm_felt3` = `true` (`r13_lamp_attempt_after3`)
  - `piko.location` = `"clinic"` (`r13_lamp_attempt_after3`)

#### `MS14_D03_S06` 갈림 · 값 (room13_v111_days123.rpy:1350)

- `r13_v111_memorial_route` if `r13_v111_value('piko_alive')==True` `→ r13_v111_piko_evening`
- `r13_v111_blankets_route` if `r13_v111_value('nero_bedding_reserved')==True` `→ r13_v111_blankets_receive`
- `r13_v111_blankets_receive` if 「예약한 침구를 확인해 받는다」 `→ r13_v111_blankets3`
- `r13_v111_sleep3` if 「그림을 세워 두고 잠든다」 `→ r13_v111_day4`
- 값
  - `stone_warm_felt3` = `true` (`r13_v111_restore3`)

### 4일

| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |
|---|---|---|---|---|
| `MS14_D04_S01` | 1. 솜이네 골목 / 닫힌 뒷문 · 4일 아침 / 조건부노동현장→솜이네문 | v111_labor, 솜이네 골목(ms14_somi) | 다람, 실룩, 너울, 네로, 솜이, 아랫길 노인 | `r13_v111_labor4`, `r13_v111_labor_sheet4`, `r13_v111_labor_confirm4`, `r13_v111_somi4`, `r13_v111_nero_route4`, `r13_v111_nero_known4` 외 6 |
| `MS14_D04_S02` | 2. 처마 / 도토리 세 개 · 4일 낮 / 광장처마→오후방문후퇴 | 돌이 있는 광장(square), 솜이네 골목(ms14_somi) | 다람, 콩이, 토실, 밤이, 초롱 | `r13_v111_eaves4`, `r13_v111_portrait_place4`, `r13_v111_bami_mother4` |
| `MS14_D04_S03` | 3. 저녁 초소 뒤 / 비명 · 4일 저녁 / 초소뒷길 | 눈에 막힌 입구(gate) | 다람, 돌목, 너울, 바둑이 | `r13_v111_cry4`, `r13_v111_look_gate4`, `r13_v111_bite4` |
| `MS14_D04_S04` | 4. 같은 밤 / 잘못 적은 키 · 4일 밤 / 밝은초소→문앞울타리→식당 | 밝은 초소 안(ms14_guardroom), 눈에 막힌 입구(gate), 여관 식당(dining), 돌이 있는 광장(square), 여관 2층 · 13호실(room13) | 다람, 바둑이, 밤이, 피코, 꼬미 | `r13_v111_testimony4`, `r13_v111_bami_ask4`, `r13_v111_bami_night4`, `r13_v111_inspect_gate4`, `r13_v111_fence_seen4`, `r13_v111_tracks_seen4` 외 9 |

#### `MS14_D04_S01` 갈림 · 값 (room13_v111_days45.rpy:10)

- `r13_v111_labor_sheet4` if 「작업표를 보여 주십시오.」 `→ r13_v111_labor_confirm4`
- `r13_v111_nero_route4` if `r13_v111_value('nero_met_day2')` `→ r13_v111_nero_known4`
- `r13_v111_nero_help4` if 「침구와 물통을 돕는다」 `→ r13_v111_nero_help_done4`
- `r13_v111_portrait_show4` if 「이분을 보셨습니까?」 `→ r13_v111_somi_talk4`

#### `MS14_D04_S02` 갈림 · 값 (room13_v111_days45.rpy:126)

- `r13_v111_eaves4` if `r13_v111_value('silluk_status')=='reporting_obligation' and not r13_v111_value('bami_cold4')` `$ r13_v111_set('bami_cold4',True)`
- `r13_v111_portrait_place4` if 「여기 두고 물러날게.」 `→ r13_v111_bami_mother4`
- 값
  - `bami_cold4` = `true` (`r13_v111_eaves4`)

#### `MS14_D04_S03` 갈림 · 값 (room13_v111_days45.rpy:178)

- `r13_v111_look_gate4` if 「밝은 쪽에서 살핀다」 `→ r13_v111_bite4`

#### `MS14_D04_S04` 갈림 · 값 (room13_v111_days45.rpy:220)

- `r13_v111_bami_ask4` if 「어디서 봤니?」 `→ r13_v111_bami_night4`
- `r13_v111_inspect_gate4` if 「울타리 천」 `→ r13_v111_fence_seen4`
- `r13_v111_inspect_gate4` if 「겹친 발자국」 `→ r13_v111_tracks_seen4`
- `r13_v111_inspect_gate4` if 「엎어진 양동이」 `→ r13_v111_bucket_seen4`
- `r13_v111_inspection_ready4` if `all(r13_v111_value(k) for k in ['d4_fence_seen', 'd4_tracks_seen', 'd4_bucket_seen'])` `→ r13_v111_tracks_talk4`
- `r13_v111_collect4` if 「같이 천을 수거해 주십시오.」 `→ r13_v111_cloth4`
- `r13_v111_sleep4` if 「관찰과 추측을 나눠 적고 잔다」 `→ r13_v111_morning5`
- 값
  - `d4_fence_seen` = `true` (`r13_v111_fence_seen4`)
  - `d4_tracks_seen` = `true` (`r13_v111_tracks_seen4`)
  - `d4_bucket_seen` = `true` (`r13_v111_bucket_seen4`)
  - `piko.location` = `"dining"` (`r13_v111_piko_sketch4`)
  - 자료 얻음 `NW_PIKO_SKETCH4` (`r13_v111_piko_sketch4`)
  - `piko.location` = `"clinic"` (`r13_v111_piko_sketch4`)
  - `day` = `5` (`r13_v111_morning5`)

### 5일

| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |
|---|---|---|---|---|
| `MS14_D05_S01` | 1. 솜이네 / 손바닥 · 5일 아침 / 솜이네안 | 솜이네 골목(ms14_somi), 솜이네 방(ms14_somi_inside) | 다람, 네로, 솜이, 무쇠 | `r13_v111_somi5` |
| `MS14_D05_S02` | 2. 문턱 / 숨긴 것과 일어난 것 · 5일 오전 / 솜이네→진료소문→초소 | 솜이네 방(ms14_somi_inside), 임시 진료실(clinic) | 다람, 네로, 솜이, 무쇠 | `r13_v111_wait_cloth5`, `r13_v111_compare_cloth5`, `r13_v111_cloth_match5` |
| `MS14_D05_S03` | 3. 초소 / 사라지지 않는 상처 · 5일 낮 / 초소밤이혐의검증 | 눈에 막힌 입구(gate) | 다람, 돌목, 너울, 네로, 바둑이, 콩이 | `r13_v111_hearing5`, `r13_v111_proof5`, `r13_v111_wrong5`, `r13_v111_hint5`, `r13_v111_bami_clear5` |
| `MS14_D05_S04` | 4. 점심 무렵 / 이제 도착한 경고 · 5일 점심무렵 / 초소앞바람막힌곳 | 눈에 막힌 입구(gate) | 다람, 초롱 | `r13_v111_warning5`, `r13_v111_envelope5`, `r13_v111_warning_read5`, `r13_v111_warning_compare5`, `r13_v111_warning_retry5`, `r13_v111_warning_compared5` 외 2 |
| `MS14_D05_S05` | 5. 저녁 / 맡긴다는 말의 무게 · 5일 저녁 / 솜이네→식당→같은복도→13호 | 솜이네 방(ms14_somi_inside), 여관 식당(dining), 여관 접수대(inn), 여관 2층 복도(hall), 여관 2층 · 13호실(room13) | 다람, 솜이, 무쇠, 네로, 바둑이, 까로, 부엉이 할아버지 | `r13_v111_night5`, `r13_v111_owl_glove5`, `r13_v111_lock_check5`, `r13_v111_blankets5`, `r13_v111_packed5`, `r13_v111_empty_bag5` 외 3 |

#### `MS14_D05_S01` 갈림 · 값 (room13_v111_days45.rpy:389)

- 값
  - 자료 얻음 `NW_MUSOE_DEEP` (`r13_v111_somi5`)

#### `MS14_D05_S02` 갈림 · 값 (room13_v111_days45.rpy:422)

- `r13_v111_compare_cloth5` if 「허락받은 옷과 천을 대조한다」 `→ r13_v111_cloth_match5`

#### `MS14_D05_S03` 갈림 · 값 (room13_v111_days45.rpy:469)

- `r13_v111_proof5` if `r13_v111_value('bami_cold4') and not r13_v111_value('gate_post_cold_cost')` `$ r13_v111_set('gate_post_cold_cost',True)`
- `r13_v111_wrong5` if `r13_nw_retry("gate_post",["E20","E22","E23","E24"],"돌목이 고개를 젓는다. 천과 겉옷, 진술을 함께 놓아야 한다.")` `→ r13_v111_proof5`
- 값
  - `gate_post_cold_cost` = `true` (`r13_v111_proof5`)
  - `tries:gate_post` = `(r13_v111_value('tries:gate_post') or 0)+1` (`r13_v111_proof5`)
  - 회의 끝 `gate_post` → `"lose"` (`r13_v111_wrong5`)
  - 명단 올림 밤이 (까닭 `gate_post_lose`) (`r13_v111_wrong5`)
  - `bami_status` = `"listed"` (`r13_v111_wrong5`)
  - 회의 끝 `gate_post` → `"win"` (`r13_v111_bami_clear5`)

#### `MS14_D05_S04` 갈림 · 값 (room13_v111_days45.rpy:533)

- `r13_v111_envelope5` if 「봉투를 받겠습니다.」 `→ r13_v111_warning_read5`
- 메뉴 `r13_v111_warning_compared5` (576줄)
  - 「첫날 기록을 다시 본다」
  - 「답장을 쓴다」
- `r13_v111_reply_handoff5` if 「답장을 맡기겠습니다.」 `→ r13_v111_reply_done5`

#### `MS14_D05_S05` 갈림 · 값 (room13_v111_days45.rpy:612)

- `r13_v111_night5` if `R13_NW_WHEN["tok_freed3"]() and r13_v111_person_alive("karo")` `$ r13_v111_join(['karo'])`
- `r13_v111_lock_check5` if 「문과 창문 잠금을 확인한다」 `→ r13_v111_safety5`
- `r13_v111_blankets5` if `r13_v111_value('carried_dry_blankets')==2` `→ r13_v111_packed5`
- `r13_v111_sleep5` if 「아침 일정을 정하고 잔다」 `→ r13_v111_morning6`
- 값
  - `day` = `6` (`r13_v111_morning6`)

### 6일

| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |
|---|---|---|---|---|
| `MS14_D06_S01` | 6-1. 오전 / 학교 뒤문 — 엄마에게 갈 물건 · ['SCHOOL_REAR', 'INN_REAR'] | 마을 학교(school), 여관 식당(dining) | 다람, 사자 선생님, 초롱, 꼬미 | `r13_v111_day6`, `r13_v111_bowl_together6`, `r13_v111_bowl_eat6`, `r13_v111_nabi_supply6`, `r13_v111_board6`, `r13_v111_board_done6` |
| `MS14_D06_S02` | 6-2. 오후 / 장작 창고 — 안전한 곳이라는 말 · ['WOODSHED', 'SCHOOL_REAR'] | v111_woodshed | 다람, 꼬미, 보리 | `r13_v111_woodshed6`, `r13_v111_woodshed_check6`, `r13_v111_woodshed_seen6`, `r13_v111_afternoon6` |
| `MS14_D06_P01` | D06_P01 — 오늘 옮기는 경로 · ['SCHOOL_ROOM'] | v111_woodshed, 마을 학교(school) | 다람, 사자 선생님, 꼬미, 보리, 도토 | `r13_v111_seat6`, `r13_v111_fetch6`, `r13_v111_today6`, `r13_v111_permission6`, `r13_v111_permission_today6`, `r13_v111_acorn_recover6` 외 4 |
| `MS14_D06_S03P` | D06_S03P — 빈 창고의 불 · ['WOODSHED', 'SCHOOL_ROOM'] | v111_fire | 보리, 도토 | `r13_v111_empty_fire6` |
| `MS14_D06_S03` | 6-3. 해 질 무렵 / 창고 바깥 — 먼저 꺼낼 것 · ['WOODSHED'] | v111_fire, 마을 학교(school) | 다람, 보리 | `r13_v111_fire6`, `r13_v111_wet_cloth6`, `r13_v111_wet_done6`, `r13_v111_clear_wood6`, `r13_v111_rescue_done6` |
| `MS14_D06_S04` | 6-4. 밤 / 학교 난로 곁 — 세 가지 잘못 · ['SCHOOL_ROOM', 'WOODSHED'] | 마을 학교(school), v111_ruin | 다람, 나비, 보리, 너울, 도토 | `r13_v111_after_fire6`, `r13_v111_fire_evidence6`, `r13_v111_fire_record6`, `r13_v111_bowl_result6`, `r13_v111_four_bowls6`, `r13_v111_empty_bowl6` 외 4 |

#### `MS14_D06_S01` 갈림 · 값 (room13_v111_days610.rpy:4)

- 메뉴 `r13_v111_day6` (36줄)
  - 「그릇을 돌려주러 같이 가자.」 `$ r13_v111_set('choice:MS14_D06_S01','together')`
  - 「오늘은 먹었니? 먹을 것부터 알아보자.」 `$ r13_v111_set('choice:MS14_D06_S01','eat_first')`
- `r13_v111_board6` if 「공개 보급판을 확인한다」 `→ r13_v111_board_done6`
- 값
  - `choice:MS14_D06_S01` = `"together"` (`r13_v111_day6`)
  - `choice:MS14_D06_S01` = `"eat_first"` (`r13_v111_day6`)

#### `MS14_D06_S02` 갈림 · 값 (room13_v111_days610.rpy:96)

- `r13_v111_woodshed_check6` if 「문 앞과 뒤창을 살핀다」 `→ r13_v111_woodshed_seen6`
- `r13_v111_afternoon6` if 「장작더미 옆 깡통 줄을 살핀다」 `→ r13_v111_afternoon6`
- `r13_v111_afternoon6` if 「줄을 풀고 도토리를 챙긴다」 `→ r13_v111_afternoon6`
- `r13_v111_afternoon6` if 「아이들 자리를 여쭌다」 `→ r13_v111_seat6`
- `r13_v111_afternoon6` if 「학교에 자리가 났어. 같이 갈래?」 `→ r13_v111_afternoon6`
- `r13_v111_afternoon6` if `not r13_v111_value('acorn_recovered')` `→ r13_v111_afternoon6`
- `r13_v111_afternoon6` if 「내일 아침에 데리러 올게」 `→ r13_v111_permission6`
- 값
  - 자료 얻음 `NW_KKOMI_NOSTONE` (`r13_v111_woodshed6`)
  - `kkomi_can_seen6` = `true` (`r13_v111_afternoon6`)
  - `acorn_recovered` = `true` (`r13_v111_afternoon6`)
  - `choice:MS14_D06_S02` = `"today"` (`r13_v111_afternoon6`)
  - `choice:MS14_D06_S02` = `"permission"` (`r13_v111_afternoon6`)
  - 생사 판정 `fate_kkomi` = `lost` (`r13_v111_afternoon6`)

#### `MS14_D06_P01` 갈림 · 값 (room13_v111_days610.rpy:169)

- `r13_v111_acorn_recover6` if 「깡통의 도토리도 챙겨 줄래?」 `→ r13_v111_acorn_recovered6`
- `r13_v111_handoff6` if 「네 아이와 물자를 확인한다」 `→ r13_v111_handoff_done6`
- 값
  - `evacuation_requested` = `true` (`r13_v111_seat6`)
  - `kkomi_seat6` = `true` (`r13_v111_seat6`)
  - `acorn_recovered` = `true` (`r13_v111_acorn_recovered6`)
  - 생사 판정 `fate_kkomi` = `saved` (`r13_v111_handoff_done6`)

#### `MS14_D06_S03` 갈림 · 값 (room13_v111_days610.rpy:273)

- `r13_v111_wet_cloth6` if 「물에 적신 천을 건넨다」 `→ r13_v111_wet_done6`
- `r13_v111_clear_wood6` if 「옆문 장작을 치운다」 `→ r13_v111_rescue_done6`

#### `MS14_D06_S04` 갈림 · 값 (room13_v111_days610.rpy:320)

- `r13_v111_fire_evidence6` if 「등잔과 천을 따로 확인한다」 `→ r13_v111_fire_record6`
- `r13_v111_bowl_result6` if `r13_v111_value('KKOMI_ALIVE')` `→ r13_v111_four_bowls6`
- `r13_v111_sleep6_input` if 「잠자리를 정리한다」 `→ r13_v111_sleep6_done`
- 값
  - `day` = `7` (`r13_v111_sleep6_done`)

### 7일

| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |
|---|---|---|---|---|
| `MS14_D07_S01` | 7-1. 오전 / 빨래터 — 내 아이들 몫 · ['LAUNDRY'] | 마을 빨래터(laundry), 마을 학교(school) | 누비, 보리, 나비, 사자 선생님, 누비의 큰아이, 누비의 둘째, 누비의 막내, 너울 | `r13_v111_day7`, `r13_v111_children_school7`, `r13_v111_children_here7`, `r13_v111_nubi_children_school7`, `r13_v111_nubi_children_receipt7`, `r13_v111_nubi_children_received7` 외 5 |
| `MS14_D07_S02` | 7-2. 낮 / 회관에서 학교까지 — 남은 사람의 자리 · ['HALL', 'SCHOOL_ROOM'] | 마을 학교(school) | 나비, 보리, 누비, 너울, 사자 선생님, 도토, 다람, 초롱, 도담 | `r13_v111_responsibility7`, `r13_v111_fire_basis_route7`, `r13_v111_empty_fire_basis7`, `r13_v111_rescue_fire_basis7`, `r13_v111_responsibility_wrong7`, `r13_v111_responsibility_answers7` 외 3 |
| `MS14_D07_S03` | 7-3. 저녁 / 여관 13호 — 잠깐이라는 약속 · ['ROOM13', 'INN_CORRIDOR'] | 여관 2층 · 13호실(room13) | 다람, 할머니, 부엉이 할아버지, 도토, 까로 | `r13_v111_room_visit7`, `r13_v111_handover7` |
| `MS14_D07_S04` | 7-4. 밤 / 초소에서 13호까지 — 열리지 않는 문 · ['SNOW_DETOUR', 'OUTPOST', 'INN_CORRIDOR', 'ROOM13'] | 임시 진료실(clinic), 여관 2층 복도(hall), 여관 2층 · 13호실(room13), 마을 학교(school) | 까로, 서리 검사원, 도토, 나비, 할머니, 너울, 다람 | `r13_v111_incident7`, `r13_v111_sleep7`, `r13_v111_free_sleep7`, `r13_v111_free_sleep7_input`, `r13_v111_free_sleep7_done`, `r13_v111_detained_sleep7` 외 3 |

#### `MS14_D07_S01` 갈림 · 값 (room13_v111_days610.rpy:437)

- 메뉴 `r13_v111_day7` (458줄)
  - 「아이들은 학교에서 기다리게 하자.」 `$ r13_v111_set('choice:MS14_D07_S01','school')`
  - 「여기서 계속 묻는다.」 `$ r13_v111_set('choice:MS14_D07_S01','here')`
- `r13_v111_nubi_children_receipt7` if 「누비 씨의 아이 셋 인수를 확인한다」 `→ r13_v111_nubi_children_received7`
- `r13_v111_bori_witness7` if 「창고 문 앞에서 무엇을 보셨습니까?」 `→ r13_v111_bori_witness_heard7`
- `r13_v111_nubi_wrong7` if `r13_nw_retry("fire")` `→ r13_v111_nubi_proof7`
- `r13_v111_nubi_admission7` if `not r13_v111_value("bori_nubi_door_witness_heard")` `→ r13_v111_bori_witness7`
- 값
  - `choice:MS14_D07_S01` = `"school"` (`r13_v111_day7`)
  - `choice:MS14_D07_S01` = `"here"` (`r13_v111_day7`)
  - `grand_snack_ready7` = `r13_v111_value("snack_bagged5") is True and not r13_v111_value("DARAM_DETAINED") and r13_v111_value("location:daram") in (None,"school") and not r13_v111_value("grand_ticket_spot_known") and not r13_v111_value("grand_snack_given7")` (`r13_v111_nubi_children_school7`)
  - `bori_nubi_door_witness_heard` = `true` (`r13_v111_bori_witness_heard7`)
  - 회의 끝 `fire` → `"lose"` (`r13_v111_nubi_wrong7`)
  - 명단 올림 보리 (까닭 `fire_lose`) (`r13_v111_nubi_wrong7`)

#### `MS14_D07_S02` 갈림 · 값 (room13_v111_days610.rpy:565)

- `r13_v111_responsibility7` if `r13_v111_value("meeting:fire")=="lose"` `→ r13_v111_responsibility_answers7`
- `r13_v111_fire_basis_route7` if `r13_v111_value('FIRE_EVACUATED')` `→ r13_v111_empty_fire_basis7`
- `r13_v111_responsibility_wrong7` if `r13_nw_retry("fire",["E06_FIRE","E06_EMPTY","E07_NUBI"] if r13_v111_value("FIRE_EVACUATED") else ["E06_FIRE","E06_RESCUE","E07_NUBI"],"너울이 고개를 젓는다. 불의 원인과 그날 밤 일을 함께 묶어야 한다.")` `→ r13_v111_fire_basis_route7`
- `r13_v111_responsibility_answers7` if `r13_v111_value("meeting:fire")=="win"` `$ r13_v111_set("fire_neoul_promise_recorded",True)`
- `r13_v111_responsibility_answers7` if `r13_nw_grand(["불의 원인과 빈 창고 진압을 구분한다","불의 원인과 아이 구조를 구분한다"],"NW_NUBI_TICKET")` `$ r13_v111_set("grand:fire",True)`
- `r13_v111_school_names7` if 「명부와 실제 침구를 확인한다」 `→ r13_v111_school_names_done7`
- 값
  - 회의 끝 `fire` → `"partial"` (`r13_v111_responsibility_wrong7`)
  - 명단 올림 보리 (까닭 `fire_partial`) (`r13_v111_responsibility_wrong7`)
  - 회의 끝 `fire` → `"win"` (`r13_v111_responsibility_answers7`)
  - `fire_neoul_promise_recorded` = `true` (`r13_v111_responsibility_answers7`)
  - `grand:fire` = `true` (`r13_v111_responsibility_answers7`)
  - `neoul_promise_proven` = `true` (`r13_v111_responsibility_answers7`)
  - `dodam_spoon7` = `true` (`r13_v111_dodam_spoon7`)

#### `MS14_D07_S03` 갈림 · 값 (room13_v111_days610.rpy:691)

- `r13_v111_room_visit7` if `r13_v111_value('stove13_7') in ('ration','empty')` `→ r13_v111_owl_well7`
- `r13_v111_handover7` if `r13_v111_value('doto_promise7')` `→ r13_v111_promise_night7`
- 값
  - `route7` = `"murder"` (`r13_v111_handover7`)
  - `choice:MS14_D07_S03` = `"C"` (`r13_v111_handover7`)
  - 생사 판정 `fate_owl` = `lost` (`r13_v111_handover7`)

#### `MS14_D07_S04` 갈림 · 값 (room13_v111_days610.rpy:737)

- `r13_v111_sleep7` if `r13_v111_value("DARAM_DETAINED")` `→ r13_v111_detained_sleep7`
- `r13_v111_free_sleep7_input` if 「잠자리를 정리한다」 `→ r13_v111_free_sleep7_done`
- `r13_v111_detained_bed7` if 「다음 날 면회를 준비한다」 `→ r13_v111_detained_morning8`
- `r13_v111_day8` if `r13_v111_value('route7')=='murder'` `→ r13_v111_custody8`
- 값
  - `day` = `8` (`r13_v111_free_sleep7_done`)
  - `day` = `8` (`r13_v111_detained_morning8`)

### 8일

| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |
|---|---|---|---|---|
| `MS14_D08_S01` | 8-1. 아침 / 보호실 — 듣기 싫은 말 · ['HOLDING_ROOM'] | 보호실 면회 자리(v111_custody) | 다람, 서리 검사원, 너울 | `r13_v111_custody8` |
| `MS14_D08_S02` | 8-2. 오전 / 13호 — 없어진 조각의 자리 · ['INN_CORRIDOR', 'ROOM13'] | 여관 2층 · 13호실(room13) | 도토, 부리 | `r13_v111_room_evidence8`, `r13_v111_room_check8`, `r13_v111_room_checked8` |
| `MS14_D08_S03` | 8-3. 오후 / 진료실 — 부러진 다음 · ['CLINIC'] | 임시 진료실(clinic) | 서리 검사원, 부리 | `r13_v111_wounds8`, `r13_v111_tool_faces8`, `r13_v111_tool_faces_seen8`, `r13_v111_wire_curve8`, `r13_v111_wire_curve_seen8` |
| `MS14_D08_P01` | 8-P. 생존 대체 / 다람과 함께 듣는 진료 · ['SCHOOL_ROOM', 'CLINIC', 'ROOM13'] | 여관 2층 · 13호실(room13) | 다람, 부엉이 할아버지, 도토, 서리 검사원, 너울, 할머니 | `r13_v111_prevent_clinic8`, `r13_v111_prevention_story8`, `r13_v111_care8`, `r13_v111_missing_pages8` |
| `MS14_D08_S04` | 8-4. 해 질 무렵 / 등 관리함 — 혼자 가지 않는 길 · ['LAMP_PATH'] | 돌이 있는 광장(square), 마을 학교(school) | 초롱, 도토, 바둑이 | `r13_v111_mother_letter8`, `r13_v111_letter_route8`, `r13_v111_letter_murder8`, `r13_v111_letter_prevent8`, `r13_v111_escort8`, `r13_v111_escort_done8` 외 4 |

#### `MS14_D08_S02` 갈림 · 값 (room13_v111_days610.rpy:860)

- `r13_v111_room_check8` if 「문틈과 발견 자리를 살핀다」 `→ r13_v111_room_checked8`
- 값
  - 자료 얻음 `NW_STONE` (`r13_v111_room_checked8`)

#### `MS14_D08_S03` 갈림 · 값 (room13_v111_days610.rpy:910)

- `r13_v111_tool_faces8` if 「손잡이·파단면·고리를 확인한다」 `→ r13_v111_tool_faces_seen8`
- `r13_v111_wire_curve8` if 「구리 조각과 핀 끝을 대조한다」 `→ r13_v111_wire_curve_seen8`

#### `MS14_D08_P01` 갈림 · 값 (room13_v111_days610.rpy:962)

- `r13_v111_prevention_story8` if `r13_v111_value('prevention')=='stone'` `→ r13_v111_owl_well8`
- 값
  - 자료 얻음 `NW_STONE` (`r13_v111_missing_pages8`)

#### `MS14_D08_S04` 갈림 · 값 (room13_v111_days610.rpy:1005)

- `r13_v111_letter_route8` if `r13_v111_value('route7')=='murder'` `→ r13_v111_letter_murder8`
- `r13_v111_escort8` if 「공개 길 동행을 부탁합니다.」 `→ r13_v111_escort_done8`
- `r13_v111_sleep8_input` if 「잠자리를 정리한다」 `→ r13_v111_sleep8_done`
- `r13_v111_day9` if `r13_v111_value('route7')=='murder'` `→ r13_v111_passage9`
- 값
  - `public_road_escort_completed` = `true` (`r13_v111_escort_done8`)
  - `day` = `9` (`r13_v111_sleep8_done`)

### 9일

| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |
|---|---|---|---|---|
| `MS14_D09_S01` | 9-1. 오전 / 주방과 책장 — 길 하나를 더 세다 · ['INN_KITCHEN', 'ROOM13', 'PASSAGE'] | 여관 1층 · 주방(kitchen) | 도토, 따닥, 할머니 | `r13_v111_passage9`, `r13_v111_safe_passage9`, `r13_v111_passage_safety_hint9`, `r13_v111_passage_walk9`, `r13_v111_passage_after9`, `r13_v111_passage_measured_hint9` |
| `MS14_D09_S02` | 9-2. 낮 / 공방 — 같은 핀이 아니다 · ['WORKSHOP', 'POST_OFFICE'] | 수리점(workshop) | 부리, 톡, 세련 | `r13_v111_workshop9`, `r13_v111_tok_route9`, `r13_v111_tok9`, `r13_v111_repair_copy9` |
| `MS14_D09_S03` | 9-3. 오후 / 식당 — 나비가 여민 것 · ['INN_DINING'] | 여관 식당(dining) | 나비, 할머니 | `r13_v111_scarf9`, `r13_v111_pin_question9`, `r13_v111_pin_time9`, `r13_v111_scarf_compare9`, `r13_v111_scarf_done9` |
| `MS14_D09_P01` | 9-P. 생존 대체 / 침입과 위조의 갈림길 · ['INN_KITCHEN', 'PASSAGE', 'ROOM13'] | 여관 1층 · 주방(kitchen), 여관 2층 · 13호실(room13) | 도토, 따닥, 할머니, 나비 | `r13_v111_prevent_passage9`, `r13_v111_safe_prevent9`, `r13_v111_prevent_walk9`, `r13_v111_papers_check9`, `r13_v111_papers_done9` |
| `MS14_D09_S04` | 9-4. 저녁 / 우체국 — 누가 부쳤는지, 누가 썼는지 · ['POST_OFFICE', 'HOLDING_ROOM', 'SCHOOL_ROOM'] | 우체국 입구(post), 보호실 면회 자리(v111_custody), 마을 학교(school) | 세련, 슬링 | `r13_v111_postal9`, `r13_v111_night_route9`, `r13_v111_custody_night9`, `r13_v111_school_night9`, `r13_v111_sleep9`, `r13_v111_sleep9_input` 외 2 |

#### `MS14_D09_S01` 갈림 · 값 (room13_v111_days610.rpy:1087)

- `r13_v111_passage9` if `not r13_v111_value('DARAM_DETAINED') and r13_v111_actor_ready('daram') and not r13_v111_value('daram_door_asked9')` `$ r13_v111_set('daram_door_asked9',True)`
- `r13_v111_safe_passage9` if 「쐐기·안전줄·문지기를 확인한다」 `→ r13_v111_passage_walk9`
- `r13_v111_safe_passage9` if 「들어가기 전에 확인할 것은요?」 `→ r13_v111_passage_safety_hint9`
- `r13_v111_passage_after9` if 「작업장으로 간다」 `→ r13_v111_workshop9`
- `r13_v111_passage_after9` if 「실측한 길을 다시 확인합니다.」 `→ r13_v111_passage_measured_hint9`
- 값
  - `daram_door_asked9` = `true` (`r13_v111_passage9`)

#### `MS14_D09_S02` 갈림 · 값 (room13_v111_days610.rpy:1141)

- `r13_v111_tok_route9` if `r13_v111_tok_attends("workshop")` `→ r13_v111_tok9`

#### `MS14_D09_S03` 갈림 · 값 (room13_v111_days610.rpy:1185)

- `r13_v111_pin_question9` if 「그날 밤 할머니 곁에서 본 것을 묻겠습니다.」 `→ r13_v111_pin_time9`
- `r13_v111_scarf_compare9` if 「목도리 끝과 핀을 대조한다」 `→ r13_v111_scarf_done9`

#### `MS14_D09_P01` 갈림 · 값 (room13_v111_days610.rpy:1257)

- `r13_v111_safe_prevent9` if 「쐐기·안전줄·문지기를 확인한다」 `→ r13_v111_prevent_walk9`
- `r13_v111_papers_check9` if 「반환 장수와 빈 자리를 확인한다」 `→ r13_v111_papers_done9`

#### `MS14_D09_S04` 갈림 · 값 (room13_v111_days610.rpy:1308)

- `r13_v111_night_route9` if `r13_v111_value('route7')=='murder'` `→ r13_v111_custody_night9`
- `r13_v111_sleep9_input` if 「잠자리를 정리한다」 `→ r13_v111_sleep9_done`
- `r13_v111_day10` if `r13_v111_value('route7')=='murder'` `→ r13_v111_waiting10`
- 값
  - `day` = `10` (`r13_v111_sleep9_done`)

### 10일

| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |
|---|---|---|---|---|
| `MS14_D10_S01` | 10-1. 아침 / 회관 대기실 — 아빠 말부터 고치기 · ['HALL_WAITING'] | 마을 학교(school) | 다람, 서리 검사원, 부리 | `r13_v111_waiting10` |
| `MS14_D10_S02` | 10-2. 오전 / 회관 — 문 하나의 증언 · ['HALL'] | 마을 학교(school) | 다람, 도토, 나비, 할머니, 너울, 뿔이 촌장, 서리 검사원 | `r13_v111_hearing10`, `r13_v111_wound_proof10`, `r13_v111_wound_answer10`, `r13_v111_passage_proof10`, `r13_v111_passage_answer10`, `r13_v111_hearing_wrong10` 외 2 |
| `MS14_D10_S03` | 10-3. 정오 / 회관 — 세 번의 변명 · ['HALL', 'HALL_WAITING'] | 마을 학교(school) | 다람, 할머니, 뿔이 촌장, 너울, 나비, 서리 검사원, 부리, 도토, 톡 | `r13_v111_owner10`, `r13_v111_owner_proof10`, `r13_v111_owner_answer10`, `r13_v111_owner_tok10`, `r13_v111_owner_copy10`, `r13_v111_time10` 외 7 |
| `MS14_D10_S04` | 10-4. 오후 / 우체국 옆 벤치 — 다음에 갈 곳 · ['POST_BENCH', 'SCHOOL_ROOM'] | 우체국 입구(post) | 다람, 세련, 부리, 나비 | `r13_v111_bench10` |
| `MS14_D10_P01` | 10-P. 예방 대체 / 그 종이를 넘기기 전에 · ['HALL', 'POST_BENCH'] | 마을 학교(school) | 다람, 부엉이 할아버지, 할머니, 뿔이 촌장, 너울, 슬링, 세련 | `r13_v111_prevent_hearing10`, `r13_v111_authority_proof10`, `r13_v111_authority_answer10`, `r13_v111_writing_proof10`, `r13_v111_writing_answer10`, `r13_v111_pocket10` 외 8 |
| `MS14_D10_S04P` | 반드시 실장할 짧은 대체 대사 · ['SCHOOL_ROOM'] | 마을 학교(school) | 다람, 꼬미 | `r13_v111_prevent_return10`, `r13_v111_sleep10`, `r13_v111_kkomi_acorn10`, `r13_v111_sleep10_input`, `r13_v111_sleep10_done` |

#### `MS14_D10_S02` 갈림 · 값 (room13_v111_days610.rpy:1403)

- `r13_v111_hearing_wrong10` if `r13_nw_retry("room13",['E08_CHILD_ACCOUNT', 'E08_TOOL'],'너울이 고개를 젓는다. 아이의 말과 촛대 조각을 함께 놓아야 한다.')` `→ r13_v111_wound_proof10`
- `r13_v111_passage_wrong10` if `r13_nw_retry("room13",['E09_PASSAGE', 'E08_ROOM'],'따닥이 고개를 젓는다. 직접 걸어 본 길과 현장 배치를 함께 놓아야 한다.')` `→ r13_v111_passage_proof10`
- `r13_v111_hearing_hint10` if `r13_v111_value("D10_S02_two_wounds_completed")` `→ r13_v111_passage_proof10`
- 값
  - 회의 끝 `room13` → `"lose"` (`r13_v111_hearing_wrong10`)
  - 명단 올림 다람 (까닭 `room13_lose`) (`r13_v111_hearing_wrong10`)
  - 회의 끝 `room13` → `"lose"` (`r13_v111_passage_wrong10`)
  - 명단 올림 다람 (까닭 `room13_lose`) (`r13_v111_passage_wrong10`)

#### `MS14_D10_S03` 갈림 · 값 (room13_v111_days610.rpy:1496)

- `r13_v111_owner_answer10` if `r13_v111_tok_attends("hearing")` `→ r13_v111_owner_tok10`
- `r13_v111_owner_wrong10` if `r13_nw_retry("room13",['E08_WOUND_WIRE', 'E09_PIN_OWNER'],'할머니가 웃는다. 구리선과 수선 기록을 함께 놓아야 한다.')` `→ r13_v111_owner_proof10`
- `r13_v111_time_wrong10` if `r13_nw_retry("room13",['E09_PIN_TIME', 'E09_PIN_HANDOVER_TIME'],'나비가 고개를 젓는다. 핀을 다시 채운 때와 계단참의 핀을 함께 놓아야 한다.')` `→ r13_v111_time_proof10`
- `r13_v111_contact_wrong10` if `r13_nw_retry("room13",['E08_CONTACT_ASSEMBLY', 'E08_WOUND_WIRE', 'E08_CHILD_POSITION', 'E08_ROOM_REACH', 'E09_SCARF'],'할머니가 목도리를 여민다. 천과 핀, 상처, 아이의 자리를 함께 놓아야 한다.')` `→ r13_v111_contact_proof10`
- 값
  - 회의 끝 `room13` → `"win"` (`r13_v111_contact_answer10`)
  - `grandmother_custody` = `"detained"` (`r13_v111_contact_answer10`)
  - `forgery_confirmed` = `true` (`r13_v111_contact_answer10`)
  - 회의 끝 `room13` → `"partial"` (`r13_v111_owner_wrong10`)
  - `room13_partial_kind` = `"unknown"` (`r13_v111_owner_wrong10`)
  - 회의 끝 `room13` → `"partial"` (`r13_v111_time_wrong10`)
  - `room13_partial_kind` = `"unknown"` (`r13_v111_time_wrong10`)
  - 회의 끝 `room13` → `"partial"` (`r13_v111_contact_wrong10`)
  - `room13_partial_kind` = `"accident"` (`r13_v111_contact_wrong10`)

#### `MS14_D10_P01` 갈림 · 값 (room13_v111_days610.rpy:1680)

- `r13_v111_pocket10` if 「어제는 전부라고 하셨습니다.」 `→ r13_v111_pocket_answer10`
- 메뉴 `r13_v111_pocket_answer10` (1759줄)
  - 「가족끼리 확인하고, 왜 숨겼는지 묻는다」 → `r13_v111_family_paper10`
  - 「공개된 수량만 대조하고 기록을 받는다」 → `r13_v111_public_paper10`
- `r13_v111_private_handoff10` if 「아내가 직접 편지를 건넸습니까?」 `→ r13_v111_owl_invitation10`
- `r13_v111_private_handoff10` if 「공개 수치만 대조하고 인계해 주십시오.」 `→ r13_v111_public_paper10`
- `r13_v111_authority_wrong10` if `r13_nw_retry("records",['E06_CONTACT', 'E09_MAIL'],'부엉이가 손을 거둔다. 할머니에게 맡겼다는 말이 어디에 적혀 있는지부터 봐야 한다. 물자를 건넨 공개 기록과 우체국 기록을 함께 놓자.')` `→ r13_v111_authority_proof10`
- `r13_v111_writing_wrong10` if `r13_nw_retry("records",['E01', 'E07', 'E09_MAIL'],'슬링이 고개를 젓는다. 편지와 봉투, 필사본을 함께 놓아야 한다.')` `→ r13_v111_writing_proof10`
- 값
  - 회의 끝 `records` → `"win"` (`r13_v111_writing_answer10`)
  - `owl_invitation_testimony` = `true` (`r13_v111_owl_invitation10`)
  - 회의 끝 `records` → `"lose"` (`r13_v111_authority_wrong10`)
  - 명단 올림 부엉이 할아버지 (까닭 `records_lose`) (`r13_v111_authority_wrong10`)
  - 회의 끝 `records` → `"partial"` (`r13_v111_writing_wrong10`)

#### `MS14_D10_S04P` 갈림 · 값 (room13_v111_days610.rpy:1834)

- `r13_v111_sleep10_input` if 「잠자리를 정리한다」 `→ r13_v111_sleep10_done`
- 값
  - `kkomi_acorn10` = `true` (`r13_v111_kkomi_acorn10`)
  - `day` = `11` (`r13_v111_sleep10_done`)

### 11일

| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |
|---|---|---|---|---|
| `MS14_D11_S00` | 장면 11-0. 셋째 말뚝 아래 · 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 | 마을 학교(school), 마을 서쪽 · 길 없는 숲(forest) | 다람, 까로 | `r13_v111_day11`, `r13_v111_pump_open11`, `r13_v111_pump_reply11` |
| `MS14_D11_S01` | 장면 11-1. 빈 뿌리 집 · 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 | 마을 서쪽 · 길 없는 숲(forest), 마을 학교(school) | 다람, 토실, 나비 | `r13_v111_root11`, `r13_v111_root_note11`, `r13_v111_root_read11`, `r13_v111_nabi_waiting11`, `r13_v111_nabi_wait11`, `r13_v111_nabi_arrival11` 외 2 |
| `MS14_D11_S02` | 장면 11-2. 폐온실의 낮은 문 · 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 | 폐온실의 지하 작업실(greenhouse) | 다람, 엄마 | `r13_v111_reunion11` |
| `MS14_D11_S02A` | 장면 11-2A. 마를 때까지 · 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 | 폐온실의 지하 작업실(greenhouse) | 다람, 엄마 | `r13_v111_dry11`, `r13_v111_blanket_use11`, `r13_v111_blanket_one11`, `r13_v111_blanket_keep11`, `r13_v111_coat_use11`, `r13_v111_dry_done11` |
| `MS14_D11_S02B` | 장면 11-2B. 단추 하나 · 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 | 폐온실의 지하 작업실(greenhouse) | 다람, 엄마 | `r13_v111_button11`, `r13_v111_mother_questions11`, `r13_v111_mother_life11`, `r13_v111_mother_invitation11`, `r13_v111_mother_return11`, `r13_v111_mother_ready11` 외 1 |
| `MS14_D11_S03` | 장면 11-3. 열이 있는 물건 · 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 | 북쪽 옛 시설(facility), 마을 학교(school), 돌이 있는 광장(square), 마을 서쪽 · 길 없는 숲(forest) | 다람, 엄마, 굴돌, 초롱, 나비, 사자 선생님, 까로, 네로, 토실, 돌목, 백 부인, 판돌, 부엉이 할아버지 | `r13_v111_facility11`, `r13_v111_guldol_heat11`, `r13_v111_heat_check11`, `r13_v111_heat_seen11`, `r13_v111_family_place11`, `r13_v111_family_place_check11` 외 58 |
| `MS14_D11_S04` | 장면 11-4. 문이 열려 있어야 하는 밤 · 학교/펌프집/뿌리 집/폐온실/옛 시설/아랫길: 각 행동에 따른 실제 이동 | 마을 학교(school), 마을 서쪽 · 길 없는 숲(forest) | 엄마, 다람, 사자 선생님, 까로, 네로, 나비 | `r13_v111_night11`, `r13_v111_night_rescue_route11`, `r13_v111_lower_safe11`, `r13_v111_request_rescue11`, `r13_v111_night_rescue_prepare11`, `r13_v111_night_rescue_choices11` 외 12 |

#### `MS14_D11_S00` 갈림 · 값 (room13_v111_days1114.rpy:25)

- `r13_v111_pump_open11` if 「셋째 말뚝 아래 통을 연다」 `→ r13_v111_pump_reply11`
- 값
  - `root_address_known` = `true` (`r13_v111_pump_reply11`)

#### `MS14_D11_S01` 갈림 · 값 (room13_v111_days1114.rpy:59)

- `r13_v111_root_note11` if 「눌러 둔 돌 아래 쪽지를 본다」 `→ r13_v111_root_read11`
- `r13_v111_root_read11` if `r13_v111_value("location:nabi") not in (None,"school")` `→ r13_v111_nabi_waiting11`
- `r13_v111_nabi_wait11` if 「나비가 올 때까지 토실과 기다린다」 `→ r13_v111_nabi_arrival11`
- `r13_v111_tosil_handoff11` if 「토실의 보호를 부탁합니다.」 `→ r13_v111_tosil_safe11`
- 값
  - `greenhouse_address_known` = `true` (`r13_v111_root_read11`)

#### `MS14_D11_S02` 갈림 · 값 (room13_v111_days1114.rpy:158)

- 값
  - `family_reunited` = `true` (`r13_v111_reunion11`)

#### `MS14_D11_S02A` 갈림 · 값 (room13_v111_days1114.rpy:183)

- `r13_v111_dry11` if `r13_v111_value('carried_dry_blankets')==0` `→ r13_v111_coat_use11`
- 메뉴 `r13_v111_dry11` (205줄)
  - 「두 장을 꺼내 덮는다」 — 조건 `r13_v111_value('carried_dry_blankets')==2` → `r13_v111_blanket_use11`
  - 「한 장을 함께 덮는다」 — 조건 `r13_v111_value('carried_dry_blankets')==1` → `r13_v111_blanket_one11`
  - 「짐 안에 둔다」 — 조건 `r13_v111_value('carried_dry_blankets')>0` → `r13_v111_blanket_keep11`
  - 「외투 안쪽을 함께 덮는다」 — 조건 `r13_v111_value('carried_dry_blankets')==0` → `r13_v111_coat_use11`

#### `MS14_D11_S02B` 갈림 · 값 (room13_v111_days1114.rpy:248)

- `r13_v111_mother_questions11` if 「어떻게 지냈어?」 `→ r13_v111_mother_life11`
- `r13_v111_mother_questions11` if 「왜 우리를 부르지 않았어?」 `→ r13_v111_mother_invitation11`
- `r13_v111_mother_questions11` if 「왜 돌아오지 못했어?」 `→ r13_v111_mother_return11`
- `r13_v111_mother_ready11` if `all(r13_v111_value(k) for k in ['mother_q_life', 'mother_q_invitation', 'mother_q_return'])` `→ r13_v111_mother_last11`
- 값
  - `mother_q_life` = `true` (`r13_v111_mother_life11`)
  - `mother_q_invitation` = `true` (`r13_v111_mother_invitation11`)
  - `mother_q_return` = `true` (`r13_v111_mother_return11`)

#### `MS14_D11_S03` 갈림 · 값 (room13_v111_days1114.rpy:347)

- `r13_v111_heat_check11` if 「종이와 벽의 자국을 맞춰 본다」 `→ r13_v111_heat_check11`
- `r13_v111_heat_check11` if 「벽 그림과 돌판을 확인한다」 `→ r13_v111_heat_seen11`
- 메뉴 `r13_v111_heat_seen11` (414줄)
  - 「가족 자리부터 본다」 → `r13_v111_family_place11`
  - 「아랫길 대피 준비를 확인한다」 → `r13_v111_rescue_prepare11`
  - 「준비된 물자를 학교로 옮긴다」 → `r13_v111_supply_school11`
- `r13_v111_family_place_check11` if 「가족 세 사람이 쓸 자리를 확인한다」 `→ r13_v111_family_place_done11`
- `r13_v111_rescue_cart11` if 「수레를 끌고 아랫길로 간다」 `→ r13_v111_rescue_ready11`
- `r13_v111_rescue_cart11` if 「수레 짐을 내려 자리를 비운다」 `$ r13_v111_set('rescue_cart_ready',True)`
- `r13_v111_rescue_cart11` elif 「덮개를 접어 빈 짐칸에 싣는다」 `$ r13_v111_set('rescue_cover_ready',True)`
- `r13_v111_rescue_cart11` elif `「까로에게 운반을 부탁한다」 and r13_v111_actor_ready('karo')` `$ r13_v111_set('rescue_driver_ready',True)`
- `r13_v111_rescue_cart11` elif 「아랫길을 비추는 등을 점검한다」 `$ r13_v111_set('rescue_lights_ready',True)`
- `r13_v111_rescue_cart11` elif `「아랫길 세 사람의 받을 자리를 비운다」 and r13_nero_receiver_ready11()` `$ r13_v111_set('rescue_school_ready11',True)`
- `r13_v111_rescue_cart11` elif 「먼저 학교 물자를 인계한다」 `→ r13_v111_supply_school11`
- `r13_v111_rescue_ready11` if `r13_nero_transport_ready11()` `→ r13_v111_day_rescue11`
- `r13_v111_day_rescue_door11` if 「아랫길 사람들의 문을 연다」 `→ r13_v111_day_rescue_school11`
- `r13_v111_school_visit11` if `not r13_v111_value("family_school_place")` `→ r13_v111_family_space_after_supply11`
- `r13_v111_family_space_after_supply11` if 「가족 세 사람의 실제 자리를 확인한다」 `→ r13_v111_family_space_checked11`
- `r13_v111_family_space_ready11` if `r13_v111_value('carried_dry_blankets')>0 and not r13_v111_value('tosil_blanket_given')` `→ r13_v111_blanket_choice11`
- 메뉴 `r13_v111_blanket_choice11` (556줄)
  - 「가족 짐에 보관한다」 → `r13_v111_blanket_store11`
  - 「토실에게 한 장을 건넨다」 → `r13_v111_tosil_blanket11`
- 메뉴 `r13_v111_hyp0_menu11` (596줄)
  - 「야생화는 옮는 병이다」 → `r13_v111_hyp0_sick11`
  - 「아르카가 사람을 부른다」 → `r13_v111_hyp0_call11`
  - 「꺼낸 아르카 곁에 오래 있던 사람부터 무너진다」 → `r13_v111_hyp0_won11`
  - 「늙으면 누구나 그렇게 된다」 → `r13_v111_hyp0_old11`
- `r13_v111_hyp0_sick11` if `r13_nw_retry("hypothesis")` `→ r13_v111_hyp0_menu11`
- `r13_v111_hyp0_call11` if `r13_nw_retry("hypothesis")` `→ r13_v111_hyp0_menu11`
- `r13_v111_hyp0_old11` if `r13_nw_retry("hypothesis")` `→ r13_v111_hyp0_menu11`
- 메뉴 `r13_v111_hyp1_q11` (632줄)
  - 「만지는 것보다 곁에서 오래 지내는 게 문제다」 → `r13_v111_hyp1_reason11`
  - 「초롱은 젊어서 버틴다」 → `r13_v111_hyp1_badreason11`
  - 「초롱은 장갑을 끼고 만진다」 → `r13_v111_hyp1_badreason11`
- `r13_v111_hyp1_badreason11` if `r13_nw_retry("hypothesis")` `→ r13_v111_hyp1_q11`
- `r13_v111_hyp1_wrong11` if `r13_nw_retry("hypothesis",['E11', 'E08', 'NW_PIKO_TREMOR'],'돌목이 팔짱을 낀다. 초롱의 하루와 피코의 밤을 함께 놓아야 한다.')` `→ r13_v111_hyp1_proof11`
- 메뉴 `r13_v111_hyp2_q11` (673줄)
  - 「켜지 않고 쌓아 둔 돌은 아무 해가 없다」 → `r13_v111_hyp2_badreason11`
  - 「백 부인은 그 돌 곁에서 잠을 자지 않는다」 → `r13_v111_hyp2_reason11`
  - 「백 부인은 돌을 팔기만 한다」 → `r13_v111_hyp2_badreason11`
- `r13_v111_hyp2_badreason11` if `r13_nw_retry("hypothesis")` `→ r13_v111_hyp2_q11`
- `r13_v111_hyp2_wrong11` if `r13_nw_retry("hypothesis",['NW_KEEPER_DATE'],'백 부인이 고개를 돌린다. 창고에서 자는 사람을 짚어야 한다.')` `→ r13_v111_hyp2_proof11`
- 메뉴 `r13_v111_hyp3_q11` (714줄)
  - 「요즘 사람들이 약해졌다」 → `r13_v111_hyp3_badreason11`
  - 「외지 사람이 병을 들여왔다」 → `r13_v111_hyp3_badreason11`
  - 「요즘 태우는 돌이 더 독하다」 → `r13_v111_hyp3_reason11`
- `r13_v111_hyp3_badreason11` if `r13_nw_retry("hypothesis")` `→ r13_v111_hyp3_q11`
- `r13_v111_hyp3_wrong11` if `r13_nw_retry("hypothesis",['NW_INNER_PRICE', 'NW_MUSOE_DEEP'],'판돌이 고개를 젓는다. “무쇠는 원래 고집이 셌소.” 돌값과 갱도 이야기를 함께 놓아야 한다.')` `→ r13_v111_hyp3_proof11`
- 메뉴 `r13_v111_hyp4_q11` (755줄)
  - 「아이 방에도 아르카등이 밤새 켜져 있었다」 → `r13_v111_hyp4_reason11`
  - 「아이들은 어른보다 약하다」 → `r13_v111_hyp4_badreason11`
  - 「아이들이 아르카를 만지고 논다」 → `r13_v111_hyp4_badreason11`
- `r13_v111_hyp4_badreason11` if `r13_nw_retry("hypothesis")` `→ r13_v111_hyp4_q11`
- `r13_v111_hyp4_wrong11` if `r13_nw_retry("hypothesis",['NW_KKOMI_NOSTONE', 'NW_SICK_BEDS'],'주민이 아이를 끌어안는다. 돌이 없는 아이들과 표시가 붙은 아이들을 함께 놓아야 한다.')` `→ r13_v111_hyp4_proof11`
- 메뉴 `r13_v111_hyp5_q11` (796줄)
  - 「한 방의 돌이 바뀌자 한 사람이 한 저녁 사이에 무너졌다」 — 조건 `r13_v111_value('OWL_ALIVE') is False` → `r13_v111_hyp5_reason11`
  - 「한 방의 돌을 치우자 무너지던 사람이 돌아왔다」 — 조건 `r13_v111_value('OWL_ALIVE') is not False and r13_v111_value('prevention')!='stone'` → `r13_v111_hyp5_reason11`
  - 「한 방의 돌을 꺼내자 그 앞에서 흐려지던 머리가 맑아졌다」 — 조건 `r13_v111_value('prevention')=='stone'` → `r13_v111_hyp5_reason11`
  - 「부엉이 어르신은 원래 아팠다」 → `r13_v111_hyp5_badreason11`
  - 「13호가 추워서 그렇다」 → `r13_v111_hyp5_badreason11`
- `r13_v111_hyp5_badreason11` if `r13_nw_retry("hypothesis")` `→ r13_v111_hyp5_q11`
- `r13_v111_hyp5_wrong11` if `r13_nw_retry("hypothesis")` `→ r13_v111_hyp5_proof11`
- `r13_v111_hyp_end11` if `r13_v111_value("guldol_facility_seen")` `$ r13_nw_list("resident_guldol","facility")`
- 값
  - `guldol_facility_seen` = `true` (`r13_v111_guldol_heat11`)
  - 자료 얻음 `NW_TABLET_A` (`r13_v111_heat_seen11`)
  - 자료 얻음 `NW_NAMES` (`r13_v111_heat_seen11`)
  - `heat_inventory_observed` = `true` (`r13_v111_heat_seen11`)
  - `family_school_place` = `true` (`r13_v111_family_place_done11`)
  - `rescue_preparation_schema11` = `true` (`r13_v111_rescue_prepare11`)
  - `rescue_cart_ready` = `true` (`r13_v111_rescue_cart11`)
  - `rescue_cover_ready` = `true` (`r13_v111_rescue_cart11`)
  - `rescue_driver_ready` = `true` (`r13_v111_rescue_cart11`)
  - `rescue_lights_ready` = `true` (`r13_v111_rescue_cart11`)
  - `rescue_school_ready11` = `true` (`r13_v111_rescue_cart11`)
  - `lower_road_arrived11` = `3` (`r13_v111_day_rescue_school11`)
  - `rescue_handoff_period11` = `"day"` (`r13_v111_day_rescue_school11`)
  - `school_supply_handed` = `true` (`r13_v111_supply_school11`)
  - `school_heat_connected` = `false` (`r13_v111_supply_school11`)
  - `family_school_place` = `true` (`r13_v111_family_space_checked11`)
  - 자료 얻음 `NW_SICK_BEDS` (`r13_v111_hypothesis11`)
  - `hyp_issue:1` = `"lost"` (`r13_v111_hyp1_lost11`)
  - `hyp_issue:1` = `"won"` (`r13_v111_hyp1_won11`)
  - `hyp_issue:2` = `"lost"` (`r13_v111_hyp2_lost11`)
  - `hyp_issue:2` = `"won"` (`r13_v111_hyp2_won11`)
  - `hyp_issue:3` = `"lost"` (`r13_v111_hyp3_lost11`)
  - `hyp_issue:3` = `"won"` (`r13_v111_hyp3_won11`)
  - `hyp_issue:4` = `"lost"` (`r13_v111_hyp4_lost11`)
  - `hyp_issue:4` = `"won"` (`r13_v111_hyp4_won11`)
  - 회의 끝 `hypothesis` → `"win" if all(r13_v111_value("hyp_issue:%d"%i)=="won" for i in (1,2,3,4)) else "partial"` (`r13_v111_hyp5_won11`)
  - 회의 끝 `hypothesis` → `"lose"` (`r13_v111_hyp_lost_gate11`)
  - 명단 올림 굴돌 (까닭 `facility`) (`r13_v111_hyp_end11`)

#### `MS14_D11_S04` 갈림 · 값 (room13_v111_days1114.rpy:850)

- `r13_v111_night_rescue_route11` if `r13_v111_value('lower_road_arrived11')==3 and r13_v111_value('lower_road_handover')!=3` `→ r13_v111_rescue_handoff11`
- `r13_v111_night_rescue_route11` if `r13_v111_value('lower_road_handover')==3` `→ r13_v111_lower_safe11`
- `r13_v111_night_rescue_prepare11` if 「오늘은 출발을 미룬다」 `→ r13_v111_late_supply11`
- `r13_v111_night_rescue_prepare11` if `not r13_v111_value('school_supply_handed')` `→ r13_v111_late_supply11`
- `r13_v111_night_rescue_prepare11` if 「낮에 챙긴 운반 준비를 확인한다」 `→ r13_v111_night_rescue_choices11`
- `r13_v111_night_rescue_choices11` if `r13_nero_transport_ready11() and r13_v111_value('school_supply_handed')` `→ r13_v111_night_rescue11`
- `r13_v111_night_rescue_choices11` if `not r13_v111_value('school_supply_handed')` `→ r13_v111_late_supply11`
- `r13_v111_snow_door11` if 「눈에 막힌 문을 연다」 `→ r13_v111_night_rescue_done11`
- `r13_v111_rescue_handoff11` if `「세 사람을 맞은 자리와 명단을 확인한다」 and r13_nero_receiver_ready11()` `→ r13_v111_school_visit11`
- `r13_v111_rescue_handoff11` if `r13_v111_value('rescue_handoff_period11')=='day'` `→ r13_v111_school_visit11`
- `r13_v111_rescue_handoff11` if 「학교 안에서 받을 사람을 기다린다」 `→ r13_v111_school_visit11`
- `r13_v111_rescue_handoff11` if `r13_v111_value('rescue_handoff_period11')=='day'` `→ r13_v111_school_visit11`
- `r13_v111_late_supply_handoff11` if 「온기 상자 인수를 확인한다」 `→ r13_v111_late_supply_done11`
- `r13_v111_sleep11_input` if 「판돌 씨 집에 들렀다 온다」 `→ r13_v111_sleep11_input`
- `r13_v111_sleep11_input` if 「남은 장작 몫을 확인한다」 `→ r13_v111_sleep11_input`
- `r13_v111_sleep11_input` if 「잠자리를 정리한다」 `→ r13_v111_sleep11_done`
- 값
  - `lower_lights_cut` = `true` (`r13_v111_night11`)
  - `rescue_handoff_period11` = `"night"` (`r13_v111_night_rescue_route11`)
  - 생사 판정 `fate_nero` = `handover` (`r13_v111_lower_safe11`)
  - `nero_alive` = `true` (`r13_v111_lower_safe11`)
  - `lower_road_arrived11` = `3` (`r13_v111_night_rescue_done11`)
  - `rescue_handoff_period11` = `"night"` (`r13_v111_night_rescue_done11`)
  - `lower_road_handover` = `3` (`r13_v111_rescue_handoff11`)
  - `nero_alive` = `true` (`r13_v111_rescue_handoff11`)
  - `alive:v111_lowerroad_elder` = `true` (`r13_v111_rescue_handoff11`)
  - 생사 판정 `fate_nero` = `handover` (`r13_v111_rescue_handoff11`)
  - 생사 판정 `fate_nero` = `rescue` (`r13_v111_rescue_handoff11`)
  - `school_supply_handed` = `true` (`r13_v111_late_supply_done11`)
  - `school_heat_connected` = `false` (`r13_v111_late_supply_done11`)
  - 생사 판정 `fate_nero` = `lost` (`r13_v111_late_road11`)
  - `lower_road_lost` = `true` (`r13_v111_late_road11`)
  - `location:resident_nero` = `"forest"` (`r13_v111_late_road11`)
  - `nero_alive` = `false` (`r13_v111_late_road11`)
  - `alive:v111_lowerroad_elder` = `false` (`r13_v111_late_road11`)
  - `day` = `12` (`r13_v111_sleep11_done`)

### 12일

| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |
|---|---|---|---|---|
| `MS14_D12_S01` | 장면 12-1. 불러야 할 이름 · 학교 배식실/진료 공간/시설 인수 지점 | 마을 학교(school), 마을 서쪽 · 길 없는 숲(forest), 돌이 있는 광장(square) | 엄마, 다람, 까로, 돌목, 사자 선생님, 네로, 백 부인, 서리 검사원 | `r13_v111_day12`, `r13_v111_loss_route12`, `r13_v111_loss_names12`, `r13_v111_living_names12`, `r13_v111_morning_notice12`, `r13_v111_morning_prep12_entry` 외 7 |
| `MS14_D12_S02` | 장면 12-2. 배식 전의 손 · 학교 배식실/진료 공간/시설 인수 지점 | 마을 학교(school), 북쪽 옛 시설(facility) | 다람, 나비, 사자 선생님, 보리, 도담, 새미, 엄마 | `r13_v111_meal12`, `r13_v111_meal_choice12`, `r13_v111_prevent_check12`, `r13_v111_medicine_missing12`, `r13_v111_seat_missing12`, `r13_v111_carrier_missing12` 외 8 |
| `MS14_D12_S03` | 장면 12-3. 돌아온 냄비 · 학교 배식실/진료 공간/시설 인수 지점 | 마을 학교(school) | 다람, 나비, 보리, 사자 선생님, 새미 | `r13_v111_late_meal12`, `r13_v111_soup_fragment12`, `r13_v111_fragment_seen12` |
| `MS14_D12_A` | 대체 장면 12-A. 배식 직전 발견 · 학교 배식실/진료 공간/시설 인수 지점 | 마을 학교(school) | 다람, 나비, 사자 선생님, 보리, 도담, 새미 | `r13_v111_premeal12` |
| `MS14_D12_S04` | 장면 12-4. 같은 것을 먹었다는 말 · 학교 배식실/진료 공간/시설 인수 지점 | 마을 학교(school) | 다람, 나비, 사자 선생님, 백 부인, 서리 검사원, 보리, 돌목, 너울, 엄마 | `r13_v111_soup_hearing12`, `r13_v111_meal_observations12`, `r13_v111_bottle_match12`, `r13_v111_bottle_matched12`, `r13_v111_seal_proof12`, `r13_v111_seal_answer12` 외 25 |
| `MS14_D12_S05` | 장면 12-5. 너무 밝은 창문 · 학교 배식실/진료 공간/시설 인수 지점 | 마을 학교(school) | 다람, 나비, 사자 선생님, 서리 검사원, 보리, 돌목, 너울, 엄마 | `r13_v111_aftermath_late12`, `r13_v111_teacher_guard_late12`, `r13_v111_teacher_neoul_late12`, `r13_v111_lights12`, `r13_v111_no_lights12` |
| `MS14_D12_B` | 대체 장면 12-B. 수프 사건이 일어나지 않은 저녁 · 학교 배식실/진료 공간/시설 인수 지점 | 마을 학교(school) | 다람, 엄마, 나비, 사자 선생님, 까로, 도담, 새미 | `r13_v111_early12`, `r13_v111_sleep12`, `r13_v111_sleep12_bed`, `r13_v111_sleep12_bed_input`, `r13_v111_sleep12_bed_done` |

#### `MS14_D12_S01` 갈림 · 값 (room13_v111_days1114.rpy:1023)

- `r13_v111_loss_route12` if `r13_v111_value('lower_road_lost')` `→ r13_v111_loss_names12`
- `r13_v111_morning_notice12` if `r13_v111_value('carried_dry_blankets')<2 and r13_v111_actor_ready('daram') and not r13_v111_value('daram_fever12')` `$ r13_v111_set('daram_fever12',True)`
- `r13_v111_morning_prep12` if 「약장 관리를 확인합니다.」 `→ r13_v111_medicine12`
- `r13_v111_morning_prep12` if 「불 땔 자리를 부탁드립니다.」 `→ r13_v111_warm_place12`
- `r13_v111_morning_prep12` if 「학교 운반을 부탁한다.」 `→ r13_v111_carrier12`
- `r13_v111_morning_prep12` if 「배식 준비를 살핀다」 `→ r13_v111_meal12`
- `r13_v111_morning_prep12` if 「학교 물자를 함께 확인하시겠습니까?」 `→ r13_v111_madam_invite12`
- `r13_v111_warm_place12` if `r13_v111_value('daram_fever12')` `→ r13_v111_morning_prep12_entry`
- `r13_v111_carrier_receipt12` if 「도착한 장작의 인수를 확인한다」 `→ r13_v111_carrier_received12`
- 값
  - `daram_fever12` = `true` (`r13_v111_morning_notice12`)
  - 자료 얻음 `NW_TRANSFER_LIST` (`r13_v111_morning_notice12`)
  - `madam_observer_consent` = `true` (`r13_v111_madam_invite12`)
  - `medicine_locked` = `true` (`r13_v111_medicine12`)
  - `warm_seat_taken12` = `true` (`r13_v111_warm_place12`)
  - `warm_seat_ready` = `true` (`r13_v111_warm_place12`)
  - `carrier_arrived` = `true` (`r13_v111_carrier12`)
  - `busy:karo` = `"school_transport"` (`r13_v111_carrier12`)
  - `warm_support_arrived` = `true` (`r13_v111_carrier_received12`)
  - `school_supply_handed` = `true` (`r13_v111_carrier_received12`)
  - `busy:karo` = `false` (`r13_v111_carrier_received12`)

#### `MS14_D12_S02` 갈림 · 값 (room13_v111_days1114.rpy:1152)

- `r13_v111_meal12` if `r13_v111_value('meal12_intro_seen')` `→ r13_v111_meal_choice12`
- 메뉴 `r13_v111_meal_choice12` (1199줄)
  - 「배식 전에 더 살핀다」 → `r13_v111_stay_meal12`
  - 「다람과 장작을 받으러 간다」 → `r13_v111_take_daram12`
  - 「다람은 나비 곁에 두고 다녀온다」 → `r13_v111_leave_daram12`
  - 「아침에 부탁한 일들을 확인한다」 → `r13_v111_prevent_check12`
- `r13_v111_prevent_check12` if `all(r13_v111_value(k) for k in ("medicine_locked","warm_seat_ready","carrier_arrived","warm_support_arrived"))` `→ r13_v111_prevent_ready12`
- `r13_v111_prevent_check12` if `not r13_v111_value("medicine_locked")` `→ r13_v111_medicine_missing12`
- `r13_v111_prevent_check12` if `not r13_v111_value("warm_seat_ready")` `→ r13_v111_seat_missing12`
- `r13_v111_meal_inspect12` if 「작은 냄비와 국자 자리를 살핀다」 `$ r13_v111_set('soup_smallpot_seen12',True)`
- `r13_v111_meal_inspect12` elif 「흰 그릇이 놓인 자리를 살핀다」 `$ r13_v111_set('soup_bowls_seen12',True)`
- `r13_v111_meal_inspect12` elif 「선반에 놓인 병의 봉인을 살핀다」 `$ r13_v111_set('soup_bottle_seen12',True)`
- `r13_v111_meal_inspect12` elif `「흰 그릇을 옆으로 옮기고 작은 냄비를 연다」 and r13_soup_inspect_ready12()` `→ r13_v111_premeal12`
- `r13_v111_meal_inspect12` elif 「장작을 받을 일을 다시 살핀다」 `→ r13_v111_meal_choice12`
- `r13_v111_pickup_box12` if 「준비된 장작 묶음을 인수한다」 `→ r13_v111_pickup_done12`
- 값
  - `location:mom` = `"facility"` (`r13_v111_meal12`)
  - `route12` = `"uncommitted"` (`r13_v111_meal12`)
  - `dodam_spoon12` = `bool(r13_v111_value('dodam_spoon7')) and r13_v111_actor_ready('daram')` (`r13_v111_meal12`)
  - `bowls_carried12` = `true` (`r13_v111_meal12`)
  - 자료 얻음 `NW_WHITE_BOWLS` (`r13_v111_meal12`)
  - `bottle_original_seal_seen` = `true` (`r13_v111_meal12`)
  - `meal12_intro_seen` = `true` (`r13_v111_meal12`)
  - `soup_smallpot_seen12` = `true` (`r13_v111_meal_inspect12`)
  - `soup_bowls_seen12` = `true` (`r13_v111_meal_inspect12`)
  - `soup_bottle_seen12` = `true` (`r13_v111_meal_inspect12`)
  - `soup_serving_separated12` = `true` (`r13_v111_meal_inspect12`)
  - `route12` = `"premeal_stopped"` (`r13_v111_meal_inspect12`)
  - 생사 판정 `fate_soup` = `lost` (`r13_v111_take_daram12`)
  - `route12` = `"late_exposure"` (`r13_v111_take_daram12`)
  - `DARAM_location` = `"with_father"` (`r13_v111_take_daram12`)
  - 생사 판정 `fate_soup` = `lost` (`r13_v111_leave_daram12`)
  - `route12` = `"late_exposure"` (`r13_v111_leave_daram12`)
  - `DARAM_location` = `"school"` (`r13_v111_leave_daram12`)
  - `busy:nabi` = `"daram_guard"` (`r13_v111_leave_daram12`)
  - `heat_box_received` = `true` (`r13_v111_pickup_done12`)

#### `MS14_D12_S03` 갈림 · 값 (room13_v111_days1114.rpy:1301)

- `r13_v111_late_meal12` if `r13_v111_value('KKOMI_ALIVE') is True` `$ r13_v111_set('KKOMI_ALIVE',False)`
- `r13_v111_soup_fragment12` if 「작은 냄비의 남은 수프를 보존한다」 `→ r13_v111_fragment_seen12`
- 값
  - `busy:nabi` = `false` (`r13_v111_late_meal12`)
  - `KKOMI_ALIVE` = `false` (`r13_v111_late_meal12`)
  - `kkomi_soup_dead` = `true` (`r13_v111_late_meal12`)
  - `medical_called` = `true` (`r13_v111_late_meal12`)
  - `busy:resident_bori` = `"medical_call"` (`r13_v111_late_meal12`)
  - `soup_fragment_observed` = `true` (`r13_v111_fragment_seen12`)

#### `MS14_D12_A` 갈림 · 값 (room13_v111_days1114.rpy:1345)

- 값
  - 생사 판정 `fate_soup` = `premeal` (`r13_v111_premeal12`)
  - `route12` = `"premeal_stopped"` (`r13_v111_premeal12`)
  - `medical_called` = `true` (`r13_v111_premeal12`)
  - `busy:resident_bori` = `"medical_call"` (`r13_v111_premeal12`)
  - `soup_fragment_observed` = `true` (`r13_v111_premeal12`)

#### `MS14_D12_S04` 갈림 · 값 (room13_v111_days1114.rpy:1366)

- `r13_v111_bottle_match12` if 「병과 파편의 경계를 대조한다」 `→ r13_v111_bottle_matched12`
- `r13_v111_seal_answer12` if `r13_v111_value('route12')=='late_exposure'` `→ r13_v111_seal_late12`
- `r13_v111_handling_route12` if `r13_v111_value('route12')=='late_exposure'` `→ r13_v111_handling_late12`
- 메뉴 `r13_v111_medical_arrival12` (1488줄)
  - 「약장 밖에 맡긴 약도 있는지 묻는다」
  - 「장부를 다시 보여 달라고 한다」
- `r13_v111_soup_conclusion_route12` if `r13_v111_value('route12')=='late_exposure'` `→ r13_v111_conclusion_late12`
- `r13_v111_list_wrong12` if `r13_nw_retry("soup",["NW_TRANSFER_LIST","NW_WHITE_BOWLS"],"선생님이 출석부를 끌어안는다. 명단의 칸과 흰 그릇을 함께 놓아야 한다.")` `→ r13_v111_list_proof12`
- `r13_v111_list_won12` if `r13_v111_value("meeting:soup")=="win" and r13_nw_grand(["명단과 흰 그릇을 대조한다"],"NW_RETURNED_BOWL")` `$ r13_v111_set("grand:soup",True)`
- `r13_v111_soup_after_route12` if `r13_v111_value('route12')=='late_exposure'` `→ r13_v111_aftermath_late12`
- `r13_v111_medicine_wrong12` if `r13_nw_retry("soup",['E12_FRAGMENT', 'E12_SEAL'],'선생님이 병을 감싼다. 파편과 봉인을 함께 놓아야 한다.')` `→ r13_v111_seal_proof12`
- `r13_v111_fragment_wrong12` if `r13_nw_retry("soup",['E12_FRAGMENT', 'E12_SEAL', 'E12_HANDLING'],'나비가 고개를 젓는다. 파편과 봉인, 냄비를 건넨 구간을 함께 놓아야 한다.')` `→ r13_v111_soup_final12`
- 메뉴 `r13_v111_aftermath_pre12` (1614줄)
  - 「돌목에게 감독을 맡긴다」 → `r13_v111_teacher_guard_pre12`
  - 「너울에게 신병을 넘긴다」 → `r13_v111_teacher_neoul_pre12`
- 값
  - `busy:resident_bori` = `false` (`r13_v111_medical_arrival12`)
  - `medical_arrived` = `true` (`r13_v111_medical_arrival12`)
  - `teacher_confessed` = `true` (`r13_v111_confessed12`)
  - 회의 끝 `soup` → `"partial"` (`r13_v111_list_wrong12`)
  - 회의 끝 `soup` → `"win"` (`r13_v111_list_won12`)
  - `transfer_list_secured` = `true` (`r13_v111_list_won12`)
  - `grand:soup` = `true` (`r13_v111_list_won12`)
  - `transfer_list_voided` = `true` (`r13_v111_list_won12`)
  - 회의 끝 `soup` → `"lose"` (`r13_v111_medicine_wrong12`)
  - `soup_lose_kind` = `"stolen"` (`r13_v111_medicine_wrong12`)
  - `seori_disciplined` = `true` (`r13_v111_medicine_wrong12`)
  - 회의 끝 `soup` → `"lose"` (`r13_v111_fragment_wrong12`)
  - `soup_lose_kind` = `"nabi"` (`r13_v111_fragment_wrong12`)
  - 명단 올림 나비 (까닭 `soup_lose`) (`r13_v111_fragment_wrong12`)
  - `book_promise12` = `true` (`r13_v111_aftermath_pre12`)

#### `MS14_D12_S05` 갈림 · 값 (room13_v111_days1114.rpy:1651)

- 메뉴 `r13_v111_aftermath_late12` (1682줄)
  - 「돌목에게 감독을 맡긴다」 → `r13_v111_teacher_guard_late12`
  - 「너울에게 신병을 넘긴다」 → `r13_v111_teacher_neoul_late12`

#### `MS14_D12_B` 갈림 · 값 (room13_v111_days1114.rpy:1730)

- `r13_v111_sleep12` if `r13_v111_value("piko_alive") is False` `$ r13_nw_acquire("NW_PIKO_PAINTING")`
- `r13_v111_sleep12_bed_input` if 「잠자리를 정리한다」 `→ r13_v111_sleep12_bed_done`
- 값
  - 생사 판정 `fate_soup` = `early` (`r13_v111_early12`)
  - `route12` = `"early_prevented"` (`r13_v111_early12`)
  - `school_heat_connected` = `true` (`r13_v111_early12`)
  - `busy:karo` = `false` (`r13_v111_early12`)
  - 자료 얻음 `NW_HALL_WINDOW` (`r13_v111_sleep12`)
  - 자료 얻음 `NW_PIKO_PAINTING` (`r13_v111_sleep12`)
  - `day` = `13` (`r13_v111_sleep12_bed_done`)

### 13일

| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |
|---|---|---|---|---|
| `MS14_D13_S01` | 장면 13-1. 판돌의 어깨 · 학교/입구 경비실/광장 수레 | 마을 학교(school) | 엄마, 다람, 판돌, 까로, 돌목, 사자 선생님, 순찰대원 | `r13_v111_day13`, `r13_v111_blanket_mend13`, `r13_v111_blanket_mended13`, `r13_v111_teacher_relief13`, `r13_v111_teacher_relief_check13`, `r13_v111_teacher_relief_done13` |
| `MS14_D13_S02` | 장면 13-2. 벤치 한 칸 · 학교/입구 경비실/광장 수레 | 눈에 막힌 입구(gate), 돌이 있는 광장(square) | 엄마, 다람, 돌목, 판돌, 뿔이 촌장, 너울, 까로 | `r13_v111_gate_bench13`, `r13_v111_offer13`, `r13_v111_offer_question13`, `r13_v111_offer_accept13`, `r13_v111_offer_refuse13` |
| `MS14_D13_S03` | 장면 13-3. 아내가 불렀다는 말 · 학교/입구 경비실/광장 수레 | 돌이 있는 광장(square), 마을 학교(school) | 엄마, 다람, 판돌, 뿔이 촌장, 돌목, 까로, 바둑이, 나비 | `r13_v111_blanket_lie13`, `r13_v111_mending_proof13`, `r13_v111_mending_answer13`, `r13_v111_badook_proof13`, `r13_v111_badook_wrong13`, `r13_v111_badook_won13` 외 9 |
| `MS14_D13_S04` | 장면 13-4. 바퀴가 멎어도 · 학교/입구 경비실/광장 수레 | 돌이 있는 광장(square), 마을 학교(school), 분리된 감독 자리(v111_supervised), v111_labor | 엄마, 다람, 까로, 돌목, 바둑이, 판돌, 모모, 굴돌, 뿔이 촌장, 너울, 실룩, 네로, 나비, 사자 선생님, 은호, 부리 | `r13_v111_stop_cart13`, `r13_v111_rein13`, `r13_v111_rein_ledger13p`, `r13_v111_rein_ledger13`, `r13_v111_rein_painting13p`, `r13_v111_rein_won13` 외 45 |
| `MS14_D13_A` | 대체 장면 13-A. 가족 셋의 하룻밤 · 학교/입구 경비실/광장 수레 | 돌이 있는 광장(square), 눈에 막힌 입구(gate) | 엄마, 다람, 돌목, 까로 | `r13_v111_family_exit13` |
| `MS14_D13_B` | 대체 장면 13-B. 멈췄지만 끝내지 못한 밤 · 학교/입구 경비실/광장 수레 | 돌이 있는 광장(square) | 까로, 돌목, 바둑이, 너울, (+식) | `r13_v111_partial13`, `r13_v111_crowd_prepare13`, `r13_v111_crowd_prepare_wait13` |
| `MS14_D13_C` | 대체 장면 13-C. 사람을 끌어내리는 손 · 학교/입구 경비실/광장 수레 | 돌이 있는 광장(square), 마을 학교(school), 눈에 막힌 입구(gate) | 까로, 바둑이, 너울, (+식), 누비, 엄마, 다람, 나비, 돌목 | `r13_v111_crowd13`, `r13_v111_crowd_legacy_menu13`, `r13_v111_daram_crowd13`, `r13_v111_crowd_block13`, `r13_v111_crowd_block_old13`, `r13_v111_crowd_guard13` 외 14 |

#### `MS14_D13_S01` 갈림 · 값 (room13_v111_days1114.rpy:1779)

- `r13_v111_day13` if `r13_v111_value("piko_alive") is not False` `$ r13_nw_list("resident_piko","street")`
- `r13_v111_blanket_mend13` if 「누나의 돌봄 인계를 확인한다」 `→ r13_v111_blanket_mend13`
- `r13_v111_blanket_mend13` if 「회색 담요를 실제로 수선한다」 `→ r13_v111_blanket_mended13`
- `r13_v111_blanket_mended13` if `r13_v111_value("teacher_custody")=="guard"` `→ r13_v111_teacher_relief13`
- `r13_v111_teacher_relief_check13` if 「초소로 가기 전 교사 감독 교대를 확인한다」 `→ r13_v111_teacher_relief_done13`
- 값
  - `busy:karo` = `false` (`r13_v111_day13`)
  - 명단 올림 피코 (까닭 `street`) (`r13_v111_day13`)
  - `pandol_blanket_mended` = `true` (`r13_v111_blanket_mended13`)
  - `busy:v111_patrol` = `"teacher_supervision"` (`r13_v111_teacher_relief_done13`)
  - `teacher_supervisor` = `"v111_patrol"` (`r13_v111_teacher_relief_done13`)
  - `busy:guard` = `false` (`r13_v111_teacher_relief_done13`)

#### `MS14_D13_S02` 갈림 · 값 (room13_v111_days1114.rpy:1854)

- 메뉴 `r13_v111_offer13` (1894줄)
  - 「조건을 더 묻는다」 → `r13_v111_offer_question13`
  - 「가족 셋이 수락하고 물러난다」 — 조건 `r13_v111_value('family_offer_terms_seen')` → `r13_v111_offer_accept13`
  - 「거절하고 현장에 남는다」 — 조건 `r13_v111_value('family_school_place')` → `r13_v111_offer_refuse13`
- `r13_v111_offer_accept13` if `r13_v111_value("listed:daram")` `$ r13_v111_set("listed:daram",False)`
- 값
  - `family_offer_terms_seen` = `true` (`r13_v111_offer_question13`)
  - `family_deal` = `true` (`r13_v111_offer_accept13`)
  - `listed:daram` = `false` (`r13_v111_offer_accept13`)
  - `daram_deal_freed` = `true` (`r13_v111_offer_accept13`)
  - `family_deal` = `false` (`r13_v111_offer_refuse13`)

#### `MS14_D13_S03` 갈림 · 값 (room13_v111_days1114.rpy:1928)

- `r13_v111_badook_wrong13` if `r13_nw_retry("blanket")` `→ r13_v111_badook_proof13`
- `r13_v111_mending_wrong13` if `r13_nw_retry("blanket")` `→ r13_v111_mending_proof13`
- `r13_v111_departed_bed13` if 「오늘 밤 자리를 확인한다」 `→ r13_v111_morning14`
- `r13_v111_cart_inspect13` if 「실제 탑승자와 하차 준비를 확인한다」 `→ r13_v111_cart_observed13`
- `r13_v111_cart_observed13` if `r13_v111_value("listed:resident_piko")` `$ r13_nw_acquire("NW_PIKO_PAINTING","told")`
- 값
  - 회의 끝 `blanket` → `"partial"` (`r13_v111_badook_wrong13`)
  - 회의 끝 `blanket` → `"win"` (`r13_v111_badook_won13`)
  - `false_message_admitted` = `true` (`r13_v111_mending_rest13`)
  - 회의 끝 `blanket` → `"lose"` (`r13_v111_mending_wrong13`)
  - `departed_names` = `_aboard` (`r13_v111_mending_wrong13`)
  - `"departed:"+_p` = `true` (`r13_v111_mending_wrong13`)
  - `location:daram` = `"cart"` (`r13_v111_mending_wrong13`)
  - `cart_departed` = `true` (`r13_v111_mending_wrong13`)
  - `outcome13` = `"partial_rescue"` (`r13_v111_mending_wrong13`)
  - `cart_roster` = `["npc_pandol", "resident_momo", "resident_guldol"]` (`r13_v111_cart_observed13`)
  - 자료 얻음 `NW_PIKO_PAINTING` (`r13_v111_cart_observed13`)
  - `location:resident_teacher` = `"square"` (`r13_v111_teacher_board_observation13`)
  - `teacher_transfer` = `"aboard"` (`r13_v111_teacher_board_observation13`)
  - `cart_roster` = `r13_v111_value("cart_roster")+["resident_teacher"]` (`r13_v111_teacher_board_observation13`)
  - `location:resident_siluk` = `"square"` (`r13_v111_silluk_board_observation13`)
  - `silluk_transfer` = `"aboard"` (`r13_v111_silluk_board_observation13`)
  - `cart_roster` = `r13_v111_value("cart_roster")+["resident_siluk"]` (`r13_v111_silluk_board_observation13`)

#### `MS14_D13_S04` 갈림 · 값 (room13_v111_days1114.rpy:2069)

- `r13_v111_stop_cart13` if `r13_v111_value("listed:daram") and not r13_v111_value("handed:daram")` `$ r13_v111_set("handed:daram",True)`
- `r13_v111_rein_ledger13p` if `not r13_v111_value("roster_shown13")` `$ r13_v111_set("roster_shown13",True)`
- `r13_v111_rein_wrong13a` if `r13_nw_retry("piko")` `→ r13_v111_rein_ledger13p`
- `r13_v111_rein_wrong13b` if `r13_nw_retry("piko")` `→ r13_v111_rein_painting13p`
- `r13_v111_after_rein13` if `r13_v111_value("meeting:blanket")=="partial"` `→ r13_v111_partial_listed13`
- `r13_v111_partial_listed13` if `r13_v111_value("listed:daram") and not r13_v111_value("handed:daram")` `$ r13_v111_set("handed:daram",True)`
- 메뉴 `r13_v111_family_position13` (2165줄)
  - 「엄마와 다람이 곁에 남게 한다」 → `r13_v111_family_stay13`
  - 「엄마와 다람을 까로와 학교로 보낸다」 — 조건 `not r13_v111_value('busy:karo')` → `r13_v111_family_karo13`
  - 「엄마와 다람을 네로와 학교로 보낸다」 — 조건 `r13_v111_value('nero_alive') and not r13_v111_value('busy:resident_nero') and r13_v111_actor_ready("resident_nero")` → `r13_v111_family_nero13`
- 메뉴 `r13_v111_handover_plan13` (2240줄)
  - 「학교 침상과 인수를 먼저 확인한다」 → `r13_v111_school_handover_prep13`
  - 「하차한 사람부터 부축한다」 — 조건 `r13_v111_value('handover_prepared13')` → `r13_v111_pandol_down13`
  - 「보온·감독 아래 인계를 기다린다」 → `r13_v111_partial13`
  - 「검증한 기록을 공개한다」 — 조건 `r13_v111_value('false_message_admitted') and not r13_v111_value('crowd_resolution_done')` → `r13_v111_crowd_prepare13`
- `r13_v111_school_handover_prep13` if `r13_v111_value('listed:nabi') is True and not r13_v111_value('handed:nabi')` `$ r13_v111_set('handed:nabi',True)`
- `r13_v111_nabi_beds13` if 「침상과 인수를 부탁합니다.」 `→ r13_v111_beds_ready13`
- `r13_v111_momo_down13` if 「모모를 부축해 학교로 모신다」 `→ r13_v111_momo_school13`
- `r13_v111_guldol_down13` if 「굴돌을 부축해 학교로 모신다」 `→ r13_v111_guldol_school13`
- `r13_v111_last_cart13` if `"resident_teacher" in r13_v111_value("cart_roster") and not r13_v111_value("handed:resident_teacher")` `→ r13_v111_teacher_transport13`
- `r13_v111_last_cart13` if `"resident_siluk" in r13_v111_value("cart_roster") and not r13_v111_value("handed:resident_siluk")` `→ r13_v111_silluk_transport13`
- `r13_v111_last_cart13` if `not all(r13_v111_value("handed:"+p) for p in r13_v111_value("cart_roster"))` `→ r13_v111_partial_listed13`
- `r13_v111_teacher_down13` if 「교사를 분리된 감독 자리로 옮긴다」 `→ r13_v111_teacher_supervised13`
- `r13_v111_teacher_receipt13` if 「분리된 감독 자리의 인수를 확인한다」 `→ r13_v111_teacher_received13`
- `r13_v111_silluk_supervision13` if 「하차 전 감독 교대를 확인합니다.」 `→ r13_v111_silluk_down13`
- `r13_v111_silluk_receipt13` if 「원래 감독 장소의 인수를 확인한다」 `→ r13_v111_silluk_received13`
- `r13_v111_transport_cleanup13` if 「앞으로의 호송을 확인한다」 `→ r13_v111_escort_refuse13`
- `r13_v111_transport_cleanup13` if 「명령 전체를 중지하고, 사본을 직접 전하겠습니다.」 `→ r13_v111_order_stop13`
- `r13_v111_transport_cleanup13` if 「강제 운반은 맡지 말고, 빈 수레를 돌려주자.」 `→ r13_v111_driver_refuse13`
- `r13_v111_transport_cleanup13` if 「빈 수레 반환을 요청한다.」 `→ r13_v111_cart_return13`
- `r13_v111_transport_cleanup13` if 「중지 명령 사본을 너울에게 다시 보인다.」 `→ r13_v111_relay_stop13`
- `r13_v111_transport_cleanup13` if 「학교로 돌아간다」 `→ r13_v111_night_finish13`
- `r13_v111_transport_cleanup13` if 「내일 쓸 공구를 부탁합니다.」 `→ r13_v111_buri_tools13`
- `r13_v111_relay_stop13` if `r13_v111_value("busy:neoul")=="teacher_supervision"` `→ r13_v111_relay_supervised13`
- `r13_v111_relay_present13` if `_return=="V111:E13_ORDER" and r13_v111_owned("E13_ORDER")` `→ r13_v111_relay_confirmed13`
- 값
  - `cart_stopped` = `true` (`r13_v111_stop_cart13`)
  - `stop_actor` = `"resident_badook"` (`r13_v111_stop_cart13`)
  - `handed:daram` = `true` (`r13_v111_stop_cart13`)
  - `busy:resident_badook` = `"stop_cart"` (`r13_v111_stop_cart13`)
  - `cart_roster` = `r13_v111_value("cart_roster") or ["npc_pandol","resident_momo","resident_guldol"]` (`r13_v111_stop_cart13`)
  - `roster_shown13` = `true` (`r13_v111_rein_ledger13p`)
  - 회의 끝 `piko` → `"win"` (`r13_v111_rein_won13`)
  - `neoul_held` = `true` (`r13_v111_rein_won13`)
  - 자료 얻음 `NW_NEOUL_LEDGER` (`r13_v111_rein_won13`)
  - 회의 끝 `piko` → `"lose"` (`r13_v111_rein_wrong13`)
  - `cart_roster` = `list(dict.fromkeys(list(r13_v111_value("cart_roster") or ["npc_pandol","resident_momo","resident_guldol"])+_left))` (`r13_v111_partial_listed13`)
  - `handed:daram` = `true` (`r13_v111_partial_listed13`)
  - `family_location` = `"square"` (`r13_v111_family_stay13`)
  - `location:daram` = `"square"` (`r13_v111_family_stay13`)
  - `busy:mom` = `"daram_guard"` (`r13_v111_family_stay13`)
  - `family_location` = `"moving_to_school"` (`r13_v111_family_karo13`)
  - `location:mom` = `"on_way_school"` (`r13_v111_family_karo13`)
  - `location:daram` = `"on_way_school"` (`r13_v111_family_karo13`)
  - `location:karo` = `"on_way_school"` (`r13_v111_family_karo13`)
  - `busy:karo` = `"family_walk"` (`r13_v111_family_karo13`)
  - `family_location` = `"school"` (`r13_v111_family_nero13`)
  - `location:mom` = `"school"` (`r13_v111_family_nero13`)
  - `location:daram` = `"school"` (`r13_v111_family_nero13`)
  - `location:resident_nero` = `"school"` (`r13_v111_family_nero13`)
  - `busy:mom` = `"daram_guard"` (`r13_v111_family_nero13`)
  - `busy:resident_nero` = `"daram_guard"` (`r13_v111_family_nero13`)
  - `location:mom` = `"school"` (`r13_v111_family_walk_karo13`)
  - `location:daram` = `"school"` (`r13_v111_family_walk_karo13`)
  - `busy:mom` = `"daram_guard"` (`r13_v111_family_walk_karo13`)
  - `family_location` = `"school"` (`r13_v111_family_walk_karo13`)
  - `busy:karo` = `false` (`r13_v111_family_walk_karo13`)
  - `handed:nabi` = `true` (`r13_v111_school_handover_prep13`)
  - `handover_prepared13` = `true` (`r13_v111_beds_ready13`)
  - `busy:karo` = `false` (`r13_v111_beds_ready13`)
  - `handed:npc_pandol` = `true` (`r13_v111_pandol_down13`)
  - `handed:resident_momo` = `true` (`r13_v111_momo_school13`)
  - `handed:resident_guldol` = `true` (`r13_v111_guldol_school13`)
  - `"handed:"+_p` = `true` (`r13_v111_last_cart13`)
  - `all_cart_handed` = `true` (`r13_v111_last_cart13`)
  - `busy:resident_badook` = `false` (`r13_v111_last_cart13`)
  - `outcome13` = `"all_rescued"` (`r13_v111_last_cart13`)
  - `handed:resident_teacher` = `true` (`r13_v111_teacher_received13`)
  - `teacher_transfer` = `"handed_over"` (`r13_v111_teacher_received13`)
  - `busy:neoul` = `"teacher_supervision"` (`r13_v111_teacher_received13`)
  - `handed:resident_siluk` = `true` (`r13_v111_silluk_received13`)
  - `silluk_transfer` = `"handed_over"` (`r13_v111_silluk_received13`)
  - `busy:guard` = `"silluk_supervision"` (`r13_v111_silluk_received13`)
  - `actual_stop_actor_refuses_transport` = `true` (`r13_v111_escort_refuse13`)
  - `current_order_execution_stopped` = `true` (`r13_v111_order_stop13`)
  - `Kkaro_forced_transport_refused` = `true` (`r13_v111_driver_refuse13`)
  - `cart_returned` = `true` (`r13_v111_cart_return13`)
  - `escort_gear_returned` = `true` (`r13_v111_cart_return13`)
  - `relay_stopped` = `true` (`r13_v111_relay_confirmed13`)
  - `buri_device_consent` = `true` (`r13_v111_buri_tools13`)
  - `current_transport_chain_stopped` = `all(r13_v111_value(k) for k in ["actual_stop_actor_refuses_transport","current_order_execution_stopped","Kkaro_forced_transport_refused","cart_returned","escort_gear_returned","relay_stopped"])` (`r13_v111_night_finish13`)

#### `MS14_D13_A` 갈림 · 값 (room13_v111_days1114.rpy:2556)

- 값
  - `family_benefits_received` = `true` (`r13_v111_family_exit13`)
  - `night14_lodging` = `"gate"` (`r13_v111_family_exit13`)
  - `outcome13` = `"family_priority"` (`r13_v111_family_exit13`)
  - `departed_unrescued` = `true` (`r13_v111_family_exit13`)

#### `MS14_D13_B` 갈림 · 값 (room13_v111_days1114.rpy:2585)

- `r13_v111_crowd_prepare_wait13` if 「기록 읽을 자리를 수레에서 떼어 놓는다」 `$ r13_v111_set('crowd_records_spaced13',True)`
- `r13_v111_crowd_prepare_wait13` elif 「수레 옆 짐을 옮겨 통로를 나눈다」 `$ r13_v111_set('crowd_cart_spaced13',True)`
- `r13_v111_crowd_prepare_wait13` elif `「돌목에게 기록 읽는 동안 너울을 맡아 달라고 한다」 and r13_crowd_guard_available13()` `$ r13_v111_set('busy:guard','crowd_supervision')`
- `r13_v111_crowd_prepare_wait13` elif 「검증한 기록을 소리 내어 읽는다」 `→ r13_v111_crowd13`
- `r13_v111_crowd_prepare_wait13` elif 「공개를 미루고 인계부터 확인한다」 `→ r13_v111_handover_plan13`
- 값
  - `outcome13` = `"partial_rescue"` (`r13_v111_partial13`)
  - `cart_stopped` = `true` (`r13_v111_partial13`)
  - `pending_handover_supervised` = `true` (`r13_v111_partial13`)
  - `crowd_preparation_schema13` = `true` (`r13_v111_crowd_prepare13`)
  - `crowd_records_spaced13` = `true` (`r13_v111_crowd_prepare_wait13`)
  - `crowd_cart_spaced13` = `true` (`r13_v111_crowd_prepare_wait13`)
  - `busy:guard` = `"crowd_supervision"` (`r13_v111_crowd_prepare_wait13`)
  - `location:guard` = `"square"` (`r13_v111_crowd_prepare_wait13`)
  - `crowd_supervisor_placed13` = `true` (`r13_v111_crowd_prepare_wait13`)

#### `MS14_D13_C` 갈림 · 값 (room13_v111_days1114.rpy:2633)

- `r13_v111_crowd13` if `r13_v111_value('neoul_promise_proven') and r13_v111_person_alive('resident_nubi') and r13_v111_person_alive('neoul')` `$ r13_v111_join(['resident_nubi'])`
- `r13_v111_crowd13` if `r13_v111_value('crowd_preparation_schema13')` `→ r13_v111_crowd_record13`
- `r13_v111_crowd13` if `r13_v111_value('neoul_promise_proven') and r13_v111_person_alive('resident_nubi') and r13_v111_person_alive('neoul')` `→ r13_v111_crowd_record13`
- `r13_v111_crowd13` if `r13_crowd_prepared13()` `→ r13_v111_crowd_guard13`
- 메뉴 `r13_v111_crowd_legacy_menu13` (2659줄)
  - 「7일 회의 기록을 함께 읽는다」 — 조건 `r13_v111_value('neoul_promise_proven') and r13_v111_person_alive('resident_nubi') and r13_v111_person_alive('neoul')` → `r13_v111_crowd_record13`
  - 「너울을 몸으로 감싼다」 → `r13_v111_crowd_block13`
  - 「돌목에게 너울을 맡긴다」 — 조건 `not r13_v111_value('busy:guard')` → `r13_v111_crowd_guard13`
  - 「주민들을 말리지 않는다」 → `r13_v111_crowd_watch13`
- `r13_v111_daram_crowd13` if `r13_v111_actor_ready('daram') and room13['location']=='square'` `$ r13_v111_set('crowd_witnessed',True)`
- `r13_v111_crowd_watch13` if `r13_v111_value('riot_momo13')` `$ r13_v111_set('alive:resident_momo',False)`
- `r13_v111_sleep13` if `r13_v111_value("outcome13")=="family_priority"` `→ r13_v111_sleep13_gate`
- `r13_v111_sleep13_gate_input` if 「가족 세 사람의 오늘 밤 자리를 확인한다」 `→ r13_v111_morning14`
- `r13_v111_sleep13_input` if 「오늘 밤 자리를 확인한다」 `→ r13_v111_morning14`
- `r13_v111_ending_dispatch14` if `r13_v111_value('ending14')=='left_name'` `→ r13_v111_left_name_ending14`
- `r13_v111_ending_dispatch14` if `r13_v111_value('ending14')=='frozen'` `→ r13_v111_frozen_ending14`
- `r13_v111_ending_dispatch14` if `r13_v111_value('ending14')=='family'` `→ r13_v111_family_ending14`
- `r13_v111_ending_dispatch14` if `r13_v111_value('ending14')=='partial'` `→ r13_v111_partial_ending14`
- `r13_v111_ending_dispatch14` if `r13_v111_value('ending14')=='violence'` `→ r13_v111_violence_ending14`
- 값
  - `crowd_witnessed` = `true` (`r13_v111_daram_crowd13`)
  - 생사 판정 `fate_crowd` = `block` (`r13_v111_crowd_block13`)
  - `crowd_blocked_by_dad` = `true` (`r13_v111_crowd_block13`)
  - `alive:neoul` = `false` (`r13_v111_crowd_block13`)
  - `crowd_resolution_done` = `true` (`r13_v111_crowd_block13`)
  - `crowd_injury` = `true` (`r13_v111_crowd_block13`)
  - `crowd_intervention` = `"failed"` (`r13_v111_crowd_block13`)
  - `outcome13` = `"crowd_violence"` (`r13_v111_crowd_block13`)
  - `crowd_resolution_done` = `true` (`r13_v111_crowd_block_old13`)
  - `crowd_injury` = `false` (`r13_v111_crowd_block_old13`)
  - `crowd_intervention` = `"success"` (`r13_v111_crowd_block_old13`)
  - `outcome13` = `"all_rescued"` (`r13_v111_crowd_block_old13`)
  - 생사 판정 `fate_crowd` = `supervisor` (`r13_v111_crowd_guard13`)
  - `crowd_resolution_done` = `true` (`r13_v111_crowd_guard13`)
  - `crowd_injury` = `false` (`r13_v111_crowd_guard13`)
  - `outcome13` = `"all_rescued"` (`r13_v111_crowd_guard13`)
  - 생사 판정 `fate_crowd` = `riot` (`r13_v111_crowd_watch13`)
  - `riot_momo13` = `r13_v111_value('handed:resident_momo') is not True and r13_v111_person_alive('resident_momo')` (`r13_v111_crowd_watch13`)
  - `alive:neoul` = `false` (`r13_v111_crowd_watch13`)
  - `alive:resident_momo` = `false` (`r13_v111_crowd_watch13`)
  - `crowd_resolution_done` = `true` (`r13_v111_crowd_watch13`)
  - `crowd_injury` = `true` (`r13_v111_crowd_watch13`)
  - `crowd_intervention` = `"none"` (`r13_v111_crowd_watch13`)
  - `outcome13` = `"crowd_violence"` (`r13_v111_crowd_watch13`)
  - `crowd_resolution_done` = `true` (`r13_v111_crowd_failed13`)
  - `crowd_injury` = `true` (`r13_v111_crowd_failed13`)
  - `crowd_intervention` = `"failed"` (`r13_v111_crowd_failed13`)
  - `outcome13` = `"crowd_violence"` (`r13_v111_crowd_failed13`)
  - `family_location` = `"school"` (`r13_v111_sleep13`)
  - `location:daram` = `"school"` (`r13_v111_sleep13`)
  - `busy:mom` = `false` (`r13_v111_sleep13`)
  - `day` = `14` (`r13_v111_morning14`)
  - `ending14` = `r13_nw_ending14()` (`r13_v111_ending_dispatch14`)
  - `story14_completed` = `true` (`r13_v111_story_end14`)

### 14일

| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |
|---|---|---|---|---|
| `MS14_D14_S01` | 장면 14-1. 아침에도 살아 있는 사람 · 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 | 마을 학교(school) | 엄마, 다람, 판돌, 나비, 토실, 백 부인 | `r13_v111_morning_safe14`, `r13_v111_old_rations14`, `r13_v111_altar_guide14`, `r13_v111_altar_ready14` |
| `MS14_D14_S02` | 장면 14-2. 아무도 묶여 있지 않은 제단 · 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 | 북쪽 산길 · 숲속 제단(altar), 눈에 막힌 입구(gate), v111_labor, 마을 학교(school) | 엄마, 다람, 바둑이, 까로, 뿔이 촌장, 부리, 돌목, 실룩, (+식), 나비 | `r13_v111_altar14`, `r13_v111_mayor_interview14`, `r13_v111_altar1_q14`, `r13_v111_altar1_proof14`, `r13_v111_altar1_wrong14`, `r13_v111_altar1_won14` 외 34 |
| `MS14_D14_S03` | 장면 14-3. 보미라는 이름 · 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 | 눈에 막힌 입구(gate) | 엄마, 다람, 할머니, 돌목, 토실, 부엉이 할아버지 | `r13_v111_granny_interview14`, `r13_v111_tosil_listen14`, `r13_v111_tosil_inside14`, `r13_v111_tosil_outside14` |
| `MS14_D14_S04` | 장면 14-4. 이름판 아래의 그릇 · 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 | 돌이 있는 광장(square), 마을 학교(school) | 엄마, 다람, 토실, 판돌, 나비, 돌목, 초롱, 부엉이 할아버지 | `r13_v111_name_board14`, `r13_v111_tosil_name14`, `r13_v111_tosil_no_name14`, `r13_v111_pandol_news14`, `r13_v111_supply_inventory14`, `r13_v111_supply_inventory_done14` 외 4 |
| `MS14_D14_END_FAMILY` | 가족 철수 결말 — 열지 않은 문 · 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 | 눈에 막힌 입구(gate) | 엄마, 다람, 돌목 | `r13_v111_family_ending14` |
| `MS14_D14_END_PARTIAL` | 부분 구조 결말 — 남은 인계표 · 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 | 돌이 있는 광장(square), 마을 학교(school) | 까로, 돌목, 바둑이, 다람, 엄마, 나비, (+식) | `r13_v111_partial_ending14`, `r13_v111_partial_departed14`, `r13_v111_partial_handoff14`, `r13_v111_partial_work14`, `r13_v111_partial_patient14`, `r13_v111_partial_receipt14` 외 2 |
| `MS14_D14_END_VIOLENCE` | 군중 폭력 결말 — 한 명의 자리가 더 필요하다 · 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 | 임시 진료실(clinic), 눈에 막힌 입구(gate), 마을 학교(school) | 엄마, 다람, 돌목, 서리 검사원 | `r13_v111_violence_ending14`, `r13_v111_family_lodging14`, `r13_v111_cookie14`, `r13_v111_cookie_gate14` |
| `MS14_D14_S05` | 장면 14-5. 엄마 몫 과자 · 학교/안전 확인된 제단/감독 면회 자리/광장/확보 숙소 | — | 엄마, 다람, 나비, 도토, 바둑이, 돌목 | `r13_v111_cookie_scene14`, `r13_v111_true_epilogue14`, `r13_v111_wild_family_wait14`, `r13_v111_wild_night14`, `r13_v111_wild_room14`, `r13_v111_wild_hall14` 외 4 |

#### `MS14_D14_S01` 갈림 · 값 (room13_v111_days1114.rpy:2832)

- `r13_v111_morning_safe14` if `r13_v111_value("OWL_ALIVE") is False` `$ r13_nw_acquire("NW_BURNT_PAGE")`
- `r13_v111_altar_guide14` if 「제단 접근로를 확인해 주십시오.」 `→ r13_v111_altar_ready14`
- 값
  - 자료 얻음 `NW_BURNT_PAGE` (`r13_v111_morning_safe14`)
  - 자료 얻음 `NW_MADAM_DAY7` (`r13_v111_morning_safe14`)
  - 자료 얻음 `NW_OLD_RATIONS` (`r13_v111_old_rations14`)
  - `altar_guide_confirmed` = `true` (`r13_v111_altar_ready14`)
  - `busy:resident_badook` = `false` (`r13_v111_altar_ready14`)

#### `MS14_D14_S02` 갈림 · 값 (room13_v111_days1114.rpy:2879)

- `r13_v111_altar1_wrong14` if `not v111_altar_half and r13_nw_retry("altar")` `→ r13_v111_altar1_proof14`
- `r13_v111_altar1_wrong14` if `v111_altar_half` `→ r13_v111_altar2_q14`
- `r13_v111_altar2_proof14` if `not all(r13_v111_owned(k) for k in ['NW_TABLET_A', 'NW_TABLET_B'])` `→ r13_v111_altar3_q14`
- `r13_v111_altar2_wrong14` if `r13_nw_retry("altar",['NW_TABLET_A', 'NW_TABLET_B'],'촌장이 고개를 젓는다. 돌판의 앞 반쪽과 밑돌의 글자를 함께 놓아야 한다.')` `→ r13_v111_altar2_proof14`
- `r13_v111_altar3_proof14` if `not all(r13_v111_owned(k) for k in ['NW_IRON_MARK'])` `→ r13_v111_altar4_q14`
- `r13_v111_altar3_wrong14` if `r13_nw_retry("altar",['NW_IRON_MARK'],None)` `→ r13_v111_altar3_proof14`
- `r13_v111_altar4_proof14` if `not (r13_v111_owned("NW_NAMES") and (r13_v111_owned("NW_NEOUL_LEDGER") or r13_v111_owned("NW_OLD_RATIONS")))` `→ r13_v111_altar_close14`
- `r13_v111_altar4_wrong14` if `r13_nw_retry("altar",['NW_NAMES', 'NW_NEOUL_LEDGER'],'촌장의 손이 떨린다. 벽의 이름과 그해 집별 배급 기록을 함께 놓아야 한다.')` `→ r13_v111_altar4_proof14`
- `r13_v111_device14` if `r13_v111_value("buri_device_consent") and not r13_v111_value("mayor_site_decided") ` `→ r13_v111_mayor_site_request14`
- `r13_v111_mayor_site_request14` if 「감독 아래 현장 확인에 동행해 주십시오.」 `→ r13_v111_mayor_site_yes14`
- `r13_v111_mayor_site_request14` if 「이 자리에서만 확인하겠습니다.」 `→ r13_v111_mayor_site_no14`
- `r13_v111_device_record14` if `_return=="V111:E13_HANDOVER" and r13_v111_owned("E13_HANDOVER")` `→ r13_v111_device_rescue14`
- `r13_v111_device_record14` if `_return=="V111:E14_SUPPLY" and r13_v111_owned("E14_SUPPLY") and r13_v111_value("school_heat_connected")` `→ r13_v111_device_supply14`
- `r13_v111_device_pause14` if 「장치를 살피며 기록을 다시 확인한다」 `→ r13_v111_device_record14`
- `r13_v111_device_worker14` if `r13_v111_value("buri_device_present")` `→ r13_v111_buri_record_answer14`
- `r13_v111_device_detach14` if 「기록한 고정부를 안전하게 분리한다」 `→ r13_v111_device_detached14`
- `r13_v111_device_detached14` if `r13_v111_value("busy:guard")=="silluk_supervision"` `→ r13_v111_guard_relief14`
- `r13_v111_guard_relief_check14` if 「학교 인수 동안의 감독 교대를 확인합니다.」 `→ r13_v111_guard_relieved14`
- `r13_v111_device_lock14` if 「부품·기록판·열쇠 인수를 확인한다」 `→ r13_v111_device_locked14`
- 값
  - 자료 얻음 `NW_TABLET_B` (`r13_v111_altar14`)
  - 자료 얻음 `NW_IRON_MARK` (`r13_v111_altar14`)
  - `altar_heat_structure_observed` = `true` (`r13_v111_altar14`)
  - `mayor_false_invitation_admitted` = `true` (`r13_v111_mayor_interview14`)
  - `altar_half1` = `true` (`r13_v111_altar1_wrong14`)
  - `altar_issue:1` = `"half"` (`r13_v111_altar1_wrong14`)
  - `altar_issue:1` = `"won"` (`r13_v111_altar1_won14`)
  - `altar_issue:2` = `"lost"` (`r13_v111_altar2_proof14`)
  - `altar_issue:2` = `"lost"` (`r13_v111_altar2_wrong14`)
  - `altar_issue:2` = `"won"` (`r13_v111_altar2_won14`)
  - `altar_issue:3` = `"lost"` (`r13_v111_altar3_proof14`)
  - `altar_issue:3` = `"lost"` (`r13_v111_altar3_wrong14`)
  - `altar_issue:3` = `"won"` (`r13_v111_altar3_won14`)
  - `altar_issue:4` = `"lost"` (`r13_v111_altar4_proof14`)
  - `altar_issue:4` = `"lost"` (`r13_v111_altar4_wrong14`)
  - `altar_issue:4` = `"won"` (`r13_v111_altar4_won14`)
  - `dallae_first_victim_known` = `true` (`r13_v111_altar4_won14`)
  - 회의 끝 `altar` → `"win" if all(r13_v111_value("altar_issue:%d"%i)=="won" for i in (1,2,3,4)) else "partial"` (`r13_v111_altar_close14`)
  - 회의 끝 `altar` → `"lose"` (`r13_v111_altar_lost14`)
  - `mayor_site_decided` = `true` (`r13_v111_mayor_site_yes14`)
  - `mayor_site_joined` = `true` (`r13_v111_mayor_site_yes14`)
  - `mayor_site_decided` = `true` (`r13_v111_mayor_site_no14`)
  - `mayor_site_joined` = `false` (`r13_v111_mayor_site_no14`)
  - `buri_device_present` = `true` (`r13_v111_buri_work_start14`)
  - `device_record_kind` = `"rescue"` (`r13_v111_device_rescue14`)
  - `device_record_shown` = `true` (`r13_v111_device_rescue14`)
  - `device_record_kind` = `"supply"` (`r13_v111_device_supply14`)
  - `device_record_shown` = `true` (`r13_v111_device_supply14`)
  - `busy:karo` = `"device_support"` (`r13_v111_device_worker14`)
  - `device_support_ready` = `true` (`r13_v111_device_worker14`)
  - `busy:karo` = `false` (`r13_v111_device_order14`)
  - `command_confrontation_done` = `true` (`r13_v111_device_order14`)
  - `busy:karo` = `"device_support"` (`r13_v111_device_order14`)
  - `device_detached` = `true` (`r13_v111_device_detached14`)
  - `busy:karo` = `false` (`r13_v111_device_detached14`)
  - `busy:buri` = `false` (`r13_v111_device_detached14`)
  - `guard_relief_person` = `"neoul" if r13_v111_value("busy:v111_patrol")=="teacher_supervision" else "v111_patrol"` (`r13_v111_guard_relief14`)
  - `"busy:"+r13_v111_value("guard_relief_person")` = `"silluk_supervision"` (`r13_v111_guard_relieved14`)
  - `busy:guard` = `false` (`r13_v111_guard_relieved14`)
  - `device_joint_control` = `true` (`r13_v111_device_locked14`)
  - `command_confrontation_done` = `true` (`r13_v111_buri_record_answer14`)
  - `busy:buri` = `"device_work"` (`r13_v111_buri_record_answer14`)
  - `device_support_ready` = `true` (`r13_v111_buri_record_answer14`)

#### `MS14_D14_S03` 갈림 · 값 (room13_v111_days1114.rpy:3261)

- 메뉴 `r13_v111_tosil_listen14` (3279줄)
  - 「안에서 직접 듣는다」 → `r13_v111_tosil_inside14`
  - 「보호자와 밖에서 기다린다」 → `r13_v111_tosil_outside14`
- 값
  - `tosil_listen` = `"inside"` (`r13_v111_tosil_inside14`)
  - `bomi_death_confirmed` = `true` (`r13_v111_tosil_inside14`)
  - `adult_interview_done` = `true` (`r13_v111_tosil_inside14`)
  - `tosil_listen` = `"outside"` (`r13_v111_tosil_outside14`)
  - `location:resident_tosil` = `"outside_guard"` (`r13_v111_tosil_outside14`)
  - `bomi_death_confirmed` = `true` (`r13_v111_tosil_outside14`)
  - `adult_interview_done` = `true` (`r13_v111_tosil_outside14`)

#### `MS14_D14_S04` 갈림 · 값 (room13_v111_days1114.rpy:3335)

- 메뉴 `r13_v111_name_board14` (3343줄)
  - 「토실이 이름을 쓰겠다면 기다린다」 → `r13_v111_tosil_name14`
  - 「지금 쓰지 않아도 된다고 말한다」 → `r13_v111_tosil_no_name14`
- `r13_v111_supply_inventory14` if 「실물·사용처·남은 양을 함께 확인한다」 `→ r13_v111_supply_inventory_done14`
- 값
  - `school_inventory_checked` = `true` (`r13_v111_supply_inventory_done14`)
  - `school_supply_handed` = `true` (`r13_v111_supply_inventory_done14`)
  - `school_heat_connected` = `true` (`r13_v111_supply_inventory_done14`)
  - `current_sacrifice_operation_closed` = `bool(r13_v111_value("current_transport_chain_stopped") and r13_v111_value("device_joint_control"))` (`r13_v111_supply_inventory_done14`)
  - `lamp_manager` = `"resident_lamplighter"` (`r13_v111_chorong_lamps14`)
  - `lamp_manager` = `"mom"` (`r13_v111_mother_lamps14`)

#### `MS14_D14_END_PARTIAL` 갈림 · 값 (room13_v111_days1114.rpy:3458)

- `r13_v111_partial_ending14` if `r13_v111_value("cart_departed")` `→ r13_v111_partial_departed14`
- `r13_v111_partial_handoff14` if 「남은 인계에 직접 참여한다」 `→ r13_v111_partial_work14`
- `r13_v111_partial_receipt14` if 「새로 난 침상의 인수를 확인한다」 `→ r13_v111_partial_received14`
- `r13_v111_partial_received14` if `v111_pending_patient` `$ r13_v111_set("handed:"+v111_pending_patient,True)`
- `r13_v111_partial_received14` if `v111_pending_rest` `→ r13_v111_partial_wait14`
- 값
  - `"handed:"+v111_pending_patient` = `true` (`r13_v111_partial_received14`)
  - `pending_handover_completed` = `true` (`r13_v111_partial_received14`)
  - `pending_handover_completed` = `false` (`r13_v111_partial_wait14`)
  - `pending_handover_supervised` = `true` (`r13_v111_partial_wait14`)

#### `MS14_D14_END_VIOLENCE` 갈림 · 값 (room13_v111_days1114.rpy:3527)

- 값
  - `night14_lodging` = `"school"` (`r13_v111_cookie14`)
  - `night14_lodging` = `"gate"` (`r13_v111_cookie_gate14`)

#### `MS14_D14_S05` 갈림 · 값 (room13_v111_days1114.rpy:3591)

- `r13_v111_cookie_scene14` if `r13_v111_value('ending14')=='morning' and r13_v111_value('meeting:hypothesis')=='lose' and r13_v111_value('meeting:altar')=='lose'` `→ r13_v111_wild_night14`
- `r13_v111_wild_hall14` if 「도토의 손에서 바구니를 떼어 낸다」 `$ r13_v111_set('wild_late',(r13_v111_value('wild_late') or 0)+1)`
- `r13_v111_wild_square14` if 「바둑이와 잠긴 문을 연다」 `$ r13_v111_set('wild_late',(r13_v111_value('wild_late') or 0)+1)`
- `r13_v111_wild_road14` if 「돌목을 초소에서 끌어낸다」 `$ r13_v111_set('wild_late',(r13_v111_value('wild_late') or 0)+1)`
- 값
  - `story14_completed` = `true` (`r13_v111_cookie_scene14`)
  - `ending14` = `"true"` (`r13_v111_true_epilogue14`)
  - `ending14` = `"wild_night"` (`r13_v111_wild_night14`)
  - `wild_night14` = `true` (`r13_v111_wild_night14`)
  - `wild_late` = `0` (`r13_v111_wild_night14`)
  - `wild_late` = `(r13_v111_value('wild_late') or 0)+1` (`r13_v111_wild_hall14`)
  - `wild_late` = `(r13_v111_value('wild_late') or 0)+1` (`r13_v111_wild_square14`)
  - `wild_late` = `(r13_v111_value('wild_late') or 0)+1` (`r13_v111_wild_road14`)
  - `wild_family` = `r13_nw_wild_family()` (`r13_v111_wild_climb14`)

### 날짜 없음

| 장면 | 제목 · 원본 장소 | 이동(travel) | 인물 | 라벨 |
|---|---|---|---|---|
| `(장면 전) room13_v111_days123.rpy` | — | — | — | `r13_v111_start` |
| `(장면 전) room13_v111_days45.rpy` | — | — | — | `r13_v111_day4` |
| `(장면 전) room13_v111_owl_prevent.rpy` | — | 임시 진료실(clinic), 여관 2층 · 13호실(room13) | 나비, 사자 선생님, 다람, 까로, 서리 검사원, 도토, 부엉이 할아버지 | `r13_v111_snack_plate5`, `r13_v111_free_day7`, `r13_v111_free_day7_wait`, `r13_v111_free_day7_pick`, `r13_v111_free_evening7`, `r13_v111_owl_well7` 외 3 |
| `(장면 전) room13_hidden_pandol.rpy` | — | 판돌 집(hidden_pandol) | 판돌, 다람, 나비, 사자 선생님, (+식) | `r13_hp_meal6`, `r13_hp_meal6_wait`, `r13_hp_pick7`, `r13_hp_wood11`, `r13_hp_visit11`, `r13_hp_house11_wait` 외 3 |
| `(장면 전) room13_hidden_base.rpy` | — | — | 엄마, 다람 | `r13_hidden_base_paper1`, `r13_hidden_base_pick7`, `r13_hidden_base_marks11`, `r13_hidden_base14`, `r13_hidden_base_door14`, `r13_hidden_base_room14` 외 1 |
| `(장면 전) room13_lamp_attempt.rpy` | — | — | — | `r13_lamp_prep2` |

#### `(장면 전) room13_v111_days45.rpy` 갈림 · 값 (room13_v111_days45.rpy:4)

- `r13_v111_day4` if `r13_v111_value('silluk_status')=='detained_work_waiting_station'` `→ r13_v111_labor4`

#### `(장면 전) room13_v111_owl_prevent.rpy` 갈림 · 값 (room13_v111_owl_prevent.rpy:18)

- `r13_v111_free_day7_wait` if 「다람아, 이제 13호에 가 보자.」 `→ r13_v111_free_evening7`
- `r13_v111_free_day7_pick` elif `n==2` `$ r13_v111_set('doto_promise7',True)`
- `r13_v111_free_day7_pick` elif `n==4` `$ r13_v111_set('pocket_ration7',True)`
- `r13_v111_free_day7_pick` elif `n==5` `$ r13_v111_set('pocket_ration7',False)`
- `r13_v111_free_day7_pick` elif `n==6` `$ r13_v111_set('tongs7',True)`
- `r13_v111_free_day7_pick` elif `n==7` `$ r13_v111_set('stove13_7','empty')`
- 값
  - `snack_bagged5` = `true` (`r13_v111_snack_plate5`)
  - `doto_promise7` = `true` (`r13_v111_free_day7_pick`)
  - `pocket_ration7` = `true` (`r13_v111_free_day7_pick`)
  - `pocket_ration7` = `false` (`r13_v111_free_day7_pick`)
  - `stove13_7` = `"ration"` (`r13_v111_free_day7_pick`)
  - 자료 얻음 `NW_STONE` (`r13_v111_free_day7_pick`)
  - `tongs7` = `true` (`r13_v111_free_day7_pick`)
  - `stove13_7` = `"empty"` (`r13_v111_free_day7_pick`)
  - `route7` = `"prevented"` (`r13_v111_owl_well7`)
  - `prevention` = `"stone"` (`r13_v111_owl_well7`)
  - `choice:MS14_D07_S03` = `"stone"` (`r13_v111_owl_well7`)
  - 생사 판정 `fate_owl` = `stone` (`r13_v111_owl_well7`)
  - `OWL_ALIVE` = `true` (`r13_v111_owl_well7`)
  - `DARAM_DETAINED` = `false` (`r13_v111_owl_well7`)
  - `D07_medical_care` = `"none"` (`r13_v111_owl_well7`)
  - `route7` = `"prevented"` (`r13_v111_promise_night7`)
  - `prevention` = `"promise"` (`r13_v111_promise_night7`)
  - `choice:MS14_D07_S03` = `"promise"` (`r13_v111_promise_night7`)
  - 생사 판정 `fate_owl` = `promise` (`r13_v111_promise_night7`)
  - `OWL_ALIVE` = `true` (`r13_v111_promise_night7`)
  - `DARAM_DETAINED` = `false` (`r13_v111_promise_night7`)
  - `D07_medical_care` = `"complete"` (`r13_v111_promise_night7`)
  - `owl_reading8_done` = `true` (`r13_v111_owl_reading8`)

#### `(장면 전) room13_hidden_pandol.rpy` 갈림 · 값 (room13_hidden_pandol.rpy:32)

- `r13_hp_wood11` if `not r13_hp_value('wood_reserved')` `$ r13_v111_join(['resident_teacher'])`

#### `(장면 전) room13_hidden_base.rpy` 갈림 · 값 (room13_hidden_base.rpy:50)

- `r13_hidden_base_pick7` if `n==100 and not r13_hidden_base_value('plate_seen')` `$ r13_v111_set('hidden_base:plate_seen',True)`
- `r13_hidden_base_pick7` elif `n==101 and r13_hidden_base_value('plate_seen') and not r13_hidden_base_value('plate')` `$ r13_v111_set('hidden_base:plate',True)`
- `r13_hidden_base14` if `_return!=0` `$ r13_v111_set('hidden_base:finished',True)`
- `r13_hidden_base14` if `r13_hidden_base_value('opened')` `→ r13_hidden_base_room14`
- `r13_hidden_base_door14` if 「문틀의 홈을 살핀다」 `$ r13_v111_set('hidden_base:frame_seen',True)`
- `r13_hidden_base_door14` elif 「홈 위에 종이를 댄다」 `$ r13_v111_set('hidden_base:paper_set',True)`
- `r13_hidden_base_door14` elif 「표시한 면을 바깥으로 끼운다」 `$ r13_v111_set('hidden_base:aligned',True)`
- `r13_hidden_base_door14` elif 「표시한 면을 안으로 끼운다」 `$ r13_v111_set('hidden_base:aligned',False)`
- `r13_hidden_base_door14` elif 「문을 연다」 `→ r13_hidden_base_room14`
- `r13_hidden_base_door14` if `r13_hidden_base_value('aligned')` `→ r13_hidden_base_room14`
- `r13_hidden_base_door14` elif 「학교로 돌아가자.」 `→ r13_hidden_base_return14`
- `r13_hidden_base_room14` if 「정비 단면판을 읽는다」 `$ r13_v111_set('hidden_base:read_section',True)`
- `r13_hidden_base_room14` elif 「고장 점검표를 읽는다」 `$ r13_v111_set('hidden_base:read_incident',True)`
- `r13_hidden_base_room14` elif 「엄마의 현장 수첩을 챙긴다」 `$ r13_v111_set('hidden_base:notebook_taken',True)`
- `r13_hidden_base_room14` if `not r13_hidden_base_value('notebook_taken')` `$ r13_v111_set('hidden_base:notebook_taken',True)`
- `r13_hidden_base_room14` elif 「학교로 돌아간다」 `→ r13_hidden_base_return14`
- `r13_hidden_base_return14` if `r13_hidden_base_value('opened') and not r13_hidden_base_value('notebook_taken')` `$ r13_v111_set('hidden_base:notebook_taken',True)`
- 값
  - `hidden_base:paper` = `true` (`r13_hidden_base_paper1`)
  - `hidden_base:plate_seen` = `true` (`r13_hidden_base_pick7`)
  - `hidden_base:plate` = `true` (`r13_hidden_base_pick7`)
  - `hidden_base:marks_copied` = `true` (`r13_hidden_base_marks11`)
  - `hidden_base:finished` = `true` (`r13_hidden_base14`)
  - `hidden_base:entered` = `true` (`r13_hidden_base14`)
  - `hidden_base:frame_seen` = `true` (`r13_hidden_base_door14`)
  - `hidden_base:paper_set` = `true` (`r13_hidden_base_door14`)
  - `hidden_base:aligned` = `true` (`r13_hidden_base_door14`)
  - `hidden_base:aligned` = `false` (`r13_hidden_base_door14`)
  - `hidden_base:opened` = `true` (`r13_hidden_base_door14`)
  - `hidden_base:read_section` = `true` (`r13_hidden_base_room14`)
  - `hidden_base:read_incident` = `true` (`r13_hidden_base_room14`)
  - `hidden_base:notebook_taken` = `true` (`r13_hidden_base_room14`)
  - `hidden_base:notebook_taken` = `true` (`r13_hidden_base_return14`)
  - `hidden_base:returned` = `true` (`r13_hidden_base_return14`)
  - `hidden_base:finished` = `true` (`r13_hidden_base_return14`)

#### `(장면 전) room13_lamp_attempt.rpy` 갈림 · 값 (room13_lamp_attempt.rpy:2)

- `r13_lamp_prep2` if 「방으로 들어간다」 `$ r13_v111_set('lamp_prep_done2',True)`
- `r13_lamp_prep2` if 「남은 끈을 빌린다」 `$ r13_v111_set('lamp_cord2',True)`
- `r13_lamp_prep2` elif 「덮개의 걸쇠를 살핀다」 `$ r13_v111_set('lamp_latch_seen2',True)`
- `r13_lamp_prep2` elif `「걸쇠에 끈을 감아 고정한다」 and r13_v111_value('lamp_cord2') and r13_v111_value('lamp_latch_seen2')` `$ r13_v111_set('lamp_bound2',True)`
- 값
  - `lamp_prep_done2` = `true` (`r13_lamp_prep2`)
  - `lamp_cord2` = `true` (`r13_lamp_prep2`)
  - `lamp_latch_seen2` = `true` (`r13_lamp_prep2`)
  - `lamp_bound2` = `true` (`r13_lamp_prep2`)

## 2. 회의

기회 수는 `R13_NW_TRIES_BY_MEETING`(표에 없으면 `R13_NW_TRIES`=5). 정답 판정은 `r13_v111_proof_accepts` — 정답 세트 하나를 다 갖추고, 나머지가 다른 정답 세트나 덧붙임에 든 자료뿐이면 받는다.

| 회의 | 이름 | 날 | 기회 | 결과(코드에 있는 것) |
|---|---|---|---|---|
| `gate` | 입구 회의 | 1일 | 3 | lose, win |
| `lamp` | 등 회의 | 3일 | 7 | lose, partial, win |
| `gate_post` | 초소 회의 | 5일 | 3 | lose, win |
| `fire` | 불 회의 | 7일 | 4 | lose, partial, win |
| `room13` | 13호실 회의 | 10일 오후 | 7 | lose, partial, win |
| `records` | 기록 회의 | 10일 오후 | 4 | lose, partial, win |
| `hypothesis` | 가설 회의 | 11일 | 13 | lose, win·partial(쟁점 모두 이기면 win) |
| `soup` | 수프 회의 | 12일 | 5 | lose, partial, win |
| `blanket` | 담요 회의 | 13일 | 4 | lose, partial, win |
| `piko` | 피코 회의 | 13일 | 4 | lose, win |
| `altar` | 제단 회의 | 14일 | 6 | lose, win·partial(쟁점 모두 이기면 win) |

회의 밖 대조(기회를 쓰지 않는 자료 맞추기 · `R13_PROOF_MEETING` 에 없음)

- 두 편지를 나란히 본다 — 정답 E01+E06 (room13_v111_days123.rpy:382)
- 측정 종료와 점검 기록을 대조한다 — 정답 E13+E11 (room13_v111_days123.rpy:946)
- 두 편지의 초대를 대조한다 — 정답 E01+E27 (room13_v111_days45.rpy:565)

### 입구 회의 `gate` · 1일 · 기회 3

| 증명 키(쟁점) | 화면 제목 | 정답 | 대체 정답 | 덧붙여도 받음 | 자리 |
|---|---|---|---|---|---|
| 함께 들어갈 근거를 고른다 | — | E02+E03+E04 | — | E01 | room13_v111_days123.rpy:216 |

결과마다 바뀌는 값

- `"win"` · `r13_v111_gate_proven` (room13_v111_days123.rpy:229)
- `"win"` · `r13_v111_gate_early` (room13_v111_days123.rpy:237)
- `"lose"` · `r13_v111_gate_number` (room13_v111_days123.rpy:250): `gate_hardened` = `true`; `gate_daram_unlisted` = `true`
- `"lose"` · `r13_v111_gate_wrong` (room13_v111_days123.rpy:262): `gate_daram_unlisted` = `true`

이 회의를 읽는 조건: `gate_last_try`, `gate_partial_retry`, `gate_post_half`, `gate_retry`

### 등 회의 `lamp` · 3일 · 기회 7

선택지 쟁점

- `menu:trial_knife` (room13_v111_days123.rpy:1116)
  - 「안쪽 파편과 칼끝을 대조한다」 — 통과
  - 「칼 모양만으로 지목한다」 — 틀림(기회 사용 또는 회의 끝)
  - 「자료를 다시 본다」 — 통과

| 증명 키(쟁점) | 화면 제목 | 정답 | 대체 정답 | 덧붙여도 받음 | 자리 |
|---|---|---|---|---|---|
| 수리와 반출을 가릴 자료를 낸다 | 톡이 고친 뒤에 등을 본 기록을 낸다 | E11+E12+E13 | — | E10 | room13_v111_days123.rpy:1089 |
| 돌과 매입 기록을 낸다 | — | E15+E16 | — | — | room13_v111_days123.rpy:1100 |
| 바깥 걸쇠 주장과 발견 위치를 대조한다 | — | E17+E32+E33 | — | — | room13_v111_days123.rpy:1150 |
| 마지막 점검과 인수한 돌을 연결한다 | — | E11+E15+E16 | — | — | room13_v111_days123.rpy:1161 |
| 수리 뒤 새로 생긴 파손을 가린다 | — | NW_LA_CHECK+NW_LA_FIELD | — | — | room13_lamp_attempt.rpy:59 |
| 남아 있는 돌과 칼의 사용을 연결한다 | — | NW_LA_CHECK+NW_LA_FIELD+NW_LA_KNIFE | — | — | room13_lamp_attempt.rpy:74 |

결과마다 바뀌는 값

- `"partial"` · `r13_v111_knife_wrong` (room13_v111_days123.rpy:1145)
- `"win"` · `r13_v111_badugi_arrives` (room13_v111_days123.rpy:1173)
- `"lose"` · `r13_v111_trial_wrong` (room13_v111_days123.rpy:1266): 명단 올림 톡 (까닭 `lamp_lose`)
- `"partial"` · `r13_v111_trial_wrong_sale` (room13_v111_days123.rpy:1284)
- `"partial"` · `r13_v111_trial_wrong_latch` (room13_v111_days123.rpy:1301)
- `"partial"` · `r13_v111_trial_wrong_stone` (room13_v111_days123.rpy:1318)
- `"lose"` · `r13_lamp_attempt_wrong3` (room13_lamp_attempt.rpy:69): 명단 올림 톡 (까닭 `lamp_lose`)
- `"partial"` · `r13_lamp_attempt_partial3` (room13_lamp_attempt.rpy:80)
- `"win"` · `r13_lamp_attempt_win3` (room13_lamp_attempt.rpy:86): `outer_latch_claim_refuted` = `true`

이 회의를 읽는 조건: `karo_heard_iron5`, `lamp_last_try`, `lamp_lose`, `lamp_not_lose`, `lamp_not_win`, `lamp_partial`, `lamp_partial_latch`, `lamp_partial_sale`, `lamp_partial_stone`, `lamp_win`, `tok_freed3`

### 초소 회의 `gate_post` · 5일 · 기회 3

| 증명 키(쟁점) | 화면 제목 | 정답 | 대체 정답 | 덧붙여도 받음 | 자리 |
|---|---|---|---|---|---|
| 밤이 혐의의 근거를 확인한다 | — | E20+E22+E23+E24 | E20+E22+NW_PIKO_SKETCH4 / E20+E22+E23+NW_PIKO_SKETCH4 / E20+E22+E24+NW_PIKO_SKETCH4 | E21, NW_PIKO_SKETCH4 | room13_v111_days45.rpy:487 |

결과마다 바뀌는 값

- `"lose"` · `r13_v111_wrong5` (room13_v111_days45.rpy:494): 명단 올림 밤이 (까닭 `gate_post_lose`); `bami_status` = `"listed"`
- `"win"` · `r13_v111_bami_clear5` (room13_v111_days45.rpy:506)

이 회의를 읽는 조건: `gate_post_half`, `gate_post_last_try`, `gate_post_lose`, `gate_post_win`

### 불 회의 `fire` · 7일 · 기회 4

| 증명 키(쟁점) | 화면 제목 | 정답 | 대체 정답 | 덧붙여도 받음 | 자리 |
|---|---|---|---|---|---|
| 불이 시작된 곳과 진술을 대조한다 | — | E06_FIRE | — | — | room13_v111_days610.rpy:527 |
| 불의 원인과 빈 창고 진압을 구분한다 | — | E06_FIRE+E06_EMPTY+E07_NUBI | E06_FIRE+E06_EMPTY+NW_NUBI_TICKET | NW_LAUNDRY_TALK, E02 | room13_v111_days610.rpy:582 |
| 불의 원인과 아이 구조를 구분한다 | — | E06_FIRE+E06_RESCUE+E07_NUBI | E06_FIRE+E06_RESCUE+NW_NUBI_TICKET | NW_LAUNDRY_TALK, E02 | room13_v111_days610.rpy:586 |

결과마다 바뀌는 값

- `"lose"` · `r13_v111_nubi_wrong7` (room13_v111_days610.rpy:534): 명단 올림 보리 (까닭 `fire_lose`)
- `"partial"` · `r13_v111_responsibility_wrong7` (room13_v111_days610.rpy:595): 명단 올림 보리 (까닭 `fire_partial`)
- `"win"` · `r13_v111_responsibility_answers7` (room13_v111_days610.rpy:600): `fire_neoul_promise_recorded` = `true`; `grand:fire` = `true`; `neoul_promise_proven` = `true`

이 회의를 읽는 조건: `fire_lose`, `fire_partial`, `fire_win`, `fire_win_plain`

### 13호실 회의 `room13` · 10일 오후 · 기회 7

| 증명 키(쟁점) | 화면 제목 | 정답 | 대체 정답 | 덧붙여도 받음 | 자리 |
|---|---|---|---|---|---|
| 두 상처와 촛대 파손을 대조한다 | — | E08_CHILD_ACCOUNT+E08_TOOL | — | — | room13_v111_days610.rpy:1421 |
| 두 번째 길을 실제 기록으로 보인다 | — | E09_PASSAGE+E08_ROOM | — | — | room13_v111_days610.rpy:1450 |
| 구리선과 수선 출처를 대조한다 | — | E08_WOUND_WIRE+E09_PIN_OWNER | E08_CONTACT_ASSEMBLY+E09_PIN_OWNER | — | room13_v111_days610.rpy:1508 |
| 첫 비명 뒤 핀을 다시 채운 때 | 핀이 언제 떨어졌는가 | E09_PIN_TIME+E09_PIN_HANDOVER_TIME | — | — | room13_v111_days610.rpy:1543 |
| 접촉면과 아이의 위치를 대조한다 | — | E08_CONTACT_ASSEMBLY+E08_WOUND_WIRE+E08_CHILD_POSITION+E08_ROOM_REACH+E09_SCARF | — | — | room13_v111_days610.rpy:1567 |

결과마다 바뀌는 값

- `"lose"` · `r13_v111_hearing_wrong10` (room13_v111_days610.rpy:1471): 명단 올림 다람 (까닭 `room13_lose`)
- `"lose"` · `r13_v111_passage_wrong10` (room13_v111_days610.rpy:1482): 명단 올림 다람 (까닭 `room13_lose`)
- `"win"` · `r13_v111_contact_answer10` (room13_v111_days610.rpy:1571): `grandmother_custody` = `"detained"`; `forgery_confirmed` = `true`
- `"partial"` · `r13_v111_owner_wrong10` (room13_v111_days610.rpy:1618): `room13_partial_kind` = `"unknown"`
- `"partial"` · `r13_v111_time_wrong10` (room13_v111_days610.rpy:1628): `room13_partial_kind` = `"unknown"`
- `"partial"` · `r13_v111_contact_wrong10` (room13_v111_days610.rpy:1638): `room13_partial_kind` = `"accident"`

이 회의를 읽는 조건: `granny_held_win`, `granny_room13_lose`, `granny_room13_partial`, `room13_lose`, `room13_not_win`, `room13_partial_accident`, `room13_partial_unknown`, `room13_win`

### 기록 회의 `records` · 10일 오후 · 기회 4

| 증명 키(쟁점) | 화면 제목 | 정답 | 대체 정답 | 덧붙여도 받음 | 자리 |
|---|---|---|---|---|---|
| 수신인과 가족 전달 권한을 구분한다 | — | E06_CONTACT+E09_MAIL | — | — | room13_v111_days610.rpy:1705 |
| 반송·필사본·초대 발송을 대조한다 | — | E01+E07+E09_MAIL | E01+E27+E09_MAIL | E07, E27, E09 | room13_v111_days610.rpy:1722 |

결과마다 바뀌는 값

- `"win"` · `r13_v111_writing_answer10` (room13_v111_days610.rpy:1726)
- `"lose"` · `r13_v111_authority_wrong10` (room13_v111_days610.rpy:1810): 명단 올림 부엉이 할아버지 (까닭 `records_lose`)
- `"partial"` · `r13_v111_writing_wrong10` (room13_v111_days610.rpy:1821)

이 회의를 읽는 조건: `records_lose`, `records_lose_fell7`, `records_lose_prev_b`, `records_lose_prev_stone`, `records_partial`, `records_partial_prev_b`, `records_partial_prev_stone`

### 가설 회의 `hypothesis` · 11일 · 기회 13

선택지 쟁점

- `menu:hyp0` (room13_v111_days1114.rpy:596)
  - 「야생화는 옮는 병이다」 — 틀림(기회 사용)
  - 「아르카가 사람을 부른다」 — 틀림(기회 사용)
  - 「꺼낸 아르카 곁에 오래 있던 사람부터 무너진다」 — 통과
  - 「늙으면 누구나 그렇게 된다」 — 틀림(기회 사용)
- `menu:hyp1` (room13_v111_days1114.rpy:632)
  - 「만지는 것보다 곁에서 오래 지내는 게 문제다」 — 통과
  - 「초롱은 젊어서 버틴다」 — 틀림(기회 사용)
  - 「초롱은 장갑을 끼고 만진다」 — 틀림(기회 사용)
- `menu:hyp2` (room13_v111_days1114.rpy:673)
  - 「켜지 않고 쌓아 둔 돌은 아무 해가 없다」 — 틀림(기회 사용)
  - 「백 부인은 그 돌 곁에서 잠을 자지 않는다」 — 통과
  - 「백 부인은 돌을 팔기만 한다」 — 틀림(기회 사용)
- `menu:hyp3` (room13_v111_days1114.rpy:714)
  - 「요즘 사람들이 약해졌다」 — 틀림(기회 사용)
  - 「외지 사람이 병을 들여왔다」 — 틀림(기회 사용)
  - 「요즘 태우는 돌이 더 독하다」 — 통과
- `menu:hyp4` (room13_v111_days1114.rpy:755)
  - 「아이 방에도 아르카등이 밤새 켜져 있었다」 — 통과
  - 「아이들은 어른보다 약하다」 — 틀림(기회 사용)
  - 「아이들이 아르카를 만지고 논다」 — 틀림(기회 사용)
- `menu:hyp5` (room13_v111_days1114.rpy:796)
  - 「한 방의 돌이 바뀌자 한 사람이 한 저녁 사이에 무너졌다」 — 통과 · 조건 `r13_v111_value('OWL_ALIVE') is False`
  - 「한 방의 돌을 치우자 무너지던 사람이 돌아왔다」 — 통과 · 조건 `r13_v111_value('OWL_ALIVE') is not False and r13_v111_value('prevention')!='stone'`
  - 「한 방의 돌을 꺼내자 그 앞에서 흐려지던 머리가 맑아졌다」 — 통과 · 조건 `r13_v111_value('prevention')=='stone'`
  - 「부엉이 어르신은 원래 아팠다」 — 틀림(기회 사용)
  - 「13호가 추워서 그렇다」 — 틀림(기회 사용)

| 증명 키(쟁점) | 화면 제목 | 정답 | 대체 정답 | 덧붙여도 받음 | 자리 |
|---|---|---|---|---|---|
| 초롱과 피코의 하루를 대조한다 | — | E11+E08+NW_PIKO_TREMOR | E11+NW_PIKO_TREMOR | E08, E28 | room13_v111_days1114.rpy:651 |
| 창고에서 잠자는 사람을 짚는다 | — | NW_KEEPER_DATE | — | — | room13_v111_days1114.rpy:692 |
| 요즘 돌이 어디서 오는지 대조한다 | — | NW_INNER_PRICE+NW_MUSOE_DEEP | — | E14 | room13_v111_days1114.rpy:733 |
| 아르카가 없는 아이들과 대조한다 | — | NW_KKOMI_NOSTONE+NW_SICK_BEDS | — | — | room13_v111_days1114.rpy:774 |
| 13호 난로의 돌을 내놓는다 | — | NW_STONE | — | — | room13_v111_days1114.rpy:820 |

결과마다 바뀌는 값

- `"win" if all(r13_v111_value("hyp_issue:%d"%i)=="won" for i in (1,2,3,4)) else "partial"` · `r13_v111_hyp5_won11` (room13_v111_days1114.rpy:834)
- `"lose"` · `r13_v111_hyp_lost_gate11` (room13_v111_days1114.rpy:839)

이 회의를 읽는 조건: `hyp_final`, `hyp_lose`, `hyp_lose_none_won`, `hyp_lose_some_won`, `hyp_not_lose`, `hyp_partial`, `hyp_retry`, `hyp_win`, `wild_omen12`, `wild_omen13_gate`, `wild_omen13_gate_kept`, `wild_omen13_gate_relit`, `wild_omen13_karo`

### 수프 회의 `soup` · 12일 · 기회 5

| 증명 키(쟁점) | 화면 제목 | 정답 | 대체 정답 | 덧붙여도 받음 | 자리 |
|---|---|---|---|---|---|
| 재사용 설명과 개봉 봉인을 대조한다 | — | E12_FRAGMENT+E12_SEAL | — | — | room13_v111_days1114.rpy:1416 |
| 파편·봉인·취급 구간을 함께 제시한다 | — | E12_FRAGMENT+E12_SEAL+E12_HANDLING | — | — | room13_v111_days1114.rpy:1501 |
| 명단과 흰 그릇을 대조한다 | — | NW_TRANSFER_LIST+NW_WHITE_BOWLS | NW_WHITE_BOWLS+NW_RETURNED_BOWL | NW_RETURNED_BOWL, NW_SICK_BEDS | room13_v111_days1114.rpy:1546 |

결과마다 바뀌는 값

- `"partial"` · `r13_v111_list_wrong12` (room13_v111_days1114.rpy:1552)
- `"win"` · `r13_v111_list_won12` (room13_v111_days1114.rpy:1557): `transfer_list_secured` = `true`; `grand:soup` = `true`; `transfer_list_voided` = `true`
- `"lose"` · `r13_v111_medicine_wrong12` (room13_v111_days1114.rpy:1575): `soup_lose_kind` = `"stolen"`; `seori_disciplined` = `true`
- `"lose"` · `r13_v111_fragment_wrong12` (room13_v111_days1114.rpy:1586): `soup_lose_kind` = `"nabi"`; 명단 올림 나비 (까닭 `soup_lose`)

이 회의를 읽는 조건: `soup_lose_nabi`, `soup_lose_nabi_murder`, `soup_lose_nabi_prevented`, `soup_lose_stolen`

### 담요 회의 `blanket` · 13일 · 기회 4

| 증명 키(쟁점) | 화면 제목 | 정답 | 대체 정답 | 덧붙여도 받음 | 자리 |
|---|---|---|---|---|---|
| 아내가 봤다는 담요의 시점을 확인한다 | — | E13_MENDING | — | E35 | room13_v111_days1114.rpy:1953 |
| 촌장이 어젯밤 있던 곳을 확인한다 | — | NW_HALL_WINDOW | — | E29 | room13_v111_days1114.rpy:1971 |

결과마다 바뀌는 값

- `"partial"` · `r13_v111_badook_wrong13` (room13_v111_days1114.rpy:1978)
- `"win"` · `r13_v111_badook_won13` (room13_v111_days1114.rpy:1983)
- `"lose"` · `r13_v111_mending_wrong13` (room13_v111_days1114.rpy:2004): `departed_names` = `_aboard`; `"departed:"+_p` = `true`; `location:daram` = `"cart"`; `cart_departed` = `true`; `outcome13` = `"partial_rescue"`

이 회의를 읽는 조건: `blanket_partial`, `blanket_undecided`

### 피코 회의 `piko` · 13일 · 기회 4

| 증명 키(쟁점) | 화면 제목 | 정답 | 대체 정답 | 덧붙여도 받음 | 자리 |
|---|---|---|---|---|---|
| 인수하지 않은 돌의 약속 값을 보인다 | — | NW_LA_OFFER | — | — | room13_v111_days1114.rpy:2107 |
| 장부의 두 배를 실룩에게 보인다 | — | E16 | — | E34 | room13_v111_days1114.rpy:2109 |
| 피코가 막혀야 했던 까닭을 보인다 | — | NW_PIKO_PAINTING | — | — | room13_v111_days1114.rpy:2117 |

결과마다 바뀌는 값

- `"win"` · `r13_v111_rein_won13` (room13_v111_days1114.rpy:2121): `neoul_held` = `true`; 자료 얻음 `NW_NEOUL_LEDGER`
- `"lose"` · `r13_v111_rein_wrong13` (room13_v111_days1114.rpy:2140)

### 제단 회의 `altar` · 14일 · 기회 6

| 증명 키(쟁점) | 화면 제목 | 정답 | 대체 정답 | 덧붙여도 받음 | 자리 |
|---|---|---|---|---|---|
| 희생의 숫자와 장부를 대조한다 | — | NW_NEOUL_LEDGER | E14_SUPPLY+NW_KKOMI_NOSTONE+NW_SICK_BEDS | — | room13_v111_days1114.rpy:2920 |
| 아르카가 부른다는 말과 옛 기록을 대조한다 | — | NW_TABLET_A+NW_TABLET_B | — | — | room13_v111_days1114.rpy:2959 |
| 쇠가 언제 붙었는지 보인다 | — | NW_IRON_MARK | — | — | room13_v111_days1114.rpy:2987 |
| 맨 처음 이름을 짚는다 | — | NW_NAMES+NW_NEOUL_LEDGER | NW_NAMES+NW_OLD_RATIONS | NW_BURNT_PAGE | room13_v111_days1114.rpy:3015 |

결과마다 바뀌는 값

- `"win" if all(r13_v111_value("altar_issue:%d"%i)=="won" for i in (1,2,3,4)) else "partial"` · `r13_v111_altar_close14` (room13_v111_days1114.rpy:3033)
- `"lose"` · `r13_v111_altar_lost14` (room13_v111_days1114.rpy:3040)

이 회의를 읽는 조건: `altar_lose`, `altar_partial`, `altar_win`, `end_morning_lost`, `end_morning_partial`, `end_morning_won`

## 3. 생사 · 명단 · 결말

### 죽음으로 세는 사람(`R13_NW_LIVES`)

| 인물 | 살아 있음을 적는 값 (False 면 죽음) |
|---|---|
| 피코 (`resident_piko`) | `piko_alive` |
| 꼬미 (`kid_kkomi`) | `KKOMI_ALIVE` |
| 부엉이 할아버지 (`resident_owlgp`) | `OWL_ALIVE` |
| 네로 (`resident_nero`) | `nero_alive` |
| 도담 (`kid_dodam`) | `alive:kid_dodam` |
| 너울 (`neoul`) | `alive:neoul` |
| 모모 (`resident_momo`) | `alive:resident_momo` |
| 아랫길 노인 (`v111_lowerroad_elder`) | `alive:v111_lowerroad_elder` |

그 밖에 `r13_nw_is_dead`: 도담은 `route12 == "late_exposure"` 이면 죽음. `r13_nw_dead`: 13일 수레로 떠난 사람(`departed_names`, 다람 빼고)도 죽음으로 센다. 「얼어붙은 마을」 기준 `R13_NW_FROZEN_AT` = 4.

```python
def r13_nw_is_dead(who,key):
    if r13_v111_value(key) is False:return True
    return who=="kid_dodam" and r13_v111_value("route12")=="late_exposure"
```

```python
def r13_nw_dead():
    dead=[who for who,key in R13_NW_LIVES if r13_nw_is_dead(who,key)]
    # D2: 13일 수레로 실려 간 사람은 돌아오지 못한다. 다람은 「남겨진 이름」이 따로 받는다.
    dead+=[p for p in (r13_v111_value("departed_names") or []) if p!="daram" and p not in dead]
    return dead
```

```python
def r13_nw_ending14():
    if r13_v111_value("departed:daram"):return "left_name"
    if r13_nw_loss_count()>=R13_NW_FROZEN_AT:return "frozen"
    outcome=r13_v111_value("outcome13")
    if outcome=="family_priority":return "family"
    if outcome=="partial_rescue":return "partial"
    if r13_v111_value("crowd_injury"):return "violence"
    return "morning"
```

```python
def r13_nw_true_ending_ready():
    """Morning ending with no one lost (R13_NW_LIVES), Neoul's ledger held, records/hypothesis/blanket/altar
    won, and both grand wins (2026-10-24 MEETING_RULES_V2.md 3장, GRAND_WIN_DESIGN.md 2-5): 7일 불 회의를
    배급표로, 12일 수프 회의를 돌아온 그릇으로 이긴 판. 12일 국을 미리 막은 판은 돌목에게 그릇을 보인
    대화가 수프 대승리를 대신한다(결정 7)."""
    if r13_v111_value("ending14")!="morning" or r13_nw_loss_count():return False
    if not r13_v111_owned("NW_NEOUL_LEDGER"):return False
    if not (r13_v111_value("grand:fire") is True and r13_v111_value("grand:soup") is True):return False
    return all(r13_v111_value("meeting:"+m)=="win" for m in ("records","hypothesis","blanket","altar"))
```

### 결말 이름과 판정 순서

| 순서 | 값 | 이름 |
|---|---|---|
| 1 | `left_name` | 남겨진 이름 |
| 2 | `frozen` | 얼어붙은 마을 |
| 3 | `family` | 함께 떠난 가족 |
| 4 | `partial` | 남은 사람들 |
| 5 | `violence` | 상처 입은 귀환 |
| 6 | `morning` | 마을의 아침 |
| 승격 | `true` | 새로운 아침 — `ending14 == "morning"` 에서 `r13_nw_true_ending_ready()` 가 참일 때 |

### 생사 판정 시점(`r13_fork_set_fate`)

| 판정 | 결과 | 적는 자리 |
|---|---|---|
| `fate_piko` | `saved` 들임 | `r13_v111_shelter_done` (room13_v111_days123.rpy:712), `r13_v111_day3` (room13_v111_days123.rpy:795) |
| `fate_piko` | `lost` 꺼진 등 | `r13_v111_day3` (room13_v111_days123.rpy:798) |
| `fate_kkomi` | `saved` 넷 인계 | `r13_v111_handoff_done6` (room13_v111_days610.rpy:252) |
| `fate_kkomi` | `lost` 타 버린 창고 | `r13_v111_afternoon6` (room13_v111_days610.rpy:162) |
| `fate_owl` | `stone` 식은 돌 | `r13_v111_owl_well7` (room13_v111_owl_prevent.rpy:78) |
| `fate_owl` | `promise` 내려가지 않은 당번 | `r13_v111_promise_night7` (room13_v111_owl_prevent.rpy:97) |
| `fate_owl` | `lost` 닫힌 문 | `r13_v111_handover7` (room13_v111_days610.rpy:733) |
| `fate_nero` | `handover` 인계 | `r13_v111_lower_safe11` (room13_v111_days1114.rpy:878), `r13_v111_rescue_handoff11` (room13_v111_days1114.rpy:952) |
| `fate_nero` | `rescue` 구조 | `r13_v111_rescue_handoff11` (room13_v111_days1114.rpy:954) |
| `fate_nero` | `lost` 끊긴 등불 | `r13_v111_late_road11` (room13_v111_days1114.rpy:988) |
| `fate_soup` | `early` 조기 예방 | `r13_v111_early12` (room13_v111_days1114.rpy:1729) |
| `fate_soup` | `premeal` 먹기 전 중단 | `r13_v111_premeal12` (room13_v111_days1114.rpy:1344) |
| `fate_soup` | `lost` 작은 냄비 | `r13_v111_take_daram12` (room13_v111_days1114.rpy:1265), `r13_v111_leave_daram12` (room13_v111_days1114.rpy:1274) |
| `fate_crowd` | `supervisor` 감독자 | `r13_v111_crowd_guard13` (room13_v111_days1114.rpy:2708) |
| `fate_crowd` | `block` 막아섬 | `r13_v111_crowd_block13` (room13_v111_days1114.rpy:2677) |
| `fate_crowd` | `riot` 올라간 주먹 | `r13_v111_crowd_watch13` (room13_v111_days1114.rpy:2720) |

### 이송 명단(`r13_nw_list`)

올릴 수 있는 사람: 톡, 밤이, 보리, 나비, 다람, 부엉이 할아버지, 피코, 실룩, 굴돌, 사자 선생님, 엄마, 아빠

| 인물 | 까닭 | 자리 |
|---|---|---|
| 실룩 | `lamp_transfer` | `r13_v111_silluk_transfer` (room13_v111_days123.rpy:1256) |
| 톡 | `lamp_lose` | `r13_v111_trial_wrong` (room13_v111_days123.rpy:1267) |
| 밤이 | `gate_post_lose` | `r13_v111_wrong5` (room13_v111_days45.rpy:495) |
| 보리 | `fire_lose` | `r13_v111_nubi_wrong7` (room13_v111_days610.rpy:535) |
| 보리 | `fire_partial` | `r13_v111_responsibility_wrong7` (room13_v111_days610.rpy:596) |
| 다람 | `room13_lose` | `r13_v111_hearing_wrong10` (room13_v111_days610.rpy:1472) |
| 다람 | `room13_lose` | `r13_v111_passage_wrong10` (room13_v111_days610.rpy:1483) |
| 부엉이 할아버지 | `records_lose` | `r13_v111_authority_wrong10` (room13_v111_days610.rpy:1811) |
| 굴돌 | `facility` | `r13_v111_hyp_end11` (room13_v111_days1114.rpy:845) |
| 나비 | `soup_lose` | `r13_v111_fragment_wrong12` (room13_v111_days1114.rpy:1588) |
| 피코 | `street` | `r13_v111_day13` (room13_v111_days1114.rpy:1788) |
| 톡 | `lamp_lose` | `r13_lamp_attempt_wrong3` (room13_lamp_attempt.rpy:70) |

### 수레로 떠남(`departed:`)

- `r13_v111_mending_wrong13` (room13_v111_days1114.rpy:2015): `departed_names` = `_aboard`
- `r13_v111_mending_wrong13` (room13_v111_days1114.rpy:2016): for _p in _aboard:r13_v111_set("departed:"+_p,True)
- `r13_v111_family_exit13` (room13_v111_days1114.rpy:2581): `departed_unrescued` = `true`

## 4. 조건 이름(`R13_NW_WHEN`)

대사 패치(`game/v111/newworld/dNN.json`)의 `"when"` 과 코드의 `R13_NW_WHEN["이름"]()` 이 쓰는 이름. 「쓰는 곳」은 그 이름이 나오는 날짜 패치·코드 파일.

| 이름 | 식 | 쓰는 곳 |
|---|---|---|
| `altar4_won_with_burnt_page` | `"V111:NW_BURNT_PAGE" in (r13_v111_value("proof_given:맨 처음 이름을 짚는다") or [])` | d14 |
| `altar4_won_with_ledger` | `"V111:NW_NEOUL_LEDGER" in (r13_v111_value("proof_given:맨 처음 이름을 짚는다") or [])` | d14 |
| `altar4_won_with_rations` | `"V111:NW_OLD_RATIONS" in (r13_v111_value("proof_given:맨 처음 이름을 짚는다") or []) and "V111:NW_NEOUL_LEDGER" not in (r13_v111_value("proof_given:맨 처음 이름을 짚는다") or [])` | d14 |
| `altar_lose` | `r13_v111_value("meeting:altar")=="lose"` | d14 |
| `altar_partial` | `r13_v111_value("meeting:altar")=="partial"` | d14 |
| `altar_win` | `r13_v111_value("meeting:altar")=="win"` | d14 |
| `always` | `True` | — |
| `badook_won_with_e29` | `"V111:E29" in (r13_v111_value("proof_given:촌장이 어젯밤 있던 곳을 확인한다") or [])` | d13 |
| `bami_cold4` | `r13_v111_value("bami_cold4") is True` | d04, d05 |
| `bami_warm4` | `r13_v111_value("bami_cold4") is not True` | d04 |
| `blanket_partial` | `r13_v111_value("meeting:blanket")=="partial"` | d13 |
| `blanket_undecided` | `r13_v111_value("meeting:blanket") is None` | d13 |
| `blanket_won_with_e35` | `"V111:E35" in (r13_v111_value("proof_given:아내가 봤다는 담요의 시점을 확인한다") or [])` | d13 |
| `buri_site_ask14` | `bool(r13_v111_value("buri_device_consent")) and not r13_v111_value("mayor_site_decided") and r13_v111_person_alive("buri")` | d14 |
| `crowd_block_failed13` | `r13_v111_value("crowd_intervention")=="failed" and r13_v111_value("crowd_blocked_by_dad") is True` | d14 |
| `d06_bowl_together` | `r13_v111_value("choice:MS14_D06_S01")=="together"` | d06 |
| `daram_deal_freed` | `r13_v111_value("daram_deal_freed") is True` | d13, d14 |
| `daram_departs13` | `r13_v111_value("listed:daram") is True and r13_v111_value("transfer_list_voided") is not True` | d13 |
| `daram_listed_unhanded` | `r13_v111_value("listed:daram") is True and not r13_v111_value("handed:daram")` | d13 |
| `daram_listed_unvoided13` | `r13_v111_value("listed:daram") is True and not (r13_v111_value("transfer_list_voided") is True and r13_v111_actor_ready("guard"))` | d13 |
| `daram_listed_voided13` | `r13_v111_value("listed:daram") is True and r13_v111_value("transfer_list_voided") is True and r13_v111_actor_ready("guard")` | d13 |
| `daram_not_deal_freed` | `r13_v111_value("daram_deal_freed") is not True` | d14 |
| `daram_not_watching13` | `not (r13_v111_actor_ready("daram") and r13_v111_value("listed:daram") is not True)` | d13 |
| `daram_ready` | `r13_v111_actor_ready("daram")` | d02, d03, d05, d12, d13 |
| `daram_watching13` | `r13_v111_actor_ready("daram") and r13_v111_value("listed:daram") is not True` | d13 |
| `dead:kid_dodam` | `"kid_dodam" in r13_nw_dead()` | d14 |
| `dead:kid_kkomi` | `"kid_kkomi" in r13_nw_dead()` | d14 |
| `dead:neoul` | `"neoul" in r13_nw_dead()` | d14 |
| `dead:resident_momo` | `"resident_momo" in r13_nw_dead()` | d14 |
| `dead:resident_nero` | `"resident_nero" in r13_nw_dead()` | d14 |
| `dead:resident_owlgp` | `"resident_owlgp" in r13_nw_dead()` | d14 |
| `dead:resident_piko` | `"resident_piko" in r13_nw_dead()` | d14 |
| `dead:v111_lowerroad_elder` | `"v111_lowerroad_elder" in r13_nw_dead()` | d14 |
| `departed_any` | `any(p!="daram" for p in (r13_v111_value("departed_names") or []))` | d14 |
| `dodam_spoon12` | `r13_v111_value("dodam_spoon12") is True` | d12 |
| `dodam_spoon_lent` | `r13_v111_value("dodam_spoon7") is True and r13_v111_actor_ready("daram")` | d12 |
| `end_family` | `r13_v111_value("ending14")=="family"` | d14 |
| `end_injury` | `bool(r13_v111_value("crowd_injury"))` | d14 |
| `end_morning_lost` | `r13_v111_value("ending14")=="morning" and r13_v111_value("meeting:altar")=="lose"` | d14 |
| `end_morning_partial` | `r13_v111_value("ending14")=="morning" and r13_v111_value("meeting:altar")=="partial"` | d14 |
| `end_morning_won` | `r13_v111_value("ending14")=="morning" and r13_v111_value("meeting:altar")=="win" and not r13_nw_true_ending_ready()` | d14 |
| `end_partial_departed` | `r13_v111_value("ending14")=="partial" and bool(r13_v111_value("cart_departed"))` | d14 |
| `end_partial_done` | `r13_v111_value("ending14")=="partial" and not r13_v111_value("cart_departed") and bool(r13_v111_value("pending_handover_completed"))` | d14 |
| `end_partial_waiting` | `r13_v111_value("ending14")=="partial" and not r13_v111_value("cart_departed") and not r13_v111_value("pending_handover_completed")` | d14 |
| `end_portrait_child` | `r13_v111_value("piko_alive") is False and r13_v111_value("portrait")=="child_completed" and not r13_nw_true_ending_ready()` | d14 |
| `family_on_square` | `r13_v111_value("family_location")=="square" and r13_v111_actor_ready("daram")` | d13 |
| `family_priority` | `r13_v111_value("outcome13")=="family_priority"` | d14 |
| `fire_evacuated` | `r13_v111_value("FIRE_EVACUATED") is True` | d06, d07 |
| `fire_grand` | `r13_v111_value("grand:fire") is True` | d07 |
| `fire_lose` | `r13_v111_value("meeting:fire")=="lose"` | d07 |
| `fire_not_evacuated` | `r13_v111_value("FIRE_EVACUATED") is not True` | d07 |
| `fire_partial` | `r13_v111_value("meeting:fire")=="partial"` | d07 |
| `fire_win` | `r13_v111_value("meeting:fire")=="win"` | d07 |
| `fire_win_plain` | `r13_v111_value("meeting:fire")=="win" and r13_v111_value("grand:fire") is not True` | d07 |
| `gate_daram_listed` | `r13_v111_value("gate_daram_unlisted") is not True` | d01 |
| `gate_daram_unlisted` | `r13_v111_value("gate_daram_unlisted") is True` | d01, d14 |
| `gate_last_try` | `(r13_v111_value("tries:gate") or 0)+1>=r13_nw_tries_max("gate")` | d01 |
| `gate_partial_retry` | `(r13_v111_value("tries:gate") or 0)+1<r13_nw_tries_max("gate") and bool(set(getattr(store,"v111_last_presented",None) or [])&{"V111:E02","V111:E03","V111:E04"})` | d01 |
| `gate_post_half` | `(r13_v111_value("tries:gate_post") or 0)>0 and r13_v111_value("meeting:gate_post") is None` | d05 |
| `gate_post_last_try` | `r13_v111_value("meeting:gate_post") is None and r13_nw_tries_left("gate_post")==1` | d05 |
| `gate_post_lose` | `r13_v111_value("meeting:gate_post")=="lose"` | d05 |
| `gate_post_win` | `r13_v111_value("meeting:gate_post")=="win"` | d05 |
| `gate_post_won_with_e21` | `"V111:E21" in (r13_v111_value("proof_given:밤이 혐의의 근거를 확인한다") or [])` | d05 |
| `gate_post_won_with_sketch` | `"V111:NW_PIKO_SKETCH4" in (r13_v111_value("proof_given:밤이 혐의의 근거를 확인한다") or [])` | d05 |
| `gate_post_won_with_sketch_only` | `"V111:NW_PIKO_SKETCH4" in (r13_v111_value("proof_given:밤이 혐의의 근거를 확인한다") or []) and not {"V111:E23","V111:E24"}&set(r13_v111_value("proof_given:밤이 혐의의 근거를 확인한다") or [])` | d05 |
| `gate_retry` | `(r13_v111_value("tries:gate") or 0)+1<r13_nw_tries_max("gate")` | d01 |
| `gate_won_with_e01` | `"V111:E01" in (r13_v111_value("proof_given:함께 들어갈 근거를 고른다") or [])` | d01 |
| `grand_soup` | `r13_v111_value("grand:soup") is True` | d12 |
| `grand_soup_guard` | `r13_v111_value("grand:soup") is True and r13_v111_actor_ready("guard")` | d12 |
| `grand_soup_noguard` | `r13_v111_value("grand:soup") is True and not r13_v111_actor_ready("guard")` | d12 |
| `granny_held_win` | `r13_v111_value("OWL_ALIVE") is False and r13_v111_value("meeting:room13")=="win"` | d14 |
| `granny_room13_lose` | `r13_v111_value("OWL_ALIVE") is False and r13_v111_value("meeting:room13")=="lose"` | d14 |
| `granny_room13_partial` | `r13_v111_value("OWL_ALIVE") is False and r13_v111_value("meeting:room13")=="partial"` | d14 |
| `guard_ready` | `r13_v111_actor_ready("guard")` | d12, d13 |
| `guldol_absent` | `not r13_v111_actor_ready("resident_guldol")` | d11 |
| `guldol_ready` | `r13_v111_actor_ready("resident_guldol")` | d11 |
| `has_burnt_page` | `r13_v111_owned("NW_BURNT_PAGE")` | d14 |
| `has_ledger` | `r13_v111_owned("NW_NEOUL_LEDGER")` | d14 |
| `heard_inn_order1` | `r13_v111_value("heard_inn_order1") is True` | d11 |
| `hp_known_trusted` | `bool(r13_v111_value("hidden_pandol:met")) and R13_NW_WHEN["town_won_before11"]()` | d11 |
| `hp_known_untrusted` | `bool(r13_v111_value("hidden_pandol:met")) and R13_NW_WHEN["town_won_none_before11"]()` | d11 |
| `hp_unknown_trusted` | `not r13_v111_value("hidden_pandol:met") and R13_NW_WHEN["town_won_before11"]()` | d11 |
| `hp_unknown_untrusted` | `not r13_v111_value("hidden_pandol:met") and R13_NW_WHEN["town_won_none_before11"]()` | d11 |
| `hyp1_won_with_e28` | `"V111:E28" in (r13_v111_value("proof_given:초롱과 피코의 하루를 대조한다") or [])` | d11 |
| `hyp1_won_without_e08` | `bool(r13_v111_value("proof_given:초롱과 피코의 하루를 대조한다")) and "V111:E08" not in r13_v111_value("proof_given:초롱과 피코의 하루를 대조한다")` | d11 |
| `hyp3_won_with_e14` | `"V111:E14" in (r13_v111_value("proof_given:요즘 돌이 어디서 오는지 대조한다") or [])` | d11 |
| `hyp_final` | `not (r13_v111_value("meeting:hypothesis") is None and (r13_v111_value("tries:hypothesis") or 0)<r13_nw_tries_max("hypothesis"))` | d11 |
| `hyp_lose` | `r13_v111_value("meeting:hypothesis")=="lose"` | d11, d14 |
| `hyp_lose_none_won` | `not (r13_v111_value("meeting:hypothesis")=="lose" and any(r13_v111_value("hyp_issue:%d"%i)=="won" for i in (1,2,3,4)))` | d11 |
| `hyp_lose_some_won` | `r13_v111_value("meeting:hypothesis")=="lose" and any(r13_v111_value("hyp_issue:%d"%i)=="won" for i in (1,2,3,4))` | d11 |
| `hyp_lost1` | `r13_v111_value("hyp_issue:1")=="lost"` | d11 |
| `hyp_lost2` | `r13_v111_value("hyp_issue:2")=="lost"` | d11 |
| `hyp_lost3` | `r13_v111_value("hyp_issue:3")=="lost"` | d11 |
| `hyp_lost4` | `r13_v111_value("hyp_issue:4")=="lost"` | d11 |
| `hyp_not_lose` | `r13_v111_value("meeting:hypothesis") in ("win","partial")` | d11, d14 |
| `hyp_partial` | `r13_v111_value("meeting:hypothesis")=="partial"` | d11, d14 |
| `hyp_retry` | `r13_v111_value("meeting:hypothesis") is None and (r13_v111_value("tries:hypothesis") or 0)<r13_nw_tries_max("hypothesis")` | d11 |
| `hyp_win` | `r13_v111_value("meeting:hypothesis")=="win"` | d11, d14 |
| `karo_absent` | `not r13_v111_actor_ready("karo")` | d11 |
| `karo_guard_not_ready13` | `not (r13_v111_actor_ready("karo") and r13_v111_actor_ready("guard"))` | d13 |
| `karo_guard_ready13` | `r13_v111_actor_ready("karo") and r13_v111_actor_ready("guard")` | d13 |
| `karo_heard_iron5` | `r13_v111_value("meeting:lamp") in ("win","partial") and r13_v111_value("listed:resident_tok") is not True and r13_v111_actor_ready("karo")` | d05 |
| `karo_ready` | `r13_v111_actor_ready("karo")` | d11 |
| `karo_ready11` | `r13_v111_actor_ready("karo")` | d11 |
| `kkomi_acorn_shared` | `r13_v111_value("kkomi_acorn10") is True and r13_v111_actor_ready("daram")` | d12 |
| `kkomi_alive` | `r13_v111_value("KKOMI_ALIVE") is not False` | d07 |
| `kkomi_dead` | `r13_v111_value("KKOMI_ALIVE") is False` | d07 |
| `kkomi_seat6` | `r13_v111_value("kkomi_seat6") is True` | d06 |
| `lamp_attempt` | `bool(r13_v111_value("lamp_bound2"))` | d04, d13 |
| `lamp_attempt_outside` | `bool(r13_v111_value("lamp_bound2")) and not r13_v111_value("piko_sheltered")` | — |
| `lamp_attempt_sheltered` | `bool(r13_v111_value("lamp_bound2")) and bool(r13_v111_value("piko_sheltered"))` | — |
| `lamp_attempt_silluk_listed` | `bool(r13_v111_value("lamp_bound2")) and bool(r13_v111_value("listed:resident_siluk"))` | d13 |
| `lamp_last_try` | `r13_v111_value("meeting:lamp") is None and r13_nw_tries_left("lamp")==1` | d03 |
| `lamp_lose` | `r13_v111_value("meeting:lamp")=="lose"` | d03 |
| `lamp_not_lose` | `r13_v111_value("meeting:lamp")!="lose"` | d04 |
| `lamp_not_win` | `r13_v111_value("meeting:lamp") in ("partial","lose")` | d03 |
| `lamp_partial` | `r13_v111_value("meeting:lamp")=="partial"` | d03 |
| `lamp_partial_latch` | `r13_v111_value("meeting:lamp")=="partial" and r13_v111_owned("E33") and r13_v111_value("outer_latch_claim_refuted") is not True` | d03 |
| `lamp_partial_sale` | `r13_v111_value("meeting:lamp")=="partial" and not r13_v111_owned("E33")` | d03 |
| `lamp_partial_stone` | `r13_v111_value("meeting:lamp")=="partial" and r13_v111_value("outer_latch_claim_refuted") is True` | d03 |
| `lamp_stage_latch` | `r13_v111_owned("E33")` | d03 |
| `lamp_stage_sale` | `r13_v111_value("repair_opening_separated") is True` | d03 |
| `lamp_stage_stone` | `r13_v111_value("outer_latch_claim_refuted") is True` | d03 |
| `lamp_stolen` | `not r13_v111_value("lamp_bound2")` | d04, d13 |
| `lamp_stolen_silluk_listed` | `not r13_v111_value("lamp_bound2") and bool(r13_v111_value("listed:resident_siluk"))` | d13 |
| `lamp_win` | `r13_v111_value("meeting:lamp")=="win"` | d03 |
| `laundry_overheard5` | `r13_v111_value("grand_laundry_seen5") is True` | d06, d07 |
| `list_not_voided` | `r13_v111_value("transfer_list_voided") is not True` | d13 |
| `list_voided` | `r13_v111_value("transfer_list_voided") is True` | d13 |
| `listed:bami` | `r13_v111_value("listed:bami") is True` | d12, d13 |
| `listed:dad` | `r13_v111_value("listed:dad") is True` | — |
| `listed:daram` | `r13_v111_value("listed:daram") is True` | d12, d13 |
| `listed:mom` | `r13_v111_value("listed:mom") is True` | — |
| `listed:nabi` | `r13_v111_value("listed:nabi") is True` | d12, d13 |
| `listed:resident_bori` | `r13_v111_value("listed:resident_bori") is True` | d12, d13 |
| `listed:resident_guldol` | `r13_v111_value("listed:resident_guldol") is True` | d11, d12, d13 |
| `listed:resident_owlgp` | `r13_v111_value("listed:resident_owlgp") is True` | d12, d13 |
| `listed:resident_piko` | `r13_v111_value("listed:resident_piko") is True` | d13 |
| `listed:resident_siluk` | `r13_v111_value("listed:resident_siluk") is True` | d12, d13 |
| `listed:resident_teacher` | `r13_v111_value("listed:resident_teacher") is True` | — |
| `listed:resident_tok` | `r13_v111_value("listed:resident_tok") is True` | d03, d12, d13 |
| `medicine_locked` | `r13_v111_value("medicine_locked") is True` | d12 |
| `medicine_unchecked` | `not r13_v111_value("medicine_locked")` | d12 |
| `mom_daram_ready14` | `r13_v111_actor_ready("mom") and r13_v111_actor_ready("daram")` | d14 |
| `morning_with_loss14` | `r13_v111_value("ending14")=="morning" and r13_nw_loss_count()>0 and r13_v111_actor_ready("mom") and r13_v111_actor_ready("daram")` | d14 |
| `no_ledger` | `not r13_v111_owned("NW_NEOUL_LEDGER")` | d14 |
| `owl_alive` | `r13_v111_value("OWL_ALIVE") is not False` | d14 |
| `owl_dead` | `r13_v111_value("OWL_ALIVE") is False` | d11, d14 |
| `owl_fell7` | `r13_v111_value("OWL_ALIVE") is not False and r13_v111_value("prevention")!="stone"` | d08, d11 |
| `piko_alive` | `r13_v111_value("piko_alive") is not False` | d03, d13, d14 |
| `piko_alive_lamp_stolen` | `r13_v111_value("piko_alive") is not False and not r13_v111_value("lamp_bound2")` | d13 |
| `piko_dead` | `r13_v111_value("piko_alive") is False` | d03, d12, d13, d14 |
| `piko_ledger_with_e34` | `"V111:E34" in (r13_v111_value("proof_given:장부의 두 배를 실룩에게 보인다") or [])` | d13 |
| `piko_sacks2` | `r13_v111_value("piko_sacks2") is True` | d02 |
| `prep12_carrier_only` | `bool(r13_v111_value("carrier_arrived")) and not r13_v111_value("warm_seat_ready")` | d12 |
| `prep12_others_missing` | `not all(r13_v111_value(k) for k in ("warm_seat_ready","carrier_arrived","warm_support_arrived"))` | d12 |
| `prep12_seat_and_carrier` | `bool(r13_v111_value("warm_seat_ready")) and bool(r13_v111_value("carrier_arrived"))` | d12 |
| `prep12_seat_only` | `bool(r13_v111_value("warm_seat_ready")) and not r13_v111_value("carrier_arrived")` | d12 |
| `prevention_b` | `r13_v111_value("prevention") in ("B","promise")` | d08, d11 |
| `prevention_stone` | `r13_v111_value("prevention")=="stone"` | d08, d09, d11 |
| `reader_nabi` | `not (r13_v111_value("departed:nabi") or not r13_v111_person_alive("nabi"))` | d14 |
| `reader_tosil` | `bool(r13_v111_value("departed:nabi") or not r13_v111_person_alive("nabi"))` | d14 |
| `records_lose` | `r13_v111_value("meeting:records")=="lose"` | d10 |
| `records_lose_fell7` | `r13_v111_value("meeting:records")=="lose" and r13_v111_value("prevention")!="stone"` | d10 |
| `records_lose_prev_b` | `r13_v111_value("meeting:records")=="lose" and r13_v111_value("prevention")!="stone"` | d10 |
| `records_lose_prev_stone` | `r13_v111_value("meeting:records")=="lose" and r13_v111_value("prevention")=="stone"` | d10 |
| `records_partial` | `r13_v111_value("meeting:records")=="partial"` | d10 |
| `records_partial_prev_b` | `r13_v111_value("meeting:records")=="partial" and r13_v111_value("prevention")!="stone"` | d10 |
| `records_partial_prev_stone` | `r13_v111_value("meeting:records")=="partial" and r13_v111_value("prevention")=="stone"` | d10 |
| `repair_won_with_e10` | `"V111:E10" in (r13_v111_value("proof_given:수리와 반출을 가릴 자료를 낸다") or [])` | d03 |
| `riot_momo13` | `r13_v111_value("riot_momo13") is True` | d13 |
| `room13_checked_d1` | `r13_v111_owned("E06")` | d01 |
| `room13_lose` | `r13_v111_value("meeting:room13")=="lose"` | d10, d11, d12 |
| `room13_not_win` | `r13_v111_value("meeting:room13") in ("partial","lose")` | d10 |
| `room13_partial_accident` | `r13_v111_value("meeting:room13")=="partial" and r13_v111_value("room13_partial_kind")=="accident"` | d10 |
| `room13_partial_unknown` | `r13_v111_value("meeting:room13")=="partial" and r13_v111_value("room13_partial_kind")=="unknown"` | d10 |
| `room13_unchecked_d1` | `not r13_v111_owned("E06")` | d01 |
| `room13_win` | `r13_v111_value("meeting:room13")=="win"` | d11 |
| `route12_late` | `r13_v111_value("route12")=="late_exposure"` | d12 |
| `route12_stayed` | `r13_v111_value("route12")!="late_exposure"` | d12 |
| `school_supply_pending` | `not r13_v111_value("school_supply_handed")` | d11 |
| `siluk_not_listed` | `r13_v111_value("listed:resident_siluk") is not True` | d13 |
| `snack_bagged5` | `r13_v111_value("snack_bagged5") is True` | d05 |
| `snack_unbagged5` | `r13_v111_value("snack_bagged5") is not True` | d05 |
| `soup_lose_nabi` | `r13_v111_value("meeting:soup")=="lose" and r13_v111_value("soup_lose_kind")=="nabi"` | d12 |
| `soup_lose_nabi_murder` | `r13_v111_value("meeting:soup")=="lose" and r13_v111_value("soup_lose_kind")=="nabi" and r13_v111_value("route7")=="murder"` | d12 |
| `soup_lose_nabi_prevented` | `r13_v111_value("meeting:soup")=="lose" and r13_v111_value("soup_lose_kind")=="nabi" and r13_v111_value("route7")!="murder"` | d12 |
| `soup_lose_stolen` | `r13_v111_value("meeting:soup")=="lose" and r13_v111_value("soup_lose_kind")=="stolen"` | d12 |
| `stove_blue7` | `r13_v111_value("stove13_7") not in ("ration","empty")` | d07 |
| `stove_emptied7` | `r13_v111_value("stove13_7")=="empty"` | d07 |
| `stove_fixed7` | `r13_v111_value("stove13_7") in ("ration","empty")` | d07 |
| `stove_ration7` | `r13_v111_value("stove13_7")=="ration"` | d07 |
| `stove_untouched7` | `r13_v111_value("stove13_7") is None` | d07 |
| `ticket_spot_kid7` | `r13_v111_value("grand_ticket_spot_kid") is True and r13_v111_value("grand_laundry_seen5") is not True` | d07 |
| `tok_freed3` | `r13_v111_value("meeting:lamp") in ("win","partial") and r13_v111_value("listed:resident_tok") is not True` | d03, days45 |
| `tok_round_asked` | `bool(r13_v111_value("followup_read:NW_RX_F007"))` | d03 |
| `tosil_inside` | `r13_v111_value("tosil_listen")=="inside"` | d14 |
| `tosil_outside` | `r13_v111_value("tosil_listen")=="outside"` | d14 |
| `town_won_before11` | `any(r13_v111_value("meeting:"+m)=="win" for m in ("lamp","gate_post","fire","room13","records"))` | newworld_text |
| `town_won_none_before11` | `not any(r13_v111_value("meeting:"+m)=="win" for m in ("lamp","gate_post","fire","room13","records"))` | newworld_text |
| `warm_support_pending` | `not r13_v111_value("warm_support_arrived")` | d12 |
| `warm_support_ready` | `r13_v111_value("warm_support_arrived") is True` | d12 |
| `wild_alone` | `r13_v111_value("wild_family")=="alone"` | d14 |
| `wild_daram_fever` | `bool(r13_v111_value("daram_fever12"))` | d14 |
| `wild_daram_well` | `not r13_v111_value("daram_fever12")` | d14 |
| `wild_no_mom` | `r13_v111_value("wild_family")=="no_mom"` | d14 |
| `wild_omen12` | `r13_v111_value("meeting:hypothesis")=="lose" and r13_v111_actor_ready("resident_teacher")` | d12 |
| `wild_omen13_gate` | `r13_v111_value("meeting:hypothesis")=="lose" and r13_v111_actor_ready("guard") and r13_v111_actor_ready("daram")` | d13 |
| `wild_omen13_gate_kept` | `r13_v111_value("meeting:hypothesis")=="lose" and r13_v111_value("hyp_issue:1")!="won" and r13_v111_actor_ready("guard")` | d13 |
| `wild_omen13_gate_relit` | `r13_v111_value("meeting:hypothesis")=="lose" and r13_v111_value("hyp_issue:1")=="won" and r13_v111_actor_ready("guard")` | d13 |
| `wild_omen13_karo` | `r13_v111_value("meeting:hypothesis")=="lose" and r13_v111_actor_ready("karo")` | d13 |
| `wild_three` | `r13_v111_value("wild_family")=="three"` | d14 |
| `wood12_missing` | `not (r13_v111_value("warm_support_arrived") or r13_v111_value("heat_box_received"))` | d12 |
| `writing_won_with_e09` | `"V111:E09" in (r13_v111_value("proof_given:반송·필사본·초대 발송을 대조한다") or [])` | d10 |
| `writing_won_with_e27` | `"V111:E27" in (r13_v111_value("proof_given:반송·필사본·초대 발송을 대조한다") or [])` | d10 |

## 5. 자동 추출 실패

- 자동 추출 실패: room13_v111_days45.rpy:364 — 세우는 인물을 읽지 못함(변수)
