"""11일 주민 행동은 실제 인계·가족 대화·광부 동행의 경계를 지킨다."""
import ast
import copy
import itertools
import json
import re
import unittest

from test_newworld_text import Layer, ROOT


class ResidentDay11(Layer):
    def label(self,name):
        source=(ROOT/'game/room13_v111_days1114.rpy').read_text()
        return re.search(r'^label '+name+r':\n(.*?)(?=^label |\Z)',source,re.M|re.S).group(1)

    def lines(self,env,label):
        rows=[]
        for match in re.finditer(r'r13_v111_lines\((\[[^\]]*\])\)',self.label(label)):
            rows+=env['r13_v111_lines'](ast.literal_eval(match.group(1)))
        return rows

    def test_tosil_eats_only_at_actual_school_handoff_without_assigning_family_or_supply(self):
        env=self.load()
        arrival=self.label('r13_v111_nabi_arrival11')
        self.assertIn("r13_v111_arrive(['daram', 'resident_tosil', 'nabi'])",arrival)
        self.assertIn("r13_v111_wait('tosil_handoff11')",self.label('r13_v111_tosil_handoff11'))
        waiting=self.lines(env,'r13_v111_nabi_waiting11')
        self.assertFalse(any('네 그릇만 씻으면' in row[1] for row in waiting))
        for custody in ('detained',None):
            with self.subTest(grandmother_custody=custody):
                env['r13_v111_set']('grandmother_custody',custody)
                before=copy.deepcopy(self.state.room13)
                rows=self.lines(env,'r13_v111_tosil_safe11')
                texts=[row[1] for row in rows]
                self.assertTrue(any('네 그릇만 씻으면' in t for t in texts))
                self.assertFalse(any('온실' in t or '편지' in t for t in texts))
                self.assertEqual(before,self.state.room13)
                env['r13_v111_commit']('MS14_D11_S01_L0052')
                self.assertTrue(env['r13_v111_value']('tosil_safe_handoff_confirmed'))
                self.assertEqual(env['r13_v111_value']('tosil_location'),'school')
                self.assertIs(env['r13_v111_value']('tosil_knows_greenhouse'),False)
                self.assertIsNot(env['r13_v111_value']('family_school_place'),True)
                self.assertIsNot(env['r13_v111_value']('school_supply_handed'),True)

    def test_button_scene_is_current_family_action_across_contact_and_blanket_branches(self):
        env=self.load()
        for owl_alive,read5,relay10,blankets in itertools.product((False,True),(False,True),(False,True),(0,1,2)):
            with self.subTest(owl_alive=owl_alive,read5=read5,relay10=relay10,blankets=blankets):
                for key,value in (('OWL_ALIVE',owl_alive),('mother_first_contact_read5',read5),
                                  ('mother_contact_relay10',relay10),('carried_dry_blankets',blankets)):
                    env['r13_v111_set'](key,value)
                before=copy.deepcopy(self.state.room13)
                rows=self.lines(env,'r13_v111_button11')
                texts=[row[1] for row in rows]
                self.assertTrue(any('소매 끝 잡을게' in t for t in texts))
                self.assertTrue(any('바늘을 멈춘다' in t for t in texts))
                self.assertFalse(any('구금' in t or '초롱에게 답' in t or '마차를 봤' in t for t in texts))
                self.assertTrue(set(row[0] for row in rows)<={None,'dad','daram','mom'})
                self.assertEqual(before,self.state.room13,'단추 장면이 연락 청취·담요·생사를 쓰지 않는다')

    def test_all_guldol_beats_disappear_together_when_original_actor_is_unavailable(self):
        env=self.load()
        anchor='MS14_D11_S03_L0006'
        data=json.loads((ROOT/'game/v111/newworld/d11.json').read_text())
        added=data['after'][anchor]
        self.assertEqual([row.get('when') for row in added],['guldol_ready']*3)
        new_texts={row['text'] for row in added}
        for ready in (True,False):
            with self.subTest(ready=ready):
                env['r13_v111_actor_ready']=lambda person:ready if person=='resident_guldol' else True
                before=copy.deepcopy(self.state.room13)
                rows=env['r13_v111_lines']([anchor])
                shown={row[1] for row in rows}&new_texts
                self.assertEqual(shown,new_texts if ready else set())
                self.assertEqual(before,self.state.room13)
        fallback=self.lines(env,'r13_v111_mother_heat11')
        self.assertFalse({row[1] for row in fallback}&new_texts)
        self.assertNotIn('MS14_D11_S03_L0006',self.label('r13_v111_mother_heat11'))

    def test_observation_preserves_existing_list_supply_rescue_and_hypothesis_state(self):
        env=self.load()
        env['r13_v111_actor_ready']=lambda person:True
        env['r13_v111_set']('guldol_facility_seen',True)
        for listed in (False,True):
            env['r13_v111_set']('listed:resident_guldol',listed)
            before=copy.deepcopy(self.state.room13)
            rows=env['r13_v111_lines'](['MS14_D11_S03_L0006'])
            self.assertTrue(any('등 앞을 가리지' in row[1] for row in rows))
            self.assertEqual(before,self.state.room13)
            self.assertIs(env['r13_v111_value']('listed:resident_guldol'),listed)
        self.assertIsNot(env['r13_v111_value']('school_supply_handed'),True)
        self.assertIsNot(env['r13_v111_value']('public_road_escort_completed'),True)
        self.assertIsNone(env['r13_v111_value']('meeting:hypothesis'))

    def test_three_manuscripts_and_nine_extracts_have_separate_release_boundaries(self):
        folder=ROOT/'docs/design/resident-reactions-day101112-20261106'
        matching=json.loads((folder/'day11_매칭.json').read_text())
        self.assertEqual(matching['day'],11)
        self.assertEqual([s['id'] for s in matching['scenes']],['RR11_01','RR11_02','RR11_03'])
        manuscript=(folder/'day11_원고.md').read_text()
        sections=re.findall(r'^## (0[456])\. (.*?)(?=^## |\Z)',manuscript,re.M|re.S)
        self.assertEqual([n for n,_ in sections],['04','05','06'])
        for _,body in sections:
            self.assertTrue(900<=len(body)<=1400,len(body))
            self.assertIn('11일',body.splitlines()[2])
            self.assertNotIn('MS14_',body)
            self.assertNotIn('NW_',body)
        data=json.loads((ROOT/'game/v111/newworld/d11.json').read_text())
        all_rows={row['id']:row for section in ('before','after','blocks') for rows in data[section].values() for row in rows}
        keys=[key for s in matching['scenes'] for key in s['game_added_ids']]
        self.assertEqual(len(keys),9)
        self.assertEqual(len(set(keys)),9)
        for scene in matching['scenes']:
            self.assertEqual(set(scene['scene_extent']),{'full_manuscript','short_extract'})
            for key in scene['game_added_ids']:
                self.assertIn(key,all_rows)
                self.assertNotEqual(all_rows[key]['kind'],'thought')


if __name__=='__main__':unittest.main()
