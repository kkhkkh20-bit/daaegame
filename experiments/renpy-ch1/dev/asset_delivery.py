"""납품 명세 사전 검사. 게임 파일은 수정하지 않는다."""
import argparse,json
from pathlib import Path
from PIL import Image
from asset_modules import inventory,PROJECT

def validate(manifest,folder,project=PROJECT):
 rows=inventory(project);slots={(r['role'],r['state']):r for r in rows};errors=[];seen=set();plan=[]
 for i,item in enumerate(manifest.get('items',[])):
  key=(item.get('role'),item.get('state'));prefix=f'{i+1}: {key}'
  if key in seen:errors.append(prefix+' 중복 슬롯');continue
  seen.add(key)
  if key not in slots:errors.append(prefix+' 등록되지 않은 슬롯');continue
  slot=slots[key]
  if item.get('baseline_sha256')!=slot['sha256']:errors.append(prefix+' 게임 원본이 바뀌었습니다. 최신 명세로 대조하세요.');continue
  name=item.get('file','');path=(folder/name).resolve()
  if not name or not path.is_relative_to(folder.resolve()) or not path.is_file():errors.append(prefix+' 납품 파일 없음/경로 오류');continue
  try:
   with Image.open(path) as im:
    im.load();size=list(im.size)
    if im.format not in ('PNG','WEBP'):raise ValueError('PNG 또는 WebP 필요')
    if item.get('size')!=size:raise ValueError('명세와 실제 크기가 다름')
  except Exception as e:errors.append(prefix+' '+str(e));continue
  if slot['module']=='대사 얼굴' and slot['state']=='neutral':errors.append(prefix+' 의도적 중립 얼굴 공백: 별도 승인 필요');continue
  plan.append(dict(role=key[0],state=key[1],file=name,previous=slot['path'],size=size,needs_geometry_review=slot['module']=='전신 표정' or size!=slot['size']))
 if not manifest.get('items'):errors.append('납품 항목이 없습니다.')
 return dict(valid=not errors,errors=errors,plan=plan,note='사전 검사 결과입니다. 게임 적용·화면 검증·배포 완료가 아닙니다.')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('manifest',type=Path);p.add_argument('--folder',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
 report=validate(json.loads(a.manifest.read_text()),a.folder or a.manifest.parent)
 text=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
 if a.output:a.output.write_text(text)
 print(text,end='');raise SystemExit(0 if report['valid'] else 1)
