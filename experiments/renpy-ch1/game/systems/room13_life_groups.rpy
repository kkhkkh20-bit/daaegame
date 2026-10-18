# Optional, non-consuming village moments. No schedule or story knowledge writes.
# 181 is deliberately after map27(178), contacts(179), and balance(180).
default r13_life_field_active = False

init 181 python:
    R13_LIFE_GROUPS = json.load(renpy.file("assets/room13-life-groups.json"))["groups"]
    for _lg in R13_LIFE_GROUPS:
        for _member in _lg["members"]:
            # New map-only art can be supplied here without changing dialogue portraits.
            _spec = _member.get("spec")
            if _spec and renpy.loadable(_spec["file"]):
                R13_ACTING.setdefault(_member["person"], {})[_member["pose"]] = _spec
                CAST[_member["person"]][_member["pose"]] = _spec
                renpy.image(_member["person"]+" "+_member["pose"], Transform(Crop(tuple(_spec["crop"]), _spec["file"]), nearest=True))

    def r13_life_group_allowed(row, actors, entry=False):
        s = store.room13 or {}
        if entry or row["status"] != "approved" or not getattr(store, "r13_life_field_active", False):return False
        if any(getattr(store, name, False) for name in ("r13_cg_active", "r13_meeting_active", "r13_meeting_live_active", "r13_aftermath_active", "r13_ending_story_active")):return False
        if set(renpy.get_showing_tags()).intersection(("r13_ep_cut", "r13_ep_book")):return False
        if s.get("location") != row["location"] or s.get("day") not in row["days"] or s.get("period") not in row["periods"]:return False
        if r13_world_width() != row["world_width"]:return False
        flags = set(s.get("flags", []))
        if not set(row["need_flags"]) <= flags or flags.intersection(row["not_flags"]):return False
        members = {m["person"] for m in row["members"]}
        if "resident_tok" in members and "tok_detained" in flags and "tok_cleared" not in flags:return False
        if any(r13_offer_for_person(person) for person in members):return False
        if row.get("conditional_cast"):
            # An ordinary school event also takes precedence over this optional play scene.
            if r13_offers_here() or any(a["person"] in members for a in actors):return False
        else:
            visible = set(r13_visible_people())
            present = {a["person"]: a for a in actors}
            for member in row["members"]:
                who = member["person"]
                if who not in visible or who not in present or r13_where(who) != row["location"]:return False
                if present[who]["pose"] not in member["replace_poses"]:return False
        for member in row["members"]:
            spec = r13_acting_spec(member["person"], member["pose"])
            if not spec or not renpy.loadable(spec["file"]):return False
            if member["anchor"] not in spec and member["anchor"] not in spec.get("anchors", {}):return False
        return True

    def r13_life_group_actor(actor, member, group):
        spec = r13_acting_spec(member["person"], member["pose"])
        anchors = dict(spec.get("anchors", {}))
        for name in ("foot", "hand", "seat"):
            if name in spec:anchors[name] = spec[name]
        geometry_spec = dict(spec, anchors=anchors)
        polygons = list(member.get("occlusion_polygons", []))
        if member.get("occlusion"):
            polygons.append(R13_WORLD_LAYOUTS[member["occlusion"]]["occlusion"])
        variant = dict(render_height=member["height"], anchor=member["anchor"], target=member["target"], depth=member["depth"], occlusion=polygons)
        # Reuse the exact draw/pick foreground masks, including authored hands and tools.
        result = r13_map27_geometry(actor, geometry_spec, variant, group["world_width"])
        result.update(pose=member["pose"], life_group=group["id"], activity=group["label"])
        if "nameplate_top" in member:result["nameplate_top"]=member["nameplate_top"]
        return result

    def r13_life_group_overlap(a, b):
        return max(0, min(a[0]+a[2], b[0]+b[2])-max(a[0], b[0])) * max(0, min(a[1]+a[3], b[1]+b[3])-max(a[1], b[1]))

    def r13_life_group_clear(row, placed, others):
        # Conservative bounds check: leave the existing people untouched if the space is occupied.
        # These rectangles only reject layouts; they are NEVER used as click targets.
        for actor in placed:
            rect = actor["rect"]
            if any(r13_life_group_overlap(rect, other["rect"]) > min(rect[2]*rect[3], other["rect"][2]*other["rect"][3])*.08 for other in others):return False
            keys = ("stove", "firewood") if row["location"] == "school" else ("door",) if row["location"] == "inn" else ()
            if any(r13_life_group_overlap(rect, ROOM13["objects"][row["location"]][key]["rect"]) for key in keys):return False
        return True

    _r13_life_groups_stage = r13_stage_people
    def r13_stage_people(entry=False):
        actors = _r13_life_groups_stage(entry)
        # Deliberately no derived cache: final visible/where, offers, flags, entry,
        # active scene and geometry are read again after the upstream stage cache.
        for row in R13_LIFE_GROUPS:
            if not r13_life_group_allowed(row, actors, entry):continue
            members = {m["person"] for m in row["members"]}
            originals = {a["person"]: a for a in actors}
            placed = [r13_life_group_actor(originals.get(m["person"], dict(person=m["person"])), m, row) for m in row["members"]]
            others = [a for a in actors if a["person"] not in members]
            if r13_life_group_clear(row, placed, others):actors = others + placed
        return sorted(actors, key=lambda a: a["depth"])

    def r13_life_groups_here():
        actors = r13_stage_people(False)
        return [row for row in R13_LIFE_GROUPS if {a["person"] for a in actors if a.get("life_group") == row["id"]} == {m["person"] for m in row["members"]}]

    def r13_life_group_lines(key, person=None):
        # Rechecked when opening AND during every interaction, including load.
        row = next((r for r in r13_life_groups_here() if r["id"] == key), None)
        if not row:return []
        if person:
            text = row.get("individual_lines", {}).get(person)
            return ([(person, text)] + list(row["lines"]) if row.get("member_conversation") else [(person, text)]) if text else []
        return row["lines"]

    def r13_life_choice_is_group(choice):
        return isinstance(choice, (tuple, list)) and len(choice) == 2 and choice[0] in ("life_group", "life_child")

    _r13_life_groups_person_action = r13_person_action
    def r13_person_action(person, entry=False):
        if not entry and getattr(store,"r13_life_field_active",False):
            for row in R13_LIFE_GROUPS:
                if person not in row.get("individual_lines", {}):continue
                # Existing child/event actors have priority over optional play.
                if r13_offer_for_person(person) or any(a["person"]==person for a in _r13_life_groups_stage(entry)):break
                # A stale play button is safely consumed; the dispatcher rechecks
                # group presence before opening any conversation or writing state.
                return Return(("life_child", person))
        return _r13_life_groups_person_action(person, entry)

