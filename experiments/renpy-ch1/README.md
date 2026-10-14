# 다람탐정 · 눈 아래의 열세 번째 방 (Room13, Ren'Py 8.5.3)

이 폴더가 게임의 유일한 원본이다. 작업 방법은 저장소 루트의 `ROOM13_GUIDE.md`를 따른다.

| 경로 | 내용 |
|---|---|
| `game/` | 스크립트(.rpy), 데이터(.json), 웹에 그대로 나가는 그림·글꼴·음악(`game/assets/`) |
| `game/qa_tests/` | Ren'Py 화면 테스트(배포에서 빠짐) |
| `dev/` | 빌드·검사 도구와 단위 테스트(`test_*.py`) |
| `docs/` | 설계 문서, `OVERRIDE_MAP.md`(함수 덮어쓰기 순서), `releases/`(판별 기록), `history/`(예전 인계 기록) |
| `web/runtime.zip` | 웹판 Ren'Py 실행 파일(엔진 쪽, 고정) |
| `story-room13/` | 집필 원본(참고용, 실행 데이터가 기준) |
| `art/` | 원화 작업 파일(배포와 무관) |

자주 쓰는 명령(이 폴더에서):

```bash
export RENPY_SDK=$(dev/setup_sdk.sh)      # SDK 한 번 받기
dev/check.sh                               # 단위 테스트 + lint (몇 초)
dev/run_renpy_tests.sh carriage_skip       # 화면 테스트 (이름 없이 실행하면 표준 묶음)
python3 dev/build_web.py --sdk "$RENPY_SDK" # 웹판을 ../../preview/room13-dev 로 빌드 (10초 남짓)
```
