# Independent executable-story logic review

Review date: 2026-10-18 UTC. Scope: the current local recommended-route executable `.rpy` files (including the later-added independent day-1 opening), their pure models/tests, the plugin API, and the recommended bundle state contract. No production source edits or remote writes were made by this reviewer.

## Decision

The route is **not yet evidence of native playability or production-ready presentation**. The existing tests initially missed a reachable clock softlock and an avoidable-harm prevention trap. The clock softlock has now been repaired and independently retested. A six-case, low-investigation/loss/partial-resolution state route can reach the ending; this is a meaningful state-logic result, not an engine walkthrough.

At the follow-up 17:06 UTC checkpoint, the EP5 prevention trap, both EP6 knowledge-order defects, M2 guidance, and the late-hearing answer-ID rewrite have been independently rechecked in the generated executable. The new day-1 opening and day-1 reunion remain viable. Two small timing/knowledge regressions found during this follow-up were corrected and retested. No demonstrated P0/P1 logic defect remains open within this bounded review. Native scene/input/save behavior and production-art premises remain real unverified release blockers, not passing state-test claims.

## Method and evidence limits

- Read actual action specifications, prerequisites, day/period restrictions, shared navigation, hearing labels, consequences, and saved-state transitions. Did not treat a passing author's test as proof of the dialogue.
- Extracted and executed the first Python init block from each of `room13_recommended_story.rpy`, `room13_recommended_ep23.rpy`, and `room13_recommended_ep456.rpy`. This independently checks the generated executable definitions rather than just importing their dev-model counterparts.
- Ran `python -m unittest discover -s dev -p 'test_*.py' -q`: 148 tests passed at the final bounded Piko timing recheck (17:29 UTC); 142 passed at 17:20 and 135 at the earlier 17:06 checkpoint. Earlier 106-test success coexisted with the demonstrated EP3 softlock.
- Exercised a full six-case low-investigation route described below, including day skips, optional prevention omissions, protected silence, and delayed reunion.
- Did **not** run Ren'Py, render scenes, inspect native mouse hitboxes, validate sound/save/load behavior, approve visual geometry, or validate the altered medical explanation. Passing pure transitions assumes that the corresponding interactive puzzle can actually be completed in the engine.
- This workspace is not a Git repository; no GitHub or revision/commit validation is claimed.

## Demonstrated defects and narrow repairs

### P0-01: sunset skip could permanently block EP3 (repaired during review)

Location: `r13_rec_evening`, the hub's evening menu, EP3 action `max_period` assignments, and `r13_rec_e3_block`.

Reproduction in the intermediate executable:

1. Enter EP3 on day 5, period 1.
2. Before `e3_bowls`, choose the available evening command and confirm waiting without school handoff.
3. Period becomes 2. All four pre-sunset actions, including `e3_bowls`, are unavailable.
4. Advancing the day still requires `e3_children_known`, obtainable only from the unavailable `e3_bowls`.

Result: no onward route, no way to reverse period, and no actual ending. The existing suite passed.

Repair observed: the optional information is no longer a date-advance prerequisite; the next-day loss scene introduces the children and their situation. School handoff itself remains unavailable after sunset. Independently retested fresh EP3 → evening → next day → loss investigation → partial verdict. This avoids solving a softlock by forcing every player to collect optional clues.

### P1-01: skipping day-11 school inspection forces poisoning despite known preventable danger (repaired and independently retested)

Location: `room13_recommended_ep456.rpy`, `e5_school`, `e5_pharmacy`, `e5_lock`, and `r13_rec_e456_block`.

Reproduction: enter EP5 → advance from day 11 without `e5_school` → inspect `e5_pots` → speak to Seori with `e5_pharmacy`.

The player now knows the planned drug use and that the drug remains in the cabinet. However, `e5_school` is day-11-only, while day-12 `e5_lock` requires its `e5_notice_checked` flag. The only remaining EP5 action is `e5_serve_accident`. Advancing requires an actual meal outcome, so onward play requires poisoned children. This is not a physical inability to prevent harm; it is an expired information gate. The notice card itself describes an 11–12-day observation.

Narrow repair: keep a current school-space/notice inspection available on day 12, or make immediate cabinet protection independent of the missed persuasion evidence. Do not repair this by making all day-11 clues mandatory.

Repair independently verified: after skipping every day-11 action, `e5_pots → e5_pharmacy → e5_school → e5_lock → e5_serve_safe` is available and leaves `e5_poison_blocked=True`, `children=well`. The school inspection is removed after the meal event, not solely because day 11 expired.

### P1-02: final person card states guilt before the direct-order evidence exists (repaired and independently retested)

Location: `e6_card_granny` and action `e6_nabi` in `room13_recommended_ep456.rpy`.

