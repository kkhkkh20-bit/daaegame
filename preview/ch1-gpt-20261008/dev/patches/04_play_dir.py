# 순서 진행기(play)에 연출 지시 {dir:{...}} 추가: 글자 없이 화면 상대·효과음을 바꾸고 잠깐 멈춘다
rep('   if(it.beat){setb(it.beat);step();return}','   if(it.dir){try{window.__innDir&&window.__innDir(it.dir)}catch(e){}setTimeout(step,it.dir.ms!=null?it.dir.ms:420);return}\n   if(it.beat){setb(it.beat);step();return}')
