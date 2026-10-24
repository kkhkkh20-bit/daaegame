# Reviewed D04–D05 source IDs in existing Ren’Py labels.


label r13_v111_day4:
    if r13_v111_value('silluk_status')=='detained_work_waiting_station':
        jump r13_v111_labor4
    jump r13_v111_somi4

label r13_v111_labor4:
    $ r13_v111_scene('MS14_D04_S01')
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('v111_labor','labor4',['daram'])
    $ r13_v111_arrive(['daram', 'resident_siluk', 'neoul'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0002']),'v111:MS14_D04_S01_L0002')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0003']),'v111:MS14_D04_S01_L0003')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0004']),'v111:MS14_D04_S01_L0004')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0005']),'v111:MS14_D04_S01_L0005')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0006']),'v111:MS14_D04_S01_L0006')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0007']),'v111:MS14_D04_S01_L0007')
    jump r13_v111_labor_sheet4

label r13_v111_labor_sheet4:
    call r13_v111_wait('labor_sheet4')
    if _return==0:
        jump r13_v111_labor_confirm4
    jump r13_v111_labor_sheet4

label r13_v111_labor_confirm4:
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0009']),'v111:MS14_D04_S01_L0009')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0010']),'v111:MS14_D04_S01_L0010')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0011']),'v111:MS14_D04_S01_L0011')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0012']),'v111:MS14_D04_S01_L0012')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0013']),'v111:MS14_D04_S01_L0013')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0014']),'v111:MS14_D04_S01_L0014')
    $ r13_v111_commit('MS14_D04_S01_L0015')
    jump r13_v111_somi4

label r13_v111_somi4:
    $ r13_v111_scene('MS14_D04_S01')
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('ms14_somi','somi4',['daram'])
    $ r13_v111_arrive(['daram', 'resident_nero', 'resident_somi'])
    $ r13_v111_score()

label r13_v111_nero_route4:
    if r13_v111_value('nero_met_day2'):
        jump r13_v111_nero_known4
    jump r13_v111_nero_new4

label r13_v111_nero_known4:
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0017']),'v111:MS14_D04_S01_L0017')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0018']),'v111:MS14_D04_S01_L0018')
    jump r13_v111_portrait_show4

label r13_v111_nero_new4:
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0020']),'v111:MS14_D04_S01_L0020')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0021']),'v111:MS14_D04_S01_L0021')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0022']),'v111:MS14_D04_S01_L0022')
    jump r13_v111_nero_help4

label r13_v111_nero_help4:
    call r13_v111_wait('nero_help4')
    if _return==0:
        jump r13_v111_nero_help_done4
    jump r13_v111_nero_help4

label r13_v111_nero_help_done4:
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0024']),'v111:MS14_D04_S01_L0024')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0025']),'v111:MS14_D04_S01_L0025')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0026']),'v111:MS14_D04_S01_L0026')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0027']),'v111:MS14_D04_S01_L0027')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0028']),'v111:MS14_D04_S01_L0028')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0029']),'v111:MS14_D04_S01_L0029')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0030']),'v111:MS14_D04_S01_L0030')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0031']),'v111:MS14_D04_S01_L0031')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0032']),'v111:MS14_D04_S01_L0032')
    $ r13_v111_commit('MS14_D04_S01_L0033')
    jump r13_v111_portrait_show4

label r13_v111_portrait_show4:
    call r13_v111_wait('portrait_show4')
    if _return==0:
        jump r13_v111_somi_talk4
    jump r13_v111_portrait_show4

label r13_v111_somi_talk4:
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0034']),'v111:MS14_D04_S01_L0034')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0035']),'v111:MS14_D04_S01_L0035')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0036']),'v111:MS14_D04_S01_L0036')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0037']),'v111:MS14_D04_S01_L0037')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0038']),'v111:MS14_D04_S01_L0038')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0039']),'v111:MS14_D04_S01_L0039')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0041']),'v111:MS14_D04_S01_L0041')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0042']),'v111:MS14_D04_S01_L0042')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0043']),'v111:MS14_D04_S01_L0043')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0044']),'v111:MS14_D04_S01_L0044')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0045']),'v111:MS14_D04_S01_L0045')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0046']),'v111:MS14_D04_S01_L0046')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0047']),'v111:MS14_D04_S01_L0047')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0048']),'v111:MS14_D04_S01_L0048')
    $ r13_v111_commit('MS14_D04_S01_L0050')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0051']),'v111:MS14_D04_S01_L0051')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0052']),'v111:MS14_D04_S01_L0052')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0053']),'v111:MS14_D04_S01_L0053')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0054']),'v111:MS14_D04_S01_L0054')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0055']),'v111:MS14_D04_S01_L0055')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0056']),'v111:MS14_D04_S01_L0056')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0057']),'v111:MS14_D04_S01_L0057')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0058']),'v111:MS14_D04_S01_L0058')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0060']),'v111:MS14_D04_S01_L0060')
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0061']),'v111:MS14_D04_S01_L0061')
    jump r13_v111_eaves4

