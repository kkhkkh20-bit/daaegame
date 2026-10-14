"""Host state matrix: optional routines move; story locations and emergency routes do not."""
import ast,copy,json,textwrap
from pathlib import Path
from qa_room13_rules import load_rules,ROOT
n=load_rules();s=n['store'];res=n['ROOM13']['residents'];n['R13_RESIDENTS']=res
src=(ROOT/'game/room13_life.rpy').read_text();start=src.index('    R13_WEEKLY_ROUTINES =');end=src.index('    def r13_activity_text',start)
block=textwrap.dedent(src[start:end]);exec(compile(block,'room13_life.rpy','exec'),n)
new=n['r13_resident_where'];oldns=dict(n);oldblock=block.replace('R13_WEEKLY_ROUTINES.get(person,R13_RESIDENTS[person]["weekly_locations"])','R13_RESIDENTS[person]["weekly_locations"]');exec(compile(oldblock,'old-routine-baseline','exec'),oldns);old=oldns['r13_resident_where']
people=set(n['R13_GREETING'])|set(res)|{'mom'};optional=set(n['R13_WEEKLY_ROUTINES']);changed=[];visible=set();cases=0;maxima={};base=copy.deepcopy(s.room13)
for day in range(1,15):
 for period in range(4):
  for victim,granny,flags in [('alive','trusted',[]),('dead','detained',[]),('alive','trusted',['mom_reunited','shelter_ready','patient_transport','nubi_protected','bami_protected'])]:
   s.room13=copy.deepcopy(base);s.room13.update(day=day,period=period,victim_state=victim,granny_state=granny,case_state='occurred' if victim=='dead'else'prevented',flags=flags)
   before=copy.deepcopy(s.room13);n['r13_resident_where']=old;original={p:n['r13_where'](p) for p in people};n['r13_resident_where']=new;actual={p:n['r13_where'](p) for p in people}
   assert s.room13==before,'Schedule reads mutated story state'
   for p in people:
    if original[p]!=actual[p]:
     assert p in optional,(p,day,period,original[p],actual[p]);changed.append((p,day,period,original[p],actual[p]))
    if actual[p]:visible.add(p)
   if day>=8:assert actual['resident_piko']=='clinic'
   if day>=11 and 'shelter_ready'in flags:
    for p in ('resident_tori','resident_yeoni','resident_kongi','resident_somi','resident_musoe'):assert actual[p]=='school'
   if victim=='dead':assert actual['resident_owlgp']is None
   if granny=='detained':assert actual['granny']is None
   if period==3:
    s.room13['period']=2;assert actual=={p:n['r13_where'](p)for p in people};s.room13['period']=3
   for loc in set(v for v in actual.values()if v):maxima[loc]=max(maxima.get(loc,0),sum(v==loc for v in actual.values()))
   cases+=1
assert set(res)<=visible,sorted(set(res)-visible)
rows=[]
for period in range(3):
 s.room13=copy.deepcopy(base);s.room13.update(day=1,period=period);n['r13_resident_where']=old;a=sorted(p for p in people if n['r13_where'](p)=='square');n['r13_resident_where']=new;b=sorted(p for p in people if n['r13_where'](p)=='square');rows.append({'period':period,'before':a,'after':b})
report={'status':'passed','conditions':cases,'optional_people':sorted(optional),'changed_schedule_entries':len(changed),'all_35_content_residents_reachable':len(set(res)&visible),'first_day_square':rows,'maxima':maxima,'checks':['Non-optional story-critical locations unchanged for all states','Piko clinic and shelter/patient overrides preserved','Dead/detained residents absent','Period3 remains evening, home is not field presence','No schedule query mutates any story state']}
out=ROOT/'qa-room13-0156/routines';out.mkdir(parents=True,exist_ok=True);(out/'source-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
