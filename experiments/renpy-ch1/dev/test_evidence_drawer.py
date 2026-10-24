"""증거 서랍(2026-10-24, docs/reviews/evidence-drawer-20261024/적용보고.md) 자리표와 쪽지 규칙 검사.

- 자리표(game/v111/evidence-drawer.json)는 이야기 원본에서 다시 뽑은 것과 같아야 한다.
- 모든 자료(records.json evidence + 새 세계 자료)는 사건 자리를 하나 이상 가진다.
- 쪽지로 접는 자료는 회의 정답 세트, 대체 세트·덧붙임, 대화·회의에서 꺼내는 자료가 아니어야 한다
  (게임은 실행 중에도 대체 세트·덧붙임을 다시 보고 겹치면 접지 않는다. 여기서는 겹침을 미리 알린다).
"""
import json, os, re, subprocess, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "dev"))
import build_evidence_drawer as drawer  # noqa: E402


def drawer_source():
    return open(os.path.join(ROOT, "game", "systems", "room13_evidence_drawer.rpy"), encoding="utf-8").read()


def note_pairs():
    block = re.search(r"R13_DRAWER_NOTES=\((.*?)\)\n", drawer_source(), re.S).group(1)
    return re.findall(r'\("(\w+)","(\w+)"\)', block)


class EvidenceDrawer(unittest.TestCase):
    def test_table_is_current(self):
        r = subprocess.run([sys.executable, os.path.join(ROOT, "dev", "build_evidence_drawer.py")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_every_record_has_a_case(self):
        data = drawer.build()
        records = json.load(open(os.path.join(ROOT, "game", "v111", "records.json"), encoding="utf-8"))
        missing = [k for k in records["evidence"] if k not in data["sites"]]
        self.assertEqual(missing, [])
        self.assertEqual([m["key"] for m in data["meetings"]],
                         ["gate", "lamp", "gate_post", "fire", "room13", "records", "hypothesis", "soup", "blanket", "piko", "altar"])

    def test_case_names_cover_meetings(self):
        names = re.search(r"R13_DRAWER_NAMES=dict\((.*?)\)\n", drawer_source(), re.S).group(1)
        named = set(re.findall(r"(\w+)=", names))
        self.assertEqual(named, set(m["key"] for m in drawer.build()["meetings"]))

    def test_notes_are_not_presented(self):
        fixed = set(drawer.build()["fixed"])
        rules = open(os.path.join(ROOT, "game", "room13_v111_newworld_rules.rpy"), encoding="utf-8").read()
        sets = re.search(r"R13_PROOF_EXTRAS=\{(.*?)\n    \}", rules, re.S).group(1) + re.search(r"R13_PROOF_ALTERNATES=\{(.*?)\n    \}", rules, re.S).group(1)
        used = fixed | set(re.findall(r'"(\w+)"', sets))
        pairs = note_pairs()
        self.assertTrue(pairs)
        clash = [note for note, base in pairs if note in used]
        self.assertEqual(clash, [], "쪽지로 접으면 제시할 수 없게 되는 자료: %s" % clash)
        for presented in ("E13_HANDOVER", "E14_SUPPLY", "E13_ORDER"):
            self.assertIn(presented, fixed)


if __name__ == "__main__":
    unittest.main()
