const {chromium,devices}=require('playwright'),assert=require('node:assert/strict');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});try{
const c=await b.newContext({...devices['iPhone 13']}),p=await c.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
await p.addInitScript(()=>{window.createdTones=0;const orig=AudioContext.prototype.createOscillator;AudioContext.prototype.createOscillator=function(...a){window.createdTones++;return orig.apply(this,a)};});
const url=process.env.CHAPTER_URL||'http://127.0.0.1:8070/chapter-one/';await p.goto(url);assert.equal(await p.evaluate(()=>DaramAudio.status().context),'uninitialized');
await p.locator('#start').tap();await p.waitForTimeout(400);let s=await p.evaluate(()=>DaramAudio.status());assert.equal(s.context,'running');assert.equal(s.playing,true);assert.ok(await p.evaluate(()=>createdTones)>0);
await p.locator('#settings').tap();await p.locator('#music-volume').fill('0');assert.equal(await p.evaluate(()=>DaramAudio.status().playing),false);assert.equal(await p.evaluate(()=>DaramAudio.status().musicGain),0);
const before=await p.evaluate(()=>createdTones);await p.evaluate(()=>DaramAudio.fx('found'));assert.ok(await p.evaluate(()=>createdTones)>before);
await p.locator('#effects-volume').fill('0');await p.waitForTimeout(100);const muted=await p.evaluate(()=>createdTones);await p.evaluate(()=>DaramAudio.fx('present'));assert.equal(await p.evaluate(()=>createdTones),muted);
await p.reload();await p.locator('#continue').tap();await p.locator('[data-resume="0"]').click();assert.deepEqual(await p.evaluate(()=>DaramAudio.get()),{music:0,effects:0});assert.equal(await p.evaluate(()=>DaramAudio.status().playing),false);
await p.locator('#settings').tap();await p.locator('#music-volume').fill('45');await p.locator('#effects-volume').fill('60');await p.evaluate(()=>DaramAudio.music('battle'));assert.equal(await p.evaluate(()=>DaramAudio.status().mode),'battle');assert.equal(await p.evaluate(()=>DaramAudio.status().playing),true);
await p.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'));});assert.equal(await p.evaluate(()=>DaramAudio.status().playing),false);
await p.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,value:false});document.dispatchEvent(new Event('visibilitychange'));});await p.waitForTimeout(120);assert.equal(await p.evaluate(()=>DaramAudio.status().playing),true);assert.equal(await p.evaluate(()=>DaramAudio.status().mode),'battle');assert.deepEqual(errors,[]);
console.log('PASS audio: no autoplay, touch unlock, original oscillator output, independent mute, preference persistence, theme switch, background pause/resume. Chromium emulation, not real Safari.');
}finally{await b.close();}})().catch(e=>{console.error(e);process.exit(1)});
