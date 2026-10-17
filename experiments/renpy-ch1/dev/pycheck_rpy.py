"""Compile the Python inside .rpy init blocks without starting Ren'Py (syntax only).
   python3 dev/pycheck_rpy.py game/systems/room13_threads.rpy ...   (exit 1 on a syntax error)"""
import re,sys,textwrap
bad=0
for path in sys.argv[1:]:
    lines=open(path,encoding="utf-8").read().split("\n")
    i=0
    while i<len(lines):
        m=re.match(r"^(\s*)(init\b[^:]*\bpython\b[^:]*|python\b[^:]*):\s*$",lines[i])
        if m:
            ind=len(m.group(1));j=i+1;body=[]
            while j<len(lines) and (not lines[j].strip() or len(lines[j])-len(lines[j].lstrip())>ind):
                body.append(lines[j]);j+=1
            src=textwrap.dedent("\n".join(body))
            try:compile(src,"%s:%d"%(path,i+2),"exec")
            except SyntaxError as e:
                bad=1;print("%s:%d: %s"%(path,i+1+(e.lineno or 0),e.msg))
            i=j
        else:i+=1
print("pycheck: %s"%("errors" if bad else "ok"));sys.exit(bad)
