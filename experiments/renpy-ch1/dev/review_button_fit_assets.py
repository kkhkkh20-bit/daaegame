"""제작자 manifest와 별개로 요청 CSV·픽셀·SVG·기존 파일을 대조한다."""
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile

from PIL import Image

PROJECT=Path(__file__).resolve().parents[1]
ROOT=PROJECT.parents[1]


def check():
    art=ROOT/'design/generated-ui-button-fit'
    assets=PROJECT/'game/assets/ui-button-fit'
    manifest=json.loads((art/'manifest.json').read_text())
    entries={row['filename']:row for row in manifest['assets']}
    with ZipFile(ROOT/'design/requests/pending-ui-buttons-20261025.zip') as archive:
        specs=list(csv.DictReader(io.StringIO(archive.read(
            'pending-ui-buttons-20261025/asset_specs.csv').decode('utf-8-sig'))))
    assert len(specs)==len(entries)==20
    assert {p.name for p in assets.glob('*.png')}==set(entries)
    masks={};alphas={};report=[]
    for row in specs:
        name=row['filename'];entry=entries[name];source=assets/name
        size=[int(row['canvas_width']),int(row['canvas_height'])]
        crop=[int(row[k]) for k in ('art_x','art_y','art_width','art_height')]
        x,y,w,h=crop;sw,sh=int(row['safe_width']),int(row['safe_height'])
        safe=[x+(w-sw)//2,y+(h-sh)//2,sw,sh]
        with Image.open(source) as image:
            assert image.mode=='RGBA' and list(image.size)==size,name
            alpha=image.getchannel('A')
            bbox=list(alpha.getbbox())
            assert bbox==[x,y,x+w,y+h],(name,bbox)
            assert alpha.crop((safe[0],safe[1],safe[0]+sw,safe[1]+sh)).getextrema()[0]>0,name
            mask=bytes(v>0 for v in alpha.tobytes())
            family=name.removesuffix('_'+row['state']+'.png')
            values=alpha.tobytes()
            if row['state']=='disabled':
                # 45% 알파에서 가장자리 1/255 픽셀이 0으로 양자화될 수 있다.
                assert max(abs(b-round(a*.45)) for a,b in zip(alphas[family],values))<=1,name
            else:
                if family in masks:assert mask==masks[family],name
                masks[family]=mask
                if row['state']=='basic':alphas[family]=values
        assert entry['canvas']==size and entry['art_rect']==crop and entry['safe_rect']==safe,name
        assert entry['alpha_bbox']==bbox and entry['display_scale']==1,name
        assert entry['sha256']==hashlib.sha256(source.read_bytes()).hexdigest(),name
        assert entry['text_in_image'] is False and entry['icons_in_image'] is False,name
        assert max(abs(v) for v in entry['pressed_visual_offset'])<=2,name
        assert max(abs(v) for v in entry['runtime_content_offset'])<=2,name
        svg=ET.parse(art/entry['svg'])
        forbidden={'text','textPath','tspan','image','foreignObject','use'}
        assert not any(node.tag.rsplit('}',1)[-1] in forbidden for node in svg.iter()),name
        report.append(dict(file=name,canvas=size,crop=crop,alpha_bbox=bbox,safe=safe))
    original=json.loads((PROJECT/'docs/reviews/button-fit-review/original-sha256.json').read_text())
    changed=[name for name,digest in original.items()
             if not (PROJECT/name).is_file() or hashlib.sha256((PROJECT/name).read_bytes()).hexdigest()!=digest]
    assert not changed,changed
    result=dict(status='PASSED',files=report,unchanged_original_files=len(original),
                equal_alpha_support_families=len(masks),
                note='SVG에 문자/래스터 삽입 없음. 아이콘 부재와 재질 유사성은 실제 미리보기로 별도 확인.')
    output=PROJECT/'docs/reviews/button-fit-review/asset-check.json'
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('납품 20파일/5계열 검사 통과; 기존 파일 %d개 SHA-256 불변'%len(original))


if __name__=='__main__':check()
