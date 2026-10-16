# 그림 제작 요청서: 장소별 조사 화면 생활·작업 동작 · 0.18.67 기준

작성일: 2026-10-15
기준: `main` 0.18.64(`fd96678`)와 0.18.67 보정 브랜치 `claude/action-fixes`

표시 규칙
- **[확정 요구]**: 지금 대본·일정·배치에서 그대로 나오는 요구다. 제작해도 게임 쪽 결정이 더 필요 없다.
- **[제안]**: 아직 정해지지 않은 것이다. 소유자 결정 전에는 만들지 않아도 된다.

이 문서는 새 사건, 일정, 장소, 해금 조건을 만들지 않는다.

---

## 0. 근거와 좌표

- 배치 근거: 게임 안에서 1~14일 × 오전·오후·저녁 × 모든 장소의 실제 배치를 뽑았다(`r13_stage_people`, 사건 표시 없음, 일정 그대로).
  - 원자료: `reports/art-request-life-actions-20261015/staging-days1-14.json`
  - 뽑은 테스트: `game/qa_tests/tests.rpy`의 `staging_dump`
- 사건 상태 기준
  - 1~4일: 사건 전
  - 5일 이후: 사건 후. 다람이는 5~7일 보호 중, 8일부터 아빠와 함께
  - 8일 이후: 2주차
  - 구금·보호·대피 같은 분기 깃발은 켜지 않은 기본 경로다.
- 행동 문장 근거: `game/room13-dialogue-openings.json`의 `calendar`와 `game/room13-content.json`의 `residents.*.activity`. 게임에 실제로 나오는 `r13_activity_text`를 그대로 옮겼다.
- 좌표
  - 원점: 각 장면 그림의 왼쪽 위
  - 단위: 게임 화면 px. 높이는 모두 720이고, 폭은 장소마다 다르다(2160·1920·1800·1280).
  - 화면에 보이는 위치 = 좌표 x − 카메라 x
  - "발" = 두 발바닥 가운데가 바닥에 닿는 점
  - "표시 키" = 게임에서 그려지는 몸 전체 높이(px)
- 실제 장면 캡처: `reports/art-request-life-actions-20261015/*.jpg`
  - 하늘색 상자는 인물이 차지하는 영역, 빨간 십자는 발 위치다.
  - 아래 띠에 장소·날짜·카메라·배경 파일을 적었다.

## 1. 공통 그림 규격 [확정 요구]

- **목적**
  - 대화용 정면 그림을 줄인 것이 아니다.
  - 하는 일(손에 든 물건, 바닥의 짐)에 시선을 둔 생활 동작이다.
- **체형**
  - 기존 주민의 원래 체형을 유지한다.
    - 새 디자인으로 바뀐 주민(여니·모모 관장·사서 선생님·누비 아주머니·설이·실룩·네로·보리, 토끼 할머니·부엉이 할아버지)은 지금 게임의 대화 그림이 기준이다.
    - 나머지는 원래 그림이 기준이다.
  - 다리를 줄이거나 머리를 키우지 않는다.
  - 31명 일괄 리모델 디자인(`claude/character-remodel-38`)은 쓰지 않는다.
- **화풍**
  - 약간 통통한 동화 느낌으로 그린다.
  - 얼굴 안쪽(눈·코·입)까지 같은 굵기의 도트로 그린다.
  - 자글자글한 미세 무늬, 반투명 잔털, 1px 노이즈는 피한다.
- **파일**
  - 1024×1536 RGBA PNG. 배경은 투명하다.
  - 한 파일에 한 자세만 그린다.
  - 글자, UI, 다른 인물은 넣지 않는다.
- **배율**
  - 선 자세는 지금 그 인물 그림과 같은 배율로 그린다. 예를 들어 누비 아주머니는 원본 1024×1536 기준 선 키가 약 1340px다.
  - 앉거나 웅크린 자세도 같은 배율로 그린다. 키를 선 키에 맞춰 늘이지 않는다. 게임은 선 키에 대한 비율로 크기를 정한다.
- **발**
  - 가장 아래에 보이는 행이 발바닥이다. 아래 여백은 8px 이상 둔다.
  - 바닥에 닿는 소품(장작 등)은 발과 같은 바닥선에 닿게 그린다.
- **소품**
  - 기본은 그림 안에 그린다(자기 완결). 같은 동작을 여러 장소에서 쓰기 때문이다.
  - 벽·가구에 붙는 소품만 별도 투명 레이어로 받는다. 그런 경우는 항목에 따로 적었다.
- **향하는 쪽**
  - 3/4 측면, 일하는 대상 쪽을 본다.
  - 가장 자주 서는 자리에서 장면 가운데를 향하게 한다(항목별 [제안]).
- **함께 줄 것**
  - 원본 px 기준으로 발 중심, 앉는 점(앉은 자세), 바닥 소품 접점, 머리 상자(정수리~턱)를 적은 메모.
- **표시 크기**
  - 각 표의 "표시 키"다. 원본은 대략 1/4~1/6로 줄어 보인다.
  - 손에 든 물건은 표시 키 200px에서도 무엇인지 읽혀야 한다.

## 2. 이미 만든 동작 대조 (중복 생성 방지)

| 묶음 | 인물·동작 | 상태 | 이 문서에서의 처리 |
|---|---|---|---|
| 01823 생활 8종 | 여니 꿰매기(벤치) | 적용(0.18.63 `living_mend`, 승인본 storybook3) | 재사용. 벤치 없는 곳은 5-2 [제안] |
| | 모모 관장 등잔 번호 | 적용(`living_lampnumber`) | 재사용 |
| | 설이 종 줄 | 적용(`living_bellrope`) | 재사용 |
| | 누비 아주머니 빨래 묶기 | **적용 보류**(디자인 균형 재검토). 카탈로그에 후보 경로만 있다(`investigation-first4/nubi_laundry.png`, `investigation-v2/nubi_laundry.png`, `nubi-investigation-v3/nubi-laundry.png`). 상태 "검토 중". **이쪽에 파일이 전달되지 않음** | 3-1. 후보 확인·수정 우선 |
| | 사서 선생님 젖은 책 | 서서 종이 끼우기(`librarian_book.png`) 17:31 수령, 0.18.67 적용(`living_bookpaper`). 앉은 후보 `librarian_seated_v2.png`는 미전달 | 3-5 |
| | 실룩 바퀴 눈 털기 | 바퀴안 제외(17:40 결정). 11~14일 '짐 나누기'로 새로 만든다. `siluk_wheel` 후보는 쓰지 않음 | 3-3 |
| | 네로 이름표 접기 | 수령: `dialogue3-investigation3-handoff.zip` `investigation/resident_nero.png`(원래 이름 `nero-fold-tag.png`). "검토 후보". 옷이 녹색 작업복이라 지금 게임 네로(조끼·모자)와 다름 | 3-4. 수정 또는 대화 그림 교체 결정 |
| | 보리 장작 끈 | 수령: 같은 ZIP `investigation/resident_bori.png`(`bori-firewood.png`). "검토 후보". 새 작업복 대화 그림과 짝 | 3-2. 승인 결정 |
| 사건 7종 | 슬링 김 쐬기, 따닥 문틀, 부리 공구함, 피코 그림 닦기, 뭉치 손 비비기, 사서 장부 묶기, 실룩 귓속말 | 모두 적용(0.18.63). 사건 표시가 떠 있을 때만 쓴다. 따닥 문틀은 여관 평소 동작으로도 쓴다 | 평소 생활 동작으로 다시 쓰지 않는다 |
| 우선 3종 | 토끼 할머니 열쇠·장부, 부엉이 할아버지 수첩, 까로 차축 | 적용 | 재사용(4절) |
| 여니·설이·모모 3종 | 위 01823 세 줄과 같은 파일 | 적용 | — |
| 그 밖에 받은 것(미승인) | batch2~8 "고유 몸짓 검토 후보"(예: `resident_bori_tie_firewood.png`, `resident_nero_tag_fidget.png`, `yeoni-checking-sleeve.png`), 같은 ZIP의 `yeoni-sewing.png`(걸상 포함), 리모델 31명 | 사용자 확정 전 시안. 리모델은 금지 | 쓰지 않는다. 3절 후보와 중복되면 그 후보를 먼저 본다 |

