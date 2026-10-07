/* Run the current original game with artwork adapters; use a separate preview save namespace. */
(async () => {
  const frame = document.getElementById('game-frame'), loading = document.getElementById('loading');
  try {
    const root = new URL('../', location.href), art = new URL('./', location.href);
    const r = await fetch(new URL('game.html', root), {cache:'no-cache'});
    if (!r.ok) throw Error('원작 게임을 불러오지 못했습니다.');
    let source = await r.text();
    if (!source.includes('function start(data){')) throw Error('원작의 연결 지점이 바뀌었습니다.');
    source = source.replaceAll('localStorage.', 'window.DaramPreviewStorage.');
    source = source.replace('function start(data){', 'window.__DaramBackgroundConnect=function(){return DaramSceneBridge.install({cases:CASES,scenes:SCENES,hots:HOTS,zooms:window.__ZOOM,zoomArt:ZART,portraitSetter:function(fn){pf=fn},portraitFallback:pf,refresh:function(){if(G)render()}})};function start(data){');
    const prep = '<base href="' + root.href + '"><link rel="stylesheet" href="' + new URL('game-scenes.css?v=4',art).href + '"><script>window.DaramPreviewStorage={getItem:function(k){return localStorage.getItem("daram-art-preview-v3:"+k)},setItem:function(k,v){localStorage.setItem("daram-art-preview-v3:"+k,v)},removeItem:function(k){localStorage.removeItem("daram-art-preview-v3:"+k)}};<\/script><script src="' + new URL('art-kit.js?v=4',art).href + '"><\/script><script src="' + new URL('scene-bridge.js?v=4',art).href + '"><\/script>';
    source = source.replace('</head>', prep + '</head>');
    const finish = '<script>window.__DaramBackgroundConnect().then(function(result){document.body.classList.add("daram-art-preview");var boot=document.getElementById("bootld");if(boot)boot.remove();window.__DaramArtPreviewReady=result;parent.postMessage({type:"daram-art-preview-ready"},"' + location.origin + '")}).catch(function(e){parent.postMessage({type:"daram-art-preview-error",message:e.message},"' + location.origin + '")});<\/script>';
    source = source.replace('</body>', finish + '</body>');
    addEventListener('message', event => {
      if (event.source !== frame.contentWindow || event.origin !== location.origin) return;
      if (event.data?.type === 'daram-art-preview-ready') loading.hidden = true;
      if (event.data?.type === 'daram-art-preview-error') loading.textContent = '현장 연결을 확인해 주세요. ' + event.data.message;
    });
    frame.srcdoc = source;
  } catch (e) { loading.textContent = e.message; console.error(e); }
})();
