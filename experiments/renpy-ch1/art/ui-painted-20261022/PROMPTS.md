# 이미지 생성 프롬프트 세트

도구: 내장 image_gen, transparent_background=true. 생성 후 PIL로 색, 크기, 외곽 알파와 상태별 테두리를 보정.

공통: Use case: ui-mockup. Production game UI sprite, hand painted storybook winter mystery visual novel. Warm walnut, antique gold, burgundy palette. Orthographic flat front view, no perspective, no cast shadow, no text letters icons or watermark. Genuine transparent exterior.

- name_ribbon: One isolated horizontal burgundy #7a1c24 dry brush stroke, aspect 4.4:1, sharp pointed left start, split bristle right end. Rich natural paint streaks and subtle pigment variations, central 60 percent evenly filled for horizontal stretching. No border, no ornament. Center with generous transparent margins.
- opt_tab: One isolated horizontal burgundy #7a1c24 dry brush stroke, aspect 3.125:1, thicker and shorter feeling. Pointed left start and split bristle right end. Hand brushed streaks, central 60 percent evenly filled for stretching. No border no ornament. Transparent margins.
- panel: One square walnut brown UI panel for nine slice scaling. Dark brown #3a281d at top subtly to #2a1c14 bottom, restrained fine painted pigment texture, flat uniform middle with no features. Two inset delicate antique gold outlines, outer darker 1.5px inner pale 1px at final 256px. Small graceful gold vine curls and circular ornaments confined to the outermost 48/256 of each corner. Border straight along sides, no decoration along middle edges. Nearly opaque fill. Rounded square corners, completely transparent exterior. Panel fills 95 percent of canvas.

버튼 공통: One nearly square rounded rectangle game button for nine slice at 96x88, corner radius 7 percent, fixed corners within 16/96. [상태별 문장] Very subtle hand painted pigment texture, even center suited to stretching. Simple delicate double edge, no diamonds, no symbols, no ornaments, no central highlight. Entire button fills 94 percent of canvas with transparent exterior.

- idle: Dark walnut brown translucent fill, thin antique gold outline.
- hover: Slightly brighter walnut brown fill, bright pale gold thin outline.
- selected: Burgundy #7a1c24 fill, bright pale gold thin outline.
- insensitive: Muted dark gray brown translucent fill, faded gray brown thin outline.
