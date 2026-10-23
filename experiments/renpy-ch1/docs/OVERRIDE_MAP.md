# 함수 덮어쓰기 지도 (자동 생성: dev/override_map.py --write)

Ren'Py는 init 우선순위 → 파일 경로 → 줄 순서로 실행한다. 아래 표는 그 순서대로이며, 마지막 줄이 게임이 실제로 부르는 바깥 층이다.
각 층은 바로 위 층을 `captured_as` 이름으로 붙잡아 부른다. 새 기능을 넣을 때 이 순서를 확인하고, 같은 우선순위에 층을 추가하지 않는다.

## `r13_topics` (24층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:160` | r13_tool_base_topics |
| 2 | 73 | `room13_tool_discovery.rpy:75` | _r13_home_topics |
| 3 | 79 | `room13_home.rpy:19` | _r13_life_topics |
| 4 | 92 | `systems/room13_livelihood_flow.rpy:35` | _r13_life_snack_topics |
| 5 | 93 | `systems/room13_livelihood_flow.rpy:114` | _r13_shop_topics |
| 6 | 94 | `systems/room13_shop.rpy:50` | _r13_firstday_topics |
| 7 | 95 | `systems/room13_first_day_flow.rpy:116` | _r13_items_topics |
| 8 | 96 | `systems/room13_items.rpy:112` | _r13_intro_topics |
| 9 | 97 | `systems/room13_intro_clues.rpy:113` | _r13_poc_topics |
| 10 | 100 | `systems/room13_poc_route.rpy:62` | _r13_daram_home_topics |
| 11 | 101 | `systems/room13_daram_home.rpy:108` | _r13_pf_topics |
| 12 | 113 | `systems/room13_present_flow.rpy:38` | _r13_night_topics |
| 13 | 117 | `systems/room13_night_talk.rpy:33` | _r13_uk_topics |
| 14 | 123 | `systems/room13_use_knowledge.rpy:53` | _r13_new_places_topics |
| 15 | 130 | `systems/room13_new_places.rpy:167` | _r13_direct_work_topics |
| 16 | 133 | `systems/room13_direct_work.rpy:14` | _r13_alibi_topics |
| 17 | 147 | `systems/room13_alibi.rpy:139` | _r13_catalog_topics |
| 18 | 148 | `systems/room13_materials.rpy:72` | _r13_e1_topics |
| 19 | 152 | `systems/room13_ep1_lamp_thief.rpy:55` | _r13_nolive_topics |
| 20 | 168 | `systems/room13_no_livelihood.rpy:10` | _r13_discovered_topics |
| 21 | 190 | `systems/room13_question_discovery.rpy:165` | _r13_qa_topics |
| 22 | 191 | `systems/room13_q1_arguments.rpy:55` | _r13_piko_topics |
| 23 | 205 | `systems/room13_piko_causality.rpy:109` | _r13_sling_confidence_topics |
| 24 | 206 | `systems/room13_sling_confidence.rpy:65` |  |

## `r13_present` (22층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:379` | r13_discovery_base_present |
| 2 | 61 | `room13_discovery.rpy:38` | r13_tool_base_present |
| 3 | 73 | `room13_tool_discovery.rpy:81` | _r13_mystery_present |
| 4 | 76 | `room13_first_mystery.rpy:98` | _r13_life_present |
| 5 | 94 | `systems/room13_first_day_flow.rpy:54` | _r13_work_present |
| 6 | 96 | `systems/room13_work_clues.rpy:25` | _r13_intro_present |
| 7 | 97 | `systems/room13_intro_clues.rpy:49` | _r13_poc_present |
| 8 | 100 | `systems/room13_poc_route.rpy:68` | _r13_daram_home_present |
| 9 | 101 | `systems/room13_daram_home.rpy:155` | _r13_pf_present |
| 10 | 113 | `systems/room13_present_flow.rpy:43` | _r13_mem_present |
| 11 | 114 | `systems/room13_memory.rpy:94` | _r13_ledger_present |
| 12 | 115 | `systems/room13_ledger.rpy:38` | _r13_tm_present |
| 13 | 116 | `systems/room13_testimony.rpy:48` | _r13_ob_present |
| 14 | 118 | `systems/room13_owl_buri.rpy:41` | _r13_uk_present |
| 15 | 123 | `systems/room13_use_knowledge.rpy:58` | _r13_sound_present |
| 16 | 150 | `systems/room13_sound.rpy:168` | _r13_e1_present |
| 17 | 152 | `systems/room13_ep1_lamp_thief.rpy:64` | _r13_wf_present |
| 18 | 154 | `systems/room13_ep3_woodfire.rpy:53` | _r13_nt_present |
| 19 | 155 | `systems/room13_ep4_night13.rpy:44` | _r13_review_present |
| 20 | 173 | `systems/room13_review_knowledge.rpy:29` | _r13_qa_present |
| 21 | 191 | `systems/room13_q1_arguments.rpy:61` | _r13_sling_confidence_present |
| 22 | 206 | `systems/room13_sling_confidence.rpy:74` |  |

