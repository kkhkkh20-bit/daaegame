"""Exercise real review wrappers across learning routes, legacy saves and replay."""
import copy
import ast
import json
import r13_timeline_env  # Actual calendar constants, shared with the production init blocks.
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
    # Pure fallback only: no synthetic day-three unlock may mask init97/100/173.
    return [('prior','preserved')]
e=dict(store=store,winter_copy=copy,R13_CASE_DAY=r13_timeline_env._ns['R13_CASE_DAY'],r13_has=lambda k:k in store.room13.get('evidence',[])+store.room13.get('flags',[]),
    r13_flag=flag,r13_note_encounter=encounter,r13_present=prior_present,r13_first_mystery_notes=lambda:[dict(title='old'),dict(title='other')],
    r13_calendar_promises=lambda:[],r13_weekday=lambda d:'토',r13_conversation_opening=lambda *a:[('prior','opening')],
    r13_conversation_topic_lines=lambda k:[('prior','historical')],r13_intro_direction_lines=lambda:[('prior','direction')],r13_intro_goal=lambda:'prior-goal',r13_home_with_daram=lambda:False)
root=Path(__file__).resolve().parents[1]
# Load the actual earlier presentation layers in production order. Unrelated UI
# and economy endpoints are stubs; the tested unlocks and replies are not.
e.update(ROOM13=json.loads((root/'game/room13-content.json').read_text()),R13_RECORD_SHORT={},
    r13_compare_result=lambda selected:'prior-comparison',r13_topics=lambda person:[],
    r13_campaign_goal=lambda:'prior-goal',r13_learning_job_context=lambda *a:'prior-job',
    r13_wallet=lambda state=None:{'jobs':[]})
# Keep the actual init94 memo definition and presentation layer. This contains
# the historical day-three behavior that the final review layer must override.
firstday=ast.parse(textwrap.dedent((root/'game/systems/room13_first_day_flow.rpy').read_text().split('init 94 python:\n')[1].split('\nlabel ')[0]))
for node in firstday.body:
    code=ast.unparse(node)
    if (isinstance(node,ast.FunctionDef) and node.name=='r13_present') or code.startswith("ROOM13['evidence']['M01'] =") or code.startswith('_r13_life_present ='):
        exec(compile(ast.Module(body=[node],type_ignores=[]),'actual-firstday-presentation','exec'),e)
exec(textwrap.dedent((root/'game/systems/room13_intro_clues.rpy').read_text().split('init 97 python:\n')[1].split('\nscreen r13_entry_daram_topics():')[0]),e)
exec(textwrap.dedent((root/'game/systems/room13_poc_route.rpy').read_text().split('init 100 python:\n')[1].split('\nlabel r13_poc_night_review:')[0]),e)
exec(textwrap.dedent((root/'game/systems/room13_review_knowledge.rpy').read_text().split('init 173 python:\n')[1]),e)
def fresh(day=1,evidence=()):
    store.room13=dict(life_poc=True,case_state='pending',day=day,evidence=list(evidence),flags=[],read_topics=[])

for item in ('M01','J04','J05'):
    for day in (1,2,3):
        fresh(day,[item]);before=copy.deepcopy(store.room13)
        e['r13_present']('resident_lamplighter',item)
        k=e['r13_mother_knowledge']()
        assert k['named'] and k['promised'] and not k['pending']
        assert 'warning_location' in store.room13['flags']
        assert 'topic:lamplighter_warning' in store.room13['flags']
        assert 'lamplighter_warning' not in store.room13['read_topics']
        assert k['recognized']==(item=='M01')
        assert '초롱 아저씨가 엄마 봉투' in str(e['r13_intro_direction_lines']())
        assert store.room13['evidence']==before['evidence'] # no automatic letter
        assert e['r13_calendar_promises']()==[]
        assert e['r13_first_mystery_notes']()[0]['title']!='old'
        assert e['r13_first_mystery_notes']()[1]['title']=='other'
        e['r13_present']('resident_lamplighter',item)
        assert len(store.room13['resident_knowledge']['resident_lamplighter'])==1
        # Every query must remain pure on old/new save states.
        snapshot=copy.deepcopy(store.room13)
        e['r13_mother_knowledge']();e['r13_calendar_promises']();e['r13_first_mystery_notes']()
        assert snapshot==store.room13
        # Location was already delivered today; opening must not invent a second wait.
        snapshot=copy.deepcopy(store.room13)
        assert e['r13_conversation_opening']('resident_lamplighter',False)==[('prior','opening')]
        assert store.room13==snapshot
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
assert e['r13_mother_knowledge']()['pending']
assert 'warning_location' not in store.room13['flags']
for key in ('M01','J04','J05'):
    fresh(2,[key]);store.room13['resident_knowledge']={'resident_lamplighter':[key+':anonymous']}
    before=copy.deepcopy(store.room13)
    assert e['r13_mother_knowledge']()['promised']
    assert e['r13_mother_knowledge']()['recognized']==(key=='M01')
    assert len(e['r13_calendar_promises']())==1 and store.room13==before
    assert e['r13_mother_knowledge']()['pending']
    assert 'warning_location' not in store.room13['flags']
    rows=e['r13_conversation_opening']('resident_lamplighter',False)
    assert '점검함' in str(rows) and '내일' not in str(rows)
    assert 'warning_location' in store.room13['flags']
    assert 'topic:lamplighter_warning' in store.room13['flags']
    assert not e['r13_mother_knowledge']()['pending']
    assert e['r13_calendar_promises']()==[]
    assert store.room13['evidence']==before['evidence']
    assert store.room13['read_topics']==before['read_topics']
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
for changes in ({'day':5,'case_state':'finished'},{'day':2,'life_poc':False},{'day':8,'case_state':'occurred'}):
    fresh(2,['M01']);store.room13.update(changes);before=copy.deepcopy(store.room13)
    expected=e['_r13_review_present']('resident_lamplighter','M01');expected_state=copy.deepcopy(store.room13)
    store.room13=before
    assert e['r13_present']('resident_lamplighter','M01')==expected
    assert store.room13==expected_state # later/legacy routes retain their real prior behavior
    assert 'warning_location' not in store.room13['flags']
for key in ('L02','L03','L04','L05','L06'):
    fresh(3,[key]);assert e['r13_present']('resident_seori',key)!=[('prior','preserved')]
    assert store.room13['evidence']==[key] and store.room13['flags']==[]
fresh(3);flag('lt_dawn')
assert '내일' not in str(e['r13_conversation_topic_lines']('ep1:tok_lamps'))
store.room13['read_topics']=['ep1:tok_lamps']
assert e['r13_conversation_topic_lines']('ep1:tok_lamps')==[('prior','historical')]
print('PASS: 9 actual init94/97/100/173 same-day learning routes; legacy pending until live opening; calendar/notebook purity; owned-only evidence; no automatic pickup; post-case delegation; five Seori responses; Tok historical replay')

