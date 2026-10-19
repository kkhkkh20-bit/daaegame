"""Independent day-one entry. No legacy event or forged-letter facts are imported."""
r13_rec_cards.update({
 'entry_list':('돌목이 옮겨 쓴 방문 목록','1일 입구에서 돌목이 직접 펼쳐 보였다. 다돌, 총 인원 1명으로 적혀 있다. 누가 일부러 바꿨다는 근거는 없다.'),
 'entry_original':('방문 신청 원본','1일 초소 선반에서 찾은 같은 날짜 원본. 신청한 사람 다돌과 동행 한 명, 모두 2명으로 적혀 있다.'),
 'entry_karo':('까로 · 함께 타고 온 두 사람','1일 입구에서 직접 들었다. 아빠와 다람을 함께 태워 왔고, 도착해 두 사람의 짐을 내렸다. 예약 원본은 초소 선반에 넘겼다.'),
})
r13_rec_identity_groups.update({
 'entry_list':('physical','입구 방문 목록',('entry_list',)),
 'entry_original':('physical','초소 선반의 신청서',('entry_original',)),
 'karo':('person','까로',('entry_karo',)),
})
r13_rec_actions.update({
 'entry_report':r13_rec_action('돌목에게 두 사람의 입장 확인을 부탁한다','gate',[
 ('guard','다돌 님 맞습니까? 제 목록에는 한 분만 적혀 있습니다.'),('dad','네, 하지만 딸과 함께 두 명으로 신청했어요. 다람아, 아빠 곁에 있어.'),('daram','제 이름은 다람이에요. 엄마 만나러 같이 왔어요.'),
 ('dad','어디가 다르게 적혔는지 보여 주시겠어요?'),(None,'돌목이 방문 목록을 펼쳤다. 다돌, 총 인원 1명이라고 적혀 있었다.'),('guard','원본을 보고 옮겨 적은 겁니다. 확인 전에는 두 분 모두 초소 앞에서 기다려 주세요. 원본은 저 선반에 있습니다.'),('dad','담당자를 기다리기만 할 필요는 없겠군요. 다람아, 같이 찾아보자.')],give=('entry_list',),day=1,target_person='guard'),
 'entry_karo':r13_rec_action('까로에게 원본을 어디에 두었는지 묻는다','gate',[
 ('dad','아이 이름이 목록에서 빠졌어요. 저희가 낸 원본은 어디에 있습니까?'),('karo','두 분 다 제 마차로 오셨지요. 원본은 아까 초소에 넘겼어요. 선반의 오늘 도착한 서류 묶음에 넣더군요.'),('dad','고맙습니다. 그 묶음부터 볼게요.')],need=('entry_report',),give=('entry_karo',),day=1,target_person='karo'),
 'entry_original':r13_rec_action('초소 선반에서 오늘 날짜의 신청 원본을 찾는다','gate',[
 (None,'선반에 도착 날짜별로 묶인 서류가 있었다. 아빠가 오늘 날짜와 자기 이름을 맞춰 원본을 꺼냈다.'),('daram','아빠 이름 옆에도 적혀 있어. 같이 오는 사람 한 명!'),('dad','그래. 모두 두 명이네. 돌목 씨가 보여 준 목록과 같이 보여 드리자.')],need=('entry_report',),give=('entry_original',),day=1,target_object='초소 서류 선반'),
 'entry_present':r13_rec_action('돌목에게 원본과 방문 목록을 나란히 보여 준다','gate',[],need=('entry_report','entry_original'),flags=('entry_cleared',),day=1,target_person='guard',label='r13_recommended_entry_present'),
 'entry_inn':r13_rec_action('까로와 짐을 옮겨 여관에서 엄마를 찾는다','inn',[
 ('karo','짐은 제가 여관까지 옮길게요. 축에 금이 간 마차는 여기 세워 두어야겠네요.'),('daram','작은 가방은 내가 들게. 엄마 만나면 과자도 줄 거야.'),('dad','고마워. 같이 들어가자.'),
 ('dad','아내가 여기서 만나자고 편지를 보냈습니다. 지금 어디 계신가요?'),('nabi','수리점의 부리 씨에게 다녀오셨다고 들었어요. 지금 여관에는 안 계세요.'),('daram','편지에는 여기서 기다린다고 했는데...'),('dad','오는 동안 무슨 일이 바뀌었는지 알아보자. 부리 씨께 어디로 가셨는지 물어보면 되겠네.')],need=('entry_cleared',),flags=('entry_inn_arrived',),day=1,target_person='nabi'),
})

