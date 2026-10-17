# Meeting expression and listener patch (independent branch)

Base: `d681b9a9db9533191377b9c402dcc92c766d1abb` (main 0.19.39).
No version bump, main merge, web build, or deployment is included.

## Behavior

- Exact `(identity, index, speaker, text)` cues; no keyword or allegiance inference.
- Each new line clears the previous speaker/listener override. At most one listener is
  highlighted gently; there is no group recoil or camera/seat reassignment.
- Authored pose/expression wins. Six approved source variants use a separate per-line
  art slot, so Nabi's authored anxious emotion and angry rebuttals remain authoritative.
- C2 s1: stern statement; Buri's reply is measured interruption, not acquittal.
  C2 s2 E07: Seori examines evidence with no shock. C3 first scream: neutral factual
  testimony; E12: Nabi's authored hesitation, then Granny's authored anxious reply.
- C2 E08 shocks only Ppul after the evidence explanation. C2 s3 E09/E10 keeps the
  canonical counterquestion; presentation never marks broken/stance/seen/clock.
- The source `surprise_react` frame lasts at most .35 seconds, followed by the
  authored talk/anxious pose. Token + pending/playing/settled phase survive save data;
  absolute shock time is no longer used. A rebuilt displayable settles a claimed
  token. Load, modal return, skip, rollback and motion-off settle without waiting.
- Re-selecting a record does not replay its proof token. A proof whose last line is
  still explanation may paint once on the first existing gasp line, never earlier.
- `R13_MEETING_RESUME_FIELDS` includes line token, listener, art slots and reaction.
  The presentation-only consumed-token list deliberately survives a nested reply;
  evidence/proof state is not restored from a presentation snapshot.

## Source art / placement

Approved source commit: `21359223062d1d6c675bcccc21588e0096d2dd9c`,
`art/incoming/meeting-reactions-six-20261017/meeting-reactions-six-source.zip`.
Archive SHA256: `641769c7d6fd572a449403a99bdef84fc4a64485f1c47d598fefd787be7031a0`.
All six runtime WebP bytes and PNG source hashes match the supplied manifest.
Only the six runtime WebPs are copied into the game; PNG originals stay intact in
that source commit. The art branch was not merged.

All six runtime images and their existing neutral counterparts were opened for
visual inspection. The new 840px images use 1.05 scaling to match the existing
882px source frames, with the existing person-specific canvas and offset. This is
an initial alignment, **not engine-verified head alignment**. The supplied bbox
anchors were not misrepresented as anatomical head/foot anchors.

Slots: Ppul `stern_statement`, Seori `evidence_check`, Seryeon `confident_report`,
Nabi `witness_hesitate`, Buri `measured_interject`, Granny `composed_answer`.
Ppul's stern also has exact public-line cues at F1 s1, Q4 s1 and Q6 s1.
These are not permanent character roles. No new eye-turn animation is claimed:
the supplied fronts remain fronts; Nabi's supplied hesitant gaze remains as drawn.

The originals contain low-alpha residue. Runtime counts for `0 < alpha <= 8`:
Ppul 4003, Seori 3743, Seryeon 4708, Nabi 3733, Buri 3814, Granny 2986 pixels.
No source cleanup or silent alpha editing was performed. Inspect against light and
dark backgrounds before release, especially Seryeon's right-side residue.

## Every meeting / remaining visual review

`inventory.json` is generated from authored source assignments by
`dev/meeting_direction_audit.py`. It is a **static possible-attendee superset**,
not a natural progression replay; runtime visibility/POV gates remain authoritative.
It includes all 15 C/F/Q claims, their statements, evidence, counter presence,
source gaze, source stance, table use and ordered possible attendees.

| Sessions | Claims | Existing placement | Close height |
| --- | --- | --- | --- |
| trial | C1–C4 | dining round table | 840 |
| finale | F1–F4 | altar stone table | 840 |
| ep1, ep2, ep6 | Q1, Q2, Q6 | square, standing | 740 |
| ep3, ep5a, ep5 | Q3, Q5A, Q5 | school, standing | 740 |
| ep4 | Q4 | dining round table | 840 |

Every possible attendee has approved smooth source frames, including all six
expression frames. No missing runtime file was found. Cast comes from each
session, never a fixed ten-person array. Existing dedicated seated art is retained.
Missing dedicated seats (Doto) now use the smooth dialogue source under the same
table mask; standing ensembles also use approved smooth art with aspect preserved.
Seat centers and name-button coordinates remain unchanged. No forced diagonal
mirroring was added. Doto's source was viewed; new drawing is not currently needed
for a front-facing torso, but hands/arm occlusion and relative head size still need
actual engine review. All four venue kinds require actual framing review.

## Validation and blockers

- Targeted meeting tests: 62 passed (direction, source profiles, flow, venue tests).
- Full Python suite after source integration: 381 passed; result recorded
  in `validation.txt`.
- Existing review captures at `review/meeting-20261017` commit
  `a1993120b26b21e4d24f6af98e41b1e3082d968c` were viewed (all four PNGs).
  Those are **before** images, not evidence of this patch.
- No actual engine captures were produced. Ren'Py 8.5.3 SDK setup failed with
  `curl: (56) CONNECT tunnel failed, response 403` from the official SDK URL.
  There was no installed SDK. No alternate download/bypass was attempted.
- Library skill read returned `skill package is not available`. Official
  `prepare_materialize` returned signed transfers, but both downloads failed with
  `URLError <urlopen error Tunnel connection failed: 403 Forbidden>`. The one
  authorized retry to this consumer's workspace failed identically. The later
  explicitly supplied Git source path succeeded and its bytes were verified.
- Ren'Py lint, new screenshots, browser checks, real save/load/rollback and actual
  hand/table/head/gaze composition remain **unverified**, not passed.

Suggested engine follow-up: `dev/run_renpy_tests.sh meeting_direction
meeting_granny_startle`, then C2 first statement/Buri reply/E07/E08, C3 E12/angry
conclusion, C2 E09 and E10 wrong/correct counters; both motion settings; record
cancel/save/load/rollback; and representatives of all sessions in the table above.
