# 대사 장면 인물 크기·위치(2026-10-28 소유자 「역전재판처럼 상당히 가까이, 머리끝이 화면 끝처럼」 → 1.55배).
# room13_rules.rpy 의 r13_speaker 가 부른다. 마차(앉은 다람)는 예전 크기(840) 그대로.
init 40 python:
    R13_SAY_ACTOR_H=int(840*1.55)   # 대사 장면 인물 높이(예전 840)
    R13_SAY_ACTOR_DY=-552           # 키운 만큼 올려 어른 머리끝이 화면 위(약 20)에 오게
    # 2026-10-28 소유자 「다람이는 좀 내려야겠다. 아이니까」「캐릭터마다 키를 생각해서 배치하는 듯」(역전재판 캡처):
    # 머리 높이를 인물 키로 정한다. 키는 현장 도트 서 있는 높이(room13-field-dot-v2.json, 어른 210)를 쓴다 —
    # 아이 165, 할머니·부엉이 195, 선생님·까로·보리 230. 210 보다 작으면 그만큼 내리고, 크면 올려 머리끝이 화면 위에서 살짝 잘린다.
    # 다람은 0.82(아래 주석). 거리 520 은 어른 머리끝(약 20)~대사판 위(약 540).
    R13_SAY_STATURE_REF=210.0
    def r13_say_stature(who):
        # 2026-10-28 소유자 「다람이 몸이 좀 더 가운데로 오고 높아야 하지 않을까」: 2/3 → 다른 아이들(165/210)보다 조금 큰 0.82.
        if who=="daram":return 0.82
        dot=(globals().get("R13_FIELD_DOT",{}).get(who) or {}).get("poses",{})
        entry=dot.get("neutral") or next(iter(dot.values()),None)
        return (entry["size"][1]/R13_SAY_STATURE_REF) if entry else 1.0
    def r13_say_child_drop(who):
        return int(round(520*(1-min(1.0,r13_say_stature(who)))))

    # 그림마다 캔버스 안 머리 위치가 달라(같은 발 선이어도 선생님·까로는 얼굴이 잘리고 할머니는 낮았다) 실제 그림의
    # 불투명 영역 윗변을 재서 머리끝을 목표 높이에 맞춘다. 재지 못하면 예전 계산(발 선 + 키 보정)으로 둔다.
    R13_SAY_HEAD_TOP=20          # 어른(키 210) 머리끝 화면 높이
    R13_SAY_TALL_CUT=36          # 210 보다 큰 인물은 키 차이만큼(최대 이만큼) 화면 위로 잘린다
    _R13_SAY_HEADTOP={}
    def _r13_say_headtop(who,pose,h):
        profile=r13_dialogue_source_profile(who,pose,h)
        if not profile:return None
        # 그리는 쪽(room13_dialogue_beats.rpy)과 같은 그림을 재야 한다. 놀람은 surprise_talk, 당황 그림이 없으면 불안을 그린다.
        # 2026-10-28 캡처 검수(11일 엄마 「이거…… 아직 갖고 다녔어?」): 이 대응이 없어 보통 표정 그림의 머리를 재고 놀람 그림을 그려
        # 머리가 화면 위로 잘리고 다리만 보였다.
        emotion={"surprise":"surprise_talk"}.get(r13_fullbody_emotion(pose),r13_fullbody_emotion(pose))
        if emotion=="flustered" and "flustered" not in profile["frames"]:emotion="anxious"
        frame=profile["frames"].get(emotion) or profile["frames"].get("neutral")
        if not frame:return None
        key=(frame["file"],h)
        if key not in _R13_SAY_HEADTOP:
            try:
                surf=renpy.display.im.Image(frame["file"]).load()
                top=surf.get_bounding_rect(min_alpha=40).top
                _R13_SAY_HEADTOP[key]=frame["offset"][1]+top*frame.get("scale",1.0)
            except Exception:
                _R13_SAY_HEADTOP[key]=None
        return _R13_SAY_HEADTOP[key]
    # 2026-10-28 캡처 검수(11일 엄마 놀람): 그림 묶음 표로 잰 머리 높이가 실제 그림과 66px 달랐다(표에 없는 표정은 다른 그림이
    # 그려진다). 실제로 그릴 그림(말하는 그림)을 한 번 그려 맨 위 불투명 줄을 잰다. 인물·자세·키마다 한 번만 잰다.
    _R13_SAY_DRAWN_TOP={}
    def _r13_say_drawn_headtop(who,pose,h):
        key=(who,pose,h)
        if key not in _R13_SAY_DRAWN_TOP:
            try:
                rect=renpy.render_to_surface(r13_close_art(who,pose,h,True)).get_bounding_rect(min_alpha=40)
                _R13_SAY_DRAWN_TOP[key]=rect.top if rect.height else None
            except Exception:
                _R13_SAY_DRAWN_TOP[key]=None
        return _R13_SAY_DRAWN_TOP[key]
    def r13_say_head_target(who):
        st=r13_say_stature(who)
        if st>1.0:return R13_SAY_HEAD_TOP-min(R13_SAY_TALL_CUT,int(round((st-1.0)*R13_SAY_STATURE_REF*1.55*0.4)))
        return R13_SAY_HEAD_TOP+r13_say_child_drop(who)
    # 그림 캔버스 가운데가 몸 가운데가 아닌 인물(다람은 왼쪽 꼬리 때문에 얼굴이 오른쪽에 섰다)은 그만큼 옮긴다.
    R13_SAY_X_NUDGE={"daram":-64}
    def r13_say_actor_x(who,pose,carriage=False):
        return r13_close_x(who,pose,r13_say_actor_h(carriage))+(0 if carriage else R13_SAY_X_NUDGE.get(who,0))
    def r13_say_actor_h(carriage=False):
        return 840 if carriage else R13_SAY_ACTOR_H
    def r13_say_actor_y(who,pose,carriage=False):
        h=r13_say_actor_h(carriage)
        if carriage:return r13_close_y(who,h,110,pose)
        head=_r13_say_drawn_headtop(who,pose,h)
        if head is None:head=_r13_say_headtop(who,pose,h)
        if head is not None:return int(round(r13_say_head_target(who)-head))
        return r13_close_y(who,h,110,pose)+R13_SAY_ACTOR_DY+r13_say_child_drop(who)

    # 2026-10-28 소유자 「대화 상대가 항상 표기되면 돼」: 아빠가 말할 때 듣는 사람.
    # 순서: 이 대사 묶음에서 다음에 말하는 사람 → 바로 앞에 말한 사람(그 장면에 있으면) → 그 장면에 있는 사람 중 다람 아닌 첫 사람 → 다람.
    def r13_dad_listener(entries,index):
        vp=r13_viewpoint()
        def ok(who):return bool(who) and who!=vp and who in CAST
        # 2026-10-28 분기 주행: 「판돌 씨, 여기요」에 돌목이, 「모모 씨, 내려요」에 까로가 섰다. 아빠가 부른 이름이 먼저다.
        text=str(entries[index][1]) if index<len(entries) and len(entries[index])>1 else ""
        called=r13_called_person(text)
        if ok(called):return called
        for p in entries[index+1:]:
            opts=p[2] if len(p)>2 and isinstance(p[2],dict) else {}
            if ok(p[0]) and not opts.get("thought"):return p[0]
        # 2026-10-28 분기 주행(9일 식당): 「할머니가 식당 입구에서 목도리를 여민다」 바로 뒤 아빠의 「끝이 찢어졌네요」에
        # 나비가 섰다. 바로 앞 줄의 화자(지문이면 그 주어)가 듣는 사람이다.
        narrated=r13_narrated_person()
        if ok(narrated):return narrated
        state=getattr(store,"room13",None) or {}
        present=list((state.get("v111") or {}).get("people") or [])
        alive=globals().get("r13_v111_person_alive",lambda w:True)
        present=[w for w in present if ok(w) and alive(w)]
        last=getattr(store,"r13_last_partner",None)
        if ok(last) and (last in present or not present):return last
        others=[w for w in present if w!="daram"]
        if others:return others[0]
        return "daram" if "daram" in present else None

    R13_CALL_GENERIC=("아빠","엄마","할머니","할아버지","선생님","아이","주민","사람","부인","영감","관장","대장")
    def r13_called_person(text):
        """아빠가 이름을 불러 말을 거는 사람(「모모 씨,」「다람아,」「굴돌 씨도」). 남 얘기로 이름만 나온 것은 아니다."""
        import re
        alive=globals().get("r13_v111_person_alive",lambda w:True)
        best=None
        for name,who in r13_person_names(R13_CALL_GENERIC):
            m=re.search(re.escape(name)+"(?: ?씨| ?님|아|야)?(?:[,!?…]| ?씨도 )",text)
            if m and alive(who) and (best is None or m.start()<best[0]):best=(m.start(),who)
        return best[1] if best else None

    R13_NARRATE_SKIP=("아빠","엄마","아이","주민","사람")
    def r13_narrated_person():
        """바로 앞에 보인 줄의 사람: 다른 사람의 대사면 그 화자, 지문이면 그 지문의 주어(「할머니가」「나비는」). 없으면 None."""
        import re
        hist=getattr(store,"_history_list",None) or []
        if not hist:return None
        last=hist[-1]
        who_label=getattr(last,"who",None)
        if who_label:
            # 바로 앞 줄을 다른 사람이 말했으면 아빠는 그 사람에게 답한다(10일 회의 「……더 들을 말이 있소?」→「있습니다」).
            label=renpy.filter_text_tags(str(who_label),allow=[])
            for name,who in r13_person_names(()):
                if label==name or label.split(" ")[0]==name:return who
            return None
        text=renpy.filter_text_tags(str(getattr(last,"what","") or ""),allow=[])
        alive=globals().get("r13_v111_person_alive",lambda w:True)
        best=None
        for name,who in r13_person_names(R13_NARRATE_SKIP):
            m=re.search(re.escape(name)+"(?:가|는|이|은|의) ",text)
            if m and alive(who) and (best is None or m.start()<best[0]):best=(m.start(),who)
        return best[1] if best else None

    def r13_person_names(skip):
        """(이름 첫 낱말, 인물) 목록. 보이는 이름(뿔이)·원래 이름·대본 화자 이름(촌장)을 다 넣는다. 그림이 있는 인물만."""
        rows=set()
        for who in CAST:
            for full in (r13_display_name(who),R13_NAMES.get(who)):
                if full:rows.add((str(full).split(" ")[0],who))
        for label,who in (globals().get("MS14_SPEAKERS") or {}).items():
            # 「창고 아이 1」「누비의 큰아이」 같은 여러 낱말 이름표는 첫 낱말이 사물(창고)이라 넣지 않는다.
            if who in CAST and label and " " not in str(label):rows.add((str(label),who))
        return [(n,w) for n,w in rows if len(n)>=2 and n not in skip]
