const{chromium,devices}=require('playwright'),assert=require('node:assert/strict');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});try{
 const c=await b.newContext({...devices['iPhone 13']}),p=await c.newPage();let failures=[];p.on('pageerror',e=>failures.push(e.message));
 const base=process.env.CHAPTER_URL||'http://127.0.0.1:8067/chapter-one/';
 await p.route('**/assets/reception.png',r=>r.abort());await p.goto(base);await p.locator('#retry-load').waitFor({state:'visible'});assert.equal(await p.locator('#start').isDisabled(),true);assert.match(await p.locator('#load-status').innerText(),/불러오지 못/);
 await p.unroute('**/assets/reception.png');await p.locator('#retry-load').tap();await p.waitForFunction(()=>!document.getElementById('start').disabled);await p.locator('#start').tap();await p.locator('#settings').tap();await p.locator('#speed').selectOption('0');await p.locator('[data-close]').tap();await p.locator('#advance').tap();assert.match(await p.locator('#text').innerText(),/엄마/);assert.deepEqual(failures,[]);
 const p2=await c.newPage();await p2.route('**/story.js',r=>r.abort());await p2.goto(base);await p2.locator('#retry-load').waitFor({state:'visible'});assert.equal(await p2.locator('#start').isDisabled(),true);
 console.log('PASS Chromium iPhone-sized touch emulation: asset failure/retry, start, settings, dialogue; script failure shows recovery. Not real Safari.');
}finally{await b.close();}})().catch(e=>{console.error(e);process.exit(1)});