Reproduction: enter EP6 → `e6_board` → `e6_nabi`, without `e6_munchi`.

The received card is titled “할머니 · 이번 지원 배제의 지시자” and asserts the knowing false-completion exclusion. Nabi's acquired account proves the request/awareness and later missing delivery, not who ordered it. Munchi's later account is expressly the proof of that missing link. The card therefore supplies the conclusion before the player's rebuttal obtains it.

Narrow repair: initially identify Granny neutrally as the person who received the 7-day request. Describe only the facts actually learned. Update the conclusion only after the order/application evidence and hearing, or keep conclusions outside the evidence card.

Repair independently verified: the initial card now reads “할머니 · 7일 식사 요청을 들은 사람” and explicitly does not establish an order. `e6_granny_order_heard` is absent after Nabi and appears only after Munchi.

### P1-03: caravan-hold dialogue uses unseen records and an unmet passenger (repaired and independently retested)

Location: `e6_hold` prerequisites and `r13_rec_e6_hold_scene` school branch.

Reproduction: fresh EP6 → `e6_manifest` → `e6_hold`, before `e6_board` and `e6_pandol`.

The action is available with the manifest alone, but Dad claims that the passengers were recorded as already protected outside while still physically here. Neither the classification nor the actual passenger check has been acquired on this path.

Narrow repair: retain urgent protection, but branch dialogue to what the manifest actually shows: the onward caregiver is unverified, so pause until checked. Do not delay protection for unrelated final-case evidence.

Repair independently verified: `r13_rec_e6_hold_lines` uses the contradiction only when both board and Pandol have been checked; the manifest-only branch cites the unknown onward caregiver and actually checks the current passengers in that scene. Immediate hold remains available with only the manifest. The at-altar branch uses its actual current location.

### P1-04: optional care omission silently empties the cart (repaired in source; native scene untested)

Location: EP2 `e2_care` and `r13_recommended_ep2_hearing` aftermath.

Previously, a player could omit the optional Musoe/Somi handoff, finish the hearing, and immediately see an “empty cart.” The resident was never visibly released or handed over. Moving into EP3 then permanently removed the day-5 care action.

Repair observed: the earlier rail inspection/card/feedback no longer falsely calls the occupied cart empty or asks the occupant to reenact restraint. If `e2_care_complete` is absent, the hearing aftermath visits the gate, performs the established handoff dialogue, and applies `e2_care` before describing the empty cart. The side activity remains optional instead of becoming a collection gate.

### P1-05: later custody relies on a nonexistent earlier procedure (repaired in source)

Location: EP4 result says “앞서 정한 절차대로”; bundle contract §8 requires that rule to have been established during EP2.

Previously, no earlier recommended-route line stated that proved confinement/rescue obstruction could justify supervised custody, including for a guard. The EP4 verdict invented the procedure while claiming prior establishment.

Repair observed: EP2 now has a public agreement on that procedure, preserves parent accompaniment for children, and records `public_custody_procedure_heard`. Engine continuity remains to be played.

### P1-06: future knowledge and stale promises around early Mother reunion (repaired during review)

Locations: common `reply`/`meet`, Piko first meeting, and day-3 survivor dialogue.

The coordinator independently found that an old “meet now” reply remained valid on later days, and that Piko still heard “I am looking for my wife” after M2. This review additionally identified Daram's survivor line “엄마 만나면…” after an actual day-2 reunion.

Repair observed: a dated reply is required for meeting; an explicit current-contact refresh is available after delay; M2 Piko lines now acknowledge reunion. These changes preserve the ability to meet early instead of forcing an arbitrary date lock.

### P1-07: repeated first-answer pattern turns later hearings into confirmation clicks (rewritten and independently retested)

Location: `r13_rec_e456_hearing`, `r13_rec_e456_step`, and `r13_rec_e456_pick`.

Every checked EP4/EP5/EP6 detail and conclusion pair has `right_detail == 0` and `right_claim == 0`. Many alternatives contrast the intended scoped statement with an obviously invalid total claim, rather than competing explanations grounded in the acquired facts. The UI presents the correct answer first every time. This does not corrupt saved state, but it directly weakens the requested deduction, real rebuttals, and meaningful player input.

Narrow repair: use plausible local rival explanations at key turning points, distribute correct positions, and require selecting/connecting observed locations or chronology where that is the actual inference. Do not merely shuffle an obvious answer against a nonsensical distractor. Keep honest partial outcomes and care choices.

Follow-up result: all 26 distinct EP4/5/6 hearing-step variants now use semantic answer IDs, local competing interpretations, and option-specific feedback. Every wrong detail and conclusion was independently tested; each returned its matching explanation without changing state. Old integer answers are rejected. Correct-detail positions are 8 first / 17 second / 1 third; correct-conclusion positions are 10 first / 16 second. The screen returns `answer_id`, and the hearing passes that unchanged into validation. This is more than shuffling the old correct-first choices. Native input/layout is still unrun.

