"""2026-10-25 이야기 인계서·대본·편집 JSON·그림 요청서 다운로드 묶음 생성."""
import json,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/story-workbench/claude-handoff-20261025.zip'

def build():
    docs=ROOT/'docs'
    inv=json.loads((docs/'dialogue-modules/inventory.json').read_text())
    files=[docs/'HANDOFF_CLAUDE_20261025.md',docs/'STORY_HANDOFF.md',docs/'design/VOICE_GUIDE.md',docs/'CODEX_OPERATING_GUIDE.md',docs/'art-requests/그림_제작_요청서.md',docs/'dialogue-modules/GUIDE.md',docs/'releases/RELEASE_0.20.54.md']
    files += [docs/'reviews/dialogue-early-20261025/README.md',docs/'reviews/dialogue-early-20261025/수정전후.md',docs/'reviews/dialogue-final-20261025/README.md']
    files+=sorted((docs/'dialogue-modules/reading').glob('d*.txt'))
    files+=sorted(p for p in (docs/'reviews/dialogue-through14-20261025').glob('*') if p.suffix in ('.md','.json'))
    missing=[str(p) for p in files if not p.is_file()]
    if missing:raise FileNotFoundError(missing)
    readme='''# 이야기 인계 묶음 · 0.20.54

먼저 docs/HANDOFF_CLAUDE_20261025.md를 읽으세요.
1~14일 합본 TXT에는 서로 다른 분기가 함께 있고 별도 JSON 블록은 부록입니다. 실제 재생 순서·모든 조합 자연 플레이 기록이 아닙니다.
편집용 최신 파일은 dialogue-edit-all.json입니다. text/review_status만 고치고 저장소에서 dev/dialogue_modules.py check로 검사합니다. 이 파일은 생성 시점 소스 기준이며 원본이 바뀌면 최신 작업실에서 다시 내려받아야 합니다.
docs/reviews/ 아래 edits.json은 적용 전 기준의 검수 증거이므로 재적용용이 아닙니다.
이 묶음에는 게임 실행 파일·그림 원본은 없습니다. 게임은 저장소 main을 기준으로 이어받으세요.
'''
    with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        z.writestr('먼저읽기.md',readme)
        for p in files:z.write(p,p.relative_to(ROOT))
        z.writestr('dialogue-edit-all.json',json.dumps(dict(schema='room13.dialogue-edit.v1',source_stamp=inv['stamp'],entries=inv['rows']),ensure_ascii=False,indent=2)+'\n')
    return dict(file=str(OUT.relative_to(ROOT)),bytes=OUT.stat().st_size,source_stamp=inv['stamp'],entries=len(inv['rows']))

if __name__=='__main__':print(json.dumps(build(),ensure_ascii=False,indent=2))
