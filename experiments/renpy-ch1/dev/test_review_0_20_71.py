"""0.20.71 외부 정밀 리뷰 반영 회귀(2026-10-27): R01 이름표·울타리, R03 휴대폰 발언 접힘, R04 등록 뒤 생각,
R07 질문 화면 발 선, R09 원본 재열람, R10 획득 효과음 1회."""
import copy
import json
import re
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

from test_play_review_field import load_function

ROOT = Path(__file__).resolve().parents[1]


class R01NameplateAvoidsObjects(unittest.TestCase):
    def nameplates(self, obstacles):
        faces = {'karo': [1000, 625, 52, 29], 'daram': [1100, 700, 50, 40]}
        names = dict(karo='까로', daram='다람')
        ns = dict(r13_touch_ui=lambda: False, r13_actor_face_target=lambda a: faces[a['person']],
                  r13_actor_nameplate=lambda a: (faces[a['person']][0] + faces[a['person']][2] / 2, faces[a['person']][1] - 36),
                  r13_world_width=lambda: 2467, r13_world_offset=lambda: 760, r13_view_width=lambda: 1707,
                  r13_field_zoom=lambda: .75, R13_NAMES=names, R13_CONTROL=dict(width=232),
                  r13_control_height=lambda: 64, store=SimpleNamespace(R13_LIFE_GROUPS=[]),
                  r13_field_ui_rects=lambda offset: [], r13_nameplate_obstacles=lambda: obstacles)
        rows = load_function('game/room13_interaction.rpy', 'r13_actor_nameplates', ns)(
            [dict(person=k, rect=v) for k, v in faces.items()])
        return {row['person']: row['rect'] for row in rows}

    @staticmethod
    def overlap(a, b):
        return max(0, min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])) * max(0, min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]))

    def test_label_moves_off_the_rules_board(self):
        rules = (986, 513, 75, 114)
        without = self.nameplates([])
        self.assertGreater(self.overlap(without['karo'], rules), 0, '벌점이 없으면 이름표가 게시판 위에 놓이는 배치여야 한다')
        with_rules = self.nameplates([rules])
        self.assertEqual(self.overlap(with_rules['karo'], rules), 0)
        # 머리 곁을 떠나지 않는다(후보는 좌우 90px·위 두 줄 안).
        self.assertLess(abs(with_rules['karo'][0] - without['karo'][0]), 100)
        self.assertLess(abs(with_rules['karo'][1] - without['karo'][1]), 80)

    def test_face_outranks_object(self):
        # 모든 후보가 얼굴 아니면 물건에 걸리면 얼굴을 비우는 쪽을 고른다.
        faces = {'karo': [1000, 625, 52, 29]}
        big = (0, 0, 2467, 960)
        ns = dict(r13_touch_ui=lambda: False, r13_actor_face_target=lambda a: faces[a['person']],
                  r13_actor_nameplate=lambda a: (1026, 589), r13_world_width=lambda: 2467, r13_world_offset=lambda: 760,
                  r13_view_width=lambda: 1707, r13_field_zoom=lambda: .75, R13_NAMES=dict(karo='까로'),
                  R13_CONTROL=dict(width=232), r13_control_height=lambda: 64, store=SimpleNamespace(R13_LIFE_GROUPS=[]),
                  r13_field_ui_rects=lambda offset: [], r13_nameplate_obstacles=lambda: [big])
        rows = load_function('game/room13_interaction.rpy', 'r13_actor_nameplates', ns)([dict(person='karo', rect=faces['karo'])])
        self.assertEqual(self.overlap(rows[0]['rect'], tuple(faces['karo'])), 0)

    def test_obstacles_are_visible_objects_and_critical_rects(self):
        objects = {'gate': {'rules': dict(rect=[986, 513, 75, 114]), 'hidden': dict(rect=[1, 1, 1, 1], hide=True)}}
        ns = dict(store=SimpleNamespace(room13={'location': 'gate'}), ROOM13={'objects': objects},
                  r13_object_visible=lambda spec: not spec.get('hide'),
                  r13_layout=lambda location: {'critical': [[986, 513, 75, 114], [1661, 583, 201, 98]]})
        rects = load_function('game/systems/room13_field_obstacles.rpy', 'r13_nameplate_obstacles', ns)()
        self.assertEqual(rects, [(986, 513, 75, 114), (1661, 583, 201, 98)])


