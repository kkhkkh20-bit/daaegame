const namespace='http://www.w3.org/2000/svg';
const gallery=document.getElementById('gallery');
document.getElementById('surface').addEventListener('change',event=>{gallery.dataset.surface=event.target.value;});
async function render(){
  const response=await fetch('manifest.json');if(!response.ok)throw new Error('manifest');
  const manifest=await response.json();
  for(const item of manifest.items){
    const card=document.createElement('section');card.className='card';
    const asset=document.createElement('div');asset.className='asset';
    const svg=document.createElementNS(namespace,'svg');const [left,top,right,bottom]=item.visibleBounds;
    svg.setAttribute('viewBox',[left,top,right-left,bottom-top].join(' '));svg.setAttribute('role','img');svg.setAttribute('aria-label',item.label);svg.setAttribute('preserveAspectRatio','xMidYMid meet');
    const image=document.createElementNS(namespace,'image');image.setAttribute('href',item.src);image.setAttribute('width',item.size[0]);image.setAttribute('height',item.size[1]);svg.append(image);asset.append(svg);
    const caption=document.createElement('div');caption.className='caption';const title=document.createElement('h2');title.textContent=item.label;const download=document.createElement('a');download.href=item.src;download.download=item.src;download.textContent='PNG 받기 ↓';caption.append(title,download);card.append(asset,caption);gallery.append(card);
  }
  document.getElementById('load-status').textContent=manifest.count+'개 · 개별 투명 PNG';
}
render().catch(()=>{document.getElementById('load-status').textContent='그림 목록을 불러오지 못했습니다. 페이지를 새로고침해 주세요.';});
