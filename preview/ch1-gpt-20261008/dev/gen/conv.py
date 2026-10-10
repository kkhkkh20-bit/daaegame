# 장면 대본 JSON(줄별 전체 상태) → 게임 데이터(EP.PRO, EP.END, EP.I9, 조사·질문 대사 덮어쓰기)
import json,re,sys
D=json.load(open('/tmp/claude-0/in2/sc.json'))
SC={s['id']:s for s in D['scenes']}
# ---- 자체 플레이 검수(2026-10-09) 수정층: 원본 JSON은 그대로 두고 생성 직전에만 고친다 ----
TXT={
 'P1-28':'다람 손님. 네, 그렇게 적어 두겠습니다. 마을 입구 광장에 내려 드릴게요. 해 지기 전엔 도착합니다. 나가는 마차는 내일 정오에 있어요.',  # P3 "마부에게 들었습니다"의 근거
 'P2-06':'산골 마을이니까. 창마다 불이 켜져서 다행이다.',                       # '묵을 곳부터 찾자' 세 번 반복 정리
 'P7-07':'네. 날씨를 적는 중이에요. 저는 도토라고 해요. 매일 이 창에서 같은 시간에 하늘을 보고 적어요.',  # "아니요" 뒤 긍정 모순
 'I04-01':'(침대 밑에 작은 나무 상자가 있다. 숫자 네 개를 맞추는 자물쇠다.)',
 'I04-04':'아빠, 이 상자 잠겨 있어. 열어 보면 안 돼?',                          # 아빠 속마음과 같은 말 반복 대신 아이다운 반응
 'I06-01':'(해가 들어 창고가 밝아졌다. 아까 못 읽은 머리판 글씨를 다시 보자.)',     # '글씨가 보인다'를 다람보다 먼저 말하지 않게
 'I08-01':'(바구니 속 아이 옆구리에 붉은 것이 묻어 있다. 맨눈으로는 잘 안 보인다.)',  # 돋보기를 다람이 꺼내기 전에 말하지 않게
 'I15-01':'(오늘 아침엔 빵 냄새가 나지 않는다. 바쁘시겠지만 어젯밤 일을 여쭤봐야겠다.)', # 아직 듣지 않은 말을 '했다'고 하지 않게
 'I15-10':'(듣거나 본 걸 여쭸는데, 아무도 없었다는 대답부터 하신다. 숨기려는 말이 있는 걸까. 아직은 모른다.)',  # 그림에 없는 '앞치마 만지기' 대신 말에서 읽히는 근거(나비 도트는 세일러복·앞치마 없음)
 'P1-14':'여기 우체국 도장 보이지? 편지를 부친 곳이 찍혀 있어.',   # 어려운 말 '소인' 풀기(사건 정보 유지)
 'P6-10':'저는 밤이예요. 여기서 겨울을 나는 손님이에요. 할머니가 천장에 가로로 놓인 저 나무 하나를 제 자리로 내주셨거든요.',   # '들보' 풀기
 'I16-04':'족제비 손님이 시계 앞을 지나 저쪽으로 갔다가 금방 돌아왔어요. 여섯 시 반쯤.',  # "무엇을 보셨습니까?" → "봤어요." 어색
}
DROP={'P2-04','P5-08','I13-12'}   # 같은 생각·같은 안내 반복, 순서 바뀐 속마음(아래 AFTER로 이동)
AFTER={
 'I07-03':[{'line_id':'I07-03a','type':'발화','speaker':'아빠','text':'실례합니다. 이 아이 상태를 보셨습니까?','display_change':'유지'}],
 'I10-02':[{'line_id':'I10-02a','type':'발화','speaker':'아빠','text':'도토 씨, 어젯밤 첫눈 시간도 적어 두셨습니까?','display_change':'유지'}],
 'I13-13':[{'line_id':'I13-13a','type':'속마음','speaker':'아빠','text':'(대답을 망설이셨다.)','display_change':'유지'}],
}

# ---- 사건 도입 재구성(2026-10-09 사용자 피드백: 사건 전 통성명 과다, 피해·쟁점 불명, 할머니 대응 없음, 너울·회의·규약 불명) ----
# 원칙: 사건 전에는 부녀의 사정과 여관 사람 최소한만. 밤이·도토는 조사 중 첫 만남으로 옮긴다(밤이의 자리 C07도 그때 듣는다).
#       부엌문 수리(P8)·종 시각·목격 시점·찻주전자 위치를 아는 사람은 바꾸지 않는다. 마을엔 국가 기관이 없고 주민 규약과 회의가 있다.
def _L(i,ty,sp,tx,dc='유지',fg='',ex='',sfx=''):return {'line_id':i,'type':ty,'speaker':sp,'text':tx,'display_change':dc,'foreground':fg,'expression_required':ex,'appearance_sfx':sfx,'condition':''}
DROP|={'P6-%02d'%n for n in range(6,21)}|{'P7-%02d'%n for n in range(1,16)}|{'P12-01','P12-03'}
SKIP_SCENES={'P7'}
# ---- 도입 단축(2026-10-10 사용자: "첫 조사까지 대사가 길고 지루하다, 빠르게 조사하면서 그들을 알아가게, 인트로가 너무 길다") ----
# 원칙: 뒤에서 쓰이는 사실(엄마 편지·우체국 도장·정오 마지막 마차·첫눈·겨울잠 손님·등잔·밤 반죽·열세 번째 침대·세련 1박/처음 왔다는 말·숙박부에서 멈춘 할머니·
#       정각에만 치는 종·목걸이 본 노인·간식 마지막 봉지·엄마 사진)은 남기고, 같은 말 되풀이·잡담·인사만 뺀다. 새 대사는 쓰지 않는다(P1-28만 앞부분 줄임).
#       P6(수프)·P8(부엌문 고치는 부리)은 통째로 뺀다: 부리는 조사 중 부엌(C04)에서 처음 만난다.
SKIP_SCENES|={'P6','P8'}
DROP|={'P1-06','P1-09','P1-12','P1-13','P1-16','P1-23','P1-25','P1-26','P1-27','P1-29','P1-30',
       'P2-05','P2-06','P2-08','P2-09','P2-14','P2-15',
       'P3-01','P3-05','P3-10','P3-11','P3-12','P3-13','P3-16',
       'P4-01','P4-07','P4-08','P4-14','P4-15','P4-16',
       'P5-01','P5-06','P5-22','P5-23','P5-24',
       'P9-01','P9-08','P9-11','P9-13','P9-14',
       'P10-03','P10-06','P10-07','P10-08','P10-15',
       'P12-09x','P12-13a','P12-13b','P12-13c','P12-13c2','P12-13f','P12-19'}
