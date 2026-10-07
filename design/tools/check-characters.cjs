const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'..'),m=JSON.parse(fs.readFileSync(root+'/manifest.json'));
(async()=>{
 assert.equal(m.characterArtVersion,4);assert.equal(m.order.length,35);assert(!m.pendingCharacters);
 for(const id of [...m.order,'luka','shadow']){
  const c=m.characters[id];assert(c.src.startsWith('characters/v4/'),id);assert.equal(c.width,1536);assert.equal(c.height,1024);assert.equal(c.frames.length,3);
  for(const [x,y,w,h] of c.frames){assert(x>=0&&y>=0&&w>0&&h===1024&&x+w<=c.width&&y+h<=c.height,id);}
 }
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1280,height:950}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 const base=process.env.DARAM_PREVIEW_URL || 'http://127.0.0.1:8070';
 await page.goto(base+'/design/quality.html?character=karo',{waitUntil:'networkidle'});
 await page.waitForFunction(()=>document.querySelectorAll('#person option').length===35);
 const decoded=await page.evaluate(async()=>{
  const m=await DaramArtKit.ready;return Promise.all([...m.order,'luka','shadow','daram'].map(async id=>{const img=new Image();img.src=DaramArtKit.url(m.characters[id].src);await img.decode();return [id,img.naturalWidth,img.naturalHeight]}));
 });assert.equal(decoded.length,38);for(const [id,w,h] of decoded){assert.equal(w,m.characters[id].width,id);assert.equal(h,m.characters[id].height,id);}
 let poses=0;
 for(const id of m.order){await page.selectOption('#person',id);for(let i=0;i<3;i++){
  await page.locator('#moods button').nth(i).click();
  assert.equal(await page.locator('#other').getAttribute('data-art-id'),id);
  assert.equal(await page.locator('#other svg').getAttribute('viewBox'),m.characters[id].frames[i].join(' '));
  assert.equal(await page.locator('#daram svg').getAttribute('viewBox'),m.characters.daram.frames[i].join(' '));poses++;
 }}
 for(const [width,height] of [[360,640],[390,844],[844,390],[1280,950]]){
  await page.setViewportSize({width,height});await page.selectOption('#person','karo');await page.locator('#moods button').first().click();assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await page.screenshot({path:'/tmp/character-quality-'+width+'.png',fullPage:true});
 }
 await page.goto(base+'/design/',{waitUntil:'networkidle'});await page.waitForFunction(()=>document.querySelectorAll('.cast-card').length===35);
 await page.getByRole('button',{name:m.characters.nero.name+' 캐릭터 보기',exact:true}).click();
 for(const [i,id] of ['nero','luka','shadow'].entries()){await page.locator('#costumes button').nth(i).click();assert.equal(await page.locator('#character-large').getAttribute('data-art-id'),id);assert((await page.locator('#character-download').getAttribute('href')).endsWith(m.characters[id].src));}
 assert.equal(errors.length,0,errors.join(';'));console.log('Characters: 35 people, 105 expressions, 38 decoded PNGs, 3 identity outfits, 4 responsive comparisons; no browser errors.');await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