label r13_v111_eaves4:
    $ r13_v111_scene('MS14_D04_S02')
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('square','eaves4',['daram'])
    $ r13_v111_arrive(['daram', 'resident_kongi', 'resident_tosil', 'bami'])
    $ r13_v111_score()
    # 0.20.18 (소유자 2026-10-23 C3 A안 "착한 선택 한다고 좋은 결과가 안 나오게"): 3일에 실룩을 풀어 준 판은
    # 그 밤 5번 등이 또 빈다. 그 밑에서 자던 밤이가 처마에서 내려와 울타리 옆에 있게 되고, 5일 회의 기회가 하나 준다.
    if r13_v111_value('silluk_status')=='reporting_obligation' and not r13_v111_value('bami_cold4'):
        $ r13_v111_set('bami_cold4',True)
        $ r13_v111_join(['resident_lamplighter'])
        call r13_lines(r13_nw_block('silluk_lamp4'),'nw:silluk_lamp4')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0002']),'v111:MS14_D04_S02_L0002')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0003']),'v111:MS14_D04_S02_L0003')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0004']),'v111:MS14_D04_S02_L0004')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0005']),'v111:MS14_D04_S02_L0005')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0006']),'v111:MS14_D04_S02_L0006')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0007']),'v111:MS14_D04_S02_L0007')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0009']),'v111:MS14_D04_S02_L0009')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0010']),'v111:MS14_D04_S02_L0010')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0011']),'v111:MS14_D04_S02_L0011')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0012']),'v111:MS14_D04_S02_L0012')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0013']),'v111:MS14_D04_S02_L0013')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0014']),'v111:MS14_D04_S02_L0014')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0015']),'v111:MS14_D04_S02_L0015')
    jump r13_v111_portrait_place4

label r13_v111_portrait_place4:
    call r13_v111_wait('portrait_place4')
    if _return==0:
        jump r13_v111_bami_mother4
    jump r13_v111_portrait_place4

label r13_v111_bami_mother4:
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0017']),'v111:MS14_D04_S02_L0017')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0018']),'v111:MS14_D04_S02_L0018')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0019']),'v111:MS14_D04_S02_L0019')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0020']),'v111:MS14_D04_S02_L0020')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0021']),'v111:MS14_D04_S02_L0021')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0022']),'v111:MS14_D04_S02_L0022')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0023']),'v111:MS14_D04_S02_L0023')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0024']),'v111:MS14_D04_S02_L0024')
    $ r13_v111_commit('MS14_D04_S02_L0025')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0026']),'v111:MS14_D04_S02_L0026')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0027']),'v111:MS14_D04_S02_L0027')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0028']),'v111:MS14_D04_S02_L0028')
    call r13_v111_travel('ms14_somi','visit_return4')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0030']),'v111:MS14_D04_S02_L0030')
    call r13_lines(r13_v111_lines(['MS14_D04_S02_L0031']),'v111:MS14_D04_S02_L0031')
    $ r13_v111_commit('MS14_D04_S02_L0031')
    jump r13_v111_cry4

