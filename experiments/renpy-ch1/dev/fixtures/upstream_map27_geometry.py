# Verbatim upstream assertion/geometry function: game/systems/room13_map_action27.rpy
# PR18C Git blob 9497a714342e42de060b6cf6dcb7f4a631984ab7; no display or image execution.
def r13_map27_geometry(actor,spec,variant,width):
    # Source anchors are crop-relative pixels. One uniform scale, applied once.
    # Desired height already includes perspective and pose stature; never resize by feet again.
    cw,ch=spec["crop"][2:]
    scale=float(variant["render_height"])/ch
    ax,ay=spec["anchors"][variant["anchor"]]
    tx,ty=variant["target"]
    x=int(round(tx-ax*scale));y=int(round(ty-ay*scale))
    w=int(round(cw*scale));h=int(round(ch*scale))
    for name,target in variant.get("secondary_targets",{}).items():
        sx,sy=spec["anchors"][name]
        if max(abs(x+sx*scale-target[0]),abs(y+sy*scale-target[1]))>variant.get("contact_tolerance",6):
            raise ValueError("map27 secondary contact mismatch: "+name)
    left=max(0,x);top=max(0,y);right=min(width,x+w);bottom=min(720,y+h)
    if right<=left or bottom<=top:raise ValueError("map27 actor outside scene")
    changed=dict(actor)
    changed.update(x=x,y=y,width=w,height=h,rect=[left,top,right-left,bottom-top],
        depth=variant.get("depth",y+h),slot=None,contact=spec.get("contact","standing"),
        occlusion=[],map27_occlusion=variant.get("occlusion",[]),
        map27_keepouts=[[(x+px*scale,y+py*scale) for px,py in poly] for poly in spec.get("foreground_parts",[])])
    return changed
