# Recommended episodes 4A / 5B / 6C implementation status

Local implementation, 2026-10-18. This report does not claim native RenPy execution, screenshots, production-art alignment, or medical review.

## Owned artifacts

- `game/systems/room13_recommended_ep456.rpy`: generated self-contained runtime plugin, init 910.
- `dev/recommended_ep456_model.py`: pure copy-on-write state, cards, actions, staged inference, consequences.
- `dev/recommended_ep456_labels.rpy`: shared-renderer scenes, object-part interactions, rebuttal UI, family first night, administrator entry labels.
- `dev/build_recommended_ep456.py`: deterministic plugin regeneration.
- `dev/test_recommended_ep456.py`: source/state regression suite.
- `dev/build_recommended_ep456_qa.py` and `game/qa_tests/recommended_ep456.rpy`: four native click testcases awaiting execution.

## What is playable in source

- 4A: three actual discovery choices in guest space R, optional early rescue, separate day-7 opening/closing testimony and clinical course, clickable R/G/P/K layout and bidirectional mechanism, day-9 wedge or complete lever lock, actual work result, separate day-9 observation, card/part/conclusion rebuttals, survival-sensitive findings, detention and Daram's release. Complete prevention never fabricates a second crime. The fall is not the fatal weapon-murder version.
- 5B: school notice, original fixed bodies and movable lids, clickable body examination, pharmacist query and actual cabinet lock, mutually exclusive normal dinner or harmful event/care, existing Bori/Saemi/Seori interviews, no-content-transfer continuity and actual same-container chain, care handoff, fixed-body/moving-label/original-target hearing. No completed mixing, concealment or swap follows successful prevention.
- 6C: day-7 decision/day-12 application/day-13 departure comparisons only for Pandol, distinct knowledge/direct instruction/application testimony, actual hold, current altar verification, real mother-original validation, five resource actions, nine-stage public challenge, then actual cancellation, correction and protection handoff, distributed checks and first night. Two documents and the hearing alone do not award completion. Missing research does not restart a paused sacrifice. Detained Neoul never returns to field duty. The finding does not aggregate all historical deaths under Granny.

## Validation and boundaries

39 unittest methods pass, including an exhaustive 108-path episode-4 matrix, early/incorrect/unearned presentation, cabinet/mixing exclusion, M0/M1/M2 preservation, missing research/resources, post-departure hold, actual execution gates, immutable inputs, JSON saves, exact generated-source synchronization, real actor IDs and click targets. This is not a native playback result.

Native testcases: `recommended_ep4_structure_and_prevention`, `recommended_ep5_prevention`, `recommended_ep5_body_lid_target`, `recommended_ep6_actual_protection`. They use disclosed administrator direct-entry fixtures for earlier M2/Piko-safe history and then real episode UI inputs. They must be executed before their screenshot names are claimed as outputs.

`r13_rec_e456_art_status` is for a developer/status panel only. New mechanism/pot diagrams are implemented; their integration with existing background art and the rewritten cause-of-death require further review. Runtime dialogue does not announce implementation contracts.

The mother B route has no verified external escape itinerary. Final family choices therefore distinguish staying tonight from postponing departure until a real route is checked. Neither is falsely marked as successful escape; the community's current forced-sacrifice stop remains complete after actual protection.

Shared dependency: `research` earned through actual reunion; `reunited`; `e6_research_verified` is additional actual validation, not a substitute for reunion. All actions have explicit world person/object targets. No common files or remote repositories were edited.

## Independent-review repairs, 17:01 UTC

- Missed day-11 school inspection can now be completed before the day-12 meal, preserving an actual prevention route after discovering the drug. Its dialogue no longer assumes the missed motive conversation.
- Granny's initial person profile records only the received request. Direct-order knowledge is earned from Munchi, and the exclusion finding is earned in the hearing.
- Manifest-only urgent hold uses only an unverified onward caregiver, then checks current passengers in the scene. It does not borrow the unseen allocation board or Pandol interview.
- M2 research guidance uses the already-received original; M0/M1 guidance follows genuine contact/reunion. First night sets period 2. Administrator fixtures explicitly include the earlier public custody agreement. The day-13 transition says this evening, not tomorrow.
- All late hearing options now use semantic answer IDs rather than list positions. Competing explanations are grounded in local facts, and every wrong detail/conclusion has its own factual response. Correct positions vary; the repair is not a shuffle of implausible choices.
- Courtroom/developer wording was removed from spoken questions, options and rebuttals while keeping the factual boundaries.

Validation at this checkpoint: 39 EP456 test methods and 133 shared test methods passed. Generated runtime and native-fixture source were rebuilt. These remain source/state results, not native Ren'Py execution or screenshots.
