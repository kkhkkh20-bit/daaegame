# Reviewed D06–D10 source IDs and explicit field/proof callbacks.

label r13_v111_day6:
    $ r13_v111_scene('MS14_D06_S01')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','day6',['daram'])
    $ r13_v111_arrive(['daram', 'resident_teacher', 'resident_lamplighter', 'kid_kkomi'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0002']),'v111:MS14_D06_S01_L0002')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0003']),'v111:MS14_D06_S01_L0003')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0004']),'v111:MS14_D06_S01_L0004')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0005']),'v111:MS14_D06_S01_L0005')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0006']),'v111:MS14_D06_S01_L0006')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0007']),'v111:MS14_D06_S01_L0007')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0008']),'v111:MS14_D06_S01_L0008')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0009']),'v111:MS14_D06_S01_L0009')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0010']),'v111:MS14_D06_S01_L0010')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0011']),'v111:MS14_D06_S01_L0011')
    $ r13_v111_commit('MS14_D06_S01_L0012')
    call r13_lines([("resident_teacher","낮 동안은 이쪽에 앉아 있어도 됩니다. 먹을 건 따로 챙겨 주세요.",{"no_lead":True})],"v111:school_day_permission")
    if r13_v111_value('carried_dry_blankets')==2:
        call r13_v111_blankets6
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0017']),'v111:MS14_D06_S01_L0017')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0018']),'v111:MS14_D06_S01_L0018')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0019']),'v111:MS14_D06_S01_L0019')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0020']),'v111:MS14_D06_S01_L0020')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0021']),'v111:MS14_D06_S01_L0021')
    # 0.20.9 (조연 검토 1·2): 혐의를 벗은 밤이의 평범한 자리, 들은 말을 스스로 고치는 콩이.
    if r13_v111_value('bami_status')=='cleared' and not r13_v111_value('listed:bami') and r13_v111_actor_ready('resident_teacher'):
        call r13_lines(r13_nw_block('bami_after5_6'),'nw:bami_after5_6')
    if r13_v111_value('alive:resident_kongi') is not False and not r13_v111_value('listed:resident_kongi') and r13_v111_actor_ready('daram'):
        call r13_lines(r13_nw_block('kongi_after4_6'),'nw:kongi_after4_6')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0022']),'v111:MS14_D06_S01_L0022')
    $ r13_v111_commit('MS14_D06_S01_L0023')
    menu:
        '그릇을 돌려주러 같이 가자.':
            $ r13_v111_set('choice:MS14_D06_S01','together')
            $ r13_v111_commit('MS14_D06_S01_L0025')
            jump r13_v111_bowl_together6
        '오늘은 먹었니? 먹을 것부터 알아보자.':  # 0.20.7 (review 6-12 #2): care, not a promise
            $ r13_v111_set('choice:MS14_D06_S01','eat_first')
            $ r13_v111_commit('MS14_D06_S01_L0025')
            jump r13_v111_bowl_eat6

label r13_v111_blankets6:
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0013']),'v111:MS14_D06_S01_L0013')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0014']),'v111:MS14_D06_S01_L0014')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0015']),'v111:MS14_D06_S01_L0015')
    $ r13_v111_commit('MS14_D06_S01_L0016')
    return

label r13_v111_bowl_together6:
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0026']),'v111:MS14_D06_S01_L0026')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0027']),'v111:MS14_D06_S01_L0027')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0028']),'v111:MS14_D06_S01_L0028')
    $ r13_v111_commit('MS14_D06_S01_L0029')
    jump r13_v111_nabi_supply6

label r13_v111_bowl_eat6:
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0030']),'v111:MS14_D06_S01_L0030')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0031']),'v111:MS14_D06_S01_L0031')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0032']),'v111:MS14_D06_S01_L0032')
    $ r13_v111_commit('MS14_D06_S01_L0033')
    jump r13_v111_nabi_supply6

label r13_v111_nabi_supply6:
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0034']),'v111:MS14_D06_S01_L0034')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0036']),'v111:MS14_D06_S01_L0036')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0037']),'v111:MS14_D06_S01_L0037')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0038']),'v111:MS14_D06_S01_L0038')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0039']),'v111:MS14_D06_S01_L0039')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0040']),'v111:MS14_D06_S01_L0040')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0041']),'v111:MS14_D06_S01_L0041')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0042']),'v111:MS14_D06_S01_L0042')
    call r13_v111_travel('dining','supply6')
    jump r13_v111_board6

label r13_v111_board6:
    call r13_v111_wait('board6')
    if _return==0:
        jump r13_v111_board_done6
    jump r13_v111_board6

label r13_v111_board_done6:
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0044']),'v111:MS14_D06_S01_L0044')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0045']),'v111:MS14_D06_S01_L0045')
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0046']),'v111:MS14_D06_S01_L0046')
    $ r13_v111_commit('MS14_D06_S01_L0048')
    jump r13_v111_woodshed6

label r13_v111_woodshed6:
    $ r13_v111_scene('MS14_D06_S02')
    $ r13_edit(period=1)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('v111_woodshed','woodshed6',['daram'])
    $ r13_v111_arrive(['daram', 'kid_kkomi', 'resident_bori'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0002']),'v111:MS14_D06_S02_L0002')
    $ r13_nw_acquire("NW_KKOMI_NOSTONE")
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0003']),'v111:MS14_D06_S02_L0003')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0004']),'v111:MS14_D06_S02_L0004')
    jump r13_v111_woodshed_check6

label r13_v111_woodshed_check6:
    call r13_v111_wait('woodshed_check6')
    if _return==0:
        jump r13_v111_woodshed_seen6
    jump r13_v111_woodshed_check6

label r13_v111_woodshed_seen6:
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0006']),'v111:MS14_D06_S02_L0006')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0007']),'v111:MS14_D06_S02_L0007')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0008']),'v111:MS14_D06_S02_L0008')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0009']),'v111:MS14_D06_S02_L0009')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0011']),'v111:MS14_D06_S02_L0011')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0012']),'v111:MS14_D06_S02_L0012')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0013']),'v111:MS14_D06_S02_L0013')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0014']),'v111:MS14_D06_S02_L0014')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0016']),'v111:MS14_D06_S02_L0016')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0017']),'v111:MS14_D06_S02_L0017')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0018']),'v111:MS14_D06_S02_L0018')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0019']),'v111:MS14_D06_S02_L0019')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0020']),'v111:MS14_D06_S02_L0020')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0021']),'v111:MS14_D06_S02_L0021')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0022']),'v111:MS14_D06_S02_L0022')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0023']),'v111:MS14_D06_S02_L0023')
    $ r13_v111_commit('MS14_D06_S02_L0024')
    menu:
        '오늘 안에 학교 자리를 확인하고 옮긴다.':
            $ r13_v111_set('choice:MS14_D06_S02','today')
            $ r13_v111_commit('MS14_D06_S02_L0026')
            jump r13_v111_today6
        '허락을 받아 두고, 아이들은 내일 아침 데리러 온다.':  # 0.20.7 (review 6-12 #1): the time span is said before
            $ r13_v111_set('choice:MS14_D06_S02','permission')
            $ r13_v111_commit('MS14_D06_S02_L0026')
            jump r13_v111_permission6

label r13_v111_today6:
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0027']),'v111:MS14_D06_S02_L0027')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0028']),'v111:MS14_D06_S02_L0028')
    $ r13_v111_commit('MS14_D06_S02_L0029')
    jump r13_v111_permission_today6

label r13_v111_permission6:
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0030']),'v111:MS14_D06_S02_L0030')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0031']),'v111:MS14_D06_S02_L0031')
    call r13_lines(r13_v111_lines(['MS14_D06_S02_L0032']),'v111:MS14_D06_S02_L0032')
    $ r13_v111_commit('MS14_D06_S02_L0033')
    jump r13_v111_fire6

label r13_v111_permission_today6:
    $ r13_v111_scene('MS14_D06_P01')
    $ r13_edit(period=1)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','permission_today6',['daram'])
    $ r13_v111_arrive(['daram', 'resident_teacher', 'doto', 'kid_kkomi'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0001']),'v111:MS14_D06_P01_L0001')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0002']),'v111:MS14_D06_P01_L0002')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0003']),'v111:MS14_D06_P01_L0003')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0004']),'v111:MS14_D06_P01_L0004')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0005']),'v111:MS14_D06_P01_L0005')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0006']),'v111:MS14_D06_P01_L0006')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0007']),'v111:MS14_D06_P01_L0007')
    $ r13_v111_commit('MS14_D06_P01_L0008')
    call r13_v111_travel('v111_woodshed','children_fetch6')
    jump r13_v111_acorn_recover6

label r13_v111_acorn_recover6:
    call r13_v111_wait('acorn_recover6')
    if _return==0:
        jump r13_v111_acorn_recovered6
    jump r13_v111_acorn_recover6

label r13_v111_acorn_recovered6:
    call r13_lines([(None,"꼬미가 깡통에서 도토리를 꺼내 손에 쥐었다.")],"v111:acorn_recovered")
    $ r13_v111_set("acorn_recovered",True)
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0009']),'v111:MS14_D06_P01_L0009')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0010']),'v111:MS14_D06_P01_L0010')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0011']),'v111:MS14_D06_P01_L0011')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0012']),'v111:MS14_D06_P01_L0012')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0013']),'v111:MS14_D06_P01_L0013')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0014']),'v111:MS14_D06_P01_L0014')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0015']),'v111:MS14_D06_P01_L0015')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0016']),'v111:MS14_D06_P01_L0016')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0017']),'v111:MS14_D06_P01_L0017')
    call r13_v111_travel('school','children_handoff6')
    jump r13_v111_handoff6

label r13_v111_handoff6:
    call r13_v111_wait('handoff6')
    if _return==0:
        jump r13_v111_handoff_done6
    jump r13_v111_handoff6

label r13_v111_handoff_done6:
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0019']),'v111:MS14_D06_P01_L0019')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0020']),'v111:MS14_D06_P01_L0020')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0021']),'v111:MS14_D06_P01_L0021')
    call r13_lines(r13_v111_lines(['MS14_D06_P01_L0022']),'v111:MS14_D06_P01_L0022')
    $ r13_v111_commit('MS14_D06_P01_L0024')
    jump r13_v111_empty_fire6

