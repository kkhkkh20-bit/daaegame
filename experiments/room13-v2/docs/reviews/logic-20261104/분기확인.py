"""읽기 전용 감사: 원본 함수의 분기와 선택 결과를 실행해 확인한다. 화면 렌더링은 하지 않는다."""
import copy,itertools,json,textwrap,types
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
DAY=json.loads((ROOT/'game/story/day01.json').read_text())
COMMON=json.loads((ROOT/'game/story/common.json').read_text())
LAYOUT=json.loads((ROOT/'game/data/layout.json').read_text())
class Music:
 def __getattr__(self,n):return lambda *a,**k:None
class Renpy:
 music=Music()
 def open_file(self,path,**kw):return (ROOT/'game'/path).open(**kw)
 def __getattr__(self,n):return lambda *a,**k:None
class Sim:
 def __init__(self):
  self.s=types.SimpleNamespace(v2_pick=[],v2_pick_for=None,v2_pair=False,v2_stage=None)
  self.ns=dict(store=self.s,persistent=types.SimpleNamespace(v2_last_end=None),renpy=Renpy(),
    Transform=lambda *a,**k:None,Fixed=lambda *a,**k:None,Solid=lambda *a,**k:None,Dissolve=lambda *a,**k:None, SnowBlossom=lambda *a,**k:None,AlphaMask=lambda *a,**k:None)
  source=(ROOT/'game/engine/engine.rpy').read_text().split('init python:\n',1)[1].split('\ntransform ',1)[0]
  exec(compile(textwrap.dedent(source),'engine.rpy','exec'),self.ns)
  self.f('v2_new_game');self.lines=[]
 def f(self,name,*a,**kw):return self.ns[name](*a,**kw)
 def drain(self):
  for _ in range(1200):
   kind=self.f('v2_advance')
   if kind=='line':
    frame,st=self.f('v2_current');self.lines.append(copy.deepcopy(st));frame[1]+=1;frame[2]=0
    if st['who'] in self.ns['V2_DRAWN'] and st['who'] not in self.s.v2_met:self.s.v2_met.append(st['who'])
   elif kind=='wait':self.f('v2_wait_enter');return kind
   else:return kind
  raise AssertionError('단계 수 초과')
 def opt(self,gate,index):self.f('v2_run_option',gate,index);return self.drain()
 def investigate(self,rules=False):
  assert self.drain()=='wait' and self.s.v2_gate=='gate_request'
  assert self.opt('gate_request',1)=='wait'
  assert self.opt('gate_choice',1)=='menu'
  self.f('v2_menu_choose',1);assert self.drain()=='wait'
  assert self.opt('gate_investigate',0)=='wait'
  if rules:assert self.opt('gate_investigate',1)=='wait'
 def proof(self,ids):
  assert self.opt('gate_investigate',4)=='proof'
  self.f('v2_proof_prepare','gate');self.f('v2_proof_result',('submit',ids));return self.drain()

out={}
rows=[]
for rules in [False,True]:
 for ids in [['E03'],['E03','E04']] if rules else [['E03']]:
  for heard in [False,True]:
   s=Sim();s.investigate(rules)
   if heard:assert s.opt('gate_investigate',3)=='ui';s.s.v2_ui=None
   s.lines=[];s.proof(ids)
   rows.append(dict(owned=s.s.v2_ev,selected=ids,difference_already_acknowledged=heard,
                    gate=s.s.v2_gate,lines=[dict(id=x.get('id'),who=x['who'],text=x['t']) for x in s.lines]))
out['부분제출후반응']=rows
rows=[]
for rules in [False,True]:
 s=Sim();s.investigate(rules);s.lines=[];s.proof(['E02','E03'])
 rows.append(dict(owned=s.s.v2_ev,rules_read=rules,gate=s.s.v2_gate,registered=s.s.v2_vals.get('gate_registered'),basis_proven=s.s.v2_vals.get('gate_basis_proven')))