---

## 3. 새 그림 또는 받은 후보의 확인·수정이 필요한 인물

칸 수는 14일 × 3시간대 동안 그 인물이 기본 자세로 서 있는 장면 수다. 우선순위는 칸 수와 장면 사용 빈도로 정했다.

### 3-1. 누비 아주머니 `resident_nubi` · 42칸 · 적용 보류(디자인 균형 재검토 중, 아래는 비교 후보용 명세)

- 현재 그림: `game/assets/room13-redesign-resident_nubi.webp` 기본 자세(대화 그림과 같음)
- 행동 문장
  - "누비는 돌아온 빨랫감의 표를 다시 봤다."
  - "누비는 아직 젖은 천을 묶지 않고 따로 폈다."
  - 01823: "마른 빨랫감을 집별로 묶었다"
- 필요한 동작: 서서 한 팔에 마른 빨랫감 묶음을 받치고, 다른 손으로 끈을 당겨 묶는다. 묶음에 작은 천 이름표.
- 시선: 손의 묶음과 이름표. 고개를 약간 숙인다.
- 소품: 빨랫감 묶음, 끈, 이름표. 그림 안에 그린다.
- 접점: 발 중심만 맞추면 된다. 손 접점은 그림 안에서 끝난다.
- 향하는 쪽 [제안]
  - 여관에서는 왼쪽 끝에 서므로 오른쪽(방 안쪽)을 본다.
  - 다른 장소는 장면 가운데 쪽. 반전 허용 여부를 같이 알려 달라.

| 맵 ID | 배경 파일 | 조건 | 발 (x,y) | 표시 키 | 자리 | 가림 | 캡처 |
|---|---|---|---|---|---|---|---|
| inn (1920) | `room13-pixel-panorama-inn-morning/afternoon.webp` | 1~7일 오전, 8~14일 오후 | (90,681) | 260 | 대기 · 왼쪽 끝 | 앞에 아무도 없음 | `ar_inn_d3p0_c0.jpg` |
| workshop (1800) | `room13-pixel-panorama-workshop-afternoon.webp` | 2·5·6·7일 오후 / 1·3·4일 오후 | (1200,571) / (1425,581) | 220 / 230 | 바닥 · 오른쪽 | 없음 | `ar_workshop_d3p1_c520.jpg` |
| store (1920) | `room13-pixel-ready-store0177-evening.webp` | 1~7일 저녁 | (1116,648) | 324 | 바닥 · 가운데 | 없음 | — |
| facility (1920) | `room13-pixel-ready-facility0177-morning.webp` | 8~14일 오전 | (1696,667) | 253 | 바닥 · 오른쪽 | 없음 | `ar_facility_d9p0_c640.jpg` |
| school (1800) | `room13-pixel-panorama-school-evening.webp` | 8~14일 저녁 | (510,541) | 240 | 책상 뒷줄 | 하반신이 책상 레이어에 가려진다. 동작이 상반신에서 읽혀야 한다 | — |

- 기존 자료: 2절. 카탈로그 후보 `nubi-investigation-v3/nubi-laundry.png`는 무릎 위 바구니 자세라 이 명세와 다르다. 제작팀이 서서 묶는 자세로 수정 제작 중이다.
- **적용 보류 (2026-10-15 17:29 지시)**
  - 누비의 인간형 느낌과 다른 캐릭터와의 균형을 사용자가 다시 검토하고 있다.
  - 새 서서 빨래 동작도 비교용 후보이며, 적용 승인본이 아니다.
  - 예전 디자인 기준도 결정 전이다. 게임의 현재 누비 그림을 자동으로 바꾸지 않고 그대로 보존한다.

### 3-2. 보리 `resident_bori` · P1 · 36칸 [확정 요구]

> **0.18.69 적용**
> - 소유자 승인 `bori-plump-v2-handoff.zip`을 `living_firewood`로 연결했다(조사 화면만).
> - 장소: 마을 입구·공동 창고·광장·수리점.
> - 학교 책상 자리는 기본 자세를 유지한다.

- 현재 그림: `game/assets/room13-redesign-resident_bori.webp` 기본 자세
- 행동 문장
  - "보리는 가져갈 장작을 문 가까이에 모았다."
  - "장작 부스러기를 모아 큰 토막 사이에 넣었다."
  - 01823: "장작 묶음의 끈을 한 번 더 당겼다"
- 필요한 동작: 웅크리거나 한쪽 무릎을 꿇고, 바닥의 장작 묶음 끈을 두 손으로 당겨 조인다.
- 시선: 장작 묶음
- 접점
  - 두 발과 장작 묶음 바닥이 같은 바닥선(발 y)에 닿는다.
  - 장작은 발 앞쪽 몸 폭 안에 둔다. 다른 인물과 겹치지 않게 하기 위해서다.
- 소품: 장작 묶음과 끈. 그림 안에 그린다.
- 향하는 쪽 [제안]: 입구에서는 왼쪽(마을 쪽), 창고에서는 왼쪽(탁자 쪽)

| 맵 ID | 배경 파일 | 조건 | 발 (x,y) | 표시 키(선 키 기준) | 자리 | 가림 | 캡처 |
|---|---|---|---|---|---|---|---|
| gate (1920) | `room13-pixel-ready-gate0173-morning.webp` | 1~3일 오전 | (920,621) | 230 | 바닥 · 가운데 | 없음 | `ar_gate_d2p0_c640.jpg` |
| gate (1920) | `…gate0173-morning/evening.webp` | 5일 오전, 8~14일 저녁 | (1109,651) | 235 | 바닥 | 없음 | — |
| store (1920) | `room13-pixel-ready-store0177-afternoon.webp` | 2·5·8~14일 오후 | (1349,690) | 354 | 바닥 · 오른쪽 | 없음 | `ar_store_d2p1_c640.jpg` |
| store (1920) | `…store0177-morning.webp` | 4·6일 오전 | (1115,648) | 324 | 바닥 | 없음 | — |
| school (1800) | `room13-pixel-panorama-school-morning.webp` | 8~14일 오전, 6일 오후 | (119,526) | 235 | 책상 뒷줄 | 웅크리면 책상에 다 가려진다 | `ar_school_d9p0_c0.jpg` |
| square (1920) | `room13-pixel-panorama-square-evening/afternoon.webp` | 1·4일 저녁 / 7일 오후 | (245,677) / (475,618) | 255 / 234 | 바닥 | 없음 | `ar_square_d1p2_c0.jpg` |
| workshop (1800) | `…workshop-afternoon.webp` | 1·3·4일 오후 | (1199,571) | 220 | 바닥 | 없음 | `ar_workshop_d3p1_c520.jpg` |

- 학교용 [제안]: 장작을 안고 선 자세 1장을 더 받거나, 학교에서만 기본 자세를 유지한다.
- 기존 자료: 받은 `bori-firewood.png`가 있다. 승인하면 바로 넣을 수 있다. 옷은 지금 게임의 파란 재킷과 가깝지만 새 작업복 대화 그림과 짝이라 결정이 필요하다. 신규 생성은 하지 않는다.

### 3-3. 실룩 `resident_siluk` · P1 · 짐 꾸러미 나누기 (2026-10-15 17:40 결정 반영)

