# 선택지 표시(350ms) 전에 대사를 빠르게 넘겨 필수 질문을 건너뛰는 것을 막는다.
rep(' /* 주민별 표: 자리 아래에 지금 누구에게 표를 두었는지, 바뀌면',
    ''' document.addEventListener("click",function(e){
  var next=e.target.closest&&e.target.closest('#rtnext,#rtgq,#rtgbar [data-g="next"]');if(!next)return;
  var L=Q?Q[QI]:curLine();if(!L||!L.ask||ANS.has(L))return;
  e.stopImmediatePropagation();e.preventDefault();askOpen(L);
 },true);
 /* 주민별 표: 자리 아래에 지금 누구에게 표를 두었는지, 바뀌면''')
rep('if(!b||!Q)return;e.stopImmediatePropagation();e.preventDefault();QI++;showQ()',
    'if(!b||!Q)return;e.stopImmediatePropagation();e.preventDefault();var L=Q[QI];if(L&&L.ask&&!ANS.has(L)){askOpen(L);return}QI++;showQ()')
