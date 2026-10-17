# 저장/불러오기·예전 저장 호환 검토 (읽기 전용, 2026-10-17)

대상: `experiments/renpy-ch1` (0.19.7 WIP), SDK 8.5.3. 원본 폴더는 고치지 않았다. 실험은 사본(`scratchpad/savecopy`, `rel_seed`, `rel_fresh`)에서만 했다.

## 확인된 사실 (Ren'Py 8.5.3 코드 기준)
- 불러오기 순서: 저장의 현재 문장 이름이 없으면 `rollback_core`가 로그를 거슬러 **이름이 남아 있는 가장 최근 문장**(대개 `label`)까지 되돌린 뒤 그 자리부터 다시 실행한다. 이때 예전 호출 스택은 그대로 남는다. 나중에 그 스택을 `return`할 때 `lookup_return`이 실패하고, 지금은 `config.return_not_found_label`로 간다. 이때 호출 스택은 전부 버린다.
- 로그 안에 남은 이름이 하나도 없으면 `load_failed()`가 실행된다. `config.load_failed_label`은 설정되어 있지 않으므로(기본값 None) 이 경우 예외가 난다.
- `merge_names`는 같은 경로의 이전 `.rpyc`와 `difflib`으로 문장을 맞춰 이름을 물려준다. `compile` 명령은 강제 재컴파일이지만, 재컴파일할 때도 이 병합을 거친다.

## seed_previous_rpyc 실측 (사본)
- 이전 공개본은 `preview/room13-dev/game.part01`, 0.19.6이며 이름 없이 새로 컴파일된 판이다. 같은 현재 소스로 빌드를 두 번 했다. 하나는 `--release rel_seed`(0.19.6 part 넣음), 다른 하나는 `--release rel_fresh`(part 없음)다.
- rpyc 2번 칸을 직접 풀어 비교한 결과(`scratchpad/tools2/rpycnames.py`, `verify_map.py`):

| 빌드 | 자동 생성 문장 이름 유지 | call 복귀 지점(Pass) 유지 |
|---|---|---|
| seed | 7850 / 8549 | **1402 / 1402** (1402개 모두 같은 call 문장에 연결되고 label·인자도 같다) |
| fresh(예전 방식) | 0 / 8549 | 0 / 1402 |

- 결론: 앞 판에서 바뀌지 않은 문장은 이름을 그대로 물려받는다. 바뀐 699개 문장은 새 이름을 받는다. 이런 문장에 멈춘 저장은 앞쪽 label로 되돌아가 다시 실행되므로 정상이다.

## 문제 목록

