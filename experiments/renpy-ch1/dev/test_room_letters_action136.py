"""첫 방에서 관찰 전·발견 뒤·구 완료 저장의 다음 조작을 구분한다."""
from pathlib import Path
import unittest
from PIL import ImageFont
from test_proof_workspace import load_pure

ROOT=Path(__file__).resolve().parents[1]
KEY="두 편지를 나란히 본다"
PAIR=("V111:E01","V111:E06")

class RoomLettersAction136(unittest.TestCase):
    def setUp(self):
        self.copy=load_pure()["r13_pw_room_letters_copy"]

    def test_before_observation_invites_inspection_without_revealing_the_difference(self):
        label,guide=self.copy(KEY,PAIR,True,False)
        self.assertEqual(label,"차이 살펴보기")
        self.assertIn("직접 짚어",guide)
        self.assertIn("기회는 줄어들지 않습니다",guide)
        for secret in ("도토리","서명","끝부분","위조","엄마가 쓴"):
            self.assertNotIn(secret,label+guide)

    def test_found_difference_explicitly_resumes_the_conversation(self):
        label,guide=self.copy(KEY,PAIR,False,True)
        self.assertEqual(label,"발견한 차이 확인")
        self.assertIn(label,guide)
        self.assertIn("다람과 이야기를 이어",guide)
        self.assertNotIn("직접 짚어",guide)
        self.assertEqual(self.copy(KEY,tuple(reversed(PAIR)),False,True),(label,guide))

    def test_completed_old_save_has_no_new_inspection_instruction(self):
        label,guide=self.copy(KEY,PAIR,False,False)
        self.assertEqual(label,"비교 내용 확인")
        self.assertIn("이야기를 이어",guide)
        self.assertNotIn("짚어",guide)
        self.assertEqual(self.copy("v111:"+KEY,PAIR,False,False),(label,guide))

    def test_other_hearings_and_wrong_or_incomplete_pairs_keep_their_existing_copy(self):
        for key,pair in [("함께 들어갈 근거를 고른다",PAIR),("두 편지의 초대를 대조한다",PAIR),
                         (KEY,None),(KEY,()),(KEY,("V111:E01",)),(KEY,("V111:E01",None)),
                         (KEY,("V111:E01","V111:E01")),(KEY,("V111:E01","V111:E03"))]:
            self.assertIsNone(self.copy(key,pair,True,False),(key,pair))

    def test_one_line_guide_fits_the_existing_notebook_body(self):
        for size in (22,24,26,28):
            font=ImageFont.truetype(str(ROOT/"game/assets/Pretendard-Bold.otf"),size)
            for needed,observed in ((True,False),(False,True),(False,False)):
                label,guide=self.copy(KEY,PAIR,needed,observed)
                self.assertLessEqual(font.getlength(guide),1074,(size,guide))
                self.assertLessEqual(font.getlength(label),208,(size,label))

if __name__=="__main__":unittest.main()
