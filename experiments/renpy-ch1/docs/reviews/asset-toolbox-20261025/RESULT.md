# 에셋 도구함 모듈화 검수 · 2026-10-25

기존 디자인과 대사·분기를 유지하면서 등록 정보, 태그 매칭, 게임 표시, 제작 도구를 분리했다. 같은 역할/그룹을 사용하는 화면은 한 번의 연결 변경을 공유한다.

- 등록: 물리 파일 3,086개와 가상 부품 15개, 연결 역할 3,104개.
- 공통 버튼: 기본·누름·선택·비활성을 묶어 교체. 상태 누락·중복 매칭·다른 캔버스·비균일 확대·잘못된 crop/frame은 저장 전에 차단한다.
- 기존 파일 경로도 공통 연결을 따라가며, 웹용 PNG/WebP 호환 로더를 함께 유지한다. 폰트와 초기화 시 고정되는 항목은 재시작이 필요하다.
- 개발 도구는 localhost에서 실행한다. 게임 화면에 제작용 버튼을 추가하지 않는다.

## 실제 화면 검증

`b_asset_toolbox`: 메인의 공통 빨강 버튼을 크림 세트로 연결한 뒤 질문 화면에서도 같은 변경 확인. 다시 읽기로 기본 세트 복원. 두 동작 모두 진행 상태 불변 확인.

`b_asset_file_alias`: 직접 경로·도구함 역할·다른 직접 경로 세 곳이 잠금→선택 스티커로 동시에 바뀌고 복원되는 것을 렌더 및 실제 파일 바이트로 확인. 기존 웹 호환 로더가 콜백을 덮어쓰던 문제를 수정했다.

`current_ui_capture`, `b_ui_button_states`, `b_map_village_delivery`, `lowerroad_elder_ticket_art` 통과. 모듈/서버 단위 20건 통과. 전체 단위 1,026건과 Ren’Py lint도 통과했다.

## 캡처

- [도구함](도구함.png)
- [메인 변경 전](toolbox-main-before.png) / [한 번 매칭한 뒤](toolbox-main-matched.png)
- [질문에도 같은 매칭 적용](toolbox-question-matched.png) / [복원](toolbox-question-restored.png)
- [기존 경로 변경 전](toolbox-file-before.png) / [세 경로 동시 적용](toolbox-file-matched.png) / [복원](toolbox-file-restored.png)

사용법과 모듈 경계: [ASSET_TOOLBOX.md](../../../../../docs/ASSET_TOOLBOX.md).

이 브랜치에만 반영한다. main 병합·Pages 공개는 이야기 담당 검토 뒤에 진행한다.
