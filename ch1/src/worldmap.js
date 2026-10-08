/* 전체 지도(승인 시안 v1) — 가로 시험본의 '이동' 화면을 대신 보여 준다
   - 지형·좌표는 시안 manifest(1280x720, 배경 drawRect 64,36,1152,648, 3배) 그대로. 화면 크기에 맞춰 같은 비율로 축소(contain).
   - 이름표·상단 바·하단 띠는 읽기 좋게 고정 CSS 크기, 터치 영역은 44px 이상.
   - 장소 연결은 지금 사건의 실제 장소 id만. 연결 안 된 장소는 흐리게, 선택해도 이동 버튼이 꺼져 있다(새 경로·잠금 해제 없음).
   - 선택만으로는 이동하지 않는다. '이동' 버튼을 눌러야 기존 지도 이동(g.mvp 클릭)을 그대로 실행한다. */
(function(){
 var MISS=window.__WMAP=[],B=document.body;
 var NODES=[["inn","여관",396,458],["post-office","우체국",386,257],["record-room","기록실",614,239],["plaza-fountain","광장",615,402],["warehouse","창고",865,438],["mine-entrance","광산",1000,218]];
 /* 사건별 연결: 장소 id → 지도 장소. 여관 사건은 방들이 모두 여관 안이라 여관을 고르면 방을 고른다 */
 var LINK={envelope:{post:"post-office",store:"warehouse",records:"record-room"},
  inn:{bed13:"inn",dining:"inn",kitchen:"inn",hall:"inn",dotoroom:"inn",front:"inn"}};
 var css=document.createElement("style");css.textContent=[
  "#wmap{position:fixed;inset:0;z-index:45;background:#22301F;overflow:hidden;font-family:var(--display,sans-serif)}",
  "#wmap .cv{position:absolute;left:50%;top:50%;transform-origin:0 0}",
  "#wmap .bd{position:absolute;image-rendering:pixelated}",
  "#wmap .nd{position:absolute;transform:translate(-50%,-100%);display:flex;flex-direction:column;align-items:center;cursor:pointer;-webkit-tap-highlight-color:transparent}",
  "#wmap .nd img{display:block;image-rendering:pixelated;pointer-events:none}",
  "#wmap .nd .br{position:absolute;inset:-4px;pointer-events:none;display:none}",
  "#wmap .nd.sel .br{display:block;background:linear-gradient(#FFF6E0,#FFF6E0) 0 0/14px 3px no-repeat,linear-gradient(#FFF6E0,#FFF6E0) 0 0/3px 14px no-repeat,linear-gradient(#FFF6E0,#FFF6E0) 100% 0/14px 3px no-repeat,linear-gradient(#FFF6E0,#FFF6E0) 100% 0/3px 14px no-repeat,linear-gradient(#FFF6E0,#FFF6E0) 0 100%/14px 3px no-repeat,linear-gradient(#FFF6E0,#FFF6E0) 0 100%/3px 14px no-repeat,linear-gradient(#FFF6E0,#FFF6E0) 100% 100%/14px 3px no-repeat,linear-gradient(#FFF6E0,#FFF6E0) 100% 100%/3px 14px no-repeat}",
  "#wmap .lb{position:absolute;transform:translate(-50%,0);padding:2px 10px 3px;background:#EFE4C6;color:#2A2F1F;border:1.5px solid #8C7A4E;box-shadow:2px 2px 0 rgba(0,0,0,.35);font-size:13px;line-height:1.2;white-space:nowrap;pointer-events:none}",
  "#wmap .lb.sel{background:#FFF6D8;border-color:#FFF6E0}",
  "#wmap .off{opacity:.45;filter:saturate(.4)}",
  "#wmap .cur{position:absolute;transform:translate(-50%,-100%);padding:1px 7px 2px;background:#D9A441;color:#2A2010;border:1.5px solid #5A4318;font-size:11px;line-height:1.2;white-space:nowrap;pointer-events:none}",
  "#wmap .cur:after{content:'';position:absolute;left:50%;bottom:-6px;margin-left:-4px;border:4px solid transparent;border-top-color:#5A4318}",
  "#wmap .cur.side{transform:translate(6px,-50%)}#wmap .cur.side:after{left:-8px;top:50%;bottom:auto;margin:-4px 0 0;border-top-color:transparent;border-right-color:#5A4318}",
  "#wmap .tb{position:absolute;left:8px;right:8px;top:max(6px,env(safe-area-inset-top));height:38px;display:flex;align-items:center;gap:12px;padding:0 6px 0 12px;background:rgba(36,52,44,.94);border:2px solid #CDBB8A;color:#FFF6E0}",
  "#wmap .tb b{font-weight:400;font-size:17px}#wmap .tb span{font-size:12px;color:#D8D0B4;flex:1}",
  "#wmap .tb button,#wmap .st button{position:relative;height:32px;padding:0 12px;border:2px solid #2A2F1F;background:#EFE4C6;color:#2A2F1F;font:14px/1 var(--display,sans-serif);cursor:pointer}",
  "#wmap .tb button:after,#wmap .st button:after{content:'';position:absolute;left:-4px;right:-4px;top:-6px;bottom:-6px}",
  "#wmap .st{position:absolute;left:50%;bottom:max(6px,env(safe-area-inset-bottom));transform:translateX(-50%);width:min(720px,calc(100vw - 24px));box-sizing:border-box;display:flex;align-items:center;gap:10px;padding:6px 8px 6px 14px;background:#EFE4C6;border:2px solid #8C7A4E;box-shadow:0 2px 0 rgba(0,0,0,.4);color:#2A2F1F}",
  "#wmap .st .tx{flex:1;min-width:0}#wmap .st .tx b{display:block;font-weight:400;font-size:17px;line-height:1.2}#wmap .st .tx small{display:block;font-size:11.5px;color:#5E5638;line-height:1.3}",
  "#wmap .st .rooms{display:flex;gap:6px;flex-wrap:nowrap;overflow-x:auto;margin-top:3px;padding-bottom:2px;scrollbar-width:thin}","#wmap .st .rooms button{flex:none}",
  "#wmap .st .rooms button{height:30px;min-width:48px;padding:0 8px;font-size:12px;background:#F8F1DC;border-width:1.5px}#wmap .st .rooms button:after{left:-3px;right:-3px;top:-8px;bottom:-8px}#wmap .st .rooms button.on{background:#3D5E45;color:#FFF6E0}",
  "#wmap .st .go{height:38px!important;min-width:84px;background:#3D5E45!important;color:#FFF6E0!important;font-size:16px!important}",
  "#wmap .st .go[disabled]{opacity:.45}",
  "body.wmap-on .fsmap{opacity:0!important}",
  "body.wmap-on #w209rail{display:none!important}"
 ].join("\n");(document.head||document.documentElement).appendChild(css);
 var EL=null,SEL=null,ROOM=null;
 function c0(){try{return CASES[G.ci]}catch(e){return null}}
 function locsOf(c,node){var L=LINK[c.id]||{},o=[];c.locations.forEach(function(l,i){if(L[l.id]===node)o.push(i)});return o}
 function nodeOfLoc(c,i){var l=c.locations[i];return l&&(LINK[c.id]||{})[l.id]}
 function close(){if(EL){EL.remove();EL=null}B.classList.remove("wmap-on")}
 function draw(){var c=c0();if(!c)return;
  var W=innerWidth,H=innerHeight,s=Math.min(W/1280,H/720),ox=(W-1280*s)/2,oy=(H-720*s)/2;
  var curNode=nodeOfLoc(c,G.loc);if(SEL==null)SEL=curNode||null;
  var h='<div class="cv" style="left:0;top:0"></div><img class="bd" alt="" src="art/worldmap/world-backdrop-384x216.png" style="left:'+(ox+64*s)+'px;top:'+(oy+36*s)+'px;width:'+(1152*s)+'px;height:'+(648*s)+'px">';
  NODES.forEach(function(n){var id=n[0],ls=locsOf(c,id),open=ls.filter(function(i){return locOpen(c,i)}),on=open.length>0,x=ox+n[2]*s,y=oy+n[3]*s,sz=Math.max(44,Math.round(144*s));
   h+='<div class="nd'+(on?'':' off')+(SEL===id?' sel':'')+'" data-node="'+id+'" role="button" tabindex="0" aria-label="'+n[1]+(on?'':' (이번 사건에서 갈 수 없음)')+'" style="left:'+x+'px;top:'+(y+10*s)+'px;width:'+sz+'px;height:'+sz+'px"><span class="br"></span><img alt="" src="art/worldmap/'+id+'.png" style="width:'+sz+'px;height:'+sz+'px"></div>';
   h+='<div class="lb'+(SEL===id?' sel':'')+(on?'':' off')+'" style="left:'+x+'px;top:'+(y+12*s)+'px">'+n[1]+'</div>';
   if(curNode===id)h+='<div class="cur" data-sx="'+(x+sz/2+2)+'" data-sy="'+(y+10*s-sz*0.55)+'" style="left:'+x+'px;top:'+(y-112*s)+'px">현재 위치</div>'});
  h+='<div class="tb"><b>전체 지도</b><span>현재 지역 · 마을</span><button type="button" data-w="close">닫기 ×</button></div>';
  var sn=NODES.filter(function(n){return n[0]===SEL})[0],sl=sn?locsOf(c,sn[0]).filter(function(i){return locOpen(c,i)}):[];
  if(sl.length>1&&(ROOM==null||sl.indexOf(ROOM)<0))ROOM=sl.indexOf(G.loc)>=0?G.loc:sl[0];if(sl.length===1)ROOM=sl[0];if(!sl.length)ROOM=null;
  var sub=!sn?"장소를 고르세요":!sl.length?"이번 사건에서는 갈 수 없어요":sl.length>1?"마을 · 선택한 장소 · 방을 고르세요":"마을 · 선택한 장소";
  var rooms=sl.length>1?'<div class="rooms">'+sl.map(function(i){return '<button type="button" data-room="'+i+'" class="'+(ROOM===i?'on':'')+'">'+esc(c.locations[i].short||c.locations[i].name)+(i===G.loc?' · 지금':'')+'</button>'}).join("")+'</div>':'';
  var can=ROOM!=null&&ROOM!==G.loc;
  h+='<div class="st"><div class="tx"><b>'+(sn?sn[1]:"전체 지도")+'</b><small>'+sub+'</small>'+rooms+'</div><button type="button" class="go" data-w="go"'+(can?'':' disabled')+'>이동 →</button></div>';
  if(!EL){EL=document.createElement("div");EL.id="wmap";document.body.appendChild(EL);
   EL.addEventListener("click",function(e){var t=e.target.closest("[data-node],[data-room],[data-w]");if(!t)return;e.stopPropagation();
    if(t.dataset.node){SEL=t.dataset.node;ROOM=null;try{SFX.select()}catch(x){}draw();return}
    if(t.dataset.room){ROOM=+t.dataset.room;try{SFX.select()}catch(x){}draw();return}
    if(t.dataset.w==="close"){try{SFX.tap()}catch(x){}close();goTab("scene");return}
    if(t.dataset.w==="go"&&!t.disabled&&ROOM!=null){var g=document.querySelector('.fsmap g.mvp[data-mvp="'+ROOM+'"]');if(!g){MISS.push("mvp "+ROOM);return}
     try{if(window.__mg207)window.__mg207.mapDown=Date.now()}catch(x){}var i=ROOM;SEL=null;ROOM=null;close();g.dispatchEvent(new MouseEvent("click",{bubbles:true}))}})}
  EL.innerHTML=h;B.classList.add("wmap-on");fixCur()}
 /* '현재 위치' 꼬리표가 다른 이름표와 겹치면 아래로 조금 내리고, 그래도 겹치면 건물 오른쪽으로 옮긴다 */
 function fixCur(){var c=EL&&EL.querySelector(".cur");if(!c)return;function ov(a,b){return !(a.right<=b.left||b.right<=a.left||a.bottom<=b.top||b.bottom<=a.top)}
  function hit(){var r=c.getBoundingClientRect(),o=null;EL.querySelectorAll(".lb").forEach(function(l){var q=l.getBoundingClientRect();if(ov(r,q))o=q});return o}
  var o=hit();if(!o)return;var r=c.getBoundingClientRect(),dy=o.bottom-r.top+2;
  if(dy<=16){c.style.top=(parseFloat(c.style.top)+dy)+"px";if(!hit())return;c.style.top=(parseFloat(c.style.top)-dy)+"px"}
  c.classList.add("side");c.style.left=c.dataset.sx+"px";c.style.top=c.dataset.sy+"px"}
 function sync(){try{var on=B.classList.contains("w209")&&G&&G.tab==="move"&&document.querySelector(".fsmap");if(!on){if(EL)close();SEL=null;ROOM=null;return}if(!EL)draw()}catch(e){MISS.push(e.message)}}
 try{var _r=render;render=function(){var r=_r.apply(this,arguments);try{sync()}catch(e){}return r}}catch(e){MISS.push("render")}
 window.addEventListener("resize",function(){if(EL)draw()});
 window.__wmapState=function(){return EL?{sel:SEL,room:ROOM}:null};
})();
