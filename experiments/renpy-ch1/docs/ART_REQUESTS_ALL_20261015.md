# 다람탐정 그림 요청서 모음 · 2026-10-15

GPT에 전달할 그림 요청을 한 문서에 모았다. 게임 기준 버전은 0.18.33이다.
같이 받은 압축 파일의 `refs/` 폴더에 참조 그림이 있다.

| 순서 | 요청 | 왜 필요한가 | 원본 문서 |
|---|---|---|---|
| A | 책상 서랍 퍼즐 그림 4종 | 지금은 탁본·눌림·열린 칸을 코드로 임시로 그린다 | `docs/ART_REQUEST_01822.md` 1절 |
| B | 여관 접수대 따닥 문틀 수리 포즈와 공사 흔적, 토리 천 바구니(선택) | 따닥의 판자가 벽에 실제로 붙어 보이지 않는다 | `docs/ART_REQUEST_01822.md` 2절 |
| C | 돌 제단 가로 맵 저녁판, 관·밸브, 연결대, 점검문, 결말 소품 | 이 그림들이 없어 새 제단 배경을 켜지 못했다 | `docs/ALTAR_WIDE_PENDING.md` |
| D | 굵은 도트 주민 24인 후속(표정·포즈 72장 등) | 다른 작업 창이 정리한 주민 그림 요청이다 | `docs/ART_REQUEST_01823.md` |
| E | 슬링이 봉투를 김에 쐬는 포즈와 주전자 김, 다른 사건 주민 포즈(선택) | 사건 글과 화면 속 주민 동작이 다르다 | `docs/ART_REQUEST_01853.md` |
| F | 새 장소 4곳 장면(강가·숲속·돌 사당·장터) 각 3시간대 | 주민이 우체국·수리점 등에 몰려 서 있다 | `docs/ART_REQUEST_01854_PLACES.md` |

공통 규격:
- 기존 게임 그림체를 따른다.
- 그림 안에 글자, UI, 아빠를 넣지 않는다.
- 같은 물건의 상태 그림끼리는 구도와 조명을 맞춘다.
- 배경은 1672×941 또는 문서에 적힌 크기로 받는다. 물건 레이어는 투명 PNG로 받는다.
- 그림만으로 새 사건, 새 증거, 비밀 통로를 만들지 않는다.

---

## A·B. 책상 서랍 퍼즐과 여관 접수대


작성 2026-10-15. 지금 게임에는 코드로 그린 임시 표현이 들어가 있다. 아래 그림이 오면 같은 자리에 교체한다.

### 공통 규격

- 기존 게임 그림체를 따른다. 큰 색면, 계단형 외곽, 단순한 명암, 따뜻한 실내 조명.
  - 참조: `game/assets/room13-pixel-inspect-drawer.webp`(서랍), `room13-pixel-life-door-before.webp`(새 생활 조사 화면).
- 배경 크기는 1672×941이다. 게임은 이 그림을 1280×720으로 줄여 그린다.
  - 아래 좌표는 모두 1280×720 기준이다. 1672 기준으로 바꾸려면 1.306을 곱한다.
- 물건 레이어는 투명 PNG로 받는다.
  - 받은 뒤 `dev/import_art.py`에서 무손실 WebP로 바꾼다. 손실 압축은 하지 않는다.
- 들어가면 안 되는 것: 글자, 숫자, UI 테두리, 손, 아빠, NPC.
  - 예외: 탁본의 ①② 같은 표시가 필요하면 기호 모양으로만 그린다.
- 같은 물건의 상태 그림끼리는 카메라, 광원, 물건 모양, 크기를 맞춘다.

---

### 1. 책상 서랍 퍼즐 (여행 필기함)

#### 게임 안 흐름

1. 얇은 종이를 운반표 위에 올린다.
2. 연필로 문지르면 그림이 나타난다. 그림 내용은 "오른쪽 칸 아래 홈을 누른 채 판을 오른쪽으로 민다"이다.
3. 자로 홈을 누른다.
4. 판을 민다.
5. 도구칸이 열리고 돋보기가 나온다.

#### 현재 임시 표현

- 탁본: 회색 줄무늬 위에 밝은 선(판 윤곽, 아래 반원 홈, ↓ 화살표, → 화살표)을 코드로 그렸다.
- 열린 칸: 어두운 사각형과 원래 판의 왼쪽 띠를 붙여 표현했다.
- 자: 아이콘을 홈 위에 겹쳐 놓았다.

#### 요청 그림

| 파일 이름(제안) | 내용 | 크기·위치(1280×720 기준) |
|---|---|---|
| `room13-pixel-inspect-rubbing-paper.png` | 운반표 위에 놓인 얇은 종이(문지르기 전). 아래 운반표 모양이 살짝 비친다. 모서리가 조금 말려 있다. | 305×150, 왼쪽 위 (435,385)에 놓는다 |
| `room13-pixel-inspect-rubbing-done.png` | 같은 종이를 연필로 문지른 상태. 흑연이 결 따라 고르지 않게 묻어 있다. 눌린 자리만 하얗게 남는다. | 위와 같음 |
| `room13-pixel-inspect-drawer-held.png` | 오른쪽 도구칸 아래 반원 홈에 자 끝이 꽂힌 모습. 자만 그린 투명 레이어. | 홈 중심 (963,528) 부근, 약 120×120 |
| `room13-pixel-inspect-drawer-open.webp` | 서랍 전체 배경에서 오른쪽 판만 오른쪽 벽 안으로 밀려 들어간 상태. 안쪽 칸이 보이고, 칸은 비어 있다. | 서랍 원본과 같은 1672×941, 같은 구도 |

탁본 완성 그림(`rubbing-done`)에서 하얗게 남을 무늬:
- 세로로 긴 판 윤곽. 오른쪽 도구칸과 같은 비율이다.
- 판 아래 가운데에 반원 홈.
- 홈을 가리키는 아래 방향 화살표.
- 판 옆의 오른쪽 방향 화살표.
- 두 화살표 옆에 순서를 나타내는 점 하나와 점 둘. 숫자 대신 쓴다.

