# 다람탐정

아이와 함께 푸는 동물 마을 추리 게임.

지금 main은 **1장 「열세 번째 침대」 테스트판**이다(가로 화면, 고정 성공 경로).
기존 게임(세로 `game.html`, `chapter-one/` 등)은 `archive/legacy-20261008` 브랜치에 보관했다 — 복구는 `docs/LEGACY_RESTORE.md`.

## 실행

- 웹: `https://kkhkkh20-bit.github.io/daaegame/`
- 가로 화면 기준(844×390, 640×360에서 검수). 진행 기록은 브라우저 저장소의 `daae-inn1:` 키에 따로 남는다.

## 파일

| 경로 | 역할 |
| --- | --- |
| `index.html` | 1장 테스트판(빌드 결과, 단일 파일) |
| `art/` | 게임 그림(배경·인물·증거·지도) |
| `ch1/src/ep1_inn_script.js` | 1장 대본·증거·회의·최종 대결·후일담 데이터. 대본 교체는 이 파일 |
| `ch1/src/ep1_inn.js` | 대본 데이터를 엔진에 연결(조사 조건, 프롤로그·후일담 진행, 실패 재개) |
| `ch1/src/rtg_inn.js` | 원탁 회의·최종 대결 판정 확장 |
| `ch1/src/worldmap.js` | 전체 지도(승인 시안 v1) |
| `ch1/src/wide209_J.js`, `inn_early.js` | 가로 화면 구성, 저장 분리 |
| `ch1/build/build.py` | `base-engine.html` + `ch1/src` → `index.html` |
| `ch1/STATUS.txt` | 구현 규칙, 실제 검수 결과(1장 완료 규칙 20항목 대조), 남은 일 |
| `ch1/qa/` | 실제 탭 완주 로그와 캡처 |
| `ch1/tests/` | 완주·배치 검사 스크립트(Playwright, 경로는 작업 환경 기준) |
| `sw.js`, `manifest.webmanifest`, `icons/` | 오프라인 캐시와 앱 설치 정보. `index.html`을 바꾸면 `sw.js`의 `VERSION`을 올린다 |
| `design/`, `docs/` | 디자인 자료와 문서 |
| `tools/` | 기존 게임(`game.html`)용 개발 도구. 보관 브랜치와 함께 쓴다 |

## 빌드

```sh
python ch1/build/build.py                 # index.html 생성
python ch1/build/build.py --test /tmp/t.html   # 검사용(window.__T 훅). 공개 경로에 두지 않는다
```
