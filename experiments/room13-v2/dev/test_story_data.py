# 이야기 데이터 무결성: 이동 대상·자료 ID·조건 이름·회의 정답·그림 파일.
import ast
import os
import unittest

from v2data import DAY, COMMON, LAYOUT, GAME, OPS, SPEAKERS, all_blocks, all_steps, walk_steps, conditions

EVIDENCE = set(COMMON["evidence"])
COND_FUNCS = {"has", "v", "chose", "chose_only"}
COND_NAMES = COND_FUNCS | {"won", "True", "False"}


def block_succ(steps, seen=None):
    """이 묶음에서 갈 수 있는 노드: goto, 그리고 대기의 선택지·증명의 결과 묶음 안의 goto 까지."""
    seen = set() if seen is None else seen
    out = set()
    for st, _ in walk_steps(steps, "x"):
        if "goto" in st:
            out.add(st["goto"])
        if "wait" in st and ("g", st["wait"]) not in seen:
            seen.add(("g", st["wait"]))
            for o in DAY["gates"][st["wait"]]["options"]:
                out |= block_succ(o["do"], seen)
        if "proof" in st and ("p", st["proof"]) not in seen:
            seen.add(("p", st["proof"]))
            for name, blk in all_blocks():
                if name.startswith("p:%s/" % st["proof"]):
                    out |= block_succ(blk, seen)
    return out


def block_gets(steps, seen=None):
    """이 묶음에서(대기 선택지·물건 읽기 포함) 얻을 수 있는 자료. 증명 결과 안은 보지 않는다."""
    seen = set() if seen is None else seen
    out = set()
    for st, _ in walk_steps(steps, "x"):
        if "get" in st:
            out.add(st["get"])
        if "wait" in st and st["wait"] not in seen:
            seen.add(st["wait"])
            gate = DAY["gates"][st["wait"]]
            for o in gate["options"]:
                out |= block_gets(o["do"], seen)
            for spec in DAY["objects"].get(gate["place"], {}).values():
                if "read" in spec:
                    out |= block_gets(spec["read"]["do"], seen)
    return out


def proof_entry(pid):
    """그 증명을 여는 노드(노드 안에 있거나, 노드의 대기 선택지 안에 있다)."""
    for node, steps in DAY["nodes"].items():
        for st, _ in walk_steps(steps, node):
            if st.get("proof") == pid:
                return node
            if "wait" in st:
                for o in DAY["gates"][st["wait"]]["options"]:
                    if any(x.get("proof") == pid for x, _ in walk_steps(o["do"], "o")):
                        return node
    return None


