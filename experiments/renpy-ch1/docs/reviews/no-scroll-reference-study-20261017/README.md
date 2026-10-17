# 질문 목록의 스크롤을 없애는 UI 검토

2026-10-17. 공개 게임은 변경하지 않은 검토용 화면이다.

## 다른 게임에서 확인한 방식

외부 게임은 직접 실행한 것이 아니라 공개된 실제 플레이 스크린샷과 설명서·가이드를 조사했다. 아래 이미지의 저작권은 각 원권리자에게 있다.

| 게임 | 확인된 방식 | 다람탐정에 가져올 점 |
| --- | --- | --- |
| Ace Attorney Investigations Collection | 질문 목록과 Present가 별도 조작으로 배치된다. 해당 사진에는 질문 3개가 보인다. | 자료 제시를 질문 개수에 따라 밀려나는 마지막 항목으로 만들지 않는다. |
| Mass Effect | 화면 아래 공간에 답변을 나누고, 추가 조사 질문은 Investigate 하위 메뉴로 묶는다. | 긴 단일 목록 대신 공간 분배와 의미 있는 묶음을 사용한다. |
| Tangle Tower | 일반 질문, 인물, 증거를 탭으로 나눈다. 일반 질문에는 Encounter/Yourself/Yesterday/Statement/Suspicion이 있으며 일부는 진행에 따라 열린다. | 질문과 증거를 한 목록에 섞지 않고 기능을 구분한다. |

### 출처와 실제 게임 화면

- 역전검사: [공식 Steam](https://store.steampowered.com/app/2401970/Ace_Attorney_Investigations_Collection/) · [실제 화면](https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2401970/ss_eca16ad1b172021bd7116a6c877ee80f0366a202.jpg)
- Mass Effect: [공식 PC 설명서](https://eaassets-a.akamaihd.net/eahelp/manuals/mass-effect-manuals_PC_en_US.pdf), printed pp.10–11 · [Investigate 동작 설명](https://masseffect.fandom.com/wiki/Codex/Player_Tutorials) · [실제 화면 및 해설](https://blog.uat.edu/gaming-passion-series-part-5-dialogue) · [이미지](https://blog.uat.edu/hubfs/mass.png)
- Tangle Tower: [게임플레이 가이드](https://strategywiki.org/wiki/Tangle_Tower/Gameplay) · [리뷰와 실제 화면](https://buried-treasure.org/2019/12/tangle-tower/) · [이미지](https://buried-treasure.org/wp-content/uploads/2019/12/06_tangletower.jpg)

이 자료로 모든 게임이 질문을 3~4개로 제한한다고 결론 내릴 수는 없다. Tangle Tower의 증거 목록은 항목 증가에 따라 가로 이동도 사용한다. 참고하는 것은 기능 분리와 질문 묶음이며, 모든 화면이 스크롤 없다는 주장이 아니다.

## 실제 Ren'Py 비교 시안

부리에게 묻는 실제 작성된 질문 제목 8개를 동일하게 사용했다. 서로 다른 이야기 단계의 질문을 합친 레이아웃 실험이며, 실제로 동시에 해금된다는 뜻은 아니다. 질문 조건·대사·스토리는 변경하지 않았다. 테스트 질문 동작은 NullAction이다.

- **추천: 두 열 × 네 줄.** 질문을 한 화면에 펼치고 가운데 얼굴을 남긴다. 자료 보여주기는 하단 중앙 고정. [PC](pc-grid.png), [모바일 큰 글씨](mobile-grid.png).
- **비교: 네 개씩 명시적 페이지.** 전체 개수와 페이지 수, 다음 질문 개수가 보인다. 스크롤보다 다음 항목의 존재가 분명하지만 추가 클릭이 들고 가운데 얼굴을 가린다. [PC 1쪽](pc-paged.png), [PC 2쪽](pc-paged-2.png), [모바일 1쪽](mobile-paged.png), [모바일 2쪽](mobile-paged-2.png).

두 열 시안은 긴 제목이 모이면 빽빽해진다. 적용 시에는 질문 버튼을 짧은 주제명으로 다듬고, 클릭 후 실제 발화는 자연스러운 문장으로 유지하는 것이 좋다. 9개 이상은 아직 검증하지 않았으며, 명확한 주제 분류 또는 표시된 페이지 조작을 추가로 설계해야 한다. 숨겨진 스크롤로 넘기지 않는다. 중요한 분기 선택지는 일반 질문 목록과 구분해서 설계해야 한다.

## 검증 및 적용 상태

Ren'Py 웹 빌드 성공. Chromium에서 PC 1280×720와 모바일 844×390/큰 글씨를 캡처했다. 페이지 이동을 실제 클릭·터치하고 2쪽 진입 및 게임 진행 상태 불변을 확인했다. [검증 결과](report.json).

검토 전용 `room13_reference_layout_preview.rpy`를 추가했다. 공개 질문 화면에는 연결하지 않았다. 메인 머지·배포는 하지 않았다.
