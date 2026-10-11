"""Prepared native dialogue/question layout checks, not a fresh story walkthrough.

Check the separate raw atlases, actual viewport bounds, native question repaint,
expression changes, and old room/council assets staying separate.
"""
import argparse,json,shutil
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

CAST=['det1','innma','seryeon','nabi','geokkuri','doto','buri','karo','wanggu']
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--url',default='http://127.0.0.1:8000/playT.html');ap.add_argument('--out',default='/tmp/dialogue-portraits');a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 root=Path(__file__).resolve().parents[2];manifest=json.loads((root/'art/ch1/dialogue-v1/manifest.json').read_text());chars=manifest['characters'];assert set(chars)==set(CAST+['det0'])
 for k,states in chars.items():
  assert set(states)=={'neutral','thinking','distressed','expressive'},(k,states.keys())
  for state,v in states.items():
   im=Image.open(root/v['src']);assert list(im.size)==[v['width'],v['height']]
   assert im.mode=='RGBA' and im.getchannel('A').getextrema()[0]==0,(k,state,'No transparency')
   x,y,w,h=v['crop'];fx,fy,fs=v['face'];assert 0<=x<x+w<=im.width and 0<=y<y+h<=im.height,(k,state,v)
   assert x<=fx<fx+fs<=x+w and y<=fy<fy+fs<=y+h,(k,state,'Face crosses another cell',v)
   assert im.getchannel('A').crop((x,y,x+w,y+h)).getbbox(),(k,state,'Empty crop')
 print('PASS 10 characters / 40 distinct cell and face crops, actual PNG alpha/canvas',flush=True)
 report=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox']);page=browser.new_page(viewport={'width':844,'height':390});errors=[];bad=[]
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
  page.goto(a.url,wait_until='domcontentloaded');page.wait_for_timeout(16000)
  def e(s):return page.evaluate('(s)=>__T(s)',s)
  e('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};');page.evaluate('document.querySelector("#innmain").remove();__w209boot()');page.wait_for_timeout(1200)
  page.wait_for_function('__innDialogueState().assets.length===5&&__innDialogueState().assets.every(a=>a.ready)')
  rows=page.evaluate("""()=>{let out=[];function walk(o){if(!o||typeof o!=='object')return;if(Array.isArray(o)&&typeof o[0]==='string'&&typeof o[1]==='string'){out.push(o);return}Object.values(o).forEach(walk)}walk(EP1INN);return out}""")
  def stage(k,md=''):
   row=next(r for r in rows if r[0]==k).copy()
   while len(row)<7:row.append(None)
   row[2]=md;row[6]=md
   e('if(DL){DL.done=null;endDlg()};G.tab="scene";render();say('+json.dumps([['@dir','who:'+('det1' if k=='det0' else k)+';chime:0;ms:40'],row],ensure_ascii=False)+',null);');page.wait_for_timeout(250)
  def inspect(k,surface):
   sel='#innstage .isf>svg.dialogue-bust' if surface=='stage' else '.fstalk .tfig>svg.dialogue-bust'
   svg=page.locator(sel);assert svg.count()==1,(k,surface,'Not one close dialogue actor')
   r=svg.evaluate("""n=>({k:n.dataset.k,src:n.dataset.src,expression:n.dataset.expression,rect:n.getBoundingClientRect().toJSON(),render:getComputedStyle(n).imageRendering,overflow:getComputedStyle(n).overflow,view:n.getAttribute('viewBox'),panel:document.querySelector('.fstalk .tpanel')?.getBoundingClientRect().toJSON(),host:n.parentNode.dataset.posture})""")
   assert r['k']==k and '/dialogue-v1/' in r['src'],r
   assert r['render']=='pixelated' and r['overflow']=='hidden',r
   rect=r['rect'];v=[float(x) for x in r['view'].split()];assert abs(rect['width']/rect['height']-v[2]/v[3])<.025,r
   assert rect['left']>=0 and rect['right']<=page.viewport_size['width']+1,r
   assert rect['top']>=0 and rect['bottom']<=page.viewport_size['height']+1,r
   if surface=='talk' and r['panel']['left']>page.viewport_size['width']*.3:assert rect['right']<r['panel']['left']-10,r
   assert r['host']==('dialogue-hanging' if k=='geokkuri' else 'dialogue-bust'),r
   assert not svg.locator('..').locator(':scope>img,:scope>.cm-layer').count(),'Old full-body/motion layer overlaps bust'
   report.append(r);return r
  for w,h in [(844,390),(390,844)]:
   page.set_viewport_size({'width':w,'height':h})
   for k in CAST:
    stage(k);inspect(k,'stage');page.screenshot(path=str(out/f'{w}-stage-{k}.png'))
   for k in CAST[1:]:
    e('if(DL){DL.done=null;endDlg()};G.who='+json.dumps(k)+';G.tab="talk";render();');page.wait_for_timeout(450);inspect(k,'talk')
   print('PASS',w,h,'9 native stage actors / 8 native question actors, no old sprite overlap',flush=True)
  page.set_viewport_size({'width':844,'height':390})
  for k in CAST+['det0']:
   coords=set()
   for md in ['normal', 'think' if k!='wanggu' else 'admonish','worried' if k!='wanggu' else 'sheepish','angry' if k in ['wanggu','karo','seryeon'] else 'joy']:
    stage(k,md);face=page.locator('#vnbox .spk9 img');assert '/dialogue-v1/' in face.get_attribute('src'),(k,md,'Speaker uses old face')
    coords.add(face.get_attribute('style'));expected=page.evaluate('(v)=>__innDialogueArt(v.k,v.md).crop',{ 'k':k,'md':md})
    if k!='det0':assert [float(x) for x in page.locator('#innstage .dialogue-bust').get_attribute('viewBox').split()]==expected,(k,md)
   assert len(coords)==4,(k,'Speaker crop does not follow four expressions')
  print('PASS 40 native utterance expression/speaker changes, father stays first-person',flush=True)
  # Real authored utterances isolate resident -> child -> resident. Advance
  # through the native Enter handlers and inspect every painted question frame.
  e('if(DL){DL.done=null;endDlg()};G.who="wanggu";G.tab="talk";render();var topic=EP1INN.TALK.wanggu.find(t=>t.id==="T_ne3");say([topic.lines[1],topic.lines[4],topic.lines[5]],null);')
  page.wait_for_timeout(100)
  e('window.__qaTalkFrames=[];window.__qaTalkOn=true;(function sample(){if(!window.__qaTalkOn)return;var host=document.querySelector(".fstalk .tfig"),svg=host&&host.querySelector("svg.dialogue-bust");window.__qaTalkFrames.push({i:DL&&DL.i,who:DL&&DL.lines[DL.i][0],old:!!(host&&host.querySelector("img")),bust:!!svg,expression:svg&&svg.dataset.expression});requestAnimationFrame(sample)})()')
  for _ in range(45):
   if not e('!!DL'):break
   page.keyboard.press('Enter');page.wait_for_timeout(110)
  e('window.__qaTalkOn=false');frames=page.evaluate('__qaTalkFrames');assert frames and not any(f['old'] or not f['bust'] for f in frames),frames
  child=[f for f in frames if f['who']=='det1'];assert child and all(f['expression']=='thinking' for f in child),child
  print('PASS authored question reply -> child keeps counterpart expression, no old full-body frame',flush=True)
  e('if(DL){DL.done=null;endDlg()};G.loc=CASES[G.ci].locations.findIndex(l=>l.id==="front");G.tab="scene";render();');page.wait_for_timeout(800)
  world=page.locator('#bigscene image.wn9[data-k="wanggu"]');assert '/neoul-v4/' in world.get_attribute('href'),'World was replaced with close bust'
  page.screenshot(path=str(out/'world-front.png'))
  page.wait_for_function('__innMask()["art/ch1/neoul-v4/neoul-default.png"]==="ok"');rect=world.bounding_box();raw=Image.open(root/'art/ch1/neoul-v4/neoul-default.png');alpha=raw.getchannel('A');nw,nh=raw.size
  points=[(rect['x']+x/nw*rect['width'],rect['y']+y/nh*rect['height']) for y in range(350,750,20) for x in range(400,650,20) if alpha.getpixel((x,y))>200]
  x,y=next((x,y) for x,y in points if 5<x<839 and 5<y<385);page.mouse.click(x,y);page.wait_for_timeout(800)
  assert e('G.tab==="talk"&&G.who==="wanggu"'),'Actual opaque pointer failed to open questions';inspect('wanggu','talk');page.screenshot(path=str(out/'talk-front.png'))
  print('PASS real opaque world pointer opens separate close dialogue atlas',flush=True)
  assert not errors,errors;assert not bad,bad
  (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('PASS separate native world art, JS/HTTP0',flush=True);browser.close()
if __name__=='__main__':main()
