"""Import only the explicitly approved front-threequarter original; no mirror or regenerated art."""
import json,hashlib,shutil
from pathlib import Path
from PIL import Image
from map27_pixel_derivative import derive_map_image,validate_map_image
ROOT=Path(__file__).resolve().parents[1]
def main():
 src=Path('/workspace/seori-v2');m=json.loads((src/'manifest.json').read_text())[0];b=(src/m['file']).read_bytes();assert hashlib.sha256(b).hexdigest()==m['sha256']=='761b7930193aecdce0ab86fb8788ebf6e900171d229678b7d5fee8d1fcc11155'
 im=Image.open(src/m['file']).convert('RGBA');assert list(im.size)==m['size']==[1037,1516]
 folder=ROOT/'art/approved-seori-threequarter-v2';folder.mkdir(exist_ok=True);(folder/'source-original.png').write_bytes(b);shutil.copyfile(src/'manifest.json',folder/'manifest.json')
 out,t=derive_map_image(im);validate_map_image(out);file='assets/map-action27/seori-threequarter-review.webp';out.save(ROOT/'game'/file,lossless=True,method=6,exact=True)
 sx,sy=t['source_to_export'];anchors={k:[v[0]*sx,v[1]*sy] for k,v in m['anchors_source_px'].items()};head=[v*(sx if i%2==0 else sy) for i,v in enumerate(m['head_box_source_xywh'])]
 spec=dict(file=file,crop=[0,0,out.width,768],foot=anchors['foot'],anchors=anchors,head=head,contact='self-contained',facing=m['facing'],nearest=True,source_sha256=m['sha256'],source_commit='12479638c1964c20325192a4514254329c9bd4fb')
 (ROOT/'game/assets/room13-seori-review-art.json').write_text(json.dumps(dict(person='resident_seori',pose='inspect_paper_threequarter_front',spec=spec),ensure_ascii=False,indent=2)+'\n')
 (folder/'receipt.json').write_text(json.dumps(dict(source_commit=spec['source_commit'],archive_bytes=876491,archive_sha256='64bcce7face6dd0f82b19bdbd115804fcb07aa2329a007837def62546bcc9f2f',source_bytes=len(b),source_sha256=m['sha256'],source_size=m['size'],export=file,export_sha256=hashlib.sha256((ROOT/'game'/file).read_bytes()).hexdigest(),transform=t),indent=2)+'\n')
if __name__=='__main__':main()
