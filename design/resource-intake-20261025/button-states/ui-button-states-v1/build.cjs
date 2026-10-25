const sharp=require('sharp');
const fs=require('fs');const path=require('path');
const root=__dirname;
const families=[{id:'primary',source:'b_button_primary.png',w:160,h:52,hit:{x:16,y:10,width:128,height:32},radius:9},{id:'standard',source:'b_button.png',w:160,h:52,hit:{x:16,y:10,width:128,height:32},radius:9},{id:'wide_choice',source:'b_panel_small.png',w:240,h:60,hit:{x:8,y:8,width:224,height:44},radius:12}];
const states=['basic','pressed','selected','disabled'];
(async()=>{const manifest={version:1,description:'Existing raster art, unchanged scale and proportions. UI-only visual state composition.',state_priority:['disabled','pressed','selected','basic'],families:[]};
for(const f of families){let p=path.join(root,'source',f.source);let original=fs.readFileSync(p);let assets={};for(const state of states){let out=path.join(root,'assets',f.id+'_'+state+'.png');if(state==='basic')fs.copyFileSync(p,out);
if(state==='pressed'){let layer=await sharp(original).extract({left:0,top:0,width:f.w,height:f.h-2}).toBuffer();await sharp({create:{width:f.w,height:f.h,channels:4,background:'#00000000'}}).composite([{input:layer,top:2,left:0}]).png().toFile(out);}
if(state==='selected'){let b=f.hit;let overlay=Buffer.from(`<svg width="${f.w}" height="${f.h}" xmlns="http://www.w3.org/2000/svg"><rect x="${b.x-3}" y="${b.y-3}" width="${b.width+6}" height="${b.height+6}" rx="${f.radius+2}" fill="none" stroke="#B83C36" stroke-width="2"/></svg>`);await sharp(original).composite([{input:overlay}]).png().toFile(out);}
if(state==='disabled'){let {data,info}=await sharp(original).raw().toBuffer({resolveWithObject:true});for(let i=3;i<data.length;i+=4)data[i]=Math.round(data[i]*0.45);await sharp(data,{raw:info}).png().toFile(out);}
assets[state]='assets/'+path.basename(out);}
manifest.families.push({id:f.id,source:'source/'+f.source,canvas:{width:f.w,height:f.h},hit_rect:f.hit,text_offset:{basic:[0,0],pressed:[0,2],selected:[0,0],disabled:[0,0]},assets});}
fs.writeFileSync(path.join(root,'manifest.json'),JSON.stringify(manifest,null,2));
const W=1175,H=470;let svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}"><rect width="100%" height="100%" fill="#FAF5E9"/><g font-family="sans-serif" fill="#25364A"><text x="30" y="42" font-size="24" font-weight="bold">UI BUTTON STATES · EXISTING ART</text><text x="30" y="69" font-size="14">Native size · same canvas / hit rectangle per family · no baked labels</text>`;
for(let i=0;i<4;i++)svg+=`<text x="${275+250*i}" y="114" text-anchor="middle" font-size="15" font-weight="bold">${states[i].toUpperCase()}</text>`;
for(let i=0;i<3;i++){let f=families[i];svg+=`<text x="30" y="${159+110*i}" font-size="15" font-weight="bold">${f.id.toUpperCase()}</text><text x="30" y="${182+110*i}" font-size="13">${f.w} × ${f.h} px</text>`;for(let j=0;j<4;j++){let x=155+250*j,y=132+110*i;svg+=`<rect x="${x}" y="${y}" width="240" height="82" rx="8" fill="#E7EBEF"/><rect x="${x+8}" y="${y+8}" width="224" height="66" fill="#FFFFFF"/>`;}}svg+='</g></svg>';
let layers=[];for(let i=0;i<3;i++)for(let j=0;j<4;j++){let f=families[i];layers.push({input:path.join(root,'assets',f.id+'_'+states[j]+'.png'),left:155+250*j+Math.round((240-f.w)/2),top:132+110*i+Math.round((82-f.h)/2)});}await sharp(Buffer.from(svg)).composite(layers).png().toFile(path.join(root,'preview.png'));
console.log('Generated 12 transparent state PNGs and preview.');})();
