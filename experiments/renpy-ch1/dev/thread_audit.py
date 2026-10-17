"""0.19.17 단서 줄기 점검 (systems/room13_threads.rpy). 엔진을 한 번 띄워 덤프를 만든 뒤 규칙으로 검사한다.
   RENPY_SDK=... dev/run_renpy_tests.sh thread_audit_dump && python3 dev/thread_audit.py [--strict]
   보고: 줄기(steps)가 없는 사건 질문, 다시 묻기(again/recap)가 없는 질문, 관련 자료에 일반 답만 하는 인물."""
import json,os,sys,collections
p=os.path.join(os.environ.get("ROOM13_QA_OUT","/tmp/room13-qa"),"thread_audit.json")
d=json.load(open(p))
no_steps=[];no_again=[];generic=[]
for k,t in d["topics"].items():
    if t["special"] or k.startswith(("job:","shop:","home:","borrow:","return:")):continue
    life=k.startswith("life:") or ":life:" in k
    if not life and not (t["steps"] or t["timeless"]):no_steps.append(k)
    if not (t["again"] or t["recap"]):no_again.append(k)
for k,v in d["present"].items():
    if v["generic"]:generic.append(k)
by=collections.Counter(k.split("|")[0] for k in generic)
print("threads:",{n:len(s) for n,s in d["threads"].items()})
print("사건 질문 중 줄기 미지정 %d / 다시 묻기 없음 %d / 관련 자료에 일반 답 %d"%(len(no_steps),len(no_again),len(generic)))
print("일반 답 인물별:",dict(by.most_common()))
if "--list" in sys.argv:
    for name,rows in (("no_steps",no_steps),("no_again",no_again),("generic",generic)):
        print("\n## "+name);print("\n".join(sorted(rows)))
if "--strict" in sys.argv and (no_steps or no_again or generic):sys.exit(1)
