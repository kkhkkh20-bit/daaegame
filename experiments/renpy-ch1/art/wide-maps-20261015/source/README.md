# Wide map first4 integration handoff
Only post/kitchen/dining/passage morning artwork in this batch. Runtime2160x720 viewport1280x720, camera0..880 and initial440. PNG names are final source references for this candidate, not already deployed.
post native2160x728 crop[0,0,2160,720]; others2172x724 uniform2160x720. Never stretch only x.
authored-coordinates.json has visually authored hitboxes and old rects, not passed runtime QA. No behind-table placement is supplied. Two front-floor slots for post/kitchen/dining, three for passage; crowded fixtures must resolve extra residents deliberately. No default old actor positions. Empty occlusion is intentional only for specified unobstructed front-floor slots, not universal proof that masks unnecessary.
Daylight afternoon/evening in production are pending; preserve old scene for those until matching variants arrive, or gate entire location replacement until all3 ready. Do not display morning image for evening as though final.
Code integrator must register scene aliases: post→winter_post, kitchen→kitchen, dining→council, passage→winter_passage. Existing r13_background world check can then dispatch them, but verify no newer wrappers override. Preserve all story unlocks, object IDs, evidence and choices.
Test every object with camera0/440/880, pointer mapping x+camera, all residents feet visible on true floor, all navigation paths, load/save/daylight. Do not announce completion without browser/game test receipt.
Do not include guestroom, character changes or unready hall/room13 in this batch.
