# 꽥순 승인 neutral 통합 — 0.19.6

공식 업로드 커밋 `bc42450b5d3d3ed6191df2747abdb17e3c9de66e`에서 원본을 수신했다. SHA-256 `dced0d974c10cc81fe0f72fdcbb884067ee54e3511e2cbf4f43d3f0b1674f2a9`, 989502 bytes, RGBA 1019×1544. Library 다운로드 경로는 여전히 차단됐지만 승인된 GitHub 업로드 경로로 정상 수신했다. 사용자 공개 배포 승인: 2026-10-17 07:06 UTC.

## 변경

- 원본: `art/incoming/kkwak-refined-20261017/kwaeksun-refined-candidate-v1.png`. 원본 크기 그대로 lossless WebP import. 알파 및 보이는 RGBA 픽셀의 완전 일치를 검사했다.
- 꽥순 기본 전신·조사 서기·프로필·avatar를 새 승인 neutral로 연결. 5표정 후보는 미승인이라 새 neutral fallback 유지.
- 꽥순만 `native_detail`로 대화/현장 렌더의 중간 격자 축소 생략. 전체 캐릭터 규칙은 변경하지 않았다. 임의 0.5 import 및 2×2 선언 없음.
- crop `[123,13,802,1519]`, figure `[127,17,794,1511]`. alpha≥32와 기존 4px margin 규칙으로 산출했다. 원본의 매우 낮은 alpha 잔여는 원본 파일에 보존한다.
- 대화 높이840에서 scale0.583719, 표시468×887, 중심x652/y119. 이전 x652/y120과 거의 같은 위치·키를 유지한다. 기존 중심 오프셋 -10은 원본 좌표 크기에 맞춰 -20으로 변환.
- JSON 항목 비교에서 변경 인물은 꽥순뿐. 지도·다른 캐릭터·회의 전용 데이터·시나리오 변경 없음. 기존 after_load 캐시 정리 유지. 버전 0.19.6.

## 검수

`dev/check.sh` 단위 검사·Ren’Py lint 통과. 공식 build_web 빌드 통과. 승인 원본 SHA, 무축소·무손실 RGBA, 미승인 표정 fallback, 꽥순만 렌더 opt-in, 다른 인물 JSON 동일성을 확인했다.

실제 Ren’Py 0.19.6 웹 엔진 + Chromium, 1280×720/DPR1에서 동일 입구 오후 배경으로 비교했다. [이전](../../reports/kkwak-refined-20261017/before.png), [새 원본+기존 격자](../../reports/kkwak-refined-20261017/approved_with_grid.png), [승인 원본+직접 표시](../../reports/kkwak-refined-20261017/approved.png), [현장 서기](../../reports/kkwak-refined-20261017/field.png). 실행 기록은 같은 폴더 `execution.json`, 재현 코드는 `render.py`다. 4개 화면 모두 실제 렌더되었고 예외 화면 없음. 직접 표시는 눈·부리·주름의 세부가 중간 격자보다 잘 유지된다.

## 검수 한계와 잔여

실제 엔진의 r13_close_art/r13_staged_art를 호출한 통제된 검수 화면이며, 전체 스토리 플레이나 모든 실제 배치·모바일·저장 복구 회귀 검수가 아니다. 현장 화면은 고정137×260의 서기 표본으로 자연 일정 출현/가림 배치를 검증하지 않는다. profile/avatar는 연결·geometry를 정적으로 확인했으며 별도 UI 캡처는 하지 않았다. 원본 경계의 낮은 alpha를 임의 수정하지 않았다. 미승인 5표정과 다른 후보들의 수신/승인은 계속 대기한다.

공개 서비스 배포 결과는 작업 완료 보고의 GitHub Pages 배포 커밋·빌드 상태를 기준으로 확인한다.