- **결정(17:40)**
  - 바퀴 청소안은 제외한다.
  - 배경에 없는 수레를 넣지 않는다. 까로의 마차를 함께 쓰는 해석도 하지 않는다.
  - 기존 11~14일 대사 "실룩은 실을 짐과 먼저 내릴 짐을 나눴다."를 두 손 짐꾸러미 동작으로 만든다.
  - 그 대사가 나오는 장면에만 쓴다. 1~10일 배치·대사·까로 마차는 바꾸지 않는다.
  - 입구 (1779,636) 울타리 위 자리는 제작 기준으로 쓰지 않는다.
- 현재 그림: `game/assets/room13-redesign-resident_siluk.webp` 기본 자세(대화 그림과 같음, 체형 유지)
  - 귓속말(`event_whisper`)은 증언 사건 전용이다.
  - 후보 `siluk_wheel`은 이 동작에 쓰지 않는다.

**대사가 나오는 실제 장면** [확정 사실]

- 확인 방법: `staging_dump`(기본 경로)와 `siluk_late_dump`
  - `siluk_late_dump`는 11~14일 × 시간대 × 장소를, 사람을 옮기는 분기 5종 × 할머니 상태 2종으로 돌렸다.
  - 분기 5종: 없음 / shelter_ready / bami·nubi 보호 / tok 구금 / 재회·환자 이송·대피
- 원점은 장면 그림 왼쪽 위, 단위는 게임 px다.

| 맵 ID (폭) | 배경 파일 | 조건 | 발 (x,y) | 표시 키 | 분기별 |
|---|---|---|---|---|---|
| gate (1920) | `room13-pixel-ready-gate0173-morning.webp` | 11~14일 오전 | (1110,651) | 235 | 모든 분기 같음(40/40) |
| store (1920) | `room13-pixel-ready-store0177-afternoon.webp` | 12~14일 오후, 11일 오후(shelter_ready 등) | (974,544) | 239 | 34/40 |
| store (1920) | 같음 | 11일 오후(기본 분기) | (1518,700) | 347 | 6/40 |

- 저녁에는 입구·창고 어디에도 없다.
- 행동 문장은 장소와 상관없이 날짜로 정해진다. 11~14일에는 두 장소 모두 이 문장이 나온다.

**동작** [확정 요구]

- 서서 두 손에 작은 짐꾸러미를 하나씩 들고, 무게나 이름표를 견주며 나눈다.
  - 끈으로 묶은 천 꾸러미나 종이 꾸러미면 된다.
  - 수레, 바퀴, 상자 더미는 그리지 않는다.
- 시선: 아래쪽 두 꾸러미 사이. 관객을 보지 않는다.
- 향하는 쪽: 3/4 왼쪽을 권한다. 세 자리 모두 장면 가운데가 비교적 왼쪽이다. 좌우 반전 사용 여부를 함께 알려 달라.
- 체형: 지금 실룩 그림과 같은 배율, 같은 비율. 선 자세라 키 비율은 1.0이다.

**손·짐꾸러미가 들어갈 수 있는 범위** (그림 한 장을 세 자리에 함께 쓰므로 세 자리 조건의 공통 범위)

- 표시 기준

| 자리 | 손·꾸러미가 보이는 범위 | 이유 |
|---|---|---|
| 입구 (1110,651) 키 235 | x 985~1175 | 왼쪽 네로(x 838~979), 오른쪽 경비(x 1179~) |
| 창고 (974,544) 키 239 | **x 925~1070, y 380~445** | 그 아래는 뭉치 상자(x ~975 이하, y 450~)와 은호 사장 꼬리(x 980~, y 495~)에, 오른쪽은 은호 몸(x 1080~)에 가린다. 가장 엄격하다 |
| 창고 (1518,700) 키 347 | x 1445~1600 | 뒤쪽 보리(x ~1439), 여니(x 1604~)와 겹치지 않게 |

- 원본 그림 기준으로 바꾼 값
  - 키를 H라 한다. 정수리 = 0, 발바닥 = 1H.
  - **세로**: 두 손과 두 꾸러미가 모두 정수리에서 0.31H~0.59H 사이에 있어야 한다. 가슴~허리 높이다.
  - **가로**: 발 중심에서 왼쪽 0.20H, 오른쪽 0.24H 안. 대략 몸 폭이다.
  - 실룩 선 키는 원본 1024×1536 기준 약 1430px다. 그러므로 세로는 정수리에서 약 445~845px, 가로는 발 중심에서 왼쪽 약 290px·오른쪽 약 345px 안이다.
- 꾸러미 최대 크기
  - 하나에 0.18H × 0.14H 이하(원본 약 260×200px)
  - 표시 크기로는 키 239에서 약 43×33px, 키 347에서 약 62×49px
  - 두 개를 합친 폭은 0.44H 이하
  - 꾸러미끼리 색이나 끈 모양을 달리해, 키 239에서도 두 개로 읽히게 한다.
- 손 접점: 장면 물건과 닿는 곳은 없다. 두 손이 각각 꾸러미를 잡는다(그림 안에서 끝남).
- 발 접점: 두 발바닥 가운데. 가장 아래 보이는 행이 발이고, 아래 여백은 8px 이상이다.

**가림 순서** (뒤 → 앞, 괄호는 발 y)

- 입구: 경비(600) → 네로(621) → **실룩(651)**
  - 실룩이 가장 앞이라 몸이 다 보인다.
  - 까로(615)와 바둑이(오른쪽 1651~1892)는 겹치지 않는다.
- 창고 (974,544): **실룩(544)** → 은호 사장(649) → 뭉치(709) → 백 부인(710)
  - 실룩이 가장 뒤라 무릎 아래와 위 표의 바깥 부분은 가린다.
- 창고 (1518,700): 여니(685) → 보리(690) → **실룩(700)**
  - 실룩이 앞이다.
- 기존 자리 문제(그림과 무관): 창고 첫 카메라(x=320)에서 (1518,700) 자리의 발은 오른쪽 아래 '생각·기록' 버튼에 걸린다. 카메라 x가 약 470 이하일 때 걸리며, 기본 자세에서도 같다.

**배경의 바퀴 조사 결과** (참고, 제작에 쓰지 않음)

- 입구 덮개 마차의 앞바퀴는 중심 (467,539), 반지름 약 52~58이다. 뒷바퀴는 중심 (259,515)이다.
- 창고에는 바퀴가 없다.
- 실룩 자신의 수레는 두 배경 어디에도 없다.
- 그래서 1~10일의 바퀴·수레 대사 장면은 지금처럼 기본 자세로 둔다.

캡처
- `siluk_bundles_gate_d12.jpg`
- `siluk_bundles_store_d12.jpg`
- `siluk_bundles_store_d11.jpg`
- 빨강은 발, 초록은 손·꾸러미가 보이는 범위다. 바퀴 조사 캡처 `siluk_wheel_gate_d9_possible.jpg`, `siluk_wheel_gate_d2_blocked.jpg`는 기록용이다.

### 3-4. 네로 `resident_nero` · P1 · 28칸 [확정 요구]

> **0.18.69 적용**
> - 소유자 승인 `nero-storybook-handoff.zip`을 `living_foldtag`로 연결했다(조사 화면만).
> - 장소: 마을 입구·공동 창고.
> - 대화 그림은 기존 조끼판 그대로다. 대화 의상을 바꿀지는 아직 결정되지 않았다.

- 현재 그림: `game/assets/room13-redesign-resident_nero.webp`(조끼·모자) 기본 자세
- 행동 문장
  - "짐에 붙은 낡은 이름표를 떼어 주머니에 넣는다."
  - "이름표를 손에 쥐었다가 다시 접었다."
  - 01823: "이름표의 젖은 쪽을 안으로 접었다"
- 필요한 동작: 서서 두 손으로 작은 종이 이름표를 반으로 접는다. 허리 가방이나 주머니 쪽.
- 시선: 손의 이름표
- 표시 키 230일 때 이름표는 약 6~8px다. 이름표를 손보다 밝은 색으로 그린다.
- 소품: 이름표. 그림 안에 그린다.

