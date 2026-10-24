"""증거 서랍(2026-10-24 소유자 "추천안대로", 시안 docs/reviews/evidence-drawer-20261024/)의 자리표를 만든다.

자료마다 어느 사건(회의)에 묶일지는 "얻은 자리에서 가장 가까운 다음 회의"로 정한다. 그 자리를
손으로 81줄 적지 않으려고, 이야기 원본에서 직접 뽑는다.
  - 회의 자리: room13_v111*.rpy 의 `call r13_v111_proof('<증명>', ...)` 중 회의(R13_PROOF_MEETING)에
    속한 마지막 호출. 그 앞의 가장 가까운 `r13_v111_scene('<장면>')` 이 그 회의의 장면이다.
  - 자료 자리: records.json 의 acquire 연산(장면 = 기록 ID 앞부분)과 rpy 의 `r13_nw_acquire("K")`,
    `r13_v111_apply(..., key='K' ...)`(장면 = 앞의 r13_v111_scene, 줄 번호까지 적어 같은 장면 안 순서를 가린다).
  - 접으면 안 되는 자료: 회의 정답 세트(r13_v111_proof 의 세 번째 인자), 대화·회의에서 꺼내는 자료
    (`_return=="V111:K"`, `"V111:K" in (v111_last_presented`), 장면 묶음의 present.
    R13_PROOF_ALTERNATES/EXTRAS 는 다른 작업자가 늘리는 중이라 게임이 실행 중에 직접 읽는다.
사용: python3 dev/build_evidence_drawer.py [--write]   (--write 없이 돌리면 바뀐 것이 있는지만 알린다)
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.join(ROOT, "game")
OUT = os.path.join(GAME, "v111", "evidence-drawer.json")


def proof_meetings():
    rules = open(os.path.join(GAME, "room13_v111_newworld_rules.rpy"), encoding="utf-8").read()
    block = re.search(r"R13_PROOF_MEETING=\{(.*?)\}", rules, re.S).group(1)
    return dict(re.findall(r'"([^"]+)":"([^"]+)"', block))


def build():
    records = json.load(open(os.path.join(GAME, "v111", "records.json"), encoding="utf-8"))
    order = list(records["scene_days"])
    meeting_of = proof_meetings()
    meetings = {}
    sites = {}
    fixed = set()

    def site(key, scene, fname, line):
        entry = [scene, fname, line]
        if entry not in sites.setdefault(key, []):
            sites[key].append(entry)

    # 이야기 기록(records.json)의 acquire: 장면은 기록 ID 앞부분. 같은 장면 안에서는 회의보다 앞으로 친다.
    scene_ids = sorted(order, key=len, reverse=True)
    for coll in ("records", "options"):
        for rid, rec in records[coll].items():
            for op in rec.get("operations", []):
                if op.get("op") != "acquire":
                    continue
                scene = next((s for s in scene_ids if rid.startswith(s + "_")), None)
                if scene:
                    site(op["key"], scene, "", -1)

    for path in sorted(glob.glob(os.path.join(GAME, "room13_v111*.rpy"))):
        fname = os.path.basename(path)
        scene = None
        for no, line in enumerate(open(path, encoding="utf-8"), 1):
            m = re.search(r"r13_v111_scene\(['\"]([^'\"]+)['\"]\)", line)
            if m and m.group(1) in records["scene_days"]:
                scene = m.group(1)
            m = re.search(r"call r13_v111_proof\(\s*['\"]([^'\"]+)['\"]\s*,\s*\[([^\]]*)\]", line)
            if m:
                fixed.update(re.findall(r"['\"](\w+)['\"]", m.group(2)))
                meeting = meeting_of.get(m.group(1))
                if meeting and scene:
                    old = meetings.get(meeting)
                    here = [scene, fname, no]
                    if old is None or (order.index(scene), no) > (order.index(old[0]), old[2]):
                        meetings[meeting] = here
            for m in re.finditer(r"r13_nw_acquire\(\s*['\"](\w+)['\"]|op=\"acquire\",key='(\w+)'", line):
                if scene:
                    site(m.group(1) or m.group(2), scene, fname, no)
            fixed.update(re.findall(r'_return==["\']V111:(\w+)["\']', line))
            fixed.update(re.findall(r'["\']V111:(\w+)["\'] in \(v111_last_presented', line))

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k == "present" and isinstance(v, str):
                    fixed.add(v[5:] if v.startswith("V111:") else v)
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(json.load(open(os.path.join(GAME, "v111", "field-bindings.json"), encoding="utf-8")))

    def pos(entry):
        return (order.index(entry[0]), entry[2])
    ordered = sorted(meetings, key=lambda k: pos(meetings[k]))
    return dict(
        note="dev/build_evidence_drawer.py 가 만든다. 손으로 고치지 않는다.",
        meetings=[dict(key=k, scene=meetings[k][0], file=meetings[k][1], line=meetings[k][2],
                       day=records["scene_days"][meetings[k][0]]) for k in ordered],
        sites={k: sorted(v, key=pos) for k, v in sorted(sites.items())},
        fixed=sorted(fixed),
    )


def main():
    data = build()
    text = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
    current = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
    if "--write" in sys.argv:
        if text != current:
            open(OUT, "w", encoding="utf-8").write(text)
        print("자리표를 썼다:", os.path.relpath(OUT, ROOT))
        return 0
    if text != current:
        print("자리표가 이야기 원본과 다르다. python3 dev/build_evidence_drawer.py --write")
        return 1
    print("자리표가 최신이다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
