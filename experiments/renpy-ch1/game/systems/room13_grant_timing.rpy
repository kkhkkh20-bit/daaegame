# Records from a presentation are granted after the reaction is read (owner, 0.18.20).
#   show record → reaction lines → lines finish → new record + notice.
#   Only grants made while a reaction is computed are held. Flags and what the resident has seen
#   keep their timing. The pending list lives in the saved state, so saving or loading during the
#   reaction neither loses nor repeats it; r13_grant itself skips records already owned.
default r13_defer_grants = False

init 125 python:
    _r13_grant_now=r13_grant
    def r13_grant(keys,source):
        if store.r13_defer_grants:
            n=winter_copy.deepcopy(store.room13)
            n.setdefault("pending_grants",[]).append([list(keys),source])
            store.room13=n
            return
        _r13_grant_now(keys,source)

    def r13_flush_grants():
        pending=list((store.room13 or {}).get("pending_grants",[]))
        if not pending:return
        n=winter_copy.deepcopy(store.room13);n["pending_grants"]=[];store.room13=n
        for keys,source in pending:
            _r13_grant_now(keys,source)