## Additional presentation/continuity concerns

- EP3 completion formerly had Dad say “실제 입력” and “부분 해결로 다음 사건을 진행할 수 있다.” These are implementation notes, not speech. The coordinator replaced them with evidence limits and a concrete request not to detain Bori. Confirmed in source, not native playback.
- EP5 originally ended with “내일 출발 명단…” despite same-day EP6 entry. **Repaired in current source:** the cue now says “이제 오늘 저녁 출발 명단…”.
- The original notebook/hearing list accumulated **47 cards** on the independently completed low-investigation route without main/episode grouping. **Repaired in current source:** a shared catalog defaults to the current episode, provides main/EP1–6 folders and person/material tabs, and groups related observations under reusable identities. Dates and historical observations remain inspectable. Four catalog tests pass. Native usability remains untested.
- The original field could position more than four targets beyond the viewport. **Repaired in current source:** the field now pages four targets at a time and uses page-local positions. Native hitbox/page-button usability remains to be checked; no native accessibility claim is made.

## Clock and missing-evidence sweep

The following minimal/omission path was executed from the generated `.rpy` definitions:

1. EP1: hear Piko and daytime heat, omit shelter and all Mother work; advance; collect only the mandatory theft-chain facts; resolve to handoff responsibility with Piko dead and Mother M0.
2. EP2: report, advance, core interviews; choose silence; resolve prior coercion without asserting the bite contact. Omit the optional care activity before hearing.
3. EP3: immediately choose evening, skip all day-5 activities, advance to loss; investigate adult/physical evidence, decline child testimony, reach `partial_no_child_testimony`.
4. EP4: wait without tools, omit fast rescue, investigate day 8, omit both prevention and day-9 watch; observe the injury outcome and resolve the independent 7-day responsibility. Neoul is detained; no day-9 exclusive-access proof is invented.
5. EP5: skip day 11; choose accident on day 12; conduct Bori/Saemi/container interviews on day 13 and hand care over; resolve responsibility. This demonstrates onward progression but does not excuse the separate lost-prevention defect.
6. EP6: check only Pandol on day 13 and advance; investigate on day 14, hold the already-arrived caravan, verify the altar, perform the full real contact/reunion chain for the first time on day 14, verify research and all survival resources, prove the case, cancel the forced transport, physically hand over care, and finish `complete_today` with M2.

No second hard softlock was found in this sweep. Date-exact essential facts in EP1 and EP4 currently remain mandatory day-advance gates; this report does not claim those episodes allow a wholly uninformed partial verdict. No additional clue gate should be added merely to satisfy a test.

## Art/runtime validation is separate from logic

- Piko contact-art verification remains False. Without it, direct-removal proof is blocked and handoff responsibility still permits progression. This gate is honest.
- EP3 geometry-art verification remains False. Even with both witnesses and successful map inputs, only a geometry-unverified partial result is allowed. This gate is honest.
- EP4/EP5 use new schematic screens and assert their proposed structural/visibility facts in narration. `r13_rec_e456_art_status` explicitly says scene/art and medical/story review are unfinished. It is **not** an enforcement gate. Their verdicts can be completed without any production-art verification flag. This is a release-validation gap, not proof that the proposed geometry is impossible or that an existing False gate was flipped.
- In particular, EP4's no-other-entry/no-hidden-trigger deductions and EP5's continuous pot/witness visibility require actual scene/art review. The diagram and pure tests do not validate those physical premises.
- Detained Neoul is not given a later physical action in the reviewed EP5/EP6 code. Prevention flags and M2 are protected by transition checks; no demonstrated prevention reversal or repeat first reunion remains in the tested path.

## Suggested native acceptance pass

Before describing the recommendation as playable, run at least: the fresh EP3 sunset skip, skipped-day-11 EP5 rescue opportunity, early-M2 Piko scenes, optional EP2 care omission, late day-14 Mother reunion, EP4 full prevention plus custody, and EP6 early-manifest hold without board/person knowledge. Inspect the actual card selector, scene target hitboxes, save/resume at hearing interruptions, map overlays, and the survival/care aftermath. Verify these through real player input rather than admin state seeding alone.

## Bounded village-dialogue check

This is a village meeting with frightened people, not a courtroom or a tutorial about evidence standards. The largest same-voice problem is not a single technical word: Dad, helpers, children, and feedback repeatedly explain what may or may not be “확정,” “입증,” or “판정.” Their jobs, relationships, urgency, and emotional reactions disappear behind the same disclaimer pattern. Keep precise dates and limits in the notebook; let spoken disagreement concern what somebody saw, whom somebody is afraid for, and what they want done now. Preserve uncertainty, but do not have every witness lecture on it.

