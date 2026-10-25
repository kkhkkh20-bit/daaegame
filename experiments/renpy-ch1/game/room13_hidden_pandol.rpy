# 승인 2026-10-25: 판돌의 누나, 식기 수리·난방 교체·실제 돌봄 인계.
# 전용 그림 납품 전: 기존 실내 배경만 임시 사용하며 누나는 지문 속 목소리로 표현한다.
init 324 python:
    def r13_hp_value(key):
        return r13_v111_value('hidden_pandol:'+key)
    def r13_hp_set(key,value=True):
        r13_v111_set('hidden_pandol:'+key,value)
    def r13_hp_heat_ready():
        return (r13_v111_value('meeting:hypothesis')=='win' and all(r13_hp_value(k) for k in ('family_seen','stove_seen','consent','wood_delivered','tongs')) and not r13_hp_value('heat_replaced'))
    def r13_hp_wood_ready():
        return bool(r13_hp_value('family_seen') and r13_v111_value('meeting:hypothesis')=='win' and r13_v111_value('school_supply_handed'))
    def r13_hp_receiver_ready():
        return (r13_hp_value('heat_replaced') and not r13_hp_value('care_handed') and not r13_v111_value('departed:npc_pandol') and not r13_v111_value('departed:nabi') and not r13_v111_value('listed:nabi') and r13_v111_value('alive:nabi') is not False)

    R13_PLACES['hidden_pandol']=('판돌 집','ms14_somi_inside')
    R13_WORLD_LAYOUTS['hidden_pandol']=winter_copy.deepcopy(R13_WORLD_LAYOUTS['ms14_somi_inside'])
    ROOM13['objects']['hidden_pandol']={
        'hp_table':dict(rect=[500,420,260,160],need=[],give=[],flags=[],text='문 옆의 식기 쟁반'),
        'hp_stove':dict(rect=[1400,290,220,230],need=[],give=[],flags=[],text='집 안쪽 난로'),
        'hp_wood':dict(rect=[1090,480,220,170],need=[],give=[],flags=[],text='장작을 놓는 상자'),
        'hp_tongs':dict(rect=[1660,330,100,170],need=[],give=[],flags=[],text='벽에 걸린 집게'),
    }
    R13_OBJECT_NAMES.update(hp_table='식기 쟁반',hp_stove='난로',hp_wood='장작 상자',hp_tongs='집게')
    R13_MAP_LABELS['hidden_pandol']='판돌 집'
    R13_V111_MAP_ALIASES['hidden_pandol']='somi'
    _hp_node=winter_copy.deepcopy(R13_CARTOGRAPHY['regions']['village']['nodes']['somi'])
    _hp_node['art_key']='somi'
    R13_CARTOGRAPHY['regions']['village']['nodes']['hidden_pandol']=_hp_node
    R13_MAP_NODES['village']['hidden_pandol']=R13_MAP_NODES['village']['somi']


label r13_hp_meal6:
    $ r13_v111_join(['npc_pandol','daram','nabi'])
label r13_hp_meal6_wait:
    call r13_v111_wait('hp_meal6')
    if _return==0:
        return
    if _return==1:
        call r13_lines(r13_nw_block('hp_spoon6'),'nw:hp_spoon6')
        $ r13_hp_set('spoon_seen')
    elif _return==2:
        call r13_lines(r13_nw_block('hp_meet6'),'nw:hp_meet6')
        $ r13_hp_set('met')
    jump r13_hp_meal6_wait

