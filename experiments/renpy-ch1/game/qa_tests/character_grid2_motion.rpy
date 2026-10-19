# QA only. Observe the actual returned Render, never synthesize a timestamp.
init 995 python:
    R13_M_ARMED=None
    R13_M_SAMPLES=[]
    R13_M_HOOKS=[]
    R13_M_CLONE_CLASSES={}
    R13_M_TRACE=[]
    R13_M_VIEW=None
    R13_M_PHASE=None
    _r13_m_world_view=r13_meeting_world_view
    _r13_m_beat_render=R13DialogueBeat.render

    def r13_meeting_world_view(claim,focus):
        global R13_M_VIEW
        value=_r13_m_world_view(claim,focus)
        if R13_M_ARMED=='meeting':R13_M_VIEW=value
        return value

    def r13_m_beat_render(self,width,height,st,at):
        global R13_M_PHASE
        elapsed=0.0 if self.started_st is None else max(0.0,st-self.started_st)
        phase='talk' if self.finished or r13_dialogue_phase(self.plan,elapsed,renpy.is_skipping(),persistent.room13_motion)==self.plan['talk'] else 'reaction'
        result=_r13_m_beat_render(self,width,height,st,at)
        if R13_M_ARMED=='dialogue':R13_M_PHASE=phase
        return result
    R13DialogueBeat.render=r13_m_beat_render

    def r13_m_watch(result,context,key,size):
        if R13_M_ARMED==context and R13_C4_ACTIVE and r13_g2_enabled() and not renpy.predicting():
            if any(obj is result for obj in R13_M_HOOKS):return result
            cls=type(result)
            if cls not in R13_M_CLONE_CLASSES:
                original_call=cls.__call__
                R13_M_CLONE_CLASSES[cls]=original_call
                def cloned(self,*args,**kwargs):
                    duplicate=original_call(self,*args,**kwargs)
                    info=getattr(self,'_r13_m_watch_info',None)
                    if info and R13_M_ARMED==info[0]:r13_m_watch(duplicate,*info)
                    return duplicate
                cls.__call__=cloned
            result._r13_m_watch_info=(context,key,size)
            original=result.render
            def observed(width,height,st,at):
                rendered=original(width,height,st,at)
                if R13_M_ARMED==context and not renpy.predicting():
                    now=renpy.display.core.get_time()
                    meta=dict(context=context,key=key,size=tuple(size),st=st,at=at,clock=now,
                        phase=R13_M_PHASE if context=='dialogue' else None,
                        view=R13_M_VIEW if context=='meeting' else None)
                    if len(R13_M_TRACE)<120:R13_M_TRACE.append(dict(meta))
                    # Avoid reading back the initial integer view before the short pan.
                    # Preserve all actual view metadata, and capture one intermediate + settled.
                    capture=True
                    if context=='meeting' and meta['view'] and meta['view'][1]:
                        fractional=abs(meta['view'][0]-round(meta['view'][0]))>0.000001
                        capture=fractional and not any(row[2]['view'] and row[2]['view'][1] for row in R13_M_SAMPLES)
                    # Keep the first actual frame per phase/time bucket.
                    bucket=(key,meta['phase'],bool(meta['view'] and meta['view'][1]),int(st*10))
                    if capture and not any(row[0]==bucket for row in R13_M_SAMPLES) and len(R13_M_SAMPLES)<20:
                        # Render.kill clears prior graphs even with Python references.
                        # Freeze pixels now, before this actual frame can be swept.
                        meta['render_killed_before_capture']=bool(getattr(rendered,'killed',False))
                        assert not meta['render_killed_before_capture']
                        surface=renpy.render_to_surface(rendered,resize=False)
                        R13_M_SAMPLES.append((bucket,surface,meta))
                return rendered
            result.render=observed
            R13_M_HOOKS.append(result)
        return result

    def r13_m_arm(context):
        global R13_M_ARMED,R13_M_VIEW,R13_M_PHASE
        assert R13_C4_ACTIVE and r13_g2_enabled() and R13_M_ARMED is None
        store.r13_m_old_motion=persistent.room13_motion
        persistent.room13_motion=True
        R13_M_SAMPLES.clear();R13_M_TRACE.clear();R13_M_VIEW=None;R13_M_PHASE=None
        R13_M_ARMED=context
        r13_c4_log('motion-arm',context=context,field_idle=R13_FIELD_IDLE,skipping=renpy.is_skipping(),motion=persistent.room13_motion)
        assert not renpy.is_skipping()
        renpy.restart_interaction()

    def r13_m_dialogue_start(person):
        store.r13_m_saved_beat=store.r13_dialogue_beat
        store.r13_m_saved_expression=store.dialogue_expression
        store.r13_m_saved_pose=store.r13_current_pose
        entry=R13_DIALOGUE_TALK_ART['people'][person]
        assert entry['status']=='approved_runtime'
        for h in ('560','760','840'):
            for key in ('surprise_react','surprise_talk'):
                frame=entry['profiles'][h]['frames'][key]
                assert frame['file'].startswith('assets/dialogue-source-master/') and renpy.loadable(frame['file'])
        # Render-only plan, no authored dialogue cue is added or changed.
        cue=dict(reviewed=True,person=person,text='',emotion='surprise',reaction=True)
        plan=r13_dialogue_plan('grid2-motion-fixture',0,(person,''),'surprise',{'grid2-motion-fixture':{'0':cue}},R13_DIALOGUE_TALK_ART['people'])
        assert plan and plan['react']=='surprise_react' and not plan['settled']
        store.r13_dialogue_beat=plan
        r13_speaker(person)
        import hashlib
        evidence={}
        for key in ('surprise_react','surprise_talk'):
            path=entry['profiles']['840']['frames'][key]['file']
            with renpy.file(path) as source:evidence[key]=dict(path=path,sha256=hashlib.sha256(source.read()).hexdigest())
        r13_c4_log('motion-dialogue-fixture',person=person,frames=evidence)

    def r13_m_finish(context):
        global R13_M_ARMED
        assert R13_M_ARMED==context and persistent.room13_motion
        R13_M_ARMED=None
        for obj in R13_M_HOOKS:
            del obj.render
            del obj._r13_m_watch_info
        for cls,original_call in R13_M_CLONE_CLASSES.items():cls.__call__=original_call
        R13_M_CLONE_CLASSES.clear()
        R13_M_HOOKS.clear()
        rows=list(R13_M_SAMPLES)
        R13_M_SAMPLES.clear()
        persistent.room13_motion=store.r13_m_old_motion
        trace=list(R13_M_TRACE);R13_M_TRACE.clear()
        r13_c4_log('motion-observer-summary',context=context,sample_count=len(rows),samples=[row[2] for row in rows],trace=trace)
        previous={}
        for index,(_,surface,meta) in enumerate(rows):
            # This owned Surface was frozen in the real render callback.
            # No old Render or displayable is re-rendered during analysis.
            assert tuple(renpy.get_physical_size())==(1280,720)
            assert surface.get_size()==meta['size'] and surface.get_masks()[3]
            data=r13_g2_bytes(surface);bad=r13_c4_bad(data,meta['size'])
            assert any(data[3::4]) and bad==0,(context,index,bad)
            path=r13_c4_os.path.join(r13_c4_out(),'motion-%s-%02d.png'%(context,index))
            r13_g2_pygame.image.save(surface,path)
            old=previous.get(meta['key'])
            changed=sum(data[i:i+4]!=old[i:i+4] for i in range(0,len(data),4)) if old is not None and len(old)==len(data) else None
            previous[meta['key']]=data
            r13_c4_log('actual-motion-render',index=index,bad_2x2_blocks=bad,changed_rgba_pixels=changed,capture='actual production Render frozen to Surface in same callback, no re-render',**meta)
        assert rows,('No actual production render observed',context)
        if context=='dialogue':assert {'reaction','talk'}<=set(row[2]['phase'] for row in rows),'Missing real reaction/settled render'
        if context=='meeting':
            views=[row['view'][0] for row in trace if row['view']]
            assert len(set(views))>=3,'Missing distinct actual camera positions'
            assert any(row[2]['view'] and row[2]['view'][1] and abs(row[2]['view'][0]-round(row[2]['view'][0]))>0.000001 for row in rows),'Missing actual intermediate camera render'
            assert any(row[2]['view'] and not row[2]['view'][1] for row in rows),'Missing actual settled camera render'
        persistent.room13_motion=store.r13_m_old_motion
        R13_M_SAMPLES.clear()
        renpy.restart_interaction()
        r13_c4_log('motion-preference-restored',context=context,value=persistent.room13_motion)

    def r13_m_dialogue_restore(person):
        store.r13_dialogue_beat=store.r13_m_saved_beat
        r13_speaker(person,store.r13_m_saved_expression,pose=store.r13_m_saved_pose)
        assert store.r13_dialogue_beat is store.r13_m_saved_beat
        assert store.dialogue_expression==store.r13_m_saved_expression and store.r13_current_pose==store.r13_m_saved_pose
