# Resource-gated dialogue direction. No held art is registered here.
default r13_dialogue_beat = None

init 170 python:
    R13_DIALOGUE_B_ART = json.load(renpy.file("assets/room13-dialogue-b-primary50.json"))
    # 2026-10-26 소유자: 인물 그림은 흰 테두리 스티커 없이 간다. B 표정 50장은 스티커라 끄고,
    # 테두리 없는 원래 대화 그림으로 돌아간다. 2026-10-26 받은 전신 묶음으로 바꾼 뒤 다시 켠다.
    R13_DIALOGUE_B_ART_ON = False
    R13_DIALOGUE_BEATS = json.load(renpy.file("assets/room13-dialogue-beats.json"))
    R13_DIALOGUE_TALK_ART = json.load(renpy.file("assets/room13-dialogue-talk-art.json"))
    # 2026-10-26 도트 통일 때 새로 든 인물(판설·아랫길 노인). 승인 59명 표와 나눠 두고 여기서 합친다.
    R13_DIALOGUE_TALK_ART["people"].update(json.load(renpy.file("assets/room13-dialogue-talk-art-extra.json"))["people"])
    # 원래 도트 등록·reviewed beat는 유지하고, 직접 상대를 보는 대화 원본만 별도로 선택한다.
    R13_DIALOGUE_PLAYER_FACING=json.load(renpy.file("assets/room13-dialogue-player-facing.json"))
    _r13_player_facing_ready={}
    # 원화·감정·자세는 그대로 두고, 최종 source 프로필의 표시 키만 현장 키에 맞춘다.
    R13_DIALOGUE_SIZE_FIT=json.load(renpy.file("assets/room13-dialogue-size-fit.json"))
    _r13_dialogue_size_cache={}

    def r13_dialogue_size_profiles(person,profiles,context_key=None):
        table=globals().get("R13_DIALOGUE_SIZE_FIT",{})
        row=table.get("contexts",{}).get(context_key) if context_key else table.get("people",{}).get(person)
        if not row:return profiles
        cache=globals().get("_r13_dialogue_size_cache",{})
        key=(person,context_key,id(profiles))
        cached=cache.get(key)
        if cached and cached[0] is profiles:return cached[1]
        signature={h:dict(canvas=p["canvas"],frames={k:[f["file"],f["offset"],f.get("scale",1.0)] for k,f in p["frames"].items()}) for h,p in profiles.items()}
        # 승인 원본·프로필을 다시 납품하면 오래된 크기표를 임의로 적용하지 않는다.
        result=row["profiles"] if signature==row["input_profiles"] else profiles
        cache[key]=(profiles,result)
        return result


    def r13_dialogue_plan(identity, index, packet, pose, cues, people, binding=None):
        """Exact text/speaker/scene binding; never infer emotion from keywords."""
        if pose not in R13_FULLBODY_PLAIN or len(packet) < 2:
            return None
        cue = (binding.get("rows", {}).get(str(index)) if binding.get("identity")==identity else None) if binding is not None else cues.get(identity, {}).get(str(index))
        if not cue or not cue.get("reviewed") or (cue.get("person"), cue.get("text")) != tuple(packet[:2]):
            return None
        person = packet[0]
        entry = people.get(person, {})
        if entry.get("status") != "approved_runtime" or entry.get("stance") != "standing" or entry.get("gaze") != "player" or entry.get("art_style") != "storybook_source" or entry.get("source_kind") != "source_master":
            return None
        emotion = cue["emotion"]
        if emotion not in ("neutral","joy","angry","anxious","surprise"):
            return None
        talk = "surprise_talk" if emotion == "surprise" else emotion
        profiles = entry.get("profiles", {})
        if not all(talk in profiles.get(str(h), {}).get("frames", {}) for h in (560,760,840)):
            return None
        react = "surprise_react" if emotion == "surprise" and cue.get("reaction") else None
        if react and not all(react in profiles[str(h)]["frames"] for h in (560,760,840)):
            react = None
        return dict(person=person, talk=talk, react=react, settled=not bool(react), duration=.35)

    def r13_dialogue_narration_plan(packet, people):
        """Use an explicit authored show/expression, never infer from narration text."""
        if len(packet)<3 or packet[0] is not None or not isinstance(packet[2],dict):
            return None
        meta=packet[2]
        if not meta.get("show") or "expression" not in meta:
            return None
        # Authored actions (offer_lantern, door_peek, etc.) keep their own art.
        pose=meta.get("pose") or meta["expression"]
        cue=dict(reviewed=True,person=meta["show"],text=packet[1],emotion=meta["expression"],reaction=False)
        return r13_dialogue_plan("narration-show",0,(meta["show"],packet[1]),pose,{"narration-show":{"0":cue}},people)

    def r13_dialogue_beat_begin(identity, index, packet, pose):
        # New lines (including narration and POV replies) invalidate the old reaction.
        store.r13_dialogue_beat = None
        if getattr(store,"r13_meeting_active",False) or getattr(store,"r13_thought_active",False):
            return
        plan = r13_dialogue_plan(identity,index,packet,pose,R13_DIALOGUE_BEATS["lines"],R13_DIALOGUE_TALK_ART["people"],getattr(store,"r13_dialogue_binding",None))
        if plan is None:
            plan=r13_dialogue_narration_plan(packet,R13_DIALOGUE_TALK_ART["people"])
        if plan:
            entry=R13_DIALOGUE_TALK_ART["people"][plan["person"]]
            if not all(frame["file"].startswith("assets/dialogue-source-master/") and renpy.loadable(frame["file"]) for profile in entry["profiles"].values() for frame in profile["frames"].values()):
                return
            if renpy.is_skipping() or renpy.in_rollback() or not persistent.room13_motion:
                plan["settled"]=True
            store.r13_dialogue_beat=plan

    def r13_dialogue_beat_settle():
        if store.r13_dialogue_beat:
            store.r13_dialogue_beat=dict(store.r13_dialogue_beat,settled=True)

    def r13_dialogue_beat_after_load():
        # Loading must never replay a saved flinch, including a restored say interaction.
        r13_dialogue_beat_settle()

    def r13_dialogue_beat_ready(person):
        return bool(store.r13_dialogue_beat and store.r13_dialogue_beat["person"]==person)

    def r13_dialogue_phase(plan, elapsed, skipping=False, motion=True):
        return plan["talk"] if plan["settled"] or skipping or not motion or elapsed>=plan["duration"] else plan["react"]

    class R13DialogueBeat(renpy.Displayable):
        def __init__(self,plan,profile,**kwargs):
            super(R13DialogueBeat,self).__init__(**kwargs)
            self.plan=plan
            self.finished=False
            self.started_st=None
            self.frames={}
            # 2026-10-28 전체 화면 시험(ep6_altar): 아빠의 말 줄에 듣는 사람을 세우면서, 앞 화자의 표정 계획
            # (empathetic_confusion)이 그 표정이 없는 사람 그림에 걸려 KeyError 로 멈췄다. 없는 표정은 neutral 로 그린다.
            # 계획은 store 와 같은 dict 라 그려진 뒤 settled 가 거기 남아야 한다. 바꿀 때만 사본을 쓴다.
            if any(plan.get(slot) and plan[slot] not in profile["frames"] for slot in ("talk","react")):
                plan=dict(plan)
                for slot in ("talk","react"):
                    if plan.get(slot) and plan[slot] not in profile["frames"]:plan[slot]="neutral"
                self.plan=plan
            for key in (plan["talk"],plan["react"]):
                if key and key not in self.frames:
                    frame=profile["frames"][key]
                    self.frames[key]=Fixed(Transform(frame["file"],xpos=frame["offset"][0],ypos=frame["offset"][1],zoom=frame.get("scale",1.0),nearest=bool(frame.get("nearest")),subpixel=not frame.get("nearest")),xysize=tuple(profile["canvas"]))
                    if profile.get("pixel_grid")==2 and not frame.get("native_detail"):
                        self.frames[key]=r13_pixel_scale(self.frames[key],profile["canvas"][0],profile["canvas"][1],2)
        def visit(self):
            return list(self.frames.values())
        def render(self,width,height,st,at):
            if self.started_st is None:self.started_st=st
            elapsed=max(0.0,st-self.started_st)
            active=store.r13_dialogue_beat
            # An old retained portrait always resolves to its calm talk frame.
            plan=self.plan if active is self.plan else dict(self.plan,settled=True)
            key=plan["talk"] if self.finished else r13_dialogue_phase(plan,elapsed,renpy.is_skipping() or renpy.in_rollback(),persistent.room13_motion)
            if key==plan["talk"]:
                self.finished=True
                # Persist completion across screen reconstruction (settings, resize).
                if active is self.plan and not active["settled"]:r13_dialogue_beat_settle()
            if key!=plan["talk"]:
                renpy.redraw(self,min(.05,max(.001,plan["duration"]-elapsed)))
            return renpy.render(self.frames[key],width,height,st,at)

    R13_DIALOGUE_POSE_SOURCE = json.load(renpy.file("assets/room13-dialogue-pose-source-art.json"))

    # 2026-10-27 소유자 "이게 말이 되는 도트 화소니?": 근접 대화 도트판은 168칸 높이를 3~4px 칸으로 늘려 배경(1칸=1px)보다
    # 3배 거칠었다. 추천안(나): 근접 대화만 붓 원본(dialogue-source-master-v2)으로 그린다. 도트판은 원본을 N칸으로 다시 찍은
    # 것이라 같은 자리에 겹치도록 높이 비율만 곱한다(표 room13-closeup-smooth.json, dev/build_closeup_smooth.py).
    # 끄면(R13_CLOSEUP_SMOOTH=False) 도트판으로 돌아간다. 1칸=1px 근접 도트 신규 작화는 요청서로 넘긴다.
    R13_CLOSEUP_SMOOTH=True
    R13_CLOSEUP_SMOOTH_TABLE=json.load(renpy.file("assets/room13-closeup-smooth.json")) if renpy.loadable("assets/room13-closeup-smooth.json") else {}
    _r13_closeup_smooth_cache={}
    def r13_closeup_smooth_profiles(person,profiles):
        key=(person,id(profiles))
        if key in _r13_closeup_smooth_cache:return _r13_closeup_smooth_cache[key]
        result={}
        for height,profile in profiles.items():
            frames={}
            changed=False
            for name,frame in profile["frames"].items():
                row=R13_CLOSEUP_SMOOTH_TABLE.get(frame.get("file"))
                if row and renpy.loadable(row["master"]):
                    r=float(row["dot"][1])/float(row["src"][1])
                    # 발·머리 기준(anchor)은 도트 파일 픽셀 기준이라, 원본 픽셀 기준으로 나눠 둔다(anchor x scale 이 같게).
                    frames[name]=dict(frame,file=row["master"],scale=frame.get("scale",1.0)*r,anchor=[a/r for a in frame.get("anchor",(0,0))],nearest=False,smooth_source=True)
                    changed=True
                else:frames[name]=frame
            converted=dict(profile,frames=frames)
            if changed:converted["smooth"]=True
            result[height]=converted
        _r13_closeup_smooth_cache[key]=result
        return result
    def r13_dialogue_fit_profile(profiles,height):
        exact=profiles.get(str(int(height))) if float(height)==int(height) else None
        if exact:return exact
        if not profiles:return None
        # 560 질문 전용 전신은 비례 크기표가 아니다. 일반 컷·대사의 중간 높이에 빌리지 않는다.
        proportional=[h for h,p in profiles.items() if "question_top" not in p] or list(profiles)
        base=min(proportional,key=lambda h:abs(int(h)-float(height)))
        ratio=float(height)/int(base);profile=profiles[base]
        k=profile.get("dot_scale")
        # 2026-10-27 붓 원본으로 바꾼 프로필(smooth)은 발 기준선(dot_scale)은 그대로 쓰되 정수 칸 배율은 쓰지 않는다.
        if k and not profile.get("smooth"):
            # 도트 그림은 비정수 배율로 늘리면 칸 크기가 다시 들쭉날쭉해진다. 한 칸이 정수 px 가 되는
            # 배율로만 늘리고, 발 밑과 가운데(anchor)는 요청한 높이의 자리에 맞춘다.
            zoom=max(1,int(round(k*ratio)))/float(k)
            frames={key:dict(frame,offset=[int(round(ratio*(o+a)-zoom*a)) for o,a in zip(frame["offset"],frame.get("anchor",(0,0)))],scale=zoom) for key,frame in profile["frames"].items()}
            return dict(canvas=[max(1,int(round(v*ratio))) for v in profile["canvas"]],frames=frames,dot_scale=k*zoom)
        frames={key:dict(frame,offset=[int(round(v*ratio)) for v in frame["offset"]],scale=frame.get("scale",1.0)*ratio) for key,frame in profile["frames"].items()}
        return dict(canvas=[max(1,int(round(v*ratio))) for v in profile["canvas"]],frames=frames,**({"pixel_grid":2} if profile.get("pixel_grid")==2 else {}))

    def r13_dialogue_pose_source(person,pose):
        entry=R13_DIALOGUE_POSE_SOURCE["people"].get(person,{})
        key=r13_fullbody_key(pose)
        if key in entry.get("pose_profiles",{}):return entry["pose_profiles"][key]
        return entry if key in entry.get("poses",[]) else {}

    def r13_dialogue_player_profiles(person):
        entry=(globals().get("R13_DIALOGUE_PLAYER_FACING",{}).get("people",{}) or {}).get(person,{})
        if (entry.get("status")!="approved_runtime" or entry.get("gaze")!="player"
                or entry.get("stance")!="standing" or entry.get("source_kind")!="source_master"
                or entry.get("art_style")!="storybook_source"):return None
        profiles=entry.get("profiles",{})
        cache=globals().get("_r13_player_facing_ready",{})
        key=(person,id(profiles))
        ready=cache.get(key)
        if ready is None:
            required={"neutral","joy","angry","anxious","flustered","surprise_talk"}
            ready=True
            for height in ("560","760","840"):
                profile=profiles.get(height,{})
                canvas=profile.get("canvas",[])
                frames=profile.get("frames",{})
                if (len(canvas)!=2 or any(not isinstance(n,(int,float)) or n<=0 for n in canvas)
                        or set(frames)!=required or profile.get("pixel_grid") or profile.get("dot_scale")):
                    ready=False;break
                for frame in frames.values():
                    path=frame.get("file","")
                    offset=frame.get("offset",[])
                    if (not isinstance(path,str) or not path.startswith(("assets/dialogue-source-master/","assets/dialogue-player-facing/"))
                            or len(offset)!=2 or any(not isinstance(n,(int,float)) for n in offset)
                            or frame.get("scale",1.0)<=0 or frame.get("nearest",False) is not False
                            or not renpy.loadable(path)):
                        ready=False;break
                if not ready:break
            if len(cache)>64:cache.clear()
            cache[key]=ready
        return profiles if ready else None

    def r13_dialogue_render_profiles(person,entry,player_facing=False):
        meeting=bool(getattr(store,"r13_meeting_active",False))
        solo_focus=bool(globals().get("R13_MEETING_SOLO") and getattr(store,"r13_meeting_focus",None)==person)
        # 돌목 새 작화는 일반 대사와 reviewed beat가 같은 승인 6표정을 쓴다.
        # 회의는 기존처럼 직접 정면 요청을 받은 단독 초점만 바꾸며, 다른 인물의 beat는 유지한다.
        if (player_facing and (not meeting or solo_focus)) or (person=="guard" and not meeting):
            profiles=r13_dialogue_player_profiles(person)
            if profiles:
                normalize=globals().get("r13_dialogue_size_profiles")
                return normalize(person,profiles) if normalize else profiles

        # Approved B expressions are dialogue-only; meeting art keeps its original profiles.
        if not getattr(store,"r13_meeting_active",False) and globals().get("R13_DIALOGUE_B_ART_ON",True) and R13_DIALOGUE_B_ART.get(person):
            profiles=R13_DIALOGUE_B_ART[person]
        else:profiles=entry.get("profiles",{})
        # 시험(dev/test_b_dialogue_art.py)은 함수만 떼어 돌리므로 전역이 없으면 그대로 돌려준다.
        profiles=r13_closeup_smooth_profiles(person,profiles) if globals().get("R13_CLOSEUP_SMOOTH") else profiles
        normalize=globals().get("r13_dialogue_size_profiles")
        return normalize(person,profiles) if normalize and (not meeting or solo_focus) else profiles

    def r13_dialogue_source_profile(person,pose,height):
        # Authored poses retain their own smooth source, even during narration/thought.
        posed=r13_dialogue_pose_source(person,pose)
        if posed:return r13_dialogue_fit_profile(posed["profiles"],height)
        if getattr(store,"r13_thought_active",False) and person!="resident_solbang":return None
        key=r13_fullbody_key(pose)
        if key not in R13_FULLBODY_PLAIN and not (person=="npc_panseol" and key=="tired"):return None
        entry=R13_DIALOGUE_TALK_ART["people"].get(person,{})
        if entry.get("status")!="approved_runtime":return None
        return r13_dialogue_fit_profile(r13_dialogue_render_profiles(person,entry,player_facing=True),height)

    def r13_dialogue_source_neutral(person,pose,height):
        profile=r13_dialogue_source_profile(person,pose,height)
        if not profile:return None
        # 0.19.98 (owner 2026-10-22: "대사에 맞는 표정들도 많이 부족해서"): every line shows the
        # expression it was written with, not only meeting lines and reviewed cues. Lines with no
        # expression are still neutral; a missing frame keeps the nearest approved one below.
        key=r13_fullbody_key(pose)
        emotion=key if key in profile["frames"] else r13_fullbody_emotion(pose)
        emotion={"surprise":"surprise_talk"}.get(emotion,emotion)
        # 2026-10-26 전신 묶음은 당황을 따로 그렸다. 없는 인물은 예전처럼 불안 그림을 빌린다.
        if emotion=="flustered" and "flustered" not in profile["frames"]:emotion="anxious"
        frame=profile["frames"].get(emotion,profile["frames"]["neutral"])
        if renpy.loadable(frame["file"]):
            art=Fixed(Transform(frame["file"],xpos=frame["offset"][0],ypos=frame["offset"][1],zoom=frame.get("scale",1.0),nearest=bool(frame.get("nearest")),subpixel=not frame.get("nearest")),xysize=tuple(profile["canvas"]))
            return r13_pixel_scale(art,profile["canvas"][0],profile["canvas"][1],2) if profile.get("pixel_grid")==2 and not frame.get("native_detail") else art
        # An approved character must never silently revert to the old pixel design.
        # A second shipped size is the same approved neutral, with its whole canvas scaled.
        posed=r13_dialogue_pose_source(person,pose)
        entry=posed or R13_DIALOGUE_TALK_ART["people"][person]
        for alternate in sorted(entry["profiles"],key=lambda h:abs(int(h)-int(height))):
            other=entry["profiles"][alternate]
            fallback=other["frames"]["neutral"]
            if renpy.loadable(fallback["file"]):
                art=Fixed(Transform(fallback["file"],xpos=fallback["offset"][0],ypos=fallback["offset"][1],zoom=fallback.get("scale",1.0),nearest=False,subpixel=True),xysize=tuple(other["canvas"]))
                renpy.log("Approved dialogue size fallback: %s %s -> %s" % (person,height,alternate))
                art=Transform(art,xysize=tuple(profile["canvas"]),nearest=False,subpixel=True)
                return r13_pixel_scale(art,profile["canvas"][0],profile["canvas"][1],2) if profile.get("pixel_grid")==2 else art
        renpy.log("Approved dialogue art unavailable: %s %s" % (person,frame["file"]))
        return Fixed(Text("인물 그림을 불러오지 못했습니다.\n연결을 확인한 뒤 게임을 다시 열어 주세요.",size=22,color="#fff4df",xalign=.5,ypos=100),xysize=tuple(profile["canvas"]))

    def r13_dialogue_beat_art(person,height):
        if not r13_dialogue_beat_ready(person):return None
        # 일반 대사의 검토된 감정 연출도 같은 정면 원본을 쓴다. 문맥 전용 그림은 바깥 래퍼가 유지한다.
        profile=r13_dialogue_fit_profile(r13_dialogue_render_profiles(person,R13_DIALOGUE_TALK_ART["people"][person],player_facing=True),height)
        if not profile:return None
        plan=store.r13_dialogue_beat
        # 별도 움찔 그림이 없는 정면 묶음은 지정된 놀람 표정을 바로 보인다.
        if plan.get("react") and plan["react"] not in profile["frames"]:
            plan=dict(plan,react=None,settled=True)
        return R13DialogueBeat(plan,profile)

    config.after_load_callbacks.append(r13_dialogue_beat_after_load)
