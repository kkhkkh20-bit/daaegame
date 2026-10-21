"""New-world rule layer: one-shot meetings, transfer list, money, thief rule, ending order."""
import re,textwrap,unittest
import test_v111 as source_tests
ROOT=source_tests.ROOT
NW=ROOT/'game/room13_v111_newworld.rpy'

class NewWorldSystems(unittest.TestCase):
 def setUp(self):
  source_tests.Transactions.setUp(self)
  block=re.search(r'^init 318 python:\n((?:[ \t].*\n|\n)*)',NW.read_text(),re.M).group(1)
  exec(textwrap.dedent(block),self.env)
  self.v=self.env['r13_v111_value'];self.set=self.env['r13_v111_set']
 def f(self,name,*a):return self.env[name](*a)

 # Meetings (plan 7-1 to 7-3)
 def test_correct_presentation_wins_and_cannot_be_retried(self):
  self.assertEqual(self.f('r13_nw_judge','lamp:knife_shard',['E11','E12'],['V111:E12','V111:E11']),'won')
  with self.assertRaisesRegex(Exception,'not open'):self.f('r13_nw_judge','lamp:knife_shard',['E11'],['V111:E11'])
 def test_wrong_presentation_settles_the_issue_as_lost(self):
  self.assertEqual(self.f('r13_nw_judge','lamp:knife_shard',['E11'],['V111:E99']),'lost')
  self.assertEqual(self.v('issue:lamp:knife_shard'),'lost')
  self.assertIsNone(self.v('meeting:lamp'),'non-gate loss keeps the meeting going')
 def test_listed_half_presentation_hardens_once_then_loses(self):
  partial=[['E11']]
  self.assertEqual(self.f('r13_nw_judge','lamp:knife_shard',['E11','E12'],['V111:E11'],partial),'hardened')
  self.assertTrue(self.f('r13_nw_issue_open','lamp:knife_shard'))
  self.assertEqual(self.f('r13_nw_judge','lamp:knife_shard',['E11','E12'],['V111:E11'],partial),'lost')
 def test_unlisted_half_presentation_is_a_plain_loss(self):
  self.assertEqual(self.f('r13_nw_judge','lamp:knife_shard',['E11','E12'],['V111:E11'],[['E12']]),'lost')
 def test_hardened_issue_can_still_be_won(self):
  self.f('r13_nw_judge','lamp:knife_shard',['E11','E12'],['V111:E11'],[['E11']])
  self.assertEqual(self.f('r13_nw_judge','lamp:knife_shard',['E11','E12'],['V111:E11','V111:E12']),'won')
 def test_empty_presentation_costs_nothing(self):
  self.assertEqual(self.f('r13_nw_judge','lamp:knife_shard',['E11'],[]),'empty')
  self.assertIsNone(self.v('issue:lamp:knife_shard'))
 def test_lost_gate_ends_meeting_as_lose_and_locks_the_rest(self):
  self.f('r13_nw_judge','lamp:tok_innocent',['E10'],['V111:E99'])
  self.assertEqual(self.v('meeting:lamp'),'lose')
  self.assertEqual(self.v('issue:lamp:culprit_words'),'locked')
  self.assertFalse(self.f('r13_nw_issue_open','lamp:knife_shard'))
 def test_results_win_partial_lose(self):
  for name in ('tok_innocent','knife_shard','closed_words','culprit_words'):self.f('r13_nw_choose','lamp:'+name,1,1)
  self.assertEqual(self.f('r13_nw_meeting_close','lamp'),'win')
  self.f('r13_nw_choose','gate_post:height',1,1);self.f('r13_nw_choose','gate_post:kongi_time',1,1);self.f('r13_nw_choose','gate_post:grey_cloth',1,2)
  self.assertEqual(self.f('r13_nw_meeting_close','gate_post'),'partial','unreached issues count as not won')
  self.assertEqual(self.v('issue:gate_post:shoes'),'locked')
 def test_close_is_one_shot(self):
  self.f('r13_nw_choose','records:recipient',1,1);self.f('r13_nw_choose','records:old_mandate',1,1)
  self.assertEqual(self.f('r13_nw_meeting_close','records'),'partial')
  self.f('r13_nw_meeting_close','records')
  self.assertEqual(self.v('meeting:records'),'partial')
  with self.assertRaisesRegex(Exception,'not open'):self.f('r13_nw_choose','records:last_page',1,1)
 def test_altar_partial_needs_two_other_wins(self):
  self.f('r13_nw_choose','altar:all_die',1,1);self.f('r13_nw_choose','altar:altar_origin',1,1)
  self.assertEqual(self.f('r13_nw_meeting_close','altar'),'lose')
  source_tests.Transactions.setUp(self);self.setUp()
  self.f('r13_nw_choose','altar:all_die',1,1);self.f('r13_nw_choose','altar:altar_origin',1,1);self.f('r13_nw_choose','altar:iron_when',1,1)
  self.assertEqual(self.f('r13_nw_meeting_close','altar'),'partial')
 def test_needs_keep_a_later_issue_closed_after_an_earlier_loss(self):
  self.env['R13_NW_MEETINGS']['lamp']['needs']={'culprit_words':('closed_words',)}
  self.f('r13_nw_choose','lamp:closed_words',1,2)
  self.assertFalse(self.f('r13_nw_issue_open','lamp:culprit_words'))
 def test_unknown_issue_is_rejected(self):
  with self.assertRaisesRegex(Exception,'Unknown meeting issue'):self.f('r13_nw_judge','lamp:nothing',['E1'],['V111:E1'])

 # Transfer list (plan 7-6)
 def test_list_cart_and_departure(self):
  self.assertTrue(self.f('r13_nw_list','daram','room13_lose'))
  self.assertFalse(self.f('r13_nw_list','daram','again'))
  self.assertTrue(self.v('daram_wristband'))
  self.f('r13_nw_list','resident_tok','lamp_lose');self.f('r13_nw_list','bami','gate_post_lose')
  self.assertEqual(self.f('r13_nw_cart_departs',['bami']),['daram','resident_tok'])
  self.assertTrue(self.v('departed:daram'));self.assertFalse(self.v('departed:bami'))
  self.assertEqual(self.f('r13_nw_cart_departs',[]),['daram','resident_tok'],'the cart leaves once')
  with self.assertRaisesRegex(Exception,'Departed'):self.f('r13_nw_unlist','daram')
 def test_unlist_and_unknown_person(self):
  self.f('r13_nw_list','daram','x');self.assertTrue(self.f('r13_nw_unlist','daram'))
  self.assertFalse(self.v('daram_wristband'));self.assertEqual(self.f('r13_nw_listed'),[])
  with self.assertRaises(Exception):self.f('r13_nw_list','karo','x')
 def test_dead_listed_person_does_not_board(self):
  self.f('r13_nw_list','resident_piko','street');self.set('piko_alive',False)
  self.assertEqual(self.f('r13_nw_listed'),[])

 # Money and the thief rule (plan 8-3 to 8-9)
 def test_wages_pay_once_and_spending_needs_money(self):
  self.assertTrue(self.f('r13_nw_earn','wage:d2',2));self.assertFalse(self.f('r13_nw_earn','wage:d2',2))
  self.assertEqual(self.f('r13_nw_nyang'),2)
  self.assertFalse(self.f('r13_nw_spend','bori_debt',6));self.assertEqual(self.f('r13_nw_nyang'),2)
  self.f('r13_nw_earn','wage:d3',3);self.f('r13_nw_earn','mom_savings',6)
  self.assertTrue(self.f('r13_nw_spend','bori_debt',6));self.assertTrue(self.f('r13_nw_spend','bori_debt',6))
  self.assertEqual(self.f('r13_nw_nyang'),5,'paying twice charges once')
 def test_second_theft_puts_dad_on_the_list(self):
  self.assertEqual(self.f('r13_nw_steal','cart_d11'),1);self.assertEqual(self.f('r13_nw_steal','cart_d11'),1)
  self.assertFalse(self.v('listed:dad'))
  self.assertEqual(self.f('r13_nw_steal','lamp_d11'),2);self.assertTrue(self.v('listed:dad'))
  self.assertEqual(self.f('r13_nw_steal','cover_d11'),2)

 # Deaths and endings (plan 11-1)
 def test_loss_count_reads_the_five_lives(self):
  self.assertEqual(self.f('r13_nw_loss_count'),0)
  self.set('piko_alive',False);self.set('KKOMI_ALIVE',False);self.set('route12','late_exposure')
  self.assertEqual(self.f('r13_nw_dead'),['resident_piko','kid_kkomi','kid_dodam'])
  self.set('nero_alive',False);self.assertEqual(self.f('r13_nw_ending14'),'frozen')
 def test_ending_order(self):
  e=lambda:self.f('r13_nw_ending14')
  self.assertEqual(e(),'morning')
  self.set('crowd_injury',True);self.assertEqual(e(),'violence')
  self.set('outcome13','departed');self.assertEqual(e(),'partial')
  self.set('outcome13','family_priority');self.assertEqual(e(),'family')
  for key in ('piko_alive','KKOMI_ALIVE','OWL_ALIVE','nero_alive'):self.set(key,False)
  self.assertEqual(e(),'frozen')
  self.set('departed:dad',True);self.assertEqual(e(),'left_name_dad')
  self.set('departed:daram',True);self.assertEqual(e(),'left_name')
 def test_true_ending_needs_every_condition(self):
  ready=lambda:self.f('r13_nw_true_ending_ready')
  self.set('ending14','morning');self.set('neoul_ledger_secured',True)
  for m in ('records','hypothesis','blanket'):self.set('meeting:'+m,'win')
  self.assertFalse(ready())
  self.set('meeting:altar','win');self.assertTrue(ready())
  self.set('OWL_ALIVE',False);self.assertFalse(ready())
  self.set('OWL_ALIVE',True);self.set('ending14','violence');self.assertFalse(ready())
 def test_frozen_text_reader_and_family_variant(self):
  rows=lambda:[t for _,t in self.f('r13_nw_ending_rows','frozen')]
  self.assertIn('나비',rows()[2])
  self.set('departed:nabi',True);self.assertIn('토실',rows()[2])
  self.set('outcome13','family_priority');self.assertIn('입구 옆 자리',' '.join(rows()))
  for kind in ('left_name','left_name_dad','true'):self.assertTrue(self.f('r13_nw_ending_rows',kind))

 # Wiring
 def test_dispatch_and_proof_are_wired(self):
  days=(ROOT/'game/room13_v111_days1114.rpy').read_text()
  dispatch=days.split('label r13_v111_ending_dispatch14:\n',1)[1].split('\nlabel ',1)[0]
  order=[m for m in re.findall(r'jump (\w+)',dispatch)]
  self.assertEqual(order,['r13_nw_left_name_ending14','r13_nw_frozen_ending14','r13_v111_family_ending14','r13_v111_partial_ending14','r13_v111_violence_ending14','r13_v111_morning_safe14'])
  cookie=days.split('label r13_v111_cookie_scene14:\n',1)[1].split('\nlabel ',1)[0]
  self.assertLess(cookie.index('r13_nw_true_epilogue14'),cookie.index("'story14_completed'"))
  proof=(ROOT/'game/room13_v111.rpy').read_text()
  self.assertIn('label r13_v111_proof(key,correct,success,wrong=None,hint=None,issue=None,partial=None,hardened=None):',proof)
  for label in ('r13_nw_left_name_ending14','r13_nw_frozen_ending14','r13_nw_true_epilogue14','r13_nw_story_end14'):
   self.assertIn('label '+label+':',NW.read_text())
 def test_no_new_screen_before_design_approval(self):
  self.assertNotRegex(NW.read_text(),r'(?m)^screen ')

if __name__=='__main__':unittest.main()
