"""Stage3: preserve stage1 alias specs, append two conditional workshop job rows."""
import copy,json,hashlib,argparse
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
RECEIPT='art/investigation-jobs-20261018/receipt.json'
KEY='assets/room13-map-action27.json'
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=True,separators=(',',':')).encode()).hexdigest()
def receipt(root=ROOT):
 r=json.loads((root/RECEIPT).read_text());assert {x['request_id'] for x in r['rows']}=={'JOB-CHORONG-STONE','JOB-MUSOE-OLD-TOOL'} and len(r['rows'])==2
 assert all(x['location']=='workshop' for x in r['rows']);return r

def restore(registries,root=ROOT,require_applied=False):
 out=copy.deepcopy(registries)
 if KEY not in out:return out
 r=receipt(root);rows=out[KEY]['rows'];ids={x['request_id'] for x in r['rows']};found=[x for x in rows if x['request_id'] in ids]
 if found:
  assert rows[-2:]==r['rows'] and found==r['rows'],'Unexpected job rows or order'
  out[KEY]['rows']=rows[:-2]
 else:assert not require_applied,'Missing job rows'
 return out

def run(root=ROOT,apply=False):
 r=receipt(root);p=root/'game'/KEY;doc=json.loads(p.read_text());before=restore({KEY:doc},root,require_applied=not apply)[KEY]
 assert digest(before)==r['baseline_map_semantic_sha256'],'Stage3 requires exact stage1+stage2 baseline'
 for a in r['assets']:
  src=root/a['source'];exp=root/a['export']
  assert hashlib.sha256(src.read_bytes()).hexdigest()==a['source_sha256']
  assert hashlib.sha256(exp.read_bytes()).hexdigest()==a['export_sha256']
  x=Image.open(src).convert('RGBA');y=Image.open(exp).convert('RGBA');assert x.size==y.size and x.tobytes()==y.tobytes()
 if apply:
  before['rows']+=r['rows'];p.write_text(json.dumps(before,ensure_ascii=False,indent=2)+'\n')
 return 2
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--apply',action='store_true');a=p.parse_args();print(run(a.root,a.apply))
