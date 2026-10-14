# 함수 덮어쓰기 지도 (자동 생성: dev/override_map.py --write)

Ren'Py는 init 우선순위 → 파일 경로 → 줄 순서로 실행한다. 아래 표는 그 순서대로이며, 마지막 줄이 게임이 실제로 부르는 바깥 층이다.
각 층은 바로 위 층을 `captured_as` 이름으로 붙잡아 부른다. 새 기능을 넣을 때 이 순서를 확인하고, 같은 우선순위에 층을 추가하지 않는다.

## `r13_topics` (11층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:160` | r13_tool_base_topics |
| 2 | 73 | `room13_tool_discovery.rpy:75` | _r13_home_topics |
| 3 | 79 | `room13_home.rpy:18` | _r13_life_topics |
| 4 | 92 | `systems/room13_livelihood_flow.rpy:35` | _r13_life_snack_topics |
| 5 | 93 | `systems/room13_livelihood_flow.rpy:96` | _r13_shop_topics |
| 6 | 94 | `systems/room13_shop.rpy:50` | _r13_firstday_topics |
| 7 | 95 | `systems/room13_first_day_flow.rpy:101` | _r13_items_topics |
| 8 | 96 | `systems/room13_items.rpy:112` | _r13_intro_topics |
| 9 | 97 | `systems/room13_intro_clues.rpy:111` | _r13_poc_topics |
| 10 | 100 | `systems/room13_poc_route.rpy:60` | _r13_daram_home_topics |
| 11 | 101 | `systems/room13_daram_home.rpy:95` |  |

## `r13_present` (10층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:343` | r13_discovery_base_present |
| 2 | 61 | `room13_discovery.rpy:38` | r13_tool_base_present |
| 3 | 73 | `room13_tool_discovery.rpy:81` | _r13_mystery_present |
| 4 | 76 | `room13_first_mystery.rpy:98` | _r13_life_present |
| 5 | 94 | `systems/room13_first_day_flow.rpy:45` | _r13_work_present |
| 6 | 96 | `systems/room13_work_clues.rpy:25` | _r13_intro_present |
| 7 | 97 | `systems/room13_intro_clues.rpy:48` | _r13_poc_present |
| 8 | 100 | `systems/room13_poc_route.rpy:66` | _r13_daram_home_present |
| 9 | 101 | `systems/room13_daram_home.rpy:142` | _r13_sound_present |
| 10 | 150 | `systems/room13_sound.rpy:161` |  |

## `r13_conversation_topic_lines` (6층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 75 | `room13_dialogue_openings_20261013.rpy:238` | _r13_mystery_topic_lines |
| 2 | 76 | `room13_first_mystery.rpy:84` | r13_tool_base_topic_lines |
| 3 | 77 | `room13_tool_discovery.rpy:183` | _r13_firstday_topic_lines |
| 4 | 95 | `systems/room13_first_day_flow.rpy:92` | _r13_intro_topic_lines |
| 5 | 97 | `systems/room13_intro_clues.rpy:90` | _r13_daram_home_topic_lines |
| 6 | 101 | `systems/room13_daram_home.rpy:103` |  |

## `r13_object_visible` (6층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 57 | `room13_life.rpy:182` | _r13_before_inspection_visible |
| 2 | 66 | `room13_inspection.rpy:162` | r13_before_gate_bundle_visible |
| 3 | 67 | `room13_gate_inspection.rpy:63` | _r13_route_object_visible |
| 4 | 90 | `room13_route_knowledge.rpy:22` | _r13_firstday_visible |
| 5 | 94 | `systems/room13_first_day_flow.rpy:15` | _r13_items_visible |
| 6 | 96 | `systems/room13_items.rpy:105` |  |

## `r13_compare_result` (5층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 78 | `room13_record_compare.rpy:8` | _r13_work_compare |
| 2 | 96 | `systems/room13_work_clues.rpy:18` | _r13_intro_compare |
| 3 | 97 | `systems/room13_intro_clues.rpy:35` | _r13_poc_compare |
| 4 | 100 | `systems/room13_poc_route.rpy:90` | _r13_daram_home_compare |
| 5 | 101 | `systems/room13_daram_home.rpy:131` |  |

## `r13_finish_topic` (5층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:169` | _r13_life_finish_topic |
| 2 | 93 | `systems/room13_livelihood_flow.rpy:100` | _r13_shop_finish_topic |
| 3 | 94 | `systems/room13_shop.rpy:61` | _r13_items_finish_topic |
| 4 | 96 | `systems/room13_items.rpy:123` | _r13_daram_home_finish |
| 5 | 101 | `systems/room13_daram_home.rpy:114` |  |

## `r13_first_mystery_notes` (5층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 76 | `room13_first_mystery.rpy:26` | _r13_firstday_notes |
| 2 | 94 | `systems/room13_first_day_flow.rpy:37` | _r13_intro_notes |
| 3 | 97 | `systems/room13_intro_clues.rpy:118` | _r13_learning_mystery_notes |
| 4 | 98 | `systems/room13_learning.rpy:121` | _r13_poc_notes |
| 5 | 100 | `systems/room13_poc_route.rpy:138` |  |

