"""New-world meetings on the existing meeting stage (game/room13_v111_meeting_stage.rpy)."""
import ast,inspect,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT/'game'
SRC=(GAME/'room13_v111_meeting_stage.rpy').read_text()
def meetings():
    block=re.search(r'    R13_NW_MEETINGS=(\{.*?\n    \})\n',SRC,re.S).group(1)
    return eval(block,{'dict':dict})
SPEAKERS=ast.literal_eval(re.search(r'MS14_SPEAKERS = (\{.*?\})\n',(GAME/'ms14_story.rpy').read_text(),re.S).group(1))
for _m in re.finditer(r'MS14_SPEAKERS\.update\((\{.*?\})\)',(GAME/'room13_v111_later_bindings.rpy').read_text()):SPEAKERS.update(ast.literal_eval(_m.group(1)))
GENERATED=''.join((GAME/f).read_text() for f in ('room13_v111_days123.rpy','room13_v111_days45.rpy','room13_v111_days610.rpy','room13_v111_days1114.rpy'))
LABELS=set(re.findall(r'^label (r13_v111_\w+):',GENERATED,re.M))
RULES=(GAME/'room13_v111_newworld_rules.rpy').read_text()

class MeetingStage(unittest.TestCase):
    def test_every_meeting_label_exists(self):
        for key,m in meetings().items():
            missing=['r13_v111_'+l for l in m['labels'] if 'r13_v111_'+l not in LABELS]
            self.assertEqual(missing,[],key)
    def test_a_label_belongs_to_one_meeting(self):
        seen={}
        for key,m in meetings().items():
            for l in m['labels']:
                self.assertNotIn(l,seen,(key,seen.get(l)));seen[l]=key
    def test_meeting_keys_are_the_rules_meetings(self):
        ruled=set(re.findall(r'r13_nw_(?:meeting_end|retry)\([\'"](\w+)[\'"]',GENERATED))
        self.assertEqual(set(meetings()),ruled)
    def test_cast_names_are_speakers(self):
        for key,m in meetings().items():
            self.assertTrue(m['cast'],key)
            for name in m['cast']:self.assertIn(name,SPEAKERS,(key,name))
    def test_each_meeting_contains_its_proof_and_result(self):
        body={};cur=None
        for line in GENERATED.split('\n'):
            mm=re.match(r'label (r13_v111_\w+):',line)
            if mm:cur=mm.group(1);body[cur]=[];continue
            if cur:body[cur].append(line)
        for key,m in meetings().items():
            text='\n'.join(l for lab in m['labels'] for l in body['r13_v111_'+lab])
            self.assertRegex(text,r'r13_nw_(?:meeting_end|retry)\([\'"]%s[\'"]'%key,key)
    def test_label_callback_takes_ren_py_arguments(self):
        # Ren'Py 8.5 calls label callbacks with (name, abnormal).
        self.assertRegex(SRC,r'def r13_nw_stage_label\(name,abnormal')
        self.assertIn('config.label_callbacks.append(r13_nw_stage_label)',SRC)
    def test_stage_helpers_do_not_shadow_rule_helpers(self):
        defined=set(re.findall(r'^\s+def (\w+)\(',SRC,re.M))
        rules=set(re.findall(r'^\s+def (\w+)\(',RULES,re.M))
        self.assertEqual(defined&rules,set())
    def test_old_meetings_keep_their_screens(self):
        say=(GAME/'screens.rpy').read_text()
        # 0.19.98: old debates keep their boxed screen; new-world meeting lines use the night
        # dialogue with the same meeting stage and header.
        self.assertIn('r13_meeting_claim in R13_DEBATE and not r13_nw_meeting_claim(r13_meeting_claim)',say)
        # 2026-10-27: 회의 상태로 돌아온 현장에서 물건을 읽을 때(r13_field_reading)는 무대를 깔지 않는다.
        self.assertIn('if r13_meeting_active and r13_nw_meeting_claim(r13_meeting_claim) and not r13_field_reading:\n            use r13_meeting_stage(',say)
        self.assertIn('use r13_meeting_tools(r13_meeting_claim,r13_meeting_live_target())',say)
        more=(GAME/'systems/room13_playback.rpy').read_text()
        self.assertIn('if r13_meeting_active and not r13_nw_meeting_claim(r13_meeting_claim):\n        use r13_meeting_more_tools',more)

if __name__=='__main__':unittest.main()