## `r13_stage_people` (14층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 59 | `room13_acting.rpy:334` | _r13_daram_home_stage |
| 2 | 101 | `systems/room13_daram_home.rpy:35` | _r13_offer_stage |
| 3 | 124 | `systems/room13_event_offers.rpy:60` | _r13_ma_stage |
| 4 | 125 | `systems/room13_map_actions.rpy:38` | _r13_perspective_stage |
| 5 | 126 | `systems/room13_perspective.rpy:32` | _r13_map9_stage |
| 6 | 176 | `systems/room13_map_work_nine.rpy:17` | _r13_map27_stage |
| 7 | 178 | `systems/room13_map_action27.rpy:51` | _r13_contact_stage |
| 8 | 179 | `systems/room13_spatial_contacts.rpy:38` | _r13_balance_stage |
| 9 | 180 | `systems/room13_investigation_balance.rpy:43` | _r13_life_groups_stage |
| 10 | 181 | `systems/room13_life_groups.rpy:73` | _r13_story_pose_stage |
| 11 | 182 | `systems/room13_story_pose.rpy:27` | _r13_v111_stage_people |
| 12 | 301 | `room13_v111.rpy:141` | _r13_order_stage_people |
| 13 | 336 | `room13_v111_field_layout.rpy:46` | _r13_clear_stage_people |
| 14 | 337 | `room13_v111_field_layout.rpy:131` |  |

## `r13_object_visible` (11층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 57 | `room13_life.rpy:188` | _r13_before_inspection_visible |
| 2 | 66 | `room13_inspection.rpy:290` | r13_before_gate_bundle_visible |
| 3 | 67 | `room13_gate_inspection.rpy:65` | _r13_route_object_visible |
| 4 | 90 | `room13_route_knowledge.rpy:22` | _r13_firstday_visible |
| 5 | 94 | `systems/room13_first_day_flow.rpy:15` | _r13_items_visible |
| 6 | 96 | `systems/room13_items.rpy:105` | _r13_ledger_visible |
| 7 | 115 | `systems/room13_ledger.rpy:26` | _r13_inn_visible |
| 8 | 120 | `systems/room13_inn_change.rpy:28` | _r13_note_spot_visible |
| 9 | 129 | `systems/room13_mother_note_spot.rpy:19` | _r13_new_places_visible |
| 10 | 130 | `systems/room13_new_places.rpy:51` | _r13_v111_object_visible |
| 11 | 301 | `room13_v111.rpy:175` |  |

## `r13_conversation_topic_lines` (10층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 75 | `room13_dialogue_openings_20261013.rpy:248` | _r13_mystery_topic_lines |
| 2 | 76 | `room13_first_mystery.rpy:84` | r13_tool_base_topic_lines |
| 3 | 77 | `room13_tool_discovery.rpy:183` | _r13_firstday_topic_lines |
| 4 | 95 | `systems/room13_first_day_flow.rpy:107` | _r13_intro_topic_lines |
| 5 | 97 | `systems/room13_intro_clues.rpy:91` | _r13_daram_home_topic_lines |
| 6 | 101 | `systems/room13_daram_home.rpy:116` | _r13_mem_topic_lines |
| 7 | 114 | `systems/room13_memory.rpy:83` | _r13_expand_topic_lines |
| 8 | 140 | `systems/room13_dialogue_expand.rpy:19` | _r13_review_topic_lines |
| 9 | 173 | `systems/room13_review_knowledge.rpy:144` | _r13_question_topic_lines |
| 10 | 190 | `systems/room13_question_discovery.rpy:186` |  |

