"""The display component returns a choice; story owners supply actual retry semantics."""
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/'game/room13_meeting_retry_ui.rpy').read_text()

class MeetingRetryContract(unittest.TestCase):
    def test_two_distinct_return_values_and_prompt_preserves_return(self):
        self.assertIn('R13_MEETING_RETRY_ACCEPT="accept"',SOURCE)
        self.assertIn('R13_MEETING_RETRY_RETRY="retry"',SOURCE)
        self.assertEqual(re.findall(r'action Return\(([^)]+)\)',SOURCE),
                         ['R13_MEETING_RETRY_ACCEPT','R13_MEETING_RETRY_RETRY'])
        self.assertRegex(SOURCE,r'label r13_meeting_retry_prompt:\s+call screen r13_meeting_retry_choice\s+return _return')

    def test_no_story_mutations_or_unapproved_failure_hook(self):
        for forbidden in ('r13_v111_set(', 'r13_nw_meeting_end(', 'Jump(', 'Start(', 'renpy.load(', 'room13['):
            self.assertNotIn(forbidden,SOURCE)
        for path in (ROOT/'game').glob('*.rpy'):
            if path.name!='room13_meeting_retry_ui.rpy':
                self.assertNotRegex(path.read_text(),r'\bcall (?:screen )?r13_meeting_retry_(?:prompt|choice)\b')

    def test_button_slots_equal_and_reference_lowres_never_upscaled(self):
        self.assertEqual(re.findall(r'area \(\d+,\d+,(\d+),(\d+)\)',SOURCE),[('410','133'),('410','133')])
        self.assertIn('background r13_sticker_button(primary=True)',SOURCE)
        self.assertIn('background r13_sticker_button()',SOURCE)
        self.assertNotIn('ui-button-states',SOURCE)
        for asset in re.findall(r'"(assets/[^\"]+\.png)"',SOURCE):
            self.assertTrue((ROOT/'game'/asset).exists(),asset)

if __name__=='__main__':unittest.main()