# 2026-10-10 03:40 사용자: "항아리(찻주전자) 속 쥐는 조사하다가 발견하게, 프롤로그 안에서 발견까지 가면 너무 길다"
#   → P12 끝(너울이 둘러봐도 된다고 허락)에서 프롤로그를 마치고, 찻주전자 발견·바구니로 옮김·너울 기록은 조사 중 부엌 찬장(o_teapot, script_a.js)으로 옮긴다.
SKIP_SCENES|={'P13'}
DROP|={'P12-18','P12-19','P12-20','P12-21','P12-22','P12-23','P12-24'}
AFTER.setdefault('P12-17',[]).append(_L('P12-z1','속마음','아빠','(마음은 급해도 하나씩 봐야 한다. 창고 안부터 보자.)',fg='너울'))
# 2026-10-10 사용자 승인: 너울 = 보안관 복장 자경단장(허세·성급하게 욱하지만 정의감). 첫 등장에서 소속·온 이유를 짧게, 돈이 나온 것만으로 유죄·양도가 자동 확정되지 않게
#   (너울이 먼저 성급하게 단정 → 아빠의 상식적 반박 → 머쓱하게 인정 → 규약은 '회의에서 정해질 때'). 규약·벌금·허가 조항 자체는 그대로
TXT['P12-11']='규약상 장부에 올리지 않은 손님을 받으면 벌금입니다.'
# 2026-10-10 논리 검수(에이전트 보고) 반영: 지운 줄에 기대던 대답·지시어, 처음 만나는데 이름 부르기, 장면에 없던 동작
TXT.update({
 'P1-17':'엄마가 지금도 거기 있어?',
 'P3-06':'며칠 묵으려고 합니다. 이 마을에서 찾아볼 사람이 있어서요.',
 'P3-09':'그게 올해 마지막 마차일 거예요. 구름 보니 오늘 밤이나 내일이 첫눈이겠어요. 그 안에 볼일을 못 보면 봄까지 여기 있어야 해요.',
 'P3-14':'숙박부는 접수대에서 나비가 적어 줄 거예요. 나비야! 손님 두 분 숙박부 좀.',
 'P3-17':'다람아, 짐 풀고 나서 엄마 사진도 한번 여쭤보자. 지금은 바쁘신 것 같으니까.',
 'P4-09':'우선 사흘로 적어 둘게요. 더 계시면 말씀해 주세요. 저는 여기 일 돕는 나비예요. 2층엔 겨울잠 손님들이 주무시니까 복도에선 조금만 살살 다녀 주세요.',
 'P5-17':'짐 풀고 편히 쉬어요. 필요한 건 아래층에 말하고.',
 'P9-06':'아닙니다. 저희도 오늘 온 손님입니다. 주인 할머니는 안쪽에 계실 겁니다.',
 'P9-09':'내일 정오 마차로 바로 나갈 거라 짐도 가볍게 왔습니다.',
 'P9-17':'(할머니가 이름을 보고 잠깐 멈추셨다. 구면이신가? 별것이 다 마음에 걸린다.)',
 'I01-07':'인주가 아직 덜 말랐네. 손은 이따 씻자.',
 'I07-01':'(부엌문이 열리고 공구 상자를 든 분이 들어와 바구니를 들여다본다.)',
 'I07-04':'장치공 부리예요. 할머니가 불러서 왔는데, 방금 만져 봤어요. 차갑고, 숨도 안 쉬어요.',
 'I11-01':'(우리 이름 바로 아래에 세련 씨 이름이 있다.)',
 'I11-06':'볼일… 무슨 볼일일까?',
 'E2-07':'두 분 서명은 명부에 잘 보관해 둘게요. 봄에 다시 뵙죠.',
 'E2-08':'네. 봄에 또 태워 주세요.',
 'E3-03':'마을 회의에 벌금은 치렀어요. 복도의 그 시계로요.',
})
# 2026-10-10 장르 비교 검수: 조사 구간에서 끊기던 엄마 찾기 서사 한 박자(새 사실 없음: 첫째 권은 10년 전에서 끝나고, 엄마 편지는 몇 해 전)
AFTER.setdefault('I03-09',[]).extend([_L('I03-09a','발화','다람','엄마 이름은… 없네.',fg='다람',ex='걱정'),
 _L('I03-09b','발화','아빠','이 공책은 10년 전에서 끝나. 엄마 편지는 몇 해 전이니까.',fg='다람'),
 _L('I03-09c','속마음','아빠','(그럼 그다음 공책이 있다는 뜻일까.)',fg='다람')])
