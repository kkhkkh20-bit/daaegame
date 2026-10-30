"""1일 마차~입구를 줄마다 두 번 찍어(넘긴 직후 20ms, 0.7초 뒤) 인물이 비는 줄을 센다.
python3 measure.py <url> <out_dir> <on|off> [throttle]
새 브라우저 프로필(캐시 없음)로 돈다."""
import asyncio,sys,json,shutil,tempfile
sys.path.insert(0,'/home/user/daaegame/experiments/renpy-ch1/dev')
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
import numpy as np
from PIL import Image
URL,OUT,MODE=sys.argv[1],Path(sys.argv[2]),sys.argv[3]
THROTTLE=len(sys.argv)>4 and sys.argv[4]=='throttle'
OUT.mkdir(parents=True,exist_ok=True)
PROBE='import renpy;s=renpy.store;result=dict(place=s.place,who=s.r13_motion_person,pose=s.r13_current_pose,shown="r13_visitor" in renpy.exports.get_showing_tags(),screens=[n for n in ("say","choice","r13_hub") if renpy.exports.get_screen(n)])'
def arr(p):return np.asarray(Image.open(p).convert('RGB').crop((300,60,1000,520))).astype(int)
def diff(a,b):return float((np.abs(a-b).max(2)>40).mean())
async def main():
    prof=tempfile.mkdtemp(prefix='r13prof-',dir='/tmp')
    rows=[];prev=None
    try:
        async with async_playwright() as p:
            ctx=await p.chromium.launch_persistent_context(prof,executable_path='/opt/pw-browsers/chromium',viewport={'width':1280,'height':720},
                args=['--no-sandbox','--enable-unsafe-swiftshader'])
            pg=ctx.pages[0] if ctx.pages else await ctx.new_page();q=UIQA(pg,OUT)
            await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=300000);await q.wait('main_menu')
            await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;result=True')
            if MODE=='off':await q.py('import renpy;renpy.store.R13_WEB_ART_READY=False;result=True')
            print('switch',await q.py('import renpy;result=getattr(renpy.store,"R13_WEB_ART_READY",None)'),flush=True)
            if THROTTLE:
                cdp=await ctx.new_cdp_session(pg)
                await cdp.send('Network.enable')
                await cdp.send('Network.emulateNetworkConditions',{'offline':False,'latency':150,'downloadThroughput':1500000,'uploadThroughput':500000})
            await q.press('처음부터')
            for i in range(140):
                info=await q.py(PROBE)
                if 'choice' in info['screens']:
                    st=await q.state();btn=[b_ for b_ in st['buttons'] if b_['text'].strip()]
                    x,y,w,h=btn[0]['rect'];await pg.mouse.click(x+w/2,y+h/2);await asyncio.sleep(1);continue
                if 'r13_hub' in info['screens'] and 'say' not in info['screens']:break
                await pg.mouse.click(810,610)
                await asyncio.sleep(0.02);a=OUT/f'{i:03d}_a.png';await pg.screenshot(path=str(a))
                await asyncio.sleep(0.7);b=OUT/f'{i:03d}_b.png';await pg.screenshot(path=str(b))
                after=await q.py(PROBE)
                kind='same' if (info['who'],info['pose'])==(after['who'],after['pose']) else ('pose' if info['who']==after['who'] else 'arrive')
                if info['place']!=after['place']:kind='scene'
                A,B=arr(a),arr(b);d=diff(A,B);dold=diff(A,prev) if prev is not None else 1.0;prev=B
                # 빈 화면: 넘긴 직후 화면이 새 그림(0.7초 뒤)과도, 앞 줄 그림과도 크게 다르다 = 인물 자리에 배경만 있다.
                rows.append(dict(i=i,before=[info['who'],info['pose']],after=[after['who'],after['pose']],place=after['place'],kind=kind,shown=after['shown'],d=round(d,3),dold=round(dold,3),blank=bool(after['shown'] and after['who'] and d>0.2 and dold>0.2 and kind in ('pose','arrive'))))
                print(rows[-1],flush=True)
                if not rows[-1]['blank']:
                    a.unlink();b.unlink()   # 디스크 절약: 빈 줄만 남긴다
            await ctx.close()
    finally:
        shutil.rmtree(prof,ignore_errors=True)
    (OUT/'rows.json').write_text(json.dumps(rows,ensure_ascii=False,indent=0))
    for k in ('pose','arrive','same'):
        sel=[r for r in rows if r['kind']==k and r['after'][0]]
        print(k,'lines',len(sel),'blank',sum(r['blank'] for r in sel))
asyncio.run(main())
