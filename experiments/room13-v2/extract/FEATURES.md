# 새 판(v2)에 필요한 공통 기능 목록 — 추출 1단계

2026-10-30. 지금 게임(`experiments/renpy-ch1/game`)을 실행하지 않고 읽어서 정리했다.
「지금 그리는 곳」은 v111 흐름에서 실제로 부르는 화면(정적 추적: 시작에서 닿는 label 이 부르는 화면 + 그 화면이 `use` 하는 화면)과, 여러 층이 덮어쓴 함수의 **마지막 층**이다. 덮어쓰기 순서는 `docs/OVERRIDE_MAP.md`.
「소유자 결정」은 `/home/user/daaegame/CLAUDE.md` 「화면 결정」과 코드 주석에 날짜가 적힌 결정이다. 새 판은 이 결정을 처음부터 지키는 한 가지 구현만 두면 된다.

화면 정의 170개 중 v111 에서 닿는 것 107개(정적 추적, 함수가 띄우는 화면 일부는 빠질 수 있다 — 아래 표는 그것까지 손으로 보탰다).

---

## 1. 시작·메인 메뉴·오프닝

| 항목 | 지금 |
|---|---|
| 메인 메뉴 | `screens.rpy:58 main_menu` — 엽서 배경(`assets/ui-b-main/b_main_background_postcard.png`)·로고·출연진 포스터. 단추 넷: 이어하기·처음부터·불러오기·설정. 「음악 출처」(`r13_music_credits`), 판 번호. 등장 연출 `systems/room13_title_fx.rpy`. |
| 처음부터 | `label start` → `room13_start`(room13.rpy:103) → `r13_v111_start`. 옛 이야기 입구는 2026-10-27 지움. |
| 오프닝 | `room13_coach_cut.rpy r13_coach_travel_cut`: 검은 화면에 글 세 줄(R13_BLACK_CARD_LINES) + 마차 소리. 건너뛰기 중이면 생략. 옛 17초 컷씬(`systems/room13_opening.rpy`, ROOM13_GUIDE 에 남은 설명)은 지금 흐름에서 부르지 않는다. |
| 마차 장면 | `room13_carriage_direction.rpy`: 같은 마차 그림 위에 다람만 앉은 그림(`room13-carriage-daram-seat-*.webp`, 표정 8종)으로 바꿔 세운다. 마차 채널 소리 둘(바퀴·말발굽). |
| 웹 로딩창 | 메인화면과 같은 그림(소유자). 파일 `assets/room13-loading-scene.webp`, 도구 `dev/make_loading_scene.py`. 배경음은 첫 터치 뒤(안내 줄). |

## 2. 대화창

| 항목 | 지금 |
|---|---|
| 그리는 곳 | `screens.rpy:116 say` (+ `room13_speaker_display.rpy`, `room13_bdialogue_faces.rpy`, `systems/room13_dialogue_*`). 줄 재생은 `room13.rpy:39 label r13_lines`. |
| 형식 | B 대사판(`assets/ui-b-dialogue/b_panel_dialogue.png`)·이름 리본(`b_ribbon_name.png`)·표정 얼굴. 검은 카드 모드(오프닝)·회의 무대 모드가 같은 화면 안에 갈래로 있다. |
| 한 줄의 꾸러미 | `(인물 키, 글, {expression, pose, no_lead, thought, cut, fx, beat, endcut, line_id, show})`. 생각 줄은 괄호를 엔진이 붙인다(`r13_nw_added_line`). |
| 줄바꿈 | `systems/room13_linebreak.rpy`: 문장 끝마다, 한 줄 35자(큰 글씨 29자), 네 줄 이상이면 두 줄씩. 대사에 `\n` 을 직접 넣지 않는 것이 원칙이나 d01 등에 `\n` 이 남아 있다(추출 원문 그대로). |
| 연출 태그 | `{w=.3}` 등 대기 태그, `{image=…}`(1일 메모 도토리). 타자음 `assets/type.wav`. |
| 듣는 사람 세우기 | 아빠 줄이면 듣는 사람(`r13_dad_listener`), 지문이면 다음에 말할 사람을 미리 세운다. 생각 줄에서는 아무도 세우지 않는다(2026-10-27). 말하는 주민은 무대에 없으면 걸어 들어온다(`r13_v111_join`). |
| 표정·몸짓 | 표정이 바뀌면 스쿼시 한 번(`r13_body_*`), 눈 깜빡임(도트 연출). 숨쉬기 없음(0.18.44). |
| 소유자 결정 | B 대사판·이름 리본·표정 얼굴. 건너뛰기 확인창 없음. 다람은 어른의 약 2/3 높이. 인물 그림에 흰 테두리 스티커 없음. 아빠는 화면에 그리지 않는다. |
| 재생 도구 | `systems/room13_playback.rpy`: 백로그(`r13_backlog`), 더보기(`r13_more_tools` → `systems/room13_footer_concept.rpy r13_concept_more`), 자동·건너뛰기(읽은 것만/전부)·대화창 숨기기·설정. 아래 조작 줄 `systems/room13_night_ui.rpy r13_night_controls`. |

