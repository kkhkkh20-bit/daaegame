import asyncio,json
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright
import webqa
webqa.FLOW_PROBE=webqa.FLOW_PROBE.replace('names=[',"names=['r13_life_group_conversation',")
from qa_smooth20_dialogue import ReviewQA
from qa_remaining_approved22 import setup
from qa_dialogue_routes import native_jump
ROOT=Path('/workspace/daaegame-reactions/experiments/renpy-ch1');OUT=Path('/workspace/life-groups-01950');OUT.mkdir(exist_ok=True)
async def main():
 report={'kind':'shipped approved registry; explicit state fixtures in actual engine','cases':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=ReviewQA(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.press('처음부터');await asyncio.sleep(.5)
   report['statuses']=await q.py('import renpy;result={g["id"]:g["status"] for g in renpy.store.R13_LIFE_GROUPS}')
   assert all(v=='approved' for v in report['statuses'].values())
   for loc,day,period,key,flags,camera in [('workshop',2,0,'workshop_pair',[],0),('inn',2,1,'inn_mending',[],0),('school',8,0,'school_play',['kids_school','wf_kkomi_saved','st_kkomi_class_seen'],520)]:
    await setup(q,day,loc,flags=['ev_g_done']+flags,period=period);await q.py('import renpy;s=renpy.store;s.r13_world_cameras={'+repr(loc)+':'+str(camera)+'};result=True');await native_jump(q,'r13_field');await q.wait('r13_hub');await q.press('주변 살피기');assert not any('함께' in x['text'] for x in (await q.state())['buttons']);await q.press('사람 보기');await page.mouse.move(1278,718);await asyncio.sleep(4.6);await q.shot(key)
    data=await q.py('import renpy;s=renpy.store;result=dict(actors=s.r13_stage_people(),offset=s.r13_world_offset(),groups=[g["id"] for g in s.r13_life_groups_here()],specs={a["person"]:s.r13_acting_spec(a["person"],a["pose"]) for a in s.r13_stage_people()})')
    assert data['groups']==[key],data['groups'];probes=[]
    clearance=await q.py('import renpy;s=renpy.store;result=dict(names=s.r13_actor_nameplates(s.r13_stage_people()),groups=s.r13_life_groups_here(),height=s.r13_control_height())')
    reserved=[tuple(g['label_position'])+(232,clearance['height']) for g in clearance['groups'] if not g.get('member_conversation')]
    members={m['person'] for g in clearance['groups'] for m in g['members']}
    def overlap(a,b):return max(0,min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0]))*max(0,min(a[1]+a[3],b[1]+b[3])-max(a[1],b[1]))
    data['nameplate_clearance']=[dict(p,overlap=sum(overlap(p['rect'],r) for r in reserved)) for p in clearance['names'] if p['person'] in members]
    assert all(not p['overlap'] for p in data['nameplate_clearance']),data['nameplate_clearance']
    for a in data['actors']:
     if a.get('life_group')!=key:continue
     spec=data['specs'][a['person']];cx,cy,cw,ch=spec['crop'];scale=a['height']/ch
     with Image.open(ROOT/'game'/spec['file']) as im:
      alpha=im.getchannel('A');candidates=[]
      for yy in range(10,int(ch)-10, max(1,int(ch)//15)):
       for xx in range(10,int(cw)-10,max(1,int(cw)//15)):
        al=alpha.getpixel((int(cx+xx),int(cy+yy)))
        if al==0 and len(candidates)<4:candidates.append((xx,yy,al))
      for xx,yy,al in candidates:
       px=int(a['x']+xx*scale-data['offset']);py=int(a['y']+yy*scale)
       if not (10<px<1270 and 105<py<600):continue
       probes.append(dict(person=a['person'],point=[px,py],source_alpha=al))
    values=await q.py('''import renpy
probes='''+repr(probes)+'''
for p in probes:
 f=renpy.display.render.focus_at_point(*p['point']);actions=getattr(getattr(f,'widget',None),'action',[]);actions=actions if isinstance(actions,(list,tuple)) else [actions];p['actions']=[str(getattr(a,'value',None)) for a in actions]
result=probes''')
    for probe in values:assert not any(probe['person'] in a for a in probe['actions']),probe
    if loc=='workshop':
     data['contact_focus']=await q.py('''import renpy
f=renpy.display.render.focus_at_point(570,425);a=getattr(getattr(f,'widget',None),'action',[]);a=a if isinstance(a,(list,tuple)) else [a];result=[str(getattr(v,'value',None)) for v in a]''')
     assert any('resident_tok' in a or 'buri' in a for a in data['contact_focus']),data['contact_focus']
    data['face_hits']=await q.py("import renpy\ns=renpy.store;result=[]\nfor a in s.r13_stage_people():\n if not a.get('life_group'):continue\n x,y,w,h=s.r13_actor_face(a,0);point=[int(x+w/2-s.r13_world_offset()),int(y+h/2)];f=renpy.display.render.focus_at_point(*point);actions=getattr(getattr(f,'widget',None),'action',[]);actions=actions if isinstance(actions,(list,tuple)) else [actions];result.append(dict(person=a['person'],point=point,actions=[str(getattr(v,'value',None)) for v in actions]))")
    for hit in data['face_hits']:assert any(hit['person'] in a for a in hit['actions']),hit
    baseline=await q.py('import renpy;result=renpy.store.room13')
    if loc=='school':
     assert not any('아이들과 함께' in b['text'] for b in (await q.state())['buttons'])
     await q.input(*data['face_hits'][0]['point'])
    else:await q.press(clearance['groups'][0]['label'])
    await q.wait('r13_life_group_conversation');await q.shot(key+'-dialogue')
    await page.set_viewport_size({'width':844,'height':390});q.touch=True;await q.shot(key+'-mobile-dialogue');await q.press('그만 듣기');await q.wait('r13_hub');assert await q.py('import renpy;result=renpy.store.room13')==baseline
    await page.set_viewport_size({'width':1280,'height':720});q.touch=False;await asyncio.sleep(.8)
    if loc=='school':
     data['member_entry_checks']=[]
     await q.shot('school-after-mobile-return')
     for hit in data['face_hits']:
      await q.input(*hit['point']);await q.wait('r13_life_group_conversation')
      lines=await q.py('import renpy;result=renpy.display.screen.get_screen("r13_life_group_conversation").scope["lines"]')
      assert lines[0][0]==hit['person'] and len(lines)==5,lines
      await q.shot('clicked-'+hit['person'])
      for _ in range(4):await q.press('계속 듣기')
      await q.press('돌아가기');await q.wait('r13_hub');assert await q.py('import renpy;result=renpy.store.room13')==baseline
      data['member_entry_checks'].append(dict(clicked=hit['person'],speakers=[line[0] for line in lines],unchanged_world=True))
    if loc=='inn':
     hit=next(h for h in data['face_hits'] if h['person']=='resident_tori');await q.py('import renpy;renpy.store.r13_target=None;result=True');await q.input(*hit['point']);await asyncio.sleep(.3);assert await q.py('import renpy;result=renpy.store.r13_target')=='resident_tori';await q.shot('tori-final-click')
    data['transparent_probes']=values;data['label']=key;report['cases'].append(data)
   report['passed']=True;print('PASS default-approved groups, rendered transparent-edge picking and shared tool focus',flush=True)
  finally:(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await b.close()
asyncio.run(main())
