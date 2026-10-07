const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('assert');
const root=path.resolve(__dirname,'..'),base=process.env.DARAM_PREVIEW_URL || 'http://127.0.0.1:8070';
const info=JSON.parse(fs.readFileSync(root+'/sandbox/snapshot.json'));
assert.equal(crypto.createHash('sha256').update(fs.readFileSync(root+'/sandbox/game.html')).digest('hex'),info.sha256,'frozen copy integrity');
(async()=>{
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
 const page=await browser.newPage(),requests=[],errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 // Make the working original unavailable: the sandbox must still boot.
 await page.route(base+'/game.html*',r=>{requests.push(r.request().url());r.fulfill({status:503,body:'Working original unavailable'})});
 await page.goto(base+'/design/');
 await page.evaluate(()=>{localStorage.setItem('daae-detective-v3','WORKING_ORIGINAL');localStorage.setItem('daram-art-preview-v3:daae-detective-v3','PREVIOUS_PREVIEW')});
 await page.goto(base+'/design/play.html?v=6',{waitUntil:'networkidle'});
 const frame=page.frames().find(f=>f.url()==='about:srcdoc');await frame.waitForFunction(()=>window.__DaramArtPreviewReady);
 assert.equal(await frame.evaluate(()=>window.__DaramArtPreviewReady.locations),82);
 assert.equal(await frame.evaluate(()=>document.baseURI),base+'/design/sandbox/');
 await frame.evaluate(()=>window.DaramPreviewStorage.setItem('daae-detective-v3','SANDBOX_ONLY'));
 const saved=await page.evaluate(()=>[localStorage.getItem('daae-detective-v3'),localStorage.getItem('daram-art-preview-v3:daae-detective-v3'),localStorage.getItem('daram-design-sandbox-v1:daae-detective-v3')]);
 assert.deepEqual(saved,['WORKING_ORIGINAL','PREVIOUS_PREVIEW','SANDBOX_ONLY']);
 assert.equal(requests.length,0,'never fetch working original');assert.equal(errors.length,0,errors.join(';'));
 assert.equal(await page.locator('a[href="../game.html"]').count(),0);
 console.log('Sandbox: frozen SHA-256 verified; boots with original blocked; 82 scene adapters; original and previous preview saves untouched.');await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
