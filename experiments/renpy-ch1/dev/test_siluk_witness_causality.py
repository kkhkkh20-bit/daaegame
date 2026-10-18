"""Execute the actual authored event label with production payment/witness helpers."""
import copy,textwrap,unittest
from test_siluk_advance_timing import SilukAdvanceIntegration

class WitnessCausality(SilukAdvanceIntegration):
    def run_event(self):
        body=self.source.split('label r13_siluk_advance_events:\n',1)[1].split('\nlabel ',1)[0]
        py=[]
        for line in textwrap.dedent(body).splitlines():
            indent=line[:len(line)-len(line.lstrip())];code=line.lstrip()
            if code.startswith('$ '):code=code[2:]
            elif code.startswith('call '):code=code[5:]
            elif code=='return':code='pass'
            py.append(indent+code)
        self.n.update(room13=self.s,r13_ev_here=lambda *a:None)
        def capture(rows,identity,**kw):
            if identity.startswith('ev:a:witness:'):
                self.assertFalse(self.f('r13_siluk_advance_record')['witness_seen'])
            self.heard.append((identity,rows))
        self.n['r13_lines']=capture
        exec(compile('\n'.join(py),'actual r13_siluk_advance_events','exec'),self.n)
    def prepare_witness(self,day):
        self.pay();self.s.update(day=day,period=0);self.people.add('resident_kongi')
    def witness_packets(self):
        return [(identity,rows) for identity,rows in self.heard if identity.startswith('ev:a:witness:')]
    def check_exchange(self,day,identity,timeword):
        self.prepare_witness(day);cash=self.f('r13_wallet',self.s)['cash'];self.run_event()
        packets=self.witness_packets();self.assertEqual(1,len(packets));self.assertEqual(identity,packets[0][0]);rows=packets[0][1]
        self.assertEqual(['dad','resident_kongi','dad','resident_kongi','dad'],[r[0] for r in rows])
        self.assertIn('찾고 있어',rows[0][1]);self.assertTrue(rows[1][1].startswith(timeword));self.assertIn('들어가는 것만',rows[3][1])
        self.assertNotIn('선금',rows[1][1]+rows[3][1]);self.assertNotIn('빚',rows[1][1]+rows[3][1])
        self.assertTrue(self.f('r13_siluk_advance_record')['witness_seen']);self.assertNotIn('know_siluk_debt',self.s['flags'])
        self.assertEqual(cash,self.f('r13_wallet',self.s)['cash']);self.assertEqual([],self.s['evidence'])
    def test_next_day_actual_question_precedes_witness(self):self.check_exchange(4,'ev:a:witness:next_day','어제')
    def test_later_actual_question_does_not_give_npc_payment_date(self):self.check_exchange(7,'ev:a:witness:later','며칠 전에')
    def test_event_repeat_and_serialized_state_dont_repeat(self):
        self.prepare_witness(4);self.run_event();self.store.room13=copy.deepcopy(self.s);self.run_event();self.assertEqual(1,len(self.witness_packets()))
    def test_same_day_does_not_trigger_witness(self):
        self.prepare_witness(3);self.s['period']=2;self.run_event();self.assertEqual([],self.witness_packets())
    def test_no_colocation_does_not_trigger_witness(self):
        self.prepare_witness(4);self.people.clear();self.run_event();self.assertEqual([],self.witness_packets())
    def test_legacy_unknown_does_not_invent_witness_date(self):
        self.s['flags']=['siluk_scammed'];self.people.add('resident_kongi');self.s['day']=7;self.run_event();self.assertEqual([],self.witness_packets())
if __name__=='__main__':unittest.main()
