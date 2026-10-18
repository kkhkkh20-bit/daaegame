# Separate native diagnostic: endpoint failures must not mask typography checks.
init 999 python:
    def r13_qa_volume_log(message):
        print("R13_VOLUME_DIAGNOSTIC " + str(message))
        renpy.log("R13_VOLUME_DIAGNOSTIC " + str(message))

    def r13_qa_volume_state(stage):
        import renpy.test.testfocus as tf
        import renpy.test.testmouse as tm
        result={"stage":stage,"raw_pointer":tm.mouse_pos,"mouse":renpy.get_mouse_pos()}
        for widget_id,mixer in (("music_volume","music"),("fx_volume","sfx")):
            w=renpy.get_displayable("pause_menu",widget_id)
            f=tf.focus_from_displayable(w)
            result[widget_id]=dict(value=w.adjustment.value,range=w.adjustment.range,
                raw_volume=_preferences.get_volume(mixer),percent=r13_mixer_percent(mixer),
                width=w.width,height=w.height,thumb_dim=w.thumb_dim,
                gutters=(w.style.fore_gutter,w.style.aft_gutter),
                focus=(f.x,f.y,f.w,f.h) if f else None,
                center=tf.find_position(w,(0.5,0.5)),outside=tf.find_position(w,(1.1,0.5)),
                grabbed=renpy.display.focus.get_grab() is w)
        r13_qa_volume_log(result)

    def r13_qa_volume_point(widget_id, outside=False, left=False):
        import renpy.test.testfocus as tf
        w=renpy.get_displayable("pause_menu",widget_id)
        f=tf.focus_from_displayable(w)
        # SDK 8.5.3 resolves an outside selector point to its top-left fallback.
        # Compute absolute integer positions from the actual rendered geometry.
        return (int(f.x-30 if left else f.x+f.w+30 if outside else f.x+f.w/2),int(f.y+f.h/2))

    def r13_qa_volume_trace_start():
        import inspect
        import renpy.test.testfocus as tf
        import renpy.test.testast as ta
        import renpy.test.testmouse as tm
        Bar=renpy.display.behavior.Bar
        store.r13_qa_volume_original_event=Bar.event
        store.r13_qa_volume_events=[]
        # Log the actual installed SDK implementation, not assumed master behavior.
        for source in (tf.find_position,ta.Drag.execute,Bar.event):
            r13_qa_volume_log("SDK SOURCE " + inspect.getsource(source))
        original=Bar.event
        def traced(self,ev,x,y,st):
            targets=[renpy.get_displayable("pause_menu",key) for key in ("music_volume","fx_volume")]
            tracked=self in targets
            before=(self.adjustment.value,self.is_focused(),renpy.display.focus.get_grab() is self) if tracked else None
            try:
                return original(self,ev,x,y,st)
            finally:
                if tracked and len(store.r13_qa_volume_events)<250:
                    store.r13_qa_volume_events.append(dict(widget=targets.index(self),event=ev.type,
                        xy=(x,y),pointer=tm.mouse_pos,before=before,
                        after=(self.adjustment.value,self.is_focused(),renpy.display.focus.get_grab() is self)))
        Bar.event=traced

    def r13_qa_volume_trace_stop():
        renpy.display.behavior.Bar.event=store.r13_qa_volume_original_event
        for row in store.r13_qa_volume_events:
            r13_qa_volume_log(row)

