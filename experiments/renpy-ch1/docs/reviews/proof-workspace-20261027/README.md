# 자료 대조 통합 화면 시범 적용 (2026-10-27, UX 인계서 D01·D02·D03·D06)

인계서 `docs/reviews/ux-handoff-20261027/인계서_v1.0.txt` 1차 범위 중 D01(발언 문맥과 통합 화면)·D02(전체 자료와 체크 선택)·
D03(두 자료 나란히 읽기와 제시 절차)·D06(휴대폰 배치)을 시범 3장면에 붙였다. D04·D05·D07은 이 작업 전에 이미 들어가 있던
계약(`review_return`, 「조사 계속」 반환 "investigate", `r13_nw_can_solve`, 목표 문구) 위에 올렸다.

- 1일 입구 「함께 들어갈 근거를 고른다」(`r13_v111_gate_proof`)
- 1일 두 편지 「두 편지를 나란히 본다」(`r13_v111_letter_compare`, compare 모드)
- 7일 화재 첫 추궁 「불이 시작된 곳과 진술을 대조한다」(`r13_v111_nubi_proof7`)

## 바뀐 파일·심볼

| 파일 | 내용 |
|---|---|
| `game/systems/room13_proof_workspace.rpy` (신규) | 표시 문맥 표 `R13_PW_CONTEXT`, 순수 선택 계산 `r13_pw_order`·`r13_pw_toggle`·`r13_pw_replace`·`r13_pw_remove`·`r13_pw_submit_ok`·`r13_pw_pair_*`, store 도우미 `r13_pw_active`·`r13_pw_entries`·`r13_pw_sections`·`r13_pw_*_action`·`r13_pw_layout`, 화면 `r13_proof_workspace`(부품 `r13_pw_card`·`r13_pw_checkbox`·`r13_pw_detail`·`r13_pw_pair`·`r13_pw_chips`), UI 기억 `default r13_pw_views` |
| `game/room13_v111.rpy` `r13_v111_proof_again` | 시범 쟁점(`r13_pw_active(key)`)이면 `call screen r13_proof_workspace`, 아니면 기존 `r13_crisis_proof`. 반환 `("toggle",키)` 분기 추가. 나머지 분기("argue"/"press"/"investigate"/("remove",키)/판정/기회)는 그대로 |
| `dev/test_proof_workspace.py` (신규) | 순수 계산·문맥 표 단위 시험 9개 |
| `dev/test_type_scale.py` | 허용 파일 목록에 새 파일 추가(새 파일은 `r13_nb_*` 도우미만 쓰고 `r13_type` 직접 호출 없음) |
| `game/qa_tests/zz_proof_workspace.rpy` (임시) | 세 장면 캡처·조작 시험. 공개 전 삭제 대상 |
| `game/qa_tests/v111_newworld_d01.rpy` `v111_nw_d01_gate_extra_letter` | 입구·편지가 통합 화면으로 바뀌어 조작을 체크/「근거 제시」로 고침(단언은 그대로) |

## 표시 문맥 표 (`R13_PW_CONTEXT`)

| 쟁점 key | mode | speaker | quote | 노출 조건 |
|---|---|---|---|---|
| 함께 들어갈 근거를 고른다 | proof | 돌목 | 종이엔 그렇게 적혀 있소. 일꾼은 본인만. 아이는 안 되오. | `r13_has("v111:entered:MS14_D01_S02")` (첫 입구 대사 장면을 지난 뒤) |
| 두 편지를 나란히 본다 | compare | (없음, 「의문」) | 두 편지를 직접 읽고 견준다. 무엇이 같고, 무엇이 다른가. | 항상 |
| 불이 시작된 곳과 진술을 대조한다 | proof | 보리 | 불이 번지기 전에 누비 씨가 창고 문 앞에 서 있는 건 봤소. | `r13_v111_value("bori_nubi_door_witness_heard") is True` |

제목은 기존 `R13_PROOF_TITLES`(없으면 key) 그대로. 정답 ID·미획득 자료·미래 대사는 표에 없다.

## 화면 구조