label r13_v111_empty_fire6:
    $ r13_v111_scene('MS14_D06_S03P')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('v111_fire','empty_fire6',[])
    $ r13_v111_arrive(['resident_bori', 'doto'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D06_S03P_L0001']),'v111:MS14_D06_S03P_L0001')
    call r13_lines(r13_v111_lines(['MS14_D06_S03P_L0002']),'v111:MS14_D06_S03P_L0002')
    call r13_lines(r13_v111_lines(['MS14_D06_S03P_L0003']),'v111:MS14_D06_S03P_L0003')
    call r13_lines(r13_v111_lines(['MS14_D06_S03P_L0004']),'v111:MS14_D06_S03P_L0004')
    call r13_lines(r13_v111_lines(['MS14_D06_S03P_L0005']),'v111:MS14_D06_S03P_L0005')
    call r13_lines(r13_v111_lines(['MS14_D06_S03P_L0006']),'v111:MS14_D06_S03P_L0006')
    call r13_lines(r13_v111_lines(['MS14_D06_S03P_L0007']),'v111:MS14_D06_S03P_L0007')
    $ r13_v111_commit('MS14_D06_S03P_L0008')
    jump r13_v111_after_fire6

label r13_v111_fire6:
    $ r13_v111_scene('MS14_D06_S03')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('v111_fire','fire6',['daram'])
    $ r13_v111_arrive(['daram', 'resident_bori'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0002']),'v111:MS14_D06_S03_L0002')
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0003']),'v111:MS14_D06_S03_L0003')
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0004']),'v111:MS14_D06_S03_L0004')
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0005']),'v111:MS14_D06_S03_L0005')
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0006']),'v111:MS14_D06_S03_L0006')
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0007']),'v111:MS14_D06_S03_L0007')
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0008']),'v111:MS14_D06_S03_L0008')
    call r13_v111_travel('school','children_safe6')
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0010']),'v111:MS14_D06_S03_L0010')
    call r13_v111_travel('v111_fire','rescue6')
    jump r13_v111_wet_cloth6

label r13_v111_wet_cloth6:
    call r13_v111_wait('wet_cloth6')
    if _return==0:
        jump r13_v111_wet_done6
    jump r13_v111_wet_cloth6

label r13_v111_wet_done6:
    jump r13_v111_clear_wood6

label r13_v111_clear_wood6:
    call r13_v111_wait('clear_wood6')
    if _return==0:
        jump r13_v111_rescue_done6
    jump r13_v111_clear_wood6

label r13_v111_rescue_done6:
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0012']),'v111:MS14_D06_S03_L0012')
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0013']),'v111:MS14_D06_S03_L0013')
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0014']),'v111:MS14_D06_S03_L0014')
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0015']),'v111:MS14_D06_S03_L0015')
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0016']),'v111:MS14_D06_S03_L0016')
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0017']),'v111:MS14_D06_S03_L0017')
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0018']),'v111:MS14_D06_S03_L0018')
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0019']),'v111:MS14_D06_S03_L0019')
    call r13_lines(r13_v111_lines(['MS14_D06_S03_L0020']),'v111:MS14_D06_S03_L0020')
    $ r13_v111_commit('MS14_D06_S03_L0022')
    jump r13_v111_after_fire6

label r13_v111_after_fire6:
    $ r13_v111_scene('MS14_D06_S04')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','after_fire6',['daram'])
    $ r13_v111_arrive(['daram', 'nabi', 'resident_bori', 'neoul', 'doto'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0001']),'v111:MS14_D06_S04_L0001')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0002']),'v111:MS14_D06_S04_L0002')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0003']),'v111:MS14_D06_S04_L0003')
    $ r13_v111_commit('MS14_D06_S04_L0005')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0006']),'v111:MS14_D06_S04_L0006')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0007']),'v111:MS14_D06_S04_L0007')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0008']),'v111:MS14_D06_S04_L0008')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0009']),'v111:MS14_D06_S04_L0009')
    $ r13_v111_commit('MS14_D06_S04_L0010')
    if r13_v111_value('FIRE_EVACUATED'):
        call r13_v111_bori_unhurt6
    else:
        call r13_v111_bori_burned6
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0019']),'v111:MS14_D06_S04_L0019')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0020']),'v111:MS14_D06_S04_L0020')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0021']),'v111:MS14_D06_S04_L0021')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0022']),'v111:MS14_D06_S04_L0022')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0023']),'v111:MS14_D06_S04_L0023')
    $ r13_v111_commit('MS14_D06_S04_L0024')
    if r13_v111_value('FIRE_EVACUATED'):
        call r13_v111_empty_testimony6
    else:
        call r13_v111_rescue_testimony6
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0031']),'v111:MS14_D06_S04_L0031')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0032']),'v111:MS14_D06_S04_L0032')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0033']),'v111:MS14_D06_S04_L0033')
    call r13_v111_travel('v111_ruin','cold_fire6')
    jump r13_v111_fire_evidence6

label r13_v111_bori_unhurt6:
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0015']),'v111:MS14_D06_S04_L0015')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0016']),'v111:MS14_D06_S04_L0016')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0017']),'v111:MS14_D06_S04_L0017')
    $ r13_v111_commit('MS14_D06_S04_L0018')
    return

label r13_v111_bori_burned6:
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0011']),'v111:MS14_D06_S04_L0011')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0012']),'v111:MS14_D06_S04_L0012')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0013']),'v111:MS14_D06_S04_L0013')
    $ r13_v111_commit('MS14_D06_S04_L0014')
    return

label r13_v111_empty_testimony6:
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0028']),'v111:MS14_D06_S04_L0028')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0029']),'v111:MS14_D06_S04_L0029')
    $ r13_v111_commit('MS14_D06_S04_L0030')
    return

label r13_v111_rescue_testimony6:
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0025']),'v111:MS14_D06_S04_L0025')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0026']),'v111:MS14_D06_S04_L0026')
    $ r13_v111_commit('MS14_D06_S04_L0027')
    return

label r13_v111_fire_evidence6:
    call r13_v111_wait('fire_evidence6')
    if _return==0:
        jump r13_v111_fire_record6
    jump r13_v111_fire_evidence6

label r13_v111_fire_record6:
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0034']),'v111:MS14_D06_S04_L0034')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0035']),'v111:MS14_D06_S04_L0035')
    $ r13_v111_commit('MS14_D06_S04_L0037')
    call r13_v111_travel('school','return_school6')

label r13_v111_bowl_result6:
    if r13_v111_value('KKOMI_ALIVE'):
        jump r13_v111_four_bowls6
    jump r13_v111_empty_bowl6

label r13_v111_four_bowls6:
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0044']),'v111:MS14_D06_S04_L0044')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0045']),'v111:MS14_D06_S04_L0045')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0046']),'v111:MS14_D06_S04_L0046')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0047']),'v111:MS14_D06_S04_L0047')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0048']),'v111:MS14_D06_S04_L0048')
    $ r13_v111_commit('MS14_D06_S04_L0049')
    jump r13_v111_sleep6

label r13_v111_empty_bowl6:
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0038']),'v111:MS14_D06_S04_L0038')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0039']),'v111:MS14_D06_S04_L0039')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0040']),'v111:MS14_D06_S04_L0040')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0041']),'v111:MS14_D06_S04_L0041')
    call r13_lines(r13_v111_lines(['MS14_D06_S04_L0042']),'v111:MS14_D06_S04_L0042')
    $ r13_v111_commit('MS14_D06_S04_L0043')
    jump r13_v111_sleep6

label r13_v111_sleep6:
    call r13_v111_travel('school','sleep6')
    jump r13_v111_sleep6_input

label r13_v111_sleep6_input:
    call r13_v111_wait('sleep6_input')
    if _return==0:
        jump r13_v111_sleep6_done
    jump r13_v111_sleep6_input

label r13_v111_sleep6_done:
    $ r13_v111_set("day",7)
    jump r13_v111_day7

label r13_v111_day7:
    $ r13_v111_scene('MS14_D07_S01')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('laundry','day7',[])
    $ r13_v111_arrive(['resident_nubi', 'resident_bori', 'nabi'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0002']),'v111:MS14_D07_S01_L0002')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0003']),'v111:MS14_D07_S01_L0003')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0004']),'v111:MS14_D07_S01_L0004')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0006']),'v111:MS14_D07_S01_L0006')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0007']),'v111:MS14_D07_S01_L0007')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0008']),'v111:MS14_D07_S01_L0008')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0009']),'v111:MS14_D07_S01_L0009')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0010']),'v111:MS14_D07_S01_L0010')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0011']),'v111:MS14_D07_S01_L0011')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0012']),'v111:MS14_D07_S01_L0012')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0013']),'v111:MS14_D07_S01_L0013')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0014']),'v111:MS14_D07_S01_L0014')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0015']),'v111:MS14_D07_S01_L0015')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0016']),'v111:MS14_D07_S01_L0016')
    $ r13_v111_commit('MS14_D07_S01_L0017')
    menu:
        '아이들은 학교에서 기다리게 하자.':
            $ r13_v111_set('choice:MS14_D07_S01','school')
            $ r13_v111_commit('MS14_D07_S01_L0019')
            jump r13_v111_children_school7
        '여기서 계속 묻는다.':
            $ r13_v111_set('choice:MS14_D07_S01','here')
            $ r13_v111_commit('MS14_D07_S01_L0019')
            jump r13_v111_children_here7

label r13_v111_children_school7:
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0020']),'v111:MS14_D07_S01_L0020')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0021']),'v111:MS14_D07_S01_L0021')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0022']),'v111:MS14_D07_S01_L0022')
    jump r13_v111_nubi_children_school7

label r13_v111_children_here7:
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0025']),'v111:MS14_D07_S01_L0025')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0026']),'v111:MS14_D07_S01_L0026')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0027']),'v111:MS14_D07_S01_L0027')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0028']),'v111:MS14_D07_S01_L0028')
    $ r13_v111_commit('MS14_D07_S01_L0029')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0020']),'v111:MS14_D07_S01_L0020')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0021']),'v111:MS14_D07_S01_L0021')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0022']),'v111:MS14_D07_S01_L0022')
    jump r13_v111_nubi_children_school7

label r13_v111_nubi_children_school7:
    call r13_v111_travel('school','nubi_children_school7',[])
    $ r13_v111_arrive(["nabi","resident_teacher","kid_nubi1","kid_nubi2","kid_nubi3"])
    jump r13_v111_nubi_children_receipt7

label r13_v111_nubi_children_receipt7:
    call r13_v111_wait('nubi_children_receipt7')
    if _return==0:
        jump r13_v111_nubi_children_received7
    jump r13_v111_nubi_children_receipt7

label r13_v111_nubi_children_received7:
    $ r13_v111_commit('MS14_D07_S01_L0024')
    call r13_lines(r13_nw_block('nubi_children_received7'),'nw:nubi_children_received7')  # 0.20.6: the hand-over is seen
    call r13_v111_travel('laundry','nubi_children_received7',[])
    $ r13_v111_arrive(["resident_nubi","resident_bori"])
    jump r13_v111_bori_witness7

label r13_v111_bori_witness7:
    call r13_v111_wait('bori_witness7')
    if _return==0:
        jump r13_v111_bori_witness_heard7
    jump r13_v111_bori_witness7

label r13_v111_bori_witness_heard7:
    call r13_lines([("resident_bori","불이 번지기 전에 누비 씨가 창고 문 앞에 서 있는 건 봤소.",{"no_lead":True})],"v111:bori_fire_door_witness")
    $ r13_v111_set("bori_nubi_door_witness_heard",True)
    jump r13_v111_nubi_proof7

label r13_v111_nubi_proof7:
    call r13_v111_proof('불이 시작된 곳과 진술을 대조한다',['E06_FIRE'],'r13_v111_nubi_admission7','r13_v111_nubi_wrong7',None)
    jump expression _return

label r13_v111_nubi_wrong7:
    if r13_nw_retry("fire"):
        call r13_lines(r13_v111_lines(["MS14_D07_S01_L0046","MS14_D07_S01_L0047"]),"v111:nubi_wrong7:retry")
        jump r13_v111_nubi_proof7
    $ r13_nw_meeting_end("fire","lose")
    $ r13_nw_list("resident_bori","fire_lose")
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0046']),'v111:MS14_D07_S01_L0046')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0047']),'v111:MS14_D07_S01_L0047')
    jump r13_v111_responsibility7

label r13_v111_nubi_admission7:
    if not r13_v111_value("bori_nubi_door_witness_heard"):
        jump r13_v111_bori_witness7
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0030']),'v111:MS14_D07_S01_L0030')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0031']),'v111:MS14_D07_S01_L0031')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0032']),'v111:MS14_D07_S01_L0032')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0033']),'v111:MS14_D07_S01_L0033')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0034']),'v111:MS14_D07_S01_L0034')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0035']),'v111:MS14_D07_S01_L0035')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0036']),'v111:MS14_D07_S01_L0036')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0037']),'v111:MS14_D07_S01_L0037')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0038']),'v111:MS14_D07_S01_L0038')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0039']),'v111:MS14_D07_S01_L0039')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0040']),'v111:MS14_D07_S01_L0040')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0041']),'v111:MS14_D07_S01_L0041')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0042']),'v111:MS14_D07_S01_L0042')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0043']),'v111:MS14_D07_S01_L0043')
    call r13_lines(r13_v111_lines(['MS14_D07_S01_L0044']),'v111:MS14_D07_S01_L0044')
    $ r13_v111_commit('MS14_D07_S01_L0045')
    jump r13_v111_responsibility7

