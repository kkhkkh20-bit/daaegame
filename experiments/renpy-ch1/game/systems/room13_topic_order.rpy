# Question numbers never move (owner, 0.18.22). Many layers insert topics at the front or
# middle of r13_topics; the list is shown in the order each topic first appeared to Dad,
# so a new question is added at the bottom and the ones already seen keep their number.
init 130 python:
    def r13_remember_topic_order(person):
        s=store.room13
        if not s:return
        orders=dict(s.get("topic_order",{}));known=list(orders.get(person,[]))
        new=[k for k,_ in r13_topics(person) if k not in known]
        if new:
            orders[person]=known+new
            r13_edit(topic_order=orders)

    def r13_topics_in_order(person):
        rows=r13_topics(person)
        known=(store.room13 or {}).get("topic_order",{}).get(person,[])
        rank={k:i for i,k in enumerate(known)}
        return sorted(rows,key=lambda row:(rank.get(row[0],len(rank)),rows.index(row)))
