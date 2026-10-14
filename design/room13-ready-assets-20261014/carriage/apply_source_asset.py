"""Apply the exact reviewed carriage PNG to a Room13 source tree without editing code."""
import argparse, hashlib, json, re, shutil
from pathlib import Path
NAME='room13-pixel-carriage-letter0153-morning.png'
OLD='14cdd63697a88e34a63370d035354910401459d574f93bab4da6fd2c3b01e9e1'
NEW='9ce6389a6b1d6575dac7922d690669b9b9b1843df854ab15db3c4044d3a63f9e'
p=argparse.ArgumentParser();p.add_argument('project',type=Path,help='Path to experiments/renpy-ch1');p.add_argument('--dry-run',action='store_true');a=p.parse_args()
root=a.project.resolve(); assert (root/'prepare_assets.py').is_file(),'Not a Room13 project'
asset=Path(__file__).resolve().parent/'source-overlay/experiments/renpy-ch1/art/pixel-b'/NAME
data=asset.read_bytes();assert hashlib.sha256(data).hexdigest()==NEW
provenance=root/'game/assets/provenance.json';raw=provenance.read_text();m=json.loads(raw);assert m[NAME]['sha256'] in (OLD,NEW),'Source asset changed since patch was prepared'
if m[NAME]['sha256']==OLD:
 pattern=r'("'+re.escape(NAME)+r'"\s*:\s*\{[^}]*?"sha256"\s*:\s*")'+OLD+r'(")'
 new,count=re.subn(pattern,lambda m:m[1]+NEW+m[2],raw);assert count==1
else:new=raw
paths=[root/'art/pixel-b'/NAME,root/'game/assets'/NAME]
for target in paths:
 if target.exists():assert hashlib.sha256(target.read_bytes()).hexdigest() in (OLD,NEW),'Refusing to replace independently modified image: '+str(target)
# All preconditions are checked before any write. Missing PNGs in text-only
# handoffs are expected and are supplied by this patch.
if not a.dry_run:
 for target in paths:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 if new!=raw:provenance.write_text(new)
 for target in paths:assert hashlib.sha256(target.read_bytes()).hexdigest()==NEW
 assert json.loads(provenance.read_text())[NAME]['sha256']==NEW
print(json.dumps({'dry_run':a.dry_run,'asset_sha256':NEW,'asset_bytes':len(data),'paths':[str(x) for x in paths],'metadata':str(provenance),'code_changed':False},indent=2))
