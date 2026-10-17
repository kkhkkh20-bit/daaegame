# 지도 적용 검수 · 0.19.3

실제 Ren’Py 웹판을 Chromium에서 입력해 캡처했다. PC는 1280×720, 터치는 844×390이다. 에피소드 날짜·자료·발견 상태는 명시적인 검사 fixture이며 자연 진행 전체 플레이스루를 뜻하지 않는다.

- [마을 지도](01-village.png): 별도 핀 없이 건물·지형 선택, 작은 현재 위치 표시와 하단 확정.
- [여관 글씨 목록](03-inn-text.png): 실제 장면 사진과 층별 이동, 비밀 장소는 조건에 맞춰 제외.
- [미발견 숲·산길](04-mountain-hidden.png): 온실과 제단의 이름뿐 아니라 건물도 숨긴다.
- [모바일 마을](05-village-mobile.png), [모바일 여관](06-inn-mobile.png).
- [여관 아래 옛 시설](07-underground.png): 산길과 별개이며 기존 발견 조건을 지킨다.
- [발견 후 외곽](08-mountain-discovered.png): 제단 돌기둥과 온실 지붕이 UI에 가리지 않는다.

`browser-results.json`에 실제 입력 검사와 빌드 SHA, `build-report.json`에 배포 파일의 크기·SHA를 기록했다. `native-results.json`은 관련 실제 엔진 검사 결과다. `check.txt`는 단위·lint 검사 결과다. 마을·외곽 다각형 전체의 교집합이 없고 각 클릭점이 올바른 마스크 안에 있는 것도 단위 검사한다.
