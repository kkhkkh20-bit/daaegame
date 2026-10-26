"""Natural V1.1.1 play through existing Room13 field, map, topics and notebook."""
import asyncio,json,os,ast,time
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
ROOT=Path(__file__).resolve().parents[1];OUT=Path(os.environ.get('ROOM13_QA_OUT','/workspace/work/v111/browser'));OUT.mkdir(parents=True,exist_ok=True)
PLAN=json.loads((ROOT/'docs/story-v111/compiled-reference.json').read_text());PROOFS={v['title']:v for v in PLAN.values() if v['kind']=='proof'}
class Fast(UIQA):
 async def state(self):
  # 0.20.42 부터 현장 좌우 이동은 글자 없는 그림 버튼이다. 이름(alt)으로 찾아 예전 '‹'/'›' 버튼처럼 보이게 한다.
  st=await super().state()
  pans=await UIQA.py(self,'import renpy\nresult=[[("‹" if f.widget.style.alt=="왼쪽 구역" else "›"),f.x,f.y,f.w,f.h] for f in renpy.display.focus.focus_list if f.x is not None and getattr(getattr(f.widget,"style",None),"alt",None) in ("왼쪽 구역","오른쪽 구역")]')
  for t,x,y,w,h in pans or []:st['buttons'].append({'text':t,'value':'pan','rect':[x,y,w,h]})
  return st
 async def py(self,code):
  # 화면이 닫히는 순간 그 화면을 읽으면 None.scope 로 실패한다. 화면이 바뀔 시간을 주고 두 번 더 본다.
  for attempt in range(3):
   try:return await super().py('ns={};exec('+repr(code)+',ns);result=ns.get("result")')
   except Exception as e:
    if attempt==2 or "'NoneType' object has no attribute" not in str(e):raise
    await asyncio.sleep(.6)
 async def input(self,x,y):
  vp=self.p.viewport_size;s=min(vp['width']/1280,vp['height']/720);x=(vp['width']-1280*s)/2+x*s;y=(vp['height']-720*s)/2+y*s
  await self.p.mouse.click(x,y);await asyncio.sleep(.08)
 async def value(self,value):
  await asyncio.sleep(.5)
  if isinstance(value,tuple) and value[0]=='person':
   st=await self.state();bs=[b for b in st['buttons'] if b.get('value')==repr(value) and b['rect'][2]>=20]
   if bs:
    b=min(bs,key=lambda b:b['rect'][2]*b['rect'][3]);x,y,w,h=b['rect']
    edge='‹' if x<=1 else '›' if x+w>=1279 else None
    if not b['text'].strip() and edge and any(t['text'].strip()==edge for t in st['buttons']):
     await self.press(edge);await asyncio.sleep(.6);return
    await self.input(x+w/2,y+h/2);return
  return await super().value(value)
 async def advance_dialogue(self):
  st=await self.state()
  bs=[b for b in st['buttons'] if '건너뛰기' in b['text']]
  if bs:
   x,y,w,h=min(bs,key=lambda b:b['rect'][2]*b['rect'][3])['rect'];await self.input(x+w/2,y+h/2)
  else:await self.input(900,590)
 async def click_object(self,key,attempt=0):
  await asyncio.sleep(.35)
  if attempt>=28:raise AssertionError(('Object not reached after sampled UI clicks',key,attempt))
  rects=await self.py('import renpy;result=[[f.x,f.y,f.w,f.h] for f in renpy.display.focus.focus_list if f.x is not None and any(getattr(a,"value",None)==("object",'+repr(key)+') for a in (getattr(f.widget,"clicked",None) if isinstance(getattr(f.widget,"clicked",None),(list,tuple)) else [getattr(f.widget,"clicked",None)]))]')
  if not rects:
   rects=await self.py('import renpy;s=renpy.store;n=s.r13_object_name('+repr(key)+');result=[[f.x,f.y,f.w,f.h] for f in renpy.display.focus.focus_list if f.x is not None and getattr(getattr(f.widget,"style",None),"alt",None)==n]')
  if not rects:
   state=await self.state()
   if any('주변 살피기' in b['text'] for b in state['buttons']):
    await self.press('주변 살피기');return
   x=await self.py('import renpy;s=renpy.store;result=s.ROOM13["objects"][s.room13["location"]]['+repr(key)+']["rect"][0]-s.r13_world_offset()')
   arrows=[b['text'].strip() for b in state['buttons'] if b['text'].strip() in ('‹','›')]
   wanted='‹' if x<640 else '›'
   if wanted in arrows:await self.press(wanted)
   elif arrows:await self.press(arrows[0])
   else:
    await asyncio.sleep(.6);return
   await asyncio.sleep(.4);return
  x,y,w,h=rects[-1]
  fx,fy=((.5,.5),(.2,.2),(.8,.2),(.2,.8),(.8,.8),(.05,.5),(.95,.5))[attempt%7]
  await self.input(x+w*fx,y+h*fy)
 async def navigate_map(self,target):
  region=await self.py('import renpy;result=renpy.store.r13_map_region('+repr(target)+')')
  await self.press({'inn':'여관 안','mountain':'숲·산길','village':'마을'}[region])
  await asyncio.sleep(.3)
  if region!='village':
   x,y,w,h=await self.py('import renpy;result=renpy.store.r13_bmap_label_rect('+repr(region)+','+repr(target)+')')
   await self.input(x+w/2,y+h/2);await asyncio.sleep(.3)
  else:
   for attempt in range(16):
    data=await self.py('import renpy;s=renpy.store;c=renpy.display.screen.get_screen("r13_map").scope;k='+repr(target)+';w=renpy.display.screen.get_widget("r13_map","map_name_"+k);f=next((f for f in renpy.display.focus.focus_list if f.widget is w and f.x is not None),None);v=renpy.display.screen.get_widget("r13_map","r13_map_view");z=max(c["village_zoom"],1136.0/1642,506.0/958);row=s.R13_VILLAGE_B_PLACES.get(k);result=dict(selected=c["selected"],rect=[f.x,f.y,f.w,f.h] if f else None,point=[88+row["label_center"][0]*z-v.xadjustment.value,122+row["label_center"][1]*z-v.yadjustment.value] if row else None,extras=c["extra_places"],label=s.r13_map_label(k))')
    if data['selected']==target:break
    if data['rect']:
     x,y,w,h=data['rect']
     if 100<x+w/2<1210 and 135<y+h/2<570:
      await self.input(x+w/2,y+h/2);await asyncio.sleep(.3);continue
    if data['point'] is None:
     if not data['extras']:await self.press('다른 장소')
     await self.press(data['label']);continue
    x,y=data['point']
    if not data['rect'] and 110<x<1200 and 140<y<560:
     await self.input(x,y);await asyncio.sleep(.3);continue
    dx=max(-450,min(450,650-x));dy=max(-250,min(250,350-y))
    # Move the visible paper through a drag, exactly as a player pans it.
    vp=self.p.viewport_size;scale=min(vp['width']/1280,vp['height']/720);ox=(vp['width']-1280*scale)/2;oy=(vp['height']-720*scale)/2
    await self.p.mouse.move(ox+650*scale,oy+350*scale);await self.p.mouse.down();await self.p.mouse.move(ox+(650+dx)*scale,oy+(350+dy)*scale,steps=12);await self.p.mouse.up();await asyncio.sleep(.4)
   else:raise AssertionError(('Map destination unreachable',target,data))
  if 'r13_map' in (await self.state())['screens']:await self.press('이곳으로 이동')
 async def page_arrow(self,direction,right=False):
  st=await self.state()
  bs=[b for b in st['buttons'] if b['text'].strip()==direction and (b['rect'][0]>=330)==right]
  if not bs:raise AssertionError(('Page arrow unavailable',direction,right,st))
  x,y,w,h=bs[0]['rect'];await self.input(x+w/2,y+h/2);await asyncio.sleep(.25)
 async def select_material(self,key,finish=True):
  """Navigate the real notebook chips, groups and pages; never set screen/story state."""
  for attempt in range(40):
   data=await self.py('import renpy;s=renpy.store;c=renpy.display.screen.get_screen("r13_book").scope;k='+repr(key)+';e=c["entries"];a=c.get("drawer_all",e);where=s.r13_drawer_where(k,a);result=dict(entries=list(e),page=s.r13_record_page(e,c["page"]),size=s.r13_record_page_size(),detail=c["selected_record"],current_group=s.r13_drawer_group_choice("past",a,c.get("drawer_case")),gpage=c.get("drawer_gpage",0),ipage=c.get("drawer_ipage",0),groups=[g for g,keys in s.r13_drawer_groups("past",a)],group_keys=s.r13_drawer_group_keys("past",a,where[1]) if where[1] else [],grid_size=s.R13_DRAWER_GRID_ROWS*s.R13_DRAWER_GRID_COLS,drawer=c.get("drawer"),view=c.get("drawer_view",["list"])[0],where=where,name=s.r13_catalog_title(k),label=c["present_label"],purpose=c.get("purpose"),group=s.r13_drawer_group_title("past",where[1],False) if where[1] else None)')
   if data['detail']==key and key in data['entries']:
    await self.press(data['label'])
    if finish and data['purpose'] in ('proof','compare'):
     await asyncio.sleep(.3);await self.press('선택 마치기')
    return
   if key in data['entries']:
    page=data['entries'].index(key)//data['size']
    if page!=data['page']:await self.page_arrow('‹' if page<data['page'] else '›');continue
    await self.press(data['name']);continue
   if data['drawer']!='past':await self.press('지난 사건');continue
   if data['view']!='groups':await self.press('지난 사건');continue
   st=await self.state();normal=lambda x:''.join(x.split())
   if any(normal(data['name']) in normal(b['text']) for b in st['buttons']):await self.press(data['name']);continue
   if data['where'][1] not in data['groups']:raise AssertionError(('Record not owned/visible',key,data))
   group_page=data['groups'].index(data['where'][1])//data['size']
   if group_page!=data['gpage']:await self.page_arrow('‹' if group_page<data['gpage'] else '›');continue
   if data['current_group']!=data['where'][1]:await self.press(data['group']);continue
   grid_page=data['group_keys'].index(key)//data['grid_size']
   if grid_page!=data['ipage']:await self.page_arrow('‹' if grid_page<data['ipage'] else '›',right=True);continue
   await self.press(data['name'])
  raise AssertionError(('Material unreachable through notebook',key,data))
 async def press(self,label):
  label={'근거를 내놓는다':'자료 고르기','논리를 연결한다':'선택한 근거 제출','그만두기':'선택 마치기'}.get(label,label)
  for attempt in range(40):
   st=await self.state();bs=[b for b in st['buttons'] if ''.join(label.split()) in ''.join(b['text'].split()) and b['rect'][3]>12]
   if bs:
    b=min(bs,key=lambda b:b['rect'][2]*b['rect'][3]);x,y,w,h=b['rect'];await self.input(x+w/2,y+h/2);return
   # 대사 한 줄이 아직 떠 있는 사이에는 찾는 버튼이 없다. 그 줄을 넘기고 다시 본다.
   if attempt and attempt%10==0 and 'say' in st['screens'] and 'choice' not in st['screens']:
    await self.input(900,590);await asyncio.sleep(.4)
   if attempt and attempt%5==0 and 'choice' in st['screens']:
    pages=[b for b in st['buttons'] if '다음 →' in b['text'] or '← 이전' in b['text']]
    if pages:
     b=next((b for b in pages if '다음 →' in b['text']),pages[0]);x,y,w,h=b['rect'];await self.input(x+w/2,y+h/2)
   await asyncio.sleep(.1)
  raise AssertionError((label,st))

