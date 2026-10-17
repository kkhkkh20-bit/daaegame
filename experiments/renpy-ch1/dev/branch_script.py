"""분기 대사본 만들기 (0.19.17). 장면(.rpy 라벨)은 조건 줄과 함께, 질문·증거 반응은 엔진 덤프(thread_audit.json)에서.
   RENPY_SDK=... dev/run_renpy_tests.sh thread_audit_dump && python3 dev/branch_script.py docs/dialogue_script
   만든 문서는 사람이 읽고 확인하는 용도다. 실행 기준은 game/이다."""
import json,os,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];G=ROOT/"game"
out=Path(sys.argv[1] if len(sys.argv)>1 else ROOT/"docs/dialogue_script");out.mkdir(parents=True,exist_ok=True)
dump=json.load(open(os.path.join(os.environ.get("ROOM13_QA_OUT","/tmp/room13-qa"),"thread_audit.json")))
N=dump.get("names",{});N.update({"dad":"아빠","None":"서술"})
def who(k):return N.get(k,k)
def cond(c):
    if c is None:return "항상"
    if isinstance(c,str):return c
    parts=[]
    if "thread" in c:parts.append("%s 줄기 %s~%s단계"%(c["thread"],c.get("min",0),c.get("max","끝")))
    if c.get("has"):parts.append("있음: "+", ".join(c["has"]))
    if c.get("not"):parts.append("없음: "+", ".join(c["not"]))
    if c.get("case"):parts.append("사건 "+c["case"])
    if c.get("all"):parts.append("모두("+" / ".join(cond(x) for x in c["all"])+")")
    if c.get("any"):parts.append("하나라도("+" / ".join(cond(x) for x in c["any"])+")")
    return " · ".join(parts) or "항상"
def lines(ls,ind="  "):
    return "\n".join("%s- **%s**%s %s"%(ind,who(a),"(생각)" if len(x)>2 else "",b) for x in ls for a,b in [x[:2]])
# ---- 1. 인물별 질문
by={}
for k,t in dump["script"].items():by.setdefault(t["npc"],[]).append((k,t))
doc=["# 질문 대사본 (인물별)\n","각 질문: 열리는 조건 → 처음 물을 때(상태별 갈래) → 다시 물을 때. 조건 이름은 깃발·기록 id다.\n"]
for npc in sorted(by,key=lambda n:who(n)):
    doc.append("\n## %s\n"%who(npc))
    for k,t in sorted(by[npc],key=lambda x:(x[1]["day"] or [0])[0]):
        lim=[]
        if t["day"]:lim.append("%s~%s일"%tuple(t["day"]))
        if t["need"]:lim.append("필요: "+", ".join(t["need"]))
        if t["not_flags"]:lim.append("없어야: "+", ".join(t["not_flags"]))
        if t["case"]:lim.append("사건 "+t["case"])
        if t["steps"]:lim.append("단계: "+cond(t["steps"]))
        doc.append("### %s `%s`\n- 열림: %s\n"%(t["title"],k," · ".join(lim) or "항상"))
        for c,ls in t["variants"]:doc.append("- 처음 · %s\n%s\n"%(cond(c),lines(ls)))
        doc.append("- 처음 · 기본\n%s\n"%lines(t["lines"]) if t["lines"] else "- 처음 · (장면으로 이어짐)\n")
        for c,ls in t["again"]:doc.append("- 다시 · %s\n%s\n"%(cond(c),lines(ls)))
        if t["recap"]:doc.append("- 다시 · 혼잣말: (%s)\n"%t["recap"])
(out/"01_questions.md").write_text("\n".join(doc))
# ---- 2. 증거 반응
doc=["# 증거 반응 대사본\n","관련 자료를 보여 줬을 때 일반 답 대신 나오는 반응. (인물 | 기록)\n"]
for key,rows in sorted(dump["reaction_script"].items()):
    p,e=key.split("|");doc.append("\n### %s ← %s\n"%(who(p),e))
    for c,ls in rows:doc.append("- %s\n%s\n"%(cond(c),lines(ls)))
(out/"02_reactions.md").write_text("\n".join(doc))
# ---- 3. 줄기 단계
doc=["# 단서 줄기 단계\n"]
for n,steps in dump["thread_steps"].items():
    doc.append("\n## %s\n| 단계 | 확인한 사실 | 다음 의문 |\n|---|---|---|"%n)
    for i,(sid,fact,q) in enumerate(steps,1):doc.append("| %d %s | %s | %s |"%(i,sid,fact,q))
(out/"00_threads.md").write_text("\n".join(doc))
# ---- 4. 장면 (정적으로: 라벨 · if/elif/else/menu 선택지 줄을 조건으로)
TUP=re.compile(r"""\(\s*(None|["']([\w]+)["'])\s*,\s*(["'])((?:\\.|(?!\3).)*)\3""")
INLINE=re.compile(r"\]\s*if\s+(.+?)\s+else\s*\[")
files=sorted(list(G.glob("*.rpy"))+list((G/"systems").glob("*.rpy")))
doc=["# 장면 대사본 (파일·라벨별)\n","들여쓰기로 조건을 묶었다. `if`/`elif`/`else`, 선택지(\"…\":), 줄 안 조건(… if 조건 else …)을 그대로 적는다.\n"]
for f in files:
    if "qa_tests" in str(f):continue
    src=f.read_text(encoding="utf-8").split("\n");body=[];stack=[];label=None
    for no,raw in enumerate(src,1):
        s=raw.strip();ind=len(raw)-len(raw.lstrip())
        if not s or s.startswith("#"):continue
        while stack and stack[-1][0]>=ind:stack.pop()
        m=re.match(r"label\s+([\w\.]+)",s)
        if m and ind==0:label=m.group(1);body.append("\n### %s  (`%s:%d`)\n"%(label,f.relative_to(G),no));stack=[];continue
        if label is None:continue
        m=re.match(r"(if|elif)\s+(.+):$",s) or re.match(r"(else):$",s) or re.match(r'''(")(.+)"\s*(?:if\s+(.+))?:$''',s)
        if m:
            if m.group(1)=='"':txt="선택지 “%s”"%m.group(2)+(" (조건 %s)"%m.group(3) if m.group(3) else "")
            elif m.group(1)=="else":txt="그 밖"
            else:txt="%s %s"%("조건" if m.group(1)=="if" else "아니면",m.group(2))
            stack.append((ind,txt));body.append("%s- %s"%("  "*(len(stack)-1),txt));continue
        if "r13_lines" in s or TUP.search(s):
            for c in INLINE.findall(s):body.append("%s- (줄 안 조건: %s)"%("  "*len(stack),c[:120]))
            for mm in TUP.finditer(s):
                w=mm.group(2) or "None";t=mm.group(4)
                if w not in N and w!="None":continue
                body.append("%s- **%s** %s"%("  "*len(stack),who(w),t))
    # 대사가 하나도 없는 조건 줄·라벨은 뺀다.
    keep=[];has=False
    for b in reversed(body):
        if b.startswith("\n###"):
            if has:keep.append(b)
            has=False;continue
        dlg="**" in b
        if dlg:has=True;keep.append(b);continue
        depth=len(b)-len(b.lstrip())
        if keep and not keep[-1].startswith("\n###") and len(keep[-1])-len(keep[-1].lstrip())>depth:keep.append(b)
    body=list(reversed(keep))
    if body:
        doc.append("\n## %s\n"%f.relative_to(G));doc+=body
(out/"03_scenes.md").write_text("\n".join(doc))
print("written:",[p.name for p in sorted(out.iterdir())])
