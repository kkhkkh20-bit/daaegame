# 남은 작업 큐 — 2026-10-17

원장: 현재 런타임은 `coverage.json/csv`, 후보 제작·승인·수신은 `batch-01.json`/`batch-02.json`. 미수신 후보를 새 제작 누락으로 다시 발주하지 않는다. 이번 갱신에서 이미 생성 보고된 후보는 BATCH_01 15장 + 꽥순5표정 + BATCH_02 18장 = **38장**이며 승인된 꽥순 neutral은 별도다. 백 부인 1장은 미생성 보류다.

## 처리 순서

1. **수신 차단 해소**: 정상 첨부/지원된 전달 경로로 후보 원본을 받는다. 승인 꽥순 neutral은 GitHub 업로드로 수신·해시 검증 완료했으며 [통합 기록](KKWAK_INTEGRATION.md)에서 추적한다. 차단 우회 금지. 수신 파일별 SHA·Library ID·크기·alpha·발점 기록. 실패 시 blocked 유지.
2. **후보별 승인·보완 정리**: BATCH_01 및 BATCH_02의 보고된 alpha/여백/캔버스/몸짓/감정 부호 문제를 검토한다. 제작 방향 승인과 개별 후보 승인을 구분한다. 수정 대상만 재작업하며 38장을 통째로 재생성하지 않는다.
3. **승인 파일 통합**: 승인된 꽥순 neutral부터 한 인물씩 연결하고, 원본 개성·표정 fallback·회의 전용 그림·캐시·최종 표시 크기를 확인한다. 경로/해시/구문 및 해당 장면 화면 검수 후 배포한다. 굵은 2×2 강제 재축소 금지. 개별 승인 없는 후보는 연결하지 않는다.
4. **다음 표정 큐**: 아래 미제작 목록에서 도토5 → 사서5 → 여니5 → 백 부인5 순으로 작은 묶음을 요청한다. 이들은 기존 도토2 조사동작 및 백 부인 보관함 동작과 다른 채널이다. 이후 나머지는 실제 호출/등장 비중에 따라 순차 선정. 제한 표정인 아이들·초롱 어머니·판돌은 장면 필요 여부를 먼저 확인한다. 아직 새 후보 생성 승인이 완료됐다는 뜻은 아니다.
5. **조사 동작 큐**: 백 부인 보관함은 장소/물체 기획 결정부터. 돌목 조사9자세의 입 수정은 기존 행동을 유지하며 한 동작씩 보완. 사자 선생님 wipe_board는 현재 호출 없는 P1로 유지. 나머지 역사 요청은 현재 연결과 대조해 중복 제거한 뒤 장소별로 발/손/좌면/가림을 확정한다. 승인 겨울 행동은 보존한다.
6. **장소·맵 큐**: 여관/창고의 백 부인 접점 → 복도의 도토 쓰기·독서 → 구슬 여관/우체국 도장 동작 순으로 실제 배치를 확인한다. 이후 원장의 시간/사건 배경·겹침·지도 연결을 검토한다. 시간대 재사용이나 기존 atlas를 누락으로 단정해 새 맵을 대량 제작하지 않는다.

## 보고된 후보를 제외한 대화 표정 잔여

현재 정적 원장 기준이며 개별 필요성 확정 전 목록이다. 생성된 후보가 미수신인 경우 이 표에서 제외한다.

|인물 ID|남은 키|
|---|---|
|chorong_mother|angry, flustered, joy, surprise|
|doto|angry, anxious, flustered, joy, surprise|
|kid_bang|angry, flustered, surprise|
|kid_dodam|angry, flustered, surprise|
|kid_kkam|angry, flustered, surprise|
|kid_kkomi|angry, flustered, surprise|
|kid_mong|angry, flustered, surprise|
|kid_nubi1|angry, flustered, surprise|
|kid_nubi2|angry, flustered, surprise|
|kid_saemi|angry, flustered, surprise|
|kid_siluk1|angry, flustered, surprise|
|kid_siluk2|angry, flustered, surprise|
|npc_pandol|angry, flustered, surprise|
|resident_dalgeurak|angry, anxious, flustered, joy, surprise|
|resident_guldol|angry, anxious, flustered, joy, surprise|
|resident_guseul|angry, anxious, flustered, joy, surprise|
|resident_hyeoni|angry, anxious, flustered, joy, surprise|
|resident_jongjong|angry, anxious, flustered, joy, surprise|
|resident_kalbaram|angry, anxious, flustered, joy, surprise|
|resident_librarian|angry, anxious, flustered, joy, surprise|
|resident_madam|angry, anxious, flustered, joy, surprise|
|resident_momo|angry, anxious, flustered, joy, surprise|
|resident_mulgyeol|angry, anxious, flustered, joy, surprise|
|resident_mungchi|angry, anxious, flustered, joy, surprise|
|resident_piko|angry, anxious, flustered, joy, surprise|
|resident_seol|angry, anxious, flustered, joy, surprise|
|resident_siluk|angry, anxious, flustered, joy, surprise|
|resident_solbang|angry, anxious, flustered, joy, surprise|
|resident_tosil|angry, anxious, flustered, joy, surprise|
|resident_yeoni|angry, anxious, flustered, joy, surprise|

## 중단 조건

수신·승인·접점 중 하나가 없으면 해당 연결/제작을 보류한다. 독립적인 문서·코드 읽기 검토는 계속할 수 있다. `reviews.json`에는 실제 게임 검수 증거만 기록한다.
