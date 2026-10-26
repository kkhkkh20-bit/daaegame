# 2026-10-25 소유자 승인: 조각을 대조한 진엔딩 판의 선택 정비실.
# 정답·진엔딩 자격은 바꾸지 않는다. 배경·물건 그림은 systems/room13_hidden_art.rpy(2026-10-26 납품).
init 324 python:
    def r13_hidden_base_value(key):
        return r13_v111_value('hidden_base:'+key)

    def r13_hidden_base_parts_ready():
        return all(r13_hidden_base_value(k) is True for k in ('paper','plate','marks_copied'))

    def r13_hidden_base_ready():
        return (r13_v111_value('ending14')=='true' and r13_hidden_base_parts_ready()
            and not r13_hidden_base_value('finished'))

    def r13_hidden_base_remember_return():
        if r13_hidden_base_value('return_context') is None:
            r13_v111_set('hidden_base:return_context',dict(location=store.room13['location'],
                period=store.room13['period'],people=list(store.room13['v111'].get('people') or []),
                gate=store.room13['v111'].get('gate',''),elapsed=r13_v111_value('elapsed_minutes') or 0))

    def r13_hidden_base_restore_return():
        context=r13_hidden_base_value('return_context')
        if not context:return
        r13_edit(location=context['location'],period=context['period'])
        r13_v111_set('elapsed_minutes',context['elapsed'])
        r13_v111_arrive(context['people'])
        r13_v111_context(context['gate'])
        r13_v111_set('hidden_base:return_context',None)

    # 명시 index는 공용 binding 함수에서 보존한다. 기존 0.. 선택 순서는 그대로다.

    R13_PLACES['hidden_base14']=('옛 시설 정비실',R13_PLACES['ancient'][1])
    R13_MAP_LABELS['hidden_base14']='옛 시설 정비실'
    R13_V111_MAP_ALIASES['hidden_base14']='facility'
    _hb_node=winter_copy.deepcopy(R13_CARTOGRAPHY['regions']['mountain']['nodes']['facility'])
    _hb_node['art_key']='facility'
    R13_CARTOGRAPHY['regions']['mountain']['nodes']['hidden_base14']=_hb_node
    R13_MAP_NODES['mountain']['hidden_base14']=winter_copy.deepcopy(R13_MAP_NODES['mountain']['facility'])
    R13_WORLD_LAYOUTS['hidden_base14']=winter_copy.deepcopy(R13_WORLD_LAYOUTS['ancient'])
    if 'ancient' in R13_FIELD_ZOOM:R13_FIELD_ZOOM['hidden_base14']=R13_FIELD_ZOOM['ancient']
    ROOM13['objects']['hidden_base14']={}
    for _hb_key,_hb_source,_hb_name in (
        ('hb_door','an_corridor','정비실 문틀'),('hb_section','an_press','누르개 옆 자료'),
        ('hb_incident','an_small_tube','유리관 옆 점검표'),('hb_notebook','an_channel','도랑 옆 수첩')):
        _hb_spec=winter_copy.deepcopy(ROOM13['objects']['ancient'][_hb_source])
        _hb_spec.update(text='',need=[],give=[],flags=[])
        ROOM13['objects']['hidden_base14'][_hb_key]=_hb_spec
        R13_OBJECT_NAMES[_hb_key]=_hb_name


label r13_hidden_base_paper1:
    if r13_hidden_base_value('paper'):
        return
    call r13_lines(r13_nw_block('hidden_base_paper1'),'nw:hidden_base_paper1')
    $ r13_v111_set('hidden_base:paper',True)
    return

label r13_hidden_base_pick7(n):
    if n==100 and not r13_hidden_base_value('plate_seen'):
        call r13_lines(r13_nw_block('hidden_base_plate_seen7'),'nw:hidden_base_plate_seen7')
        $ r13_v111_set('hidden_base:plate_seen',True)
    elif n==101 and r13_hidden_base_value('plate_seen') and not r13_hidden_base_value('plate'):
        call r13_lines(r13_nw_block('hidden_base_plate7'),'nw:hidden_base_plate7')
        $ r13_v111_set('hidden_base:plate',True)
    return

label r13_hidden_base_marks11:
    if not (r13_hidden_base_value('paper') and r13_hidden_base_value('plate')) or r13_hidden_base_value('marks_copied'):
        return
    call r13_lines(r13_nw_block('hidden_base_marks11'),'nw:hidden_base_marks11')
    $ r13_v111_set('hidden_base:marks_copied',True)
    return

