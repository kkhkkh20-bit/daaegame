"""Fit the approved forty-person masters to existing dialogue profiles.

No new art, pose alignment, or story inference. Preserve canvas and bottom
anchor; sample the master directly at the final half-resolution, then repeat
each pixel twice. The runtime also snaps after profile scaling.
"""
import argparse, hashlib, json
from pathlib import Path
from PIL import Image
from import_smooth20_sources import ALIASES as FIRST_ALIASES
from import_smooth_next20_sources import ALIASES as NEXT_ALIASES
ALIASES = dict(FIRST_ALIASES, **NEXT_ALIASES)

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'docs/reviews/dialogue-beats'
SLOTS = ('neutral','joy','angry','anxious','surprise_talk','surprise_react')

def read(path): return json.loads(path.read_text())
def write(path, data): path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def sources(folder):
    rows = {}
    for name in ('smooth20-receipt','smooth-next20-receipt'):
        for row in read(REVIEW/(name+'.json'))['records']:
            person=ALIASES.get(row['character'],row['character'])
            rows[person,row['slot']] = (folder/row['runtime_file'],row['sha256'])
    for name in ('smooth-fifth10-receipt','smooth-final9-receipt'):
        for row in read(REVIEW/(name+'.json'))['neutral_replacements']:
            person=ALIASES.get(row['character_id'],row['character_id'])
            if (person,'neutral') in rows:
                rows[person,'neutral']=(folder/'highres'/row['source_relative_path'],row['sha256'])
    assert len(rows)==240
    for path,expected in rows.values():
        if not path.is_file() or sha(path)!=expected:raise ValueError('Missing/unverified master: '+str(path))
    return rows

def main(folder, selected=None):
    masters=sources(Path(folder));registry=ROOT/'game/assets/room13-dialogue-talk-art.json'
    data=read(registry);receipts=[]
    for (person,slot),(source,expected) in masters.items():
        if selected and person not in selected:continue
        image=Image.open(source).convert('RGBA')
        for height,profile in data['people'][person]['profiles'].items():
            frame=profile['frames'][slot];target=ROOT/'game'/frame['file']
            with Image.open(target) as old: w,h=old.size
            # Keep the original frame box. An odd remainder remains transparent
            # above the sampled image, so the original bottom edge is unchanged.
            small=image.resize((max(1,w//2),max(1,h//2)),Image.Resampling.NEAREST)
            fitted=small.resize((small.width*2,small.height*2),Image.Resampling.NEAREST)
            result=Image.new('RGBA',(w,h));result.paste(fitted,(0,h-fitted.height))
            result.save(target,format='WEBP',lossless=True,method=6,exact=True)
            decoded=Image.open(target).convert('RGBA')
            block=decoded.crop((0,h-fitted.height,fitted.width,h))
            assert block.resize(small.size,Image.Resampling.NEAREST).resize(block.size,Image.Resampling.NEAREST).tobytes()==block.tobytes()
            profile['pixel_grid']=2
            frame.update(source_sha256=expected,source_master=str(source.relative_to(Path(folder))),pixel_filter='nearest-final-grid2')
            receipts.append(dict(person=person,slot=slot,height=int(height),source_sha256=expected,
                source_size=list(image.size),file=frame['file'],file_size=[w,h],offset=frame['offset'],
                canvas=profile['canvas'],grid=2,bottom_anchor_preserved=True))
    write(registry,data)
    out=REVIEW/'expression-fit-20261020';out.mkdir(exist_ok=True)
    write(out/'grid2-receipt.json',dict(base='70e9488d7faf000f52325fda0a793c5fb7338492',
        verified_master_slots=len(masters),selected_people=sorted(set(x['person'] for x in receipts)),
        profiles=receipts,policy='master -> half final display size -> nearest 2x; no per-pose bbox alignment'))
    print('Verified master slots:',len(masters),'converted display frames:',len(receipts))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder');p.add_argument('--people',nargs='*');a=p.parse_args();main(a.folder,set(a.people) if a.people else None)
