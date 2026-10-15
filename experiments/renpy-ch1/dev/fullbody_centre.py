"""Upper-body centre of each dialogue figure (0.18.39, owner: "까로를 좀 더 중앙으로").

The close-up is placed by its crop box at x=640. A long tail or a wide coat pulls the head and
torso to one side of that box (Karo: 58px left). This measures, on the neutral image, the mean x of
opaque pixels in the top 45% of the crop, relative to the crop centre, and writes
assets/room13-fullbody-centre.json. Re-run after new full-body art: python3 dev/fullbody_centre.py
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image
GAME = Path(__file__).resolve().parents[1] / "game"
people = json.loads((GAME / "assets/room13-fullbody-dialogue.json").read_text(encoding="utf-8"))["people"]
out = {}
for person, entry in sorted(people.items()):
    x, y, w, h = entry["crop"]
    alpha = np.array(Image.open(GAME / entry["images"]["neutral"]["file"]).convert("RGBA").crop((x, y, x + w, y + h)))[:, :, 3]
    xs = np.nonzero(alpha[:int(h * .45)] > 0)[1]
    out[person] = int(round(xs.mean() - w / 2)) if len(xs) else 0
(GAME / "assets/room13-fullbody-centre.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(out), "figures")
