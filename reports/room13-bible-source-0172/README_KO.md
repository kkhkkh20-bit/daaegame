# 최신 대본·인물·관계 검토용 텍스트 추출본

- 실제 배포 버전: **0.17.2-dev**
- 기준 main: **bc0359b16935feb77712b791ca5335ab06f61480**
- 정본 경로: `preview/room13-source/ROOM13_SOURCE_HANDOFF.zip`
- ZIP 내부 루트: `experiments/renpy-ch1/game/`
- 원본 SHA-256과 각 추출 파일 해시: `manifest.json`

사용자가 사건 진상·스포일러를 포함한 최신 대본과 인물관계 검토 자료의 공개 GitHub 추출을 승인했다. 게임 파일/실행 코드 동작은 변경하지 않은 추출본이다. 진행 중인 0.17.3 가로 배경 작업본은 포함하지 않았다.

## 읽는 순서

1. `resident-facts.json`: 현재 Room13 주민 데이터의 이름·직업·지키려는 것·일상 행동·기본 주간 위치를 원문 그대로 추출했다. 등장인물 전부가 이 주민 사전에 들어 있지는 않으므로 아래 런타임 이름·대본도 함께 읽는다.
2. `source/game/room13-content.json`: 증거, 질문, 행동, 사건 주장·결말 및 인물 원문. **이 파일 단독으로 최종 대사를 확정하지 않는다.** 아래 init 단계의 교체·래퍼가 실제 표시 내용을 바꾼다.
3. `source/game/room13-dialogue-openings.json`, `room13_dialogue_openings_20261013.rpy`: 날짜/사건/판결 상태별 대화와 말투. `calendar_daily`, `calendar_ready` 및 함수의 분기까지 읽는다.
4. `room13_conversations.rpy`, `room13_life.rpy`, `room13_rules.rpy`, `room13_revision.rpy`, `room13_week2*.rpy`, `room13_home.rpy`, `room13_first_mystery.rpy`, `room13_gate_continuity.rpy`: 실제 대사·호칭·사건 상태와 관계 반응을 확인한다.
5. `source/game/systems/room13_debate.rpy`: **최신 0.17.1에서 갱신된 회의 실패/입증 규칙 포함**. 과거 신뢰도 감소 설명으로 회귀하지 않는다. `systems/room13_first_day_flow.rpy`, `room13_livelihood_*.rpy`, `room13_work_clues.rpy`도 최종 안내와 질문 조건에 영향을 준다.
6. `korean-text-index.tsv`: 위 파일의 한국어가 있는 원문 행/JSON 경로를 찾는 검색용 인덱스다. 코드와 대사, 조건별 상충 문장이 함께 들어 있으므로 확정 설정집으로 취급하지 않는다.

인물관계는 실제 대사·조건·사건 상태를 근거로 구분해야 한다. 보호·의심·가족 관계를 이름이나 감정 문장 하나만으로 추측해 확정하지 않는다. 기존 로딩/동작 코드를 함께 추출한 이유는 최종 표시 우선순위를 검토하기 위해서다. 오래된 루트 `experiments/renpy-ch1` 스냅샷, 구 HTML 프로토타입 및 0.17.0 문서를 최신 정본으로 혼동하지 않는다.
