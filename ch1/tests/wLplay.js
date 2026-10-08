// 다람탐정 1장(최신 대본): 새 게임부터 실제 탭만으로 프롤로그 → 조사 → 회의 → 최종 대결 → 후일담 (상태 주입 없음). 인자 3 'fail'이면 설득력 0칸 경로도 실제 탭으로 시험
const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const W=+process.argv[2],H=+process.argv[3],O='/tmp/claude-0/L/cap/';require('fs').mkdirSync(O,{recursive:true});
const ctx=await b.newContext({viewport:{width:W,height:H},isMobile:true,hasTouch:true});const p=await ctx.newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/claude-0/L/innT.html');
await p.evaluate(()=>{var R=window.__W209REAL;for(var i=R.length-1;i>=0;i--){var k=R.key(i);if(k&&k.indexOf('dc1:')!==0)R.removeItem(k)}R.setItem('daae-detective-v3','{"marker":"REAL-SAVE"}')});
await p.reload();await p.waitForTimeout(2500);
const T=s=>p.evaluate(s=>{try{return String(window.__T(s))}catch(e){return 'ERR '+e.message}},s);// 읽기 전용 확인에만 사용
const log=[],stuck=[],dlgKinds={},dbg=[];const _lp=log.push.bind(log);log.push=(...a)=>{a.forEach(x=>console.log(x));return _lp(...a)};const t0=Date.now();
async function tapXY(x,y){await p.touchscreen.tap(x,y)}
async function tapEl(sel){const e=typeof sel==='string'?await p.$(sel):sel;if(!e)return false;const r=await e.boundingBox();if(!r)return false;await tapXY(r.x+r.width/2,r.y+r.height/2);return true}
let lastSig='',same=0;
async function clear(max=80){for(let k=0;k<max;k++){
  const s=JSON.parse(await T('JSON.stringify({dl:!!DL,i:DL?DL.i:-1,m:!!document.querySelector("#ov .modal"),pad:!!document.getElementById("innpad"),tm:!!document.getElementById("tomeet"),b:!!document.querySelector(".banner:not(.out),.cutin,.flash")})'));
  if(s.tm||s.pad)return s;
  if(!s.dl&&!s.m&&!s.b)return s;
  if(s.m){const ok=await p.$('#ov .modal #okfind')||await p.$('#ov .modal #closeit')||await p.$('#ov .modal .btn');if(ok){await p.waitForTimeout(250);await tapEl(ok)}await p.waitForTimeout(400);continue}
  if(s.dl){const sig=s.i+'|'+(await T('DL&&DL.lines&&String(DL.lines[DL.i]&&DL.lines[DL.i][1]).slice(0,20)'));if(sig===lastSig)same++;else{lastSig=sig;same=0}
   const vb=await p.$('#vnbox .vband');let kind='vband';
   if(vb){const r=await vb.boundingBox();if(r&&r.width>0){await tapXY(r.x+r.width/2,r.y+r.height/2)}else kind='vband-hidden'}else kind='none';
   if(kind!=='vband'){const alt=await p.evaluate(()=>{var c=['#sbtext','.sbook','#dlgveil','.vn'];for(var i=0;i<c.length;i++){var e=document.querySelector(c[i]);if(e){var r=e.getBoundingClientRect();if(r.width>0)return {sel:c[i],x:r.left+r.width/2,y:r.top+r.height*.8}}}return null});
    if(alt){kind+='>'+alt.sel;await tapXY(alt.x,alt.y)}}
   dlgKinds[kind]=(dlgKinds[kind]||0)+1;
   if(same===8){stuck.push({sig,kind,stack:await p.evaluate(()=>{var v=document.querySelector('#vnbox .vband');if(!v)return 'no vband';var r=v.getBoundingClientRect();return document.elementsFromPoint(r.left+r.width/2,r.top+r.height/2).slice(0,5).map(e=>e.tagName+'#'+e.id+'.'+String(e.className).slice(0,30)).join(' > ')})});await p.screenshot({path:O+`stuck_${W}x${H}_${stuck.length}.png`})}
   await p.waitForTimeout(260);continue}
  await p.waitForTimeout(250)}return null}
