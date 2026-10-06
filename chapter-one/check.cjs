const {chromium}=require('playwright'),assert=require('node:assert/strict'),path=require('node:path');
const base=process.env.CHAPTER_URL||'http://127.0.0.1:8066/chapter-one/';
(async()=>{const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});let errors=[];
async function open(size){const p=await browser.newPage({viewport:size});p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});await p.goto(base);await p.locator('#start').click();await p.locator('#settings').click();await p.locator('#speed').selectOption('0');await p.locator('[data-close]').click();return p;}
async function step(p){await p.waitForTimeout(180);await p.locator('#advance').click();}
async function read(p){for(let i=0;i<80&&await p.locator('#advance').count();i++)await step(p);assert.equal(await p.locator('#advance').count(),0);}
async function present(p,id){await p.locator('#present').click();await p.locator(`[data-evidence="${id}"]`).click();await p.locator('#submit').click();}
try{
const p=await open({width:390,height:844});assert.equal(await p.locator('#actor').isVisible(),false);await step(p);await p.screenshot({path:path.join(__dirname,'previews/dialogue.png')});await read(p);
await p.locator('[data-q=delivery]').click();await p.evaluate(()=>document.querySelector('[data-q=delivery]')?.click());await read(p);assert.match(await p.locator('[data-q=delivery]').innerText(),/다시 듣기/);
await p.locator('#investigate').click();assert.equal(await p.locator('#actor').isVisible(),false);await p.screenshot({path:path.join(__dirname,'previews/investigation.png')});
for(const id of ['receipt','tray','clock','cabinet']){await p.locator(`[data-spot=${id}]`).click();if(id==='receipt')await p.screenshot({path:path.join(__dirname,'previews/evidence.png')});await p.locator('#return').click();}
await p.locator('#back').click();await p.locator('#verify').click();await present(p,'receipt');await read(p);assert.equal(await p.locator('.claim').count(),1);assert.match(await p.locator('.claim').innerText(),/세 시/);
await p.locator('#next').click();await present(p,'tray');await read(p);assert.match(await p.locator('.claim').innerText(),/지급/);
await p.locator('#press').click();await read(p);await p.reload();assert.equal(await p.locator('#continue').isVisible(),true);await p.locator('#continue').click();assert.match(await p.locator('.claim').innerText(),/지급/);
await p.screenshot({path:path.join(__dirname,'previews/testimony.png')});await present(p,'receipt');await read(p);assert.equal(await p.locator('[data-q=key]').count(),1);
await p.locator('[data-q=key]').click();await read(p);await p.locator('#verify').click();await present(p,'key');await read(p);assert.equal(await p.locator('.claim').count(),1);await p.locator('#next').click();await present(p,'receipt');await read(p);assert.equal(await p.locator('.claim').count(),1);await present(p,'key');await read(p);
assert.equal(await p.locator('[data-answer=right]').count(),1);await p.locator('[data-answer=right]').click();assert.equal(await p.locator('[data-answer=right]').count(),1); // unread documents cannot be bypassed
for(const id of ['roster','report']){await p.locator('#'+id).click();await p.locator('#return').click();}
await p.locator('[data-answer=wrong]').first().click();await read(p);assert.equal(await p.locator('[data-answer=right]').count(),1);await p.locator('[data-answer=right]').click();await read(p);assert.match(await p.locator('.ending h2').innerText(),/다음 질문/);await p.screenshot({path:path.join(__dirname,'previews/ending.png')});await p.reload();await p.locator('#continue').click();assert.equal(await p.locator('.ending').count(),1);await p.close();console.log('PASS: full chapter, wrong evidence, wrong claim, two confrontations, document comparison, reload, epilogue.');
for(const size of [{width:360,height:640},{width:390,height:844},{width:430,height:932},{width:844,height:390},{width:1280,height:720}]){
 const p=await open(size);await step(p);const panel=await p.locator('#panel').boundingBox(),name=await p.locator('.nameplate').boundingBox(),actor=await p.locator('#actor').boundingBox();assert.ok(name.y>=0&&name.x>=0);assert.ok(panel.y+panel.height<=size.height);if(actor.x+actor.width>panel.x&&actor.x<panel.x+panel.width)assert.ok(actor.y+actor.height*.4<panel.y,'Face must remain above text');assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await p.screenshot({path:path.join(__dirname,`previews/layout-${size.width}.png`)});await read(p);await p.locator('#investigate').click();
 for(const id of ['receipt','tray','clock','cabinet']){const bb=await p.locator(`[data-spot=${id}]`).boundingBox(),pp=await p.locator('#panel').boundingBox();assert.ok(bb.x>=0&&bb.x+bb.width<=size.width+.5,`${id} horizontal at ${size.width}`);assert.ok(bb.y>=60&&bb.y+bb.height<pp.y,`${id} not occluded at ${size.width}: ${JSON.stringify(bb)}`);}
 await p.locator('#notebook').click();await p.keyboard.press('Escape');assert.equal(await p.locator('.sheet').count(),0);await p.close();console.log(`PASS viewport ${size.width}×${size.height}`);
}
assert.deepEqual(errors,[]);console.log('No browser errors / failed requests.');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
