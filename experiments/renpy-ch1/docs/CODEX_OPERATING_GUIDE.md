# Codex 운영 안내서 — Claude가 하던 일과 확인 항목 (2026-10-23)

2026-10-23까지 Claude가 맡았던 개발·검수·공개 절차를 그대로 옮긴다. 이 문서대로 하면 Claude 없이 같은 품질로 진행할 수 있다. 소유자 작업 규칙의 원문은 저장소 루트 `CLAUDE.md`, 기본 구조는 `ROOM13_GUIDE.md`.

## 0. 실행 환경 주의

- 샌드박스(`-s workspace-write`)에서는 가상 화면(xvfb)·소켓·Ren'Py SDK 쓰기가 막혀 **화면 시험, 웹 빌드, 브라우저 QA가 안 된다**(2026-10-23 확인, `docs/reviews/qa-0.20.12/REPORT.md`). 이 셋이 필요한 작업은 소유자가 Codex를 **전체 권한(샌드박스 해제)** 으로 실행해야 한다. 권한이 없으면 해당 확인을 "못 했다"고 보고하고 공개(push)하지 않는다.
- SDK: `/root/.cache/renpy/renpy-8.5.3-sdk`. 크롬: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`(Playwright).
- **화면 시험과 웹 빌드를 동시에 돌리지 않는다**(같은 `game/saves`를 써서 `persistent.*.tmp` 오류가 난다).
- `pkill -f <패턴>`을 쓰지 말 것: 패턴이 자기 명령줄에도 있어 자기 셸이 죽는다. PID로 끈다.

## 1. 기본 순환 (변경 하나마다)

1. **요청 정리**: 소유자 문서·리뷰를 항목으로 쪼개고, 항목마다 "고칠 곳(파일·라벨·대사 ID) / 지킬 것 / 확인 기준"을 적는다. 판정·생사·진상·UI 디자인에 닿으면 멈추고 소유자에게 묻는다.
2. **구현**(2장 규칙).
3. **갱신 명령**(대사·rpy를 고쳤으면 항상):
   ```
   cd experiments/renpy-ch1
   python3 dev/refresh_intake21_lines.py
   python3 dev/refresh_literal_lines.py
   python3 dev/override_map.py --write
   python3 dev/build_dialogue_bindings.py
   ```
4. **단위+lint**: `RENPY_SDK=/root/.cache/renpy/renpy-8.5.3-sdk dev/check.sh` → `OK`, `lint: ok`.
5. **대사·로직 검수**(3장) — 매번.
6. **화면 시험**: 고친 곳과 관련된 시험 + 새 경로면 새 시험 추가(`game/qa_tests/*.rpy`). 큰 묶음을 마칠 때는 전체 목록(`docs/codex/qa_names_0.20.12.txt`, 70개, 약 20분):
   `RENPY_SDK=/root/.cache/renpy/renpy-8.5.3-sdk dev/run_renpy_tests.sh $(cat docs/codex/qa_names_0.20.12.txt)` → 로그 `/tmp/room13-qa/renpy/<이름>.txt`. 시험 이름은 testcase 이름이다(파일명과 다를 수 있음).
7. **커밋·push**: 원본 변경은 바로 커밋(한국어 메시지, 무엇을 왜). `git -c user.name="kkhkkh20-bit" -c user.email="kkhkkh20@gmail.com" commit`. `.rpyc`는 커밋하지 않는다. `git fetch` → `git merge origin/main` → `git push origin HEAD:main`.
8. **공개**는 5장 절차로, 묶음이 끝났을 때.
9. **실제 플레이에 가까운 검사**: 화면 시험(장면 시험)은 상태를 주입해 특정 장면만 확인하므로 1~14일을 이어서 할 때의 막힘·흐름은 잡지 못한다. 큰 묶음마다 브라우저 자동 플레이(`dev/qa_v111_play.py`, `dev/qa_v111_continuation.py` — 처음부터 클릭으로 진행)를 돌리고, 막힌 지점·이상한 화면을 캡처해 보고한다(소유자 2026-10-23 "실제 플레이 검사야?").

## 2. 구현 규칙 (자주 틀리는 것)

- **대사 추가**: `call r13_lines([...])` 안에 튜플 대사를 직접 쓰지 않는다(literal inventory 행 수가 바뀌어 단위 시험 실패). `game/v111/newworld/dNN.json`의 `blocks`에 넣고 `call r13_lines(r13_nw_block('이름'),'nw:이름')`, 또는 파이썬에서 `r13_nw_added_line(dict(speaker=..., kind="thought", text=...))`. 생각 대사는 `kind="thought"`. 블록 행의 `"cut":"ev:KEY"`는 블록 끝까지 그림을 띄운다. 조건은 `"when"` 키와 `game/room13_v111_newworld_text.rpy`의 `R13_NW_WHEN`.
- **기존 대사 교체**: `dNN.json`의 `replace`(ID → {"text":...}), 앞뒤 추가는 `before`/`after`, 빼기는 `drop`. `v111/records.json` 원문은 고치지 않는다.
- **JSON 저장**: 기존 들여쓰기 유지(`{` 다음 2칸이면 indent=2, 아니면 1), `ensure_ascii=False`, 끝 줄바꿈 유지.
- **조사 선택지**: `game/v111/field-bindings.json` 게이트별 `options`(title, location, person/object/move/present, guard). 반환 index로 라벨이 분기하므로 **순서를 바꾸지 말고**, 숨기기는 `guard` 또는 `r13_v111_binding()`에서 거른다(index 보존).
- **장소·조사 지점·배경 덮어쓰기**: `game/room13_v111_later_bindings.rpy`의 등록(init 310~312) **뒤** init에서 한다(현재 init 318). `init N python:` 블록 사이에 0열 주석을 두지 않는다(`dev/test_v111_continuation.py`가 블록을 dedent해 읽음 — 주석은 블록 안에 들여쓴다).
- **함수 덮어쓰기**: `docs/OVERRIDE_MAP.md` 순서를 지키고 바꾸면 `override_map.py --write`.
- **바로 이동**: `$ r13_v111_time("move:travel:<dest>",5)` 후 `call r13_v111_travel(dest,id,companions,direct=True)`.
- **그림**: 픽셀 아트 파노라마 2048×768(또는 넓게 2560×768 → 표시 폭 2400, `R13_WORLD_LAYOUTS[...]["width"]`). 기존 배경과 같은 도트 화풍(평평한 면, 적은 색, 계단식 가장자리, 굵은 윤곽, 잔무늬·붓질 없음 — 소유자 "도트 퀄리티 비슷하게"). 원본은 `art/<주제-날짜>/`에 두고 게임에는 `game/assets/`로 복사. 확대 비교 캡처로 확인.
- **UI**: 공통 부품(`game/room13_controls.rpy`, `docs/design/UI_COMPONENTS.md`)만. 새 디자인은 이미지 시안 → 소유자 승인 → 적용.
- 버전: `game/options.rpy`의 `config.version`. 릴리스 노트 `docs/releases/RELEASE_<버전>.md`(한국어, 무엇이 바뀌었나·검사).

## 3. 로직·대사 검수 체크리스트 (Claude가 매번 하던 것)

### 로직
- [ ] 결말·생사·정답 판정 값(`r13_v111_set`의 outcome·alive·meeting:* 등, proof 정답 묶음, `R13_PROOF_ALTERNATES`)이 의도 없이 바뀌지 않았다.
- [ ] 자료(`r13_v111_apply ... acquire`, `r13_nw_acquire`)를 얻는 시점이 그 자료를 쓰는 회의·선택지보다 앞이다. 자료가 없는 경로에서 막히지 않는다(되묻기·cannot 처리).
- [ ] 모든 분기 끝이 다음 게이트(`r13_v111_wait`)나 이동으로 이어진다. `jump` 대상 라벨이 있다. 같은 게이트로 돌아올 때 끝없이 같은 대사가 반복되지 않는다.
- [ ] 이미 한 확인은 목록에서 빠지거나 다르게 답한다. 이송·인수·구금 상태(`busy:`, `location:`, `handed:`)가 장면 인물 배치와 맞다(사라진 사람이 서 있지 않음).
- [ ] 증인 사망·부재 경로(`r13_v111_actor_ready`, `when` 조건)에서 그 사람 대사가 나오지 않고, 필요한 정보는 다른 사람·물건으로 전달된다.
- [ ] 미연결 분기는 `docs/design/UNCONNECTED_BRANCHES.md`에 적고 구현 분기 수에 세지 않는다.
- [ ] 시간·날짜(`r13_edit(day,period)`, 이동 시간)와 배경 시간대가 맞다.

### 대사
- [ ] **인물이 플레이어보다 먼저 추리하거나 단서의 의미·정답을 말하지 않는다**(소유자 2026-10-22). 관찰 사실·생각 대사·되묻기(`R13_PROOF_RANGE`)도 정답 자료 이름을 말하지 않고 비교할 범위만.
- [ ] 제시 직후 아군·상대가 구조를 길게 풀어 설명하지 않는다(결론은 플레이어 선택 쪽). 같은 사실을 서술과 대사가 두 번 말하지 않는다.
- [ ] 앞뒤 설정·시간선: 그 시점에 아빠가 알 수 있는 것만 말한다(지문에 적혔다고 아빠가 아는 것 아님). 이름을 모르는 사람을 이름으로 부르지 않는다.
- [ ] 말투: 아빠와 다람(딸)의 관계가 말투로 보이고, 감정(느낌표·말끝)이 살아 있다. 인물마다 말투 일관(다람: 아이 말투·당돌함, 아빠: 짧고 단정하지 않는 탐정, 확인하지 못한 의도를 덧씌우지 않음).
- [ ] 톤: 이야기는 어둡게(2026-10-21~). 잘 쓴 짧은 대사는 보존(리뷰 항목이 많다고 다 고치지 않는다).
- [ ] 선택지 문구가 실제 행동과 일치한다(누가 남고 누가 가는지 등). 결과를 미리 말하거나 "위험한 선택" 표시를 하지 않는다.
- [ ] 사건 직후·긴장 장면에서 평소 인사(“또 오셨어요?”)가 나오지 않는다(`R13_TENSE_SCENES`).
- [ ] 줄 길이: 대사창 두 줄 자동 분할이 있지만 의미 단위로 끊는다.

### 화면 (캡처로)
- [ ] 인물이 조사할 물건 앞에 서지 않는다, 이름표가 겹치지 않는다, 화면 이동 화살표와 이름표가 겹치지 않는다.
- [ ] 조사 지점(rect, 월드 좌표=표시 폭 기준)이 그림 속 물건 위치와 맞다.
- [ ] PC 1280×720과 휴대폰 844×390 둘 다.

## 4. 리뷰 문서를 받았을 때

1. 원문을 `docs/reviews/`에 보관.
2. 항목마다 현재 코드와 대조해 반영됨/일부/미반영/이미 고침을 근거와 함께 표로(`docs/reviews/audit-20261023/` 형식).
3. 판정·진상·디자인에 닿는 것은 소유자 결정 항목으로 분리, 나머지는 바로 적용.
4. 적용 후 릴리스 노트의 "이미 고쳐져 있던 항목", "남긴 것"에 정리.

## 5. 공개(웹판) 절차

1. `game/options.rpy` 버전 올림, `RELEASE_<버전>.md` 작성.
2. `dev/check.sh` 통과, 화면 시험 전체 통과(웹 빌드와 동시에 돌리지 않음).
3. `python3 dev/build_web.py --sdk /root/.cache/renpy/renpy-8.5.3-sdk` → `preview/room13-dev/`(손으로 고치지 않음).
4. `cd preview/room13-dev && python3 -m http.server 8766` (백그라운드, PID 기억).
5. 브라우저 확인(참고 스크립트 `docs/codex/ref_scripts/`): `save_load_smoke.py`(PC·휴대폰 저장→새로고침→불러오기, 버전 표시), 바뀐 화면 캡처(`book_and_places.py`, `map_capture.py` 방식). `pageerror` 없음, Ren'Py 예외 화면 없음.
6. 서버를 PID로 끈다.
7. `git add -A preview/room13-dev` + 원본 → 커밋("Room13 <버전> 공개" + 요약) → fetch·merge → push. GitHub Pages 반영.
8. 소유자 보고(한국어): 무엇이 바뀌었나, 검사 결과, 확인 못 한 것, 캡처.

## 6. 지금 이어서 할 일

- 0.20.12: 원본 준비 완료, 공개 절차 진행 중(Claude가 마무리 — 끝나면 `docs/releases/RELEASE_0.20.12.md`와 커밋 로그에 "공개"로 남는다).
- 다음 개발: `docs/design/PLAN_20261023_NEXT.md` 1단계(P1~P5) + 2단계 시범(P6). 13호실은 지금 구조 유지. B(할머니 수첩)·C(누비 동기)는 소유자 진상 결정 전 착수하지 않음.
- 참고 문서: `docs/HANDOFF_CODEX_20261023.md`, `docs/reviews/audit-20261023/AUDIT_review20261021.md`, `docs/design/UNCONNECTED_BRANCHES.md`, `docs/design/QUESTION_DISCOVERY.md`, `docs/design/UI_COMPONENTS.md`.
