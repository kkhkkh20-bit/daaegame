"""Exercise real review wrappers across learning routes, legacy saves and replay."""
import copy
import textwrap
import types
from pathlib import Path

store=types.SimpleNamespace(room13={})
def flag(*keys):
    n=copy.deepcopy(store.room13)
    n['flags']=list(dict.fromkeys(n.get('flags',[])+list(keys)))
    store.room13=n
def encounter(person):
    store.room13.setdefault('encounters',[]).append(dict(person=person))
def prior_present(person,key,identity=False):
    if key in store.room13.get('evidence',[]) and store.room13.get('day',1)>=3:
        flag('topic:lamplighter_warning')
    return [('prior','preserved')]
e=dict(store=store,winter_copy=copy,R13_CASE_DAY=4,r13_has=lambda k:k in store.room13.get('evidence',[])+store.room13.get('flags',[]),
    r13_flag=flag,r13_note_encounter=encounter,r13_present=prior_present,r13_first_mystery_notes=lambda:[dict(title='old'),dict(title='other')],
    r13_calendar_promises=lambda:[],r13_weekday=lambda d:'토',r13_conversation_opening=lambda *a:[('prior','opening')],
    r13_conversation_topic_lines=lambda k:[('prior','historical')],r13_intro_direction_lines=lambda:[('prior','direction')],r13_intro_goal=lambda:'prior-goal',r13_home_with_daram=lambda:False)
root=Path(__file__).resolve().parents[1]
exec(textwrap.dedent((root/'game/systems/room13_review_knowledge.rpy').read_text().split('init 173 python:\n')[1]),e)
def fresh(day=1,evidence=()):
    store.room13=dict(life_poc=True,case_state='pending',day=day,evidence=list(evidence),flags=[],read_topics=[])

for item in ('M01','J04','J05'):
    for day in (1,2,3):
        fresh(day,[item]);before=copy.deepcopy(store.room13)
        e['r13_present']('resident_lamplighter',item)
        k=e['r13_mother_knowledge']()
        assert k['named'] and k['promised'] and k['pending']
        assert k['recognized']==(item=='M01')
        assert '초롱 아저씨가 엄마 봉투' in str(e['r13_intro_direction_lines']())
        assert store.room13['evidence']==before['evidence'] # no automatic letter
        assert len(e['r13_calendar_promises']())==1
        assert e['r13_first_mystery_notes']()[0]['title']!='old'
        assert e['r13_first_mystery_notes']()[1]['title']=='other'
        e['r13_present']('resident_lamplighter',item)
        assert len(store.room13['resident_knowledge']['resident_lamplighter'])==1
        # Every query must remain pure on old/new save states.
        snapshot=copy.deepcopy(store.room13)
        e['r13_mother_knowledge']();e['r13_calendar_promises']();e['r13_first_mystery_notes']()
        assert snapshot==store.room13
        store.room13['day']=3
        assert '다시 오셨군요' in str(e['r13_conversation_opening']('resident_lamplighter',False))
        assert 'topic:lamplighter_warning' in store.room13['flags']
        store.room13['read_topics']=['lamplighter_warning']
        assert e['r13_calendar_promises']()==[]
        assert '점검함' in e['r13_first_mystery_notes']()[0]['fact']
        store.room13['evidence'].append('E18')
        assert not e['r13_mother_knowledge']()['pending']
        assert e['r13_mother_note_row']() is None

fresh(1,['M01']);store.room13['resident_knowledge']={'resident_lamplighter':['M01:anonymous']}
assert e['r13_mother_knowledge']()['recognized'] # legacy presentation
assert e['r13_mother_knowledge']()['promised']
for key in ('J04','J05'):
    fresh(2,[key]);store.room13['resident_knowledge']={'resident_lamplighter':[key+':anonymous']}
    before=copy.deepcopy(store.room13)
    assert e['r13_mother_knowledge']()['promised'] and not e['r13_mother_knowledge']()['recognized']
    assert len(e['r13_calendar_promises']())==1 and store.room13==before
for evidence,flags in ((['J01'],[]),([],['mother_lamplighter_lead']),([],['poc:note_shown:karo'])):
    fresh(1,evidence);store.room13['flags']=flags
    assert e['r13_mother_knowledge']()['named'] and not e['r13_mother_knowledge']()['recognized']
fresh(1,['M01','E03']);flag('entry_corrected','lodging','portrait_lamp_seen')
assert e['r13_intro_goal']()!='prior-goal'
assert '알아봤지' in str(e['r13_intro_direction_lines']())
for key in ('J04','J05'):
    fresh(2,['M01',key]);flag('mother_lamplighter_lead')
    assert e['r13_mother_note_row']() is None # keep the more advanced witness question
    assert '봉투' in str(e['r13_intro_direction_lines']())
fresh(9);flag('mother_letter_promised','chorong_dead')
assert e['r13_calendar_promises']()==[]
fresh(8);flag('mother_letter_promised');store.room13['case_state']='occurred'
assert e['r13_calendar_promises']()==[]
fresh();before=copy.deepcopy(store.room13)
assert e['r13_present']('resident_lamplighter','M01')==[('prior','preserved')]
assert store.room13==before
fresh(5,['M01']);store.room13['case_state']='finished'
assert e['r13_present']('resident_lamplighter','M01')==[('prior','preserved')]
for key in ('L02','L03','L04','L05','L06'):
    fresh(3,[key]);assert e['r13_present']('resident_seori',key)!=[('prior','preserved')]
    assert store.room13['evidence']==[key] and store.room13['flags']==[]
fresh(3);flag('lt_dawn')
assert '내일' not in str(e['r13_conversation_topic_lines']('ep1:tok_lamps'))
store.room13['read_topics']=['ep1:tok_lamps']
assert e['r13_conversation_topic_lines']('ep1:tok_lamps')==[('prior','historical')]
print('PASS: 9 learning routes; legacy memory; calendar/notebook purity; owned-only evidence; delayed pickup; post-case delegation; five Seori responses; Tok historical replay')
