# Native Room13 story labels. Generated from reviewed source IDs; no runtime route interpreter.
label r13_v111_start:
    $ room13["v111"]=dict(version="1.1.1",values=winter_copy.deepcopy(R13_V111["initial"]),gate="",people=["daram"])
    $ ms14=None; r13_flag("lodging"); r13_carriage_skip=False
    call r13_carriage_departure
    jump r13_v111_start_block

label r13_v111_start_block:
    $ r13_v111_scene('MS14_D01_S01')
    $ r13_v111_score()
    call r13_lines([('daram','아빠, 숲이 아직 깜깜해.',{'no_lead':True}),('dad','조금 있으면 날이 밝을 거야.',{'no_lead':True}),('daram','엄마는 벌써 일어났을까?',{'no_lead':True}),('dad','만나면 물어보자.',{'no_lead':True})], 'v111:carriage:before-bump')
    call r13_lines(r13_v111_lines(['MS14_D01_S01_L0001', 'MS14_D01_S01_L0002', 'MS14_D01_S01_L0003', 'MS14_D01_S01_L0004', 'MS14_D01_S01_L0005', 'MS14_D01_S01_L0006', 'MS14_D01_S01_L0007', 'MS14_D01_S01_L0008', 'MS14_D01_S01_L0009']), 'v111:start:MS14_D01_S01_L0002')
    jump r13_v111_letter_open

label r13_v111_letter_open:
    $ v111_answer=0
    if v111_answer==0:
        jump r13_v111_letter_read
    jump r13_v111_letter_open

label r13_v111_letter_read:
    $ r13_v111_scene('MS14_D01_S01')
    call r13_v111_travel('gate','letter_read')
    $ r13_v111_score()
    $ r13_v111_commit('MS14_D01_S01_L0010')
    call r13_lines(r13_v111_lines(['MS14_D01_S01_L9101', 'MS14_D01_S01_L0011', 'MS14_D01_S01_L0012', 'MS14_D01_S01_L0013', 'MS14_D01_S01_L0014']), 'v111:letter_read:MS14_D01_S01_L9101')
    jump r13_v111_letter_menu

label r13_v111_letter_menu:
    $ v111_menu_owner='letter_menu'
    $ v111_menu=[('마지막 줄을 본다',0) for _ in [0] if True] + [('글씨를 살핀다',1) for _ in [0] if True] + [('편지를 접는다',2) for _ in [0] if True]
    $ v111_answer=renpy.display_menu(v111_menu)
    if v111_answer==0:
        $ r13_v111_option('MS14_D01_S01_L0014_O1')
        jump r13_v111_letter_last
    if v111_answer==1:
        $ r13_v111_option('MS14_D01_S01_L0014_O2')
        jump r13_v111_letter_hand
    if v111_answer==2:
        $ r13_v111_option('MS14_D01_S01_L0014_O3')
        jump r13_v111_letter_close
    jump r13_v111_letter_menu

label r13_v111_letter_last:
    $ r13_v111_scene('MS14_D01_S01')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S01_L0015']), 'v111:letter_last:MS14_D01_S01_L0015')
    $ r13_v111_commit('MS14_D01_S01_L0015')
    jump r13_v111_letter_menu

label r13_v111_letter_hand:
    $ r13_v111_scene('MS14_D01_S01')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S01_L0016']), 'v111:letter_hand:MS14_D01_S01_L0016')
    $ r13_v111_commit('MS14_D01_S01_L0016')
    jump r13_v111_letter_menu

label r13_v111_letter_close:
    if r13_v111_value('K01a')==True:
        jump r13_v111_letter_any
    jump r13_v111_letter_close_b

label r13_v111_letter_close_b:
    if r13_v111_value('K01b')==True:
        jump r13_v111_letter_any
    jump r13_v111_letter_none

label r13_v111_letter_any:
    $ r13_v111_scene('MS14_D01_S01')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S01_L0017']), 'v111:letter_any:MS14_D01_S01_L0017')
    jump r13_v111_carriage_end

label r13_v111_letter_none:
    $ r13_v111_scene('MS14_D01_S01')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S01_L0018']), 'v111:letter_none:MS14_D01_S01_L0018')
    jump r13_v111_carriage_end

label r13_v111_carriage_end:
    $ r13_v111_scene('MS14_D01_S01')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S01_L0019', 'MS14_D01_S01_L0020', 'MS14_D01_S01_L0021', 'MS14_D01_S01_L0022']), 'v111:carriage_end:MS14_D01_S01_L0019')
    jump r13_v111_leave_carriage

label r13_v111_leave_carriage:
    $ v111_answer=0
    if v111_answer==0:
        $ r13_v111_apply('option:leave_carriage:0',[{'op': 'set', 'field': 'carriage_stopped', 'value': True}])
        jump r13_v111_gate_arrival
    jump r13_v111_leave_carriage

label r13_v111_gate_arrival:
    $ r13_v111_scene('MS14_D01_S02')
    call r13_v111_travel('gate','gate_arrival')
    $ r13_v111_score()
    $ r13_carriage_finish(); r13_carriage_skip=False
    call r13_scene("winter","눈에 막힌 입구","calm")
    call r13_lines(r13_v111_lines(['MS14_D01_S02_L0002', 'MS14_D01_S02_L0003', 'MS14_D01_S02_L0005', 'MS14_D01_S02_L0006', 'MS14_D01_S02_L0007', 'MS14_D01_S02_L0009', 'MS14_D01_S02_L0010', 'MS14_D01_S02_L0011', 'MS14_D01_S02_L0012', 'MS14_D01_S02_L0013', 'MS14_D01_S02_L0014', 'MS14_D01_S02_L0015', 'MS14_D01_S02_L0017', 'MS14_D01_S02_L0018']), 'v111:gate_arrival:MS14_D01_S02_L0002')
    jump r13_v111_gate_request

label r13_v111_gate_request:
    call r13_v111_travel('gate','gate_request')
    call r13_v111_wait('gate_request')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_gate_list
    jump r13_v111_gate_request

label r13_v111_gate_list:
    $ r13_v111_scene('MS14_D01_S02')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S02_L0019']), 'v111:gate_list:MS14_D01_S02_L0019')
    $ r13_v111_commit('MS14_D01_S02_L0019')
    call r13_lines(r13_v111_lines(['MS14_D01_S02_L0020', 'MS14_D01_S02_L0021', 'MS14_D01_S02_L0022']), 'v111:gate_list:MS14_D01_S02_L0020')
    jump r13_v111_gate_choice

label r13_v111_gate_choice:
    call r13_v111_travel('gate','gate_choice')
    call r13_v111_wait('gate_choice')
    $ v111_answer=_return
    if v111_answer==0:
        $ r13_v111_option('MS14_D01_S02_L0022_O1')
        jump r13_v111_gate_letter
    if v111_answer==1:
        $ r13_v111_option('MS14_D01_S02_L0022_O2')
        jump r13_v111_gate_original
    jump r13_v111_gate_choice

label r13_v111_gate_letter:
    $ r13_v111_scene('MS14_D01_S02')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S02_L0023', 'MS14_D01_S02_L0024', 'MS14_D01_S02_L0025']), 'v111:gate_letter:MS14_D01_S02_L0023')
    jump r13_v111_gate_original_out

label r13_v111_gate_original:
    $ r13_v111_scene('MS14_D01_S02')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S02_L0026', 'MS14_D01_S02_L0027']), 'v111:gate_original:MS14_D01_S02_L0026')
    jump r13_v111_gate_original_out

label r13_v111_gate_original_out:
    $ r13_v111_scene('MS14_D01_S02')
    $ r13_v111_score()
    jump r13_v111_gate_investigate

label r13_v111_gate_investigate:
    call r13_v111_travel('gate','gate_investigate')
    call r13_v111_wait('gate_investigate')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_gate_read_original
    if v111_answer==1:
        jump r13_v111_gate_read_rules
    if v111_answer==2:
        jump r13_v111_gate_reread_list
    if v111_answer==3:
        $ r13_v111_option('MS14_D01_S03_L0008_O1')
        jump r13_v111_gate_purpose
    if v111_answer==4:
        $ r13_v111_option('MS14_D01_S03_L0008_O2')
        jump r13_v111_gate_lodging
    if v111_answer==5:
        $ r13_v111_option('MS14_D01_S03_L0008_O3')
        jump r13_v111_gate_proof
    if v111_answer==6:
        $ r13_v111_option('MS14_D01_S03_L0008_O4')
        jump r13_v111_gate_hint
    if v111_answer==7:
        $ r13_v111_option('MS14_D01_S03_L0008_O5')
        jump r13_v111_gate_reason
    jump r13_v111_gate_investigate

