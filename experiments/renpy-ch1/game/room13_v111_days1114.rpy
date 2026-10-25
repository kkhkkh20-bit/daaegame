init 324 python:
    def r13_crowd_guard_available13(reserved=False):
        busy=r13_v111_value('busy:guard')
        return (r13_v111_person_alive('guard') and not r13_v111_value('departed:guard') and not r13_v111_value('listed:guard')
            and r13_v111_value('location:guard') in (None,'square') and (not busy or reserved and busy=='crowd_supervision'))
    def r13_crowd_prepared13():
        return (all(r13_v111_value(k) is True for k in ('crowd_records_spaced13','crowd_cart_spaced13','crowd_supervisor_placed13'))
            and r13_crowd_guard_available13(True) and r13_v111_value('busy:guard')=='crowd_supervision')
    def r13_crowd_release13():
        if r13_v111_value('busy:guard')=='crowd_supervision':r13_v111_set('busy:guard',False)
        r13_v111_set('crowd_supervisor_placed13',None)
    def r13_soup_inspect_ready12():
        return all(r13_v111_value(k) is True for k in ('soup_smallpot_seen12','soup_bowls_seen12','soup_bottle_seen12'))
    def r13_nero_transport_ready11():
        # Old saves may already be waiting after the original preparation scene.
        physical=all(r13_v111_value(k) is True for k in ('rescue_cart_ready','rescue_cover_ready','rescue_driver_ready','rescue_lights_ready'))
        seat=r13_v111_value('rescue_school_ready11') is True or not r13_v111_value('rescue_preparation_schema11')
        return physical and seat and r13_v111_actor_ready('karo') and not r13_v111_value('departed:karo')
    def r13_nero_receiver_ready11():
        return any(r13_v111_actor_ready(p) and not r13_v111_value('departed:'+p) and not r13_v111_value('listed:'+p) for p in ('resident_teacher','nabi'))

# Reviewed D11–D14 source records and native callbacks.

label r13_v111_day11:
    $ r13_v111_scene('MS14_D11_S00')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','day11',['daram'])
    $ r13_v111_arrive(['daram', 'karo'])
    $ r13_v111_score()
    $ r13_v111_arrive(['daram', 'karo'])
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D11_S00_L0002']),'v111:MS14_D11_S00_L0002')
    call r13_lines(r13_v111_lines(['MS14_D11_S00_L0003']),'v111:MS14_D11_S00_L0003')
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D11_S00_L0004']),'v111:MS14_D11_S00_L0004')
    call r13_lines(r13_v111_lines(['MS14_D11_S00_L0005']),'v111:MS14_D11_S00_L0005')
    call r13_v111_travel('forest','pump11')
    $ r13_v111_arrive(['daram', 'karo'])
    call r13_lines(r13_v111_lines(['MS14_D11_S00_L0007']),'v111:MS14_D11_S00_L0007')
    call r13_lines(r13_v111_lines(['MS14_D11_S00_L0008']),'v111:MS14_D11_S00_L0008')
    jump r13_v111_pump_open11

label r13_v111_pump_open11:
    call r13_v111_wait('pump_open11')
    if _return==0:
        jump r13_v111_pump_reply11
    jump r13_v111_pump_open11

label r13_v111_pump_reply11:
    call r13_lines(r13_v111_lines(['MS14_D11_S00_L0010']),'v111:MS14_D11_S00_L0010')
    call r13_lines(r13_v111_lines(['MS14_D11_S00_L0011']),'v111:MS14_D11_S00_L0011')
    call r13_lines(r13_v111_lines(['MS14_D11_S00_L0012']),'v111:MS14_D11_S00_L0012')
    call r13_lines(r13_v111_lines(['MS14_D11_S00_L0013']),'v111:MS14_D11_S00_L0013')
    $ r13_v111_set('root_address_known',True)
    jump r13_v111_root11

label r13_v111_root11:
    $ r13_v111_scene('MS14_D11_S01')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('forest','root11',['daram'])
    $ r13_v111_arrive(['daram', 'resident_tosil'])
    $ r13_v111_score()
    $ r13_v111_arrive(['daram', 'resident_tosil'])
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0002']),'v111:MS14_D11_S01_L0002')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0003']),'v111:MS14_D11_S01_L0003')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0004']),'v111:MS14_D11_S01_L0004')
    jump r13_v111_root_note11

label r13_v111_root_note11:
    $ r13_world_cameras=dict(r13_world_cameras,forest=0)  # 0.20.10: the roots are at the left edge
    call r13_v111_wait('root_note11')
    if _return==0:
        jump r13_v111_root_read11
    jump r13_v111_root_note11

label r13_v111_root_read11:
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0006']),'v111:MS14_D11_S01_L0006')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0008']),'v111:MS14_D11_S01_L0008')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0009']),'v111:MS14_D11_S01_L0009')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0010']),'v111:MS14_D11_S01_L0010')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0011']),'v111:MS14_D11_S01_L0011')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0013']),'v111:MS14_D11_S01_L0013')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0014']),'v111:MS14_D11_S01_L0014')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0015']),'v111:MS14_D11_S01_L0015')
    $ r13_v111_set('greenhouse_address_known',True)
    if r13_v111_value('grandmother_custody')=='detained':
        call r13_v111_tosil_detained11
    else:
        call r13_v111_tosil_free11
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0025']),'v111:MS14_D11_S01_L0025')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0026']),'v111:MS14_D11_S01_L0026')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0027']),'v111:MS14_D11_S01_L0027')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0028']),'v111:MS14_D11_S01_L0028')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0029']),'v111:MS14_D11_S01_L0029')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0030']),'v111:MS14_D11_S01_L0030')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0032']),'v111:MS14_D11_S01_L0032')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0033']),'v111:MS14_D11_S01_L0033')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0034']),'v111:MS14_D11_S01_L0034')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0035']),'v111:MS14_D11_S01_L0035')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0036']),'v111:MS14_D11_S01_L0036')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0037']),'v111:MS14_D11_S01_L0037')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0038']),'v111:MS14_D11_S01_L0038')
    call r13_v111_travel('school','tosil_school11')
    $ r13_v111_arrive(['daram', 'resident_tosil'])
    if r13_v111_value("location:nabi") not in (None,"school"):
        jump r13_v111_nabi_waiting11
    jump r13_v111_nabi_arrival11

label r13_v111_tosil_detained11:
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0021']),'v111:MS14_D11_S01_L0021')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0022']),'v111:MS14_D11_S01_L0022')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0023']),'v111:MS14_D11_S01_L0023')
    return

label r13_v111_tosil_free11:
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0017']),'v111:MS14_D11_S01_L0017')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0018']),'v111:MS14_D11_S01_L0018')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0019']),'v111:MS14_D11_S01_L0019')
    return

label r13_v111_nabi_waiting11:
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0048']),'v111:MS14_D11_S01_L0048')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0049']),'v111:MS14_D11_S01_L0049')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0050']),'v111:MS14_D11_S01_L0050')
    jump r13_v111_nabi_wait11

label r13_v111_nabi_wait11:
    call r13_v111_wait('nabi_wait11')
    if _return==0:
        jump r13_v111_nabi_arrival11
    jump r13_v111_nabi_wait11

label r13_v111_nabi_arrival11:
    $ r13_v111_arrive(['daram', 'resident_tosil', 'nabi'])
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0041']),'v111:MS14_D11_S01_L0041')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0042']),'v111:MS14_D11_S01_L0042')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0043']),'v111:MS14_D11_S01_L0043')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0044']),'v111:MS14_D11_S01_L0044')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0045']),'v111:MS14_D11_S01_L0045')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0046']),'v111:MS14_D11_S01_L0046')
    jump r13_v111_tosil_handoff11

label r13_v111_tosil_handoff11:
    call r13_v111_wait('tosil_handoff11')
    if _return==0:
        jump r13_v111_tosil_safe11
    jump r13_v111_tosil_handoff11

label r13_v111_tosil_safe11:
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0051']),'v111:MS14_D11_S01_L0051')
    call r13_lines(r13_v111_lines(['MS14_D11_S01_L0052']),'v111:MS14_D11_S01_L0052')
    $ r13_v111_commit('MS14_D11_S01_L0052')
    jump r13_v111_reunion11

label r13_v111_reunion11:
    $ r13_v111_scene('MS14_D11_S02')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('greenhouse','reunion11',['daram', 'mom'])
    $ r13_v111_arrive(['daram', 'mom'])
    $ r13_v111_score()
    $ r13_v111_arrive(['daram', 'mom'])
    call r13_lines(r13_v111_lines(['MS14_D11_S02_L0002']),'v111:MS14_D11_S02_L0002')
    call r13_lines(r13_v111_lines(['MS14_D11_S02_L0003']),'v111:MS14_D11_S02_L0003')  # 0.20.7: the distance at the doorway
    call r13_lines(r13_v111_lines(['MS14_D11_S02_L0004']),'v111:MS14_D11_S02_L0004')
    call r13_lines(r13_v111_lines(['MS14_D11_S02_L0005']),'v111:MS14_D11_S02_L0005')
    call r13_lines(r13_v111_lines(['MS14_D11_S02_L0006']),'v111:MS14_D11_S02_L0006')
    call r13_lines(r13_v111_lines(['MS14_D11_S02_L0007']),'v111:MS14_D11_S02_L0007')
    call r13_lines(r13_v111_lines(['MS14_D11_S02_L0008']),'v111:MS14_D11_S02_L0008')  # 0.20.7: Daram takes the coat
    call r13_lines(r13_v111_lines(['MS14_D11_S02_L0009']),'v111:MS14_D11_S02_L0009')
    call r13_lines(r13_v111_lines(['MS14_D11_S02_L0010']),'v111:MS14_D11_S02_L0010')
    call r13_lines(r13_v111_lines(['MS14_D11_S02_L0011']),'v111:MS14_D11_S02_L0011')
    call r13_lines(r13_v111_lines(['MS14_D11_S02_L0013']),'v111:MS14_D11_S02_L0013')
    call r13_lines(r13_v111_lines(['MS14_D11_S02_L0014']),'v111:MS14_D11_S02_L0014')
    call r13_lines(r13_v111_lines(['MS14_D11_S02_L0015']),'v111:MS14_D11_S02_L0015')
    call r13_lines(r13_v111_lines(['MS14_D11_S02_L0016']),'v111:MS14_D11_S02_L0016')
    $ r13_v111_set('family_reunited',True)
    jump r13_v111_dry11

label r13_v111_dry11:
    $ r13_v111_scene('MS14_D11_S02A')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('greenhouse','dry11',['daram', 'mom'])
    $ r13_v111_arrive(['daram', 'mom'])
    $ r13_v111_score()
    $ r13_v111_arrive(['daram', 'mom'])
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0002']),'v111:MS14_D11_S02A_L0002')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0003']),'v111:MS14_D11_S02A_L0003')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0005']),'v111:MS14_D11_S02A_L0005')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0006']),'v111:MS14_D11_S02A_L0006')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0008']),'v111:MS14_D11_S02A_L0008')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0009']),'v111:MS14_D11_S02A_L0009')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0010']),'v111:MS14_D11_S02A_L0010')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0011']),'v111:MS14_D11_S02A_L0011')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0013']),'v111:MS14_D11_S02A_L0013')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0014']),'v111:MS14_D11_S02A_L0014')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0016']),'v111:MS14_D11_S02A_L0016')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0017']),'v111:MS14_D11_S02A_L0017')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0018']),'v111:MS14_D11_S02A_L0018')
    if r13_v111_value('carried_dry_blankets')==0:
        jump r13_v111_coat_use11
    menu:
        '두 장을 꺼내 덮는다' if r13_v111_value('carried_dry_blankets')==2:
            jump r13_v111_blanket_use11
        '한 장을 함께 덮는다' if r13_v111_value('carried_dry_blankets')==1:
            jump r13_v111_blanket_one11
        '짐 안에 둔다' if r13_v111_value('carried_dry_blankets')>0:
            jump r13_v111_blanket_keep11
        '외투 안쪽을 함께 덮는다' if r13_v111_value('carried_dry_blankets')==0:
            jump r13_v111_coat_use11

label r13_v111_blanket_use11:
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0022']),'v111:MS14_D11_S02A_L0022')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0023']),'v111:MS14_D11_S02A_L0023')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0024']),'v111:MS14_D11_S02A_L0024')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0025']),'v111:MS14_D11_S02A_L0025')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0027']),'v111:MS14_D11_S02A_L0027')
    jump r13_v111_dry_done11

label r13_v111_blanket_one11:
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0036']),'v111:MS14_D11_S02A_L0036')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0037']),'v111:MS14_D11_S02A_L0037')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0038']),'v111:MS14_D11_S02A_L0038')
    jump r13_v111_dry_done11

label r13_v111_blanket_keep11:
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0029']),'v111:MS14_D11_S02A_L0029')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0030']),'v111:MS14_D11_S02A_L0030')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0031']),'v111:MS14_D11_S02A_L0031')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0033']),'v111:MS14_D11_S02A_L0033')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0034']),'v111:MS14_D11_S02A_L0034')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0035']),'v111:MS14_D11_S02A_L0035')
    jump r13_v111_dry_done11

label r13_v111_coat_use11:
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0029']),'v111:MS14_D11_S02A_L0029')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0030']),'v111:MS14_D11_S02A_L0030')
    call r13_lines(r13_v111_lines(['MS14_D11_S02A_L0031']),'v111:MS14_D11_S02A_L0031')
    jump r13_v111_dry_done11

label r13_v111_dry_done11:
    jump r13_v111_button11

label r13_v111_button11:
    $ r13_v111_scene('MS14_D11_S02B')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('greenhouse','button11',['daram', 'mom'])
    $ r13_v111_arrive(['daram', 'mom'])
    $ r13_v111_score()
    $ r13_v111_arrive(['daram', 'mom'])
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0002']),'v111:MS14_D11_S02B_L0002')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0003']),'v111:MS14_D11_S02B_L0003')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0004']),'v111:MS14_D11_S02B_L0004')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0005']),'v111:MS14_D11_S02B_L0005')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0007']),'v111:MS14_D11_S02B_L0007')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0008']),'v111:MS14_D11_S02B_L0008')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0010']),'v111:MS14_D11_S02B_L0010')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0011']),'v111:MS14_D11_S02B_L0011')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0012']),'v111:MS14_D11_S02B_L0012')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0014']),'v111:MS14_D11_S02B_L0014')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0015']),'v111:MS14_D11_S02B_L0015')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0016']),'v111:MS14_D11_S02B_L0016')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0018']),'v111:MS14_D11_S02B_L0018')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0019']),'v111:MS14_D11_S02B_L0019')
    jump r13_v111_mother_questions11

label r13_v111_mother_questions11:
    call r13_v111_wait('mother_questions11')
    if _return==0:
        jump r13_v111_mother_life11
    if _return==1:
        jump r13_v111_mother_invitation11
    if _return==2:
        jump r13_v111_mother_return11
    jump r13_v111_mother_questions11

label r13_v111_mother_life11:
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0022']),'v111:MS14_D11_S02B_L0022')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0023']),'v111:MS14_D11_S02B_L0023')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0024']),'v111:MS14_D11_S02B_L0024')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0025']),'v111:MS14_D11_S02B_L0025')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0026']),'v111:MS14_D11_S02B_L0026')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0027']),'v111:MS14_D11_S02B_L0027')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0028']),'v111:MS14_D11_S02B_L0028')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0029']),'v111:MS14_D11_S02B_L0029')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0030']),'v111:MS14_D11_S02B_L0030')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0031']),'v111:MS14_D11_S02B_L0031')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0032']),'v111:MS14_D11_S02B_L0032')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0033']),'v111:MS14_D11_S02B_L0033')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0034']),'v111:MS14_D11_S02B_L0034')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0035']),'v111:MS14_D11_S02B_L0035')
    $ r13_v111_set('mother_q_life',True)
    jump r13_v111_mother_ready11

label r13_v111_mother_invitation11:
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0037']),'v111:MS14_D11_S02B_L0037')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0038']),'v111:MS14_D11_S02B_L0038')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0039']),'v111:MS14_D11_S02B_L0039')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0040']),'v111:MS14_D11_S02B_L0040')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0041']),'v111:MS14_D11_S02B_L0041')
    $ r13_v111_set('mother_q_invitation',True)
    jump r13_v111_mother_ready11

label r13_v111_mother_return11:
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0043']),'v111:MS14_D11_S02B_L0043')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0044']),'v111:MS14_D11_S02B_L0044')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0045']),'v111:MS14_D11_S02B_L0045')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0046']),'v111:MS14_D11_S02B_L0046')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0047']),'v111:MS14_D11_S02B_L0047')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0048']),'v111:MS14_D11_S02B_L0048')
    $ r13_v111_set('mother_q_return',True)
    jump r13_v111_mother_ready11

label r13_v111_mother_ready11:
    if all(r13_v111_value(k) for k in ['mother_q_life', 'mother_q_invitation', 'mother_q_return']):
        jump r13_v111_mother_last11
    jump r13_v111_mother_questions11

label r13_v111_mother_last11:
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0050']),'v111:MS14_D11_S02B_L0050')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0051']),'v111:MS14_D11_S02B_L0051')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0052']),'v111:MS14_D11_S02B_L0052')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0053']),'v111:MS14_D11_S02B_L0053')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0054']),'v111:MS14_D11_S02B_L0054')
    if r13_v111_value('forgery_confirmed'):
        call r13_v111_forgery_question11
    if r13_v111_value('OWL_ALIVE') and r13_v111_value('owl_invitation_testimony'):
        call r13_v111_owl_question11
    jump r13_v111_facility11

label r13_v111_forgery_question11:
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0055']),'v111:MS14_D11_S02B_L0055')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0056']),'v111:MS14_D11_S02B_L0056')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0057']),'v111:MS14_D11_S02B_L0057')
    return

label r13_v111_owl_question11:
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0058']),'v111:MS14_D11_S02B_L0058')
    call r13_lines(r13_v111_lines(['MS14_D11_S02B_L0059']),'v111:MS14_D11_S02B_L0059')
    return

label r13_v111_facility11:
    $ r13_v111_scene('MS14_D11_S03')
    $ r13_edit(period=1)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('facility','facility11',['daram', 'mom'])
    $ r13_v111_arrive(['daram', 'mom', 'resident_guldol', 'resident_lamplighter'])
    $ r13_v111_score()
    $ r13_v111_arrive(['daram', 'mom', 'resident_guldol', 'resident_lamplighter'])
    if r13_v111_actor_ready("resident_guldol"):
        call r13_v111_guldol_heat11
    else:
        call r13_v111_mother_heat11
    # 검토 0.20.4 추가 4: 3일 광장에서 따뜻한 받침을 직접 만져 본 경로만 회상한다.
    if r13_v111_value('stone_warm_felt3') and r13_v111_actor_ready('daram') and r13_v111_actor_ready('mom'):
        call r13_lines(r13_nw_block('warm_recall11'),'nw:warm_recall11')
    jump r13_v111_heat_check11

label r13_v111_guldol_heat11:
    $ r13_v111_set('guldol_facility_seen',True)
    if r13_v111_actor_ready('resident_guldol'):
        call r13_lines(r13_v111_lines(['MS14_D11_S03_L0002']),'v111:MS14_D11_S03_L0002')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0003']),'v111:MS14_D11_S03_L0003')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0004']),'v111:MS14_D11_S03_L0004')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0005']),'v111:MS14_D11_S03_L0005')
    if r13_v111_actor_ready('resident_guldol'):
        call r13_lines(r13_v111_lines(['MS14_D11_S03_L0006']),'v111:MS14_D11_S03_L0006')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0008']),'v111:MS14_D11_S03_L0008')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0009']),'v111:MS14_D11_S03_L0009')
    return

label r13_v111_mother_heat11:
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0043']),'v111:MS14_D11_S03_L0043')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0044']),'v111:MS14_D11_S03_L0044')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0045']),'v111:MS14_D11_S03_L0045')
    return

label r13_v111_heat_check11:
    call r13_v111_wait('heat_check11')
    if _return==100:
        call r13_hidden_base_marks11
        jump r13_v111_heat_check11
    if _return==0:
        jump r13_v111_heat_seen11
    jump r13_v111_heat_check11

label r13_v111_heat_seen11:
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0011']),'v111:MS14_D11_S03_L0011')
    if r13_v111_actor_ready('resident_lamplighter'):
        call r13_lines(r13_v111_lines(['MS14_D11_S03_L0012']),'v111:MS14_D11_S03_L0012')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0013']),'v111:MS14_D11_S03_L0013')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0014']),'v111:MS14_D11_S03_L0014')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0015']),'v111:MS14_D11_S03_L0015')
    if r13_v111_actor_ready('resident_guldol'):
        call r13_lines(r13_v111_lines(['MS14_D11_S03_L0016']),'v111:MS14_D11_S03_L0016')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0018']),'v111:MS14_D11_S03_L0018')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0019']),'v111:MS14_D11_S03_L0019')
    # 0.20.9 (6~12일 검토 10): 벽화 → 깨진 돌판 → 새긴 이름. 한 번에 몰아 설명하지 않고 하나씩 본다.
    $ renpy.display_menu([("벽 아래 깨진 돌판을 들여다본다",0)])
    call r13_lines(r13_nw_block('mural_tablet11'),'nw:mural_tablet11')
    $ renpy.display_menu([("그림 옆 벽에 새긴 글씨를 본다",0)])
    call r13_lines(r13_nw_block('mural_names11'),'nw:mural_names11')
    $ r13_nw_acquire("NW_TABLET_A")
    $ r13_nw_acquire("NW_NAMES")
    $ r13_v111_set('heat_inventory_observed',True)
    if r13_v111_value('carried_dry_blankets')>0:
        call r13_v111_family_blankets11
    else:
        call r13_v111_no_blankets11
    menu:
        '가족 자리부터 본다':
            jump r13_v111_family_place11
        '아랫길 대피 준비를 확인한다':
            jump r13_v111_rescue_prepare11
        '준비된 물자를 학교로 옮긴다':
            jump r13_v111_supply_school11

label r13_v111_family_blankets11:
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0021']),'v111:MS14_D11_S03_L0021')
    return

label r13_v111_no_blankets11:
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0023']),'v111:MS14_D11_S03_L0023')
    return

label r13_v111_family_place11:
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0048']),'v111:MS14_D11_S03_L0048')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0049']),'v111:MS14_D11_S03_L0049')
    call r13_v111_travel('school','family_place11')
    $ r13_v111_arrive(['mom', 'daram', 'nabi', 'resident_teacher'])
    jump r13_v111_family_place_check11

label r13_v111_family_place_check11:
    call r13_v111_wait('family_place_check11')
    if _return==0:
        jump r13_v111_family_place_done11
    jump r13_v111_family_place_check11

label r13_v111_family_place_done11:
    $ r13_v111_set('family_school_place',True)
    jump r13_v111_school_visit11

label r13_v111_rescue_prepare11:
    $ r13_v111_set('rescue_preparation_schema11',True)
    call r13_v111_travel('square','rescue_prepare11')
    $ r13_v111_arrive(['mom', 'daram', 'karo', 'resident_nero', 'resident_lamplighter'])
    jump r13_v111_rescue_cart11

label r13_v111_rescue_cart11:
    call r13_v111_wait('rescue_cart11')
    if _return==0:
        jump r13_v111_rescue_ready11
    if _return==80:
        call r13_lines(r13_nw_block('nr_cart11'),'nw:nr_cart11')
        $ r13_v111_set('rescue_cart_ready',True)
    elif _return==81:
        call r13_lines(r13_nw_block('nr_cover11'),'nw:nr_cover11')
        $ r13_v111_set('rescue_cover_ready',True)
    elif _return==82 and r13_v111_actor_ready('karo'):
        call r13_lines(r13_nw_block('nr_driver11'),'nw:nr_driver11')
        $ r13_v111_set('rescue_driver_ready',True)
    elif _return==83:
        call r13_lines(r13_nw_block('nr_lights11'),'nw:nr_lights11')
        $ r13_v111_set('rescue_lights_ready',True)
    elif _return==84 and r13_nero_receiver_ready11():
        # The cart driver waits beside the cart; school dialogue must not relocate him.
        $ r13_v111_arrive(['mom','daram','resident_teacher','nabi'])
        if r13_v111_actor_ready('resident_teacher') and not r13_v111_value('listed:resident_teacher') and not r13_v111_value('departed:resident_teacher'):
            call r13_lines(r13_nw_block('nr_seat11'),'nw:nr_seat11')
        else:
            call r13_lines(r13_nw_block('nr_seat_nabi11'),'nw:nr_seat_nabi11')
        $ r13_v111_set('rescue_school_ready11',True)
    elif _return==85:
        jump r13_v111_supply_school11
    # 2026-10-24 대승리 S1(GRAND_WIN_DESIGN.md 2-3): 짐칸을 비우며 그릇 상자를 내리고, 하나를 주머니에 넣을 수 있다.
    if _return==1:
        call r13_v111_bowl_cart11
    if _return==2:
        call r13_v111_bowl_pocket11
    if _return==3:
        call r13_lines(r13_nw_block('bowl_cart_again11'),'nw:bowl_cart_again11')
    jump r13_v111_rescue_cart11

label r13_v111_rescue_ready11:
    if r13_nero_transport_ready11():
        jump r13_v111_day_rescue11
    call r13_lines(r13_nw_block('nr_missing11'),'nw:nr_missing11')
    jump r13_v111_supply_school11

label r13_v111_day_rescue11:
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0050']),'v111:MS14_D11_S03_L0050')
    if r13_v111_actor_ready('resident_nero'):
        call r13_lines(r13_v111_lines(['MS14_D11_S03_L0051']),'v111:MS14_D11_S03_L0051')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0052']),'v111:MS14_D11_S03_L0052')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0053']),'v111:MS14_D11_S03_L0053')
    call r13_v111_travel('forest','day_rescue11',[])
    $ r13_v111_arrive(['karo', 'resident_nero'])
    jump r13_v111_day_rescue_door11

