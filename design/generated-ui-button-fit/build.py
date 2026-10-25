#!/usr/bin/env python3
"""새 SVG 도형 원본에서 exact-canvas PNG 20장을 렌더한다. 참고 PNG는 읽거나 변형하지 않는다."""
from pathlib import Path
from zipfile import ZipFile
import csv, io, json, hashlib, subprocess, random, sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
GAME=ROOT/'experiments/renpy-ch1/game/assets/ui-button-fit'
archive=ROOT/'design/requests/pending-ui-buttons-20261025.zip'
with ZipFile(archive) as z:
    specs=list(csv.DictReader(io.StringIO(z.read('pending-ui-buttons-20261025/asset_specs.csv').decode('utf-8-sig'))))
    originals={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if '/approved-originals/' in n and n.endswith('.png')}
def paper_path(x,y,w,h,r):
    # Uneven hand-drawn paper contour; shared exact geometry across every state.
    return (f'M{x+r:.2f},{y+.20:.2f} '
      f'C{x+w*.28:.2f},{y+.52:.2f} {x+w*.35:.2f},{y:.2f} {x+w*.48:.2f},{y+.18:.2f} '
      f'S{x+w*.76:.2f},{y+.64:.2f} {x+w-r:.2f},{y+.16:.2f} '
      f'Q{x+w-.15:.2f},{y+.30:.2f} {x+w-.20:.2f},{y+r:.2f} '
      f'C{x+w:.2f},{y+h*.34:.2f} {x+w-.62:.2f},{y+h*.64:.2f} {x+w-.24:.2f},{y+h-r:.2f} '
      f'Q{x+w-.20:.2f},{y+h-.20:.2f} {x+w-r:.2f},{y+h-.18:.2f} '
      f'C{x+w*.72:.2f},{y+h-.55:.2f} {x+w*.48:.2f},{y+h:.2f} {x+w*.34:.2f},{y+h-.24:.2f} '
      f'S{x+w*.21:.2f},{y+h-.61:.2f} {x+r:.2f},{y+h-.18:.2f} '
      f'Q{x+.20:.2f},{y+h-.20:.2f} {x+.22:.2f},{y+h-r:.2f} '
      f'C{x+.60:.2f},{y+h*.64:.2f} {x:.2f},{y+h*.35:.2f} {x+.18:.2f},{y+r:.2f} '
      f'Q{x+.20:.2f},{y+.15:.2f} {x+r:.2f},{y+.20:.2f} Z')
