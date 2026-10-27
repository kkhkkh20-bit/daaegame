init 999 python:
    def r13_qa_settings_offset(end=False):
        widget=renpy.get_displayable("pause_menu","r13_settings_body")
        widget.yadjustment.change(widget.yadjustment.range if end else 0)

    def r13_qa_mixer_matches(widget_id, mixer, expected):
        widget=renpy.get_displayable("pause_menu",widget_id)
        adj=widget.adjustment
        fill=100.0*adj.value/float(adj.range)
        label=renpy.get_displayable("pause_menu",widget_id+"_percent")
        visible="".join(str(part) for part in label.text)
        return (abs(fill-expected)<0.001 if expected==100 else abs(fill-expected)<=0.5) and r13_mixer_percent(mixer)==int(round(fill)) and visible=="%d%%"%r13_mixer_percent(mixer)

testcase settings_typography:
    pause 2.0
    $ persistent.room13_option_tab="reading"
    run Function(r13_set_text_size,"normal")
    run Show("pause_menu")
    pause 0.5
    assert eval (r13_opt_size()==(24 if R13_TYPE_V2 else 22) and r13_opt_title_size()==(28 if R13_TYPE_V2 else 30))
    screenshot "settings-type-01-normal-reading.png"
    click "소리"
    run Function(r13_qa_settings_offset)
    pause 0.3
    screenshot "settings-type-02-normal-sound.png"
    click "화면"
    run Function(r13_qa_settings_offset)
    pause 0.3
    screenshot "settings-type-03-normal-screen.png"
    click "읽기"
    click id "r13_text_size_large"
    run Function(r13_qa_settings_offset)
    pause 0.3
    assert eval (r13_opt_size()==(28 if R13_TYPE_V2 else 26) and r13_opt_title_size()==(32 if R13_TYPE_V2 else 34))
    screenshot "settings-type-04-large-reading-top.png"
    run Function(r13_qa_settings_offset,True)
    pause 0.3
    assert eval (renpy.get_screen("pause_menu").scope["typing_preview"].signature[1]==_r13_say_size())
    screenshot "settings-type-05-large-preview-footer.png"
    click "소리"
    run Function(r13_qa_settings_offset)
    pause 0.3
    screenshot "settings-type-06-large-sound.png"
    click "화면"
    run Function(r13_qa_settings_offset)
    pause 0.3
    screenshot "settings-type-07-large-screen.png"
    click "읽기"
    run Function(r13_qa_settings_offset)
    click id "r13_text_size_small"
    pause 0.3
    assert eval (r13_opt_size()==(22 if R13_TYPE_V2 else 20) and r13_opt_title_size()==(25 if R13_TYPE_V2 else 27))
    screenshot "settings-type-08-small-reading.png"
    click id "r13_text_size_normal"
    run Hide("pause_menu")