label r13_v111_day_rescue_door11:
    call r13_v111_wait('day_rescue_door11')
    if _return==0:
        jump r13_v111_day_rescue_school11
    jump r13_v111_day_rescue_door11

label r13_v111_day_rescue_school11:
    call r13_v111_travel('school','day_rescue_school11')
    $ r13_v111_arrive(['mom', 'daram', 'nabi', 'resident_teacher', 'resident_nero', 'karo'])
    $ r13_v111_set('lower_road_arrived11',3)
    $ r13_v111_set('rescue_handoff_period11','day')
    jump r13_v111_rescue_handoff11

label r13_v111_supply_school11:
    call r13_v111_travel('school','supply_school11')
    $ r13_v111_arrive(['mom', 'daram', 'karo', 'resident_teacher', 'nabi'])
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0025']),'v111:MS14_D11_S03_L0025')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0026']),'v111:MS14_D11_S03_L0026')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0027']),'v111:MS14_D11_S03_L0027')
    $ r13_v111_set('school_supply_handed',True)
    $ r13_v111_set('school_heat_connected',False)
    $ r13_v111_apply('actual_school_supply11',[dict(op="acquire",key='E14_SUPPLY',variant="observed")])
    jump r13_v111_school_visit11

label r13_v111_school_visit11:
    $ r13_v111_arrive(['mom', 'daram', 'nabi', 'resident_teacher', 'resident_tosil'])
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0029']),'v111:MS14_D11_S03_L0029')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0030']),'v111:MS14_D11_S03_L0030')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0031']),'v111:MS14_D11_S03_L0031')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0032']),'v111:MS14_D11_S03_L0032')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0033']),'v111:MS14_D11_S03_L0033')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0035']),'v111:MS14_D11_S03_L0035')
    if not r13_v111_value("family_school_place"):
        jump r13_v111_family_space_after_supply11
    jump r13_v111_family_space_ready11

label r13_v111_family_space_after_supply11:
    call r13_v111_wait('family_space_after_supply11')
    if _return==0:
        jump r13_v111_family_space_checked11
    jump r13_v111_family_space_after_supply11

label r13_v111_family_space_checked11:
    $ r13_v111_set('family_school_place',True)
    jump r13_v111_family_space_ready11

label r13_v111_family_space_ready11:
    if r13_v111_value('carried_dry_blankets')>0 and not r13_v111_value('tosil_blanket_given'):
        jump r13_v111_blanket_choice11
    jump r13_v111_hypothesis11

label r13_v111_blanket_choice11:
    menu:
        '가족 짐에 보관한다':
            jump r13_v111_blanket_store11
        '토실에게 한 장을 건넨다':
            jump r13_v111_tosil_blanket11

label r13_v111_blanket_store11:
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0054']),'v111:MS14_D11_S03_L0054')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0055']),'v111:MS14_D11_S03_L0055')
    jump r13_v111_hypothesis11

label r13_v111_tosil_blanket11:
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0038']),'v111:MS14_D11_S03_L0038')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0039']),'v111:MS14_D11_S03_L0039')
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0040']),'v111:MS14_D11_S03_L0040')
    if r13_v111_value("carried_dry_blankets")>1:
        call r13_v111_tosil_blanket_remaining11
    else:
        call r13_v111_tosil_blanket_last11
    $ r13_v111_apply("tosil_actual_blanket",[dict(op="set",field="carried_dry_blankets",value=r13_v111_value("carried_dry_blankets")-1),dict(op="set",field="tosil_bedding_received",value=1),dict(op="set",field="tosil_blanket_given",value=True)])
    jump r13_v111_hypothesis11

label r13_v111_tosil_blanket_remaining11:
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0041']),'v111:MS14_D11_S03_L0041')
    return

label r13_v111_tosil_blanket_last11:
    call r13_lines(r13_v111_lines(['MS14_D11_S03_L0057']),'v111:MS14_D11_S03_L0057')
    return

label r13_v111_hypothesis11:
    $ r13_v111_arrive(["daram","resident_teacher","guard","resident_madam","npc_pandol","resident_lamplighter","resident_owlgp"])
    call r13_lines(r13_nw_block('hyp_open11'),'nw:hyp_open11')
    $ r13_nw_acquire("NW_SICK_BEDS")
    jump r13_v111_hyp0_menu11

label r13_v111_hyp0_menu11:
    $ r13_meeting_checkpoint("hypothesis")
    call r13_nw_wrong_thought
    $ v111_claim='menu:hyp0'
    menu:
        '야생화는 옮는 병이다':
            jump r13_v111_hyp0_sick11
        '아르카가 사람을 부른다':
            jump r13_v111_hyp0_call11
        '꺼낸 아르카 곁에 오래 있던 사람부터 무너진다':
            jump r13_v111_hyp0_won11
        '늙으면 누구나 그렇게 된다':
            jump r13_v111_hyp0_old11

label r13_v111_hyp0_sick11:
    call r13_lines(r13_nw_block('hyp0_sick11'),'nw:hyp0_sick11')
    if r13_nw_retry("hypothesis"):
        jump r13_v111_hyp0_menu11
    jump r13_v111_hyp_lost_gate11

label r13_v111_hyp0_call11:
    call r13_lines(r13_nw_block('hyp0_call11'),'nw:hyp0_call11')
    if r13_nw_retry("hypothesis"):
        jump r13_v111_hyp0_menu11
    jump r13_v111_hyp_lost_gate11

label r13_v111_hyp0_old11:
    call r13_lines(r13_nw_block('hyp0_old11'),'nw:hyp0_old11')
    if r13_nw_retry("hypothesis"):
        jump r13_v111_hyp0_menu11
    jump r13_v111_hyp_lost_gate11

label r13_v111_hyp0_won11:
    call r13_lines(r13_nw_block('hyp0_won11'),'nw:hyp0_won11')
    jump r13_v111_hyp1_q11

label r13_v111_hyp1_q11:
    call r13_nw_wrong_thought
    call r13_lines(r13_nw_block('hyp1_q11'),'nw:hyp1_q11')
    $ v111_claim='menu:hyp1'
    menu:
        '만지는 것보다 곁에서 오래 지내는 게 문제다':
            jump r13_v111_hyp1_reason11
        '초롱은 젊어서 버틴다':
            jump r13_v111_hyp1_badreason11
        '초롱은 장갑을 끼고 만진다':
            jump r13_v111_hyp1_badreason11

label r13_v111_hyp1_badreason11:
    if r13_nw_retry("hypothesis"):
        call r13_lines(r13_nw_block("hyp1_lost11"),"nw:hyp1_lost11:retry")
        jump r13_v111_hyp1_q11
    jump r13_v111_hyp1_lost11

label r13_v111_hyp1_reason11:
    call r13_lines(r13_nw_block('hyp1_reason11'),'nw:hyp1_reason11')
    jump r13_v111_hyp1_proof11

label r13_v111_hyp1_proof11:
    call r13_v111_proof('초롱과 피코의 하루를 대조한다',['E11', 'E08', 'NW_PIKO_TREMOR'],'r13_v111_hyp1_won11','r13_v111_hyp1_wrong11',None)
    jump expression _return

label r13_v111_hyp1_wrong11:
    if r13_nw_retry("hypothesis",['E11', 'E08', 'NW_PIKO_TREMOR'],'돌목이 팔짱을 낀다. 초롱의 하루와 피코의 밤을 함께 놓아야 한다.'):
        jump r13_v111_hyp1_proof11
    jump r13_v111_hyp1_lost11

label r13_v111_hyp1_lost11:
    call r13_lines(r13_nw_block('hyp1_lost11'),'nw:hyp1_lost11')
    $ r13_v111_set('hyp_issue:1','lost')
    jump r13_v111_hyp2_q11

label r13_v111_hyp1_won11:
    call r13_lines(r13_nw_block('hyp1_won11'),'nw:hyp1_won11')
    $ r13_v111_set('hyp_issue:1','won')
    jump r13_v111_hyp2_q11

label r13_v111_hyp2_q11:
    call r13_nw_wrong_thought
    call r13_lines(r13_nw_block('hyp2_q11'),'nw:hyp2_q11')
    $ v111_claim='menu:hyp2'
    menu:
        '켜지 않고 쌓아 둔 돌은 아무 해가 없다':
            jump r13_v111_hyp2_badreason11
        '백 부인은 그 돌 곁에서 잠을 자지 않는다':
            jump r13_v111_hyp2_reason11
        '백 부인은 돌을 팔기만 한다':
            jump r13_v111_hyp2_badreason11

label r13_v111_hyp2_badreason11:
    if r13_nw_retry("hypothesis"):
        call r13_lines(r13_nw_block("hyp2_lost11"),"nw:hyp2_lost11:retry")
        jump r13_v111_hyp2_q11
    jump r13_v111_hyp2_lost11

label r13_v111_hyp2_reason11:
    call r13_lines(r13_nw_block('hyp2_reason11'),'nw:hyp2_reason11')
    jump r13_v111_hyp2_proof11

label r13_v111_hyp2_proof11:
    call r13_v111_proof('창고에서 잠자는 사람을 짚는다',['NW_KEEPER_DATE'],'r13_v111_hyp2_won11','r13_v111_hyp2_wrong11',None)
    jump expression _return

label r13_v111_hyp2_wrong11:
    if r13_nw_retry("hypothesis",['NW_KEEPER_DATE'],'백 부인이 고개를 돌린다. 창고에서 자는 사람을 짚어야 한다.'):
        jump r13_v111_hyp2_proof11
    jump r13_v111_hyp2_lost11

label r13_v111_hyp2_lost11:
    call r13_lines(r13_nw_block('hyp2_lost11'),'nw:hyp2_lost11')
    $ r13_v111_set('hyp_issue:2','lost')
    jump r13_v111_hyp3_q11

label r13_v111_hyp2_won11:
    call r13_lines(r13_nw_block('hyp2_won11'),'nw:hyp2_won11')
    $ r13_v111_set('hyp_issue:2','won')
    jump r13_v111_hyp3_q11

label r13_v111_hyp3_q11:
    call r13_nw_wrong_thought
    call r13_lines(r13_nw_block('hyp3_q11'),'nw:hyp3_q11')
    $ v111_claim='menu:hyp3'
    menu:
        '요즘 사람들이 약해졌다':
            jump r13_v111_hyp3_badreason11
        '외지 사람이 병을 들여왔다':
            jump r13_v111_hyp3_badreason11
        '요즘 태우는 돌이 더 독하다':
            jump r13_v111_hyp3_reason11

label r13_v111_hyp3_badreason11:
    if r13_nw_retry("hypothesis"):
        call r13_lines(r13_nw_block("hyp3_lost11"),"nw:hyp3_lost11:retry")
        jump r13_v111_hyp3_q11
    jump r13_v111_hyp3_lost11

label r13_v111_hyp3_reason11:
    call r13_lines(r13_nw_block('hyp3_reason11'),'nw:hyp3_reason11')
    jump r13_v111_hyp3_proof11

label r13_v111_hyp3_proof11:
    call r13_v111_proof('요즘 돌이 어디서 오는지 대조한다',['NW_INNER_PRICE', 'NW_MUSOE_DEEP'],'r13_v111_hyp3_won11','r13_v111_hyp3_wrong11',None)
    jump expression _return

label r13_v111_hyp3_wrong11:
    if r13_nw_retry("hypothesis",['NW_INNER_PRICE', 'NW_MUSOE_DEEP'],'판돌이 고개를 젓는다. “무쇠는 원래 고집이 셌소.” 돌값과 갱도 이야기를 함께 놓아야 한다.'):
        jump r13_v111_hyp3_proof11
    jump r13_v111_hyp3_lost11

label r13_v111_hyp3_lost11:
    call r13_lines(r13_nw_block('hyp3_lost11'),'nw:hyp3_lost11')
    $ r13_v111_set('hyp_issue:3','lost')
    jump r13_v111_hyp4_q11

label r13_v111_hyp3_won11:
    call r13_lines(r13_nw_block('hyp3_won11'),'nw:hyp3_won11')
    $ r13_v111_set('hyp_issue:3','won')
    jump r13_v111_hyp4_q11

label r13_v111_hyp4_q11:
    call r13_nw_wrong_thought
    call r13_lines(r13_nw_block('hyp4_q11'),'nw:hyp4_q11')
    $ v111_claim='menu:hyp4'
    menu:
        '아이 방에도 아르카등이 밤새 켜져 있었다':
            jump r13_v111_hyp4_reason11
        '아이들은 어른보다 약하다':
            jump r13_v111_hyp4_badreason11
        '아이들이 아르카를 만지고 논다':
            jump r13_v111_hyp4_badreason11

label r13_v111_hyp4_badreason11:
    if r13_nw_retry("hypothesis"):
        call r13_lines(r13_nw_block("hyp4_lost11"),"nw:hyp4_lost11:retry")
        jump r13_v111_hyp4_q11
    jump r13_v111_hyp4_lost11

label r13_v111_hyp4_reason11:
    call r13_lines(r13_nw_block('hyp4_reason11'),'nw:hyp4_reason11')
    jump r13_v111_hyp4_proof11

label r13_v111_hyp4_proof11:
    call r13_v111_proof('아르카가 없는 아이들과 대조한다',['NW_KKOMI_NOSTONE', 'NW_SICK_BEDS'],'r13_v111_hyp4_won11','r13_v111_hyp4_wrong11',None)
    jump expression _return

label r13_v111_hyp4_wrong11:
    if r13_nw_retry("hypothesis",['NW_KKOMI_NOSTONE', 'NW_SICK_BEDS'],'주민이 아이를 끌어안는다. 돌이 없는 아이들과 표시가 붙은 아이들을 함께 놓아야 한다.'):
        jump r13_v111_hyp4_proof11
    jump r13_v111_hyp4_lost11

label r13_v111_hyp4_lost11:
    call r13_lines(r13_nw_block('hyp4_lost11'),'nw:hyp4_lost11')
    $ r13_v111_set('hyp_issue:4','lost')
    jump r13_v111_hyp5_q11

label r13_v111_hyp4_won11:
    call r13_lines(r13_nw_block('hyp4_won11'),'nw:hyp4_won11')
    $ r13_v111_set('hyp_issue:4','won')
    jump r13_v111_hyp5_q11

label r13_v111_hyp5_q11:
    call r13_nw_wrong_thought
    call r13_lines(r13_nw_block('hyp5_q11'),'nw:hyp5_q11')
    $ v111_claim='menu:hyp5'
    menu:
        '한 방의 돌이 바뀌자 한 사람이 한 저녁 사이에 무너졌다' if r13_v111_value('OWL_ALIVE') is False:
            jump r13_v111_hyp5_reason11
        '한 방의 돌을 치우자 무너지던 사람이 돌아왔다' if r13_v111_value('OWL_ALIVE') is not False and r13_v111_value('prevention')!='stone':
            jump r13_v111_hyp5_reason11
        # 2026-10-25 부엉이 예방 1단계: 7일 낮 돌을 꺼낸 판은 부엉이가 무너진 적이 없다. 그 앞에서 흐려진 것은 아빠의 머리였다.
        '한 방의 돌을 꺼내자 그 앞에서 흐려지던 머리가 맑아졌다' if r13_v111_value('prevention')=='stone':
            jump r13_v111_hyp5_reason11
        '부엉이 어르신은 원래 아팠다':
            jump r13_v111_hyp5_badreason11
        '13호가 추워서 그렇다':
            jump r13_v111_hyp5_badreason11

label r13_v111_hyp5_badreason11:
    if r13_nw_retry("hypothesis"):
        call r13_lines(r13_nw_block("hyp5_lost11"),"nw:hyp5_lost11:retry")
        jump r13_v111_hyp5_q11
    jump r13_v111_hyp5_lost11

label r13_v111_hyp5_reason11:
    call r13_lines(r13_nw_block('hyp5_reason11'),'nw:hyp5_reason11')
    jump r13_v111_hyp5_proof11

label r13_v111_hyp5_proof11:
    call r13_v111_proof('13호 난로의 돌을 내놓는다',['NW_STONE'],'r13_v111_hyp5_won11','r13_v111_hyp5_wrong11',None)
    jump expression _return

label r13_v111_hyp5_wrong11:
    if r13_nw_retry("hypothesis"):
        jump r13_v111_hyp5_proof11
    jump r13_v111_hyp5_lost11

label r13_v111_hyp5_lost11:
    call r13_lines(r13_nw_block('hyp5_lost11'),'nw:hyp5_lost11')
    jump r13_v111_hyp_lost_gate11

label r13_v111_hyp5_won11:
    call r13_lines(r13_nw_block('hyp5_won11'),'nw:hyp5_won11')
    $ r13_nw_meeting_end("hypothesis","win" if all(r13_v111_value("hyp_issue:%d"%i)=="won" for i in (1,2,3,4)) else "partial")
    call r13_lines(r13_nw_block('hyp_chief11'),'nw:hyp_chief11')
    jump r13_v111_hyp_end11

label r13_v111_hyp_lost_gate11:
    $ r13_nw_meeting_end("hypothesis","lose")
    call r13_lines(r13_nw_block('hyp_lose11'),'nw:hyp_lose11')
    jump r13_v111_hyp_end11

label r13_v111_hyp_end11:
    if r13_v111_value("guldol_facility_seen"):
        $ r13_nw_list("resident_guldol","facility")
    call r13_lines(r13_nw_block('hyp_result11'),'nw:hyp_result11')
    jump r13_v111_night11

label r13_v111_night11:
    $ r13_v111_scene('MS14_D11_S04')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','night11',['mom', 'daram'])
    $ r13_v111_arrive(['mom', 'daram', 'resident_teacher', 'karo', 'resident_nero'])
    $ r13_v111_score()
    $ r13_v111_arrive(['mom', 'daram', 'resident_teacher', 'karo', 'resident_nero'])
    call r13_lines(r13_nw_block('night_lights11'),'nw:night_lights11')
    $ r13_v111_set('lower_lights_cut',True)
    if r13_v111_value('carried_dry_blankets')>0:
        call r13_v111_rest_blanket11

label r13_v111_night_rescue_route11:
    if r13_v111_value('lower_road_arrived11')==3 and r13_v111_value('lower_road_handover')!=3:
        $ r13_v111_set('rescue_handoff_period11','night')
        jump r13_v111_rescue_handoff11
    if r13_v111_value('lower_road_handover')==3:
        jump r13_v111_lower_safe11
    jump r13_v111_request_rescue11

label r13_v111_rest_blanket11:
    call r13_lines(r13_v111_lines(['MS14_D11_S04_L0003']),'v111:MS14_D11_S04_L0003')
    call r13_lines(r13_v111_lines(['MS14_D11_S04_L0004']),'v111:MS14_D11_S04_L0004')
    call r13_lines(r13_v111_lines(['MS14_D11_S04_L0006']),'v111:MS14_D11_S04_L0006')
    call r13_lines(r13_v111_lines(['MS14_D11_S04_L0007']),'v111:MS14_D11_S04_L0007')
    return

label r13_v111_lower_safe11:
    $ r13_fork_set_fate('fate_nero','handover')
    if r13_v111_actor_ready('resident_nero'):
        call r13_lines(r13_v111_lines(['MS14_D11_S04_L0030']),'v111:MS14_D11_S04_L0030')
    call r13_lines(r13_v111_lines(['MS14_D11_S04_L0031']),'v111:MS14_D11_S04_L0031')
    if r13_v111_actor_ready('resident_nero'):
        call r13_lines(r13_v111_lines(['MS14_D11_S04_L0032']),'v111:MS14_D11_S04_L0032')
    $ r13_v111_set('nero_alive',True)
    jump r13_v111_sleep11

label r13_v111_request_rescue11:
    if r13_v111_actor_ready('resident_nero'):
        call r13_lines(r13_v111_lines(['MS14_D11_S04_L0009']),'v111:MS14_D11_S04_L0009')
    call r13_lines(r13_v111_lines(['MS14_D11_S04_L0010']),'v111:MS14_D11_S04_L0010')
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D11_S04_L0011']),'v111:MS14_D11_S04_L0011')
    call r13_lines(r13_v111_lines(['MS14_D11_S04_L0012']),'v111:MS14_D11_S04_L0012')
    if r13_v111_actor_ready('resident_nero'):
        call r13_lines(r13_v111_lines(['MS14_D11_S04_L0013']),'v111:MS14_D11_S04_L0013')
    jump r13_v111_night_rescue_prepare11

label r13_v111_night_rescue_prepare11:
    call r13_v111_wait('night_rescue_prepare11')
    if _return==1:
        if not r13_v111_value('school_supply_handed'):
            jump r13_v111_late_supply11
        jump r13_v111_late_road11
    if _return==0:
        jump r13_v111_night_rescue_choices11
    jump r13_v111_night_rescue_prepare11

label r13_v111_night_rescue_choices11:
    if r13_nero_transport_ready11() and r13_v111_value('school_supply_handed'):
        jump r13_v111_night_rescue11
    if not r13_v111_value('school_supply_handed'):
        jump r13_v111_late_supply11
    jump r13_v111_late_cart11

label r13_v111_night_rescue11:
    call r13_v111_travel('forest','night_rescue11',[])
    $ r13_v111_arrive(['karo', 'resident_nero'])
    if r13_v111_actor_ready('resident_nero'):
        call r13_lines(r13_v111_lines(['MS14_D11_S04_L0016']),'v111:MS14_D11_S04_L0016')
    jump r13_v111_snow_door11

label r13_v111_snow_door11:
    call r13_v111_wait('snow_door11')
    if _return==0:
        jump r13_v111_night_rescue_done11
    jump r13_v111_snow_door11

label r13_v111_night_rescue_done11:
    call r13_lines(r13_v111_lines(['MS14_D11_S04_L0018']),'v111:MS14_D11_S04_L0018')
    call r13_lines(r13_v111_lines(['MS14_D11_S04_L0019']),'v111:MS14_D11_S04_L0019')
    call r13_v111_travel('school','night_rescue_done11')
    $ r13_v111_arrive(['mom', 'daram', 'resident_teacher', 'karo', 'resident_nero'])
    if r13_v111_actor_ready('resident_nero'):
        call r13_lines(r13_v111_lines(['MS14_D11_S04_L0021']),'v111:MS14_D11_S04_L0021')
    call r13_lines(r13_v111_lines(['MS14_D11_S04_L0022']),'v111:MS14_D11_S04_L0022')
    if r13_v111_actor_ready('resident_nero'):
        call r13_lines(r13_v111_lines(['MS14_D11_S04_L0023']),'v111:MS14_D11_S04_L0023')
    call r13_lines(r13_v111_lines(['MS14_D11_S04_L0024']),'v111:MS14_D11_S04_L0024')
    $ r13_v111_set('lower_road_arrived11',3)
    $ r13_v111_set('rescue_handoff_period11','night')
    jump r13_v111_rescue_handoff11

label r13_v111_rescue_handoff11:
    $ r13_v111_arrive(['mom','daram','resident_teacher','nabi','karo','resident_nero'])
    call r13_v111_wait('rescue_handoff11')
    if _return==0 and r13_nero_receiver_ready11():
        call r13_lines(r13_nw_block('nr_handoff11'),'nw:nr_handoff11')
        $ r13_v111_set('lower_road_handover',3)
        $ r13_v111_set('nero_alive',True)
        $ r13_v111_set('alive:v111_lowerroad_elder',True)
        if r13_v111_value('rescue_handoff_period11')=='day':
            $ r13_fork_set_fate('fate_nero','handover')
            jump r13_v111_school_visit11
        $ r13_fork_set_fate('fate_nero','rescue')
        jump r13_v111_sleep11
    if _return==1:
        call r13_lines(r13_nw_block('nr_pending11'),'nw:nr_pending11')
        if r13_v111_value('rescue_handoff_period11')=='day':
            jump r13_v111_school_visit11
        jump r13_v111_sleep11
    jump r13_v111_rescue_handoff11

label r13_v111_late_supply11:
    call r13_lines(r13_v111_lines(['MS14_D11_S04_L0035']),'v111:MS14_D11_S04_L0035')
    if r13_v111_actor_ready('resident_nero'):
        call r13_lines(r13_v111_lines(['MS14_D11_S04_L0036']),'v111:MS14_D11_S04_L0036')
    jump r13_v111_late_supply_handoff11

label r13_v111_late_supply_handoff11:
    call r13_v111_wait('late_supply_handoff11')
    if _return==0:
        jump r13_v111_late_supply_done11
    jump r13_v111_late_supply_handoff11

label r13_v111_late_supply_done11:
    $ r13_v111_set('school_supply_handed',True)
    $ r13_v111_set('school_heat_connected',False)
    $ r13_v111_apply('actual_late_school_supply11',[dict(op="acquire",key='E14_SUPPLY',variant="observed")])
    jump r13_v111_late_road11

label r13_v111_late_cart11:
    call r13_lines(r13_v111_lines(['MS14_D11_S04_L0037']),'v111:MS14_D11_S04_L0037')
    if r13_v111_actor_ready('resident_nero'):
        call r13_lines(r13_v111_lines(['MS14_D11_S04_L0038']),'v111:MS14_D11_S04_L0038')
    jump r13_v111_late_road11

label r13_v111_late_road11:
    $ r13_fork_set_fate('fate_nero','lost')
    call r13_v111_travel('forest','late_road11',[])
    $ r13_v111_arrive(['karo'])
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D11_S04_L0027']),'v111:MS14_D11_S04_L0027')
    call r13_lines(r13_v111_lines(['MS14_D11_S04_L0028']),'v111:MS14_D11_S04_L0028')
    $ r13_v111_set('lower_road_lost',True)
    $ r13_v111_set('location:resident_nero','forest')
    $ r13_v111_set('nero_alive',False)
    # D4: 네로가 데리러 가던 아랫길 노인도 함께 묻힌다.
    $ r13_v111_set('alive:v111_lowerroad_elder',False)
    call r13_lines(r13_nw_block('lower_elder11'),'nw:lower_elder11')
    jump r13_v111_sleep11

label r13_v111_sleep11:
    call r13_v111_travel('school','sleep11')
    jump r13_v111_sleep11_input

