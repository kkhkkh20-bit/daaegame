"""Focused state checks for the hostile hearing, using the shipped pure helpers.

The fixtures are not browser progression. Native routes verify presentation and
real interaction separately; these tests exercise both proof orders and retries.
"""
import ast
import copy
import json
import textwrap
from pathlib import Path
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parent


def main():
    source=(ROOT/'game/council_issue.rpy').read_text().split('init 26 python:\n',1)[1].split('\nscreen ',1)[0]
    tree=ast.parse(textwrap.dedent(source))
    helpers=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[])
    issue=json.loads((ROOT/'game/council-issue.json').read_text())
    timeline=json.loads((ROOT/'game/village-state.json').read_text())
    state=SimpleNamespace(source_inventory=[],village_testimonies={},village_trust_events=[],village_trust={})
    def relationship(key,people,amount):
        if key in state.village_trust_events:return
        state.village_trust_events.append(key)
        for person in people:state.village_trust[person]=state.village_trust.get(person,-1)+amount
    env=dict(store=state,COUNCIL_ISSUE=issue,TIMELINE=timeline,village_relationship=relationship)
    exec(compile(helpers,'council_issue.rpy','exec'),env)
    env['council_reset']()
    env['council_resume']()
    assert state.council_result=='open' and not state.source_inventory
    for _ in range(3):env['council_listen']()
    assert state.council_result=='adverse' and state.council_history==['adverse']
    env['council_resume']()
    assert state.council_result=='open' and state.council_claim_index==0

    # Neither a nonexistent card nor a sympathetic hearsay statement is proof.
    assert env['council_evidence']('C01') is None
    state.source_inventory=['C01','C12']
    record=dict(id='T_V_TORI',kind='bed_context',speaker='resident_tori',claim='뜨거운 물을 받았다.',permission=False,verified=False)
    state.village_testimonies={record['id']:record}
    state.council_claim_index=2
    env['council_share_testimony'](record)
    assert state.council_claim_index==1 and not env['council_resolved']()
    assert 'private_statement_exposed' in state.council_relationship_memories['resident_tori']
    env['council_share_testimony'](record)
    assert state.council_claim_index==1 # No unlimited social reset by repetition.
    env['council_evidence']('C01')
    assert not env['council_resolved']()
    for _ in range(3):env['council_listen']()
    assert state.council_result=='adverse' and 'sealed_money' in state.council_marks
    env['council_resume']()
    env['council_evidence']('C12')
    assert env['council_resolved']() and state.council_result=='resolved'

    # An independent material route works in either order without the money pair.
    for order in (['C11','C02'],['C02','C11'],['C12','C01']):
        env['council_reset']();env['council_resume']();state.source_inventory=order
        env['council_evidence'](order[0]);assert not env['council_resolved']()
        env['council_evidence'](order[1]);assert env['council_resolved']()

    # Save data has no hidden object identities or transient screen dependencies.
    record['permission']=True
    env['council_share_testimony'](record)
    assert 'public_permission_kept' in state.council_relationship_memories['resident_tori']
    before=copy.deepcopy(state.__dict__)
    state.__dict__.update(json.loads(json.dumps(before)))
    assert state.__dict__==before and env['council_resolved']()

    # A valid, case-specific proof wins support even from an initially unfriendly
    # resident. It cannot increase influence endlessly when shown again.
    state.source_inventory=['C06']
    assert not env['council_confirm_support']('karo','C06')
    assert env['council_confirm_support']('doto','C06')
    trust=copy.deepcopy(state.village_trust)
    assert env['council_confirm_support']('doto','C06')
    assert state.village_trust==trust and state.council_confirmed_support==['doto']
    print(json.dumps(dict(empty_investigation_hearing_can_reach_adverse_result=True,
        adverse_retry_preserves_earned_material_proof=True,
        two_material_paths_work_in_either_order=True,
        unowned_cards_cannot_prove_claims=True,
        context_testimony_does_not_establish_innocence=True,
        private_exposure_and_public_permission_are_distinct_memories=True,
        repeated_context_does_not_farm_influence=True,
        all_issue_progress_and_relationship_memories_are_serializable=True,
        valid_proof_can_convince_without_friendship_threshold=True,
        repeated_support_proof_does_not_farm_trust=True),indent=2))

if __name__=='__main__':main()