TXT['P1-28']='감사합니다. 마을 입구 광장에 내려 드릴게요. 나가는 마차는 내일 정오에 있어요.'

TXT.update({
 'P12-13':'그래서 회의를 엽니다. 정오 우편 마차가 떠나기 전에요.',
 'P12-09':'자경단장 너울입니다. 나비 씨가 집까지 달려와 신고하더군요. 사정은 아래층에서 들었습니다.',
 'P12-12':'게다가 주인 창고 침대에서 손님 돈이 나왔다… 이거 뻔한 일 아닙니까!',   # 2026-10-10 너울 재정립(아래 12a~12c)
 'P8-01':'(부엌으로 가는데 문 앞에 공구가 놓여 있다. 다람이가 밟기 전에 불러야겠다.)',
 'E1-04':'세련 씨는 마을 감옥에 들였습니다. 처분은 주민들이 정합니다.',
 'P12-17':'현장의 물건을 옮기지만 않는다면요. 회의에서는 손님도 본 것을 말할 수 있습니다.',
 'I16-01':'(복도 천장에 누가 거꾸로 매달려 있다. 이 소란에 깼는지 졸린 얼굴이다.)',
 'I10-01':'(창가에 공책을 펴 두고 하늘을 보는 분이 있다. 어젯밤 날씨도 적어 두셨을까.)',
 'I10-04':'어젯밤에 올해 첫눈이 왔어요. 정확히 자정, 밤 열두 시예요.',
})
AFTER.update({
 'P6-05':[_L('P6-05a','발화','다람','다 먹었다! 그릇은 내가 들게.'),_L('P6-05b','발화','아빠','부엌에 갖다 드리자. 할머니 혼자 바쁘시겠다.')],
 'P12-09':[_L('P12-09x','발화','너울','나비 씨가 집까지 부르러 왔더군요. 아래층에서 할머니께 사정은 들었습니다.',fg='너울'),
           _L('P12-09a','발화','아빠','자경단이라면, 마을 일을 맡아 보시는 분입니까?',fg='너울'),
           _L('P12-09b','발화','너울','이 마을엔 관리가 따로 없습니다. 주민들이 정한 규약이 있고, 그 규약을 지키게 하는 게 자경단이죠. 회의 기록도 제가 합니다.',fg='너울')],
 'P12-12':[_L('P12-12a','발화','아빠','할머니가 훔치셨다는 증거는 아직 없습니다. 돈이 거기 있었다는 것뿐입니다.',fg='너울'),
           _L('P12-12b','발화','너울','…크흠. 맞는 말입니다. 제가 성급했군요.',fg='너울'),
           _L('P12-12c','발화','너울','규약대로라면, 여관 주인이 손님 돈을 훔쳤다고 회의에서 정해지면 허가를 잃고, 봄 첫 마차 전까지 여관을 새 주인에게 넘겨야 합니다.',fg='너울')],
 'P12-13':[_L('P12-13a','발화','아빠','회의라면, 무엇을 정하는 겁니까?',fg='너울'),
           _L('P12-13b','발화','너울','마을 일은 겨울 주민 명부에 오른 주민들이 모여 표로 정합니다.',fg='너울'),
           _L('P12-13c','발화','너울','말과 증거를 듣고, 돈을 가져간 사람이 누구라고 보는지 표를 던집니다.',fg='너울'),
           _L('P12-13c2','발화','너울','네 표가 모이면 그 사람을 지목하고, 마지막으로 그 사람의 변론을 듣습니다. 결론은 그 뒤에 냅니다.',fg='너울'),
           _L('P12-13d','발화','다람','왜 정오까지예요?',fg='너울'),
           _L('P12-13e','발화','너울','세련 씨가 정오 마차로 떠나시니까요. 그 뒤로는 봄까지 길이 막힙니다.',fg='너울'),
           _L('P12-13f','발화','너울','돈을 잃었다는 분이 떠나기 전에 매듭을 지어야지요.',fg='너울'),
           _L('P12-13g','속마음','아빠','(지금 이대로 회의를 열면, 다들 할머니를 지목하겠지.)',fg='너울')],
 'P12-07':[],
 'I10-02':[_L('I10-02a','발화','아빠','실례합니다. 아래층 일 때문에 여쭤볼 게 있어서요.',fg='도토'),
           _L('I10-02b','발화','도토','네. 저는 도토라고 해요. 매일 이 창에서 같은 시간에 하늘을 보고 날씨를 적어요.',fg='도토'),
           _L('I10-02c','발화','아빠','어젯밤 날씨도 적어 두셨습니까?',fg='도토')],
 'I16-02':[_L('I16-02a','발화','다람','아빠, 위에… 거꾸로 매달려 있어.',fg='밤이'),
           _L('I16-02b','발화','밤이','아, 놀랐어요? 미안해요. 아침엔 원래 자는 시간이라.',fg='밤이'),
           _L('I16-02c','발화','밤이','저는 밤이예요. 여기서 겨울을 나는 손님이에요.',fg='밤이'),
           _L('I16-02d','발화','아빠','소란에 깨셨군요. 몇 가지만 여쭙겠습니다. 밤에는 주로 어디 계십니까?',fg='밤이'),
           _L('I16-02e','발화','밤이','해 질 녘에 일어나서, 새벽 다섯 시 종이 치면 자요. 밤에는 저기 시계 맞은편, 천장에 가로로 놓인 저 나무에 매달려 있고요.',fg='밤이'),
           _L('I16-02f','발화','밤이','복도 등불 옆이라 거기가 제일 따뜻해요.',fg='밤이'),
           _L('I16-02g','연출',None,'[증거 획득: 밤이의 말]',fg='밤이'),
           _L('I16-02h','발화','다람','그럼 밤새 복도가 다 보이겠네요.',fg='밤이'),
           _L('I16-02i','발화','밤이','보이긴 다 보여요. 남의 일엔 끼어들지 않지만, 물어보면 본 대로 대답은 해 줘요.',fg='밤이')],
})
# P12 첫머리: 수색 경과는 아빠 목소리로, 이어서 할머니 일대일(항변·비밀은 지킴) → 할머니 퇴장 → 다람 → 너울
BEFORE={'P12-04':[
 _L('P12-g1','속마음','아빠','(다 같이 방과 복도를 뒤졌다. 주머니는 창고의 열세 번째 침대, 베개 쪽에서 나왔다.)'),
 _L('P12-g2','속마음','아빠','(창가 방 손님이 찾았고, 잃어버린 손님은 자기 봉인이 맞다고 했다. 할머니만 아직 창고 문 앞에 서 계신다.)'),
 _L('P12-g3','연출',None,'할머니 표시','등장','할머니'),
 _L('P12-g4','발화','할머니','그 침대는 남는 침대예요. 어젯밤엔 아무도 안 잤어요.',fg='할머니',ex='경계'),
 _L('P12-g5','발화','할머니','손님 돈에 손을 대다니. 내가 그런 짓을 할 사람으로 보여요?',fg='할머니',ex='걱정'),
 _L('P12-g6','발화','아빠','아닙니다. 주머니가 왜 거기 있었는지는 아직 아무도 모릅니다.',fg='할머니'),
 _L('P12-g7','발화','할머니','…나비를 보내서 자경단장을 불렀어요. 이런 일은 마을 규약대로 해야 하니까.',fg='할머니',ex='걱정'),
 _L('P12-g8','발화','할머니','손님들은 방에 들어가 있어요. 아침부터 미안해요.',fg='할머니',ex='걱정'),
 _L('P12-g9','연출',None,'할머니 퇴장','퇴장',''),
 _L('P12-g10','속마음','아빠','(내려가시면서도 그 베개 구석에서 눈을 떼지 못하셨다. 뭘 걱정하시는 걸까.)'),
],
 'P12-07':[_L('P12-d1','발화','다람','돈은 찾았잖아. 그럼 끝난 거 아니야?',fg='다람'),
           _L('P12-d2','발화','아빠','어디서 나왔는지가 문제야. 할머니네 창고 침대에서 나왔으니까, 할머니가 가져간 거 아니냐고 의심할 수 있어.',fg='다람')],
}
# ---- 도입 재배치(2026-10-10 사용자 최종 확정): 콜드오픈 → 마차(엄마를 찾으러 온 사유·짧은 티키타카) → 광장(여관 찾아 짧게) → 여관(할머니에게 방 받고 짐 풀고 하룻밤)
#      → 다음 날 사건. 세련은 사건 뒤 피해자로 처음 소개, 다른 주민은 조사하며 소개. 승객 명부 서명 제거(E2 서명 참조 정리). 정오 마지막 마차는 간결히.
#      도입에서만 주던 공정한 단서는 지우지 않고 옮긴다:
#        세련이 '처음 와 본다'고 한 말(P9-12): 사건 신고 대사에 넣었다가 사용자 피드백으로 뺌. '처음'이라는 말은 조사 중 C12 증언("어제가 처음입니다")으로만 남고, 장부(C11)와의 모순은 그대로.
#        할머니가 세련을 보고 멈칫한 것(P9-16·17) → 창고 앞 수색 경과(P12-g2b, 아빠가 직접 본 것)로. 할머니 질문(T_ma3)도 같은 근거로(script_a).
#        복도 등잔을 밤새 켜 둔다(P4-11, 밤이 증언의 전제) → 2층 안내(P5-05)로. 겨울잠 손님 안내는 P5-05에 이미 있음.
#        밤 반죽(P4-13)은 나비의 조사 증언(C03)에 그대로 있어 별도 이관 없음. 세련 가방 속 봉인 편지(P9-10)는 사건 단서가 아닌 후일담(E1) 복선이라 E1에서만 보인다.
#      목걸이를 본 노인(P2-10~16)은 조사 중 광장 첫 방문 일회 이벤트로 옮긴다(script_a 광장 장소·BEATS).
SKIP_SCENES|={'P4','P9'}
DROP|={'P1-24','P2-10','P2-11','P2-12','P2-13','P2-16','P3-08','P3-15','P3-17','P3-18'}
TXT.update({
 'P1-22':'손님, 곧 골짜기 마을입니다. 이 마차 마부 까로예요.',
 'P1-28':'마을 입구 광장에 내려 드릴게요. 나가는 마차는 내일 정오, 올해 마지막이에요.',
 'P3-09':'구름 보니 오늘 밤이나 내일이 첫눈이겠어요. 내일 정오 마차를 놓치면 봄까지 여기 있어야 해요.',
 'P3-14':'숙박부에 이름만 적고 따라와요. 방까지 데려다줄게요.',
 'P5-05':'여기가 2층이에요. 양쪽은 겨울잠 손님들 방이라 복도 등잔은 밤새 켜 둬요. 문 앞에선 발소리만 낮춰 줘요.',
 'P5-15':'거긴 지금은 안 쓰는 방이에요. 손님 받는 침대는 열둘이에요.',
 'P11-06':'여기 묵는 여행객, 세련입니다. 계약금이 든 주머니가 없어졌습니다.',   # 2026-10-10 사용자: '늦게 든'·'처음 묵는데' 설명이 길고 어색 → 묵는 손님임과 피해만
 'E2-07':'봄에 다시 뵙죠. 그때까지 잘 지내세요.',
})
# 2026-10-10 사용자: "안 쓰는 방이라고 하는데 다람이가 숫자를 이상하게 센 것처럼 따지는 건 이치에 맞지 않다, 그냥 '안 쓰는구나' 해야지"
#   → 할머니의 '숫자 헷갈린다'와 부녀의 '누가 헷갈렸나' 문답(P5-19~21)을 빼고, 다람은 수긍만. 열세 번째 침대를 센 사실(P5-12·14)은 그대로
DROP|={'P5-19','P5-20','P5-21'}
AFTER.setdefault('P5-15',[]).append(_L('P5-15a','발화','다람','아, 안 쓰는 방이구나.'))
# 2026-10-10 사용자 확정 새 1장 구조 — 첫 우선: 강제 양도 규약 삭제(자동 양도·배액 배상·유죄 시 몰수 규칙을 쓰지 않음).
#   너울의 '허가를 잃고 봄 첫 마차 전까지 새 주인에게 넘긴다'(P12-12c)를 빼고, 회의는 경위를 듣는 자리로. 계약서 뒷면 조항·'허가를 잃는 날' 대사(I01)도 뺌
DROP|={'P12-12c','I01-12'}
TXT.update({'P12-13':'회의를 열어 경위를 듣겠습니다. 정오 우편 마차가 떠나기 전에요.','I01-11':'할머니는 서명하지 않았다는 거지. 이 계약서도 기억해 두자.'})
AFTER.setdefault('P11-06',[]).append(_L('P11-06a','발화','세련','어젯밤 침대 머리맡에 두고 잤는데, 일어나 보니 없었습니다.',fg='세련'))
BEFORE.setdefault('P12-04',[])
_g=BEFORE['P12-04'];_i=[k for k,x in enumerate(_g) if x['line_id']=='P12-g2'][0]
_g.insert(_i+1,_L('P12-g2b','속마음','아빠','(할머니는 아까부터 세련 씨 얼굴을 자꾸 보신다. 구면이신가?)'))
for _s in D['scenes']:
    _n=[]
    for _l in _s['lines']:
        for _b in BEFORE.get(_l['line_id'],[]):_n.append(dict(_b))
        if _l['line_id'] in DROP:continue
        if _l['line_id'] in TXT:_l=dict(_l,text=TXT[_l['line_id']])
        _n.append(_l)
        for _a in AFTER.get(_l['line_id'],[]):
            if _a.get('line_id') in DROP:continue
            _x=dict(_l);_x.pop('appearance_sfx',None);_x.update(_a);_n.append(_x)
    _s['lines']=_n
