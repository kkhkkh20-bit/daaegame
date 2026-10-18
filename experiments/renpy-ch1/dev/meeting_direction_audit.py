"""Static presentation inventory; never a campaign replay or runtime cast assertion.

Reads only authored assignments, using the same seat ordering as the cast builders.
Run: python3 dev/meeting_direction_audit.py > docs/reviews/meeting-direction-20261017/inventory.json
"""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def init_nodes(path):
    raw = path.read_text().split(' python:\n', 1)[1]
    lines = []
    for line in raw.splitlines():
        if line and not line.startswith((' ', '#')):
            break
        lines.append(line[4:] if line.startswith('    ') else line)
    return ast.parse('\n'.join(lines)).body


def authored_data():
    env = dict(R13_DEBATE={}, R13_DEBATE_SEATS={}, R13_EP_MEETING_PLACE={}, R13_MEETING_VENUES={})
    files = [ROOT/'game/systems/room13_debate.rpy',
             ROOT/'game/room13_meeting_seating.rpy',
             *sorted((ROOT/'game/systems').glob('room13_ep[1-6]_*.rpy'))]
    for path in files:
        for node in init_nodes(path):
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            target = node.targets[0]
            base = (target.value.id if isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name)
                    else target.id if isinstance(target, ast.Name) else '')
            if base in env:
                exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), 'exec'), env)
    return env


def inventory():
    env = authored_data()
    art = json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people']
    results = []
    for claim, spec in env['R13_DEBATE'].items():
        session = spec.get('session', 'trial' if claim.startswith('C') else 'finale')
        venue = env['R13_MEETING_VENUES'][session]
        extra = ['granny', 'resident_seori'] if session == 'trial' else ['mom'] if session == 'finale' else []
        # Static superset: runtime visibility, POV and story gates remain authoritative.
        seats = list(dict.fromkeys(env['R13_DEBATE_SEATS'][session] + extra +
                                  [s['who'] for s in spec['statements']] + [spec['chair']]))
        people = []
        for person in seats:
            profile = art.get(person, {}).get('profiles', {}).get('840', {})
            frames = profile.get('frames', {})
            people.append(dict(person=person, approved=art.get(person, {}).get('status') == 'approved_runtime',
                               frames=list(frames), missing_files=[f['file'] for f in frames.values()
                                                                 if not (ROOT/'game'/f['file']).is_file()],
                               source_gaze=art.get(person, {}).get('gaze'),
                               source_stance=art.get(person, {}).get('stance')))
        results.append(dict(claim=claim, title=spec['title'], session=session, venue=venue,
                            close_height=840 if venue[1] in ('round', 'stone') else 740,
                            table_occlusion=venue[1] in ('round', 'stone'), people=people,
                            statements=[dict(id=s['id'], speaker=s['who'], text=s['text'],
                                             evidence=s.get('accept', []), counter=bool(s.get('counter')))
                                        for s in spec['statements']]))
    return dict(kind='static authored superset; NOT engine capture or natural progression', meetings=results)


if __name__ == '__main__':
    print(json.dumps(inventory(), ensure_ascii=False, indent=2))
