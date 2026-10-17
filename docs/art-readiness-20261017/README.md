# 캐릭터별 제작·연결 현황 — 0.19.7 읽기 전용 감사

게임 변경/배포 없음. 기준 main `b772a2a0016279d0e9146b97dd5d6513a82bc6ed`. 표정 최소4개는 **neutral 자체와 그 복제/fallback을 모두 제외**하여 보수적으로 계산합니다. 조사 동작 수를 대화 표정 수에 합산하지 않습니다. 서로 다른 파일도 얼굴/체형/옷의 현재 승인 일치 및 실제 화면 검수가 끝나야 완료입니다.

## 현재 수치

- CAST·대화·조사 모두 63명: 확정48 + 에피소드12 + 기존 추가3(보둠·마을어른·작업장 어른). 아빠도 누락하지 않고 목록에 넣되 플레이어 시점 원칙상 화면에 새로 그리지 않습니다.
- 조사 avatar를 제외한 대화표정·대화몸동작·조사동작 718개 경로가 모두 존재합니다. 보이는 crop의 픽셀, neutral fallback, 미제작 표시를 대조하여 중복을 수량에서 제외했습니다.
- **25명은 서로 다른 비중립 표정 파일 4개 이상**, **38명은 4개 미만**, 이 중 **24명은 0개**입니다. 이는 파일 자격 집계이며 25명 전부 최종 시각 승인 완료라는 뜻이 아닙니다.
- 표정키만 4개로 세면 잠정 차이는125개입니다. 별도 대화 몸동작까지 합쳐 4개 이상인 인물은 26명이며, 이 몸동작과 후보 재활용 여부에 따라 실제 제작 수는 줄어듭니다. 125를 확정 제작량으로 해석하지 않습니다. **기존 후보38개를 아직 전달받지 못했으므로 신규 제작125개를 요청하거나 생성하지 마세요.** 후보의 중복·승인 상태를 먼저 대조해야 합니다. 캐릭터38명과 후보38개는 별개입니다.
- 돌목은 수정된 중립 이외의 표정5개·조사9동작을 완성 수량에서 제외. 누비 큰아이 hold_skirt는 수정본 실패/기존 유지 상태라 완료로 세지 않았습니다.

## 캐릭터별 대화 / 조사 분리

`표정`은 neutral 제외 서로 다른 파일 수, `몸`은 별도 대화 자세 파일 수입니다. `부족`은 표정4 기준입니다. 각 파일의 정확한 경로·SHA·crop·원본 해시 일치 경로는 [channels.json](channels.json), 승인 기준/직업/활동/주간 장소는 [characters.json](characters.json), 표 계산용은 [CSV](characters.csv)입니다.