## `r13_where` (10층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:227` | _r13_before_gate_where |
| 2 | 67 | `room13_gate_continuity.rpy:9` | _r13_home_where |
| 3 | 79 | `room13_home.rpy:10` | _r13_life_where |
| 4 | 93 | `systems/room13_livelihood_flow.rpy:107` | _r13_episode_where |
| 5 | 103 | `systems/room13_episodes.rpy:55` | _r13_alibi_where |
| 6 | 147 | `systems/room13_alibi.rpy:30` | _r13_kd_where |
| 7 | 153 | `systems/room13_ep2_kids.rpy:92` | _r13_nt_where |
| 8 | 155 | `systems/room13_ep4_night13.rpy:34` | _r13_continuity_where |
| 9 | 162 | `systems/room13_story_continuity.rpy:19` | _r13_relocate_where |
| 10 | 336 | `room13_v111_field_layout.rpy:104` |  |

## `r13_first_mystery_notes` (9층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 76 | `room13_first_mystery.rpy:26` | _r13_firstday_notes |
| 2 | 94 | `systems/room13_first_day_flow.rpy:46` | _r13_intro_notes |
| 3 | 97 | `systems/room13_intro_clues.rpy:120` | _r13_learning_mystery_notes |
| 4 | 98 | `systems/room13_learning.rpy:115` | _r13_poc_notes |
| 5 | 100 | `systems/room13_poc_route.rpy:140` | _r13_tn_notes |
| 6 | 121 | `systems/room13_trial_notes.rpy:48` | _r13_alibi_notes |
| 7 | 147 | `systems/room13_alibi.rpy:157` | _r13_review_notes |
| 8 | 173 | `systems/room13_review_knowledge.rpy:90` | _r13_q1_notes |
| 9 | 181 | `systems/room13_q1_review.rpy:49` |  |

## `r13_compare_result` (6층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 78 | `room13_record_compare.rpy:8` | _r13_work_compare |
| 2 | 96 | `systems/room13_work_clues.rpy:18` | _r13_intro_compare |
| 3 | 97 | `systems/room13_intro_clues.rpy:36` | _r13_poc_compare |
| 4 | 100 | `systems/room13_poc_route.rpy:90` | _r13_daram_home_compare |
| 5 | 101 | `systems/room13_daram_home.rpy:144` | _r13_tm_compare |
| 6 | 116 | `systems/room13_testimony.rpy:42` |  |

## `r13_places` (6층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:215` | _r13_route_places |
| 2 | 90 | `room13_route_knowledge.rpy:28` | _r13_firstday_places |
| 3 | 94 | `systems/room13_first_day_flow.rpy:19` | _r13_new_places |
| 4 | 130 | `systems/room13_new_places.rpy:18` | _r13_ws_places |
| 5 | 156 | `systems/room13_ep5_soup.rpy:39` | _r13_v111_places |
| 6 | 301 | `room13_v111.rpy:198` |  |

## `r13_finish_topic` (5층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:169` | _r13_life_finish_topic |
| 2 | 93 | `systems/room13_livelihood_flow.rpy:118` | _r13_shop_finish_topic |
| 3 | 94 | `systems/room13_shop.rpy:61` | _r13_items_finish_topic |
| 4 | 96 | `systems/room13_items.rpy:123` | _r13_daram_home_finish |
| 5 | 101 | `systems/room13_daram_home.rpy:127` |  |

## `r13_intro_goal` (5층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 97 | `systems/room13_intro_clues.rpy:95` | _r13_poc_intro_goal |
| 2 | 100 | `systems/room13_poc_route.rpy:126` | _r13_daram_room_intro_goal |
| 3 | 101 | `systems/room13_daram_home.rpy:135` | _r13_note_spot_goal |
| 4 | 129 | `systems/room13_mother_note_spot.rpy:29` | _r13_review_intro_goal |
| 5 | 173 | `systems/room13_review_knowledge.rpy:119` |  |

