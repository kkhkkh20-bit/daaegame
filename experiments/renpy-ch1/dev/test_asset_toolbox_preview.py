"""빠른 미리보기 보호 검사. SDK나 게임 프로세스를 실제로 실행하지 않는다."""
from pathlib import Path
import os
import selectors
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import asset_toolbox_preview as preview


class AssetToolboxPreview(unittest.TestCase):
    def test_missing_sdk_stops_before_subprocess_and_releases_lock(self):
        with tempfile.TemporaryDirectory() as directory:
            project=Path(directory);(project/'game').mkdir()
            with patch.dict(preview.os.environ,{'RENPY_SDK':str(project/'absent-sdk')}), \
                 patch.object(preview.subprocess,'Popen') as process:
                with self.assertRaisesRegex(preview.PreviewError,'SDK'):
                    preview.capture(project)
                process.assert_not_called()
            self.assertFalse(preview._LOCK.locked())
            self.assertFalse((project/'docs/reviews/toolbox-preview/current.png').exists())

    def test_changed_fixture_fails_instead_of_capturing_a_different_scene(self):
        with tempfile.TemporaryDirectory() as directory:
            game=Path(directory);(game/'qa_tests').mkdir()
            source=game/'qa_tests/admin_meeting.rpy'
            for text in ('testcase another_case:\n    pause 1\n',
                         'testcase admin_meeting_replay:\n    screenshot "different.png"\n'):
                with self.subTest(text=text):
                    source.write_text(text,encoding='utf-8')
                    with self.assertRaises(preview.PreviewError):preview._fixture(game)

    def test_current_fixture_keeps_actual_meeting_entry_and_assertions(self):
        game=Path(__file__).resolve().parents[1]/'game'
        fixture=preview._fixture(game)
        self.assertIn('testcase toolbox_meeting_preview:',fixture)
        self.assertIn('회의 바로 테스트 (진행 보존)',fixture)
        self.assertIn('assert eval (r13_meeting_active',fixture)
        self.assertIn('screenshot "toolbox-meeting-current.png"',fixture)
        self.assertNotIn('r13_debate_mark(',fixture)

    def test_concurrent_capture_is_refused_before_project_access(self):
        preview._LOCK.acquire()
        try:
            with self.assertRaisesRegex(preview.PreviewError,'이미 회의'):
                preview.capture(Path('/does-not-exist'))
        finally:preview._LOCK.release()

    def test_input_fingerprint_ignores_generated_cache_but_detects_mapping_edits(self):
        with tempfile.TemporaryDirectory() as directory:
            game=Path(directory);(game/'asset-toolbox').mkdir()
            binding=game/'asset-toolbox/bindings.json';binding.write_text('{}')
            original=preview._fingerprint(game)
            (game/'cache').mkdir();(game/'cache/generated').write_text('cache')
            (game/'script.rpyc').write_bytes(b'compiled')
            self.assertEqual(preview._fingerprint(game),original)
            binding.write_text('{"changed":true}')
            self.assertNotEqual(preview._fingerprint(game),original)

    def test_cleanup_kills_detached_child_but_leaves_unrelated_process_running(self):
        child_code=('import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); '
                    'print("ready",flush=True); time.sleep(60)')
        parent_code=('import subprocess,sys,time; '
                     'p=subprocess.Popen([sys.executable,"-u","-c",sys.argv[1]],'
                     'stdout=subprocess.PIPE,start_new_session=True); '
                     'p.stdout.readline(); print(p.pid,flush=True); time.sleep(60)')
        unrelated=subprocess.Popen([sys.executable,'-c','import time; time.sleep(60)'])
        parent=subprocess.Popen([sys.executable,'-u','-c',parent_code,child_code],
                                stdout=subprocess.PIPE,start_new_session=True)
        child=None;owned={}
        try:
            with selectors.DefaultSelector() as selector:
                selector.register(parent.stdout,selectors.EVENT_READ)
                self.assertTrue(selector.select(timeout=5))
            child=int(parent.stdout.readline())
            self.assertNotEqual(os.getpgid(child),os.getpgid(parent.pid))
            owned=preview._owned_processes(parent.pid)
            self.assertIn(child,owned)
            preview._stop(parent)
            self.assertFalse(preview._alive(owned))
            self.assertIsNone(unrelated.poll())
        finally:
            preview._signal_owned(owned,preview.signal.SIGKILL)
            if parent.poll() is None:parent.kill()
            parent.wait(timeout=3);parent.stdout.close()
            unrelated.terminate();unrelated.wait(timeout=3)


if __name__=='__main__':unittest.main()