label r13_v111_responsibility7:
    $ r13_v111_scene('MS14_D07_S02')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','responsibility7',[])
    $ r13_v111_arrive(['nabi', 'resident_bori', 'resident_nubi', 'neoul'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0001']),'v111:MS14_D07_S02_L0001')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0002']),'v111:MS14_D07_S02_L0002')
    if r13_v111_value("meeting:fire")=="lose":
        jump r13_v111_responsibility_answers7

label r13_v111_fire_basis_route7:
    if r13_v111_value('FIRE_EVACUATED'):
        jump r13_v111_empty_fire_basis7
    jump r13_v111_rescue_fire_basis7

label r13_v111_empty_fire_basis7:
    call r13_v111_proof('불의 원인과 빈 창고 진압을 구분한다',['E06_FIRE', 'E06_EMPTY', 'E07_NUBI'],'r13_v111_responsibility_answers7','r13_v111_responsibility_wrong7',None)
    jump expression _return

label r13_v111_rescue_fire_basis7:
    call r13_v111_proof('불의 원인과 아이 구조를 구분한다',['E06_FIRE', 'E06_RESCUE', 'E07_NUBI'],'r13_v111_responsibility_answers7','r13_v111_responsibility_wrong7',None)
    jump expression _return

label r13_v111_responsibility_wrong7:
    if r13_nw_retry("fire",["E06_FIRE","E06_EMPTY","E07_NUBI"] if r13_v111_value("FIRE_EVACUATED") else ["E06_FIRE","E06_RESCUE","E07_NUBI"],"너울이 고개를 젓는다. 불의 원인과 그날 밤 일을 함께 묶어야 한다."):
        jump r13_v111_fire_basis_route7
    $ r13_nw_meeting_end("fire","partial")
    $ r13_nw_list("resident_bori","fire_partial")
    jump r13_v111_responsibility_answers7

label r13_v111_responsibility_answers7:
    $ r13_nw_meeting_end("fire","win")
    if r13_v111_value("meeting:fire")=="win":
        $ r13_v111_set("fire_neoul_promise_recorded",True)
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0004']),'v111:MS14_D07_S02_L0004')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0005']),'v111:MS14_D07_S02_L0005')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0006']),'v111:MS14_D07_S02_L0006')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0007']),'v111:MS14_D07_S02_L0007')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0008']),'v111:MS14_D07_S02_L0008')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0009']),'v111:MS14_D07_S02_L0009')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0010']),'v111:MS14_D07_S02_L0010')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0011']),'v111:MS14_D07_S02_L0011')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0012']),'v111:MS14_D07_S02_L0012')
    $ r13_v111_commit('MS14_D07_S02_L0014')
    jump r13_v111_school_names7

label r13_v111_school_names7:
    call r13_v111_wait('school_names7')
    if _return==0:
        jump r13_v111_school_names_done7
    jump r13_v111_school_names7

label r13_v111_school_names_done7:
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0015']),'v111:MS14_D07_S02_L0015')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0016']),'v111:MS14_D07_S02_L0016')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0017']),'v111:MS14_D07_S02_L0017')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0018']),'v111:MS14_D07_S02_L0018')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0019']),'v111:MS14_D07_S02_L0019')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0020']),'v111:MS14_D07_S02_L0020')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0021']),'v111:MS14_D07_S02_L0021')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0022']),'v111:MS14_D07_S02_L0022')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0023']),'v111:MS14_D07_S02_L0023')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0024']),'v111:MS14_D07_S02_L0024')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0025']),'v111:MS14_D07_S02_L0025')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0026']),'v111:MS14_D07_S02_L0026')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0028']),'v111:MS14_D07_S02_L0028')
    $ r13_v111_commit('MS14_D07_S02_L0029')
    if r13_v111_value('KKOMI_ALIVE'):
        call r13_v111_living_child7
    else:
        call r13_v111_lost_child7
    $ r13_v111_join(['doto'])
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0038']),'v111:MS14_D07_S02_L0038')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0039']),'v111:MS14_D07_S02_L0039')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0040']),'v111:MS14_D07_S02_L0040')
    $ r13_v111_join(['resident_lamplighter'])
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0041']),'v111:MS14_D07_S02_L0041')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0042']),'v111:MS14_D07_S02_L0042')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0043']),'v111:MS14_D07_S02_L0043')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0044']),'v111:MS14_D07_S02_L0044')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0045']),'v111:MS14_D07_S02_L0045')
    $ r13_v111_commit('MS14_D07_S02_L0046')
    jump r13_v111_room_visit7

label r13_v111_living_child7:
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0034']),'v111:MS14_D07_S02_L0034')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0035']),'v111:MS14_D07_S02_L0035')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0036']),'v111:MS14_D07_S02_L0036')
    $ r13_v111_commit('MS14_D07_S02_L0037')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0049']),'v111:MS14_D07_S02_L0049')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0050']),'v111:MS14_D07_S02_L0050')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0051']),'v111:MS14_D07_S02_L0051')
    $ r13_v111_commit('MS14_D07_S02_L0052')
    return

label r13_v111_lost_child7:
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0030']),'v111:MS14_D07_S02_L0030')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0031']),'v111:MS14_D07_S02_L0031')
    call r13_lines(r13_v111_lines(['MS14_D07_S02_L0032']),'v111:MS14_D07_S02_L0032')
    $ r13_v111_commit('MS14_D07_S02_L0033')
    return

label r13_v111_room_visit7:
    $ r13_v111_scene('MS14_D07_S03')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('room13','room_visit7',['daram'])
    $ r13_v111_arrive(['daram', 'granny', 'resident_owlgp', 'doto', 'karo'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0002']),'v111:MS14_D07_S03_L0002')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0003']),'v111:MS14_D07_S03_L0003')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0004']),'v111:MS14_D07_S03_L0004')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0005']),'v111:MS14_D07_S03_L0005')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0006']),'v111:MS14_D07_S03_L0006')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0007']),'v111:MS14_D07_S03_L0007')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0008']),'v111:MS14_D07_S03_L0008')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0009']),'v111:MS14_D07_S03_L0009')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0010']),'v111:MS14_D07_S03_L0010')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0011']),'v111:MS14_D07_S03_L0011')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0012']),'v111:MS14_D07_S03_L0012')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0013']),'v111:MS14_D07_S03_L0013')
    $ r13_v111_commit('MS14_D07_S03_L0014')
    menu:
        '다람과 남고 까로를 의료진에게 보낸다':
            $ r13_v111_set('route7','prevented')
            $ r13_v111_set('prevention','A')
            $ r13_v111_set('choice:MS14_D07_S03','A')
            $ r13_v111_commit('MS14_D07_S03_L0016')
            jump r13_v111_stay7
        '다람과 함께 의료진을 데리러 간다':
            $ r13_v111_set('route7','prevented')
            $ r13_v111_set('prevention','B')
            $ r13_v111_set('choice:MS14_D07_S03','B')
            $ r13_v111_commit('MS14_D07_S03_L0016')
            jump r13_v111_take7
        '다람을 도토에게 맡기고 의료진을 데리러 간다':
            $ r13_v111_set('route7','murder')
            $ r13_v111_set('choice:MS14_D07_S03','C')
            $ r13_v111_commit('MS14_D07_S03_L0016')
            jump r13_v111_handover7

label r13_v111_stay7:
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0017']),'v111:MS14_D07_S03_L0017')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0018']),'v111:MS14_D07_S03_L0018')
    $ r13_v111_commit('MS14_D07_S03_L0019')
    jump r13_v111_prevent_a7

label r13_v111_take7:
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0020']),'v111:MS14_D07_S03_L0020')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0021']),'v111:MS14_D07_S03_L0021')
    $ r13_v111_commit('MS14_D07_S03_L0022')
    jump r13_v111_prevent_b7

label r13_v111_handover7:
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0023']),'v111:MS14_D07_S03_L0023')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0024']),'v111:MS14_D07_S03_L0024')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0025']),'v111:MS14_D07_S03_L0025')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0026']),'v111:MS14_D07_S03_L0026')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0027']),'v111:MS14_D07_S03_L0027')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0028']),'v111:MS14_D07_S03_L0028')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0029']),'v111:MS14_D07_S03_L0029')
    call r13_lines(r13_v111_lines(['MS14_D07_S03_L0030']),'v111:MS14_D07_S03_L0030')
    $ r13_v111_commit('MS14_D07_S03_L0031')
    jump r13_v111_incident7

