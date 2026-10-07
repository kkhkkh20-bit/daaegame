(() => {
 'use strict';
 const $=id=>document.getElementById(id);let m,expression=0;
 function paint(){const id=$('person').value,c=m.characters[id];DaramArtKit.character($('daram'),'daram',expression);DaramArtKit.character($('other'),id,expression);$('other-name').textContent=c.name;$('description').textContent=c.design;for(const b of $('moods').children)b.setAttribute('aria-pressed',Number(b.dataset.mood)===expression);}
 DaramArtKit.ready.then(data=>{m=data;for(const id of m.order)$('person').add(new Option(m.characters[id].name,id));for(const [i,label] of ['기본','생각·의심','감정'].entries()){const b=document.createElement('button');b.textContent=label;b.dataset.mood=i;b.onclick=()=>{expression=i;paint()};$('moods').append(b)}const initial=new URLSearchParams(location.search).get('character');if(m.order.includes(initial))$('person').value=initial;$('person').onchange=paint;paint()}).catch(e=>{$('description').textContent='그림을 불러오지 못했습니다. 새로고침해 주세요.';console.error(e)});
})();
