# 닿지 않는 갈래는 옮기지 않았다(추출 day01.json 이 「닿지 않는다」고 한 것). 다시 들어오면 알린다.
import json
import os
import unittest

from v2data import GAME

DEAD_KEYS = ["gate_lodging_retired", "gate_daram_unlisted", "gate_last_try", "gate_both_given",
             "room13_checked_d1", "compare_warning5", "letter_close_selected"]
DEAD_IDS = ["NW_D01_S03_R03", "NW_AR_D01_01", "NW_AR_D01_02", "NW_AR_D01_03", "NW_D01_S04_A08",
            "MS14_D01_S03_L0013", "NW_DLG_D01_01", "NW_CMP_RETRY_05",
            "MS14_D01_S01_L0014", "MS14_D01_S02_L0026", "MS14_D01_S02_L0027",
            "MS14_D01_S03_L0008", "MS14_D01_S03_L0018", "MS14_D01_S03_L0026"]


class DeadBranches(unittest.TestCase):
    def test_dead_branches_absent(self):
        with open(os.path.join(GAME, "story/day01.json"), encoding="utf-8") as f:
            text = f.read()
        for k in DEAD_KEYS + DEAD_IDS:
            self.assertNotIn('"%s"' % k, text, k)
            self.assertNotIn("'%s'" % k, text, k)


if __name__ == "__main__":
    unittest.main()
