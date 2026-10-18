# C2 회의 후보 동결 및 제작 인계

후속 상태: [속도선 후보 검수](../meeting-speed-card-review/README.md). 아래는 제작 전 인계 기록이다. 이후 궁지/붕괴를 수령해 진단용으로 등록했으며 군중 A/B는 사용자 거절로 제외했다. 소리 목표는 최신 지시의 금관 ‘빠밤!’으로 변경됐다.

기준: 후보 `5921fa0c`, 자연 진행 기록 `6cf67eb6`. 이 문서는 제작 요청이며 새 그림·음원·연출 연결의 완료 보고가 아니다. 후보 코드/빌드/영상은 동결한다. main에 후보를 머지하거나 배포하지 않았다.

## 추가 그림 2장: 뿔이 `resident_ppul`

현재 C2의 s1/s2/s3 발언자가 모두 뿔이이므로 이번 제작 대상은 이 ID 하나다. 다른 회의 인물의 궁지/붕괴 전용 그림까지 제작 완료 또는 필요 확정으로 확대하지 않는다.

경로는 별도 표시가 없으면 `experiments/renpy-ch1/` 기준이다.

| 용도 | 승인 자료 및 현행 경로 |
|---|---|
| 확정 디자인 원본 | `art/canonical48-rev45/originals/resident_ppul.webp` — RGBA 1010×1499 |
| 최신 대화 승인 원화 | `/workspace/smooth-next20-approved/extracted/sources/ppul/{neutral,joy,angry,anxious,surprise_talk,surprise_react}.png` — 이 작업 환경에 실재하나 저장소 상대 경로가 아닌 제작 작업 원본 |
| 지속 가능한 저장소 내 표정 참조 | `game/assets/dialogue-source-master/resident_ppul/{560,760,840}/{neutral,joy,angry,anxious,surprise_talk,surprise_react}.webp` |
| 승인·배치 기준 | `game/assets/room13-dialogue-talk-art.json`의 `people.resident_ppul`, `source_commit=f25caf86ded3a8d874c938e353d14c268b23b8e2`, `approved_runtime`, standing/player |
| 기존 단호한 발언 자세 | `game/assets/meeting-source-master/resident_ppul--stern_statement.webp`; 등록은 `room13-meeting-source-art.json`, canvas 611×906, offset (8,33), scale 1.05 |
| 프로필 | `game/assets/profile-source-master/resident_ppul.webp`; `room13-profile-source-art.json` |

대화 neutral 원화는 1029×1528 RGBA, SHA256 `a10889d8460429662b4e32c97d3b90b2b263c3364674144a96f6a3b916e016c8`. 다른 원화도 동일 크기이며 surprise_talk만 1030×1527이다. 위 로컬 원화가 전달되지 않으면 저장소 840 표정 파일을 참조하고 원화를 별도로 전달받아야 한다. 옛 pixel/retro 그림을 대체 참조로 쓰지 않는다.

### 제작 규격

- 새 파일 이름 제안: `resident_ppul--cornered.png`, `resident_ppul--collapse.png`. **아직 파일 없음, 런타임 키도 미등록.**
- neutral 원화에 맞춘 1029×1528 RGBA PNG, 투명 배경. 전신과 뿔/귀/신발/지팡이 끝을 자르지 않는다. 배경·테이블·바닥 그림자는 합성하지 않는다. 전신 중심·발 기준선·크기는 neutral과 맞춘다.
- 정면 서기, 시선은 플레이어. 크림색 털, 갈색 말린 뿔, 둥근 금색 안경, 금색 테두리 남색 긴 코트, 버건디 조끼·금색 단추/체인, 흰 칼라, 갈색 바지/신발, 금색 장식 지팡이를 그대로 보존한다. 기존 겨울 복장을 유지하며 모자·목도리 등 새 소품을 더하지 않는다.
- 궁지: 불안보다 분명한 눈썹/눈/어깨 긴장, 지팡이를 움켜쥐는 손. 붕괴: 주장에 대한 자신감이 꺾인 어깨·손과 표정. 범인 자백·기절·무릎 꿇기·새 의상으로 해석하지 않는다. 얼굴 식별과 정면 시선을 유지한다. 입 애니메이션은 요청 범위가 아니다.
- 납품 후 승인받아 기존 변환 절차로 WebP를 만든다. 프로필명 560/760/840은 원화 픽셀 높이가 아니다. 실제 합성 canvas는 각각 413×612 / 416×617 / 611×906. 현행 840 파일은 대개 594×882(놀람 대화 595×882), offset은 표정별로 다르다. 새 그림의 알파 경계를 측정해 배치하며 기존 offset을 무조건 복사하거나 그림을 늘이지 않는다.

