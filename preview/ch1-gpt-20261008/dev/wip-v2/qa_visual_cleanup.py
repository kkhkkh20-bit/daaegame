"""Production wrapper: actual admin entries, source-pixel feet and face visibility.

No progress/lines are injected. PNG alpha is read without editing images.
--slow delays the family atlas decode Promise after its real PNG has loaded.
This simulates late art readiness without modifying game state or image pixels.
"""
import argparse
import asyncio
import json
import shutil
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

TRACE=r'''(()=>{const report={faces:0,dad:0,pending:0,cards:0,bad:[]};window.__qaVisualCleanup=report;
function tick(){try{
 const sp=document.querySelector('#vnbox .spk9'),im=sp&&sp.querySelector('img');
 if(sp&&im&&sp.dataset.k?.endsWith('|img')){
  const css=getComputedStyle(sp),r=sp.getBoundingClientRect(),visible=css.visibility==='visible'&&css.display!=='none'&&r.width>0;
  if(sp.classList.contains('loading'))report.pending++;
  if(visible){
   if(!im.complete||!im.naturalWidth){if(report.bad.length<5)report.bad.push('Visible empty portrait: '+sp.dataset.k)}
   else{const ir=im.getBoundingClientRect(),c=document.createElement('canvas');c.width=c.height=16;const ctx=c.getContext('2d');
    ctx.drawImage(im,(r.left-ir.left)/ir.width*im.naturalWidth,(r.top-ir.top)/ir.height*im.naturalHeight,r.width/ir.width*im.naturalWidth,r.height/ir.height*im.naturalHeight,0,0,16,16);
    const data=ctx.getImageData(0,0,16,16).data;let opaque=0;for(let i=3;i<data.length;i+=4)if(data[i]>32)opaque++;
    if(opaque<40&&report.bad.length<5)report.bad.push('Empty source-pixel face crop: '+sp.dataset.k);
    report.faces++;if(sp.dataset.k.startsWith('det0|'))report.dad++;
   }
  }
 }
 const b=document.querySelector('.banner.inn-place-panel');if(b){report.cards++;const mid=b.querySelector('.mid'),r=mid.getBoundingClientRect();
  if((b.querySelector('.bar1,.bar2,.mid b span')||r.width>Math.min(420,innerWidth-20)||r.height>130)&&report.bad.length<5)report.bad.push('Legacy or oversized place banner');
 }
}catch(e){if(report.bad.length<5)report.bad.push(String(e))}requestAnimationFrame(tick)}requestAnimationFrame(tick)})();'''