## 3. 조사 화면(현장)

| 항목 | 지금 |
|---|---|
| 그리는 곳 | `room13_screens.rpy:71 r13_hub` → `r13_world_contents`(인물·물건), `r13_resident_stage`. 위 단추 `systems/room13_field_views.rpy`(지도·기록·생각), 설정 톱니 `r13_options_control`. |
| 들어오는 곳 | `room13_v111.rpy label r13_v111_wait(key)` / `r13_v111_wait_again`. 대기 관문 묶음은 `v111/field-bindings.json`(149개, 제목은 dNN `titles` 로 덮임). 고르면 그 선택지의 index 를 돌려준다. |
| 인물 누르기 | 선택지·읽지 않은 후속 질문·아직 안 본 자료 반응이 있으면 질문 목록, 없으면 한가한 줄(`room13_v111_idle.rpy`, 5층: 2일 안내 → 긴장 장면 → 맡은 일 지문 → 첫 만남 인사 → 방금 대화 → 그날 첫 인사 → 아빠 속말 3종). 다람은 장면마다 처음 한 번 먼저 대답. |
| 물건 누르기 | 선택지가 가리키면 그 선택지(같은 물건에 둘 이상이면 「(이름, 어떻게 할까?)」 메뉴). 아니면 관찰 줄(`r13_v111_ambient_text` → `room13_thoughts.rpy r13_observe`): 아빠 속말 + 다람이 곁에 있으면 주고받기(R13_OBSERVATION_CHAT, 같은 때 네 번까지). 자료 물건은 가졌으면 그 설명문, 아니면 「지금은 먼저 할 일이 있다」류. |
| 보이는 인물 | `r13_visible_people`(5층, 바깥 층 `room13_v111_scene_elsewhere.rpy`): 대기 묶음 people + 옛 일과표 주민 − 죽은 사람·붙잡힌 사람·떠난 사람. 다람은 아빠 곁 동행이라 현장에 세우지 않는다(선택지가 다람을 가리킬 때만). |
| 보이는 물건 | `r13_object_visible`(11층, 마지막 `room13_v111.rpy:237`): 이 장소 선택지가 가리키거나 관찰 글이 있는 물건만. |
| 카메라 좌우 | 넓은 그림(1920·2160·2400px)을 1280 창으로 본다: `room13_world_camera.rpy r13_world_camera_controls`, 배치표 `assets/room13-world-layout.json`. 대기에 닿을 때 카메라를 그 대상 쪽으로(`systems/room13_camera_follow.rpy`, `r13_v111_context` 2층). 확대 장소는 아래 띠(0.20.3). |
| 시간대 그림 | period 0/1/2 → morning/afternoon/evening(`r13_daylight`). 13호·복도는 사건 전후(before/after) 그림. |
| 시각 | 경과 분(`r13_v111_time`: 물건 15분, 질문 10분, 이동 5분 등)과 날짜판(`r13_hud`: 날짜·요일·시간대·시계). 날은 잠자리 선택지로만 넘어간다. |
| 소유자 결정 | 지도·기록·생각은 상단, 장면 하단은 비운다. 인물이 기본이고 배경 물건은 직접 누른다. 돋보기 표식 없음. 현장 인물 도트는 1칸=1px(`field-dot-v2`). 빨간 테이프는 장소 이름표 한 곳만. 사람을 누르면 주고받기가 먼저(말 없이 지문만 흐르거나 자료가 저절로 생기면 안 된다). 선택지가 하나면 창을 띄우지 않는다(`screens.rpy choice` 가 .01초 뒤 자동 진행). 조사 화면 인물은 움직이지 않는다. |

