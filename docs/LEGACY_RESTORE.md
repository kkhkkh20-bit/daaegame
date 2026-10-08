# 기존 게임 보관과 복구

2026-10-08, main을 **다람탐정 1장 「열세 번째 침대」 테스트판**으로 바꾸면서 기존 게임을 main에서 뺐다.
기존 게임은 지우지 않았고, 아래 브랜치에 바뀌기 직전 그대로 남아 있다.

- 보관 브랜치: `archive/legacy-20261008` (커밋 `813fbc0`, v210 시점)
- 들어 있는 것
  - 루트 게임: `index.html`(세로 PWA 껍데기), `game.html`(게임 본체), `dot.html`, `wide.html`(v210 가로 시험본)
  - `chapter-one/` 「사라진 봉투」 세로형 1장과 그 검사 도구
  - 당시의 `sw.js`, `manifest.webmanifest`, `art/`, `tools/`

## 저장 데이터

새 테스트판은 `daae-inn1:` 접두사로 따로 저장하고, 기존 게임의 저장(`daae-detective-v3` 등)은 건드리지 않는다.
같은 주소에서 기존 게임을 복구하면 예전 진행 기록을 그대로 다시 읽는다.

## 복구 방법

파일 하나만 다시 꺼내 보기(예: 옛 게임 본체를 `legacy/` 폴더로):

```sh
git fetch origin archive/legacy-20261008
mkdir -p legacy
git show origin/archive/legacy-20261008:game.html > legacy/game.html
```

`chapter-one/` 폴더째 되살리기:

```sh
git checkout origin/archive/legacy-20261008 -- chapter-one
```

main 전체를 보관 시점으로 되돌리기(새 테스트판을 내리는 경우, 먼저 확인할 것):

```sh
git checkout main
git revert --no-edit <1장 테스트판 반영 커밋>..HEAD   # 또는 보관 브랜치에서 새 브랜치를 만들어 검토 후 main에 합친다
```

참고: `art/`는 새 테스트판 기준으로 갱신됐다(파일 추가 63개, 같은 경로의 그림 10개 교체).
옛 그림이 필요하면 보관 브랜치의 `art/`에서 꺼낸다. `ch1/build/base-engine.html`은 옛 `game.html`과 같은 파일이다.
