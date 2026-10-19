"""Episode 2 C / Episode 3 A plugin. Execute after recommended_model.py.
All transitions are pure. Geometry is a proposal, not verified production art.
"""
import copy
r13_rec_e3_source_geometry_verified = True
r13_rec_e3_native_geometry_verified = False
r13_rec_e3_geometry_art_verified = r13_rec_e3_source_geometry_verified and r13_rec_e3_native_geometry_verified
def r13_rec_e3_geometry_ready(s):
    isolated = s.get("qa_fixture") == "native_geometry_probe_v1" and s.get("qa_native_gates",{}).get("e3",False)
    return bool(r13_rec_e3_geometry_art_verified or (r13_rec_e3_source_geometry_verified and isolated))

r13_rec_e3_geometry = dict(L=(0,0), M=(5,0), W=(10,0), child=(0,1), teacher=(6,3), child_range=(0,6), teacher_range=(4,10), overlap=(4,6), unobserved_crossings_during_interval=0)

r13_rec_cards.update({
'e2_card_rail': ('수레 난간 · 소매가 닿은 자리', '5일 입구에서 아빠와 다람이 직접 확인. 4일 돌목의 소매가 걸렸다는 자리와 난간 바깥쪽에서 확인한 손 위치를 대조했다. 난간 안으로 팔을 뻗은 자세와 맞는다. 천만으로 물림·선후·정당성을 확정하지 않는다. 사람을 묶거나 물림을 재현하지 않았다.'),
'e2_card_ties': ('담요와 두 짧은 고정끈', '5일 입구 현물. 담요 전체를 두르는 끈이 아니라 난간 양쪽의 짧은 두 고리다. 손이 실제 묶였는지와 언제인지는 목격과 함께 판단해야 한다.'),
'e2_card_somi': ('솜이 · 돌아오기로 한 약속', '5일 입구에서 직접 대화. 솜이는 4일 담요의 주인과 귀가 약속을 안다. 결박이나 물림 순간은 보지 못했다. 보호받는 주민의 이름과 거처는 공개하지 않기로 했다.'),
'e2_card_bami': ('밤이 · 풀어 달라는 요구', '5일 입구에서 4일 자신의 경험을 설명. 수레 안 사람의 손을 풀라고 했고, 그 사람이 끌려갈까 봐 이름을 말하지 말아 달라고 요청했다. 물림 여부는 이름 비공개와 보호 범위를 먼저 정한 뒤 별도로 답한다.'),
'e2_card_badook': ('바둑이 · 비명보다 먼저 본 손', '5일 입구에서 들은 4일 직접 관찰. 수레 담당 바둑이는 난간 양쪽에 손이 묶인 것을 보았고 밤이의 “손을 풀어 줘”도 들었다. 경비를 부르러 돌아선 뒤 비명을 들었다. 물림 접촉 순간은 보지 못했다.'),
'e2_card_dolmok': ('돌목 · 보고와 실제 행위', '4일 입구에서 자신의 팔을 물렸으며 길에서 갑자기 공격받았다고 보고. 당사자의 주장이지 확정 사실은 아니다. 수레 주변에서 실제 한 행동은 별도 질문으로 검사한다.'),
'e3_card_handoff': ('선생님 · 네 아이의 실제 인계', '5일 해지기 전 학교에서 아빠와 다람이 직접 확인. 꼬미·깜이·몽이·방울이 이불 자리로 옮겼고 교사가 네 명을 맞았다. 난로·저녁·야간 돌봄을 확인했다. 출석 이름만 적은 약속과 다르다.'),
'e3_card_wall': ('사람이 지나는 뜯긴 벽', '6일 안전 확인 뒤 창고 바깥에서 직접 관찰. 문과 떨어진 벽의 판자가 사람을 통과시킬 폭으로 뜯겼다. 상처 모양만으로 구조 의도나 방화자를 정하지 않는다.'),
'e3_card_layout': ('문·등잔·벽의 배치', '6일 창고 바깥에서 확인. 등잔은 안쪽에 넘어지지 않은 상태로 남았고 통은 문밖 W에 있다. 문·벽의 상대 위치는 보이지만 그을음만으로 발화 원인을 과학적으로 확정하지 않는다.'),
'e3_card_can': ('W에 남은 통과 맞는 주둥이 조각', '6일 창고 문앞 W에서 아빠와 다람이 직접 대조. 통과 바로 옆 조각의 단면이 맞는다. 통은 빨래터로 돌아간 것이 아니다. 같은 물건이라는 대조일 뿐 사용자를 특정하지 않는다.'),
'e3_card_bori': ('보리 · 불 뒤 반대편에서 도착', '6일 창고 바깥에서 들은 5일 밤 자신의 경험. 반대편 길에서 문불을 보고 와서 벽을 뜯었다. 학교 사전 인계 여부는 당시 몰랐다. 구조한 사람이 있었다는지는 실제 인계 결과에 따라 다르며 화상으로 무죄를 판단하지 않는다.'),
'e3_card_teacher': ('선생님 · M–W 한 차례 왕복', '6일 학교에서 들은 5일 밤 창문 관찰. 밤에 창문에서 통을 든 사람의 움직임을 보았으나 거리와 비스듬한 시야 때문에 누군지 자신 있게 알아보지는 못했다. 그 사람이 M→W로 가 통을 내려놓고 문앞에 점화하고, 빈손으로 W→M으로 돌아갈 때까지 짧게 봤다. 돌아올 때도 불빛을 등지고 있어 얼굴을 자신 있게 알아보지 못했다. 점화를 보자마자 창에서 경보를 외쳤고 그 구간에 교차·인계는 없었다. 보리는 점화 뒤 반대편에서 왔다. L은 못 봤으며 이후 구조 협조로 이동했다.'),
'e3_card_nubi': ('누비 · 통 소유와 대여 주장', '6일 빨래터 직접 대화. 누비는 W에서 발견한 통을 자기 생활용 통이라고 확인하며 보리에게 빌려줬다고 주장한다. 소유 확인은 착화 자백이 아니다. 회의에서 주장할 전달 지점을 기존 관찰로 검사해야 한다.'),
'e3_card_child': ('누비의 큰아이 · L–M 출발과 빈손 귀환', '6일 학교 보호자 동석 비공개 면담에서 들은 5일 밤 직접 관찰. L에서 엄마 얼굴과 통을 보았고 L→M 이동을 계속 봤다. 그 짧은 왕복 동안 다른 통행·인계 없이 기다렸다. 불빛 뒤 M→L 귀환을 계속 보고 L에서 엄마 얼굴과 빈손을 확인했다. W 점화는 못 봤다.'),
})