class R01FenceFollowsWideGate(unittest.TestCase):
    def test_fence_and_bucket_rects_take_the_wide_gate_shift(self):
        source = (ROOT / 'game/room13_v111_later_bindings.rpy').read_text()
        self.assertIn('rect=r13_gate_wide_rect([850,300,170,240])', source)
        self.assertIn('rect=r13_gate_wide_rect([1050,500,150,140])', source)
        shift = load_function('game/systems/room13_field_obstacles.rpy', 'r13_gate_wide_rect', dict(R13_WORLD_LAYOUTS={'gate': {'wide_shift': [320, 200]}}))
        self.assertEqual(shift([850, 300, 170, 240]), [1170, 500, 170, 240])
        self.assertEqual(load_function('game/systems/room13_field_obstacles.rpy', 'r13_gate_wide_rect', dict(R13_WORLD_LAYOUTS={}))([850, 300, 170, 240]), [850, 300, 170, 240])
        # 옮긴 울타리 천(1170,500)은 규칙 게시판(986,513,75,114)과 겹치지 않는다.
        fence = (850 + 320, 300 + 200, 170, 240)
        rules = (666 + 320, 313 + 200, 75, 114)
        self.assertEqual(R01NameplateAvoidsObjects.overlap(fence, rules), 0)
        self.assertGreater(R01NameplateAvoidsObjects.overlap((850, 300, 170, 240), rules), 0, '옮기기 전에는 겹쳐 있었다')


class R03PhoneQuoteFolded(unittest.TestCase):
    def test_phone_opens_with_the_quote_folded(self):
        source = (ROOT / 'game/systems/room13_proof_workspace.rpy').read_text()
        self.assertIn('default quote_open=remembered.get("quote_open",not r13_touch_ui())', source)
        # 접힘이면 본문이 발언 틀 자리까지 올라온다.
        ns = dict(r13_touch_ui=lambda: True, R13_NB_LEFT=20, R13_NB_RIGHT=824, R13_NB_WIDTH=804, R13_NB_TOP=60,
                  r13_nb_footer_y=lambda: 330, r13_pw_chip_height=lambda: 40, r13_pw_tab_height=lambda: 44,
                  r13_pw_quote_height=lambda text, width: 60, r13_pw_card_height=lambda: 80,
                  persistent=SimpleNamespace(room13_large_text=False))
        layout = load_function('game/systems/room13_proof_workspace.rpy', 'r13_pw_layout', ns)
        folded = layout(False, '발언')
        opened = layout(True, '발언')
        self.assertEqual(folded['quote_h'], 0)
        self.assertEqual(opened['body_top'] - folded['body_top'], 60 + 24 + 8)


class R04RegisteredThought(unittest.TestCase):
    def goal(self, registered, scene_text):
        source = re.split(r'^(?=\S)', (ROOT / 'game/systems/room13_v111_goal.rpy').read_text().split('init 341 python:\n', 1)[1], flags=re.M)[0]
        ns = dict(store=SimpleNamespace(room13={'v111': {'gate': 'travel'}}), r13_v111_goal=lambda: scene_text,
                  r13_day2_guidance=lambda: None, r13_v111_value=lambda key: registered if key == 'gate_registered' else None,
                  R13_V111_QUESTIONS={'MS14_D01_S04': '우리 두 사람 모두 제대로 등록됐을까?'})
        exec(textwrap.dedent(source), ns)
        return ns['r13_v111_goal']()

    def test_question_is_replaced_once_registration_is_done(self):
        stale = '우리 두 사람 모두 제대로 등록됐을까?'
        self.assertEqual(self.goal(False, stale), stale)
        self.assertEqual(self.goal(True, stale), '등록은 끝났다. 여관에서 13호 방과 아내의 소식을 확인하자.')
        self.assertEqual(self.goal(True, '다른 장면'), '다른 장면')


