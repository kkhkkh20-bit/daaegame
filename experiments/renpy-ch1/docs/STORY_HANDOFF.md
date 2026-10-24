# 이야기·대사 인계 기록 (Claude → Codex 이어받기용)

소유자(2026-10-24): "대사 쪽은 너가 해. 기록도 남겨서 너 사용량 끝나면 코덱스에게 대사와 너랑 나눈 우리 논리와 포인트도 이어가게 해."
이 문서는 Claude가 대사·로직·분기·스토리 작업을 할 때마다 갱신한다. Claude가 멈추면 Codex는 이 문서부터 읽고 「다음 할 일」의 맨 위부터 이어 간다.

## 1. 먼저 읽을 것 (순서대로)
1. **이야기 총정리 두 문서** — 이야기 상태를 한 번에 파악하는 기준 문서다. `docs/design/story_master.md`(사람이 쓰는 부분: 사건 여섯 칸·감정선·퍼즐·대승리·예방·불타는 밤·숨겨진 에피소드·회의 규칙, 항목마다 현행/설계 표시)와 `docs/design/story_master_auto.md`(코드에서 뽑는 부분: 날짜별 장면 순서·세우는 인물·갈림 조건·판정 값·회의 쟁점/정답/기회 수/결과·생사·명단·결말 판정·조건 이름). 자동 부분은 손으로 고치지 않고 `python3 dev/story_master.py --write` 로 다시 만든다(대사·조건·회의 코드를 고친 커밋에 함께). 한 장 요약은 `docs/design/branch_table.html`.
2. 루트 `CLAUDE.md` — 맨 위 규칙들이 전부 소유자 결정이다. 특히: Claude의 핵심 임무(분기 논리 오류 0·인물 대사 맞춤·아빠 입장 이해), 살인 사건은 맞물려야 한다, 죽는 사람과 먼저 감정선, 두 가지 추리, 예방은 물건 퍼즐(인과 비틀기), 회의가 본 게임·예방은 보너스, 대사는 대화로 이해시킨다.
3. `docs/design/DECISIONS_20261024.md` — 확정된 결정 목록과 넣는 순서.
4. `docs/design/VOICE_GUIDE.md` 1-0 — 아빠가 묻고 상대가 답하는 대화. 플레이어는 아빠만큼만 안다.
5. `docs/design/EPISODES.md` — 18개 사건의 사실(피해자·가해자·동기·결과·아빠의 동기). 엄마는 이름이 없다. 모과는 판돌의 아내.
6. 설계: `MEETING_RULES_V2.md`(회의는 전투 — 기본 증거로 언제나 이김, 보너스 증거는 대체 정답, 대승리는 7일·12일만, 회의 중 아빠 생각 줄 규칙), `PUZZLE_GRAMMAR.md`(조사·대화·선택지·아이템 조합, 우연히 못 맞춤, 표시 없음, 맥거핀), `OWL_PREVENTION_DESIGN.md`, `GRAND_WIN_DESIGN.md`, `WILD_NIGHT_DESIGN.md`(+`docs/reviews/wild-night-20261024/지시서.md`), `HIDDEN_WILD_FAMILY.md`, `PRICE_DESIGN.md`(아빠의 동기·탈출의 끈), `FUTURE_KNOWLEDGE_KEYS.md`.
7. 검수 기록(사실 근거): `docs/reviews/branch-review-20261024/`(사실조사·회차구조_검수), `case-logic-20261024/사건맞물림_대조.md`, `bonds-20261024/감정선_검수.md`, `action-review-20261024/`(행동 이해도·적용보고), `meeting-balance-20261024/기회수_분석.md`, `owl-prevention-20261024/사실대조.md`, `self-review-20261024/`.

