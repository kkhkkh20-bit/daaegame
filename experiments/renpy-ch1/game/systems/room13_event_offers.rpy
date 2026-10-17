# Approaching general events is a choice (owner, 0.18.19).
#   Arriving no longer starts a long ordinary event. The scene shows what is happening as a marker;
#   clicking it enters the event. Passing by lets the event run on its own schedule: when the time
#   slot ends, the outcome is that of the event's own "look away" branch, and Dad hears of it later.
#   Events about 다람이's safety or an accident right in front of Dad still start by themselves.
init 124 python:
    # label: (marker text, flags when passed by, what Dad hears later)
    R13_EVENT_OFFERS={
        "r13_w1c_portrait":("광장 구석에서 피코가 판자에 물감을 문지르고 있다",["ev_g_done"],"광장 구석의 그림 장수는 저녁 전에 자리를 걷었다고 했다."),
        "r13_w1c_letters":("우체국 안쪽에서 슬링이 봉투를 김에 쐬고 있다",["ev_l_done","warning_exposed"],"우체국 화덕 위에서 누군가 봉투를 김에 쐬고 있었다는 말을 들었다."),
        "r13_w1c_extension":("여관 뒷벽에서 따닥이 판자를 덧대고 있다",["ev_i_done"],"여관 뒷벽 공사는 그날 끝났다고 했다."),
        "r13_w1c_seal":("봉해 둔 13호 문 앞에서 뭉치가 서성인다",["ev_s_done","family_items_lost"],"봉해 둔 13호에서 누군가 물건을 꺼내 갔다는 말을 들었다."),
        "r13_w1c_testimony":("실룩이 사람들 사이를 오가며 귓속말을 한다",["ev_t_done"],"실룩이 재판에 쓸 증언을 팔러 다닌다는 말이 돌았다."),
        "r13_b3_ration":("배급대 앞에서 줄이 멈춰 있다",["ev_e_done","bori_punished"],"배급대 앞에서 보리가 빈 수레로 돌아갔다는 말을 들었다."),
        "r13_b3_pages":("사서 선생님이 우체국 구석에서 옛 장부를 묶고 있다",["ev_u_done","pages_sold"],"우체국 구석의 옛 장부가 은호의 자루로 넘어갔다고 했다."),
        "r13_w2e_bell":("종탑 아래에서 설이와 너울이 다투고 있다",["w2e_k_done","w2_bell_silent"],"그날 밤 불이 꺼진 두 집 사람들은 아침이 되어서야 학교에 왔다고 했다."),
        "r13_w2e_numbers":("수리점 작업대에 계측 장부가 펼쳐져 있다",["w2e_p_done","numbers_forged"],"수리점 계측 장부에서 숫자 하나가 지워졌다는 말을 들었다."),
        "r13_w2e_tools":("부리가 할아버지 공구함 앞에 서 있다",["w2e_w_done","tools_sold"],"부리의 할아버지 공구함이 은호의 자루로 넘어갔다고 했다."),
        "r13_ep3_bell":("광장의 등이 한꺼번에 깜빡인다. 종탑 아래가 소란스럽다",["ep3_bell_seen","stone_hidden","bori_child_sick"],"그날 밤 종은 울리지 않았다. 아침에 보리네 아이가 열이 난다는 말을 들었다."),
        "r13_ep4_accused":("수리점 앞에 사람들이 모여 있다",["ep4_seen","ep4_open"],"수리점 앞에서 너울이 톡을 몰아세웠다는 말을 들었다."),
        "r13_ev_b_store":("창고 앞에서 백 부인이 누군가를 몰아세우고 있다",[],""),
    }

    # 0.18.53 (owner): press the person doing it, not a text marker. label: (person, event pose).
    # The event pose is used only once its art exists; until then the closest existing pose.
    # 0.18.63: event art delivered 2026-10-15 (art/event-actions9-20261015, dev/apply_map_actions.py).
    R13_OFFER_ACTORS={
        "r13_w1c_portrait":("resident_piko",("event_paintwipe","living_paint")),
        "r13_w1c_letters":("resident_sling",("event_steam","thinking")),
        "r13_w1c_extension":("resident_ttadak",("living_doorframe",)),
        "r13_w1c_seal":("resident_mungchi",("event_handrub",)),
        "r13_w1c_testimony":("resident_siluk",("event_whisper",)),
        "r13_b3_pages":("resident_librarian",("event_ledgertie",)),
        "r13_w2e_tools":("buri",("event_toolbox",)),
        "r13_ep4_accused":("resident_tok",None),
        "r13_ev_b_store":("resident_madam",None),
    }

    def r13_offer_for_person(person):
        for key,text in r13_offers_here():
            if R13_OFFER_ACTORS.get(key,(None,))[0]==person:return key
        return None

    def r13_offer_staged(key,actors):
        person=R13_OFFER_ACTORS.get(key,(None,))[0]
        return bool(person) and any(a["person"]==person for a in actors)

    def r13_person_action(person,entry=False):
        key=None if entry else r13_offer_for_person(person)
        return Return(("offer",key)) if key else Return(("person",person))

    def r13_offer_pose(person,poses):
        for pose in poses:
            if r13_acting_spec(person,pose):return pose
        return None

    _r13_offer_stage=r13_stage_people
    def r13_stage_people(entry=False):
        actors=_r13_offer_stage(entry)
        if entry or not store.room13:return actors
        result=[]
        for actor in actors:
            key=r13_offer_for_person(actor["person"])
            poses=R13_OFFER_ACTORS.get(key,(None,None))[1] if key else None
            pose=r13_offer_pose(actor["person"],poses) if poses else None
            if not pose or pose==actor["pose"]:result.append(actor);continue
            # Keep the same feet and stature; only the activity changes.
            old=r13_acting_spec(actor["person"],actor["pose"]) or {};new=r13_acting_spec(actor["person"],pose)
            ow,oh=r13_actor_geometry(actor["person"],actor["pose"]);nw,nh=r13_actor_geometry(actor["person"],pose)
            scale=float(actor["height"])/oh
            of=old.get("foot",[ow/2.0,oh]);nf=new.get("foot",[nw/2.0,nh])
            fx=actor["x"]+of[0]*scale;fy=actor["y"]+of[1]*scale
            # 0.18.63: the event art can be drawn at another pixel size and in other
            # proportions; its height follows the same standing height (shape ratio).
            probe={"standing_height_reference":1000}
            shape_old=r13_world_display_height(actor["person"],actor["pose"],1000.0,probe)
            shape_new=r13_world_display_height(actor["person"],pose,1000.0,probe)
            scale=float(actor["height"])*shape_new/max(1.0,shape_old)/nh
            # A place may name where the event happens (e.g. Buri leaves the workbench for the
            # toolbox on the floor): feet go there; the event pose stands free of furniture masks.
            spot=(r13_layout(store.room13["location"]) or {}).get("offer_spots",{}).get(key)
            if spot:
                fx,fy=spot
                line=r13_perspective_line(store.room13["location"])
                if line:scale=(line[0]*fy+line[1])*shape_new/1000.0/nh
            x=int(fx-nf[0]*scale);y=int(fy-nf[1]*scale);w=int(nw*scale);h=int(nh*scale)
            changed=dict(actor);changed.update(pose=pose,x=x,y=y,width=w,height=h,rect=[max(0,x),max(0,y),w,h],depth=y+h,contact=new.get("contact","standing"),occlusion=[] if spot else actor.get("occlusion",[]))
            result.append(changed)
        return sorted(result,key=lambda a:a["depth"])

    _r13_offer_edge_label=r13_world_edge_label
    def r13_world_edge_label(people):
        # Someone off to the side has an event going on: mark the edge tag too.
        label=_r13_offer_edge_label(people)
        return ("! "+label) if any(r13_offer_for_person(p) for p in people) else label

    def r13_offer(label):
        s=store.room13
        offers=dict(s.get("offers",{}))
        if label in offers:return
        offers[label]=dict(day=s["day"],period=s["period"],location=s["location"])
        r13_edit(offers=offers)
        # Screen tests written before 0.18.19 expect the old start-on-arrival.
        if "qa_auto_offer" in s.get("flags",[]):renpy.call("r13_take_offer",label)

    def r13_offers_here():
        s=store.room13 or {}
        return [(k,R13_EVENT_OFFERS[k][0]) for k,o in s.get("offers",{}).items()
            if k in R13_EVENT_OFFERS and o["day"]==s.get("day") and o["period"]==s.get("period") and o["location"]==s.get("location")]

    def r13_offers_tick():
        """Offers whose time slot has passed run without Dad: apply the look-away outcome."""
        s=store.room13;offers=dict(s.get("offers",{}));news=list(s.get("offer_news",[]));changed=False
        for k,o in list(offers.items()):
            if (o["day"],o["period"])!=(s["day"],s["period"]):
                text,flags,heard=R13_EVENT_OFFERS.get(k,("",[],""))
                if flags:r13_flag(*flags)
                if k=="r13_w2e_tools" and not r13_has("tok_cleared"):r13_flag("tools_missing")
                if heard:news.append(heard)
                offers.pop(k);changed=True
        if changed:r13_edit(offers=offers,offer_news=news)

label r13_offer_news:
    $ r13_offers_tick()
    if room13.get("offer_news"):
        $ _news=list(room13["offer_news"])
        $ r13_edit(offer_news=[])
        call r13_lines([(None,n) for n in _news],"offer:news:%d:%d"%(room13["day"],room13["period"]), binding_route="dynamic:565")
    return

label r13_take_offer(label):
    $ _o=dict(room13.get("offers",{}))
    $ _o.pop(label,None)
    $ r13_edit(offers=_o)
    call expression label
    return _return

screen r13_event_offers(ready=False):
    # Offers whose person stands here are pressed on that person (see r13_world_contents).
    $ staged=r13_stage_people()
    $ offers=[(k,t) for k,t in r13_offers_here() if not r13_offer_staged(k,staged)]
    if offers:
        vbox:
            xpos 24 ypos 236 spacing 8
            for key,text in offers:
                textbutton ("! "+text):
                    style "r13_action_button" xmaximum 620 padding (14,8) text_size r13_read_size(19,23)
                    action Return(("offer",key)) sensitive ready
                    tooltip "가까이 가서 본다"
