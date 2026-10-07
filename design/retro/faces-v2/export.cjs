// Technical export only: crop fixed atlas cells, shrink and clean alpha. No redrawing.
const fs=require('fs'),path=require('path'),cp=require('child_process'),crypto=require('crypto');
const root=path.resolve(__dirname,'../../..');
const roster=JSON.parse(fs.readFileSync(path.join(__dirname,'roster.json')));
for(const key of ['teacher','librarian']) if(!roster.some(r=>r.key===key)) roster.push({key,src:'design/retro/daram-face/neutral.png',costume: key==='teacher'?'bear, gold glasses, cream shirt, maroon vest and tie':'grey cat, gold glasses, navy cloak, cream blouse, green bow'});
const out=path.join(root,'art/faces-v2');fs.mkdirSync(out,{recursive:true});
const entries=[];
for(const r of roster){
 const source=path.join(__dirname,r.key+'.png');
 if(!fs.existsSync(source))throw Error('Missing atlas: '+r.key);
 const [w,h]=cp.execFileSync('identify',['-format','%w %h',source],{encoding:'utf8'}).trim().split(' ').map(Number);
 const six=['teacher','librarian'].includes(r.key), rows=six?3:2;
 const states=six?['neutral','think','happy','nervous','shock','angry']:['happy','nervous','shock',r.key==='grandma'?'sad':'angry'];
 const exports=[];
 for(let i=0;i<states.length;i++){
  const col=i%2,row=Math.floor(i/2),x=Math.round(col*w/2),y=Math.round(row*h/rows);
  const cw=Math.round((col+1)*w/2)-x,ch=Math.round((row+1)*h/rows)-y;
  const dest=path.join(out,`${r.key}-${states[i]}.png`);
  cp.execFileSync('convert',[source,'-crop',`${cw}x${ch}+${x}+${y}`,'+repage','-filter','Box','-resize','192x192!','-channel','A','-threshold','50%','+channel','-dither','None','-colors','48','-strip','PNG32:'+dest]);
  exports.push({mood:states[i],crop:[x,y,cw,ch],path:path.relative(root,dest),sha256:crypto.createHash('sha256').update(fs.readFileSync(dest)).digest('hex')});
 }
 entries.push({...r,atlas:path.relative(root,source),size:[w,h],sha256:crypto.createHash('sha256').update(fs.readFileSync(source)).digest('hex'),exports});
}
const manifest={version:'expressions2',sourceCommit:'38d4a4df9f1833c8dd62e84db7988bbc57b60f55',status:'ready-for-review',userApproved:false,browserPlaytest:false,strictRasterCompliant:false,notes:'AI-created pixel-style atlases, fixed cells, no independent face trimming. Original approved portraits retained. Grandma anger maps to nervous; shadow identity stays concealed.',entries};
fs.writeFileSync(path.join(__dirname,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
console.log(JSON.stringify({characters:entries.length,images:entries.reduce((n,r)=>n+r.exports.length,0)}));
