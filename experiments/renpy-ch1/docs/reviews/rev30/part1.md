# rev29 배역 검토 1부 (1~16행)

> revision30: 보리 = latest-0 bear life pose (무스는 뭉치로 이동, 이 파일의 보리 항목은 곰 기준으로 다시 썼다)

검토 기준: `brief.md`. 읽기 전용 조사이며 저장소 파일은 고치지 않았다.
경로 약어: `G/` = `experiments/renpy-ch1/game/`, `A/` = `experiments/renpy-ch1/art/`, `N` = `experiments/renpy-ch1/story-room13/narrative.json`.

## 공통 확인 사항

- 선택 이미지와 현재 게임 대화 전신(neutral)을 알파 영역 기준 48×72 흑백으로 비교했다.
  - 차이 0.0, 즉 같은 그림: 다람·아빠·엄마·할머니(redesign v2)·세련·나비·까로·돌목·밤이·토리·여니(redesign)
  - 다른 그림: 부리(56.9)·도토(71.0)·너울(67.5)·콩이(30.6, 같은 디자인의 소폭 수정본)
  - 이 네 배역의 선택 그림은 저장소 어디에도 들어와 있지 않다. `remodel-resident_kongi`, `brown_owl`, `child_deer`, `golden_dog`를 검색해도 걸리는 것이 없다.
  - 보리(revision30, latest-0)는 대화 그림이 아니라 생활 동작 `living_firewood`로 이미 게임에 들어와 있다(14절).
- 실행 본문(rpy·room13-content·openings)에는 종을 직접 가리키는 단어가 거의 없다. 종은 주로 `N`의 `species` 메타, `A/npc-redesign-20261015/redesign.json`, 레거시 `G/assets/resident-art.json`에 있다.
  - `resident-art.json`은 rpy와 dev 스크립트 어디에서도 읽지 않는다. 그래서 설정 문서로만 다룬다.
  - `G/assets/room13-avatars.json`도 rpy 참조를 찾지 못했다. 확인 불가로 둔다.
- 대화 전신을 redesign으로 바꾼 전례가 있다: 할머니·보리·여니는 6개 표정 모두 같은 그림 한 장을 쓴다(`G/assets/room13-fullbody-dialogue.json`). 같은 방식이면 선택 그림을 대화에 넣을 때 새로 그릴 필요가 없다.
- 회의 자리:
  - trial(원탁, 의자): `seryeon, resident_ppul, buri, nabi, resident_bori, resident_tori, doto, resident_kongi` (`G/systems/room13_debate.rpy:358`). 앉은 그림은 `G/assets/room13-meeting-seated.json`.
  - finale(제단, 의자 없음): `resident_ppul, resident_bori, nabi, buri, neoul, resident_tori` (`:359`). 서 있는 neutral 그림을 쓴다(`G/room13_meeting_seating.rpy:112`, `:94-97`).

---

## 1. 다람 (daram) — current-fd96678

1. **선택 이미지**: 어린 다람쥐 여자아이. 빨간 사냥모자(리본), 남색 세일러 원피스, 빨간 나비리본, 갈색 수첩을 두 손으로 든다. 큰 머리, 짧은 다리.
2. **현재 설정**: 아이 탐정. `G/room13.rpy:604` "그 안에는 다람 양이 있었습니다." 아빠의 딸.
3. **충돌**: 없음.
4. **적용 상태**: 대화 전신 `room13-fullbody-daram-*`(선택 그림과 같음), 조사 그림 `room13-pixel-world-daram-gray-gutter.webp`, 프로필 `room13-pixel-family-profile-icons.webp`, 눈 깜빡임 효과가 있다. 선택 그림이 이미 게임에 있다.
5. **분류**: ① 지금 게임 그림과 같고 설정과도 맞는다.

## 2. 아빠 (dad) — current-fd96678

1. **선택 이미지**: 어른 다람쥐 남성. 남색 코트, 크림 조끼, 빨간 목도리, 올리브 바지, 두 주먹을 쥔 자세.
2. **현재 설정**: 플레이어 시점의 아버지. `G/options.rpy:124` `"dad":"아빠"`
3. **충돌**: 없음.
4. **적용 상태**: 대화 전신(같은 그림), 조사 그림 `room13-pixel-world-dad-gray.webp`·`family-extra-gray`, 프로필 아이콘. 컷신 `room13-pixel-cinematic-key-family015.webp`(return/rescue)도 같은 복장이다.
5. **분류**: ① 지금 그림과 같다.

## 3. 엄마 (mom) — current-fd96678

1. **선택 이미지**: 어른 다람쥐 여성. 이마에 고글, 청록 망토, 크림 블라우스, 붉은 바지, 어깨 가방, 갈색 장화, 책을 든다.
2. **현재 설정**: 실종된 연구자 어머니. 온실(greenhouse)에서 action_1/2를 한다(`G/room13_acting.rpy:280`).
3. **충돌**: 없음.
4. **적용 상태**: 대화 전신(같은 그림), `room13-pixel-world-mom-gray-gutter.webp`, 깜빡임 효과.
5. **분류**: ① 지금 그림과 같다.

## 4. 부리 (buri) ← 갈색 부엉이 `brown_owl-dry_amusement`

