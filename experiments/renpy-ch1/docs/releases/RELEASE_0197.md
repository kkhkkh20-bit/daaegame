# 0.19.7 — 이전 판 저장 불러오기 오류, 검수에서 나온 코드 오류

## 소유자 보고
0.19.6에서 저장을 불러오자 `Could not find return label ('game/room13.rpy', 980342182, 975)`로 멈췄다.

## 원인
- 웹 빌드는 매번 .rpyc 없이 처음부터 컴파일했다.
- 그래서 Ren'Py가 `call`마다 자동으로 붙이는 돌아갈 자리 이름이 판마다 모두 바뀌었다.
- 대화·장면 안(호출 중)에서 만든 저장은 다음 판에서 돌아갈 자리를 찾지 못했다.

## 바꾼 것
- `dev/build_web.py`
  - 컴파일 전에 직전 공개본(game.part*)의 .rpyc를 스테이지에 넣는다.
  - 바뀌지 않은 `call` 문은 Ren'Py가 예전 이름을 이어 쓰므로, 다음 판부터 저장이 깨지지 않는다.
- `systems/room13_return_recovery.rpy`: 이미 깨진 저장을 위한 장치다.
  - `config.return_not_found_label = "r13_return_lost"`로 둔다.
  - 돌아갈 자리를 못 찾으면 하던 장면을 건너뛰고 안내를 띄운 뒤 가까운 안전한 자리로 보낸다(아래 복구 보강).
  - Room13 상태가 없으면 메인 메뉴로 간다.
- 복구 보강(저장 호환 재검토 반영)
  - `config.load_failed_label`도 같은 라벨로 보낸다. 되감기 기록에 남은 문장이 하나도 없는 0.19.5 이전 저장도 멈추지 않는다.
  - 복구할 때 회의·장면 상태(`r13_meeting_*`, `r13_cg_active` 등)와 회의 화면을 끈다. 그 뒤 날짜 분기(`r13_day`)로 보내므로 재판일에는 재판으로, 2주차에는 2주차 분기로 간다.
  - 피날레 중이면 제단 화면, 첫날 도입 중(E01 전)이면 처음부터, 결말 뒤에는 메인 메뉴로 보낸다.
  - 빌드는 이전 공개본 part가 있는데 .rpyc를 하나도 넣지 못하면 실패한다(조용히 이름이 다 바뀌는 일을 막는다).
- 웹 메모리: 게임 파일을 푼 뒤 남던 `/game.zip`(약 18MB)을 지운다(`systems/room13_web_memory.rpy`). 휴대폰에서 WebGL 화면을 만들 여유를 조금 늘린다.
- 소유자 요청: 마차에서 다람이가 "왁!" 할 때의 효과음을 더 밝고 튀는 소리로 바꿨다(`assets/sfx-surprise.wav`, 키 `surprise`, 생성기 `dev/make_sfx_surprise.py`). 위로 튀는 보잉 소리 뒤에 도·미·솔·도 반짝임이 이어진다.
- 검수에서 나온 코드 오류
  - `systems/room13_relations.rpy`: 만난 사람이 칸(30)보다 많으면 「전체 관계도」가 KeyError로 멈췄다. 관계선이 있는 사람부터 칸을 주고, 칸 밖 사람은 격자에 그리지 않는다(아래 얼굴 줄에는 그대로 나온다).
  - `room13_notebook.rpy`·`room13_screens.rpy`: 「안 읽음」 거름이 자기 목록을 하나씩 읽음 처리해 비웠고, 보여주기 화면에서는 제시 단추가 꺼졌다. 거름이 켜진 동안 읽은 기록은 거름을 바꾸거나 화면을 다시 열 때까지 목록에 남는다.
  - `systems/room13_time_flow.rpy`: 7일 오전에도 지나간 "6일 저녁 학교에서 미리 열 수 있다"를 안내했다. 그날 밤까지만 붙인다.
  - `systems/room13_alibi.rpy`: 사건 날 행동 문구 키가 옛 사건일 4로 남아 있어 4일 저녁에 사건 문구가 미리 나오고 7일에는 빠졌다. `R13_CASE_DAY`로 바꿨다.
- 정본 문서 두 개(`CASE13_CANON_SYNC.md`, `CURRENT_STORY_DECISIONS.txt`) 머리에 지금 날짜표(사건 7일)와 이번 검수에서 정한 사실을 적었다.

## 검증
- `dev/check.sh`: 단위 235개 통과, lint ok.
- 새 화면 테스트
  - `lost_return`: 복구 장치가 없으면 소유자 화면과 같은 예외가 나는 것을 확인했고, 있으면 장소 화면으로 돌아온다.
  - `relgrid_overflow`
  - `unread_filter_keeps`
- `stale_meeting`: 재판 토론판에서 호출 스택을 모두 없는 이름으로 바꿔도, 회의 화면이 남은 채 돌아다니지 않는다.
- `carriage_pop`: 0.19.5 마차 순서에 맞게 고쳤다. 0.19.6에서도 실패하던 테스트다. 이제 새 효과음을 확인한다.
- 브라우저(새 빌드)
  - 0.19.7로 시작하고 렌더러가 정상이다.
  - `/game.zip`이 지워졌다.
  - 복구 라벨 두 개가 설정됐다.
- `dev/qa_carriage.py`, `qa_save_slots.py`, `qa_navigation.py`는 0.19.6 공개본에서도 같은 자리에서 실패한다. 0.19.1~0.19.5 화면 변경 뒤 스크립트를 고치지 않아 생긴 실패다(다음 판에서 정리).
- 기존 테스트 `relations_tab`, `time_flow`, `alibi_cross`, `owner_fixes_0192`, `present_portrait`.