돋보기는 기존 아이콘(`room13-pixel-inspect-items.webp`)을 열린 칸 위에 겹친다. 열린 칸 그림에 돋보기를 넣지 않는다.

---

### 2. 여관 접수대: 토리와 따닥

#### 현재 상태(0.18.22)

- 토리: 기존 그림 중 '자기 의자에 앉아 천을 꿰매는' 포즈로 바꿨다. 소파 옆 바닥에 앉아 있다. 새 그림은 없어도 된다.
- 따닥: 기존 '판자를 세워 망치질하는' 포즈를 출입문 옆 벽 앞에 세웠다.
  - 판자는 캐릭터 그림에 붙어 있어서, 벽이나 문틀에 실제로 댄 것처럼 보이지 않는다.
  - 배경 쪽에도 공사 흔적이 없다.

#### 요청 그림

| 파일 이름(제안) | 내용 | 크기 |
|---|---|---|
| `room13-pixel-acting-ttadak-doorframe.png` | 따닥이 옆으로 서서 왼손으로 문틀에 판자를 대고, 오른손으로 망치를 드는 포즈. 판자는 그리지 않는다(배경 레이어로 따로 받는다). 발 위치를 바닥선에 맞춘다. | 세로 약 440px, 투명 |
| `room13-pixel-inn-doorframe-repair.png` | 여관 로비 출입문 오른쪽 문틀에 덧댄 새 판자, 바닥의 못 상자, 대팻밥 조금. 배경 위에 겹치는 투명 레이어. | 여관 파노라마(1920×720) 기준 x 1100~1220, y 150~470 |
| (선택) `room13-pixel-inn-tori-basket.png` | 토리 발치의 천 바구니와 접힌 천 두세 장. 토리가 무슨 일을 하는지 멀리서도 보이게 한다. | 약 110×80, 투명 |

참조 배경: `game/assets/room13-pixel-panorama-inn-morning.webp`(오후·저녁판 포함). 세 시간대에서 모두 자연스럽게 보이도록 조명을 중간 톤으로 맞춘다.

---

### 3. 받은 뒤 할 일 (개발 메모)

- 서랍 그림이 오면 `room13_inspection.rpy`의 `r13_inspection_art`를 바꾼다.
  - `R13RubbingSheet`와 `R13DrawerCavity` 대신 위 파일을 쓴다.
  - 클릭 영역 좌표는 그대로 둔다.
- 따닥 그림이 오면 다음을 연결한다.
  - `room13-pixel-acting.json`에 `living_doorframe` 포즈를 추가한다.
  - `room13-world-layout.json`의 `inn.poses`, `inn.positions`를 그 포즈에 맞춘다.
  - 배경 레이어는 따닥이 여관에 있는 시간대에만 표시한다.
- 이 요청서의 그림은 사람이 플레이해서 재미를 검증한 결과가 아니다. 보이는 상태를 맞추기 위한 요청이다.

---

## C. 돌 제단 가로 맵


원본: `reports/stone-altar-20261015/wide/` (2172×724, 낮 한 장). 지시서: 같은 폴더 `CLAUDE_APPLY.md`.

### 결정

**새 배경은 활성화하지 않았다.** 지시서 5절과 6절의 완료 조건을 아직 채울 수 없다.

- 현재 `altar`는 14일째 결말 장면(`r13_finale`, `r13_rescue`, `r13_final_hub`)에서 쓴다. 대사와 판정이 다음 장치를 직접 가리킨다.
  - "산 아래로 내려가는 관", "연결 장치"(finale:mountain_approach)
  - "연결 손잡이"(finale:mother_arrives)
  - "점검문", "연결대", "끌고 가는 수레"(rescue:altar:maintenance)
  - "관을 떼어 낸다", 수레에서 아이를 내림(finale:emergency_rescue)
  - "묶인 환자들", "담요를 든 가족", "쓰러진 난간"(finale:arrival)
- 새 그림에는 관·밸브·연결대·점검문이 없다. 조사 지점 `valve`에 대응할 물건이 없다.
- 저녁 그림이 없다. 기존 저녁 그림은 1920 폭이라 새 2160 좌표와 섞을 수 없다.

### 필요한 자산 (그림 요청 대상)

| 자산 | 내용 | 규격 |
|---|---|---|
| 저녁판 배경 | 같은 구도, 같은 카메라의 저녁 조명. 결말이 저녁·밤에 진행된다. | 2172×724 원본, 논리 2160×720 |
| (선택) 아침판 배경 | 아침 조명. 없으면 낮 그림을 오전·오후에 함께 쓴다. | 같음 |
| 관·밸브 전경 레이어 | 제단 옆에서 산 아래로 내려가는 관과 밸브. 사람 쪽과 난방 쪽 관이 구분되어야 한다. | 투명 PNG, 월드 좌표 지정 |
| 연결대·연결 손잡이 | 엄마가 붙드는 손잡이, 아이를 올리는 연결대(결말 상태 전용) | 투명 PNG |
| 점검문 | 부리가 여는 관리용 문. 관리 동선에 붙는다. | 투명 PNG |
| 결말 상태 소품 | 끌고 가는 수레, 담요, 쓰러진 난간. 평상시 배경에는 넣지 않는다. | 투명 PNG, 상태별 |

석조 아치를 포털이나 배관 장치로 해석하지 않는다. 비밀 통로나 지하 유적 이벤트는 만들지 않는다.

### 미리 잰 조사 좌표 (아직 적용 안 함)

2160×720 월드 좌표, `[x, y, w, h]`. 새 그림을 1.5배로 확대한 격자 이미지에서 측정했고, 실제 클릭으로 확인하지는 않았다.

