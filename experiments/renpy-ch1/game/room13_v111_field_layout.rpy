# Field staging keeps investigable objects clear (owner-approved plan 2026-10-22, item 1:
# "조사할 때 인물이 방해하지 않게 — 캐릭터 크기는 유지하고, 증거를 가리지 않는 자리로 배치").
# r13_stage_people (room13_acting.rpy) scores each standing slot; a body covering a "critical"
# rectangle costs a lot. Besides the layout's fixed list, every object the current story step
# lets the player inspect at this place now counts as critical, so residents stand elsewhere.
init 336 python:
    def r13_stage_critical(location,layout):
        base=list(layout.get("critical",R13_STAGE_CRITICAL.get(location,[]))) if layout else list(R13_STAGE_CRITICAL.get(location,[]))
        if not r13_v111_active() or location!=(store.room13 or {}).get("location"):
            return base
        objects=ROOM13["objects"].get(location,{})
        for option in r13_v111_binding().get("options",[]):
            key=option.get("object")
            if not key or option.get("location")!=location:continue
            spec=objects.get(r13_v111_object_key(key)) or objects.get(key)
            rect=spec and spec.get("rect")
            if rect and tuple(rect) not in [tuple(r) for r in base]:base.append(tuple(rect))
        return base

    # A resident chosen into a free slot can end up behind someone staged later at a fixed spot
    # (gate: 실룩 behind 바둑이, owner QA 2026-10-22 mockup note). If a free-slot resident's face is
    # covered by a body in front, stage the fixed-position people first and choose again.
    R13_STAGE_ORDER_OVERRIDE=None
    _r13_order_visible_people=r13_visible_people
    def r13_visible_people():
        people=_r13_order_visible_people()
        order=R13_STAGE_ORDER_OVERRIDE
        if order:
            people=[p for p in order if p in people]+[p for p in people if p not in order]
        return people

    def r13_stage_face_covered(rows):
        for i,a in enumerate(rows):
            if not a.get("slot"):continue
            try:fx,fy,fw,fh=r13_actor_face_target(a)
            except Exception:continue
            cx,cy=fx+fw/2.0,fy+fh/2.0
            for b in rows:
                if b is a:continue
                bx,by,bw,bh=b["rect"]
                if bx<=cx<=bx+bw and by<=cy<=by+bh and by+bh>a["rect"][1]+a["rect"][3]:
                    return True
        return False

    _r13_order_stage_people=r13_stage_people
    def r13_stage_people(entry=False):
        global R13_STAGE_ORDER_OVERRIDE
        rows=_r13_order_stage_people(entry)
        if R13_STAGE_ORDER_OVERRIDE is None and r13_v111_active() and r13_stage_face_covered(rows):
            fixed=[a["person"] for a in rows if not a.get("slot")]
            R13_STAGE_ORDER_OVERRIDE=fixed+[a["person"] for a in rows if a.get("slot")]
            try:
                again=_r13_order_stage_people(entry)
            finally:
                R13_STAGE_ORDER_OVERRIDE=None
            if not r13_stage_face_covered(again):rows=again
        return rows

    # Stand spots by role (owner 2026-10-22, mockup D: "서 있을 자리를 먼저 정한다").
    # Gate: the gatekeeper beside the right gate post, the carter whispering at his shoulder,
    # Karo kneeling at his own wheel, Daram beside him with her notebook, Bori carrying wood at
    # the woodpile. The gate passage and the booth papers stay clear; ordinary things (the
    # cart, crates, fence) have people beside them so the empty space is not a pointer.
    R13_STAND_SPOTS={
        "gate":dict(
            # 2026-10-27 한 명씩 검수: 바둑이가 빈 자리(720,700)로 들어가 까로의 다리 위에 쪼그려 앉았다(겹침 45%).
            # 까로의 수레와 네로 사이에 자기 자리를 준다.
            positions={"guard":[1234,592,222],"resident_siluk":[1290,545,212],"karo":[630,628,230],
                       "daram":[730,704,205],"resident_bori":[1770,666,238],"resident_badook":[870,690,212]},
            poses={"guard":"neutral","daram":"thinking","resident_siluk":"event_whisper","karo":"living_axlewrap",
                   "resident_bori":"map27_carry_firewood_v2"},
            pose_positions={"karo:living_axlewrap":[630,628]},
            pinned=["karo","guard","daram","resident_siluk","resident_bori","resident_badook"],
        ),
        # 0.20.9 (play review D23-01): the north exchange box (1150-1370) stays clear. Chorong stands
        # at its left edge with her lamp, Silluk a step behind her.
        "forest":dict(
            positions={"resident_lamplighter":[1060,700,226],"resident_siluk":[880,700,240]},
            poses={},
            pose_positions={},
            pinned=["resident_lamplighter","resident_siluk"],
        ),
    }
    for _spot_place,_spot in R13_STAND_SPOTS.items():
        _spot_layout=R13_WORLD_LAYOUTS.get(_spot_place)
        if not _spot_layout:continue
        # Spots are written against the old 1920x720 picture; a wider picture moves them with it.
        _sdx,_sdy=_spot_layout.get("wide_shift",[0,0])
        _spot=dict(_spot,positions={k:[v[0]+_sdx,v[1]+_sdy]+v[2:] for k,v in _spot["positions"].items()},
            pose_positions={k:[v[0]+_sdx,v[1]+_sdy] for k,v in _spot["pose_positions"].items()})
        _spot_layout["positions"]=dict(_spot_layout.get("positions",{}),**_spot["positions"])
        _spot_layout["poses"]=dict(_spot_layout.get("poses",{}),**_spot["poses"])
        _spot_layout["pose_positions"]=dict(_spot_layout.get("pose_positions",{}),**_spot["pose_positions"])
        _spot_layout["pinned"]=list(dict.fromkeys(list(_spot_layout.get("pinned",[]))+_spot["pinned"]))

    # People with no part in the current gate scene go where their day's work is
    # ("다른 주민은 생활과 이야기상 맞는 장소로 분산"): Nero to the general store, Badook to the
    # square patrol. Anyone the current scene names, or who has an option here, stays.
    R13_RELOCATE={("gate","resident_nero"):"store",("gate","resident_badook"):"square"}
    def r13_v111_needed_at(person,place):
        if not r13_v111_active():return True
        binding=r13_v111_binding()
        if person in binding.get("people",[]):return True
        return any(o.get("person")==person and o.get("location")==place for o in binding.get("options",[]))
    _r13_relocate_where=r13_where
    def r13_where(person):
        place=_r13_relocate_where(person)
        target=R13_RELOCATE.get((place,person))
        if target and not r13_v111_needed_at(person,place):return target
        return place

