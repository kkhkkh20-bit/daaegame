# 실룩 선금: 시간 경계와 재접촉 수정안

## 결과와 적용 상태

.19.64 `a3350f2618b33ca1aab57504c8e8227174153b0e`를 기준으로 로컬 후보 소스, 정확한 diff, fullcontent bundle, 회귀 테스트를 준비했다. 원격 쓰기와 게임 실행은 하지 않았다. 최초 작성 시 테스트 미실행이었고, 이후 부모가 허용한 pure unittest만 실행해 16/16 통과했다. .65에는 적용하지 않는다. 아래 메타데이터 갱신과 CI 검증을 완료하기 전에는 배포 가능한 검증 완료본으로 취급하지 않는다.

- 지급 직후에는 떠나는 현재 장면만 보여 준다. 일반 선금의 “해 지기 전”과 전액·추적 분기의 “오늘 안에”를 서로 다른 원래 기한으로 저장한다.
- 기한 전에는 진척 질문, 기한 후에는 해명·환불 요구·원래 심부름 이행 요구를 플레이어가 고른다. 재접촉에서 이미 지급한 사실을 기억한다.
- 환불 요구는 실제 환불이 아니다. 새 돈을 지급하거나 짐을 받았다고 처리하지 않으며, 요구만으로 해결 상태로 바꾸지 않는다.
- 다음 날 콩이의 “어제”는 실제 다음 날이면서 콩이가 현재 장소에 있을 때만 말한다. 그보다 늦게 만나면 “선금을 주신 날”로 바뀐다.
- 옛 장부가 일반 5냥과 추적 5냥을 구분하지 못하면 기한을 추정하지 않는다. 같은 선금의 재지급도 막는다.

## 기준 소스와 재현 근거

모든 링크는 고정 커밋의 실제 파일이다.