| 맵 ID | 배경 파일 | 조건 | 발 (x,y) | 표시 키 | 자리 | 가림 | 캡처 |
|---|---|---|---|---|---|---|---|
| gate (1920) | `…gate0173-morning.webp` | 4·8~14일 오전 | (919,621) | 230 | 바닥 · 가운데 | 없음 | — |
| gate (1920) | 같음 | 1~3·6·7일 오전 / 5일 오전 | (1109,651) / (1779,636) | 235 / 230 | 바닥 | (1779,636)은 3-3과 같은 울타리 문제 | `ar_gate_d2p0_c640.jpg` |
| store (1920) | `…store0177-afternoon.webp` | 1~3·5~7일 오후 | (216,667) | 338 | 바닥 · 왼쪽 | 없음 | `ar_store_d2p1_c0.jpg` |
| store (1920) | 같음 | 4·8~10·12~14일 / 11일 오후 | (1724,685) / (974,545) | 351 / 250 | 바닥 | 백 부인(1) / 은호·뭉치 | — |

- 기존 자료: 받은 `nero-fold-tag.png`는 녹색 작업복이라 대화 그림과 옷이 다르다. 둘 중 하나를 골라야 한다.
  - 그 후보를 지금 옷(갈색 조끼·흰 셔츠·모자)으로 고친다.
  - 네로 대화 그림을 작업복판으로 바꾼다. 이 경우 새 디자인 적용 범위가 넓어지므로 별도 결정이다.

### 3-5. 사서 선생님 `resident_librarian` · 28칸 · **0.18.67에서 적용 완료**

- 현재 그림: `game/assets/room13-redesign-resident_librarian.webp` 기본 자세. 장부 묶기(`event_ledgertie`)는 b3 사건 전용이다.
- 행동 문장
  - "젖은 책 사이에 마른 종이를 끼운다."
  - "수정 기록을 책 바깥에 붙였다."
  - "펼친 책 밑에 받침을 넣었다."
- 필요한 동작: 서서 한 손에 펼친 책을 받치고, 다른 손으로 마른 종이 한 장을 책장 사이에 끼운다.
- 시선: 책
- 소품: 책, 종이. 그림 안에 그린다.
- 향하는 쪽 [제안]: 우체국 왼쪽 자리에서 오른쪽(방 가운데)을 본다.

| 맵 ID | 배경 파일 | 조건 | 발 (x,y) | 표시 키 | 자리 | 가림 | 캡처 |
|---|---|---|---|---|---|---|---|
| post (2160) | `room13-pixel-wide-post-morning.webp` | 1·8~14일 오전 | (285,636) | 205 | 대기 · 왼쪽 | 없음 | — |
| post (2160) | 같음 | 2~7일 오전 | (480,685) | 230 | 대기 | 3·4·6일은 모모 관장이 앞(585,712)에 선다 | `ar_post_d2p0_c440.jpg`, `ar_post_d3p0_c0.jpg` |
| 옛 우체국 1280 (`winter_post`) | `room13-pixel-village-afternoon.webp` 2×2 묶음의 우체국 칸(위 오른쪽) | 2~14일 오후 / 1일 오후 | (912,586) / (756,591) | 252 / 248 | 카운터 뒤 | 하반신이 카운터에 가려진다. 책과 손은 카운터 위로 보여야 한다 | — |

- 적용 (2026-10-15 17:31 수령·지시)
  - 받은 ZIP: `librarian-standing-book-reuse.zip`, SHA-256 `9701f9a8…e37c`
  - `librarian_book.png`: 1038×1515, SHA-256 `3efbfa5a…b226`. manifest 값과 일치한다.
  - 원본은 `art/librarian-bookpaper-20261015/`에 그대로 두었다. 0.5배로 균일하게 줄여 `living_bookpaper`로 넣었다. 늘이지 않았다.
  - `event_ledgertie`는 b3 사건 전용으로 그대로 둔다.
- 실행 검수(`librarian_bookpaper` 테스트): 세 자리 모두 기본 자세와 발 위치(±1px)·표시 키가 같다.
  - 오전 넓은 우체국 (480,685) 키 230
  - 오전 넓은 우체국 (285,636) 키 205
  - 오후 옛 1280 장면 카운터 (912,586) 키 252. 카운터 가림 마스크는 그대로이고, 책과 손이 카운터 위로 보인다.
- 기존 자리 문제(그림과 무관): 2~7일 오전 자리 (480,685)는 카메라 440에서 화면 왼쪽 끝이다. 발이 왼쪽 아래 '조사 중' 표시 가까이에 온다. 기본 자세에서도 같다.
- 앉은 자세 후보(`librarian_seated_v2.png`)는 지금 자리가 대기·카운터라 그대로 쓸 수 없다.

### 3-6. 여니 `resident_yeoni` 선 자세 변형 · P2 · 18칸 [제안]

- 지금 꿰매기(`living_mend`)는 벤치에 앉는 자세라 광장 벤치에서만 쓴다.
- 나머지 장소에서는 기본 자세로 서 있다.

| 맵 ID | 조건 | 발 (x,y) | 표시 키 | 자리 |
|---|---|---|---|---|
| inn (1920) | 2·3·9·10·13일 오후 / 6일 오후 | (485,707) / (94,681) | 265 / 260 | 대기 |
| workshop (1800) | 11일 오전, 5·8·12일 오후 / 4일 오전, 1일 오후 | (1425,581) / (1700,706) | 230 / 280 | 바닥 |
| store (1920) | 13일 오전, 4일 오후 / 6일 오전 / 11일 오후 | (216,667) / (1349,690) / (1724,685) | 338 / 354 / 351 | 바닥 |
| school (1800) | 7·14일 오후 | (120,526) | 235 | 책상 뒷줄 |

- 필요한 동작 [제안]: 서서 벌어진 소매를 뒤집어 바늘을 꽂는다. 행동 문장은 "벌어진 소매를 접어 바늘을 꽂았다", "작은 천 조각까지 모아 접었다".
- 기존 자료: 받은 `yeoni-sewing.png`는 걸상을 그림 안에 포함한 꿰매기 자세다. 승인되면 걸상째 어디서나 쓸 수 있어 새로 만들 필요가 없다. 승인 여부를 정해 달라.

### 3-7. 피코 `resident_piko` 임시 진료실 · 21칸 · 결정 필요

- 8일 이후 진료실에 있다. 지금은 `distressed` 자세로 서 있다.
- 카탈로그 인계문도 "누운 환자라는 근거가 없다"고 적었다.
- 대본에서 역할(환자·간병·대기)이 정해져야 동작을 정할 수 있다. 정해지기 전에는 만들지 않는다.

---

## 4. 새 그림 없이 기존 그림을 다시 쓸 수 있는 인물 [확정 요구, 그림 제작 불필요]

- 원인
  - 지도 대기 자리(waiting)·카운터·책상 뒷줄에 서면 코드가 자세를 기본으로 바꾼다(`game/room13_acting.rpy` 411행).
  - 그래서 생활 동작 그림이 있는데도 기본 자세로 보인다.
- 처리
  - 제작팀이 새로 그릴 필요는 없다. 배치 규칙만 연결하면 된다(0.18.63의 모모 관장 `slot_actions`와 같은 방식).
  - 이번 0.18.67 배포 범위에는 넣지 않는다.
- 주의
  - 웅크리거나 무릎 꿇은 동작은 카운터·책상 뒷줄 자리에서 가려진다. 그 자리에서는 기본 자세를 유지한다.

> **0.18.69 연결**
> - 11명: 슬링·도토·구슬·뿔이 촌장·우박·은호 사장·백 부인·서리 검사원·부엉이 할아버지·모모 관장·세련.
> - 연결하지 않은 2명
>   - 콩이: 웅크린 그림이 계산대 뒤에 가려진다.
>   - 톡: 앉은 그림인데 그 자리에 의자가 없다.
> - 자세한 내용: `docs/releases/RELEASE_01869.md`.

