# Knowledge eligibility is captured at NEW GAME, never unlocked mid-run.
init 90 python:
    def r13_secret_route_available():
        return bool((store.room13 or {}).get("secret_route_unlocked", False))

    for _key in ("map", "passage_measure"):
        ROOM13["activities"][_key]["secret_route_only"] = True
    ROOM13["topics"]["mystery:door"]["secret_route_only"] = True
    for _place, _key in (("room13", "books"), ("kitchen", "shelf"), ("workshop", "plans")):
        ROOM13["objects"][_place][_key]["secret_route_only"] = True
    for _spec in ROOM13["objects"].get("passage", {}).values():
        _spec["secret_route_only"] = True

    _r13_route_available = r13_available
    def r13_available(spec):
        if spec.get("secret_route_only") and not r13_secret_route_available():
            return False
        return _r13_route_available(spec)

    _r13_route_object_visible = r13_object_visible
    def r13_object_visible(spec):
        if spec.get("secret_route_only") and not r13_secret_route_available():
            return False
        return _r13_route_object_visible(spec)

    _r13_route_places = r13_places
    def r13_places():
        return [p for p in _r13_route_places() if p != "passage" or r13_secret_route_available()]
