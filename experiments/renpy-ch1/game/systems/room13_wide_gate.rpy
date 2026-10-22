# Wider gate art (owner 2026-10-22: "맵을 새로 넓게 그려서 만들어야지"). The new 2560x960 picture
# keeps the old 1920x720 gate unchanged at (320,200) and continues it above, below and to both
# sides, so the gate can be drawn at 75% and still fill the whole screen (no strip below).
# Every authored gate coordinate moves by the same (320,200); nothing about the objects or
# the story changes. A time of day whose wide picture is not delivered yet shows its old
# picture at (320,200) over the morning extension.
init 59 python:
    R13_WIDE_GATE_DIR="assets/gate-wide/"
    R13_WIDE_GATE_SHIFT=(320,200)

    def _r13_wide_shift_rect(r):
        return [r[0]+R13_WIDE_GATE_SHIFT[0],r[1]+R13_WIDE_GATE_SHIFT[1]]+list(r[2:])

    def _r13_wide_gate():
        spec=R13_WORLD_LAYOUTS.get("gate")
        if not spec or spec.get("width")!=1920 or not renpy.loadable(R13_WIDE_GATE_DIR+"gate-wide-morning.webp"):return
        dx,dy=R13_WIDE_GATE_SHIFT
        old_files=dict(spec["files"])
        files={}
        for period,path in old_files.items():
            wide=R13_WIDE_GATE_DIR+"gate-wide-%s.webp"%period
            if renpy.loadable(wide):files[period]=wide
            else:
                name="r13_gate_wide_fallback_"+period
                renpy.image(name,Composite((2560,960),(0,0),R13_WIDE_GATE_DIR+"gate-wide-morning.webp",
                    (dx,dy),Transform(path,size=(1920,720),nearest=True)))
                files[period]=name
        spec["files"]=files
        spec["width"]=2560;spec["height"]=960
        spec["initial_x"]=spec.get("initial_x",0)+dx
        for key in ("objects","late_objects"):
            if key in spec:spec[key]={k:_r13_wide_shift_rect(v) for k,v in spec[key].items()}
        for key in ("documents","documents_crop"):
            if key in spec:spec[key]=_r13_wide_shift_rect(spec[key])
        for key in ("critical","floors","slots"):
            if key in spec:spec[key]=[_r13_wide_shift_rect(v) for v in spec[key]]
        for key in ("positions","pose_positions"):
            if key in spec:spec[key]={k:_r13_wide_shift_rect(v) for k,v in spec[key].items()}
        a,b=R13_WIDE_GATE_PERSPECTIVE
        spec["perspective"]=[a,b-a*dy]  # same standing height for the same spot of the old picture
        spec["wide_shift"]=[dx,dy]
    R13_WIDE_GATE_PERSPECTIVE=(0.217,94)
    _r13_wide_gate()
    r13_field_zoom_init()
