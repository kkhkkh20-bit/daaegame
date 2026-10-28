# 자동 완주 검사

2026-10-28. 웹 빌드를 브라우저로 열어 1일부터 결말까지 플레이어처럼 눌러 가는 검사다.
화면 시험(xvfb)이 장면 하나씩을 본다면, 이것은 이어진 한 판 전체가 막히지 않고 끝나는지를 본다.
이 검사로 찾은 것: 11일 가설 회의의 예방 판 정답 공백, 4지선다 넷째 칸 화면 밖, 현장 인물 겹침 넷.

## 돌리는 법

```
cd experiments/renpy-ch1
python3 dev/build_web.py --sdk $HOME/.cache/renpy/renpy-8.5.3-sdk     # 공개본을 먼저 만든다
(cd ../.. && python3 -m http.server 8766 --bind 127.0.0.1 &)          # 저장소 뿌리에서 공개본을 연다
mkdir -p dev/qa-out && python3 dev/qa_autoplay.py > dev/qa-out/base.txt 2>&1   # 기본 길(약 30분)
ROUTE=alt    ROOM13_QA_OUT=$PWD/dev/qa-out/alt    python3 dev/qa_autoplay.py > dev/qa-out/alt.txt 2>&1
ROUTE=cheese ROOM13_QA_OUT=$PWD/dev/qa-out/cheese python3 dev/qa_autoplay.py > dev/qa-out/cheese.txt 2>&1
ROUTE=true   ROOM13_QA_OUT=$PWD/dev/qa-out/true   python3 dev/qa_autoplay.py > dev/qa-out/true.txt 2>&1
python3 dev/qa_layout_check.py dev/qa-out/base.txt                    # 겹침·가장자리 잘림
```

- 화면 시험·웹 빌드와 동시에 돌리지 않는다. 길 둘을 동시에 돌려도 느려져 시간 초과가 난다. 하나씩 돈다.
- 바뀐 구간만 볼 때는 `RESUME_DAY=N` 으로 저장 `auto-dayN`(그 날짜 아침)에서 시작한다. 저장은 같은 길(같은 브라우저 프로필)의 앞선 주행이 만든 것이다.

## 길

| ROUTE | 하는 것 |
|---|---|
| (비움) | 선택창마다 첫 선택지. 대부분 살리는 쪽 |
| alt | 선택창·현장 선택을 뒤에서부터. 예방 판·다른 인물 배치를 지난다 |
| true | 진엔딩 「새로운 아침」 예방 길. 관문·선택창마다 `TRUE_GATES`·`TRUE_CHOICES`(구동기 맨 위의 계획표, 사건마다 무엇을 막는지 주석)를 먼저 따르고, 계획에 없으면 기본 길과 같다. 회의 제출은 대승리 보너스 증거(`NW_NUBI_TICKET`·`NW_RETURNED_BOWL`)가 든 정답 묶음을 먼저 낸다 |
| cheese | 회의마다 기회가 셋 이상 남았거나 무제한이면 「전부 내기」, 「엉뚱한 하나」를 먼저 내고 판정을 적는다. 그다음 정답 |

## 로그 읽기

- `==== N일` 날짜, `SHOT` 캡처 이름, `선택`/`질문` 누른 것, `배치` 현장 인물 좌표(화면 기준 x·y·폭·높이·빈 자리 여부).
- 끝 줄 `ERRORS [] 시간 초` 가 정상 종료다. 바로 앞에 `메인 화면(결말)` 이 있으면 결말까지 간 것이다.
- `ERROR`·`STALE`(같은 상태 60바퀴)·`EXCEPTION` 이 나오면 멈춘 것이다. 게임이 막힌 것인지 구동기가 모르는 화면인지 캡처로 가린다.
- 꼼수 길: `꼼수 all|wrong 쟁점 낸 수 → 막힘|통과 남김 [...] 기회 a → b`.
  `CHEESE-PASS` 는 꼼수 제출이 통과한 것이다. 가진 자료가 정답·덧붙임뿐이면 정상(1일 첫 회의)이고, 아니면 결함이다.
  `CHEESE-KEPT` 는 전부 내기 뒤 자료가 남은 것이다. 비교 모드(둘까지만 고름)면 정상이다.

- 진엔딩 길 로그: `  값 키 이전 → 이후`(생사·회의·대승리·명단·결말 값이 바뀔 때마다), `MEETING-LOST`(회의를 짐), `TRUE-CHECK`(결말 판정 직후와 이야기를 마친 뒤 `r13_nw_true_ending_ready()` 결과와 못 맞춘 조건), `결말 이름`.

## 2026-10-28 결과

| 길 | 결과 |
|---|---|
| 기본 | 1~14일 완주, 겹침 0 |
| 다른 길 | 1~14일 완주(11일·12일·13일 수정 뒤) |
| 꼼수 | 1~14일 완주. 꼼수 제출 33건 중 통과 1건(정상), 전부 내기 뒤 남은 자료 0건(비교 모드 1건 제외) |