testcase settings_volume_endpoint:
    pause 2.0
    $ r13_qa_saved_mixers=(_preferences.get_volume("music"),_preferences.get_volume("sfx"))
    $ persistent.room13_option_tab="sound"
    run Function(r13_set_text_size,"normal")
    run Show("pause_menu")
    pause 0.5
    run Function(r13_qa_settings_offset)
    run Function(r13_qa_volume_state,"before-input")
    run Function(r13_qa_volume_trace_start)
    $ r13_qa_music_middle=r13_qa_volume_point("music_volume")
    $ r13_qa_fx_middle=r13_qa_volume_point("fx_volume")
    $ r13_qa_music_end=r13_qa_volume_point("music_volume",True)
    $ r13_qa_fx_end=r13_qa_volume_point("fx_volume",True)
    $ r13_qa_volume_log(("absolute-targets",r13_qa_music_middle,r13_qa_fx_middle,r13_qa_music_end,r13_qa_fx_end))
    click pos (r13_qa_music_middle[0],r13_qa_music_middle[1])
    click pos (r13_qa_fx_middle[0],r13_qa_fx_middle[1])
    pause 0.3
    run Function(r13_qa_volume_state,"after-midpoint-click")
    screenshot "settings-volume-50-percent.png"
    $ r13_qa_volume_half_ok=(r13_qa_mixer_matches("music_volume","music",50) and r13_qa_mixer_matches("fx_volume","sfx",50))
    # Real pointer drag with no selector on the outside endpoint; preserves grab.
    drag pos (r13_qa_music_middle[0],r13_qa_music_middle[1]) to pos (r13_qa_music_end[0],r13_qa_music_end[1]) steps 20
    run Function(r13_qa_volume_state,"after-music-outside-drag")
    drag pos (r13_qa_fx_middle[0],r13_qa_fx_middle[1]) to pos (r13_qa_fx_end[0],r13_qa_fx_end[1]) steps 20
    pause 0.3
    run Function(r13_qa_volume_state,"after-both-outside-drags")
    screenshot "settings-volume-endpoint-before-assert.png"
    $ r13_qa_volume_full_ok=(r13_qa_mixer_matches("music_volume","music",100) and r13_qa_mixer_matches("fx_volume","sfx",100))
    # Endpoint legibility at the largest UI size, with unchanged mixer curve.
    run Function(r13_set_text_size,"large")
    pause 0.3
    run Function(r13_qa_volume_state,"large-100")
    screenshot "settings-volume-large-100.png"
    $ r13_qa_volume_large_full_ok=(r13_qa_mixer_matches("music_volume","music",100) and r13_qa_mixer_matches("fx_volume","sfx",100))
    $ r13_qa_music_middle=r13_qa_volume_point("music_volume")
    $ r13_qa_fx_middle=r13_qa_volume_point("fx_volume")
    $ r13_qa_music_left=r13_qa_volume_point("music_volume",left=True)
    $ r13_qa_fx_left=r13_qa_volume_point("fx_volume",left=True)
    click pos (r13_qa_music_middle[0],r13_qa_music_middle[1])
    click pos (r13_qa_fx_middle[0],r13_qa_fx_middle[1])
    pause 0.3
    run Function(r13_qa_volume_state,"large-50")
    screenshot "settings-volume-large-50.png"
    $ r13_qa_volume_large_half_ok=(r13_qa_mixer_matches("music_volume","music",50) and r13_qa_mixer_matches("fx_volume","sfx",50))
    drag pos (r13_qa_music_middle[0],r13_qa_music_middle[1]) to pos (r13_qa_music_left[0],r13_qa_music_left[1]) steps 20
    drag pos (r13_qa_fx_middle[0],r13_qa_fx_middle[1]) to pos (r13_qa_fx_left[0],r13_qa_fx_left[1]) steps 20
    pause 0.3
    run Function(r13_qa_volume_state,"large-0")
    screenshot "settings-volume-large-0.png"
    $ r13_qa_volume_large_zero_ok=(r13_qa_mixer_matches("music_volume","music",0) and r13_qa_mixer_matches("fx_volume","sfx",0) and _preferences.get_volume("music")==0 and _preferences.get_volume("sfx")==0)
    run Function(r13_set_text_size,"normal")
    pause 0.3
    run Function(r13_qa_volume_state,"normal-0")
    screenshot "settings-volume-normal-0.png"
    $ r13_qa_volume_zero_ok=(r13_qa_mixer_matches("music_volume","music",0) and r13_qa_mixer_matches("fx_volume","sfx",0) and _preferences.get_volume("music")==0 and _preferences.get_volume("sfx")==0)
    run Function(r13_qa_volume_trace_stop)
    $ _preferences.set_volume("music",r13_qa_saved_mixers[0])
    $ _preferences.set_volume("sfx",r13_qa_saved_mixers[1])
    run Hide("pause_menu")
    assert eval (r13_qa_volume_half_ok)
    assert eval (r13_qa_volume_full_ok)
    assert eval (r13_qa_volume_large_full_ok and r13_qa_volume_large_half_ok and r13_qa_volume_large_zero_ok and r13_qa_volume_zero_ok)
