# 실제 목적지와 v5 아트 매핑

기준 main: `47618b989b1d7c79f0964c12db0c40bf4bb34cb1` (`0.17.25-dev`). 실행 소스는 `preview/room13-source/ROOM13_SOURCE_HANDOFF.zip` 안의 `experiments/renpy-ch1/`이다.

v5는 글자가 없는 지도이므로 아래 건물 배치는 기존 장소 노드를 위한 UI 매핑이다. 아트에 원래 적혀 있던 주소나 주민 소유권으로 주장하지 않는다. 배경 주택에 주민/방문 노드를 새로 만들지 않았다. 클릭은 목적지를 선택하고 오른쪽 `이곳으로 이동`에서 확정한다. 모든 일반 지도 이동/열람/선택/취소는 **시간 0**이다.

| 실제 ID | UI 이름 | v5 구조물 / 원본 좌표 기준점 | 기존 조건 |
|---|---|---|---|
| gate | 마을 입구 | 아래쪽 다리 (974,790) | 기본 |
| square | 광장 | 중앙 우물 (872,583) | 기본 |
| inn | 여관 접수대 | 중앙 오른쪽 큰 붉은 지붕 (1047,498) | 기본, 숙박 등록 전에도 접수 가능 |
| post | 우체국 | 다리 왼쪽 앞 붉은 지붕·부속채 (704,625) | 기본 |
| workshop | 수리점 | 왼쪽 아래 물레방아 건물 (291,585) | 기본 |
| clinic | 진료실 | 물레방아 오른쪽 작은 집 (469,546) | lodging |
| school | 학교 | 중앙 왼쪽 큰 푸른 지붕 (711,491) | lodging |
| store | 공동 창고 | 오른쪽 가장자리 목조 건물 (1502,468) | lodging |

미등록 때 clinic/school/store의 레이어 그림은 배경에 그대로 남지만 이름/클릭/접근성 대상은 없다. 큰 목록은 동일한 노출 규칙을 사용한다. 건물별 정확한 다각형·label 좌표·bounds는 `design/maps/20261014/worldmap-v5.json`에 있다.

## 여관 및 산길: 기존 연결 보존

| 실제 ID | 기존 장소 | 노출/이동 조건 |
|---|---|---|
| dining | 식당 | lodging |
| kitchen | 1층 주방 | lodging |
| hall | 2층 복도 | lodging |
| room13 | 13호실 | lodging |
| guestroom | 임시 객실 | lodging AND (family_room_unusable OR case_state == occurred) |
| passage | 13호 뒤 서비스 통로 | passage_open AND secret_route_unlocked |
| facility | 북쪽 보호시설 | day >= 8 |
| greenhouse | 폐온실 지하 작업실 | day >= 8 AND E19 |
| altar | 숲속 제단 | 일반 r13_places에 없고 14일 finale에서 직접 진입. 현재 위치 표시도 finale_started일 때만 |

- 접수대→식당/주방/복도/바깥, 복도→13호/임시 객실 등 기존 `R13_LOCAL_CONNECTIONS`는 변경하지 않았다.
- 세탁실은 독립 node가 없다. 발견 전 이름/툴팁/클릭/접근성에 서비스 통로를 노출하지 않는다. 비밀 장소가 현재 위치로 남은 호환 저장도 발견 필터를 통과해야 지도에 나타난다.
- v5 작은 돌 **신당**과 **옛 채석장**의 독립 방문 노드는 없다. 클릭 없는 장식 레이어로 유지하며 새 사건·대사·보상을 만들지 않았다. 기존 `altar`를 신당에 연결하지 않았다.
- 교회 없음. 이름 없는 주택도 장식 레이어뿐이다.
- 여관 새 아트 `libfile_222a6713fef08191a7bb2487dc1a5c6d`는 사용하지 않았다.

## 소스 근거

- `game/room13_rules.rpy`: R13_PLACES, r13_places, 숙박/사건 조건.
- `game/room13_week2_rules.rpy`: 산길 및 진료실/학교/창고 실제 노드.
- `game/room13_route_knowledge.rpy`: 현재 회차 secret_route_unlocked 필터.
- `game/room13_navigation.rpy`: 장소 표시·선택, R13_LOCAL_CONNECTIONS, 새 발견 필터.
- `game/room13.rpy`: 지도 Return 후 r13_places 재검사 및 r13_edit(location=...). 시간 차감 없음.
- `game/room13_week2.rpy`: finale에서 14일 제단 위치 설정.
