"""Archive isolation and simultaneous known appointments from real runtime helpers."""
import copy, runpy
from pathlib import Path
n=runpy.run_path(str(Path(__file__).with_name('test_room13_review0155.py')))
e=n['env'];s=n['store'];p=n['persistent']
s.room13=dict(day=2,flags=['elder_appointment','trial_notice'],events=[],evidence=['E01'],record_ui={'favorites':[]})
p.room13_knowledge=['E01','E02']
assert e['r13_record_entries'](archive=True,favorite_only=True)==['E01','E02']
assert e['r13_record_entries'](favorite_only=True)==[]
calls=[];e['renpy'].set_screen_variable=lambda *args,**kw:calls.append((args,kw))
before=copy.deepcopy(s.room13)
e['r13_record_select']('r13_records','detail','E01',False)
assert s.room13==before and calls
assert len(e['r13_calendar_promises']())==2
s.room13['day']=5
assert len(e['r13_calendar_promises']())==1 and '7일째' in e['r13_calendar_promises']()[0]
s.room13['day']=8
assert e['r13_calendar_promises']()==[]
s.room13.update(day=13,events=['day13_warning'])
assert '14일째' in e['r13_calendar_promises']()[0]
s.room13.update(flags=[],events=[])
assert e['r13_calendar_promises']()==[]
e['r13_record_select']('r13_records','detail','E01')
assert not e['r13_record_unread']('E01')
print('PASS: archive filter and read isolation; all known appointments; past/unknown appointments absent; current record read tracking')

assert e["r13_record_mark_seen"]("E01") is None
print("PASS: automatic read action never exits its parent interaction")
