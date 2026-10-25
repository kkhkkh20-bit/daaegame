# 2026-10-25 부엉이 예방 1단계(docs/design/OWL_PREVENTION_DESIGN.md 9장 「물건을 몰래 옮겨 미래를 바꾼다」, 7장 1단계).
# 소유자 승인: 7일 A/B/C 메뉴를 걷는다. 첫 판의 자연스러운 흐름은 살인 → 8~10일 13호 회의(본 게임)다.
# 예방은 미래를 아는 사람만 하는 보너스로, 7일 낮 자유 시간의 현장 조사(기존 field-bindings 방식)로만 한다.
#   ① 난로 돌: 공방에서 집게를 빌린다 → 13호 난로의 검푸른 돌을 꺼내 눈에 묻는다(재받이의 배급 돌을 대신 넣을 수도 있다).
#   ② 도토의 다짐: 여관 복도에서 「아래서 누가 부르면」을 물어 다짐을 받는다 → 거짓 부름에 내려가지 않는다.
# 표시·권유가 없고, 결과를 알리는 특별한 대사 없이 그 밤 일이 그냥 일어나지 않는다.
# 새 사실(설계 문서 범위 안): 할머니는 7일 아침 도토가 13호 돌을 간 뒤 그 배급 돌을 꺼내 재받이에 묻고 안쪽 돌을 넣었다.
# 보고: docs/reviews/owl-prevention-20261024/적용보고.md
init 322 python:
    # 13호 그림에는 난로가 그려져 있지 않다(전용 그림 필요). 책장과 화분 사이 빈 벽에 조사 자리만 둔다.
    # 오른쪽 끝으로 밀었을 때 오른쪽 아래 조작 버튼(새 생각·기록)에 가리지 않는 높이다.
    # 글이 빈 물건은 그 단계의 선택이 있을 때만 눌린다(7일 낮 자유 시간에만).
    ROOM13["objects"].setdefault("room13",{})["v111_stove"]=dict(rect=[1820,250,170,190],need=[],give=[],flags=[],text="")
    ROOM13["objects"]["room13"]["v111_ashbin"]=dict(rect=[1830,445,100,60],need=[],give=[],flags=[],text="")
    R13_OBJECT_NAMES.update(v111_stove="난로",v111_ashbin="재받이")

# ---------------------------------------------------------------- 5일 밤 (결정 11: 과자 봉지)
label r13_v111_snack_plate5:
    call r13_lines(r13_nw_block('snack_plate5'),'nw:snack_plate5')
    $ r13_v111_set('snack_bagged5',True)
    return

# ---------------------------------------------------------------- 7일 낮 자유 시간
label r13_v111_free_day7:
    $ r13_edit(period=1)
    call r13_lines(r13_nw_block('free_open7'),'nw:free_open7')
    # 도토는 여관으로 먼저 돌아갔다. 학교 무대에는 나비·선생님·다람이 남는다.
    $ r13_v111_arrive(['nabi','resident_teacher','daram'])
label r13_v111_free_day7_wait:
    call r13_v111_wait('free_day7')
    if _return==0:
        jump r13_v111_free_evening7
    call r13_v111_free_day7_pick(_return)
    jump r13_v111_free_day7_wait

# 대기 화면이 돌려준 번호(field-bindings.json free_day7 의 선택 차례)로 한 가지 행동을 한다.
label r13_v111_free_day7_pick(n):
    if n==1:
        call r13_lines(r13_nw_block('doto_basket7'),'nw:doto_basket7')
    elif n==2:
        call r13_lines(r13_nw_block('doto_promise7'),'nw:doto_promise7')
        $ r13_v111_set('doto_promise7',True)
    elif n==3:
        call r13_lines(r13_nw_block('stove_look7'),'nw:stove_look7')
    elif n==4:
        call r13_lines(r13_nw_block('ashbin7'),'nw:ashbin7')
        $ r13_v111_set('pocket_ration7',True)
    elif n==5:
        call r13_lines(r13_nw_block('stove_swap7'),'nw:stove_swap7')
        $ r13_v111_set('pocket_ration7',False)
        $ r13_v111_set('stove13_7','ration')
        $ r13_nw_acquire("NW_STONE","swapped")
    elif n==6:
        call r13_lines(r13_nw_block('buri_tongs7'),'nw:buri_tongs7')
        $ r13_v111_set('tongs7',True)
    elif n==7:
        call r13_lines(r13_nw_block('stove_hide7'),'nw:stove_hide7')
        $ r13_v111_set('stove13_7','empty')
        $ r13_nw_acquire("NW_STONE","swapped")
    return

label r13_v111_free_evening7:
    call r13_lines(r13_nw_block('free_evening7'),'nw:free_evening7')
    jump r13_v111_room_visit7

# ---------------------------------------------------------------- 7일 저녁 13호
# 돌을 꺼낸 판: 부엉이가 무너지지 않는다. 의료진을 부를 일이 없으니 할머니의 틈도 없다.
# 할머니의 동기는 남는다 — 난로를 들여다보고(7일), 8일 너울에게 「같은 말을 두 번 묻는 노인」이라 이른다.
label r13_v111_owl_well7:
    call r13_lines(r13_nw_block('owl_well7'),'nw:owl_well7')
    $ r13_v111_set('route7','prevented')
    $ r13_v111_set('prevention','stone')
    $ r13_v111_set('choice:MS14_D07_S03','stone')
    $ r13_fork_set_fate('fate_owl','stone')
    $ r13_v111_set('OWL_ALIVE',True)
    $ r13_v111_set('DARAM_DETAINED',False)
    $ r13_v111_set('D07_medical_care','none')
    jump r13_v111_sleep7

# 다짐만 받은 판: 부엉이는 무너지고 아빠는 서리를 부르러 간다(다람은 걷지 못해 도토에게 맡긴다).
# 계단 아래 거짓 부름에 도토가 내려가지 않아 할머니는 돌아간다. 돌은 밤새 남고 8일 서리가 꺼낸다(예전 B 판과 같다).
label r13_v111_promise_night7:
    # 살인 판과 같은 이동(지도로 진료소). 갈림은 돌아온 뒤에야 보인다.
    call r13_v111_travel('clinic','incident7',[])
    $ r13_v111_arrive(['karo','resident_seori'])
    call r13_lines(r13_nw_block('promise_clinic7'),'nw:promise_clinic7')
    call r13_v111_travel('room13','promise_room7',[],True)
    $ r13_v111_arrive(['daram','doto','resident_owlgp','resident_seori','karo'])
    call r13_lines(r13_nw_block('promise_room7'),'nw:promise_room7')
    $ r13_v111_set('route7','prevented')
    $ r13_v111_set('prevention','promise')
    $ r13_v111_set('choice:MS14_D07_S03','promise')
    $ r13_fork_set_fate('fate_owl','promise')
    $ r13_v111_set('OWL_ALIVE',True)
    $ r13_v111_set('DARAM_DETAINED',False)
    $ r13_v111_set('D07_medical_care','complete')
    jump r13_v111_sleep7

# ---------------------------------------------------------------- 8일 아침 (돌을 꺼낸 판)
label r13_v111_owl_well8:
    call r13_lines(r13_nw_block('owl_well8'),'nw:owl_well8')
    jump r13_v111_missing_pages8
