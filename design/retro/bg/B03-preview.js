"use strict";
const controls=["markers","people","front"].map(id=>document.getElementById(id));
const loadImage=src=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=()=>reject(new Error("이미지 없음: "+src));im.src=src});
function crop(im){const w=im.naturalWidth,h=im.naturalHeight;return h>w*5/9?[0,(h-w*5/9)/2,w,w*5/9]:[(w-h*9/5)/2,0,h*9/5,h]}
let loaded=[];
function render(){for(const {a,c,bg,front,characters} of loaded){const x=c.getContext("2d");x.imageSmoothingEnabled=false;x.clearRect(0,0,360,200);x.drawImage(bg,...crop(bg),0,0,360,200);
if(controls[1].checked){for(const position of a.characterPositions){let pos=position;if(a.behindCounter&&position.id===a.behindCounter.id)pos=a.behindCounter;const asset=characters[pos.id];if(!asset)continue;const [sx,sy,sw,sh]=asset.crop,h=pos.height,w=sw*h/sh; x.drawImage(asset.im,sx,sy,sw,sh,pos.feet[0]-w/2,pos.feet[1]-h,w,h);}}
if(front&&controls[2].checked)x.drawImage(front,...crop(front),0,0,360,200);
if(controls[0].checked){for(const [i,t] of [...a.evidence,...a.observations].entries()){const [px,py]=t.point;const color=t.spotId?"#e86b76":"#80cbf0";x.fillStyle=color;x.strokeStyle="#132331";x.lineWidth=1;x.beginPath();x.arc(px,py,3,0,Math.PI*2);x.fill();x.stroke();x.font="bold 8px sans-serif";x.textAlign="center";x.fillStyle="#132331";x.fillRect(px-7,py-17,14,10);x.fillStyle=color;x.fillText(String(i+1),px,py-9);}
for(const pos of a.characterPositions){const [px,py]=pos.feet;x.strokeStyle="#a6dc83";x.beginPath();x.moveTo(px-4,py);x.lineTo(px+4,py);x.moveTo(px,py-4);x.lineTo(px,py+4);x.stroke();}}
}}
async function init(){const m=await fetch("B03-manifest.json").then(r=>{if(!r.ok)throw Error(r.status);return r.json()});const chars=m.previewCharacters;chars.karo={src:"../chars/karo.png",crop:[96,57,510,644]};const characters={};await Promise.all(Object.entries(chars).map(async([id,a])=>characters[id]={...a,im:await loadImage(a.src)}));
for(const a of m.assets){const article=document.createElement("article");const title=document.createElement("h2");title.textContent=a.name;article.append(title);const c=document.createElement("canvas");c.width=360;c.height=200;c.setAttribute("aria-label",a.name+" 배경과 조사 위치");article.append(c);const ul=document.createElement("ul");[...a.evidence,...a.observations].forEach((t,i)=>{const li=document.createElement("li");li.textContent=(i+1)+". "+t.name+" ("+t.point.join(",")+") · "+(t.spotId||t.id);ul.append(li)});article.append(ul);document.getElementById("scenes").append(article);loaded.push({a,c,bg:await loadImage(a.src),front:a.front?await loadImage(a.front):null,characters});}
controls.forEach(el=>el.addEventListener("change",render));render();window.B03_READY=true;window.B03_SCENE_COUNT=loaded.length;}
init().catch(e=>{document.getElementById("scenes").textContent=e.message;console.error(e)});