## 2. 우리가 정한 논리의 핵심 (요약)
- 본 게임은 회의(재판). 조사는 자유·시간 제한 없음. 회의에 필요한 기본 증거는 정해진 행동을 하면 반드시 얻고, 기본 증거만으로 언제나 이길 수 있다.
- 판을 넘는 추리: 실패한 판에서 알게 된 사실로 다음 판에 조사·대화·아이템을 조합해 인과의 고리를 비튼다 → 예방·대승리·진엔딩. 회차 기억은 플레이어만, 아빠는 매번 처음 — 예방 행동은 그날 아빠가 할 만한 생활 행동으로 보이고, 결과를 알리는 특별한 대사 없이 그 일이 그냥 안 일어난다.
- 친절한 선택이 곧 예방이 되는 길을 두지 않는다. 처음 하는 사람에게 예방 단서를 주지 않는다.
- 회의 중 아빠 생각: 쟁점이 열릴 때는 주장 정리·걸린 사람·감정만(추리 금지). 틀리면 「증거는 이미 손에 있다」 + 틀릴수록 좁히는 힌트(주장의 어느 부분 → 자료의 종류, 이름·정답은 끝까지 말하지 않음 — 역전재판 방식). 기회를 다 쓰면 「다 있었다, 이어 붙이지 못했다」.
- 사건마다 피해자·범인·동기·수단·기회·증거가 맞물린다. 예방된 판에서도 범인의 동기는 사라지지 않는다.
- 위기에 놓이는 인물은 그 전 에피소드에서 아빠·다람과 주고받은 일이 있고, 위기 장면이 그것을 비춘다.
- 무서운 결과는 최악까지 허용(불타는 밤: 다람·엄마도 죽을 수 있음).

## 3. 대사 작업 방법
- 대사는 `game/v111/newworld/dNN.json` 패치(replace/before/after/blocks/new_evidence), 조건은 `game/room13_v111_newworld_text.rpy`의 `R13_NW_WHEN`, 블록 재생은 `r13_nw_block(name)`. 하루 대본 보기·적용: `python3 dev/dialogue_day.py show N` / `apply N EDITS.json`(조건 변형이 섞여 나오므로 의심 줄은 조건을 코드에서 확인).
- 말하는 사람은 그 장면에 세운다(`r13_v111_arrive`/`r13_v111_join`). 죽었거나 떠난 판에서는 나오지 않게 조건.
- 점검(모두 통과해야 반영): 단위 시험 `python3 -m unittest discover -s dev -p 'test_*.py'`(원래 실패 3건 — drawer_puzzle 2, actor_intent 1 — 외 0), lint `$SDK/renpy.sh . lint`, `dev/dialogue_logic_check.py`, `dev/dialogue_sweep.py`, `dev/branch_audit.py --all`(새 의심 0), `dev/reanchor_lines.py --write`, `dev/override_map.py --write`, 화면 시험 `dev/run_renpy_tests.sh <이름>`(다른 renpy와 동시에 돌리지 않음).
- 대사·조건·회의 코드를 고쳤으면 `python3 dev/story_master.py --write` 로 총정리 자동 부분을 다시 만들고, 바뀐 뜻이 있으면 `docs/design/story_master.md`·`branch_table.html` 도 고친다.
- 반영: 작업 브랜치 `claude/cool-gates-s9msjz`에 커밋 → 검증 → `git push origin HEAD:main`(강제 push 금지). 버전은 `game/options.rpy` 두 곳, 릴리스 노트 `docs/releases/RELEASE_x.md`, 웹 빌드 `dev/build_web.py`.
- 커밋·보고는 한글, 이모지 금지, 모델 이름 넣지 않음.