label r13_v111_sleep11_input:
    call r13_v111_wait('sleep11_input')
    if _return==80:
        call r13_hp_visit11
        jump r13_v111_sleep11_input
    if _return==81:
        call r13_hp_wood11
        jump r13_v111_sleep11_input
    if _return==0:
        jump r13_v111_sleep11_done
    jump r13_v111_sleep11_input

label r13_v111_sleep11_done:
    $ r13_v111_set("day",12)
    jump r13_v111_day12

label r13_v111_day12:
    $ r13_v111_scene('MS14_D12_S01')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','day12',['mom', 'daram'])
    $ r13_v111_arrive(['mom', 'daram', 'karo', 'guard', 'resident_teacher', 'resident_nero'])
    $ r13_v111_score()
    $ r13_v111_arrive(['mom', 'daram', 'karo', 'guard', 'resident_teacher', 'resident_nero'])

label r13_v111_loss_route12:
    if r13_v111_value('lower_road_lost'):
        jump r13_v111_loss_names12
    jump r13_v111_living_names12

label r13_v111_loss_names12:
    call r13_v111_travel('forest','loss_names12',[])
    $ r13_v111_arrive(['karo'])
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0002']),'v111:MS14_D12_S01_L0002')
    call r13_v111_travel('square','names_square12')
    $ r13_v111_arrive(['daram', 'karo'])
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0005']),'v111:MS14_D12_S01_L0005')
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0006']),'v111:MS14_D12_S01_L0006')
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0007']),'v111:MS14_D12_S01_L0007')
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0008']),'v111:MS14_D12_S01_L0008')
    if r13_v111_value('alive:v111_lowerroad_elder') is False:
        call r13_lines(r13_nw_block('elder_name12'),'nw:elder_name12')
    jump r13_v111_morning_notice12

label r13_v111_living_names12:
    if r13_v111_actor_ready('resident_nero'):
        call r13_lines(r13_v111_lines(['MS14_D12_S01_L0011']),'v111:MS14_D12_S01_L0011')
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0012']),'v111:MS14_D12_S01_L0012')
    if r13_v111_actor_ready('resident_nero'):
        call r13_lines(r13_v111_lines(['MS14_D12_S01_L0013']),'v111:MS14_D12_S01_L0013')
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0014']),'v111:MS14_D12_S01_L0014')
    if r13_v111_actor_ready('resident_nero'):
        call r13_lines(r13_v111_lines(['MS14_D12_S01_L0015']),'v111:MS14_D12_S01_L0015')
    jump r13_v111_morning_notice12

label r13_v111_morning_notice12:
    call r13_v111_travel('school','notice12')
    $ r13_v111_arrive(['mom', 'daram', 'guard', 'resident_teacher'])
    # 0.20.18 (소유자 2026-10-23 "착한 선택 한다고 좋은 결과가 안 나오게", CRUEL_CHOICES.md C2·C4): 2일에 피코를
    # 들여 담요를 못 받았거나 11일 토실에게 한 장을 건넨 판은, 그날 밤 다람이 외투로 버티고 아침에 열이 난다.
    if r13_v111_value('carried_dry_blankets')<2 and r13_v111_actor_ready('daram') and not r13_v111_value('daram_fever12'):
        $ r13_v111_set('daram_fever12',True)
        call r13_lines(r13_nw_block('daram_fever12'),'nw:daram_fever12')
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0017']),'v111:MS14_D12_S01_L0017')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D12_S01_L0018']),'v111:MS14_D12_S01_L0018')
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0019']),'v111:MS14_D12_S01_L0019')
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0020']),'v111:MS14_D12_S01_L0020')
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0021']),'v111:MS14_D12_S01_L0021')
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0023']),'v111:MS14_D12_S01_L0023')
    $ r13_nw_acquire("NW_TRANSFER_LIST")
    jump r13_v111_morning_prep12_entry

label r13_v111_morning_prep12_entry:
    $ r13_v111_scene("MS14_D12_S01")
    jump r13_v111_morning_prep12

label r13_v111_morning_prep12:
    call r13_v111_wait('morning_prep12')
    if _return==0:
        jump r13_v111_medicine12
    if _return==1:
        jump r13_v111_warm_place12
    if _return==2:
        jump r13_v111_carrier12
    if _return==3:
        jump r13_v111_meal12
    if _return==4:
        jump r13_v111_madam_invite12
    jump r13_v111_morning_prep12

label r13_v111_madam_invite12:
    $ r13_v111_arrive(['resident_madam'])
    call r13_lines([("resident_madam","내놓은 돌이 어디 쓰이는지는 보겠어요.",{"no_lead":True})],"v111:madam_observer_consent12")
    $ r13_v111_set('madam_observer_consent',True)
    call r13_v111_travel('school','madam_school12',[])
    $ r13_v111_arrive(['mom', 'daram', 'resident_teacher', 'resident_madam'])
    jump r13_v111_morning_prep12_entry

label r13_v111_medicine12:
    $ r13_v111_arrive(['resident_seori'])
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0024']),'v111:MS14_D12_S01_L0024')
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0025']),'v111:MS14_D12_S01_L0025')
    $ r13_v111_set('medicine_locked',True)
    jump r13_v111_morning_prep12_entry

label r13_v111_warm_place12:
    call r13_v111_travel('school','warm_place12')
    $ r13_v111_arrive(['mom', 'daram', 'resident_teacher'])
    # 열이 난 판: 하나뿐인 난로 옆자리를 다람이 쓴다. 배식 때 쓸 자리는 끝내 마련되지 않는다(조기 예방 불가).
    if r13_v111_value('daram_fever12'):
        call r13_lines(r13_nw_block('fever_seat12'),'nw:fever_seat12')
        $ r13_v111_set('warm_seat_taken12',True)
        jump r13_v111_morning_prep12_entry
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0026']),'v111:MS14_D12_S01_L0026')
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0027']),'v111:MS14_D12_S01_L0027')
    $ r13_v111_set('warm_seat_ready',True)
    jump r13_v111_morning_prep12_entry

label r13_v111_carrier12:
    $ r13_v111_arrive(['karo'])
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D12_S01_L0028']),'v111:MS14_D12_S01_L0028')
    call r13_lines(r13_v111_lines(['MS14_D12_S01_L0029']),'v111:MS14_D12_S01_L0029')
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D12_S01_L0030']),'v111:MS14_D12_S01_L0030')
    call r13_v111_travel('school','carrier_arrived12')
    $ r13_v111_arrive(['karo', 'mom', 'daram', 'resident_teacher'])
    $ r13_v111_set('carrier_arrived',True)
    $ r13_v111_set('busy:karo','school_transport')
    jump r13_v111_carrier_receipt12

label r13_v111_carrier_receipt12:
    call r13_v111_wait('carrier_receipt12')
    if _return==0:
        jump r13_v111_carrier_received12
    jump r13_v111_carrier_receipt12

label r13_v111_carrier_received12:
    $ r13_v111_set('warm_support_arrived',True)
    $ r13_v111_set('school_supply_handed',True)
    $ r13_v111_apply('actual_school_supply12',[dict(op="acquire",key='E14_SUPPLY',variant="observed")])
    $ r13_v111_set('busy:karo',False)
    jump r13_v111_morning_prep12_entry

label r13_v111_meal12:
    $ r13_v111_scene('MS14_D12_S02')
    $ r13_edit(period=1)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','meal12',['daram'])
    $ r13_v111_arrive(['daram', 'nabi', 'resident_teacher', 'resident_bori', 'kid_dodam', 'kid_saemi'])
    $ r13_v111_score()
    $ r13_v111_arrive(['daram', 'nabi', 'resident_teacher', 'resident_bori', 'kid_dodam', 'kid_saemi'])
    # 검토 0.20.4 연결 3 / 후반 기획서 A: 준비를 보완하고 돌아오면 도입을 되풀이하지 않는다.
    # 이미 정한 배식 분기를 되돌리지 않도록 route12 초기화보다 먼저 판정한다.
    if r13_v111_value('meal12_intro_seen'):
        $ r13_v111_set('location:mom','facility')
        call r13_lines(r13_nw_block('meal12_return'),'nw:meal12_return')
        jump r13_v111_meal_choice12
    $ r13_v111_set('route12','uncommitted')
    $ r13_v111_set('location:mom','facility')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0003']),'v111:MS14_D12_S02_L0003')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0004']),'v111:MS14_D12_S02_L0004')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0005']),'v111:MS14_D12_S02_L0005')
    # 2026-10-24 지시서 02 감정선(도담): 7일에 빌린 숟가락을 다람이 보리 자리에 놓았는지(그 저녁 창가 지문이 읽는다).
    $ r13_v111_set('dodam_spoon12',bool(r13_v111_value('dodam_spoon7')) and r13_v111_actor_ready('daram'))
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0007']),'v111:MS14_D12_S02_L0007')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0008']),'v111:MS14_D12_S02_L0008')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0009']),'v111:MS14_D12_S02_L0009')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0010']),'v111:MS14_D12_S02_L0010')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0011']),'v111:MS14_D12_S02_L0011')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0012']),'v111:MS14_D12_S02_L0012')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0013']),'v111:MS14_D12_S02_L0013')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0014']),'v111:MS14_D12_S02_L0014')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0015']),'v111:MS14_D12_S02_L0015')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0017']),'v111:MS14_D12_S02_L0017')
    # 0.20.7 (owner days 2-14 #6): Dad sets the white bowls out himself, an ordinary chore now.
    $ renpy.display_menu([("흰 그릇을 작은 배식대로 나른다",0)])
    $ r13_v111_set("bowls_carried12",True)
    call r13_lines(r13_nw_block('bowls_carried12'),'nw:bowls_carried12')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0018']),'v111:MS14_D12_S02_L0018')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0019']),'v111:MS14_D12_S02_L0019')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0020']),'v111:MS14_D12_S02_L0020')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0021']),'v111:MS14_D12_S02_L0021')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0023']),'v111:MS14_D12_S02_L0023')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0024']),'v111:MS14_D12_S02_L0024')
    $ r13_nw_acquire("NW_WHITE_BOWLS","daram" if r13_v111_value("meeting:room13")=="lose" else "observed")
    $ r13_v111_set('bottle_original_seal_seen',True)
    # 도입·관찰·획득이 모두 끝난 뒤에만 기록한다(구형 저장은 기본값 미완료로 한 번 보여 준다).
    $ r13_v111_set('meal12_intro_seen',True)
    jump r13_v111_meal_choice12

label r13_v111_meal_choice12:
    menu:
        '배식 전에 더 살핀다':
            jump r13_v111_stay_meal12
        '다람과 장작을 받으러 간다':
            jump r13_v111_take_daram12
        '다람은 나비 곁에 두고 다녀온다':
            jump r13_v111_leave_daram12
        '아침에 부탁한 일들을 확인한다':
            jump r13_v111_prevent_check12

label r13_v111_prevent_check12:
    if all(r13_v111_value(k) for k in ("medicine_locked","warm_seat_ready","carrier_arrived","warm_support_arrived")):
        jump r13_v111_prevent_ready12
    if not r13_v111_value("medicine_locked"):
        jump r13_v111_medicine_missing12
    if not r13_v111_value("warm_seat_ready"):
        jump r13_v111_seat_missing12
    jump r13_v111_carrier_missing12

label r13_v111_medicine_missing12:
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0034']),'v111:MS14_D12_S02_L0034')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0035']),'v111:MS14_D12_S02_L0035')
    jump r13_v111_morning_prep12_entry

label r13_v111_seat_missing12:
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0036']),'v111:MS14_D12_S02_L0036')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0037']),'v111:MS14_D12_S02_L0037')
    jump r13_v111_morning_prep12_entry

label r13_v111_carrier_missing12:
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0038']),'v111:MS14_D12_S02_L0038')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0039']),'v111:MS14_D12_S02_L0039')
    jump r13_v111_morning_prep12_entry

label r13_v111_prevent_ready12:
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0041']),'v111:MS14_D12_S02_L0041')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0042']),'v111:MS14_D12_S02_L0042')
    $ r13_v111_commit('MS14_D12_S02_L0042')
    jump r13_v111_early12

label r13_v111_stay_meal12:
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0026']),'v111:MS14_D12_S02_L0026')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0027']),'v111:MS14_D12_S02_L0027')
    jump r13_v111_meal_inspect12

label r13_v111_meal_inspect12:
    call r13_v111_wait('meal_inspect12')
    if _return==0:
        call r13_lines(r13_nw_block('sp_smallpot12'),'nw:sp_smallpot12')
        $ r13_v111_set('soup_smallpot_seen12',True)
    elif _return==1:
        call r13_lines(r13_nw_block('sp_bowls12'),'nw:sp_bowls12')
        $ r13_v111_set('soup_bowls_seen12',True)
    elif _return==2:
        call r13_lines(r13_nw_block('sp_bottle12'),'nw:sp_bottle12')
        $ r13_v111_set('soup_bottle_seen12',True)
    elif _return==3 and r13_soup_inspect_ready12():
        call r13_lines(r13_nw_block('sp_separate12'),'nw:sp_separate12')
        $ r13_v111_set('soup_serving_separated12',True)
        $ r13_v111_set('route12','premeal_stopped')
        jump r13_v111_premeal12
    elif _return==4:
        jump r13_v111_meal_choice12
    jump r13_v111_meal_inspect12

label r13_v111_take_daram12:
    $ r13_fork_set_fate('fate_soup','lost')
    $ r13_v111_set('route12','late_exposure')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0028']),'v111:MS14_D12_S02_L0028')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0029']),'v111:MS14_D12_S02_L0029')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0030']),'v111:MS14_D12_S02_L0030')
    $ r13_v111_set('DARAM_location','with_father')
    jump r13_v111_pickup12

label r13_v111_leave_daram12:
    $ r13_fork_set_fate('fate_soup','lost')
    $ r13_v111_set('route12','late_exposure')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0031']),'v111:MS14_D12_S02_L0031')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0032']),'v111:MS14_D12_S02_L0032')
    call r13_lines(r13_v111_lines(['MS14_D12_S02_L0033']),'v111:MS14_D12_S02_L0033')
    $ r13_v111_set('DARAM_location','school')
    $ r13_v111_set('busy:nabi','daram_guard')
    jump r13_v111_pickup12

label r13_v111_pickup12:
    call r13_v111_travel('facility','pickup12')
    $ r13_v111_arrive(['mom'])
    if r13_v111_value("DARAM_location")=="with_father":
        $ r13_v111_arrive(["mom","daram"])
    jump r13_v111_pickup_box12

label r13_v111_pickup_box12:
    call r13_v111_wait('pickup_box12')
    if _return==0:
        jump r13_v111_pickup_done12
    jump r13_v111_pickup_box12

label r13_v111_pickup_done12:
    $ r13_v111_set('heat_box_received',True)
    jump r13_v111_late_meal12

label r13_v111_late_meal12:
    $ r13_v111_scene('MS14_D12_S03')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','late_meal12',['daram'])
    $ r13_v111_arrive(['daram', 'nabi', 'resident_bori', 'resident_teacher', 'kid_saemi'])
    $ r13_v111_score()
    $ r13_v111_arrive(['daram', 'nabi', 'resident_bori', 'resident_teacher', 'kid_saemi'])
    $ r13_v111_set('busy:nabi',False)
    call r13_lines(r13_v111_lines(['MS14_D12_S03_L0002']),'v111:MS14_D12_S03_L0002')
    call r13_lines(r13_v111_lines(['MS14_D12_S03_L0003']),'v111:MS14_D12_S03_L0003')
    call r13_lines(r13_v111_lines(['MS14_D12_S03_L0004']),'v111:MS14_D12_S03_L0004')
    call r13_lines(r13_v111_lines(['MS14_D12_S03_L0005']),'v111:MS14_D12_S03_L0005')
    # D3: 6일에 살린 꼬미도 같은 냄비를 먹었다.
    if r13_v111_value('KKOMI_ALIVE') is True:
        call r13_lines(r13_nw_block('kkomi_soup12'),'nw:kkomi_soup12')
        $ r13_v111_set('KKOMI_ALIVE',False)
        $ r13_v111_set('kkomi_soup_dead',True)
    call r13_lines(r13_v111_lines(['MS14_D12_S03_L0007']),'v111:MS14_D12_S03_L0007')
    call r13_lines(r13_v111_lines(['MS14_D12_S03_L0008']),'v111:MS14_D12_S03_L0008')
    call r13_lines(r13_v111_lines(['MS14_D12_S03_L0009']),'v111:MS14_D12_S03_L0009')
    call r13_lines(r13_v111_lines(['MS14_D12_S03_L0010']),'v111:MS14_D12_S03_L0010')
    call r13_lines(r13_v111_lines(['MS14_D12_S03_L0011']),'v111:MS14_D12_S03_L0011')
    $ r13_v111_set('medical_called',True)
    $ r13_v111_set('busy:resident_bori','medical_call')
    jump r13_v111_soup_fragment12

label r13_v111_soup_fragment12:
    call r13_v111_wait('soup_fragment12')
    if _return==0:
        jump r13_v111_fragment_seen12
    jump r13_v111_soup_fragment12

label r13_v111_fragment_seen12:
    call r13_lines(r13_v111_lines(['MS14_D12_S03_L0013']),'v111:MS14_D12_S03_L0013')
    call r13_lines(r13_v111_lines(['MS14_D12_S03_L0014']),'v111:MS14_D12_S03_L0014')
    call r13_lines(r13_v111_lines(['MS14_D12_S03_L0016']),'v111:MS14_D12_S03_L0016')
    call r13_lines(r13_v111_lines(['MS14_D12_S03_L0017']),'v111:MS14_D12_S03_L0017')
    call r13_lines(r13_v111_lines(['MS14_D12_S03_L0018']),'v111:MS14_D12_S03_L0018')
    call r13_lines(r13_v111_lines(['MS14_D12_S03_L0019']),'v111:MS14_D12_S03_L0019')
    $ r13_v111_set('soup_fragment_observed',True)
    jump r13_v111_soup_hearing12

label r13_v111_premeal12:
    $ r13_fork_set_fate('fate_soup','premeal')
    $ r13_v111_scene('MS14_D12_A')
    $ r13_edit(period=1)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','premeal12',['daram'])
    $ r13_v111_arrive(['daram', 'nabi', 'resident_teacher', 'resident_bori', 'kid_dodam', 'kid_saemi'])
    $ r13_v111_score()
    $ r13_v111_arrive(['daram', 'nabi', 'resident_teacher', 'resident_bori', 'kid_dodam', 'kid_saemi'])
    $ r13_v111_set('route12','premeal_stopped')
    call r13_lines(r13_v111_lines(['MS14_D12_A_L0002']),'v111:MS14_D12_A_L0002')
    call r13_lines(r13_v111_lines(['MS14_D12_A_L0003']),'v111:MS14_D12_A_L0003')
    call r13_lines(r13_v111_lines(['MS14_D12_A_L0004']),'v111:MS14_D12_A_L0004')
    call r13_lines(r13_v111_lines(['MS14_D12_A_L0005']),'v111:MS14_D12_A_L0005')
    call r13_lines(r13_v111_lines(['MS14_D12_A_L0006']),'v111:MS14_D12_A_L0006')
    call r13_lines(r13_v111_lines(['MS14_D12_A_L0007']),'v111:MS14_D12_A_L0007')
    call r13_lines(r13_v111_lines(['MS14_D12_A_L0008']),'v111:MS14_D12_A_L0008')
    $ r13_v111_set('medical_called',True)
    $ r13_v111_set('busy:resident_bori','medical_call')
    $ r13_v111_set('soup_fragment_observed',True)
    jump r13_v111_soup_hearing12

label r13_v111_soup_hearing12:
    $ r13_v111_scene('MS14_D12_S04')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','soup_hearing12',['daram'])
    $ r13_v111_arrive(['daram', 'nabi', 'resident_teacher', 'resident_madam'])
    $ r13_v111_score()
    $ r13_v111_arrive(['daram', 'nabi', 'resident_teacher', 'resident_madam'])
    if r13_v111_value('route12')=='late_exposure':
        call r13_v111_meal_observations12
    jump r13_v111_bottle_match12

label r13_v111_meal_observations12:
    if r13_v111_actor_ready('resident_madam'):
        call r13_lines(r13_v111_lines(['MS14_D12_S04_L0002']),'v111:MS14_D12_S04_L0002')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0003']),'v111:MS14_D12_S04_L0003')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0004']),'v111:MS14_D12_S04_L0004')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0005']),'v111:MS14_D12_S04_L0005')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0006']),'v111:MS14_D12_S04_L0006')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0007']),'v111:MS14_D12_S04_L0007')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0008']),'v111:MS14_D12_S04_L0008')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0010']),'v111:MS14_D12_S04_L0010')
    if r13_v111_value("bowls_carried12"):
        call r13_lines(r13_nw_block('bowls_recall12'),'nw:bowls_recall12')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0011']),'v111:MS14_D12_S04_L0011')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0012']),'v111:MS14_D12_S04_L0012')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0013']),'v111:MS14_D12_S04_L0013')
    return

label r13_v111_bottle_match12:
    call r13_v111_wait('bottle_match12')
    if _return==0:
        jump r13_v111_bottle_matched12
    # 2026-10-24 대승리 S1: 11일 주머니에 넣은 그릇을 작은 배식대 옆에 놓아 본 판에서만 자료가 된다.
    if _return==1:
        call r13_v111_bowl_compare12
    jump r13_v111_bottle_match12

label r13_v111_bottle_matched12:
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0015']),'v111:MS14_D12_S04_L0015')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0016']),'v111:MS14_D12_S04_L0016')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0017']),'v111:MS14_D12_S04_L0017')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0018']),'v111:MS14_D12_S04_L0018')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0019']),'v111:MS14_D12_S04_L0019')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0020']),'v111:MS14_D12_S04_L0020')
    $ r13_v111_apply('fragment_comparison12',[dict(op="acquire",key='E12_FRAGMENT',variant="observed")])
    $ r13_v111_apply('original_seal_recalled12',[dict(op="acquire",key='E12_SEAL',variant="observed")])
    jump r13_v111_seal_proof12

label r13_v111_seal_proof12:
    $ r13_meeting_checkpoint("soup")
    call r13_v111_proof('재사용 설명과 개봉 봉인을 대조한다',['E12_FRAGMENT', 'E12_SEAL'],'r13_v111_seal_answer12','r13_v111_medicine_wrong12','r13_v111_soup_hint12')
    jump expression _return

label r13_v111_seal_answer12:
    if r13_v111_value('route12')=='late_exposure':
        jump r13_v111_seal_late12
    jump r13_v111_seal_pre12

label r13_v111_seal_late12:
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0022']),'v111:MS14_D12_S04_L0022')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0023']),'v111:MS14_D12_S04_L0023')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0024']),'v111:MS14_D12_S04_L0024')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0025']),'v111:MS14_D12_S04_L0025')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0026']),'v111:MS14_D12_S04_L0026')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0027']),'v111:MS14_D12_S04_L0027')
    jump r13_v111_handling12

label r13_v111_seal_pre12:
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0062']),'v111:MS14_D12_S04_L0062')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0063']),'v111:MS14_D12_S04_L0063')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0064']),'v111:MS14_D12_S04_L0064')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0065']),'v111:MS14_D12_S04_L0065')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0066']),'v111:MS14_D12_S04_L0066')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0067']),'v111:MS14_D12_S04_L0067')
    jump r13_v111_handling12

label r13_v111_handling12:

label r13_v111_handling_route12:
    if r13_v111_value('route12')=='late_exposure':
        jump r13_v111_handling_late12
    jump r13_v111_handling_pre12

label r13_v111_handling_late12:
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0029']),'v111:MS14_D12_S04_L0029')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0030']),'v111:MS14_D12_S04_L0030')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0031']),'v111:MS14_D12_S04_L0031')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0032']),'v111:MS14_D12_S04_L0032')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0033']),'v111:MS14_D12_S04_L0033')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0034']),'v111:MS14_D12_S04_L0034')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0035']),'v111:MS14_D12_S04_L0035')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0036']),'v111:MS14_D12_S04_L0036')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0037']),'v111:MS14_D12_S04_L0037')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0038']),'v111:MS14_D12_S04_L0038')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0039']),'v111:MS14_D12_S04_L0039')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0040']),'v111:MS14_D12_S04_L0040')
    jump r13_v111_medical_arrival12

label r13_v111_handling_pre12:
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0068']),'v111:MS14_D12_S04_L0068')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0069']),'v111:MS14_D12_S04_L0069')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0070']),'v111:MS14_D12_S04_L0070')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0071']),'v111:MS14_D12_S04_L0071')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0072']),'v111:MS14_D12_S04_L0072')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0073']),'v111:MS14_D12_S04_L0073')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0074']),'v111:MS14_D12_S04_L0074')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0075']),'v111:MS14_D12_S04_L0075')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0076']),'v111:MS14_D12_S04_L0076')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0077']),'v111:MS14_D12_S04_L0077')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0078']),'v111:MS14_D12_S04_L0078')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0079']),'v111:MS14_D12_S04_L0079')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0094']),'v111:MS14_D12_S04_L0094')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0095']),'v111:MS14_D12_S04_L0095')
    jump r13_v111_medical_arrival12

label r13_v111_medical_arrival12:
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0042']),'v111:MS14_D12_S04_L0042')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0044']),'v111:MS14_D12_S04_L0044')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0045']),'v111:MS14_D12_S04_L0045')
    if r13_v111_value('route12')=='late_exposure':
        call r13_lines(r13_v111_lines(['MS14_D12_S04_L0046']),'v111:MS14_D12_S04_L0046')
        # 검토 0.20.4 추가 2: 서리가 좁혀 말한 범위를 아빠가 한 번 짚는다. 어느 쪽이든 고백은 바로 이어진다.
        menu:
            '약장 밖에 맡긴 약도 있는지 묻는다':
                call r13_lines(r13_nw_block('seori_ask12'),'nw:seori_ask12')
            '장부를 다시 보여 달라고 한다':
                call r13_lines(r13_nw_block('seori_ledger12'),'nw:seori_ledger12')
        call r13_lines(r13_nw_block('seori_confess12'),'nw:seori_confess12')
    $ r13_v111_arrive(['daram', 'nabi', 'resident_teacher', 'resident_seori', 'resident_bori', 'guard', 'neoul'])
    $ r13_v111_set('busy:resident_bori',False)
    $ r13_v111_set('medical_arrived',True)
    $ r13_v111_apply('handling_observed12',[dict(op="acquire",key='E12_HANDLING',variant="observed")])
    jump r13_v111_soup_final12

