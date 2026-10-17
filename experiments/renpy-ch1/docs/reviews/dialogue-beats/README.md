# Dialogue binding review — local work, assets HOLD

Latest instruction: finish dynamic bindings and record review quality; do not activate
resources, merge, push, or deploy until the final front-facing dialogue package arrives.
This report supersedes the earlier “118 pending” summary.

## Implemented

- All 118 dynamic `r13_lines` calls pass a stable audited route. Original argument
  expressions remain unchanged and are checked by AST comparison.
- `room13_dialogue_bindings.rpy` binds the **evaluated** packet list to that call site,
  identity, index, exact speaker and full text. State changes do not rebuild a saved
  transcript. Unknown/conflicting output fails closed; it never borrows a static cue
  from a different branch merely because the scene ID or text matches.
- Expanded and child-companion topic variants use full-sequence matching. Replays
  retain the recorded words and suppress a fresh startle. Source scopes separate
  the teacher's neutral reassurance from the same words in the Q5A failure branch.
- Snapshot state participates in save/rollback and nested meeting resume. Load,
  skip, reduced motion and rollback suppress the brief startle. Click/AUTO/page
  completion settle the current beat; the timed reaction also expires at 0.35 s.
- Investigation poses and the meeting renderer are preserved. No HOLD artwork is
  registered: `room13-dialogue-talk-art.json` still has `people: {}`.

## Evidence and honest limits

- 80,982 inline/calendar/opening/notice cases: 0 unresolved outputs.
- 63,970 final-init provider cases: 0 unresolved outputs. This runs the real Ren'Py
  data and presentation wrapper chain, including overwritten/init-added data,
  topic rewrites, alibi, carryover, activities, meeting replies and conclusions.
- The union of probes covers all 118 dynamic routes. These are bounded state and
  constructor matrices, not every reachable game history or complete game QA.
- Unit tests exercise the real binding/planning functions, exact call arguments,
  stored transcript isolation, click/AUTO settle path and controlled skip/load/
  rollback engine signals. They are not visual UI playback or image approval.
- `test-results.txt` contains the regression result. `lint-results.txt` contains
  the script lint result. The SDK also logs its existing missing
  `/home/agent/.renpy/tokens/security_keys.txt`; no permission escalation was made.

The final-init probe uncovered an omission in the earlier literal inventory:
`room13-dialogue-expand.json` rewrites. Its 160 NPC rows were read and added to
`expanded-context-review.json`. Another 14 source rows cover song verses and
new residents' unrelated-material replies. A contradictory grouped default for
Nabi's crisis opening was corrected after comparing both variants.

## How the review was authored

Static 1,808 = 1,422 context-reviewed occurrences + 386 mechanically copied,
exactly-equal replay aliases. Dynamic literal 972 = manually chosen contextual
range defaults plus indexed overrides, not 972 independently written essays.
Extraction, source hashes, copying and serialization are automatic. Emotion
selection is not a keyword classifier. Group rationales are explicitly distinguished
from individually reconsidered examples in `quality-examples-20.md`.

- `quality-examples-20.md`: 20 exact IDs, emotions, reasons and adjacent transitions.
- `completion-evidence.json`: counts, route coverage and HOLD status.
- `binding-state-results.json`, `provider-state-results.json`: probe evidence.
- `runtime-binding-queue.json`: all 803 call sites, including 685 static and 118 dynamic.
- `remaining-work.json`: final artwork, visual acceptance, activation/merge/deploy hold.
- `intermediate-resource-receipt.json`: verified incoming intermediate archive, not approval.

## Reproduce

From `experiments/renpy-ch1`:

```sh
python dev/build_dialogue_bindings.py
python dev/audit_dynamic_dialogue.py
python dev/check_dialogue_bindings.py
python dev/run_dialogue_provider_probe.py /path/to/renpy.sh
python -m unittest discover -s dev -p 'test_*.py' -q
```

The provider runner installs a temporary lint hook and removes both its `.rpy` and
`.rpyc` in `finally`. Sound/UI effect callbacks are stubbed only during this probe;
real selectors and presentation responses run unchanged. All work is local on
`dialogue/reaction-states-20261017` over `a60d263`; no new commit, merge or deployment.

## Latest semantic and style revision

See `actor-intent-review.md` and `actor-intent-audit.json`. The teacher's two
reassurance lines now share a composed neutral surface; outcome-based anxiety was
removed. `performance-resource-requests.json` tracks unproduced expressions and
physical/event poses independently. The example IDs were corrected.

Dialogue's approved direction is now smooth storybook source masters on a dedicated
path; map investigation assets remain pixel art. `dev/prepare_dialogue_source_profiles.py`
only produces HOLD staging profiles using explicit sizes/offsets and LANCZOS. The
six-person intermediate package and runtime activation remain on hold.
