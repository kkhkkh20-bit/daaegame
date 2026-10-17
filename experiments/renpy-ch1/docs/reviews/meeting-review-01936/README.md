# 요청된 회의 화면 — 실제 실행 캡처

합성/목업이 아닌 정식 SDK 빌드의 Chromium/WASM 화면 4장이다. 기준 커밋 `57472ad4fe4e3b83fae41a936a3b2eb9b073dc35` (배포 성공 0.19.35), 캡처 빌드는 배치 수정 작업 중인 0.19.36이다. 회의 원화/로직/UI 소스는 기준 커밋과 동일하다. 캡처용으로 게임 파일을 수정하지 않았다.

검수 상태로 day7 저녁과 증거 보유를 설정한 뒤 실제 `r13_trial`에 진입했다. 런타임 실제 날짜는 **7일 저녁**이다. 화면 상단의 ‘식당 회의 · 10일째’는 회의 chrome의 정해진 표시라 fixture의 날짜와 다르다. 이 차이도 현 상태 그대로 캡처했다. 자연 전체 진행 캡처로 표현하지 않는다. 증거는 검수 fixture에서 전체 보유하여 목록 개수가 실제 플레이와 다를 수 있다.

1. `01-whole-meeting-agenda.png`: 식당 회의 전체 배치와 안건 선택.
2. `02-focused-speaker.png`: C2 발언자 확대, 실제 대사·도구.
3. `03-statement-selection.png`: C2 발언 고르기 화면.
4. `04-evidence-presentation.png`: C2 발언에 보여줄 증거 선택 화면.

`runtime.json`에 각 캡처의 실제 날짜/시간/회의 ID/발언자/대사를 기록했다. Library는 기존 연결 실패 상태여서 재시도하지 않았고 반환 ID가 없다. 이 저장소의 검수 브랜치 파일이 공유 원본이다.

## 읽기 전용 후속 확인 (2026-10-17)

- 실제 회의일은 `systems/room13_timeline.rpy`의 `R13_TRIAL_DAY=10`이며 본편 진입 조건과 회의 머리말이 같은 상수를 쓴다. fixture day7/머리말10의 차이는 이야기 날짜 오류가 아니다. 날짜를 바꾸지 않았다.
- 04번 화면 가장자리는 돌담·목조 천장·식탁/의자가 있는 **일반 식당 조사 배경**이다. 광장으로 전환한 흔적은 없다. `r13_trial`은 `r13_scene("council",...)`을 실행하며 council은 dining의 월드 배경에 연결된다. 확대 회의 배경은 `say`/회의 화면이 그리므로 증거 `r13_book`이 열릴 때 그 화면이 사라지고 밑의 일반 식당이 보인다. 즉 fixture 광장 잔상은 아니며, 회의 전용 배경을 모달 뒤에도 유지할지는 별도 연출 개선 항목이다. 이번에는 변경하지 않았다.
- 전체 회의의 도토는 `room13-meeting-seated.json`에 전용 좌석 그림이 없다. `r13_meeting_actor(...,seated=True)`가 CAST의 `assets/room13-role-doto.webp`로 fallback하고 `nearest=True`로 표시한다. 별도 구형 좌석 이미지가 선택된 것이 아니라 기본 픽셀 인물 fallback이다. 확대 발언자는 별도의 정본 대화 원화를 쓴다.
- 155개 자료는 fixture의 `evidence=list(ROOM13["evidence"])` 전체 지급 결과다. 일반 플레이 대표 수량이 아니다.
