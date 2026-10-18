/* Shared, read-only original-ratio image viewer. Native dialog supplies focus trapping. */
(()=>{
 const dialog=document.createElement('dialog');dialog.className='image-viewer';dialog.setAttribute('aria-labelledby','image-viewer-title');
 dialog.innerHTML='<header><h2 id="image-viewer-title">이미지 크게 보기</h2><button type="button" data-close>닫기 ×</button></header><div class="viewer-tools"><button type="button" data-zoom>원본 크기</button><a data-original target="_blank" rel="noopener">원본 파일 열기 ↗</a><span>전체 화면 보기 · 확대 후 밀어서 살펴보세요</span></div><div class="viewer-stage"><img alt=""></div><p class="viewer-error" role="status"></p>';
 document.body.append(dialog);const img=dialog.querySelector('img'),stage=dialog.querySelector('.viewer-stage');let trigger=null,zoom=false,priorOverflow='';
 function fit(){zoom=false;img.style.width='';img.style.height='';stage.classList.remove('zoomed');dialog.querySelector('[data-zoom]').textContent='원본 크기';stage.scrollTo(0,0);}
 function show(url,title,fromHistory=false){
  if(!dialog.open){trigger=document.activeElement;priorOverflow=document.body.style.overflow;document.body.style.overflow='hidden';dialog.showModal();}
  fit();img.alt=title;img.src=url;dialog.querySelector('h2').textContent=title;dialog.querySelector('[data-original]').href=url;dialog.querySelector('.viewer-error').textContent='';dialog.querySelector('[data-close]').focus();
  if(!fromHistory)history.pushState({...history.state,resourceImage:{url,title}},'',location.pathname+location.search+location.hash);
 }
 function hide(){if(!dialog.open)return;dialog.close();document.body.style.overflow=priorOverflow;fit();if(trigger?.isConnected)trigger.focus({preventScroll:true});}
 function close(){if(history.state?.resourceImage)history.back();else hide();}
 dialog.querySelector('[data-close]').onclick=close;dialog.addEventListener('cancel',e=>{e.preventDefault();close();});
 dialog.querySelector('[data-zoom]').onclick=()=>{if(zoom){fit();return;}zoom=true;stage.classList.add('zoomed');img.style.width=img.naturalWidth+'px';img.style.height='auto';dialog.querySelector('[data-zoom]').textContent='화면에 맞추기';};
 dialog.addEventListener('keydown',e=>{if(e.key!=='Tab')return;const items=[...dialog.querySelectorAll('button:not([disabled]),a[href]')].filter(x=>x.getClientRects().length);const first=items[0],last=items.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}});
 img.onerror=()=>dialog.querySelector('.viewer-error').textContent='이미지를 불러오지 못했습니다. 원본 파일 경로와 연결 상태를 확인해 주세요.';
 dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)close();}});
 window.addEventListener('popstate',()=>{if(history.state?.resourceImage){const {url,title}=history.state.resourceImage;show(url,title,true);}else hide();});
 document.addEventListener('click',e=>{const el=e.target.closest('[data-image-url]');if(!el)return;e.preventDefault();show(el.dataset.imageUrl,el.dataset.imageTitle||'이미지 자료 · 원본 비율');});
 window.ResourceViewer={open:show,close,isOpen:()=>dialog.open};
})();
