// 첫 5분 대조 기록: 새 게임 → 프롤로그 → 첫 조사(창고) → 첫 대화(식당 할머니). 실제 탭만, 상태 주입 없음(읽기 전용 확인만)
// 대사 한 줄마다: 장면 · 화자 키 · 이름표 · 보이는 인물 그림 · 흐림 여부 · 배경 · 메뉴/조사 버튼 노출 · 문구
const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
const W=+process.argv[2],H=+process.argv[3],TAG=process.argv[4]||'before',O='/tmp/claude-0/M/cap/'+TAG+'_'+W+'/';require('fs').mkdirSync(O,{recursive:true});
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const ctx=await b.newContext({viewport:{width:W,height:H},isMobile:true,hasTouch:true});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/claude-0/M/innT.html');
const shots=[];for(const ms of [150,400,800]){await p.waitForTimeout(ms);const f=O+`boot_${ms}.png`;await p.screenshot({path:f});shots.push(await p.evaluate(()=>({title:!!document.querySelector('.tfull,.tui'),dl:!!document.querySelector('#dlgveil')})))}
console.log('BOOT',JSON.stringify(shots));
const T=s=>p.evaluate(s=>{try{return String(window.__T(s))}catch(e){return 'ERR '+e.message}},s);
const rows=[];let n=0,lastScene='',sceneShot={};
async function snap(){return JSON.parse(await T(`JSON.stringify((function(){var L=DL&&DL.lines&&DL.lines[DL.i];var pl=document.querySelector('#vnbox .plate');var fig=document.querySelector('#vnfig img,#vnfig svg');var fg=document.getElementById('vnfig');
 var rail=document.getElementById('w209rail');var vis=function(e){if(!e)return false;var r=e.getBoundingClientRect();var s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none'&&+s.opacity>0.05};
 var hots=[].filter.call(document.querySelectorAll('#bigscene .hot,#bigscene .npc'),vis).length;
 var vw=innerWidth,vh=innerHeight;function onScr(e){if(!e)return 0;var r=e.getBoundingClientRect();var w=Math.max(0,Math.min(r.right,vw)-Math.max(r.left,0)),h=Math.max(0,Math.min(r.bottom,vh)-Math.max(r.top,0));var cs=getComputedStyle(e);return (cs.visibility==='hidden'||+cs.opacity<0.05)?0:Math.round(w*h)}
 var fe=document.getElementById('vnfig'),fimg=fe&&fe.querySelector('img'),fsvg=fe&&!fimg&&fe.querySelector('svg');
 var figChk=!fe?'없음':fe.classList.contains('inn-cghide')?'그림속인물(겹침숨김)':fimg?((fimg.complete&&fimg.naturalWidth>32?'로드':'빈그림/미로드')+' '+(fimg.getAttribute('src')||'').split('?')[0].split('/').pop().slice(0,24)+' 표시'+onScr(fimg)+'px²'):fsvg?('절차얼굴 표시'+onScr(fsvg)+'px²'):'빈칸';
 var bgs=document.querySelector('#bigscene svg'),bk=bgs&&bgs.getAttribute('data-bg'),bi=bgs&&bgs.querySelector('image');var bh=bi?(bi.getAttribute('href')||''):'';var bl='-';if(bh){var im=new Image();im.src=bh;bl=(im.complete&&im.naturalWidth>0)?'로드':'미로드'}
 var bgChk=bk?(bk+' '+bh.split('/').pop()+' '+bl):'옛 임시 장면('+(bgs&&bgs.getAttribute('aria-label')||'?')+')';
 return {figChk:figChk,bgChk:bgChk,sc:(G.beats&&G.beats.inn_pi!=null?'P'+(G.beats.inn_pi+1):''),pro:!!(G.beats&&G.beats.inn_pro),loc:CASES[G.ci].locations[G.loc].id,who:L?L[0]:null,plate:pl?pl.textContent.trim():'',fig:fig?(fig.getAttribute('src')||fig.querySelector&&fig.querySelector('image')&&fig.querySelector('image').getAttribute('href')||'svg').replace(/\\?.*$/,'').replace(/^.*\\//,''):'-',dim:fg?fg.className.indexOf('dim')>=0:false,stage:DL&&DL.stageWho||'',txt:L?String(L[1]).slice(0,60):'',rail:vis(rail),hots:hots,arrows:vis(document.getElementById('fsal'))}})())`))}
for(let k=0;k<400;k++){
 const dl=await T('!!DL');
 if(dl==='true'){const s=await snap();const key=s.sc+'|'+s.txt;if(rows.length&&rows[rows.length-1].key===key){}else{s.key=key;rows.push(s);n++;
   if(!sceneShot[s.sc+s.who]){sceneShot[s.sc+s.who]=1;await p.screenshot({path:O+`${String(rows.length).padStart(3,'0')}_${s.sc||'I'}_${s.who}.png`})}}
  const vb=await p.$('#vnbox .vband');if(vb){const r=await vb.boundingBox();if(r)await p.touchscreen.tap(r.x+r.width/2,r.y+r.height/2)}await p.waitForTimeout(260);continue}
 const m=await p.$('#ov .modal');if(m){await p.screenshot({path:O+`${String(rows.length).padStart(3,'0')}_modal.png`});const ok=await p.$('#ov .modal #okfind')||await p.$('#ov .modal #closeit')||await p.$('#ov .modal .btn');if(ok){const r=await ok.boundingBox();await p.touchscreen.tap(r.x+r.width/2,r.y+r.height/2)}await p.waitForTimeout(400);continue}
 if(await T('!!(G.beats&&G.beats.inn_pro)')==='true')break;if(process.argv[5]==='pro3'&&rows.length&&/^P[4-9]/.test(rows[rows.length-1].sc))break;await p.waitForTimeout(300)}