label r13_hp_pick7(n):
    if n==80 and r13_hp_value('spoon_seen') and not r13_hp_value('pin_seen'):
        call r13_lines(r13_nw_block('hp_pin7'),'nw:hp_pin7')
        $ r13_hp_set('pin_seen')
    elif n==81 and r13_hp_value('met') and r13_hp_value('pin_seen') and not r13_hp_value('pin_fitted'):
        call r13_lines(r13_nw_block('hp_fit7'),'nw:hp_fit7')
        $ r13_hp_set('pin_fitted')
    elif n==82 and r13_hp_value('pin_fitted') and not r13_hp_value('visit_allowed'):
        $ r13_v111_arrive(['npc_pandol'])
        call r13_lines(r13_nw_block('hp_permit7'),'nw:hp_permit7')
        $ r13_hp_set('visit_allowed')
    elif n==83 and r13_hp_value('visit_allowed') and not r13_hp_value('family_seen'):
        $ r13_v111_arrive(['npc_pandol'])
        call r13_lines(r13_nw_block('hp_discover7'),'nw:hp_discover7')
        $ r13_hp_set('family_seen')
    elif n==84 and r13_hp_value('family_seen'):
        call r13_lines(r13_nw_block('hp_house7'),'nw:hp_house7')
    return

label r13_hp_wood11:
    if not r13_hp_wood_ready():
        call r13_lines(r13_nw_block('hp_no_wood11'),'nw:hp_no_wood11')
        return
    if not r13_hp_value('wood_reserved'):
        $ r13_v111_join(['resident_teacher'])
        call r13_lines(r13_nw_block('hp_wood11'),'nw:hp_wood11')
        $ r13_hp_set('wood_reserved')
    return

label r13_hp_visit11:
    if not r13_hp_value('family_seen') or r13_v111_value('meeting:hypothesis')!='win':
        return
    $ hp_return=(room13['location'],room13['period'],list(room13['v111'].get('people',[])))
    $ r13_v111_talk_person=None
    call r13_v111_travel('hidden_pandol','hp_visit11',[],True)
    $ r13_v111_arrive(['npc_pandol'])
    call r13_lines(r13_nw_block('hp_visit11'),'nw:hp_visit11')
label r13_hp_house11_wait:
    call r13_v111_wait('hp_house11')
    if _return==0:
        $ r13_edit(location=hp_return[0],period=hp_return[1])
        $ r13_v111_arrive(hp_return[2])
        $ r13_v111_talk_person=None
        call r13_scene(R13_PLACES[room13['location']][1],R13_PLACES[room13['location']][0],'night')
        return
    call r13_hp_house11_pick(_return)
    jump r13_hp_house11_wait

label r13_hp_house11_pick(n):
    if n==1 and not r13_hp_value('stove_seen'):
        call r13_lines(r13_nw_block('hp_look11'),'nw:hp_look11')
        $ r13_hp_set('stove_seen')
    elif n==2 and r13_hp_value('wood_reserved') and r13_hp_value('stove_seen') and not r13_hp_value('consent'):
        call r13_lines(r13_nw_block('hp_consent11'),'nw:hp_consent11')
        $ r13_hp_set('consent')
    elif n==3 and r13_hp_value('consent') and not r13_hp_value('wood_delivered'):
        call r13_lines(r13_nw_block('hp_place11'),'nw:hp_place11')
        $ r13_hp_set('wood_delivered')
    elif n==4 and r13_hp_heat_ready():
        call r13_lines(r13_nw_block('hp_replace11'),'nw:hp_replace11')
        $ r13_hp_set('heat_replaced')
    elif n==5 and r13_hp_value('stove_seen') and not r13_hp_value('tongs'):
        call r13_lines(r13_nw_block('hp_tongs11'),'nw:hp_tongs11')
        $ r13_hp_set('tongs')
    return

label r13_hp_handoff13:
    if not r13_hp_value('heat_replaced') or r13_hp_value('care_handed') or r13_v111_value('departed:npc_pandol'):
        return
    $ r13_v111_join(['npc_pandol'])
    call r13_lines(r13_nw_block('hp_handoff_open13'),'nw:hp_handoff_open13')
    if not r13_hp_receiver_ready():
        call r13_lines(r13_nw_block('hp_handoff_missing13'),'nw:hp_handoff_missing13')
        return
    $ r13_v111_join(['nabi'])
    call r13_lines(r13_nw_block('hp_handoff13'),'nw:hp_handoff13')
    $ r13_hp_set('care_handed')
    $ r13_hp_set('care_person','nabi')
    $ r13_hp_set('care_location','school')
    return

label r13_hidden_idle:
    call r13_lines(r13_nw_block('hidden_idle'),'nw:hidden_idle')
    return
