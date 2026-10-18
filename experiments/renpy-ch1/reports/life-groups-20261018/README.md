# 주민 생활 그룹 구현 인계 — 2026-10-18

배포본 아님. 독립 작업 브랜치 `feat/resident-life-groups-20261018`, 기준 main `fc8c35c5585e8ede3aaea5470bca750548bea1e8`.
main 병합·버전 변경·웹 빌드·배포는 부모의 단일 통합 담당에게 맡긴다. 회의/새12동작/대시보드 파일은 수정하지 않았다.
`.agents/skills`, `AGENTS.md`는 이 체크아웃과 `/workspace/.agents`에 없었다. `CLAUDE.md`, `ROOM13_GUIDE.md`, `docs/OVERRIDE_MAP.md`를 읽었다.

## 현재 활성화 상태 (중요)

세 registry 행은 **모두 기본 비활성**이다. 원화·실게임 검수가 끝난 행만 `game/assets/room13-life-groups.json`의 `status`를 `approved`로 바꾼다. 중립 원화/서로 다른 작업물을 협업 완성으로 공개하지 않는다.

| 행 | 구현/자료 | 남은 작업 |
|---|---|---|
| workshop_pair | day2/3 오전·오후, 최종 visible/where 및 톡 구금·해제·양쪽 offer 검사. 손 목표620,421 / 760,425. 기존 테이블 마스크 및 톡 손/드라이버 keepout 사용. | `awaiting_art`: 부리는 기어가 놓인 천, 톡은 별도 랜턴이라 동일 작업물이 아님. **부리 부품받치기 + 톡 같은 부품맞추기 2포즈** 필요. 배경가구/부품 중복 금지. |
| inn_mending | day2/3/6 오후 여관. 여니 seat505,397, height210; 토리 foot840,525, height212. 기존 주민/따닥/문 클릭 공간 보존. | `awaiting_art`: 토리 neutral은 오른쪽을 봐 왼쪽 여니/천과 시선이 반대이고 335px 떨어짐. **왼쪽 여니의 천을 보는 토리 포즈** 및 더 가까운 위치/앞 안락의자 가림 검토 필요. 후보좌표는 확정 아님. 광장안은 폐기. |
| school_play | day8/9 오전·오후, 소개·구조·학교 flag 전부 필요. 사망3flag/컷/회의/사건/혼잡이면 없음. 실제 놀이3원본과 WebP export 연결. | `awaiting_live_review`: SDK 403으로 실제 화면/알파클릭/세이브로드 미검수. 원본 저알파 잔여 픽셀 보존했으므로 실제 picker 가장자리 확인 필요. |

## 구현

- 마지막 `init 181` 단계. map27 178 / 접점179 / 배치보정180 이후 적용, 별도 파생 캐시 없음. 앞단 캐시 결과를 수정하지 않고 현재 조건을 매번 검사한다.
- 기존 성인 actor만 복사/재배치한다. 부재/다른장소/사건포즈/offer면 원래 solo 결과 그대로. 생활그룹에 없는 주민을 옮기거나 숨기지 않는다.
- 아이들3은 기존 클래스 소개에 나온 인물만 별도 조건부 actor로 추가. R13_RESIDENTS/주간일정/최종 where에는 등록하지 않는다. 다른 주민과 영역이 겹치면 그룹 전체 생략.
- 그림은 개별 투명 에셋과 기존 `r13_actor_hit_mask` 유지. 큰 합성그림·그룹사각 클릭은 없음. 작은 그룹 버튼은 별도로 둔다.
- 성인 클릭은 원래 `r13_talk`로, 아이 클릭은 새 비소모 개인반응으로 보낸다. stale 아이 클릭이 성인 대화/encounter로 흘러가지 않도록 별도 처리.
- 짧은 다중화자 화면은 현장 인물/가구를 유지하면서 이름·대사를 순차 표시. 취소·저장·불러오기 제공. 열기 직전과 interaction/load 때 조건 재확인.
- `r13_lines`, 이벤트label, 기록/관계/hidden knowledge/encounter/tick/grant API를 호출하지 않는다. 반복·취소 후 `r13_field`로 바로 복귀하여 도착이벤트 재실행도 피한다.
- 기존 대사 ID/원문 및 대사 감사의 소스 줄 번호 유지. 새로운 안정된 `from` 반환 지점 사용. 기존 자동생성 반환점으로 저장된 과거 저장은 프로젝트의 기존 return-recovery 정책 적용 대상이며 별도 실제 검수 필요.

