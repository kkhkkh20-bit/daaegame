# 이동·조사 UI 진단 근거

기준0.19.47(ec6acca9). 실제 Chromium 웹 빌드, PC1280×720와 터치844×390·큰 글씨.2일차 현장 UI fixture이며 전체 스토리 리뷰·실물 휴대폰 테스트가 아니다.

기획: [이동·조사 UI 사용성 개선안](../../design/INVESTIGATION_USABILITY_PLAN_20261018.md).

| 증거 | 관찰 |
|---|---|
| [여관 현장](01-inn-initial.png) | 인접 이동4개가 중앙 가로976px를 덮는다. 열쇠 중심과 ‘여관 밖으로’가 겹친다 |
| [PC 열쇠 중심 탭](pc-keys-center-opens-map.png), [터치 중심 탭](mobile-keys-center-opens-map.png) | 조사 대상 중심을 눌렀지만 지도 창이 열린다 |
| [열쇠 아래쪽 탭](mobile-keys-lower-area-selects.png) | 같은 물건 아래쪽에서는 정상적으로 열쇠가 선택된다 |
| [대화 모드가 이어진13호실](05-room-inherited-mode.png) | 여관→복도→13호실에서도 대화 모드가 유지되어 물건 조작이 비활성이다 |
| [코트 선택](07-selected-coat.png) → [화면을 옮긴 뒤](08-selection-after-pan.png) | 코트가 시야 밖인데 선택 이름과 조사 버튼이 유지된다 |
| [학교에서 돌아온13호실](15-mobile-return-room.png) | 카메라 위치가 복원되며 오래된 코트 선택도 다시 살아난다 |
| [모바일 표식](10-mobile-room-markers.png) |44px 게임 좌표의 작은 표식은 이 해상도에서 약24픽셀이다 |
| [방 안에서 연 마을 지도](12-mobile-village-from-room.png) | 상단은13호실, 여관 건물에는 현재 위치 표식이 없다. 선택 밑줄과 모임 설명이 목적지 정보에 섞인다 |
| [실제 터치 스와이프](mobile-real-swipe.png) | 카메라 이동은 동작하며 게임 진행 상태는 유지됐다 |

`navigation-observations.json`은 실제 인접 이동·지도 선택·취소·학교 왕복·기록 복귀 상태다. `hit-target-observations.json`은 열쇠 중심이 지도를 여는 문제의 PC/터치 재현과 실제 스와이프 결과다. **passed=true는 진단 스크립트가 완료됐다는 뜻이며, 사용성 문제가 해결됐다는 뜻이 아니다.**

선택/실행: game/systems/room13_field_views.rpy. 현장 이동 행: game/room13_screens.rpy. 카메라 기억: game/room13_world_camera.rpy. 지도 현재 위치·선택 표시: game/room13_worldmap_v5.rpy 및 game/room13_navigation.rpy. 소스와 실제 입력 결과를 함께 대조했다.

게임 소스나 공개 배포는 변경하지 않은 기획 브랜치다.

진단 재현 스크립트: navigation_probe.py, hit_target_probe.py. 레포 루트 HTTP 서버8776을 사용하고 프로젝트 디렉터리에서 실행한다. ROOM13_UI_QA_OUT으로 결과 디렉터리를 지정한다. 열쇠 재현은 현재의 잘못된 동작을 확인하는 진단이며, 구현 후에는 올바른 선택 결과로 회귀 기준을 바꿔야 한다.
