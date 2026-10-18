# Ren’Py 기본 기능 우선 검토

기준 SDK: 설치된 **Ren’Py 8.5.3**. 온라인 공식 문서는 현재 8.5.4로 표시되므로 사용 가능한 기능은 로컬 문서/소스로 재확인했다. 엔진 업그레이드는 하지 않았다. 이전 전체 후보는 `63d48c07`의 [투명선·템포 영상](../meeting-tempo-review/after.mp4). 최신 요청의 인터럽트 전후는 이 폴더의 `before.mp4` / `after.mp4`(각 약 10초)다. before는 native ATL/오디오 적용 후, 인터럽트 강화 전 실제 녹화의 11.3초부터 10초를 정상 속도로 잘랐다. after는 같은 C2/E35 자료를 실제로 제시하는 별도 실제 녹화다. 오디오 후합성 없음. main 배포 없음.

## 최신 요청: ‘잠깐만요!’ 인터럽트

기존 `r13_meeting_objection_appear`는 정의만 있고 실제 타이포 이미지에 연결되지 않았다. 승인된 `room13-ui-objection01917.webp`에 ATL을 연결했다. 표시 시간은 동작 켬 **0.68→1.68초**, 동작 끔 **0.42→1.42초**, 각각 정확히 1초 추가다. 음성 길이 변경이 아니다. 기존과 같이 사용자가 클릭/스킵하면 조기 종료할 수 있는 pause 동작은 유지한다.

- 글자: 시작 zoom 1.30 / xoffset -160 / alpha 1(첫 프레임부터 보임) → easeout 0.14초에 zoom 1.04 / xoffset 8 / alpha 1 → ease 0.10초에 zoom 1.0 / xoffset 0 정착. 이후 안정적인 홀드.
- 회의 장면: 기본 ATL의 짧은 x/y offset 시퀀스(-8/+8/-5/+4/0px, y ±2px), 총 0.18초. 제목·발언 인용 UI는 흔들리는 fixed 밖에 두었다. 지속 흔들림/강한 점멸/노란 채움 없음.
- 동작 끔이면 이동·확대·흔들림 시간을 0으로 하며 표시만 1.42초다. 기존 `sfx-present.wav` 유지, 새 외침 음성 없음.

## 기본 기능으로 바꾼 두 부분

1. **투명 가로선: 수동 Canvas와 alpha/x 이동 계산 → ATL.** `r13_meeting_speed_lines_atl`에서 `animation`, `parallel`, `linear`, `pause`를 사용한다. 등장 20ms / 유지 40ms / 소멸 90ms, 총 150ms. 6개 Solid의 alpha 최대 .12, 두께 1px, 같은 색/좌표/방향을 유지했다. 노란 채움·불투명 카드·새 효과는 없다. `R13MeetingOrbit`가 이미 사용하는 shot 경과 시간을 ATL의 animation time으로 전달해, 새 대사/displayable 생성 때 처음부터 재시작하지 않는다. 사건/저장 값은 그대로다.
2. **음악 이어 재생: play + queue → 기본 partial playback `<from 위치 loop 0>`.** SDK `renpy/audio/audio.py:395`의 `split_filename`은 첫 재생에 from, 이후 루프에 loop를 적용한다. `play(..., loop=True)` 한 호출로 같은 의미를 표현해 추가 queue 호출을 제거했다. 문맥 복귀에도 같은 방법을 사용한다. `<from …>` 정규화, 실제 재생 위치, user mixer, 템포 단계 규칙은 보존했다.

## 공식 기능과 현재 경로의 맞음새

| 기능 | 8.5.3 지원 / 현재 판단 |
|---|---|
| ATL `linear`, `ease`, `easein`, `easeout`, `parallel` | 지원. `ease`는 시간 보간 곡선이며 FPS 생성 기능은 아니다. 작은 가로선에는 일정 속도인 linear가 요청에 맞아 채택했다. |
| `Transform` / `At` / xoffset / alpha | 지원. 기존 `R13MeetingOrbit` 같은 creator-defined displayable에도 적용 가능. 이번 선은 6개 Solid+Fixed에 At(ATL)을 붙였다. |
| `camera` / `show layer` | 지원. camera는 명시적으로 해제할 때까지 유지, show layer는 다음 scene에서 해제되는 차이가 있다. 현재 회의는 `screen r13_meeting_stage`의 `add R13MeetingOrbit(...)` 경로다. `camera master`로 이 screens 내부 장면만 이동시킬 수 없고 `camera screens`는 제목/대사/버튼까지 움직일 수 있다. 이번에는 레이어 분리 구조 변경을 하지 않았다. |
| 배경 자체 가로 이동 | 배경 displayable만 Transform/ATL로 이동하는 것은 가능하다. 다만 현재 Orbit는 좌석 투영·인물 크기·배경 타일·탁자 가림을 함께 계산한다. 2D xoffset 하나가 이 전체 시점 계산을 대체하지는 않는다. Orbit 전체를 감싸면 전체 합성 장면을 평면 이동시킬 수 있지만, 최신 요청은 최소 투명선이므로 새 배경 이동 후보를 임의로 더하지 않았다. |
| `hpunch` / `vpunch` | 기본 0.25초 수평/수직 흔들림을 지원하며 공식 문서는 맞춤형 변형에 ATL을 권한다. 이번에는 대사 UI를 제외한 회의 장면에만 적용하기 위해 0.18초 ATL offset 시퀀스를 사용했다. |
| `Dissolve`, `CropMove`, `PushMove`, `MoveTransition` | 지원. 서로 다른 scene/displayable 전환에 쓰는 기능이며, 현재 동일 Orbit 내부의 view 값 변화에 `with ease`만 붙여 좌석 시점을 자동 보간할 수는 없다. MoveTransition류는 공식 문서상 with를 통한 layer 전환 제약도 있다. |
| `blur` transform property | **지원한다.** 다만 자식을 먼저 flatten한 뒤 흐리게 하며 변하는 그림에서 artifact가 날 수 있다고 명시돼 있다. 방향성 motion blur와 동일하다고 말할 수 없고 렌더 비용 절감도 보장하지 않는다. 요청 범위를 넓혀 추가하지 않았다. |
| `fps` property | 지원하지만 transform 시간을 불연속화하여 **낮은 FPS를 흉내 내는** 속성이다. 60으로 적어 실제 렌더가 60fps가 되지는 않는다. 사용하지 않았다. |
| `renpy.render` / `renpy.redraw` | CDD의 공식 경로. redraw는 재그리기 요청이며 지정 시각/FPS 보장 API가 아니다. 기존 장면 합성에 유지한다. |
| music channel / queue / set_volume / get_pos / partial playback | 모두 지원. 현재도 이 기본 오디오 기능을 사용한다. 단일 normal channel은 파일 하나씩 재생하므로 fadeout/fadein을 진짜 겹침 crossfade라고 부르지 않는다. 필요하면 별도 채널 두 개로 가능하나 상태/볼륨/동기 관리가 늘어 이번에는 확장하지 않았다. |
| pitch-preserving tempo | 로컬 audio filter 문서에서 즉시 대체할 내장 tempo API를 확인하지 못했다. 기존 Rubber Band pitch=1 파생 파일과 native music channel 사용을 유지한다. BPM/마디 정렬은 미확정이다. |

