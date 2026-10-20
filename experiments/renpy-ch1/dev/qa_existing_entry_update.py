import asyncio,json,sys,os
from pathlib import Path
from playwright.async_api import async_playwright
sys.path.insert(0,str(Path(__file__).resolve().parent))
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'))/'existing-entry';OUT.mkdir(exist_ok=True)
AUDIO="""(()=>{window.__audioAnalysers=[];let orig=AudioNode.prototype.connect;AudioNode.prototype.connect=function(dest,...args){if(dest instanceof AudioDestinationNode){const a=this.context.createAnalyser();a.fftSize=2048;orig.call(a,dest);window.__audioAnalysers.push(a);return orig.call(this,a,...args);}return orig.call(this,dest,...args);};})()"""
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/usr/bin/chromium'),ignore_default_args=['--mute-audio'],args=['--no-sandbox','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
  c=await b.new_context(viewport={'width':1280,'height':720});await c.add_init_script(AUDIO);pg=await c.new_page();q=UIQA(pg,OUT);report={'checks':[]};errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
  try:
   await pg.goto(os.environ.get('ROOM13_URL','http://localhost:8765/preview/room13-dev/'))
   await pg.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu')
   await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True')
   await q.press('처음부터');await q.wait('say');await q.shot('01-existing-carriage')
   before=await q.py('import renpy;s=renpy.store;result=dict(ms14=s.ms14,music=renpy.audio.music.get_playing(),scene=s.r13_scene_key,place=s.place)')
   assert before['ms14'] is None and before['music'] and before['place']=='마차 안',before
   await q.advance();await q.wait('r13_hub');await q.shot('02-existing-gate-click-scene')
   gate=await q.py('import renpy;s=renpy.store;result=dict(ms14=s.ms14,music=renpy.audio.music.get_playing(),ambience=renpy.audio.music.get_playing(channel="ambience"),actors=[a["person"] for a in s.r13_stage_people(True)],location=s.room13["location"],evidence=s.room13["evidence"])')
   assert gate['ms14'] is None and gate['location']=='gate' and {'guard','karo','daram'}<=set(gate['actors']),gate
   assert gate['music']=='assets/bgm-snow.mp3' and gate['ambience']=='assets/amb-wind.mp3',gate
   samples=[]
   for _ in range(8):
    samples+=await pg.evaluate('()=>window.__audioAnalysers.map(a=>{let v=new Float32Array(a.fftSize);a.getFloatTimeDomainData(v);return Math.sqrt(v.reduce((s,x)=>s+x*x,0)/v.length)})');await asyncio.sleep(.2)
   assert max(samples or [0])>.00001,('no audio output',samples)
   report['audio_rms_peak']=max(samples);report['checks'].append('Original scene music and ambience play and produce a nonzero WebAudio signal')
   await q.value(('person','guard'));await q.wait('r13_entry_topics');await q.shot('03-original-guard-questions')
   await q.press('제가 낸 신청서');await q.advance();await q.wait('r13_entry_topics')
   room=(await q.state())['room'];assert 'G3' in room['evidence'] and 'entry_corrected' not in room['flags'],room
   await q.press('자료 보여주기');await q.wait('r13_book');await q.shot('04-original-notebook');await q.press('그만두기');await q.advance();await q.wait('r13_entry_topics')
   assert (await q.state())['room']==room,'Cancel changed story state'
   await q.press('돌아가기');await q.wait('r13_hub')
   async def object_click(key):
    pos=await q.py('import renpy;s=renpy.store;x,y,w,h=s.ROOM13["objects"]["gate"]['+repr(key)+']["rect"];result=[x+w/2-s.r13_world_offset(),y+h/2]')
    assert 0<pos[0]<1280,pos
    await q.input(*pos);await q.advance();await q.wait('r13_hub')
   await object_click('gate_documents');await q.shot('05-clicked-shelf-new-original')
   assert 'G1' in (await q.state())['room']['evidence']
   await object_click('rules');await q.shot('06-clicked-rules')
   assert 'G2' in (await q.state())['room']['evidence']
   await q.value(('person','guard'));await q.wait('r13_entry_topics')
   await q.press('자료 보여주기');await q.wait('r13_book')
   title=await q.py('import renpy;result=renpy.store.R13_RECORD_SHORT["G1"]')
   await q.press(title);await q.shot('07-new-evidence-existing-book');await q.press('돌목에게 보여주기');await q.advance();await q.wait('r13_hub')
   end=(await q.state())['room'];assert 'entry_corrected' in end['flags'],end
   await q.shot('08-existing-engine-after-presentation')
   report.update(status='passed',opening=before,gate=gate,final_location=end['location'],page_errors=errors,scope='Natural start and real clicks only; game-state probes are read-only except text speed preference')
  except Exception as e:
   report.update(status='failed',error=repr(e));await pg.screenshot(path=str(OUT/'failure.png'))
   try:(OUT/'failure-state.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
   except:pass
  (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
  if report['status']!='passed':raise SystemExit(1)
asyncio.run(main())