def shelter_step2(route,v):
 # 피코 보호: 포대 → 천 → 벤치 살피기(80) → 벤치 닦기(81) → 자리 전하기. 벤치 두 단계는 0.20.4x 에 더해졌다.
 if route!='shelter':return 3
 for key,idx in (('piko_sacks2',0),('piko_cloth2',1),('piko_bench_seen2',80),('piko_bench_clean2',81)):
  if not v.get(key):return idx
 return 2
async def main():
 route=os.environ.get('V111_ROUTE','shelter');stone=int(os.environ.get('V111_STONE','0'));custody=int(os.environ.get('V111_CUSTODY','0'))
 async with async_playwright() as p:
  b=await p.chromium.launch_persistent_context(str(OUT/('profile-'+os.environ.get('V111_PROFILE',route))),executable_path=os.environ.get('ROOM13_CHROME','/opt/pw-browsers/chromium-1194/chrome-linux/chrome'),viewport={'width':1280,'height':720},args=['--no-sandbox','--remote-debugging-port=9224','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])

  for previous in b.pages:await previous.close()
  pg=await b.new_page();q=Fast(pg,OUT);errors=[];pg.on('pageerror',lambda e:errors.append(str(e)));events=[];shots=set()
  async def snap():
   return await q.py('import renpy;s=renpy.store;result=dict(screens=[n for n in ("main_menu","say","choice","r13_confirm","r13_hub","r13_topics","r13_map","r13_book","r13_records","r13_crisis_proof","_exception") if renpy.display.screen.get_screen(n)],gate=(s.room13 or {}).get("v111",{}).get("gate"),choice=getattr(s,"v111_menu_owner",None),claim=getattr(s,"v111_claim",None),binding=s.r13_v111_binding() if s.r13_v111_active() else {},values=(s.room13 or {}).get("v111",{}).get("values",{}),evidence=(s.room13 or {}).get("evidence",[]),location=(s.room13 or {}).get("location"),music=renpy.audio.music.get_playing(),people=s.r13_visible_people() if s.r13_v111_active() else [])')
  try:
   await pg.goto(os.environ.get('ROOM13_URL','http://localhost:8766/preview/room13-dev/'),wait_until='domcontentloaded',timeout=180000)
   await pg.wait_for_function("typeof renpy_exec==='function'",timeout=180000);await asyncio.sleep(12);await q.input(1100,600);await q.wait('main_menu')
   await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True')
   print('BUILD_VERSION',await q.py('import renpy;result=renpy.store.config.version'),flush=True)
   if os.environ.get('V111_RESUME'):
    code='import renpy;renpy.exports.load('+repr(os.environ['V111_RESUME'])+')'
    await pg.evaluate('code=>{renpy_exec("exec("+JSON.stringify(code)+")").catch(()=>{});return true;}',code)
    await asyncio.sleep(3)
    await pg.evaluate("window._renpy_cmd_callback({data:true})")
   else:await q.press('처음부터')
   if route=='nero' and os.environ.get('V111_RESUME'):
    await q.wait('r13_hub');await q.press('기록');await q.wait('r13_records')
    for _ in range(8):
     try:await q.press('초대 편지');break
     except AssertionError:
      paging=await q.py('import renpy;s=renpy.store;c=renpy.display.screen.get_screen("r13_records").scope;e=c["entries"];result=[e.index("V111:E01")//s.r13_record_page_size(),s.r13_record_page(e,c["page"])]')
      await q.press('이전' if paging[0]<paging[1] else '다음')
    else:raise AssertionError('Letter record unavailable')
    assert await q.py('import renpy;result=renpy.store.r13_material_art("V111:E01") is not None')
    await q.shot('nero-letter-icon');await q.press('닫기')
   reread_checked=False;audit_seen=set();audit_rows=[];smoke_daram=False;wrong_probe=0;proof_keys=[];book_target=None;map_target=None;last=None;checkpoints=set();object_attempts={};stale_n=0;stale_last=None
   for step in range(4500):
    st=await snap();sc=st['screens'];assert '_exception' not in sc,st
    state=(st['gate'],tuple(sc),st['choice'],st['claim'])
    if os.environ.get('V111_STOP_GATE')==st['gate'] and 'r13_hub' in sc:
     await q.shot('natural-stop-'+st['gate']);break
    if os.environ.get('V111_SMOKE') and st['gate']=='room_observe' and 'r13_hub' in sc:
     await q.shot('smoke-room-observe');break
    if state!=last:events.append(dict(step=step,**st));last=state;print('STATE',step,st['gate'],sc,st['choice'],st['location'],flush=True)
    # 같은 화면·값에서 입력이 아무것도 바꾸지 못하면 조용히 돌지 말고 화면을 남기고 멈춘다.
    finger=json.dumps([st['gate'],sc,st['location'],st.get('values'),st.get('evidence'),st.get('say')],sort_keys=True,default=str)
    stale_n=stale_n+1 if finger==stale_last else 0;stale_last=finger
    if stale_n>=80:
     dump=await q.state();print('STALE',st['gate'],st['location'],[b['text'] for b in dump['buttons']][:40],flush=True)
     raise AssertionError(('Input did not progress',st['gate'],st['location']))
    if st['gate']=='checkpoint' and 'r13_confirm' in sc:
     assert st['values']['piko_alive']==(route=='shelter'),st
     assert st['values']['carried_dry_blankets']==(0 if route=='shelter' else 2),st
     assert st['values']['public_stones']==('restored' if stone==0 else 'with_baek'),st
     assert st['values']['silluk_status']==('reporting_obligation' if custody==0 else 'detained_work_waiting_station'),st
     await q.shot(route+'-complete')
     if os.environ.get('V111_SAVE_END'):
      await q.press('저장하기');await q.wait('save');await q.shot(route+'-completion-save');await q.press('돌아가기');await q.wait('r13_confirm')
     await q.press('메인 화면으로')
     break
    if 'say' in sc:
     await q.advance_dialogue();continue
    if 'r13_confirm' in sc:
     yes=await q.py('import renpy;result=renpy.display.screen.get_screen("r13_confirm").scope["yes"]')
     await q.press(yes);continue
    if 'choice' in sc:
     if st['choice'] in ('afternoon','stone_choice','custody_choice') and st['choice'] not in shots:
      await q.shot(route+'-'+st['choice']);shots.add(st['choice'])
     key=st['choice'];pick={'letter_menu':2,'afternoon':0 if route=='shelter' else 1,'stone_choice':stone,'custody_choice':custody}.get(key,0)
     if st['gate']=='lamp_observe':pick=next(i for i in range(4) if not st['values'].get('lamp_part_'+str(i)))
     caption=await q.py('import renpy;result=[i.caption for i in renpy.display.screen.get_screen("choice").scope["items"] if i.action is not None]['+str(pick)+']')
     await asyncio.sleep(.4);await q.press(caption);continue
    if 'r13_crisis_proof' in sc:
     title=st['claim'][5:];node=PROOFS[title]
     selected=await q.py('import renpy;result=list(renpy.store.room13["arguments"].get(renpy.store.v111_claim,[]))')
     if os.environ.get('V111_WRONG_ONCE') and wrong_probe<2:
      if wrong_probe==0 and 'V111:E01' not in selected:
       book_target='V111:E01';await q.press('근거를 내놓는다');continue
      if wrong_probe==0:
       await q.press('논리를 연결한다');wrong_probe=1;continue
      assert selected==[],('Wrong proof retained materials',selected)
      wrong_probe=2
     missing=[x for x in node['correct'] if 'V111:'+x not in selected]
     if missing:book_target='V111:'+missing[0];await q.press('근거를 내놓는다')
     else:
      if 'proof' not in shots:await q.shot(route+'-proof');shots.add('proof')
      await q.press('논리를 연결한다')
     continue
    if 'r13_book' in sc:
     if book_target:
      await q.select_material(book_target);book_target=None
     else:await q.press('그만두기')
     continue
    if 'r13_records' in sc:
     await q.press('닫기');continue
    if 'r13_topics' in sc:
     options=st['binding']['options'];person=await q.py('import renpy;c=renpy.display.screen.get_screen("r13_topics");result=c.scope["person"] if c else None')
     if person is None:continue
     eligible=[o for o in options if o.get('person')==person]
     gate=st['gate']
     if gate=='gate_investigate' and any(k not in st['evidence'] for k in ('V111:E03','V111:E04')):
      await q.press('돌아가기');continue
     if gate=='afternoon2':
      wanted=shelter_step2(route,st['values'])
      desired=next(o for o in options if o['index']==wanted)
      if desired.get('person')!=person or desired.get('location')!=st['location']:
       await q.press('돌아가기');continue
      eligible=[desired]
     preferred={'gate_investigate':5,'gate_choice':1,'registered_menu':1,'post_menu':1}.get(gate)
     if not eligible:
      await q.press('돌아가기');await asyncio.sleep(.3);continue
     option=next((o for o in eligible if o.get('index')==preferred),eligible[0])
     # A present question opens the book: remember what to show (review 2026-10-22).
     if option.get('present'):book_target=option['present']
     await q.press(option['title']);continue
    if 'r13_map' in sc:
     target=map_target or next(o.get('move') for o in st['binding']['options'] if o.get('move'))
     map_target=None
     await q.navigate_map(target)
     continue
    if 'r13_hub' in sc:
     gate=st['gate']
     if gate in ('sleep1','box_inspect','post_menu','lamp_observe','sleep2','lamp_inspect3','loan_read','sale_check','sleep3') and gate not in checkpoints:
      slot='v111-'+gate
      await q.py('import renpy;renpy.exports.save('+repr(slot)+');result=True');checkpoints.add(gate)
      print('SAVED',slot,flush=True)
      if gate=='sleep3':
       assert st['values']['piko_alive']==(route=='shelter'),('Wrong afternoon route',route,st['values'])
       assert st['values']['carried_dry_blankets']==(0 if route=='shelter' else 2),st
       await asyncio.sleep(1)
       await q.shot(route+'-day3-save');break
     if os.environ.get('V111_AUDIT') and st['location'] not in audit_seen:
      loc=st['location'];audit_seen.add(loc)
      candidates=await q.py('import renpy;s=renpy.store;bound={o.get("object") for o in s.r13_v111_binding().get("options",[])};result=[(k,s.r13_v111_ambient_text(k,v)) for k,v in s.ROOM13["objects"].get(s.room13["location"],{}).items() if k not in bound and s.r13_object_visible(v) and s.r13_v111_ambient_text(k,v) and not v.get("give") and not v.get("flags") and not v.get("special")]')
      for obj,text in candidates[:2]:
       observed=False
       for attempt in range(20):
        fx,fy=((.5,.5),(.05,.5),(.95,.5),(.05,.05),(.95,.05),(.05,.95),(.95,.95),(.25,.25),(.75,.75))[attempt%9]
        pos=await q.py('import renpy;s=renpy.store;x,y,w,h=s.ROOM13["objects"][s.room13["location"]]['+repr(obj)+']["rect"];result=[x+w*'+str(fx)+'-s.r13_world_offset(),y+h*'+str(fy)+']')
        if not 24<pos[0]<1230:
         arrow='‹' if pos[0]<24 else '›'
         if any(arrow in b['text'] for b in (await q.state())['buttons']):
          await q.press(arrow);await asyncio.sleep(.6)
         continue
        await asyncio.sleep(.25);await q.input(*pos);await asyncio.sleep(.15);current=await snap()
        if 'say' in current['screens']:
         said=(await q.state())['say'];observed=''.join(text[:16].split()) in ''.join(said.split())
         if observed:
          await q.shot('audit-reaction-'+loc+'-'+obj)
          print('AMBIENT',obj,repr((await q.state())['say']),flush=True)
         if not observed:print('MISSED',loc,obj,'expected',repr(text),'got',repr(said),flush=True)
         for _ in range(10):
          if 'say' not in (await snap())['screens']:break
          await q.input(900,590)
         if observed:break
         continue
        if 'r13_topics' in current['screens']:
         await q.press('돌아가기');await asyncio.sleep(.3)
       after=await snap()
       assert after['values']==st['values'] and after['evidence']==st['evidence'] and after['gate']==st['gate'],('Ambient changed story',loc,obj,after)
       if not observed:
        audit_rows.append(dict(location=loc,object=obj,status='not reached by sampled clicks; inspect overlap'));await q.shot('overlap-'+loc+'-'+obj);continue
       audit_rows.append(dict(location=loc,object=obj,reaction=text));await q.shot('audit-'+loc+'-'+obj)
      people=await q.py('import renpy;s=renpy.store;result=[p for p in s.r13_visible_people() if not s.r13_v111_questions(p)]')
      for person in people:
       state=await q.state()
       if not any(b.get('value')==repr(('person',person)) and b['text'].strip() for b in state['buttons']):continue
       await q.value(('person',person));await q.wait('r13_topics');await q.press('돌아가기');await q.wait('r13_hub')
       after=await snap();assert after['values']==st['values'] and after['evidence']==st['evidence'],('Empty topic changed story',person)
       audit_rows.append(dict(location=loc,person=person,empty_topics='opened and returned'))
      continue
     if os.environ.get('V111_SMOKE') and gate=='gate_request' and not smoke_daram:
      await q.value(('person','daram'));await q.wait('r13_topics');await q.shot('smoke-daram-response');await q.press('돌아가기');await q.wait('r13_hub');smoke_daram=True;continue
     gate=st['gate'];options=st['binding'].get('options',[])
     if gate not in shots and gate in ('gate_investigate','box_inspect','afternoon','sleep2','piko_clean','lamp_inspect3','measurement_read','sleep3'):
      await q.shot(route+'-'+gate);shots.add(gate)
     if gate=='gate_investigate':
      idx=0 if 'V111:E03' not in st['evidence'] else 1 if 'V111:E04' not in st['evidence'] else 5
      if os.environ.get('V111_AUDIT') and idx==5 and not reread_checked:idx=2;reread_checked=True
      option=next(o for o in options if o['index']==idx)
     elif gate=='lamp_observe':idx=next(i for i in range(4) if not st['values'].get('lamp_part_'+str(i)));option=next(o for o in options if o['index']==idx)
     elif gate=='registered_menu':option=next(o for o in options if o.get('move'))
     elif gate=='afternoon2':
      wanted=shelter_step2(route,st['values'])
      option=next(o for o in options if o['index']==wanted)
     else:option=options[0]
     if option.get('location') and option['location']!=st['location']:
      map_target=option.get('move') or option['location'];await q.press('지도');continue
     if option.get('move'):await q.press('지도');continue
     if option.get('person'):
      person=option['person'];state=await q.state()
      if not any(b.get('value')==repr(('person',person)) for b in state['buttons']):
       x=await q.py('import renpy;s=renpy.store;a=next(a for a in s.r13_stage_people() if a["person"]=='+repr(person)+');result=a["x"]-s.r13_world_offset()')
       arrow='‹' if x<640 else '›'
       if any(arrow in b['text'] for b in state['buttons']):await q.press(arrow)
       await asyncio.sleep(.6)
      else:await q.value(('person',person))
      continue
     if option.get('object'):
      obj=option['object'];attempt=object_attempts.get((gate,obj),0);object_attempts[(gate,obj)]=attempt+1
      await q.click_object(obj,attempt);continue
    await asyncio.sleep(.1)
   else:raise AssertionError(('Play did not complete',st))
   assert not errors,errors
   report=dict(status='passed',route=route,stone=stone,custody=custody,final=st,events=events,page_errors=errors,ambient_audit=audit_rows,wrong_proof_recovered=(wrong_probe==2),resume=os.environ.get('V111_RESUME'),scope='Actual field/map/topic/record clicks; starts new or resumes an actual prior-play save. Only text speed preference changed.')
   (OUT/(('smoke' if os.environ.get('V111_SMOKE') else route)+'-report.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASSED',route,flush=True)
  except Exception:
   try:await q.py('import renpy;renpy.exports.save("v111-harness-recovery");result=True');await asyncio.sleep(1)
   except Exception:pass
   await pg.screenshot(path=str(OUT/(route+'-failure.png')));(OUT/(route+'-events.json')).write_text(json.dumps(events,ensure_ascii=False,indent=2));raise
  finally:await b.close()
if __name__=="__main__":asyncio.run(main())
