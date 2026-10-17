"""All-skip works with fresh preferences and returns the original preference."""
import ast,types,textwrap
from pathlib import Path
source=(Path(__file__).resolve().parents[1]/'game/room13_ui_flow.rpy').read_text().split('init 99 python:\n',1)[1]
names={'r13_sync_skip_unseen','r13_toggle_read_skip','r13_toggle_fast_all','r13_end_skip_modes','r13_stop_skip_at_choices'}
tree=ast.parse(textwrap.dedent(source))
functions=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[])
s=types.SimpleNamespace(room13_mode=True,r13_fast_all=False,r13_fast_read=False,r13_read_id='read')
pref=types.SimpleNamespace(skip_unseen=False)
config=types.SimpleNamespace(skipping=None)
screens=set()
renpy=types.SimpleNamespace(config=config,stop_skipping=lambda:setattr(config,'skipping',None),restart_interaction=lambda:None,notify=lambda x:None,get_screen=lambda n:n in screens)
e=dict(store=s,preferences=pref,renpy=renpy,persistent=types.SimpleNamespace(room13_read=['read']))
exec(compile(functions,'skip-helpers','exec'),e)
for original in (False,True):
 for destination in ('choice','r13_topics','r13_book','r13_debate_board','r13_meeting_agenda','pause_menu','save','load','main_menu','confirm'):
  pref.skip_unseen=original;screens.clear()
  e['r13_toggle_fast_all']();assert s.r13_fast_all and pref.skip_unseen and config.skipping=='slow'
  e['r13_sync_skip_unseen']();assert getattr(renpy,'_r13_skip_unseen_before',None)==original
  screens.add(destination);e['r13_stop_skip_at_choices']()
  assert not s.r13_fast_all and pref.skip_unseen==original and getattr(renpy,'_r13_skip_unseen_before',None) is None
 pref.skip_unseen=original;screens.clear()
 e['r13_toggle_fast_all']();e['r13_toggle_read_skip']()
 assert pref.skip_unseen==original and s.r13_fast_read and not s.r13_fast_all
 e['r13_end_skip_modes']()
 e['r13_toggle_fast_all']();s.r13_fast_all=False;e['r13_stop_skip_at_choices']()
 assert pref.skip_unseen==original and getattr(renpy,'_r13_skip_unseen_before',None) is None
print('PASS: all-skip crosses unread lines; ten choice/menu boundaries restore both original preferences; read-only mode and external stops restore the preference')
