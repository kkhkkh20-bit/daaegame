# 아트 충족 현황 — 자동 생성

기준: 0.19.6 / `b50d9fbf3257c21176b7cde900023fd35e4b09f0`. 확정 48명과 추가/기존 보조 런타임 15명을 구분한다. 추가 15명 모두를 신규 제작 대상으로 확정한 것은 아니다.

JSON이 단일 현황 원장이고 CSV는 같은 자료의 보기다. 자산·사용 장면·제작 요청을 포함하므로 전체 행 수는 그림 장수가 아니다. 기존 제작 요청 153건은 최신 연결과 재조정할 항목이며, 옛 상태 문구를 완료 근거로 사용하지 않는다.

실제 화면 검수는 이번 실행에서 전부 미실행이다. 파일 존재, 과거 캡처, 단위 검사로 화면 합격을 대신하지 않는다. 동적 조건과 script_pose_cue는 정적 추출 한계로 별도 확인이 필요하다.

## 범위

|유형|행 수|
|---|---:|
|dialogue_expression|378|
|investigation|586|
|profile|253|
|cast|1312|
|dialogue_pose|16|
|map_time_state|66|
|investigation_usage|73|
|map_prop|1|
|map_event|18|
|map_event_overlay|13|
|dialogue_usage|986|
|navigation_map|2|
|navigation_node|30|
|navigation_reveal|2|
|map_runtime_treatment|3|
|production_request|153|
|script_pose_cue|19|

## 대화 표정

|인물 ID|이름|독립 파일 표정 수*|중립 대체|수정 필요|
|---|---|---:|---|---|
|bami|밤이|6|—|—|
|bodum|보둠|6|—|—|
|buri|부리|6|—|—|
|chorong_mother|초롱 어머니|2|angry,flustered,joy,surprise|—|
|dad|아빠|0|—|—|
|daram|다람|6|—|—|
|doto|도토|1|angry,anxious,flustered,joy,surprise|—|
|elder|별지기 장로|6|—|—|
|granny|할머니|6|—|—|
|guard|돌목|1|—|angry,anxious,flustered,joy,surprise|
|karo|까로|6|—|—|
|kid_bang|방울|3|angry,flustered,surprise|—|
|kid_dodam|도담|3|angry,flustered,surprise|—|
|kid_kkam|깜이|3|angry,flustered,surprise|—|
|kid_kkomi|꼬미|3|angry,flustered,surprise|—|
|kid_mong|몽이|3|angry,flustered,surprise|—|
|kid_nubi1|누비의 큰아이|3|angry,flustered,surprise|—|
|kid_nubi2|누비의 둘째|3|angry,flustered,surprise|—|
|kid_saemi|새미|3|angry,flustered,surprise|—|
|kid_siluk1|실룩의 큰아이|3|angry,flustered,surprise|—|
|kid_siluk2|실룩의 작은아이|3|angry,flustered,surprise|—|
|mom|엄마|6|—|—|
|nabi|나비|6|—|—|
|neoul|너울|1|angry,anxious,flustered,joy,surprise|—|
|npc_pandol|판돌 영감|3|angry,flustered,surprise|—|
|resident_badook|바둑이|6|—|—|
|resident_bori|보리|1|angry,anxious,flustered,joy,surprise|—|
|resident_dalgeurak|달그락|1|angry,anxious,flustered,joy,surprise|—|
|resident_eunho|은호 사장|6|—|—|
|resident_guldol|굴돌|1|angry,anxious,flustered,joy,surprise|—|
|resident_guseul|구슬|1|angry,anxious,flustered,joy,surprise|—|
|resident_hyeoni|현이|1|angry,anxious,flustered,joy,surprise|—|
|resident_jongjong|종종이|1|angry,anxious,flustered,joy,surprise|—|
|resident_kalbaram|칼바람|1|angry,anxious,flustered,joy,surprise|—|
|resident_kkwak|꽥순|1|angry,anxious,flustered,joy,surprise|—|
|resident_kongi|콩이|6|—|—|
|resident_lamplighter|초롱|3|angry,joy,surprise|—|
|resident_librarian|사서 선생님|1|angry,anxious,flustered,joy,surprise|—|
|resident_madam|백 부인|1|angry,anxious,flustered,joy,surprise|—|
|resident_momo|모모 관장|1|angry,anxious,flustered,joy,surprise|—|
|resident_mulgyeol|물결|1|angry,anxious,flustered,joy,surprise|—|
|resident_mungchi|뭉치|1|angry,anxious,flustered,joy,surprise|—|
|resident_musoe|무쇠 할아버지|6|—|—|
|resident_nero|네로|6|—|—|
|resident_nubi|누비 아주머니|1|angry,anxious,flustered,joy,surprise|—|
|resident_owlgp|부엉이 할아버지|6|—|—|
|resident_piko|피코|1|angry,anxious,flustered,joy,surprise|—|
|resident_ppul|뿔이 촌장|6|—|—|
|resident_seol|설이|1|angry,anxious,flustered,joy,surprise|—|
|resident_seori|서리 검사원|6|—|—|
|resident_siluk|실룩|1|angry,anxious,flustered,joy,surprise|—|
|resident_sling|슬링|6|—|—|
|resident_solbang|솔방울|1|angry,anxious,flustered,joy,surprise|—|
|resident_somi|솜이|6|—|—|
|resident_teacher|사자 선생님|1|angry,anxious,flustered,joy,surprise|—|
|resident_tok|톡|6|—|—|
|resident_tori|토리|6|—|—|
|resident_tosil|토실|1|angry,anxious,flustered,joy,surprise|—|
|resident_ttadak|따닥|6|—|—|
|resident_ubak|우박|6|—|—|
|resident_yeoni|여니|1|angry,anxious,flustered,joy,surprise|—|
|seryeon|세련|6|—|—|
|workshop|공방 주인|6|—|—|

