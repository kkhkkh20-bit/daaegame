"""Exact canonical investigation overlay. Run after the legacy importer.
No resampling, recoloring, schedule, position, or height changes are performed.
"""
import argparse, copy, hashlib, io, json
from pathlib import Path
from PIL import Image
from investigation_native_residual import restore as restore_residual
ROOT=Path(__file__).resolve().parents[1]
RECEIPT='art/investigation-canonical-20261018/receipt.json'
JOB_ROWS={'VA-9-square','VA-9-hall','VA-10-square','VA-10-hall','VA-11-post','VA-12-post','VA-2','VA-3'}
FAMILY={('/'+p+'/'+s) for p in ('resident_musoe','resident_lamplighter') for s in ('neutral','thinking','distressed','expressive')}
FAMILY|={'/resident_musoe/living_foldmap','/resident_lamplighter/living_inspectlamp'}
def sha(data):return hashlib.sha256(data).hexdigest()
def slot(doc,pointer):
 parts=pointer.strip('/').split('/');node=doc
 for k in parts[:-1]:node=node[int(k)] if isinstance(node,list) else node[k]
 return node,int(parts[-1]) if isinstance(node,list) else parts[-1]
def receipt(root=ROOT):
 r=json.loads((root/RECEIPT).read_text())
 assert len(r['assets'])==14 and len(r['operations'])==18
 assert len({a['destination'] for a in r['assets']})==14
 assert {o['match']['request_id'] for o in r['operations'] if 'match' in o}==JOB_ROWS
 assert {o['pointer'] for o in r['operations'] if 'match' not in o}==FAMILY
 return r

def restored_registries(registries, r):
 """Verify exact new specs, then reverse ONLY this overlay for legacy scope tests."""
 out=restore_residual(registries)
 for o in r['operations']:
  path=o['file'].removeprefix('game/');node,k=slot(out[path],o['pointer'])
  assert node[k]==o['value'], 'Noncanonical overlay spec: '+o['pointer']
  node[k]=copy.deepcopy(o['expected'])
 return out

def run(root=ROOT, apply=False):
 r=receipt(root);docs={f:json.loads((root/f).read_text()) for f in {o['file'] for o in r['operations']}};exports=[]
 baseline={('game/'+p):v for p,v in restore_residual({p.removeprefix('game/'):v for p,v in docs.items()},root).items()}
 for o in r['operations']:
  node,k=slot(baseline[o['file']],o['pointer'])
  assert node[k] in (o['expected'],o['value']), 'Unexpected spec/order: '+o['pointer']
  node[k]=copy.deepcopy(o['expected'])
 for path,expected in r['baseline_semantic_sha256'].items():
  assert sha(json.dumps(baseline[path],sort_keys=True,ensure_ascii=True,separators=(',',':')).encode())==expected, 'Unexpected complete registry baseline: '+path

 for a in r['assets']:
  raw=(root/a['portable_source']).read_bytes();assert sha(raw)==a['source_png_sha256']
  original=Image.open(io.BytesIO(raw)).convert('RGBA');x,y,w,h=a['spec']['crop']
  assert 0<=x<x+w<=original.width and 0<=y<y+h<=original.height
  assert a['spec']['source_sha256']==a['source_png_sha256']
  # Stored approved output is always hash-pinned. Local encoder bytes are not portable.
  data=(root/a['destination']).read_bytes()
  assert sha(data)==a['webp_sha256'], 'Stored approved export differs: '+a['destination']
  exported=Image.open(io.BytesIO(data)).convert('RGBA')
  assert exported.size==original.size and exported.tobytes()==original.tobytes()
  if apply:
   buf=io.BytesIO();original.save(buf,'WEBP',lossless=True,exact=True)
   regenerated=Image.open(io.BytesIO(buf.getvalue())).convert('RGBA')
   assert regenerated.size==original.size and regenerated.tobytes()==original.tobytes()
   # Do not replace approved stored bytes with encoder-version-dependent bytes.
  exports.append((root/a['destination'],data))
 for o in r['operations']:
  node,k=slot(docs[o['file']],o['pointer'])
  if 'match' in o:
   row=docs[o['file']]['rows'][int(o['pointer'].split('/')[2])]
   assert all(row[key]==value for key,value in o['match'].items())
  if apply:
   assert node[k] in (o['expected'],o['value']), 'Unexpected pre-overlay spec: '+o['pointer']
   node[k]=copy.deepcopy(o['value'])
  else:assert node[k]==o['value'],o['pointer']
 if apply:
  for path,data in exports:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
  for path,doc in docs.items():(root/path).write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
 return {'assets':14,'bindings':18,'job_rows':8,'runtime_reviewed':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--apply',action='store_true');a=p.parse_args();print(run(a.root,a.apply))
