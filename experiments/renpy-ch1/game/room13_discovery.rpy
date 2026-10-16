# Small, existing-fact investigation loops. No evidence or story flags are
# awarded here; physical observations and explicit presentation remain separate.
init 61 python:
    R13_DISCOVERY_OBJECTS = json.load(renpy.file("assets/room13-discovery-objects.json")) if renpy.loadable("assets/room13-discovery-objects.json") else {}
    for discovery_place, discovery_objects in R13_DISCOVERY_OBJECTS.items():
        # These props belong to the expanded artwork, never the old backdrop.
        if discovery_place not in R13_WORLD_LAYOUTS:
            continue
        for discovery_key, discovery_spec in discovery_objects.items():
            if discovery_key in ROOM13["objects"].get(discovery_place, {}):
                raise ValueError("Discovery prop would replace an existing object: " + discovery_place + ":" + discovery_key)
            ROOM13["objects"].setdefault(discovery_place, {})[discovery_key] = dict(
                rect=list(discovery_spec["rect"]), text=discovery_spec["text"],
                need=[], give=[], flags=[], discovery_role="life")

    def r13_discovery_observation_feedback(location, key, was_observed=False):
        """Read-only follow-up; the caller captures was_observed before marking."""
        if not was_observed:
            return []
        spec = ROOM13["objects"].get(location, {}).get(key, {})
        keys = spec.get("give", [])
        if keys and all(item in store.room13["evidence"] for item in keys):
            names = " · ".join(ROOM13["evidence"][item]["name"] for item in keys)
            return [(None, "「" + names + "」는 이미 수첩에 적혀 있다. 수첩에서 다시 읽거나 상대에게 보여 줄 수 있다.")]
        if location == "workshop" and key == "plans":
            if r13_has("E04"):
                return [(None, "도면을 비교한 기록은 수첩에 적혀 있다. 부리에게 보여 주고 확인받을 수 있다.")]
            if any(action == "map" for action, unused in r13_actions()):
                return [(None, "도면을 보는 것만으로는 비교 기록이 남지 않는다. 도면의 조사 메뉴에서 외벽과 비교할 수 있다.")]
        if location == "inn" and key == "register" and r13_has("lodging"):
            return [(None, "장부의 내용은 주인에게 확인해야 한다. 아내의 초대 편지는 수첩에 남아 있다.")]
        return []

    # Keep the original disclosure bookkeeping, caution flags and later-week
    # routes. Only two early unrelated-fallback replies are replaced.
    r13_discovery_base_present = r13_present

    def r13_present(person, key, identity=False):
        owned = key in store.room13["evidence"]
        early = store.room13["day"] <= R13_TRIAL_DAY
        disclosure = key + (":named" if identity else ":anonymous")
        repeated = disclosure in store.room13.get("resident_knowledge", {}).get(person, [])
        response = r13_discovery_base_present(person, key, identity)
        if not owned or not early:
            return response
        if person == "granny" and key == "E01":
            if repeated:
                return [(person, "그 편지는 부인 부탁으로 제가 부쳤어요. 물어볼 일이 더 있으세요?")]
            if r13_has("lodging"):
                return [(person, "가족에게 돌려줘야 할 물건이 남았잖아요."),
                    ("dad", "아내가 정말 직접 연락해 달라고 부탁했는지도 듣고 싶습니다."),
                    (None, "대화 목록의 ‘아내가 저희를 부른다고 하던가요?’에서 더 물어볼 수 있다.")]
            return [(person, "부인 편지는 받으셨죠. 같은 방으로 드릴게요."),
                (None, "대화 목록에서 방을 부탁할 수 있다.")]
        if person == "buri" and key == "E04":
            if repeated:
                return [(person, "종이에 남은 선과 지금 열리는 길은 따로 확인해야 해요. 그 점은 달라지지 않았어요.")]
            return [(person, "집 구조는 옛 도면이고, 붉은 선은 할머니가 고치면서 덧그린 거예요."),
                ("dad", "이 기록만으로는 그 문이 지금도 열리는지까지 알 수 없겠군요."),
                (person, "네. 도면대로 지금도 열리는지는 직접 봐야죠.")]
        return response

init 62 python:
    for discovery_objects in R13_DISCOVERY_OBJECTS.values():
        for discovery_key, discovery_spec in discovery_objects.items():
            R13_OBJECT_NAMES[discovery_key] = discovery_spec["name"]