| 인물 | 이미 있는 동작(파일) | 맞는 행동 문장 | 기본 자세로 보이는 곳(칸) | 재사용 가능한 자리 |
|---|---|---|---|---|
| 슬링 `resident_sling` | `activity` 무릎 꿇고 우편 가방 봉투 나누기(`room13-pixel-acting-resident_sling.webp`) | "배달할 봉투와 돌아온 봉투를 나눴다" | 우체국 36 | 넓은 우체국 오전 대기 자리. 옛 1280 오후 카운터는 가림 |
| 도토 `doto` | `action_1` 서서 수첩에 적기 / `action_2` 앉아 책 읽기 | "쓰던 줄을 끝내고 빈칸을 남겼다" | 2층 복도 30 | 복도 (1471,616) |
| 구슬 `resident_guseul` | `living_stamp` 도장 닦기(선 자세) | "계약서에 눌린 도장을 닦아 낸다" | 우체국 14, 여관 14 | 대기 자리 |
| 뿔이 촌장 `resident_ppul` | `activity` 몸 굽혀 종이 묶음 정리 | "쌓인 종이를 한 장씩 나눴다" | 우체국 22 | 대기 자리 |
| 우박 `resident_ubak` | `living_measure` 웅크려 계측기 기록 | "계측기 바늘과 종이 눈금을 맞춘다" | 여관 14, 수리점 7 | 바닥·대기 자리만 |
| 은호 사장 `resident_eunho` | `living_prices` 장부에 값 적기 | "물자 목록 옆에 값을 다시 적는다" | 우체국 7, 여관 7 | 대기 자리 |
| 백 부인 `resident_madam` | `living_inspect` 보관함 살피기 | "보관함을 봉해 둔 자리를 다시 만졌다" | 여관 14 | 대기 자리 |
| 콩이 `resident_kongi` | `activity` 웅크려 빵 바구니 | "빵 꾸러미를 작은 것부터 모았다" | 우체국 14 | 대기 자리 |
| 톡 `resident_tok` | `activity` 앉아서 부품 손질(seat) | "작은 핀을 집게로 물고 살핀다" | 식당 7, 학교 7 | 의자가 있는 자리만 |
| 서리 검사원 `resident_seori` | `living_notes` 서서 기록 | "오늘 확인한 줄을 적었다" | 학교 7 | 책상 뒷줄은 상반신만 보임 |
| 부엉이 할아버지 `resident_owlgp` | `living_notebook` 접이 의자에 앉아 수첩 묶기(의자 포함) | "풀린 수첩을 다시 묶었다" | 여관 4, 식당 4 | 바닥·대기 자리 |
| 모모 관장 `resident_momo` | `living_lampnumber` | "등잔 바닥 번호를 읽는다" | 옛 1280 우체국 오후 카운터 14 | 카운터라 하반신 가림. 상반신 동작은 보임 |
| 세련 `seryeon` | `action_1` 서서 클립보드에 적기(우체국 오전), `chair_read`(오후 의자) | "돌아온 봉투의 이름을 다시 확인했다" | 넓은 우체국 오전 대기 자리 (90,675) 13 | 오전 대기 자리 |

---

## 5. 이미 생활 동작이 정상으로 보이는 인물 (추가 제작 불필요)

- 토끼 할머니(여관), 부엉이 할아버지(광장), 까로(입구), 설이(광장), 모모 관장(넓은 우체국 오전), 여니(광장 벤치)
- 바둑이, 등불지기 아저씨, 피코(광장), 솜이, 서리(진료실)
- 우박(진료실·수리점 일부), 따닥, 무쇠 할아버지, 구슬(창고), 은호(창고), 뭉치(창고), 백 부인(창고)
- 선생님, 톡(수리점), 꽥순, 콩이(창고), 토리, 부리, 나비, 경비, 너울, 밤이

## 6. 결정되지 않은 것 [제안 · 제작 보류]

- **큰 강·깊은 숲·장터 주민 일정**
  - `docs/ART_REQUEST_01854_PLACES.md`의 '올 주민' 목록이 있다.
    - 강가: 꽥순·네로·무쇠 할아버지
    - 숲속: 바둑이·보리·실룩
    - 장터: 은호 사장·구슬·콩이·누비 아주머니·여니
  - 날짜·시간대가 정해지지 않아 지금 세 장소에는 아무도 없다.
  - 일정이 정해지면 다음 순서로 진행한다.
    - 1~5절의 동작을 다시 쓸 수 있는지 먼저 본다. 예: 장터 은호 `living_prices`, 구슬 `living_stamp`, 콩이 빵 바구니.
    - 낚시·사냥처럼 그 장소에만 있는 동작은 그때 새로 요청한다.
  - 지금은 만들지 않는다.
- **지하 초고대 돌 제작 시설**: 진입 지도, 해금 조건, 입구 연결이 미정이라 이 문서에서 다루지 않는다.
- **피코 진료실 역할(3-7)**, **네로 옷(3-4)**, **보리·여니 후보 승인(3-2, 3-6)**, **입구 울타리 자리(3-3)**: 소유자 결정 대상이다.
- 다람이·아빠: 제작 금지(카탈로그 "hold")라 목록에서 뺐다.

---

## 부록 A. 기본 자세로 서 있는 모든 칸 (자동 추출)

- 출처: `staging-days1-14.json`(사서 선생님 적용 전, 0.18.67 작업 중에 추출). 다람이·아빠는 뺐다.
- "자리"
  - 대기·카운터·책상 뒷줄은 코드가 기본 자세를 쓰는 구역이다.
  - "바닥"은 그 인물의 생활 동작이 그 장소에 허용되지 않았거나, 그림이 없는 경우다.
- "앞에 서는 사람": 같은 장면에서 이 인물 앞(더 아래쪽)에 겹쳐 서는 사람과 그 횟수다.
- "좌우": 장면 폭을 셋으로 나눈 위치다.