## `r13_v111_idle_lines` (5층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 336 | `room13_v111_idle.rpy:51` | _r13_met_idle_lines |
| 2 | 346 | `room13_v111_idle.rpy:85` | _r13_state_idle_lines |
| 3 | 348 | `room13_v111_idle.rpy:143` | _r13_guard_idle_lines |
| 4 | 349 | `room13_v111_idle.rpy:163` | _r13_scene_idle_lines |
| 5 | 351 | `room13_v111_idle.rpy:194` |  |

## `r13_calendar_topic_seen` (4층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 75 | `room13_dialogue_openings_20261013.rpy:275` | _r13_daram_home_seen |
| 2 | 101 | `systems/room13_daram_home.rpy:123` | _r13_current_topic_seen |
| 3 | 130 | `systems/room13_topic_record.rpy:26` | _r13_piko_topic_seen |
| 4 | 205 | `systems/room13_piko_causality.rpy:103` |  |

## `r13_campaign_goal` (4층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:561` | _r13_poc_campaign_goal |
| 2 | 100 | `systems/room13_poc_route.rpy:128` | _r13_time_campaign_goal |
| 3 | 169 | `systems/room13_time_flow.rpy:32` | _r13_v111_campaign_goal |
| 4 | 340 | `systems/room13_v111_goal.rpy:6` |  |

## `r13_debate_judge` (4층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:441` | _r13_sound_debate_judge |
| 2 | 150 | `systems/room13_sound.rpy:180` | _r13_qa_judge |
| 3 | 191 | `systems/room13_q1_arguments.rpy:161` | _r13_qh_judge |
| 4 | 192 | `systems/room13_q1_difficulty.rpy:188` |  |

## `r13_debate_seats` (4층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:581` | _r13_e1_seats |
| 2 | 152 | `systems/room13_ep1_lamp_thief.rpy:168` | _r13_continuity_seats |
| 3 | 162 | `systems/room13_story_continuity.rpy:59` | _r13_qa_seats |
| 4 | 191 | `systems/room13_q1_arguments.rpy:198` |  |

## `r13_next_day` (4층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:144` | _r13_life_next_day |
| 2 | 92 | `systems/room13_livelihood_flow.rpy:11` | _r13_conv_next_day |
| 3 | 165 | `systems/room13_convenience.rpy:12` | _r13_nolive_next_day |
| 4 | 168 | `systems/room13_no_livelihood.rpy:27` |  |

## `r13_person_action` (4층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 124 | `systems/room13_event_offers.rpy:50` | _r13_life_groups_person_action |
| 2 | 181 | `systems/room13_life_groups.rpy:103` | _r13_question_person_action |
| 3 | 190 | `systems/room13_question_discovery.rpy:288` | _r13_v111_person_action |
| 4 | 301 | `room13_v111.rpy:145` |  |

## `r13_visible_people` (4층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 59 | `room13_acting.rpy:302` | _r13_entry_visible_people |
| 2 | 62 | `room13_entry_window.rpy:10` | _r13_v111_visible_people |
| 3 | 301 | `room13_v111.rpy:119` | _r13_order_visible_people |
| 4 | 336 | `room13_v111_field_layout.rpy:25` |  |

## `r13_activity_text` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 57 | `room13_life.rpy:174` | _r13_reason_activity |
| 2 | 146 | `systems/room13_place_reasons.rpy:128` | _r13_alibi_activity |
| 3 | 147 | `systems/room13_alibi.rpy:37` |  |

## `r13_available` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:150` | r13_conversation_base_available |
| 2 | 70 | `room13_conversations.rpy:216` | _r13_route_available |
| 3 | 90 | `room13_route_knowledge.rpy:16` |  |

## `r13_bed_available` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 61 | `room13_interaction.rpy:94` | _r13_firstday_bed |
| 2 | 94 | `systems/room13_first_day_flow.rpy:31` | _r13_v111_bed |
| 3 | 301 | `room13_v111.rpy:202` |  |

