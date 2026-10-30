# 단위 시험이 함께 쓰는 읽기 도구(게임에는 들어가지 않는다).
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.join(ROOT, "game")


def load(rel):
    with open(os.path.join(GAME, rel), encoding="utf-8") as f:
        return json.load(f)


DAY = load("story/day01.json")
COMMON = load("story/common.json")
LAYOUT = load("data/layout.json")

OPS = {"place", "move", "scene", "music", "loop", "loop_stop", "get", "set", "add", "if", "goto", "wait",
       "menu", "proof", "time", "period", "mark_read", "meeting", "retry", "end_day", "run_option"}
SPEAKERS = set(COMMON["people"]) | {"narr", "doc", "card"}


def rpy_files(include_qa=False):
    out = []
    for base, dirs, files in os.walk(GAME):
        if not include_qa and os.path.relpath(base, GAME).split(os.sep)[0] == "qa":
            continue
        for f in files:
            if f.endswith(".rpy"):
                out.append(os.path.join(base, f))
    return sorted(out)


def walk_steps(steps, where):
    """모든 단계를 (단계, 위치) 로 펼친다(if 의 then/else, menu 의 do 포함)."""
    for i, st in enumerate(steps):
        here = "%s/%d" % (where, i)
        yield st, here
        if "if" in st:
            for key in ("then", "else"):
                for x in walk_steps(st.get(key, []), here + "/" + key):
                    yield x
        if "menu" in st:
            for j, item in enumerate(st["menu"]):
                for x in walk_steps(item.get("do", []), here + "/m%d" % j):
                    yield x


def all_blocks():
    """(이름, 단계 목록) — 엔진이 등록하는 것과 같은 묶음들."""
    for k, steps in DAY["nodes"].items():
        yield "n:" + k, steps
    for g, gate in DAY["gates"].items():
        for i, o in enumerate(gate["options"]):
            yield "g:%s/%d" % (g, i), o["do"]
    for p, proof in DAY["proofs"].items():
        for i, o in enumerate(proof["outcomes"]):
            yield "p:%s/o%d" % (p, i), o["do"]
        for key in ("press", "investigate"):
            if key in proof:
                yield "p:%s/%s" % (p, key), proof[key]
        for s in (proof.get("observe") or {}).get("spots", []):
            yield "p:%s/spot:%s" % (p, s["id"]), s["do"]
    for place, objs in DAY["objects"].items():
        for o, spec in objs.items():
            if "read" in spec:
                yield "o:%s/%s" % (place, o), spec["read"]["do"]
            if "chat" in spec:
                yield "o:%s/%s/chat" % (place, o), spec["chat"]
    for f in DAY["followups"]:
        yield "f:" + f["id"], f["do"]
    for r in DAY["reactions"]:
        yield "r:%s:%s" % (r["person"], r["ev"]), r["lines"]
    for p, spec in COMMON["people"].items():
        for key in ("first", "daily"):
            if key in spec:
                yield "c:%s/%s" % (p, key), spec[key]


def all_steps():
    for name, steps in all_blocks():
        for st, where in walk_steps(steps, name):
            yield st, where


def conditions():
    """데이터에 적힌 모든 조건 문자열과 위치."""
    for st, where in all_steps():
        if "if" in st:
            yield st["if"], where
    for g, gate in DAY["gates"].items():
        for i, o in enumerate(gate["options"]):
            if "when" in o:
                yield o["when"], "g:%s/%d" % (g, i)
    for p, proof in DAY["proofs"].items():
        for i, o in enumerate(proof["outcomes"]):
            yield o["when"], "p:%s/o%d" % (p, i)
    for place, objs in DAY["objects"].items():
        for o, spec in objs.items():
            if "read" in spec:
                yield spec["read"]["when"], "o:%s/%s" % (place, o)