label r13_v111_prevent_a7:
    $ r13_v111_scene('MS14_D07_P01')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('room13','prevent_a7',['daram'])
    $ r13_v111_arrive(['daram', 'doto', 'resident_owlgp', 'karo'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D07_P01_L0001']),'v111:MS14_D07_P01_L0001')
    call r13_lines(r13_v111_lines(['MS14_D07_P01_L0002']),'v111:MS14_D07_P01_L0002')
    call r13_lines(r13_v111_lines(['MS14_D07_P01_L0003']),'v111:MS14_D07_P01_L0003')
    call r13_lines(r13_v111_lines(['MS14_D07_P01_L0004']),'v111:MS14_D07_P01_L0004')
    call r13_lines(r13_v111_lines(['MS14_D07_P01_L0005']),'v111:MS14_D07_P01_L0005')
    call r13_lines(r13_v111_lines(['MS14_D07_P01_L0006']),'v111:MS14_D07_P01_L0006')
    call r13_lines(r13_v111_lines(['MS14_D07_P01_L0007']),'v111:MS14_D07_P01_L0007')
    call r13_lines(r13_v111_lines(['MS14_D07_P01_L0008']),'v111:MS14_D07_P01_L0008')
    call r13_lines(r13_v111_lines(['MS14_D07_P01_L0009']),'v111:MS14_D07_P01_L0009')
    call r13_lines(r13_v111_lines(['MS14_D07_P01_L0010']),'v111:MS14_D07_P01_L0010')
    call r13_lines(r13_v111_lines(['MS14_D07_P01_L0011']),'v111:MS14_D07_P01_L0011')
    call r13_lines(r13_v111_lines(['MS14_D07_P01_L0012']),'v111:MS14_D07_P01_L0012')
    call r13_lines(r13_v111_lines(['MS14_D07_P01_L0013']),'v111:MS14_D07_P01_L0013')
    $ r13_v111_commit('MS14_D07_P01_L0014')
    jump r13_v111_sleep7

label r13_v111_prevent_b7:
    $ r13_v111_scene('MS14_D07_P02')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('room13','prevent_b7_room',['daram'])
    $ r13_v111_arrive(['daram', 'doto', 'resident_owlgp', 'karo'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0001']),'v111:MS14_D07_P02_L0001')
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0002']),'v111:MS14_D07_P02_L0002')
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0003']),'v111:MS14_D07_P02_L0003')
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0004']),'v111:MS14_D07_P02_L0004')
    call r13_v111_travel('clinic','prevent_b7',['daram'])
    $ r13_v111_arrive(['daram', 'karo', 'resident_seori'])
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0006']),'v111:MS14_D07_P02_L0006')
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0007']),'v111:MS14_D07_P02_L0007')
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0008']),'v111:MS14_D07_P02_L0008')
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0011']),'v111:MS14_D07_P02_L0011')
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0012']),'v111:MS14_D07_P02_L0012')
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0013']),'v111:MS14_D07_P02_L0013')
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0014']),'v111:MS14_D07_P02_L0014')
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0015']),'v111:MS14_D07_P02_L0015')
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0016']),'v111:MS14_D07_P02_L0016')
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0017']),'v111:MS14_D07_P02_L0017')
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0019']),'v111:MS14_D07_P02_L0019')
    call r13_lines(r13_v111_lines(['MS14_D07_P02_L0020']),'v111:MS14_D07_P02_L0020')
    $ r13_v111_commit('MS14_D07_P02_L0021')
    jump r13_v111_sleep7

label r13_v111_incident7:
    $ r13_v111_scene('MS14_D07_S04')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('gate','incident7',[])
    $ r13_v111_arrive(['karo', 'resident_seori', 'doto', 'nabi'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0002']),'v111:MS14_D07_S04_L0002')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0003']),'v111:MS14_D07_S04_L0003')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0004']),'v111:MS14_D07_S04_L0004')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0005']),'v111:MS14_D07_S04_L0005')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0006']),'v111:MS14_D07_S04_L0006')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0007']),'v111:MS14_D07_S04_L0007')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0008']),'v111:MS14_D07_S04_L0008')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0009']),'v111:MS14_D07_S04_L0009')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0012']),'v111:MS14_D07_S04_L0012')
    call r13_v111_travel('room13','incident_room7')
    $ r13_v111_arrive(['karo', 'resident_seori', 'doto', 'nabi'])
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0013']),'v111:MS14_D07_S04_L0013')
    $ r13_v111_join(['granny'])
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0014']),'v111:MS14_D07_S04_L0014')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0016']),'v111:MS14_D07_S04_L0016')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0017']),'v111:MS14_D07_S04_L0017')
    $ r13_v111_join(['neoul'])
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0018']),'v111:MS14_D07_S04_L0018')
    $ r13_v111_join(['daram'])
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0020']),'v111:MS14_D07_S04_L0020')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0021']),'v111:MS14_D07_S04_L0021')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0022']),'v111:MS14_D07_S04_L0022')
    # 0.20.6 (owner suggestion, days 2-14 #3): rescue -> the child in Dad's arms -> only then the
    # investigator's question about the scream (was asked at the door, mid-rescue).
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0010']),'v111:MS14_D07_S04_L0010')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0011']),'v111:MS14_D07_S04_L0011')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0023']),'v111:MS14_D07_S04_L0023')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0024']),'v111:MS14_D07_S04_L0024')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0025']),'v111:MS14_D07_S04_L0025')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0026']),'v111:MS14_D07_S04_L0026')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0027']),'v111:MS14_D07_S04_L0027')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0028']),'v111:MS14_D07_S04_L0028')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0029']),'v111:MS14_D07_S04_L0029')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0030']),'v111:MS14_D07_S04_L0030')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0031']),'v111:MS14_D07_S04_L0031')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0033']),'v111:MS14_D07_S04_L0033')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0034']),'v111:MS14_D07_S04_L0034')
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0035']),'v111:MS14_D07_S04_L0035')
    $ r13_v111_commit('MS14_D07_S04_L0036')
    jump r13_v111_sleep7

label r13_v111_sleep7:
    if r13_v111_value("DARAM_DETAINED"):
        jump r13_v111_detained_sleep7
    jump r13_v111_free_sleep7

label r13_v111_free_sleep7:
    call r13_v111_travel('school','free_sleep7')
    jump r13_v111_free_sleep7_input

label r13_v111_free_sleep7_input:
    call r13_v111_wait('free_sleep7_input')
    if _return==0:
        jump r13_v111_free_sleep7_done
    jump r13_v111_free_sleep7_input

label r13_v111_free_sleep7_done:
    $ r13_v111_set("day",8)
    jump r13_v111_day8

label r13_v111_detained_sleep7:
    call r13_v111_travel('room13','detained_sleep7')
    jump r13_v111_detained_bed7

label r13_v111_detained_bed7:
    call r13_v111_wait('detained_bed7')
    if _return==0:
        jump r13_v111_detained_morning8
    jump r13_v111_detained_bed7

label r13_v111_detained_morning8:
    $ r13_v111_set("day",8)
    jump r13_v111_day8

label r13_v111_day8:
    if r13_v111_value('route7')=='murder':
        jump r13_v111_custody8
    jump r13_v111_prevent_clinic8

label r13_v111_custody8:
    $ r13_v111_scene('MS14_D08_S01')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('v111_custody','custody8',['daram'])
    $ r13_v111_arrive(['daram', 'resident_seori', 'neoul'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0002']),'v111:MS14_D08_S01_L0002')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0003']),'v111:MS14_D08_S01_L0003')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0004']),'v111:MS14_D08_S01_L0004')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0005']),'v111:MS14_D08_S01_L0005')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0006']),'v111:MS14_D08_S01_L0006')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0007']),'v111:MS14_D08_S01_L0007')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0008']),'v111:MS14_D08_S01_L0008')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0009']),'v111:MS14_D08_S01_L0009')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0010']),'v111:MS14_D08_S01_L0010')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0011']),'v111:MS14_D08_S01_L0011')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0012']),'v111:MS14_D08_S01_L0012')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0013']),'v111:MS14_D08_S01_L0013')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0014']),'v111:MS14_D08_S01_L0014')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0015']),'v111:MS14_D08_S01_L0015')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0016']),'v111:MS14_D08_S01_L0016')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0017']),'v111:MS14_D08_S01_L0017')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0018']),'v111:MS14_D08_S01_L0018')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0019']),'v111:MS14_D08_S01_L0019')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0020']),'v111:MS14_D08_S01_L0020')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0021']),'v111:MS14_D08_S01_L0021')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0022']),'v111:MS14_D08_S01_L0022')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0023']),'v111:MS14_D08_S01_L0023')
    call r13_lines(r13_v111_lines(['MS14_D08_S01_L0024']),'v111:MS14_D08_S01_L0024')
    $ r13_v111_commit('MS14_D08_S01_L0025')
    jump r13_v111_room_evidence8

label r13_v111_room_evidence8:
    $ r13_v111_scene('MS14_D08_S02')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('room13','room_evidence8',[])
    $ r13_v111_arrive(['doto', 'buri'])
    $ r13_v111_score()
    jump r13_v111_room_check8

label r13_v111_room_check8:
    call r13_v111_wait('room_check8')
    if _return==0:
        jump r13_v111_room_checked8
    jump r13_v111_room_check8

label r13_v111_room_checked8:
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0001']),'v111:MS14_D08_S02_L0001')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0002']),'v111:MS14_D08_S02_L0002')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0003']),'v111:MS14_D08_S02_L0003')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0004']),'v111:MS14_D08_S02_L0004')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0005']),'v111:MS14_D08_S02_L0005')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0008']),'v111:MS14_D08_S02_L0008')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0009']),'v111:MS14_D08_S02_L0009')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0010']),'v111:MS14_D08_S02_L0010')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0011']),'v111:MS14_D08_S02_L0011')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0013']),'v111:MS14_D08_S02_L0013')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0014']),'v111:MS14_D08_S02_L0014')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0015']),'v111:MS14_D08_S02_L0015')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0016']),'v111:MS14_D08_S02_L0016')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0017']),'v111:MS14_D08_S02_L0017')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0018']),'v111:MS14_D08_S02_L0018')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0019']),'v111:MS14_D08_S02_L0019')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0020']),'v111:MS14_D08_S02_L0020')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0021']),'v111:MS14_D08_S02_L0021')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0022']),'v111:MS14_D08_S02_L0022')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0023']),'v111:MS14_D08_S02_L0023')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0024']),'v111:MS14_D08_S02_L0024')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0025']),'v111:MS14_D08_S02_L0025')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0026']),'v111:MS14_D08_S02_L0026')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0027']),'v111:MS14_D08_S02_L0027')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0028']),'v111:MS14_D08_S02_L0028')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0029']),'v111:MS14_D08_S02_L0029')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0030']),'v111:MS14_D08_S02_L0030')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0031']),'v111:MS14_D08_S02_L0031')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0032']),'v111:MS14_D08_S02_L0032')
    call r13_lines(r13_v111_lines(['MS14_D08_S02_L0033']),'v111:MS14_D08_S02_L0033')
    $ r13_v111_commit('MS14_D08_S02_L0037')
    $ r13_nw_acquire("NW_STONE")
    jump r13_v111_wounds8

label r13_v111_wounds8:
    $ r13_v111_scene('MS14_D08_S03')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('clinic','wounds8',[])
    $ r13_v111_arrive(['resident_seori', 'buri'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0001']),'v111:MS14_D08_S03_L0001')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0002']),'v111:MS14_D08_S03_L0002')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0003']),'v111:MS14_D08_S03_L0003')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0004']),'v111:MS14_D08_S03_L0004')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0005']),'v111:MS14_D08_S03_L0005')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0006']),'v111:MS14_D08_S03_L0006')
    jump r13_v111_tool_faces8

label r13_v111_tool_faces8:
    call r13_v111_wait('tool_faces8')
    if _return==0:
        jump r13_v111_tool_faces_seen8
    jump r13_v111_tool_faces8

label r13_v111_tool_faces_seen8:
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0008']),'v111:MS14_D08_S03_L0008')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0009']),'v111:MS14_D08_S03_L0009')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0010']),'v111:MS14_D08_S03_L0010')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0011']),'v111:MS14_D08_S03_L0011')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0012']),'v111:MS14_D08_S03_L0012')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0013']),'v111:MS14_D08_S03_L0013')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0014']),'v111:MS14_D08_S03_L0014')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0015']),'v111:MS14_D08_S03_L0015')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0016']),'v111:MS14_D08_S03_L0016')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0017']),'v111:MS14_D08_S03_L0017')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0018']),'v111:MS14_D08_S03_L0018')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0019']),'v111:MS14_D08_S03_L0019')
    jump r13_v111_wire_curve8

label r13_v111_wire_curve8:
    call r13_v111_wait('wire_curve8')
    if _return==0:
        jump r13_v111_wire_curve_seen8
    jump r13_v111_wire_curve8

label r13_v111_wire_curve_seen8:
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0021']),'v111:MS14_D08_S03_L0021')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0022']),'v111:MS14_D08_S03_L0022')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0024']),'v111:MS14_D08_S03_L0024')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0025']),'v111:MS14_D08_S03_L0025')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0026']),'v111:MS14_D08_S03_L0026')
    call r13_lines(r13_v111_lines(['MS14_D08_S03_L0027']),'v111:MS14_D08_S03_L0027')
    $ r13_v111_commit('MS14_D08_S03_L0028')
    jump r13_v111_mother_letter8

label r13_v111_prevent_clinic8:
    $ r13_v111_scene('MS14_D08_P01')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('room13','prevent_clinic8',['daram'])
    $ r13_v111_arrive(['daram', 'resident_owlgp', 'resident_seori', 'doto'])
    $ r13_v111_score()

label r13_v111_prevention_story8:
    if r13_v111_value('prevention')=='A':
        jump r13_v111_fear8
    jump r13_v111_care8

label r13_v111_fear8:
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0002']),'v111:MS14_D08_P01_L0002')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0003']),'v111:MS14_D08_P01_L0003')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0004']),'v111:MS14_D08_P01_L0004')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0005']),'v111:MS14_D08_P01_L0005')
    # 0.20.7 (review 6-12 #4): the promise "복도에 있어도 돼" is kept as a real place to stand.
    $ v111_answer=renpy.display_menu([("방에 같이 들어간다",0),("복도에서 문을 열어 두고 듣는다",1)])
    if v111_answer==0:
        call r13_lines(r13_nw_block('owl_room8'),'nw:owl_room8')
    else:
        call r13_lines(r13_nw_block('owl_hall8'),'nw:owl_hall8')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0007']),'v111:MS14_D08_P01_L0007')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0008']),'v111:MS14_D08_P01_L0008')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0009']),'v111:MS14_D08_P01_L0009')
    $ r13_v111_commit('MS14_D08_P01_L0010')
    jump r13_v111_missing_pages8

