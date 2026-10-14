# 월드맵 v5 건물 레이어·이동 PR 후보

v5 원본을 마을 지도에 연결했다. 22개 구조물에 독립 투명 다각형 레이어를 만들고 8개 실제 목적지만 UI 이름과 클릭 이동에 연결했다. 선택·호버·키보드 포커스가 해당 건물에 적용된다. 목적지 선택 뒤 별도로 이동을 확정하며 기존 이동 비용(시간 0)과 숙박/사건 조건을 유지한다.

## 기준과 변경 범위

- 기준 main `47618b989b1d7c79f0964c12db0c40bf4bb34cb1`, `0.17.25-dev`. 작업 도중 추가된 마차 색·다람이 기쁨 표정 변경을 최신 ZIP에서 그대로 보존했다.
- 승인된 아트 전달 커밋 `e829cdbdbf9df10102676b287c67854656881dc5`에서 PNG **한 파일만** 가져왔다. 아트 브랜치 전체를 병합하지 않았다.
- 원본 SHA256: `86ef28a4971e244aadca28833414a800f22a03c0f0a82081dea7c4fc5210f4fd`, 1672×941, 2,635,792 bytes.
- Library 원본 다운로드는 403이었으나 부모가 원본을 Git 아트 브랜치로 전달하여 해결됐다. 다른 지도로 대체하지 않았다.
- 기존 여관 그림과 인접 이동을 유지했다. 신당/채석장/배경 주택에는 새 방문 노드나 이야기가 없다.
- main 병합·실배포는 하지 않았다. `preview/room13-dev/` 공개 패키지는 이 PR에서 변경하지 않는다.

## 레이어 구현과 정확한 한계

이 결과는 사각형 클릭 상자만 얹은 것이 아니다. `room13_worldmap_v5.rpy`는 각 구조물마다 `AlphaMask(Crop(original), polygon)`으로 **별도 투명 Displayable**을 구성한다. 이미지 버튼의 `focus_mask=True`가 그 알파 형태를 클릭 판정에 사용한다. 동일 좌표의 투명 SVG 22개와 [레이어 검수 페이지](../../design/maps/20261014/layers.html)도 제공한다. SVG는 인접한 원본 PNG를 참조하므로 그 PNG와 함께 전달해야 한다.

원본 PNG 픽셀과 건물 외형은 다시 그리지 않는다. 이미지 편집 도구의 투명 분리 시안은 위치/형태가 달라져 채택하지 않았다. 승인된 원본과 직접 지정한 다각형만 사용한다.

**완료한 것:** 독립 투명 다각형 레이어 22개, 실제 목적지의 다각형 클릭과 개별 강조, 별도 UI 이름, 기존 이동 연결.

**완료했다고 주장하지 않는 것:** 픽셀 단위 정밀 배경 제거, 건물을 지운 깨끗한 배경판, 22개의 독립 PNG 에셋. 다각형 가장자리에는 일부 눈/바닥·부속물이 포함될 수 있다. 건물 밑의 원본 배경은 그대로이며, 이번 지도는 목적지 선택 화면이지 건물을 드래그하는 편집기가 아니다. 완전한 스프라이트 미술 납품이 필요하면 별도 정밀 마스킹 검수가 남는다.

## 검증

- `contract-report.json`: 256개 해금/사건/비밀 장소 현재 위치 조합. 숙박 및 임시 객실 조건, 미발견 비밀 노드 숨김, 저장된 선택 재검사, 레이어 22개·목적지 8개, label 영역의 경계/서로 겹침 없음, 원본 해시 일치.
- `browser/report.json`: 최종 후보 패키지에서 실제 Chromium 마우스·방향키/Enter/Escape·터치 입력. 명시적인 2일차 숙박 등 fixture를 사용했으며 자연 14일 완주 검증으로 주장하지 않는다.
- 8개 건물 다각형 선택, 투명 사각 모서리 클릭 무시, 개별 hover/focus, 선택·취소 상태 불변, 확정 이동 및 지도 재진입, 실제 저장/불러오기, 기존 여관 이동, 비밀 장소 접근성 이름/툴팁 숨김, 844×390 터치와 390×844 목록, 중복 클릭 시간 불변.
- Ren'Py 8.5.3 compile 성공. lint에는 기존 스트리밍/레거시 이미지 16개 `is not loadable` 경고가 남고 새 지도 관련 오류는 없다. `lint.txt` 참조. 런타임 page error 0.
- 소스 ZIP 내부에서 최신 main 변경 파일이 보존되는지 바이트 비교했다. 여관 배경/대본 파일 변경 없음.
- 실물 휴대폰·스크린 리더 음성 출력·자연 전체 캠페인은 미검증이다. 세로 화면은 기존 가로 게임의 축소/레터박스와 회전 안내를 유지한다.

## 검토할 화면

- `before-world.png`, `before-inn.png`: 변경 전 지도.
- `browser/02-world-all-eight.png`: v5 적용 후.
- `browser/04-hover-individual-building.png`, `browser/05-keyboard-focus.png`: 개별 강조.
- `browser/10-mobile-landscape.png`, `browser/11-mobile-large-list.png`, `browser/12-mobile-portrait-list.png`: 모바일.
- `layers-gallery.png`: 배경과 분리된 투명 레이어 검수.
- `baseline-reception.png`, `baseline-hall.png`, `baseline-kitchen.png`: 실제 인게임 여관 참고. 복도는 오른쪽 벽, 왼쪽 전경 계단 개구부의 난간, 닫힌 13호 문까지 이어지는 바닥이다. 이 사실은 차후 여관 아트용이며 새 여관 그림은 적용하지 않았다.

## PR 이후 릴리스 절차 — 별도 승인 필요

현재는 **검증된 소스 PR 후보**다. 부모가 PR과 미술 한계를 검토한 뒤 main 병합/배포를 별도 지시해야 한다.

1. 최신 main을 다시 확인하고 이 소스 ZIP 및 아트·manifest 변경을 보존한다. ZIP을 별도 소스 작업 디렉터리에 푼다.
2. 공개 `preview/room13-dev/`를 외부 후보 디렉터리로 복사하고 Ren'Py **8.5.3** SDK를 준비한다. 저장 토큰 쓰기 위치가 제한된 환경은 `RENPY_PATH_TO_SAVES`를 쓰기 가능한 임시 디렉터리로 지정한다.
3. 소스에서 `python dev/package_web_webp.py --release <candidate>/room13-dev --sdk <renpy-8.5.3-sdk> --asset-root <repo> --work <fresh-work>` 실행. 새 JSON의 패키징 허용 및 원본 PNG의 selected_asset_overlay가 이 ZIP에 포함된다.
4. `python dev/test_worldmap_v5.py`, 후보를 HTTP로 연 후 `python dev/qa_worldmap_v5.py --url http://127.0.0.1:<port>/room13-dev/ --out <results>` 실행한다. lint와 실제 화면을 검토한다.
5. 승인 이후에만 최종 후보 패키지를 릴리스 경로에 반영하고 manifest/part 해시를 확인해 배포한다. 이 PR 자체는 공개 패키지를 덮어쓰지 않는다.

노드별 조건과 아트 매핑은 [MAPPING_KO.md](MAPPING_KO.md), 런타임 변경의 읽기 쉬운 diff는 `source.patch`를 참조한다. ZIP이 실행 소스의 기준이며, diff는 검토용이다.
