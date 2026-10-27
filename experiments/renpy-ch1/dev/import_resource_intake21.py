"""Import verified approved art into exact existing dialogue contexts only.

Input: safely extracted resource-intake ZIPs from art/resource-intake-20261021.
Original bytes remain in that immutable Git commit; never replace general slots.
"""
import ast
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from PIL import Image
from line_cues import scene_rows, _match_bracket

ROOT = Path(__file__).resolve().parents[1]
COMMIT = 'ae62bf081fce0e08eebbbf2dcd8896292175bd56'
BATCH = 'resource-intake-20261021'
DARAM_IDS = [
 ('01_bravado', 'MS14_D01_S01_L0013'),
 ('02_reproach_lean', 'MS14_D03_S02_L0007'),
 ('03_stubborn', 'MS14_D01_S04_L0006'),
 ('04_flustered', 'MS14_D01_S03_L0005'),
 ('05_playful_evasion', 'MS14_D02_S03_L0018'),
 ('06_eureka', 'MS14_D03_S03_L0020'),
 ('07_delighted', 'MS14_D03_S06_L0003'),
 ('08_scared_brave', 'MS14_D03_S04_L0003'),
 ('09_wipe_tears', 'MS14_D03_S06_L0018'),
 ('10_resolve', 'MS14_D02_S04_L0027'),
]
# These legacy scenes already contain these speakers and conditions. No new route.
OTHER_SCENES = [
 ('kkomi_anxious', 'kid_kkomi', 'wf:hideout:refuse', 1),
 ('kkomi_joy', 'kid_kkomi', 'st:kkomi_class', 1),
 ('dodam_joy', 'kid_dodam', 'st:dodam', 3),
 ('saemi_anxious', 'kid_saemi', 'ws:soup:all', 0),
 ('ubak_anxious', 'resident_ubak', 'ep1:ubak', 3),
]

def read(path): return json.loads(path.read_text())
def write(path, value):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def box(im): return im.convert('RGBA').getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox()

def v111_bindings():
 source=(ROOT/'game/room13_v111_days123.rpy').read_text()
 records=read(ROOT/'game/v111/records.json')['records'];found={}
 for m in re.finditer(r'call r13_lines\(',source):
  start=m.end()-1;end=_match_bracket(source,start)
  call=ast.parse('f'+source[start:end+1],mode='eval').body
  first=call.args[0]
  # 2026-10-27 R09: 다시 읽을 때 비우는 조건식([] if … else r13_v111_lines([...]))은 호출 쪽 가지를 읽는다.
  if isinstance(first,ast.IfExp):first=first.orelse if isinstance(first.orelse,ast.Call) else first.body
  # 0.19.89: the day files call r13_v111_lines([...]) (new-world text layer).
  if isinstance(first,ast.Call) and getattr(first.func,'id',None)=='r13_v111_lines':ids=ast.literal_eval(first.args[0])
  elif isinstance(first,ast.ListComp):ids=ast.literal_eval(first.generators[0].iter)
  else:continue
  identity=ast.literal_eval(call.args[1])
  for i,rid in enumerate(ids):
   r=records[rid]
   found[rid]=dict(identity=identity,index=i,text=r['text'],line_id=rid,
                   source='game/room13_v111_days123.rpy',source_line=source[:m.start()].count('\n')+1)
 return found

def reviewed_bindings():
 v=v111_bindings();rows=scene_rows();cues=[]
 for slot,rid in DARAM_IDS:
  cues.append(dict(v[rid],person='daram',slot='intake21_'+slot))
 for asset,person,identity,index in OTHER_SCENES:
  if identity=='ws:soup:all':
   # Literal prefix of the existing conditional call; appended Daram packet
   # never changes this first Saemi packet or its surrounding branch.
   s=(ROOT/'game/systems/room13_ep5_soup.rpy').read_text()
   start=s.index('call r13_lines([("kid_saemi","일어나.')+len('call r13_lines(')
   packet=ast.literal_eval(s[start:_match_bracket(s,start)+1])[index]
  else:packet=rows[identity][index]
  assert packet[0]==person
  cues.append(dict(person=person,slot='intake21_'+asset,identity=identity,index=index,text=packet[1]))
 cues.append(dict(v['MS14_D03_S03_L0023'],person='resident_ubak',slot='intake21_ubak_angry'))
 for cue in cues:cue.update(key=cue['person']+':'+cue['slot'],batch=BATCH)
 return cues

