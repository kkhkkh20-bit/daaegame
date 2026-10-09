# 미리보기 play.html 빌드: 164838b 기준본 + 패치 목록 + inn_stage.js 주입
import re,sys,os
D='/home/claude/daae/stage/'
s=open(D+'base_play.html',encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    n=s.count(old)
    if n!=cnt: sys.exit('패치 실패(%d회): %s'%(n,old[:80]))
    s=s.replace(old,new)
# 1) 프롤로그 관찰 지문 복구(무대 지문 stage는 dirList에서 이미 빠짐)
rep('EP.PRO.forEach(function(sc){sc.items=sc.items.filter(function(x){return !(Array.isArray(x)&&x[0]==="narr")})});',
    '/* 프롤로그: 무대 지문(stage)은 dirList에서 빠지고, 이야기에 필요한 관찰(obs)만 짧은 지문으로 남긴다(inn_stage). */')
# 1-1) 대본 전면 교체(증거·조사·질문 / 회의 직전~후일담)
a=s.index(' /* ---- 증거 C01~C13');b=s.index(' /* ---- 프롤로그 P1~P11 ---- */',a)
s=s[:a]+open(D+'script_a.js',encoding='utf-8').read()+s[b:]
a=s.index(' /* ---- I9 회의 직전 ---- */');b=s.index(' /* 대본·구현에서 아직 확정되지 않았거나',a)
s=s[:a]+open(D+'script_b.js',encoding='utf-8').read()+s[b:]
for f in sorted(os.listdir(D+'patches')) if os.path.isdir(D+'patches') else []:
    exec(open(D+'patches/'+f,encoding='utf-8').read())
# 2) 프롤로그 대사본 교체(개별 만남 구도)
a=s.index(' EP.PRO=[\n');b=s.index(' /* ---- 장면 배경 ----',a)
s=s[:a]+open(D+'pro_new.js',encoding='utf-8').read()+s[b:]
rep(' EP.PRO[0].bg="carriage";EP.PRO[1].bg="plaza";EP.PRO[2].bg="reception";EP.PRO[3].bg="corridor";EP.PRO[5].bg="reception";EP.PRO[6].bg="room";EP.PRO[7].bg="corridor";',' /* 프롤로그 장면 배경은 EP.PRO의 B(배경, 상대, 장면)에서 지정 */')
# 3) 대화 무대 모듈: 엔진 클로저 안(첫 실행 직전)에 넣는다
js=open(D+'inn_stage.js',encoding='utf-8').read()
hk='CASES.forEach(function(c){var cf=CONFESS[c.id];c.contra.forEach(function(x){if(cf&&x.unlock===cf)x.unlock=null})});\n'
rep(hk,js+'\n'+hk)
out='/home/claude/daaegame/preview/ch1-gpt-20261008/play.html'
open(out,'w',encoding='utf-8').write(s)
hook='CASES.forEach(function(c){var cf=CONFESS[c.id];c.contra.forEach(function(x){if(cf&&x.unlock===cf)x.unlock=null})});\n'
assert s.count(hook)==1
open('/tmp/claude-0/P/playT.html','w',encoding='utf-8').write(s.replace(hook,hook+'window.__T=function(code){return eval(code)};\n'))
print('ok',len(s))