| 심각도 | 위치 | 문제 | 근거/재현 | 수정안 |
|---|---|---|---|---|
| 높음 | `systems/room13_return_recovery.rpy` `r13_return_lost` | 회의 도중에 만든 저장이 복구되면 `r13_meeting_active`, `r13_meeting_claim` 등 회의 상태가 그대로 남은 채 `r13_roam`으로 간다. 그 결과 HUD(날짜·시계·장소)가 사라진다. 이후 모든 대사창(`screen say`)과 선택지(`screen choice`)가 회의 무대·회의 선택지로 그려진다. `r13_speaker`도 회의 좌석 쪽으로 간다. 다음 회의에서 `r13_debate_run`이 False로 돌려 놓을 때까지 이어진다. | 사본에 테스트 `stale_meeting`을 추가해 실행했다. 재판 C2 토론판에서 return/call_location 스택 6개를 모두 없는 이름으로 바꾸고 "회의 중단"을 누르면 결과는 PASSED다. 복구 뒤 `r13_hub` 상태: `meeting_active=True claim=C2 stack=0`. 스크린샷 `savecopy/tests/screenshots/stale_after.png`에는 오른쪽 위 날짜·시계와 왼쪽 위 장소 틀이 없다. 근거 코드: `screens.rpy:121,226`, `room13_screens.rpy:12`, `room13_rules.rpy:297`. | 복구 라벨 앞부분에서 잠시만 쓰는 상태를 초기화한다. 대상 변수: `r13_meeting_active/intro/interrupting/replaying=False`, `r13_meeting_live_active=False`, `r13_meeting_pending_resume=None`, `r13_cg_active=False`, `r13_scene_key=None`, `r13_conv_skip=False`. 숨길 화면: `r13_material_corner`, `r13_meeting_cut_in`, `r13_meeting_rebuttal_hold`, `r13_rebuttal_cutin`, `r13_book`, `r13_calendar`. `r13_cutin_music_pause(False)`를 부르고 `show screen r13_hud`를 한다. |
| 높음 | 같은 곳 (재판일 분기 없음) | 재판일(day 10, `trial_ended=False`)에 복구되면 `r13_roam`으로만 간다. `r13_roam`에는 `r13_trial`로 가는 길이 없다(`r13_entry`·`r13_day`에만 있다). 그 상태에서 자면 `r13_next_day`로 11일이 되고, `r13_day`에서 `r13_week2_day`를 거쳐 `r13_week2_opening`으로 간다. 재판이 열리지 않은 채(`trial_result="pending"`) 2주차가 시작된다. | 코드 경로: `room13.rpy:254-267`(r13_day 분기), `room13.rpy:269`(r13_roam 분기 없음), `room13_interaction.rpy:266-279`(잠자기), `room13_week2.rpy:2-6,24-29`. | 복구 뒤 행선지를 `r13_day`와 같은 기준으로 정한다. 재판일이고 `trial_ended`가 False면 `jump r13_trial`로 간다. `r13_trial`은 닫힌 논점을 `r13_trial_choose`에서 거른다. |
| 중간 | 같은 곳 (결말·피날레) | `room13["ending"]`이 정해진 뒤(결말 시네마틱이나 이름판 도중, 그 직후 `force_autosave`가 있다) 복구되면 결말이 끝난 판에서 돌아다니게 된다. 이때 `hide screen r13_hud`는 그대로다. 피날레(`finale_started`, 제단) 도중이면 `r13_final_hub`로 돌아가는 길이 없다. 자고 나면 `r13_finale` 전체가 다시 재생된다. | `room13_week2.rpy:295-345`(r13_ending: hide r13_hud, call r13_cinematic, force_autosave), `room13_week2.rpy:181`(final_hub에는 r13_finale에서만 들어온다), `room13_week2.rpy:24-29`. | `ending`이 있으면 `jump r13_ending`(또는 `full_restart`)으로 보낸다. `finale_started`이고 `ending`이 없으면 `call r13_scene("r13_altar",...)`, `show screen r13_hud`, `jump r13_final_hub`로 보낸다. |
| 중간 | 같은 곳 (첫날 도입) | 마차 대화나 입구 등록 도중(`day=1`, `location="gate"`, `R13_PLACES`에 있음) 복구되면 `r13_roam`으로 간다. 그러면 `E01` 지급, 경비 대화, `r13_entry` 허브(entry=True, 명단 정정)를 모두 건너뛴 채 입구에서 바로 돌아다니게 된다. | `room13.rpy:86-130`(`room13_start`가 call r13_carriage 다음 E01 지급, 입구 대화, r13_entry 순서로 진행), `room13_rules.rpy:70`(r13_new location="gate"). | 도입이 끝났다는 표식이 없을 때의 처리를 둔다. 예: `"E01" not in evidence`이거나 입구 정정 플래그가 없을 때다. 이 경우 `renpy.full_restart(label="room13_start")`로 첫날을 다시 시작하거나 `jump r13_entry`로 보낸다. |
| 중간 | `config.load_failed_label` 미설정 | 0.19.6 이하 저장은 모든 자동 이름이 바뀐 상태다. 그 저장의 되감기 로그(최대 128개)에 지금도 남아 있는 이름(label 등)이 하나도 없으면, `return_not_found` 처리까지 가지 못한다. 불러오는 순간 "Couldn't find a place to stop rolling back" 예외가 난다. | SDK `renpy/rollback.py:848-871, 962-971`, `config.py:1036`(기본 None). 프로젝트 전체를 검색해도 설정하는 곳이 없다. | `define config.load_failed_label = "r13_return_lost"`를 추가한다. `load_failed`가 호출 스택을 비우고 그 라벨로 보낸다. 위의 상태 초기화·분기도 같이 적용된다. |
| 중간 | `dev/build_web.py` `seed_previous_rpyc` | (a) 이전 판 part가 없거나 깨진 zip이면 `seeded 0`만 출력하고 빌드는 그대로 성공한다. 이름이 조용히 모두 바뀌는 회귀가 다시 생길 수 있다. (b) 시드는 바로 앞 판에서만 가져온다. 0.19.6 공개본이 이미 새로 컴파일된 판이라 0.19.5 이하 저장은 시드로 살릴 수 없고 복구 라벨에만 의존한다. (c) 병합할 때 `game.part01`이 이진 충돌을 일으키면 작업 트리에는 내 쪽(ours) 빌드가 남는다. 그 상태로 다시 빌드하면 상대 세션이 이미 공개한 판의 새 문장 이름이 끊긴다. | 함수 본문(`except BadZipFile: return 0`, 경고·실패 없음). 사본 실측: part가 없는 `rel_fresh`는 복귀 지점 0/1402만 유지했다. | release에 part가 있는데 `seeded==0`이면 빌드를 실패시킨다. 빌드 보고서에 '이전 판 call 복귀 지점 유지 수/전체'를 적고, 크게 줄면 경고한다(`scratchpad/tools2/rpycnames.py` 방식). 가이드에는 '병합 뒤 다시 빌드할 때는 `git show origin/main:preview/room13-dev/game.part01`을 시드로 쓴다'를 적는다. |
| 낮음 | `r13_return_lost` 조건 | `room13_mode`를 확인하지 않는다. 지금은 `winter_start`가 `Start()`로 store를 새로 만들어 `room13`이 None이므로 실제 문제는 없다. | `winter.rpy:133-`, `winter_screens.rpy:279`. | 조건에 `room13_mode`를 더한다. |
| 낮음 | 에피소드 ②(다람 시점) 등 에피소드 내부 | 에피소드 도중에 복구되면 `pov="daram"`이 남은 채 돌아다니게 된다. 다만 `r13_town_events`에서 `r13_ep2_events`로 가는 경로가 `kd_done` 기준으로 에피소드를 처음부터 다시 시작해 스스로 회복된다. 다른 회의 에피소드(Q1~Q6)도 완료 플래그 기준으로 다시 열린다. 회의 직전 자동저장도 있다. | `systems/room13_ep2_kids.rpy:123-135,159-202`. | 복구 라벨에서 진행 중인 에피소드 플래그가 없으면 `pov`를 None으로 되돌린다. |
| 낮음 | `systems/room13_polish3.rpy` 아침 스냅샷 | `r13morning-N` 슬롯은 `renpy.load`로 바로 불러와서 `r13_save_status` 호환 확인을 거치지 않는다. 예전 판의 스냅샷도 같은 `run_token`이면 열린다. 이야기 개정은 `r13_upgrade`의 `revision_restart_required`가 막고, 이름 문제는 위의 복구가 맡는다. | `room13_polish3.rpy:79-90`, `room13_save_ui.rpy:20-26`. | 스냅샷 목록에서도 `r13_save_status(renpy.slot_json(slot))=="compatible"`인 것만 보여 준다. |
| 낮음(정보) | Ren'Py `merge_names` 특성 | `Call.diff_info`에는 인자가 들어가지 않는다. 같은 `call r13_lines(...)`가 연달아 있는 곳에 같은 꼴의 call을 끼워 넣으면 이름이 한 칸 밀려 대사가 반복될 수 있다. 엔진 특성이므로 이번 변경에서 실측한 차이는 없었다(1402개 모두 같은 대상). | SDK `renpy/script.py:556-570`. | 중요한 복귀 지점(회의·재판)은 지금처럼 `call ... from <이름>`을 쓴다(`r13_argument_debate_return`, `r13_crisis_debate_return` 등). |
| 정보 | 라벨·default·persistent | 확인 가능한 기록(얕은 클론, 2026-10-15부터) 안에서 지워지거나 이름이 바뀐 `label`이나 `call ... from` 라벨은 없다. 새로 생긴 store 변수(`r13_record_scrolls`, `r13_records_view`, `r13_book_views`, `r13_scene_bg` 등)는 모두 `default`가 있다. default 없이 쓰는 persistent 필드 2개(`r13_save_page`, `room13_opening_cut_seen`)는 `or 1`이나 대입으로만 써서 안전하다. `retain_after_load`는 화면 스크롤과 run_token에만 쓰여 문제가 없다. | `git log -p` 검색, `scratchpad/tools2/defaults.py`. | 조치 필요 없음. |

