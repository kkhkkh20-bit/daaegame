# Controlled NATIVE fixtures, queued for official SDK8.5.3. Not natural campaign proof.
# Uses existing roam, renderer, topmost body picker, ordinary dialogue and object dispatch.
init 999 python:
    def r13_ps_begin(name,day,period):
        r13_pd_begin(name)
        store.r13_ps_date=(day,period)
        store.r13_ps_saved_people=R13_PD_MAP_PEOPLE['post']
        store.r13_ps_saved_objects=R13_PD_MAP_OBJECTS['post']
        store.r13_ps_outcomes={}

    def r13_ps_inside(x,y,poly):
        inside=False
        for i,(ax,ay) in enumerate(poly):
            bx,by=poly[(i+1)%len(poly)]
            if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/float(by-ay)+ax:inside=not inside
        return inside

    def r13_ps_geometry(step):
        assert room13['location']=='post' and (room13['day'],room13['period'])==tuple(r13_ps_date)
        hub=renpy.get_screen('r13_hub')
        assert hub and hub.scope.get('ready',False) and r13_pd_scene_ready(),'Post field/camera not settled'
        offset=r13_world_offset();assert isinstance(offset,int) and 0<=offset<=r13_world_width()-1280
        original=_r13_post_staff_stage(False);actors=r13_stage_people(False)
        old={a['person']:a for a in original};new={a['person']:a for a in actors}
        assert set(old)==set(new),'Placement must never create or remove residents'
        for person in old:
            if person!='seryeon':assert old[person]==new[person],('Unrelated actor changed',person)
        day,period=r13_ps_date
        if period==0 and day>1:
            assert 'seryeon' in new,'Do not fabricate staff presence'
            assert not any(r13_offer_for_person(a['person']) for a in actors),'Authored event active: diagnose fixture; do not suppress it'
            a=new['seryeon'];assert a['pose']=='action_1' and a['rect']==[1403,340,195,234] and a['depth']==560 and a['slot'] is None
            assert r13_world_width()==2160 and r13_world_file('post','morning')==R13_POST_STAFF_CONTACT['background']
            assert tuple(renpy.image_size(R13_POST_STAFF_CONTACT['background']))==(2160,728)
            assert len(a.get('map27_occlusion',[]))==1 and not a.get('map27_keepouts')
            s=r13_acting_spec('seryeon','action_1');scale=a['height']/float(s['crop'][3]);hand=[a['x']+s['hand'][0]*scale,a['y']+s['hand'][1]*scale]
            assert max(abs(hand[i]-R13_POST_STAFF_CONTACT['hand'][i]) for i in (0,1))<0.51
            # Independent world-polygon oracle, not R13FurnitureMask reused as its own oracle.
            x,y,w,h=a['rect']
            assert all(isinstance(v,int) for v in (x,y,w,h)),'Native alpha oracle requires integer virtual pixels'
            raw=dict(a);raw['map27_occlusion']=[]
            raw_render=renpy.render(r13_staged_visible_art(raw,still=True),w,h,1.2,1.2)
            visible=renpy.render(r13_staged_visible_art(a,still=True),w,h,1.2,1.2)
            hit=renpy.render(r13_actor_hit_mask(a),w,h,1.2,1.2)
            poly=R13_POST_STAFF_CONTACT['foreground'];hidden=[];outside=[];body=[]
            for ly in range(3,h-3,2):
                for lx in range(3,w-3,2):
                    px,py=x+lx,y+ly
                    solid=raw_render.is_pixel_opaque(lx,ly)
                    # A3x3 interior test stays clear of raster polygon boundaries.
                    concealed=all(r13_ps_inside(px+dx,py+dy,poly) for dx in (-2,0,2) for dy in (-2,0,2))
                    assert bool(visible.is_pixel_opaque(lx,ly))==bool(hit.is_pixel_opaque(lx,ly)),('Visible/picker mismatch',lx,ly)
                    if solid and concealed:
                        assert not hit.is_pixel_opaque(lx,ly),('Hidden lower body still clickable',px,py)
                        hidden.append([px,py])
                    elif not solid:
                        assert not hit.is_pixel_opaque(lx,ly),('Transparent exterior still clickable',px,py)
                        outside.append([px,py])
                    elif hit.is_pixel_opaque(lx,ly):body.append([px,py])
            assert len(hidden)>30 and len(outside)>30 and len(body)>100,(len(hidden),len(outside),len(body))
            offset=r13_world_offset();expected=r13_person_caption('seryeon')+' · 말 걸기';plates=[p['rect'] for p in r13_actor_nameplates(actors)]
            checked=[]
            for px,py in hidden[::max(1,len(hidden)//30)]:
                if not (24<px-offset<1256 and 110<py<690):continue
                if any(rx<=px<rx+rw and ry<=py<ry+rh for rx,ry,rw,rh in plates):continue
                sx,sy=int(px-offset),int(py)
                assert (sx+offset,sy)==(px,py),'World/screen pixel conversion drift'
                f=renpy.display.render.focus_at_point(sx,sy);tip=f.widget._get_tooltip() if f else None
                assert tip!=expected,('Concealed body stole native focus',px,py,tip)
                checked.append(dict(world=[px,py],screen=[sx,sy],local=[px-x,py-y],camera_offset=offset,tooltip=tip))
            r13_pd_flow_log('post-staff-native-alpha',dict(step=step,hand=hand,hidden_count=len(hidden),transparent_count=len(outside),visible_count=len(body),hidden_focus_samples=checked,visual_acceptance=False))
            r13_pd_target_render('seryeon','action_1',step)
        elif period==1:
            assert r13_world_width()==1280 and new['seryeon']==old['seryeon']
            assert new['seryeon']['pose']=='chair_read' and new['seryeon']['rect']==[10,310,310,364]
        elif period==2 or day==1:
            assert 'seryeon' not in new,'Do not invent an evening/day1 shift'
        r13_pd_flow_log('post-staff-context',dict(step=step,day=day,period=period,camera=r13_world_offset(),people=sorted(new),actors=actors,visual_acceptance=False))

    def r13_ps_choose(person):
        R13_PD_MAP_PEOPLE['post']=(person,)
        r13_pd_choose_person(True)

    def r13_ps_object(key):
        R13_PD_MAP_OBJECTS['post']=(key,)
        r13_pd_choose_object()

    def r13_ps_end():
        r13_pd_flow_log('post-staff-result',dict(outcomes=dict(r13_ps_outcomes),visual_acceptance=False))
        R13_PD_MAP_PEOPLE['post']=r13_ps_saved_people
        R13_PD_MAP_OBJECTS['post']=r13_ps_saved_objects
        r13_pd_end()

testcase investigation_post_staff_d2:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_ps_begin,"investigation_post_staff_d2",2,0)
    run Call("r13_qa_roam",dict(day=2,period=0,location="post",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Show("r13_qa_pixel_variant")
    screenshot "investigation_post_staff_d2-01-before-strict.png"
    run Function(r13_pd_check_field,"initial-field",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d2-02-before-strict.png"
    run Function(r13_ps_geometry,"initial-field",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d2-01-initial.png"
    screenshot "investigation_post_staff_d2-03-camera-before-assert.png"
    assert eval (r13_world_offset()==440)
    if eval (r13_world_offset()>0):
        click "‹"
        pause 0.5
    if eval (r13_world_offset()>0):
        click "‹"
        pause 0.5
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_d2-04-camera-before-assert.png"
    assert eval (r13_world_offset()==0)
    screenshot "investigation_post_staff_d2-05-before-strict.png"
    run Function(r13_ps_geometry,"camera-zero",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d2-06-before-strict.png"
    run Function(r13_ps_choose,"seryeon",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    assert eval (not r13_pd_person_ready)
    screenshot "investigation_post_staff_d2-02-camera-zero.png"
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_d2-07-camera-before-assert.png"
    assert eval (r13_world_offset()==880)
    screenshot "investigation_post_staff_d2-08-before-strict.png"
    run Function(r13_ps_geometry,"camera-right",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d2-03-camera-right.png"
    screenshot "investigation_post_staff_d2-09-before-strict.png"
    run Function(r13_ps_choose,"seryeon",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    assert eval (r13_pd_person_ready and r13_pd_person=="seryeon")
    click pos (r13_pd_person_x,r13_pd_person_y)
    pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None or renpy.get_screen("notify") is not None) timeout 5
    if eval (r13_pd_contact_allowed):
        if screen "say":
            run Function(r13_pd_log_opening,"investigation_post_staff_d2-seryeon-first-notice",_update_screens=False)
            screenshot "investigation_post_staff_d2-seryeon-notice.png"
        advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
        assert eval (r13_target=="seryeon")
        pause 0.4
        if screen "r13_resident_approach":
            run Function(r13_pd_approach_yes,_update_screens=False)
            click expression r13_question_summary(r13_pd_approach_text)
        advance until screen "r13_topics" timeout 40
        pause 0.4
        if eval (bool(r13_pd_plain_topics(r13_pd_person))):
            run Function(r13_pd_choose_topic,_update_screens=False)
            click expression r13_pd_topic_title
            advance until eval (r13_pd_topic_say_ready()) timeout 40
            pause 0.4
            run Function(r13_pd_assert_topic_say,_update_screens=False)
            screenshot "investigation_post_staff_d2-seryeon-actual-say.png"
            advance until screen "r13_topics" timeout 40
            assert eval (r13_pd_topic in room13['read_topics'])
            $ r13_ps_outcomes['investigation_post_staff_d2-seryeon']='ACTUAL_BODY_AND_PLAIN_SPEECH'
        else:
            $ r13_ps_outcomes['investigation_post_staff_d2-seryeon']='ACTUAL_BODY_NORMAL_MENU_NO_PLAIN_TOPIC'
            screenshot "investigation_post_staff_d2-seryeon-normal-menu.png"
        pause 0.3
        click "돌아가기"
        advance until screen "r13_hub" timeout 40
    else:
        assert screen "notify"
        assert eval (renpy.get_screen("notify").scope.get("message")=="지금은 %s에게 더 물어볼 이야기가 없다."%R13_NAMES[r13_pd_person])
        $ r13_ps_outcomes['investigation_post_staff_d2-seryeon']='ACTUAL_BODY_NO_CONTENT_SPEECH_NOT_VERIFIED'
        screenshot "investigation_post_staff_d2-seryeon-no-content.png"
        pause until eval (renpy.get_screen("notify") is None) timeout 5
        assert screen "r13_hub"
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_d2-10-before-strict.png"
    run Function(r13_ps_geometry,"investigation_post_staff_d2-seryeon-returned",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d2-seryeon-returned.png"
    screenshot "investigation_post_staff_d2-11-before-strict.png"
    run Function(r13_ps_choose,"resident_sling",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    assert eval (r13_pd_person_ready and r13_pd_person=="resident_sling")
    click pos (r13_pd_person_x,r13_pd_person_y)
    pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None or renpy.get_screen("notify") is not None) timeout 5
    if eval (r13_pd_contact_allowed):
        if screen "say":
            run Function(r13_pd_log_opening,"investigation_post_staff_d2-sling-first-notice",_update_screens=False)
            screenshot "investigation_post_staff_d2-sling-notice.png"
        advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
        assert eval (r13_target=="resident_sling")
        pause 0.4
        if screen "r13_resident_approach":
            run Function(r13_pd_approach_yes,_update_screens=False)
            click expression r13_question_summary(r13_pd_approach_text)
        advance until screen "r13_topics" timeout 40
        pause 0.4
        if eval (bool(r13_pd_plain_topics(r13_pd_person))):
            run Function(r13_pd_choose_topic,_update_screens=False)
            click expression r13_pd_topic_title
            advance until eval (r13_pd_topic_say_ready()) timeout 40
            pause 0.4
            run Function(r13_pd_assert_topic_say,_update_screens=False)
            screenshot "investigation_post_staff_d2-sling-actual-say.png"
            advance until screen "r13_topics" timeout 40
            assert eval (r13_pd_topic in room13['read_topics'])
            $ r13_ps_outcomes['investigation_post_staff_d2-sling']='ACTUAL_BODY_AND_PLAIN_SPEECH'
        else:
            $ r13_ps_outcomes['investigation_post_staff_d2-sling']='ACTUAL_BODY_NORMAL_MENU_NO_PLAIN_TOPIC'
            screenshot "investigation_post_staff_d2-sling-normal-menu.png"
        pause 0.3
        click "돌아가기"
        advance until screen "r13_hub" timeout 40
    else:
        assert screen "notify"
        assert eval (renpy.get_screen("notify").scope.get("message")=="지금은 %s에게 더 물어볼 이야기가 없다."%R13_NAMES[r13_pd_person])
        $ r13_ps_outcomes['investigation_post_staff_d2-sling']='ACTUAL_BODY_NO_CONTENT_SPEECH_NOT_VERIFIED'
        screenshot "investigation_post_staff_d2-sling-no-content.png"
        pause until eval (renpy.get_screen("notify") is None) timeout 5
        assert screen "r13_hub"
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_d2-12-before-strict.png"
    run Function(r13_ps_geometry,"investigation_post_staff_d2-sling-returned",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d2-sling-returned.png"
    screenshot "investigation_post_staff_d2-13-before-strict.png"
    run Function(r13_ps_choose,"resident_jongjong",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    assert eval (r13_pd_person_ready and r13_pd_person=="resident_jongjong")
    click pos (r13_pd_person_x,r13_pd_person_y)
    pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None or renpy.get_screen("notify") is not None) timeout 5
    if eval (r13_pd_contact_allowed):
        if screen "say":
            run Function(r13_pd_log_opening,"investigation_post_staff_d2-jongjong-first-notice",_update_screens=False)
            screenshot "investigation_post_staff_d2-jongjong-notice.png"
        advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
        assert eval (r13_target=="resident_jongjong")
        pause 0.4
        if screen "r13_resident_approach":
            run Function(r13_pd_approach_yes,_update_screens=False)
            click expression r13_question_summary(r13_pd_approach_text)
        advance until screen "r13_topics" timeout 40
        pause 0.4
        if eval (bool(r13_pd_plain_topics(r13_pd_person))):
            run Function(r13_pd_choose_topic,_update_screens=False)
            click expression r13_pd_topic_title
            advance until eval (r13_pd_topic_say_ready()) timeout 40
            pause 0.4
            run Function(r13_pd_assert_topic_say,_update_screens=False)
            screenshot "investigation_post_staff_d2-jongjong-actual-say.png"
            advance until screen "r13_topics" timeout 40
            assert eval (r13_pd_topic in room13['read_topics'])
            $ r13_ps_outcomes['investigation_post_staff_d2-jongjong']='ACTUAL_BODY_AND_PLAIN_SPEECH'
        else:
            $ r13_ps_outcomes['investigation_post_staff_d2-jongjong']='ACTUAL_BODY_NORMAL_MENU_NO_PLAIN_TOPIC'
            screenshot "investigation_post_staff_d2-jongjong-normal-menu.png"
        pause 0.3
        click "돌아가기"
        advance until screen "r13_hub" timeout 40
    else:
        assert screen "notify"
        assert eval (renpy.get_screen("notify").scope.get("message")=="지금은 %s에게 더 물어볼 이야기가 없다."%R13_NAMES[r13_pd_person])
        $ r13_ps_outcomes['investigation_post_staff_d2-jongjong']='ACTUAL_BODY_NO_CONTENT_SPEECH_NOT_VERIFIED'
        screenshot "investigation_post_staff_d2-jongjong-no-content.png"
        pause until eval (renpy.get_screen("notify") is None) timeout 5
        assert screen "r13_hub"
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_d2-14-before-strict.png"
    run Function(r13_ps_geometry,"investigation_post_staff_d2-jongjong-returned",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d2-jongjong-returned.png"
    $ renpy.save("qa-post-staff-placement")
    click "‹"
    pause 0.5
    screenshot "investigation_post_staff_d2-15-camera-before-assert.png"
    assert eval (r13_world_offset()<880)
    run Function(renpy.load,"qa-post-staff-placement")
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_d2-16-camera-before-assert.png"
    assert eval (r13_world_offset()==880)
    screenshot "investigation_post_staff_d2-17-before-strict.png"
    run Function(r13_ps_geometry,"actual-save-loaded",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "post-staff-d2-actual-save-loaded.png"
    screenshot "investigation_post_staff_d2-18-before-strict.png"
    run Function(r13_ps_choose,"seryeon",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    assert eval (r13_pd_person_ready and r13_pd_person=="seryeon")
    click pos (r13_pd_person_x,r13_pd_person_y)
    pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None or renpy.get_screen("notify") is not None) timeout 5
    if eval (r13_pd_contact_allowed):
        if screen "say":
            run Function(r13_pd_log_opening,"investigation_post_staff_d2-repeated-seryeon-first-notice",_update_screens=False)
            screenshot "investigation_post_staff_d2-repeated-seryeon-notice.png"
        advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
        assert eval (r13_target=="seryeon")
        pause 0.4
        if screen "r13_resident_approach":
            run Function(r13_pd_approach_yes,_update_screens=False)
            click expression r13_question_summary(r13_pd_approach_text)
        advance until screen "r13_topics" timeout 40
        pause 0.4
        if eval (bool(r13_pd_plain_topics(r13_pd_person))):
            run Function(r13_pd_choose_topic,_update_screens=False)
            click expression r13_pd_topic_title
            advance until eval (r13_pd_topic_say_ready()) timeout 40
            pause 0.4
            run Function(r13_pd_assert_topic_say,_update_screens=False)
            screenshot "investigation_post_staff_d2-repeated-seryeon-actual-say.png"
            advance until screen "r13_topics" timeout 40
            assert eval (r13_pd_topic in room13['read_topics'])
            $ r13_ps_outcomes['investigation_post_staff_d2-repeated-seryeon']='ACTUAL_BODY_AND_PLAIN_SPEECH'
        else:
            $ r13_ps_outcomes['investigation_post_staff_d2-repeated-seryeon']='ACTUAL_BODY_NORMAL_MENU_NO_PLAIN_TOPIC'
            screenshot "investigation_post_staff_d2-repeated-seryeon-normal-menu.png"
        pause 0.3
        click "돌아가기"
        advance until screen "r13_hub" timeout 40
    else:
        assert screen "notify"
        assert eval (renpy.get_screen("notify").scope.get("message")=="지금은 %s에게 더 물어볼 이야기가 없다."%R13_NAMES[r13_pd_person])
        $ r13_ps_outcomes['investigation_post_staff_d2-repeated-seryeon']='ACTUAL_BODY_NO_CONTENT_SPEECH_NOT_VERIFIED'
        screenshot "investigation_post_staff_d2-repeated-seryeon-no-content.png"
        pause until eval (renpy.get_screen("notify") is None) timeout 5
        assert screen "r13_hub"
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_d2-19-before-strict.png"
    run Function(r13_ps_geometry,"investigation_post_staff_d2-repeated-seryeon-returned",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d2-repeated-seryeon-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_ps_end)

testcase investigation_post_staff_d3:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_ps_begin,"investigation_post_staff_d3",3,0)
    run Call("r13_qa_roam",dict(day=3,period=0,location="post",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Show("r13_qa_pixel_variant")
    screenshot "investigation_post_staff_d3-01-before-strict.png"
    run Function(r13_pd_check_field,"initial-field",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d3-02-before-strict.png"
    run Function(r13_ps_geometry,"initial-field",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d3-01-initial.png"
    screenshot "investigation_post_staff_d3-03-camera-before-assert.png"
    assert eval (r13_world_offset()==440)
    if eval (r13_world_offset()>0):
        click "‹"
        pause 0.5
    if eval (r13_world_offset()>0):
        click "‹"
        pause 0.5
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_d3-04-camera-before-assert.png"
    assert eval (r13_world_offset()==0)
    screenshot "investigation_post_staff_d3-05-before-strict.png"
    run Function(r13_ps_geometry,"camera-zero",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d3-06-before-strict.png"
    run Function(r13_ps_choose,"seryeon",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    assert eval (not r13_pd_person_ready)
    screenshot "investigation_post_staff_d3-02-camera-zero.png"
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_d3-07-camera-before-assert.png"
    assert eval (r13_world_offset()==880)
    screenshot "investigation_post_staff_d3-08-before-strict.png"
    run Function(r13_ps_geometry,"camera-right",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d3-03-camera-right.png"
    screenshot "investigation_post_staff_d3-09-before-strict.png"
    run Function(r13_ps_choose,"seryeon",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    assert eval (r13_pd_person_ready and r13_pd_person=="seryeon")
    click pos (r13_pd_person_x,r13_pd_person_y)
    pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None or renpy.get_screen("notify") is not None) timeout 5
    if eval (r13_pd_contact_allowed):
        if screen "say":
            run Function(r13_pd_log_opening,"investigation_post_staff_d3-seryeon-first-notice",_update_screens=False)
            screenshot "investigation_post_staff_d3-seryeon-notice.png"
        advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
        assert eval (r13_target=="seryeon")
        pause 0.4
        if screen "r13_resident_approach":
            run Function(r13_pd_approach_yes,_update_screens=False)
            click expression r13_question_summary(r13_pd_approach_text)
        advance until screen "r13_topics" timeout 40
        pause 0.4
        if eval (bool(r13_pd_plain_topics(r13_pd_person))):
            run Function(r13_pd_choose_topic,_update_screens=False)
            click expression r13_pd_topic_title
            advance until eval (r13_pd_topic_say_ready()) timeout 40
            pause 0.4
            run Function(r13_pd_assert_topic_say,_update_screens=False)
            screenshot "investigation_post_staff_d3-seryeon-actual-say.png"
            advance until screen "r13_topics" timeout 40
            assert eval (r13_pd_topic in room13['read_topics'])
            $ r13_ps_outcomes['investigation_post_staff_d3-seryeon']='ACTUAL_BODY_AND_PLAIN_SPEECH'
        else:
            $ r13_ps_outcomes['investigation_post_staff_d3-seryeon']='ACTUAL_BODY_NORMAL_MENU_NO_PLAIN_TOPIC'
            screenshot "investigation_post_staff_d3-seryeon-normal-menu.png"
        pause 0.3
        click "돌아가기"
        advance until screen "r13_hub" timeout 40
    else:
        assert screen "notify"
        assert eval (renpy.get_screen("notify").scope.get("message")=="지금은 %s에게 더 물어볼 이야기가 없다."%R13_NAMES[r13_pd_person])
        $ r13_ps_outcomes['investigation_post_staff_d3-seryeon']='ACTUAL_BODY_NO_CONTENT_SPEECH_NOT_VERIFIED'
        screenshot "investigation_post_staff_d3-seryeon-no-content.png"
        pause until eval (renpy.get_screen("notify") is None) timeout 5
        assert screen "r13_hub"
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_d3-10-before-strict.png"
    run Function(r13_ps_geometry,"investigation_post_staff_d3-seryeon-returned",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d3-seryeon-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_ps_end)

testcase investigation_post_staff_d6:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_ps_begin,"investigation_post_staff_d6",6,0)
    run Call("r13_qa_roam",dict(day=6,period=0,location="post",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    # Real day6 arrival event: resolve the authored ledger sale through its actual UI.
    # Never seed ev_u_done/pages_sold, change the date, or jump over the production event.
    advance until screen "choice" timeout 40
    pause until eval (renpy.get_screen("choice").scope.get("choice_ready",False)) timeout 5
    screenshot "post-staff-d6-00-real-ledger-menu.png"
    assert eval (room13['day']==6 and room13['period']==0 and room13['location']=='post' and r13_has('ev_u_done'))
    assert eval ('모른 척 지나간다' in [item.caption for item in renpy.get_screen('choice').scope['items']])
    run Function(r13_pd_flow_log,"post-staff-real-ledger-menu",dict(choices=[item.caption for item in renpy.get_screen('choice').scope['items']],state=r13_pd_copy.deepcopy(room13),camera_offset=r13_world_offset()),_update_screens=False)
    click "모른 척 지나간다"
    advance until screen "r13_hub" timeout 40
    screenshot "post-staff-d6-00-real-ledger-return.png"
    assert eval (room13['day']==6 and room13['period']==0 and room13['location']=='post' and r13_has('ev_u_done') and r13_has('pages_sold'))
    assert eval (not r13_has('pages_copy_promised') and not r13_has('know_stone_history') and 'W3' not in room13['evidence'])
    run Function(r13_pd_flow_log,"post-staff-real-ledger-resolved",dict(choice="모른 척 지나간다",state=r13_pd_copy.deepcopy(room13),camera_offset=r13_world_offset()),_update_screens=False)
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Show("r13_qa_pixel_variant")
    screenshot "investigation_post_staff_d6-01-before-strict.png"
    run Function(r13_pd_check_field,"initial-field",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d6-02-before-strict.png"
    run Function(r13_ps_geometry,"initial-field",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d6-01-initial.png"
    screenshot "investigation_post_staff_d6-03-camera-before-assert.png"
    assert eval (r13_world_offset()==440)
    if eval (r13_world_offset()>0):
        click "‹"
        pause 0.5
    if eval (r13_world_offset()>0):
        click "‹"
        pause 0.5
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_d6-04-camera-before-assert.png"
    assert eval (r13_world_offset()==0)
    screenshot "investigation_post_staff_d6-05-before-strict.png"
    run Function(r13_ps_geometry,"camera-zero",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d6-06-before-strict.png"
    run Function(r13_ps_choose,"seryeon",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    assert eval (not r13_pd_person_ready)
    screenshot "investigation_post_staff_d6-02-camera-zero.png"
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_d6-07-camera-before-assert.png"
    assert eval (r13_world_offset()==880)
    screenshot "investigation_post_staff_d6-08-before-strict.png"
    run Function(r13_ps_geometry,"camera-right",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d6-03-camera-right.png"
    screenshot "investigation_post_staff_d6-09-before-strict.png"
    run Function(r13_ps_choose,"seryeon",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    assert eval (r13_pd_person_ready and r13_pd_person=="seryeon")
    click pos (r13_pd_person_x,r13_pd_person_y)
    pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None or renpy.get_screen("notify") is not None) timeout 5
    if eval (r13_pd_contact_allowed):
        if screen "say":
            run Function(r13_pd_log_opening,"investigation_post_staff_d6-seryeon-first-notice",_update_screens=False)
            screenshot "investigation_post_staff_d6-seryeon-notice.png"
        advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
        assert eval (r13_target=="seryeon")
        pause 0.4
        if screen "r13_resident_approach":
            run Function(r13_pd_approach_yes,_update_screens=False)
            click expression r13_question_summary(r13_pd_approach_text)
        advance until screen "r13_topics" timeout 40
        pause 0.4
        if eval (bool(r13_pd_plain_topics(r13_pd_person))):
            run Function(r13_pd_choose_topic,_update_screens=False)
            click expression r13_pd_topic_title
            advance until eval (r13_pd_topic_say_ready()) timeout 40
            pause 0.4
            run Function(r13_pd_assert_topic_say,_update_screens=False)
            screenshot "investigation_post_staff_d6-seryeon-actual-say.png"
            advance until screen "r13_topics" timeout 40
            assert eval (r13_pd_topic in room13['read_topics'])
            $ r13_ps_outcomes['investigation_post_staff_d6-seryeon']='ACTUAL_BODY_AND_PLAIN_SPEECH'
        else:
            $ r13_ps_outcomes['investigation_post_staff_d6-seryeon']='ACTUAL_BODY_NORMAL_MENU_NO_PLAIN_TOPIC'
            screenshot "investigation_post_staff_d6-seryeon-normal-menu.png"
        pause 0.3
        click "돌아가기"
        advance until screen "r13_hub" timeout 40
    else:
        assert screen "notify"
        assert eval (renpy.get_screen("notify").scope.get("message")=="지금은 %s에게 더 물어볼 이야기가 없다."%R13_NAMES[r13_pd_person])
        $ r13_ps_outcomes['investigation_post_staff_d6-seryeon']='ACTUAL_BODY_NO_CONTENT_SPEECH_NOT_VERIFIED'
        screenshot "investigation_post_staff_d6-seryeon-no-content.png"
        pause until eval (renpy.get_screen("notify") is None) timeout 5
        assert screen "r13_hub"
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_d6-10-before-strict.png"
    run Function(r13_ps_geometry,"investigation_post_staff_d6-seryeon-returned",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_d6-seryeon-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_ps_end)

testcase investigation_post_staff_day1_absent:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_ps_begin,"investigation_post_staff_day1_absent",1,0)
    run Call("r13_qa_roam",dict(day=1,period=0,location="post",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Show("r13_qa_pixel_variant")
    screenshot "investigation_post_staff_day1_absent-01-before-strict.png"
    run Function(r13_pd_check_field,"initial-field",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_day1_absent-02-before-strict.png"
    run Function(r13_ps_geometry,"initial-field",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_day1_absent-01-initial.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_ps_end)

testcase investigation_post_staff_afternoon:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_ps_begin,"investigation_post_staff_afternoon",2,1)
    run Call("r13_qa_roam",dict(day=2,period=1,location="post",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Show("r13_qa_pixel_variant")
    screenshot "investigation_post_staff_afternoon-01-before-strict.png"
    run Function(r13_pd_check_field,"initial-field",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_afternoon-02-before-strict.png"
    run Function(r13_ps_geometry,"initial-field",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_afternoon-01-initial.png"
    screenshot "investigation_post_staff_afternoon-03-before-strict.png"
    run Function(r13_ps_choose,"seryeon",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    assert eval (r13_pd_person_ready and r13_pd_person=="seryeon")
    click pos (r13_pd_person_x,r13_pd_person_y)
    pause until eval (renpy.get_screen("say") is not None or renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None or renpy.get_screen("notify") is not None) timeout 5
    if eval (r13_pd_contact_allowed):
        if screen "say":
            run Function(r13_pd_log_opening,"post-staff-afternoon-seryeon-first-notice",_update_screens=False)
            screenshot "post-staff-afternoon-seryeon-notice.png"
        advance until eval (renpy.get_screen("r13_resident_approach") is not None or renpy.get_screen("r13_topics") is not None) timeout 40
        assert eval (r13_target=="seryeon")
        pause 0.4
        if screen "r13_resident_approach":
            run Function(r13_pd_approach_yes,_update_screens=False)
            click expression r13_question_summary(r13_pd_approach_text)
        advance until screen "r13_topics" timeout 40
        pause 0.4
        if eval (bool(r13_pd_plain_topics(r13_pd_person))):
            run Function(r13_pd_choose_topic,_update_screens=False)
            click expression r13_pd_topic_title
            advance until eval (r13_pd_topic_say_ready()) timeout 40
            pause 0.4
            run Function(r13_pd_assert_topic_say,_update_screens=False)
            screenshot "post-staff-afternoon-seryeon-actual-say.png"
            advance until screen "r13_topics" timeout 40
            assert eval (r13_pd_topic in room13['read_topics'])
            $ r13_ps_outcomes['post-staff-afternoon-seryeon']='ACTUAL_BODY_AND_PLAIN_SPEECH'
        else:
            $ r13_ps_outcomes['post-staff-afternoon-seryeon']='ACTUAL_BODY_NORMAL_MENU_NO_PLAIN_TOPIC'
            screenshot "post-staff-afternoon-seryeon-normal-menu.png"
        pause 0.3
        click "돌아가기"
        advance until screen "r13_hub" timeout 40
    else:
        assert screen "notify"
        assert eval (renpy.get_screen("notify").scope.get("message")=="지금은 %s에게 더 물어볼 이야기가 없다."%R13_NAMES[r13_pd_person])
        $ r13_ps_outcomes['post-staff-afternoon-seryeon']='ACTUAL_BODY_NO_CONTENT_SPEECH_NOT_VERIFIED'
        screenshot "post-staff-afternoon-seryeon-no-content.png"
        pause until eval (renpy.get_screen("notify") is None) timeout 5
        assert screen "r13_hub"
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_afternoon-04-before-strict.png"
    run Function(r13_ps_geometry,"post-staff-afternoon-seryeon-returned",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "post-staff-afternoon-seryeon-returned.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_ps_end)

testcase investigation_post_staff_evening_absent:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_ps_begin,"investigation_post_staff_evening_absent",2,2)
    run Call("r13_qa_roam",dict(day=2,period=2,location="post",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Show("r13_qa_pixel_variant")
    screenshot "investigation_post_staff_evening_absent-01-before-strict.png"
    run Function(r13_pd_check_field,"initial-field",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_evening_absent-02-before-strict.png"
    run Function(r13_ps_geometry,"initial-field",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_evening_absent-01-initial.png"
    run Hide("r13_qa_pixel_variant")
    run Function(r13_ps_end)

testcase investigation_post_staff_objects:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ persistent.room13_motion=False
    run Function(r13_ps_begin,"investigation_post_staff_objects",2,0)
    run Call("r13_qa_roam",dict(day=2,period=0,location="post",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    run Show("r13_qa_pixel_variant")
    screenshot "investigation_post_staff_objects-01-before-strict.png"
    run Function(r13_pd_check_field,"initial-field",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_objects-02-before-strict.png"
    run Function(r13_ps_geometry,"initial-field",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    screenshot "investigation_post_staff_objects-01-initial.png"
    if eval (r13_world_offset()>0):
        click "‹"
        pause 0.5
    if eval (r13_world_offset()>0):
        click "‹"
        pause 0.5
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_objects-03-camera-before-assert.png"
    assert eval (r13_world_offset()==0)
    screenshot "investigation_post_staff_objects-04-before-strict.png"
    run Function(r13_ps_object,"scarf",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    assert eval (r13_pd_object_ready and r13_pd_object=="scarf")
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    screenshot "post-staff-object-scarf.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_objects-05-before-strict.png"
    run Function(r13_ps_geometry,"object-scarf-returned",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    $ r13_ps_outcomes['object-scarf']='ACTUAL_OBJECT_DISPATCH_AND_RETURN'
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_objects-06-camera-before-assert.png"
    assert eval (r13_world_offset()==880)
    screenshot "investigation_post_staff_objects-07-before-strict.png"
    run Function(r13_ps_object,"twine",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    assert eval (r13_pd_object_ready and r13_pd_object=="twine")
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    screenshot "post-staff-object-twine.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_objects-08-before-strict.png"
    run Function(r13_ps_geometry,"object-twine-returned",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    $ r13_ps_outcomes['object-twine']='ACTUAL_OBJECT_DISPATCH_AND_RETURN'
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_objects-09-camera-before-assert.png"
    assert eval (r13_world_offset()==880)
    screenshot "investigation_post_staff_objects-10-before-strict.png"
    run Function(r13_ps_object,"notice",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    assert eval (r13_pd_object_ready and r13_pd_object=="notice")
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    screenshot "post-staff-object-notice.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_objects-11-before-strict.png"
    run Function(r13_ps_geometry,"object-notice-returned",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    $ r13_ps_outcomes['object-notice']='ACTUAL_OBJECT_DISPATCH_AND_RETURN'
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    if eval (r13_world_offset()<r13_world_width()-1280):
        click "›"
        pause 0.5
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_objects-12-camera-before-assert.png"
    assert eval (r13_world_offset()==880)
    screenshot "investigation_post_staff_objects-13-before-strict.png"
    run Function(r13_ps_object,"parcels",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    assert eval (r13_pd_object_ready and r13_pd_object=="parcels")
    click pos (r13_pd_object_x,r13_pd_object_y)
    pause until eval (r13_has(r13_pd_observed_flag)) timeout 10
    assert screen "say"
    screenshot "post-staff-object-parcels.png"
    advance until screen "r13_hub" timeout 40
    pause until eval (renpy.get_screen("r13_hub").scope.get("ready",False)) timeout 5
    pause 1.2
    pause until eval (r13_pd_scene_ready()) timeout 8
    move pos (600,20)
    pause 0.1
    move pos (640,20)
    pause 0.2
    pause until eval (r13_pd_hover_clear()) timeout 3
    screenshot "investigation_post_staff_objects-14-before-strict.png"
    run Function(r13_ps_geometry,"object-parcels-returned",_update_screens=False)
    # Yield completed GPU/focus work to the SDK scheduler; normal watchdog unchanged.
    pause 0.01
    $ r13_ps_outcomes['object-parcels']='ACTUAL_OBJECT_DISPATCH_AND_RETURN'
    run Hide("r13_qa_pixel_variant")
    run Function(r13_ps_end)
