# 카드 기술 ID 노출 후속 점검

- 기준 main: `de62ee8c3a931a7b63ef4df9640fb14a2c32ac4a` (0.19.44 대시보드 재생성).
- 브랜치: `codex/dashboard-hide-technical-ids-20261018`. main 병합/배포하지 않음.

## 발견과 패치 범위

최신 main 로컬 화면에서는 카드 ID 노출을 재현하지 못했다. `resident_piko`의 이름은 `피코`이며, 현재 카드 템플릿에는 ID 출력이 없다. 전체 63명 팝업의 기본 표시에도 기술 ID/원시 조건은 없었다. ID와 경로/조건 근거는 접힌 상세 정보에 이미 보존돼 있다.

이전 UI(`c1a1642e^`)는 카드 안에 `<div class="muted mono">${esc(c.id)}</div>`를 출력했다. 이전·현재 HTML이 같은 `app.js` URL을 사용하므로 구형 스크립트 캐시 가능성이 있다. 공개 환경의 원인으로 확정하지는 않는다.

생성기에서 `app.js?v=<스크립트 내용 SHA256 앞 16자리>`를 출력하도록 변경했다. 새 HTML을 받으면 변경된 표시 스크립트를 요청하고, 후속 빌드도 자동 갱신된다. 이미 열린 구형 페이지나 캐시된 HTML을 소급 변경하는 기능은 아니다. ID 검색은 `search` 사전 계산 필드 외에도 `c.id`를 직접 대소문자 구분 없이 검사하도록 명시했다. 이름·동작 표시, 상세 정보 구조와 디자인에는 변경이 없다.

생성 결과의 캐릭터/음향 데이터는 이전 main과 동일하다. 달라진 index 항목은 game_commit/data_version/generated_at/inputs뿐이다. 게임 원화·대사·배치·음원·Sites 데이터 수정 없음.

## 검증

```sh
python3 tools/resource-dashboard/build.py
python3 -m unittest discover -s tools/resource-dashboard -p 'test_*.py' -v
node --check tools/resource-dashboard/web/app.js
python3 -m http.server 8765 --bind 127.0.0.1
# 별도 터미널
python3 tools/resource-dashboard/qa_technical_ids.py
```

단위 테스트 8개. 새 브라우저 회귀 검사는 데스크톱 1365px와 모바일 390px에서 전체 63명의 ID 검색, 카드 이름, 팝업 기본 화면과 펼친 근거를 검사한다. 장소·음향·점검 기본 화면의 기술 문자열 비노출, 동작 검색, 버전이 붙은 스크립트 요청도 검사한다. 결과는 `browser-report.json`, 실제 로컬 캡처는 `piko-card-*.png`, `piko-popup-*.png`.

## 공개 접근 제한 및 통합

정상 `urllib.request.urlopen`으로 `https://kkhkkh20-bit.github.io/daaegame/preview/resource-dashboard/` 읽기를 시도했으나 프록시 `Tunnel connection failed: 403 Forbidden`으로 차단됐다. 우회하지 않았다. 공개 검수는 차단, 로컬 검수는 별도로 수행했다.

통합 담당이 브랜치 병합 후 생성기를 다시 실행하고 기존 Pages 과정으로 배포한다. 공개 HTML이 버전이 붙은 app.js를 요청하는지, 피코 카드에 이름만 보이고 인물 상세 근거에는 ID가 남는지 확인한다. 본 패치의 스크립트 URL 갱신은 새 HTML 수신 후 유효하다.

캡처 주의: 피코 카드의 기존 프로필 썸네일은 투명 픽셀만 포함한다(Pillow getbbox=None). 따라서 카드 캡처의 그림 영역이 비어 있다. 이미지 로드는 확인했으며 이 ID 노출 패치에서는 기존 원화·썸네일을 바꾸지 않았다.