KEY={'아빠':'det0','다람':'det1','할머니':'innma','세련':'seryeon','너울':'wanggu','나비':'nabi','밤이':'geokkuri','도토':'doto','부리':'buri','까로':'karo'}
# 화면 인물 표정(그림 강도 기준) → 무대 표정 키. 없는 그림은 기본.
def face(who,expr):
    e=expr or ''
    if who=='det1':
        if e in('놀람','당황'):return 'shock'
        if e in('걱정','그리움'):return 'sad'
        if e=='결심':return 'resolve'
        if e in('활짝 웃음','기쁨','큰 웃음'):return 'laugh'
        return ''
    if who=='seryeon':return 'shock' if e in('놀람','다급함') else ''
    if who=='geokkuri':return 'shock' if e in('놀람','당황') else ''
    if who=='innma':
        if e in('경계','망설임','걱정'):return 'think'
        if e in('옅은 미소','안도'):return 'smile'
        return ''
    if who in('doto',):return 'shock' if e in('당황','놀람') else ('think' if e in('의문',) else '')
    if who=='buri':return 'shock' if e in('미안함',) else ''
    if who=='wanggu':return 'think' if e in('의문',) else ''
    return ''
def js(s):return json.dumps(s,ensure_ascii=False)
def fg(l):
    f=l.get('foreground') or ''
    return KEY.get(f.split(' ')[0],'')
