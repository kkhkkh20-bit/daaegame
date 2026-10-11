"""Guard authored dialogue against losing puzzle gates, events or private knowledge."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORIGINAL = json.loads((ROOT / 'game/chapter-source.json').read_text())['episode']
AUTHORED = json.loads((ROOT / 'game/chapter-dialogue.json').read_text())['sections']
SPEAKERS = {'det0', 'det1', 'innma', 'seryeon', 'nabi', 'geokkuri', 'doto', 'buri', 'wanggu', 'karo', '???'}


def events(value):
    result = Counter()
    if isinstance(value, dict):
        for key in ('grant', 'beat', 'fx'):
            if key in value:
                result[(key, str(value[key]))] += 1
        for child in value.values():
            result.update(events(child))
    elif isinstance(value, list):
        if len(value) > 1 and value[0] in ('@grant', '@inspect', '@dir'):
            result[(value[0], json.dumps(value[1], sort_keys=True))] += 1
        else:
            for child in value:
                result.update(events(child))
    return result


def spoken(value):
    if isinstance(value, dict):
        if value.get('w') in SPEAKERS and value.get('t'):
            yield value['w'], value['t']
        for child in value.values():
            yield from spoken(child)
    elif isinstance(value, list):
        if len(value) > 1 and isinstance(value[0], str) and isinstance(value[1], str):
            if value[0] in SPEAKERS:
                yield value[0], value[1]
        else:
            for child in value:
                yield from spoken(child)


def main():
    assert set(AUTHORED) == {'MEET', 'FINAL', 'TALK', 'END'}
    for section in ('MEET', 'FINAL'):
        before, after = ORIGINAL[section]['phases'], AUTHORED[section]['phases']
        assert len(before) == len(after)
        for old, new in zip(before, after):
            for key in ('type', 'mode', 'need', 'votes', 'q'):
                assert old.get(key) == new.get(key), (section, key)
            assert len(old.get('stms', [])) == len(new.get('stms', []))
            for a, b in zip(old.get('stms', []), new.get('stms', [])):
                for key in ('k', 'a', 'needPress'):
                    assert a.get(key) == b.get(key), (section, key)
                assert [s['ids'] for s in a.get('steps', [])] == [s['ids'] for s in b.get('steps', [])]
                assert set(a.get('wr', {})) == set(b.get('wr', {}))
                assert {k: {f: v for f, v in item.items() if f != 'lines'} for k, item in a.get('soft', {}).items()} == {
                    k: {f: v for f, v in item.items() if f != 'lines'} for k, item in b.get('soft', {}).items()}
    for person, topics in ORIGINAL['TALK'].items():
        revised = AUTHORED['TALK'][person]
        assert [{k: v for k, v in t.items() if k != 'lines'} for t in topics] == [
            {k: v for k, v in t.items() if k != 'lines'} for t in revised]
    assert events({k: ORIGINAL[k] for k in AUTHORED}) == events(AUTHORED)
    old_choice = ORIGINAL['MEET']['phases'][1]['stms'][0]['ok'][0]['ask']
    new_choice = AUTHORED['MEET']['phases'][1]['stms'][0]['ok'][0]['ask']
    assert old_choice == new_choice
    # The culprit's precise-location slip must remain a discovery the player can catch.
    early = list(spoken(AUTHORED['MEET']['phases'][:8])) + list(spoken(AUTHORED['TALK']['seryeon']))
    assert not any(w == 'seryeon' and any(word in text for word in ('침대 밑', '상자 뒤', '부인', '엄마')) for w, text in early)
    assert '침대 밑' in AUTHORED['MEET']['phases'][8]['stms'][2]['t']
    counts = {k: {'before': len(list(spoken(ORIGINAL[k]))), 'after': len(list(spoken(AUTHORED[k])))} for k in AUTHORED}
    print(json.dumps({'puzzle_gates_and_valid_alternative_proofs_preserved': True,
        'discovery_grants_and_story_events_preserved': True,
        'player_life_choice_preserved': True,
        'culprit_private_knowledge_not_leaked_before_location_trap': True,
        'spoken_packets': counts}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