1. **선택 이미지**
   - 수리부엉이 계열(귀깃 있음), 어른 남성 인상, 둥근 안경, 비꼬는 듯한 웃는 표정(입을 벌림).
   - 크림 셔츠, 금단추 빨간 조끼, 초록 넥타이, E자 버클 벨트, 회색 반바지, 맨발톱.
   - 한 손은 허리, 한 손은 가슴. 날개가 소매 아래로 길게 늘어진다.
2. **현재 설정**
   - `N:215` `"species": "owl"`
   - `G/room13-content.json:8162` "수리점과 조부의 도구 관리"
   - 조부는 부엉이 할아버지(resident_owlgp)다. `G/room13.rpy:575` "할아버지! 비켜요!"
   - 말투는 존댓말 어른이다. openings:486 "보는 건 괜찮아요. 하지만 만지시면 어느…"
   - 나이를 적은 곳은 없다.
3. **충돌**
   - 종·성별·나이 기능은 충돌하지 않는다(어른 손자로 읽힌다).
   - 시각 주의점이 하나 있다. 현재 resident_owlgp(`room13-redesign-resident_owlgp.webp`)도 귀깃 있는 갈색 부엉이에 안경을 썼다. 머리 디자인이 매우 비슷해서 할아버지와 손자가 같은 사람처럼 보일 수 있다. 복장 차이(초록 코트·지팡이 vs 빨간 조끼)로만 구분된다. 원화 수정은 요구하지 않는다. 대화창 이름표로 충분한지 사용자 확인만 권한다.
   - 참고: `A/npc-redesign-20261015/redesign.json` basis에 "The brown owl is NOT applied: resident_owlgp waits for an elderly version."이라는 이력이 있다. 그 갈색 부엉이가 이번에 부리로 배정된 것이다.
4. **적용 상태(모두 옛 부리: 앳된 부엉이, 검정 조끼, 빨간 나비넥타이, 회중시계)**
   - 조사 기본·생각·동작: `room13-pixel-acting-buri.webp`
     - action_1 = 공구로 회중시계 수리(right)
     - action_2 = 무릎 꿇고 돋보기(right)
     - 수리점에서 오전·오후는 action_1, 저녁은 action_2 (`G/room13_acting.rpy:270`)
   - 사건 동작: `room13-action-buri-event_toolbox.webp` (r13_w2e_tools)
   - 대화: `room13-pixel-dialogue-buri.webp`(portraits), `room13-fullbody-buri-{6표정}.webp`
   - 깜빡임: `room13-fx-blink-buri-*` 10장
   - 프로필: `room13-pixel-main-profile-b.webp` [1450,0,720,720]
   - 회의 착석: `room13-meeting-seated-buri068.webp`(trial). finale에서는 서 있는 neutral을 쓴다.
   - 몸 반응: `R13_REACT_PEOPLE`에 포함(`G/systems/room13_dot_fx.rpy:408`)
   - 선택 이미지는 게임에 없다.
5. **분류**: ③ 이미지·동작 추가 필요. 설정 수정은 필요 없다(종 owl 그대로).
6. **제작 명세**
   - 대화: 선택 그림을 redesign 방식으로 6표정 공용 neutral로 쓴다. 새로 그리지 않는다.
     - 선택본 표정이 '비꼬는 웃음'이라 슬픔·분노 장면에도 그대로 나온다. 표정을 따로 원하면 추가 표정 5장(joy/anxious/surprise/angry/flustered)을 같은 구도로 요청한다. 선택 사항이다.
     - `room13-fx-blink-buri-*` 눈 좌표는 옛 그림 기준이다. 다시 만들거나(`dev/make_dot_fx.py`) 부리를 깜빡임 목록에서 빼야 한다.
   - 조사(수리점 workshop, 1주·2주 매일 오전·오후·저녁 상주)
     - action_1: 서서 작업대 쪽으로 몸을 숙이고 작은 망치와 회중시계를 든다. 시선은 손. 오른쪽을 본다. 발은 바닥선. 안경 유지.
     - action_2: 한쪽 무릎을 꿇고 돋보기로 회중시계를 본다. 오른쪽. 무릎과 앞발이 바닥에 닿는다. stature 약 0.7.
     - event_toolbox: 서서 나무 공구함 위에 한 손(날개 손)을 얹는다. 공구함은 발 앞 바닥에 둔다. 사건 r13_w2e_tools.
   - 회의 착석(trial 원탁): 의자에 오른쪽 사선으로 앉아 두 손을 무릎에 둔다. 발은 바닥, 날개 끝은 의자 옆으로 늘어진다. 기존 seated 규격(약 1190×1322 캔버스, 알파 128 기준 crop)을 따른다.
   - 프로필: 선택 그림 머리 부분을 정사각으로 자른다(안경 포함).
   - 재사용: 선택 원화 한 장(복장·얼굴 기준). 기존 포즈 구성은 `room13-pixel-acting-buri.webp`를 참조한다.

## 5. 할머니 (granny) — current-fd96678

1. **선택 이미지**: 늙은 토끼 여성. 처진 귀, 둥근 안경, 붉은 카디건, 꽃자수 앞치마, 행주, 갈색 장화.
2. **현재 설정**: `G/room13-content.json:8345` "토끼 할머니", `N:419` `"species": "rabbit"`. 여관 접수, 진범.
3. **충돌**: 없음.
4. **적용 상태**
   - 대화·조사·프로필 모두 `room13-redesign-granny.webp`(granny_elders_reference_v2). 선택 그림과 같다.
   - 생활 동작 `living_keyledger`(열쇠와 장부, 같은 복장 확인)
   - 회의 착석 `room13-meeting-seated-granny068.webp`(redesign을 참조해 생성, README에 기재)
