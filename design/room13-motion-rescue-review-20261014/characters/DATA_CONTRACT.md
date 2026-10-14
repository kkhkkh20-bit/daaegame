# Daram motion gallery data contract v1

The portable build is `dist/`. Open `dist/index.html` directly or host that directory. It uses classic local scripts, not fetch, so it also works from file://.

`dist/gallery-data.js` assigns `window.DARAM_GALLERY`. `gallery-data.json` is the identical JSON data for tooling. Each character has `id`, `name`, `source` (base image descriptor), `states`, `references`, and `caveats`.

## States
Exactly four keys: `idle` (기본), `think` (생각), `surprise` (놀람), `startle` (화들짝).

```json
{
  "status": "pending",
  "note": "새 포즈·모션 제작 중",
  "pose": null,
  "frames": [],
  "layers": [],
  "timing": {"durationMs": 2400, "loop": true, "holdFrame": "last"},
  "motionDescription": "꼬리 레이어의 작은 좌우 움직임",
  "quality": {"poseReviewed": false, "motionReviewed": false}
}
```

Status: `pending` = no new state asset; `pose_only` = static state image; `motion_draft` = actual animated asset exists but needs visual review; `ready` = visually reviewed state and motion. Do not set `ready` from merely assigning CSS motion to the whole image. The UI separately derives whether actual moving layers/frames exist and downgrades inconsistent readiness.

Image descriptor: `{ "src": "assets/characters/daram.png", "width": 1024, "height": 1536, "crop": [x,y,width,height] }`. Crop is optional and always x/y/width/height (not x1/y1/x2/y2). Source image pixels stay unchanged; cropping is runtime-only.

`pose` is a complete state image, or the cleaned body plate when using separated layers. All state image, frames and layers must share the character coordinate system. The state's optional `viewBox: [x,y,width,height]` overrides the base visible content bounds. Optional `kneeCrop: [x,y,width,height]` provides an artist-authored knee-up crop; otherwise the gallery explicitly labels its 78% height preview crop as approximate.

## Frame animation

```json
"frames": [
  {"image": {"src":"assets/motion/daram/surprise-0.png","width":1024,"height":1536},"durationMs":90},
  {"image": {"src":"assets/motion/daram/surprise-1.png","width":1024,"height":1536},"durationMs":120}
]
```

Frames replace the pose, and can be complete frames or same-sized cleaned body frames plus layers. Use timing.loop=false for surprise/flinch. Final frame holds until replay/state change. Reduced motion renders the final complete frame with no interpolation. Multiple references to the same still image do not count as actual frame animation.

## Independent layers

```json
"layers": [{
  "id":"tail",
  "role":"tail",
  "image":{"src":"assets/motion/daram/tail.png","width":1024,"height":1536},
  "z":-1,
  "pivot":[450,950],
  "keyframes":[
    {"at":0,"rotation":-2,"x":0,"y":0},
    {"at":0.5,"rotation":2,"x":0,"y":0},
    {"at":1,"rotation":-2,"x":0,"y":0}
  ]
}]
```

Layer image uses the same coordinate system as pose. Its optional `rect: [x,y,width,height]` changes its destination position/size. `z<0` is behind the base; otherwise it draws in front. Motion is linear between keyframes; `at` is normalized 0..1; supported fields: x/y source pixels, rotation degrees, scaleX/scaleY (default 1), opacity (default 1). A layer can override `timing` and set `reducedMotionAt` (0..1, default 0). **A moving tail layer requires the tail removed from the base pose** so no double tail appears. No synthetic tail motions are enabled for unseparated full-body artwork.

## Timing defaults
- idle: 3200ms loop; subtle independent tail/ear movement only
- think: 4200ms loop; slow independent hand/tail movement
- surprise: 650ms one-shot, hold final expression
- startle: 820ms one-shot, hold final expression

## Integrating produced assets
Copy assets under `dist/assets/motion/`, preserve paths relative to dist, then update the character states and regenerate the JS assignment from JSON. Alternatively write a `motion-overrides.json` with `{ "characters": [{"id":"daram","states":{...}}] }` and run `python build_gallery_data.py --overrides /absolute/path/motion-overrides.json`. The script preserves source PNG bytes and merges state fields. Run `python validate.py` afterward. No GitHub or Sites publication is done by this project.

## Atlas and body-reaction extension
`frame.sourceRect: [x,y,w,h]` overrides `frame.image.crop`. `frame.rect: [dx,dy,w,h]` is the destination rectangle in state coordinates, allowing source cells of unequal width and per-frame anchor registration. Check actual PNG size and alpha gaps before assuming an equal grid.

`bodyMotion` takes the same pivot/keyframes/timing fields as a layer but transforms only the body pose/frame. Intended for explicitly labeled whole-body recoil/flinch. It is never described as tail motion, and is counted as motion only if properties actually change. Sample: `{"role":"whole_body_flinch","pivot":[240,515],"keyframes":[{"at":0,"y":0},{"at":0.15,"y":-12},{"at":1,"y":0}]}`.

## Review-only extensions (v6)

- `state.displayBox`: optional crop/viewport overriding `viewBox` for display. It does not rescale source frames. Daram and child Bami use equal 400×550 viewports with a common feet baseline; Bami's idle visible source height is 496px versus Daram522px (95.019%). Do not independently fit their silhouettes when comparing height.
- `character.originalSource`: preserved earlier static source `{image,viewBox,sha256,version}` when an explicitly requested redesign becomes the selected `source`. The original43 PNGs remain byte-identical in `assets/characters`.
- `character.styleCandidates[]`: optional unselected style variants with `{id,label,states,caveat}`. These never replace `character.states` by merely existing. The gallery shows first-frame comparisons in a closed details panel. Yeoni and Librarian large-head v3 variants are intentionally not default selected.
- `styleReviewStatus`, `designReviewStatus`, `motionRevision`: review metadata only. They cannot make a state ready; `motion_draft` remains authoritative until motion and art approval.
- Pixel-grid rendering modes are temporary viewport derivatives: original-nearest, world2px, close3px, side-by-side. They do not edit PNGs, fix drawing style, or reproduce the game's scene-dependent head scaling.
- Story review: `dist/story/inventory.json`, 85 usage records, 73 unique PNGs (54 background +4CG atlases +15new). Twelve CG use-crops are not twelve independent PNGs. Four UI records are specifications, not missing images. M06 states are explicitly held for continuity defects.
- Audio review pages never autoplay. Actual listening and game integration remain pending. Saved external provenance HTML is retained as inert `.html.txt`, not executable same-origin pages.
