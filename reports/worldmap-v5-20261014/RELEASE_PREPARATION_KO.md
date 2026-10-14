# 기존 저장 호환·후반 긍정 분기 및 배포 준비

## 범위와 기준

최신 main `47618b989b1d7c79f0964c12db0c40bf4bb34cb1`과 충돌 없음(브랜치의 조상). 기존 공개 경로 패키지 버전은 `0.17.25-dev`, archive SHA256 `bba431fcbbace463df278ff22826d984cb01ff065c9c041415e5273b6637e6fb`이다. 테스트용 구판의 transport와 4개 part를 main의 실제 Git blob과 바이트 비교했다.

GitHub Pages 실 URL의 추가 CDN 조회는 연결 터널 403으로 완료하지 못했다(자동 승인 심사 거부 아님). 따라서 **기존 공개 패키지와 동일한 로컬 복사본을 실제 브라우저에서 실행한 검증**이며, 실서버 origin에서 직접 저장했다고 주장하지 않는다. 구판 저장을 새 객체로 재구성하거나 후보에 상태를 주입해서 호환으로 판정하지 않았다.

## 실제 구판 저장 → 후보 복원

`dev/qa_worldmap_compat_week2.py`는 구판에서 2일차 숙박/E03 fixture를 준비한 뒤 **실제 저장 UI**를 눌러 `1-1-LT1.save`를 만든다. 같은 browser context/origin의 IndexedDB를 유지하고 서버가 제공하는 게임만 새 후보로 바꾼다. 새 판 부팅 뒤 저장 파일의 SHA256이 동일함을 검사하고 ‘이어하기’ 및 슬롯 불러오기 UI로 읽는다. 저장 직전과 복원 뒤의 전체 room 딕셔너리가 같고, 새 월드맵으로 수리점 이동 및 시간 불변이 확인됐다. 두 판 모두 `0.17.25-dev`이므로 **서로 다른 archive 해시와 v5 구현 존재 여부**로 실행 판을 확인했다.

## 전체 런타임 긍정 분기

기존 256 fixture는 추출한 기본/비밀 통로 함수의 제한적 검사다. 후반 긍정 분기는 추출 함수를 실행하지 않고 게임의 모든 init 이후 설치된 실제 `r13_places()`를 사용했다. 런타임 체인은 `systems/room13_first_day_flow.rpy` → `room13_route_knowledge.rpy` → `room13_rules.rpy`로 기록됐다. week2 장소 데이터와 day/E19 분기도 실제 엔진에서 실행된다.

- 8일차, E19 없음: 보호시설은 보이고 폐온실은 숨김.
- 실제 `r13_grant(["E19"], ...)` 호출: E19 기록이 생긴 뒤 폐온실이 allowed/nodes에 나타남. 실제 지도 클릭과 이동 확정으로 greenhouse 도착, 8일차 오전 유지.
- 14일차 finale 이전: 제단 숨김.
- 실제 `r13_finale` label 진입: day=14, location=altar, finale_started=True가 실행됨. **검증용으로 지도 overlay를 명시적으로 열어** 제단이 현재 위치로 표시되고 선택되는 것을 확인. finale에 새 지도 진입 동선을 추가하거나 자연 플레이로 전체 결말을 완료한 검증은 아니다. altar는 일반 r13_places에 추가되지 않았고 v5 신당에 이동 연결하지 않았다.

모든 결과와 스크린샷: `compat-week2/`. page error 0.

## 재패키징 및 PR에 포함된 공개 경로 변경

PR의 canonical 소스 ZIP을 새 디렉터리에 풀고 Ren’Py 8.5.3 SDK와 `dev/package_web_webp.py`로 구판 공개 패키지에서 재패키징했다. 결과:

- archive SHA256 `74b11fc409234f54332dd805963f7907f7a2e8c7c55ff383128ea8a8cd8c207a`
- 252,331,225 bytes, 5개 part (각 파일 60 MiB 이하).
- `preview/room13-dev/game.part01`~`game.part05`
- `game-transport.json`, `build-manifest.json`
- `renpy-pre.js` (part 목록과 전체 크기), `index.html` (새 로더 캐시 키)
- `pwa_catalog.json` (part05 포함 목록과 새 버전)

158개 manifest 항목의 실제 크기/SHA256, 157개 catalog 경로 존재, 전체 archive 재조립 해시, 로더의 part 목록/전체 크기, index의 digest 캐시 키를 검증했다. 기존 `game/assets/` 스트리밍 파일은 바뀌지 않았고 여관 관련 배경 이미지 10개는 아카이브 내 바이트도 동일하다. compile 성공, 기존 legacy/streaming 이미지 16개 lint 경고는 보존. 새 코드 오류 없음.

최종 아카이브에서 기존 전체 지도 브라우저 검증도 다시 통과했다(`release-browser/report.json`). PC와 가로 모바일의 조작 검증이며 **세로 모바일은 작은 레터박스, 모바일 최적화 완료 아님**. 실물폰·음성 스크린리더·자연 14일 완주·배포 후 CDN/PWA 업데이트는 미검증이다.

## 승인 후 실제 적용 순서

1. 부모가 PR의 소스, 미술 한계, 저장 호환 결과 및 package 해시를 승인한다. 아직 main 병합·공개 배포는 하지 않았다.
2. main이 `47618b9`보다 진행됐으면 새 source ZIP/공개 package 변경을 먼저 통합하고 **새 main 기준으로 재패키징·해시/회귀 검사**한다. 이전 binary parts로 최신 변경을 덮어쓰지 않는다.
3. 승인된 동일 커밋의 **소스 ZIP과 위 공개 패키지 10개 변경을 함께** main에 반영한다. 소스 ZIP만 병합해서는 실행 게임이 바뀌지 않는다. part05나 loader/catalog 중 일부를 누락하지 않는다.
4. 별도 허용된 Pages 배포를 실행/확인한다. 실 URL의 game-transport/build-manifest, loader cache key가 승인한 커밋·archive 해시와 맞는지 확인한다.
5. 배포 후 새 브라우저 cold load, 기존 사용자 저장 불러오기, 서비스워커/PWA 갱신, 모바일 가로 지도 smoke를 확인한다. CDN cache가 구판을 제공하면 배포 완료로 보고하지 않는다.

재현 명령(소스 프로젝트에서):

```sh
RENPY_PATH_TO_SAVES=<writable-save-root> python dev/package_web_webp.py --release <candidate>/room13-dev --sdk <renpy-8.5.3-sdk> --asset-root <repo> --work <fresh-work>
python dev/test_worldmap_v5.py
python dev/qa_worldmap_v5.py --url http://127.0.0.1:<port>/room13-dev/ --out <results>
python dev/qa_worldmap_compat_week2.py --url http://127.0.0.1:<port>/room13-dev/ --link <served-root>/room13-dev --baseline <old-public-copy>/room13-dev --candidate <candidate>/room13-dev --out <compat-results>
```

호환 테스트는 `--link` symlink만 원자적으로 교체한다. baseline과 candidate는 따로 유지하며 동일 origin의 저장 DB를 사용한다. 새 저장을 위해 구판 상태에 fixture를 쓰지만 후보 복원 전에는 candidate의 게임 상태/저장 바이트를 주입하지 않는다.
