# 두 번째 제작 묶음 — 4인 18장

**제작 요청서이며 생성·적용 완료가 아니다.** 기존 후보는 중복 생성하지 않는다. 원본 수신 차단은 유지하며 정상 첨부 전달을 기다린다. 기준 main `ad722b1`. 경로는 `experiments/renpy-ch1/` 기준. 기계용 상세는 [batch-02.json](batch-02.json).

## 승인된 제작 방향

- 2026-10-17 사용자 승인: 꽥순·사자 선생님 비교 후 “좋다 이런느낌으로 쭉가자”. 선명도·입체감·다양한 상반신 연기를 다음 제작 방향으로 채택.
- 각 승인 원본의 얼굴·종·체형·복장·소품·색 개성 보존. 다른 인물의 그림체를 획일적으로 복제하지 않는다.
- 억지로 굵은 2×2 블록으로 재축소하지 않는다. 원본 상세를 유지하고 최종 게임 표시 품질로 판단한다. 엄격 2×2 격자 인증은 납품 필수조건에서 제외.
- 대화 전신 1장=1표정. 얼굴뿐 아니라 손·어깨·고개로 구별되는 연기. 상반신만 잘라 납품하지 않는다.
- 투명 배경, alpha 경계와 손/귀/소품 여유 보존. 원본 크기·crop·head/foot·손 기준점·파일 SHA 기록. 캔버스/발점 차이를 숨기기 위한 임의 축소 금지.
- 각 키의 연기는 제작 제안이다. 모든 인용 대사가 그 감정 키를 현재 호출한다는 뜻은 아니며 대사·분기·표정 연결은 이번 문서 작업에서 변경하지 않는다.
- 제작 방향 승인과 개별 후보 승인·수신·해시 검증·연결·실제 화면 검수·배포는 별개 상태다. Library 차단을 우회하지 않는다.

## 선정 근거

|인물|장수|Room13 문자열 튜플 등장 수*|현황의 대화 사용 행 수*|주요 장면|
|---|---:|---:|---:|---|
|너울|5|146|19|현장 보존·봉인·발밑 물건 경고, ep1 및 ep3 대결의 주장과 반박.|
|누비 아주머니|5|47|14|ep3 세탁터의 배급 대화, 다친 손에 대한 질문, 장작 창고 화재 추궁·자백.|
|보리|5|55|13|ep3 아이 구출·방화 누명·아이를 맡는 후일담, ep5 아이에 대한 걱정과 회의.|
|초롱|3|70|31|ep4 편지 직접 전달 약속, 황혼의 종탑 길 경고, 밤의 귀환·후일담. 기존 neutral/anxious/flustered는 재제작 제외.|

*정적 코드 집계다. 플레이 횟수나 독립 장면 수가 아니며 조건 분기·재사용·비대사 튜플을 포함할 수 있다. 대화 사용 행은 emotion/pose 지시를 별도 집계한다. `room13*.rpy`의 `(인물 ID, 문자열...)` 패턴을 세며 `qa_tests`와 winter 파일은 제외했다. 인물별 상위 파일·횟수는 JSON에 보존했다. 핵심 사건 역할과 현재 미제작 채널을 함께 고려했다.

실제 호출 경로: `game/room13.rpy:40`의 `r13_lines` → 같은 파일 61행의 `r13_speaker` → `game/room13_rules.rpy:295` 및 326행의 `r13_close_art`. 회의 화면은 별도 분기이므로 회의에 등장한다는 사실만으로 새 대화 전신이 회의에 적용됐다고 보지 않는다.

초롱은 기존 neutral/anxious/flustered가 있으므로 부족한 3표정만 요청한다. 도토 대화 5표정은 후속 후보로 남기되 이번에는 사건 전반과 ep3/ep4 주요 인물에 집중한다. 이미 생성된 도토 2동작과는 별도 요구다.

## 너울 — 5장

승인 원본: `art/canonical48-rev45/originals/neoul.webp` (1023×1499). SHA-256: `31172d4a4f9aec679442105059098fe8679f869df90ece81ca2a0cd3b34300f9`.

장면: 현장 보존·봉인·발밑 물건 경고, ep1 및 ep3 대결의 주장과 반박.

코드 근거: `game/room13_rules.rpy:295`, `game/systems/room13_ep1_lamp_thief.rpy:108`, `game/systems/room13_ep3_woodfire.rpy:79`, `game/systems/room13_ep3_woodfire.rpy:193`.

|키|표정·몸짓 제작 요구|
|---|---|
|joy|입꼬리만 올린 절제된 만족. 어깨를 펴고 한 손을 가슴 가까이 편다.|
|flustered|말이 막혀 시선을 옆으로 피하며 팔꿈치를 몸 쪽으로 당긴다.|
|angry|몸을 약간 앞으로 기울이고 한 손바닥을 세워 제지한다. 검은 집행관 의상으로 바꾸지 않는다.|
|anxious|미간을 모으고 손가락을 모아 몸 앞에 둔다. 어깨 긴장으로 우려를 드러낸다.|
|surprise|눈을 크게 뜨고 상체를 살짝 뒤로 뺀다. 손을 반쯤 들어 발밑 위험을 알린다.|

## 누비 아주머니 — 5장

승인 원본: `art/canonical48-rev45/originals/resident_nubi.webp` (957×1516). SHA-256: `af0df1c2e0f8af56132d027ce8a60eed7f2c4e4599d93d887c2d96740ddfd31b`.

