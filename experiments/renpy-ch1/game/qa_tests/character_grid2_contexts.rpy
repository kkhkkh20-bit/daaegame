# QA-only overlay. Never include in a release build. Requires default-off v1
# production patch and PR15 character_grid2_diag helpers; no source art changes.
init 990 python:
    import inspect as r13_c4_inspect
    import os as r13_c4_os
    import json as r13_c4_json
    R13_C4_ACTIVE=False
    R13_C4_RECORDS={}
    _r13_c4_final=r13_g2_final

    def r13_g2_final(art,size=(1280,720)):
        result=_r13_c4_final(art,size)
        if R13_C4_ACTIVE and not renpy.predicting():
            frame=r13_c4_inspect.currentframe().f_back
            context=None;key=None
            try:
                # Observe the exact displayable handed back to production.
                # Never wrap it a second time just for a passing capture.
                name=frame.f_code.co_name
                if name=='r13_g2_profile_transform':
                    context='profile';key=str(frame.f_locals.get('art'))+str(size)
                elif name=='r13_staged_visible_art':
                    context='field';key=frame.f_locals['actor']['person']
                elif name=='__init__' and type(frame.f_locals.get('self')).__name__=='R13MeetingOrbit':
                    context='meeting';key='orbit'
                elif 'room13_rules.rpy' in frame.f_code.co_filename:
                    context='dialogue';key='visitor'
                if context:
                    R13_C4_RECORDS[(context,key)]=(art,result,tuple(size))
            finally:
                del frame
        return result

    def r13_c4_out():
        path=r13_c4_os.path.join(r13_c4_os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'),'character-grid2-contexts')
        r13_c4_os.makedirs(path,exist_ok=True)
        return path

    def r13_c4_log(event,**fields):
        fields['event']=event
        with open(r13_c4_os.path.join(r13_c4_out(),'metrics.jsonl'),'a') as f:
            f.write(r13_c4_json.dumps(fields,default=str,ensure_ascii=False)+'\n')

    def r13_c4_checkpoint(step):
        r13_c4_log('checkpoint',step=step,grid_enabled=bool(R13_CHARACTER_GRID2_ENABLED))

    def r13_c4_begin():
        global R13_C4_ACTIVE,R13_CHARACTER_GRID2_ENABLED
        assert not R13_C4_ACTIVE and not R13_CHARACTER_GRID2_ENABLED,'Default-off prerequisite failed'
        store.r13_c4_old_motion=persistent.room13_motion
        R13_C4_RECORDS.clear()
        R13_CHARACTER_GRID2_ENABLED=True
        R13_C4_ACTIVE=True
        r13_c4_log('begin',version=R13_CHARACTER_GRID2_VERSION,production_default=False)
        renpy.restart_interaction()

    def r13_c4_replay_enable():
        global R13_C4_ACTIVE,R13_CHARACTER_GRID2_ENABLED
        assert _in_replay=='r13_admin_meeting_replay' and r13_admin_meeting_test
        assert not R13_CHARACTER_GRID2_ENABLED and not R13_C4_ACTIVE,'Replay must start from default-off store'
        R13_C4_RECORDS.clear()
        R13_CHARACTER_GRID2_ENABLED=True
        R13_C4_ACTIVE=True
        r13_c4_checkpoint('meeting-replay-scoped-enable')
        # Real production screen evaluates its actual Orbit constructor again.
        # No synthetic meeting object is inserted into the observer registry.
        renpy.restart_interaction()

    def r13_c4_outer_restored():
        assert not _in_replay
        assert R13_CHARACTER_GRID2_ENABLED and R13_C4_ACTIVE,'Original QA outer store was not restored'
        r13_c4_checkpoint('meeting-outer-store-restored')

    def r13_c4_end():
        global R13_C4_ACTIVE,R13_CHARACTER_GRID2_ENABLED
        R13_C4_ACTIVE=False
        R13_CHARACTER_GRID2_ENABLED=False
        persistent.room13_motion=store.r13_c4_old_motion
        R13_C4_RECORDS.clear()
        renpy.restart_interaction()
        r13_c4_log('end',enabled=r13_g2_enabled())

    def r13_c4_surface(art,size):
        assert tuple(renpy.get_physical_size())==(1280,720),'No post-capture resizing permitted'
        surface=renpy.render_to_surface(art,size[0],size[1],resize=False)
        assert surface.get_size()==size,(surface.get_size(),size)
        assert surface.get_masks()[3],'RGBA capture required'
        return surface,r13_g2_bytes(surface)

    def r13_c4_bad(data,size):
        w,h=size
        assert w%2==h%2==0
        bad=0
        for y in range(0,h,2):
            for x in range(0,w,2):
                i=(y*w+x)*4;p=data[i:i+4]
                bad+=int(p!=data[i+4:i+8] or p!=data[i+w*4:i+w*4+4] or p!=data[i+w*4+4:i+w*4+8])
        return bad

    def r13_c4_expression_begin(person):
        # QA rendering fixture only: use the shipped approved plan/loadability gate.
        store.r13_c4_saved_expression=store.dialogue_expression
        store.r13_c4_saved_beat=store.r13_dialogue_beat
        store.r13_c4_saved_speaker_state=(store.r13_current_pose,store.r13_motion_person,store.dialogue_speaker)
        previous=(store.r13_dialogue_beat or {}).get('talk','neutral')
        emotion='angry' if previous=='joy' else 'joy'
        entry=R13_DIALOGUE_TALK_ART['people'][person]
        assert entry['status']=='approved_runtime'
        frames=entry['profiles']['840']['frames']
        assert emotion in frames and previous in frames
        assert frames[emotion]['file']!=frames[previous]['file']
        packet=(None,'',dict(show=person,expression=emotion))
        r13_dialogue_beat_begin('grid2-qa-render-fixture',0,packet,emotion)
        plan=store.r13_dialogue_beat
        assert plan and plan['person']==person and plan['talk']==emotion
        assert plan['settled'] and not persistent.room13_motion
        import hashlib
        with renpy.file(frames[emotion]['file']) as source:
            source_sha256=hashlib.sha256(source.read()).hexdigest()
        r13_c4_log('expression-fixture',person=person,previous=previous,talk=emotion,source=frames[emotion]['file'],source_sha256=source_sha256,settled=plan['settled'],motion=persistent.room13_motion)
        r13_speaker(person)

    def r13_c4_expression_restore(person):
        store.r13_dialogue_beat=store.r13_c4_saved_beat
        r13_speaker(person,store.r13_c4_saved_expression,pose=store.r13_c4_saved_speaker_state[0])
        assert store.r13_dialogue_beat is store.r13_c4_saved_beat
        assert store.dialogue_expression==store.r13_c4_saved_expression
        assert (store.r13_current_pose,store.r13_motion_person,store.dialogue_speaker)==store.r13_c4_saved_speaker_state

    def r13_c4_capture(context,step):
        records=[(key,value) for (kind,key),value in list(R13_C4_RECORDS.items()) if kind==context]
        assert r13_g2_enabled() and R13_C4_ACTIVE,('Capture requires actual enabled context',context)
        assert records,('No production displayable observed',context)
        if context=='dialogue':
            assert renpy.get_screen('say')
            bounds=renpy.get_image_bounds('r13_visitor',layer='master')
            r13_c4_log('live-dialogue-bounds',bounds=bounds,required=[0,0,1280,720])
            assert bounds is not None and tuple(bounds)==(0,0,1280,720),('Live visitor layer displaced after show',bounds)
        for index,(key,(before,after,size)) in enumerate(records[:12]):
            # Compare the same pre-grid canvas used by production r13_g2_final.
            # Source art can be odd-width; padding is transparent, never rescaling.
            before_canvas=Fixed(before,xysize=size)
            a,raw=r13_c4_surface(before_canvas,size)
            b,data=r13_c4_surface(after,size)
            nz=sum(v>0 for v in data[3::4]);bad=r13_c4_bad(data,size)
            prefix='%s-%s-%02d'%(context,step,index)
            r13_g2_pygame.image.save(a,r13_c4_os.path.join(r13_c4_out(),prefix+'-before.png'))
            r13_g2_pygame.image.save(b,r13_c4_os.path.join(r13_c4_out(),prefix+'-after.png'))
            r13_c4_log('layer',context=context,step=step,key=key,size=size,nonzero_alpha=nz,bad_2x2_blocks=bad,
                capture='exact production object, independently rendered at current state; screen screenshot is separate',
                before='same enabled-path geometry before final grid, not full legacy mode')
            assert nz>0 and any(raw[3::4]) and bad==0,(context,key,nz,bad)
            if context=='dialogue':
                import hashlib
                digest=hashlib.sha256(bytes(data)).hexdigest()
                r13_c4_log('dialogue-render-digest',step=step,sha256=digest)
                if step=='repeat':store.r13_c4_original_render_digest=digest
                elif step=='expression':assert digest!=store.r13_c4_original_render_digest,'Approved expression did not change actual pixels'
                elif step=='restored':assert digest==store.r13_c4_original_render_digest,'Original expression pixels were not restored'


    def r13_c4_field(step):
        assert renpy.get_screen('r13_hub') and not persistent.room13_motion
        offset=r13_world_offset()
        assert offset==int(offset) and int(offset)%2==0,('Camera must preserve world grid phase',offset)
        for actor in r13_stage_people(False):
            if actor['x']+actor['width']<=offset or actor['x']>=offset+1280:continue
            assert renpy.get_displayable('r13_hub','r13_world_'+actor['person']) is not None
            x,y,w,h=map(int,actor['rect']);dx=x-int(actor['x']);dy=y-int(actor['y'])
            visual,rgba=r13_c4_surface(r13_staged_visible_art(actor,still=True),(actor['width'],actor['height']))
            mask,mrgba=r13_c4_surface(r13_actor_hit_mask(actor),(w,h))
            expected=bytes(rgba[((dy+yy)*actor['width']+dx+xx)*4+3] for yy in range(h) for xx in range(w))
            actual=mrgba[3::4]
            mismatch=sum(a!=b for a,b in zip(expected,actual))
            r13_c4_log('field-mask',step=step,person=actor['person'],rect=actor['rect'],alpha_mismatch=mismatch,opaque=sum(v>0 for v in actual))
            assert mismatch==0 and any(actual),'Visible geometry and click mask diverged'
        r13_c4_capture('field',step)

    def r13_c4_clear_profiles():
        for key in list(R13_C4_RECORDS):
            if key[0]=='profile':del R13_C4_RECORDS[key]

    def r13_c4_require_profile_size(size):
        observed=[value[2] for key,value in R13_C4_RECORDS.items() if key[0]=='profile']
        assert tuple(size) in observed,('Actual profile dimensions missing',size,observed)

    class R13C4Choice(object):
        def __init__(self,caption):
            self.caption=caption
            self.action=NullAction()

    def r13_c4_choices():
        return [R13C4Choice(R13_NAMES[p]) for p in ('nabi','resident_bori','resident_teacher','granny')]

# Explicit screen fixture for the real 48x48 four-suspect choice layout.
# This does NOT claim that the corresponding narrative choice was reached.
screen r13_c4_choices_fixture():
    modal True
    zorder 220
    use r13_meeting_choices(r13_c4_choices(),True)
