# 작업 규칙

- 배포: 검증을 마친 변경은 별도 확인 없이 `main`에 반영하고 push한다(GitHub Pages 공개까지). 2026-10-13 저장소 소유자 지시.
  - 반영 전 해당 프로젝트의 검사(단위 테스트, Ren'Py lint, 실제 브라우저 확인)를 통과해야 한다.
  - `main`이 앞서 있으면 병합해서 반영하고, 강제 push는 하지 않는다.
- Room13(Ren'Py) 웹판: **먼저 `ROOM13_GUIDE.md`를 읽는다.** (2026-10-14 리팩토링, 0.18.0부터)
  - 원본: `experiments/renpy-ch1/` 일반 파일. 예전 `ROOM13_SOURCE_HANDOFF.zip` 방식은 폐지됐다. zip을 만들거나 풀지 않는다.
  - 공개본: `preview/room13-dev/`. `experiments/renpy-ch1/dev/build_web.py`로만 만든다. 손으로 고치거나 병합하지 않는다.
  - 검사: `dev/check.sh`(단위+lint), `dev/run_renpy_tests.sh`(화면), `dev/qa_*.py`(브라우저).
  - 함수 덮어쓰기 순서: `experiments/renpy-ch1/docs/OVERRIDE_MAP.md`. 층을 더하면 `python3 dev/override_map.py --write`.