The following are **proposed dialogue-only examples**, not source edits or new story facts. “Before” quotes preserve the reviewed checkpoint; the coordinator has already softened some early-episode lines during this review. One example per episode is enough for this bounded pass.

### EP1: ask about the unresolved act, not the validation pipeline

Location: `r13_recommended_hearing`, handoff-only result.

Before: “아이에게 넘긴 사실과 광장에서 직접 꺼낸 사실은 다릅니다. 현장의 접촉 흔적을 검증하기 전에는 직접 반출까지 확정하지 않겠습니다.”

After: “꼬미는 돌을 받았지만, 광장에서 꺼내는 건 못 봤대요. 등에서 누가 꺼냈는지는 아직 더 알아봐야겠어요.”

Same facts: a handoff is established; the original removal is not. This sounds like a parent pursuing one remaining question, not a reviewer explaining an art gate.

### EP2: protect the friend without giving a legal closing argument

Location: `r13_recommended_ep2_hearing`, admitted-bite result.

Before: “그 말로 먼저 묶고 귀가를 막은 일이 없어지지는 않습니다. 물림과 선행 강제 이동을 각각 다뤄야 합니다.”

After: “밤이가 문 일도 그냥 넘길 수는 없어요. 그렇다고 그 전에 사람을 묶어 집에 못 가게 한 일이 없어지는 건 아니죠.”

Same facts: bite and prior coercion both remain. Keep Bami's apology and fear in the scene rather than making Dad summarize two case classifications.

### EP3: ask a witness the concrete question

Location: `e3_bori_loss` action.

Before: “구조 행동을 확인하겠습니다. 그것만으로 이전 행위까지 무죄라고 단정하지는 않겠습니다.”

After: “문이 타서 벽으로 들어가신 거군요. 처음 불붙을 때를 본 사람이 있는지도 찾아볼게요.”

Same facts: Bori has already described rescue and a burning blocked door; Dad acknowledges that account and looks for an independent witness instead of pronouncing provisional innocence or asking him to repeat it. The independent teacher account is still needed. The newer EP3 partial-result text is improved, but long witness-limit summaries remain frequent.

### EP4: confront Neoul with the parent's actual grievance

Location: `r13_rec_e456_hearing`, final 7-day Neoul step; its answer is spoken by Dad.

Before: “그 문을 직접 열었던 사람이, 살아 있는 사람이 남았다는 말을 듣고도 못 연다고 했습니다. 묻는 것은 7일의 그 감금과 구조 방해입니다.”

After: “너울 씨, 그날 직접 문을 열었잖아요. 다람이가 안에 사람이 살아 있다고 했는데, 왜 우리한테는 못 연다고 했어요?”

Same facts: knowledge of opening, the live-person report, and the false refusal. This restores direct tension between the guard and a father whose child tried to help. Diagram letters belong on the diagram; ordinary speech can say “객실 쪽,” “안쪽 칸,” and “그 레버.”

### EP5: keep the disputed motive, but do not let it erase the act

Location: `r13_rec_e456_result`, non-prevented soup branch.

Before: “그 부분은 구별했습니다. 다른 사람에게 줄 음식에 위험약을 넣은 일과, 자신이 바꾼 표식의 책임을 보리에게 돌린 일은 남습니다.”

After: “아이들을 노렸다고 몰아가지는 않겠어요. 그래도 약을 넣고 뚜껑을 바꾼 일까지 보리에게 떠넘기진 마세요.”

Same facts: the original target is distinguished from child harm; mixing and the lid change remain established. Do not state that the teacher's hidden intention has been proved merely to soften the language. Remove especially out-of-world choice text such as “일어나지 않은 혼입을 기수로 판정한다”; a natural alternative is “아이들이 먹었으니 약도 넣었을 거야,” which is still a mistaken inference the scene can correct.

### EP6: talk about the person whose meal disappeared

Location: `r13_rec_e456_hearing`, last Granny step.

Before: “할머니가 입증된 것은 이번 지원 배제와 대안 차단의 지휘 책임입니다. 너울의 별도 폭력과 촌장의 방치까지 사라지는 것은 아닙니다.”

After: “할머니, 판돌 씨가 아직 학교에 있다는 걸 들으셨잖아요. 그런데도 그분 몫을 빼라고 하셨어요. 남아 있는 사람의 밥과 잠자리는 돌려놔야죠.”

Same facts: known continued presence, direct exclusion order, and the immediate remedy. This does not make Granny responsible for all winter deaths or excuse Neoul/the chief; those limits need not be recited in every character's last line. Remove the author numbering in “⑤ 이후 추가된 선생님…” from player-facing choices.

### Additional concrete continuity bug found during this pass

