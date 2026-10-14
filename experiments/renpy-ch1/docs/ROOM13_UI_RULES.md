# Room13 UI rules

- Default field is investigation. Select a visible person to talk. The same people remain when entrance permission changes without time passing.
- Bottom actions: 조사 (return to field), 제시 (current partner only), 기록 (evidence/testimony/people/history), in compact translucent cells without a full-width opaque bar. 옵션 (save/load/settings) is a separate upper-right gear. Map and adjacent destinations remain distinct. Right-click does not open options.
- Finish the active line/choice before investigation or presentation; reading records and options never jumps out of the dialogue call stack.
- Acquired evidence appears with its icon/name and a short sound. Reinspection does not award or announce a duplicate. Everyday observations do not pretend to award evidence.
- One physical bundle has one field target; its contents are examined in a close-up. Evidence and testimony share two-row icon pagination with an explicit category, detail, acquisition source and current-run ownership.
- Proof limitations remain in story/rules, not repetitive UI disclaimers. Do not expose future evidence, meeting times or mystery answers.
- Questions use spoken Korean, opaque-enough dark scrim, centered text, clear strikethrough/dimming when read; rereading remains available.
- Father is the player viewpoint: no small avatars in any Room13 dialogue. The conversation partner appears on stage and remains during Dad’s reply; Dad never replaces them. Inner thoughts use blue parentheses. Nameplate and dialogue panel are centered, body left aligned with symmetric 40 px inset. Character profiles remain in records; cinematic art is preserved.
- Arrival cards use actual story day, weekday, period and canonical location. No invented calendar date or minute precision.

## Typography

Common definitions: game/room13_typography.rpy. Body uses real Galmuri11 Regular. Current pixel family has no bundled Light/Medium/Black; keep Regular rather than synthesize weights. The existing title font is a real Bold. Italic requires asking the user.

Small Korean secondary text stays Regular with sufficient contrast. Emphasis colors have semantic roles (person, place, evidence, testimony, thought); no arbitrary rainbow hints. Dark and paper backgrounds have separate foreground tokens.

Container padding roles: button/row=(18,12), compact=(12,8), panel=(24,20), name=(16,8). Values are horizontal, vertical logical pixels at 1280×720. Update shared roles globally. Fixed hitboxes and no-padding artwork containers are geometry exceptions. Check mobile landscape wrapping and touch areas after changing sizes.

## 0.15.5 읽기와 기록

- `r13_read_size(base, large)`와 `persistent.room13_large_text`를 읽기 크기의 단일 기준으로 쓴다. 웹에서도 옵션으로 직접 켜고 끌 수 있으며 Regular 글꼴을 유지한다.
- 기록은 일반 6열×2행, 큰 글씨 4열×2행이다. 페이지 계산·선택·렌더 모두 `r13_record_page_size()`를 사용한다.
- 최근순은 이번 저장의 실제 획득 목록을 역순으로 표시한다. 같은 날짜/시간대 자료도 획득 순서를 보존한다.
- 관심 표시와 읽음은 `room13.record_ui`에만 저장한다. 증거 보유·스토리 플래그·시간·인물 신뢰도는 변경하지 않는다.
- 문서 소유와 비교 수행을 구분한다. `gate_documents_compared`는 초소 비교창에서 동일 항목의 차이를 직접 비교했을 때만 기록한다.
- 증거 아이콘은 원화 atlas와 명시적 crop 메타데이터를 사용한다. 제시/획득/기록에서 같은 아이콘을 쓴다.

## 0.15.6 시점과 생활 배치

- 작은 대화 프사는 사용하지 않는다. 인물 기록용 프사는 유지한다. 아빠가 먼저 질문하는 대사도 해당 상대를 먼저 보여 준다.
- 질문 목록과 초면 접근 화면은 명시적인 돌아가기를 제공한다. 접근 취소는 실제 만남으로 기록하지 않는다.
- 화면 중앙 좌표의 절대 픽셀 계산에는 정수를 쓴다. Ren’Py의 float xpos는 화면 비율이므로 나눗셈으로 실수가 되지 않도록 한다.
- 현장 인물은 정지한 생활 포즈다. 대화 인물 움직임 설정은 1:1 대화·질문 화면에만 적용한다.
- 넓은 현장은 드래그/스와이프로 이동한다. 별도의 좌우 둘러보기 막대·화살표는 표시하지 않는다.
- 현장에는 해당 장소·요일·시간에 실제 일정이 있는 주민만 배치한다. 집에 머무는 상태는 실외 슬롯으로 대체하지 않는다. 사건 필수 등장·구금·사망·피난 규칙이 평상시 일정에 우선한다.
- 가구 사용 포즈는 실제 배경 가구의 접점에 배치한다. 할머니는 접수대 바깥 전신, 토리는 기존 벤치, 도토는 게시판을 보는 뒷모습이다.
- 제시 카드 등장에는 source-page.wav를 show 이벤트에서 한 번만 재생한다. 획득 알림음과 구분하며 다시 그리기로 반복하지 않는다.
- 다람이 가족의 털색은 짙은 밤갈색, 얼굴·꼬리 무늬는 크림색이다. 회색 버전은 원본 백업으로만 보관한다.

## 0.15.8 첫 추리

- 도면은 빈 폭 → 붉은 연결선의 두 끝 → 가설의 세 단계로 직접 비교한다. 취소·오답·힌트는 증거와 시간을 바꾸지 않는다. 완료만 기존 map 활동의 E04와 시간 비용을 적용한다.
- 종이 도면과 실제 작동(E37/E05)을 구분한다. 도면 제시로 통로를 열거나 할머니의 실제 출입구 인정을 대신하지 않는다.
- 추리 메모는 이번 저장에서 확인한 사실·남은 의문을 보여주며, 다음 행동의 힌트는 사용자가 펼친다.
- 이미 E04를 얻은 이전 저장은 재수집을 강요하지 않는다. 첫날의 추가 제시 반응은 4일째까지이며 이후 사건 반응을 덮지 않는다.
- 재판의 제시 취소는 반드시 같은 논점으로 돌아간다. 일반 대화 label로 이동하지 않는다.