|인물|ID|표정|몸|부족|조사 동작 키|
|---|---|---:|---:|---:|---|
|밤이|bami|6|0|0|action_1, action_2|
|보둠|bodum|5|0|0|activity|
|부리|buri|5|0|0|action_1, action_2, event_toolbox|
|아빠|dad|5|0|0|action_1, action_2, listen_right, protect|
|다람|daram|5|0|0|action_1, action_2, inspect_floor|
|도토|doto|0|0|4|없음|
|별지기 장로|elder|5|0|0|activity|
|할머니|granny|4|1|0|living_keyledger, withdraw_hand|
|돌목|guard|0|0|4|action_1, action_2, check_records_low, listen_left|
|까로|karo|5|0|0|action_1, action_2, living_axlewrap|
|엄마|mom|5|1|0|action_1, action_2, show_fragments|
|나비|nabi|5|0|0|action_1, action_2|
|너울|neoul|0|0|4|없음|
|바둑이|resident_badook|5|1|0|living_bootlace, block_cart|
|보리|resident_bori|0|0|4|living_firewood|
|은호 사장|resident_eunho|5|0|0|living_prices|
|구슬|resident_guseul|0|0|4|없음|
|꽥순|resident_kkwak|0|0|4|없음|
|콩이|resident_kongi|5|0|0|activity|
|초롱|resident_lamplighter|2|0|2|living_inspectlamp|
|사서 선생님|resident_librarian|0|0|4|event_ledgertie, living_bookpaper|
|백 부인|resident_madam|0|0|4|없음|
|모모 관장|resident_momo|0|0|4|living_lampnumber|
|뭉치|resident_mungchi|0|0|4|없음|
|무쇠 할아버지|resident_musoe|5|0|0|living_foldmap|
|네로|resident_nero|5|0|0|activity|
|누비 아주머니|resident_nubi|0|0|4|없음|
|부엉이 할아버지|resident_owlgp|2|0|2|living_notebook|
|피코|resident_piko|0|0|4|없음|
|뿔이 촌장|resident_ppul|5|1|0|activity, kneel_stone|
|설이|resident_seol|0|0|4|living_bellrope|
|서리 검사원|resident_seori|5|0|0|living_notes|
|실룩|resident_siluk|0|0|4|event_whisper|
|슬링|resident_sling|5|0|0|activity, event_steam|
|솜이|resident_somi|5|0|0|living_bootice|
|사자 선생님|resident_teacher|0|0|4|없음|
|톡|resident_tok|5|0|0|activity|
|토리|resident_tori|5|0|0|activity, world_bench_left|
|따닥|resident_ttadak|5|0|0|living_repair, living_doorframe|
|우박|resident_ubak|5|0|0|living_measure|
|여니|resident_yeoni|0|0|4|living_mend|
|세련|seryeon|5|0|0|action_1, action_2, chair_read, chair_listen|
|공방 주인|workshop|5|0|0|activity|
|꼬미|kid_kkomi|2|2|2|door_peek, hideout_proud|
|깜이|kid_kkam|2|0|2|없음|
|몽이|kid_mong|2|0|2|없음|
|방울|kid_bang|2|1|2|cling_leg|
|누비의 큰아이|kid_nubi1|2|0|2|hold_skirt|
|누비의 둘째|kid_nubi2|2|0|2|없음|
|실룩의 큰아이|kid_siluk1|2|0|2|없음|
|실룩의 작은아이|kid_siluk2|2|0|2|없음|
|새미|kid_saemi|2|1|2|hide_bowl|
|도담|kid_dodam|2|1|2|lick_ladle|
|판돌 영감|npc_pandol|2|1|2|point_name|
|초롱 어머니|chorong_mother|1|1|3|offer_lantern|
|토실|resident_tosil|0|1|4|living_thermos, hold_storybook|
|솔방울|resident_solbang|0|0|4|없음|
|굴돌 할아버지|resident_guldol|0|0|4|없음|
|물결|resident_mulgyeol|0|0|4|없음|
|달그락|resident_dalgeurak|0|0|4|없음|
|종종이|resident_jongjong|0|0|4|없음|
|현이|resident_hyeoni|0|0|4|없음|
|칼바람|resident_kalbaram|0|0|4|없음|

## 장소별 연결과 제작 대기

[place-actions.json](place-actions.json)은 layout의 직접 연결/대기 키와 정확한 런타임 경로, 기존 원본 후보 및 이야기 근거입니다. [story-references.json](story-references.json)은 인물별 실제 코드 줄로, 사건 전용 등장/동작도 빠뜨리지 않기 위한 근거 목록입니다.
[runtime-summary.json](runtime-summary.json)은 실제 엔진의 CAST 63명·레지스트리 JSON 일치와 기본 상태의 1~14일/3시간대 관측을 담습니다. `r13_living_pose` 기본 선택 관측이며 최종 `r13_stage_people`의 사건·가구·원근 덮어쓰기까지 전수 화면 검수한 결과가 아닙니다. 사건 깃발에 따라 등장하는 아이·보호자에게 기본 주간 일정을 새로 부여하지 않습니다.

우선 복구해야 할 기존 대기 연결: 구슬 여관/우편소 `living_stamp`, 백부인 여관 `living_inspect`, 도토 회관 오전·오후 `action_1`/저녁 `action_2`. 도토의 광장 뒷모습 등 준비된 별도 동작은 보존합니다. 사자 선생님의 도포 디자인 `wipe_board/write_attendance/collapse_attendance`도 이전 조끼 그림을 다시 붙이지 않고 제작/승인 대기입니다. 토실 겨울 모자/목도리 행동은 의도된 승인 변형이므로 보존합니다.

## 제작 담당에게 넘길 순서

