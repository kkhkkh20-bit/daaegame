# 2026-10-25 승인된 3번 등 절도 미수판. 도난판의 증거를 재사용하지 않는다.
label r13_lamp_prep2:
    call r13_v111_wait('lamp_prep2')
    if _return==0:
        $ r13_v111_set('lamp_prep_done2',True)
        return
    if _return==1:
        call r13_lines(r13_nw_block('la_cord2'),'nw:la_cord2')
        $ r13_v111_set('lamp_cord2',True)
    elif _return==2:
        call r13_lines(r13_nw_block('la_latch2'),'nw:la_latch2')
        $ r13_v111_set('lamp_latch_seen2',True)
    elif _return==3 and r13_v111_value('lamp_cord2') and r13_v111_value('lamp_latch_seen2'):
        call r13_lines(r13_nw_block('la_bind2'),'nw:la_bind2')
        $ r13_v111_set('lamp_bound2',True)
    jump r13_lamp_prep2

label r13_lamp_attempt3:
    $ r13_edit(period=0)
    $ r13_v111_set('piko_alive',True)
    $ r13_v111_set('piko.location','square')
    $ r13_v111_scene('MS14_D03_S01')
    call r13_v111_travel('square','lamp_attempt_morning3',direct=True)
    $ r13_v111_arrive(['resident_piko','resident_lamplighter','resident_tok','daram'])
    call r13_lines(r13_nw_block('la_morning3'),'nw:la_morning3')
    $ r13_v111_apply('lamp_attempt:portrait3',[dict(op='set',field='portrait',value='complete'),dict(op='acquire',key='E09',variant='complete')])
label r13_lamp_attempt_field3:
    call r13_v111_wait('lamp_attempt_field3')
    if _return==0:
        jump r13_lamp_attempt_open3
    elif _return==1:
        call r13_lines(r13_nw_block('la_field3'),'nw:la_field3')
        $ r13_nw_acquire("NW_LA_CHECK")
        $ r13_nw_acquire("NW_LA_FIELD")
        $ r13_v111_set('lamp_field_done3',True)
    elif _return==2:
        call r13_lines(r13_nw_block('la_knife3'),'nw:la_knife3')
        $ r13_nw_acquire("NW_LA_KNIFE")
        $ r13_v111_set('lamp_knife_done3',True)
    elif _return==3:
        call r13_lines(r13_nw_block('la_store3'),'nw:la_store3')
        $ r13_nw_acquire("NW_LA_OFFER")
        $ r13_nw_acquire("NW_INNER_PRICE")
        $ r13_nw_acquire("NW_KEEPER_DATE")
        $ r13_v111_set('lamp_store_done3',True)
    jump r13_lamp_attempt_field3

label r13_lamp_attempt_open3:
    $ r13_edit(period=1)
    $ r13_v111_set('silluk.children.location','workshop_with_buri')
    $ r13_v111_scene('MS14_D03_S05')
    call r13_v111_travel('workshop','lamp_attempt_open3',direct=True)
    $ r13_v111_arrive(['resident_tok','resident_lamplighter','resident_siluk','neoul','daram'])
    call r13_lines(r13_nw_block('la_open3'),'nw:la_open3')
    jump r13_lamp_attempt_repair3

label r13_lamp_attempt_repair3:
    $ r13_meeting_checkpoint('lamp')
    call r13_v111_proof('수리 뒤 새로 생긴 파손을 가린다',['NW_LA_CHECK','NW_LA_FIELD'],'r13_lamp_attempt_repair_ok3','r13_lamp_attempt_wrong3',None)
    jump expression _return
label r13_lamp_attempt_repair_ok3:
    $ r13_v111_set('repair_opening_separated',True)
    call r13_lines(r13_nw_block('la_repair_ok3'),'nw:la_repair_ok3')
    jump r13_lamp_attempt_final3
label r13_lamp_attempt_wrong3:
    call r13_lines(r13_nw_block('la_wrong3'),'nw:la_wrong3')
    if r13_nw_retry('lamp'):
        jump r13_lamp_attempt_repair3
    $ r13_nw_meeting_end('lamp','lose')
    $ r13_nw_list('resident_tok','lamp_lose')
    call r13_lines(r13_nw_block('la_lose3'),'nw:la_lose3')
    jump r13_v111_custody_choice
label r13_lamp_attempt_final3:
    call r13_v111_proof('남아 있는 돌과 칼의 사용을 연결한다',['NW_LA_CHECK','NW_LA_FIELD','NW_LA_KNIFE'],'r13_lamp_attempt_win3','r13_lamp_attempt_partial3',None)
    jump expression _return
label r13_lamp_attempt_partial3:
    call r13_lines(r13_nw_block('la_wrong3'),'nw:la_wrong3')
    if r13_nw_retry('lamp'):
        jump r13_lamp_attempt_final3
    $ r13_nw_meeting_end('lamp','partial')
    call r13_lines(r13_nw_block('la_partial3'),'nw:la_partial3')
    jump r13_v111_custody_choice
label r13_lamp_attempt_win3:
    call r13_lines(r13_nw_block('la_final3'),'nw:la_final3')
    $ r13_v111_set('outer_latch_claim_refuted',True)
    $ r13_nw_meeting_end('lamp','win')
    jump r13_v111_custody_choice

label r13_lamp_attempt_after3:
    call r13_lines(r13_nw_block('tok_axle3'),'nw:tok_axle3')
    $ r13_edit(period=2)
    call r13_v111_travel('square','lamp_attempt_after3',direct=True)
    $ r13_v111_arrive(['resident_lamplighter','resident_piko','daram'])
    call r13_lines(r13_nw_block('la_after3'),'nw:la_after3')
    $ r13_v111_set('stone_warm_felt3',True)
    $ r13_v111_set('piko.location','clinic')
    jump r13_v111_somi_lead
