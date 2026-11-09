# 시작 시점은 직접 준비한다. 이후 버튼·페이지·선택·대화는 실제 GUI로 검수한다.
# 공통 준비/보고 helper는 runtime146_sweep.rpy와 함께 로드한다.
init python:
    def qa_field146_prepare(kind):
        qa146_begin()
        if kind in ('companion','journal'):
            qa146_prepare(2,1,'inn',gate='afternoon2',scene='MS14_D02_S04')
        elif kind=='bundle':
            qa146_prepare(1,0,'room13',gate='bundle_open',scene='MS14_D01_S05',
                          values={'hidden_base:paper':None})
        elif kind=='late_piko':
            # 나비의 실제 일과 장소를 쓴다. oldpeople/physical만 적은 inn은 visible을 보장하지 않는다.
            qa146_prepare(4,1,'dining',gate='sleep4',scene='MS14_D04_S01',
                values={'piko_alive':False,'portrait':'unfinished','E09.variant':'unfinished',
                        'location:nabi':'dining','busy:nabi':None,'piko_news3:nabi':False},
                evidence=['E09'],flags=['piko_dead','v111:applied:MS14_D03_S01_L0021'],people=['nabi'])
        elif kind=='late_piko7':
            # helpers.rpy init999의 자료함 stub을 쓰지 않고 제품의 실제 화면을 누른다.
            renpy.display.screen.screens[('r13_book',None)]=QA_FIELD146_REAL_BOOK
            qa146_prepare(7,1,'dining',gate='free_day7',scene='MS14_D07_S02',
                values={'piko_alive':False,'portrait':'unfinished','E09.variant':'unfinished',
                        'location:nabi':'dining','busy:nabi':None,'piko_news3:nabi':False,
                        'D06_S03P_empty_fire_completed':True,'D06_S03_main_completed':False,
                        'FIRE_EVACUATED':True,'warehouse_children_school_handover':4,'KKOMI_ALIVE':True,
                        'meeting:fire':'win','D07_S02_handover_completed':True,
                        'D07_S02_message_completed':True,'route7':'uncommitted'},
                evidence=['E09','E06_CONTACT'],flags=['piko_dead','v111:applied:MS14_D03_S01_L0021'],people=['nabi'])
        elif kind=='day7_seam':
            qa146_prepare(7,1,'inn',gate='free_day7',scene='MS14_D07_S02',
                values={'piko_alive':False,'portrait':'unfinished','E09.variant':'unfinished',
                        'location:nabi':'dining','busy:nabi':None,
                        'D06_S03P_empty_fire_completed':True,'D06_S03_main_completed':False,
                        'FIRE_EVACUATED':True,'warehouse_children_school_handover':4,'KKOMI_ALIVE':True,
                        'meeting:fire':'win','D07_S02_handover_completed':True,
                        'D07_S02_message_completed':True,'route7':'uncommitted'},
                evidence=['E09','E06_CONTACT'],flags=['piko_dead','v111:applied:MS14_D03_S01_L0021'])
            n=winter_copy.deepcopy(store.room13)
            n['v111']['sidequests']={'seam':dict(status='accepted',accepted_day=2,accepted_period=1)}
            store.room13=n
        r13_v111_arrive(['nabi','daram'] if kind in ('late_piko','late_piko7') else ['daram'])
        if kind=='journal':
            n=winter_copy.deepcopy(store.room13)
            n['v111']['sidequests']={key:dict(status='accepted',accepted_day=2,accepted_period=1) for key in R13_SIDEQUESTS}
            store.room13=n
        renpy.test.field146_before=qa146_quest_projection()
        renpy.test.field146_result=None
        renpy.test.field146_kind=kind

    def qa_field146_journal_page():
        screen=renpy.get_screen('r13_sidequest_journal146')
        return screen.scope.get('page') if screen else None

    def qa_field146_object_point(key):
        rect=ROOM13['objects'][room13['location']][key]['rect']
        return r13_world_to_screen((rect[0]+rect[2]//2,rect[1]+rect[3]//2))

    def qa_field146_journal_mode(touch):
        if not hasattr(renpy.test,'field146_type_before'):
            renpy.test.field146_type_before=(tuple(config.variants),persistent.room13_large_text,persistent.room13_text_small)
        config.variants=(['touch'] if touch else [])+['pc',None]
        persistent.room13_large_text=touch
        persistent.room13_text_small=False
        renpy.restart_interaction()

    def qa_field146_restore_mode():
        variants,large,small=renpy.test.field146_type_before
        config.variants=list(variants)
        persistent.room13_large_text=large
        persistent.room13_text_small=small
        del renpy.test.field146_type_before
        renpy.restart_interaction()

    def qa_field146_record(name,extra=None):
        rows=getattr(renpy.test,'field146_log',[])
        rows.append(dict(name=name,prepared_kind=renpy.test.field146_kind,day=room13['day'],
                         period=room13['period'],place=room13['location'],extra=extra))
        renpy.test.field146_log=rows
        qa146_output('field-gui.json',dict(scope='직접 준비한 장면 이후 실제 GUI 입력. 자연 플레이 도달성 증거와 구분.',checks=rows))

    def qa_field146_diagnostics(name):
        person='nabi'
        qa146_output('field-diagnostics-'+name+'.json',dict(result=getattr(renpy.test,'field146_result',None),
            day=room13['day'],place=room13['location'],gate=room13['v111']['gate'],
            people=room13['v111'].get('people'),visible=list(r13_visible_people()),
            nabi_where=r13_where(person),nabi_physical=r13_v111_value('location:'+person),
            nabi_busy=r13_v111_value('busy:'+person),nabi_actor_ready=r13_v111_actor_ready(person),
            piko_dead=r13_v111_value('piko_alive') is False,owns_E09=r13_v111_owned('E09'),
            news=r13_v111_value('piko_news3:nabi'),report_due=r13_piko_report_due(person),
            resident_available=r13_piko_resident_available(person),
            required_business=r13_piko_required_business(person),current_activity=r13_piko_current_activity(person),
            followups=r13_v111_followups(person),binding=r13_v111_binding()))

    def qa_field146_p036():
        return next(spec for spec in R13_REACTIONS['present']
                    if spec['person']=='nabi' and spec['evidence']=='E06_CONTACT' and spec.get('days')==[7,7])

init 998 python:
    QA_FIELD146_REAL_BOOK=renpy.display.screen.screens[('r13_book',None)]

label qa_field146_start(kind):
    $ qa_field146_prepare(kind)
    call r13_scene(R13_PLACES[room13['location']][1],R13_PLACES[room13['location']][0],'calm')
    call r13_v111_wait(room13['v111']['gate'])
    # 메인 진행은 실행하지 않고 반환된 원본 index만 기록한다.
    $ renpy.test.field146_result=_return
    call screen r13_hub
    return


testcase field146_hidden_companion:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa_field146_start','companion')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    assert eval ('daram' not in r13_visible_people() and r13_field_companion_button146())
    screenshot '146-hidden-companion-hub.png'
    click id 'r13_field_companion'
    click pos (900,600) until screen 'r13_topics' timeout 25
    pause .7
    assert eval (renpy.get_screen('r13_topics').scope.get('person')=='daram')
    screenshot '146-hidden-companion-topics.png'
    if not '다람아, 지금 걷는 속도 괜찮아?':
        click id 'r13_topics_next' until '다람아, 지금 걷는 속도 괜찮아?' timeout 15
    click '다람아, 지금 걷는 속도 괜찮아?'
    click pos (900,600) until screen 'r13_topics' timeout 25
    assert eval (r13_v111_value('resident_chat_read:resident146:daram:work') is True)
    pause .7
    click '돌아가기'
    pause until screen 'r13_hub' timeout 15
    assert eval (qa146_quest_projection()==renpy.test.field146_before)
    run Function(qa_field146_record,'hidden_companion_actual_chat_return')


testcase field146_quest_journal_pc_touch_large:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa_field146_start','journal')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    run Function(qa_field146_journal_mode,False)
    pause .7
    click id 'r13_field_quests'
    pause until screen 'r13_sidequest_journal146' timeout 15
    pause .7
    assert eval (len(r13_sidequest_tasks146())==3 and qa_field146_journal_page()==0)
    screenshot '146-quest-journal-pc-page1.png'
    click id 'r13_quest_journal_next'
    pause .5
    assert eval (qa_field146_journal_page()==1)
    screenshot '146-quest-journal-pc-page2.png'
    click id 'r13_quest_journal_prev'
    pause .5
    assert eval (qa_field146_journal_page()==0)
    click id 'r13_quest_journal_close'
    pause until screen 'r13_hub' timeout 15
    run Function(qa_field146_journal_mode,True)
    pause .7
    click id 'r13_field_quests'
    pause until screen 'r13_sidequest_journal146' timeout 15
    pause .7
    screenshot '146-quest-journal-touch-large-page1.png'
    click id 'r13_quest_journal_next'
    pause .5
    assert eval (qa_field146_journal_page()==1 and r13_touch_ui() and persistent.room13_large_text)
    screenshot '146-quest-journal-touch-large-page2.png'
    click id 'r13_quest_journal_close'
    pause until screen 'r13_hub' timeout 15
    assert eval (qa146_quest_projection()==renpy.test.field146_before)
    run Function(qa_field146_restore_mode)
    run Function(qa_field146_record,'journal_two_pages_pc_touch_large_actual_clicks')


testcase field146_bundle_original_index_cancel:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa_field146_start','bundle')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    assert eval ([o['index'] for o in r13_v111_binding()['options']]==[0,100])
    click pos qa_field146_object_point('mother_note')
    pause until screen 'r13_v111_object_choices146' timeout 15
    pause .7
    assert eval (set(renpy.get_showing_tags()) & {'r13_visitor','r13_dialogue_actor'}==set())
    screenshot '146-bundle-two-actions.png'
    click '돌아가기'
    pause until screen 'r13_hub' timeout 15
    run Function(qa_field146_diagnostics,'bundle-after-cancel')
    assert eval (renpy.test.field146_result is None and room13['v111']['gate']=='bundle_open')
    assert eval (qa146_quest_projection()==renpy.test.field146_before)
    pause .7
    click pos qa_field146_object_point('mother_note')
    pause until screen 'r13_v111_object_choices146' timeout 15
    pause .7
    click '서랍 밑 종이를 빼낸다'
    pause until eval (renpy.test.field146_result is not None) timeout 15
    assert eval (renpy.test.field146_result==100)
    assert eval (qa146_quest_projection()==renpy.test.field146_before)
    run Function(qa_field146_record,'bundle_cancel_and_second_original_index',100)


testcase field146_late_piko_nabi_report_followup:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa_field146_start','late_piko')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    run Function(qa_field146_diagnostics,'late-piko-before-click')
    assert eval (r13_piko_report_due('nabi') and not r13_v111_value('piko_news3:nabi'))
    assert eval (not any(t.get('context')=='piko_after' for t in r13_v111_resident_topics('nabi')))
    if not '나비':
        click '오른쪽 구역' until '나비' timeout 20
    click '나비'
    click pos (900,600) until eval (renpy.get_screen('say') and '피코 씨가 어제 아침' in renpy.get_screen('say').scope.get('what','')) timeout 25
    screenshot '146-late-piko-first-report.png'
    click pos (900,600) until screen 'r13_topics' timeout 35
    assert eval (r13_v111_value('piko_news3:nabi') is True)
    pause .7
    if not '피코 씨 얘기 뒤로 좀 쉬셨습니까?':
        click id 'r13_topics_next' until '피코 씨 얘기 뒤로 좀 쉬셨습니까?' timeout 15
    screenshot '146-late-piko-followup-unlocked.png'
    click '피코 씨 얘기 뒤로 좀 쉬셨습니까?'
    click pos (900,600) until screen 'r13_topics' timeout 25
    assert eval (qa146_quest_projection()==renpy.test.field146_before)
    run Function(qa_field146_record,'late_piko_actual_first_report_then_followup')


# 7일차 미제시 P036가 남아 있어도 피코 소식을 먼저 전할 수 있어야 한다.
# 6일차 학교 네 아이 인계·화재 완료 경로를 보존하고 두 사건의 기억 공존을 확인한다.
testcase field146_late_piko7_optional_present:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa_field146_start','late_piko7')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    run Function(qa_field146_diagnostics,'late-piko7-before-click')
    assert eval (room13['v111']['scene']=='MS14_D07_S02' and r13_v111_value('meeting:fire')=='win')
    assert eval (r13_v111_value('D07_S02_handover_completed') is True and r13_v111_value('D07_S02_message_completed') is True and r13_v111_value('route7')=='uncommitted')
    assert eval (qa_field146_p036()['lines'][0]['id']=='NW_RX_P036_01')
    assert eval (r13_v111_owned('E06_CONTACT') and r13_reaction_day_ok(qa_field146_p036()) and not r13_reaction_seen(qa_field146_p036()))
    assert eval (_r13_resident_business('nabi') and not r13_piko_required_business('nabi') and not r13_piko_current_activity('nabi'))
    assert eval (r13_piko_report_due('nabi') and not r13_v111_value('piko_news3:nabi'))
    assert eval (r13_v111_value('D06_S03P_empty_fire_completed') is True and r13_v111_value('warehouse_children_school_handover')==4 and r13_v111_value('KKOMI_ALIVE') is True and r13_v111_owned('E06_FIRE'))
    if not '나비':
        click '오른쪽 구역' until '나비' timeout 20
    click '나비'
    click pos (900,600) until eval (renpy.get_screen('say') and '피코 씨가 며칠 전 아침' in renpy.get_screen('say').scope.get('what','')) timeout 25
    screenshot '146-late-piko7-first-report-before-present.png'
    click pos (900,600) until screen 'r13_topics' timeout 35
    assert eval (r13_v111_value('piko_news3:nabi') is True and r13_v111_resident_talk_context('nabi')=='fire_safe')
    assert eval (not r13_reaction_seen(qa_field146_p036()))
    assert eval (any(t['title']=='아이들 식사는 챙길 수 있겠습니까?' for t in r13_v111_resident_topics('nabi')))
    pause .7
    if not '피코 씨 얘기 뒤로 좀 쉬셨습니까?':
        click id 'r13_topics_next' until '피코 씨 얘기 뒤로 좀 쉬셨습니까?' timeout 15
    screenshot '146-late-piko7-followup-keeps-optional-record.png'
    click '피코 씨 얘기 뒤로 좀 쉬셨습니까?'
    click pos (900,600) until screen 'r13_topics' timeout 25
    pause .7
    assert eval (not r13_reaction_seen(qa_field146_p036()) and qa146_quest_projection()==renpy.test.field146_before)
    click '자료 제시'
    pause until screen 'r13_book' timeout 15
    pause .7
    assert eval (renpy.get_screen('r13_book').scope.get('target')=='nabi')
    assert eval ('V111:E06_CONTACT' in r13_present_entries(r13_catalog_entries(False,False),'nabi'))
    screenshot '146-late-piko7-existing-present-browser.png'
    click id 'r13_ev_stop'
    pause until screen 'r13_topics' timeout 20
    assert eval (not r13_reaction_seen(qa_field146_p036()) and qa146_quest_projection()==renpy.test.field146_before)
    run Function(qa_field146_record,'late_piko7_optional_P036_does_not_block_news_or_present')


# 2일에 수락해 둔 부탁만 실제 7일차 자유 조사 경계에서 마친다. 새 의뢰 시작은 하지 않는다.
testcase field146_day7_finish_accepted_seam:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa_field146_start','day7_seam')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    assert eval (room13['day']==7 and room13['v111']['scene']=='MS14_D07_S02' and room13['v111']['gate']=='free_day7')
    assert eval (r13_v111_value('meeting:fire')=='win' and r13_v111_value('D07_S02_handover_completed') is True and r13_v111_value('D07_S02_message_completed') is True and r13_v111_value('route7')=='uncommitted')
    assert eval (r13_sidequest_status('seam')=='accepted' and r13_sidequest_state('seam')['accepted_day']==2 and not r13_sidequest_allowed('seam','offer'))
    assert eval (r13_sidequest_calm() and r13_where('resident_yeoni')=='inn' and r13_v111_value('location:daram')=='inn')
    if not '털실 바구니':
        click '오른쪽 구역' until '털실 바구니' timeout 20
    pause .7
    screenshot '146-day7-accepted-seam-worksite.png'
    click '털실 바구니'
    pause until screen 'r13_confirm' timeout 15
    pause .7
    click '천을 받치고 한 땀 뜬다'
    pause until '움직일 틈을 두고 꿰맨다' timeout 15
    pause .7
    click '움직일 틈을 두고 꿰맨다'
    click pos (900,600) until screen 'r13_hub' timeout 25
    assert eval (r13_sidequest_status('seam')=='worked' and r13_sidequest_state('seam').get('result')=='room' and r13_sidequest_state('seam').get('work_day')==7)
    assert eval (qa146_quest_projection()==renpy.test.field146_before)
    if not '여니':
        click '왼쪽 구역' until '여니' timeout 20
    pause .7
    click '여니'
    pause until screen 'r13_topics' timeout 15
    pause .7
    if not '부탁하신 일을 마쳤습니다.':
        click id 'r13_topics_next' until '부탁하신 일을 마쳤습니다.' timeout 15
    screenshot '146-day7-accepted-seam-report.png'
    click '부탁하신 일을 마쳤습니다.'
    click pos (900,600) until screen 'r13_topics' timeout 35
    assert eval (r13_sidequest_status('seam')=='done' and r13_sidequest_state('seam')['accepted_day']==2 and r13_sidequest_state('seam').get('completed_day')==7)
    assert eval (qa146_quest_projection()==renpy.test.field146_before and renpy.test.field146_result is None)
    pause .7
    screenshot '146-day7-accepted-seam-finished.png'
    run Function(qa_field146_record,'day7_actual_finish_prior_accepted_seam')
