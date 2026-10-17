# 0.19.17 엄마 찾기 줄기 (systems/room13_threads.rpy). 앞 단계(1~5)는 0.19.16 r13_mother_knowledge를 그대로 쓴다.
init 181 python:
    def _r13_mk(field):
        return lambda s:r13_mother_knowledge(s)[field]
    r13_thread("mom",[
        ("memo",lambda s:"M01" in s.get("evidence",[]),"엄마가 13호 책상에 메모를 남겼다.","메모에 적힌 ‘등불을 돌보는 사람’은 누구일까?"),
        ("named",lambda s:"M01" in s.get("evidence",[]) and r13_mother_knowledge(s)["named"],"등불을 돌보는 사람은 초롱이다.","초롱도 엄마를 만났을까?"),
        ("recognized",_r13_mk("recognized"),"초롱은 엄마의 글씨와 얼굴을 알아봤다.","언제 어디서 만났고, 엄마는 무엇을 맡겼을까?"),
        ("promised",_r13_mk("promised"),"엄마가 초롱에게 가족 앞으로 봉투를 맡겼다.","봉투에는 무엇이 적혀 있고, 언제 받을 수 있을까?"),
        ("received",_r13_mk("received"),"엄마가 맡긴 봉투를 읽었다. 엄마는 오라는 편지를 쓴 적이 없다고 했다.","그럼 우리를 부른 초대 편지는 누가 썼을까?"),
        ("letter",lambda s:"N06" in s.get("evidence",[]),"엄마가 초롱을 통해 직접 편지를 보냈다.","엄마는 지금 어디에 숨어 있을까?"),
        ("hideout",lambda s:"Y02" in s.get("evidence",[]),"숲 뿌리 밑 은신처는 들켰고, 엄마는 더 깊은 곳으로 옮겼다.","엄마는 어디로 옮겼을까?"),
        ("reunited",lambda s:"mom_reunited" in s.get("flags",[]),"엄마를 다시 만났다.","엄마가 연구해 온 것으로 마을을 구할 수 있을까?"),
    ])
