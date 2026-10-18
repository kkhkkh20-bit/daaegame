# 추천 조합 회차 플러그인 API v1 · 2026-10-18

통합 소유자: implement_selected_story_routes. 다른 구현자는 공용 screens.rpy, room13_recommended_story.rpy, dev/recommended_model.py를 수정하지 않는다.

## 파일과 init
- game/systems/room13_recommended_ep23.rpy 또는 room13_recommended_ep456.rpy.
- init 910 python: 으로 등록한다. 공용 기반은 init900이다.
- 독립 단위검사를 위해 dev/recommended_ep23_model.py 등의 순수 Python 원본과 시험도 제공한다. 외부 파일을 게임 런타임에 import하지 말고 rpy 안에 동일 소스를 포함한다.
- prefix r13_rec_e2_, e3_, e4_, e5_, e6_ 사용. label은 r13_recommended_ep2_hearing 등.

## 저장
r13_recommended = dict(revision, episode=1, day=2, done=[], facts=[], observed={}, mother='M0', piko='outside', nabi='working', hearing=0, verdict=None, selected=[], log=[], episodes={})
- done: 실제 실행한 action id와 획득한 플래그. e2_*, e3_* 이름을 사용한다.
- facts: 획득한 카드 id. e2_card_* 등 이름을 사용한다.
- observed: 카드 id→직접 확인/듣기 수행 날짜. 카드 본문에는 관찰 사실이 발생한 날짜·장소·직접/전언을 분리한다.
- episodes: 회차별 상태. episodes['2'] 등 아래 독립 dict, 회의 단계·사건결과를 넣는다.
- mother(M0/M1/M2), piko(outside/sheltered/safe/dead), nabi(working/supervised_relief)는 상위 공유. 후속에서 낮은 단계로 되돌리지 않는다.
- 추가 상위 공통: neoul='active'/'detained', daram='with_parent'/'protected_wait', e3_school_handoff=False, e4_lever_blocked=False, e5_poison_blocked=False. 기본값은 신규 state에서 제공 예정.
- 모든 변경은 deepcopy 후 새 dict 반환. 함수에서 store/global 저장 상태를 직접 바꾸지 않는다.

## 등록할 자료
r13_rec_cards.update({'e2_card_x':('표제','알고 있는 사실 및 한계')})
r13_rec_actions.update({'e2_action_x': r13_rec_action(title, place, lines, need=(), forbid=(), give=(), flags=(), day=None, episode=2, background_key=None, label=None)})
- place는 기존 R13_PLACES 키만. 기존에 없는 관찰 그림은 새 설정/미제작 여부를 표시한다. 별도 scene background 필요 시 r13_rec_backgrounds[place]=(title,existing_background_key) 등록.
- lines는 [(speaker,text), ...]. 기존 R13_CHARS의 speaker id만 사용, 미등장 아이는 내레이션으로 기록하지 말고 실제 등록된 이름과 인물카드를 확인하라.
- need/forbid는 done 플래그만. 카드가 있어야 열리면 그 카드와 함께 주는 실제 관찰 플래그를 사용한다.
- action은 반복 실행 불가. 멱등적 반복을 원하면 별도 회의/현장 label에서 처리한다.
- day=None이면 해당 episode 내 날짜에서 허용; 정수면 그 날짜에만 허용.
- episode=0은 가족 행동처럼 여러 회차에 남는 독립 행동. 에피소드별 제작자는 2~6만 사용한다.
- r13_rec_effects['e2_action_x']=pure_function(state)->new_state: 대사 정상 반환 뒤 give/flags/done가 적용된 상태를 받는다. 예방완료/결과 등에 사용.

## 회차 등록
r13_rec_episodes[2] = dict(title='밤이 C', start_day=4, end_day=5, hearing_label='r13_recommended_ep2_hearing', next_label=None)
- r13_rec_episode_start[2]=pure_function(state)->new_state: 회차 진입 때 공유상태 유지, episode=2/day=4/episodes['2'] 초기화를 담당.
- r13_rec_day_advance[2]=pure_function(state)->new_state: 날짜 진행, 실제 발생/예방 결과를 처리.
- r13_rec_advance_block[2]=pure_function(state)->str_or_None: 진행을 막을 필수 현장 행동이 있으면 짧은 이유. 전수 수집이나 예방 선택을 강제하지 않는다.
- r13_rec_episode_done[2]=pure_function(state)->bool: 다음 회차 버튼 활성 조건. 실명 범인 확정이 안 된 부분 결론도 정직하게 기록하고 진행 가능해야 한다.
- 제작자는 회차 전환 시 r13_rec_episode_start 호출과 다음 회차 버튼을 직접 구현하지 않는다. 공용 hub가 등록한 순서대로 전환한다.

## 공용 화면/표시 label
- call r13_scene(background_key,title,mood)
- call r13_lines(lines,'recommended:e2:unique-id')
- call screen r13_recommended_cards(question) → _return=획득 card id 또는 None(현장으로 돌아감).
- 회의 label의 모든 종료/중단 경로는 jump r13_recommended_hub.
- 공용 r13_recommended_actions가 해당 episode action, 보유 카드, 날짜 진행, 회의, 다음 회차 버튼을 렌더한다.
- 기존 room13의 증거·범인·NPC 지식·자동일정 함수 호출 금지. 공유 렌더러의 읽음 기록 외에 기존 이야기 사실을 재사용하지 않는다.

## 진짜 입력과 검증
회차는 조사→실제 관찰→획득 카드→제시/반박→결과→후속가용성을 구현한다. 카드 정답표만으로 끝내지 않는다. 잘못된 카드·조기 질문·생존/사망·예방 성공·M2·너울 구금 조합과 날짜/장소를 회귀검사한다. 기존 API에 없는 기능이 필요하면 임의 우회 말고 통합 담당에게 알린다.

## 범위 분담 제안
- ep23 담당: 밤이C(결박→요구→물림 선후, 돌목 책임)와 화재A(누비 통 왕복, 실제 시야 겹침, E3 학교 인계). 이동 지도는 현재아트 검수 전이면 확정범위 제한을 명시하고 진행한다.
- ep456 담당: 13호A(7일 감금/구조방해 사망과9일 별개, 너울 구금), 수프B(사전 약장/혼입 예방), 최종C(명단과 실제배급·남은사람, 실제 하루 생존 자원). 서로 넓으면 두 구현자로 나눈다.

## 선택적 현장 interaction
background_key는 그 action의 실제 기존 배경을 직접 선택한다. label이 있으면 hub가 lines 뒤 call expression하고, return False면 취소로 간주하여 flags/give/effects를 적용하지 않는다. 완료는 return True. 현장 입력을 성공해야만 물증 획득시킬 때 쓴다.

## 장소명/기본배경 override
r13_rec_location_overrides[episode] = function(state,location) → (title,background_key) 또는 None. field/map/action 기본배경 모두 이 callback을 우선하고 명시 action background_key는 그보다 우선한다. 예: store를 장작창고로 쓰는 ep3은 기존 공동물품창고 이름을 그대로 내보내지 않는다.
