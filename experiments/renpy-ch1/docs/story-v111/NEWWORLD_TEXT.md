# 새 세계관 대사판 (0.19.89부터)

V1.1.1 원본(`game/v111/records.json`)은 원본 대본과 글자까지 같아야 한다(`dev/test_v111.py`). 새 세계관 수정은 원본을 고치지 않고 `game/v111/newworld/d01.json` ~ `d14.json`에 레코드 ID로 적는다. 적용은 `game/room13_v111_newworld_text.rpy`가 한다.

| 키 | 뜻 |
|---|---|
| `replace` | `{레코드ID: {"text": 새 문장}}` 원본 줄의 문장만 바꾼다. 화자·표정·조건·효과는 원본 그대로 |
| `before`, `after` | `{레코드ID: [새 줄, ...]}` 원본 줄 앞뒤에 줄을 넣는다 |
| `drop` | `[레코드ID, ...]` 화면에 내지 않는다(효과·조건 처리는 장면 코드 그대로) |
| `evidence` | `{증거키: {"name": ..., "variants": {상태: 설명}}}` |

새 줄: `{"id": "NW_D01_S05_A01", "speaker": "다람" 또는 null, "text": ..., "kind": "dialogue|narration", "expression": "anxious", "when": "owl_alive", "cut": "O47-handprints"}`

- `id`는 `NW_`로 시작하고 겹치지 않는다. `speaker`는 기존 화자 목록(`MS14_SPEAKERS`)만 쓴다.
- `when`은 `R13_NW_WHEN`에 이름으로 정의한 판정만 쓴다. 문자열을 실행하지 않는다.
- `cut`은 기존 도트 그림 `assets/room13-ep-<이름>.webp`만 쓴다. 새 그림을 만들지 않는다.
- 잘못된 참조가 있으면 게임이 시작할 때 멈추고, `dev/test_newworld_text.py`도 실패한다.
- 장면 코드는 모두 `r13_v111_lines([...])`로 대사를 낸다. 4~14일은 생성기(`dev/build_v111_days45.py` 출력 함수)가 이 모양으로 만든다. 1~3일 파일은 손으로 관리한다.
- 원본 줄에는 레코드 ID(`line_id`)가 실려 나간다. 1~3일의 승인된 다람 표정 연결 11개는 순번·문장이 아니라 이 ID로 찾으므로, 앞에 줄을 넣거나 문장을 바꿔도 유지된다.
- 마차 장면 8줄의 기존 덮어쓰기(`R13_V111_CARRIAGE_TEXT`)는 그대로 둔다.
- 작업 순서: 사건마다 원문 대 수정안 문서로 소유자 확인 → 대사판 반영 → `dev/check.sh`와 그 날짜 실제 진행 확인.
