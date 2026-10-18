# 리소스 도감·장소별 화면 UI 개선

기준 main: `39573ae51eabbe109040243a358d423bc318f154`.
독립 브랜치: `codex/resource-dashboard-polish-20261017`. 이 작업에서 main 병합/배포하지 않는다.

## 재현과 변경

- 공개 URL 두 곳은 `urllib.request.urlopen` 읽기 요청에서 모두 `Tunnel connection failed: 403 Forbidden`이었다. URL: `https://kkhkkh20-bit.github.io/daaegame/preview/resource-dashboard/`, `https://kkhkkh20-bit.github.io/daaegame/reports/place-balance-01936/`. 제한을 우회하지 않았다. 모든 캡처와 브라우저 검증은 **최신 main 기반 로컬 서버**다.
- 장소 갤러리는 viewport 선언이 없었다. 실제 모바일 에뮬레이션에서 390px 장치가 **innerWidth 980 / scale 0.397959**로 축소됐다(`before-mobile-metrics.json`). 수정 후 390px에서 가로 넘침 없이 표시된다.
- 원래 도감은 캐릭터 ID·파일 경로·조건/좌표 JSON을 기본 팝업과 카드에 노출했다. 원본 캡처나 원화 확대도 별도 창/원본 이동에 의존했다. 전후 캡처 참조.
- 기본 화면은 이름·한글 장소·동작·날짜/시간·조건부 연결/캡처 상태를 표시한다. ID/경로/원시 조건/좌표/소스 증거는 **접힌 ‘상세 정보’**에 보존한다. 미확인 조건을 적용/등장 확정으로 바꾸지 않는다.
- 인물은 `object-fit:contain`으로 전신을 보여 주고, 게임 캡처는 자동 높이로 전체 비율을 유지한다. 눌러 원본 파일을 비율대로 확대하고, 원본 크기/화면 맞춤, 스크롤, Escape/닫기/브라우저 Back, 초점 복귀를 지원한다. 원본 파일 자체가 아틀라스인 경우 원본 파일의 모든 그림이 표시되며 원화를 수정하지 않는다.
- 음향의 실제 곡명·작곡가·크레딧 링크를 게임의 `music-v6-credits.txt`에서 추가 추출한다. 역할은 한국어로 표시하고 경로/사용 조건/볼륨/루프 근거는 상세 정보에 둔다. 소리 자체는 변경하지 않는다. 재생은 클릭해야 시작하며 다른 소리/탭/필터로 옮기면 이전 소리를 정지한다.
- 66장 원본 캡처와 원본 figcaption은 HTML에 그대로 유지한다. 실제 엔진 캡처/검수용 상태/해당 캡처 범위/추가 검토 필요라는 구분을 유지한다. 화면 스크립트가 이를 읽어 검색·장소·날짜·시간 필터와 카드로 정리한다.

## 검증과 다시 실행

```sh
python3 tools/resource-dashboard/build.py
python3 -m unittest discover -s tools/resource-dashboard -p 'test_*.py' -v
node --check tools/resource-dashboard/web/app.js
node --check tools/resource-dashboard/web/viewer.js
node --check tools/resource-dashboard/gallery/ui.js
python3 -m http.server 8765 --bind 127.0.0.1
# 별도 터미널
python3 tools/resource-dashboard/qa_browser.py
```

- 추출/계약/재생성 보존 단위 테스트 7개.
- Chromium 151, 데스크톱 1365×1000 / 실제 모바일 에뮬레이션 390×844.
- 한국어 카드·상세 정보, 세로 원화/가로 캡처 비율, 반복 팝업, Tab 초점 가두기, Escape/Back/닫기/초점 복귀, 장소/날짜/시간 필터, MP3/WAV 실제 재생·음량·정지·중복 방지·오류 피드백·버전 갱신.
- 터치 2점 입력을 전송해 실제 visualViewport 배율 상승과 축소 복귀를 확인한다. CSS 설정만 확인한 테스트가 아니다.
- 게임 코드/원화/배치를 수정하지 않아 Ren'Py 실행/재빌드 검사는 수행하지 않았다. 이 작업은 조회 화면과 생성기 표시 메타데이터만 변경한다.

## 통합 담당 단계

1. 최신 main에 이 브랜치를 병합한다. 게임/원화/배치 및 Sites 선택 보드는 변경하지 않았다.
2. `python3 tools/resource-dashboard/build.py`와 위 검사 실행. 생성 파일 충돌은 수동 병합하지 말고 재생성한다.
3. 빌드는 `preview/resource-dashboard/`의 화면과 데이터, 공통 확대 뷰어를 생성한다. `gallery.py`가 재생성된 장소 리포트의 원본 figcaption/이미지를 보존하면서 `ui.js/ui.css` 연결을 중복 없이 붙인다. UI 소스는 `tools/resource-dashboard/gallery/`다.
4. 기존 단일 Pages 배포 과정으로 게시한다. `reports/place-balance-01936/index.html`, `ui.js`, `ui.css`와 `preview/resource-dashboard/viewer.js/viewer.css`를 함께 포함한다.
5. 여기서는 공개 URL 검수가 차단됐으므로 배포 담당 환경에서 공개 경로/캐시/모바일 접근을 최종 확인한다.

주요 전후 캡처: `before-character.png` → `after-character.png`, `before-audio-mobile.png` → `after-audio-mobile.png`, `before-gallery-mobile.png` → `after-gallery-mobile.png`, `after-portrait-expanded.png`, `after-landscape-mobile.png`.
