# 다람탐정 효과음과 대사 표현 자산 감사

2026-10-14 · 기준 0.16.2 · 커밋 5e6c2c53ae067b7fc2eb9d10075320587a342f0e

## 결론

증거 획득음과 제시음은 이미 연결되어 있다. 새 자산을 추가하는 것보다 먼저 현재 작은 소리를 알아듣기 쉽게 다듬고, 획득·제시·추론 성공·모순 확인을 구별하는 것이 중요하다. 타이핑은 25ms짜리 첫 탭을 반복하는 현재 방식에서, 또렷하지만 짧은 38ms 변형 3종과 줄 단위 배경음 저감을 비교하도록 준비했다. 독백은 현재 글자색만 파랑이므로 파란 창 자체와 ‘속마음’ 라벨이 필요하다.

이번 산출물은 외부 음원 샘플 없는 새 효과음 19종, 논리 이벤트 17개, 지속 작성 규칙과 구현 연결표다. 게임 코드·대사·배포에는 적용하지 않았다.

## 조사 범위와 증거 수준

- [기준 커밋](https://github.com/kkhkkh20-bit/daaegame/commit/5e6c2c53ae067b7fc2eb9d10075320587a342f0e)의 [소스 인계 ZIP](https://github.com/kkhkkh20-bit/daaegame/blob/5e6c2c53ae067b7fc2eb9d10075320587a342f0e/preview/room13-source/ROOM13_SOURCE_HANDOFF.zip)을 읽었다. 이하 코드 위치는 ZIP 안 `experiments/renpy-ch1/` 기준이다.
- Git 트리를 전체 조회했으며 잘림 없음. 독립 음원은 49개(43 MP3, 3 WAV, 3 OGG)였다. 다수가 과거 시안·보관용이다. `reference/repository_audio_inventory.json`에 경로와 Git blob SHA를 보존했다.
- 현행 빌드의 `game/assets/provenance.json`에는 오디오 40개(14 BGM, 26 SFX/타이핑/심박)가 있다. 이는 저장소의 독립 파일 목록과 다른 범위다. 생성 파일과 패키지 안 파일도 포함하기 때문이다. `existing_runtime_audio.json`에 모두 기록했다.
- 기존 합성 레시피를 새 검토 폴더로만 다시 렌더링했다. 공개된 해시가 있는 23개는 모두 일치했다. `type.wav`는 현행 provenance에 비교할 해시가 없어 레시피 재현으로만 분류했다.
- 마을 BGM 1개와 기존 문 닫힘 WAV 1개는 실제 파일을 받았다. 마을 BGM의 Git SHA와 SHA-256이 기준 트리·provenance와 일치했다. 전체 배포 게임 압축파일은 추출하지 않았다.
- 신호 검사와 A/B용 오디오 파일을 만들었지만 사람이 실제로 듣거나 게임 브라우저의 소리를 청취한 검증은 하지 않았다.

## 기존 자산과 누락 자산

| 영역 | 현재 상태와 근거 | 제안 자산·조치 | 우선순위 |
|---|---|---|---|
| 새 증거/증언 | `r13_grant`, room13_rules.rpy:100-118에서 found 재생 + 카드. source-found 300ms, 피크 -23.26dBFS | evidence_acquire. 기존 호출 개선이며 두 번째 호출을 추가하지 않음 | P0 |
| 자료 제시 | room13_screens.rpy:265-269에서 카드 show 시 page 재생 | evidence_present. 획득과 다른 종이 질감, 제시 확정 뒤 한 번 | P0 |
| 타이핑 | room13_dialogue_rhythm.rpy:77-91, type.wav 첫 25ms. 원본 288ms는 4음이지만 실제로 첫 음만 사용 | typed_blip 38ms × 3변형, 최소 70ms 간격, BGM -6dB 비교 | P0 |
| 선택 확정/취소 | source-select/tap은 존재. 공통 room13 선택지에 확인/취소가 일관되게 연결된 중앙 규칙은 확인 못함 | choice_confirm, choice_cancel. hover 무음, 의미 이벤트 발생 시 confirm 생략 | P1 |
| 추론 성공 | 원고·증거 피드백은 있으나 독립적인 공통 성공 이벤트는 확인 못함 | deduction_success. 검증 결과 공개 때만 | P1 |
| 모순 확인 | 과거 shock/cut/low 등의 효과음 존재. room13에서 의미별 공통 모순음 연결은 확인 못함 | contradiction. 오답·거절과 구별 | P1 |
| 긴장 전환 | legacy pulse/심박·충격 레시피 존재, 현재 장면 BGM quiet/night 등 사용 | suspense_rise/release 2종. 갑작스러운 강타 없이 장면 경계에서만 | P1 |
| 주방 레버 on/off | room13_revision.rpy:34/38 모두 tap | mechanism_lever_on/off 2종 | P1 |
| 책장 해제 | room13_revision.rpy:54에서 일반 door(닫힘 음원 경로) 사용 | book_latch_unlock. 금속 걸쇠+나무 판 | P1 |
| 잠긴 책장 | room13_revision.rpy:66-67, 별도 음향 없음 | book_latch_locked. 실제 저항 신호 | P1 |
| 통로 안쪽 출구 | room13_revision.rpy:16-24, 별도 음향 없음 | passage_exit_release. 내부 수동 해제 구별 | P1 |
| 구조 중 강제 개방 | room13.rpy:480에서 impact 뒤 즉시 장면 전환 | door_forced_open. 화면 동기화 및 전환 시 끊김 확인 | P1 |
| 수첩 열기/넘김 | legacy page 존재, 독립된 새 기록/단순 열람 구별 필요 | notebook_open/page 2종 | P2 |
| 일반 방문 | 녹음 기반 wood-door-open/close 있음. CC BY 3.0 크레딧 | 유지 가능. 메커니즘/강제 개방과 재사용하지 않음 | 기존 유지 |
| 문 두드림 | source-knock, room13.rpy:450/478 연결 | 이번 변경 제외. 새 팩과 레벨만 실제 청음 비교 | 기존 유지 |
| 발걸음/종/잠금/충격 | source-steps/bell10/lock/slam/impact/shock9/cut9/low9/pop9 등 레시피 존재 | 목적별 사용 여부를 확인하고 무조건 새 장면에 재사용하지 않음 | 보관·선별 |
| 마차·말발굽 | 녹음 파일은 저장소에 있으나 source.rpy:72-73에서 관련 호출 비활성 | 다시 켜지 않음. 사용자 불만족 음원의 자동 복귀 금지 | 사용 제외 |
| 까마귀 울음 | 이번 소스·음원 목록에서 전용 독립 파일 확인 못함 | 새로 넣지 않음. 요구 없는 야생동물음 추가 금지 | 사용 제외 |
| 바람/눈/불/수프 등 생활환경 | 별도 전용 현장음은 이번 목록에서 확인 못함 | P2 후속 장면표 승인 후 필요 장면만 제작/확보. UI팩을 환경음처럼 반복하지 않음 | 미제작 P2 |

## 새 파일의 구성

- `audio/wav/`: 19개 원샷 PCM WAV, mono, 44.1kHz, signed 16bit. 전체 661,808바이트.
- `audio/ogg/`: 같은 19개 Ogg Vorbis 대안. 짧은 탭은 WAV를 우선 시험한다.
- 17개 논리 이벤트가 19개 자산을 사용한다. `typed_blip`만 a/b/c 3변형이다.
- 모든 새 파일에 시작·끝 페이드, 고정 피크, 0인 시작/끝 샘플을 적용했다. 4배 오버샘플 피크·클리핑·DC·해시·OGG 디코딩 검사를 통과했다.
- 신규 파일 피크는 -12~-21dBFS 범위이며 이것은 기기 청취 음압을 뜻하지 않는다. 음량은 기기·사용자 설정·채널 gain과 함께 정한다.
- UI는 부드러운 종이·나무 탭·펠트성 짧은 음을 공통 어휘로 사용한다. 픽셀 그림이라는 이유로 사각파/8bit 사운드를 가정하지 않았다.
- 소리 생성 재현: `python tools/generate_sfx.py`. 결과의 객관 검증: `python tools/build_contract.py`(소스 감사 재생성은 지정된 소스 스냅샷 경로가 있어야 함).

## 타이핑이 묻히는 문제의 재현과 한계

같은 마을 BGM 14~26초, 효과음 설정 0.70, 음악 설정 0.75로 비교 파일 세 개를 만들었다. 기존 재현은 25ms 탭을 초당 34회, 새 버전은 38ms 세 변형을 약 14회/초 사용한다.

| 파일 | 변화 | 1~4kHz 탭 구간의 신호 대 배경음 비율 |
|---|---|---|
| typing_current_reconstruction.wav | 기존 레시피와 잘라 재생하는 방식 재현 | -12.64dB |
| typing_new_same_bgm.wav | 새 음색·길이·간격만 변경 | -1.38dB |
| typing_new_with_duck.wav | 위 변경 + 대사 중 BGM 6dB 낮춤 | +4.64dB |

이는 특정 구간·대역에서 측정한 기술 지표다. 사람의 체감 명료도나 실제 브라우저 재생을 보증하지 않는다. 세 파일 모두 클리핑은 0이다. 게임의 밝은 마을·탐색·밤·심문 음악과 실제 휴대폰/헤드폰에서 적정 레벨을 최종 결정한다. 후보 중 BGM 저감 버전을 먼저 듣되, 음악이 지나치게 작아지는지 같이 확인한다.

## 이벤트 규격 요약

정확한 파일·길이·gain·priority·cooldown·시점은 `sound_events.json`, 정렬 가능한 목록은 `audio_event_inventory.csv`에 있다. 숫자는 시작 제안이다.

- 선택 20, 타이핑 10, 기계장치 50~65, 증거 70~75, 성공/모순 85, 강제 개방 90의 우선순위. 숫자가 높을수록 우선한다.
- 새 획득/성공/모순은 잠깐 음악에 0.40계수, 읽기 중 타이핑은 줄 전체 음악에 0.50계수. 두 요청은 곱하지 않고 더 작은 계수 하나를 쓴다.
- 음악·효과음 사용자 설정을 덮어쓰지 않는다. mute 상태, 스킵, 저장/복원, 기록 재열람은 존중한다.
- 같은 입력의 confirm+present+success를 겹치지 않는다. 배치 획득은 한 번. 실시간 화면 렌더링·예측 호출은 효과음을 발행하지 않는다.
- 성급한 정답음으로 답을 누설하지 않는다. 시스템 결과가 화면에 공개되는 정확한 지점에 연결한다.

## 출처와 배포 점검

새 19개는 동봉 생성 코드로 만든 원본 합성으로, 외부 녹음·곡·목소리·악기 샘플이 없다. 기존 문소리와 말발굽은 새 팩에 섞지 않았다. 별도의 라이선스 구매나 유료 사용도 없다. 권리·해시는 `provenance_license_manifest.json`에 보존했다.

기존 문 열림은 CGEffex/BlockMen, 닫힘은 bennstir의 [Minetest 문 음원](https://github.com/minetest/minetest_game/tree/master/mods/doors)이며 프로젝트 크레딧은 [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)을 명시한다. 기존 말발굽은 Wildfire Games의 0 A.D. 자산과 [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) 조건을 명시하지만 이번 팩에는 넣지 않았다. 기존 마을 음악의 프로젝트 크레딧과 FluidR3_GM MIT 문서를 비교용 묶음에도 포함했다.

`options.rpy:95`에는 모든 `.txt`를 제외하는 분류 규칙이 있다. 현재 크레딧·라이선스도 `.txt`이므로 실제 배포 ZIP에 포함되는지, 웹에서 읽을 수 있는지 확인할 필요가 있다. 소스에 파일이 있다는 사실만으로 배포 크레딧이 완비됐다고 결론내리지 않는다.

## 완료와 남은 일

완료: 소스 감사, 신규 WAV/OGG 19쌍, 원본 생성기, 디지털 QA, 비교 청음 파일, 별도 검토 HTML, 지속 작성 규칙, Claude 연결표.

남음: 사용자의 음색 선택·실제 청음, Claude의 런타임 연결, 읽음/저장/취소/모바일 회귀, 최종 배포 크레딧 확인. 이 단계가 끝나기 전에는 ‘게임에서 잘 들리도록 적용 완료’라고 표현하지 않는다.