1. [원래 실룩 사건](https://github.com/kkhkkh20-bit/daaegame/blob/a3350f2618b33ca1aab57504c8e8227174153b0e/experiments/renpy-ch1/game/systems/room13_town_events2.rpy#L82-L155): day 3, period 0, square에서 실행. 일반 선금 후 “실룩은 해가 져도, 다음 날이 되어도 오지 않았다.”와 콩이의 “어제”가 같은 호출에 묶여 있다. 그 사이 tick/next_day가 없다. 전액 분기도 지급 직후 미래를 단정한다.
2. [지갑과 장부 함수](https://github.com/kkhkkh20-bit/daaegame/blob/a3350f2618b33ca1aab57504c8e8227174153b0e/experiments/renpy-ch1/game/systems/room13_town_events.rpy#L49-L59): 장부에는 day/text/amount만 있고 period나 지급 분기는 없다. 일반과 추적 모두 “실룩에게 선금” -5다.
3. [시간 단위](https://github.com/kkhkkh20-bit/daaegame/blob/a3350f2618b33ca1aab57504c8e8227174153b0e/experiments/renpy-ch1/game/room13_rules.rpy#L129-L155), [절대시간](https://github.com/kkhkkh20-bit/daaegame/blob/a3350f2618b33ca1aab57504c8e8227174153b0e/experiments/renpy-ch1/game/room13_week2_rules.rpy#L141-L142): 오전0, 오후1, 저녁2, 늦은 저녁3. abs=(day-1)*4+period.
4. [일반 대화 특수 라벨 디스패치](https://github.com/kkhkkh20-bit/daaegame/blob/a3350f2618b33ca1aab57504c8e8227174153b0e/experiments/renpy-ch1/game/room13.rpy#L440-L455): R13_TOPIC_LABELS의 라벨을 호출한 뒤 대화 메뉴로 돌아간다. 자동으로 finish_topic하지 않는다. 따라서 미해결 선금 질문을 반복 가능한 살아 있는 항목으로 둘 수 있다.
5. [재접촉 가능성 판정](https://github.com/kkhkkh20-bit/daaegame/blob/a3350f2618b33ca1aab57504c8e8227174153b0e/experiments/renpy-ch1/game/systems/room13_question_discovery.rpy): 실제 읽지 않은 활성 topic을 contact_has_content가 인정한다. 새 항목은 지급 flag로만 열린다. 미지급자에게 지불을 전제한 질문은 나오지 않는다.

수정 원본 blob SHA:
- game/systems/room13_town_events2.rpy: `6151bea752d4a59f305bb5ad8b89e5c241d02341`
- game/room13_dialogue_openings_20261013.rpy: `8cdadcb781e8841e8d550787e060c2ced188487e`

## 정확한 대사 before / after

### 일반 5냥 지급

Before ev:a:paid:
1. 실룩: “해 지기 전에 짐 가지고 올게요. 걱정 마세요.”
2. 서술: “실룩은 해가 져도, 다음 날이 되어도 오지 않았다.”
3. 콩이: “실룩 아저씨요? 어제 백 부인네 뒷문으로 들어가던데요.”
4. 즉시 siluk_scammed 및 know_siluk_debt.

After 같은 ev:a:paid:
1. 실룩: “해 지기 전에 짐 가지고 올게요. 걱정 마세요.”
2. 서술: “실룩은 선금을 챙겨 자리를 떠났다.”
3. 금액 -5와 지급시점·원래 기한을 한 save-local 대입으로 기록한다. 시간은 그대로다. 즉시 미이행/빚 단정은 하지 않는다.

실제 같은 날 저녁 이후 ev:a:overdue:sunset:
“해가 졌지만, 실룩이 가져오기로 한 짐은 아직 받지 못했다.”

저녁 통지를 이미 들은 뒤 다음 날 ev:a:overdue:next_day:
“날이 바뀌어도 실룩에게 부탁한 짐은 오지 않았다.”

기한 후 처음 확인하는 시점이 다음 날 이상이면 ev:a:overdue:late:
“실룩이 짐을 가져오겠다고 약속한 날이 지났다. 아직 짐은 받지 못했다.”

콩이가 실제로 같은 장소에 있을 때만 한 번:
- 지급 다음 날 ev:a:witness:next_day: 기존 “어제” 대사 그대로.
- 그 이후 ev:a:witness:later: “실룩 아저씨요? 선금을 주신 날, 백 부인네 뒷문으로 들어가는 걸 봤어요.”

### 전액 지급(보유금 1–4냥)

Before ev:a:paid_all:
실룩 “……이것뿐이에요? 뭐, 일단 받죠.” / 서술 “그 뒤로 실룩은 다시 나타나지 않았다.” / 즉시 siluk_scammed.

After:
실룩 대사는 그대로. 서술만 “실룩은 내가 건넨 돈을 챙겨 자리를 떠났다.”로 바뀐다. 실제 차감액을 기록한다. 공통 제안의 “오늘 안에”가 기한이므로 같은 날 늦은 저녁까지는 미이행 단정을 하지 않고 다음 날짜부터 판정한다.

### 추적 5냥 지급

ev:a:follow의 목격 대사 세 줄은 전혀 바꾸지 않았다. 뭉치의 “이번 주 이자”를 직접 들었으므로 know_siluk_debt와 know_madam_hoard도 즉시 유지한다. 다만 아직 마감되지 않은 심부름의 siluk_scammed는 제거하고 실제 기한 경계에서만 추가한다. 일반 지급 후 전용 “해 지기 전” 약속을 추적 분기에 새로 끼워 넣지 않는다.

### 재접촉 인사와 선택지

기존 첫 만남/일반 인사보다 지급 상태를 먼저 본다. 인사 자체는 읽기 전용이다.
- pending: “짐을 맡기신 분이죠. 선금은 받았습니다.”
- overdue/confronted: “……맡기신 짐 말씀이죠. 아직 가져오지 못했어요.”
- 옛 저장 기한 불명: “맡기신 짐하고 선금 이야기인가요?”
- 외부의 실제 이행/정산 처리로 resolved/fulfilled가 이미 기록된 경우: “그때 맡기신 짐 이야기는 기억해요.”

항목: “맡긴 짐과 선금을 묻는다”. 메뉴와 결과:

1. pending/unknown: “맡긴 짐은 어디까지 확인하셨습니까?”
   - 아빠: “선금 드리고 부탁한 짐 말입니다. 어디까지 확인하셨습니까?”
   - 실룩: “……아직 가져오지는 못했어요.”
2. overdue: “약속한 때가 지났습니다. 어떻게 된 겁니까?”
   - 아빠: “짐을 가져오기로 한 때가 지났습니다. 어떻게 된 겁니까?”
   - 실룩: “……받은 돈을 백 부인 빚 갚는 데 썼어요. 짐은 아직 못 가져왔어요.”
3. overdue: “짐을 못 가져오셨으면 선금을 돌려주세요.”
   - 아빠: 선택지와 같은 말.
   - 실룩: “……받은 돈을 백 부인 빚 갚는 데 썼어요. 지금은 돌려드릴 돈이 없어요.”
   - 아빠: “그럼 돌려받을 돈으로 남겨 두겠습니다.”
4. overdue: “선금은 이미 드렸습니다. 부탁한 짐부터 가져와 주세요.”
   - 아빠: 선택지와 같은 말.
   - 실룩: “……알겠습니다. 아직 가져오지 못했어요.”
5. 항상: “지금은 돌아간다”. 아무 약속/거래 없음.

2·3의 직접 고백만 know_siluk_debt를 준다. 요구 종류와 대화 시점을 기록하지만 돈·증거는 지급하지 않는다. 이행 요구에 임의의 새 기한을 붙이지 않는다. “resolved”는 이 패치의 요구만으로 도달하지 않으며, 실제 반환/물품전달 시스템이 생길 때만 연결해야 한다. 이미 정산된 저장을 보존하기 위한 방어 분기만 있다.

## 저장과 시간 계약

새 저장 위치: room13.town.siluk_advance. version=1, branch, amount, payment_day, payment_period, due_day, due_kind, due_abs, status, overdue_seen, next_day_seen, witness_seen, unknown_seen. 대화 후 last_request/contact_day/contact_period 추가.

- paid: due_day=지급일, due_kind=sunset, due_abs=(day-1)*4+2.
- paid_all/follow: due_day=지급일, due_kind=end_of_day, due_abs=day*4.
- 상태: 한 원자적 지급에서 pending 생성 → 실제 기한 후 통지 시 overdue → 기한 후 플레이어가 질문/요구하면 confronted. 각종 조회는 계산만 한다.
- 저장 재로드, 다른 지급분기 재진입, 반복 질문 모두 추가 차감 없음. 표준 rollback이 지급 전 세계로 돌아가면 다른 선택을 할 수 있는 기존 Ren'Py 의미는 유지한다. persistent로 지급 사실을 강제하지 않는다.
- 대화 패킷을 실제 재생한 뒤 통지/증언 seen을 기록한다. 조회·hover·예측에서 상태를 쓰지 않는다.
- 일반 이동 루프의 r13_town_events → r13_town_events2 진입 시 기한 확인이 먼저 실행된다. 마지막 질문 뒤 같은 메뉴에 남아 있어도 재접촉은 절대시간으로 직접 판정한다.

옛 저장:
- ev_a_done만 있고 지급 장부/옛 scammed가 없으면 거절 가능성이 있으므로 지급자로 만들지 않는다.
- 유효한 단일 “실룩에게 선금(가진 돈 전부)” 행의 day와 -1..-4는 end_of_day만 회복한다. period는 모르는 그대로 둔다.
- 일반/추적 공통 5냥 행, 누락/중복/미래 날짜/잘못된 금액은 unknown_time. 옛 scammed flag는 시계의 증거가 아니다. 오래됐다고 임의의 default day를 채우지 않는다.
- unknown은 늦었다고 비난하지 않는 진척 질문만 연다. 새 돈을 요구하지 않는다. 이 보수성 때문에 날짜가 끝내 복구되지 않는 저장은 자동 overdue로 바뀌지 않는다.
- 옛 scammed와 debt flag는 파괴적으로 지우지 않는다. 과거 잘못 재생된 콩이 증언도 다시 재생하지 않는다.

## know_siluk_debt 의미 변경과 도달 가능성

이 부분은 단순 시계 수정 외의 명시적인 지식 확정 기준 교정이다. 보통 선금을 지급했다는 사실 또는 콩이가 뒷문 출입을 봤다는 사실만으로 실룩의 빚을 확정하지 않는다.

.64 로컬 전체 game의 rpy/json 사용처를 검색했을 때 소비자는 r13_ev_a_siluk 내부 “백 부인 빚 때문입니까?” 하나뿐이며 know_siluk_debt OR know_madam_hoard다. 다른 기존 필수수사/증거/재판의 의존은 발견되지 않았다. 직접 경로는 다음과 같이 남는다.

- “짐을 받아 오면 돈을 주겠다고 한다”는 조건 없는 무료 선택. 실룩이 빚을 직접 고백하고 _ep_loop=True로 돌아오므로 같은 사건 안에서 빚 질문을 고를 수 있다. 선금이나 바둑이 조건이 필요 없다.
- “바둑이를 불러 증인으로 세운다”는 기존 badook_doubt 또는 badook_ally 조건 그대로. 고백 후 _ep_loop=True로 돌아온다. 테스트도 실제 조건을 세우고 원래 분기 본문을 사용한다. 이 대안만을 필수 경로로 삼지 않는다.
- “돈을 주고 몰래 뒤를 밟는다”는 실제 이자 목격으로 두 지식 flag를 그대로 준다. 이 유료 분기는 원래부터 사건을 종료했으므로 새로 같은 메뉴로 되돌리거나 빚을 대신 갚게 만들지 않는다.
- 일반 지급 뒤 새 재접촉에서 해명/환불 요구를 고르면 직접 고백으로 빚을 알게 된다. 원래 유료 분기는 flag를 줘도 사건을 종료했으므로 그 직후 원래 빚 선택지가 열려 있던 것은 아니다.

이미 알고 있던 flag를 삭제하지 않고, 무료 진입 경로도 유지하므로 기존 필요 단서를 차단하는 변경은 아니다. 기존 빚 갚기 8냥·장부제시·입막음·마차 루트의 로직/대사/보상은 수정하지 않았다.

## 수정 경계 및 init 의존성

수정 소스 두 개:
- systems/room13_town_events2.rpy: 실룩 helper/init topic, 실룩 지급분기, 시간통지/재접촉 라벨. 누비·약상자·기존 빚 해결 라벨은 내용 그대로이며 줄만 이동한다.
- room13_dialogue_openings_20261013.rpy: r13_siluk_advance_greeting 새 순수 helper와 r13_conversation_opening 맨 앞 실룩 지급상태 분기.

새 override는 없다. init104 helpers는 기존 wallet(init91), town_set(init102), abs_time(init56), 최종 r13_people를 런타임에 호출한다. init75 인사 helper가 init104 helper를 호출하는 것도 init 완료 후의 대화 때뿐이다. encounter 기록은 기존 r13_note_encounter를 호출한다. 기존 override 체인을 덮어쓰지 않는다.

OVERRIDE_MAP에는 새 체인을 추가할 필요가 없다. opening 파일의 기존 r13_conversation_opening 및 뒤따르는 override 위치가 +10줄 이동하므로 합성 후 위치를 갱신해야 한다. 슬링의 week1_cases/memory와 소스 충돌은 없다. 공용 daram-nabi-prep는 읽기만 했다.

## 메타데이터 및 검증 인계

동봉 siluk-advance-metadata-plan.json이 정확한 packet/인사 before-after와 소스 줄 이동을 담는다. 별도 siluk-advance-context-review.json에서 모든 신규/변경 본문과 인사에 대한 실제 문맥 검수를 완료했다. 실룩·콩이의 기존 승인 talk-art registry와 정확한 emotion을 대응했으며, 새 그림 승인 또는 시각 QA를 주장하지 않는다. 문맥 판단 불능/HOLD 행은 없지만 메타데이터 통합과 런타임 시각 검증은 남는다.

필수 후속 작업:
1. 고정 .64 SHA를 확인하고 다른 수정과 합성한다. 기존 정적 ev:a:paid의 콩이 index2 바인딩을 제거하고 새 witness identity로 이동해야 한다. paid index1 및 paid_all index1의 옛 미래 서술을 남기면 안 된다.
2. 문맥 검수를 완료한 새 정적 packet 11개와 opening helper의 동적 literal 4개를 동봉 context-review JSON의 정확한 화자/본문/identity/index로 적용한다. 실룩의 기한전 답변과 일반 거래 확인 인사는 neutral, 기한후 고백·미이행·반환불능·이행요구 응답은 anxious, 콩이 증언은 neutral이다. 모든 reaction은 false다. 아빠 POV/생각과 서술은 NPC talk-art cue를 붙이지 않는다. 인사 helper는 기존 opening provider 허용 파일 안에 있어 compiler whitelist 확대가 필요 없다.
3. inventory/callsites/summary/runtime-binding-queue/dynamic-literal-inventory와 출처줄을 가진 review JSON 및 bindings를 합성 tree에서 다시 맞춘다. dynamic:739 및 기존 모든 dynamic route ID를 단순 추가 순번 때문에 바꾸지 않는다. compiler PROVIDERS의 위치 기반 인덱스가 영향을 받으므로 원래 call 표현과 binding_route를 대응시켜 확인해야 한다.
4. .64의 대사 beats/line-direction에서 제거·이동된 packet index를 정리한다. fullbody/talk-art는 새 인물/새 포즈가 없으므로 추가 art 승인을 요구하지 않는다. 이 패치만을 이유로 해당 asset registry를 바꾸지 않는다.
5. OVERRIDE_MAP 갱신. CI에서 기존 회귀와 새 dev/test_siluk_advance_timing.py 실행, Ren'Py lint, 저장/로드/rollback 및 실제 화면 확인을 맡는다.

테스트 파일은 production helper/원래 시간·장부·대화 발견 함수와 실제 authored branch 본문을 같은 store에서 사용한다. 상태를 흉내 낸 독립 사본 테스트가 아니다. 단, Ren'Py UI 엔진이나 최종 override 전체 체인을 실행하는 테스트는 아니며 화면·세이브스택 검증을 대신하지 않는다. 16개 테스트를 작성했다. 최초 미실행 전달 후 부모가 pure unittest를 승인했고, 하네스의 kwargs 전달 누락만 수정한 뒤 16/16 통과했다(최종 파일 재확인 0.215초). 검증을 약화한 변경은 없다. exact 결과와 의존파일 SHA는 siluk-advance-test-result.json에 있다. 통합 CI와 Ren'Py 런타임 검증은 여전히 미실행이다.

### 문맥 검수 근거와 한계

.64 고정 커밋의 talk-art registry blob `3445c0fbdd93a887f13d8754b1f8661ae10fb392`를 원격 읽기로 확인했고 로컬 파일과 SHA가 일치한다. 실룩과 콩이는 approved_runtime이며 neutral/anxious의 560·760·840 프레임이 등록되어 있다. 새 표현 자산을 만들거나 기존 pending fallback을 승인하지 않는다. 실룩의 빚 고백은 기존 ev:a:later/ev:a:badook/ev:a:confront의 anxious 맥락과 이어지고, 기한전 확인에는 불안을 선제 부여하지 않는다. 콩이는 이미 본 방문을 알릴 뿐이므로 기존 목격 cue와 같은 neutral이다. exact mapping JSON의 reason은 각 대사별로 작성했다. 실제 파일 loadable 여부·얼굴의 시각적 적합성·화면 전환은 실행하지 않았으므로 통합 QA가 확인해야 한다.
