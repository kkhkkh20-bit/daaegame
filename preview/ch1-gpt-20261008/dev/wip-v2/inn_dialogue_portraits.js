/* Separate world/full-body and close dialogue drawings share one authored
   character identity. Immutable raw atlases are clipped at source coordinates.
   Father remains the first-person player: his bust supplies the speaker tile. */
(function(){
 var NS='http://www.w3.org/2000/svg',manifest=window.__innDialogueManifest||{},chars=manifest.characters||{},world=manifest.world||{},assets={},markupCache={},serial=0;
 function node(tag,attrs){var n=document.createElementNS(NS,tag);Object.keys(attrs||{}).forEach(function(k){n.setAttribute(k,attrs[k])});return n}
 function state(k,m){var s=String(m||'').split(/\s+/)[0];
  if(k==='wanggu'&&window.__innNeoState){if(/^(think|memo)$/.test(s))return 'thinking';if(/^(sad|worried|nervous|shock|panic)$/.test(s))return 'distressed';var n=window.__innNeoState(m,'');return {default:'neutral',admonish:'thinking',sheepish:'distressed',angry:'expressive'}[n]||'neutral'}
  if(/^(sad|worried|cower|nervous|panic|shock|surprise|oops|shy|caught|sheepish|sweat)$/.test(s))return 'distressed';
  if(/^(angry|mad|confront|pout|held|held-anger)$/.test(s))return /^(seryeon|karo)$/.test(k)?'expressive':'thinking';
  if(/^(think|memo|resolve|claim|admonish|focus)$/.test(s))return 'thinking';
  if(/^(smile|laugh|joy|happy)$/.test(s))return /^(seryeon|karo|wanggu)$/.test(k)?'neutral':'expressive';
  return 'neutral';
 }
 function art(k,m){var a=chars[k]&&chars[k][state(k,m)];return a&&assets[a.src]&&assets[a.src].ready?a:null}
 window.__innDialogueArt=art;
 window.__innDialogueArtReady=function(src){return !!(assets[src]&&assets[src].ready)};
 window.__innDialogueFace=function(k,m){var a=chars[k]&&chars[k][state(k,m)];return a&&assets[a.src]&&!assets[a.src].failed?{src:a.src,w:a.width,h:a.height,x:a.face[0],y:a.face[1],size:a.face[2]}:null};
 // The notebook, residents list and council use the same face as dialogue.
 // An explicit source clip prevents a neighbouring atlas cell in letterboxing.
 function markup(k,m,figure){var a=art(k,m);if(!a)return null;var key=k+'|'+state(k,m)+'|'+!!figure;if(figure&&markupCache[key])return markupCache[key];
  var c=figure?a.crop:[a.face[0],a.face[1],a.face[2],a.face[2]],id='cast-crop-'+(++serial),cls=figure?'sf innpixel inn-council-cast':'nodot inn-pixel-face';
  var result='<svg class="'+cls+'" data-face="'+k+'" data-k="'+k+'" data-expression="'+state(k,m)+'" data-src="'+a.src+'" viewBox="'+c.join(' ')+'" preserveAspectRatio="xMidYMid meet" aria-hidden="true" style="image-rendering:pixelated;overflow:hidden"><defs><clipPath id="'+id+'" clipPathUnits="userSpaceOnUse"><rect x="'+c[0]+'" y="'+c[1]+'" width="'+c[2]+'" height="'+c[3]+'"/></clipPath></defs><image clip-path="url(#'+id+')" href="'+a.src+'" width="'+a.width+'" height="'+a.height+'" style="image-rendering:pixelated"/></svg>';
  if(figure)markupCache[key]=result;return result;
 }
 window.__innCouncilCast=function(k,m){return markup(k,m,true)};
 try{var originalFace=pf;pf=function(k,m){try{if(G&&CASES[G.ci].id==='inn'){var face=markup(k,m,false);if(face)return face}}catch(e){}return originalFace.apply(this,arguments)}}catch(e){}
 function frame(k,a,opt){var W=innerWidth,H=innerHeight,c=a.crop,portrait=H>W*1.15,x0=12,x1=W-12;
  var topSafe=portrait?116:52,plate=document.querySelector('#vnbox .vtxt'),pr=plate&&plate.getBoundingClientRect();
  var floor=pr&&pr.height>10?pr.top+35:H-65;
  if(opt&&opt.surface==='talk'){floor=H-4;var panel=opt.panel;if(panel&&panel.width>0&&panel.left>W*.3)x1=panel.left-18}
  var height=Math.min(Math.max(160,floor-topSafe),H*.87,430),scale=Math.min(height/c[3],(x1-x0)/c[2]);
  var h=c[3]*scale,w=c[2]*scale;
  // Inverted Bami starts at the top beam rather than the ground line.
  var top=k==='geokkuri'?Math.max(0,topSafe-30):Math.max(topSafe,floor-h);
  return {left:Math.round((x0+x1-w)/2),top:Math.round(top),width:Math.round(w),height:Math.round(h)};
 }
 window.__innPaintDialogue=function(host,k,m,opt){var a=art(k,m),planned=chars[k]&&chars[k][state(k,m)];if(!host||!planned)return false;
  if(!a){var loading=assets[planned.src];if(!loading||loading.failed)return false;
   // A cold Continue can open questions before decoding finishes. Reserve the
   // close-up surface instead of flashing the room's full-body sprite first.
   if(host.children.length)host.replaceChildren();host.dataset.k=k;host.dataset.mood=String(m||'').split(/\s+/)[0];host.dataset.dialogueLoading='1';return true;
  }
  delete host.dataset.dialogueLoading;
  var c=a.crop,key=k+'|'+state(k,m)+'|'+a.src+'|'+c.join(','),svg=host.querySelector(':scope>svg.dialogue-bust');
  if(!svg){Array.from(host.children).forEach(function(n){n.remove()});svg=node('svg',{class:'dialogue-bust','aria-hidden':'true',preserveAspectRatio:'xMidYMid meet'});
   var id='dialogue-crop-'+(++serial),defs=node('defs'),clip=node('clipPath',{id:id,clipPathUnits:'userSpaceOnUse'}),rect=node('rect');clip.appendChild(rect);defs.appendChild(clip);svg.appendChild(defs);
   var im=node('image',{'clip-path':'url(#'+id+')'});svg.appendChild(im);svg.__rect=rect;svg.__image=im;host.appendChild(svg);
  }
  if(svg.dataset.art!==key){svg.dataset.art=key;svg.dataset.k=k;svg.dataset.src=a.src;svg.dataset.expression=state(k,m);svg.setAttribute('viewBox',c.join(' '));
   ['x','y','width','height'].forEach(function(n,i){svg.__rect.setAttribute(n,c[i])});svg.__image.setAttribute('href',a.src);svg.__image.setAttribute('width',a.width);svg.__image.setAttribute('height',a.height);
  }
  host.dataset.k=k;host.dataset.mood=String(m||'').split(/\s+/)[0];host.dataset.posture=k==='geokkuri'?'dialogue-hanging':'dialogue-bust';
  var f=frame(k,a,opt),geo=[f.left,f.top,f.width,f.height].join('|');
  if(host.dataset.dialogueFrame!==geo){host.dataset.dialogueFrame=geo;Object.keys({position:1,left:1,top:1,width:1,height:1,right:1,transform:1}).forEach(function(n){var v=n==='position'?'absolute':n==='right'?'auto':n==='transform'?'none':f[n]+'px';host.style.setProperty(n,v,'important')})}
  return true;
 };
 var drawings=[];Object.keys(chars).forEach(function(k){drawings=drawings.concat(Object.values(chars[k]))});drawings=drawings.concat(Object.values(world));
 drawings.forEach(function(a){if(assets[a.src])return;var entry=assets[a.src]={ready:false},im=entry.image=new Image();
  function refresh(){requestAnimationFrame(function(){if(window.__innRefreshDialogueStage)window.__innRefreshDialogueStage();document.dispatchEvent(new Event('inn-dialogue-art-ready'))})}
  im.onerror=function(){entry.failed=true;refresh()};im.onload=function(){Promise.resolve(im.decode?im.decode():null).catch(function(){}).then(function(){if(!im.naturalWidth)return;entry.ready=true;refresh()})};im.src=a.src;
 });
 window.__innDialogueState=function(){return {version:manifest.id,characters:Object.keys(chars),world:Object.keys(world),assets:Object.keys(assets).map(function(s){return {src:s,ready:assets[s].ready,failed:!!assets[s].failed}}),actors:Array.from(document.querySelectorAll('svg.dialogue-bust')).map(function(n){return {k:n.dataset.k,expression:n.dataset.expression,src:n.dataset.src,surface:n.closest('.tfig')?'talk':'stage'}})}};
 var css=document.createElement('style');css.id='inn-dialogue-portraits-css';css.textContent='html body.inn1 #vnbox .spk9.loading{visibility:hidden}html body.inn1 .dialogue-bust{display:block;position:absolute;inset:0;width:100%!important;height:100%!important;max-width:none!important;max-height:none!important;overflow:hidden;image-rendering:pixelated;pointer-events:none}.dialogue-bust image{image-rendering:pixelated}html body.inn1 .isf:has(>.dialogue-bust),html body.inn1 .tfig:has(>.dialogue-bust){overflow:visible}'+
  'html body.inn1 #rtg .seat>svg.inn-council-cast{height:75%!important;top:15%!important;width:auto!important;max-width:100%;position:relative}'+
  'html body.inn1 #rtg .seat[data-k="innma"]>svg.inn-council-cast{height:90%!important;top:0!important}'+
  'html body.inn1 #rtg .seat[data-k="buri"]>svg.inn-council-cast,html body.inn1 #rtg .seat[data-k="det1"]>svg.inn-council-cast{height:65%!important;top:25%!important}'+
  'html body.inn1 #rtg .seat[data-k="geokkuri"]{top:max(0px,calc((100% - 100vh)/2))!important}'+
  'html body.inn1 #rtg .seat[data-k="geokkuri"]>svg.inn-council-cast{height:65%!important;top:0!important}';document.head.appendChild(css);
})();