label r13_v111_soup_final12:
    call r13_v111_proof('파편·봉인·취급 구간을 함께 제시한다',['E12_FRAGMENT', 'E12_SEAL', 'E12_HANDLING'],'r13_v111_soup_conclusion12','r13_v111_fragment_wrong12','r13_v111_soup_hint_final12')
    jump expression _return

label r13_v111_soup_conclusion12:

label r13_v111_soup_conclusion_route12:
    if r13_v111_value('route12')=='late_exposure':
        jump r13_v111_conclusion_late12
    jump r13_v111_conclusion_pre12

label r13_v111_conclusion_late12:
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0048']),'v111:MS14_D12_S04_L0048')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0049']),'v111:MS14_D12_S04_L0049')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0050']),'v111:MS14_D12_S04_L0050')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0052']),'v111:MS14_D12_S04_L0052')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0053']),'v111:MS14_D12_S04_L0053')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0054']),'v111:MS14_D12_S04_L0054')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0055']),'v111:MS14_D12_S04_L0055')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0056']),'v111:MS14_D12_S04_L0056')
    jump r13_v111_confessed12

label r13_v111_conclusion_pre12:
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0080']),'v111:MS14_D12_S04_L0080')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0081']),'v111:MS14_D12_S04_L0081')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0082']),'v111:MS14_D12_S04_L0082')
    $ room13["v111"]["music_hold"]=room13["v111"]["scene"]
    $ renpy.music.stop(fadeout=.15)
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0084']),'v111:MS14_D12_S04_L0084')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0085']),'v111:MS14_D12_S04_L0085')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0086']),'v111:MS14_D12_S04_L0086')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0087']),'v111:MS14_D12_S04_L0087')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0088']),'v111:MS14_D12_S04_L0088')
    jump r13_v111_confessed12

label r13_v111_confessed12:
    $ room13["v111"]["music_hold"]=room13["v111"]["scene"]
    $ renpy.music.stop(fadeout=.15)
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0058']),'v111:MS14_D12_S04_L0058')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0059']),'v111:MS14_D12_S04_L0059')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0060']),'v111:MS14_D12_S04_L0060')
    $ r13_v111_set('teacher_confessed',True)
    call r13_lines(r13_nw_block('soup_list_q12'),'nw:soup_list_q12')
    jump r13_v111_list_proof12

label r13_v111_list_proof12:
    call r13_v111_proof('명단과 흰 그릇을 대조한다',['NW_TRANSFER_LIST', 'NW_WHITE_BOWLS'],'r13_v111_list_won12','r13_v111_list_wrong12',None)
    jump expression _return

label r13_v111_list_wrong12:
    if r13_nw_retry("soup",["NW_TRANSFER_LIST","NW_WHITE_BOWLS"],"선생님이 출석부를 끌어안는다. 명단의 칸과 흰 그릇을 함께 놓아야 한다."):
        jump r13_v111_list_proof12
    $ r13_nw_meeting_end("soup","partial")
    call r13_lines(r13_nw_block('soup_list_lost12'),'nw:soup_list_lost12')
    jump r13_v111_soup_after_route12

label r13_v111_list_won12:
    $ r13_nw_meeting_end("soup","win")
    $ r13_v111_set('transfer_list_secured',True)
    # 2026-10-24 대승리(GRAND_WIN_DESIGN.md 2-4): 돌아온 그릇으로 이겼으면 돌목이 이송 예정 칸을 무효로 적는다.
    if r13_v111_value("meeting:soup")=="win" and r13_nw_grand(["명단과 흰 그릇을 대조한다"],"NW_RETURNED_BOWL"):
        $ r13_v111_set("grand:soup",True)
        $ r13_v111_set("transfer_list_voided",True)
    call r13_lines(r13_nw_block('soup_list_won12'),'nw:soup_list_won12')
    jump r13_v111_soup_after_route12

label r13_v111_soup_after_route12:
    if r13_v111_value('route12')=='late_exposure':
        jump r13_v111_aftermath_late12
    jump r13_v111_aftermath_pre12

label r13_v111_medicine_wrong12:
    if r13_nw_retry("soup",['E12_FRAGMENT', 'E12_SEAL'],'선생님이 병을 감싼다. 파편과 봉인을 함께 놓아야 한다.'):
        call r13_lines(r13_v111_lines(['MS14_D12_S04_L0089', 'MS14_D12_S04_L0090']),'v111:medicine_wrong12:half')
        jump r13_v111_seal_proof12
    $ r13_nw_meeting_end("soup","lose")
    $ r13_v111_set('soup_lose_kind','stolen')
    $ r13_v111_set('seori_disciplined',True)
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0089']),'v111:MS14_D12_S04_L0089')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0090']),'v111:MS14_D12_S04_L0090')
    jump r13_v111_soup_lost12

label r13_v111_fragment_wrong12:
    if r13_nw_retry("soup",['E12_FRAGMENT', 'E12_SEAL', 'E12_HANDLING'],'나비가 고개를 젓는다. 파편과 봉인, 냄비를 건넨 구간을 함께 놓아야 한다.'):
        call r13_lines(r13_v111_lines(['MS14_D12_S04_L0091', 'MS14_D12_S04_L0092']),'v111:fragment_wrong12:half')
        jump r13_v111_soup_final12
    $ r13_nw_meeting_end("soup","lose")
    $ r13_v111_set('soup_lose_kind','nabi')
    $ r13_nw_list("nabi","soup_lose")
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0091']),'v111:MS14_D12_S04_L0091')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0092']),'v111:MS14_D12_S04_L0092')
    jump r13_v111_soup_lost12

label r13_v111_soup_lost12:
    call r13_lines(r13_nw_block('soup_lost12'),'nw:soup_lost12')
    jump r13_v111_sleep12

label r13_v111_soup_hint12:
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0093']),'v111:MS14_D12_S04_L0093')
    jump r13_v111_seal_proof12

label r13_v111_soup_hint_final12:
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0093']),'v111:MS14_D12_S04_L0093')
    jump r13_v111_soup_final12

label r13_v111_aftermath_pre12:
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0096']),'v111:MS14_D12_S04_L0096')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0097']),'v111:MS14_D12_S04_L0097')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0098']),'v111:MS14_D12_S04_L0098')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0099']),'v111:MS14_D12_S04_L0099')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0100']),'v111:MS14_D12_S04_L0100')
    $ r13_v111_set('book_promise12',True)
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0101']),'v111:MS14_D12_S04_L0101')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0102']),'v111:MS14_D12_S04_L0102')
    menu:
        '돌목에게 감독을 맡긴다':
            jump r13_v111_teacher_guard_pre12
        '너울에게 신병을 넘긴다':
            jump r13_v111_teacher_neoul_pre12

label r13_v111_teacher_guard_pre12:
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0103']),'v111:MS14_D12_S04_L0103')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0104']),'v111:MS14_D12_S04_L0104')
    $ r13_v111_commit('MS14_D12_S04_L0104')
    jump r13_v111_soup_pre_close12

label r13_v111_teacher_neoul_pre12:
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0105']),'v111:MS14_D12_S04_L0105')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0106']),'v111:MS14_D12_S04_L0106')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0107']),'v111:MS14_D12_S04_L0107')
    call r13_lines(r13_v111_lines(['MS14_D12_S04_L0108']),'v111:MS14_D12_S04_L0108')
    $ r13_v111_commit('MS14_D12_S04_L0108')
    jump r13_v111_soup_pre_close12

label r13_v111_soup_pre_close12:
    if r13_v111_value("school_heat_connected"):
        call r13_v111_pre_lights12
    else:
        call r13_v111_pre_no_lights12
    jump r13_v111_sleep12

label r13_v111_pre_lights12:
    return

label r13_v111_pre_no_lights12:
    $ r13_v111_arrive(['mom', 'daram', 'nabi', 'resident_teacher', 'guard', 'neoul'])
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0027']),'v111:MS14_D12_S05_L0027')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0028']),'v111:MS14_D12_S05_L0028')
    return

label r13_v111_aftermath_late12:
    $ r13_v111_scene('MS14_D12_S05')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','aftermath_late12',['daram'])
    $ r13_v111_arrive(['daram', 'nabi', 'resident_teacher', 'resident_seori', 'resident_bori', 'guard', 'neoul'])
    $ r13_v111_score()
    $ r13_v111_arrive(['daram', 'nabi', 'resident_teacher', 'resident_seori', 'resident_bori', 'guard', 'neoul'])
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0002']),'v111:MS14_D12_S05_L0002')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0003']),'v111:MS14_D12_S05_L0003')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0004']),'v111:MS14_D12_S05_L0004')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0006']),'v111:MS14_D12_S05_L0006')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0007']),'v111:MS14_D12_S05_L0007')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0008']),'v111:MS14_D12_S05_L0008')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0009']),'v111:MS14_D12_S05_L0009')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0010']),'v111:MS14_D12_S05_L0010')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0012']),'v111:MS14_D12_S05_L0012')
    if r13_v111_value('school_heat_connected'):
        call r13_v111_lights12
    else:
        call r13_v111_no_lights12
    $ r13_v111_commit('MS14_D12_S05_L0043')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0018']),'v111:MS14_D12_S05_L0018')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0019']),'v111:MS14_D12_S05_L0019')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0020']),'v111:MS14_D12_S05_L0020')
    if r13_v111_value('school_heat_connected'):
        call r13_v111_child_light12
    else:
        call r13_v111_child_dark12
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D12_S05_L0030']),'v111:MS14_D12_S05_L0030')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0031']),'v111:MS14_D12_S05_L0031')
    menu:
        '돌목에게 감독을 맡긴다':
            jump r13_v111_teacher_guard_late12
        '너울에게 신병을 넘긴다':
            jump r13_v111_teacher_neoul_late12

label r13_v111_teacher_guard_late12:
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0032']),'v111:MS14_D12_S05_L0032')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D12_S05_L0033']),'v111:MS14_D12_S05_L0033')
        $ r13_v111_commit('MS14_D12_S05_L0033')
    jump r13_v111_sleep12

label r13_v111_teacher_neoul_late12:
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0034']),'v111:MS14_D12_S05_L0034')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0035']),'v111:MS14_D12_S05_L0035')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0036']),'v111:MS14_D12_S05_L0036')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0037']),'v111:MS14_D12_S05_L0037')
    $ r13_v111_commit('MS14_D12_S05_L0037')
    jump r13_v111_sleep12

label r13_v111_lights12:
    $ r13_v111_arrive(['daram', 'mom', 'nabi', 'resident_teacher', 'resident_seori', 'resident_bori', 'guard', 'neoul'])
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0014']),'v111:MS14_D12_S05_L0014')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0016']),'v111:MS14_D12_S05_L0016')
    return

label r13_v111_no_lights12:
    $ r13_v111_arrive(['daram', 'mom', 'nabi', 'resident_teacher', 'resident_seori', 'resident_bori', 'guard', 'neoul'])
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0027']),'v111:MS14_D12_S05_L0027')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0028']),'v111:MS14_D12_S05_L0028')
    return

label r13_v111_child_light12:
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0022']),'v111:MS14_D12_S05_L0022')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0023']),'v111:MS14_D12_S05_L0023')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0024']),'v111:MS14_D12_S05_L0024')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0025']),'v111:MS14_D12_S05_L0025')
    return

label r13_v111_child_dark12:
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0039']),'v111:MS14_D12_S05_L0039')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0040']),'v111:MS14_D12_S05_L0040')
    call r13_lines(r13_v111_lines(['MS14_D12_S05_L0041']),'v111:MS14_D12_S05_L0041')
    return

label r13_v111_early12:
    $ r13_fork_set_fate('fate_soup','early')
    $ r13_v111_scene('MS14_D12_B')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','early12',['daram', 'mom'])
    $ r13_v111_arrive(['daram', 'mom', 'nabi', 'resident_teacher', 'karo', 'kid_dodam', 'kid_saemi'])
    $ r13_v111_score()
    $ r13_v111_arrive(['daram', 'mom', 'nabi', 'resident_teacher', 'karo', 'kid_dodam', 'kid_saemi'])
    call r13_lines(r13_v111_lines(['MS14_D12_B_L0002']),'v111:MS14_D12_B_L0002')
    call r13_lines(r13_v111_lines(['MS14_D12_B_L0003']),'v111:MS14_D12_B_L0003')
    call r13_lines(r13_v111_lines(['MS14_D12_B_L0004']),'v111:MS14_D12_B_L0004')
    call r13_lines(r13_v111_lines(['MS14_D12_B_L0005']),'v111:MS14_D12_B_L0005')
    call r13_lines(r13_v111_lines(['MS14_D12_B_L0007']),'v111:MS14_D12_B_L0007')
    call r13_lines(r13_v111_lines(['MS14_D12_B_L0008']),'v111:MS14_D12_B_L0008')
    call r13_lines(r13_v111_lines(['MS14_D12_B_L0010']),'v111:MS14_D12_B_L0010')
    call r13_lines(r13_v111_lines(['MS14_D12_B_L0011']),'v111:MS14_D12_B_L0011')
    call r13_lines(r13_v111_lines(['MS14_D12_B_L0012']),'v111:MS14_D12_B_L0012')
    call r13_lines(r13_v111_lines(['MS14_D12_B_L0013']),'v111:MS14_D12_B_L0013')
    $ r13_v111_set('route12','early_prevented')
    $ r13_v111_set('school_heat_connected',True)
    $ r13_v111_set('busy:karo',False)
    # 2026-10-24 결정 7: 수프 회의가 없는 판. 주머니에 그릇을 든 판에만 돌목이 문간에 선다.
    if r13_v111_value('grand_bowl_pocket') and r13_v111_person_alive('guard') and not r13_v111_value('departed:guard'):
        call r13_v111_early_bowl12
    # 0.20.7 (ending review 8): the prevented path gets its own ordinary evening.
    call r13_lines(r13_nw_block('early_ordinary12'),'nw:early_ordinary12')
    jump r13_v111_sleep12

label r13_v111_sleep12:
    call r13_lines(r13_nw_block('portrait12'),'nw:portrait12')
    $ r13_nw_acquire("NW_HALL_WINDOW")
    if r13_v111_value("piko_alive") is False:
        $ r13_nw_acquire("NW_PIKO_PAINTING")
    jump r13_v111_sleep12_bed

label r13_v111_sleep12_bed:
    call r13_v111_travel('school','sleep12_bed')
    jump r13_v111_sleep12_bed_input

label r13_v111_sleep12_bed_input:
    call r13_v111_wait('sleep12_bed_input')
    if _return==0:
        jump r13_v111_sleep12_bed_done
    jump r13_v111_sleep12_bed_input

label r13_v111_sleep12_bed_done:
    $ r13_v111_set("day",13)
    jump r13_v111_day13

label r13_v111_day13:
    $ r13_v111_scene('MS14_D13_S01')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','day13',['mom', 'daram'])
    $ r13_v111_arrive(['mom', 'daram', 'npc_pandol', 'karo'])
    $ r13_v111_score()
    $ r13_v111_arrive(['mom', 'daram', 'npc_pandol', 'karo'])
    $ r13_v111_set('busy:karo',False)
    if r13_v111_value("piko_alive") is not False:
        $ r13_nw_list("resident_piko","street")
    # 0.20.20 뒤 반응: 12일 같은 냄비로 죽은 꼬미의 빈자리, 12일부터 이어지는 다람의 열.
    if r13_v111_value('kkomi_soup_dead'):
        call r13_lines(r13_nw_block('kkomi_gone13'),'nw:kkomi_gone13')
    if r13_v111_value('daram_fever12') and r13_v111_actor_ready('daram'):
        call r13_lines(r13_nw_block('fever13'),'nw:fever13')
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0002']),'v111:MS14_D13_S01_L0002')
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0003']),'v111:MS14_D13_S01_L0003')
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0004']),'v111:MS14_D13_S01_L0004')
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D13_S01_L0005']),'v111:MS14_D13_S01_L0005')
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0007']),'v111:MS14_D13_S01_L0007')
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0008']),'v111:MS14_D13_S01_L0008')
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0009']),'v111:MS14_D13_S01_L0009')
    # 검토 0.20.4 추가 7: 어제 나비가 한 책 약속을 지킨다(약속을 들은 경로, 나비가 학교에 남은 경우만).
    if r13_v111_value('book_promise12') and r13_v111_value('alive:nabi') is not False and not r13_v111_value('listed:nabi'):
        call r13_lines(r13_nw_block('book_promise13'),'nw:book_promise13')
    jump r13_v111_blanket_mend13

label r13_v111_blanket_mend13:
    call r13_v111_wait('blanket_mend13')
    if _return==80:
        call r13_hp_handoff13
        jump r13_v111_blanket_mend13
    if _return==0:
        jump r13_v111_blanket_mended13
    jump r13_v111_blanket_mend13

label r13_v111_blanket_mended13:
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0011']),'v111:MS14_D13_S01_L0011')
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0012']),'v111:MS14_D13_S01_L0012')
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0013']),'v111:MS14_D13_S01_L0013')
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0014']),'v111:MS14_D13_S01_L0014')
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D13_S01_L0016']),'v111:MS14_D13_S01_L0016')
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0017']),'v111:MS14_D13_S01_L0017')
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0018']),'v111:MS14_D13_S01_L0018')
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0020']),'v111:MS14_D13_S01_L0020')
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0021']),'v111:MS14_D13_S01_L0021')
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0022']),'v111:MS14_D13_S01_L0022')
    call r13_lines(r13_v111_lines(['MS14_D13_S01_L0023']),'v111:MS14_D13_S01_L0023')
    $ r13_v111_set('pandol_blanket_mended',True)
    $ r13_v111_apply('actual_blanket_mending13',[dict(op="acquire",key='E13_MENDING',variant="observed")])
    if r13_v111_value("teacher_custody")=="guard":
        jump r13_v111_teacher_relief13
    jump r13_v111_gate_bench13

label r13_v111_teacher_relief13:
    $ r13_v111_arrive(['mom', 'daram', 'guard', 'resident_teacher', 'v111_patrol'])
    jump r13_v111_teacher_relief_check13

label r13_v111_teacher_relief_check13:
    call r13_v111_wait('teacher_relief_check13')
    if _return==0:
        jump r13_v111_teacher_relief_done13
    jump r13_v111_teacher_relief_check13

label r13_v111_teacher_relief_done13:
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_nw_block('relief_done13'),'nw:relief_done13')
    $ r13_v111_set('busy:v111_patrol','teacher_supervision')
    $ r13_v111_set('teacher_supervisor','v111_patrol')
    $ r13_v111_set('busy:guard',False)
    jump r13_v111_gate_bench13

label r13_v111_gate_bench13:
    $ r13_v111_scene('MS14_D13_S02')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('gate','gate_bench13',['mom', 'daram'])
    $ r13_v111_arrive(['mom', 'daram', 'guard'])
    $ r13_v111_score()
    $ r13_v111_arrive(['mom', 'daram', 'guard'])
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_S02_L0002']),'v111:MS14_D13_S02_L0002')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0003']),'v111:MS14_D13_S02_L0003')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_S02_L0004']),'v111:MS14_D13_S02_L0004')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0005']),'v111:MS14_D13_S02_L0005')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_S02_L0006']),'v111:MS14_D13_S02_L0006')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0007']),'v111:MS14_D13_S02_L0007')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_S02_L0008']),'v111:MS14_D13_S02_L0008')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_S02_L0010']),'v111:MS14_D13_S02_L0010')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0011']),'v111:MS14_D13_S02_L0011')
    call r13_v111_travel('square','cart_arrival13')
    $ r13_v111_arrive(['mom', 'daram', 'npc_pandol', 'resident_ppul', 'neoul', 'karo', 'guard'])
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0013']),'v111:MS14_D13_S02_L0013')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0014']),'v111:MS14_D13_S02_L0014')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0015']),'v111:MS14_D13_S02_L0015')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0017']),'v111:MS14_D13_S02_L0017')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0018']),'v111:MS14_D13_S02_L0018')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0019']),'v111:MS14_D13_S02_L0019')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0020']),'v111:MS14_D13_S02_L0020')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_S02_L0021']),'v111:MS14_D13_S02_L0021')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0022']),'v111:MS14_D13_S02_L0022')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0023']),'v111:MS14_D13_S02_L0023')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0025']),'v111:MS14_D13_S02_L0025')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0026']),'v111:MS14_D13_S02_L0026')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0027']),'v111:MS14_D13_S02_L0027')
    jump r13_v111_offer13

label r13_v111_offer13:
    menu:
        '조건을 더 묻는다':
            jump r13_v111_offer_question13
        '가족 셋이 수락하고 물러난다' if r13_v111_value('family_offer_terms_seen'):
            jump r13_v111_offer_accept13
        '거절하고 현장에 남는다' if r13_v111_value('family_school_place'):
            jump r13_v111_offer_refuse13

label r13_v111_offer_question13:
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0029']),'v111:MS14_D13_S02_L0029')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0030']),'v111:MS14_D13_S02_L0030')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0031']),'v111:MS14_D13_S02_L0031')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_S02_L0032']),'v111:MS14_D13_S02_L0032')
    $ r13_v111_set('family_offer_terms_seen',True)
    jump r13_v111_offer13

label r13_v111_offer_accept13:
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0038']),'v111:MS14_D13_S02_L0038')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0039']),'v111:MS14_D13_S02_L0039')
    $ r13_v111_set('family_deal',True)
    if r13_v111_value("listed:daram"):
        $ r13_v111_set("listed:daram",False)
        $ r13_v111_set("daram_deal_freed",True)
    jump r13_v111_family_exit13

label r13_v111_offer_refuse13:
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0033']),'v111:MS14_D13_S02_L0033')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0034']),'v111:MS14_D13_S02_L0034')
    call r13_lines(r13_v111_lines(['MS14_D13_S02_L0035']),'v111:MS14_D13_S02_L0035')
    $ r13_v111_set('family_deal',False)
    jump r13_v111_blanket_lie13

label r13_v111_blanket_lie13:
    $ r13_v111_scene('MS14_D13_S03')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('square','blanket_lie13',['mom', 'daram'])
    $ r13_v111_arrive(['mom', 'daram', 'npc_pandol', 'resident_ppul', 'guard', 'karo', 'resident_badook'])
    $ r13_v111_score()
    $ r13_v111_arrive(['mom', 'daram', 'npc_pandol', 'resident_ppul', 'guard', 'karo', 'resident_badook'])
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0002']),'v111:MS14_D13_S03_L0002')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0003']),'v111:MS14_D13_S03_L0003')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0004']),'v111:MS14_D13_S03_L0004')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0005']),'v111:MS14_D13_S03_L0005')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0006']),'v111:MS14_D13_S03_L0006')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0007']),'v111:MS14_D13_S03_L0007')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0009']),'v111:MS14_D13_S03_L0009')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0010']),'v111:MS14_D13_S03_L0010')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0011']),'v111:MS14_D13_S03_L0011')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0012']),'v111:MS14_D13_S03_L0012')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0013']),'v111:MS14_D13_S03_L0013')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0015']),'v111:MS14_D13_S03_L0015')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0016']),'v111:MS14_D13_S03_L0016')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0017']),'v111:MS14_D13_S03_L0017')
    jump r13_v111_mending_proof13

label r13_v111_mending_proof13:
    $ r13_meeting_checkpoint("blanket")
    call r13_v111_proof('아내가 봤다는 담요의 시점을 확인한다',['E13_MENDING'],'r13_v111_mending_answer13','r13_v111_mending_wrong13','r13_v111_mending_hint13')
    jump expression _return

label r13_v111_mending_answer13:
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0019']),'v111:MS14_D13_S03_L0019')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0020']),'v111:MS14_D13_S03_L0020')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0021']),'v111:MS14_D13_S03_L0021')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0022']),'v111:MS14_D13_S03_L0022')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0023']),'v111:MS14_D13_S03_L0023')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0024']),'v111:MS14_D13_S03_L0024')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0025']),'v111:MS14_D13_S03_L0025')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0026']),'v111:MS14_D13_S03_L0026')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0027']),'v111:MS14_D13_S03_L0027')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0028']),'v111:MS14_D13_S03_L0028')
    call r13_lines(r13_nw_block('badook_q13'),'nw:badook_q13')
    jump r13_v111_badook_proof13

label r13_v111_badook_proof13:
    call r13_v111_proof('촌장이 어젯밤 있던 곳을 확인한다',['NW_HALL_WINDOW'],'r13_v111_badook_won13','r13_v111_badook_wrong13',None)
    jump expression _return

label r13_v111_badook_wrong13:
    if r13_nw_retry("blanket"):
        call r13_lines(r13_nw_block("badook_q13"),"nw:badook_q13:retry")
        jump r13_v111_badook_proof13
    $ r13_nw_meeting_end("blanket","partial")
    call r13_lines(r13_nw_block('badook_lost13'),'nw:badook_lost13')
    jump r13_v111_mending_rest13

label r13_v111_badook_won13:
    $ r13_nw_meeting_end("blanket","win")
    call r13_lines(r13_nw_block('badook_won13'),'nw:badook_won13')
    jump r13_v111_mending_rest13

label r13_v111_mending_rest13:
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0030']),'v111:MS14_D13_S03_L0030')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0031']),'v111:MS14_D13_S03_L0031')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0032']),'v111:MS14_D13_S03_L0032')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0034']),'v111:MS14_D13_S03_L0034')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0035']),'v111:MS14_D13_S03_L0035')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0036']),'v111:MS14_D13_S03_L0036')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0038']),'v111:MS14_D13_S03_L0038')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0039']),'v111:MS14_D13_S03_L0039')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0040']),'v111:MS14_D13_S03_L0040')
    $ r13_v111_set('false_message_admitted',True)
    jump r13_v111_cart_inspect13