## 4. 질문 목록

| 항목 | 지금 |
|---|---|
| 그리는 곳 | `room13_screens.rpy:247 r13_topics(person)` → `r13_question_list` / `systems/room13_side_questions.rpy`(쪽 넘김 목록). 메뉴 선택지도 같은 모양(`screens.rpy choice` → `r13_question_list`). |
| 목록 내용 | `r13_v111_questions`(2층: 묶음 선택지 중 이 사람·이 장소 것, present_only 제외 + reactions.json 후속 질문, 안 들은 것엔 빨간 「새」). 읽은 질문 표시(remember_read). |
| 이어 묻기 | 한 질문이 끝나면 같은 사람의 목록이 다시 열린다(0.20.6, `r13_v111_talk_person`). 「돌아가기」로 빠진다. |
| 소유자 결정 | 인물 왼쪽·질문지 오른쪽. 긴 목록은 명시적 쪽 넘김(숨은 스크롤 없음). 하단 4버튼은 같은 크기·같은 아이콘 계열. **질문 목록은 그 사람에게 하는 말만**(「힌트를 생각한다」「자료를 함께 제시한다」 같은 조작은 질문이 아니다, 2026-10-27). 선택지 문구 24자 이하. |
| 옛 층 | `r13_topics` 함수 24층(옛 판 주제·직업·상점·알리바이 등)은 v111 에서 `r13_v111_questions` 가 대신한다. 새 판에서는 v111 층만 옮기면 된다. |

## 5. 자료 제시

| 항목 | 지금 |
|---|---|
| 그리는 곳 | 질문 화면의 「자료 제시」 → `room13_screens.rpy:300 r13_book(person,present=True)` (수첩 틀 `systems/room13_notebook_shell.rpy`, 자료 목록 `systems/room13_evidence_view.rpy`). |
| 판정 | `r13_v111_present_index`: 이 사람·이 장소의 `present` 선택지와 같은 자료면 그 선택지로 간다. 아니면 반응: reactions.json `present`(사람×자료×날짜, after_meeting 조건) → generic(사람별 고정 답) → 다람이면 다람 답 → 그 밖에는 아빠 속말. |
| 소유자 결정 | 자료를 대신 내미는 대화 주제를 만들지 않는다 — 자료는 직접 제시. 「초대 편지를 보여 준다」처럼 내미는 일뿐인 선택지는 질문 목록에 두지 않고(present_only) 제시로만 한다(2026-10-29). |
| 옛 층 | `r13_present` 함수 22층은 v111 에서 쓰지 않는다(v111 은 위 경로). |

## 6. 회의(증명 화면)

