다람탐정 0.17.7-dev 개발 소스
최신 개발 0.17.7-dev (2026-10-14)
0.17.4~0.17.6-dev(입구 공동 조사·엄마 단서, 입구 가로 배경, 회의 좌석)를 3-way로 합친 판. 회의 자동 테스트 6개(dev/renpy_trial_tests) 추가·통과. 발언을 깬 뒤 선택이 '사실인 말'로 가던 문제, 제단 화면 카드 넘침 수정. RELEASE_0177.md 참조. 재포장은 --asset-root로 디자인 브랜치(ac8760b)의 입구 배경 원본을 지정해야 한다.
최신 UI·회의·저장 규칙을 유지하고 입구 공동 조사와 인물 접근 대화 복구.
FIRST_RUN_CLUE_FLOW.md 및 qa-room13-intro-clues/report.json 참조.

0.17.5-dev: main 7bade06(0.17.4)의 동행 조사·주민 접근·엄마 단서 연결을 보존. 입구 가로 배경 3장과 조사 좌표·취소 영역, 저장 쪽 전환 수정. RELEASE_0175.md 및 reports/room13-spatial-20261014/GATE_0175_KO.md 참조. 추가 PNG는 design/room13-ready-assets-20261014/backgrounds/gate/, 해시는 dev/selected_asset_overlay.json.

0.17.6-dev: 기존 프로필을 이용한 회의 자리·발언자 강조, 발언 스크롤 복귀, 긴 힌트/고정 행동 버튼. 회의 엔진과 C2/C4 입증 규칙은 보존. RELEASE_0176.md 및 MEETING_0176_KO.md 참조.
