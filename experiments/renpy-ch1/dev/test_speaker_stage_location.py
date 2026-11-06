"""필드의 실제 신규 발화자는 합류하지만 다른 장소의 사람은 이동하지 않는다."""
import copy,textwrap,unittest
from pathlib import Path
from types import SimpleNamespace
SOURCE=(Path(__file__).resolve().parents[1]/'game/room13_v111_idle.rpy').read_text()

def load():
    st=SimpleNamespace(room13={'location':'workshop','v111':{'people':['daram','nabi','resident_teacher','local'],'values':{'location:daram':'school','location:nabi':'school','location:resident_teacher':'school','location:local':'workshop','meeting:fire':'win','KKOMI_ALIVE':True}}})
    ns=dict(store=st,winter_copy=copy,r13_v111_person_alive=lambda p:st.room13['v111']['values'].get('alive:'+p) is not False,
            r13_v111_value=lambda k:st.room13['v111']['values'].get(k),r13_v111_active=lambda:True,
            CAST={'buri':{},'daram':{}},R13_NAMES={'buri':'부리'},r13_offscreen_voice=lambda n:False,_r13_met_line_art=lambda p:p)
    helper=SOURCE[SOURCE.index('    def r13_v111_stage_speaker('):SOURCE.index('    _r13_met_line_art=')]
    callback=SOURCE[SOURCE.index('    def r13_ep_line_art(packet):',SOURCE.index('init 346 python:')):SOURCE.index('    _r13_met_idle_lines=',SOURCE.index('init 346 python:'))]
    exec(textwrap.dedent(helper),ns);exec(textwrap.dedent(callback),ns)
    return ns,st

class SpeakerStage(unittest.TestCase):
    def test_actual_buri_line_never_moves_school_residents_to_workshop(self):
        ns,st=load();before=copy.deepcopy(st.room13);packet=('buri','집게를 빌려드립니다.')
        self.assertEqual(ns['r13_ep_line_art'](packet),packet)
        self.assertEqual(st.room13['v111']['people'],['local','buri'])
        values=st.room13['v111']['values']
        for p in ('daram','nabi','resident_teacher'):self.assertEqual(values['location:'+p],'school')
        self.assertEqual(values['location:buri'],'workshop')
        self.assertEqual({k:v for k,v in values.items() if k!='location:buri'},before['v111']['values'])
        self.assertEqual(before['v111']['people'],['daram','nabi','resident_teacher','local'])

    def test_offscreen_dead_and_departed_speakers_do_not_change_the_world(self):
        for mode in ('offscreen','dead','departed'):
            ns,st=load()
            if mode=='offscreen':ns['r13_offscreen_voice']=lambda n:True
            elif mode=='dead':st.room13['v111']['values']['alive:buri']=False
            else:st.room13['v111']['values']['departed:buri']=True
            before=copy.deepcopy(st.room13);ns['r13_ep_line_art'](('buri','말'))
            self.assertEqual(st.room13,before)

if __name__=='__main__':unittest.main()
