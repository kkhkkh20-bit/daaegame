# Usage: python3 build_scenes.py <out.html> <scenes.js>  -- inserts a scene-override file right before the v64 blocks (after chapters), plus test hook
import sys
g=open('/home/claude/daae/game.html',encoding='utf-8').read()
M='// ================= v64: detective look ================='
assert g.count(M)==1
g=g.replace(M,'\n'+open(sys.argv[2],encoding='utf-8').read()+'\n'+M)
g=g.replace('function start(data){','window.__T=function(code){return eval(code)};\nfunction start(data){',1)
open(sys.argv[1],'w',encoding='utf-8').write(g);print('built',sys.argv[1])