5. **분류**: ① 이미 2026-10-15 redesign으로 적용된 그림과 같다.

## 6. 세련 (seryeon) — current-fd96678

1. **선택 이미지**: 여우 청년 남성. 붉은 앞머리, 금단추 파란 코트, 노란 조끼, 빨간 넥타이, 종이 뭉치를 든다.
2. **현재 설정**: 우편 접수 담당. openings "저는 여기서 우편 접수를 맡고 있습니다."
3. **충돌**: 없음.
4. **적용 상태**: 대화 전신(같은 그림). 조사는 `room13-pixel-acting-seryeon.webp`, 의자 그림은 `-chair`(우체국 오후 chair_read). 회의 착석 seryeon068.
5. **분류**: ① 지금 그림과 같다.

## 7. 나비 (nabi) — current-fd96678

1. **선택 이미지**: 크림색 고양이 소녀. 방울 귀걸이와 방울, 남색 세일러복, 두 손을 모은다.
2. **현재 설정**: `N:164` `"species": "cat"`. 여관 식사 담당 아이. openings "아이가 그릇을 하나 더 꺼냈다."
3. **충돌**: 없음.
4. **적용 상태**: 대화 전신(같은 그림), 조사 `room13-pixel-acting-nabi.webp`, 회의 착석 nabi068, 깜빡임 효과.
5. **분류**: ① 지금 그림과 같다.

## 8. 도토 (doto) ← 꼬마 사슴 `child_deer-base`

1. **선택 이미지**
   - 어린 사슴(새끼 노루 인상) 남자아이. 뿔은 없고 큰 귀.
   - 파란 단추 재킷, 크림 스웨터, 녹슨 주황 목도리, 짙은 갈색 바지, 갈색 장화. 손에 든 것은 없다.
   - 머리가 크고 몸이 가늘다. 키가 작은 아이 체형이다.
2. **현재 설정**
   - 종: `N:317` `"species": "squirrel"`(메타). 현재 그림은 안경 쓴 통통한 다람쥐.
   - 직업: `G/room13-content.json:8254` "장부 정리와 광장 배급 보조"
   - 아이로 쓰인 곳
     - `G/room13-dialogue-openings.json:761` "광장 한쪽에서 한 아이가 무언가를 쓰고 있었다."
     - openings:709 아빠의 반말 "안녕. 잠깐 뭐 좀 물어봐도 되니?"
     - `G/systems/room13_use_knowledge.rpy:34` "그날 복도는 어디까지 보였니?"
   - 어른 역할로 쓰인 곳(사건)
     - `G/room13.rpy:563` "도토가 할머니에게서 지렛대를 받아 문틀 틈에 밀어 넣었다. 너울과 함께 문을 받쳤다."
     - `G/systems/room13_inn_change.rpy:56` "도토가 지렛대를 문틀 틈에 밀어 넣었다."
     - `G/room13.rpy:571` 너울 "도토 씨, 바닥에 지금 보이는 자국부터 그려 주십시오."
     - `G/room13.rpy:573` E33 "구한 직후 너울·도토가 남긴 방 그림과 봉해 둔 물건"
     - `G/room13-content.json:7733` `"E11": "doto"`(복도의 구조 순서, :136 "공구가 온 뒤 빗장을 부숨")
     - `G/systems/room13_testimony.rpy:11` J10 "도토가 지킨 곳은 복도 쪽 13호 문이다."
     - testimony:51-55 "제가 지킨 문으로는 아무도 들어가지 못했어요."
     - use_knowledge:35-40 J17 (복도 시야 증언)
     - `G/systems/room13_debate.rpy:119` E11 반박 "복도 사람들이 지켜본 건 13호 앞문뿐입니다."
   - 배급 장면: `G/systems/room13_bundle3.rpy:134-143`. 도토가 장부를 보여 주고 표준 추를 올린다(아이 보조로도 가능).
   - 일정: 1~4일 광장, 5일부터 hall(`G/room13_rules.rpy:236`), 2주차 hall(`G/room13_week2_rules.rpy:161`).
   - 레거시(Room13 흐름에서 호출 확인 안 됨): `G/winter.rpy:284` "아침에 도토 씨가 그랬잖아", `G/options.rpy:149` "도토의 날씨 일지"
