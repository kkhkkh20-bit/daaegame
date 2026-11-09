"""좌우 팬은 카메라만 옮기며, 물건·사람 회피가 인물을 반대편에 다시 배치하지 않는다."""
import copy
import unittest
from test_additional_field_layout import functions


def actor(person,x):
    return dict(person=person,pose='neutral',x=x,y=400,width=120,height=210,
                rect=[x,400,120,210],depth=610,contact='standing',slot=True)


class PanoramaPeople144(unittest.TestCase):
    def setUp(self):
        self.offset=0
        self.camera_reads=[]
        self.layout={'initial_x':320}
        self.ns=dict(r13_world_height=lambda:720,r13_view_width=lambda:1280,
                     r13_layout=lambda:self.layout,r13_actor_face_target=lambda a:a['rect'],
                     R13_CLEAR_STEP_MAX=320,r13_world_offset=self.read_camera)
        def place(a,pose,fx,fy,h):
            return dict(a,x=fx-a['width']/2,
                        rect=[fx-a['width']/2,a['y'],a['width'],a['height']])
        self.ns['r13_ma_place']=place
        for path,names in [
            ('game/systems/room13_investigation_balance.rpy',{'r13_balance_translate'}),
            ('game/room13_v111_field_layout.rpy',{
                'r13_stage_reference_view','r13_clear_critical_x','r13_separate_overlaps',
                'r13_clear_objects','r13_separate_overlaps_final',
                'r13_foot_in_keepout','r13_keepout_cover_rects'})]:
            exec(compile(functions(path,names),path,'exec'),self.ns)

    def read_camera(self):
        self.camera_reads.append(self.offset)
        return self.offset

    def compare_pans(self,name,x,critical):
        rows=[actor('resident_lamplighter',x),actor('resident_badook',x+20)]
        before=copy.deepcopy(rows)
        results=[]
        for self.offset in (0,320,640,0):
            if name=='r13_clear_critical_x':
                result=[self.ns[name](rows[0],critical,rows,1920),rows[1]]
            else:
                result=self.ns[name](rows,critical,1920)
            results.append(result)
        self.assertEqual(rows,before)
        self.assertTrue(all(r==results[0] for r in results[1:]),name)
        self.assertEqual(self.camera_reads,[],name)
        self.assertEqual([a['person'] for a in results[0]],[a['person'] for a in rows])
        self.assertEqual([a['y'] for a in results[0]],[a['y'] for a in rows])

    def test_object_side_step_does_not_follow_camera(self):
        self.compare_pans('r13_clear_critical_x',60,[(100,350,130,270)])

    def test_first_overlap_pass_does_not_follow_camera(self):
        self.compare_pans('r13_separate_overlaps',620,[])

    def test_final_object_clearance_does_not_follow_camera(self):
        self.compare_pans('r13_clear_objects',580,[(680,350,130,270)])

    def test_final_overlap_pass_does_not_follow_camera(self):
        self.compare_pans('r13_separate_overlaps_final',620,[])

    def test_reference_view_uses_authored_initial_frame_and_clamps_old_layouts(self):
        reference=self.ns['r13_stage_reference_view']
        self.assertEqual(reference(1920),(320,1600))
        self.layout['initial_x']=9000
        self.assertEqual(reference(1920),(640,1920))
        self.layout['initial_x']=-10
        self.assertEqual(reference(1920),(0,1280))
        self.assertEqual(reference(900),(0,900))
        self.assertEqual(self.camera_reads,[])


if __name__=='__main__':unittest.main()