label r13_v111_cry4:
    $ r13_v111_scene('MS14_D04_S03')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('gate','cry4',['daram'])
    $ r13_v111_arrive(['daram', 'guard', 'neoul', 'resident_badook'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0002']),'v111:MS14_D04_S03_L0002')
    jump r13_v111_look_gate4

label r13_v111_look_gate4:
    call r13_v111_wait('look_gate4')
    if _return==0:
        jump r13_v111_bite4
    jump r13_v111_look_gate4

label r13_v111_bite4:
    $ r13_v111_commit('MS14_D04_S03_L0003')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0004']),'v111:MS14_D04_S03_L0004')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0005']),'v111:MS14_D04_S03_L0005')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0006']),'v111:MS14_D04_S03_L0006')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0007']),'v111:MS14_D04_S03_L0007')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0008']),'v111:MS14_D04_S03_L0008')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0009']),'v111:MS14_D04_S03_L0009')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0010']),'v111:MS14_D04_S03_L0010')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0012']),'v111:MS14_D04_S03_L0012')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0013']),'v111:MS14_D04_S03_L0013')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0014']),'v111:MS14_D04_S03_L0014')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0015']),'v111:MS14_D04_S03_L0015')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0016']),'v111:MS14_D04_S03_L0016')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0017']),'v111:MS14_D04_S03_L0017')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0018']),'v111:MS14_D04_S03_L0018')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0019']),'v111:MS14_D04_S03_L0019')
    $ r13_v111_commit('MS14_D04_S03_L0020')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0021']),'v111:MS14_D04_S03_L0021')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0022']),'v111:MS14_D04_S03_L0022')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0023']),'v111:MS14_D04_S03_L0023')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0024']),'v111:MS14_D04_S03_L0024')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0025']),'v111:MS14_D04_S03_L0025')
    call r13_lines(r13_v111_lines(['MS14_D04_S03_L0026']),'v111:MS14_D04_S03_L0026')
    jump r13_v111_testimony4

label r13_v111_testimony4:
    $ r13_v111_scene('MS14_D04_S04')
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('ms14_guardroom','testimony4',['daram'])
    $ r13_v111_arrive(['daram', 'resident_badook', 'bami'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0002']),'v111:MS14_D04_S04_L0002')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0003']),'v111:MS14_D04_S04_L0003')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0004']),'v111:MS14_D04_S04_L0004')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0005']),'v111:MS14_D04_S04_L0005')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0006']),'v111:MS14_D04_S04_L0006')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0007']),'v111:MS14_D04_S04_L0007')
    jump r13_v111_bami_ask4

label r13_v111_bami_ask4:
    call r13_v111_wait('bami_ask4')
    if _return==0:
        jump r13_v111_bami_night4
    jump r13_v111_bami_ask4

label r13_v111_bami_night4:
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0008']),'v111:MS14_D04_S04_L0008')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0009']),'v111:MS14_D04_S04_L0009')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0010']),'v111:MS14_D04_S04_L0010')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0011']),'v111:MS14_D04_S04_L0011')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0012']),'v111:MS14_D04_S04_L0012')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0013']),'v111:MS14_D04_S04_L0013')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0014']),'v111:MS14_D04_S04_L0014')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0015']),'v111:MS14_D04_S04_L0015')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0016']),'v111:MS14_D04_S04_L0016')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0017']),'v111:MS14_D04_S04_L0017')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0018']),'v111:MS14_D04_S04_L0018')
    $ r13_v111_commit('MS14_D04_S04_L0018')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0020']),'v111:MS14_D04_S04_L0020')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0021']),'v111:MS14_D04_S04_L0021')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0022']),'v111:MS14_D04_S04_L0022')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0023']),'v111:MS14_D04_S04_L0023')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0024']),'v111:MS14_D04_S04_L0024')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0025']),'v111:MS14_D04_S04_L0025')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0026']),'v111:MS14_D04_S04_L0026')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0027']),'v111:MS14_D04_S04_L0027')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0028']),'v111:MS14_D04_S04_L0028')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0029']),'v111:MS14_D04_S04_L0029')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0030']),'v111:MS14_D04_S04_L0030')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0031']),'v111:MS14_D04_S04_L0031')
    $ r13_v111_commit('MS14_D04_S04_L0032')
    call r13_v111_travel('gate','fence4')
    jump r13_v111_inspect_gate4

label r13_v111_inspect_gate4:
    call r13_v111_wait('inspect_gate4')
    if _return==0:
        jump r13_v111_fence_seen4
    if _return==1:
        jump r13_v111_tracks_seen4
    if _return==2:
        jump r13_v111_bucket_seen4
    jump r13_v111_inspect_gate4

label r13_v111_fence_seen4:
    $ r13_v111_set('d4_fence_seen',True)
    # Audit d01-05 #11: the inspected object is described (source MS14_D04_S04_L0034).
    $ r13_field_reading=True
    call r13_lines([(None,'울타리 못에 회색 천이 걸렸다.')],'v111:fence_seen4')
    $ r13_field_reading=False
    jump r13_v111_inspection_ready4