`r13_rec_e456_ready` at EP6 hearing index >= 6 tells Dad to “엄마와 재회해 원본을 받고…” whenever research is not yet field-verified. This is wrong on an M2 early-reunion route that already owns `research`. **Repaired and independently retested:** M2 now receives “엄마에게 받은 원본을 현재 난로와 교실에 대조해 보자.” M0/M1 still need the genuine contact/reunion chain. Reunion is not undone and field verification is not automatically granted.


## First-fix checkpoint (historical, superseded below)

The independently tested first-fix snapshot at 16:57 UTC had these SHA-256 values:

- `room13_recommended_story.rpy`: `948b50ddf205f1f521d196f9b5e144d135471d4369d87bb5d2c383343ef23706`
- `room13_recommended_ep23.rpy`: `b92b0bbe33d60b0041bec0002e1419193e9e81d1e50bdafe4fac5d6fe18f09a2`
- `room13_recommended_ep456.rpy`: `d57e93cafc4b47d8ae452f2653b420d6a161000b7475b56ed65dd988c15536d3`

At that checkpoint the later-case owner was still improving choice IDs/distractors and dialogue. The follow-up review below now covers those regenerated definitions.

The first-fix snapshot still contained an EP5 pharmacy line claiming a school motive Dad had not heard on the skipped-day-11 path. **Now repaired and source-checked:** Dad only notes that the drug is still present, proposes keeping it stored, and says he will ask the teacher what is worrying them. No prevention prerequisite was added.

The requested examples remain a bounded voice guide; several were adopted by the authors. No production edits were made by this reviewer.


## Follow-up checkpoint: day-1 opening and semantic answers, 17:06 UTC

### Independently checked

- Extracted the actual init-906 opening block after the core block, then EP23/EP456 registration, respecting their initialization order. The optional driver testimony was not needed to clear the gate.
- Fresh day 1 exposes only the guard report. Ending the day before actual admission/arrival is refused. Choosing evening first does **not** hide the mandatory opening actions: report → original → two earned documents → inn still works. The two-document screen handles wrong evidence, duplicate selection, and cancellation without applying clearance; that wiring was read, not clicked in Ren'Py.
- Family contact, actual reply, meeting, room check, and shelter can finish on day 1. Advancing to day 2 preserves M2 and opens Piko's day-2 encounter. No date lock was inserted to defer reunion. `family_route` is optional after reunion, checks the existing carriage/pass conditions, and does not claim repairs or road clearance already happened.
- The opening creates empty isolated `facts`/`done`, adds only its own earned document/person facts, and never calls the old carriage story or automatic campaign event path. G1/G3 are used only to retrieve existing document artwork. The shared renderer/upgrade bridge was inspected: the old dead/Mother stand-in dialogue substitution applies to `debate:`/`meeting:` identities, not these `recommended:` identities. This is source/state separation evidence, not native proof that every old HUD is inaccessible.
- Re-probed skipped-day-11 prevention, the neutral Granny card before Munchi, the order flag after Munchi, manifest-only hold, and M2 research guidance with the opening wrapper installed. All pass.
- Independently exercised all 26 semantic hearing variants using step-focused prerequisite snapshots. These are intentionally focused model snapshots, not a claim that every branch was reached through native play. Each wrong choice preserves state and returns its own feedback; each correct ID advances the intended step. The pure full-route suite also passes.
- Read `r13_rec_e456_pick`: it destructures `(answer_id, caption, feedback)`, returns the ID, and the hearing loop supplies both returned IDs to `r13_rec_e456_present`. Generated QA fixture captions match the rewritten choices, but those fixtures have not been run here.
- Piko contact-art and EP3 geometry-art booleans remain False. No review action silently enabled either production-art gate.

### Regressions found and repaired during this follow-up

1. **Day-1 reunion / day-2 Piko date claim:** M2 Piko speech still said “오늘 아내와 다시 만났습니다.” The author removed the false “today”; the actual day-1-meet → day-2-Piko path was retested. The opening inn's unexplained “며칠 전” visit timing was also removed, avoiding conflict with the existing day-1 visit card.
2. **Premature altar inspection at hearing index 4:** the rewritten next-caregiver answer/one distractor feedback said the family had already visited the altar. That action is legitimately required only at index 5. The author replaced those lines with wording that is true before or after inspection. Independently verified that index 4 can be answered without the altar flag, says no past visit, and then index 5 correctly asks for the actual inspection. No new all-clue gate was added.

### Latest checked hashes

- `room13_recommended_story.rpy`: `1f7f72c5b4a9608083bcc3794a16647f434137cfca2810b0c9d060644f9c62b3`
- `room13_recommended_opening.rpy`: `ed59ed6534fa6ad147dc19575e5d7b65a688e8b54e72f6d394fb1498502bffdc`
- `room13_recommended_ep23.rpy`: `b92b0bbe33d60b0041bec0002e1419193e9e81d1e50bdafe4fac5d6fe18f09a2`
- `room13_recommended_ep456.rpy`: `0b402dad142e54f2b0e36a629e5738be34a94d2deaa95d8610ac06c8a90b5c91`

