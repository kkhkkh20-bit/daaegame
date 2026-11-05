"""소설 적용 후 정보 청취·예방·구형 저장·학교 결말의 실제 대사 경로 검증."""
import re
import unittest
import test_newworld_text as layer

SOURCE = layer.ROOT / 'game/room13_v111_days1114.rpy'


class NovelLateGame(layer.Layer):
    def setUp(self):
        self.load()
        self.rows = []
        self.present = {'mom', 'daram'}
        self.env.update(
            r13_lines=lambda rows, tag=None: self.rows.extend(rows),
            r13_v111_actor_ready=lambda person: person in self.present,
            r13_v111_scene=lambda *a: None,
            r13_edit=lambda **kw: None,
            r13_v111_score=lambda: None,
            r13_v111_travel=lambda *a: None,
            r13_v111_arrive=lambda people: None,
            r13_v111_guldol_heat11=lambda: None,
            r13_v111_mother_heat11=lambda: None,
        )
        self.env['room13'] = self.state.room13

    def run_label(self, name):
        """입력 없는 대상 라벨을 그대로 실행해 출력·상태·다음 라벨을 확인한다."""
        source = SOURCE.read_text()
        match = re.search(r'^label ' + re.escape(name) + r':\n(.*?)(?=^label |^init |\Z)', source, re.M | re.S)
        self.assertIsNotNone(match)
        code = []
        for line in match.group(1).splitlines():
            indent = line[:len(line) - len(line.lstrip())]
            statement = line.lstrip()
            if statement.startswith('$ '):
                line = indent + statement[2:]
            elif statement.startswith('call '):
                line = indent + statement[5:]
            elif statement.startswith('jump '):
                line = indent + 'return ' + repr(statement[5:])
            code.append(line)
        exec('def run_authored_label():\n' + '\n'.join(code), self.env)
        self.rows.clear()
        target = self.env['run_authored_label']()
        return target, ' '.join(row[1] for row in self.rows)

    def setv(self, **values):
        for key, value in values.items():
            self.env['r13_v111_set'](key, value)

    def test_reunion_uses_actual_first_letter_and_relay_independently(self):
        for first in (False, True):
            for relay in (False, True):
                with self.subTest(first=first, relay=relay):
                    self.setv(mother_first_contact_read5=first, mother_contact_relay10=relay, OWL_ALIVE=False)
                    target, text = self.run_label('r13_v111_mother_life11')
                    self.assertEqual(target, 'r13_v111_mother_ready11')
                    self.assertTrue(self.env['r13_v111_value']('mother_q_life'))
                    self.assertEqual('그저께' in text, relay)
                    self.assertEqual('우리는 벌써 그 여관에 있었잖아' in text, first)
                    self.assertEqual('너희 마차를 봤어' in text, not first)

    def test_reunion_does_not_remember_custody_on_owl_survival_path(self):
        self.setv(mother_first_contact_read5=True, mother_contact_relay10=True, OWL_ALIVE=True)
        _, text = self.run_label('r13_v111_mother_life11')
        self.assertNotIn('붙잡혔다는', text)
        self.assertNotIn('손목의 멍', text)
        self.assertNotIn('그저께', text)

    def test_shortened_questions_still_unlock_existing_ready_gate(self):
        for first in (False, True):
            self.setv(mother_first_contact_read5=first)
            self.run_label('r13_v111_mother_life11')
            self.run_label('r13_v111_mother_invitation11')
            self.run_label('r13_v111_mother_return11')
            self.assertEqual(self.run_label('r13_v111_mother_ready11')[0], 'r13_v111_mother_last11')

    def test_stone_prevention_does_not_invent_child_fever(self):
        self.setv(stone_warm_felt3=True)
        for sick in (False, True):
            self.setv(D07_S03_medical_request_completed=sick)
            _, text = self.run_label('r13_v111_facility11')
            self.assertEqual('아팠잖아' in text, sick)
            self.assertIn('벽', text)
        self.setv(stone_warm_felt3=False)
        self.assertEqual(self.run_label('r13_v111_facility11')[1], '')

    def test_school_portrait_completes_only_new_waiting_path_once(self):
        self.setv(ending14='morning', piko_alive=False, portrait='unfinished', portrait_waiting_for_mom=True)
        target, text = self.run_label('r13_v111_cookie14')
        self.assertEqual(target, 'r13_v111_cookie_scene14')
        self.assertIn('빈 코 자리', text)
        self.assertEqual(self.env['r13_v111_value']('portrait'), 'child_completed')
        self.assertFalse(self.env['r13_v111_value']('portrait_waiting_for_mom'))
        _, again = self.run_label('r13_v111_cookie14')
        self.assertNotIn('코를 그려 넣는다', again)
        self.assertIn('초상을 꺼내', again)

    def test_other_endings_absent_family_and_living_piko_do_not_get_new_completion(self):
        for ending, present, piko in [('family', {'mom', 'daram'}, False), ('partial', {'mom', 'daram'}, False), ('morning', {'mom'}, False), ('morning', {'mom', 'daram'}, True)]:
            with self.subTest(ending=ending, present=present, piko=piko):
                self.present = present
                self.setv(ending14=ending, piko_alive=piko, portrait='unfinished', portrait_waiting_for_mom=True)
                _, text = self.run_label('r13_v111_cookie14')
                self.assertNotIn('빈 코 자리', text)
                self.assertEqual(self.env['r13_v111_value']('portrait'), 'unfinished')

    def test_old_completed_portrait_is_acknowledged_without_drawing_again(self):
        self.setv(ending14='morning', piko_alive=False, portrait='child_completed', portrait_waiting_for_mom=None)
        _, text = self.run_label('r13_v111_cookie14')
        self.assertIn('잘 가져왔네', text)
        self.assertNotIn('코를 그려 넣는다', text)

    def test_granny_new_confession_is_not_shared_with_prevention_or_unproved_path(self):
        for alive, verdict in [(False, 'win'), (True, 'win'), (False, 'partial'), (False, 'lose')]:
            self.setv(OWL_ALIVE=alive)
            self.env['r13_v111_set']('meeting:room13', verdict)
            rows = self.env['r13_v111_lines'](['MS14_D14_S03_L0032'])
            text = ' '.join(row[1] for row in rows)
            if not alive and verdict == 'win':
                self.assertIn('불이 날 줄은 몰랐어요', text)
                self.assertIn('아이가 살아서 나오더군요', text)
                self.assertLess(text.index('숨을 쉬었어요'), text.index('내가 쳤어요'))
                self.assertLess(text.index('내가 쳤어요'), text.index('아이가 살아서 나오더군요'))
            else:
                self.assertNotIn('내가 쳤어요', text)
                self.assertNotIn('그 애가 죽으면', text)


if __name__ == '__main__':
    unittest.main()
