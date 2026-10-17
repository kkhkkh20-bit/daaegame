# 정식 0.19.39 빌드의 표정 연결 검증

공식 SDK가 컴파일한 웹 빌드이며 production 함수/label 주입 없이 실행했다. archive SHA256 `4883c104198f52ef3a8270cecb9cf4595037d16d5e605fcd71895ee79ea08240`.

- 실제 `r13_ep1_siluk` 장면에서 `kid_siluk2/joy` 확인. 실제 UI 저장/불러오기 뒤 동일 packet과 joy 복원.
- 실제 “아이에게 묻는다” 선택으로 `ep1:siluk:kid` 진입 및 kid_siluk1 neutral 확인.
- 별도 제어 fixture에서 컴파일된 렌더러로 다람 joy → 미등록 대사 neutral을 호출했다. 논리 pose가 neutral로 같아도 실제 그림이 갱신됨을 두 캡처에서 확인했다. 이 두 화면의 대사 자막은 이전 장면에 남아 있는 것으로, 자연 대사와 해당 표정의 연출 증거가 아니다.
- 꼬미 door_peek 정본 경로와 explicit pose 보호 조건 확인. 이번 검사에서 꼬미 전체 장면/옛 버전 저장 파일 이행은 재검증하지 않았다.
- **대화 묶음 간 되돌리기 미검증**: PageUp, rollback 이벤트, 실제 UI Rollback 액션을 시도했지만 child-one packet에서 이전 packet으로 이동하지 않았다. can_rollback/설정은 true였으므로 “rollback 성공”으로 표시하지 않는다. 원인과 과거 버전 대비는 이 좁은 QA에서 확정하지 않았다. 04번은 복원 성공 화면이 아니라 그때 남아 있던 상태다. 반복 QA를 확대하지 않고 한계로 기록한다.

unit/lint와 공식 빌드는 통과했으며 전체 캠페인/전 버전 저장 호환성까지 검증한 것은 아니다.
