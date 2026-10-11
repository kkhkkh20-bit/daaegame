/* Preview-only, named scene shortcuts. The existing slot storage shim keeps
   every test save separate; navigation also disposes the old scene's timers. */
(function(){
 'use strict';
 if(!window.__EP1INN||!window.EP1INN)return;
 var ep=window.EP1INN,panel=null,opener=null,busy=false;
 var RETURN='inn-admin-return-url',PREFIX='daae-preview-ch1-gpt-20261008-admin-test:';
 var entries=[
  {id:'cold',group:'스토리',name:'오프닝',note:'자정의 기척부터',icon:'moon'},
  {id:'carriage',group:'스토리',name:'마차 · 마을',note:'엄마의 편지를 따라오는 길',icon:'book',sid:'P1'},
  {id:'welcome',group:'스토리',name:'여관 첫 만남',note:'엄마 사진과 할머니의 반응',icon:'door',sid:'P3'},
  {id:'night',group:'스토리',name:'밤 복도',note:'문 밑 빛 · 밤이 등장',icon:'moon',sid:'P10b'},
  {id:'report',group:'스토리',name:'도난 신고 · 수색',note:'주머니 신고부터 발견까지',icon:'search',sid:'P11'},
  {id:'investigation',group:'조사',name:'조사 시작',note:'증거를 찾기 전 상태',icon:'search'},
  {id:'discovery',group:'조사',name:'솜솜 발견',note:'돈 조사 뒤 · 침대 밑 연출',icon:'paw'},
  {id:'puzzle',group:'조사',name:'숫자 자물쇠',note:'머리판 날짜와 상자 조사',icon:'lock'},
  {id:'meeting',group:'회의 · 대결',name:'원탁 회의',note:'필요한 증거가 준비된 상태',icon:'people'},
  {id:'final',group:'회의 · 대결',name:'최종 대결',note:'까로의 증언까지 준비',icon:'speech'},
  {id:'ending',group:'후일담',name:'사건 뒤 일상',note:'너울의 처리 · 겨울 머무르기',icon:'book',end:0},
  {id:'mother',group:'후일담',name:'엄마의 글씨',note:'책과 장부를 직접 비교',icon:'book',end:3}
 ];
 var query=new URLSearchParams(location.search),entry=entries.find(function(x){return x.id===query.get('testScene')});
 var active=window.__QASLOT==='admin-test'&&!!entry;
 var paths={moon:'<path d="M20 15A8 8 0 0 1 9 4a8 8 0 1 0 11 11Z"/>',book:'<path d="M3 4h7l2 2 2-2h7v16h-7l-2 2-2-2H3zM12 6v16"/>',door:'<path d="M4 21h16M6 21V3h12v18M14 12h1"/>',search:'<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',paw:'<ellipse cx="12" cy="16" rx="6" ry="5"/><circle cx="4" cy="8" r="2"/><circle cx="10" cy="5" r="2"/><circle cx="16" cy="5" r="2"/><circle cx="21" cy="9" r="2"/>',lock:'<path d="M5 10h14v11H5zM8 10V6a4 4 0 0 1 8 0v4M12 14v3"/>',people:'<circle cx="12" cy="7" r="3"/><path d="M6 21v-5a6 6 0 0 1 12 0v5M2 20v-7M22 20v-7"/>',speech:'<path d="M3 3h18v14H9l-6 5zM7 8h10M7 12h7"/>'};
 function icon(k){return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+paths[k]+'</svg>'}
 function close(){if(!panel)return;panel.remove();panel=null;if(opener&&opener.isConnected)opener.focus();opener=null}
 function group(name){if(!panel)return;panel.querySelectorAll('[data-admin-group]').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.adminGroup===name))});panel.querySelectorAll('.admin-group').forEach(function(s){s.hidden=s.dataset.group!==name})}
 function open(from){if(panel)return;opener=from||document.activeElement;panel=document.createElement('div');panel.id='inn-admin';
  panel.innerHTML='<section role="dialog" aria-modal="true" aria-labelledby="inn-admin-title"><header><div><small>플레이테스트</small><h2 id="inn-admin-title">관리자 테스트</h2></div><button type="button" data-admin-close aria-label="관리자 테스트 닫기">×</button></header><p class="admin-note">장면을 고르면 바로 시작해요. 일반 플레이 저장은 따로 유지됩니다.</p><nav class="admin-tabs" aria-label="테스트 장면 분류"></nav><div class="admin-groups"></div><p class="admin-error" role="alert"></p></section>';
  var groups=panel.querySelector('.admin-groups');['스토리','조사','회의 · 대결','후일담'].forEach(function(name){var tab=document.createElement('button');tab.type='button';tab.dataset.adminGroup=name;tab.textContent=name;panel.querySelector('.admin-tabs').appendChild(tab);var s=document.createElement('section');s.className='admin-group';s.dataset.group=name;s.innerHTML='<h3>'+name+'</h3><div class="admin-grid"></div>';entries.filter(function(x){return x.group===name}).forEach(function(x){var b=document.createElement('button');b.type='button';b.dataset.adminScene=x.id;b.innerHTML=icon(x.icon)+'<span><b>'+x.name+'</b><small>'+x.note+'</small></span>';s.querySelector('.admin-grid').appendChild(b)});groups.appendChild(s)});group(active?entry.group:'스토리');
  document.body.appendChild(panel);panel.querySelector('[data-admin-close]').focus();
 }
 function error(t){if(panel)panel.querySelector('.admin-error').textContent=t;busy=false}
 function launch(id){if(busy||!entries.some(function(x){return x.id===id}))return;busy=true;
  try{
   if(!window.__W209SAFE||!window.__W209REAL)throw Error('storage isolation unavailable');
   if(!active){if(G&&S.screen==='case')saveProg();sessionStorage.setItem(RETURN,location.pathname+location.search)}
   // Only the test namespace is reset. Copy saved preferences, never progress.
   var real=window.__W209REAL,settings=real.getItem(window.__W209P+'inn_settings'),keys=[];
   for(var i=0;i<real.length;i++){var key=real.key(i);if(key&&key.indexOf(PREFIX)===0)keys.push(key)}
   keys.forEach(function(key){real.removeItem(key)});if(settings!==null)real.setItem(PREFIX+'inn_settings',settings);
   sessionStorage.removeItem('inn9seen-admin-test');
   var url=new URL(location.href);url.searchParams.set('slot','admin-test');url.searchParams.delete('qa');url.searchParams.set('testScene',id);location.replace(url.href);
  }catch(e){error('테스트 저장을 준비하지 못했어요. 다시 눌러 주세요.')}
 }
 function leave(){if(busy)return;busy=true;var url=new URL(location.href);url.searchParams.delete('testScene');url.searchParams.delete('slot');url.searchParams.delete('qa');
  try{var back=sessionStorage.getItem(RETURN);if(back){var savedUrl=new URL(back,location.href);if(savedUrl.origin===location.origin&&savedUrl.pathname===location.pathname)url=savedUrl}sessionStorage.removeItem(RETURN)}catch(e){}
  location.replace(url.href);
 }
 function setup(){var ci=CASES.findIndex(function(c){return c.id==='inn'}),g=fresh(ci),c=CASES[ci];g.introDone=true;g.beats={m151new:1,toFight:1,inn_admin_test:1};g.visited=c.locations.map(function(l,i){return i});g.loc=c.locations.findIndex(function(l){return l.id==='bed13'});g.who=null;
  if(entry.sid)g.beats.inn_pi=ep.PRO.findIndex(function(s){return s.sid===entry.sid});
  else if(entry.id!=='cold')g.beats.inn_pro=1;
  if(entry.id==='discovery'){g.found=['C01','C02','C09'];g.asked=['C03','C12'];g.beats.inn_discovery_return=1;g.exam.C01=true}
  if(entry.id==='puzzle'){g.found=['C01'];g.exam.C01=true}
  if(entry.id==='meeting'||entry.id==='final'||entry.end!=null){g.found=Object.keys(ep.EV);g.asked=['C03','C07','C12','C13','C14'];g.unlocked=c.locations.map(function(l){return l.req}).filter(Boolean);g.beats.inn_i9=1;g.beats.inn_basket_transferred=1;g.beats.inn_discovery_return=1;allSpots(c).forEach(function(s){g.exam[s.ev.id]=true})}
  if(entry.id==='final'||entry.end!=null){g.beats.inn_meet=1;g.beats.inn_meeting_version=ep.MEET.schemaVersion;g.beats.inn_life_confirmed=1;g.beats.inn_c13fix=1;g.beats.inn_show_geokkuri_C08=1}
  if(entry.end!=null){g.beats.inn_final=1;g.beats.inn_ei=entry.end;g.beats.inn_case_cleared=1;g.beats.inn_child_heard=1}
  S.prog.inn=g;
 }
 var main=window.__innMain;
 window.__innMain=function(boot){if(!active)return main.apply(this,arguments);
  if(!window.__W209SAFE||window.__W209P!==PREFIX)return main.apply(this,arguments);
  // The native boot cover can outlive DOM readiness. Start the selected scene
  // after it clears so its first sound, caption and discovery beat stay visible.
  function ready(){if(document.getElementById('bootld')){setTimeout(ready,100);return}
   setup();if(entry.id==='cold'){window.__innCold(boot);return}boot();
   if(entry.id==='meeting')setTimeout(function(){if(G&&G.beats.inn_admin_test)window.__rtOpen(CASES[G.ci])},450);
   if(entry.id==='discovery')setTimeout(function(){if(G&&G.beats.inn_admin_test)window.__innDiscover()},450);
  }ready();
 };
 function sync(){
  var menu=document.querySelector('#w209more');if(menu&&!menu.querySelector('[data-admin-open]')){var section=document.createElement('div');section.className='admin-entry';section.innerHTML='<small>플레이테스트</small><button type="button" data-admin-open>'+icon('lock')+'관리자 테스트</button>';var closeButton=Array.from(menu.children).find(function(n){return n.tagName==='BUTTON'&&!n.dataset.w});menu.insertBefore(section,closeButton||null)}
  var settings=document.querySelector('#innopt .rows');if(settings&&!settings.querySelector('[data-admin-open]')){var section=document.createElement('div');section.className='admin-entry';section.innerHTML='<small>플레이테스트</small><button type="button" data-admin-open>'+icon('lock')+'관리자 테스트<span>장면 바로가기 ›</span></button>';settings.appendChild(section)}
  if(active&&!document.getElementById('inn-admin-status')){var badge=document.createElement('div');badge.id='inn-admin-status';badge.innerHTML='<span>테스트 · '+entry.name+'</span><button type="button" data-admin-open>장면 선택</button><button type="button" data-admin-return>일반 플레이로</button>';document.body.appendChild(badge)}
 }
 window.addEventListener('click',function(e){var t=e.target&&e.target.closest&&e.target.closest('[data-admin-open],[data-admin-scene],[data-admin-group],[data-admin-close],[data-admin-return]');if(t){e.preventDefault();e.stopImmediatePropagation();if(t.hasAttribute('data-admin-open')){var rail=document.getElementById('w209rail');if(rail)rail.classList.remove('more');open(t)}else if(t.hasAttribute('data-admin-group'))group(t.dataset.adminGroup);else if(t.hasAttribute('data-admin-close'))close();else if(t.hasAttribute('data-admin-return'))leave();else launch(t.dataset.adminScene);return}if(panel&&e.target===panel){e.preventDefault();e.stopImmediatePropagation();close()}else if(panel&&panel.contains(e.target)){e.stopImmediatePropagation()}},true);
 ['pointerdown','pointerup','touchstart','touchend'].forEach(function(type){window.addEventListener(type,function(e){var t=e.target;if(panel&&panel.contains(t)||t.closest&&t.closest('#inn-admin-status,[data-admin-open]'))e.stopPropagation()},{capture:true,passive:true})});
 window.addEventListener('keydown',function(e){var inControl=e.target&&e.target.closest&&e.target.closest('#inn-admin-status,[data-admin-open]');if(!panel&&!inControl)return;e.stopImmediatePropagation();if(e.key==='Escape'&&panel){e.preventDefault();close();return}if((e.key==='Enter'||e.key===' ')&&e.target.tagName==='BUTTON'){e.preventDefault();e.target.click();return}if(e.key==='Tab'&&panel){var bs=Array.from(panel.querySelectorAll('button:not([disabled])')).filter(function(b){return b.getClientRects().length}),first=bs[0],last=bs[bs.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}},true);
 var pending=false;new MutationObserver(function(){if(pending)return;pending=true;requestAnimationFrame(function(){pending=false;sync()})}).observe(document.body,{childList:true,subtree:true});sync();
 var css=document.createElement('style');css.textContent=`
 .admin-entry{border-top:1px dashed #9d8763;margin-top:9px;padding-top:9px}.admin-entry>small{display:block;color:#bbaa85;font-size:12px;margin:0 0 5px}.admin-entry button{display:flex!important;align-items:center;gap:8px;font:inherit;min-height:44px;border:1px solid #9e875c;background:#292e2d;color:#f0dfba;cursor:pointer;padding:8px 12px;width:100%;text-align:left}.admin-entry svg{width:20px;height:20px;flex:none}.admin-entry button span{margin-left:auto;font-size:12px;color:#d4c29d}
 #innopt .rows{overflow-y:auto;min-height:0;justify-content:flex-start;padding:8px 0}#innopt .row,#innopt .admin-entry{flex:none}#innopt .admin-entry{margin-top:14px}#innopt .admin-entry button{background:#292e2d!important;color:#f0dfba!important}
 #inn-admin{position:fixed;inset:0;z-index:300;background:#100e13c9;display:grid;place-items:center;font-family:var(--display,Galmuri11,sans-serif);color:#f1e6cc}#inn-admin>section{width:min(720px,calc(100vw - 28px));max-height:calc(100dvh - 24px);overflow-y:auto;box-sizing:border-box;background:#292b28;border:2px solid #b69b68;box-shadow:0 8px 35px #0009;padding:16px}#inn-admin header{display:flex;align-items:center;justify-content:space-between}#inn-admin header small{font-size:12px;color:#d7b97e}#inn-admin h2{margin:4px 0;font-size:22px}#inn-admin button{font:inherit;cursor:pointer}#inn-admin [data-admin-close]{width:44px;height:44px;border:1px solid #8d805f;color:#f1e6cc;background:#383d34;font-size:24px}#inn-admin .admin-note{font-size:13px;line-height:1.6;color:#d2c4a6;margin:10px 0}#inn-admin h3{font-size:13px;font-weight:normal;color:#d7b97e;margin:14px 0 7px}#inn-admin .admin-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px}#inn-admin [data-admin-scene]{display:flex;align-items:center;gap:9px;min-height:62px;border:1px solid #7f765c;background:#353b32;color:#f3e7cd;padding:9px;text-align:left}#inn-admin [data-admin-scene]:hover,#inn-admin button:focus-visible{outline:2px solid #e4c886;outline-offset:2px;background:#414c3b}#inn-admin [data-admin-scene] svg{width:23px;height:23px;flex:none}#inn-admin [data-admin-scene] b{display:block;font-size:14px;font-weight:normal}#inn-admin [data-admin-scene] small{display:block;font-size:11px;line-height:1.5;color:#ccbf9c;margin-top:5px}#inn-admin .admin-error{color:#ffbaac;font-size:13px;min-height:0}
 #inn-admin-status{position:fixed;z-index:230;top:5px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:6px;max-width:calc(100vw - 170px);padding:4px 7px;background:#252e2bed;border:1px solid #ab976c;color:#f2e0ad;font:12px var(--display,Galmuri11,sans-serif)}#inn-admin-status span{white-space:nowrap}#inn-admin-status button{font:inherit;min-height:32px;border:1px solid #887a55;background:#384336;color:#f2e5c3;padding:4px 7px;cursor:pointer;white-space:nowrap}
 #inn-admin .admin-tabs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:5px}#inn-admin .admin-tabs button{min-height:40px;border:1px solid #847758;background:#242922;color:#d3c39f;font-size:13px}#inn-admin .admin-tabs button[aria-pressed=true]{background:#d9c598;color:#302c24;border-color:#eedbb2}
 @media(max-width:550px){#inn-admin .admin-grid{grid-template-columns:repeat(2,minmax(0,1fr))}#inn-admin-status{max-width:calc(100vw - 12px);top:47px}#inn-admin-status span{display:none}}`;
 document.head.appendChild(css);
})();
