/* Report loading failures instead of leaving an unresponsive mobile preview. */
(()=>{
 const status=document.getElementById('load-status'),retry=document.getElementById('retry-load');
 const controls=['start','continue'].map(id=>document.getElementById(id));
 let failed=false;
 const fail=()=>{failed=true;status.hidden=false;status.textContent='게임을 불러오지 못했어요. 인터넷 연결을 확인한 뒤 다시 열어 주세요.';retry.hidden=false;controls.forEach(b=>b.disabled=true);};
 window.chapterLoadError=fail;
 retry.onclick=()=>location.reload();
 window.addEventListener('error',e=>{if(e.filename&&/\/(audio|story|case-data|legacy-core|effects|portraits|evidence-art|game)\.js(?:\?|$)/.test(e.filename))fail();});
 const load=src=>new Promise((resolve,reject)=>{const img=new Image();img.onload=()=>resolve();img.onerror=reject;img.src=src;});
 window.chapterStartReady=async()=>{
  try{
   const bg=window.ART?.reception||'assets/reception.png';
   await Promise.all([load(bg),load(window.ART?.daram||'assets/daram.png'),document.fonts?Promise.all([document.fonts.load('16px DaramDot'),document.fonts.load('16px DaramDotBold')]).catch(()=>{}):Promise.resolve()]);
   if(failed)return;
   status.hidden=true;controls.forEach(b=>b.disabled=false);
   // Fetch the other actors while the introduction is being read.
   ['karo','mungchi','daram-extra','panorama'].forEach(id=>load(window.ART?.[id]||'assets/'+id+'.png').catch(()=>{}));
  }catch{fail();}
 };
})();