label r13_v111_gate_read_original:
    $ r13_v111_scene('MS14_D01_S03')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S03_L0002']), 'v111:gate_read_original:MS14_D01_S03_L0002')
    $ r13_v111_commit('MS14_D01_S03_L0002')
    call r13_lines(r13_v111_lines(['MS14_D01_S03_L0003', 'MS14_D01_S03_L0004', 'MS14_D01_S03_L0005', 'MS14_D01_S03_L0006']), 'v111:gate_read_original:MS14_D01_S03_L0003')
    jump r13_v111_gate_investigate

label r13_v111_gate_read_rules:
    $ r13_v111_scene('MS14_D01_S03')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S03_L0007']), 'v111:gate_read_rules:MS14_D01_S03_L0007')
    $ r13_v111_commit('MS14_D01_S03_L0007')
    jump r13_v111_gate_investigate

label r13_v111_gate_reread_list:
    show screen r13_material_corner('V111:E02')
    call r13_lines([(None,ROOM13["evidence"]['V111:E02']["establishes"])],'v111:read:gate_reread_list')
    hide screen r13_material_corner
    jump r13_v111_gate_investigate

label r13_v111_gate_purpose:
    $ r13_v111_scene('MS14_D01_S03')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S03_L0009', 'MS14_D01_S03_L0010', 'MS14_D01_S03_L0011', 'MS14_D01_S03_L0012']), 'v111:gate_purpose:MS14_D01_S03_L0009')
    $ r13_v111_commit('MS14_D01_S03_L0012')
    jump r13_v111_gate_investigate

label r13_v111_gate_lodging:
    $ r13_v111_scene('MS14_D01_S03')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S03_L0013']), 'v111:gate_lodging:MS14_D01_S03_L0013')
    jump r13_v111_gate_investigate

label r13_v111_gate_proof:
    call r13_v111_proof('함께 들어갈 근거를 고른다',['E02', 'E03', 'E04'],'r13_v111_gate_proven_dispatch','r13_v111_gate_wrong','r13_v111_gate_hint')
    jump expression _return

label r13_v111_gate_proven_dispatch:
    if r13_v111_value('purpose_difference_known')==True:
        jump r13_v111_gate_proven
    jump r13_v111_gate_early

label r13_v111_gate_proven:
    $ r13_v111_scene('MS14_D01_S03')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S03_L0014', 'MS14_D01_S03_L0015', 'MS14_D01_S03_L0016', 'MS14_D01_S03_L0017', 'MS14_D01_S03_L0018', 'MS14_D01_S03_L0019']), 'v111:gate_proven:MS14_D01_S03_L0014')
    $ r13_v111_commit('MS14_D01_S03_L0019')
    jump r13_v111_registered

label r13_v111_gate_early:
    $ r13_v111_scene('MS14_D01_S03')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S03_L0020', 'MS14_D01_S03_L0021', 'MS14_D01_S03_L0022', 'MS14_D01_S03_L0023']), 'v111:gate_early:MS14_D01_S03_L0020')
    $ r13_v111_commit('MS14_D01_S03_L0023')
    jump r13_v111_registered

label r13_v111_gate_number:
    $ r13_v111_scene('MS14_D01_S03')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S03_L0024']), 'v111:gate_number:MS14_D01_S03_L0024')
    # New world (event 01, plan A): a half presentation earns one more try only.
    $ r13_v111_set('gate_hardened',True)
    jump r13_v111_gate_investigate

label r13_v111_gate_wrong:
    $ r13_v111_scene('MS14_D01_S03')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S03_L0025']), 'v111:gate_wrong:MS14_D01_S03_L0025')
    # New world: three chances per meeting (2026-10-22); the third wrong answer stands
    # and Daram enters as '외 한 명' (plan A).
    if r13_nw_retry('gate'):
        jump r13_v111_gate_investigate
    $ r13_v111_set('gate_daram_unlisted',True)
    jump r13_v111_registered

label r13_v111_gate_hint:
    $ r13_v111_scene('MS14_D01_S03')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S03_L0027']), 'v111:gate_hint:MS14_D01_S03_L0027')
    jump r13_v111_gate_investigate

label r13_v111_gate_reason:
    $ r13_v111_scene('MS14_D01_S03')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S03_L0028', 'MS14_D01_S03_L0029', 'MS14_D01_S03_L0030', 'MS14_D01_S03_L0031']), 'v111:gate_reason:MS14_D01_S03_L0028')
    $ r13_v111_commit('MS14_D01_S03_L0031')
    jump r13_v111_gate_investigate

label r13_v111_registered:
    $ r13_v111_scene('MS14_D01_S04')
    call r13_v111_travel('gate','registered')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S04_L0002', 'MS14_D01_S04_L0003', 'MS14_D01_S04_L0004', 'MS14_D01_S04_L0005', 'MS14_D01_S04_L0006', 'MS14_D01_S04_L0008']), 'v111:registered:MS14_D01_S04_L0002')
    $ r13_v111_commit('MS14_D01_S04_L0008')
    if r13_v111_value('gate_daram_unlisted'):
        $ r13_v111_set('E05.variant','unlisted')
    call r13_lines(r13_v111_lines(['MS14_D01_S04_L9101', 'MS14_D01_S04_L0009', 'MS14_D01_S04_L0010', 'MS14_D01_S04_L0011', 'MS14_D01_S04_L0012']), 'v111:registered:MS14_D01_S04_L9101')
    jump r13_v111_registered_menu

label r13_v111_registered_menu:
    call r13_v111_wait('registered_menu')
    $ v111_answer=_return
    if v111_answer==0:
        $ r13_v111_option('MS14_D01_S04_L0012_O1')
        jump r13_v111_registered_reason
    if v111_answer==1:
        $ r13_v111_option('MS14_D01_S04_L0012_O2')
        jump r13_v111_registered_depart
    jump r13_v111_registered_menu

label r13_v111_registered_reason:
    $ r13_v111_scene('MS14_D01_S04')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S04_L0013', 'MS14_D01_S04_L0014', 'MS14_D01_S04_L0015', 'MS14_D01_S04_L0016']), 'v111:registered_reason:MS14_D01_S04_L0013')
    $ r13_v111_commit('MS14_D01_S04_L0016')
    jump r13_v111_registered_menu

label r13_v111_registered_depart:
    $ r13_v111_scene('MS14_D01_S04')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S04_L0018', 'MS14_D01_S04_L0019', 'MS14_D01_S04_L0020']), 'v111:registered_depart:MS14_D01_S04_L0018')
    $ r13_v111_commit('MS14_D01_S04_L0020')
    call r13_lines(r13_v111_lines(['MS14_D01_S04_L0021']), 'v111:registered_depart:MS14_D01_S04_L0021')
    jump r13_v111_inn

label r13_v111_inn:
    $ r13_v111_scene('MS14_D01_S05')
    call r13_v111_travel('inn','inn')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S05_L0001', 'MS14_D01_S05_L0003', 'MS14_D01_S05_L0004', 'MS14_D01_S05_L0006', 'MS14_D01_S05_L0007', 'MS14_D01_S05_L0008', 'MS14_D01_S05_L0009', 'MS14_D01_S05_L0010', 'MS14_D01_S05_L0011', 'MS14_D01_S05_L0012', 'MS14_D01_S05_L0013']), 'v111:inn:MS14_D01_S05_L0001')
    jump r13_v111_room_observe

label r13_v111_room_observe:
    call r13_v111_travel('room13','room_observe')
    call r13_v111_wait('room_observe')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_room_empty
    jump r13_v111_room_observe

label r13_v111_room_empty:
    $ r13_v111_scene('MS14_D01_S05')
    call r13_v111_travel('room13','room_empty')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S05_L0016', 'MS14_D01_S05_L0017']), 'v111:room_empty:MS14_D01_S05_L0016')
    jump r13_v111_note_pick

label r13_v111_note_pick:
    call r13_v111_travel('room13','note_pick')
    call r13_v111_wait('note_pick')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_room_note
    jump r13_v111_note_pick

label r13_v111_room_note:
    $ r13_v111_scene('MS14_D01_S05')
    call r13_v111_travel('room13','room_note')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D01_S05_L0018']), 'v111:room_note:MS14_D01_S05_L0018')
    $ r13_v111_commit('MS14_D01_S05_L0019')
    call r13_lines(r13_v111_lines(['MS14_D01_S05_L9101', 'MS14_D01_S05_L0020', 'MS14_D01_S05_L0021']), 'v111:room_note:MS14_D01_S05_L9101')
    jump r13_v111_bundle_open

label r13_v111_bundle_open:
    call r13_v111_travel('room13','bundle_open')
    call r13_v111_wait('bundle_open')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_bundle
    jump r13_v111_bundle_open

label r13_v111_bundle:
    $ r13_v111_scene('MS14_D01_S05')
    call r13_v111_travel('room13','bundle')
    $ r13_v111_score()
    $ r13_v111_commit('MS14_D01_S05_L0022')
    call r13_lines(r13_v111_lines(['MS14_D01_S05_L9102', 'MS14_D01_S05_L0023', 'MS14_D01_S05_L0024', 'MS14_D01_S05_L0025', 'MS14_D01_S05_L0026', 'MS14_D01_S05_L0027', 'MS14_D01_S05_L0028', 'MS14_D01_S05_L0029', 'MS14_D01_S05_L0030']), 'v111:bundle:MS14_D01_S05_L9102')
    jump r13_v111_letter_compare