async function locate(sel){return p.evaluate(sel=>{var e=document.querySelector(sel);if(!e)return null;var fx=document.getElementById('fsscroll');if(!fx)return true;var r=e.getBoundingClientRect(),fr=fx.getBoundingClientRect();if(r.left<fr.left+40||r.right>fr.right-40){fx.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));fx.scrollLeft+=(r.left+r.width/2)-(fr.left+fr.width/2)}return true},sel)}
async function tapScene(){let n=0;for(let pass=0;pass<6;pass++){const items=await p.evaluate(()=>[...document.querySelectorAll('#bigscene [data-spot],#bigscene [data-obs]')].map(e=>e.dataset.spot?'[data-spot="'+e.dataset.spot+'"]':'[data-obs="'+e.dataset.obs+'"]'));
  const todo=[];for(const it of items){const done=await p.evaluate(s=>{var e=document.querySelector('#bigscene '+s);return !e||e.classList.contains('done')||e.classList.contains('seen')},it);if(!done||it.indexOf('o_inn_lock')>=0)todo.push(it)}
  dbg.push('pass'+pass+' items '+items.length+' todo '+todo.join(','));if(!todo.length)break;let did=0;
  for(const it of todo){const sel='#bigscene '+it;await clear();let okEl=false;for(let r=0;r<4&&!okEl;r++){await locate(sel);await p.waitForTimeout(300);okEl=!!await p.$(sel);if(!okEl){dbg.push(' missing '+it+' tab='+await T('G.tab')+' notice='+await T('JSON.stringify(G.notice&&G.notice.title)'));await p.waitForTimeout(600)}}if(!okEl)continue;
   if(it.indexOf('o_inn_lock')>=0){await tapEl(sel);await p.waitForTimeout(600);await lock();did++;continue}
   const f0=await T('G.found.length');await tapEl(sel);n++;did++;await p.waitForTimeout(700);for(let w=0;w<10;w++){await clear();await p.waitForTimeout(350);if(it.indexOf('data-obs')>=0||await T('G.found.length')!==f0)break}await clear();dbg.push(' tap '+it+' found='+await T('G.found.join(",")'))}
  if(!did&&pass>0)break}return n}
async function lock(){if(!await p.$('#innpad'))return;await p.screenshot({path:O+`lock_${W}x${H}.png`});await tapEl('#innhint');await p.waitForTimeout(250);log.push('자물쇠 힌트 '+await p.evaluate(()=>{var m=document.getElementById('innmsg');return m?m.textContent:''}));await p.screenshot({path:O+`lockhint_${W}x${H}.png`});await tapEl('#innpad [data-d="0"]');await p.waitForTimeout(150);await tapEl('#innopen');await p.waitForTimeout(400);log.push('자물쇠 오입력 1000 → '+await p.evaluate(()=>{var m=document.getElementById('innmsg');return (m?m.textContent:'')+' / 창 유지 '+!!document.getElementById('innpad')}));const want=[0,1,0,2];
 for(let i=0;i<4;i++)for(let k=0;k<want[i];k++){await tapEl(`#innpad [data-d="${i}"]`);await p.waitForTimeout(120)}
 await tapEl('#innopen');await p.waitForTimeout(900);log.push('자물쇠 실제 탭 1102 → 열림 '+await T('!!(G.beats&&G.beats.inn_lock)'));await clear()}
async function askAll(){const npcs=await p.evaluate(()=>[...document.querySelectorAll('#bigscene .npc')].map(e=>e.dataset.npc));let n=0;
 for(const k of npcs){await clear();const sel=`#bigscene .npc[data-npc="${k}"]`;await locate(sel);await p.waitForTimeout(300);if(!await tapEl(sel))continue;await p.waitForTimeout(1200);await clear();
  for(let q=0;q<8;q++){const tp=await p.$('.fstalk .topic:not(.done)');if(!tp)break;await tapEl(tp);n++;await p.waitForTimeout(700);await clear();await p.waitForTimeout(400)}
  for(let w=0;w<20&&await p.evaluate(()=>!!document.querySelector('.veil.vn'));w++)await p.waitForTimeout(150);for(let r=0;r<4&&await T('G.tab')!=='scene';r++){const bk=await p.$('#w209back');if(!bk)break;await p.waitForTimeout(500);await tapEl(bk);await p.waitForTimeout(700)}await clear()}return n}
