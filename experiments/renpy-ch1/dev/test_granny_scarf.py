"""Scarf delivery geometry, runtime coverage, and reversible installation."""
import json
import tempfile
import unittest
from pathlib import Path
from shutil import copytree

import numpy as np
from PIL import Image
from apply_granny_scarf import ART, ROOT, digest, run

MANIFEST = json.loads((ART / 'manifest.json').read_text()) if (ART / 'manifest.json').exists() else {}


def approved_path(path):
    """Expected pixels after the explicitly approved costume-only replacement."""
    relative = Path(path).relative_to(ROOT).as_posix()
    row = next(row for row in MANIFEST['files'] if row['path'] == relative)
    return ART / 'edited' / row['path']


class GrannyScarf(unittest.TestCase):
    def test_installed_files_and_originals(self):
        self.assertEqual(run(check=True), len(MANIFEST['files']))
        for row in MANIFEST['files']:
            self.assertTrue((ROOT / row['path']).is_file(), row['path'])
            if row['before_sha256']:
                self.assertTrue((ART / 'originals' / row['path']).is_file())

    def test_canvas_alpha_feet_and_unchanged_pixels(self):
        for row in MANIFEST['files']:
            if row['kind'] != 'image':
                continue
            with self.subTest(path=row['path']):
                current = Image.open(ROOT / row['path']).convert('RGBA')
                template = ART / 'originals' / row.get('geometry_template', row['path'])
                original = Image.open(template).convert('RGBA')
                self.assertEqual(current.size, original.size)
                a = np.asarray(current); b = np.asarray(original)
                old_box = original.getchannel('A').getbbox(); new_box = current.getchannel('A').getbbox()
                self.assertLessEqual(abs(old_box[3] - new_box[3]), 2)
                if row['before_sha256']:
                    self.assertEqual(new_box, old_box)
                    self.assertTrue(np.array_equal(a[:, :, 3], b[:, :, 3]))
                    x1,y1,x2,y2=row['edit_rectangle']
                    changed=np.any(a!=b,axis=2);changed[y1:y2,x1:x2]=False
                    self.assertFalse(changed.any(), 'Pixels outside scarf edit changed')
                self.assertEqual(current.getpixel((0, 0))[3], 0)

    def test_inventory_covers_runtime_registries(self):
        paths={row['path'] for row in MANIFEST['files']}
        for relative in MANIFEST['runtime_registries']:
            data=json.loads((ROOT / relative).read_text())
            def walk(value):
                if isinstance(value,dict):
                    for key,child in value.items():
                        # 2026-10-26 전신 묶음(dialogue-source-master-v2)은 처음부터 승인 목도리(버건디·은핀·찢어짐 없음)로
                        # 그려 온 새 그림이라 이 일괄 수정 목록 밖이다. 육안 확인: docs/art-requests/납품검수_20261026.md
                        if key=='file' and 'granny' in child and not child.startswith(('assets/dialogue-source-master-v2/','assets/dialogue-dot-v2/')):
                            self.assertIn('game/'+child,paths)
                        else:walk(child)
                elif isinstance(value,list):
                    for child in value:walk(child)
            walk(data)

    def test_apply_revert_idempotence_and_unrelated_edit_guard(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);copytree(ART/'originals',root,dirs_exist_ok=True)
            run(root=root);run(root=root);run(check=True,root=root)
            run(revert=True,root=root);run(revert=True,root=root);run(check=True,revert=True,root=root)
            row=MANIFEST['files'][0];path=root/row['path'];path.write_bytes(b'unrelated')
            with self.assertRaisesRegex(ValueError,'Unrelated edits'):
                run(root=root)
            self.assertEqual(path.read_bytes(),b'unrelated')


if __name__ == '__main__':
    unittest.main()