## `r13_catalog_record` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 148 | `systems/room13_materials.rpy:40` | _r13_v111_catalog_record |
| 2 | 306 | `room13_v111.rpy:434` | _r13_nw_rules_catalog_record |
| 3 | 318 | `room13_v111_newworld_rules.rpy:14` |  |

## `r13_conversation_opening` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 75 | `room13_dialogue_openings_20261013.rpy:177` | _r13_review_opening |
| 2 | 173 | `systems/room13_review_knowledge.rpy:135` | _r13_q1_opening |
| 3 | 181 | `systems/room13_q1_review.rpy:141` |  |

## `r13_debate_required` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:426` | _r13_qa_required |
| 2 | 191 | `systems/room13_q1_arguments.rpy:153` | _r13_qh_required |
| 3 | 192 | `systems/room13_q1_difficulty.rpy:194` |  |

## `r13_debate_session` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:373` | _r13_e1_session |
| 2 | 152 | `systems/room13_ep1_lamp_thief.rpy:162` | _r13_nw_debate_session |
| 3 | 321 | `room13_v111_meeting_stage.rpy:97` |  |

## `r13_debate_statements` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:388` | _r13_qa_statements |
| 2 | 191 | `systems/room13_q1_arguments.rpy:145` | _r13_qh_statements |
| 3 | 192 | `systems/room13_q1_difficulty.rpy:173` |  |

## `r13_ep_line_art` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 160 | `systems/room13_ep_art.rpy:128` | _r13_impact_line_art |
| 2 | 345 | `systems/room13_impact_fx.rpy:65` | _r13_met_line_art |
| 3 | 346 | `room13_v111_idle.rpy:70` |  |

## `r13_finish_action` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:193` | _r13_mystery_finish_action |
| 2 | 76 | `room13_first_mystery.rpy:92` | _r13_items_finish_action |
| 3 | 96 | `systems/room13_items.rpy:140` |  |

## `r13_flag` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:94` | _r13_rel_flag |
| 2 | 166 | `systems/room13_relations.rpy:20` | _r13_shelf_flag |
| 3 | 170 | `systems/room13_shelf.rpy:28` |  |

## `r13_line_performance` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 59 | `room13_acting.rpy:93` | _r13_mood_line_performance |
| 2 | 141 | `systems/room13_daram_mood.rpy:28` | _r13_carriage_line_performance |
| 3 | 306 | `room13_carriage_direction.rpy:88` |  |

## `r13_meeting_cast` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 99 | `room13_meeting_seating.rpy:50` | _r13_e1_cast |
| 2 | 152 | `systems/room13_ep1_lamp_thief.rpy:185` | _r13_nw_meeting_cast |
| 3 | 321 | `room13_v111_meeting_stage.rpy:102` |  |

## `r13_meeting_plate` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 99 | `room13_meeting_seating.rpy:147` | _r13_e1_plate |
| 2 | 152 | `systems/room13_ep1_lamp_thief.rpy:179` | _r13_nw_meeting_plate |
| 3 | 321 | `room13_v111_meeting_stage.rpy:135` |  |

## `r13_new` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:69` | _r13_life_new |
| 2 | 94 | `systems/room13_first_day_flow.rpy:4` | _r13_fresh_new |
| 3 | 105 | `systems/room13_no_carryover.rpy:6` |  |

## `r13_object_name` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 61 | `room13_interaction.rpy:84` | _r13_before_inspection_name |
| 2 | 66 | `room13_inspection.rpy:294` | _r13_day2_object_name |
| 3 | 353 | `systems/room13_day2_guidance.rpy:40` |  |

## `r13_q1_notes` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 181 | `systems/room13_q1_review.rpy:21` | _r13_qa_notes |
| 2 | 191 | `systems/room13_q1_arguments.rpy:239` | _r13_piko_q1_notes |
| 3 | 205 | `systems/room13_piko_causality.rpy:42` |  |

