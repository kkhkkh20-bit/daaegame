# 질문 대사(ep1_inn의 say 확장)에서도 연출 지시(@dir)·근접 조사(@inspect)·첫 만남 속마음을 처리하도록 inn_stage에 넘긴다
rep('''  }}catch(e){MISS.push("say "+e.message)}
  return _say.call(this,lines,done,sk)}}catch(e){MISS.push("say")}''','''  }}catch(e){MISS.push("say "+e.message)}
  return window.__innSayX?window.__innSayX(_say,this,lines,done,sk):_say.call(this,lines,done,sk)}}catch(e){MISS.push("say")}''')
