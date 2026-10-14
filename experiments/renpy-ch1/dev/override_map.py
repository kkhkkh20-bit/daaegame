"""Map every r13_* function that is redefined across script files.

    python dev/override_map.py            # print the map
    python dev/override_map.py --write    # refresh docs/OVERRIDE_MAP.md

Many systems extend a base function by capturing it and redefining it:

    _r13_items_topics=r13_topics          # keep the previous layer
    def r13_topics(person): ...           # new outer layer calls the old one

Ren'Py runs init blocks by priority, then by file path, then by line, so the
last definition in that order is what the game calls. This tool lists each
chain in that order, marks a definition as DEAD when a later one replaces it
without capturing it, and flags layers that share an init priority (their
order then depends only on file names).
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
INIT = re.compile(r"^init(?:\s+(-?\d+))?\s+python\b|^init(?:\s+(-?\d+))?\s*:|^python early\b")
DEF = re.compile(r"^(\s+)def\s+(r13_\w+)\s*\(")
CAPTURE = re.compile(r"^\s+(\w+)\s*=\s*(r13_\w+)\s*$")


def scan():
    events = []  # (priority, path, line, kind, name, extra)
    for path in sorted(GAME.rglob("*.rpy")):
        rel = path.relative_to(GAME).as_posix()
        if rel.startswith("qa_tests/"):
            continue
        priority = None
        for n, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            if line and not line[0].isspace():
                m = INIT.match(line)
                priority = (int(m.group(1) or m.group(2) or 0) if m else None)
                continue
            if priority is None:
                continue
            d = DEF.match(line)
            if d and len(d.group(1)) == 4:
                events.append((priority, rel[:-4], n, "def", d.group(2), None))
                continue
            c = CAPTURE.match(line)
            if c and len(line) - len(line.lstrip()) == 4:
                events.append((priority, rel[:-4], n, "capture", c.group(2), c.group(1)))
    events.sort(key=lambda e: (e[0], e[1], e[2]))
    return events


def chains(events):
    out = {}
    for prio, rel, line, kind, name, alias in events:
        out.setdefault(name, []).append((prio, rel, line, kind, alias))
    result = {}
    for name, rows in out.items():
        defs = [r for r in rows if r[3] == "def"]
        if len(defs) < 2:
            continue
        layers, pending_capture = [], False
        for r in rows:
            if r[3] == "capture":
                pending_capture = True
                if layers:
                    layers[-1]["captured_as"] = r[4]
                continue
            if layers and not layers[-1].get("captured_as"):
                layers[-1]["dead"] = True
            layers.append(dict(prio=r[0], file=r[1] + ".rpy", line=r[2]))
        result[name] = layers
    return result


def render(result):
    lines = ["# 함수 덮어쓰기 지도 (자동 생성: dev/override_map.py --write)", "",
             "Ren'Py는 init 우선순위 → 파일 경로 → 줄 순서로 실행한다. 아래 표는 그 순서대로이며, 마지막 줄이 게임이 실제로 부르는 바깥 층이다.",
             "각 층은 바로 위 층을 `captured_as` 이름으로 붙잡아 부른다. 새 기능을 넣을 때 이 순서를 확인하고, 같은 우선순위에 층을 추가하지 않는다.", ""]
    warn = []
    for name in sorted(result, key=lambda n: (-len(result[n]), n)):
        layers = result[name]
        lines += ["## `%s` (%d층)" % (name, len(layers)), "", "| 순서 | init | 위치 | 이전 층 이름 |", "|---|---|---|---|"]
        for i, layer in enumerate(layers, 1):
            mark = " **DEAD**" if layer.get("dead") else ""
            lines.append("| %d | %d | `%s:%d`%s | %s |" % (i, layer["prio"], layer["file"], layer["line"], mark, layer.get("captured_as", "")))
        prios = [l["prio"] for l in layers if not l.get("dead")]
        dup = sorted({p for p in prios if prios.count(p) > 1})
        if dup:
            warn.append("`%s`: init %s에 층이 둘 이상" % (name, ", ".join(map(str, dup))))
        lines.append("")
    if warn:
        lines[5:5] = ["주의(같은 우선순위 → 파일 이름이 순서를 결정):", ""] + ["- " + w for w in warn] + [""]
    return "\n".join(lines) + "\n"


def main():
    result = chains(scan())
    text = render(result)
    if "--write" in sys.argv:
        (ROOT / "docs/OVERRIDE_MAP.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
