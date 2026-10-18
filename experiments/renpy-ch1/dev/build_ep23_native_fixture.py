"""Prepare native UI tests. Requires official RenPy runner. Not executed here."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
g={}
exec((root/'dev/recommended_model.py').read_text(),g)
exec((root/'dev/recommended_ep23_model.py').read_text(),g)
a=g['r13_rec_actions'];cards=g['r13_rec_cards']
lines=['# Native fixtures only. No native execution or screenshots claimed by generation.', '# The field test clicks actual locations, NPC/object subjects, questions and hearings.', '# Direct-entry boot seeds M2/Piko-safe/Nabi supervised; it does not claim earlier gameplay.', 'testcase recommended_ep2_field_and_hearing:', '    pause 2.0', '    $ r13_rec_admin_harness=False', '    run Call("r13_recommended_ep2_admin")', '    click pos (640,600) until screen "r13_recommended_field" timeout 40', '    click "지도 · 이동"', '    click "눈에 막힌 입구"', '    pause 0.5']
def action(key,field=True):
 if field:
  spec=a[key];target=spec.get('target_person')
  captions={'guard':'돌목','resident_somi':'솜이','bami':'밤이','resident_badook':'바둑이'}
  lines.append('    click '+repr(captions.get(target,spec.get('target_object'))))
  lines.append('    assert screen "r13_recommended_subject"')
 lines.extend(['    click '+repr(a[key]['title']), '    click pos (640,600) until screen '+repr('r13_recommended_field' if field else 'r13_recommended_actions')+' timeout 100'])
action('e2_report')
lines+=['    screenshot "recommended-e2-01-reported.png"','    click "오늘을 마친다"','    click "다음 날로 간다"','    click pos (640,600) until screen "r13_recommended_field" timeout 50']
for key in ['e2_rail','e2_ties','e2_somi','e2_bami','e2_badook']:action(key)
lines+=['    assert eval ("e2_card_badook" in r13_recommended["facts"] and not r13_recommended["episodes"]["2"]["bite_admitted"])','    screenshot "recommended-e2-02-before-hearing.png"','    click "약속한 회의에 간다"','    click pos (640,600) until screen "r13_rec_stage_choice" timeout 80','    click "이름·거처 비공개를 회의 규칙으로 정하고, 밤이가 답할지 고르게 한다"','    click pos (640,600) until screen "r13_recommended_cards" timeout 80','    assert eval (r13_recommended["episodes"]["2"]["bite_admitted"])','    click '+repr(cards['e2_card_somi'][0]),'    click pos (640,600) until screen "r13_recommended_cards" timeout 80','    assert eval (r13_recommended["episodes"]["2"]["stage"]==0)','    screenshot "recommended-e2-03-wrong-card.png"']
for i,c in enumerate(['e2_card_rail','e2_card_badook','e2_card_ties','e2_card_dolmok']):
 lines+=['    click '+repr(cards[c][0]),'    click pos (640,600) until screen '+repr('r13_rec_stage_choice' if i==3 else 'r13_recommended_cards')+' timeout 100']
lines+=['    click "결박 → 풀라는 요구 → 수레 안으로 뻗은 팔 → 밤이의 물림"','    click pos (640,600) until screen "r13_recommended_field" timeout 100','    assert eval (r13_recommended["episodes"]["2"]["verdict"]=="bite_and_prior_coercion")','    assert eval (r13_recommended["mother"]=="M2" and r13_recommended["piko"]=="safe")','    screenshot "recommended-e2-04-consequence.png"','    $ r13_qa_note("recommended_ep2_field_and_hearing: real map, actor/object, question, anonymity, wrong/correct card and order clicks. Initial M2/Piko-safe state is a disclosed fixture.")','']
lines+=['# Separate admin-action harness: tests dialogue/actions + evidence/map, not physical hotspot navigation.','testcase recommended_ep3_prevention_map:', '    pause 2.0','    $ r13_rec_admin_harness=True','    run Call("r13_recommended_ep3_admin")','    click pos (640,600) until screen "r13_recommended_actions" timeout 40']
for key in ['e3_bowls','e3_meet_children','e3_school_place','e3_handoff']:action(key,False)
lines+=['    assert eval (r13_recommended["e3_school_handoff"] and r13_recommended["episodes"]["3"]["children"]=="school")','    screenshot "recommended-e3-01-actual-school-handoff.png"','    click "오늘을 마친다"','    click "다음 날로 간다"','    click pos (640,600) until screen "r13_recommended_actions" timeout 50']
for key in ['e3_outcome_safe','e3_wall','e3_bori_safe','e3_layout','e3_teacher','e3_can','e3_nubi','e3_child_boundary','e3_child_support']:action(key,False)
lines+=['    assert eval (r13_recommended["episodes"]["3"]["kkomi"]=="alive")','    assert eval ("e3_card_child" not in r13_recommended["facts"])','    click "공개 회의"','    click pos (640,600) until screen "r13_rec_stage_choice" timeout 80','    click "보호자 동석·이름 비공개로, 아이가 동의한 관찰만 듣는다"','    click pos (640,600) until screen "r13_recommended_cards" timeout 100']
for i,c in enumerate(['e3_card_wall','e3_card_teacher','e3_card_can']):
 lines+=['    click '+repr(cards[c][0]),'    click pos (640,600) until screen '+repr('r13_rec_e3_route_map' if i==2 else 'r13_recommended_cards')+' timeout 100']
lines+=['    screenshot "recommended-e3-02-proposed-sightline-map.png"','    click "L"','    click pos (640,600) until screen "r13_rec_e3_route_map" timeout 60','    assert eval (r13_recommended["episodes"]["3"]["map_step"]==0)']
for i,caption in enumerate(['W','L','큰아이 · L–M','선생님 · M–W',None]):
 lines+=[('    click pos (656,428)' if caption is None else '    click '+repr(caption)),'    click pos (640,600) until screen '+repr('r13_recommended_cards' if i==4 else 'r13_rec_e3_route_map')+' timeout 100']
lines+=['    click '+repr(cards['e3_card_nubi'][0]),'    click pos (640,600) until screen "r13_recommended_actions" timeout 100','    assert eval (r13_recommended["episodes"]["3"]["verdict"]=="partial_geometry_unverified")','    assert eval (r13_recommended["episodes"]["3"]["kkomi"]=="alive" and r13_recommended["e3_school_handoff"])','    screenshot "recommended-e3-03-honest-partial-result.png"','    $ r13_qa_note("recommended_ep3_prevention_map: admin action harness for actual school handoff and safe branch; native evidence and map clicks, wrong can endpoint rejected; default production geometry gate remains closed. This is not proof of actual sightline art.")']
(root/'game/qa_tests/recommended_ep23.rpy').write_text('\n'.join(lines)+'\n')
print('Prepared native fixture; execution still pending.')

from catalog_native import rewrite_catalog_clicks
rewrite_catalog_clicks(Path(__file__).resolve().parents[1]/"game/qa_tests/recommended_ep23.rpy")
