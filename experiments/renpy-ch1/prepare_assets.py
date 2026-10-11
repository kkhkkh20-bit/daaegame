"""Copy existing approved assets without modifying image/audio originals."""
from pathlib import Path
import hashlib
import json
import shutil
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
SOURCE = REPO / "preview/ch1-gpt-20261008"
TARGET = ROOT / "game/assets"

FILES = {
    "carriage.png": "art/ch1/cinematics/carriage-family-close.png",
    "approach.png": "art/ch1/cinematics/village-approach-road.png",
    "room.png": "art/ch1/locations/BG04_I1_box_free.png",
    "pouch-world.png": "art/ch1/locations/C01_money_pouch_world_alpha.png",
    "flour-world.png": "art/ch1/locations/C02_powder_handprint_decal_alpha.png",
    "council.png": "art/council/council-room-background-v1.png",
    "pouch.png": "art/ch1/cinematics/sealed-pouch-close.png",
    "somsom.png": "art/ch1/discovery/somsom-held.png",
    "family.png": "art/ch1/dialogue-v2/family.png",
    "inn.png": "art/ch1/dialogue-v2/inn.png",
    "travel.mp3": "audio/v4/friend-context-v4.mp3",
    "search.mp3": "audio/v5/search-scene-v5.mp3",
    "meeting.mp3": "audio/v4/serious-context-v4.mp3",
    "font-license.txt": "art/ui/Galmuri-OFL.txt",
}
for icon in ("evidence", "save", "menu", "back", "present", "investigate", "record"):
    FILES[f"{icon}.png"] = f"art/icons/{icon}.png"

def main():
    TARGET.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, relative in FILES.items():
        src, dest = SOURCE / relative, TARGET / name
        shutil.copyfile(src, dest)
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        assert digest == hashlib.sha256(dest.read_bytes()).hexdigest()
        manifest[name] = {"source": relative, "sha256": digest}
    # Font format conversion only; all PNGs and MP3s remain byte-for-byte copies.
    font = TTFont(SOURCE / "art/ui/galmuri11.woff2")
    font.flavor = None
    font.save(TARGET / "Galmuri11.ttf")
    (TARGET / "provenance.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"Prepared {len(FILES)} existing assets and the licensed Korean font.")

if __name__ == "__main__":
    main()
