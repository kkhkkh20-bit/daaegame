# Six-hearing recommended presentation adapter

Status: source/data wiring completed locally, default OFF. Native Ren'Py behavior, visuals, sound and screenshots have NOT been validated. This document supersedes the earlier five-shot preview description. No GitHub changes were made by this work.

## Implemented

- A recommended-only claim/session/cast registry for all six actual hearings. Nothing is inserted into `R13_DEBATE`; no old evidence, guilt, voting or conclusion logic is invoked.
- Exact pre-answer step IDs for core, EP2, EP3 and EP4–6, plus explicit line-identity cues. The route coordinator has wired enter, prompt, answer and exit calls into the actual hearing labels.
- Existing `r13_meeting_stage` / `R13MeetingOrbit`, focus/pan, approved full-body pose profiles, surprise frames and reaction timing are reused. No art exports, assets or 2×2 filters were modified or duplicated.
- Camera follows the actual speaking attendee. Papa is never in the roster. M0/M1 Mother never appears; even M2 Mother is included only in the authored EP6 meeting, and an explicit attendance list can exclude her. Safe Piko attends EP1 only; dead Piko never attends. Detained Neoul is excluded immediately. EP3 child testimony respects the actual consent state.
- Presented proof raises visible pressure gradually. A failed argument or successful, authored defense restores composure instead. The teacher's corrected-target defense and prevented-poison branch do not imply guilt. Unverified EP3 geometry cannot produce a visually decisive conviction.
- Major public revelations create a one-time group surprise; the target retains nervous talking afterwards. Prediction, skip, reduced motion, reload and repeat proof do not intentionally replay the reaction.
- Dedicated recommended say screen, menu screen, pause controls and recommended notebook. There are no legacy claim or record buttons. Shared typewriter behavior remains. Existing council/pressure music and ambience are reused with purposeful ducking and a short silence; no new impact SFX.
- Exit and interruption restore pre-entry channel tracks/gains/pause states, original Character routing, and neutral presentation state. Interruption unwinds only call frames created after entry before jumping to investigation. Reentry preserves presentation pressure without modifying story progress. The after-load callback restores the saved recommended camera session and settles, rather than repeats, the shock.

## Owned files and build

- `game/systems/room13_recommended_meeting_adapter.rpy`: generated runtime, including its own screens/labels.
- `dev/recommended_meeting_staging_model.py`: pure presentation state/cue model.
- `dev/recommended_meeting_staging_runtime.rpy`: Ren'Py integration and screens.
- `dev/build_meeting_staging.py`: generator for this adapter only.
- `dev/test_recommended_staging.py`: 30 deterministic tests.
- This document and `dev/recommended_meeting_staging_native.rpy`: native handoff fixture.

Run `python dev/build_meeting_staging.py`, then `cd dev && python -m unittest discover -p 'test_*.py'`.
The latest local integrated result is 181 tests passed, including the 30 staging tests. Runtime tests use explicit mocks and are not a claim of native success.

## Native validation and release gate

Use exact main066 production source plus the complete recommended candidate overlay in the existing disposable Ren'Py 8.5.3 QA environment. Do not run against personal saves or persistent data. Keep `r13_rec_staging_enabled = False` in the shipped source. Set it to True only in the QA state, after starting a new candidate run or the supplied fixture.

1. Run the normal Ren'Py lint/compile first. This must verify custom Character screen routing, the `tag say`/typewriter lookup, screen-language menu delegation, and all inherited renderer calls.
2. Copy `dev/recommended_meeting_staging_native.rpy` into the disposable game's QA directory and run testcase `recommended_meeting_adapter_smoke`. This is a seeded adapter smoke, not proof of campaign traversal.
3. Run the existing actual recommended-route fixtures with the staging flag enabled after initialization. Exercise all six hearing entrances and actual prompt/answer hooks, not only the admin preview. Core uses the new-defense and optional cloth routes; EP2 includes silence and consent; EP3 includes limited and fully verified geometry; EP4 includes prevention and detention; EP5 includes prevention and corrected target; EP6 includes M0/M2 and real protective arrangements.
4. In each real hearing capture the speaking cut, major reveal, settled nervous response, successful defense, recommended notebook open/return and final cleanup. Confirm no Papa, absent Mother, dead Piko or detained Neoul; no old claim/evidence UI. Compare reduced-motion and normal-motion behavior.
5. Save during an NPC line, a proof explanation and a custom menu. Also save while the nested notebook is open. Reload each; verify exact story/card cursor, same speaker/pressure, no repeated shock, no old UI, functioning typewriter. Test back-to-investigation from mid-line, nested inspection, menu, repeated leave/reentry, and then a different episode. Verify call stack has no abandoned hearing frames.
6. Hear the audio, not merely inspect variables: check typewriter preference, volume preference, intentional duck/silence, recovery cue, no unrequested impact sounds, and original ambience/track/pause restoration on exit.
7. Attach actual screenshots and logs, record exact commit/source hashes, then request release activation review. Do not equate the current 181 Python tests, source hooks or seeded fixture with completed native QA.

The user-facing admin item still calls `r13_recommended_staging_admin`; it now previews each of the six real cue maps without turning on ordinary campaign staging. Preview is not a substitute for the actual-hearing matrix.

## Verified API references

Character-specific say screens use the documented `screen` parameter: https://www.renpy.org/doc/html/dialogue.html
Bounded interruption cleanup uses the documented return-stack and pop-call APIs: https://www.renpy.org/doc/html/label.html
Their existence was checked in official documentation; behavior against this exact candidate remains a native gate.
