"""다람탐정 1장 테스트판 빌드.

기본 엔진(base-engine.html = 옛 game.html, 보관 브랜치와 같은 파일)에 1장 모듈을 끼워 넣어
저장소 루트의 index.html을 만든다.

  python ch1/build/build.py            -> index.html
  python ch1/build/build.py --test OUT -> 검사용 빌드(window.__T 훅 포함, 공개 경로에 두지 말 것)
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "ch1", "src")


def read(*p):
    with open(os.path.join(*p), encoding="utf-8") as f:
        return f.read()


def build():
    s = read(ROOT, "ch1", "build", "base-engine.html")
    early = read(SRC, "inn_early.js")
    late = read(SRC, "wide209_J.js")
    ep = read(SRC, "ep1_inn_script.js") + "\n" + read(SRC, "ep1_inn.js")
    rti = read(SRC, "rtg_inn.js") + "\n" + read(SRC, "worldmap.js")
    V = '<meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">'
    assert s.count(V) == 1
    s = s.replace(V, V + "<script>" + early + "</script>", 1)
    s = s.replace("<title>다람 탐정 사무소</title>", "<title>다람탐정 · 1장 열세 번째 침대 (테스트판)</title>", 1)
    A = 'if(MISS.length)try{console.warn("ui207 miss",MISS)}catch(e){}\n})();'
    assert s.count(A) == 1
    s = s.replace(A, A + "\n" + ep + "\n" + late + "\n" + rti, 1)
    return s


def main():
    s = build()
    if len(sys.argv) > 2 and sys.argv[1] == "--test":
        M = "CASES.forEach(function(c){var cf=CONFESS[c.id];c.contra.forEach(function(x){if(cf&&x.unlock===cf)x.unlock=null})});\n"
        assert s.count(M) == 1
        out = sys.argv[2]
        with open(out, "w", encoding="utf-8") as f:
            f.write(s.replace(M, M + "window.__T=function(code){return eval(code)};\n"))
        print("test build", out, len(s))
        return
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(s)
    print("index.html", len(s))


if __name__ == "__main__":
    main()