r13_rec_actions.update({
'e2_report': r13_rec_action('돌목의 보고를 듣고 밤이의 상황을 확인한다', 'gate', [
 ('guard','밤이가 내 팔을 물었어. 저기 수레를 타고 가던 사람을 보호하던 중인데, 길에서 갑자기 달려들었지.'),('bami','그 사람 이름은 말하지 말아 줘. 또 데려가려고 할까 봐 무서워.'),
 ('dad','누구를 어디로 데려가던 중이었는지는 아직 모르겠습니다. 물림을 부정하지도, 보고만으로 격리를 정하지도 맙시다.'),
 (None,'밤이는 오늘 보호자 곁에서 쉰다. 내일 입구의 수레와 당사자들에게 실제로 본 범위를 묻는다.')],give=('e2_card_dolmok',),flags=('e2_report_seen',),day=4,episode=2),
'e2_rail': r13_rec_action('수레 난간과 소매가 걸린 자리를 살펴본다', 'gate', [
 (None,'수레 바깥쪽에서 난간에 소매천이 걸렸던 자리를 확인했다. 돌목이 벗어 둔 겉옷을 댔고, 아빠가 난간 위 손 위치만 표시했다. 안에 있는 사람에게 묶인 자세를 다시 취하라고 요구하지 않았다.'),
 ('daram','수레 밖에 곧게 서면 소매가 안 닿아. 안으로 팔을 뻗어야 닿네.'),('dad','그 자세와 맞는다는 데까지야. 천만 보고 누가 언제 물었는지 말하지는 말자.')],need=('e2_report_seen',),give=('e2_card_rail',),flags=('e2_rail_seen',),day=5,episode=2),
'e2_ties': r13_rec_action('담요를 펼쳐 두 짧은 고정끈을 확인한다', 'gate', [
 (None,'담요를 펼치자 난간 양쪽에 짧은 고리 두 개가 남았다. 담요 전체를 두르는 길이는 아니었다.'),('daram','이건 원래 뭘 묶던 거예요?'),
 ('resident_somi','그 담요는 우리가 쓰던 거야.'),('dad','솜이가 담요를 아는구나. 생긴 것만 보고 사람을 묶었다고 정하지 말고 용도를 물어보자.')],need=('e2_rail_seen',),give=('e2_card_ties',),flags=('e2_ties_seen',),day=5,episode=2),
'e2_somi': r13_rec_action('솜이에게 담요 주인과 귀가 약속을 묻는다', 'gate', [
 ('daram','수레에 있던 이 담요를 알아?'),('resident_somi','응. 내가 돌보는 분 거야. 나랑 집에 돌아오기로 했는데 보호한다며 태웠어.'),
 ('dad','손이 묶이거나 밤이가 닿는 순간도 봤니?'),('resident_somi','그건 못 봤어요. 이름과 집은 사람들 앞에서 말하지 말아 주세요.'),
 ('dad','공개할 필요가 없는 이름과 거처는 보호하자. 네가 직접 아는 귀가 약속만 기록할게.')],need=('e2_ties_seen',),give=('e2_card_somi',),flags=('e2_somi_heard',),day=5,episode=2),
'e2_bami': r13_rec_action('밤이에게 수레에서 누구를 보고 있었는지 묻는다', 'gate', [
 ('daram','소매가 난간 안쪽에 닿았어. 넌 그때 누구를 보고 있었어?'),('bami','수레 안 사람. 손을 풀어 달라고 했어. 수레 담당 바둑이도 풀어 주라고 했어.'),
 ('dad','그래서 돌목에게 어떻게 했니?'),('bami','말하면 그분이 다시 끌려갈까 봐... 이름은 말하지 말아 줘. 먼저 그 약속을 해 줘.'),
 ('dad','왜 말하기 어려운지는 알겠어. 네가 말할 범위를 먼저 정하자. 대답하지 않는다고 보호를 거두지 않겠다.')],need=('e2_somi_heard',),give=('e2_card_bami',),flags=('e2_bami_heard',),day=5,episode=2),
'e2_badook': r13_rec_action('수레 담당 바둑이에게 요구 전후를 처음부터 듣는다', 'gate', [
 ('dad','어제 이 수레를 보셨다고 들었습니다. 직접 본 순서만 말씀해 주세요.'),
 ('resident_badook','처음 봤을 때 이미 손이 난간 양쪽에 묶여 있었어요. 밤이가 손을 풀어 달라고 외쳤죠.'),
 ('resident_badook','저도 풀라고 하고 경비를 부르러 돌아섰어요. 그 뒤 비명이 들렸어요. 닿는 순간은 못 봤습니다.'),
 ('daram','비명보다 먼저 본 건 묶인 손이구나.'),('dad','회의에 갈 때도 오늘 들은 이 관찰부터 쓰자. 못 본 접촉을 보셨다고 바꾸지는 말고.')],need=('e2_bami_heard',),give=('e2_card_badook',),flags=('e2_badook_heard',),day=5,episode=2),
'e2_care': r13_rec_action('솜이와 보호받던 주민의 실제 귀가 인계를 돕는다', 'gate', [
 ('resident_somi','할아버지, 제가 옆에서 같이 갈게요.'),('resident_musoe','오늘은 집에 가자. 담요도 가져가고.'),
 (None,'무쇠가 내려서 솜이 곁에 섰다. 아빠가 수레 바퀴를 멈추고 담요를 건넸다. 두 사람은 공개 회의에 이름·거처를 알리지 않은 채 집으로 갔다.'),
 ('dad','누가 무슨 말을 했든, 집에 갈 길은 도와야지. 이제 두 분이 함께 가시는구나.')],need=('e2_somi_heard',),flags=('e2_care_complete',),day=5,episode=2),
'e3_bowls': r13_rec_action('나비에게 따로 덜어 둔 네 그릇을 묻는다', 'kitchen', [
 ('daram','이 네 그릇은 어디로 가요?'),('nabi','학교 뒤 장작창고의 꼬미, 깜이, 몽이, 방울에게요. 오늘 밤도 거기서 잔대요.'),
 ('dad','해지기 전에 학교에 물어볼게요. 자리가 있으면 아이들을 데려다줘야겠어요.')],flags=('e3_children_known',),day=5,episode=3),
'e3_meet_children': r13_rec_action('창고에서 네 아이에게 오늘 밤 계획을 듣는다', 'store', [
 ('kid_kkomi','나는 꼬미. 여기는 깜이, 몽이, 방울이야. 오늘도 여기서 잘 거야.'),('daram','학교에 잘 곳이 있으면 같이 갈래?'),
 ('kid_kkam','지금 바로 들어갈 수 있는 거야?'),('dad','먼저 잘 자리와 기다려 줄 어른이 있는지 보고 오마. 그다음 같이 가자.')],need=('e3_children_known',),flags=('e3_children_met',),day=5,episode=3),
'e3_school_place': r13_rec_action('학교의 난로·네 자리·야간 돌봄을 확인한다', 'school', [
 ('dad','창고에서 네 아이를 만났습니다. 오늘 실제로 잘 수 있는 자리가 있습니까?'),('resident_teacher','이 교실 네 자리로 오면 됩니다. 난로는 켜져 있고 오늘 밤 제가 남아요.'),
 (None,'아빠와 다람이 이불 네 채와 저녁 네 그릇을 직접 확인했다.'),('resident_teacher','해지기 전에 데리고 와 주세요. 오면 제가 한 명씩 맞겠습니다.'),
 ('dad','자리가 있구나. 아이들이 해지기 전에 올 수 있게 지금 데리러 가자.')],need=('e3_children_met',),flags=('e3_school_ready',),day=5,episode=3),
'e3_handoff': r13_rec_action('네 아이를 데리고 학교에 들어가 실제 인계한다', 'school', [
 (None,'아빠와 다람이 창고로 돌아가 네 아이와 짐을 함께 옮겼다. 해지기 전 학교 문을 열자 선생님이 맞았다.'),
 ('resident_teacher','꼬미, 깜이, 몽이, 방울. 모두 왔구나. 저녁 먹고 이 자리에서 자자.'),('kid_kkomi','오늘은 여기서 잘게. 이불도 가져왔어.'),
 ('kid_mong','창고로 돌아갈 필요 없지?'),('resident_teacher','응. 밤에도 내가 여기 있어.'),
 (None,'네 아이가 이불 자리에 앉았다. 선생님이 이름을 한 명씩 부르며 곁에 앉고, 아이들의 짐을 안쪽에 놓았다.')],need=('e3_school_ready',),give=('e3_card_handoff',),flags=('e3_handoff_complete',),day=5,episode=3),
'e3_outcome_safe': r13_rec_action('학교에서 네 아이가 무사한 아침을 확인한다', 'school', [
 ('kid_kkomi','우리는 어젯밤 여기서 잤어. 창고 쪽에서 불빛이 보여서 선생님이 어른들을 부르셨어.'),
 ('resident_teacher','네 명 모두 학교에 있었습니다. 창고 안에서 불을 본 아이는 없어요. 보리 씨가 벽을 열어 안을 찾았다고 제게 말했어요.'),
 ('dad','다들 여기 있었구나. 정말 다행이다. 불난 곳에는 우리가 다녀올게. 너희는 선생님 곁에 있자.')],need=('e3_fire_happened','e3_handoff_complete'),flags=('e3_outcome_seen',),day=6,episode=3),
'e3_outcome_loss': r13_rec_action('구조된 아이들과 꼬미의 소식을 확인한다', 'school', [
 ('resident_teacher','학교 뒤 장작창고에서 밤을 보내던 네 아이가 있었습니다. 꼬미, 깜이, 몽이, 방울이에요. 보리가 벽을 뜯고 세 아이를 데리고 나왔습니다. 꼬미는 구조대가 찾았지만 숨졌습니다.'),
 ('kid_kkam','꼬미가 우리부터 깨웠어요...'),('dad','지금은 따뜻한 곳에서 쉬자. 같은 일을 되풀이하지 않도록 바깥의 어른들에게 묻겠다.'),
 (None,'아이들에게 불 안쪽 목격을 요구하지 않았다. 조사는 살아 있는 성인과 현장 자료로 계속할 수 있다.')],need=('e3_fire_happened',),forbid=('e3_handoff_complete',),flags=('e3_outcome_seen',),day=6,episode=3),
'e3_wall': r13_rec_action('안전 확인 뒤 뜯긴 벽의 폭과 방향을 본다', 'store', [
 (None,'진화 뒤 어른이 안전을 확인한 바깥에서 벽을 보았다. 판자가 좁은 장작 틈이 아니라 사람이 지나갈 폭으로 뜯겨 있었다.'),
 ('daram','문이 있는데 왜 벽을 뜯었을까?'),('dad','어디서 와서 어느 쪽부터 손댔는지 보리 씨에게 묻자. 손의 화상만으로 의도를 맞히지는 말고.')],need=('e3_outcome_seen',),give=('e3_card_wall',),flags=('e3_wall_seen',),day=6,episode=3),
'e3_bori_safe': r13_rec_action('보리에게 불난 뒤 벽을 뜯은 이유를 묻는다', 'store', [
 ('dad','이 벽을 어느 쪽에서 뜯었습니까?'),('resident_bori','반대편 길에서 달려와 바깥부터요. 문불 때문에 들어갈 수 없었어요. 안에 애들이 있는 줄 알았죠.'),
 ('resident_bori','열고 불렀는데 아무도 없었어요. 학교로 갔다는 건 그 뒤 들었어요.'),('dad','빈 창고에서 아이를 데리고 나왔다고 기록하지 않겠습니다. 누가 점화했는지는 따로 확인해야 합니다.')],need=('e3_wall_seen','e3_handoff_complete'),give=('e3_card_bori',),flags=('e3_bori_heard',),day=6,episode=3),
'e3_bori_loss': r13_rec_action('보리에게 불난 뒤 구조한 순서를 묻는다', 'store', [
 ('dad','이 벽을 어느 쪽에서 뜯었습니까?'),('resident_bori','반대편 길에서 달려와 바깥부터요. 문이 타서 막혔어요. 벽을 뜯고 셋을 데리고 나왔어요.'),
 ('resident_bori','넷이라고 들었는데... 다시 들어가는 건 구조대가 막았어요.'),('dad','아이들을 꺼내려 한 건 들었어요. 불이 나기 전에 어디 계셨는지도 함께 확인할게요.')],need=('e3_wall_seen',),forbid=('e3_handoff_complete',),give=('e3_card_bori',),flags=('e3_bori_heard',),day=6,episode=3),
'e3_layout': r13_rec_action('등잔 자리·문밖 통·뜯긴 벽의 배치를 확인한다', 'store', [
 (None,'창고 안쪽 등잔은 넘어지지 않은 채 남았다. 문밖에는 연료통이 있고, 뜯긴 벽은 문과 떨어져 있었다.'),
 ('daram','등잔이 그대로니까 불이 어디서 시작됐는지도 알 수 있어?'),('dad','이것만으로는 안 돼. 처음 불빛과 사람의 행동을 실제 본 사람에게 묻자.')],need=('e3_bori_heard',),give=('e3_card_layout',),flags=('e3_layout_seen',),day=6,episode=3),
'e3_teacher': r13_rec_action('선생님에게 창문에서 본 순서와 시야 끝을 묻는다', 'school', [
 ('dad','문불을 처음 보셨다면서요. 그 직전부터 직접 본 범위만 말씀해 주세요.'),
 ('resident_teacher','밤에 창문에서 통 든 사람의 움직임은 보였어요. 하지만 멀고 비스듬해서 누군지는 자신 있게 말할 수 없어요. 담장 끝 M에서 창고 문 W로 가 통을 내려놓고 문앞에 불을 붙였죠.'),
 ('resident_teacher','보자마자 창에서 불이야, 창고 쪽이라고 외쳤어요. 어른들을 부르며 빈손으로 M까지 돌아오는 짧은 구간을 봤어요. 문불의 역광에 얼굴은 어두웠어요.'),
 ('resident_teacher','그 구간에 다른 사람이나 통 전달은 없었어요. 보리는 불이 난 뒤 반대편에서 왔고요. 곧바로 내려가 구조를 도왔어요.'),
 ('dad','빨래터 문 L에서 누가 나왔는지도 보셨습니까?'),('resident_teacher','아니요. 빨래터 문 쪽은 보지 못했어요. 돌아오는 걸 본 뒤에는 구조를 도우러 내려갔고요.'),],need=('e3_layout_seen',),give=('e3_card_teacher',),flags=('e3_teacher_heard',),day=6,episode=3),
'e3_can': r13_rec_action('창고 문앞 W의 통과 바로 옆 주둥이 조각을 맞춘다', 'store', [
 (None,'문앞 W에 남아 있는 통과 옆 조각의 깨진 단면을 대조했다. 둘은 맞았다.'),('daram','그럼 이 통이 여기 남아 있었네. 돌아간 건 통이 아니라 사람이야.'),
 ('dad','맞아. 통 주인이 누구인지와 그때 사용자가 누구인지는 다른 질문이다.'),
 ('resident_nubi','그 통... 빨래터에서 쓰던 건데 여기 있었네요.'),('dad','누비 씨가 알아보셨구나. 빨래터에서 직접 인계를 물어보자.')],need=('e3_layout_seen',),give=('e3_card_can',),flags=('e3_can_seen',),day=6,episode=3),
'e3_nubi': r13_rec_action('누비에게 현장에 남은 통을 보여 주고 인계를 묻는다', 'post', [
 ('dad','창고 문앞에서 이 통을 찾았습니다. 알아보시겠습니까?'),('resident_nubi','빨래터에서 쓰던 제 통이에요. 하지만 보리가 빌려 갔어요.'),
 ('dad','소유 확인만으로 사용자를 정하지 않겠습니다. 어디서 누구에게 건넸는지 회의 지도에 직접 표시해 주세요.'),
 ('resident_nubi','그럼 그때 설명하지요. 큰아이가 문에서 절 기다려요. 먼저 돌아가 볼게요.'),('dad','통은 창고 문밖에 그대로 있었어요. 선생님은 그 길에서 오가는 사람도 봤고요. 빌려줬다는 말씀을 그때 일과 맞춰 봐야겠어요.')],need=('e3_can_seen','e3_teacher_heard'),give=('e3_card_nubi',),flags=('e3_nubi_heard',),day=6,episode=3),
'e3_child_boundary': r13_rec_action('큰아이에게 귀가를 기다린 자리와 걱정을 묻는다', 'post', [
 ('dad','어젯밤 빨래터 문에서 기다렸니? 직접 본 것이 있어도 말하고 싶지 않은 건 먼저 알려 줘.'),
 ('kid_nubi1','문에서 엄마를 기다렸어요. 말하면 엄마가 붙잡히고 우리도 갈 곳이 없어질까 봐 무서워요.'),
 ('dad','잠자리와 식사는 네 진술과 상관없이 마련하겠다. 원하면 학교에서 믿을 만한 어른이 함께 듣고, 이름과 거처는 공개하지 않을 수 있어.'),
 ('kid_nubi1','그 약속이 지켜지는 곳에서 생각해 볼래요.')],need=('e3_nubi_heard',),flags=('e3_child_boundary_known',),day=6,episode=3),
'e3_child_support': r13_rec_action('큰아이의 학교 돌봄과 비공개 면담 범위를 실제 마련한다', 'school', [
 ('resident_teacher','두 아이가 지낼 자리와 저녁은 여기 준비했어요. 말하지 않아도 머물 수 있습니다. 제가 동석할게요.'),
 ('dad','이름·거처는 공개하지 않고 관찰 내용만 회의에 쓸 수 있어. 싫으면 답하지 않아도 돼. 사람을 단정할 때 어떤 말이 쓰이는지도 먼저 설명하겠다.'),
 ('kid_nubi1','알겠어요. 어디까지 말할지는 내가 정할게요.')],need=('e3_child_boundary_known',),flags=('e3_child_support_ready',),day=6,episode=3),
})

