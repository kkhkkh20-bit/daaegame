"""Produce a local handoff only. Never writes Git, remotes, or a PR."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parents[1]
def blob(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
files=[]
for top in ('game','dev','docs'):
 for p in sorted((R/top).rglob('*')):
  if not p.is_file() or '__pycache__' in p.parts or p.suffix=='.pyc' or p.name=='draw_piko_contact.py' or 'piko-native-v3' in p.parts:continue
  rel=p.relative_to(R).as_posix(); data=p.read_bytes()
  old=R/'base-game'/p.relative_to(R/'game') if top=='game' else None
  files.append(dict(path=rel,size=len(data),sha256=hashlib.sha256(data).hexdigest(),git_blob=blob(data),base_git_blob=blob(old.read_bytes()) if old and old.exists() else None))
manifest=dict(base_commit='24ce3b6037093a562f0bd9b1c35c64a9b690a13d',native_test_status='NOT RUN',deployment_status='LOCAL ONLY; remote creation approval pending',excluded=['base-game','art/piko-contact (obsolete broad-lamp proposal)','dev/draw_piko_contact.py (obsolete proposal generator)','__pycache__'],files=files)
(R/'DELIVERY_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(R/'recommended-story-local-bundle.zip','w',zipfile.ZIP_DEFLATED) as z:
 for item in files:z.write(R/item['path'],item['path'])
 z.write(R/'DELIVERY_MANIFEST.json','DELIVERY_MANIFEST.json')
 for name in ('integrated-source-tests.log','staging-integrated-tests.log'):
  if (R/name).exists():z.write(R/name,name)
print('Local bundle:',len(files),'files; native and deployment remain unverified.')