| ID | 새 그림의 대상 | 좌표 |
|---|---|---|
| `ledger` | 왼쪽 작업대 위 천을 덮은 문서 | `[155, 425, 90, 65]` |
| `supplies` | 왼쪽 오두막의 장작과 통 | `[215, 345, 130, 75]` |
| `offerings` | 중앙 돌상 위 그릇·천·도토리 | `[980, 430, 165, 90]` |
| `village_view` | 오른쪽 난간 너머 마을 지붕 | `[1890, 340, 265, 150]` |
| `approach` | 아래쪽 진입 계단 | `[570, 600, 240, 115]` |
| `valve` | 대응 물건 없음. 관·밸브 레이어가 오면 그 자리에 맞춘다. | — |

적용할 때 바꿀 것:
- `room13-world-layout.json` `altar`: `width 2160`, `initial_x 440`, `revision 2`, `files`, `objects`, `critical`, `floors`/`slots`.
- `offerings` 관찰문: 보이는 사실만 바꾼다. 예: "제단 앞에 천과 작은 그릇들이 놓여 있다. 놓은 이유와 주인은 모양만 보고 정할 수 없다."

진입 조건(`finale_started`), 증거, 구출, 결말 조건은 바꾸지 않는다.

---

## D. 굵은 도트 주민 24인 후속


작성일은 2026-10-15이다. 기준은 작업 브랜치 `claude/town-trio-candidates`(0.18.23-dev, 커밋 `197c4b1`)이다.

표시 기준은 다음과 같다.
- **[현재 구현]**: 지금 코드와 데이터에 있는 사실이다. 출처 파일을 적는다.
- **[제안]**: 아직 결정되지 않은 제작이나 수정 제안이다. 확정 전에는 게임에 넣지 않는다.

이 문서는 새 역할, 장소, 사건, hotspot을 만들지 않는다.

---

### 1. 굵은 도트 24인 수신 확인

- 받은 것: `all22refs-24characters-coarse.zip`(PNG 24장, README, 카탈로그 CSV·JSON)과 따로 받은 `COARSE24_CATALOG.json`
- 대조 결과
  - 24장 모두 SHA-256이 두 카탈로그와 같다.
  - 크기와 알파 bbox도 카탈로그와 같다.
  - 모두 RGBA이고, 네 모서리가 투명하다(알파 0~1).
- 크기: `snow_tea`만 1038×1515이고 나머지 23장은 1024×1536이다.
- 여백 주의
  - 아래 여백이 거의 없다: `white_owl` 1px, `white_eagle` 3px, `lizard` 4px. 발끝이 캔버스 끝에 닿아 있다.
  - `deer_right`는 위 171px, 아래 61px가 비어 그림이 작다. 넣을 때 키를 따로 맞춰야 한다.
  - `child_deer`(위 82px)와 `golden_dog`(위 53px)도 같다.
- 게임 적용: 하지 않았다. 원본은 작업 공간에만 두었고 저장소에 넣지 않았다.
- 표정·포즈 추가 72장은 아직 받지 않았다(제작 중).

### 2. 이미 코드에 적용된 8명 [현재 구현]

| NPC ID | 이름 | 적용한 그림(이전 판) | 굵은 도트 판 |
|---|---|---|---|
| `resident_yeoni` | 여니 | foxtown.png | `fox_town` (판이 다름) |
| `resident_momo` | 모모 관장 | shrine_goat_records_pixel_v2.png | `shrine_goat` |
| `resident_librarian` | 사서 선생님 | snow_leopard_tea_hostess.png | `snow_tea` |
| `resident_nubi` | 누비 아주머니 | sheep_helper_calm_standing_pixel_v2.png | `sheep_linen` |
| `resident_seol` | 설이 | owl_white_winter_pixel_v2.png | `white_owl` |
| `resident_siluk` | 실룩 | hyena_town_v2.png | `hyena` |
| `resident_nero` | 네로 | tiger-worker.png | `tiger` |
| `resident_bori` | 보리 | bear-resident.png | `bear` |

- 출처: `art/npc-redesign-20261015/redesign.json`, 커밋 `58f7de9`, `2f43fcf`
- 게임에는 굵은 도트 이전 판이 들어 있다. 굵은 도트 판으로 바꿀지는 결정이 필요하다(8절).
  - 바꾸게 되면 `redesign.json`의 원본 경로, 해시, 머리·얼굴 영역만 고치고 `dev/apply_npc_redesign.py`를 다시 돌리면 된다.

#### 역할 출처 확인

- 기준: `game/room13-content.json`의 `residents`와 `game/room13-dialogue-openings.json`의 `calendar`
- `village-residents.json`의 0.8.1 초안은 옛 캠페인 데이터다. Room13 시작 흐름(`start` → `room13_start`)에서는 읽지 않는다.

| NPC | work (content.json) | 기본 행동 문장 | 사용자 요약과 비교 |
|---|---|---|---|
| 사서 | 도서관 기록 보존 | 젖은 책 사이에 마른 종이를 끼운다 | 같다 |
| 모모 | 박물관 보관과 옛 생활 자료 | 낡은 등잔 바닥에 붙은 번호를 읽는다 | 같다 |
| 누비 | 세탁 협업과 **임시 숙박 연결** | 마른 빨래를 사람별로 나눠 묶는다 | 같다. 다만 work에 "임시 숙박 연결"도 있다 |
| 여니 | 의복 수선과 **물자 교환** | 헤진 소매 안쪽을 뒤집어 살핀다 | 같다. 다만 work에 "물자 교환"도 있다 |

- **코드가 다른 점**: 도서관과 박물관은 이동할 수 있는 장소가 아니다.
  - `r13_resident_where`(`game/room13_life.rpy:158`)가 `library`를 `post`로 바꾼다.
  - 그래서 사서와 모모는 실제로 **우체국**에 서 있고, 그 자리에서 젖은 책·등잔 번호 문장이 나온다.
- 카탈로그와 인계문의 역할 제안(차 대접, 신당 기록, 린넨 보조 등)은 본편에 넣지 않았다.

