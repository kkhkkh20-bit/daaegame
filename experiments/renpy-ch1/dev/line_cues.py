"""Per-line acting cues stay attached to the dialogue they were written for (0.18.35).

The two cue files key each cue by scene identity + line index and only apply when the
speaker and the text are exactly the current line (room13_acting.rpy, room13_fullbody_dialogue.rpy).
A dialogue edit therefore silently drops the cue. This tool finds and repairs that.

  python3 dev/line_cues.py            # report cues that no longer match their line
  python3 dev/line_cues.py --reanchor # move each cue to the most similar line of the same
                                      # speaker in the same scene; drop cues with no match

Scenes are read statically: literal r13_lines([...],"identity") calls in game/**/*.rpy and
topic lines in room13-content.json. Identities built at runtime are left untouched.
"""
import ast,difflib,glob,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CUE_FILES={"fullbody":ROOT/"game/assets/room13-fullbody-line-emotions.json",
    "direction":ROOT/"game/assets/room13-line-direction.json"}

def _match_bracket(s,i):
    depth=0;j=i;quote=None
    while j<len(s):
        c=s[j]
        if quote:
            if c=="\\":j+=2;continue
            if c==quote:quote=None
        elif c in "\"'":quote=c
        elif c in "([{":depth+=1
        elif c in ")]}":
            depth-=1
            if depth==0:return j
        j+=1
    return -1

def scene_rows():
    rows={}
    content=json.loads((ROOT/"game/room13-content.json").read_text(encoding="utf-8"))
    for tid,topic in content.get("topics",{}).items():
        if isinstance(topic,dict) and topic.get("lines"):
            lines=[tuple(r) for r in topic["lines"]]
            rows["topic:"+tid]=lines;rows["topic:review:"+tid]=lines
    for path in sorted(glob.glob(str(ROOT/"game/**/*.rpy"),recursive=True)):
        if "qa_tests" in path:continue
        s=Path(path).read_text(encoding="utf-8")
        for m in re.finditer(r"r13_lines\(\s*\[",s):
            i=m.end()-1;j=_match_bracket(s,i)
            if j<0:continue
            ident=re.match(r'\s*,\s*"([^"]+)"\s*\)',s[j+1:j+300])
            if not ident:continue
            try:lines=ast.literal_eval(s[i:j+1])
            except Exception:continue
            rows.setdefault(ident.group(1),[tuple(r) for r in lines])
    return rows

def cues(kind):
    data=json.loads(CUE_FILES[kind].read_text(encoding="utf-8"))
    return data,(data["lines"] if kind=="fullbody" else data)

def stale(rows=None):
    """[(kind, identity, index, cue)] for cues whose scene is known but whose line changed."""
    rows=rows or scene_rows();out=[]
    for kind in CUE_FILES:
        _,table=cues(kind)
        for ident,entries in table.items():
            lines=rows.get(ident)
            if lines is None:continue
            for idx,cue in entries.items():
                i=int(idx)
                if not (i<len(lines) and lines[i][0]==cue["person"] and lines[i][1]==cue["text"]):
                    out.append((kind,ident,idx,cue))
    return out

def reanchor(threshold=.55):
    rows=scene_rows();report=[]
    for kind in CUE_FILES:
        data,table=cues(kind);new={}
        for ident,entries in table.items():
            lines=rows.get(ident)
            if lines is None:new[ident]=entries;continue
            for idx,cue in entries.items():
                i=int(idx);best=None
                for j,line in enumerate(lines):
                    if line[0]!=cue["person"]:continue
                    score=difflib.SequenceMatcher(None,cue["text"],line[1]).ratio()+(.15 if j==i else 0)
                    if not best or score>best[0]:best=(score,j,line[1])
                if best and (best[1]==i and best[2]==cue["text"] or best[0]>=threshold) and str(best[1]) not in new.get(ident,{}):
                    new.setdefault(ident,{})[str(best[1])]=dict(cue,text=best[2])
                else:
                    report.append(("dropped",kind,ident,idx,cue["person"],cue["text"]))
        if kind=="fullbody":data["lines"]=new
        else:data=new
        CUE_FILES[kind].write_text(json.dumps(data,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
    return report

if __name__=="__main__":
    if "--reanchor" in sys.argv:
        for row in reanchor():print(*row)
    left=stale()
    for kind,ident,idx,cue in left:print("stale",kind,ident,idx,cue["person"],cue["text"])
    print("stale cues:",len(left))
    sys.exit(1 if left else 0)
