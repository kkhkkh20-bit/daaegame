/* 1장 이동: 기존 data-i/이동 핸들러를 보존하는 층별 공간 안내. */
(function(){
 var active=null,scheduled=false;
 var ROOMS={bed13:['열세 번째 침대','bed'],hall:['2층 복도','hall'],dotoroom:['도토의 방','room'],front:['접수대','desk'],dining:['식당','table'],kitchen:['부엌','pot'],plaza:['여관 밖','tree']};
 var GOALS={bed13:'방 안의 물건을 직접 살펴보자.',hall:'복도에서 물건을 살펴보고, 만난 사람에게 이야기하자.',dotoroom:'도토의 날씨 일지를 확인해 보자.',front:'접수대의 기록을 살펴보고 이야기를 들어보자.',dining:'식당에 있는 사람들의 말을 들어보자.',kitchen:'부엌에 있는 사람들에게 이야기를 들어보자.',plaza:'여관 밖에도 들러 주변을 살펴보자.'};
 var EVIDENCE_ROOMS={bed13:['C01','C02','C04','C05','C11'],hall:['C06','C07','C13'],dotoroom:['C08'],front:['C09','C10'],dining:['C12'],kitchen:['C03'],plaza:[]};
 var PATH={bed:'M3 18V9h4v5h14v4M3 12h18M7 9h5v5M3 18v3M21 18v3',hall:'M3 20V4h18v16M7 20V8h10v12M12 8v12',room:'M5 21V3h14v18M9 15h1M3 21h18',desk:'M3 11h18v10H3zM6 11V6h12v5M8 16h8',table:'M3 9h18v4H3zM6 13v8M18 13v8M7 3v6M17 3v6',pot:'M5 10h14v10H5zM3 12h2M19 12h2M7 6h10M12 3v3',tree:'M12 2L4 13h5l-3 5h5v4h2v-4h5l-3-5h5z',pin:'M12 21s7-7 7-12a7 7 0 10-14 0c0 5 7 12 7 12zM10 9h4',check:'M4 12l5 5L20 6',clue:'M7 3h10v18H7zM10 7h4M10 11h4M10 15h4'};
 function icon(k){return '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="'+(PATH[k]||PATH.room)+'"/></svg>'}
 function current(){try{return S.screen==='case'&&G&&CASES[G.ci].id==='inn'}catch(e){return false}}
 function close(d){var b=d&&d.querySelector('[data-x]');if(b)b.click()}
 function purpose(){
  var found=G.found||[];
  if(G.innfinal&&!G.innfinal.done&&G.innfinal.pi===3&&found.indexOf('C14')<0)return '여관 밖 까로에게 세련 손님을 묻자. 이미 들었다면 숙박부를 보여주자.';
  if(found.indexOf('C04')>=0&&!(G.beats||{}).inn_life_confirmed&&!(G.beats||{}).inn_meet)return '모두 식당에 모여 작은 손님부터 살펴보자.';
  if(found.indexOf('C04')<0&&window.__innDiscoveryReady&&window.__innDiscoveryReady())return '밝아진 아침. 열세 번째 침대의 어두웠던 곳을 다시 살펴보자.';
  /* 찾은 정보만 연결한다. 기록 내용과 사건의 답은 안내에 넣지 않는다. */
  if(found.indexOf('C06')>=0&&found.indexOf('C08')<0)return '시간을 더 확인하려면 도토의 날씨 일지를 살펴보자.';
  if(found.length)return '살펴본 물건과 사람들의 말을 비교해 보자. 다른 방에도 들러볼까?';
  return '방을 골라 물건을 살펴보고, 만난 사람에게 이야기를 들어보자.';
 }
 function enhance(d){
  if(d.dataset.spaceMap)return;
  d.dataset.spaceMap='1';d.setAttribute('aria-modal','true');d.setAttribute('aria-labelledby','inn-map-title');d.setAttribute('aria-describedby','inn-map-purpose');
  var hd=d.querySelector('.hd b');if(hd){hd.id='inn-map-title';hd.textContent='여관 공간 지도'}
  var ls=d.querySelector('.ls');if(!ls)return;
  var buttons=Array.from(ls.querySelectorAll('button[data-i]'));
  var guide=document.createElement('p');guide.id='inn-map-purpose';guide.className='map-purpose';guide.textContent=purpose();d.querySelector('.hd').after(guide);
  var floors=[['2층',['bed13','hall','dotoroom']],['1층',['front','dining','kitchen']],['여관 밖',['plaza']]];
  ls.replaceChildren();
  floors.forEach(function(f,fi){
   var row=document.createElement('section');row.className='map-floor'+(fi===2?' outside':'');row.setAttribute('aria-label',f[0]);
   var title=document.createElement('b');title.className='map-floor-title';title.textContent=f[0];row.appendChild(title);
   var grid=document.createElement('div');grid.className='map-rooms';row.appendChild(grid);
   f[1].forEach(function(id){var b=buttons.find(function(btn){var l=CASES[G.ci].locations[+btn.dataset.i];return l&&l.id===id});if(!b)return;
    var l=CASES[G.ci].locations[+b.dataset.i],r=ROOMS[id],here=+b.dataset.i===G.loc,visit=(G.visited||[]).indexOf(+b.dataset.i)>=0;
    var acquired=(EVIDENCE_ROOMS[id]||[]).filter(function(eid){return (G.found||[]).indexOf(eid)>=0});visit=visit||acquired.length>0;
    var state=here?'지금 여기':visit?'다녀온 곳':'아직 안 감';
    b.classList.add('map-room');b.dataset.roomId=id;b.innerHTML='<span class="map-room-icon">'+icon(r[1])+'</span><span class="map-room-name">'+r[0]+'</span><small class="map-room-state">'+icon(here?'pin':visit?'check':'room')+state+'</small>'+(acquired.length?'<small class="map-room-clues">'+icon('clue')+'단서 '+acquired.length+'</small>':'');
    b.setAttribute('aria-label',r[0]+', '+state+(acquired.length?', 확보한 단서 '+acquired.length+'개':''));
    if(acquired.length)b.title=acquired.map(function(eid){try{return EP.EV[eid].name}catch(e){return eid}}).join(' · ');
    b.setAttribute('aria-describedby','inn-map-purpose');
    b.addEventListener('focus',function(){guide.textContent=GOALS[id]||purpose()});
    b.addEventListener('pointerenter',function(){guide.textContent=GOALS[id]||purpose()});
    grid.appendChild(b);
   });
   if(grid.children.length)ls.appendChild(row);
  });
  var wm=d.querySelector('[data-map]');if(wm)wm.hidden=true; // 이 이동 화면에서 지도 두 단계를 만들지 않는다.
  var legend=document.createElement('p');legend.className='map-legend';legend.innerHTML=icon('pin')+'현재 위치 '+icon('check')+'다녀온 곳 '+icon('clue')+'확보한 단서';d.appendChild(legend);
  var footer=document.createElement('small');footer.className='map-footnote';footer.textContent='갈 수 있는 방만 표시돼요 · 방 아이콘을 누르면 이동';d.appendChild(footer);
  d.addEventListener('keydown',function(e){
   if(e.key!=='Tab')return;
   var all=Array.from(d.querySelectorAll('button:not([disabled])')).filter(function(b){return !b.hidden&&b.getClientRects().length});if(!all.length)return;
   var first=all[0],last=all[all.length-1];
   if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}
   else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}
  });
  var first=d.querySelector('button[data-i]:not([disabled])')||d.querySelector('[data-x]');if(first)first.focus({preventScroll:true});guide.textContent=purpose();
 }
 function sync(){scheduled=false;if(!current())return;var d=document.getElementById('innmove');
  /* 다른 전체 지도가 열린 경우 현재 목록은 원래 닫기 핸들러로 정리. */
  if(d&&document.getElementById('wmap')){close(d);d=null}
  if(d){enhance(d);active=d}
  else if(active){active=null;var b=document.querySelector('#w209rail .g>[data-w="move"]');if(b&&document.activeElement===document.body)b.focus({preventScroll:true})}
 }
 function schedule(){if(!scheduled){scheduled=true;requestAnimationFrame(sync)}}
 new MutationObserver(schedule).observe(document.body,{childList:true,subtree:true});
 var style=document.createElement('style');style.id='inn-map-navigation-style';style.textContent=[
  '#innmove[data-space-map]{top:60px!important;left:50%!important;right:auto!important;transform:translateX(-50%);width:min(650px,calc(100vw - 24px))!important;max-height:calc(100dvh - 72px)!important;padding:12px!important;background:#faf1da!important;border:3px solid #96713e!important;box-shadow:0 8px 28px #24170870!important;color:#463423!important;border-radius:14px!important;overflow:auto!important;font:14px/1.4 var(--display,Galmuri11,sans-serif)}',
  'html body.w209.inn1 #innmove[data-space-map] .hd{margin:0!important;background:transparent!important;border:0!important;box-shadow:none!important}html body.w209.inn1 #innmove[data-space-map] .hd b{color:#4e3823!important;font-size:17px!important}html body.w209.inn1 #innmove[data-space-map] .hd button{min-width:44px!important;min-height:44px!important;color:#4e3823!important;border-radius:8px!important}',
  '#innmove[data-space-map] .map-purpose{box-sizing:border-box;min-height:3.8em;margin:0 0 10px;padding:7px 10px;border-radius:7px;background:#e9ddbf;color:#5d4630;font-size:13px;word-break:keep-all}',
  '#innmove[data-space-map] .ls{display:flex!important;flex-direction:column!important;gap:8px!important}',
  '#innmove[data-space-map] .map-floor{position:relative;padding:6px 8px 8px;border:1px solid #c7ae80;border-radius:8px;background:#f0e3c8}',
  '#innmove[data-space-map] .map-floor-title{display:block;color:#74512d;font-size:12px;margin:0 0 4px;font-weight:400}',
  '#innmove[data-space-map] .map-rooms{position:relative;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}',
  '#innmove[data-space-map] .map-rooms:before{content:"";position:absolute;top:38px;left:15%;right:15%;height:4px;background:#b49667}',
  '#innmove[data-space-map] .ls .map-room{position:relative;display:flex!important;flex-direction:column!important;justify-content:center!important;align-items:center!important;gap:3px!important;min-height:86px!important;min-width:44px!important;padding:6px 4px!important;background:#fffaf0!important;color:#473321!important;border:2px solid #b5945e!important;border-radius:8px!important;text-align:center!important;box-shadow:0 2px 0 #c2a374;font-size:14px!important;line-height:1.3!important}',
  '#innmove[data-space-map] .ls .map-room[aria-current]{background:#e2ead6!important;border-color:#637749!important;color:#374329!important;opacity:1!important}',
  '#innmove[data-space-map] .map-room-icon{line-height:0!important}#innmove[data-space-map] .map-room-icon svg{display:block;width:25px;height:25px}#innmove[data-space-map] .map-room-name{word-break:keep-all}',
  '#innmove[data-space-map] .ls .map-room small{display:flex;gap:3px;align-items:center;font-size:11px!important;line-height:1.3!important;color:#6a573b!important}#innmove[data-space-map] .map-room small svg{width:12px;height:12px;flex:none}',
  '#innmove[data-space-map] .outside .map-rooms{grid-template-columns:minmax(0,1fr);max-width:190px;margin:auto}#innmove[data-space-map] .outside .map-rooms:before{display:none}',
  '#innmove[data-space-map] .map-legend{display:flex;justify-content:center;align-items:center;gap:5px;flex-wrap:wrap;font-size:11px;color:#715c3e;margin:8px 0 4px}#innmove[data-space-map] .map-legend svg{width:13px;height:13px}',
  '#innmove[data-space-map] .map-footnote{display:block;text-align:center;font-size:11px;color:#79674c}#innmove[data-space-map] [data-map]{display:none!important}',
  '#innmove[data-space-map] button:focus-visible{outline:3px solid #ad5f27!important;outline-offset:2px}',
  '@media(max-height:440px){#innmove[data-space-map]{top:58px!important;padding:8px!important;max-height:calc(100dvh - 66px)!important}html body.w209.inn1 #innmove[data-space-map] .hd button{min-height:44px!important}#innmove[data-space-map] .map-purpose{min-height:2.4em;margin-bottom:6px;padding:4px 8px}#innmove[data-space-map] .ls{display:grid!important;grid-template-columns:1fr 1fr!important;gap:6px!important}#innmove[data-space-map] .outside{grid-column:1/-1;padding:4px 8px!important}#innmove[data-space-map] .outside .map-room{min-height:44px!important;flex-direction:row!important;gap:8px!important}#innmove[data-space-map] .ls .map-room{min-height:68px!important;font-size:12px!important}#innmove[data-space-map] .map-floor{padding:4px 6px 6px}#innmove[data-space-map] .map-rooms{gap:6px}#innmove[data-space-map] .map-room-icon svg{width:22px;height:22px}#innmove[data-space-map] .map-legend{display:none!important}#innmove[data-space-map] .map-footnote{display:none!important}#innmove[data-space-map] .ls .outside .map-room{min-height:44px!important}}',
  '@media(prefers-reduced-motion:no-preference){#innmove[data-space-map]{animation:innMapOpen .16s ease-out}@keyframes innMapOpen{from{opacity:0;translate:0 4px}to{opacity:1;translate:0 0}}}'
 ].join('\n');document.head.appendChild(style);schedule();
})();