3. **충돌**
   - (a) 나이 기능: 본문 자체가 이미 둘로 갈려 있다. 첫 만남과 탐문은 아이, 사건은 어른 역할이다. '꼬마 사슴' 그림은 첫 만남과 탐문 쪽에는 맞는다. 하지만 아래 셋과는 정면으로 부딪친다.
     - 지렛대로 빗장을 뜯는 힘 쓰는 구조 행동(room13.rpy:563, inn_change.rpy:56)
     - "도토 씨" 호칭과 공식 현장 도면 작성(room13.rpy:571, E33)
     - 단독 문지기 증언이 재판 반박 근거가 되는 구조(E11 출처, J10, J17, debate.rpy:119)
   - (b) 종: 메타 squirrel 대 그림 사슴. 실행 본문에는 종 단어가 없다(꼬리·도토리 묘사는 다람이 엄마 표시이지 도토 묘사가 아님).
   - (c) 표시 크기: 대화 전신 보정 `R13_FULLBODY_TUNING = {"bami":.88,"doto":.92}`(`G/room13_fullbody_dialogue.rpy:38`)은 옛 그림의 귀 높이에 맞춘 값이다. 큰 사슴 귀로 바뀌면 다시 확인해야 한다. 광장 표시 키 `("doto","square"):(1030,624,245)`(`G/room13_acting.rpy:197`)는 어른 키 245px다(까로·너울은 280). 꼬마 체형이면 더 낮춰야 하는지 결정이 필요하다.
4. **적용 상태(모두 옛 다람쥐)**
   - 조사: `room13-pixel-acting-doto.webp`
     - neutral = 장부를 낀 서기, left
     - action_1 = 서서 장부에 쓰기(held_ledger, right). hall 오전·오후.
     - action_2 = 바닥에 책상다리로 앉아 읽기(floor_sit, left). hall 저녁.
     - world_bulletin_back = 게시판을 가리키는 뒷모습(`room13-pixel-world-context0156.webp`, 광장)
   - 대화: `room13-pixel-dialogue-doto.webp`, `room13-fullbody-doto-{6}.webp`
   - 프로필: `main-profile-b` [770,0,678,678]
   - 회의 착석: `room13-meeting-seated-doto068.webp`(trial)
   - 몸 반응: `R13_REACT_PEOPLE` 포함
   - 선택 이미지는 게임에 없다.
5. **분류**: ④(주) + ② + ③
   - ④ 사용자 결정 필요
     - A안(권장, 본문 대부분과 일치): 도토를 아이로 확정한다.
       - room13.rpy:563·inn_change.rpy:56의 지렛대 행동을 너울이 하게 하고 도토는 등불을 들거나 문을 잡게 한다. E11 "공구가 온 뒤 빗장을 부숨"은 누가 했는지 적지 않으므로 증거 문구는 그대로 둘 수 있다.
       - room13.rpy:571 "도토 씨"는 "도토야"나 이름만 부르는 것으로 바꾼다.
       - E33 도면 작성자와 J10·J17 문지기 증언을 아이가 맡는 것을 그대로 둘지 결정한다.
     - B안: 사건 기능을 지키고 '키 작은 청년 사슴'으로 해석한다. 이 경우 openings:709·761·use_knowledge:34의 아이 취급(반말, "한 아이")을 고쳐야 하고, 꼬마 체형 그림과 어긋남이 남는다.
     - 어느 안이든 증거 ID·성립 조건은 바꾸지 않는다. 증언자 연령에 따른 신빙성 대사(재판 쪽)를 손대려면 회의 담당과 맞춰야 한다.
   - ② `N:317` squirrel → deer. 결정 뒤 위 해당 행만 고친다.
   - ③ 아래 명세.
6. **제작 명세(④ 결정 뒤 진행. 복장은 선택 그림 그대로: 파란 재킷·주황 목도리·뿔 없음)**
   - 대화: 선택 그림을 6표정 공용으로 쓴다(redesign 방식). 새로 그리지 않는다. TUNING .92와 머리 상자(귀 끝~턱)를 다시 잰다.
   - 조사 neutral: 선택 그림을 그대로 쓰고, 장부는 들지 않은 채로 둔다. 장부를 원하면 action에서만 보인다.
   - action_1(held_ledger): hall(여관 2층 13호 앞 복도), 5일 이후 오전·오후. 서서 작은 장부를 왼팔에 끼고 연필로 쓴다. 시선은 장부, 오른쪽을 본다. 발은 바닥선.
   - action_2(floor_sit): hall 저녁. 복도 바닥에 책상다리로 앉아 무릎 위 장부를 읽는다. 엉덩이와 발이 바닥에 닿는다. stature 약 0.6. 왼쪽을 본다.
   - world_bulletin_back: 광장 1~4일. 게시판 쪽으로 돌아선 뒷모습(오른쪽 사선). 한 손은 게시판을 가리키고, 다른 팔에 종이 몇 장을 낀다. 게시판 바로 앞 바닥선에 선다. 지금은 context0156 공용 시트의 칸이라 단독 파일로 받는다.
   - 회의 착석(trial): 의자에 오른쪽 사선으로 앉아 손을 무릎에 둔다. 다리가 짧아 발이 바닥에 겨우 닿거나 떠 있다. 의자 높이에 맞추고 발 접점을 표시한다.
   - 프로필: 선택 그림에서 귀 포함 정사각으로 자른다.
   - 필요한 표정: 사건 직후 장면은 anxious/surprise 계열. 공용 neutral을 쓰면 표정 변화가 없다는 점을 사용자에게 알린다.

## 9. 까로 (karo) — current-fd96678 (사용자 대표 선택)

1. **선택 이미지**: 까마귀 계열 어른 남성. 남색 깃털에 파란 줄무늬 볏, 빨간 셔츠재킷, 노란 조끼, 어깨띠 가방, 갈색 반바지, 남색 손(장갑처럼 보임), 맨발톱.
2. **현재 설정**
   - `N:623` `"species": "crow"`. 마차 수리와 반송품 운반(`G/room13-content.json:8571` activity "마차 축의 갈라진 부분을 감싼다.")
   - "까로 아저씨"(openings:1443)
   - 장갑 서술: openings:1407·1490 "까로가 장갑을 다시 꼈다.", 1443·1461 "장갑을 벗고 다시 뻗었다."