label r13_v111_letter_compare:
    call r13_v111_proof('두 편지를 나란히 본다',['E01', 'E06'],'r13_v111_room_compare',None,None)
    jump expression _return

label r13_v111_room_compare:
    $ r13_edit(period=2)
    $ r13_v111_scene('MS14_D01_S05')
    call r13_v111_travel('room13','room_compare')
    $ r13_v111_score()
    $ r13_v111_commit('MS14_D01_S05_L0031')
    call r13_lines(r13_v111_lines(['MS14_D01_S05_L0032', 'MS14_D01_S05_L0033', 'MS14_D01_S05_L0034', 'MS14_D01_S05_L0035']), 'v111:room_compare:MS14_D01_S05_L0032')
    call r13_v111_travel('inn','MS14_D01_S05_L0036')
    call r13_lines(r13_v111_lines(['MS14_D01_S05_L0037', 'MS14_D01_S05_L0038']), 'v111:room_compare:MS14_D01_S05_L0037')
    call r13_v111_travel('room13','MS14_D01_S05_L0039')
    call r13_lines(r13_v111_lines(['MS14_D01_S05_L0040', 'MS14_D01_S05_L0041', 'MS14_D01_S05_L0042', 'MS14_D01_S05_L0043', 'MS14_D01_S05_L0044', 'MS14_D01_S05_L0045', 'MS14_D01_S05_L0046', 'MS14_D01_S05_L0047', 'MS14_D01_S05_L0048']), 'v111:room_compare:MS14_D01_S05_L0040')
    $ r13_v111_commit('MS14_D01_S05_L0048')
    call r13_lines(r13_v111_lines(['MS14_D01_S05_L0049', 'MS14_D01_S05_L0050', 'MS14_D01_S05_L0051', 'MS14_D01_S05_L0052']), 'v111:room_compare:MS14_D01_S05_L0049')
    jump r13_v111_sleep1

label r13_v111_sleep1:
    call r13_v111_travel('room13','sleep1')
    call r13_v111_wait('sleep1')
    $ v111_answer=_return
    if v111_answer==0:
        $ r13_v111_apply('option:sleep1:0',[{'op': 'set', 'field': 'day', 'value': 2}])
        jump r13_v111_day2
    jump r13_v111_sleep1

label r13_v111_day2:
    $ r13_v111_scene('MS14_D02_S01')
    call r13_v111_travel('gate','day2')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S01_L0002', 'MS14_D02_S01_L0003', 'MS14_D02_S01_L0004', 'MS14_D02_S01_L0005', 'MS14_D02_S01_L0006', 'MS14_D02_S01_L0007']), 'v111:day2:MS14_D02_S01_L0002')
    $ r13_v111_commit('MS14_D02_S01_L0008')
    jump r13_v111_square2

label r13_v111_square2:
    $ r13_v111_scene('MS14_D02_S01')
    call r13_v111_travel('square','square2')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S01_L0010', 'MS14_D02_S01_L0011']), 'v111:square2:MS14_D02_S01_L0010')
    jump r13_v111_lamp_rope

label r13_v111_lamp_rope:
    call r13_v111_travel('square','lamp_rope')
    call r13_v111_wait('lamp_rope')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_chorong
    jump r13_v111_lamp_rope

label r13_v111_chorong:
    $ r13_v111_scene('MS14_D02_S01')
    call r13_v111_travel('square','chorong')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S01_L0014', 'MS14_D02_S01_L0015', 'MS14_D02_S01_L0016', 'MS14_D02_S01_L0017', 'MS14_D02_S01_L0018', 'MS14_D02_S01_L0019', 'MS14_D02_S01_L0020', 'MS14_D02_S01_L0021', 'MS14_D02_S01_L0022', 'MS14_D02_S01_L0023', 'MS14_D02_S01_L0024', 'MS14_D02_S01_L0025', 'MS14_D02_S01_L0026', 'MS14_D02_S01_L0027', 'MS14_D02_S01_L0028', 'MS14_D02_S01_L0029']), 'v111:chorong:MS14_D02_S01_L0014')
    jump r13_v111_go_box

label r13_v111_go_box:
    call r13_v111_wait('go_box')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_box_path
    jump r13_v111_go_box

label r13_v111_box_path:
    $ r13_v111_scene('MS14_D02_S01')
    call r13_v111_travel('forest','box_path')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S01_L0031', 'MS14_D02_S01_L0032']), 'v111:box_path:MS14_D02_S01_L0031')
    jump r13_v111_box_inspect

label r13_v111_box_inspect:
    call r13_v111_travel('forest','box_inspect')
    call r13_v111_wait('box_inspect')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_box_empty
    jump r13_v111_box_inspect

label r13_v111_box_empty:
    $ r13_v111_scene('MS14_D02_S01')
    call r13_v111_travel('forest','box_empty')
    $ r13_v111_score()
    $ r13_v111_commit('MS14_D02_S01_L0033')
    call r13_lines(r13_v111_lines(['MS14_D02_S01_L0034', 'MS14_D02_S01_L0035', 'MS14_D02_S01_L0036', 'MS14_D02_S01_L0037', 'MS14_D02_S01_L0038']), 'v111:box_empty:MS14_D02_S01_L0034')
    jump r13_v111_box_note

label r13_v111_box_note:
    call r13_v111_travel('forest','box_note')
    call r13_v111_wait('box_note')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_box_written
    jump r13_v111_box_note

label r13_v111_box_written:
    $ r13_v111_scene('MS14_D02_S01')
    call r13_v111_travel('forest','box_written')
    $ r13_v111_score()
    $ r13_v111_commit('MS14_D02_S01_L0039')
    call r13_lines(r13_v111_lines(['MS14_D02_S01_L0040', 'MS14_D02_S01_L0041', 'MS14_D02_S01_L0042', 'MS14_D02_S01_L0043', 'MS14_D02_S01_L0044', 'MS14_D02_S01_L0045']), 'v111:box_written:MS14_D02_S01_L0040')
    jump r13_v111_post

label r13_v111_post:
    $ r13_v111_scene('MS14_D02_S02')
    call r13_v111_travel('post','post')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S02_L0002', 'MS14_D02_S02_L0003', 'MS14_D02_S02_L0004']), 'v111:post:MS14_D02_S02_L0002')
    jump r13_v111_envelope_show

label r13_v111_envelope_show:
    call r13_v111_travel('post','envelope_show')
    call r13_v111_wait('envelope_show')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_post_checked
    jump r13_v111_envelope_show

label r13_v111_post_checked:
    $ r13_v111_scene('MS14_D02_S02')
    call r13_v111_travel('post','post_checked')
    $ r13_v111_score()
    $ r13_v111_commit('MS14_D02_S02_L0005')
    call r13_lines(r13_v111_lines(['MS14_D02_S02_L9101', 'MS14_D02_S02_L0006', 'MS14_D02_S02_L0007', 'MS14_D02_S02_L0008', 'MS14_D02_S02_L0009', 'MS14_D02_S02_L0010', 'MS14_D02_S02_L0011', 'MS14_D02_S02_L0012', 'MS14_D02_S02_L0013', 'MS14_D02_S02_L0014', 'MS14_D02_S02_L0015']), 'v111:post_checked:MS14_D02_S02_L9101')
    jump r13_v111_post_menu

label r13_v111_post_menu:
    call r13_v111_travel('post','post_menu')
    call r13_v111_wait('post_menu')
    $ v111_answer=_return
    if v111_answer==0:
        $ r13_v111_option('MS14_D02_S02_L0015_O1')
        jump r13_v111_post_scribe
    if v111_answer==1:
        $ r13_v111_option('MS14_D02_S02_L0015_O2')
        jump r13_v111_post_return
    jump r13_v111_post_menu

label r13_v111_post_scribe:
    $ r13_v111_scene('MS14_D02_S02')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S02_L0016']), 'v111:post_scribe:MS14_D02_S02_L0016')
    jump r13_v111_post_menu

label r13_v111_post_return:
    $ r13_v111_scene('MS14_D02_S02')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S02_L0017', 'MS14_D02_S02_L0018', 'MS14_D02_S02_L0019', 'MS14_D02_S02_L0020', 'MS14_D02_S02_L0021', 'MS14_D02_S02_L0022', 'MS14_D02_S02_L0023', 'MS14_D02_S02_L0024']), 'v111:post_return:MS14_D02_S02_L0017')
    $ r13_v111_commit('MS14_D02_S02_L0025')
    call r13_lines(r13_v111_lines(['MS14_D02_S02_L0026', 'MS14_D02_S02_L0027', 'MS14_D02_S02_L0028']), 'v111:post_return:MS14_D02_S02_L0026')
    jump r13_v111_piko2