label r13_v111_care8:
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0012']),'v111:MS14_D08_P01_L0012')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0013']),'v111:MS14_D08_P01_L0013')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0014']),'v111:MS14_D08_P01_L0014')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0015']),'v111:MS14_D08_P01_L0015')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0016']),'v111:MS14_D08_P01_L0016')
    $ r13_v111_commit('MS14_D08_P01_L0017')
    jump r13_v111_missing_pages8

label r13_v111_missing_pages8:
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0018']),'v111:MS14_D08_P01_L0018')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0019']),'v111:MS14_D08_P01_L0019')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0020']),'v111:MS14_D08_P01_L0020')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0021']),'v111:MS14_D08_P01_L0021')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0022']),'v111:MS14_D08_P01_L0022')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0023']),'v111:MS14_D08_P01_L0023')
    call r13_lines(r13_v111_lines(['MS14_D08_P01_L0024']),'v111:MS14_D08_P01_L0024')
    $ r13_v111_commit('MS14_D08_P01_L0026')
    $ r13_nw_acquire("NW_STONE","removed" if r13_v111_value("prevention")=="A" else "clinic")
    jump r13_v111_mother_letter8

label r13_v111_mother_letter8:
    $ r13_v111_scene('MS14_D08_S04')
    $ r13_edit(period=1)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('square','mother_letter8',[])
    $ r13_v111_arrive(['resident_lamplighter', 'doto', 'resident_badook'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0001']),'v111:MS14_D08_S04_L0001')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0002']),'v111:MS14_D08_S04_L0002')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0003']),'v111:MS14_D08_S04_L0003')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0004']),'v111:MS14_D08_S04_L0004')
    $ r13_v111_commit('MS14_D08_S04_L0005')

label r13_v111_letter_route8:
    if r13_v111_value('route7')=='murder':
        jump r13_v111_letter_murder8
    jump r13_v111_letter_prevent8

label r13_v111_letter_murder8:
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0006']),'v111:MS14_D08_S04_L0006')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0008']),'v111:MS14_D08_S04_L0008')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0009']),'v111:MS14_D08_S04_L0009')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0010']),'v111:MS14_D08_S04_L0010')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0011']),'v111:MS14_D08_S04_L0011')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0012']),'v111:MS14_D08_S04_L0012')
    $ r13_v111_commit('MS14_D08_S04_L0013')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0022']),'v111:MS14_D08_S04_L0022')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0023']),'v111:MS14_D08_S04_L0023')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0024']),'v111:MS14_D08_S04_L0024')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0025']),'v111:MS14_D08_S04_L0025')
    $ r13_v111_commit('MS14_D08_S04_L0026')
    jump r13_v111_escort8

label r13_v111_letter_prevent8:
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0014']),'v111:MS14_D08_S04_L0014')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0016']),'v111:MS14_D08_S04_L0016')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0017']),'v111:MS14_D08_S04_L0017')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0018']),'v111:MS14_D08_S04_L0018')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0019']),'v111:MS14_D08_S04_L0019')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0020']),'v111:MS14_D08_S04_L0020')
    $ r13_v111_commit('MS14_D08_S04_L0021')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0027']),'v111:MS14_D08_S04_L0027')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0028']),'v111:MS14_D08_S04_L0028')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0029']),'v111:MS14_D08_S04_L0029')
    $ r13_v111_commit('MS14_D08_S04_L0030')
    jump r13_v111_escort8

label r13_v111_escort8:
    call r13_v111_wait('escort8')
    if _return==0:
        jump r13_v111_escort_done8
    jump r13_v111_escort8

label r13_v111_escort_done8:
    $ r13_v111_set("public_road_escort_completed",True)
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0031']),'v111:MS14_D08_S04_L0031')
    call r13_lines(r13_v111_lines(['MS14_D08_S04_L0032']),'v111:MS14_D08_S04_L0032')
    $ r13_v111_commit('MS14_D08_S04_L0033')
    jump r13_v111_sleep8

label r13_v111_sleep8:
    call r13_v111_travel('school','sleep8')
    jump r13_v111_sleep8_input

label r13_v111_sleep8_input:
    call r13_v111_wait('sleep8_input')
    if _return==0:
        jump r13_v111_sleep8_done
    jump r13_v111_sleep8_input

label r13_v111_sleep8_done:
    $ r13_v111_set("day",9)
    jump r13_v111_day9

label r13_v111_day9:
    if r13_v111_value('route7')=='murder':
        jump r13_v111_passage9
    jump r13_v111_prevent_passage9

label r13_v111_passage9:
    $ r13_v111_scene('MS14_D09_S01')
    $ r13_edit(period=0)
    # 0.20.9 (30선 21): 7일 구조를 겪은 다람의 작은 확인. 다람이 곁에 있을 때 한 번만.
    if not r13_v111_value('DARAM_DETAINED') and r13_v111_actor_ready('daram') and not r13_v111_value('daram_door_asked9'):
        $ r13_v111_set('daram_door_asked9',True)
        call r13_lines(r13_nw_block('daram_door9'),'nw:daram_door9')
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('kitchen','passage9',[])
    $ r13_v111_arrive(['doto', 'resident_ttadak', 'granny'])
    $ r13_v111_score()
    jump r13_v111_safe_passage9

label r13_v111_safe_passage9:
    call r13_v111_wait('safe_passage9')
    if _return==0:
        jump r13_v111_passage_walk9
    if _return==1:
        jump r13_v111_passage_safety_hint9
    jump r13_v111_safe_passage9

label r13_v111_passage_safety_hint9:
    call r13_lines(r13_v111_lines(['MS14_D09_S01_L0015']),'v111:MS14_D09_S01_L0015')
    call r13_lines(r13_v111_lines(['MS14_D09_S01_L0016']),'v111:MS14_D09_S01_L0016')
    jump r13_v111_safe_passage9

label r13_v111_passage_walk9:
    call r13_lines(r13_v111_lines(['MS14_D09_S01_L0001']),'v111:MS14_D09_S01_L0001')
    call r13_lines(r13_v111_lines(['MS14_D09_S01_L0002']),'v111:MS14_D09_S01_L0002')
    call r13_lines(r13_v111_lines(['MS14_D09_S01_L0003']),'v111:MS14_D09_S01_L0003')
    call r13_lines(r13_v111_lines(['MS14_D09_S01_L0004']),'v111:MS14_D09_S01_L0004')
    call r13_lines(r13_v111_lines(['MS14_D09_S01_L0005']),'v111:MS14_D09_S01_L0005')
    call r13_lines(r13_v111_lines(['MS14_D09_S01_L0007']),'v111:MS14_D09_S01_L0007')
    call r13_lines(r13_v111_lines(['MS14_D09_S01_L0008']),'v111:MS14_D09_S01_L0008')
    call r13_lines(r13_v111_lines(['MS14_D09_S01_L0009']),'v111:MS14_D09_S01_L0009')
    call r13_lines(r13_v111_lines(['MS14_D09_S01_L0010']),'v111:MS14_D09_S01_L0010')
    call r13_lines(r13_v111_lines(['MS14_D09_S01_L0011']),'v111:MS14_D09_S01_L0011')
    call r13_lines(r13_v111_lines(['MS14_D09_S01_L0012']),'v111:MS14_D09_S01_L0012')
    $ r13_v111_commit('MS14_D09_S01_L0014')
    jump r13_v111_passage_after9

label r13_v111_passage_after9:
    call r13_v111_wait('passage_after9')
    if _return==0:
        jump r13_v111_workshop9
    if _return==1:
        jump r13_v111_passage_measured_hint9
    jump r13_v111_passage_after9

label r13_v111_passage_measured_hint9:
    call r13_lines(r13_v111_lines(['MS14_D09_S01_L0017']),'v111:MS14_D09_S01_L0017')
    $ r13_v111_commit('MS14_D09_S01_L0018')
    jump r13_v111_passage_after9

label r13_v111_workshop9:
    $ r13_v111_scene('MS14_D09_S02')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('workshop','workshop9',[])
    $ r13_v111_arrive(['buri'])
    $ r13_v111_score()

label r13_v111_tok_route9:
    if r13_v111_tok_attends("workshop"):
        jump r13_v111_tok9
    jump r13_v111_repair_copy9

label r13_v111_tok9:
    $ r13_v111_arrive(["buri","resident_tok"])
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0001']),'v111:MS14_D09_S02_L0001')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0002']),'v111:MS14_D09_S02_L0002')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0003']),'v111:MS14_D09_S02_L0003')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0004']),'v111:MS14_D09_S02_L0004')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0006']),'v111:MS14_D09_S02_L0006')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0007']),'v111:MS14_D09_S02_L0007')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0008']),'v111:MS14_D09_S02_L0008')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0009']),'v111:MS14_D09_S02_L0009')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0010']),'v111:MS14_D09_S02_L0010')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0011']),'v111:MS14_D09_S02_L0011')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0012']),'v111:MS14_D09_S02_L0012')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0013']),'v111:MS14_D09_S02_L0013')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0014']),'v111:MS14_D09_S02_L0014')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0015']),'v111:MS14_D09_S02_L0015')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0016']),'v111:MS14_D09_S02_L0016')
    $ r13_v111_commit('MS14_D09_S02_L0018')
    jump r13_v111_scarf9

label r13_v111_repair_copy9:
    $ r13_v111_join(['seryeon'])
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0019']),'v111:MS14_D09_S02_L0019')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0020']),'v111:MS14_D09_S02_L0020')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0021']),'v111:MS14_D09_S02_L0021')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0022']),'v111:MS14_D09_S02_L0022')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0024']),'v111:MS14_D09_S02_L0024')
    call r13_lines(r13_v111_lines(['MS14_D09_S02_L0025']),'v111:MS14_D09_S02_L0025')
    $ r13_v111_commit('MS14_D09_S02_L0026')
    jump r13_v111_scarf9

label r13_v111_scarf9:
    $ r13_v111_scene('MS14_D09_S03')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('dining','scarf9',[])
    $ r13_v111_arrive(['nabi'])
    $ r13_v111_score()
    if r13_v111_value('NABI_relationship')=='strained':
        call r13_v111_repair_trust9
    jump r13_v111_pin_question9

label r13_v111_repair_trust9:
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0001']),'v111:MS14_D09_S03_L0001')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0002']),'v111:MS14_D09_S03_L0002')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0003']),'v111:MS14_D09_S03_L0003')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0004']),'v111:MS14_D09_S03_L0004')
    $ r13_v111_commit('MS14_D09_S03_L0005')
    return

label r13_v111_pin_question9:
    call r13_v111_wait('pin_question9')
    if _return==0:
        jump r13_v111_pin_time9
    jump r13_v111_pin_question9

