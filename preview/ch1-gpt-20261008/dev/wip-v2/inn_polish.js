/* Chapter-one v2: cream paper, dark walnut and muted brass. Layout, story,
   character sizes and all existing input handlers remain owned by the engine. */
(function(){
 var style=document.createElement('style');style.id='inn-polish-v1';
 style.textContent=`
 #innmain .kv:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,22,21,.52),transparent 34%,transparent 64%,rgba(18,15,12,.88))}
 #innmain .tt{top:22px!important}#innmain .tt small{color:#dcc697!important;letter-spacing:.23em!important;font-size:11px!important}
 #innmain .tt h1{font-size:clamp(30px,5vw,45px)!important;letter-spacing:.06em!important;color:#fff3d6!important;text-shadow:0 3px 0 #21180f!important}
 #innmain .tt i{width:64px!important;background:#bca36b!important;margin-top:10px!important}
 #innmain .chapter-tag{margin-top:9px;color:#e0cfaa;font-size:14px;letter-spacing:.04em;text-shadow:0 1px 3px #000}
 #innmain .menu{bottom:20px!important;gap:8px!important;padding:8px;background:rgba(31,26,21,.88);border:1px solid #88744c;box-shadow:0 5px 20px #0005}
 #innmain .menu button{height:44px!important;min-width:102px!important;justify-content:center;padding:0 14px!important;border:1px solid #8f7c57!important;color:#efe4ca!important;background:#3b332a!important;text-shadow:none!important}
 #innmain .menu button[data-m=new]{background:#ead8aa!important;color:#35291d!important;border-color:#f9e7b5!important}
 #innmain .menu button:before{display:none!important}#innmain .menu button.f{box-shadow:inset 0 0 0 2px #c3a56b!important}
 #innmain .menu button[disabled]{opacity:.5!important}#innmain .menu button small{color:inherit!important}
 #innmain .pv{right:14px!important;bottom:8px!important;color:#d3c4a1!important;font-size:10px!important}
 #sndhint9{border:1px solid #ae9666!important;background:rgba(37,32,25,.94)!important;color:#f2e4c6!important;padding:10px 15px!important;font:14px/1.3 var(--display,sans-serif)!important;min-height:44px}
 html body.w209.inn1 #w209rail .g>button,html body.w209.inn1 #w209more button{background:rgba(246,233,206,.96)!important;border-color:#a18b62!important;color:#3e3225!important;border-radius:4px!important;box-shadow:0 2px 0 #3b302b66!important}
 html body.w209.inn1 #w209rail .g>button.on{background:#ead3a0!important;border-color:#795f37!important;box-shadow:inset 0 -3px #ad8a50!important}
 html body.w209.inn1 .fstalk .tpanel .topic{background:rgba(245,233,208,.96)!important;color:#3e3228!important;border-color:#ae9871!important;border-radius:4px!important;box-shadow:0 2px 0 #30221940!important;min-height:44px!important}
 html body.w209.inn1 .fstalk .tpanel .topic.done{background:rgba(214,207,188,.93)!important;color:#625b4a!important}
 html body.w209.inn1 .fstalk .tpanel .topic:focus-visible,html body.w209.inn1 .fstalk .tpanel .topic.sel9{outline-color:#d4b46c!important}
 html body.w209.inn1 .showev{background:#4a594a!important;border-color:#8ca085!important;color:#f6ecd5!important;border-radius:4px!important}
 html body.w209.inn1 #innmove{background:#f0e4c8!important;border:2px solid #967d50!important;box-shadow:0 10px 40px #0006!important;color:#3c3024!important;border-radius:6px!important}
 html body.w209.inn1 #innmove .hd{background:#4b4939!important;color:#f3e8cd!important;border-color:#8c784f!important}
 html body.w209.inn1 #innmove .ls button{background:#faf1dc!important;border-color:#c3b18a!important;color:#47382a!important;min-height:44px!important;border-radius:3px!important}
 html body.w209.inn1 .crec2{background:rgba(26,29,24,.97)!important}
 html body.w209.inn1 .crec2 .cr-in{background:#f1e6ca!important;border-color:#a18a5d!important;box-shadow:0 0 0 1px #e2ce9c,0 8px 30px #0005!important}
 html body.w209.inn1 .crec2 .cr-top>b{color:#493a26!important}
 html body.w209.inn1 .crec2 .cr-x{color:#493a26!important;border-color:#9d8255!important;min-width:44px!important;min-height:44px!important}
 html body.w209.inn1 .crec2 .crtab2 button{background:#514c3c!important;background-image:none!important;color:#eee1bf!important;border-color:#8d7952!important;border-radius:3px!important;min-height:40px!important}
 html body.w209.inn1 .crec2 .crtab2 button.on,html body.w209.inn1 .crec2 .crtab2 button[aria-pressed=true]{background:#e8d4a8!important;background-image:none!important;color:#3b3023!important;border-color:#b6985f!important}
 html body.w209.inn1 .crec2 .crtab2 button b,html body.w209.inn1 .crec2 .crtab2 button em{color:inherit!important}
 html body.w209.inn1 .crec2 .crtab2 button::before,html body.w209.inn1 .crec2 .crtab2 button::after{content:none!important;display:none!important}
 html body.w209.inn1 .crec2 .crtab2 button{border-image:none!important;border-width:1px!important;box-shadow:inset 0 -2px #29271f!important;text-shadow:none!important}
 html body.w209.inn1 .crec2 .cr-det .cr-tx .minib{background:#4b5c4a!important;border-color:#7a8b6a!important;color:#fff2d5!important}
 html body.w209.inn1 .crec2 [data-cr199=meet]{background:#7e3f39!important;border-color:#b67254!important;color:#fff2d5!important;border-radius:3px!important}
 #innopt{color:#f1e4c8!important}#innopt .bg:after{background:rgba(28,29,23,.91)!important}
 #innopt .hd{border-color:#82734f!important}#innopt .sep{background:#82734f!important}
 #innopt .grp button,#innopt .x{background:#3b3d31!important;color:#f1e4c8!important;border-color:#9f8b5e!important}
 #innopt .grp button[aria-checked=true]{background:#ead6a5!important;color:#392e23!important;border-color:#d4b778!important;box-shadow:inset 0 -3px #b3945b!important}
 #innopt .sv{background:#ead6a5!important;color:#392e23!important;border-color:#d4b778!important}
 #innopt input[type=range]{accent-color:#d4b778;background:linear-gradient(90deg,#c5a96c var(--p),#545549 var(--p))!important}
 #innopt input[type=range]::-webkit-slider-thumb{background:#f0deb3!important;border-color:#957d4f!important}
 html body.w209.inn1 button:focus-visible{outline:2px solid #e8c978!important;outline-offset:2px!important}
 @media(max-width:500px){#innmain .kv{background-position:32% center!important}#innmain .tt{top:35px!important}#innmain .menu{bottom:28px!important;flex-direction:column!important;width:min(250px,80vw)!important;box-sizing:border-box}#innmain .menu button{width:100%!important;min-width:0!important;height:48px!important}#innmain .chapter-tag{font-size:14px}#sndhint9{top:150px!important;right:12px!important}}
 @media(max-height:350px) and (min-width:501px){#innmain .tt{top:12px!important}#innmain .tt h1{font-size:30px!important}#innmain .chapter-tag{margin-top:5px;font-size:12px}#innmain .menu{bottom:12px!important}}
 @media(max-width:500px){html body.w209.inn1 .crec2 .crtab2 button{min-width:0!important;flex:1 1 0!important;white-space:nowrap!important;font-size:12px!important;gap:3px!important}html body.w209.inn1 .crec2 .crtab2 button em{min-width:14px!important;padding:2px 3px!important}}
 @media(prefers-reduced-motion:reduce){#innmain *,#innmove *,html body.w209.inn1 .crec2 *{animation:none!important;transition:none!important}}
 `;document.head.appendChild(style);
 function update(){var m=document.getElementById('innmain');if(m&&!m.querySelector('.chapter-tag')){var t=document.createElement('div');t.className='chapter-tag';t.textContent='1장 · 열세 번째 침대';m.querySelector('.tt').appendChild(t)}
  if(m){var p=m.querySelector('.pv');if(p&&p.textContent!=='숲속 마을의 첫 번째 사건')p.textContent='숲속 마을의 첫 번째 사건';}
  var h=document.getElementById('sndhint9');if(h&&m&&h.textContent!=='메인 음악 듣기'){h.textContent='메인 음악 듣기';h.setAttribute('aria-label','메인 음악 듣기');}}
 document.addEventListener('keydown',function(e){var m=document.getElementById('innmain');if(!m||!['ArrowUp','ArrowDown'].includes(e.key)||document.getElementById('innopt'))return;var b=[].slice.call(m.querySelectorAll('.menu button:not([disabled])'));if(!b.length)return;e.preventDefault();var i=b.indexOf(document.activeElement);b[(Math.max(0,i)+(e.key==='ArrowDown'?1:b.length-1))%b.length].focus();});
 var scheduled=false;new MutationObserver(function(){if(scheduled)return;scheduled=true;requestAnimationFrame(function(){scheduled=false;update()})}).observe(document.body,{childList:true,subtree:true});update();
})();
