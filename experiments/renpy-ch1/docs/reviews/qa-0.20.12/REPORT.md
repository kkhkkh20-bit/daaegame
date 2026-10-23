# 0.20.12 시험·웹 빌드·화면 확인 보고

작업일: 2026-10-23. 대상 커밋: `95a64986`. 게임 버전: 0.20.12.

| 항목 | 결과 | 근거 파일 |
|---|---|---|
| 단위 시험 | **통과: 894개**, 57.983초 | [check.txt](check.txt) |
| Ren’Py lint | **통과** (`lint: ok`) | [lint.txt](lint.txt), [check.txt](check.txt) |
| 지정 화면 시험 70개 | **통과 0개 / 정상 완료하지 못함 70개**. 시험 본문의 통과·실패 판정은 불가 | [renpy-run.txt](renpy-run.txt), 아래 시험별 표 |
| 웹 빌드 | **완료, 종료 코드 0**. SDK 공통 캐시 쓰기 오류가 함께 출력됨 | [build.txt](build.txt), [build-report.json](build-report.json) |
| PC 자료 목록 | **확인 못 함**. `book-pc.png` 생성 못 함 | [browser-pc.json](browser-pc.json), [browser.txt](browser.txt) |
| 휴대폰 자료 목록 | **확인 못 함**. `book-mobile.png` 생성 못 함 | [browser-mobile.json](browser-mobile.json), [browser.txt](browser.txt) |
| 창고 오후 좌·우 끝 | **확인 못 함**. `woodshed-left.png`, `woodshed-right.png` 생성 못 함 | [http-server.txt](http-server.txt), [browser.txt](browser.txt) |
| 창고 저녁 | **확인 못 함**. `woodshed-evening.png` 생성 못 함 | [browser.txt](browser.txt) |
| 보호시설 좌·우 끝, 벽화·돌판 | **확인 못 함**. `facility-left.png`, `facility-right.png` 생성 못 함 | [browser.txt](browser.txt) |
| 긴 이름 세 줄·● 그림 모서리 | **실제 화면 확인 못 함** | [browser.txt](browser.txt) |
| 페이지 오류·Ren’Py 예외 화면 | **확인 못 함**. 브라우저가 페이지를 열기 전에 종료됨 | [browser-pc.json](browser-pc.json), [browser-mobile.json](browser-mobile.json) |
| PC 1280×720 저장→새로고침→불러오기 | **확인 못 함** | [browser-pc.json](browser-pc.json) |
| 휴대폰 844×390 저장→새로고침→불러오기 | **확인 못 함** | [browser-mobile.json](browser-mobile.json) |

## 실행 조건과 원인

- 안내 문서는 지정된 `experiments/renpy-ch1/ROOM13_GUIDE.md`가 없어 저장소 루트의 `ROOM13_GUIDE.md`를 읽었다. 릴리스 문서·시험 목록·참고 스크립트는 프로젝트 내부 `docs/`에서 읽었다. 보고서도 프로젝트 내부 `docs/reviews/qa-0.20.12/`에 기록했다.
- 요청한 `dev/check.sh`를 SDK 경로와 함께 실행했다. 단위 시험과 lint는 통과했다.
- 화면 시험 첫 실행은 `renpy.pygame.error.error: No available video device`와 `RuntimeError: Exception occurred outside of a testcase or hook.`로 중단됐다. `SDL_VIDEODRIVER=x11` 및 `offscreen`을 지정한 단일 시험 재시도도 각각 `x11 not available`, `offscreen not available`로 중단됐다.
- 이후 **`ROOM13_TEST_TIMEOUT=5`**를 지정하여 목록의 70개 이름 전부를 `dev/run_renpy_tests.sh`에 전달했다. 반복되는 초기화 오류에 대한 대기를 줄인 실행이며, 정상적인 전체 화면 회귀를 완료한 것으로 볼 수 없다. 개별 로그의 원래 위치는 `/tmp/room13-qa/renpy/<이름>.txt`다. 이번 실행의 독립 집계는 `renpy-run.txt`에 보존했다.
- 공용 `/tmp/room13-qa/renpy/`에서 일부 파일이 이번 실행 후 다른 실행 결과로 교체되는 현상을 확인했다. 그 파일에 나중에 나타난 통과·실패는 이번 실행 집계에 합산하지 않았다. 아래 오류 줄은 보존된 이번 실행 집계에서 가져왔다.
- 수정 후보는 게임 코드가 아니라 **Ren’Py SDK/SDL의 사용 가능한 영상 드라이버와 Xvfb 실행 환경**이다. 현재 증거만으로 특정 게임 함수의 결함을 판정할 수 없다.
- 웹 빌드는 지정된 `python3 dev/build_web.py --sdk /root/.cache/renpy/renpy-8.5.3-sdk`로 실행했고 산출물은 손으로 수정하지 않았다. SDK의 `renpy/common/*.rpyc`, `*.rpymc`에 쓰려는 단계에서 `OSError: [Errno 30] Read-only file system`이 출력됐지만 빌드는 최종 보고서를 출력하고 0으로 종료했다. SDK 캐시를 쓸 수 있는 실행 환경에서 재검증이 필요하다.
- `python3 -m http.server 8766`은 소켓 생성 단계에서 `PermissionError: [Errno 1] Operation not permitted`로 종료됐다. 지정 Chromium을 Playwright로 PC·휴대폰 각각 실행하려 했으나 두 경우 모두 `setsockopt: Operation not permitted` 및 `SIGTRAP`으로 시작하지 못했다. 서버 및 Chromium 소켓 사용이 허용되는 환경에서 다시 실행해야 한다. 승인 요청이나 권한 우회는 하지 않았다.
- [browser_qa.py](browser_qa.py)는 `dev/webqa.py`의 `QA`를 사용하는 재실행용 검사 스크립트다. 새 이야기 시작, 자료 주입, 긴 이름 페이지, 카메라 좌우 끝, 설정창 저장·새로고침·불러오기 순서가 들어 있으나 **브라우저 본문은 실행되지 않아 검증되지 않았다**.
- 서버 정리는 시작한 프로세스 PID에 `kill`을 보내는 `trap`으로 처리했다. `pkill -f`는 사용하지 않았다.