label r13_v111_tracks_seen4:
    $ r13_v111_set('d4_tracks_seen',True)
    # Audit d01-05 #11: the inspected object is described (source MS14_D04_S04_L0034).
    $ r13_field_reading=True
    call r13_lines([(None,'눈 위에 발자국이 여러 겹 겹쳐 있다.')],'v111:tracks_seen4')
    $ r13_field_reading=False
    jump r13_v111_inspection_ready4

label r13_v111_bucket_seen4:
    $ r13_v111_set('d4_bucket_seen',True)
    # Audit d01-05 #11: the inspected object is described (source MS14_D04_S04_L0034).
    $ r13_field_reading=True
    call r13_lines([(None,'양동이가 엎어져 있다. 옆의 발자국도 겹쳐 있다.')],'v111:bucket_seen4')
    $ r13_field_reading=False
    jump r13_v111_inspection_ready4

label r13_v111_inspection_ready4:
    if all(r13_v111_value(k) for k in ['d4_fence_seen', 'd4_tracks_seen', 'd4_bucket_seen']):
        jump r13_v111_tracks_talk4
    jump r13_v111_inspect_gate4

label r13_v111_tracks_talk4:
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0035']),'v111:MS14_D04_S04_L0035')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0037']),'v111:MS14_D04_S04_L0037')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0038']),'v111:MS14_D04_S04_L0038')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0039']),'v111:MS14_D04_S04_L0039')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0040']),'v111:MS14_D04_S04_L0040')
    jump r13_v111_collect4

label r13_v111_collect4:
    call r13_v111_wait('collect4')
    if _return==0:
        jump r13_v111_cloth4
    jump r13_v111_collect4

label r13_v111_cloth4:
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0042']),'v111:MS14_D04_S04_L0042')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0043']),'v111:MS14_D04_S04_L0043')
    $ r13_v111_commit('MS14_D04_S04_L0044')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0045']),'v111:MS14_D04_S04_L0045')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0046']),'v111:MS14_D04_S04_L0046')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0047']),'v111:MS14_D04_S04_L0047')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0048']),'v111:MS14_D04_S04_L0048')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0049']),'v111:MS14_D04_S04_L0049')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0050']),'v111:MS14_D04_S04_L0050')
    call r13_v111_travel('dining','night_diner4')
    $ r13_v111_commit('MS14_D04_S04_L0051')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0052']),'v111:MS14_D04_S04_L0052')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0053']),'v111:MS14_D04_S04_L0053')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0054']),'v111:MS14_D04_S04_L0054')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0055']),'v111:MS14_D04_S04_L0055')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0056']),'v111:MS14_D04_S04_L0056')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0057']),'v111:MS14_D04_S04_L0057')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0058']),'v111:MS14_D04_S04_L0058')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0059']),'v111:MS14_D04_S04_L0059')
    call r13_v111_piko_sketch4
    call r13_v111_travel('square','night_lamp4')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0061']),'v111:MS14_D04_S04_L0061')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0062']),'v111:MS14_D04_S04_L0062')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0063']),'v111:MS14_D04_S04_L0063')
    call r13_lines(r13_v111_lines(['MS14_D04_S04_L0064']),'v111:MS14_D04_S04_L0064')
    call r13_v111_travel('room13','bed4')
    jump r13_v111_sleep4

# 2026-10-24 지시서 01: 이 레이블은 4일 밤에 불린다. 서랍 자리표(dev/build_evidence_drawer.py)는 파일 안의
# 바로 앞 장면 표시로 자리를 정하므로, 5일 장면 뒤에 두면 4일에 얻은 그림이 5일 저녁 묶음으로 잘못 들어간다.
label r13_v111_piko_sketch4:
    # 0.20.18 연쇄 P1 (CHAIN_DESIGN.md): 2일에 살린 피코가 4일 저녁 처마 옆에서 본 것을 그려 온다.
    # 피코는 3일부터 진료소에 머물므로, 국을 받으러 온 이 장면에서만 식당에 세웠다가 되돌린다.
    if r13_v111_value('piko_alive')!=True or r13_v111_owned('NW_PIKO_SKETCH4'):
        return
    $ v111_people_before=list(room13["v111"].get("people") or [])
    $ r13_v111_set('piko.location','dining')
    $ r13_v111_join(['resident_piko'])
    call r13_lines(r13_nw_block('piko_sketch4'),'nw:piko_sketch4')
    $ r13_nw_acquire("NW_PIKO_SKETCH4")
    $ r13_v111_set('piko.location','clinic')
    $ r13_v111_arrive(v111_people_before)
    return