### 사용할 사건과 미구현 경계

현재 후보는 `room13_meeting_pressure.rpy`에서 C2에만 0=중립, 1=anxious, 2=surprise(대화에서는 surprise_talk)를 사용한다. flustered는 anxious와 동일 원화이므로 별도 단계가 아니다. 승인된 angry 등 명시 표정은 해당 대사에서 보존한다.

| 실제 사건 | 현행 | 새 그림 연결 제안 — 승인 후 별도 구현 |
|---|---|---|
| C2 s1 E06 또는 E08, s2 E35, s3 E09 또는 동의가 있는 E10으로 공개 반박 성립 | 서로 다른 statement당 1회 상승, 최대 2; 같은 증거/statement 반복은 상승 없음 | 두 번째 고유 반박 이후 지속 상태에 궁지 사용 제안. 현재는 surprise를 사용하므로 자동 교체된 것이 아님 |
| C2 s3 반문에서 플레이어가 over/weak 답변 → 뿔이 반문 성립 | 압박 1단계 회복, 해당 대사 angry 보존 | 새 궁지 상태도 기존 회복 규칙을 따라 내려가야 함. 실패한 플레이어 답변에 붕괴를 표시하지 않음 |
| `r13_debate_conclude`에서 C2 correct 결론 선택, `debate:conclusion:C2` 시작 | 기존 결론 대사/판정 유지 | 붕괴는 이 공개 결론 시점의 뿔이 듣는 자세로 제안. 뜻은 **뿔이의 주장 붕괴**이며 범인 확정이 아님. 현재 연결 없음 |

C2에 완전 역전으로 압박을 모두 초기화하는 별도 서사 사건은 추가하지 않았다. 그림 제작만으로 단계/판정/분기를 늘리지 않는다. 저장·불러오기·롤백은 승인 뒤 연결할 때 기존 상태 복원 규칙을 유지해야 한다.

## 군중 소리 제작 요청

저장소 음원 파일 목록, `game/assets/*credits*`, `systems/room13_sound.rpy`를 대조했다. **군중 웅성거림/집단 숨 들이킴으로 식별되고 라이선스가 기록된 재사용 음원은 찾지 못했다.** 파일명을 넘어 모든 음원을 청취 감정한 결과는 아니다. 기존 gasp/murmur 대사는 음성 녹음이 아니다.

현재 후보의 실제 소리는 기존 `sfx-present.wav`(Kenney Music Jingles HIT00, CC0), BGM/환경음 감쇠와 복원이다. 출처는 `music-v6-credits.txt`; council/pressure 음악은 각각 Kevin MacLeod의 Iron Horse와 Scott Buckley의 Sanctuary(CC BY 4.0). 별도 군중 녹음이 추가됐다고 표시하지 않는다.

요청 납품:

