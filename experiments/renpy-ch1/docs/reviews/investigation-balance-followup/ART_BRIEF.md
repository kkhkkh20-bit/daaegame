# 추가 원화 제작 지침 및 기존 동작 선택 원인

## 제작 필요 — 나비 식당 쟁반과 컵

현재 리소스: `game/assets/room13-pixel-acting-nabi.webp`, `action_2` crop `[1084,533,416,454]`. 0.19.39 식당 실측은 표시 높이226px, 머리 약100.6px이며 컵은 약18~22px로 작다. 전체 인물을 키워도 컵/손/머리 내부 비율은 변하지 않는다. 주변 전경 머그와의 깊이 차이를 고려하더라도 현재 컵은 작은 찻잔으로 읽혀 식당 서빙 소품과 어울리지 않는다.

- 정본 디자인: `art/canonical48-rev45/originals/nabi.webp`.
- 승인된 작업 원화의 얼굴/체형/옷 참고: `art/approved-action27-remaining/originals/KI-1--nabi.png`, `art/approved-nabi-kitchen-extra4/originals/arrange_tray.png`.
- 현재 쟁반 자세는 위 runtime sheet의 action_2. 같은 얼굴·종·의상·꼬리·쟁반 받치는 양손을 유지한다. 식당에서 걷거나 서서 쟁반을 드는 완전한 전신, 투명 배경, 발/손/쟁반 잘림 없이 제작한다.
- 일상용 머그 2개를 머리 높이의 약30~38%로 그린다. 최종 머리 표시 높이110~120px 기준 컵 높이33~46px를 목표로 하되, 손잡이와 손이 서로 파고들지 않고 쟁반 위 바닥 접점이 분명해야 한다. 배경의 매우 가까운 큰 머그와 픽셀 크기를 무조건 같게 만들지 않는다.
- 실제 배경 비교: `reports/place-balance-01936/026-dining-d2-p1-routine.png`, `041-dining-d2-p2-routine.png`, `043-dining-d2-p2-routine.png`; 배경 자산 `game/assets/room13-pixel-wide-dining-afternoon.webp`/`evening.webp`.
- 납품: 수정 없는 원본 PNG와 SHA256, alpha bbox, 머리 bbox, 양발·양손·쟁반 바닥·각 컵 바닥/입구 anchor. 크기 조절/픽셀 파생은 승인 후 기존 importer 방식으로 한다.

이 원화는 현재 미제작이다. 기존 서빙 원화는 보존하며 임의 확대/부분 잘라붙이기로 컵을 완성했다고 표시하지 않는다.

## 반복 동작의 코드 원인 / 새 동작의 교체 조건

`game/room13_acting.rpy:r13_living_pose`는 explicit desired 다음 `living`/`activity`, 이어 첫 번째 `living_*` 키를 선택한다. 마지막 단계에는 날짜·시간 순환이 없다.

- 바둑이: `R13_LIVING_ALLOWED`가 입구·광장을 허용하고 기존 `living_bootlace`가 반복 선택된다. 새 순찰/등 점검 등을 입구와 광장, 오전/오후/저녁으로 분리할 수 있다. 사건 `block_cart`는 덮지 않는다.
- 보리: 입구·창고·광장·수리점에서 `living_firewood`가 반복된다. 실제 의도는 장작 묶기지만 숙인 구도가 신발끈 묶기처럼 반복된다. 학교 뒷줄은 기본 자세가 우선한다. 새 운반/장작 분류 동작은 실제 도구가 있는 장소와 시간대에만 연결한다.
- 종종이: 우체국 모든 시간에 map9 편지 대기 → map27 `PO-3` 편지 품기가 대체된다. 다른 새 동작을 넣으려면 map27의 동일 장소/시간 우선순위를 명시적으로 나눈다.
- 도토: 광장은 action_1, 복도는 오전/오후 action_1·저녁 action_2로 고정이다. 새 동작은 실제 출현하는 이 장소/시간에서 나누고 기존 특별 대화 원화와 구분한다.
- 피코: 광장 오전/오후 `map27_sq_2` 액자 소개, 진료실 day>=11 `map27_cl_1` 침대 앉기. 그림 그리기는 광장의 실제 존재 인물에 연결하고, 환자/이송 상태에서는 침대 동작을 보존한다.
- 굴돌: 수리점 오전/오후에는 이미 `map9_stone_tapping`이 등록돼 있다. 다른 장소/시간의 기본 서기는 이 조건 밖이다. 추가 작업 동작도 실제 작업대/도구 접점과 시간대를 정해 연결한다.

공통: 기존 `r13_where`/사망·구금·이송·대피·event offer가 결정한 출현을 그대로 사용한다. 인물을 새로 만들거나 기존 사건 포즈를 일반 작업으로 바꾸지 않는다. 승인된 새 원화가 도착하기 전에는 빈 행동 이름을 neutral에 붙이지 않는다.