if(process.argv[5]==='pro3'){require('fs').writeFileSync(O+'audit.json',JSON.stringify(rows,null,1));console.log('줄 수',rows.length,'errs',JSON.stringify(errs));console.log(rows.map(r=>[r.sc,r.loc,r.who,'['+r.plate+']','그림:'+r.figChk+(r.dim?'(흐림)':''),'배경:'+r.bgChk,'rail='+(r.rail?1:0),'hot='+r.hots,r.txt.slice(0,30)].join(' | ')).join('\n'));await b.close();return}
await p.waitForTimeout(800);await p.screenshot({path:O+'900_after_pro.png'});
console.log('AFTER_PRO',JSON.stringify(await snap()));
// 첫 조사: 창고의 돈주머니
async function tapSel(sel){const e=await p.$(sel);if(!e)return false;const r=await e.boundingBox();if(!r)return false;await p.touchscreen.tap(r.x+r.width/2,r.y+r.height/2);return true}
async function runDl(tag){for(let k=0;k<80;k++){if(await T('!!DL')==='true'){const s=await snap();const key=tag+'|'+s.txt;if(!rows.length||rows[rows.length-1].key!==key){s.key=key;s.sc=tag;rows.push(s);if(!sceneShot[tag+s.who]){sceneShot[tag+s.who]=1;await p.screenshot({path:O+`${String(rows.length).padStart(3,'0')}_${tag}_${s.who}.png`})}}
  const vb=await p.$('#vnbox .vband');if(vb){const r=await vb.boundingBox();if(r)await p.touchscreen.tap(r.x+r.width/2,r.y+r.height/2)}await p.waitForTimeout(260);continue}
 const m=await p.$('#ov .modal');if(m){await p.screenshot({path:O+`${String(rows.length).padStart(3,'0')}_${tag}_modal.png`});const ok=await p.$('#ov .modal #okfind')||await p.$('#ov .modal #closeit');if(ok){const r=await ok.boundingBox();await p.touchscreen.tap(r.x+r.width/2,r.y+r.height/2)}await p.waitForTimeout(400);continue}
 await p.waitForTimeout(300);if(await T('!!DL')!=='true'&&!await p.$('#ov .modal'))break}}
await p.waitForTimeout(600);
for(const id of ['C01','C02']){await p.evaluate(id=>{var e=document.querySelector('#bigscene [data-spot="'+id+'"]');if(e)e.scrollIntoView({inline:'center',block:'nearest'})},id);await p.waitForTimeout(300);
 for(let r=0;r<3;r++){if(await tapSel(`#bigscene [data-spot="${id}"]`)){await p.waitForTimeout(600);if(await T('!!DL')==='true'||await p.$('#ov .modal'))break}}await runDl('I1_'+id)}
// 첫 대화: 식당 할머니(지도 이동은 이번 기록 범위 밖이라 생략하지 않고 실제로 지도 사용)
await tapSel('#w209rail [data-more]');await p.waitForTimeout(350);await tapSel('#w209more [data-w="move"]');await p.waitForTimeout(900);
await tapSel('#wmap .nd[data-node="inn"]');await p.waitForTimeout(300);
const di=+await T('CASES[G.ci].locations.findIndex(function(l){return l.id==="dining"})');await p.evaluate(i=>{var b=document.querySelector('#wmap [data-room="'+i+'"]');if(b)b.scrollIntoView({inline:'nearest'})},di);await tapSel(`#wmap [data-room="${di}"]`);await p.waitForTimeout(300);await tapSel('#wmap .go');await p.waitForTimeout(2000);
await p.screenshot({path:O+'950_dining.png'});
for(let r=0;r<3;r++){if(await tapSel('#bigscene .npc[data-npc="innma"]')){await p.waitForTimeout(1200);if(await p.$('.fstalk .topic'))break}}
await p.screenshot({path:O+'960_talk_menu.png'});
for(let r=0;r<3;r++){if(await tapSel('.fstalk .topic:not(.done)')){await p.waitForTimeout(600);if(await T('!!DL')==='true')break}}
await runDl('I2_innma');await p.screenshot({path:O+'990_after_talk.png'});
require('fs').writeFileSync(O+'audit.json',JSON.stringify(rows,null,1));
console.log('줄 수',rows.length,'errs',JSON.stringify(errs));
console.log(rows.map(r=>[r.sc,r.loc,r.who,'['+r.plate+']','그림:'+r.figChk+(r.dim?'(흐림)':''),'배경:'+r.bgChk,'stage='+r.stage,'rail='+(r.rail?1:0),'hot='+r.hots,r.txt].join(' | ')).join('\n'));
await b.close()})();
