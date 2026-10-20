"""Natural V1.1.1 play through existing Room13 field, map, topics and notebook."""
import asyncio,json,os,ast,time
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
ROOT=Path(__file__).resolve().parents[1];OUT=Path(os.environ.get('ROOM13_QA_OUT','/workspace/work/v111/browser'));OUT.mkdir(parents=True,exist_ok=True)
PLAN=json.loads((ROOT/'docs/story-v111/compiled-reference.json').read_text());PROOFS={v['title']:v for v in PLAN.values() if v['kind']=='proof'}
class Fast(UIQA):
 async def input(self,x,y):
  vp=self.p.viewport_size;s=min(vp['width']/1280,vp['height']/720);x=(vp['width']-1280*s)/2+x*s;y=(vp['height']-720*s)/2+y*s
  await self.p.mouse.click(x,y);await asyncio.sleep(.08)
 async def value(self,value):
  await asyncio.sleep(.5);return await super().value(value)
 async def press(self,label):
  for _ in range(40):
   st=await self.state();bs=[b for b in st['buttons'] if label in b['text'] and b['rect'][3]>12]
   if bs:
    b=min(bs,key=lambda b:b['rect'][2]*b['rect'][3]);x,y,w,h=b['rect'];await self.input(x+w/2,y+h/2);return
   await asyncio.sleep(.1)
  raise AssertionError((label,st))

