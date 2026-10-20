# 제작기준본01 · D01 연결 검토

개발 브랜치 `story/production-basis01-demo`, 기준 `1085e4e5a6fdceda24e208a5975a2f6ac097bb4f`.
전달 커밋 `8e59ee44abcf768cd1920a6272fa3463008b1345`의 자료 폴더만 추출했다. 소스 병합·reset·배포는 하지 않았다.
원본 10개, 149,679,809바이트의 크기/SHA-256/Git blob SHA가 모두 일치했다.
transfer-manifest SHA-256: `8774f00b32a155c274e7a8ff45e52b2c46a9c752f24cdf09c3f745620f4a39bb`.
ZIP CRC 및 중복 경로 검사, 623개 파일 해제 후 VERIFY.py 전체 통과.

## 이번 범위

`MS14_D01_S01` 마차·편지 → `S02` 정차·처리 명단 → `S03` 조사·반박 →
`S04_B001`의 등록 완료 대사까지 연결한다. S04_L0012의 추가 질문 선택부터는 다음 작업 범위다.
기존 대사/블록/선택 ID와 본문은 원본 그대로 유지한다. 원본 전체분기 JSON과 CSV의 해당 18개 분기도 대조했다.
데모가 끝나면 메인화면으로 돌아가며, 기존 이야기 후반으로 합류하지 않는다.

`production-basis01-d01.json`은 원문 일부 추출물이다. 원문 해시를 포함하고
`dev/import_production_basis01.py SOURCE --check`로 모든 원문 필드의 동일성을 검사한다.
전체 14일을 실행하는 해석기나 완성본이 아니다. D02~D03·13호실·가족 그림·E01/M01 비교는 아직 미연결이다.

## 저장 상태와 원문 매핑

새 상태는 저장 가능한 `r13_basis01_state`의 단순 dict/list/bool/문자열이다.
Ren'Py가 호출 스택, 현재 레코드·대사 위치, 타이핑 진행과 롤백을 소유한다.
Python 함수는 이전 상태를 복사해서 반환하며 효과 적용 원장은 `record_id:effect_index`이다.
중간 효과 실행 도중 새 입력/저장 UI를 호출하지 않고, 원장과 수첩 획득을 같은 Python 문장에서 처리한다.

| 원문 | 엔진 상태 / 입력 | 초기값 및 변경점 |
|---|---|---|
| day / father·daram 생존·동행 | day, father_alive, daram_alive, father_with_daram, location | 1 / true / true / true / carriage. 정차 뒤 gate, 자료 확인 입력 뒤 guardhouse |
| input_completed(S01:2) | completed_inputs의 open_letter | 실제 ‘편지를 펼친다’ 입력 뒤 B002만 허용 |
| E01 | evidence의 E01 | S01_L0010 한 번 획득. 장면 진입만으로 지급하지 않음 |
| K01a / K01b | 같은 이름 bool | 마지막 줄/글씨 조사 결과. 재열람 중복 효과 없음 |
| letter_close_selected | 같은 이름 bool | 접기 입력. 조사 유무에 따라 B005/B006 하나만 재생 |
| carriage_stopped | 같은 이름 bool | Karo L0022 뒤 하차 입력. S02 진입 조건 |
| E02 | evidence의 E02 | S02_L0019 처리 명단을 읽은 뒤 획득 |
| E03 / E04 | evidence의 같은 ID | 신청 원본/규정 클릭 후 각각 L0002/L0007에서 획득 |
| purpose_difference_known | 같은 이름 bool | 목적 비교 B002 또는 정답 직행 B005에서만 true |
| reason_heard / K05 | 같은 이름 bool | 목적 차이를 아는 상태의 선택 질문 B010에서만 true |
| selected | 선택한 근거의 명시적 enum 목록 | 문서에 있는 항목을 플레이어가 직접 고름. 선택 표시만 사용하며 정답 강조 없음 |
| gate_basis_proven | 같은 이름 bool | E02/E03/E04 및 세 근거가 모두 있을 때 B004/B005 결과 |
| gate_registered / E05 | 같은 이름 bool / evidence ID | S04_L0008의 실제 정정 결과. 반박 성공만으로 지급하지 않음 |
| 물자·미확인 정보 | family_cookie=1, invitation_author=unknown, mother_location=unknown | 이번 구간에서 변경하지 않음 |
| 시간 | elapsed_minutes / completed_inputs | 하차 이동 5분, 원본·규정 상세 조사 각 15분 한 번. 오답·힌트·비교·재열람 0분. 날짜 변경 없음 |

