# 제작기준본01 D01 · 기존 시스템 재사용 교정

기존 main 기준: `1085e4e5a6fdceda24e208a5975a2f6ac097bb4f`.
이전 작업 head: `8675ce76d0759cec5da952fa3de3f45805851e19`.
복구 브랜치: `backup/production-basis01-before-reuse-8675ce76`.
이번 교정은 같은 `story/production-basis01-demo`와 Draft PR20에 게시한다. 사용자가 기존 실행분 포함 총 US$1 이내 CI·빌드·검수 결과물 업로드를 승인했다. main 병합과 배포는 제외한다.

## 교정한 책임

- runtime `game/python-packages/production_basis01.py`의 별도 상태 생성·조건 실행·효과 원장을 제거했다.
- 제작용 원문 조건/효과/ID 검증만 `dev/validate_production_basis01.py`로 옮겼다. 게임에서 import하지 않는다.
- `production_basis01.rpy`는 원문을 대사 packet으로 읽는 함수와 D01 장면 대본이다. when/effects 배열을 실행하지 않는다.
- 증거는 기존 `room13.evidence/records`, 분기는 `room13.flags`, 날짜·장소는 기존 `r13_edit`에만 기록한다.
- 획득은 `r13_grant`, 플래그는 `r13_flag`, 가용성은 `r13_available`를 사용한다.
- D01의 효과는 증거 추가와 bool 표식뿐이다. 기존 함수의 중복 방지를 사용하므로 별도 applied/completed_inputs 원장이 없다.
- 일회성 활동이 아닌 대사·자료 재열람에 가짜 activity/done 항목을 추가하지 않는다. 실제 활동의 done 처리는 기존대로 둔다.
- 별도 day/location/evidence/alive/elapsed_minutes 상태와 새 상태 저장 체계가 없다. 분 단위 시계를 추가하지 않는다.
- 추가 default 상태 변수가 없다. 선택은 기존 r13_choice/r13_item/r13_present_priority를 사용한다.

## 실제 연결

1. `room13_start`의 초기화는 기존 `r13_new/r13_upgrade` 그대로이다.
2. D01 시작은 기존 `r13_carriage`를 호출한다. 해당 label의 캠페인 분기에서 새 대사만 재생한다.
3. 입구는 기존 `r13_entry` → `r13_hub(entry=True)`를 사용한다. 별도 조사 메뉴를 제거했다.
4. 현장 서류 클릭은 `r13_object` → 기존 `r13_inspect_gate_documents` → 새 원문 대사와 `r13_grant`로 이어진다.
5. 벽 규정 클릭도 기존 `r13_object` 경로에서 새 규정 대사와 획득으로 이어진다. 입장 즉시 E03/E04를 지급하지 않는다.
6. 돌목 질문은 기존 `r13_entry_topics`와 `r13_entry_dispatch`에서 원문 선택지/조건으로 연결한다.
7. 수첩/제시 화면은 기존 `r13_book`이고, 제시는 최종 `r13_present` wrapper의 PB01 증거 분기에서 기존 22층 호출 체인의 이력 처리를 유지한다.
8. 비교는 최종 `r13_compare_result` wrapper에서 해당 두 원문 문서만 대조한다. 소지하지 않은 문서를 비교해도 목적 차이 표식이 생기지 않는다.
9. 정답 뒤 기존 `r13_entry_done` 경로에서 새 등록 대사를 재생하고 `entry_corrected`를 기록한다. 반박 성공과 등록 완료는 별개 표식이다.

새 screen/조사 엔진/대결 엔진은 없다. 별도 근거 체크 선택도 제거했다. 기존 r13_book에서 신청 원본과 규정을 차례로 고른다. 원본의 가족 방문·2인 숙소와 규정이 세 근거이고, E02 보유도 기존 r13_available로 확인한다.
기존 비교 판정에 문서 쌍만 연결했다. r13_records에서 compare 탭을 all로 돌리는 기존 처리는 그대로이며, 퇴역 UI를 재활성화하지 않았다. 돌목의 기존 질문 목록에서 두 문서를 대조한다.
증거 ID는 구 본편 E02/E03/E04와 뜻이 달라 수첩 키에 PB01 이름공간을 유지한다. 소유 목록은 room13 하나뿐이다.
원문 scene/record/option ID는 추출 JSON에 그대로 있고 대사 packet의 source_record_id에도 남긴다.

## 적용 상태와 범위

D01 마차·편지 → 정차·처리 명단 → 원본/규정 조사 → 목적 비교·힌트·제시 → S04 등록 완료까지이다.
이유 질문은 선택이며 세 근거를 먼저 제시하면 즉시 정답 대사로 간다.
S04의 추가 질문 이후, 13호실, D02/D03, 새 아트는 이번 범위가 아니다.
승인되지 않은 표정·문서 후보·새 음원·분 시계를 추가하지 않는다.
원본 조건과 기존 시간대 모델의 분 단위 표현 차이는 임의 시계 구현으로 해결하지 않는다.

## 검수와 남은 제한

- 원문 추출 동일성: `dev/import_production_basis01.py SOURCE --check`.
- D01 로컬 검사는 기존 r13_new/r13_edit/r13_grant/r13_flag/r13_available/r13_compare_result 함수를 소스에서 그대로 불러 수행한다.
- native 검사도 기존 room13 소유 목록/플래그만 확인하도록 수정했다. 이전 테스트용 별도 원장 비교는 제거했다. 수첩 선택은 기존 QA harness의 stub을 사용하므로 실제 수첩의 화면 검수와 구분한다.
- 로컬 JSON roundtrip은 실제 Ren'Py 저장/로드 검증이 아니다. 이번 교정의 native/시각 검수는 미실시다.
- SDK 로컬 공식 다운로드는 이전에 CONNECT HTTP403으로 차단됐다. 이번에는 재시도하거나 다른 경로로 받지 않았다.
- 기존 head의 등록 후 로드 단언은 실패했다. 교정 뒤 실제 엔진 재검사가 필요하며 해결 완료로 보고하지 않는다.
- 기존 granny 실패는 `investigation_person_placement_diag.rpy:227`의 tooltip/hub hint 해제 3초 대기에서 발생했다.
  해당 테스트/호버 helper는 main과 바이트가 같고 이번 교정에서도 변경하지 않는다. 회귀/환경 여부는 baseline native 비교 전 미확정이다.
- 이전 PR20 save의 삭제된 label 호환은 보장하지 않는다. 복구 head/브랜치와 PR은 보존했다. 새 UI/저장 변환 기능을 추가하지 않는다.
- 이전 CI/스크린샷 통과를 이번 미커밋 교정의 플레이 통과로 쓰지 않는다.

## 검사 책임 교정

기존 15개 단위검사에서 제거한 별도 상태 factory·조건 실행기·효과 원장·copy-on-write 검사는 삭제된 구현에 종속됐다. 현재 12개는 실제 기존 상태 함수의 증거/플래그 중복 방지, 미조사 자료 미지급, 소지 조건, 조기/정규 정답, 누락/오답, 기존 제시 체인 호출과 상태 roundtrip을 검사한다. 검사 개수 자체는 동등한 native 커버리지의 증명이 아니다. 편지 열기·마지막 줄·글씨·닫기와 두 도착 선택, 오답→힌트→정답, 실제 저장/로드/스킵은 native 2개에서 확인한다. JSON roundtrip이나 소스 hook 단언으로 native 성공을 대체하지 않는다.