3. **충돌**: 없음. 그림의 남색 손이 장갑으로 읽힌다. "벗었다"는 서술에만 있는 동작이라 그림과 어긋나지 않는다.
4. **적용 상태**: 일관된다. 흰 독수리 관련 참조는 게임·art 어디에도 없다(`eagle` 검색 0건).
   - 대화 전신 = 선택 그림
   - portraits `room13-pixel-karo-fullbody.webp`
   - 조사 `room13-pixel-acting-karo.webp`
   - 입구 생활 동작 `living_axlewrap`(무릎 꿇고 축 감기, stature 0.72, 같은 복장·남색 손 확인)
   - 프로필 `main-profile-c`
   - 회의 착석 대상이 아니다.
5. **분류**: ① 현재 그림 유지가 선택이며 대사와도 맞는다.

## 10. 너울 (neoul) ← 황금빛 개 `golden_dog-base`

1. **선택 이미지**
   - 골든리트리버형 큰 개, 어른 남성, 둥근 안경, 웃는 얼굴.
   - 흰 긴 코트(실험복·의사 가운 인상), 적갈색 조끼, 청록 목도리, 갈색 바지, 장화. 손에 든 것은 없다.
   - 몸통이 넓고 키가 크다. 꼬리가 코트 밖으로 나온다.
2. **현재 설정**
   - 역할: 경비 책임자. `G/systems/room13_learning.rpy:8` `"neoul":"경비"`
   - `G/systems/room13_episodes.rpy:141` "경비 두 사람이 들어왔다. 너울과 바둑이였다."
   - 권위적이고 고압적이다
     - `G/systems/room13_bundle3.rpy:127` "배급 장부에 적힌 것보다 감자 한 자루…"
     - episodes:392 "너울이 톡의 작업대를 손바닥으로 내리쳤다."
     - episodes:406 "너울이 톡의 손목을 묶었다."
   - 사건
     - `G/room13.rpy:563` 도토와 함께 문을 받친다.
     - :568 "너울이 연기 나는 작은 깔개 위에 젖은 천을 덮었다."
     - :571 "문 앞은 제가 막겠습니다."
     - :576 촛대를 싸서 봉하고 "아이는 초소 보호실에 두겠습니다."
   - 일정: 사건 뒤 입구(`G/room13_rules.rpy:240`), 2주차 옛 시설(`G/room13_week2_rules.rpy:158`)
   - 종 메타 없음(`N:1808`은 id·이름만). 어른 남성(레거시 `chapter-dialogue.json:2193` "너울 아저씨").
   - 이름 잔재: `G/room13-content.json:9127-9129` `"id": "wanggu"`, `"name": "왕구"`, `"work": "광장 질서와 행사 준비"`. 화면 이름은 `G/options.rpy:124` "너울"이라 표시에는 영향이 없다.
3. **충돌**
   - 종·나이·성별·사건 기능은 충돌하지 않는다. 어른 남성 덩치라 문 받치기·현장 봉인 역할에 맞는다.
   - 인상과 역할 표지: 지금 너구리 그림의 보안관 별 배지·중절모가 '경비'를 알려 주는 장치였다. 선택본의 흰 가운과 온화한 웃음은 의사·학자로 읽힐 수 있다. 진료소 서리 검사원과 혼동될 위험이 있다. 사용자 방향(이미지 우선)에 따라 그림은 그대로 두고, 필요하면 첫 등장 서술에 "경비 완장/호루라기" 같은 소품 언급을 더할지 결정만 남긴다(선택 사항).
   - 시각 주의: 같은 황금색 처진귀 개인 콩이(아이)와 부자처럼 보일 수 있다. 본문에 둘의 관계는 없다.
   - 몸 반응 목록 `R13_REACT_PEOPLE`(`G/systems/room13_dot_fx.rpy:408`)에 neoul이 있다. 같은 파일 :407 주석은 "몸집이 큰 인물은 움직임이 과해 보여 넣지 않았다"이다. 큰 개 그림이 되면 빼거나 다시 확인해야 한다.
   - 참고: 기획안 `plan/NEW_CHARACTERS_PLAN_0171.md:28` 달그락 = 너구리. 옛 너울 너구리 그림과 겹치던 문제가 이 교체로 풀린다.
4. **적용 상태(모두 옛 너구리 보안관)**
   - 조사: `room13-pixel-acting-neoul.webp`
     - neutral = 팔짱(left)
     - action_1 = 뒷모습으로 수첩에 적기(held_notebook, rear). 입구.
     - action_2 = 접이식 의자에 앉아 이마를 짚기(portable_stool, left). 옛 시설 저녁(`G/room13_acting.rpy:282-283`)
     - 입구 표시 키 `(788,614,280)`(:191)
   - 대화: `room13-pixel-dialogue-neoul.webp`, `room13-fullbody-neoul-{6}.webp`
   - 프로필: `main-profile-c` [735,0,710,710]
   - 회의: finale 제단에서 서 있는 neutral(앉은 그림 없음)
   - 선택 이미지는 게임에 없다.
