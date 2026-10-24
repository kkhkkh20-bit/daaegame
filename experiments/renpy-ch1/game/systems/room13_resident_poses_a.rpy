# 주민 생활 동작 A안(흰 테두리 스티커) 그림 교체 (2026-10-24 소유자: "이것들 에셋 매칭해서 적용시켜줘").
# 같은 동작의 옛 그림이 쓰이던 자리만 바꾼다. 누가·어디서·언제·무슨 조건으로 서는지는
# 기존 배치 층(map9 176, solbang 177, map27 178, life groups 181, 회의 99)이 그대로 정한다.
# 교체표는 dev/import_resident_poses_a.py 가 만든다. 기존 JSON 은 영수증·지문 시험에 묶여 있어 고치지 않고,
# 여기서 같은 spec dict 를 제자리에서 바꾼다(행·R13_ACTING·CAST 가 같은 dict 를 함께 가리킨다).
# 옛 그림이 이미 다른 그림으로 바뀌어 있으면(다른 작업) 그 자리는 건드리지 않는다.
# 함수 덮어쓰기 층은 없다.
init 186 python:
    import copy as r13_poses_a_copy
    R13_RESIDENT_POSES_A = json.load(renpy.file("assets/room13-resident-poses-a.json")) if renpy.loadable("assets/room13-resident-poses-a.json") else {"slots": []}

    def r13_poses_a_targets(slot):
        person, pose = slot["person"], slot["pose"]
        kind = slot["kind"]
        if kind in ("acting", "cast", "map27", "map9", "life_group"):
            for table in (R13_ACTING, CAST):
                spec = table.get(person, {}).get(pose)
                if isinstance(spec, dict):
                    yield spec, None
        if kind == "map27":
            for row in R13_MAP_ACTION27["rows"]:
                if row.get("request_id") == slot.get("request_id") and row["person"] == person and row["pose"] == pose:
                    yield row["spec"], None
        if kind == "map9":
            for row in R13_MAP_WORK_NINE["people"]:
                if row["person"] == person and row["pose"] == pose:
                    yield row["spec"], row
        if kind == "life_group":
            for group in R13_LIFE_GROUPS:
                if group["id"] != slot.get("group"):continue
                for member in group["members"]:
                    if member["person"] == person and member["pose"] == pose and member.get("spec"):
                        yield member["spec"], None
        if kind == "meeting":
            spec = R13_MEETING_SEATED.get(person)
            if isinstance(spec, dict):
                yield spec, None

    def r13_poses_a_apply():
        changed = set()
        for slot in R13_RESIDENT_POSES_A["slots"]:
            fields = slot["fields"]
            if not renpy.loadable(fields["file"]):continue
            for spec, row in r13_poses_a_targets(slot):
                # 행과 R13_ACTING 이 같은 dict 를 가리키면 두 번째로 만날 때는 이미 바뀌어 있다.
                if spec.get("file") != fields["file"]:
                    if spec.get("file") != slot["old_file"]:continue
                    spec.update(r13_poses_a_copy.deepcopy(fields))
                if row is not None and slot.get("row_fields"):
                    row["source_size"] = list(slot["row_fields"]["source_size"])
                    row.setdefault("contacts", {})["contacts_normalized_full_canvas"] = r13_poses_a_copy.deepcopy(slot["row_fields"]["contacts_normalized_full_canvas"])
                if slot["kind"] != "meeting":
                    changed.add((slot["person"], slot["pose"]))
        # 현장 그림은 "인물 자세" 이미지 이름으로 그린다(r13_art). 바뀐 자리만 새 그림으로 다시 등록한다.
        for person, pose in sorted(changed):
            spec = R13_ACTING.get(person, {}).get(pose) or CAST.get(person, {}).get(pose)
            if spec:
                renpy.image(person + " " + pose, Transform(Crop(tuple(spec["crop"]), spec["file"]), nearest=spec.get("nearest", True)))
        return changed

    R13_RESIDENT_POSES_A_CHANGED = r13_poses_a_apply()
