from playwright.sync_api import sync_playwright
import argparse, shutil
parser = argparse.ArgumentParser(description="Prepared-evidence browser regression: council to epilogue (not a fresh-game walkthrough).")
parser.add_argument("--url", default="http://127.0.0.1:8000/playT.html")
parser.add_argument("--retry", action="store_true", help="Check the first conclusion question appears again after reset")
parser.add_argument("--failure", action="store_true", help="Present five wrong clues and check failure/restart preserves evidence")
parser.add_argument("--final", action="store_true", help="Start at the final confrontation (use with --failure)")
parser.add_argument("--without-ledger", action="store_true", help="Complete the story without optional C11 ledger discovery")
parser.add_argument("--resume", help="Use actual collected storage; acquire C05 and C14 through native UI instead of injecting evidence")
parser.add_argument("--from-final", action="store_true", help="Resume an actual collected final checkpoint through the native evidence-record footer; assert final/ending outcomes only")
args = parser.parse_args()
if args.from_final and not args.resume:parser.error('--from-final requires --resume')
TICK=r'''() => {
 const q=s=>document.querySelector(s), click=s=>{const e=q(s);if(e&&!e.disabled){e.click();return true}return false};
 if(q('#inn-mother-lead')){const state=window.__innMotherLeadState();
  return click('#inn-mother-lead [data-mother-action="'+(state.compared?'record':'compare')+'"]')?'mother clue':'wait mother clue'}
 if(q('#inn-ch2-peek'))return click('#inn-ch2-peek .peek-finish')?'finish teaser':'wait teaser';
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
 context=b.new_context(viewport={'width':844,'height':390},storage_state=args.resume if args.resume else None)
 pg=context.new_page();errs=[];bad=[]
 pg.on('pageerror',lambda e:errs.append(str(e)))
 pg.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
 pg.goto(args.url,wait_until='domcontentloaded');pg.wait_for_timeout(16000)
 if args.resume:
  pg.locator('#innmain [data-m="cont"]').click();pg.wait_for_timeout(1000)
 else:
  pg.evaluate('''window.__T('S.prog.inn=fresh(CASES.findIndex(c=>c.id=="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};');document.querySelector('#innmain').remove();window.__w209boot()''');pg.wait_for_timeout(1000)
 prepared='G.found=Object.keys(window.EP1INN.EV);G.exam={};allSpots(CASES[G.ci]).forEach(s=>G.exam[s.ev.id]=true);G.unlocked=CASES[G.ci].locations.map(l=>l.req).filter(Boolean);'
 if args.without_ledger:prepared+='G.found=G.found.filter(id=>id!=="C11");'
 prepared += 'G.beats.inn_meet=1;window.__innOpenFinal()' if args.final else ('G.beats.inn_meeting_version=2;G.beats.inn_life_confirmed=1;G.debate={pi:3,sus:{}};window.__rtOpen(CASES[G.ci])' if args.failure else 'window.__rtOpen(CASES[G.ci])')
 if args.resume:
  if args.from_final:
   assert pg.evaluate('window.__T("!!G.innfinal&&G.innfinal.pi===3")'), 'Actual Continue lost the paused final phase'
   if not pg.locator('body>.rt').count() and pg.evaluate('(code)=>window.__T(code)', 'G.found.includes("C14")||G.asked.includes("C14")'):
    pg.locator('#w209rail .g>[data-w="ev"]').click()
    pg.locator('#inn-final-record-resume').click()
  else:pg.evaluate('(code)=>window.__T(code)', 'window.__rtOpen(CASES[G.ci])')
 else:pg.evaluate('(code)=>window.__T(code)', prepared)
 pg.evaluate('''window.__audioSeen={};window.__caseTurns={};setInterval(()=>{const s=window.__innAudioState();if(s.line){window.__audioSeen[s.line]={who:s.who,key:s.key,confession:s.confession,cue:s.cue,want:window.__innWant(),duck:window.__innDuck(),tense:window.__innTense()};window.__caseTurns[s.line]=window.__T('Object.assign({},G.beats.rtVotes)')}},60)''')
 if args.failure:
  initial=pg.evaluate('window.__T("G.found.slice()")');wr=0;saw_mf=False;recovered=False
  for i in range(700):
   st=pg.evaluate('(code)=>window.__T(code)', '({hp:G.hp,wrong:G.wrong,dl:!!DL,pi:G.debate&&G.debate.pi,rt:!!document.querySelector("body>.rt")})')
   if st['wrong']>=5 and st['dl']:saw_mf=True
   if saw_mf and st['hp']==5 and st['rt']:
    recovered=True;break
   if pg.locator('#rtgpick').count():
    pg.locator('#rtgpick [data-pi="1"]').click();wr+=1
   elif pg.evaluate('!!window.__rtgQueue()') or pg.locator('#rtnext').count() or pg.evaluate('window.__T("!!DL")'):
    pg.evaluate(TICK)
   elif pg.evaluate('window.__rtPh()?.type')=='debate':
    pg.evaluate('''()=>{if(!document.body.classList.contains('rtg-drw')){document.querySelector('#rtgbar [data-g="ev"]').click();return}const c=document.querySelector('.rt .bl.on');if(!c||c.dataset.bl!=='C09'){document.querySelector('.rt [data-bl="C09"]').click();return}document.querySelector('#rtgbar [data-g="present"]').click()}''')
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
  print('Five wrong presentations → failure → restart OK', st, flush=True)
  b.close()
 elif args.retry:
  steps=[]
  for run in range(2):
   pg.evaluate('(code)=>window.__T(code)', 'if(DL){DL.done=null;endDlg()};document.querySelectorAll("body>.rt").forEach(x=>x.remove());window.__inMeeting=false;window.__rtgReset();G.beats.inn_meeting_version=2;G.debate={pi:3,sus:{}};window.__rtOpen(CASES[G.ci])')
   pg.wait_for_timeout(2500)
   steps.append(pg.evaluate('window.__rtgStep(window.__rtPh().stms[1])'))
   if run==0:
    pg.evaluate('document.querySelector("#rtnx").click();document.querySelector("#rtgbar [data-g=ev]").click()')
    pg.wait_for_timeout(250)
    pg.evaluate('document.querySelector(".rt [data-bl=C02]").click()')
    pg.wait_for_timeout(250)
    pg.evaluate('document.querySelector("#rtgbar [data-g=present]").click()')
    pg.wait_for_timeout(250)
    assert pg.evaluate('window.__rtgStep(window.__rtPh().stms[1])')==1
  assert steps==[0,0],steps
  assert not errs, errs
  assert not bad, bad
  print('Retry direct proof OK: first evidence step is required again',steps,flush=True)
  b.close()
 else:
  if args.resume:
   from qa_scene_guidance import Investigation
   actual=Investigation(pg)
   def actual_npc(npc):
    if pg.locator('#closeNotice:visible').count():actual.click('#closeNotice')
    elif pg.locator('#closeNotice').count():pg.wait_for_function('!document.getElementById("closeNotice")',timeout=12000)
    pg.wait_for_function('(npc)=>{const im=document.querySelector("#bigscene svg image.wn9[data-k="+npc+"]");return im&&window.__innMask()[im.getAttribute("href")]==="ok"}',arg=npc)
    point=None
    for direction in [None,'#fsar','#fsar','#fsal']:
     if direction and pg.locator(direction+':visible').count():actual.click(direction);pg.wait_for_timeout(550)
     point=pg.evaluate('''(npc)=>{const r=document.querySelector('#bigscene').getBoundingClientRect();for(let y=Math.max(12,r.top+12);y<Math.min(innerHeight-12,r.bottom-12);y+=6)for(let x=Math.max(12,r.left+12);x<Math.min(innerWidth-12,r.right-12);x+=6)if(document.elementFromPoint(x,y)?.closest('#bigscene')&&[[0,0],[-6,0],[6,0],[0,-6],[0,6]].every(([dx,dy])=>window.__innNpcHit(x+dx,y+dy)===npc))return {x,y};return null}''',npc)
     if point:break
    if not point:
     pg.screenshot(path='/tmp/purchase-npc-diagnostic.png')
     print('NPC diagnostic',actual.state(),pg.locator('body').inner_text()[-1600:],pg.evaluate('({modal:!!document.querySelector("#ov .modal,#mveil .modal,.crec2,#innmove"),rt:!!document.querySelector("body>.rt"),meeting:window.__inMeeting,native:window.__logicNativeEpoch})'),flush=True)
    assert point, ('NPC has no reachable opaque character pixels',npc)
    pg.mouse.click(point['x'],point['y']);pg.wait_for_timeout(400);actual.drain()
    assert actual.state()['tab']=='talk', ('Character tap did not open native talk',npc,actual.state())
   def collect_fur():
    assert pg.evaluate('window.__T("!!G.beats.inn_life_confirmed")'), 'Fur collection began before clinical confirmation'
    actual.drain();actual.move('dining');actual_npc('innma')
    actual.click('#showev');actual.click('[data-show="C04"]');actual.drain()
    assert pg.evaluate('window.__T("!!G.beats.inn_show_innma_C04")')
    actual.click('#w209rail .g>[data-w="scene"]');actual.drain();actual.move('bed13');actual.collect('C05')
    assert not pg.evaluate('(code)=>window.__T(code)', 'G.found.includes("C11")')
    context.storage_state(path='/tmp/late-actual-before-final.json')
    pg.evaluate('(code)=>window.__T(code)', 'window.__rtOpen(CASES[G.ci])')
    print('Actual adjournment → grandma lends magnifier → native C05 → resume; no evidence injection',flush=True)
   def collect_carriage_record():
    assert not pg.evaluate('(code)=>window.__T(code)', 'G.found.includes("C14")||G.asked.includes("C14")'), 'Final dialogue granted the carriage record without investigation'
    actual.drain()
    if actual.state()['room']!='plaza':actual.move('plaza')
    context.storage_state(path='/tmp/purchase-actual-before-karo.json')
    actual_npc('karo')
    if not pg.evaluate('(code)=>window.__T(code)', 'G.asked.includes("T_ka2")') and pg.locator('[data-ask="T_ka2"]:visible').count():
     actual.click('[data-ask="T_ka2"]');actual.drain()
    else:
     actual.click('#showev');actual.click('[data-show="C09"]')
     pg.wait_for_function("(code)=>window.__T('!!DL')||document.querySelector('#innins')||window.__T(code)",arg='G.found.includes("C14")')
     actual.drain()
    assert pg.evaluate('(code)=>window.__T(code)', 'G.found.includes("C14")||G.asked.includes("C14")'), 'Actual Karo encounter failed to grant the carriage record'
    actual.click('#w209rail .g>[data-w="scene"]');actual.drain()
    context.storage_state(path='/tmp/purchase-actual-before-f3.json')
    actual.click('#w209rail .g>[data-w="ev"]')
    actual.click('#inn-final-record-resume')
    print('Actual F3 adjournment → village plaza → native Karo question → C14 → final resume; no evidence injection',flush=True)
  last=None;captured_mother=False;captured_teaser=False
  for i in range(1600):
   state=pg.evaluate('window.__T("({beats:G.beats,wrong:G.wrong,dl:DL&&DL.full,phase:window.__rtPh&&window.__rtPh()&&window.__rtPh().topic})")')
   if state['beats'].get('inn_end') and not pg.locator('#inn-ch2-peek').count() and state['beats'].get('inn_ch2_peek_seen'):break
   if pg.locator('#inn-mother-lead').count():
    compared=pg.evaluate('window.__innMotherLeadState().compared')
    if compared and not captured_mother:
     pg.screenshot(path='/tmp/purchase-actual-mother-comparison.png');captured_mother=True
    pg.locator('#inn-mother-lead [data-mother-action="'+('record' if compared else 'compare')+'"]').click()
    pg.wait_for_timeout(500 if not compared else 220);continue
   if pg.locator('#inn-ch2-peek').count():
    teaser=pg.evaluate('window.__innChapter2PeekState()')
    if teaser['stage']=='missing' and not captured_teaser:
     pg.screenshot(path='/tmp/purchase-actual-chapter2-preview.png');captured_teaser=True
    if teaser['ready']:pg.locator('#inn-ch2-peek .peek-finish').click()
    pg.wait_for_timeout(180);continue
   if args.resume and pg.evaluate('(code)=>window.__T(code)', '!!(G.debate&&G.debate.hold)&&!G.found.includes("C05")'):
    collect_fur();continue
   if args.resume and pg.evaluate('(code)=>window.__T(code)', '!!(G.innfinal&&G.innfinal.hold)&&!(G.found.includes("C14")||G.asked.includes("C14"))'):
    collect_carriage_record();continue
   action=pg.evaluate(TICK)
   key=state.get('phase')
   if key!=last or i%200==0:print('progress',i,key,action,flush=True);last=key
   if action.startswith('unknown'): print(action,flush=True);break
   pg.wait_for_timeout(180)
  assert state['beats'].get('inn_end'), state
  assert state['beats'].get('inn_mother_lead'), 'Played route skipped the direct handwriting comparison'
  assert state['beats'].get('inn_ch2_peek_seen'), 'Native chapter 2 preview did not finish'
  assert state['beats'].get('inn_case_cleared') and state['beats'].get('inn_child_heard'), 'Unfair accusation or child testimony never received a public resolution'
  assert state['wrong']==0, state
  assert not pg.locator('#logic-panel,#logic-note').count(), 'Separate deduction quiz returned'
  turns=pg.evaluate('window.__caseTurns')
  expected_turns=[
   '나비 씨도 갔네요. 할머니 표는 거둡니다.',
   '살아 있습니다. 살해 의심은 거둡니다.',
   '[표 변화] 세련 3 · 할머니 2 · 부녀 1',
   '두 분께 둔 표는 거둡니다. 내가 서둘렀네요.',
   '같은 도장입니다. 덜 마른 띠에 털이 눌렸죠.',
   '…제가 넣었습니다. 제 돈을 숨긴 겁니다.',
   '…노름판에서 잃었습니다. 이백 냥.',
   '…배상 요구는 거두겠습니다. 계약서도요.',
  ]
  assert all(t in turns for t in (expected_turns[-2:] if args.from_final else expected_turns)),turns
  if not args.from_final:
   assert '살아 있습니다. 살해 의심은 거둡니다.' in turns
   assert all(v=='기권' for v in turns['살아 있습니다. 살해 의심은 거둡니다.'].values()), 'Guilty votes were cast before life was confirmed'
   assert list(turns).index('살아 있습니다. 살해 의심은 거둡니다.')<list(turns).index('[잠정 투표] 할머니 5 · 기권 1 나비')
   first=list(turns[expected_turns[0]].values())
   assert first.count('innma')==4 and first.count('기권')==2,first
   middle=list(turns[expected_turns[2]].values())
   assert middle.count('seryeon')==3 and middle.count('부녀')==1,middle
   assert '부녀' not in turns[expected_turns[3]].values(),turns[expected_turns[3]]
  assert all(v=='seryeon' for v in turns[expected_turns[-1]].values()),turns[expected_turns[-1]]
  print('Actual final checkpoint: earned confession and payment withdrawal OK' if args.from_final else 'Reversals: first objection withdraws a vote; eight accepted outcomes through accusation/payment withdrawal OK',flush=True)
  if args.without_ledger:assert not pg.evaluate('(code)=>window.__T(code)', 'G.found.includes("C11")')
  audio=pg.evaluate('window.__audioSeen')
  if not args.from_final:assert audio.get('너울이 바구니를 식탁에 놓는다.',{}).get('want')=='inn_serious', 'Clinical opening lost its restrained music'
  for relationship_beat in (() if args.from_final else ('살해 의심은 거둡니다',))+('다니면서 물어볼게요',
                            '엄마 편지는 여기서 왔잖아', '우체국에도 가봐야지',
                            '엄마 찾으면 서점 다시 열자'):
   assert any(relationship_beat in t for t in audio),('Epilogue relationship missing',relationship_beat)
  print('Family epilogue: child testimony accepted, village allies and active mother search before bookstore return OK',flush=True)
  comfort=next((v for t,v in audio.items() if '다람의 손을 감싼다' in t),None)
  if not args.from_final:assert comfort and comfort['want'] is None and not comfort['tense'],('Comfort must use quiet without heartbeat',comfort)
  following=next((v for t,v in audio.items() if t.startswith('옮기기 전 일은 두 분께도')),None)
  if not args.from_final:assert following and following['want'] in ('inn_meet','inn_meet_press','inn_climax'),('Comfort quiet leaked into the next testimony',following)
  for emotional_beat in (() if args.from_final else ('엄마가 그랬어요. 겨울잠 땐',))+('두 사람 몫도 끓여',
                         '솜솜을 베개 구석에', '오늘은 아빠한테 읽어줘',
                         '다람이 먼저 한 입', '할머니가 머리판을 쓸어본다'):
   assert any(emotional_beat in t for t in audio),('Emotional payoff missing from played route',emotional_beat)
  for t,v in audio.items():
   if t.startswith(('할머니가 솜솜을 베개 구석에 눕힌다', '오늘은 아빠한테 읽어줘', '아껴 먹어', '고맙다. 같이 먹자', '(다람이 먼저 한 입')):
    assert v['want']=='inn_after' and 0<v['duck']<=.5 and not v['tense'],('Gentle epilogue cue missing',t,v)
  assert not any('빈 열세 번째 침대' in t for t in audio), 'Epilogue contradicts Somsom returning to the bed'
  print('Final segment emotional beats: winter home, sleeping guest and shared reading/snack with gentle strings OK' if args.from_final else 'Emotional beats: quiet comfort → next testimony restores music; winter home, sleeping guest and shared reading/snack all played with gentle strings OK',flush=True)
  assert audio.get('…네.',{}).get('confession'), audio.get('…네.')
  if not args.from_final:
   assert any(v['key'] for k,v in audio.items() if k.startswith('첫눈은 자정')), 'Council dialogue audio hook missing'
   assert any(v['want']=='inn_meet_press' for v in audio.values()), 'Council pressure tempo missing'
   assert any(v['cue']=='pulse' and v['want'] is None for v in audio.values()), 'Council heartbeat silence missing'
  print('Audio hooks: final confession and gentle epilogue OK' if args.from_final else 'Audio hooks: council silence/pulse/pressure and final confession OK',flush=True)
  assert not errs, errs
  assert not bad, bad
  print('RESULT',state,'errors',errs,'bad',bad,flush=True)
  print(pg.locator('body').inner_text()[-2000:],flush=True)
  pg.screenshot(path='/tmp/ch1-council.png');b.close()