async function goLoc(id){const i=+await T('CASES[G.ci].locations.findIndex(function(l){return l.id==="'+id+'"})');if(+await T('G.loc')===i&&await T('G.tab')==='scene')return true;
 await clear();await tapEl('#w209rail [data-more]');await p.waitForTimeout(350);const mv=await p.$('#w209more [data-w="move"]');if(!mv){log.push('이동 버튼 없음');return false}await tapEl(mv);
 for(let k=0;k<8&&!await p.$('#wmap');k++){await p.waitForTimeout(300);if(k===4){await clear();await tapEl('#w209rail [data-more]');await p.waitForTimeout(300);const m2=await p.$('#w209more [data-w="move"]');if(m2)await tapEl(m2)}}
 if(!await p.$('#wmap')){log.push('전체 지도 안 열림');return false}
 if(!mapShot){mapShot=1;await p.screenshot({path:O+`wmap_open_${W}x${H}.png`})}
 await tapEl('#wmap .nd[data-node="inn"]');await p.waitForTimeout(300);
 if(await p.$(`#wmap [data-room="${i}"]`)){await p.evaluate(i=>{var b=document.querySelector('#wmap [data-room="'+i+'"]');if(b)b.scrollIntoView({inline:"nearest",block:"nearest"})},i);await p.waitForTimeout(150);await tapEl(`#wmap [data-room="${i}"]`);await p.waitForTimeout(250)}
 if(mapShot===1){mapShot=2;await p.screenshot({path:O+`wmap_room_${W}x${H}.png`})}
 const dis=await p.evaluate(()=>{var g=document.querySelector('#wmap .go');return !g||g.disabled});if(dis){log.push('이동 버튼 꺼짐 '+id);await tapEl('#wmap [data-w="close"]');return false}
 await tapEl('#wmap .go');await p.waitForTimeout(1800);await clear();return +await T('G.loc')===i}
const FAIL=process.argv[4]==='fail';
let mapShot=0;
// 1) 프롤로그
for(let k=0;k<60;k++){await clear(120);if(await T('!!(G.beats&&G.beats.inn_pro)')==='true')break;await p.waitForTimeout(500)}
log.push('프롤로그 끝 '+await T('!!(G.beats&&G.beats.inn_pro)')+' · C07 '+await T('G.found.indexOf("C07")>=0')+' (경과 '+Math.round((Date.now()-t0)/1000)+'초)');await p.screenshot({path:O+`pro_end_${W}x${H}.png`});
// 2) 조사 (실제 탭)
for(const id of ['bed13','dining','kitchen','hall','dotoroom','front','bed13','kitchen']){const ok=await goLoc(id);if(!ok){log.push(id+' 이동 실패');continue}
 if(!mapShot)mapShot=1;
 await p.screenshot({path:O+`inv_${id}_${W}x${H}.png`});
 const n=await tapScene();const q=await askAll();log.push(`${id}: 살펴보기 ${n}, 질문 ${q}, 증거 ${await T('G.found.join(",")')} / 증언 ${await T('G.asked.join(",")')}`)}
log.push('조사 후 부족 '+await T('JSON.stringify(window.__rtGap(CASES[G.ci]))'));
// 3) 회의 진입(I9 → 실제 버튼)
let st=await clear();let how='';
log.push('I9 재생 '+await T('!!(G.beats&&G.beats.inn_i9)'));
if(st&&st.tm){await p.screenshot({path:O+`tomeet_${W}x${H}.png`});for(let k=0;k<5&&await p.$('#tomeet');k++){await p.waitForTimeout(600);await tapEl('#tomeet')}how='회의 열까요 창';}
else{await tapEl('#w209rail [data-w="ev"]');await p.waitForTimeout(900);const mb=await p.$('.crec2 [data-cr199="meet"]');if(mb){await tapEl(mb);how='증거창 버튼'}else how='버튼 없음'}
await p.waitForTimeout(4000);log.push('회의 진입('+how+') '+await p.evaluate(()=>!!document.querySelector('body>.rt')));
// 4) 회의·최종 대결: 라운드별 실제 탭 계획
const F5=n=>Array.from({length:n},()=>({op:'present',i:0,id:'C09',exp:'fail-run'}));
const PLAN={
 M1:[...(FAIL?F5(5):[]),{op:'present',i:0,id:'C01',exp:'-1'},{op:'present',i:2,id:'C03',exp:'0'},{op:'press',i:1},{op:'present',i:1,id:'C03',exp:'0 순서'},{op:'present',i:1,id:'C02',exp:'0 단계'},{op:'present',i:1,id:'C03',exp:'정답'}],
 M3:[{op:'present',i:2,id:'C09',exp:'-1'},{op:'present',i:1,id:'C04',exp:'0 이동→정답'}],
 M5:[{op:'present',i:1,id:'C08',exp:'0 이른 C08'},{op:'present',i:0,id:'C06',exp:'0'},{op:'present',i:0,id:'C13',exp:'0 ②로 이동'},{op:'present',i:1,id:'C07',exp:'0 단계'},{op:'present',i:1,id:'C08',exp:'정답'}],
 M6:[{op:'present',i:1,id:'C04',exp:'0'},{op:'present',i:0,id:'C13',exp:'0'},{op:'present',i:2,id:'C10',exp:'정답'}],
 F1:[...(FAIL?F5(5):[]),{op:'present',i:0,id:'C12',exp:'0'},{op:'present',i:0,id:'C13',exp:'0 단계'},{op:'present',i:0,id:'C01',exp:'정답'}],
 F3:[{op:'present',i:0,id:'C11',pick:1,exp:'-1 꽃'},{op:'present',i:0,id:'C11',pick:3,exp:'0 별 단계'},{op:'present',i:0,id:'C05',exp:'정답(대체 정답 C05)'}]};
