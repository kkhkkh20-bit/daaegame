// [배치 측정 전용: 상태 주입 — 플레이 검증 아님] 자물쇠 창 버튼이 화면 안에 들어오는지
const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
for(const [W,H] of [[844,390],[640,360]]){const ctx=await b.newContext({viewport:{width:W,height:H},isMobile:true,hasTouch:true});const p=await ctx.newPage();
await p.goto('file:///tmp/claude-0/L/innT.html');await p.waitForTimeout(2500);const T=s=>p.evaluate(s=>{try{return String(window.__T(s))}catch(e){return 'ERR '+e.message}},s);
for(let k=0;k<200;k++){const v=await T('(function(){while(DL)endDlg();var m=document.querySelector("#ov .modal .btn");if(m)m.click();return !!(G.beats&&G.beats.inn_pro)&&!DL})()');if(v==='true')break;await p.waitForTimeout(150)}
await p.waitForTimeout(500);await T('closeModal&&closeModal();1');await p.waitForTimeout(300);
const r=await p.evaluate(()=>{var o=[];return o});await T('(function(){var e=document.createElement("div");return 1})()');
await p.evaluate(()=>{});const ok=await T('(function(){var c=CASES[G.ci];G.loc=0;G.tab="scene";render();return 1})()');
await p.waitForTimeout(300);
/* 자물쇠 창은 장면의 자물쇠 대상에서만 열린다: 같은 함수를 부르기 위해 대상 클릭을 흉내 */
await T('(function(){var b=document.createElement("button");b.dataset.obs="o_inn_lock";var bs=document.getElementById("bigscene");bs.appendChild(b);b.click();return 1})()');await p.waitForTimeout(600);
const m=await p.evaluate(()=>['innhint','innclose','innopen'].map(id=>{var e=document.getElementById(id);if(!e)return id+':none';var r=e.getBoundingClientRect();return id+':'+Math.round(r.left)+','+Math.round(r.top)+' '+Math.round(r.width)+'x'+Math.round(r.height)+(r.bottom<=innerHeight&&r.top>=0?' 안':' 밖')}));
await p.tap('#innhint');await p.waitForTimeout(300);const msg=await p.evaluate(()=>document.getElementById('innmsg').textContent);
await p.screenshot({path:`/tmp/claude-0/L/cap/layout_lock_${W}x${H}.png`});console.log(W+'x'+H,m.join(' / '),'| 힌트:',msg);await ctx.close()}
await b.close()})();
