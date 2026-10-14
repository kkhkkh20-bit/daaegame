# Each run starts from zero (owner's rule): no records, routes or rewards carry
# over from an earlier run. Only conveniences stay (settings, read-dialogue skip,
# skipping already seen cinematics). The player's own knowledge is the only edge.
init 105 python:
    _r13_fresh_new=r13_new
    def r13_new():
        s=_r13_fresh_new()
        s["secret_route_unlocked"]=False
        s["learning_archive"]=[]
        return s

    # Skip modes are one-shot footer buttons (0.18.4); a loaded save starts with them off.
    def r13_disable_fast_read():
        store.r13_fast_read=False
        store.r13_fast_all=False
    config.after_load_callbacks.append(r13_disable_fast_read)
