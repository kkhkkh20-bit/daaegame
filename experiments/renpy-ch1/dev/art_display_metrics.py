"""Measure source bytes and calculate current dialogue geometry, without changing pixels.

These are engine-coordinate calculations, not measured browser/CSS screenshots.
"""
import csv
import io
import json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT/'game'
OUT=ROOT/'docs/art-coverage'


def build():
    fb=json.loads((GAME/'assets/room13-fullbody-dialogue.json').read_text())['people']
    coverage=json.loads((OUT/'coverage.json').read_text())
    refs={r['character']:r['canonical_reference'] for r in coverage['items'] if r['kind']=='dialogue_expression' and r['requirement']=='neutral'}
    rows=[]
    for person,entry in sorted(fb.items()):
        image=entry['images']['neutral'];file=image['file']
        with Image.open(GAME/file) as im:runtime_size=list(im.size)
        ref=refs.get(person) or {};source=ROOT/ref.get('path','')
        source_size=None
        if source.is_file() and source.suffix.lower() in ('.png','.webp','.jpg'):
            with Image.open(source) as im:source_size=list(im.size)
        for height in (840,760,560):
            scale=height*1.05*{'bami':.88,'doto':.92}.get(person,1)/max(1,entry['figure'][3])
            cap=(880.0 if height>=800 else 400.0)/max(1,entry['crop'][2])
            pixel=entry.get('pixel')
            if pixel:
                unit=float(pixel['u'])*pixel['cell'];k=max(1,int(round(scale*unit)))
                while k>1 and k/unit>cap:k-=1
                scale=k/unit
            else:scale=min(scale,cap)
            mapped=bool(image.get('map'))
            u=image['map'][0] if mapped else 1.0
            iw,ih=image.get('crop',entry['crop'])[2:]
            width,height_native=(iw*scale*u,ih*scale*u) if mapped else (entry['crop'][2]*scale,entry['crop'][3]*scale)
            pixel_path=mapped and image.get('cell')
            if pixel_path:
                drawn=[max(1,int(round(width))),max(1,int(round(height_native)))];grid=None;sample=None
            else:
                grid=3
                sample=[max(1,int(round(width))//grid),max(1,int(round(height_native))//grid)]
                drawn=[v*grid for v in sample]
            rows.append(dict(character=person,dialogue_height=height,approved_reference=ref.get('path'),source_size=source_size,
                source_cell_px=2 if person in ('guard','buri','resident_solbang','resident_guldol') else None,
                source_cell_note='approved 2x2 source' if person in ('guard','buri','resident_solbang','resident_guldol') else 'not declared by source; do not infer from renderer grid',
                runtime_file=file,runtime_size=runtime_size,runtime_cell_px=image.get('cell'),reference_map_u=u,
                scale_in_reference_coordinates=scale,runtime_pixel_scale=scale*u,frame_size=[max(1,int(round(entry['crop'][2]*scale))),max(1,int(round(entry['crop'][3]*scale)))],
                final_drawn_picture_size=drawn,renderer_grid_px=grid,intermediate_sample_size=sample,
                screen_px_per_declared_cell=scale*u*image['cell'] if image.get('cell') else None,
                measurement_type='calculated_engine_pixels_not_browser_capture',
                limitations='neutral only; pose fit=1; preview override disabled; body may extend behind dialogue; CSS/device pixel scaling and screenshot compression not measured'))
    return rows


def main():
    rows=build();(OUT/'display-metrics.json').write_text(json.dumps({'basis':'game/room13_fullbody_dialogue.rpy + room13_acting.rpy; current code formula','rows':rows},ensure_ascii=False,indent=2)+'\n')
    s=io.StringIO();w=csv.DictWriter(s,fieldnames=list(rows[0]));w.writeheader()
    for row in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in row.items()})
    (OUT/'display-metrics.csv').write_text(s.getvalue(),encoding='utf-8-sig')
    print(json.dumps(next(r for r in rows if r['character']=='resident_teacher' and r['dialogue_height']==760),ensure_ascii=False,indent=2))


if __name__=='__main__':main()
