# Version1, opt-in candidate only. Source masters/identities remain unchanged.
# Runtime pixel format is NOT a substitute for art-direction review.
init 57 python:
    import math as r13_g2_math
    R13_CHARACTER_GRID2_ENABLED = False
    R13_CHARACTER_GRID2_VERSION = 1

    def r13_g2_enabled():
        return bool(R13_CHARACTER_GRID2_ENABLED)

    def r13_g2_snap(value):
        return int(r13_g2_math.floor(float(value)/2.0+.5))*2

    def r13_g2_extent(value):
        return max(2,int(r13_g2_math.ceil(float(value)/2.0))*2)

    def r13_g2_final(art,size=(1280,720)):
        if not r13_g2_enabled():return art
        w,h=map(int,size)
        assert w>0 and h>0 and w%2==h%2==0,"Final grid requires even bounds"
        canvas=Fixed(art,xysize=(w,h))
        low=Transform(canvas,xysize=(w//2,h//2),nearest=True,subpixel=False,rotate_pad=False)
        return Transform(Flatten(low),xysize=(w,h),nearest=True,subpixel=False,rotate_pad=False)

    def r13_g2_positioned(art,x,y,center=True):
        positioned=Transform(art,xpos=x,xanchor=(.5 if center else 0),ypos=y)
        return r13_g2_final(Fixed(positioned,xysize=(1280,720))) if r13_g2_enabled() else positioned

    def r13_g2_profile_transform(art,**kwargs):
        # Registry avatar files are already approved face crops. No guessed
        # full-body face rectangle; no source mutation or alpha threshold.
        # Text/question-mark placeholders are deliberately excluded.
        original=Transform(art,**kwargs)
        if not r13_g2_enabled() or not isinstance(art,str):return original
        size=kwargs.get("xysize",kwargs.get("size"))
        if not size:return original
        w,h=map(r13_g2_extent,size)
        opts=dict(kwargs);opts.pop("size",None);opts.pop("xysize",None)
        opts.update(nearest=True,subpixel=False)
        return r13_g2_final(Transform(art,xysize=(w,h),**opts),(w,h))

    def r13_g2_actor_geometry(actor,world_width):
        # Copy only: no stage cache/save/metadata mutation. Retain raw source
        # dimensions, snap feet at most1px, pad rather than rescale canvas.
        result=dict(actor)
        w,h=actor["width"],actor["height"]
        result["grid2_source_size"]=(w,h)
        result["width"]=r13_g2_extent(w);result["height"]=r13_g2_extent(h)
        result["x"]=r13_g2_snap(actor["x"])
        result["y"]=r13_g2_snap(actor["y"]+h)-result["height"]
        x,y=result["x"],result["y"];w,h=result["width"],result["height"]
        left,top=max(0,x),max(0,y);right,bottom=min(world_width,x+w),min(720,y+h)
        result["rect"]=[left,top,max(1,right-left),max(1,bottom-top)]
        result["depth"]=y+h
        return result

# Wrap the final source/occlusion selection AFTER all authored map providers.
init 980 python:
    _r13_g2_stage_people = r13_stage_people
    _r13_g2_visible_art = r13_staged_visible_art

    def r13_stage_people(entry=False):
        actors=_r13_g2_stage_people(entry)
        if not r13_g2_enabled():return actors
        return sorted([r13_g2_actor_geometry(a,r13_world_width()) for a in actors],key=lambda a:a["depth"])

    def r13_staged_visible_art(actor,still=False):
        art=_r13_g2_visible_art(actor,still)
        if not r13_g2_enabled():return art
        # Furniture/map27 masks and raw idle motion already applied. Drawing
        # and r13_actor_hit_mask both call this exact function; no second mask.
        return r13_g2_final(art,(actor["width"],actor["height"]))
