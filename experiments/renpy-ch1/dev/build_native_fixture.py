from pathlib import Path
root=Path(__file__).resolve().parents[1]
from recommended_model import r13_rec_actions
lines=['# Official RenPy 8.5.3 testcase. Unrun locally; no claim of native success.', '# Disposable CI profile only. Actual title button, actions and card UI.', 'testcase recommended_story_first_slice:', '    pause 2.0', '    click "추천 스토리 검증판 · 엄마 B / 피코 C"', '    click "새 추천 이야기 시작"', '    $ r13_rec_admin_harness=True', '    click pos (640,600) until screen "r13_recommended_actions" timeout 80', '    assert eval (r13_recommended["mother"]=="M0" and r13_recommended["day"]==2)', '    screenshot "recommended-01-entry.png"']
from opening_native import opening_clicks
entry_at=next(i for i,line in enumerate(lines) if 'assert eval' in line)
lines[entry_at:entry_at]=opening_clicks(True)+['    click "오늘을 마친다"','    click "다음 날로 간다"','    click pos (640,600) until screen "r13_recommended_actions" timeout 90']
for key in ['piko','heat','escort','repair','records','contact','delivery_wait','reply','meet','room','shelter']:
 if key=='room':lines += ['    click "저녁까지 기다린다"', '    click pos (640,600) until screen "r13_recommended_actions" timeout 40']
 lines += ['    click '+repr(r13_rec_actions[key]['title']), '    click pos (640,600) until screen "r13_recommended_actions" timeout 90']
 if key in ['contact','reply','meet','shelter']:
  expected={'contact':'M0','reply':'M1','meet':'M2','shelter':'M2'}[key]
  lines += ['    assert eval (r13_recommended["mother"]=='+repr(expected)+')', '    screenshot "recommended-'+key+'.png"']
lines+=['    assert eval ("family_shelter" in r13_recommended["done"] and r13_recommended["verdict"] is None)', '    click "오늘을 마친다"', '    click "다음 날로 간다"', '    click pos (640,600) until screen "r13_recommended_actions" timeout 40', '    assert eval (r13_recommended["piko"]=="safe" and r13_recommended["mother"]=="M2")']
for key in ['pedestal','chorong','nabi_route','child']:
 lines += ['    click '+repr(r13_rec_actions[key]['title'])]
 if key=='child':lines += ['    click pos (640,600) until screen "r13_rec_piko_intact_cloth" timeout 90','    screenshot "recommended-intact-cloth-loan.png"','    click "돌을 내려놓을 때 모습"','    screenshot "recommended-torn-cloth-delivery.png"','    click "꼬미의 이야기로 돌아간다"']
 lines += ['    click pos (640,600) until screen "r13_recommended_actions" timeout 90']
lines += ['    click "오늘을 마친다"', '    click "다음 날로 간다"', '    pause 0.5', '    click "공개 회의"', '    click pos (640,600) until screen "r13_rec_stage_choice" timeout 90', '    click "우선 들은 말과 돌의 이동부터 정리한다"', '    assert screen "r13_recommended_cards"', '    click "꼬미 · 용기의 전후 인계"', '    click pos (640,600) until screen "r13_recommended_cards" timeout 40', '    assert eval (r13_recommended["hearing"]==0)', '    screenshot "recommended-hearing-wrong.png"']
for i,caption in enumerate(['아빠와 다람 · 짧은 잔열','아이 거처의 17번 돌','꼬미 · 용기의 전후 인계']):
 lines += ['    click '+repr(caption), '    click pos (640,600) until screen '+repr('r13_recommended_actions' if i==2 else 'r13_recommended_cards')+' timeout 90']
lines+=['    assert eval (r13_recommended["verdict"]=="handoff_responsibility")', '    assert eval (r13_recommended["piko"]=="safe" and r13_recommended["mother"]=="M2" and r13_recommended["nabi"]=="supervised_relief")', '    assert eval (not room13["evidence"] and not room13["flags"])', '    screenshot "recommended-09-partial-verdict.png"', '    $ renpy.save("qa-recommended-slice")', '    $ r13_qa_note("recommended_story_first_slice: actual title, family contact/reunion/shelter, Piko escort, field cards, wrong/correct presentation. Partial handoff finding only; direct-removal art gate remains closed.")']
(root/'game/qa_tests/recommended_story.rpy').write_text('\n'.join(lines)+'\n')

p=root/"game/qa_tests/recommended_story.rpy"
field=(root/"dev/field_native_fixture.rpy").read_text()
field=field.replace('    screenshot "recommended-field-01-entry.png"','    screenshot "recommended-field-01-entry.png"'+'\n'+'\n'.join(opening_clicks(False)))
p.write_text(p.read_text()+"\n"+field)

from catalog_native import rewrite_catalog_clicks
rewrite_catalog_clicks(Path(__file__).resolve().parents[1]/"game/qa_tests/recommended_story.rpy")
