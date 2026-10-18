# 현장 직접 조사 검증 — 0.19.55

원인: 물건 클릭이 조사 실행 대신 r13_field_pick 선택 상태만 바꾸고 있었다. 배경/앞쪽 소품의 클릭을 기존 object 디스패처로 직접 연결하고, 표식과 별도 실행 버튼을 제거했다.

실제 공식 웹 빌드에서 PC(1280×720)와 터치(844×390) 각각 초소 선반 직접 클릭 → G1 실제 획득 → 사람 보기 → 돌목 대화 → 획득한 예약 원본 선택·제시 → entry_corrected 진행을 확인했다. 단서 획득/제시/정정 플래그는 테스트가 부여하지 않고 실제 게임 코드가 만든 결과다.

추가로 여관 열쇠와 장부를 각각 눌러 observed 상태가 생기는지 확인했다. 실제 터치 스와이프로 카메라가640→280 이동한 뒤에도 조사 장면이 열리지 않고 이야기 상태 전체가 같았다. 전체 이야기 재검수는 아니다. 테스트는 dev/qa_direct_investigation.py, 결과는 report.json.

- [PC: 표식 없는 배경](pc-background-no-markers.png)
- [휴대폰: 표식 없는 배경](mobile-background-no-markers.png)
- [획득 자료 제시](pc-owned-record.png)
- [제시 후 진행](pc-after-presentation.png)
- [휴대폰 스와이프](mobile-pan-no-inspection.png)

검사: dev/check.sh(단위 검사와 Ren’Py lint), 공식 웹 빌드 통과.
