(() => {
 const Native=window.AudioContext||window.webkitAudioContext;
 window.__gameAudio=[];
 const connect=AudioNode.prototype.connect;
 AudioNode.prototype.connect=function(dest,...args){
  const value=connect.call(this,dest,...args);
  if(this.context.__qaTap && dest===this.context.destination) connect.call(this,this.context.__qaTap,...args);
  return value;
 };
 if(Native){
  const Wrapped=new Proxy(Native,{construct(T,args){const ctx=new T(...args);ctx.__qaTap=ctx.createMediaStreamDestination();window.__gameAudio.push(ctx);return ctx;}});
  window.AudioContext=Wrapped;if(window.webkitAudioContext)window.webkitAudioContext=Wrapped;
 }
 window.__startGameCapture=()=>{
  const canvas=document.querySelector('canvas');const video=canvas.captureStream(30);
  const contexts=window.__gameAudio;
  const tracks=contexts.flatMap(c=>c.__qaTap.stream.getAudioTracks());
  const stream=new MediaStream([...video.getVideoTracks(),...tracks]);
  window.__qaAudioStates=contexts.map(c=>({state:c.state,sampleRate:c.sampleRate}));
  const rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:6000000,audioBitsPerSecond:128000});
  window.__qaChunks=[];rec.ondataavailable=e=>{if(e.data.size)window.__qaChunks.push(e.data)};window.__qaRecorder=rec;rec.start(1000);
  return {audioTracks:tracks.length,contexts:window.__qaAudioStates,width:canvas.width,height:canvas.height};
 };
 window.__stopGameCapture=()=>new Promise(resolve=>{const r=window.__qaRecorder;r.onstop=async()=>{const b=new Blob(window.__qaChunks,{type:r.mimeType});const a=new Uint8Array(await b.arrayBuffer());window.__qaCaptureBytes=a;resolve({bytes:a.length,mime:r.mimeType})};r.stop()});
 window.__gameCaptureChunk=(offset)=>{const a=window.__qaCaptureBytes.subarray(offset,offset+500000);let s='';for(let i=0;i<a.length;i++)s+=String.fromCharCode(a[i]);return btoa(s)};
})();
