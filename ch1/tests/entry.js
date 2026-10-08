// 첫 진입 실제 탭 검수: 메인 → 설정 저장·복구 → 새 게임 → 콜드 오픈 → P1 → 첫 조사·첫 질문 → 새로고침 → 이어하기 → 새 게임 덮어쓰기 확인
// 상태 주입 없음. window.__T는 읽기 전용 확인에만 사용.
const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
const W=+process.argv[2],H=+process.argv[3],O=`/tmp/claude-0/M/cap/entry_${W}/`;require('fs').mkdirSync(O,{recursive:true});
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const ctx=await b.newContext({viewport:{width:W,height:H},isMobile:true,hasTouch:true});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
const log=[];const L=(...a)=>{const s=a.join(' ');log.push(s);console.log(s)};let n=0;const shot=async t=>{n++;const f=`${String(n).padStart(2,'0')}_${t}.png`;await p.screenshot({path:O+f});return f};
const T=s=>p.evaluate(s=>{try{return String(window.__T(s))}catch(e){return 'ERR '+e.message}},s);
async function tap(sel){const e=typeof sel==='string'?await p.$(sel):sel;if(!e)return false;const r=await e.boundingBox();if(!r||!r.width)return false;await p.touchscreen.tap(r.x+r.width/2,r.y+r.height/2);return true}
async function clearDl(max=200,tag){let calm=0;for(let k=0;k<max;k++){const s=JSON.parse(await T('JSON.stringify({dl:!!DL,m:!!document.querySelector("#ov .modal")})'));if(!s.dl&&!s.m){if(++calm>=4)return k;await p.waitForTimeout(250);continue}calm=0;
  if(s.m){if(tag&&!clearDl.mshot){clearDl.mshot=1;await shot(tag+'_card')}const ok=await p.$('#ov .modal #okfind')||await p.$('#ov .modal #closeit')||await p.$('#ov .modal .btn');if(ok){await p.waitForTimeout(250);await tap(ok)}await p.waitForTimeout(400);continue}
  const vb=await p.$('#vnbox .vband');if(vb)await tap(vb);await p.waitForTimeout(240)}return -1}