### 3. 미확정 디자인 매칭 후보 [제안]

규칙
- 이미 적용한 8명과 겹치지 않게, 한 NPC에 한 그림만 배정했다.
- 주인공 가족(다람, 아빠, 엄마)과 할머니·나비·밤이·도토·부리는 후보에서 뺐다.
- 종족이 이름에 들어 있는 NPC(곰 선생님, 토끼 할머니)는 종족을 바꾸지 않는다.
- 진료·연구 역할은 본편에 없다. "의료 지원" 제안은 쓰지 않았다.

| 디자인 | 후보 NPC | 근거(현재 데이터) | 실제 충돌 | 확신 |
|---|---|---|---|---|
| `brown_owl` | `resident_owlgp` 부엉이 할아버지 | 같은 종족, 안경, 조끼 | **노인 버전이 필요하다(보류 유지).** 굵은 도트 판도 중년 인상이고 지팡이가 없다. "-오" 말투를 쓰는 노인이다 | 보류 |
| `white_eagle` | `karo` 까로 | 새 → 새. 마차 수리와 반송품 운반에 가방이 맞는다. 긍정 피드백이 있었다 | 까마귀 → 독수리. 주요 인물이다. 입구 전용 포즈 `action_1`(sorting)과 `action_2`(portable_crate)를 다시 그려야 한다 | 중간, 미확정 |
| `white_goat` | `resident_ppul` 뿔이 촌장 | 염소이고 나이 든 남성이다. 촌장·배급 일 | 정장과 지팡이 인상이 시골 외투로 바뀐다 | 높음 |
| `white_wolf` | `resident_badook` 바둑이 | 흰 개과 성인 남성. 야간 순찰 | 점박이 무늬, 제복, 등불이 없다. `living_bootlace`를 다시 그려야 한다 | 중간 |
| `white_duck` | `resident_kkwak` 꽥순 | 남은 유일한 오리이고 이름도 여성형이다 | 예전 설정은 아이인데 그림은 젊은 여성이다. 노랑 → 흰색 | 중간(나이 확인 필요) |
| `long_ears` | `resident_tori` 토리 | 긴 귀, 초록 옷, 수줍은 자세. 수선과 여관 납품 | 꼬리가 여우 모양이라 종족이 불명확하다. 0.18.22 여관 바느질 `activity`(앉기)를 다시 그려야 한다 | 중간 |
| `pink_bird` | `resident_piko` 피코 | 새이고 화려한 색. 그림 그리는 사람 | 공작 → 볏 있는 분홍 새. 그림은 치마 차림이라 **성별 확인이 필요하다** | 낮음 |
| `formal_deer` | `resident_eunho` 은호 사장 | 도시 상인, 단정한 긴 외투, "-하오" 말투 | 흰 여우 → 사슴, 금테 안경이 없다 | 중간 |
| `pale_teen` | `resident_guseul` 구슬 | 수줍은 10대 견습생. 은회색과 연한 털빛이 가깝다 | 너구리 → 사슴 | 중간 |
| `child_deer` | `resident_kongi` 콩이 | 어린아이, 심부름과 길 안내. 빨간 목도리를 이어 간다 | 강아지 → 사슴 | 중간 |
| `deer_right` | `resident_sling` 슬링 | 친절하게 손을 내미는 자세. 우편 배달 | 족제비(지금 그림은 여우형) → 사슴. 우편 가방이 없다 | 중간 |
| `golden_dog` | `resident_tok` 톡 | 성인 남성("톡 아저씨"), 작은 수리. 안경 | 두더지 → 개. 흰 외투가 의사처럼 보일 수 있다 | 낮음 |
| `moose` | `resident_lamplighter` 등불지기 아저씨 | 성인 남성. 가방이 몰래 식량을 나르는 일에 맞는다 | 토끼 → 무스, 등불이 없다. `living_inspectlamp`를 다시 그려야 한다 | 낮음 |
| `deer_left` | `resident_ttadak` 따닥 | 빨간 상의가 붉은 볏의 색을 이어 간다. 건물·목재 점검 | 딱따구리 → 사슴. 0.18.22 여관 문틀 수리 `living_repair`를 다시 그려야 한다 | 낮음 |
| `curly` | (후보 없음) | 남은 NPC 중 맞는 사람이 없다 | — | 보류 |
| `lizard` | (후보 없음) | 뭉치(심부름하는 10대)가 가깝다 | 어머니 백 부인이 판다라서 가족 생김새가 깨진다 | 보류 |

남은 NPC(후보 없음): 서리, 우박, 무쇠 할아버지, 뭉치, 백 부인, 솜이, 곰 선생님, 너울, 돌목, 세련

### 4. 캐릭터 그림 규격 [현재 구현]

| 항목 | 지금 코드 | 출처 |
|---|---|---|
| 받는 원본 | 투명 PNG 1024×1536 전후, 전신 한 명 | 이번 24장 |
| 게임용 변환 | 0.5배로 줄이고 premultiplied로 리샘플한다. WebP 품질 95, 투명도는 무손실 | `dev/apply_npc_redesign.py`, `dev/import_art.py` |
| 크롭 | 알파 32 이상인 영역에 여백 4px | 같음 |
| 발 앵커 | 그림 맨 아래 4% 구간에서 두 발 범위의 가운데 | 같음 |
| 장소 화면 크기 | 크롭 높이를 장소의 표시 높이에 맞춘다(아래 표). 2px 격자로 줄여 그린다 | `room13_acting.rpy` `r13_stage_people`, `R13_WORLD_PIXEL_GRID=2` |
| 대화 화면 크기 | 전신이 대화 높이의 1.05배다. 위쪽에 맞추고 다리는 대화창 뒤로 이어진다. 3px 격자 | `room13_fullbody_dialogue.rpy` |
| 표정 | 6종: neutral, joy, flustered, angry, anxious, surprise. 한 인물은 모든 표정에 **같은 크롭 하나**를 쓴다 | 같음 |
| 동작 포즈 데이터 | crop, foot, head, contact 필수. 앉은 자세는 seat, 손으로 하는 일은 hand, 매달린 자세는 hook 좌표를 더한다 | `assets/room13-pixel-acting.json` |

