# 0.18.5-dev · 2026-10-14 — 장소별 배경음, 리모컨 버튼 효과음 (소유자 지시)

소유자 요청: 메인 배경음은 몽환적인 피아노로, 장소마다 맞는 배경음을 넣는다. 무료 음원을 최대한 쓴다. 옵션·증거 제출 같은 UI 버튼에는 TV 리모컨 버튼을 누르는 '딸깍' 소리를 넣는다(띡 소리 없이 딸깍만).

## 파일

- `game/systems/room13_sound.rpy` (init -5, 150) 새 파일
  - `R13_PLACE_SOUND`: 장소(배경 이름)별 평온·조사·밤 배경음과 환경음.
  - `R13_SCENE_SOUND`: 이야기 장면 13곳 따로 지정(초소 보호실 만남, 끌고 가는 수레, 연기가 새는 문 등).
  - `r13_sound_scene_music(bg,title,mood)`: `label r13_scene`이 부른다. 배경음 경로를 돌려주고 환경음을 맞춘다.
  - 분위기 규칙: `travel`=이동 곡, `hearing`=회의 곡(환경음 끔), `quiet`=무음(장소 환경음은 유지).
  - `ambience` 채널(효과음 음량을 따름) 추가. 메인 메뉴로 가면 멈춘다.
  - `source_fx` 층 추가: 기존 효과음 키(tap, page, found, impact, knock, door 등)를 새 파일로 바꾼다. 매칭이 없는 키는 예전 파일을 쓴다.
  - `r13_present` 10층(init 150): 증거를 보여 주면 오케스트라 히트.
  - `r13_debate_judge` 2층(init 150): 회의에서 증거를 내밀면 히트 뒤에 반박 성공=맞음, 틀림=틀림 소리. 그 밖(이미 반박됨·동의 없음 등)은 히트만.
  - `style button`의 `activate_sound` = 리모컨 버튼 '딸깍'. 버튼 스타일을 물려받는 모든 버튼에 적용된다.
  - `r13_music_credits` 화면: 옵션 → 소리 → 음악 출처 → 보기. CC BY 4.0 표기.
- `game/room13.rpy`: `r13_scene`의 분위기별 곡 사전을 `r13_sound_scene_music` 호출로 바꿨다(한 줄).
- `game/options.rpy`: 타이틀 곡 `assets/bgm-title.mp3`. 버전 0.18.5-dev.
- `game/room13_options.rpy`: '효과음 듣기'가 새 딸깍 소리를 낸다.
- `game/screens.rpy`: 옵션 소리 탭에 '음악 출처' 줄.
- `game/assets/`: `bgm-*.mp3` 16곡, `amb-*.mp3` 3개, `sfx-*.wav` 15개, `music-v6-credits.txt`.
  - 예전 곡(town-bright.mp3 등)은 예전 장(source·winter)이 아직 쓰므로 남겼다.
- `game/qa_tests/`: `sound_places` 화면 테스트, `r13_qa_sound` 도우미.
- `dev/qa_sound.py`: 웹판 브라우저 소리 검사.

## 장소별 배경음

| 장소 | 평온 | 조사(사건 뒤) | 밤 | 환경음 |
|---|---|---|---|---|
| 눈에 막힌 입구 | First Snow | First Snow | Measured Paces | 바람 |
| 광장 · 우체국 | Childhood | Investigations | Measured Paces | 바람 |
| 수리점 | Heartwarming | Investigations | Comfortable Mystery 4 | 시계 |
| 공동 물품 창고 | Heartwarming | Investigations | Measured Paces | |
| 여관 접수대 · 식당 · 주방 | Midvinter | Comfortable Mystery 4 | Water Lily | 난로 |
| 여관 2층 복도 | Midvinter | Investigations | Measured Paces | |
| 임시 객실 | Water Lily | Comfortable Mystery 4 | Water Lily | |
| 13호실 | Measured Paces | Measured Paces | Measured Paces | |
| 서비스 통로 · 폐온실 · 보호시설 | The Long Dark | | | |
| 임시 진료실 | Comfortable Mystery 4 | | | |
| 마을 학교 | Water Lily | | | |
| 숲속 제단 | Shadows and Dust | | | |
| 마차 안 · 이동 | Snowfall | | | |
| 타이틀 | Sleep (Piano Only) | | | |
| 원탁 회의 · 청문 | Iron Horse | | | |
| 가족 장면 / 엔딩 | The Long Way Home / Home Was You | | | |
| 압박(끌고 가는 수레) | Sanctuary | | | |

## 라이선스

- 배경음: Scott Buckley 10곡, Kevin MacLeod 6곡. CC BY 4.0. 게임 안 '음악 출처' 화면과 `assets/music-v6-credits.txt`에 표기.
- 효과음: Kenney, OpenGameArt의 CC0 소리. 딸깍은 OpenGameArt "Middle Mouse Click"(1j01, CC0)을 둔하게 다듬은 것.
- 배경음은 원본에서 앞뒤 무음을 자르고 -24 LUFS로 일정하게 맞췄다(곡 내용 변경 없음).

## 검증

- `dev/check.sh`: 단위 101개 통과, lint 문제 없음. `override_map.py --write`로 지도 갱신.
- `dev/run_renpy_tests.sh` 표준 묶음 26개 + `override_chain` + `sound_places` 통과(`SDL_AUDIODRIVER=dummy`).
  - `sound_places`: 장소 18곳 × 분위기 4가지의 실제 재생 곡·환경음 확인, 효과음·곡 파일 모두 불러올 수 있음, 회의 판정 뒤 히트→판정 소리 순서.
- 브라우저(웹판, archive_sha256 `463e6747…`): `qa_sound.py`, `qa_carriage.py` 통과. `qa_navigation.py`, `qa_save_slots.py`는 음악 출처 화면을 넣기 전 빌드에서 통과.
  - `qa_sound.py`: 타이틀 곡 설정, 마차=Snowfall, 입구=First Snow+바람, 실제 버튼으로 여관 이동(복도=Midvinter, 13호실=Measured Paces, 접수대=Midvinter+난로), 음원 요청 200, 콘솔 오디오 오류 없음, 음악 출처 화면 열고 닫기.
- 사람이 직접 들어 보는 확인은 하지 않았다. 곡 반복 이음새는 곡 전체 반복이다.