rows=[]
for spec in specs:
    name=spec['filename'];state=spec['state'];family=name.removesuffix('_'+state+'.png')
    w,h,aw,ah,sw,sh=[int(spec[k]) for k in ['canvas_width','canvas_height','art_width','art_height','safe_width','safe_height']]
    primary='_primary' in name
    edge='#683d2b' if primary else '#805534'
    top,bottom=('#d64a42','#c43c36') if primary else ('#fcf0dc','#f4e3c7')
    if state=='pressed':top,bottom=('#bf3833','#cd443b') if primary else ('#ebd7b9','#f5e4c9')
    outline='#b83c36' if state=='selected' else edge
    opacity=.45 if state=='disabled' else 1
    r=9 if family.startswith('square') else 8
    # Opaque silhouette ends exactly at x/y 8 and x/y 8+art extent.
    # Every family/state shares this same silhouette, with no shifted drop shadow.
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="paper" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient>
<clipPath id="paperClip"><rect x="11" y="11" width="{aw-6}" height="{ah-6}" rx="{r-3}"/></clipPath></defs>
<g opacity="{opacity}">
<path d="{paper_path(8,8,aw,ah,r)}" fill="{outline}"/>
<path d="{paper_path(10,10,aw-4,ah-4,r-2)}" fill="url(#paper)"/>
'''
    # Thin warm inner edge is part of the paper, never an external selected ring.
    svg+=f'<path d="{paper_path(11.1,10.8,aw-6.2,ah-5.7,r-3)}" fill="none" stroke="{"#ed9680" if primary else "#c79d6d"}" stroke-width=".85" opacity=".65"/>\n'
    if state=='selected':
        svg+=f'<path d="{paper_path(10.8,10.8,aw-5.6,ah-5.6,r-2.8)}" fill="none" stroke="{"#fff2dd" if primary else edge}" stroke-width=".9" opacity=".9"/>\n'
    if state=='pressed':
        svg+=f'<path d="M {8+r} 11 L {8+aw-r} 11" stroke="{edge}" stroke-width="1.6" opacity=".28"/>\n'
    else:
        svg+=f'<path d="M {8+r} 10.4 L {8+aw-r} 10.4" stroke="{"#ffd6b1" if primary else "#fff9ed"}" stroke-width=".8" opacity=".5"/>\n'
    # Sparse deterministic vector fibres keep the safe area quiet and legible.
    rng=random.Random(1325+w+h)
    svg+='<g clip-path="url(#paperClip)" opacity=".16">\n'
    for _ in range(aw*ah//20):
        x=11+rng.random()*(aw-6);y=11+rng.random()*(ah-6)
        svg+=f'<path d="M{x:.2f} {y:.2f}h{rng.uniform(.3,1.1):.2f}" stroke="{"#f4a489" if primary else "#ba9467"}" stroke-width=".45"/>\n'
    svg+='</g></g></svg>\n'
    source=OUT/(Path(name).stem+'.svg');source.write_text(svg)
    target=GAME/name
    if '--validate-existing' not in sys.argv:subprocess.run(['inkscape',str(source),'--export-type=png','--export-filename='+str(target)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    with Image.open(target) as im:
        assert im.mode=='RGBA',(name,im.mode)
        bbox=list(im.getchannel('A').getbbox());expected=[8,8,8+aw,8+ah]
        assert bbox==expected,(name,bbox,expected)
        assert im.size==(w,h)
    rows.append(dict(filename=name,family=family,state=state,canvas=[w,h],art_rect=[8,8,aw,ah],alpha_bbox=bbox,safe_rect=[8+(aw-sw)//2,8+(ah-sh)//2,sw,sh],display_size=[aw,ah],display_scale=1,pressed_visual_offset=[0,0],runtime_content_offset=[0,2] if state=='pressed' else [0,0],sha256=hashlib.sha256(target.read_bytes()).hexdigest(),svg=source.name,text_in_image=False,icons_in_image=False))
for family in sorted({row['family'] for row in rows}):
    group=[r for r in rows if r['family']==family]
    masks=[]
    for row in group:
        with Image.open(GAME/row['filename']) as im:masks.append(bytes(v>0 for v in im.getchannel('A').getdata()))
    assert len(set(masks[:3]))==1,family
    basic=list(Image.open(GAME/group[0]['filename']).getchannel('A').getdata())
    disabled=list(Image.open(GAME/group[3]['filename']).getchannel('A').getdata())
    assert max(abs(a*.45-b) for a,b in zip(basic,disabled))<=1,family
manifest=dict(version=1,description='승인된 크림/빨강 종이 버튼을 참고해 새로 그린 크기별 SVG 원본. 기존 래스터 재가공 없음.',source_request=str(archive.relative_to(ROOT)),renderer='Inkscape SVG native-size PNG',state_priority=['disabled','pressed','selected','basic'],reference_original_sha256=originals,assets=rows,qa=dict(files=20,canvas_and_alpha_bbox='passed',identical_active_alpha_support_per_family='passed',disabled_alpha_ratio_045_tolerance_1='passed',identical_svg_outer_contour_per_family='passed',no_raster_resizing=True),preview='preview-1280x720.png',preview_kind='합성 제작 검토판; 실제 게임 캡처 아님')
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
# New comparison board: references are embedded unchanged; no source screenshot edits.
svg='<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1280" height="720"><rect width="1280" height="720" fill="#f7f1e5"/><g font-family="sans-serif" fill="#493426"><text x="36" y="44" font-size="26" font-weight="bold">다람탐정 · 규격별 버튼 20종 제작 검토판</text><text x="36" y="72" font-size="16">새 SVG 원본 · 실제 표시 크기 · 글자/아이콘 없음 · 게임 적용 전 합성 미리보기</text>'
labels=['기본','누름','선택','비활성'];families=['square_standard','main_primary','main_standard','topic_primary','topic_standard']
for j,label in enumerate(labels):svg+=f'<text x="{400+j*238}" y="118" text-anchor="middle" font-size="18">{label}</text>'
for i,family in enumerate(families):
    y=144+i*104
    svg+=f'<text x="36" y="{y+38}" font-size="19">{family}</text>'
    group=[r for r in rows if r['family']==family]
    svg+=f'<text x="36" y="{y+62}" font-size="15">종이 {group[0]["art_rect"][2]} × {group[0]["art_rect"][3]} / 배율 1:1</text>'
    for j,row in enumerate(group):
        w,h=row['canvas'];x=400+j*238-w/2
        svg+=f'<rect x="{280+j*238}" y="{y-4}" width="230" height="92" rx="8" fill="#e6dfd2"/><image x="{x}" y="{y+(80-h)/2}" width="{w}" height="{h}" xlink:href="{GAME/row["filename"]}"/>'
svg+='<text x="36" y="697" font-size="16">모든 상태: 바깥 여백 8px · 외곽 중심 고정 · 누름은 내부 음영만 변경 · 비활성 알파 45%</text></g></svg>'
(OUT/'preview-1280x720.svg').write_text(svg)
subprocess.run(['inkscape',str(OUT/'preview-1280x720.svg'),'--export-type=png','--export-filename='+str(OUT/'preview-1280x720.png')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print('20 PNG / 20 SVG / manifest / 1280x720 검토판 생성; 규격 및 상태외곽 검사 통과')