label r13_v111_pin_time9:
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0006']),'v111:MS14_D09_S03_L0006')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0007']),'v111:MS14_D09_S03_L0007')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0008']),'v111:MS14_D09_S03_L0008')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0009']),'v111:MS14_D09_S03_L0009')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0010']),'v111:MS14_D09_S03_L0010')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0011']),'v111:MS14_D09_S03_L0011')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0012']),'v111:MS14_D09_S03_L0012')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0013']),'v111:MS14_D09_S03_L0013')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0014']),'v111:MS14_D09_S03_L0014')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0015']),'v111:MS14_D09_S03_L0015')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0016']),'v111:MS14_D09_S03_L0016')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0017']),'v111:MS14_D09_S03_L0017')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0019']),'v111:MS14_D09_S03_L0019')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0020']),'v111:MS14_D09_S03_L0020')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0021']),'v111:MS14_D09_S03_L0021')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0022']),'v111:MS14_D09_S03_L0022')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0023']),'v111:MS14_D09_S03_L0023')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0024']),'v111:MS14_D09_S03_L0024')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0026']),'v111:MS14_D09_S03_L0026')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0027']),'v111:MS14_D09_S03_L0027')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0028']),'v111:MS14_D09_S03_L0028')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0029']),'v111:MS14_D09_S03_L0029')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0030']),'v111:MS14_D09_S03_L0030')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0031']),'v111:MS14_D09_S03_L0031')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0032']),'v111:MS14_D09_S03_L0032')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0033']),'v111:MS14_D09_S03_L0033')
    $ r13_v111_commit('MS14_D09_S03_L0034')
    jump r13_v111_scarf_compare9

label r13_v111_scarf_compare9:
    call r13_v111_wait('scarf_compare9')
    if _return==0:
        jump r13_v111_scarf_done9
    jump r13_v111_scarf_compare9

label r13_v111_scarf_done9:
    $ r13_v111_join(['granny'])
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0042']),'v111:MS14_D09_S03_L0042')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0043']),'v111:MS14_D09_S03_L0043')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0044']),'v111:MS14_D09_S03_L0044')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0046']),'v111:MS14_D09_S03_L0046')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0047']),'v111:MS14_D09_S03_L0047')
    call r13_lines(r13_v111_lines(['MS14_D09_S03_L0048']),'v111:MS14_D09_S03_L0048')
    $ r13_v111_commit('MS14_D09_S03_L0049')
    jump r13_v111_postal9

label r13_v111_prevent_passage9:
    $ r13_v111_scene('MS14_D09_P01')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('kitchen','prevent_passage9',[])
    $ r13_v111_arrive(['doto', 'resident_ttadak', 'granny', 'nabi'])
    $ r13_v111_score()
    jump r13_v111_safe_prevent9

label r13_v111_safe_prevent9:
    call r13_v111_wait('safe_prevent9')
    if _return==0:
        jump r13_v111_prevent_walk9
    jump r13_v111_safe_prevent9

label r13_v111_prevent_walk9:
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0001']),'v111:MS14_D09_P01_L0001')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0002']),'v111:MS14_D09_P01_L0002')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0003']),'v111:MS14_D09_P01_L0003')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0004']),'v111:MS14_D09_P01_L0004')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0006']),'v111:MS14_D09_P01_L0006')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0007']),'v111:MS14_D09_P01_L0007')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0009']),'v111:MS14_D09_P01_L0009')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0010']),'v111:MS14_D09_P01_L0010')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0011']),'v111:MS14_D09_P01_L0011')
    $ r13_v111_commit('MS14_D09_P01_L0012')
    call r13_v111_travel('room13','returned_papers9')
    jump r13_v111_papers_check9

label r13_v111_papers_check9:
    call r13_v111_wait('papers_check9')
    if _return==0:
        jump r13_v111_papers_done9
    jump r13_v111_papers_check9

label r13_v111_papers_done9:
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0013']),'v111:MS14_D09_P01_L0013')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0014']),'v111:MS14_D09_P01_L0014')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0015']),'v111:MS14_D09_P01_L0015')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0016']),'v111:MS14_D09_P01_L0016')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0017']),'v111:MS14_D09_P01_L0017')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0019']),'v111:MS14_D09_P01_L0019')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0020']),'v111:MS14_D09_P01_L0020')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0022']),'v111:MS14_D09_P01_L0022')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0023']),'v111:MS14_D09_P01_L0023')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0024']),'v111:MS14_D09_P01_L0024')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0025']),'v111:MS14_D09_P01_L0025')
    call r13_lines(r13_v111_lines(['MS14_D09_P01_L0026']),'v111:MS14_D09_P01_L0026')
    $ r13_v111_commit('MS14_D09_P01_L0027')
    jump r13_v111_postal9

label r13_v111_postal9:
    $ r13_v111_scene('MS14_D09_S04')
    $ r13_edit(period=1)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('post','postal9',[])
    $ r13_v111_arrive(['seryeon', 'resident_sling'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0001']),'v111:MS14_D09_S04_L0001')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0002']),'v111:MS14_D09_S04_L0002')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0003']),'v111:MS14_D09_S04_L0003')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0004']),'v111:MS14_D09_S04_L0004')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0006']),'v111:MS14_D09_S04_L0006')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0007']),'v111:MS14_D09_S04_L0007')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0008']),'v111:MS14_D09_S04_L0008')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0009']),'v111:MS14_D09_S04_L0009')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0010']),'v111:MS14_D09_S04_L0010')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0011']),'v111:MS14_D09_S04_L0011')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0012']),'v111:MS14_D09_S04_L0012')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0013']),'v111:MS14_D09_S04_L0013')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0014']),'v111:MS14_D09_S04_L0014')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0016']),'v111:MS14_D09_S04_L0016')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0017']),'v111:MS14_D09_S04_L0017')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0018']),'v111:MS14_D09_S04_L0018')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0019']),'v111:MS14_D09_S04_L0019')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0021']),'v111:MS14_D09_S04_L0021')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0022']),'v111:MS14_D09_S04_L0022')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0023']),'v111:MS14_D09_S04_L0023')
    $ r13_v111_commit('MS14_D09_S04_L0024')

label r13_v111_night_route9:
    if r13_v111_value('route7')=='murder':
        jump r13_v111_custody_night9
    jump r13_v111_school_night9

label r13_v111_custody_night9:
    call r13_v111_travel('v111_custody','custody_night9')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0026']),'v111:MS14_D09_S04_L0026')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0027']),'v111:MS14_D09_S04_L0027')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0028']),'v111:MS14_D09_S04_L0028')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0029']),'v111:MS14_D09_S04_L0029')
    $ r13_v111_commit('MS14_D09_S04_L0030')
    jump r13_v111_sleep9

label r13_v111_school_night9:
    call r13_v111_travel('school','school_night9')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0032']),'v111:MS14_D09_S04_L0032')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0033']),'v111:MS14_D09_S04_L0033')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0034']),'v111:MS14_D09_S04_L0034')
    call r13_lines(r13_v111_lines(['MS14_D09_S04_L0035']),'v111:MS14_D09_S04_L0035')
    $ r13_v111_commit('MS14_D09_S04_L0036')
    jump r13_v111_sleep9

label r13_v111_sleep9:
    call r13_v111_travel('school','sleep9')
    jump r13_v111_sleep9_input

label r13_v111_sleep9_input:
    call r13_v111_wait('sleep9_input')
    if _return==0:
        jump r13_v111_sleep9_done
    jump r13_v111_sleep9_input

label r13_v111_sleep9_done:
    $ r13_v111_set("day",10)
    jump r13_v111_day10

label r13_v111_day10:
    if r13_v111_value('route7')=='murder':
        jump r13_v111_waiting10
    jump r13_v111_prevent_hearing10

label r13_v111_waiting10:
    $ r13_v111_scene('MS14_D10_S01')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','waiting10',['daram'])
    $ r13_v111_arrive(['daram', 'resident_seori', 'buri'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D10_S01_L0002']),'v111:MS14_D10_S01_L0002')
    call r13_lines(r13_v111_lines(['MS14_D10_S01_L0003']),'v111:MS14_D10_S01_L0003')
    call r13_lines(r13_v111_lines(['MS14_D10_S01_L0004']),'v111:MS14_D10_S01_L0004')
    call r13_lines(r13_v111_lines(['MS14_D10_S01_L0005']),'v111:MS14_D10_S01_L0005')
    call r13_lines(r13_v111_lines(['MS14_D10_S01_L0006']),'v111:MS14_D10_S01_L0006')
    call r13_lines(r13_v111_lines(['MS14_D10_S01_L0007']),'v111:MS14_D10_S01_L0007')
    call r13_lines(r13_v111_lines(['MS14_D10_S01_L0008']),'v111:MS14_D10_S01_L0008')
    call r13_lines(r13_v111_lines(['MS14_D10_S01_L0009']),'v111:MS14_D10_S01_L0009')
    call r13_lines(r13_v111_lines(['MS14_D10_S01_L0011']),'v111:MS14_D10_S01_L0011')
    call r13_lines(r13_v111_lines(['MS14_D10_S01_L0012']),'v111:MS14_D10_S01_L0012')
    call r13_lines(r13_v111_lines(['MS14_D10_S01_L0013']),'v111:MS14_D10_S01_L0013')
    call r13_lines(r13_v111_lines(['MS14_D10_S01_L0014']),'v111:MS14_D10_S01_L0014')
    call r13_lines(r13_v111_lines(['MS14_D10_S01_L0016']),'v111:MS14_D10_S01_L0016')
    call r13_lines(r13_v111_lines(['MS14_D10_S01_L0017']),'v111:MS14_D10_S01_L0017')
    $ r13_v111_commit('MS14_D10_S01_L0019')
    jump r13_v111_hearing10

label r13_v111_hearing10:
    $ r13_v111_scene('MS14_D10_S02')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','hearing10',['daram'])
    $ r13_v111_arrive(['daram', 'doto', 'nabi', 'granny', 'neoul', 'resident_ppul', 'resident_seori'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0002']),'v111:MS14_D10_S02_L0002')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0003']),'v111:MS14_D10_S02_L0003')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0004']),'v111:MS14_D10_S02_L0004')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0005']),'v111:MS14_D10_S02_L0005')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0006']),'v111:MS14_D10_S02_L0006')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0007']),'v111:MS14_D10_S02_L0007')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0008']),'v111:MS14_D10_S02_L0008')
    $ r13_v111_commit('MS14_D10_S02_L0010')
    jump r13_v111_wound_proof10

label r13_v111_wound_proof10:
    call r13_v111_proof('두 상처와 촛대 파손을 대조한다',['E08_CHILD_ACCOUNT', 'E08_TOOL'],'r13_v111_wound_answer10','r13_v111_hearing_wrong10','r13_v111_hearing_hint10')
    jump expression _return

label r13_v111_wound_answer10:
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0011']),'v111:MS14_D10_S02_L0011')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0012']),'v111:MS14_D10_S02_L0012')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0013']),'v111:MS14_D10_S02_L0013')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0014']),'v111:MS14_D10_S02_L0014')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0015']),'v111:MS14_D10_S02_L0015')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0016']),'v111:MS14_D10_S02_L0016')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0017']),'v111:MS14_D10_S02_L0017')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0018']),'v111:MS14_D10_S02_L0018')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0019']),'v111:MS14_D10_S02_L0019')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0020']),'v111:MS14_D10_S02_L0020')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0021']),'v111:MS14_D10_S02_L0021')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0022']),'v111:MS14_D10_S02_L0022')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0023']),'v111:MS14_D10_S02_L0023')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0024']),'v111:MS14_D10_S02_L0024')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0025']),'v111:MS14_D10_S02_L0025')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0026']),'v111:MS14_D10_S02_L0026')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0028']),'v111:MS14_D10_S02_L0028')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0029']),'v111:MS14_D10_S02_L0029')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0030']),'v111:MS14_D10_S02_L0030')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0031']),'v111:MS14_D10_S02_L0031')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0032']),'v111:MS14_D10_S02_L0032')
    $ r13_v111_commit('MS14_D10_S02_L0033')
    jump r13_v111_passage_proof10

label r13_v111_passage_proof10:
    call r13_v111_proof('두 번째 길을 실제 기록으로 보인다',['E09_PASSAGE', 'E08_ROOM'],'r13_v111_passage_answer10','r13_v111_passage_wrong10','r13_v111_hearing_hint10')
    jump expression _return