screen r13_life_group_labels(entry=False, ready=False):
    if not entry and r13_field_view == "people":
        for group in [g for g in r13_life_groups_here() if not g.get("member_conversation")]:
            fixed:
                area (group["label_position"][0],group["label_position"][1],R13_CONTROL["width"],r13_control_height())
                use r13_control(group["label"],"dialogue",Return(("life_group",group["id"])),enabled=ready,control_id="life_group_"+group["id"])

screen r13_life_group_conversation(key, person=None):
    modal True
    zorder 40
    default line_index = 0
    default ready = False
    timer .15 action SetScreenVariable("ready", True)
    $ lines = r13_life_group_lines(key, person)
    if not lines or line_index >= len(lines):
        timer .01 action Return(None)
    else:
        fixed:
            xoffset -r13_world_offset()
            for prop,px,py in r13_world_props(False):
                add prop xpos px ypos py
            use r13_resident_stage(False, False)
        frame:
            xpos 120 ypos 112 xsize 1040 padding (26,18) background R13InkPanel(alpha="e8")
            vbox:
                spacing 12
                text R13_NAMES[lines[line_index][0]] size 26 color "#f6d18a"
                text lines[line_index][1] size r13_read_size(26,30) color "#fff2cf" xsize 980
        use r13_footer_control(0,"돌아가기" if line_index == len(lines)-1 else "계속 듣기","dialogue",Return(None) if line_index == len(lines)-1 else SetScreenVariable("line_index",line_index+1),enabled=ready)
        use r13_footer_control(1,"그만 듣기","dialogue",Return(None),enabled=ready)
        use r13_footer_control(3,"저장",None,ShowMenu("save"))
        use r13_footer_control(4,"불러오기",None,ShowMenu("load"))
        key "game_menu" action Return(None)

label r13_life_group_talk(key, person=None):
    # No call to r13_talk/r13_lines/events: even encounter and read-knowledge flags stay unchanged.
    if r13_life_group_lines(key, person):
        call screen r13_life_group_conversation(key, person)
    return

label r13_life_field_person_dispatch:
    # Keep the main file's dialogue inventory line locations stable for its provenance audit.
    if r13_choice[0] == "life_group":
        call r13_life_group_talk(r13_choice[1]) from r13_life_group_field_return
    elif r13_choice[0] == "life_child":
        $ r13_life_child_group=next((g["id"] for g in r13_life_groups_here() if r13_choice[1] in g.get("individual_lines",{})),None)
        if r13_life_child_group:
            call r13_life_group_talk(r13_life_child_group,r13_choice[1]) from r13_life_child_field_return
    else:
        call r13_talk from r13_life_ordinary_person_return
    return
