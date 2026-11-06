"""게임 내용은 동일한 채 전송 부분을 나누어도 버전 검사로 전체 묶음을 확인한다."""
import io
import tempfile
import unittest
import zipfile
from pathlib import Path

from check_release import bundle_version


class ReleaseParts(unittest.TestCase):
    def archive(self):
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w') as z:
            z.writestr('game/options.rpy', 'define config.version = "0.20.107"\n')
        return data.getvalue()

    def test_single_part(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'game.part01'
            path.write_bytes(self.archive())
            self.assertEqual(bundle_version(path), '0.20.107')

    def test_zip_header_and_directory_can_be_in_different_parts(self):
        with tempfile.TemporaryDirectory() as root:
            data = self.archive()
            path = Path(root) / 'game.part01'
            path.write_bytes(data[:17])
            (Path(root) / 'game.part02').write_bytes(data[17:])
            self.assertEqual(bundle_version(path), '0.20.107')

    def test_missing_last_part_is_not_a_valid_release(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'game.part01'
            path.write_bytes(self.archive()[:17])
            with self.assertRaises(zipfile.BadZipFile):
                bundle_version(path)


if __name__ == '__main__':
    unittest.main()