장소별 서 있는 키(화면 픽셀): `room13-world-layout.json`의 floors·slots 값과 `room13_acting.rpy`의 기본 바닥 값이다.

| 장소 | 너비 | 키 범위 |
|---|---|---|
| gate, square, inn, clinic, greenhouse, facility, altar | 1920 | 200~275 |
| school, workshop | 1800 | 205~280 |
| store | 1920 | 250~368 (기준 키 271, 가까운 구도) |
| dining, kitchen, hall, post, room13 등 | 1280 고정 | 190~290 |

- 우체국 기본 바닥은 (368,645,265), (700,512,222), (1050,548,236)이다.

#### 추가 72장(표정·포즈) 받을 때 지킬 것 [제안]

- **표정**
  - neutral과 캔버스 크기, 몸 위치, 자세가 같아야 한다. 얼굴만 바뀌어야 한다. 대화에서 표정이 바뀔 때 몸이 움직이지 않게 하기 위해서다.
  - 파일 이름에 6종 중 어느 키인지 적는다.
- **생활 포즈**
  - 같은 인물 neutral과 키 비율이 같아야 한다. 앉거나 숙인 자세도 머리 크기가 같아야 한다. 코드가 머리 높이 비율로 키를 맞춘다.
  - 발(또는 엉덩이·무릎)이 닿는 바닥 줄이 그림 안에 있어야 한다.
  - 소품은 캐릭터 그림에 함께 그린다(따로 된 소품 레이어는 지금 없다).

### 5. 장소별 현재 배치 [현재 구현]

- 1주차(1~7일) 기본 상태를 실제 실행해서 뽑았다(사건 전, 특수 사건 제외).
- ★는 이번에 새 그림으로 바뀐 NPC다. `neutral`은 생활 동작 없이 서 있는 모습이다.

