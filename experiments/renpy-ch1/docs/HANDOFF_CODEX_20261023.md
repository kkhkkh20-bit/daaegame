# Codex 인계 문서 (2026-10-23)

소유자 결정(2026-10-23): "코덱스에게 작업 이관하자. 새로 내가 코덱스 개발과 리뷰를 맡길게." 개발(구현·시험·빌드·그림)과 코드 리뷰는 소유자가 직접 Codex에 맡긴다. Claude는 로직·대사 검수와 기획을 맡는다(아래 역할표).

먼저 읽을 것: `ROOM13_GUIDE.md`, 저장소 루트 `CLAUDE.md`(작업 규칙), `docs/design/PLAN_20261023_NEXT.md`(다음 개발 계획), `docs/reviews/audit-20261023/AUDIT_review20261021.md`(검토 보고 반영 현황).

## 1. 지금 상태

- 공개본: **0.20.11** (GitHub Pages, `preview/room13-dev/`).
- main 원본: **0.20.12** 준비 완료(공개 전). 릴리스 노트 `docs/releases/RELEASE_0.20.12.md`.
  - 13일 구조 뒤 다섯 확인 → 바둑이·돌목·까로 세 대화(후반 기획서 C안). 화면 시험 `v111_nw_d13_cleanup_bundled` 추가.
  - 6일 장작 창고 안 새 배경(2560×768, 표시 폭 2400), 보호시설 오른쪽 벽 확장·벽화(폭 2400). 등록: `game/room13_v111_later_bindings.rpy` 맨 아래 `init 318`. 그림 원본 `art/bg-woodshed-mural-20261023/round2/`.
  - 자료 목록(PC) 이름 세 줄·글자 폭 계산·안 읽음 ● 그림 모서리(`game/systems/room13_evidence_view.rpy`).
- 0.20.12 확인 진행 상황:
  - `dev/check.sh`(단위 894 + lint) 통과.
  - 화면 시험 70개: Codex 환경에서는 가상 화면(xvfb)이 안 떠 실행 불가. Claude가 돌리던 중 **웹 빌드와 동시에 돌려 저장 폴더 충돌**(`game/saves/persistent.*.tmp` 없음)로 `v111_fork_screen` 1건 실패 — 게임 오류 아님. **빌드·브라우저 QA가 끝난 뒤 단독으로 다시 돌려야 한다.**
  - 웹 빌드·브라우저 캡처·저장 확인: Codex 작업 `docs/codex/TASK_0.20.12_QA.md` 진행 중, 결과는 `docs/reviews/qa-0.20.12/REPORT.md`.
  - 공개(커밋·push)는 위 확인 뒤.

## 2. 다음 개발 (소유자 승인 2026-10-23: 1단계 + 2단계 시범, 13호실은 지금 구조 유지)

`docs/design/PLAN_20261023_NEXT.md` 참고. 요약:
- P1 13일 촌장 담요 거짓말을 아빠의 질문 메뉴로 단계적으로(촌장이 묻지 않은 세부를 먼저 말하지 않게).
- P2 3일 「판 것과 훔친 것은 다르다」 질문 선택.
- P3 제시 직후 아군·상대의 자동 해설 줄이기(3일 톡 걸쇠, 5일 다람 시간차, 10일 상처 대조 뒤).
- P4 10일 종이 수량·날짜 대조를 자료 제시 입력으로, 기록 승리는 대조 뒤 기록.
- P5 12일 ‘새 물’ 주장 확인을 현장 조사 지점 확인 뒤 진행, E12_HANDLING은 확인 뒤 지급.
- P6(시범) 3일 칼 접합 뒤 회의를 멈추고 등돌 안쪽을 다시 조사해 E17을 그때 얻기. 새 화면 없이 wait/travel/proof 조합.
- 13호실 밀실 재설계(A)는 하지 않는다(지금 구조 유지). 할머니 수첩 내용(B)·누비 동기(C)는 진상 결정 전 착수하지 않는다.
- 결말·생사·정답 판정은 바꾸지 않는다. 바꿔야 하면 멈추고 보고한다.

## 3. 반드시 지킬 개발 규칙(요약, 전문은 CLAUDE.md)

- 웹판은 `dev/build_web.py`로만. `preview/room13-dev/`를 손으로 고치지 않는다.
- 대사를 `call r13_lines([...])` 안에 튜플로 직접 넣지 않는다(literal inventory 행 수가 바뀐다). `game/v111/newworld/dNN.json`의 `blocks`(→ `r13_nw_block('이름')`)나 `r13_nw_added_line(dict(...))`를 쓴다. 생각 대사는 `kind="thought"`.
- 수정 뒤 갱신: `python3 dev/refresh_intake21_lines.py`, `python3 dev/refresh_literal_lines.py`, `python3 dev/override_map.py --write`, `python3 dev/build_dialogue_bindings.py`.
- `game/room13_v111_later_bindings.rpy`의 `init N python:` 블록 사이에 0열 주석을 두지 않는다(`dev/test_v111_continuation.py`가 블록을 dedent해 읽는다).
- 장소·조사 지점 덮어쓰기는 등록(init 310~312) **뒤** init에서 한다.
- UI·메인화면 디자인 변경은 이미지 시안 → 소유자 승인 → 적용.
- 관찰 사실·생각 대사에 정답 단서를 글로 적지 않는다. 인물이 플레이어보다 먼저 추리하지 않는다.
- 화면 시험과 웹 빌드는 **동시에 돌리지 않는다**(같은 `game/saves`를 쓴다).
- 커밋 메시지·보고는 한글. 커밋 끝 두 줄(Co-Authored-By, Claude-Session)은 Claude가 커밋할 때만.

## 4. 역할 분담

| 일 | 맡는 쪽 |
|---|---|
| 구현(코드·데이터·화면), 단위 시험·화면 시험 추가, 웹 빌드, 브라우저 캡처, 그림 제작 | Codex (소유자가 지시) |
| 코드 리뷰 | Codex (소유자가 지시) |
| **로직 검수**: 분기 조건·플래그·판정 값이 의도와 맞는지, 자료 획득 시점과 회의 정답 조합, 생사·결말 판정 불변 확인, 막히는 경로·미연결 분기 | Claude |
| **대사 검수**: 앞뒤 설정·시간선, 인물 말투, 인물이 먼저 추리하거나 정답을 말하는지, 같은 사실 반복, 경로마다(증인 부재·자료 미획득) 대사가 자연스러운지 | Claude |
| 기획: 다음 개발 거리 정리, Codex 지시서 초안, 검토 보고·플레이 리뷰를 항목으로 쪼개기 | Claude |
| 화면 시험 실행(Codex 환경에서 불가), main 반영·공개(push), 소유자 보고 | Claude |
| 디자인·진상 결정, 적용 승인 | 소유자 |

### Claude에게 검수를 맡길 때 넘길 것

- 바뀐 커밋(또는 diff)과 의도 한 줄.
- 대사를 바꿨으면 해당 `dNN.json` 키·대사 ID, 바뀐 라벨.
- Claude는 검수 결과를 `docs/reviews/logic-dialogue/검수_<날짜>_<주제>.md`에 「문제 / 근거(파일·ID) / 고칠 방향」으로 남기고, 판정·생사에 닿는 문제는 따로 표시한다.
