"""Copy existing approved assets without modifying image/audio originals."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
from source_sounds import render as render_source_sounds
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
    "basket-world.png": "art/ch1/locations/C04_basket_world.png",
    "front.png": "art/ch1/bg/BG01_reception_panorama.png",
    "kitchen.png": "art/ch1/locations/BG03_kitchen_base.png",
    "hall.png": "art/ch1/bg/BG_corridor_2f_pixel_v1.png",
    "doto-room.png": "art/ch1/bg/BG_doto_room_pixel_v1.png",
    "post-office.png": "art/ch1/cinematics/post-office-closed-exterior.png",
    "inn-door.png": "art/ch1/cinematics/inn-entrance-evening.png",
    "table.png": "art/council/council-table-foreground-v1.png",
    "map.png": "art/worldmap/world-backdrop-autumn-v3-512x288.png",
    "chest.png": "art/ch1/locations/chest_closed_world.png",
    "chest-open.png": "art/ch1/locations/chest_open_with_ledger.png",
    "notebook.png": "art/ch1/props/doto_room/prop_weather_notebook_open_rgba.png",
    "clock-base.png": "art/ch1/closeup/wall-clock-base-512.png",
    "clock-hands.png": "art/ch1/closeup/wall-clock-exact-overlay-512.png",
    "seal.png": "art/ch1/closeup/I1-seal-strip-complete-512.png",
    "fur-stamp.png": "art/ch1/closeup/dormouse-flank-exact-overlay-512.png",
    "contract.png": "art/ch1/closeup/I1-contract-front-complete-512.png",
    "family.png": "art/ch1/dialogue-v2/family.png",
    "inn.png": "art/ch1/dialogue-v2/inn.png",
    "friends.png": "art/ch1/dialogue-v2/friends.png",
    "scholars.png": "art/ch1/dialogue-v2/scholars.png",
    "witnesses.png": "art/ch1/dialogue-v2/witnesses.png",
    "travel.mp3": "audio/v4/friend-context-v4.mp3",
    "search.mp3": "audio/v5/search-scene-v5.mp3",
    "meeting.mp3": "audio/v3/meeting-strings-v3.mp3",
    "pressure.mp3": "audio/v3/climax-press-strings-v3.mp3",
    "night.mp3": "audio/v5/night-scene-v5.mp3",
    "after.mp3": "audio/v3/after-strings-v3.mp3",
    "comic.mp3": "audio/v4/comic-context-v4.mp3",
    "door.wav": "audio/v3/sfx/wood-door-open.wav",
    "sound-credits.txt": "audio/v3/sfx/SFX_CREDITS.txt",
    "music-credits.txt": "audio/v3/CREDITS.txt",
    "music-v4-credits.txt": "audio/v4/CREDITS.txt",
    "music-v5-credits.txt": "audio/v5/CREDITS.txt",
    "sample-license.txt": "audio/v2/FLUIDR3-LICENSE.txt",
    "font-license.txt": "art/ui/Galmuri-OFL.txt",
}
for icon in ("evidence", "save", "menu", "back", "present", "investigate", "record", "move", "talk", "press", "sound-on", "sound-off", "lock", "notebook"):
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
    cast = {}
    aliases = {"det1": "daram", "det0": "dad", "innma": "granny", "geokkuri": "bami", "wanggu": "neoul"}
    for atlas in ("family", "inn", "friends", "scholars", "witnesses"):
        metadata = json.loads((SOURCE / f"art/ch1/dialogue-v2/{atlas}.meta.json").read_text())
        for original, states in metadata["characters"].items():
            entry = {state: {"file": f"assets/{atlas}.png", "crop": spec["crop"]} for state, spec in states.items()}
            if original in metadata.get("world", {}):
                entry["world"] = {"file": f"assets/{atlas}.png", "crop": metadata["world"][original]["crop"]}
            cast[aliases.get(original, original)] = entry
    (TARGET / "cast.json").write_text(json.dumps(cast, ensure_ascii=False, indent=2))
    source = json.loads((ROOT / 'game/chapter-source.json').read_text())
    assert source['sha256'] == hashlib.sha256((REPO/source['source']).read_bytes()).hexdigest(), 'Chapter source changed; refresh the captured source data before building.'
    paths = {v['src'] for v in source['episode']['BGS'].values() if v.get('src')}
    paths.update(v['media'] for v in source['music'].values() if v.get('media'))
    paths.update('art/ch1/cinematics/'+name for name in
                 ('carriage-driver-close.png','village-arrival-wide.png'))
    paths.add('audio/v3/sfx/wood-door-close.wav')
    source_map={}
    existing={relative:name for name,relative in FILES.items()}
    for generated in TARGET.glob('source-*'):
        generated.unlink()
    for relative in sorted(paths):
        if relative in existing:
            source_map[relative]='assets/'+existing[relative]
            continue
        src=SOURCE/relative
        if not src.is_file():
            raise FileNotFoundError(src)
        name='source-'+src.name
        dest=TARGET/name
        shutil.copyfile(src,dest)
        digest=hashlib.sha256(src.read_bytes()).hexdigest()
        assert digest==hashlib.sha256(dest.read_bytes()).hexdigest()
        source_map[relative]='assets/'+name
        manifest[name]={'source':relative,'sha256':digest}
    (TARGET/'source-map.json').write_text(json.dumps(source_map,ensure_ascii=False,indent=2))
    render_source_sounds(TARGET)
    for dest in TARGET.glob('source-*.wav'):
        if dest.name not in manifest:
            manifest[dest.name]={'source':'dev/wip-v2/inn_audio.js',
                'adaptation':'Offline procedural PCM reconstruction; same cue, bounded gain. Not a recording or byte-identical WebAudio output.',
                'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
    # A quiet wooden text tick, adapted from our attributed door recording.
    # No live speech synthesis or replacement of the music originals.
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.12", "-t", "0.032", "-i",
                    str(SOURCE / "audio/v3/sfx/wood-door-close.wav"), "-af",
                    "highpass=f=700,lowpass=f=2600,afade=t=in:d=0.004,afade=t=out:st=0.016:d=0.016,volume=0.3,apad=whole_dur=0.095",
                    "-t", "0.095", str(TARGET / "type.wav")], check=True)
    manifest["type.wav"] = {"source": "audio/v3/sfx/wood-door-close.wav", "adaptation": "32 ms wooden excerpt; bandpass, fades, gain and 95 ms loop padding; CC BY 3.0 bennstir"}
    # Font format conversion only; all PNGs and MP3s remain byte-for-byte copies.
    font = TTFont(SOURCE / "art/ui/galmuri11.woff2")
    font.flavor = None
    font.save(TARGET / "Galmuri11.ttf")
    (TARGET / "provenance.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"Prepared {len(FILES)} existing assets and the licensed Korean font.")

if __name__ == "__main__":
    main()