## 스킵 / 로드 / 롤백

- 기존 `renpy.is_skipping()`, `renpy.in_rollback()`, 사용자 motion 설정으로 선을 생략한다. ATL 자체가 모든 커스텀 상태를 자동으로 deduplicate해 주는 것은 아니므로 shot revision / 동일 화자 guard를 유지했다.
- 회의 단계 milestone은 default 저장 상태, 선 displayable은 표현이다. 새 개인 압박/서사 사건을 추가하지 않았다. 이전 실제 저장/로드·Ctrl 스킵·mute·무음 복귀 검사는 [state-report](../meeting-tempo-review/state-report.json)를 재사용하며 이번 변경은 단위 검사와 실제 회의 영상으로 재확인한다.
- **기존 롤백 진단 보완:** SDK `renpy/game.py:301`의 `call_in_new_context`는 새 문맥 안의 rollback을 비활성화하고 save/load는 최상위 문맥에서 처리한다고 명시한다. 현재 자료 제시가 이 기능을 사용한다. 따라서 자료 제시 중 롤백 제한에는 엔진 기본 동작이라는 명확한 근거가 있다. 다만 이전 PageUp/휠 실패 시점의 문맥 깊이를 기록하지 않았으므로, 관찰된 모든 실패가 이 이유라고 단정하지 않는다. 기존 중복 checkpoint 가능성과 구분하며 story rollback 정책을 바꾸지 않았다.

## 근거

로컬 `/workspace/renpy-sdk/renpy-8.5.3-sdk/doc/`의 `transforms.html`, `transform_properties.html`, `displaying_images.html`, `transitions.html`, `audio.html`, `cdd.html`; SDK `renpy/atl.py`, `renpy/audio/audio.py`, `renpy/audio/music.py`, `renpy/game.py`.

공식 문서: [ATL](https://www.renpy.org/doc/html/transforms.html), [transform 속성](https://www.renpy.org/doc/html/transform_properties.html), [camera/layer](https://www.renpy.org/doc/html/displaying_images.html), [전환](https://www.renpy.org/doc/html/transitions.html), [오디오](https://www.renpy.org/doc/html/audio.html), [CDD](https://www.renpy.org/doc/html/cdd.html).

## 남는 한계

기본 기능을 사용해도 기존 Orbit의 합성 비용·그림 디코드·브라우저 CPU/GPU 제약은 남는다. 낮은 렌더 빈도의 원인을 분리한 프로파일링이나 실제 기기 60fps 검증은 하지 않았다. 20ms 등장 구간이 모든 기기에서 별도 프레임으로 보인다는 보장도 없다. 원작 전환과 같다고 설명하지 않는다. 새 외침 음성은 뒤로 미뤘으며 기존 `sfx-present.wav`를 유지했다. 군중 A/B·금관 A/B는 제외 상태다.

Native 오디오 검증: `native-loop-diagnostic.json`은 실제 브라우저에서 86.176초 곡을 85.800초부터 재생한 뒤 loop 0으로 곡 처음에 돌아온 재생 위치를 기록한다. 이 진단은 영상 뒤의 별도 오디오 검사이며 story/회의 stage/volume/mute 값은 변하지 않았다.

검수 완료: 최신 전체 단위 검사와 Ren’Py lint 통과(`check.log`), 공식 빌드의 모든 transport part SHA256와 ZIP CRC 검증. 실제 C2/E35 제시를 유음 녹화하고 정착 후 타이포/인용문 가독성을 확인했다(`settled-hold.png`). 이전 native 전체 회의 경로에서도 기존 판정/압박·템포 상태를 유지했고, native loop 0 실측은 85.889초→0.017초로 돌아왔다. 낮은 렌더 빈도의 원인 해결이나 새로운 외침 음성 완성을 뜻하지 않는다.
