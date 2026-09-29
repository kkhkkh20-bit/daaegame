// Usage: node flavshot.js <built.html> <out.png> "sceneKey1,sceneKey2,..."   (renders each scene 720x400 with hotspot markers, stacked 2 per row)
const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
const file=process.argv[2],out=process.argv[3],keys=process.argv[4].split(',');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});const p=await b.newPage({viewport:{width:1460,height:20+Math.ceil(keys.length/2)*410}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+file);await p.waitForTimeout(400);
await p.evaluate(keys=>{document.body.style.background='#222';document.body.innerHTML='<div id="g" style="display:grid;grid-template-columns:repeat(2,720px);gap:10px;padding:10px">'+keys.map(k=>{
  var pts=window.__T('(function(){var o=[];CASES.forEach(function(c){c.locations.forEach(function(l){if(c.id+"-"+l.id!=="'+k+'")return;l.spots.forEach(function(s){var h=HOTS[s.id];if(h&&!s.inZoom)o.push([h[0],h[1],s.id])});(l.obs||[]).forEach(function(s){o.push([s.x,s.y,"o:"+s.id])});((c.ppl||{})[l.id]||[]).forEach(function(q){o.push([q[1],q[2],"N:"+q[0]])})})});return o})()');
  var fl=[];try{fl=window.FLAV[k]||[]}catch(e){}
  var svg;try{svg=window.__T('SCENES["'+k+'"]()')}catch(e){svg='<div style="color:red">'+e+'</div>'}
  return '<div style="width:720px;height:400px;position:relative;overflow:hidden">'+String(svg).replace('<svg ','<svg style="width:720px;height:400px" ')+'<svg viewBox="0 0 360 200" style="position:absolute;left:0;top:0;width:720px;height:400px">'+fl.map(f=>'<circle cx="'+f.x+'" cy="'+f.y+'" r="'+(f.r||18)+'" fill="#f0f" fill-opacity=".12" stroke="#f0f" stroke-width="1"/><text x="'+f.x+'" y="'+(f.y+2)+'" text-anchor="middle" font-size="7" fill="#fff" stroke="#000" stroke-width=".3">'+f.n+'</text>').join('')+pts.map(q=>'<circle cx="'+q[0]+'" cy="'+q[1]+'" r="3" fill="none" stroke="#0f0" stroke-width="1"/><text x="'+(q[0]+4)+'" y="'+q[1]+'" font-size="5" fill="#0f0">'+q[2]+'</text>').join('')+'</svg><span style="position:absolute;left:4px;top:2px;color:#fff;font:12px sans-serif;background:#000a">'+k+'</span></div>'}).join('')+'</div>'},keys);
await p.waitForTimeout(300);await p.locator('#g').screenshot({path:out});console.log('saved',out,'errors',errs);await b.close()})();