# 연출 줄 처리표: 표시할 회색 지문(대체 그림 없는 사실), 효과음, 특수 연출
NARR={'P9-16':'할머니가 나와 숙박부를 받다가, 세련의 이름 앞에서 잠깐 손을 멈춘다.','P1-10':'아빠가 안주머니에서 접힌 편지를 꺼낸다.','P1-24':'아빠와 다람이 차례로 승객 명부에 서명한다.',
 'P2-10':'긴 옷을 입은 노인이 걸음을 멈추고 다람의 목걸이를 바라본다.','P2-11':'노인은 말없이 고개를 돌려 골목으로 사라진다.',
 'P4-06':'아빠가 펜을 받아 두 사람 이름을 적는다.','P9-10':'세련이 내려놓은 가방 틈으로, 처음 보는 봉인이 찍힌 편지 묶음이 보인다.',
 'P13-09':'아빠가 겨울잠쥐를 조심스럽게 꺼내 빈 빵 바구니로 옮기고, 수건을 한 겹 덮는다.',
 'E1-06':'너울의 기록부 사이로, 처음 보는 봉인이 찍힌 편지 묶음이 들어간다.','E2-09':'마차가 고개 너머로 멀어진다. 길이 금세 하얗게 지워진다.',
 'E4-05':'펼쳐진 공책. 표지에 「손님 장부 둘째 권」.','E4-14':'할머니가 다람이 내민 엄마 사진을 한참 들여다보다가, 장부를 천천히 덮는다.',
 'E5-05':'창고 안쪽에서 이불 펴는 소리가 난다.','E5-13':'다람이 마차에서부터 아껴 둔 마지막 간식 봉지를 뜯어, 절반을 아빠 손에 올린다.'}