init 337 python:
    # 0.20.9 (play review D23-01): fixed daily-work spots (map27, e.g. Kalbaram in the forest) are
    # placed after the slot scoring and can still stand on the object the current story step needs.
    # Such a figure steps sideways off it: same pose and height, only the feet move along the floor.
    def r13_clear_critical_x(actor,rects,others,width):
        ax,ay,aw,ah=actor["rect"]
        for ox,oy,ow,oh in rects:
            cover=min(ax+aw,ox+ow)-max(ax,ox)
            if cover<=aw*0.3 or ay+ah<=oy:continue
            foot_y=actor["y"]+actor["height"]
            sides=[ox-aw/2.0-24-k*80 for k in range(8)]+[ox+ow+aw/2.0+24+k*80 for k in range(8)]
            sides=[f for f in sides if aw/2.0<=f<=width-aw/2.0]
            def crowd(f):
                return sum(1 for b in others if b is not actor and abs((b["rect"][0]+b["rect"][2]/2.0)-f)<(aw+b["rect"][2])/2.0)
            if not sides:continue
            cx=ax+aw/2.0
            # 2026-10-28 다른 길 자동 플레이 3일 광장: 3번 등 옆의 피코가 등(조사 물건)을 피해 오른쪽으로 비키며 첫 화면 밖으로
            # 나갔다(952→1210, 카메라 0). 비킨 자리가 지금 화면 밖으로 1/3 넘게 나가면 붐비는 쪽이라도 안쪽을 고른다.
            try:view_left=r13_world_offset();view_right=view_left+r13_view_width()
            except Exception:view_left,view_right=0,width
            def offscreen(f):
                hidden=max(0,view_left-(f-aw/2.0))+max(0,(f+aw/2.0)-view_right)
                return 1 if hidden>aw/3.0 else 0
            best=min(sides,key=lambda f:(offscreen(f),crowd(f),abs(f-cx)))
            # 2026-10-27 검수(입구 까로): 마차 자리(630)의 까로가 수레 칸을 조금 덮는다고 오른쪽이 다람으로 붐빈다는 이유로
            # 왼쪽 끝(128)까지 밀려 화면 가장자리에 붙어 보였다. 이 층은 자리 옆으로 한 걸음 비키는 것이다 — 화면 반
            # (R13_CLEAR_STEP_MAX) 을 넘는 이동은 하지 않고 사슬 끝의 물건 회피(1/5 넘게 덮을 때만 비킴)에 맡긴다.
            if abs(best-cx)>R13_CLEAR_STEP_MAX:continue
            return r13_ma_place(actor,actor["pose"],int(best),foot_y,actor["height"])
        return actor
    R13_CLEAR_STEP_MAX=320

    _r13_clear_stage_people=r13_stage_people
    def r13_stage_people(entry=False):
        rows=_r13_clear_stage_people(entry)
        if not r13_v111_active():return rows
        location=(store.room13 or {}).get("location")
        rects=[tuple(r) for r in r13_stage_critical(location,R13_WORLD_LAYOUTS.get(location))]
        width=r13_world_width()
        out=[]
        for actor in rows:
            out.append(r13_clear_critical_x(actor,rects,rows,width) if (rects and actor.get("rect")) else actor)
        # 2026-10-28 다른 길 13일 입구·광장: 조사 물건이 없는 장면에서는 여기서 바로 돌아가 겹침 풀기까지 건너뛰었다.
        # 혀이 뒤에 돌목이 72px 묻혀도 그대로였다. 물건 회피는 물건이 있을 때만, 겹침 풀기는 늘 돈다.
        out=r13_separate_overlaps(out,rects,width)
        # 조사 물건 위에 선 사람을 마지막으로 치우는 r13_clear_objects 는 여기서 부르지 않는다.
        # 뒤 층(도트 환산)이 사각형을 바꾸므로 배치 사슬의 맨 끝(room13_field_dot.rpy)에서 한 번만 돈다.
        return sorted(out,key=lambda a:a.get("depth",0))

    # 0.20.10 (4~14일 리뷰: 5일 골목, 9일 주방, 11일 숲): 두 사람이 거의 같은 자리에 서면 뒤에 선
    # 사람의 얼굴과 이름표가 가린다. 뒤쪽(깊이가 얕은) 사람이 가장 가까운 빈자리로 비켜 선다.
    def r13_separate_overlaps(rows,rects,width):
        rows=list(rows)
        for _ in range(3):
            moved=False
            for i,a in enumerate(rows):
                for j,b in enumerate(rows):
                    if j<=i or not a.get("rect") or not b.get("rect"):continue
                    ax,ay,aw,ah=a["rect"];bx,by,bw,bh=b["rect"]
                    cover=min(ax+aw,bx+bw)-max(ax,bx)
                    if cover<=0.55*min(aw,bw) or min(ay+ah,by+bh)-max(ay,by)<=0.5*min(ah,bh):continue
                    k=i if a.get("depth",0)<=b.get("depth",0) else j
                    # 2026-10-28 다른 길 3일 광장: 등 옆의 피코(이야기 자리)와 빈 자리의 바둑이가 겹치자 뒤에 선 피코가 더 오른쪽으로
                    # 밀려 화면 밖으로 나갔다. 둘 중 하나만 빈 자리(slot) 사람이면 그쪽이 비킨다 — 이야기 자리는 그 물건 옆이 뜻이다.
                    if bool(a.get("slot"))!=bool(b.get("slot")):k=i if a.get("slot") else j
                    back=rows[k];fx,fy,fw,fh=back["rect"];cx=fx+fw/2.0
                    others=[r for n,r in enumerate(rows) if n!=k and r.get("rect")]
                    def crowd(f):
                        hit=sum(1 for r in others if abs((r["rect"][0]+r["rect"][2]/2.0)-f)<(fw+r["rect"][2])/2.0*0.5)
                        # 2026-10-28 다른 길 13일 광장: 물건을 가로로 스치기만 해도 막힌 자리로 세어 ±810 안이 전부 붐볐고,
                        # 혀이 뒤의 돌목이 그대로 묻혔다. 물건 회피 규칙과 같게 몸이 물건을 1/5 넘게 덮을 때만 붐빔이다.
                        for ox,oy,ow,oh in rects:
                            bx=f-fw/2.0;cover=max(0,min(bx+fw,ox+ow)-max(bx,ox))*max(0,min(fy+fh,oy+oh)-max(fy,oy))
                            if cover>0.2*max(1,ow*oh):hit+=1
                        return hit
                    feet=[cx+d*s for d in range(90,900,90) for s in (-1,1) if fw/2.0<=cx+d*s<=width-fw/2.0]
                    if not feet:continue
                    try:view_left=r13_world_offset();view_right=view_left+r13_view_width()
                    except Exception:view_left,view_right=0,width
                    def offscreen(f):
                        hidden=max(0,view_left-(f-fw/2.0))+max(0,(f+fw/2.0)-view_right)
                        return 1 if hidden>fw/3.0 else 0
                    best=min(feet,key=lambda f:(offscreen(f),crowd(f),abs(f-cx)))
                    if crowd(best)>0:continue
                    rows[k]=r13_ma_place(back,back["pose"],int(best),back["y"]+back["height"],back["height"])
                    moved=True
            if not moved:break
        return rows


    def r13_stage_keepouts(location,layout=None):
        # 2026-10-27 소유자(공동 창고 4일 낮): 실룩이 파란 통 안에, 여니가 소쿠리 위에 선 것처럼 그려졌다.
        # 바닥 소품(통·소쿠리·상자) 영역은 world-layout 의 "keepouts" 에 적는다. 조사 물건(critical)과 달리 누르는 것이
        # 아니지만, 발을 그 안에 둘 수 없고 몸으로 1/5 넘게 덮지도 않는다. 다섯째 칸이 "feet" 면 발만 못 둔다(그림 아래쪽의
        # 큰 상자처럼 그 앞 바닥이 있는 것). 자리 점수(room13_acting.rpy)와 여기서 같이 읽는다.
        layout=layout if layout is not None else R13_WORLD_LAYOUTS.get(location)
        return [tuple(r) for r in (layout or {}).get("keepouts",[])]

    def r13_keepout_cover_rects(keepouts):
        return [tuple(k[:4]) for k in keepouts if len(k)<5 or k[4]!="feet"]

    def r13_foot_in_keepout(rect,keepouts):
        fx,fy=rect[0]+rect[2]/2.0,rect[1]+rect[3]
        return any(k[0]<=fx<=k[0]+k[2] and k[1]<=fy<=k[1]+k[3] for k in keepouts)

    def r13_clear_objects(rows,critical,width,keepouts=()):
        # 소유자 2026-10-27 "캐릭터 배치를 증거랑 겹치게 하면 안 돼": 배치 사슬의 맨 끝에서 모든 장소에 적용한다.
        # 규칙은 하나다 — 몸이 조사 물건(critical)을 1/5 넘게 덮거나 물건 가운데를 밟으면 옆으로 비킨다.
        # 고정 자리(까로의 마차 등)도 예외가 아니다. 물건은 눌러야 하는 것이고 사람은 옆에 서면 된다.
        # 발 선은 지킨다(아래로 내리면 화면 밖·앞사람 위로 간다). 가구에 붙은 자세는 그림에서 떼지 않는다.
        # 바닥 소품(keepouts)도 같은 규칙에 더해 발을 그 안에 두지 않는다(통 안에 선 것처럼 보인다).
        def overlap(a,b):
            return max(0,min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0]))*max(0,min(a[1]+a[3],b[1]+b[3])-max(a[1],b[1]))
        def covers(body,rect):
            area=max(1,rect[2]*rect[3]);cx,cy=rect[0]+rect[2]/2.0,rect[1]+rect[3]/2.0
            inside=body[0]<=cx<=body[0]+body[2] and body[1]<=cy<=body[1]+body[3]
            return inside or overlap(body,rect)>area*0.2
        keepouts=[tuple(r) for r in keepouts]
        critical=list(critical)+r13_keepout_cover_rects(keepouts)
        height=r13_world_height()
        # 2026-10-28 다른 길 자동 플레이 3일 광장: 등(3번 등)을 피하느라 피코가 오른쪽으로 264px 밀려 첫 화면 밖(1314)으로 나갔다.
        # 비킨 자리가 지금 화면(카메라 폭) 밖으로 1/3 넘게 나가면 벌점을 둔다 — 보이지 않는 것이 겹침보다 나쁘다.
        try:view_left=r13_world_offset();view_right=view_left+r13_view_width()
        except Exception:view_left,view_right=0,width
        def offscreen(rect):
            hidden=max(0,view_left-rect[0])+max(0,rect[0]+rect[2]-view_right)
            return 1 if hidden>rect[2]/3.0 else 0
        out=list(rows)
        all_critical=critical
        for index,actor in enumerate(out):
            # 그 물건에서 일하는 사람(field-life "at_object")은 자기 물건만 덮어도 된다.
            critical=[r for r in all_critical if tuple(r)!=actor.get("work_rect")] if actor.get("work_rect") else all_critical
            if not any(covers(actor["rect"],r) for r in critical) and not r13_foot_in_keepout(actor["rect"],keepouts):continue
            if actor.get("contact") in ("hanging","background_bench","bench_sit","behind_counter","background_chair"):continue
            face=r13_actor_face_target(actor) or actor["rect"]
            dxs={0}
            for rect in critical:
                dxs.update((int(rect[0]-8-face[0]-face[2]),int(rect[0]+rect[2]+8-face[0]),
                            int(rect[0]-8-actor["rect"][0]-actor["rect"][2]),int(rect[0]+rect[2]+8-actor["rect"][0])))
            dxs.update(d for n in (48,96,144,240,384,640) for d in (-n,n))
            candidates=[]
            for dx in sorted(dxs):
                candidate=r13_balance_translate(actor,dx,0)
                x,y,w,h=candidate["rect"]
                if x<8 or x+w>width-8 or y<100 or y+h>height:continue
                cf=r13_actor_face_target(candidate) or candidate["rect"]
                object_cover=sum(overlap(candidate["rect"],r) for r in critical if covers(candidate["rect"],r))
                if r13_foot_in_keepout(candidate["rect"],keepouts):object_cover+=10**6
                people=0
                for other_index,other in enumerate(out):
                    if other_index==index:continue
                    of=r13_actor_face_target(other) or other["rect"]
                    people+=overlap(cf,of)*4
                    if candidate.get("depth",0)>other.get("depth",0):people+=overlap(candidate["rect"],of)
                    else:people+=overlap(cf,other["rect"])
                    people+=overlap(candidate["rect"],other["rect"])//2   # 몸끼리도 피한다(보리가 돌목 앞을 막았다)
                candidates.append(((object_cover,offscreen(candidate["rect"]) if not offscreen(actor["rect"]) else 0,people,abs(dx)),candidate))
            if candidates:out[index]=min(candidates,key=lambda item:item[0])[1]
        return out

    def r13_clamp_to_world(rows,width):
        # 2026-10-27 검수: 사슬 끝에서 인물 사각형이 월드 왼쪽·오른쪽 끝 밖으로 나가지 않게 한다(가장자리에 반쯤 걸친 인물).
        # 사각형이 월드보다 넓으면(없다) 그대로 둔다. 발 선은 지킨다.
        out=[]
        for actor in rows:
            rect=actor.get("rect")
            if rect and rect[2]<=width:
                dx=0
                if rect[0]<0:dx=-rect[0]
                elif rect[0]+rect[2]>width:dx=width-(rect[0]+rect[2])
                if dx:actor=r13_balance_translate(actor,dx,0)
            out.append(actor)
        return out
