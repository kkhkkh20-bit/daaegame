# A. 13호 비밀통로 장치와 열린 객실 상태 제작

## 목표와 범위
신규 PNG 10개를 만든다. 기존 배경 42개를 다시 만들지 않는다. 아빠가 직접 관찰·조작할 수 있는 그림만 제작한다. 범행·할머니 진입·살해 CG는 만들지 않는다. 게임 소스, 대사, 시스템, GitHub 게시를 변경하지 않는다.

기준 소스: main `5e6c2c53ae067b7fc2eb9d10075320587a342f0e` (0.16.2-dev). 개발 소스 ZIP blob `2f0215fcd3acd54b14590ffff6feaba9ab5fe31d`와 로컬 바이트 일치 확인.

최신 소스 루트:
`/workspace/shared/daram_story_asset_plan/source/latest0162/experiments/renpy-ch1`

필수 원문:
- `story-room13/CURRENT_STORY_DECISIONS.txt` 4절: 주방 유지식 스위치 ON → 13호 책장 오른쪽 아래 특정 책 조작 → 숨은 출입구. 안쪽에는 독립 수동 해제 손잡이.
- `game/room13_revision.rpy` 13~68행: 선반 아래 옆으로 미는 덮개, 전선 없는 금속 줄, 올려 걸림턱에 고정되는 레버, 붉은 책 아래를 누르고 옆으로 젖힘. 책장 하부 판이 벽 안쪽으로 밀리고 하강 계단이 보임. 손을 떼면 판은 다시 닫히지만 해제 상태는 유지.
- `game/room13-content.json`: objects.kitchen.shelf, objects.kitchen.rear, objects.room13.books, objects.passage.handle.
- `story-room13/VISUAL_REFERENCE.txt` 34~38행: 방 카메라는 출입문 앞 모서리에서 안을 봄. 정문은 카메라 뒤. 화면 창문은 외벽. 복도 끝13호/오른쪽 경첩/왼쪽 빗장 받이.

## 반드시 먼저 직접 볼 기존 그림
기준 폴더: `/workspace/scratch/6fde33eec4d5/delivery/daram-backgrounds-42-review`
- `kitchen/afternoon.png` (2048×768): 선반·후면 세탁실 문 위치 참조
- `room-before/afternoon.png`, `room-before/morning.png`, `room-before/evening.png` (각2048×768): 객실 전체의 정확한 기준
- `room-after/afternoon.png`: 사건 후 동일 공간과 작은 바닥 탄 자국, 온전한 침대
- `passage/afternoon.png` (2048×768): 계단과 우측 안쪽 손잡이의 형태

그림체: 위에 실제 있는 픽셀풍 원본과 일관된 넓은 색면, 차분한 목재·크림벽, 부드러운 광원, 명확한 물건 실루엣. 미세 자글거림·글자/버튼·인물·범인 표시를 추가하지 않는다. image_gen으로 생성/편집하고 원본 결과를 그대로 보존한다. 파일명이 다르게 나오면 바이트 그대로 복사할 수 있다. 알파가 필요한 요청이 아니므로 불투명 PNG.

## 출력 계약
저장 폴더: `/workspace/shared/daram_story_asset_plan/new_art/mechanisms/`