SFX={'I07-02':'doorOpen','P12-g9':'steps','P1-21':'carStop','P5-16':'door','P8-11':'door','P10-09':'bell10','P12-18':'steps','P13-12':'steps','P13-17':'steps','I04-05':'steps','I07-08':'steps',
 'I12-03':'lock','E2-09':'carDepart','E4-09':'steps','E4-16':'door','E5-08':'steps','P3-15':'steps','P5-18':'steps','P2-11':'steps'}
# 다람 강한 감정(v3 전신 포즈): 장면 대본의 같은 '걱정' 중에서도 무서운 발견을 전하는 줄만. 포즈가 줄마다 바뀌지 않게 이어지는 줄까지 유지
STRONG={'P1-17':'sad','P1-18':'sad','P1-19':'sad','P1-20':'sad','P12-23':'cower','P12-24':'cower','P13-10':'cower','P13-11':'cower','I01-06':'oops','I01-07':'oops'}
INSPECT={'I01-05':'C01a','I01-09':'C01b','I03-06':'C11','I08-04':'C05','I10-03':'C08','I11-03':'C09','I16-09':'C01show'}
def conv(s,mode):
    """mode: play(프롤로그·후일담: 배열+객체) / say(조사·질문: 배열, 연출은 @dir)"""
    out=[];prev_fg=None
    for l in s['lines']:
        lid=l['line_id'];t=l['text'];ty=l['type'];cond=l.get('condition') or ''
        f=fg(l);fc=face(f,l.get('expression_required'))
        entry=cond.startswith('이 장소에 새로 진입') or cond.startswith('첫 진입 또는')
        snd=l.get('appearance_sfx') or ''
        chime=('띠링' in snd)
        old_fg=prev_fg
        if ty!='연출' or l.get('display_change') in('등장','교체','퇴장'):prev_fg=f if l.get('display_change')!='퇴장' else None
        if ty=='연출':
            dc=l.get('display_change')
            d={}
            if lid in SFX:d['sfx']=SFX[lid]
            if dc in('등장','교체') and f:d['who']=f;d['chime']=1 if chime else 0
            if dc=='퇴장':d['who']='none'
            m=re.match(r'\[(안내|암전|증거 획득[^\]]*)\]\s*(.*)',t)
            items=[]
            if lid=='P3-15' or lid=='P5-18' or lid=='P13-17' or lid=='I07-08' or lid=='E5-08':
                # 실제 퇴장 뒤 다람 등장: 비우고 잠깐 뒤 다람
                items.append(('dir',{'who':'none','sfx':SFX.get(lid,'steps'),'ms':380}))
                if lid=='I07-08':items.append(('dir',{'who':'det1','chime':0,'ms':220}))
                elif lid=='E5-08':items.append(('dir',{'who':'det1','chime':1,'ms':220}))
                elif lid=='P13-17':pass
                else:items.append(('dir',{'who':'det1','chime':1,'ms':220}))
                d={}
            elif lid=='P2-10':items.append(('dir',{'who':'none','ms':300}))
            elif lid=='E4-16':items.append(('dir',{'who':'none','sfx':'door','ms':450}));items.append(('dir',{'who':'det1','chime':0,'ms':250}));d={}
            elif lid in('P12-08','P13-12','E4-09','I04-05','E5-05','P6-06','E1-02','E2-02','P1-21'):
                if 'sfx' in d:items.append(('dir',{'sfx':d.pop('sfx'),'ms':380}))
            if m:
                k=m.group(1)
                if k=='안내':items.append(('hint',m.group(2)))
                elif k=='암전':items.append(('fade',1))
                elif k.startswith('증거 획득'):items.append(('grant','C07'))
                d={}
            if d:dd=dict(d);dd.setdefault('ms',4000 if d.get('sfx')=='bell10' else 380 if 'who' in d else 420);items.append(('dir',dd))
            if lid in INSPECT:items.append(('inspect',INSPECT[lid]))
            if lid in NARR:items.append(('narr',NARR[lid]))
            if lid=='P13-09':items.insert(0,('beat','inn_basket_transferred'))
            for it in items:out.append(it+(entry,))
            continue
        w=KEY.get(l.get('speaker'),'narr')
        dc=l.get('display_change')
        if dc in('등장','교체') and f and f!=old_fg and mode in('play','say'):
            out.append(('dir',{'who':f,'chime':1 if chime else 0,'ms':260},entry))
        if lid in STRONG:fc=STRONG[lid]
        if ty=='속마음':out.append(('inner',t,entry,fc));continue
        txt=re.sub(r'^[①②③]\s*','',t)
        out.append(('line',w,txt,fc,entry))
    return out
