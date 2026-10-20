"""Pure, serializable state transitions for the explicitly compiled MS14 pilot.

No author guard, prose, effect string or dispatch expression is executable here.
Ren'Py owns interactions, save/load and rollback; transitions return fresh values.
"""
from copy import deepcopy


def new_state(data):
    return dict(schema=data.get('runtime_schema',1),node='start', cursor=0, values=deepcopy(data['initial']),
                presentation=dict(music_silent=False,cues=[]),
                evidence={}, applied=[], selected=[], last_record=None)


def upgrade(state, data):
    """Add declared initial fields to v1 saves; never recompute past choices/effects."""
    if state.get('schema',1) == data.get('runtime_schema',1):
        return state
    if state.get('schema',1) != 1 or data.get('runtime_schema',1) != 2:
        raise ValueError('Unsupported MS14 save schema')
    out=deepcopy(state)
    for key,value in data['initial'].items():
        if key not in out['values']:out['values'][key]=deepcopy(value)
    out.setdefault('presentation',dict(music_silent=False,cues=[]))
    out['schema']=2
    return out


def silence(state):
    out=deepcopy(state)
    presentation=out.setdefault('presentation',dict(music_silent=False,cues=[]))
    cue='MS14_D05_S04_L0006:first_sentence_done'
    if cue not in presentation['cues']:presentation['cues'].append(cue)
    presentation['music_silent']=True
    return out


def warning_parts(text):
    anchor='당신과 다람이를 부른 적 없어.'
    if not text.startswith('“'+anchor):raise ValueError('Warning anchor changed')
    index=len('“'+anchor)
    return text[:index],text[index:]


def presentable(data, state, key):
    """Private documents can be picked only for the family's private comparison."""
    if key not in state['evidence']:return False
    return not data['evidence'][key].get('private',False) or state['node']=='d5_warning_compare'


def branch_target(state, node):
    if node['field'] not in state['values']:
        raise ValueError('Missing compiled branch field: '+node['field'])
    value=state['values'][node['field']]
    if value==node['value']:return node['yes']
    if 'otherwise_value' in node and value!=node['otherwise_value']:
        raise ValueError('No authored branch for '+node['field']+'='+str(value))
    return node['no']


def allowed(state, guards):
    for kind, key, expected in guards:
        if kind == 'evidence':
            value = key in state['evidence']
        elif kind == 'state':
            if key not in state['values']:
                raise ValueError('Missing compiled state field: '+key)
            value = state['values'][key]
        else:
            raise ValueError('Unknown compiled guard: '+kind)
        if value != expected:
            return False
    return True


def apply(state, event_id, operations):
    if event_id in state['applied']:
        return state
    out = deepcopy(state)
    for operation in operations:
        if operation['op'] == 'set':
            out['values'][operation['field']] = operation['value']
        elif operation['op'] == 'acquire':
            out['evidence'][operation['key']] = operation['variant']
        else:
            raise ValueError('Unknown compiled operation: '+operation['op'])
    out['applied'].append(event_id)
    return out


def enter(state, node):
    out = deepcopy(state)
    out.update(node=node, cursor=0, selected=[])
    return out


def finish_record(state, record):
    out = deepcopy(apply(state, record['id'], record['operations']))
    out['cursor'] += 1
    out['last_record'] = record['id']
    return out


def choose(state, node, index):
    option = node['options'][index]
    if not allowed(state, option['guard']):
        raise ValueError('Unavailable input')
    out = apply(state, state['node']+':choice:'+str(index), option['operations'])
    return enter(out, option['to'])


def select(state, key):
    if key not in state['evidence']:
        raise ValueError('Unacquired evidence: '+key)
    out = deepcopy(state)
    if key in out['selected']:
        out['selected'].remove(key)
    else:
        out['selected'].append(key)
    return out


def submit(state, node):
    if not set(node['requires']) <= state['evidence'].keys():
        raise ValueError('Missing proof prerequisites')
    picked = set(state['selected'])
    if picked == set(node['correct']) and picked <= state['evidence'].keys():
        return enter(state, node['to'])
    wrong = node.get('wrong_routes', {}).get(','.join(sorted(picked)), node['wrong'])
    return enter(state, wrong) if wrong else state


def observed(data, state, key):
    """A read-only view: even variant evidence never reads a mutable global cache."""
    if key not in state['evidence']:
        return None
    spec = data['evidence'][key]
    variant = state['evidence'][key]
    text = spec['variants'].get(variant)
    if text is None:
        raise ValueError('Missing evidence variant: '+key+':'+variant)
    name = spec['name']
    if key == 'E09':
        status = state['values']['portrait']
        name = {'complete':'엄마의 완성 초상', 'unfinished':'엄마의 미완성 초상',
                'child_completed':'다람이 코를 그린 초상'}[status]
    if key == 'E35':
        received = state['values'].get('E35.status') == 'received'
        name = '가족 침구 수령 기록' if received else '가족 침구 예약'
        if received:
            text = '예약한 마른 담요 두 장을 네로에게서 실제로 받아 여행가방에 넣었다.'
    return dict(id='MS14:'+key, name=name, kind=spec['kind'], establishes=text,
                does_not_establish='', current_run_only=True, retained_on_show=True,
                scenes=[])


def validate(data):
    """Reject incomplete routing rather than silently playing the next array item."""
    nodes = data['nodes']
    targets = []
    kinds = {'block','choice','proof','branch','read','mark','notebook','end'}
    for key, node in nodes.items():
        if node['kind'] not in kinds:
            raise ValueError('Unknown node '+key)
        if node['kind'] == 'block':
            for rid in node['records']:
                record = data['records'][rid]
                if record.get('requires'):
                    raise ValueError('Uncompiled record prerequisite '+rid)
        for field in ('next','to','yes','no','wrong','hint'):
            if node.get(field): targets.append(node[field])
        targets.extend(o['to'] for o in node.get('options', []))
        targets.extend(node.get('wrong_routes', {}).values())
    missing = set(targets)-nodes.keys()
    if missing:
        raise ValueError('Missing compiled routes: '+str(sorted(missing)))
    return True
