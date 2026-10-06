/* Face/eye anchors measured in one frame of the existing sprite atlases.
   Keep apparent face size stable despite different canvas framing. */
(()=>{'use strict';
const profiles={daram:{aspect:960/(1639/3),face:.51,eye:.30},karo:{aspect:2,face:.52,eye:.17},mungchi:{aspect:2,face:.54,eye:.20}};
const pixelProfiles={daram:{aspect:2,face:.52,eye:.32},karo:{aspect:2,face:.58,eye:.235},mungchi:{aspect:2,face:.56,eye:.235}};
function layout(){const actor=document.getElementById('actor'),id=actor?.dataset.actor,p=(actor?.dataset.art==='pixel'?pixelProfiles:profiles)[id];if(!p||actor.hidden)return;
 if(document.getElementById('game').classList.contains('title-screen')){['width','height','left','right','top','bottom','aspect-ratio','clip-path'].forEach(k=>actor.style.removeProperty(k));return;}
 const game=document.getElementById('game').getBoundingClientRect(),scene=document.getElementById('scene').getBoundingClientRect(),panel=document.getElementById('panel').getBoundingClientRect(),header=document.querySelector('header').getBoundingClientRect();
 const wide=game.width>game.height&&game.height<550,areaWidth=wide?scene.width:game.width;
 let eyeY=Math.max(header.bottom-game.top+85,game.height*.36)+(id==='daram'?12:0);
 let width=Math.min(areaWidth*.38/p.face,areaWidth*.92,(eyeY-(header.bottom-game.top+10))/(p.eye*p.aspect));
 if(!wide){const ceiling=header.bottom-game.top+14,available=panel.top-game.top-ceiling; if(available>0)width=Math.min(width,available/(p.eye*p.aspect+p.face*.55));eyeY=Math.min(eyeY,panel.top-game.top-width*p.face*.55-8);}
 const height=width*p.aspect,top=eyeY-height*p.eye,left=(areaWidth-width)/2;
 // In portrait the sprite's cut edge must stay inside the dialogue window.
 const cropEnd=wide?game.height:panel.bottom-game.top-7,crop=Math.max(0,top+height-cropEnd);
 Object.assign(actor.style,{width:width+'px',height:height+'px',left:left+'px',right:'auto',top:top+'px',bottom:'auto',aspectRatio:'auto',clipPath:`inset(0 0 ${crop}px 0)`});
 actor.dataset.eyeY=String(eyeY);actor.dataset.faceWidth=String(width*p.face);actor.dataset.cropEnd=String(Math.min(top+height,cropEnd));
}
window.DaramPortraits={layout};window.addEventListener('resize',layout);
new ResizeObserver(layout).observe(document.getElementById('game'));
})();