def emit(items,mode):
    r=[]
    for it in items:
        k=it[0]
        if k=='line':
            _,w,t,fc,entry=it;r.append('L(%s,%s,%s)'%(js(w),js(t),js(fc)) if fc else 'L(%s,%s)'%(js(w),js(t)))
        elif k=='inner':
            _,t,entry,fc=it;r.append('I(%s%s)'%(js(t[1:-1] if t.startswith('(') else t),',null,1' if entry else ''))
        elif k=='narr':r.append('N(%s)'%js(it[1]))
        elif k=='dir':
            d=it[1];entry=it[2]
            if mode=='play':r.append('D(%s)'%js(d))
            else:r.append('L("@dir",%s)'%js(';'.join('%s:%s'%(a,b) for a,b in d.items())+(';entry:1' if entry else '')))
        elif k=='hint':r.append('{hint:%s}'%js(it[1]))
        elif k=='fade':r.append('{fade:1}')
        elif k=='grant':r.append('{grant:"C07",card:1}' if mode=='play' else 'L("@grant","C07")')
        elif k=='beat':r.append('{beat:%s}'%js(it[1]) if mode=='play' else '')
        elif k=='inspect':r.append('L("@inspect",%s)'%js(it[1]))
    return ',\n   '.join(x for x in r if x)
BG={'P1':'carriage','P2':'plaza','P3':'reception','P4':'reception_desk_wide','P5':'corridor','P6':None,'P7':None,'P8':None,'P9':'reception','P10':'room','P11':'corridor','P12':None,'P13':None,
    'E1':'reception','E2':'reception','E3':None,'E4':'corridor','E5':'corridor'}
LOC={'P1':'front','P2':'front','P3':'front','P4':'front','P5':'hall','P6':'dining','P7':'dining','P8':'dining','P9':'front','P10':'hall','P11':'hall','P12':'bed13','P13':'kitchen',
     'E1':'front','E2':'front','E3':'dining','E4':'hall','E5':'hall'}
SUB={'P1':('고갯길, 우편 마차 안','첫날 오후'),'P2':('마을 입구, 광장','첫날 저녁'),'P3':('여관 현관','첫날 저녁'),'P4':('여관 접수대','첫날 저녁'),'P5':('2층 복도','첫날 저녁'),
 'P6':('여관 식당','첫날 저녁'),'P7':('식당 창가 자리','첫날 저녁'),'P8':('식당 안쪽, 부엌문 앞','첫날 저녁'),'P9':('여관 현관','첫날 밤 9시'),'P10':('부녀의 방','첫날 한밤'),
 'P11':('2층 복도','다음 날 아침 7시'),'P12':('2층 창고 앞','아침 7시 반'),'P13':('부엌','아침 7시 반'),
 'E1':('여관 앞','정오'),'E2':('여관 앞, 우편 마차','정오'),'E3':('식당','오후'),'E4':('할머니 방 앞','밤'),'E5':('2층 복도','다음 날 저녁')}
def scene(id_,extra_pre=None):
    s=SC[id_];items=conv(s,'play')
    pre=extra_pre or []
    body=emit(items,'play')
    who=None
    for it in items:
        if it[0]=='dir' and it[1].get('who') not in(None,'none'):who=it[1]['who'];break
    title,sub=SUB[id_]
    after=',"title"' if id_=='P5' else ''
    return '  /* %s %s */\n  SID(%s,B(%s,%s,S(%s,%s,%s,[%s%s\n   %s]%s)))'%(id_,s['title'],js(id_),js(BG[id_]),js(who),js(LOC[id_]),js(title),js(sub),''.join(p+',' for p in pre),'' ,body,after)
PRE={'P1':[],'P3':['D({sfx:"knock",ms:650})','D({sfx:"doorOpen",ms:550})','D({sfx:"door",ms:450})'],'P5':['D({sfx:"steps",ms:450})'],
     'P9':['D({sfx:"doorOpen",ms:500})','D({sfx:"door",ms:350})'],'P2':[],'P13':['D({sfx:"steps",ms:450})'],'P11':['{sfx:"slam"}'],'P4':[],'P6':[],'E2':[]}
