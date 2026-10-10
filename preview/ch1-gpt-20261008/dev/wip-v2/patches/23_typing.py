# 타이핑 호흡(2026-10-10): 쉼표 뒤 짧게, 문장 끝 조금 길게, 말줄임(…)은 점마다 조금씩, 말줄임 바로 앞 두 글자는 느리게(망설임).
# 공백·쉼은 무음. 첫 탭(advance)은 그대로 즉시 완성(타이머 해제 → 남은 쉼·소리 없음). 1장 밖은 그대로
rep('''  else DL.timer=setInterval(function(){
    DL.shown++;el.textContent=DL.full.slice(0,DL.shown);
    if(!DL.spoken&&DL.shown%2===0&&DL.full[DL.shown-1]!==" ")SFX.blip(l.side==="thought"?0:(VOICE[l.who]||0));''',
'''  else{var _inn=!!window.__innPace;DL.hold=0;DL.timer=setInterval(function(){
    if(_inn&&DL.hold>0){DL.hold--;return}
    DL.shown++;el.textContent=DL.full.slice(0,DL.shown);
    var _ch=DL.full[DL.shown-1];if(_inn){try{DL.hold=window.__innPace(DL.full,DL.shown)}catch(e){DL.hold=0}}
    if(!DL.spoken&&(_inn?(_ch&&!/[\\s.,?!…·~"'“”‘’()「」]/.test(_ch)):(DL.shown%2===0&&_ch!==" ")))SFX.blip(l.side==="thought"?0:(VOICE[l.who]||0));''')
rep('''    if(DL.shown>=DL.full.length){clearInterval(DL.timer);DL.timer=null;el.innerHTML=hl(DL.full)}
  },sp);
}''','''    if(DL.shown>=DL.full.length){clearInterval(DL.timer);DL.timer=null;el.innerHTML=hl(DL.full)}
  },sp)}
}''')
