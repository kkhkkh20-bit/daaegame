# One player-facing collection. Domain inventories remain separate so evidence,
# consumable goods and borrowed tools keep their existing ownership rules.
init 148 python:
    def r13_catalog_object(key):
        if not isinstance(key,str) or ":" not in key:return None
        kind,item=key.split(":",1)
        if kind=="bag" and item in set(R13_SHOP)|set(R13_BORROW):return kind,item
        if kind=="tool" and item in R13_INSPECTION_ITEMS:return kind,item
        return None

    def r13_catalog_owned(key):
        obj=r13_catalog_object(key)
        if obj:
            kind,item=obj
            return item in (r13_wallet(store.room13)["items"] if kind=="bag" else r13_inspection_state()["inventory"])
        return bool(key and key in ROOM13["evidence"] and key in (store.room13 or {}).get("evidence",[]))

    def r13_catalog_entries(archive=False,hearing=False,shelf=False):
        raw=list((getattr(persistent,"room13_knowledge",[]) or []) if archive else (store.room13 or {}).get("evidence",[]))
        keys=list(dict.fromkeys(k for k in raw if k in ROOM13["evidence"]))
        # 0.18.99: records of a finished episode move to the 지난 사건 shelf (systems/room13_shelf.rpy).
        if not archive:
            shelved=getattr(store,"r13_shelved_keys",lambda:set())()
            if shelf:return [k for k in keys if k in shelved]
            keys=[k for k in keys if k not in shelved]
        if not archive and not hearing:
            keys += ["tool:"+k for k in r13_inspection_state()["inventory"] if k in R13_INSPECTION_ITEMS]
            keys += ["bag:"+k for k in r13_wallet(store.room13)["items"] if k in set(R13_SHOP)|set(R13_BORROW)]
        return list(dict.fromkeys(keys))

    def r13_catalog_observed(key):
        """0.18.99: while a case is open a record shows only what was observed; the meaning
        ("그래서 무슨 뜻? …") is for the meeting to reveal. Shelved (finished) records show it again."""
        ev=ROOM13["evidence"].get(key)
        if not ev or "그래서 무슨 뜻?" not in ev.get("establishes",""):return ev
        if key in getattr(store,"r13_shelved_keys",lambda:set())():return ev
        ev=dict(ev);ev["establishes"]=ev["establishes"].split("그래서 무슨 뜻?")[0].strip()
        return ev

    def r13_catalog_record(key):
        obj=r13_catalog_object(key)
        if not obj:return r13_catalog_observed(key)
        kind,item=obj
        if kind=="tool":name,detail=R13_INSPECTION_ITEMS[item]
        else:
            spec=R13_SHOP.get(item) or R13_BORROW[item]
            name,detail=spec["title"],spec["detail"]
        return dict(name=name,establishes=detail,kind="물건")

    def r13_catalog_title(key):
        record=r13_catalog_record(key)
        return record["name"] if record else "자료"

    def r13_catalog_origin(key):
        obj=r13_catalog_object(key)
        if not obj:return r13_record_origin(key)
        kind,item=obj
        if kind=="tool":return "필기함에서 챙긴 물건"
        if item in r13_wallet(store.room13)["borrowed"]:return "빌린 물건 · 보증금은 돌려줄 때 반환"
        return "가지고 있는 물건"

    def r13_catalog_object_icon(key):
        art=r13_material_art(key)
        if art is not None:return art
        kind,item=r13_catalog_object(key)
        return r13_inspection_icon(item,96,96) if kind=="tool" else R13PixelIcon(item,6)

    def r13_catalog_can_present(key,hearing=False):
        return r13_catalog_owned(key) and (not hearing or key in ROOM13["evidence"])

    _r13_catalog_topics=r13_topics
    def r13_topics(person):
        # No separate hand-over / return / snack buttons next to showing a material.
        return [(key,spec) for key,spec in _r13_catalog_topics(person)
            if not key.startswith(("item:","return:")) and key not in ("life:snack","home:records")]

    def r13_catalog_offer(person,key):
        obj=r13_catalog_object(key)
        if not obj or obj[0]!="bag" or not r13_catalog_owned(key):return None
        item=obj[1]
        allowed=dict(_r13_catalog_topics(person))
        for topic in ("return:"+item,"item:"+item,"life:snack" if item=="snack" else ""):
            if topic and topic in allowed:return topic
        return None

    def r13_catalog_transferable(key):
        obj=r13_catalog_object(key)
        if not obj or obj[0]!="bag" or not r13_catalog_owned(key):return False
        item=obj[1]
        # Only authored recipients can accept this object. Avoid checking all
        # residents on every card redraw; retain current day/quest eligibility.
        # The offer flow revalidates again before consumption.
        topics=("return:"+item,"item:"+item,"life:snack" if item=="snack" else "")
        people={ROOM13["topics"][topic]["npc"] for topic in topics if topic in ROOM13["topics"]}
        return any(r13_catalog_offer(person,key) for person in people)

    def r13_complete_catalog_offer(person,key,topic):
        # Revalidate at commit. A decline, wrong recipient or repeated callback cannot
        # consume an item, refund a deposit, grant evidence, or record resident help.
        if not topic or r13_catalog_offer(person,key)!=topic:return False
        r13_finish_topic(topic)
        return True

label r13_show_catalog_object(person,key):
    if not r13_catalog_object(key) or not r13_catalog_owned(key):
        return
    show screen r13_material_corner(key)
    $ r13_offer_topic=r13_catalog_offer(person,key)
    if not r13_offer_topic:
        call r13_lines([(person,"아빠 물건이네. 더 아는 건 없어." if person=="daram" else "제게 보여 주셔도 따로 아는 이야기는 없어요.")],"material:show:"+person+":"+key, binding_route="dynamic:600")
    else:
        $ r13_offer_item_name=r13_catalog_title(key)
        if r13_offer_topic.startswith("return:"):
            call r13_lines([(person,"빌려 드린 물건, 이제 돌려주시려고요?")],"material:return_offer:"+key, binding_route="dynamic:601")
            $ r13_offer_yes="돌려준다 · "+r13_offer_item_name
        elif r13_offer_topic=="life:snack":
            call r13_lines([("daram","구운 밤이다! 아빠, 같이 먹어도 돼?")],"material:snack_offer")
            $ r13_offer_yes="함께 먹는다 · "+r13_offer_item_name
        elif r13_offer_topic=="item:postcard":
            call r13_lines([("daram","이 엽서에 엄마한테 보낼 그림 그려도 돼?")],"material:postcard_offer")
            $ r13_offer_yes="엽서를 함께 쓴다"
        else:
            call r13_lines([(person,"나 주려고 가져온 거야?" if person=="daram" else "이 물건을 제게 주시려는 건가요?")],"material:gift_offer:"+person+":"+key, binding_route="dynamic:604")
            $ r13_offer_yes="건넨다 · "+r13_offer_item_name+" 1개"
        menu:
            "[r13_offer_yes]":
                if r13_catalog_offer(person,key)==r13_offer_topic:
                    $ r13_offer_rows=r13_conversation_topic_lines(r13_offer_topic)
                    call r13_lines(r13_offer_rows,"material:accepted:"+r13_offer_topic, binding_route="dynamic:605")
                    $ r13_topic_shown=r13_offer_rows
                    $ r13_complete_catalog_offer(person,key,r13_offer_topic)
            "지금은 보여주기만 한다":
                pass
    hide screen r13_material_corner
    return
