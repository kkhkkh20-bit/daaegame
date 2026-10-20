# 배포 준비 및 차단 — 2026-10-20

사용자 최신 승인으로 원격 push/배포 허용. 단, 이전 실행 포함 총 $1 상한과 실패 검사 무시 배포 금지는 유지된다.

- 통합 기준 main: `5783d7f2a9588e88eeab3f56ab57fb0e7c7ea47a` (0.19.82).
- 원본 구현 `49eec056`을 `2b8f2495`로 cherry-pick. 충돌 2곳은 최신 main의 하단 지도 위치와 안내 영역을 유지하고 이동 잠금/화살표 안내만 결합했다.
- 승인된 타이틀 `bd51fddb`를 `8a66c374`로 cherry-pick. title WebP 하나만 변경되었고 원본 승인 커밋과 Git blob이 동일하다. 다른 Codex의 마차 연출은 보존했다. 다람 10종 미전달 파일은 변경하지 않았다.
- Python 전체 검사 778개 통과(41.899초). git diff --check 통과.
- 0.19.82 로컬 웹 런타임에 통합 소스를 오버레이한 실제 렌더러 검사 재통과: 입구 왕복/시장 이동/입력 잠금/모바일 터치/움직임 끄기/복원 콜백/87개 클릭 판정 개선. 새 빌드 및 실제 저장 파일 재시작/로드 검사가 아니다.

## 배포 미실행 및 정확한 차단

1. `GET /users/kkhkkh20-bit/settings/billing/usage`: HTTP 403 `Resource not accessible by integration`. 계정 전체 사용액/남은 $1 한도 확인 불가. 우회하지 않았다.
2. 저장소는 public이고 워크플로는 표준 ubuntu 러너다. GitHub 공식 문서상 표준 공개 러너 실행은 무료지만 artifact 저장공간은 별도 초과 과금 가능성이 있다. 현재 공식 verify/build에는 artifact 업로드가 있으며 main push에도 Resource dashboard 및 Pages 작업이 연동된다. 따라서 업로드 포함 실행 전체가 무료라고 확정할 수 없어 CI 실행/PR/main push를 하지 않는다. 비용 확인 자료나 잔액 확인 권한이 필요하다. 추가 비용을 임의 승인하지 않았다.
3. SDK 다운로드의 기존 프록시 403이 해소되었다는 증거가 없어 재시도하지 않았다. 새 SDK lint/빌드/native 테스트/실제 저장 파일 회귀는 미실행이다.
4. 실제 공개 URL의 `build-manifest.json` 직접 요청이 이 환경에서 `Tunnel connection failed: 403 Forbidden`으로 실패했다. 공개 버전 확인 성공으로 처리하지 않는다.

현재 공식 배포 경로: main 루트의 GitHub Pages legacy build. 대상 URL은 https://kkhkkh20-bit.github.io/daaegame/preview/room13-dev/ 이다. GitHub API가 보고한 기존 Pages 완료 SHA는 `5783d7f2`; 이번 변경이 게시되었다는 의미가 아니다.

소스만 CI 자동 실행 대상이 아닌 `integrate/two-zone-01982` 브랜치로 전달한다. main 병합/새 배포는 하지 않는다. 원화 25개 장소의 최소 두 화면 공간 확장은 기존 보고서대로 미완료다. Library 저장 실패는 별도 사안이며 재시도하지 않았다.

비용 근거: https://docs.github.com/en/billing/concepts/product-billing/github-actions