const OPI={},opLog=[],shots={};let idle=0,steps=0,lastOp=null,hpAt=null,mf=0,fr=0,gone=0;
async function key(){return T('(function(){var p=window.__rtPh&&window.__rtPh();if(!p)return "";var a=EP1INN.MEET.phases.indexOf(p);return a>=0?"M"+a:"F"+EP1INN.FINAL.phases.indexOf(p)})()')}
async function stmIdx(){return p.evaluate(()=>{var e=document.querySelector('.rt-bub small em');return e?+(e.textContent.split('/')[0].trim())-1:0})}
async function goStm(i){for(let k=0;k<6;k++){if(await stmIdx()===i)return true;await tapEl('#rtgbar [data-g="next"]');await p.waitForTimeout(160)}return await stmIdx()===i}
async function drainQ(){for(let k=0;k<30&&await T('!!(window.__rtgQueue&&window.__rtgQueue())')==='true';k++){await tapEl('#rtgbar [data-g="next"]');await p.waitForTimeout(140)}}
function closeOp(hp){if(lastOp){lastOp.hp=hpAt+'→'+hp;opLog.push(lastOp);lastOp=null}}
while(steps++<1500){
 const s=await T('(function(){if(!document.querySelector("body>.rt"))return "gone";if(window.__rtgPick&&window.__rtgPick())return "pick";if(document.querySelector(".flash,.cutin,.banner:not(.out)"))return "busy";if(window.__rtgQueue&&window.__rtgQueue())return "queue";if(document.getElementById("rtnext"))return "talk";return window.__rtCur()||"?"})()');
 if(s==='gone'){if(await T('!!(G.beats&&G.beats.inn_end)')==='true'&&await T('!!DL')==='false')break;
  if(await T('!!DL')==='true'){const tx=await T('DL&&DL.lines&&String(DL.lines[DL.i]&&DL.lines[DL.i][1]).slice(0,24)');
   if(/솜솜이 깨거든/.test(tx)&&!shots.mf){shots.mf=1;mf++;await p.screenshot({path:O+`mf_${W}x${H}.png`})}
   if(/엄마 글씨다/.test(tx)&&!shots.e3){shots.e3=1;await p.screenshot({path:O+`e3_${W}x${H}.png`})}
   if(/반은 잘 지켜/.test(tx)&&!shots.e4){shots.e4=1;await p.screenshot({path:O+`e4_${W}x${H}.png`})}
   await clear(6);continue}
  if(++gone%20===0)log.push('대기 '+gone+' notice='+await T('JSON.stringify(G.notice&&G.notice.title)'));
  await clear(6);await p.waitForTimeout(400);continue}
 gone=0;
 if(s==='busy'){await p.waitForTimeout(200);continue}
 if(s==='queue'){await tapEl('#rtgbar [data-g="next"]');await p.waitForTimeout(140);continue}
 if(s==='talk'){const k=await key();if(!shots['t'+k]){shots['t'+k]=1;await p.screenshot({path:O+`r_${k}_talk_${W}x${H}.png`})}
  if(k==='F0'&&!shots.show&&await p.$('#rtgshow')){shots.show=1;await p.screenshot({path:O+`f1_show_${W}x${H}.png`});log.push('F1 C05 자동 재표시 '+await p.evaluate(()=>document.getElementById('rtgshow').innerText.replace(/\s+/g,' ')))}
  await tapEl('#rtgbar [data-g="next"]');await p.waitForTimeout(140);continue}
 if(s==='pick'){await p.screenshot({path:O+`pick_${W}x${H}.png`});const it=lastOp&&lastOp.pick;await tapEl(`#rtgpick [data-pi="${it}"]`);await p.waitForTimeout(300);continue}
 if(s==='debate'){const k=await key();const hp=await T('G.hp');closeOp(hp);
  if(!shots['d'+k]){shots['d'+k]=1;await p.screenshot({path:O+`r_${k}_${W}x${H}.png`})}
  const L=PLAN[k]||[];OPI[k]=OPI[k]||0;const op=L[OPI[k]];if(!op){if(++idle>30){log.push('계획 없음/소진 '+k);break}await p.waitForTimeout(250);continue}idle=0;OPI[k]++;
  lastOp=Object.assign({k},op);hpAt=hp;
  for(let w=0;w<30&&await p.evaluate(()=>!!document.querySelector('.banner:not(.out)'));w++)await p.waitForTimeout(150);
  if(await p.evaluate(()=>document.body.classList.contains('rtg-drw'))){await tapEl('#rtgbar [data-g="back"]');await p.waitForTimeout(300)}
  if(!await goStm(op.i)){lastOp.err='발언 이동 실패';continue}
  if(op.op==='press'){await tapEl('#rtgbar [data-g="press"]');await p.waitForTimeout(300);if(!shots['p'+k]){shots['p'+k]=1;await p.screenshot({path:O+`r_${k}_press_${W}x${H}.png`})}continue}
  for(let r=0;r<3&&await p.evaluate(()=>!document.body.classList.contains('rtg-drw'));r++){await tapEl('#rtgbar [data-g="ev"]');await p.waitForTimeout(350)}
  await p.evaluate(id=>{var e=document.querySelector('.rt-bul .bl[data-bl="'+id+'"]');if(e)e.scrollIntoView({block:'nearest',inline:'nearest'})},op.id);await p.waitForTimeout(200);
  const selOk=await tapEl(`.rt-bul .bl[data-bl="${op.id}"]`)&&await p.waitForTimeout(150)===undefined&&await p.evaluate(id=>{var e=document.querySelector('.rt-bul .bl.on');return !!e&&e.dataset.bl===id},op.id);
  if(!selOk){lastOp.err='증거 버튼 없음';const bb=await p.$('#rtgbar [data-g="back"]');if(bb)await tapEl(bb);continue}
  await p.waitForTimeout(200);await tapEl('#rtgbar [data-g="present"]');await p.waitForTimeout(350);
  const tag=k+'_'+op.id+'_'+OPI[k];if(/정답|이동|단계|-1/.test(op.exp))await p.screenshot({path:O+`op_${tag}_${W}x${H}.png`});
  continue}
 if(s==='vote'){closeOp(await T('G.hp'));if(!shots.vote){shots.vote=1;await p.waitForTimeout(400);await p.screenshot({path:O+`r_vote_${W}x${H}.png`});log.push('투표판 '+await p.evaluate(()=>{var h=document.querySelector('#rtgvote .hd');return h?h.innerText.replace(/\s+/g,' '):'없음'}))}
  await tapEl('#rtgvote [data-pick="seryeon"]');await p.waitForTimeout(2200);continue}
 await p.waitForTimeout(300)}