| 항목 | 지금 |
|---|---|
| 흐름 | `room13_v111.rpy label r13_v111_proof(key,correct,success,wrong,hint,review_return)` → `r13_v111_proof_again`/`_pick`. |
| 화면 둘 | ① 통합 화면 `systems/room13_proof_workspace.rpy r13_proof_workspace` — 시범 쟁점 셋(1일 입구, 1일 두 편지(비교 모드), 7일 불 첫 추궁)만. 왼쪽 실제 발언, 가운데 보유 자료 체크(획득 최신순), 오른쪽 상세, 아래 고른 칩·「근거 제시」. 두 편지는 나란히 보기·구역 짚기(`r13_pw_pair`). ② 그 밖 쟁점: `room13_week2_screens.rpy:126 r13_crisis_proof` + 자료 고르기 책 `r13_book(purpose=proof/compare)`. |
| 판정 | 정답 세트 하나를 다 갖추고 나머지가 다른 세트·덧붙임뿐이면 이김(`r13_v111_proof_accepts`). 대체 정답 `R13_PROOF_ALTERNATES`, 덧붙임 `R13_PROOF_EXTRAS`, 보이는 제목 `R13_PROOF_TITLES`. 틀리면 맞는 쪽 자료만 남김(`r13_v111_proof_kept`, 전부 내기 방지). 빈 제출·읽기·체크는 기회를 안 쓴다. |
| 기회 | 회의마다 함께 쓰는 수 `R13_NW_TRIES_BY_MEETING`(gate 3→무제한, gate_post 3, fire·records·blanket·piko 4, soup 5, altar 6, lamp·room13 7, hypothesis 13). 마지막 기회의 오답이 결과가 된다. 칩 「회의 기회 n / m · 이번이 마지막」. |
| 틀린 뒤 | 상대 반박(일부 정답이면 빈 고리만 묻는 반박 묶음 half_*) → 아빠 속말(`R13_NW_WRONG_THOUGHTS` 1·2·3번째, 탐색 안내, 「다 있었다」). 자료 이름·정답은 말하지 않는다. |
| 되묻기·조사 계속 | press → 힌트 label 또는 `R13_PROOF_RANGE` 한 줄. investigate → 그 현장 대기로 돌아감(기회 불변). |
| 회의 다시 하기 | 첫 쟁점 직전 체크포인트(`room13_meeting_retry_logic.rpy`), 기회를 다 쓰면 `room13_meeting_retry_ui.rpy r13_meeting_retry_choice`(자료는 남기고 회의 상태만 되돌림). |
| 회의 무대 | label 콜백 `room13_v111_meeting_stage.rpy`: 회의 label 의 대사는 무대(근접 한 사람, `room13_meeting_seating.rpy r13_meeting_stage`, 머리띠 쟁점 문장)로. 현장 물건 읽기(`r13_field_reading`)는 무대를 깔지 않는다. |
| 선택지 쟁점 | 3일 칼(trial_knife), 11일 가설 hyp0~hyp5 는 증명 화면이 아니라 메뉴로 묻는 쟁점(`menu:` 키). |
| 대승리 | 7일 불(배급표), 12일 수프(돌아온 그릇) — 덧붙인 보너스 자료로 이기면 grand:*. 표시는 없다. |
| 소유자 결정 | 회의는 근접 한 사람 모드(`R13_MEETING_SOLO`), 머리띠는 V2 글자 단계. 기본 증거만으로 언제나 이길 수 있다. 회의 중 아빠의 생각은 보이되 추리를 미리 하지 않는다. 1일 입구는 회의가 아니라 기회를 세지 않는다(2026-10-27). |

## 7. 지도

| 항목 | 지금 |
|---|---|
| 그리는 곳 | `room13_navigation.rpy:135 r13_map` → 마을은 납품 B 지도 `room13_map_village_b.rpy r13_map_village_b`(수첩 틀·이름표·확대), 그 밖 지역은 `room13_map_b.rpy`. 상태 표식 `room13_map_status.rpy`. 지도 노드 `room13-cartography.json`, 별칭 `R13_V111_MAP_ALIASES`. |
| v111 규칙 | 갈 수 있는 곳 = 지금 장소 + 이 대기 선택지의 장소(`r13_places` 6층, 마지막 v111). 이동 대기(`travel`)는 목적지 하나. 이동 차례면 목적지를 골라 둔 채 연다(2026-10-30). 「이야기가 데려가는 이동」(move_by_story)은 지도에서 골라도 이야기 label 이 옮긴다. |

## 8. 기록(수첩): 자료·사람·메모·갈림길

