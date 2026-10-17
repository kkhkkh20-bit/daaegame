# Smooth dialogue sources: 20 characters / 120 expressions

Original source masters only, without pixel derivatives. Each of the eight ZIP files is independently extractable; extract all into the same destination. They are not byte-split archive segments.

Use `smooth20-source-only-manifest.json` for character IDs, expression roles, source hashes and runtime guidance. The manifest is preserved byte-for-byte from preparation; its `github_uploaded: false` and `game_applied: false` fields describe preparation-time state, not this repository delivery. Uploading these sources does not itself apply them to the game.

Dialogue roles: neutral, joy, angry, anxious, surprise_talk. Use surprise_react briefly, then transition to surprise_talk. Use smooth texture sampling rather than nearest-neighbor pixel rendering. Preserve per-character size and pose anchors.

Existing six-character intermediate packages remain unchanged in the separate dialogue-gaze-20261017 folder. No main-branch changes are included in this delivery.