label r13_v111_sleep4:
    call r13_v111_wait('sleep4')
    if _return==0:
        jump r13_v111_morning5
    jump r13_v111_sleep4

label r13_v111_morning5:
    $ r13_v111_set("day",5)
    jump r13_v111_somi5

label r13_v111_somi5:
    $ r13_v111_scene('MS14_D05_S01')
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('ms14_somi','somi5',['daram'])
    $ r13_v111_arrive(['daram', 'resident_nero', 'resident_somi', 'resident_musoe'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0002']),'v111:MS14_D05_S01_L0002')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0003']),'v111:MS14_D05_S01_L0003')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0004']),'v111:MS14_D05_S01_L0004')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0005']),'v111:MS14_D05_S01_L0005')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0006']),'v111:MS14_D05_S01_L0006')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0007']),'v111:MS14_D05_S01_L0007')
    call r13_v111_travel('ms14_somi_inside','inside5')
    $ r13_v111_commit('MS14_D05_S01_L0008')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0009']),'v111:MS14_D05_S01_L0009')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0010']),'v111:MS14_D05_S01_L0010')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0011']),'v111:MS14_D05_S01_L0011')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0012']),'v111:MS14_D05_S01_L0012')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0013']),'v111:MS14_D05_S01_L0013')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0015']),'v111:MS14_D05_S01_L0015')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0016']),'v111:MS14_D05_S01_L0016')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0017']),'v111:MS14_D05_S01_L0017')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0018']),'v111:MS14_D05_S01_L0018')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0019']),'v111:MS14_D05_S01_L0019')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0020']),'v111:MS14_D05_S01_L0020')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0021']),'v111:MS14_D05_S01_L0021')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0022']),'v111:MS14_D05_S01_L0022')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0023']),'v111:MS14_D05_S01_L0023')
    call r13_lines(r13_v111_lines(['MS14_D05_S01_L0024']),'v111:MS14_D05_S01_L0024')
    $ r13_v111_commit('MS14_D05_S01_L0024')
    $ r13_nw_acquire("NW_MUSOE_DEEP")
    jump r13_v111_wait_cloth5

label r13_v111_wait_cloth5:
    $ r13_v111_scene('MS14_D05_S02')
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('ms14_somi_inside','wait_cloth5',['daram'])
    $ r13_v111_arrive(['daram', 'resident_nero', 'resident_somi', 'resident_musoe'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0002']),'v111:MS14_D05_S02_L0002')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0003']),'v111:MS14_D05_S02_L0003')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0004']),'v111:MS14_D05_S02_L0004')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0006']),'v111:MS14_D05_S02_L0006')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0007']),'v111:MS14_D05_S02_L0007')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0008']),'v111:MS14_D05_S02_L0008')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0009']),'v111:MS14_D05_S02_L0009')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0010']),'v111:MS14_D05_S02_L0010')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0011']),'v111:MS14_D05_S02_L0011')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0012']),'v111:MS14_D05_S02_L0012')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0013']),'v111:MS14_D05_S02_L0013')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0014']),'v111:MS14_D05_S02_L0014')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0015']),'v111:MS14_D05_S02_L0015')
    jump r13_v111_compare_cloth5

label r13_v111_compare_cloth5:
    call r13_v111_wait('compare_cloth5')
    if _return==0:
        jump r13_v111_cloth_match5
    jump r13_v111_compare_cloth5

label r13_v111_cloth_match5:
    $ r13_v111_commit('MS14_D05_S02_L0016')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0017']),'v111:MS14_D05_S02_L0017')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0018']),'v111:MS14_D05_S02_L0018')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0019']),'v111:MS14_D05_S02_L0019')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0020']),'v111:MS14_D05_S02_L0020')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0021']),'v111:MS14_D05_S02_L0021')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0022']),'v111:MS14_D05_S02_L0022')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0023']),'v111:MS14_D05_S02_L0023')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0024']),'v111:MS14_D05_S02_L0024')
    $ r13_v111_commit('MS14_D05_S02_L0025')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0026']),'v111:MS14_D05_S02_L0026')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0027']),'v111:MS14_D05_S02_L0027')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0028']),'v111:MS14_D05_S02_L0028')
    call r13_v111_travel('clinic','clinic_handoff5')
    call r13_lines(r13_v111_lines(['MS14_D05_S02_L0030']),'v111:MS14_D05_S02_L0030')
    $ r13_v111_commit('MS14_D05_S02_L0031')
    call r13_lines(r13_nw_block('clinic_next5'),'nw:clinic_next5')
    jump r13_v111_hearing5