label r13_v111_mending_wrong13:
    if r13_nw_retry("blanket"):
        call r13_lines(r13_v111_lines(["MS14_D13_S03_L0043","MS14_D13_S03_L0044"]),"v111:mending_wrong13:retry")
        jump r13_v111_mending_proof13
    $ r13_nw_meeting_end("blanket","lose")
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0043']),'v111:MS14_D13_S03_L0043')
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0044']),'v111:MS14_D13_S03_L0044')
    call r13_lines(r13_nw_block('blanket_lost13'),'nw:blanket_lost13')
    python:
        _aboard=list(r13_v111_value("cart_roster") or ["npc_pandol","resident_momo","resident_guldol"])
        if r13_v111_value("teacher_transfer")=="listed" and r13_v111_person_alive("resident_teacher"):_aboard.append("resident_teacher")
        if r13_v111_value("silluk_status")=="supervised_compulsory_labor" and r13_v111_person_alive("resident_siluk"):_aboard.append("resident_siluk")
        # 2026-10-24 대승리(수프): 무효 칸으로 실린 사람은 떠나기 전에 내린다(blanket_lost13 의 무효 줄).
        r13_gw_void_down()
        _aboard=[p for p in dict.fromkeys(_aboard+r13_nw_listed()) if not r13_v111_value("handed:"+p)]
        r13_v111_set("departed_names",_aboard)
        for _p in _aboard:r13_v111_set("departed:"+_p,True)
        if "daram" in _aboard:r13_v111_set("location:daram","cart")
    $ r13_v111_set('cart_departed',True)
    $ r13_v111_set('outcome13','partial_rescue')
    jump r13_v111_departed_night13

label r13_v111_departed_night13:
    call r13_v111_travel('school','departed_night13',['mom'])
    $ r13_v111_arrive(['mom', 'nabi'])
    jump r13_v111_departed_bed13

label r13_v111_departed_bed13:
    call r13_v111_wait('departed_bed13')
    if _return==0:
        jump r13_v111_morning14
    jump r13_v111_departed_bed13

label r13_v111_mending_hint13:
    call r13_lines(r13_v111_lines(['MS14_D13_S03_L0045']),'v111:MS14_D13_S03_L0045')
    jump r13_v111_mending_proof13

label r13_v111_cart_inspect13:
    call r13_v111_wait('cart_inspect13')
    if _return==0:
        jump r13_v111_cart_observed13
    jump r13_v111_cart_inspect13

label r13_v111_cart_observed13:
    $ r13_v111_set('cart_roster',['npc_pandol', 'resident_momo', 'resident_guldol'])
    call r13_lines(r13_nw_block('cart_names13'),'nw:cart_names13')
    if r13_v111_value("listed:resident_piko"):
        $ r13_nw_acquire("NW_PIKO_PAINTING","told")
    if r13_v111_value("silluk_status")=="supervised_compulsory_labor" and r13_v111_person_alive("resident_siluk"):
        call r13_v111_silluk_board_observation13
    if r13_v111_value("teacher_transfer")=="listed" and r13_v111_person_alive("resident_teacher"):
        call r13_v111_teacher_board_observation13
    jump r13_v111_stop_cart13

label r13_v111_teacher_board_observation13:
    $ r13_v111_set('location:resident_teacher','square')
    call r13_lines([(None,"사자 선생님이 출석부를 품에 안고 앉아 있었다.",{"show":"resident_teacher","pose":"collapse_attendance"})],"v111:teacher_actual_cart_observation")
    $ r13_v111_set("teacher_transfer","aboard")
    $ r13_v111_set("cart_roster",r13_v111_value("cart_roster")+["resident_teacher"])
    return

label r13_v111_silluk_board_observation13:
    $ r13_v111_set('location:resident_siluk','square')
    call r13_lines([(None,"짐칸 끝에 실룩. 고개를 숙이고 있었다.")],"v111:silluk_actual_cart_observation")
    $ r13_v111_set("silluk_transfer","aboard")
    $ r13_v111_set("cart_roster",r13_v111_value("cart_roster")+["resident_siluk"])
    return

label r13_v111_stop_cart13:
    $ r13_v111_scene('MS14_D13_S04')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('square','stop_cart13',['mom', 'daram'])
    $ r13_v111_arrive(['mom', 'daram', 'karo', 'guard', 'resident_badook', 'npc_pandol', 'resident_momo', 'resident_guldol', 'resident_ppul', 'neoul'])
    $ r13_v111_score()
    $ r13_v111_arrive(['mom', 'daram', 'karo', 'guard', 'resident_badook', 'npc_pandol', 'resident_momo', 'resident_guldol', 'resident_ppul', 'neoul'])
    $ room13["v111"]["music_hold"]=room13["v111"]["scene"]
    $ renpy.music.stop(fadeout=.15)
    if r13_v111_actor_ready('resident_badook'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0002']),'v111:MS14_D13_S04_L0002')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0003']),'v111:MS14_D13_S04_L0003')
    if r13_v111_actor_ready('resident_badook'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0004']),'v111:MS14_D13_S04_L0004')
    $ r13_v111_set('cart_stopped',True)
    $ r13_v111_set('stop_actor','resident_badook')
    # 2026-10-24 대승리(수프): 이송 예정 칸이 무효면 그 칸으로 실린 사람이 모두 이 자리에서 내린다.
    call r13_v111_listed_void13
    # Audit d11-14 #7: listed Daram is untied as soon as the cart stops.
    if r13_v111_value("listed:daram") and not r13_v111_value("handed:daram"):
        call r13_lines(r13_nw_block('listed_down_daram13'),'nw:listed_down_daram13:stop')
        $ r13_v111_set("handed:daram",True)
    $ r13_v111_set('busy:resident_badook','stop_cart')
    $ r13_v111_set("cart_roster",r13_v111_value("cart_roster") or ["npc_pandol","resident_momo","resident_guldol"])
    jump r13_v111_rein13

label r13_v111_rein13:
    # Audit d11-14 #14: Silluk speaks in this meeting, so he stands in the scene.
    $ r13_v111_arrive(['mom', 'daram', 'karo', 'guard', 'resident_badook', 'npc_pandol', 'resident_momo', 'resident_guldol', 'resident_ppul', 'neoul', 'resident_siluk'])
    call r13_lines(r13_nw_block('rein_open13'),'nw:rein_open13')
    jump r13_v111_rein_ledger13p

label r13_v111_rein_ledger13p:
    $ r13_meeting_checkpoint("piko")
    if not r13_v111_value("roster_shown13"):
        $ r13_v111_set("roster_shown13",True)
        call r13_lines(r13_nw_roster_lines(),'nw:roster13')
    if r13_v111_value('lamp_bound2'):
        call r13_v111_proof('인수하지 않은 돌의 약속 값을 보인다',['NW_LA_OFFER'],'r13_v111_rein_ledger13','r13_v111_rein_wrong13a',None)
    else:
        call r13_v111_proof('장부의 두 배를 실룩에게 보인다',['E16'],'r13_v111_rein_ledger13','r13_v111_rein_wrong13a',None)
    jump expression _return

label r13_v111_rein_ledger13:
    call r13_lines(r13_nw_block('rein_ledger13'),'nw:rein_ledger13')
    jump r13_v111_rein_painting13p

label r13_v111_rein_painting13p:
    call r13_v111_proof('피코가 막혀야 했던 까닭을 보인다',['NW_PIKO_PAINTING'],'r13_v111_rein_won13','r13_v111_rein_wrong13b',None)
    jump expression _return

label r13_v111_rein_won13:
    $ r13_nw_meeting_end("piko","win")
    call r13_lines(r13_nw_block('rein_won13'),'nw:rein_won13')
    $ r13_v111_set('neoul_held',True)
    $ r13_nw_acquire("NW_NEOUL_LEDGER","full" if r13_v111_value("meeting:hypothesis")=="win" else "some" if r13_v111_value("meeting:hypothesis")=="partial" else "observed")
    jump r13_v111_after_rein13

label r13_v111_rein_wrong13a:
    if r13_nw_retry("piko"):
        call r13_lines(r13_nw_block("rein_retry13"),"nw:rein_retry13")
        jump r13_v111_rein_ledger13p
    jump r13_v111_rein_wrong13

label r13_v111_rein_wrong13b:
    if r13_nw_retry("piko"):
        call r13_lines(r13_nw_block("rein_retry13"),"nw:rein_retry13")
        jump r13_v111_rein_painting13p
    jump r13_v111_rein_wrong13

label r13_v111_rein_wrong13:
    $ r13_nw_meeting_end("piko","lose")
    call r13_lines(r13_nw_block('rein_lost13'),'nw:rein_lost13')
    jump r13_v111_after_rein13

label r13_v111_after_rein13:
    if r13_v111_value("meeting:blanket")=="partial":
        jump r13_v111_partial_listed13
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0011']),'v111:MS14_D13_S04_L0011')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0012']),'v111:MS14_D13_S04_L0012')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0013']),'v111:MS14_D13_S04_L0013')
    if r13_v111_actor_ready('resident_badook'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0014']),'v111:MS14_D13_S04_L0014')
    jump r13_v111_family_position13

label r13_v111_partial_listed13:
    python:
        _left=[p for p in r13_nw_listed() if p!="daram" and r13_v111_person_alive(p) and not r13_v111_value("handed:"+p)]
        r13_v111_set("cart_roster",list(dict.fromkeys(list(r13_v111_value("cart_roster") or ["npc_pandol","resident_momo","resident_guldol"])+_left)))
    if r13_v111_value("listed:daram") and not r13_v111_value("handed:daram"):
        call r13_lines(r13_nw_block('listed_down_daram13'),'nw:listed_down_daram13')
        $ r13_v111_set("handed:daram",True)
    jump r13_v111_partial13

label r13_v111_family_position13:
    menu:
        '엄마와 다람이 곁에 남게 한다':
            jump r13_v111_family_stay13
        '엄마와 다람을 까로와 학교로 보낸다' if not r13_v111_value('busy:karo'):
            jump r13_v111_family_karo13
        '엄마와 다람을 네로와 학교로 보낸다' if r13_v111_value('nero_alive') and not r13_v111_value('busy:resident_nero') and r13_v111_actor_ready("resident_nero"):
            jump r13_v111_family_nero13

label r13_v111_family_stay13:
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0063']),'v111:MS14_D13_S04_L0063')
    if r13_v111_actor_ready('mom') and room13['location']=='square':
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0064']),'v111:MS14_D13_S04_L0064')
    $ r13_v111_set('family_location','square')
    # 검토 0.20.4 기록 3: 관계도가 12일 값(DARAM_location)이 아니라 지금 있는 곳을 읽게 한다.
    $ r13_v111_set('location:daram','square')
    $ r13_v111_set('busy:mom','daram_guard')
    jump r13_v111_handover_plan13

label r13_v111_family_karo13:
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0056']),'v111:MS14_D13_S04_L0056')
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0057']),'v111:MS14_D13_S04_L0057')
    if r13_v111_actor_ready('daram') and room13['location']=='square':
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0058']),'v111:MS14_D13_S04_L0058')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0059']),'v111:MS14_D13_S04_L0059')
    $ r13_v111_set('family_location','moving_to_school')
    $ r13_v111_set('location:mom','on_way_school')
    $ r13_v111_set('location:daram','on_way_school')
    $ r13_v111_set('location:karo','on_way_school')
    $ r13_v111_set('busy:karo','family_walk')
    jump r13_v111_family_walk_karo13

label r13_v111_family_nero13:
    $ r13_v111_arrive(['mom', 'daram', 'resident_nero', 'karo', 'guard', 'resident_badook'])
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0060']),'v111:MS14_D13_S04_L0060')
    if r13_v111_actor_ready('resident_nero'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0061']),'v111:MS14_D13_S04_L0061')
    if r13_v111_actor_ready('mom') and room13['location']=='square':
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0062']),'v111:MS14_D13_S04_L0062')
    hide r13_visitor
    $ renpy.pause(.35)
    $ r13_v111_set('family_location','school')
    $ r13_v111_set('location:mom','school')
    $ r13_v111_set('location:daram','school')
    $ r13_v111_set('location:resident_nero','school')
    $ r13_v111_set('busy:mom','daram_guard')
    $ r13_v111_set('busy:resident_nero','daram_guard')
    $ r13_v111_arrive(['karo', 'guard', 'resident_badook'])
    jump r13_v111_handover_plan13

label r13_v111_family_walk_karo13:
    hide r13_visitor
    $ renpy.pause(.35)
    $ r13_v111_set('location:mom','school')
    $ r13_v111_set('location:daram','school')
    $ r13_v111_set('busy:mom','daram_guard')
    $ r13_v111_set('family_location','school')
    $ r13_v111_set('busy:karo',False)
    $ r13_v111_arrive(['karo', 'guard', 'resident_badook'])
    call r13_lines([(None,"잠시 뒤, 까로가 혼자 광장으로 돌아왔다.",{"show":"karo","no_lead":True})],"v111:family_escort_return13")
    # 0.20.9 (구체 수정안 6): 내부의 도착 반영을 아빠가 들은 정보로 만든다.
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_nw_block('karo_report13'),'nw:karo_report13')
    jump r13_v111_handover_plan13

label r13_v111_handover_plan13:
    if room13["v111"].get("scene")!="MS14_D13_S04":
        $ r13_v111_scene("MS14_D13_S04")
        $ room13["v111"]["music_hold"]="MS14_D13_S04"
        $ renpy.music.stop(fadeout=.15)
        $ r13_v111_score()
    # 2026-10-24 행동 검수 13-10: 「기다린다」를 고르면 그날이 끝난다는 것을 고르기 전에 한 번 들려준다.
    if not r13_has("v111:shown:handover_wait13"):
        $ r13_flag("v111:shown:handover_wait13")
        call r13_lines(r13_nw_block('handover_wait13'),'nw:handover_wait13')
    menu:
        '학교 침상과 인수를 먼저 확인한다':
            jump r13_v111_school_handover_prep13
        '하차한 사람부터 부축한다' if r13_v111_value('handover_prepared13'):
            jump r13_v111_pandol_down13
        '보온·감독 아래 인계를 기다린다':
            jump r13_v111_partial13
        '검증한 기록을 공개한다' if r13_v111_value('false_message_admitted') and not r13_v111_value('crowd_resolution_done'):
            jump r13_v111_crowd_prepare13

label r13_v111_school_handover_prep13:
    # Review 0.20.1 4-3: a listed Nabi gets off the cart before she works the school handover.
    if r13_v111_value('listed:nabi') is True and not r13_v111_value('handed:nabi'):
        $ r13_v111_arrive(['guard', 'karo', 'nabi'])
        call r13_lines(r13_nw_block('nabi_down13'),'nw:nabi_down13')
        $ r13_v111_set('handed:nabi',True)
    call r13_v111_travel('school','handover_prep13')
    $ r13_v111_arrive(['nabi', 'karo'])
    jump r13_v111_nabi_beds13

label r13_v111_nabi_beds13:
    call r13_v111_wait('nabi_beds13')
    if _return==0:
        jump r13_v111_beds_ready13
    jump r13_v111_nabi_beds13

label r13_v111_beds_ready13:
    if r13_v111_actor_ready('nabi'):
        call r13_lines(r13_nw_block('beds_ready13'),'nw:beds_ready13')
    $ r13_v111_set('handover_prepared13',True)
    $ r13_v111_set('busy:karo',False)
    call r13_v111_travel('square','beds_ready13')
    $ r13_v111_arrive(['guard', 'karo', 'resident_badook'])
    jump r13_v111_handover_plan13

label r13_v111_pandol_down13:
    $ r13_v111_arrive(['guard', 'karo', 'resident_badook', 'npc_pandol'])
    if r13_v111_value("family_location")=="square":
        $ r13_v111_arrive(["guard","karo","resident_badook","npc_pandol","mom","daram"])
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0016']),'v111:MS14_D13_S04_L0016')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0017']),'v111:MS14_D13_S04_L0017')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0018']),'v111:MS14_D13_S04_L0018')
    call r13_v111_travel('school','pandol_school13')
    $ r13_v111_arrive(['nabi', 'karo', 'npc_pandol'])
    if r13_v111_actor_ready('nabi') and room13['location']=='school':
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0021']),'v111:MS14_D13_S04_L0021')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0022']),'v111:MS14_D13_S04_L0022')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0023']),'v111:MS14_D13_S04_L0023')
    $ r13_v111_set('handed:npc_pandol',True)
    $ r13_v111_apply('pandol_actual_school_handover',[dict(op="acquire",key='E13_HANDOVER',variant="observed")])
    jump r13_v111_momo_transport13

label r13_v111_momo_transport13:
    call r13_v111_travel('square','momo_transport13')
    $ r13_v111_arrive(['karo', 'guard', 'resident_badook', 'resident_momo'])
    jump r13_v111_momo_down13

label r13_v111_momo_down13:
    call r13_v111_wait('momo_down13')
    if _return==0:
        jump r13_v111_momo_school13
    jump r13_v111_momo_down13

label r13_v111_momo_school13:
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0065']),'v111:MS14_D13_S04_L0065')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0066']),'v111:MS14_D13_S04_L0066')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0067']),'v111:MS14_D13_S04_L0067')
    # 후반 기획서 B: 첫 왕복(침상·판돌)은 지도 이동 그대로, 같은 길을 되풀이하는 모모·굴돌은 이어서 간다.
    call r13_lines(r13_nw_block('momo_walk13'),'nw:momo_walk13')
    $ r13_v111_time("move:travel:school",5)
    call r13_v111_travel('school','momo_school13',direct=True)
    $ r13_v111_arrive(['nabi', 'karo', 'resident_momo'])
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0068']),'v111:MS14_D13_S04_L0068')
    $ r13_v111_set('handed:resident_momo',True)
    jump r13_v111_guldol_transport13

label r13_v111_guldol_transport13:
    call r13_lines(r13_nw_block('back_square13'),'nw:back_square13')
    $ r13_v111_time("move:travel:square",5)
    call r13_v111_travel('square','guldol_transport13',direct=True)
    $ r13_v111_arrive(['karo', 'guard', 'resident_badook', 'resident_guldol'])
    jump r13_v111_guldol_down13

label r13_v111_guldol_down13:
    call r13_v111_wait('guldol_down13')
    if _return==0:
        jump r13_v111_guldol_school13
    jump r13_v111_guldol_down13

label r13_v111_guldol_school13:
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0069']),'v111:MS14_D13_S04_L0069')
    if r13_v111_actor_ready('resident_guldol'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0070']),'v111:MS14_D13_S04_L0070')
    call r13_lines(r13_nw_block('guldol_walk13'),'nw:guldol_walk13')
    $ r13_v111_time("move:travel:school",5)
    call r13_v111_travel('school','guldol_school13',direct=True)
    $ r13_v111_arrive(['nabi', 'karo', 'resident_guldol'])
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0071']),'v111:MS14_D13_S04_L0071')
    $ r13_v111_set('handed:resident_guldol',True)
    jump r13_v111_last_cart13

label r13_v111_last_cart13:
    call r13_lines(r13_nw_block('back_square13'),'nw:back_square13')
    $ r13_v111_time("move:travel:square",5)
    call r13_v111_travel('square','last_cart13',[],direct=True)
    $ r13_v111_arrive(['karo', 'resident_badook', 'resident_ppul'])
    if "resident_teacher" in r13_v111_value("cart_roster") and not r13_v111_value("handed:resident_teacher"):
        jump r13_v111_teacher_transport13
    if "resident_siluk" in r13_v111_value("cart_roster") and not r13_v111_value("handed:resident_siluk"):
        jump r13_v111_silluk_transport13
    if r13_v111_value("family_location")=="square":
        call r13_v111_family_still_here13
    else:
        call r13_v111_family_already_school13
    if not all(r13_v111_value("handed:"+p) for p in r13_v111_value("cart_roster")):
        jump r13_v111_partial_listed13
    call r13_lines(r13_nw_block('listed_down13'),'nw:listed_down13')
    python:
        for _p in r13_nw_listed():r13_v111_set("handed:"+_p,True)
    $ room13["v111"]["music_hold"]=None
    $ room13["v111"]["music_override"]={'scene': 'MS14_D13_S04', 'path': 'assets/bgm-village.mp3'}
    $ renpy.music.play('assets/bgm-village.mp3',fadein=1.0,relative_volume=.28)
    if r13_v111_actor_ready('resident_badook'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0040']),'v111:MS14_D13_S04_L0040')
    $ r13_v111_set('all_cart_handed',True)
    $ r13_v111_set('busy:resident_badook',False)
    $ r13_v111_set('outcome13','all_rescued')
    jump r13_v111_transport_cleanup13

label r13_v111_family_still_here13:
    $ r13_v111_arrive(['karo', 'resident_badook', 'resident_ppul', 'mom', 'daram'])
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0034']),'v111:MS14_D13_S04_L0034')
    if r13_v111_actor_ready('mom') and room13['location']=='square':
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0035']),'v111:MS14_D13_S04_L0035')
    return

label r13_v111_family_already_school13:
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0037']),'v111:MS14_D13_S04_L0037')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0088']),'v111:MS14_D13_S04_L0088')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0038']),'v111:MS14_D13_S04_L0038')
    return

label r13_v111_teacher_transport13:
    $ r13_v111_arrive(['karo', 'guard', 'resident_badook', 'resident_teacher', 'neoul'])
    jump r13_v111_teacher_down13

label r13_v111_teacher_down13:
    call r13_v111_wait('teacher_down13')
    if _return==0:
        jump r13_v111_teacher_supervised13
    jump r13_v111_teacher_down13

label r13_v111_teacher_supervised13:
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0072']),'v111:MS14_D13_S04_L0072')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0073']),'v111:MS14_D13_S04_L0073')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0074']),'v111:MS14_D13_S04_L0074')
    call r13_v111_travel('v111_supervised','teacher_supervised13',[])
    $ r13_v111_arrive(['karo', 'resident_teacher', 'neoul'])
    jump r13_v111_teacher_receipt13

label r13_v111_teacher_receipt13:
    call r13_v111_wait('teacher_receipt13')
    if _return==0:
        jump r13_v111_teacher_received13
    jump r13_v111_teacher_receipt13

label r13_v111_teacher_received13:
    $ r13_v111_set('handed:resident_teacher',True)
    $ r13_v111_set('teacher_transfer','handed_over')
    $ r13_v111_set('busy:neoul','teacher_supervision')
    jump r13_v111_last_cart13

label r13_v111_silluk_transport13:
    $ r13_v111_arrive(['karo', 'guard', 'resident_badook', 'resident_siluk'])
    jump r13_v111_silluk_supervision13

label r13_v111_silluk_supervision13:
    call r13_v111_wait('silluk_supervision13')
    if _return==0:
        jump r13_v111_silluk_down13
    jump r13_v111_silluk_supervision13

label r13_v111_silluk_down13:
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0008']),'v111:MS14_D13_S04_L0008')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0009']),'v111:MS14_D13_S04_L0009')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0025']),'v111:MS14_D13_S04_L0025')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0026']),'v111:MS14_D13_S04_L0026')
    if r13_v111_value("family_location")=="square":
        call r13_v111_silluk_family13
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0030']),'v111:MS14_D13_S04_L0030')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0031']),'v111:MS14_D13_S04_L0031')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0032']),'v111:MS14_D13_S04_L0032')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0075']),'v111:MS14_D13_S04_L0075')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0076']),'v111:MS14_D13_S04_L0076')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0077']),'v111:MS14_D13_S04_L0077')
    call r13_v111_travel('v111_labor','silluk_down13',[])
    $ r13_v111_arrive(['karo', 'guard', 'resident_siluk'])
    jump r13_v111_silluk_receipt13

label r13_v111_silluk_family13:
    $ r13_v111_arrive(['karo', 'guard', 'resident_badook', 'resident_siluk', 'mom', 'daram'])
    if r13_v111_actor_ready('daram') and room13['location']=='square':
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0028']),'v111:MS14_D13_S04_L0028')
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0029']),'v111:MS14_D13_S04_L0029')
    return

label r13_v111_silluk_receipt13:
    call r13_v111_wait('silluk_receipt13')
    if _return==0:
        jump r13_v111_silluk_received13
    jump r13_v111_silluk_receipt13

label r13_v111_silluk_received13:
    $ r13_v111_set('handed:resident_siluk',True)
    $ r13_v111_set('silluk_transfer','handed_over')
    $ r13_v111_set('busy:guard','silluk_supervision')
    jump r13_v111_last_cart13

label r13_v111_transport_cleanup13:
    call r13_v111_wait('transport_cleanup13')
    if _return==0:
        jump r13_v111_escort_refuse13
    if _return==1:
        jump r13_v111_order_stop13
    if _return==2:
        jump r13_v111_driver_refuse13
    if _return==3:
        jump r13_v111_cart_return13
    if _return==4:
        jump r13_v111_relay_stop13
    if _return==5:
        jump r13_v111_night_finish13
    if _return==6:
        jump r13_v111_buri_tools13
    jump r13_v111_transport_cleanup13

label r13_v111_escort_refuse13:
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0044']),'v111:MS14_D13_S04_L0044')
    if r13_v111_actor_ready('resident_badook'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0045']),'v111:MS14_D13_S04_L0045')
    $ r13_v111_set('actual_stop_actor_refuses_transport',True)
    jump r13_v111_transport_cleanup13

label r13_v111_order_stop13:
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0080']),'v111:MS14_D13_S04_L0080')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0081']),'v111:MS14_D13_S04_L0081')
        $ r13_v111_commit('MS14_D13_S04_L0081')
    $ r13_v111_set('current_order_execution_stopped',True)
    $ r13_v111_apply('actual_stopped_order13',[dict(op="acquire",key='E13_ORDER',variant="observed")])
    # 0.20.12 (후반 기획서 C안): 명령 중지와 사본 전달을 한 번의 대화로 잇는다.
    call r13_lines(r13_nw_block('order_relay_next13'),'nw:order_relay_next13')
    jump r13_v111_relay_stop13