label r13_v111_piko2:
    $ r13_v111_scene('MS14_D02_S03')
    call r13_v111_travel('square','piko2')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S03_L0002', 'MS14_D02_S03_L0003', 'MS14_D02_S03_L0004', 'MS14_D02_S03_L0005', 'MS14_D02_S03_L0006', 'MS14_D02_S03_L0007', 'MS14_D02_S03_L0008']), 'v111:piko2:MS14_D02_S03_L0002')
    jump r13_v111_portrait_ask

label r13_v111_portrait_ask:
    call r13_v111_travel('square','portrait_ask')
    call r13_v111_wait('portrait_ask')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_portrait_commission
    jump r13_v111_portrait_ask

label r13_v111_portrait_commission:
    $ r13_v111_scene('MS14_D02_S03')
    call r13_v111_travel('square','portrait_commission')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S03_L0010', 'MS14_D02_S03_L0011', 'MS14_D02_S03_L0012', 'MS14_D02_S03_L0013', 'MS14_D02_S03_L0014', 'MS14_D02_S03_L0015', 'MS14_D02_S03_L0016', 'MS14_D02_S03_L0017', 'MS14_D02_S03_L0018', 'MS14_D02_S03_L0019']), 'v111:portrait_commission:MS14_D02_S03_L0010')
    $ r13_v111_commit('MS14_D02_S03_L0020')
    call r13_lines(r13_v111_lines(['MS14_D02_S03_L0021', 'MS14_D02_S03_L0022', 'MS14_D02_S03_L0023', 'MS14_D02_S03_L0024']), 'v111:portrait_commission:MS14_D02_S03_L0021')
    $ r13_nw_acquire("NW_PIKO_TREMOR")
    jump r13_v111_lamp_observe

label r13_v111_lamp_observe:
    if all(r13_v111_value("lamp_part_%d"%i) for i in range(4)):
        jump r13_v111_lamp_details
    call r13_v111_travel('square','lamp_observe')
    call r13_v111_wait('lamp_observe')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_lamp_seen_0
    if v111_answer==1:
        jump r13_v111_lamp_seen_1
    if v111_answer==2:
        jump r13_v111_lamp_seen_2
    if v111_answer==3:
        jump r13_v111_lamp_seen_3
    if v111_answer==4:
        jump r13_v111_lamp_details
    jump r13_v111_lamp_observe

label r13_v111_lamp_seen_0:
    $ r13_v111_apply('lamp_seen_0',[{'op': 'set', 'field': 'lamp_part_0', 'value': True}])
    jump r13_v111_lamp_observe

label r13_v111_lamp_seen_1:
    $ r13_v111_apply('lamp_seen_1',[{'op': 'set', 'field': 'lamp_part_1', 'value': True}])
    jump r13_v111_lamp_observe

label r13_v111_lamp_seen_2:
    $ r13_v111_apply('lamp_seen_2',[{'op': 'set', 'field': 'lamp_part_2', 'value': True}])
    jump r13_v111_lamp_observe

label r13_v111_lamp_seen_3:
    $ r13_v111_apply('lamp_seen_3',[{'op': 'set', 'field': 'lamp_part_3', 'value': True}])
    jump r13_v111_lamp_observe

label r13_v111_lamp_details:
    $ r13_v111_scene('MS14_D02_S03')
    call r13_v111_travel('square','lamp_details')
    $ r13_v111_score()
    $ r13_v111_commit('MS14_D02_S03_L0025')
    call r13_lines(r13_v111_lines(['MS14_D02_S03_L9101', 'MS14_D02_S03_L0026', 'MS14_D02_S03_L0027', 'MS14_D02_S03_L0028', 'MS14_D02_S03_L0029', 'MS14_D02_S03_L0030', 'MS14_D02_S03_L0031', 'MS14_D02_S03_L0032', 'MS14_D02_S03_L0033', 'MS14_D02_S03_L0034', 'MS14_D02_S03_L0035', 'MS14_D02_S03_L0037', 'MS14_D02_S03_L0038', 'MS14_D02_S03_L0039', 'MS14_D02_S03_L0040', 'MS14_D02_S03_L0041', 'MS14_D02_S03_L0042', 'MS14_D02_S03_L0043', 'MS14_D02_S03_L0044', 'MS14_D02_S03_L0045', 'MS14_D02_S03_L0046']), 'v111:lamp_details:MS14_D02_S03_L9101')
    $ r13_v111_commit('MS14_D02_S03_L0047')
    jump r13_v111_diner_offer

label r13_v111_diner_offer:
    $ r13_edit(period=1)
    $ r13_v111_scene('MS14_D02_S04')
    call r13_v111_travel('dining','diner_offer')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S04_L0002', 'MS14_D02_S04_L0003', 'MS14_D02_S04_L0004', 'MS14_D02_S04_L0005', 'MS14_D02_S04_L0006', 'MS14_D02_S04_L0007', 'MS14_D02_S04_L0008', 'MS14_D02_S04_L0009', 'MS14_D02_S04_L0010', 'MS14_D02_S04_L0012', 'MS14_D02_S04_L0013', 'MS14_D02_S04_L0014', 'MS14_D02_S04_L0016', 'MS14_D02_S04_L0017', 'MS14_D02_S04_L0018', 'MS14_D02_S04_L0019', 'MS14_D02_S04_L0020']), 'v111:diner_offer:MS14_D02_S04_L0002')
    jump r13_v111_afternoon

label r13_v111_afternoon:
    $ v111_menu_owner='afternoon'
    $ v111_menu=[('피코가 오늘 안에서 잘 자리를 마련한다',0) for _ in [0] if True] + [('아내를 봤다는 네로를 만나러 간다',1) for _ in [0] if True]
    $ v111_answer=renpy.display_menu(v111_menu)
    if v111_answer==0:
        $ r13_v111_option('MS14_D02_S04_L0020_O1')
        $ r13_v111_apply('option:afternoon:0',[{'op': 'set', 'field': 'D02_afternoon', 'value': 'shelter'}])
        jump r13_v111_shelter_choice
    if v111_answer==1:
        $ r13_v111_option('MS14_D02_S04_L0020_O2')
        $ r13_v111_apply('option:afternoon:1',[{'op': 'set', 'field': 'D02_afternoon', 'value': 'nero'}])
        jump r13_v111_nero_choice
    jump r13_v111_afternoon

label r13_v111_shelter_choice:
    $ r13_v111_scene('MS14_D02_S04')
    call r13_v111_travel('dining','shelter_choice')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S04_L0021', 'MS14_D02_S04_L0022']), 'v111:shelter_choice:MS14_D02_S04_L0021')
    jump r13_v111_shelter_work

label r13_v111_shelter_work:
    call r13_v111_travel('dining','shelter_work')
    call r13_v111_wait('shelter_work')
    $ v111_answer=_return
    call r13_v111_travel("inn","shelter_cloth")
    call r13_v111_wait("shelter_cloth")
    call r13_v111_travel("square","shelter_invite")
    call r13_v111_wait("shelter_invite")
    if v111_answer==0:
        jump r13_v111_shelter_prepare
    jump r13_v111_shelter_work

label r13_v111_shelter_prepare:
    $ r13_v111_scene('MS14_D02_S04')
    call r13_v111_travel('square','shelter_prepare')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S04_L0024', 'MS14_D02_S04_L0025', 'MS14_D02_S04_L0026', 'MS14_D02_S04_L0027', 'MS14_D02_S04_L0028']), 'v111:shelter_prepare:MS14_D02_S04_L0024')
    jump r13_v111_shelter_enter

label r13_v111_shelter_enter:
    call r13_v111_wait('shelter_enter')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_shelter_done
    jump r13_v111_shelter_enter

label r13_v111_shelter_done:
    $ r13_v111_scene('MS14_D02_S04')
    call r13_v111_travel('dining','shelter_done')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S04_L0030', 'MS14_D02_S04_L0031', 'MS14_D02_S04_L0032', 'MS14_D02_S04_L0033', 'MS14_D02_S04_L0034', 'MS14_D02_S04_L0035', 'MS14_D02_S04_L0036', 'MS14_D02_S04_L0038']), 'v111:shelter_done:MS14_D02_S04_L0030')
    $ r13_v111_commit('MS14_D02_S04_L0038')
    jump r13_v111_evening2

