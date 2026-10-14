# 다람탐정 무료 효과음 비교 패키지

2026-10-14 · 무료 CC0 후보 20개 + 기존 프로젝트 합성안 19종

## 먼저 볼 것

`preview/index.html`을 열어 A(무료 후보)와 B(합성안)를 직접 비교한다. 자동재생은 없고 한 번에 하나만 재생된다. 볼륨은 55%에서 시작한다. 모바일 폭에 맞춘 레이아웃을 포함하며 카테고리 필터, 전체 정지, 청음 선택 기록/내려받기가 있다. 페이지와 상위 폴더 구조를 함께 유지해야 한다. `preview/cc0_20_audition_reel.wav`에서는 무료 후보 20개를 카드 번호 순서로 이어 들을 수 있다. 번호별 시간은 같은 폴더의 JSON에 기록했다.

이 패키지는 게임에 바로 적용된 결과가 아니다. 제작자 설명, 라이선스, 파일 해시, 디지털 신호를 확인했다. 현재 비언어 효과음을 직접 듣는 도구가 없어 실제 청음은 수행하지 못했다. 재생/디코딩 검증은 청음으로 기록하지 않는다. 파일별 용도는 제작자 명명·설명과 길이에 근거한 잠정 제안이다.

## 추천 검토 순서

1. 종이/수첩: Luckius의 종이 2개와 합성 `notebook_open/page`를 비교한다.
2. 문/걸쇠: Cough-E의 잠금·해제·손잡이 흔들기·일반 문을 비교한다. 강제 파손에는 일반 문 음을 쓰지 않는다.
3. 레버: Brian MacIntosh의 기계음 3개와 합성 상태별 음을 비교한다. 길이가 긴 후보는 화면과 맞는지 확인한다.
4. UI/증거: Kenney의 확인·취소·선택·pluck을 비교한다. 증거 제시가 정답으로 느껴지는 후보는 제외한다.
5. 목재/발걸음: 발걸음 2개와 목재 충격 3개는 장면에 필요한 경우만 선택한다.

타이핑, 긴장 상승/해제, 추론 성공, 모순 신호는 원래 합성 후보로 검토한다. 새 분위기 루프를 무리하게 추가하지 않았다. 기존 BGM과 맞춰 듣는 작업이 먼저다.

## 출처와 사용 조건

무료 후보 20개는 모두 제작자 공개 페이지에 CC0 1.0이 명시된 파일이다. 상업용 사용·수정·배포가 가능하며 크레딧은 의무가 아니다. CC0도 저작권 상태/품질을 보증하거나 상표·제3자 권리를 자동 해결하는 것은 아니다. 업로더 설명과 명명에 기반한 출처 검증이며 원 제작의 녹음 과정을 독립적으로 증명한 것은 아니다.

- Kenney: [Interface Sounds](https://kenney.nl/assets/interface-sounds), [UI Audio](https://kenney.nl/assets/ui-audio), [Impact Sounds](https://kenney.nl/assets/impact-sounds). 원 배포 ZIP과 License.txt를 보존했다.
- Luckius: [Various Paper Sound Effects](https://opengameart.org/content/various-paper-sound-effects). 업로더가 지도 열기/닫기용으로 만든 자료이며 페이지에 CC0와 선택적 크레딧이 명시되어 있다.
- Brian MacIntosh (BMacZero): [Mechanical Sounds](https://opengameart.org/content/mechanical-sounds). 페이지에 CC0와 선택적 크레딧이 명시되어 있다.
- Cough-E: [Door Lock Sounds](https://opengameart.org/content/door-lock-sounds). 페이지에 CC0와 상업용/무크레딧 사용이 명시되어 있다.
- [CC0 설명](https://creativecommons.org/publicdomain/zero/1.0/) / [CC0 전체 법률문](https://creativecommons.org/publicdomain/zero/1.0/legalcode.en).

OpenGameArt 전체가 CC0라는 뜻이 아니다. 이번에 선택한 개별 작품의 조건이다. Freesound·Sonniss 자료는 포함하지 않았다. 별도 계정, 결제, 개인정보 전송 없이 받았다.

합성 19종은 앞서 이 프로젝트용으로 만든 원본이다. 외부 샘플이 없으며 무료 CC0 다운로드 파일과 권리 출처를 구별한다. 합성 원본을 임의로 CC0로 재지정하지 않았다.

## 처리 내용

- `selected/originals/`: 선택한 20개 원본. 원본 바이트와 SHA-256 그대로 보존.
- `selected/game_wav/`: 44.1 kHz / 모노 / PCM16 WAV 비교·적용 후보.
- 부동소수점으로 먼저 디코딩한 뒤 감쇠하고 PCM16으로 변환한다. 일부 원본은 디코딩 피크가 0 dBFS를 넘으므로 무감쇠 정수 변환을 피한다.
- 끝단에 2ms 페이드, 이벤트에 맞춘 최대 피크 감쇠만 적용한다. 증폭·잘라 붙이기·피치 변경·무음 트리밍은 하지 않았다.
- 수치 검사에서 변환본 20개 모두 클리핑 샘플 0, 목표 피크 이하. 원본에 이미 있는 왜곡은 감쇠로 복구되지 않는다.
- 같은 피크가 같은 체감 음량은 아니다. 파일마다 BGM 속 식별과 반복 피로도를 실제로 들어야 한다.

## 파일 안내

- `manifest.json`: 20개 원본/가공본의 경로·길이·피크·해시·처리·출처와 합성 19종 목록
- `event_mapping.json`, `event_mapping.csv`: 논리 이벤트별 잠정 후보와 기존 계약
- `CLAUDE_HANDOFF_KO.md`: 런타임 적용 담당자에게 넘길 기준
- `comparison/original_synth/`: 합성 19종 WAV 원본
- `comparison/AUTHORING_RULES.md`: 대사·증거·독백·타이핑 연출 규칙
- `licenses/`: 원 배포 라이선스와 작품별 출처 기록
- `CREDITS_KO.txt`: 채택한 후보에 맞게 줄여 사용할 수 있는 출처 목록
- `qa/`: 디지털 검사 및 페이지 정적/브라우저 검증 결과
- `provenance/`: 다운로드 URL, 원 배포 ZIP 해시, 출처 확인 기록

## 완료 상태

- 완료: 20개 선정/파일 확보, CC0 출처 확인, 원본 보존, 감쇠 WAV, 신호 검사, 19종 합성 비교 페이지, Claude 이벤트 매핑
- 미실시: 실제 청음, 주관적 품질 평가, 게임 런타임 연결, 장면 회귀 테스트, 배포본 확인

게임 코드·대사·판정·원격 저장소·배포는 변경하지 않았다.