## `r13_where` (5층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:213` | _r13_before_gate_where |
| 2 | 67 | `room13_gate_continuity.rpy:9` | _r13_home_where |
| 3 | 79 | `room13_home.rpy:10` | _r13_life_where |
| 4 | 93 | `systems/room13_livelihood_flow.rpy:89` | _r13_episode_where |
| 5 | 103 | `systems/room13_episodes.rpy:55` |  |

## `r13_available` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:150` | r13_conversation_base_available |
| 2 | 70 | `room13_conversations.rpy:185` | _r13_route_available |
| 3 | 90 | `room13_route_knowledge.rpy:16` |  |

## `r13_finish_action` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:181` | _r13_mystery_finish_action |
| 2 | 76 | `room13_first_mystery.rpy:92` | _r13_items_finish_action |
| 3 | 96 | `systems/room13_items.rpy:140` |  |

## `r13_intro_goal` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 97 | `systems/room13_intro_clues.rpy:94` | _r13_poc_intro_goal |
| 2 | 100 | `systems/room13_poc_route.rpy:124` | _r13_daram_room_intro_goal |
| 3 | 101 | `systems/room13_daram_home.rpy:122` |  |

## `r13_new` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:69` | _r13_life_new |
| 2 | 94 | `systems/room13_first_day_flow.rpy:4` | _r13_fresh_new |
| 3 | 105 | `systems/room13_no_carryover.rpy:6` |  |

## `r13_places` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:203` | _r13_route_places |
| 2 | 90 | `room13_route_knowledge.rpy:28` | _r13_firstday_places |
| 3 | 94 | `systems/room13_first_day_flow.rpy:19` |  |

## `r13_bed_available` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 61 | `room13_interaction.rpy:94` | _r13_firstday_bed |
| 2 | 94 | `systems/room13_first_day_flow.rpy:31` |  |

## `r13_calendar_topic_seen` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 75 | `room13_dialogue_openings_20261013.rpy:265` | _r13_daram_home_seen |
| 2 | 101 | `systems/room13_daram_home.rpy:110` |  |

## `r13_campaign_goal` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:405` | _r13_poc_campaign_goal |
| 2 | 100 | `systems/room13_poc_route.rpy:126` |  |

## `r13_click_feedback` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 69 | `room13_feedback.rpy:8` | _r13_sound_click_feedback |
| 2 | 150 | `systems/room13_sound.rpy:194` |  |

## `r13_debate_judge` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:348` | _r13_sound_debate_judge |
| 2 | 150 | `systems/room13_sound.rpy:167` |  |

## `r13_ending_notes` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 56 | `room13_week2_rules.rpy:270` | _r13_w2e_notes |
| 2 | 109 | `systems/room13_week2_events.rpy:42` |  |

## `r13_evidence_acquired` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 69 | `room13_feedback.rpy:3` | _r13_sound_evidence_acquired |
| 2 | 150 | `systems/room13_sound.rpy:180` |  |

## `r13_has` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:100` | _r13_items_has |
| 2 | 96 | `systems/room13_items.rpy:95` |  |

## `r13_learning_job_context` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_learning.rpy:78` | _r13_poc_job_context |
| 2 | 100 | `systems/room13_poc_route.rpy:129` |  |

## `r13_life_apply_purchase` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 92 | `systems/room13_livelihood_flow.rpy:3` | _r13_sound_apply_purchase |
| 2 | 150 | `systems/room13_sound.rpy:200` |  |

## `r13_local_connections` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 60 | `room13_navigation.rpy:31` | _r13_firstday_connections |
| 2 | 94 | `systems/room13_first_day_flow.rpy:25` |  |

## `r13_next_day` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:144` | _r13_life_next_day |
| 2 | 92 | `systems/room13_livelihood_flow.rpy:11` |  |

## `r13_object_name` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 61 | `room13_interaction.rpy:84` | _r13_before_inspection_name |
| 2 | 66 | `room13_inspection.rpy:166` |  |

## `r13_record_entries` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 68 | `room13_notebook.rpy:18` | _r13_learning_record_entries |
| 2 | 98 | `systems/room13_learning.rpy:113` |  |

## `r13_secret_route_available` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 90 | `room13_route_knowledge.rpy:4` | _r13_items_route |
| 2 | 96 | `systems/room13_items.rpy:101` |  |

## `r13_shop_price` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 91 | `systems/room13_livelihood_model.rpy:30` | _r13_b3_shop_price |
| 2 | 107 | `systems/room13_bundle3.rpy:49` |  |

## `r13_stage_people` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 59 | `room13_acting.rpy:303` | _r13_daram_home_stage |
| 2 | 101 | `systems/room13_daram_home.rpy:28` |  |

## `r13_w2_action_done` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 56 | `room13_week2_rules.rpy:175` | _r13_w1c_action_done |
| 2 | 110 | `systems/room13_week1_cases.rpy:57` |  |

