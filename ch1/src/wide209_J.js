/* v210 가로 시험본(wide.html 전용) · 1장 우체국 조사·대화·질문·복귀만
   - 기본 게임(game.html/index.html)에는 들어가지 않는다. 이 파일은 wide.html을 만들 때만 붙는다.
   - 배경·전경·증거 좌표·전신 포즈·대사·질문 조건은 기존 것을 그대로 쓰고, 배치(CSS)와 오른쪽 보조 줄만 더한다.
   - 지도·원탁회의·다른 장소는 시험 범위 밖: 누르면 안내만 띄운다.
   - 저장은 wide209_early.js의 격리 저장만 쓴다. 격리가 확인되지 않으면 저장 함수를 막고 시작하지 않는다. */
(function(){
 if(!window.__W209)return;
 var B=document.body,MISS=window.__W209MISS=[];
 function safe(){return !!window.__W209SAFE}
 /* 격리 실패 시 저장 차단 */
 if(!safe()){try{persist=function(){};saveProg=function(){}}catch(e){}}

 var css=document.createElement("style");css.id="w209css";
 css.textContent=[
 'body.w209{--rail:clamp(100px,16vw,150px);background:#0B1026!important;overflow:hidden}',
 /* 기존 위·아래 막대는 화면에서 빼고(기능은 오른쪽 줄이 대신 누름) */
 'body.w209 #app>.hud,body.w209 #app>.status,body.w209 #app .bnav{position:fixed!important;left:-9999px!important;top:0!important;visibility:hidden!important;pointer-events:none!important}',
 'body.w209 .helpfab,body.w209 #admdot{display:none!important}',
 /* 조사 장면: 화면 높이 전체 + 오른쪽 줄만큼 비움(360×200 비율 그대로, 넘치면 기존 좌우 보기로 이동) */
 'body.w209 .stage,body.w209 .fstalk,body.w209 .fsmap{top:0!important;bottom:0!important;left:0!important;right:var(--rail)!important}',
 'body.w209 .stage{background:#0B1026}',
 'body.w209 .stage>.fsscroll{width:100%!important;max-width:100%!important;align-self:stretch!important;box-sizing:border-box}',
 /* 탭 전환 미끄럼(transform)이 고정 배치 장면의 높이를 0으로 만들어 복귀 위치가 풀리던 것 방지 */
 'body.w209 #app .view{animation:none!important;transform:none!important}',
 'body.w209 .stage .scenerow.stagebar{position:absolute!important;left:10px;top:10px;right:auto!important;z-index:7;width:auto!important;max-width:calc(100% - 120px);box-sizing:border-box;background:rgba(10,14,32,.62)!important;border:0!important;outline:0!important;border-radius:12px!important;box-shadow:none!important;margin:0!important;padding:5px 6px 5px 12px!important;display:flex!important;align-items:center;gap:10px}',
 'body.w209 .stage .stagebar .scap b{font-size:15px!important;color:#FFF6E0!important;position:static!important;background:none!important;border:0!important;padding:0!important}',
 'body.w209 .stage .stagebar .scap small{font-size:13px!important;color:#DDE5FF!important}',
 'body.w209 .stage .stagebar .sbtns button{min-height:40px}',
 /* 대화(이야기 장면): 배경은 화면 전체를 덮고, 상대는 크게 가운데, 하반신 위로 반투명 대사창 */
 'body.w209 #dlgveil .vnbg,body.w209 #dlgveil .vnshade{position:absolute!important;inset:0!important;top:0!important;height:auto!important;overflow:hidden}',
 'body.w209 #dlgveil .vnbg>svg,body.w209 .fstalk .tbg>svg{position:absolute!important;left:50%!important;top:50%!important;width:max(100vw,180vh)!important;height:auto!important;aspect-ratio:360/200;transform:translate(-50%,-50%)!important;max-width:none!important}',
 'body.w209 #dlgveil .vnshade{background:linear-gradient(180deg,rgba(8,10,24,.05),rgba(8,10,24,.28))!important}',
 'html body.w209 .fstalk .tstage .tfig.b202{position:absolute!important;left:0!important;right:0!important;top:6vh!important;bottom:auto!important;height:82vh!important;width:auto!important;transform:none!important}',
 'html body.w209 #dlgveil #vnfig.b202{position:absolute!important;left:0!important;right:var(--rail)!important;top:6vh!important;bottom:auto!important;height:82vh!important;width:auto!important;transform:none!important}',
 'html body.w209 #dlgveil #vnfig.b202 img.b202,html body.w209 .fstalk .tstage .tfig.b202 img.b202{position:absolute!important;top:0!important;bottom:auto!important;left:50%!important;height:100%!important;width:auto!important;max-width:none!important;max-height:none!important;transform:translateX(-50%)!important}',
 'body.w209 #vnbox .vband.bot{position:fixed!important;left:calc((100vw - var(--rail)) / 2)!important;right:auto!important;top:auto!important;bottom:10px!important;transform:translateX(-50%)!important;width:min(760px,calc(100vw - var(--rail) - 24px))!important;height:auto!important;min-height:min(31vh,150px)!important;max-height:40vh!important;margin:0!important;box-sizing:border-box;background:rgba(14,18,38,.72)!important;border:1px solid rgba(255,230,170,.35)!important;outline:0!important;border-radius:14px!important;box-shadow:0 6px 24px rgba(0,0,0,.35)!important;backdrop-filter:blur(2px);-webkit-backdrop-filter:blur(2px);animation:none}',
 'body.w209 #vnbox .vband.bot::before,body.w209 #vnbox .vband.bot::after,body.w209 #vnbox .vtxt::before,body.w209 #vnbox .vtxt::after{display:none!important}',
 'body.w209 #vnbox .vtxt{background:none!important;border:0!important;box-shadow:none!important;padding:26px 22px 14px!important;height:auto!important}',
 'body.w209 #vnbox #dtxt,body.w209 #vnbox .txt{color:#FFF6E0!important;font-size:17px!important;line-height:1.6!important;text-shadow:0 1px 0 rgba(0,0,0,.4)}',
 'body.w209 #vnbox .plate{top:-16px!important;left:16px!important}',
 'body.w209 #vnbox .nx{color:#FFD84D!important}',
 'body.w209 #dlgveil #skip{top:10px!important;right:calc(var(--rail) + 10px)!important;left:auto!important;bottom:auto!important;min-height:40px}',
 'body.w209 #dlgveil #logb{top:10px!important;left:10px!important;bottom:auto!important;min-height:40px}',
 /* 질문 고르기: 상대 크게 + 아래 반투명 질문판(2열) */
 'body.w209 .fstalk .tstage{position:absolute!important;inset:0!important;top:0!important;height:auto!important;overflow:hidden}',
 'body.w209 .fstalk .tbg{position:absolute!important;inset:0!important;overflow:hidden}',
 'body.w209 .fstalk .tname{top:12px!important;left:118px!important;bottom:auto!important;right:auto!important}',
 'body.w209 .fstalk .whonav{top:10px!important;right:10px!important}',
 'body.w209 .fstalk .tpanel{position:absolute!important;left:50%!important;right:auto!important;top:auto!important;bottom:10px!important;transform:translateX(-50%)!important;width:min(760px,calc(100% - 24px))!important;height:auto!important;max-height:42vh!important;overflow-y:auto!important;box-sizing:border-box;padding:8px!important;background:rgba(14,18,38,.70)!important;border:1px solid rgba(255,230,170,.35)!important;border-radius:14px!important;box-shadow:0 6px 24px rgba(0,0,0,.35)!important;backdrop-filter:blur(2px);-webkit-backdrop-filter:blur(2px)}',
 'body.w209 .fstalk .tpanel .topics{display:grid!important;grid-template-columns:1fr 1fr;gap:6px!important;margin:0!important;position:static!important}',
 'body.w209 .fstalk .tpanel .topic{min-height:46px!important;height:auto!important;margin:0!important;padding:8px 12px!important;background:rgba(255,248,232,.94)!important;border:1px solid #C9A96A!important;border-radius:10px!important;box-shadow:none!important;color:#2A1F16!important;font-size:15px!important;line-height:1.35;text-align:left;width:auto!important}',
 'body.w209 .fstalk .tpanel .topic span{font-size:15px!important;white-space:normal!important}',
 'body.w209 .fstalk .tpanel>*:not(.topics){grid-column:1/-1}',
 'body.w209 .metto{top:10px!important;left:calc((100vw - var(--rail)) / 2)!important;transform:translateX(-50%)!important;right:auto!important}',
 'body.w209 #w209back{position:absolute;left:10px;top:10px;z-index:6;height:44px;min-width:44px;padding:0 12px 0 8px;display:flex;align-items:center;gap:4px;border:0;border-radius:12px;background:rgba(10,14,32,.62);color:#FFF6E0;font:15px var(--display,sans-serif);cursor:pointer}',
 'body.w209 #w209back img{width:22px;height:22px;image-rendering:pixelated}',
 /* 오른쪽 보조 줄 */
 /* 가운데 창(증거 발견 등): 화면 높이 안에 들어오게, 증거 그림은 왼쪽 */
 'body.w209 #ov .modal{max-height:calc(100vh - 20px)!important;overflow-y:auto!important;box-sizing:border-box!important;width:min(700px,calc(100vw - var(--rail) - 24px))!important;max-width:none!important}',
 'body.w209 #ov .modal:has(>.bigic){display:grid!important;grid-template-columns:132px 1fr;column-gap:18px;align-items:start;text-align:left}',
 'body.w209 #ov .modal:has(>.bigic)>*{grid-column:2;margin-top:0}',
 'body.w209 #ov .modal:has(>.bigic)>.bigic{grid-column:1;grid-row:1 / span 8;width:124px!important;height:124px!important;margin:8px 0 0!important}',
 'body.w209 #ov .modal:has(>.bigic) .btn{min-height:44px}',
 'body.w209 #ov .modal{padding-top:14px!important;padding-bottom:12px!important}',
 'body.w209 #ov .modal #okfind,body.w209 #ov .modal #closeit{position:sticky!important;bottom:0!important;z-index:3;margin-top:8px!important}',
 /* P3b: 낮은 화면(높이 420px 이하: 640x360, 844x390)에서는 창 높이를 고정하고, 다람 메모만 독립 스크롤 / 확인 버튼은 맨 아래 칸에 고정 */
 '@media (max-height:420px){body.w209 #ov .modal:has(>.bigic){height:calc(100vh - 20px)!important;overflow:hidden!important;grid-template-rows:auto auto minmax(0,max-content) minmax(44px,1fr) auto}body.w209 #ov .modal:has(>.bigic)>p{min-height:0;align-self:stretch;overflow-y:auto;overscroll-behavior:contain}body.w209 #ov .modal:has(>.bigic)>.dmfind{grid-row:4;align-self:stretch;min-height:0;margin-top:3px!important;overflow-y:auto;overscroll-behavior:contain;margin-bottom:0!important}body.w209 #ov .modal:has(>.bigic)>#okfind{grid-row:5;position:static!important;margin-top:6px!important;min-height:44px!important;padding-top:6px!important;padding-bottom:6px!important}body.w209 #ov .modal:has(>.bigic)>*{margin-bottom:0!important}body.w209 #ov .modal:has(>.bigic){row-gap:4px!important}body.w209 #ov .modal:has(>.bigic)>.bigic{grid-row:1 / span 5!important}body.w209 #ov .modal:has(>.bigic) h3{margin:0!important;line-height:1.2!important}}',
 '@media (max-height:380px){body.w209 #ov .modal:has(>.bigic){grid-template-columns:104px 1fr}body.w209 #ov .modal:has(>.bigic)>.bigic{width:96px!important;height:96px!important}body.w209 #ov .modal h3{margin:2px 0 4px!important}}',
 /* 증거 기록(기존 화면): 가로에서는 왼쪽 상세, 오른쪽 목록 */
 'body.w209 .crec2 .cr-in{width:min(860px,calc(100vw - 24px))!important;max-width:none!important;height:calc(100vh - 20px)!important;margin:10px auto!important;box-sizing:border-box;display:grid!important;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);grid-template-rows:auto auto auto minmax(0,1fr) auto auto;column-gap:14px;row-gap:6px;overflow:hidden!important}',
 'body.w209 .crec2 .cr-top{grid-column:1/-1;grid-row:1}',
 'body.w209 .crec2 .cr-det{grid-column:1;grid-row:2/7;overflow-y:auto;align-self:stretch;margin:0!important;min-height:0}',
 /* P3: 가로에서는 상세가 왼쪽 칸 전체 높이를 쓰고, 조사/결합 버튼은 스크롤해도 아래에 붙어 보인다 */
 'body.w209 .crec2 .cr-in{margin:0 auto!important;height:100%!important}',
 'body.w209 .crec2 .cr-in>.cr-det{height:auto!important;max-height:none!important;min-height:0!important;align-self:stretch;overflow-y:auto!important;overflow-x:hidden;overscroll-behavior:contain}',
 'body.w209 .crec2 .cr-det #crexam{position:sticky;bottom:0;z-index:2;box-shadow:0 -6px 6px -2px #F4EEDC}',
 '@media (max-height:400px){body.w209 .crec2 .cr-det p{font-size:14.5px!important;line-height:1.5!important}}',
 'body.w209 .crec2 .crtab2{grid-column:2;grid-row:2;margin:0!important}',
 'body.w209 .crec2 .cr-fil{grid-column:2;grid-row:3;margin:0!important}',
 'body.w209 .crec2 .cr-grid{grid-column:2;grid-row:4;overflow-y:auto!important;min-height:0!important;height:auto!important;max-height:none!important;margin:0!important}',
 'body.w209 .crec2 .cr-msg{grid-column:2;grid-row:5;margin:0!important}',
 'body.w209 .crec2 .cr199,body.w209 .crec2 #crgo{grid-column:2;grid-row:6;margin:0!important}',
 'body.w209.dl-on .fstalk .tpanel{visibility:hidden}',
 '#w209rail{display:none}',
 'body.w209 #w209rail{display:flex;flex-direction:column;position:fixed;top:0;right:0;bottom:0;width:var(--rail);z-index:30;box-sizing:border-box;padding:max(8px,env(safe-area-inset-top)) max(8px,env(safe-area-inset-right)) 8px 8px;gap:6px;background:linear-gradient(180deg,#141A38,#0E1330);color:#FFF6E0;font-family:var(--display,sans-serif)}',
 '#w209rail .rh{display:flex;flex-direction:column;gap:2px;line-height:1.2}',
 '#w209rail .rh b{font-size:13px;color:#FFD84D;font-weight:400}',
 '#w209rail .rh small{font-size:12px;color:#C9D4F2}',
 '#w209rail .tag{align-self:flex-start;font-size:12px;padding:1px 6px;border-radius:6px;background:#FFD84D;color:#1B2447}',
 '#w209rail .hp{display:flex;align-items:center;gap:2px;min-height:16px}#w209rail .hp i{display:inline-block;width:10px;height:10px;border-radius:2px;background:#E0474C}#w209rail .hp i.off{background:#3A3F5C}',
 '#w209rail .g{display:grid;grid-template-columns:1fr 1fr;gap:6px;flex:1;min-height:0;align-content:start}',
 '#w209rail button{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;min-height:48px;min-width:44px;padding:4px 2px;border:0;border-radius:10px;background:rgba(255,255,255,.06);color:#FFF6E0;font:12px/1.1 var(--display,sans-serif);cursor:pointer}',
 '#w209rail button img{width:24px;height:24px;image-rendering:pixelated}',
 '#w209rail button.on{background:rgba(255,216,77,.22);box-shadow:inset 0 0 0 2px #FFD84D}',
 '#w209rail button.out{opacity:.55}',
 '#w209rail button .n{position:absolute;top:2px;right:4px;min-width:18px;height:18px;padding:0 4px;box-sizing:border-box;border-radius:9px;background:#E0474C;color:#fff;font-size:12px;line-height:18px}',
 '#w209rail .ft{display:flex;flex-direction:column;gap:4px}',
 '#w209rail .ft button{flex-direction:row;min-height:44px;font-size:12px;background:rgba(255,255,255,.04)}',
 '#w209rail .ft a{font-size:12px;color:#9FB0DA;text-align:center;text-decoration:underline}',
 '@media (max-height:400px){#w209rail{gap:4px!important}#w209rail .rh small{display:none}#w209rail .g{gap:4px}#w209rail button{min-height:44px}#w209rail button img{width:20px;height:20px}#w209rail .ft{gap:2px}}',
 '#w209ret{position:fixed;left:50%;bottom:12px;transform:translateX(-50%);z-index:99980;min-height:44px;padding:0 18px;border:0;border-radius:22px;background:#FFD84D;color:#1B2447;font:15px var(--display,sans-serif);box-shadow:0 4px 14px rgba(0,0,0,.35)}',
 /* 범위 밖 안내 */
 '#w209note{position:fixed;inset:0;z-index:99990;display:flex;align-items:center;justify-content:center;background:rgba(6,8,20,.6)}',
 '#w209note .bx{max-width:min(440px,calc(100vw - 32px));box-sizing:border-box;padding:18px 20px;border-radius:14px;background:#141A38;color:#FFF6E0;font:15px/1.55 var(--display,sans-serif);box-shadow:0 10px 30px rgba(0,0,0,.4)}',
 '#w209note .bx b{display:block;font-size:17px;color:#FFD84D;margin-bottom:6px;font-weight:400}',
 '#w209note button{margin-top:12px;min-height:44px;width:100%;border:0;border-radius:10px;background:#FFD84D;color:#1B2447;font:16px var(--display,sans-serif)}',
 /* 세로로 들면 안내만(강제 회전 없음) */
 '#w209rot{display:none}',
 '@media (orientation:portrait){#w209rot{display:flex;position:fixed;inset:0;z-index:99999;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:24px;box-sizing:border-box;background:#0E1330;color:#FFF6E0;text-align:center;font:16px/1.6 var(--display,sans-serif)}#w209rot b{font-size:20px;color:#FFD84D;font-weight:400}#w209rot a{color:#9FB0DA}}',
 'html body.w209 .crec2{padding:max(6px,env(safe-area-inset-top)) 8px 6px!important}',
 'html body.w209 .crec2 .cr-in{width:min(560px,calc(100vw - 16px))!important;height:auto!important;max-height:100%!important;margin:auto!important;box-sizing:border-box!important;display:grid!important;grid-template-columns:auto minmax(0,1fr) auto!important;grid-template-rows:46px minmax(0,1fr) auto auto auto auto!important;column-gap:0!important;row-gap:0!important;padding:0!important;overflow:hidden!important;border:3px solid #C9A96A!important;border-radius:14px!important;background:linear-gradient(#1B2447 0 46px,#F4EEDC 46px)!important}',
 'html body.w209 .crec2 .cr-top{display:contents}',
 'html body.w209 .crec2 .cr-top>b{grid-column:1;grid-row:1;align-self:center;margin:0 0 0 12px!important;font-size:17px;line-height:1;white-space:nowrap;color:#FFD84D}',
 'html body.w209 .crec2 .cr-x{grid-column:3;grid-row:1;width:44px;height:44px;min-width:44px;margin:0 1px 0 0!important;padding:0;display:flex;align-items:center;justify-content:center;font-size:24px;border-radius:10px}',
 'html body.w209 .crec2 .crtab2{grid-column:2;grid-row:1;margin:0 8px!important;display:flex;gap:6px;align-self:center;justify-content:center}',
 'html body.w209 .crec2 .crtab2 button{position:relative;flex:0 1 120px;min-height:40px!important;height:40px;margin:0;padding-top:0!important;padding-bottom:0!important}',
 'html body.w209 .crec2 .crtab2 button::after{content:\'\';position:absolute;left:0;right:0;top:-2px;bottom:-2px}',
 'html body.w209 .crec2 .cr-in>.cr-det{grid-column:1/-1!important;grid-row:2!important;height:auto!important;max-height:none!important;min-height:0!important;align-self:stretch!important;margin:0!important;border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important}',
 'html body.w209 .crec2 .cr-in>.cr-det:not(.empty){display:grid!important;grid-template-columns:76px minmax(0,1fr) auto auto!important;grid-template-rows:auto auto auto auto!important;min-height:min(174px,calc(100vh - 186px))!important;grid-auto-rows:auto!important;align-content:start!important;align-items:start!important;column-gap:8px!important;row-gap:6px!important;padding:10px 12px 0!important;overflow-y:auto!important;overflow-x:hidden!important;overscroll-behavior:contain}',
 'html body.w209 .crec2 .cr-det:not(.empty)::before{display:none!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-ic{grid-column:1!important;grid-row:1/span 2!important;width:72px!important;height:72px!important;margin:0 4px 0 0!important;align-self:start!important;position:static!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx{display:contents!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx h3{grid-column:2/-1!important;grid-row:1!important;margin:0!important;padding:0!important;font-size:18px!important;line-height:1.25!important;align-self:center!important;position:static!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>p{grid-column:2/-1!important;grid-row:2!important;margin:0!important;padding:0!important;font-size:15.5px!important;line-height:1.55!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>p.cr-ex{grid-row:3!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>.dmemo{display:none!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>#crexam,html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>#crdaram,html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>.cr-act{position:sticky!important;bottom:0!important;z-index:3;margin:0!important;min-height:44px;box-shadow:0 0 0 4px #F4EEDC;align-self:end!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>#crexam{grid-column:1/3!important;grid-row:4!important;white-space:nowrap}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>#crdaram{grid-column:3!important;grid-row:4!important;white-space:nowrap}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>.cr-act{grid-column:4!important;grid-row:4!important;display:flex!important;gap:6px!important;width:auto!important;padding:0!important;background:#F4EEDC}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>.cr-act button{min-height:44px}',
 'html body.w209 .crec2 .cr-in>.cr-grid{grid-column:1/-1;grid-row:3;display:flex!important;flex-wrap:nowrap!important;gap:6px;overflow-x:auto!important;overflow-y:hidden!important;height:auto!important;max-height:none!important;min-height:0!important;padding:6px 8px 4px!important;margin:0!important;align-items:stretch;background:#E6D8B6;border-top:3px solid #C9A96A;-webkit-overflow-scrolling:touch}',
 'html body.w209 .crec2 .cr-grid .cr-th{flex:none;position:relative;width:80px!important;height:76px!important;min-width:80px;min-height:0!important;padding:3px 2px 2px!important;margin:0!important;display:flex!important;flex-direction:column;align-items:center;justify-content:flex-start;gap:1px}',
 'html body.w209 .crec2 .cr-grid .cr-th .cr-ic2{width:34px!important;height:34px!important;margin:0!important;flex:none;display:flex;align-items:center;justify-content:center}',
 'html body.w209 .crec2 .cr-grid .cr-th .cr-ic2 svg,html body.w209 .crec2 .cr-grid .cr-th .cr-ic2 img{width:100%!important;height:100%!important}',
 'html body.w209 .crec2 .cr-grid .cr-th .cr-nm{display:-webkit-box!important;-webkit-box-orient:vertical;-webkit-line-clamp:2;overflow:hidden;max-width:100%;font-size:12px!important;line-height:1.1!important;text-align:center;word-break:keep-all;padding:0 1px}',
 'html body.w209 .crec2 .cr-grid .cr-th .bdg{top:-3px!important;left:auto!important;right:-3px;transform:none!important;width:12px;height:12px;padding:0!important;font-size:0!important;border-radius:50%}',
 'html body.w209 .crec2 .cr199{grid-column:1/-1;grid-row:4;margin:0!important;padding:0 10px 5px!important;background:#E6D8B6;text-align:center}',
 'html body.w209 .crec2 .cr199 small{font-size:12.5px;color:#4B3E22}',
 'html body.w209 .crec2 .cr-fil{grid-column:1/-1;grid-row:5;margin:0!important;padding:0 8px 6px;background:#E6D8B6;display:flex;gap:6px;overflow-x:auto}',
 'html body.w209 .crec2 .cr-fil:not(:has(button:nth-child(3))){display:none!important}',
 'html body.w209 .crec2 .cr-fil button{min-height:40px}',
 'html body.w209 .crec2 .cr-msg{grid-column:1/-1;grid-row:6;margin:0!important;background:#E6D8B6}',
 'html body.w209 .crec2 .cr-msg:empty{display:none}',
 /* D4: D2 비율 유지 + 버튼·탭·타일 축소, 띠가 넘치면 좌우 화살표와 남은 개수 */
 'html body.w209 .crec2 .cr-in{position:relative!important;grid-template-rows:40px minmax(0,1fr) auto auto auto auto!important;border-width:2px!important;border-radius:12px!important;background:linear-gradient(#1B2447 0 40px,#F4EEDC 40px)!important}',
 'html body.w209 .crec2 .cr-top>b{font-size:15px!important}',
 'html body.w209 .crec2 .crtab2{overflow:visible!important}',
 'html body.w209 .crec2 .crtab2 button{position:relative!important;overflow:visible!important;flex:0 1 104px!important;height:30px!important;min-height:30px!important;font-size:14px!important}',
 'html body.w209 .crec2 .crtab2 button::after{top:-6px!important;bottom:-6px!important}',
 'html body.w209 .crec2 .crtab2 button svg{width:16px!important;height:16px!important}',
 'html body.w209 .crec2 .cr-in>.cr-det:not(.empty){grid-template-columns:68px minmax(0,1fr) auto auto!important;padding:10px 12px 0!important;min-height:0!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-ic{width:64px!important;height:64px!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx h3{font-size:17px!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>p{font-size:15px!important;line-height:1.55!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>#crexam,html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>#crdaram{min-height:32px!important;height:32px!important;padding:0 12px!important;font-size:13px!important;gap:5px!important;display:inline-flex!important;align-items:center!important;justify-self:start!important;width:max-content!important;max-width:100%;box-shadow:0 0 0 4px #F4EEDC,0 2px 0 rgba(0,0,0,.25)!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>#crexam img,html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>#crdaram>svg{width:18px!important;height:18px!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>.cr-act{min-height:32px!important;gap:4px!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>.cr-act button{position:relative;height:32px!important;min-height:32px!important;min-width:32px!important;padding:0 10px!important;font-size:13px!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>.cr-act button img{width:16px!important;height:16px!important}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>#crexam::after,html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>#crdaram::after,html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>.cr-act button::after{content:\'\';position:absolute;left:0;right:0;top:-6px;bottom:-6px}',
 'html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>#crexam,html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>#crdaram,html body.w209 .crec2 .cr-det:not(.empty) .cr-tx>.cr-act{margin:6px 0 8px!important}',
 'html body.w209 .crec2 .cr-in>.cr-grid{gap:4px!important;padding:6px 10px 4px!important;border-top-width:2px!important;scroll-behavior:smooth}',
 'html body.w209 .crec2 .cr-grid .cr-th{width:62px!important;min-width:62px!important;height:66px!important;padding:3px 2px 2px!important;border-width:1.5px!important}',
 'html body.w209 .crec2 .cr-grid .cr-th .cr-ic2{width:26px!important;height:26px!important}',
 'html body.w209 .crec2 .cr-grid .cr-th .cr-nm{font-size:11px!important;line-height:1.15!important;padding:1px 1px 0!important;margin:0!important;max-height:none!important;height:auto!important}',
 'html body.w209 .crec2 .cr-grid .cr-th .bdg{width:9px!important;height:9px!important}',
 'html body.w209 .crec2 .cr199 small{font-size:12px!important}',
 'html body.w209 .crec2 .crar{position:absolute;z-index:5;width:28px;border:0;padding:0;margin:0;display:flex;align-items:center;justify-content:center;font:16px/1 var(--display,sans-serif);color:#FFF6E0;background:rgba(27,36,71,.82);cursor:pointer}',
 'html body.w209 .crec2 .crar.l{left:0;border-radius:0 8px 8px 0}',
 'html body.w209 .crec2 .crar.r{right:0;border-radius:8px 0 0 8px}',
 'html body.w209 .crec2 .crar[hidden]{display:none!important}',
 'html body.w209 .crec2 .crar::after{content:\'\';position:absolute;inset:0 -8px}',
 'html body.w209 .crec2 .crar b{position:absolute;bottom:2px;left:0;right:0;font-size:10px;font-weight:400;text-align:center;opacity:.9}',
 /* E: 10쪽 시안 — 오른쪽 세로 줄 없이 장면 전체, 오른쪽 위 작은 아이콘 + 더보기, 왼쪽 위 종이 장소 카드 */
 'html body.w209{--rail:0px!important}',
 'html body.w209 #w209rail{top:max(8px,env(safe-area-inset-top))!important;right:max(8px,env(safe-area-inset-right))!important;bottom:auto!important;left:auto!important;width:auto!important;padding:0!important;background:none!important;flex-direction:row!important;align-items:flex-start;gap:6px!important;z-index:40}',
 'html body.w209 #w209rail .rh,html body.w209 #w209rail .ft{display:none!important}',
 'html body.w209 #w209rail .g{display:flex!important;flex-direction:row;gap:6px!important;flex:none!important}',
 'html body.w209 #w209rail button{width:46px;min-width:46px!important;height:46px;min-height:46px!important;padding:3px 0 2px!important;gap:1px!important;border-radius:10px!important;background:#F4EEDC!important;color:#2A2F45!important;border:2px solid #C9A96A!important;box-shadow:0 2px 0 rgba(0,0,0,.35)!important;font-size:11px!important;line-height:1!important}',
 'html body.w209 #w209rail button img{width:22px!important;height:22px!important}',
 'html body.w209 #w209rail button.on{background:#FFE9A8!important;border-color:#F2C230!important;box-shadow:0 0 0 2px #F2C230,0 2px 0 rgba(0,0,0,.35)!important}',
 'html body.w209 #w209rail button .n{top:-5px!important;right:-5px!important}',
 'html body.w209 #w209rail .g button[data-w=hint],html body.w209 #w209rail .g button[data-w=spine],html body.w209 #w209rail .g button[data-w=move],html body.w209 #w209rail .g button[data-w=set]{display:none!important}',
 '#w209more{display:none}',
 'html body.w209 #w209rail.more #w209more{display:grid!important;position:absolute;top:52px;right:0;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;width:200px;padding:10px;border-radius:12px;background:#151B3A;border:2px solid #C9A96A;box-shadow:0 8px 20px rgba(0,0,0,.4);color:#FFF6E0;font:12px/1.3 var(--display,sans-serif)}',
 '#w209more .hd{grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;gap:6px}#w209more .hd b{color:#FFD84D;font-weight:400}',
 '#w209more .hp i{display:inline-block;width:9px;height:9px;margin-left:2px;border-radius:2px;background:#E0474C}#w209more .hp i.off{background:#3A3F5C}',
 'html body.w209 #w209rail #w209more button{width:auto!important;height:40px!important;min-height:40px!important;flex-direction:row!important;gap:6px!important;font-size:13px!important;background:#2E3766!important;color:#FFF6E0!important;border:1px solid #4A5590!important;box-shadow:none!important;opacity:1!important}',
 'html body.w209 #w209more button img{width:18px!important;height:18px!important}',
 '#w209more a{grid-column:1/-1;color:#9FB0DA;text-align:center;text-decoration:underline;padding:4px 0}',
 'html body.w209 .stage .scenerow.stagebar{background:#F4EEDC!important;border:2px solid #C9A96A!important;box-shadow:0 2px 0 rgba(0,0,0,.35)!important;padding:4px 6px 4px 10px!important;max-width:calc(100% - 260px)!important}',
 'html body.w209 .stage .stagebar .scap b{color:#2A2F45!important;font-size:14px!important}',
 'html body.w209 .stage .stagebar .scap small{color:#6B5A3A!important;font-size:12px!important}',
 'html body.w209 .stage .stagebar .scap b::before{content:\'\';display:inline-block;width:9px;height:9px;margin-right:6px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:#C0392B;vertical-align:1px}',
 'html body.w209 .stage .stagebar .sbtns button{min-height:34px!important;height:34px}',
 'html body.w209 #vnbox .vband.bot{width:min(820px,calc(100vw - 32px))!important}',
 'html body.w209 .stage{background:radial-gradient(ellipse at center,#2b1f16 0%,#120d0a 70%)!important}',
 'html body.w209 .stage>.fsscroll>#bigscene{margin-left:auto!important;margin-right:auto!important}',
 'html body.w209.dl-on .stage .scenerow.stagebar{visibility:hidden!important}',
 /* F: 장면 속 주민을 서 있는 전신으로(바닥에 선 주민 / 카운터 뒤 주민은 상반신만) */
 'html body.w209 #bigscene .npc.f210{transform:translate(-50%,-100%)!important;margin-top:var(--ft,0px)!important;width:var(--fw,auto)!important;height:var(--fh,auto)!important;padding:0!important;justify-content:flex-end!important;overflow:visible!important;animation:none!important;background:transparent!important;border:0!important;box-shadow:none!important;outline:0!important;border-radius:0!important}',
 'html body.w209 #bigscene .npc.f210>svg{display:none!important}',
 'html body.w209 #bigscene .npc.f210 .npcclip{background:none!important;border:0!important;padding:0!important;margin:0!important;border-radius:0!important;box-shadow:none!important;position:absolute;left:50%;bottom:0;transform:translateX(-50%);height:var(--vh,100%);width:var(--iw,100px);overflow:hidden;pointer-events:none}',
 'html body.w209 #bigscene .npc.f210 .npcclip img{position:absolute;left:0;top:0;width:100%;height:var(--ih,100px);image-rendering:pixelated;filter:drop-shadow(0 3px 0 rgba(0,0,0,.28))}',
 'html body.w209 #bigscene .npc.f210>span{position:absolute;left:50%;transform:translateX(-50%);bottom:-6px;margin:0!important;z-index:3}',
 'html body.w209 #bigscene .npc.f210.up>span{bottom:auto;top:-20px}',
 'html body.w209 #bigscene .npc.f210 .tk{top:2px!important;right:auto!important;left:calc(50% + var(--iw,100px) * .22)!important}',
 'html body.w209 #bigscene .npc.f210.on .npcclip img{filter:drop-shadow(0 0 2px #FFD84D) drop-shadow(0 0 2px #FFD84D) drop-shadow(0 3px 0 rgba(0,0,0,.28))}',
 'html body.w209 #bigscene .npc.f210.heard .npcclip img{filter:brightness(.92) drop-shadow(0 3px 0 rgba(0,0,0,.28))}',
 /* G: 대화 상대 크게 + 등장 순간 확 커지는 연출 */
 'html body.w209 #dlgveil #vnfig.b202,html body.w209 .fstalk .tstage .tfig.b202{top:2vh!important;height:108vh!important}',
 'html body.w209 #dlgveil #vnfig.b202.in img.b202,html body.w209 .fstalk .tstage .tfig.b202 img.b202{animation:g210pop .2s cubic-bezier(.2,.9,.3,1.2)!important;transform-origin:50% 60%}',
 '@keyframes g210pop{from{opacity:.2;transform:translateX(-50%) translateY(6%) scale(.88)}to{opacity:1;transform:translateX(-50%) translateY(0) scale(1)}}',
 /* G2: 테두리처럼 보이던 흰 빛 번짐 제거 */
 'html body.w209 #dlgveil #vnfig.b202 img.b202,html body.w209 .fstalk .tstage .tfig.b202 img.b202{filter:drop-shadow(0 5px 6px rgba(0,0,0,.28))!important}',
 'html body.w209 #dlgveil #vnfig.b202.dim img.b202{filter:brightness(.9) drop-shadow(0 5px 6px rgba(0,0,0,.25))!important}',
 ].join("\n");
 (document.head||document.documentElement).appendChild(css);

 var ICON="art/icons/";
 function q(s){return document.querySelector(s)}
 function note(title,text){var o=q("#w209note");if(o)o.remove();
  var d=document.createElement("div");d.id="w209note";d.setAttribute("role","dialog");
  d.innerHTML='<div class="bx"><b>'+title+'</b><div>'+text+'</div><button type="button">닫기</button></div>';
  document.body.appendChild(d);d.querySelector("button").onclick=function(){d.remove()};
  d.addEventListener("click",function(e){if(e.target===d)d.remove()})}
 function outOfScope(what){note("가로 시험 범위 밖",what+"은(는) 이번 가로 시험본에 들어 있지 않아요. 이 시험은 1장 우체국의 조사·대화·질문만 다룹니다. 기본 게임(세로)에서는 그대로 쓸 수 있어요.")}

 /* 범위 제한: 지도·원탁회의·다른 장소 */
 function inScope(){try{return !!(G&&S.screen==="case"&&CASES[G.ci]&&(CASES[G.ci].id==="envelope"||CASES[G.ci].id==="inn"))}catch(e){return false}}
 try{var _gt=goTab;goTab=function(t,opts){if(inScope()){
   /* I: 원탁회의에 필요한 증거가 창고·기록실에 있어서, 1장 안에서는 이동·회의 탭을 막지 않는다 */}
  return _gt.apply(this,arguments)}}catch(e){MISS.push("goTab")}
 

 /* 오른쪽 보조 줄: 기존 버튼을 그대로 눌러 준다 */
 function proxy(sel){var e=q(sel);if(e){e.click();return true}return false}
 var BTN=[
  ["scene","investigate.png","조사",function(){goTab("scene")}],
  ["ev","evidence.png","증거",function(){proxy("#presentbtn")}],
  ["hint","hint.png","힌트",function(){proxy("#helpnav")}],
  ["rec","record.png","기록",function(){proxy("#recbtn")}],
  ["spine","notebook.png","줄기",function(){proxy("#spinebtn")}],
  ["move","move.png","이동",function(){goTab("move")}],
  ["set","settings.png","설정",function(){proxy("#snd")}]
 ];
 function num(sel){var e=q(sel);if(!e)return "";var b=e.querySelector("b,.hl,.n");var t=b?(b.textContent||"").replace(/[^0-9/]/g,""):"";return t}
 function rail(){
  var r=q("#w209rail");if(!r){r=document.createElement("nav");r.id="w209rail";r.setAttribute("aria-label","가로 시험 메뉴");document.body.appendChild(r)}
  if(!B.classList.contains("w209")){return}
  var hp=0,hpMax=5;try{hpMax=(typeof window.hpMax==="function")?window.hpMax(CASES[G.ci]):5;hp=G.hp==null?hpMax:G.hp}catch(e){}
  var h='<div class="rh"><span class="tag">가로 시험본</span><b>1장 · 우체국</b><small>조사·대화만</small><span class="hp" aria-label="신뢰 '+hp+'/'+hpMax+'">';
  for(var i=0;i<hpMax;i++)h+='<i'+(i<hp?'':' class="off"')+'></i>';
  h+='</span></div><div class="g">';
  BTN.forEach(function(x){var n=x[0]==="rec"?num("#recbtn"):x[0]==="hint"?num("#helpnav"):"";
   h+='<button type="button" data-w="'+x[0]+'" class="'+(x[0]==="scene"&&G&&G.tab==="scene"?"on":"")+""+'" aria-label="'+x[2]+'"><img src="'+ICON+x[1]+'" alt="">'+x[2]+(n&&n!=="0"?'<span class="n">'+n+'</span>':'')+'</button>'});
  h+='</div><div class="ft"><button type="button" data-w="reset">시험 처음부터</button><a href="game.html" target="_top">기본 게임(세로)</a></div>';
  r.innerHTML=h;
  r.querySelectorAll("[data-w]").forEach(function(b){b.onclick=function(e){e.preventDefault();var k=b.dataset.w;
   if(k==="reset"){if(b.dataset.arm){try{localStorage.clear()}catch(x){}location.reload();return}b.dataset.arm=1;b.textContent="한 번 더 누르면 초기화";setTimeout(function(){if(b.isConnected){delete b.dataset.arm;b.textContent="시험 처음부터"}},3000);return}
   if(typeof DL!=="undefined"&&DL)return;
   BTN.forEach(function(x){if(x[0]===k){try{SFX.tap()}catch(z){}x[3]()}})}})
 }
 function back(){var ft=q(".fstalk");if(!ft||!B.classList.contains("w209"))return;if(ft.querySelector("#w209back"))return;
  var b=document.createElement("button");b.id="w209back";b.type="button";b.setAttribute("aria-label","조사로 돌아가기");b.innerHTML='<img src="'+ICON+'back.png" alt="">조사로';
  b.onclick=function(){if(typeof DL!=="undefined"&&DL)return;goTab("scene")};ft.appendChild(b)}
 function retBtn(show){var r=q("#w209ret");if(!show){if(r)r.remove();return}if(r)return;r=document.createElement("button");r.id="w209ret";r.type="button";r.textContent="가로 시험(우체국)으로 돌아가기";r.onclick=function(){r.remove();boot()};document.body.appendChild(r)}
 function apply(){try{var on=inScope()&&safe();B.classList.toggle("w209",on);retBtn(!on&&safe()&&S.screen!=="title");if(on){rail();back();try{fsLayout()}catch(x){}}}catch(e){MISS.push("apply "+e.message)}}
 try{var _r=render;render=function(){var r=_r.apply(this,arguments);apply();return r}}catch(e){MISS.push("render")}
 try{new MutationObserver(function(){if(apply.t)return;apply.t=setTimeout(function(){apply.t=0;if(inScope()&&safe()&&!B.classList.contains("w209"))apply()},30)}).observe(B,{attributes:true,attributeFilter:["class"]})}catch(e){}

 /* 세로 안내 */
 var rot=document.createElement("div");rot.id="w209rot";rot.innerHTML='<b>가로 시험본</b><div>기기를 가로로 돌려 주세요.<br>1장 우체국 장면만 가로로 시험합니다.</div><a href="game.html" target="_top">기본 게임(세로)으로 가기</a>';
 document.body.appendChild(rot);

 /* 시작: 격리 저장에 1장 진행이 있으면 이어서, 없으면 1장 우체국 첫 조사 상태로 */
 function boot(){
  if(!safe()){note("시험을 시작할 수 없어요","이 브라우저에서 시험 저장을 따로 만들 수 없어, 기본 게임 저장을 지키기 위해 시험을 멈췄어요.");return}
  try{
   var EPK=window.__EP1INN?"inn":"envelope",ci=0;CASES.forEach(function(c,i){if(c.id===EPK)ci=i});
   S.story=S.story||{};S.story.named=true;S.story.pro=true;
   if(!S.players||!S.players[0])S.players=["아빠","다람"];
   if(S.prog&&S.prog[EPK]){G=S.prog[EPK];CASES[ci].contra.forEach(function(x){if(G.broken&&G.broken[x.t]&&x.unlock&&G.unlocked.indexOf(x.unlock)<0)G.unlocked.push(x.unlock)})}
   else{G=fresh(ci);G.introDone=true;G.visited=[0];G.beats=G.beats||{};G.beats.m151new=1;G.beats["place204:post"]=1;G.beats.deal=1}
   if(EPK==="envelope"){G.loc=0;G.tab="scene";G.notice=null}S.screen="case";
   try{saveProg()}catch(e){}
   render();if(EPK==="inn"&&window.__innStart)setTimeout(window.__innStart,300);
  }catch(e){MISS.push("boot "+e.message);note("시험 시작 오류",String(e.message||e))}
 }
 window.__w209boot=boot;
 if(document.readyState==="complete")setTimeout(boot,60);else window.addEventListener("load",function(){setTimeout(boot,60)});

 /* 후보 D: 다람에게 물어보기 — 기존 다람 메모(window.__memoOf)를 기존 say 대화로 재사용. 새 대사·상태 변경 없음 */
 (function(){
  function sel(){var t=document.querySelector(".crec2 .cr-th.on");return t?t.dataset.crs:null}
  function memo(id){try{return id?(window.__memoOf?window.__memoOf(CASES[G.ci],id):""):""}catch(e){return ""}}
  function split(m){var a=String(m).split(/(?<=[.!?…])\s+/).filter(Boolean),o=[];a.forEach(function(x){if(o.length&&(o[o.length-1].length+x.length)<=34)o[o.length-1]+=" "+x;else o.push(x)});return o.length?o:[m]}
  var busy=false;
  function ask(){if(busy||(typeof DL!=="undefined"&&DL))return;var id=sel(),m=memo(id);if(!m)return;
   var det=document.querySelector(".crec2 .cr-det"),st=det?det.scrollTop:0;busy=true;
   try{say(split(m).map(function(l){return ["det1",l,"think"]}),function(){setTimeout(function(){busy=false;
     var t=document.querySelector('.crec2 .cr-th[data-crs="'+id+'"]');if(t&&!t.classList.contains("on"))t.click();
     var d=document.querySelector(".crec2 .cr-det");if(d)d.scrollTop=st},80)})}catch(e){busy=false}}
  var q=0;
  function sync(){q=0;try{var tx=document.querySelector(".crec2 .cr-det .cr-tx");if(!tx)return;var id=sel(),m=memo(id),b=tx.querySelector("#crdaram");
   if(b&&(!m||b.dataset.id!==id)){b.remove();b=null}
   if(!b&&m){b=document.createElement("button");b.type="button";b.id="crdaram";b.className="minib";b.dataset.id=id;b.setAttribute("aria-label","다람에게 물어보기");
    var face="";try{face=pf("det1","")}catch(e){}b.innerHTML=face+"<span>다람에게 물어보기</span>";b.onclick=function(e){e.stopPropagation();ask()};
    var ce=tx.querySelector("#crexam"),ca=tx.querySelector(".cr-act");if(ce&&ce.nextSibling)tx.insertBefore(b,ce.nextSibling);else if(ca)tx.insertBefore(b,ca);else tx.appendChild(b)}}catch(e){}}
  var st0=document.createElement("style");st0.textContent="html body.w209 .crec2 #crdaram{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;min-height:44px!important;box-sizing:border-box}html body.w209 .crec2 #crdaram>svg{width:26px;height:26px;flex:none;border-radius:50%;background:#F3E6CB;clip-path:circle(50%)}";
  (document.head||document.documentElement).appendChild(st0);
  try{new MutationObserver(function(){if(!q)q=requestAnimationFrame(sync)}).observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:["class"]})}catch(e){MISS.push("dobs")}
 })();

 /* D4: 아이콘 띠가 넘칠 때만 좌우 화살표(남은 개수 표시), 선택한 증거는 보이게 스크롤 */
 (function(){
  var q=0,lastSel=null;
  function upd(){q=0;try{var inr=document.querySelector(".crec2 .cr-in"),g=inr&&inr.querySelector(".cr-grid");if(!g)return;
   var L=inr.querySelector(".crar.l"),R=inr.querySelector(".crar.r");
   if(!L){L=document.createElement("button");L.type="button";L.className="crar l";L.setAttribute("aria-label","앞 증거 보기");L.innerHTML="&#9664;<b></b>";L.onclick=function(e){e.stopPropagation();g.scrollBy({left:-(g.clientWidth-60)})};inr.appendChild(L)}
   if(!R){R=document.createElement("button");R.type="button";R.className="crar r";R.setAttribute("aria-label","뒤 증거 보기");R.innerHTML="&#9654;<b></b>";R.onclick=function(e){e.stopPropagation();g.scrollBy({left:g.clientWidth-60})};inr.appendChild(R)}
   if(!g.__d4){g.__d4=1;g.addEventListener("scroll",function(){if(!q)q=requestAnimationFrame(upd)},{passive:true})}
   var top=g.offsetTop+2,h=g.offsetHeight-4;[L,R].forEach(function(b){b.style.top=top+"px";b.style.height=h+"px"});
   var ths=[].slice.call(g.querySelectorAll(".cr-th")),gl=g.getBoundingClientRect(),left=0,right=0;
   ths.forEach(function(t){var r=t.getBoundingClientRect();if(r.right<gl.left+8)left++;else if(r.left>gl.right-8)right++});
   L.hidden=!left;R.hidden=!right;L.querySelector("b").textContent=left?left:"";R.querySelector("b").textContent=right?right:"";
   var on=g.querySelector(".cr-th.on");if(on&&on.dataset.crs!==lastSel){lastSel=on.dataset.crs;var r=on.getBoundingClientRect();if(r.left<gl.left||r.right>gl.right)g.scrollLeft+=(r.left<gl.left?r.left-gl.left-12:r.right-gl.right+12)}
  }catch(e){}}
  try{new MutationObserver(function(){if(!q)q=requestAnimationFrame(upd)}).observe(document.body,{childList:true,subtree:true})}catch(e){}
  window.addEventListener("resize",function(){if(!q)q=requestAnimationFrame(upd)});
 })();

 /* E: 오른쪽 위 묶음에 '더보기' — 힌트·줄기·이동·설정·처음부터·기본 게임은 펼침 안에 그대로 */
 try{var _railE=rail;rail=function(){_railE.apply(this,arguments);try{var r=q("#w209rail");if(!r||!B.classList.contains("w209"))return;
   var g=r.querySelector(".g");if(!g)return;
   var mb=document.createElement("button");mb.type="button";mb.dataset.more="1";mb.setAttribute("aria-label","더보기");mb.innerHTML='<span style="font-size:18px;line-height:18px">&#8943;</span>더보기';g.appendChild(mb);
   var hp=r.querySelector(".rh .hp"),m=document.createElement("div");m.id="w209more";
   m.innerHTML='<div class="hd"><b>가로 시험본 · 1장</b>'+(hp?'<span class="hp">'+hp.innerHTML+'</span>':'')+'</div>';
   ["hint","spine","move","set"].forEach(function(k){var b=g.querySelector('[data-w="'+k+'"]');if(b){var c=b.cloneNode(true);c.style.display="flex";c.onclick=function(e){e.preventDefault();r.classList.remove("more");b.click()};m.appendChild(c)}});
   var ft=r.querySelector(".ft");if(ft){var rs=ft.querySelector('[data-w="reset"]');if(rs)m.appendChild(rs);var a=ft.querySelector("a");if(a)m.appendChild(a)}
   var cl=document.createElement("button");cl.type="button";cl.textContent="닫기";cl.onclick=function(e){e.preventDefault();r.classList.remove("more")};m.appendChild(cl);
   r.appendChild(m);mb.onclick=function(e){e.preventDefault();e.stopPropagation();r.classList.toggle("more")};
  }catch(e){MISS.push("railE "+e.message)}}}catch(e){MISS.push("railE0")}
 document.addEventListener("pointerdown",function(e){var r=q("#w209rail");if(r&&r.classList.contains("more")&&!r.contains(e.target))r.classList.remove("more")},true);

 /* F: 장면 속 주민 전신 — 기존 art/body/{키}-0.png를 그대로 써서 장면 단위(--u)로 크기를 맞춘다.
    바닥 주민(위치 60% 아래): 발이 바닥에 닿게 키 72u. 높은 곳 주민(카운터 뒤): 기준점 아래 15u에서 잘라 상반신만 보인다. */
 (function(){
  var q=0,cache={};
  function nat(k,cb){if(cache[k])return cb(cache[k]);var im=new Image();im.onload=function(){cache[k]=[im.naturalWidth,im.naturalHeight];cb(cache[k])};im.onerror=function(){};im.src="art/body/"+k+"-0.png"}
  function fix(){q=0;try{var sc=document.querySelector("#bigscene");if(!sc||!B.classList.contains("w209"))return;
   var u=parseFloat(getComputedStyle(sc).getPropertyValue("--u"))||1.95;
   sc.querySelectorAll(".npc").forEach(function(n){var k=n.dataset.npc;if(!k||n.dataset.f210===String(u))return;
    nat(k,function(d){try{var top=parseFloat(n.style.top)||50,floor=top>=60,H=(floor?66:62)*u,W=H*d[0]/d[1];
     var vis=floor?H:Math.min(H,(top>=60?H:H*.62)),ft=floor?22*u:15*u;
     n.classList.add("f210");n.classList.toggle("up",!floor);
     n.style.setProperty("--ih",H+"px");n.style.setProperty("--iw",W+"px");n.style.setProperty("--vh",vis+"px");
     n.style.setProperty("--fw",Math.round(W*.72)+"px");n.style.setProperty("--fh",Math.round(vis)+"px");n.style.setProperty("--ft",ft+"px");
     var c=n.querySelector(".npcclip");if(!c){c=document.createElement("div");c.className="npcclip";c.innerHTML='<img alt="" draggable="false" src="art/body/'+k+'-0.png">';n.insertBefore(c,n.firstChild)}
     n.dataset.f210=String(u)}catch(e){}})})}catch(e){}}
  try{new MutationObserver(function(){if(!q)q=requestAnimationFrame(fix)}).observe(document.body,{childList:true,subtree:true})}catch(e){}
  window.addEventListener("resize",function(){document.querySelectorAll("#bigscene .npc").forEach(function(n){delete n.dataset.f210});if(!q)q=requestAnimationFrame(fix)});
 })();






 /* ===== H 후보 (로컬 비교용) =====
    1) 대화용 큰 그림은 고해상도 원본(art/portrait/), 장면용 작은 그림은 도트(art/body/)로 경로 분리
    2) 화면에 보이는 '왕구' 이름을 '로웬'으로 (내부 키 wanggu·저장 형식은 그대로)
    3) 원탁 회의: 한 장면에 고정 좌석으로 앉아 말풍선으로 대화 (기존 회의 엔진의 진행·증거·투표를 그대로 쓰고 화면만 바꿈) */
 (function(){
  /* ---- 1) 고해상도 대화 그림 ---- */
  /* 대화용 큰 그림 표정 표 (교체 가능): 파일 art/portrait/{키}-{이름}.png, 값 = 그 파일의 실제 보이는 키(px, 1100 캔버스).
     v2 기본(0)·당황(2)은 같은 배율(기본 키)로 쓰고, v3 주장·의심·동조·반박은 각자 키로 나눠 기본과 같은 보이는 키가 되게 한다. 바닥선 1050·발 기준 550 공통 */
  window.__PORT=window.__PORT||{
   karo:  {base:816,file:{normal:"0",fluster:"2",assert:"assert",doubt:"doubt",agree:"agree",rebuttal:"rebuttal"},vh:{assert:639,doubt:640,agree:625,rebuttal:613}},
   wanggu:{base:791,file:{normal:"0",fluster:"2",assert:"assert",doubt:"doubt",agree:"agree",rebuttal:"rebuttal"},vh:{assert:600,doubt:600,agree:596,rebuttal:594}},
   nabi:  {base:934,file:{normal:"0",fluster:"2",assert:"assert",doubt:"doubt",agree:"agree",rebuttal:"rebuttal"},vh:{assert:611,doubt:607,agree:614,rebuttal:591}}};
  /* 대사 기분 → 표정 이름 (교체 가능) */
  window.__MOOD_EXPR=window.__MOOD_EXPR||{neutral:"normal",angry:"rebuttal",pout:"rebuttal",tense:"rebuttal",smug:"assert",claim:"assert",think:"doubt",confused:"doubt",doubt:"doubt",huh:"doubt",happy:"agree",smile:"agree",laugh:"agree",
   nervous:"fluster",shock:"fluster",embarrassed:"fluster",panic:"fluster",scared:"fluster",worried:"fluster",sad:"fluster",cry:"fluster",shy:"fluster"};
  function exprOf(mood,pose){var m=String(mood||"").split(/\s+/)[0];if(m&&window.__MOOD_EXPR[m])return window.__MOOD_EXPR[m];return pose==="2"?"fluster":pose==="1"?"doubt":"normal"}
  function hiSwap(root){try{(root||document).querySelectorAll("#vnfig img.b202,.tfig img.b202,#sbfocus img.b202").forEach(function(im){
    var k=im.dataset.k,P=window.__PORT[k];if(!P)return;var mood="";
    if(im.closest("#vnfig")){try{mood=(typeof DL!=="undefined"&&DL&&DL.stageMood)||""}catch(e){}}
    var ex=exprOf(mood,im.dataset.pose);if(!P.file[ex])ex=ex==="fluster"?"fluster":"normal";
    var src="art/portrait/"+k+"-"+P.file[ex]+".png",hs=1100/((P.vh&&P.vh[ex])||P.base);
    if(im.getAttribute("src")!==src)im.setAttribute("src",src);im.dataset.expr=ex;im.style.setProperty("--hs",hs.toFixed(4));im.classList.add("hires")})}catch(e){}}
  /* ---- 2) 표시 이름 로웬 ---- */
  function jo(m,p){var M={"가":"이","는":"은","를":"을","야":"아","라":"이라","다":"이다","예":"이에","와":"과","로":"으로","여":"이여"};return "로웬"+(M[p]!=null?M[p]:p)}
  function ren(v){return typeof v==="string"?v.replace(/왕구(가|는|를|야|라|다|예|와|로|여)?/g,function(m,p){return p?jo(m,p):"로웬"}):v}
  function walk(o,d){if(!o||d>8)return;if(Array.isArray(o)){for(var i=0;i<o.length;i++){if(typeof o[i]==="string")o[i]=ren(o[i]);else walk(o[i],d+1)}return}
   if(typeof o==="object")Object.keys(o).forEach(function(k){var v=o[k];if(typeof v==="string")o[k]=ren(v);else if(v&&typeof v==="object")walk(v,d+1)})}
  try{if(CAST.wanggu){CAST.wanggu.name="로웬";CAST.wanggu.kind=ren(CAST.wanggu.kind||"")}}catch(e){MISS.push("ren cast")}
  try{CASES.forEach(function(c){if(c.id==="envelope")walk(c,0)});if(window.DEBATE&&DEBATE.envelope)walk(DEBATE.envelope,0);if(window.__MEMO)walk(window.__MEMO,0)}catch(e){MISS.push("ren data "+e.message)}

  /* ---- 3) 원탁 회의 장면 ---- */
  var st=document.createElement("style");st.id="h210rt";st.textContent=[
   "html body.w209 #dlgveil #vnfig.b202,html body.w209 .fstalk .tstage .tfig.b202{top:9vh!important;height:100vh!important}",
   "html body.w209 #dlgveil #vnfig.b202 img.b202.hires,html body.w209 .fstalk .tstage .tfig.b202 img.b202.hires,html body.w209 #sbfocus img.b202.hires{top:auto!important;bottom:calc(var(--hs) * -100% * 50 / 1100)!important;height:calc(var(--hs) * 100%)!important;width:auto!important;image-rendering:auto!important}",
   "html body.rtg>div.rt.rt{background:none!important;background-image:none!important}",
   "body.rtg .rt{background:transparent!important;display:block!important;overflow:hidden!important;z-index:60!important}",
   "body.rtg .rt-in{max-width:none!important;width:100%!important;height:100%!important;padding:0!important;display:block!important;position:relative}",
   "body.rtg .rt-seats,body.rtg .rt-big,body.rtg .rt-sn{display:none!important}",
   "body.rtg #w209rail{display:none!important}",
   /* 장면 */
   "#rtg{position:fixed;inset:0;z-index:58;overflow:hidden;background:#1a120c}",
   "#rtg .stg{position:absolute;left:50%;top:50%;width:max(100vw,calc(100vh * 1672 / 941));aspect-ratio:1672/941;transform:translate(-50%,-50%)}",
   "#rtg .bg{position:absolute;inset:0;background:url(art/council/council-room-background-v1.png) center/100% 100% no-repeat;filter:brightness(.82)}",
   "#rtg .tbl{position:absolute;left:-5%;width:110%;top:54%;aspect-ratio:2120/742;z-index:3;pointer-events:none}",
   "#rtg .tbl img{display:block;width:100%;height:auto}",
   "#rtg .seat{position:absolute;transform:translateX(-50%);pointer-events:none}",
   "#rtg .seat>svg{display:block;height:100%;width:auto}",
   "#rtg .seat img{display:block;height:100%;width:auto;image-rendering:pixelated;filter:drop-shadow(0 4px 4px rgba(0,0,0,.35));transition:filter .2s}",
   "#rtg .seat.flip:not(.sa) img{transform:scaleX(-1)}","#rtg .seat.sa{aspect-ratio:1/1}","#rtg .seat.sa img{image-rendering:auto;width:100%;height:100%}",
   "#rtg .seat.dim img{filter:brightness(.72) drop-shadow(0 4px 4px rgba(0,0,0,.35))}",
   "#rtg .seat.on img{filter:brightness(1.06) drop-shadow(0 0 3px rgba(255,216,77,.9)) drop-shadow(0 4px 4px rgba(0,0,0,.35))}",
   "#rtg .seat .nm{display:none;position:absolute;left:50%;transform:translateX(-50%);top:calc(var(--tb) - 4px);font:12px/1 var(--display,sans-serif);color:#FFF6E0;background:rgba(20,16,30,.72);padding:3px 7px;border-radius:999px;white-space:nowrap;z-index:2}",
   "#rtg .seat .rtgrx{display:block;height:auto;width:auto;min-height:0;position:absolute;left:62%;top:14%;transform:none;z-index:3;font:13px/1.2 var(--display,sans-serif);color:#2A2F45;background:#FFFCF3;border:2px solid #2A2F45;border-radius:12px;padding:3px 9px;white-space:nowrap;box-shadow:0 2px 0 rgba(0,0,0,.3)}",
   "#rtg .table-old{display:none;position:absolute;left:-12%;right:-12%;top:66%;height:80%;border-radius:50% 50% 0 0/26% 26% 0 0;background:radial-gradient(ellipse at 50% 18%,#9a6a3c 0%,#7a4e2a 45%,#4e3019 100%);box-shadow:inset 0 6px 0 #b98450,inset 0 -30px 60px rgba(0,0,0,.45),0 -4px 18px rgba(0,0,0,.4);z-index:3}",
   "#rtg .table:after{content:'';position:absolute;left:38%;top:7%;width:24%;height:18%;background:#E9DCB8;border-radius:4px;transform:rotate(-3deg);box-shadow:0 2px 0 rgba(0,0,0,.25)}",
   "#rtg .front{z-index:4}","#rtg .front.near{z-index:2}",
   "#rtg .tmp{position:absolute;right:8px;top:auto;bottom:4px;z-index:9;font:10px/1.2 sans-serif;color:rgba(255,246,224,.6);max-width:42vw;text-align:right}",
   /* 위쪽 표시 */
   "#rtgtpc{position:fixed;left:50%;top:6px;transform:translateX(-50%);z-index:62;max-width:min(44vw,420px);padding:6px 14px;border-radius:6px;background:#F4EEDC;border:2px solid #C9A96A;color:#2A2F45;font:13px/1.25 var(--display,sans-serif);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;box-shadow:0 2px 0 rgba(0,0,0,.35)}#rtgtpc b{color:#8A2E2E;font-weight:400}",
   "#rtgtop{position:fixed;left:8px;top:6px;z-index:62;display:flex;align-items:center;gap:8px;max-width:22vw;padding:5px 12px;border-radius:10px;background:rgba(20,16,30,.78);border:1.5px solid #C9A96A;color:#FFF6E0;font:14px/1.2 var(--display,sans-serif)}",
   "#rtgtop b{color:#FFD84D;font-weight:400;white-space:nowrap}#rtgtop span{font-size:12px;color:#E6DCC4;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}",
   "#rtgtop i{display:inline-block;width:8px;height:8px;border-radius:2px;background:#E0474C;margin-left:2px}#rtgtop i.off{background:#3A3F5C}",
   "#rtgtr{position:fixed;right:8px;top:6px;z-index:62;display:flex;gap:6px}",
   "#rtgtr button,#rtgbar button{font:13px/1 var(--display,sans-serif);color:#FFF6E0;background:rgba(20,16,30,.85);border:1.5px solid #C9A96A;border-radius:10px;height:34px;padding:0 12px;cursor:pointer;position:relative}",
   "#rtgtr button:after,#rtgbar button:after{content:'';position:absolute;left:0;right:0;top:-5px;bottom:-5px}",
   /* 아래 버튼 */
   "#rtgbar{position:fixed;left:50%;bottom:8px;transform:translateX(-50%);z-index:62;display:flex;gap:8px}",
   "#rtgbar button{height:38px;min-width:min(27vw,150px)}",
   "#rtgbar button[disabled]{opacity:.45}",
   "#rtgbar button.rtghot{border-color:#FFD84D!important;color:#FFE9A8!important;box-shadow:none!important;border-radius:10px!important}",
   /* 엔진 요소 다시 배치 */
   "body.rtg .rt-top{display:none!important}",
   "body.rtg .rt-goal{display:none!important}",
   "body.rtg .rt-goal b{display:inline!important;font-size:12px!important;margin-right:6px}",
   "body.rtg .rt-mid{position:static!important;display:block!important;min-height:0!important;height:0!important;padding:0!important;margin:0!important;background:none!important;border:0!important}",
   "body.rtg .rt-srow{display:contents!important}",
   "html body.rtg:not(.ds-mc) .rt .rt-bub{border:2.5px solid #2A2F45!important;border-image:none!important;background:#FFFCF3!important;border-radius:14px!important;filter:none!important;box-shadow:0 3px 0 rgba(0,0,0,.35)!important;padding:6px 12px 7px!important;outline:0!important}",
   "body.rtg .rt-bub{position:fixed!important;z-index:61;margin:0!important;width:var(--bw2,320px)!important;max-width:calc(100vw - 24px)!important;box-sizing:border-box;padding:7px 12px 8px!important;background:#FFFCF3!important;color:#1B2447!important;border:2.5px solid #2A2F45!important;border-radius:14px!important;box-shadow:0 3px 0 rgba(0,0,0,.35)!important;min-height:0!important}",
   "body.rtg .rt-bub small{display:block;font-size:12px!important;color:#8A2E2E!important;margin:0 0 2px!important}",
   "html body.rtg .rt .rt-bub p{margin:0!important;font-size:15px!important;line-height:1.45!important}","html body.rtg .rt .rt-bub small{font-size:12px!important;margin:0 0 1px!important}","html body.rtg .rt .rt-bub .wk{padding:0 4px!important;min-height:0!important;line-height:1.3!important}",
   "body.rtg .rt-bub .nx{display:none!important}",
   "body.rtg .rt-bub:after{content:'';position:absolute;left:var(--tx,40px);width:14px;height:14px;background:#FFFCF3;border:2.5px solid #2A2F45;border-top:0;border-left:0;transform:rotate(45deg);bottom:-9px}",
   "body.rtg .rt-bub.tl:after{bottom:auto;top:-9px;transform:rotate(225deg)}",
   "body.rtg .rt-bub.sd:after{display:none}",
   "body.rtg .rt-nav{position:fixed!important;left:50%;bottom:54px;transform:translateX(-50%);z-index:62;margin:0!important;width:auto!important;max-width:calc(100vw - 24px);background:rgba(20,16,30,.85);border-radius:8px;padding:3px 10px!important;font-size:12px!important}",
   "body.rtg .rt-nav span{font-size:12px!important}",
   "body.rtg .rt-evd,body.rtg .rt-bul{display:none!important}",
   "body.rtg .rt-foot{display:none!important}",
   "body.rtg.rtg-drw .rt-bul{display:flex!important;flex-wrap:wrap;gap:6px;position:fixed!important;left:auto;right:8px;bottom:54px;transform:none;z-index:63;width:min(480px,calc(66vw - 24px))!important;max-height:42vh;overflow:auto;padding:8px!important;background:rgba(20,16,30,.94);border:1.5px solid #C9A96A;border-radius:12px;margin:0!important}",
   "body.rtg.rtg-drw .rt-bul .bl{flex:1 1 calc(50% - 6px);min-height:40px!important}",
   "body.rtg.rtg-drw .rt-evd{display:block!important;position:fixed!important;left:8px;transform:none;z-index:63;width:min(250px,30vw)!important;margin:0!important;font-size:12.5px!important;top:46px;bottom:auto;max-height:calc(100vh - 110px - var(--dh,120px));overflow:auto;background:#F4EEDC!important;color:#2A2F45!important;border:2px solid #C9A96A!important;border-radius:8px!important}",
   "body.rtg.rtg-drw .rt-nav{display:none!important}",
   /* 투표: 엔진 투표판을 장면 위 가운데에 */
   "body.rtg .rt-mid.vote{display:none!important}",
   "#rtgvote .hd{position:fixed;left:50%;top:6px;transform:translateX(-50%);z-index:62;text-align:center;padding:5px 18px 6px;border-radius:6px;background:#F4EEDC;border:2px solid #C9A96A;color:#2A2F45;font:15px/1.25 var(--display,sans-serif);box-shadow:0 2px 0 rgba(0,0,0,.35);max-width:min(56vw,460px)}",
   "#rtgvote .hd b{color:#8A2E2E;font-weight:400}#rtgvote .hd small{display:block;font-size:11.5px;color:#6B5A3A}",
   "#rtgvote .tc{position:absolute;transform:translate(-50%,0);z-index:6;padding:3px 9px 4px;border-radius:6px;background:#F4EEDC;border:1.5px solid #C9A96A;color:#2A2F45;font:12px/1.25 var(--display,sans-serif);text-align:center;white-space:nowrap;box-shadow:0 2px 0 rgba(0,0,0,.3)}",
   "#rtgvote .tc b{font-weight:400;color:#8A2E2E;margin-left:3px}#rtgvote .tc i{display:block;font-style:normal;font-size:10.5px;color:#6B5A3A}",
   "#rtgvote .pk{position:fixed;left:50%;bottom:8px;transform:translateX(-50%);z-index:62;display:flex;gap:6px;align-items:center;padding:5px 8px;border-radius:10px;background:rgba(20,16,30,.88);border:1.5px solid #C9A96A;color:#FFF6E0;font:12px/1 var(--display,sans-serif);max-width:calc(100vw - 16px);flex-wrap:wrap;justify-content:center}",
   "#rtgvote .pk button{position:relative;height:34px;padding:0 12px;border-radius:8px;border:1.5px solid #C9A96A;background:#2A2236;color:#FFF6E0;font:13px/1 var(--display,sans-serif)}#rtgvote .pk button:after{content:'';position:absolute;left:0;right:0;top:-5px;bottom:-5px}#rtgvote .pk button[disabled]{opacity:.5}",
   /* 기록 */
   "#rtglog{position:fixed;left:8px;bottom:54px;max-height:min(46vh,240px);width:min(560px,64vw);z-index:64;overflow:auto;background:rgba(20,16,30,.95);border:1.5px solid #C9A96A;border-radius:12px;padding:8px 10px;color:#FFF6E0;font:13px/1.45 var(--body,sans-serif)}",
   "#rtglog p{margin:0;padding:5px 0;border-top:1px solid rgba(201,169,106,.35);display:flex;gap:8px;align-items:baseline}#rtglog b{flex:none;min-width:58px;text-align:center;color:#FFD84D;font-weight:400;background:rgba(255,255,255,.07);border:1px solid rgba(201,169,106,.6);border-radius:6px;padding:1px 6px;font-size:12px}#rtglog .now{color:#FFE9A8}",
   "#rtglog .dm{font-size:11px;color:#9FB0DA;margin-bottom:6px}"
  ].join("\n");(document.head||document.documentElement).appendChild(st);

  var SC=null,TOP=null,TPC=null,VT=null,TR=null,BAR=null,LOG=null,HIST=[],lastKey="",timer=0,tStart=0,tNeed=0,prevSus=null,logOpen=false;
  function rtEl(){return document.querySelector("body>.rt")}
  function nameOf(k){if(k==="det0")return (S.players&&S.players[0])||"아빠";if(k==="det1")return (S.players&&S.players[1])||"다람";return (CAST[k]||{}).name||k}
  /* 앉은 그림 (교체 가능): art/seat/{키}-{표정}.png, 800x800, 몸 중심 x400·탁자선 y560. 목록에 없는 표정은 normal */
  window.__RTG_SEAT=window.__RTG_SEAT||{karo:["normal","reaction"],wanggu:["normal","reaction"],nabi:["normal","reaction"],det1:["normal"],buri:["normal"]};
  window.__RTG_EXPR=window.__RTG_EXPR||{fluster:"reaction",rebuttal:"reaction",doubt:"normal",assert:"normal",agree:"normal",normal:"normal"};
  function seatSrc(k,m){var L=window.__RTG_SEAT[k];if(!L||!L.length)return null;var e=window.__RTG_EXPR[exprOf(m,"0")]||"normal";if(L.indexOf(e)<0)e="normal";return "art/seat/"+k+"-"+e+".png"}
  function figHtml(k,m){var ss=seatSrc(k,m);if(ss)return '<img alt="" class="sf seat-art" draggable="false" src="'+ss+'">';var h="";try{h=window.__stageFig?window.__stageFig(k,m||""):""}catch(e){}
   if(!/img/.test(h)){try{h=pf(k,m||"")}catch(e){h=""}return h}return h.replace(/class="b202"/,'class="sf"')}
  function seatsOf(r){return [].map.call(r.querySelectorAll(".rt-seats .rs[data-seat]"),function(x){return x.dataset.seat})}
  function moodOf(r){var g=r.querySelector(".rt-big g[id^='an-']");if(!g)return "";var p=g.id.split("-");return p.slice(2).join("-")}
  function layout(n){/* 뒷줄 좌석: 화면 너비 비율 x, 아래쪽 y(발 기준선, 탁자에 가려짐), 키 비율 h */
   var L=[],x0=26,x1=90;for(var i=0;i<n;i++){var t=n===1?.5:i/(n-1),x=x0+(x1-x0)*t,mid=1-Math.abs(t-.5)*2;var hh=38-mid*2,far=72-mid*3;L.push({x:x,b:far+hh*.42,h:hh,far:far})}return L}
  function build(r){
   if(!SC){SC=document.createElement("div");SC.id="rtg";document.body.appendChild(SC)}
   var ks=seatsOf(r);if(!ks.length&&SC.dataset.k)ks=SC.dataset.k.split(",");var key=ks.join(",");
   if(SC.dataset.k!==key){var P=layout(ks.length),h='<div class="stg"><div class="bg"></div>';
    ks.forEach(function(k,i){var p=P[i],sa=!!seatSrc(k,"");
     /* 앉은 그림: 캔버스 높이 44%, y560(70%)을 원탁 먼 가장자리(far)에 맞춤. 없으면 서 있는 도트를 원탁으로 가림(임시) */
     var bot=sa?(p.far+42*.30):p.b,hh=sa?42:p.h;
     h+='<div class="seat'+(sa?' sa':'')+'" data-k="'+k+'" data-far="'+p.far+'" style="left:'+p.x+'%;bottom:'+(100-bot)+'%;height:'+hh+'%;--tb:100%">'+figHtml(k,"")+'<span class="nm">'+esc(nameOf(k))+'</span></div>'});
    var tmpN=ks.filter(function(k){return !seatSrc(k,"")}).map(nameOf);
    h+='<div class="tbl"><img alt="" src="art/council/council-table-foreground-v1.png"></div>';
    var dsa=!!seatSrc("det1","");/* 다람: 아빠 옆 근경, 원탁 왼쪽 끝에 앉음. 탁자선 y560을 그 자리 원탁 가장자리(무대 높이 약 72%)에 맞추고 원탁 뒤에 둠 */
    h+='<div class="seat front'+(dsa?' sa near':'')+'" data-k="det1" data-far="75" style="left:'+(dsa?15:12)+'%;bottom:'+(dsa?(100-(75+52*.30)):8)+'%;height:'+(dsa?52:50)+'%;--tb:100%">'+figHtml("det1","")+'<span class="nm">'+esc(nameOf("det1"))+'</span></div>';
    h+='</div>'+(tmpN.length?'<span class="tmp">임시 자산: '+esc(tmpN.join("·"))+' 앉은 그림 없음(서 있는 그림을 원탁으로 가림)</span>':'');
    SC.innerHTML=h;SC.dataset.k=key}
   if(!TOP){TOP=document.createElement("div");TOP.id="rtgtop";document.body.appendChild(TOP)}
   if(!TR){TR=document.createElement("div");TR.id="rtgtr";TR.innerHTML='<button type="button" data-g="hint">힌트</button><button type="button" data-g="leave">수사로</button><button type="button" data-g="log">발언 기록</button>';document.body.appendChild(TR);
    TR.onclick=function(e){var b=e.target.closest("[data-g]");if(!b)return;var g=b.dataset.g;
     if(g==="log"){logOpen=!logOpen;b.textContent=logOpen?"기록 닫기":"발언 기록";drawLog();return}
     var x=document.querySelector(g==="hint"?"#rthint":"#rtleave");if(x)x.click()}}
   if(!BAR){BAR=document.createElement("div");BAR.id="rtgbar";BAR.innerHTML='<button type="button" data-g="ev">증거 보기</button><button type="button" data-g="obj">끼어들기</button><button type="button" data-g="next">계속 듣기</button><button type="button" data-g="present">제시하기</button><button type="button" data-g="back">돌아가기</button>';document.body.appendChild(BAR);
    BAR.onclick=function(e){var b=e.target.closest("[data-g]");if(!b||b.disabled)return;act(b.dataset.g)}}
  }
  function act(g){var r=rtEl();if(!r)return;var talk=!!r.querySelector("#rtnext"),deb=!!r.querySelector(".rt-bub.stm");
   if(g==="back"){B.classList.remove("rtg-drw");delete B.dataset.rtgsel;sync();return}
   if(g==="present"){var s0=r.querySelector(".rt-bul .bl.on");if(!s0)return;B.classList.remove("rtg-drw");delete B.dataset.rtgsel;var w0=r.querySelector(".rt-bub.stm .wk");if(w0)w0.click();return}
   if(g==="next"){if(talk){r.querySelector("#rtnext").click()}else if(deb){var nx=r.querySelector("#rtnx");if(nx)nx.click()}return}
   if(g==="ev"){if(deb&&!talk){B.classList.toggle("rtg-drw");sync();return}
    try{openRecord(CASES[G.ci],"view")}catch(e){}return}
   if(g==="obj"){if(!deb||talk)return;var sel=r.querySelector(".rt-bul .bl.on");if(!sel){B.classList.add("rtg-drw");sync();return}
    B.classList.remove("rtg-drw");var w=r.querySelector(".rt-bub.stm .wk");if(w)w.click()}}
  function drawLog(){if(!logOpen){if(LOG){LOG.remove();LOG=null}return}
   if(!LOG){LOG=document.createElement("div");LOG.id="rtglog";document.body.appendChild(LOG)}
   LOG.innerHTML='<div class="dm">공개 발언 · 최근 것이 아래 (열려 있는 동안 회의는 멈춰요)</div>'+HIST.map(function(h,i){return '<p class="'+(i===HIST.length-1?"now":"")+'"><b>'+esc(h.n)+'</b>'+esc(h.t)+'</p>'}).join("");LOG.scrollTop=1e6}
  function rect(el){return el.getBoundingClientRect()}
  function heads(){return [].map.call(SC.querySelectorAll(".seat"),function(s){var r=rect(s.querySelector("img")||s);
    if(s.classList.contains("sa")){var front=s.classList.contains("front");/* 800 캔버스 기준 얼굴·손 영역 */
     return front?{k:s.dataset.k,l:r.left+r.width*.3,r:r.left+r.width*.7,t:r.top+r.height*.19,b:r.top+r.height*.5,cx:r.left+r.width*.5}
                 :{k:s.dataset.k,l:r.left+r.width*.3,r:r.left+r.width*.7,t:r.top+r.height*.12,b:r.top+r.height*.46,cx:r.left+r.width*.5}}
    return {k:s.dataset.k,l:r.left+r.width*.18,r:r.right-r.width*.18,t:r.top,b:r.top+r.height*.42,cx:(r.left+r.right)/2}})}
  function ov(a,b){return !(a.r<=b.l||a.l>=b.r||a.b<=b.t||a.t>=b.b)}
  function place(bub,spk){/* 말풍선 위치: 화자 머리 위 → 옆 → 위쪽 가운데. 다른 얼굴·버튼과 겹치지 않는 첫 자리 */
   var W=innerWidth,H=innerHeight,bw=Math.min(W*0.46,360);bub.style.setProperty("--bw2",bw+"px");bub.style.left="0px";bub.style.top="0px";
   var bh=rect(bub).height,HD=heads(),me=HD.filter(function(h){return h.k===spk})[0],topLim=40,botLim=H-52;
   var others=HD.filter(function(h){return h!==me});
   var cands=[];
   if(me){var cx=me.cx;
    cands.push({l:cx-bw*.3,t:me.t-bh-10,cls:"",tx:bw*.3-7});
    cands.push({l:cx-bw*.7,t:me.t-bh-10,cls:"",tx:bw*.7-7});
    cands.push({l:me.r+8,t:me.t,cls:"sd"});cands.push({l:me.l-8-bw,t:me.t,cls:"sd"});
    cands.push({l:cx-bw/2,t:me.b+6,cls:"tl",tx:bw/2-7})}
   cands.push({l:(W-bw)/2,t:topLim+2,cls:"sd"});
   var best=null,bs=1e9;
   cands.forEach(function(c){var l=Math.max(8,Math.min(W-bw-8,c.l)),t=Math.max(topLim,Math.min(botLim-bh,c.t)),R={l:l,r:l+bw,t:t,b:t+bh};
    var s=0;others.forEach(function(h){if(ov(R,h))s+=1});if(me&&ov(R,me))s+=2;if(R.b>botLim)s+=3;
    s+=Math.abs(l-c.l)/400+Math.abs(t-c.t)/400;if(s<bs){bs=s;best={l:l,t:t,cls:c.cls,tx:c.tx!=null?c.tx-(l-c.l):null}}});
   bub.style.left=best.l+"px";bub.style.top=best.t+"px";bub.classList.remove("tl","sd");if(best.cls)bub.classList.add(best.cls);
   if(best.tx!=null)bub.style.setProperty("--tx",Math.max(12,Math.min(bw-26,best.tx))+"px");else bub.classList.add("sd");
   bub.dataset.ovl=String(Math.floor(bs))}
  function reactions(spk,mood){/* 반응(데모): 대사 데이터에 반응 정보가 없어서, 이번 발언에서 의심 수치가 바뀐 주민을 놀람/안도로 표시하고,
      나머지는 화자 쪽으로 고개를 돌린다. 짧은 반응 말풍선은 1개만. 새 대사는 만들지 않고 기호만 쓴다. */
   var sus={};try{sus=JSON.parse(JSON.stringify((G.debate&&G.debate.sus)||{}))}catch(e){}
   var d={};if(prevSus)Object.keys(sus).forEach(function(k){var a=sus[k]-(prevSus[k]==null?10:prevSus[k]);if(a)d[k]=a});prevSus=sus;
   var sp=SC.querySelector('.seat[data-k="'+spk+'"]'),sx=sp?parseFloat(sp.style.left):50,rxDone=false;
   SC.querySelectorAll(".seat").forEach(function(s){var k=s.dataset.k,x=parseFloat(s.style.left),old=s.querySelector(".rtgrx");if(old)old.remove();
    s.classList.toggle("on",k===spk);s.classList.toggle("dim",!!spk&&k!==spk);s.classList.toggle("flip",!!spk&&k!==spk&&x>sx);
    var m=k===spk?mood:(d[k]>0?"nervous":"");var want=figHtml(k,m),im=s.querySelector("img"),src=(want.match(/src="([^"]+)"/)||[])[1];if(im&&src&&im.getAttribute("src")!==src)im.setAttribute("src",src);
    if(!rxDone&&k!==spk&&d[k]){var e=document.createElement("span");e.className="rtgrx";e.textContent=d[k]>0?"!?":"휴…";s.appendChild(e);rxDone=true}});
   if(!rxDone&&spk){var near=null,bd=1e9;SC.querySelectorAll(".seat").forEach(function(s){if(s.dataset.k===spk)return;var dx=Math.abs(parseFloat(s.style.left)-sx);if(dx<bd){bd=dx;near=s}});
    if(near){var e=document.createElement("span");e.className="rtgrx";e.textContent="…";near.appendChild(e)}}}
  function drawVote(r){/* 공개 득표·논의 대상: 엔진 투표 데이터(ph.votes)를 그대로 보여 준다. 득표는 의견이고, 지목(범인 판단)은 아래 버튼으로 따로 한다 */
   var ph=window.__rtPh&&window.__rtPh();if(!ph)return;var V=ph.votes||{},mob=ph.type==="mob",cnt={};Object.keys(V).forEach(function(v){cnt[V[v]]=(cnt[V[v]]||0)+1});
   var top=null,tn=0,tie=false;Object.keys(cnt).forEach(function(k){if(cnt[k]>tn){top=k;tn=cnt[k];tie=false}else if(cnt[k]===tn)tie=true});
   var key=JSON.stringify(V)+mob;if(VT&&VT.dataset.k===key)return;if(VT)VT.remove();VT=document.createElement("div");VT.id="rtgvote";VT.dataset.k=key;
   var h='<div class="hd">공개 득표 · 최다 <b>'+(top?esc(nameOf(top))+' '+tn+'표':'없음')+(tie?' (동률)':'')+'</b><small>논의 대상 · '+(top&&!tie?esc(nameOf(top)):'정해지지 않음')+' — 득표는 범인 확정이 아니에요</small></div>';
   var stg=SC&&SC.querySelector(".stg");
   if(stg){var tc="";stg.querySelectorAll(".seat:not(.front)").forEach(function(s){var k=s.dataset.k,far=parseFloat(s.dataset.far||66);
     tc+='<div class="tc" style="left:'+s.style.left+';top:'+(far+1.5)+'%">'+esc(nameOf(k))+'<b>'+(cnt[k]||0)+'표</b>'+(V[k]?'<i>'+esc(nameOf(k))+' → '+esc(nameOf(V[k]))+'</i>':'')+'</div>'});
    var tw=document.createElement("div");tw.className="tcw";tw.innerHTML=tc;tw.id="rtgtc";var o=stg.querySelector("#rtgtc");if(o)o.remove();stg.appendChild(tw)}
   var sus=[].map.call(r.querySelectorAll(".rt-mid.vote .vc[data-seat]"),function(b){return b.dataset.seat});
   h+='<div class="pk"><span>'+(mob?'모두의 표가 나왔어요…':'다람이 지목할 사람')+'</span>'+sus.map(function(k){return '<button type="button" data-pick="'+k+'"'+(mob?' disabled':'')+'>'+esc(nameOf(k))+'</button>'}).join("")+'</div>';
   VT.innerHTML=h;document.body.appendChild(VT);
   VT.querySelectorAll("[data-pick]").forEach(function(b){b.onclick=function(){var v=r.querySelector('.rt-mid.vote .vc[data-seat="'+b.dataset.pick+'"]');if(v)v.click()}})}
  function arm(len){clearTimeout(timer);tNeed=1400+len*70;tStart=Date.now();timer=setTimeout(tick,tNeed)}
  function paused(){return (window.__rtgPausedExtra&&window.__rtgPausedExtra())||B.classList.contains("rtg-drw")||logOpen||!!document.querySelector(".crec2")||!!document.querySelector("#ov .modal")||!!(typeof DL!=="undefined"&&DL)}
  function tick(){var r=rtEl();if(!r)return;var n=r.querySelector("#rtnext");if(!n)return;
   if(paused()){timer=setTimeout(tick,500);return}
   if(window.__rtgNoAuto)return;n.click()}
  function sync(){try{
   var r=rtEl();
   if(!r||!B.classList.contains("w209")){if(B.classList.contains("rtg")){B.classList.remove("rtg","rtg-drw");[SC,TOP,TPC,VT,TR,BAR,LOG].forEach(function(x){if(x)x.remove()});SC=TOP=TPC=VT=TR=BAR=LOG=null;HIST=[];lastKey="";prevSus=null;logOpen=false;clearTimeout(timer)}return}
   B.classList.add("rtg");build(r);
   var top=r.querySelector(".rt-top"),t1=top&&top.querySelector("b"),t2=top&&top.querySelector("span:not(.rt-hp)"),hp=top&&top.querySelector(".rt-hp");
   var gl=r.querySelector(".rt-goal b");TOP.innerHTML='<b>마을 회의</b>'+(hp?'<span>'+[].map.call(hp.querySelectorAll("i"),function(i){return '<i class="'+(i.classList.contains("on")?"":"off")+'"></i>'}).join("")+'</span>':"");
   if(!TPC){TPC=document.createElement("div");TPC.id="rtgtpc";document.body.appendChild(TPC)}
   var vt=r.querySelector(".rt-mid.vote");TPC.style.display=vt?"none":"";TPC.innerHTML=(gl?'<b>'+esc(gl.textContent)+'</b> · ':'<b>쟁점</b> · ')+esc(t2?t2.textContent:"");
   var talk=!!r.querySelector("#rtnext"),bub=r.querySelector(".rt-bub"),deb=!!r.querySelector(".rt-bub.stm"),vote=!!r.querySelector(".rt-mid.vote");
   var on=r.querySelector(".rt-seats .rs.on"),spk=on?on.dataset.seat:null,nmEl=bub&&bub.querySelector("small"),txt=bub&&bub.querySelector("p");
   if(!spk&&nmEl){var nt=(nmEl.firstChild&&nmEl.firstChild.nodeType===3?nmEl.firstChild.textContent:nmEl.textContent).trim();if(nt===nameOf("det1"))spk="det1";else if(nt===nameOf("det0"))spk="det0"}
   var drw=B.classList.contains("rtg-drw"),bg=function(g){return BAR.querySelector('[data-g="'+g+'"]')},b=[bg("ev"),bg("obj"),bg("next"),bg("present"),bg("back")];[0,1,2].forEach(function(i){b[i].style.display=drw?"none":""});[3,4].forEach(function(i){b[i].style.display=drw?"":"none"});b[3].disabled=!r.querySelector(".rt-bul .bl.on");b[1].disabled=!(deb&&!talk);b[2].disabled=!(talk||deb);b[0].classList.toggle("rtghot",B.classList.contains("rtg-drw"));
   b[1].classList.toggle("rtghot",!!r.querySelector(".rt-bul .bl.on"));
   TR.querySelector('[data-g="hint"]').style.display=r.querySelector("#rthint")?"":"none";TR.querySelector('[data-g="leave"]').style.display=r.querySelector("#rtleave")?"":"none";
   BAR.style.display=vote?"none":"";if(!vote){var tw0=SC&&SC.querySelector('#rtgtc');if(tw0)tw0.remove()}
   
   if(B.classList.contains("rtg-drw")){var bl=r.querySelector(".rt-bul");if(bl)document.documentElement.style.setProperty("--dh",rect(bl).height+"px")}
   if(bub&&txt){var key=(spk||"")+"|"+txt.textContent;
    if(key!==lastKey){lastKey=key;HIST.push({n:nmEl?(nmEl.firstChild&&nmEl.firstChild.nodeType===3?nmEl.firstChild.textContent:nmEl.textContent).trim():"",t:txt.textContent});if(HIST.length>200)HIST.shift();drawLog();
     reactions(spk,moodOf(r));if(talk)arm(txt.textContent.length);else clearTimeout(timer)}
    place(bub,spk==="det0"?null:spk)}
   else if(vote){reactions(null,"");drawVote(r)}
   if(!vote&&VT){VT.remove();VT=null}
  }catch(e){MISS.push("rtg "+e.message)}}
  var qd=0;
  try{new MutationObserver(function(ms){var mine=ms.every(function(m){var t=m.target;return t&&t.closest&&t.closest("#rtg,#rtgtop,#rtgtpc,#rtgvote,#rtgtr,#rtgbar,#rtglog")});if(mine)return;
   if(!qd)qd=requestAnimationFrame(function(){qd=0;hiSwap();sync()})}).observe(document.body,{childList:true,subtree:true})}catch(e){MISS.push("h obs")}
  window.addEventListener("resize",function(){var r=rtEl(),bub=r&&r.querySelector(".rt-bub");if(bub){var on=r.querySelector(".rt-seats .rs.on");place(bub,on?on.dataset.seat:null)}});
  window.__rtgState=function(){return {hist:HIST.length,last:lastKey,paused:paused(),need:tNeed,elapsed:Date.now()-tStart}};
 })();
 if(MISS.length)try{console.warn("w209 miss",MISS)}catch(e){}
})();
