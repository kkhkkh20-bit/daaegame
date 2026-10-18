# 회의 단계별 템포 + 투명 가로선 검토 후보

C2만 적용하는 작은 후보. main 배포 없음. 노란 채움/불투명 카드는 사용자 거절로 제거했고, 원래 회의 장면 위 양옆에 회백색 최대 12% 불투명도 가로선 6개만 약 0.15초 지나간다. 중앙 얼굴·대사창을 피한다. 같은 화자 연속 대사, 동작 끄기, 스킵, 롤백에는 반복하지 않는다. 원작과 같은 구현이 아닌 사용자 요청에 따른 독자 후보다. 저프레임 원인 해결을 뜻하지 않는다.

사운드 최신 지시는 1초 이내 성우식 ‘잠깐만요!’ 외침이다. 특정 성우/원작 음성 복제 없음. 부모가 실제 음성 제작 경로를 확인 중이므로 이번에는 기존 `sfx-present.wav`가 남는다. 거절된 군중 A/B와 금관 A/B는 포함하지 않았다.

## 확인한 소스와 지원

기존 저장소 `game/assets/music-v6-credits.txt`에서 일반 회의곡은 **Iron Horse / Kevin MacLeod**, 반문은 **Sanctuary / Scott Buckley**, 제단은 **Shadows and Dust / Scott Buckley**, CC BY 4.0으로 기록돼 있다. 후보는 앞의 두 곡만 변형한다.

- Iron Horse 원본 페이지: https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1100735 . 현재 동적 카탈로그 상세는 텍스트 도구에서 확인되지 않아 곡 식별은 기존 저장소 기록을 사용했다. 공식 https://incompetech.com/music/royalty-free/licenses/ 에서 출처 표기 조건의 무료 CC 경로를 확인했다.
- Sanctuary 작곡가 페이지 https://www.scottbuckley.com.au/library/sanctuary/ 에서 CC BY 4.0 및 표기 조건 확인.
- https://creativecommons.org/licenses/by/4.0/ 는 변형을 허용하고 출처/라이선스/수정 사실 표기를 요구한다. 기존 출처를 보존하고 `music-v6-credits.txt`에 파생 과정과 변경을 추가했다. 작곡가의 보증을 뜻하지 않는다.

로컬 SDK 8.5.3의 `renpy/audio/music.py` play/queue/get_pos와 `doc/audio_filters.html`를 확인했다. 내장 pitch-preserving tempo 지원을 확인하지 못해 재생 샘플레이트를 바꾸지 않는다. 설치된 FFmpeg Rubber Band의 독립 tempo/pitch 옵션으로 오프라인 변형했다: `rubberband=tempo=1.06:pitch=1` / `tempo=1.12:pitch=1`, Vorbis q4. 원본은 기존 정규화 MP3다. 파생본 출처 해시·실제 재생 길이는 `game/assets/meeting-tempo-derivatives.json`에 기록했다.

## 적용 규칙

| 회의 진행 단계 | 속도 비율 | 조건 |
|---|---|---|
| 0 | 1.00 | C2 공개 반박 이력 없음 |
| 1 | 1.06 | 첫 고유 진술의 공개 반박 성립 |
| 2 | 1.12 | 두 번째 이후 고유 진술의 공개 반박 성립; 상한 |

비율은 BPM 측정값이 아니다. 독립 rollback-aware `r13_meeting_tempo_milestones`가 `(run, claim, statement)`를 기억한다. 반복 증거·틀린 자료·매 대사로 누적하지 않는다. 개인 압박 2→1 회복과 별개로 회의 stage는 2를 유지한다. 다른 run/claim에는 적용하지 않는다.

집단 반응의 정적이 끝난 뒤 단계 곡으로 바꾼다. 같은 곡이면 `현재 재생초 × 이전 비율 ÷ 새 비율`의 대응 위치부터 재생하고 이후에는 곡 처음부터 루프한다. 동일 파일 반복 호출은 재시작하지 않는다. get_pos가 None인 mute 상황은 처음부터 재생하는 안전한 경로를 사용한다. council→pressure의 기존 선곡 전환은 보존하고 해당 stage 버전을 쓴다.

