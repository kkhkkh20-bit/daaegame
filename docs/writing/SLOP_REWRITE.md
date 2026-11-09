# 한국어 윤문 도구 설정

2026-11-09. 소유자가 지정한 [slop-rewrite](https://github.com/byungjunjang/slop-rewrite)를 Codex·Claude Code의 전역과 이 프로젝트에 연결했다. 본체는 `/workspace/tools/slop-rewrite`, 고정 커밋은 `b6d301120cfa0ceec90b80907f6110995dcc7395`다. 설치값은 [설정 파일](../../tools/slop-rewrite.json)에 둔다.

## 쓰는 범위

- 한국어 글의 윤문·퇴고·AI 티 제거·문장 검토에서 `slop-rewrite`를 부른다. 성능 측정·코드 리뷰·게임 플레이 검수는 기존 절차로 한다.
- 이 게임의 대사와 소설은 `--guide 없음`으로 시작한다. 업무·블로그 문체와 분량 지표를 등장인물에게 강요하지 않는다. 사용자가 가이드를 따로 지정하면 그 지시를 따른다.
- `검토`는 발견과 근거만 남긴다. `윤문`은 원본 옆에 `.taste` 결과와 `.taste-notes.md`를 만든다. 검사기는 원문을 자동 교정하지 않는다.
- 검사 통과는 재미·자연스러움의 판정이 아니다. 앞말에 답하는지, 그 시점에 인물이 아는 사실인지, 감정과 행동이 맞는지는 사람이 문맥과 실제 화면으로 다시 본다.
- 작업본에서 문장을 고쳐도 원본 기록 ID·변수·태그·증거·정답·분기를 자동 변경하지 않는다. 게임 반영은 기존 대사 반영 절차와 검증을 거친다. 사용자 지시와 정본이 먼저다.

## 확인과 호출

저장소 루트에서 실행한다. 기본 검사에는 Python 표준 라이브러리만 필요하다.

```bash
python3 tools/slop_rewrite.py --status
python3 tools/slop_rewrite.py --guide 없음 --hint /절대/경로/원문.md
python3 tools/slop_rewrite.py --guide 없음 --bundle /절대/경로/원문.md
python3 tools/slop_rewrite.py --guide 없음 --orig /절대/경로/원문.md /절대/경로/원문.taste.md
```

`--bundle`은 검토 담당이 읽을 자료를 출력한다. 문장을 실제로 고치는 것은 LLM 담당이며, 쓰기 훅이나 자동 치환은 설치하지 않았다. 자연어로는 “이 대사본을 검토만 해줘”, “이 문서를 가이드 없이 윤문해줘”라고 요청할 수 있다.

## 취향과 문체

기존 대화에서 명시된 대사 피드백만 로컬 `taste/`에 정리했다. 독자에게 없는 배경지식을 전제하지 않기, 앞말에 이어지는 대답, 가족 부재·사망에 맞는 반응, 한 사건의 추리 목적을 분명히 하기다. 사용자 작품 다섯 편을 분석해 만든 작가 문체 가이드는 아니다. 따라서 `styleguide-builder`는 연결만 했고 새 작가 가이드는 만들지 않았다.

개인 취향 문서·원문 코멘트·원장은 `/workspace/tools/slop-rewrite/taste/`에만 있으며 본체의 `.gitignore`로 제외된다. 공개 게임 저장소에는 넣지 않는다. 새 취향은 사용자가 저장을 요청한 경우에만 `taste-builder`로 추가한다. 외부 발행은 기본으로 하지 않으며 별도 지시가 있을 때만 한다.

## 설치를 복구할 때

```bash
mkdir -p /workspace/tools
git clone https://github.com/byungjunjang/slop-rewrite.git /workspace/tools/slop-rewrite
git -C /workspace/tools/slop-rewrite checkout --detach b6d301120cfa0ceec90b80907f6110995dcc7395
```

프로젝트의 `.agents/skills/`와 `.claude/skills/`에는 본체 경로를 가리키는 세 진입점이 있다. 이 환경의 `~/.agents/skills/`와 `~/.claude/skills/`에도 같은 세 진입점을 설치했다. 다른 환경에서는 경로와 기존 파일 유무를 먼저 확인하고 진입점을 연결한다. Codex 목록에 바로 보이지 않으면 새 작업을 시작해야 할 수 있다. 개인 취향은 공개 저장소에서 복구되지 않으므로 비공개 백업이나 사용자가 제공한 피드백으로 별도 복구한다.
