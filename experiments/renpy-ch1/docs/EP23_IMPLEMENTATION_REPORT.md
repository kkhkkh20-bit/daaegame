> Later integration update: the abstract diagnostic strip has been replaced with exact night-v3 panorama and source-aligned L/M/W, witness and overlap interactions. Both day/night v3 sources passed static review. Source/native flags are now separate; native remains False. See SCENE_GEOMETRY_REVIEW.md and NATIVE_QA_PROMOTION_CHECKLIST.md. The original implementation checkpoint below is retained as history, not the current art status.

# Episodes 2 C and 3 A implementation report

Status: source integration delivered, pure transition regression passed. Native RenPy rendering/click execution and production-art sightline verification are not yet performed. This report is not a claim that the campaign or fire identity proof is finished.

## Owned files

- game/systems/room13_recommended_ep23.rpy: independent init 910 plugin, investigation actions, hearings, route-map screen, isolated direct-entry QA labels.
- dev/recommended_ep23_model.py: pure state transitions and episode-specific source data.
- dev/recommended_ep23_ui.rpy: RenPy labels and screen source.
- dev/build_ep23.py: deterministic model + UI generation.
- dev/test_recommended_ep23.py: 38 source/state tests.
- docs/EP23_SOURCE_TEST_RESULTS.txt: captured executed output.
- dev/build_ep23_native_fixture.py and game/qa_tests/recommended_ep23.rpy: prepared, not yet executed native field/hearing and prevention/map tests.

No common files or remote repository writes were performed by this worker. Common action location, character/object click targets, background_key rendering and card selectors are the integrator's ownership.

## Implemented story flow

Episode 2 starts on day 4 and hears the report. Day 5 investigations unlock only from already learned facts: report mentions cart; rail reveals inside reach; Somi recognizes blanket; Bami names the cart attendant; Badook gives the restraint and release-request observation before the hearing. The hearing establishes anonymity before a voluntary admission, or respects silence and records an honest contact-unconfirmed result. The player's card submissions rebut Dolmok's new sequence and blanket-only explanation; a separate order choice connects restraint, request, reach and bite. Both Bami's bite and prior coercion remain distinct. The scene visibly stops isolation and cart movement. Optional actual care handoff is not payment for testimony.

Episode 3 begins on day 5 after the second hearing, preserving an explicit pre-sunset prevention opportunity. Four bowls reveal four named registered children; the player meets them, checks school heat/bedding/food/staff, and actually brings them in. A promise alone does not save anyone. Day 6 safe and loss paths have different dialogue and actual outcome states. Successful prevention cannot spawn an inside-fire witness, a rescue from the empty building, or a forced death.

Investigation earns the wall, layout, can-plus-fragment and four person records. The teacher describes the anonymous action sequence during investigation, before the hearing. Nubi recognizes the can before a personal ownership question unlocks. Her ownership admission is not an ignition confession. Her child's reason for refusing is stated early; housing and support are supplied without testimony obligations. No child's testimony is required to reach a partial result.

The hearing requires real card selections, preserves Nubi's valid objection that later rescue does not alone disprove earlier arson, then adds her specific new M handoff claim. The map requires five player inputs: can endpoint W; empty-handed person return L; child L–M observation; teacher M–W observation; M overlap contradiction. A final person-card selection is separate from the final certainty gate.

## Art and logic gates

r13_rec_e3_geometry_art_verified is False by default. The new diagram has L=(0,0), M=(5,0), W=(10,0), child coverage 0–6, teacher 4–10, overlap 4–6. It is explicitly labeled as a proposed diagnostic diagram, not a verified panorama. Existing woodshed and laundry images are scene illustration only.

Before lifting the gate, the actual background must show a short uninterrupted L–M–W path, no branches or intervening entrances, visible overlap at M, the school window and low wall, the distinct opposite Bori approach, and plausible distant action visibility without face recognition. The can must remain at W in both the artwork and gameplay. Each observer's exact brief continuous interval and any other crossings need independent review. The teacher must plausibly distinguish body/can movements without recognizing the face: outbound orientation away from the school window, followed by face detail obscured by the door-fire backlight, with no invented hood or new path-blocking wall. The teacher calls out immediately and observes only the short return to M while raising the alarm, then goes to help; this interval must match the child's short return observation. Any gap or crossing forces partial resolution even if art is later approved.

The default playable result is partial_geometry_unverified, not Nubi convicted. Without the child's testimony it is partial_no_child_testimony. Both proceed to episode 4. A complete identity conclusion is implemented and tested only under explicit hypothetical geometry verification; the production default is not changed by tests.

## Verification completed

38 executed Python tests cover knowledge-dependent unlocks, premature/unearned presentations, wrong evidence/order/map/person, voluntary anonymity and refusal, actual-vs-promised school handoff, safe/loss parity of core evidence, no retroactive rescue, no repeat fire, M2/Piko/Nabi/Neoul state preservation, snapshot purity, save/load JSON, source/runtime parity, registered speakers/targets, date/place fields, absence of legacy story calls, no developer caveats in investigation dialogue, and native-art gates.

## Not yet verified

- Native RenPy syntax/rendering, text clipping and real screen interaction.
- Real placement of NPC/object hotspots by the common scene UI.
- Production art for the cart reconstruction and L–M–W continuous sightlines.
- Full campaign handoff into episodes 4–6 on the final integrated artifact.
- Native screenshots. The QA fixture requests them; no image is presented as an executed screenshot.

## Integration additions

The plugin registers r13_rec_location_overrides[3] so store maps to the school-back woodshed (day 5 intact, day 6 ruin) and post maps to the laundry, instead of falsely labeling them as the communal stockroom and post office. Every investigation action supplies target_person or target_object for the shared physical scene UI. Direct-entry labels are r13_recommended_ep2_admin and r13_recommended_ep3_admin. The native E2 fixture traverses the shared map/actor/object/question screens; the E3 fixture deliberately uses the disclosed administrator action harness before real evidence/map clicks.
