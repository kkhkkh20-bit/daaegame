# 새 장(chapter) 작성 가이드 — 다람 탐정 사무소

게임은 단일 HTML(game.html) 안의 JS 데이터로 사건을 정의한다. 새 장은 **하나의 IIFE**로 작성해 별도 .js 파일로 저장한다.
파일은 `python3 /home/claude/daae/work/build_with.py /tmp/claude-0/chX.html /path/to/chX.js` 로 게임에 끼워 넣어 테스트 빌드를 만들 수 있고,
`node /home/claude/daae/work/validate.js /tmp/claude-0/chX.html <caseId>` 로 데이터 무결성/해결 가능성 검사를 돌릴 수 있다 (오류 0이어야 함, "pageerrors []" 이어야 함).
`node /home/claude/daae/work/shot.js /tmp/claude-0/chX.html /tmp/claude-0/chX.png "<caseId>-<locId>,..."` 로 배경 장면을 스크린샷(핫스팟 위치 표시 포함)해서 Read 도구로 직접 눈으로 확인한다.

## 반드시 참고할 템플릿
- `/home/claude/daae/work/template_ch7.js` : 7장 전체(가장 최신 구조). **이 구조를 그대로 따른다.**
- `/home/claude/daae/work/template_piko.js` : 인물 추가 예 (suspects.push, talk, spot, contra, HOTS, THINK, ppl, TIMELINE, CHAT, BOOK 수정)
- `/home/claude/daae/work/template_scenes_dark.js` : 배경 SVG 예 (viewBox 360x200, sv(inner,label) 헬퍼)