## 웹 빌드 근거

- 핵심 아카이브: 14,982,246바이트, 1개 조각. 첫 로딩: 27,699,737바이트.
- 아카이브 SHA-256: `2267433ca2b5fa86f53003230c15e3d5c629f5cfbd473a86b46f6eb5313f76f5`. 생성된 `game.part01`의 실제 SHA-256과 일치했다.

## 화면 시험별 오류

아래 70개는 정상 판정을 얻지 못했다. 오류가 있는 항목은 시험 본문 밖 예외이며, 해당 줄만으로 게임 코드 실패를 뜻하지 않는다.

| 시험 이름 | 결과 | 이번 실행의 오류 줄 |
|---|---|---|
| `v111_opening_native` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_fork_screen` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d01_gate_lost` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d01_gate_won` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d01_gate_extra_letter` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d03_lamp_lost` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d03_lamp_partial` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d03_lamp_won` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d05_half_then_lost` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d05_extra_e21_wins` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d07_fire_lost` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d07_fire_partial` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d08_room_stone` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d10_room13_half_then_lost` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d10_room13_partial` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d10_records_lost` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d10_records_partial` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d10_room13_won` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d07_stone_out` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d10_five_chances` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d10_owner_contact_pin` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d11_hyp_lost` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d11_hyp_wrong_reason` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d11_hyp_partial` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d11_hyp_won` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d11_hyp_stone_proof` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d11_hyp1_two_records` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d12_morning_list` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d12_soup_list_partial` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d12_soup_won` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d12_soup_lost_nabi` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d12_portrait` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d13_cart_left_with_daram` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d13_badook_partial` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d13_cart_names` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d13_rein_won` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d13_rein_painting_first` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d13_partial_listed` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d14_left_name` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d14_frozen` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d14_partial_departed` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d14_altar_lost` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d14_altar_half_then_partial` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d14_bomi` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d14_true_ending` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_d14_altar_without_records` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `v111_nw_relations` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `acorn_preview` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `evidence_facts_engine` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `evidence_large_touch` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `extra_faces` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `zz_forest_box` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `gate_zoom` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `gate_zoom_times` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `idle_resident` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `impact_preview` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `impact_save` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `more_save_karo` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `morning_path` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `night_ui_preview` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `owner_play_fixes` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `proof_pick` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `reaction_days` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `reaction_followup` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `relations_reveal` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `scene_cuts` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `settings_touch` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `story_pose` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |
| `ui_current` | 확인 불가 | 상태·오류 줄 없이 종료 |
| `v111_nw_d13_cleanup_bundled` | 확인 불가 | `RuntimeError: Exception occurred outside of a testcase or hook.` |

## 변경 범위

게임 코드·원본 그림·이야기 파일은 수정하지 않았다. 변경은 웹 빌드 산출물과 이 QA 폴더다. 커밋·푸시는 하지 않았다. 캡처와 저장 복원 확인이 완료되지 않았으므로 화면 검증 완료로 승인할 수 없다.