| 항목 | 지금 |
|---|---|
| 그리는 곳 | `room13_notebook.rpy:282 r13_records` → `systems/room13_evidence_view.rpy r13_evidence_browser`(탭: 자료·사람·메모·갈림길, `r13_ev_record_tabs`), 수첩 틀 `systems/room13_notebook_shell.rpy`, 자료 서랍(획득 날·출처 묶음) `systems/room13_evidence_drawer.rpy`(표 `v111/evidence-drawer.json`, 생성기 `dev/build_evidence_drawer.py`). |
| 자료 | 이름·종류(물증·기록·관찰기록·증언)·그림·facts(`v111/evidence-facts.json`)·얻은 곳. 변형(variant)과 동적 이름(초상·침구·E05). 자료 그림 `assets/evidence/<ID>.webp`, 없으면 옛 그림 대응(`R13_V111_MATERIAL_ART`). |
| 사람 | 관계도 `systems/room13_relations.rpy` + `systems/room13_v111_relations.rpy`(만난 사람만, 죽음 표시). |
| 메모 | `systems/room13_learning.rpy r13_learning_notes`. |
| 갈림길 | `room13_fork_screen.rpy r13_fork_screen`: 회의·운명점마다 결과 카드(persistent 회차 기록, 스크린샷). |
| 소유자 결정 | 수첩 계열 화면은 **모두 갈림길과 같은 수첩 판**(`b_opt_panel`, 화면 안에 다 들어오는 것). 글자가 칸 밖으로 나가면 안 되고 버튼은 틀 안에(2026-10-27). 「대화」 탭은 뺐다(백로그가 대신). 갈림길: 누군가의 운명이 갈린 회의에만 「?」, 안 본 결과는 개수만. 기록 문장은 관찰·들은 말만, 추론을 넣지 않는다. |

## 9. 생각(목표 문구)

| 항목 | 지금 |
|---|---|
| 그리는 곳 | `r13_hub` 안 `systems/room13_goal_fold.rpy r13_goal_fold`(접히는 띠). 글은 `r13_v111_goal`(4층, 마지막 `systems/room13_v111_goal.rpy:213`). |
| 글 | 대기별 할 일 한 문장 `R13_V111_STEP_GOALS`, 없으면 장면 의문 `R13_V111_QUESTIONS`(later_bindings). 이동 중에는 직전 장면 문구를 유지(thought_pending), 이동 목적지 안내를 덧붙임. |
| 원칙 | 안내는 목적지·행동 대신 풀리지 않은 의문으로(ROOM13_GUIDE). 정답 자료·결과는 말하지 않는다. |

## 10. 저장·불러오기·설정

| 항목 | 지금 |
|---|---|
| 설정 | `screens.rpy:323 pause_menu`: 탭 넷(소리·화면·읽기·저장), 수첩 판 `assets/ui-b-options/b_opt_panel.png`. 글자 크기(작게·보통·크게), 창 투명도, 움직임, 타자음 미리보기. |
| 저장 | 설정의 넷째 탭 `r13_settings_save_tab` + `file_slots`, `save`/`load` 화면(screens.rpy:439·444). 메인 메뉴에서는 불러오기만. 저장 정리 `room13_save_ui.rpy`. |
| 불러온 뒤 | `label after_load` → `r13_upgrade()`. **v111 이전 저장 호환은 포기**(소유자 승인, room13.rpy 주석). 옛 png 경로는 `room13_webp_alias.rpy` 가 webp 로 잇는다. |
| 소유자 결정 | 저장·불러오기는 설정창 아래 줄. 다시 시작할 아침은 뺐다(2026-10-27). |

## 11. 엔딩

| 항목 | 지금 |
|---|---|
| 결정 | 14일 `r13_nw_ending14`: 남겨진 이름(다람이 수레로) → 얼어붙은 마을(잃은 사람 4명 이상) → 가족을 택한 밤 → 남은 사람들 → 상처 입은 귀환 → 마을의 아침. 진엔딩 「새로운 아침」 조건 `r13_nw_true_ending_ready`, 불타는 밤 `r13_nw_wild_night_ready`. |
| 결말 컷 | `systems/room13_end_cut.rpy`: 줄의 `endcut`(END-xx[:판], MEM-xx) → 어두워졌다 그림만 2초. 그림 없으면 아무것도 안 함. |
| 엔딩 카드 | `systems/room13_end_cut.rpy:120 r13_end_card(name, stat, lost)`: 수첩 판에 결말 이름·지킨/잃은 사람, 「저장하기」「메인 화면으로」. 결말 기록은 이야기가 끝날 때(story14_completed) `r13_fork_ending`. |

## 12. 그 밖의 공통 장치

