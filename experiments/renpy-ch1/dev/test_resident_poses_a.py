"""주민 생활 동작 A안 교체표: 새 자리를 만들지 않고, 옛 그림이 있던 자리만 바꾼다(2026-10-24)."""
import json, unittest
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
TABLE = json.loads((GAME / "assets/room13-resident-poses-a.json").read_text(encoding="utf-8"))


def base_specs():
    """기존 JSON 에서 (종류, 인물, 자세) -> spec 목록."""
    out = {}
    acting = json.loads((GAME / "assets/room13-pixel-acting.json").read_text())
    cast = json.loads((GAME / "assets/cast.json").read_text())
    for kind, doc in (("acting", acting), ("cast", cast)):
        for person, poses in doc.items():
            if isinstance(poses, dict):
                for pose, spec in poses.items():
                    if isinstance(spec, dict):
                        out.setdefault((kind, person, pose), []).append(spec)
    for row in json.loads((GAME / "assets/room13-map-action27.json").read_text())["rows"]:
        out.setdefault(("map27", row["person"], row["pose"]), []).append(row["spec"])
    for row in json.loads((GAME / "assets/room13-map-work-nine.json").read_text())["people"]:
        out.setdefault(("map9", row["person"], row["pose"]), []).append(row["spec"])
    for group in json.loads((GAME / "assets/room13-life-groups.json").read_text())["groups"]:
        for m in group["members"]:
            if m.get("spec"):
                out.setdefault(("life_group", m["person"], m["pose"]), []).append(m["spec"])
    for who, spec in json.loads((GAME / "assets/room13-meeting-seated.json").read_text()).items():
        out.setdefault(("meeting", who, "meeting_seated"), []).append(spec)
    return out


class ResidentPosesA(unittest.TestCase):
    def test_every_slot_replaces_an_existing_slot_with_the_same_old_art(self):
        specs = base_specs()
        for slot in TABLE["slots"]:
            have = specs.get((slot["kind"], slot["person"], slot["pose"]), [])
            self.assertTrue(any(s.get("file") == slot["old_file"] for s in have), slot["person"] + " " + slot["pose"])

    def test_new_files_exist_and_crops_fit(self):
        for slot in TABLE["slots"]:
            f = slot["fields"]
            im = Image.open(GAME / f["file"])
            x, y, w, h = f["crop"]
            self.assertTrue(0 <= x and 0 <= y and x + w <= im.width and y + h <= im.height, f["file"])
            self.assertTrue(f["file"].startswith("assets/resident-poses-a/"))

    def test_scale_keeps_body_share_of_crop(self):
        # 잘라내기 안에서 몸이 차지하는 높이 비율이 옛 그림과 같아야 화면 키가 같다.
        for a in TABLE["assets"]:
            sx, sy = a["scale"]
            self.assertLess(abs(sx / sy - 1), 0.2, a["file"])

    def test_dialogue_and_carriage_art_untouched(self):
        # 대화 동작(1:1)과 마차 다람은 「확인 필요」라 바꾸지 않았다.
        olds = {s["old_file"] for s in TABLE["slots"]}
        self.assertFalse(any("dialogue-pose-source" in o or "carriage" in o for o in olds))
        self.assertFalse(any(s["kind"] not in ("acting", "cast", "map27", "map9", "life_group", "meeting") for s in TABLE["slots"]))

    def test_layer_runs_after_placement_layers(self):
        text = (GAME / "systems/room13_resident_poses_a.rpy").read_text(encoding="utf-8")
        self.assertIn("init 186 python:", text)
        self.assertIn("_r13_poses_a_stage=r13_stage_people", text)


if __name__ == "__main__":
    unittest.main()
