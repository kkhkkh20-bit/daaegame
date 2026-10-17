"""Measure source-master layouts before local import; never alter source images.

Usage: python dev/audit_dialogue_profile_layout.py layout.json report.json
Uses the explicit layout schema of prepare_dialogue_source_profiles.py.
Warnings are review candidates, not automatic pose corrections or blur judgments.
"""
import hashlib,json,sys
from pathlib import Path
from PIL import Image
SLOTS={'neutral','joy','angry','anxious','surprise_talk','surprise_react'}

def audit(layout):
    result={'status':'MEASUREMENTS_ONLY_VISUAL_REVIEW_REQUIRED','errors':[], 'frames':[], 'warnings':[]}
    if len(layout['people'])!=layout.get('expected_people',20):result['errors'].append('Unexpected approved batch size')
    for person,entry in layout['people'].items():
        if set(entry['profiles'])!={'560','760','840'}:result['errors'].append([person,'Missing runtime profile'])
        for height,profile in entry['profiles'].items():
            if set(profile['frames'])!=SLOTS:result['errors'].append([person,height,'Expected six distinct slot names'])
            measured={}
            for slot,frame in profile['frames'].items():
                source=Path(frame['source_master'])
                if 'final_pixel' in source.parts:result['errors'].append([person,slot,'Pixel derivative supplied'])
                if not source.is_file():result['errors'].append([person,slot,'Missing source']);continue
                with Image.open(source) as image:
                    w,h=image.size
                    alpha=image.convert('RGBA').getchannel('A')
                    bounds=alpha.point(lambda a:255 if a>=16 else 0).getbbox()
                    if not bounds:result['errors'].append([person,slot,'Empty image']);continue
                    tw,th=frame['size'];ox,oy=frame['offset'];sx,sy=tw/w,th/h
                    box=[ox+bounds[0]*sx,oy+bounds[1]*sy,ox+bounds[2]*sx,oy+bounds[3]*sy]
                    item=dict(person=person,profile=height,slot=slot,source=str(source),source_size=[w,h],target_size=[tw,th],scale=[sx,sy],visible_bounds=box,foot_baseline=box[3],sha256=hashlib.sha256(source.read_bytes()).hexdigest())
                    measured[slot]=item;result['frames'].append(item)
                    if sx>1 or sy>1:result['warnings'].append(dict(person=person,profile=height,slot=slot,kind='upscale_requires_visual_sharpness_review',scale=[sx,sy]))
                    if box[0]<0 or box[1]<0 or box[2]>profile['canvas'][0] or box[3]>profile['canvas'][1]:result['warnings'].append(dict(person=person,profile=height,slot=slot,kind='visible_bounds_outside_canvas'))
            neutral=measured.get('neutral')
            if neutral:
                for slot,item in measured.items():
                    item['baseline_delta_from_neutral']=item['foot_baseline']-neutral['foot_baseline']
                    nb=neutral['visible_bounds'];b=item['visible_bounds']
                    item['visible_height_ratio_to_neutral']=(b[3]-b[1])/(nb[3]-nb[1])
                    if slot!='neutral' and abs(item['baseline_delta_from_neutral'])>3:
                        result['warnings'].append(dict(person=person,profile=height,slot=slot,kind='baseline_shift_check_pose_before_adjusting',delta=item['baseline_delta_from_neutral']))
                    if slot!='neutral' and item['sha256']==neutral['sha256']:
                        result['warnings'].append(dict(person=person,profile=height,slot=slot,kind='same_source_as_neutral_verify_intent'))
    return result

if __name__=='__main__':
    result=audit(json.loads(Path(sys.argv[1]).read_text()))
    Path(sys.argv[2]).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('frames:',len(result['frames']),'errors:',len(result['errors']),'review warnings:',len(result['warnings']))
    raise SystemExit(bool(result['errors']))
