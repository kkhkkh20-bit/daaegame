# Local-only story handoff

Apply only after the separately required remote-write approval. This bundle is not art PR14 and not the default-off character grid candidate.

Base main .66: 24ce3b6037093a562f0bd9b1c35c64a9b690a13d. DELIVERY_MANIFEST records exact Git blob preimages and new blobs. New recommended files use their own prefix. game/screens.rpy has only the title entry added to the base; if art/grid work changed screens, apply that small insertion rather than overwriting the entire file. Existing Start() is preserved.

Run pure tests from dev with `python -m unittest discover -p 'test_recommended*.py'`, plus `test_full_recommended_route`. Tests can use R13_BASE_GAME pointing to exact base game. Default uses local base-game, otherwise full current game checkout. Source/AST checks are not RenPy lint.

Native fixtures in game/qa_tests/recommended_*.rpy are UNRUN. Use only official RenPy 8.5.3 workflow after approval; no bypass of unavailable local environment. Run lint and native fixtures, retain logs/screenshots, and fix failures before claiming engine verification. The first fixture contains an explicitly identified admin action harness; field ep1/ep2 fixtures exercise actual scene navigation. Direct-entry episode fixtures seed earlier state and cannot substantiate the preceding story.

Piko contact and fire sightline geometry gates must remain False unless the actual source artwork is reviewed against the precise physical claims. Do not set them True merely because an icon exists. Old broad-standing-lamp proposal under art/piko-contact is excluded. New close-ups preserve the existing tapered hanging lantern, with proposed normal maintenance on the bench.

The new route is isolated and labeled a verification campaign. This is not proof that every selected story is fully deployed: native execution, final artwork integration and semantic/visual review remain explicit outstanding items in IMPLEMENTATION_STATUS.md and the independent review report.