label r13_v111_driver_refuse13:
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0082']),'v111:MS14_D13_S04_L0082')
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0083']),'v111:MS14_D13_S04_L0083')
        $ r13_v111_commit('MS14_D13_S04_L0083')
    $ r13_v111_set('Kkaro_forced_transport_refused',True)
    # 0.20.12 (후반 기획서 C안): 운반 거부와 빈 수레 반환을 한 번의 대화로 잇는다.
    call r13_lines(r13_nw_block('karo_cart_next13'),'nw:karo_cart_next13')
    jump r13_v111_cart_return13

label r13_v111_cart_return13:
    $ r13_v111_arrive(['karo', 'guard', 'resident_badook', 'resident_eunho'])
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0084']),'v111:MS14_D13_S04_L0084')
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0085']),'v111:MS14_D13_S04_L0085')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_S04_L0086']),'v111:MS14_D13_S04_L0086')
    $ r13_v111_set('cart_returned',True)
    $ r13_v111_set('escort_gear_returned',True)
    jump r13_v111_transport_cleanup13

label r13_v111_relay_stop13:
    if r13_v111_value("busy:neoul")=="teacher_supervision":
        jump r13_v111_relay_supervised13
    $ r13_v111_arrive(['neoul', 'guard'])
    jump r13_v111_relay_present13

label r13_v111_relay_supervised13:
    call r13_v111_travel('v111_supervised','relay_supervised13',[])
    $ r13_v111_arrive(['neoul', 'resident_teacher'])
    jump r13_v111_relay_present13

label r13_v111_relay_present13:
    call screen r13_book("neoul",present=True)
    if _return=="V111:E13_ORDER" and r13_v111_owned("E13_ORDER"):
        jump r13_v111_relay_confirmed13
    if _return:
        $ renpy.notify("중지 명령 사본을 직접 보여 줘야 한다.")
    jump r13_v111_transport_cleanup13

label r13_v111_relay_confirmed13:
    $ r13_v111_set('relay_stopped',True)
    jump r13_v111_transport_cleanup13

label r13_v111_buri_tools13:
    $ r13_v111_arrive(['buri'])
    # 2026-10-24 행동 검수 13-13: 「고정부」를 아직 모르므로, 아빠가 짐작을 말하고 부리가 받는다.
    call r13_lines(r13_nw_block('buri_tools13'),'nw:buri_tools13')
    call r13_lines([(None,"부리가 공구와 받침을 챙겼다. 내일 현장에 함께 가겠다고 했다.")],"v111:buri_tools_consent13")
    $ r13_v111_set('buri_device_consent',True)
    jump r13_v111_transport_cleanup13

label r13_v111_night_finish13:
    $ r13_v111_set("current_transport_chain_stopped",all(r13_v111_value(k) for k in ["actual_stop_actor_refuses_transport","current_order_execution_stopped","Kkaro_forced_transport_refused","cart_returned","escort_gear_returned","relay_stopped"]))
    jump r13_v111_sleep13

label r13_v111_family_exit13:
    $ r13_v111_scene('MS14_D13_A')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('square','family_exit13',['mom', 'daram'])
    $ r13_v111_arrive(['mom', 'daram', 'guard', 'karo'])
    $ r13_v111_score()
    $ r13_v111_arrive(['mom', 'daram', 'guard', 'karo'])
    call r13_lines(r13_v111_lines(['MS14_D13_A_L0002']),'v111:MS14_D13_A_L0002')
    call r13_lines(r13_v111_lines(['MS14_D13_A_L0003']),'v111:MS14_D13_A_L0003')
    call r13_lines(r13_v111_lines(['MS14_D13_A_L0005']),'v111:MS14_D13_A_L0005')
    call r13_lines(r13_v111_lines(['MS14_D13_A_L0006']),'v111:MS14_D13_A_L0006')
    call r13_lines(r13_v111_lines(['MS14_D13_A_L0007']),'v111:MS14_D13_A_L0007')
    call r13_lines(r13_v111_lines(['MS14_D13_A_L0008']),'v111:MS14_D13_A_L0008')
    call r13_v111_travel('gate','family_gate13')
    $ r13_v111_arrive(['mom', 'daram', 'guard', 'karo'])
    call r13_lines(r13_v111_lines(['MS14_D13_A_L0010']),'v111:MS14_D13_A_L0010')
    call r13_lines(r13_v111_lines(['MS14_D13_A_L0011']),'v111:MS14_D13_A_L0011')
    call r13_lines(r13_v111_lines(['MS14_D13_A_L0012']),'v111:MS14_D13_A_L0012')
    call r13_lines(r13_v111_lines(['MS14_D13_A_L0014']),'v111:MS14_D13_A_L0014')
    call r13_lines(r13_v111_lines(['MS14_D13_A_L0015']),'v111:MS14_D13_A_L0015')
    call r13_lines(r13_v111_lines(['MS14_D13_A_L0016']),'v111:MS14_D13_A_L0016')
    call r13_lines(r13_v111_lines(['MS14_D13_A_L0018']),'v111:MS14_D13_A_L0018')
    $ r13_v111_set('family_benefits_received',True)
    $ r13_v111_set('night14_lodging','gate')
    $ r13_v111_set('outcome13','family_priority')
    $ r13_v111_set('departed_unrescued',True)
    jump r13_v111_sleep13

label r13_v111_partial13:
    $ r13_v111_scene('MS14_D13_B')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('square','partial13',[])
    $ r13_v111_arrive(['karo', 'guard', 'resident_badook'])
    $ r13_v111_score()
    $ r13_v111_arrive(['karo', 'guard', 'resident_badook'])
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D13_B_L0002']),'v111:MS14_D13_B_L0002')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_B_L0003']),'v111:MS14_D13_B_L0003')
    call r13_lines(r13_v111_lines(['MS14_D13_B_L0004']),'v111:MS14_D13_B_L0004')
    call r13_lines(r13_v111_lines(['MS14_D13_B_L0005']),'v111:MS14_D13_B_L0005')
    if r13_v111_actor_ready('resident_badook'):
        call r13_lines(r13_v111_lines(['MS14_D13_B_L0006']),'v111:MS14_D13_B_L0006')
    call r13_lines(r13_v111_lines(['MS14_D13_B_L0008']),'v111:MS14_D13_B_L0008')
    call r13_lines(r13_v111_lines(['MS14_D13_B_L0009']),'v111:MS14_D13_B_L0009')
    $ r13_v111_set('outcome13','partial_rescue')
    $ r13_v111_set('cart_stopped',True)
    $ r13_v111_set('pending_handover_supervised',True)
    jump r13_v111_sleep13

label r13_v111_crowd_prepare13:
    $ r13_v111_set('crowd_preparation_schema13',True)
    call r13_v111_travel('square','crowd_prepare13',[],True)
    $ r13_v111_arrive(['karo','resident_badook','neoul']+(['guard'] if r13_crowd_guard_available13(True) else []))
label r13_v111_crowd_prepare_wait13:
    call r13_v111_wait('crowd_prepare13')
    if _return==0:
        call r13_lines(r13_nw_block('crowd_space_records13'),'nw:crowd_space_records13')
        $ r13_v111_set('crowd_records_spaced13',True)
    elif _return==1:
        call r13_lines(r13_nw_block('crowd_space_cart13'),'nw:crowd_space_cart13')
        $ r13_v111_set('crowd_cart_spaced13',True)
    elif _return==2 and r13_crowd_guard_available13():
        call r13_lines(r13_nw_block('crowd_place_guard13'),'nw:crowd_place_guard13')
        $ r13_v111_set('busy:guard','crowd_supervision')
        $ r13_v111_set('location:guard','square')
        $ r13_v111_set('crowd_supervisor_placed13',True)
        $ r13_v111_talk_person=None
    elif _return==3:
        jump r13_v111_crowd13
    elif _return==4:
        $ r13_crowd_release13()
        jump r13_v111_handover_plan13
    jump r13_v111_crowd_prepare_wait13

label r13_v111_crowd13:
    $ r13_v111_scene('MS14_D13_C')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('square','crowd13',[])
    $ r13_v111_arrive(['karo', 'resident_badook', 'neoul']+(['guard'] if not r13_v111_value('crowd_preparation_schema13') or r13_crowd_guard_available13(True) else []))
    $ r13_v111_score()
    $ r13_v111_arrive(['karo', 'resident_badook', 'neoul']+(['guard'] if not r13_v111_value('crowd_preparation_schema13') or r13_crowd_guard_available13(True) else []))
    call r13_lines(r13_v111_lines(['MS14_D13_C_L0002']),'v111:MS14_D13_C_L0002')
    call r13_lines(r13_v111_lines(['MS14_D13_C_L0003']),'v111:MS14_D13_C_L0003')
    if r13_v111_value('family_location')=='square':
        call r13_v111_daram_crowd13
    # 2026-10-24 대승리(불, GRAND_WIN_DESIGN.md 1-5): 7일 회의에 배급표가 적힌 판에서는 누비가 먼저 나선다.
    if r13_v111_value('neoul_promise_proven') and r13_v111_person_alive('resident_nubi') and r13_v111_person_alive('neoul'):
        $ r13_v111_join(['resident_nubi'])
        call r13_lines(r13_nw_block('crowd_record13'),'nw:crowd_record13')
    # New runs settle from the actual pre-publication state. Saved old menus remain below.
    if r13_v111_value('crowd_preparation_schema13'):
        if r13_v111_value('neoul_promise_proven') and r13_v111_person_alive('resident_nubi') and r13_v111_person_alive('neoul'):
            jump r13_v111_crowd_record13
        if r13_crowd_prepared13():
            jump r13_v111_crowd_guard13
        jump r13_v111_crowd_watch13

label r13_v111_crowd_legacy_menu13:
    # 2026-10-24 행동 검수 13-11: 메뉴 글이 두 뜻으로 읽혔다(「너울 앞을 막는다」=달아나는 길을 막는다?,
    # 「막지 않는다」=무엇을?, 「현장 감독자」=이 장면에서 불린 적 없는 말). 같은 갈래를 뜻이 하나로 읽히게 쓴다.
    menu:
        '7일 회의 기록을 함께 읽는다' if r13_v111_value('neoul_promise_proven') and r13_v111_person_alive('resident_nubi') and r13_v111_person_alive('neoul'):
            jump r13_v111_crowd_record13
        '너울을 몸으로 감싼다':
            jump r13_v111_crowd_block13
        '돌목에게 너울을 맡긴다' if not r13_v111_value('busy:guard'):
            jump r13_v111_crowd_guard13
        '주민들을 말리지 않는다':
            jump r13_v111_crowd_watch13

label r13_v111_daram_crowd13:
    $ r13_v111_arrive(['mom', 'daram', 'karo', 'neoul', 'resident_badook']+(['guard'] if not r13_v111_value('crowd_preparation_schema13') or r13_crowd_guard_available13(True) else []))
    if r13_v111_actor_ready('daram') and room13['location']=='square':
        call r13_lines(r13_v111_lines(['MS14_D13_C_L0006']),'v111:MS14_D13_C_L0006')
        $ r13_v111_set('crowd_witnessed',True)
    return

label r13_v111_crowd_block13:
    $ r13_fork_set_fate('fate_crowd','block')
    call r13_lines(r13_v111_lines(['MS14_D13_C_L0009']),'v111:MS14_D13_C_L0009')
    call r13_lines(r13_v111_lines(['MS14_D13_C_L0010']),'v111:MS14_D13_C_L0010')
    call r13_lines(r13_v111_lines(['MS14_D13_C_L0011']),'v111:MS14_D13_C_L0011')
    # 0.20.18 (소유자 2026-10-23 "권선징악으로 유도하면 안 돼", CRUEL_CHOICES.md C1): 원수를 몸으로 감싸도
    # 아무도 구하지 못한다. 군중이 아빠 쪽으로 쏠리고 너울은 그 틈에 빠져나간다. 막는 길은 비어 있는 감독자뿐이다.
    call r13_lines(r13_nw_block('crowd_block_fail13'),'nw:crowd_block_fail13')
    $ r13_v111_set('crowd_blocked_by_dad',True)
    $ r13_v111_set('alive:neoul',False)
    $ r13_v111_set('crowd_resolution_done',True)
    $ r13_v111_set('crowd_injury',True)
    $ r13_v111_set('crowd_intervention','failed')
    $ r13_v111_set('outcome13','crowd_violence')
    jump r13_v111_sleep13

# 0.20.18 이전의 「너울 앞을 막는다」 성공 줄. 새 판은 지나지 않는다(옛 저장용).
label r13_v111_crowd_block_old13:
    call r13_lines(r13_v111_lines(['MS14_D13_C_L0009']),'v111:MS14_D13_C_L0009')
    if r13_v111_actor_ready('daram') and room13['location']=='square':
        call r13_lines(r13_v111_lines(['MS14_D13_C_L0013']),'v111:MS14_D13_C_L0013')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_C_L0014']),'v111:MS14_D13_C_L0014')
    call r13_lines(r13_v111_lines(['MS14_D13_C_L0015']),'v111:MS14_D13_C_L0015')
    call r13_lines(r13_v111_lines(['MS14_D13_C_L0016']),'v111:MS14_D13_C_L0016')
    $ r13_v111_set('crowd_resolution_done',True)
    $ r13_v111_set('crowd_injury',False)
    $ r13_v111_set('crowd_intervention','success')
    $ r13_v111_set('outcome13','all_rescued')
    jump r13_v111_handover_plan13

label r13_v111_crowd_guard13:
    $ r13_fork_set_fate('fate_crowd','supervisor')
    call r13_lines(r13_v111_lines(['MS14_D13_C_L0017']),'v111:MS14_D13_C_L0017')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D13_C_L0018']),'v111:MS14_D13_C_L0018')
    $ r13_v111_set('crowd_resolution_done',True)
    $ r13_v111_set('crowd_injury',False)
    $ r13_v111_set('outcome13','all_rescued')
    if r13_v111_value('crowd_preparation_schema13'):
        $ r13_crowd_release13()
    jump r13_v111_handover_plan13

label r13_v111_crowd_watch13:
    $ r13_fork_set_fate('fate_crowd','riot')
    call r13_lines(r13_v111_lines(['MS14_D13_C_L0020']),'v111:MS14_D13_C_L0020')
    # D1: 손을 놓으면 폭동이 된다. 너울이 맞아 죽고, 뒤집힌 수레에 아직 내리지 못한 모모가 깔린다.
    $ r13_v111_set('riot_momo13',r13_v111_value('handed:resident_momo') is not True and r13_v111_person_alive('resident_momo'))
    call r13_lines(r13_nw_block('riot13'),'nw:riot13')
    $ r13_v111_set('alive:neoul',False)
    if r13_v111_value('riot_momo13'):
        $ r13_v111_set('alive:resident_momo',False)
    $ r13_v111_set('crowd_resolution_done',True)
    $ r13_v111_set('crowd_injury',True)
    $ r13_v111_set('crowd_intervention','none')
    $ r13_v111_set('outcome13','crowd_violence')
    if r13_v111_value('crowd_preparation_schema13'):
        $ r13_crowd_release13()
    jump r13_v111_sleep13

# 미연결 분기(검토 0.20.4 연결 2): 정상 선택에서 들어오는 길이 없다. docs/design/UNCONNECTED_BRANCHES.md (2026-10-23 미연결 유지 결정).
label r13_v111_crowd_failed13:
    call r13_lines(r13_v111_lines(['MS14_D13_C_L0021']),'v111:MS14_D13_C_L0021')
    call r13_lines(r13_v111_lines(['MS14_D13_C_L0022']),'v111:MS14_D13_C_L0022')
    $ r13_v111_set('crowd_resolution_done',True)
    $ r13_v111_set('crowd_injury',True)
    $ r13_v111_set('crowd_intervention','failed')
    $ r13_v111_set('outcome13','crowd_violence')
    jump r13_v111_sleep13

label r13_v111_sleep13:
    if r13_v111_value("outcome13")=="family_priority":
        jump r13_v111_sleep13_gate
    if r13_v111_value("family_location")=="square":
        call r13_v111_collect_family13
    call r13_v111_travel('school','sleep13',['mom', 'daram'])
    $ r13_v111_set('family_location','school')
    $ r13_v111_set('location:daram','school')
    $ r13_v111_set('busy:mom',False)
    $ r13_v111_arrive(['mom', 'daram', 'nabi'])
    jump r13_v111_sleep13_input

label r13_v111_collect_family13:
    call r13_v111_travel('square','collect_family13',[])
    $ r13_v111_arrive(['mom', 'daram'])
    return

label r13_v111_sleep13_gate:
    call r13_v111_travel('gate','sleep13_gate',['mom', 'daram'])
    $ r13_v111_arrive(['mom', 'daram', 'guard'])
    jump r13_v111_sleep13_gate_input

label r13_v111_sleep13_gate_input:
    call r13_v111_wait('sleep13_gate_input')
    if _return==0:
        jump r13_v111_morning14
    jump r13_v111_sleep13_gate_input

label r13_v111_sleep13_input:
    call r13_v111_wait('sleep13_input')
    if _return==0:
        jump r13_v111_morning14
    jump r13_v111_sleep13_input

label r13_v111_morning14:
    $ r13_v111_set('day',14)
    jump r13_v111_day14

# 0.20.20 (소유자 2026-10-23 "다 해 줘", docs/reviews/aftermath-20261023): 결말마다 이번 판에 죽은 사람의
# 남은 물건을 한 줄씩. 죽은 사람이 없으면 아무것도 나오지 않는다(진엔딩은 사망 0 이라 늘 비어 있다).
label r13_v111_memorial14:
    if r13_nw_dead():
        call r13_lines(r13_nw_block('end_memorial14'),'nw:end_memorial14')
    return

label r13_v111_day14:
    jump r13_v111_ending_dispatch14

label r13_v111_ending_dispatch14:
    $ r13_v111_set('ending14',r13_nw_ending14())
    if r13_v111_value('ending14')=='left_name':
        jump r13_v111_left_name_ending14
    if r13_v111_value('ending14')=='frozen':
        jump r13_v111_frozen_ending14
    if r13_v111_value('ending14')=='family':
        jump r13_v111_family_ending14
    if r13_v111_value('ending14')=='partial':
        jump r13_v111_partial_ending14
    if r13_v111_value('ending14')=='violence':
        jump r13_v111_violence_ending14
    jump r13_v111_morning_safe14

label r13_v111_left_name_ending14:
    $ r13_edit(period=0,location='school')
    $ room13["v111"]["people"]=[]
    call r13_scene(R13_PLACES['school'][1],'남겨진 이름',"quiet")
    call r13_v111_memorial14
    call r13_lines(r13_nw_block('end_left_name14'),'nw:end_left_name14')
    jump r13_v111_story_end14

label r13_v111_frozen_ending14:
    $ r13_edit(period=0,location='gate')
    $ room13["v111"]["people"]=[]
    call r13_scene(R13_PLACES['gate'][1],'얼어붙은 마을',"quiet")
    call r13_v111_memorial14
    call r13_lines(r13_nw_block('end_frozen14'),'nw:end_frozen14')
    jump r13_v111_story_end14

label r13_v111_story_end14:
    $ r13_v111_set('story14_completed',True)
    call screen r13_confirm("이야기를 마쳤습니다. 현재 진행을 저장할 수 있습니다.",yes="메인 화면으로",no="저장하기")
    if not _return:
        call screen save
    return

label r13_v111_morning_safe14:
    $ r13_v111_scene('MS14_D14_S01')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('school','morning_safe14',['mom', 'daram'])
    $ r13_v111_arrive(['mom', 'daram', 'npc_pandol', 'nabi', 'resident_tosil', 'resident_madam'])
    $ r13_v111_score()
    call r13_v111_memorial14
    $ r13_v111_arrive(['mom', 'daram', 'npc_pandol', 'nabi', 'resident_tosil', 'resident_madam'])
    call r13_lines(r13_v111_lines(['MS14_D14_S01_L0002']),'v111:MS14_D14_S01_L0002')
    call r13_lines(r13_v111_lines(['MS14_D14_S01_L0003']),'v111:MS14_D14_S01_L0003')
    call r13_lines(r13_v111_lines(['MS14_D14_S01_L0004']),'v111:MS14_D14_S01_L0004')
    call r13_lines(r13_v111_lines(['MS14_D14_S01_L0006']),'v111:MS14_D14_S01_L0006')
    call r13_lines(r13_v111_lines(['MS14_D14_S01_L0007']),'v111:MS14_D14_S01_L0007')
    call r13_lines(r13_v111_lines(['MS14_D14_S01_L0008']),'v111:MS14_D14_S01_L0008')
    call r13_lines(r13_v111_lines(['MS14_D14_S01_L0010']),'v111:MS14_D14_S01_L0010')
    call r13_lines(r13_v111_lines(['MS14_D14_S01_L0011']),'v111:MS14_D14_S01_L0011')
    call r13_lines(r13_v111_lines(['MS14_D14_S01_L0012']),'v111:MS14_D14_S01_L0012')
    call r13_lines(r13_v111_lines(['MS14_D14_S01_L0013']),'v111:MS14_D14_S01_L0013')
    call r13_lines(r13_v111_lines(['MS14_D14_S01_L0014']),'v111:MS14_D14_S01_L0014')
    call r13_lines(r13_v111_lines(['MS14_D14_S01_L0015']),'v111:MS14_D14_S01_L0015')
    call r13_lines(r13_v111_lines(['MS14_D14_S01_L0017']),'v111:MS14_D14_S01_L0017')
    call r13_lines(r13_v111_lines(['MS14_D14_S01_L0018']),'v111:MS14_D14_S01_L0018')
    if r13_v111_value("OWL_ALIVE") is False:
        $ r13_nw_acquire("NW_BURNT_PAGE")
    $ r13_nw_acquire("NW_MADAM_DAY7")
    call r13_v111_old_rations14
    jump r13_v111_altar_guide14

label r13_v111_old_rations14:
    call r13_lines(r13_nw_block('old_rations14'),'nw:old_rations14')
    $ r13_nw_acquire("NW_OLD_RATIONS")
    return

label r13_v111_altar_guide14:
    call r13_v111_wait('altar_guide14')
    if _return==0:
        jump r13_v111_altar_ready14
    jump r13_v111_altar_guide14

label r13_v111_altar_ready14:
    if r13_v111_actor_ready('resident_badook'):
        call r13_lines(r13_nw_block('altar_guide14'),'nw:altar_guide14')
    $ r13_v111_set('altar_guide_confirmed',True)
    $ r13_v111_set('busy:resident_badook',False)
    jump r13_v111_altar14

label r13_v111_altar14:
    $ r13_v111_scene('MS14_D14_S02')
    $ r13_edit(period=1)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('altar','altar14',['mom', 'daram'])
    $ r13_v111_arrive(['mom', 'daram', 'resident_badook', 'karo'])
    $ r13_v111_score()
    $ r13_v111_arrive(['mom', 'daram', 'resident_badook', 'karo'])
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0003']),'v111:MS14_D14_S02_L0003')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0004']),'v111:MS14_D14_S02_L0004')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0005']),'v111:MS14_D14_S02_L0005')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0006']),'v111:MS14_D14_S02_L0006')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0008']),'v111:MS14_D14_S02_L0008')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0009']),'v111:MS14_D14_S02_L0009')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0010']),'v111:MS14_D14_S02_L0010')
    $ r13_nw_acquire("NW_TABLET_B")
    $ r13_nw_acquire("NW_IRON_MARK")
    $ r13_v111_set('altar_heat_structure_observed',True)
    jump r13_v111_mayor_interview14

label r13_v111_mayor_interview14:
    call r13_v111_travel('gate','mayor_interview14')
    $ r13_v111_arrive(['mom', 'resident_ppul', 'resident_badook', 'karo'])
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0012']),'v111:MS14_D14_S02_L0012')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0013']),'v111:MS14_D14_S02_L0013')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0014']),'v111:MS14_D14_S02_L0014')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0015']),'v111:MS14_D14_S02_L0015')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0016']),'v111:MS14_D14_S02_L0016')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0017']),'v111:MS14_D14_S02_L0017')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0019']),'v111:MS14_D14_S02_L0019')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0021']),'v111:MS14_D14_S02_L0021')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0022']),'v111:MS14_D14_S02_L0022')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0023']),'v111:MS14_D14_S02_L0023')
    $ r13_v111_set('mayor_false_invitation_admitted',True)
    jump r13_v111_altar1_q14

label r13_v111_altar1_q14:
    call r13_lines(r13_nw_block('altar1_q14'),'nw:altar1_q14')
    jump r13_v111_altar1_proof14

label r13_v111_altar1_proof14:
    $ r13_meeting_checkpoint("altar")
    call r13_v111_proof('희생의 숫자와 장부를 대조한다',['NW_NEOUL_LEDGER'],'r13_v111_altar1_won14','r13_v111_altar1_wrong14',None)
    jump expression _return

label r13_v111_altar1_wrong14:
    # 2026-10-25 결정 10: 장작 기록만 낸 판은 지금처럼 반쪽 답이다. 대체 정답(창고 아이들·침상 목록)을 함께 노리다 빠뜨린
    # 제출은 반쪽으로 끝내지 않고 기회를 쓴다.
    $ v111_altar_half=("V111:E14_SUPPLY" in (v111_last_presented or []) and not r13_v111_owned("NW_NEOUL_LEDGER") and not any(k in (v111_last_presented or []) for k in ("V111:NW_KKOMI_NOSTONE","V111:NW_SICK_BEDS")))
    if not v111_altar_half and r13_nw_retry("altar"):
        call r13_lines(r13_nw_block("altar1_lost14"),"nw:altar1_lost14:retry")
        jump r13_v111_altar1_proof14
    if v111_altar_half:
        $ r13_v111_set("altar_half1",True)
        $ r13_v111_set("altar_issue:1","half")
        call r13_lines(r13_nw_block("altar1_half14"),"nw:altar1_half14")
        jump r13_v111_altar2_q14
    call r13_lines(r13_nw_block('altar1_lost14'),'nw:altar1_lost14')
    jump r13_v111_altar_lost14