| 장소 | 인물 | 포즈 (contact) | 때 |
|---|---|---|---|
| gate | 돌목 `guard` | `action_1` (held_ledger) | 매일 오전·오후·저녁 |
| gate | 보리 `resident_bori` ★ | `neutral` (standing) | 1,2,3,5일 오전 |
| gate | 실룩 `resident_siluk` ★ | `neutral` (standing) | 매일 오전 |
| gate | 네로 `resident_nero` ★ | `neutral` (standing) | 매일 오전 |
| gate | 까로 `karo` | `action_1` (sorting) | 매일 오전·오후 |
| gate | 바둑이 `resident_badook` | `living_bootlace` (self-contained) | 매일 오전 |
| gate | 꽥순 `resident_kkwak` | `activity` (standing) | 매일 오후 |
| gate | 등불지기 아저씨 `resident_lamplighter` | `living_inspectlamp` (self-contained) | 매일 저녁 |
| gate | 까로 `karo` | `action_2` (portable_crate) | 매일 저녁 |
| square | 설이 `resident_seol` ★ | `neutral` (standing) | 매일 오전·오후 |
| square | 도토 `doto` | `world_bulletin_back` (standing) | 1,2,3,4일 오전·오후·저녁 |
| square | 토리 `resident_tori` | `world_bench_left` (background_bench) | 1,2,5,6,7일 오전·오후 |
| square | 부엉이 할아버지 `resident_owlgp` | `activity` (seat) | 매일 오전 |
| square | 피코 `resident_piko` | `living_paint` (self-contained) | 매일 오전·오후 |
| square | 등불지기 아저씨 `resident_lamplighter` | `living_inspectlamp` (self-contained) | 매일 오후 |
| square | 바둑이 `resident_badook` | `living_bootlace` (self-contained) | 매일 저녁 |
| square | 보리 `resident_bori` ★ | `neutral` (standing) | 1,4,7일 오후·저녁 |
| square | 여니 `resident_yeoni` ★ | `neutral` (standing) | 2일 오전 |
| square | 뿔이 촌장 `resident_ppul` | `activity` (standing) | 2,5,7일 오전 |
| square | 솜이 `resident_somi` | `living_bootice` (self-contained) | 2,4,6,7일 오후 |
| square | 슬링 `resident_sling` | `activity` (standing) | 2,4,6일 오후 |
| square | 콩이 `resident_kongi` | `activity` (standing) | 3,6일 오전 |
| inn | 할머니 `granny` | `world_counter_wipe` (counter_front) | 매일 오전·오후·저녁 |
| inn | 누비 아주머니 `resident_nubi` ★ | `neutral` (standing) | 매일 오전 |
| inn | 따닥 `resident_ttadak` | `living_repair` (self-contained) | 매일 오후 |
| inn | 부엉이 할아버지 `resident_owlgp` | `neutral` (standing) | 매일 오후 |
| inn | 토리 `resident_tori` | `activity` (seat) | 1,2,3,4,6,7일 오후·저녁 |
| inn | 구슬 `resident_guseul` | `neutral` (standing) | 매일 저녁 |
| inn | 우박 `resident_ubak` | `neutral` (standing) | 매일 저녁 |
| inn | 은호 사장 `resident_eunho` | `neutral` (standing) | 매일 저녁 |
| inn | 백 부인 `resident_madam` | `neutral` (standing) | 매일 저녁 |
| inn | 여니 `resident_yeoni` ★ | `neutral` (standing) | 2,3,6일 오후 |
| dining | 나비 `nabi` | `action_2` (carrying_tray) | 매일 오전·오후·저녁 |
| dining | 부엉이 할아버지 `resident_owlgp` | `neutral` (standing) | 매일 저녁 |
| dining | 톡 `resident_tok` | `neutral` (standing) | 매일 저녁 |
| kitchen | (배치된 인물 없음) | | |
| hall | 도토 `doto` | `action_1` (held_ledger) | 5,6,7일 오전·오후 |
| hall | 도토 `doto` | `action_2` (floor_sit) | 5,6,7일 저녁 |
| room13 | 다람 `daram` | `action_1` (floor_sit) | 매일 오전 |
| room13 | 다람 `daram` | `action_2` (kneeling) | 매일 오후 |
| room13 | 다람 `daram` | `inspect_floor` (standing) | 매일 저녁 |
| guestroom | 다람 `daram` | `action_1` (floor_sit) | 매일 오전 |
| guestroom | 다람 `daram` | `action_2` (kneeling) | 매일 오후 |
| guestroom | 다람 `daram` | `inspect_floor` (standing) | 매일 저녁 |
| passage | (배치된 인물 없음) | | |
| post | 모모 관장 `resident_momo` ★ | `neutral` (standing) | 매일 오전·오후 |
| post | 사서 선생님 `resident_librarian` ★ | `neutral` (standing) | 매일 오전·오후 |
| post | 뿔이 촌장 `resident_ppul` | `neutral` (standing) | 매일 오전·오후 |
| post | 슬링 `resident_sling` | `neutral` (standing) | 매일 오전·오후·저녁 |
| post | 은호 사장 `resident_eunho` | `neutral` (standing) | 매일 오전 |
| post | 구슬 `resident_guseul` | `neutral` (standing) | 매일 오후 |
| post | 콩이 `resident_kongi` | `neutral` (standing) | 매일 오후 |
| post | 세련 `seryeon` | `action_1` (clipboard) | 2,3,4,5,6,7일 오전 |
| post | 세련 `seryeon` | `chair_read` (background_chair) | 2,3,4,5,6,7일 오후 |
| workshop | 우박 `resident_ubak` | `neutral` (standing) | 1,2,3,5,6,7일 오전 |
| workshop | 부리 `buri` | `action_1` (tool) | 매일 오전·오후 |
| workshop | 등불지기 아저씨 `resident_lamplighter` | `living_inspectlamp` (self-contained) | 매일 오전 |
| workshop | 따닥 `resident_ttadak` | `living_repair` (self-contained) | 1,2,3,5,6,7일 오전 |
| workshop | 톡 `resident_tok` | `activity` (seat) | 매일 오전·오후 |
| workshop | 무쇠 할아버지 `resident_musoe` | `living_foldmap` (self-contained) | 매일 오전 |
| workshop | 보리 `resident_bori` ★ | `neutral` (standing) | 1,3,4일 오후 |
| workshop | 누비 아주머니 `resident_nubi` ★ | `neutral` (standing) | 매일 오후 |
| workshop | 여니 `resident_yeoni` ★ | `neutral` (standing) | 1,4,5일 오전·오후 |
| workshop | 부리 `buri` | `action_2` (kneeling) | 매일 저녁 |
| workshop | 따닥 `resident_ttadak` | `neutral` (standing) | 4일 오전 |
| workshop | 토리 `resident_tori` | `activity` (seat) | 4일 오전 |
| workshop | 우박 `resident_ubak` | `living_measure` (self-contained) | 4일 오전 |
| clinic | 서리 검사원 `resident_seori` | `living_notes` (self-contained) | 매일 오전·오후·저녁 |
| clinic | 우박 `resident_ubak` | `living_measure` (self-contained) | 매일 오후 |
| school | 곰 선생님 `resident_teacher` | `activity` (standing) | 매일 오전·오후 |
| school | 보리 `resident_bori` ★ | `neutral` (standing) | 6일 오후 |
| school | 여니 `resident_yeoni` ★ | `neutral` (standing) | 7일 오후 |
| store | 콩이 `resident_kongi` | `activity` (standing) | 1,2,4,5,7일 오전 |
| store | 꽥순 `resident_kkwak` | `activity` (standing) | 매일 오전 |
| store | 구슬 `resident_guseul` | `living_stamp` (self-contained) | 매일 오전 |
| store | 은호 사장 `resident_eunho` | `living_prices` (self-contained) | 매일 오후 |
| store | 네로 `resident_nero` ★ | `neutral` (standing) | 매일 오후 |
| store | 뭉치 `resident_mungchi` | `living_carry` (self-contained) | 매일 오후 |
| store | 실룩 `resident_siluk` ★ | `neutral` (standing) | 매일 오후 |
| store | 백 부인 `resident_madam` | `living_inspect` (self-contained) | 매일 오후 |
| store | 누비 아주머니 `resident_nubi` ★ | `neutral` (standing) | 매일 저녁 |
| store | 보리 `resident_bori` ★ | `neutral` (standing) | 2,4,5,6일 오전·오후 |
| store | 여니 `resident_yeoni` ★ | `neutral` (standing) | 4,6일 오전·오후 |
| greenhouse | (배치된 인물 없음) | | |
| facility | (배치된 인물 없음) | | |
| altar | (배치된 인물 없음) | | |
### 6. 조사 화면 hotspot [현재 구현]

#### 동작 방식

- "조사"는 따로 열리는 화면이 아니다. 장소 화면 위에 보이지 않는 클릭 사각형이 겹쳐 있다(`room13_screens.rpy` `r13_world_contents`).
- 마우스를 올리거나 클릭할 때
  - 강조 그림은 없다.
  - (24,580)에 이름 풍선이 뜬다.
  - 클릭하면 반짝이는 효과가 나온다.
  - 이미 본 물건은 사각형 가운데에 체크 표시가 붙는다.
- 사각형이 어디서 오는가
  - 가로 스크롤 장소(gate, inn, square, workshop, school, clinic, store, greenhouse, facility, altar): `assets/room13-world-layout.json`의 `objects`에 있다. 좌표는 **장소 전체 너비 기준**이다(1800 또는 1920).
  - 1280 고정 장소: `room13-content.json`의 `objects`에 있다.
  - 단서 없는 구경거리: `assets/room13-discovery-objects.json`(스크롤 장소만)