# Existing art used only as scene illustration, not as proof of new geometry.
for _r13_e3_key in ('e3_meet_children',):
    r13_rec_actions[_r13_e3_key]['background_key']='ep_woodshed_intact'
for _r13_e3_key in ('e3_wall','e3_bori_safe','e3_bori_loss','e3_layout','e3_can'):
    r13_rec_actions[_r13_e3_key]['background_key']='ep_woodshed_ruin'
for _r13_e3_key in ('e3_nubi','e3_child_boundary'):
    r13_rec_actions[_r13_e3_key]['background_key']='ep_laundry'


def r13_rec_e2_start(s):
    n=copy.deepcopy(s); n['episode']=2; n['day']=4; n['period']=2
    n.setdefault('episodes',{})['2']=dict(stage=0,privacy=None,bite_admitted=False,selected=[],verdict=None)
    return n

def r13_rec_e2_block(s):
    if s['day']==4 and 'e2_report_seen' not in s['done']: return '먼저 입구의 보고와 밤이가 말하기 어려운 이유를 듣자.'
    return None

def r13_rec_e2_advance(s):
    if r13_rec_e2_block(s): raise ValueError(r13_rec_e2_block(s))
    n=copy.deepcopy(s)
    if n['day']==4: n['day']=5
    return n