모든 항목과 입력 대기는 저장 대상이다. 선택 중인 항목은 `pb01_selected`도 Ren'Py default 변수로 저장한다.
`enter_when`, block `when`, record `requires`, 효과와 선택 조건은 허용 목록과 직접 작성한 판정으로 매핑했다.
미해석 조건·효과·화자·scene은 예외로 중단한다. 문자열 eval은 없다.
분기표의 state_changes와 연출의 source_effects를 별도로 실행하지 않는다.

기존 E02/E03/E04와 뜻이 달라 기존 수첩에서는 `PB01:E02`처럼 이름공간을 사용한다.
원문 ID는 데이터 안에 그대로 보존되며, 기존 저장의 증거 정의를 교체하지 않는다.
기존 `r13_lines`, `choice`/질문 목록, 수첩·문서 상세·하단 도구 모음·저장 UI를 사용한다.
수첩에서 문서를 고른 것만으로 정답 처리하지 않고 근거 선택 입력으로 연결한다.

## 입력과 분기

편지의 세 선택과 정차 전 두 선택을 원문 옵션 ID로 구분한다.
신청서만 읽거나 규정만 읽은 상태로 정답을 제출해도 성공하지 않는다.
목적 비교 → 선택 질문/숙소 확인 → 제시와, 세 근거 즉시 제시를 모두 지원한다.
신청 인원만/까로 확인만 제시하면 원문의 불충분 답변으로 돌아간다. 힌트는 요청할 때만 표시한다.
다른 집 신청서 오답 B008은 판정에는 매핑했으나, 확인되지 않은 새 문서를 만들지 않으므로 이번 UI에서는 노출하지 않는다.

조사·선택·제시 전 기존 스킵을 종료하고 자동 진행을 끈다.
기존 choice의 0.35초 입력 장벽과 Ren'Py say의 첫 클릭 문장 완성 동작을 재사용한다.
기존 ‘마차 전체 건너뛰기’는 새 구간에서 표시하지 않아 필수 편지 입력을 통과시키지 않는다.
연타·저장·로드·롤백의 실제 Ren'Py 동작은 SDK 차단으로 아직 미검증이다.

## 자산·연출

전달된 마차와 입구 원화를 실제로 열어 확인했다. 마차는 저장소 원화와 바이트가 같다.
마차 초반은 원화의 오른쪽 좌석 `(650,0,736,780)`만 고정 배율로 보여 주고,
Karo의 S01_L0022 뒤에만 전체 창을 노출한다. 새 레이어나 무릎 위 과자 CG는 만들지 않았다.
착석 포즈가 없으므로 마차 좌석에 서 있는 전신을 배치하지 않고 대사와 기존 UI를 사용한다.
가족 그림·미승인 표정·DEV 물증·교정 문서 이미지·새 음원은 적용하지 않았다.
문서는 원문 텍스트로 기존 수첩에 기록하며, 날짜나 숫자를 새로 만들어 채우지 않는다.
전용 초소 내부·얼어 있는 발판·일치하는 손동작·초반 숲 팬은 미연출이다.
입구 기존 배경은 위치 안내용이며 초소 내부 구조 검증을 대신하지 않는다.

## 검수 증거와 차단

새 단위 테스트: `python3 -B -m unittest discover -s dev -p test_production_basis01.py -v`.
15개에서 편지/도착 선택, 두 문서 조사 순서, 정답 직행/정규 경로, 오답/힌트/재시도,
누락 근거 차단, JSON 저장 상태 직렬화, 효과 전후 복원과 중복 적용 차단을 검사한다.
이는 실제 Ren'Py 저장 파일이나 클릭 테스트를 대신하지 않는다.

중간 결과: 새 15개 통과. 전체 단위 검사 첫 실행은 743개 중 5개 실패였다
(`/tmp/pb01-unittest.log`). 새 연결을 넣으며 이동한 기존 소스 줄번호와 조건 문자열의
선택지 오인 문제를 수정했다. 기존 줄번호를 유지하므로 출처 자료를 다시 생성하지 않았다.
수정 뒤 실패 관련 4개 묶음과 새 묶음을 합친 49개 재검사는 모두 통과했다
(choice_length 1, override_map 3, dynamic_dialogue_bindings 12, dialogue_beats 18, production_basis01 15).
최종 수정 상태에서 전체 **743개가 34.554초에 통과**했다. 최종 로그는 `/tmp/pb01-final-unittest.log`이다.
원문 추출 동일성, 명시적 조건/효과 매핑, Python 모듈·Ren'Py init 내부/단일행 Python 구문,
모든 어댑터 call/jump 대상, 재사용 이미지 존재, git diff --check도 통과했다.
이 구문 검사는 Ren'Py 문법 검사(lint)를 대체하지 않는다.