장면: ep3 세탁터의 배급 대화, 다친 손에 대한 질문, 장작 창고 화재 추궁·자백.

코드 근거: `game/systems/room13_ep3_woodfire.rpy:188`, `game/systems/room13_ep3_woodfire.rpy:381`, `game/systems/room13_ep3_woodfire.rpy:432`.

|키|표정·몸짓 제작 요구|
|---|---|
|joy|생활 대화용 작은 미소. 어깨를 풀고 두 손을 느슨하게 겹친다. 사건 자백에 웃음을 강제하지 않는다.|
|flustered|당황해 시선을 피하고 한 손으로 자기 소매를 잡는다. 다른 인물과 접촉하지 않는다.|
|angry|턱을 조금 들고 팔을 몸 앞에 모아 방어적으로 항변한다.|
|anxious|어깨를 움츠리고 손을 가슴 아래에 모은다. 아이들을 걱정하는 시선.|
|surprise|눈과 입이 작게 벌어지고 한 손이 가슴으로 올라간다. 과장된 개그 표정은 피한다.|

## 보리 — 5장

승인 원본: `art/canonical48-rev45/originals/resident_bori.webp` (1210×1300). SHA-256: `1294543146bd66c747901d8b1cb83460650bb049384727254d0012789f17f2e7`.

장면: ep3 아이 구출·방화 누명·아이를 맡는 후일담, ep5 아이에 대한 걱정과 회의.

코드 근거: `game/systems/room13_ep3_woodfire.rpy:256`, `game/systems/room13_ep3_woodfire.rpy:298`, `game/systems/room13_ep3_woodfire.rpy:515`, `game/systems/room13_ep5_soup.rpy:404`.

|키|표정·몸짓 제작 요구|
|---|---|
|joy|구출 이후/생활 대화에 쓸 수 있는 작은 안도. 고개를 조금 숙이고 손바닥을 편다.|
|flustered|머쓱하게 시선을 내리고 한 손을 목 가까이에 둔다. 원본 둥근 얼굴 유지.|
|angry|상체를 앞으로 기울여 항변하고 팔을 약간 벌린다. 근육을 키우거나 얼굴을 각지게 만들지 않는다.|
|anxious|미간을 모으고 손을 서로 감싸 쥔다. 아이의 안부를 걱정하는 긴장.|
|surprise|눈을 크게 뜨고 한쪽 어깨와 손을 들어 뒤로 반응한다. 몸통 크기는 유지한다.|

## 초롱 — 3장

승인 원본: `art/canonical48-rev45/originals/resident_lamplighter.webp` (993×1519). SHA-256: `067e60f202442c2ad56b87febafe612c1b72c1a819dc837f95bcbb477d542759`.

장면: ep4 편지 직접 전달 약속, 황혼의 종탑 길 경고, 밤의 귀환·후일담. 기존 neutral/anxious/flustered는 재제작 제외.

코드 근거: `game/systems/room13_ep4_night13.rpy:167`, `game/systems/room13_ep4_night13.rpy:190`, `game/systems/room13_ep4_night13.rpy:195`, `game/systems/room13_ep4_night13.rpy:273`, `game/systems/room13_ep4_night13.rpy:388`.

|키|표정·몸짓 제작 요구|
|---|---|
|joy|편지를 전하거나 다람이에게 등 켜기를 권할 때의 따뜻한 미소. 손바닥을 열고 상체를 살짝 기울인다.|
|angry|의지를 단호하게 전하는 눈썹과 입. 한 손을 몸 가까이 쥐되 위협적인 무기나 새 도구는 넣지 않는다.|
|surprise|종탑 길 경고에 눈을 크게 뜨고 한 손을 가슴 가까이 든다. 기존 anxious/flustered와 실루엣을 구별한다.|

## 접점 미확정 — 제작 수에서 제외

백 부인 `living_inspect` 요청은 유지한다. 현재 여관 layout의 object 목록에는 desk/door/keys/register/knitting/coats/cups가 있으나 봉인 보관함의 명시적 손끝 anchor는 없다. desk나 waiting slot 좌표로 대신 확정하지 않는다.

확인할 최신 배경: `game/assets/room13-pixel-panorama-inn-{morning,afternoon,evening}.webp`; 배치: `game/assets/room13-world-layout.json`의 `inn`. 실제 카메라·crop을 적용한 화면에서 봉인 면을 먼저 확인하고 손끝 world/screen 좌표, 캐릭터 발·손 기준점, 가림 관계를 기록한 뒤 제작한다. 이번에는 배경의 시각 검수와 접점 확정을 수행하지 않았으며 **미생성 보류**다.

## 납품·검수 및 중복 방지

- `art/incoming/art-coverage-batch-02/<character>/dialogue-<key>.png`에 원본 그대로 납품. 현재 파일이 있다는 뜻이 아니다.
- 꽥순5·사자 선생님7·돌목5·도토2·구슬1 후보는 재생성 제외. 꽥순 승인 neutral 수신 블록도 계속 유지한다.
- 수신 뒤 SHA/alpha/경계 여유/원본 개성/몸짓 구별/기준점 확인 → 개별 후보 검토 → 승인 채널만 연결 → 최종 표시 크기의 실제 게임 화면 검수.
- 원본을 굵은 2×2로 강제 재축소하거나 전역 렌더러를 변경하는 요청이 아니다. 인물별 실제 표시 품질을 보고 처리한다.
- 이 문서 작성으로 게임·보드 연결, 실제 화면 검수 또는 배포 완료 상태를 올리지 않는다.
