from playwright.sync_api import sync_playwright
import argparse, shutil
parser = argparse.ArgumentParser(description="Prepared-evidence browser regression: council to epilogue (not a fresh-game walkthrough).")
parser.add_argument("--url", default="http://127.0.0.1:8000/playT.html")
parser.add_argument("--retry", action="store_true", help="Check the first conclusion question appears again after reset")
parser.add_argument("--failure", action="store_true", help="Choose five wrong conclusions and check M-F/restart preserves evidence")
parser.add_argument("--final", action="store_true", help="Start at the final confrontation (use with --failure)")
parser.add_argument("--without-ledger", action="store_true", help="Complete the story without optional C11 ledger discovery")
args = parser.parse_args()
TICK=r'''() => {
 const q=s=>document.querySelector(s), click=s=>{const e=q(s);if(e&&!e.disabled){e.click();return true}return false};
 if(q('#logic-panel')){
  if(q('#logic-panel [data-act="finish"]')){click('#logic-panel [data-act="finish"]');return 'reason finish'}
  const solutions={linen:[['C02','C03']],time:[['C06','C07'],['C13','C08']],location:[['C04','C10']],contact:[['C05','C01']],seal:[['C10','C12']]};
  const root=q('#logic-panel'),ids=(solutions[root.dataset.reason]||[])[Number(root.dataset.stage)];if(!ids)return 'unknown reason';
  for(const id of ids)if(!q('#logic-panel [data-card="'+id+'"][aria-pressed="true"]')){click('#logic-panel [data-card="'+id+'"]');return 'reason card '+id}
  if(!q('#logic-panel [data-option="0"][aria-pressed="true"]')){click('#logic-panel [data-option="0"]');return 'reason conclusion'}
  click('#logic-panel [data-act="submit"]');return 'reason submit';
 }
 if(q('#rtgpick')){const title=q('#rtgpick b').textContent;let opts=[];const ph=window.__rtPh();
 for(const L of [...(ph.lines||[]),...(ph.stms||[]).flatMap(s=>[...(s.ok||[]),...(s.steps||[]).flatMap(x=>x.lines||[])])])if(L.ask&&L.ask.title===title)opts=L.ask.items;
 for(const st of ph.stms||[])for(const step of st.steps||[])if(step.pick&&step.pick.title===title)opts=step.pick.items;
 const i=opts.findIndex(x=>x.ok);if(i<0)return 'unknown pick '+title;click('#rtgpick [data-pi="'+i+'"]');return 'pick'}
 if(q('#rtgq')){click('#rtgq');return 'queue'}
 if(window.__T('!!DL')){window.__T('advance()');return 'dialog'}
 if(q('#rtnext')){click('#rtnext');return 'next'}
 const ph=window.__rtPh&&window.__rtPh();if(!ph)return 'wait';
 if(ph.type==='vote'){click('.vc[data-seat="seryeon"]');return 'vote'}
 if(ph.type!=='debate')return 'wait '+ph.type;
 const idx=ph.stms.findIndex(s=>s.a&&s.k);const em=q('.rt-bub.stm em');if(!em)return 'wait stm';
 const current=parseInt(em.textContent)-1;if(current!==idx){click('#rtnx');return 'change stm'}
 const st=ph.stms[idx],step=window.__rtgStep(st),id=step<(st.steps||[]).length?st.steps[step].ids[0]:st.a[0];
 if(!document.body.classList.contains('rtg-drw')){click('#rtgbar [data-g="ev"]');return 'drawer'}
 if(!q('.bl.on')||q('.bl.on').dataset.bl!==id){click('[data-bl="'+id+'"]');return 'select '+id}
 if(click('#rtexam'))return 'examine';
 click('#rtgbar [data-g="present"]');return 'present '+id;
}'''
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
 pg=b.new_page(viewport={'width':844,'height':390});errs=[];bad=[]
 pg.on('pageerror',lambda e:errs.append(str(e)))
 pg.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
 pg.goto(args.url,wait_until='domcontentloaded');pg.wait_for_timeout(16000)
 pg.evaluate('''window.__T('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};');document.querySelector('#innmain').remove();window.__w209boot()''');pg.wait_for_timeout(1000)
 prepared='G.found=Object.keys(window.EP1INN.EV);G.exam={};allSpots(CASES[G.ci]).forEach(s=>G.exam[s.ev.id]=true);G.unlocked=CASES[G.ci].locations.map(l=>l.req).filter(Boolean);'
 if args.without_ledger:prepared+='G.found=G.found.filter(id=>id!=="C11");'
 prepared += 'G.beats.inn_meet=1;window.__innOpenFinal()' if args.final else 'window.__rtOpen(CASES[G.ci])'
 pg.evaluate('(code)=>window.__T(code)', prepared)
 pg.evaluate('''window.__audioSeen={};window.__caseTurns={};setInterval(()=>{const s=window.__innAudioState();if(s.line){window.__audioSeen[s.line]={who:s.who,key:s.key,confession:s.confession,cue:s.cue,want:window.__innWant()};if(s.line.startsWith('[반박 결과]'))window.__caseTurns[s.line]=window.__T('Object.assign({},G.beats.rtVotes)')}},60)''')
 if args.failure:
  initial=pg.evaluate('window.__T("G.found.slice()")');wr=0;saw_mf=False;recovered=False
  for i in range(700):
   st=pg.evaluate('(code)=>window.__T(code)', '({hp:G.hp,wrong:G.wrong,dl:!!DL,pi:G.debate&&G.debate.pi,rt:!!document.querySelector("body>.rt")})')
   if st['wrong']>=5 and st['dl']:saw_mf=True
   if saw_mf and st['hp']==5 and st['rt']:
    recovered=True;break
   if pg.locator('#logic-panel').count():
    pg.evaluate('''()=>{const root=document.querySelector('#logic-panel'),maps={linen:[['C02','C03']],time:[['C06','C07'],['C13','C08']],location:[['C04','C10']],contact:[['C05','C01']],seal:[['C10','C12']]},ids=maps[root.dataset.reason][Number(root.dataset.stage)];for(const id of ids){const b=root.querySelector('[data-card="'+id+'"]');if(b.getAttribute('aria-pressed')!=='true')b.click()}root.querySelector('[data-option="1"]').click();root.querySelector('[data-act="submit"]').click()}''')
   elif pg.locator('#rtgpick').count():
    pg.locator('#rtgpick [data-pi="1"]').click();wr+=1
   else:pg.evaluate(TICK)
   pg.wait_for_timeout(220)
  assert recovered,st
  assert st['wrong']==5, (wr,st)
  assert not pg.evaluate('window.__innAudioState().failure')
  pg.wait_for_timeout(500)
  assert pg.evaluate('window.__T("G.wrong")')==5
  if args.final:
   assert pg.evaluate('window.EP1INN.FINAL.phases.indexOf(window.__rtPh())')==0
  assert pg.evaluate('window.__T("G.found.slice()")')==initial
  assert not errs,errs
  assert not bad,bad
  print('Five wrong choices → M-F → restart OK', st, flush=True)
  b.close()
 elif args.retry:
  titles=[]
  for run in range(2):
   pg.evaluate('(code)=>window.__T(code)', 'if(DL){DL.done=null;endDlg()};document.querySelectorAll("body>.rt").forEach(x=>x.remove());window.__inMeeting=false;window.__rtgReset();G.debate={pi:1,sus:{}};window.__rtOpen(CASES[G.ci])')
   title=None
   for i in range(180):
    if pg.locator('#logic-panel').count():
     title=pg.locator('#logic-panel h2').inner_text()
     if run==0:
      for _ in range(15):
       if not pg.locator('#logic-panel').count():break
       pg.evaluate(TICK);pg.wait_for_timeout(200)
     break
    pg.evaluate(TICK);pg.wait_for_timeout(180)
   titles.append(title)
   pg.wait_for_timeout(700)
  assert titles[0] == '이불의 손자국을 누구에게 다시 물어볼까?', titles
  assert titles[1] == titles[0], titles
  assert not errs, errs
  assert not bad, bad
  print('Retry choices OK:', titles, flush=True)
  b.close()
 else:
  last=None
  for i in range(1600):
   state=pg.evaluate('window.__T("({beats:G.beats,wrong:G.wrong,dl:DL&&DL.full,phase:window.__rtPh&&window.__rtPh()&&window.__rtPh().topic})")')
   if state['beats'].get('inn_end'):break
   action=pg.evaluate(TICK)
   key=state.get('phase')
   if key!=last or i%200==0:print('progress',i,key,action,flush=True);last=key
   if action.startswith('unknown'): print(action,flush=True);break
   pg.wait_for_timeout(180)
  assert state['beats'].get('inn_end'), state
  assert state['wrong']==0, state
  turns=pg.evaluate('window.__caseTurns')
  expected_turns=[
   '[반박 결과] 할머니만 그 방을 드나들었다는 생각이 깨졌다.',
   '[반박 결과] 차갑다는 이유로 손님을 죽였다고 몰아갈 수 없다.',
   '[반박 결과] 우리를 몰아붙이던 목격담이 세련의 알리바이를 무너뜨렸다.',
   '[반박 결과] 처음 발견했다는 이유로 부녀를 몰아가던 의심이 걷혔다.',
   '[반박 결과] 주머니를 보지도 못했다는 말이 바뀌었다.',
   '[반박 결과] 남을 도둑으로 몰던 사람이 직접 주머니를 숨겼다고 인정했다.',
   '[반박 결과] 사라진 이백 냥은 도난 피해가 아니라 세련의 노름 손실이었다.',
   '[반박 결과] 도난 누명과 이백 냥 배상 요구가 철회됐다. 여관을 넘기라는 압박도 끝났다.',
  ]
  assert all(t in turns for t in expected_turns),turns
  first=list(turns[expected_turns[0]].values())
  assert first.count('innma')==4 and first.count('기권')==2,first
  middle=list(turns[expected_turns[2]].values())
  assert middle.count('seryeon')==3 and middle.count('부녀')==1,middle
  assert '부녀' not in turns[expected_turns[3]].values(),turns[expected_turns[3]]
  assert all(v=='seryeon' for v in turns[expected_turns[-1]].values()),turns[expected_turns[-1]]
  print('Reversals: first objection withdraws a vote; eight accepted outcomes through accusation/payment withdrawal OK',flush=True)
  if args.without_ledger:assert not pg.evaluate('(code)=>window.__T(code)', 'G.found.includes("C11")')
  audio=pg.evaluate('window.__audioSeen')
  for relationship_beat in ('다람 양이 본 것도 기록', '다니는 길에 물어볼게요',
                            '엄마 단서를 그냥 두고', '내일은 우체국에서',
                            '엄마 찾으면 서점 다시 열자'):
   assert any(relationship_beat in t for t in audio),('Epilogue relationship missing',relationship_beat)
  print('Family epilogue: child testimony accepted, village allies and active mother search before bookstore return OK',flush=True)
  assert audio.get('…네.',{}).get('confession'), audio.get('…네.')
  assert any(v['key'] for k,v in audio.items() if k.startswith('첫눈은 자정')), 'Council dialogue audio hook missing'
  assert any(v['want']=='inn_meet_press' for v in audio.values()), 'Council pressure tempo missing'
  assert any(v['cue']=='pulse' and v['want'] is None for v in audio.values()), 'Council heartbeat silence missing'
  print('Audio hooks: council silence/pulse/pressure and final confession OK',flush=True)
  assert not errs, errs
  assert not bad, bad
  print('RESULT',state,'errors',errs,'bad',bad,flush=True)
  print(pg.locator('body').inner_text()[-2000:],flush=True)
  pg.screenshot(path='/tmp/ch1-council.png');b.close()
