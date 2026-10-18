"""Second diagnostic overlay: 47 exact selected actual pose specs, one flag each."""
import copy,json,hashlib,argparse
from pathlib import Path
from investigation_job_overlay import restore as restore_jobs
ROOT=Path(__file__).resolve().parents[1]
RECEIPT='art/investigation-native-residual-20261018/receipt.json'
def slot(doc,p):
 parts=p.strip('/').split('/');n=doc
 for k in parts[:-1]:n=n[int(k)] if isinstance(n,list) else n[k]
 return n,int(parts[-1]) if isinstance(n,list) else parts[-1]
def receipt(root=ROOT):
 r=json.loads((root/RECEIPT).read_text());assert len(r['operations'])==47
 for o in r['operations']:assert o['value']==dict(o['expected'],native_detail=True) and not o['expected'].get('native_detail')
 return r

def restore(registries,root=ROOT,require_applied=False):
 out=restore_jobs(registries,root)
 for o in receipt(root)['operations']:
  if o['file'] not in out:continue
  n,k=slot(out[o['file']],o['pointer'])
  assert n[k]==o['value'] or (not require_applied and n[k]==o['expected']),o['pointer']
  n[k]=copy.deepcopy(o['expected'])
 return out

def run(root=ROOT,apply=False):
 r=receipt(root);docs={p:json.loads((root/'game'/p).read_text()) for p in r['baseline_semantic_sha256']}
 old=restore(docs,root,require_applied=not apply)
 for f,h in r["source_export_hashes"].items():assert hashlib.sha256((root/"game"/f).read_bytes()).hexdigest()==h,f
 for p,d in old.items():assert hashlib.sha256(json.dumps(d,sort_keys=True,ensure_ascii=True,separators=(',',':')).encode()).hexdigest()==r['baseline_semantic_sha256'][p],p
 if apply:
  for o in r['operations']:
   n,k=slot(docs[o['file']],o['pointer']);n[k]=o['value']
  for p,d in docs.items():(root/'game'/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 return 47
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--apply',action='store_true');a=p.parse_args();print(run(a.root,a.apply))
