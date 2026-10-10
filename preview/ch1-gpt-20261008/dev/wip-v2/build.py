# 미리보기 play.html 빌드: 164838b 기준본 + 패치 목록 + inn_stage.js 주입
import re,sys,os
from pathlib import Path
import subprocess
SOURCE = Path(__file__).resolve().parent
D = str(SOURCE) + os.sep
OUTPUT = SOURCE / 'build'
OUTPUT.mkdir(exist_ok=True)
# The immutable base stays in Git; no previous container's files are required.
repo = subprocess.check_output(['git', '-C', str(SOURCE), 'rev-parse', '--show-toplevel'], text=True).strip()
s = subprocess.check_output(['git', '-C', repo, 'show',
    '164838b:preview/ch1-gpt-20261008/play.html']).decode('utf-8')
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
s=s[:a]+open(D+'script_b.js',encoding='utf-8').read()+open(D+'gen/end_gen.js',encoding='utf-8').read()+s[b:]
for f in sorted(os.listdir(D+'patches')) if os.path.isdir(D+'patches') else []:
    exec(open(D+'patches/'+f,encoding='utf-8').read())
# 2) 프롤로그 대사본 교체(개별 만남 구도)
a=s.index(' EP.PRO=[\n');b=s.index(' /* ---- 장면 배경 ----',a)
s=s[:a]+open(D+'pro_new.js',encoding='utf-8').read()+s[b:]
rep(' EP.PRO[0].bg="carriage";EP.PRO[1].bg="plaza";EP.PRO[2].bg="reception";EP.PRO[3].bg="corridor";EP.PRO[5].bg="reception";EP.PRO[6].bg="room";EP.PRO[7].bg="corridor";',' /* 프롤로그 장면 배경은 EP.PRO의 B(배경, 상대, 장면)에서 지정 */')
# 3) 대화 무대 모듈: 엔진 클로저 안(첫 실행 직전)에 넣는다
js=open(D+'inn_stage.js',encoding='utf-8').read()+'\n'+open(D+'inn_audio.js',encoding='utf-8').read()+'\n'+open(D+'inn_input.js',encoding='utf-8').read()+'\n'+open(D+'inn_ui9.js',encoding='utf-8').read()+'\n'+open(D+'inn_polish.js',encoding='utf-8').read()+'\n'+open(D+'inn_reasoning.js',encoding='utf-8').read()
hk='CASES.forEach(function(c){var cf=CONFESS[c.id];c.contra.forEach(function(x){if(cf&&x.unlock===cf)x.unlock=null})});\n'
rep(hk,js+'\n'+hk)
out=str(OUTPUT / 'play_v2.html')   # 2026-10-10: 작업 중 v2는 공개 파일에 쓰지 않는다(배포는 dev/ 소스로 따로)
hook='CASES.forEach(function(c){var cf=CONFESS[c.id];c.contra.forEach(function(x){if(cf&&x.unlock===cf)x.unlock=null})});\n'
assert s.count(hook)==1
test_out = OUTPUT / 'playT.html'
open(test_out,'w',encoding='utf-8').write(s.replace(hook,hook+'window.__T=function(code){return eval(code)};\n'))
print('ok',len(s))
# 빌드 후 스크립트 문법 검사(괄호 하나 빠진 패치가 게임 전체를 멈추게 한 일이 있어 상시 확인)
chk=subprocess.run(['node','-e',"const s=require('fs').readFileSync(process.argv[1],'utf8');const re=/<script>([\\s\\S]*?)<\\/script>/g;let m,i=0,bad=0;while((m=re.exec(s))){i++;try{new Function(m[1])}catch(e){bad++;console.log('script',i,e.message)}}if(bad)process.exit(1)",str(test_out)],capture_output=True,text=True)
if chk.returncode!=0: sys.exit('문법 오류: '+chk.stdout)
print('syntax ok')
open(out,'w',encoding='utf-8').write(s)   # 문법 검사를 통과한 뒤에만 비공개 v2 빌드를 쓴다
print('written',out)
