# 0.18.7-dev · 2026-10-14 — 장소 배경음 조정, 음량, 효과음·환경음 전체 연결 (소유자 지시)

소유자 요청
- 13호실도 객실과 같은 배경음으로.
- 진료소도 공방(수리점)과 같은 소리로.
- 비밀 통로 배경음이 너무 작다. 기본 음량을 키운다.
- 숲속 제단 노래도 음량을 키운다.
- 효과음과 환경음을 일단 다 넣는다.

## 배경음

- 13호실(`room`): 객실과 같게 평온·밤 Water Lily, 조사 Comfortable Mystery 4. 바람 환경음.
- 임시 진료실(`r13_clinic`): 수리점과 같게 평온 Heartwarming, 조사 Investigations, 밤 Comfortable Mystery 4. 시계 환경음.
  - 이야기 장면 "금요일 · 진료실 앞"도 같은 곡과 시계 소리.
- `bgm-dark.mp3`(The Long Dark: 비밀 통로·폐온실·보호시설), `bgm-altar.mp3`(Shadows and Dust: 숲속 제단)
  - 두 곡 모두 앞부분이 매우 조용했다(처음 1~2분 단기 음량 -28~-30 LUFS).
  - 조용한 부분을 천천히 끌어올리는 평탄화(dynaudnorm) 뒤 통로 -21.5, 제단 -20.4 LUFS로 맞췄다. 앞부분은 -20~-22 LUFS 정도가 됐다.
  - 다른 곡은 -24 LUFS 그대로다.

## 환경음

모든 장소에 환경음을 넣었다.

| 장소 | 환경음 |
|---|---|
| 입구·광장·우체국·창고·객실·13호실·통로·폐온실·숲속 제단·마차 | 바람 |
| 여관 접수대·식당·주방·학교 | 난로 |
| 2층 복도·수리점·진료실·보호시설 | 시계 |
| "연기가 새는 문", "13호 구조 직후" | 심장박동(음악 없음) |

## 효과음 (새로 연결)

| 언제 | 소리 | 연결한 곳 |
|---|---|---|
| 장소를 옮길 때 | 실내 마루 발소리, 바깥 눈길 발소리, 실내↔바깥 문 열림 | `r13_sound_scene_music` → `r13_sound_move` |
| 13호실 들어갈 때·나올 때 | 문 열림·닫힘 | 같음 |
| 비밀 통로 들어갈 때·나올 때 | 삐걱·걸쇠 | 같음 |
| 새 날 첫 장면 | 종 | 같음 (`room13["day"]`가 바뀌면) |
| 새 자료 기록 | 물건=칼림바, 증언=연필, 세계 기록(W)=미스터리 | `r13_evidence_acquired` 2층(init 150) |
| 장면 속 물건 누름 | 반짝 | `r13_click_feedback` 2층(init 150) |
| 수첩(기록) 열고 닫기, 증거 고르는 수첩 열기 | 책 펼침·덮음 | `r13_records`, `r13_book` 화면 `on "show"/"hide"` |
| 저장 | 저장 차임 | `screens.rpy` `r13_slot_action` |
| 상점 구입 성공·실패 | 피치카토·오류음 | `r13_life_apply_purchase` 2층(init 150) |

- 새 파일: `sfx-note-open`, `sfx-note-close`, `sfx-pencil`, `sfx-save`, `sfx-error`, `sfx-mystery`, `sfx-comic`, `sfx-heartbeat`, `sfx-creak`, `sfx-latch` (.wav, CC0).
- UI 버튼은 소유자 결정대로 리모컨 딸깍 하나만 쓴다(올림·열기·닫기·토글 같은 UI 변형음은 넣지 않음).
- 출처는 `assets/music-v6-credits.txt`와 게임 안 '음악 출처' 화면에 추가했다.

## 검증

- `dev/check.sh`: 단위 106개 통과, lint 문제 없음. `override_map.py --write`로 지도 갱신.
- `dev/run_renpy_tests.sh` 표준 묶음 30개 + `override_chain` + `sound_places` 통과(`SDL_AUDIODRIVER=dummy`).
  - `sound_places`: 장소 18곳 × 분위기 4가지 곡·환경음, 이동 소리 판정(복도→13호=문 열림, 13호→복도=닫힘, 통로=삐걱·걸쇠, 실내↔바깥=문, 바깥끼리=눈길), 모든 효과음 파일을 불러올 수 있음.
- 브라우저(웹판, archive_sha256 `05baa6c9…`): `qa_sound.py`, `qa_carriage.py`, `qa_navigation.py`, `qa_save_slots.py` 통과.
  - `qa_sound.py`: 실제 버튼으로 여관 이동 시 곡·환경음·발소리·13호 문소리, 수첩 열고 닫는 소리, 콘솔 오디오 오류 없음.
- 사람이 직접 들어 보는 확인은 하지 않았다.
