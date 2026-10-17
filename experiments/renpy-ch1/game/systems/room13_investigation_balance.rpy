# Keep working surfaces fixed; reserve people-sized lanes after authored map actions.
init 180 python:
    def r13_balance_translate(actor,dx,dy=0):
        result=dict(actor)
        result.update(x=actor['x']+dx,y=actor['y']+dy,
            rect=[actor['rect'][0]+dx,actor['rect'][1]+dy,actor['rect'][2],actor['rect'][3]],depth=actor['depth']+dy)
        # Furniture masks stay in world coordinates; carried foreground pieces follow the hands.
        if actor.get('map27_keepouts'):
            result['map27_keepouts']=[[(x+dx,y+dy) for x,y in poly] for poly in actor['map27_keepouts']]
        return result

    def r13_balance_school(actors):
        result=[]
        for actor in actors:
            if r13_offer_for_person(actor['person']):
                result.append(actor);continue
            slot=actor.get('slot')
            dx=0
            if slot and slot[3]=='class_back':
                # The teacher's approved chalkboard pose occupies the old middle column.
                dx={309:166,510:120}.get(slot[0],0)
            elif actor['person']=='resident_nubi' and actor['pose']=='map27_in_1':dx=220
            elif actor['pose']=='neutral':
                # Rear coat benches and front shelter aisle use alternating columns.
                dx={'resident_tori':-120,'resident_yeoni':-210,'resident_kongi':30}.get(actor['person'],0)
            result.append(r13_balance_translate(actor,dx) if dx else actor)
        return result

    def r13_balance_post(actors):
        # Preserve authored event composition as a unit; it is outside the idle work layout.
        if any(r13_offer_for_person(a['person']) for a in actors):return actors
        result=[]
        visitors=sorted([a for a in actors if a['person'] not in ('seryeon','resident_sling','resident_librarian')],key=lambda a:a['x'])
        lanes={a['person']:x for a,x in zip(visitors,(600,970,1160))}
        for actor in actors:
            if actor['person'] in lanes and actor.get('slot') and actor['slot'][3]=='counter':
                fx,fy=r13_ma_feet(actor)
                actor=r13_balance_translate(actor,int(round(lanes[actor['person']]-fx)))
            result.append(actor)
        return result

    _r13_balance_stage=r13_stage_people
    def r13_stage_people(entry=False):
        actors=_r13_balance_stage(entry)
        location=(store.room13 or {}).get('location')
        if location=='school' and r13_world_width()==1800:actors=r13_balance_school(actors)
        elif location=='post' and r13_world_width()==1280:actors=r13_balance_post(actors)
        return sorted(actors,key=lambda a:a['depth'])
