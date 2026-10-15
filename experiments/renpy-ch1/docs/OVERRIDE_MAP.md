# 함수 덮어쓰기 지도 (자동 생성: dev/override_map.py --write)

Ren'Py는 init 우선순위 → 파일 경로 → 줄 순서로 실행한다. 아래 표는 그 순서대로이며, 마지막 줄이 게임이 실제로 부르는 바깥 층이다.
각 층은 바로 위 층을 `captured_as` 이름으로 붙잡아 부른다. 새 기능을 넣을 때 이 순서를 확인하고, 같은 우선순위에 층을 추가하지 않는다.

## `r13_present` (16층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:356` | r13_discovery_base_present |
| 2 | 61 | `room13_discovery.rpy:38` | r13_tool_base_present |
| 3 | 73 | `room13_tool_discovery.rpy:81` | _r13_mystery_present |
| 4 | 76 | `room13_first_mystery.rpy:98` | _r13_life_present |
| 5 | 94 | `systems/room13_first_day_flow.rpy:54` | _r13_work_present |
| 6 | 96 | `systems/room13_work_clues.rpy:25` | _r13_intro_present |
| 7 | 97 | `systems/room13_intro_clues.rpy:48` | _r13_poc_present |
| 8 | 100 | `systems/room13_poc_route.rpy:66` | _r13_daram_home_present |
| 9 | 101 | `systems/room13_daram_home.rpy:144` | _r13_pf_present |
| 10 | 113 | `systems/room13_present_flow.rpy:43` | _r13_mem_present |
| 11 | 114 | `systems/room13_memory.rpy:85` | _r13_ledger_present |
| 12 | 115 | `systems/room13_ledger.rpy:38` | _r13_tm_present |
| 13 | 116 | `systems/room13_testimony.rpy:48` | _r13_ob_present |
| 14 | 118 | `systems/room13_owl_buri.rpy:41` | _r13_uk_present |
| 15 | 123 | `systems/room13_use_knowledge.rpy:58` | _r13_sound_present |
| 16 | 150 | `systems/room13_sound.rpy:161` |  |

## `r13_topics` (14층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:160` | r13_tool_base_topics |
| 2 | 73 | `room13_tool_discovery.rpy:75` | _r13_home_topics |
| 3 | 79 | `room13_home.rpy:19` | _r13_life_topics |
| 4 | 92 | `systems/room13_livelihood_flow.rpy:35` | _r13_life_snack_topics |
| 5 | 93 | `systems/room13_livelihood_flow.rpy:104` | _r13_shop_topics |
| 6 | 94 | `systems/room13_shop.rpy:50` | _r13_firstday_topics |
| 7 | 95 | `systems/room13_first_day_flow.rpy:110` | _r13_items_topics |
| 8 | 96 | `systems/room13_items.rpy:112` | _r13_intro_topics |
| 9 | 97 | `systems/room13_intro_clues.rpy:112` | _r13_poc_topics |
| 10 | 100 | `systems/room13_poc_route.rpy:60` | _r13_daram_home_topics |
| 11 | 101 | `systems/room13_daram_home.rpy:97` | _r13_pf_topics |
| 12 | 113 | `systems/room13_present_flow.rpy:38` | _r13_night_topics |
| 13 | 117 | `systems/room13_night_talk.rpy:33` | _r13_uk_topics |
| 14 | 123 | `systems/room13_use_knowledge.rpy:53` |  |

## `r13_object_visible` (9층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 57 | `room13_life.rpy:182` | _r13_before_inspection_visible |
| 2 | 66 | `room13_inspection.rpy:253` | r13_before_gate_bundle_visible |
| 3 | 67 | `room13_gate_inspection.rpy:65` | _r13_route_object_visible |
| 4 | 90 | `room13_route_knowledge.rpy:22` | _r13_firstday_visible |
| 5 | 94 | `systems/room13_first_day_flow.rpy:15` | _r13_items_visible |
| 6 | 96 | `systems/room13_items.rpy:105` | _r13_ledger_visible |
| 7 | 115 | `systems/room13_ledger.rpy:26` | _r13_inn_visible |
| 8 | 120 | `systems/room13_inn_change.rpy:28` | _r13_note_spot_visible |
| 9 | 129 | `systems/room13_mother_note_spot.rpy:11` |  |

## `r13_conversation_topic_lines` (7층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 75 | `room13_dialogue_openings_20261013.rpy:238` | _r13_mystery_topic_lines |
| 2 | 76 | `room13_first_mystery.rpy:84` | r13_tool_base_topic_lines |
| 3 | 77 | `room13_tool_discovery.rpy:183` | _r13_firstday_topic_lines |
| 4 | 95 | `systems/room13_first_day_flow.rpy:101` | _r13_intro_topic_lines |
| 5 | 97 | `systems/room13_intro_clues.rpy:90` | _r13_daram_home_topic_lines |
| 6 | 101 | `systems/room13_daram_home.rpy:105` | _r13_mem_topic_lines |
| 7 | 114 | `systems/room13_memory.rpy:74` |  |

## `r13_compare_result` (6층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 78 | `room13_record_compare.rpy:8` | _r13_work_compare |
| 2 | 96 | `systems/room13_work_clues.rpy:18` | _r13_intro_compare |
| 3 | 97 | `systems/room13_intro_clues.rpy:35` | _r13_poc_compare |
| 4 | 100 | `systems/room13_poc_route.rpy:90` | _r13_daram_home_compare |
| 5 | 101 | `systems/room13_daram_home.rpy:133` | _r13_tm_compare |
| 6 | 116 | `systems/room13_testimony.rpy:42` |  |

