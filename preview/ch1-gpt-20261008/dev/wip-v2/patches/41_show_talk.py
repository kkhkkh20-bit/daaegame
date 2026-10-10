# 2026-10-10 v2 사용자 "증거를 증인에게 제시하는 걸 일부러 없앤 거야?" → 다시 켠다(1장). 인물별 반응표 EP.SHOW, 일부 반응은 새 질문을 연다(beat)
#   공식 '모순 지목'은 원탁회의에만 둔다. 질문 조건: beat(먼저 생겨야 하는 상황), sets(물으면 생기는 상황)
rep('var o={id:t.id,q:t.q,a:t.rec};if(t.after)o.after=t.after;if(t.need)o.need=t.need;return o',
    'var o={id:t.id,q:t.q,a:t.rec};if(t.after)o.after=t.after;if(t.need)o.need=t.need;if(t.beat)o.beat=t.beat;return o')
rep('r=r.filter(function(t){return !t.need||has(t.need)});return r}',
    'r=r.filter(function(t){return (!t.need||has(t.need))&&(!t.beat||bt(t.beat))});return r}')
rep('var T=TALKBY[lines[1][5]],id=lines[1][5],out=[],marked=false;',
    'var T=TALKBY[lines[1][5]],id=lines[1][5],out=[],marked=false;if(T.sets){try{setb(T.sets)}catch(e){}}')
# 반응: 1장에서는 EP.SHOW 표를 먼저 본다
rep(' function react(c,k,id){\n',
    ' function react(c,k,id){\n  try{if(c&&c.id==="inn"&&window.__innShow){var X=window.__innShow(k,id);if(X)return X}}catch(e){}\n')
rep('flash("이걸 봐!",false,true).then(function(){say([["det","이거, 본 적 있어?"]].concat(react(c,k,id)),function(){render()})})',
    'flash("이걸 봐!",false,true).then(function(){say(((c&&c.id==="inn")?[["det0","이걸 보신 적 있습니까?"]]:[["det","이거, 본 적 있어?"]]).concat(react(c,k,id)),function(){render()})})')
rep("'.fstalk .showev{display:none!important}'+","'.fstalk .showev{display:none!important}body.inn1 .fstalk .showev{display:flex!important}'+")
