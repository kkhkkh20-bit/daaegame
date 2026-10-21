"""Refresh only the source_line metadata of the 2026-10-21 intake cues.

Editing game/room13_v111_days123.rpy shifts line numbers. The cues match by
record ID at runtime (room13_v111_newworld_text.rpy), so only this recorded
location goes stale. Every other field must stay identical.
    python3 dev/refresh_intake21_lines.py
"""
import json
from import_resource_intake21 import reviewed_bindings, BATCH, ROOT

def strip(c):return {k:v for k,v in c.items() if k!='source_line'}

def refresh(path,key):
    data=json.loads(path.read_text());new=iter(reviewed_bindings());changed=0;out=[]
    for c in data[key]:
        if key=='bindings' and c.get('batch')!=BATCH:out.append(c);continue
        n=next(new)
        assert strip(c)==strip(n),(c,n)
        changed+=c.get('source_line')!=n.get('source_line');out.append(n)
    data[key]=out;path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    return changed

if __name__=='__main__':
    a=refresh(ROOT/'game/assets/room13-dialogue-context-art.json','bindings')
    b=refresh(ROOT/'docs/reviews'/BATCH/'receipt.json','bindings')
    print('source_line updated',a,b)
