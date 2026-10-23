# Codex 작업 지시 — 0.20.12 시험·웹 빌드·화면 확인 (2026-10-23)

저장소: `/home/claude/daaegame`. 게임 원본: `experiments/renpy-ch1/`. 먼저 `experiments/renpy-ch1/ROOM13_GUIDE.md`와 `docs/releases/RELEASE_0.20.12.md`를 읽는다. 보고·기록은 모두 한국어로 쓴다.

이번 변경(이미 main에 커밋됨, 코드는 고치지 않는다 — 실패하면 원인과 고칠 곳만 보고):
1. 13일 구조 뒤 다섯 확인을 세 대화로 묶음(`game/room13_v111.rpy` r13_v111_binding, `game/room13_v111_days1114.rpy` order_stop13·driver_refuse13).
2. 새 배경: 6일 장작 창고 안(`v111_woodshed`, 폭 2400), 보호시설 오른쪽 벽 확장·벽화(`facility`, 폭 2400) — `game/room13_v111_later_bindings.rpy` 맨 아래 init 318.
3. 자료 목록 이름 세 줄(`game/systems/room13_evidence_view.rpy` r13_evidence_grid, r13_ev_two_lines).

## 할 일 (순서대로)

1. 단위+lint: `cd experiments/renpy-ch1 && RENPY_SDK=/root/.cache/renpy/renpy-8.5.3-sdk dev/check.sh` → 결과 요약.
2. 화면 시험: 목록 `docs/codex/qa_names_0.20.12.txt`의 시험 이름 전부를 `RENPY_SDK=/root/.cache/renpy/renpy-8.5.3-sdk dev/run_renpy_tests.sh <이름들>`로 실행(로그 `/tmp/room13-qa/renpy/<이름>.txt`). 통과/실패 개수, 실패한 시험의 오류 줄.
3. 웹 빌드: `python3 dev/build_web.py --sdk /root/.cache/renpy/renpy-8.5.3-sdk` (결과 `preview/room13-dev/`, 손으로 고치지 않는다). 버전은 이미 0.20.12.
4. 브라우저 확인(`preview/room13-dev`를 `python3 -m http.server 8766`로 띄우고 Playwright, 크롬 `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, `dev/webqa.py`의 QA 클래스 사용. 참고 스크립트: `docs/codex/ref_scripts/`). 캡처는 `docs/reviews/qa-0.20.12/`에 저장:
   - `book-pc.png`, `book-mobile.png`: 새 이야기 시작 후 현장(r13_hub)에서 모든 `V111:` 자료를 가진 상태로 자료 목록(r13_book). 긴 이름이 세 줄(PC)로 끝까지 보이는지, ● 표시가 그림 모서리에 있는지.
   - `woodshed-left.png`, `woodshed-right.png`: location `v111_woodshed`, period 1, 화면을 왼쪽 끝·오른쪽 끝으로 옮긴 두 장. `woodshed-evening.png`: period 2.
   - `facility-left.png`, `facility-right.png`: location `facility`, period 1. 오른쪽 끝에 벽화·돌판이 보이는지. 화면 옮기기는 현장의 좌우 이동 화살표를 실제로 누르거나 `r13_world_cameras` 값을 바꾼다.
   - 각 화면에서 페이지 오류(pageerror)·Ren'Py 예외 화면이 없는지.
   - 저장·불러오기: 설정창 → 저장 1쪽 1번 저장 → 새로고침 → 불러오기 → 같은 날짜·장소인지(PC 1280×720, 휴대폰 844×390 두 번).
5. `docs/reviews/qa-0.20.12/REPORT.md`에 위 결과를 표로(항목, 결과, 근거 파일). 확인 못 한 것은 못 했다고 적는다.

## 지킬 것

- 게임 코드·그림·이야기 파일은 고치지 않는다(시험 실패 원인 분석만). `git commit`·`git push`는 하지 않는다(검토 뒤 Claude가 한다).
- `pkill -f`로 자기 셸을 죽이지 않게, 서버는 끝나면 PID로 끈다.