## 4. 지금 상태 (2026-10-24 마지막 갱신)
- 2026-10-24: **0.20.29 공개**(main). 1부 대사 47건·회의 결함/기회 수/전부 내기·사건 맞물림·주민 동작 그림이 main에 들어갔다. main의 B 디자인(0.20.26~28)과 병합됨. 남은 기존 시험 실패 `new_places`는 새 끌기 지도의 좌표 문제로 지도(디자인) 쪽 몫.
- main 공개: 0.20.25. 작업 브랜치에는 그 뒤로 1부 대사 반영(47건), 「그제도요」 수정, 주민 동작 그림 46장, 각종 설계·검수 문서가 있다(main 미반영).
- 디자인(B안 UI·옵션창·표정 매핑)은 소유자 지시로 Claude가 손대지 않는다(작업 사본에 중간 결과만 있음).
- 지시서 01 반영(작업 브랜치, main 미반영): 회의별 기회 표 `R13_NW_TRIES_BY_MEETING`(쟁점 수 + 2, 가설 13), 「전부 내기」 막기(`r13_v111_proof_kept`), 정답 판정은 정답 세트 합집합까지 받음(`r13_v111_proof_accepts`), 3일 칼 쟁점 정답 보기 상시(회의 진입 조건에서 칼 동의 뺌), 틀렸을 때 아빠 속말 장치(`R13_NW_WRONG_THOUGHTS` — 아직 비어 있음, 기본 문구만), 맞물림 1·3·4·5 대사. 보고 `docs/reviews/codex-01/적용보고.md`.

## 5. 다음 할 일 (위에서부터)
1. 용량 정리·리팩토링(소유자 2026-10-24 「끝나면 리팩토링하면서 용량 정리」): ① 큰 파일·안 쓰는 그림·오래된 캡처·PNG/WebP 중복 목록을 소유자에게 먼저 보이고 승인 뒤 삭제(git 기록 축소는 강제 push가 필요해 따로 묻는다) ② 이야기 쪽(대사 패치·조건·회의 데이터) 리팩토링, 동작 불변·화면 시험으로 확인.
2. 지시서 02 — `docs/codex/지시서_02_감정선_다섯.md`
3. 회의 11개 쟁점별 「틀렸을 때 아빠 생각 줄」 채우기 — 장치는 01에서 만들었다. `game/room13_v111_newworld_rules.rpy` 의 `R13_NW_WRONG_THOUGHTS["<증명 키 또는 menu:trial_knife / menu:hyp0~5>"]={1:...,2:...,3:...}` 에 넣는다. 2번째는 상대 주장의 한 구절, 3번째부터 자료의 종류까지(이름·정답 금지, MEETING_RULES_V2 6장 1번). 쟁점 키 목록은 `story_master_auto.md` 2장.
4. 기회를 다 썼을 때 「결과를 받아들인다 / 회의를 처음부터 다시」 화면(시안 먼저) — 지금은 「다 있었다」 줄만 대사 묶음 끝에 붙는다.
5. 대승리 7일·12일 퍼즐(`GRAND_WIN_DESIGN.md`)
6. 부엉이 예방 퍼즐(`OWL_PREVENTION_DESIGN.md` 9·10장 — 7일 낮 자유 시간 필요)
7. 불타는 밤(`docs/reviews/wild-night-20261024/지시서.md`, 결정 `WILD_NIGHT_DESIGN.md` 6장)
8. 숨겨진 에피소드 시안(판돌, `HIDDEN_WILD_FAMILY.md`)
9. 나머지 예방(피코·꼬미·네로·12일 국·13일 군중)을 물건 퍼즐 문법으로(`회차구조_검수.md` 우선순위)

## 6. 갱신 기록
- 2026-10-24: 0.20.29 공개, 용량 정리(예전 캡처 1.2GB) 완료.
- 2026-10-24: 처음 작성.
- 2026-10-24: 지시서 01 반영(결함 둘, 회의별 기회 수, 전부 내기, 아빠 속말 장치, 맞물림 1·3·4·5). 「지금 상태」·「다음 할 일」 갱신.
- 2026-10-24: 이야기 총정리 — 생성 도구 `dev/story_master.py`(+시험 `dev/test_story_master.py`), 자동 부분 `docs/design/story_master_auto.md`, 사람이 쓰는 부분 `docs/design/story_master.md`, 분기표 `branch_table.html` 갱신(진엔딩 승격, 회의 부분 결과 6곳, 회의별 기회 수, 감독자 연쇄 없음, 노인 밤 구조). 「다음 할 일」 1·10번을 지우고 번호를 맞춤.