label r13_v111_hearing5:
    $ r13_v111_scene('MS14_D05_S03')
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('gate','hearing5',['daram'])
    $ r13_v111_arrive(['daram', 'guard', 'neoul', 'resident_nero', 'resident_badook', 'resident_kongi'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0003']),'v111:MS14_D05_S03_L0003')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0005']),'v111:MS14_D05_S03_L0005')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0006']),'v111:MS14_D05_S03_L0006')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0007']),'v111:MS14_D05_S03_L0007')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0009']),'v111:MS14_D05_S03_L0009')
    jump r13_v111_proof5

label r13_v111_proof5:
    # C3 A안: 밤이가 울타리 옆에 있었던 판은 너울이 한 수를 더 쥔다(기회 하나 감소, 한 번만).
    if r13_v111_value('bami_cold4') and not r13_v111_value('gate_post_cold_cost'):
        $ r13_v111_set('gate_post_cold_cost',True)
        $ r13_v111_set('tries:gate_post',(r13_v111_value('tries:gate_post') or 0)+1)
    call r13_v111_proof("밤이 혐의의 근거를 확인한다",["E20","E22","E23","E24"],"r13_v111_bami_clear5","r13_v111_wrong5","r13_v111_hint5")
    jump expression _return

label r13_v111_wrong5:
    if r13_nw_retry("gate_post",["E20","E22","E23","E24"],"돌목이 고개를 젓는다. 천과 겉옷, 진술을 함께 놓아야 한다."):
        call r13_lines(r13_v111_lines(["MS14_D05_S03_L0038","MS14_D05_S03_L0039"]),"v111:MS14_D05_S03_L0038")
        jump r13_v111_proof5
    $ r13_nw_meeting_end("gate_post","lose")
    $ r13_nw_list("bami","gate_post_lose")
    $ r13_v111_set("bami_status","listed")
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0038']),'v111:MS14_D05_S03_L0038')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0039']),'v111:MS14_D05_S03_L0039')
    jump r13_v111_warning5

label r13_v111_hint5:
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0040']),'v111:MS14_D05_S03_L0040')
    jump r13_v111_proof5

label r13_v111_bami_clear5:
    $ r13_nw_meeting_end("gate_post","win")
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0013']),'v111:MS14_D05_S03_L0013')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0014']),'v111:MS14_D05_S03_L0014')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0015']),'v111:MS14_D05_S03_L0015')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0016']),'v111:MS14_D05_S03_L0016')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0017']),'v111:MS14_D05_S03_L0017')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0018']),'v111:MS14_D05_S03_L0018')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0019']),'v111:MS14_D05_S03_L0019')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0021']),'v111:MS14_D05_S03_L0021')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0022']),'v111:MS14_D05_S03_L0022')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0023']),'v111:MS14_D05_S03_L0023')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0024']),'v111:MS14_D05_S03_L0024')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0025']),'v111:MS14_D05_S03_L0025')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0026']),'v111:MS14_D05_S03_L0026')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0028']),'v111:MS14_D05_S03_L0028')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0029']),'v111:MS14_D05_S03_L0029')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0030']),'v111:MS14_D05_S03_L0030')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0031']),'v111:MS14_D05_S03_L0031')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0032']),'v111:MS14_D05_S03_L0032')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0033']),'v111:MS14_D05_S03_L0033')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0034']),'v111:MS14_D05_S03_L0034')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0035']),'v111:MS14_D05_S03_L0035')
    call r13_lines(r13_v111_lines(['MS14_D05_S03_L0036']),'v111:MS14_D05_S03_L0036')
    $ r13_v111_commit('MS14_D05_S03_L0037')
    jump r13_v111_warning5

label r13_v111_warning5:
    $ r13_v111_scene('MS14_D05_S04')
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('gate','warning5',['daram'])
    $ r13_v111_arrive(['daram', 'resident_lamplighter'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0002']),'v111:MS14_D05_S04_L0002')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0003']),'v111:MS14_D05_S04_L0003')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0004']),'v111:MS14_D05_S04_L0004')
    jump r13_v111_envelope5