### Remaining real blockers

No open demonstrated softlock or knowledge-order defect was found in the bounded recheck. Still required before a native/playable claim: actual title-entry and card-selector interaction, hearing cancellation/save/resume, target paging, dialogue layout, engine integration with the base game, production art/geometry verification, and the already-disclosed medical/story review. The schemes in EP4/5 are still new proposed geometry, not an approved physical scene. Piko/EP3 deliberately produce limited results until their art gates are genuinely verified.

This clearance is limited to demonstrated logic defects, not a claim that every narrative goal is implemented. The family ending currently supports staying together or explicitly postponing departure; it does not execute or verify an actual journey home. A playable departure, if required by the final scope, remains unfinished. Likewise, the main investigation's dramatic/inference depth is not established by the state tests or by adding the admission tutorial.


## Bounded Piko access and meeting-causality follow-up, 17:21 UTC

Scope was only the new Piko field/owner-consent/meeting flow, using the actual generated source. This is not an extension of the earlier clearance to any meeting-renderer adapter currently under development.

### Verified behavior

- The ordinary day-3 route discovers the inner fragment and follows the numbered stone and child's handoff account, but does not silently acquire Nabi's working cloth/container. `child` grants only `stone` and `child`; `contact_match` is not yet available.
- The optional `piko_cloth_consent` asks the obvious source and sole-user questions early. Nabi gives permission without surrendering her property, then actually brings the cloth/container to the square with the family. Her explanation is recorded as a claim, not independent proof.
- At the normal meeting Nabi states the outside-only/sole-user defense and physically places the container/cloth beside Chorong's lamp. `r13_rec_piko_hear_defense` then grants the two earned records and comparison access. On the optional earlier-account route the already-heard explanation is remembered instead of treated as new information.
- Independently executed eight production-gate paths from generated init blocks: ordinary versus earlier consent, Piko safe versus dead, and M0 versus day-1 M2. All retain the False art gate, refuse direct-removal credit, allow the three-card limited result, preserve prevention/reunion, and unlock EP2. Wrong presentation of `container` at the first step does not mutate state.
- In an isolated in-memory namespace only, simulated future-approved art for the two intended comparison paths. Normal meeting comparison requires four earned presentations. Earlier completed comparison can be summarized without forced repeat card clicks; it does not produce a day-3 verdict. These probes do not approve the production art or its causal premises.
- The matching screen remains cancellable. Its successful `matched` return is checked against the False geometry flag before `r13_rec_apply`; current play cannot acquire `cloth_contact_matched` merely by aligning the texture.

### Demonstrated access regression, repaired

`room13_recommended_story.rpy`, `r13_recommended_hearing`: when day-3 consent had already set `piko_source_claim_early`, the meeting skipped the entire new-defense block. That block also contained the only line physically bringing the lamp to the meeting. The optional route brought the cloth back but offered inner-fragment comparison without bringing the lamp back.

Reproduction: day 3 `pedestal` → `chorong` → `nabi_route` → `child` → `piko_cloth_consent`; cancel or decline the unverified comparison; advance to day 4 and enter the meeting. This is reachable with the production False gate, not only a fabricated approved-art state.

The coordinator added “초롱이 광장의 등을 회의 탁자에 내려놓았다.” to `recommended:hearing:earlier-account`. Independently source-verified at line 592. No extra evidence requirement or forced field collection was added.

### Latent causal issue before direct-removal can be enabled

The current False gate prevents this from becoming an active wrong verdict. However, `r13_rec_hearing_steps` and `recommended:hearing:prior-case` still infer the particular removal from a matching inner fragment plus a sole-user claim limited to borrowing through handoff. The day-2 maintenance scene does not establish that the fitting was previously clean, and no earned testimony excludes an older or separate innocent internal contact. Physical matching establishes contact, not its time or purpose. The later admission also says only that Nabi lifted the stone with the cloth and put it in the container, without explicitly locating that action inside this lamp.

Before enabling `direct_removal`, establish the time boundary through an actual observed clean fitting and ask about other internal contact, or limit the result to a contradiction/internal-contact finding until Nabi explicitly admits removal from this lamp. Merely approving a rendering of the closed lid does not close this temporal inference gap. Sent to parent/coordinator immediately; no production edit made by this reviewer.

### Snapshot and limits

