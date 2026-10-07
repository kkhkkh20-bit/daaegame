const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright'),fs=require('fs'),assert=require('assert'),path=require('path');
const root=path.resolve(__dirname,'../..')+'/';const source=JSON.parse(fs.readFileSync(root+'design/scene-map.json'));const manifest=JSON.parse(fs.readFileSync(root+'design/manifest.json'));
(async()=>{
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']}); const page=await browser.newPage({viewport:{width:1280,height:800}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto((process.env.DARAM_PREVIEW_URL || 'http://127.0.0.1:8070')+'/design/',{waitUntil:'networkidle'});await page.waitForFunction(()=>document.querySelectorAll('#cast-grid button').length===35);
 let checked=0,zoomChecked=0;
 for(const key of source.locationOrder){const l=source.locations[key];await page.selectOption('#case-select',l.caseId);await page.selectOption('#location-select',key);
  if(l.evidence.some(e=>e.uv))await page.locator('#uv-mode').check();
  const r=await page.locator('.scene-stage').boundingBox();assert(Math.abs(r.width/r.height-16/9)<.01,key);
  for(const e of l.evidence.filter(e=>!e.inZoom)){
   const point=page.locator('#scene-hotspots [data-point="'+e.spotId+'"]');assert.equal(await point.count(),1,key+':'+e.spotId);
   await point.evaluate(el=>el.click());assert.equal(await page.locator('#evidence-name').innerText(),e.evidence.name);assert.equal(await page.locator('#evidence-desc').innerText(),e.evidence.desc);checked++;
  }
  for(const [zk,z] of Object.entries(l.zooms)){if(!source.zoomBackgrounds[zk])continue;const o=l.observations.find(o=>o.zoom===zk);assert(o);await page.locator('#scene-hotspots [data-point="'+o.id+'"]').evaluate(el=>el.click());
   assert.equal(await page.locator('#zoom-background').getAttribute('data-art-id'),source.zoomBackgrounds[zk]);
   for(const it of z.items.filter(it=>it.ev)){await page.locator('#zoom-hotspots [data-point="'+it.id+'"]').evaluate(el=>el.click());assert.equal(await page.locator('#zoom-evidence-desc').innerText(),it.ev.desc);zoomChecked++;}
   await page.locator('#zoom-close').click();
  }
 }
 assert.equal(checked+zoomChecked,250);assert.equal(source.reviewedLocations.length,82);
 for(const [width,height] of [[360,640],[390,844],[844,390],[1280,800]]){await page.setViewportSize({width,height});await page.selectOption('#case-select','cake');await page.selectOption('#location-select','cake-kitchen');await page.locator('#scene-workbench').scrollIntoViewIfNeeded();assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));const r=await page.locator('.scene-stage').boundingBox();assert(Math.abs(r.width/r.height-16/9)<.01);await page.screenshot({path:'/tmp/wide-gallery-'+width+'.png'});}
 console.log('Gallery:',checked,'scene evidence +',zoomChecked,'drawer evidence; all 82 locations; 4 viewport checks; errors',errors);assert.equal(errors.length,0);
 await page.route('**/game.html',r=>{const s=fs.readFileSync(root+'game.html','utf8').replace('function start(data){','window.__T=function(c){return eval(c)};function start(data){');r.fulfill({contentType:'text/html',body:s})});
 await page.evaluate(()=>localStorage.setItem('daae-detective-v3','ORIGINAL_SAVE_SENTINEL'));
 await page.goto((process.env.DARAM_PREVIEW_URL || 'http://127.0.0.1:8070')+'/design/play.html',{waitUntil:'networkidle'});const frame=page.frames().find(f=>f.url()==='about:srcdoc');await frame.waitForFunction(()=>window.__DaramArtPreviewReady);
 const unchanged=await frame.evaluate(()=>window.__T('({caseCount:CASES.length, locs:CASES.reduce((n,c)=>n+c.locations.length,0),allScenes:CASES.every(c=>c.locations.every(l=>SCENES[c.id+"-"+l.id]().includes("data-daram-art=\\\""+c.id+"-"+l.id+"\\\""))),zarts:Object.keys(window.__ZOOM).filter(k=>window.__ZOOM[k].art.indexOf("daram-art-")===0),player:pf("det0","normal").indexOf("data-daram-art")<0,npc:pf("karo","normal").includes("data-daram-art=\\\"karo\\\"")})'));
 console.log('Actual game bridge',unchanged);assert.equal(unchanged.locs,82);assert(unchanged.allScenes);assert(unchanged.player&&unchanged.npc);assert.equal(unchanged.zarts.length,5);
 await frame.evaluate(()=>window.__T('S.sound=false;S.players=["검수 아빠","다람"];S.screen="case";G=fresh(0);G.introDone=true;S.tut={map:1,spot:1};render()'));
 const hair=source.locations['cake-kitchen'].evidence.find(e=>!e.inZoom);
 await frame.locator('[data-spot="'+hair.evidenceId+'"]').click();await frame.waitForFunction(id=>window.__T('G.found').includes(id),hair.evidenceId,{timeout:10000});
 assert(await frame.evaluate(id=>window.__T('G.found').includes(id),hair.evidenceId));console.log('Actual source click acquired',hair.evidenceId);
 // Close any acquisition modal through the original game function, then open a real drawer.
 await frame.evaluate(()=>window.__T('closeModal();G.notice=null;render()'));
 await frame.locator('[data-obs="o_drawer"]').click();await frame.locator('[data-zi="z_list"]').click();await frame.waitForFunction(()=>window.__T('G.found.includes("guestlist")'),null,{timeout:10000});assert(await frame.evaluate(()=>window.__T('G.found.includes("guestlist")')));
 await frame.evaluate(()=>window.__T('closeModal()'));await frame.locator('#zclose').click();
 await page.waitForTimeout(1000);assert((await frame.locator('.npc svg[data-daram-art="bori"] image').getAttribute('href')).endsWith(manifest.characters.bori.src));assert(await frame.locator('.npc g[id^="daram-npc-"]').count()>0);
 assert.equal(await page.evaluate(()=>localStorage.getItem('daae-detective-v3')),'ORIGINAL_SAVE_SENTINEL');assert(await page.evaluate(()=>Object.keys(localStorage).some(k=>k.startsWith('daram-art-preview-v3:'))));
 for(const [width,height] of [[360,640],[390,844],[844,390],[1280,800]]){await page.setViewportSize({width,height});await frame.evaluate(()=>window.__T('closeModal();G.notice=null;render()'));const r=await frame.locator('#bigscene').boundingBox();assert(Math.abs(r.width/r.height-16/9)<.01);assert(await frame.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await page.screenshot({path:'/tmp/wide-original-'+width+'.png'});}
 console.log('Actual game: main evidence + drawer evidence acquisition passed; original save isolated; 4 responsive viewports; errors',errors);assert.equal(errors.length,0);await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