1. `kitchen-lever-off.png`: 주방 선반 아래 덮개를 옆으로 민 확대 화면. 아래로 내려간 작은 유지식 기계 레버, 느슨한 금속 줄, 걸림턱. 전선·마법·전기등 없음. 옆 찬장/후면문과 같은 목재.
2. `kitchen-lever-on.png`: 1번과 정확히 같은 카메라와 물건. 위로 올려 걸림턱에 걸린 레버와 팽팽한 줄만 변함. 계속 누르는 손 없음. 16:9 확대 권장. 두 장 모두 덮개·레버·줄에 클릭 영역 기록.
3. `book-latch-locked.png`: 기존 객실 우측 책장 하부의 확대. 특정 붉은 책 모양 손잡이와 하부 닫힌 판넬. 책장이 우측이라는 관계와 침대 측 방향이 명확. 작동용 책을 바구니로 가리지 않도록 읽을 수 있는 선택 영역 확보. 기본 원화의 책/바구니 자리 변경이 꼭 필요하면 연속성 수정 제안으로 명시하고 몰래 바꾸지 않는다.
4. `book-latch-open.png`: 3번과 같은 확대 카메라. 붉은 책을 아래쪽 누른 뒤 옆으로 젖힌 위치, 안쪽으로 밀린 하부 판넬, 뒤로 내려가는 좁은 계단의 입구. 출입 가능한 구조여야 하며 마법 포털·정문으로 표현하지 않음. 고정 경첩 회전문으로 바꾸지 않음.
5. `room13-passage-open-morning.png`
6. `room13-passage-open-afternoon.png`
7. `room13-passage-open-evening.png`
  - 5~7은 각 `room-before/{period}.png`를 참조해 편집. 2048×768 가로 구도 유지 요청. 왼쪽 창문, 오른쪽 침대, 오른쪽 끝 책장, 책상·의자·여행짐·매트는 동일한 위치. 책장 하부 입구만 열고 내부가 보이게 함.
  - 외부 정문을 새로 화면 안에 추가하지 않는다. 이 세 장은 사건 전 또는 사건 예방 상태 전용이며, 사건 후 통로 개방에는 사건후 레이어 보존이 추가로 필요함을 명시한다. 사건후 촛대/탄흔이 지워지는 상태 전환을 금지한다.
  - 기준 책장 하부가 너무 좁거나 바구니가 통로를 가린다면 통과 가능 크기의 연속성 문제로 보고하고, 승인 없이 방 전체 구조를 뒤집지 않는다. 가장 실용적 대안은 열림 확대3/4를 메인 화면 위에 표시하고 기존 wide 배경은 유지하는 방식이다.

8. `room13-after-evidence-removed-morning.png`
9. `room13-after-evidence-removed-afternoon.png`
10. `room13-after-evidence-removed-evening.png`
  - 각 `room-after/{period}.png`를 편집해 바닥의 회수된 촛대 두 조각만 제거한 사건 후 재조사 상태. 작은 국소 탄흔, 매트와 온전한 침대, 가구·창·책장 위치는 그대로 유지한다. 새로운 불/연기/피해자/범인/새 핀을 추가하지 않는다.
  - 최신 `game/room13.rpy` 483~493행은 촛대를 회수·봉인하여 E07/E14를 지급한다. 그 후에도 기존 after 배경에 흉기가 남아 보이는 결함을 해결할 그림이다.
  - 시각 상태키 제안: `evidence_removed=true`. 이것은 새로 제안한 키이며 현재 코드에 있다고 주장하지 않는다. Claude가 실제 회수·봉인 사건 뒤의 권위 있는 상태값에 연결해야 한다. 증거를 이미 얻었다는 이유만으로 회수 이전 장면에 소급 적용하면 안 된다.
  - 무삭제 기하학을 생성 파이프라인이 보장할 수 없으므로 창/책상/침대/책장/매트 위치를 기존 참조와 직접 대조하고 변한 부분을 QA에 남긴다. 픽셀 동일 ‘촛대만 제거’를 검증했다고 주장하지 않는다.

## QA/인계
- 생성된 실제 파일을 직접 보고 장치·방 구조·시간대·해상도를 확인한다. 이미지별 권장 클릭 rect(x,y,w,h)를 실제 PNG 좌표로 기록하되 ‘이미지 육안 제안, 런타임 클릭 검증 전’으로 표기한다.
- `manifest.json`: id, file, source_refs, before_after_pair, actual_size, sha256, produced, visual_review, game_applied=false, suggested_hotspots, limitations.
- 같은 상태쌍의 카메라/사물 위치 변화가 있으면 차이를 정확히 적고 일치한다고 주장하지 않는다.
- `QA_KO.md`와 간단 contact sheet/preview를 만들 수 있으나 새로운 원본 자산 개수에 포함하지 않는다.
- 코드 충돌: 최신 runtime은 `secret_route_unlocked=bool(persistent.room13_endings)`로 첫 회차를 막는다. 결정문은 첫 회차 물리 조작을 허용한다. 어느 쪽도 임의로 고치지 말고 Claude 판단사항으로 남긴다. 그림 자체에 회차/챕터 잠금은 그리지 않는다.