class StoryData(unittest.TestCase):
    def test_every_step_has_one_known_op(self):
        for st, where in all_steps():
            if "t" in st:
                self.assertIn(st.get("who"), SPEAKERS, where)
                self.assertIsInstance(st["t"], str, where)
                continue
            keys = set(st) & OPS
            self.assertEqual(len(keys), 1, "%s: %r" % (where, st))
            self.assertTrue(set(st) <= OPS | {"then", "else"}, "%s: %r" % (where, st))

    def test_goto_wait_proof_targets_exist(self):
        for st, where in all_steps():
            if "goto" in st:
                self.assertIn(st["goto"], DAY["nodes"], where)
            if "wait" in st:
                self.assertIn(st["wait"], DAY["gates"], where)
            if "proof" in st:
                self.assertIn(st["proof"], DAY["proofs"], where)
            if "scene" in st:
                self.assertIn(st["scene"], DAY["scenes"], where)
            if "place" in st or "move" in st:
                place = st.get("place") or st.get("move")
                self.assertTrue(place == "black" or place in LAYOUT["places"], where)
        self.assertIn(DAY["start"], DAY["nodes"])

    def test_every_node_reachable_from_start(self):
        seen, todo = set(), [DAY["start"]]
        while todo:
            n = todo.pop()
            if n in seen:
                continue
            seen.add(n)
            todo.extend(block_succ(DAY["nodes"][n]) - seen)
        self.assertEqual(set(DAY["nodes"]) - seen, set(), "닿지 않는 노드")

    def test_evidence_ids_defined(self):
        used = set()
        for st, where in all_steps():
            if "get" in st:
                used.add(st["get"])
        for p in DAY["proofs"].values():
            for c in p["correct"]:
                used |= set(c)
            used |= set(p.get("extras", []))
            used |= set((p.get("observe") or {}).get("pair", []))
        for g in DAY["gates"].values():
            for o in g["options"]:
                if o.get("present"):
                    used.add(o["present"])
        for r in DAY["reactions"]:
            used.add(r["ev"])
        for f in DAY["followups"]:
            used.add(f["after"])
        for objs in DAY["objects"].values():
            for spec in objs.values():
                if "ev" in spec:
                    used.add(spec["ev"])
        for cond, where in conditions():
            for node in ast.walk(ast.parse(cond, mode="eval")):
                if isinstance(node, ast.Call) and node.func.id in ("has", "chose", "chose_only"):
                    for a in node.args:
                        used.add(a.value)
        self.assertEqual(used - EVIDENCE, set(), "정의되지 않은 자료")

    def test_conditions_use_only_known_names(self):
        set_keys = set()
        for st, _ in all_steps():
            for k in ("set", "add"):
                if k in st:
                    set_keys |= set(st[k])
        for cond, where in conditions():
            tree = ast.parse(cond, mode="eval")
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    self.assertIn(node.id, COND_NAMES, "%s: %s" % (where, cond))
                if isinstance(node, ast.Call):
                    self.assertIn(node.func.id, COND_FUNCS, where)
                    self.assertTrue(all(isinstance(a, ast.Constant) and isinstance(a.value, str) for a in node.args), where)
                    if node.func.id == "v":
                        key = node.args[0].value
                        # 엔진이 쓰는 값(tries:·_wrong_pending)이 아니면 데이터 어딘가에서 쓰는 값이어야 한다.
                        self.assertTrue(key in set_keys or key.startswith("tries:") or key.endswith("_wrong_pending"),
                                        "%s: 아무도 쓰지 않는 값 %s" % (where, key))

    def test_proof_answers_obtainable_before_proof(self):
        # 회의 정답 자료는 그 회의를 열기 전에 얻을 수 있어야 한다(기본 증거만으로 언제나 이길 수 있다).
        # 시작에서 회의 노드까지 회의 결과 묶음을 거치지 않고 닿는 노드들의 자료를 모은다.
        for pid, proof in DAY["proofs"].items():
            entry = proof_entry(pid)
            self.assertIsNotNone(entry, pid)
            seen, todo, gets = set(), [DAY["start"]], set()
            while todo:
                n = todo.pop()
                if n in seen:
                    continue
                seen.add(n)
                gets |= block_gets(DAY["nodes"][n])
                if n == entry:
                    continue
                nxt = block_succ(DAY["nodes"][n], {("p", pid)})
                todo.extend(nxt - seen)
            for c in proof["correct"]:
                self.assertTrue(set(c) <= gets, "%s 정답 %s 를 그 전에 얻을 수 없다(얻는 것 %s)" % (pid, c, sorted(gets)))

    def test_choice_titles_short(self):
        # 고르기 문구 24자 이하(소유자 0.18.4, 지금 판 test_choice_length 와 같은 범위: 메뉴만).
        for st, where in all_steps():
            if "menu" in st:
                for item in st["menu"]:
                    self.assertLessEqual(len(item["t"]), 24, where)

    def test_gate_places_people_objects_exist(self):
        for g, gate in DAY["gates"].items():
            place = LAYOUT["places"][gate["place"]]
            for p in gate["people"]:
                self.assertIn(p, place["people"], g)
                self.assertTrue(os.path.exists(os.path.join(GAME, "assets/field-dot-v2/%s/neutral.webp" % p)), p)
            for o in gate["options"]:
                for obj in o.get("obj", []):
                    self.assertIn(obj, place["objects"], "%s: %s" % (g, obj))
                if o.get("move"):
                    self.assertIn(o["move"], LAYOUT["places"], g)
            if gate.get("travel"):
                self.assertTrue(any(o.get("move") == gate["travel"] for o in gate["options"]), g)
        for place, objs in DAY["objects"].items():
            for key in objs:
                self.assertIn(key, LAYOUT["places"][place]["objects"], "%s/%s" % (place, key))

    def test_asset_files_exist(self):
        need = set()
        for s in DAY["scenes"].values():
            need.add("assets/%s.mp3" % s["music"])
            need.add("assets/amb-%s.mp3" % s["ambience"])
        for p in LAYOUT["places"].values():
            need |= {"assets/" + a for a in p["art"].values()}
        for e in COMMON["evidence"].values():
            need.add("assets/" + e["art"])
        face = {"surprise": "surprise_talk", "thinking": "neutral"}
        seat = {"neutral": "neutral", "joy": "joy", "angry": "pout", "anxious": "wistful", "flustered": "secret", "surprise": "quiz"}
        for st, where in all_steps():
            if "t" not in st:
                continue
            who = st["who"]
            if st.get("cut"):
                need.add("assets/evidence/%s.webp" % st["cut"])
            if who in ("daram", "guard", "karo", "granny", "neoul"):
                e = st.get("e", "neutral")
                need.add("assets/dialogue-dot-v2/%s/760/%s.webp" % (who, face.get(e, e)))
            if st.get("pose", "").startswith("seat_"):
                need.add("assets/room13-carriage-daram-seat-%s.webp" % st["pose"][5:])
        for f in sorted(need):
            self.assertTrue(os.path.exists(os.path.join(GAME, f)), f)


if __name__ == "__main__":
    unittest.main()
