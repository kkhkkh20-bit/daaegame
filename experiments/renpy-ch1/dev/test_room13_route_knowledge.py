"""Check actual route wrappers with fresh/replay/legacy run states."""
import ast, json, textwrap, types
from pathlib import Path
root=Path(__file__).resolve().parents[1]
content=json.loads((root/'game/room13-content.json').read_text())
content['topics']['mystery:door']={}
store=types.SimpleNamespace(room13={})
env=dict(ROOM13=content,store=store,r13_available=lambda s:True,
         r13_object_visible=lambda s:True,r13_places=lambda:['room13','passage'])
source=(root/'game/room13_route_knowledge.rpy').read_text().split('init 90 python:\n')[1]
exec(textwrap.dedent(source),env)
for state,allowed in (({},False),({'secret_route_unlocked':False},False),({'secret_route_unlocked':True},True)):
 store.room13=state
 for key in ('map','passage_measure'):
  assert env['r13_available'](content['activities'][key])==allowed
 assert env['r13_available'](content['topics']['mystery:door'])==allowed
 for place,key in (('room13','books'),('kitchen','shelf'),('workshop','plans')):
  assert env['r13_object_visible'](content['objects'][place][key])==allowed
 assert ('passage' in env['r13_places']())==allowed
 assert env['r13_object_visible'](content['objects']['room13']['bed'])
# Each run starts from zero: a new run is locked even after endings were seen.
source=(root/'game/room13_rules.rpy').read_text().split('    def r13_new():\n')[1].split('\n    def ',1)[0]
persistent=types.SimpleNamespace(room13_endings=[])
exec('def new():\n'+textwrap.indent(textwrap.dedent(source),'    '),dict(ROOM13=content,persistent=persistent),local:={})
first=local['new'](); assert not first['secret_route_unlocked']
persistent.room13_endings=['ending_seen']
assert not first['secret_route_unlocked']
assert not local['new']()['secret_route_unlocked']
print('PASS: fresh / legacy route gates; new runs never inherit the route from earlier runs')