| 인물 | 맵 ID | 폭 | 조건 | 발 (x,y) | 표시 키 | 자리 | 좌우 | 앞에 서는 사람 | 배경 파일 | 현재 그림 | 칸 수 | 처리 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 도토 `doto` | hall | 2160 | 5~14일 오전; 5~14일 오후; 5~14일 저녁 | (1471,616) | 238 | 대기 | 오른쪽 | 없음 | room13-pixel-wide-hall-after-afternoon.webp, room13-pixel-wide-hall-after-evening.webp, room13-pixel-wide-hall-after-morning.webp | room13-pixel-acting-doto.webp | 30 | 재사용(4절) |
| 보리 `resident_bori` | gate | 1920 | 5일 오전; 8~14일 저녁 | (1109,651) | 235 | 바닥 | 가운데 | 없음 | room13-pixel-ready-gate0173-evening.webp, room13-pixel-ready-gate0173-morning.webp | room13-redesign-resident_bori.webp | 8 | P1 후보승인(3-2) |
| 보리 `resident_bori` | gate | 1920 | 1~3일 오전 | (920,621) | 230 | 바닥 | 가운데 | 없음 | room13-pixel-ready-gate0173-morning.webp | room13-redesign-resident_bori.webp | 3 | P1 후보승인(3-2) |
| 보리 `resident_bori` | school | 1800 | 8~14일 오전; 6일 오후 | (119,526) | 235 | 책상 뒷줄(하반신 가림) | 왼쪽 | 없음 | room13-pixel-panorama-school-afternoon.webp, room13-pixel-panorama-school-morning.webp | room13-redesign-resident_bori.webp | 8 | P1 후보승인(3-2) |
| 보리 `resident_bori` | square | 1920 | 1,4일 저녁 | (245,677) | 255 | 바닥 | 왼쪽 | 없음 | room13-pixel-panorama-square-evening.webp | room13-redesign-resident_bori.webp | 2 | P1 후보승인(3-2) |
| 보리 `resident_bori` | square | 1920 | 7일 오후 | (475,618) | 234 | 바닥 | 왼쪽 | 없음 | room13-pixel-panorama-square-afternoon.webp | room13-redesign-resident_bori.webp | 1 | P1 후보승인(3-2) |
| 보리 `resident_bori` | store | 1920 | 2,5,8~14일 오후 | (1349,690) | 354 | 바닥 | 오른쪽 | 없음 | room13-pixel-ready-store0177-afternoon.webp | room13-redesign-resident_bori.webp | 9 | P1 후보승인(3-2) |
| 보리 `resident_bori` | store | 1920 | 4,6일 오전 | (1115,648) | 324 | 바닥 | 가운데 | 없음 | room13-pixel-ready-store0177-morning.webp | room13-redesign-resident_bori.webp | 2 | P1 후보승인(3-2) |
| 보리 `resident_bori` | workshop | 1800 | 1,3~4일 오후 | (1199,571) | 220 | 바닥 | 가운데 | 없음 | room13-pixel-panorama-workshop-afternoon.webp | room13-redesign-resident_bori.webp | 3 | P1 후보승인(3-2) |
| 은호 사장 `resident_eunho` | inn | 1920 | 1~7일 저녁 | (5,682) | 260 | 대기 | 왼쪽 | 없음 | room13-pixel-panorama-inn-evening.webp | room13-pixel-acting-eunho.webp | 7 | 재사용(4절) |
| 은호 사장 `resident_eunho` | post | 2160 | 2~7일 오전 | (212,636) | 205 | 대기 | 왼쪽 | 없음 | room13-pixel-wide-post-morning.webp | room13-pixel-acting-eunho.webp | 6 | 재사용(4절) |
| 은호 사장 `resident_eunho` | post | 2160 | 1일 오전 | (12,676) | 220 | 대기 | 왼쪽 | 없음 | room13-pixel-wide-post-morning.webp | room13-pixel-acting-eunho.webp | 1 | 재사용(4절) |
| 구슬 `resident_guseul` | inn | 1920 | 1~6,14일 저녁 | (1002,541) | 216 | 대기 | 가운데 | 없음 | room13-pixel-panorama-inn-evening.webp | room13-pixel-acting-guseul.webp | 7 | 재사용(4절) |
| 구슬 `resident_guseul` | inn | 1920 | 8~13일 저녁 | (804,621) | 238 | 대기 | 가운데 | 없음 | room13-pixel-panorama-inn-evening.webp | room13-pixel-acting-guseul.webp | 6 | 재사용(4절) |
| 구슬 `resident_guseul` | inn | 1920 | 7일 저녁 | (1171,611) | 245 | 대기 | 가운데 | 없음 | room13-pixel-panorama-inn-evening.webp | room13-pixel-acting-guseul.webp | 1 | 재사용(4절) |
| 구슬 `resident_guseul` | post | 1280 | 3,5,7~8,10,12,14일 오후 | (834,558) | 216 | 카운터 뒤(하반신 가림) | 가운데 | 사서 선생님(7) | winter_post | room13-pixel-acting-guseul.webp | 7 | 재사용(4절) |
| 구슬 `resident_guseul` | post | 1280 | 2,4,6,9,11,13일 오후 | (334,590) | 220 | 카운터 뒤(하반신 가림) | 왼쪽 | 없음 | winter_post | room13-pixel-acting-guseul.webp | 6 | 재사용(4절) |
| 구슬 `resident_guseul` | post | 1280 | 1일 오후 | (493,608) | 238 | 카운터 뒤(하반신 가림) | 가운데 | 콩이(1) | winter_post | room13-pixel-acting-guseul.webp | 1 | 재사용(4절) |
| 콩이 `resident_kongi` | post | 1280 | 2~14일 오후 | (579,608) | 238 | 카운터 뒤(하반신 가림) | 가운데 | 없음 | winter_post | room13-pixel-acting-resident_kongi.webp | 13 | 재사용(4절) |
| 콩이 `resident_kongi` | post | 1280 | 1일 오후 | (414,619) | 256 | 카운터 뒤(하반신 가림) | 왼쪽 | 없음 | winter_post | room13-pixel-acting-resident_kongi.webp | 1 | 재사용(4절) |
| 사서 선생님 `resident_librarian` | post | 1280 | 2~14일 오후 | (912,586) | 252 | 카운터 뒤(하반신 가림) | 오른쪽 | 없음 | winter_post | room13-redesign-resident_librarian.webp | 13 | 0.18.67 적용 완료(3-5) |
| 사서 선생님 `resident_librarian` | post | 2160 | 1,8~14일 오전 | (285,636) | 205 | 대기 | 왼쪽 | 없음 | room13-pixel-wide-post-morning.webp | room13-redesign-resident_librarian.webp | 8 | 0.18.67 적용 완료(3-5) |
| 사서 선생님 `resident_librarian` | post | 2160 | 2~7일 오전 | (479,686) | 230 | 대기 | 왼쪽 | 모모 관장(3) | room13-pixel-wide-post-morning.webp | room13-redesign-resident_librarian.webp | 6 | 0.18.67 적용 완료(3-5) |
| 사서 선생님 `resident_librarian` | post | 1280 | 1일 오후 | (756,591) | 248 | 카운터 뒤(하반신 가림) | 가운데 | 없음 | winter_post | room13-redesign-resident_librarian.webp | 1 | 0.18.67 적용 완료(3-5) |
| 백 부인 `resident_madam` | inn | 1920 | 1~7일 저녁 | (397,708) | 265 | 대기 | 왼쪽 | 없음 | room13-pixel-panorama-inn-evening.webp | room13-pixel-acting-madam.webp | 7 | 재사용(4절) |
| 백 부인 `resident_madam` | inn | 1920 | 8~14일 저녁 | (5,682) | 260 | 대기 | 왼쪽 | 없음 | room13-pixel-panorama-inn-evening.webp | room13-pixel-acting-madam.webp | 7 | 재사용(4절) |
| 모모 관장 `resident_momo` | post | 1280 | 2~14일 오후 | (755,562) | 213 | 카운터 뒤(하반신 가림) | 가운데 | 없음 | winter_post | room13-redesign-resident_momo.webp | 13 | 재사용(4절) |
| 모모 관장 `resident_momo` | post | 1280 | 1일 오후 | (912,586) | 252 | 카운터 뒤(하반신 가림) | 오른쪽 | 없음 | winter_post | room13-redesign-resident_momo.webp | 1 | 재사용(4절) |
| 네로 `resident_nero` | gate | 1920 | 4,8~14일 오전 | (919,621) | 230 | 바닥 | 가운데 | 없음 | room13-pixel-ready-gate0173-morning.webp | room13-redesign-resident_nero.webp | 8 | P1 후보수정(3-4) |
| 네로 `resident_nero` | gate | 1920 | 1~3,6~7일 오전 | (1109,651) | 235 | 바닥 | 가운데 | 없음 | room13-pixel-ready-gate0173-morning.webp | room13-redesign-resident_nero.webp | 5 | P1 후보수정(3-4) |
| 네로 `resident_nero` | gate | 1920 | 5일 오전 | (1779,636) | 230 | 바닥 | 오른쪽 | 없음 | room13-pixel-ready-gate0173-morning.webp | room13-redesign-resident_nero.webp | 1 | P1 후보수정(3-4) |
| 네로 `resident_nero` | store | 1920 | 4,8~10,12~14일 오후 | (1724,685) | 351 | 바닥 | 오른쪽 | 백 부인(1) | room13-pixel-ready-store0177-afternoon.webp | room13-redesign-resident_nero.webp | 7 | P1 후보수정(3-4) |
| 네로 `resident_nero` | store | 1920 | 1~3,5~7일 오후 | (216,667) | 338 | 바닥 | 왼쪽 | 없음 | room13-pixel-ready-store0177-afternoon.webp | room13-redesign-resident_nero.webp | 6 | P1 후보수정(3-4) |
| 네로 `resident_nero` | store | 1920 | 11일 오후 | (974,545) | 250 | 바닥 | 가운데 | 은호 사장(1), 뭉치(1) | room13-pixel-ready-store0177-afternoon.webp | room13-redesign-resident_nero.webp | 1 | P1 후보수정(3-4) |
| 누비 아주머니 `resident_nubi` | facility | 1920 | 8~14일 오전 | (1696,667) | 253 | 바닥 | 오른쪽 | 없음 | room13-pixel-ready-facility0177-morning.webp | room13-redesign-resident_nubi.webp | 7 | 적용 보류 · 비교 후보(3-1) |
| 누비 아주머니 `resident_nubi` | inn | 1920 | 1~7일 오전; 8~14일 오후 | (90,681) | 260 | 대기 | 왼쪽 | 없음 | room13-pixel-panorama-inn-afternoon.webp, room13-pixel-panorama-inn-morning.webp | room13-redesign-resident_nubi.webp | 14 | 적용 보류 · 비교 후보(3-1) |
| 누비 아주머니 `resident_nubi` | school | 1800 | 8~14일 저녁 | (510,541) | 240 | 책상 뒷줄(하반신 가림) | 왼쪽 | 없음 | room13-pixel-panorama-school-evening.webp | room13-redesign-resident_nubi.webp | 7 | 적용 보류 · 비교 후보(3-1) |
| 누비 아주머니 `resident_nubi` | store | 1920 | 1~7일 저녁 | (1116,648) | 324 | 바닥 | 가운데 | 없음 | room13-pixel-ready-store0177-evening.webp | room13-redesign-resident_nubi.webp | 7 | 적용 보류 · 비교 후보(3-1) |
| 누비 아주머니 `resident_nubi` | workshop | 1800 | 2,5~7일 오후 | (1200,571) | 220 | 바닥 | 가운데 | 없음 | room13-pixel-panorama-workshop-afternoon.webp | room13-redesign-resident_nubi.webp | 4 | 적용 보류 · 비교 후보(3-1) |
| 누비 아주머니 `resident_nubi` | workshop | 1800 | 1,3~4일 오후 | (1425,581) | 230 | 바닥 | 오른쪽 | 없음 | room13-pixel-panorama-workshop-afternoon.webp | room13-redesign-resident_nubi.webp | 3 | 적용 보류 · 비교 후보(3-1) |
| 부엉이 할아버지 `resident_owlgp` | dining | 2160 | 1~4일 저녁 | (539,681) | 260 | 고정 자리 | 왼쪽 | 없음 | room13-pixel-wide-dining-evening.webp | room13-redesign-resident_owlgp.webp | 4 | 재사용(4절) |
| 부엉이 할아버지 `resident_owlgp` | inn | 1920 | 1~4일 오후 | (89,681) | 260 | 대기 | 왼쪽 | 없음 | room13-pixel-panorama-inn-afternoon.webp | room13-redesign-resident_owlgp.webp | 4 | 재사용(4절) |
| 피코 `resident_piko` | clinic | 1920 | 8~14일 오후; 8~14일 저녁 | (1607,654) | 244 | 바닥 | 오른쪽 | 없음 | room13-pixel-ready-clinic0177-afternoon.webp, room13-pixel-ready-clinic0177-evening.webp | room13-pixel-acting-piko.webp [distressed] | 14 | 결정 필요(3-7) |
| 피코 `resident_piko` | clinic | 1920 | 8~14일 오전 | (182,658) | 244 | 바닥 | 왼쪽 | 없음 | room13-pixel-ready-clinic0177-morning.webp | room13-pixel-acting-piko.webp [distressed] | 7 | 결정 필요(3-7) |
| 뿔이 촌장 `resident_ppul` | post | 1280 | 2~14일 오후 | (1108,561) | 245 | 카운터 뒤(하반신 가림) | 오른쪽 | 없음 | winter_post | room13-pixel-acting-resident_ppul.webp | 13 | 재사용(4절) |
| 뿔이 촌장 `resident_ppul` | post | 2160 | 1,8,10~11,13일 오전 | (479,686) | 230 | 대기 | 왼쪽 | 없음 | room13-pixel-wide-post-morning.webp | room13-pixel-acting-resident_ppul.webp | 5 | 재사용(4절) |
| 뿔이 촌장 `resident_ppul` | post | 2160 | 3~4,6일 오전 | (869,691) | 230 | 대기 | 가운데 | 없음 | room13-pixel-wide-post-morning.webp | room13-pixel-acting-resident_ppul.webp | 3 | 재사용(4절) |
| 뿔이 촌장 `resident_ppul` | post | 1280 | 1일 오후 | (1109,590) | 285 | 카운터 뒤(하반신 가림) | 오른쪽 | 없음 | winter_post | room13-pixel-acting-resident_ppul.webp | 1 | 재사용(4절) |
| 서리 검사원 `resident_seori` | school | 1800 | 8~14일 저녁 | (242,536) | 240 | 책상 뒷줄(하반신 가림) | 왼쪽 | 없음 | room13-pixel-panorama-school-evening.webp | room13-pixel-acting-seori.webp | 7 | 재사용(4절) |
| 실룩 `resident_siluk` | gate | 1920 | 4,8~14일 오전 | (1110,651) | 235 | 바닥 | 가운데 | 없음 | room13-pixel-ready-gate0173-morning.webp | room13-redesign-resident_siluk.webp | 8 | P1 11~14일만 짐 나누기(3-3) |
| 실룩 `resident_siluk` | gate | 1920 | 1~3,6~7일 오전 | (1779,636) | 230 | 바닥 | 오른쪽 | 없음 | room13-pixel-ready-gate0173-morning.webp | room13-redesign-resident_siluk.webp | 5 | 기본 자세 유지(3-3) |
| 실룩 `resident_siluk` | gate | 1920 | 5일 오전 | (1250,691) | 245 | 바닥 | 가운데 | 없음 | room13-pixel-ready-gate0173-morning.webp | room13-redesign-resident_siluk.webp | 1 | 기본 자세 유지(3-3) |
| 실룩 `resident_siluk` | store | 1920 | 2,5,8~10,12~14일 오후 | (974,544) | 239 | 바닥 | 가운데 | 은호 사장(8), 뭉치(6), 백 부인(2) | room13-pixel-ready-store0177-afternoon.webp | room13-redesign-resident_siluk.webp | 8 | P1 11~14일만 짐 나누기(3-3) |
| 실룩 `resident_siluk` | store | 1920 | 1,3~4,6~7일 오후 | (1349,690) | 339 | 바닥 | 오른쪽 | 백 부인(1) | room13-pixel-ready-store0177-afternoon.webp | room13-redesign-resident_siluk.webp | 5 | 기본 자세 유지(3-3) |
| 실룩 `resident_siluk` | store | 1920 | 11일 오후 | (1518,700) | 347 | 바닥 | 오른쪽 | 없음 | room13-pixel-ready-store0177-afternoon.webp | room13-redesign-resident_siluk.webp | 1 | P1 11~14일만 짐 나누기(3-3) |
| 슬링 `resident_sling` | post | 1280 | 1~14일 저녁 | (830,677) | 281 | 고정 자리 | 가운데 | 없음 | winter_post | room13-pixel-acting-resident_sling.webp | 14 | 재사용(4절) |
| 슬링 `resident_sling` | post | 2160 | 1~2,5,7~8,10~11,13일 오전 | (869,691) | 230 | 대기 | 가운데 | 없음 | room13-pixel-wide-post-morning.webp | room13-pixel-acting-resident_sling.webp | 8 | 재사용(4절) |
| 슬링 `resident_sling` | post | 1280 | 3,5,7~8,10,12,14일 오후 | (414,590) | 220 | 카운터 뒤(하반신 가림) | 왼쪽 | 없음 | winter_post | room13-pixel-acting-resident_sling.webp | 7 | 재사용(4절) |
| 슬링 `resident_sling` | post | 2160 | 3~4,6일 오전 | (1060,621) | 205 | 대기 | 가운데 | 없음 | room13-pixel-wide-post-morning.webp | room13-pixel-acting-resident_sling.webp | 3 | 재사용(4절) |
| 슬링 `resident_sling` | post | 2160 | 9,12,14일 오전 | (479,686) | 230 | 대기 | 왼쪽 | 없음 | room13-pixel-wide-post-morning.webp | room13-pixel-acting-resident_sling.webp | 3 | 재사용(4절) |
| 슬링 `resident_sling` | post | 1280 | 1일 오후 | (126,651) | 250 | 바닥 | 왼쪽 | 없음 | winter_post | room13-pixel-acting-resident_sling.webp | 1 | 재사용(4절) |
| 톡 `resident_tok` | dining | 2160 | 1~4일 저녁 | (134,692) | 265 | 고정 자리 | 왼쪽 | 없음 | room13-pixel-wide-dining-evening.webp | room13-pixel-acting-resident_tok.webp | 4 | 재사용(4절) |
| 톡 `resident_tok` | dining | 2160 | 5~7일 저녁 | (539,682) | 260 | 고정 자리 | 왼쪽 | 없음 | room13-pixel-wide-dining-evening.webp | room13-pixel-acting-resident_tok.webp | 3 | 재사용(4절) |
| 톡 `resident_tok` | school | 1800 | 8~14일 저녁 | (119,526) | 235 | 책상 뒷줄(하반신 가림) | 왼쪽 | 없음 | room13-pixel-panorama-school-evening.webp | room13-pixel-acting-resident_tok.webp | 7 | 재사용(4절) |
| 따닥 `resident_ttadak` | workshop | 1800 | 4일 오전 | (196,548) | 215 | doorfloor | 왼쪽 | 톡(1) | room13-pixel-panorama-workshop-morning.webp | room13-pixel-acting-ttadak.webp | 1 | 재사용(4절) |
| 우박 `resident_ubak` | inn | 1920 | 8~14일 저녁 | (398,708) | 265 | 대기 | 왼쪽 | 없음 | room13-pixel-panorama-inn-evening.webp | room13-pixel-acting-ubak.webp | 7 | 재사용(4절) |
| 우박 `resident_ubak` | inn | 1920 | 1~6일 저녁 | (812,621) | 238 | 대기 | 가운데 | 없음 | room13-pixel-panorama-inn-evening.webp | room13-pixel-acting-ubak.webp | 6 | 재사용(4절) |
| 우박 `resident_ubak` | inn | 1920 | 7일 저녁 | (1009,541) | 216 | 대기 | 가운데 | 없음 | room13-pixel-panorama-inn-evening.webp | room13-pixel-acting-ubak.webp | 1 | 재사용(4절) |
| 우박 `resident_ubak` | workshop | 1800 | 1~3,5~7,11일 오전 | (199,548) | 215 | doorfloor | 왼쪽 | 톡(7) | room13-pixel-panorama-workshop-morning.webp | room13-pixel-acting-ubak.webp | 7 | 재사용(4절) |
| 여니 `resident_yeoni` | inn | 1920 | 2~3,9~10,13일 오후 | (485,707) | 265 | 대기 | 왼쪽 | 없음 | room13-pixel-panorama-inn-afternoon.webp | room13-redesign-resident_yeoni.webp | 5 | P2 [제안](3-6) |
| 여니 `resident_yeoni` | inn | 1920 | 6일 오후 | (94,681) | 260 | 대기 | 왼쪽 | 없음 | room13-pixel-panorama-inn-afternoon.webp | room13-redesign-resident_yeoni.webp | 1 | P2 [제안](3-6) |
| 여니 `resident_yeoni` | school | 1800 | 7,14일 오후 | (120,526) | 235 | 책상 뒷줄(하반신 가림) | 왼쪽 | 없음 | room13-pixel-panorama-school-afternoon.webp | room13-redesign-resident_yeoni.webp | 2 | P2 [제안](3-6) |
| 여니 `resident_yeoni` | store | 1920 | 13일 오전; 4일 오후 | (216,667) | 338 | 바닥 | 왼쪽 | 없음 | room13-pixel-ready-store0177-afternoon.webp, room13-pixel-ready-store0177-morning.webp | room13-redesign-resident_yeoni.webp | 2 | P2 [제안](3-6) |
| 여니 `resident_yeoni` | store | 1920 | 6일 오전 | (1349,690) | 354 | 바닥 | 오른쪽 | 없음 | room13-pixel-ready-store0177-morning.webp | room13-redesign-resident_yeoni.webp | 1 | P2 [제안](3-6) |
| 여니 `resident_yeoni` | store | 1920 | 11일 오후 | (1724,685) | 351 | 바닥 | 오른쪽 | 없음 | room13-pixel-ready-store0177-afternoon.webp | room13-redesign-resident_yeoni.webp | 1 | P2 [제안](3-6) |
| 여니 `resident_yeoni` | workshop | 1800 | 11일 오전; 5,8,12일 오후 | (1425,581) | 230 | 바닥 | 오른쪽 | 무쇠 할아버지(1) | room13-pixel-panorama-workshop-afternoon.webp, room13-pixel-panorama-workshop-morning.webp | room13-redesign-resident_yeoni.webp | 4 | P2 [제안](3-6) |
| 여니 `resident_yeoni` | workshop | 1800 | 4일 오전; 1일 오후 | (1700,706) | 280 | 바닥 | 오른쪽 | 없음 | room13-pixel-panorama-workshop-afternoon.webp, room13-pixel-panorama-workshop-morning.webp | room13-redesign-resident_yeoni.webp | 2 | P2 [제안](3-6) |
| 세련 `seryeon` | post | 2160 | 2~14일 오전 | (90,675) | 220 | 대기 | 왼쪽 | 없음 | room13-pixel-wide-post-morning.webp | room13-pixel-acting-seryeon.webp | 13 | 재사용(4절) |

