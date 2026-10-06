const crops={receipt:['panorama',.072,.465,.16,.16,1.5],tray:['panorama',.465,.495,.2,.15,1.5],clock:['panorama',.563,.19,.085,.13,1.5],cabinet:['panorama',.66,.13,.18,.36,1.5],t_paid:['karo',.1,.08,.17,.29,1.5],key:['mungchi',.837,.448,.065,.125,1.5]};
const icons={envelope:'invite',roster:'roles',report:'script'};
const pairs={cx_reception_0:['receipt','t_paid'],cx_reception_1:['key','cabinet'],cx_reception_2:['roster','report']};
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function visual(id,title,mini=false){const c=crops[id];if(c){const [asset,x,y,w,h,ratio]=c,r=ratio*w/h;return `<span class="evidence-crop ${mini?'mini':''}" style="--art-ratio:${r};--art-width:${156*r}px"><img alt="${escape(title)}" src="${window.ART?.[asset]||'assets/'+asset+'.png'}" style="width:${100/w}%;height:${100/h}%;left:${-x/w*100}%;top:${-y/h*100}%" draggable="false"></span>`;}
 if(pairs[id])return '<span class="paired-evidence">'+pairs[id].map(x=>visual(x,'관련 자료',true)).join('<b aria-hidden="true">＋</b>')+'</span>';
 return `<span class="original-evidence-icon" role="img" aria-label="${escape(title)}">${evIcon(icons[id]||'anon')}</span>`;
}
window.DaramEvidenceArt={html(id,title){return `<figure class="evidence-art" data-art="${escape(id)}">${visual(id,title)}<figcaption>${crops[id]?'조사한 부분':pairs[id]?'함께 비교한 자료':'증거 그림'}</figcaption></figure>`;}};