- **상태 저장소**: 모든 상태는 `room13` 사전 한 곳(`room13["v111"]["values"]`, 자료 `room13["evidence"]`, 깃발 `room13["flags"]`). 쓰기는 `r13_v111_set`(3층: 날짜·생사·구금이 옛 상태 칸까지 같이 바꾼다, 마지막 층 `room13_fork_screen.rpy:370` 이 갈림길 기록). 원문 동작은 `r13_v111_apply/commit/option` 이 한 번만 적용(applied 깃발).
- **장면 진입 검사**: `r13_v111_scene` 이 장면마다 날짜·필요 자료·값(R13_V111_ENTRY, R13_V111_SCENE_CHECKS)을 검사하고 어기면 예외로 멈춘다. 새 판에서도 같은 단언을 두면 분기 오류를 바로 잡는다.
- **음악·환경음**: 장면별(records.json audio/ambience 82장면), 장면 덮어쓰기(music_override/hold), 장소별 기본(`systems/room13_sound.rpy R13_PLACE_SOUND`), 이동 효과음, 환경음 채널 4종(wind·fire·clock·heartbeat).
- **도트 연출**: `systems/room13_dot_fx.rpy`(불꽃·눈·연기·깜빡임·조명 장치), 그림책 전환(`systems/room13_storybook.rpy`), 한 번 치는 효과(`systems/room13_impact_fx.rpy`, fx: jolt·shake·slam·flash). 원칙: 튀는 효과 없이 은은하게(0.18.47).
- **대사 컷·그림책**: `systems/room13_ep_art.rpy r13_ep_line_art`(4층, 마지막 end_cut): 줄의 `cut`(ev:자료 그림, room13-ep-*, 특수 컷).
- **회의 결과 → 운명**: `r13_nw_meeting_end`(한 번만), `r13_fork_set_fate`, 이송 명단 `r13_nw_list`, 죽음 깃발.
- **관리자 도구**: `systems/room13_admin.rpy`(톱니 길게, 장소·날짜 이동), `systems/room13_admin_meeting.rpy`. 시험용.
- **글자 단계**: `systems/room13_type_scale.rpy r13_type`(하드코딩 금지), 타이포 `docs/design/TYPOGRAPHY_V2.md`, 부품 규격 `docs/design/UI_COMPONENTS.md`.

---

## 버리는 옛 기능 (v111 에서 닿지 않는 것)

판정: 시작(`start`)에서 label·화면이 하나도 닿지 않는 rpy 67개(정적 추적). 단 함수·화면을 다른 길로 부르는 15개(갈림길·회의 다시 하기·도트 연출·임팩트·그림책·회의 연출·polish3 오버레이·선택 문제 안내·room13_life·room13_interaction·first_mystery·gate_inspection·first_day_flow·new_places·materials)는 일부가 살아 있어 「버림」에서 뺐다. 이 파일들의 **함수 층**은 v111 경로에서도 불릴 수 있으므로(예: `r13_topics` 24층) 새 판에서 옮기지 않으면 되고, 지금 판에서 지우는 것은 별도 검증이 필요하다.

