const {chromium}=require('playwright'),assert=require('node:assert/strict');
const KEY='daram-illustrated-chapter1-v1';
(async()=>{
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
 try{for(const [width,height] of [[360,640],[390,844],[844,390]]){
  const p=await browser.newPage({viewport:{width,height},hasTouch:true}),errors=[];p.on('pageerror',e=>errors.push(e.message));
  const state=()=>p.evaluate(k=>JSON.parse(localStorage.getItem(k)),KEY);
  await p.goto('http://127.0.0.1:8070/chapter-one/');await p.locator('#start').click();await p.locator('#begin-story').click();await p.locator('#skip-intro').click();
  await p.evaluate(k=>{const v=JSON.parse(localStorage.getItem(k));v.mode='investigate';v.speed=0;v.found=['receipt','tray','clock','cabinet','key','locknote','envelope','roster','report'];v.asked=['delivery','witness'];Object.assign(v.system,{found:v.found,asked:['t_delivery','t_paid','t_witness'],exam:{},recordSelection:'receipt',logic:[]});localStorage.setItem(k,JSON.stringify(v));},KEY);
  await p.reload();await p.locator('#continue').click();await p.locator('[data-resume="0"]').click();await p.locator('#notebook').click();
  const sheet=await p.locator('.sheet').elementHandle();
  async function find(id){for(let i=0;i<6;i++){const item=p.locator('[data-evidence="'+id+'"]');if(await item.count())return item;await p.locator('#record-page-next').click();}throw Error('Unreachable icon '+id);}
  async function fits(){const m=await p.locator('.case-record').evaluate(e=>{const d=e.querySelector('#record-detail'),doc=e.querySelector('.record-document'),op=e.querySelector('.record-operation');return {scroll:e.scrollHeight-e.clientHeight,horizontal:e.scrollWidth-e.clientWidth,doc:doc.lastElementChild.getBoundingClientRect().bottom,action:op?.getBoundingClientRect().top??Infinity};});assert(m.scroll<=1&&m.horizontal<=1&&m.doc<=m.action+1,JSON.stringify({width,height,...m}));}
  assert.equal(await p.locator('#connection-partner').count(),0);
  await p.locator('#record-action').selectOption('combine');await p.locator('#combine-go').click();await fits();await(await find('t_paid')).click();
  assert.match(await p.locator('#record-feedback').innerText(),/작은 글씨/);assert(!(await state()).found.includes('cx_reception_0'));await fits();
  await p.locator('#examine').click();const before=(await state()).system;
  await p.locator('[data-evidence=receipt]').dragTo(p.locator('[data-evidence=tray]'));
  assert.match(await p.locator('#record-feedback').innerText(),/이어지지/);const after=(await state()).system;assert.equal(after.hp,before.hp);assert.equal(after.coins,before.coins);await fits();
  await p.locator('#combine-go').click();await p.locator('[data-evidence=receipt]').click();assert.equal(await p.locator('.case-record.combining').count(),0);
  await p.locator('#combine-go').click();await(await find('t_paid')).click();assert((await state()).found.includes('cx_reception_0'));assert.equal(await sheet.evaluate(e=>e===document.querySelector('.sheet')),true);
  assert(await p.locator('#record-detail.newfact').count());assert.equal(await p.locator('#record-detail .record-source .record-thumb').count(),2);
  await(await find('key')).click();await p.locator('#examine').click();
  const source=await p.locator('[data-evidence=key]').boundingBox(),target=await p.locator('[data-evidence=cabinet]').boundingBox();assert(source&&target);
  const client=await p.context().newCDPSession(p),a={x:source.x+source.width/2,y:source.y+source.height/2},b={x:target.x+target.width/2,y:target.y+target.height/2};
  await client.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[a]});await client.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:(a.x+b.x)/2,y:(a.y+b.y)/2}]});await client.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[b]});await client.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
  assert((await state()).found.includes('cx_reception_1'),'touch drag must combine icons');await p.waitForTimeout(350);
  await(await find('report')).click();await p.locator('#examine').click();await p.locator('#combine-go').click();await fits();await p.screenshot({path:__dirname+'/previews/icon-combination-'+width+'.png'});await p.locator('#combine-cancel').click();assert.equal(await p.locator('.case-record.combining').count(),0);
  assert.deepEqual(errors,[]);await p.close();console.log('PASS icon-to-icon combination, cross-page testimony, inspection gate, cancel, mouse and touch drag, original visuals fit',width,height);
 }}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