def r13_rec_e2_ready(s):
    return s.get('episode')==2 and s['day']==5 and {'e2_rail_seen','e2_ties_seen','e2_somi_heard','e2_bami_heard','e2_badook_heard'}<=set(s['done'])

def r13_rec_e2_privacy(s, allow):
    if not r13_rec_e2_ready(s): raise ValueError('Interview and protection boundary must be established first')
    n=copy.deepcopy(s); ep=n['episodes']['2']
    if ep['privacy'] is not None: return n
    ep['privacy']=bool(allow); ep['bite_admitted']=bool(allow)
    n['log'].append('e2_anonymous_consent' if allow else 'e2_respect_silence')
    return n

r13_rec_e2_steps=(
 ('돌목의 “길에서 갑자기 공격받았다”는 공간 설명을 무엇으로 검사할까?', 'e2_card_rail', '난간과 소매의 대조는 팔이 난간 안으로 뻗은 위치를 보여 준다. 물림 자체를 부정하는 자료는 아니다.'),
 ('“결박은 공격 뒤였다.” 비명 전에 실제 본 사람을 제시하자.', 'e2_card_badook', '바둑이는 비명 전 묶인 손을 봤고 풀라는 요구도 들었다. 접촉 순간을 못 봤다는 한계는 그대로다.'),
 ('“그때는 담요만 고정했다.” 목격한 두 손 위치와 무엇을 대조할까?', 'e2_card_ties', '양쪽 짧은 고리는 목격한 손 위치와 맞는다. 끈 모양만이 아니라 기존 직접 목격을 함께 쓴다.'),
 ('밤이가 물기 전에 손을 묶고 데려가려 했던 사람은 누구일까?', 'e2_card_dolmok', '돌목 씨가 먼저 한 일과 밤이가 문 일은 따로 물어야겠어요. 여기 없던 다른 사람이 했다고 바꿔 말할 수는 없고요.'),
)