closeOp(await T('G.hp'));
await p.waitForTimeout(1500);await clear();await p.screenshot({path:O+`end_${W}x${H}.png`});
log.push('제시 기록:\n'+opLog.map(o=>`  ${o.k} ${o.op} ${o.i!=null?'발언'+(o.i+1):''} ${o.id||''}${o.pick!=null?' 줄'+o.pick:''} 기대 ${o.exp||''} → 설득력 ${o.hp}${o.err?' !'+o.err:''}`).join('\n'));
log.push(`단계 ${steps}, M-F ${mf}, 회의 완료 ${await T('!!(G.beats&&G.beats.inn_meet)')}, 최종 대결 완료 ${await T('!!(G.beats&&G.beats.inn_final)')}, 후일담 끝 ${await T('!!(G.beats&&G.beats.inn_end)')}, 안내 ${await T('JSON.stringify(G.notice&&G.notice.title)')}`);
log.push('C13 갱신 '+await T('!!(G.beats&&G.beats.inn_c13fix)')+' · '+await T('JSON.stringify(evById(CASES[G.ci],"C13").desc.slice(0,14))')+' / 증거 '+await T('G.found.join(",")'));
log.push('기본 저장 그대로 '+await p.evaluate(()=>window.__W209REAL.getItem('daae-detective-v3')==='{"marker":"REAL-SAVE"}')+' / 시험 저장 키 '+await p.evaluate(()=>{var R=window.__W209REAL,n=0;for(var i=0;i<R.length;i++)if(R.key(i).indexOf('daae-inn1:')===0)n++;return n}));
log.push('대화창 종류 '+JSON.stringify(dlgKinds)+' / 막힘 '+JSON.stringify(stuck));
log.push('내부 누락 '+await T('JSON.stringify({inn:window.__INNMISS,rti:window.__RTI,wmap:window.__WMAP})'));
log.push('DBG\n'+dbg.join('\n'));log.push('errs '+JSON.stringify(errs)+' 경과 '+Math.round((Date.now()-t0)/1000)+'초');
console.log(log.join('\n'));await b.close()})();
