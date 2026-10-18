# Diagnostic-only; must be excluded from release builds. Requires grid2 helper.
# Run at actual 1280x720 window, after first interaction, in disposable QA HOME.
init 999 python:
    import os as r13_g2_os
    import json as r13_g2_json
    import pygame_sdl2 as r13_g2_pygame
    import inspect as r13_g2_inspect

    def r13_g2_out():
        folder=r13_g2_os.path.join(r13_g2_os.environ.get("ROOM13_QA_OUT","/tmp/room13-qa"),"character-grid2")
        r13_g2_os.makedirs(folder,exist_ok=True)
        return folder

    def r13_g2_log(event,**fields):
        fields["event"]=event
        with open(r13_g2_os.path.join(r13_g2_out(),"runtime.jsonl"),"a") as f:
            f.write(r13_g2_json.dumps(fields,default=str)+"\n")

    def r13_g2_signature(fn):
        try:return str(r13_g2_inspect.signature(fn))
        except Exception as error:return "unavailable: "+str(error)

    def r13_g2_prepare_physical_window():
        # Diagnostic-only window resize BEFORE capture, never a screenshot resize.
        info=renpy.get_renderer_info()
        r13_g2_log("window_before_request",physical_size=renpy.get_physical_size(),renderer=info)
        maximum=info.get("max_window_size",(0,0))
        assert maximum[0]>=1280 and maximum[1]>=720,"Start Xvfb with1920x1080x24; renderer cannot fit native1280x720"
        renpy.set_physical_size((1280,720))
        r13_g2_log("window_resize_requested",requested=[1280,720])

    def r13_g2_runtime_probe():
        r13_g2_log("startup",engine_version=getattr(renpy,"version_string",None),
            engine_version_tuple=getattr(renpy,"version_tuple",None),
            virtual_viewport=[config.screen_width,config.screen_height],
            physical_window=renpy.get_physical_size(),
            renderer=renpy.get_renderer_info(),
            render_to_surface_signature=r13_g2_signature(renpy.render_to_surface),
            tostring_signature=r13_g2_signature(getattr(r13_g2_pygame.image,"tostring",None)),
            rgba_reader=("image.tostring" if callable(getattr(r13_g2_pygame.image,"tostring",None)) else "Surface.get_at exact RGBA"),
            pygame_module_file=getattr(r13_g2_pygame,"__file__",None),
            dialogue_profile_signature=r13_g2_signature(r13_dialogue_source_profile),
            final_helper_available=callable(r13_grid2_final_character_layer),
            preview_enabled=bool(store.R13_CHARACTER_GRID2_PREVIEW))
        assert tuple(renpy.get_physical_size())==(1280,720),"Window resize not established; see physical_window, do not rescale capture"
        # Isolate API/alpha support before touching character assets.
        probe=renpy.render_to_surface(Fixed(Solid("#34567880",xsize=2,ysize=2),xysize=(1280,720)),1280,720,resize=False)
        data=r13_g2_bytes(probe)
        r13_g2_log("api_probe",capture_size=probe.get_size(),rgba_bytes=len(data),
            expected_rgba_bytes=probe.get_width()*probe.get_height()*4,
            masks=probe.get_masks(),origin_rgba=list(data[:4]),far_corner_rgba=list(data[-4:]),
            transparent_supported=bool(probe.get_masks()[3] and data[-1]==0),
            partial_alpha_supported=bool(probe.get_masks()[3] and 0<data[3]<255))
        assert len(data)==probe.get_width()*probe.get_height()*4,"pygame_sdl2 RGBA byte-count mismatch"
        assert probe.get_masks()[3] and data[-1]==0 and 0<data[3]<255,"Transparent/partial-alpha surface unsupported; see api_probe, no RGB-only fallback"
        assert probe.get_size()==(1280,720),"Need native1280x720 capture; inspect runtime.jsonl"

    def r13_g2_bytes(surface):
        # pygame_sdl2 is NOT pygame2: upstream image.pyx has no tostring.
        # Use it only if SDK provides it; otherwise exact Surface.get_at reads.
        convert=getattr(r13_g2_pygame.image,"tostring",None)
        if callable(convert):return convert(surface,"RGBA")
        w,h=surface.get_size();data=bytearray(w*h*4);get=surface.get_at
        for y in range(h):
            for x in range(w):
                i=(y*w+x)*4;c=get((x,y))
                data[i]=c[0];data[i+1]=c[1];data[i+2]=c[2];data[i+3]=c[3]
        return bytes(data)

    def r13_g2_repeat(surface,data=None):
        w,h=surface.get_size()
        assert (w,h)==(1280,720),"Set native viewport1280x720; never resize screenshot for this test"
        data=r13_g2_bytes(surface) if data is None else data;bad=0
        for y in range(0,h,2):
            for x in range(0,w,2):
                p=(y*w+x)*4;v=data[p:p+4]
                if any(data[q:q+4]!=v for q in (p+4,p+w*4,p+w*4+4)):bad+=1
        return bad

    def r13_g2_capture(name,layer):
        folder=r13_g2_out()
        r13_g2_log("capture_begin",name=name)
        before=renpy.render_to_surface(layer,1280,720,st=1.2,at=1.2,resize=False)
        r13_g2_log("before_surface",name=name,size=before.get_size(),masks=before.get_masks())
        assert before.get_size()==(1280,720),"Capture must be native1:1; resize=True introduces smoothing"
        old=store.R13_CHARACTER_GRID2_PREVIEW
        try:
            store.R13_CHARACTER_GRID2_PREVIEW=True
            art=r13_grid2_final_character_layer(layer)
            after=renpy.render_to_surface(art,1280,720,st=1.2,at=1.2,resize=False)
        finally:store.R13_CHARACTER_GRID2_PREVIEW=old
        r13_g2_log("after_surface",name=name,size=after.get_size(),masks=after.get_masks())
        before_bytes=r13_g2_bytes(before);after_bytes=r13_g2_bytes(after)
        bad=r13_g2_repeat(after,after_bytes)
        r13_g2_pygame.image.save(before,r13_g2_os.path.join(folder,name+"-before.png"))
        r13_g2_pygame.image.save(after,r13_g2_os.path.join(folder,name+"-after.png"))
        a=before_bytes[3::4];b=after_bytes[3::4]
        result=dict(name=name,viewport=[1280,720],bad_2x2_blocks=bad,
            alpha_capture_available=bool(before.get_masks()[3] and after.get_masks()[3] and 0 in a and 0 in b),
            before_nonzero_alpha=sum(v>0 for v in a),after_nonzero_alpha=sum(v>0 for v in b),
            before_partial_alpha=sum(0<v<255 for v in a),after_partial_alpha=sum(0<v<255 for v in b),
            lost_opaque_pixels=sum(x>=128 and y<128 for x,y in zip(a,b)),
            new_opaque_pixels=sum(x<128 and y>=128 for x,y in zip(a,b)),
            eyes_hands_review="REQUIRED: compare paired captures; exact grid does not prove detail preservation")
        with open(r13_g2_os.path.join(folder,"metrics.jsonl"),"a") as f:f.write(r13_g2_json.dumps(result)+"\n")
        assert result["before_nonzero_alpha"]>0 and result["after_nonzero_alpha"]>0,("Empty character capture",result)
        assert result["alpha_capture_available"],("Capture API did not preserve transparent RGBA; no RGB-only pass",result)
        assert bad==0,("Flatten+Transform did not produce exact final2x2 RGBA",result)
        return result

    def r13_g2_dialogue_cases():
        r13_g2_runtime_probe()
        # Use actual current registry and shipped runtime exports, never560 proof PNGs.
        for person in ("resident_bori","nabi","resident_teacher"):
            profile=r13_dialogue_source_profile(person,"neutral",840)
            assert profile,(person,"missing840 profile")
            for emotion in ("neutral","angry"):
                frame=profile["frames"][emotion]
                assert renpy.loadable(frame["file"]),frame
                # Current profile geometry; no source smoothing, no legacy grid.
                piece=Fixed(Transform(frame["file"],xpos=frame["offset"][0],ypos=frame["offset"][1],
                    zoom=frame.get("scale",1.0),nearest=True,subpixel=False),xysize=tuple(profile["canvas"]))
                for depth in (1.0,.82):
                    # Transparent actor-only composition. Camera transform is INSIDE final pass.
                    actor=Transform(piece,zoom=depth,xzoom=(1.0 if depth==1 else .96),
                        xcenter=640,ypos=108,nearest=True,subpixel=False)
                    layer=Fixed(actor,xysize=(1280,720))
                    r13_g2_capture(person+"-"+emotion+"-"+str(depth),layer)

    def r13_g2_check_live_masks():
        # Call only after real investigation hub is ready; does not change state.
        actors=r13_stage_people(False)
        assert actors,"No naturally staged actors"
        offset=r13_world_offset();records=[]
        for actor in actors:
            x,y,w,h=actor["rect"]
            mask=renpy.render(r13_actor_hit_mask(actor),w,h,1.2,1.2)
            opaque=[]
            for ly in range(2,int(h)-2,4):
                for lx in range(2,int(w)-2,4):
                    if mask.is_pixel_opaque(lx,ly):opaque.append([int(x+lx-offset),int(y+ly)])
            assert opaque,(actor["person"],"empty production click mask")
            records.append(dict(person=actor["person"],pose=actor["pose"],mask_samples=len(opaque),
                note="Existing mask sampled only. Actual rendered-body click -> topic -> return still required; no success claimed."))
        return records

testcase character_grid2_source_proof:
    pause 2.0
    run Function(r13_g2_prepare_physical_window)
    pause 1.0
    run Function(r13_g2_dialogue_cases)
