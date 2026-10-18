"""Final exact two-source overlay; no schedule/placement changes."""
import copy,json,hashlib,argparse
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
KEY='assets/room13-pixel-acting.json'
RECEIPT='art/investigation-source2-20261018/receipt.json'
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=True,separators=(',',':')).encode()).hexdigest()
def receipt(root=ROOT):
 r=json.loads((root/RECEIPT).read_text());assert [o['pointer'] for o in r['operations']]==['/resident_ttadak/living_doorframe','/resident_tosil/living_thermos'];return r

def restore(registries,root=ROOT,require_applied=False):
 out=copy.deepcopy(registries)
 if KEY not in out:return out
 for o in receipt(root)['operations']:
  person,pose=o['pointer'].strip('/').split('/');spec=out[KEY][person][pose]
  assert spec==o['value'] or (not require_applied and spec==o['expected']),o['pointer']
  out[KEY][person][pose]=copy.deepcopy(o['expected'])
 return out

def run(root=ROOT,apply=False):
 r=receipt(root);path=root/'game'/KEY;doc=json.loads(path.read_text());before=restore({KEY:doc},root,require_applied=not apply)[KEY]
 assert digest(before)==r['baseline_acting_semantic_sha256']
 for a in r['assets']:
  src=root/a['source'];exp=root/a['export'];assert hashlib.sha256(src.read_bytes()).hexdigest()==a['source_sha256'];assert hashlib.sha256(exp.read_bytes()).hexdigest()==a['export_sha256']
  x=Image.open(src).convert('RGBA');y=Image.open(exp).convert('RGBA');assert x.size==y.size and x.tobytes()==y.tobytes()
 for o in r['operations']:
  assert {k:v for k,v in o['expected'].items() if k not in ('file','crop','foot','head','source_sha256','reviewed','native_detail')}=={k:v for k,v in o['value'].items() if k not in ('file','crop','foot','head','source_sha256','reviewed','native_detail')}
  person,pose=o['pointer'].strip('/').split('/');before[person][pose]=o['value']
 assert digest(before)==r['expected_final_acting_semantic_sha256']
 if apply:path.write_text(json.dumps(before,ensure_ascii=False,indent=2)+'\n')
 return 2
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--apply',action='store_true');a=p.parse_args();print(run(a.root,a.apply))