label r13_v111_nero_choice:
    $ r13_v111_scene('MS14_D02_S04')
    call r13_v111_travel('dining','nero_choice')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S04_L0039', 'MS14_D02_S04_L0040', 'MS14_D02_S04_L0041']), 'v111:nero_choice:MS14_D02_S04_L0039')
    call r13_v111_travel('square','MS14_D02_S04_L0042')
    call r13_lines(r13_v111_lines(['MS14_D02_S04_L0043', 'MS14_D02_S04_L0044', 'MS14_D02_S04_L0045', 'MS14_D02_S04_L0046', 'MS14_D02_S04_L0047', 'MS14_D02_S04_L0048']), 'v111:nero_choice:MS14_D02_S04_L0043')
    call r13_v111_travel('forest','MS14_D02_S04_L0049')
    call r13_lines(r13_v111_lines(['MS14_D02_S04_L0050', 'MS14_D02_S04_L0051', 'MS14_D02_S04_L0052', 'MS14_D02_S04_L0053', 'MS14_D02_S04_L0054', 'MS14_D02_S04_L0055', 'MS14_D02_S04_L0057', 'MS14_D02_S04_L0058', 'MS14_D02_S04_L0059', 'MS14_D02_S04_L0060', 'MS14_D02_S04_L0061']), 'v111:nero_choice:MS14_D02_S04_L0050')
    jump r13_v111_nero_work

label r13_v111_nero_work:
    call r13_v111_travel('forest','nero_work')
    call r13_v111_wait('nero_work')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_nero_done
    jump r13_v111_nero_work

label r13_v111_nero_done:
    $ r13_v111_scene('MS14_D02_S04')
    call r13_v111_travel('forest','nero_done')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S04_L0063', 'MS14_D02_S04_L0065', 'MS14_D02_S04_L0066', 'MS14_D02_S04_L0067', 'MS14_D02_S04_L0068', 'MS14_D02_S04_L0069', 'MS14_D02_S04_L0070', 'MS14_D02_S04_L0071', 'MS14_D02_S04_L0073', 'MS14_D02_S04_L0074', 'MS14_D02_S04_L0075']), 'v111:nero_done:MS14_D02_S04_L0063')
    call r13_v111_travel('square','MS14_D02_S04_L0076')
    call r13_lines(r13_v111_lines(['MS14_D02_S04_L0077', 'MS14_D02_S04_L0078']), 'v111:nero_done:MS14_D02_S04_L0077')
    call r13_v111_travel('inn','MS14_D02_S04_L0079')
    call r13_lines(r13_v111_lines(['MS14_D02_S04_L0080', 'MS14_D02_S04_L0081']), 'v111:nero_done:MS14_D02_S04_L0080')
    call r13_v111_travel('room13','MS14_D02_S04_L0083')
    $ r13_v111_commit('MS14_D02_S04_L0083')
    call r13_lines(r13_v111_lines(['MS14_D02_S04_L9101', 'MS14_D02_S04_L9102']), 'v111:nero_done:MS14_D02_S04_L9101')
    jump r13_v111_evening2

label r13_v111_evening2:
    $ r13_edit(period=2)
    $ r13_v111_scene('MS14_D02_S05')
    call r13_v111_travel('inn','evening2')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S05_L0001', 'MS14_D02_S05_L0002', 'MS14_D02_S05_L0003', 'MS14_D02_S05_L0004', 'MS14_D02_S05_L0005']), 'v111:evening2:MS14_D02_S05_L0001')
    call r13_v111_travel('room13','MS14_D02_S05_L0006')
    call r13_lines(r13_v111_lines(['MS14_D02_S05_L0007', 'MS14_D02_S05_L0008', 'MS14_D02_S05_L0009']), 'v111:evening2:MS14_D02_S05_L0007')
    jump r13_v111_evening2_route

label r13_v111_evening2_route:
    if r13_v111_value('piko_sheltered')==True:
        jump r13_v111_evening2_alive
    jump r13_v111_evening2_outside

label r13_v111_evening2_alive:
    $ r13_v111_scene('MS14_D02_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S05_L0010', 'MS14_D02_S05_L0011']), 'v111:evening2_alive:MS14_D02_S05_L0010')
    jump r13_v111_evening2_end

label r13_v111_evening2_outside:
    $ r13_v111_scene('MS14_D02_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D02_S05_L0012', 'MS14_D02_S05_L0013']), 'v111:evening2_outside:MS14_D02_S05_L0012')
    jump r13_v111_evening2_end

label r13_v111_evening2_end:
    $ r13_edit(period=2)
    $ r13_v111_scene('MS14_D02_S05')
    call r13_v111_travel('room13','evening2_end')
    $ r13_v111_score()
    jump r13_v111_sleep2

label r13_v111_sleep2:
    call r13_v111_travel('room13','sleep2')
    call r13_v111_wait('sleep2')
    $ v111_answer=_return
    if v111_answer==0:
        $ r13_v111_apply('option:sleep2:0',[{'op': 'set', 'field': 'day', 'value': 3}])
        jump r13_v111_day3
    jump r13_v111_sleep2

label r13_v111_day3:
    if r13_v111_value('piko_sheltered')==True:
        jump r13_v111_piko_alive3
    jump r13_v111_piko_dead3

label r13_v111_piko_alive3:
    $ r13_edit(period=0)
    $ r13_v111_scene('MS14_D03_S01')
    call r13_v111_travel('dining','piko_alive3')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S01_L0023', 'MS14_D03_S01_L0024', 'MS14_D03_S01_L0025', 'MS14_D03_S01_L0026', 'MS14_D03_S01_L0028', 'MS14_D03_S01_L0029', 'MS14_D03_S01_L0030', 'MS14_D03_S01_L0031', 'MS14_D03_S01_L0032', 'MS14_D03_S01_L0033', 'MS14_D03_S01_L0034']), 'v111:piko_alive3:MS14_D03_S01_L0023')
    jump r13_v111_piko_clean

label r13_v111_piko_clean:
    call r13_v111_travel('dining','piko_clean')
    call r13_v111_wait('piko_clean')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_piko_receive
    jump r13_v111_piko_clean

label r13_v111_piko_receive:
    $ r13_v111_scene('MS14_D03_S01')
    call r13_v111_travel('dining','piko_receive')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S01_L0036', 'MS14_D03_S01_L0037', 'MS14_D03_S01_L0038']), 'v111:piko_receive:MS14_D03_S01_L0036')
    $ r13_v111_commit('MS14_D03_S01_L0039')
    jump r13_v111_lamp3

label r13_v111_piko_dead3:
    $ r13_edit(period=0)
    $ r13_v111_scene('MS14_D03_S01')
    call r13_v111_travel('square','piko_dead3')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S01_L0002', 'MS14_D03_S01_L0003', 'MS14_D03_S01_L0004', 'MS14_D03_S01_L0005', 'MS14_D03_S01_L0006', 'MS14_D03_S01_L0007', 'MS14_D03_S01_L0008', 'MS14_D03_S01_L0009', 'MS14_D03_S01_L0010', 'MS14_D03_S01_L0011', 'MS14_D03_S01_L0012', 'MS14_D03_S01_L0013', 'MS14_D03_S01_L0014', 'MS14_D03_S01_L0015', 'MS14_D03_S01_L0016', 'MS14_D03_S01_L0018', 'MS14_D03_S01_L0019', 'MS14_D03_S01_L0020']), 'v111:piko_dead3:MS14_D03_S01_L0002')
    $ r13_v111_commit('MS14_D03_S01_L0021')
    call r13_lines(r13_v111_lines(['MS14_D03_S01_L9101']), 'v111:piko_dead3:MS14_D03_S01_L9101')
    jump r13_v111_lamp3

label r13_v111_lamp3:
    $ r13_v111_scene('MS14_D03_S02')
    call r13_v111_travel('square','lamp3')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S02_L0002', 'MS14_D03_S02_L0003', 'MS14_D03_S02_L0004', 'MS14_D03_S02_L0005', 'MS14_D03_S02_L0006', 'MS14_D03_S02_L0007', 'MS14_D03_S02_L0008', 'MS14_D03_S02_L0009', 'MS14_D03_S02_L0010', 'MS14_D03_S02_L0011']), 'v111:lamp3:MS14_D03_S02_L0002')
    jump r13_v111_lamp_inspect3

label r13_v111_lamp_inspect3:
    call r13_v111_travel('square','lamp_inspect3')
    call r13_v111_wait('lamp_inspect3')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_lamp_interior3
    jump r13_v111_lamp_inspect3

label r13_v111_lamp_interior3:
    $ r13_v111_scene('MS14_D03_S02')
    call r13_v111_travel('square','lamp_interior3')
    $ r13_v111_score()
    $ r13_v111_commit('MS14_D03_S02_L0012')
    call r13_lines(r13_v111_lines(['MS14_D03_S02_L9101', 'MS14_D03_S02_L0013', 'MS14_D03_S02_L0014', 'MS14_D03_S02_L0015']), 'v111:lamp_interior3:MS14_D03_S02_L9101')
    jump r13_v111_fragment_request

label r13_v111_fragment_request:
    call r13_v111_travel('square','fragment_request')
    call r13_v111_wait('fragment_request')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_lamp_fragment3
    jump r13_v111_fragment_request

