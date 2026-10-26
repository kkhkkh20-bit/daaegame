"""2026-10-26 소유자: 인물 그림은 흰 테두리 스티커 없이 간다.
스티커 묶음 셋은 파일·연결표를 남긴 채 화면에서만 끈다. 테두리 없는 판으로 바꾼 뒤에 켠다."""
import re, unittest
from pathlib import Path
GAME = Path(__file__).resolve().parents[1] / 'game'
SWITCHES = {
    'systems/room13_resident_poses_a.rpy': 'R13_RESIDENT_POSES_A_ON',   # 주민 생활 동작 A안 46장
    'systems/room13_dialogue_beats.rpy': 'R13_DIALOGUE_B_ART_ON',       # B 대사 표정 50장
    'room13_bdialogue_faces.rpy': 'R13_BDIALOGUE_FACES_ON',             # 얼굴 스티커 50장
}

class NoStickerArt(unittest.TestCase):
    def test_sticker_sets_are_off(self):
        for path, name in SWITCHES.items():
            text = (GAME / path).read_text()
            self.assertRegex(text, r'\n\s+%s = False\n' % name, path)

    def test_sticker_files_kept_for_later(self):
        # 끄기만 하고 지우지 않는다. 새 판을 받으면 같은 자리를 바꿔 켠다.
        for folder in ('resident-poses-a', 'dialogue-b-primary50', 'dialogue-b-faces'):
            self.assertTrue(any((GAME / 'assets' / folder).iterdir()), folder)

if __name__ == '__main__':
    unittest.main()