1. **후보38개 원본 + 캐릭터ID/표정·동작키/승인 여부/버전/원본경로 manifest**를 수령하여 [channels.json](channels.json)과 해시·그림을 대조. 이미 승인·연결된 것을 새로 만들지 않음.
2. 꽥순 승인 refined 원본을 기준으로 비중립4개(joy/angry/anxious/surprise 우선)를 후보에서 확보. 돌목은 승인 입만 기존 표정5/행동9에 일관되게 반영하는 수정 작업으로 분리.
3. 구슬·백부인·도토·사자 선생님 위 장소 동작의 승인 디자인본 우선. 정해진 스토리·직업과 실제 작업 소품이 맞는 원본만 연결.
4. 표정0개 인물→1~3개 인물 순으로 부족분 확보. 어린 인물은 어른 직업 동작을 만들지 말고 실제 사건의 문틈/그릇/소매잡기 등 기존 대본 연출과 매칭.
5. 제작됨 → 승인됨 → 키 연결됨 → 대화/현장 실제 캡처 검수됨을 각각 기록. 현재 보고서는 이 네 단계를 한 가지 완료 상태로 합치지 않음.

[production-requests.json](production-requests.json)에 인물마다 정확한 현재 기본형/원본 경로, 필요한 키, 장소별 직업·활동 문구와 기존 동작을 모았습니다. 원본 해시를 찾지 못한11명은 현재 런타임 파일과 디자인 참조를 분리 표시했으며 정확한 원본 출처 확인 전 원화 재작업을 확정하지 않습니다.

## 꽥순 기준 선명도: 원본과 렌더를 분리

- 전체45명은 3px 중간 축소 경로, 9명은 3px/2px-cell 직접 경로 혼합, 8명은 mapped-cell 직접 경로, 꽥순1명만 native_detail 전용입니다. 이 경로 수는 원화 스타일 동일성을 뜻하지 않습니다.
- 꽥순: 원본1019×1544를 lossless 런타임으로 보존하고 대화3px/조사2px 중간 축소를 opt-in 생략.
- 까로 neutral·다람 neutral·돌목 neutral: 이미 `map+cell` 직접 렌더 경로. 동일화 시험에서 배우 영역 픽셀이 그대로였습니다. 원화의 작은 얼굴·조밀한 세부와 SD 색면 차이를 필터로 같게 만들지 않습니다.
- 까로 flustered·칼바람 neutral: 원본/체형/위치를 바꾸지 않고 중간3px 축소만 생략한 시험에서 눈·옷 경계의 정보 손실이 줄어듭니다. 게임 적용은 아직 하지 않았습니다.
- 조사 화면은 별도의2px 경로이고, 꽥순 외는 현재 기본 경로입니다. 조사 크기는 가구·원근·stature_ratio·발/손 접점을 유지해야 하므로 대화 결과만으로 일괄 배포하지 않습니다.
- 이미 반 크기로 수입한 이미지에서 잃은 디테일은 렌더 플래그로 복구되지 않습니다. 원본 해시 일치 경로를 먼저 확보하고 source→import→runtime을 따로 비교해야 합니다.

대표 비교는 [render-comparison.png](render-comparison.png). 실제 엔진의 같은 장면·배우 좌표·스케일, 메모리 옵션만 전환했습니다. 대화 중립과 flustered를 구분하며 돌목을 정면 새 그림으로 만들지 않았습니다. 꽥순·까로 neutral·다람·돌목은 현재 직접 경로여서 비교상 그대로인 것이 정상입니다. 원본 그림 편집 없음.

## 미완료 / 다음 연결 조건

후보38개 manifest와 실제 파일은 이 작업환경에서 확인하지 못했습니다. 정확히 필요한 전달물은 위1번 목록입니다. 모든 캐릭터의 최종 디자인 시각 승인, 모든 사건/일정/장소 화면검수, 신규 표정·동작 제작, main 배포는 미완료입니다. 이번 결과는 제작·재사용 순서를 정하는 감사 자료와 비파괴 렌더 비교이며 선택지 레이아웃은 적용하지 않았습니다. 최신 사용자 지시에 따라 이후 준비된 아트 묶음은 배역·투명도·잘림·경로·실제 출력 검수 후 별도 승인 대기를 반복하지 않고 main에 통합합니다. 선택지 A/B/C는 이 권한에 포함되지 않습니다.
원본 결과 경로 `/workspace/art-readiness/`, 문서·이미지 `/workspace/daaegame/docs/art-readiness-20261017/`.