label r13_v111_lamp_fragment3:
    $ r13_v111_scene('MS14_D03_S02')
    call r13_v111_travel('square','lamp_fragment3')
    $ r13_v111_score()
    $ r13_v111_commit('MS14_D03_S02_L0016')
    call r13_lines(r13_v111_lines(['MS14_D03_S02_L9102', 'MS14_D03_S02_L0017', 'MS14_D03_S02_L0019', 'MS14_D03_S02_L0020', 'MS14_D03_S02_L0021', 'MS14_D03_S02_L0022', 'MS14_D03_S02_L0023', 'MS14_D03_S02_L0024', 'MS14_D03_S02_L0025']), 'v111:lamp_fragment3:MS14_D03_S02_L9102')
    jump r13_v111_lamp_log_request

label r13_v111_lamp_log_request:
    call r13_v111_travel('square','lamp_log_request')
    call r13_v111_wait('lamp_log_request')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_lamp_log3
    jump r13_v111_lamp_log_request

label r13_v111_lamp_log3:
    $ r13_v111_scene('MS14_D03_S02')
    call r13_v111_travel('square','lamp_log3')
    $ r13_v111_score()
    $ r13_v111_commit('MS14_D03_S02_L0027')
    call r13_lines(r13_v111_lines(['MS14_D03_S02_L9103', 'MS14_D03_S02_L0028']), 'v111:lamp_log3:MS14_D03_S02_L9103')
    jump r13_v111_workshop3

label r13_v111_workshop3:
    $ r13_v111_scene('MS14_D03_S03')
    call r13_v111_travel('workshop','workshop3')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S03_L0002', 'MS14_D03_S03_L0003', 'MS14_D03_S03_L0004', 'MS14_D03_S03_L0005', 'MS14_D03_S03_L0006']), 'v111:workshop3:MS14_D03_S03_L0002')
    jump r13_v111_loan_read

label r13_v111_loan_read:
    call r13_v111_travel('workshop','loan_read')
    call r13_v111_wait('loan_read')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_loan3
    jump r13_v111_loan_read

label r13_v111_loan3:
    $ r13_v111_scene('MS14_D03_S03')
    call r13_v111_travel('workshop','loan3')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S03_L0007']), 'v111:loan3:MS14_D03_S03_L0007')
    $ r13_v111_commit('MS14_D03_S03_L0008')
    call r13_lines(r13_v111_lines(['MS14_D03_S03_L9101', 'MS14_D03_S03_L0009', 'MS14_D03_S03_L0010', 'MS14_D03_S03_L0011']), 'v111:loan3:MS14_D03_S03_L9101')
    jump r13_v111_clinic3

label r13_v111_clinic3:
    $ r13_v111_scene('MS14_D03_S03')
    call r13_v111_travel('clinic','clinic3')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S03_L0013', 'MS14_D03_S03_L0014', 'MS14_D03_S03_L0015', 'MS14_D03_S03_L0016', 'MS14_D03_S03_L0017', 'MS14_D03_S03_L0018', 'MS14_D03_S03_L0019', 'MS14_D03_S03_L0020', 'MS14_D03_S03_L0021', 'MS14_D03_S03_L0022', 'MS14_D03_S03_L0023', 'MS14_D03_S03_L0024', 'MS14_D03_S03_L0025', 'MS14_D03_S03_L0026']), 'v111:clinic3:MS14_D03_S03_L0013')
    jump r13_v111_measurement_read

label r13_v111_measurement_read:
    call r13_v111_travel('clinic','measurement_read')
    call r13_v111_wait('measurement_read')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_measurement3
    jump r13_v111_measurement_read

label r13_v111_measurement3:
    $ r13_v111_scene('MS14_D03_S03')
    call r13_v111_travel('clinic','measurement3')
    $ r13_v111_score()
    $ r13_v111_commit('MS14_D03_S03_L0027')
    call r13_lines(r13_v111_lines(['MS14_D03_S03_L9102', 'MS14_D03_S03_L0028', 'MS14_D03_S03_L0029', 'MS14_D03_S03_L0030', 'MS14_D03_S03_L0031']), 'v111:measurement3:MS14_D03_S03_L9102')
    jump r13_v111_measurement_proof

label r13_v111_measurement_proof:
    call r13_v111_proof('측정 종료와 점검 기록을 대조한다',['E13', 'E11'],'r13_v111_measurement_correct','r13_v111_measurement_wrong','r13_v111_measurement_hint')
    jump expression _return

label r13_v111_measurement_correct:
    $ r13_v111_scene('MS14_D03_S03')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S03_L0033', 'MS14_D03_S03_L0034', 'MS14_D03_S03_L0035']), 'v111:measurement_correct:MS14_D03_S03_L0033')
    $ r13_v111_commit('MS14_D03_S03_L0035')
    jump r13_v111_measurement_after

label r13_v111_measurement_wrong:
    $ r13_v111_scene('MS14_D03_S03')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S03_L0039', 'MS14_D03_S03_L0040']), 'v111:measurement_wrong:MS14_D03_S03_L0039')
    jump r13_v111_measurement_proof

label r13_v111_measurement_hint:
    $ r13_v111_scene('MS14_D03_S03')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S03_L0041']), 'v111:measurement_hint:MS14_D03_S03_L0041')
    jump r13_v111_measurement_proof

label r13_v111_measurement_after:
    $ r13_v111_scene('MS14_D03_S03')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S03_L0036', 'MS14_D03_S03_L0037', 'MS14_D03_S03_L0038']), 'v111:measurement_after:MS14_D03_S03_L0036')
    jump r13_v111_silluk3

label r13_v111_silluk3:
    $ r13_v111_scene('MS14_D03_S04')
    call r13_v111_travel('square','silluk3')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S04_L0002', 'MS14_D03_S04_L0003', 'MS14_D03_S04_L0004', 'MS14_D03_S04_L0005', 'MS14_D03_S04_L0006', 'MS14_D03_S04_L0007', 'MS14_D03_S04_L0008']), 'v111:silluk3:MS14_D03_S04_L0002')
    jump r13_v111_transport_read

label r13_v111_transport_read:
    call r13_v111_travel('square','transport_read')
    call r13_v111_wait('transport_read')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_transport3
    jump r13_v111_transport_read

label r13_v111_transport3:
    $ r13_v111_scene('MS14_D03_S04')
    call r13_v111_travel('square','transport3')
    $ r13_v111_score()
    $ r13_v111_commit('MS14_D03_S04_L0009')
    call r13_lines(r13_v111_lines(['MS14_D03_S04_L9101']), 'v111:transport3:MS14_D03_S04_L9101')
    jump r13_v111_knife_permission

label r13_v111_knife_permission:
    call r13_v111_travel('square','knife_permission')
    call r13_v111_wait('knife_permission')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_knife_observed
    jump r13_v111_knife_permission

label r13_v111_knife_observed:
    $ r13_v111_scene('MS14_D03_S04')
    call r13_v111_travel('square','knife_observed')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S04_L0010', 'MS14_D03_S04_L0011', 'MS14_D03_S04_L0013', 'MS14_D03_S04_L0014', 'MS14_D03_S04_L0015']), 'v111:knife_observed:MS14_D03_S04_L0010')
    $ r13_v111_commit('MS14_D03_S04_L0016')
    call r13_lines(r13_v111_lines(['MS14_D03_S04_L0017', 'MS14_D03_S04_L0018', 'MS14_D03_S04_L0019', 'MS14_D03_S04_L0020']), 'v111:knife_observed:MS14_D03_S04_L0017')
    jump r13_v111_store_visit

label r13_v111_store_visit:
    call r13_v111_wait('store_visit')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_store3
    jump r13_v111_store_visit

label r13_v111_store3:
    $ r13_v111_scene('MS14_D03_S04')
    call r13_v111_travel('store','store3')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S04_L9001', 'MS14_D03_S04_L0022', 'MS14_D03_S04_L0023', 'MS14_D03_S04_L0024']), 'v111:store3:MS14_D03_S04_L9001')
    jump r13_v111_stone_check

label r13_v111_stone_check:
    call r13_v111_travel('store','stone_check')
    call r13_v111_wait('stone_check')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_stone3
    jump r13_v111_stone_check

label r13_v111_stone3:
    $ r13_v111_scene('MS14_D03_S04')
    call r13_v111_travel('store','stone3')
    $ r13_v111_score()
    call r13_v111_travel('workshop','MS14_D03_S04_L0026')
    call r13_lines(r13_v111_lines(['MS14_D03_S04_L0026', 'MS14_D03_S04_L0027']), 'v111:stone3:MS14_D03_S04_L0026')
    call r13_v111_travel('store','MS14_D03_S04_L0028')
    $ r13_v111_commit('MS14_D03_S04_L0028')
    call r13_lines(r13_v111_lines(['MS14_D03_S04_L9102', 'MS14_D03_S04_L0029', 'MS14_D03_S04_L0030', 'MS14_D03_S04_L0031']), 'v111:stone3:MS14_D03_S04_L9102')
    jump r13_v111_sale_check

label r13_v111_sale_check:
    call r13_v111_travel('store','sale_check')
    call r13_v111_wait('sale_check')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_sale3
    jump r13_v111_sale_check