def r13_rec_opening_state():
 s=r13_rec_new_state();s.update(day=1,period=0,location='gate',entry_pending=True)
 return s

def r13_rec_opening_present(s,selected):
 if not set(selected)<=set(s['facts']):raise ValueError('Cannot present unearned entry evidence')
 return set(selected)=={'entry_list','entry_original'}

_r13_rec_available_before_entry=r13_rec_available
def r13_rec_available(s):
 rows=_r13_rec_available_before_entry(s)
 if s.get('entry_pending') and 'entry_inn_arrived' not in s['done']:
  if 'entry_cleared' in s['done']:return [row for row in rows if row[0]=='entry_inn']
  return [row for row in rows if row[0].startswith('entry_')]
 return rows

_r13_rec_block_before_entry=r13_rec_block_reason
def r13_rec_block_reason(s):
 if s['day']==1:
  if 'entry_inn_arrived' not in s['done']:return '입장 확인을 마치고 여관에서 엄마 소식부터 묻자.'
  return None
 return _r13_rec_block_before_entry(s)

_r13_rec_day_before_entry=r13_rec_next_day
def r13_rec_next_day(s):
 if s['day']!=1:return _r13_rec_day_before_entry(s)
 reason=r13_rec_block_reason(s)
 if reason:raise ValueError(reason)
 n=copy.deepcopy(s);n.update(day=2,period=0)
 return r13_rec_validate_transition(s,n)

_r13_rec_card_episode_before_entry=r13_rec_card_episode
def r13_rec_card_episode(key):
 return 0 if key.startswith('entry_') or key=='family_travel' else _r13_rec_card_episode_before_entry(key)

r13_rec_cards['family_travel']=('까로 · 함께 떠날 길의 현재 상태','가족이 직접 까로에게 확인한 현재 이동 조건. 마차 축에 금이 가 손님을 태울 수 없고, 고갯길은 폭설로 막혀 있다. 수리나 개통을 확인한 사실은 아직 없다.')
r13_rec_identity_groups['karo']=('person','까로',('entry_karo','family_travel'))
r13_rec_actions['family_route']=r13_rec_action('까로에게 가족이 함께 떠날 수 있는지 확인한다','gate',[
 ('dad','아내와 만났습니다. 이제 셋이 함께 움직일 수 있어요. 마차로 돌아갈 수 있습니까?'),
 ('karo','축에 금이 간 채라 사람을 태울 수는 없어요. 고개도 폭설로 막혔고요. 마차만 고쳐도 바로 출발할 수 있는 건 아닙니다.'),
 ('dad','그럼 차축 수리와 고갯길, 둘 다 확인해야겠군요. 길이 열렸는지 모른 채 아이를 데리고 나서지는 않을게요.'),
 ('karo','수리나 길 사정이 달라지면 여관으로 알려 드릴게요. 출발 전에 저와 함께 다시 확인합시다.'),
 ('mom','오늘 쉴 곳은 같이 챙기고, 돌아갈 길도 같이 알아보자.')],need=('reunited',),give=('family_travel',),flags=('family_route_checked',),episode=0,target_person='karo')


def r13_rec_main_objective(s):
 if s.get('entry_pending') and 'entry_inn_arrived' not in s['done']:
  return '먼저 함께 입장하고 여관에서 엄마를 찾자.'
 if s['mother']=='M0':return '엄마의 마지막 방문을 따라가서, 우리가 도착했다고 전하자.'
 if s['mother']=='M1':
  return '오늘 답을 다시 확인하고 만나자.' if s.get('observed',{}).get('reply')!=s['day'] else '엄마가 답한 공개 자리에서 직접 만나자.'
 if 'family_shelter' not in s['done']:return '엄마와 만났다. 셋이 오늘 안전하게 잘 자리와 식사를 확인하자.'
 if 'family_route_checked' not in s['done']:return '오늘 함께 쉴 곳은 있다. 까로에게 셋이 떠날 수 있는지 물어보자.'
 return '마차 축과 눈에 막힌 고갯길을 확인했다. 가족의 안전을 지키며 실제 출발 조건을 마련하자. 아직 개통·수리 완료는 확인하지 못했다.'