label r13_v111_envelope5:
    call r13_v111_wait('envelope5')
    if _return==0:
        jump r13_v111_warning_read5
    jump r13_v111_envelope5

label r13_v111_warning_read5:
    $ r13_v111_commit('MS14_D05_S04_L0005')
    call r13_lines([(None,'“당신과 다람이를 부른 적 없어.',dict(no_lead=True,v111_silence_after=True))],'v111:MS14_D05_S04_L0006:first')
    $ renpy.music.stop(fadeout=0.0 if renpy.is_skipping() else .15)
    $ room13["v111"]["music_hold"]=room13["v111"]["scene"]
    call r13_lines([(None,'그 편지는 내가 쓴 게 아니야. 나를 찾는 곳이나 이 편지 이야기를 여관에 말하지 마. 당장 만나러 내려갈 수 없어. 초롱에게 답을 맡겨 줘. 먹을 것과 마른 천이 필요해. 다람이 손은 괜찮아? 겨울이면 또 트는데.”',dict(no_lead=True))],'v111:MS14_D05_S04_L0006:rest')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0007']),'v111:MS14_D05_S04_L0007')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0008']),'v111:MS14_D05_S04_L0008')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0009']),'v111:MS14_D05_S04_L0009')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0010']),'v111:MS14_D05_S04_L0010')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0011']),'v111:MS14_D05_S04_L0011')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0012']),'v111:MS14_D05_S04_L0012')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0013']),'v111:MS14_D05_S04_L0013')
    jump r13_v111_warning_compare5

label r13_v111_warning_compare5:
    call r13_v111_proof("두 편지의 초대를 대조한다",["E01","E27"],"r13_v111_warning_compared5","r13_v111_warning_retry5")
    jump expression _return

label r13_v111_warning_retry5:
    # 0.20.4 (audit d01-05 B): a wrong pair is not a meeting; say so and choose again.
    call r13_lines(r13_nw_block('compare_retry'),'nw:compare_retry:warning')
    jump r13_v111_warning_compare5

label r13_v111_warning_compared5:
    $ r13_v111_commit('MS14_D05_S04_L0014')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0015']),'v111:MS14_D05_S04_L0015')
    menu:
        "첫날 기록을 다시 본다":
            call r13_v111_review5
        "답장을 쓴다":
            pass
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0018']),'v111:MS14_D05_S04_L0018')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0019']),'v111:MS14_D05_S04_L0019')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0020']),'v111:MS14_D05_S04_L0020')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0021']),'v111:MS14_D05_S04_L0021')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0022']),'v111:MS14_D05_S04_L0022')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0023']),'v111:MS14_D05_S04_L0023')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0024']),'v111:MS14_D05_S04_L0024')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0025']),'v111:MS14_D05_S04_L0025')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0026']),'v111:MS14_D05_S04_L0026')
    $ r13_v111_commit('MS14_D05_S04_L0027')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0028']),'v111:MS14_D05_S04_L0028')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0029']),'v111:MS14_D05_S04_L0029')
    jump r13_v111_reply_handoff5

label r13_v111_reply_handoff5:
    call r13_v111_wait('reply_handoff5')
    if _return==0:
        jump r13_v111_reply_done5
    jump r13_v111_reply_handoff5

label r13_v111_reply_done5:
    $ r13_v111_commit('MS14_D05_S04_L9501')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L9502']),'v111:MS14_D05_S04_L9502')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L9503']),'v111:MS14_D05_S04_L9503')
    jump r13_v111_night5

label r13_v111_review5:
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0017']),'v111:MS14_D05_S04_L0017')
    return