## `r13_q1_summary` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 181 | `systems/room13_q1_review.rpy:57` | _r13_qa_summary |
| 2 | 191 | `systems/room13_q1_arguments.rpy:215` | _r13_qh_summary |
| 3 | 192 | `systems/room13_q1_difficulty.rpy:253` |  |

## `r13_sound_scene_music` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 150 | `systems/room13_sound.rpy:123` | _r13_contrast_scene_music |
| 2 | 163 | `systems/room13_scene_contrast.rpy:25` | _r13_v111_scene_music |
| 3 | 307 | `room13_v111.rpy:463` |  |

## `r13_speaker` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:299` | _r13_v111_speaker_base |
| 2 | 304 | `room13_v111.rpy:478` | _r13_carriage_speaker |
| 3 | 306 | `room13_carriage_direction.rpy:94` |  |

## `r13_v111_present_reaction` (3층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 335 | `room13_v111_reactions.rpy:59` | _r13_idle_present_reaction |
| 2 | 336 | `room13_v111_idle.rpy:42` | _r13_present_fallback |
| 3 | 347 | `room13_v111_idle.rpy:119` |  |

## `r13_background` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 57 | `room13_life.rpy:86` | _r13_ep_art_background |
| 2 | 160 | `systems/room13_ep_art.rpy:44` |  |

## `r13_before_line` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:346` | _r13_question_before_line |
| 2 | 190 | `systems/room13_question_discovery.rpy:171` |  |

## `r13_calendar_promises` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 68 | `room13_notebook.rpy:201` | _r13_review_promises |
| 2 | 173 | `systems/room13_review_knowledge.rpy:128` |  |

## `r13_click_feedback` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 69 | `room13_feedback.rpy:8` | _r13_sound_click_feedback |
| 2 | 150 | `systems/room13_sound.rpy:210` |  |

## `r13_contact_presentations` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 190 | `systems/room13_question_discovery.rpy:227` | _r13_qa_contact |
| 2 | 191 | `systems/room13_q1_arguments.rpy:29` |  |

## `r13_debate_answerable` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:496` | _r13_qa_answerable |
| 2 | 191 | `systems/room13_q1_arguments.rpy:179` |  |

## `r13_debate_engageable` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:509` | _r13_qa_engageable |
| 2 | 191 | `systems/room13_q1_arguments.rpy:186` |  |

## `r13_debate_hint_due` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:488` | _r13_qa_hints |
| 2 | 191 | `systems/room13_q1_arguments.rpy:190` |  |

## `r13_debate_partial_lines` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:528` | _r13_qa_partial |
| 2 | 191 | `systems/room13_q1_arguments.rpy:194` |  |

## `r13_debate_ready` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:429` | _r13_qa_ready |
| 2 | 191 | `systems/room13_q1_arguments.rpy:157` |  |

## `r13_debate_visible` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_debate.rpy:422` | _r13_qa_visible |
| 2 | 191 | `systems/room13_q1_arguments.rpy:149` |  |

## `r13_dialogue_beat_art` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 170 | `systems/room13_dialogue_beats.rpy:157` | _r13_context_beat_art |
| 2 | 172 | `systems/room13_dialogue_context_art.rpy:28` |  |

## `r13_dialogue_beat_begin` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 170 | `systems/room13_dialogue_beats.rpy:43` | _r13_context_beat_begin |
| 2 | 172 | `systems/room13_dialogue_context_art.rpy:14` |  |

## `r13_dialogue_context_match` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 172 | `systems/room13_dialogue_context_art.rpy:5` | _r13_nw_context_match |
| 2 | 319 | `room13_v111_newworld_text.rpy:321` |  |

## `r13_ending_notes` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 56 | `room13_week2_rules.rpy:272` | _r13_w2e_notes |
| 2 | 109 | `systems/room13_week2_events.rpy:42` |  |

## `r13_ep_background` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 160 | `systems/room13_ep_art.rpy:37` | _r13_v111_ruin_bg |
| 2 | 162 | `systems/room13_ep_art.rpy:194` |  |

## `r13_ep_cut_art` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 160 | `systems/room13_ep_art.rpy:105` | _r13_regular_ep_cut_art |
| 2 | 162 | `systems/room13_special_scenes.rpy:33` |  |