*파일과 중립 중복 여부 기준이며 디자인 승인/화면 합격 수가 아니다. 아빠는 1인칭 시점이라 화면 제작 대상에서 제외한다. 기본 6키 밖의 동작은 별도 행으로 관리한다.

## 장소·시간대

|장소|상태|시간|연결|파일|
|---|---|---|---|---|
|altar|normal|afternoon|linked|assets/room13-pixel-ready-altar0177-afternoon.webp|
|altar|normal|evening|linked|assets/room13-pixel-ready-altar0177-evening.webp|
|altar|normal|morning|linked|assets/room13-pixel-ready-altar0177-morning.webp|
|ancient|normal|afternoon|linked|assets/room13-pixel-wide-ancient-day.webp|
|ancient|normal|evening|linked|assets/room13-pixel-wide-ancient-day.webp|
|ancient|normal|morning|linked|assets/room13-pixel-wide-ancient-day.webp|
|clinic|normal|afternoon|linked|assets/room13-pixel-ready-clinic0177-afternoon.webp|
|clinic|normal|evening|linked|assets/room13-pixel-ready-clinic0177-evening.webp|
|clinic|normal|morning|linked|assets/room13-pixel-ready-clinic0177-morning.webp|
|dining|normal|afternoon|linked|assets/room13-pixel-wide-dining-afternoon.webp|
|dining|normal|evening|linked|assets/room13-pixel-wide-dining-evening.webp|
|dining|normal|morning|linked|assets/room13-pixel-wide-dining-morning.webp|
|facility|normal|afternoon|linked|assets/room13-pixel-ready-facility0177-afternoon.webp|
|facility|normal|evening|linked|assets/room13-pixel-ready-facility0177-evening.webp|
|facility|normal|morning|linked|assets/room13-pixel-ready-facility0177-morning.webp|
|forest|normal|afternoon|linked|assets/room13-pixel-wide-forest-afternoon.webp|
|forest|normal|evening|linked|assets/room13-pixel-wide-forest-evening.webp|
|forest|normal|morning|linked|assets/room13-pixel-wide-forest-morning.webp|
|gate|normal|afternoon|linked|assets/room13-pixel-ready-gate0173-afternoon.webp|
|gate|normal|evening|linked|assets/room13-pixel-ready-gate0173-evening.webp|
|gate|normal|morning|linked|assets/room13-pixel-ready-gate0173-morning.webp|
|greenhouse|normal|afternoon|linked|assets/room13-pixel-ready-greenhouse0177-afternoon.webp|
|greenhouse|normal|evening|linked|assets/room13-pixel-ready-greenhouse0177-evening.webp|
|greenhouse|normal|morning|linked|assets/room13-pixel-ready-greenhouse0177-morning.webp|
|hall|after|afternoon|linked|assets/room13-pixel-wide-hall-after-afternoon.webp|
|hall|after|evening|linked|assets/room13-pixel-wide-hall-after-evening.webp|
|hall|after|morning|linked|assets/room13-pixel-wide-hall-after-morning.webp|
|hall|before|afternoon|linked|assets/room13-pixel-wide-hall-before-afternoon.webp|
|hall|before|evening|linked|assets/room13-pixel-wide-hall-before-evening.webp|
|hall|before|morning|linked|assets/room13-pixel-wide-hall-before-morning.webp|
|inn|normal|afternoon|linked|assets/room13-pixel-panorama-inn-afternoon.webp|
|inn|normal|evening|linked|assets/room13-pixel-panorama-inn-evening.webp|
|inn|normal|morning|linked|assets/room13-pixel-panorama-inn-morning.webp|
|kitchen|normal|afternoon|linked|assets/room13-pixel-wide-kitchen-afternoon.webp|
|kitchen|normal|evening|linked|assets/room13-pixel-wide-kitchen-evening.webp|
|kitchen|normal|morning|linked|assets/room13-pixel-wide-kitchen-morning.webp|
|market|normal|afternoon|linked|assets/room13-pixel-wide-market-afternoon.webp|
|market|normal|evening|linked|assets/room13-pixel-wide-market-evening.webp|
|market|normal|morning|linked|assets/room13-pixel-wide-market-morning.webp|
|passage|normal|afternoon|linked|assets/room13-pixel-wide-passage-afternoon.webp|
|passage|normal|evening|linked|assets/room13-pixel-wide-passage-evening.webp|
|passage|normal|morning|linked|assets/room13-pixel-wide-passage-morning.webp|
|post|normal|afternoon|legacy_atlas|assets/room13-pixel-village-afternoon.webp|
|post|normal|evening|legacy_atlas|assets/room13-pixel-village-evening.webp|
|post|normal|morning|linked|assets/room13-pixel-wide-post-morning.webp|
|river|normal|afternoon|linked|assets/room13-pixel-wide-river-afternoon.webp|
|river|normal|evening|linked|assets/room13-pixel-wide-river-evening.webp|
|river|normal|morning|linked|assets/room13-pixel-wide-river-morning.webp|
|room13|after|afternoon|linked|assets/room13-pixel-wide-room13-after-afternoon.webp|
|room13|after|evening|linked|assets/room13-pixel-wide-room13-after-evening.webp|
|room13|after|morning|linked|assets/room13-pixel-wide-room13-after-morning.webp|
|room13|before|afternoon|linked|assets/room13-pixel-wide-room13-before-afternoon.webp|
|room13|before|evening|linked|assets/room13-pixel-wide-room13-before-evening.webp|
|room13|before|morning|linked|assets/room13-pixel-wide-room13-before-morning.webp|
|school|normal|afternoon|linked|assets/room13-pixel-panorama-school-afternoon.webp|
|school|normal|evening|linked|assets/room13-pixel-panorama-school-evening.webp|
|school|normal|morning|linked|assets/room13-pixel-panorama-school-morning.webp|
|square|normal|afternoon|linked|assets/room13-pixel-panorama-square-afternoon.webp|
|square|normal|evening|linked|assets/room13-pixel-panorama-square-evening.webp|
|square|normal|morning|linked|assets/room13-pixel-panorama-square-morning.webp|
|store|normal|afternoon|linked|assets/room13-pixel-ready-store0177-afternoon.webp|
|store|normal|evening|linked|assets/room13-pixel-ready-store0177-evening.webp|
|store|normal|morning|linked|assets/room13-pixel-ready-store0177-morning.webp|
|workshop|normal|afternoon|linked|assets/room13-pixel-panorama-workshop-afternoon.webp|
|workshop|normal|evening|linked|assets/room13-pixel-panorama-workshop-evening.webp|
|workshop|normal|morning|linked|assets/room13-pixel-panorama-workshop-morning.webp|

## 다음 처리

1. `BATCH_01.md` / `BATCH_02.md`의 후보 보고와 `NEXT_QUEUE.md`를 따라 수신·개별 승인·통합을 우선한다. 이미 생성된 후보를 중복 발주하지 않으며 승인 전 현재 연결을 유지한다.
2. 기존 요청과 코드 조건 재조정: 특히 조사 생활 동작, 겨울 야외 옷, 눈 깜빡임, 추가 인물 제한 표정.
3. 새 승인 그림 수령 후 경로·해시·2×2 셀·몸 비율·접점 검사 → 해당 장면 화면 검수 → 연결 상태와 리뷰 기록 갱신.
4. 맵 66 시간/사건 조합과 18 이벤트 배경, 13 겹침 효과는 그림 추가가 필요한지 실제 조건별 화면을 보고 결정. 시간대 재사용/기존 atlas를 곧바로 누락으로 판단하지 않는다.
5. 전체 6표정이 중립인 23명 외에도 초롱/추가 아이들 등 일부 표정 fallback이 있다. 제한 표정 세트가 의도된 경우 장면 필요도를 확인한 뒤 제작 여부 결정.
