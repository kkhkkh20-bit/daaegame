"""Build the authored Room 13 narrative data; this is not a game runtime."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEGACY = ROOT.parent / 'game' / 'legacy-resident-roster.json'

# id | public work | protected interest | hidden knowledge | opens with | refusal trigger | change after case
CAST_TEXT = '''
tori|광장 수선과 여관 납품|혼자서도 일을 맡길 수 있다는 신뢰|사건 당일 브로치 수리를 도왔다|수리 쪽지와 남은 부품을 함께 확인하고 공개 범위를 합의|겁이 많으니 틀렸다고 몰아붙임|진범 입증 뒤 할머니 물건을 돌려주지 못하고 보관함에 둔다
bori|장작 운반과 가족 돌봄|자기 집의 난방|중앙 창고로 먼저 돌아간 연료 수량|가족 대피 자리 확보와 수량 원본 대조|공동체를 위해 가족 몫을 포기하라고 강요|둘째 주 제단을 붙잡는 사람 또는 환자를 옮기는 사람으로 갈린다
yeoni|의복 수선과 물자 교환|토리의 안전과 자기 작업실|엄마의 수선 방식과 여관 납품 시점|물건 공개 목적과 원본 보존에 동의|토리 이름을 허락 없이 경비에게 전달|증언 동의 여부에 따라 수선소가 조용한 만남 장소가 된다
nabi|여관 식사와 임시 운영|자신을 거둔 할머니와 아이들의 식사|식당 알리바이의 실제 공백|본 것과 추측을 구분하는 질문 및 남은 식량 대책|할머니를 믿었다는 이유만으로 공범 취급|할머니 구금 뒤 접수대 운영 또는 침묵; 아이에게는 계속 밥을 준다
buri|수리점과 조부의 도구 관리|죽은 조부의 명예|조부의 초기 증상과 보관 사본|병력 비공개 확인과 조부의 잘못도 사실대로 기록할 약속|조부를 괴물이라고 부르거나 공개 조롱|조사에는 협조해도 다람이를 즉시 용서하지 않는다
kongi|가게 심부름과 동네 길 안내|자기 관찰을 비웃지 않는 관계|특정 소리 전후 누가 골목을 지났는지|시각 대신 앞뒤 사건으로 질문|시계를 잘 못 본다는 이유로 무시|경비가 증언을 고치라 하면 입을 닫거나 독립 증인을 찾는다
doto|장부 정리와 광장 배급 보조|기록의 정확성과 일자리|사망 시각이 진료가 아니라 첫 비명에서 옮겨졌음|원본 두 장의 출처 대조|처음부터 장부 위조범으로 몰기|사실 정정 후에도 식량 부족을 이유로 대피 정책에 반대할 수 있다
kkwak|빨래 물 나르기와 하천 길 확인|멀리 있는 가족에게 돌아갈 길|낮은 수로의 눈 쌓임과 위험 구간|현재 길을 함께 확인하는 동행|수영을 잘할 것이라 단정하고 위험 작업을 맡김|검증된 탈출로의 안내를 돕거나 대피소에 남는다
grandma|여관 접수와 옛 돌 운용 자문|자신의 질서와 과거 희생의 정당화|살인 계획·엄마와의 결별·강제 추출|의심받지 않을 정도만 부분적으로 인정|엄마 현재 위치와 살인 입증 자료가 공개됨|의심/구금/자유 상태에 따라 감시와 명령 가능 범위가 실제로 달라진다
librarian|도서관 기록 보존|과거 자료의 독립성|옛 건물 구조와 누락된 회복 기록|반출 대신 현장 대조와 보호할 보관처|원본을 가져가 숨기겠다는 요구|여론에 맞서 기록을 공개하거나 열람만 허용한다
owlgp|은퇴 탐정과 등 점검|과거 오판의 정정과 손자|엄마 연락 일부와 실종 사건의 빈 기록|확인한 사실을 소문과 구별하는 태도|사람을 몰아가기 위해 명성을 이용|기본 경로 4일 사망, 예방 경로 생존 증인; 죽은 뒤 일상 배치 금지
teacher|학교와 비상 대피소|학생들의 안전|가족별 실제 피난 인원|연료와 식사 확보 후 수용 계획|학교만 열면 해결이라고 책임 전가|교실을 대피소로 열거나 정원을 제한한다
karo|마차 수리와 반송품 운반|일의 신뢰와 생계|아빠의 부재 증명·할머니의 전달 요청|반송 원본과 자신의 실제 운행 기록|운반했다는 이유로 살인 공범 단정|호송 거부/탈출 지원/중립으로 나뉜다
nero|외곽 노동과 비공식 통행|등록되지 않은 사람들의 안전|보호시설 외곽 점검 통로|이름을 노출하지 않는 보호 대책|탈출자의 신원 공개|자기 사람을 위해 부녀를 거절할 수 있으나 위험 통로의 사실은 남긴다
seol|종탑과 야간 안내|종이 경고로 기능한다는 신뢰|종은 정상이며 호송 신호가 따로 있다는 사실|종 소리의 용도와 실제 시점을 구별|종을 조작했다고 근거 없이 비난|대피 경고를 울리거나 촌장의 호송 명령을 따른다
ppul|촌장·배급·경비 지휘|마을 생존과 통치 권한|희생이 사망이라는 사실·특혜 배급|증거와 실제 생존 대안 및 집행 협조 이탈|대안 없는 전면 정지 강요|할머니 구금 뒤에도 자기 판단으로 기존 의식을 추진하며 책임진다
tok|시계·등·작은 금속 수리|수리 결과의 신뢰|브로치 새 핀의 이음과 작업 시각|물리적으로 맞는 부품과 수리 기록|금속 조각 하나로 범인을 단정해 달라는 요구|장치 분리 실무에 참여; 첫 사건의 관찰을 과장하지 않는다
bami|처마 거처와 밤길 관찰|강제 검사를 피할 안전한 잠자리|다람이의 침대 아래 위치|안전 확보와 증언 공개 동의|신원을 경비에 노출|안전한 증인/압박받은 침묵/이동한 목격자로 달라진다
sling|우편 접수와 마을 안 배달|배달 책임과 직장|할머니 편지 발송과 미전달 경고|봉투와 접수 원본 대조|남의 봉투를 전부 열라는 요구|외부 보고를 보존하거나 감시 아래 소극적으로 전달한다
momo|박물관 보관과 옛 생활 자료|수집품을 잃지 않는 것|난방 개조 전 돌 장치 도면|보관 책임과 복사 방식 합의|유물을 빼앗거나 팔아넘긴다고 의심|원본 대피/복사 제공/창고 봉쇄 중 선택한다
ttadak|건물 보수와 목재 점검|불법 증축 책임을 피하는 것|13호 벽 뒤 길이와 서비스 계단|옛 도면과 실제 치수로 작업 범위 확인|은신처를 만들었다고 살인 공범 몰기|건물 조사 또는 대피소 보강 지원; 숨겨진 출입 사실만 인정 가능
piko|그림과 가족 초상 작업|자기 이름과 직업|초기 증상에서 돌아온 직접 경험|조용한 자리와 반복 관찰 동의|환자로 전시하거나 완치 증거라 단정|회복 증인/후유증 환자; 상태에 따라 대사와 장소 변경
mungchi|수집상 집 심부름|백 부인의 인정과 친구 관계|창고에 보관한 담요 수량|자기 책임을 공개 망신 없이 분리|훔쳐오라고 시킴|몰래 도움보다 공개 배분 기록에 이름을 올리는 변화 가능
madam|비축품과 사유 창고 관리|재산과 가족 안전|배급의 특혜와 남은 비축품|반환/공동 보관 기록과 대피 계획|근거 없는 약탈 선동|계산적인 조건으로 대피 지원; 폭로됐다고 모두 내놓지 않는다
siluk|짐 운반과 마구간|고용과 과거 빚|세탁실/창고 이동의 실제 순서|자기 가족의 추궁 범위 제한과 독립 기록|고용주 앞에서 신원 공개|운반 기록 공개/침묵; 첫 범행을 몰랐다면 공범으로 바꾸지 않는다
wanggu|광장 질서와 행사 준비|주민들에게 유능해 보이는 것|제단 동원 대상과 인원 변경|명령서와 실제 사람 수 대조|공개적으로 허풍만 비웃음|촌장 동원에 협조하거나 피난 안내자로 전환
musoe|폐광 통로와 손녀 돌봄|솜이의 생존|옛 관리 계단과 저부하 수동 운용|솜이에게 위험 일을 맡기지 않는 조사 계획|손녀를 미끼로 이용|수동 운용/안전 통로 지원; 나이가 많다고 모든 고대 진실을 알지 않는다
somi|지붕 길 심부름|자기 판단을 존중받는 것|관측점 사이의 안전한 길|무쇠와 합의한 지상 지원|혼자 시설 잠입을 요구|연락을 돕되 아이가 위험 임무를 해야만 진엔딩인 구조 금지
seori|외부 관리국 검사와 사실 확인|기록의 정합성과 직무|자기 이전 검사에서도 경고가 누락됐음|원본/독립 관측/자기 책임 인정의 조건|기록만 믿으니 공범이라고 몰기|재판 진행·독립 증언 확인·추출 중단 명령; 관측 없이 정답 선언하지 않는다
ubak|검사원 보조와 계측|스승의 인정과 기술 신뢰|부하별 수치와 장치 변경 흔적|자기 측정을 다시 확인할 기회|서리 앞에서 자료를 조롱|독립 측정자로 성장하거나 숫자를 전달만 한다
nubi|세탁 협업과 임시 숙박 연결|가족의 난방과 보복 회피|수습 물품 이동·시설 세탁 동선|가족 대피/공개 동의/현행 교대 확인|경고 뒤 이름 공개|공개 증인/구출 조력자/압박된 주민; 같은 자료라도 상태에 따라 반응
eunho|도시 물품·보석 거래|투자 회수와 도시 평판|반출된 개조 부품과 비축 연료|거래 기록과 반환 보증|근거 없는 도둑 취급|유상 지원도 유효; 다음 편 거래 자료의 연결점
guseul|거래품 정리와 견습|은호에게 해고되지 않는 것|상자에 찍힌 제작/반출 표식|발언을 자기 추측과 구별하고 보호|상사의 거래 비밀 전부 공개 요구|현물 확인 보조; 어린 증언자에게 모든 책임을 맡기지 않는다
badook|야간 순찰과 대피 경호|동료와 맡은 주민의 안전|시설 주변 이동과 교대|현재 명령 모순·안전한 인계처|그냥 규칙을 어기라고 강요|호송 협조/합법 중지/구출 경호로 변화
lamplighter|등불 점검과 비밀 식량 전달|엄마를 돕는 약속과 자기 어머니에 대한 감정|엄마 연락망·할머니의 돌 관리 관행|가족 확인·추적 대응·신원 비공개|은신처 좌표 즉시 공개 강요|어머니의 범죄 입증에 협조하거나 가족만 돕는다; 살인 피해자로 바꾸지 않는다
'''.strip()

PLACES = {
 'gate':'눈에 막힌 입구','square':'돌이 있는 광장','post':'우체국 입구/접수실',
 'inn':'여관 접수대/식당','room13':'13호실','passage':'은신처/서비스 통로',
 'workshop':'수리점','library':'도서관','clinic':'진료소','school':'학교 대피소',
 'store':'공동 창고/세탁실','greenhouse':'폐온실','facility':'북쪽 보호시설',
 'altar':'중앙 제단','lowroad':'낮은 고갯길','home':'주민의 집', 'tower':'종탑',
}

# Each triple is morning/afternoon/evening; comma-separated seven weekdays.
WEEK_PATTERNS = {
 'tori':'square square home,square inn home,home square home,workshop inn home,square home home,square inn home,home square inn',
 'bori':'gate workshop square,gate store home,gate workshop home,store workshop square,gate store home,store school home,home square home',
 'yeoni':'home square home,square square home,home inn home,workshop square home,home square home,square inn home,home school home',
 'nabi':'inn inn inn', 'buri':'workshop workshop home', 'kongi':'square post home',
 'doto':'square post home', 'kkwak':'store lowroad home', 'grandma':'inn inn inn',
 'librarian':'library library home', 'owlgp':'square library inn', 'teacher':'school school home',
 'karo':'gate post inn,gate post gate,gate workshop inn,gate post gate,gate post inn,gate store inn,inn gate inn',
 'nero':'lowroad store home','seol':'tower tower home','ppul':'square post home',
 'tok':'workshop workshop square,workshop workshop home,workshop post home,workshop inn home,workshop clinic home,post workshop home,square workshop home',
 'bami':'inn home inn','sling':'post square post','momo':'library library home',
 'ttadak':'workshop inn home','piko':'square square home','mungchi':'home store home',
 'madam':'home store inn','siluk':'gate store home','wanggu':'square school home',
 'musoe':'workshop home home','somi':'home square home','seori':'post clinic inn',
 'ubak':'workshop clinic inn','nubi':'inn workshop store','eunho':'post store inn',
 'guseul':'store post inn','badook':'gate home square','lamplighter':'square gate workshop,square greenhouse workshop,square gate greenhouse,square library workshop,square gate greenhouse,square workshop home,square gate home',
}

OVERRIDES = [
 {'id':'OV_CASE_DEATH','when':{'all':['victim_dead']},'actors':['owlgp'],'location':None,'behavior':'사망 후 부재. 대화와 회의 출석 없음.','priority':100},
 {'id':'OV_GRANNY_HELD','when':{'all':['granny_detained']},'actors':['grandma'],'location':'facility','behavior':'감시 아래 면회. 명령권과 자유 이동 없음.','priority':95},
 {'id':'OV_DARAM_HELD','when':{'all':['daram_held']},'actors':['daram'],'location':'facility','behavior':'면회와 관찰만 가능. 부녀 동행 화면에서 제외.','priority':100},
 {'id':'OV_NUBI_PRESSURED','when':{'all':['nubi_identity_exposed'],'not':['nubi_protected']},'actors':['nubi'],'location':'home','behavior':'다음 시간대부터 대화 거부/경비 방문. 보호/대체 조사 경로 유지.','priority':70},
 {'id':'OV_BAMI_PRESSURED','when':{'all':['bami_identity_exposed'],'not':['bami_protected']},'actors':['bami'],'location':'home','behavior':'처마에서 이동. 신원 보호 전 공개 증언 거부.','priority':70},
 {'id':'OV_DISASTER','when':{'all':['disaster_started']},'actors':['teacher','nabi','bori','wanggu'],'location':'school','behavior':'평소 일 대신 식사·대피·운반. 자원 준비에 따라 협조.','priority':60},
 {'id':'OV_MEASURE','when':{'all':['measurement_active']},'actors':['mom','buri','seori','ubak'],'location':'workshop','behavior':'관측 중. 동시에 원래 위치에서 만나지 않음.','priority':75},
 {'id':'OV_FINALE','when':{'all':['finale_active'],'not':['granny_detained']},'actors':['grandma','ppul','seori','neoul'],'location':'altar','behavior':'제단 대결의 실제 역할.','priority':80},
]

DAYS = [
 (1,'도착','등록 정정·숙소 확보','엄마에게 접근할 출발점','S01 S02 S03 S04 S05'),
 (2,'엄마가 남긴 자리','물건·미전달 편지 확인','실제 연락 시도가 있었나','S06 S07'),
 (3,'말이 전해지는 마을','증언 보호·회복 사례·경고 편지','누구에게 어디까지 말할까','S08 S09 S10'),
 (4,'열세 번째 방','기본 사건 또는 예방','딸이 왜 자신이 죽였다고 믿나','S11 S12 S13 S14 S43'),
 (5,'딸의 기억','현장 보존·면회·은신처','방어와 죽음은 같은 순간인가','S15 S16 S17'),
 (6,'알리바이의 빈 시간','목격 범위·새 핀·위험 공개','할머니가 보이지 않던 구간','S18 S19 S20'),
 (7,'첫 재판','석방/진범 입증/구금/예방 대면','딸의 죄를 입증했다고 할 수 있나','S21 S22 S23 S24 S25'),
 (8,'같은 골목, 다른 마을','독립 재난·생활 변화','딸의 위치와 마을 상황','S26 S27'),
 (9,'첫 연락','초롱·현재 표식·추적 대응','엄마에게 가는 길이 누구에게 알려졌나','S28 S29'),
 (10,'엄마를 만난다는 것','재회 또는 흔적 추적','왜 나타나지 못했나','S30 S31'),
 (11,'누구를 옮길 것인가','구출·대피소·연료','내 가족과 다른 가족의 생존','S32 S33'),
 (12,'돌을 끄면','독립 관측·희생 기록','희생은 무엇을 바꾸었나','S34'),
 (13,'기다렸던 저녁','두 번째 관측·이송 대응','오늘 밤 대안을 실행할 수 있나','S35 S36'),
 (14,'재판장이 없는 결전','호송 중지·제단 대결·결말','공동체의 행동을 바꿀 수 있나','S37 S38 S39 S40 S41 S42'),
]

EVIDENCE_TEXT = '''
E01|할머니의 초대 편지|물증|가족이 마을에 온 이유|편지만으로 살인 계획은 증명되지 않는다|S01 S04
E02|등록 정정 원본|물증|부녀의 합법적인 동행 등록|살인 누명과는 별도|S02
E03|엄마의 바느질 흔적|물증|옛 은신처 이용 가능성|현재 위치/당일 출입 아님|S06 S07 S17
E04|옛 도면과 외벽 치수|기록|13호 뒤 공간의 가능성|현재 개방된 통로인지는 미확인|S09 S17
E05|현재 통로 조사|관찰기록|정문 외의 이동 경로와 소요 시간|이용자의 신원 아님|S17
E06|다람이의 초기 면회 기록|증언|방어·숨음·두 소리의 순서|목격하지 않은 범인의 신원 아님|S15
E07|분리된 촛대|물증|낙하 뒤 다시 사용된 윗부분|사용자와 정확한 시각은 별도|S14
E08|최초 부상 기록|기록|팔의 방어 흔적과 머리 치명상 구분|분 단위 사망 시각 추정 불가|S14 S16
E09|보존된 촛농 진입 흔적|물증|첫 낙하 이후 제삼자의 접근|신발 하나로 개인 확정 불가|S14 S17
E10|밤이의 관찰|증언|두 번째 소리 동안 딸이 숨었던 위치|범인의 얼굴은 보지 못함|S18
E11|복도에서 들은 순서|증언|비명 뒤 생존 발언과 나중 충격|정문 외 출입은 못 봄|S19 S23
E12|식당의 실제 목격 구간|증언|할머니의 참인 첫 비명 알리바이와 공백|공백만으로 살인 확정 불가|S19
E13|새 핀의 수리 쪽지와 부품|물증|당일 교체와 물리적 맞물림|접촉 시점은 다른 자료 필요|S12
E14|피해자 손의 핀 조각|물증|수습 전부터 남은 접촉 흔적|단독으로 행위 목적 판단 불가|S14
E15|식당에서 여민 브로치|증언|첫 비명 후에도 새 핀이 붙어 있었음|목격자의 실제 확인 범위 준수|S12 S19
E16|별도 구금 전달 초안|기록|가족을 통제하려던 사전 계획|살인 현장의 증거 대신 쓰지 않음|S20 S24
E17|피해자의 보관 사본|기록|엄마 접촉과 누락된 실종 조사|현재 엄마 위치의 자동 정답 아님|S16
E18|미전달 경고 봉투|물증|엄마가 첫 주에도 가족에게 경고했다|전달되지 않은 이유 확인 필요|S07 S08
E19|초롱의 현재 답장|물증|엄마의 현재 접촉 의사|주소 공개 시 추적 가능|S28 S29
E20|초기 증상과 회복 관찰|관찰기록|일부 환자는 돌아올 수 있다|모든 환자 완치 아님|S10
E21|과거 발병·출력 원본|기록|엄마 도착 전에도 과부하 뒤 악화|한 번의 상관만으로 원리 확정 불가|S31
E22|추출 시설 원본 기록|기록|희생이 사망이며 출력은 일시 상승|지속 효과는 전후 구간 필요|S31 S39
E23|회로 분리 관측 1|관찰기록|안전한 작은 구간의 반응|단 한 번의 결과|S34
E24|회로 분리 관측 2|관찰기록|다른 부하에서 재현된 반응|확인 범위 밖 완전 복구 약속 금지|S36
E25|실제 대피소 인계 기록|기록|장소와 수용 인원이 준비됨|식량/연료는 따로 필요|S32
E26|연료·식량 인수 기록|기록|실물 자원이 확보됨|계획뿐이면 획득 처리 금지|S32
E27|현행 호송 명령|기록|누가 언제 어디로 옮겨지는가|이전 회차 명령으로 대체 불가|S27 S33
E28|현재 교대 관찰|관찰기록|구출 가능한 현행 경로|경계 상태 변하면 재확인|S33
E29|확인한 낮은 통로|관찰기록|기상 창에 사용할 귀로|눈보라 때 무조건 통과 불가|S36 S46
E30|엄마의 연구 원본|기록|장치 원리와 추출의 문제|엄마 말만으로 주민 동의 없음|S31
E31|회복 기록의 삭제 전 사본|기록|할머니가 알고도 일부 환자를 되돌릴 수 없다고 분류|직접 살인 입증과 별개|S31 S38
E32|외부 반출 개조 도면|기록|다른 지역의 같은 개조 가능성|새 상위 흑막의 존재를 단정하지 않음|S49
E33|최초 현장 출입 봉인 기록|기록|물증 보관 전후의 접근자 제한|실제 보존 실패 경로에는 강한 형태로 생성 금지|S14
E34|아빠의 반송품 동행 기록|증언|사건 때 아빠가 별채 밖에 있었음|딸이 무죄라는 직접 증거 아님|S11 S14
'''.strip()

ACTIONS = [
 ('A01','입구 원본과 공고 조사',1,1,'gate',0,[],['E02'],'S02'),
 ('A02','엄마 물건과 여관 방 조사',1,14,'inn',0,[],['E03'],'S06'),
 ('A03','수선물을 함께 대조',2,6,'square',0,['E03'],['sewing_confirmed'],'S07'),
 ('A04','피코가 회복할 때까지 동행',3,3,'square',1,[],['E20'],'S10'),
 ('A05','경고 표식과 봉투 확인',3,4,'square',0,['contact_sign_known'],['E18'],'S08'),
 ('A06','피해자의 안전한 대면 준비',3,4,'inn',1,['E18','E05'],['victim_protected'],'S43'),
 ('A07','사건 현장 최초 보존 요청',4,4,'room13',0,[],['E07','E08','E14','E33'],'S14'),
 ('A08','다람이 면회',5,13,'facility',1,['daram_held'],['E06'],'S15'),
 ('A09','현재 서비스 통로 조사',2,13,'passage',1,['E04'],['E05'],'S17'),
 ('A10','부리의 보관 사본 확인',5,13,'workshop',1,['private_medical_consent'],['E17'],'S16'),
 ('A11','밤이 관찰과 공개 범위 확인',5,7,'inn',0,['bami_encountered'],['E10'],'S18'),
 ('A12','식당과 복도의 목격 범위 질문',5,7,'inn',0,[],['E11','E12','E15'],'S19'),
 ('A13','수리 쪽지와 핀 대조',4,7,'workshop',0,[],['E13'],'S12'),
 ('A14','봉인된 바닥 흔적 대조',5,7,'room13',1,['E33'],['E09'],'S17'),
 ('A15','증인의 안전한 거처 마련',5,13,'school',1,['shelter_offer'],['witness_protected'],'S18'),
 ('A16','초롱에게 답장 맡기기',3,12,'workshop',1,['family_verified'],['contact_pending'],'S28'),
 ('A17','현행 접촉 표식 확인',4,13,'greenhouse',1,['contact_pending'],['E19'],'S29'),
 ('A18','추적을 확인하고 접촉 장소 변경',4,13,'lowroad',1,['mother_exposed'],['mother_relocated'],'S29'),
 ('A19','엄마와 안전하게 합류',4,14,'greenhouse',1,['E19','contact_safe'],['mom_reunited','E30'],'S30'),
 ('A20','원본 발병·추출 기록 대조',8,13,'library',1,['E17'],['E21','E22','E31'],'S31'),
 ('A21','대피소와 교대 인원 마련',8,13,'school',1,[],['E25','shelter_ready'],'S32'),
 ('A22','제분·연료 공동 작업',8,13,'workshop',1,['labor_agreement'],['E26','supplies_ready'],'S32'),
 ('A23','현행 호송·교대 조사',8,13,'facility',1,['daram_held'],['E27','E28'],'S27'),
 ('A24','명령 중지 또는 운반로 구출',10,13,'facility',1,['E27','rescue_support'],['daram_rescued'],'S33'),
 ('A25','작은 회로의 첫 안전 관측',10,12,'workshop',1,['E30','operators_ready'],['E23'],'S34'),
 ('A26','다른 부하에서 두 번째 관측',11,13,'workshop',1,['E23'],['E24'],'S36'),
 ('A27','현재 낮은 통로와 날씨 확인',8,13,'lowroad',1,['route_hint'],['E29'],'S36'),
 ('A28','자료 제시 미리보기·확정',1,14,'any',0,[],[],'S50'),
 ('A29','보호자 자격으로 구금 전달 원본 확인',5,7,'post',1,['E02'],['E16'],'S24'),
 ('A30','옛 보수 도면과 외벽을 대조',2,13,'library',0,[],['E04'],'S17'),
 ('A31','등 수리함의 연락 표식 관찰',2,12,'square',0,[],['contact_sign_known'],'S28'),
 ('A32','피해자 가족과 병력 열람 범위 합의',5,13,'workshop',0,['E06'],['private_medical_consent'],'S16'),
 ('A33','외곽 약속을 미루고 아빠가 대면에 동행',4,4,'inn',1,[],['victim_protected','case_prevented','outside_appointment_missed'],'S43'),
]

CLAIMS = [
 {'id':'C1','scene':'S22','assertion':'정문이 잠겨 다람이만 범행 가능','support_sets':[['E04','E05']], 'alternative':'현재 통로 실측과 초롱/따닥의 독립 확인도 허용','result':'exclusive_access_refuted','counter':'엄마의 옛 물건을 당일 출입으로 오인'},
 {'id':'C2','scene':'S23','assertion':'첫 방어가 사망 원인','support_sets':[['E06','E07','E08','E10','E11'],['E07','E08','E09','E11','E33']], 'alternative':'피해자 생존 경로는 당사자 진술과 실제 부상으로 별도 처리','result':'daram_cleared','counter':'첫 부상으로 뒤늦게 죽었다는 주장'},
 {'id':'C3','scene':'S24','assertion':'할머니는 살해 시각 식당에 있었다','support_sets':[['E05','E11','E12']], 'alternative':'소리의 상대 순서와 이동 시간으로도 충분, 초 단위 시계 정답 금지','result':'granny_alibi_limited','counter':'가능했어도 실제 출입 증거가 없다는 주장'},
 {'id':'C4','scene':'S24','assertion':'출입했어도 구조했을 뿐','support_sets':[['E13','E14','E15','E33','E09','E16','E17'],['E13','E14','E15','E33','E10','E11','E16','E17']], 'alternative':'범행 예방 경로는 관찰된 침입/위협과 사전 계획을 별도로 입증','result':'granny_culprit_proven','counter':'오후의 선의 접촉/수습 접촉이라는 해명'},
 {'id':'F1','scene':'S38','assertion':'야생화한 주민은 누구도 돌아오지 못함','support_sets':[['E20','E31']], 'alternative':'독립적인 회복 관찰 2개와 본인/가족의 확인','result':'patients_protected','counter':'한 사람의 일시 반응일 뿐'},
 {'id':'F2','scene':'S39','assertion':'희생은 지속 가능한 해결이며 엄마가 고장냈음','support_sets':[['E21','E22','E23','E24','E30']], 'alternative':'원리와 한계, 엄마 이전 고장 시점, 재현 관측을 각각 입증','result':'extraction_refuted','counter':'추출 직후 실제 출력이 올랐다는 사실'},
 {'id':'F3','scene':'S40','assertion':'오늘 밤 희생 없이 살 방법이 없음','support_sets':[['E25','E26']], 'alternative':'기록만 아니라 실제 shelter/supplies/operators/patient_transport 상태 필요','result':'survival_alternative_ready','counter':'방이 있어도 식량과 교대 인원이 없다는 반론'},
 {'id':'F4','scene':'S41','assertion':'가족이 질서를 깨뜨려 위기를 만들었음','support_sets':[['E01','E16','E17','E18']], 'alternative':'이미 확정한 살인/미수 판결은 재증명하지 않고 인용','result':'granny_control_exposed','counter':'보호를 위한 조치였다는 해명'},
]

PRESENTATIONS = [
 {'id':'P_BURI','recipient':'buri','items':['E06','E08'],'requires':['private_medical_consent'],'topic':'조부가 남긴 일','reward_after_topic':['E17'],'risk':'공개 병력 비난은 거절. 원본을 압수하지 않음'},
 {'id':'P_NABI','recipient':'nabi','items':['E11'],'requires':[],'topic':'물을 가지러 간 동안','reward_after_topic':['E12'],'risk':'할머니를 믿었다는 이유로 공범 몰이 시 공개 증언 거절'},
 {'id':'P_TOK','recipient':'tok','items':['E14'],'requires':[],'topic':'새 핀과 오래된 핀','reward_after_topic':['E13'],'risk':'단독 범인 확정을 요구하면 한계를 지적'},
 {'id':'P_BAMI','recipient':'bami','items':['E06'],'requires':[],'topic':'두 번째 소리 때 보인 것','reward_after_topic':['E10'],'risk':'이름 공개는 별도 확인. 공개 동의와 관찰 획득은 별개'},
 {'id':'P_CHORONG','recipient':'lamplighter','items':['E01','E03'],'requires':['family_verified'],'topic':'가족에게 보낼 답장','reward_after_topic':['contact_pending'],'risk':'연락 장소를 공개하면 다음 시점에 추적 발생'},
 {'id':'P_GRANNY','recipient':'grandma','items':['E09','E10','E13'],'requires':[],'topic':'그날의 수습','reward_after_topic':[],'risk':'공개한 항목만 대비. 확보 물증 소급 삭제 금지'},
 {'id':'P_NUBI','recipient':'nubi','items':['E27'],'requires':['nubi_protected'],'topic':'현행 세탁 반입','reward_after_topic':['rescue_support'],'risk':'가족 난방 대책 없이 공개 반입 요구하면 거절'},
 {'id':'P_SEORI','recipient':'seori','items':['E21','E22'],'requires':[],'topic':'삭제 전 검사 기록','reward_after_topic':['E31'],'risk':'자기 이전 검사 책임도 묻게 되므로 방어적 반응'},
 {'id':'P_EUNHO','recipient':'eunho','items':['E26'],'requires':['restitution_agreed'],'topic':'공동 연료 인수','reward_after_topic':['supplies_ready'],'risk':'지원은 거래일 수 있으며 호감도 보상으로 대체하지 않음'},
]

ENDINGS = [
 {'id':'E0','title':'닫힌 문','scene':'S44','when':{'all':['safe_route','daram_with_dad','choose_leave_early'],'not':['mom_reunited']},'knowledge':'도달하지 못한 연락 시점과 편지 소인'},
 {'id':'E1','title':'남겨진 이름','scene':'S45','when':{'all':['daram_held','last_intervention_lost']},'knowledge':'마지막 호송 경로와 개입 지점'},
 {'id':'E2','title':'세 사람의 겨울','scene':'S46','when':{'all':['family_reunited','safe_route','pursuit_managed','choose_family_escape']},'knowledge':'마을에 남은 희생 구조'},
 {'id':'E3','title':'불은 돌아왔다','scene':'S47','when':{'all':['finale_resolved'],'not':['extraction_stopped']},'knowledge':'일시 출력 상승 뒤 다시 고장나는 시점'},
 {'id':'E4','title':'이름을 되찾은 마을','scene':'S48','when':{'all':['extraction_stopped','abuse_exposed'],'not':['survival_ready']},'knowledge':'부족했던 대피·식량·열원'},
 {'id':'E5','title':'우리 몫의 봄','scene':'S42','when':{'all':['family_reunited','extraction_stopped','survival_ready']},'knowledge':'공동체가 생존한 실제 조합'},
 {'id':'E6','title':'열세 번째 창','scene':'S49','when':{'all':['family_reunited','extraction_stopped','survival_ready','granny_control_exposed','mother_original_safe','witness_protected','two_observations_complete'],'any':['granny_culprit_proven','premeditation_prevented_proven']},'knowledge':'고대 장치의 원래 목적과 외부 개조 도면'},
]

def make_data():
    original = json.loads(LEGACY.read_text())
    originals = {r['original_id']:r['original_spec'] for r in original['entries']}
    cast=[]
    for line in CAST_TEXT.splitlines():
        ident,work,interest,truth,opens,refuses,changes=line.split('|')
        source=originals[ident]
        pattern=WEEK_PATTERNS[ident].split(',')
        if len(pattern)==1:pattern*=7
        runtime = {'grandma':'granny','karo':'karo','nabi':'nabi','buri':'buri','doto':'doto','bami':'bami'}.get(ident,'resident_'+ident)
        cast.append(dict(id=ident,name=source['name'],species=source.get('animal'),runtime_id=runtime,
                         work=work,protects=interest,private_knowledge=truth,opens_with=opens,
                         refuses_when=refuses,post_case_change=changes,
                         weekly_locations=[x.split() for x in pattern],source='legacy-resident-roster.json',
                         legacy_incidents_imported=False))
    evidence=[]
    for row in EVIDENCE_TEXT.splitlines():
        ident,name,kind,fact,limit,scenes=row.split('|')
        evidence.append(dict(id=ident,name=name,kind=kind,establishes=fact,does_not_establish=limit,
                             scenes=scenes.split(),current_run_only=True,retained_on_show=True))
    actions=[dict(id=i,title=t,start_day=s,end_day=e,place=p,time_cost=c,requires=r,
                  grants_after_completion=g,scene=sc,discovery_not_auto=True)
             for i,t,s,e,p,c,r,g,sc in ACTIONS]
    return dict(schema='room13.authoring.v1',status='authored_not_connected_to_runtime',
      date='2026-10-12',title='다람탐정: 눈 아래의 열세 번째 방',
      canonical_scope='본편 인과·주요 대사·분기와 구현용 집필 데이터. 완성 실행본 아님.',
      cast=cast,additional_roles=[{'id':'dad','name':'아빠'},{'id':'daram','name':'다람'},
        {'id':'mom','name':'엄마'},{'id':'neoul','name':'너울'},{'id':'seryeon','name':'세련'},{'id':'guard','name':'돌목'}],
      places=PLACES,day_flow=[dict(day=d,weekday='월화수목금토일'[(d-1)%7],title=t,objective=o,
                                  question=q,scenes=sc.split()) for d,t,o,q,sc in DAYS],
      evidence=evidence,actions=actions,claims=CLAIMS,presentations=PRESENTATIONS,
      schedule_overrides=OVERRIDES,endings=ENDINGS,
      ending_resolution={'explicit_early_choice_first':True,'final_priority':['E6','E5','E4','E3'],
                        'E1_only_when_last_rescue_opportunity_is_actually_lost':True,
                        'never_require_playthrough_count':True},
      fact_sources={
        'family_verified':'S28에서 E01/E03과 부녀의 현재 신원을 확인하는 대화 완료',
        'contact_safe':'추적 없음 확인 또는 A18 이후 새 장소의 신호 확인',
        'shelter_offer':'학교/누비에게 실제 빈 자리와 보호 범위를 확인하는 관계 대화',
        'bami_encountered':'마을 탐색에서 밤이와 직접 대면. 소문만으로 자동 등록하지 않음',
        'labor_agreement':'S32에서 운용할 주민의 동의와 가족 교대 대책 합의',
        'operators_ready':'부리/톡/무쇠 중 실무자와 독립 기록자 서리/우박의 동의',
        'rescue_support':'S33의 경로별 인계처와 실행자 확보. P_NUBI만이 유일 경로 아님',
        'route_hint':'까로/꽥순/무쇠의 거친 길 안내. 실제 E29 확인과 구분',
        'restitution_agreed':'S32에서 공동 인수/반환 기록에 합의',
        'premeditation_prevented_proven':'S43 실제 범행 예방 및 현재 회차 침입/계획 근거의 공개 확인',
        'survival_ready':'실제 대피 장소+식량/연료+수동 운용 인원+환자 이송 경로 모두 준비',
        'two_observations_complete':'E23과 E24가 서로 다른 부하/시간대에 실제 활동으로 확보됨'},
      state_rules={'presentation_max_items':2,'support_sets_mean':'전체 논증 자료. 작은 논점을 순서와 무관하게 입증 후 연결.',
        'time_periods':['오전','오후','저녁'],'questions_spend_time':False,'showing_spends_time':False,
        'skip_preserves_time_and_effects':True,'replay_is_diegetic_time_travel':False,
        'no_initial_end_date_countdown':True,'prior_run_evidence_submittable':False,
        'victim_preventable':True,'granny_custody_persists':True},
      baseline_schedule_note='주간 기본 위치. 상태별 우선 규칙과 CASE13_TRUTH의 4일 사건 세부 동선이 우선. 플레이어에게 미래 정답표를 노출하지 않음.',
      asset_dependencies=['13호 실제 공간 배치','침대 아래 시야','은신처/계단/창고 연결','촛대 파단 전후','브로치 새 핀','엄마/초롱 얼굴','구금/재난 상태 배경'],
      gameplay_tests='not_run_at_user_request',runtime_changed=False)

if __name__=='__main__':
    data=make_data()
    (ROOT/'narrative.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('집필 데이터 생성:',len(data['cast']),'명 원작 주민,',len(data['evidence']),'개 자료,',len(data['actions']),'개 활동')