async def main():
 route=os.environ.get('V111_ROUTE','shelter');stone=int(os.environ.get('V111_STONE','0'));custody=int(os.environ.get('V111_CUSTODY','0'))
 async with async_playwright() as p:
  b=await p.chromium.launch_persistent_context(str(OUT/('profile-'+os.environ.get('V111_PROFILE',route))),executable_path='/usr/bin/chromium',viewport={'width':1280,'height':720},args=['--no-sandbox','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])

  for previous in b.pages:await previous.close()
  pg=await b.new_page();q=Fast(pg,OUT);errors=[];pg.on('pageerror',lambda e:errors.append(str(e)));events=[];shots=set()
  async def snap():
   return await q.py('import renpy;s=renpy.store;result=dict(screens=[n for n in ("main_menu","say","choice","r13_confirm","r13_hub","r13_topics","r13_map","r13_book","r13_crisis_proof","_exception") if renpy.display.screen.get_screen(n)],gate=(s.room13 or {}).get("v111",{}).get("gate"),choice=getattr(s,"v111_menu_owner",None),claim=getattr(s,"v111_claim",None),binding=s.r13_v111_binding() if s.r13_v111_active() else {},values=(s.room13 or {}).get("v111",{}).get("values",{}),evidence=(s.room13 or {}).get("evidence",[]),location=(s.room13 or {}).get("location"),music=renpy.audio.music.get_playing())')
  try:
   await pg.goto(os.environ.get('ROOM13_URL','http://localhost:8766/preview/room13-dev/'),wait_until='domcontentloaded',timeout=180000)
   await pg.wait_for_function("typeof renpy_exec==='function'",timeout=180000);await asyncio.sleep(12);await q.input(1100,600);await q.wait('main_menu')
   await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True')
   if os.environ.get('V111_RESUME'):
    code='import renpy;renpy.exports.load('+repr(os.environ['V111_RESUME'])+')'
    await pg.evaluate('code=>{renpy_exec("exec("+JSON.stringify(code)+")").catch(()=>{});return true;}',code)
    await asyncio.sleep(3)
    await pg.evaluate("window._renpy_cmd_callback({data:true})")
   else:await q.press('처음부터')
   wrong_probe=0;proof_keys=[];book_target=None;last=None;checkpoints=set();object_attempts={}
   for step in range(4500):
    st=await snap();sc=st['screens'];assert '_exception' not in sc,st
    state=(st['gate'],tuple(sc),st['choice'],st['claim'])
    if state!=last:events.append(dict(step=step,**st));last=state;print('STATE',step,st['gate'],sc,st['choice'],st['location'],flush=True)
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
     await q.input(900,590);continue
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
      name=await q.py('import renpy;result=renpy.store.ROOM13["evidence"]['+repr(book_target)+']["name"]')
      try:await q.press(name)
      except AssertionError:
       paging=await q.py('import renpy;s=renpy.store;c=renpy.display.screen.get_screen("r13_book").scope;e=c["entries"];result=[e.index('+repr(book_target)+')//s.r13_record_page_size(),s.r13_record_page(e,c["page"])]')
       await q.press('이전' if paging[0]<paging[1] else '다음');continue
      await q.press('보여주기');book_target=None
     else:await q.press('그만두기')
     continue
    if 'r13_topics' in sc:
     options=st['binding']['options'];person=await q.py('import renpy;result=renpy.display.screen.get_screen("r13_topics").scope["person"]')
     eligible=[o for o in options if o.get('person')==person]
     gate=st['gate']
     preferred={'gate_investigate':5,'gate_choice':1,'registered_menu':1,'post_menu':1}.get(gate)
     option=next((o for o in eligible if o.get('index')==preferred),eligible[0])
     await q.press(option['title']);continue
    if 'r13_map' in sc:
     target=next(o.get('move') for o in st['binding']['options'] if o.get('move'))
     region='inn' if target in ('inn','room13','dining') else 'mountain' if target=='forest' else 'village'
     await q.press({'inn':'여관 안','mountain':'숲·산길','village':'마을'}[region]);await q.value(target)
     if 'r13_map' in (await snap())['screens']:await q.press('이곳으로 이동')
     continue
    if 'r13_hub' in sc:
     gate=st['gate']
     if gate in ('sleep1','box_inspect','post_menu','lamp_observe','sleep2','lamp_inspect3','loan_read','sale_check','sleep3') and gate not in checkpoints:
      slot='v111-'+gate
      await q.py('import renpy;renpy.exports.save('+repr(slot)+');result=True');checkpoints.add(gate)
      print('SAVED',slot,flush=True)
     gate=st['gate'];options=st['binding'].get('options',[])
     if gate not in shots and gate in ('gate_investigate','box_inspect','afternoon','sleep2','piko_clean','lamp_inspect3','measurement_read','sleep3'):
      await q.shot(route+'-'+gate);shots.add(gate)
     if gate=='gate_investigate':idx=0 if 'V111:E03' not in st['evidence'] else 1 if 'V111:E04' not in st['evidence'] else 5;option=next(o for o in options if o['index']==idx)
     elif gate=='lamp_observe':idx=next(i for i in range(4) if not st['values'].get('lamp_part_'+str(i)));option=next(o for o in options if o['index']==idx)
     elif gate=='registered_menu':option=next(o for o in options if o.get('move'))
     else:option=options[0]
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
      fx,fy=((.5,.5),(.2,.8),(.8,.8),(.2,.2),(.8,.2))[attempt%5]
      pos=await q.py('import renpy;s=renpy.store;x,y,w,h=s.ROOM13["objects"][s.room13["location"]]['+repr(obj)+']["rect"];result=[x+w*'+str(fx)+'-s.r13_world_offset(),y+h*'+str(fy)+']')
      if not 0<pos[0]<1280:
       direction=-1 if pos[0]<0 else 1
       await q.press('‹' if direction<0 else '›');await asyncio.sleep(.6);continue
      await q.input(*pos);continue
    await asyncio.sleep(.1)
   else:raise AssertionError(('Play did not complete',st))
   assert not errors,errors
   report=dict(status='passed',route=route,stone=stone,custody=custody,final=st,events=events,page_errors=errors,wrong_proof_recovered=(wrong_probe==2),resume=os.environ.get('V111_RESUME'),scope='Actual field/map/topic/record clicks; starts new or resumes an actual prior-play save. Only text speed preference changed.')
   (OUT/(route+'-report.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASSED',route,flush=True)
  except Exception:
   await pg.screenshot(path=str(OUT/(route+'-failure.png')));(OUT/(route+'-events.json')).write_text(json.dumps(events,ensure_ascii=False,indent=2));raise
  finally:await b.close()
asyncio.run(main())