## 검수자료와 재현

`geometry-review.json`은 실제 최종 일정/10단계 Python 배치 함수를 실행한 11조건 결과다. 렌더러·캡션은 host fixture이므로 Ren'Py 실행으로 부르지 않는다.

- `*-before-offline.jpg`, `*-after-offline.jpg`: **오프라인 소스 좌표 검토 합성도**, 상단에 NOT AN ENGINE SCREENSHOT 표시. 실제 스크린샷 아님. 인물 크기·손/발접점·가구관계 검토용.
- `python3 dev/review_life_groups.py`: 위 자료 재생성. 승인 후보만 테스트 안에서 임시 활성화한다.
- `python3 -m unittest discover -s dev -p test_life_groups.py`: 최종 일정 체인, 상태불변, 구금/offer/부재/사망/소개누락/날짜/컷/혼잡, 소스SHA/alpha 보존, stale클릭, 캐시/좌표 검사.
- `game/qa_tests/life_groups.rpy`: 실제 엔진용 후보 fixtures. `dev/run_renpy_tests.sh life_group_workshop life_group_inn life_group_school` (RENPY_SDK 필요). **작성만 했으며 실행하지 못함**. 학교 개인3클릭/그룹순차대화/취소/엔진저장로드/상태 동일성 캡처 포함. 활성화 전 desktop 및 mobile 화면과 alpha투명빈공간·손/도구 클릭을 추가 검수한다.

## 원본 출처

부모 제공 `art/dialogue-gaze-20261017` 커밋 `e993c8854dc99ac99a2948ae13198c90bbab733b`의 `art/incoming/children-play-three-20261018/children-play-three-sources.zip`만 읽었다. 브랜치 전체 병합 없음.
ZIP SHA256 `f1d4a34db58501221c4bb1ccf423e16649ee1e209b85d5a4a878e0a9c5b23d9c` 일치.
원본3장은 `art/resident-life-groups-20261018/originals/`, 원본 메타데이터는 같은 폴더 `source-manifest.json`. 원본1024x1536, 공통 `dev/import_art.py` WebP quality95/무손실 alpha. crop은 제공 alpha>128 visible bbox이며 실제 픽셀을 재그리거나 알파를 임의로 삭제하지 않았다. 각 발접점과 head box는 원본을 직접 보고 넣은 후보이며 엔진 검수 후 보정한다.

## 차단 및 미검증

1. **차단/실패 확정**: `RENPY_SDK_HOME=/tmp/group-renpy dev/setup_sdk.sh` → `https://www.renpy.org/dl/8.5.3/renpy-8.5.3-sdk.tar.bz2` 요청에서 `curl: (56) CONNECT tunnel failed, response 403`. 재시도·미러·우회 없음. 따라서 Ren'Py lint, 실제 게임 실행, 실제 전후캡처, 브라우저/모바일, 엔진 save/load는 미검증.
2. Library의 원본 ZIP `libfile_442a7f842ff08191907bc3266e58d1c1` 공식 materialization은 서명URL 발급까지만 성공, 실제 GET은 `Tunnel connection failed: 403 Forbidden`. 파일 전달 실패 확정. 이후 부모가 별도로 전달한 **GitHub에 이미 업로드된 커밋/경로**를 새 근거로 읽어 원화 입수를 완료했다. 서명URL이나 토큰은 저장소에 저장하지 않았다.
3. G1/G2 보완원화는 아직 전달되지 않았다. G3 원화 연결까지 완료했지만 실게임 검수 전 활성화하지 않았다.

최종 host 검증: 전체 `python3 -m unittest discover -s dev -p 'test_*.py'` **402개 / 55.840초 / OK** (`all-tests.txt`). 그룹 전용 **12개 통과** (`focused-tests.txt`). override 지도 검사3개와 `git diff --check` 통과. 전체 테스트 뒤 변경은 QA fixture·인계문서뿐이며, 실제 엔진 실행 여부와 혼동하지 않는다.
