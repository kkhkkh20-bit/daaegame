# 검증 범위

기준 commit `91ec49f1c80af18d0c7298f1e4b7463b426c52bb`, tree `d98f5c7026b449b10e93c084198600047adfa8ee`에서 필요한 소스 파일을 Git blob 해시로 확인하고 fixture를 다시 구성했다.

## 통과한 소스 검사

- 57개 회귀 검사.
- 기본 OFF: 882개 상태에서 기존 리스트 identity와 내용을 그대로 보존.
- 예제 ON: 같은 882개 상태/1,520개 등장 기록의 인물·포즈·좌표·크기·깊이·접촉·가림 동일. 52개 상태는 예제 적용, 798개는 미이관 장소, 32개는 해당 연결 대상 없음.
- ON은 전체 actor dictionary의 바이트 동일성을 주장하지 않는다. 오후 세련13개 기록에는 ground_depth=670과 빈 map27_occlusion/map27_keepouts 메타데이터가 추가된다. 기존 화면 좌표·크기·정렬 depth·실제 가림 내용은 같다. OFF는 이 정규화도 하지 않는다.
- 포즈 교체: 세련 chair_read→chair_listen은 geometry 좌표 변경 없이 좌판/발 접촉 유지.
- 기존 map27의 geometry/2차 접촉 assertion과 현행 여관 contact geometry 함수를 fixture로 재사용.
- 우체국 오전 세련 C의 d2/d3/d6 rectangle, depth, 가림이 그대로이며 중복 binding이 없음.
- 없는 pose/asset, 잘못된 digest/crop/투명 여백/방향/접촉/크기, 충돌, 잘못된 polygon/depth, 불완전 guard는 원본으로 되돌아감.
- offer/활성장면/entry/그룹 우선순위, 원래 명단에 없는 인물 미생성.
- alias의 init-only 등록, exact 이름 충돌 거부, 검증 데이터와 runtime spec의 복사 분리, 미검수 새 원화 거부.

전체 actor fixture는 고정 QA flags를 사용한 소스-only 재구성이다. 자연스러운 캠페인 전체 진행이나 가능한 모든 사건 조합의 완전 탐색이 아니다. fixture 구성 때 이미지 loadability와 renderer가 stub 처리되므로 실제 이미지가 보이거나 클릭된다는 증거가 아니다.

기존 override-map 검사 3개와 현행 우체국 직원 접촉 assertion도 함께 통과했다. 새 init184 층을 반영하기 위해 자동 생성 문서 docs/OVERRIDE_MAP.md만 갱신하며, 기존 production source는 수정하지 않는다.

기준 C의 별도 native d2/d3/d6 결과는 [Actions run 39206549349](https://github.com/kkhkkh20-bit/daaegame/actions/runs/39206549349)에서 PASS다. 이는 현재 C의 기술 회귀 검사 결과일 뿐, 오른쪽 서비스 창구의 업무 위치·동작이 적절하다는 시각적 승인이나 기본 OFF인 이 adapter의 native 승인 결과가 아니다.

## 이 패키지에서 하지 않은 것

- 게임 활성화/배포, 기존 production source 수정, 새로운 원화 추가.
- 공통 2×2 renderer 변경이나 저해상도 원화 복원.
- 실행 중 파일 hot reload.
- 이 adapter의 실제 Ren'Py 렌더링, 마우스 클릭, save-load 승인.
- 모든 몸/소품/물체의 opaque-pixel 충돌 판정. 현재 충돌 검사는 얼굴끼리와 이동한 얼굴/중요 물체의 겹침 악화만 막는다.

세련 C는 클립보드 정지 자세만으로 업무 동작이 분명하지 않고 오른쪽 서비스 창구와의 관계도 재검토가 필요해, 배경·업무 포즈 수정이 요청된 실험 배치다. 최종 디자인 승인으로 기록하지 않는다. 오전 C는 registry에 연결하지 않으며 이 문서 갱신은 코드·좌표·가림·원화를 변경하지 않는다.

PR18 C의 별도 native 실행 결과와 이 adapter의 acceptance는 다르다. 기준 배치가 native 검사를 통과하더라도 새 adapter 또는 새 alias가 자동으로 승인되는 것은 아니다. 실제 활성화는 README와 인수인계의 후속 수락 조건을 만족한 뒤 별도 검토한다.

## 원화 승인

기존 authored asset의 사용 가능 상태와 최신 visual reference 검수 상태를 구분한다. 현재 누비 IN-1은 `legacy_coarse` 경고를 유지한다. source_quality의 render_grid_target=2는 목표 기록이며 renderer 변경 완료를 뜻하지 않는다. 생성 중/미승인 원화는 이 패키지에 없다.