label r13_v111_altar1_won14:
    # 2026-10-25 결정 10: 장부가 없는 판(13일 피코 회의를 진 판)의 대체 정답 — 장작 인수·창고 아이들·침상 목록.
    if "V111:NW_NEOUL_LEDGER" not in (r13_v111_value("proof_given:희생의 숫자와 장부를 대조한다") or []):
        call r13_lines(r13_nw_block('altar1_won_alt14'),'nw:altar1_won_alt14')
    else:
        call r13_lines(r13_nw_block('altar1_won14'),'nw:altar1_won14')
    $ r13_v111_set('altar_issue:1','won')
    jump r13_v111_altar2_q14

label r13_v111_altar2_q14:
    call r13_lines(r13_nw_block('altar2_q14'),'nw:altar2_q14')
    jump r13_v111_altar2_proof14

label r13_v111_altar2_proof14:
    # 0.20.5 (Codex T01): without the records this question needs (an earlier meeting was lost),
    # say so and let the question stand unanswered; no chance is spent on an impossible answer.
    if not all(r13_v111_owned(k) for k in ['NW_TABLET_A', 'NW_TABLET_B']):
        call r13_lines(r13_nw_block('altar2_cannot14'),'nw:altar2_cannot14')
        call r13_lines(r13_nw_block('altar2_lost14'),'nw:altar2_lost14:cannot')
        $ r13_v111_set('altar_issue:2','lost')
        jump r13_v111_altar3_q14
    call r13_v111_proof('아르카가 부른다는 말과 옛 기록을 대조한다',['NW_TABLET_A', 'NW_TABLET_B'],'r13_v111_altar2_won14','r13_v111_altar2_wrong14',None)
    jump expression _return

label r13_v111_altar2_wrong14:
    if r13_nw_retry("altar",['NW_TABLET_A', 'NW_TABLET_B'],'촌장이 고개를 젓는다. 돌판의 앞 반쪽과 밑돌의 글자를 함께 놓아야 한다.'):
        call r13_lines(r13_nw_block("altar2_lost14"),"nw:altar2_lost14:retry")
        jump r13_v111_altar2_proof14
    call r13_lines(r13_nw_block('altar2_lost14'),'nw:altar2_lost14')
    $ r13_v111_set('altar_issue:2','lost')
    jump r13_v111_altar3_q14

label r13_v111_altar2_won14:
    call r13_lines(r13_nw_block('altar2_won14'),'nw:altar2_won14')
    $ r13_v111_set('altar_issue:2','won')
    jump r13_v111_altar3_q14

label r13_v111_altar3_q14:
    call r13_lines(r13_nw_block('altar3_q14'),'nw:altar3_q14')
    jump r13_v111_altar3_proof14

label r13_v111_altar3_proof14:
    # 0.20.5 (Codex T01): without the records this question needs (an earlier meeting was lost),
    # say so and let the question stand unanswered; no chance is spent on an impossible answer.
    if not all(r13_v111_owned(k) for k in ['NW_IRON_MARK']):
        call r13_lines(r13_nw_block('altar3_cannot14'),'nw:altar3_cannot14')
        call r13_lines(r13_nw_block('altar3_lost14'),'nw:altar3_lost14:cannot')
        $ r13_v111_set('altar_issue:3','lost')
        jump r13_v111_altar4_q14
    call r13_v111_proof('쇠가 언제 붙었는지 보인다',['NW_IRON_MARK'],'r13_v111_altar3_won14','r13_v111_altar3_wrong14',None)
    jump expression _return

label r13_v111_altar3_wrong14:
    if r13_nw_retry("altar",['NW_IRON_MARK'],None):
        call r13_lines(r13_nw_block("altar3_lost14"),"nw:altar3_lost14:retry")
        jump r13_v111_altar3_proof14
    call r13_lines(r13_nw_block('altar3_lost14'),'nw:altar3_lost14')
    $ r13_v111_set('altar_issue:3','lost')
    jump r13_v111_altar4_q14

label r13_v111_altar3_won14:
    call r13_lines(r13_nw_block('altar3_won14'),'nw:altar3_won14')
    $ r13_v111_set('altar_issue:3','won')
    jump r13_v111_altar4_q14

label r13_v111_altar4_q14:
    call r13_lines(r13_nw_block('altar4_q14'),'nw:altar4_q14')
    jump r13_v111_altar4_proof14

label r13_v111_altar4_proof14:
    # The school copy replaces only this question's yearly ration facts, not Neoul's whole ledger.
    # Missing both sources (or the wall names) still spends no chance on an impossible answer.
    if not (r13_v111_owned("NW_NAMES") and (r13_v111_owned("NW_NEOUL_LEDGER") or r13_v111_owned("NW_OLD_RATIONS"))):
        call r13_lines(r13_nw_block('altar4_cannot14'),'nw:altar4_cannot14')
        call r13_lines(r13_nw_block('altar4_lost14'),'nw:altar4_lost14:cannot')
        $ r13_v111_set('altar_issue:4','lost')
        jump r13_v111_altar_close14
    call r13_v111_proof('맨 처음 이름을 짚는다',['NW_NAMES', 'NW_NEOUL_LEDGER'],'r13_v111_altar4_won14','r13_v111_altar4_wrong14',None)
    jump expression _return

label r13_v111_altar4_wrong14:
    if r13_nw_retry("altar",['NW_NAMES', 'NW_NEOUL_LEDGER'],'촌장의 손이 떨린다. 벽의 이름과 그해 집별 배급 기록을 함께 놓아야 한다.'):
        call r13_lines(r13_nw_block("altar4_lost14"),"nw:altar4_lost14:retry")
        jump r13_v111_altar4_proof14
    call r13_lines(r13_nw_block('altar4_lost14'),'nw:altar4_lost14')
    $ r13_v111_set('altar_issue:4','lost')
    jump r13_v111_altar_close14

label r13_v111_altar4_won14:
    call r13_lines(r13_nw_block('altar4_won14'),'nw:altar4_won14')
    $ r13_v111_set('altar_issue:4','won')
    $ r13_v111_set('dallae_first_victim_known',True)
    jump r13_v111_altar_close14

label r13_v111_altar_close14:
    $ r13_nw_meeting_end("altar","win" if all(r13_v111_value("altar_issue:%d"%i)=="won" for i in (1,2,3,4)) else "partial")
    call r13_lines(r13_nw_block('altar_result14'),'nw:altar_result14')
    if r13_v111_value('dallae_first_victim_known'):
        call r13_v111_dallae14
    jump r13_v111_device14

label r13_v111_altar_lost14:
    $ r13_nw_meeting_end("altar","lose")
    call r13_lines(r13_nw_block('altar_lost14'),'nw:altar_lost14')
    jump r13_v111_granny_interview14

label r13_v111_dallae14:
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0025']),'v111:MS14_D14_S02_L0025')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0026']),'v111:MS14_D14_S02_L0026')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0027']),'v111:MS14_D14_S02_L0027')
    return

label r13_v111_device14:
    if r13_v111_value("buri_device_consent") and not r13_v111_value("mayor_site_decided") :
        jump r13_v111_mayor_site_request14
    # 검토 0.20.4 연결 1: 촌장이 동행하지 않으면 부리를 붙잡아 두는 이유와 부리의 조언을 문간에서 보인다.
    if r13_v111_value("buri_device_consent") and not r13_v111_value("mayor_site_joined") and r13_v111_person_alive("buri"):
        call r13_lines(r13_nw_block('buri_held14'),'nw:buri_held14')
    call r13_v111_travel('altar','device14')
    $ r13_v111_arrive(['mom', 'daram', 'karo', 'resident_badook'])
    if r13_v111_value("mayor_site_joined") and r13_v111_person_alive("buri"):
        call r13_v111_buri_work_start14
    jump r13_v111_device_record14

label r13_v111_mayor_site_request14:
    call r13_v111_wait('mayor_site_request14')
    if _return==0:
        jump r13_v111_mayor_site_yes14
    if _return==1:
        jump r13_v111_mayor_site_no14
    jump r13_v111_mayor_site_request14

label r13_v111_mayor_site_yes14:
    $ r13_v111_set('mayor_site_decided',True)
    $ r13_v111_set('mayor_site_joined',True)
    jump r13_v111_device14

label r13_v111_mayor_site_no14:
    $ r13_v111_set('mayor_site_decided',True)
    $ r13_v111_set('mayor_site_joined',False)
    jump r13_v111_device14

label r13_v111_buri_work_start14:
    $ r13_v111_arrive(['mom', 'daram', 'buri', 'resident_ppul', 'resident_badook', 'karo'])
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0031']),'v111:MS14_D14_S02_L0031')
    if r13_v111_actor_ready('buri'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0032']),'v111:MS14_D14_S02_L0032')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0034']),'v111:MS14_D14_S02_L0034')
    if r13_v111_value("madam_observer_consent"):
        call r13_v111_madam_device_question14
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0043']),'v111:MS14_D14_S02_L0043')
    $ r13_v111_set('buri_device_present',True)
    return

label r13_v111_madam_device_question14:
    if r13_v111_actor_ready('resident_madam'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0036']),'v111:MS14_D14_S02_L0036')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0037']),'v111:MS14_D14_S02_L0037')
    if r13_v111_actor_ready('resident_madam'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0038']),'v111:MS14_D14_S02_L0038')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0039']),'v111:MS14_D14_S02_L0039')
    if r13_v111_actor_ready('resident_madam'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0040']),'v111:MS14_D14_S02_L0040')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0041']),'v111:MS14_D14_S02_L0041')
    return

label r13_v111_madam_device_close14:
    if r13_v111_actor_ready('resident_madam'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0060']),'v111:MS14_D14_S02_L0060')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0061']),'v111:MS14_D14_S02_L0061')
    return

label r13_v111_device_record14:
    # 2026-10-24 행동 검수 14-6: 촌장이 따라오지 않은 판은 무엇에 답하려고 기록을 꺼내는지 물음이 없었다.
    if not r13_v111_value("buri_device_present") and r13_v111_actor_ready("resident_badook") and not r13_has("v111:shown:record_question14"):
        $ r13_flag("v111:shown:record_question14")
        call r13_lines(r13_nw_block('record_question14'),'nw:record_question14')
    call screen r13_book("dad",present=True,purpose="use")
    if _return=="V111:E13_HANDOVER" and r13_v111_owned("E13_HANDOVER"):
        jump r13_v111_device_rescue14
    if _return=="V111:E14_SUPPLY" and r13_v111_owned("E14_SUPPLY") and r13_v111_value("school_heat_connected"):
        jump r13_v111_device_supply14
    if _return:
        call r13_lines([r13_nw_added_line(dict(speaker="아빠",kind="thought",text="이걸로는 부족하다. 사람을 실제로 넘겨받은 기록이나, 물자를 연결해 쓴 것까지 확인한 기록이어야 한다."))],"v111:device_record_wrong14")
    jump r13_v111_device_pause14

label r13_v111_device_pause14:
    call r13_v111_wait('device_pause14')
    if _return==0:
        jump r13_v111_device_record14
    jump r13_v111_device_pause14

label r13_v111_device_rescue14:
    $ r13_v111_set('device_record_kind','rescue')
    if r13_v111_actor_ready('dad'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0082']),'v111:MS14_D14_S02_L0082')
    if r13_v111_actor_ready('mom'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0083']),'v111:MS14_D14_S02_L0083')
    $ r13_v111_set('device_record_shown',True)
    jump r13_v111_device_worker14

label r13_v111_device_supply14:
    $ r13_v111_set('device_record_kind','supply')
    if r13_v111_actor_ready('dad'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0079']),'v111:MS14_D14_S02_L0079')
    if r13_v111_actor_ready('mom'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0080']),'v111:MS14_D14_S02_L0080')
    $ r13_v111_set('device_record_shown',True)
    jump r13_v111_device_worker14

label r13_v111_device_worker14:
    if r13_v111_value("buri_device_present"):
        jump r13_v111_buri_record_answer14
    $ r13_v111_arrive(['mom', 'daram', 'karo', 'resident_badook'])
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0052']),'v111:MS14_D14_S02_L0052')
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0053']),'v111:MS14_D14_S02_L0053')
    $ r13_v111_set('busy:karo','device_support')
    $ r13_v111_set('device_support_ready',True)
    jump r13_v111_device_order14

label r13_v111_device_order14:
    call r13_v111_travel('gate','device_order14')
    $ r13_v111_arrive(['mom', 'resident_ppul', 'resident_badook', 'karo'])
    $ r13_v111_set('busy:karo',False)
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0074']),'v111:MS14_D14_S02_L0074')
    if r13_v111_actor_ready('resident_badook'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0075']),'v111:MS14_D14_S02_L0075')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0076']),'v111:MS14_D14_S02_L0076')
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0077']),'v111:MS14_D14_S02_L0077')
    if r13_v111_value("madam_observer_consent"):
        call r13_v111_madam_device_close14
    $ r13_v111_set('command_confrontation_done',True)
    call r13_v111_travel('altar','device_work14')
    $ r13_v111_arrive(['mom', 'daram', 'karo', 'resident_badook'])
    $ r13_v111_set('busy:karo','device_support')
    jump r13_v111_device_detach14

label r13_v111_device_detach14:
    call r13_v111_wait('device_detach14')
    if _return==0:
        jump r13_v111_device_detached14
    jump r13_v111_device_detach14

label r13_v111_device_detached14:
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0063']),'v111:MS14_D14_S02_L0063')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0064']),'v111:MS14_D14_S02_L0064')
    $ r13_v111_set('device_detached',True)
    $ r13_v111_set('busy:karo',False)
    $ r13_v111_set('busy:buri',False)
    if r13_v111_value("busy:guard")=="silluk_supervision":
        jump r13_v111_guard_relief14
    jump r13_v111_device_school14

label r13_v111_guard_relief14:
    call r13_v111_travel('v111_labor','guard_relief14',[])
    $ r13_v111_set("guard_relief_person","neoul" if r13_v111_value("busy:v111_patrol")=="teacher_supervision" else "v111_patrol")
    $ r13_v111_arrive(["guard","resident_siluk",r13_v111_value("guard_relief_person")])
    jump r13_v111_guard_relief_check14

label r13_v111_guard_relief_check14:
    call r13_v111_wait('guard_relief_check14')
    if _return==0:
        jump r13_v111_guard_relieved14
    jump r13_v111_guard_relief_check14

label r13_v111_guard_relieved14:
    $ r13_v111_set("busy:"+r13_v111_value("guard_relief_person"),"silluk_supervision")
    $ r13_v111_set('busy:guard',False)
    jump r13_v111_device_school14

label r13_v111_device_school14:
    call r13_v111_travel('school','device_school14')
    $ r13_v111_arrive(['mom', 'daram', 'karo', 'nabi', 'guard'])
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0067']),'v111:MS14_D14_S02_L0067')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0068']),'v111:MS14_D14_S02_L0068')
    jump r13_v111_device_lock14

label r13_v111_device_lock14:
    call r13_v111_wait('device_lock14')
    if _return==0:
        jump r13_v111_device_locked14
    jump r13_v111_device_lock14

label r13_v111_device_locked14:
    $ r13_v111_set('device_joint_control',True)
    jump r13_v111_granny_interview14

label r13_v111_buri_record_answer14:
    $ r13_v111_arrive(['mom', 'daram', 'buri', 'resident_ppul', 'resident_badook', 'karo'])
    if r13_v111_value("device_record_kind")=="supply" and r13_v111_value("buri_supply_participated"):
        call r13_v111_buri_supply_answer14
    else:
        call r13_v111_buri_no_transport_answer14
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0055']),'v111:MS14_D14_S02_L0055')
    if r13_v111_actor_ready('resident_badook'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0057']),'v111:MS14_D14_S02_L0057')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0058']),'v111:MS14_D14_S02_L0058')
    if r13_v111_value("madam_observer_consent"):
        call r13_v111_madam_device_close14
    $ r13_v111_set('command_confrontation_done',True)
    $ r13_v111_set('busy:buri','device_work')
    $ r13_v111_set('device_support_ready',True)
    jump r13_v111_device_detach14

label r13_v111_buri_supply_answer14:
    if r13_v111_actor_ready('buri'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0046']),'v111:MS14_D14_S02_L0046')
    call r13_lines(r13_v111_lines(['MS14_D14_S02_L0047']),'v111:MS14_D14_S02_L0047')
    if r13_v111_actor_ready('buri'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0048']),'v111:MS14_D14_S02_L0048')
    if r13_v111_actor_ready('buri'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0050']),'v111:MS14_D14_S02_L0050')
    return

label r13_v111_buri_no_transport_answer14:
    if r13_v111_actor_ready('buri'):
        call r13_lines(r13_v111_lines(['MS14_D14_S02_L0085']),'v111:MS14_D14_S02_L0085')
    return

label r13_v111_granny_interview14:
    $ r13_v111_scene('MS14_D14_S03')
    $ r13_edit(period=1)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('gate','granny_interview14',['mom', 'daram'])
    $ r13_v111_arrive(['mom', 'daram', 'granny', 'guard', 'resident_tosil', 'resident_owlgp'])
    $ r13_v111_score()
    $ r13_v111_arrive(['mom', 'daram', 'granny', 'guard', 'resident_tosil', 'resident_owlgp'])
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0002']),'v111:MS14_D14_S03_L0002')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0003']),'v111:MS14_D14_S03_L0003')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0004']),'v111:MS14_D14_S03_L0004')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0005']),'v111:MS14_D14_S03_L0005')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0006']),'v111:MS14_D14_S03_L0006')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0008']),'v111:MS14_D14_S03_L0008')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0009']),'v111:MS14_D14_S03_L0009')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0010']),'v111:MS14_D14_S03_L0010')
    jump r13_v111_tosil_listen14

label r13_v111_tosil_listen14:
    menu:
        '안에서 직접 듣는다':
            jump r13_v111_tosil_inside14
        '보호자와 밖에서 기다린다':
            jump r13_v111_tosil_outside14

label r13_v111_tosil_inside14:
    $ r13_v111_set('tosil_listen','inside')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0012']),'v111:MS14_D14_S03_L0012')
    if r13_v111_value('tosil_listen')=='inside' and r13_v111_actor_ready('resident_tosil'):
        call r13_lines(r13_v111_lines(['MS14_D14_S03_L0013']),'v111:MS14_D14_S03_L0013')
    if r13_v111_value('tosil_listen')=='inside' and r13_v111_actor_ready('resident_tosil'):
        call r13_lines(r13_v111_lines(['MS14_D14_S03_L0015']),'v111:MS14_D14_S03_L0015')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0016']),'v111:MS14_D14_S03_L0016')
    if r13_v111_value('tosil_listen')=='inside' and r13_v111_actor_ready('resident_tosil'):
        call r13_lines(r13_v111_lines(['MS14_D14_S03_L0017']),'v111:MS14_D14_S03_L0017')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0019']),'v111:MS14_D14_S03_L0019')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0020']),'v111:MS14_D14_S03_L0020')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0021']),'v111:MS14_D14_S03_L0021')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0022']),'v111:MS14_D14_S03_L0022')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0023']),'v111:MS14_D14_S03_L0023')
    if r13_v111_value('tosil_listen')=='inside' and r13_v111_actor_ready('resident_tosil'):
        call r13_lines(r13_v111_lines(['MS14_D14_S03_L0025']),'v111:MS14_D14_S03_L0025')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0027']),'v111:MS14_D14_S03_L0027')
    if r13_v111_value('tosil_listen')=='inside' and r13_v111_actor_ready('resident_tosil'):
        call r13_lines(r13_v111_lines(['MS14_D14_S03_L0028']),'v111:MS14_D14_S03_L0028')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0030']),'v111:MS14_D14_S03_L0030')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0031']),'v111:MS14_D14_S03_L0031')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0032']),'v111:MS14_D14_S03_L0032')
    if r13_v111_value('tosil_listen')=='inside' and r13_v111_actor_ready('resident_tosil'):
        call r13_lines(r13_v111_lines(['MS14_D14_S03_L0034']),'v111:MS14_D14_S03_L0034')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0035']),'v111:MS14_D14_S03_L0035')
    $ r13_v111_set('bomi_death_confirmed',True)
    $ r13_v111_set('adult_interview_done',True)
    jump r13_v111_name_board14

label r13_v111_tosil_outside14:
    $ r13_v111_set('tosil_listen','outside')
    $ r13_v111_set('location:resident_tosil','outside_guard')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0019']),'v111:MS14_D14_S03_L0019')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0020']),'v111:MS14_D14_S03_L0020')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0021']),'v111:MS14_D14_S03_L0021')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0022']),'v111:MS14_D14_S03_L0022')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0023']),'v111:MS14_D14_S03_L0023')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0030']),'v111:MS14_D14_S03_L0030')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0031']),'v111:MS14_D14_S03_L0031')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0032']),'v111:MS14_D14_S03_L0032')
    $ r13_v111_set('bomi_death_confirmed',True)
    $ r13_v111_set('adult_interview_done',True)
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0037']),'v111:MS14_D14_S03_L0037')
    if r13_v111_value('tosil_listen')=='outside' and r13_v111_value('adult_interview_done'):
        call r13_lines(r13_v111_lines(['MS14_D14_S03_L0038']),'v111:MS14_D14_S03_L0038')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0039']),'v111:MS14_D14_S03_L0039')
    jump r13_v111_name_board14

label r13_v111_name_board14:
    $ r13_v111_scene('MS14_D14_S04')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('square','name_board14',['mom', 'daram'])
    $ r13_v111_arrive(['mom', 'daram', 'resident_tosil', 'npc_pandol'])
    $ r13_v111_score()
    $ r13_v111_arrive(['mom', 'daram', 'resident_tosil', 'npc_pandol'])
    call r13_lines(r13_nw_block('name_board_intro14'),'nw:name_board_intro14')
    menu:
        '토실이 이름을 쓰겠다면 기다린다':
            jump r13_v111_tosil_name14
        '지금 쓰지 않아도 된다고 말한다':
            jump r13_v111_tosil_no_name14

label r13_v111_tosil_name14:
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0003']),'v111:MS14_D14_S04_L0003')
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0004']),'v111:MS14_D14_S04_L0004')
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0006']),'v111:MS14_D14_S04_L0006')
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0007']),'v111:MS14_D14_S04_L0007')
    jump r13_v111_pandol_news14

label r13_v111_tosil_no_name14:
    if r13_v111_value('tosil_listen')=='inside' and r13_v111_actor_ready('resident_tosil'):
        call r13_lines(r13_v111_lines(['MS14_D14_S03_L0040']),'v111:MS14_D14_S03_L0040')
    call r13_lines(r13_v111_lines(['MS14_D14_S03_L0041']),'v111:MS14_D14_S03_L0041')
    jump r13_v111_pandol_news14

label r13_v111_pandol_news14:
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0009']),'v111:MS14_D14_S04_L0009')
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0010']),'v111:MS14_D14_S04_L0010')
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0011']),'v111:MS14_D14_S04_L0011')
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0013']),'v111:MS14_D14_S04_L0013')
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0014']),'v111:MS14_D14_S04_L0014')
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0015']),'v111:MS14_D14_S04_L0015')
    call r13_v111_travel('school','supply_display14')
    $ r13_v111_arrive(['mom', 'daram', 'nabi', 'guard'])
    jump r13_v111_supply_inventory14

label r13_v111_supply_inventory14:
    call r13_v111_wait('supply_inventory14')
    if _return==0:
        jump r13_v111_supply_inventory_done14
    jump r13_v111_supply_inventory14

label r13_v111_supply_inventory_done14:
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0017']),'v111:MS14_D14_S04_L0017')
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0018']),'v111:MS14_D14_S04_L0018')
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0019']),'v111:MS14_D14_S04_L0019')
    if r13_v111_actor_ready("resident_madam"):
        call r13_v111_madam_inventory14
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D14_S04_L0025']),'v111:MS14_D14_S04_L0025')
    $ r13_v111_set('school_inventory_checked',True)
    $ r13_v111_set('school_supply_handed',True)
    $ r13_v111_set('school_heat_connected',True)
    $ r13_v111_set("current_sacrifice_operation_closed",bool(r13_v111_value("current_transport_chain_stopped") and r13_v111_value("device_joint_control")))
    jump r13_v111_lamp_assignment14

label r13_v111_madam_inventory14:
    if r13_v111_actor_ready('resident_madam'):
        call r13_lines(r13_v111_lines(['MS14_D14_S04_L0022']),'v111:MS14_D14_S04_L0022')
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0023']),'v111:MS14_D14_S04_L0023')
    return

label r13_v111_lamp_assignment14:
    $ r13_v111_arrive(['mom', 'daram', 'nabi', 'guard', 'resident_lamplighter'])
    if r13_v111_actor_ready("resident_lamplighter"):
        call r13_v111_chorong_lamps14
    else:
        call r13_v111_mother_lamps14
    if r13_v111_value('OWL_ALIVE'):
        call r13_v111_owl_alive14
    if not (r13_v111_value("current_transport_chain_stopped") and r13_v111_value("device_joint_control")):
        call r13_v111_unfinished_operation14
    jump r13_v111_cookie14

label r13_v111_chorong_lamps14:
    if r13_v111_actor_ready('resident_lamplighter'):
        call r13_lines(r13_v111_lines(['MS14_D14_S04_L0029']),'v111:MS14_D14_S04_L0029')
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0030']),'v111:MS14_D14_S04_L0030')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D14_S04_L0031']),'v111:MS14_D14_S04_L0031')
    $ r13_v111_set('lamp_manager','resident_lamplighter')
    return

label r13_v111_mother_lamps14:
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0032']),'v111:MS14_D14_S04_L0032')
    $ r13_v111_set('lamp_manager','mom')
    return

label r13_v111_owl_alive14:
    $ r13_v111_arrive(['mom', 'daram', 'nabi', 'guard', 'resident_owlgp'])
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0033']),'v111:MS14_D14_S04_L0033')
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0034']),'v111:MS14_D14_S04_L0034')
    return

