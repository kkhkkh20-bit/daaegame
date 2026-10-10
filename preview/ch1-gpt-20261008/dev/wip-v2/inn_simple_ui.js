/* Chapter 1: decorate native controls; never replace their input handlers or proof state. */
(function(){
 function own(){return !!(G&&CASES[G.ci]&&CASES[G.ci].id==='inn')}
 var PATH={
  scene:'<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',
  move:'<path d="m3 5 6-2 6 2 6-2v16l-6 2-6-2-6 2zM9 3v16M15 5v16"/>',
  ev:'<path d="M5 7h14v14H5zM8 7V3h8v4M8 12h8M8 16h5"/>',
  rec:'<path d="M4 3h16v18H4zM8 7h8M8 11h8M8 15h5"/>',
  press:'<path d="M3 4h18v12H10l-5 5v-5H3zM8 8h8M8 12h5"/>',
  next:'<path d="m8 4 9 8-9 8"/>',
  present:'<path d="M3 14h9l3-3h6v7l-5 3H8l-5-3zM10 3h9v7h-9z"/>',
  back:'<path d="m10 4-7 7 7 7M3 11h12a6 6 0 0 1 6 6"/>',
  hint:'<path d="M8 17h8M9 21h6M8 14a7 7 0 1 1 8 0v3H8z"/>',
  leave:'<path d="M13 3H4v18h9M10 12h11m-5-5 5 5-5 5"/>',
  log:'<path d="M5 3h14v18H5zM8 7h8M8 11h8M8 15h5"/>',
  more:'<circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/>'
 };
 function icon(key){return '<svg class="simple-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+(PATH[key]||PATH.ev)+'</svg>'}
 var SHORT={C01:"주머니",C02:"손자국",C03:"나비의 말",C04:"손님",C05:"붉은 털",C06:"시계",C07:"잠자리",C08:"첫눈 일지",C09:"숙박부",C10:"발견 기록",C11:"옛 장부",C12:"세련의 말",C13:"목격담"};
 var LABEL={scene:['조사','장면 조사'],move:['이동','장소 이동'],ev:['증거','증거 보기'],rec:['증언','주민의 증언 기록'],press:['질문','발언 되묻기'],next:['다음','다음 발언 듣기'],present:['제시','선택한 증거 제시하기'],back:['취소','증거 선택 취소하고 회의로'],hint:['도움','추리 도움말'],leave:['조사','조사로 돌아가기'],log:['기록','공개 발언 기록 열기'],more:['메뉴','게임 메뉴']};
 function decorate(b,key){var spec=LABEL[key];if(!b||!spec)return;
  if(b.querySelector('.simple-icon'))return;
  var badge=b.querySelector('.n'),badgeCopy=badge&&badge.cloneNode(true);
  b.innerHTML=icon(key)+'<span class="simple-label">'+spec[0]+'</span>';
  if(badgeCopy)b.appendChild(badgeCopy);
  b.setAttribute('aria-label',spec[1]);b.title=spec[1];
 }
 var style=document.createElement('style');style.id='inn-simple-ui-style';style.textContent=`
 html body.inn1 #logic-note{display:none!important}
 html body.inn1 .simple-icon{width:25px!important;height:25px!important;flex:none;pointer-events:none}
 html body.inn1 .simple-label{font:12px/1.2 var(--display,sans-serif)!important;white-space:nowrap;pointer-events:none}
 html body.inn1 #w209rail .g>button,html body.inn1 #rtgbar button,html body.inn1 #rtgtr button{min-width:44px!important;min-height:44px!important;border:1px solid #aa915f!important;border-image:none!important;background:#f2e6cc!important;color:#493725!important;box-shadow:0 2px 0 #604c32!important;border-radius:5px!important;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:5px 8px!important}
 html body.inn1 #w209rail .g>button.on,html body.inn1 #rtgbar button.rtghot{background:#e4cb8b!important;outline:2px solid #ad7e32}
 html body.inn1 #w209rail .g>button:disabled,html body.inn1 #rtgbar button:disabled,html body.inn1 #rtgtr button:disabled{opacity:.45!important}
 html body.inn1 #rtgbar{left:50%!important;right:auto!important;bottom:8px!important;transform:translateX(-50%)!important;gap:8px!important;width:auto!important;max-width:calc(100vw - 16px)}
 html body.inn1 #rtgbar button{width:72px!important;height:58px!important;min-width:72px!important}
 html body.inn1 #rtgbar [data-g=obj]{display:none!important}
 html body.inn1 #rtgbar button[style*="display: none"],html body.inn1 #rtgtr button[style*="display: none"]{display:none!important}
 html body.inn1 #rtgtr{gap:5px!important;top:8px!important;right:8px!important}
 html body.inn1 #rtgtr button{width:48px!important;height:48px!important;padding:3px!important}
 html body.inn1 #rtgtr .simple-icon{width:21px!important;height:21px!important}
 html body.inn1 #rtgtr .simple-label{font-size:11px!important}
 html body.inn1 #rtgbar button::before,html body.inn1 #rtgbar button::after,html body.inn1 #rtgtr button::before,html body.inn1 #rtgtr button::after{display:none!important}
 html body.inn1 #rtgbar button:focus-visible,html body.inn1 #rtgtr button:focus-visible,html body.inn1 #w209rail button:focus-visible,html body.inn1 .rt-bul button:focus-visible,html body.inn1 #rtexam:focus-visible,html body.inn1 #rtgvote [data-pick]:focus-visible{outline:3px solid #bd7730!important;outline-offset:2px!important}
 html body.inn1.rtg.rtg-drw .rt-bul{left:calc(36vw + 12px)!important;right:8px!important;bottom:78px!important;top:156px!important;width:auto!important;max-height:none!important;height:auto!important;display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr));align-content:start;gap:7px!important;background:#e9dab8!important;border:2px solid #aa915f!important;border-radius:6px!important;overflow:auto!important;padding:9px!important}
 html body.inn1.rtg.rtg-drw .rt-bul .bl{display:flex!important;flex-direction:column;justify-content:center;align-items:center;gap:4px;min-height:86px!important;min-width:0!important;padding:6px!important;background:#faf2df!important;color:#493725!important;border:1px solid #af996a!important;border-radius:5px!important;text-align:center!important;box-shadow:none!important;font-size:12px!important}
 html body.inn1.rtg.rtg-drw .rt-bul .bl.on{background:#e2c97e!important;outline:2px solid #a5772e!important}
 html body.inn1.rtg.rtg-drw .rt-bul .bl .evic{display:block!important;width:42px!important;height:42px!important;flex:none}
 html body.inn1.rtg.rtg-drw .rt-bul .bl>span{font:12px/1.3 var(--display,sans-serif)!important;word-break:keep-all;white-space:normal}
 html body.inn1.rtg.rtg-drw .rt-evd{display:block!important;left:8px!important;right:auto!important;top:156px!important;bottom:78px!important;width:36vw!important;max-height:none!important;overflow:auto!important;padding:10px!important;background:#faf2df!important;color:#493725!important;border:2px solid #aa915f!important;box-sizing:border-box!important}
 html body.inn1.rtg.rtg-drw .rt-evd>.evic{width:62px!important;height:62px!important;display:block!important;margin:0 auto 8px!important}
 html body.inn1.rtg.rtg-drw .rt-evd p{font-size:14px!important;line-height:1.55!important;word-break:keep-all}
 html body.inn1 #rtexam{position:sticky!important;bottom:0!important;min-height:44px!important;width:100%;background:#e4cb8b!important;color:#493725!important;border:1px solid #aa915f!important;white-space:normal}
 html body.inn1 #rtg .seat .vt9{display:flex!important;align-items:center;justify-content:center;gap:2px;padding:2px 4px!important;min-width:30px;background:#f4e8cc!important;color:#493725!important;border:1px solid #b99b61!important}
 html body.inn1 #rtg .seat .vt9 svg,html body.inn1 #rtg .seat .vt9 img{width:23px!important;height:23px!important;flex:none}
 html body.inn1 #rtg .seat .vt9 span{font:10px/1.2 var(--display,sans-serif)}
 html body.inn1 #rtgvote [data-pick]{min-height:60px!important;min-width:70px!important;display:inline-flex!important;flex-direction:column;align-items:center;justify-content:center;gap:3px;padding:5px!important;white-space:normal}
 html body.inn1 #rtgvote [data-pick] svg,html body.inn1 #rtgvote [data-pick] img{width:36px!important;height:36px!important}
 html body.inn1 #simple-drawer-claim{display:none!important;position:fixed;z-index:64;left:8px;right:8px;top:72px;height:76px;box-sizing:border-box;padding:7px 10px;overflow:auto;overscroll-behavior:contain;background:#faf2df;border:2px solid #aa915f;border-radius:6px;color:#493725;font:14px/1.4 var(--display,sans-serif)}
 html body.inn1.rtg.rtg-drw:not(.rtgq-on) #simple-drawer-claim{display:block!important}
 html body.inn1:has(.rt-mid.vote) #simple-drawer-claim{display:none!important}
 html body.inn1 #simple-drawer-claim b{display:block;color:#795021;font-size:12px;margin-bottom:3px}
 html body.inn1 #simple-drawer-claim p{margin:0;word-break:keep-all}
 html body.inn1.rtg-drw #rtgtal{display:none!important}
 html body.inn1.rtg.rtg-drw .rt .rt-bub.stm{visibility:hidden!important}
 html body.inn1.rtg .rt .rt-nav{display:none!important}
 @media(max-height:450px){html body.inn1.rtg.rtg-drw .rt-evd>.evic{width:40px!important;height:40px!important;margin:0 auto 4px!important}}
 @media(max-width:550px){
  html body.inn1 #simple-drawer-claim{top:112px;height:74px}
  html body.inn1.rtg:not(.rtg-drw) .rt .rt-bub,html body.inn1.rtg #rtgq{top:clamp(120px,15vh,160px)!important;left:12px!important;right:12px!important;width:calc(100vw - 24px)!important;max-width:none!important;transform:none!important;max-height:calc(100vh - 220px)!important;overflow-y:auto!important;box-sizing:border-box!important}

  html body.inn1.rtg.rtg-drw .rt-evd{left:8px!important;right:8px!important;top:194px!important;bottom:auto!important;width:calc(100vw - 16px)!important;height:24vh!important;max-height:24vh!important;min-height:90px}
  html body.inn1.rtg.rtg-drw .rt-bul{left:8px!important;right:8px!important;top:calc(194px + 24vh + 8px)!important;bottom:78px!important;grid-template-columns:repeat(3,minmax(0,1fr))}
  html body.inn1 #rtgbar{gap:7px!important}html body.inn1 #rtgbar button{width:70px!important;min-width:70px!important}
  html body.inn1 #rtgtop{max-width:calc(100vw - 172px)!important;overflow:hidden!important}
  html body.inn1 #rtgvote .pk{display:flex!important;flex-wrap:wrap!important;justify-content:center;gap:5px}
 }
 `;document.head.appendChild(style);
 function decorateVotes(){var v=G.beats&&G.beats.rtVotes;if(!v)return;
  document.querySelectorAll('#rtg .seat[data-k] .vt9').forEach(function(b){var seat=b.closest('[data-k]'),target=v[seat.dataset.k];if(!target)return;
   var labels={innma:'할머니',seryeon:'세련','부녀':'부녀','기권':'기권'},label=labels[target]||target,k=target==='부녀'?'det1':target;
   b.setAttribute('aria-label',((CAST[seat.dataset.k]||{}).name||seat.dataset.k)+'의 의심 대상: '+label);b.setAttribute('role','img');b.title=b.getAttribute('aria-label');
   if(b.dataset.simpleVote===target&&b.querySelector('.simple-vote-label'))return;b.dataset.simpleVote=target;
   var face='';try{if(target!=='기권')face=pf(k,'')}catch(e){}
   b.innerHTML=face+'<span class="simple-vote-label">'+esc(label)+'</span>';
  });
 }
 function drawerClaim(){var stmt=document.querySelector('body>.rt .rt-bub.stm'),queue=document.querySelector('#rtgq'),open=own()&&document.body.classList.contains('rtg-drw')&&stmt&&!queue&&!document.querySelector('body>.rt #rtnext,body>.rt .rt-mid.vote');
  var box=document.getElementById('simple-drawer-claim');if(!open){if(box)box.remove();return}
  var heading=stmt.querySelector('small'),paragraph=stmt.querySelector('p'),who=heading?heading.cloneNode(true):null;
  if(who){var counter=who.querySelector('em');if(counter)counter.remove()}
  var name=who?who.textContent.trim():'현재 발언',line=paragraph?paragraph.textContent.trim():'';
  if(!box){box=document.createElement('section');box.id='simple-drawer-claim';box.setAttribute('aria-label','비교할 현재 발언');document.body.appendChild(box)}
  var key=name+'|'+line;if(box.dataset.claim===key)return;box.dataset.claim=key;box.innerHTML='<b>'+esc(name)+'의 말</b><p>'+esc(line)+'</p>';
 }
 function sync(){if(!own()){var old=document.getElementById('simple-drawer-claim');if(old)old.remove();return}
  document.querySelectorAll('#w209rail .g>[data-w]').forEach(function(b){decorate(b,b.dataset.w)});
  decorate(document.querySelector('#w209rail [data-more]'),'more');
  document.querySelectorAll('#rtgbar [data-g],#rtgtr [data-g]').forEach(function(b){decorate(b,b.dataset.g)});
  document.querySelectorAll('body>.rt .rt-bul [data-bl]').forEach(function(b){var id=b.dataset.bl,x=(window.EP1INN.EV||{})[id];if(x){var full=x.full||x.name;b.setAttribute('aria-label',full+' 선택');b.title=full;var label=b.querySelector(':scope>span');if(label&&label.textContent!==(SHORT[id]||x.name))label.textContent=SHORT[id]||x.name}});
  document.querySelectorAll('#rtgvote [data-pick]').forEach(function(b){var k=b.dataset.pick;if(b.querySelector('.simple-pick-name'))return;var name=(CAST[k]||{}).name||b.textContent;var face='';try{face=pf(k,'')}catch(e){}b.innerHTML=face+'<span class="simple-pick-name">'+esc(name)+'</span>';b.setAttribute('aria-label',name+' 지목')});
  decorateVotes();drawerClaim();
 }
 document.addEventListener('click',function(e){if(own()&&e.target.closest&&e.target.closest('#rtgbar [data-g="back"]')&&window.__rtClearSel)window.__rtClearSel()},true);
 setInterval(sync,180);
})();