중요한 기존 구조: 자료 제시는 `call_in_new_context`로 진행하며 끝나면 부모 문맥의 옛 오디오가 복원된다. 새 연결은 자식 문맥의 파일/위치/채널 gain/pause만 넘겨 같은 지점부터 이어 재생한다. 판정/스토리/증거를 변경하지 않는다. 사용자 mixer volume/mute 값은 쓰지 않는다.

단일 music 채널에 0.12초 fade-out / 0.20초 fade-in, 문맥 복귀에는 0.08/0.12초를 사용한다. **실제 두 채널 크로스페이드나 마디 경계 정렬은 아니다.** 박자/마디 그리드를 확인하지 않아 정렬을 주장하지 않는다. 초기 preload는 파생 OGG 4개로 약 8MB 증가한다. 채택 시 리소스 전달 최적화는 별도다.

## 검수와 한계

이전 비교 영상: `../meeting-speed-card-review/after.mp4`(거절된 노란 카드가 있던 이전 상태). 최신 영상은 투명선과 단계 템포를 함께 검토한다. 모두 C2 day10/E35/E09/C1 초기 fixture 이후 실제 UI 입력, WebAudio+canvas 동시 녹화이며 후합성 오디오가 아니다.

단위 검사는 중복/상한/run 분리, 개인 압박과 독립, 정적 중 변경 연기, 반복 재시작 방지, mute 위치 None, 로드 경로 유지와 rollback 이력 감소를 포함한다. 실제 브라우저는 저장/불러오기·Ctrl 스킵·mute action·무음 복귀를 좁게 확인한다. 전체 캠페인 QA가 아니다.

궁지·붕괴 그림은 기존 별도 진단 전용 상태다. 사람의 청감 평가, 실제 모바일 성능, 측정 BPM/마디 정렬, 새 외침 음성은 미완료다. Rubber Band pitch=1은 음정 보존 변형 방식이며 사람의 음질 승인을 대신하지 않는다. 기존 낮은 렌더 빈도의 CPU/GPU/디코딩 원인은 아직 분리 진단하지 않았다.

투명선 최종 제안값: 20ms 등장 / 40ms 유지 / 90ms 소멸, 720p 두께 1px, 길이 128~190px, 상하 빈공간의 고정 위치. 이동방향으로 1회, 랜덤/깜빡임/색면 없음. 공식 영상에서 관찰된 것은 배경 이동 약 0.3초/중간 흐림 약 0.2초이며 독립 가로선이 아니었다는 부모 분석을 반영했다. 우리 수치는 원작 측정치로 소개하지 않는다.

검사 결과: 전체 단위 검사와 Ren’Py lint 통과(`check.log`); 최종 선 파라미터 변경 뒤 카메라 테스트 5개 재통과. 실제 저장/로드·스킵·음악 mute·무음→복귀 검사 모두 통과(`state-report.json`). 개인 압박은 1로 회복, 회의 stage는 2 유지, 사용자 volume/mute 원복 확인. 초기 QA probe에서 외부 Python의 `renpy.music` 접근이 잘못돼 실패한 것은 `store.renpy.music`으로 수정한 검사 코드 문제이며 게임 오류가 아니었다.

최신 유음 결과: `after.mp4` 56.571초, H.264/AAC 48kHz, 평균 -40.1dB / 최대 -18.1dB. `tempo-events.json`에서 stage 0/1/2와 각 실제 재생 파일을 확인했으며 증거 문맥 복귀 뒤 stage1 곡이 원속도 파일로 돌아가지 않았다. 최종 압박 1, 회의 stage 2, 깨진 진술 s2만, music/ambience gain=1. `04-transparent-lines.png`는 실제 영상에서 추출한 희미한 선 프레임이다. 새 외침은 미적용이다.
