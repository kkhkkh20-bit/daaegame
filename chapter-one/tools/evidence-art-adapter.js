const crops={envelope:['room-archive',.19,.595,.17,.16,1.5],roster:['room-archive',.405,.56,.17,.2,1.5],report:['room-archive',.605,.59,.305,.19,1.5],receipt:['panorama',.072,.465,.16,.16,1.5],tray:['panorama',.465,.495,.2,.15,1.5],clock:['room-lounge',.455,.09,.15,.23,1.5],cabinet:['room-office',.595,.125,.25,.6,1.5],t_paid:['karo',.1,.08,.17,.29,1.5],key:['mungchi',.837,.448,.065,.125,1.5]};
const icons={envelope:'invite',roster:'roles',report:'script',locknote:'script'};
const pairs={cx_reception_0:['receipt','t_paid'],cx_reception_1:['key','cabinet'],cx_reception_2:['roster','report']};
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function visual(id,title,mini=false){const c=crops[id];if(c){const [asset,x,y,w,h,ratio]=c,r=ratio*w/h;return `<span class="evidence-crop ${mini?'mini':''}" style="--art-ratio:${r};--art-width:${156*r}px"><img alt="${escape(title)}" src="${window.ART?.[asset]||'assets/'+asset+'.png'}" style="width:${100/w}%;height:${100/h}%;left:${-x/w*100}%;top:${-y/h*100}%" draggable="false"></span>`;}
 if(pairs[id])return '<span class="paired-evidence">'+pairs[id].map(x=>visual(x,'관련 자료',true)).join('<b aria-hidden="true">＋</b>')+'</span>';
 return `<span class="original-evidence-icon" role="img" aria-label="${escape(title)}">${evIcon(icons[id]||'anon')}</span>`;
}
function recordIcon(id,title){
 const cells={receipt:0,tray:1,clock:2,cabinet:3,key:4,envelope:5,roster:6,report:7};
 if(window.DaramArt?.has('evidence')&&cells[id]!==undefined){const c=cells[id];return `<span class="pixel-evidence" role="img" aria-label="${escape(title)}" style="background-image:url(${DaramArt.source('evidence')});background-position:${c%3*50}% ${Math.floor(c/3)*50}%"></span>`;}

 const symbols={tray:'<path d="M4 14h32v18H4z" fill="#B5814A"/><path d="M4 14l6-7h20l6 7-6 8H10z" fill="#EDD5A5"/><path d="M10 12h20v7H10z" fill="#765035"/>',cabinet:'<path d="M7 4h26v33H7z" fill="#B5814A"/><path d="M11 8h18v25H11z" fill="#EDD5A5"/><path d="M23 19h4v7h-4z" fill="#475369"/>',key:'<path d="M13 4h12v12H13z M17 16h4v20h-4z M21 26h7v4h-7z M21 33h7v3h-7z" fill="#E8B84A"/><path d="M17 8h4v4h-4z" fill="#fff8e5"/>'};
 if(pairs[id])return '<span class="paired-evidence">'+pairs[id].map(x=>recordIcon(x,'관련 자료')).join('<b>＋</b>')+'</span>';
 if(id==='t_paid')return visual(id,title,true);
 const svg=symbols[id]?'<svg viewBox="0 0 40 40" aria-hidden="true" stroke="#2A2F45" stroke-width="2">'+symbols[id]+'</svg>':evIcon(({receipt:'order',clock:'clock',envelope:'invite',roster:'roles',report:'script',locknote:'script'})[id]||'anon');
 return '<span class="original-evidence-icon" role="img" aria-label="'+escape(title)+'">'+svg+'</span>';
}
window.DaramEvidenceArt={thumb(id,title){return `<span class="record-thumb">${recordIcon(id,title)}</span>`;},html(id,title){return `<figure class="evidence-art" data-art="${escape(id)}">${visual(id,title)}<figcaption>${crops[id]?'조사한 부분':pairs[id]?'함께 비교한 자료':'증거 그림'}</figcaption></figure>`;}};