def r13_rec_e2_present(s, card):
    if not r13_rec_e2_ready(s) or s['episodes']['2']['privacy'] is None or card not in s['facts']: raise ValueError('Unearned card or hearing not ready')
    n=copy.deepcopy(s); ep=n['episodes']['2']; step=ep['stage']
    if ep['verdict'] is not None or step>=len(r13_rec_e2_steps): raise ValueError('Hearing already at reconstruction or complete')
    if card!=r13_rec_e2_steps[step][1]: return n,'이걸 본 때와 지금 묻는 때가 달라. 그 순간을 직접 본 사람의 말부터 다시 보자.',False
    ep['stage']+=1; ep['selected'].append(card)
    return n,r13_rec_e2_steps[step][2],True

def r13_rec_e2_reconstruct(s, sequence):
    n=copy.deepcopy(s); ep=n['episodes']['2']
    if not r13_rec_e2_ready(s) or ep['stage']!=4 or ep['verdict'] is not None: raise ValueError('Reconstruction not ready')
    expected='restraint_request_reach_bite' if ep['bite_admitted'] else 'restraint_request_cry_unconfirmed'
    if sequence!=expected: return n,'바둑이 씨는 비명 전에 묶인 손을 봤어. 그 뒤 일은 밤이가 실제로 말해 준 데까지만 이어 보자.',False
    ep['verdict']='bite_and_prior_coercion' if ep['bite_admitted'] else 'prior_coercion_contact_unconfirmed'
    ep['stage']=5; n['done']=list(dict.fromkeys(n['done']+['e2_resolved'])); n['log'].append('e2_verdict:'+ep['verdict'])
    return n,('먼저 손을 묶었고, 풀어 달라는 말 뒤에 팔을 뻗었군요. 밤이가 문 건 맞지만, 그 전에 억지로 데려가려 한 일도 그냥 넘길 수는 없어요.' if ep['bite_admitted'] else '비명 전부터 손이 묶여 있었고 풀어 달라는 말도 있었어요. 밤이가 아직 말하지 않은 순간을 우리가 채워 넣지는 맙시다. 그래도 물어서 묶었다는 설명은 순서가 맞지 않아요.'),True

