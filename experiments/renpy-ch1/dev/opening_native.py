"""Actual click path for the independent day-one opening. Native execution pending."""
def opening_clicks(admin=False):
 screen='r13_recommended_actions' if admin else 'r13_recommended_field'
 lines=[]
 def act(subject,title,after=screen):
  if not admin:lines.append('    click '+repr(subject))
  lines.append('    click '+repr(title))
  lines.append('    click pos (640,600) until screen '+repr(after)+' timeout 90')
 act('돌목','돌목에게 두 사람의 입장 확인을 부탁한다')
 act('초소 서류 선반','초소 선반에서 오늘 날짜의 신청 원본을 찾는다')
 act('돌목','돌목에게 원본과 방문 목록을 나란히 보여 준다','r13_recommended_cards')
 lines.extend(['    click "방문 신청 원본"','    click "돌목이 옮겨 쓴 방문 목록"',
  '    click pos (640,600) until screen '+repr(screen)+' timeout 90',
  '    assert eval ("entry_cleared" in r13_recommended["done"])'])
 if not admin:lines.extend(['    click "지도 · 이동"','    click "여관 접수대"'])
 act('나비','까로와 짐을 옮겨 여관에서 엄마를 찾는다')
 lines.append('    assert eval (r13_recommended["day"]==1 and "entry_inn_arrived" in r13_recommended["done"])')
 return lines
