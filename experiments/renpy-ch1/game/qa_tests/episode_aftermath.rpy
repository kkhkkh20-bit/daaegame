# Explicit art tour; production branch selection is independently covered in unit/browser QA.
label r13_qa_aftermath_gallery:
    call r13_qa_setup(11,[],("+ep",))
    $ r13_edit(daram_state="with_dad")
    $ _af_qa_before=repr(room13)
    $ r13_aftermath_frames=[dict(frame,id=key) for key,frame in R13_AFTERMATH.items()]
    $ r13_aftermath_index=0
    $ r13_aftermath_active=True
    while r13_aftermath_index<len(r13_aftermath_frames):
        $ r13_aftermath_episode=r13_aftermath_frames[r13_aftermath_index]["episode"]
        call screen r13_episode_aftermath_view
        $ r13_aftermath_index+=1
    $ r13_aftermath_active=False
    $ renpy.store.qa_aftermath_readonly=repr(room13)==_af_qa_before
    return

testcase episode_aftermath_gallery:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_aftermath_gallery")
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==0)
    screenshot "af_01_piko_saved.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==1)
    screenshot "af_02_piko_dead.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==2)
    screenshot "af_03_tok_free.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==3)
    screenshot "af_04_tok_detained.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==4)
    screenshot "af_05_siluk_debt.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==5)
    screenshot "af_06_siluk_handed.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==6)
    screenshot "af_07_madam_open.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==7)
    screenshot "af_08_musoe_farewell.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==8)
    screenshot "af_09_musoe_clinic.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==9)
    screenshot "af_10_musoe_shoes.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==10)
    screenshot "af_11_somi_silent.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==11)
    screenshot "af_12_clinic_empty.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==12)
    screenshot "af_13_bami_safe.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==13)
    screenshot "af_14_bami_taken.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==14)
    screenshot "af_15_kkomi_saved.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==15)
    screenshot "af_16_kkomi_dead.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==16)
    screenshot "af_17_bori_adopts.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==17)
    screenshot "af_18_shed_empty.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==18)
    screenshot "af_19_kkomi_alone.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==19)
    screenshot "af_20_bori_taken.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==20)
    screenshot "af_21_nabi_children.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==21)
    screenshot "af_22_chorong_safe.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==22)
    screenshot "af_23_chorong_dead.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==23)
    screenshot "af_24_ttadak_hurt.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==24)
    screenshot "af_25_ttadak_dead.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==25)
    screenshot "af_26_ttadak_safe.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==26)
    screenshot "af_27_owl_hat.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==27)
    screenshot "af_28_granny_goodbye.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==28)
    screenshot "af_29_soup_alive.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==29)
    screenshot "af_30_soup_three.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==30)
    screenshot "af_31_soup_empty.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==31)
    screenshot "af_32_bori_shoe.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==32)
    screenshot "af_33_dodam_sick.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==33)
    screenshot "af_34_bori_four.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==34)
    screenshot "af_35_mom_portrait.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==35)
    screenshot "af_36_cart_safe.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==36)
    screenshot "af_37_cart_left.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==37)
    screenshot "af_38_cart_family.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==38)
    screenshot "af_39_cart_unrest.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==39)
    screenshot "af_40_guldol_free.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==40)
    screenshot "af_41_badook_hurt.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==41)
    screenshot "af_42_badook_dead.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==42)
    screenshot "af_43_cart_skipped.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==43)
    screenshot "af_44_pandol_family.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==44)
    screenshot "af_45_order_tomorrow.png"
    click pos (640,600)
    pause until screen "r13_episode_aftermath_view" timeout 30
    pause .8
    assert eval (r13_aftermath_index==45)
    screenshot "af_46_chorong_hurt.png"
    click pos (640,600)
    pause until eval (not r13_aftermath_active) timeout 30
    assert eval (qa_aftermath_readonly)