await p.goto('file:///tmp/claude-0/M/innT.html');
await p.evaluate(()=>{var R=window.__W209REAL;for(var i=R.length-1;i>=0;i--){var k=R.key(i);if(k&&k.indexOf('dc1:')!==0)R.removeItem(k)}R.setItem('daae-detective-v3','{"marker":"REAL-SAVE"}')});
await p.reload();await p.waitForTimeout(400);await shot('loading');await p.waitForTimeout(2600);
// 1) 메인
const m1=await p.evaluate(()=>{var M=document.getElementById('innmain');if(!M)return null;var bs=[...M.querySelectorAll('.menu button')];return {menu:bs.map(b=>b.textContent+(b.disabled?'(꺼짐)':'')+(b===document.activeElement?'(포커스)':'')),case:!!document.querySelector('#bigscene'),dl:!!document.querySelector('#dlgveil'),hit:bs.map(b=>{var r=b.getBoundingClientRect();return Math.round(r.width)+'x'+Math.round(r.height)})}});
L('1 메인(저장 없음):',JSON.stringify(m1));await shot('main_nosave');
// 2) 설정: 바꾸고 저장
await tap('#innmain [data-m="set"]');await p.waitForTimeout(500);await shot('options_open');
const sl=await p.$('#innopt input[data-s="musicVolume"]');const r=await sl.boundingBox();await p.touchscreen.tap(r.x+r.width*0.3,r.y+r.height/2);await p.waitForTimeout(200);
await tap('#innopt .grp[data-g="fontSize"] [data-v="large"]');await tap('#innopt .grp[data-g="dialogueSpeed"] [data-v="fast"]');await p.waitForTimeout(700);
L('2 설정 변경:',await p.evaluate(()=>[...document.querySelectorAll('#innopt [data-vv]')].map(e=>e.textContent).join('/')+' '+[...document.querySelectorAll('#innopt [aria-checked=true]')].map(e=>e.textContent).join('/')));await shot('options_changed');
// 변경 후 닫기 → 확인창
await tap('#innopt .x');await p.waitForTimeout(300);L('  변경 후 닫기 확인창:',await p.evaluate(()=>{var c=document.querySelector('.innconf');return c?c.innerText.replace(/\s+/g,' ')+' 포커스='+document.activeElement.textContent:'없음'}));await shot('options_unsaved');
await tap('.innconf [data-k="no"]');await p.waitForTimeout(200);
await tap('#innopt .sv');await p.waitForTimeout(400);L('  저장 후 메인 복귀:',await p.evaluate(()=>!document.getElementById('innopt')&&!!document.getElementById('innmain')),'저장값',await p.evaluate(()=>window.__W209REAL.getItem('daae-inn1:inn_settings')));
// 새로고침 후 설정 복구
await p.reload();await p.waitForTimeout(3000);await tap('#innmain [data-m="set"]');await p.waitForTimeout(500);
L('3 새로고침 후 설정:',await p.evaluate(()=>[...document.querySelectorAll('#innopt [data-vv]')].map(e=>e.textContent).join('/')+' '+[...document.querySelectorAll('#innopt [aria-checked=true]')].map(e=>e.textContent).join('/')));await shot('options_restored');
await tap('#innopt .x');await p.waitForTimeout(300);
// 4) 새 게임 → 콜드 오픈
await tap('#innmain [data-m="new"]');await p.waitForTimeout(500);
const beats=[];for(let k=0;k<40;k++){const s=await p.evaluate(()=>{var c=document.getElementById('inncold');if(!c)return null;var st=window.__innColdState&&window.__innColdState();var bg=c.querySelector('.cbg').style.backgroundImage;return {i:st&&st.i,tag:c.querySelector('.tag').textContent,say:c.querySelector('.box.on p')?c.querySelector('.box p').textContent:'',ttl:c.querySelector('.ttl.on')?c.querySelector('.ttl').textContent:'',bg:bg.replace(/.*\//,'').replace(/["\)]/g,''),sk:!!c.querySelector('.sk')}});
 if(!s)break;const key=s.i+'|'+s.say+'|'+s.ttl;if(!beats.length||beats[beats.length-1].key!==key){s.key=key;beats.push(s);await p.waitForTimeout(700);await shot('cold_'+String(s.i+1).padStart(2,'0'))}
 if(k===3){const i0=s.i;await p.waitForTimeout(5000);L('  자동 넘김 없음 확인(5초 대기):',(await p.evaluate(()=>window.__innColdState().i))===i0)}
 await p.mouse.click(W/2,H/3);await p.waitForTimeout(450)}
L('4 콜드 오픈 비트:',beats.map(x=>[String(x.i+1).padStart(2,'0'),x.bg,x.tag,x.say,x.ttl].filter(Boolean).join(' ')).join(' / '),'건너뛰기 버튼(첫 회):',beats.length?beats[0].sk:'-');
await p.waitForTimeout(1500);
const p1=await T('JSON.stringify({pi:G.beats.inn_pi,bg:(window.__innBg&&window.__innBg()||{}).key,line:DL&&DL.lines[DL.i]&&DL.lines[DL.i][1]})');L('5 P1 진입:',p1);await shot('p1_first');
// 프롤로그 진행(실제 탭)
for(let k=0;k<80;k++){await clearDl(30);if(await T('!!(G.beats&&G.beats.inn_pro)')==='true')break;await p.waitForTimeout(400)}
L('6 프롤로그 끝:',await T('JSON.stringify({pro:!!G.beats.inn_pro,loc:CASES[G.ci].locations[G.loc].id,found:G.found,notice:G.notice&&G.notice.title})'));await shot('investigation_start');
// 첫 조사: 창고 돈주머니·이불(핫스폿 실제 탭)
for(let w=0;w<30&&await p.evaluate(()=>!!document.getElementById('dlgveil')||document.body.classList.contains('inn-cut'));w++)await p.waitForTimeout(200);
for(const id of ['C01','C02']){await p.evaluate(id=>{var e=document.querySelector('#bigscene [data-spot="'+id+'"]');if(e)e.scrollIntoView({inline:'center',block:'nearest'})},id);await p.waitForTimeout(300);
 let ok=false;for(let r=0;r<3&&!ok;r++){ok=await tap(`#bigscene [data-spot="${id}"]`);await p.waitForTimeout(700)}clearDl.mshot=0;await clearDl(60,'spot_'+id);L('7 조사 핫스폿',id,'탭',ok,'→ 획득',await T('G.found.indexOf("'+id+'")>=0'))}
await shot('after_spots');
// 새로고침 → 이어하기
const before=await T('JSON.stringify({loc:G.loc,found:G.found.length,asked:G.asked.length})');
await p.reload();await p.waitForTimeout(3000);
L('8 새로고침 후 메인:',JSON.stringify(await p.evaluate(()=>[...document.querySelectorAll('#innmain .menu button')].map(b=>b.textContent+(b.disabled?'(꺼짐)':'')+(b===document.activeElement?'(포커스)':'')))));await shot('main_withsave');
await tap('#innmain [data-m="cont"]');await p.waitForTimeout(2500);
L('9 이어하기:',await T('JSON.stringify({loc:G.loc,found:G.found.length,asked:G.asked.length,cold:!!document.getElementById("inncold"),dl:!!DL})'),'이전',before);await shot('continue');
// 새 게임 덮어쓰기 확인(취소 기본)
await p.reload();await p.waitForTimeout(3000);await tap('#innmain [data-m="new"]');await p.waitForTimeout(400);
L('10 저장 있을 때 새 게임:',await p.evaluate(()=>{var c=document.querySelector('.innconf');return c?c.innerText.replace(/\s+/g,' ')+' 기본 포커스='+document.activeElement.textContent:'확인창 없음'}));await shot('newgame_confirm');
await tap('.innconf [data-k="no"]');await p.waitForTimeout(300);L('   취소 후 저장 유지:',await p.evaluate(()=>!!window.__W209REAL.getItem('daae-inn1:daae-detective-v3')));
L('기본 게임 저장 그대로:',await p.evaluate(()=>window.__W209REAL.getItem('daae-detective-v3')==='{"marker":"REAL-SAVE"}'));
L('errs',JSON.stringify(errs),'MISS',await T('JSON.stringify({main:window.__INNMAIN_MISS,inn:window.__INNMISS})'));
require('fs').writeFileSync(O+'entry.log',log.join('\n'));await b.close()})();