pro=[scene('P%d'%i,PRE.get('P%d'%i)) for i in range(1,14) if 'P%d'%i not in SKIP_SCENES]
# P9: 문 소리는 세련 등장 전
end=[scene('E%d'%i) for i in range(1,6)]
head=''' /* ---- 프롤로그 P1~P13 (2026-10-09 장면 대본 JSON에서 생성: gen/conv.py) ----
    I(속마음[,무대,첫진입만]) / L(화자,대사,"",표정) / N(회색 지문: 대체 그림이 없는 사실만) / D({who,sfx,ms,chime}) 글자 없는 연출 */
 function I(t,cue,entry){var x="("+t+")";if(cue)(window.__INNCUE=window.__INNCUE||{})[x]=cue;if(entry)(window.__INNENTRY=window.__INNENTRY||{})[x]=1;return ["narr",x]}
 function B(bg,who,s){s.bg=bg;s.who=who;return s}
 function D(o){return {dir:o}}
 function SID(id,s){s.sid=id;return s}
 window.__INNSID=SID;
 function FL(w,t,f){return f?[w,t,"","","","",f]:[w,t]}
 window.__INNFL=FL;
'''
body=' EP.PRO=[\n'+',\n'.join(pro)+'\n ];\n'
pro_js=head+body.replace('L(','FL(').replace('FL("@','L("@')
open('/home/claude/daae/stage/pro_new.js','w').write(pro_js)
# 후일담·회의 직전
r0=conv(SC['R0'],'play')
end_js=' var FL=window.__INNFL,SID=window.__INNSID;\n /* ---- 후일담 E1~E5 · 회의 직전 R0 (장면 대본 JSON에서 생성) ---- */\n EP.END=[\n'+',\n'.join(end).replace('L(','FL(')+'\n ];\n EP.THE_END={banner:["1장 끝","열세 번째 침대"],notice:{title:"1장 끝 · 열세 번째 침대",text:"다람탐정 1장을 마쳤어요."}};\n'
end_js+=' EP.I9=[{loc:"dining"},\n   '+emit(r0,'play').replace('L(','FL(')+'];\n'
# 조사 대사 덮어쓰기
SPOT={'I01':('bed13','spots','bag'),'I02':('bed13','spots','quilt'),'I03':('bed13','spots','ledger'),'I04':('bed13','obs','o_inn_box'),'I05':('bed13','obs','o_inn_head'),'I06':('bed13','obs','o_inn_head2'),
 'I07':('kitchen','spots','basket'),'I08':('kitchen','spots','fur'),'I09':('hall','spots','clock'),'I10':('dotoroom','spots','diary'),'I11':('front','spots','book')}
ov=[' /* ---- 조사·질문 대사 (장면 대본 JSON에서 생성) ---- */',' function FIND(loc,kind,id){var l=EP.LOCS.filter(function(x){return x.id===loc})[0];return l&&(l[kind]||[]).filter(function(x){return x.id===id})[0]}']
for sid,(loc,kind,id_) in SPOT.items():
    items=conv(SC[sid],'say')
    if sid=='I04':items.append(('dir',{'who':'none','sfx':'steps','ms':380},False))
    if sid=='I06':items.append(('inner','(열한 번째 달 둘째 날. 네 자리 숫자로 옮기면 될까.)',False,''))
    ov.append(' (function(){var x=FIND(%s,%s,%s);if(x)x.say=[%s];})();'%(js(loc),js(kind),js(id_),emit(items,'say').replace('L(','FL(').replace('FL("@','L("@')))
# 자물쇠 열림
ov.append(' EP.LOCK.open=[L("@dir","sfx:lock;ms:500")];')
# 질문: 장면별로 질문 단위 분리
def talk(sid):
    s=SC[sid];groups={};order=[];entry=None
    for l in s['lines']:
        c=l.get('condition') or ''
        if c.startswith('이 장소에 새로') and l['type']=='속마음':entry=l['text'];continue
        if c.startswith('첫 진입 또는'):continue
        g=c[len('질문 선택 '):] if c.startswith('질문 선택') else '_first'
        groups.setdefault(g,[]).append(l)
        if g not in order:order.append(g)
    return entry,order,groups
def tlines(ls):
    sub={'scenes':[]};fake={'lines':ls}
    return emit(conv(fake,'say'),'say').replace('L(','FL(').replace('FL("@','L("@')
TMAP={'I13':('innma',{'_first':'T_ma1','어젯밤 할머니는':'T_ma2','세련에 대해':'T_ma3'}),
      'I14':('seryeon',{'_first':'T_se1','어젯밤 무엇을 했나':'T_se2','이 여관에 와 본 적은 → C12':'C12'}),
      'I15':('nabi',{'_first':'C03','열세 번째 침대에 대해':'T_na2','할머니에 대해':'T_na3'}),
      'I16':('geokkuri',{'_first':'C13'})}
for sid,(who,mp) in TMAP.items():
    entry,order,groups=talk(sid)
    ov.append(' (window.__INNTALKENTRY=window.__INNTALKENTRY||{})[%s]=%s;'%(js(who),js(entry)))
    for g in order:
        tid=mp.get(g)
        if not tid:print('미대응',sid,g);continue
        ls=[l for l in groups[g] if not (l['type']=='연출' and '획득' in l['text'] and l['line_id']!='I16-02g')]
        ov.append(' (function(){var t=EP.TALK[%s].filter(function(x){return x.id===%s})[0];if(t)t.lines=[%s].concat(t.__follow||[]);})();'%(js(who),js(tid),tlines(ls)))
open('/home/claude/daae/stage/gen/end_gen.js','w').write(end_js+'\n'.join(ov)+'\n')
print('ok')
