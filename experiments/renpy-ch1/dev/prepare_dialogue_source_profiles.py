"""Prepare HOLD dialogue profiles from source masters, never map/pixel assets.

Input layout: {people:{id:{profiles:{height:{canvas:[w,h],frames:{slot:
{source_master:'/absolute/source.png',size:[w,h],offset:[x,y]}}}}}}}.
Dimensions and offsets are explicit layout decisions; no automatic pose alignment.
Output is a staging manifest, NOT the game's approved registry.
"""
import argparse,json
from pathlib import Path
from PIL import Image

def resize_source(source, size):
    if len(size)!=2 or any(type(n) is not int or n<=0 for n in size):
        raise ValueError('Explicit positive integer dimensions required')
    return source.convert('RGBA').resize(tuple(size),Image.Resampling.LANCZOS)

def prepare(layout, destination):
    destination=Path(destination)
    if destination.name!='dialogue-source-master':
        raise ValueError('Use a separate dialogue-source-master staging directory')
    manifest={'status':'HOLD_LAYOUT_AND_FINAL_DIRECTION_REVIEW','people':{}}
    for person,entry in layout['people'].items():
        if not person.replace('_','').isalnum():raise ValueError('Invalid person id')
        output={'status':'HOLD','art_style':'storybook_source','source_kind':'source_master','profiles':{}}
        for height,profile in entry['profiles'].items():
            if height not in ('560','760','840'):raise ValueError('Unknown profile')
            output['profiles'][height]={'canvas':profile['canvas'],'frames':{}}
            for slot,frame in profile['frames'].items():
                if slot not in ('neutral','joy','angry','anxious','surprise_talk','surprise_react'):raise ValueError('Unapproved slot schema')
                source=Path(frame['source_master'])
                if 'final_pixel' in source.parts:raise ValueError('Pixel derivative is not a source master')
                target=destination/person/height/(slot+'.png')
                if target.exists():raise FileExistsError(target)
                target.parent.mkdir(parents=True,exist_ok=True)
                with Image.open(source) as original:
                    resize_source(original,frame['size']).save(target)
                output['profiles'][height]['frames'][slot]={'file':'assets/dialogue-source-master/'+target.relative_to(destination).as_posix(),'offset':frame['offset'],'source_master':str(source)}
        manifest['people'][person]=output
    return manifest

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('layout');parser.add_argument('destination');args=parser.parse_args()
    result=prepare(json.loads(Path(args.layout).read_text()),args.destination)
    path=Path(args.destination)/'HOLD-manifest.json'
    if path.exists():raise FileExistsError(path)
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
