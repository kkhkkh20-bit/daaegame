"""Prepared native-dialogue regression for approved atlas tail/ear/crest tips.

Existing authored neutral/distress lines enter native say/@dir. Source art is
unchanged. CSS animations are paused briefly at their movement frame to measure
actual screen displacement, then resumed. Expression replacement must remove
the old source mask/layer; quiet, menus and reduced motion remain static.
"""
import argparse
import json
import shutil
from playwright.sync_api import sync_playwright


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',default='http://127.0.0.1:8000/playT.html')
    args=parser.parse_args()
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':844,'height':390});errors=[];bad=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
        try:
            page.goto(args.url,wait_until='domcontentloaded');page.wait_for_timeout(16000)
            def state(code):return page.evaluate('(code)=>window.__T(code)',code)
            state('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};')
            page.evaluate('document.querySelector("#innmain").remove();window.__w209boot()');page.wait_for_timeout(1500)
            def speak(k,quiet=False):
                row=page.evaluate('''({k,quiet})=>{let rows=[];function scan(o){if(!o||typeof o!=='object')return;if(Array.isArray(o)&&o[0]===k&&typeof o[1]==='string'){rows.push(o);return}Object.values(o).forEach(scan)}scan(EP1INN);
                    return rows.find(l=>{const m=__innMood(l)||'neutral';return quiet?/^(sad|worried|cower)$/.test(m):m==='neutral'&&!/(엄마|죽|솜솜|시체|숨|증거|봉인)/.test(l[1])})}''',{'k':k,'quiet':quiet})
                assert row,('Authored feature fixture missing',k,quiet)
                state('if(DL){DL.done=null;endDlg()};window.__innAudioReset();G.who=null;G.tab="scene";render();say('+json.dumps([['@dir','who:'+k+';chime:0;ms:80'],row],ensure_ascii=False)+',null);')
                page.wait_for_timeout(550)
                page.wait_for_function('(k)=>Array.from(document.querySelectorAll("#innstage svg.dialogue-bust")).some(s=>s.dataset.k===k)',arg=k)
            for k in ['det1','nabi','geokkuri','karo']:
                speak(k)
                page.wait_for_function('(k)=>Array.from(document.querySelectorAll("#innstage svg.dialogue-bust")).some(s=>s.dataset.k===k&&s.querySelector(".cm-bust-layer"))',arg=k)
                result=page.locator('#innstage svg.dialogue-bust').evaluate('''svg=>{
                    const layer=svg.querySelector('.cm-bust-layer'),part=layer.querySelector('.cm-part'),animation=part.getAnimations()[0];
                    const source=svg.__image,rect=svg.getBoundingClientRect();
                    if(!animation)return {animation:false,mood:svg.dataset.cmMood,quiet:svg.dataset.cmQuiet,paused:__innMotionState().paused};
                    animation.pause();animation.currentTime=animation.effect.getTiming().duration*.8;
                    const moved=new DOMPoint(0,0).matrixTransform(part.getScreenCTM()),base=new DOMPoint(0,0).matrixTransform(layer.getScreenCTM());
                    const result={animation:true,step:Math.hypot(moved.x-base.x,moved.y-base.y),layers:svg.querySelectorAll('.cm-bust-layer').length,baseOpacity:getComputedStyle(source).opacity,part:layer.dataset.part,rotate:getComputedStyle(svg).rotate,scale:getComputedStyle(svg).scale};animation.play();return result;
                }''')
                assert result['animation'],('Approved feature never animates in calm dialogue',k,result)
                assert .95<=result['step']<=1.05,('Tip displacement is not one screen pixel',k,result)
                assert result['layers']==1 and result['baseOpacity']=='0',('Feature compositing layers duplicate visible source',k,result)
                assert result['rotate'] in ['none','0deg'] and result['scale'] in ['none','1'],('Whole actor rotates/scales',k,result)
                print('PASS',k,result['part'],'actual screen movement',round(result['step'],3),'px',flush=True)
            speak('det1',quiet=True)
            clean=page.locator('#innstage svg.dialogue-bust').evaluate('s=>({layers:s.querySelectorAll(".cm-bust-layer").length,baseOpacity:getComputedStyle(s.__image).opacity,expression:s.dataset.expression,quiet:s.dataset.cmQuiet})')
            assert clean=={'layers':0,'baseOpacity':'1','expression':'distressed','quiet':'1'},('Old tip source survived distress expression',clean)
            speak('det1')
            page.evaluate('(()=>{let p=document.createElement("div");p.id="inn-settings";document.body.appendChild(p)})()');page.wait_for_timeout(220)
            assert page.evaluate('__innMotionState().paused'),'Settings fail to pause motion'
            assert page.locator('.cm-part').evaluate_all('ns=>ns.every(n=>n.getAnimations().length===0)'),'Feature keeps animating behind settings'
            page.evaluate('document.querySelector("#inn-settings").remove()');page.emulate_media(reduced_motion='reduce');page.wait_for_timeout(220)
            assert page.locator('.cm-part').evaluate_all('ns=>ns.every(n=>n.getAnimations().length===0)'),'Reduced-motion feature remains animated'
            assert page.evaluate('__innMotionState().timerCount')==1
            assert not errors,errors
            assert not bad,bad
            print('PASS feature cleanup, quiet distress, settings/reduced-motion static; JS/HTTP errors 0',flush=True)
        finally:
            browser.close()


if __name__=='__main__':main()
