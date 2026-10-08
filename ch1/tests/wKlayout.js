// [배치 측정 전용: 상태 주입 — 플레이 검증 아님] 전체 지도 겹침·터치 크기
const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
for(const [W,H] of [[844,390],[640,360]]){
const ctx=await b.newContext({viewport:{width:W,height:H},isMobile:true,hasTouch:true});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/claude-0/K/innT.html');await p.waitForTimeout(2500);
const T=s=>p.evaluate(s=>{try{return String(window.__T(s))}catch(e){return 'ERR '+e.message}},s);
for(let k=0;k<0;k++){const d=await T('(function(){var n=0;while(DL&&n<50){endDlg();n++}return n})()');await p.waitForTimeout(150);if(d==='0'&&k>5)break}
for(let k=0;k<200;k++){const v=await T('(function(){while(DL)endDlg();var m=document.querySelector("#ov .modal .btn");if(m)m.click();return !!(G.beats&&G.beats.inn_pro)&&!DL})()');if(v==='true')break;await p.waitForTimeout(200)}
await T('G.beats.inn_pro=1;goTab("move");1');await p.waitForTimeout(800);
await p.evaluate(()=>{var n=document.querySelector('#wmap .nd[data-node="inn"]');n&&n.click()});await p.waitForTimeout(300);
const r=await p.evaluate(()=>{function bb(e){var r=e.getBoundingClientRect();return {l:r.left,t:r.top,r:r.right,b:r.bottom,w:r.width,h:r.height}}
 function ov(a,b){return !(a.r<=b.l||b.r<=a.l||a.b<=b.t||b.b<=a.t)}
 var tb=bb(document.querySelector('#wmap .tb')),st=bb(document.querySelector('#wmap .st')),out={tb:tb,st:st,hit:[],small:[],items:[]};
 document.querySelectorAll('#wmap .nd,#wmap .lb,#wmap .cur').forEach(function(e){var b=bb(e),n=e.dataset.node||e.textContent;out.items.push(e.className+':'+n+' '+Math.round(b.w)+'x'+Math.round(b.h));if(ov(b,tb))out.hit.push(n+'×상단바');if(ov(b,st))out.hit.push(n+'×하단띠')});
 var lbs=[].slice.call(document.querySelectorAll('#wmap .lb,#wmap .cur'));for(var i=0;i<lbs.length;i++)for(var j=i+1;j<lbs.length;j++)if(ov(bb(lbs[i]),bb(lbs[j])))out.hit.push(lbs[i].textContent+'×'+lbs[j].textContent);
 document.querySelectorAll('#wmap button,#wmap .nd').forEach(function(e){var b=bb(e),cs=getComputedStyle(e,':after'),ex=cs.content&&cs.content!=='none'?{x:-parseFloat(cs.left)*2||0,y:-parseFloat(cs.top)*2||0}:{x:0,y:0};if(b.w+ex.x<44||b.h+ex.y<44)out.small.push((e.dataset.room?'방 '+e.textContent:e.dataset.w||e.dataset.node)+' '+Math.round(b.w)+'x'+Math.round(b.h)+(ex.y?' (+'+ex.y+' 확장)':''))});
 var rm=document.querySelector('#wmap .rooms');out.rooms=rm?{vis:rm.clientWidth,full:rm.scrollWidth}:null;out.inview=st.b<=innerHeight&&st.r<=innerWidth&&st.l>=0;return out});
await p.screenshot({path:'/tmp/claude-0/K/cap/layout_wmap_'+W+'x'+H+'.png'});console.log(W+'x'+H,JSON.stringify(r,null,0));console.log('errs',errs,'MISS',await T('JSON.stringify(window.__WMAP)'));await ctx.close()}
await b.close()})();