- `council-gasp`: 0.5초 내외(0.4–0.65초), 한 번 재생. 실내 주민 여러 명이 동시에 짧게 숨을 들이키는 반응. 현행 집단 반응 약 0.52초에 맞출 후보.
- `council-murmur`: 4초, 앞뒤가 자연스럽게 연결되는 반복 가능 파일. 낮은 웅성거림, 알아들을 수 있는 단어·이름·범인 암시 없음. 실제 사용은 공개 반박 직후 1.5–2.5초 및 0.15초 fade를 제안하며, 사용자 승인 전 타이밍/루프 연결을 구현하지 않는다.
- 원본 WAV PCM 48kHz/24bit stereo, 음악·충격음 혼합 없이 별도 stem, clipping 없음. 웹용 OGG와 필요 시 MP3 파생본. 시작/끝 무음 길이와 권장 gain을 기재하고 최종 볼륨은 기존 대사/BGM과 비교한다.
- 직접 제작/녹음 또는 재배포 가능한 CC0/CC BY 자료. 제작자·원본 URL·라이선스 전문/버전·수정 내역·표기 문구를 함께 납품한다. 기존 게임 음원 추출본은 사용하지 않는다. 이번 문서 작성에서 외부 음원을 구매·다운로드하지 않았다.

## PageUp / 휠 롤백 읽기 전용 진단

확인 사실:

- `game/options.rpy:65`는 `config.rollback_enabled = True`. 저장소 RPY에 `block_rollback`, `fix_rollback`, rollback keymap 재정의가 없다. SDK 기본 입력에는 PageUp과 마우스 휠 위가 포함된다.
- 실제 후보 QA에서 PageUp 18회/휠 24회로 사건 경계를 넘지 못했다. `renpy.exports.can_rollback()`은 True였다.
- QA용 임시 UI에서 엔진의 `Rollback(checkpoints=2)`를 실제 클릭하자 증거 제시 이전으로 돌아가 pressure=0, events=[], collective=None, 중립, 음악/환경음 gain=1을 복원했다. E35 재제시는 상승을 1회만 적용했다. 기록: `state-report.json` 및 `05-engine-rollback-before-proof.png`, `06-rollback-replay-consistent.png`.
- main `d10cabfe`와 후보 `5921fa0c`를 비교하면 options 설정은 동일하다. `r13_lines`의 수동 `renpy.checkpoint()`는 main에도 이미 존재한다. 후보의 이 함수 변경은 집단 반응 호출 2줄이다. Character 발화의 체크포인트와 수동 체크포인트가 함께 기록된다.

판정: **의도된 롤백 차단이라는 근거는 없다. 새 후보 회귀라고 확정할 근거도 없다.** 기존 중복 체크포인트 때문에 한 단계 입력이 같은 대사에 머무는 가능성이 있으나, 동일 저장/입력으로 main과 후보를 A/B 재현하지 않았으므로 원인은 미확정이다. 집단 반응 호출의 체크포인트 영향도 배제하지 않는다. 상태 복원 성공과 기본 입력 UX 성공을 구분한다. 후보 코드는 고치지 않았다. 후속 승인 시 같은 저장의 main/후보 기본 입력 비교가 우선이다.

## 자연 진행 QA 인계

새 게임부터 3일 밤을 지나 4일 아침까지 **선택한 경로**를 실제 입력으로 완료. 1쪽5번 저장, 이전 1~4번 보존. 진행 차단 없음. 사서에게 L04→L00 제시해 warned/safe 및 장작 지원 없는 ill 분기를 확인했다. 근거는 `../natural-days-1-3-20261018/`의 README, 입력/대화 기록, 33~35번 캡처.

남은 관찰: 일반 여관 토리 앉기 자세의 발/의자 접점. 협동 토리 간격 수정과 다른 포즈다. 구 UI 입구의 발 가림은 main에서 버튼 제거를 확인했지만 같은 1일 저장으로 최종 UI 재검증은 하지 않았다.

미검증: 피코 생존/예방, 나비 장작 지원 및 사서 완전 구조, 그 외 모든 선택지, 전체 캠페인, 실제 iPhone, 기본 롤백 입력 UX. 자연 진행은 main 0.19.52 브라우저이며 C2 후보와 별도다. 승인 대기 중에는 새 전체 QA나 후보 시스템 확장을 시작하지 않는다.