label r13_hidden_base14:
    if not r13_hidden_base_ready():
        return
    $ r13_hidden_base_remember_return()
    $ r13_edit(location='school',period=2)
    $ r13_v111_arrive(['mom','daram'])
    call r13_lines(r13_nw_block('hidden_base_offer14'),'nw:hidden_base_offer14')
    call r13_v111_wait('hidden_base_offer14')
    $ r13_v111_talk_person=None
    if _return!=0:
        $ r13_v111_set('hidden_base:finished',True)
        $ r13_hidden_base_restore_return()
        return
    $ r13_v111_set('hidden_base:entered',True)
    $ r13_edit(location='hidden_base14',period=2)
    $ room13['v111']['people']=[]
    call r13_scene(R13_PLACES['hidden_base14'][1],'옛 시설 정비실','quiet')
    $ r13_v111_arrive(['mom','daram'])
    call r13_lines(r13_nw_block('hidden_base_arrival14'),'nw:hidden_base_arrival14')
    if r13_hidden_base_value('opened'):
        jump r13_hidden_base_room14

label r13_hidden_base_door14:
    call r13_v111_wait('hidden_base_door14')
    if _return==0:
        call r13_lines(r13_nw_block('hidden_base_frame14'),'nw:hidden_base_frame14')
        $ r13_v111_set('hidden_base:frame_seen',True)
    elif _return==1:
        call r13_lines(r13_nw_block('hidden_base_paper_set14'),'nw:hidden_base_paper_set14')
        $ r13_v111_set('hidden_base:paper_set',True)
    elif _return==2:
        call r13_lines(r13_nw_block('hidden_base_plate_right14'),'nw:hidden_base_plate_right14')
        $ r13_v111_set('hidden_base:aligned',True)
    elif _return==3:
        call r13_lines(r13_nw_block('hidden_base_plate_wrong14'),'nw:hidden_base_plate_wrong14')
        $ r13_v111_set('hidden_base:aligned',False)
    elif _return==4:
        if r13_hidden_base_value('aligned'):
            # 2026-10-26 열린 문 그림: 문이 열리는 줄에서 그림도 열려 있게 대사보다 먼저 세운다.
            $ r13_v111_set('hidden_base:opened',True)
            call r13_lines(r13_nw_block('hidden_base_open14'),'nw:hidden_base_open14')
            jump r13_hidden_base_room14
        call r13_lines(r13_nw_block('hidden_base_stuck14'),'nw:hidden_base_stuck14')
    elif _return==5:
        jump r13_hidden_base_return14
    jump r13_hidden_base_door14

label r13_hidden_base_room14:
    call r13_v111_wait('hidden_base_room14')
    if _return==0:
        call r13_lines(r13_nw_block('hidden_base_section14'),'nw:hidden_base_section14')
        $ r13_v111_set('hidden_base:read_section',True)
    elif _return==1:
        call r13_lines(r13_nw_block('hidden_base_incident14'),'nw:hidden_base_incident14')
        $ r13_v111_set('hidden_base:read_incident',True)
    elif _return==2:
        if not r13_hidden_base_value('notebook_taken'):
            call r13_lines(r13_nw_block('hidden_base_notebook14'),'nw:hidden_base_notebook14')
            $ r13_v111_set('hidden_base:notebook_taken',True)
        else:
            call r13_lines(r13_nw_block('hidden_base_notebook_kept14'),'nw:hidden_base_notebook_kept14')
    elif _return==3:
        jump r13_hidden_base_return14
    jump r13_hidden_base_room14

label r13_hidden_base_return14:
    if r13_hidden_base_value('opened') and not r13_hidden_base_value('notebook_taken'):
        call r13_lines(r13_nw_block('hidden_base_notebook14'),'nw:hidden_base_notebook14')
        $ r13_v111_set('hidden_base:notebook_taken',True)
    call r13_lines(r13_nw_block('hidden_base_return14'),'nw:hidden_base_return14')
    $ r13_v111_set('hidden_base:returned',True)
    $ r13_v111_set('hidden_base:finished',True)
    $ r13_hidden_base_restore_return()
    $ r13_v111_talk_person=None
    call r13_scene(R13_PLACES[room13['location']][1],R13_PLACES[room13['location']][0],'calm')
    return
