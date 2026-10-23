"""Unified collection and showing-to-gift contracts, using the actual shop completion layer."""
import copy,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Materials(unittest.TestCase):
    def setUp(self):
        self.store=types.SimpleNamespace(room13=dict(day=5,period=0,case_state='occurred',flags=[],evidence=['E01','E06'],read_topics=[],inspection_items={'inventory':['pencil']},livelihood={'cash':30,'items':['herbs','lamp_oil']}))
        self.content={'evidence':{'E01':dict(name='편지',kind='물증'),'E06':dict(name='목격담',kind='증언')},'topics':{}}
        env=dict(winter_copy=copy,store=self.store,ROOM13=self.content,persistent=types.SimpleNamespace(room13_knowledge=['E01']),R13_BORROW={'knife':dict(title='작업칼',npc='buri',deposit=5,detail='작업 도구')},R13_INSPECTION_ITEMS={'pencil':('연필','글을 쓴다.')},r13_home_with_daram=lambda:True)
        exec(textwrap.dedent((ROOT/'game/systems/room13_livelihood_model.rpy').read_text().split('init 91 python:\n')[1]),env)
        env['r13_has']=lambda key:key in self.store.room13['flags'] or key in self.store.room13['evidence']
        env['r13_inspection_state']=lambda:copy.deepcopy(self.store.room13['inspection_items'])
        def topics(person):
            return [(k,t) for k,t in self.content['topics'].items() if t['npc']==person and t['day'][0]<=self.store.room13['day']<=t['day'][1]]
        def finish(key):
            spec=self.content['topics'][key]
            for k in spec['give']:
                if k not in self.store.room13['evidence']:self.store.room13['evidence'].append(k)
            for flag in spec['flags']:
                if flag not in self.store.room13['flags']:self.store.room13['flags'].append(flag)
            self.store.room13['read_topics'].append(key)
        env.update(r13_topics=topics,r13_finish_topic=finish)
        shop=(ROOT/'game/systems/room13_shop.rpy').read_text().split('init 94 python:\n')[1].split('\nscreen r13_shop')[0]
        exec(textwrap.dedent(shop),env)
        source=(ROOT/'game/systems/room13_materials.rpy').read_text().split('init 148 python:\n')[1].split('\nlabel r13_show_catalog_object')[0]
        exec(textwrap.dedent(source),env);self.e=env
    def test_transfer_badge_is_owned_actionable_and_read_only(self):
        self.e['R13_NAMES']={'resident_seori':'서리','buri':'부리'}
        before=copy.deepcopy(self.store.room13)
        badge=self.e['r13_catalog_transferable']
        self.assertTrue(badge('bag:herbs'))
        self.assertFalse(badge('E01'))
        self.assertFalse(badge('tool:pencil'))
        self.assertFalse(badge('bag:knife'))
        self.assertFalse(badge(None))
        self.assertEqual(before,self.store.room13)
        self.store.room13['evidence'].append('E20')
        self.assertFalse(badge('bag:herbs'))

    def test_all_material_kinds_share_one_read_only_collection(self):
        before=copy.deepcopy(self.store.room13)
        self.assertEqual(set(self.e['r13_catalog_entries']()),{'E01','E06','tool:pencil','bag:herbs','bag:lamp_oil'})
        self.assertEqual(self.e['r13_catalog_title']('bag:herbs'),'해열 약초 묶음')
        self.assertEqual(self.store.room13,before)
    def test_new_evidence_keeps_existing_evidence_positions(self):
        before=self.e['r13_catalog_entries'](hearing=True)
        self.content['evidence']['E02']=dict(name='새 기록',kind='기록')
        self.store.room13['evidence'].append('E02')
        self.assertEqual(self.e['r13_catalog_entries'](hearing=True),before+['E02'])
    def test_hearing_and_archive_never_include_inventory_or_invent_ownership(self):
        self.assertEqual(set(self.e['r13_catalog_entries'](hearing=True)),{'E01','E06'})
        self.assertEqual(self.e['r13_catalog_entries'](archive=True),['E01'])
        self.assertFalse(self.e['r13_catalog_can_present']('bag:herbs',True))
        self.assertFalse(self.e['r13_catalog_can_present']('E20'))
        self.assertFalse(self.e['r13_catalog_can_present']('bag:not_real'))
    def test_showing_or_declining_leaves_inventory_rewards_and_help_unchanged(self):
        before=copy.deepcopy(self.store.room13)
        self.assertEqual(self.e['r13_catalog_offer']('resident_seori','bag:herbs'),'item:herbs')
        self.assertIsNone(self.e['r13_catalog_offer']('daram','bag:herbs'))
        self.assertIsNone(self.e['r13_catalog_offer']('resident_seori','tool:pencil'))
        self.assertEqual(self.store.room13,before)
    def test_acceptance_uses_actual_shop_layer_once(self):
        self.assertTrue(self.e['r13_complete_catalog_offer']('resident_seori','bag:herbs','item:herbs'))
        state=self.store.room13
        self.assertNotIn('herbs',state['livelihood']['items'])
        self.assertEqual(state['evidence'].count('E20'),1)
        self.assertEqual(len(state['resident_help']),1)
        after=copy.deepcopy(state)
        self.assertFalse(self.e['r13_complete_catalog_offer']('resident_seori','bag:herbs','item:herbs'))
        self.assertEqual(self.store.room13,after)
    def test_stale_or_wrong_recipient_cannot_commit(self):
        before=copy.deepcopy(self.store.room13)
        self.assertFalse(self.e['r13_complete_catalog_offer']('daram','bag:herbs','item:herbs'))
        self.assertFalse(self.e['r13_complete_catalog_offer']('resident_seori','bag:herbs','item:hat'))
        self.assertEqual(self.store.room13,before)
    def test_shop_purchase_does_not_record_help(self):
        state=dict(day=3,period=0,flags=['livelihood_open'],evidence=['E01'],livelihood={'cash':10})
        purchased,ok=self.e['r13_purchase'](state,'lamp_oil')
        self.assertTrue(ok);self.assertNotIn('resident_help',purchased)
        self.assertEqual(purchased['evidence'],['E01'])
    def test_hand_over_topics_are_hidden_but_still_available_from_showing(self):
        self.assertNotIn('item:herbs',dict(self.e['r13_topics']('resident_seori')))
        self.assertEqual(self.e['r13_catalog_offer']('resident_seori','bag:herbs'),'item:herbs')
if __name__=='__main__':unittest.main()
