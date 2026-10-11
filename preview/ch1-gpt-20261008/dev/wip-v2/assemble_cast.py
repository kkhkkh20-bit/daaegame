"""Assemble reviewed cast metadata; inspect original PNGs without editing them.

Actual generated spacing is authoritative. Dialogue frames use a common size
and vertical baseline per character so expressions do not change actor scale.
"""
import copy
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'art/ch1/dialogue-v2'
STATES=['neutral','thinking','distressed','expressive']
PAIRS={'family':['det1','det0'],'inn':['innma','seryeon'],
       'friends':['nabi','geokkuri'],'scholars':['doto','buri'],
       'witnesses':['karo','wanggu']}


def main():
    manifest={'id':'ch1-cast-identity-v2','created':'2026-10-11',
        'authorization':'User approved creation and integration of distinct cast designs after reviewing the ten characters.',
        'creation':'Reference-guided image_gen originals; no pixel editing, resizing, splitting or background removal. SVG clips the reviewed source rectangles at runtime.',
        'state_order':STATES,'atlases':{},'characters':{},'world':{}}
    for name,cast in PAIRS.items():
        metadata=json.loads((ART/f'{name}.meta.json').read_text())
        original=ROOT/metadata['src'];im=Image.open(original)
        assert im.mode=='RGBA' and im.getchannel('A').getextrema()[0]==0,(name,'Missing transparency')
        assert list(im.size)==[metadata['width'],metadata['height']],name
        assert hashlib.sha256(original.read_bytes()).hexdigest()==metadata['sha256'],name
        manifest['atlases'][name]=metadata
        for key in cast:
            states=metadata['characters'][key]
            manifest['world'][key]=copy.deepcopy(metadata.get('world',{}).get(key) or states['world'])
            boxes=[]
            for state in STATES:
                a=states[state];x,y,w,h=a['crop'];fx,fy,fs=a['face']
                boxes.append([min(x,fx),min(y,fy),max(x+w,fx+fs),max(y+h,fy+fs)])
            width=max(right-left for left,top,right,bottom in boxes)
            top=min(b[1] for b in boxes);bottom=max(b[3] for b in boxes)
            drawings={}
            for state,box in zip(STATES,boxes):
                a=copy.deepcopy(states[state]);left=(box[0]+box[2]-width)//2
                # Keep every source pixel and the speaker square inside the
                # common frame. Source cells remain separate from room art.
                a['crop']=[left,top,width,bottom-top]
                x,y,w,h=a['crop'];fx,fy,fs=a['face']
                assert 0<=x<x+w<=im.width and 0<=y<y+h<=im.height,(key,state,a)
                assert x<=fx and fx+fs<=x+w and y<=fy and fy+fs<=y+h,(key,state,a)
                assert im.getchannel('A').crop((x,y,x+w,y+h)).getbbox(),(key,state,'Empty drawing')
                for cell in metadata.get('cells',[]):
                    if cell['character']==key and cell['state']==state:continue
                    bbox=cell.get('foreground_bbox') or cell.get('bbox')
                    if bbox:
                        l,t,r,b=bbox
                        assert x+w<=l or r<=x or y+h<=t or b<=y,(key,state,'Adjacent drawing in crop',cell)
                drawings[state]=a
            manifest['characters'][key]=drawings
    feature_file=ART/'features.json'
    if feature_file.is_file():
        for key,states in json.loads(feature_file.read_text()).items():
            for state,feature in states.items():
                manifest['characters'][key][state]['feature']=feature
    (ART/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print('PASS immutable originals / 10 world actors / 40 stable dialogue frames / no adjacent artwork')


if __name__=='__main__':main()