label r13_v111_sale3:
    $ r13_v111_scene('MS14_D03_S04')
    call r13_v111_travel('store','sale3')
    $ r13_v111_score()
    $ r13_v111_commit('MS14_D03_S04_L0032')
    call r13_lines(r13_v111_lines(['MS14_D03_S04_L9103', 'MS14_D03_S04_L0033']), 'v111:sale3:MS14_D03_S04_L9103')
    $ r13_nw_acquire("NW_INNER_PRICE")
    $ r13_nw_acquire("NW_KEEPER_DATE")
    call r13_v111_travel('workshop','MS14_D03_S04_L0034')
    call r13_lines(r13_v111_lines(['MS14_D03_S04_L0035', 'MS14_D03_S04_L0036', 'MS14_D03_S04_L0037']), 'v111:sale3:MS14_D03_S04_L0035')
    $ r13_v111_commit('MS14_D03_S04_L0037')
    jump r13_v111_trial_open

label r13_v111_trial_open:
    $ r13_edit(period=1)
    $ r13_v111_scene('MS14_D03_S05')
    call r13_v111_travel('workshop','trial_open')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0002']), 'v111:trial_open:MS14_D03_S05_L0002')
    jump r13_v111_trial_repair

label r13_v111_trial_repair:
    call r13_v111_proof('수리와 반출을 가릴 자료를 낸다',['E11', 'E12', 'E13'],'r13_v111_trial_repair_ok','r13_v111_trial_wrong','r13_v111_trial_hint')
    jump expression _return

label r13_v111_trial_repair_ok:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0004', 'MS14_D03_S05_L0005']), 'v111:trial_repair_ok:MS14_D03_S05_L0004')
    $ r13_v111_commit('MS14_D03_S05_L0005')
    jump r13_v111_trial_sale

label r13_v111_trial_sale:
    call r13_v111_proof('돌과 매입 기록을 낸다',['E15', 'E16'],'r13_v111_trial_sale_ok','r13_v111_trial_wrong_sale','r13_v111_trial_hint_sale')
    jump expression _return

label r13_v111_trial_sale_ok:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0007', 'MS14_D03_S05_L0008', 'MS14_D03_S05_L0009']), 'v111:trial_sale_ok:MS14_D03_S05_L0007')
    jump r13_v111_trial_knife

label r13_v111_trial_knife:
    $ v111_menu_owner='trial_knife'
    $ v111_menu=[('안쪽 파편과 칼끝을 대조한다',0) for _ in [0] if r13_v111_value('silluk_knife_comparison_consent')==True and r13_v111_owned('E32')] + [('칼 모양만으로 지목한다',1) for _ in [0] if True] + [('자료를 다시 본다',2) for _ in [0] if True]
    $ v111_answer=renpy.display_menu(v111_menu)
    if v111_answer==0:
        jump r13_v111_knife_fit
    if v111_answer==1:
        jump r13_v111_knife_wrong
    if v111_answer==2:
        jump r13_v111_trial_knife_records
    jump r13_v111_trial_knife

label r13_v111_trial_knife_records:
    call screen r13_book
    jump r13_v111_trial_knife

label r13_v111_knife_fit:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0012', 'MS14_D03_S05_L0013', 'MS14_D03_S05_L0014', 'MS14_D03_S05_L0016', 'MS14_D03_S05_L0017']), 'v111:knife_fit:MS14_D03_S05_L0012')
    $ r13_v111_commit('MS14_D03_S05_L0018')
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L9101', 'MS14_D03_S05_L9102']), 'v111:knife_fit:MS14_D03_S05_L9101')
    jump r13_v111_trial_latch

label r13_v111_knife_wrong:
    $ r13_v111_scene('MS14_D03_S05')
    # New world (event 03): naming by the knife's shape alone costs a chance; the third loses the knife issue.
    $ r13_v111_score()
    if r13_nw_retry('lamp'):
        call r13_lines(r13_v111_lines(['MS14_D03_S05_L0068', 'MS14_D03_S05_L0069', 'MS14_D03_S05_L0070']), 'v111:knife_wrong:retry')
        jump r13_v111_trial_knife
    $ r13_nw_meeting_end('lamp','partial')
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0068', 'MS14_D03_S05_L0069', 'MS14_D03_S05_L0070']), 'v111:knife_wrong:MS14_D03_S05_L0068')
    jump r13_v111_trial_choices

label r13_v111_trial_latch:
    call r13_v111_proof('바깥 걸쇠 주장과 발견 위치를 대조한다',['E17', 'E32', 'E33'],'r13_v111_trial_latch_ok','r13_v111_trial_wrong_latch','r13_v111_trial_hint_latch')
    jump expression _return

label r13_v111_trial_latch_ok:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0020', 'MS14_D03_S05_L0021', 'MS14_D03_S05_L0023', 'MS14_D03_S05_L0024', 'MS14_D03_S05_L0025']), 'v111:trial_latch_ok:MS14_D03_S05_L0020')
    $ r13_v111_commit('MS14_D03_S05_L0025')
    jump r13_v111_trial_stone

label r13_v111_trial_stone:
    call r13_v111_proof('마지막 점검과 인수한 돌을 연결한다',['E11', 'E15', 'E16'],'r13_v111_trial_stone_ok','r13_v111_trial_wrong_stone','r13_v111_trial_hint_stone')
    jump expression _return

label r13_v111_trial_stone_ok:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0027', 'MS14_D03_S05_L0028', 'MS14_D03_S05_L0029']), 'v111:trial_stone_ok:MS14_D03_S05_L0027')
    $ r13_v111_commit('MS14_D03_S05_L0029')
    jump r13_v111_badugi_arrives

label r13_v111_badugi_arrives:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_nw_meeting_end('lamp','win')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0030', 'MS14_D03_S05_L0032', 'MS14_D03_S05_L0033', 'MS14_D03_S05_L0034', 'MS14_D03_S05_L0036']), 'v111:badugi_arrives:MS14_D03_S05_L0030')
    jump r13_v111_trial_piko

label r13_v111_trial_piko:
    if r13_v111_value('piko_alive')==True:
        jump r13_v111_trial_alive
    jump r13_v111_trial_dead

label r13_v111_trial_alive:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0039']), 'v111:trial_alive:MS14_D03_S05_L0039')
    jump r13_v111_trial_choices

label r13_v111_trial_dead:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0037', 'MS14_D03_S05_L0038']), 'v111:trial_dead:MS14_D03_S05_L0037')
    jump r13_v111_trial_choices

label r13_v111_trial_choices:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0040', 'MS14_D03_S05_L0041', 'MS14_D03_S05_L0042', 'MS14_D03_S05_L0043', 'MS14_D03_S05_L0044', 'MS14_D03_S05_L0045', 'MS14_D03_S05_L0046', 'MS14_D03_S05_L0048']), 'v111:trial_choices:MS14_D03_S05_L0040')
    jump r13_v111_stone_choice

label r13_v111_stone_choice:
    $ v111_menu_owner='stone_choice'
    $ v111_menu=[('확인된 3번 돌을 돌려 달라고 한다',0) for _ in [0] if True] + [('오늘은 반환 요구를 보류한다',1) for _ in [0] if True]
    $ v111_answer=renpy.display_menu(v111_menu)
    if v111_answer==0:
        $ r13_v111_option('MS14_D03_S05_L0048_O1')
        jump r13_v111_stone_return
    if v111_answer==1:
        $ r13_v111_option('MS14_D03_S05_L0048_O2')
        jump r13_v111_stone_defer
    jump r13_v111_stone_choice

label r13_v111_stone_return:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0049', 'MS14_D03_S05_L0050', 'MS14_D03_S05_L0051']), 'v111:stone_return:MS14_D03_S05_L0049')
    $ r13_v111_commit('MS14_D03_S05_L0052')
    jump r13_v111_custody_choice

label r13_v111_stone_defer:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0053', 'MS14_D03_S05_L0054']), 'v111:stone_defer:MS14_D03_S05_L0053')
    $ r13_v111_commit('MS14_D03_S05_L0055')
    jump r13_v111_custody_choice

label r13_v111_custody_choice:
    # Partial or lost meeting: Silluk is only the one who sold a found stone.
    if r13_v111_value('meeting:lamp')!='win':
        $ r13_v111_set('silluk_status','released')
        jump r13_v111_restore_route
    $ v111_menu_owner='custody_choice'
    $ v111_menu=[('지금 데려가지 못하게 하고 내일 다시 나오게 한다',0) for _ in [0] if True] + [('증거를 넘기고 너울이 실룩을 데려가게 한다',1) for _ in [0] if True]
    $ v111_answer=renpy.display_menu(v111_menu)
    if v111_answer==0:
        $ r13_v111_option('MS14_D03_S05_L0056_O1')
        jump r13_v111_silluk_report
    if v111_answer==1:
        $ r13_v111_option('MS14_D03_S05_L0056_O2')
        jump r13_v111_silluk_transfer
    jump r13_v111_custody_choice