- 인물이 물건 앞에 서면, 얼굴 부분을 뺀 영역으로 물건 버튼을 다시 그린다(`r13_object_mask`).
- 조건 판단: `r13_available`(`room13_rules.rpy:150`)이 날짜 범위, 사건 상태, 시간대, 필요한 물건, 막는 깃발을 본다.
- 시간: 조사는 시간을 쓰지 않는다. 시간은 일할 때와 13호에서 잘 때만 흐른다.

#### 장소별 hotspot

형식은 `ID[x,y,w,h]`이다. 따로 적지 않으면 설명 문장만 나온다.

| 장소 | hotspot | 단서·연결과 조건 |
|---|---|---|
| gate (1920) | gate_documents[1341,383,201,98], rules[666,313,75,114], road[216,469,413,127], bundles[370,396,178,75], shovel[760,414,82,177], crates[1288,534,206,100], woodpile[1560,437,125,111]. 숨김: booth, ledger | gate_documents: 장면이 열리고 G1. rules: G2, 면담(5~13일, 사건 후, 다람이 붙잡혀 있을 때). road: 2주차 경로 활동. bundles: 기다리기 |
| inn (1920) | desk[1294,334,548,343], door[980,165,131,273], keys[1670,136,150,170], register[1556,355,127,46], knitting[1713,353,134,82], coats[1158,155,121,201], cups[1422,101,180,63]. 구경거리 4개 | door: 2일 이후, 오전·오후, 할머니가 있을 때 문틈 클로즈업. keys: 밤이 보호(5일 이후, E10과 숙박 필요). cups: 기다리기 |
| square (1920) | stone[598,269,170,236], offerings[861,475,121,52], lamp[904,270,187,201], stall[0,278,298,174], cart[326,420,282,144], wood[0,457,147,147]. 구경거리 3개 | stone: 탁본 도구가 있고 2~13일이면 `r13_gm_stone`(R01). lamp: 3일부터 경고 확인, 2주차 답장. cart: 3일 되찾기, 기다리기 |
| workshop (1800) | plans[696,113,219,203], wood[0,381,173,170], axle[528,360,350,93], bolts[470,438,145,54], rag[789,471,150,117], wheel[835,245,226,241], tools[0,56,237,281]. 구경거리 3개 | plans: 숨은 길이 열리거나 `passage_found`가 있을 때만 보인다. E04, 돋보기. axle·tools: 2주차 활동 |
| school (1800) | desks[32,386,702,181], stove[865,399,158,182], blankets[0,482,260,127], lessons[235,419,123,28], firewood[965,470,80,94]. 구경거리 3개 | 2주차 활동만 있다. stove: 기다리기 |
| clinic (1920) | notes[625,463,316,79], bed[1012,322,431,221], basin[598,344,142,60], bottles[322,85,179,302], curtain[1112,78,124,296] | notes: 사례 비교(E35·E33). bed: 2주차 활동, 기다리기 |
| store (1920) | ledger[422,422,338,94], sacks[1359,225,281,291], scale[444,293,243,139], burlap[822,330,163,62] | burlap: 칼이 있고 5~13일이면 `r13_gm_package`. scale: 추가 있으면 `r13_gm_scale`. sacks: H1이 있으면 같은 자리가 `hoard`/`hoard_moved`(H11)로 바뀐다 |
| greenhouse·facility·altar (1920) | `world-layout.json` 참조 | 2주차 활동과 기다리기 |
| room13 (1280) | desk[0,350,430,170], mother_note[136,376,118,44], bed[605,311,537,151], window[197,25,193,248], under[600,480,437,60], floor[590,523,208,82], books[1195,267,50,72], cup·letters·notebook·coat 등 | mother_note: 1일, M01. desk 등: 필기함 클로즈업. bed: E03, 잠자기. under: 칼이 있으면 `r13_gm_floor`(M02). floor: E09. books: 숨은 길 조건이 맞으면 E37 |
| guestroom (1280) | bed, window, boxes, cup, desk | 단서 없음. 숙소를 옮긴 뒤 필기함 |
| hall (1280) | rail, door[705,134,208,305], towels, boots, bucket, lamp | door: 사건 뒤 문장이 바뀐다 |
| dining (1280) | table[420,493,855,129], mittens, blankets, breadboard, pot | table: 기다리기 |
| kitchen (1280) | shelf, stove, rear[13,94,238,517], vegetables, flour, dishes, herbs, ladles | rear: 등불이 있으면 `r13_gm_lamp`(R02). 사건 뒤에는 rear_after(H14). shelf: 숨은 길에서만 |
| passage (1280) | steps, handle, linen, mop, baskets | 숨은 길에서만 보인다. steps: E05 |
| post (1280) | notice[982,239,66,134], parcels, cup, scarf, twine | notice: 2주차 증명 활동 |

#### 클로즈업 화면

- 모두 1672×941 불투명 배경이다. 클릭 영역은 0~1 비율 좌표다(`systems/room13_life_closeups.rpy`, `room13_gimmicks.rpy`).

| 클로즈업 | 그림 | 여는 곳 |
|---|---|---|
| r13_life_door | life-door-before / after | inn door |
| r13_life_meal | meal-before / after | 첫 주방 일 |
| r13_delivery_inspect | delivery-before / after | 배달 일 |
| r13_gm_package | package-closed / seam / revealed | store burlap |
| r13_gm_lamp | lamp-floor + 코드로 그린 어둠 | kitchen rear |
| r13_gm_scale | scale-base / loaded / pivot | store scale |
| r13_gm_floor | floor-closed / open / note-open | room13 under |
| r13_gm_stone | stone-base / paper / rubbed | square stone |

- 필기함: inspect-desk·drawer(1672×941)와 아이콘 시트를 쓴다.
- 이미 낸 그림 요청은 `docs/ART_REQUEST_01822.md`(서랍 퍼즐, 따닥 문틀, 토리 바구니)에 있다. 이 문서에서 다시 요청하지 않는다.