label r13_v111_passage_answer10:
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0035']),'v111:MS14_D10_S02_L0035')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0036']),'v111:MS14_D10_S02_L0036')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0037']),'v111:MS14_D10_S02_L0037')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0038']),'v111:MS14_D10_S02_L0038')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0039']),'v111:MS14_D10_S02_L0039')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0040']),'v111:MS14_D10_S02_L0040')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0041']),'v111:MS14_D10_S02_L0041')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0042']),'v111:MS14_D10_S02_L0042')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0043']),'v111:MS14_D10_S02_L0043')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0044']),'v111:MS14_D10_S02_L0044')
    $ r13_v111_commit('MS14_D10_S02_L0046')
    jump r13_v111_owner10

label r13_v111_hearing_wrong10:
    if r13_nw_retry("room13",['E08_CHILD_ACCOUNT', 'E08_TOOL'],'너울이 고개를 젓는다. 아이의 말과 촛대 조각을 함께 놓아야 한다.'):
        call r13_lines(r13_v111_lines(['MS14_D10_S02_L0047', 'MS14_D10_S02_L0048']),'v111:hearing_wrong10:half')
        jump r13_v111_wound_proof10
    $ r13_nw_meeting_end("room13",'lose')
    $ r13_nw_list("daram","room13_lose")
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0047']),'v111:MS14_D10_S02_L0047')
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0048']),'v111:MS14_D10_S02_L0048')
    $ r13_v111_apply('MS14_D10_S03_L0088',[o for o in R13_V111['records']['MS14_D10_S03_L0088']['operations'] if o['field'] in ('DARAM_DETAINED','DARAM_location','D10_confrontation_release_completed')])
    jump r13_v111_bench10

label r13_v111_passage_wrong10:
    if r13_nw_retry("room13",['E09_PASSAGE', 'E08_ROOM'],'따닥이 고개를 젓는다. 직접 걸어 본 길과 현장 배치를 함께 놓아야 한다.'):
        call r13_lines(r13_v111_lines(['MS14_D10_S02_L0050']),'v111:passage_wrong10:half')
        jump r13_v111_passage_proof10
    $ r13_nw_meeting_end("room13",'lose')
    $ r13_nw_list("daram","room13_lose")
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0050']),'v111:MS14_D10_S02_L0050')
    $ r13_v111_apply('MS14_D10_S03_L0088',[o for o in R13_V111['records']['MS14_D10_S03_L0088']['operations'] if o['field'] in ('DARAM_DETAINED','DARAM_location','D10_confrontation_release_completed')])
    jump r13_v111_bench10

label r13_v111_hearing_hint10:
    call r13_lines(r13_v111_lines(['MS14_D10_S02_L0051']),'v111:MS14_D10_S02_L0051')
    $ r13_v111_commit('MS14_D10_S02_L0052')
    if r13_v111_value("D10_S02_two_wounds_completed"):
        jump r13_v111_passage_proof10
    jump r13_v111_wound_proof10

label r13_v111_owner10:
    $ r13_v111_scene('MS14_D10_S03')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','owner10',['daram'])
    $ r13_v111_arrive(['daram', 'granny', 'resident_ppul', 'neoul', 'nabi', 'resident_seori', 'buri', 'doto'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0001']),'v111:MS14_D10_S03_L0001')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0002']),'v111:MS14_D10_S03_L0002')
    $ r13_v111_commit('MS14_D10_S03_L0004')
    jump r13_v111_owner_proof10

label r13_v111_owner_proof10:
    call r13_v111_proof('구리선과 수선 출처를 대조한다',['E08_WOUND_WIRE', 'E09_PIN_OWNER'],'r13_v111_owner_answer10','r13_v111_owner_wrong10',None)
    jump expression _return

label r13_v111_owner_answer10:
    if r13_v111_tok_attends("hearing"):
        jump r13_v111_owner_tok10
    jump r13_v111_owner_copy10

label r13_v111_owner_tok10:
    $ r13_v111_arrive(["daram","granny","resident_ppul","neoul","nabi","resident_seori","resident_tok","buri","doto"])
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0005']),'v111:MS14_D10_S03_L0005')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0006']),'v111:MS14_D10_S03_L0006')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0007']),'v111:MS14_D10_S03_L0007')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0008']),'v111:MS14_D10_S03_L0008')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0010']),'v111:MS14_D10_S03_L0010')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0011']),'v111:MS14_D10_S03_L0011')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0012']),'v111:MS14_D10_S03_L0012')
    $ r13_v111_commit('MS14_D10_S03_L0013')
    jump r13_v111_time10

label r13_v111_owner_copy10:
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0014']),'v111:MS14_D10_S03_L0014')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0015']),'v111:MS14_D10_S03_L0015')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0016']),'v111:MS14_D10_S03_L0016')
    $ r13_v111_commit('MS14_D10_S03_L0017')
    jump r13_v111_time10

label r13_v111_time10:
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0018']),'v111:MS14_D10_S03_L0018')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0019']),'v111:MS14_D10_S03_L0019')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0020']),'v111:MS14_D10_S03_L0020')
    $ r13_v111_commit('MS14_D10_S03_L0022')
    jump r13_v111_time_proof10

label r13_v111_time_proof10:
    call r13_v111_proof('첫 비명 뒤 핀을 다시 채운 때',['E09_PIN_TIME', 'E09_PIN_HANDOVER_TIME'],'r13_v111_time_answer10','r13_v111_time_wrong10',None)
    jump expression _return

label r13_v111_time_answer10:
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0024']),'v111:MS14_D10_S03_L0024')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0025']),'v111:MS14_D10_S03_L0025')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0026']),'v111:MS14_D10_S03_L0026')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0027']),'v111:MS14_D10_S03_L0027')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0028']),'v111:MS14_D10_S03_L0028')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0030']),'v111:MS14_D10_S03_L0030')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0032']),'v111:MS14_D10_S03_L0032')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0033']),'v111:MS14_D10_S03_L0033')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0034']),'v111:MS14_D10_S03_L0034')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0035']),'v111:MS14_D10_S03_L0035')
    $ r13_v111_commit('MS14_D10_S03_L0036')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0037']),'v111:MS14_D10_S03_L0037')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0038']),'v111:MS14_D10_S03_L0038')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0039']),'v111:MS14_D10_S03_L0039')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0040']),'v111:MS14_D10_S03_L0040')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0041']),'v111:MS14_D10_S03_L0041')
    $ r13_v111_commit('MS14_D10_S03_L0044')
    jump r13_v111_contact_proof10

label r13_v111_contact_proof10:
    call r13_v111_proof('접촉면과 아이의 위치를 대조한다',['E08_CONTACT_ASSEMBLY', 'E08_WOUND_WIRE', 'E08_CHILD_POSITION', 'E08_ROOM_REACH', 'E09_SCARF'],'r13_v111_contact_answer10','r13_v111_contact_wrong10',None)
    jump expression _return

label r13_v111_contact_answer10:
    $ r13_nw_meeting_end("room13","win")
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0045']),'v111:MS14_D10_S03_L0045')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0046']),'v111:MS14_D10_S03_L0046')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0047']),'v111:MS14_D10_S03_L0047')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0048']),'v111:MS14_D10_S03_L0048')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0050']),'v111:MS14_D10_S03_L0050')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0051']),'v111:MS14_D10_S03_L0051')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0052']),'v111:MS14_D10_S03_L0052')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0053']),'v111:MS14_D10_S03_L0053')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0055']),'v111:MS14_D10_S03_L0055')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0056']),'v111:MS14_D10_S03_L0056')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0057']),'v111:MS14_D10_S03_L0057')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0058']),'v111:MS14_D10_S03_L0058')
    $ r13_v111_commit('MS14_D10_S03_L0059')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0060']),'v111:MS14_D10_S03_L0060')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0061']),'v111:MS14_D10_S03_L0061')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0063']),'v111:MS14_D10_S03_L0063')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0064']),'v111:MS14_D10_S03_L0064')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0065']),'v111:MS14_D10_S03_L0065')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0066']),'v111:MS14_D10_S03_L0066')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0067']),'v111:MS14_D10_S03_L0067')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0068']),'v111:MS14_D10_S03_L0068')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0069']),'v111:MS14_D10_S03_L0069')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0070']),'v111:MS14_D10_S03_L0070')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0071']),'v111:MS14_D10_S03_L0071')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0073']),'v111:MS14_D10_S03_L0073')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0074']),'v111:MS14_D10_S03_L0074')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0075']),'v111:MS14_D10_S03_L0075')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0076']),'v111:MS14_D10_S03_L0076')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0077']),'v111:MS14_D10_S03_L0077')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0079']),'v111:MS14_D10_S03_L0079')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0080']),'v111:MS14_D10_S03_L0080')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0081']),'v111:MS14_D10_S03_L0081')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0082']),'v111:MS14_D10_S03_L0082')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0083']),'v111:MS14_D10_S03_L0083')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0084']),'v111:MS14_D10_S03_L0084')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0085']),'v111:MS14_D10_S03_L0085')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0086']),'v111:MS14_D10_S03_L0086')
    $ r13_v111_commit('MS14_D10_S03_L0088')
    $ r13_v111_set("grandmother_custody","detained")
    $ r13_v111_set("forgery_confirmed",True)
    jump r13_v111_bench10

label r13_v111_owner_wrong10:
    if r13_nw_retry("room13",['E08_WOUND_WIRE', 'E09_PIN_OWNER'],'할머니가 웃는다. 구리선과 수선 기록을 함께 놓아야 한다.'):
        call r13_lines(r13_v111_lines(['MS14_D10_S03_L0089']),'v111:owner_wrong10:half')
        jump r13_v111_owner_proof10
    $ r13_nw_meeting_end("room13",'partial')
    $ r13_v111_set("room13_partial_kind",'unknown')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0089']),'v111:MS14_D10_S03_L0089')
    $ r13_v111_apply('MS14_D10_S03_L0088',[o for o in R13_V111['records']['MS14_D10_S03_L0088']['operations'] if o['field'] in ('DARAM_DETAINED','DARAM_location','D10_confrontation_release_completed')])
    jump r13_v111_bench10

label r13_v111_time_wrong10:
    if r13_nw_retry("room13",['E09_PIN_TIME', 'E09_PIN_HANDOVER_TIME'],'나비가 고개를 젓는다. 핀을 다시 채운 때와 계단참의 핀을 함께 놓아야 한다.'):
        call r13_lines(r13_v111_lines(['MS14_D10_S03_L0090']),'v111:time_wrong10:half')
        jump r13_v111_time_proof10
    $ r13_nw_meeting_end("room13",'partial')
    $ r13_v111_set("room13_partial_kind",'unknown')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0090']),'v111:MS14_D10_S03_L0090')
    $ r13_v111_apply('MS14_D10_S03_L0088',[o for o in R13_V111['records']['MS14_D10_S03_L0088']['operations'] if o['field'] in ('DARAM_DETAINED','DARAM_location','D10_confrontation_release_completed')])
    jump r13_v111_bench10