label r13_v111_silluk_report:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0057', 'MS14_D03_S05_L0058', 'MS14_D03_S05_L0059', 'MS14_D03_S05_L0060', 'MS14_D03_S05_L0061', 'MS14_D03_S05_L0062']), 'v111:silluk_report:MS14_D03_S05_L0057')
    $ r13_v111_commit('MS14_D03_S05_L0062')
    jump r13_v111_restore_route

label r13_v111_silluk_transfer:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0063', 'MS14_D03_S05_L0064', 'MS14_D03_S05_L0065', 'MS14_D03_S05_L0066']), 'v111:silluk_transfer:MS14_D03_S05_L0063')
    $ r13_v111_commit('MS14_D03_S05_L0067')
    # Neoul lists Silluk the same night to keep him quiet (plan 사건 03).
    $ r13_nw_list('resident_siluk','lamp_transfer')
    jump r13_v111_restore_route

label r13_v111_trial_wrong:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    if r13_nw_retry('lamp'):
        call r13_lines(r13_v111_lines(['MS14_D03_S05_L0071', 'MS14_D03_S05_L0072']), 'v111:trial_wrong:retry:MS14_D03_S05_L0071')
        jump r13_v111_trial_repair
    # New world (event 03): one presentation. Losing Tok's innocence (gate) ends the meeting.
    $ r13_nw_meeting_end('lamp','lose')
    $ r13_nw_list('resident_tok','lamp_lose')
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0071', 'MS14_D03_S05_L0072']), 'v111:trial_wrong:MS14_D03_S05_L0071')
    jump r13_v111_trial_choices

label r13_v111_trial_hint:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0073']), 'v111:trial_hint:MS14_D03_S05_L0073')
    jump r13_v111_trial_repair

label r13_v111_trial_wrong_sale:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    if r13_nw_retry('lamp'):
        call r13_lines(r13_v111_lines(['MS14_D03_S05_L0071', 'MS14_D03_S05_L0072']), 'v111:trial_wrong_sale:retry:MS14_D03_S05_L0071')
        jump r13_v111_trial_sale
    # New world (event 03): a lost later issue ends the meeting as partial.
    $ r13_nw_meeting_end('lamp','partial')
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0071', 'MS14_D03_S05_L0072']), 'v111:trial_wrong_sale:MS14_D03_S05_L0071')
    jump r13_v111_trial_choices

label r13_v111_trial_hint_sale:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0073']), 'v111:trial_hint_sale:MS14_D03_S05_L0073')
    jump r13_v111_trial_sale

label r13_v111_trial_wrong_latch:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    if r13_nw_retry('lamp'):
        call r13_lines(r13_v111_lines(['MS14_D03_S05_L0071', 'MS14_D03_S05_L0072']), 'v111:trial_wrong_latch:retry:MS14_D03_S05_L0071')
        jump r13_v111_trial_latch
    # New world (event 03): a lost later issue ends the meeting as partial.
    $ r13_nw_meeting_end('lamp','partial')
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0071', 'MS14_D03_S05_L0072']), 'v111:trial_wrong_latch:MS14_D03_S05_L0071')
    jump r13_v111_trial_choices

label r13_v111_trial_hint_latch:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0073']), 'v111:trial_hint_latch:MS14_D03_S05_L0073')
    jump r13_v111_trial_latch

label r13_v111_trial_wrong_stone:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    if r13_nw_retry('lamp'):
        call r13_lines(r13_v111_lines(['MS14_D03_S05_L0071', 'MS14_D03_S05_L0072']), 'v111:trial_wrong_stone:retry:MS14_D03_S05_L0071')
        jump r13_v111_trial_stone
    # New world (event 03): a lost later issue ends the meeting as partial.
    $ r13_nw_meeting_end('lamp','partial')
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0071', 'MS14_D03_S05_L0072']), 'v111:trial_wrong_stone:MS14_D03_S05_L0071')
    jump r13_v111_trial_choices

label r13_v111_trial_hint_stone:
    $ r13_v111_scene('MS14_D03_S05')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S05_L0073']), 'v111:trial_hint_stone:MS14_D03_S05_L0073')
    jump r13_v111_trial_stone

label r13_v111_restore_route:
    if r13_v111_value('public_stones')=='returned_uninstalled':
        jump r13_v111_restore_input
    jump r13_v111_restore_defer

label r13_v111_restore_input:
    call r13_v111_travel('square','restore_input')
    call r13_v111_wait('restore_input')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_restore3
    jump r13_v111_restore_input

label r13_v111_restore3:
    $ r13_edit(period=2)
    $ r13_v111_scene('MS14_D03_S06')
    call r13_v111_travel('square','restore3')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S06_L0002', 'MS14_D03_S06_L0003', 'MS14_D03_S06_L0004']), 'v111:restore3:MS14_D03_S06_L0002')
    $ r13_v111_commit('MS14_D03_S06_L0004')
    jump r13_v111_box_news3

label r13_v111_restore_defer:
    $ r13_edit(period=2)
    $ r13_v111_scene('MS14_D03_S06')
    call r13_v111_travel('square','restore_defer')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S06_L0006', 'MS14_D03_S06_L0007', 'MS14_D03_S06_L0008']), 'v111:restore_defer:MS14_D03_S06_L0006')
    jump r13_v111_box_news3

label r13_v111_box_news3:
    $ r13_edit(period=2)
    $ r13_v111_scene('MS14_D03_S06')
    call r13_v111_travel('square','box_news3')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S06_L0009', 'MS14_D03_S06_L0010', 'MS14_D03_S06_L0011']), 'v111:box_news3:MS14_D03_S06_L0009')
    jump r13_v111_memorial_route

label r13_v111_memorial_route:
    if r13_v111_value('piko_alive')==True:
        jump r13_v111_piko_evening
    jump r13_v111_piko_memorial

label r13_v111_piko_evening:
    $ r13_edit(period=2)
    $ r13_v111_scene('MS14_D03_S06')
    call r13_v111_travel('clinic','piko_evening')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S06_L0024', 'MS14_D03_S06_L0025', 'MS14_D03_S06_L0026', 'MS14_D03_S06_L0027', 'MS14_D03_S06_L0028', 'MS14_D03_S06_L0029', 'MS14_D03_S06_L0030']), 'v111:piko_evening:MS14_D03_S06_L0024')
    jump r13_v111_somi_lead

label r13_v111_piko_memorial:
    $ r13_edit(period=2)
    $ r13_v111_scene('MS14_D03_S06')
    call r13_v111_travel('square','piko_memorial')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S06_L0013', 'MS14_D03_S06_L0014', 'MS14_D03_S06_L0015', 'MS14_D03_S06_L0016', 'MS14_D03_S06_L0018', 'MS14_D03_S06_L0019', 'MS14_D03_S06_L0020', 'MS14_D03_S06_L0021', 'MS14_D03_S06_L0022']), 'v111:piko_memorial:MS14_D03_S06_L0013')
    $ r13_v111_commit('MS14_D03_S06_L0022')
    jump r13_v111_somi_lead

label r13_v111_somi_lead:
    $ r13_v111_scene('MS14_D03_S06')
    call r13_v111_travel('square','somi_lead')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S06_L0032', 'MS14_D03_S06_L0033']), 'v111:somi_lead:MS14_D03_S06_L0032')
    jump r13_v111_blankets_route

label r13_v111_blankets_route:
    if r13_v111_value('nero_bedding_reserved')==True:
        jump r13_v111_blankets_receive
    jump r13_v111_stairs3

label r13_v111_blankets_receive:
    call r13_v111_travel('square','blankets_receive')
    call r13_v111_wait('blankets_receive')
    $ v111_answer=_return
    if v111_answer==0:
        jump r13_v111_blankets3
    jump r13_v111_blankets_receive

label r13_v111_blankets3:
    $ r13_v111_scene('MS14_D03_S06')
    call r13_v111_travel('square','blankets3')
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D03_S06_L0035', 'MS14_D03_S06_L0037', 'MS14_D03_S06_L0038', 'MS14_D03_S06_L0039', 'MS14_D03_S06_L0040']), 'v111:blankets3:MS14_D03_S06_L0035')
    $ r13_v111_commit('MS14_D03_S06_L0041')
    jump r13_v111_stairs3

label r13_v111_stairs3:
    $ r13_edit(period=2)
    $ r13_v111_scene('MS14_D03_S06')
    call r13_v111_travel('room13','stairs3')
    $ r13_v111_score()
    jump r13_v111_sleep3

label r13_v111_sleep3:
    call r13_v111_travel('room13','sleep3')
    call r13_v111_wait('sleep3')
    $ v111_answer=_return
    if v111_answer==0:
        $ r13_v111_apply('option:sleep3:0',[{'op': 'set', 'field': 'day', 'value': 4}])
        jump r13_v111_day4
    jump r13_v111_sleep3