공식 기존 절차 `RENPY_SDK_HOME=/workspace/daaegame-inputs/renpy-sdk bash dev/setup_sdk.sh`는
`curl: (56) CONNECT tunnel failed, response 403`으로 실패했다. SDK는 설치되지 않았다.
정확한 요청 대상은 공식 `https://www.renpy.org/dl/8.5.3/renpy-8.5.3-sdk.tar.bz2`이다.
메시지는 CONNECT 터널 단계의 접근 차단이다. 공식 원본 서버가 직접 403을 반환했는지는 확인되지 않았다.
이후 다른 호스트·프록시·부모 우회 전송으로 재시도하지 않았다.
추가 결제·권한 요청·네트워크 설정 변경·비공식 미러는 사용하지 않았다.
Ren'Py lint, 수정본 컴파일/웹 빌드, 실제 입력/저장/스킵, 게임 화면 캡처는 미실시다.
모바일·직접 청취·사람 재미 검수도 미실시다. 기존 웹판은 수정 전 0.19.67이며 새 구현의 증거로 제시하지 않는다.
모델·추론·실제 서비스 속도는 이 환경에서 확인할 수 없다. 임의 모델 전환은 하지 않았다.

## 기존 CI를 이용할 경우 필요한 입력과 한계

사용자가 개발 브랜치 게시·Draft PR·검사/빌드를 총 US$1 한도로 승인했다.
공개 저장소와 표준 Ubuntu runner를 다시 확인했다. 공식 과금 문서상 이 조합의 실행 시간은 무료다.
아티팩트는 두 workflow 모두 최대 100 MiB·1일 보관으로 제한한다.
이번 검토는 최대 4개 head 실행 묶음(각 두 workflow)을 한도로 진행한다.
최대 저장량을 모두 유료로 계산해도 공식 $0.25/GB·월 기준 총 $0.01 미만이다.
근거: https://docs.github.com/en/billing/concepts/product-billing/github-actions
금액은 이 작업이 추가하는 bounded artifact에 대한 상한이며 계정의 다른 작업 지출을 포함하지 않는다.
실행은 게시된 소스 커밋의 PR 이벤트를 사용하고 같은 head에 수동 실행을 중복하지 않는다.
`.github/workflows/room13-verify-build.yml`은 `workflow_dispatch`에 사용자 정의 inputs가 없으며,
실행 ref를 선택한다. 경로가 맞는 pull_request에도 반응하므로 PR은 단순 자료 게시와 구분해야 한다.

workflow는 Python 3.12, Node 22, xvfb 등 OS 의존성, Pillow/numpy/scipy,
공식 Ren'Py 8.5.3 SDK와 SHA-256 검증, 고정 과거 아트 커밋
`2ea4d41bb8918b74d95d9cb6dc0bb8705e3297fd`를 준비한다.
`dev/check.sh`가 전체 단위 검사와 Ren'Py lint를 실행한다.
이번 D01 검토에서는 기존 화면 테스트 6개 대신 전용 `pb01_input_save_skip`, `pb01_regular`를 실행한다.
기존 harness를 사용하고 시작 상태나 증거를 주입하지 않는다. 새 게임부터 실제 클릭/숫자키 입력,
편지 획득 전후 저장/로드, 재조사, 오답/힌트, 직행/정규 반박, 등록 후 저장/로드와 캡처를 포함한다.
실제 통과 여부는 각 CI run의 native-qa-summary와 스크린샷으로 판정한다.
현재 workflow에는 브라우저 테스트 단계도 없다.
`import_production_basis01.py --check`의 원문 대조까지 CI에서 실행하려면 별도로 검증된
`01_스토리기준본` 폴더를 제공해야 한다. 현재 sparse checkout에는 전달 폴더가 포함되지 않는다.

현재 설정의 자원 상한은 ubuntu-24.04 단일 작업 30분, 화면 진단 단계 12분,
dashboard 작업 10분, workflow별 업로드 최대 100 MiB 및 보관 1일이다.
Pages 설정은 main 브랜치 `/`의 legacy 빌드다. 개발 브랜치 게시와 PR은 main을 변경하지 않는다.
워크플로에는 push·merge·deploy 단계가 없으며 이번 작업에서도 실행하지 않았다.
