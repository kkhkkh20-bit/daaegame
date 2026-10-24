# PR29 후속 UI 실행 검수 (2026-10-24)

기준 main `83102b0993c77ceaea131b4fdf3f95a27bd21a2d`, PR29 `1d8618c691e09fc53d374d6f3830529c9eadd33e`. 새 환경 `/workspace/daaegame`에서 기존 PR 브랜치를 받아 fast-forward했다. 시작 시 작업 트리는 깨끗했다. `.agents/skills`는 checkout에 없고 `/workspace/.agents`도 비어 있었다. AGENTS → CLAUDE → ROOM13_GUIDE → CODEX_OPERATING_GUIDE를 읽었다. 이번 요청의 merge/deploy 금지가 과거 일반 공개 지시보다 우선한다.

## 실제 확인과 변경

- `/usr/bin/chromium`과 Python Playwright, 저장소 웹 실행본을 localhost:8765에서 사용했다. 실제 엔진 버전 0.20.28.
- 선택 제목은 밝은 금색 글자만 밝은 배경 위에 있었다. 기존 B 카드 한 장을 제목 받침으로 사용하고 갈색 28/30px 글자로 바꿨다. 선택 본문은 24/28→26/30px. PR29의 종이 카드 및 번호키·콜백을 보존했다.
- 질문 본문과 번호는 26/28→28/32px. 높이 측정도 같은 크기로 바꿨다. 기존 명시적 페이지 분할을 보존했으며, 큰 글씨 모바일에서는 긴 세 번째 질문이 두 번째 페이지로 이동한다. 12개 질문 표본은 총 8쪽에 빠짐없이 담겼고 각 페이지 하단 331~376px가 페이지 조작 시작 416px보다 위였다.
- 대화 하단 조작은 PC 20→24px, 터치 28→30px, 더보기 아이콘은 PC 20×15→28×21, 터치 26×20→32×24. 기존 터치영역과 기준선·action은 유지했다.
- 이름표/얼굴은 실제 PC·모바일 화면에서 본문과 겹치지 않았다. 얼굴 크기·위치는 바꾸지 않았다. 이름표/얼굴의 전체 재디자인 완료를 의미하지 않는다.
- 질문·선택의 카드에는 Crop+Frame 한 겹이 사용되며, 별도 outline/추가 테두리를 덧씌우지 않았다. 실제 hover 캡처에서 빨간 외곽선이 확인됐다.
- 메인은 `main-current-desktop.png`에서 기존 사각 버튼을 확인했다. 새 primary/secondary 버튼은 부모의 업로드 승인 대기 지시에 따라 가져오거나 연결하지 않았다. 메인 수정은 보류다. 기존 에셋 픽셀은 수정하지 않았다.
- 대사·사건·분기·선택 결과·주민 정책·원탁 카메라 및 설정/지도 큰틀은 변경하지 않았다. 이미 해결된 질문 뒤 대사 겹침/선택 제목 찌그러짐을 새 결함으로 기록하지 않는다.

## 검증 범위

원본 RPY를 기존 웹 엔진의 `renpy_exec`/`load_string`으로 임시 로드했다. `qa_runtime.py`와 `qa_surfaces.py`가 재현 스크립트다. 새 SDK 패키지 빌드·공개 적용 결과가 아니다. 질문/선택은 무해한 콜백을 둔 표본 화면이며 자연 플레이 완주가 아니다.

- 통과: 전체 단위 978개(34.697초), 입력 guard 3개·질문배치 2개·선택길이 1개, git diff --check.
- 통과: 기존 PR29 검사를 수정 전 재실행. 이번 수정 후 PC 1280×720, 모바일 844×390, 모바일 큰 글씨, 긴 선택/질문, 실제 빨간 hover, 선택 번호키/터치, 선택 열기/닫기 3회.
- 통과: 대화 더보기→설정→닫기 3회, 질문 이전/다음 3회, 질문 돌아가기→재열기 3회, 질문 번호키/터치, 페이지 하단 측정. pageerror 없음. `captures/runtime-review.json`, `captures/surfaces-result.json` 참조.
- 통과: 기존 `dev/qa_b_dialogue.py` 기준 실행(수정 전)에서 얼굴·큰 글씨·설정 복귀·여관/숲/마을 지도 확인. 임시 결과는 `/tmp/r13-ui-followup-before/`.
- 갱신 스크립트 4개 실행. 기존 receipt의 오래된 source_line 10개가 갱신됐으나 UI와 무관하므로 해당 생성 차이만 제외했다. 대사 원문 변경 없음.
- 초기 QA 실패: 큰 글씨 모바일에서 3번 질문이 2쪽으로 이동했는데 1쪽에서 누르려던 검사 가정을 수정했다. 페이지를 연 뒤 다시 검증해 통과. 임시 대화 인물을 지우지 않아 겹쳐 보인 검사 장면도 배경 초기화 후 재촬영했다. 게임 결함으로 분류하지 않는다.
- 미실행: standalone SDK lint, 새 웹 빌드·새 패키지 실행, 공개본 최신 SHA 대조, 전체 자연 플레이. `/workspace/renpy-sdk`는 없고 `/root/.cache/renpy` 읽기는 Permission denied였다. SDK 다운로드·403 경로·CI artifact를 재시도하거나 우회하지 않았다.

## 캡처

모두 이 폴더 `captures/` 아래 실제 Chromium 캡처다.

- 선택: `carriage-before.png`, `carriage-after-runtime.png`, `carriage-after-hover-runtime.png`, `carriage-mobile-large-after-runtime.png`.
- 대화: `dialogue-before-desktop.png`, `dialogue-after-desktop.png`, `dialogue-before-mobile-large.png`, `dialogue-after-mobile-large.png`.
- 질문: `questions-before-desktop.png`, `questions-after-desktop.png`, `questions-after-hover.png`, `questions-after-mobile-large.png`, `questions-long-mobile-large.png`, `questions-many-mobile-large.png`.
- 메인 현재 상태: `main-current-desktop.png`.

전체 승인 시안과 일치 또는 모든 UI 완료라고 판단하지 않는다. 남은 일은 승인 후 새 메인 버튼 실물 연결·검수, 정상 SDK 환경의 lint/패키지 통합 검증, 최종 시각 검토다. 병합·배포하지 않는다.