## 부록 B. 캡처 목록

경로: `reports/art-request-life-actions-20261015/`. 1280×720 실제 게임 화면이다. 하늘색 상자는 인물 영역, 빨간 십자는 발 위치다.

| 파일 | 장면 | 보이는 대상 |
|---|---|---|
| `ar_inn_d3p0_c0.jpg` | 여관 접수대 3일 오전, 카메라 0 | 누비 아주머니 (90,681) |
| `ar_gate_d2p0_c640.jpg`, `ar_gate_d2p0_c0.jpg` | 마을 입구 2일 오전 | 보리 (920,621), 네로 (1109,651), 실룩 (1779,636, 울타리 위) |
| `ar_post_d2p0_c440.jpg`, `ar_post_d3p0_c0.jpg` | 우체국 2·3일 오전 | 사서 선생님, 슬링, 뿔이 촌장 |
| `ar_hall_d6p0_c880.jpg` | 2층 복도 6일 오전 | 도토 (1471,616) |
| `ar_store_d2p1_c0.jpg`, `ar_store_d2p1_c640.jpg` | 공동 창고 2일 오후 | 네로 (216,667), 실룩 (974,544), 보리 (1349,690) |
| `ar_workshop_d3p1_c520.jpg` | 수리점 3일 오후 | 보리 (1199,571), 누비 아주머니 (1425,581) |
| `ar_square_d1p2_c0.jpg` | 광장 1일 저녁 | 보리 (245,677) |
| `ar_school_d9p0_c0.jpg` | 학교 9일 오전 | 보리 (119,526, 책상 뒷줄) |
| `ar_facility_d9p0_c640.jpg` | 보호시설 9일 오전 | 누비 아주머니 (1696,667) |

다시 찍기: `RENPY_SDK=… dev/run_renpy_tests.sh art_request_captures`. 배치표를 다시 뽑으려면 `staging_dump`를 쓴다.
