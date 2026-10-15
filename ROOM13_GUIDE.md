# Room13 작업 가이드 (0.18.0부터)

다른 채팅·세션이 Room13(다람탐정 Ren'Py 웹판)을 고칠 때 이 문서를 먼저 읽는다.
2026-10-14 리팩토링으로 작업 방식이 바뀌었다. 예전 방식(소스 zip 풀기·3-way 병합·다시 압축)은 더 이상 쓰지 않는다.

## 1. 한눈에

| 항목 | 지금 | 예전 |
|---|---|---|
| 원본 | `experiments/renpy-ch1/` 일반 파일 | `preview/room13-source/ROOM13_SOURCE_HANDOFF.zip` (삭제됨) |
| 그림 원본 | `experiments/renpy-ch1/game/assets/` (웹에 나가는 파일 그대로) | 지난 공개본 game.zip 안에만 있었음 |
| 빌드 | `python3 dev/build_web.py --sdk $RENPY_SDK` (10초 남짓) | 지난 공개본을 풀어 덮어쓰고 다시 압축 (수 분) |
| 공개본 | `preview/room13-dev/` (GitHub Pages) | 같음 |
| 첫 로딩 | 핵심 7.5MB + 그림·글꼴 개별 파일 약 58MB | 250MB 한 덩어리 |
| 다른 세션과 합치기 | 평범한 `git pull`(텍스트 병합) | zip 3-way 병합 |

## 2. 작업 순서

```bash
cd experiments/renpy-ch1
export RENPY_SDK=$(dev/setup_sdk.sh)        # 처음 한 번 (~/.cache/renpy 에 받음)

# 1) 고친다 (game/*.rpy, game/*.json, game/assets/...)
# 2) 빠른 검사: 단위 테스트 100개 + lint, 몇 초
dev/check.sh
# 3) 화면 테스트: 고친 곳과 관련된 것만, 또는 이름 없이 표준 묶음(약 4분)
dev/run_renpy_tests.sh carriage_skip trial_win
# 4) 웹판 빌드 → preview/room13-dev 갱신
python3 dev/build_web.py --sdk "$RENPY_SDK"
# 5) 실제 브라우저 확인 (저장소 루트에서 서버를 띄운다)
(cd ../.. && python3 -m http.server 8765 >/dev/null 2>&1 &)
python3 dev/qa_carriage.py && python3 dev/qa_navigation.py && python3 dev/qa_save_slots.py
# 6) 커밋·push (CLAUDE.md 규칙: 검증 후 main에 바로 반영, 강제 push 금지)
```

- 브라우저 QA는 기본으로 `http://localhost:8765/preview/room13-dev/`를 연다. 다른 주소는 `ROOM13_URL`, 결과 폴더는 `ROOM13_QA_OUT`(기본 `/tmp/room13-qa`)로 바꾼다.
- 공개 확인: push 뒤 `https://kkhkkh20-bit.github.io/daaegame/preview/room13-dev/game-transport.json`의 `archive_sha256`이 빌드 결과(`/tmp/room13-build/build-report.json`)와 같아질 때까지 기다린 뒤 실제로 열어 본다.

## 3. 규칙

### 소스와 병합
- 원본은 `experiments/renpy-ch1/` 하나다. zip을 만들거나 풀지 않는다.
- main이 앞서 있으면 `git pull`(merge)로 합친다. 충돌은 소스 파일에서만 푼다.
- `preview/room13-dev/`의 빌드 결과물(game.part01, game-transport.json, game/assets 등)이 충돌하면 손으로 고치지 않는다. 소스를 합친 뒤 `dev/build_web.py`로 다시 빌드한 결과를 커밋한다.
- `.rpyc`, `game/cache/`, `game/saves/`, `tests/`, `qa_result.txt`는 커밋하지 않는다(.gitignore에 있음).

### 버전과 기록
- 버전: `game/options.rpy`의 `config.version`과 `build.version` 두 곳.
- 판 기록: `docs/releases/RELEASE_<버전>.md` 하나에 무엇을 왜 바꿨고 무엇으로 검증했는지 적는다.
- 같은 번호를 다른 세션이 이미 썼으면 다음 번호를 쓴다. 번호 겹침은 병합 때 바로 보인다.

### 그림·소리
- 새 그림은 `python3 dev/import_art.py 새그림.png [--name room13-pixel-이름.webp]`로 넣는다.
  - WebP 품질 95, 투명도는 무손실로 저장된다. 3배 확대 비교에서 원본과 구별되지 않고 크기는 약 1/4이다.
  - 1픽셀이 중요한 작은 UI 그림은 `--lossless`.
- 스크립트·JSON에서는 `.webp` 이름으로 참조한다.
  - 예전 저장에 남은 `room13-pixel-*.png` 경로는 `game/room13_webp_alias.rpy`가 `.webp`로 이어 준다.
- 쓰지 않는 그림은 지운다. 빌드는 `game/assets`의 64KB 이상 그림·글꼴을 모두 첫 로딩에 받으므로, 남겨 두면 그만큼 느려진다.
- 웹 로딩 분류(`dev/build_web.py` 위쪽 상수)
  - **첫 로딩:** 64KB 이상 그림·글꼴·타이틀 음악. 시작 전에 병렬로 받는다.
  - **핵심 zip:** 작은 파일과 스크립트.
  - **필요할 때 받음:** 배경음악 mp3와 예전 캠페인 PNG. Ren'Py progressive download로 받는다.

### 함수 덮어쓰기 (중요)
- 여러 시스템이 기존 함수를 붙잡아 새로 정의하는 방식으로 확장되어 있다.
  - 예: `_r13_items_topics=r13_topics` 다음 줄에 `def r13_topics(person): ...`
  - `r13_topics`는 11층, `r13_present`는 8층이다.
- 순서와 위치는 `experiments/renpy-ch1/docs/OVERRIDE_MAP.md`에 있다. 손대기 전에 확인한다.
- 새 층을 넣을 때 지킬 것
  - 같은 함수의 다른 층과 **같은 init 우선순위를 쓰지 않는다**. 같으면 파일 이름이 순서를 정한다.
  - 넣은 뒤 `python3 dev/override_map.py --write`로 지도를 갱신한다. 갱신하지 않으면 `test_override_map`이 실패한다.
- 붙잡지 않고 다시 정의한 함수(앞 정의가 버려지는 경우)도 테스트가 잡는다.
- 지도와 실제 실행 순서가 같은지 보려면: `dev/run_renpy_tests.sh override_chain`. 결과의 각 층 (파일, 줄)이 지도와 같아야 한다.

### 데이터
- `game/room13-content.json`은 직접 고친다.
  - 예전 생성기(`dev/build_room13_content.py`)는 지금 내용을 재현하지 못해서 삭제했다. 돌리면 이후 수정이 사라졌다.
  - 필요하면 git 기록에서 볼 수 있다.
- `story-room13/`은 집필 참고 자료다. 실행 기준은 `game/`의 데이터다.

### 마을 사건과 재판 관문 (0.18.2·0.18.3)
- 사건 코드 파일은 셋이다. 기존 흐름에 붙는 곳은 두 군데다.
  - 파일: `room13_town_events.rpy`(묶음 1), `room13_episodes.rpy`(큰 사건 4개), `room13_town_events2.rpy`(묶음 2)
  - 도착 사건: `r13_roam`에서 `r13_town_events`를 호출한다.
  - 선택지가 있는 대화 주제: `R13_TOPIC_LABELS`에 등록한다.
- 재판 관문은 `room13_episodes.rpy`에 있다.
  - `R13_WITNESS_GATES`: E10은 밤이, E12·E15는 나비, E13은 톡이 증언해야 쓸 수 있다.
  - C4 결론은 `fair_hearing`이 있어야 집행된다.
  - 재판 테스트를 새로 만들면 `r13_qa_setup`이 이 관문들을 기본으로 켠다. 끄려면 `"-gates"`를 넘긴다.
- 사건 목록과 상태는 `docs/EVENT_CATALOG.md`에 있다.
- 검사 순서(소유자 요청): 작업 중에는 고친 곳의 테스트만 돌리고, 전체 회귀(`dev/run_renpy_tests.sh` 인자 없이)는 묶음을 마친 뒤 배포 전에 한 번 돌린다.

### 시간 규칙과 저녁 미션 (0.18.5)
- 시간은 일(오전·오후)과 13호에서 자는 것으로만 흐른다. 새 장면에 `r13_tick()`을 넣지 않는다. 활동 비용은 `systems/room13_evening.rpy`가 0으로 맞춘다.
- 저녁(period 2)에 2·3·5·6일의 저녁 미션이 열린다. 새 저녁 사건은 `R13_EVENING_MISSIONS`에 등록하고, 도착 장면은 `r13_evening_events`에 넣는다.
- 테스트의 `r13_qa_roam`은 저녁 안내를 건너뛴다. 안내를 보려면 flags에 `"+brief"`를 넣는다.

### 대사 다듬기 (외부 도구로 고친 뒤 반영)
- 내보내기: `python3 dev/dialogue_tool.py export` → 저장소 루트 `dialogue_work/export/`에 장면별 CSV(150줄 안팎)와 `지침.md`. 이 폴더는 git에 넣지 않는다.
- 반영: `python3 dev/dialogue_tool.py import 파일.csv|폴더|zip` → 시험 반영 보고서(`dialogue_work/반영_보고서.md`)만 쓴다. 확인 뒤 `--apply`.
- 위치와 원문이 지금 소스와 같아야 한다. 아래에 걸리는 줄은 반영하지 않고 이유를 보고서에 적는다.
  - 괄호 조각이 달라진 줄
  - 인물 이름 횟수가 달라진 줄
  - 줄바꿈, 문자열을 닫는 따옴표가 들어간 줄
  - 길이 제한(선택지 24자)을 넘는 줄
- 테스트가 글자로 확인하는 대사는 내보내지 않는다. 테스트가 클릭하는 선택지는 tests.rpy도 함께 바뀐다.
- 반영 뒤에는 보통 변경과 같이 check → 화면 테스트 → 빌드 → 브라우저 확인을 거친다.
  - `dev/test_*.py`에도 대사를 글자로 확인하는 곳이 있다. 실패하면 새 문장에 맞춘다.
- 말투 기준(0.18.12, 소유자 선호): 그거·거기·그분은 가리키는 대상으로, 잘린 대답은 뜻이 드러나게, 대사 속 만든 말은 일상어로 쓴다. 고정 용어와 장소·물건·기록 이름은 바꾸지 않는다.

### 대사 줄바꿈 (0.18.12)
- `systems/room13_linebreak.rpy`가 `r13_lines`에서 자동으로 처리한다. 대사에 `\n`을 직접 넣지 않는다.
- 문장 끝마다 줄을 바꾸고, 한 줄은 35자(큰 글씨 29자)를 넘기지 않는다. 네 줄 이상이면 두 줄씩 나눠 보인다.

### 반복 플레이 설계 규칙 (0.18.13~0.18.19, 소유자 지시)
- 안내는 목적지·행동 대신 풀리지 않은 의문으로 쓴다. "누구에게 무엇을 보여 주자"를 쓰지 않는다.
- 자료를 대신 제시해 주는 대화 주제를 만들지 않는다. 기록을 직접 제시하게 한다(`systems/room13_present_flow.rpy`).
- 기록 문장은 관찰·들은 말만 쓰고 추론을 넣지 않는다.
- 주민은 자기가 겪은 일을 기억한다. 좋은 소문으로 피해를 지우지 않는다(`systems/room13_memory.rpy`).
- 새 일반 사건은 바로 시작하지 말고 `R13_EVENT_OFFERS`(`systems/room13_event_offers.rpy`)에 등록해 표시로 띄운다. 지나쳤을 때의 결과 깃발과 전해 들은 말을 같이 적는다.
- 정본은 `story-room13/CURRENT_STORY_DECISIONS.txt`와 `story-room13/CASE13_CANON_SYNC.md`다. 사건 연쇄를 건드리기 전에 읽는다.

### 도트 연출 (0.18.29~0.18.37)
- 벽난로 불꽃·저녁 불빛, 실외 저녁 눈·가로등, 다람이 눈 깜빡임, 광장 굴뚝 연기, 증거 반짝임, 제시·반박 집중선, 지도 현재 위치 핀, 시간대 전환 디더. 화면 연출 신호는 `r13_fx_cue`. 코드는 `systems/room13_dot_fx.rpy`, 좌표·프레임은 `game/assets/room13-dot-fx.json`.
- 표정이 바뀔 때 몸 반응과 반응음(놀람 움찔→튀어오름 등). 인물은 `R13_REACT_PEOPLE`. 연결은 `r13_speaker` 안 한 곳.
- 눈 깜빡임 인물은 `make_dot_fx.py`의 `BLINK_MORE`·`BLINK_SKIP`. 새로 만들면 표정마다 눈을 사람이 확인한다.
- 조사(배경 위 현장) 화면 인물은 움직이지 않는다(`R13_FIELD_IDLE = False`). 1:1 대화 그림은 평소엔 멈춰 있고 눈만 깜빡인다. 감정이 바뀌면 부드러운 스쿼시·스트레치 동작 한 번(`r13_body_*`, 0.18.43). 숨쉬기는 없다(0.18.44 소유자). 검수 녹화용 화면 테스트 `motion_reel`.
- 프레임은 `python3 dev/make_dot_fx.py`로 다시 만든다. 손으로 고친 프레임을 넣지 않는다(다시 돌리면 덮인다).
- 원본 그림은 바꾸지 않고 위에 얹는다. 설정의 '움직임'이 꺼져 있거나 건너뛰기 중이면 원본만 보인다.
- 배경을 바꾸면(같은 파일 이름) `make_dot_fx.py`를 다시 돌리고 `dev/run_renpy_tests.sh dot_fx` 캡처를 확인한다.

### 오프닝 컷씬 (0.18.39)
- 새 게임에서 마차 대화 앞에 약 17초(편지 → 지도 경로 → 제목 → 마차). 코드는 `systems/room13_opening.rpy`, 연결은 `room13_start`의 `call r13_opening_cut`.
- 화면 테스트 중에는 나오지 않는다. 확인은 `dev/run_renpy_tests.sh opening_cut`.
- 컷씬도 아빠는 그리지 않고, 아빠가 아는 사실만 글로 쓴다.

### 그림책 톤 (0.18.47, 소유자: 동화처럼)
- 튀는 효과(별 반짝임, 집중선, 흔들림, 통통 튐, 위아래로 움직이는 표식)는 쓰지 않는다. 은은하게 스며드는 효과를 쓴다.
- 불빛이 있는 장면은 조명 장치(`R13FxLightRig`, 0.18.54)로 빛과 그림자가 함께 일렁인다. 새 장면은 `make_dot_fx.py`의 `light_rigs()`에 빛 위치를 적는다. 움직임 점검은 `motion_audit` 화면 테스트를 녹화해서 본다.
- 화면 전환은 종이 번짐(`r13_bleed`), 증거는 따뜻한 빛, 제시·반박은 가장자리 비네트. 코드는 `systems/room13_storybook.rpy`.

### 메인 타이틀 연출 (0.18.41)
- 첫 등장 로고·메뉴 페이드인(게임을 켠 뒤 한 번, 0.18.46 동화 같은 느낌으로), 도트 눈, 불빛 일렁임. 코드는 `systems/room13_title_fx.rpy`, 연결은 `main_menu`의 세 줄.

### 선택지 문구 (0.18.4)
- 인물과 대화하는 선택지는 아빠가 할 말로 쓴다(“…”). 판단을 대신하는 말(협박한다, 달랜다, 편을 든다)은 쓰지 않는다. 확정된 돈·시간만 짧게 붙인다(12냥, · 늦은 저녁까지).
- `menu` 선택지는 무엇을 할지만 24자 이하로 쓴다. 자세한 말은 고른 뒤 대사로 넣는다. `dev/test_choice_length.py`가 검사한다.
- 선택지 화면은 940px 한 줄이다. 번호와 1~9 키가 붙고, 바로 앞 대사가 위에 남는다.

### 하지 말 것
- 지난 공개본(game.part*)에서 파일을 꺼내 소스로 쓰지 않는다. 원본은 항상 `game/`이다.
- 예전 QA 결과 폴더(`qa-room13-0150` 등)나 버전별 QA 스크립트를 다시 만들지 않는다.
  - 브라우저 QA 보조 기능은 `dev/webqa.py` 하나에 있다.
  - 새 검사는 `dev/qa_carriage.py` 형식을 따른다.
- 게임 기본 원칙(소유자 결정)
  - **회차 리셋:** 회차마다 처음부터 시작한다. 앞 회차 기록·보상·해금은 없다. 남는 것은 플레이어 지식뿐이다.
  - **화면:** 아빠는 화면에 그리지 않는다. 플레이어가 아빠 시점에 몰입하도록 하기 위해서다.

## 4. 예전 방식으로 하던 작업이 있다면

zip 기반으로 고치던 변경이 남아 있으면 다음 순서로 옮긴다.

1. zip 안 `experiments/renpy-ch1/...`의 고친 파일을 같은 경로의 저장소 파일에 반영한다. 다른 사람 변경을 덮지 않도록 `git diff`로 확인한다.
2. 고친 파일 안의 `assets/room13-pixel-*.png` 참조를 `.webp`로 바꾼다.
3. 새 그림이 있으면 `dev/import_art.py`로 넣는다.
4. `selected_asset_overlay.json`에 새 항목을 추가하지 않는다. 그림을 `game/assets`에 넣으면 끝이다. 이 파일은 예전 선정 기록이다.
5. 2절의 순서로 검사·빌드한다.

## 5. 참고

- **변경 기록:** `experiments/renpy-ch1/docs/releases/RELEASE_0180.md`
- **엔진 용량:** Ren'Py 웹 엔진(renpy.wasm·renpy.data, 약 37MB)은 고정이다. 한 번 받은 뒤에는 브라우저 캐시를 쓴다.
- **캐시 반영:** GitHub Pages 캐시가 10분이라, 바뀐 그림은 최대 10분 뒤에 보일 수 있다.
  - 첫 로딩 파일은 주소에 내용 해시(`?v=`)가 붙어 바로 바뀐다.
- **2026-10-14 git 기록 재작성(소유자 지시, 1회 한정 강제 push)**
  - 예전 빌드 파일(game.part*, 소스 zip 등 498개, 압축 전 13.4GB)을 지난 기록에서 지웠다. 저장소 팩은 4.3GB → 2.3GB.
  - 모든 브랜치의 커밋 번호가 바뀌었다. 각 브랜치 최신 내용은 그대로다. 다만 main·PR #8 외 12개 브랜치에서는 예전 빌드 파일만 빠졌다.
  - 그 전에 받은 클론에서는 그냥 pull하지 않는다.
    - 새로 받거나, 올리지 않은 작업이 없으면 `git fetch origin && git reset --hard origin/<브랜치>`를 쓴다.
    - 올리지 않은 작업이 있으면 패치로 뽑아(`git format-patch`) 새 기록 위에 다시 적용한다.
  - 이후 강제 push 금지 규칙(CLAUDE.md)은 그대로다.