class R07QuestionScreenFeet(unittest.TestCase):
    def test_dot_profiles_stand_inside_the_screen(self):
        art = json.loads((ROOT / 'game/assets/room13-dialogue-talk-art.json').read_text())
        source = (ROOT / 'game/room13_fullbody_dialogue.rpy').read_text()
        for person in ('guard', 'daram', 'karo'):
            profile = art['people'][person]['profiles']['840']
            ns = dict(r13_dialogue_source_profile=lambda p, pose, h, profile=profile: profile,
                      R13_QUESTION_FEET_LINE=int(re.search(r'R13_QUESTION_FEET_LINE=(\d+)', source).group(1)),
                      r13_dot_feet=load_function('game/room13_fullbody_dialogue.rpy', 'r13_dot_feet', {}))
            y = load_function('game/room13_fullbody_dialogue.rpy', 'r13_question_close_y', ns)(person, 840, 110, 'interview_neutral')
            feet = y + ns['r13_dot_feet'](profile)
            self.assertLessEqual(feet, 720 - 8, person)
            self.assertGreater(feet, 660, person)
            # 대사창 기준 발 선(640+110=750)은 화면 밖이었다.
            self.assertGreater(110 + 640, 720)
        self.assertIn('ypos r13_question_close_y(person,840,110,pose)', (ROOT / 'game/systems/room13_side_questions.rpy').read_text())

    def test_other_art_keeps_the_dialogue_rule(self):
        ns = dict(r13_dialogue_source_profile=lambda p, pose, h: None, r13_close_y=lambda p, h, t, pose: 777, R13_QUESTION_FEET_LINE=712)
        self.assertEqual(load_function('game/room13_fullbody_dialogue.rpy', 'r13_question_close_y', ns)('x', 840, 110, 'p'), 777)


class R09OriginalRereadIsShort(unittest.TestCase):
    def test_second_reading_shows_only_the_document(self):
        day = (ROOT / 'game/room13_v111_days123.rpy').read_text()
        block = day.split('label r13_v111_gate_read_original:\n', 1)[1].split('\nlabel ', 1)[0]
        self.assertIn("v111_reread_original=r13_has('v111:applied:MS14_D01_S03_L0002')", block.split('\n')[0])
        self.assertIn("call r13_lines([] if v111_reread_original else r13_v111_lines(['MS14_D01_S03_L0003'", block)
        # 문서 본문(L0002)은 매번 보인다.
        self.assertIn("call r13_lines(r13_v111_lines(['MS14_D01_S03_L0002'])", block)
        self.assertLess(block.index("v111_reread_original=r13_has"), block.index("r13_v111_commit('MS14_D01_S03_L0002')"))


class R10FoundSoundOnce(unittest.TestCase):
    def test_one_acquisition_requests_found_once(self):
        log = []
        store = SimpleNamespace(room13={'evidence': [], 'records': {}, 'day': 1, 'period': 0, 'location': 'gate'})
        ns = dict(store=store, winter_copy=copy, source_fx=log.append, renpy=SimpleNamespace(notify=lambda t: None),
                  persistent=SimpleNamespace(room13_knowledge=[]),
                  ROOM13={'evidence': {'V111:E03': {'name': '원본', 'kind': '기록'}}},
                  _r13_sound_evidence_acquired=lambda keys: None)
        load_function('game/systems/room13_sound.rpy', 'r13_evidence_acquired', ns)
        grant = load_function('game/room13_rules.rpy', 'r13_grant', ns)
        grant(['V111:E03'], 'gate')
        self.assertEqual(log, ['found'])
        grant(['V111:E03'], 'gate')
        self.assertEqual(log, ['found'], '이미 가진 자료는 소리도 없다')

    def test_without_the_feedback_layer_the_rule_still_sounds_once(self):
        log = []
        store = SimpleNamespace(room13={'evidence': [], 'records': {}, 'day': 1, 'period': 0, 'location': 'gate'})
        ns = dict(store=store, winter_copy=copy, source_fx=log.append, renpy=SimpleNamespace(notify=lambda t: None),
                  persistent=SimpleNamespace(room13_knowledge=[]), ROOM13={'evidence': {'E1': {'name': 'x', 'kind': '물건'}}})
        load_function('game/room13_rules.rpy', 'r13_grant', ns)(['E1'], 'q')
        self.assertEqual(log, ['found'])


if __name__ == '__main__':
    unittest.main()
