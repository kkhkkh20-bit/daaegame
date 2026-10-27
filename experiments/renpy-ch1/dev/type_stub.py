"""시험용 글자 단계 스텁. 실제 단계표(game/systems/room13_type_scale.rpy)를 읽어 r13_type 과 같은 값을 준다."""
from test_type_scale import load_scale
def r13_type_stub(touch=False,large=False,small=False):
    ns=load_scale(touch=touch,large=large,small=small)
    return ns['r13_type']
