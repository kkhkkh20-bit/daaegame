# Usage: python3 build_with.py <out.html> [extra.js ...]
# Inserts each extra JS file (wrapped as-is) before the final wiring line, then adds the test hook.
import sys
g=open('/home/claude/daae/game.html',encoding='utf-8').read()
K='CASES.forEach(function(c){var cf=CONFESS[c.id];'
assert g.count(K)==1
extra=''
for f in sys.argv[2:]:
    extra+='\n'+open(f,encoding='utf-8').read()+'\n'
g=g.replace(K,extra+K)
hook='window.__T=function(code){return eval(code)};\nfunction start(data){'
assert g.count('function start(data){')==1
g=g.replace('function start(data){',hook,1)
open(sys.argv[1],'w',encoding='utf-8').write(g)
print('built',sys.argv[1])
