import sys
src=open(sys.argv[1],encoding='utf-8').read()
hook='window.__T=function(code){return eval(code)};\nfunction start(data){'
assert src.count('function start(data){')==1
src=src.replace('function start(data){',hook,1)
open(sys.argv[2],'w',encoding='utf-8').write(src)