## `r13_evidence_acquired` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 69 | `room13_feedback.rpy:3` | _r13_sound_evidence_acquired |
| 2 | 150 | `systems/room13_sound.rpy:196` |  |

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

## `r13_intro_direction_lines` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 97 | `systems/room13_intro_clues.rpy:76` | _r13_review_direction |
| 2 | 173 | `systems/room13_review_knowledge.rpy:98` |  |

## `r13_learning_job_context` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_learning.rpy:77` | _r13_poc_job_context |
| 2 | 100 | `systems/room13_poc_route.rpy:131` |  |

## `r13_learning_sleep_text` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 98 | `systems/room13_learning.rpy:59` | _r13_conv_sleep_text |
| 2 | 165 | `systems/room13_convenience.rpy:24` |  |

## `r13_life_apply_purchase` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 92 | `systems/room13_livelihood_flow.rpy:3` | _r13_sound_apply_purchase |
| 2 | 150 | `systems/room13_sound.rpy:216` |  |

## `r13_life_tool_name` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 126 | `systems/room13_life_closeups.rpy:23` | _r13_gm_tool_name |
| 2 | 127 | `systems/room13_gimmicks.rpy:45` |  |

## `r13_living_pose` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 59 | `room13_acting.rpy:270` | _r13_solbang_living_pose |
| 2 | 177 | `systems/room13_solbang_chinchilla.rpy:4` |  |

## `r13_local_connections` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 60 | `room13_navigation.rpy:35` | _r13_firstday_connections |
| 2 | 94 | `systems/room13_first_day_flow.rpy:25` |  |

## `r13_material_art` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 150 | `systems/room13_material_art.rpy:8` | _r13_v111_material_art |
| 2 | 302 | `room13_v111.rpy:363` |  |

## `r13_meeting_direct_line` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 174 | `systems/room13_meeting_direction.rpy:170` | _r13_nw_meeting_direct_line |
| 2 | 321 | `room13_v111_meeting_stage.rpy:150` |  |

## `r13_meeting_focus_person` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 99 | `room13_meeting_seating.rpy:57` | _r13_nw_meeting_focus_person |
| 2 | 321 | `room13_v111_meeting_stage.rpy:108` |  |

## `r13_meeting_header` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 152 | `systems/room13_ep1_lamp_thief.rpy:102` | _r13_nw_meeting_header |
| 2 | 321 | `room13_v111_meeting_stage.rpy:143` |  |

## `r13_meeting_orbit_height` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 175 | `room13_meeting_camera.rpy:39` | _r13_nw_meeting_orbit_height |
| 2 | 321 | `room13_v111_meeting_stage.rpy:119` |  |

## `r13_meeting_portrait_x` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 175 | `room13_meeting_camera.rpy:42` | _r13_nw_meeting_portrait_x |
| 2 | 321 | `room13_v111_meeting_stage.rpy:126` |  |

## `r13_prove` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:456` | _r13_nolive_prove |
| 2 | 168 | `systems/room13_no_livelihood.rpy:49` |  |

## `r13_q1_node_open` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 191 | `systems/room13_q1_arguments.rpy:137` | _r13_qh_node_open |
| 2 | 192 | `systems/room13_q1_difficulty.rpy:177` |  |

## `r13_q1_press_done` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 191 | `systems/room13_q1_arguments.rpy:170` | _r13_qh_press |
| 2 | 192 | `systems/room13_q1_difficulty.rpy:199` |  |

## `r13_q1_removal_proved` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 191 | `systems/room13_q1_arguments.rpy:134` | _r13_qh_removal |
| 2 | 192 | `systems/room13_q1_difficulty.rpy:43` |  |

## `r13_q1_review_lines` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 181 | `systems/room13_q1_review.rpy:66` | _r13_qa_review_lines |
| 2 | 191 | `systems/room13_q1_arguments.rpy:231` |  |

## `r13_q1_review_rows` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 181 | `systems/room13_q1_review.rpy:52` | _r13_qa_review_rows |
| 2 | 191 | `systems/room13_q1_arguments.rpy:210` |  |