5. **분류**: ③ (+② 선택: content.json:9127-9129 이름 잔재 정리, REACT 목록 확인)
6. **제작 명세(복장은 선택 그림: 흰 코트·조끼·청록 목도리·안경)**
   - 대화: 선택 그림을 6표정 공용으로 쓴다. 새로 그리지 않는다. 고압적인 대사가 많아서 angry 표정 1장을 추가하면 효과가 크다(선택 사항).
   - action_1(입구, 사건 뒤 오전·오후): 등을 반쯤 보이며 서서 수첩에 적는다. 시선은 수첩. 발은 바닥선. 표시 키 약 280px 기준.
   - action_2(옛 시설, 2주차 저녁): 접이식 나무 의자에 앉아 한 손으로 이마를 짚고 무릎에 수첩을 둔다. 엉덩이는 의자, 발은 바닥. stature 약 0.75. 왼쪽을 본다. 큰 몸통이 의자를 덮지 않게 의자 다리가 보이도록 한다.
   - finale 제단: 서 있는 neutral 그대로 쓴다. 선택본은 정면에서 조금 오른쪽을 보므로 facing 값을 다시 매긴다.
   - 프로필: 안경과 목도리가 들어가게 정사각으로 자른다.

## 11. 돌목 (guard) — current-fd96678

1. **선택 이미지**: 오소리·너구리 계열 어른. 초록 군용 코트(털 칼라), 빨간 목도리, 금단추, 허리 주머니, 장부를 든다.
2. **현재 설정**: 경비. 입구 action_1(`G/room13_acting.rpy:268`). `N:1816`에는 id·이름만 있다.
3. **충돌**: 없음.
4. **적용 상태**: 대화 전신(같은 그림), `room13-pixel-acting-guard(-extra).webp`, 프로필 `main-profile-c`.
5. **분류**: ① 지금 그림과 같다.

## 12. 밤이 (bami) — current-fd96678

1. **선택 이미지**: 박쥐 아이. 큰 분홍 귀, 갈색 두건, 하트 앞판 옷, 빨간 리본, 보라 피부.
2. **현재 설정**
   - `N:878` `"species": "bat"`
   - `G/systems/room13_episodes.rpy:182` "밤에 깨어 있는 건 원래 그런 거예요. 박쥐니까요."
   - openings "처마 밑에 한 아이가 무릎을 끌어안고"
3. **충돌**: 없음.
4. **적용 상태**: 대화 전신(같은 그림, TUNING .88). 조사는 거꾸로 매달린 자세(contact hanging, `room13-pixel-acting-bami.webp`). 깜빡임 효과.
5. **분류**: ① 지금 그림과 같다.

## 13. 토리 (resident_tori) — current-fd96678 (사용자 대표 선택)

1. **선택 이미지**: 크림색 토끼 청년(한쪽 귀가 접힘). 초록 재킷, 크림 셔츠, 겨자색 바지, 갈색 서류가방을 어깨에 멘다.
2. **현재 설정**: `N:11` `"species": "rabbit"`. `G/room13-content.json:7977-` 광장 수선과 여관 납품. openings "토리예요. 첫인사를 일 시키면서 하다니"
3. **충돌**: 없음.
4. **적용 상태**: 확인 결과 일관된다(같은 복장·가방).
   - 대화 전신 = 선택 그림
   - portraits `room13-pixel-dialogue-support-01.webp`
   - 조사 `room13-pixel-acting-resident_tori.webp`(activity = 바느질)
   - 광장 벤치 `world_bench_left`(context0156)
   - 회의 착석 tori068
   - 아바타 `room13-pixel-avatar-support-0.webp`
5. **분류**: ① 현재 유지가 선택이고 모든 파일이 같은 디자인이다.

## 14. 보리 (resident_bori) ← revision30: 본인 선택 `latest-0`(파란 패치 작업복 곰, 장작 묶기 생활 동작)

1. **선택 이미지**
   - 원본: `A/bori-nero-storybook-20261015/bori/bori-firewood-plump-v2.png`. 사용자 확정 2026-10-15 19:16. 게임 파일은 `G/assets/room13-action-resident_bori-living_firewood.webp`.
   - 갈색 곰 어른 남성. 통통한 볼과 몸통, 짧고 밝은 주둥이, 작은 눈, 부드러운 미소.
   - 연청색 누빔(퀼팅) 작업복: 왼팔꿈치 갈색 덧댐, 큰 단추 하나, 크림 소맷부리. 크림 터틀넥, 회색 바지, 주황빛 황갈색 장화.
   - 웅크려 장작 묶음의 끈을 두 손으로 당긴다. 시선은 장작.
   - 이 그림은 생활 동작이다. 대화 기본 그림이나 학교 책상 자세로 쓰지 않는다(소유자 지시, INTAKE.md "대화 그림은 바꾸지 않는다").
2. **현재 설정**
   - 종: `N:62` `"species": "bear"`. 실행 본문에 곰 단어는 없다("곰 선생님"은 resident_teacher). 레거시 `G/assets/resident-art.json:54` `"animal": "bear"`(미사용).
   - 직업: `G/room13-content.json:8024` "장작 운반과 가족 돌봄", :8064 activity "장작을 묶고 끈을 다시 조이고 있다."
   - 어른, 아이를 키움: openings:178 "저 아저씨, 장작 때문에 앞이 보이긴 해?", `G/systems/room13_town_events2.rpy:54` "애 열이 사흘째예요."
   - 배급 누명 장면: `G/systems/room13_bundle3.rpy:126-`