def r13_rec_e3_location_info(s, location):
    if location=='store': return ('학교 뒤 장작창고', 'ep_woodshed_intact' if s['day']==5 else 'ep_woodshed_ruin')
    if location=='post': return ('여관 뒤 빨래터', 'ep_laundry')
    return None


def r13_rec_e3_start(s):
    n=copy.deepcopy(s); n['episode']=3; n['day']=5; n['period']=1
    n.setdefault('episodes',{})['3']=dict(stage=0,privacy=None,selected=[],verdict=None,fire=False,children='warehouse',kkomi='alive',map_step=0,map_answers=[],geometry_seen=False,sightline_gap=False,other_crossing=False)
    return n

def r13_rec_e3_handoff(s):
    n=copy.deepcopy(s)
    if n['day']!=5 or n['episodes']['3']['fire']: raise ValueError('Handoff cannot rewrite the fire')
    n['e3_school_handoff']=True; n['episodes']['3']['children']='school'; n['episodes']['3']['kkomi']='alive'
    return n

def r13_rec_e3_block(s):
    # Missing an optional warning changes the outcome, never freezes the calendar.
    return None

def r13_rec_e3_advance(s):
    if r13_rec_e3_block(s): raise ValueError(r13_rec_e3_block(s))
    n=copy.deepcopy(s)
    if n['day']==5:
        n['day']=6; ep=n['episodes']['3']; ep['fire']=True
        if n.get('e3_school_handoff') and 'e3_handoff_complete' in n['done']:
            ep['children']='school'; ep['kkomi']='alive'
        else: ep['children']='three_rescued'; ep['kkomi']='dead'
        n['done']=list(dict.fromkeys(n['done']+['e3_fire_happened']))
    return n