## `r13_record_entries` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 68 | `room13_notebook.rpy:65` | _r13_learning_record_entries |
| 2 | 98 | `systems/room13_learning.rpy:107` |  |

## `r13_rel_edges` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 166 | `systems/room13_relations.rpy:92` | _r13_nw_rel_edges |
| 2 | 330 | `systems/room13_v111_relations.rpy:88` |  |

## `r13_rel_status` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 166 | `systems/room13_relations.rpy:33` | _r13_nw_rel_status |
| 2 | 330 | `systems/room13_v111_relations.rpy:42` |  |

## `r13_remember_line` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 55 | `room13_rules.rpy:361` | _r13_question_remember_line |
| 2 | 190 | `systems/room13_question_discovery.rpy:176` |  |

## `r13_resident_where` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 57 | `room13_life.rpy:164` | _r13_new_places_resident_where |
| 2 | 130 | `systems/room13_new_places.rpy:105` |  |

## `r13_secret_route_available` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 90 | `room13_route_knowledge.rpy:4` | _r13_items_route |
| 2 | 96 | `systems/room13_items.rpy:101` |  |

## `r13_shop_price` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 91 | `systems/room13_livelihood_model.rpy:32` | _r13_b3_shop_price |
| 2 | 107 | `systems/room13_bundle3.rpy:50` |  |

## `r13_staged_visible_art` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 59 | `room13_acting.rpy:541` | _r13_map27_visible |
| 2 | 178 | `systems/room13_map_action27.rpy:87` |  |

## `r13_topic_current_context` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 130 | `systems/room13_topic_record.rpy:12` | _r13_piko_topic_context |
| 2 | 205 | `systems/room13_piko_causality.rpy:62` |  |

## `r13_topic_current_lines` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 130 | `systems/room13_topic_record.rpy:31` | _r13_piko_topic_lines |
| 2 | 205 | `systems/room13_piko_causality.rpy:97` |  |

## `r13_v111_arrive` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 311 | `room13_v111_later_bindings.rpy:69` | _r13_nw_arrive |
| 2 | 318 | `room13_v111_newworld_rules.rpy:189` |  |

## `r13_v111_binding` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 301 | `room13_v111.rpy:71` | _r13_nw_binding |
| 2 | 318 | `room13_v111_newworld_rules.rpy:195` |  |

## `r13_v111_goal` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 317 | `room13_v111_later_bindings.rpy:233` | _r13_step_goal |
| 2 | 341 | `systems/room13_v111_goal.rpy:22` |  |

## `r13_v111_line` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 301 | `room13_v111.rpy:57` | _r13_nw_authored_line |
| 2 | 319 | `room13_v111_newworld_text.rpy:273` |  |

## `r13_v111_questions` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 301 | `room13_v111.rpy:109` | _r13_reaction_questions |
| 2 | 335 | `room13_v111_reactions.rpy:81` |  |

## `r13_v111_set` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 301 | `room13_v111.rpy:12` | _r13_nw_rel_set |
| 2 | 330 | `systems/room13_v111_relations.rpy:18` |  |

## `r13_w2_action_done` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 56 | `room13_week2_rules.rpy:177` | _r13_w1c_action_done |
| 2 | 110 | `systems/room13_week1_cases.rpy:50` |  |

## `r13_w2_present` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 56 | `room13_week2_rules.rpy:194` | _r13_pf_w2_present |
| 2 | 113 | `systems/room13_present_flow.rpy:69` |  |

## `r13_world_background` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 58 | `room13_world_camera.rpy:68` | _r13_ep_art_world_background |
| 2 | 160 | `systems/room13_ep_art.rpy:86` |  |

## `r13_world_edge_label` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 58 | `room13_world_camera.rpy:187` | _r13_offer_edge_label |
| 2 | 124 | `systems/room13_event_offers.rpy:94` |  |

## `r13_world_props` (2층)

| 순서 | init | 위치 | 이전 층 이름 |
|---|---|---|---|
| 1 | 125 | `systems/room13_map_actions.rpy:80` | _r13_v111_props |
| 2 | 301 | `room13_v111.rpy:189` |  |

