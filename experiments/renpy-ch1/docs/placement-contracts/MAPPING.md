# 데이터 연결표

## 구조

| 데이터 | 책임 | 좌표 수정 시점 |
|---|---|---|
| background_variants | 실제 배경 file/crop/hash, 장소와 시간대, geometry 선택 | 배경 자체가 달라질 때 |
| geometries / slots | 공간 크기, 역할·접촉·방향, anchor target, 비례 기준, 깊이/단차, 가구 mask, 중요 물체 | 해당 가구/자리 구성이 달라질 때 |
| assets | 인물/정확한 포즈, 승인 상태, 원화 hash/canvas/crop/alpha bounds, 신체/소품 anchors, 원화 품질 | 원화나 포즈를 등록할 때 한 번 |
| bindings | 기존 roster 중 누가, 어느 날짜·시간·조건에, 어떤 asset/slot을 쓰는지 | 시나리오 또는 포즈 교체 |
| upstream_guards | 기존 staging의 위치·크기·접촉·가림 14필드 | 기준 소스가 달라진 후 재검증할 때 |

bindings에는 x/y/높이/깊이/가림 좌표를 넣지 않는다. guard는 기존 수정의 되돌림을 막는 이관 스냅샷이며, 새로운 배치 좌표를 작성하는 장소가 아니다.

## 실제 예제

| binding | 공간 | 인물 / 포즈 | 슬롯 접촉 | 일정 필터 |
|---|---|---|---|---|
| inn.morning.nubi | inn.morning, 1920×720 | resident_nubi / map27_in_1 | 발 (420,535), 높이226, 깊이535, 기존 가구 mask | 1~14일 오전, 기존 명단/포즈일 때만 |
| post.morning.sling | post.morning, 2160×720 | resident_sling / map27_po_1 | 소포 아랫면 (1450,548), 높이280 | 1~14일 오전, 기존 명단/포즈일 때만 |
| post.afternoon.sling | post.afternoon, 1280×720 | 같은 인물 / 포즈 | 소포 아랫면 (800,540), 높이290 | 1~14일 오후, 기존 명단/포즈일 때만 |
| post.evening.sling | post.evening, 1280×720 | 같은 인물 / 포즈 | 소포 아랫면 (800,540), 높이290 | 1~14일 저녁, 기존 명단/포즈일 때만 |
| post.afternoon.seryeon | post.afternoon, 1280×720 | seryeon / chair_read | 좌판 (175,562), 좌판→발 세로108, 발 Y670, 깊이674 | 2~14일 오후, 기존 명단/포즈일 때만 |

여관 3개 시간대와 우체국 3개 시간대의 배경을 구분해 등록하지만 여관 binding은 오전 예제만 있다. 기존 출현이 없는 날짜에는 이 표만으로 인물을 생성하지 않는다.

## 원본과 표시 공간

여관 panorama 원본은 각 2048×768이고 기존 공간은 1920×720이다. 우체국 오전 원본은 2160×728이며 crop(0,0,2160,720)을 쓴다. 오후/저녁은 village atlas crop(836,0,836,470)을 기존 1280×720 공간에 표시한다. 인물의 가로·세로를 따로 늘려 배경 변환을 흉내 내지 않는다.

원화 투명 여백은 canvas/crop/alpha_bounds를 구분한다. 같은 원화 재현은 visible_height, 다른 자세는 head_height 또는 vertical_anchor_span 같은 명시한 신체 기준을 쓸 수 있다. 큰 소품 때문에 몸 전체가 작아지지 않도록 새 포즈 검토에서 적절한 기준을 택한다. 크기는 uniform scale을 한 번만 적용한다.

발의 화면 Y와 정렬 depth는 다를 수 있다. 단차는 ground_depth/elevation으로 표현한다. 가구 mask는 공간 좌표, 손/소품 keepout은 원화 좌표에 같은 affine 변환을 적용한다. 렌더와 클릭은 기존 visible-art/alpha 경로를 공유하며 새 사각형 picker를 만들지 않는다.

## 전체 장소 범위

882개 고정 QA 상태는 다음 21개 장소를 포함한다.

`altar`, `ancient`, `clinic`, `dining`, `facility`, `forest`, `gate`, `greenhouse`, `guestroom`, `hall`, `inn`, `kitchen`, `market`, `passage`, `post`, `river`, `room13`, `school`, `square`, `store`, `workshop`.

관찰 기록은 1,520개, 인물46명, 포즈/파일98조합, 장소×인물×포즈145묶음이다. 이 예제의 계약은 3묶음이며 나머지142묶음은 legacy passthrough다. 고정 QA 프로필에서 비어 있는 장소가 모든 이야기 조건에서도 비어 있다는 뜻은 아니다. 원화나 현재 화면 전체의 합격 개수도 아니다.