def main(folder):
 folder=Path(folder)
 for name,digest in [('dialogue-icons-8.zip','63a23ba25e3c75502c5804df763b2e7d78ae39eff7f856c7eb4476fcfe406feb'),('other-expressions-6.zip','6c6d285ad88b5e5df7732fd79afa77c8ea51563fbb296abe97b804a3b21a4c5f'),('daram-approved-10.zip','f6c3e2d6e6ddcc632253ea15f6a4e7de2532a71107d52846c41224fcef53eb30')]:
  assert sha(folder/name)==digest,name
 daram=folder/'daram-approved-10/daram-acting10-approved-20261020';other=folder/'other-expressions-6'
 dm=read(daram/'manifest.json');om=read(other/'manifest.json');sources={}
 for r in dm['assets']:
  sources['intake21_'+r['key']]=(daram/r['source'],r['source_sha256'],r['source'])
 for r in om['items']:
  name=r['id']+'.png'
  assert sha(other/'pixel2x_candidates'/name)==r['sha256']
  with zipfile.ZipFile(folder/'other-expressions-6.zip') as z:
   member=next(n for n in z.namelist() if n.endswith('masters/'+name))
   digest=hashlib.sha256(z.read(member)).hexdigest()
  sources['intake21_'+r['id']]=(other/'masters'/name,digest,'masters/'+name)
 for path,digest,_ in sources.values():assert sha(path)==digest,path
 base=read(ROOT/'game/assets/room13-dialogue-talk-art.json')['people']
 target=ROOT/'game/assets/room13-dialogue-context-art.json';data=read(target)
 cues=reviewed_bindings();reference=Image.open(sources['intake21_01_bravado'][0]).convert('RGBA');reference_box=box(reference)
 receipt=dict(source_commit=COMMIT,source_directory='design/'+BATCH,bindings=cues,profiles=[],held_icons=read(folder/'dialogue-icons-8/manifest.json'),limits=['Icon evidence IDs D06/D11/D12 absent from current runtime records; not registered.','Other-expression production_manifest_audit.json not delivered: exact existing contexts reviewed here instead.','No new SDK build or deployment; runtime source-overlay QA only.'])
 for cue in cues:
  person,slot=cue['person'],cue['slot'];path,digest,original=sources[slot]
  im=Image.open(path).convert('RGBA');bb=box(im);profiles={}
  for h,p in base[person]['profiles'].items():
   f=p['frames']['neutral'];old=Image.open(ROOT/'game'/f['file']);ob=box(old)
   ref=reference_box if person=='daram' else bb
   scale=(ob[3]-ob[1])/float(ref[3]-ref[1])
   # Shared source canvas/scale preserves all ten poses' relative size.
   if person=='daram':
    padded=Image.new('RGBA',tuple(dm['source_canvas']));padded.paste(im,(0,0));im_for_size=padded
   else:im_for_size=im
   size=tuple(round(v*scale) for v in im_for_size.size)
   new=im_for_size.resize(size,Image.Resampling.LANCZOS)
   nb=box(new);centre=f['offset'][0]+(ob[0]+ob[2])/2.;foot=f['offset'][1]+ob[3]
   offset=[round(centre-(nb[0]+nb[2])/2.),foot-nb[3]]
   assert 0<=offset[0]+nb[0]<offset[0]+nb[2]<=p['canvas'][0],(slot,h,'width',nb,offset,p['canvas'])
   assert 0<=offset[1]+nb[1]<offset[1]+nb[3]<=p['canvas'][1],(slot,h,'height')
   dest=ROOT/'game/assets/dialogue-context-master'/person/h/(slot+'.webp');dest.parent.mkdir(parents=True,exist_ok=True)
   new.save(dest,format='WEBP',lossless=True,method=4)
   frame=dict(file=dest.relative_to(ROOT/'game').as_posix(),offset=offset,source_master=original,source_sha256=digest,source_commit=COMMIT)
   profiles[h]=dict(canvas=p['canvas'],pixel_grid=2,frames={slot:frame})
   receipt['profiles'].append(dict(person=person,slot=slot,height=h,canvas=p['canvas'],image_size=list(size),visible_box=list(nb),offset=offset,scale=scale,foot=foot,output_sha256=sha(dest)))
  data['entries'][cue['key']]=dict(person=person,slot=slot,profiles=profiles,status='approved_runtime',batch=BATCH)
 data['bindings']=[c for c in data['bindings'] if c.get('batch')!=BATCH]+cues
 assert len({(c['identity'],c['index'],c['person'],c['text']) for c in data['bindings']})==len(data['bindings'])
 write(target,data);write(ROOT/'docs/reviews'/BATCH/'receipt.json',receipt)
 print('Verified 3 ZIPs and 16 source hashes; connected 16 contexts / 48 profiles; 8 icons held.')
if __name__=='__main__':main(sys.argv[1])
