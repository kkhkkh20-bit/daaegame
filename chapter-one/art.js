/* Pixel play sprites; original illustrations stay available for art and loading fallback. */
(()=>{const ids=['daram','daram-extra','karo','mungchi','evidence'],ready=new Set();const source=id=>window.ART?.[id+'-pixel']||'assets/'+id+'-pixel.png';
window.DaramArt={has:id=>ready.has(id),source,ready:Promise.all(ids.map(id=>new Promise(resolve=>{const i=new Image();i.onload=()=>{ready.add(id);resolve()};i.onerror=resolve;i.src=source(id)})))};})();