def r13_rec_e3_ready(s):
    return s.get('episode')==3 and s['day']==6 and {'e3_wall_seen','e3_layout_seen','e3_can_seen','e3_bori_heard','e3_teacher_heard','e3_nubi_heard'}<=set(s['done'])

def r13_rec_e3_privacy(s, allow):
    if not r13_rec_e3_ready(s): raise ValueError('Fire investigation not ready')
    if allow and 'e3_child_support_ready' not in s['done']: raise ValueError('Actual support must precede testimony')
    n=copy.deepcopy(s); ep=n['episodes']['3']
    if ep['privacy'] is not None: return n
    ep['privacy']=bool(allow)
    if allow:
        n['facts']=list(dict.fromkeys(n['facts']+['e3_card_child'])); n['observed']['e3_card_child']=s['day']; n['done'].append('e3_child_heard')
    n['log'].append('e3_private_testimony' if allow else 'e3_respect_silence')
    return n

r13_rec_e3_steps=(
 ('“벽을 뜯었으니 장작 도둑이 불을 냈다.” 실제 만든 통로를 제시하자.', 'e3_card_wall', '이 구멍은 사람이 빠져나올 만큼 커요. 벽을 연 것과 그 전에 불을 붙인 것은 다른 일이에요. 벽 하나만 보고 누가 불을 냈다고 할 수는 없죠.'),
 ('보리가 도착하기 전 문앞 점화와 빈손 귀환을 본 사람을 제시하자.', 'e3_card_teacher', '선생님은 M–W 행동과 보리의 뒤늦은 반대편 도착을 봤다. 점화자의 얼굴과 L의 출발은 모른다.'),
 ('“내 통을 보리에게 빌려줬다.” 먼저 실제로 남은 물체를 제시하자.', 'e3_card_can', '통은 W에 남았다. 소유자를 사용자로 바꾸지 말고, 이제 주장한 전달 지점과 실제 관찰을 대조하자.'),
)

def r13_rec_e3_present(s, card):
    if not r13_rec_e3_ready(s) or s['episodes']['3']['privacy'] is None or card not in s['facts']: raise ValueError('Unearned card or hearing not ready')
    n=copy.deepcopy(s); ep=n['episodes']['3']; step=ep['stage']
    if ep['verdict'] is not None or step>=3: raise ValueError('Field presentation complete')
    if card!=r13_rec_e3_steps[step][1]: return n,'자료가 보여 주는 범위를 다시 보자. 소유·구조·착화는 서로 다른 주장이다.',False
    ep['stage']+=1; ep['selected'].append(card)
    return n,r13_rec_e3_steps[step][2],True

r13_rec_e3_map_questions=(
 ('통이 실제로 이동한 화살표는 어디서 끝날까?',('W','L','M'),'W','통은 창고 문앞 W에서 발견됐다. 통을 L까지 되돌리면 실제 발견 위치와 모순이다.'),
 ('빈손인 사람의 귀환 화살표는 어디까지 이어질까?',('L','W','M'),'L','사람만 W→M→L로 돌아온다는 주장이다. 큰아이는 L 얼굴·빈손을, 교사는 W→M을 본다.'),
 ('큰아이 카드의 연속 관찰 구간은?',('L-M','M-W','L-W'),'L-M','큰아이는 W 점화를 못 봤다. L–M 및 M 주변 겹침까지만 놓자.'),
 ('선생님 카드의 연속 관찰 구간은?',('M-W','L-M','L-W'),'M-W','교사는 L 출발을 못 봤다. M–W 및 M 주변 겹침까지만 놓자.'),
 ('누비가 새로 주장한 M의 통 전달은 어느 범위와 충돌할까?',('overlap','outside','unknown'),'overlap','M 주변 4–6은 두 시야가 겹치는 제안 구간이다. 실제 연속 시야가 검증돼야 인계 대안을 배제할 수 있다.'),
)

def r13_rec_e3_map_answer(s, answer):
    n=copy.deepcopy(s); ep=n['episodes']['3']
    if ep['stage']!=3 or not ep['privacy'] or 'e3_card_child' not in s['facts'] or ep['verdict'] is not None: raise ValueError('Need both actual witness cards')
    step=ep['map_step']
    if step>=5: raise ValueError('Map complete')
    q=r13_rec_e3_map_questions[step]; ep['geometry_seen']=True
    if answer!=q[2]: return n,q[3],False
    ep['map_answers'].append(answer); ep['map_step']+=1
    return n,q[3],True

