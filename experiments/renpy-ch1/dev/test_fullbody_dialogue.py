"""0.18.5 full-body dialogue expressions: data completeness and selection rules.

The real Ren'Py rendering is checked by dev/run_renpy_tests.sh fullbody_dialogue
(screenshots of every character and expression); this file checks the data
and the pure selection functions without a renderer.
"""
import ast, json, textwrap, unittest
from pathlib import Path
from types import SimpleNamespace

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
DATA = json.loads((GAME / "assets/room13-fullbody-dialogue.json").read_text(encoding="utf-8"))
LINES = json.loads((GAME / "assets/room13-fullbody-line-emotions.json").read_text(encoding="utf-8"))
PORTRAITS = json.loads((GAME / "assets/room13-portraits.json").read_text(encoding="utf-8"))
DIRECTION = json.loads((GAME / "assets/room13-line-direction.json").read_text(encoding="utf-8"))
EMOTIONS = ("neutral", "joy", "flustered", "angry", "anxious", "surprise")


def load_module():
    source = (GAME / "room13_fullbody_dialogue.rpy").read_text(encoding="utf-8")
    body = source[source.index("init 58 python:") + len("init 58 python:"):]
    loaded = {"assets/room13-fullbody-dialogue.json": DATA, "assets/room13-fullbody-line-emotions.json": LINES,
              "assets/room13-fullbody-centre.json": json.loads((GAME / "assets/room13-fullbody-centre.json").read_text(encoding="utf-8"))}
    env = {"json": SimpleNamespace(load=lambda f: f),
           "renpy": SimpleNamespace(loadable=lambda name: name in loaded or (GAME / name).exists(),
                                    file=lambda name: loaded[name])}
    exec(compile(ast.parse(textwrap.dedent(body)), "room13_fullbody_dialogue.rpy", "exec"), env)
    return env


class FullbodyData(unittest.TestCase):
    def test_every_dialogue_character_has_six_expressions_on_disk(self):
        self.assertEqual(set(DATA["people"]), set(PORTRAITS))
        # 43 original characters + 13 from the 2026-10-16 episode art (dev/apply_ep_art.py)
        # + 7 new residents connected to their confirmed pictures in 0.19.0 (dev/apply_role_connect.py).
        self.assertEqual(len(DATA["people"]), 63)
        for person, entry in DATA["people"].items():
            # 0.18.92: the expression package can add a named extra (bami "thinking").
            self.assertEqual(set(entry["images"]) - {"thinking"}, set(EMOTIONS), person)
            for pose, image in entry.get("poses", {}).items():
                path = GAME / image["file"]
                self.assertTrue(path.exists(), path)
                with Image.open(path) as im:
                    self.assertEqual(list(im.size), image["size"], path)
                x, y, w, h = image["crop"]
                self.assertLessEqual(x + w, image["size"][0], (person, pose))
                self.assertLessEqual(y + h, image["size"][1], (person, pose))
            for emotion, image in entry["images"].items():
                path = GAME / image["file"]
                self.assertTrue(path.exists(), path)
                with Image.open(path) as im:
                    self.assertEqual(list(im.size), image["size"], path)
                    self.assertEqual(im.mode, "RGBA", path)

    def test_one_crop_fits_every_expression_of_a_character(self):
        for person, entry in DATA["people"].items():
            x, y, w, h = entry["crop"]
            fx, fy, fw, fh = entry["figure"]
            mapped = any("map" in image for image in entry["images"].values())
            if not mapped:
                self.assertTrue(x <= fx and y <= fy and fx + fw <= x + w and fy + fh <= y + h, person)
            for image in entry["images"].values():
                if "map" in image:
                    # 0.18.92: own pixels + map to the reference canvas (dev/apply_expression_acting.py)
                    ix, iy, iw, ih = image["crop"]
                    self.assertTrue(0 <= ix and 0 <= iy and ix + iw <= image["size"][0] and iy + ih <= image["size"][1], person)
                    if image.get("cell"):
                        self.assertTrue(ix % 2 == 0 and iy % 2 == 0 and iw % 2 == 0 and ih % 2 == 0, person)
                else:
                    self.assertLessEqual(x + w, image["size"][0], person)
                    self.assertLessEqual(y + h, image["size"][1], person)

    def test_old_busts_and_sprites_are_kept(self):
        for spec in (s for poses in PORTRAITS.values() for s in poses.values()):
            self.assertTrue((GAME / spec["file"]).exists(), spec["file"])

    def test_line_emotions_match_actual_dialogue_text(self):
        # 0.18.35: compare with the dialogue itself (dev/line_cues.py), not with the
        # older cue file, which had drifted together with these cues.
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import line_cues
        rows = line_cues.scene_rows()
        for identity, cues in LINES["lines"].items():
            for index, cue in cues.items():
                actual = rows[identity][int(index)]
                self.assertEqual((cue["person"], cue["text"]), tuple(actual[:2]), (identity, index))
                self.assertIn(cue["emotion"], EMOTIONS)
                self.assertNotEqual(cue["person"], "dad")  # Dad is never drawn
        used = {cue["emotion"] for cues in LINES["lines"].values() for cue in cues.values()}
        self.assertTrue({"angry", "anxious", "flustered", "surprise", "joy"} <= used)


