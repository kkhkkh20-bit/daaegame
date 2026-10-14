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

### 선택지 문구 (0.18.4)
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