### 7. 배경 레이어와 화면 예약 영역 [현재 구현]

- 스크롤 장소
  - 오전·오후·저녁 그림 세 장을 쓴다(밤은 저녁 그림).
  - 원본은 2048×768(학교·수리점은 1983×793)이고, 장소 너비×720으로 줄여 그린다.
- 1280 장소
  - 1672×941 그림을 1280×720으로 줄여 그린다.
  - 주방·통로·식당은 여관 그림(2×2 분할)의 한 칸이고, 우체국은 마을 그림의 한 칸이다.
  - 복도와 13호는 사건 전·후 그림이 따로 있다.
- 앞 가림
  - 인물만 다각형으로 가린다(AlphaMask). 가림용 앞그림은 따로 없다.
  - 예: inn 접수대 다각형, `R13_STAGE_COUNTERS`의 post·kitchen·dining
- 화면 예약 영역(1280 화면 기준, 그림에 중요한 물건을 두지 말 것)
  - 왼쪽 위: 상태 상자(24,20,410,82)
  - 위쪽 줄: 일거리, 지도·이동, 옵션 버튼
  - 왼쪽: 목표 줄(24,178부터)
  - 왼쪽 아래: 이름 풍선(24,580)
  - 아래: 안내 줄(y 646)과 도구줄(y 650~712)
  - 여관·복도: 이동 칩(`room13-inn-navigation-v4.json`)

### 8. 필요한 제작 항목 [제안]

#### 8-1. 8명의 생활 동작 복원 (그림 필요)

- **지금 상태**
  - 새 그림이 서 있는 자세 하나뿐이다. 그래서 예전 동작을 뺐고, 8명은 모두 `neutral`로 서 있다.
  - 행동 문장은 그대로 나온다. 그래서 문장과 그림이 다르다(예: "수레 바퀴에 낀 눈을 털었다"라고 나오는데 그냥 서 있다).
- **필요한 것**: 인물마다 생활 포즈 1장
  - 내용은 지금 코드에 있는 행동 문장에서만 고른다.
  - 출처: `room13-dialogue-openings.json` `calendar`의 settling·before_case 행동 문장

| NPC | 뺀 포즈 (contact) | 나오는 곳 (5절) | 지금 코드의 행동 문장 |
|---|---|---|---|
| 여니 | activity (seat, 앉기) | 광장·여관·수리점·학교·가게 | 풀어낸 실을 길이별로 나눴다 / 벌어진 소매를 접어 바늘을 꽂았다 |
| 모모 | living_read (self-contained) | 우체국 | 책을 펼치고 돋보기로 내용을 살핀다(예전 포즈) / 전시품 밑의 번호를 다시 읽었다 |
| 사서 | activity (seat, 앉기) | 우체국 | 젖은 책 사이의 종이를 새것으로 갈았다 |
| 누비 | living_fold (self-contained) | 여관·수리점·가게 | 마른 빨랫감을 집별로 묶었다 |
| 설이 | activity (standing) | 광장 | 종줄의 매듭을 다시 만졌다 |
| 실룩 | living_clean (self-contained) | 입구·가게 | 수레 바퀴에 낀 눈을 털었다 |
| 네로 | activity (standing) | 입구·가게 | 이름표의 젖은 쪽을 안으로 접었다 |
| 보리 | activity (standing) | 입구·광장·수리점·학교·가게 | 장작 묶음의 끈을 한 번 더 당겼다 |

- **규격**
  - 4절과 같다.
  - 앉은 포즈는 앉는 점(seat)을 표시해 주면 좋다. 받은 뒤 데이터에 넣는다.
  - 소품(바늘, 책, 종줄, 장작 등)은 그림 안에 그린다.
- 받으면 `redesign.json`에 포즈를 추가할 수 있게 적용 스크립트를 넓힌다(코드 작업).

#### 8-2. 실룩이 울타리 위에 보이는 문제 (그림 필요 없음, 코드·데이터 수정)

- **원인 [현재 구현]**
  - 입구 배치 자리 `slots`의 `[1780,635,230,"floor"]`가 배경의 나무 울타리 가로대 위에 있다.
  - 그 뒤는 돌담이라 바닥이 없다. 확인 그림으로 검증했다.
  - 예전 족제비 그림도 같은 자리에 섰다. 이번 교체로 생긴 문제가 아니다.
- **수정 제안 [제안]**
  - 이 자리의 발 높이를 울타리 앞 눈 바닥(y 690~700 정도)으로 내리거나, 이 자리를 지운다.
  - 데이터 한 줄을 고치고 입구 화면 테스트로 확인하면 된다.

#### 8-3. 그 밖의 결정·제작

1. 부엉이 할아버지: 갈색 부엉이 **노인 버전**이 필요하다. 굵은 도트 판도 아직 중년이다.
2. 이미 적용한 8명을 굵은 도트 판으로 바꿀지 결정이 필요하다. 바꾸면 2절 방법으로 다시 적용하고 같은 검사를 한다.
3. 3절 후보 중 확정한 것만 적용한다. 그때 확인할 것
   - 까로 독수리: 입구 전용 포즈 2장(정리하기 `action_1`, 상자 들기 `action_2`)
   - 피코 분홍 새: 성별
   - 꽥순 흰 오리: 나이
4. 추가 72장: 4절 규격(같은 크롭, 같은 키 비율)을 지켜 주면 표정은 데이터만 넣어 적용할 수 있다.
5. 조사 화면 새 디자인
   - 지금 hotspot 좌표(6절)는 배경 그림 속 물건 위치에 맞춰져 있다.
   - 배경을 새로 그리면 물건 위치를 지금 사각형 안에 두거나, 새 좌표를 함께 넘겨 주어야 한다.
   - 7절의 예약 영역에는 단서 물건을 두지 않는다.
