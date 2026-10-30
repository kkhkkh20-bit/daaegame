# 정리(B안) 인계 — 2026-10-30

다음 세션은 이 문서부터 읽는다. 소유자 결정: 새로 만들지 않고(C안 시범 뒤 철회) 지금 판(renpy-ch1)을 정리한다.
게임 동작·대사·화면 모양은 바꾸지 않는다. 단계마다 전후 숫자를 소유자에게 보고한다.

## 지금 상태

- 공개판: 0.20.89 (`main`, Pages `preview/room13-dev`). 지금 판의 마지막 공개.
- 작업 브랜치 `claude/cool-gates-s9msjz` 에 있고 아직 공개하지 않은 것:
  - `ba57e9de` 웹에서 표정이 바뀔 때 인물이 잠깐 비던 것(다음 3줄 그림 미리 받기, 대화 중 지우지 않기, 못 받았으면 앞 화면 유지 — `game/systems/room13_web_art_ready.rpy`, 스위치 `R13_WEB_ART_READY`), 마차 다람 앉은 자세를 도트 3배 대신 붓 원본으로.
  - `c101e4cf`·`d6e10117` 그림 요청 DLG-HIRES-155(대사 장면 인물 고해상 원본) — **보류**. 소유자: 「이미지는 나중에 전수조사해서 품질 떨어지는 것만 골라 요청」.
  - `9b9b57bf` 작업 규칙: 전체 화면 회귀는 날마다가 아니라, 고칠 것을 다 고친 뒤 공개 직전에 한 번.
- 새 판(C안) 시범은 참고용으로 남김: `experiments/room13-v2/`(1일 시범, 추출 `extract/` — 1~14일 지도·기능·그림 목록), 웹 `preview/room13-v2/`. 더 만들지 않는다.

## 정리 단계(소유자 승인 순서)

1. **안 쓰는 것 빼기** — 지금 이야기(v111)에서 닿지 않는 옛 판 코드(재판·상점·생계·장터·옛 사건·저녁 미션 등)와 그 시험, 확실히 안 쓰는 그림. **진행 중 멈춤(커밋 없음).**
2. 조사 화면 속도 — 클릭마다 화면 전체를 다시 계산하는 부분(새 판은 0.06~0.09ms, 지금 판 약 47ms).
3. 덮어쓰기 합치기 — 함수 114개·층 381(최대 24겹, `docs/OVERRIDE_MAP.md`)을 층 많은 것부터 하나로.
4. 대사 한 곳으로 — rpy 에 직접 쓴 대사를 `game/v111/newworld/dNN.json` 으로, 생성기(`dev/build_v111_days*.py`)와 줄 수 고정 파일(days123 1467, later_bindings 263, interaction 307) 없애기.

## 1단계 이어 하기

- 중간 결과를 패치로 보관했다(작업 트리는 깨끗하게 되돌림):
  - `b1_wip_first_attempt.patch` — 첫 시도(파일 16개, 옛 사건·옛 시험 빼기). 이 시도 뒤 시험이 깨져 작업자가 되돌렸다.
  - `b1_wip_second_attempt.patch` — 두 번째 시도(파일 9개, 78줄 삭제). 단위 시험을 돌리기 직전에 멈췄다 — **검증되지 않음**.
  - `b1_dead_spans.json` — 정적 분석으로 고른 「닿지 않는」 label·def·변수 위치(파일별 줄 범위).
  - 두 패치 모두 `git apply --check` 통과(2026-10-30 기준). 그대로 믿지 말고 다시 확인하며 작은 묶음으로 적용한다.
- 출발점: `experiments/room13-v2/extract/INVENTORY.md`(시작에서 닿는 label 856, v111 안에서 닿지 않는 label 8), `FEATURES.md`(버릴 옛 기능 표), `ASSETS.md`(확인 사용 248개 120.5MB / 후보 3,770개 405MB / 미사용 872개 188.6MB).
- 지켜야 할 것: 동적 이름(문자열 조합·getattr·globals().get·renpy.has_label)으로 불릴 수 있으면 남긴다. 옛 저장 호환용 store default 는 남긴다. 「후보」 그림은 실행 로그로 가린 뒤 소유자 확인을 받고 뺀다.
- 통과 기준(모든 묶음 뒤): v111 화면 회귀 158개 중 153개 통과(실패 5개는 이전부터: `v111_opening_native`, `v111_ar_d05_iron`, `v111_evidence_drawer`, `v111_rules_tries_table`, `v111_nw_d14_bomi`), 웹 빌드 후 `dev/qa_autoplay.py` 기본 길 `ERRORS []`, 단위 시험·lint·`dev/dialogue_logic_check.py` A/B/C 0. 이것이 같아야 다음 단계로 간다.

## 실행할 때 주의(이번 세션에서 실제로 막힌 것)

- Ren'Py 를 띄우는 명령(화면 시험·웹 빌드·lint)은 한 번에 하나: `flock -o /tmp/room13-renpy.lock <명령>`. **`-o` 를 꼭 붙인다** — 없으면 xvfb-run 이 남긴 Xvfb 가 잠금을 쥐어 다른 실행이 모두 멈춘다.
- 화면 시험은 시험 이름을 반드시 넘긴다. 비우면 옛 기본 목록 116개가 돈다.
  v111 회귀: `T=$(grep -hoE "^testcase [a-z0-9_]+" game/qa_tests/v111*.rpy game/qa_tests/kkomi_puzzle.rpy | awk '{print $2}' | tr '\n' ' ')`
- 세션 디스크 할당량이 작다(가득 차서 브라우저가 멈췄다). 브라우저 프로필·연속 캡처·`/tmp/room13-build` 는 쓰고 지운다.
- 웹 확인용 빌드 결과(`preview/room13-dev`)는 커밋하지 않는다. 확인 뒤 `git checkout -- preview/room13-dev`.
- 웹 표정 깜빡임 재측정: `web_art_flash_measure.py`(로컬 서버 + Playwright, 새 프로필, 느린 회선 흉내).

## 남은 결정·할 일

- 이미지 전수조사(정리 뒤): 품질이 떨어지는 그림만 골라 DLG-HIRES-155 를 좁혀 확정. 원본이 없어 도트로 남은 다섯 벌(npc_panseol, v111_lowerroad_elder, v111_patrol, v111_resident, v111_child)은 그림 요청 DLG-SMOOTH-DOTONLY 로 등록돼 있다. 3일 광장 꺼진 3번 등 SQ-LAMP3-OFF 도 등록돼 있다.
- 시안 대기(지금 판에 넣지 않음): 지도 끌어 옮기기 표시, 고른 근거 강조, 휴대폰 3일 회의 셋째 선택지와 「더보기」 리본 겹침.
- 정리 단계가 끝나 회귀를 통과하면 위 미공개 수정과 함께 0.20.90 으로 공개(공개 순서는 `CLAUDE.md`).
