# Actor intent revision and art direction

Local only. No activation, commit, merge, push or deployment.

The teacher's “고맙습니다. 걱정 마세요.” now uses neutral in both
`ws:teacher:alone / 0` and `dynamic:223 / debate:conclusion_wrong:Q5A:weak / 0`.
The performance is warm, composed reassurance while the teacher maintains a
closed conviction that their own plan will protect the children. The teacher does
not yet know the later return of warmth. Dad's unease is not evidence that the
teacher visibly looks anxious. Nor does the bad consequence justify an anxious
portrait. No villainous smile or premature guilt is requested.

The same distinction changes the teacher's lullaby and spilled-soup cover story:
soothing/calm outward speech is separate from hidden despair or subsequent remorse.
Once the light has actually returned, the speaker can react to that new knowledge.
The later admission, collapse and crying require remorse/grief expressions, not
an automatic anxious assignment for a failed branch.

The audit re-read Q5A/Q5, the surrounding school/soup sequence, Chorong's encounter,
and the cart/altar sequence. It inspected outcome-worded rationales across the review
catalogs, then replaced the two broad teacher/cart rationales with individual
speaker-intent explanations. It also checked static reasons mentioning endings,
survival and failure: an actor responding to something already witnessed is
separate from an actor displaying the author's knowledge of a future outcome.
`actor-intent-audit.json` records the old/new decisions and exact source references.
This is a focused re-review of risky defaults, not an assertion that every earlier
line has received a second independent semantic review.

`performance-resource-requests.json` separates experienced affect, visible acting,
physical state, and resource needs. In particular:

- Chorong `nt:night8:half / 1`: alive but collapsed, forehead injured, lantern broken.
  Request a collapsed/injured event body plus pain/remorse expressions and the scene
  prop. Generic standing anxious art is not a completed substitute; the dead branch
  must not be reused. Dialogue text is unchanged.
- Teacher lying beside the children: request lying-under-blanket event body and
  exhausted/resigned expression. Keep singular/plural dialogue variants intact.
- Quiet relief, grief, guilt, tearful relief and grief with resolve are explicitly
  requested for the relevant Bami, Chorong, Daram, Kkomi, Nero, teacher, Mom, Bori,
  Granny and Ppul contexts. Existing emotion enums are compatibility labels where
  marked, not approval of a generic happy/anxious face.

The example report now uses the actual carriage identity
`opening:carriage:daram:v4` and the actual Q5A weak conclusion route/identity above.
The previous `dynamic:607 / debate:Q5A:conclusion:weak` was a probe label, not the
real call site; it must not be used as a production scene ID.

## Approved style direction; resources still held

Dialogue uses clear storybook source masters. The new renderer uses smooth sampling
(`nearest=False`, `subpixel=True`) and accepts only entries explicitly marked
`storybook_source` / `source_master`, under `assets/dialogue-source-master/`.
The profile staging utility uses LANCZOS, preserves alpha and allows odd dimensions;
there is no 2px grid or pixel filter. Canvas, frame size and offsets must be explicit
layout decisions, not inferred from a mismatched pose. Its output is always HOLD
and does not write to the approved game registry.

Map investigation pixels and their paths are unchanged. Face, species, outfit,
colors and asymmetric props must match between the two uses. The received six-person
intermediate package remains HOLD because front-facing refinement is pending. The
active new-art registry still contains zero people. The staging utility has only
been tested with synthetic images, not used to approve or publish delivered art.
