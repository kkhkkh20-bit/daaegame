"""Align the audited defaults to the confirmed board without inventing expressions.

Run once per approved source revision; unchanged roles and authored map actions stay intact.
"""
import copy
import csv
import json
from pathlib import Path
from PIL import Image
from apply_role_connect import (ROOT, GAME, ASSETS, FILES, load, dump, indent_of,
    sha, write_webp, geometry, world_entries, canon_fullbody, kept_map_actions)
from apply_npc_redesign import resample

ART = ROOT / "art/canonical-channel-alignment-20261017"
ROLES = ("neoul", "resident_teacher", "resident_tosil", "resident_momo", "resident_bori", "resident_seol")


def main():
    ART.mkdir(exist_ok=True)
    data = {k: load(p) for k, p in FILES.items()}
    people = data["fullbody"]["people"]
    canon = {r["roleId"]: r for r in csv.DictReader((ROOT / "art/canonical48-rev45/canonical48.csv").open(encoding="utf-8-sig"))}
    backup = ART / "original-entries.json"
    if not backup.exists():
        backup.write_text(json.dumps({k: {r: copy.deepcopy(v.get("people", v).get(r)) for r in ROLES + ("guard",)}
                                     for k, v in data.items() if k != "dotfx"}, ensure_ascii=False, indent=1) + "\n")
    baseline = load(backup)
    report = {"basis": "Owner requested canonical48 defaults and approved rev47 updates; no new art generated.",
              "roles": {}, "pending_expressions": {}, "pending_layout_actions": [],
              "guard_pending": "Five non-neutral dialogue expressions and authored investigation actions still need the approved mouth correction; retained, not marked complete."}
    for rid in ROLES:
        src = ROOT / "art/canonical48-rev45/originals" / (rid + ".webp")
        digest = sha(src)
        assert digest == canon[rid]["sha256"], rid
        img = resample(Image.open(src).convert("RGBA"), 0.5)
        file = write_webp(img, "room13-canonical-default-%s.webp" % rid, False, False)
        geo = geometry(img, 4, 1)
        version = "canonical48-rev47-aligned"
        cast, acting, portraits = world_entries(file, geo, version)
        kept = kept_map_actions(rid, data["acting"].get(rid, {}))
        prior = baseline["acting"].get(rid, {})
        if rid == "resident_tosil" and "hold_storybook" in prior:
            kept["hold_storybook"] = prior["hold_storybook"]
        pending = [k for k in prior if k not in acting and k not in kept and not k.startswith("avatar_")]
        acting.update(kept)
        fb = canon_fullbody(people[rid]["name_ko"], file, img, geo, digest, version)
        if rid == "resident_tosil":
            fb["poses"] = baseline["fullbody"][rid].get("poses", {})
        data["cast"][rid], data["acting"][rid], data["portraits"][rid], people[rid] = cast, acting, portraits, fb
        data["meeting"].pop(rid, None)
        data["dotfx"].get("blink", {}).get("people", {}).pop(rid, None)
        report["roles"][rid] = {"source": str(src.relative_to(ROOT)), "sha256": digest,
                                  "preserved_approved_actions": sorted(kept), "pending_revised_actions": pending}

    # Mouth-fixed neutral also supplies profiles and ordinary standing paths.
    # Distinct authored actions and the five uncorrected expressions remain honest production debt.
    fixed = people["guard"]["images"]["neutral"]
    img = Image.open(GAME / fixed["file"]).convert("RGBA")
    cast, acting, portraits = world_entries(fixed["file"], geometry(img, 4, 2), "dolmok-mouth-v1-approved")
    for key in ("neutral", "world", "interview_neutral"):
        data["cast"]["guard"][key] = cast[key]
    for key in cast:
        if key.startswith(("avatar_", "portrait_")):
            data["cast"]["guard"][key] = cast[key]
    data["acting"]["guard"]["neutral"] = acting["neutral"]
    for key in acting:
        if key.startswith("avatar_"):
            data["acting"]["guard"][key] = acting[key]
    data["portraits"]["guard"] = portraits
    # Explicit metadata: aliases are fallback, never six completed expressions.
    for rid, fb in people.items():
        images = fb.get("images", {})
        if images and len({v["file"] for v in images.values()}) == 1:
            missing = [e for e in images if e != "neutral"]
            if missing:
                report["pending_expressions"][rid] = missing
                for e in missing:
                    images[e]["fallback"] = "neutral"
                    images[e]["production_status"] = "pending"

    layout_path = ASSETS / "room13-world-layout.json"
    layout = load(layout_path)
    layout_backup = ART / "original-layout.json"
    if not layout_backup.exists():
        layout_backup.write_text(layout_path.read_text())
    original_layout = load(layout_backup)
    for place, field, rid in (("inn", "slot_actions", "resident_guseul"),
                              ("inn", "slot_actions", "resident_madam"),
                              ("hall", "slot_actions", "doto"),
                              ("post", "old_scene_slot_actions", "resident_guseul")):
        previous = original_layout[place][field].get(rid)
        layout[place][field].pop(rid, None)
        if previous is not None:
            report["pending_layout_actions"].append({"place": place, "field": field, "person": rid, "requested": previous})
    # Removing an unavailable override lets the ordinary current neutral path render.
    dump(layout_path, layout, indent_of(layout_path))
    for kind, path in FILES.items():
        dump(path, data[kind], indent_of(path))
    (ART / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