- Full suite: **142 source/state tests PASS** (includes the two full-route tests), not 142 native play tests.
- `room13_recommended_story.rpy`: `6f42b8c493827b354577dc97bfad9d23254775c50e9a19cd3017fc29b5f5172c`
- `room13_recommended_cloth_compare.rpy`: `9c8c556850521cad9d5e0116222c6d839cd2eaa62a3d877b8acbc0def4f9c222`
- No open demonstrated active P0/P1 blocker in this bounded Piko snapshot after the lamp-staging repair. The latent direct-removal causal condition above remains a requirement before that gated conclusion is enabled. Native interaction and all art/geometry approval remain unperformed.


## Final bounded Piko timing recheck, 17:29 UTC

**The temporal objection above is resolved by the latest explicitly added testimony, at the level of ordinary reasonable inference.** This does not approve the actual lamp geometry. It also does not certify the separate meeting-staging adapter currently being integrated.

The first `child` inquiry and its existing person card now include both observations: Kkomi unfolded this cloth and saw the same corner intact before lending it with the empty container on day 2; that evening, as Nabi unfolded the cloth to set down the returned stone, the same corner was already torn. Continuing the loan thereafter establishes custody only, not the time of the tear. These are explicit new recommended-story details, not Dad's invented prior knowledge, a new witness/item, or a later recovered memory.

`r13_rec_piko_intact_loan` calls the before/after reconstruction before the action applies. Both pictures use the same canonical crop/scale; the later picture uses the same complementary parent mask as the physical comparison. The screen calls itself a reconstruction of Kkomi's account rather than a second independent photograph. The first visit requires reaching the after-delivery view before returning; the existing child's notebook card offers the same reconstruction again. Screen source was read, not natively displayed.

Together, the bounded tear interval, the same numbered stone, the uniquely matching inner fragment, and Nabi's sole-use/no-opening/no-cleaning explanation support the intended ordinary inference. The earlier possibility of an old unrelated tear is no longer left open by the stated facts. This assessment does not demand disproving every invented stranger or conspiracy, and it remains conditional on genuine future verification of the inner-contact geometry.

Independently executed from actual generated init blocks:

- Production False gate: ordinary meeting and early-consent routes still reject contact credit and reach the limited verdict/EP2 with Piko's prevention preserved.
- Hypothetical approved-art namespace only: both ordinary four-presentation and remembered earlier-comparison paths reach the evidence-based result.
- Removing either `piko_cloth_intact_at_loan` or `piko_cloth_torn_at_delivery`, or the sole-use claim, prevents the fourth presentation without changing the state. The early-summary function likewise cannot skip either timing fact.
- No `record_admission` setter remains. No admission flag is needed to establish the verdict. The ordinary reaction follows the evidence result rather than conveniently granting it.
- Found one stale contact-inspection sentence saying the container had been returned, contradicting the continuing loan. Coordinator changed it to “누가 빌려 썼고 돌을 내려놓을 때 천이 어땠는지도…”, and the regenerated line was independently re-read.

Full current suite: **148 source/state tests PASS**, including two full-route tests. No new demonstrated active P0/P1 defect remains in this bounded timing/access/inference check. All native interaction, rendering, save behavior, new meeting-adapter behavior, and art/geometry verification remain outside this clearance.

Checked file hashes (the story also contains new adapter calls; only Piko logic and the indicated screen wiring were reviewed here):
- `room13_recommended_story.rpy`: `01bfd55752c1a66f0ae117e181890e8d237d5d77f944a6d37e1f65b99be75ae1`
- `room13_recommended_field.rpy`: `d93edab9d6bc5c87b816d688355c454f578a3c139b6e1bd503eca68e78c8b8d6`
- `room13_recommended_cloth_compare.rpy`: `9c8c556850521cad9d5e0116222c6d839cd2eaa62a3d877b8acbc0def4f9c222`


## Final frozen meeting-adapter and isolated-QA review, 17:43 UTC

### Result and boundary

No concrete uncorrected source blocker remains in the bounded candidate below after the coordinated repairs. **This is source/model/mock clearance only.** No Ren'Py execution, screen click, screenshot, audio audition, save/load in the engine, remote write, or GitHub change was performed. Meeting staging is still default-off; the native geometry flags remain False. The separate source-geometry review's approval is not native approval by this reviewer.

### Actual wiring checked

