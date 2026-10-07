const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const root=path.resolve(__dirname,'../../..'),html=fs.readFileSync(path.join(root,'game.html'),'utf8');
assert.equal(html,fs.readFileSync(path.join(root,'dot.html'),'utf8'));
assert(!html.includes('mflap'),'Animated mouth overlay remains');
const scripts=[...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)];
scripts.forEach((m,i)=>new vm.Script(m[1],{filename:'inline-'+i}));
const face=html.match(/var FACE=(\{[^;]+\});/)[1];
const near=html.slice(html.indexOf(' var NEAR='),html.indexOf(' var PRE={}'));
const ctx={};vm.createContext(ctx);vm.runInContext('var FACE='+face+';'+near,ctx);
const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'manifest.json'))),keys=manifest.entries.map(r=>r.key);
for(const key of keys.concat('det0')){
 for(const mood of ['happy','nervous','shock','angry']){
  const result=ctx.strong(key,mood),expected=key==='grandma'&&mood==='angry'?'nervous':mood;
  assert.equal(result,expected,key+' '+mood);
  const actual=key==='det0'?'papa':key;
  assert(fs.existsSync(path.join(root,'art/faces-v2',`${actual}-${result}.png`)));
 }
}
assert.equal(ctx.strong('grandma','cry'),'sad');
for(const k of ['teacher','librarian']){assert.equal(ctx.strong(k,''),'neutral');assert.equal(ctx.strong(k,'think'),'think')}
assert.equal(ctx.pick('wanggu','embarrassed'),'embarrassed');
vm.runInContext(html.slice(html.indexOf('function dialogueMood('),html.indexOf('function lineData(')),ctx);
for(const [line,expected] of [[['papa','헤헤','sad'],'sad'],[['narr','헉!',''],''],[['karo','헉!',''],'shock'],[['rei','저, 저는…',''],'nervous'],[['det1','헤헤!',''],'happy'],[['papa','평범한 대사',''],''],[['papa','다른 대사','',null,'blush'],'blush']])assert.equal(ctx.dialogueMood(line),expected);
ctx.PIXCACHE={};ctx.document={createElement:()=>({})};
vm.runInContext(html.slice(html.indexOf('function pixelize('),html.indexOf('function presTid(')),ctx);
const prefix='<svg class="nodot" viewBox="0 0 100 101" aria-hidden="true"><g id="an-v2-lamplighter-';
const svgs=['happy','angry','shock'].map(m=>prefix+m+'"><image href="art/faces-v2/lamplighter-'+m+'.png"/></g></svg>');
assert.equal(svgs[0].slice(0,80),svgs[1].slice(0,80));assert.equal(svgs[0].length,svgs[1].length);
svgs.forEach((svg,i)=>{ctx.PIXCACHE['216:'+svg]='face-'+i;const el={appendChild:img=>assert.equal(img.src,'face-'+i)};ctx.pixelize(el,svg,216)});
let count=0;for(const r of manifest.entries){const hashes=new Set();for(const e of r.exports){assert(fs.existsSync(path.join(root,e.path)));hashes.add(e.sha256);count++}assert.equal(hashes.size,r.exports.length,'Identical expressions: '+r.key)}
const result={scriptsParsed:scripts.length,characters:keys.length,runtimeImages:count,mouthOverlayRemoved:true,entrypointsIdentical:true,emotionRouting:'passed',dialogueInference:'passed',allPathsExist:true,uniqueExpressions:true,cacheCollisionRegression:"passed",browserPlaytest:false};
fs.writeFileSync(path.join(__dirname,'validation.json'),JSON.stringify(result,null,2)+'\n');console.log(result);