- PC 1280x720(시안 A): 수첩 공통 틀(`r13_notebook_shell`, 제목 「자료 대조」, 오른쪽 위 남은 기회 stamp, 「조사 계속」이 있는 쟁점만 X).
  왼쪽 열 쟁점 제목·발언·안내 / 가운데 탭(전체·이번 사건·지난 사건·사람별)과 자료 목록(체크 영역 | 이름·그림 영역) /
  오른쪽 열어 본 자료 상세(기존 `r13_evidence_heading`·`r13_evidence_picture_box`·`r13_evidence_fact_list`·`r13_drawer_note_blocks`,
  아래 고정 「출처 펼치기」·「⇆ 나란히 놓기」) / 아래 고른 자료 칩(× 해제) / 버튼 줄(되묻는다·조사 계속·근거 제시|비교 마치기·나란히 보기).
  전체 화면 스크롤 없음, 목록·상세·쌍 열만 뷰포트.
- compare(두 편지): 정확히 둘을 체크해야 「나란히 보기」·「비교 마치기」가 켜진다. 셋째를 체크하면 칩 줄이 「〈셋째〉와 바꿀 자료: [A ⇆][B ⇆][취소]」로 바뀐다(자동 교체 없음).
  「비교 마치기」는 "argue" 를 돌려 기존 성공/`r13_v111_letter_retry` 판정으로 바로 간다.
- 일반 proof 의 읽기용 쌍: 상세의 「⇆ 나란히 놓기」 → 목록에서 이름을 누르면 둘을 나란히 읽는다. 제출 묶음(`room13["arguments"]`)은 건드리지 않는다.
- 휴대폰(`r13_touch_ui()` True, 시안 C): 위 한 줄에 발언 접기 버튼(쟁점 제목 한 줄 + 「돌목의 말 · 접기/펼치기」)과 탭 넷(88px),
  펼친 발언 틀, 본문은 목록(두 열, 큰 글씨는 한 열) 또는 상세(그림 왼쪽·관찰 사실 오른쪽) 중 하나(모달 겹침 없음), 아래 칩 줄(64px)과 버튼 줄(88px).
  상세에서 「목록으로」로 돌아오면 탭·선택·발언 상태가 그대로다.
- 기억: 탭·열어 본 자료·발언 접힘은 `r13_pw_views[claim]` 에만 둔다(구 저장에 없으면 기본값). 선택은 기존대로 `room13["arguments"][claim]`.

## 지키지 않은 것이 없는지 (인계서 13장)

- 정답 함수(`r13_v111_proof_accepts`·`R13_PROOF_ALTERNATES`·`R13_PROOF_EXTRAS`·`r13_v111_proof_kept`·`r13_v111_proof_sets`)를 새 파일에서 부르지 않는다(단위 시험 `test_no_answer_function_in_module`).
  목록은 `r13_catalog_entries(hearing=True)` + `r13_catalog_can_present` + 서랍 접기(`r13_drawer_visible`)로만 뽑고 획득 날(최신 먼저, 동률은 목록 순서)로 정렬한다.
- 기회는 `r13_v111_proof_chances`를 표시만 하고 차감은 기존 라벨(`r13_nw_retry`)만 한다. 읽기·체크·탭·비교·복귀·빈 제출은 "argue" 를 돌려주지 않는다(빈 선택은 주 행동 비활성, 키 바인딩 없음).
- `v111_claim`·`room13["arguments"]` 구조·판정 분기·오답 특례(`gate_number`)·결말·생사 조건은 손대지 않았다.
- 정답 ID·미획득 자료·정답 개수·실루엣을 화면에 내지 않는다(T01 단언: E04 미획득 상태에서 목록에 없음).
- 가짜 임시 그림을 넣지 않았다(D07 관찰도는 이 작업 범위 밖, 기존 그림 그대로).

## 검사

- 단위: `python3 -m unittest discover -s dev -p 'test_*.py'` → 1140개 OK(기존 1131 + 신규 9). override map 실패 없음.
- lint: 새로 생긴 경고 없음. 남은 「Unreachable Statements」(`room13.rpy`, `room13_v111_days123.rpy`)는 이 작업이 손대지 않은 파일의 기존 경고.
- 화면 시험(`RENPY_SDK=... ROOM13_TEST_TIMEOUT=300 ./dev/run_renpy_tests.sh zz_pw_gate zz_pw_letters zz_pw_fire v111_nw_d01_gate_extra_letter`) 전부 PASSED. 캡처는 이 폴더(`pw-*.png`).