- EP1 enters staging with episode 1 and uses the real expected evidence-card ID before presentation; EP2 uses its four card IDs and `e2_order`; EP3 uses its three card IDs, `e3_map_0` through `_4`, and `e3_finish`; EP4/5/6 enter with 4/5/6 and the shared loop passes semantic `step['id']` on prompts and all correct/incorrect answers. These are hooks in the actual hearing labels, not only the preview fixture.
- All normal completion, cancellation, missing-evidence and investigation-return jumps reach `r13_recommended_hub`, whose first operation exits staging. EP2 also exits explicitly before its optional actual care/handoff field scene. Repeated enter for the same active episode keeps the original snapshot; a different entry exits first. The remembered prior Piko comparison remains a deliberate no-repeat-card route, not fabricated fresh inputs.
- Recommended claim/session maps route only to the existing renderer/camera primitives. No `R13_DEBATE` insertion or old verdict/ballot execution is used. Papa is absent from every roster; M0/M1 Mother is absent, M2 Mother is authored only for EP6; dead Piko is absent and safe Piko is only in EP1; detained Neoul is filtered out. The EP3 child's first testimony now follows the actual consent update.
- New say/menu/footer/notebook screens use recommended data. Existing legacy screens are cleared on entry/exit. The previously missed global R-key path is now separately isolated as described below.
- Read bounded return-stack unwinding (`pop_call` for only deeper frames, then saved stack restoration), inherited Character restoration, after-load settlement of one-time reactions, and music/ambience path/gain/pause restoration. Independently exercised twelve mocked lifecycle paths covering six episodes × M0/M2, repeated entry, every cue, after-load, exit and double-exit. Story state stayed unchanged; both mocked audio channels returned to the pre-entry state. This does not validate the actual engine's call frames, rendering or audio timing.
- Normal fresh state has no QA marker or gate switches. QA requires the exact marker and per-state gate plus source-geometry approval; its confirmed new-entry path creates a separate campaign, while normal new entry recreates a clean state. Neither gate helper changes the global native/production flags. QA saves now have distinct labelling and an explicit load confirmation; normal title Continue excludes QA, including when QA is the only available save.

### Concrete regressions found and repaired in this pass

1. **P1: legacy records still reachable from the global R key.** The base `r13_shortcuts` overlay invokes `r13_shortcut_records` above modal screens, and the old implementation knew nothing about recommended screens. Clearing `r13_records` only on entry did not prevent reopening it. New init-935 `room13_recommended_shortcuts.rpy` routes recommended/QA campaigns only to the recommended notebook, ignores relevant modal screens, and delegates unchanged for the old campaign. Generated wrapper and mock dispatch were rechecked.
2. **P1: isolated QA saves could not be reloaded through the UI.** QA used `room13_recommended_qa_v1`, but the save wrapper handled only the normal ID; base code marked QA incompatible and exposed no load action. The revised metadata/status/caption/load wrappers support labelled QA saves with explicit confirmation, reject stale revisions, and keep all QA saves out of normal Continue. Independently executed the real base save functions plus generated init-920 wrapper together, including normal delegation, QA-only Continue, and stale-QA rejection.
3. **QA day mismatch and cross-run cue carryover.** Admin boot left `room13.day=4` after the recommended state was replaced with day 1, and prior campaign presentation memory remained. QA now synchronizes the actual day immediately, and both fresh normal/QA starts clear stage memory. Interrupted reentry within one campaign still preserves pressure, as intended.
4. **First EP3 child testimony omitted its speaking attendee.** Its consent flag was assigned after the entire testimony, but the roster required that flag to include the child. The consent choice now applies the flag before the child's first line; this does not invent consent for the decline route.

### Verification and candidate hashes

- **186 read-only source/state/mock unit tests passed.** The suite's one generator-write test was deliberately not invoked; its intended byte-for-byte equivalence check was performed independently without writing production source and passed. This corresponds to 187 checks, not 187 engine tests.
- Independently compared generated adapter bytes with its model/runtime composition without running the writer.
- No production files were edited by this reviewer. The coordinator made the repairs above; this reviewer only updated this review document.

- `room13_recommended_story.rpy`: `1667e918ef06d4f4834c838aeb582b6d56b161ebadae4e6540cc04e382590c1a`
- `room13_recommended_ep23.rpy`: `a7d83ab4aad202fa4730d1c5b377bee11933c1c538fe5492a47f04525ad8c3ff`
- `room13_recommended_ep456.rpy`: `07b2731169a69537b06c4fb211bf8bac200a9c430157227ea2fd0659ecd5165b`
- `room13_recommended_meeting_adapter.rpy`: `a2eb140f8632e7d60f26e0d28f03ad3f6ca3b8e90de3050891774d594822069a`
- `room13_recommended_native_qa.rpy`: `f9cd5b1cf150a097fc98cfb15ceb81cabe2181b5d90f57dad3b0c550bb244ba2`
- `room13_recommended_shortcuts.rpy`: `fc63efaf4f39c15a1ba7d654a8a4bced2ffe585cc6a9eb90984cfdc1dc2fb4bd`
- `room13_recommended_field.rpy`: `0c9b32200a099c5a5d247bde2f17628afa69e3524dcc1eec4e35eeb69d672eed`


Stop point: this exact source snapshot is reviewed. Any later changes require their own targeted recheck. Remaining release blockers are the already-required native title/meeting/input/save/load/audio matrix and production-native geometry verification, not another demonstrated uncorrected source defect from this bounded pass.