label r13_v111_unfinished_operation14:
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0035']),'v111:MS14_D14_S04_L0035')
    call r13_lines(r13_v111_lines(['MS14_D14_S04_L0036']),'v111:MS14_D14_S04_L0036')
    $ r13_v111_commit('MS14_D14_S04_L0036')
    return

label r13_v111_family_ending14:
    $ r13_v111_scene('MS14_D14_END_FAMILY')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('gate','family_ending14',['mom', 'daram'])
    $ r13_v111_arrive(['mom', 'daram', 'guard'])
    $ r13_v111_score()
    call r13_v111_memorial14
    $ r13_v111_arrive(['mom', 'daram', 'guard'])
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D14_END_FAMILY_L0002']),'v111:MS14_D14_END_FAMILY_L0002')
    call r13_lines(r13_v111_lines(['MS14_D14_END_FAMILY_L0003']),'v111:MS14_D14_END_FAMILY_L0003')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D14_END_FAMILY_L0004']),'v111:MS14_D14_END_FAMILY_L0004')
    call r13_lines(r13_v111_lines(['MS14_D14_END_FAMILY_L0006']),'v111:MS14_D14_END_FAMILY_L0006')
    call r13_lines(r13_v111_lines(['MS14_D14_END_FAMILY_L0007']),'v111:MS14_D14_END_FAMILY_L0007')
    call r13_lines(r13_v111_lines(['MS14_D14_END_FAMILY_L0008']),'v111:MS14_D14_END_FAMILY_L0008')
    call r13_lines(r13_v111_lines(['MS14_D14_END_FAMILY_L0010']),'v111:MS14_D14_END_FAMILY_L0010')
    jump r13_v111_family_lodging14

label r13_v111_partial_ending14:
    $ r13_v111_scene('MS14_D14_END_PARTIAL')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('square','partial_ending14',[])
    $ r13_v111_arrive(['karo', 'guard', 'resident_badook', 'daram'])
    $ r13_v111_score()
    call r13_v111_memorial14
    $ r13_v111_arrive(['karo', 'guard', 'resident_badook', 'daram'])
    if r13_v111_value("cart_departed"):
        jump r13_v111_partial_departed14
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D14_END_PARTIAL_L0002']),'v111:MS14_D14_END_PARTIAL_L0002')
    call r13_lines(r13_v111_lines(['MS14_D14_END_PARTIAL_L0003']),'v111:MS14_D14_END_PARTIAL_L0003')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D14_END_PARTIAL_L0004']),'v111:MS14_D14_END_PARTIAL_L0004')
    call r13_lines(r13_v111_lines(['MS14_D14_END_PARTIAL_L0006']),'v111:MS14_D14_END_PARTIAL_L0006')
    call r13_lines(r13_v111_lines(['MS14_D14_END_PARTIAL_L0007']),'v111:MS14_D14_END_PARTIAL_L0007')
    jump r13_v111_partial_handoff14

label r13_v111_partial_departed14:
    call r13_lines(r13_nw_block('partial_departed14'),'nw:partial_departed14')
    jump r13_v111_cookie14

label r13_v111_partial_handoff14:
    call r13_v111_wait('partial_handoff14')
    if _return==0:
        jump r13_v111_partial_work14
    jump r13_v111_partial_handoff14

label r13_v111_partial_work14:
    $ v111_pending_patient=next((p for p in (r13_v111_value("cart_roster") or ["npc_pandol","resident_momo","resident_guldol"]) if not r13_v111_value("handed:"+p) and r13_v111_person_alive(p)),None)
    jump r13_v111_partial_patient14

label r13_v111_partial_patient14:
    call r13_v111_travel('school','partial_patient14',[])
    $ r13_v111_arrive(["mom","daram","nabi","karo","guard"]+([v111_pending_patient] if v111_pending_patient else []))
    jump r13_v111_partial_receipt14

label r13_v111_partial_receipt14:
    call r13_v111_wait('partial_receipt14')
    if _return==0:
        jump r13_v111_partial_received14
    jump r13_v111_partial_receipt14

label r13_v111_partial_received14:
    if v111_pending_patient:
        $ r13_v111_set("handed:"+v111_pending_patient,True)
    $ v111_pending_rest=[p for p in (r13_v111_value("cart_roster") or ["npc_pandol","resident_momo","resident_guldol"]) if not r13_v111_value("handed:"+p) and r13_v111_person_alive(p)]
    if v111_pending_rest:
        jump r13_v111_partial_wait14
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D14_END_PARTIAL_L0009']),'v111:MS14_D14_END_PARTIAL_L0009')
    call r13_lines(r13_v111_lines(['MS14_D14_END_PARTIAL_L0010']),'v111:MS14_D14_END_PARTIAL_L0010')
    if r13_v111_actor_ready('karo'):
        call r13_lines(r13_v111_lines(['MS14_D14_END_PARTIAL_L0011']),'v111:MS14_D14_END_PARTIAL_L0011')
    $ r13_v111_set('pending_handover_completed',True)
    jump r13_v111_cookie14

label r13_v111_partial_wait14:
    call r13_v111_travel('square','partial_wait14',[])
    $ r13_v111_arrive(['karo', 'guard', 'resident_badook'])
    call r13_lines(r13_v111_lines(['MS14_D14_END_PARTIAL_L0012']),'v111:MS14_D14_END_PARTIAL_L0012')
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D14_END_PARTIAL_L0013']),'v111:MS14_D14_END_PARTIAL_L0013')
    $ r13_v111_set('pending_handover_completed',False)
    $ r13_v111_set('pending_handover_supervised',True)
    jump r13_v111_cookie14

label r13_v111_violence_ending14:
    $ r13_v111_scene('MS14_D14_END_VIOLENCE')
    $ r13_edit(period=0)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('clinic','violence_ending14',['mom', 'daram'])
    $ r13_v111_arrive(['mom', 'daram', 'guard', 'resident_seori'])
    $ r13_v111_score()
    call r13_v111_memorial14
    $ r13_v111_arrive(['mom', 'daram', 'guard', 'resident_seori'])
    call r13_lines(r13_v111_lines(['MS14_D14_END_VIOLENCE_L0002']),'v111:MS14_D14_END_VIOLENCE_L0002')
    call r13_lines(r13_v111_lines(['MS14_D14_END_VIOLENCE_L0003']),'v111:MS14_D14_END_VIOLENCE_L0003')
    call r13_lines(r13_v111_lines(['MS14_D14_END_VIOLENCE_L0004']),'v111:MS14_D14_END_VIOLENCE_L0004')
    if r13_v111_value('crowd_witnessed') or r13_v111_value('family_location')=='square':
        call r13_v111_crowd_child_saw14
    else:
        call r13_v111_crowd_child_away14
    if r13_v111_value('crowd_intervention')=='failed':
        call r13_v111_crowd_failed14
    else:
        call r13_v111_crowd_no_action14
    jump r13_v111_cookie14

label r13_v111_crowd_child_saw14:
    call r13_lines(r13_v111_lines(['MS14_D14_END_VIOLENCE_L0007']),'v111:MS14_D14_END_VIOLENCE_L0007')
    return

label r13_v111_crowd_child_away14:
    call r13_lines(r13_v111_lines(['MS14_D14_END_VIOLENCE_L0009']),'v111:MS14_D14_END_VIOLENCE_L0009')
    call r13_lines(r13_v111_lines(['MS14_D14_END_VIOLENCE_L0010']),'v111:MS14_D14_END_VIOLENCE_L0010')
    call r13_lines(r13_v111_lines(['MS14_D14_END_VIOLENCE_L0011']),'v111:MS14_D14_END_VIOLENCE_L0011')
    call r13_lines(r13_v111_lines(['MS14_D14_END_VIOLENCE_L0012']),'v111:MS14_D14_END_VIOLENCE_L0012')
    return

label r13_v111_crowd_failed14:
    call r13_lines(r13_v111_lines(['MS14_D14_END_VIOLENCE_L0017']),'v111:MS14_D14_END_VIOLENCE_L0017')
    call r13_lines(r13_v111_lines(['MS14_D14_END_VIOLENCE_L0018']),'v111:MS14_D14_END_VIOLENCE_L0018')
    return

label r13_v111_crowd_no_action14:
    call r13_lines(r13_v111_lines(['MS14_D14_END_VIOLENCE_L0014']),'v111:MS14_D14_END_VIOLENCE_L0014')
    call r13_lines(r13_v111_lines(['MS14_D14_END_VIOLENCE_L0015']),'v111:MS14_D14_END_VIOLENCE_L0015')
    return

label r13_v111_family_lodging14:
    call r13_v111_travel('gate','family_lodging14')
    $ r13_v111_arrive(['mom', 'daram', 'guard'])
    if r13_v111_actor_ready('guard'):
        call r13_lines(r13_v111_lines(['MS14_D14_S05_L0024']),'v111:MS14_D14_S05_L0024')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0025']),'v111:MS14_D14_S05_L0025')
    $ r13_v111_commit('MS14_D14_S05_L0025')
    jump r13_v111_cookie_gate14

label r13_v111_cookie14:
    call r13_v111_travel('school','cookie14')
    $ r13_v111_arrive(['mom', 'daram'])
    $ r13_v111_set('night14_lodging','school')
    jump r13_v111_cookie_scene14

label r13_v111_cookie_gate14:
    $ r13_v111_arrive(['mom', 'daram'])
    $ r13_v111_set('night14_lodging','gate')
    jump r13_v111_cookie_scene14

label r13_v111_cookie_scene14:
    $ r13_edit(period=2)
    $ r13_v111_scene('MS14_D14_S05')
    call r13_scene(R13_PLACES[room13["location"]][1],R13_PLACES[room13["location"]][0],"calm")
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0002']),'v111:MS14_D14_S05_L0002')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0003']),'v111:MS14_D14_S05_L0003')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0004']),'v111:MS14_D14_S05_L0004')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0006']),'v111:MS14_D14_S05_L0006')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0007']),'v111:MS14_D14_S05_L0007')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0008']),'v111:MS14_D14_S05_L0008')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0009']),'v111:MS14_D14_S05_L0009')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0010']),'v111:MS14_D14_S05_L0010')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0012']),'v111:MS14_D14_S05_L0012')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0013']),'v111:MS14_D14_S05_L0013')
    if r13_v111_value('crowd_injury'):
        call r13_v111_cookie_distance14
    if not r13_v111_value('crowd_injury'):
        call r13_lines(r13_v111_lines(['MS14_D14_S05_L0015']),'v111:MS14_D14_S05_L0015')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0017']),'v111:MS14_D14_S05_L0017')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0018']),'v111:MS14_D14_S05_L0018')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0019']),'v111:MS14_D14_S05_L0019')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0020']),'v111:MS14_D14_S05_L0020')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0021']),'v111:MS14_D14_S05_L0021')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0022']),'v111:MS14_D14_S05_L0022')
    if r13_v111_value('ending14')=='morning' and r13_v111_value('meeting:hypothesis')=='lose' and r13_v111_value('meeting:altar')=='lose':
        jump r13_v111_wild_night14
    # 0.20.7 (ending review): the path's last act (what was saved, lost or still waiting).
    call r13_lines(r13_nw_block('ending_last14'),'nw:ending_last14')
    if r13_nw_true_ending_ready():
        call r13_v111_true_epilogue14
    $ r13_v111_set('story14_completed',True)
    call screen r13_confirm("이야기를 마쳤습니다. 현재 진행을 저장할 수 있습니다.",yes="메인 화면으로",no="저장하기")
    if not _return:
        call screen save
    return

label r13_v111_cookie_distance14:
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0031']),'v111:MS14_D14_S05_L0031')
    call r13_lines(r13_v111_lines(['MS14_D14_S05_L0032']),'v111:MS14_D14_S05_L0032')
    return

label r13_v111_true_epilogue14:
    # 0.20.5 (Codex T02): the ending just read is recorded before the true epilogue replaces it.
    $ r13_fork_ending(r13_v111_value('ending14'))
    $ r13_v111_set('ending14','true')
    call r13_hidden_base14
    $ r13_edit(location="gate")
    $ room13["v111"]["people"]=[]
    call r13_scene(R13_PLACES["gate"][1],"말을 위한 돌","quiet")
    call r13_lines(r13_nw_block('end_true14'),'nw:end_true14')
    return

label r13_v111_wild_family_wait14:
    call r13_lines(r13_nw_block('wild_family_wait14'),'nw:wild_family_wait14')
    return

label r13_v111_wild_night14:
    $ r13_v111_set('ending14','wild_night')
    $ r13_v111_set('wild_night14',True)
    $ r13_v111_set('wild_late',0)
    jump r13_v111_wild_room14

label r13_v111_wild_room14:
    $ r13_edit(period=2,location='school')
    $ room13["v111"]["people"]=[]
    call r13_scene(R13_PLACES['school'][1],'불타는 밤',"night")
    $ r13_sound_ambience('fire')
    $ r13_v111_arrive(['mom', 'daram', 'nabi'])
    call r13_lines(r13_nw_block('wild_wake14'),'nw:wild_wake14')
    call r13_v111_wait('wild_room14')
    jump r13_v111_wild_hall14

label r13_v111_wild_hall14:
    $ r13_edit(period=2,location='school')
    $ room13["v111"]["people"]=[]
    call r13_scene(R13_PLACES['school'][1],'불타는 밤',"night")
    $ r13_sound_ambience('fire')
    $ r13_v111_arrive(['mom', 'daram', 'doto'])
    call r13_lines(r13_nw_block('wild_hall14'),'nw:wild_hall14')
    call r13_v111_wait('wild_hall14')
    if _return==0:
        $ r13_v111_set('wild_late',(r13_v111_value('wild_late') or 0)+1)
        call r13_lines(r13_nw_block('wild_hall_help14'),'nw:wild_hall_help14')
    jump r13_v111_wild_square14

label r13_v111_wild_square14:
    $ r13_edit(period=2,location='square')
    $ room13["v111"]["people"]=[]
    call r13_scene(R13_PLACES['square'][1],'불타는 밤',"night")
    $ r13_sound_ambience('fire')
    $ r13_v111_arrive(['mom', 'daram', 'resident_badook'])
    call r13_lines(r13_nw_block('wild_square14'),'nw:wild_square14')
    call r13_v111_wait('wild_square14')
    if _return==0:
        $ r13_v111_set('wild_late',(r13_v111_value('wild_late') or 0)+1)
        call r13_lines(r13_nw_block('wild_square_help14'),'nw:wild_square_help14')
    jump r13_v111_wild_road14

label r13_v111_wild_road14:
    $ r13_edit(period=2,location='forest')
    $ room13["v111"]["people"]=[]
    call r13_scene(R13_PLACES['forest'][1],'불타는 밤',"night")
    $ r13_sound_ambience('fire')
    $ r13_v111_arrive(['mom', 'daram', 'guard'])
    call r13_lines(r13_nw_block('wild_road14'),'nw:wild_road14')
    call r13_v111_wait('wild_road14')
    if _return==0:
        $ r13_v111_set('wild_late',(r13_v111_value('wild_late') or 0)+1)
        call r13_lines(r13_nw_block('wild_road_help14'),'nw:wild_road_help14')
    jump r13_v111_wild_climb14

label r13_v111_wild_climb14:
    $ r13_edit(period=2,location='forest')
    $ room13["v111"]["people"]=[]
    $ r13_v111_arrive(['mom','daram'])
    $ r13_v111_set('wild_family',r13_nw_wild_family())
    call r13_lines(r13_nw_block('wild_climb14'),'nw:wild_climb14')
    jump r13_v111_wild_ending14

label r13_v111_wild_ending14:
    $ r13_edit(period=0,location='greenhouse')
    $ room13["v111"]["people"]=[]
    if r13_v111_value('wild_family')=='three':
        $ r13_v111_arrive(['mom','daram'])
    elif r13_v111_value('wild_family')=='no_mom':
        $ r13_v111_arrive(['daram'])
    call r13_scene(R13_PLACES['greenhouse'][1],'불타는 밤',"quiet")
    call r13_lines(r13_nw_block('end_wild_night14'),'nw:end_wild_night14')
    jump r13_v111_story_end14

init 315 python:
    R13_V111_ALLOWED={
        'MS14_D11_S00_L0002':lambda: r13_v111_actor_ready('karo'),
        'MS14_D11_S00_L0004':lambda: r13_v111_actor_ready('karo'),
        'MS14_D11_S03_L0002':lambda: r13_v111_actor_ready('resident_guldol'),
        'MS14_D11_S03_L0006':lambda: r13_v111_actor_ready('resident_guldol'),
        'MS14_D11_S03_L0012':lambda: r13_v111_actor_ready('resident_lamplighter'),
        'MS14_D11_S03_L0016':lambda: r13_v111_actor_ready('resident_guldol'),
        'MS14_D11_S03_L0051':lambda: r13_v111_actor_ready('resident_nero'),
        'MS14_D11_S04_L0009':lambda: r13_v111_actor_ready('resident_nero'),
        'MS14_D11_S04_L0011':lambda: r13_v111_actor_ready('karo'),
        'MS14_D11_S04_L0013':lambda: r13_v111_actor_ready('resident_nero'),
        'MS14_D11_S04_L0016':lambda: r13_v111_actor_ready('resident_nero'),
        'MS14_D11_S04_L0021':lambda: r13_v111_actor_ready('resident_nero'),
        'MS14_D11_S04_L0023':lambda: r13_v111_actor_ready('resident_nero'),
        'MS14_D11_S04_L0027':lambda: r13_v111_actor_ready('karo'),
        'MS14_D11_S04_L0030':lambda: r13_v111_actor_ready('resident_nero'),
        'MS14_D11_S04_L0032':lambda: r13_v111_actor_ready('resident_nero'),
        'MS14_D11_S04_L0036':lambda: r13_v111_actor_ready('resident_nero'),
        'MS14_D11_S04_L0038':lambda: r13_v111_actor_ready('resident_nero'),
        'MS14_D12_S01_L0011':lambda: r13_v111_actor_ready('resident_nero'),
        'MS14_D12_S01_L0013':lambda: r13_v111_actor_ready('resident_nero'),
        'MS14_D12_S01_L0015':lambda: r13_v111_actor_ready('resident_nero'),
        'MS14_D12_S01_L0018':lambda: r13_v111_actor_ready('guard'),
        'MS14_D12_S01_L0028':lambda: r13_v111_actor_ready('karo'),
        'MS14_D12_S01_L0030':lambda: r13_v111_actor_ready('karo'),
        'MS14_D12_S04_L0002':lambda: r13_v111_actor_ready('resident_madam'),
        'MS14_D12_S04_L0046':lambda: r13_v111_value('route12')=='late_exposure',
        'MS14_D12_S05_L0030':lambda: r13_v111_actor_ready('guard'),
        'MS14_D12_S05_L0033':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S01_L0005':lambda: r13_v111_actor_ready('karo'),
        'MS14_D13_S01_L0016':lambda: r13_v111_actor_ready('karo'),
        'MS14_D13_S02_L0002':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S02_L0004':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S02_L0006':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S02_L0008':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S02_L0010':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S02_L0021':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S02_L0032':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S04_L0002':lambda: r13_v111_actor_ready('resident_badook'),
        'MS14_D13_S04_L0004':lambda: r13_v111_actor_ready('resident_badook'),
        'MS14_D13_S04_L0009':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S04_L0012':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S04_L0014':lambda: r13_v111_actor_ready('resident_badook'),
        'MS14_D13_S04_L0021':lambda: r13_v111_actor_ready('nabi') and room13['location']=='school',
        'MS14_D13_S04_L0026':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S04_L0028':lambda: r13_v111_actor_ready('daram') and room13['location']=='square',
        'MS14_D13_S04_L0031':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S04_L0035':lambda: r13_v111_actor_ready('mom') and room13['location']=='square',
        'MS14_D13_S04_L0040':lambda: r13_v111_actor_ready('resident_badook'),
        'MS14_D13_S04_L0045':lambda: r13_v111_actor_ready('resident_badook'),
        'MS14_D13_S04_L0055':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S04_L0057':lambda: r13_v111_actor_ready('karo'),
        'MS14_D13_S04_L0058':lambda: r13_v111_actor_ready('daram') and room13['location']=='square',
        'MS14_D13_S04_L0061':lambda: r13_v111_actor_ready('resident_nero'),
        'MS14_D13_S04_L0062':lambda: r13_v111_actor_ready('mom') and room13['location']=='square',
        'MS14_D13_S04_L0064':lambda: r13_v111_actor_ready('mom') and room13['location']=='square',
        'MS14_D13_S04_L0070':lambda: r13_v111_actor_ready('resident_guldol'),
        'MS14_D13_S04_L0074':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S04_L0077':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S04_L0079':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S04_L0081':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_S04_L0083':lambda: r13_v111_actor_ready('karo'),
        'MS14_D13_S04_L0085':lambda: r13_v111_actor_ready('karo'),
        'MS14_D13_S04_L0086':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_B_L0002':lambda: r13_v111_actor_ready('karo'),
        'MS14_D13_B_L0003':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_B_L0006':lambda: r13_v111_actor_ready('resident_badook'),
        'MS14_D13_C_L0006':lambda: r13_v111_actor_ready('daram') and room13['location']=='square',
        'MS14_D13_C_L0013':lambda: r13_v111_actor_ready('daram') and room13['location']=='square',
        'MS14_D13_C_L0014':lambda: r13_v111_actor_ready('guard'),
        'MS14_D13_C_L0018':lambda: r13_v111_actor_ready('guard'),
        'MS14_D14_S02_L0032':lambda: r13_v111_actor_ready('buri'),
        'MS14_D14_S02_L0036':lambda: r13_v111_actor_ready('resident_madam'),
        'MS14_D14_S02_L0038':lambda: r13_v111_actor_ready('resident_madam'),
        'MS14_D14_S02_L0040':lambda: r13_v111_actor_ready('resident_madam'),
        'MS14_D14_S02_L0079':lambda: r13_v111_actor_ready('dad'),
        'MS14_D14_S02_L0080':lambda: r13_v111_actor_ready('mom'),
        'MS14_D14_S02_L0082':lambda: r13_v111_actor_ready('dad'),
        'MS14_D14_S02_L0083':lambda: r13_v111_actor_ready('mom'),
        'MS14_D14_S02_L0046':lambda: r13_v111_actor_ready('buri'),
        'MS14_D14_S02_L0048':lambda: r13_v111_actor_ready('buri'),
        'MS14_D14_S02_L0050':lambda: r13_v111_actor_ready('buri'),
        'MS14_D14_S02_L0085':lambda: r13_v111_actor_ready('buri'),
        'MS14_D14_S02_L0053':lambda: r13_v111_actor_ready('karo'),
        'MS14_D14_S02_L0057':lambda: r13_v111_actor_ready('resident_badook'),
        'MS14_D14_S02_L0060':lambda: r13_v111_actor_ready('resident_madam'),
        'MS14_D14_S02_L0068':lambda: r13_v111_actor_ready('guard'),
        'MS14_D14_S02_L0070':lambda: r13_v111_actor_ready('buri'),
        'MS14_D14_S02_L0075':lambda: r13_v111_actor_ready('resident_badook'),
        'MS14_D14_S02_L0077':lambda: r13_v111_actor_ready('karo'),
        'MS14_D14_S03_L0013':lambda: r13_v111_value('tosil_listen')=='inside' and r13_v111_actor_ready('resident_tosil'),
        'MS14_D14_S03_L0015':lambda: r13_v111_value('tosil_listen')=='inside' and r13_v111_actor_ready('resident_tosil'),
        'MS14_D14_S03_L0017':lambda: r13_v111_value('tosil_listen')=='inside' and r13_v111_actor_ready('resident_tosil'),
        'MS14_D14_S03_L0025':lambda: r13_v111_value('tosil_listen')=='inside' and r13_v111_actor_ready('resident_tosil'),
        'MS14_D14_S03_L0028':lambda: r13_v111_value('tosil_listen')=='inside' and r13_v111_actor_ready('resident_tosil'),
        'MS14_D14_S03_L0034':lambda: r13_v111_value('tosil_listen')=='inside' and r13_v111_actor_ready('resident_tosil'),
        'MS14_D14_S03_L0038':lambda: r13_v111_value('tosil_listen')=='outside' and r13_v111_value('adult_interview_done'),
        'MS14_D14_S03_L0040':lambda: r13_v111_value('tosil_listen')=='inside' and r13_v111_actor_ready('resident_tosil'),
        'MS14_D14_S04_L0022':lambda: r13_v111_actor_ready('resident_madam'),
        'MS14_D14_S04_L0025':lambda: r13_v111_actor_ready('guard'),
        'MS14_D14_S04_L0029':lambda: r13_v111_actor_ready('resident_lamplighter'),
        'MS14_D14_S04_L0031':lambda: r13_v111_actor_ready('guard'),
        'MS14_D14_S05_L0015':lambda: not r13_v111_value('crowd_injury'),
        'MS14_D14_S05_L0024':lambda: r13_v111_actor_ready('guard'),
        'MS14_D14_S05_L0026':lambda: r13_v111_actor_ready('guard'),
        'MS14_D14_END_FAMILY_L0002':lambda: r13_v111_actor_ready('guard'),
        'MS14_D14_END_FAMILY_L0004':lambda: r13_v111_actor_ready('guard'),
        'MS14_D14_END_FAMILY_L0012':lambda: r13_v111_actor_ready('guard'),
        'MS14_D14_END_FAMILY_L0014':lambda: r13_v111_actor_ready('guard'),
        'MS14_D14_END_PARTIAL_L0002':lambda: r13_v111_actor_ready('karo'),
        'MS14_D14_END_PARTIAL_L0004':lambda: r13_v111_actor_ready('guard'),
        'MS14_D14_END_PARTIAL_L0009':lambda: r13_v111_actor_ready('karo'),
        'MS14_D14_END_PARTIAL_L0011':lambda: r13_v111_actor_ready('karo'),
        'MS14_D14_END_PARTIAL_L0013':lambda: r13_v111_actor_ready('guard'),
    }
