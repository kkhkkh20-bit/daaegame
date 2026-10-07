const fs=require('node:fs'),assert=require('node:assert/strict'),{chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});try{
const p=await b.newPage({viewport:{width:390,height:844}}),source=fs.readFileSync(__dirname+'/../game.html','utf8');
await p.route('**/game.html',r=>r.fulfill({contentType:'text/html',body:source.replace('function start(data){','window.__T=function(code){return eval(code)};function start(data){')}));
await p.goto('http://127.0.0.1:8070/game.html');await p.waitForFunction(()=>window.__T);
const pair=await p.evaluate(()=>window.__T('G=fresh(0);S.screen="case";G.introDone=true;var c=CASES[0],x=COMBO[c.id][0];G.found=[x.a,x.b].filter(function(id){return !!evById(c,id)});G.asked=[x.a,x.b].filter(function(id){return !!tById(c,id)});G.exam={};[x.a,x.b].forEach(function(id){G.exam[id]=true});render();openRecord(c,"view");({a:x.a,b:x.b,id:"cx_"+c.id+"_0"})'));
async function icon(id){let q=p.locator('[data-crs="'+id+'"]');if(!await q.count()){await p.locator('[data-crt=t]').click();q=p.locator('[data-crs="'+id+'"]');}return q;}
await(await icon(pair.a)).click();await p.locator('#crcomb').click();assert(await p.locator('.crec2.combining').count());await(await icon(pair.b)).click({force:true});assert(await p.evaluate(id=>window.__T('G.found').includes(id),pair.id));assert.equal(await p.locator('.crec2.combining').count(),0);await p.screenshot({path:__dirname+'/previews/original-icon-combination.png'});
console.log('PASS original game.html: select first icon, arm combination, choose second icon, new fact becomes evidence');
}finally{await b.close();}})().catch(e=>{console.error(e);process.exit(1)});