def r13_rec_e3_can_identify(s):
    ep=s['episodes']['3']
    return bool(r13_rec_e3_geometry_ready(s) and ep['privacy'] and ep['map_step']==5 and not ep['sightline_gap'] and not ep['other_crossing'] and {'e3_card_teacher','e3_card_child','e3_card_nubi','e3_card_can','e3_card_layout'}<=set(s['facts']))

def r13_rec_e3_finish(s, person=None):
    n=copy.deepcopy(s); ep=n['episodes']['3']
    if ep['stage']!=3 or ep['verdict'] is not None: raise ValueError('Conclusion not ready')
    if ep['privacy'] and ep['map_step']!=5: raise ValueError('Finish the actual arrow and sightline inputs first')
    if person is not None and person not in s['facts']: raise ValueError('Unearned person card')
    if ep['privacy'] and person!='e3_card_nubi': return n,'인계 주장을 한 사람의 카드를 골라 경로와 대조하자. 지목만으로 유죄가 되지는 않는다.',False
    if r13_rec_e3_can_identify(s): ep['verdict']='nubi_ignition_bori_afterward'
    elif not ep['privacy']: ep['verdict']='partial_no_child_testimony'
    elif ep['sightline_gap'] or ep['other_crossing']: ep['verdict']='partial_sightline_gap'
    else: ep['verdict']='partial_geometry_unverified'
    ep['stage']=4; n['done']=list(dict.fromkeys(n['done']+['e3_resolved'])); n['log'].append('e3_verdict:'+ep['verdict'])
    if ep['verdict']=='nubi_ignition_bori_afterward': msg='문밖에서 불을 붙인 사람과 그 뒤 벽을 연 사람은 다릅니다. 앞뒤 이동을 함께 보면 누비 씨의 점화와 보리 씨의 구조를 구별할 수 있습니다. 하지만 사람을 죽이려 했는지, 너울 씨가 그렇게 지시했는지까지 입증한 것은 아닙니다.'
    else: msg='보리 씨 혼자 불을 냈다는 주장은 목격 순서와 맞지 않습니다. 누비 씨의 대여 설명에는 의문이 남지만, 아직 누가 문밖에서 불을 붙였는지 확정할 수는 없습니다. 보리 씨를 그 혐의만으로 붙잡아 두지 말아 주세요.'
    return n,msg,True

# Stable scene-click targets, consumed by the shared location UI.
_r13_e2_people={'e2_report':'guard','e2_somi':'resident_somi','e2_bami':'bami','e2_badook':'resident_badook','e2_care':'resident_somi'}
_r13_e3_people={'e3_bowls':'nabi','e3_meet_children':'kid_kkomi','e3_school_place':'resident_teacher','e3_handoff':'resident_teacher','e3_outcome_safe':'kid_kkomi','e3_outcome_loss':'resident_teacher','e3_bori_safe':'resident_bori','e3_bori_loss':'resident_bori','e3_teacher':'resident_teacher','e3_nubi':'resident_nubi','e3_child_boundary':'kid_nubi1','e3_child_support':'resident_teacher'}
for _r13_e2_key,_r13_e2_person in list(_r13_e2_people.items())+list(_r13_e3_people.items()):
    r13_rec_actions[_r13_e2_key]['target_person']=_r13_e2_person
for _r13_e2_key,_r13_e2_object in {'e2_rail':'수레 난간과 소매천','e2_ties':'담요와 짧은 두 고리','e3_wall':'뜯긴 벽 가장자리','e3_layout':'등잔·문·벽 배치','e3_can':'문앞 통과 주둥이 조각'}.items():
    r13_rec_actions[_r13_e2_key]['target_object']=_r13_e2_object

r13_rec_location_overrides[3]=r13_rec_e3_location_info
r13_rec_effects['e3_handoff']=r13_rec_e3_handoff
r13_rec_episodes.update({2:dict(title='사건2 C · 밤이는 물었다',start_day=4,end_day=5,hearing_label='r13_recommended_ep2_hearing',next_label=None),3:dict(title='사건3 A · 불은 문을 막으러 왔다',start_day=5,end_day=6,hearing_label='r13_recommended_ep3_hearing',next_label=None)})
r13_rec_episode_start.update({2:r13_rec_e2_start,3:r13_rec_e3_start})
r13_rec_day_advance.update({2:r13_rec_e2_advance,3:r13_rec_e3_advance})
r13_rec_advance_block.update({2:r13_rec_e2_block,3:r13_rec_e3_block})
r13_rec_episode_done.update({2:lambda s: s.get('episodes',{}).get('2',{}).get('verdict') is not None,3:lambda s: s.get('episodes',{}).get('3',{}).get('verdict') is not None})

# These actions explicitly take place before sunset, never after an evening skip.
for _key in ("e3_bowls","e3_meet_children","e3_school_place","e3_handoff"):
    r13_rec_actions[_key]["max_period"]=1
