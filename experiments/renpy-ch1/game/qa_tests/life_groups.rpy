# Actual engine gate for the integration owner. Never claim these passed without SDK output.
# Pending-art rows may be tested locally, but are never enabled by the shipped game.
label r13_qa_life_groups(key):
    call r13_qa_setup(2,[],['-gates'])
    $ r13_life_field_active=True
    $ r13_qa_group=next(g for g in R13_LIFE_GROUPS if g['id']==key)
    $ r13_qa_group['status']='approved'
    $ room13.update(day=r13_qa_group['days'][0],period=r13_qa_group['periods'][0],location=r13_qa_group['location'])
    $ room13['flags']=list(set(room13['flags'])|set(r13_qa_group['need_flags']))
    call r13_scene(R13_PLACES[room13['location']][1],R13_PLACES[room13['location']][0],'calm')
    $ r13_world_cameras[room13['location']]=520 if key=='school_play' else 0
    $ r13_qa_group_before=winter_copy.deepcopy(room13)
    while True:
        call screen r13_hub
        $ r13_choice=_return
        call r13_life_field_person_dispatch
        $ assert room13==r13_qa_group_before, 'Life group changed world state'

testcase life_group_workshop:
    run Jump('r13_qa_life_workshop')
    pause 1.0
    screenshot "life-workshop-existing-art-candidate.png"
    click "함께 부품 손질"
    pause .3
    screenshot "life-workshop-dialogue.png"
    click "그만 듣기"
    pause .3
    assert eval (room13==r13_qa_group_before)

label r13_qa_life_workshop:
    call r13_qa_life_groups('workshop_pair')
    return

testcase life_group_inn:
    run Jump('r13_qa_life_inn')
    pause 1.0
    screenshot "life-inn-existing-art-candidate.png"
    click "함께 바느질"
    pause .3
    screenshot "life-inn-dialogue.png"
    click "그만 듣기"
    pause .3
    assert eval (room13==r13_qa_group_before)

label r13_qa_life_inn:
    call r13_qa_life_groups('inn_mending')
    return

testcase life_group_school:
    run Jump('r13_qa_life_school')
    pause 1.0
    screenshot "life-school-play.png"
    click "깜이"
    pause .3
    screenshot "life-school-kkam-individual.png"
    click "돌아가기"
    pause .3
    click "몽이"
    pause .3
    screenshot "life-school-mong-individual.png"
    click "돌아가기"
    pause .3
    click "방울"
    pause .3
    screenshot "life-school-bang-individual.png"
    click "돌아가기"
    pause .3
    click "아이들과 함께 이야기"
    pause .3
    screenshot "life-school-dialogue.png"
    $ renpy.save("qa-life-group","qa")
    click "계속 듣기"
    run Function(renpy.load,"qa-life-group")
    pause .5
    assert eval (room13==r13_qa_group_before)
    assert eval (renpy.get_screen("r13_life_group_conversation").scope["line_index"]==0)
    click "계속 듣기"
    click "계속 듣기"
    click "계속 듣기"
    click "돌아가기"
    pause .3
    assert eval (room13==r13_qa_group_before)

label r13_qa_life_school:
    call r13_qa_life_groups('school_play')
    return
