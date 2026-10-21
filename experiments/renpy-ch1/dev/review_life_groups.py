"""Offline geometry review from actual Python stage layers. NOT a Ren'Py screenshot.
Only renderer/music/captions are stubbed; schedules and placement functions execute source.
"""
import copy,json
from pathlib import Path
from test_life_groups import ROOT,environment,selected

def stage_environment(key):
    e,row,_=environment(key);group_stage=e['r13_stage_people']
    selected(e,'room13_world_camera.rpy',{'r13_layout','r13_world_width'})
    selected(e,'room13_acting.rpy',{'R13_STAGE_FLOORS','R13_STAGE_COUNTERS','R13_STAGE_CACHE','R13_CROWD_SLOTS','R13_STAGE_CRITICAL','R13_STAGE_POSITIONS','R13_LIVING_ALLOWED','r13_acting_spec','r13_actor_geometry','r13_acting_head','r13_living_pose','r13_world_display_height','r13_stage_people','r13_staged_activity'})
    selected(e,'room13_typography.rpy',{'r13_field_ui_rects'})
    e.update(R13_CALENDAR={},r13_activity_text=lambda p:'',r13_calendar_activity=lambda p:'',r13_control_height=lambda:64,r13_control_y=lambda:640,r13_control_upper_y=lambda:560)
    e['store'].R13_WORLD_LAYOUTS=e['R13_WORLD_LAYOUTS']
    for filename,names in [
        ('systems/room13_daram_home.rpy',{'_r13_daram_home_stage','r13_stage_people','r13_daram_home_activity'}),
        ('systems/room13_event_offers.rpy',{'_r13_offer_stage','r13_stage_people','r13_offer_pose'}),
        ('systems/room13_map_actions.rpy',{'_r13_ma_stage','r13_stage_people','r13_ma_place','r13_ma_shape','r13_ma_feet'}),
        ('systems/room13_perspective.rpy',{'R13_PERSPECTIVE','R13_PERSPECTIVE_COUNTER_DEPTH','R13_PERSPECTIVE_CONTACTS','r13_perspective_line','r13_perspective_height','_r13_perspective_stage','r13_stage_people'}),
        ('systems/room13_map_work_nine.rpy',{'R13_MAP_WORK_NINE','r13_map_work_nine_allowed','_r13_map9_stage','r13_stage_people'}),
        ('systems/room13_solbang_chinchilla.rpy',{'_r13_solbang_living_pose','r13_living_pose'}),
        ('systems/room13_map_action27.rpy',{'R13_MAP_ACTION27','r13_map27_variant','_r13_map27_stage','r13_stage_people'}),
        ('systems/room13_spatial_contacts.rpy',{'R13_HOME_CONTACTS','R13_SQUARE_LEVELS','r13_contact_geometry','_r13_contact_stage','r13_stage_people'}),
        ('systems/room13_investigation_balance.rpy',{'r13_balance_translate','r13_balance_school','r13_balance_post','_r13_balance_stage','r13_stage_people'})]:
        selected(e,filename,names)
    for m in e['R13_MAP_WORK_NINE']['people']:e['R13_ACTING'].setdefault(m['person'],{})[m['pose']]=m['spec']
    e['_r13_life_groups_stage']=e['r13_stage_people'];e['r13_stage_people']=group_stage
    return e,row

def render(e,actors,path):
    from PIL import Image,ImageDraw
    layout=e['r13_layout']();bg=Image.open(ROOT/'game'/layout['files'][e['r13_daylight']()]).convert('RGBA').resize((layout['width'],720))
    for a in actors:
        spec=e['r13_acting_spec'](a['person'],a['pose']);x,y,w,h=spec['crop']
        sprite=Image.open(ROOT/'game'/spec['file']).crop((x,y,x+w,y+h)).resize((a['width'],a['height']),Image.Resampling.NEAREST).convert('RGBA')
        mask=Image.new('L',sprite.size);d=ImageDraw.Draw(mask)
        polygons=([a['occlusion']] if a.get('occlusion') else [])+a.get('map27_occlusion',[])
        for poly in polygons:d.polygon([(px-a['x'],py-a['y']) for px,py in poly],fill=255)
        for poly in a.get('map27_keepouts',[]):d.polygon([(px-a['x'],py-a['y']) for px,py in poly],fill=0)
        from PIL import ImageChops
        sprite.putalpha(ImageChops.subtract(sprite.getchannel('A'),mask));bg.alpha_composite(sprite,(a['x'],a['y']))
    d=ImageDraw.Draw(bg);d.rectangle((0,0,layout['width'],30),fill='#151515');d.text((12,8),'OFFLINE SOURCE GEOMETRY REVIEW - NOT AN ENGINE SCREENSHOT',fill='white')
    bg.convert('RGB').save(path)

if __name__=='__main__':
    out=ROOT/'reports/life-groups-20261018';out.mkdir(parents=True,exist_ok=True);report=[]
    for key in ('workshop_pair','inn_mending','school_play'):
        e,row=stage_environment(key)
        for day in row['days']:
            for period in row['periods']:
                e['store'].room13.update(day=day,period=period)
                before=copy.deepcopy(e['store'].room13)
                solo=e['_r13_life_groups_stage']();staged=e['r13_stage_people']()
                assert e['store'].room13==before
                report.append(dict(group=key,day=day,period=period,eligible=e['r13_life_group_allowed'](row,solo),formed=bool(e['r13_life_groups_here']()),actors=staged))
                if day==row['days'][0] and period==row['periods'][0]:
                    render(e,solo,out/(key+'-before-offline.jpg'));render(e,staged,out/(key+'-after-offline.jpg'))
    (out/'geometry-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps([{k:r[k] for k in ('group','day','period','eligible','formed')} for r in report],indent=2))
