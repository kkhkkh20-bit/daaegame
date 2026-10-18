"""Official RenPy testcase source, not a claim that native execution succeeded."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
N={}
for p in ['recommended_model.py','recommended_ep456_model.py']:
 exec(compile((R/'dev'/p).read_text(),p,'exec'),N)
A=N['r13_rec_actions'];C=N['r13_rec_cards']
out=['# Generated native fixtures. Administrator direct-entry seeds prior M2 and Piko-safe.', '# Earlier gameplay is not tested by these fixtures. All episode actions and inference clicks are real.', '# Native execution/screenshots are still required; do not present source generation as a passed playtest.']

def boot(name,ep):
 out.extend(['','testcase '+name+':','    pause 2.0','    $ r13_rec_admin_harness=True','    run Call("r13_recommended_ep%d_admin")'%ep,'    click pos (640,600) until screen "r13_recommended_actions" timeout 80'])
 return N['r13_rec_e456_admin_seed'](ep)
def act(s,key):
 out.append('    click '+repr(A[key]['title']))
 if key=='e4_mechanism':
  out.extend(['    click pos (640,600) until screen "r13_rec_e4_layout" timeout 80','    screenshot "recommended-e4-layout.png"','    click "P · 작업칸 쪽"','    click pos (640,600) until screen "r13_rec_e4_layout" timeout 80','    assert eval ("e4_card_lever" not in r13_recommended["facts"])','    click "R · 객실 쪽"','    click pos (640,600) until screen "r13_rec_e4_layout" timeout 80','    click "L 올리기"','    click pos (640,600) until screen "r13_rec_e4_layout" timeout 80','    click "L 끝까지 내리기"'])
 if key=='e5_pots':
  out.extend(['    click pos (640,600) until screen "r13_rec_e5_pots_screen" timeout 80','    screenshot "recommended-e5-pots-original.png"','    click "몸체: 깨진 귀"'])
 if key=='e6_night':
  out.extend(['    click pos (640,600) until screen "choice" timeout 80','    click "오늘은 학교에 함께 남는다"'])
 out.append('    click pos (640,600) until screen "r13_recommended_actions" timeout 100')
 return N['r13_rec_apply'](s,key)
def advance(s):
 out.extend(['    click "오늘을 마친다"','    click "다음 날로 간다"','    click pos (640,600) until screen "r13_recommended_actions" timeout 80'])
 return N['r13_rec_next_day'](s)
def hearing(s):
 out.extend(['    click "공개 회의"','    click pos (640,600) until screen "r13_recommended_cards" timeout 80'])
 steps=N['r13_rec_e456_hearing'](s)
 for i,step in enumerate(steps):
  if i==0:
   wrong=next(k for k in s['facts'] if k!=step['card'])
   out.extend(['    click '+repr(C[wrong][0]),'    click pos (640,600) until screen "r13_recommended_cards" timeout 80','    assert eval (r13_recommended["episodes"][str(r13_recommended["episode"])]["hearing"]==0)'])
  out.append('    click '+repr(C[step['card']][0]))
  if s['episode']==5 and not s['e5_poison_blocked'] and i==0:
   out.extend(['    assert screen "r13_rec_e5_pots_screen"','    screenshot "recommended-e5-pots-swapped.png"','    click "몸체: 깨진 귀"'])
  out.extend(['    assert screen "r13_rec_e456_pick"','    click '+repr(next(x[1] for x in step['details'] if x[0]==step['right_detail'])),'    assert screen "r13_rec_e456_pick"','    click '+repr(next(x[1] for x in step['claims'] if x[0]==step['right_claim'])),'    click pos (640,600) until screen '+repr('r13_recommended_actions' if i==len(steps)-1 else 'r13_recommended_cards')+' timeout 100'])
  s,_,ok=N['r13_rec_e456_present'](s,step['card'],step['right_detail'],step['right_claim']);assert ok
 return s
s=boot('recommended_ep4_structure_and_prevention',4)
for k in ['e4_escort','e4_rescue']:s=act(s,k)
s=advance(s)
for k in ['e4_nabi7','e4_clinic_alive','e4_mechanism','e4_plan']:s=act(s,k)
s=advance(s)
for k in ['e4_block_lever','e4_watch','e4_work']:s=act(s,k)
out+=['    assert eval (r13_recommended["episodes"]["4"]["victim"]=="recovering" and r13_recommended["episodes"]["4"]["day9"]=="prevented")']
s=advance(s);s=hearing(s)
out+=['    assert eval (r13_recommended["neoul"]=="detained" and "e4_card_nabi9" not in r13_recommended["facts"])','    screenshot "recommended-e4-survival-and-detention.png"']
for safe in (True,False):
 s=boot('recommended_ep5_'+('prevention' if safe else 'body_lid_target'),5)
 if safe:s=act(s,'e5_school')
 s=advance(s)
 for k in ['e5_pots','e5_pharmacy']:s=act(s,k)
 for k in (['e5_lock','e5_serve_safe'] if safe else ['e5_serve_accident','e5_interview','e5_saemi','e5_bottle']):s=act(s,k)
 s=advance(s)
 if not safe:s=act(s,'e5_care_handoff')
 s=hearing(s)
 out+=['    assert eval (r13_recommended["episodes"]["5"]["event"]=='+repr('prevented' if safe else 'contaminated')+')','    assert eval (r13_recommended["neoul"]=="detained")','    screenshot "recommended-e5-'+('prevented' if safe else 'responsibility')+'.png"']
s=boot('recommended_ep6_actual_protection',6)
for k in ['e6_board','e6_manifest','e6_pandol','e6_nabi','e6_munchi','e6_hold','e6_altar','e6_research','e6_heat','e6_beds','e6_meals','e6_care','e6_route']:s=act(s,k)
s=advance(s);s=hearing(s)
out+=['    assert eval (not r13_recommended["episodes"]["6"]["today_sacrifice_stopped"])','    screenshot "recommended-e6-proof-not-yet-handoff.png"']
for k in ['e6_cancel','e6_handoff','e6_split_duties','e6_night']:s=act(s,k)
out+=['    assert eval (r13_recommended["episodes"]["6"]["verdict"]=="complete_today" and r13_recommended["episodes"]["6"]["today_sacrifice_stopped"])','    assert eval (r13_recommended["mother"]=="M2" and r13_recommended["neoul"]=="detained")','    screenshot "recommended-e6-first-night.png"','    $ r13_qa_note("recommended_ep456: direct-entry fixture seeds prior history; episode actions, layout/pot clicks, card/part/conclusion, survival prevention and actual cancellation/handoff are native UI-tested only if this testcase has passed.")']
(R/'game/qa_tests/recommended_ep456.rpy').write_text('\n'.join(out)+'\n')

from catalog_native import rewrite_catalog_clicks
rewrite_catalog_clicks(Path(__file__).resolve().parents[1]/"game/qa_tests/recommended_ep456.rpy")
