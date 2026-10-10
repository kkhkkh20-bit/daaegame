"""Prepared native actor geometry QA; authored dialogue and native talk renderer.
This tests screen layout, not a complete fresh prologue/investigation playthrough.
"""
import argparse,json,shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
CAST=['nabi','karo','doto','buri','seryeon','innma','wanggu','geokkuri','det1']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--url',default='http://127.0.0.1:8000/playT.html');ap.add_argument('--out',default='/tmp/actor-frame-direction');args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True);report=[]
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox']);page=b.new_page(viewport={'width':844,'height':390});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(args.url,wait_until='domcontentloaded');page.wait_for_timeout(16000)
  def e(s):return page.evaluate('(s)=>__T(s)',s)
  e('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};');page.evaluate('document.querySelector("#innmain").remove();__w209boot()');page.wait_for_timeout(1500)
  assert page.evaluate('typeof __innSetActorFrame==="function"'),'Build has previous oversized geometry'
  rows=page.evaluate('''()=>{let out=[];function walk(o){if(!o||typeof o!=='object')return;if(Array.isArray(o)&&typeof o[0]==='string'&&typeof o[1]==='string'){out.push(o);return}Object.values(o).forEach(walk)}walk(EP1INN);return out}''')
  def inspect(selector,k,surface):
   state=page.locator(selector).first.evaluate('''(im,args)=>{const [k,surface]=args,s=im.getAttribute('src'),r=im.getBoundingClientRect(),panel=document.querySelector('.fstalk .tpanel'),p=panel&&panel.getBoundingClientRect(),f=__innFrame(k,s,surface==='talk'?{surface,panel:p}:null),a=f.opaque;return {k,surface,src:s,natural:[im.naturalWidth,im.naturalHeight],rect:r.toJSON(),frame:f,loaded:im.complete&&im.naturalWidth>0,render:getComputedStyle(im).imageRendering,alpha:{left:r.left+a[0]*f.scale,top:r.top+a[1]*f.scale,right:r.left+a[2]*f.scale,bottom:r.top+a[3]*f.scale},plate:document.querySelector('#vnbox .vtxt')?.getBoundingClientRect().top,panel:p?.toJSON()}}''',[k,surface])
   assert state['loaded'],state;f=state['frame'];r=state['rect'];a=state['alpha'];assert abs(r['width']/r['height']-state['natural'][0]/state['natural'][1])<.02,state;assert state['render'] in ['pixelated','crisp-edges'],state
   assert a['left']>=-2 and a['right']<=page.viewport_size['width']+2,state
   if k=='geokkuri':assert abs(a['top'])<=2,state
   else:assert a['top']>=42,state
   if max(state['natural'])<=256:assert f['scale']<=1.751,state
   if surface=='stage':assert a['bottom']<=state['plate']-7,state
   elif state['panel'] and state['panel']['left']>page.viewport_size['width']*.3:assert a['right']<=state['panel']['left']-10,state
   report.append(state);return state
  for w,h in [(844,390),(390,844),(1280,720)]:
   page.set_viewport_size({'width':w,'height':h})
   for k in CAST:
    row=next(r for r in rows if r[0]==k);e('if(DL){DL.done=null;endDlg()};G.tab="scene";render();say('+json.dumps([['@dir','who:'+k+';chime:0;ms:80'],row],ensure_ascii=False)+',null);');page.wait_for_timeout(650);inspect('#innstage .isf img',k,'stage')
    if k in ['nabi','wanggu','geokkuri','det1']:page.screenshot(path=str(out/f'{w}-stage-{k}.png'))
   for k in CAST[:-1]:
    e('if(DL){DL.done=null;endDlg()};G.who='+json.dumps(k)+';G.tab="talk";render();');page.wait_for_timeout(800);inspect('.fstalk .tfig img',k,'talk')
    if k in ['nabi','wanggu']:page.screenshot(path=str(out/f'{w}-talk-{k}.png'))
   print('PASS geometry',w,h,'9 authored stage actors / 8 native question actors',flush=True)
  # Explicit mood fixtures use an authored utterance with its mood replaced;
  # they exercise the production source selector, speaker crop and native seats.
  page.set_viewport_size({'width':844,'height':390});base=next(r for r in rows if r[0]=='wanggu')
  for name,md in [('default','think'),('admonish','admonish'),('angry','angry'),('sheepish','sheepish')]:
   row=base.copy()
   while len(row)<7:row.append(None)
   row[2]=md;row[6]=md;expected='art/ch1/neoul-v4/neoul-'+name+'.png'
   e('if(DL){DL.done=null;endDlg()};G.tab="scene";render();say('+json.dumps([['@dir','who:wanggu;chime:0;ms:80'],row],ensure_ascii=False)+',null);');page.wait_for_timeout(800)
   state=inspect('#innstage .isf img','wanggu','stage');assert state['src']==expected,state
   assert page.locator('#vnbox .spk9 img').get_attribute('src')==expected,'Speaker and body Neoul diverge'
   page.screenshot(path=str(out/f'v4-stage-{name}.png'))
   council={'w':'wanggu','t':base[1],'m':md}
   e('if(DL){DL.done=null;endDlg()};__rtgReset();document.querySelectorAll("body>.rt").forEach(x=>x.remove());__inMeeting=false;__rtOpen(CASES[G.ci],{key:"qaNeoulV4",title:"QA",seats:EP1INN.MEET.seats,phases:[{type:"talk",lines:['+json.dumps(council,ensure_ascii=False)+']}]});')
   page.wait_for_function('(t)=>document.querySelector("body>.rt #rtnext .rt-bub p")?.textContent===t',arg=base[1],timeout=12000);page.wait_for_timeout(650)
   seat=page.locator('#rtg .seat[data-k="wanggu"] svg[data-face="wanggu"]');assert seat.count()==1,'Native Neoul face crop missing'
   assert seat.get_attribute('viewBox')=='180 60 600 600';assert seat.locator('image').get_attribute('href')==expected
   page.screenshot(path=str(out/f'v4-council-{name}.png'));print('PASS v4 native mood/body/speaker/council',name,flush=True)
   e('__rtgReset();document.querySelectorAll("body>.rt").forEach(x=>x.remove());__inMeeting=false;')
  # Actual world painter prewarms the same native hit cache before any input.
  e('if(DL){DL.done=null;endDlg()};G.loc=CASES[G.ci].locations.findIndex(l=>l.id==="front");G.tab="scene";render();');page.wait_for_timeout(1600)
  src='art/ch1/neoul-v4/neoul-default.png';assert page.evaluate('__innMask()')[src]=='ok','New Neoul native mask not ready before input'
  im=page.locator('#bigscene image.wn9[data-k="wanggu"]');assert im.get_attribute('href')==src;rect=im.bounding_box();assert rect
  raw=Image.open(Path(__file__).resolve().parents[2]/src).convert('RGBA');alpha=raw.getchannel('A');nw,nh=raw.size
  clear=next((x,y) for y in range(110,450,12) for x in range(330,680,12) if alpha.crop((x-4,y-4,x+5,y+5)).getextrema()[1]==0)
  solid=next((x,y) for y in range(350,750,20) for x in range(400,650,20) if alpha.crop((x-4,y-4,x+5,y+5)).getextrema()[0]>200)
  def point(px):return {'x':rect['x']+px[0]/nw*rect['width'],'y':rect['y']+px[1]/nh*rect['height']}
  empty,hit=point(clear),point(solid)
  assert page.evaluate('(p)=>__innNpcHit(p.x,p.y)',empty)=='','Transparent upper pixels accepted as Neoul'
  assert page.evaluate('(p)=>__innNpcHit(p.x,p.y)',hit)=='wanggu','Actual opaque Neoul pixels rejected'
  page.mouse.click(empty['x'],empty['y']);page.wait_for_timeout(300);assert e('G.tab')=='scene','Transparent body canvas opened NPC'
  e('if(DL){DL.done=null;endDlg()};');page.wait_for_timeout(1000);page.screenshot(path=str(out/'v4-world-front.png'))
  assert 0<hit['x']<844 and 0<hit['y']<390,hit
  page.mouse.click(hit['x'],hit['y']);page.wait_for_timeout(900);assert e('G.tab')=='talk' and e('G.who')=='wanggu','Actual opaque-pointer failed to open Neoul questions'
  assert '/neoul-v4/' in page.locator('.fstalk .tfig img').get_attribute('src');print('PASS v4 native prewarmed alpha cache, transparent reject, actual opaque pointer opens questions',flush=True)
  assert all('/neoul-v4/' in r['src'] for r in report if r['k']=='wanggu'),'Old Neoul source remains'
  assert not errors,errors
  # Independently measure actual PNG alpha, rather than trusting frame metadata.
  measured={}
  for state in report:
   src=state['src'].split('?')[0]
   if src not in measured:
    im=Image.open(Path(__file__).resolve().parents[2]/src).convert('RGBA');measured[src]=(list(im.size),list(im.getchannel('A').point(lambda a:255 if a>=32 else 0).getbbox()))
   natural,alpha=measured[src];assert state['frame']['canvas']==natural and state['frame']['opaque']==alpha,('Actual PNG differs from frame metadata',src,alpha,state['frame'])
  print('PASS independent native PNG canvas/opaque alpha',len(measured),'sources',flush=True)
  (out/'geometry.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('PASS actor whole/medium bounds, pixel rendering, native upscale, question separation JS0',flush=True);b.close()
if __name__=='__main__':main()