| 묶음 | 파일 | 무엇이었나 |
|---|---|---|
| 재판·옛 회의 | `room13_week2.rpy`, `room13_week2_rules.rpy`(장소 표만 v111 이 씀), `systems/room13_debate.rpy`, `systems/room13_meeting_flow.rpy`, `systems/room13_q1_arguments.rpy`, `systems/room13_q1_difficulty.rpy`, `systems/room13_q1_review.rpy`, `systems/room13_alibi.rpy`, `room13.rpy` 의 `r13_trial`·`r13_day`·`r13_roam`·`r13_field` | 사건 09 재판·C1~C4 쟁점·투표·알리바이 대조. v111 회의는 6장의 새 경로. |
| 상점·생계(직업)·장터 | `systems/room13_shop.rpy`, `systems/room13_livelihood_flow.rpy`, `systems/room13_livelihood_ui.rpy`, `systems/room13_direct_work.rpy`, `systems/room13_bundle3.rpy`, `systems/room13_gimmicks.rpy`, `systems/room13_new_places.rpy` 의 label(장터·낚시) | 돈(냥)·일감·물건 사기·가판대. `r13_hub` 의 「가진 돈」은 livelihood_open 깃발이 없어 v111 에서 안 보인다. |
| 옛 사건·마을 사건 | `systems/room13_ep1_lamp_thief.rpy`~`room13_ep6_cart.rpy`, `systems/room13_episodes.rpy`, `systems/room13_ep_story.rpy`, `systems/room13_episode_aftermath.rpy`, `systems/room13_town_events.rpy`, `systems/room13_town_events2.rpy`, `systems/room13_week1_cases.rpy`, `systems/room13_week2_events.rpy`, `systems/room13_new_cast.rpy`, `systems/room13_owl_buri.rpy`, `systems/room13_piko_causality.rpy`, `systems/room13_sling_confidence.rpy` | 옛 이야기 판의 사건 6개·마을 사건 묶음. 같은 인물이 v111 에서 다른 이야기로 나온다. |
| 저녁 미션·사건 제안 | `systems/room13_evening.rpy`, `systems/room13_event_offers.rpy`(화면은 v111 에서 숨김) | 저녁 할 일 고르기, 표시로 띄우는 일반 사건. v111 대기에는 저녁 메뉴가 없다(0.20.6). |
| 옛 첫날·생활 | `room13_family_bundle.rpy`, `room13_gate_inspection.rpy` 의 label, `systems/room13_first_day_flow.rpy` 의 label, `room13_inspection.rpy`(책상 근접 조사), `room13_life.rpy` 의 label, `systems/room13_life_closeups.rpy`, `systems/room13_life_groups.rpy`(화면 일부만 닿음), `systems/room13_daram_mood.rpy`, `systems/room13_convenience.rpy`, `systems/room13_inn_change.rpy`, `systems/room13_granny_reply.rpy`, `systems/room13_reinspect.rpy`, `systems/room13_use_knowledge.rpy`, `systems/room13_memory.rpy`, `systems/room13_topic_record.rpy`, `systems/room13_carryover.rpy`, `systems/room13_poc_route.rpy`, `systems/room13_materials.rpy` 의 label | 옛 1일(입구 정정·편지 근접)·생활 행동·잠자기·회차 넘김(회차 리셋 원칙과 충돌해 꺼짐). |
| 옛 화면 | `room13_cinematics.rpy`, `room13_record_compare.rpy`, `room13_revision.rpy`, `room13_worldmap_v5.rpy`, `room13_inn_navigation_v4.rpy`, `room13_dialogue_openings_20261013.rpy`, `room13_asset_toolbox.rpy`, `systems/room13_ending_story.rpy`, `systems/room13_return_recovery.rpy` | 옛 컷씬 보기·기록 대조·판 개정 재시작·옛 세계지도·여관 안내·옛 엔딩 이야기. |

v111 안에서도 닿지 않는 label 8개: `r13_v111_crowd_block_old13`, `r13_v111_crowd_failed13`, `r13_v111_shelter_choice`, `r13_v111_shelter_work`, `r13_v111_today6`, `r13_v111_permission_today6`, `r13_v111_acorn_recover6`, `r13_v111_acorn_recovered6`(옛 저장을 위해 남긴 이름). 1일 입구의 짐 갈래와 조사 선택지 [4](gate_lodging_retired, 쓰는 곳 없음)도 실제로 닿지 않는다.

## 새 판 설계에 바로 쓸 관찰(사실)

- v111 이 쓰는 흐름 장치는 사실상 다섯: **대사 묶음 재생**(r13_lines), **대기 관문**(field-bindings 한 표 + 인물/물건/지도/제시 입력), **증명**(정답·대체·덧붙임·기회), **메뉴**(menu/display_menu, 37곳), **상태 값 쓰기·읽기**(r13_v111_set/value, 조건 이름표 R13_NW_WHEN 308개). 나머지는 표시 층이다.
- 대사는 원문(records.json) + 날짜 패치(dNN.json)의 2단 합성에 rpy 직접 줄이 더해진다. 새 판은 합성 결과(day01.json 형식)를 원본으로 삼으면 덮어쓰기 층이 필요 없다.
- 같은 함수의 층이 많다(`r13_topics` 24, `r13_present` 22, `r13_stage_people` 18, `r13_object_visible` 11, `r13_where` 10 …). v111 경로가 실제로 쓰는 것은 각 함수의 마지막 v111 층과 그것이 부르는 바로 앞 층 일부뿐이다(INVENTORY.md 「덮어쓰기 최종 동작」).
