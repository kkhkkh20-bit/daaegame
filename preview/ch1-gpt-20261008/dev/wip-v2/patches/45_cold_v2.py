# [적용 2026-10-10 사용자 결정: 시각 태그 자정] build.py가 wip-v2/patches/를 적용하므로 이 패치는 별도 v2 빌드에 포함된다.
# 현재 구현은 자정 단일 방문·침대 밑 발견. 노션의 새벽 재방문·주전자 시안과의 차이는 CODEX_AGENT_REVIEW_20261010.txt 참고.
# 원칙: 범인은 '???'(EP.COLD_SPEAKER 그대로). 얼굴·옷·손 종류·웃음·프로필 노출 없음. 돈은 화면에 직접 보이지 않음.
#       새 그림 없이 기존 침대(INTRO02_bed)·문(INTRO03_door) 그림과 기존 카메라 자리만 쓴다.
# 흐름: 천 스치는 소리 → 숨기던 손이 멈칫하는 기척(손은 안 보임) → '어… 뭐야?' / '이봐요. 일어나 봐요.' / '……죽었어?' / '젠장. 여기서 나오면 내가…'
#       → 망설임과 다시 움직이는 소리 → 암전. 옛 반복 독백('문 열렸네' '확인만' '돌아가면' '다시 나가자' 등)은 모두 뺀다.
# 소리: 천 스침 전용 효과음이 없어 기존 콜드오픈 숨소리(breath, 대역 잡음)를 임시로 쓴다(새 효과음 미제작). 심장 박동은 기존대로 비트마다 빨라진다.
#       옛 비트 번호(01~19)에 붙던 카메라·소리 표(inn_audio STAGE)는 v번호에 걸리지 않아, 아래 배열에 카메라 값을 직접 적었다.
rep(' EP.COLD_SPEAKER="???";',
''' EP.COLD_V1=EP.COLD;   /* [검토용] 옛 콜드오픈 보관 */
 EP.COLD=[
  {"id":"v01","img":"art/ch1/bg/INTRO02_bed.png","z":1,"fx":0.72,"fy":0.6,"push":4,"duck":0.8,"fxs":"breath","tag":"자정","say":"(사락… 사락…)"},
  {"id":"v02","img":"art/ch1/bg/INTRO02_bed.png","z":1.3,"fx":0.74,"fy":0.6,"push":3,"duck":0.5,"say":"(무언가를 밀어 넣던 기척이 뚝 멈춘다.)"},
  {"id":"v03","img":"art/ch1/bg/INTRO02_bed.png","z":1.8,"fx":0.74,"fy":0.62,"push":4,"duck":0.4,"say":"어… 뭐야?"},
  {"id":"v04","img":"art/ch1/bg/INTRO02_bed.png","z":1.8,"fx":0.74,"fy":0.62,"dim":0.8,"duck":0.35,"say":"이봐요. 일어나 봐요."},
  {"id":"v05","img":"art/ch1/bg/INTRO02_bed.png","z":2.1,"fx":0.74,"fy":0.62,"dim":0.7,"duck":0.15,"fxs":"heart","say":"……죽었어?"},
  {"id":"v06","img":"art/ch1/bg/INTRO03_door.png","z":1,"fx":0.5,"fy":0.5,"duck":0.3,"say":"젠장. 여기서 나오면 내가…"},
  {"id":"v07","img":"art/ch1/bg/INTRO03_door.png","z":1,"fx":0.5,"fy":0.5,"duck":0.5,"fxs":"step","say":"(망설이는 숨소리… 사락, 다시 움직이는 소리)"},
  {"id":"v08","img":"art/ch1/bg/INTRO03_door.png","z":1.8,"fx":0.7,"fy":0.55,"shade":true,"black":450,"title":"1장. 열세 번째 침대","sfx":"doorClose"}
 ];
 EP.COLD_SPEAKER="???";''')