3. **충돌**
   - 종·나이·가족·사건 기능 모두 충돌하지 않는다(곰 유지, ② 없음). 동작은 content activity 문장과 정확히 맞는다.
   - 그림끼리 어긋나는 곳(생활 동작 곰 vs 대화·서 있는 곰)이 있다. 비교 근거는 `room13-redesign-resident_bori.webp`, firewood 원본, `room13-meeting-seated-resident_bori068.webp`를 나란히 놓고 본 것이다.

     | 항목 | 대화·서 있는 곰(redesign five_town_bear) | 생활 동작 곰(latest-0) |
     |---|---|---|
     | 상의 | 진청색 평직 초어 재킷, 접은 깃, 가슴 주머니, 앞이 열림 | 연청색 누빔 재킷, 덧댐, 큰 단추, 패딩 질감 |
     | 안쪽 | 골지 크루넥 크림 스웨터, 갈색 벨트가 보임 | 크림 터틀넥, 벨트 안 보임 |
     | 바지 | 짙은 회갈색 | 밝은 회색 |
     | 장화 | 황갈색 | 주황빛 황갈색(비슷함) |
     | 얼굴 | 치켜뜬 눈썹, 굳은 표정, 짙은 주둥이 | 둥근 얼굴, 순한 미소, 밝은 주둥이, 통통한 볼 |
     | 체형 | 근육질, 키가 크고 날렵함 | 통통하고 둥근 체형 |

   - 색 계열(파랑·크림·회색·황갈)이 같아서 같은 사람으로는 읽힌다. 다만 조사 화면에서 서 있는 보리와 웅크린 보리가 번갈아 나오면 얼굴 인상과 재킷 재질이 달라 보인다.
4. **적용 상태**
   - 대화 전신 6표정·portraits·cast 기본/생각/곤란/표현·아바타: 모두 `G/assets/room13-redesign-resident_bori.webp`(2026-10-15 redesign five_town_bear, 근육질 진청 재킷 곰). 6표정이 같은 그림 한 장이다(`G/assets/room13-fullbody-dialogue.json`).
   - 생활 동작 `living_firewood`
     - stature_ratio 0.69, foot [210,560], contact crouching(`G/assets/room13-pixel-acting.json:3773-`)
     - 입구·가게·광장·작업장에서 idle일 때 표시(`R13_LIVING_ALLOWED`, `G/room13_acting.rpy:254`). 시간대 구분은 없다.
     - 2주차 가게(오후)·입구(저녁)에도 나온다(`G/room13_week2_rules.rpy:156`).
     - 선택 그림이 이미 게임에 이 자리로 적용되어 있다.
   - 학교 뒷줄(2주차 오전)·숲: 기본 서 있는 redesign 곰
   - 회의
     - trial 원탁: `room13-meeting-seated-resident_bori068.webp`. redesign 곰을 참조해 생성했다(README). 근육질 진청 재킷, 벨트.
     - finale 제단: 서 있는 redesign 곰. facing right 보정(`G/room13_meeting_seating.rpy:23`).
   - 쓰이지 않는 옛 파일: `room13-fullbody-resident_bori-*.webp`, `room13-pixel-acting-resident_bori.webp`(provenance·coverage에만 남음)
5. **분류**: ① 대사·설정은 그대로 가능 + ③(선택) 외형 통일용 기본 그림
   - 선택한 생활 동작은 이미 들어가 있다. 지금 상태로도 실행에 문제는 없다.
   - 사용자가 '보리 = latest-0 외형'으로 통일하기를 원하면 아래 ③을 진행한다. 지금 redesign 곰을 대화 기본으로 계속 쓸지는 사용자가 확인할 사항이다.
6. **제작 명세(통일을 원할 때만. latest-0 원화는 다시 그리지 않는다)**
   - 서 있는 기본 그림 1장(대화 6표정 공용 + 조사 neutral·학교 뒷줄·제단)
     - 복장: latest-0 그대로(연청 누빔 재킷·팔꿈치 덧댐·큰 단추·크림 터틀넥·회색 바지·주황빛 황갈 장화).
     - 얼굴·체형: 통통한 볼, 순한 눈, 밝은 주둥이.
     - 자세: 정면에서 약간 오른쪽을 보고 선다. 두 발은 바닥선, 빈손.
     - 규격: 512×768(게임) / 1024×1536(원본). 머리 상자(귀 끝~턱)와 아바타 상자를 표시한다.
     - 표시 키: 기존 곰 기준인 입구 230px·광장 253px(`G/room13_acting.rpy:192·201`)를 유지한다. 생활 동작 0.69 비율이 이 키에 맞춰져 있다.
     - 학교 뒷줄은 책상 뒤라서 상반신만 보인다. 재킷 윗부분과 얼굴이 맞으면 충분하다.
   - 회의 착석 1장(trial 원탁)
     - `room13-meeting-seated-resident_bori068.webp`를 대체한다. 같은 복장으로 의자에 오른쪽 사선으로 앉는다.
     - 손은 무릎, 발은 바닥. 1024×1536 캔버스.
   - 표정: 공용 neutral(순한 미소)이면 배급 누명 장면(bundle3:126-)에서 어색하다. anxious 1장은 선택 사항.
   - 재사용: latest-0 원화(복장·얼굴 기준), 기존 seated 구도(`room13-meeting-seated-resident_bori068.webp`)

