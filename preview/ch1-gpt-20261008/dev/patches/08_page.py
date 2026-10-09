# 대사 쪽 나누기: 엔진 say 입구에서 1장 줄을 문장 단위 쪽·두 줄로 바꾼다(inn_stage.js의 __innPage)
rep('function say(lines,done,skippable){\n  if(DL&&!document.getElementById("dlgveil")){clearInterval(DL.timer);DL=null}',
    'function say(lines,done,skippable){\n  if(window.__innPage){try{lines=window.__innPage(lines)}catch(e){}}\n  if(DL&&!document.getElementById("dlgveil")){clearInterval(DL.timer);DL=null}')