class FullbodySelection(unittest.TestCase):
    def setUp(self):
        self.env = load_module()

    def test_authored_pose_picture_is_used_with_the_character_scale(self):
        # 0.18.89 (dev/apply_ep_art.py): a pose with its own picture wins over the emotion.
        spec = self.env["r13_fullbody_spec"]
        posed = spec("kid_kkomi", "door_peek")
        self.assertEqual(posed["file"], DATA["people"]["kid_kkomi"]["poses"]["door_peek"]["file"])
        self.assertEqual(posed["crop"], DATA["people"]["kid_kkomi"]["poses"]["door_peek"]["crop"])
        self.assertEqual(spec("kid_kkomi", "joy")["file"], DATA["people"]["kid_kkomi"]["images"]["joy"]["file"])
        self.assertEqual(spec("granny", "withdraw_hand")["emotion"], "withdraw_hand")
        self.assertEqual(spec("granny", "neutral")["file"], DATA["people"]["granny"]["images"]["neutral"]["file"])

    def test_legacy_keys_map_to_fullbody_images(self):
        emotion = self.env["r13_fullbody_emotion"]
        self.assertEqual(emotion("interview_distressed"), "anxious")
        self.assertEqual(emotion("expressive"), "joy")
        self.assertEqual(emotion("thinking"), "neutral")
        self.assertEqual(emotion("panic"), "surprise")
        self.assertEqual(emotion("chair_listen"), "neutral")
        for key in EMOTIONS:
            self.assertEqual(emotion(key), key)

    def test_authored_line_overrides_only_on_matching_text(self):
        pick = self.env["r13_fullbody_line_emotion"]
        cue = LINES["lines"]["buri:consent:refused"]["0"]
        self.assertEqual(pick("buri:consent:refused", 0, cue["person"], cue["text"], "distressed", "distressed"), "angry")
        self.assertIsNone(pick("buri:consent:refused", 0, cue["person"], cue["text"] + " 바뀐 대사", "distressed", "distressed"))
        self.assertIsNone(pick("buri:consent:refused", 0, cue["person"], cue["text"], "distressed", "chair_read"))
        self.assertEqual(pick("x", 0, "karo", "t", "surprise", "neutral"), "surprise")

    def test_scale_is_fixed_per_character(self):
        scale = self.env["r13_fullbody_scale"]
        for person in DATA["people"]:
            self.assertGreater(scale(person, 840), 0)
            self.assertLessEqual(DATA["people"][person]["crop"][2] * scale(person, 760), 400.5)

    def test_no_mouth_or_idle_animation_is_added(self):
        code = [line for line in (GAME / "room13_fullbody_dialogue.rpy").read_text(encoding="utf-8").splitlines()
                if not line.lstrip().startswith("#")]
        for word in ("R13CharacterMotion", "function=", "mouth"):
            self.assertFalse(any(word in line for line in code), word)


if __name__ == "__main__":
    unittest.main()
