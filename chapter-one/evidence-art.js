/* Original evIcon from game.html; see evidence-art-provenance.json. */
(()=>{
function evIcon(id){
 var o='stroke="#2A2F45" stroke-width="2.5"',g="";
 switch(id){
  case"hair":g='<path d="M8 28 q8 -16 16 -6 q6 8 10 -8" fill="none" stroke="#A89F90" stroke-width="5" stroke-linecap="round"/><path d="M8 28 q8 -16 16 -6 q6 8 10 -8" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>';break;
  case"uvw":case"uvc":case"uvs":case"uvb":case"uvd":g='<rect x="6" y="8" width="28" height="24" rx="3" fill="#2B1E5A" '+o+'/><path d="M12 22 q4 -10 8 0 q4 10 8 0" fill="none" stroke="#C9B4FF" stroke-width="3" stroke-linecap="round"/><circle cx="20" cy="13" r="2.5" fill="#9B7BFF"/>';break;
  case"anon":g='<path d="M9 9 L31 7 L30 33 L8 31 Z" fill="#FFFDF4" '+o+'/><path d="M13 15 H26 M13 20 H26 M13 25 H22" stroke="#8E97AD" stroke-width="2"/><path d="M6 12 l4 -3 M32 30 l-3 3" stroke="#2A2F45" stroke-width="2"/>';break;
  case"honey":g='<path d="M11 34 q-5 -14 3 -22 h12 q8 8 3 22 Z" fill="#F2B632" '+o+'/><rect x="12" y="8" width="16" height="6" rx="2" fill="#C98A2A" '+o+'/>';break;
  case"sill":g='<rect x="4" y="24" width="32" height="7" fill="#E9D2A8" '+o+'/><path d="M8 24 q8 -8 14 -2 q6 -6 12 0" fill="#FFFDF8" '+o+'/>';break;
  case"box":g='<rect x="8" y="16" width="24" height="18" fill="#F7C6D9" '+o+'/><path d="M20 16 V34" stroke="#E0567F" stroke-width="3"/><path d="M20 15 l-8 -6 v10 Z M20 15 l8 -6 v10 Z" fill="#F28DB2" '+o+'/>';break;
  case"tree":g='<path d="M20 12 l-8 4 l8 4 l8 -4 Z" fill="#4E9A3A" '+o+'/><path d="M20 20 q-9 2 -7 10 q3 6 7 6 q4 0 7 -6 q2 -8 -7 -10 Z" fill="#E0474C" '+o+'/>';break;
  case"invite":g='<rect x="6" y="11" width="28" height="19" fill="#FFFFFF" '+o+'/><path d="M6 11 l14 10 l14 -10" fill="none" '+o+'/><circle cx="29" cy="26" r="3" fill="#E0474C"/>';break;
  case"glass":g='<path d="M8 30 L16 10 L22 26 Z" fill="#CFE8F2" '+o+'/><path d="M22 32 L30 14 L34 30 Z" fill="#CFE8F2" '+o+'/>';break;
  case"foot":g=paw(20,26,8,"#5A402B");break;
  case"lace":g='<path d="M4 24 q6 -10 12 0 t12 0 t10 -4" fill="none" stroke="#E0474C" stroke-width="4" stroke-linecap="round"/>';break;
  case"kick":g='<circle cx="26" cy="20" r="9" fill="#FFFFFF" '+o+'/><path d="M26 15 l4 3 l-1.5 4.5 h-5 l-1.5 -4.5 Z" fill="#2A2F45"/><path d="M4 14 H14 M2 20 H14 M4 26 H14" stroke="#2A2F45" stroke-width="2.5" stroke-linecap="round"/>';break;
  case"ball":g='<circle cx="20" cy="20" r="13" fill="#FFFFFF" '+o+'/><path d="M20 13 l6 4.5 l-2.3 7 h-7.4 l-2.3 -7 Z" fill="#2A2F45"/>';break;
  case"owl":g=face("owl","#9A846E","").replace('<svg ','<svg x="0" y="0" width="40" height="40" style="width:40px;height:40px" ');break;
  case"clock":g='<circle cx="20" cy="20" r="14" fill="#FFFFFF" '+o+'/><path d="M20 20 V9 M20 20 L28 15" stroke="#2A2F45" stroke-width="2.5" stroke-linecap="round"/>';break;
  case"log":g='<path d="M4 12 l16 -4 l16 4 v20 l-16 -4 l-16 4 Z" fill="#FFFFFF" '+o+'/><path d="M20 8 V28" '+o+'/>';break;
  case"glitter":g=spark(14,16,8,"#E0B021")+spark(28,26,6,"#F2C94C")+spark(28,10,4,"#E0B021");break;
  case"roles":case"script":g='<rect x="9" y="5" width="22" height="30" fill="#FAF7EE" '+o+'/><path d="M13 13 H27 M13 19 H27 M13 25 H23" stroke="#8E97AD" stroke-width="2"/>'+(id==="roles"?'<circle cx="20" cy="6" r="3" fill="#E0474C"/>':'');break;
  case"rehearsal":g='<rect x="8" y="8" width="24" height="28" rx="2" fill="#C69A6E" '+o+'/><rect x="12" y="12" width="16" height="20" fill="#FFFFFF"/><rect x="15" y="5" width="10" height="6" rx="1" fill="#8E97AD" '+o+'/><path d="M14 18 l3 3 l6 -6" stroke="#23805F" stroke-width="2.5" fill="none"/>';break;
  case"feather":g='<path d="M8 34 q10 -24 26 -28 q-6 18 -26 28 Z" fill="#9A846E" '+o+'/><path d="M8 34 L32 8" stroke="#2A2F45" stroke-width="1.5"/>';break;
  case"crumbs":g='<circle cx="10" cy="28" r="4" fill="#FFF1E8" '+o+'/><circle cx="20" cy="22" r="3.5" fill="#FFF1E8" '+o+'/><circle cx="30" cy="15" r="3" fill="#FFF1E8" '+o+'/><path d="M26 30 h10 m-4 -4 l4 4 l-4 4" stroke="#2A2F45" stroke-width="2" fill="none"/>';break;
  case"latch":g='<rect x="6" y="8" width="28" height="24" fill="#9FD1E6" stroke="#7A5236" stroke-width="3"/><path d="M16 20 q6 -8 12 -1" fill="none" stroke="#2A2F45" stroke-width="3" stroke-linecap="round"/>';break;
  case"bell":g='<path d="M20 8 q-10 2 -10 16 h20 q0 -14 -10 -16 Z" fill="#FFD84D" '+o+'/><circle cx="20" cy="27" r="3" fill="#2A2F45"/><path d="M20 4 v4" '+o+'/>';break;
  case"carrots":g='<path d="M8 18 h24 l-4 16 h-16 Z" fill="#C98A4E" '+o+'/><path d="M13 18 l2 -10 M20 18 v-12 M27 18 l-2 -10" stroke="#F08A2E" stroke-width="4" stroke-linecap="round"/>';break;
  case"bottle":g='<rect x="13" y="10" width="14" height="26" rx="5" fill="#6FB7E8" '+o+'/><rect x="15" y="5" width="10" height="6" fill="#E0474C" '+o+'/>';break;
  case"seat":g='<path d="M4 14 l16 -5 l16 5 v18 l-16 -4 l-16 4 Z" fill="#FFD34E" '+o+'/><path d="M26 10 q6 -6 10 -4 q-4 4 -10 4 Z" fill="#FFE27A" stroke="#2A2F45" stroke-width="1.5"/>';break;
  case"pond":g='<path d="M8 26 q12 -24 24 0 Z" fill="#FFD34E" '+o+'/><path d="M20 6 v8" '+o+'/><path d="M6 32 h28" stroke="#6FB7E8" stroke-width="3"/>';break;
  case"hanky":g='<path d="M6 14 l22 -6 l6 20 l-22 6 Z" fill="#FFFFFF" '+o+'/><circle cx="20" cy="21" r="3.5" fill="#F28DB2"/><path d="M28 34 q2 3 5 0" stroke="#7EC8F0" stroke-width="2" fill="none"/>';break;
  case"earmuff":g='<path d="M9 24 q11 -24 22 0" fill="none" stroke="#E9853A" stroke-width="4"/><circle cx="9" cy="26" r="6" fill="#F28DB2" '+o+'/><circle cx="31" cy="26" r="6" fill="#F28DB2" '+o+'/>';break;
  case"bag":g='<path d="M8 34 q-2 -20 12 -22 q14 2 12 22 Z" fill="#9A846E" '+o+'/><path d="M11 22 h18" stroke="#E0B021" stroke-width="2" stroke-dasharray="3 2"/>'+spark(30,10,5,"#FFD84D");break;
  case"order":g='<rect x="7" y="5" width="26" height="30" fill="#FAF7EE" '+o+'/><path d="M11 13 H29 M11 19 H29 M11 25 H23" stroke="#8E97AD" stroke-width="2"/><circle cx="20" cy="6" r="3" fill="#E0474C"/>';break;
  default:g='<circle cx="20" cy="20" r="12" fill="#FFD84D" '+o+'/>';
 }
 return '<svg class="evic" viewBox="0 0 40 40" aria-hidden="true">'+g+'</svg>';
}
const crops={envelope:['room-archive',.19,.595,.17,.16,1.5],roster:['room-archive',.405,.56,.17,.2,1.5],report:['room-archive',.605,.59,.305,.19,1.5],receipt:['reception-pixel',.072,.465,.16,.16,1.5],tray:['reception-pixel',.465,.495,.2,.15,1.5],clock:['room-lounge',.455,.09,.15,.23,1.5],cabinet:['room-office',.595,.125,.25,.6,1.5],t_paid:['karo',.1,.08,.17,.29,1.5],key:['mungchi',.837,.448,.065,.125,1.5]};
const icons={envelope:'invite',roster:'roles',report:'script'};
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
 const svg=symbols[id]?'<svg viewBox="0 0 40 40" aria-hidden="true" stroke="#2A2F45" stroke-width="2">'+symbols[id]+'</svg>':evIcon(({receipt:'order',clock:'clock',envelope:'invite',roster:'roles',report:'script'})[id]||'anon');
 return '<span class="original-evidence-icon" role="img" aria-label="'+escape(title)+'">'+svg+'</span>';
}
window.DaramEvidenceArt={thumb(id,title){return `<span class="record-thumb">${recordIcon(id,title)}</span>`;},html(id,title){return `<figure class="evidence-art" data-art="${escape(id)}">${visual(id,title)}<figcaption>${crops[id]?'조사한 부분':pairs[id]?'함께 비교한 자료':'증거 그림'}</figcaption></figure>`;}};

})();
