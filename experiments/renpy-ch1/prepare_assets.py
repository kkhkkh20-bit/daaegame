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

# The original 35-person cast contains seven identities already represented by
# the approved chapter-one cast. Preserve those designs; only revive the others.
LEGACY_EXISTING = {"nabi", "buri", "doto", "grandma", "karo", "bami", "wanggu"}
LEGACY_NEW_PAIR = ("librarian", "teacher")

def prepare_legacy_residents(cast, manifest):
    """Register lightweight original animal-pixel drafts without rewriting PNGs."""
    specifications = json.loads((REPO / "design/character-specs.json").read_text())
    report = {"status": "lightweight-design-drafts", "original_count": 35,
              "approved_existing_cast_preserved": sorted(LEGACY_EXISTING),
              "pixel_policy": "Immutable source PNGs; runtime alpha-bound crops and nearest-neighbor rendering.",
              "residents": []}
    for original in specifications["characters"]:
        old_id = original["id"]
        if old_id in LEGACY_EXISTING or old_id in LEGACY_NEW_PAIR:
            continue
        person = "resident_" + old_id
        entry = {}
        details = {"id": person, "original_id": old_id, "name": original["name"],
                   "animal": original["animal"], "design_stage": "restored-original-pixel-draft"}
        for kind, source_relative in (("body", "art/body/" + old_id + "-0.png"),
                                      ("face", "art/faces/" + old_id + "-neutral.png")):
            source = REPO / source_relative
            assert source.is_file(), source
            name = person + "-" + kind + ".png"
            destination = TARGET / name
            shutil.copyfile(source, destination)
            im = Image.open(source)
            assert im.mode == "RGBA", source
            alpha = im.getchannel("A")
            # Original portraits contain shoulders. Their upper three quarters
            # retain the full ears/hat/beak while keeping the dialogue face large.
            inspection = alpha if kind == "body" else alpha.crop((0, 0, im.width, round(im.height * .75)))
            bounds = inspection.point(lambda a: 255 if a > 20 else 0).getbbox()
            assert bounds is not None, (person, kind)
            geometry = {"file": "assets/" + name,
                        "crop": [bounds[0], bounds[1], bounds[2] - bounds[0], bounds[3] - bounds[1]]}
            details[kind] = {"source": source_relative, "size": list(im.size), **geometry}
            for state in ("neutral", "thinking", "distressed", "expressive"):
                if kind == "body":
                    entry[state] = geometry
                    entry["interview_" + state] = geometry
                else:
                    entry["avatar_" + state] = geometry
            if kind == "body":
                entry["world"] = geometry
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            assert digest == hashlib.sha256(destination.read_bytes()).hexdigest()
            manifest[name] = {"source": source_relative, "sha256": digest,
                "approval": "User requested lightweight drafts of the original 35 residents. Existing approved chapter-one cast is preserved.",
                "adaptation": "Original animal pixel PNG copied byte-for-byte; runtime Crop only. One neutral pose reused for world/interview; expression names alias that pose, not newly generated expressions.",
                "design_stage": "lightweight-original-draft"}
        cast[person] = entry
        report["residents"].append(details)
    # These two original roster members had no full-body pixel originals.
    # Keep the new, reference-guided pair immutable too: both paws and shoes
    # are visible and separated by a wide transparent gap.
    pair = ROOT / "art/resident-librarian-teacher.png"
    shutil.copyfile(pair, TARGET / pair.name)
    pair_im = Image.open(pair)
    assert pair_im.mode == "RGBA", pair
    pair_alpha = pair_im.getchannel("A")
    assert pair_alpha.getpixel((0, 0)) == 0
    for column, old_id in enumerate(LEGACY_NEW_PAIR):
        left, right = round(pair_im.width * column / 2), round(pair_im.width * (column + 1) / 2)
        bounds = pair_alpha.crop((left, 0, right, pair_im.height)).point(lambda a: 255 if a > 20 else 0).getbbox()
        assert bounds and bounds[0] > 3 and bounds[1] > 3 and bounds[2] < right-left-3 and bounds[3] < pair_im.height-3
        x, y, width, height = left + bounds[0], bounds[1], bounds[2] - bounds[0], bounds[3] - bounds[1]
        body = {"file": "assets/" + pair.name, "crop": [x, y, width, height]}
        head = pair_alpha.crop((x, y, x + width, y + round(height * .4))).point(lambda a: 255 if a > 20 else 0).getbbox()
        assert head, old_id
        face = {"file": "assets/" + pair.name,
                "crop": [x + head[0], y + head[1], head[2] - head[0], head[3] - head[1]]}
        entry = {"world": body}
        for state in ("neutral", "thinking", "distressed", "expressive"):
            entry[state] = body
            entry["interview_" + state] = body
            entry["avatar_" + state] = face
        person = "resident_" + old_id
        cast[person] = entry
        original = next(c for c in specifications["characters"] if c["id"] == old_id)
        report["residents"].append({"id": person, "original_id": old_id, "name": original["name"],
            "animal": original["animal"], "design_stage": "new-reference-guided-pixel-draft",
            "body": {"source": "experiments/renpy-ch1/art/" + pair.name, "size": list(pair_im.size), **body},
            "face": {"source": "experiments/renpy-ch1/art/" + pair.name, "size": list(pair_im.size), **face}})
    manifest[pair.name] = {"source": "experiments/renpy-ch1/art/" + pair.name,
        "generation": "Reference-guided image_gen, 2026-10-12; two new full-body animal pixel design drafts.",
        "approval": "User requested lightweight original-roster resident designs. Original approved chapter-one characters remain unchanged.",
        "adaptation": "Immutable transparent pair; runtime body/head Crop only. One neutral pose per resident, shared by world/interview and expression aliases.",
        "sha256": hashlib.sha256(pair.read_bytes()).hexdigest()}
    assert len(report["residents"]) == 28
    return report

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
                     "map-plaza-fountain.png","map-signpost.png","map-bench.png","village-map.png"):
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
                 "outdoor-gate.png","outdoor-gate-morning.png","outdoor-fountain.png","outdoor-lane.png","outdoor-post.png","outdoor-inn.png","village-overview.png"):
        src=ROOT/"art"/name
        shutil.copyfile(src,TARGET/name)
        manifest[name]={"source":"experiments/renpy-ch1/art/"+name,"generation":"User-requested reference-guided image_gen, 2026-10-11","sha256":hashlib.sha256(src.read_bytes()).hexdigest()}
    for name in ("town-bright.mp3","town-credits.txt"):
        src=ROOT/"audio"/name
        shutil.copyfile(src,TARGET/name)
        manifest[name]={"source":"experiments/renpy-ch1/audio/"+name,"composition":"Original 116 BPM C major arrangement; licensed FluidR3 recorded instruments; compose_town.py","sha256":hashlib.sha256(src.read_bytes()).hexdigest()}
    # New recurring residents have a front interview and a separate work pose.
    # Immutable generated sheet; only runtime Crop metadata is produced here.
    future=ROOT/"art"/"future-villagers-v3.png"
    shutil.copyfile(future,TARGET/future.name)
    future_image=Image.open(future)
    assert future_image.mode=="RGBA" and future_image.size==(1536,1024)
    future_alpha=future_image.getchannel("A")
    assert future_alpha.getpixel((0,0))<=3 and future_alpha.getpixel((1535,1023))<=3
    solid=future_alpha.point(lambda a:255 if a>20 else 0)
    gaps=[y for y in range(450,551) if solid.crop((0,y,1536,y+1)).getbbox() is None]
    assert gaps,"Interview and activity rows must have a transparent separating gap"
    row_edges=(0,gaps[len(gaps)//2],1024)
    for column,person in enumerate(("elder","bodum","workshop")):
        entry={}
        bounds=[]
        for row in range(2):
            x,y=column*512,row_edges[row]
            height=row_edges[row+1]-y
            region=future_alpha.crop((x,y,x+512,y+height))
            bbox=region.point(lambda a:255 if a>20 else 0).getbbox()
            assert bbox and bbox[0]>3 and bbox[1]>3 and bbox[2]<509 and bbox[3]<height-3,(person,row,bbox)
            bounds.append([x+bbox[0],y+bbox[1],bbox[2]-bbox[0],bbox[3]-bbox[1]])
        normal=dict(file="assets/"+future.name,crop=bounds[0])
        entry["world"]=dict(file="assets/"+future.name,crop=bounds[1])
        x,y,w,h=bounds[0]
        head_h=round(h*(.48 if person=="workshop" else .34))
        head=future_alpha.crop((x,y,x+w,y+head_h)).point(lambda a:255 if a>20 else 0).getbbox()
        assert head,(person,"head")
        avatar=dict(file="assets/"+future.name,crop=[x+head[0],y+head[1],head[2]-head[0],head[3]-head[1]])
        for state in ("neutral","thinking","distressed","expressive"):
            entry[state]=normal
            entry["interview_"+state]=normal
            entry["avatar_"+state]=avatar
        cast[person]=entry
    manifest[future.name]={"source":"experiments/renpy-ch1/art/"+future.name,
        "approval":"User requested more outdoor characters from future episodes; original approved cast is preserved.",
        "generation":"image_gen new recurring cast and reference-guided sprite layout, 2026-10-12; one interview expression and one separate activity pose per resident.",
        "sha256":hashlib.sha256(future.read_bytes()).hexdigest()}
    resident_report = prepare_legacy_residents(cast, manifest)
    activity_source=ROOT/"art"/"village-activities.png"
    shutil.copyfile(activity_source,TARGET/activity_source.name)
    activity_image=Image.open(activity_source)
    assert activity_image.mode=="RGBA" and activity_image.size==(1536,1024)
    for index,person in enumerate(("resident_tori","resident_piko","resident_momo","resident_tok")):
        x,y=(index%2)*768,(index//2)*512
        region=activity_image.getchannel("A").crop((x,y,x+768,y+512))
        bbox=region.point(lambda a:255 if a>20 else 0).getbbox()
        assert bbox and bbox[0]>3 and bbox[1]>3 and bbox[2]<765 and bbox[3]<509,(person,bbox)
        cast[person]["activity"]=dict(file="assets/"+activity_source.name,crop=[x+bbox[0],y+bbox[1],bbox[2]-bbox[0],bbox[3]-bbox[1]])
    manifest[activity_source.name]={"source":"experiments/renpy-ch1/art/"+activity_source.name,
        "generation":"image_gen, reference-guided activity poses, 2026-10-12",
        "sha256":hashlib.sha256(activity_source.read_bytes()).hexdigest()}
    inn_source=ROOT/"art"/"inn-activities.png"
    shutil.copyfile(inn_source,TARGET/inn_source.name)
    inn_image=Image.open(inn_source)
    assert inn_image.mode=="RGBA"
    half=inn_image.width//2
    for index,person in enumerate(("granny","resident_nubi")):
        x=index*half
        region=inn_image.getchannel("A").crop((x,0,x+half,inn_image.height))
        bbox=region.point(lambda a:255 if a>20 else 0).getbbox()
        assert bbox and bbox[0]>3 and bbox[1]>3 and bbox[2]<half-3 and bbox[3]<inn_image.height-3,(person,bbox)
        cast[person]["inn_activity"]=dict(file="assets/"+inn_source.name,crop=[x+bbox[0],bbox[1],bbox[2]-bbox[0],bbox[3]-bbox[1]])
    for name in ("inn-activities.png","inn-lounge.png","winter-gate.webp"):
        src=ROOT/"art"/name
        shutil.copyfile(src,TARGET/name)
        manifest[name]={"source":"experiments/renpy-ch1/art/"+name,
            "generation":("image_gen winter checkpoint, 2026-10-12; WebP delivery encoding" if name=="winter-gate.webp" else "image_gen reference-guided inn activity and adjoining dusk lounge, 2026-10-12"),
            "sha256":hashlib.sha256(src.read_bytes()).hexdigest()}
    # New checkpoint guard: separate working body, front body and face geometry.
    guard=ROOT/"art"/"winter-guard.webp"
    guard_image=Image.open(guard)
    half=guard_image.width//2
    bounds=[]
    for col in range(2):
        bbox=guard_image.getchannel("A").crop((col*half,0,(col+1)*half,guard_image.height)).point(lambda a:255 if a>20 else 0).getbbox()
        assert bbox and bbox[0]>3 and bbox[2]<half-3
        bounds.append([col*half+bbox[0],bbox[1],bbox[2]-bbox[0],bbox[3]-bbox[1]])
    front=dict(file="assets/winter-guard.webp",crop=bounds[1])
    x,y,w,h=bounds[1]
    head=dict(file="assets/winter-guard.webp",crop=[x+round(w*.13),y,round(w*.74),round(h*.36)])
    cast["guard"]={"world":dict(file="assets/winter-guard.webp",crop=bounds[0])}
    for state in ("neutral","thinking","distressed","expressive"):
        cast["guard"][state]=front
        cast["guard"]["interview_"+state]=front
        cast["guard"]["avatar_"+state]=head
    for name in ("winter-guard.webp","winter-places.webp"):
        src=ROOT/"art"/name
        shutil.copyfile(src,TARGET/name)
        manifest[name]={"source":"experiments/renpy-ch1/art/"+name,"generation":"image_gen, 2026-10-12; immutable source PNG retained, WebP delivery, runtime Crop geometry only", "sha256":hashlib.sha256(src.read_bytes()).hexdigest()}
    (TARGET / "resident-art.json").write_text(json.dumps(resident_report, ensure_ascii=False, indent=2))
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