## 권장 복구 라벨 골격 (참고)
```renpy
define config.return_not_found_label = "r13_return_lost"
define config.load_failed_label = "r13_return_lost"

label r13_return_lost:
    window hide
    python:
        for _n in ("r13_meeting_active","r13_meeting_intro","r13_meeting_interrupting","r13_meeting_replaying","r13_meeting_live_active","r13_cg_active","r13_conv_skip"):
            setattr(store,_n,False)
        r13_meeting_pending_resume=None; r13_scene_key=None
        for _s in ("r13_material_corner","r13_meeting_cut_in","r13_meeting_rebuttal_hold","r13_rebuttal_cutin","r13_book","r13_calendar"):
            renpy.hide_screen(_s)
    if not (room13_mode and isinstance(room13,dict) and room13.get("day") and room13.get("location") in R13_PLACES):
        $ renpy.full_restart()
    $ renpy.notify("…")
    if room13.get("ending"):
        $ renpy.full_restart()            # 또는 jump r13_ending
    if "E01" not in room13.get("evidence",[]):
        $ renpy.full_restart(label="room13_start")
    show screen r13_hud
    if room13.get("finale_started"):
        call r13_scene("r13_altar","북쪽 산길 끝 · 숲속 제단","hearing")
        jump r13_final_hub
    if room13["day"]==R13_TRIAL_DAY and not room13.get("trial_ended"):
        jump r13_trial
    jump r13_roam
```
(첫날 도입 판정 플래그는 이야기 담당이 정한다. 위 코드는 예시다.)