LATE_DECODE=r'''(()=>{const native=Image.prototype.decode;
Image.prototype.decode=function(){const done=native.call(this);
return /\/art\/ch1\/dialogue-v2\/family\.png(?:[?#]|$)/.test(this.src)
 ?done.then(()=>new Promise(resolve=>setTimeout(resolve,40000))):done};})();'''

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--url',required=True);ap.add_argument('--version',required=True)
ap.add_argument('--slow',action='store_true');ap.add_argument('--output',default='/tmp/visual-cleanup')
args=ap.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
root=Path(__file__).resolve().parents[2]
async def main():
  async with async_playwright() as p:
    browser=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    context=await browser.new_context(viewport={'width':844,'height':390});await context.add_init_script(TRACE)
    if args.slow:
        await context.add_init_script(LATE_DECODE)
    page=await context.new_page();errors=[];bad=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
    await page.goto(args.url,wait_until='domcontentloaded');frame=page.frame_locator('#game')
    inner=await (await page.locator('#game').element_handle()).content_frame()
    await frame.locator('#innmain [data-m="set"]').click(timeout=45000)
    await frame.locator('#innopt [data-admin-open]').click()
    print('INFO native admin opened; family decode delay '+('40s' if args.slow else 'off'),flush=True)
    slow_pending=0
    # The night camera deliberately gates input until its world art is ready.
    # Carriage CG is independent of the speaker atlas, so actual dialogue there
    # exercises a pending portrait without disabling the normal camera guard.
    if args.slow:
        await frame.locator('[data-admin-scene="carriage"]').click(timeout=45000,no_wait_after=True)
        await inner.wait_for_url('**/*testScene=carriage*',wait_until='domcontentloaded',timeout=45000)
        await frame.locator('#inn-story-cg.ready').wait_for(timeout=45000)
        print('INFO native carriage CG ready; checking pending speaker pixels',flush=True)
        for _ in range(30):
            if await inner.evaluate('__qaVisualCleanup.pending>0'):break
            await frame.locator('#vnbox .vtxt').first.click()
            await page.wait_for_timeout(180)
        await inner.wait_for_function('__qaVisualCleanup.pending>0',timeout=1000)
        pending_trace=await inner.evaluate('__qaVisualCleanup')
        assert not pending_trace['bad'],pending_trace
        slow_pending=pending_trace['pending']
        print('PASS actual pending portrait hidden; no visible empty face',flush=True)
        await page.screenshot(path=str(out/'pending-portrait.png'))
        await inner.wait_for_function('__innDialogueArtReady(__innDialogueManifest.world.det1.src)',timeout=45000)
        await frame.locator('#inn-admin-status [data-admin-open]').click()
    await frame.locator('[data-admin-scene="night"]').click(timeout=45000)
    await frame.locator('#inn-night-walk.ready').wait_for(timeout=45000)
    assert 'build='+args.version in inner.url and await inner.evaluate('typeof __T')=='undefined'
    art=await inner.evaluate('__innDialogueManifest.world.det1')
    im=Image.open(root/art['src']);x,y,w,h=art['crop']
    alpha=im.getchannel('A').crop((x,y,x+w,y+h)).point(lambda v:255 if v>=32 else 0).getbbox()
    opaque=[x+alpha[0],y+alpha[1],x+alpha[2],y+alpha[3]]
    checks=[]
    for width,height in [(844,390),(390,844),(640,360),(1280,720)]:
        await page.set_viewport_size({'width':width,'height':height});await page.wait_for_timeout(350)
        result=await inner.evaluate('''({opaque})=>{const s=document.querySelector('#inn-night-walk svg[data-surface="room"]'),m=s.getScreenCTM(),p=document.querySelector('#vnbox .vtxt').getBoundingClientRect();
         function project(x,y){return new DOMPoint(x,y).matrixTransform(m)}const a=project(opaque[0],opaque[1]),z=project(opaque[2],opaque[3]);
         return {src:s.querySelector('image').getAttribute('href'),crop:s.getAttribute('viewBox'),body:{left:a.x,top:a.y,right:z.x,bottom:z.y},plate:p.toJSON(),W:innerWidth,H:innerHeight}}''',{'opaque':opaque})
        assert result['src']==art['src'] and [float(v) for v in result['crop'].split()]==art['crop'],result
        body=result['body'];assert 0<=body['left']<body['right']<=result['W'],result
        assert 0<=body['top']<body['bottom']<=result['plate']['top']-10,result
        await page.screenshot(path=str(out/f'full-body-{width}.png'));checks.append(result)
    trace=await inner.evaluate('__qaVisualCleanup');assert not trace['bad'],trace
    assert trace['cards']>0,'Native place/time card was not exercised'
    print('PASS full-body source pixels/feet above dialogue at four wrapper sizes; compact native place card',flush=True)
    await page.set_viewport_size({'width':390,'height':844})
    await frame.locator('#inn-admin-status [data-admin-open]').click()
    await frame.locator('[data-admin-scene="carriage"]').click(timeout=45000)
    await frame.locator('#inn-story-cg.ready').wait_for(timeout=45000)
    if args.slow:
        await inner.wait_for_function('__innDialogueArtReady(__innDialogueManifest.world.det1.src)',timeout=45000)
    for turn in range(65):
        if await frame.locator('#vnbox .spk9[data-k="det0|img"]:visible').count():break
        if await frame.locator('#vnbox .vtxt').count():await frame.locator('#vnbox .vtxt').first.click()
        await page.wait_for_timeout(180)
    await frame.locator('#vnbox .spk9[data-k="det0|img"]:visible').wait_for(timeout=45000)
    await page.wait_for_timeout(500);trace=await inner.evaluate('__qaVisualCleanup')
    assert trace['faces']>0 and trace['dad']>0 and not trace['bad'],trace
    if args.slow:assert slow_pending>0,('Slow loading case never reached a pending portrait',trace)
    assert not errors,errors;assert not bad,bad
    await page.screenshot(path=str(out/'father-portrait.png'))
    (out/'result.json').write_text(json.dumps({'sizes':checks,'faceTrace':trace,'slow':args.slow,'pendingPortraitFrames':slow_pending,'errors':errors,'bad':bad},ensure_ascii=False))
    print('PASS visible father face pixels, loading visibility, actual native dialogue; JS/HTTP0',flush=True)
    await browser.close()

asyncio.run(main())
