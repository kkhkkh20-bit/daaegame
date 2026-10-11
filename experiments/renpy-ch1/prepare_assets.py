"""Copy originals plus the two explicitly requested Ren'Py art revisions."""
from pathlib import Path
import hashlib
import json
import shutil
from source_sounds import render as render_source_sounds, render_typing
from fontTools.ttLib import TTFont
from PIL import Image

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
SOURCE = REPO / "preview/ch1-gpt-20261008"
TARGET = ROOT / "game/assets"

FILES = {
    "carriage.png": "art/ch1/cinematics/carriage-family-close.png",
    "approach.png": "art/ch1/cinematics/village-approach-road.png",
    "driver.png": "art/ch1/cinematics/carriage-driver-close.png",
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
    "table.png": "art/council/council-table-foreground-v1.png",
    "map.png": "art/worldmap/world-backdrop-autumn-v3-512x288.png",
    "chest.png": "art/ch1/locations/chest_closed_world.png",
    "chest-open.png": "art/ch1/locations/chest_open_with_ledger.png",
    "notebook.png": "art/ch1/props/doto_room/prop_weather_notebook_open_rgba.png",
    "clock-base.png": "art/ch1/closeup/wall-clock-base-512.png",
    "clock-hands.png": "art/ch1/closeup/wall-clock-exact-overlay-512.png",
    "seal.png": "art/ch1/closeup/I1-seal-strip-complete-512.png",
    "fur-stamp.png": "art/ch1/closeup/dormouse-flank-exact-overlay-512.png",
    "somsom-hidden-source.png": "art/ch1/discovery/somsom-held.png",
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
    (TARGET / "fur-base.png").unlink(missing_ok=True) # Obsolete golden-fur test copy.
    for obsolete in ("post-office.png","inn-door.png","map-inn.png","map-post-office.png",
                     "map-plaza-fountain.png","map-signpost.png","map-bench.png"):
        (TARGET/obsolete).unlink(missing_ok=True) # Source originals remain in the HTML art library.
    manifest = {}
    for name, relative in FILES.items():
        src, dest = SOURCE / relative, TARGET / name
        shutil.copyfile(src, dest)
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        assert digest == hashlib.sha256(dest.read_bytes()).hexdigest()
        manifest[name] = {"source": relative, "sha256": digest}
    for name, revision in {"pouch.png":"pouch-no-hand.png", "somsom.png":"somsom-gentle.png", "driver.png":"driver-autumn.png"}.items():
        src = ROOT / "art" / revision
        shutil.copyfile(src, TARGET / name)
        manifest[name] = {"source":"experiments/renpy-ch1/art/"+revision,
            "original":FILES[name], "approval":"User explicitly requested this RenPy image revision; original public art is preserved.",
            "generation":"image_gen reference-image edit, 2026-10-11", "sha256":hashlib.sha256(src.read_bytes()).hexdigest()}
    cast = {}
    head_height={"det1":.88,"det0":.88,"innma":.70,"seryeon":.65,
                 "nabi":.84,"geokkuri":1.0,"doto":.95,"buri":.74,"karo":.83,"wanggu":.77}
    aliases = {"det1": "daram", "det0": "dad", "innma": "granny", "geokkuri": "bami", "wanggu": "neoul"}
    for atlas in ("family", "inn", "friends", "scholars", "witnesses"):
        alpha=Image.open(SOURCE/f"art/ch1/dialogue-v2/{atlas}.png").getchannel("A")
        metadata = json.loads((SOURCE / f"art/ch1/dialogue-v2/{atlas}.meta.json").read_text())
        for original, states in metadata["characters"].items():
            entry = {state: {"file": f"assets/{atlas}.png", "crop": spec["crop"]} for state, spec in states.items()}
            for state, spec in states.items():
                if "face" in spec:
                    x,y,size=spec["face"]
                    # The source's square face boxes include torsos; retain only the head.
                    # Alpha inspection derives runtime geometry, without rewriting any PNG.
                    height=round(size*head_height[original])
                    bbox=alpha.crop((x,y,x+size,y+height)).point(lambda a:255 if a>20 else 0).getbbox()
                    assert bbox is not None,(atlas,original,state)
                    entry["avatar_"+state]={"file":f"assets/{atlas}.png",
                        "crop":[x+bbox[0],y+bbox[1],bbox[2]-bbox[0],bbox[3]-bbox[1]]}
            if original in metadata.get("world", {}):
                entry["world"] = {"file": f"assets/{atlas}.png", "crop": metadata["world"][original]["crop"]}
            cast[aliases.get(original, original)] = entry
    rows={"family":("daram","dad",512),"inn":("granny","seryeon",512),
          "friends":("nabi","bami",565),"scholars":("doto","buri",550),
          "witnesses":("karo","neoul",528)}
    for atlas,(top,bottom,split) in rows.items():
        src=ROOT/"art"/("interview-"+atlas+".png")
        dest=TARGET/src.name
        shutil.copyfile(src,dest)
        im=Image.open(src)
        assert im.size==(1536,1024) and im.mode=="RGBA"
        assert im.getpixel((0,0))[3]==0, "Sprite background must be transparent"
        for person,y,height in [(top,0,split),(bottom,split,1024-split)]:
            for col,state in enumerate(("neutral","thinking","distressed","expressive")):
                cast[person]["interview_"+state]={"file":"assets/"+src.name,"crop":[col*384,y,384,height]}
        manifest[src.name]={"source":"experiments/renpy-ch1/art/"+src.name,
            "approval":"User requested complete front-facing interview sprites for all ten characters.",
            "generation":"Reference-guided image_gen, 2026-10-11; immutable PNG, runtime crops only.","sha256":hashlib.sha256(src.read_bytes()).hexdigest()}
    for name in ("village-stone.png","chest-complete.png","hidden-somsom.png","inn-map.png",
                 "outdoor-gate.png","outdoor-gate-morning.png","outdoor-fountain.png","outdoor-lane.png","outdoor-post.png","outdoor-inn.png","village-map.png"):
        src=ROOT/"art"/name
        shutil.copyfile(src,TARGET/name)
        manifest[name]={"source":"experiments/renpy-ch1/art/"+name,"generation":"User-requested reference-guided image_gen, 2026-10-11","sha256":hashlib.sha256(src.read_bytes()).hexdigest()}
    for name in ("town-bright.mp3","town-credits.txt"):
        src=ROOT/"audio"/name
        shutil.copyfile(src,TARGET/name)
        manifest[name]={"source":"experiments/renpy-ch1/audio/"+name,"composition":"Original 116 BPM C major arrangement; licensed FluidR3 recorded instruments; compose_town.py","sha256":hashlib.sha256(src.read_bytes()).hexdigest()}
    (TARGET / "cast.json").write_text(json.dumps(cast, ensure_ascii=False, indent=2))
    source = json.loads((ROOT / 'game/chapter-source.json').read_text())
    assert source['sha256'] == hashlib.sha256((REPO/source['source']).read_bytes()).hexdigest(), 'Chapter source changed; refresh the captured source data before building.'
    paths = {v['src'] for v in source['episode']['BGS'].values() if v.get('src')}
    paths.update(v['media'] for v in source['music'].values() if v.get('media'))
    paths.update('art/ch1/cinematics/'+name for name in
                 ('carriage-driver-close.png','village-arrival-wide.png'))
    paths.update(packet['img'] for packet in source['episode']['COLD'])
    paths.add('audio/v3/sfx/wood-door-close.wav')
    source_map={}
    existing={relative:name for name,relative in FILES.items() if name!="somsom-hidden-source.png"}
    for generated in TARGET.glob('source-*'):
        generated.unlink()
    for relative in sorted(paths):
        if relative==source['episode']['BGS']['plaza']['src']:
            source_map[relative]='assets/outdoor-gate-morning.png'
            continue
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
    for dest in TARGET.glob("cold-heart-*.wav"):
        manifest[dest.name]={"source":"experiments/renpy-ch1/source_sounds.py","composition":"Original bounded heartbeat pulse, 55-130 BPM","sha256":hashlib.sha256(dest.read_bytes()).hexdigest()}
    render_typing(TARGET / "type.wav")
    manifest["type.wav"] = {"source":"experiments/renpy-ch1/source_sounds.py",
        "adaptation":"Original deterministic soft text tick; four gently varied 30 ms taps per loop, peak bounded to 0.22; no external samples."}
    # Font format conversion; unchanged assets retain their original hashes.
    font = TTFont(SOURCE / "art/ui/galmuri11.woff2")
    font.flavor = None
    font.save(TARGET / "Galmuri11.ttf")
    (TARGET / "provenance.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"Prepared {len(FILES)} existing assets and the licensed Korean font.")

if __name__ == "__main__":
    main()