label r13_v111_contact_wrong10:
    if r13_nw_retry("room13",['E08_CONTACT_ASSEMBLY', 'E08_WOUND_WIRE', 'E08_CHILD_POSITION', 'E08_ROOM_REACH', 'E09_SCARF'],'할머니가 목도리를 여민다. 천과 핀, 상처, 아이의 자리를 함께 놓아야 한다.'):
        call r13_lines(r13_v111_lines(['MS14_D10_S03_L0091', 'MS14_D10_S03_L0092']),'v111:contact_wrong10:half')
        jump r13_v111_contact_proof10
    $ r13_nw_meeting_end("room13",'partial')
    $ r13_v111_set("room13_partial_kind",'accident')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0091']),'v111:MS14_D10_S03_L0091')
    call r13_lines(r13_v111_lines(['MS14_D10_S03_L0092']),'v111:MS14_D10_S03_L0092')
    $ r13_v111_apply('MS14_D10_S03_L0088',[o for o in R13_V111['records']['MS14_D10_S03_L0088']['operations'] if o['field'] in ('DARAM_DETAINED','DARAM_location','D10_confrontation_release_completed')])
    jump r13_v111_bench10

label r13_v111_bench10:
    $ r13_v111_scene('MS14_D10_S04')
    $ r13_edit(period=1)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('post','bench10',['daram'])
    $ r13_v111_arrive(['daram', 'seryeon', 'buri', 'nabi'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0001']),'v111:MS14_D10_S04_L0001')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0002']),'v111:MS14_D10_S04_L0002')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0003']),'v111:MS14_D10_S04_L0003')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0004']),'v111:MS14_D10_S04_L0004')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0005']),'v111:MS14_D10_S04_L0005')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0006']),'v111:MS14_D10_S04_L0006')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0007']),'v111:MS14_D10_S04_L0007')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0008']),'v111:MS14_D10_S04_L0008')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0010']),'v111:MS14_D10_S04_L0010')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0011']),'v111:MS14_D10_S04_L0011')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0012']),'v111:MS14_D10_S04_L0012')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0013']),'v111:MS14_D10_S04_L0013')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0014']),'v111:MS14_D10_S04_L0014')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0015']),'v111:MS14_D10_S04_L0015')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0017']),'v111:MS14_D10_S04_L0017')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0018']),'v111:MS14_D10_S04_L0018')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0019']),'v111:MS14_D10_S04_L0019')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0020']),'v111:MS14_D10_S04_L0020')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0021']),'v111:MS14_D10_S04_L0021')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0022']),'v111:MS14_D10_S04_L0022')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0023']),'v111:MS14_D10_S04_L0023')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0024']),'v111:MS14_D10_S04_L0024')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0025']),'v111:MS14_D10_S04_L0025')
    call r13_lines(r13_v111_lines(['MS14_D10_S04_L0026']),'v111:MS14_D10_S04_L0026')
    $ r13_v111_commit('MS14_D10_S04_L0027')
    jump r13_v111_sleep10

label r13_v111_prevent_hearing10:
    $ r13_v111_scene('MS14_D10_P01')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','prevent_hearing10',['daram'])
    $ r13_v111_arrive(['daram', 'resident_owlgp', 'granny', 'resident_ppul', 'neoul', 'resident_sling', 'seryeon'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0002']),'v111:MS14_D10_P01_L0002')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0003']),'v111:MS14_D10_P01_L0003')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0004']),'v111:MS14_D10_P01_L0004')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0005']),'v111:MS14_D10_P01_L0005')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0006']),'v111:MS14_D10_P01_L0006')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0007']),'v111:MS14_D10_P01_L0007')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0008']),'v111:MS14_D10_P01_L0008')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0010']),'v111:MS14_D10_P01_L0010')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0011']),'v111:MS14_D10_P01_L0011')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0012']),'v111:MS14_D10_P01_L0012')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0013']),'v111:MS14_D10_P01_L0013')
    $ r13_v111_commit('MS14_D10_P01_L0014')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0015']),'v111:MS14_D10_P01_L0015')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0016']),'v111:MS14_D10_P01_L0016')
    $ r13_v111_commit('MS14_D10_P01_L0018')
    jump r13_v111_authority_proof10

label r13_v111_authority_proof10:
    call r13_v111_proof('수신인과 가족 전달 권한을 구분한다',['E06_CONTACT', 'E09_MAIL'],'r13_v111_authority_answer10','r13_v111_authority_wrong10',None)
    jump expression _return

label r13_v111_authority_answer10:
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0019']),'v111:MS14_D10_P01_L0019')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0020']),'v111:MS14_D10_P01_L0020')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0021']),'v111:MS14_D10_P01_L0021')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0022']),'v111:MS14_D10_P01_L0022')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0024']),'v111:MS14_D10_P01_L0024')
    $ r13_v111_commit('MS14_D10_P01_L0025')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0026']),'v111:MS14_D10_P01_L0026')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0027']),'v111:MS14_D10_P01_L0027')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0028']),'v111:MS14_D10_P01_L0028')
    $ r13_v111_commit('MS14_D10_P01_L0030')
    jump r13_v111_writing_proof10

label r13_v111_writing_proof10:
    call r13_v111_proof('반송·필사본·초대 발송을 대조한다',['E01', 'E07', 'E09_MAIL'],'r13_v111_writing_answer10','r13_v111_writing_wrong10',None)
    jump expression _return

label r13_v111_writing_answer10:
    $ r13_nw_meeting_end("records","win")
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0031']),'v111:MS14_D10_P01_L0031')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0032']),'v111:MS14_D10_P01_L0032')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0033']),'v111:MS14_D10_P01_L0033')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0034']),'v111:MS14_D10_P01_L0034')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0035']),'v111:MS14_D10_P01_L0035')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0036']),'v111:MS14_D10_P01_L0036')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0037']),'v111:MS14_D10_P01_L0037')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0038']),'v111:MS14_D10_P01_L0038')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0040']),'v111:MS14_D10_P01_L0040')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0041']),'v111:MS14_D10_P01_L0041')
    $ r13_v111_commit('MS14_D10_P01_L0042')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0043']),'v111:MS14_D10_P01_L0043')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0044']),'v111:MS14_D10_P01_L0044')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0045']),'v111:MS14_D10_P01_L0045')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0046']),'v111:MS14_D10_P01_L0046')
    $ r13_v111_commit('MS14_D10_P01_L0048')
    jump r13_v111_pocket10

label r13_v111_pocket10:
    call r13_v111_wait('pocket10')
    if _return==0:
        jump r13_v111_pocket_answer10
    jump r13_v111_pocket10

label r13_v111_pocket_answer10:
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0049']),'v111:MS14_D10_P01_L0049')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0050']),'v111:MS14_D10_P01_L0050')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0051']),'v111:MS14_D10_P01_L0051')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0052']),'v111:MS14_D10_P01_L0052')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0053']),'v111:MS14_D10_P01_L0053')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0054']),'v111:MS14_D10_P01_L0054')
    $ r13_v111_commit('MS14_D10_P01_L0055')
    menu:
        "가족끼리 확인하고, 왜 숨겼는지 묻는다":  # 0.20.7 (review 6-12 #3)
            jump r13_v111_family_paper10
        "공개된 수량만 대조하고 기록을 받는다":
            jump r13_v111_public_paper10

label r13_v111_family_paper10:
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0057']),'v111:MS14_D10_P01_L0057')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0058']),'v111:MS14_D10_P01_L0058')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0059']),'v111:MS14_D10_P01_L0059')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0060']),'v111:MS14_D10_P01_L0060')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0062']),'v111:MS14_D10_P01_L0062')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0063']),'v111:MS14_D10_P01_L0063')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0064']),'v111:MS14_D10_P01_L0064')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0065']),'v111:MS14_D10_P01_L0065')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0067']),'v111:MS14_D10_P01_L0067')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0068']),'v111:MS14_D10_P01_L0068')
    $ r13_v111_commit('MS14_D10_P01_L0069')
    jump r13_v111_private_handoff10

label r13_v111_private_handoff10:
    call r13_v111_wait('private_handoff10')
    if _return==0:
        jump r13_v111_owl_invitation10
    if _return==1:
        jump r13_v111_public_paper10
    jump r13_v111_private_handoff10

label r13_v111_owl_invitation10:
    call r13_lines([("resident_owlgp","부인이 직접 준 게 아니네. 편지는 할머니가 전했지.",{"no_lead":True})],"v111:owl_invitation_testimony")
    $ r13_v111_set("owl_invitation_testimony",True)
    jump r13_v111_private_handoff10

label r13_v111_public_paper10:
    $ r13_v111_arrive(["daram","resident_owlgp","granny","seryeon"])
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0071']),'v111:MS14_D10_P01_L0071')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0072']),'v111:MS14_D10_P01_L0072')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0073']),'v111:MS14_D10_P01_L0073')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0074']),'v111:MS14_D10_P01_L0074')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0075']),'v111:MS14_D10_P01_L0075')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0078']),'v111:MS14_D10_P01_L0078')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0079']),'v111:MS14_D10_P01_L0079')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0080']),'v111:MS14_D10_P01_L0080')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0081']),'v111:MS14_D10_P01_L0081')
    $ r13_v111_commit('MS14_D10_P01_L0083')
    jump r13_v111_prevent_return10

label r13_v111_authority_wrong10:
    if r13_nw_retry("records",['E06_CONTACT', 'E09_MAIL'],'부엉이가 손을 거둔다. 아내가 실제로 쓴 연락 길과 우체국 기록을 함께 놓아야 한다.'):
        call r13_lines(r13_v111_lines(['MS14_D10_P01_L0084', 'MS14_D10_P01_L0085']),'v111:authority_wrong10:half')
        jump r13_v111_authority_proof10
    $ r13_nw_meeting_end("records","lose")
    $ r13_nw_list("resident_owlgp","records_lose")
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0084']),'v111:MS14_D10_P01_L0084')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0085']),'v111:MS14_D10_P01_L0085')
    $ r13_v111_commit('MS14_D10_P01_L0083')
    jump r13_v111_prevent_return10

label r13_v111_writing_wrong10:
    if r13_nw_retry("records",['E01', 'E07', 'E09_MAIL'],'슬링이 고개를 젓는다. 편지와 봉투, 필사본을 함께 놓아야 한다.'):
        call r13_lines(r13_v111_lines(['MS14_D10_P01_L0086']),'v111:writing_wrong10:half')
        jump r13_v111_writing_proof10
    $ r13_nw_meeting_end("records","partial")
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0086']),'v111:MS14_D10_P01_L0086')
    jump r13_v111_writing_partial10

label r13_v111_writing_partial10:
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0043']),'v111:MS14_D10_P01_L0043')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0044']),'v111:MS14_D10_P01_L0044')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0045']),'v111:MS14_D10_P01_L0045')
    call r13_lines(r13_v111_lines(['MS14_D10_P01_L0046']),'v111:MS14_D10_P01_L0046')
    $ r13_v111_commit('MS14_D10_P01_L0048')
    jump r13_v111_pocket10

label r13_v111_prevent_return10:
    $ r13_v111_scene('MS14_D10_S04P')
    $ r13_edit(period=1)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','prevent_return10',['daram'])
    $ r13_v111_arrive(['daram'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D10_S04P_L0001']),'v111:MS14_D10_S04P_L0001')
    call r13_lines(r13_v111_lines(['MS14_D10_S04P_L0002']),'v111:MS14_D10_S04P_L0002')
    call r13_lines(r13_v111_lines(['MS14_D10_S04P_L0003']),'v111:MS14_D10_S04P_L0003')
    call r13_lines(r13_v111_lines(['MS14_D10_S04P_L0004']),'v111:MS14_D10_S04P_L0004')
    $ r13_v111_commit('MS14_D10_S04P_L0005')
    jump r13_v111_sleep10

label r13_v111_sleep10:
    call r13_v111_travel('school','sleep10')
    jump r13_v111_sleep10_input

label r13_v111_sleep10_input:
    call r13_v111_wait('sleep10_input')
    if _return==0:
        jump r13_v111_sleep10_done
    jump r13_v111_sleep10_input

label r13_v111_sleep10_done:
    $ r13_v111_set("day",11)
    jump r13_v111_day11