| 항목 | 결과 | 어디서 |
|---|---|---|
| T01 미획득 미노출·조사 계속 무벌점 | 통과 | zz_pw_gate(E04 미획득 → 목록 없음, 「조사 계속」 뒤 tries:gate 0) |
| T02 미수집 오답 1회 차감 | 통과(차감만) | zz_pw_gate(E01+E02 제출 → tries:gate 1). 「다 있었다」 문구 미노출은 D04 쪽 시험 범위라 여기서 단언하지 않음 |
| T03 확보 후 오답·유효 자료 보존 | 부분 | zz_pw_letters(E01+E02 → E01 남고 E02 빠짐). 입구에서는 따로 안 함 |
| T04 조사 복귀→재진입 | 통과(1회) | zz_pw_gate·zz_pw_fire. 3회 반복은 안 함 |
| T05 체크·상세·출처·탭·비교 취소 무차감·선택 보존 | 통과 | zz_pw_gate(탭 바꿔도 선택 유지, 쌍 읽기 뒤 선택 유지), zz_pw_letters(교체 취소) |
| T06 기존 정답·덧붙임 제출 | 통과 | v111_nw_d01_gate_extra_letter(E01~E04 → win, proof_given 동일) |
| T07 두 편지 나란히 읽고 완료 | 통과 | zz_pw_letters(체크 A → 체크 B → 나란히 보기 → 비교 마치기 → room_compare) |
| T08 잘못된 조합·셋째 자료 | 통과 | zz_pw_letters(셋째 → 교체 질문, 잘못된 쌍 → 무벌점 재시도) |
| T09 3개 선택 뒤 두 개 읽기 | 통과(2개 선택 기준) | zz_pw_gate(E02·E03 선택 상태에서 E02·E01 읽기 쌍 → 선택 그대로). 3개 이상 선택은 자료가 셋뿐이라 둘로 확인 |
| T10 witness False/True | 통과 | zz_pw_fire(False 에서 발언 숨김, True 에서 표시). 구 저장 불러오기는 안 함 |
| T11 선택 중 저장→불러오기 | 미수행 | 저장/불러오기 조작 시험을 만들지 않음. 새 변수는 `default` 라 구 저장에서 기본값으로 열린다(코드 상 확인만) |
| T14 1280x720 · 844x390(터치 규격) · 큰 글씨 | 통과(캡처 확인) | 세 장면 PC/휴대폰/큰 글씨 캡처. 390x844 세로·실기 브라우저 배율은 안 함 |
| T12·T13·T15·T16·T17 | 미수행 | 이번 작업 범위 밖(옛 캠페인·NPC 제시 화면은 건드리지 않았고 폴백 유지) |

## 지시와 다르게 한 것

- 「`r13_evidence_single`/`r13_evidence_pair` 부품 재사용」은 그 두 화면 자체가 `R13_EV_*` 고정 좌표(기록 화면 자리)에 그려지므로 통째로 넣을 수 없었다.
  그 안의 부품(`r13_evidence_heading`·`r13_evidence_picture_box`·`r13_evidence_fact_list`·`r13_drawer_note_blocks`, 출처 펼치기 본문 구성)을 가져와
  `r13_pw_detail`·`r13_pw_pair` 가 자기 자리에 그린다. 기존 두 화면은 손대지 않았다.
- 체크 켜기·끄기는 화면 안에서 `r13_pw_toggle_action` 이 처리한다(기존 `("remove",키)` 반환처럼 라벨로 되돌아가 다시 `call screen` 하면 탭·열어 본 자료가 매번 초기화돼서).
  room13 을 복사해 `arguments` 만 바꾸는 규칙은 같고, 라벨 쪽에도 `("toggle",키)` 반환 분기를 두어 어느 길로 와도 같은 계산을 쓴다.

## 알려진 한계·남은 문제

- 목록 폭이 좁아 긴 이름(「등잔·천·발화 지점」)은 두 줄이고, 그때는 「N일 · 장소」 꼬리표를 숨긴다(휴대폰 88px 칸에서는 보인다).
- 휴대폰에서 발언을 펼친 채 상세를 열면 본문이 낮다(약 180px). 사실 줄이 길면 상세 열 안에서 스크롤한다.
- 캡처의 왼쪽 위 작은 상자(「방문 신청 원본」 등)는 시험 fixture 의 `r13_grant` 가 띄운 획득 알림이지 이 화면의 요소가 아니다.
- 터치 표적은 Ren'Py 좌표 기준(버튼 88·탭 88·카드 88·칩 64·체크 영역 56x88). 844x390 실표시(약 0.54배)에서 칩 줄 64px 는 약 35 CSS px 라 44 CSS px 기준에 못 미친다. 실기 확인 필요.
