# Called by r13_scene after its existing fade to black. This file owns only
# arrival presentation; it never advances the clock or changes the location.
init 59 python:
    def r13_arrival_info(bg,title,mood="calm"):
        state=store.room13
        if not state or mood in ("travel","hearing"):
            return None
        location=state.get("location")
        actual=R13_PLACES.get(location)
        # Several scripted scenes deliberately reuse a background while the
        # exploration location still points elsewhere. Only canonical arrivals
        # qualify, never carriage, courtroom, visits, flashbacks or epilogues.
        if not actual or (title,bg)!=tuple(actual):
            return None
        key=(state["day"],state["period"],location,state.get("case_state"))
        if key in state.get("arrival_seen",[]):
            return None
        return dict(key=key,clock=r13_clock(),place=title)

    def r13_arrival_claim(bg,title,mood="calm"):
        info=r13_arrival_info(bg,title,mood)
        if info is None:
            return None
        # Replace the entire snapshot, just like r13_edit/r13_flag. The record
        # travels with saves and rollback, never persistent cross-playthrough
        # state. Claim before the interaction so loading during it cannot add a
        # second arrival after the displayed card is dismissed.
        state=winter_copy.deepcopy(store.room13)
        state["arrival_seen"]=list(state.get("arrival_seen",[]))+[info["key"]]
        store.room13=state
        return info

transform r13_arrival_reveal:
    alpha 0.0
    linear .16 alpha 1.0

# Compatibility for saves made while the former arrival card was open.
screen r13_arrival_card(info):
    timer .01 action Return()

label r13_arrival(bg,title,mood="calm"):
    # Clock and location stay in the normal HUD; no blocking arrival card.
    return
