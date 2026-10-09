# 1장 단계 잠금(햇빛 전 머리판·자물쇠, 자물쇠 전 장부, 장부 전 돋보기)을 힌트·'남은 곳'에서도 따른다
rep(' function prune(){var c=cur();',' window.__innAvail=avail;\n function prune(){var c=cur();')
rep('left=l.spots.filter(function(s){return G.found.indexOf(s.ev.id)<0&&!(s.uv&&!uvOn())}).length;','left=l.spots.filter(function(s){return G.found.indexOf(s.ev.id)<0&&!(s.uv&&!uvOn())&&(!window.__innAvail||!(G&&CASES[G.ci]&&CASES[G.ci].id==="inn")||window.__innAvail(s.ev.id))}).length;',4)
rep('var s=l.spots.filter(function(s){return !s.inZoom&&G.found.indexOf(s.ev.id)<0&&!(s.uv&&!uvOn())})[0];','var s=l.spots.filter(function(s){return !s.inZoom&&G.found.indexOf(s.ev.id)<0&&!(s.uv&&!uvOn())&&(!window.__innAvail||!(G&&CASES[G.ci]&&CASES[G.ci].id==="inn")||window.__innAvail(s.ev.id))})[0];')
# 장소 카드 '살펴볼 곳 N군데 남음': 잠긴 지점(햇빛 전 머리판·자물쇠, 자물쇠 전 장부, 장부 전 돋보기)은 세지 않는다
AV='(!window.__innAvail||!(G&&CASES[G.ci]&&CASES[G.ci].id==="inn")||window.__innAvail('
rep('var obsLeft=(l.obs||[]).filter(function(o){return o.zoom?','var obsLeft=(l.obs||[]).filter(function(o){if(!'+AV+'o.id)))return false;return o.zoom?')
rep('var lensLeft=l.spots.filter(function(s){return !s.inZoom&&!(s.uv&&!uvOn())&&G.found.indexOf(s.ev.id)<0}).length;','var lensLeft=l.spots.filter(function(s){return !s.inZoom&&!(s.uv&&!uvOn())&&G.found.indexOf(s.ev.id)<0&&'+AV+'s.ev.id))}).length;')
