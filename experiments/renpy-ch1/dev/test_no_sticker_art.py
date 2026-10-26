"""2026-10-26 소유자: 인물 그림은 흰 테두리 스티커 없이 간다.
스티커 묶음은 파일·연결표를 남긴 채 화면에서만 끈다. 테두리 없는 판으로 바꾼 뒤에 켠다."""
import json, unittest
from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np
GAME = Path(__file__).resolve().parents[1] / 'game'
OFF = {
    'systems/room13_dialogue_beats.rpy': 'R13_DIALOGUE_B_ART_ON',       # B 대사 표정 50장(스티커)
    'room13_bdialogue_faces.rpy': 'R13_BDIALOGUE_FACES_ON',             # 얼굴 스티커 50장(쓰지 않음)
}


def white_edge(path):
    # 외곽 2픽셀 띠에서 흰색(RGB 모두 225 초과)이 차지하는 비율. 스티커 테두리는 0.4~1.0 이 나온다.
    a = np.array(Image.open(path).convert('RGBA')).astype(int)
    m = a[:, :, 3] >= 128
    inner = np.array(Image.fromarray((m * 255).astype('uint8')).filter(ImageFilter.MinFilter(5))) > 0
    c = a[m & ~inner][:, :3]
    return float((c.min(1) > 225).mean()) if len(c) else 0.0


class NoStickerArt(unittest.TestCase):
    def test_sticker_sets_are_off(self):
        for path, name in OFF.items():
            self.assertRegex((GAME / path).read_text(), r'\n\s+%s = False\n' % name, path)

    def test_resident_poses_use_noborder_art(self):
        # 생활 동작 A안은 흰 외곽을 걷어 낸 판으로 바꾸고 다시 켰다.
        self.assertRegex((GAME / 'systems/room13_resident_poses_a.rpy').read_text(), r'\n\s+R13_RESIDENT_POSES_A_ON = True\n')
        table = json.loads((GAME / 'assets/room13-resident-poses-a.json').read_text(encoding='utf-8'))
        files = {s['fields']['file'] for s in table['slots']}
        self.assertEqual(len(files), 46)
        for f in sorted(files):
            self.assertTrue(f.endswith('-noborder.webp'), f)
            self.assertLess(white_edge(GAME / f), 0.02, f)

    def test_sticker_files_kept_for_later(self):
        # 끄거나 바꾸기만 하고 지우지 않는다.
        for folder in ('resident-poses-a', 'dialogue-b-primary50', 'dialogue-b-faces'):
            self.assertTrue(any((GAME / 'assets' / folder).iterdir()), folder)


if __name__ == '__main__':
    unittest.main()