## `r13_first_mystery_notes` (6층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 76 | `room13_first_mystery.rpy:26` | _r13_firstday_notes |
| 2 | 94 | `systems/room13_first_day_flow.rpy:46` | _r13_intro_notes |
| 3 | 97 | `systems/room13_intro_clues.rpy:119` | _r13_learning_mystery_notes |
| 4 | 98 | `systems/room13_learning.rpy:116` | _r13_poc_notes |
| 5 | 100 | `systems/room13_poc_route.rpy:138` | _r13_tn_notes |
| 6 | 121 | `systems/room13_trial_notes.rpy:48` |  |

## `r13_finish_topic` (5층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:169` | _r13_life_finish_topic |
| 2 | 93 | `systems/room13_livelihood_flow.rpy:108` | _r13_shop_finish_topic |
| 3 | 94 | `systems/room13_shop.rpy:61` | _r13_items_finish_topic |
| 4 | 96 | `systems/room13_items.rpy:123` | _r13_daram_home_finish |
| 5 | 101 | `systems/room13_daram_home.rpy:116` |  |

## `r13_where` (5층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:221` | _r13_before_gate_where |
| 2 | 67 | `room13_gate_continuity.rpy:9` | _r13_home_where |
| 3 | 79 | `room13_home.rpy:10` | _r13_life_where |
| 4 | 93 | `systems/room13_livelihood_flow.rpy:97` | _r13_episode_where |
| 5 | 103 | `systems/room13_episodes.rpy:55` |  |

## `r13_intro_goal` (4층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 97 | `systems/room13_intro_clues.rpy:94` | _r13_poc_intro_goal |
| 2 | 100 | `systems/room13_poc_route.rpy:124` | _r13_daram_room_intro_goal |
| 3 | 101 | `systems/room13_daram_home.rpy:124` | _r13_note_spot_goal |
| 4 | 129 | `systems/room13_mother_note_spot.rpy:18` |  |

## `r13_available` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:150` | r13_conversation_base_available |
| 2 | 70 | `room13_conversations.rpy:216` | _r13_route_available |
| 3 | 90 | `room13_route_knowledge.rpy:16` |  |

## `r13_finish_action` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:189` | _r13_mystery_finish_action |
| 2 | 76 | `room13_first_mystery.rpy:92` | _r13_items_finish_action |
| 3 | 96 | `systems/room13_items.rpy:140` |  |

## `r13_new` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:69` | _r13_life_new |
| 2 | 94 | `systems/room13_first_day_flow.rpy:4` | _r13_fresh_new |
| 3 | 105 | `systems/room13_no_carryover.rpy:6` |  |

## `r13_places` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:211` | _r13_route_places |
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
| 2 | 101 | `systems/room13_daram_home.rpy:112` |  |

## `r13_campaign_goal` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:501` | _r13_poc_campaign_goal |
| 2 | 100 | `systems/room13_poc_route.rpy:126` |  |

## `r13_click_feedback` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 69 | `room13_feedback.rpy:8` | _r13_sound_click_feedback |
| 2 | 150 | `systems/room13_sound.rpy:197` |  |

## `r13_debate_judge` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:407` | _r13_sound_debate_judge |
| 2 | 150 | `systems/room13_sound.rpy:168` |  |

## `r13_ending_notes` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 56 | `room13_week2_rules.rpy:270` | _r13_w2e_notes |
| 2 | 109 | `systems/room13_week2_events.rpy:42` |  |

## `r13_evidence_acquired` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 69 | `room13_feedback.rpy:3` | _r13_sound_evidence_acquired |
| 2 | 150 | `systems/room13_sound.rpy:183` |  |

## `r13_grant` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:103` | _r13_grant_now |
| 2 | 125 | `systems/room13_grant_timing.rpy:10` |  |

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
| 2 | 150 | `systems/room13_sound.rpy:203` |  |

## `r13_life_tool_name` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 126 | `systems/room13_life_closeups.rpy:23` | _r13_gm_tool_name |
| 2 | 127 | `systems/room13_gimmicks.rpy:45` |  |

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
| 2 | 66 | `room13_inspection.rpy:257` |  |

## `r13_record_entries` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 68 | `room13_notebook.rpy:20` | _r13_learning_record_entries |
| 2 | 98 | `systems/room13_learning.rpy:108` |  |

## `r13_secret_route_available` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 90 | `room13_route_knowledge.rpy:4` | _r13_items_route |
| 2 | 96 | `systems/room13_items.rpy:101` |  |

## `r13_shop_price` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 91 | `systems/room13_livelihood_model.rpy:30` | _r13_b3_shop_price |
| 2 | 107 | `systems/room13_bundle3.rpy:50` |  |

## `r13_stage_people` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 59 | `room13_acting.rpy:303` | _r13_daram_home_stage |
| 2 | 101 | `systems/room13_daram_home.rpy:30` |  |

## `r13_visible_people` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 59 | `room13_acting.rpy:278` | _r13_entry_visible_people |
| 2 | 62 | `room13_entry_window.rpy:10` |  |

## `r13_w2_action_done` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 56 | `room13_week2_rules.rpy:175` | _r13_w1c_action_done |
| 2 | 110 | `systems/room13_week1_cases.rpy:50` |  |

## `r13_w2_present` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 56 | `room13_week2_rules.rpy:192` | _r13_pf_w2_present |
| 2 | 113 | `systems/room13_present_flow.rpy:69` |  |

