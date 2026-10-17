# 다람탐정

아이와 함께 푸는 동물 마을 추리 게임.

지금 main은 **Room13(Ren'Py 웹판)** 하나만 개발한다. 작업 전에 `ROOM13_GUIDE.md`를 읽는다.

- 보관한 예전 판
  - 1장 「열세 번째 침대」 HTML 테스트판: `archive/ch1-html-test` 브랜치(2026-10-17 main에서 정리)
  - 그보다 앞선 세로 게임: `archive/legacy-20261008` 브랜치(복구는 `docs/LEGACY_RESTORE.md`)

## 실행

- 웹: `https://kkhkkh20-bit.github.io/daaegame/` → `preview/room13-dev/`로 넘어간다.
- 루트 `sw.js`는 예전 테스트판이 설치한 서비스 워커를 스스로 지우는 역할만 한다. 지우지 않는다(지우면 예전 워커가 브라우저에 남는다).

## 파일

| 경로 | 역할 |
| --- | --- |
| `experiments/renpy-ch1/` | Room13 원본(Ren'Py) |
| `preview/room13-dev/` | Room13 공개본. `dev/build_web.py`로만 만든다 |
| `preview/room13-music/` | 음악 미리보기 |
| `design/` | 디자인 자료. Room13 지도 검사가 `design/maps/`를 읽는다 |
| `docs/`, `reports/` | 문서와 검수 기록 |
| `index.html`, `sw.js` | 첫 주소 안내, 예전 서비스 워커 정리 |