label r13_v111_night5:
    $ r13_v111_scene('MS14_D05_S05')
    $ r13_edit(period=2)
    $ room13["v111"]["people"]=[]
    call r13_v111_travel('ms14_somi_inside','night5',['daram'])
    $ r13_v111_arrive(['daram', 'resident_somi', 'resident_musoe', 'resident_nero', 'resident_badook'])
    $ r13_v111_score()
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0002']),'v111:MS14_D05_S05_L0002')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0003']),'v111:MS14_D05_S05_L0003')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0005']),'v111:MS14_D05_S05_L0005')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0006']),'v111:MS14_D05_S05_L0006')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0007']),'v111:MS14_D05_S05_L0007')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0008']),'v111:MS14_D05_S05_L0008')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0009']),'v111:MS14_D05_S05_L0009')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0010']),'v111:MS14_D05_S05_L0010')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0011']),'v111:MS14_D05_S05_L0011')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0012']),'v111:MS14_D05_S05_L0012')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0013']),'v111:MS14_D05_S05_L0013')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0014']),'v111:MS14_D05_S05_L0014')
    $ r13_v111_commit('MS14_D05_S05_L0014')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0015']),'v111:MS14_D05_S05_L0015')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0016']),'v111:MS14_D05_S05_L0016')
    call r13_v111_travel('dining','diner5')
    # 2026-10-24 행동 검수(소유자 결정 4, 탈출 축): 3일에 톡에게 쇠 토막 이야기를 들은 판은 식당에 까로가 있다.
    if R13_NW_WHEN["tok_freed3"]() and r13_v111_person_alive("karo"):
        $ r13_v111_join(['karo'])
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0019']),'v111:MS14_D05_S05_L0019')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0020']),'v111:MS14_D05_S05_L0020')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0021']),'v111:MS14_D05_S05_L0021')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0022']),'v111:MS14_D05_S05_L0022')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0023']),'v111:MS14_D05_S05_L0023')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0024']),'v111:MS14_D05_S05_L0024')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0025']),'v111:MS14_D05_S05_L0025')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0026']),'v111:MS14_D05_S05_L0026')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L9501']),'v111:MS14_D05_S05_L9501')
    $ r13_v111_commit('MS14_D05_S05_L9502')
    call r13_v111_travel('inn','lobby5')
    $ r13_v111_commit('MS14_D05_S05_L0027')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0028']),'v111:MS14_D05_S05_L0028')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0029']),'v111:MS14_D05_S05_L0029')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0030']),'v111:MS14_D05_S05_L0030')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0031']),'v111:MS14_D05_S05_L0031')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0032']),'v111:MS14_D05_S05_L0032')
    call r13_v111_travel('hall','hall5')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0034']),'v111:MS14_D05_S05_L0034')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0035']),'v111:MS14_D05_S05_L0035')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0037']),'v111:MS14_D05_S05_L0037')
    call r13_v111_travel('room13','lock5')
    jump r13_v111_lock_check5

label r13_v111_lock_check5:
    call r13_v111_wait('lock_check5')
    if _return==0:
        jump r13_v111_safety5
    jump r13_v111_lock_check5

label r13_v111_safety5:
    $ r13_v111_commit('MS14_D05_S05_L0038')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0039']),'v111:MS14_D05_S05_L0039')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0040']),'v111:MS14_D05_S05_L0040')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0041']),'v111:MS14_D05_S05_L0041')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0042']),'v111:MS14_D05_S05_L0042')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0043']),'v111:MS14_D05_S05_L0043')

label r13_v111_blankets5:
    if r13_v111_value('carried_dry_blankets')==2:
        jump r13_v111_packed5
    jump r13_v111_empty_bag5

label r13_v111_packed5:
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0045']),'v111:MS14_D05_S05_L0045')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0046']),'v111:MS14_D05_S05_L0046')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0047']),'v111:MS14_D05_S05_L0047')
    jump r13_v111_last5

label r13_v111_empty_bag5:
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0049']),'v111:MS14_D05_S05_L0049')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0050']),'v111:MS14_D05_S05_L0050')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0051']),'v111:MS14_D05_S05_L0051')
    jump r13_v111_last5

label r13_v111_last5:
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0053']),'v111:MS14_D05_S05_L0053')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0054']),'v111:MS14_D05_S05_L0054')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0055']),'v111:MS14_D05_S05_L0055')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0056']),'v111:MS14_D05_S05_L0056')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0057']),'v111:MS14_D05_S05_L0057')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0058']),'v111:MS14_D05_S05_L0058')
    $ r13_v111_commit('MS14_D05_S05_L0059')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0060']),'v111:MS14_D05_S05_L0060')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0061']),'v111:MS14_D05_S05_L0061')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0062']),'v111:MS14_D05_S05_L0062')
    call r13_lines(r13_v111_lines(['MS14_D05_S05_L0063']),'v111:MS14_D05_S05_L0063')
    jump r13_v111_sleep5

label r13_v111_sleep5:
    call r13_v111_wait('sleep5')
    if _return==0:
        jump r13_v111_morning6
    jump r13_v111_sleep5

label r13_v111_morning6:
    $ r13_v111_set("day",6)
    jump r13_v111_day6