## 15. 여니 (resident_yeoni) — current-fd96678

1. **선택 이미지**: 주황 여우 여성. 노란 목도리, 검정 재킷, 크로스 가방, 짙은 바지, 장화.
2. **현재 설정**: `N:113` `"species": "fox"`. 의복 수선과 물자 교환. `G/systems/room13_testimony.rpy:13` J11 "까로에게 들은 말이고"
3. **충돌**: 없음.
4. **적용 상태**: 대화·조사·프로필 모두 `room13-redesign-resident_yeoni.webp`(candidate_fox_town)로 선택 그림과 같다. 광장 벤치 `living_mend`(같은 복장 확인).
5. **분류**: ① 이미 적용된 redesign과 같다.

## 16. 콩이 (resident_kongi) — `remodel-resident_kongi` (사용자 대표 선택)

1. **선택 이미지**: 황금색 처진귀 강아지 남자아이. 빨간 목도리, 청록 재킷, 배낭, 회중시계, 갈색 반바지, 장화. 현재 그림과 같은 디자인이다. 차이는 머리를 3/4로 돌린 것, 다리가 조금 길어진 것, 얼굴 선이 조금 더 또렷해진 것이다.
2. **현재 설정**
   - `N:266` `"species": "dog"`
   - `G/room13-content.json:8208` "가게 심부름과 동네 길 안내"
   - :8249 "킁. 아무리 봐도 제가 아는 건 없어요."
   - 아이: openings:590 "이름이 뭐니?"
   - `N` refuses_when "시계를 잘 못 본다는 이유로 무시"(회중시계 소품과 잘 맞는다)
3. **충돌**: 없음.
4. **적용 상태(모두 기존 판)**
   - 대화 전신 `room13-fullbody-resident_kongi-{6}.webp`
   - portraits `room13-pixel-dialogue-support-03.webp`
   - 조사 `room13-pixel-acting-resident_kongi.webp`
   - 아바타 support-0
   - 회의 착석 kongi068
   - 수정본은 게임에 없다.
5. **분류**: ③(경미)
6. **제작 명세**
   - 대화: 수정본 원화를 neutral로 쓴다. 다른 5표정이 기존 판(정면 머리)으로 남으면 표정이 바뀔 때 머리 각도가 튄다. 둘 중 하나를 고른다.
     - (a) 수정본을 6표정 공용으로 쓰기
     - (b) 수정본 구도로 5표정 추가 요청
   - 조사·회의 착석·아바타는 디자인이 같으므로 기존 파일을 유지해도 된다(권장). 이 경우 두 판이 섞인다는 점만 기록한다.

---

## 요약표

| 배역 | 분류 | 핵심 한 줄 |
|---|---|---|
| 다람 | ① | 지금 게임 그림과 같다 |
| 아빠 | ① | 지금 게임 그림과 같다 |
| 엄마 | ① | 지금 게임 그림과 같다 |
| 부리 | ③ | 갈색 부엉이 미적용. 조사 2동작·공구함·착석·깜빡임 효과를 다시 만들어야 한다. 부엉이 할아버지와 머리가 비슷한 점 주의 |
| 할머니 | ① | redesign v2로 이미 적용됨 |
| 세련 | ① | 지금 게임 그림과 같다 |
| 나비 | ① | 지금 게임 그림과 같다 |
| 도토 | ④ + ② + ③ | 꼬마 사슴과 사건 어른 역할(지렛대 room13.rpy:563, "도토 씨" :571, E33·E11·J10·J17)이 충돌. 아이로 확정할지 사용자 결정 필요 |
| 까로 | ① | 현재 그림 유지. 장갑 서술과도 맞음. 흰 독수리 흔적 없음 |
| 너울 | ③ (+② 선택) | 경비 책임자 어른 남성이라 기능 충돌 없음. 흰 가운이 의사로 읽힐 수 있고, REACT 목록 확인 필요. 2동작 다시 제작 |
| 돌목 | ① | 지금 게임 그림과 같다 |
| 밤이 | ① | 지금 게임 그림과 같다 |
| 토리 | ① | 현재 유지. 대화·조사·벤치·착석 모두 같은 디자인 |
| 보리 | ①(+③ 선택) | revision30: latest-0 곰 생활 동작은 이미 적용(living_firewood). 대화·서 있는 그림·착석은 redesign 곰이라 재킷 재질·얼굴 인상이 다름. 통일하려면 서 있는 기본 1장 + 착석 1장 |
| 여니 | ① | redesign으로 이미 적용됨 |
| 콩이 | ③(경미) | 같은 디자인의 수정본 미적용. 표정 세트 머리 각도 정리만 필요 |

분류별 개수(한 배역이 여러 분류에 들 수 있음)
- ① 12명: 다람·아빠·엄마·할머니·세련·나비·까로·돌목·밤이·토리·보리·여니
- ② 2명: 도토·너울(선택)
- ③ 5명: 부리·도토·너울·콩이, 보리(선택: 외형 통일)
- ④ 1명: 도토