## 규칙 (지키지 않으면 게임이 깨진다)
- case id: 소문자 영문만 (예: "cart"). 이 id로 SCENES 키는 `"<id>-<locId>"`.
- 모든 spot은 `HOTS[spot.id]=[x,y]` 좌표 필요 (360x200 기준, 가장자리 30px 안쪽). inZoom 스팟은 제외.
- 증거 id는 전체 게임에서 유일해야 한다. 접두어를 붙여라 (예: `c8_...`). 진술 id도 유일 (예: `mungchi_c1`).
- 새 인물: `CAST.xxx={name,animal,kind,color,acc?}`. animal은 face()에 있는 것만: rabbit, bear, fox, cat, owl, dog, squirrel, crow, duck, raccoon, flyingsq, lynx, crane, goat, mole, bat, weasel, panda, woodpecker, peacock. `VOICE.xxx=숫자(360~1250)`, BIO, PERSONA도 추가.
- 기존 인물 id: tori(토끼) bori(곰) yeoni(여우) nabi(고양이) buri(부엉이,할아버지 손자) kongi(강아지,코 좋음,시계 못봄) doto(다람쥐,정확) kkwak(오리 꽥순) grandma librarian teacher(곰 선생님) owlgp(부엉이 할아버지, 은퇴 탐정) karo(까마귀, 전 반짝이 도둑→우체국) shadow nero(스라소니, 검은 망토단 두목, 지금은 숲의 작은 등불에 살며 탐정들과 묘한 동맹) seol ppul tok bami(박쥐 소녀, 은빛 마을) sling luka momo(염소 관장) ttadak(딱따구리, 뭐든 두드림) piko(공작새). 탐정 둘은 det0(큰 탐정, 침착), det1(주니어 탐정, 직감형) — 대사에서 이름은 {p0} {p1} 치환.
- contra: `{t:진술id, items:[증거/진술/결합id...], kind:"culprit"|"shy"|"mistake", say:"...", unlock:진술id|null|"door:<locId>", loc?:locId}`. hidden 진술은 contra.unlock으로 열린다. `after:"진술id"`는 그 진술을 들은 뒤 보이는 후속 질문.
- 잠긴 장소: `{id, name, req:"door:<id>" 또는 진술id, spots}` → contra.unlock/RIDDLES[].loc 로 연다. 모든 장소/진술/contra가 도달 가능해야 한다 (validate.js가 검사).
- CONFESS[id]="xxx_conf" : q:"" 인 숨은 자백 진술.
- BATTLE[id]: 4~5 라운드, 각 라운드 `{stm:[{t,p,a?}...],hit,pre?}`. 각 라운드에 accept(a) 있는 문장 최소 1개. a에는 증거/진술 id.
- final: [0]은 suspect(범인). 나머지 4~5개: text(opts 4개) 또는 place(지도에서 짚기). DEDUCE[id] 문장에 [1]..[n] 자리표시(각 final 인덱스), {C}/{C2}=범인 이름.
- COMBO[id]: 3~4개 `{a,b,name,text}` — 두 단서를 결합해 새 사실. 결합 사실은 자동으로 증거 id `cx_<caseId>_<i>`가 되어 contra.items/BATTLE a에 쓸 수 있다 (예: items:["cx_cart_0"]). **핵심 거짓말 1~2개는 결합 사실로만 깨지게 설계**할 것.
- TIMELINE, RECON, INFO, MAPS(장소 좌표 360x160 + 아이콘 종류 + roads), PPL(장면에 서 있는 인물 x,y), OBS(관찰 지점; zoom 가능), THINK(증거 발견 시 속마음), RIDDLES(3개, 정답 배열, hint), IHINT(간접 힌트 3개), CHAT(잡담 2세트씩), MOMENT(사건 순간 미니게임, 선택), LETTERS[id], VFILE.push, BOOK{pre:[...],post:[...]}(그림책 컷씬: bg, time, cast{who:x}, lines), STORY{intro,outro}.
- 아이콘: 새 증거는 `evIcon` 매핑에 기존 아이콘 id로 연결 (template_ch7 맨 위 `var M={...}` 참고). 기존 아이콘 id 목록: hair honey sill box tree invite glass foot lace kick ball owl clock log glitter roles rehearsal feather crumbs latch bell carrots bottle seat pond hanky earmuff bag order fakestone blackfeather glasscase ladder owlfeather shopsign glassjar flyer dancelamp fishsnack claw torn kongibed realstone stamps ledger anon uvw.
- SCENES: 장소마다 함수. `sv(innerSvg,"라벨")`. 색은 진한 외곽선(#0A0D24/#1B2447) + 평면 색면 스타일이지만 **깊이감(원경/중경/근경), 조명(글로우, 빛줄기), 바닥 질감**을 넣어 정성 들일 것. 헬퍼: __sky()(밤하늘), __lamp(x,y,color), __bunting(y). 문자열 연결 시 작은따옴표 안에 작은따옴표 금지.
- 톤: 중학생이 볼 수 있는 수준의 다크함. 폭력 묘사는 결과(기절, 다침)까지만, 잔혹 묘사 금지. 존댓말/반말은 캐릭터 성격대로. 이모지 금지.
- 마지막에 `c.map=MAPS[id];c.timeline=...;c.recon=...;c.ppl=...;c.locations.forEach(...info/obs...)` 배선과 `applyOV` 불필요. HOTS는 Object.assign(HOTS,{...}).
- 새 장은 `part:3`.

## 난이도 곡선: 범인이 점점 똑똑해진다 (v85부터 필수)
새 묶음(11장~)은 아래를 기본으로 넣고, 뒤로 갈수록 강하게 한다.
- 결합 전용 거짓말: 사건당 최소 2개. 절반만 내밀면 넛지, 단일 증거 설명문에는 결론을 쓰지 않는다.
- "?" 검사: 결합 재료 중 하나는 검사해야 핵심 특이점이 드러나게(check.gate).
- 자외선: 사건당 1개 이상, 결합 재료로 쓰인다.
- 함정 증거(TRAP): 범인이 심어 둔 증거 1개. 겉 설명은 무고한 사람을 가리키고, 검사하면 심은 흔적이 보인다. 무고한 사람에게 내밀면 목숨 -1 + TRAP think 대사.
- 만들어진 알리바이: 증인의 착각(kind:"mistake")을 먼저 깨야 범인 알리바이가 깨지는 2단 구조 1개.
- 증거 역이용(BAIT): 대결에서 그럴듯한 오답 증거를 내밀면 범인이 그 증거로 오히려 자기 편을 드는 반박 대사. 사건당 2~3개.
- 범인의 반격(TWIST): 최후 반론 직전, 범인이 반격 증거를 내민다(check.gate로 허점 숨김). 두 번 틀리면 친구가 도와준다(help).
- REACT/BRK: 새 범인은 work/react.js의 RX(당황 4단계), BRK(최후 한마디)에 대사를 추가한다.
