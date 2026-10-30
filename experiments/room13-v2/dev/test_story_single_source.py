# 대사는 story/dayNN.json 한 곳에만: rpy 에 대사 문장(Ren'Py 말하기 문장, renpy.say 의 글자)이 없어야 한다.
# 줄 번호에 기대는 파일도 없어야 한다(원본 줄을 「몇째 줄」로 가리키지 않는다).
import os
import re
import unittest

from v2data import rpy_files, DAY, GAME

SAY_STMT = re.compile(r'^\s+(?:[a-z_]\w*\s+)?"[^"]*[가-힣][^"]*"\s*(?:with\s+\w+)?\s*$')
SAY_CALL = re.compile(r'renpy\.say\([^,]*,\s*["\']')
LINE_REF = re.compile(r"\.(?:rpy|json):\d+")


class SingleSource(unittest.TestCase):
    def test_no_dialogue_in_rpy(self):
        bad = []
        for path in rpy_files(include_qa=True):
            in_label = False
            with open(path, encoding="utf-8") as f:
                for n, line in enumerate(f, 1):
                    if re.match(r"^\S", line):
                        in_label = line.startswith("label")
                    # 말하기 문장은 label 안에만 있을 수 있다.
                    if in_label and SAY_STMT.match(line):
                        bad.append("%s:%d" % (path, n))
                    if SAY_CALL.search(line):
                        bad.append("%s:%d" % (path, n))
        self.assertEqual(bad, [])

    def test_no_line_number_references_in_data(self):
        bad = []
        for rel in ("story/day01.json", "story/common.json", "data/layout.json"):
            with open(os.path.join(GAME, rel), encoding="utf-8") as f:
                if LINE_REF.search(f.read()):
                    bad.append(rel)
        self.assertEqual(bad, [])

    def test_line_ids_unique_per_block(self):
        # 같은 묶음 안에서 줄 ID 가 겹치면 시험이 진행 상태를 잘못 읽는다.
        from v2data import all_blocks, walk_steps
        for name, steps in all_blocks():
            ids = [st["id"] for st, _ in walk_steps(steps, name) if "t" in st and st.get("id")]
            # 갈래(then/else) 사이 중복은 괜찮다. 같은 목록 바로 아래만 본다.
            top = [st["id"] for st in steps if "t" in st and st.get("id")]
            self.assertEqual(len(top), len(set(top)), name)


if __name__ == "__main__":
    unittest.main()