out['규칙자료선택성']=rows
s=Sim();s.investigate();assert s.proof(['E02','E03'])=='wait';assert s.s.v2_gate=='registered_menu'
out['등록후자료반응']=[]
for ev in ['E01','E02','E05']:
 t=Sim();t.investigate();t.proof(['E02','E03']);t.f('v2_click_person','guard');ui=copy.deepcopy(t.s.v2_ui)
 t.lines=[];t.f('v2_present_to','guard',ev);t.drain()
 out['등록후자료반응'].append(dict(ev=ev,ui_was_available=ui,lines=[x['t'] for x in t.lines]))
out['회의제출조합']=[]
for n in range(1,5):
 for ids in itertools.combinations(['E01','E02','E03','E04'],n):
  s=Sim();s.investigate(True);s.lines=[];s.proof(list(ids))
  out['회의제출조합'].append(dict(selected=list(ids),win=s.s.v2_vals.get('gate_basis_proven',False),reply=[x['t'] for x in s.lines if x['who']=='guard'],next_hint=[x['t'] for x in s.lines if x['who']=='dad' and x['t'].startswith('(')]))
out['정정후후속질문']=[]
for reason_heard in [False,True]:
 s=Sim();s.investigate()
 if reason_heard:
  assert s.opt('gate_investigate',3)=='ui';s.s.v2_ui=None
  assert s.opt('gate_investigate',5)=='ui';s.s.v2_ui=None
 assert s.proof(['E02','E03'])=='wait'
 topics=s.f('v2_topics','guard')
 follow=next(t for t in topics if t['key']==('follow','F002'))
 s.lines=[];s.f('v2_pick_topic','guard',('follow','F002'));s.drain()
 out['정정후후속질문'].append(dict(reason_heard=reason_heard,
  marked_read_before_question=follow['read'],lines=[x['t'] for x in s.lines]))

out['끝부분미관찰비교성공']=[]
for night_path in [0,1]:
 s=Sim();s.investigate();assert s.proof(['E02','E03'])=='wait'
 assert s.opt('registered_menu',1)=='wait'
 assert s.opt('to_room13',0)=='wait'
 assert s.opt('note_pick',0)=='wait'
 assert s.opt('bundle_open',0)=='proof'
 assert not s.s.v2_vals.get('letter_tail_observed')
 s.lines=[];s.f('v2_proof_prepare','letters')
 s.f('v2_proof_result',('submit',['E01','E06']))
 assert s.drain()=='menu'
 auto=[x['t'] for x in s.lines if (x.get('id') or '').startswith('NW_D01_SR0')]
 assert len(auto)==3
 s.lines=[];s.f('v2_menu_choose',night_path);kind=s.drain()
 if night_path==1:
  assert kind=='wait';assert s.s.v2_gate=='to_inn'
  assert s.opt('to_inn',0)=='wait';assert s.s.v2_gate=='to_room13_night'
 assert any(x.get('id')=='MS14_D01_S05_L0037' for x in s.lines)
 out['끝부분미관찰비교성공'].append(dict(night_path=night_path,
  tail_observed=bool(s.s.v2_vals.get('letter_tail_observed')),
  automatic_explanation=auto,
  chorong_location_told_before_bed=True))

# 이번 검수의 핵심 관찰을 재실행 시에도 확인한다.
assert all(r['win']==({'E02','E03'}<=set(r['selected'])) for r in out['회의제출조합'])
assert all(r['registered'] and r['basis_proven'] for r in out['규칙자료선택성'])
assert '확인하지 않은 서류' in out['부분제출후반응'][1]['lines'][-1]['text']
assert out['등록후자료반응'][-1]['lines']==['그것만으로는 확인이 안 되오.']
Path(__file__).with_name('분기확인.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('분기 확인 완료:', {k:len(v) for k,v in out.items()})
