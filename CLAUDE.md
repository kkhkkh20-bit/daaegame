# 작업 규칙

- 배포: 검증을 마친 변경은 별도 확인 없이 `main`에 반영하고 push한다(GitHub Pages 공개까지). 2026-10-13 저장소 소유자 지시.
  - 반영 전 해당 프로젝트의 검사(단위 테스트, Ren'Py lint, 실제 브라우저 확인)를 통과해야 한다.
  - `main`이 앞서 있으면 병합해서 반영하고, 강제 push는 하지 않는다.
- Room13(Ren'Py) 웹판: 소스는 `preview/room13-source/ROOM13_SOURCE_HANDOFF.zip`, 공개본은 `preview/room13-dev/`.
  게임 데이터 재포장은 소스 안의 `experiments/renpy-ch1/dev/package_web_webp.py`(Ren'Py 8.5.3 SDK 필요).
