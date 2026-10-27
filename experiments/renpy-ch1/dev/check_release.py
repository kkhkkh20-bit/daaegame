"""공개 전 확인: 공개 묶음(preview/room13-dev/game.part01) 안의 판 번호가 원본과 같은가.

0.20.67 은 웹판을 만든 뒤에 판 번호를 올려 공개 화면이 0.20.66 으로 보였다(외부 리뷰 2026-10-27).
웹 빌드 직후, main 에 올리기 전에 돌린다. 다르면 0으로 끝나지 않는다.
"""
import io, re, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


def source_version():
    text = (ROOT / 'game/options.rpy').read_text(encoding='utf-8')
    return re.search(r'config\.version = "([^"]+)"', text).group(1)


def bundle_version(part=REPO / 'preview/room13-dev/game.part01'):
    with zipfile.ZipFile(io.BytesIO(Path(part).read_bytes())) as z:
        text = z.read('game/options.rpy').decode('utf-8')
    return re.search(r'config\.version = "([^"]+)"', text).group(1)


def main():
    src, pub = source_version(), bundle_version()
    note = ROOT / ('docs/releases/RELEASE_%s.md' % src)
    problems = []
    if src != pub:
        problems.append('공개 묶음 판 번호 %s, 원본 %s — 웹 빌드를 다시 한다' % (pub, src))
    if not note.exists():
        problems.append('릴리스 노트 없음: %s' % note.relative_to(REPO))
    for p in problems:
        print(p)
    if not problems:
        print('공개 확인 통과: %s' % src)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
